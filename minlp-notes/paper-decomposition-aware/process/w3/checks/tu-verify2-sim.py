"""Second verification pass for Section 8 / Appendix (group tu): exact end-to-end runs.

Run: python3 -B tu-verify2-sim.py

Simulates TU-GRID (union and hull variants) and TU-EXACT exactly (Fractions)
on small continuous instances (n_d = 0), brute-forcing the grid, and checks:
  * Prop. prop:tu-sound (b),(d),(e): beta_j <= OPT <= U_j <= OPT + E_j, S in D^(j+1);
  * Thm. thm:tu-states (a),(b),(c): localization radius a_j + h_j and node bounds;
  * Lemma lem:tu-snap: whenever dist(y^(j), S) <= tau/(2 sqrt(n_c)), step (ii)
    finds a point and every vertex of P_z(J) is optimal;
  * Thm. thm:tu-exact (a),(c): TU-EXACT returns an exact minimizer, no later than
    the first level with E_j <= min{g_S tau^2/(4 n_c), 1/(2 Omega^2)}.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import math

ok = True


def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and bool(cond)


INF = None


def lt(a, b):  # a <= b with a possibly +inf (None)
    return a is not None and a <= b


class Instance:
    def __init__(self, name, lo, hi, A, b, F, Lbar, eta=Fr(1)):
        self.name, self.lo, self.hi, self.A, self.b = name, lo, hi, A, b
        self.F, self.Lbar, self.eta, self.nc = F, Lbar, eta, len(lo)

    def feasible(self, x):
        return all(sum(a * xi for a, xi in zip(row, x)) <= bi
                   for row, bi in zip(self.A, self.b))


def nodes_of(D, h):
    out = set()
    for a, b in D:
        k0, k1 = a / h, b / h
        assert k0.denominator == 1 and k1.denominator == 1
        for k in range(int(k0), int(k1) + 1):
            out.add(k * h)
    return sorted(out)


def merge(cells):
    cells = sorted(cells)
    out = []
    for a, b in cells:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def tugrid_levels(P, levels, hull):
    """Yield per level: j, h, E, domains D, nodes, mu, y, beta, U, m (dict per coord)."""
    D = [[(P.lo[i], P.hi[i])] for i in range(P.nc)]
    for j in range(levels + 1):
        h = P.eta / 2 ** j
        E = P.nc * P.Lbar * h * h / 8
        nodes = [nodes_of(D[i], h) for i in range(P.nc)]
        feas = [x for x in product(*nodes) if P.feasible(x)]
        assert feas, "X empty"
        vals = {x: P.F(x) for x in feas}
        mu = min(vals.values())
        y = min(x for x in feas if vals[x] == mu)
        m = []
        for i in range(P.nc):
            mi = {}
            for x, v in vals.items():
                t = x[i]
                if t not in mi or v < mi[t]:
                    mi[t] = v
            m.append({t: (mi[t] - E if t in mi else None) for t in nodes[i]})
        U, beta = mu, mu - E
        yield dict(j=j, h=h, E=E, D=D, nodes=nodes, mu=mu, y=y, beta=beta, U=U, m=m)
        newD = []
        for i in range(P.nc):
            cells = []
            for a, b in D[i]:
                if a == b:
                    if lt(m[i][a], U):
                        cells.append((a, a))
                    continue
                t = a
                while t < b:
                    if lt(m[i][t], U) or lt(m[i][t + h], U):
                        cells.append((t, t + h))
                    t += h
            cells = merge(cells)
            if hull:
                cells = [(cells[0][0], cells[-1][1])]
            newD.append(cells)
        D = newD


def dist2(x, S):
    return min(sum((a - b) ** 2 for a, b in zip(x, s)) for s in S)


def in_domain(D, x):
    return all(any(a <= xi <= b for a, b in D[i]) for i, xi in enumerate(x))


def run_grid_checks(P, S, OPT, gS, levels, hull, r):
    good_sound = good_loc = good_cnt = good_S = True
    worst = 0
    prev = None
    for L in tugrid_levels(P, levels, hull):
        j, h, E = L["j"], L["h"], L["E"]
        good_sound &= L["beta"] <= OPT <= L["U"] <= OPT + E and L["U"] - L["beta"] == E
        if prev is not None:
            # D^(j) is the domain produced at level j-1: check S inside, localization, counts
            hp = prev["h"]
            a2 = P.nc * P.Lbar * hp * hp / (4 * gS)  # a_{j-1}^2
            good_S &= all(in_domain(L["D"], s) for s in S)
            for i in range(P.nc):
                Si = sorted({s[i] for s in S})
                for (a, b) in L["D"][i]:
                    for t in (a, b):
                        # |t - nu| <= a_{j-1} + h_{j-1} for some nu in S_i
                        dmin = min(abs(t - nu) for nu in Si)
                        good_loc &= (dmin - hp) <= 0 or (dmin - hp) ** 2 <= a2
                cnt = len(L["nodes"][i])
                worst = max(worst, cnt)
                bound = r * (5 + math.isqrt(int(math.floor(4 * P.nc * P.Lbar / gS))))
                # floor(2 sqrt(nc Lbar/gS)) = isqrt(floor(4 nc Lbar/gS))
                good_cnt &= cnt <= bound
        prev = L
    tag = f"{P.name} ({'hull' if hull else 'union'})"
    check(good_sound, f"{tag}: beta_j <= OPT <= U_j <= OPT+E_j and U_j-beta_j=E_j at levels 0..{levels}")
    check(good_S, f"{tag}: S contained in every D^(j)")
    check(good_loc, f"{tag}: every retained point within a_j+h_j of S_i (Thm tu-states(a)/(c))")
    check(good_cnt, f"{tag}: node counts <= r(5+floor(2 sqrt(nc Lbar/gS))) (max seen {worst})")


# ------------------------------------------------------------- instance A
# ex:tu-union, one block: x1+x2=x3 on [0,1]^3, F=(2x1-x3)^2 + x3(1-x3)/4
def FA(x):
    return (2 * x[0] - x[2]) ** 2 + Fr(1, 4) * x[2] * (1 - x[2])


PA = Instance("ex:tu-union block", [Fr(0)] * 3, [Fr(1)] * 3,
              [[1, 1, -1], [-1, -1, 1]], [0, 0], FA, Fr(12))
SA = [(Fr(0),) * 3, (Fr(1, 2), Fr(1, 2), Fr(1))]
run_grid_checks(PA, SA, Fr(0), Fr(1, 6), 7, hull=False, r=2)

# ------------------------------------------------------------- instance B
# prop:tu-misaligned objective with m=1/3, lambda=1/5, L=1 on x1<=x2: unique
# minimizer (1/3,1/3), growth g=L/2 (stated in the proposition).
mB, lamB = Fr(1, 3), Fr(1, 5)


def FB(x):
    return Fr(1, 2) * ((x[0] - mB) ** 2 + (x[1] - mB) ** 2) + lamB * (x[1] - x[0])


PB = Instance("order row, unique minimizer", [Fr(0)] * 2, [Fr(1)] * 2, [[1, -1]], [0], FB, Fr(1))
SB = [(mB, mB)]
for hull in (False, True):
    run_grid_checks(PB, SB, Fr(0), Fr(1, 2), 10, hull=hull, r=1)


# ------------------------------------------------------------- TU-EXACT
def nullspace(rows, n):
    """Basis (list of vectors) of {w: row.w = 0 for all rows}, exact."""
    M = [list(map(Fr, r)) for r in rows]
    piv = []
    rk = 0
    for c in range(n):
        p = next((k for k in range(rk, len(M)) if M[k][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        M[rk] = [v / M[rk][c] for v in M[rk]]
        for k in range(len(M)):
            if k != rk and M[k][c] != 0:
                f = M[k][c]
                M[k] = [a - f * b for a, b in zip(M[k], M[rk])]
        piv.append(c)
        rk += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        w = [Fr(0)] * n
        w[fc] = Fr(1)
        for k, pc in enumerate(piv):
            w[pc] = -M[k][fc]
        basis.append(w)
    return basis


def solve(rows, rhs):
    n = len(rows)
    M = [list(map(Fr, r)) + [Fr(v)] for r, v in zip(rows, rhs)]
    for c in range(n):
        p = next((k for k in range(c, n) if M[k][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for k in range(n):
            if k != c and M[k][c] != 0:
                f = M[k][c] / M[c][c]
                M[k] = [a - f * b for a, b in zip(M[k], M[c])]
    return tuple(M[k][n] / M[k][k] for k in range(n))


def polytope_vertices(eqs, ineqs, n):
    """All vertices of {x: e.x = f (eqs), a.x <= b (ineqs)} (bounded), by enumeration."""
    cands = [(r, v) for r, v in eqs] + [(r, v) for r, v in ineqs]
    verts = set()
    for sub in combinations(range(len(cands)), n):
        x = solve([cands[k][0] for k in sub], [cands[k][1] for k in sub])
        if x is None:
            continue
        if all(sum(a * b for a, b in zip(r, x)) == v for r, v in eqs) and \
           all(sum(a * b for a, b in zip(r, x)) <= v for r, v in ineqs):
            verts.add(x)
    return sorted(verts)


def tuexact(P, H, g, c0, S, OPT, gS, maxlev, Delta):
    """H: Hessian (rational), g: grad F(0); continuous only; eta=1 so Delta_eta=1."""
    nc = P.nc
    Hh = [[Delta * v for v in row] for row in H]
    assert all(v.denominator == 1 for row in Hh for v in row)
    C = max(1, max(abs(v) for row in Hh for v in row))
    R = (2 * nc * C) ** nc
    Om = Delta * R ** 2
    mp = len(P.A) + 2 * nc
    tau = Fr(1, 4 * mp * R)
    cz = [Delta * v for v in g]
    assert all(v.denominator == 1 for v in cz)
    Ahat = [list(map(Fr, r)) for r in P.A]
    bhat = [Fr(v) for v in P.b]
    for i in range(nc):
        e = [Fr(0)] * nc
        e[i] = Fr(1)
        Ahat.append(e)
        bhat.append(P.hi[i])
    for i in range(nc):
        e = [Fr(0)] * nc
        e[i] = Fr(-1)
        Ahat.append(e)
        bhat.append(-P.lo[i])
    thr = min(gS * tau ** 2 / (4 * nc), 1 / (2 * Om ** 2))
    snap_ok = True
    nnear = 0
    returned = None
    for L in tugrid_levels(P, maxlev, hull=False):
        y, beta, E, j = L["y"], L["beta"], L["E"], L["j"]
        J = [k for k in range(len(Ahat))
             if bhat[k] - sum(a * b for a, b in zip(Ahat[k], y)) <= tau]
        Xi = nullspace([Ahat[k] for k in J], nc)
        eqs = [(Ahat[k], bhat[k]) for k in J]
        for w in Xi:  # w^T (Hh x + cz) = 0
            row = [sum(w[a] * Hh[a][b] for a in range(nc)) for b in range(nc)]
            eqs.append((row, -sum(w[a] * cz[a] for a in range(nc))))
        V = polytope_vertices(eqs, list(zip(Ahat, bhat)), nc)
        near = dist2(y, S) <= tau ** 2 / (4 * nc)
        if near:
            # Lemma tu-snap: nonempty and contained in S (vertices suffice: F is
            # constant on P_z(J) by the proof; check all vertices are optimal)
            nnear += 1
            snap_ok &= bool(V) and all(P.F(v) == OPT for v in V)
        if V and returned is None:
            xh = V[0]
            val = P.F(xh)
            W = val.denominator
            if val - beta < Fr(1, Om * W):
                returned = (j, xh, val, E)
        # keep running past acceptance to exercise Lemma tu-snap
    check(snap_ok and nnear > 0, f"{P.name}: Lemma tu-snap holds at all {nnear} levels with dist(y,S) <= tau/(2 sqrt nc)")
    check(returned is not None and returned[2] == OPT and P.feasible(returned[1])
          and dist2(returned[1], S) == 0,
          f"{P.name}: TU-EXACT returns an exact minimizer {returned[1] if returned else None}, "
          f"value {returned[2] if returned else None} (OPT {OPT}) at level {returned[0] if returned else None}")
    # Thm tu-exact(c): termination no later than first level with E_j <= thr
    jthr = 0
    while P.nc * P.Lbar * (P.eta / 2 ** jthr) ** 2 / 8 > thr:
        jthr += 1
    check(returned is not None and returned[0] <= jthr,
          f"{P.name}: terminated at level {returned[0] if returned else None} <= first level {jthr} with E_j <= min{{g tau^2/(4nc), 1/(2 Omega^2)}}")
    return returned


# Instance C: nonconvex. F = (x1+x2-2/3)^2 - (x2-x1)^2/2 + 2(x2-x1) + c on x1<=x2, [0,1]^2.
# Hessian [[1,3],[3,1]] (eigenvalues 4,-2), Lbar = 4 (row sums), minimizer (1/3,1/3).
# On X: F - OPT = (s-2/3)^2 + 2d - d^2/2 >= (s-2/3)^2 + d^2 = 2 dist^2, d = x2-x1 in [0,1].
for cst, Delta in ((Fr(0), 18), (Fr(1, 7), 126)):
    def FC(x, cst=cst):
        s, d = x[0] + x[1], x[1] - x[0]
        return (s - Fr(2, 3)) ** 2 - d * d / 2 + 2 * d + cst
    PC = Instance(f"nonconvex order-row QP (+{cst})", [Fr(0)] * 2, [Fr(1)] * 2,
                  [[1, -1]], [0], FC, Fr(4))
    H = [[Fr(1), Fr(3)], [Fr(3), Fr(1)]]
    g = [Fr(-10, 3), Fr(2, 3)]
    # sanity: quadratic representation matches FC
    for x in [(Fr(1, 5), Fr(3, 4)), (Fr(0), Fr(1)), (Fr(2, 3), Fr(5, 6))]:
        q = Fr(1, 2) * sum(x[a] * H[a][b] * x[b] for a in range(2) for b in range(2)) \
            + sum(g[a] * x[a] for a in range(2)) + Fr(4, 9) + cst
        assert q == FC(x)
    # growth sanity on a rational sample
    S = [(Fr(1, 3), Fr(1, 3))]
    OPT = cst
    gmin = min((FC((Fr(a, 40), Fr(b, 40))) - OPT) / dist2((Fr(a, 40), Fr(b, 40)), S)
               for a in range(41) for b in range(41)
               if a <= b and (Fr(a, 40), Fr(b, 40)) != S[0])
    check(gmin >= 2, f"instance C: growth ratio >= 2 on sample (min {gmin})")
    tuexact(PC, H, g, Fr(4, 9) + cst, S, OPT, Fr(2), 45, Delta)

# Instance D: concave objective whose unique minimizer (1/2,1) has the TU row x1+x2<=3/2 and
# the bound x2<=1 active; eta = 1/2 for alignment. Minimizers of a concave function are
# vertices; enumerate them.
eta = Fr(1, 2)


def FD(x):
    return -(x[0] - Fr(1, 2)) ** 2 - (x[1] - Fr(1, 2)) ** 2 - 3 * x[0] / 4 - x[1]


PD = Instance("concave, sum row, eta=1/2", [Fr(0)] * 2, [Fr(1)] * 2, [[1, 1]], [Fr(3, 2)], FD,
              Fr(1), eta)
verts = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(1), Fr(1, 2)), (Fr(1, 2), Fr(1))]
OPTD = min(FD(v) for v in verts)
SD = [v for v in verts if FD(v) == OPTD]
# Lbar: Hessian -2I, so any positive rational is valid; use 1.
# growth: concave on a polytope with isolated vertex minimizers has linear growth; a valid
# g_S is not needed for (a),(b) of Thm tu-exact; use the termination check only loosely.
H = [[Fr(-2), Fr(0)], [Fr(0), Fr(-2)]]
g = [Fr(1, 4), Fr(0)]
for x in [(Fr(1, 5), Fr(3, 4)), (Fr(0), Fr(1))]:
    q = Fr(1, 2) * sum(x[a] * H[a][b] * x[b] for a in range(2) for b in range(2)) \
        + sum(g[a] * x[a] for a in range(2)) - Fr(1, 2)
    assert q == FD(x)
# alignment: l/eta, u/eta, b/eta integral
assert all((v / eta).denominator == 1 for v in PD.lo + PD.hi + PD.b)
# Delta: coefficients -1, -1, 1/4, -1/2 -> 4
# g_S lower bound: F - OPT >= c * dist over X with c from the edge slopes; on [0,1]^2 dist <= sqrt2,
# so g_S = (min over X\S-sample of (F-OPT)/dist^2) is estimated, and we use a safe lower bound.
samp = [(Fr(a, 32), Fr(b, 32)) for a in range(33) for b in range(33) if a + b <= 48]
gD = min((FD(x) - OPTD) / dist2(x, SD) for x in samp if dist2(x, SD) > 0)
print(f"instance D: OPT={OPTD}, S={SD}, sampled growth ratio {gD}")
# Delta_eta = 2 here; the simulator above assumes Delta_eta = 1, so only (a),(b) are run here
# by a direct loop with Delta_eta folded into R.
Delta = 4
Hh = [[Delta * v for v in row] for row in H]
C = max(1, max(abs(v) for row in Hh for v in row))
R = (2 * 2 * C) ** 2
Deta = 2
Om = Delta * (Deta * R) ** 2
tau = Fr(1, 4 * (1 + 4) * Deta * R)
Ahat = [[Fr(1), Fr(1)], [Fr(1), Fr(0)], [Fr(0), Fr(1)], [Fr(-1), Fr(0)], [Fr(0), Fr(-1)]]
bhat = [Fr(3, 2), Fr(1), Fr(1), Fr(0), Fr(0)]
cz = [Delta * v for v in g]
ret = None
snapD = True
nD = 0
for L in tugrid_levels(PD, 40, hull=False):
    y, beta = L["y"], L["beta"]
    J = [k for k in range(5) if bhat[k] - sum(a * b for a, b in zip(Ahat[k], y)) <= tau]
    Xi = nullspace([Ahat[k] for k in J], 2)
    eqs = [(Ahat[k], bhat[k]) for k in J]
    for w in Xi:
        row = [sum(w[a] * Hh[a][b] for a in range(2)) for b in range(2)]
        eqs.append((row, -sum(w[a] * cz[a] for a in range(2))))
    V = polytope_vertices(eqs, list(zip(Ahat, bhat)), 2)
    if dist2(y, SD) <= tau ** 2 / 8:
        nD += 1
        snapD &= bool(V) and all(FD(v) == OPTD for v in V)
    if ret is None and V and FD(V[0]) - beta < Fr(1, Om * FD(V[0]).denominator):
        ret = (L["j"], V[0])
check(snapD and nD > 0, f"instance D (concave, eta=1/2): Lemma tu-snap at all {nD} near levels")
check(ret is not None and FD(ret[1]) == OPTD and PD.feasible(ret[1]),
      f"instance D: TU-EXACT returns exact minimizer {ret[1] if ret else None} at level {ret[0] if ret else None}")

print("ALL PASS" if ok else "SOME CHECKS FAILED")
