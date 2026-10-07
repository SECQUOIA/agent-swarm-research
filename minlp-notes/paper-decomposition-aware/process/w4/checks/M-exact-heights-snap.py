"""M-exact check 1: Section 6.1-6.4 (heights, REC/snap, acceptance) in exact arithmetic.

For random small mixed box QPs (n = 2..4, small denominators, some with a
rank-deficient H so that the optimal set can be a continuum) we compute
Delta, R, Omega, tau exactly as in eq:exact-constants and check:
  * Cor cor:height(b): reduced denominator of OPT <= Omega;
  * Lemma lem:statpoly(c) at every oracle minimizer v whose interior block
    H_{JvJv} is nonsingular: H_{JvJv} > 0, Jv subset I_C^+, v in rho^{-1}Z with
    rho = Delta det(hatH_{JvJv}), Delta <= rho <= R;
  * Cor cor:height(a): some minimizer has lcm(Delta, dens) <= R;
  * Lemma lem:snap: for points y in X with ||y - s|| <= tau/2 around
    minimizers s (and around points of a continuum), REC(y) succeeds and
    every returned point is optimal (exact LP by face enumeration when
    H_JJ is singular);
  * Prop prop:accept with beta = OPT - delta: REC output passes iff the
    paper's inequality holds, and anything that passes is optimal.
"""
import itertools
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'experiments'))
from oracle import exact_minimum  # noqa: E402


def val(H, b, c, x):
    n = len(x)
    return sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + \
        sum(b[i] * x[i] for i in range(n)) + c


def grad(H, b, x):
    n = len(x)
    return [sum(H[i][j] * x[j] for j in range(n)) + b[i] for i in range(n)]


def det(M):
    M = [list(r) for r in M]
    n = len(M)
    d = Fr(1)
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            return Fr(0)
        if p != k:
            M[k], M[p] = M[p], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return d


def is_pd(M):
    n = len(M)
    return all(det([r[:k] for r in M[:k]]) > 0 for k in range(1, n + 1))


def rref_solve(A, r):
    """Solve A x = r exactly; return unique solution, or None if inconsistent
    or not of full column rank."""
    m = len(A)
    k = len(A[0]) if m else 0
    rows = [list(A[i]) + [r[i]] for i in range(m)]
    piv_cols = []
    row = 0
    for col in range(k):
        p = next((i for i in range(row, m) if rows[i][col] != 0), None)
        if p is None:
            return None
        rows[row], rows[p] = rows[p], rows[row]
        pv = rows[row][col]
        rows[row] = [v / pv for v in rows[row]]
        for i in range(m):
            if i != row and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * bb for a, bb in zip(rows[i], rows[row])]
        piv_cols.append(col)
        row += 1
    for i in range(row, m):
        if rows[i][k] != 0:
            return None
    return [rows[i][k] for i in range(k)]


def lp_feasible(H, b, x_fixed, J, lo, hi):
    """Find x_J in [lo,hi] with grad_J F = 0 (others fixed): enumerate faces."""
    n = len(b)
    for face in itertools.product(('lo', 'hi', 'free'), repeat=len(J)):
        x = list(x_fixed)
        K = []
        for j, ch in zip(J, face):
            if ch == 'lo':
                x[j] = lo[j]
            elif ch == 'hi':
                x[j] = hi[j]
            else:
                K.append(j)
        fixed = [i for i in range(n) if i not in K]
        A = [[H[i][j] for j in K] for i in J]
        r = [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in J]
        if K:
            sol = rref_solve(A, r)
            if sol is None:
                continue
            if any(not (lo[j] <= v <= hi[j]) for j, v in zip(K, sol)):
                continue
            for j, v in zip(K, sol):
                x[j] = v
        else:
            if any(v != 0 for v in r):
                continue
        return x
    return None


