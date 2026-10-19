# Current model scorecard

**2026-09-18 complete v15 review:** read
`reports/joint_capability_v15_codex_review.md`. Same44quarter/5,607cell matched
primary: MAIN_RB half RMSE10.72573/MAE8.00072/r².13904 versus old HALF+D
10.73215/8.01862/.13801; incremental RMSE−.00642[−.04077,+.02369],4/11season
wins, not established. Both know actual opponents. Old NN+D leads novel RMSE
11.68172; new half11.70240 has slightly better novel MAE. Cross/rebound channels
improve11/11seasons but calibration explains most of the tiny point edge.
Post-hoc common prior-affine sensitivity reverses it; not a replacement score.
Broader cohorts are separately reported, since this primary inherits old profile
support restrictions. Finite-outcome80/95coverage79.88/94.19%; five-center
offense, stable average-opponent integration and latent OOD uncertainty remain
unfinished. **Research candidates only; no scorer promotion.** Older tables
below are historical, not the current winner list.

**Latest diagnostic, 2026-09-17:** shared game-situation adjustment is complete;
see `reports/game_situation_diagnostic_review.md` and the diagnostic addendum
below. Original forward scores are unchanged. Clock adjustment reduces much
of substantial-lineup FTA bias; relative NN/blend advantage survives, while
Cleveland's large point error remains. No scorer promotion.

**2026-09-17 separate transfer benchmark:** see
`reports/transfer_role_benchmark_review.md`. On the newly fixed retrospective
q1team-change cohort (>=200poss/5games;146cells/47,419poss), RMSE is A6.85781,
oldHALF6.68694, ROLE_SL direct6.58670/half6.63805, renewal direct6.59685/
half6.64233, combined SHIFT direct6.68083/half6.68329. This is a DIFFERENT,
higher-exposure population; do not replace full-population v14 numbers below.
OldHALF leads broader available/100poss slices. Explicit shift-channel effect
is small and uncertain. Finite-outcome coverage is reported, not latent OOD
validation; center concerns remain. No model promotion or new fit.

**2026-09-17 complete v14 review:**
`reports/joint_capability_v14_codex_review.md` supersedes older best labels on
the same44-quarter/726,364-possession primary population. Three-seed direct
RB_RENEW_FAC_SHIFT: MAE8.06193/RMSE10.79367/r².12809/corr.36084. External
half:8.04230/10.77978/.13034/.36396. Its recurring RMSE10.30223 improves
old HALF10.34554, but novel11.76679 is tied with old HALF11.76624.
ROLE_SL half has best ensemble MAE8.03297, RMSE10.78859. Renewal FAC half
8.03744/10.78462 is a useful simpler mechanism candidate. New architecture
contrasts do not survive Holm; combined-half nominal season RMSE advantage
over old HALF crosses0, versus additive does not. All three seeds support
shift/renewal directions, not a certain causal influence interpretation.
Combined five-Gobert direct120.01 exceeds conventional118.84; half115.91
versus118.95 partly relies on additive. Finite-outcome80/95 coverage79.19/94.63%;
latent-quality OOD uncertainty still unvalidated. **No scorer promotion.**

**2026-09-15 complete v13 review:**
`reports/joint_capability_v13_codex_review.md` supersedes older best-forecast
labels below on the same44-quarter primary population. Leading research blend
is half additive / J_ROLE_SUPPLY_LOAD: MAE8.03415, RMSE10.79364, r².12810;
old HALF 8.07273/10.80812/.12576. Best direct B_SUPPLY_LOAD:
8.06789/10.81579/.12452. The new blend improves recurring RMSE10.31894 versus
10.34554, but novel11.77519 trails old HALF11.76624. Season-RMSE advantage over
HALF remains uncertain (6/11; nominal CI crosses0), and winning ROLE is one seed.
Creation/load improves center behavior but39.55FTA/100 persists; native ROLE
five-Gobert118.94 is effectively tied with conventional118.89. External blend
gets115.58 versus119.19 partly through additive. New blend finite-outcome
coverage80/95 is79.15%/94.60% by cell; latent-mean OOD uncertainty remains
unvalidated. **No scorer promotion; three-pillar product acceptance unfinished.**

