# Contextual lineup modeling: literature and research notes

Date: 2026-09-27. Requested by Adam after the J_BOTH architecture discussion.
This records the external review and the ideas it prompted. It is **not a
frozen experiment, implementation authorization, or amendment to v17**.
The [canonical backlog](../MODEL_RESEARCH_ROADMAP.md) still owns priorities.

## Assessment of novelty

The broad problem and approach have clear precedents: infer basketball skills
from play-by-play, combine ten players nonadditively, predict unfamiliar
lineups, and value a player relative to particular teammates. Neural set
aggregation and uncertainty-aware lineup evaluation also have precedents.
Do not claim we invented contextual lineup modeling, event-based synergy,
or graph/neural lineup prediction.

We did not find an exact match for our combination of strictly dated adjusted
multi-event profiles, separate own/teammate influence information, support and
coefficient-uncertainty inputs, identity-free neural context, explicit
creation/workload/renewal accounting, and three-pillar evaluation. This is a
candidate contribution, not a certified first. No head-to-head replication
establishes superiority over the literature. Private team work is unknown.

The most promising empirical claim is narrower: adjusted event representations
may improve lineup generalization more reliably than more elaborate neural
interaction architectures. The [v16 review](joint_capability_v16_codex_review.md)
supports investigating that claim, with its shared-data/multiplicity caveats.
It does not establish causal complementarity or valid synthetic OOD means.

Scope: focused public-source search, not a systematic/exhaustive review.
Source descriptions below distinguish papers, abstracts and live project
documentation. Publication/preprint dates come from the works, not search
engine crawl dates. Published possession metrics, classification accuracy,
KL divergence and our weighted lineup-quarter r² are not comparable scores.

## Closest predecessors

### Skills Plus Minus — Maymin, Maymin and Shen (2013)

