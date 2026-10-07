"""Review check of the structural statements in retry.md Section 2 (float data from egdata,
exact data compared as Fractions)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "open-instances-wave3", "eg", "retry"))
import egdata

Ds = {n: egdata.Data(n) for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s", "eg_all_s")}
D0 = Ds["eg_int_s"]
for n, D in Ds.items():
    same = all(D.qa[k] == D0.qa[k] and D.qmu[k] == D0.qmu[k] and D.qga[k] == D0.qga[k] and D.qlin[k] == [l * s / s0 for l, s0, s in zip(D0.qlin[k], D0.qs, D.qs)]
               and D.qc[k] == D0.qc[k] and D.qglo[k] == D0.qglo[k] and D.qghi[k] == D0.qghi[k] for k in range(28))
    y_lb = [lb * s for lb, s in zip(D.qlb, D.qs)]; y_ub = [ub * s for ub, s in zip(D.qub, D.qs)]
    print(n, "scales", [str(s) for s in D.qs], "isint", D.isint.astype(int).tolist(),
          "same data as eg_int_s in y:", same, "y box", [(float(a), float(b)) for a, b in zip(y_lb, y_ub)])
D = D0
print("e27 == e28 terms:", D.qa[26] == D.qa[27] and D.qmu[26] == D.qmu[27] and D.qga[26] == D.qga[27] and D.qlin[26] == D.qlin[27])
print("sum|a| e27 %.1f, max|a| %.1f" % (np.abs(D.a[26]).sum(), np.abs(D.a[26]).max()))
print("side bounds glo", [None if v is None else float(v) for v in D.qglo[24:]], "ghi", [None if v is None else float(v) for v in D.qghi[24:]])
print("lin rows", {k: [float(v) for v in D.qlin[k]] for k in range(28) if any(D.qlin[k])})
x = np.array([0.564219345763436, 0.6468471890552644, 1.0, 0.9390699678023392, 2, 4, 3.0])
t = D.mu + D.s * x
W = D.a * np.exp((D.ga[:, None, :] * t * t).sum(-1))
g, _ = D.g(x[None])
print("e12: sum|w| %.2f  g %.3f ; e26: sum|w| %.2f  gauss part %.4f" % (np.abs(W[11]).sum(), g[0, 11], np.abs(W[25]).sum(), W[25].sum()))
f, viol, gg = D.F(x[None])
print("F at retry point %.12f; obj rows within 1e-6 of max:" % f[0], [k + 1 for k in range(24) if D.c[k] + gg[0, k] > f[0] - 1e-6])
print("max |gamma|", np.abs(D.ga).max())
