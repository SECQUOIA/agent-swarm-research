"""Analyse logs/sweep_sphere.jsonl: growth rates and lower bounds (Section 9 of the note).

For each instance: bisection nodes and leaves = (nodes+1)/2; the local exponent
log(nodes_k/nodes_{k-1}) / log(eps_{k-1}/eps_k); the Theorem 4.5(i) lower bound
on the number of leaves of ANY certificate,
    alpha^{d/2} * int_S (m + eps)^{-d/2} dsigma / (C_{n,d} * sum_I M^I(S)),
    C_{n,d} = (pi^2/d)^{d/2} * binom(n,d)^{1/2},
for the strata S = unit circle/sphere (d = n-1; every coordinate line meets it in
<= 2 points, so sum_I M^I <= 2n) and, when the optimal set M is a great circle in
R^3, S = M (d = 1; sum_I M^I <= 4).  For the ball instances also the
full-dimensional integral (alpha n/pi^2)^{n/2} int_F (m+eps)^{-n/2}, which is a
valid but weaker bound with the wrong exponent.  The full-dimensional integral
is also computed for all 3D ball instances by a second method (closed-form
radial integral, angular quadrature with polar axis e_1) as a cross-check; for
B3_iso it stays bounded as eps -> 0 (Section 8.2 of the note).
Usage: python3 analyze_sweep.py
"""
import json
import math
from scipy import integrate

C = {"S2_iso": [1, .5], "S2_circ": [1, 1], "S3_iso": [1, .5, .25], "S3_circ": [1, 1, .5],
     "S3_all": [1, 1, 1], "B2_circ": [1, 1], "B3_iso": [1, .5, .25], "B3_circ": [1, 1, .5],
     "B3_all": [1, 1, 1]}


def Cnd(n, d):
    return (math.pi ** 2 / d) ** (d / 2) * math.comb(n, d) ** 0.5


def sphere_stratum_integral(c, eps):
    cm = max(c)
    if len(c) == 2:
        g = lambda t: ((cm - c[0]) * math.cos(t) ** 2 + (cm - c[1]) * math.sin(t) ** 2 + eps) ** -0.5
        return integrate.quad(g, 0, 2 * math.pi, points=[0.5 * math.pi, math.pi, 1.5 * math.pi],
                              limit=400)[0]

    def inner(ph):  # polar angle ph from the y3 axis, azimuth th
        def h(th):
            y = (math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph))
            m = sum((cm - ci) * yi * yi for ci, yi in zip(c, y))
            return (m + eps) ** -1.0
        return integrate.quad(h, 0, 2 * math.pi, points=[0.5 * math.pi, math.pi, 1.5 * math.pi],
                              limit=400)[0] * math.sin(ph)
    return integrate.quad(inner, 0, math.pi, points=[0.5 * math.pi], limit=400)[0]


def ball_full_integral(c, eps):
    n = len(c)
    if n == 2 and c[0] == c[1]:
        return math.pi * math.log((1 + eps) / eps)

    def inner(ph):  # c1 = c2 >= c3 assumed; m = 1 - r^2 k(ph)
        k = (c[0] * math.sin(ph) ** 2 + c[2] * math.cos(ph) ** 2) / max(c)
        pts = [x for x in (1 - 30 * eps, 1 - 3 * eps, 1 - math.sqrt(eps)) if 0 < x < 1]
        rad = integrate.quad(lambda r: (max(c) * (1 - k * r * r) + eps) ** -1.5 * r * r, 0, 1,
                             points=pts, limit=1000)[0]
        return 2 * math.pi * rad * math.sin(ph)
    h = 0.5 * math.pi
    pts = [h - 3 * math.sqrt(eps), h - math.sqrt(eps), h, h + math.sqrt(eps), h + 3 * math.sqrt(eps)]
    return integrate.quad(inner, 0, math.pi, points=pts, limit=1000)[0]


def ball_full_integral_general(c, eps):
    """int_{unit ball} (m + eps)^{-3/2}, m = cmax - sum c_i y_i^2, n = 3.
    With a = 1 + eps/cmax and k(u) = sum c_i u_i^2 / cmax, the radial integral
    int_0^1 r^2 (a - k r^2)^{-3/2} dr = 1/(k sqrt(a-k)) - asin(sqrt(k/a))/k^1.5."""
    cm = max(c)
    a = 1 + eps / cm

    def radial(k):
        return 1 / (k * math.sqrt(a - k)) - math.asin(math.sqrt(k / a)) / k ** 1.5

    def inner(ph):
        def h(th):
            u = (math.cos(ph), math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th))
            k = sum(ci * ui * ui for ci, ui in zip(c, u)) / cm
            return radial(k)
        return integrate.quad(h, 0, 2 * math.pi, points=[0.5 * math.pi, math.pi, 1.5 * math.pi],
                              limit=400)[0] * math.sin(ph)
    pts = [x for x in (math.sqrt(eps), 3 * math.sqrt(eps), 0.5 * math.pi,
                       math.pi - 3 * math.sqrt(eps), math.pi - math.sqrt(eps)) if 0 < x < math.pi]
    return cm ** -1.5 * integrate.quad(inner, 0, math.pi, points=pts, limit=1000)[0]


def main():
    rows = [json.loads(l) for l in open("logs/sweep_sphere.jsonl")]
    for inst in C:
        rs = sorted([r for r in rows if r["inst"] == inst], key=lambda r: -r["eps"])
        c = C[inst]
        n = len(c)
        alpha = 1.1 * max(c)
        mult_max = sum(1 for ci in c if ci == max(c))
        p = mult_max - 1
        print(f"== {inst}: n={n}, c={c}, alpha={alpha:.2f}, dim optimal set p={p}")
        prev = None
        for r in rs:
            eps, nodes = r["eps"], r["nodes"]
            leaves = (nodes + 1) / 2
            lb_S = alpha ** ((n - 1) / 2) * sphere_stratum_integral(c, eps) / (Cnd(n, n - 1) * 2 * n)
            lb = lb_S
            extra = ""
            if n == 3 and p == 1:
                lb_M = alpha ** 0.5 * 2 * math.pi * eps ** -0.5 / (Cnd(3, 1) * 4)
                lb = max(lb, lb_M)
            if inst.startswith("B") and inst != "B3_iso":
                full = (alpha * n / math.pi ** 2) ** (n / 2) * ball_full_integral(c, eps)
                extra = f" full-dim bound {full:8.2f}"
            if inst.startswith("B3"):
                full2 = (alpha * n / math.pi ** 2) ** (n / 2) * ball_full_integral_general(c, eps)
                extra += f" full-dim (method 2) {full2:8.2f}"
            slope = ""
            if prev is not None:
                slope = f" exponent {math.log(nodes / prev[1]) / math.log(prev[0] / eps):.2f}" \
                        f" (+{nodes - prev[1]} nodes)"
            print(f"eps={eps:7.1e} nodes={nodes:7d} leaves={leaves:9.1f} ThmLB={lb:9.2f} "
                  f"leaves/LB={leaves / lb:7.1f}{extra}{slope}")
            prev = (eps, nodes)


if __name__ == "__main__":
    main()