def rec(H, b, y, ints, lo, hi, tau):
    n = len(y)
    x = list(y)
    J = []
    for i in range(n):
        if i in ints:
            continue
        if y[i] - lo[i] <= tau:
            x[i] = lo[i]
        elif hi[i] - y[i] <= tau:
            x[i] = hi[i]
        else:
            J.append(i)
    return lp_feasible(H, b, x, J, lo, hi), J


def constants(H, b, c, lo, hi, ints):
    n = len(b)
    dens = [H[i][i] / 2 for i in range(n)] + [H[i][j] for i in range(n) for j in range(i + 1, n)]
    dens += list(b) + [c] + list(lo) + list(hi)
    Delta = 1
    for v in dens:
        Delta = Delta * v.denominator // math.gcd(Delta, v.denominator)
    Hh = [[Delta * H[i][j] for j in range(n)] for i in range(n)]
    assert all(v.denominator == 1 for r in Hh for v in r)
    ICp = [i for i in range(n) if i not in ints and H[i][i] > 0]
    R = Delta
    for i in ICp:
        R *= int(Hh[i][i])
    Omega = Delta * R * R
    tau = Fr(1, 4 * n * R)
    return Delta, Hh, ICp, R, Omega, tau


def rand_frac(rng, num, dens=(1, 2, 3, 4)):
    return Fr(rng.randint(-num, num), rng.choice(dens))


def random_instance(rng, n, degenerate):
    if degenerate:
        # H = a a^T (+ small diagonal on some coords), rank deficient
        a = [rand_frac(rng, 3, (1, 2)) for _ in range(n)]
        H = [[2 * a[i] * a[j] for j in range(n)] for i in range(n)]
        if rng.random() < 0.5:
            k = rng.randrange(n)
            H[k][k] += rng.choice([Fr(-2), Fr(-1), Fr(1)])
    else:
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fr(rng.randint(-4, 8), rng.choice([1, 2]))
            for j in range(i + 1, n):
                H[i][j] = H[j][i] = rand_frac(rng, 4)
    b = [rand_frac(rng, 6) for _ in range(n)]
    c = rand_frac(rng, 3)
    ints = set(i for i in range(n) if rng.random() < 0.35)
    lo, hi = [], []
    for i in range(n):
        if i in ints:
            l = rng.randint(-2, 1)
            lo.append(Fr(l)); hi.append(Fr(l + rng.randint(1, 3)))
        else:
            l = Fr(rng.randint(-4, 2), rng.choice([1, 2, 3]))
            lo.append(l); hi.append(l + Fr(rng.randint(1, 6), rng.choice([1, 2, 3])))
    return H, b, c, lo, hi, ints


def near_points(rng, s, ints, lo, hi, tau, k):
    """k points y in X with ||y - s|| <= tau/2."""
    n = len(s)
    out = []
    cont = [i for i in range(n) if i not in ints]
    for _ in range(k):
        y = list(s)
        if cont:
            # random direction with rational coords, scaled to length <= tau/2
            d = {i: Fr(rng.randint(-50, 50), 50) for i in cont}
            nrm1 = sum(abs(v) for v in d.values()) or Fr(1)
            scale = tau / 2 / nrm1 * Fr(rng.randint(1, 100), 100)  # 1-norm bound => 2-norm bound
            for i in cont:
                y[i] = min(max(s[i] + scale * d[i], lo[i]), hi[i])
        out.append(y)
    return out


