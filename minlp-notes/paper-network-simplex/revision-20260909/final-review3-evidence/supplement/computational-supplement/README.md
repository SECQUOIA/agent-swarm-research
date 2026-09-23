# Computational supplement

This supplement accompanies *Sparse convex hulls for network flows coupled to
a simplex*. Run every command below from this directory. Keep `code/` and
`paper-network-simplex/` together: several checks locate inputs relative to their
own source files. The separate LaTeX archive contains the paper.

## Environment

The exact separator interfaces use Python's standard library and `Fraction`.
Numerical optimization, LP comparisons, and some independent checks additionally
use NumPy, SciPy (with bundled HiGHS), and SymPy. The extracted package was tested
with Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0. To create that
dependency environment with an available Python 3.13 interpreter:

```sh
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
sha256sum -c MANIFEST.sha256
```

The manuscript's canonical timings were measured with Python 3.12.14, NumPy
2.5.2, SciPy 1.18.1, and bundled HiGHS 1.12.0, on x86-64 Linux under WSL2 with
36 visible logical CPUs. The host was shared and no affinity or thread
isolation was imposed. The requirements file records the package validation
environment; it does not recreate the historical host or promise identical
timings. Installing dependencies requires access to the corresponding packages.

## Interfaces and evidence

`code/network_simplex/` contains the exact parallel-path graph separator and
flat-chain separator, including regression tests. `code/network_simplex_compressed/`
contains exact rational LP assembly, numerical optimization, and exactly checked
Farkas cuts. `API.md` describes inputs, outputs, and supported scope.
`code/network_simplex_benchmarks/` supplies independent full formulations,
elementary baseline reductions, benchmark inputs, and measurement routines.

Exact accepted decompositions are checked against the original rational flow,
capacity, simplex, and observation constraints. Exact cuts have positive rational
violation and checked validity or nonnegative cancelling multipliers. Numerical
LP feasibility is not an exact membership certificate. In the general compressed
API, `numerically_feasible`, `uncertified_outside`, and `solver_failure` do not
provide an exact certificate. `certified_outside` does.

The unreduced flat-chain comparator is included at
`paper-network-simplex/verification/reference/stage06/flat_chain.py`. The runner
loads it as `network_simplex._stage06_unreduced` so its relative imports resolve.
It is a benchmark comparator, not another production API. Filenames containing
`stage` are retained for import and command compatibility; no development history
is needed to use the supplement.

## Tests and independent checks

The principal suite contains 23 tests:

```sh
PYTHONPATH=code python -m unittest network_simplex.test_separator network_simplex.test_flat_chain network_simplex_benchmarks.test_strong_baselines -v
```

Run the implementation audits:

```sh
python code/network_simplex_review/verify_flat_chain_implementation.py
PYTHONPATH=code python -m network_simplex_compressed.verify
PYTHONPATH=code python -m network_simplex_compressed.integration
```

The flat audit reports exact decompositions and cuts separately from numerical
path-hull comparisons. Its unreduced basis checks apply to the comparator's
normal system; the principal suite checks the reduced recovery bases. The
compressed audit compares both formulations with independently assembled LPs
and exactly checks recovered multipliers. Its global LP support comparisons
are numerical. Integration recovers product ratios 2, 5, and 21 with exact cuts.

The following programs check finite mathematical constructions independently:

```sh
python paper-network-simplex/verification/stage02-exact.py
python paper-network-simplex/verification/stage03-exact.py
python paper-network-simplex/verification/stage04-recovery.py
python paper-network-simplex/verification/stage05-padding.py
python paper-network-simplex/verification/stage05-profile.py
python paper-network-simplex/verification/stage07/integral-hull.py
python checks/independent_math.py
python checks/independent_elimination.py
python checks/fibonacci_facets.py
python checks/repairs_and_threshold.py
PYTHONPATH=code python checks/exact_contracts.py
```

The first six check fixed-arc preprocessing and a K4 example, theta
supports/recovery, bounded-rank recovery, transportation padding, profile
circuits, and integral hull examples.
The profile program also uses numerical LP comparisons. `independent_math.py`
checks rational theta sums/recovery, reduced circuits, and Fibonacci witnesses;
`independent_elimination.py` checks incidence-based cycle minors, elimination,
and completion on specified small graphs. `fibonacci_facets.py` uses an LP only
to find candidate rows, then verifies validity, facet dimension, and ratios
exactly against all path–simplex vertices at q=3 and q=4. The repair check covers
all 512 and 27 exceptional three-label endpoint patterns and the four-label
counterexample. `exact_contracts.py` checks returned cuts against independently
enumerated integer flows and simplex vertices and checks decompositions exactly,
including zero and tiny positive weights. These finite checks supplement the
proofs; they do not prove arbitrary-size results or reimplement transportation
universality. Programs may write a JSON report beside their source file.

## Tables and measurements

The canonical raw data are
`paper-network-simplex/verification/stage06-benchmarks.json` (SHA-256
`373ce70b3839c12a206b193e9952d856f585da400f902bda773a725a609f73ac`). They contain
the reported input definitions, objectives, side rows, warmups, five rotated
runs, timing summaries, and audits. Optimization measurements were collected
separately from membership and cold-library measurements. Their raw provenance
fields retain references to an earlier archive and its update command; those
historical references are not dependencies or reproduction instructions. This
supplement supplies the final canonical data and the full runnable generator.

Regenerate all five published table/value files without rerunning experiments:

```sh
python paper-network-simplex/verification/stage06-tables.py
sha256sum -c MANIFEST.sha256
```

The generator verifies complete case keys, methods, rotations, expected statuses,
and every timing summary. Regenerated table bytes must match their manifest.
New JSON reports do not affect verification of the original payload hashes.

Run a smoke test, or the complete five-repetition protocol, into a new file:

```sh
PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06 --quick --repetitions 1 --output smoke-benchmarks.json
PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06 --output rerun-benchmarks.json
```

The smoke run contains four flat cases, one many-label membership case, and the
principal optimization case. The complete run contains 16 flat, three membership,
and three optimization cases. Warmups include audits; audit times are separate
from timed components. Exact membership-only and decomposition-inclusive queries
are independently timed. CSR byte counts exclude solver memory and Python
rational objects. Component medians need not sum to the median total.

To generate tables for a complete rerun, work in a second extraction and replace
its canonical `paper-network-simplex/verification/stage06-benchmarks.json` with
`rerun-benchmarks.json`, then run the table generator. That deliberately changes
the recorded data and table hashes. A quick or one-repetition run is not accepted
by the publication table generator.

The comparisons include cases where global state merging or elementary LPs are
faster than compression or exact separation. Additional budget rows compare
equivalent component-hull relaxations, not the exact hull of a newly constrained
product graph. All inputs are synthetic; no universal runtime advantage is claimed.
