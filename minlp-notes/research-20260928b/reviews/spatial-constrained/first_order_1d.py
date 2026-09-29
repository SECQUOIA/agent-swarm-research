"""Reviewer's check of Theorem 8.2 (first-order gaps) in 1D, with exact N_opt.

f(y) = (y - a)^2 on X0 = [0, 1], a = 1/3, f* = 0.  Lip_inf(f) = 4/3.
Node bound: vertex Lipschitz bound f_B(y) = max(f(l) - L_B (y-l), f(u) - L_B (u-y)), L_B = 8/3, so
  LB([l,u]) = (f(l)+f(u))/2 - L_B (u-l)/2   (value at the crossing of the two cones).
(G^1_alpha) holds with alpha = L_B - Lip = 4/3; (U^1_tau) with tau = Lip + L_B = 4.
LB of a sub-interval is >= LB of the interval (cone from an inner vertex dominates), so the greedy
sweep gives the exact N_opt.
Compares N_opt with the lower bounds of Theorem 8.2(a) (best eta), (c) and (e), and binary bisection
with the upper bound of Theorem 8.2(b) (kappa = 0, n = 1).
Usage: python3 first_order_1d.py
"""
import math
from scipy import integrate

A = 1 / 3
LIP = 2 * (1 - A)
LB_ = 2 * LIP
ALPHA = LB_ - LIP
TAU = LIP + LB_
f = lambda y: (y - A) ** 2


def lbnd(l, u):
    return 0.5 * (f(l) + f(u)) - 0.5 * LB_ * (u - l)


def nopt(eps):
    l, cnt = 0.0, 0
    while l < 1.0:
        cnt += 1
        if lbnd(l, 1.0) >= -eps:
            break
        lo, hi = l, 1.0
        for _ in range(100):
            m = 0.5 * (lo + hi)
            if lbnd(l, m) >= -eps:
                lo = m
            else:
                hi = m
        l = lo
    return cnt


def bisect_nodes(eps):
    stack, nodes, levels = [(0.0, 1.0, 0)], 0, {}
    while stack:
        l, u, j = stack.pop()
        nodes += 1
        if lbnd(l, u) >= -eps:
            continue
        levels[j] = levels.get(j, 0) + 1
        m = 0.5 * (l + u)
        stack += [(l, m, j + 1), (m, u, j + 1)]
    return nodes


def Nj(j, t):  # closed dyadic cells of side 2^-j meeting E(t) = [A - sqrt t, A + sqrt t] cap [0,1]
    s = 2.0 ** -j
    lo, hi = max(0.0, A - math.sqrt(max(t, 0))), min(1.0, A + math.sqrt(max(t, 0)))
    return min(2 ** j - 1, math.floor(hi / s)) - max(0, math.ceil(lo / s - 1)) + 1


def main():
    print(f"alpha = {ALPHA:.4f}, tau = Lambda_1 = {TAU:.4f}")
    print(" eps     N_opt  N_opt*sqrt(eps) | (a) best eta | (c)     | (e)     | bisect nodes | (b) bound")
    for k in range(2, 11):
        eps = 10.0 ** -k
        N = nopt(eps)
        best_a = 0.0
        for e2 in [eps * 2 ** (i / 4) for i in range(-40, 80)]:
            half = math.sqrt(e2)
            length = min(1.0, A + half) - max(0.0, A - half)
            best_a = max(best_a, 0.5 * math.ceil(length / (2 * (eps + e2) / ALPHA)))
        c_bound = 0.5 * 2 * (ALPHA ** 2 / (8 * 2 * eps)) ** 0.5
        I = integrate.quad(lambda y: 1 / ((y - A) ** 2 + eps), 0, 1, points=[A], limit=400)[0]
        e_bound = ALPHA * I / (2 * (1 + math.log(ALPHA * 1.0 / (2 * eps))))
        nb = bisect_nodes(eps)
        j0 = 0  # v == 0
        ub = 1 + 2 * (2 ** j0 + 3 * sum(Nj(j, TAU * 2.0 ** -j - eps) for j in range(0, 80) if TAU * 2.0 ** -j > eps))
        ok = N >= max(best_a, c_bound, e_bound) and nb <= ub
        print(f" {eps:6.0e} {N:6d} {N * math.sqrt(eps):8.3f}        | {best_a:10.1f}   | {c_bound:7.1f} | {e_bound:7.1f} | {nb:12d} | {ub:9d}  {'ok' if ok else 'VIOLATION'}")


if __name__ == "__main__":
    main()
