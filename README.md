# True Crime Video Producer

A reusable Manus skill and production starter kit for ethical, source-grounded true-crime YouTube videos. It guides the creator through format and duration intake, a topic shortlist with story summaries, case research, script approval, narration, visual planning, production and quality checks.

## What is included

- `true-crime-video-producer/SKILL.md` — the installable Manus skill and complete staged workflow.
- `docs/REFERENCE_STYLE.md` — a production design brief derived from analysis of the creator-provided YouTube reference.
- `docs/ETHICS_AND_FACT_CHECK.md` — sourcing, attribution, privacy and factuality standards.
- `docs/WORKFLOW.md` — step-by-step operator guide and output checklist.
- `demo/` — an original fictional case concept and storyboard for a one-minute style demonstration.
- `starter/` — local intake utility that saves a production brief without uploading data.

## Install the skill

In Manus, add the skill from `true-crime-video-producer/SKILL.md` (or the `.skill` archive supplied with the project). Start a request such as: “Use True Crime Video Producer for a 45-second Persian Short about a well-documented historical case.” The skill asks about format and duration, offers several topic ideas with short summaries, and waits for your topic choice before researching and scripting.

To run the local intake scaffold, use Python 3:

```bash
python3 starter/intake.py
```

This is a local project organizer, not a standalone AI video editor. It writes an intake brief and production folder; video generation, research, and editing depend on the tools available in your Manus session or your own media software. It does not upload your answers or request a GitHub token.

## Reference-inspired look

The reference analysis informed a general visual direction—cinematic dossier graphics, archival textures, restrained red evidence marks, concise file/date labels, rapid but readable visual changes, and deliberate sound design. The project does not copy the reference video's footage, narration, exact edit, or branded assets.

## Important safety and quality note

A topic's “viral potential” is a creative hypothesis, not a guarantee. True-crime material must be source-grounded, careful with victims and surviving family, and neutral around unresolved allegations. Generated reconstructions must not be presented as authentic evidence.

## Video length

Use the actual capabilities available in your session. Some generation tools only create short clips; a full one-minute video may need a narration-timed edit using multiple permitted visual elements and motion graphics. Do not stretch one short generated shot and describe it as a complete documentary.

## Security

Never put personal access tokens, API keys, credentials, or private case information in source control. If a token was exposed, revoke it and create a replacement through the provider's secure authorization flow. No credentials are included in this repository.

## License

MIT; see `LICENSE`.
