"""Negative controls for rev_chain_exact.py (reviewer's own code), chain50 only.

Each case alters the generator data in memory and reruns the exact check.
Expected: the unaltered data passes; altered data fails, except the root
swap (t_a <-> t_b), which by symmetry of the two conditions (w_a = w_b = 2)
gives another exactly feasible point with a different objective.
"""
import copy
import io
import json
import contextlib

import rev_chain_exact as R

N = 50
orig_load = json.load
gen0 = orig_load(open("%s/points/chain%d_generator.json" % (R.TRACK, N)))
box0 = orig_load(open("%s/points/chain%d_box.json" % (R.TRACK, N)))


def run_with(gen, box, perturb=None):
    def fake_load(fh):
        name = fh.name
        if name.endswith("_generator.json"):
            return copy.deepcopy(gen)
        if name.endswith("_box.json"):
            return copy.deepcopy(box)
        return orig_load(fh)
    R.json.load = fake_load
    try:
        out = []
        with contextlib.redirect_stdout(io.StringIO()):
            R.run(N, out, perturb)
        return "PASS", out[0]
    except AssertionError as e:
        import traceback
        fr = traceback.extract_tb(e.__traceback__)[-1]
        return "FAIL (assert %s at line %d: %s)" % (e.args[0] if e.args else "", fr.lineno, fr.line), None
    except Exception as e:
        return "FAIL (%s: %s)" % (type(e).__name__, e), None
    finally:
        R.json.load = orig_load


print("unaltered:", run_with(gen0, box0)[0])

g = copy.deepcopy(gen0)
from fractions import Fraction as Q
t5 = Q(g["t"][5]) + Q(1, 10 ** 20)
g["t"][5] = R.fmt_int(int(t5 * 10 ** 20), 20)
print("t_5 + 1e-20 (generator re-solves the free pair, so rows still hold; box check must fail):", run_with(g, box0)[0])

g = copy.deepcopy(gen0)
g["root_a"] = "larger"
st, res = run_with(g, box0)
print("root swap (box check expected to fail since the point moves):", st)

# root swap without the box check: feasibility only
g = copy.deepcopy(gen0)
g["root_a"] = "larger"
box_sw = copy.deepcopy(box0)
box_sw["radius"] = "1e3"          # make the box trivially contain any point
box_sw["objective_enclosure"] = ["-1e9", "1e9"]
box_sw["objective_enclosure_decimal"] = ["-1e9", "1e9"]
st, res = run_with(g, box_sw)
print("root swap, box check disabled:", st, "objective in", res and [res["obj_lo_40"][:22], res["obj_hi_40"][:22]])

b = copy.deepcopy(box0)
c = R.Q(b["variables"][7]["centre"]) + R.Q(3, 10 ** 40)
b["variables"][7]["centre"] = str(c.numerator / c.denominator) if False else "%s" % (R.fmt_int(int(c * 10 ** 45), 45))
print("box centre x8 moved by 3e-40:", run_with(gen0, b)[0])

b = copy.deepcopy(box0)
b["objective_enclosure_decimal"] = ["5.0722614939828723164454381769845467731844", "5.0722614939828723164454381769845467731845"]
st, res = run_with(gen0, b)
print("objective decimal shifted up by 1e-40:", st, res and res["track_obj_decimal_valid"])


def bump(j, eps):
    def f(X, F):
        X[j] = F.add(X[j], F.c(eps))
    return f


print("x_5 + 1e-30 (rows must fail):", run_with(gen0, box0, bump(5, Q(1, 10 ** 30)))[0])
print("u_5 + 1e-30 (sqrt lookup must fail):", run_with(gen0, box0, bump(N + 1 + 5, Q(1, 10 ** 30)))[0])
print("x_N + 1e-30 (bound x_N = 3 must fail):", run_with(gen0, box0, bump(N, Q(1, 10 ** 30)))[0])
