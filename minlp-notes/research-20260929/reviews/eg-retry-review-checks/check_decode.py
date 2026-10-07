"""Review check: the retry's decoding (eg_model.py / egdata.py, from OSIL via osilx) against an
independent reading of the MINLPLib GAMS files (gms_model.py).

1. Exact comparison (Fractions) of every row's term multiset {(a, mu vector, gamma vector)},
   the scales, the linear terms, the constants c_k, the side-row bounds glo/ghi, the variable
   bounds and the integrality flags.
2. The regex-extracted term data reproduce the direct evaluation of the GAMS expression text
   at random points (50 digits).
3. egdata's float evaluator agrees with the GAMS expression text at random points.

    python3 check_decode.py
"""
import os
import random
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RETRY = os.path.join(HERE, "..", "..", "open-instances-wave3", "eg", "retry")
sys.path.insert(0, RETRY)
sys.path.insert(0, HERE)
import egdata  # noqa: E402
from gms_model import GmsModel, eval_terms  # noqa: E402


def main():
    rng = random.Random(1)
    for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s"):
        G = GmsModel(name)
        T = G.terms()
        D = egdata.Data(name)
        dv = [v for v in G.vars if v != "objvar"]
        assert D.M["names"] == dv, (D.M["names"], dv)
        # bounds and integrality
        assert [G.lb[v] for v in dv] == D.qlb and [G.ub[v] for v in dv] == D.qub
        assert [v in G.ints for v in dv] == list(D.isint)
        # rows
        nmis = 0
        for k, t in enumerate(T):
            obj = t["objc"] == 1
            assert obj == bool(D.objrows[k])
            if obj:
                assert t["sense"] == "=G=" and D.qc[k] == t["rhs"]
            else:
                # -(S) >= rhs  <=>  S <= -rhs ;  -(S) <= rhs  <=>  S >= -rhs
                if t["sense"] == "=G=":
                    assert D.qghi[k] == -t["rhs"] and D.qglo[k] is None
                else:
                    assert t["sense"] == "=L=" and D.qglo[k] == -t["rhs"] and D.qghi[k] is None
            lin = [t["lin"].get(v, Fr(0)) for v in dv]
            assert lin == D.qlin[k], (k, lin, D.qlin[k])
            gset = sorted((a, tuple(fac[v][1] for v in dv), tuple(fac[v][2] for v in dv)) for a, fac in t["terms"])
            dset = sorted((D.qa[k][m], tuple(D.qmu[k][m]), tuple(D.qga[k])) for m in range(D.Mt))
            nmis += gset != dset
            for a, fac in t["terms"]:
                assert [fac[v][0] for v in dv] == D.qs
        print(f"{name}: rows {len(T)}, terms/row {D.Mt}; exact data mismatches vs egdata: {nmis}")
        # extracted data vs direct evaluation, and egdata float evaluator vs GAMS text
        worst_x, worst_f = 0.0, 0.0
        for _ in range(12):
            pt = {}
            for v in dv:
                lo, hi = float(G.lb[v]), float(G.ub[v])
                pt[v] = Fr(rng.randint(int(lo), int(hi))) if v in G.ints else Fr(rng.uniform(lo, hi))
            pt["objvar"] = Fr(rng.uniform(-5, 10))
            x = np.array([float(pt[v]) for v in dv])
            gf, _ = D.g(x[None])
            for k, t in enumerate(T):
                with mp.workdps(50):
                    vd = G.lhs(k, pt)
                    ve = eval_terms(t, pt)
                    S = -(vd - t["objc"] * mp.mpf(float(pt["objvar"])))       # = g_k
                    worst_x = max(worst_x, float(abs(vd - ve)))
                    scale = float(sum(abs(mp.mpf(float(a))) for a, _ in t["terms"])) + 1
                    worst_f = max(worst_f, abs(float(S) - gf[0, k]) / scale)
        print(f"  max |direct - extracted| = {worst_x:.2e}; max |egdata float g - GAMS g| / (sum|a|+1) = {worst_f:.2e}")


if __name__ == "__main__":
    main()