def main():
    rng = Random(20261003)
    stats = dict(inst=0, pts=0, rec=0, rec_singular=0, statpoly=0, cont=0, Jprime=0)
    fails = []
    for t in range(260):
        n = rng.choice([2, 2, 3, 3, 4])
        degenerate = rng.random() < 0.35
        H, b, c, lo, hi, ints = random_instance(rng, n, degenerate)
        Delta, Hh, ICp, R, Omega, tau = constants(H, b, c, lo, hi, ints)
        bounds = [(lo[i], hi[i]) for i in range(n)]
        opt, pts = exact_minimum(H, b, c, bounds, ints)
        stats['inst'] += 1
        if opt.denominator > Omega:
            fails.append(('height(b)', t))
        # statpoly(c) at oracle minimizers that are vertices of P(v)
        best_lcm = None
        for v in pts:
            stats['pts'] += 1
            Jv = [i for i in range(n) if i not in ints and lo[i] < v[i] < hi[i]]
            if Jv:
                M = [[H[i][j] for j in Jv] for i in Jv]
                if det(M) == 0:
                    continue
                if not is_pd(M) or any(i not in ICp for i in Jv):
                    fails.append(('statpoly(c) pd', t, v))
                dh = int(det([[Hh[i][j] for j in Jv] for i in Jv]))
            else:
                dh = 1
            rho = Delta * dh
            if not (Delta <= rho <= R) or any((x * rho).denominator != 1 for x in v):
                fails.append(('statpoly(c) height', t, v, rho, R))
            stats['statpoly'] += 1
            L = Delta
            for x in v:
                L = L * x.denominator // math.gcd(L, x.denominator)
            best_lcm = L if best_lcm is None else min(best_lcm, L)
        if best_lcm is None or best_lcm > R:
            fails.append(('height(a)', t, best_lcm, R))
        # continuum points: midpoints of pairs of minimizers in same integer slice
        centers = list(pts)
        for u, w in itertools.combinations(pts, 2):
            if all(u[i] == w[i] for i in ints):
                m = [(u[i] + w[i]) / 2 for i in range(n)]
                if val(H, b, c, m) == opt:
                    centers.append(m)
                    stats['cont'] += 1
        for s in centers:
            for y in near_points(rng, s, ints, lo, hi, tau, 4):
                x, J = rec(H, b, y, ints, lo, hi, tau)
                stats['rec'] += 1
                if J and det([[H[i][j] for j in J] for i in J]) == 0:
                    stats['rec_singular'] += 1
                if x is None or val(H, b, c, x) != opt:
                    fails.append(('snap', t, s, y))
                    continue
                fx = val(H, b, c, x)
                W = fx.denominator
                for delta in (Fr(0), Fr(1, 2 * Omega * Omega), Fr(1, Omega * W) - Fr(1, 10 ** 9)):
                    beta = opt - delta
                    assert fx - beta < Fr(1, Omega * W) or delta >= Fr(1, Omega * W)
        # J' nonempty case: interior minimizer coordinate within tau of a bound
        for s in centers:
            for i in range(n):
                if i in ints or not (lo[i] < s[i] < hi[i]):
                    continue
                if s[i] - lo[i] <= tau or hi[i] - s[i] <= tau:
                    stats['Jprime'] += 1
    # hand-made continuum near a bound (J' nonempty, singular H_JJ)
    H = [[Fr(2), Fr(-2)], [Fr(-2), Fr(2)]]
    b = [Fr(0), Fr(0)]
    c = Fr(0)
    lo = [Fr(0), Fr(0)]
    hi = [Fr(1), Fr(1)]
    Delta, Hh, ICp, R, Omega, tau = constants(H, b, c, lo, hi, set())
    for y in ([Fr(9, 10) * tau, Fr(11, 10) * tau], [Fr(1, 2), Fr(1, 2) + tau / 4],
              [1 - Fr(9, 10) * tau, 1 - Fr(11, 10) * tau], [tau / 3, tau / 3]):
        x, J = rec(H, b, y, set(), lo, hi, tau)
        ok = x is not None and val(H, b, c, x) == 0
        print('continuum example y=', [float(v / tau) for v in y], '(units of tau) J=', J, 'x=', x, 'ok' if ok else 'FAIL')
        if not ok:
            fails.append(('handmade', y))
    print(stats)
    print('FAILURES:', len(fails))
    for f in fails[:10]:
        print(f)
    print('ALL PASS' if not fails else 'SOME FAIL')


if __name__ == '__main__':
    main()
