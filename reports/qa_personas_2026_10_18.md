# First-time-user QA with five personas (2026-10-18)

Adam: "Act as my launch QA lead. Spin up 5 subagents, each a different first-time
user … Merge everything into one list ranked by how many users hit it. Fix it all in
one pass, then rerun the 5 users to prove it's fixed."

## Method

- **The personas.** Five subagents, each a first-time user given only "a friend sent you
  a link to Lineup Lab":
  - **Impatient:** skims, clicks the obvious thing, quits at the first error; up to three visits.
  - **Skeptic:** reads the fine print. The tool has no pricing, sign-up or terms, so this
    meant authorship, data, privacy, accuracy claims and limits.
  - **Mobile:** 375 px phone, slow 3G, CPU slowed 4x.
  - **Non-native English speaker:** follows only what the screen literally says.
  - **Breaker:** junk input, clones, back and forward mid-flow, double-clicks.
- **How they tested.** Each drove a real (headless) Chrome through
  `scripts/qa_browser.mjs` and screenshotted every moment of confusion. One browser ran at a
  time, because the refresh was holding two cores; each page used two threads.
- **What they tested.** Round 1 used a frozen copy of review copy v9
  (`experiments/cache/qa_2026_10_18/build_before`), served locally with gzip. Round 2 used
  the fixed page (`build_after`, commit 89378b95). Neither round can reproduce the claude.ai
  frame around the artifact.
- **Where the evidence is.** Findings and screenshots are in
  `experiments/cache/qa_2026_10_18/{before,after}/<persona>/`. The subagents could not
  write files, so I saved each report from its message.

## First success, round 1

| Persona | Result | Time |
| --- | --- | --- |
| Impatient | yes, on the second visit | 28 s to a number with one player of their choice; 2 min 20 s for a full five of their own |
| Skeptic | **no** | Got a plausible +10.8 for the 2016–17 Hamptons Five but didn't trust it |
| Mobile | yes | 6 min 56 s, about 5 of them loading with no progress shown |
| Non-native | yes | about 2 min, mostly working out Enter and exact accents |
| Breaker | yes | about 27 s; no crashes, no script injection, no console errors |

## Findings, ranked by how many personas hit them

The persona letters: I = impatient, S = skeptic, M = mobile, N = non-native, B = breaker.

