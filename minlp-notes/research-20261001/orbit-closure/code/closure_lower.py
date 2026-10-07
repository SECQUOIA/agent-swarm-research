"""Certified lower bound on the closure value z_cl,A(1, 1, 1) at the Proposition 16 corner
(Proposition 10, Section 5 of note.md): the closure strictly improves on the best single cut there.

Steps: cut generation (closure.py) gives orbit sets F_i (X_i = F_i^T M(sbar) = S_i + c_i J);
each X_i is rounded to rationals; for every ray j a rational mu_ij slightly below alpha_j is
certified exactly by sym(X_i) > 0 and sym(X_i (I + mu_ij N_j)) >= 0 (so sbar + mu_ij p_j lies in
C_{F_i} and alpha_j >= mu_ij); the weaker valid cuts sum_j lam_j / mu_ij >= 1 are then used in an
exact rational LP  min{1^T lam : lam >= 0, sum_j lam_j / mu_ij >= 1 for all i}  (all vertices
enumerated).  Its value is a certified lower bound on z_cl,A(1, 1, 1).
Compare: the recheck of the sfree note certified 0.9838 <= z_1,A(1,1,1) <= 0.9839.
Usage: python3 closure_lower.py [--save CERT.json | --verify CERT.json]
"""
import sys, itertools, warnings, argparse, json
from fractions import Fraction as Fr
warnings.filterwarnings('ignore')

sb = [Fr(-2), Fr(3), Fr(2)]
V = [[Fr(0), Fr(0), Fr(0)], [Fr(6), Fr(-2), Fr(1, 4)], [Fr(1), Fr(-5, 2), Fr(1, 2)]]
P = [[V[j][i] - sb[i] for i in range(3)] for j in range(3)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def sym(A):
    return [[A[0][0], (A[0][1] + A[1][0]) / 2], [(A[0][1] + A[1][0]) / 2, A[1][1]]]


def psd(X, strict=False):
    d = X[0][0] * X[1][1] - X[0][1] ** 2
    return (X[0][0] > 0 and d > 0) if strict else (X[0][0] >= 0 and X[1][1] >= 0 and d >= 0)


Mi = inv([[sb[2], sb[0]], [sb[1], Fr(1)]])
N = [mm(Mi, [[p[2], p[0]], [p[1], Fr(0)]]) for p in P]
I2 = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]

parser = argparse.ArgumentParser(description=__doc__)
mode = parser.add_mutually_exclusive_group()
mode.add_argument('--save', help='save rational sets, steps and exact LP result')
mode.add_argument('--verify', help='recheck saved rational data without cut generation')
args = parser.parse_args()
instance = dict(sbar=[str(v) for v in sb], verts=[[str(v) for v in row] for row in V])
saved = None
if args.verify:
    with open(args.verify) as fh:
        saved = json.load(fh)
    assert saved['instance'] == instance, 'wrong corner in saved certificate'
    records = saved['cuts']
else:
    import numpy as np
    from orbit_lib import Corner, theta_to_Sc
    from closure import closure_value
    sbf = np.array([float(v) for v in sb]); Pf = np.array([[float(v) for v in p] for p in P]).T
    cn = Corner(sbf, Pf)
    z, lam, cuts, thetas, hist = closure_value(cn, np.ones(3), fam='A', maxit=60, tol=1e-8)
    print('numerical closure value %.7f with %d generated cuts' % (z, len(cuts)))

    records = []
    for th in thetas:
        S, c = theta_to_Sc(th)
        if S is None:
            continue
        a = cn.cut_A(S, c)
        Sr = [[Fr(S[0, 0]).limit_denominator(10 ** 7), Fr(S[0, 1]).limit_denominator(10 ** 7)], [None, Fr(S[1, 1]).limit_denominator(10 ** 7)]]
        Sr[1][0] = Sr[0][1]
        cr = Fr(float(c)).limit_denominator(10 ** 7)
        X = [[Sr[0][0], Sr[0][1] + cr], [Sr[1][0] - cr, Sr[1][1]]]
        if not psd(sym(X), True):
            continue
        mus = []
        for j in range(3):
            if a[j] <= 1e-12:
                mu = Fr(10 ** 6)                # very long step, certified below like any other
            else:
                mu = Fr(1 / a[j] * (1 - 1e-6)).limit_denominator(10 ** 7)
            # shrink until certified exactly
            for _ in range(60):
                A = sym(mm(X, [[I2[r][k] + mu * N[j][r][k] for k in range(2)] for r in range(2)]))
                if psd(A):
                    break
                mu = mu * Fr(999, 1000)
            else:
                mu = None
            mus.append(mu)
        if all(mu is not None and mu > 0 for mu in mus):
            records.append(dict(X=[[str(v) for v in row] for row in X], mu=[str(v) for v in mus]))

# Recheck the same exact conditions for generated and saved rational data.
certified = []
for rec in records:
    X = [[Fr(v) for v in row] for row in rec['X']]
    mus = [Fr(v) for v in rec['mu']]
    assert len(X) == 2 and all(len(row) == 2 for row in X) and len(mus) == 3
    assert psd(sym(X), True), 'set does not contain the vertex in its interior'
    for j, mu in enumerate(mus):
        assert mu > 0
        A = sym(mm(X, [[I2[r][k] + mu * N[j][r][k] for k in range(2)] for r in range(2)]))
        assert psd(A), 'step membership not certified'
    certified.append(mus)
print('%d cuts certified exactly' % len(certified))

# exact LP: min sum lam s.t. sum_j lam_j / mu_ij >= 1, lam >= 0 ; enumerate vertices
rows = [([1 / mu for mu in mus], Fr(1)) for mus in certified]
rows += [([Fr(1) if k == j else Fr(0) for k in range(3)], Fr(0)) for j in range(3)]


def solve3(A, b):
    # Cramer's rule for 3x3
    def det3(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det3(A)
    if D == 0:
        return None
    out = []
    for k in range(3):
        Mk = [[b[r] if cc == k else A[r][cc] for cc in range(3)] for r in range(3)]
        out.append(det3(Mk) / D)
    return out


best = None
for trip in itertools.combinations(range(len(rows)), 3):
    A = [rows[t][0] for t in trip]; b = [rows[t][1] for t in trip]
    x = solve3(A, b)
    if x is None:
        continue
    if all(sum(r[0][k] * x[k] for k in range(3)) >= r[1] for r in rows):
        val = sum(x)
        if best is None or val < best[0]:
            best = (val, x)
val, x = best
print('exact LP value (certified lower bound on z_cl,A(1,1,1)): %s (approximately %.7f) at lam = %s' % (val, float(val), [float(v) for v in x]))
if saved is not None:
    assert Fr(saved['value']) == val, 'saved LP value differs from exact enumeration'
    assert [Fr(v) for v in saved['lam']] == x, 'saved minimizing point differs'
    print('saved rational certificate and exact LP result: PASS')
if args.save:
    with open(args.save, 'w') as fh:
        json.dump(dict(instance=instance, cuts=records, value=str(val), lam=[str(v) for v in x]), fh, indent=2)
        fh.write('\n')
    print('saved %d rational cuts to %s' % (len(records), args.save))
print('certified single-cut upper bound (sfree recheck): 0.9839;  closure lower bound exceeds it: %s'
      % ('PASS' if val > Fr(9839, 10000) else 'FAIL'))
sys.exit(0 if val > Fr(9839, 10000) else 1)
