"""The lineup event model: five attackers, five defenders, one possession ledger.

This is a flat implementation of the retained reference (J_POINT_BOTH): the v14
offense (RB_RENEW_FAC), v15 broadcast defense (D_MAIN_RB) and v16 adjusted
capability heads, without the version inheritance chain. ``tests/test_model_parity``
checks it against saved fits.

Shapes: B rows (game x offense five x defense five), 5 players, float32 inputs.

Inputs per row (all standardized upstream):
    base              [B,5,18]  dated offensive state, the decoder's anchor
    msg               [B,5,18]  the same state as the teammate-context input
    role              [B,5,8]   recent-minus-long contrasts and historical teammate context
    rb_input          [B,5,28]  rebound-head input
    rb_prior          [B,5]     prior offensive-rebound capture share
    league_capture    [B]       league offensive capture rate
    adjusted_offense  [B,5,97]  adjusted own/teammate-influence capability bank
    adjusted_defense  [B,5,49]  adjusted defender capability bank
    defense           [B,5,19]  dated defender descriptors

Environment: ``budget`` (non-rebound opportunity budget per possession),
``non_rebound`` (initial possessions), ``eta`` (eligible live-miss rate).

The 18 state coordinates are 3 log rates (FGA, FTA, TO), 6 location logits,
6 location make logits, FT make logit, log assist rate and assisted-make logit.
"""
from types import SimpleNamespace

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

N_STATE = 18
FT_MAKE = 15          # teammates and opponents never move a shooter's FT%
SUPPLY = 16           # log assist rate: passing supply
ASSISTED = 17         # assisted-make logit: finishing demand
SHOT_VALUES = (2., 2., 2., 2., 3., 3.)
USAGE_WEIGHTS = (1., .44, 1.)  # FGA + .44 FTA + TO = one opportunity
ADJUSTED_OFFENSE = 97
ADJUSTED_DEFENSE = 49
DEFENSE = 19
ROLE = 8
REBOUND_INPUT = 28


def mlp(inputs, outputs, width=32):
    """Linear-tanh-linear with a zero output layer, so new heads start at zero."""
    net = nn.Sequential(nn.Linear(inputs, width), nn.Tanh(), nn.Linear(width, outputs))
    nn.init.zeros_(net[-1].weight)
    nn.init.zeros_(net[-1].bias)
    return net


def centered(net, values):
    """Head output relative to its value at the all-zero (average) input."""
    return net(values) - net(torch.zeros_like(values))


def moments(values, leave_one_out=False):
    """Mean and SD over players; leave-one-out excludes the receiving player."""
    if leave_one_out:
        mean = (values.sum(1, keepdim=True) - values) / 4
        var = ((values * values).sum(1, keepdim=True) - values * values) / 4 - mean.square()
    else:
        mean = values.mean(1, keepdim=True)
        var = values.var(1, unbiased=False, keepdim=True)
    sd = torch.where(var > 0, var.clamp(min=1e-8).sqrt(), torch.zeros_like(var))
    return torch.cat([mean, sd], -1)


def mask_free_throw(effect):
    return torch.cat([effect[..., :FT_MAKE], torch.zeros_like(effect[..., FT_MAKE:FT_MAKE + 1]),
                      effect[..., FT_MAKE + 1:]], -1)


class Backbone(nn.Module):
    """Offensive state: own anchor + teammate context + role history, then decoder.

    Teammate context reads the other four players' mean and SD (leave-one-out).
    The decoder is a coordinate-wise affine map. k_* are the nonnegative
    creation-shortage, FT-shortage and overload penalty coefficients.
    """

    def __init__(self):
        super().__init__()
        self.context = nn.Linear(2 * N_STATE, 32)
        self.context_sd = nn.Linear(N_STATE, 32, bias=False)
        self.context_out = nn.Linear(32, N_STATE)
        self.role = mlp(N_STATE + ROLE, N_STATE)
        self.intercept = nn.Parameter(torch.zeros(N_STATE))
        self.raw_slope = nn.Parameter(torch.full((N_STATE,), 0.5413248546129181))  # softplus^-1(1)
        self.k_supply = nn.Parameter(torch.zeros(()))
        self.k_ft = nn.Parameter(torch.zeros(()))
        self.k_load = nn.Parameter(torch.zeros(6))

    def state(self, base, x, role):
        mean = (x.sum(1, keepdim=True) - x) / 4
        var = ((x * x).sum(1, keepdim=True) - x * x) / 4 - mean.square()
        sd = var.clamp(min=1e-8).sqrt()
        hidden = torch.tanh(self.context(torch.cat([x, mean], -1)) + self.context_sd(sd))
        message = self.context_out(hidden) + self.role(torch.cat([x, role], -1))
        return base + mask_free_throw(message)

    def decode(self, state):
        return self.intercept + F.softplus(self.raw_slope) * state


