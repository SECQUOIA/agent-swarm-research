"""Dossier check (camshape): exact-rational recomputation from the OSIL text, written from scratch.

Reads camshape{n}.osil from the current directory. All constants are parsed as exact decimal
Fractions. No floating point is used in any decision; floats appear only in printed summaries.

Checks:
  A. structure of every row / bound / objective coefficient against the expected camshape model;
  B. Chebyshev U_m(c/2) >= 0 (m <= n-1), S_j > 0, and the analytic test c/2 > cos(pi/n);
  C. envelope E (greatest element of the relaxation) and the bound -c0 * sum E, exactly;
  D. exact feasibility of (r, d) = (E, diff E) for EVERY OSIL row and bound, evaluated generically
     from the parsed sparse data (not from the structural template);
  E. hypotheses of the dossier's analytic feasibility lemma (contact/concavity case split),
     the phase structure, the omitted COPS curvature row (pair (1,2)), and strict feasibility facts;
  F. safe decimal displays (rounded toward -inf at 14 decimals) vs the summary strings;
  G. exact evaluation of the MINLPLib .sol points (objective - optimum, max violation).
"""
import json
import math
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

sys.set_int_max_str_digits(0)
NS = '{os.optimizationservices.org}'
INF = None  # marker


def els(node):
    """expand <el mult= incr=> lists to a list of strings/Fractions (exact)."""
    out = []
    for e in node.findall(NS + 'el'):
        mult = int(e.get('mult', '1'))
        incr = e.get('incr')
        v = Fr(e.text.strip())
        for k in range(mult):
            out.append(v + (Fr(incr) * k if incr is not None else 0))
    return out


def bnd(s, default):
    if s is None:
        return default
    if s in ('INF', 'inf', '+INF'):
        return 'INF'
    if s in ('-INF', '-inf'):
        return '-INF'
    return Fr(s)


def read_osil(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + 'instanceData')
    vars_ = data.find(NS + 'variables').findall(NS + 'var')
    nv = len(vars_)
    lb = [bnd(v.get('lb'), Fr(0)) for v in vars_]
    ub = [bnd(v.get('ub'), 'INF') for v in vars_]
    vtype = [v.get('type', 'C') for v in vars_]
    names = [v.get('name') for v in vars_]
    objs = data.find(NS + 'objectives').findall(NS + 'obj')
    assert len(objs) == 1
    ob = objs[0]
    obj = dict(sense=ob.get('maxOrMin'), constant=Fr(ob.get('constant', '0')),
               lin={int(c.get('idx')): Fr(c.text.strip()) for c in ob.findall(NS + 'coef')})
    cons = data.find(NS + 'constraints').findall(NS + 'con')
    nc = len(cons)
    rows = [dict(name=c.get('name'), lb=bnd(c.get('lb'), '-INF'), ub=bnd(c.get('ub'), 'INF'),
                 constant=Fr(c.get('constant', '0')), lin={}, quad=[]) for c in cons]
    L = data.find(NS + 'linearConstraintCoefficients')
    start = [int(x) for x in els(L.find(NS + 'start'))]
    assert L.find(NS + 'colIdx') is not None, 'row-major storage expected'
    col = [int(x) for x in els(L.find(NS + 'colIdx'))]
    val = els(L.find(NS + 'value'))
    assert len(start) == nc + 1 and len(col) == len(val) == start[-1]
    for i in range(nc):
        for k in range(start[i], start[i + 1]):
            assert col[k] not in rows[i]['lin']
            rows[i]['lin'][col[k]] = val[k]
    Q = data.find(NS + 'quadraticCoefficients')
    oquad = []
    for q in Q.findall(NS + 'qTerm'):
        t = (int(q.get('idxOne')), int(q.get('idxTwo')), Fr(q.get('coef')))
        i = int(q.get('idx'))
        if i == -1:
            oquad.append(t)
        else:
            rows[i]['quad'].append(t)
    assert data.find(NS + 'nonlinearExpressions') is None
    obj['quad'] = oquad
    return dict(nv=nv, lb=lb, ub=ub, vtype=vtype, names=names, obj=obj, rows=rows)


