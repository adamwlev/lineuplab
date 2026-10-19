# Public NBA tracking and spatial data: availability assessment

Checked 2026-09-08 UTC / September 7 Pacific. Companion to
[MODEL_RESEARCH_ROADMAP.md](../../MODEL_RESEARCH_ROADMAP.md), especially R03–R08/R12.
This is reconnaissance, not a successful ingestion or an experiment result.

## 1. Bottom line and evidence levels

There are useful public-facing **tracking-derived summaries**, shot-location
records, and newly published model-derived metrics. None is equivalent to
having a current, complete, unrestricted feed of all player/ball trajectories.
Do not treat a public webpage, a documented endpoint, a retrieved dataset and
permission to redistribute it as interchangeable.

Evidence levels used here:

- **Published:** official page/announcement exists and was read.
- **Schema:** the `nba_api` maintainers document an endpoint and fields. This is
  primary documentation of that community client, not an official NBA API
  guarantee. Some endpoint examples were last validated in 2020 or 2023.
- **Retrieved:** a current nonempty numerical response was actually obtained
  and checked. **No new tracking dataset reached this level in this session.**
- **Validated:** date filters, coverage, definitions and joins reconcile with
  our data. None of the external candidates has reached this level here.

Public NBA pages loaded through web research, but their extracted text often
showed the interface without numerical rows. No connected interactive browser
was available to verify table filters. Availability of every season, game,
field and API route remains an empirical question.

## 2. Older tracking-derived statistics: useful candidates

