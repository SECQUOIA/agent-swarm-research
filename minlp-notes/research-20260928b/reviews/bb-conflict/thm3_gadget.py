"""Independent check of Theorem 3 (correlated-pair gadget) of the scout report.

Block j: features u = e1, v = (cos th, sin th) in its own R^2, response
y_j = s (u+v)/|u+v|, ridge lam, global budget sum z <= k.
Perspective relaxation (after minimizing out beta):
    g(z) = sum_j y_j' (I + (z_u u u' + z_v v v')/lam)^{-1} y_j.

Checks:
  1. closed forms for g00, g10, g11, ghat(1/2,1/2), delta; condition (i) <=> cos th > 0.
  2. reduced (symmetrized) node relaxation agrees with the full 2k-dim CVXPY model.
  3. exact minimum number of leaves over all variable-branching trees (DP over
     multisets of block states), compared with 2^k.
  4. k = 2: exact minimum number of classes over arbitrary convex pieces that
     cover the feasible supports (hypergraph partition number of Section 3.1).
  5. part (c): root value of the per-block disjunctive hull relaxation equals OPT.
"""
import itertools, functools, math, sys
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize, linprog

TH, S, LAM = 0.3, 3.0, 1.0


def vecs(th, s):
    u = np.array([1.0, 0.0]); v = np.array([math.cos(th), math.sin(th)])
    w = (u + v) / np.linalg.norm(u + v)
    return u, v, s * w


def ghat(z1, z2, th=TH, s=S, lam=LAM):
    u, v, y = vecs(th, s)
    M = np.eye(2) + (z1 * np.outer(u, u) + z2 * np.outer(v, v)) / lam
    return float(y @ np.linalg.solve(M, y))


def closed_forms(th=TH, s=S, lam=LAM):
    c = math.cos(th)
    g00 = s * s
    g10 = s * s * (1 + 2 * lam - c) / (2 * (1 + lam))
    g11 = s * s * lam / (lam + 1 + c)
    gh = 2 * lam * s * s / (2 * lam + 1 + c)
    delta = s * s * math.sin(th) ** 2 / (2 * (1 + lam) * (1 + 2 * lam + c))
    return g00, g10, g11, gh, delta


def check_closed_forms():
    print("== 1. closed forms ==")
    worst = 0.0
    rng = np.random.default_rng(0)
    for _ in range(200):
        th = rng.uniform(0.01, math.pi - 0.01); s = rng.uniform(0.1, 5); lam = rng.uniform(0.05, 5)
        g00, g10, g11, gh, delta = closed_forms(th, s, lam)
        num = (ghat(0, 0, th, s, lam), ghat(1, 0, th, s, lam), ghat(0, 1, th, s, lam),
               ghat(1, 1, th, s, lam), ghat(.5, .5, th, s, lam))
        worst = max(worst, abs(num[0] - g00), abs(num[1] - g10), abs(num[2] - g10),
                    abs(num[3] - g11), abs(num[4] - gh), abs((g10 - gh) - delta))
        cond_i = (g00 - g10) - (g10 - g11)
        assert (cond_i > 1e-12) == (math.cos(th) > 1e-12) or abs(math.cos(th)) < 1e-6, (th, cond_i)
        assert delta > 0
    print("max abs deviation closed form vs numeric over 200 random (th,s,lam): %.2e" % worst)
    print("condition (i) held exactly when cos(th) > 0 in all 200 samples; delta > 0 in all")
    g00, g10, g11, gh, delta = closed_forms()
    print("th=0.3,s=3,lam=1: g00=%.5f g10=%.5f g11=%.5f ghat(.5,.5)=%.5f delta=%.5f "
          "g00-g10=%.4f g10-g11=%.4f" % (g00, g10, g11, gh, delta, g00 - g10, g10 - g11))
    # th = pi/2: equality in (i)
    g00, g10, g11, gh, delta = closed_forms(math.pi / 2)
    print("th=pi/2: (g00-g10)-(g10-g11) = %.3e (equality: condition (i) fails)" % ((g00 - g10) - (g10 - g11)))