def structure(M, n):
    """Assert the camshape structure; return the constants (exact Fractions)."""
    assert M['nv'] == 2 * n - 1 and len(M['rows']) == 2 * n
    assert all(t == 'C' for t in M['vtype'])
    ob = M['obj']
    assert ob['sense'] == 'min' and ob['constant'] == 0 and ob['quad'] == []
    assert sorted(ob['lin']) == list(range(n)) and len(set(ob['lin'].values())) == 1
    c0 = -ob['lin'][0]
    assert c0 > 0
    rows = M['rows']
    c = None
    # rows 0..n-3: G_j for j = 2..n-1 (0-based r indices j-2, j-1, j)
    for j in range(2, n):
        R = rows[j - 2]
        a, b, d = j - 2, j - 1, j
        assert R['lin'] == {} and R['constant'] == 0 and R['lb'] == '-INF' and R['ub'] == 0
        qs = {(min(p, q), max(p, q)): v for p, q, v in R['quad']}
        assert len(qs) == 3 == len(R['quad'])
        assert qs[(a, b)] == -1 and qs[(b, d)] == -1
        if c is None:
            c = qs[(a, d)]
        assert qs[(a, d)] == c
    R = rows[n - 2]  # G_1
    assert R['lin'] == {0: Fr(-1), 1: c} and [(min(p, q), max(p, q), v) for p, q, v in R['quad']] == [(0, 1, Fr(-1))]
    assert R['lb'] == '-INF' and R['ub'] == 0 and R['constant'] == 0
    R = rows[n - 1]  # G_n
    assert set(R['lin']) == {n - 2, n - 1} and R['lin'][n - 1] == -2
    c2 = R['lin'][n - 2]
    assert [(min(p, q), max(p, q), v) for p, q, v in R['quad']] == [(n - 2, n - 1, Fr(-1))]
    assert R['lb'] == '-INF' and R['ub'] == 0 and R['constant'] == 0
    R = rows[n]  # E row
    assert R['lin'] == {n - 1: Fr(-4)} and R['quad'] == [(n - 1, n - 1, c)] and R['ub'] == 0 and R['lb'] == '-INF'
    for i in range(1, n):  # D_i: r_i - r_{i+1} + d_i = 0
        R = rows[n + i]
        assert R['lin'] == {i - 1: Fr(1), i: Fr(-1), n + i - 1: Fr(1)} and R['quad'] == []
        assert R['lb'] == 0 and R['ub'] == 0 and R['constant'] == 0
    lb, ub = M['lb'], M['ub']
    assert lb[0] == 1 and ub[n - 1] == 2
    for j in range(1, n - 1):
        assert lb[j] == 1 and ub[j] == 2
    ub1, lbn = ub[0], lb[n - 1]
    assert lb[n] == '-INF' and ub[n] == 'INF'
    alpha = ub[n + 1]
    for i in range(n + 1, 2 * n - 1):
        assert lb[i] == -alpha and ub[i] == alpha
    return dict(c0=c0, c=c, c2=c2, ub1=ub1, lbn=lbn, alpha=alpha)


def certificate(K, n):
    c, ub1, al = K['c'], K['ub1'], K['alpha']
    U = [Fr(1), c]
    while len(U) < n:
        U.append(c * U[-1] - U[-2])
    S = [Fr(1), 1 / ub1]
    while len(S) < n + 1:
        S.append(c * S[-1] - S[-2])
    ubv = [None, ub1] + [Fr(2)] * (n - 1)
    R = [None] + [(1 / S[j]) if S[j] > 0 else None for j in range(1, n + 1)]
    B = [None] + [min(R[j], ubv[j]) if R[j] is not None else ubv[j] for j in range(1, n + 1)]
    # greatest element: E_1 = B_1; for j >= 2, E_j = min_{k >= 2} (B_k + al*|j-k|) (direct O(n^2), no passes)
    # forward/backward min-plus passes over the slope-constrained pairs (2,3),...,(n-1,n)
    F = [None, B[1], B[2]] + [None] * (n - 2)
    for j in range(3, n + 1):
        F[j] = min(B[j], F[j - 1] + al)
    E = F[:]
    for j in range(n - 1, 1, -1):
        E[j] = min(F[j], E[j + 1] + al)
    if n <= 100:  # cross-check against the direct definition E_j = min_{k>=2} (B_k + al |j-k|)
        assert E[2:] == [min(B[k] + al * abs(j - k) for k in range(2, n + 1)) for j in range(2, n + 1)]
    return dict(U=U, S=S, R=R, B=B, E=E)


