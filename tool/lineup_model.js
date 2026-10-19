/* The release lineup model in the browser: a transcription of lineups/model.py (EventModel forward pass),
 * lineups/players.py (inputs, era-relative rule), lineups/release.py (calibration, average-opponent panel),
 * lineups/support.py + lineups/band.py (band and reasons), lineups/explain.py (explanations) and
 * lineups/combinations.py (the measured combination effects) and lineups/learned.py (the learned
 * combination module, lineups.model.PairInteractions).
 *
 * Data: the export of scripts/export_release.py (meta.json, weights.bin, players.bin).
 * Parity with Python: tests/test_tool_parity.py.
 *
 * Works in a browser (window.LineupModel) and in node (module.exports).
 */
(function (root) {
  "use strict";

  // ---- small numeric helpers ---------------------------------------------------
  const tanh = Math.tanh;
  const sigmoid = (x) => 1 / (1 + Math.exp(-x));
  const softplus = (x) => (x > 20 ? x : Math.log1p(Math.exp(x)));
  const clamp = (x, lo, hi) => Math.min(Math.max(x, lo), hi);
  const logaddexp0 = (x) => (x > 0 ? x + Math.log1p(Math.exp(-x)) : Math.log1p(Math.exp(x)));   // log(1 + e^x)
  const logit = (p) => Math.log(p) - Math.log1p(-p);
  const sum = (a) => { let s = 0; for (const v of a) s += v; return s; };

  function layer(params, name, buffer) {
    const [offset, shape] = params[name + ".weight"];
    const out = shape[0], inp = shape[1];
    const W = Float64Array.from(buffer.subarray(offset, offset + out * inp));
    let b = null;
    if (params[name + ".bias"]) {
      const [bo, bs] = params[name + ".bias"];
      b = Float64Array.from(buffer.subarray(bo, bo + bs[0]));
    }
    return { W, b, out, inp };
  }
  function vector(params, name, buffer) {
    const [offset, shape] = params[name];
    const n = shape.length ? shape.reduce((a, c) => a * c, 1) : 1;
    return Float64Array.from(buffer.subarray(offset, offset + n));
  }
  function linear(L, x, add) {               // W x + b (+ add)
    const y = new Float64Array(L.out);
    for (let o = 0; o < L.out; o++) {
      let s = L.b ? L.b[o] : 0;
      const row = o * L.inp;
      for (let i = 0; i < L.inp; i++) s += L.W[row + i] * x[i];
      y[o] = add ? s + add[o] : s;
    }
    return y;
  }
  function mlp(net) { return { first: net.first, second: net.second, zero: Float64Array.from(net.first.b, tanh) }; }
  function mlpPlain(net, x) { return linear(net.second, Float64Array.from(linear(net.first, x), tanh)); }
  // centered(net, v) = W2 (tanh(W1 v + b1) - tanh(b1)); the second bias cancels.
  function centeredFromPre(net, pre) {
    const h = new Float64Array(pre.length);
    for (let k = 0; k < pre.length; k++) h[k] = tanh(pre[k]) - net.zero[k];
    const L = net.second, y = new Float64Array(L.out);
    for (let o = 0; o < L.out; o++) { let s = 0; const row = o * L.inp; for (let k = 0; k < L.inp; k++) s += L.W[row + k] * h[k]; y[o] = s; }
    return y;
  }
  function centered(net, x) { return centeredFromPre(net, linear(net.first, x)); }

  // ---- the network -----------------------------------------------------------------
  // A layer's weight matrix split by input block (columns), without the bias.
  function split(L, parts) {
    let at = 0; const out = [];
    for (const width of parts) {
      const W = new Float64Array(L.out * width);
      for (let o = 0; o < L.out; o++) for (let i = 0; i < width; i++) W[o * width + i] = L.W[o * L.inp + at + i];
      out.push({ W, b: null, out: L.out, inp: width }); at += width;
    }
    return out;
  }
  function loadNetwork(spec, buffer) {
    const p = spec.params;
    const two = (name) => mlp({ first: layer(p, name + ".0", buffer), second: layer(p, name + ".2", buffer) });
    const backbone = (prefix) => {
      const bb = {
        context: layer(p, prefix + ".context", buffer), contextSd: layer(p, prefix + ".context_sd", buffer),
        contextOut: layer(p, prefix + ".context_out", buffer), role: two(prefix + ".role"),
        intercept: vector(p, prefix + ".intercept", buffer),
        slope: Float64Array.from(vector(p, prefix + ".raw_slope", buffer), softplus),
        kSupply: vector(p, prefix + ".k_supply", buffer)[0], kFt: vector(p, prefix + ".k_ft", buffer)[0],
        kLoad: vector(p, prefix + ".k_load", buffer),
      };
      bb.contextParts = split(bb.context, [18, 18]);        // own message | teammates' mean message
      return bb;
    };
    const net = {
      arm: spec.arm, seed: spec.seed, checkpoint: spec.checkpoint, capacity: spec.arm === "C",
      backbone: backbone("backbone"), parent: backbone("parent"),
      reboundOwn: two("rebound.own"), reboundDonor: two("rebound.donor"),
      adjOwn: two("adjusted.own"), adjTeammate: two("adjusted.teammate"), adjDonor: two("adjusted.donor"),
      adjDefense: two("adjusted.defense"),
    };
    net.teammateParts = split(net.adjTeammate.first, [97, 97]);   // teammates' mean | their spread
    if (net.capacity) {
      net.pressure = two("defense.pressure"); net.inside = two("defense.inside"); net.perimeter = two("defense.perimeter");
      // First layers split by input block: attacker (20) | assigned defender (70) | inside pool (140).
      net.pressureParts = split(net.pressure.first, [20, 70, 140]);
      net.perimeterParts = split(net.perimeter.first, [20, 70]);
    } else {
      net.main = two("defense.main"); net.recovery = two("defense.recovery");
    }
    return net;
  }

  // What one player contributes to a network on his own, whoever his teammates are: computed once per
  // player-season and network. The teammates' means enter the first layers linearly, so each player's
  // share of them is a projection of his own inputs.
  function alone(net, p) {
    const own = (bb) => {
      const xr = new Float64Array(26); xr.set(p.msg); xr.set(p.role, 18);
      return { x: linear(bb.contextParts[0], p.msg), mean: linear(bb.contextParts[1], p.msg), role: mlpPlain(bb.role, xr) };
    };
    const out = {
      backbone: own(net.backbone), parent: own(net.parent),
      own: Float64Array.from(centered(net.adjOwn, p.adjOff), tanh), mean: linear(net.teammateParts[0], p.adjOff),
      donor: tanh(centered(net.adjDonor, p.adjOff)[0]), rbDonor: 2 * tanh(centered(net.reboundDonor, p.rbInput)[0]),
      rbOwn: 2 * tanh(mlpPlain(net.reboundOwn, p.rbInput)[0]),
    };
    if (net.capacity) {
      const att = new Float64Array(20); att.set(p.msg); att[18] = p.height; att[19] = p.position;
      out.pressure = linear(net.pressureParts[0], att); out.perimeter = linear(net.perimeterParts[0], att);
    }
    return out;
  }

  function contextState(bb, which, A, base, msg) {    // Backbone.state then decode, for five players (A: alone)
    const out = [];
    const S = new Float64Array(18), SS = new Float64Array(18), M = new Float64Array(32);
    for (const x of msg) for (let k = 0; k < 18; k++) { S[k] += x[k]; SS[k] += x[k] * x[k]; }
    for (const a of A) for (let k = 0; k < 32; k++) M[k] += a[which].mean[k];
    const b = bb.context.b, sd = new Float64Array(18), hidden = new Float64Array(32);
    for (let i = 0; i < 5; i++) {
      const x = msg[i], a = A[i][which];
      for (let k = 0; k < 18; k++) {
        const mean = (S[k] - x[k]) / 4, v = (SS[k] - x[k] * x[k]) / 4 - mean * mean;
        sd[k] = Math.sqrt(Math.max(v, 1e-8));
      }
      const spread = linear(bb.contextSd, sd);
      for (let k = 0; k < 32; k++) hidden[k] = tanh(b[k] + a.x[k] + (M[k] - a.mean[k]) / 4 + spread[k]);
      const message = linear(bb.contextOut, hidden, a.role);
      message[15] = 0;
      const decoded = new Float64Array(18);
      for (let k = 0; k < 18; k++) decoded[k] = bb.intercept[k] + bb.slope[k] * (base[i][k] + message[k]);
      out.push(decoded);
    }
    return out;
  }

  function moments(rows, width, leaveOneOut) {     // lineups.model.moments (rows: 5 vectors)
    const S = new Float64Array(width), SS = new Float64Array(width);
    for (const x of rows) for (let k = 0; k < width; k++) { S[k] += x[k]; SS[k] += x[k] * x[k]; }
    const one = (i) => {
      const out = new Float64Array(2 * width);
      for (let k = 0; k < width; k++) {
        let mean, v;
        if (leaveOneOut) { mean = (S[k] - rows[i][k]) / 4; v = (SS[k] - rows[i][k] * rows[i][k]) / 4 - mean * mean; }
        else { mean = S[k] / 5; v = 0; for (const x of rows) v += (x[k] - mean) * (x[k] - mean); v /= 5; }
        out[k] = mean; out[width + k] = v > 0 ? Math.sqrt(Math.max(v, 1e-8)) : 0;
      }
      return out;
    };
    return leaveOneOut ? [0, 1, 2, 3, 4].map(one) : one(0);
  }

  // Everything that depends on the offense five only (A: each player's terms alone, from alone()).
  function offenseSide(net, X, A) {
    const decoded = contextState(net.backbone, "backbone", A, X.base, X.msg);
    const parent = contextState(net.parent, "parent", A, X.base, X.msg);
    // the teammates' adjusted offense, leave-one-out: mean (through each player's projection) and spread
    const S = new Float64Array(97), SS = new Float64Array(97), M = new Float64Array(32), sd = new Float64Array(97);
    for (const x of X.adjOff) for (let k = 0; k < 97; k++) { S[k] += x[k]; SS[k] += x[k] * x[k]; }
    for (const a of A) for (let k = 0; k < 32; k++) M[k] += a.mean[k];
    let donors = 0, rbDonors = 0;
    for (const a of A) { donors += a.donor; rbDonors += a.rbDonor; }
    const league = clamp(X.league, 1e-6, 1 - 1e-6), b = net.adjTeammate.first.b, pre = new Float64Array(32);
    const players = [];
    for (let i = 0; i < 5; i++) {
      const x = X.adjOff[i], a = A[i];
      for (let k = 0; k < 97; k++) {
        const mean = (S[k] - x[k]) / 4, v = (SS[k] - x[k] * x[k]) / 4 - mean * mean;
        sd[k] = v > 0 ? Math.sqrt(Math.max(v, 1e-8)) : 0;
      }
      const spread = linear(net.teammateParts[1], sd);
      for (let k = 0; k < 32; k++) pre[k] = b[k] + (M[k] - a.mean[k]) / 4 + spread[k];
      const mates = Float64Array.from(centeredFromPre(net.adjTeammate, pre), tanh);
      const logits = new Float64Array(15);
      for (let k = 0; k < 15; k++) logits[k] = decoded[i][k] + a.own[k] + mates[k];
      const reboundAdjustment = a.own[15] + (donors - a.donor) / 4;
      const facilitation = (rbDonors - a.rbDonor) / 4;
      const score = Math.log(clamp(X.rbPrior[i], 1e-6, 1 - 1e-6)) - Math.log1p(-league) + a.rbOwn + facilitation
        + reboundAdjustment;
      const p = { logits, score, ftMake: sigmoid(parent[i][15]), assisted: sigmoid(parent[i][17]) };
      if (net.capacity) { p.pressure = a.pressure; p.perimeter = a.perimeter; }
      players.push(p);
    }
    return { players, base: X.base, key: X.listingKey, pids: X.pids, ids: X.ids };
  }

  // Everything that depends on the defense five only.
  function defenseSide(net, X) {
    const out = { key: X.listingKey, pids: X.pids, ids: X.ids };
    if (!net.capacity) {
      const z = new Float64Array(38);
      for (let k = 0; k < 19; k++) {
        let m = 0; for (const d of X.defense) m += d[k]; m /= 5;
        let v = 0; for (const d of X.defense) v += (d[k] - m) * (d[k] - m); v /= 5;
        z[k] = m; z[19 + k] = Math.sqrt(Math.max(v, 1e-12));
      }
      const main = Float64Array.from(centered(net.main, z), tanh);
      let recovery = tanh(centered(net.recovery, z)[0]);
      const adj = Float64Array.from(centered(net.adjDefense, moments(X.adjDef, 49, false)), tanh);
      for (let k = 0; k < 15; k++) main[k] += adj[k];
      recovery += adj[15];
      out.effect = main; out.recovery = recovery;
      return out;
    }
    const x = [];
    for (let j = 0; j < 5; j++) {
      const v = new Float64Array(70); v.set(X.defense[j]); v.set(X.adjDef[j], 19); v[68] = X.height[j]; v[69] = X.position[j];
      x.push(v);
    }
    const presence = X.defense.map((d, j) => d[1] + d[2] + X.tiebreak[j]);
    const order = [0, 1, 2, 3, 4].sort((a, b) => (presence[b] - presence[a]) || (a - b));   // stable, descending
    const pool = new Float64Array(140); pool.set(x[order[0]]); pool.set(x[order[1]], 70);
    out.poolId = X.ids[order[0]] * 32768 + X.ids[order[1]];
    out.inside = Float64Array.from(centered(net.inside, pool), tanh);
    out.poolPressure = linear(net.pressureParts[2], pool, net.pressure.first.b);
    out.defenderPressure = x.map((v) => linear(net.pressureParts[1], v));
    out.defenderPerimeter = x.map((v) => linear(net.perimeterParts[1], v, net.perimeter.first.b));
    return out;
  }

  // Each attacker's assigned defender: both fives sorted by (position, height, pid), paired in order.
  const order = (key) => [0, 1, 2, 3, 4].sort((a, b) => (key[a] - key[b]) || (a - b));
  const MATCH = new Int32Array(5);
  function matched(off, def) {
    const ro = off.order || (off.order = order(off.key)), rd = def.order || (def.order = order(def.key));
    for (let k = 0; k < 5; k++) MATCH[ro[k]] = rd[k];
    return MATCH;
  }

  // Arm C: each attacker's 15 defensive effects (pressure from his assigned defender and the inside pool,
  // perimeter from his assigned defender, inside from the pool) written into E (5 x 15); returns the recovery.
  const CAP = { pre: new Float64Array(32), per: new Float64Array(32), h: new Float64Array(32), out: new Float64Array(8) };
  const PRESSURE = [0, 1, 2], INSIDE = [3, 4, 9, 10], PERIMETER = [5, 6, 7, 8, 11, 12, 13, 14];
  function centeredTanh(net, pre, n) {        // tanh(centeredFromPre(net, pre)) into CAP.out[0..n)
    const h = CAP.h, z = net.zero, L = net.second, out = CAP.out;
    for (let k = 0; k < pre.length; k++) h[k] = tanh(pre[k]) - z[k];
    for (let o = 0; o < n; o++) { let s = 0; const row = o * L.inp; for (let k = 0; k < L.inp; k++) s += L.W[row + k] * h[k]; out[o] = tanh(s); }
    return out;
  }
  // memo (optional): attacker x assigned defender x inside pool -> the 11 pressure and perimeter effects; a
  // search's ranges share them, since its lineups share four players.
  function capacityEffects(net, off, def, E, memo) {
    const m = matched(off, def), pre = CAP.pre, per = CAP.per, pool = def.poolPressure;
    let byPool = null;
    if (memo) { byPool = memo.get(def.poolId); if (!byPool) memo.set(def.poolId, (byPool = new Map())); }
    for (let i = 0; i < 5; i++) {
      const e = 15 * i;
      for (let k = 0; k < 4; k++) E[e + INSIDE[k]] = def.inside[k];
      const key = byPool ? off.ids[i] * 32768 + def.ids[m[i]] : 0, hit = byPool ? byPool.get(key) : undefined;
      if (hit) {
        for (let k = 0; k < 3; k++) E[e + PRESSURE[k]] = hit[k];
        for (let k = 0; k < 8; k++) E[e + PERIMETER[k]] = hit[3 + k];
        continue;
      }
      const a = off.players[i], dp = def.defenderPressure[m[i]], dq = def.defenderPerimeter[m[i]];
      for (let k = 0; k < 32; k++) { pre[k] = a.pressure[k] + dp[k] + pool[k]; per[k] = a.perimeter[k] + dq[k]; }
      let x = centeredTanh(net.pressure, pre, 3);
      for (let k = 0; k < 3; k++) E[e + PRESSURE[k]] = x[k];
      x = centeredTanh(net.perimeter, per, 8);
      for (let k = 0; k < 8; k++) E[e + PERIMETER[k]] = x[k];
      if (byPool) {
        const v = new Float64Array(11);
        for (let k = 0; k < 3; k++) v[k] = E[e + PRESSURE[k]];
        for (let k = 0; k < 8; k++) v[3 + k] = E[e + PERIMETER[k]];
        byPool.set(key, v);
      }
    }
    return def.inside[4];
  }

  // ---- the learned combination module (lineups.model.PairInteractions, joint hold; lineups.learned) ------
  function loadModule(spec, buffer) {
    const p = spec.params, v = (name) => vector(p, name, buffer);
    const matrix = (name) => { const x = v(name); return [...Array(15).keys()].map((i) => x.subarray(15 * i, 15 * i + 15)); };
    const bounds = (name) => { const x = v(name); return [x.subarray(0, 15), x.subarray(15, 30)]; };
    return { seed: spec.seed, level: spec.level, rank: 4,
             offenseMap: layer(p, "offense_map", buffer), defenseMap: layer(p, "defense_map", buffer),
             u: layer(p, "u", buffer), v: layer(p, "v", buffer), p: layer(p, "p", buffer), q: layer(p, "q", buffer),
             player: bounds("player_bounds"), lineup: bounds("lineup_bounds"), defense: bounds("defense_bounds"),
             lineupMetric: matrix("lineup_metric"), lineupRadius: v("lineup_radius")[0],
             defenseMetric: matrix("defense_metric"), defenseRadius: v("defense_radius")[0], measured: v("measured")[0] > 0 };
  }
  function moduleFeatures(L, x) {              // tanh(W x + b) - tanh(b)
    const y = linear(L, x);
    for (let k = 0; k < y.length; k++) y[k] = tanh(y[k]) - tanh(L.b[k]);
    return y;
  }
  // sum_r a[c, r] * (sum_{j != i} b_j[c, r]) for each channel c (index c * rank + r).
  function pairSums(a, others, rank) {
    const out = new Float64Array(15);
    for (let c = 0; c < 15; c++) { let s = 0; for (let r = 0; r < rank; r++) s += a[c * rank + r] * others[c * rank + r]; out[c] = s; }
    return out;
  }
  const clampTo = (x, b) => Math.max(Math.min(x, b[1]), b[0]);
  function jointScale(t, metric, radius) {
    let d = 0;
    for (let j = 0; j < 15; j++) { let s = 0; for (let i = 0; i < 15; i++) s += t[i] * metric[i][j]; d += s * t[j]; }
    d = Math.sqrt(Math.max(d, 0));
    return d > radius ? radius / Math.max(d, 1e-12) : 1;
  }
  // One player's terms in a learned module (they depend on him alone): offense u, v and defense p, q.
  function moduleAlone(mod, p) {
    const s = new Float64Array(21); s.set(p.msg); s[18] = p.rbInput[26]; s[19] = p.rbInput[27]; s[20] = p.height;
    const x = new Float64Array(20); x.set(p.defense); x[19] = p.height;
    const g = moduleFeatures(mod.offenseMap, s), h = moduleFeatures(mod.defenseMap, x);
    return { u: linear(mod.u, g), v: linear(mod.v, g), p: linear(mod.p, h), q: linear(mod.q, h) };
  }
  // The module's 15 offensive corrections per attacker (held), from the offense five.
  function moduleOffense(mod, A) {                // A: the five's moduleAlone terms
    const u = A.map((a) => a.u), v = A.map((a) => a.v);
    const V = new Float64Array(60);
    for (const x of v) for (let k = 0; k < 60; k++) V[k] += x[k];
    let out = u.map((ui, i) => Float64Array.from(pairSums(ui, V.map((s, k) => s - v[i][k]), mod.rank), tanh));
    if (!mod.measured) return out;
    out = out.map((o) => o.map((x, c) => clampTo(x, [mod.player[0][c], mod.player[1][c]])));
    const total = new Float64Array(15);
    for (const o of out) for (let c = 0; c < 15; c++) total[c] += o[c];
    const scaled = new Float64Array(15);
    for (let c = 0; c < 15; c++) {
      const target = clampTo(total[c], [mod.lineup[0][c], mod.lineup[1][c]]);
      scaled[c] = target !== total[c] ? target / total[c] : 1;
    }
    out = out.map((o) => o.map((x, c) => x * scaled[c]));
    const held = new Float64Array(15);
    for (const o of out) for (let c = 0; c < 15; c++) held[c] += o[c];
    const k = jointScale(held, mod.lineupMetric, mod.lineupRadius);
    return out.map((o) => o.map((x) => x * k));
  }
  // The module's lineup-level defensive shift (15 channels, every attacker alike), from the defense five.
  function moduleDefense(mod, A) {
    const p = A.map((a) => a.p), q = A.map((a) => a.q);
    const Q = new Float64Array(60);
    for (const x of q) for (let k = 0; k < 60; k++) Q[k] += x[k];
    const total = new Float64Array(15);
    p.forEach((pl, l) => { const s = pairSums(pl, Q.map((t, k) => t - q[l][k]), mod.rank); for (let c = 0; c < 15; c++) total[c] += s[c]; });
    let out = total.map((t) => tanh(t / 2));
    if (!mod.measured) return out;
    out = out.map((x, c) => clampTo(x, [mod.defense[0][c], mod.defense[1][c]]));
    const k = jointScale(out, mod.defenseMetric, mod.defenseRadius);
    return out.map((x) => x * k);
  }


  const SHOT_VALUES = [2, 2, 2, 2, 3, 3];

  // EventModel.ledger + mix_renewal, split in two. prepare: everything that depends on the offense five
  // alone, once per five and network. settle: the rest, for each defense (its effects and recovery).
  // The defense enters as exp(effect) factors on rates, odds and location weights, so prepare keeps them in
  // that form. Per attacker (PREP floats): FGA, FTA, TOV shares before the defense; location shares; the odds
  // against each make (exp of minus the make logit); FT make rate; creation demand and supply. Then, for the
  // five, log H: the log of the summed rebound odds before the defense's recovery.
  const PREP = 18;
  function prepare(net, off, env) {
    const bb = net.backbone, budget = env.budget, P = off.players, out = new Float64Array(5 * PREP + 1);
    const q = new Float64Array(15), expected = new Float64Array(5), supply = new Float64Array(5);
    const loc = new Float64Array(30), demand = new Float64Array(5);
    let load = 0;
    for (let i = 0; i < 5; i++) {
      for (let k = 0; k < 3; k++) q[3 * i + k] = Math.exp(clamp(P[i].logits[k], -12, 4));
      load += q[3 * i] + .44 * q[3 * i + 1] + q[3 * i + 2];
      const b = off.base[i];
      expected[i] = Math.exp(clamp(b[0], -12, 4)) + .44 * Math.exp(clamp(b[1], -12, 4)) + Math.exp(clamp(b[2], -12, 4));
      supply[i] = Math.exp(clamp(b[16], -12, 4));
    }
    const scale = budget / Math.max(load, 1e-8);
    for (let j = 0; j < 15; j++) q[j] *= scale;
    let totalDemand = 0, totalSupply = 0;
    for (let i = 0; i < 5; i++) {
      const lg = P[i].logits, l = 6 * i;
      let m = -Infinity, s = 0, d = 0;
      for (let z = 0; z < 6; z++) m = Math.max(m, lg[3 + z]);
      for (let z = 0; z < 6; z++) { loc[l + z] = Math.exp(lg[3 + z] - m); s += loc[l + z]; }
      for (let z = 0; z < 6; z++) { loc[l + z] /= s; d += q[3 * i] * loc[l + z] * sigmoid(lg[9 + z]); }
      demand[i] = d * P[i].assisted;
      totalDemand += demand[i]; totalSupply += supply[i];
    }
    const teamRatio = Math.log(Math.max(totalDemand, 1e-8) / Math.max(totalSupply, 1e-8));
    const kFt = clamp(bb.kFt, 0, 4), kSupply = clamp(bb.kSupply, 0, 4);
    let maxScore = -Infinity, h = 0;
    for (let i = 0; i < 5; i++) {
      const o = i * PREP, j = 3 * i, lg = P[i].logits;
      const ownRatio = Math.log(Math.max(demand[i], 1e-8) / Math.max(totalSupply - supply[i], 1e-8));
      const shortage = clamp(Math.max(teamRatio, ownRatio), 0, 4);
      const ld = clamp(Math.log((q[j] + .44 * q[j + 1] + q[j + 2]) / Math.max(expected[i], 1e-8)), 0, 4);
      const fta = q[j + 1] * Math.exp(-kFt * shortage);
      out[o] = q[j]; out[o + 1] = fta; out[o + 2] = q[j + 2] + .44 * (q[j + 1] - fta);
      for (let z = 0; z < 6; z++) {
        out[o + 3 + z] = Math.max(loc[6 * i + z], 1e-12);
        const conv = lg[9 + z] - kSupply * shortage * P[i].assisted - clamp(bb.kLoad[z], 0, 4) * ld;
        const p = clamp(sigmoid(conv), 1e-6, 1 - 1e-6);
        out[o + 9 + z] = (1 - p) / p;
      }
      out[o + 15] = P[i].ftMake; out[o + 16] = demand[i]; out[o + 17] = supply[i];
      maxScore = Math.max(maxScore, P[i].score);
    }
    for (let i = 0; i < 5; i++) h += Math.exp(P[i].score - maxScore);
    out[5 * PREP] = maxScore + Math.log(h);
    return out;
  }

  // Points per 100 for a prepared offense against defensive effects E and recovery. E: 15 effects shared by
  // the five attackers (a lineup-level defense) or 5 x 15. With S, also the ledger's sums (SUMMARY floats):
  // points100, FGA, FTA, TOV, FT made, offensive rebounds, demand, supply, attempts and makes by zone; then per
  // attacker FGA, FTA, TOV, points, three attempts, rim attempts.
  const SUMMARY = 50;
  const SET = { q: new Float64Array(15), loc: new Float64Array(30), fm: new Float64Array(30), x: new Float64Array(75) };
  function settle(prep, E, recovery, env, S) {
    const budget = env.budget, q = SET.q, loc = SET.loc, fm = SET.fm, x = SET.x, wide = E.length > 15;
    const n = wide ? 75 : 15;
    for (let k = 0; k < n; k++) { const c = k % 15; x[k] = Math.exp(c < 9 ? E[k] : -E[k]); }
    let load = 0;
    for (let i = 0; i < 5; i++) {
      const o = i * PREP, e = wide ? 15 * i : 0, j = 3 * i;
      q[j] = prep[o] * x[e]; q[j + 1] = prep[o + 1] * x[e + 1]; q[j + 2] = prep[o + 2] * x[e + 2];
      load += q[j] + .44 * q[j + 1] + q[j + 2];
    }
    const scale = budget / Math.max(load, 1e-8);
    for (let j = 0; j < 15; j++) q[j] = q[j] * scale / budget;
    let miss = 0;
    for (let i = 0; i < 5; i++) {
      const o = i * PREP, e = wide ? 15 * i : 0, l = 6 * i;
      let s = 0;
      for (let z = 0; z < 6; z++) { const v = prep[o + 3 + z] * x[e + 3 + z]; loc[l + z] = v; s += v; }
      for (let z = 0; z < 6; z++) {
        loc[l + z] /= s; fm[l + z] = 1 / (1 + prep[o + 9 + z] * x[e + 9 + z]);
        miss += q[3 * i] * loc[l + z] * (1 - fm[l + z]);
      }
    }
    miss *= env.eta;
    // renewal(1, miss, score): H = summed collector odds, the first collector's chance H / (1 + H);
    // repeat = exp(log(1 + H) - log(1 + (1 - m) H))
    const logH = prep[5 * PREP] - recovery, lse = logaddexp0(logH);
    const repeat = Math.exp(lse - logaddexp0(Math.log1p(-miss) + logH));
    const initial = env.non_rebound, renewed = initial * (miss * Math.exp(logH - lse)) * repeat, total = initial + renewed;
    if (S) S.fill(0, 0, 20);
    let points = 0;
    for (let i = 0; i < 5; i++) {
      const o = i * PREP, j = 3 * i, l = 6 * i, fta = total * q[j + 1];
      let p = 0;
      for (let z = 0; z < 6; z++) {
        const a = total * (q[j] * loc[l + z]), mk = a * fm[l + z];
        p += mk * SHOT_VALUES[z];
        if (S) { S[8 + z] += a; S[14 + z] += mk; }
      }
      p += fta * prep[o + 15];
      points += p;
      if (S) {
        const fga = total * q[j], tov = total * q[j + 2], u = 20 + 6 * i;
        S[1] += fga; S[2] += fta; S[3] += tov; S[4] += fta * prep[o + 15]; S[6] += prep[o + 16]; S[7] += prep[o + 17];
        S[u] = fga; S[u + 1] = fta; S[u + 2] = tov; S[u + 3] = p;
        S[u + 4] = total * (q[j] * loc[l + 4]) + total * (q[j] * loc[l + 5]); S[u + 5] = total * (q[j] * loc[l]);
      }
    }
    if (S) { S[0] = 100 * points; S[5] = renewed; }
    return 100 * points;
  }

  // ---- the release ---------------------------------------------------------------------
  function create(meta, weightsBuffer, playersBuffer) {
    const W = new Float32Array(weightsBuffer), M = new Float32Array(playersBuffer);
    const nets = meta.models.map((spec) => loadNetwork(spec, W));
    const LR = meta.learned, modules = LR ? LR.modules.map((spec) => loadModule(spec, W)) : [];
    const seeds = meta.seeds, N = meta.normalizer, layout = meta.players.layout, width = meta.players.width;
    const C = meta.constants;
    const pid = meta.players.pid, season = meta.players.season;
    const rowIndex = new Map();
    pid.forEach((p, r) => rowIndex.set(p * 10000 + season[r], r));
    const meanKeys = ["base_mean", "role_mean", "rebound_mean", "defense_mean", "offense_mean", "defense_bank_mean"];
    const block = (r, k) => M.subarray(r * width + layout[k][0], r * width + layout[k][0] + layout[k][1]);

    function raw(r, rule) {
      const x = { base: Array.from(block(r, "base")), role: Array.from(block(r, "role")), rbProb: block(r, "rb_prob")[0],
                  rbNeff: block(r, "rb_neff")[0], defense: Array.from(block(r, "defense")),
                  adjOff: Array.from(block(r, "adjusted_offense")), adjDef: Array.from(block(r, "adjusted_defense")) };
      if (rule === "relative") {
        const s = season[r] - meta.season_normalizer.first, own = {};
        meanKeys.forEach((k) => { own[k] = meta.season_normalizer.means[k][s]; });
        const shift = (k, i) => Math.fround(Math.fround(N[k][i]) - Math.fround(own[k][i]));
        x.base = x.base.map((v, i) => Math.fround(v + shift("base_mean", i)));
        x.role = x.role.map((v, i) => Math.fround(v + shift("role_mean", i)));
        const p = clamp(x.rbProb, 1e-6, 1 - 1e-6);
        x.rbProb = Math.fround(sigmoid(logit(p) + shift("rebound_mean", 0)));
        x.rbNeff = Math.fround(Math.expm1(Math.log1p(x.rbNeff) + shift("rebound_mean", 1)));
        x.defense = x.defense.map((v, i) => Math.fround(v + shift("defense_mean", i)));
        x.adjOff = x.adjOff.map((v, i) => Math.fround(v + shift("offense_mean", i)));
        x.adjDef = x.adjDef.map((v, i) => Math.fround(v + shift("defense_bank_mean", i)));
      }
      return x;
    }
    const playerCache = new Map();
    function player(r, rule) {
      const key = r + "|" + rule;
      if (playerCache.has(key)) return playerCache.get(key);
      const x = raw(r, rule);
      const msg = x.base.map((v, k) => (v - N.base_mean[k]) / Math.max(N.base_sd[k], 1e-6));
      const role = x.role.map((v, k) => (v - N.role_mean[k]) / N.role_scale[k]);
      const p = clamp(x.rbProb, 1e-6, 1 - 1e-6);
      const extra = [(logit(p) - N.rebound_mean[0]) / N.rebound_scale[0], (Math.log1p(x.rbNeff) - N.rebound_mean[1]) / N.rebound_scale[1]];
      const [h, pos] = meta.listings[String(pid[r])];
      const out = { key, pid: pid[r], base: x.base, msg, role, rbInput: [...msg, ...role, ...extra], rbPrior: x.rbProb,
        defense: x.defense.map((v, k) => (v - N.defense_mean[k]) / N.defense_scale[k]),
        adjOff: x.adjOff.map((v, k) => (v - N.offense_mean[k]) / N.offense_scale[k]),
        adjDef: x.adjDef.map((v, k) => (v - N.defense_bank_mean[k]) / N.defense_bank_scale[k]),
        height: (h - C.height_scale[0]) / C.height_scale[1], position: (pos - C.position_scale[0]) / C.position_scale[1],
        listingKey: pos * 1e4 + h * 10 + pid[r] * 1e-5, tiebreak: Math.fround(pid[r] * C.tiebreak), raw: x,
        id: 2 * r + (rule === "relative" ? 0 : 1) };
      playerCache.set(key, out);
      return out;
    }
    function five(rows, rule) {
      const ps = rows.map((r) => player(r, rule));
      return { base: ps.map((p) => p.base), msg: ps.map((p) => p.msg), role: ps.map((p) => p.role),
               rbInput: ps.map((p) => p.rbInput), rbPrior: ps.map((p) => p.rbPrior), defense: ps.map((p) => p.defense),
               adjOff: ps.map((p) => p.adjOff), adjDef: ps.map((p) => p.adjDef), height: ps.map((p) => p.height),
               position: ps.map((p) => p.position), listingKey: ps.map((p) => p.listingKey),
               tiebreak: ps.map((p) => p.tiebreak), pids: ps.map((p) => p.pid), ids: ps.map((p) => p.id),
               league: meta.league_capture, players: ps };
    }
    // ---- five states: what depends on one five, per network (and learned module), computed once ---------
    // Networks are addressed by index; idx[arm][seed] lists that seed's checkpoints. The panel's fives are kept
    // for the session; other fives in a small recent cache.
    const env = meta.env, NN = nets.length, idx = {};
    nets.forEach((n, k) => { ((idx[n.arm] = idx[n.arm] || {})[n.seed] = idx[n.arm][n.seed] || []).push(k); });
    const newFive = (rows, rule) => ({ X: five(rows, rule), off: [], def: [], prep: [], modOff: [], modDef: [],
                                       prepOn: [], Eon: [] });
    const RECENT = 512, recent = new Map();
    function fiveOf(rows, rule) {
      const key = rule + "|" + rows.join(",");
      let f = recent.get(key);
      if (f === undefined) {
        if (recent.size >= RECENT) recent.delete(recent.keys().next().value);
        recent.set(key, (f = newFive(rows, rule)));
      }
      return f;
    }
    const panels = {};
    const panelOf = (rule) => panels[rule] || (panels[rule] = {
      defense: meta.panel.defense.rows.map((r) => newFive(r, rule)), offense: meta.panel.offense.rows.map((r) => newFive(r, rule)) });
    // Each player's terms alone, per network and learned module, kept for the most recent players.
    const TERMS = 256, terms = new Map();
    function termsOf(p) {
      let t = terms.get(p.key);
      if (t) { terms.delete(p.key); terms.set(p.key, t); return t; }
      if (terms.size >= TERMS) terms.delete(terms.keys().next().value);
      terms.set(p.key, (t = { alone: [], module: [] }));
      return t;
    }
    const aloneOf = (p, n) => { const t = termsOf(p); return t.alone[n] || (t.alone[n] = alone(nets[n], p)); };
    const moduleTermsOf = (p, m) => { const t = termsOf(p); return t.module[m] || (t.module[m] = moduleAlone(modules[m], p)); };
    const offOf = (f, n) => f.off[n] || (f.off[n] = offenseSide(nets[n], f.X, f.X.players.map((p) => aloneOf(p, n))));
    const defOf = (f, n) => f.def[n] || (f.def[n] = defenseSide(nets[n], f.X));
    const prepOf = (f, n) => f.prep[n] || (f.prep[n] = prepare(nets[n], offOf(f, n), env));
    // A lineup-level defensive effect (the same for all five attackers), with the learned module's shift.
    const shifted = (effect, shift) => Float64Array.from(effect, (x, k) => x + shift[k]);
    const effectOf = (f, n) => defOf(f, n).effect;
    const EC = new Float64Array(75);
    let capMemo = null, memoToken = null;            // the capacity arm's memo for one search's ranges (memo())
    function memo(token) {
      if (token === undefined || token === null) { capMemo = null; memoToken = null; return; }
      if (token !== memoToken) { memoToken = token; capMemo = nets.map(() => new Map()); }
    }
    function pair(fo, fd, n, S) {                  // network n's points per 100 (and sums into S) for fo against fd
      const net = nets[n];
      if (!net.capacity) return settle(prepOf(fo, n), effectOf(fd, n), defOf(fd, n).recovery, env, S);
      const recovery = capacityEffects(net, offOf(fo, n), defOf(fd, n), EC, capMemo ? capMemo[n] : null);
      return settle(prepOf(fo, n), EC, recovery, env, S);
    }
    // The learned module m (arm R): its corrections to the offense's event logits and the defense's effect.
    const modTerms = (f, m) => f.X.players.map((p) => moduleTermsOf(p, m));
    const modOffOf = (f, m) => f.modOff[m] || (f.modOff[m] = moduleOffense(modules[m], modTerms(f, m)));
    const modDefOf = (f, m) => f.modDef[m] || (f.modDef[m] = moduleDefense(modules[m], modTerms(f, m)));
    function prepOnOf(f, n, m) {
      const k = m * NN + n;
      if (f.prepOn[k]) return f.prepOn[k];
      const o = offOf(f, n), add = modOffOf(f, m);
      const shifted = { ...o, players: o.players.map((p, i) => ({ ...p, logits: p.logits.map((x, c) => x + add[i][c]) })) };
      return (f.prepOn[k] = prepare(nets[n], shifted, env));
    }
    const effectOnOf = (f, n, m) => f.Eon[m * NN + n] || (f.Eon[m * NN + n] = shifted(defOf(f, n).effect, modDefOf(f, m)));

    // Per-seed native points (mean over that seed's checkpoints), then the calibrated seed mean.
    function seedNatives(arm, fo, fd, subset) {     // subset: {arm: {seed: [net indices]}}, all by default
      return seeds.map((s) => {
        const ks = (subset || idx)[arm][s];
        let p = 0;
        for (const n of ks) p += pair(fo, fd, n, null);
        return p / ks.length;
      });
    }
    const nativeBySeed = (arm, offRows, defRows, rule) => seedNatives(arm, fiveOf(offRows, rule), fiveOf(defRows, rule));
    function calibrate(arm, natives) {
      return sum(natives.map((p, i) => {
        const c = meta.calibration[arm + "_s" + seeds[i]];
        return meta.league + c.intercept + c.slope * (p - meta.league);
      })) / natives.length;
    }
    const points = (arm, offRows, defRows, rule) => calibrate(arm, nativeBySeed(arm, offRows, defRows, rule));
    function ratings(rows, rule, arm) {
      arm = arm || meta.forecast;
      const f = fiveOf(rows, rule), P = panelOf(rule), D = meta.panel.defense, O = meta.panel.offense;
      if (arm === meta.forecast) { const x = pass(f, rule); return { offense: x.offense, defense: x.defense, margin: x.margin }; }
      let offense = 0, defense = 0;
      P.defense.forEach((d, k) => { offense += D.weights[k] * calibrate(arm, seedNatives(arm, f, d)); });
      P.offense.forEach((o, k) => { defense += O.weights[k] * calibrate(arm, seedNatives(arm, o, f)); });
      return { offense, defense, margin: offense - defense };
    }
    function matchup(aRows, bRows, rule, arm) {
      arm = arm || meta.forecast;
      const a = points(arm, aRows, bRows, rule), b = points(arm, bRows, aRows, rule);
      return { a_offense: a, b_offense: b, margin: a - b };
    }

    // ---- learned combinations (lineups.release.Release.season_learned*) -----------------------
    const S1 = new Float64Array(SUMMARY), S2 = new Float64Array(SUMMARY);
    function addRates(acc, S, n) {                // lineups.learned.rates on the checkpoint mixture: sums / n
      for (let z = 0; z < 6; z++) acc[z] += S[8 + z] / n;
      acc[6] += S[3] / n; acc[7] += S[2] / n; acc[8] += S[0] / n;
    }
    function eventRates(acc) {
      let fga = 0; for (let z = 0; z < 6; z++) fga += acc[z];
      return { points: acc[8], rim_share: acc[0] / fga, three_share: (acc[4] + acc[5]) / fga, tov: acc[6], fta: acc[7] };
    }
    const EVENT_FIELDS = LR ? LR.fields.filter((k) => k !== "points") : [];
    const FIELDS = LR ? LR.fields : [], NF = FIELDS.length;
    const CODE = { points: 0, rim_share: 1, three_share: 2, tov: 3, fta: 4 }, codes = FIELDS.map((k) => CODE[k]);
    if (codes.some((c) => c === undefined)) throw new Error("unknown learned field in " + FIELDS.join(","));
    const levels = modules.map((mod) => FIELDS.map((k) => mod.level[k]));
    const slopes = modules.map((mod) => meta.calibration["R_s" + mod.seed].slope);
    function rateOf(acc, c) {                      // lineups.learned.rates: one field from the sums
      if (c === 0) return acc[8];
      if (c === 3) return acc[6];
      if (c === 4) return acc[7];
      let fga = 0; for (let z = 0; z < 6; z++) fga += acc[z];
      return c === 1 ? acc[0] / fga : (acc[4] + acc[5]) / fga;
    }
    const RATES = modules.map(() => [new Float64Array(9), new Float64Array(9)]);   // per module: off, on
    const clearRates = () => { for (const r of RATES) { r[0].fill(0); r[1].fill(0); } return RATES; };
    function learnedInto(rates, x) {               // calibrated points and native event changes, seed means (x: NF)
      x.fill(0);
      modules.forEach((mod, m) => {
        for (let j = 0; j < NF; j++) {
          const c = codes[j], change = LR.scale * (rateOf(rates[m][1], c) - rateOf(rates[m][0], c) - levels[m][j]);
          x[j] += (c === 0 ? slopes[m] * change : change) / modules.length;
        }
      });
      return x;
    }
    function moduleOn(fo, fd, n, m, rates, count) {   // module m switched on, for network n
      settle(prepOnOf(fo, n, m), effectOnOf(fd, n, m), defOf(fd, n).recovery, env, S2);
      addRates(rates[m][1], S2, count);
    }
    const X1 = new Float64Array(NF);
    function learnedOf(fo, fd) {
      const rates = clearRates();
      modules.forEach((mod, m) => {
        const ks = idx.R[mod.seed];
        for (const n of ks) { pair(fo, fd, n, S1); addRates(rates[m][0], S1, ks.length); moduleOn(fo, fd, n, m, rates, ks.length); }
      });
      return learnedInto(rates, X1);
    }
    function learnedPoints(offRows, defRows, rule) {
      const x = learnedOf(fiveOf(offRows, rule), fiveOf(defRows, rule));
      return Object.fromEntries(FIELDS.map((k, j) => [k, x[j]]));
    }

    // ---- one pass over the average-opponent panel for the forecast arm ---------------------------------
    // Calibrated points, the learned combinations and the explanation's mixture sums, sharing every ledger;
    // ratings, learned.lineup and explain.lineup read it. A view uses some of the checkpoints and panel
    // lineups (the missing-piece screen); without one, everything.
    const modsOf = {};
    modules.forEach((mod, m) => { (modsOf[mod.seed] = modsOf[mod.seed] || []).push(m); });
    const shared = meta.forecast === "R";          // the learned module sits on arm R
    function mixAdd(team, players, S, u) {
      team.points += u * S[0] / 100; team.fga += u * S[1]; team.fta += u * S[2]; team.tov += u * S[3];
      team.ftm += u * S[4]; team.orb += u * S[5]; team.demand += u * S[6]; team.supply += u * S[7];
      for (let z = 0; z < 6; z++) { team.attempts[z] += u * S[8 + z]; team.makes[z] += u * S[14 + z]; }
      if (players) for (let k = 0; k < 30; k++) players[k] += u * S[20 + k];
    }
    function pass(f, rule, view) {
      const key = view ? view.key : "all", F = meta.forecast;
      if (!f.pass) f.pass = {};
      if (f.pass[key]) return f.pass[key];
      const P = panelOf(rule), ix = view ? view.idx : idx, natives = new Float64Array(seeds.length);
      const out = { offense: 0, defense: 0, margin: 0, team: newTeam(), players: new Float64Array(30), learned: null };
      if (LR) {
        out.learned = { offense: 0, defense: 0, events: { offense: {}, defense: {} }, margin: 0 };
        EVENT_FIELDS.forEach((k) => { out.learned.events.offense[k] = 0; out.learned.events.defense[k] = 0; });
      }
      for (const side of ["defense", "offense"]) {      // the five attacks the panel's defenses, then defends
        const attacking = side === "defense", which = attacking ? "offense" : "defense";
        const panel = meta.panel[side], fives = P[side], use = view ? view[side] : null;
        const count = use ? use.at.length : fives.length;
        for (let j = 0; j < count; j++) {
          const k = use ? use.at[j] : j, w = use ? use.weights[j] : panel.weights[k];
          const fo = attacking ? f : fives[k], fd = attacking ? fives[k] : f, rates = LR && shared ? clearRates() : null;
          seeds.forEach((s, i) => {
            const ks = ix[F][s], u = w / (seeds.length * ks.length), mods = rates ? (modsOf[s] || []) : [];
            let p = 0;
            for (const n of ks) {
              p += pair(fo, fd, n, S1);
              if (attacking) mixAdd(out.team, out.players, S1, u);
              for (const m of mods) { addRates(rates[m][0], S1, ks.length); moduleOn(fo, fd, n, m, rates, ks.length); }
            }
            natives[i] = p / ks.length;
          });
          out[which] += w * calibrate(F, natives);
          if (LR) {
            const x = rates ? learnedInto(rates, X1) : learnedOf(fo, fd), L = out.learned, ev = L.events[which];
            for (let j = 0; j < NF; j++) { if (codes[j] === 0) L[which] += w * x[j]; else ev[FIELDS[j]] += w * x[j]; }
          }
        }
      }
      out.margin = out.offense - out.defense;
      if (LR) out.learned.margin = out.learned.offense - out.learned.defense;
      return (f.pass[key] = out);
    }
    // A view: the first `checkpoints` of every seed and `perSide` panel lineups a side (every k-th in weight
    // order, reweighted to sum to one).
    function view(key, perSide, checkpoints) {
      const pick = (panel) => {
        const order = panel.weights.map((_, i) => i).sort((a, b) => panel.weights[b] - panel.weights[a] || a - b);
        const n = Math.min(perSide, order.length), at = [...Array(n).keys()].map((j) => order[Math.floor(j * order.length / n)]);
        const total = sum(at.map((i) => panel.weights[i]));
        return { at, weights: at.map((i) => panel.weights[i] / total) };
      };
      const sub = {};
      for (const arm of Object.keys(idx)) {
        sub[arm] = {};
        for (const s of seeds) sub[arm][s] = idx[arm][s].filter((n) => nets[n].checkpoint < checkpoints);
      }
      return { key, idx: sub, defense: pick(meta.panel.defense), offense: pick(meta.panel.offense) };
    }
    function learnedRatings(rows, rule) {
      const L = pass(fiveOf(rows, rule), rule).learned;
      return { offense: L.offense, defense: L.defense, events: { offense: { ...L.events.offense }, defense: { ...L.events.defense } },
               margin: L.margin };
    }
    function learnedMatchup(aRows, bRows, rule) {
      const a = learnedPoints(aRows, bRows, rule), b = learnedPoints(bRows, aRows, rule);
      const pick = (x) => Object.fromEntries(EVENT_FIELDS.map((k) => [k, x[k]]));
      return { a_offense: a.points, b_offense: b.points, margin: a.points - b.points,
               events: { a_offense: pick(a), b_offense: pick(b) } };
    }

    // ---- support reasons (lineups.support with lineups.players.relative states) ---------
    const S = meta.support, latestMeans = meta.season_means[String(meta.latest_season)];
    function relativeStates(r) {
      const own = meta.season_means[String(season[r])];
      const b = block(r, "base"), d = block(r, "defense");
      return { base: Array.from(b, (v, k) => v + (latestMeans[0][k] - own[0][k])),
               defense: Array.from(d, (v, k) => v + (latestMeans[1][k] - own[1][k])) };
    }
    function composition(states, side) {
      const x = states.map((v) => side === "offense"
        ? v.map((u, k) => (u - N.base_mean[k]) / Math.max(N.base_sd[k], 1e-6))
        : v.map((u, k) => (u - N.defense_mean[k]) / N.defense_scale[k]));
      const F = x[0].length, z = new Array(2 * F);
      for (let k = 0; k < F; k++) {
        let m = 0; for (const v of x) m += v[k]; m /= 5;
        let s = 0; for (const v of x) s += (v[k] - m) * (v[k] - m);
        z[k] = m; z[F + k] = Math.sqrt(s / 5);
      }
      const ref = S[side], d = z.map((v, k) => v - ref.mean[k]);
      let q = 0;
      for (let i = 0; i < d.length; i++) { let t = 0; for (let j = 0; j < d.length; j++) t += ref.inverse[i][j] * d[j]; q += d[i] * t; }
      return Math.sqrt(q);
    }
    function roles(baseRows, pids) {
      let bestPasser = -Infinity, bestShooter = -Infinity, bigs = 0;
      baseRows.forEach((b, i) => {
        const loc = b.slice(3, 9), m = Math.max(...loc), e = loc.map((v) => Math.exp(v - m)), s = sum(e);
        const three = 100 * Math.exp(clamp(b[0], -12, 4)) * (e[4] + e[5]) / s;
        const assist = 100 * Math.exp(clamp(b[16], -12, 4));
        bestPasser = Math.max(bestPasser, assist); bestShooter = Math.max(bestShooter, three);
        if (meta.listings[String(pids[i])][0] >= S.big_inches && three < S.non_shooter) bigs += 1;
      });
      return { best_passer: bestPasser, best_shooter: bestShooter, nonspacing_bigs: bigs };
    }
    const fmt = (x, d) => x.toFixed(d);
    function compositionReasons(offRows, defRows) {
      const reasons = [];
      const offStates = offRows.map(relativeStates), defStates = defRows.map(relativeStates);
      for (const [side, states] of [["offense", offStates.map((s) => s.base)], ["defense", defStates.map((s) => s.defense)]]) {
        const d = composition(states, side), real = S[side].distance, max = real[real.length - 1];
        if (d > max) reasons.push(`${side} composition beyond every trained lineup (distance ${fmt(d, 1)}, max ${fmt(max, 1)})`);
      }
      const r = roles(offStates.map((s) => s.base), offRows.map((x) => pid[x]));
      if (r.best_passer < S.limits.best_passer) reasons.push(`no ball handler: best passer ${fmt(r.best_passer, 1)} assists/100, below every trained lineup (${fmt(S.limits.best_passer, 1)})`);
      if (r.best_shooter < S.limits.best_shooter) reasons.push(`no shooter: best 3PA rate ${fmt(r.best_shooter, 1)}/100, below every trained lineup`);
      if (r.nonspacing_bigs > S.limits.nonspacing_bigs) reasons.push(`${r.nonspacing_bigs} non-spacing bigs, more than any trained lineup (${S.limits.nonspacing_bigs})`);
      return reasons;
    }

    // ---- band (lineups.band) --------------------------------------------------------------
    const B = meta.band;
    const crossEraShare = (rows) => rows.filter((r) => season[r] < B.first_training_season).length / rows.length;
    function playerReasons(rows, label, rule) {
      const reasons = [];
      if (new Set(rows.map((r) => pid[r])).size < 5) reasons.push(`${label} repeats a player`);
      rows.forEach((r) => {
        if (meta.players.offense_possessions[r] < B.thin_possessions) {
          reasons.push(`thin player data: ${meta.names[String(pid[r])]} played ${Math.trunc(meta.players.offense_possessions[r])} offensive possessions in ${season[r]}`);
        }
      });
      const old = [...new Set(rows.map((r) => season[r]).filter((s) => s < B.first_training_season))].sort();
      if (old.length) {
        reasons.push(`cross-era: ${label} uses ${old.join(", ")} player-seasons in a model trained on ${B.first_training_season}-${meta.latest_season}; across eras the model ranks real lineups with about ${Math.round(100 * B.cross_era_correlation[rule])}% of its in-era correlation, and levels across eras are not validated`);
      }
      return reasons;
    }
    function assumptionReasons(margins) {
      const moved = margins.C - margins.R;
      if (Math.abs(moved) <= B.spread_reason) return [];
      return [`assumption C, capacity defense, moves the margin ${moved >= 0 ? "+" : ""}${fmt(moved, 1)}: rim protection counts only the two best inside defenders, and each attacker is matched with one defender. The era backtest found real big defenses did better than this assumes, so it is a labeled alternative, not the forecast.`];
    }
    function withLayer(byArm, keys, layer, learned) {    // lineups.band.Band.with_layer
      const out = {}, add = (k) => (learned ? learned[k] : 0);
      for (const k of keys) {
        out[k] = Object.fromEntries(B.arms.map((a) => [a, byArm[a][k] + add(k) + (layer ? layer.layer[k] : 0)]));
        if (layer) out[k].K = byArm.R[k] + layer.continued[k] + add(k);
        if (learned) out[k].N = byArm.R[k] + (layer ? layer.layer[k] : 0);
      }
      return out;
    }
    function learnedReasons(learned, key, label) {
      if (!learned || Math.abs(learned[key]) <= B.spread_reason) return [];
      return [`assumption N: the learned combinations move the ${label} ${learned[key] >= 0 ? "+" : ""}${fmt(learned[key], 1)}. They are learned from real lineups at half strength and are not validated one by one; without them the players add up, apart from the measured combination effects.`];
    }
    function combinationReasons(layer, key, label) {
      if (!layer || !layer.beyond.length) return [];
      const past = layer.beyond.map((b) => `${b.count} ${K.plurals[b.type]} on ${b.side} (measured up to ${b.measured})`).join("; ");
      const moved = layer.continued[key] - layer.layer[key];
      return [`assumption K: combination effects are held at the most players of a type measured together: ${past}. If they keep adding pair by pair, the ${label} moves ${moved >= 0 ? "+" : ""}${fmt(moved, 1)}.`];
    }
    function interval(values, variance) {
      const sd = Math.sqrt(variance), vs = Object.values(values), lo = Math.min(...vs), hi = Math.max(...vs);
      return { point: values.R, low: lo - B.z * sd, high: hi + B.z * sd, sd, assumption_low: lo, assumption_high: hi };
    }
    function bandLineup(rows, rule, layer, learned) {
      const byArm = {};
      B.arms.forEach((a) => { byArm[a] = ratings(rows, rule, a); });
      const share = crossEraShare(rows), ce = B.cross_era_variance[rule];
      const variance = { offense: B.tau2.offense + ce * share, defense: B.tau2.defense + ce * share,
                         margin: B.tau2.margin + 2 * ce * share };
      const out = {}, values = withLayer(byArm, Object.keys(variance), layer, learned);
      for (const k of Object.keys(variance)) out[k] = interval(values[k], variance[k]);
      out.arms = byArm;
      out.reasons = [...compositionReasons(rows, rows), ...playerReasons(rows, "the lineup", rule),
                     ...assumptionReasons(Object.fromEntries(B.arms.map((a) => [a, byArm[a].margin]))),
                     ...combinationReasons(layer, "margin", "net"), ...learnedReasons(learned, "margin", "net")];
      return out;
    }
    function bandMatchup(aRows, bRows, rule, layer, learned) {
      const byArm = {};
      B.arms.forEach((a) => { byArm[a] = matchup(aRows, bRows, rule, a); });
      const sa = crossEraShare(aRows), sb = crossEraShare(bRows), ce = B.cross_era_variance[rule];
      const side = B.tau2.offense + B.tau2.defense;
      const variance = { a_offense: side + ce * (sa + sb), b_offense: side + ce * (sa + sb),
                         margin: 2 * B.tau2.margin + 2 * ce * (sa + sb) };
      const out = {}, values = withLayer(byArm, Object.keys(variance), layer, learned);
      for (const k of Object.keys(variance)) out[k] = interval(values[k], variance[k]);
      out.arms = byArm;
      let reasons = [];
      for (const [label, mine, theirs] of [["team A", aRows, bRows], ["team B", bRows, aRows]]) {
        reasons = reasons.concat(compositionReasons(mine, theirs).filter((r) => !r.startsWith("defense")).map((r) => `${label}: ${r}`));
        reasons = reasons.concat(playerReasons(mine, label, rule));
      }
      out.reasons = reasons.concat(assumptionReasons(Object.fromEntries(B.arms.map((a) => [a, byArm[a].margin]))),
                                   combinationReasons(layer, "margin", "margin"), learnedReasons(learned, "margin", "margin"));
      return out;
    }

    // ---- explanations (lineups.explain) ---------------------------------------------------
    const E = meta.explain;
    // Each seed's checkpoint mixture, seeds weighted equally (Release.ledger): checkpoint weight 1 / (seeds x its
    // checkpoints). Adds w times the mixture's sums against one opponent into team (and per attacker into players).
    const newTeam = () => ({ points: 0, fga: 0, fta: 0, tov: 0, ftm: 0, orb: 0, attempts: new Array(6).fill(0),
                             makes: new Array(6).fill(0), demand: 0, supply: 0 });
    const copyTeam = (t) => ({ ...t, attempts: t.attempts.slice(), makes: t.makes.slice() });
    function mixInto(arm, fo, fd, w, team, players, ix) {
      for (const s of seeds) {
        const ks = ix[arm][s], u = w / (seeds.length * ks.length);
        for (const n of ks) { pair(fo, fd, n, S1); mixAdd(team, players, S1, u); }
      }
    }
    function channels(lineup, reference) {
      const a0 = reference.attempts, a1 = lineup.attempts, s0t = sum(a0), s1t = sum(a1);
      let volume = 0, mix = 0, conversion = 0;
      for (let z = 0; z < 6; z++) {
        const m0 = reference.makes[z] / a0[z], m1 = lineup.makes[z] / a1[z], s0 = a0[z] / s0t, s1 = a1[z] / s1t, v = SHOT_VALUES[z];
        volume += (lineup.fga - reference.fga) * s0 * m0 * v;
        mix += lineup.fga * (s1 - s0) * m0 * v;
        conversion += lineup.fga * s1 * (m1 - m0) * v;
      }
      const k = 100 * E.slope;
      return { volume: k * volume, shot_mix: k * mix, conversion: k * conversion, free_throws: k * (lineup.ftm - reference.ftm) };
    }
    function summary(t) {
      const tot = sum(t.attempts);
      return { fga: 100 * t.fga, fta: 100 * t.fta, turnovers: 100 * t.tov, offensive_rebounds: 100 * t.orb,
               three_share: (t.attempts[4] + t.attempts[5]) / tot, rim_share: t.attempts[0] / tot,
               rim_fg: t.makes[0] / t.attempts[0], three_fg: (t.makes[4] + t.makes[5]) / (t.attempts[4] + t.attempts[5]) };
    }
    function playersFrom(x, rows, rule) {          // x: the mixture's per-attacker sums (FGA, FTA, TOV, points, threes, rim)
      const load = [0, 1, 2, 3, 4].map((i) => x[6 * i] + C.usage_weights[1] * x[6 * i + 1] + x[6 * i + 2]);
      const base = rows.map((r) => player(r, rule).base);
      const own = base.map((b) => [0, 1, 2].reduce((s, k) => s + C.usage_weights[k] * Math.exp(clamp(b[k], -12, 4)), 0));
      const totalLoad = sum(load), totalOwn = sum(own);
      return rows.map((r, i) => ({ player: meta.names[String(pid[r])], season: season[r], usage_share: load[i] / totalLoad,
        usual_share: own[i] / totalOwn, points: 100 * x[6 * i + 3], threes: 100 * x[6 * i + 4], rim_attempts: 100 * x[6 * i + 5] }));
    }
    function explainLineup(rows, rule) {
      const x = pass(fiveOf(rows, rule), rule), total = copyTeam(x.team), players = x.players;
      const league = Object.assign({}, E.league);
      return { team: summary(total), league: summary(league), channels: channels(total, league),
               players: playersFrom(players, rows, rule), creation: { demand: 100 * total.demand, supply: 100 * total.supply },
               rates: total };
    }
    function explainAgainst(rows, opponentRows, rule) {
      const f = fiveOf(rows, rule), average = copyTeam(pass(f, rule).team), mine = newTeam(), players = new Float64Array(30);
      mixInto(meta.forecast, f, fiveOf(opponentRows, rule), 1, mine, players, idx);
      return { team: summary(mine), average_defense: summary(average), channels: channels(mine, average),
               players: playersFrom(players, rows, rule), rates: mine };
    }

    // ---- combination effects (lineups.combinations) ------------------------------------------
    const K = meta.combinations, KL = K.layer;
    const typeBit = Object.fromEntries(K.types.map((t, j) => [t, j]));
    const effectInfo = Object.fromEntries(K.effects.map((e) => [e.id, e]));
    const isOffense = (id) => id.split(":")[1].startsWith("O");
    const flagRows = (rows, rule, names) => rows.map((r) => names.map((t) => (K.flags[rule][r] >> typeBit[t]) & 1));
    function layerTerms(offRows, defRows, rule, cap) {     // {effect id: [beta, pairs, expected pairs]}
      const out = {};
      for (const [event, e] of Object.entries(KL.events)) {
        for (const [side, names, rows] of [["offense", K.offense, offRows], ["defense", K.defense, defRows]]) {
          if (!e.pairs.some((p) => p[0] === side)) continue;
          const F = flagRows(rows, rule, names), n = {};
          names.forEach((t, j) => { let c = 0; for (const f of F) c += f[j]; n[t] = cap ? Math.min(c, KL.measured_max[t]) : c; });
          e.pairs.forEach((p, k) => {
            if (p[0] !== side) return;
            const a = p[1], b = p[2];
            let P;
            if (a === b) P = n[a] * (n[a] - 1) / 2;
            else {
              const ja = names.indexOf(a), jb = names.indexOf(b);
              let overlap = 0; for (const f of F) overlap += f[ja] & f[jb];
              P = n[a] * n[b] - Math.min(overlap, Math.min(n[a], n[b]));
            }
            let s = 0;
            e.types.forEach((t, j) => { if (t in n) s += e.slopes[k][j] * n[t]; });
            out[`${event}:${a}x${b}`] = [e.beta[k], P, e.intercept[k] + s];
          });
        }
      }
      return out;
    }
    function unitValues(t) {                               // lineups.combinations.values, per-100 points per unit
      const total = sum(t.attempts), share = t.attempts.map((a) => a / total);
      const value = t.makes.map((m, z) => m / Math.max(t.attempts[z], 1e-12) * SHOT_VALUES[z]);
      let perFga = 0; for (let z = 0; z < 6; z++) perFga += share[z] * value[z];
      const moved = (zones) => {
        let sIn = 0, vIn = 0, vOut = 0;
        for (let z = 0; z < 6; z++) {
          if (zones.includes(z)) { sIn += share[z]; vIn += share[z] * value[z]; } else vOut += share[z] * value[z];
        }
        return t.fga * (vIn / Math.max(sIn, 1e-12) - vOut / Math.max(1 - sIn, 1e-12));
      };
      return { rim_share: moved([0]), three_share: moved([4, 5]), tov: -t.points / (1 - t.tov), fta: t.ftm / t.fta - 0.5 * perFga };
    }
    const panelCache = {};
    function panelMeans(rule) {                           // {side:cap: {effect: mean event change}}
      if (panelCache[rule]) return panelCache[rule];
      const out = {};
      for (const side of ["offense", "defense"]) {
        const P = meta.panel[side];
        for (const cap of [true, false]) {
          const acc = {};
          P.rows.forEach((rows, i) => {
            for (const [id, [b, pairs, x]] of Object.entries(layerTerms(rows, rows, rule, cap))) {
              if (isOffense(id) !== (side === "offense")) continue;
              acc[id] = (acc[id] || 0) + P.weights[i] * (b * (pairs - x));
            }
          });
          out[`${side}:${cap}`] = acc;
        }
      }
      return (panelCache[rule] = out);
    }
    function effectsOf(terms, values, keep) {
      const out = [];
      for (const [id, [b, pairs, x]] of Object.entries(terms)) {
        if (!keep(id)) continue;
        const event = id.split(":")[0], change = b * (pairs - x);
        out.push({ id, title: effectInfo[id].title, side: effectInfo[id].side, event, pairs, expected: x, change,
                   points: change * values[event] });
      }
      return out.sort((p, q) => Math.abs(q.points) - Math.abs(p.points));
    }
    const panelPoints = (means, values) => sum(Object.entries(means).map(([id, v]) => v * values[id.split(":")[0]]));
    function beyond(offRows, defRows, rule) {
      const used = new Set();
      for (const e of Object.values(KL.events)) for (const p of e.pairs) { used.add(p[1]); used.add(p[2]); }
      const out = [];
      for (const [names, rows, side] of [[K.offense, offRows, "offense"], [K.defense, defRows, "defense"]]) {
        const F = flagRows(rows, rule, names);
        names.forEach((t, j) => {
          let n = 0; for (const f of F) n += f[j];
          if (used.has(t) && n > KL.measured_max[t]) out.push({ type: t, side, count: n, measured: KL.measured_max[t] });
        });
      }
      return out;
    }
    function notes(rows, rule, label) {                    // H1, pre-registered for 2026-27; not in the number
      let small = 0, anchor = false;
      for (const r of rows) { small += (K.flags[rule][r] >> K.h1_bits.small) & 1; anchor = anchor || Boolean((K.flags[rule][r] >> K.h1_bits.anchor) & 1); }
      return small ? [{ id: "h1", label, small, anchor }] : [];
    }
    function combinationsLineup(rows, rule, rates) {
      const vOwn = unitValues(rates), vLeague = unitValues(E.league), panel = panelMeans(rule), out = {};
      for (const [cap, key] of [[true, "layer"], [false, "continued"]]) {
        const terms = layerTerms(rows, rows, rule, cap);
        const off = effectsOf(terms, vOwn, isOffense), de = effectsOf(terms, vLeague, (id) => !isOffense(id));
        const offPanel = panelPoints(panel[`defense:${cap}`], vOwn), defPanel = panelPoints(panel[`offense:${cap}`], vLeague);
        const offense = sum(off.map((e) => e.points)) + offPanel, defense = sum(de.map((e) => e.points)) + defPanel;
        out[key] = { offense, defense, margin: offense - defense };
        if (cap) { out.effects = { offense: off, defense: de }; out.opponent = { offense: offPanel, defense: defPanel }; }
      }
      out.beyond = beyond(rows, rows, rule);
      out.notes = notes(rows, rule, "the lineup");
      return out;
    }
    function combinationsMatchup(aRows, bRows, rule, aRates, bRates) {
      const va = unitValues(aRates), vb = unitValues(bRates), out = {};
      for (const [cap, key] of [[true, "layer"], [false, "continued"]]) {
        const ea = effectsOf(layerTerms(aRows, bRows, rule, cap), va, () => true);
        const eb = effectsOf(layerTerms(bRows, aRows, rule, cap), vb, () => true);
        const a = sum(ea.map((e) => e.points)), b = sum(eb.map((e) => e.points));
        out[key] = { a_offense: a, b_offense: b, margin: a - b };
        if (cap) out.effects = { a_offense: ea, b_offense: eb };
      }
      out.beyond = beyond(aRows, bRows, rule).concat(beyond(bRows, aRows, rule));
      out.notes = notes(aRows, rule, "team A").concat(notes(bRows, rule, "team B"));
      return out;
    }
    function typesOf(r, rule) { return K.types.filter((t) => (K.flags[rule][r] >> typeBit[t]) & 1); }

    // ---- the missing piece (Adam, 2026-10-14): rank candidate fifths for a four-player core ----------------
    // forecast: the printed number for a lineup against the league-average opponent (band.lineup's point: the
    // calibrated network, half the learned module, the measured combinations), with its parts. With a view, the
    // same on fewer checkpoints and panel lineups, to rank candidates before the exact forecast (screen).
    function forecastOf(rows, rule, v) {
      const x = pass(fiveOf(rows, rule), rule, v), layer = combinationsLineup(rows, rule, x.team).layer;
      const L = x.learned || { offense: 0, defense: 0, margin: 0 };
      return { offense: x.offense + L.offense + layer.offense, defense: x.defense + L.defense + layer.defense,
               margin: x.margin + L.margin + layer.margin, network: x.margin, learned: L.margin, combinations: layer.margin };
    }
    // The screen's view: one checkpoint per seed and 10 panel lineups a side. On eight cores of 2025-26 players
    // its ranking held every exact top-10 candidate within its top 19 (scripts/screen_check.js); the page
    // forecasts the screen's top 30 exactly.
    const SCREEN = view("screen", 10, 1);
    // Against one opponent five (Team B): the forecast arm's calibrated points and the learned module's, one way.
    const POINTS = FIELDS.indexOf("points");
    function oneWay(fo, fd, ix) {
      const F = meta.forecast, natives = new Float64Array(seeds.length), rates = LR && shared ? clearRates() : null;
      seeds.forEach((s, i) => {
        const ks = ix[F][s], mods = rates ? (modsOf[s] || []) : [];
        let p = 0;
        for (const n of ks) {
          p += pair(fo, fd, n, S1);
          for (const m of mods) { addRates(rates[m][0], S1, ks.length); moduleOn(fo, fd, n, m, rates, ks.length); }
        }
        natives[i] = p / ks.length;
      });
      const learned = !LR ? 0 : rates ? learnedInto(rates, X1)[POINTS] : learnedOf(fo, fd)[POINTS];
      return { points: calibrate(F, natives), learned };
    }
    // The printed forecast for Team A against Team B (band.matchup's point), with its parts.
    function matchupOf(aRows, bRows, rule, v) {
      const fa = fiveOf(aRows, rule), fb = fiveOf(bRows, rule), ix = v ? v.idx : idx;
      const a = oneWay(fa, fb, ix), b = oneWay(fb, fa, ix), ra = newTeam(), rb = newTeam();
      mixInto(meta.forecast, fa, fb, 1, ra, null, ix); mixInto(meta.forecast, fb, fa, 1, rb, null, ix);
      const layer = combinationsMatchup(aRows, bRows, rule, ra, rb).layer;
      return { a_offense: a.points + a.learned + layer.a_offense, b_offense: b.points + b.learned + layer.b_offense,
               margin: a.points - b.points + (a.learned - b.learned) + layer.margin, network: a.points - b.points,
               learned: a.learned - b.learned, combinations: layer.margin };
    }
    const forecast = (rows, rule, opponent, v) => (opponent ? matchupOf(rows, opponent, rule, v) : forecastOf(rows, rule, v));
    const screen = (core, candidates, rule, v, opponent) => candidates.map((c) => forecast([...core, c], rule, opponent, v || SCREEN).margin);
    // The range the main result shows for a lineup (against the average opponent or one five), without the
    // breakdowns it also draws.
    function bandOf(rows, rule, opponent) {
      if (!opponent) return bandLineup(rows, rule, combinationsLineup(rows, rule, pass(fiveOf(rows, rule), rule).team), learnedRatings(rows, rule));
      const fa = fiveOf(rows, rule), fb = fiveOf(opponent, rule), ra = newTeam(), rb = newTeam();
      mixInto(meta.forecast, fa, fb, 1, ra, null, idx); mixInto(meta.forecast, fb, fa, 1, rb, null, idx);
      return bandMatchup(rows, opponent, rule, combinationsMatchup(rows, opponent, rule, ra, rb), learnedMatchup(rows, opponent, rule));
    }
    // Compute the panel's sides before the first search: for the screen, the exact forecast, and (unless
    // only "forecast" is asked for) the band's other arms.
    function warm(rule, only) {
      const rows = meta.panel.defense.rows[0];
      screen(rows.slice(0, 4), [rows[4]], rule);
      if (only === "screen") return;
      forecastOf(rows, rule, null);
      if (only === "forecast") return;
      for (const arm of Object.keys(idx)) if (arm !== meta.forecast) ratings(rows, rule, arm);
    }

    // ---- a player-season's capability estimates (the library's adjusted regressions) -----------------
    // Three blocks of 16 coefficients on the event links (counts: log rate; location: multinomial logit;
    // conversion: logit; recovery: log odds of the offensive rebound): his own events, his teammates' events
    // while he is on the floor, and the events of the players he defends against. Each with its standard
    // error and the evidence behind it. Raw (as he played); the bank is already relative to his league.
    const FAMILY = [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3];
    function estimates(r) {
      const o = block(r, "adjusted_offense"), d = block(r, "adjusted_defense");
      const part = (v, c, m, s) => ({ coef: Array.from(v.subarray(c, c + 16)), mass: Array.from(v.subarray(m, m + 16), Math.expm1),
                                      sd: Array.from(v.subarray(s, s + 16), Math.exp) });
      return { own: part(o, 0, 32, 64), teammates: part(o, 16, 48, 80), defense: part(d, 0, 16, 32) };
    }
    const percentileCache = new Map();
    function seasonTables(s) {
      // per block and coordinate: sorted coefficients of the season's players with at least the season's median
      // evidence on that coordinate's family
      if (percentileCache.has(s)) return percentileCache.get(s);
      const rows = [];
      season.forEach((x, r) => { if (x === s) rows.push(r); });
      const all = rows.map(estimates), out = {};
      for (const b of ["own", "teammates", "defense"]) {
        const evidence = all.map((e) => [0, 1, 2, 3].map((f) => e[b].mass.reduce((t, m, k) => t + (FAMILY[k] === f ? m : 0), 0)));
        const median = [0, 1, 2, 3].map((f) => { const v = evidence.map((x) => x[f]).sort((a, c) => a - c); return v[Math.floor(v.length / 2)]; });
        out[b] = Array.from({ length: 16 }, (_, k) => all.filter((e, i) => evidence[i][FAMILY[k]] >= median[FAMILY[k]])
          .map((e) => e[b].coef[k]).sort((a, c) => a - c));
      }
      percentileCache.set(s, out);
      return out;
    }
    function profile(r) {
      const e = estimates(r), tables = seasonTables(season[r]), out = { season: season[r], blocks: {} };
      for (const b of ["own", "teammates", "defense"]) {
        out.blocks[b] = e[b].coef.map((c, k) => {
          const v = tables[b][k];
          let lo = 0, hi = v.length;
          while (lo < hi) { const m = (lo + hi) >> 1; if (v[m] < c) lo = m + 1; else hi = m; }
          return { coef: c, sd: e[b].sd[k], evidence: e[b].mass[k], percentile: v.length ? 100 * lo / v.length : null, among: v.length };
        });
      }
      return out;
    }

    function row(p, s) { const r = rowIndex.get(p * 10000 + s); if (r === undefined) throw new Error(`no player-season ${p} ${s}`); return r; }
    function seasonsOf(p) { const out = []; pid.forEach((q, r) => { if (q === p) out.push(season[r]); }); return out.sort(); }

    return { meta, row, seasonsOf, defaultSeason: (p) => meta.defaults[String(p)], name: (p) => meta.names[String(p)],
             points, ratings, matchup, nativeBySeed, profile,
             search: { screen, forecast: (rows, rule, opponent) => forecast(rows, rule, opponent, null), band: bandOf, view, warm, memo },
             band: { lineup: bandLineup, matchup: bandMatchup },
             learned: { lineup: learnedRatings, matchup: learnedMatchup, points: learnedPoints },
             explain: { lineup: explainLineup, against: explainAgainst },
             combinations: { lineup: combinationsLineup, matchup: combinationsMatchup, terms: layerTerms, values: unitValues,
                              types: typesOf } };
  }

  const api = { create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.LineupModel = api;
})(typeof window !== "undefined" ? window : globalThis);