class BroadcastDefense(nn.Module):
    """Defense as one lineup-level shift, identical for all five attackers.

    Reads the defenders' mean and SD. Produces 15 bounded log-rate/logit
    effects (3 actions, 6 locations, 6 conversions) and a recovery strength.
    """

    def __init__(self):
        super().__init__()
        self.main = mlp(2 * DEFENSE, 15)
        self.recovery = mlp(2 * DEFENSE, 1)

    def forward(self, defense):
        z = torch.cat([defense.mean(1), defense.var(1, unbiased=False).clamp(min=1e-12).sqrt()], -1)
        effect = torch.tanh(centered(self.main, z)[:, None, :]).expand(-1, 5, -1)
        recovery = torch.tanh(centered(self.recovery, z).squeeze(-1))
        return effect, recovery


class Rebound(nn.Module):
    """Offensive collector scores: prior odds + own skill + teammates' facilitation."""

    def __init__(self):
        super().__init__()
        self.own = mlp(REBOUND_INPUT, 1, 16)
        self.donor = mlp(REBOUND_INPUT, 1, 16)

    def forward(self, x, prior, league):
        own = 2 * torch.tanh(self.own(x).squeeze(-1))
        donor = 2 * torch.tanh(centered(self.donor, x).squeeze(-1))
        facilitation = (donor.sum(1, keepdim=True) - donor) / 4
        league = torch.as_tensor(league, dtype=x.dtype, device=x.device)
        if league.ndim == 1:
            league = league[:, None]
        score = prior.clamp(1e-6, 1 - 1e-6).log() - torch.log1p(-league.clamp(1e-6, 1 - 1e-6)) + own + facilitation
        return score.double()


class AdjustedHeads(nn.Module):
    """Bounded effects of the adjusted capability banks (own, teammates, defenders)."""

    def __init__(self):
        super().__init__()
        self.own = mlp(ADJUSTED_OFFENSE, 16)
        self.teammate = mlp(2 * ADJUSTED_OFFENSE, 15)
        self.donor = mlp(ADJUSTED_OFFENSE, 1)
        self.defense = mlp(2 * ADJUSTED_DEFENSE, 16)

    def offense(self, adjusted):
        own = torch.tanh(centered(self.own, adjusted))
        teammates = torch.tanh(centered(self.teammate, moments(adjusted, True)))
        donor = torch.tanh(centered(self.donor, adjusted).squeeze(-1))
        rebound = own[..., 15] + (donor.sum(1, keepdim=True) - donor) / 4
        return own[..., :15] + teammates, rebound

    def defense_effect(self, adjusted):
        return torch.tanh(centered(self.defense, moments(adjusted)[:, 0]))


SPACER_3PA = 8.       # 3PA per 100 possessions at which an attacker fully tethers his defender
MEAN_SPACING = .5


def gather(values, index):
    """values [B,5,F] reordered by slot index [B,5]."""
    return torch.gather(values, 1, index[..., None].expand(-1, -1, values.shape[-1]))


class Coverage(nn.Module):
    """Defense through an explicit assignment, one defender per attacker (optional; not in the reference).

    Needs the batch listings (lineups.features): ``matched`` pairs each attacker
    with a defender by sorted listed position.

    matched  Each attacker's 15 effects depend on its own state and listings and
             on its assigned defender's descriptors, capability bank and listings.
    help     Team help H = sum_j a_j h_j. h_j >= 0 is defender j's help capacity;
             a_j = 1 - kappa * s_j discounts a defender whose assigned attacker is a
             floor spacer (s from that attacker's own 3PA rate, full at SPACER_3PA
             per 100). kappa in [0, 1] is learned. Every attacker's 15 effects
             move monotonically in H, relative to five average defenders.

    Both parts are bounded and output exactly zero at initialization, so a model
    with coverage starts at the function of the same model without it.
    """

    def __init__(self, matched=True, help_term=False):
        super().__init__()
        side = 2   # standardized listed height and position
        self.matched = mlp(N_STATE + side + DEFENSE + ADJUSTED_DEFENSE + side, 15) if matched else None
        if help_term:
            self.capacity = nn.Linear(DEFENSE + ADJUSTED_DEFENSE + side, 1)
            self.raw_kappa = nn.Parameter(torch.zeros(()))
            self.help_effect = nn.Parameter(torch.zeros(15))
        self.has_help = help_term

    def kappa(self):
        return self.raw_kappa.clamp(0, 1)

    def forward(self, batch):
        matched = batch["matched"]
        defenders = torch.cat([batch["defense"], batch["adjusted_defense"], batch["defense_height"][..., None],
                               batch["defense_position"][..., None]], -1)
        effect = 0.
        if self.matched is not None:
            attackers = torch.cat([batch["msg"], batch["offense_height"][..., None],
                                   batch["offense_position"][..., None]], -1)
            effect = effect + torch.tanh(centered(self.matched, torch.cat([attackers, gather(defenders, matched)], -1)))
        if self.has_help:
            base = batch["base"]
            three = 100 * base[..., 0].clamp(-12, 4).exp() * torch.softmax(base[..., 3:9], -1)[..., 4:].sum(-1)
            spacing = (three / SPACER_3PA).clamp(0, 1)
            # The attacker each defender is assigned to: invert the attacker -> defender pairing.
            guarding = torch.argsort(matched, 1)
            available = 1 - self.kappa() * torch.gather(spacing, 1, guarding)
            help_total = (available * F.softplus(self.capacity(defenders)).squeeze(-1)).sum(1)
            average = 5 * F.softplus(self.capacity.bias) * (1 - self.kappa() * MEAN_SPACING)
            effect = effect + torch.tanh(self.help_effect * (help_total - average)[:, None, None])
        return effect


