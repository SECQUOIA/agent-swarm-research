"""Independent exact derivation of the terminal row from the OSIL rows (dossier check)."""
import sys
from fractions import Fraction as F
import osilmini

def run(T):
    m = osilmini.read(f'waterno2_{T:02d}.osil')
    V, C, R, NL = m['vars'], m['cons'], m['rows'], m['nonlin']
    lin = [i for i in range(len(C)) if i not in NL]
    par = list(range(len(V)))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    copy_rows = []
    for i in lin:
        r = R[i]
        if len(r) == 2 and sorted(r.values()) == [-1, 1] and C[i]['lb'] == 0 and C[i]['ub'] == 0:
            a, b = list(r); copy_rows.append(i); par[find(a)] = find(b)
    bal = []
    for i in lin:
        r = R[i]
        vals = sorted(r.values())
        if len(r) == 4 and C[i]['lb'] == 0 and C[i]['ub'] == 0 and F(3600) in vals and F(-3600) in vals:
            A = max(abs(v) for v in vals if abs(v) != 3600)
            assert sorted(vals) == sorted([F(3600), F(-3600), A, -A]), (i, vals)
            bal.append((i, A))
    hor = [i for i in lin if C[i]['lb'] is not None and C[i]['lb'] > 0 and C[i]['ub'] is None
           and all(v == 1 for v in R[i].values()) and len(R[i]) == T]
    assert len(hor) == 1, hor
    h = hor[0]; c = C[h]['lb']
    # sum of balance rows / 3600 as a form over classes
    S = {}
    for i, A in bal:
        for j, v in R[i].items():
            k = find(j); S[k] = S.get(k, 0) + v / 3600
    S = {k: v for k, v in S.items() if v != 0}
    # classes fixed by single-variable equality rows or by fixed bounds
    fixed = {}
    for i in lin:
        r = R[i]
        if len(r) == 1 and C[i]['lb'] is not None and C[i]['lb'] == C[i]['ub']:
            (j, a), = r.items(); fixed.setdefault(find(j), set()).add(C[i]['lb'] / a)
    for j, v in enumerate(V):
        if v['lb'] is not None and v['lb'] == v['ub']:
            fixed.setdefault(find(j), set()).add(v['lb'])
    hcls = {find(j) for j in R[h]}
    assert len(hcls) == T
    # classify the classes of S
    plus1 = {k for k, v in S.items() if v == 1}
    minus1 = {k for k, v in S.items() if v == -1}
    other = {k: v for k, v in S.items() if abs(v) != 1}
    assert plus1 == hcls, 'tank-1 inflow classes must be the horizon variables'
    assert all(k in fixed and len(fixed[k]) == 1 for k in minus1)
    dsum = sum(next(iter(fixed[k])) for k in minus1)
    assert len(minus1) == T
    init = {k: v for k, v in other.items() if k in fixed}
    final = {k: v for k, v in other.items() if k not in fixed}
    assert len(init) == 3 and len(final) == 3
    assert all(v > 0 for v in init.values()) and all(v < 0 for v in final.values())
    # identity on feasible points: sum_t h_t - sum_t d_t + sum init_k * L0_k + sum final_k * E_k = 0
    # => sum_k (-final_k) E_k = sum h - sum d + sum init_k L0_k >= c - dsum + sum init_k L0_k
    rhs = c - dsum + sum(v * next(iter(fixed[k])) for k, v in init.items())
    coefs = sorted(-v for v in final.values())
    names = {k: [V[j]['name'] for j in range(len(V)) if find(j) == k] for k in final}
    return dict(T=T, c=c, dsum=dsum, c_minus_dsum=c - dsum, coefs=coefs, rhs=rhs, final_classes=names,
                n_copy=len(copy_rows), n_bal=len(bal))

for T in [2, 3, 4, 6, 9, 12, 18, 24]:
    r = run(T)
    print(T, 'c =', r['c'], '= %s' % float(r['c']), 'sum d =', r['dsum'], 'c - sum d =', r['c_minus_dsum'],
          'coefs', [str(x) for x in r['coefs']], 'rhs', r['rhs'], float(r['rhs']), 'copy', r['n_copy'], 'bal', r['n_bal'])
    if T == 6: print('  final-level classes:', r['final_classes'])
