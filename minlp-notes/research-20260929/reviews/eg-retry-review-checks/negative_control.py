"""Negative control for indep_cert: the certifier must NOT certify a target above the optimum.

For each instance: boxes of several sizes around the retry primal point x* (integers fixed),
target theta = F(x*) + delta with delta in {1e-6, 1e-9}: the box contains x*, which is
feasible with F(x*) < theta, so certification must fail.  Also the leaves of a recorded tree
that contain x* must fail for theta = UB + 1e-9.  With theta = claimed bound - 1e-6 the same
boxes should certify (positive control).

    python3 negative_control.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from indep_cert import Certifier  # noqa: E402

PTS = {"eg_int_s": ([0.564219345763436, 0.6468471890552644, 1.0, 0.9390699678023392, 2, 4, 3], "6.4531031593842274",
                    "6.4531031529331155"),
       "eg_disc_s": ([3, 10, 8, 12, 1.0800209145804143, 3.485358811359775, 2.2415838244871797], "5.7605396164535106",
                     "5.760539610694994"),
       "eg_disc2_s": ([0.339986187975027, 1.0, 0.7526242429543005, 1.2370734367691458, 11, 34, 24], "5.6421005799711068",
                      "5.642100574331458")}


def main():
    for name, (x, F, lbc) in PTS.items():
        x = np.array(x, float)
        for delta in ("1e-6", "1e-9"):
            from fractions import Fraction as Fr
            th = Fr(F) + Fr(delta)
            C = Certifier(name, th, max_depth=12)
            M = C.M
            los, his = [], []
            for rel in (1e-2, 1e-4, 1e-6, 1e-8):
                half = rel * (M.ub - M.lb)
                lo = np.where(M.isint, x, np.maximum(x - half, M.lb)); hi = np.where(M.isint, x, np.minimum(x + half, M.ub))
                los.append(lo); his.append(hi)
            ok = C.certify_batch(np.array(los), np.array(his))
            print(f"{name}: theta = F(x*) + {delta}: certified {ok.tolist()} (must be all False); stats {C.stats}")
        C = Certifier(name, Fr(lbc) - Fr("1e-6"), max_depth=12)
        ok = C.certify_batch(np.array(los), np.array(his))
        print(f"{name}: theta = claimed bound - 1e-6: certified {ok.tolist()} (positive control)")


if __name__ == "__main__":
    main()
