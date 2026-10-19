# Can the network learn the interactions itself? Screen results — 2026-10-13

Results of the [protocol](nonlinearity_screen_protocol_2026_10_13.md),
committed (04527431) before any arm was trained. This is an exploratory
screen: one seed (17) at the 20 quarters of 2022–2026.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`.

## Summary

- **Adam's nonlinearity reward fails, as predicted.** At the strength the
  declared rule picked, it invents interactions on a massive scale and
  accuracy collapses. Weaker settings change nothing: early stopping picks an
  epoch before the reward has acted.
- **The pairwise module learns real interactions without inventing false
  ones.**
  - The residual held-up interactions fall by 40% (χ²_H 254 → 154).
  - Residual structure elsewhere falls too (χ²_N 1,417 → 1,136), the
    opposite of invention.
  - It learns roughly a third to a half of the free-throw effects, a fifth of
    rim deterrence, 10–20% of "one plays outside", and none of the turnover
    effects.
  - Accuracy on real lineups does not move: +0.0002 ± 0.0025 r² with equal
    calibration.
- **Its extrapolation is worse for pillar 2.** At 2026q4, five Goberts
  against Jokić/Westbrook rise from +11.8 to +18.7. On offense, the module
  carries "bigs together draw fouls and keep the ball", learned from two- and
  three-big lineups, to five.
- **Conclusion.** Learning interactions inside the network works on real
  lineups. It needs the same structure as the bolted-on layer before it can
  replace it: effects held at the measured counts, or a much tighter bound.
  The tool keeps the layer.

## Pilot: the reward's strength (labeled pilot, origin 2024q2)

λ = k × 0.25 / (point-loss level). The declared rule takes the smallest k
whose non-additive share reaches 5× the reference's (5 × 0.0115).

| k | Selected epoch | Non-additive share | × reference |
| ---: | ---: | ---: | ---: |
| 1 | 7 | 0.0132 | 1.15 |
| 10 | 1 | 0.0144 | 1.25 |
| 100 | 1 | 0.305 | 26 |

- At k = 10 and k = 100 the training loss goes negative within two epochs,
  and the validation objective rises from 1.28 to 3.4–4.7.
- Early stopping therefore keeps epoch 1. The rule picks k = 100.

## Results (2022–2026, 20 origins, seed 17)

| | reference | pairs | pairs_fast | reward (k = 100) |
| --- | ---: | ---: | ---: | ---: |
| Non-additive share of points-forecast variance | 0.0110 | 0.0193 | 0.0180 | 0.31 |
| χ²_H, residual, 14 held-up cells (lower = learned) | 253.5 | 153.5 | 149.1 | 1,781 |
| χ²_N, residual, 511 other cells (higher = invented) | 1,417 | 1,136 | 1,159 | 65,659 |
| Implied interactions on N cells, RMS in SE units | 0.36 | 0.36 | 0.37 | 11.8 |
| Capture ratio (implied / actual, held-up cells) | −0.00 | +0.08 | +0.08 | −0.15 |
| Accuracy vs reference, equal in-quarter calibration | — | +0.0002 (0.0025), 10/20 | −0.0019 (0.0026), 12/20 | −0.096 (0.009), 0/20 |
| Accuracy vs reference, reference's prior calibration | — | −0.0039 (0.0050), 7/20 | −0.0055 (0.0041), 10/20 | −43.7 |
| Selected epochs (median) | — | 8 | 8 | 1 |

Accuracy is calibrated points r² on outer broad cells; each entry is the mean
of arm minus reference over the 20 origins, with origin SE and the count of
positive origins.

**By the declared criteria:**
- **pairs** and **pairs_fast** succeed on interactions: χ²_H falls and χ²_N
  does not rise.
- On accuracy they do not establish non-inferiority at −0.003. The SEs are
  0.0025–0.005 because each refit picks different epochs. There is no sign of
  a loss under equal calibration.
- **reward** fails both criteria.

**Measurement caveat (post hoc).** The capture ratio understates what the
pairs arm learned. It measures the arm's interactions after removing a
player-dummy additive fit. Within one quarter, that fit absorbs part of any
interaction between players who usually share the floor. The residual test
(χ²) is the direct one, and the per-effect residuals below agree with it.

## Per held-up effect: residual coefficient (post hoc, descriptive)

Each value is actual minus that arm's forecast. 0 would mean fully learned.

| Event | Combination | Reference | pairs | pairs_fast | SE |
| --- | --- | ---: | ---: | ---: | ---: |
| FTA | small defenders × small defenders | +0.59 | +0.25 | +0.27 | 0.14 |
| FTA | bigs × bigs (defense) | +0.85 | +0.54 | +0.53 | 0.16 |
| FTA | small × passer | +0.44 | +0.30 | +0.32 | 0.09 |
| FTA | small × self-creator | +0.26 | +0.13 | +0.17 | 0.09 |
| FTA | small × small (offense) | +0.57 | +0.42 | +0.45 | 0.14 |
| Rim share | bigs × bigs (defense) | +0.73 | +0.56 | +0.60 | 0.15 |
| Rim share | shot-blocker × defensive rebounder | +0.44 | +0.35 | +0.33 | 0.09 |
| Rim share | big × shot-blocker | +0.34 | +0.28 | +0.26 | 0.10 |
| Three share | big × offensive rebounder | +0.33 | +0.26 | +0.24 | 0.10 |
| Three share | non-shooter × offensive rebounder | +0.58 | +0.51 | +0.47 | 0.10 |
| Three share | offensive rebounders × offensive rebounders | +0.77 | +0.70 | +0.65 | 0.17 |
| Turnovers | shooter × self-creator | −0.14 | −0.13 | −0.13 | 0.04 |
| Turnovers | slasher × high usage | −0.11 | −0.13 | −0.11 | 0.04 |
| Turnovers | non-shooter × offensive rebounder | −0.22 | −0.19 | −0.19 | 0.06 |

The largest leftover cells outside the held-up set also shrink. For example:
- bigs × shot-blockers on FTA: z² 30.7 → 10.6;
- small defenders × shot-blockers on FTA: z² 22.1 → 6.7.

## Pillar 2: fixtures at 2026q4 (native, seed 17)

| Matchup (margin, A − B) | reference | pairs | pairs_fast | reward |
| --- | ---: | ---: | ---: | ---: |
| Legal centers vs Jokić/Westbrook | +5.6 | +8.5 | +4.2 | −3.5 |
| Legal centers vs Jokić/Korver | +4.4 | +6.6 | +3.0 | −132.1 |
| Five Goberts vs Jokić/Westbrook | +11.8 | +18.7 | +16.4 | −4.2 |
| Five Jokićs vs Jokić/Westbrook | +24.7 | +24.0 | +22.8 | −1.7 |

**Five Goberts vs Jokić/Westbrook, split by side** (pairs arm, post hoc):
- **Defense moved the right way.** Jokić/Westbrook score 111.1 → 115.4: rim
  saturation, learned.
- **Offense moved the wrong way.** The Goberts score 122.9 → 134.1:
  - FTA per 100: 33.9 → 48.2;
  - turnovers: 15.5 → 11.7;
  - rim FG%: .704 → .751.

The module learned bigs-together offensive interactions (for example bigs ×
bigs on FTA, z² 31.5 in the reference's residuals) from lineups with two or
three bigs. With five it applies them across ten pairs. Its ±1 bound on each
log-rate still allows FTAs to nearly triple. This is the
selection-on-the-outcome hazard AGENTS.md warns about. The bolted-on layer
avoids it by holding counts at the measured maximum.

## Reading

1. **Rewarding nonlinearity cannot be tuned into something useful.** Below
   the point where the reward beats the likelihood, early stopping erases it.
   Above it, the network makes up interactions wherever there is no data to
   contradict them. χ²_N rose 46× and implied interactions on null cells
   averaged 12 SEs. Whatever the reward adds beyond what the data support is,
   by construction, unsupported.
2. **The network was linear partly by design, not only for lack of signal.**
   With first-order pairwise capacity and no decay on it, the network learns
   real interactions from the same data and the same early stopping. The
   free-throw and rim effects are clearest. Its forecasts become about 75%
   more non-additive (1.1% → 1.9% of variance), close to the size the data
   support.
3. **Learning them in-network is not yet safe off-support.** Before it could
   replace the layer, a learned module would need, declared before fitting:
   - pair contributions held at the measured counts per type, or a bound
     tied to the measured range;
   - three seeds at the release origin and the property suite.
   That would be a next screen, not a change to the tool.

Nothing here changes the tool or the forecast.
