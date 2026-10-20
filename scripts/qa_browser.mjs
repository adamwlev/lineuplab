// A shared headless-Chrome session for QA personas (first-time-user QA of the built tool, 2026-10-18).
// One browser at a time on this laptop (the Mac is shared and the refresh holds two cores): `start` waits for the
// lock. The browser and a static server for the built page live in a background daemon, so emulation (phone
// screen, slow network, slow CPU) holds across commands. The page sees navigator.hardwareConcurrency = 3, so it
// runs its model worker and one helper: two threads.
//
//   node scripts/qa_browser.mjs PERSONA start --build DIR --out DIR [--viewport 1280x800] [--mobile]
//                                              [--network slow3g] [--cpu 4]
//   node scripts/qa_browser.mjs PERSONA goto [PAGE]            open PAGE of the build (default index.html, else lineups.html)
//   node scripts/qa_browser.mjs PERSONA elements               visible controls, each with a selector to use
//   node scripts/qa_browser.mjs PERSONA sections               headings, each with a selector for text or shot
//   node scripts/qa_browser.mjs PERSONA text [SELECTOR]        visible text (default the whole page)
//   node scripts/qa_browser.mjs PERSONA shot NAME [--full] [--selector CSS]   a screenshot: OUT/NN-NAME.png
//   node scripts/qa_browser.mjs PERSONA click SELECTOR | --text "VISIBLE TEXT" [--double]
//   node scripts/qa_browser.mjs PERSONA hover SELECTOR | --text "VISIBLE TEXT"   and the tooltip it would show
//   node scripts/qa_browser.mjs PERSONA type SELECTOR "TEXT" [--clear]
//   node scripts/qa_browser.mjs PERSONA suggest SELECTOR       what a text box's suggestion list offers
//   node scripts/qa_browser.mjs PERSONA press KEY              Enter, Tab, Escape, Backspace, ArrowDown, ArrowUp
//   node scripts/qa_browser.mjs PERSONA select SELECTOR VALUE | --label "OPTION TEXT"
//   node scripts/qa_browser.mjs PERSONA scroll SELECTOR | --text "VISIBLE TEXT" | --y PIXELS
//   node scripts/qa_browser.mjs PERSONA wait SECONDS           (at most 300)
//   node scripts/qa_browser.mjs PERSONA viewport WxH [--mobile]  a new screen size (and touch), keeping the page
//   node scripts/qa_browser.mjs PERSONA scheme light | dark     the system theme the page sees (prefers-color-scheme)
//   node scripts/qa_browser.mjs PERSONA back | forward | reload | status | errors
//   node scripts/qa_browser.mjs PERSONA eval "JS"              diagnosis only
//   node scripts/qa_browser.mjs PERSONA stop                   always, when done: frees the browser
//
// A session closes itself after 15 idle minutes. Lock and session: experiments/cache/qa_browser/.
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import zlib from "node:zlib";

const SELF = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(SELF), "..");
const STATE = path.join(ROOT, "experiments", "cache", "qa_browser");
const LOCK = path.join(STATE, "lock"), OWNER = path.join(LOCK, "owner.json"), SESSION = path.join(LOCK, "session.json");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const IDLE_MS = 15 * 60 * 1000, WAIT_MS = 540 * 1000;
const NETWORKS = {   // Chrome DevTools' presets
  slow3g: { offline: false, latency: 2000, downloadThroughput: 51200, uploadThroughput: 51200 },
  fast3g: { offline: false, latency: 563, downloadThroughput: 184320, uploadThroughput: 86400 },
};
const KEYS = { Enter: [13, "\r"], Tab: [9, ""], Escape: [27, ""], Backspace: [8, ""], ArrowDown: [40, ""], ArrowUp: [38, ""] };
const sleep = (ms) => new Promise((ok) => setTimeout(ok, ms));
const alive = (pid) => { try { process.kill(pid, 0); return true; } catch { return false; } };
const readJson = (f) => { try { return JSON.parse(fs.readFileSync(f, "utf8")); } catch { return null; } };
function usage(msg) {
  if (msg) { console.error(msg); process.exit(2); }
  console.error(fs.readFileSync(SELF, "utf8").split("\n").filter((l) => l.startsWith("//")).slice(0, 26).join("\n"));
  process.exit(2);
}
function flags(args) {                       // --name value, --switch
  const out = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const k = args[i].slice(2);
      if (i + 1 < args.length && !args[i + 1].startsWith("--")) out[k] = args[++i]; else out[k] = true;
    } else out._.push(args[i]);
  }
  return out;
}

