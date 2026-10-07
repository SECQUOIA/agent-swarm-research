"""Read loop records from .jsonl files or their gzip-compressed .jsonl.gz copies.

records(pattern) expands the glob pattern, also matching PATTERN.gz, uses the plain file when both
exist, and stops with an error if nothing matches (so an analysis never silently reads 0 files)."""
import glob, gzip, json, sys


def files(pattern):
    plain = sorted(glob.glob(pattern))
    gz = [f for f in sorted(glob.glob(pattern + '.gz')) if f[:-3] not in plain]
    out = sorted(plain + gz)
    if not out:
        sys.exit('recio: no file matches %r (nor %r)' % (pattern, pattern + '.gz'))
    return out


def lines(path):
    with (gzip.open(path, 'rt') if path.endswith('.gz') else open(path)) as f:
        for line in f:
            yield line


def records(pattern):
    for f in files(pattern):
        for line in lines(f):
            yield f, json.loads(line)
