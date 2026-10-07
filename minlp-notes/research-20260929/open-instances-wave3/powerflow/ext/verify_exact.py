"""Second, float-free evaluation of the pf_bb3 leaf certificates (written separately from
pf_cert.certify): for each stored leaf (box, multipliers) rebuild the node rows, form
    L(x, y) = obj(y) + sum_eq w (h - rhs) + sum_ineq [m+ (h - ub) + m- (lb - h)]
            = const + sum_y (sigma_y y^2 + kappa_y y) + x^T A x
exactly in rationals, minimize the y part exactly over the y boxes, and prove A >= 0 by an
exact LDL^T factorization (symmetric pivoting on the diagonal; a zero pivot requires a
zero remaining column), applied to A + eps I for the smallest eps in {0, 1e-9, ..., 1e-5}
that succeeds; then x^T A x >= -eps sum_k vmax_k^2 on R.  Leaves whose unboxed y terms are not
bounded below (sigma_y = 0, kappa_y != 0) are reported as failures here.
    python3 verify_exact.py <name> [tag]
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pf_model as pm  # noqa: E402
import leafcut as lc  # noqa: E402
from pf_bb3 import node_model  # noqa: E402


def exact_bound(M, rows, raw):
    const = M["obj"]["const"]
    kap = dict(M["obj"]["lin"])
    sig = dict(M["obj"]["qy"])
    A = {}
    for r, rv in zip(rows, raw):
        if rv[0] == "eq":
            w = Fr(rv[1])
            const -= w * r["lb"]
        else:
            mp_ = Fr(max(rv[1], 0.0)) if rv[1] is not None else Fr(0)
            mm_ = Fr(max(rv[2], 0.0)) if rv[2] is not None else Fr(0)
            assert mp_ == 0 or r["ub"] is not None
            assert mm_ == 0 or r["lb"] is not None
            if mp_:
                const -= mp_ * r["ub"]
            if mm_:
                const += mm_ * r["lb"]
            w = mp_ - mm_
        if w == 0:
            continue
        for y, c in r["lin"].items():
            kap[y] = kap.get(y, Fr(0)) + w * c
        for y, c in r["qy"].items():
            sig[y] = sig.get(y, Fr(0)) + w * c
        for (i, j), c in r["Q"].items():
            if i == j:
                A[(i, i)] = A.get((i, i), Fr(0)) + w * c
            else:
                h = w * c / 2
                A[(i, j)] = A.get((i, j), Fr(0)) + h
                A[(j, i)] = A.get((j, i), Fr(0)) + h
    inner = Fr(0)
    for y in M["ys"]:
        s, k = sig.get(y, Fr(0)), kap.get(y, Fr(0))
        if s < 0:
            return None, f"sigma < 0 for y{y}"
        box = M["ybox"].get(y)
        if box is not None:
            l, u = box
            if s > 0:
                t = min(max(-k / (2 * s), l), u)
                inner += s * t * t + k * t
            else:
                inner += min(k * l, k * u)
        elif s > 0:
            inner -= k * k / (4 * s)
        elif k != 0:
            return None, f"unbounded y{y}"
    n = 2 * M["n"]
    # smallest eps in the list with A + eps I >= 0 (exact); then x^T A x >= -eps sum_k vmax_k^2
    for eps in (Fr(0), Fr(1, 10**9), Fr(1, 10**8), Fr(1, 10**7), Fr(1, 10**6), Fr(1, 10**5)):
        if ldl_psd([[A.get((i, j), Fr(0)) + (eps if i == j else 0) for j in range(n)] for i in range(n)]):
            return const + inner - eps * sum(M["vmax2"]), f"ok, exact eps {eps}"
    return None, "A + 1e-5 I not psd"


def ldl_psd(A):
    """exact test of A >= 0 (A symmetric, list of lists of Fractions)."""
    n = len(A)
    A = [row[:] for row in A]
    alive = list(range(n))
    while alive:
        # pick the largest diagonal among the remaining indices
        k = max(alive, key=lambda i: A[i][i])
        d = A[k][k]
        if d < 0:
            return False
        if d == 0:
            # psd requires the whole remaining row to vanish
            if any(A[k][j] != 0 for j in alive):
                return False
            alive.remove(k)
            continue
        alive.remove(k)
        rk = A[k]
        nz = [j for j in alive if rk[j] != 0]
        for i in nz:
            f = rk[i] / d
            Ai = A[i]
            for j in nz:
                Ai[j] -= f * rk[j]
    return True


def main(name, tag="bb3"):
    D = json.load(open(os.path.join(HERE, "logs", f"{name}.{tag}.json")))
    M = pm.decode(name)
    info = lc.leaf_info(M)
    LB = None
    for L in D["leaves"]:
        bx = tuple((Fr(a), Fr(c)) for a, c in L["box"])
        t = time.time()
        MM, extra = node_model(M, info, bx)
        rows = list(MM["rows"]) + extra
        b, msg = exact_bound(MM, rows, L["raw"])
        print(f"  leaf {[[round(float(a), 6), round(float(c), 6)] for a, c in bx]}: stored {float(Fr(L['bound']))!r} "
              f"exact {None if b is None else float(b)!r} ({msg}) {time.time()-t:.1f}s")
        assert b is not None
        LB = b if LB is None else min(LB, b)
    k12 = int(LB * 10**12)
    assert Fr(k12, 10**12) <= LB
    print(f"{name}: float-free minimum over leaves {float(LB)!r}; rational bound {k12}/10^12 <= minimum")


if __name__ == "__main__":
    main(*sys.argv[1:])
