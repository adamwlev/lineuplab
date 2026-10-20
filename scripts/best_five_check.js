// The best-five search's screen and stop rule against exhaustive exact forecasts (tool/lineups.html, "Find the best five").
//
//   node scripts/best_five_check.js EXPORT_DIR TEAM_SEASONS_JSON
//
// For each team-season below and each opponent (a league-average lineup, or a named five as Team B), every five of
// the roster: the exact forecast (the printed number) and the screen (one checkpoint per seed, ten panel lineups a
// side). Prints how deep in the screen's ranking the exact top ten reach, how many exact forecasts the page's stop
// rule uses, whether it finds the exact top ten, and the time per five. One process.
const fs = require("fs"), path = require("path");
const { create } = require("../tool/lineup_model.js");
const [dir, teamsFile] = process.argv.slice(2);
const meta = JSON.parse(fs.readFileSync(path.join(dir, "meta.json"), "utf8"));
const buf = (n) => { const b = fs.readFileSync(path.join(dir, n)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); };
const model = create(meta, buf("weights.bin"), buf("players.bin"));
const P = meta.players, rule = meta.default_rule;
const rowOf = new Map(P.pid.map((p, r) => [p * 10000 + P.season[r], r]));
const teams = JSON.parse(fs.readFileSync(teamsFile, "utf8")).team_seasons;
const teamRows = (name, season) => { const t = teams.find((x) => x.team === name && x.season === season); return t.roster.map(([p]) => rowOf.get(p * 10000 + season)); };
const combos = (rows) => { const out = []; const n = rows.length;
  for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) for (let c = b + 1; c < n; c++) for (let d = c + 1; d < n; d++) for (let e = d + 1; e < n; e++)
    out.push([rows[a], rows[b], rows[c], rows[d], rows[e]]); return out; };
const CASES = [
  ["Golden State Warriors", 2017, null],
  ["Golden State Warriors", 2017, ["Cleveland Cavaliers", 2017]],
  ["Minnesota Timberwolves", 2026, ["Oklahoma City Thunder", 2026]],
  ["San Antonio Spurs", 2014, ["Miami Heat", 2014]],
  ["Detroit Pistons", 2004, ["Los Angeles Lakers", 2004]],
];
const STOP = { shown: 10, first: 12, most: 64, batch: 8, slack: 0.5 };       // as in tool/lineups.html
for (const [team, season, against] of CASES) {
  const rows = teamRows(team, season), fives = combos(rows);
  let opponent = null;
  if (against) {          // the opponent: its most-used five
    const t = teams.find((x) => x.team === against[0] && x.season === against[1]);
    opponent = t.most_used.five.map((p) => rowOf.get(p * 10000 + against[1]));
  }
  let t0 = Date.now();
  const screen = model.search.screenFives(fives, rule, opponent);
  const tScreen = (Date.now() - t0) / fives.length;
  t0 = Date.now();
  const exact = fives.map((f) => model.search.forecast(f, rule, opponent).margin);
  const tExact = (Date.now() - t0) / fives.length;
  const order = fives.map((_, i) => i).sort((a, b) => screen[b] - screen[a]);
  const top = fives.map((_, i) => i).sort((a, b) => exact[b] - exact[a]).slice(0, STOP.shown);
  const depth = Math.max(...top.map((i) => order.indexOf(i))) + 1;
  // the page's stop rule
  const done = []; let next = 0;
  while (next < order.length && done.length < STOP.most) {
    done.push(...order.slice(next, next + STOP.batch)); next = done.length;
    if (next >= order.length || done.length < STOP.first) continue;
    const tenth = done.map((i) => exact[i]).sort((a, b) => b - a)[STOP.shown - 1];
    const gaps = done.map((i) => exact[i] - screen[i]), mean = gaps.reduce((a, b) => a + b, 0) / gaps.length;
    const spread = Math.max(...gaps.map((g) => Math.abs(g - mean)));
    if (screen[order[next]] + mean + spread + STOP.slack < tenth) break;
  }
  const found = top.every((i) => done.includes(i));
  const names = (i) => fives[i].map((r) => meta.names[String(P.pid[r])].split(" ").slice(-1)[0]).join("-");
  console.log(`${team} ${season} vs ${against ? against.join(" ") : "league average"}: ${rows.length} players, ${fives.length} fives; `
    + `exact top ten within the screen's top ${depth}; stop rule: ${done.length} exact, ${found ? "finds" : "MISSES"} the top ten; `
    + `${tScreen.toFixed(2)} ms a screen, ${tExact.toFixed(2)} ms an exact forecast; best ${names(top[0])} ${exact[top[0]].toFixed(1)}`);
}
