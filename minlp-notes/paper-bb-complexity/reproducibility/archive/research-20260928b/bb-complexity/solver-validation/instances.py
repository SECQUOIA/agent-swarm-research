"""Instance families for the SCIP node-exponent experiments.

Every instance is  min f(x)  over a box (plus optional constraints), written
for SCIP as  min t  s.t.  f(x) - t <= 0.  Each f is built so that f* and an
optimal point are known exactly:

  h_c(s)  = (s-1)^2 ((s+1)^2 + c) = s^4 + (c-2) s^2 - 2c s + (1+c) >= 0,
            unique zero at s = 1 (nondegenerate, h'' = 8 + 2c); the concave
            part -(2-c) s^2 is relaxed by secants (gap (2-c)(s-l)(u-s)).
  g4_d(y) = (y+d)^4 + (y-d)^4 - 12 d^2 y^2 - 2 d^4 = 2 y^4  (identity), so
            growth is quartic at y = 0, while SCIP sees two convex quartics
            and a concave quadratic with secant gap 12 d^2 (y-l)(u-y).
  z_d(y)  = g4_d(y) - 2 y^4 = 0 identically ("hidden zero"); SCIP does not
            detect this, so the relaxation has a secant gap in y although f
            does not depend on y.

Expressions are CIP strings; the same string is evaluated in Python with
mpmath to check f at returned points.
"""
import re
import mpmath as mp

mp.mp.dps = 40


def h(c, s):
    """CIP text of h_c(s) for an atom or parenthesised expression s."""
    return f"({s})^4 + ({c - 2:.17g})*({s})^2 + ({-2 * c:.17g})*({s}) + {1 + c:.17g}"


def g4(d, y):
    return (f"({y} + {d:.17g})^4 + ({y} - {d:.17g})^4 + ({-12 * d * d:.17g})*({y})^2"
            f" + ({-2 * d ** 4:.17g})")


def z(d, y):
    return g4(d, y) + f" + (-2)*({y})^4"


def V(i):
    return f"<x{i}>"


def inst(name, family, bounds, obj, xstar, fstar, p, pred, cons=(), notes="", params=None):
    return dict(name=name, family=family, n=len(bounds), bounds=bounds, obj=obj,
                cons=list(cons), xstar=xstar, fstar=fstar, p=p, pred=pred, notes=notes,
                params=params or {})


A3 = "0.3333333333333333"          # a = 1/3 (double)
B2 = "0.41421356237309515"         # b = sqrt(2) - 1 (double)

INSTANCES = {}


def add(d):
    INSTANCES[d["name"]] = d


# ---- (a) isolated nondegenerate minima, (G_alpha) via secants ------------
BX = [(-2.0, 2.2), (-1.9, 2.3), (-2.1, 2.05), (-1.95, 2.15)]
CS = [0.5, 0.7, 0.6, 0.8]
for n in (2, 3, 4):
    add(inst(f"iso{n}", "a:isolated", BX[:n],
             " + ".join(h(CS[i], V(i + 1)) for i in range(n)),
             [1.0] * n, 0.0, 0, dict(kind="log", slope=0.0),
             notes="separable tilted double wells, unique nondegenerate minimizer x=1"))
add(inst("iso2c", "a:isolated", BX[:2],
         h(0.5, V(1)) + " + " + h(0.7, V(2)) + " + 0.5*(<x1> - <x2>)^4",
         [1.0, 1.0], 0.0, 0, dict(kind="log", slope=0.0),
         notes="iso2 plus convex non-separable coupling 0.5(x1-x2)^4"))
# minimizer at 0 with even powers: interval arithmetic is tight there
# (the review's nondeg1 mechanism); the secant gap of -2x^4 is quartic, so
# (G_alpha) fails near the minimizer.
add(inst("isofbbt2", "a:isolated", [(-0.6, 0.55), (-0.55, 0.62)],
         "<x1>^2 - 2*<x1>^4 + <x2>^2 - 1.5*<x2>^4",
         [0.0, 0.0], 0.0, 0, dict(kind="n/a", slope=None),
         notes="review's t^2-2t^4 in 2D; FBBT with the objective cutoff is tight"))

# ---- (b) one-dimensional optimal sets ------------------------------------
add(inst("linediag2", "b:p=1", [(-2.0, 2.2), (-1.9, 2.1)],
         h(0.5, "<x1> - <x2>"), [1.0, 0.0], 0.0, 1, dict(kind="power", slope=0.5),
         notes="f = h(x1-x2); optimal segment x1-x2=1 transversal to the axes"))
add(inst("lineaxis2", "b:p=1", [(-2.0, 2.2), (-1.9, 2.1)],
         h(0.5, V(1)) + " + " + z(0.375, V(2)), [1.0, 0.3], 0.0, 1,
         dict(kind="power", slope=0.5),
         notes="f = h(x1) + z(x2) with z == 0; optimal segment x1=1 aligned with an axis"))
