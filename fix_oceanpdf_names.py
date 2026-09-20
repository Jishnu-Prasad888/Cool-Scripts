#!/usr/bin/env python3

from pathlib import Path
import re

DOWNLOADS = Path.home() / "Downloads"

# Only rename these PDF patterns.
# Everything else in Downloads is left alone.
def clean_name(path: Path) -> str:
    name = path.stem

    # Remove OceanofPDF prefix
    name = re.sub(r"^_OceanofPDF\.com_", "", name, flags=re.I)

    # Convert separators to spaces
    name = name.replace("_", " ")

    # Normalize "Author - Title" / "Title - Author"
    name = re.sub(r"\s+", " ", name).strip()

    # Remove "(1)", "(2)", etc. from duplicate copies
    name = re.sub(r"\s+\(\d+\)$", "", name)

    return name + path.suffix.lower()


def main():
    for pdf in DOWNLOADS.glob("*.pdf"):
        # Only touch OceanofPDF files or obvious book PDFs.
        if (
            pdf.name.lower().startswith("_oceanofpdf.com_")
            or pdf.name in {
                "Slow_Horses_Deluxe_Edition-Mick_Herron.pdf",
                "Soldier Spy-Tom_Marcus.pdf",
            }
        ):
            new_name = clean_name(pdf)
            destination = pdf.with_name(new_name)

            # Don't overwrite an existing file
            if destination.exists() and destination != pdf:
                print(f"SKIP  {pdf.name!r} -> {destination.name!r} (already exists)")
                continue

            if destination != pdf:
                pdf.rename(destination)
                print(f"RENAMED  {pdf.name} -> {destination.name}")


if __name__ == "__main__":
    main()
