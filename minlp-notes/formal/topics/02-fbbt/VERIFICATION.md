Completed locally on 2026-09-11 20:15:23 UTC.

| Check | Result |
|---|---|
| Import coverage | PASS: all 40 project modules imported, including 8 FBBT modules |
| Full project build with `--wfail` | PASS: no errors or warnings |
| Full project axiom audit | PASS: 12,393 declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Kernel replay | PASS: every `Formal.FBBT` module |
| Previously completed switching package | Source fingerprints unchanged; its recorded kernel replay remains applicable |
| Independent specification review | PASS: exact hulls, original unit-box runs, comparison direction, arbitrary schedules, fair singleton limit, syntax and dependency graph |

The [run log](verification/run.log) records the checks. This stage replayed the
new FBBT modules; the already completed switching modules were unchanged.
The full project was rebuilt and audited together. Run `bash scripts/verify.sh`
from `formal/` for a complete replay of all packages, or the following commands
for this stage's scope:

```bash
python3 scripts/check_imports.py
lake build --wfail
lake env lean Verify.lean
LEAN_NUM_THREADS=1 lake env leanchecker -v Formal.FBBT
```

The main theorem is `FBBT.doubly_exponential_fbbt`. Its only run assumption is
that each update is an actual primitive interval hull of one defining equality.
Fairness is needed for the limiting value, and not for the finite-prefix lower
bound. `originalRun_isRun` and `canonical_slow_run` establish existence of actual
runs and a fair example. `PrimitiveRun.singleton_limit` proves convergence of
both endpoint vectors from the original unit box.

The [coverage record](COVERAGE.md) states the precise scope. In particular,
serialized encoding length and the companion PosSLP-hardness result are not
claimed as formalized. The residual result uses exact upstream initialization.

Source and dependency fingerprints are in [SHA256SUMS](verification/SHA256SUMS).
Run `sha256sum -c topics/02-fbbt/verification/SHA256SUMS` from `formal/`.
The shared pinned environment is Lean 4.33.1 and Mathlib v4.33.1. No custom axioms,
unfinished proofs, native-computation axioms, or external solver results are
used. Kernel replay uses the installed Lean kernel and its imported Mathlib
base, not a separately implemented proof assistant. No publication or push was
performed.
