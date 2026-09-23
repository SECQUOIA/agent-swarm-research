"""Kissing-number (spherical code) instances knpD-N: exact feasibility check of classical configurations.

Model (verified by parsing): points x_i in R^D (x-variables in blocks of D, bounds [-2,2]),
rows ||x_i||^2 = 4, rows ||x_i - x_j||^2 - 4*objvar >= 0 (all pairs), maximize objvar.
So objvar* = max over N-point codes of min_{i<j} ||x_i - x_j||^2 / 4 = 2 - 2 cos(theta_min);
objvar >= 1 iff N unit balls can all touch a central unit ball (kissing configuration).
"""
import itertools, os, sympy
from osil_eval import Model, exact_backend

OS = os.path.expanduser("~/.cache/minlplib/minlplib/osil/")
LISTED = {"knp3-12": (1.105572809, 2.280669105), "knp4-24": (1.0, 3.676074738),
          "knp5-40": (0.9848552014, 4.000000002)}


def icosahedron():
    phi = (1 + sympy.sqrt(5)) / 2
    pts = []
    for a, b in itertools.product([1, -1], repeat=2):
        for v in [(0, a, b * phi), (a, b * phi, 0), (b * phi, 0, a)]:
            pts.append(v)
    s = 2 / sympy.sqrt(1 + phi ** 2)
    return [tuple(sympy.radsimp(s * c) for c in p) for p in pts]


def cell24():  # Hurwitz units scaled to radius 2: integer coordinates
    pts = []
    for i in range(4):
        for sg in (2, -2):
            v = [0] * 4; v[i] = sg; pts.append(tuple(v))
    pts += list(itertools.product([1, -1], repeat=4))
    return [tuple(sympy.Integer(c) for c in p) for p in pts]


def d5roots():  # +-e_i +- e_j, scaled by sqrt(2) to radius 2
    pts = []
    for i, j in itertools.combinations(range(5), 2):
        for a, b in itertools.product([1, -1], repeat=2):
            v = [0] * 5; v[i] = a; v[j] = b
            pts.append(tuple(sympy.sqrt(2) * c for c in v))
    return pts


def main():
    B = exact_backend()
    for name, pts in [("knp3-12", icosahedron()), ("knp4-24", cell24()), ("knp5-40", d5roots())]:
        M = Model(OS + name + ".osil")
        D = len(pts[0]); N = len(pts)
        assert M.n == N * D + 1
        alpha = min(sympy.nsimplify(sympy.expand(sum((a - b) ** 2 for a, b in zip(p, q))))
                    for p, q in itertools.combinations(pts, 2)) / 4
        alpha = sympy.radsimp(alpha)
        x = [c for p in pts for c in p] + [alpha]
        v = M.check(x, B)
        viol_b = sympy.simplify(v["bound"][0]); viol_r = sympy.simplify(v["row"][0])
        # exact: every equality row residual simplifies to 0 and every >= row to a nonnegative number
        nonzero_eq = 0
        for r in range(M.m):
            a = sympy.simplify(sympy.expand(M.row_value(r, x, B)))
            if M.clb[r] == M.cub[r] and sympy.simplify(a - sympy.Rational(M.clb[r])) != 0:
                nonzero_eq += 1
        obj = M.objective(x, B)
        p, d = LISTED[name]
        print(f"{name}: N={N}, D={D}, objvar = {obj} = {sympy.N(obj, 15)}; max bound viol {viol_b}, "
              f"max row viol {viol_r} (exact), equality rows not exactly satisfied: {nonzero_eq}; "
              f"listed primal {p}, listed dual {d}")


if __name__ == "__main__":
    main()
