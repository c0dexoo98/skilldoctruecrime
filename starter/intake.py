#!/usr/bin/env python3
"""Create a private local production brief; does not call a service or upload data."""
from datetime import datetime, timezone
from pathlib import Path
import json
import re


def ask(label, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def safe_slug(text):
    slug = re.sub(r"[^a-zA-Z0-9\u0600-\u06FF]+", "-", text.strip()).strip("-")
    return slug[:64] or "new-case"


def main():
    print("True Crime Video Producer — local intake (answers stay on this computer)\n")
    title = ask("Working title or case theme", "New case")
    language = ask("Narration language", "Persian")
    format_kind = ask("Format (Short / long-form)", "Short")
    duration = ask("Target duration (e.g. 45 seconds / 12 minutes)", "60 seconds")
    ratio = ask("Aspect ratio", "9:16" if format_kind.lower().startswith("s") else "16:9")
    audience = ask("Audience / region", "General YouTube audience")
    focus = ask("Preferred themes, tone, or case status", "Evidence-led, respectful, resolved cases")
    voice = ask("Narration plan (recorded / synthesize later)", "Recorded by creator")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    project = Path("projects") / f"{safe_slug(title)}-{stamp}"
    project.mkdir(parents=True, exist_ok=False)
    data = {
        "title": title, "language": language, "format": format_kind,
        "duration": duration, "aspect_ratio": ratio, "audience": audience,
        "creative_preferences": focus, "narration_plan": voice,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "intake_complete_topic_selection_pending",
        "privacy": "Stored locally. No network requests are made by this utility."
    }
    (project / "brief.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (project / "NEXT_STEPS.md").write_text(
        "# Next steps\n\n"
        "1. Open the `true-crime-video-producer` skill in Manus and provide the intake brief.\n"
        "2. Request 5–8 topic candidates with hooks, short story summaries, format fit, and sourceability.\n"
        "3. Choose one topic. Research sources and approve a sourced script before producing.\n"
        "4. Put narration and licensed/source-cleared assets in this project folder; never add credentials.\n\n"
        "This local utility does not generate research, narration, or video.\n", encoding="utf-8")
    print(f"\nBrief saved locally: {project / 'brief.json'}")
    print("No network calls were made. Follow NEXT_STEPS.md to continue with the Manus skill.")


if __name__ == "__main__":
    main()
