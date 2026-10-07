"""Estimate the floating-point error of the prototype's min-sum DP at large n (study, 4.3).

Records the unary and pair piece bounds of the final iteration of chain_bb (amp 0.2, n = 8192,
seed 0, eps 1e-6), recomputes the forward DP in float64 and in np.longdouble (64-bit mantissa),
and reports the difference, plus the largest |partial sum| (which sets the rigorous bound
sum_k |S_k| * u for recursive summation).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import instances as I
import chain_bb as CB

n, seed, amp, eps = int(sys.argv[1]), 0, 0.2, 1e-6
store = {}
orig_tr, orig_us = CB.transfers, CB.unary_lb_sub


def tr(prob, xhat, mode):
    store["u"], store["P"] = [], []
    return orig_tr(prob, xhat, mode)


def us(prob, vidx, p, q, Qt, Lt, sub):
    out = orig_us(prob, vidx, p, q, Qt, Lt, sub)
    store["u"].append(out.copy())
    return out


class Rec(I.Probe3Chain):
    def pair_lb(self, *a):
        out = super().pair_lb(*a)
        store["P"].append(out.copy())
        return out


CB.transfers, CB.unary_lb_sub = tr, us
r = CB.chain_bb(Rec(I.coeffs(n, seed, amp)), eps, mode="quad", unary_sub=16, max_pairs_iter=30_000_000)
K = np.array([len(c) for c in r["cell_list"]])
uflat = np.concatenate(store["u"]); pflat = np.concatenate(store["P"])
assert len(uflat) == K.sum() and len(pflat) == (K[:-1] * K[1:]).sum()
uo = np.concatenate([[0], np.cumsum(K)])
po = np.concatenate([[0], np.cumsum(K[:-1] * K[1:])])


def dp(dtype):
    f = uflat[uo[0]:uo[1]].astype(dtype); big = float(np.abs(f).max())
    for e in range(n - 1):
        P = pflat[po[e]:po[e + 1]].reshape(K[e], K[e + 1]).astype(dtype)
        f = (f[:, None] + P).min(axis=0) + uflat[uo[e + 1]:uo[e + 2]].astype(dtype)
        big = max(big, float(np.abs(f).max()))
    return f.min(), big


lb64, big = dp(np.float64)
lbld, _ = dp(np.longdouble)
print(f"status={r['status']} LB={r['LB']!r} UB={r['UB']!r} final K max={K.max()}")
print(f"DP float64={lb64!r} longdouble={float(lbld)!r} diff={float(lb64 - lbld):.3e}")
print(f"max |partial sum| = {big:.3f}; rigorous recursive-summation bound 2n*max|S|*u = "
      f"{2 * n * big * 1.11e-16:.3e}")
