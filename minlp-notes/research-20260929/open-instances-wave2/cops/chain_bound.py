"""Rigorous dual bound and primal check for chain50/100/200/400.

Notation (see chain_model.py): eta = h/2 = 1/(2N) (decimal from the file),
pieces of the polyline A=(0,1) -> Q_1 -> ... -> Q_N -> B=(1,3), Q_k = ((k-1/2)h, z_k).
Piece 0 (A->Q_1, horizontal eta) carries weight lam_0 at height 1, piece N
(Q_N->B, horizontal eta) carries weight lam_N at height 3, interior pieces
k = 1..N-1 (horizontal h) carry weight lam_k at their midpoint.
objective = lam_0 + 3 lam_N + sum_k lam_k (z_k+z_{k+1})/2,  sum_k lam_k = 4.

Certificate (proved in report.md): for every feasible point, every V and Hp > 0,
  f >= Bnd(z_1, z_N; V, Hp) := lam_0 + 3 lam_N + (V+L) z_N - V z_1
                                - G(V+L) + G(V) + (N-1) c,
  lam_0 = sqrt(eta^2 + (z_1-1)^2), lam_N = sqrt(eta^2 + (3-z_N)^2),
  L = 4 - lam_0 - lam_N,  G(v) = (v sqrt(Hp^2+v^2) + Hp^2 asinh(v/Hp))/2,
  c = 2 G(eta).
A 2-D interval branch and bound over (z_1, z_N) proves Bnd >= target.
"""
import heapq
import json
import sys
import time
from fractions import Fraction

import mpmath as mp
from mpmath import iv

import chain_model as cm
import osilx

iv.dps = 40


# ---------------- interval helpers (mpmath iv, outward rounded) ----------------
def I(x):
    return iv.mpf(x)


def iasinh_pos(x):
    """asinh on an interval with x > 0 (asserted): log(x + sqrt(x^2+1)), monotone."""
    assert x.a > 0
    return iv.log(x + iv.sqrt(x ** 2 + 1))


def _asinh_pt(t):
    """enclosure of asinh at the point t (t exact mpf)"""
    if t > 0:
        return iasinh_pos(iv.mpf(t))
    if t < 0:
        return -iasinh_pos(iv.mpf(-t))
    return iv.mpf(0)


def iasinh(x):
    """asinh is increasing: enclose via the endpoints."""
    if x.a > 0:
        return iasinh_pos(x)
    if x.b < 0:
        return -iasinh_pos(-x)
    return iv.mpf([_asinh_pt(x.a).a, _asinh_pt(x.b).b])


def iG(v, Hp):
    return (v * iv.sqrt(Hp ** 2 + v ** 2) + Hp ** 2 * iasinh(v / Hp)) / 2


def ig(v, Hp):
    return iv.sqrt(Hp ** 2 + v ** 2)


