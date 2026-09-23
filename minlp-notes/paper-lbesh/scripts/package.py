#!/usr/bin/env python3
"""Build the paper and create a deterministic source archive and checksums.

Run after every manuscript correction. Does not modify the frozen supplement.
Requires latexmk/BibTeX and the packages declared in main.tex.
"""
from pathlib import Path
import gzip
import hashlib
import io
import json
import shutil
import subprocess
import tarfile

P = Path(__file__).resolve().parents[1]
subprocess.run(['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
                'main.tex'], cwd=P, check=True)
paths = [P/n for n in ['main.tex', 'main.bbl', 'references.bib', 'README.md']]
for directory in ['sections', 'figures', 'tables', 'data', 'scripts']:
    paths.extend(p for p in (P/directory).rglob('*') if p.is_file()
                 and '__pycache__' not in p.parts and p.suffix != '.pyc')
for name in ['check_stage02.py', 'coverage.md', 'literature.md',
             'stage02-checks.json', 'stage03-claims.json',
             'stage03-independent-audit.json']:
    paths.append(P/'evidence'/name)
paths.extend(p for p in (P/'supplement').iterdir() if p.is_file()
             and p.name != 'publication_bundle_v1.tar.gz')
payload = {str(p.relative_to(P)): p.read_bytes() for p in sorted(set(paths))}
manifest = {'format': 1, 'files': {name: {'bytes': len(data),
             'sha256': hashlib.sha256(data).hexdigest()}
             for name, data in sorted(payload.items())}}
payload['source-manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode()
dist = P/'dist'
dist.mkdir(exist_ok=True)
archive = dist/'paper-lbesh-source.tar.gz'
with archive.open('wb') as raw:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for name, data in sorted(payload.items()):
                entry = tarfile.TarInfo('paper-lbesh/'+name)
                entry.size = len(data)
                entry.mode = 0o644
                entry.mtime = 0
                tar.addfile(entry, io.BytesIO(data))
shutil.copyfile(P/'main.pdf', dist/'paper-lbesh.pdf')
delivery = [dist/'paper-lbesh.pdf', archive,
            P/'supplement/publication_bundle_v1.tar.gz']
checks = []
for path in delivery:
    if not path.is_file():
        raise FileNotFoundError(f'Required delivery missing: {path}')
    checks.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+
                  str(path.relative_to(P)))
(P/'SHA256SUMS').write_text('\n'.join(checks)+'\n')
(dist/'source-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(f'Packaged {len(manifest["files"])} source files; see SHA256SUMS.')
