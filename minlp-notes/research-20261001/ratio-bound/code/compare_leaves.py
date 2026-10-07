"""Compare two box-certificate files of certify_zB.py (plain or .gz): same set of leaves
(facet, bisection path, certificate type, certificate data)?  Prints both headers.
usage: python3 compare_leaves.py FILE1 FILE2"""
import gzip
import json
import sys


def load(fn):
    op = gzip.open if fn.endswith('.gz') else open
    head, leaves = None, []
    with op(fn, 'rt') as f:
        for line in f:
            d = json.loads(line)
            if 'path' in d:
                leaves.append((tuple(d['facet']), d['path'], d['cert'], json.dumps(d['data'])))
            elif head is None:
                head = line.strip()
    return head, leaves


h1, a = load(sys.argv[1])
h2, b = load(sys.argv[2])
print('header 1:', h1)
print('header 2:', h2)
print('leaves: %d vs %d' % (len(a), len(b)))
print('same facets, paths and certificate types:', sorted(x[:3] for x in a) == sorted(x[:3] for x in b))
print('same including certificate data:', sorted(a) == sorted(b))
