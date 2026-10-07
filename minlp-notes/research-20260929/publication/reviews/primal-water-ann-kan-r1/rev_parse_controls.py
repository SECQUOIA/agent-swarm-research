"""Parser validation and negative controls (reviewer's code).

1. Parser validation: evaluate the MINLPLib-listed points (open-instances-wave3/sol/*.p*.sol,
   sparse: absent = 0) with the reviewer's reader and interval arithmetic; a mis-read
   coefficient would show as a large violation.
2. Negative controls: the checkers must reject corrupted points.
usage: python3 rev_parse_controls.py
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import contextlib
import copy
import io
import json
from fractions import Fraction as Fr

import rev_nn
import rev_water
import rosil
from rint import V

W3 = _REPRO_ROOT + "/research-20260929/open-instances-wave3"


def read_sol(path):
    d = {}
    for line in open(path):
        p = line.split()
        if len(p) == 2:
            d[p[0]] = p[1]
    return d


def max_viol(M, X):
    worst, wn = Fr(0), None
    for c in M["cons"]:
        b = rosil.eval_body(c, X, V)
        v = max(Fr(0), (c["lb"] - b.lo) if c["lb"] is not None else 0, (b.hi - c["ub"]) if c["ub"] is not None else 0)
        if v > worst:
            worst, wn = v, c["name"]
    bv = Fr(0)
    for j in range(M["n"]):
        if M["lb"][j] is not None:
            bv = max(bv, M["lb"][j] - X[j].lo)
        if M["ub"][j] is not None:
            bv = max(bv, X[j].hi - M["ub"][j])
    return worst, wn, bv


def parse_validation():
    for name, f in (("ann_cumene_tanh", "ann_cumene_tanh.p1.sol"), ("kan_r5_h1_n3", "kan_r5_h1_n3.p2.sol"),
                    ("kan_r5_h1_n5", "kan_r5_h1_n5.p2.sol"), ("kan_r5_h1_n8", "kan_r5_h1_n8.p3.sol")):
        M = rosil.load(name)
        s = read_sol(f"{W3}/sol/{f}")
        extra = set(s) - set(M["names"])
        X = [V.num(Fr(s.get(nm, "0"))) for nm in M["names"]]
        w, wn, bv = max_viol(M, X)
        o = rosil.eval_body(dict(const=M["obj"]["const"], lin=M["obj"]["lin"], quad=M["obj"]["quad"],
                                 nl=M["obj"]["nl"]), X, V)
        print(f"parse check {name} at listed {f}: max row violation {float(w):.2e} ({wn}), "
              f"max bound violation {float(bv):.2e}, objective {float(o.lo):.10g}; non-model entries {sorted(extra)}")


def expect_fail(label, fn):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
    except AssertionError as e:
        last = [l for l in buf.getvalue().splitlines() if l.strip()][-1:] or [""]
        print(f"negative control '{label}': rejected as expected ({str(e)[:80] or 'assertion'}); "
              f"last checker line: {last[0][:230]}")
        return
    print(f"negative control '{label}': NOT rejected  <-- checker too weak")


def controls():
    # waterno2_06: shift one rational coordinate by 1e-30
    orig = json.load(open(f"{rev_water.PTS}/waterno2_06.exact.json"))

    def run_water(mod):
        J = copy.deepcopy(orig)
        mod(J)
        real = json.load
        json.load = lambda fh: J
        try:
            rev_water.main("06")
        finally:
            json.load = real

    def m1(J):
        k = next(k for k, v in J["x"].items() if isinstance(v, str) and k.startswith("x") and Fr(v) != 0)
        J["x"][k] = str(Fr(J["x"][k]) + Fr(1, 10**30))
    expect_fail("waterno2_06: one continuous coordinate + 1e-30", lambda: run_water(m1))

    def m2(J):
        s = J["symbols"]["0"]
        w = Fr(s["hi"]) - Fr(s["lo"])
        s["lo"], s["hi"] = str(Fr(s["hi"]) + w), str(Fr(s["hi"]) + 2 * w)
    expect_fail("waterno2_06: root interval moved off the root", lambda: run_water(m2))

    def m3(J):
        k = next(k for k, v in J["x"].items() if isinstance(v, dict))
        J["x"][k]["c0"] = str(Fr(J["x"][k]["c0"]) + Fr(1, 10**40))
    expect_fail("waterno2_06: field coordinate c0 + 1e-40", lambda: run_water(m3))

    def m4(J):
        k = next(k for k, v in J["x"].items() if k.startswith("b") and v == "1")
        J["x"][k] = "0"
    expect_fail("waterno2_06: one binary flipped 1 -> 0", lambda: run_water(m4))

    # KAN: flip a binary of a one-hot group; keep the partition rows
    origk = json.load(open(f"{rev_nn.PTS}/kan_r5_h1_n3.point.json"))

    def run_kan(mod, keep_partition=False):
        P = copy.deepcopy(origk)
        mod(P)
        real = json.load

        def fake(fh):
            if getattr(fh, "name", "").endswith(".point.json"):
                return P
            return real(fh)
        json.load = fake
        realload = rosil.load
        try:
            if keep_partition:
                # make the partition rows unrecognisable so they are kept and must hold
                def ld(name):
                    M = realload(name)
                    for c in M["cons"]:
                        if c["lb"] == 1 and c["ub"] == 1 and not c["quad"] and c["nl"] is None and \
                                all(a == 1 for a in c["lin"].values()) and not any(M["vtype"][j] == "B" for j in c["lin"]):
                            c["const"] = Fr(0)
                            c["lin"] = {j: Fr(2) * a for j, a in c["lin"].items()}
                            c["lb"] = c["ub"] = Fr(2)
                    return M
                rosil.load = ld
            rev_nn.main("kan_r5_h1_n3")
        finally:
            json.load = real
            rosil.load = realload

    def k1(P):
        ones = [k for k, v in P["x"].items() if k.startswith("b") and v == "1"]
        zeros = [k for k, v in P["x"].items() if k.startswith("b") and v == "0"]
        # flip the first selected binary and the next binary name (same group, neighbour interval)
        b = ones[0]
        nb = "b" + str(int(b[1:]) + 1)
        P["x"][b], P["x"][nb] = "0", "1"
    expect_fail("kan_r5_h1_n3: knot-interval binary moved to the neighbour interval", lambda: run_kan(k1))
    expect_fail("kan_r5_h1_n3: partition rows kept (point must then fail, OSIL model infeasible)",
                lambda: run_kan(lambda P: None, keep_partition=True))

    def k3(P):
        k = next(iter(P["inputs"]))
        P["inputs"][k] = str(Fr(P["inputs"][k]) + Fr(1, 10**20))
    expect_fail("kan_r5_h1_n3: input changed by 1e-20 (must differ from result.json u)", lambda: run_kan(k3))


if __name__ == "__main__":
    parse_validation()
    controls()
