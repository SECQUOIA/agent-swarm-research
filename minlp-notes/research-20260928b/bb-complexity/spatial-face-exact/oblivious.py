"""Theorem 5.2 check: oblivious branching rules on the aligned-kink family, and the R(alpha<1) remark.

f_a(x,y)  = L|x-a| + c (x-a)(y-b0)   (optimal set: x = a),
f'_b(x,y) = L|y-b| + c (x-a0)(y-b)   (optimal set: y = b),   L = 2, c = -1, on [0,1]^2.
Both have N_opt = 2 for every a, b and every eps >= 0 (Theorem 4.1).

The node bound is computed exactly (closed form): the McCormick relaxation is a convex piecewise-linear
function whose breaklines are the kink line and the envelope ridge (a box diagonal), so its minimum over
the box is attained at a box corner, a kink-line/edge intersection, or the kink-line/ridge intersection.
Cross-checked against the HiGHS LP of face_bb.py on random boxes.

Oblivious rules (split tree independent of the instance), split ratio in [beta, 1-beta]:
  O1 bisection, widest side (beta = 1/2);  O2 ratio 0.3, widest side (beta = 0.3);
  O3 ratio 0.3, coordinates alternating with depth (beta = 0.3);
  O4 pseudo-random ratio in [0.2, 0.8] from a hash of the box, widest side (beta = 0.2).
Theorem 5.2: E_a N(f_a) + E_b N(f'_b) >= beta * sqrt(|c| / (8 eps)) for a, b ~ U[0,1].
"""
import math
import sys
import numpy as np

L, C = 2.0, -1.0
A0, B0 = 1.0 / 3.0, math.sqrt(2.0) - 1.0


def lb_kink(l, u, a, b, kink_in_x):
    Xl, Xu, Yl, Yu = l[0] - a, u[0] - a, l[1] - b, u[1] - b

    def fB(X, Y):
        k = L * abs(X) if kink_in_x else L * abs(Y)
        if C > 0:
            env = C * max(Yl * X + Xl * Y - Xl * Yl, Yu * X + Xu * Y - Xu * Yu)
        else:
            env = max(C * (Yu * X + Xl * Y - Xl * Yu), C * (Yl * X + Xu * Y - Xu * Yl))
        return k + env

    cands = [(Xl, Yl), (Xl, Yu), (Xu, Yl), (Xu, Yu)]
    wx, wy = Xu - Xl, Yu - Yl
    if kink_in_x and Xl < 0 < Xu:
        cands += [(0.0, Yl), (0.0, Yu)]
        t = -Xl / wx
        cands.append((0.0, Yl + t * wy) if C < 0 else (0.0, Yu - t * wy))
    if (not kink_in_x) and Yl < 0 < Yu:
        cands += [(Xl, 0.0), (Xu, 0.0)]
        t = -Yl / wy
        cands.append((Xl + t * wx, 0.0) if C < 0 else (Xu - t * wx, 0.0))
    return min(fB(X, Y) for X, Y in cands)


def split(rule, l, u, depth):
    w = u - l
    if rule == "O1":
        i = 0 if w[0] >= w[1] else 1; r = 0.5
    elif rule == "O2":
        i = 0 if w[0] >= w[1] else 1; r = 0.3
    elif rule == "O3":
        i = depth % 2; r = 0.3
    elif rule == "O4":
        i = 0 if w[0] >= w[1] else 1
        h = math.sin(1000.0 * (l[0] + 2 * l[1] + 3 * u[0] + 5 * u[1])) * 43758.5453
        r = 0.2 + 0.6 * (h - math.floor(h))
    return i, l[i] + r * w[i]


def count(rule, eps, a, b, kink_in_x, cap=10 ** 6):
    stack = [(np.zeros(2), np.ones(2), 0)]
    n = 0
    while stack:
        l, u, d = stack.pop()
        n += 1
        if n > cap:
            return None
        if lb_kink(l, u, a, b, kink_in_x) >= -eps:
            continue
        i, p = split(rule, l, u, d)
        l1, u1 = l.copy(), u.copy(); u1[i] = p
        l2, u2 = l.copy(), u.copy(); l2[i] = p
        stack += [(l1, u1, d + 1), (l2, u2, d + 1)]
    return n


def crosscheck(trials=300):
    from face_bb import relax
    import instances as I
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(trials):
        a, b = rng.uniform(0, 1, 2)
        l = rng.uniform(0, 0.7, 2); u = l + rng.uniform(0.01, 0.3, 2)
        for kx in (True, False):
            P = I.kink(a=a, b=b) if kx else I.kink_mirror(a=a, b=b)
            worst = max(worst, abs(relax(P, l, u)[0] - lb_kink(l, u, a, b, kx)))
    print(f"closed-form LB vs HiGHS LP on {2 * trials} random boxes: max abs diff = {worst:.2e}")


BETA = {"O1": 0.5, "O2": 0.3, "O3": 0.3, "O4": 0.2}

if __name__ == "__main__":
    crosscheck()
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    grid = (np.arange(K) + 0.5) / K
    for rule in ("O1", "O2", "O3", "O4"):
        for eps in (1e-3, 1e-4, 1e-5, 1e-6):
            Na = [count(rule, eps, a, B0, True) for a in grid]
            Nb = [count(rule, eps, A0, b, False) for b in grid]
            Ea, Eb = np.mean(Na), np.mean(Nb)
            bound = BETA[rule] * math.sqrt(abs(C) / (8 * eps))
            print(f"{rule} eps={eps:.0e}: E_a N(f_a)={Ea:9.1f}  E_b N(f'_b)={Eb:9.1f}  sum={Ea + Eb:9.1f}  "
                  f"Thm5.2 bound={bound:7.1f}  sum*sqrt(eps)={(Ea + Eb) * math.sqrt(eps):.3f}  "
                  f"min_a N={min(Na)} min_b N={min(Nb)}", flush=True)
