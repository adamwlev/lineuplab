# Joint capability v11 launch checkpoint

Prepared 2026-09-13 after implementing `SOL_JOINT_CAPABILITY_DAY5_PLAN.md`.
This is an operational checkpoint, not a result review. Production has not run.

## Implemented scope

The v11 runner projects each frozen, calibrated `V9_SPREAD` forecast into a
reference-average player main effect and a remaining lineup interaction, under
both the fixed EXPOSURE and UNIFORM prior-year reference distributions. It then
constructs the pre-registered M_ONLY, HALF, VALUE_SWAP, CONTEXT_RELEASE and
FULL_SWAP forecasts. Additive, NN and saved GLOBAL are controls. There are zero
optimizer fits and zero epochs. This is the frozen-transfer diagnostic; it does
not let neural context adapt to replacement player values.

The completed production job will automatically create scorecards, paired-season
contrasts, decomposition diagnostics, high-exposure cases and player ledgers,
basketball fixtures, reference sensitivity, finite-outcome intervals and final
machine-readable status. It will not write the eventual editorial review or
handoff; Sol does that after inspecting completed outputs.

## Verification

- Focused suite: 6 tests in 0.024 seconds, OK. Durable log:
  `reports/joint_capability_v11_focused_tests.log`.
- Full suite: 749 tests in 35.654 seconds; 748 pass. The sole failure is the
  repository reproducibility guard reporting the three new v11 Python producers
  as untracked. Day5 prohibits staging/committing, so this remains explicitly
  unresolved until Adam later authorizes a commit. Durable log:
  `reports/joint_capability_v11_test_suite.log`.
- Shell syntax and Python compilation pass. Final production preflight reports
  897,778 grouped rows, 48 eligible origins, zero fits. Durable log:
  `reports/joint_capability_v11_preflight.log`.
- Report smoke completed on the final pilot. Durable log:
  `reports/joint_capability_v11_report_smoke.log`.

Final pilot prefix:
`experiments/cache/joint_capability_2026_09_13_v11_pilot_final5/`.
It completed 4/4 origin-reference cells and 9,665,502 forward lineup evaluations
in 34.0 measured seconds. 2026q4 passed at K=512 EXPOSURE and K=256 UNIFORM.
2016q1 reached K=1024 for both references and remained honestly marked
`integration_limited` (panel RMS .1351/.1245 and maximum .3185/.2782 pts/100).
No threshold or K cap was changed in response. The report smoke includes the
derived familiar-real and clone-ladder fixtures; the historical injected Korver
state is explicitly recorded as omitted rather than approximated with a current
state. Pilot scores are operational, not research evidence. Earlier incomplete/
superseded pilot and preflight prefixes are preserved.

Linear extrapolation from the two-origin pilot is about 13.6 minutes. Applying
the slowest observed reference-cell time to all 96 cells gives about 19.2 minutes.
Allow roughly 15–25 minutes plus final reports; actual K choices and donor counts
vary. Maximum registered sampling remains K=1024 per panel.

## Verified commands

From `/Users/adam/Documents/basketball`, launch exactly once:

```bash
nohup bash experiments/run_joint_capability_v11.sh core \
  experiments/cache/joint_capability_2026_09_13_v11_prod_final \
  > experiments/cache/joint_capability_2026_09_13_v11_prod_final/logs/production.log 2>&1 &
```

Follow the quantitative live log:

```bash
tail -f experiments/cache/joint_capability_2026_09_13_v11_prod_final/logs/production.log
```

Check process/completion/exit receipts:

```bash
bash experiments/run_joint_capability_v11.sh status \
  experiments/cache/joint_capability_2026_09_13_v11_prod_final
```

The verified pre-launch status is:

```text
pid=none alive=no completed=0/96 success=no exit=pending
```

Successful completion requires `completed=96/96`, `success=yes`, `exit=0`, a
`SUCCESS.json`, and `reports/final_status.json`. A dead process without those
receipts is a failure, even if the log appears nearly complete. Resume uses the
same launch command and prefix; completed origin-reference cells are reused only
after the frozen protocol, code and source manifests match.
