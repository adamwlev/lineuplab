# Working agreement

## 2026-09-15 override — direct implementation

Adam asked Codex to stop using Opus workers and implement directly. Do not
delegate to Opus or other agents. This supersedes the lead/worker execution
instructions below, which are retained as historical context. Codex owns
implementation as well as design, verification and communication.

Read `CLAUDE.md`, then the latest checkpoint in `SESSION_HANDOFF.md` and the
product contract in `CONTEXTUAL_MODEL.md`. Those remain the research sources
of truth; this file defines how Codex and the implementation worker cooperate.

## Lead / worker workflow

Codex is the lead: own user communication, intent, architecture, experiment
design, task decomposition, acceptance criteria, review, and final decisions.
Use `.agents/skills/opus-worker/SKILL.md` for substantial implementation after
the direction is settled. Delegate when the problem is intellectually settled
but mechanically expensive. Make small changes directly.

Before delegation, inspect the relevant code and write a bounded implementation
contract. Do not forward an ambiguous request or ask Opus to choose the model,
architecture, next experiment, or product tradeoffs. The worker implements;
Codex independently reviews the actual changes and verifies the result.

Use one Claude Code / Opus worker at a time, sequentially in this working tree.
Do not edit while it runs, and ask Adam not to run another editing session in
parallel. No worker branches, commits, staging, stashing, resets, cleaning,
reverts, publishing, or additional agents. No bypass-permissions or API-billing
fallback. A blocked worker returns control to the lead.

The runner's before/after comparison separates worker edits from existing dirty
work. It is an audit aid, not a sandbox or complete backup. Review all changed
paths, including untracked files, and preserve pre-existing work. Never treat a
worker's successful exit or written handoff as proof of correctness.

## Amendment 2026-09-07 — a second lead for the on-floor influence workstream

Adam asked Claude Opus directly to design and advance the on-floor / on-off
influence work (`TEAMMATE_INFLUENCE_EXPERIMENT.md`). For **that workstream only**,
Opus acts as lead rather than worker: it owns the estimand, the design, the
pre-registration, the cutoff rules and the write-up, and it may commit its own
documents and code. Everything above still governs every other workstream, and
Codex remains the lead there.

Boundaries that do not change, for either agent:

- No scraper, database mutation, cache rebuild, scorer promotion or page
  deployment without Adam saying so in the request itself.
- No edits to a completed run directory under `experiments/cache/`, and no
  change that invalidates a frozen protocol fingerprint. New work, new prefix.
- `MODEL_FEEDBACK_FROM_CLAUDE.md` is preserved untouched.
- Pre-registration still binds the agent that wrote it: a protocol is not
  revised in response to the results it produced.
- One editing agent in this working tree at a time. Opus and Codex must not run
  concurrent editing sessions; whoever is working says so in the handoff.

Commits from this workstream are ordinary repository commits on `main`, with the
model and session recorded in the trailer, so Codex can review or revert them.

## Basketball-specific boundaries

- `CONTEXTUAL_MODEL.md` §2 defines three co-equal standards: forward prediction,
  basketball-coherent counterfactuals, and honest out-of-distribution uncertainty.
  Do not replace that contract with maximizing r² alone or a coverage gate.
- The primary model has no known-pair chemistry. Named examples are mechanism
  checks, not invitations to add player-specific bonuses or force a total ranking.
- Codex owns pre-registration, causal cutoff rules, comparison populations,
  tuning decisions, and interpretation. Opus may implement an agreed protocol;
  it must not change that protocol in response to results.
- No scraper, database mutation, expensive sweep, cache rebuild, scorer promotion,
  or page deployment unless the task explicitly includes it.
- Preserve `MODEL_FEEDBACK_FROM_CLAUDE.md`; it is Adam's supplied feedback.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u` for model code/tests.

## Worker entry point

Read the skill before using it. Check authentication without a model call:

```bash
bash .agents/skills/opus-worker/scripts/run-opus.sh --check
```

If the Codex sandbox cannot access the macOS Keychain or Claude's network,
request the normal execution approval. Do not reinterpret that failure as a
need to log out, replace credentials, or weaken permissions.