add(inst("ring2", "b:p=1", [(-1.7, 1.9), (-1.8, 1.6)],
         "(<x1>^2 + <x2>^2 - 1)^2", [1.0, 0.0], 0.0, 1, dict(kind="power", slope=0.5),
         notes="unit circle of minimizers; SCIP expands the square"))
add(inst("mccaxis2", "b:p=1 McCormick", [(0.0, 1.0), (0.0, 1.0)],
         f"2*abs(<x1> - {A3}) - (<x1> - {A3})*(<x2> - {B2})",
         [float(A3), 0.5], 0.0, 1, dict(kind="rule-dependent", slope=None),
         notes="scout 3.7: optimal segment x1=a aligned; McCormick exact on x1=a",
         # default checkvarlocks='t' turns x2 into a binary (f is linear in x2)
         params={"constraints/nonlinear/checkvarlocks": "d"}))
add(inst("mccdiag2", "b:p=1 McCormick", [(0.0, 1.0), (0.0, 1.0)],
         f"2*abs(<x1> - <x2> - {A3}) - (<x1> - <x2> - {A3})*(<x2> - {B2})",
         [float(A3) + 0.25, 0.25], 0.0, 1, dict(kind="power", slope=0.5),
         notes="optimal segment x1-x2=a transversal; any McCormick tree needs >= c eps^-1/2"))

# ---- (c) two-dimensional optimal sets ------------------------------------
add(inst("sphere3", "c:p=2", [(0.2, 1.3), (-0.6, 0.5), (-0.55, 0.45)],
         "(<x1>^2 + <x2>^2 + <x3>^2 - 1)^2", [1.0, 0.0, 0.0], 0.0, 2,
         dict(kind="power", slope=1.0), notes="unit sphere of minimizers"))
add(inst("plane3", "c:p=2", [(0.2, 1.4), (-0.5, 0.6), (-0.4, 0.7)],
         h(0.5, "<x1> + <x2> - <x3>"), [1.0, 0.0, 0.0], 0.0, 2,
         dict(kind="power", slope=1.0), notes="f = h(x1+x2-x3); optimal plane"))

# ---- (d) flat quartic directions ------------------------------------------
add(inst("qflat1", "d:quartic", [(-1.9, 2.1)], g4(0.375, V(1)), [0.0], 0.0, 0,
         dict(kind="power", slope=0.25), notes="f = 2 x^4 written as g4; q=(4)"))
add(inst("qflat2a", "d:quartic", [(-2.0, 2.2), (-1.9, 2.1)],
         h(0.5, V(1)) + " + " + g4(0.375, V(2)), [1.0, 0.0], 0.0, 0,
         dict(kind="power", slope=0.25), notes="q=(2,4): exponent 1-1/2-1/4"))
add(inst("qflat2b", "d:quartic", [(-2.0, 2.2), (-1.9, 2.1)],
         g4(0.375, V(1)) + " + " + g4(0.5, V(2)), [0.0, 0.0], 0.0, 0,
         dict(kind="power", slope=0.5), notes="q=(4,4): exponent 1-1/4-1/4"))
add(inst("qflat3", "d:quartic", [(-2.0, 2.2), (-1.9, 2.1), (-2.1, 2.0)],
         h(0.5, V(1)) + " + " + g4(0.375, V(2)) + " + " + g4(0.5, V(3)),
         [1.0, 0.0, 0.0], 0.0, 0, dict(kind="power", slope=0.5),
         notes="q=(2,4,4): exponent 3/2-1/2-1/4-1/4"))

# ---- (e) constrained: optimal set on a curved constraint ------------------
add(inst("condisk2", "e:constrained p=1", [(-1.2, 1.3), (-1.1, 1.25)],
         "-<x1>^2 - <x2>^2", [1.0, 0.0], -1.0, 1, dict(kind="power", slope=0.5),
         cons=[("disk", "<x1>^2 + <x2>^2 <= 1")],
         notes="concave objective, circle of minimizers; shares x_i^2 with the constraint"))
add(inst("condisk2soc", "e:constrained p=1", [(-1.2, 1.3), (-1.1, 1.25)],
         "-<x1>^2 - <x2>^2", [1.0, 0.0], -1.0, 1, dict(kind="power", slope=0.5),
         cons=[("disk", "(<x1>^2 + <x2>^2)^0.5 <= 1")],
         notes="same set, constraint written as a norm"))