**2026-09-14 partial v12 qualification:** see
`reports/joint_capability_v12_partial_codex_review.md`. On 33/44 primary quarters,
flexible/strict/HALF RMSE is 10.85056/10.86143/10.76273. The latest-pilot flexible
five-Gobert offense is 125.01 versus conventional 119.32. Anchored C reverses
the apparent direction of learned message effects through subtraction of B.
No uncertainty gain is established. Hold the full rerun and discuss the design;
these partial numbers must not replace the complete-population controls below.

Updated 2026-09-13 after v12 implementation and pilots. The v12 production run
has not started, so the table still reflects completed v11/Day5 evidence. The
two v12 pilot origins are documented in
`reports/joint_capability_v12_launch_checkpoint.md` and are not promoted into
this scorecard. The three co-equal
standards remain forward prediction, basketball-coherent counterfactuals, and
honest OOD uncertainty. “Candidate” does not mean promoted or ready for the
public tool.

Read `reports/joint_capability_v11_review.md`. Frozen value replacement does not
recover recurring performance. Full projected context is tied overall and helps
novel RMSE slightly, but the extracted interaction raises five-Gobert offense and
lowers five-Jokic offense; it is not a user-facing complementarity term. Historical
rows below use different populations as labeled. Five-Gobert final offense and
arbitrary-lineup latent uncertainty remain open.

