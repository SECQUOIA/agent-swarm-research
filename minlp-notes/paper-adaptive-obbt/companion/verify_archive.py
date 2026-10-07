"""Verify the companion without extracting files or executing scientific code."""
import hashlib
import json
from pathlib import Path
import tarfile

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
for record in manifest['companion_files']:
    data = (root / record['path']).read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit('Companion digest mismatch: ' + record['path'])
expected = {record['path']: record for record in manifest['archive_members']}
with tarfile.open(root / manifest['archive'], 'r:gz') as archive:
    members = archive.getmembers()
    if len(members) != len(expected) or {m.name for m in members} != set(expected):
        raise SystemExit('Archive inventory mismatch')
    for member in members:
        if not member.isfile():
            raise SystemExit('Unexpected non-file member: ' + member.name)
        data = archive.extractfile(member).read()
        record = expected[member.name]
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise SystemExit('Archive member digest mismatch: ' + member.name)
print('Verified', len(expected), 'archive members and',
      len(manifest['companion_files']), 'companion files; no scientific code executed.')
