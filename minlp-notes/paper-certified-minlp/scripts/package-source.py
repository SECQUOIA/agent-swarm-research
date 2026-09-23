#!/usr/bin/env python3
"""Package explicitly selected source files without reading experimental archives."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import tarfile

root = Path(__file__).resolve().parents[1]
paths = [root / name for name in (
    'main.tex', 'references.bib', 'README.md',
    'supplement/README.md', 'supplement/archives.json',
    'evidence/repository-inventory.md', 'evidence/literature-review.md',
)]
for directory in ('sections', 'tables', 'scripts', 'formal'):
    paths += [p for p in (root / directory).rglob('*')
              if p.is_file() and '.lake' not in p.relative_to(root).parts
              and '__pycache__' not in p.relative_to(root).parts]
paths = sorted(set(paths), key=lambda p: p.relative_to(root).as_posix())
if any(p.is_symlink() for p in paths):
    raise SystemExit('Source inventory unexpectedly contains a symlink')
man = root / 'PAPER-SHA256SUMS'
man.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  '
                       f'{p.relative_to(root).as_posix()}\n' for p in paths))
paths.append(man)
archive = root / 'certified-minlp-paper-source.tar.gz'
with archive.open('wb') as raw:
    with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.PAX_FORMAT) as out:
            for path in paths:
                data = path.read_bytes()
                info = tarfile.TarInfo('certified-minlp-paper/' + path.relative_to(root).as_posix())
                info.size = len(data)
                info.mtime = 0
                info.mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
                out.addfile(info, io.BytesIO(data))
record = {'file': archive.name, 'bytes': archive.stat().st_size,
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
          'source_files_including_manifest': len(paths),
          'excluded': ['experimental core and bulk archives', '.lake caches',
                       'LaTeX auxiliaries and compiled PDF', 'literature PDFs',
                       'duplicate builds and internal review history']}
(root / 'paper-source-archive.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
