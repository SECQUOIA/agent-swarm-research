# Extension diagnostics

Ten configurations exercise the polynomial grid, exact implicit boundary output,
and mixed convex/concave submodular recourse added during completion. Six reach
their requested mathematical outcome. Three return valid bounds while reporting
a table cap, a cut cap, or an unsupported structural class. One boundary search
is inconclusive and emits no exact-output certificate. All nine emitted
certificates pass separate replay against the original input and an independent
reference. These small diagnostics do not establish competitive performance.

| Configuration | Result | Independent reference | Separate replay |
| --- | --- | --- | --- |
| Quartic without quadratic growth | Requested gap achieved | `(x−1/3)^4`, minimum 0 | Valid |
| Sparse mixed polynomial | Requested gap achieved | Sum of three squares, minimum 0 | Valid |
| Same polynomial, one-state table cap | `table_limit`, no grid stage completed | Same input and reference | Valid interval |
| Irrational boundary optimizer | Exact implicit convex patch | `(1/√2,0)`, minimum 0 | Valid; patch contains optimizer |
| Weak boundary reduction | Exact implicit convex patch | `(1/4,0)`, minimum 0 | Valid; patch contains optimizer |
| Symmetric quartic, two search rounds | `inconclusive` | Two irrational minimizers, minimum 0 | No certificate emitted |
| Mixed two-cut example | Exact value 0 | Independent stationary-face enumeration | Valid |
| Fresh signed mixed QP, six variables | Exact value `−509/105` | Independent integer-label and stationary-face enumeration | Valid |
| Two-cut example with one-cut cap | `resource_limit`; gap `13/16` | Same exact reference | Valid interval |
| Unbalanced signed triangle | `unsupported`; gap `3/2` | Independent exact minimum `−1/2` | Valid interval |

The fresh six-variable instance uses seed 12803, four concave coordinates, two
coupled convex coordinates, and two native integer coordinates. It has no planted
optimizer. The recourse method uses 9 conditional QP queries, 5 greedy-base cuts,
and 88 LP/QP pivots. The separate three-variable regression requires a genuine
mixture of two bases. The remaining examples have stated analytic constructions;
they are not random or public-library instances.

The polynomial run without quadratic growth completes 36 grid stages and 545
table states. Its approximation certificate makes no growth assumption. The
mixed polynomial completes 8 stages and 469 states. The irrational boundary
example needs global refinement before the restricted convex patch can be
certified. A patch describes an exact optimizer implicitly; it does not claim
an explicit rational point or a zero numerical gap. The symmetric example's
failure is failure of this bounded sufficient test, not a proof that exact
output is impossible.

All configurations run sequentially in fresh processes with one numerical
thread, a two-second cooperative solver budget, a five-second hard deadline per
solver or checker, and a 512 MiB address-space limit. Imports, decomposition,
validation, serialization, and process startup are included in subprocess wall
time. Exact references were prepared separately and are excluded from solver
timings. The sum of recorded solver and checker subprocess times is 1.377
seconds; maximum recorded process peak RSS is 23,708 KiB. No process reaches its
hard deadline or address-space cap. These single-run timings characterize this
small diagnostic run only.

[summary.json](summary.json) contains all timings, statuses, source paths, and
loaded-module hashes. [results/](results/) holds exact JSON certificates and
separate replay records. [frozen/manifest.json](frozen/manifest.json) hashes the
actual runner, corpus, exact inputs, references, solver modules, and sibling
modules needed by dynamic imports. Every loaded repository module is checked
to lie within that snapshot. The checker reconstructs the original input from
the frozen corpus and verifies certificate binding before checking a proof.
For capped and unsupported submodular results, replay proves the returned
interval; its status label is not itself a mathematical certificate of class
membership or nonmembership.

Targeted commands actually run from the repository root:

```sh
python -m py_compile research-20261002-decomposition/completion/benchmarks/extensions/corpus.py research-20261002-decomposition/completion/benchmarks/extensions/run_extensions.py
python research-20261002-decomposition/completion/benchmarks/extensions/run_extensions.py --freeze
python research-20261002-decomposition/completion/benchmarks/extensions/run_extensions.py --run
```

The frozen run refuses to overwrite its evidence. To replay the retained nine
proofs, or reproduce all ten configurations in temporary output directories:

```sh
python research-20261002-decomposition/completion/benchmarks/extensions/reproduce.py
python research-20261002-decomposition/completion/benchmarks/extensions/reproduce.py --solve
```

No project-wide or CI verification was run for this extension suite.
