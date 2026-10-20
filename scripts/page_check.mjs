// Drive a built Lineup Lab page in headless Chrome: the missing-piece search and its overall-quality limit.
//
//   node scripts/page_check.mjs BUILD_DIR [PAGE]   (BUILD_DIR from tool/build_lineups.py, e.g. its --out directory;
//                                                 PAGE lineups.html, or index.html for a --site build)
//
// Serves BUILD_DIR on localhost, opens lineups.html with navigator.hardwareConcurrency set to 3 (the model's
// worker and one helper: two threads), and checks, against meta.json's values:
//   - the limit starts off, at the replaced player's overall quality, and follows the slot and the rule;
//   - with the limit on, every listed candidate is at or under it, and the note says how many were left out;
//   - a typed limit is used as typed; an impossible or empty one is refused with a message;
//   - the replaced player-season is listed once, as the "now" row;
//   - against Team B the combinations column says it holds both teams' effects;
//   - at 400 px wide nothing scrolls sideways (SHOT=file.png saves a picture of the search there), and at 375 px both
//     search tables keep all their columns, scrolling inside their own boxes;
//   - names resolve forgivingly or explain themselves, the result greys out while a slot is unfinished, Escape brings
//     back the last player, and a reload keeps the lineup;
//   - the designer's review (2026-10-19): the result's message line, numbers that hold still while a name is typed,
//     aligned search buttons, the measured-combinations table, the phone summary bar and the model page's contents.
// Prints each search's time. Exits 1 if any check failed.
import { spawn } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";

const DIR = path.resolve(process.argv[2] || ".");
const PAGE = process.argv[3] || "lineups.html";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const meta = JSON.parse(readFileSync(path.join(DIR, "meta.json"), "utf8"));
const quality = (rule, r) => meta.values.rules[rule].offense[r] - meta.values.rules[rule].defense[r];
const TYPES = { ".html": "text/html", ".json": "application/json", ".txt": "text/plain" };

const server = http.createServer((req, res) => {
  const file = path.join(DIR, decodeURIComponent(new URL(req.url, "http://x").pathname));
  try { const body = readFileSync(file); res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "application/octet-stream" }); res.end(body); }
  catch { res.writeHead(404); res.end(); }
});
await new Promise((ok) => server.listen(0, "127.0.0.1", ok));
const site = `http://127.0.0.1:${server.address().port}`;

