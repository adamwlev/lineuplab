# Persona QA, round 3: "Find the best five" (2026-10-19)

Adam: "since this is a bigger feature, once you're done and before publishing let's do another
iteration of the subagent user testing and then correct things appropriately."

## Method

As in [round 1 and 2](qa_personas_2026_10_18.md), with these differences:
- **The testers.** Five subagents (impatient, skeptic, mobile on slow 3G, non-native English, breaker).
  Each drove one shared headless Chrome (`scripts/qa_browser.mjs`), took turns, and screenshotted
  every moment of confusion.
- **What they tested.**
  - Round A used the first build of the feature (`experiments/cache/qa_2026_10_20/build_before`,
    commit f75dc3ce).
  - Round B used the fixed build (`build_after`, commit 99d3de0a). Each tester re-checked their own
    findings as FIXED, PARTLY or NOT FIXED, and looked for new ones.
  - Both builds are the public site's standalone pages (`build_lineups.py --site`).
- **Where the evidence is.** The findings and screenshots are in
  `experiments/cache/qa_2026_10_20/{before,after}/<persona>/`, saved from the subagents' messages.

## First success, round A

Every tester reached the goal: the best five for a team against an opposing five, loaded into Team A.

| Persona | Time | Note |
| --- | --- | --- |
| Impatient | about 65 s | The first Find did nothing (Team B was a league-average lineup) |
| Skeptic | about 6 min | Partly trusted it; Use broke the numbers' consistency |
| Mobile | about 6 min | About 5 min of it the 20.6 MB download; the search took 1.2 s |
| Non-native | about 8 min | Didn't understand "A − B", "vs most used" or "Combinations, both teams" |
| Breaker | about 3 min | Found stale searches and a TypeError |

## Findings, ranked by how many testers hit them

Letters: I = impatient, S = skeptic, M = mobile, N = non-native, B = breaker.

| # | Finding | Who | Fix |
| ---: | --- | --- | --- |
| 1 | Use gives no visible confirmation; the lineup changes far above | I S N M | "Put in Team A", a bold line "… is now Team A: see the forecast", and the row's button says "In Team A ✓" |
| 2 | The teams are never named: pickers reset, the opponent unnamed, captions stale | I S N M | Pickers name the team whose projected five the slots hold. The opponent is named (team when known, and players). The caption describes the picker. |
| 3 | Use from a league-average search shows a different number (the main result plays Team B's five) | S N | The main result switches Team B to a league-average lineup and says so; "Choose a five" brings Team B's five back |
| 4 | Headers "Net, A − B", "B's offense", "vs most used", "Combinations, both teams", "inside the margin" | N S | Net, Scored, Allowed, Combination effects, vs most-used five, the same in both modes; one plain sentence for the effects |
| 5 | The feature is hard to find | I M | "Searches:" links under the intro |
| 6 | "Best" overclaims: the top ten within a point, ranges about 20 points wide | S | A bold line with the spread and range width; the model page adds that the order often comes down to effects with almost no forward gain |
| 7 | Tables cut off on phones | M | Phones hide Scored, Allowed and Combination effects; the "vs" value sits under the net |
| 8 | The model page unreadable on phones (the contents list drawn over the text) | M | A CSS rule order fix; tables wrap |
| 9 | Find does nothing when Team B has no five | I | Two buttons beside Find: choose a five for Team B, or search against a league-average lineup |
| 10 | A team or season change mid-search finishes as "Done" with live buttons | B | Changes cancel a running search; the old list is hidden or greyed with "Click Find to search again" |
| 11 | Use on the old table during a new Find: a TypeError | B | The old list is off during a search, and Use ignores a vanished row |
| 12 | A Team B with an empty slot is searched as the last complete five | B | Team B counts only when all five slots are complete |
| 13 | League average and back throws away Team B's five | B | Kept and restored |
| 14 | The projected starters' stand-in is not marked; the reference five is untagged in the top ten | S | "projected starters (Middleton in place of the rookie Dybantsa)"; the tag "the projected five" or "the most-used five" |
| 15 | Load progress only in the result card | M | The search sections show the megabytes loaded |
| 16 | Model page text: "13 players make 1,287 fives", a guarantee-like stop rule | S | "Up to 13 … the list names the players"; "a check … not a proof"; the 2026–27 pool stated |
| 17 | Idioms and jargon: opening-night, pit against, stands in, screen, short list, two-way, verdict | N | Plain words throughout |
| 18 | Smaller items | various | "ms" became seconds; no red "+0.0"; the season and team remembered; the footnote hidden during a search; switching the levels back restores a finished list; the static "14" became 12 |

## Re-test, round B

| Persona | Earlier findings: fixed / partly / not fixed | New findings |
| --- | --- | --- |
| Impatient | 5 / 1 / 0 | 6 minor |
| Skeptic | 8 / 0 / 0 | 4 minor; "trust: yes, more than last time" |
| Mobile | 5 / 2 / 0 | 7 minor |
| Non-native | 5 / 3 / 0 | 7 minor |
| Breaker | 7 / 0 / 0 | 1 major (same-surname players identical across rows), 7 minor |

Of the 36 earlier findings re-checked, 30 were fixed and 6 partly; none were not fixed. Every loaded
five reproduced its row's numbers exactly. No tester saw a console error.

## The second fix pass (after round B)

- **Same-surname players** are told apart across the whole table: Jalen, Jaylin and Kenrich
  Williams, and Spencer and Tyus Jones.
- **Team pickers** name a team whenever Team A or B holds its projected five, including on a
  return visit and after "Put in Team A".
- **Put in Team A:** the row's button reads "In Team A ✓". Team A changed some other way clears it.
- **The opponent** names its team ("the Oklahoma City Thunder's projected starters, …").
- **Phone tables:** the "vs" value sits under the net, the name columns are wider, and the jump
  links are bigger targets.
- **Plain words:** the remaining idioms ("screen", "short list", "opening-night", "two-way") and the
  combination-effects sentence, with the tooltip and footnote now agreeing.
- **Smaller fixes:**
  - the blocked-search message is no longer repeated;
  - a cleared block says "find again";
  - a refused quality limit hides the old note;
  - relocated franchises keep their place across seasons (SuperSonics and Thunder);
  - "under 0.1 seconds";
  - "How the search works" stays in the tab.

There was no third tester round. `scripts/page_check.mjs` now has 58 checks, covering each fixed
finding above that a script can see. All pass on the deployed build (version d4e6c106).

## Left open

- **Actual results** for the most-used five: deferred to v2 by Adam.
- **"Why the range is this wide"** doesn't explain the full width against one five (S, N, M); it is
  an existing feature.
- **The page jumps** 40–250 px when status lines appear (I, S).
- **The main result's heading** never names the teams (M).
- **Earlier leftovers:** the 20 MB first download, small badge text, "straight-line estimate",
  "stricter defense view" and long names cut off in the name boxes.
- **Against** is not remembered on a return visit; it follows Team B's mode, by design.
