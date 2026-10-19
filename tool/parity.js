// Node harness for tests/test_tool_parity.py: node tool/parity.js <export dir> <cases.json> <out.json>
const fs = require("fs");
const path = require("path");
const { create } = require("./lineup_model.js");

const [dir, casesPath, outPath] = process.argv.slice(2);
const meta = JSON.parse(fs.readFileSync(path.join(dir, "meta.json"), "utf8"));
const buffer = (name) => { const b = fs.readFileSync(path.join(dir, name)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); };
const model = create(meta, buffer("weights.bin"), buffer("players.bin"));
const cases = JSON.parse(fs.readFileSync(casesPath, "utf8"));

const started = Date.now();
const out = {
  native: cases.native.map((c) => model.nativeBySeed(c.arm, c.offense, c.defense, c.rule)),
  profile: (cases.profile || []).map((r) => model.profile(r)),
  ratings: cases.ratings.map((c) => model.ratings(c.rows, c.rule, c.arm)),
  band_lineup: cases.band_lineup.map((c) => model.band.lineup(c.rows, c.rule)),
  band_matchup: cases.band_matchup.map((c) => model.band.matchup(c.a, c.b, c.rule)),
  explain_lineup: cases.explain_lineup.map((c) => model.explain.lineup(c.rows, c.rule)),
  explain_against: cases.explain_against.map((c) => model.explain.against(c.rows, c.opponent, c.rule)),
  combinations_lineup: cases.combinations_lineup.map((c) => {
    const layer = model.combinations.lineup(c.rows, c.rule, model.explain.lineup(c.rows, c.rule).rates);
    return { layer, band: model.band.lineup(c.rows, c.rule, layer) };
  }),
  combinations_matchup: cases.combinations_matchup.map((c) => {
    const layer = model.combinations.matchup(c.a, c.b, c.rule, model.explain.against(c.a, c.b, c.rule).rates,
                                             model.explain.against(c.b, c.a, c.rule).rates);
    return { layer, band: model.band.matchup(c.a, c.b, c.rule, layer) };
  }),
  learned_points: cases.learned_points.map((c) => model.learned.points(c.offense, c.defense, c.rule)),
  learned_lineup: cases.learned_lineup.map((c) => {
    const layer = model.combinations.lineup(c.rows, c.rule, model.explain.lineup(c.rows, c.rule).rates);
    const learned = model.learned.lineup(c.rows, c.rule);
    return { learned, band: model.band.lineup(c.rows, c.rule, layer, learned), search: model.search.forecast(c.rows, c.rule) };
  }),
  learned_matchup: cases.learned_matchup.map((c) => {
    const layer = model.combinations.matchup(c.a, c.b, c.rule, model.explain.against(c.a, c.b, c.rule).rates,
                                             model.explain.against(c.b, c.a, c.rule).rates);
    const learned = model.learned.matchup(c.a, c.b, c.rule);
    return { learned, band: model.band.matchup(c.a, c.b, c.rule, layer, learned), search: model.search.forecast(c.a, c.rule, c.b),
             searchBand: model.search.band(c.a, c.rule, c.b).margin };
  }),
};
out.seconds = (Date.now() - started) / 1000;
fs.writeFileSync(outPath, JSON.stringify(out));
