"""lukvle10: rigorous partial-Lagrangian bound.

Model (asserted in pattern_check): min sum_{i=0}^{499} f(x_{2i}, x_{2i+1}),
  f(a, b) = (a^2)^(b^2+1) + (b^2)^(a^2+1),
  c_j(x) = -x_j + 3 x_{j+1} - 2 x_{j+2} - 2 x_{j+1}^2 + 1 = 0,  j = 0..997,  x free.
Constraints j < m are dualized with multipliers lam_j (KKT multipliers of the best known
point); constraints j >= m are kept (the last K pairs, m = 1000 - 2K). The Lagrangian
splits into
  head pairs i < m/2:  l_i(a, b) = f(a, b) + beta_{2i} a + q_{2i} a^2 + beta_{2i+1} b + q_{2i+1} b^2,
  tail block:          tau(a, b) = sum_{k<K} f(P^k(a, b)) + beta_m a + q_m a^2 + beta_{m+1} b + q_{m+1} b^2,
where (a, b) = (x_m, x_{m+1}) and P is the two-step map of the kept recurrence
x_{j+2} = (1 + 3 x_{j+1} - 2 x_{j+1}^2 - x_j)/2. Weak duality:
  optimum >= sum_i min l_i + min tau + sum_{j<m} lam_j.
Each 2-D minimum is bounded by an interval branch-and-bound in mpmath interval
arithmetic (natural and mean-value enclosures) on a box outside of which the
separable bound l >= psi_a(a) + psi_b(b) (psi(t) = phi(t) + q t^2 + beta t,
phi(t) = t^2 if |t| >= 1 else 0, valid because f(a,b) >= phi(a) + phi(b)) exceeds a
rigorous upper bound of the minimum.
"""
import heapq
import json
import sys
import time
from fractions import Fraction

import mpmath as mp
import numpy as np

from lukvle10_lagr import kkt_multipliers, load_sol, objective
from osil_eval import check, load

iv = mp.iv
iv.dps = 30
n = 1000