| # | Finding | Who | Fix (commit 89378b95) |
| ---: | --- | --- | --- |
| 1 | Names silently rejected over case, spacing or accents ("Nikola Jokic", "rudy gobert", "Porzingis") | I N B M | Case, spacing and accents no longer matter. A fragment that fits one player takes that player. Otherwise the slot asks "Which one?" with buttons, or says "No player matches". |
| 2 | The old forecast stays at full strength while a slot is empty, unknown or half-typed | I N B M | The result, combinations and breakdowns grey out, and the status names the slot and the reason. A half-typed name shows as pending. |
| 3 | Opening "The forecast under each assumption" pushes the card's content under its neighbour, or widens the phone page | N S M | Card grid columns can shrink, so the table scrolls inside its card. Checked at 375 px. |
| 4 | After "Use", the "now" row is stale and nothing nearby confirms the change; Use works on a stale list | I B M | The list greys and says "X is in spot 5 now: see the forecast". Use is off on a stale list. |
| 5 | The offense breakdown is labelled "against a league-average offense" | N S M | Now "compared with a league-average offense". |
| 6 | The five quality numbers don't add up to the "add up to" total; the offset is hidden | I S | The sentence starts from five typical players (net −4.1, because "league average" is the average lineup that played 100+ possessions) and adds the shown numbers, so the arithmetic is exact on screen. |
| 7 | "How these five combine" (−13.0) vs "combination effects" (+0.36): two things with one name | N S | Now three numbers that add up: the straight-line estimate, the full model before combination effects, and the combination effects. "Combine" names one thing. |
| 8 | "Pick five" loads the 2016–17 Warriors without saying so | I N | Renamed "Choose a five", with a hint that it starts as the 2016–17 Warriors and that any name can be typed over. Team A has a hint too. |
| 9 | Breakdown total ≠ the offense number at the top | N S | Labelled "Total, before combinations". |
| 10 | Jargon: Assumption C/K/N, era backtest, distance/max, held up, same sign, reverses, pp, screened, 3PA, FGA, USAGE | N S | Reasons are in plain words, with the model's wording as the tooltip. Badges, units and headers are spelled out. |
| 11 | The training window is described four ways; season notation is mixed | N S | One statement (2021–22 to 2025–26) everywhere. Seasons are written 2016–17. |
| 12 | Details sheet: a stray "." and a link one word wide | N B | The footnote no longer uses the two-column grid style. |
| 13 | One search reports two different times | B M | One time, in the status. |
| 14 | Five Goberts shows a green +4.2 with no warning nearby; "unusual" flags unexplained | I S | An "Unusual lineup" note sits beside the number (no ball handler, no outside shooter, the same player more than once …). The number itself is the model's and is unchanged. |
| 15 | The player-levels switch is unexplained | N S | A line under the switch. The 7-point swing is a model question (below). |
| 16 | Long names cut off in the boxes | N M | Narrower season box on phones, and 16 px fields. |
| 17 | Combination lines: numbers without units, "adding up implies 4.7" | N S | Units in words; "the model already expects 4.7 from the players alone, so only the difference counts". |
| 18 | "Held up" on the model page vs "2007–13 reverses" on the cards | S N | The model page gives the re-check per effect: nine held up, three pointed the same way more weakly, two pointed the other way. |
| 19 | **Blocker:** about 5 minutes of blank boxes and "Loading the model (15 MB)" on slow 3G | M | The player list loads first, so the boxes are usable in seconds, and the status counts megabytes. The payload is still about 20 MB (below). |
| 20 | Missing-piece table on a phone: Use and most columns off the right edge, no cue | M | Use sits beside each name; the rank and name stay put; edge shadows show the table scrolls; a new search starts at the left. |
| 21 | On a phone the forecast is about 1,550 px below the inputs | M | The result follows Team A, and a summary bar is pinned to the bottom of the screen. |
| 22 | Breakdown chart labels at about 7 px on a phone | M | HTML bars instead of a shrinking SVG. |
| 23 | Tables cut off with no swipe cue | M | Edge shadows on every sideways-scrolling table. |
| 24 | Small tap targets | M | 40 px controls on touch screens and narrow widths. |
| 25 | The 14-combination table falls apart on a phone | M | It stacks into one card per combination. |
| 26 | Badges stretch into tall blocks | M | Aligned to the top. |
| 27 | No author, contact, date or privacy statement | S | Data source, date and privacy are on the main page and in "About this site". **Author and contact are Adam's call.** |
| 28 | The accuracy table puts a level under "Change in r²"; no comparison; the shipped model isn't scored | S | r² is explained, with its comparison (0.1615 vs the replaced release's 0.1630). Re-scored numbers are pending the refresh. |
| 29 | The range's coverage is never reported | S | The model page explains why a long-run level can't be checked by counting hits, and where the width comes from. |
| 30 | Real lineups never show what they actually did | S | **Not done:** needs lineup outcomes in the export (a feature). |
| 31 | The cross-era figure differs (85% vs 88%/84%) | S | 88% (relative) / 84% (as played) everywhere. |
| 32 | The model page's Contents skips the missing piece | S | Added. |
| 33 | NET vs MARGIN for the same quantity | N | "Net" everywhere, with "Net, A − B" against Team B. |
| 34 | "pts" means percentage points in the Details sheet | N | "pp", with a one-line key. |
| 35 | The preset row has no label; "Heat 2013" vs "2012–13" | N | "Examples:" and season-style names. |
| 36 | Tag abbreviations (Off./Def. rebounder) | N | Spelled out, with a tooltip. |
| 37 | The "Creation" sentence can't be interpreted | N | "Passing: … about 25 …: enough / not enough". |
| 38 | Double-clicking a preset loads a different preset | B | The second click of a double-click is ignored. |
| 39 | A cleared box keeps the old player's tags and Details | B | The row clears. |
| 40 | Against Team B: "choose Pick five" although it is chosen | B | Separate messages for an incomplete Team B and League average. |
| 41 | "Fill Team A's other four spots first" stays after the team is fixed | B | Cleared on the next team change. |
| 42 | The same player-season on both teams, with no note | B | A note in the result. |
| 43 | Back or reload loses the lineup | B | This browser remembers the last lineup (localStorage). A share link isn't possible inside an artifact. |
| 44 | Escape doesn't undo a half-typed name | B | Escape brings back the last player. |
| 45 | The quality cap accepts 1e308 | B | Limited to −30 to +30. |
| 46 | Junk names appear in the Replace dropdown | B | Only real players; otherwise "(empty)". |
| 47 | "+0.0" in green | B | Neutral colour. |