# ---------------------------------------------------------------- node relaxation
# block state: pair (a, b) with a, b in {'F', 0, 1}; canonical form uses the u/v symmetry.
def canon(a, b):
    key = {'F': 2, 0: 0, 1: 1}
    return (a, b) if key[a] >= key[b] else (b, a)


TYPES = [canon(a, b) for a in ('F', 0, 1) for b in ('F', 0, 1)]
TYPES = sorted(set(TYPES), key=str)


def relax_reduced(state, k, th=TH, s=S, lam=LAM):
    """state: tuple of counts per TYPES. Returns node bound (inf if infeasible).
    By convexity + symmetry all blocks of one type share one z, and type (F,F)
    uses z_u = z_v."""
    fixed_budget = 0.0; const = 0.0; free = []
    for t, cnt in zip(TYPES, state):
        if cnt == 0:
            continue
        a, b = t
        if a != 'F' and b != 'F':
            fixed_budget += cnt * (a + b); const += cnt * ghat(a, b, th, s, lam)
        elif a == 'F' and b == 'F':
            free.append((cnt, 2.0, lambda x: ghat(x, x, th, s, lam)))
        else:
            other = b if a == 'F' else a
            fixed_budget += cnt * other
            free.append((cnt, 1.0, (lambda o: (lambda x: ghat(x, o, th, s, lam)))(other)))
    if fixed_budget > k + 1e-12:
        return math.inf
    if not free:
        return const
    slack = k - fixed_budget

    def f(x):
        return sum(c * fn(xi) for (c, _, fn), xi in zip(free, x))
    cons = [{'type': 'ineq', 'fun': lambda x: slack - sum(c * w * xi for (c, w, _), xi in zip(free, x))}]
    best = math.inf
    for x0 in (np.zeros(len(free)), np.full(len(free), min(1.0, slack / max(1e-9, sum(c * w for c, w, _ in free))))):
        r = minimize(f, x0, method='SLSQP', bounds=[(0, 1)] * len(free), constraints=cons,
                     options={'ftol': 1e-13, 'maxiter': 500})
        x = np.clip(r.x, 0, 1)
        if slack - sum(c * w * xi for (c, w, _), xi in zip(free, x)) >= -1e-9:
            best = min(best, f(x))
    return const + best


def relax_full_cvxpy(fix, k, th=TH, s=S, lam=LAM):
    """fix: dict var index -> 0/1 over 2k vars (2j = u_j, 2j+1 = v_j)."""
    u, v, y = vecs(th, s)
    z = cp.Variable(2 * k)
    obj = 0
    for j in range(k):
        M = np.eye(2) + (z[2 * j] * np.outer(u, u) + z[2 * j + 1] * np.outer(v, v)) / lam
        obj += cp.matrix_frac(y, M)
    cons = [z >= 0, z <= 1, cp.sum(z) <= k] + [z[i] == val for i, val in fix.items()]
    p = cp.Problem(cp.Minimize(obj), cons)
    p.solve(solver='CLARABEL')
    if p.status in ('infeasible', 'infeasible_inaccurate'):
        return math.inf
    return p.value


def state_of(fix, k):
    cnt = [0] * len(TYPES)
    for j in range(k):
        a = fix.get(2 * j, 'F'); b = fix.get(2 * j + 1, 'F')
        cnt[TYPES.index(canon(a, b))] += 1
    return tuple(cnt)


def check_reduced(k=3, trials=25):
    print("== 2. reduced relaxation vs full CVXPY model (k=%d) ==" % k)
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(trials):
        fix = {i: int(rng.integers(0, 2)) for i in range(2 * k) if rng.random() < 0.4}
        a = relax_reduced(state_of(fix, k), k); b = relax_full_cvxpy(fix, k)
        if math.isinf(a) or math.isinf(b):
            assert math.isinf(a) and math.isinf(b), (fix, a, b)
        else:
            worst = max(worst, abs(a - b))
    print("max |reduced - cvxpy| over %d random fixings: %.2e" % (trials, worst))


