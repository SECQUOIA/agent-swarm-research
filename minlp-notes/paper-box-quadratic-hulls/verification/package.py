"""Create the two submission archives from the completed local artifacts."""

from hashlib import sha256
from pathlib import Path
import json
from zipfile import ZIP_DEFLATED, ZipFile


paper = Path(__file__).resolve().parents[1]
source_names = ["main.tex", "macros.tex", "references.bib", "main.bbl"]
source_files = [paper / name for name in source_names]
source_files += sorted((paper / "sections").glob("*.tex"))
source_files += sorted((paper / "appendices").glob("*.tex"))
source_files += sorted((paper / "figures").glob("*.pdf"))
source_files += sorted((paper / "figures").glob("*.py"))

with ZipFile(paper / "submission-source.zip", "w", ZIP_DEFLATED) as archive:
    for path in source_files:
        archive.write(path, path.relative_to(paper).as_posix())
    archive.write(paper / "SUBMISSION.md", "README.md")

companion_files = sorted(
    path for path in (paper / "companion").rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
)
with ZipFile(paper / "companion.zip", "w", ZIP_DEFLATED) as archive:
    for path in companion_files:
        archive.write(path, path.relative_to(paper).as_posix())

manifest = {}
for name in ("main.pdf", "submission-source.zip", "companion.zip"):
    path = paper / name
    manifest[name] = {"bytes": path.stat().st_size,
                      "sha256": sha256(path.read_bytes()).hexdigest()}
(paper / "verification" / "artifact-manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n"
)
print(f"Packaged {len(source_files) + 1} submission files and "
      f"{len(companion_files)} companion files.")
for name, record in manifest.items():
    print(f"{name}: {record['bytes']} bytes; SHA256 {record['sha256']}")
