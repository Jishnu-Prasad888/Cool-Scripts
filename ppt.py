
import subprocess
from pathlib import Path

folder = Path.cwd()
output_dir = folder / "pdfs"
output_dir.mkdir(exist_ok=True)

extensions = {".ppt", ".pptx", ".pptm"}

files = [
    f for f in folder.iterdir()
    if f.is_file() and f.suffix.lower() in extensions
]

if not files:
    print("No PowerPoint files found.")
    exit()

for file in files:
    print(f"Converting: {file.name}")

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(file)
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"  Done: {file.stem}.pdf")
    else:
        print(f"  Failed: {result.stderr}")

print(f"\nFinished. PDFs saved in: {output_dir}")
