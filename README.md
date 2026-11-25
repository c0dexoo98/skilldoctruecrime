# True Crime Video Producer

A reusable Manus skill and production starter kit for ethical, source-grounded true-crime YouTube videos. It guides a creator through format and duration intake, topic pitches with story summaries, case research, script approval, narration, visual planning, motion design, sound and quality checks.

## What is included

- `true-crime-video-producer/SKILL.md` — installable Manus skill and staged workflow.
- `true-crime-video-producer/references/still-image-editing.md` — still-image-only documentary editing, motion, red-pencil reveals, sound and QA guidance.
- `docs/REFERENCE_STYLE.md` — original reference-inspired visual direction, without copying branded assets or exact edits.
- `docs/ETHICS_AND_FACT_CHECK.md` — sourcing, attribution, privacy and factuality standards.
- `docs/WORKFLOW.md` — operator workflow and output checklist.
- `demo/` — fictional case concept, sample narration and a still-image-only storyboard.
- `starter/intake.py` — local intake utility that records visual-source mode, motion energy and sound-design preferences without uploading data.
- `starter/EDIT_PLAN_TEMPLATE.md` — reusable beat map, image provenance, transition, Foley and final-QA template.

## Install the skill

In Manus, add the skill from `true-crime-video-producer/SKILL.md` (or the `.skill` archive supplied with the project). Start a request such as: “Use True Crime Video Producer for a 45-second Persian Short about a well-documented historical case.” The skill asks about format, duration and picture-source constraints, offers several topic ideas with short summaries, and waits for your topic choice before researching and scripting.

To run the local intake scaffold, use Python 3:

```bash
python3 starter/intake.py
```

This local project organizer does not call an AI service or upload your answers. It records whether the edit is still-image-only, the desired motion energy and sound-design density. Research, image generation, sound and editing depend on tools available in the Manus session or your own media software.

## Still-image-only motion workflow

When requested, the final video can be assembled entirely from photographs, generated stills, original diagrams, titles and programmatic motion graphics—without video footage or generated video clips. The edit can animate map pans, parallax, zoom-outs, paper wipes, match cuts, red pencil underlines/circles and clue connections on an evidence board. A final MP4 made from moving stills is not the same as using video clips as source material.

Keep narration foremost. Use a restrained score and cue Foley—paper, pencil, pins, mechanical clicks and whooshes—only when it reinforces a visible action. Do not let transitions overwhelm factual clarity or captions.

## Reference-inspired look

The art direction uses cinematic dossier graphics, archival textures, muted teal/charcoal shadows, warm practical light, restrained red marks, concise file/date labels and deliberate sound design. It aims for original premium documentary quality without copying a specific service, show, creator, footage or edit.

## Safety and quality

A topic's “viral potential” is a creative hypothesis, not a guarantee. Treat victims and families respectfully; stay neutral around unresolved allegations; keep a source ledger; distinguish verified sources from illustrative/generated assets. Never present generated reconstructions as authentic evidence. In a fictional story, label the story and props as fictional throughout.

Match final duration to the actual narration unless the creator authorizes trimming or speed changes. A still-image-only request forbids footage and video clips; verify this source constraint during final QA.

## Security

Never put personal access tokens, API keys, credentials or private case information in source control. If a token was exposed, revoke it and create a replacement through the provider's secure authorization flow. No credentials or private narration are included in this repository.

## License

MIT; see `LICENSE`.
