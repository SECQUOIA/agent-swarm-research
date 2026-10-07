"""Dossier recheck of certB: partition of each link's root box, record containment,
exact Lemma-2 corrections, exact shortest path. Own code; reads the pickle via a stub."""
import math, sys, time
from fractions import Fraction as F
import numpy as np
import load_cs

st = load_cs.load(sys.argv[1])
T = st['T']; cells = st['cells']; leaves = st['leaves']; lam = st['lam']; recs = st['recs']
t0 = time.time()
INF = float('inf')

# 1. partition: leaves inside root, pairwise interiors disjoint, volumes sum to root volume
for l in range(T - 1):
    root = cells[l][0]
    assert root['parent'] is None
    los = np.array([cells[l][i]['lo'] for i in leaves[l]]); his = np.array([cells[l][i]['hi'] for i in leaves[l]])
    assert (los >= np.array(root['lo'])).all() and (his <= np.array(root['hi'])).all()
    assert (his > los).all()
    n = len(leaves[l])
    # pairwise interior overlap
    ov = 0
    for i in range(n):
        inter = (np.minimum(his[i], his) > np.maximum(los[i], los)).all(axis=1)
        inter[i] = False
        ov += int(inter.sum())
    vol = sum(math.prod(F(h) - F(lo) for lo, h in zip(cells[l][i]['lo'], cells[l][i]['hi'])) for i in leaves[l])
    rvol = math.prod(F(h) - F(lo) for lo, h in zip(root['lo'], root['hi']))
    print(f'link {l}: {n} leaves, overlapping pairs {ov}, volume equal {vol == rvol}, root lo {root["lo"]} hi {root["hi"]}')
    assert ov == 0 and vol == rvol
    # one finite slope per leaf
    for i in leaves[l]:
        assert len(lam[l][i]) == 3 and all(math.isfinite(x) for x in lam[l][i])

# 2. pair bounds from records, best containing record chosen by float value, then exact
def corr(lnew, aold, lo, hi, sign):
    s = F(0)
    for k in range(3):
        dk = F(lnew[k]) - F(aold[k])
        s += min(sign * dk * F(lo[k]), sign * dk * F(hi[k]))
    return s

zero = [0.0, 0.0, 0.0]
pair = []  # pair[t][(r, c)] = Fraction or None (inf)
used = set()
for t in range(T):
    rows = leaves[t - 1] if t > 0 else [None]
    cols = leaves[t] if t < T - 1 else [None]
    if t > 0:
        rlo = np.array([cells[t - 1][i]['lo'] for i in rows]); rhi = np.array([cells[t - 1][i]['hi'] for i in rows])
    if t < T - 1:
        clo = np.array([cells[t][i]['lo'] for i in cols]); chi = np.array([cells[t][i]['hi'] for i in cols])
    best = {}  # (ri, ci) -> (floatval, rid)
    for rid, rec in enumerate(recs):
        if rec['t'] != t: continue
        assert rec['mu'] == 0.0
        if t == 0: assert rec['cin_box'] is None and rec['lam_in'] == zero
        if t == T - 1: assert rec['cout_box'] is None and rec['lam_out'] == zero
        b = rec['bound']
        assert not (isinstance(b, float) and (math.isnan(b) or b == -INF))
        if b == INF: assert rec['status'] == 'infeasible'
        if t > 0:
            lo, hi = np.array(rec['cin_box'][0]), np.array(rec['cin_box'][1])
            ri = np.nonzero(((rlo >= lo) & (rhi <= hi)).all(axis=1))[0]
        else:
            ri = np.array([0])
        if len(ri) == 0: continue
        if t < T - 1:
            lo, hi = np.array(rec['cout_box'][0]), np.array(rec['cout_box'][1])
            ci = np.nonzero(((clo >= lo) & (chi <= hi)).all(axis=1))[0]
        else:
            ci = np.array([0])
        if len(ci) == 0: continue
        for a in ri:
            if t > 0:
                L = lam[t - 1][rows[a]]; d = np.array(L) - np.array(rec['lam_in'])
                cin = float(np.minimum(d * rlo[a], d * rhi[a]).sum())
            else:
                cin = 0.0
            for c in ci:
                if t < T - 1:
                    L2 = lam[t][cols[c]]; d2 = np.array(L2) - np.array(rec['lam_out'])
                    cout = float(np.minimum(-d2 * clo[c], -d2 * chi[c]).sum())
                else:
                    cout = 0.0
                v = INF if b == INF else b + cin + cout
                key = (a, c)
                if key not in best or v > best[key][0] or (v == best[key][0] and rid < best[key][1]):
                    best[key] = (v, rid)
    nexp = len(rows) * len(cols)
    assert len(best) == nexp, (t, len(best), nexp)
    tab = {}
    for (a, c), (v, rid) in best.items():
        rec = recs[rid]; used.add(rid)
        if rec['bound'] == INF:
            tab[(a, c)] = None; continue
        val = F(rec['bound'])
        if t > 0:
            r = cells[t - 1][rows[a]]; val += corr(lam[t - 1][rows[a]], rec['lam_in'], r['lo'], r['hi'], 1)
        if t < T - 1:
            cc = cells[t][cols[c]]; val += corr(lam[t][cols[c]], rec['lam_out'], cc['lo'], cc['hi'], -1)
        tab[(a, c)] = val
    pair.append(tab)
    print(f'period {t}: {nexp} leaf pairs, finite {sum(v is not None for v in tab.values())}', flush=True)

# 3. exact DP
f = {c: pair[0][(0, c)] for c in range(len(leaves[0]))}
for t in range(1, T - 1):
    g = {}
    for c in range(len(leaves[t])):
        bestv = None
        for a in range(len(leaves[t - 1])):
            if f[a] is None or pair[t][(a, c)] is None: continue
            v = f[a] + pair[t][(a, c)]
            if bestv is None or v < bestv: bestv = v
        g[c] = bestv
    f = g
val = None
for a in range(len(leaves[T - 2])):
    if f[a] is None or pair[T - 1][(a, 0)] is None: continue
    v = f[a] + pair[T - 1][(a, 0)]
    if val is None or v < val: val = v
print('exact DP value', val, '=', float(val))
print('rounded down 9dp', F(math.floor(val * 10**9), 10**9), float(F(math.floor(val * 10**9), 10**9)))
print('records used', len(used), 'time', round(time.time() - t0, 1), 's')