const profile = mkdtempSync(path.join(tmpdir(), "page-check-"));
const chrome = spawn(CHROME, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`, "--no-first-run", "about:blank"],
                     { stdio: ["ignore", "ignore", "pipe"] });
const browserUrl = await new Promise((ok, fail) => {
  let err = "";
  chrome.stderr.on("data", (d) => { err += d; const m = err.match(/DevTools listening on (ws:\/\/\S+)/); if (m) ok(m[1]); });
  setTimeout(() => fail(new Error("Chrome did not start")), 20000);
});
const port = new URL(browserUrl).port;
const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" })).json();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((ok) => ws.addEventListener("open", ok));
let id = 0;
const pending = new Map(), errors = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === "Runtime.exceptionThrown") errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
});
const send = (method, params = {}) => new Promise((ok) => { const k = ++id; pending.set(k, ok); ws.send(JSON.stringify({ id: k, method, params })); });
const ev = async (expression) => {
  const m = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (m.result.exceptionDetails) throw new Error(`${expression.slice(0, 80)}: ${m.result.exceptionDetails.exception?.description}`);
  return m.result.result.value;
};
const waitFor = async (expression, ms = 60000) => {
  for (const t0 = Date.now(); Date.now() - t0 < ms;) { if (await ev(expression)) return; await new Promise((ok) => setTimeout(ok, 50)); }
  throw new Error(`timed out waiting for ${expression}`);
};
let failed = 0;
const check = (ok, what) => { console.log(`${ok ? "ok  " : "FAIL"} ${what}`); if (!ok) failed++; };
const finish = async () => {
  ws.close(); server.close();
  await new Promise((ok) => { chrome.once("exit", ok); chrome.kill(); });
  rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
  process.exit(failed ? 1 : 0);
};

try {
  await send("Runtime.enable");
  await send("Emulation.setHardwareConcurrencyOverride", { hardwareConcurrency: 3 });
  await send("Page.navigate", { url: `${site}/${PAGE}` });
  await waitFor(`document.getElementById("piece-go") && !document.getElementById("piece-go").disabled`);
  await waitFor(`!document.getElementById("status").classList.contains("busy")`);
  await new Promise((ok) => setTimeout(ok, 1500));            // the helper's warm-up

  const $ = (x) => `document.getElementById(${JSON.stringify(x)})`;
  const set = (x, value, event) => ev(`(() => { const e = ${$(x)}; e.value = ${JSON.stringify(value)}; e.dispatchEvent(new Event(${JSON.stringify(event)})); })()`);
  const shown = (slot) => ev(`Number(${$(`pvalue-a-${slot}`)}.querySelector("strong").textContent.replace("−", "-"))`);
  // 2026–27 teams (scripts/rosters_2026_27.py): a fresh browser opens on the default team's projected five
  const rosters = JSON.parse(readFileSync(new URL("../tool/rosters_2026_27.json", import.meta.url), "utf8"));
  const fiveOf = (team) => rosters.teams.find((t) => t.team === team).five;
  const lineup = (side) => ev(`[0, 1, 2, 3, 4].map((i) => [document.getElementById("name-${side}-" + i).value, Number(document.getElementById("season-${side}-" + i).value)])`);
  const same = (got, team) => JSON.stringify(got) === JSON.stringify(fiveOf(team).map((x) => [meta.names[String(x.pid)], x.season]));
  const opened = await lineup("a");
  check(same(opened, "Minnesota Timberwolves"), `a fresh browser opens on the Timberwolves' projected 2026–27 five, each at his latest season (${opened.map((x) => x[0]).join(", ")})`);
  const units = await ev(`${$("status")}.textContent`);
  check(/^Points per 100 possessions/.test(units), `after a forecast the result's message line explains the units ("${units.slice(0, 40)}…"), not "Updated" (designer QA 2026-10-19)`);
  const cap = () => ev(`({ value: ${$("piece-cap")}.value, disabled: ${$("piece-cap")}.disabled, on: ${$("piece-cap-on")}.value })`);
  const find = async () => {
    const t0 = Date.now();
    await ev(`${$("piece-go")}.click()`);
    await waitFor(`/^(Done in|No candidates|Enter |Fill)/.test(${$("piece-status")}.textContent)`);
    return { ms: Date.now() - t0, ...(await ev(`({ status: ${$("piece-status")}.textContent, note: ${$("piece-note")}.textContent,
      rows: [...${$("piece-table")}.querySelectorAll("tbody tr:not(.now) .use")].map((b) => Number(b.dataset.row)),
      who: [...${$("piece-table")}.querySelectorAll("tbody tr:not(.now) td.who")].map((t) => t.textContent.replace(/Use$/, "").trim()),
      now: ${$("piece-table")}.querySelector("tbody tr.now td.who")?.textContent.replace(/ · current$/, "").trim(),
      head: [...${$("piece-table")}.querySelectorAll("thead th")].map((t) => t.textContent.trim()) })`)) };
  };
  const names = (rows) => rows.map((r) => `${meta.names[String(meta.players.pid[r])]} ${quality("relative", r).toFixed(1)}`).join(", ");

  let c = await cap(), q5 = await shown(4);
  check(c.on === "most" && !c.disabled, `the limit starts on, "At most" (${JSON.stringify(c)})`);   // Adam, 2026-10-19
  check(Math.abs(Number(c.value) - q5) < 0.051, `it starts at slot 5's overall quality (${c.value} vs ${q5})`);

  let r = await find();
  console.log(`  at most ${c.value}: ${r.status}; ${names(r.rows)}`);
  check(r.rows.length > 0 && r.rows.every((x) => quality("relative", x) <= q5 + 0.051), "every listed candidate is at or under the limit");
  check(/with overall quality [+−]\d+\.\d or lower/.test(r.note) && /above that quality left out/.test(r.note), `the note says so: "${r.note.slice(0, 160)}…"`);

  await set("piece-cap-on", "any", "change");
  c = await cap();
  check(c.disabled, "choosing Any turns the number off");
  r = await find();
  console.log(`  any: ${r.status}; ${r.rows.length} listed: ${names(r.rows)}`);
  check(r.head.includes("Combination effects") && r.head.includes("Scored") && /play differently together\./.test(r.note), "against a league-average lineup the columns are in plain words (Net, Scored, Allowed, Combination effects)");
  const best = Math.max(...r.rows.map((x) => quality("relative", x)));
  console.log(`  without the limit the best listed quality was ${best.toFixed(1)}; the limit was ${c.value}`);
  await set("piece-cap-on", "most", "change");
  check(!(await cap()).disabled, "choosing At most again enables the number");

  await set("piece-cap", "0", "input");
  r = await find();
  check(r.rows.length > 0 && r.rows.every((x) => quality("relative", x) <= 1e-9), `a typed limit of 0 is used as typed (${r.rows.length} listed, ${r.status})`);

  await set("piece-cap", "-99", "input");
  r = await find();
  check(/^Enter an overall quality between/.test(r.status), `a limit out of range is refused: "${r.status}"`);
  await set("piece-cap", "-25", "input");
  r = await find();
  check(/^No candidates/.test(r.status), `a limit no player meets says so: "${r.status}"`);
  await set("piece-cap", "", "input");
  r = await find();
  check(/^Enter the/.test(r.status), `an empty limit is refused: "${r.status}"`);

  await set("piece-slot", "0", "change");
  c = await cap();
  const q1 = await shown(0);
  check(Math.abs(Number(c.value) - q1) < 0.051, `changing the slot resets the limit to that player (${c.value} vs ${q1})`);
  r = await find();
  check(r.rows.every((x) => quality("relative", x) <= q1 + 0.051), `slot 1 at most ${c.value}: ${r.status}`);
  check(r.now && !r.who.includes(r.now), `the replaced player-season (${r.now}) is the "now" row, not a candidate`);

  await ev(`${$("rule-as-was")}.click()`);
  await waitFor(`!${$("status")}.classList.contains("busy")`);
  c = await cap();
  const qa = await shown(0);
  check(Math.abs(Number(c.value) - qa) < 0.051, `switching to As they played resets the limit to that rule's quality (${c.value} vs ${qa})`);
  r = await find();
  check(r.rows.every((x) => quality("as_was", x) <= qa + 0.051), `as played, at most ${c.value}: ${r.status}`);

  await set("piece-cap-on", "any", "change");
  r = await find();
  check(!/with overall quality/.test(r.note), `Any again: no limit in the note (${r.status})`);
  await ev(`${$("b-mode-five")}.click()`);                    // Team B: the 2017 Warriors (the page's first five)
  await waitFor(`!${$("status")}.classList.contains("busy")`);
  await set("piece-slot", "4", "change");
  check(await ev(`${$("piece-against")}.value === "b"`), "picking Team B's five switches the search to it");
  r = await find();
  check(r.head.includes("Combination effects") && /minus the effects for Team B's five/.test(r.note) && /for comparing the rows/.test(r.note),
        `against Team B the note says the combination effects are both teams' and are for comparing rows (${r.status})`);

  await set("piece-cap-on", "most", "change");
  await send("Emulation.setDeviceMetricsOverride", { width: 400, height: 900, deviceScaleFactor: 2, mobile: true });
  await new Promise((ok) => setTimeout(ok, 500));
  const fit = await ev(`({ page: document.documentElement.scrollWidth, cap: Math.round(${$("piece-cap")}.getBoundingClientRect().right) })`);
  check(fit.page <= 400 && fit.cap <= 400 - 16, `at 400 px nothing scrolls sideways and the limit fits inside the gutter (${JSON.stringify(fit)})`);
  if (process.env.SHOT) {                                    // a phone-width picture of the search
    const box = await ev(`(() => { const r = ${$("piece")}.getBoundingClientRect(); return { x: 0, y: r.top + scrollY, width: 400, height: Math.min(r.height, 900), scale: 1 }; })()`);
    const shot = await send("Page.captureScreenshot", { format: "png", clip: box, captureBeyondViewport: true });
    (await import("node:fs")).writeFileSync(process.env.SHOT, Buffer.from(shot.result.data, "base64"));
  }
  // names, stale results, Escape and reload (first-time-user QA, 2026-10-18)
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await ev(`${$("b-mode-average")}.click()`);
  await ev(`${$("rule-relative")}.click()`);
  const quiet = () => waitFor(`!${$("status")}.classList.contains("busy")`);
  const name = async (slot, text, how = "change") => {
    await ev(`(() => { const e = ${$(`name-a-${slot}`)}; e.focus(); e.value = ${JSON.stringify(text)};
      e.dispatchEvent(new Event("input", { bubbles: true })); ${how === "change" ? `e.dispatchEvent(new Event("change", { bubbles: true }));` : ""} })()`);
    await quiet();
    return ev(`({ value: ${$(`name-a-${slot}`)}.value, msg: ${$(`msg-a-${slot}`)}.textContent, stale: ${$("result")}.classList.contains("is-stale"),
      status: ${$("status")}.textContent, warn: ${$("status")}.classList.contains("warn") })`);
  };
  let n = await name(0, "nikola jokic");
  check(n.value === "Nikola Jokić" && !n.stale && !n.warn, `"nikola jokic" becomes ${n.value}`);
  n = await name(1, "  porzingis ");
  check(n.value === "Kristaps Porziņģis" && !n.stale, `"porzingis" becomes ${n.value}`);
  n = await name(2, "Curry");
  check(/Which one\?/.test(n.msg) && n.stale && n.warn && /pick which/.test(n.status), `"Curry" asks which one, greys the result and says so: "${n.status.slice(0, 90)}"`);
  await ev(`document.querySelector("#msg-a-2 button.pick").click()`);
  await quiet();
  n = await name(2, await ev(`${$("name-a-2")}.value`));
  check(/Curry/.test(n.value) && !n.stale && !n.warn, `picking a suggestion fills the slot: ${n.value}`);
  const before3 = await ev(`${$("name-a-3")}.value`);
  n = await name(3, "<img src=x onerror=alert(1)>");
  check(/No player matches/.test(n.msg) && n.stale && n.warn, `junk is refused with a message: "${n.msg.slice(0, 60)}"`);
  await ev(`${$("name-a-3")}.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }))`);
  await quiet();
  n = await name(3, await ev(`${$("name-a-3")}.value`));
  check(n.value === before3 && !n.stale, `Escape brings back the last player: ${n.value}`);
  const offset = () => ev(`[${$("metrics")}.getBoundingClientRect().top - ${$("result")}.getBoundingClientRect().top,
    document.querySelector("#team-a > .presets:not(.team-row)").getBoundingClientRect().top - ${$("team-a")}.getBoundingClientRect().top].map(Math.round).join()`);
  const before4 = await offset();
  n = await name(4, "Steph", "input");
  check(n.stale && /press Enter/.test(n.status) && await ev(`${$("slot-a-4")}.classList.contains("pending")`), "a half-typed name greys the result until it is finished");
  const after4 = await offset();
  check(after4 === before4, `typing it moves neither the numbers nor the rows under the box (${before4} px, then ${after4}; designer QA 2026-10-19)`);
  await ev(`${$("name-a-4")}.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }))`);
  await quiet();
  const before = await ev(`[0, 1, 2, 3, 4].map((i) => document.getElementById("name-a-" + i).value).join(", ")`);
  await send("Page.reload");
  await waitFor(`document.getElementById("piece-go") && !document.getElementById("piece-go").disabled`);
  await quiet();
  const after = await ev(`[0, 1, 2, 3, 4].map((i) => document.getElementById("name-a-" + i).value).join(", ")`);
  check(after === before, `a reload keeps the lineup (${after})`);
  // round 2 (QA, 2026-10-18): a reload with an unfinished box brings back the last complete lineup
  await name(1, "qqq");
  await send("Page.reload");
  await waitFor(`document.getElementById("piece-go") && !document.getElementById("piece-go").disabled`);
  await quiet();
  const again = await ev(`[0, 1, 2, 3, 4].map((i) => document.getElementById("name-a-" + i).value).join(", ")`);
  check(again === before, `a reload with an unknown name brings back the last complete lineup (${again})`);
  n = await name(1, "james");
  check(/^Which one\? LeBron James/.test(n.msg), `"james" lists the most-played first: "${n.msg.slice(0, 40)}"`);
  n = await name(1, "Doncicc");
  check(/Did you mean Luka Dončić/.test(n.msg), `a typo offers a near name: "${n.msg.slice(0, 60)}"`);
  await ev(`${$("name-a-1")}.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }))`);
  await quiet();
  await ev(`[...document.querySelectorAll(".preset")].find((b) => b.textContent === "Five Goberts").click()`);
  await quiet();
  const chips = await ev(`[...document.querySelectorAll("#result #reasons > li > .chip")].map((c) => c.textContent)`);
  check(chips.length >= 3 && chips.length === new Set(chips).size && chips.includes("unusual lineup"),
        `five Goberts: the reasons sit in the result card, one badge per kind (${chips.join(", ")}; designer QA 2026-10-19)`);
  const text = await ev(`document.body.innerText`);
  check(!/\d\.\.(\s|$)/.test(text), "no double full stops after numbers");
  await ev(`document.querySelector("details.assume").open = true`);
  const fits = await ev(`[...document.querySelectorAll("#below .scroll")].map((s) => s.scrollWidth - s.clientWidth)`);
  check(fits.every((x) => x <= 1), `the range and breakdown tables fit at 1280 px (overflow ${JSON.stringify(fits)})`);
  const teams = await ev(`[...${$("pick-team-a")}.options].map((o) => o.value).filter(Boolean)`);
  check(teams.length === 30, `the 2026–27 team picker lists ${teams.length} teams`);
  await set("pick-team-a", "Los Angeles Lakers", "change");
  await quiet();
  const lakers = await lineup("a");
  check(same(lakers, "Los Angeles Lakers") && await ev(`${$("pick-team-a")}.value`) === "Los Angeles Lakers", `picking the Lakers loads their projected five, and the picker names them (${lakers.map((x) => x[0]).join(", ")})`);
  await set("name-a-0", "LeBron James", "change");
  await quiet();
  check(await ev(`${$("pick-team-a")}.value`) === "", "changing a player clears the picker's team");
  await set("pick-team-a", "Golden State Warriors", "change");
  await quiet();
  const gsw = fiveOf("Golden State Warriors"), k = gsw.findIndex((x) => x.stands_in_for);
  const standIn = await ev(`${$(`msg-a-${k}`)}.textContent`);
  check(k >= 0 && same(await lineup("a"), "Golden State Warriors") && standIn.includes(`In place of ${gsw[k].stands_in_for}`),
        `a rookie starter's stand-in says so: "${standIn}"`);
  // the candidates start at the season of the player being replaced (2016–17 Warriors: 2016–17 players)
  await ev(`[...document.querySelectorAll("#team-a .preset")].find((b) => b.textContent === "Warriors 2016–17").click()`);
  await quiet();
  await set("piece-slot", "4", "change");
  const pool = await ev(`${$("piece-pool")}.value`);
  await set("piece-cap-on", "any", "change");
  r = await find();
  const seasonsListed = [...new Set(r.rows.map((x) => meta.players.season[x]))];
  check(pool === "2017" && r.rows.length > 0 && seasonsListed.join() === "2017" && /2016–17 players checked/.test(r.note),
        `replacing a 2016–17 player searches 2016–17 players (${pool}; ${r.status}; ${names(r.rows.slice(0, 3))})`);
  await set("piece-pool", "2008", "change");
  await set("piece-slot", "3", "change");
  r = await find();
  check(await ev(`${$("piece-pool")}.value`) === "2008" && r.rows.every((x) => meta.players.season[x] === 2008),
        `a season the viewer picks stays picked (${r.status})`);
  await set("piece-cap-on", "most", "change");
  if (!await ev(`!!${$("pick-team-b")}`)) { await ev(`${$("b-mode-five")}.click()`); await quiet(); }
  await set("pick-team-b", "Boston Celtics", "change");
  await quiet();
  const celtics = await lineup("b");
  check(same(celtics, "Boston Celtics") && !await ev(`document.getElementById("status").classList.contains("busy")`), `Team B can load a team too (${celtics.map((x) => x[0]).join(", ")})`);
  // the best five (Adam, 2026-10-19): every five of a team-season against Team B's five (the Celtics, loaded above)
  check(await ev(`${$("best-team")}.value`) === "Minnesota Timberwolves" && /start of season/.test(await ev(`${$("best-season")}.selectedOptions[0].textContent`))
        && await ev(`${$("best-against")}.value`) === "b", "the best five starts at the 2026–27 Timberwolves, against Team B's five");
  await set("best-season", "2017", "change");
  await set("best-team", "Cleveland Cavaliers", "change");
  const tBest = Date.now();
  await ev(`${$("best-go")}.click()`);
  await waitFor(`/^(Done in|The search stopped)/.test(${$("best-status")}.textContent)`, 180000);
  // the reference five: tagged in the list when it is among the best, otherwise the last row (designer QA 2026-10-19)
  const refRow = (tag) => `[...${$("best-table")}.querySelectorAll("tbody tr")].find((tr) => ${tag}.test(tr.querySelector("td.who").textContent))`;
  const bres = await ev(`({ status: ${$("best-status")}.textContent, rows: ${$("best-table")}.querySelectorAll("tbody tr").length,
    last: Boolean(${$("best-table")}.querySelector("tbody tr.now")), ref: ${refRow("/most used/")}?.querySelector("td.who").textContent, head: [...${$("best-table")}.querySelectorAll("thead th")].map((x) => x.textContent.trim()),
    note: ${$("best-note")}.textContent, first: ${$("best-table")}.querySelector("tbody tr:not(.now) .five")?.title,
    pending: ${$("best-table")}.querySelectorAll(".pending").length, summary: ${$("best-summary")}.textContent })`);
  console.log(`  best five: ${bres.status} (${Date.now() - tBest} ms in all); first: ${bres.first}; last row: ${bres.ref}`);
  check(/^Done in/.test(bres.status) && bres.rows === (bres.last ? 11 : 10) && /most used/.test(bres.ref) && bres.pending === 0 && bres.head.includes("Combination effects")
        && bres.head.includes("vs most-used five") && /All 1,287 fives/.test(bres.note) && /against Team B's five \(.+\)\. The top 10 are within/.test(bres.summary),
        `the best five lists ten fives with ranges and the most-used five, and names the opponent (${bres.status}; "${bres.summary}")`);
  const tagged = await ev(`[...${$("best-table")}.querySelectorAll("tbody td.who")].filter((td) => /most used/.test(td.textContent)).length`);
  check(tagged === 1, `the most-used five is listed once (${tagged}; designer QA 2026-10-19)`);
  const rights = await ev(`[...document.querySelectorAll("#best-table tbody .use")].map((b) => Math.round(b.getBoundingClientRect().right))`);
  check(rights.length === bres.rows && Math.max(...rights) - Math.min(...rights) <= 1, `the best five's "Put in Team A" buttons line up on one edge (designer QA 2026-10-19: ${JSON.stringify([...new Set(rights)])})`);
  await ev(`${$("library")}.open = true`);
  const lib = await ev(`(() => { const t = document.querySelector("#library table"), s = t.parentElement;
    return { cells: [...new Set([...t.querySelectorAll("tbody tr:first-child td")].map((c) => getComputedStyle(c).display))], over: s.scrollWidth - s.clientWidth }; })()`);
  check(lib.cells.join() === "table-cell" && lib.over <= 1, `the measured-combinations table is a table at 1280 px and fits its box (designer QA 2026-10-19: ${JSON.stringify(lib)})`);
  await ev(`${$("library")}.open = false`);
  await ev(`${$("best-table")}.querySelector("tbody tr:not(.now) .use").click()`);
  await quiet();
  const usedFive = (await lineup("a")).map((x) => x[0]).sort().join(", ");
  check(usedFive === bres.first.split(", ").sort().join(", ") && (await lineup("a")).every((x) => x[1] === 2017), `Use puts that five, as of 2016–17, in Team A (${usedFive})`);
  check(/is now Team A: see the forecast/.test(await ev(`${$("best-status")}.textContent`)), "Put in Team A says what it did, with a link to the forecast");
  await set("pick-team-b", "Denver Nuggets", "change");
  await quiet();
  check(await ev(`${$("best")}.classList.contains("stale")`) && /find again/.test(await ev(`${$("best-status")}.textContent`)), "a new Team B greys the best-five list");
  await set("best-against", "average", "change");
  check(/slower search/.test(await ev(`${$("best-hint")}.textContent`)), "against a league-average lineup the hint says it is slower");
  await set("best-against", "b", "change");
  // from a league-average search, Team A plays a league-average lineup too; Choose a five brings Team B's five back
  const teamBBefore = (await lineup("b")).map((x) => x[0]).join(", ");
  await set("best-against", "average", "change");
  await ev(`${$("best-go")}.click()`);
  await waitFor(`/^(Done in|The search stopped)/.test(${$("best-status")}.textContent)`, 180000);
  const avgRow = await ev(`Number(${$("best-table")}.querySelector("tbody tr:not(.now) td.net").firstChild.textContent.replace("−", "-"))`);
  await ev(`${$("best-table")}.querySelector("tbody tr:not(.now) .use").click()`);
  await quiet();
  const mainNet = await ev(`Number(document.querySelector("#mini-text strong").textContent.replace("−", "-"))`);
  check(Math.abs(mainNet - avgRow) < 0.051 && await ev(`${$("b-mode-average")}.getAttribute("aria-pressed")`) === "true",
        `after a league-average search, the main result plays a league-average lineup too (${avgRow} in the list, ${mainNet} above)`);
  await ev(`${$("b-mode-five")}.click()`);
  await quiet();
  check((await lineup("b")).map((x) => x[0]).join(", ") === teamBBefore, `Choose a five brings Team B's five back (${teamBBefore})`);
  await ev(`${$("b-mode-average")}.click()`);
  await quiet();
  await set("best-against", "b", "change");
  await ev(`${$("best-go")}.click()`);
  check(await ev(`${$("best-status")}.querySelectorAll("button[data-act]").length`) === 2, "Find against Team B with no five for Team B offers the two ways on, beside Find");
  await ev(`${$("best-status")}.querySelector("button[data-act=five]").click()`);
  await quiet();
  // the breaker's cases (QA 2026-10-19)
  await ev(`[...document.querySelectorAll("#team-b .preset")].find((b) => b.textContent === "Five Jokićs").click()`);
  await quiet();
  await ev(`${$("b-mode-average")}.click()`);
  await quiet();
  await ev(`${$("b-mode-five")}.click()`);
  await quiet();
  check((await lineup("b")).every((x) => x[0] === "Nikola Jokić"), "League average and back keeps the five Team B had (five Jokićs)");
  await set("name-b-3", "", "change");
  await quiet();
  await set("best-against", "b", "change");
  await ev(`${$("best-go")}.click()`);
  check(/Fix Team B above/.test(await ev(`${$("best-status")}.textContent`)) && /empty or unrecognized/.test(await ev(`${$("best-hint")}.textContent`)),
        "a Team B with an empty slot is not searched, and the hint says why");
  await ev(`${$("b-mode-five")}.click()`);
  await ev(`[...document.querySelectorAll("#team-b .preset")].find((b) => b.textContent === "Warriors 2016–17").click()`);
  await quiet();
  // players who share a surname are told apart across the table; a searched projected five names its team in the picker
  await set("best-season", "2027", "change");
  await set("best-team", "Oklahoma City Thunder", "change");
  await ev(`${$("best-go")}.click()`);
  await waitFor(`/^(Done in|The search stopped)/.test(${$("best-status")}.textContent)`, 180000);
  const okc = await ev(`[...document.querySelectorAll("#best-table .five")].map((x) => x.textContent)`);
  check(okc.length >= 10 && !okc.some((x) => /(^| · )Williams( · |$)/.test(x)) && okc.some((x) => /Jalen Williams/.test(x)),
        `players who share a surname are told apart in every row (${okc[0]})`);
  await ev(`${refRow("/projected starters/")}.querySelector(".use").click()`);
  await quiet();
  check(await ev(`${$("pick-team-a")}.value`) === "Oklahoma City Thunder" && /In Team A ✓/.test(await ev(`${refRow("/projected starters/")}.querySelector(".use").textContent`)),
        "putting the projected five in Team A names the team in the picker, and the row says it is in Team A");
  await set("pick-team-a", "Boston Celtics", "change");
  await quiet();
  check(!(await ev(`${$("best-table")}.querySelector("tbody tr.used")`)) && !/is now Team A/.test(await ev(`${$("best-status")}.textContent`)),
        "a Team A changed another way clears the list's In Team A row and message");
  await set("best-season", "2026", "change");
  await set("best-team", "Utah Jazz", "change");
  await ev(`${$("best-go")}.click()`);
  await ev(`document.querySelector("#best-table tbody tr:not(.now) .use")?.click()`);    // the old list, while the new one runs
  await set("best-team", "Miami Heat", "change");
  await new Promise((ok) => setTimeout(ok, 3000));
  check(await ev(`${$("best")}.classList.contains("stale")`) && /Click Find to search again/.test(await ev(`${$("best-status")}.textContent`)),
        `a new team mid-search cancels the search and keeps the list grey ("${await ev(`${$("best-status")}.textContent`)}")`);
  await send("Emulation.setDeviceMetricsOverride", { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
  await new Promise((ok) => setTimeout(ok, 400));
  const seasons = await ev(`[0, 1, 2, 3, 4].map((i) => { const s = document.getElementById("season-a-" + i); return s.scrollWidth - s.clientWidth; })`);
  check(seasons.every((x) => x <= 0), `season boxes are not clipped at 375 px (${JSON.stringify(seasons)})`);
  await ev(`${$("best-go")}.click()`);                         // both searches at phone width: the Heat, and the missing piece
  await waitFor(`/^(Done in|The search stopped)/.test(${$("best-status")}.textContent)`, 180000);
  await find();
  for (const id of ["best-table", "piece-table"]) {
    const wide = await ev(`(() => { const t = ${$(id)}, s = t.parentElement;
      return { shown: [...t.querySelectorAll("thead th")].filter((h) => getComputedStyle(h).display !== "none").length,
               heads: t.querySelectorAll("thead th").length, table: s.scrollWidth, box: s.clientWidth, page: document.documentElement.scrollWidth,
               swipe: getComputedStyle(s.previousElementSibling).display !== "none" }; })()`);
    check(wide.shown === wide.heads && wide.heads === 8 && wide.table > wide.box && wide.page <= 375 && wide.swipe,
          `at 375 px ${id} keeps all its columns and scrolls inside its box, not the page, with a line saying so (Adam, 2026-10-19: ${JSON.stringify(wide)})`);
  }
  const box = (id) => `(() => { const r = ${$(id)}.getBoundingClientRect(); return { top: Math.round(r.top + scrollY), bottom: Math.round(r.bottom + scrollY), left: Math.round(r.left), right: Math.round(r.right) }; })()`;
  await ev(`${$("b-mode-average")}.click()`);
  await quiet();
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await new Promise((ok) => setTimeout(ok, 400));
  let A = await ev(box("team-a")), B = await ev(box("team-b")), R = await ev(box("result"));
  check(R.left === B.left && R.top - B.bottom <= 20 && B.bottom - B.top < 180 && R.left > A.right,
        `at 1440 px a league-average Team B is a slim card right above the result, beside Team A (designer QA 2026-10-19: A ${JSON.stringify(A)}, B ${JSON.stringify(B)}, result ${JSON.stringify(R)})`);
  const head0 = await ev(box("team-a"));
  await ev(`document.querySelector("details.rule-help").open = true`);
  const head1 = await ev(box("team-a"));
  await ev(`document.querySelector("details.rule-help").open = false`);
  check(head1.top === head0.top, `opening the levels note moves nothing (Team A at ${head0.top} px, then ${head1.top})`);
  await send("Emulation.setDeviceMetricsOverride", { width: 820, height: 1000, deviceScaleFactor: 1, mobile: false });
  await new Promise((ok) => setTimeout(ok, 400));
  A = await ev(box("team-a")); R = await ev(box("result"));
  check(R.left > A.right && Math.abs(R.top - A.top) <= 2, `at 820 px the result sits beside Team A (designer QA 2026-10-19: A ${JSON.stringify(A)}, result ${JSON.stringify(R)})`);
  await send("Emulation.setDeviceMetricsOverride", { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
  await new Promise((ok) => setTimeout(ok, 400));
  await ev(`window.scrollTo(0, document.body.scrollHeight)`);
  await new Promise((ok) => setTimeout(ok, 400));
  const mini = await ev(`({ shown: !${$("mini")}.hidden, height: ${$("mini")}.offsetHeight, text: ${$("mini-text")}.textContent,
    button: getComputedStyle(document.querySelector("#mini a")).backgroundColor !== "rgba(0, 0, 0, 0)" })`);
  check(mini.shown && mini.height <= 72 && mini.button, `on a phone the summary bar is one compact block with a filled button (${mini.height} px: "${mini.text}"; designer QA 2026-10-19)`);
  await send("Page.navigate", { url: `${site}/model.html` });
  await waitFor(`document.readyState === "complete" && document.getElementById("toc")`);
  const folded = await ev(`!document.getElementById("toc").open`);
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await new Promise((ok) => setTimeout(ok, 300));
  check(folded && await ev(`document.getElementById("toc").open`), "the model page's contents fold on a phone and stay open beside the text on a wide screen (designer QA 2026-10-19)");
  check(errors.length === 0, `no page errors${errors.length ? ": " + errors.join(" | ") : ""}`);
} catch (err) {
  check(false, String(err && err.stack || err));
}
await finish();