class Chain:
    def __init__(self, N):
        self.N = N
        self.m, eta_s = cm.extract(N)
        self.eta_s = eta_s
        self.eta = I(eta_s)
        self.etaF = Fraction(eta_s)
        self.h = float(2 * self.etaF)

    # ---------- float optimizer of (V, Hp) for given (z1, zN) ----------
    def best_mult(self, z1, zN):
        import math
        N, eta = self.N, float(self.etaF)
        l0 = math.hypot(eta, z1 - 1)
        lN = math.hypot(eta, 3 - zN)
        L = 4 - l0 - lN
        if L <= 0 or L * L - (zN - z1) ** 2 <= (1 - 2 * eta) ** 2 * (1 + 1e-12):
            return None
        phm = math.atanh((zN - z1) / L)
        target = L / (2 * math.cosh(phm))
        def f(Hp):  # decreasing in Hp
            arg = (N - 1) * math.asinh(eta / Hp)
            return math.inf if arg > 700 else Hp * math.sinh(arg) - target
        lo, hi = 1e-3, 1.0
        while f(hi) > 0:
            hi *= 2
        while f(lo) < 0:
            lo /= 2
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        Hp = math.sqrt(lo * hi)
        tau = math.asinh(eta / Hp)
        V = Hp * math.sinh(phm - (N - 1) * tau)
        return V, Hp

    # ---------- interval evaluation of the bound and its gradient ----------
    def bound_iv(self, Z1, ZN, V, Hp):
        N, eta = self.N, self.eta
        V, Hp = I(V), I(Hp)
        l0 = iv.sqrt(eta * eta + (Z1 - 1) ** 2)
        lN = iv.sqrt(eta * eta + (3 - ZN) ** 2)
        L = 4 - l0 - lN
        c = 2 * iG(eta, Hp)
        B = l0 + 3 * lN + (V + L) * ZN - V * Z1 - iG(V + L, Hp) + iG(V, Hp) + (N - 1) * c
        return B, l0, lN, L

    def grad_iv(self, Z1, ZN, V, Hp):
        eta = self.eta
        V, Hp = I(V), I(Hp)
        l0 = iv.sqrt(eta * eta + (Z1 - 1) ** 2)
        lN = iv.sqrt(eta * eta + (3 - ZN) ** 2)
        L = 4 - l0 - lN
        gg = ig(V + L, Hp)
        d0 = (Z1 - 1) / l0
        dN = (ZN - 3) / lN
        g1 = d0 * (1 - ZN + gg) - V
        gN = dN * (3 - ZN + gg) + V + L
        return g1, gN

    def box_lb(self, z1a, z1b, zNa, zNb, mult):
        """rigorous lower bound of Bnd over the box (fixed multipliers), or +inf if the
        box contains no point satisfying the necessary feasibility condition
        L >= sqrt((1-h)^2 + (zN-z1)^2)."""
        Z1 = iv.mpf([z1a, z1b])
        ZN = iv.mpf([zNa, zNb])
        eta = self.eta
        l0 = iv.sqrt(eta * eta + (Z1 - 1) ** 2)
        lN = iv.sqrt(eta * eta + (3 - ZN) ** 2)
        L = 4 - l0 - lN
        chord2 = (1 - 2 * eta) ** 2 + (ZN - Z1) ** 2
        if L.b < 0 or (L.b) ** 2 < chord2.a:
            return mp.inf, "infeasible"
        if mult is None:
            return -mp.inf, "nomult"
        V, Hp = mult
        # natural extension
        B, *_ = self.bound_iv(Z1, ZN, V, Hp)
        lb = B.a
        # mean-value form around the center
        c1, cN = (z1a + z1b) / 2, (zNa + zNb) / 2
        Bc, *_ = self.bound_iv(I(c1), I(cN), V, Hp)
        g1, gN = self.grad_iv(Z1, ZN, V, Hp)
        mv = Bc + g1 * (Z1 - c1) + gN * (ZN - cN)
        lb = max(lb, mv.a)
        return lb, "ok"

    def branch_and_bound(self, target, box, max_boxes=2_000_000, min_width=1e-13, log=None):
        """prove Bnd >= target on all of box (up to leaves reported)."""
        t0 = time.time()
        stack = [box]
        nboxes = 0
        worst = mp.inf
        unresolved = []
        n_inf = 0
        while stack:
            z1a, z1b, zNa, zNb = stack.pop()
            nboxes += 1
            if nboxes > max_boxes:
                raise RuntimeError("box limit")
            mult = self.best_mult((z1a + z1b) / 2, (zNa + zNb) / 2)
            if mult is None:  # center violates the chord condition: try other points of the box
                for t1, tN in ((0, 0), (0, 1), (1, 0), (1, 1), (.5, 0), (.5, 1), (0, .5), (1, .5),
                               (.25, .25), (.25, .75), (.75, .25), (.75, .75)):
                    mult = self.best_mult(z1a + t1 * (z1b - z1a), zNa + tN * (zNb - zNa))
                    if mult is not None:
                        break
            lb, st = self.box_lb(z1a, z1b, zNa, zNb, mult)
            if st == "infeasible":
                n_inf += 1
                continue
            if lb >= target:
                worst = min(worst, lb)
                continue
            if max(z1b - z1a, zNb - zNa) < min_width:
                unresolved.append((z1a, z1b, zNa, zNb, lb))
                worst = min(worst, lb)
                continue
            if z1b - z1a >= zNb - zNa:
                m = (z1a + z1b) / 2
                stack += [(z1a, m, zNa, zNb), (m, z1b, zNa, zNb)]
            else:
                m = (zNa + zNb) / 2
                stack += [(z1a, z1b, zNa, m), (z1a, z1b, m, zNb)]
        return dict(boxes=nboxes, infeasible_boxes=n_inf, min_leaf_lb=float(worst) if worst != mp.inf else None,
                    unresolved=len(unresolved), seconds=time.time() - t0,
                    bound=float(min(worst, target)) if not unresolved else float(min(u[4] for u in unresolved)))