class Creation(nn.Module):
    """Offense through specific teammates rather than the teammate average (optional; not in the reference).

    Each attacker's 15 offensive coordinates (action rates, locations,
    conversions) get a bounded correction from his own state, his best-passing
    teammate's state (highest dated assist rate among the other four) and his
    best-shooting teammate's state (highest dated 3PA rate). Like the capacity
    defense, the inputs are always real individual players, so five centers
    read as "a center whose best passer and best shooter are centers" rather
    than an out-of-range teammate mean. Zero at initialization.
    """

    def __init__(self):
        super().__init__()
        self.net = mlp(3 * N_STATE, 15)

    def forward(self, batch):
        base = batch["base"]
        passing = base[..., SUPPLY]
        shooting = base[..., 0].clamp(-12, 4).exp() * torch.softmax(base[..., 3:9], -1)[..., 4:].sum(-1)
        self_mask = torch.eye(5, dtype=torch.bool, device=base.device)

        def best(score):
            others = score[:, None, :].expand(-1, 5, -1).masked_fill(self_mask, -torch.inf)
            return others.argmax(-1)

        msg = batch["msg"]
        x = torch.cat([msg, gather(msg, best(passing)), gather(msg, best(shooting))], -1)
        return torch.tanh(centered(self.net, x))


INSIDE = (3, 4, 9, 10)                  # rim and paint location and conversion
PERIMETER = (5, 6, 7, 8, 11, 12, 13, 14)  # mid-range and three-point location and conversion
PRESSURE = (0, 1, 2)                     # FGA, FTA and turnover rates
BLOCK, DEFENSIVE_REBOUND = 1, 2          # raw defensive descriptor columns


class CapacityDefense(nn.Module):
    """Defense under declared capacity laws (an assumption model; not the reference).

    Every defender is described by x_j = [raw descriptors, adjusted capability
    bank, listed height, listed position]. No input averages the five
    defenders: each pooled input is a set of real individual defenders, so an
    impossible lineup maps to inputs that real lineups also produce. The 15
    effects are split by where they happen:

    one rim       Rim and paint location and conversion, and rebound recovery,
                  read only the two defenders with the most inside presence
                  (standardized blocks + defensive rebounds; ties by player id).
                  Five centers look like a real two-big lineup inside.
    five for five Mid-range and three-point location and conversion for each
                  attacker read his own state and listings and his assigned
                  defender (sorted listed position; lineups.features).
    pressure      Each attacker's FGA, FTA and turnover rates read his own
                  state, his assigned defender and the two inside defenders.

    The heads are learned, bounded and zero at initialization. Only the pooling
    is asserted. This is version 2. Version 1 (commit 6f5e7b67) read pressure
    from the mean of all five, and its five-center inputs extrapolated. Version 3
    (screened 2026-10-09, not kept) fed listings only to the assignment; it was
    slightly less accurate and did not fix the perimeter-coverage property.
    """

    def __init__(self):
        super().__init__()
        width = DEFENSE + ADJUSTED_DEFENSE + 2
        attacker = N_STATE + 2
        self.pressure = mlp(attacker + 3 * width, len(PRESSURE))
        self.inside = mlp(2 * width, len(INSIDE) + 1)
        self.perimeter = mlp(attacker + width, len(PERIMETER))

    def forward(self, batch):
        x = torch.cat([batch["defense"], batch["adjusted_defense"], batch["defense_height"][..., None],
                       batch["defense_position"][..., None]], -1)
        presence = batch["defense"][..., BLOCK] + batch["defense"][..., DEFENSIVE_REBOUND] + batch["defense_tiebreak"]
        top = torch.argsort(presence, dim=1, descending=True, stable=True)[:, :2]
        pool = gather(x, top).flatten(1)
        inside = torch.tanh(centered(self.inside, pool))
        attackers = torch.cat([batch["msg"], batch["offense_height"][..., None],
                               batch["offense_position"][..., None]], -1)
        assigned = gather(x, batch["matched"])
        perimeter = torch.tanh(centered(self.perimeter, torch.cat([attackers, assigned], -1)))
        pressure = torch.tanh(centered(self.pressure, torch.cat([attackers, assigned,
                                                                 pool[:, None].expand(-1, 5, -1)], -1)))
        effect = x.new_zeros(*perimeter.shape[:2], 15)
        effect[..., list(PRESSURE)] = pressure
        effect[..., list(INSIDE)] = inside[:, None, :len(INSIDE)].expand(-1, 5, -1)
        effect[..., list(PERIMETER)] = perimeter
        return effect, inside[:, len(INSIDE)]


