#!/usr/bin/env python3
"""Reject ordinary Git blobs at or above GitHub's 100 MiB file limit."""
import argparse
import subprocess

LIMIT = 100 * 1024 * 1024


def git(*args, data=None):
    return subprocess.check_output(['git', *args], input=data)


def check(staged, base):
    if staged:
        changed = set(git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').split(b'\0'))
        objects = {}
        for entry in git('ls-files', '--stage', '-z').split(b'\0'):
            if not entry:
                continue
            metadata, path = entry.split(b'\t', 1)
            mode, oid, stage = metadata.split()
            if path in changed and stage == b'0' and mode.startswith(b'100'):
                objects[oid] = path
    else:
        objects = {}
        for entry in git('rev-list', '--objects', 'HEAD', '--not', base).splitlines():
            oid, _, path = entry.partition(b' ')
            objects[oid] = path
    if not objects:
        print('PASS: no new Git blobs to check')
        return
    sizes = git('cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)',
                data=b'\n'.join(objects) + b'\n')
    oversized = []
    for entry in sizes.splitlines():
        oid, kind, size = entry.split()
        if kind == b'blob' and int(size) >= LIMIT:
            oversized.append((objects[oid].decode(errors='replace'), int(size)))
    if oversized:
        for path, size in oversized:
            print(f'BLOCKED: {size / 1024**2:.2f} MiB {path}')
        raise SystemExit('Archive these files before committing or pushing; see artifacts/README.md.')
    print('PASS: new ordinary Git blobs are below 100 MiB')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--base', default='origin/main', help='Published base for checking unpublished history')
    args = parser.parse_args()
    check(args.staged, args.base)