# ---------------- exact checks of the algebra ----------------
def check_identity(N, trials=3):
    """sum_k lam_k (z_k+z_{k+1})/2 == (V+L) z_N - V z_1 - sum_k V_k dy_k  (rational arithmetic,
    lam_k arbitrary positive rationals in place of the square roots: the identity is linear)."""
    import random
    rnd = random.Random(7)
    for _ in range(trials):
        z = [Fraction(rnd.randint(-10 ** 6, 10 ** 6), 10 ** 5) for _ in range(N + 1)]  # z_1..z_N at z[1..N]
        lam = [None] + [Fraction(rnd.randint(1, 10 ** 6), 10 ** 6) for _ in range(N - 1)]
        V = Fraction(rnd.randint(-10 ** 6, 10 ** 6), 10 ** 6)
        L = sum(lam[1:])
        lhs = sum(lam[k] * (z[k] + z[k + 1]) / 2 for k in range(1, N))
        sig = Fraction(0)
        s = Fraction(0)
        for k in range(1, N):
            Vk = V + sig + lam[k] / 2
            s += Vk * (z[k + 1] - z[k])
            sig += lam[k]
        rhs = (V + L) * z[N] - V * z[1] - s
        assert lhs == rhs
    return True


def check_objective_decomposition(N, chain, trials=2):
    """OSIL objective and length row == piece form, on random z (60-digit arithmetic)."""
    import random
    rnd = random.Random(11)
    mp.mp.dps = 60
    eta = mp.mpf(chain.eta_s)
    for _ in range(trials):
        zin = [mp.mpf(rnd.uniform(0.2, 3.0)) for _ in range(N)]
        z = cm.full_z(zin, N)
        x = [(z[i] + z[i + 1]) / 2 for i in range(N + 1)]
        u = [(z[i + 1] - z[i]) / (2 * eta) for i in range(N + 1)]
        X = x + u
        fns = {"sqrt": mp.sqrt}
        obj = osilx.ev_row(dict(constant="0", lin={}, quad=[], nl=chain.m["obj"]["nl"]), X, mp.mpf, fns)
        lenrow = osilx.ev_row(chain.m["cons"][N], X, mp.mpf, fns)
        dyn = max(abs(osilx.ev_row(chain.m["cons"][i], X, mp.mpf, fns)) for i in range(N))
        lam0 = mp.sqrt(eta ** 2 + (z[1] - 1) ** 2)
        lamN = mp.sqrt(eta ** 2 + (3 - z[N]) ** 2)
        lam = [mp.sqrt(4 * eta ** 2 + (z[k + 1] - z[k]) ** 2) for k in range(1, N)]
        piece_obj = lam0 + 3 * lamN + sum(lam[k - 1] * (z[k] + z[k + 1]) / 2 for k in range(1, N))
        piece_len = lam0 + lamN + sum(lam)
        assert abs(obj - piece_obj) < mp.mpf(10) ** -50 and abs(lenrow - piece_len) < mp.mpf(10) ** -50
        assert dyn < mp.mpf(10) ** -50
    return True


