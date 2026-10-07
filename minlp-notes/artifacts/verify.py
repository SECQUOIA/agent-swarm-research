#!/usr/bin/env python3
"""Verify downloaded evidence assets, optionally checking every archive member."""
import argparse
import contextlib
import gzip
import hashlib
import json
from pathlib import Path
import tarfile


def sha256(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


class PartsReader:
    """Read ordered release parts as one tar.gz stream without joining on disk."""
    def __init__(self, paths):
        self.paths = iter(paths)
        self.current = None

    def read(self, size):
        chunks = []
        while size:
            if self.current is None:
                path = next(self.paths, None)
                if path is None:
                    break
                self.current = path.open('rb')
            chunk = self.current.read(size)
            if not chunk:
                self.current.close()
                self.current = None
                continue
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)

    def close(self):
        if self.current is not None:
            self.current.close()


def verify(directory, contents):
    registry = Path(__file__).parent
    manifest = json.loads((registry / 'manifest.json').read_text())
    index_spec = manifest['member_index']
    index = registry / index_spec['file']
    if index.stat().st_size != index_spec['bytes'] or sha256(index) != index_spec['sha256']:
        raise ValueError('Committed member index does not match manifest')
    expected = {}
    if contents:
        with gzip.open(index, 'rt') as source:
            for line in source:
                member = json.loads(line)
                expected.setdefault(member['package'], {})[member['path']] = member
    for package in manifest['packages']:
        paths = []
        for asset in package['assets']:
            path = directory / asset['file']
            if path.stat().st_size != asset['bytes'] or sha256(path) != asset['sha256']:
                raise ValueError(f'Asset checksum or size mismatch: {path}')
            paths.append(path)
        if contents:
            members = expected[package['id']].copy()
            count = 0
            with contextlib.closing(PartsReader(paths)) as stream:
                with tarfile.open(fileobj=stream, mode='r|gz') as archive:
                    for info in archive:
                        record = members.pop(info.name, None)
                        if record is None or info.size != record['bytes']:
                            raise ValueError(f'Unexpected, repeated or changed archive member: {info.name}')
                        if 'symlink' in record:
                            if not info.issym() or info.linkname != record['symlink']:
                                raise ValueError(f'Symlink mismatch: {info.name}')
                        else:
                            if not info.isfile():
                                raise ValueError(f'File type mismatch: {info.name}')
                            with archive.extractfile(info) as source:
                                if hashlib.file_digest(source, 'sha256').hexdigest() != record['sha256']:
                                    raise ValueError(f'Member checksum mismatch: {info.name}')
                        count += 1
            if members or count != package['member_count']:
                raise ValueError(f'Missing archive members: {package["id"]}')
        print(f'PASS {package["id"]}: assets' + (' and every member' if contents else ''), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='Directory containing the downloaded release assets')
    parser.add_argument('--contents', action='store_true', help='Stream and verify every original file without extraction')
    args = parser.parse_args()
    verify(args.directory, args.contents)
