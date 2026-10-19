# Basketball lineup research

Build two five-player lineups and ask how they would perform together—not just
how their individual ratings add up. The intended tool combines date-specific
player capabilities, basketball mechanisms and honest uncertainty, with a
league-average opponent available by default.

Three standards have equal standing: **forward prediction, basketball-coherent
counterfactuals, and honest out-of-distribution uncertainty**. The authoritative
agreement is [CONTEXTUAL_MODEL.md §2](CONTEXTUAL_MODEL.md#2-three-co-equal-acceptance-standards).

## Start here

| Question | Authoritative page |
| --- | --- |
| Where are we now? What is next? | [Current research state](JOINT_CAPABILITY_STATE.md) |
| How do the retained models compare? | [Current scorecard](MODEL_SCORECARD.md) |
| How does the neural model actually work? | [Neural architecture](NEURAL_MODEL.md) |
| What should we build, and what is deferred? | [Prioritized research backlog](MODEL_RESEARCH_ROADMAP.md) |
| What happened in the last session? | [Current handoff](SESSION_HANDOFF.md) |
| Where is the evidence and older history? | [Documentation index](docs/README.md) |

For an editing/research session, read [AGENTS.md](AGENTS.md) and its required
context. For a quick project orientation, start with the current state above;
there is no need to reconstruct the entire research journal.

## Research is not the published tool

As of 2026-09-18, v15 is complete and independently reviewed; v16 is a
[written plan](JOINT_CAPABILITY_V16_PLAN.md), not an implemented or running model.
The research candidates have not been promoted.

[tool/five.html](tool/five.html) remains the older additive-based page.
[CURRENT_MODEL.md](CURRENT_MODEL.md) documents that shipped baseline, including
legacy pair terms and a coverage gate; those are **not** the new neural model or
the intended final product contract. [STRUCTURAL_MODEL.md](STRUCTURAL_MODEL.md)
describes the earlier pre-neural prototype.

## Working locally

Model code and tests use
`/Users/adam/miniconda3/envs/basketball25/bin/python -u`, from the repository
root. Research code is in [experiments/](experiments/), tests in [tests/](tests/),
and completed interpretations in [reports/](reports/).

The large data/checkpoint artifacts under `experiments/cache/` are local;
this is not yet a self-contained, reproducible fresh-clone distribution.
[Current state: operations](JOINT_CAPABILITY_STATE.md#operations) gives verified
read-only commands for the existing checkout. Do not rebuild data, retrain,
publish or deploy merely to read the results.

## Documentation maintenance

Current pages describe one present state; reports and frozen plans preserve
what was actually done. Replace stale operational instructions instead of
prepending another update. Preserve displaced material in the
[dated archive](docs/archive/2026-09-18_pre_cleanup/README.md), and follow the
[document ownership rules](docs/README.md#maintenance-rules).
