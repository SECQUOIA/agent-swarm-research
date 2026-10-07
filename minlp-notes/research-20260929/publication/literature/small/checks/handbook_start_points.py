"""Evaluate the MINLPLib Gibbs objectives (ex6_2_7, ex6_2_5) at the start points
written in the handbook GAMS files (../sources/titan/ex6.2.*.gms) and compare
with our certified optimum and optimal point
(open-instances-wave2/small/logs/ex6_2_*_primal.txt).  Evidence only.
For ex6_2_5 the handbook gives start values only for liquid phases 1 and 2;
the vapour phase is set to the mass-balance remainder here."""
import os
from mpmath import mp, mpf
mp.dps = 40
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'compare_gms.py')).read().split("a, b = sys.argv[1]")[0]
cg = {}; exec(src, cg)
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
def ours(name):
    d = {}
    for line in open(os.path.join(root, 'open-instances-wave2', 'small', 'logs', name + '_primal.txt')):
        p = line.split()
        if len(p) == 2 and p[0].startswith('x'): d[p[0]] = mpf(p[1])
    return d
cases = {
 'ex6_2_7': ({'x2': '0.00880', 'x3': '0.33595', 'x4': '0.05525', 'x5': '0.00065', 'x6': '0.00193', 'x7': '0.09742',
              'x8': '0.30803', 'x9': '0.14700', 'x10': '0.04497'}, None),
 'ex6_2_5': ({'x2': '31.459', 'x3': '0.901998', 'x5': '3.10348', 'x6': '0.0000096', 'x8': '26.1669', 'x9': '15.0141'},
             {'x4': ('40.30707', 'x2', 'x3'), 'x7': ('5.14979', 'x5', 'x6'), 'x10': ('54.54314', 'x8', 'x9')}),
}
for name, (start, rem) in cases.items():
    eqs, bnd, pos, var = cg['parse'](os.path.join(here, '..', 'sources', 'minlplib_gms', name + '.gms'))
    x = {k: mpf(v) for k, v in start.items()}
    if rem:
        for k, (tot, a, b) in rem.items(): x[k] = mpf(tot) - x[a] - x[b]
    def G(x):
        xx = dict(x); xx['objvar'] = mpf(0)
        l, k, r = eqs['e1']
        return -(cg['ev'](l, xx) - cg['ev'](r, xx))
    o = ours(name)
    print(name)
    print('  objective at handbook start point :', mp.nstr(G(x), 15))
    print('  objective at our optimal point    :', mp.nstr(G(o), 15))
    # phases with identical Gibbs functions may be listed in any order:
    # ex6_2_7 has three identical liquid phases, ex6_2_5 two (phases 1, 2).
    import itertools
    comps = [('x2', 'x3', 'x4'), ('x5', 'x6', 'x7'), ('x8', 'x9', 'x10')]
    perms = itertools.permutations(range(3)) if name == 'ex6_2_7' else [(0, 1, 2), (1, 0, 2)]
    best = None
    for pm in perms:
        dev = max(abs(x[c[k]] - o[c[pm[k]]]) for c in comps for k in range(3))
        if best is None or dev < best[0]: best = (dev, pm)
    print('  max |start - ours| (best phase order', best[1], '):', mp.nstr(best[0], 6))
    bal = [cg['ev'](eqs[e][0], x) - cg['ev'](eqs[e][2], x) for e in ['e2', 'e3', 'e4']]
    print('  mass-balance residuals at start   :', [mp.nstr(b, 3) for b in bal])
