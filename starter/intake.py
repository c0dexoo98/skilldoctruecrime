#!/usr/bin/env python3
"""Create a private local brief for code-rendered continuous-world video; no network calls."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import re


def ask(label, default=""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def safe_slug(text):
    slug = re.sub(r"[^a-zA-Z0-9\u0600-\u06FF]+", "-", text.strip()).strip("-")
    return slug[:64] or "new-project"


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    print("True Crime Video Producer — continuous-world intake (answers stay local)\n")
    title = ask("Project title", "New case")
    language = ask("Narration language", "Persian")
    story_status = ask("Story status (factual / fictional / reconstruction)", "Fictional")
    format_kind = ask("Format (Short / long-form)", "Short")
    duration = ask("Target duration or measured voice duration", "Awaiting voice file")
    ratio = ask("Aspect ratio", "21:9 (confirm exact dimensions)")
    resolution = ask("Resolution", "3840x1646 (confirm before render)")
    fps = ask("Frame rate", "30 (confirm before render)")
    script = ask("Approved script path or status", "Not provided")
    voice = ask("New narration file path or status", "Not provided")
    photos = ask("New approved photo directory or status", "Not provided")
    provenance = ask("Photo rights/provenance notes", "Must be confirmed")
    references = ask("Style reference path(s) or status", "Text brief only")
    asset_rule = ask("Reuse rule", "New project assets only; do not reuse prior assets")
    output = ask("Output path", "output/final.mp4")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    project = Path("projects") / f"{safe_slug(title)}-{stamp}"
    project.mkdir(parents=True, exist_ok=False)
    brief = {
        "title": title,
        "language": language,
        "story_status": story_status,
        "format": format_kind,
        "duration_or_voice_duration": duration,
        "aspect_ratio": ratio,
        "resolution": resolution,
        "fps": fps,
        "approved_script": script,
        "new_voiceover": voice,
        "new_photo_assets": photos,
        "photo_rights_and_provenance": provenance,
        "style_references": references,
        "asset_reuse_rule": asset_rule,
        "hard_video_rules": {
            "all_frames_code_rendered": True,
            "ai_video_generator": False,
            "stock_footage": False,
            "cuts_or_slide_changes": False,
            "single_continuous_world_and_camera": True
        },
        "output_path": output,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "intake_only_beat_table_pending",
        "privacy": "Stored locally; this utility makes no network calls."
    }
    (project / "brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (project / "NEXT_STEPS.md").write_text(
        "# Next steps\n\n"
        "1. Supply the approved script, a new narration file, new approved photos, and provenance/rights notes.\n"
        "2. Measure the narration and align every line/action to actual audio time.\n"
        "3. Fill `starter/EDIT_PLAN_TEMPLATE.md` and show the beat table for creator approval before code/render.\n"
        "4. Build one persistent world and one smooth, uninterrupted camera path.\n"
        "5. Render every frame deterministically with code; never use AI video, stock footage, cuts, or slide changes.\n"
        "6. Inspect a still for every beat and camera sequences before full export.\n"
        "7. Verify exact format, duration, audio sync, full-file decoding, and the private asset manifest.\n\n"
        "This local intake utility neither uploads assets nor creates a finished video.\n", encoding="utf-8")
    print(f"\nBrief saved locally: {project / 'brief.json'}")
    print("No network calls were made. Provide the missing assets before any project-specific render.")


if __name__ == "__main__":
    main()