class PairInteractions(nn.Module):
    """Explicit pairwise interactions between teammates and between defenders (exploratory screens).

    reports/nonlinearity_screen_protocol_2026_10_13.md and ..._screen2_protocol_2026_10_13.md.
    Identity-free: the inputs are the capability states the network already reads, plus listed height.

    A centered feature map g = tanh(W s + b) - tanh(b) gives every player PAIR_WIDTH features.
    - Offense: player i's 15 log-rate/logit corrections are
      tanh(sum_r (U g_i)_r * partners_ir), partners_i = sum_{j != i} V g_j, rank PAIR_RANK.
    - Defense: one lineup-level shift for all attackers,
      tanh(1/2 sum_l sum_r (P h_l)_r * partners_lr), partners_l = sum_{j != l} Q h_j.

    U and P start at zero, so a model starts at its parent's function. The
    interactions are first order in U and P, so gradient descent reaches them
    as readily as main effects; the existing heads mix teammates only through
    tanh curvature. The tanh bounds each correction at +-1, like the other heads.

    hold holds the module at its measured range when forecasting, the
    continuous analogue of holding type counts at the measured maximum
    (lineups.combinations). Ranges are the 0.5% and 99.5% quantiles over
    training rows, saved with the weights.
    - "inputs" (second screen): every partner sum, per component; running
      values (momentum HOLD_MOMENTUM) kept in training.
    - "outputs" (third screen): each player's 15 offensive corrections, then
      their sum over the lineup (all five scaled alike, so the sum reaches the
      nearer bound), and the defensive shift. Set by bound_outputs from
      unclamped outputs on training rows; lineup ranges include 0.
    - "joint" (fourth screen): "outputs", then the lineup's 15-channel
      offensive sum and the defensive shift each held inside an ellipsoid
      around no interaction: T' M^-1 T <= r^2, M the second moment of T over
      training rows (after the per-channel holds) and r the 99.5% quantile
      of that distance. Outside it, the lineup's outputs are scaled by r/d.

    centered=True (sixth screen) makes the module a pure interaction: the
    feature maps g and h are centered on their mean over training players
    (the batch mean in training, as batch normalization does; a running mean,
    momentum HOLD_MOMENTUM, when forecasting). U g and V g are then centered
    too, so neither a player's own features nor a partner's adds a main
    effect or a level on average; only their combination does.
    """
    HOLD_QUANTILES, HOLD_MOMENTUM = (.005, .995), .05

    def __init__(self, rank=4, width=16, hold=None, centered=False):
        super().__init__()
        assert hold in (None, "inputs", "outputs", "joint")
        self.rank, self.hold, self.centered = rank, hold, centered
        self.offense_map = nn.Linear(N_STATE + 3, width)
        self.defense_map = nn.Linear(DEFENSE + 1, width)
        self.u, self.v = nn.Linear(width, 15 * rank, bias=False), nn.Linear(width, 15 * rank, bias=False)
        self.p, self.q = nn.Linear(width, 15 * rank, bias=False), nn.Linear(width, 15 * rank, bias=False)
        nn.init.zeros_(self.u.weight)
        nn.init.zeros_(self.p.weight)
        if hold == "inputs":
            for side in ("offense", "defense"):
                self.register_buffer(f"{side}_range", torch.zeros(2, 15 * rank))
            self.register_buffer("seen", torch.zeros((), dtype=torch.bool))
        if hold in ("outputs", "joint"):
            for name in ("player_bounds", "lineup_bounds", "defense_bounds"):
                self.register_buffer(name, torch.zeros(2, 15))
            self.register_buffer("measured", torch.zeros((), dtype=torch.bool))
        if hold == "joint":
            for side in ("lineup", "defense"):
                self.register_buffer(f"{side}_metric", torch.zeros(15, 15))
                self.register_buffer(f"{side}_radius", torch.zeros(()))
        if centered:
            for side in ("offense", "defense"):
                self.register_buffer(f"{side}_center", torch.zeros(width))
            self.register_buffer("centers_seen", torch.zeros((), dtype=torch.bool))

    @staticmethod
    def features(layer, s):
        return torch.tanh(layer(s)) - torch.tanh(layer.bias)

    def center(self, g, side):
        """Pure interaction: subtract the features' mean over players (batch mean in training)."""
        if not self.centered:
            return g
        running = getattr(self, f"{side}_center")
        if self.training:
            mean = g.reshape(-1, g.shape[-1]).mean(0)
            with torch.no_grad():
                running.copy_(mean.detach() if not bool(self.centers_seen)
                              else running + self.HOLD_MOMENTUM * (mean.detach() - running))
            return g - mean
        return g - running

    def held(self, partners, side):
        """Track the measured range in training; clamp to it when forecasting."""
        if self.hold != "inputs":
            return partners
        flat = partners.reshape(-1, 15 * self.rank)
        bounds = getattr(self, f"{side}_range")
        if self.training:
            with torch.no_grad():
                q = torch.quantile(flat.detach().float(), torch.tensor(self.HOLD_QUANTILES), dim=0)
                bounds.copy_(q if not bool(self.seen) else bounds + self.HOLD_MOMENTUM * (q - bounds))
            return partners
        return torch.maximum(torch.minimum(flat, bounds[1]), bounds[0]).view_as(partners)

    def forward(self, batch):
        shape = lambda t: t.view(*t.shape[:2], 15, self.rank)
        s = torch.cat([batch["msg"], batch["rb_input"][..., -2:], batch["offense_height"][..., None]], -1)
        g = self.center(self.features(self.offense_map, s), "offense")
        u, v = shape(self.u(g)), shape(self.v(g))
        offense = torch.tanh((u * self.held(v.sum(1, keepdim=True) - v, "offense")).sum(-1))
        h = self.center(self.features(self.defense_map, torch.cat([batch["defense"], batch["defense_height"][..., None]], -1)),
                        "defense")
        p, q = shape(self.p(h)), shape(self.q(h))
        pairs = torch.tanh((p * self.held(q.sum(1, keepdim=True) - q, "defense")).sum((1, 3)) / 2)
        if self.hold == "inputs" and self.training:
            self.seen.fill_(True)
        if self.centered and self.training:
            self.centers_seen.fill_(True)
        if self.hold in ("outputs", "joint") and not self.training and bool(self.measured):
            offense, pairs = self.held_outputs(offense, pairs)
        return offense, pairs[:, None, :].expand(-1, 5, -1)

    @torch.no_grad()
    def bound_outputs(self, offense, defense):
        """Measured output ranges from unclamped outputs on training rows: offense [N, 5, 15], defense [N, 15]."""
        q = lambda x: torch.as_tensor(np.quantile(x.double().numpy(), self.HOLD_QUANTILES, axis=0), dtype=torch.float32)
        with_zero = lambda r: torch.stack([r[0].clamp(max=0), r[1].clamp(min=0)])
        self.player_bounds.copy_(q(offense.reshape(-1, 15)))
        self.lineup_bounds.copy_(with_zero(q(offense.sum(1))))
        self.defense_bounds.copy_(with_zero(q(defense)))
        if self.hold == "joint":
            offense, defense = self.channel_holds(offense.float(), defense.float())
            for side, t in (("lineup", offense.sum(1)), ("defense", defense)):
                t = t.double()
                m = t.T @ t / len(t)
                inverse = torch.linalg.inv(m + 1e-6 * m.trace() / 15 * torch.eye(15, dtype=m.dtype))
                distance = ((t @ inverse) * t).sum(-1).clamp(min=0).sqrt()
                getattr(self, f"{side}_metric").copy_(inverse.float())
                getattr(self, f"{side}_radius").fill_(float(np.quantile(distance.numpy(), self.HOLD_QUANTILES[1])))
        self.measured.fill_(True)

    def channel_holds(self, offense, defense):
        clamp = lambda x, b: torch.maximum(torch.minimum(x, b[1]), b[0])
        offense = clamp(offense, self.player_bounds)
        total = offense.sum(1)
        target = clamp(total, self.lineup_bounds)
        outside, one = target != total, torch.ones_like(total)
        scale = torch.where(outside, target / torch.where(outside, total, one), one)  # range includes 0: total != 0
        return offense * scale[:, None, :], clamp(defense, self.defense_bounds)

    @staticmethod
    def joint_scale(total, metric, radius):
        distance = ((total @ metric) * total).sum(-1).clamp(min=0).sqrt()
        return torch.where(distance > radius, radius / distance.clamp(min=1e-12), torch.ones_like(distance))

    def held_outputs(self, offense, defense):
        offense, defense = self.channel_holds(offense, defense)
        if self.hold == "joint":
            offense = offense * self.joint_scale(offense.sum(1), self.lineup_metric, self.lineup_radius)[:, None, None]
            defense = defense * self.joint_scale(defense, self.defense_metric, self.defense_radius)[:, None]
        return offense, defense