def min_leaves_varbranch(k, eps, th=TH, s=S, lam=LAM):
    g00, g10, g11, gh, delta = closed_forms(th, s, lam)
    OPT = k * g10
    thr = OPT - eps - 1e-9

    @functools.lru_cache(maxsize=None)
    def bound(state):
        return relax_reduced(state, k, th, s, lam)

    @functools.lru_cache(maxsize=None)
    def T(state):
        if bound(state) >= thr:
            return 1
        best = math.inf
        for ti, t in enumerate(TYPES):
            if state[ti] == 0 or 'F' not in t:
                continue
            a, b = t
            kids = []
            for val in (0, 1):
                na, nb = (val, b) if a == 'F' else (a, val)
                st = list(state); st[ti] -= 1; st[TYPES.index(canon(na, nb))] += 1
                kids.append(tuple(st))
            best = min(best, T(kids[0]) + T(kids[1]))
        return best
    root = [0] * len(TYPES); root[TYPES.index(('F', 'F'))] = k
    root = tuple(root)
    return T(root), bound(root), OPT


def check_min_trees(kmax=8):
    print("== 3. exact minimum variable-branching trees ==")
    g00, g10, g11, gh, delta = closed_forms()
    for eps in (1e-6, 0.9 * delta):
        for k in range(1, kmax + 1):
            L, rb, OPT = min_leaves_varbranch(k, eps)
            print("eps=%.4g k=%d: min leaves=%d (nodes=%d), 2^k=%d, root gap=%.5f, k*delta=%.5f"
                  % (eps, k, L, 2 * L - 1, 2 ** k, OPT - rb, k * delta))
            sys.stdout.flush()


def check_partition_k2(eps=1e-6):
    print("== 4. k=2: min number of admissible classes (arbitrary convex pieces) ==")
    k = 2
    g00, g10, g11, gh, delta = closed_forms()
    OPT = k * g10
    pts = [np.array(p, float) for p in itertools.product([0, 1], repeat=2 * k) if sum(p) <= k]
    u, v, y = vecs(TH, S)
    m = len(pts)

    def minconv(idx):
        lam_ = cp.Variable(len(idx))
        z = sum(lam_[i] * pts[j] for i, j in enumerate(idx))
        obj = 0
        for j in range(k):
            M = np.eye(2) + (z[2 * j] * np.outer(u, u) + z[2 * j + 1] * np.outer(v, v)) / LAM
            obj += cp.matrix_frac(y, M)
        p = cp.Problem(cp.Minimize(obj), [lam_ >= 0, cp.sum(lam_) == 1])
        p.solve(solver='CLARABEL')
        return p.value
    adm = {}
    for mask in range(1, 1 << m):
        idx = [j for j in range(m) if mask >> j & 1]
        # hereditary: if some subset missing one element is inadmissible, so is mask
        if any(not adm.get(mask & ~(1 << j), True) for j in idx if mask & ~(1 << j)):
            adm[mask] = False
            continue
        adm[mask] = (len(idx) == 1) or (minconv(idx) >= OPT - eps - 1e-7)

    @functools.lru_cache(maxsize=None)
    def P(rem):
        if rem == 0:
            return 0
        low = rem & -rem
        best = math.inf
        sub = rem
        while sub:
            if sub & low and adm[sub]:
                best = min(best, 1 + P(rem & ~sub))
            sub = (sub - 1) & rem
        return best
    nadm = sum(adm.values())
    print("feasible supports: %d, admissible classes: %d, min #classes = %d (2^k = %d)"
          % (m, nadm, P((1 << m) - 1), 2 ** k))


def check_hull_root(kmax=10):
    print("== 5. part (c): disjunctive block-hull relaxation at the root ==")
    g00, g10, g11, gh, delta = closed_forms()
    vals = [g00, g10, g10, g11]; sizes = [0, 1, 1, 2]
    for k in (2, 5, kmax):
        c = np.tile(vals, k)
        A_eq = np.kron(np.eye(k), np.ones((1, 4))); b_eq = np.ones(k)
        A_ub = np.tile(sizes, k)[None, :]; b_ub = [k]
        r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
        print("k=%d: hull root value=%.8f, OPT=k*g10=%.8f, diff=%.2e" % (k, r.fun, k * g10, r.fun - k * g10))


if __name__ == '__main__':
    check_closed_forms()
    check_reduced()
    check_hull_root()
    check_partition_k2()
    check_min_trees(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
