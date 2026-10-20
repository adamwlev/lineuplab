# Designer review of the tool (2026-10-19)

Adam: "ok i think we should do one more subagent review. this persona should be "the designer". this person
has an eye for layouts, aesthetics and graphics and detests clunkiness and the like."

## Method

- **The tester.** One subagent, a senior product and visual designer, reviewing the built site in a headless
  Chrome (`scripts/qa_browser.mjs`). It covered desktop (1440, 1024 and 820 px) and a phone (390 px), each in
  light and dark, and looked at every screenshot it took.
- **New QA browser commands.** `viewport` and `scheme` change the screen size and the system theme within one
  session.
- **Rounds.**
  - Round 1 used the live build, Worker version 41a4f023, copied to
    `experiments/cache/qa_2026_10_20_designer/build`.
  - The first fix pass is commit ccaa597d.
  - Round 2 re-checked each finding on that build (`build_after`) and looked for new ones.
  - A second fix pass followed. There was no third round.
- **Evidence.** The findings and screenshots are in
  `experiments/cache/qa_2026_10_20_designer/{round1,round2}/designer/`, saved from the subagent's messages.

## Round 1: 19 findings

There were 8 major, 6 minor and 5 polish findings. The designer's first impression: "a serious, well-made tool"
whose trouble "starts as soon as you read anything".

| # | Finding | Fix (first pass) |
| ---: | --- | --- |
| F1 | The measured-combinations table was broken on desktop: rows about 240 px tall, the last column cut off | Its text cells used `class="wrap"`, the page wrapper's class (`display: grid`); renamed |
| F2 | The range graphics were too small, unlabeled, with overlapping markers and a far-off legend | HTML strips with tick labels on one scale per card, the range beside each number, a one-line legend under them |
| F3 | The result was split up: explanations below both searches, stretched empty cards | The explanations moved above the searches; cards no longer stretch |
| F4 | The result card jumped: a red three-line message on top while typing, and a small first card that grew | A fixed two-line message slot (amber dot, plain text); a skeleton at the final height |
| F5 | Walls of text | A two-sentence intro, the levels note behind a disclosure, a short "How the net adds up" equation, one-line search notes with the column key behind "How to read this table", the players footnote once |
| F6 | Phone: the tool below the fold; a wrapping sticky bar with a text link | A shorter header; a two-row sticky bar with a filled button |
| F7 | "Put in Team A" where the names ended (a jagged edge) | The button at the right edge of the names column; a divider on the fixed column on phones |
| F8 | The browser's built-in name suggestions | Deferred: a custom list is a bigger build |
| F9–F14 | Link colours; a cluttered quality line; label styles; mismatched fields and names cut off at 1024 px; clipped focus rings; no hover states | One link style; "Overall quality +1.7 (offense +2.0, allowed +0.3)" with "Details ›" at the right; labels without colons; one field style with a custom chevron; inset focus rings; hover states |
| F15 | The Details dialog | A darker blurred backdrop; full screen on phones with a sticky name and × button; a colour key |
| F16–F19 | Noisy combination cards; label baselines; the model page; "Updated" and duplicated helper text | A quiet "✓ Held up on 2022–26 games" line; a labelled mini chart; the contents mark the current section and fold on phones; the units note replaces "Updated" |

## Round 2: the re-check

| Re-check | Count | Findings |
| --- | ---: | --- |
| Fixed | 10 | F1, F4, F7, F9, F10, F12, F13, F15, F17, F19 |
| Fixed with small leftovers | 2 | F14, F16 |
| Mostly fixed | 3 | F2, F11, F18 |
| Partly | 3 | F3, F5, F6 |
| Not fixed | 0 | |

The designer's verdict: "It looks clearly better ... Most of the earlier findings are fixed properly, not just
patched." There were 14 new findings: 3 major, 5 minor and 6 polish. The second pass:

- **"Why the range is this wide"** moved into the result card, under the equation.
  - Each kind of reason has one badge above its text, with several reasons as a list. Before, there were five
    "unusual lineup" badges, and one badge covered its own text.
  - "More than measured" is a short list ("5 bigs on offense, measured together up to 3").
  - One tinted badge style; no solid fills.
- **A grid with no holes.**
  - On wide screens, a league-average Team B is a slim card above the result, in two columns. With Team B's five
    it is three columns.
  - From 641 to 1199 px, Team A sits beside the result and Team B under Team A.
  - The sticky bar now shows up to 1199 px.
  - The breakdowns run full width in two columns.
- **The header** is top-aligned. The levels note opens as a popover. The two search links are pills named like
  their sections.
- **Numbers and tables.**
  - The equation's numbers line up on the decimal point.
  - The reference five is tagged in the list, and is a separate last row only when it is not among the best.
  - The names column takes the spare width.
  - Phone search controls are one column.
- **Smaller fixes.**
  - Typing shows an "Enter ↵" hint inside the box, so nothing below moves.
  - An emptied box hides the old player's tags.
  - Hover styles apply only where a pointer hovers.
  - The alternative markers sit in a lane under the bar.
  - Crowded tick labels thin to the tens.
  - A larger mini chart.
  - The library intro is in three paragraphs.
  - The model page shares the main page's width and has a continuous contents rule.

**Not changed.**

- *Finding 5, mixed typefaces in the tables.* It was a misreading: every number there is IBM Plex Mono (checked in
  the browser's computed styles).
- *F8, custom name suggestions.* Deferred.
- *Smaller items:* the unbalanced combination columns and the size of the phone search-table rows. On phones the
  table keeps its full width and scrolls, as Adam asked.

## Checks

`scripts/page_check.mjs` now has 71 checks. 11 are new for this review; each covers a fixed finding a script can
see. All pass on the deployed build (Worker version c5828f6b). The new checks were also run on the builds from
before each pass:

- **Before the first pass**, five of its six checks failed. The sixth, the sticky bar, was then tightened to
  require the filled button; that version was not re-run on the old build.
- **Before the second pass**, five of its six checks failed. The sixth, the most-used five listed once, passes on
  both builds: in the test case that five is not in the top ten, so it was never shown twice.

QA browser fixes found along the way: the server cached gzipped files without checking whether they had changed,
so rebuilt pages were served stale, and it served images as downloads.

## Left open

- F8: custom player-name suggestions.
- The phone search tables' tall rows.
- The combination-effects columns can be unequal in length.
- The 20 MB first download.