def evaluate(M, x):
    """generic exact evaluation of all rows and bounds at x (list of Fractions, 0-based)."""
    worst_row = Fr(0)
    worst_name = None
    act = []
    for R in M['rows']:
        v = R['constant'] + sum(a * x[k] for k, a in R['lin'].items()) + sum(a * x[p] * x[q] for p, q, a in R['quad'])
        viol = Fr(0)
        if R['ub'] != 'INF':
            viol = max(viol, v - R['ub'])
        if R['lb'] != '-INF':
            viol = max(viol, R['lb'] - v)
        if viol > worst_row:
            worst_row, worst_name = viol, R['name']
        act.append(v)
    worst_b = Fr(0)
    for k in range(M['nv']):
        if M['lb'][k] != '-INF':
            worst_b = max(worst_b, M['lb'][k] - x[k])
        if M['ub'][k] != 'INF':
            worst_b = max(worst_b, x[k] - M['ub'][k])
    ob = M['obj']
    f = ob['constant'] + sum(a * x[k] for k, a in ob['lin'].items()) + sum(a * x[p] * x[q] for p, q, a in ob['quad'])
    return dict(row_viol=worst_row, row=worst_name, bnd_viol=worst_b, obj=f, act=act)


def dec(q, digits):
    """decimal string of q truncated toward -inf at `digits` decimals (safe lower display)."""
    s = 10 ** digits
    fl = (q.numerator * s) // q.denominator
    sign = '-' if fl < 0 else ''
    a = abs(fl)
    return f"{sign}{a // s}.{str(a % s).zfill(digits)}"


