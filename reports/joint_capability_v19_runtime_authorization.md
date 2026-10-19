# V19 runtime decision — 2026-09-30

After reviewing the [prelaunch checkpoint](joint_capability_v19_prelaunch.md),
Adam directed: “Let’s keep that optimization in our back pocket. Something like
65 hours is fine for v19.”

This is an operational amendment, not a change to the scientific experiment:

- Roughly65hours is acceptable; the former48h reference/54h stress targets are
  no longer launch blockers. This is neither a precise runtime promise nor a
  hard process-kill deadline. Report a materially larger all-in estimate before
  launch if the remaining measurements reveal one.
- Defer the per-epoch reference-validation optimization. Keep the current
  verified fitter and all scientific arms, seeds, cutoffs, objectives, stopping
  rules and required analyses unchanged. Do not spend further v19 prelaunch
  time implementing or benchmarking this optional speedup.
- Keep the optimization as a future engineering option, backed by
  `experiments/cache/joint_capability_2026_09_30_v19_validation_profile1`.
  Future adoption still requires a new versioned producer and exact trajectory,
  selection and resume verification.
- Complete the remaining analysis/launcher integration and all-in storage check,
  including the10GiB reserve. Existing launch approval remains conditional on
  readiness; this decision does not make the unfinished pipeline ready.

The measured native-only estimates remain53.19h selected and63.82h at1.2× stress;
downstream runtime remains additional and not yet fully measured. Preserve the
original frozen plan, producer fingerprints, completed resource reports and
prelaunch report. Future readiness manifests should bind this amendment alongside
the unchanged plan so they do not enforce superseded runtime thresholds.

No optimization, training launch, artifact deletion or commit accompanies this
documentation update.
