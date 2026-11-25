# Still-image-only documentary edit

Read this reference whenever the creator forbids video footage, asks for images instead of clips, or wants a still-led motion-graphics documentary.

## Hard source boundary

When the request says still images only, use only still raster/vector images, titles, graphic shapes and code-authored animation as picture inputs. Do not generate, search for, download, reuse or insert video clips, stock footage or animated-video backgrounds. A final MP4 may still be rendered from still frames, but that does not authorize video-picture sources. Keep the original audio separate and unchanged unless the creator authorizes an audio edit.

Create an asset manifest with path, provenance, fictional/authentic status, permitted use and the beat it supports. Use creator-supplied or properly cleared stills for factual claims. For fictional cases, generate original props and label the story/props as fictional. Never fabricate a real person's document, official seal or evidence photo.

## Image sequence design

1. Lock aspect ratio, safe areas, palette, light, grain and lens language before generating the set. Keep repeatable anchors—e.g. paper color, red annotation, desk-light direction—across images.
2. Assign one image to one narrative job. Use a mix of wide scene setters, close details, maps, clue objects and a final board/reveal. Avoid asking an image model to render long exact copy; leave clear text-safe areas and typeset verified labels during editing.
3. Write a timestamped shot list. For every still, specify start crop, end crop, move direction, hold, transition-in/out, overlay animation, spoken beat and optional SFX.
4. Change the visual idea when information changes (often every 1–3 seconds), not just because a timer fires. Retain a stable hold for factual labels and captions.

## Motion grammar

Treat the still as a multi-layer scene. Use modest foreground/background separation and parallax when possible; never invent a clue, person or object with a motion mask. Vary push-in, pull-out, diagonal drift, detail-to-wide reframing, match-cut, paper/folder wipe, map pan, split-screen comparison, snap zoom and carefully controlled whip-pan. Make high-speed transitions brief and reserve them for reveals or narrative turns. Use motion blur or light leaks sparingly; preserve readable faces, maps, dates, labels and captions.

For pencil annotations, define vector paths in picture coordinates. Animate stroke reveal from the plausible pen-entry point to the endpoint; follow the pencil Foley timing. Use separate stroke layers for underline, circle, arrow and connection line. Avoid instant full-line appearance unless it is an intentional impact beat. On evidence boards, reveal a node first, then the line connecting it, then the next node; label relationships without claiming more than the sources support. A zoom-out can reveal the whole board after detail work, then ease to the final frame.

Transitions should communicate a real editorial relationship: paper movement between records, match shape/position between clues, a directional move to a new location, or a deliberate break in time. Use a coherent small transition vocabulary and rotate through it; do not chain elaborate effects on every beat. The effect should never obscure the narrator's key phrase or subtitles.

## Sound and mix

Build a cue sheet tied to picture time. Use distinct reusable assets for pencil/marker, paper/page/folder, soft pin/click, mechanical switch, ambience, whoosh and low impact. Place sound on the action frame, not on every cut. Keep transients below voice peaks and the score low under narration; duck the score around spoken content and key Foley. Leave intentional quiet. Avoid police-radio, gunshot, alarm or horror cues that could imply events not in evidence. Check stereo motion translates acceptably to mono and verify tails do not mask the next line.

## Tooling and QA

Render image-based compositions deterministically and time-driven. Keep source project, source images, fonts, cue sheet, generated effects, captions and render instructions together. Do not rely on remote CDN assets. Use streaming-friendly H.264/AAC for MP4 unless the user specifies another delivery format. Check `ffprobe` metadata, then decode the entire file; inspect the opening, every visual state/important transition, a stable reading hold and final end card. Confirm all picture inputs are stills/graphics, labels are clear, captions remain inside safe margins, the motion has deliberate endpoints and no audio clips or distorts.

## Deliverable checklist

- Final playable video and actual duration.
- Storyboard/beat map and still-asset manifest.
- Reusable render/edit sources and project dependencies when requested.
- Explicit note about generated imagery and reconstruction labels.
- No public upload of private narration or credentials unless the creator explicitly requests it.
