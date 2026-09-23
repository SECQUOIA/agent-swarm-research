"""Original and binarized models must agree on small instances (Gurobi and SCIP)."""
import pytest

from sob.backends import SOLVERS
from sob.instances import FAMILIES
from sob.model import binarized_ir, original_ir

CASES = [("jeroslow", 9, 1, 0), ("cknap", 8, 1, 3), ("cknap", 8, 2, 4), ("power", 8, 2, 5),
         ("sigmoid", 6, 1, 6), ("sigmoid", 6, 2, 7), ("quartic", 4, 1, 8)]


@pytest.mark.parametrize("solver", ["gurobi", "scip"])
@pytest.mark.parametrize("family,n,m,seed", CASES)
def test_same_optimum(family, n, m, seed, solver):
    p = FAMILIES[family](n, m, seed)
    res = {}
    for form, ir in (("orig", original_ir(p)), ("sob", binarized_ir(p))):
        r = SOLVERS[solver](ir, 120, threads=2, gap=1e-6)
        assert r["status"] in ("optimal", "gaplimit"), (form, r["status"])
        true = sum(f(r["x"][f"x{i}"]) for i, f in enumerate(p.funcs))
        assert abs(true - r["primal"]) <= 1e-5 * max(1, abs(true))
        res[form] = r["primal"]
    assert abs(res["orig"] - res["sob"]) <= 2e-5 * max(1, abs(res["orig"]))
