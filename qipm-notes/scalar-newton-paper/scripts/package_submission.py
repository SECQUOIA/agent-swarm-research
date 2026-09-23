"""Bundle the standalone manuscript and diagnostics, excluding internal audits."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
paths = [root / name for name in (
    "main.tex", "macros.tex", "bibliography.bib", "main.bbl", "main.pdf",
    "Makefile", "README.md",
)]
for folder, pattern in (("sections", "*.tex"), ("scripts", "*.py"), ("checks", "*.py")):
    paths.extend(sorted((root / folder).glob(pattern)))
for path in paths:
    if not path.is_file():
        raise FileNotFoundError(f"Build the manuscript before packaging: {path.name}")
output = root / "scalar-newton-submission.zip"
with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
    for path in paths:
        archive.write(path, path.relative_to(root))
print(f"Wrote {output.name} with {len(paths)} files")