## Not fixed, and why

- **Load size (mobile blocker, partly fixed).** The page is now usable during the
  download, but the first forecast still needs about 20 MB, roughly 5 minutes on slow 3G.
  Shrinking it (for example float16 weights) changes the model's numbers, so it needs a
  protocol.
- **Actual results for real lineups (skeptic).** Needs lineup outcomes in the export,
  with their own noise shown. This is a feature to decide on.
- **Author and contact (skeptic).** Adam's decision.
- **Accuracy of the shipped model (skeptic).** The refresh re-scores it; the model page
  gets the numbers when it lands.
- **The "relative" setting gives the 2016–17 Warriors 61–69% of their shots from three,
  and the net moves about 7 points between settings (skeptic).** This is the model's
  cross-era translation, not the page. It needs investigation (v2 research). The default is
  Adam's decision of 2026-10-12.

## Round 2 (build_after, commit 89378b95)

Each persona re-checked every one of their own round-1 findings, then walked the journey
again. Round 2 had no console errors and no crashes.

| Persona | Fixed | Partly | Not fixed | New | First success, round 1 → 2 |
| --- | ---: | ---: | ---: | ---: | --- |
| Impatient | 5 | 1 | 0 | 1 | two visits, 2 min 20 s → one visit, 28 s |
| Skeptic | 10 | 4 | 2 | 4 | no → yes for an in-range lineup (not the cross-era famous five) |
| Mobile | 8 | 6 | 0 | 2 | 6 min 56 s → 4 min 51 s; player boxes usable at 0:49, not about 5 min |
| Non-native | 11 | 8 | 0 | 5 | about 2 min → 1 min 20 s |
| Breaker | 11 | 4 | 0 | 6 | 27 s → 7 s, with lower-case, unaccented names |
| **All** | **45** | **23** | **2** | **18** | |

**What "partly" mostly meant:**
- **Five Goberts:** the number is still a big green +4.2. The note beside it explains it, but the colour is unchanged.
- **Tables:** some were still cut at the right edge, the breakdown's player table at 1280 px and the missing piece's columns on phones.
- **Season boxes:** narrowing them for phones cut the last digit ("2015–1"), a regression of mine.
- **Leftover wording:** the gap between the straight line and the model; "learned from 2021–22 to 2025–26" reading as not knowing older players; tag tooltips that say nothing specific; "Beyond measured"; double full stops after numbers.
- **Reload:** with an unfinished box it went back to the default lineup.

**Second pass (commit 64df50b0), from the round-2 reports:**
- **Reload** brings back the last *complete* lineup.
- **Names:** "Which one?" lists the most-played first ("james" now offers LeBron James first). A typo or two gets "Did you mean" ("Doncicc" offers Luka Dončić).
- **Season boxes** size to their content again.
- **Tables:** they fit at 1280 px. On phones, the missing piece's range sits under the net and the name column has a fixed width.
- **Disabled controls:** stale "Use" buttons and an unfinished row's Details look and act disabled.
- **Wording:**
  - the straight-line gap explained in plain words;
  - "league average" is better than most fives, because coaches keep good lineups on the floor;
  - older players come in through their own seasons' numbers;
  - the player-level switch can move older lineups by several points;
  - each tag says what it measures;
  - the unusual-lineup note names the seasons;
  - one full stop after numbers.

`scripts/page_check.mjs` now runs 34 checks, including each of these, and all pass. I also
checked the phone layout by screenshot. The second pass has **not** been through a third
persona round.

**Still open:**
- **Your decisions:** the five Goberts colour, author and contact, showing actual results for
  real lineups, the "relative" setting's cross-era translation (61–69% threes, about a 7-point
  swing), and the 20 MB download.
- **Waiting on the refresh:** the shipped model's accuracy and baseline on the model page.
- **Not testable headless:** browsers' own suggestion lists match accents exactly, so "jokic"
  shows no suggestion until Enter.
- **Not possible inside an artifact:** a share link.

The review copy was updated to this page as version 10 (clean release; the refresh not yet
switched in).
