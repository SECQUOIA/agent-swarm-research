#!/usr/bin/env python3
"""Create a portable submission archive from an explicit source allowlist."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
files = [root / name for name in ('main.tex', 'macros.tex', 'bibliography.bib',
          'main.bbl', 'Makefile', 'README.md', 'figures/query-overview.pdf')]
files += sorted((root / 'sections').glob('*.tex'))
files += sorted((root / 'scripts').glob('*.py'))
for path in files:
    if not path.is_file():
        raise FileNotFoundError(f'Build the manuscript before packaging: {path}')
archive = root / 'submission-source.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for path in files:
        z.write(path, path.relative_to(root))
print(f'Wrote {archive} ({len(files)} files)')