def check_gradient(chain, trials=30):
    """finite differences (60 digits) against the analytic gradient used in the mean-value form."""
    import random
    rnd = random.Random(3)
    mp.mp.dps = 60
    worst = mp.mpf(0)
    for _ in range(trials):
        z1, zN = rnd.uniform(0.3, 1.5), rnd.uniform(2.0, 3.5)
        V, Hp = rnd.uniform(-1.2, 0.5), rnd.uniform(0.05, 1.0)
        e = mp.mpf("1e-20")
        B = lambda a, b: chain.bound_iv(iv.mpf(a), iv.mpf(b), V, Hp)[0].mid
        g1, gN = chain.grad_iv(iv.mpf(z1), iv.mpf(zN), V, Hp)
        fd1 = (B(mp.mpf(z1) + e, zN) - B(mp.mpf(z1) - e, zN)) / (2 * e)
        fdN = (B(z1, mp.mpf(zN) + e) - B(z1, mp.mpf(zN) - e)) / (2 * e)
        d1, dN = abs(fd1 - g1.mid), abs(fdN - gN.mid)   # interval-valued
        worst = max(worst, mp.mpf(d1.b), mp.mpf(dN.b))
    assert worst < mp.mpf("1e-15"), worst
    return float(worst)


def primal_check(N, chain):
    """KKT point -> double-rounded OSIL vector -> 50-digit evaluation."""
    z, mu, _ = cm.solve(N, dps=60)
    x, u = cm.to_xu(z, N, mp.mpf(chain.eta_s))
    X = [float(v) for v in x + u]
    X[0], X[N] = 1.0, 3.0
    mp.mp.dps = 50
    Xm = [mp.mpf(v) for v in X]
    fns = {"sqrt": mp.sqrt}
    obj = osilx.ev_row(dict(constant="0", lin={}, quad=[], nl=chain.m["obj"]["nl"]), Xm, mp.mpf, fns)
    viol = 0
    for i, r in enumerate(chain.m["cons"]):
        val = osilx.ev_row(r, Xm, mp.mpf, fns)
        viol = max(viol, abs(val - mp.mpf(r["lb"])))
    L, G, *_ = cm.lag_grad_hess(z, mu, N, mp.mpf(1) / N, mp.mpf, mp.sqrt)
    fstar = L - mu * G
    return dict(obj_double_point=mp.nstr(obj, 20), max_row_violation=mp.nstr(viol, 3),
                kkt_value=mp.nstr(fstar, 25), mu=mp.nstr(mu, 20), z1=float(z[0]), zN=float(z[-1]),
                X=X)


def main(N, target_gap):
    out = {"N": N}
    ch = Chain(N)
    check_identity(N)
    check_objective_decomposition(N, ch)
    out["gradient_fd_check_max_diff"] = check_gradient(ch)
    out["algebra_checks"] = "passed"
    pc = primal_check(N, ch)
    X = pc.pop("X")
    out["primal"] = pc
    fstar = mp.mpf(pc["kkt_value"])
    z1, zN = pc["z1"], pc["zN"]
    mult = ch.best_mult(z1, zN)
    Bopt, *_ = ch.bound_iv(I(z1), I(zN), *mult)
    out["bound_at_kkt_ends"] = [mp.nstr(Bopt.a, 20), mp.nstr(Bopt.b, 20)]
    out["mult_at_kkt_ends"] = {"V": mult[0], "Hp": mult[1]}
    target = float(fstar) - target_gap
    h = 2 * float(ch.etaF)
    box = (-2 - h, 4 + h, -h, 6 + h)
    res = ch.branch_and_bound(target, box)
    out["target"] = target
    out["bnb"] = res
    out["domain_box"] = box
    return out, X


if __name__ == "__main__":
    gap = float(sys.argv[1])
    for N in [int(v) for v in sys.argv[2:]]:
        out, X = main(N, gap)
        print(json.dumps(out, indent=1), flush=True)
        with open("logs/chain%d_bound.json" % N, "w") as f:
            json.dump(out, f, indent=1)
        with open("logs/chain%d_primal.txt" % N, "w") as f:
            f.write("\n".join(repr(v) for v in X) + "\n")
