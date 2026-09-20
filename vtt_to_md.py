import re
import sys
from pathlib import Path


def vtt_to_markdown(vtt_path, md_path):
    text = Path(vtt_path).read_text(encoding="utf-8")

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = text.split("\n")
    output = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip WEBVTT header
        if line.startswith("WEBVTT"):
            continue

        # Skip NOTE, STYLE, and REGION blocks
        if line.startswith(("NOTE", "STYLE", "REGION")):
            continue

        # Skip cue numbers
        if re.fullmatch(r"\d+", line):
            continue

        # Skip timestamp lines
        if "-->" in line:
            continue

        # Remove VTT tags such as <c>, <i>, <b>, <u>, etc.
        line = re.sub(r"<[^>]+>", "", line)

        # Decode common HTML entities
        line = (
            line.replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&nbsp;", " ")
                .replace("&quot;", '"')
                .replace("&#39;", "'")
        )

        if line:
            output.append(line)

    # Join subtitle lines into paragraphs
    markdown = "\n\n".join(output)

    Path(md_path).write_text(markdown + "\n", encoding="utf-8")
    print(f"Converted: {vtt_path} -> {md_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vtt_to_markdown.py input.vtt output.md")
        sys.exit(1)

    vtt_to_markdown(sys.argv[1], sys.argv[2])