def dec_up(q, digits):
    s = 10 ** digits
    ce = -((-q.numerator * s) // q.denominator)
    sign = '-' if ce < 0 else ''
    a = abs(ce)
    return f"{sign}{a // s}.{str(a % s).zfill(digits)}"


def read_sol(path, M):
    idx = {nm: k for k, nm in enumerate(M['names'])}
    x = [Fr(0)] * M['nv']
    for line in open(path):
        p = line.split()
        if len(p) != 2 or p[0] == 'objvar':
            continue
        x[idx[p[0]]] = Fr(p[1])
    return x


SUMMARY = {100: '-4.28414712174675', 200: '-4.27850023299273', 400: '-4.27568847892555', 800: '-4.27427414195420'}


def main(n):
    M = read_osil(f'camshape{n}.osil')
    K = structure(M, n)
    C = certificate(K, n)
    U, S, R, B, E = C['U'], C['S'], C['R'], C['B'], C['E']
    c, al, ub1, lbn, c2, c0 = K['c'], K['alpha'], K['ub1'], K['lbn'], K['c2'], K['c0']
    out = dict(n=n, consts={k: str(v) if v.denominator == 1 else f"{float(v):.17g}" for k, v in K.items()})
    out['const_strings_exact'] = {k: (str(v.numerator) + '/' + str(v.denominator)) if len(str(v.denominator)) < 25 else 'long' for k, v in K.items()}
    # B: Green's function positivity
    out['U_min'] = float(min(U[:n]))
    out['U_nonneg'] = all(u >= 0 for u in U[:n])
    out['U_max'] = float(max(U[:n]))
    out['sumU'] = float(sum(U[:n - 1]))
    out['S_pos'] = all(s > 0 for s in S[1:n + 1])
    out['S_min'] = float(min(S[1:n + 1]))
    out['S_decreasing'] = all(S[j + 1] < S[j] for j in range(0, n))
    # analytic sufficient test: c/2 > cos(pi/n)  <=> arccos(c/2) < pi/n  => U_m > 0 for m <= n-1
    # rigorous: use Taylor bound cos(x) <= 1 - x^2/2 + x^4/24 with x = pi/n, pi < 355/113
    x_hi = Fr(355, 113) / n   # > pi/n ; cos decreasing on [0, pi] so cos(pi/n) < cos(...)? no: need upper bound of cos(pi/n)
    x_lo = Fr(333, 106) / n   # < pi/n  (333/106 = 3.14150... < pi)
    cos_up = 1 - x_lo ** 2 / 2 + x_lo ** 4 / 24  # cos(pi/n) <= cos(x_lo) <= 1 - x_lo^2/2 + x_lo^4/24
    out['analytic_cheb_test'] = (c / 2 > cos_up) and (c < 2)
    # C: bound
    sumE = sum(E[1:])
    opt = -c0 * sumE
    out['opt_30'] = dec(opt, 30)
    out['opt_safe14'] = dec(opt, 14)
    out['summary_display'] = SUMMARY[n]
    out['summary_display_valid'] = Fr(SUMMARY[n]) <= opt
    out['summary_display_is_floor14'] = dec(opt, 14) == SUMMARY[n]
    out['opt_denominator_digits'] = len(str(opt.denominator))
    # D: exact feasibility of the envelope point, generic evaluation
    x = [E[j] for j in range(1, n + 1)] + [E[i + 1] - E[i] for i in range(1, n)]
    ev = evaluate(M, x)
    out['E_row_viol'] = str(ev['row_viol'])
    out['E_bnd_viol'] = str(ev['bnd_viol'])
    out['E_obj_equals_bound'] = (ev['obj'] == opt)
    act = ev['act']
    out['active_G_count'] = sum(1 for i in range(0, n) if act[i] == 0)  # rows 0..n-1 are the n convexity rows
    out['G_n_slack'] = float(-act[n - 1])
    out['E_row_slack'] = float(-act[n])
    # E: structure / lemma hypotheses
    onR = [j for j in range(1, n + 1) if R[j] is not None and E[j] == R[j]]
    m = max(onR)
    out['m_contact_last'] = m
    out['contact_prefix'] = onR == list(range(1, m + 1))
    tail_ok = all(E[j] == min(R[m] + al * (j - m), Fr(2)) for j in range(m, n + 1))
    out['tail_is_min_affine_2'] = tail_ok
    first2 = min(j for j in range(1, n + 1) if E[j] == 2)
    out['first_at_2'] = first2
    out['n_at_2'] = n - first2 + 1
    out['n_slope_phase'] = first2 - 1 - m
    out['R_increasing'] = all(R[j + 1] > R[j] for j in range(1, n))
    out['R_increments_increasing'] = all(R[j + 2] - R[j + 1] > R[j + 1] - R[j] for j in range(1, n - 1))
    out['m_def_check'] = (R[m] - R[m - 1] <= al) and (R[m + 1] - R[m] > al)
    out['R1_eq_ub1'] = R[1] == ub1
    out['E_le_R'] = all(E[j] <= R[j] for j in range(1, n + 1))
    out['E_ge_1'] = all(E[j] >= 1 for j in range(1, n + 1))
    out['E_n_eq_2'] = E[n] == 2 and E[n - 1] == 2
    out['lbn_le_2'] = lbn <= 2
    out['ub1_le_1_plus_alpha'] = ub1 <= 1 + al
    out['c_lt_2'] = c < 2
    out['c2_le_4'] = c2 <= 4
    out['c2_minus_2c'] = float(c2 - 2 * c)
    out['E_lipschitz_2n'] = all(abs(E[j + 1] - E[j]) <= al for j in range(2, n))
    # contact/concavity case split, checked row by row
    u = [Fr(1)] + [1 / E[j] for j in range(1, n + 1)]
    caseA = caseB = 0
    for j in range(1, n):
        ej = u[j - 1] - c * u[j] + u[j + 1]
        assert ej >= 0
        if E[j] == R[j]:
            caseA += 1
        else:
            assert E[j - 1] + E[j + 1] <= 2 * E[j], j  # concavity used in case B
            assert ej >= (2 - c) * u[j]
            caseB += 1
    out['caseA_rows'] = caseA
    out['caseB_rows'] = caseB
    # slack of e_m (first non-contact row)
    out['e_m_slack'] = float(u[m - 1] - c * u[m] + u[m + 1])
    # omitted COPS curvature row on (r_1, r_2) and COPS end rows
    out['omitted_pair12'] = float(abs(E[2] - E[1]))
    out['omitted_pair12_ok'] = abs(E[2] - E[1]) <= al
    out['alpha'] = float(al)
    # strict greatest element: any feasible r <= E componentwise; uniqueness follows
    # G: MINLPLib points
    pts = {}
    for p in ('p1', 'p2'):
        try:
            xs = read_sol(f'camshape{n}.{p}.sol', M)
        except FileNotFoundError:
            continue
        ev = evaluate(M, xs)
        pts[p] = dict(obj=float(ev['obj']), obj_minus_opt=float(ev['obj'] - opt), row_viol=float(ev['row_viol']),
                      row=ev['row'], bnd_viol=float(ev['bnd_viol']))
    out['minlplib_points'] = pts
    return out, dict(E=E, R=R, S=S, U=U, K=K, opt=opt)


if __name__ == '__main__':
    res = []
    for a in sys.argv[1:]:
        o, _ = main(int(a))
        print(json.dumps(o, indent=1), flush=True)
        res.append(o)
    json.dump(res, open('check_exact.json', 'w'), indent=1)
