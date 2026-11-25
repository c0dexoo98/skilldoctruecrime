# Continuous-world code rendering

Read this reference for a narration-led video that must stay inside one persistent world and use no AI-generated video, stock footage, cuts, or slide changes.

## Inputs and lock file

Before coding, lock the exact script, measured voice duration, line/word timings, frame size, aspect ratio, fps, codec, approved photographs, photo rights/provenance, references, caption policy, and private/public boundary. Do not automatically reuse assets from another project. Keep the voice untouched and make it the timing authority.

Create a project JSON and a beat table. The table has one row per spoken line and records verbatim text, start/end time, one hero object, the single text channel (document, typeset, captions, or none), the exact spoken-word action, the world-space camera waypoint, dimming/focus, and sound cue. Ask the creator to approve the table and output format before building the final world or running a full render.

## Render architecture

The bundled Python starter is `scripts/continuous-world/render.py`; its editable example is `templates/continuous-world/project.template.json`. It requires Python 3.10+, Pillow, NumPy, FFmpeg with `libx264`, and `ffprobe`. Install Pillow/NumPy with `python3 -m pip install Pillow numpy`. From the skill directory, validate with `python3 scripts/continuous-world/render.py templates/continuous-world/project.template.json --dry-run`; for a real project, copy/edit the template and run `python3 scripts/continuous-world/render.py project.json -o output/final.mp4 --provenance output/final.provenance.json`. The standalone intake helper is `scripts/intake.py`; it writes local files only.

The compositor checks beat coverage, unique IDs, photo paths, text-channel uniqueness, camera waypoint continuity, and measured voice duration. It renders code-drawn shapes and user-approved photographs as physical print cards, and muxes the supplied narration at its original speed. It does not create topic ideas, research or fact-check a case, transcribe or word-align narration, generate subtitles, or mix music/SFX; those require separate, creator-approved steps. `voiceover: null` is only for silent previews, never for a finished narration-led deliverable.

Render all frames with deterministic code. Canvas/WebGL, SVG rendered per frame, or a Python/Pillow compositor are valid. A practical pipeline is:

1. Build a large 2D/2.5D world canvas with a consistent desk/map/board surface, world-space lighting, and named coordinates.
2. Place user-approved photographs as physical prints or papers. Preserve source pixels except for layout transforms that do not misrepresent a person/object. Record each file, rights, factual/illustrative status, and beat in a provenance manifest.
3. Add only story-required vector objects, text, shadows, paper edges, red marks, lighting, grain, vignette, and glow in code. Avoid readable filler copy, fabricated seals, random props, and duplicate text.
4. Define one camera path across the world for the entire narration. Sample that path at each exact frame time. Keep a single continuous world coordinate system and do not splice separate scenes.
5. Stream rendered RGB frames to FFmpeg or another deterministic encoder. Map the approved audio at its original speed and duration; apply only explicitly approved mixing/subtitle changes.

No AI video generator, stock clip, downloaded video, animated-video background, or cut-based assembly may enter this pipeline. A photo file is an image input, not a video source.

## Continuous camera path

Represent camera center, scale/zoom, rotation, and optionally depth/focus at timed waypoints. Interpolate with a cubic spline or another curve with continuous position and velocity; use bounded acceleration/jerk so the move eases naturally through beats. Do not ease to zero velocity at every line. Keep a low-amplitude forward drift during holds, and use a deterministic, low-frequency handheld term that cannot shift text off screen. Clamp camera limits to protect all hero objects and safe areas.

Apply motion blur only when camera/object velocity exceeds a threshold, with strength proportional to speed. Use grain, soft glow, vignette and lens softness as stable subtle treatments rather than per-beat flashes. Keep the camera's orientation and desk lighting consistent. A paper may drop, slide or rotate as a physical object, but no movement may disguise a camera reset or hard cut.

## One-line, one-hero, one-text-channel

For each narration line, choose exactly one hero. Reduce brightness/contrast or apply a restrained depth-of-field mask to non-heroes, without obscuring relevant context. The phrase's on-screen representation can occur in one location only: on the approved document/photo, as a typeset overlay, or in the caption channel. Do not repeat the same phrase in a prop and subtitle/title. If the creator wants accessibility captions, make captions the selected text channel for each phrase, or provide a separate optional subtitle track when requested.

Use exact wording only when approved. For fictional documents, show only the specific line that belongs to the beat; leave other copy as nonverbal soft-grey rules. For real cases, never fabricate a document or alter a source image to invent evidence. Make hero typography phone-readable in about one second. Remove any label, stamp, tape, card, prop, glow, or sound that does not help the current narration line.

## Audio synchronization

Use a supplied line/word timing map when available. Otherwise create a timestamped transcript and verify it against the audio; do not infer precise word timing from total duration or guessed syllable rates. Place a line reveal, circle, route stroke, paper drop or camera arrival on the actual spoken word. Keep foley short and perceptually subordinate. Preserve the full source voice unless the creator authorizes trimming or speed change. If video and audio sample/frame boundaries differ slightly, report the exact measured durations and never claim sample-perfect equality without verifying it.

## Pre-render review

Before a full render, export one still per beat and low-resolution sequences spanning every camera waypoint. Review at intended display size and phone size. Fix: multiple simultaneous heroes; text duplicated across channels; unreadable/overlapping text; background that competes instead of dimming; camera jerk, stop, overshoot, drift reversal, sudden scale jump, object teleport, hidden photo detail, fake document copy, or an accidental cut/reset. Check all coordinates against the actual aspect ratio.

## Final encoding and QA

Use the locked width, height, fps and container. Probe all inputs first. Encode to the requested codec; preserve narration start at zero and its full run. Check the output with `ffprobe`, render representative stills at every beat and transitions, inspect camera sequences, listen at normal speed, assess peaks/clipping, and decode the entire MP4. Confirm there is one video stream generated from code-rendered frames and the expected audio stream. Record output duration, frame count, dimensions, fps, codec, audio timing, and source manifest.

Deliver the MP4, editable renderer/project configuration, approved beat table, script/timing map, and provenance manifest. Keep project-specific private audio/photos outside the public plugin repository.
