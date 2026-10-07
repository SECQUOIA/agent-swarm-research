"""Review r2: exact .gms-text vs MINLPLib OSIL comparison for one instance.
Usage: python3 cmp_forms.py NAME [point.sol ...]
Prints per-row verdicts summary, objective coefficient differences by degree,
and exact objective values at given .sol points (missing variables = 0)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])
_PUBLIC_HOME = str(_PublicPath.home())

import sys, json, time
from fractions import Fraction
import sympy as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import exactcmp as X

GMS = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/gms')
OSIL = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil')

def poly_dict(e, gens=None):
    """monomial -> exact coefficient of the expanded polynomial (raises PolynomialError if not polynomial)"""
    d = {}
    for m, c in sp.expand(e).as_coefficients_dict().items():
        if not m.is_polynomial():
            raise sp.PolynomialError(str(m))
        d[m] = d.get(m, 0) + c
    return {m: c for m, c in d.items() if c != 0}

def degree(m):
    return 0 if m == 1 else sum(int(p) for p in m.as_powers_dict().values())

def main():
    name = sys.argv[1]
    t0 = time.time()
    eqs, objvar, sense = X.read_gms(f'{GMS}/{name}.gms')
    rows, obj_o, osense, names, bounds = X.read_osil(f'{OSIL}/{name}.osil')
    objrow, obj_g = X.gms_objective(eqs, objvar)
    print(name, 'gms eqs', len(eqs), 'objrow', objrow, 'osil rows', len(rows), 'sense', sense, osense, 'read %.1fs' % (time.time() - t0), flush=True)
    assert set(rows) == set(eqs) - {objrow}, 'row names differ'
    ndiff_rows, diff_rows, coef_stats = 0, [], []
    for k in rows:
        f, lb, ub = rows[k]
        e, s = eqs[k]
        c = {'E': lb, 'G': lb, 'L': ub}[s]
        assert (s == 'E' and lb == ub) or (s == 'G' and ub is None) or (s == 'L' and lb is None), (k, s, lb, ub)
        fo = f - X.Q(c)
        d = sp.expand(e - fo)
        if d != 0:
            d = sp.cancel(sp.together(e - fo))
        if d != 0:
            ndiff_rows += 1
            gens = sorted((e.free_symbols | fo.free_symbols), key=str)
            try:
                pg, po = poly_dict(e, gens), poly_dict(fo, gens)
                keys = set(pg) | set(po)
                dk = [(m, pg.get(m, 0), po.get(m, 0)) for m in keys if pg.get(m, 0) != po.get(m, 0)]
                diff_rows.append((k, len(dk)))
                for m, a, b in dk:
                    coef_stats.append((k, str(m), a, b))
            except sp.PolynomialError:
                diff_rows.append((k, 'nonpolynomial'))
    print('rows differing:', ndiff_rows, 'of', len(rows))
    from collections import Counter
    cc = Counter((str(a), str(b)) for _, _, a, b in coef_stats)
    for (a, b), n in cc.most_common(10):
        fa, fb = Fraction(a), Fraction(b)
        print('  row coef gms', a, '=', float(fa), ' osil', b, '=', repr(float(fb)), ' count', n, ' rel', float(abs(fa - fb) / abs(fa)))
    print('  coefficients per differing row:', Counter(n for _, n in diff_rows))
    # objective
    gens = sorted(obj_g.free_symbols | obj_o.free_symbols, key=str)
    try:
        pg, po = poly_dict(obj_g, gens), poly_dict(obj_o, gens)
    except sp.PolynomialError:
        d = sp.cancel(sp.together(obj_g - obj_o))
        print('objective is not polynomial; exact difference after cancel:', d)
        pg, po = {}, {}
    keys = set(pg) | set(po)
    dk = [(m, pg.get(m, 0), po.get(m, 0)) for m in keys if pg.get(m, 0) != po.get(m, 0)]
    bydeg = Counter(degree(m) for m, _, _ in dk)
    print('objective: gms monomials', len(pg), 'osil monomials', len(po), 'differing', len(dk), 'by degree', dict(sorted(bydeg.items())))
    if dk:
        mabs = max(abs(Fraction(int(sp.numer(a - b)), int(sp.denom(a - b)))) for _, a, b in dk)
        mrel = max(abs(Fraction(int(sp.numer(a - b)), int(sp.denom(a - b)))) / abs(Fraction(int(sp.numer(a)), int(sp.denom(a)))) for _, a, b in dk if a != 0)
        print('  max abs diff', float(mabs), 'max rel diff', float(mrel), 'zero-in-gms coefs', sum(1 for _, a, _ in dk if a == 0))
        for m, a, b in sorted(dk, key=lambda t: -degree(t[0]))[:3]:
            print('   e.g.', m, a, '=', float(a), 'osil', b, '=', repr(float(b)))
        print('  total-degree counts of all gms objective monomials:', dict(sorted(Counter(degree(m) for m in pg).items())))
    res = dict(name=name, rows=len(rows), rows_differing=ndiff_rows, obj_monomials=len(pg), obj_diff=len(dk), obj_diff_by_degree=dict(bydeg), diffs=[(str(m), str(a), str(b)) for m, a, b in dk])
    # points
    for sol in sys.argv[2:]:
        vals = {}
        for line in open(sol):
            p = line.split()
            if len(p) >= 2 and p[0] != objvar:
                vals[X.S(p[0])] = X.Q(p[1])
        allsyms = obj_g.free_symbols | obj_o.free_symbols
        sub = {s: vals.get(s, sp.Integer(0)) for s in allsyms}
        vg, vo = obj_g.subs(sub), obj_o.subs(sub)
        print('point', sol.rsplit('/', 1)[-1], 'obj gms =', vg, '=', sp.N(vg, 30), '; obj osil =', vo, '=', sp.N(vo, 30), '; gms-osil =', sp.N(vg - vo, 6))
        res['point_' + sol.rsplit('/', 1)[-1]] = dict(gms=str(vg), osil=str(vo))
    print('time %.1fs' % (time.time() - t0))
    json.dump(res, open(f'{_PUBLIC_REPO}/research-20260929/publication/reviews/minlplib-status-r2/logs/cmp_forms_{name}.json', 'w'), indent=1)

main()
