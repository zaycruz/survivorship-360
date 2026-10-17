"""Build the hosted deck viewer: web/index.html plus web/slides/NN.png, from slides/ and slides.py notes.

Run: python3 build_web.py [out_dir]   (default: ./web). Publish index.html with the PNGs as files.
"""
import datetime
import html
import json
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from slides import SLIDES  # noqa: E402

out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "web"))
os.makedirs(os.path.join(out, "slides"), exist_ok=True)
for i in range(1, len(SLIDES) + 1):
    shutil.copy(os.path.join(here, "slides", f"{i:02d}.png"), os.path.join(out, "slides", f"{i:02d}.png"))

# Live Patient 360 screenshots used on slides 3 and 10 (Paper loads them from the hosted URL).
if os.path.isdir(os.path.join(here, "shots")):
    shutil.copytree(os.path.join(here, "shots"), os.path.join(out, "shots"), dirs_exist_ok=True)

data = [{"n": i, "name": s["name"][3:], "notes": s["notes"]} for i, s in enumerate(SLIDES, 1)]
thumbs = "\n".join(
    f'<button class="thumb" data-i="{d["n"] - 1}" aria-label="Slide {d["n"]}: {html.escape(d["name"])}">'
    f'<img src="slides/{d["n"]:02d}.png" alt="" loading="lazy"><span>{d["n"]:02d} · {html.escape(d["name"])}</span></button>'
    for d in data
)

page = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Survivorship 360 Pitch</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;700&display=swap">
<style>
/* Layout: a presenter frame. Slide stage on top, controls bar, then a strip of every slide. */
:root {
  --bg: #f3f5f8; --surface: #ffffff; --ink: #0f1b2d; --muted: #44536a; --line: #dde3eb; --accent: #0b5cad; --on-accent: #ffffff;
  --display: "IBM Plex Sans", system-ui, sans-serif; --body: "IBM Plex Sans", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, monospace;
}
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font-family: var(--body); margin: 0 }
.wrap { max-width: 1280px; margin-inline: auto; padding-inline: 16px; padding-block: 20px 32px; display: flex; flex-direction: column; gap: 14px }
header { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap }
h1 { font-family: var(--display); font-weight: 700; letter-spacing: -0.02em; font-size: clamp(22px, 3vw, 30px); margin: 0 }
.eyebrow { font-family: var(--mono); font-weight: 500; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent) }
.stage { position: relative; aspect-ratio: 16 / 9; max-width: 100%; background: #FFFFFF; border: 1px solid var(--line); overflow: hidden; touch-action: pan-y }
.stage img { display: block; width: 100%; height: 100%; object-fit: contain }
.stage .hit { position: absolute; top: 0; bottom: 0; width: 30%; background: none; border: 0; cursor: pointer }
.stage .hit.prev { left: 0 } .stage .hit.next { right: 0 }
.stage:fullscreen { border: 0; background: #FFFFFF }
.bar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap }
.bar .spacer { flex: 1 }
.count { font-family: var(--mono); font-weight: 500; font-size: 14px; letter-spacing: 0.06em; font-variant-numeric: tabular-nums; color: var(--muted); min-width: 7ch }
.title { font-family: var(--body); font-weight: 500; font-size: 15px }
button.ctl { font-family: var(--mono); font-weight: 500; font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink); background: var(--surface); border: 1px solid var(--line); padding: 8px 12px; cursor: pointer }
button.ctl:hover { border-color: var(--ink) }
button.ctl[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--on-accent) }
button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }
.notes { background: var(--surface); border-left: 4px solid var(--accent); padding: 16px 20px; font-size: 16px; line-height: 1.6; max-width: 75ch }
.notes .eyebrow { display: block; margin-bottom: 6px }
.strip { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 6px; scroll-snap-type: x proximity; -webkit-mask-image: linear-gradient(to right, #000 calc(100% - 48px), transparent); mask-image: linear-gradient(to right, #000 calc(100% - 48px), transparent) }
.thumb { flex: 0 0 calc((100% - 70px) / 8); min-width: 132px; scroll-snap-align: start; display: flex; flex-direction: column; gap: 6px; background: none; border: 0; padding: 0; cursor: pointer; text-align: left; color: var(--muted) }
.thumb img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border: 2px solid var(--line); background: #FFFFFF }
.thumb span { font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis }
.thumb[aria-current="true"] img { border-color: var(--accent) }
.thumb[aria-current="true"] span { color: var(--ink) }
.hint { font-size: 13px; color: var(--muted) }
#slidesBtn, .eyebrow .short { display: none }
/* Phone: full-width stage, short eyebrow, 48px controls on one row, every slide as a 3-up grid below. */
@media (max-width: 600px) {
  .wrap { padding-block: 12px 24px; gap: 12px }
  .stage { margin-inline: -16px; max-width: none; border-inline: 0 }
  .eyebrow .long, .hint, .bar .spacer { display: none }
  .eyebrow .short { display: inline }
  .bar { display: grid; grid-template-columns: 1fr 1fr auto; gap: 8px }
  .bar .count { grid-column: 3; grid-row: 1; align-self: center; text-align: right }
  .bar .title { grid-column: 1 / -1; font-size: 14px }
  button.ctl { min-height: 48px; padding: 8px 10px }
  #prev { grid-column: 1; grid-row: 1 } #next { grid-column: 2; grid-row: 1 }
  .strip { display: grid; grid-template-columns: repeat(3, 1fr); overflow: visible; -webkit-mask-image: none; mask-image: none }
  .thumb { flex: none; min-width: 0 }
  .thumb span { font-size: 10px }
}
</style>
<div class="wrap">
  <header>
    <div><div class="eyebrow"><span class="long">eMerge Hackathon · Sylvester healthcare track</span><span class="short">eMerge · Sylvester track</span></div><h1>Survivorship 360</h1></div>
    <div class="hint">← → to move · F for full screen · N for speaker notes · updated __STAMP__</div>
  </header>
  <div class="stage" id="stage">
    <img id="slide" src="slides/01.png" alt="">
    <button class="hit prev" id="hitPrev" aria-label="Previous slide"></button>
    <button class="hit next" id="hitNext" aria-label="Next slide"></button>
  </div>
  <div class="bar">
    <button class="ctl" id="prev">Prev</button>
    <button class="ctl" id="next">Next</button>
    <span class="count" id="count">01 / 11</span>
    <span class="title" id="title"></span>
    <span class="spacer"></span>
    <button class="ctl" id="notesBtn" aria-pressed="false">Notes</button>
    <button class="ctl" id="fsBtn">Full screen</button>
    <button class="ctl" id="slidesBtn" aria-pressed="false" aria-controls="strip">Slides</button>
  </div>
  <div class="notes" id="notes" hidden><span class="eyebrow">Speaker notes</span><span id="notesText"></span></div>
  <nav class="strip" id="strip" aria-label="All slides">
__THUMBS__
  </nav>
</div>
<script>
const SLIDES = __DATA__;
const $ = id => document.getElementById(id);
const pad = n => String(n).padStart(2, "0");
let i = 0;
SLIDES.forEach(s => { const im = new Image(); im.src = `slides/${pad(s.n)}.png`; });
function show(n) {
  i = Math.max(0, Math.min(SLIDES.length - 1, n));
  const s = SLIDES[i];
  $("slide").src = `slides/${pad(s.n)}.png`;
  $("slide").alt = `Slide ${s.n}: ${s.name}`;
  $("count").textContent = `${pad(s.n)} / ${pad(SLIDES.length)}`;
  $("title").textContent = s.name;
  $("notesText").textContent = s.notes;
  document.querySelectorAll(".thumb").forEach((t, k) => {
    t.setAttribute("aria-current", k === i ? "true" : "false");
    if (k === i) t.scrollIntoView({ block: "nearest", inline: "nearest" });
  });
  try { history.replaceState(null, "", "#" + s.n); } catch (e) {}
}
function toggleNotes() {
  const on = $("notes").hidden;
  $("notes").hidden = !on;
  $("notesBtn").setAttribute("aria-pressed", on ? "true" : "false");
}
function fullscreen() {
  const st = $("stage");
  if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
  else if (st.requestFullscreen) st.requestFullscreen().catch(() => {});
}
$("prev").onclick = $("hitPrev").onclick = () => show(i - 1);
$("next").onclick = $("hitNext").onclick = () => show(i + 1);
$("notesBtn").onclick = toggleNotes;
$("fsBtn").onclick = fullscreen;
$("slidesBtn").onclick = () => { const on = $("strip").classList.toggle("open"); $("slidesBtn").setAttribute("aria-pressed", on ? "true" : "false"); };
document.querySelectorAll(".thumb").forEach(t => t.onclick = () => show(+t.dataset.i));
document.addEventListener("keydown", e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); show(i + 1); }
  else if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(i - 1); }
  else if (e.key === "Home") show(0);
  else if (e.key === "End") show(SLIDES.length - 1);
  else if (e.key === "n" || e.key === "N") toggleNotes();
  else if (e.key === "f" || e.key === "F") fullscreen();
});
let x0 = null;
$("stage").addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
$("stage").addEventListener("touchend", e => {
  if (x0 === null) return;
  const dx = e.changedTouches[0].clientX - x0; x0 = null;
  if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
});
const start = parseInt((location.hash || "").slice(1), 10);
show(Number.isFinite(start) ? start - 1 : 0);
</script>
"""
stamp = datetime.datetime.now().astimezone().strftime("%b %-d, %-I:%M %p %Z")
page = page.replace("__STAMP__", stamp).replace("__THUMBS__", thumbs).replace("__DATA__", json.dumps(data))
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
# Serve the page as UTF-8 so the · and → separators never render as mojibake.
open(os.path.join(out, "_headers"), "w").write("/\n  Content-Type: text/html; charset=utf-8\n/index.html\n  Content-Type: text/html; charset=utf-8\n")
print(f"wrote {out}/index.html and {len(data)} slides")
