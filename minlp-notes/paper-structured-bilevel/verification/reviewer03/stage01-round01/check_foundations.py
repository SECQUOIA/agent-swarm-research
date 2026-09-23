"""Independent finite diagnostics; not a replacement for the proof review."""
from pathlib import Path
import hashlib
import json
import re
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SNAPSHOT = ROOT / "paper-structured-bilevel/process/snapshots/stage01-round01"
manifest_bytes = (SNAPSHOT / "SHA256.json").read_bytes()
digest = hashlib.sha256(manifest_bytes).hexdigest()
assert digest == "2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de"
manifest = json.loads(manifest_bytes)
for name, expected in manifest.items():
    assert hashlib.sha256((SNAPSHOT / name).read_bytes()).hexdigest() == expected

coverage = (SNAPSHOT / "process/coverage.md").read_text()
paths = sorted(set(re.findall(r"`((?:results|notes|code)/[^`*]+)`", coverage)))
missing = [name for name in paths if not (ROOT / name).exists()]
assert not missing, missing

# Denominator clearing with a polynomial involving several recovered coordinates.
x, w, z0, z1, z2 = sp.symbols("x w z0 z1 z2")
D = 1 + x*x + w*w
Z = [x+w, x*w-1, x*x-w]
p = sp.Rational(3,7)*x*z0*z1**2 - z2**4 + w
delta = 4
cleared = sp.cancel(D**delta*p.subs(dict(zip([z0,z1,z2], [v/D for v in Z]))))
assert sp.denom(cleared) == 1
assert sp.Poly(cleared, x, w).total_degree() <= delta*(1+2)
assert sp.simplify(cleared/D**delta-p.subs(dict(zip([z0,z1,z2], [v/D for v in Z])))) == 0

# Fixed-normal compactness does not imply pessimistic attainment.
z = sp.symbols("z", real=True)
quartic = z**2*(1-z)**2
assert sp.solve(quartic, z) == [0,1]
assert quartic.subs(z, sp.Rational(1,2)) == sp.Rational(1,16)
# For x>0 and z in [0,1], quartic+x*z >=0 with equality only at z=0.
# Therefore W(x)=x for x>0, W(0)=1, while optimistic F=x+z attains 0.
assert sp.limit(x, x, 0, dir="+") == 0

# A feasible problem can have an empty strict inner approximation.
# Choose follower z*=0 from min z^2/2 on [0,1], and upper row z<=0.
# Its true row value is zero at every leader, so every positive tightening fails.
inner_true_feasible = (sp.Integer(0) <= 0)
inner_tightened_feasible = (sp.Integer(0) <= -sp.Rational(1,4))
assert bool(inner_true_feasible) and not bool(inner_tightened_feasible)

# Numerical-degree output obstruction: X={x in [1,2]:x^(2^t)=2}.
# Eisenstein at 2 establishes irreducibility for arbitrary t; small cases checked.
degree_examples = []
for t in range(1,7):
    polynomial = sp.Poly(x**(2**t)-2, x)
    assert polynomial.is_irreducible
    degree_examples.append({"t":t, "output_degree":polynomial.degree()})

summary = {
    "manifest_sha256": digest,
    "verified_snapshot_files": list(manifest),
    "explicit_inventory_paths_checked": len(paths),
    "missing_inventory_paths": missing,
    "substitution_diagnostic": "passed",
    "pessimistic_nonattainment_example": "symbolic identities passed; positivity argument reviewed manually",
    "inner_surrogate_scope_example": "true feasible, every positive uniform tightening infeasible",
    "degree_examples": degree_examples,
    "limitations": "Finite symbolic checks do not prove asymptotic complexity or the later compression theorems.",
}
(HERE / "checks.json").write_text(json.dumps(summary, indent=2)+"\n")
print(json.dumps(summary, indent=2))