def renewal(non_rebound, miss_per_cycle, score):
    """Stationary renewal: B(1+H)/(1+(1-m)H), H = sum of collector odds."""
    m = miss_per_cycle.double()
    b = torch.as_tensor(non_rebound, dtype=m.dtype, device=m.device)
    if not torch.isfinite(m).all() or (m < 0).any() or (m > 1).any() or (b <= 0).any():
        raise ValueError("invalid renewal inputs")
    log_h = torch.logsumexp(score.double(), 1)
    zero = torch.zeros_like(log_h)
    usage = b * torch.exp(torch.logaddexp(zero, log_h) - torch.logaddexp(zero, torch.log1p(-m) + log_h))
    continuation = m * torch.sigmoid(log_h)
    if not torch.isfinite(usage).all() or (continuation >= 1).any():
        raise FloatingPointError("nonterminating renewal")
    return usage, usage * continuation, continuation


class EventModel(nn.Module):
    """Expected per-possession event ledger for an offense five against a defense five."""

    def __init__(self):
        super().__init__()
        self.backbone = Backbone()
        self.parent = Backbone()   # frozen: supplies FT% and assisted share only
        for p in self.parent.parameters():
            p.requires_grad_(False)
        self.rebound = Rebound()
        self.adjusted = AdjustedHeads()
        self.defense = BroadcastDefense()
        self.coverage = None       # optional Coverage; None in the reference
        self.creation = None       # optional Creation; None in the reference
        self.pairs = None          # optional PairInteractions; None in the reference
        self.defense_off = False   # offense-only training (phase A of the two-phase fit)

    @classmethod
    def from_parent(cls, parent_state, seed, defense="broadcast"):
        """Start from a fitted offense (v14 RB_RENEW_FAC state dict) with zero new heads.

        New heads are seeded exactly as the pre-refactor Model16 did (adjusted
        heads seed+1600, defense seed+1500), so both start at the parent's
        function and follow the same training trajectory. ``defense="capacity"``
        swaps in CapacityDefense (same seed); the adjusted defense head is then unused.
        """
        model = cls()
        state = {}
        for name, value in parent_state.items():
            if name in ("offset", "backbone.penalty_weight"):
                continue
            if name.startswith("backbone."):
                state["offense." + name] = value
                state["frozen." + name[len("backbone."):]] = value
            elif name.startswith("rebound_head."):
                state["offense." + name] = value
            else:
                raise KeyError(f"unexpected parent parameter {name}")
        with torch.random.fork_rng():
            torch.manual_seed(seed + 1600)
            model.adjusted = AdjustedHeads()
        with torch.random.fork_rng():
            torch.manual_seed(seed + 1500)
            model.defense = dict(broadcast=BroadcastDefense, capacity=CapacityDefense)[defense]()
        if defense == "capacity":
            model.adjusted.defense.requires_grad_(False)
        missing, unexpected = model.load_state_dict(from_legacy_state(state), strict=False)
        if unexpected or any(not k.startswith(("adjusted.", "defense.")) for k in missing):
            raise KeyError(f"parent load mismatch: missing={missing} unexpected={unexpected}")
        return model

    @classmethod
    def fresh(cls, seed):
        """Single-stage start: every learned correction is zero, the decoder is identity.

        The model then predicts each player's own dated rates under the shared
        budget. The frozen copy supplies own FT% and assisted share.
        """
        with torch.random.fork_rng():
            torch.manual_seed(seed)
            model = cls()
            for layer in (model.backbone.context_out, model.backbone.context_sd):
                nn.init.zeros_(layer.weight)
                if layer.bias is not None:
                    nn.init.zeros_(layer.bias)
            model.parent.load_state_dict(model.backbone.state_dict())
        return model

    @classmethod
    def offense_only(cls, seed):
        """Phase A of the two-phase fit: the single-stage start with every defense and adjusted head off.

        Trains the backbone and the rebound heads only, the role the separately
        trained v14 offense played for the reference.
        """
        model = cls.fresh(seed)
        model.defense_off = True
        for head in (model.adjusted, model.defense):
            head.requires_grad_(False)
        return model

    @classmethod
    def from_offense(cls, offense, seed, defense="broadcast"):
        """Phase B: start from a phase-A model exactly as from_parent starts from a v14 parent.

        The fitted backbone is both the trainable offense and the frozen parent
        (FT% and assisted share); adjusted and defense heads are new, zero-output
        and seeded as in from_parent.
        """
        model = cls()
        model.backbone.load_state_dict(offense.backbone.state_dict())
        model.parent.load_state_dict(offense.backbone.state_dict())
        model.rebound.load_state_dict(offense.rebound.state_dict())
        with torch.random.fork_rng():
            torch.manual_seed(seed + 1600)
            model.adjusted = AdjustedHeads()
        with torch.random.fork_rng():
            torch.manual_seed(seed + 1500)
            model.defense = dict(broadcast=BroadcastDefense, capacity=CapacityDefense)[defense]()
        if defense == "capacity":
            model.adjusted.defense.requires_grad_(False)
        return model

    def parameter_groups(self, lr, weight_decay, pair_lr_scale=1., pair_decay=0.):
        """Optimizer groups: everything as configured; PairInteractions with its own rate and decay."""
        if self.pairs is None:
            return [dict(params=list(self.parameters()), lr=lr, weight_decay=weight_decay)]
        mine = {id(p) for p in self.pairs.parameters()}
        return [dict(params=[p for p in self.parameters() if id(p) not in mine], lr=lr, weight_decay=weight_decay),
                dict(params=list(self.pairs.parameters()), lr=lr * pair_lr_scale, weight_decay=pair_decay)]

    def project(self):
        """Keep constraint coefficients in [0, 4] (and coverage kappa in [0, 1]) after each optimizer step."""
        with torch.no_grad():
            for p in (self.backbone.k_supply, self.backbone.k_ft, self.backbone.k_load):
                p.clamp_(0, 4)
            if self.coverage is not None and self.coverage.has_help:
                self.coverage.raw_kappa.clamp_(0, 1)

    def forward(self, batch, environment):
        base, x, role = batch["base"], batch["msg"], batch["role"]
        decoded = self.backbone.decode(self.backbone.state(base, x, role))
        with torch.no_grad():
            parent = self.parent.decode(self.parent.state(base, x, role))
        ft_make = torch.sigmoid(parent[..., FT_MAKE])
        assisted = torch.sigmoid(parent[..., ASSISTED])

        adjustment, rebound_adjustment = self.adjusted.offense(batch["adjusted_offense"])
        if self.creation is not None:
            adjustment = adjustment + self.creation(batch)
        if self.defense_off:
            effect, recovery = base.new_zeros(*base.shape[:2], 15), base.new_zeros(len(base))
        elif isinstance(self.defense, CapacityDefense):
            effect, recovery = self.defense(batch)
        else:
            effect, recovery = self.defense(batch["defense"])
            adjusted_defense = self.adjusted.defense_effect(batch["adjusted_defense"])
            effect = effect + adjusted_defense[:, None, :15]
            recovery = recovery + adjusted_defense[:, 15]
        if self.coverage is not None:
            effect = effect + self.coverage(batch)
        if self.pairs is not None:
            pair_offense, pair_defense = self.pairs(batch)
            adjustment = adjustment + pair_offense
            if not self.defense_off:
                effect = effect + pair_defense
        score = (self.rebound(batch["rb_input"], batch["rb_prior"], batch["league_capture"])
                 + rebound_adjustment.double() - recovery[:, None].double())

        budget = base.new_tensor(environment["budget"]).expand(len(base))
        phase = self.ledger(decoded[..., :15] + adjustment, base, assisted, ft_make, effect, score,
                            budget, float(environment["eta"]))
        return mix_renewal(phase, environment["non_rebound"], effect=effect, recovery=recovery)

    def ledger(self, logits, base, assisted, ft_make, effect, score, budget, eta):
        """One possession cycle: actions, locations and makes under the shared budget."""
        k = self.backbone
        q = logits[..., :3].clamp(-12, 4).exp()
        own_q = base[..., :3].clamp(-12, 4).exp()
        expected_load = own_q[..., 0] + .44 * own_q[..., 1] + own_q[..., 2]
        q = q * (budget / (q[..., 0] + .44 * q[..., 1] + q[..., 2]).sum(1).clamp(min=1e-8))[:, None, None]
        location = torch.softmax(logits[..., 3:9], -1)

        # Creation constraint: assisted-finishing demand against passing supply.
        demand = (q[..., 0, None] * location * torch.sigmoid(logits[..., 9:15])).sum(-1) * assisted
        supply = base[..., SUPPLY].clamp(-12, 4).exp()
        team_ratio = (demand.sum(1, keepdim=True).clamp(min=1e-8) / supply.sum(1, keepdim=True).clamp(min=1e-8)).log()
        own_ratio = (demand.clamp(min=1e-8) / (supply.sum(1, keepdim=True) - supply).clamp(min=1e-8)).log()
        shortage = torch.maximum(team_ratio, own_ratio).clamp(0, 4)
        load = ((q[..., 0] + .44 * q[..., 1] + q[..., 2]) / expected_load.clamp(min=1e-8)).log().clamp(0, 4)
        conversion = logits[..., 9:15] - k.k_supply.clamp(0, 4) * shortage[..., None] * assisted[..., None]
        fta = q[..., 1] * torch.exp(-k.k_ft.clamp(0, 4) * shortage)
        q = torch.stack([q[..., 0], fta, q[..., 2] + .44 * (q[..., 1] - fta)], -1)
        conversion = conversion - k.k_load.clamp(0, 4) * load[..., None]
        make = torch.sigmoid(conversion)

        # Defense shifts actions, location and conversion; the budget is re-imposed.
        q = q * effect[..., :3].exp()
        q = q * (budget / (q[..., 0] + .44 * q[..., 1] + q[..., 2]).sum(1).clamp(min=1e-8))[:, None, None]
        location = torch.softmax(location.clamp(min=1e-12).log() + effect[..., 3:9], -1)
        make = torch.sigmoid(torch.logit(make.clamp(1e-6, 1 - 1e-6)) + effect[..., 9:15])
        rebound_log_prob = torch.log_softmax(torch.cat([score, torch.zeros_like(score[:, :1])], 1), 1)

        q = q / budget[:, None, None]
        attempts = q[..., 0, None] * location
        makes = attempts * make
        miss = eta * (attempts * (1 - make)).sum((1, 2))
        return SimpleNamespace(q=q, fga=q[..., 0], fta=q[..., 1], turnover=q[..., 2], location=location,
                               make=make, expected_attempts=attempts, expected_makes=makes, ft_make=ft_make,
                               rebound_log_prob=rebound_log_prob, score=score, miss=miss, assisted=assisted,
                               supply=supply, demand=demand, shortage=shortage, load=load)