[NBA Chemistry: Positive and Negative Synergies in Basketball — full paper](https://philipmaymin.com/papers/Maymin%20Maymin%20and%20Shen%20-%20NBA%20Chemistry%20-%20IJCSS.pdf).
Inspected methods, data and interpretation sections.

Uses roughly 987,000 NBA/ESPN-derived plays from 2006–2010. Nested probit
models estimate offensive/defensive player event effects. The possession
process combines those skills to measure lineup synergy relative to individual
values and examine trades. This is skill interaction, not merely a known-pair
bonus table. Entry states distinguish steals, rebounds and out-of-bounds play.

Precision correction to the initial conversational summary: although the
framework supports game simulation, the paper's main calculations use
steady-state expectations rather than repeated full-game simulation. Its
outcome variability discussion is not evidence of validated uncertainty about
arbitrary lineups' true quality. This is our closest accounting/skill-synergy
ancestor; rebound-driven nonadditivity is not a new concept.

### Complementary skill sets — Joseph Kuehn (2016 conference; 2017 journal)

[Conference description](https://www.sloansportsconference.com/research-papers/accounting-for-complementary-skill-sets-when-evaluating-nba-players-values-to-a-speci-ic-team),
[Economic Inquiry publication](https://onlinelibrary.wiley.com/doi/abs/10.1111/ecin.12451).
Descriptions/abstracts inspected; linked conference full text was not retrieved.

Models possessions as event progressions depending on offensive skills,
defensive skills and teammate complementarities. Separates individual
production from teammate effects and studies lineup-specific value. Very close
to our product question. Detailed estimation/data/validation comparisons need
full-text follow-up; do not infer those details from the abstract.

### Play-style profiles — Matthew Goldberg (2017 thesis)

[Evaluating Lineups and Complementary Play Styles in the NBA — full thesis](https://dash.harvard.edu/server/api/core/bitstreams/acbdac45-fdea-4960-a957-d4ba7637dd46/content).
Inspected data, methods and validation/results sections.

Uses eleven seasons of Basketball Reference play-by-play and statistical
player profiles for both lineups. Tests dimensionality reduction and
regression methods; PCA plus linear regression beats the tested tree/boosting
alternatives. Players are ordered by RAPM, so this is not just additive RAPM.
The final two seasons are held out. Our permutation-equivariant event network
differs, but neither the source data nor profile-based lineup prediction is new.

### NBA2Vec — Guan, Javed and Lu (2023 preprint)

[Full paper](https://arxiv.org/html/2302.13386v1). Methods and evaluation inspected.
Learns eight-dimensional player-ID embeddings, separately averages offense
and defense, and predicts 23 event outcomes through an MLP. Millions of
play-by-play events; rebounds/defensive plays are excluded in preprocessing.
Closer to our early embedding models than current J_BOTH. A useful neural
reference, not a directly comparable published leaderboard result.

### Ability versus play choice — Skinner and Guy (2015)

[Full PLOS ONE paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136393).
Methods and empirical scope inspected.

Describes offense as a network whose transition success depends on player
skills, while play frequencies reflect coaching/strategy. Proposes joint
inference of abilities and intended plays. Motivated by tracking, but its
real-data demonstration uses 401 hand-recorded possessions, alongside
simulation—not a league-wide public-PBP benchmark. Its separation of ability
from deployment is especially relevant to our unfinished role adaptation.

## Additional references and limits

| Reference | Relevance / evidence inspected |
| --- | --- |
| [Arcidiacono, Kinsler and Price, Productivity Spillovers in Team Production (2017)](https://www.journals.uchicago.edu/doi/pdf/10.1086/687529?download=true) | Publication abstract: own productivity and ability to facilitate others are distinct. Full estimation not audited. |
| [Martonosi, Gonzalez and Oshiro, Predicting Elite NBA Lineups Using Individual Player Order Statistics (2023)](https://arxiv.org/abs/2303.04963) | Paper/method descriptions: transferable player statistics and previously untested lineups, but elite/non-elite classification rather than our event/rating target. |
| [Josephs and Upton, Hypergraph Adjusted Plus-Minus (2024 preprint)](https://arxiv.org/html/2403.20214v1) | Model/related-work sections: rankings for players and combinations via graph structure. Not an identity-free neural capability mechanism. |
| [L-RAPM (2026 preprint)](https://arxiv.org/html/2601.15000v1) | Methods: opponent-adjusted lineup effects shrunk toward individual-RAPM-informed priors; relevant sparse-lineup comparator. |
| [Barrientos et al., Bayesian Inferences on Uncertain Ranks and Orderings (2023 journal; earlier preprint)](https://arxiv.org/abs/1907.04842) | Abstract/publication scope: uncertainty in player and lineup orderings. Not validation of our synthetic-lineup intervals. |
| [Cervone et al., Multiresolution Stochastic Process / EPV](https://arxiv.org/abs/1408.0777) | Abstract: tracking-based event/movement process for possession value; richer information set than our public-PBP scorer. |
| [Zaheer et al., Deep Sets (2017)](https://arxiv.org/abs/1703.06114) | Established permutation-invariant/equivariant architecture family; set pooling alone is not our novelty claim. |
| [EvanZ, NBA lineup model — neural documentation](https://github.com/EvanZ/nba-lineup-model/blob/main/docs/models/neural-networks.md) | Contemporary public implementation, not peer-reviewed evidence. Documents Deep Sets, RAPM-plus-transformer and a profile extension; reports an initial nonlinear model failing to beat additive. Documentation inspected, code/results not independently reproduced. |

## Ideas prompted by the review

These are **our proposed extensions**, not claims that the cited authors
implemented our suggested experiments. Consider after the frozen v17 review.

### A. Separate capability, allocation and conditional success

Highest conceptual upside. Historical assist/shot rates mix ability with
opportunity, coaching, teammates and realized success. A future model could
separate player capabilities, lineup-dependent role allocation, and success
at allocated actions. Test predicted changes in player usage, shot mix,
assists and efficiency as well as team ratings.

Already explored: dated role features, overload constraints, v16 action
allocation, and v17 capacity-constrained creator-to-finisher flow. These are
not a clean ability/policy factorization. v17 still uses realized historical
assists as supply and a frozen assisted-make fraction. Neither is identified
potential-assist capacity. Separate latent quantities require partial pooling,
anchoring and explicit identification assumptions; PBP cannot reveal them
uniquely. No unrestricted latent-factor expansion is approved here.

### B. Link both teams through possession-entry states

Most interesting underexplored mechanism. A steal can prevent a shot and
change the stealing team's next offensive opportunity. A compact transition
model could link the two offenses through steals, rebounds and dead-ball
entries, averaging internally for the existing average-game product. It does
not require users to provide score or clock.

Already explored: v16 initial/post-ORB phase heads, without compelling point
gains. The proposed distinction is cross-team entry-state coupling, not another
renamed phase head. Audit available sequences/substitutions first; any new
derived labels, fits and runtime need a separate plan. Avoid double-counting
turnover/rebound value or treating a realized future entry mix as a forecast
input. Maintain action conservation, terminating renewal and swap symmetry.

### C. Evaluate role changes, not just novel five-player IDs

Separate new combinations with familiar roles from large role reassignment,
changed supporting skills, and team/system transfers. Build on the existing
[transfer library](../docs/history/TRANSFER_ROLE_BENCHMARK.md) and its
[review](transfer_role_benchmark_review.md), not a duplicate case collection.
Freeze cohort definitions using pre-change information; forecast subsequent
player events and team outcomes, including failed/successful adaptations.
Personnel-change dates and any retrospective annotation need explicit
availability rules. Do not select cases by subsequent model error or realized
role change and then call the results a prospective cohort test. These remain
observational predictions, not identified causal injury/trade effects.

### D. Separate accounting complementarity from contextual adaptation

Fixed skills can already produce nonadditive point values through nonlinear
links and possession accounting. Distinguish that from predicted changes in
a player's behavior/efficiency caused by model context inputs. Reuse/audit
v16 ADJUSTED_CHANNEL and message-off diagnostics first. They are not exact
SPM replications or automatically matched nested controls; verify information,
calibration and trained-versus-intervened differences before attribution.
Mechanism interventions need no synthetic winner and do not prove causality.

### E. Validate uncertainty under environment changes

Use the predeclared role/teammate-change cohorts to test interval coverage,
width and proper scores, not just point error. Preserve finite-game versus
persistent-quality uncertainty and matched U1 controls. Keep all eligible
lineups; no coverage gate. Good observed-transfer coverage would be useful,
but still would not validate five-center true-quality coverage or all cross-era
counterfactuals. Seed disagreement is not a substitute for this test.

## Decision checkpoint after v17

1. Finish and independently review v17 unchanged on all three standards.
2. Inventory existing controls/labels before proposing new fits. In particular,
   ADJUSTED_CHANNEL, early embedding models, phase/action arms and transfer
   cohorts already address parts of the external comparisons.
3. Decide whether capability/role separation or linked possession states has
   a tractable data signal and a clear hypothesis. Larger generic attention
   models are not the default next step given v16's evidence.
4. Freeze any experiment's targets, temporal information, cohorts, fair
   baselines, ablations, uncertainty tests, multiplicity and runtime first.
   A reasonable historical comparison is development evidence, not a fresh
   prospective test or a license to claim causal skills.

Unresolved reading: retrieve Kuehn's full methods; consider exact SPM and
NBA2Vec reproductions only if existing controls leave a meaningful gap.
Potential writeup framing: a temporally evaluated, profile-based neural
possession model for lineup generalization, combining adjusted event skills
with explicit basketball accounting. No publication or model promotion is
authorized by these notes.
