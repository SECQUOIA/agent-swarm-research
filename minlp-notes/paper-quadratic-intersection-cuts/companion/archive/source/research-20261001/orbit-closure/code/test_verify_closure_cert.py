"""Targeted regression checks for closure points and outside pruning.

Usage: python3 test_verify_closure_cert.py CERT_PROP16_A.json CERT_WCORNER_A.json
"""
import contextlib
import copy
import io
import json
import sys
import tempfile
from fractions import Fraction as Fr
import verify_closure_cert as V
from certify_closure_point import outside_V


def run(d):
    with tempfile.NamedTemporaryFile('w+', suffix='.json') as fh:
        json.dump(d, fh)
        fh.flush()
        with contextlib.redirect_stdout(io.StringIO()):
            return V.main(fh.name)


def main():
    with open(sys.argv[1]) as fh:
        prop16 = json.load(fh)
    with open(sys.argv[2]) as fh:
        wcorner = json.load(fh)
    tests = []
    for name, d in (('Prop16', prop16), ('W-corner', wcorner)):
        tests.append((name + ' unmodified certificate', d, 0))
        lam = d['instance']['lam']
        for case, bad_lam in (
            ('negative final entry', lam[:-1] + ['-5']),
            ('missing entry', lam[:-1]),
            ('extra nonnegative entry', lam + ['0']),
            ('extra negative entry', lam + ['-5']),
        ):
            m = copy.deepcopy(d); m['instance']['lam'] = bad_lam
            tests.append((name + ' lam_hat: ' + case, m, 1))
    m = copy.deepcopy(prop16)
    m['instance']['xpoints'] = [['1', '0', '0']]
    pc = next(pc for pc in m['blocks'][0]['pieces']
              if all(Fr(a[0]) < 1 for a in pc['vertices']))
    pc.pop('Y')
    pc['outside'] = 0
    tests.append(('valid outside piece, points under instance', m, 0))
    m = copy.deepcopy(m)
    # The top-level field must not override instance data.
    m['xpoints'] = [['1', '0', '0']]
    m['instance']['xpoints'] = [['0', '0', '0']]
    tests.append(('invalid instance point with valid top-level decoy', m, 1))
    m = copy.deepcopy(wcorner)
    m['instance']['xpoints'] = [['0', '0', '0', '2']]
    pc = m['blocks'][0]['pieces'][0]
    pc.pop('Y')
    pc['outside'] = 0
    tests.append(('point positive on unbounded inactive coordinate', m, 1))
    for name, d, expected in tests:
        rc = run(d)
        assert rc == expected, '%s: exit %d, expected %d' % (name, rc, expected)
        print('PASS %s (exit %d)' % (name, rc))
    vertices = [tuple(Fr(a) for a in row) for row in pc['vertices']]
    assert outside_V(vertices, [[Fr(0), Fr(0), Fr(0), Fr(2)]], [0, 1, 2]) is None
    print('PASS producer also rejects pruning on an inactive coordinate')
    print('ALL %d CLOSURE REGRESSION CHECKS PASS' % (len(tests) + 1))


if __name__ == '__main__':
    main()