General league-wide tracking began in 2013–14. That is an era boundary, **not
proof every field is populated in every game since then**. [NBA rollout announcement](https://pr.nba.com/nba-stats-llc-partnership/)

The following are model-use proposals, not claims of measured predictive gains.

| Family | Published/documented form | What it could help us measure | Important limitation |
|---|---|---|---|
| Passing | Potential assists on the public passing dashboard; `LeagueDashPtStats` has Passing and date filters | Creation opportunities rather than only completed assists | Does not measure every useful pass or independently identify creator impact |
| Touches, drives, role | `LeagueDashPtStats` measures include Possessions, Drives, ElbowTouch, PostTouch and PaintTouch | Primary/secondary handling, penetration, interior role | Player/team summaries, not all-five spatial configurations |
| Catch-and-shoot / pull-up | Same endpoint has CatchShoot and PullUpShot | Off-ball versus on-ball shooting roles | These categories do not fully identify assisted versus self-created attempts |
| Shot context | `PlayerDashPtShots` separates defender proximity, dribbles, touch time and shot-clock contexts | Difficulty proxies beyond distance from the hoop | Separate marginal tables are not a joint event-level dataset |
| Filtered shot-context summaries | `LeagueDashPlayerPtShot` documents distance, defender, clock, touch-time and dribble filters | Potential joint context slices with counts | Filter support and sparse intersections must be tested; no arbitrary teammate-on-floor filter documented |
| Passer-to-receiver summaries | `PlayerDashPtPass` contains teammate IDs, passes, assists and 2P/3P attempts/makes | Diagnostic creator/receiver role and conversion patterns | Pair aggregates are not shot-by-shot locations/defender pressure; avoid known-pair score bonuses |
| Game-level tracking boxes | `BoxScorePlayerTrackV3` has player/team touches, passes, rebound chances, contested/uncontested shooting and defended-rim fields | Dated state updates and coverage reconciliation | A game-wide player row is not an on/off or five-man stint row; potential assists are not in this documented V3 box schema |
| Defensive shooting | `LeagueDashPtDefend` includes attempts/makes attributed to a nearby defender, by distance/category | Rim/perimeter defensive descriptors | Assignment/shot selection/scheme confounding; not a causal defensive coefficient |
| Hustle and box-outs | `LeagueHustleStatsPlayer` includes screens, contests, deflections and box-out/team-rebound outcomes | Screening and Adams-style contributions beyond credited rebounds | Screen assists still depend on completed scores; missing box-out fields must not be treated as zero |
| Offensive-defensive matchup summaries | `LeagueSeasonMatchups` documents matchup minutes, partial possessions and outcomes | Defensive role/assignment diagnostics | Whole-season schema has no date cutoff; unsuitable as an intraseason predictor without a dated alternative |
| Play types | `SynergyPlayTypes` documents play-type frequency and efficiency summaries | Tactical role descriptors, possible scheme context | Coverage/rights/within-season availability unverified; no date-filtered history assumed |

Sources for the table, grouped by the corresponding endpoint families:

- Passing/role categories and date parameters: [LeagueDashPtStats client documentation](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashptstats.md).
  Potential assists count passes followed by a shot within one dribble, including
  misses. [NBA glossary](https://www.nba.com/stats/help/glossary)
- Shot contexts: [PlayerDashPtShots](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playerdashptshots.md)
  and [LeagueDashPlayerPtShot](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashplayerptshot.md).
- Receiver/passer fields: [PlayerDashPtPass](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playerdashptpass.md).
- Per-game fields: [BoxScorePlayerTrackV3](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoreplayertrackv3.md).
- Defensive outcomes: [LeagueDashPtDefend](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashptdefend.md).
- Box-out and hustle fields: [LeagueHustleStatsPlayer](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md).
  In particular, `BOX_OUT_PLAYER_TEAM_REBS` and `BOX_OUT_PLAYER_REBS` distinguish
  team from individual recovery following the credited box-out. This is a
  relevant measurement candidate, not a causal team-rebounding impact estimate.
- Matchups and play types: [LeagueSeasonMatchups](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leagueseasonmatchups.md),
  [SynergyPlayTypes](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/synergyplaytypes.md).

The NBA dates its hustle program to the 2016 postseason; field-specific
start dates, especially box-outs, still need checking rather than assigning
that date to every column. [NBA hustle history](https://www.nba.com/news/history-hustle-award-winners)

## 3. Actual shot coordinates: useful without full tracking

`ShotChartDetail` documents one row per selected shot event, with game/event
IDs, player/team IDs, time, action, distance, shot zones, x/y coordinates and
make/attempt flags. It does **not** include closest-defender distance or passer
identity in that schema. Request attempts, not a made-shot/points-only context.
[ShotChartDetail schema](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/shotchartdetail.md)

For this project, this could replace the misleading distance-only "corner"
proxy and improve R03/R04's location controls. Joining NBA events to our
Basketball Reference-derived records requires validated game/player/event
crosswalks; do not assume the providers share event IDs. Period/clock alone
does not uniquely identify simultaneous events. Coverage before the tracking
era may be broader, but was **not** audited here; do not promise a start year.

## 4. Important new option: Inside the Game

The NBA/AWS rollout announced for 2025–26 includes Gravity, Shot Difficulty and
Defensive Box Score. Gravity describes defensive attention with/without the
ball; Shot Difficulty uses richer spatial/contest information; defensive
statistics use inferred assignments. Play Finder is another announced product,
not a verified downloadable training corpus. [NBA/AWS announcement](https://press.aboutamazon.com/2025/10/nba-and-aws-announce-new-multi-year-partnership-to-power-the-next-era-of-basketball-innovation)

Public destinations inspected:

- [Player Gravity](https://www.nba.com/inside-the-game/player/gravity).
- [Player Shot Difficulty](https://www.nba.com/inside-the-game/player/shot-difficulty).
- [Definitions](https://www.nba.com/news/inside-the-game-stat-glossary).

These are potentially closer to our actual mechanism questions than another
box-score feature. They could be external diagnostic targets or prior player
descriptors, **not automatic point bonuses**. A player's own shot difficulty
still does not identify what he did to his teammates' shots; that requires
teammate outcomes linked to his presence and context.

Unresolved checks before use:

1. Are numerical data available in an authorized reusable form, and at what
   granularity: season, date interval, game, stint or individual attempt?
2. Is there historical backfill? The launch date does not establish either the
   first data season or availability of every older season in the UI.
3. Can a past cutoff be reconstructed without later games or later-trained
   vendor models? A dated shot run through a model trained on future seasons
   is not automatically a historically honest feature.
4. Are model versions, missing-game flags and denominators available? Are
   values revised retrospectively?
5. What does the particular expected-FG field condition on? NBA defines xFG%
   for an average shooter. [NBA definition](https://www.nba.com/news/inside-the-game-stat-glossary)
   AWS's engineering description also mentions shooter skill, so verify the
   exact exported field before separating ability from quality. [AWS engineering account](https://aws.amazon.com/blogs/media/how-the-nba-and-aws-built-an-ai-system-to-measure-what-actually-wins-basketball-games/)
6. What extra information would it add beyond prior profiles and observed
   shot mix? Keep upstream model outputs distinct from directly measured events.

No Inside the Game numerical rows, historical filters, export API or event
joins were verified in this session. It is a promising lead, not available
model input yet. Do not assume it comes from `leaguedashptstats` or that an
`nba_api` endpoint exists merely because the web page exists.

## 5. Full trajectories and other sources

The NBA's Hawk-Eye partnership began in 2023–24 and describes richer tracking
for the league/teams and fan products; it is not a public raw-data license.
[NBA/Hawk-Eye announcement](https://pr.nba.com/nba-sony-hawk-eye-innovations-partnership/)

I did not find an official, current, freely downloadable league-wide trajectory
feed. Historical SportVU movement archives do exist: the
[sealneaward archive](https://github.com/sealneaward/nba-movement-data) describes
itself as a preservation copy after public movement access ended, and
[Rajiv Shah's original analysis](https://github.com/rajshah4/NBA_SportVu/blob/master/EDA_NBA_SportVu.Rmd)
demonstrates a December 2015 game with player/ball movement and event links.
These are potentially useful for a narrow spatial-mechanism prototype, not a
current-season update source. Completeness and underlying data reuse rights
were not established. No archive was downloaded or its scripts executed.

Licensed vendor access, a research partnership, or validated video-derived
tracking are possible longer-term routes if public summaries prove insufficient.
No price, access entitlement or permission is assumed. Video reconstruction
would be a separate substantial project, not a shortcut implicit in this task.

## 6. Existing local fetcher and actual access check

`experiments/fetch_tracking.py` already exists. Read-only inspection found:

- Six `LeagueDashPtStats` measures: Passing, Drives, CatchShoot, PullUpShot,
  Defense, Rebounding; player side only; 2013–14 through 2025–26.
- 78 full-season requests, nominal five-second success spacing, 45-second
  per-request timeout. Failures are retried only by running the script again.
- `DateFrom`/`DateTo` are blank: outputs cannot serve as intraseason priors for
  earlier dates in the same season. They are not 180-day or quarterly states.
- Any existing file larger than 200 bytes is skipped without revalidating the
  rows; new JSON is parsed but an empty valid result could still be cached.
  Writes are not atomic and there is no source/coverage manifest.
- No shot-coordinate, shot-context dashboard, hustle/box-out, per-game tracking
  or Inside the Game collection. The old suggested pair-predictability test is
  not the full current three-pillar acceptance standard.
- `experiments/cache/tracking/` did not exist at inspection. No fetched tracking
  corpus was present at that intended location.

Do not launch it as the next automatic step or rely on its old "six minutes"
estimate as an operational guarantee. The script was left unchanged.

Probe performed this session: one unauthenticated read of its Passing/Player/
2025–26 URL, no custom browser headers, no cookies, no writes; 12-second timeout
and 2 MB read cap. In the sandbox it failed DNS resolution in 0.032 seconds.
A normal approved outside-sandbox attempt then failed with
`ConnectionResetError: [Errno 54] Connection reset by peer` in 0.284 seconds.
There was **no HTTP 429**, no successful JSON and no evidence establishing the
cause of the reset. Do not call this a proven rate limit or assume that running
the same script manually will work. No retries, proxy rotation, authentication
changes or access-control bypass were attempted.

## 7. Public access is not an open-data license

NBA's FAQ restricts downloading even for personal or academic use.
[NBA FAQ](https://www.nba.com/stats/help/faq)

Treat acquisition, persistence, model-training and redistribution permissions
as unresolved before bulk ingestion or a public deployment. A community client
license does not confer rights to the source data. Verify an authorized route
and applicable terms; if necessary seek permission or licensed data. No legal
conclusion about this project's intended use is made here, and no paid service,
account creation or contact with a provider was authorized/performed.

## 8. Proposed small pilot, conditional on an authorized access route

Do not build a large scraper before this question has an answer. One bounded
data pilot should deliver a manifest and an actual usability decision:

1. Check the authorization route and a small current/older numerical response.
   Stop on access denial; do not turn it into an unbounded retry exercise.
2. Prioritize passing/role counts, one shot-context source, and hustle/box-outs;
   separately establish whether new xFG%/Gravity can be obtained at useful dates.
3. Test an early prefix versus later prefix for the same season. Determine
   whether date endpoints are inclusive and whether filtering really changes
   counts as expected. Use cutoff-minus-one-day for inclusive date APIs.
4. Reconcile IDs, game dates, minutes/exposure, raw numerators/denominators and
   missing rows on a small fixed sample. Keep missing tracking distinct from
   zero activity. Audit field-by-field history, not just requested season labels.
5. Preserve regular season/playoff distinctions, time zones, API version,
   retrieval time, parameters, raw-response hash and revisions. Cache only valid
   responses atomically. Do not change existing possession caches/database.
6. Define an analysis population shared by all candidate/control arms; print
   total covered possessions and a historical/no-tracking fallback plan.

Success is an accessible, permitted, dated and joinable feature set that answers
a specific mechanism question. Failure is also useful: it routes us back to
the existing-data workload/shot-mix experiment without another stalled scrape.
No new model run is required to finish this pilot, and no pilot was run here
beyond the bounded availability probe described above.
