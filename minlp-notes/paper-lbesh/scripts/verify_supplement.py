#!/usr/bin/env python3
"""Verify every frozen research member, optionally extracting safely.

The extraction destination must be new or empty. No links, special files,
absolute paths, dot/dot-dot components, or duplicate names are accepted.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import tarfile

EXPECTED = '96c50c412dbea4386d530419570c0215685a40c43a96aac4a6b9c9c4aca8131e'
MANIFEST = 'code/minlp_solver_lab/results/lbesh_development/publication_manifest_v1.json'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', type=Path)
parser.add_argument('--extract', type=Path)
args = parser.parse_args()
assert hashlib.sha256(args.archive.read_bytes()).hexdigest() == EXPECTED, 'Archive hash mismatch'
if args.extract:
    assert not args.extract.is_symlink(), 'Destination must not be a link'
    assert not args.extract.exists() or (args.extract.is_dir() and not any(args.extract.iterdir())), 'Destination must be new or empty'
with tarfile.open(args.archive, 'r:gz') as tar:
    members = tar.getmembers()
    names = [m.name for m in members]
    assert len(names) == len(set(names)) == 9077, 'Wrong or duplicate members'
    for m in members:
        parts = m.name.split('/')
        assert m.isfile() and not PurePosixPath(m.name).is_absolute(), m.name
        assert all(p not in ('', '.', '..') for p in parts), m.name
    manifest = json.load(tar.extractfile(MANIFEST))
    assert set(names) == set(manifest['files']) | {MANIFEST}, 'Manifest member mismatch'
    total = 0
    for m in members:
        data = tar.extractfile(m).read()
        if m.name != MANIFEST:
            entry = manifest['files'][m.name]
            assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], m.name
            total += len(data)
        if args.extract:
            target = args.extract.joinpath(*PurePosixPath(m.name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
print(json.dumps({'archive_sha256': EXPECTED, 'members': len(members),
                  'verified_payload_files': len(manifest['files']),
                  'payload_bytes': total, 'extracted': bool(args.extract)}, indent=2))
