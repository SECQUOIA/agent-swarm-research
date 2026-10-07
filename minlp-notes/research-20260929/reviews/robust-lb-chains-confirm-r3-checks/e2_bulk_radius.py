"""Referee check: per-bond (bulk) version of 'opposite orientation + ball 2M^2 - x^2 - y^2'.

Bulk problem (translation-invariant certificate for the infinite chain):
  maximize gamma  s.t.  W(x, y) + h(x) - h(y) - gamma
      = s0(x, y) + s1(x, y) (1 + x) + s2(x, y) (1 - y) + s3(x, y) (2M^2 - x^2 - y^2),
  h univariate of degree <= 4 (the shared moments of one variable), s0 SOS of degree 4,
  s1, s2, s3 SOS of degree 2 in (x, y).
  W(x, y) = (a/2)(x^2 + y^2) + b x y + (g/2)(x y^2 - x^2 y), (b, g, ev) = (0.6, 0.3, 0.05), a = b + ev.
Opposite orientation: in clique (e, e+1) the constraints are 1 + x_e and 1 - x_{e+1}.
gamma* < 0 means a root gap of at least about |gamma*| per bond for long chains (heuristic: the end
terms are ignored); gamma* = 0 means the bulk is exact.
Also: finite-n moment values (e1_two_sides.mom_side) at n = 64 for a few M.
Floating point (Clarabel).
"""
import sys
import json
import itertools

import cvxpy as cp

B, G, EV = 0.6, 0.3, 0.05
A = B + EV


def bulk(M, place="opp"):
    acc = {}
    def put(k, expr):
        acc.setdefault(k, []).append(expr)
    gamma = cp.Variable()
    h = cp.Variable(5)  # h_0..h_4, h_0 irrelevant
    put((0, 0), gamma)
    for d in range(1, 5):
        put((d, 0), -h[d])   # move h(x) - h(y) to the right side: W - gamma = ... - h(x) + h(y)
        put((0, d), h[d])
    basis2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
    basis1 = [(0, 0), (1, 0), (0, 1)]
    def gram(basis, poly):
        Q = cp.Variable((len(basis), len(basis)), PSD=True)
        for i, j in itertools.product(range(len(basis)), repeat=2):
            for k, c in poly.items():
                put((basis[i][0] + basis[j][0] + k[0], basis[i][1] + basis[j][1] + k[1]), c * Q[i, j])
    gram(basis2, {(0, 0): 1.0})
    if place == "opp":
        gram(basis1, {(0, 0): 1.0, (1, 0): 1.0})    # 1 + x
        gram(basis1, {(0, 0): 1.0, (0, 1): -1.0})   # 1 - y
    elif place == "match":
        gram(basis1, {(0, 0): 1.0, (1, 0): -1.0})   # 1 - x
        gram(basis1, {(0, 0): 1.0, (0, 1): 1.0})    # 1 + y
    if M is not None:
        gram(basis1, {(0, 0): 2 * M ** 2, (2, 0): -1.0, (0, 2): -1.0})
    W = {(2, 0): A / 2, (0, 2): A / 2, (1, 1): B, (1, 2): G / 2, (2, 1): -G / 2}
    keys = set(acc) | set(W)
    cons = [cp.sum(cp.hstack(acc.get(k, [cp.Constant(0.0)]))) == W.get(k, 0.0) for k in keys]
    prob = cp.Problem(cp.Maximize(gamma), cons)
    prob.solve(solver="CLARABEL")
    return prob.status, (None if prob.value is None else float(f"{prob.value:.7g}"))


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "bulk":
        print(json.dumps(dict(place="match", M=None, bulk=bulk(None, "match"))), flush=True)
        print(json.dumps(dict(place="opp", M=None, bulk=bulk(None, "opp"))), flush=True)
        for M in (1.0, 1.0408, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 10.0):
            print(json.dumps(dict(place="opp", M=M, bulk=bulk(M))), flush=True)
        lo, hi = 1.0, 3.0
        for _ in range(30):
            mid = (lo + hi) / 2
            if bulk(mid)[1] > -1e-7:
                lo = mid
            else:
                hi = mid
        print(json.dumps(dict(threshold_M_bulk=[lo, hi])), flush=True)
    elif what == "long":
        from e1_two_sides import run
        for n, M in [(64, 1.5), (64, 1.3), (64, 1.1), (128, 1.5)]:
            run(n, "opp", ball=M, sides=("mom",))
