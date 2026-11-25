# Procedural continuous-world renderer

A deterministic Pillow-to-FFmpeg starter for one persistent, code-drawn world and one smooth camera journey. It does not call an AI video generator, use stock footage, create cuts/slides, or download assets. Every frame is composed by code. Creator-approved photographs can be inserted only as flat physical print cards, with source and rights metadata in the project JSON; the template itself contains no user or legacy images.

## Requirements

Python 3.10+, Pillow, NumPy, FFmpeg with `libx264`, and `ffprobe` on `PATH`. No network access or external service is used.

```sh
python3 -m pip install Pillow numpy
python3 render.py project.template.json --dry-run
```

Copy and edit the JSON for a real production, add newly approved photographs under that project folder, and set `voiceover` to the new narration path. Do not copy previous-project assets when the creator has requested an asset reset. The renderer measures voice duration and refuses a mismatched configured duration instead of silently shortening or speeding the narration.

```sh
python3 render.py project.json -o output/final.mp4 --provenance output/final.provenance.json
```

`voiceover: null` is only for silent code-render smoke tests/previews; it is not a finished narration-led delivery. The default template is 1280×720, 24fps, 12 seconds. Configure width, height, fps, and measured duration explicitly for each project.

## Project JSON

`camera_waypoints` use `{at, value:[world_x, world_y, zoom, rotation_degrees]}` and must span time zero through full duration. Time-domain cubic Hermite interpolation shares tangents at knots; a small `camera_drift` persists through holds. `beats` are `{start,end,hero,text}`; every hero ID must refer to one object. Set `text.channel` to exactly one of `none`, `overlay`, or `document`; the validator rejects repeated visible phrases. Do not duplicate a phrase in image/document text and a typeset overlay/caption.

`objects` may be code-drawn `circle`, `box`, `pin`, or `route` shapes. A photo object has an `image` path, `pos`, `size`, `rotation`, and `provenance` fields such as `source`, `rights`, and `status`; it is rendered as a paper-backed print with a natural shadow, never as a moving clip. Keep real photos unaltered except for fit/placement and disclose illustrative/reconstruction status.

The output `.provenance.json` records the project config hash, frame dimensions/fps/count, voice duration, photo paths/hashes and supplied source/rights metadata. It is a local project file; do not publish private project manifests or photos in the generic public plugin repository.

## Render and inspect

The renderer streams RGB frames to FFmpeg and writes H.264 MP4, plus a provenance manifest. It supports subtle deterministic handheld drift, speed-scaled frame-blend motion blur, optional grain/glow/vignette, physical print cards, per-beat hero dimming, and timed route strokes. Review the beat table first, then contact sheets from every beat and short camera sequences before the full export. Confirm the camera never resets or stops, each line has one hero, screen text is not duplicated, and the MP4 matches the voice and requested format.
