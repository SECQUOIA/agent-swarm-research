"""Handler modes must reproduce SCIP's optimum on small separable instances."""
import json
import subprocess
import sys

import pytest

CASES = [("quartic", 5, 1), ("quartic", 6, 2), ("sigmoid", 6, 1), ("power", 5, 2)]


def solve(family, n, m, mode):
    out = subprocess.run([sys.executable, "run_quartic.py", family, str(n), str(m), "3", mode, "--tl", "120"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads([l for l in out.split("\n") if l.startswith("{")][-1])


@pytest.mark.parametrize("family,n,m", CASES)
def test_modes_agree(family, n, m):
    ref = solve(family, n, m, "native")
    assert ref["status"] in ("optimal", "gaplimit")
    for mode in ("hybrid", "uenv"):
        if mode == "uenv" and family == "power":
            continue      # standalone mode is documented as unsuitable for single-operator concave terms
        r = solve(family, n, m, mode)
        assert r["status"] in ("optimal", "gaplimit"), (mode, r["status"])
        assert abs(r["true_obj"] - ref["true_obj"]) <= 3e-4 * max(1.0, abs(ref["true_obj"])), (mode, r, ref)
        assert r["dual"] <= ref["true_obj"] + 1e-6 * max(1.0, abs(ref["true_obj"]))