def pattern_check(I):
    assert len(I["vt"]) == n and I["ncons"] == n - 2
    assert all(np.isinf(I["lb"][j]) and np.isinf(I["ub"][j]) for j in range(n))
    for j in range(n - 2):
        r = I["rows"][j]
        assert r["lin"] == {j: -1.0, j + 1: 3.0, j + 2: -2.0} and r["quad"] == [(j + 1, j + 1, -2.0)]
        assert r["lb"] == r["ub"] == -1.0 and r["nl"] is None
    obj = I["rows"][-1]
    assert obj["lin"] == {} and obj["quad"] == []
    t = obj["nl"]
    assert t[0] == "sum" and len(t) == n + 1
    for i in range(n // 2):
        a, b = 2 * i, 2 * i + 1
        assert t[1 + 2 * i] == ("power", ("square", ("var", a)), ("sum", ("square", ("var", b)), ("num", 1.0)))
        assert t[2 + 2 * i] == ("power", ("square", ("var", b)), ("sum", ("square", ("var", a)), ("num", 1.0)))


def coeffs_exact(lam, m):
    """Exact rational beta_k, q_k (k = 0..n-1) from dualized rows j < m, and sum lam_j."""
    L = [Fraction(float(v)) for v in lam]
    beta = [Fraction(0)] * n
    q = [Fraction(0)] * n
    for j in range(m):
        beta[j] += -L[j]; beta[j + 1] += 3 * L[j]; beta[j + 2] += -2 * L[j]; q[j + 1] += -2 * L[j]
    return beta, q, sum(L[:m], Fraction(0))


def clean_multipliers(lam, J1=30, J2=960):
    """Any multipliers give a valid bound. Setting lam_j to one constant for J1 <= j <= J2
    (where the KKT values agree to ~1e-9) makes all middle pair problems identical
    (beta = 0 exactly, q = -2 lam_bar), so one branch-and-bound covers them."""
    lam = lam.copy()
    lam[J1:J2 + 1] = lam[(J1 + J2) // 2]
    return lam


def F2iv(fr):
    return iv.mpf(fr.numerator) / fr.denominator


# ---------- forward-mode AD with mpmath intervals ----------
class D:
    __slots__ = ("v", "a", "b")

    def __init__(s, v, a, b):
        s.v, s.a, s.b = v, a, b

    def __add__(s, o):
        if isinstance(o, D):
            return D(s.v + o.v, s.a + o.a, s.b + o.b)
        return D(s.v + o, s.a, s.b)

    __radd__ = __add__

    def __sub__(s, o):
        if isinstance(o, D):
            return D(s.v - o.v, s.a - o.a, s.b - o.b)
        return D(s.v - o, s.a, s.b)

    def __rsub__(s, o):
        return D(o - s.v, -s.a, -s.b)

    def __mul__(s, o):
        if isinstance(o, D):
            return D(s.v * o.v, s.a * o.v + s.v * o.a, s.b * o.v + s.v * o.b)
        return D(s.v * o, s.a * o, s.b * o)

    __rmul__ = __mul__

    def sq(s):
        return D(iv.square(s.v) if hasattr(iv, "square") else s.v ** 2, 2 * s.v * s.a, 2 * s.v * s.b)


def contains_zero(x):
    return mp.mpf(x.a) <= 0 <= mp.mpf(x.b)


def ipow_nat(base, e):
    """Natural enclosure of base^e, base >= 0, e >= 0 (monotone in each argument)."""
    return base ** e


def f_nat(a, b):
    a2, b2 = a ** 2, b ** 2
    return a2 ** (b2 + 1) + b2 ** (a2 + 1)


def f_ad(a, b):
    """f with gradient; a, b are D. Requires a.v, b.v excluding 0 (checked by caller)."""
    A2, B2 = a.sq(), b.sq()
    E1, E2 = B2 + 1, A2 + 1
    T1v = A2.v ** E1.v
    T2v = B2.v ** E2.v
    lA, lB = iv.log(A2.v), iv.log(B2.v)
    # d(A^E) = A^E ln A dE + E A^(E-1) dA
    c1 = E1.v * A2.v ** (E1.v - 1)
    c2 = E2.v * B2.v ** (E2.v - 1)
    ga = T1v * lA * E1.a + c1 * A2.a + T2v * lB * E2.a + c2 * B2.a
    gb = T1v * lA * E1.b + c1 * A2.b + T2v * lB * E2.b + c2 * B2.b
    return D(T1v + T2v, ga, gb)


class PairFun:
    """l(a, b) = sum_{k<K} f(P^k(a,b)) + ba a + qa a^2 + bb b + qb b^2 (K = 1: head pair)."""

    def __init__(s, ba, qa, bb, qb, K=1):
        s.ba, s.qa, s.bb, s.qb, s.K = ba, qa, bb, qb, K

    @staticmethod
    def step(x0, x1):  # x2 = (1 + 3 x1 - 2 x1^2 - x0)/2
        if isinstance(x0, D):
            return (1 + 3 * x1 - 2 * x1.sq() - x0) * iv.mpf(0.5)
        return (1 + 3 * x1 - 2 * x1 ** 2 - x0) * iv.mpf(0.5)

    def nat(s, a, b):
        val = s.ba * a + s.qa * a ** 2 + s.bb * b + s.qb * b ** 2
        x0, x1 = a, b
        for k in range(s.K):
            val += f_nat(x0, x1)
            if k < s.K - 1:
                x2 = s.step(x0, x1); x3 = s.step(x1, x2); x0, x1 = x2, x3
        return val

    def grad(s, a, b):
        """Interval gradient over the box, or None if some f-argument interval contains 0."""
        A = D(a, iv.mpf(1), iv.mpf(0)); B = D(b, iv.mpf(0), iv.mpf(1))
        val = A * s.ba + A.sq() * s.qa + B * s.bb + B.sq() * s.qb
        x0, x1 = A, B
        for k in range(s.K):
            if contains_zero(x0.v) or contains_zero(x1.v):
                return None
            val = val + f_ad(x0, x1)
            if k < s.K - 1:
                x2 = s.step(x0, x1); x3 = s.step(x1, x2); x0, x1 = x2, x3
        return val.a, val.b


def box_lb(fun, a, b):
    nat = fun.nat(a, b)
    lb = nat.a
    g = fun.grad(a, b)
    if g is not None:
        ca, cb = iv.mpf(a.mid), iv.mpf(b.mid)
        fc = fun.nat(ca, cb)
        mv = fc + g[0] * (a - ca) + g[1] * (b - cb)
        lb = max(mp.mpf(lb), mp.mpf(mv.a))
    return mp.mpf(lb)


def bnb(fun, R_a, R_b, tol, max_boxes=400000, x0=None):
    """Rigorous lower bound of min fun over [-R_a, R_a] x [-R_b, R_b]."""
    UB = mp.inf
    if x0 is not None:
        UB = mp.mpf(fun.nat(iv.mpf(x0[0]), iv.mpf(x0[1])).b)
    root = (iv.mpf([-R_a, R_a]), iv.mpf([-R_b, R_b]))
    heap = [(box_lb(fun, *root), 0, root)]
    cnt, processed = 1, 0
    while heap:
        lb, _, (a, b) = heap[0]
        if UB - lb <= tol or processed >= max_boxes:
            break
        heapq.heappop(heap)
        processed += 1
        # incumbent from the center
        UB = min(UB, mp.mpf(fun.nat(iv.mpf(a.mid), iv.mpf(b.mid)).b))
        if lb > UB:
            continue
        if a.delta >= b.delta:
            m = a.mid
            kids = [(iv.mpf([a.a, m]), b), (iv.mpf([m, a.b]), b)]
        else:
            m = b.mid
            kids = [(a, iv.mpf([b.a, m])), (a, iv.mpf([m, b.b]))]
        for k in kids:
            kl = box_lb(fun, *k)
            if kl <= UB:
                cnt += 1
                heapq.heappush(heap, (kl, cnt, k))
    LB = heap[0][0] if heap else UB
    return mp.mpf(LB), mp.mpf(UB), processed, len(heap)


def radius(qa, ba, qb, bb, UB):
    """R such that psi_a(t) + min psi_b > UB for |t| >= R (checked in intervals)."""
    def min_psi(q, beta):
        c = [q + beta, q - beta]  # |t| < 1 part (concave since q < 0): endpoints t = +-1
        opq = 1 + q
        assert opq.a > 0
        c += [opq + beta, opq - beta]
        tv = -beta / (2 * opq)
        if (abs(tv)).b >= 1:
            c.append(-(beta ** 2) / (4 * opq))
        return min(mp.mpf(x.a) for x in c)
    mb = min_psi(qb, bb)
    opq = 1 + qa
    target = UB - mb
    # (1+q) R^2 - |beta| R - target > 0
    babs = max(abs(mp.mpf(ba.a)), abs(mp.mpf(ba.b)))
    oa = mp.mpf(opq.a)
    Rf = (babs + mp.sqrt(babs ** 2 + 4 * oa * max(target, 0))) / (2 * oa)
    R = max(mp.mpf(1), Rf) * mp.mpf("1.01") + mp.mpf("0.01")
    check = opq * R ** 2 - babs * R - target
    assert mp.mpf(check.a) > 0 and R >= babs / (2 * mp.mpf(opq.a))
    return R


def main(K=3, tol_mid=1e-11, tol=1e-9):
    t0 = time.time()
    I = load("lukvle10")
    pattern_check(I)
    x = load_sol("minlplib_sol/lukvle10.p5.sol")
    chk = check("lukvle10", x, I)
    lam, res = kkt_multipliers(x)
    lam = clean_multipliers(lam)
    m = n - 2 * K
    beta, q, lamsum = coeffs_exact(lam, m)
    # group head pairs by exact coefficients
    groups = {}
    for i in range(m // 2):
        key = (beta[2 * i], q[2 * i], beta[2 * i + 1], q[2 * i + 1])
        groups.setdefault(key, []).append(i)
    print(f"{len(groups)} distinct head pair problems; KKT residual {res:.2e}", flush=True)
    total = F2iv(lamsum)
    details = []
    for key, members in sorted(groups.items(), key=lambda kv: kv[1][0]):
        ba, qa, bb, qb = [F2iv(v) for v in key]
        fun = PairFun(ba, qa, bb, qb, K=1)
        i0 = members[0]
        xp = (x[2 * i0], x[2 * i0 + 1])
        UBp = mp.mpf(fun.nat(iv.mpf(xp[0]), iv.mpf(xp[1])).b) + 1
        Ra = radius(qa, ba, qb, bb, UBp)
        Rb = radius(qb, bb, qa, ba, UBp)
        LB, UB, proc, left = bnb(fun, Ra, Rb, tol_mid if len(members) > 10 else tol, x0=xp)
        total += iv.mpf(LB) * len(members)
        details.append(dict(first_pair=i0, count=len(members), R=[float(Ra), float(Rb)], LB=float(LB), UB=float(UB),
                            boxes=proc, open_boxes=left))
        print(details[-1], flush=True)
    # tail block
    ba, qa, bb, qb = F2iv(beta[m]), F2iv(q[m]), F2iv(beta[m + 1]), F2iv(q[m + 1])
    tail = PairFun(ba, qa, bb, qb, K=K)
    xp = (x[m], x[m + 1])
    UBt = mp.mpf(tail.nat(iv.mpf(xp[0]), iv.mpf(xp[1])).b) + 1
    Ra = radius(qa, ba, qb, bb, UBt)
    Rb = radius(qb, bb, qa, ba, UBt)
    LBt, UBt2, proc, left = bnb(tail, Ra, Rb, tol, max_boxes=2000000, x0=xp)
    total += iv.mpf(LBt)
    details.append(dict(tail=True, K=K, R=[float(Ra), float(Rb)], LB=float(LBt), UB=float(UBt2), boxes=proc, open_boxes=left))
    print(details[-1], flush=True)
    rec = dict(name="lukvle10", K=K, primal_obj=chk["obj"], primal_cons_viol=chk["cons_viol"],
               dual_bound=float(mp.mpf(total.a)), groups=details, seconds=time.time() - t0)
    print(json.dumps({k: v for k, v in rec.items() if k != "groups"}), flush=True)
    with open(f"logs/lukvle10_bound_K{K}.json", "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main(K=int(sys.argv[1]) if len(sys.argv) > 1 else 3)
