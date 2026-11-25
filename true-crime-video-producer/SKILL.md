---
name: true-crime-video-producer
description: Plan, research, and produce ethical true-crime videos as deterministic code-rendered continuous-world motion films. Use for topic pitches, sourced scripts, narration-led beat maps, and videos with one unbroken camera move over a designed world—no AI video generators, stock footage, cuts, or slides.
---

# True Crime Video Producer — Continuous World

Guide the creator from intake through a sourced script, an approved beat table, deterministic code-rendered motion, and final QA. For the continuous-world mode, every output frame must be rendered by code over one persistent world and one unbroken camera journey.

## Hard production contract

- Do not call an AI video generator. Do not source, download, or insert stock footage. Do not cut between clips, change slides, or fake continuity with dissolves.
- Render every frame deterministically from code (for example, Canvas/WebGL or a Python/Pillow pipeline). User-provided or permission-cleared photographs may be composited as physical prints/documents/objects in the coded world; track their provenance. A photo is an input layer, not a video clip.
- Do not silently reuse prior-project audio, images, documents, or style references after the creator says to forget/replace them. Treat each project as asset-isolated unless reuse is explicitly authorized.
- Never make generated or illustrative material look like real evidence. For fictional cases, identify the story as fictional in a concise, readable way. Never invent real-case documents, seals, quotes, evidence, or facts.
- Preserve approved narration verbatim and at its recorded speed/duration unless the creator explicitly authorizes a change.

## 1. Intake and missing-input gate

Capture language, platform, short/long format, exact aspect ratio, resolution, frame rate, target runtime, factual/fictional status, script, recorded narration, approved photos, style references, music/SFX preferences, and publication destination. Ask only for details that block a correct plan or render.

Measure the supplied voice file with media tools before planning. Inspect duration, sample rate, channels, and clarity. Use supplied line timestamps or create a timestamped transcript/forced alignment; mark uncertain boundaries instead of guessing. Keep the original voice file untouched.

If a required input is missing, do not fabricate it or substitute an old project asset. Continue only with independent work (such as a reusable template or a provisional beat map from an approved script), then request the missing file/details before rendering. Do not describe placeholders as attached or received assets.

For case topics, proceed in order: offer 5–8 distinct candidates with a hook, 2–4 sentence summary, cautious audience-interest hypothesis, likely format fit, and sourceability; wait for topic selection; research the selected case from primary sources and reputable corroboration; maintain a claim/source ledger; then draft and obtain script approval. Attribute allegations, state research date, preserve uncertainty, avoid victim exploitation and unnecessary personal details.

## 2. Beat table before code

Before building the world or writing project-specific renderer code, show a beat table and ask the creator to confirm it or clarify blockers. Use one row per spoken line/idea:

| Start–end | Verbatim narration | One hero object/word | Text channel (document OR typeset OR none) | Word-timed action | Continuous camera waypoint | Dim/focus plan | Sound cue |
|---|---|---|---|---|---|---|---|

The table must account for the complete narration and exact runtime. Each beat has exactly one visual hero. Dim secondary objects while that hero carries the line. At each beat, choose at most one on-screen representation of the narrated phrase: physical text on a real/approved document, typeset text, or no text. Never duplicate the same phrase as document copy plus overlay/subtitle. Do not add filler labels or unreadable fake body copy; use soft grey nonverbal lines only when paper texture needs them. Keep hero type phone-readable in about one second. Mark important actions against the actual spoken word, not just the music beat.

When the table is unclear, ask before production. Do not proceed to the final renderer until the creator approves the table and the output format.

## 3. Design one persistent world

Choose one coherent stage that fits the story (desk, map, board, archive table). Establish a single world coordinate system and place all photos/objects on it as physical prints or papers. Keep the world present for the entire piece; never use a cut, slide change, scene replacement, or transition that resets the camera.

