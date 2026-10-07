"""Verification checks for group recB (Sections 7.4, 7.5, Appendix D).

1. Example ex:cr-flat: simulate CORE on V(v)=sum_t (v_{2t-1}-v_{2t})^2 for
   k=2,4 and check that level j keeps >= 2^{jk/2} cells and U-lambda_j=e_j.
2. Lemma lem:cr-height: sharper test with residual bounds of denominators up
   to 5 and k<=3. For every residual endpoint vector y, Psi(y) is computed by
   face enumeration; its reduced denominator W satisfies W <= Omega_K, and W
   divides Delta_K*rho^2 with rho = Delta_K*det(hat H_JJ) for the interior set
   J of a minimizing face solution with nonsingular block (Lemma statpoly(c)).
3. Theorem thm:cr-exact with accuracy eps = Omega_K^{-2}/2: on small
   instances, CORE stops by the first level with e_J <= eps, and the face
   enumeration of F(., y_U) passes the acceptance test of Prop. accept and
   returns OPT.
4. Proposition prop:cr-greedy(c): max over the base polytope of
   sum_i min{0, abar_i} equals min hat Phi (LP over greedy vectors, floats),
   and the optimal LP value of max{t : 0<=xi<=1, t + a^pi.xi <= 0} is
   -min hat Phi.
All exact parts use fractions.Fraction.
"""
import itertools
import random
from fractions import Fraction as Fr
from math import lcm

random.seed(20261003)


def det(M):
    M = [row[:] for row in M]
    n = len(M)
    d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for cc in range(c, n):
                M[r][cc] -= f * M[c][cc]
    return d


