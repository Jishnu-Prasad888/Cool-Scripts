#!/usr/bin/env python3

import sys
from pathlib import Path


def clean_md_file(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    # Read everything before writing, so input and output can be the same file.
    lines = input_path.read_text(encoding="utf-8").splitlines()

    cleaned = []
    previous = None

    for line in lines:
        normalized = line.strip()

        # Remove consecutive duplicate non-empty lines.
        if normalized and normalized == previous:
            continue

        cleaned.append(line)

        # Blank lines reset duplicate detection.
        previous = normalized if normalized else None

    output_path.write_text(
        "\n".join(cleaned) + "\n",
        encoding="utf-8"
    )

    print(f"Cleaned: {input_path}")
    print(f"Output:  {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} INPUT.md OUTPUT.md")
        sys.exit(1)

    clean_md_file(sys.argv[1], sys.argv[2])
