# Production workflow — Continuous World

This project mode creates a narration-led motion film from deterministic code-rendered frames over one persistent world. It is not a slideshow, clip edit, stock-footage montage, or AI-video generation workflow.

1. **Intake and isolation:** record project language, factual/fictional status, script, measured narration, exact output format, approved photo/reference assets, provenance/rights, and privacy limits. When the creator says to forget old assets, do not copy them into the new project.
2. **Case research (factual cases only):** present 5–8 candidates, wait for selection, research from primary records and reputable corroboration, and maintain a claim/source ledger. Avoid unsupported allegations and label uncertainty.
3. **Script approval:** prepare the narration script and get creator approval before production. Do not invent dialogue, evidence or quotations.
4. **Audio lock:** inspect the approved audio and measure duration, channels and sample rate. Align lines/important words to actual audio. Keep the original file unchanged; no trimming or speed changes without approval.
5. **Beat table:** before project-specific rendering, show one row per narration line with timestamps, verbatim words, one hero, one text channel, a word-timed action, camera waypoint, dim/focus plan and sound cue. Ask the creator to confirm or clarify. No final render before approval.
6. **One-world layout:** establish a coordinate system, prop placements and an uninterrupted camera route. Treat approved photos as printed physical objects in that world. All other surfaces, shadows, labels, motion and final frames are produced with code.
7. **Code-only render:** render frames deterministically with Canvas/WebGL or a code compositor and encode them with FFmpeg. Never call an AI video generator; never use stock footage, downloaded clips, cuts, slide changes or reset transitions. Keep the camera moving gently through holds; use smooth splines, subtle handheld motion, speed-driven blur, restrained grain/glow/vignette.
8. **Typography and focus:** give each line one hero. Dim non-hero elements. Show a narrated phrase at most once on screen—on a document, as typeset text, or in captions, never duplicated across channels. Avoid filler text and tiny copy; favor one-second phone readability.
9. **Pre-render review:** inspect a still for every beat and short sequences around camera waypoints. Fix clutter, text overlaps, jerks, dead stops, accidental cuts, unreadable type and inconsistent prop continuity before full export.
10. **Sound and final QA:** preserve the narration, add only approved, story-motivated music/Foley, and check sync/peaks. Use `ffprobe`; verify exact format and duration against the narration; decode the full MP4; inspect all beats and the beginning/end.
11. **Delivery/privacy:** deliver MP4, approved script, beat table, provenance manifest and source code. Never publish private narration, user photos, tokens or project-specific private material in the public plugin repository.

## Gate conditions

Do not render until the creator approves the script, actual narration timing, beat table, input assets/rights, and output format. If an input is missing, make that explicit and request it; do not silently reuse old assets or make a finished-video claim. No AI video generation, no stock footage, no cuts, and no slide replacement in continuous-world mode.