def mix_renewal(phase, non_rebound, **diagnostics):
    """Initial possessions plus renewed ones after offensive rebounds (same process)."""
    repeat, _, renewal_continuation = renewal(1., phase.miss, phase.score)
    continuation = phase.miss.double() * phase.rebound_log_prob[:, :5].exp().sum(1)
    initial = torch.as_tensor(non_rebound, dtype=torch.float64, device=continuation.device).expand_as(continuation)
    renewed = initial * continuation * repeat
    if (continuation < 0).any() or (continuation >= 1).any() or not torch.isfinite(renewed).all() or (initial <= 0).any():
        raise FloatingPointError("invalid initial phase or nonterminating renewal")
    total = initial + renewed

    def scaled(value):
        value = value.double()
        return total.reshape(-1, *([1] * (value.ndim - 1))) * value

    q = scaled(phase.q)
    attempts = scaled(phase.expected_attempts)
    makes = scaled(phase.expected_makes)
    fga, fta, turnover = (q[..., k] for k in range(3))
    live = total * phase.miss.double()
    collector = phase.rebound_log_prob.exp()
    player = (makes * makes.new_tensor(SHOT_VALUES)).sum(-1) + fta * phase.ft_make
    return SimpleNamespace(
        fga=fga, fta=fta, turnover=turnover, location=attempts / fga[..., None].clamp(min=1e-30),
        make=makes / attempts.clamp(min=1e-30), ft_make=phase.ft_make, assisted=phase.assisted,
        expected_attempts=attempts, expected_makes=makes, player_points=player,
        points100=100 * player.sum(1), usage_budget=total, orb=renewed,
        player_orb=live[:, None] * collector[:, :5], live=live,
        rebound_log_prob=collector.clamp(min=1e-300).log(), continuation=continuation,
        renewal_continuation=renewal_continuation, phase=phase, initial_usage=initial,
        renewed_usage=renewed, **diagnostics)


