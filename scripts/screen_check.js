// The missing-piece screen against the exact forecast (tool/lineups.html, "Find the missing piece").
//
//   node scripts/screen_check.js EXPORT_DIR [latest|any] [OPPONENT]
//
// OPPONENT: five comma-separated 2025-26 names to search against that five (Team B) instead of the
// league-average opponent.
//
// For each four-player core below and every candidate fifth (2025-26 players, or every player at his default
// season, with at least the band's thin-data possessions), the exact forecast and the screen (one checkpoint
// per seed, ten panel lineups a side). Prints how deep in the screen's ranking the exact top ten reach, and how
// many exact forecasts the page's stop rule uses and whether it finds the exact top ten. One process; a core
// takes about 5 s for 2025-26 players and 20 s for every player.
const fs = require("fs"), path = require("path");
const { create } = require("../tool/lineup_model.js");
const [dir, which = "latest", against] = process.argv.slice(2);
const meta = JSON.parse(fs.readFileSync(path.join(dir, "meta.json"), "utf8"));
const buf = (n) => { const b = fs.readFileSync(path.join(dir, n)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); };
const model = create(meta, buf("weights.bin"), buf("players.bin"));
const P = meta.players, rule = meta.default_rule, byName = {};
P.pid.forEach((p, r) => { if (P.season[r] === meta.latest_season) byName[meta.names[String(p)]] = r; });
const rowOf = new Map(P.pid.map((p, r) => [p * 10000 + P.season[r], r]));
const pool = which === "latest" ? P.season.map((s, r) => r).filter((r) => P.season[r] === meta.latest_season)
  : Object.entries(meta.defaults).map(([p, s]) => rowOf.get(Number(p) * 10000 + s));
const CORES = [
  ["Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren", "Luguentz Dort"],
  ["Nikola Jokić", "Jamal Murray", "Aaron Gordon", "Christian Braun"],
  ["Rudy Gobert", "Walker Kessler", "Clint Capela", "Mitchell Robinson"],
  ["Jalen Brunson", "Karl-Anthony Towns", "OG Anunoby", "Mikal Bridges"],
  ["Luka Dončić", "LeBron James", "Austin Reaves", "Rui Hachimura"],
  ["Jayson Tatum", "Jaylen Brown", "Derrick White", "Kristaps Porziņģis"],
  ["Rudy Gobert", "Julius Randle", "Donte DiVincenzo", "Anthony Edwards"],
  ["Trae Young", "Jalen Brunson", "Darius Garland", "Tyrese Maxey"],
];
const opponent = against ? against.split(",").map((n) => byName[n.trim()]) : null;
if (opponent && opponent.some((r) => r === undefined)) throw new Error("opponent: a name is not a 2025-26 player");
const STOP = { shown: 10, first: 12, most: 64, batch: 8, slack: 0.5 };       // as in tool/lineups.html
for (const names of CORES) {
  if (names.some((n) => !(n in byName))) { console.log("skip:", names.filter((n) => !(n in byName)).join(", "), "not in", meta.latest_season); continue; }
  const core = names.map((n) => byName[n]), taken = new Set(core.map((r) => P.pid[r]));
  const cands = pool.filter((r) => !taken.has(P.pid[r]) && P.offense_possessions[r] >= meta.band.thin_possessions);
  const sc = model.search.screen(core, cands, rule, null, opponent), screen = new Map(cands.map((c, i) => [c, sc[i]]));
  const exact = new Map(cands.map((c) => [c, model.search.forecast([...core, c], rule, opponent).margin]));
  const truth = cands.slice().sort((a, b) => exact.get(b) - exact.get(a)).slice(0, STOP.shown);
  const order = cands.slice().sort((a, b) => screen.get(b) - screen.get(a)), rank = new Map(order.map((r, k) => [r, k + 1]));
  let next = 0; const done = [];
  while (next < order.length && done.length < STOP.most) {
    done.push(...order.slice(next, next + STOP.batch)); next = done.length;
    if (done.length < STOP.first || next >= order.length) continue;
    const tenth = done.map((r) => exact.get(r)).sort((a, b) => b - a)[STOP.shown - 1];
    const gaps = done.map((r) => exact.get(r) - screen.get(r)), mean = gaps.reduce((a, b) => a + b, 0) / gaps.length;
    if (screen.get(order[next]) + mean + Math.max(...gaps.map((g) => Math.abs(g - mean))) + STOP.slack < tenth) break;
  }
  const found = new Set(done);
  console.log(`${names.join(", ")}: ${cands.length} candidates; exact top ten within the screen's top ${Math.max(...truth.map((r) => rank.get(r)))};`
    + ` stop rule: ${done.length} exact, ${truth.filter((r) => !found.has(r)).length} of the top ten missed`);
}
