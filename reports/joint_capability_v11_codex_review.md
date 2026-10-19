# Independent Day5 review and Day6 direction

Codex/Astra, 2026-09-13. Read together with Sol's v11 review, not as a replacement
for completed scientific artifacts. No original model or run outputs changed.

All 6,179 saved descriptive V9 forecasts were independently replayed from actual
checkpoints using the v11 scorer. Maximum absolute discrepancy: 1.4211e-14.
Primary metrics reproduce Sol's report. Durable receipt:
`reports/joint_capability_v11_codex_audit.log`.

On the primary exposure reference, the symmetric SSE attribution of HALF versus
A yields weighted MSE deltas -0.622458 from the main-value change and -0.089256
from context, totaling -0.711714. For novel fives these are -1.786824 and
-0.262919, totaling -2.049743. Thus about 87% is attributed to main-value change
under this reference and accounting convention. This is not a causal fraction.
Uniform-reference allocation differs. The useful neural signal is not restricted
to nonadditive interactions; retaining a learned profile-value correction is a
necessary comparison in the next experiment.

VALUE_SWAP did not establish recurring improvement: its nominal interval spans
harm and benefit. CONTEXT_RELEASE is tied overall with a small exposure-reference
novel RMSE gain. Neither is a decisive new winner. Frozen recombination cannot
test adaptation to the replacement value surface, as Adam correctly anticipated.

The basketball interpretation in Sol's handoff is too strong. Negative interaction
for five Jokics could reflect diminishing returns, not incoherence. A positive
interaction also depends on reference; its sign alone is not a verdict. The
concerning comparison is final five-Gobert offense: CONTEXT_RELEASE 117.21 versus
118.56 for the conventional fixture. Inspect allocation and event totals rather
than forcing signs. Neither functional projection nor message ablation is a
causal estimate of teammate facilitation.

Core production completed, but the full Day5 plan did not: conditional projection
diagnostics, comprehensive consumed-source provenance, weighted disagreement
selection, certain breakdowns and historical Korver injection remain incomplete.
The independent audit supplied ordinary replay and SSE attribution, not the
remaining deliverables. The corrected interval summary must be used; near-nominal
finite-outcome coverage does not finish latent-mean OOD uncertainty.

Adam approves warranted refits. Day6 therefore implements two trained hybrids,
not another frozen-only gate. It uses an explicitly new exact anchored functional
decomposition to keep training practical, with frozen anchored controls separating
that reference change from adaptation. One arm trains context against A; the other
also learns an identity-free profile-value correction. Full details and limits are
in `SOL_JOINT_CAPABILITY_DAY6_PLAN.md`. No training was launched during planning.
