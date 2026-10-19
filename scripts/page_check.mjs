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
//   - at 400 px wide nothing scrolls sideways (SHOT=file.png saves a picture of the search there);
//   - names resolve forgivingly or explain themselves, the result greys out while a slot is unfinished, Escape brings
//     back the last player, and a reload keeps the lineup.
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
  check(c.on === "any" && c.disabled, `the limit starts off (${JSON.stringify(c)})`);
  check(Math.abs(Number(c.value) - q5) < 0.051, `it starts at slot 5's overall quality (${c.value} vs ${q5})`);

  let r = await find();
  console.log(`  any: ${r.status}; ${r.rows.length} listed: ${names(r.rows)}`);
  check(r.head.includes("Combinations") && /inside the net\./.test(r.note), "against a league-average lineup the column is Combinations, in the net");
  const best = Math.max(...r.rows.map((x) => quality("relative", x)));

  await set("piece-cap-on", "most", "change");
  c = await cap();
  check(!c.disabled, "choosing At most enables the number");
  r = await find();
  console.log(`  at most ${c.value}: ${r.status}; ${names(r.rows)}`);
  check(r.rows.length > 0 && r.rows.every((x) => quality("relative", x) <= q5 + 0.051), "every listed candidate is at or under the limit");
  check(/with overall quality [+−]\d+\.\d or lower/.test(r.note) && /above that quality left out/.test(r.note), `the note says so: "${r.note.slice(0, 160)}…"`);
  console.log(`  without the limit the best listed quality was ${best.toFixed(1)}; the limit was ${c.value}`);

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
  check(r.head.includes("Combinations, both teams") && /Team A's minus Team B's/.test(r.note) && /compare rows, not signs/.test(r.note),
        `against Team B the column is "Combinations, both teams" and the note explains it (${r.status})`);

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
  n = await name(3, "<img src=x onerror=alert(1)>");
  check(/No player matches/.test(n.msg) && n.stale && n.warn, `junk is refused with a message: "${n.msg.slice(0, 60)}"`);
  await ev(`${$("name-a-3")}.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }))`);
  await quiet();
  n = await name(3, await ev(`${$("name-a-3")}.value`));
  check(n.value === "Anthony Edwards" && !n.stale, `Escape brings back the last player: ${n.value}`);
  n = await name(4, "Steph", "input");
  check(n.stale && /press Enter/.test(n.status) && await ev(`${$("slot-a-4")}.classList.contains("pending")`), "a half-typed name greys the result until it is finished");
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
  const text = await ev(`document.body.innerText`);
  check(!/\d\.\.(\s|$)/.test(text), "no double full stops after numbers");
  await ev(`document.querySelector("details.assume").open = true`);
  const fits = await ev(`[...document.querySelectorAll("#below .scroll")].map((s) => s.scrollWidth - s.clientWidth)`);
  check(fits.every((x) => x <= 1), `the range and breakdown tables fit at 1280 px (overflow ${JSON.stringify(fits)})`);
  await send("Emulation.setDeviceMetricsOverride", { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
  await new Promise((ok) => setTimeout(ok, 400));
  const seasons = await ev(`[0, 1, 2, 3, 4].map((i) => { const s = document.getElementById("season-a-" + i); return s.scrollWidth - s.clientWidth; })`);
  check(seasons.every((x) => x <= 0), `season boxes are not clipped at 375 px (${JSON.stringify(seasons)})`);
  check(errors.length === 0, `no page errors${errors.length ? ": " + errors.join(" | ") : ""}`);
} catch (err) {
  check(false, String(err && err.stack || err));
}
await finish();