| candidate | prediction | basketball cases | uncertainty | defects / limitations | status |
| --- | --- | --- | --- | --- | --- |
| v11 CONTEXT_RELEASE, EXPOSURE reference | 8.0769 MAE / **10.8081 RMSE / .12577 r2**; novel 8.8324 / **11.7586** | Projected C is +4.77 for five Goberts, +1.66 limited centers, -7.57 five Jokics: not coherent as transferable context | Finite-outcome coverage near nominal; 13/96 integrations capped; reference sensitivity measured; latent mean unvalidated | Frozen NN cannot adapt to replacement values; reference-defined residual includes budget/value compensation | **not promoted; evidence for jointly adapted residual design** |
| v11 VALUE_SWAP, EXPOSURE reference | 8.0940 / 10.8367 / .12114; recurring RMSE 10.3497 versus HALF 10.3455 | Half-dose extracted C weakens center/Jokic interpretation; Korver/Westbrook difference reference-sensitive | Same finite-outcome method; latent mean unvalidated | Registered recurring contrast +.0054 [-.0278,+.0386], 4/11 favorable | rejected frozen value replacement |
| half corrected-additive + `V9_SPREAD` | **8.0727 MAE / 10.8081 RMSE / .12576 r2** on the 2016–26 primary population; novel 8.8386 / 11.7662 / .11348 | Retains half of the structural context correction and improves both additive and structural pooled scores | Best listed 80% weighted interval score 35.755; latent/OOD mean unvalidated | Fixed compromise rather than a unified model; season win vs additive not established | **best pre-registered combined forecast; no scorer promotion** |
| prior-only GLOBAL additive/`V9_SPREAD` | **8.0707 MAE** / 10.8097 RMSE / .12550 r2; novel 8.8418 | Context exposure similar to fixed half | Near-nominal finite-outcome coverage; latent/OOD mean unvalidated | Extra fitted weight does not materially beat fixed half | research control |
| `TEAM_1`, alpha 1 team-point loss | 8.1122 MAE / .11917 r2; novel 8.8878 / .10804 | Preserves fixture directions but attenuates clone/context magnitudes | 80% .789/.788 cell/weighted; 95% .946/.943 | Native team MSE improves 0.027%; outer event loss worse 11/11 seasons; no reliable additive win | **not adopted** |
| `TEAM_01`, alpha .1 team-point loss | 8.1591 MAE / .11511 r2; novel 8.9176 / .10468 | Preserves signs, attenuates Korver/Jokic contextual correction | Near-nominal finite-outcome coverage; latent/OOD mean unvalidated | Worse than BASE pooled; outer event loss worse 10/11 seasons | rejected dose |
| corrected additive | Standalone baseline: 8.0920 MAE / .12043 r² | No structural mechanisms | Same rolling finite-batch audit | Cannot explain contextual role/fit | candidate baseline |
| E0M_L2, anchored states + mean context | 8.1224 MAE / .11414 r²; best novel MAE 8.8574 | Mean context lowers limited centers by 10.27 and five Goberts by 12.29 vs fixed; raises five Jokics 2.52 | 80% constant interval .796/.790 cell/weighted coverage; synthetic latent mean unvalidated | No encoder, sender resolution, opponent, defense or rebound loop | provisional structural backbone |
| E1P_L2, encoder + pair context | Best neural pooled: 8.1096 MAE / .11749 r²; novel RMSE 11.7808 | Similar coherent center/clone directions; pair adds little beyond mean | Best listed 80% weighted interval score 35.937; synthetic latent mean unvalidated | Extra encoder/pair complexity; no opponent, defense or rebound loop | strongest neural reference |
| E1M_L2, encoder + mean context | 8.1234 MAE / .11637 r²; best novel RMSE 11.7773 | Mean supplies almost all E1 context behavior | 80% constant interval .796/.789 cell/weighted coverage; latent/OOD missing | Encoder has no established incremental practical gain | research control |
| pair-context aliases H2/H3 | H2 8.1228 MAE; H3 8.1229 | Preserve v3 pair reference and coherent fixtures | Full matched rolling interval report now complete | Pair resolution adds little beyond mean | reference controls |
| fixed-context E0/E1 | 8.1713 / 8.1604 MAE | Fails center/clone coherence relative to mean | Full matched rolling interval report complete | Control without actual teammate aggregate | controls |
| structural parent | 8.1440 MAE / .10733 r² | Finite usage + assist deficit; five centers weak | Intervals measured; latent/OOD missing | Flat location curve; no teammate response | historical research-only |
| location + shooting | 8.1312 MAE / .11142 r²; novel 8.8674 | Earlier Korver relative-fit result; centers 106.94 | 80% 0.801 coverage / width 33.05; latent/OOD missing | Shooting attribution remains confounded; no defense | prior structural candidate |
| corrected mix + shooting | 8.1408 MAE / .11120 r² | Mix channel forecasts but adds no established points | 80% 0.801 coverage / width 33.04 | Induced-shot conversion assumption unresolved | held |
| location + shooting + factor | 8.1407 MAE / .10984 r² | Factor improves turnover channel, not point increment | 80% 0.802 coverage / width 33.15 | Borrows shooting signal; no incremental value | held |
| all four | 8.1496 MAE / .10901 r² | Full path reconciles; weakest repaired combination | 80% 0.804 coverage / width 33.19 | Complexity without predictive payoff | rejected |
| joint capability E0M (v5 BASE) | 8.0986 MAE / .10930 r² on 2016-25; **best novel of eight arms** 8.7462 / .09947 | Mean pooling gives the clone and limited-creator response with no position rule | Not validated for a synthetic lineup's latent mean | Six input interventions all null or harmful; conversion unmoved for five versions; fixture magnitudes ~2x the in-range maximum | research backbone |
| joint capability E0M, composition holdout (v6) | HOLD75 8.1199 MAE, best withheld-region MAE of five arms (8.3164) on a quarter less data | Clone response invariant to the holdout, r = 0.9966 with the full model | Still not validated for a synthetic lineup's latent mean | Validated only ACROSS the observed range: 99.5% of withheld cells at or below the real maximum, while the fixtures sit at 1.8-3x | research backbone |
| joint capability E0M, donor-extremity holdout (v7 `HOLDX2`) | 8.0565 MAE / .1373 r² on 48 origins; best neural arm on 3 of 4 regions; −0.0164 ± 0.0077 (7/12) vs its matched random control | Clone ladder sane: 1,068 five-clone lineups span 90.85–132.43, max 106.6% of the model's own in-range prediction max | **Disagrees with the full model by 1.64 pts/100 on donors it never saw vs 0.51 on the rest**, gradient +0.0616/unit distance | Wins by deleting 21 real players (Gobert, Capela, Zubac) from training — diagnostic, not shippable | research diagnostic |
| joint capability E0M + §8.1 overload (v7 `V7_LOAD`) | 8.0637 MAE / .1375 r²; best arm on donor2 (7.6185); −0.0026 ± 0.0025 (8/12) vs FULL | `k_make_over` non-zero **48/48** (mean .0709); `k_to_over` exactly zero **47/48** — overload costs shooting, not turnovers | Unchanged from the backbone | Mechanism fits; points effect an order of magnitude below what this population resolves | mechanism candidate |
| joint capability E0M, standardised message inputs (v8 `V8_STD`) | 8.0837 MAE / .1367 r² — **fifth of seven, +0.0125 ± 0.0233 vs base** | **Improves the TRAINING objective in 47/48 origins and 12/12 seasons on all five families**: event loss −4.12e-04 ± 4e-05, conversion −1.39e-04 (first movement in seven versions) | Unchanged from the backbone | A large, unanimous objective gain that converts to nothing in points | **adopt in any future backbone; not a points lever** |
| joint capability E0M + standardised inputs + **teammate sd** (v9 `V9_SPREAD`) | 8.0730 MAE / .1400 r²; **−0.0088 ± 0.0114 vs `V9_BASE`**, and `V9_ALL` is level with `V8_BASE` at −0.0008 ± 0.0254 | **Objective improves in 12/12 seasons and 45/48 origins**: event loss −2.46e-04 ± 2e-05, and −6.58e-04 stacked against `V8_BASE`. Penalises zero-variety clone lineups 2–3x harder than the mean-only sender | Unchanged | The largest objective gain on record still converts to nothing in points | **adopt in any future backbone** |
| joint capability E0M, scale-free message penalty (v8 `V8_SCALE`) | 8.0725 MAE / .1368 r²; net event +1.21e-05 (ns) | Moved the message budget exactly as diagnosed — location 0.105→0.125, make 0.481→0.405; location −6.13e-05 (10/12), conversion +3.40e-05 (0/12) | Unchanged | The penalty's units were wrong and the wrongness was free | diagnosis confirmed, closed |