// ---- the lock --------------------------------------------------------------------------------------------
function holder() {                          // who holds the browser, or null if the lock is free or stale
  if (!fs.existsSync(LOCK)) return null;
  const s = readJson(SESSION), o = readJson(OWNER);
  if (s && alive(s.daemon)) return s.persona;
  if (!s && o && alive(o.pid)) return o.persona;
  if (!s && !o && Date.now() - fs.statSync(LOCK).mtimeMs < 30000) return "(starting)";
  fs.rmSync(LOCK, { recursive: true, force: true });     // stale: its owner is gone
  return null;
}
async function acquire(persona) {
  fs.mkdirSync(STATE, { recursive: true });
  const t0 = Date.now();
  let said = false;
  while (Date.now() - t0 < WAIT_MS) {
    const h = holder();
    if (h === persona) return "mine";
    if (h === null) {
      try { fs.mkdirSync(LOCK); fs.writeFileSync(OWNER, JSON.stringify({ persona, pid: process.pid })); return "got"; }
      catch (e) { if (e.code !== "EEXIST") throw e; }
    } else if (!said) { console.log(`Waiting: the browser is in use by "${h}" (one browser at a time).`); said = true; }
    await sleep(5000);
  }
  console.log(`The browser is still in use by "${holder()}". Run start again to keep waiting.`);
  process.exit(3);
}

async function start(persona, args) {
  const f = flags(args);
  if (!f.build || !f.out) usage("start needs --build DIR and --out DIR");
  const got = await acquire(persona);
  if (got === "mine") { console.log(`The browser is already yours, ${persona}. Use goto.`); return; }
  const opts = { build: path.resolve(f.build), out: path.resolve(f.out), viewport: f.viewport || "1280x800",
                 mobile: Boolean(f.mobile), network: f.network || "none", cpu: Number(f.cpu || 1) };
  if (!["lineups.html", "index.html"].some(f => fs.existsSync(path.join(opts.build, f)))) {   // a --site build has index.html
    fs.rmSync(LOCK, { recursive: true, force: true }); usage(`no lineups.html or index.html in ${opts.build}`);
  }
  if (opts.network !== "none" && !NETWORKS[opts.network]) { fs.rmSync(LOCK, { recursive: true, force: true }); usage(`unknown network ${opts.network}`); }
  fs.mkdirSync(opts.out, { recursive: true });
  const log = fs.openSync(path.join(opts.out, "browser.log"), "a");
  spawn(process.execPath, [SELF, persona, "daemon", JSON.stringify(opts)], { detached: true, stdio: ["ignore", log, log] }).unref();
  for (let i = 0; i < 120; i++) {
    const s = readJson(SESSION);
    if (s && s.port) {
      console.log(`Browser ready for ${persona}: ${opts.viewport}${opts.mobile ? " phone" : ""}, network ${opts.network}`
        + `${opts.cpu > 1 ? `, CPU slowed ${opts.cpu}x` : ""}. Screenshots go to ${opts.out}. Next: goto`);
      return;
    }
    await sleep(500);
  }
  console.log(`The browser did not start; see ${path.join(opts.out, "browser.log")}`);
  process.exit(1);
}