# log(x2) >= x1 on {x2 >= exp(x1)}: f = log(x2) - x1 >= 0 with equality on the
# whole curve x2 = exp(x1), which lies on the (convex, active) constraint.
# Only log is nonconvex (secant gap in x2), and nothing is shared with exp.
add(inst("conexp2", "e:constrained p=1", [(-1.0, 1.2), (0.3, 3.5)],
         "log(<x2>) - <x1>", [0.0, 1.0], 0.0, 1, dict(kind="power", slope=0.5),
         cons=[("curve", "exp(<x1>) - <x2> <= 0")],
         notes="optimal curve x2=exp(x1) on an active curved constraint; gap only in x2"))
add(inst("conexp4", "e:constrained p=2", [(-1.0, 1.2), (-0.9, 1.1), (0.3, 3.5), (0.35, 3.2)],
         "log(<x3>) + log(<x4>) - <x1> - <x2>", [0.0, 0.0, 1.0, 1.0], 0.0, 2,
         dict(kind="power", slope=1.0),
         cons=[("curve1", "exp(<x1>) - <x3> <= 0"), ("curve2", "exp(<x2>) - <x4> <= 0")],
         notes="product of two conexp2 curves: 2-dim optimal set on active constraints"))


# ---------------------------------------------------------------------------
def cip_text(d):
    n = d["n"]
    lines = ["STATISTICS", f"  Problem name     : {d['name']}",
             f"  Variables        : {n + 1} (0 binary, 0 integer, 0 implicit integer, {n + 1} continuous)",
             f"  Constraints      : {1 + len(d['cons'])} initial, {1 + len(d['cons'])} maximal",
             "OBJECTIVE", "  Sense            : minimize", "VARIABLES"]
    for i, (lb, ub) in enumerate(d["bounds"]):
        lines.append(f"  [continuous] <x{i + 1}>: obj=0, original bounds=[{lb:.17g},{ub:.17g}]")
    lines.append("  [continuous] <t>: obj=1, original bounds=[-1000,1000]")
    lines.append("CONSTRAINTS")
    lines.append(f"  [nonlinear] <fobj>: {d['obj']} - <t> <= 0;")
    for cname, ctext in d["cons"]:
        lines.append(f"  [nonlinear] <{cname}>: {ctext};")
    lines.append("END")
    return "\n".join(lines) + "\n"


def _py(expr):
    s = re.sub(r"<x(\d+)>", r"X[\1]", expr).replace("^", "**")
    return s.replace("abs(", "mp.fabs(").replace("log(", "mp.log(").replace("exp(", "mp.exp(")


def f_eval(d, x, exact=True):
    """Objective at x (list of floats); 40-digit arithmetic if exact."""
    conv = mp.mpf if exact else float
    X = {i + 1: conv(v) for i, v in enumerate(x)}
    return eval(_py(d["obj"]), {"mp": mp if exact else _FloatMp, "X": X})


class _FloatMp:
    import math
    fabs = staticmethod(abs)
    log = staticmethod(math.log)
    exp = staticmethod(math.exp)


def cons_violation(d, x, exact=True):
    conv = mp.mpf if exact else float
    X = {i + 1: conv(v) for i, v in enumerate(x)}
    worst = conv(0)
    for _, c in d["cons"]:
        lhs, rhs = c.split("<=")
        v = eval(_py(lhs), {"mp": mp if exact else _FloatMp, "X": X}) - conv(rhs)
        worst = max(worst, v)
    for i, (lb, ub) in enumerate(d["bounds"]):
        worst = max(worst, conv(lb) - X[i + 1], X[i + 1] - conv(ub))
    return worst


def np_func(expr):
    import numpy as np
    return eval("lambda X: " + re.sub(r"<x(\d+)>", r"X[\1-1]", expr).replace("^", "**")
                .replace("abs(", "np.abs(").replace("log(", "np.log(").replace("exp(", "np.exp("),
                {"np": np})


if __name__ == "__main__":
    # sanity: f(x*) == f*, x* feasible, and a grid finds nothing below f*
    import numpy as np
    for name, d in INSTANCES.items():
        fx = f_eval(d, d["xstar"])
        viol = cons_violation(d, d["xstar"])
        k = {1: 200001, 2: 2001, 3: 201, 4: 61}[d["n"]]
        X = np.meshgrid(*[np.linspace(lb, ub, k) for lb, ub in d["bounds"]], indexing="ij")
        F = np_func(d["obj"])(X)
        ok = np.ones_like(F, dtype=bool)
        for _, c in d["cons"]:
            lhs, rhs = c.split("<=")
            ok &= np_func(lhs)(X) <= float(rhs)
        best = F[ok].min()
        print(f"{name:12s} n={d['n']} p={d['p']} f(x*)-f*={float(fx - d['fstar']):+.2e} "
              f"viol={float(viol):.1e} grid_min-f*={best - d['fstar']:+.3e} (grid {k}^{d['n']})")