**v9's headline is that the teammate summary was a mean and nothing else.** Adding
the leave-one-out standard deviation improves the objective in 12/12 seasons and
45/48 origins, and stacked with v8's standardisation reaches −6.58e-04 against
`V8_BASE` for 576 extra parameters. A second message round is established harm and
a non-diagonal decoder is null, so the finding is the second MOMENT, not capacity.
In points it is a wash (`V9_ALL − V8_BASE` = −0.0008 ± 0.0254), which makes **a
point evaluation with power the binding constraint on the whole project**.

**v8's finding was that the model was never fed standardised inputs.** The 18
message coordinates had means from −3.663 to +1.307 and a 9.7x sd range and went
into `Linear(36, 32)` raw for eight versions; `V8_STD` fixes only that and
improves every event family in 12/12 seasons — conversion included, for the first
time in seven versions — while being worth nothing in points. Across v8's six
arms the event-loss and MAE improvements are inversely ranked (Spearman −0.886,
n = 6), which is the open question for v9. v7's `HOLDX2` lead did not survive a
matched continuous trim.

**v7 changes two standing claims.** v6's "no composition-distance gradient" was
true of v6's holdout, not of the model: pushed past the observed range the
disagreement rises to 1.64 pts/100 on withheld donors against 0.51 on the rest,
while the correlation stays at 0.9958 — correlation is blind to the level shift a
tool that prints a number cares about. And the fixture-magnitude guardrail was
being read backwards: the five-clone context swing is 255% of the in-range
maximum, but its SIGN was never checked and it is negative — a composition
penalty of −3.004 ± 0.432 pts/100 at matched score, 8/8 origins, with real
lineups untouched at +0.196. The model learned from event data the duplication
penalty the tool asserts; the magnitude is not yet calibrated.

Current decision: keep corrected additive as the predictive baseline; use
E0M_L2 as the pragmatic structural research backbone and E1P_L2 as the strongest
neural reference. Mean pooling supplies the important contextual behavior and
novel-lineup gains; pair resolution, the learned encoder and lambda .0001 do not
earn their complexity here. Rolling finite-outcome intervals are calibrated,
but composition scaling does not beat the matched constant control and
arbitrary-lineup latent-mean uncertainty is unfinished. No scorer/page change.
See `reports/joint_capability_v4_review.md`; the v3 review and artifacts remain
historical sources.
# 2026-09-17 diagnostic addendum — not new forward scores

`reports/game_situation_diagnostic_review.md` reports a shared, prior-fitted
ENV/CLOCK/MARGIN sensitivity applied identically to all saved models. Original
point scores below remain authoritative. Combined-half/additive RMSE is
10.77978/10.84099 unchanged; CLOCK-conditional diagnostic10.72205/10.78877,
MARGIN10.73364/10.80199. These use realized future context to standardize
outcomes, so they are not deployable pre-quarter improvements. Substantial
FTA bias4.010→.995→.913; Cleveland failure remains. No counterfactual/OOD pass
or promotion. Three standards remain equal.