async function send(persona, cmd, args) {
  const s = readJson(SESSION);
  if (!s || !alive(s.daemon)) usage(`No browser session: run "node scripts/qa_browser.mjs ${persona} start ..." first.`);
  if (s.persona !== persona) usage(`The browser is in use by "${s.persona}". Run start to wait for it.`);
  const body = JSON.stringify({ cmd, args });
  const reply = await new Promise((ok, fail) => {
    const req = http.request({ host: "127.0.0.1", port: s.port, method: "POST", path: "/" }, (res) => {
      let d = ""; res.on("data", (c) => (d += c)); res.on("end", () => ok(d));
    });
    req.on("error", fail); req.end(body);
  });
  const r = JSON.parse(reply);
  console.log(r.out);
  if (!r.ok) process.exit(1);
}

// ---- the daemon: static server, Chrome, CDP ---------------------------------------------------------------
async function daemon(persona, opts) {
  const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json", ".txt": "text/plain", ".png": "image/png", ".svg": "image/svg+xml" };
  const HOME = fs.existsSync(path.join(opts.build, "index.html")) ? "index.html" : "lineups.html";   // a --site build's page
  const gz = new Map();
  const site = http.createServer((req, res) => {                // gzip, with revalidation, like a typical host
    const name = decodeURIComponent(new URL(req.url, "http://x").pathname).replace(/^\/+/, "") || HOME;
    if (name === "favicon.ico") { res.writeHead(204); res.end(); return; }      // the host supplies the icon
    const file = path.join(opts.build, name);
    if (!file.startsWith(opts.build) || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404); res.end("not found"); return; }
    const etag = `"${fs.statSync(file).mtimeMs}"`, key = file + etag;     // a rebuilt file is served fresh
    if (!gz.has(key)) gz.set(key, zlib.gzipSync(fs.readFileSync(file)));
    if (req.headers["if-none-match"] === etag) { res.writeHead(304, { etag }); res.end(); return; }
    const zipped = /gzip/.test(req.headers["accept-encoding"] || "");
    const body = zipped ? gz.get(key) : fs.readFileSync(file);
    res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "application/octet-stream", "content-length": body.length,
                         "cache-control": "no-cache", etag, ...(zipped ? { "content-encoding": "gzip" } : {}) });
    res.end(body);
  });
  await new Promise((ok) => site.listen(0, "127.0.0.1", ok));
  const origin = `http://127.0.0.1:${site.address().port}`;

  let [w, h] = opts.viewport.split("x").map(Number);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "qa-browser-"));
  const chrome = spawn(CHROME, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`, "--no-first-run",
                                "--disable-gpu", `--window-size=${w},${h}`, "about:blank"], { stdio: ["ignore", "ignore", "pipe"] });
  const wsUrl = await new Promise((ok, fail) => {
    let err = ""; chrome.stderr.on("data", (d) => { err += d; const m = err.match(/DevTools listening on (ws:\/\/\S+)/); if (m) ok(m[1]); });
    setTimeout(() => fail(new Error("Chrome did not start")), 30000);
  });
  const target = await (await fetch(`http://127.0.0.1:${new URL(wsUrl).port}/json/new?about:blank`, { method: "PUT" })).json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok) => ws.addEventListener("open", ok));
  let seq = 0;
  const pending = new Map(), listeners = [], errors = [];
  ws.addEventListener("message", (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
    if (m.method === "Runtime.exceptionThrown") errors.push(`uncaught: ${m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text}`);
    if (m.method === "Runtime.consoleAPICalled" && (m.params.type === "error" || m.params.type === "warning"))
      errors.push(`console.${m.params.type}: ${m.params.args.map((a) => a.value ?? a.description ?? "").join(" ")}`);
    if (m.method === "Log.entryAdded" && m.params.entry.level === "error") errors.push(`browser: ${m.params.entry.text} ${m.params.entry.url || ""}`);
    for (const l of listeners.slice()) l(m);
  });
  const cdp = (method, params = {}) => new Promise((ok, fail) => {
    const k = ++seq; pending.set(k, (m) => (m.error ? fail(new Error(`${method}: ${m.error.message}`)) : ok(m.result)));
    ws.send(JSON.stringify({ id: k, method, params }));
  });
  const once = (method, ms) => new Promise((ok) => {
    const l = (m) => { if (m.method === method) { listeners.splice(listeners.indexOf(l), 1); ok(true); } };
    listeners.push(l); setTimeout(() => { const i = listeners.indexOf(l); if (i >= 0) { listeners.splice(i, 1); ok(false); } }, ms);
  });
  for (const d of ["Page", "Runtime", "Log", "Network"]) await cdp(`${d}.enable`);
  await cdp("Emulation.setHardwareConcurrencyOverride", { hardwareConcurrency: 3 });
  await cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: opts.mobile ? 2 : 1, mobile: opts.mobile });
  if (opts.mobile) {
    await cdp("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
    await cdp("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1" });
  }
  if (opts.cpu > 1) await cdp("Emulation.setCPUThrottlingRate", { rate: opts.cpu });
  if (NETWORKS[opts.network]) await cdp("Network.emulateNetworkConditions", NETWORKS[opts.network]);

  const evaluate = async (expression) => {
    const r = await cdp("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };
  const PAGE_HELPERS = `
    const visible = (e) => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
      return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none" && !e.closest("[hidden]"); };
    const cssPath = (e) => { if (e.id) return "#" + CSS.escape(e.id); const parts = [];
      while (e && e.nodeType === 1 && !e.id) { let i = 1, s = e; while ((s = s.previousElementSibling)) if (s.tagName === e.tagName) i++;
        parts.unshift(e.tagName.toLowerCase() + ":nth-of-type(" + i + ")"); e = e.parentElement; }
      if (e && e.id) parts.unshift("#" + CSS.escape(e.id)); return parts.join(" > "); };
    const labelOf = (e) => { const t = (x) => (x || "").replace(/\\s+/g, " ").trim();
      if (e.getAttribute("aria-label")) return t(e.getAttribute("aria-label"));
      if (e.id) { const l = document.querySelector('label[for="' + e.id + '"]'); if (l) return t(l.innerText); }
      return t(e.innerText) || t(e.placeholder) || t(e.title) || t(e.value); };
    const find = (sel, text) => {
      if (sel) return document.querySelector(sel);
      const want = text.replace(/\\s+/g, " ").trim().toLowerCase(), norm = (e) => (e.innerText || "").replace(/\\s+/g, " ").trim().toLowerCase();
      const all = [...document.querySelectorAll("button, a, summary, label, [role=button], th, td, h1, h2, h3, li, span, p, div, abbr, strong")].filter(visible);
      const act = (e) => /^(BUTTON|A|SUMMARY|LABEL)$/.test(e.tagName) || e.getAttribute("role") === "button";
      return all.find((e) => act(e) && norm(e) === want) || all.find((e) => norm(e) === want)
          || all.find((e) => act(e) && norm(e).includes(want))
          || all.filter((e) => norm(e).includes(want)).sort((p, q) => norm(p).length - norm(q).length)[0] || null; };`;
  let counter = fs.readdirSync(opts.out).filter((f) => /^\d+-.*\.png$/.test(f)).length, lastGoto = Date.now();
  const at = async (sel, text) => {          // scroll the element into view; its centre in CSS pixels
    const r = await evaluate(`(() => { ${PAGE_HELPERS} const e = find(${JSON.stringify(sel || null)}, ${JSON.stringify(text || "")});
      if (!e) return null; e.scrollIntoView({ block: "center", inline: "center" });
      // a wrapped link has one box per line: aim at the largest, and say if something else is on top of it
      const boxes = [...e.getClientRects()].filter((r) => r.width > 0 && r.height > 0).sort((p, q) => q.width * q.height - p.width * p.height);
      const b = boxes[0] || e.getBoundingClientRect(), x = b.left + b.width / 2, y = b.top + b.height / 2;
      const top = document.elementFromPoint(x, y), covered = top && top !== e && !e.contains(top) && !top.contains(e);
      return { x, y, what: e.tagName.toLowerCase() + (e.id ? "#" + e.id : "") + ' "' + labelOf(e).slice(0, 60) + '"', disabled: Boolean(e.disabled),
               covered: covered ? top.tagName.toLowerCase() + (top.id ? "#" + top.id : "") + ' "' + labelOf(top).slice(0, 40) + '"' : null }; })()`);
    if (!r) throw new Error(`Nothing on the page matches ${sel ? `selector ${sel}` : `text "${text}"`}. Try elements.`);
    return r;
  };
  const mouse = async (x, y, count) => {
    await cdp("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
    for (let c = 1; c <= count; c++) {
      await cdp("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", clickCount: c });
      await cdp("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", clickCount: c });
    }
  };
  const newErrors = (n0) => (errors.length > n0 ? `\nNew page errors:\n  ${errors.slice(n0).join("\n  ")}` : "");
  const navWait = async (fn) => { const loaded = once("Page.loadEventFired", 90000); await fn(); return (await loaded) ? "loaded" : "still loading after 90 s"; };
  const historyWait = async (fn) => {             // back, forward, reload: any navigation signal, then the document
    const signals = ["Page.loadEventFired", "Page.navigatedWithinDocument", "Page.frameNavigated"].map((m) => once(m, 30000));
    await fn();
    const moved = await Promise.race(signals);
    for (let i = 0; i < 120; i++) { if (await evaluate("document.readyState") === "complete") return moved ? "loaded" : "no navigation seen in 30 s"; await sleep(250); }
    return "still loading after 30 s";
  };

  const commands = {
    async goto([page = HOME]) {
      lastGoto = Date.now();
      const n0 = errors.length, t0 = Date.now();
      const s = await navWait(() => cdp("Page.navigate", { url: `${origin}/${page.replace(/^\/+/, "")}` }));
      return `${page}: ${s} in ${((Date.now() - t0) / 1000).toFixed(1)} s (the page may keep loading data after this)` + newErrors(n0);
    },
    async elements() {
      const list = await evaluate(`(() => { ${PAGE_HELPERS}
        return [...document.querySelectorAll("a[href], button, input, select, textarea, summary, [role=button], [tabindex]:not([tabindex='-1'])")]
          .filter(visible).slice(0, 150).map((e) => { const b = e.getBoundingClientRect();
            const s = { sel: cssPath(e), tag: e.tagName.toLowerCase() + (e.type && e.tagName !== "BUTTON" && e.tagName !== "SELECT" ? "[" + e.type + "]" : ""),
                        label: labelOf(e).slice(0, 80), on_screen: b.bottom > 0 && b.top < innerHeight, disabled: Boolean(e.disabled) };
            if (e.tagName === "SELECT") { s.value = e.options[e.selectedIndex]?.text; s.options = [...e.options].map((o) => o.text).slice(0, 10); s.count = e.options.length; }
            else if (e.tagName === "INPUT") s.value = e.value;
            if (e.getAttribute("aria-pressed")) s.pressed = e.getAttribute("aria-pressed");
            return s; }); })()`);
      return list.map((e) => `${e.on_screen ? "  " : "↓ "}${e.sel}  ${e.tag}  "${e.label}"${e.value !== undefined ? `  value="${e.value}"` : ""}`
        + `${e.options ? `  options=[${e.options.join(" | ")}${e.count > 10 ? ` | … ${e.count} in all` : ""}]` : ""}${e.pressed ? `  pressed=${e.pressed}` : ""}${e.disabled ? "  DISABLED" : ""}`).join("\n")
        + "\n(↓ = below or above the visible screen)";
    },
    async text([sel]) {
      const t = await evaluate(`(() => { const e = ${sel ? `document.querySelector(${JSON.stringify(sel)})` : "document.body"};
        return e ? e.innerText : null; })()`);
      if (t === null) throw new Error(`Nothing matches ${sel}`);
      return t.length > 6000 ? t.slice(0, 6000) + `\n… (${t.length - 6000} more characters; pass a selector)` : t;
    },
    async shot([name = "screen", ...rest]) {
      const f = flags(rest), file = path.join(opts.out, `${String(++counter).padStart(2, "0")}-${name.replace(/[^\w-]+/g, "-").slice(0, 60)}.png`);
      const p = { format: "png" };
      if (f.selector) {
        const b = await evaluate(`(() => { const e = document.querySelector(${JSON.stringify(f.selector)}); if (!e) return null;
          const r = e.getBoundingClientRect(); return { x: Math.max(0, r.left + scrollX), y: Math.max(0, r.top + scrollY), width: Math.max(1, r.width), height: Math.min(Math.max(1, r.height), 4000) }; })()`);
        if (!b) throw new Error(`Nothing matches ${f.selector}`);
        Object.assign(p, { clip: { ...b, scale: 1 }, captureBeyondViewport: true });
      } else if (f.full) {
        const m = await cdp("Page.getLayoutMetrics");
        Object.assign(p, { clip: { x: 0, y: 0, width: w, height: Math.min(m.cssContentSize.height, 8000), scale: 1 }, captureBeyondViewport: true });
      }
      const r = await cdp("Page.captureScreenshot", p);
      fs.writeFileSync(file, Buffer.from(r.data, "base64"));
      return `Saved ${file}`;
    },
    async click(args) {
      const f = flags(args), n0 = errors.length, el = await at(f._[0], f.text);
      await mouse(el.x, el.y, f.double ? 2 : 1);
      await sleep(400);
      return `Clicked ${el.what}${el.disabled ? " (it is disabled)" : ""}${f.double ? " twice" : ""}.`
        + (el.covered ? ` Note: ${el.covered} is on top of it, so the click landed there.` : "") + newErrors(n0);
    },
    async type(args) {
      const f = flags(args), [sel, text = ""] = f._, n0 = errors.length;
      const el = await at(sel);
      await mouse(el.x, el.y, 1);
      await evaluate(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); e.focus();
        ${f.clear ? `e.value = ""; e.dispatchEvent(new Event("input", { bubbles: true }));` : ""} })()`);
      if (text) await cdp("Input.insertText", { text });
      await sleep(200);
      const v = await evaluate(`document.querySelector(${JSON.stringify(sel)}).value`);
      return `Typed into ${el.what}; it now reads "${v}". (A text box usually takes effect on Enter or Tab.)` + newErrors(n0);
    },
    async suggest([sel]) {
      const r = await evaluate(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null;
        if (!e.list) return []; const v = e.value.toLowerCase();
        return [...e.list.options].map((o) => o.value).filter((x) => x.toLowerCase().includes(v)).slice(0, 12); })()`);
      if (r === null) throw new Error(`Nothing matches ${sel}`);
      return r.length ? `The suggestion list would show (roughly):\n  ${r.join("\n  ")}` : "No suggestions.";
    },
    async press([key]) {
      if (!KEYS[key]) throw new Error(`Unknown key ${key}; use ${Object.keys(KEYS).join(", ")}`);
      const [code, text] = KEYS[key], n0 = errors.length;
      const before = await evaluate(`document.activeElement && (document.activeElement.id || document.activeElement.tagName)`);
      await cdp("Input.dispatchKeyEvent", { type: "keyDown", key, code: key, windowsVirtualKeyCode: code, text: text || undefined });
      await cdp("Input.dispatchKeyEvent", { type: "keyUp", key, code: key, windowsVirtualKeyCode: code });
      if (key === "Tab" && before === await evaluate(`document.activeElement && (document.activeElement.id || document.activeElement.tagName)`))
        await evaluate(`document.activeElement && document.activeElement.blur()`);
      await sleep(300);
      return `Pressed ${key}.` + newErrors(n0);
    },
    async select(args) {
      const f = flags(args), [sel, value] = f._, n0 = errors.length;
      await at(sel);
      const r = await evaluate(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e || e.tagName !== "SELECT") return { error: "not a dropdown" };
        const want = ${JSON.stringify(f.label || value || "")}.toLowerCase();
        const o = [...e.options].find((o) => ${f.label ? "o.text.toLowerCase().includes(want)" : "o.value.toLowerCase() === want"});
        if (!o) return { error: "no such option; options: " + [...e.options].map((o) => o.text + " (value " + o.value + ")").join(", ") };
        if (e.disabled) return { error: "the dropdown is disabled" };
        e.value = o.value; e.dispatchEvent(new Event("input", { bubbles: true })); e.dispatchEvent(new Event("change", { bubbles: true }));
        return { chose: o.text }; })()`);
      if (r.error) throw new Error(r.error);
      await sleep(300);
      return `Chose "${r.chose}".` + newErrors(n0);
    },
    async scroll(args) {
      const f = flags(args);
      if (f.y !== undefined) await evaluate(`scrollTo(0, ${Number(f.y)})`);
      else if (f._[0] || f.text) await at(f._[0], f.text);
      else throw new Error("scroll needs a selector, --text \"VISIBLE TEXT\" or --y PIXELS");
      return `Scrolled; the window's top is at ${await evaluate("Math.round(scrollY)")} px of ${await evaluate("document.documentElement.scrollHeight")}.`;
    },
    async viewport([size, ...rest]) {     // the designer persona (2026-10-19) compares desktop and phone in one session
      const f = flags(rest), m = /^(\d+)x(\d+)$/.exec(size || "");
      if (!m) throw new Error("usage: viewport WIDTHxHEIGHT [--mobile]");
      [w, h] = [Number(m[1]), Number(m[2])];
      await cdp("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: f.mobile ? 2 : 1, mobile: Boolean(f.mobile) });
      await cdp("Emulation.setTouchEmulationEnabled", { enabled: Boolean(f.mobile), maxTouchPoints: 5 });
      opts.viewport = size;
      return `The screen is now ${size}${f.mobile ? ", a phone" : ""}.`;
    },
    async scheme([value]) {
      if (!["light", "dark"].includes(value)) throw new Error("usage: scheme light | dark");
      await cdp("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value }] });
      return `The page now sees a ${value} system theme.`;
    },
    async wait([s = "2"]) { await sleep(Math.min(Number(s), 300) * 1000); return `Waited ${Math.min(Number(s), 300)} s.`; },
    async back() {
      const n0 = errors.length, h = await cdp("Page.getNavigationHistory");
      if (h.currentIndex < 1) return "Nothing to go back to.";
      const s = await historyWait(() => cdp("Page.navigateToHistoryEntry", { entryId: h.entries[h.currentIndex - 1].id }));
      return `Went back to ${h.entries[h.currentIndex - 1].url.replace(origin, "")}: ${s}.` + newErrors(n0);
    },
    async forward() {
      const n0 = errors.length, h = await cdp("Page.getNavigationHistory");
      if (h.currentIndex >= h.entries.length - 1) return "Nothing to go forward to.";
      const s = await historyWait(() => cdp("Page.navigateToHistoryEntry", { entryId: h.entries[h.currentIndex + 1].id }));
      return `Went forward to ${h.entries[h.currentIndex + 1].url.replace(origin, "")}: ${s}.` + newErrors(n0);
    },
    async reload() { const n0 = errors.length; const s = await historyWait(() => cdp("Page.reload")); lastGoto = Date.now(); return `Reloaded: ${s}.` + newErrors(n0); },
    async hover(args) {
      const f = flags(args), el = await at(f._[0], f.text);
      await cdp("Input.dispatchMouseEvent", { type: "mouseMoved", x: el.x, y: el.y });
      await sleep(300);
      const tip = await evaluate(`(() => { const e = document.elementFromPoint(${el.x}, ${el.y}); const t = e && e.closest("[title]"); return t ? t.title : null; })()`);
      return `Hovering over ${el.what}.` + (tip ? ` Its tooltip would say: "${tip}"` : " It has no tooltip.");
    },
    async sections() {
      const list = await evaluate(`(() => { ${PAGE_HELPERS}
        return [...document.querySelectorAll("h1, h2, h3, summary, [role=dialog][open] h2")].filter(visible).map((h) => {
          let c = h.closest("section, details, dialog, .card, .team, .result, header") || h.parentElement;
          const b = h.getBoundingClientRect();
          return (b.bottom > 0 && b.top < innerHeight ? "  " : "↓ ") + h.innerText.replace(/\\s+/g, " ").trim().slice(0, 60) + "  ->  " + cssPath(c); }); })()`);
      return list.join("\n") + "\n(use the selector after -> with text or shot --selector; ↓ = off screen)";
    },
    async status() {
      const r = await evaluate(`({ url: location.href, title: document.title, ready: document.readyState, scroll: Math.round(scrollY), height: document.documentElement.scrollHeight })`);
      return `${r.url.replace(origin, "")} "${r.title}" ${r.ready}; ${((Date.now() - lastGoto) / 1000).toFixed(0)} s since the last goto or reload;`
        + ` scrolled ${r.scroll} of ${r.height} px; viewport ${opts.viewport}, network ${opts.network}.`;
    },
    async errors() { return errors.length ? errors.slice(-50).join("\n") : "No page errors so far."; },
    async eval([js]) { const v = await evaluate(js); const s = JSON.stringify(v); return s && s.length > 4000 ? s.slice(0, 4000) + "…" : String(s); },
  };

  let idle = null, queue = Promise.resolve(), stopping = false;
  const stop = async () => {
    if (stopping) return; stopping = true;
    try { ws.close(); } catch {}
    await new Promise((ok) => { chrome.once("exit", ok); chrome.kill(); setTimeout(ok, 5000); });
    site.close(); control.close();
    fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    fs.rmSync(LOCK, { recursive: true, force: true });
    process.exit(0);
  };
  const touch = () => { clearTimeout(idle); idle = setTimeout(() => { console.log("idle: closing"); stop(); }, IDLE_MS); };
  const control = http.createServer((req, res) => {
    let d = ""; req.on("data", (c) => (d += c));
    req.on("end", () => {
      queue = queue.then(async () => {
        touch();
        const { cmd, args } = JSON.parse(d);
        if (cmd === "stop") { res.end(JSON.stringify({ ok: true, out: "Browser closed; it is free for the next user." })); setTimeout(stop, 50); return; }
        try {
          if (!commands[cmd]) throw new Error(`Unknown command ${cmd}`);
          res.end(JSON.stringify({ ok: true, out: await commands[cmd](args || []) }));
        } catch (e) { res.end(JSON.stringify({ ok: false, out: `Error: ${e.message}` })); }
      });
    });
  });
  await new Promise((ok) => control.listen(0, "127.0.0.1", ok));
  chrome.once("exit", () => { if (!stopping) { console.log("Chrome exited"); stop(); } });
  touch();
  fs.writeFileSync(SESSION, JSON.stringify({ persona, daemon: process.pid, port: control.address().port, opts }));
  console.log(`daemon ${process.pid} for ${persona}: site ${origin}, control ${control.address().port}`);
}

const [persona, cmd, ...rest] = process.argv.slice(2);
if (!persona || !cmd || persona.startsWith("-")) usage();
if (cmd === "daemon") await daemon(persona, JSON.parse(rest[0]));
else if (cmd === "start") await start(persona, rest);
else await send(persona, cmd, rest);
