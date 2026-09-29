"""Sanity checks of dcheck.py on functions with known discrete-convexity status."""
import numpy as np
from dcheck import *

def tab(fun, n, lo=-2, hi=2):
    return {p: float(fun(np.array(p))) for p in box(lo, hi, n)}

cases = {
    "|2x1-x2| (convex-ext, not IC)": (lambda x: abs(2*x[0]-x[1]), 2),
    "DD mixed-sign quadratic (DDM, IC, not Lnat)": (lambda x: x @ np.array([[2,1,-1],[1,2,1],[-1,1,3]]) @ x, 3),
    "non-DD PSD quadratic (not DDM; n=3 IC?)": (lambda x: x @ np.array([[2,1,1],[1,2,1],[1,1,2]]) @ x * 0 + (x.sum())**2 + 0.1*(x@x), 3),
    "max(x) (Lnat)": (lambda x: max(x), 3),
    "(x1-x2)^2 (Lnat, not Mnat)": (lambda x: (x[0]-x[1])**2, 2),
    "(x1+x2)^2+(x1+x2+x3)^2 laminar (Mnat)": (lambda x: (x[0]+x[1])**2 + x.sum()**2, 3),
}
for name, (fun, n) in cases.items():
    f = tab(fun, n)
    print(f"{name:48s} DDM:{len(ddm_violations(f)):5d} Lnat:{len(lnat_violations(f)):5d} "
          f"Mnat:{len(mnat_violations(f)):5d} IC:{len(ic_violations(f)):5d} falseLocMin:{len(ninf_false_local_minima(f))}")