Create one continuous camera path through the world. Interpolate position, scale/zoom, rotation, and focus with a smooth spline/easing curve whose position and velocity do not jump at beat boundaries. The camera glides toward each next waypoint during holds; it must not stop dead. Add only subtle deterministic handheld drift. Use motion blur only as a function of camera speed; keep grain, glow, and vignette restrained and stable. Physical paper can enter by sliding, dropping, rotating, or unfolding with coherent shadows, but it must remain part of the same world and camera move.

## 4. Readability and visual hierarchy

For each narrated line, promote exactly one hero and dim the rest of the world. Keep one focal point; remove decorative clutter that has no story job. Use large, high-contrast text only when chosen as that beat's sole text channel. Do not render long paragraphs, fake documents, repeated wording, decorative stamps, random tape, or tiny labels. Preserve truthful photo details; do not alter a real person's face or a real document to imply facts not present in the source.

Keep every text object anchored in world space or explicitly identified as a screen-space overlay. Do not let object edges, subtitles, toolbars, or camera movement crop critical text. Ask whether captions are required; if they are, subtitles become the selected text channel for those phrases, not a second copy on a prop.

## 5. Code rendering and sound

Use a deterministic code pipeline for every frame. Appropriate approaches include a time-addressable HTML Canvas/WebGL scene or a Python image-compositing renderer that samples the same continuous camera path at exact frame times. Feed the numbered frames to FFmpeg for the requested codec/container. Do not render or insert AI-generated video, downloaded clips, stock loops, or prerecorded animated backgrounds.

For a local starter, use `scripts/continuous-world/render.py` with `templates/continuous-world/project.template.json`; install Pillow, NumPy, and FFmpeg first. `scripts/intake.py` creates a local-only brief. The bundled compositor renders primitives, approved photo prints, a continuous camera path, text and the supplied voice track; it does not research cases, transcribe/align narration, generate topic ideas, or mix music/SFX. Complete and approve those steps separately. Consult `references/continuous-world-code-rendering.md` for its schema and limitations.

Keep a manifest of every input image/audio file, creator/license, provenance, factual or illustrative status, and beat use. Use only supplied or permission-cleared photographs unless the creator explicitly authorizes another static-asset source. Never place private narration, credentials, or project photos in the public plugin repository.

Time pencil circles, route strokes, paper drops, reveals, and sound cues to supplied word-level timings where possible. Keep the narration intelligible and foremost. Avoid loud, misleading SFX; never imply an unverified event. Preserve the original narration as a separate source. Mix only as authorized, with a restrained score, clear headroom, and optional side-chain ducking.

## 6. Pre-render review and final QA

Before a full render, inspect at least one still at every beat and contact sheets/sequences across every camera transition. Check the same persistent world, camera direction, smooth acceleration/deceleration, no dead stops, no jumps/cuts, one hero per line, secondary dimming, text uniqueness, phone-size readability, unobstructed evidence, natural object shadows, and absence of clutter. Fix problems before full-resolution export.

After rendering, use `ffprobe` to verify exact dimensions, frame rate, duration, audio streams, codec, and start/end timing. Confirm video length matches the narration to the requested frame/sample tolerance without silently trimming or speeding the voice. Decode the entire MP4, inspect beginning/middle/end and every beat, listen to representative sound transitions, check clipping/peaks, and verify the manifest accounts for all media inputs. State honestly when only still frames/graphics—not footage—were used.

Deliver the final MP4, approved script, beat table/storyboard, asset manifest, and reusable code project. Keep private assets out of the public GitHub repository; publish only generic skill/plugin code and documentation when requested.

## Conversation order

1. Intake and asset/rights check.
2. Topic slate and creator selection (for researched cases).
3. Sourced research, script, and approval.
4. Narration inspection and exact timing.
5. Beat table and creator confirmation.
6. Continuous-world layout and code-render plan.
7. Pre-render still/sequence review and corrections.
8. Full deterministic render and mix.
9. Technical, visual, factual, and privacy QA.
10. Deliver MP4 and reusable source package.

Read `references/continuous-world-code-rendering.md` for implementation details and `references/ETHICS_AND_FACT_CHECK.md` for factual-case standards.