def solve(A, rhs):
    n = len(A)
    M = [A[i][:] + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                for cc in range(c, n + 1):
                    M[r][cc] -= f * M[c][cc]
    return [M[i][n] / M[i][i] for i in range(n)]


def quad(H, b, c, x):
    n = len(x)
    return (Fr(1, 2) * sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            + sum(b[i] * x[i] for i in range(n)) + c)


def box_min_faces(H, b, c, k):
    """Minimize 1/2 v^T H v + b^T v + c over [0,1]^k by face enumeration.
    Returns (value, minimizer, free set J of the face that produced it; the
    block H_JJ is nonsingular)."""
    best = None
    for pat in itertools.product((0, 1, 2), repeat=k):
        J = [i for i in range(k) if pat[i] == 2]
        fixed = {i: Fr(pat[i]) for i in range(k) if pat[i] != 2}
        if J:
            A = [[H[i][j] for j in J] for i in J]
            if det(A) == 0:
                continue
            rhs = [-(b[i] + sum(H[i][j] * fixed[j] for j in fixed)) for i in J]
            sol = solve(A, rhs)
            if sol is None or any(s < 0 or s > 1 for s in sol):
                continue
            v = [Fr(0)] * k
            for i in fixed:
                v[i] = fixed[i]
            for t, i in enumerate(J):
                v[i] = sol[t]
        else:
            v = [fixed[i] for i in range(k)]
        val = quad(H, b, c, v)
        if best is None or val < best[0]:
            best = (val, v, J)
    return best


# ---------------------------------------------------------------- 1. flat
def core_flat(k, levels):
    def V(v):
        return sum((v[2 * t] - v[2 * t + 1]) ** 2 for t in range(k // 2))
    L = 2
    cells = [tuple([Fr(0)] * k)]  # lower corners, side h
    U = None
    for j in range(levels + 1):
        h = Fr(1, 2 ** j)
        e = Fr(k * L, 8) * h * h
        lam = None
        keep = []
        for lo in cells:
            cm = min(V([lo[i] + h * s[i] for i in range(k)])
                     for s in itertools.product((0, 1), repeat=k))
            U = cm if U is None else min(U, cm)
            beta = cm - e
            lam = beta if lam is None else min(lam, beta)
            keep.append((lo, beta))
        kept = [lo for lo, beta in keep if beta <= U]
        assert U == 0 and lam == -e, (k, j, U, lam, e)
        assert len(kept) >= 2 ** (j * k // 2), (k, j, len(kept))
        cells = [tuple(lo[i] + (h / 2) * s[i] for i in range(k))
                 for lo in kept for s in itertools.product((0, 1), repeat=k)]
    return True


assert core_flat(2, 6)
assert core_flat(4, 3)
print("ex:cr-flat: retained >= 2^{jk/2} and U-lambda_j=e_j (k=2 to level 6, k=4 to level 3)")


# ---------------------------------------------------------------- 2. height
def rnd(dens):
    return Fr(random.randint(-7, 7), random.choice(dens))


def instance(k, r, dens=(1, 2, 3)):
    n = k + r
    o = [random.choice([-1, 1]) for _ in range(r)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                if i >= k:
                    H[i][i] = -abs(rnd(dens))
                else:
                    H[i][i] = Fr(random.randint(0, 9), random.choice(dens))
            else:
                h = rnd(dens)
                if i >= k and j >= k:
                    h = -abs(h) * o[i - k] * o[j - k]
                H[i][j] = H[j][i] = h
    # make the core block PSD-ish sometimes and indefinite sometimes: leave random
    b = [rnd(dens) for _ in range(n)]
    c = rnd(dens)
    lo = [Fr(random.randint(-6, 0), random.choice((1, 2, 3, 4, 5))) for _ in range(r)]
    up = [lo[i] + Fr(random.randint(1, 6), random.choice((1, 2, 3, 4, 5))) for i in range(r)]
    return H, b, c, lo, up, o


def restrict(H, b, c, k, y):
    r = len(y)
    Hb = [[H[i][j] for j in range(k)] for i in range(k)]
    bb = [b[i] + sum(H[i][k + j] * y[j] for j in range(r)) for i in range(k)]
    cb = (c + sum(b[k + j] * y[j] for j in range(r))
          + Fr(1, 2) * sum(H[k + i][k + j] * y[i] * y[j] for i in range(r) for j in range(r)))
    return Hb, bb, cb


def DeltaK(H, b, c, lo, up):
    n = len(H)
    coefs = ([H[i][i] / 2 for i in range(n)] + [H[i][j] for i in range(n) for j in range(i + 1, n)]
             + list(b) + [c])
    Lc = 1
    for q in coefs:
        Lc = lcm(Lc, q.denominator)
    Le = 1
    for q in list(lo) + list(up):
        Le = lcm(Le, q.denominator)
    return Lc * Le * Le


def OmegaK(H, k, D):
    R = Fr(D)
    for i in range(k):
        if H[i][i] > 0:
            R *= D * H[i][i]
    assert R.denominator == 1
    return D * R * R


cnt = 0
for trial in range(150):
    k = random.randint(1, 3)
    r = random.randint(1, 3)
    H, b, c, lo, up, o = instance(k, r)
    D = DeltaK(H, b, c, lo, up)
    Om = OmegaK(H, k, D)
    for y in itertools.product(*[(lo[i], up[i]) for i in range(r)]):
        Hb, bb, cb = restrict(H, b, c, k, list(y))
        # Delta_K clears all monomial coefficients of F_y
        for q in [Hb[i][i] / 2 for i in range(k)] + [Hb[i][j] for i in range(k) for j in range(i + 1, k)] + bb + [cb]:
            assert (q * D).denominator == 1
        val, v, J = box_min_faces(Hb, bb, cb, k)
        W = val.denominator
        assert W <= Om, (W, Om)
        # sharper: some minimizer with nonsingular interior block gives W | D*rho^2
        if J:
            hatH = [[D * Hb[i][j] for j in J] for i in J]
            dt = det(hatH)
            assert dt > 0 and dt.denominator == 1
            rho = D * int(dt)
        else:
            rho = D
        assert (Fr(D * rho * rho) * val).denominator == 1, (val, D, rho)
        cnt += 1
print("lem:cr-height: %d endpoint values; W <= Omega_K and W | Delta_K rho^2" % cnt)

# the 1/8 example: H_12 = 1/2 between two residual coordinates at endpoints 1/2
Hx = [[Fr(0), Fr(1, 2)], [Fr(1, 2), Fr(0)]]
assert quad(Hx, [0, 0], 0, [Fr(1, 2), Fr(1, 2)]) == Fr(1, 8)
assert (Fr(1, 8) * 2 * 2).denominator != 1 and (Fr(1, 8) * 2 * 4).denominator == 1
print("lem:cr-height: 1/8 example (Lambda_c Lambda_e = 4 fails, Lambda_c Lambda_e^2 = 8 works)")


# ---------------------------------------------------------------- 3. thm:cr-exact pipeline
def V_and_y(H, b, c, k, lo, up, v):
    r = len(lo)
    best = None
    for y in itertools.product(*[(lo[i], up[i]) for i in range(r)]):
        val = quad(H, b, c, list(v) + list(y))
        if best is None or val < best[0]:
            best = (val, list(y))
    return best


def opt_value(H, b, c, k, lo, up):
    best = None
    for y in itertools.product(*[(lo[i], up[i]) for i in range(len(lo))]):
        Hb, bb, cb = restrict(H, b, c, k, list(y))
        val = box_min_faces(Hb, bb, cb, k)[0]
        best = val if best is None else min(best, val)
    return best


ran = 0
for trial in range(400):
    if ran >= 12:
        break
    k = 1
    r = random.randint(1, 2)
    H, b, c, lo, up, o = instance(k, r, dens=(1,))
    lo = [Fr(random.randint(-2, 0)) for _ in range(r)]
    up = [lo[i] + random.randint(1, 2) for i in range(r)]
    D = DeltaK(H, b, c, lo, up)
    Om = OmegaK(H, k, D)
    if Om > 2 ** 12:
        continue
    L = max(H[0][0], 0)
    eps = Fr(1, 2 * Om * Om)
    Jlim = 0
    while Fr(k) * L / 8 / 4 ** Jlim > eps:
        Jlim += 1
    cells = [Fr(0)]
    U = None
    inc = None
    cache = {}
    stopped = None
    for j in range(Jlim + 1):
        h = Fr(1, 2 ** j)
        e = Fr(k) * L / 8 * h * h
        betas = []
        for a in cells:
            vals = []
            for v in (a, a + h):
                if v not in cache:
                    cache[v] = V_and_y(H, b, c, k, lo, up, [v])
                val, y = cache[v]
                vals.append(val)
                if U is None or val < U:
                    U, inc = val, ([v], y)
            betas.append(min(vals) - e)
        lam = min(betas)
        if U - min(lam, U) <= eps:
            stopped = j
            beta = min(lam, U)
            break
        cells = [a + s * h / 2 for a, bt in zip(cells, betas) if bt <= U for s in (0, 1)]
    assert stopped is not None and stopped <= Jlim
    yU = inc[1]
    Hb, bb, cb = restrict(H, b, c, k, yU)
    val, vhat, _ = box_min_faces(Hb, bb, cb, k)
    W = val.denominator
    assert val - beta < Fr(1, Om * W)  # acceptance test of Prop. accept
    assert val == opt_value(H, b, c, k, lo, up)
    ran += 1
assert ran >= 5
print("thm:cr-exact with eps = Omega_K^-2/2: %d instances stop by level J, pass acceptance, output OPT" % ran)


# ---------------------------------------------------------------- 4. greedy LP
try:
    from scipy.optimize import linprog
    have_scipy = True
except Exception:
    have_scipy = False

if have_scipy:
    checked = 0
    for trial in range(40):
        m = random.randint(1, 4)
        # random submodular set function: cut function plus modular part (exact)
        w = {(i, j): Fr(random.randint(0, 5)) for i in range(m) for j in range(i + 1, m)}
        mod = [Fr(random.randint(-6, 6)) for _ in range(m)]

        def f(S):
            return (sum(mod[i] for i in S)
                    + sum(w[(i, j)] for (i, j) in w if (i in S) != (j in S))
                    + Fr(random.randint(0, 0)))
        sets = [frozenset(s) for t in range(m + 1) for s in itertools.combinations(range(m), t)]
        vals = {S: f(S) for S in sets}
        hat = {S: vals[S] - vals[frozenset()] for S in sets}
        mn = min(hat.values())
        perms = list(itertools.permutations(range(m)))
        G = []
        for p in perms:
            a = [Fr(0)] * m
            pre = frozenset()
            for i in p:
                a[i] = hat[pre | {i}] - hat[pre]
                pre = pre | {i}
            G.append(a)
        # dual: min sum r  s.t.  sum_p lam_p a^p + r >= 0, sum lam = 1, lam, r >= 0
        P = len(G)
        cobj = [0.0] * P + [1.0] * m
        A_ub = []
        b_ub = []
        for i in range(m):
            row = [-float(G[p][i]) for p in range(P)] + [-1.0 if t == i else 0.0 for t in range(m)]
            A_ub.append(row)
            b_ub.append(0.0)
        A_eq = [[1.0] * P + [0.0] * m]
        res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * (P + m),
                      method="highs")
        assert res.status == 0
        assert abs(-res.fun - float(mn)) < 1e-7, (res.fun, mn)
        # primal: max t s.t. t + a^p.xi <= 0, 0 <= xi <= 1
        c2 = [-1.0] + [0.0] * m
        A2 = [[1.0] + [float(x) for x in G[p]] for p in range(P)]
        res2 = linprog(c2, A_ub=A2, b_ub=[0.0] * P, bounds=[(None, None)] + [(0, 1)] * m, method="highs")
        assert res2.status == 0 and abs(-res2.fun - (-float(mn))) < 1e-7
        checked += 1
    print("prop:cr-greedy(c): LP values equal -min hat Phi and max sum min(0,abar) = min hat Phi on %d set functions" % checked)
else:
    print("prop:cr-greedy(c): scipy not available, LP check skipped")
print("ALL OK")