def average_ledgers(predictions):
    """Mixture of checkpoint forecasts: average expected events, then derive rates.

    Probabilities are never averaged directly; FT% and recovery shares are
    re-derived from averaged numerators and denominators.
    """
    if not predictions:
        raise ValueError("no checkpoints to average")

    def mean(name):
        return torch.stack([getattr(p, name).double() for p in predictions]).mean(0)

    fga, fta, turnover = (mean(k) for k in ("fga", "fta", "turnover"))
    attempts, makes = mean("expected_attempts"), mean("expected_makes")
    ft_made = torch.stack([p.fta.double() * p.ft_make.double() for p in predictions]).mean(0)
    ft_make = torch.where(fta > 0, ft_made / fta.clamp(min=1e-30), mean("ft_make"))
    live = mean("live")
    recovered = torch.stack([p.live[:, None] * p.rebound_log_prob.exp() for p in predictions]).mean(0)
    fallback = torch.stack([p.rebound_log_prob.exp() for p in predictions]).mean(0)
    collector = torch.where(live[:, None] > 0, recovered / live[:, None].clamp(min=1e-30), fallback)
    player = (makes * makes.new_tensor(SHOT_VALUES)).sum(-1) + ft_made
    return SimpleNamespace(
        fga=fga, fta=fta, turnover=turnover, ft_make=ft_make, expected_attempts=attempts,
        expected_makes=makes, player_points=player, points100=100 * player.sum(1),
        location=attempts / fga[..., None].clamp(min=1e-30), make=makes / attempts.clamp(min=1e-30),
        usage_budget=mean("usage_budget"), orb=mean("orb"), player_orb=mean("player_orb"), live=live,
        initial_usage=mean("initial_usage"), renewed_usage=mean("renewed_usage"),
        rebound_log_prob=collector.clamp(min=1e-300).log())


