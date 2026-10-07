"""Cross-check of the 'bad' one-clique assignment with a second solver (SCS) and the dual-side check that
the 'bad' relaxation value is below 0 with the box-moment bounds |y_alpha| <= 1 added (Waki et al. Sec. 5.6 style)."""
import cvxpy as cp
import importlib.util
spec = importlib.util.spec_from_file_location("v", "c4_sdp_variants.py")
src = open("c4_sdp_variants.py").read().split("\nfor n in (5, 8):")[0]
ns = {}; exec(src, ns)
import types
# re-solve with SCS
def solve_with(n, variant, solver, extra_bounds=False):
    orig = cp.Problem.solve
    def patched(self, *a, **k):
        if extra_bounds:
            vs = [v for v in self.variables() if v.ndim == 0]
            self = cp.Problem(self.objective, self.constraints + [cp.abs(v) <= 1 for v in vs])
        k["solver"] = solver
        if solver == "SCS":
            k["eps"] = 1e-9; k["max_iters"] = 200000
        r = orig(self, *a, **k)
        patched.val = self.value
        return r
    cp.Problem.solve = patched
    try:
        ns["solve"](n, variant)
    finally:
        cp.Problem.solve = orig
    return patched.val
for n in (5,):
    print(f"n={n} bad, SCS: {solve_with(n, 'bad', 'SCS'):+.4e}")
    print(f"n={n} bad, Clarabel, with |y_alpha| <= 1 added: {solve_with(n, 'bad', 'CLARABEL', True):+.4e}")
    print(f"n={n} univar, Clarabel, with |y_alpha| <= 1 added: {solve_with(n, 'univar', 'CLARABEL', True):+.4e}")
