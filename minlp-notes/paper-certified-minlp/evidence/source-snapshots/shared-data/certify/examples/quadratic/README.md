> Portable supplement: this archived README retains original repository-relative commands and notes links for provenance. Start with the top-level `README.md` and run `reproduce.py small` from the extracted supplement root; no external notes folder is required.

# Reproducible quadratic certificate

This bundle certifies a lower bound of **1/4** for

```text
minimize y
subject to (x - 1/2)^2 <= y
           x in {0,1}, 0 <= y <= 2.
```

The exact point `x = 0, y = 1/4` is feasible and has objective `1/4`: its nonlinear constraint holds with equality. Together with the replayed lower bound, this establishes optimum `1/4` for this example. The general certificate checker verifies lower bounds; the feasible-point argument here is a separate exact calculation.

The source `instance.py` is byte-identical to the original producer input `quadratic.py`. Its hash matches the source hash in `lemma.json`. The producer generated these artifacts during the 2026-09-13 repair, using the current working-tree implementation. They are a fresh example, not reclassified historical benchmark results. `validation.json` records the producer summary, source and artifact hashes, package versions, exact witness, and complete replay result. The recorded Git commit has a dirty working tree; the replay source hashes identify the checked implementation more precisely. They do not reconstruct an earlier producer source manifest.

Replay was tested with Python 3.13.11 and five Python packages: Pyomo, NumPy, SymPy, mpmath, and python-flint. Their tested versions are pinned in `requirements.txt`. NumPy is imported through the row-description module even though this replay does not run numerical optimization. No external optimization solver, solver license, or external VIPR checker is needed.

From the repository root, create an environment and install the replay dependencies:

```sh
python3 -m venv /tmp/minlp-quadratic-replay
/tmp/minlp-quadratic-replay/bin/python -m pip install -r code/minlp_solver_lab/certify/examples/quadratic/requirements.txt
```

Then run the complete checker and verify the feasible point with rational arithmetic:

```sh
PYTHONPATH=code/minlp_solver_lab /tmp/minlp-quadratic-replay/bin/python - <<'PY'
import json
from fractions import Fraction
from pathlib import Path
from certify.driver import check_certificate

example = Path("code/minlp_solver_lab/certify/examples/quadratic")
report = check_certificate(
    str(example / "instance.py"), str(example),
    require_vipr=True, verbose=False,
)
print(json.dumps(report, indent=2))
assert report["ok"] and report["status"] == "verified", report
assert Fraction(report["certified_master_lb"]) == Fraction(1, 4)

x, y = Fraction(0), Fraction(1, 4)
assert x in (0, 1) and 0 <= y <= 2
assert (x - Fraction(1, 2))**2 <= y
assert y == Fraction(report["certified_master_lb"])
print("Exact optimum: 1/4")
PY
```

The expected report verifies all 11 nonlinear cuts, reconstructs the identical rational master, matches the VIPR problem to that master, and checks all 39 derivations. Replay reads the saved artifacts without changing them. The complete supported checker contract and trust assumptions are documented in [`notes/certified-minlp-soundness.md`](../../../../../notes/certified-minlp-soundness.md) and [`notes/certified-minlp-vipr-replay.md`](../../../../../notes/certified-minlp-vipr-replay.md).
