"""Structure check (run in /tmp/egdossier/ic with the reviewer's certifier copied there):
shared centres, gamma ranges, constants, sum|a| per row, e27 = e28, linear terms."""
import numpy as np, indep_cert as IC
M = IC.Model('eg_int_s')
cent = [set(map(tuple, np.round(-M.MU[k], 6))) for k in range(28)]
print("rows:", M.R, "terms per row:", M.Mt, "dims:", M.d)
print("same 97 centres in all 28 rows:", all(c == cent[0] for c in cent), "; distinct centres in row 1:", len(cent[0]))
print("gamma ranges per coordinate (min..max over rows):", [(round(float(M.GA[:, i].min()), 4), round(float(M.GA[:, i].max()), 4)) for i in range(7)])
print("objective-row constants c_k range:", float(min(M.c)), float(max(M.c)))
sa = np.abs(M.A).sum(1)
print("sum|a| objective rows: min %.1f max %.1f; side rows e25..e28:" % (sa[:24].min(), sa[:24].max()), np.round(sa[24:], 1).tolist())
print("rows e27, e28 identical data:", np.array_equal(M.A[26], M.A[27]) and np.array_equal(M.MU[26], M.MU[27]) and np.array_equal(M.GA[26], M.GA[27]))
print("linear terms (nonzero):", [(k + 1, [(i, float(v)) for i, v in enumerate(M.LIN[k]) if v != 0]) for k in range(28) if np.any(M.LIN[k] != 0)])