LEGACY_NAMES = {
    "offense.backbone.message.0.": "backbone.context.",
    "offense.backbone.sender_extra.": "backbone.context_sd.",
    "offense.backbone.message.2.": "backbone.context_out.",
    "offense.backbone.extra_head.": "backbone.role.",
    "offense.backbone.": "backbone.",
    "frozen.message.0.": "parent.context.",
    "frozen.sender_extra.": "parent.context_sd.",
    "frozen.message.2.": "parent.context_out.",
    "frozen.extra_head.": "parent.role.",
    "frozen.": "parent.",
    "offense.rebound_head.own.": "rebound.own.",
    "offense.rebound_head.donor.": "rebound.donor.",
    "adjusted_own.": "adjusted.own.",
    "adjusted_teammate.": "adjusted.teammate.",
    "adjusted_donor.": "adjusted.donor.",
    "adjusted_defense.": "adjusted.defense.",
    "defense.main.": "defense.main.",
    "defense.recovery.": "defense.recovery.",
}
# The readout offset and the training-time penalty weights do not enter the forward pass.
LEGACY_UNUSED = ("offense.offset", "offense.backbone.penalty_weight", "frozen.penalty_weight")


def from_legacy_state(state_dict):
    """Map a pre-refactor J_POINT_BOTH (Model16) state dict onto EventModel names."""
    out = {}
    for name, value in state_dict.items():
        if name in LEGACY_UNUSED:
            continue
        for old, new in LEGACY_NAMES.items():
            if name.startswith(old):
                out[new + name[len(old):]] = value
                break
        else:
            raise KeyError(f"unmapped legacy parameter {name}")
    return out


def load_legacy(state_dict):
    model = EventModel()
    model.load_state_dict(from_legacy_state(state_dict), strict=True)
    return model.eval()
