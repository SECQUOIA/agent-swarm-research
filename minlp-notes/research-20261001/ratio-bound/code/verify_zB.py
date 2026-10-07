"""Exact verification of the leaves written by certify_zB.py (Theorem B2 of the note).

Checks, in exact rational arithmetic:
  1. every one of the 8 facets {x_ij = +-1, other entries in [-1, 1]} has a completed block of leaves;
  2. the bisection paths of each facet are prefix-free with Kraft sum exactly 1, so the leaf boxes cover
     the facet;
  3. every leaf certificate holds on its whole box:
       'det' : det X < 0 at all vertices of the box (det is multilinear in the free entries);
       'psi' : interval upper bound of rho x21 (x11 - x22) + x11 x22 - rho^2 x21^2 is < 0;
       'a22' : rho x21 + x22 < 0 on the box;
       'pt'  : v^T X M(s) v < 0 and v^T X M(s - q(s) e_w) v < 0 on the box, for the stated test point s
               and rational v.
usage: python3 verify_zB.py LEAVESFILE[.gz] RHO [FAMILY]
"""
import sys
import json
import gzip
from fractions import Fraction
from certify_zB import box_of, det_max_vertices, psi_upper, FACETS, family_points_exact




def M(s):
    x, y, w = s
    return ((w, x), (y, Fraction(1)))


def lin_coef(v, N):
    Nv = (N[0][0] * v[0] + N[0][1] * v[1], N[1][0] * v[0] + N[1][1] * v[1])
    return ((v[0] * Nv[0], v[0] * Nv[1]), (v[1] * Nv[0], v[1] * Nv[1]))


def box_max_lin(c, lo, hi):
    m = Fraction(0)
    for i in range(2):
        for j in range(2):
            m += c[i][j] * (hi[i][j] if c[i][j] > 0 else lo[i][j])
    return m


def main(fname, rho, spec='B'):
    rho = Fraction(rho)
    pts = family_points_exact(spec, rho)
    blocks = {}
    cur = {}
    opener = gzip.open if fname.endswith('.gz') else open
    for line in opener(fname, 'rt'):
        d = json.loads(line)
        if 'facet_start' in d:
            assert Fraction(d['rho']) == rho, 'rho mismatch'
            assert d.get('family', 'B') == spec, 'family mismatch'
            cur[tuple(d['facet_start'])] = []
        elif 'facet_done' in d:
            f = tuple(d['facet'])
            blocks[f] = cur.pop(f)
        elif 'cert' in d:
            cur[tuple(d['facet'])].append(d)
        elif 'feasible_point' in d or 'maxdepth' in d or 'timeout' in d:
            print('non-certificate record:', d)
    ok = True
    counts = {}
    for f in FACETS:
        if f not in blocks:
            print('facet', f, 'MISSING')
            ok = False
            continue
        leaves = blocks[f]
        paths = [d['path'] for d in leaves]
        kraft = sum(Fraction(1, 2 ** len(p)) for p in paths)
        ps = sorted(paths)
        prefix_free = all(not ps[i + 1].startswith(ps[i]) for i in range(len(ps) - 1)) and len(set(ps)) == len(ps)
        if kraft != 1 or not prefix_free:
            print('facet', f, 'coverage FAIL: kraft', kraft, 'prefix-free', prefix_free)
            ok = False
        for d in leaves:
            lo, hi = box_of(f, d['path'])
            c = d['cert']
            if c == 'det':
                good = det_max_vertices(lo, hi) < 0
            elif c == 'psi':
                good = psi_upper(lo, hi, rho) < 0
            elif c == 'a22':
                good = rho * hi[1][0] + hi[1][1] < 0
            elif c == 'pt':
                k, (v0, v1) = d['data']
                v = (Fraction(v0), Fraction(v1))
                s = pts[k]
                q = s[2] - s[0] * s[1]
                foot = (s[0], s[1], s[2] - q)
                good = (box_max_lin(lin_coef(v, M(s)), lo, hi) < 0 and
                        box_max_lin(lin_coef(v, M(foot)), lo, hi) < 0)
            else:
                good = False
            counts[c] = counts.get(c, 0) + 1
            if not good:
                print('leaf FAIL', f, d)
                ok = False
    print('family', spec, ' rho =', rho, ' leaves by certificate type:', counts, ' total', sum(counts.values()))
    print('ALL LEAVES VERIFIED, ALL 8 FACETS COVERED' if ok else 'VERIFICATION FAILED')
    return ok


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'B')
