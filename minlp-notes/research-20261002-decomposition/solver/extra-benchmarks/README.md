# Independent bounded benchmark

This benchmark tests the complete rational box-QP implementation on small
diagnostics and on two unmodified compatible library instances. It records
failures and resource limits. It is a diagnostic experiment, not evidence
of competitive performance on general MINLP.

## Corpus and references

`corpus.py` defines ten small rational problems: random signed path and
band objectives, a branching interaction tree, mixed and pure integer
paths, flat and tied optimal sets, and a pair with a weak negative
curvature direction and differently scaled positive curvature. The random
problems do not use planted optimizers. The flat cases and curvature pair
are deliberate diagnostics and are labeled accordingly. Integer domains
have three values, so the mixed tests are not merely binary reformulations.

An independent exact oracle enumerates integer assignments and all
continuous active faces on these small cases. It solves the stationary
linear systems over rational numbers. If a minimizing stationary face is
singular, a null direction reaches a smaller face at the same value;
repeating this gives a nonsingular face or a vertex. This establishes why
the enumeration is exhaustive, including the degenerate examples. The
oracle is exponential and is used only as a reference.

The two external inputs are
[QPLIB_3852](https://qplib.zib.de/QPLIB_3852.html), with 231 binary variables
and 440 quadratic terms, and
[QPLIB_5881](https://qplib.zib.de/QPLIB_5881.html), with 120 binary variables
and 2,123 quadratic terms. Both have no constraints beyond their binary
domains. The supplied objectives and domains are retained in full.
Maximization is converted to minimization by reversing the objective
sign. These are binary QP experiments; they do not establish performance
on continuous library instances or constrained MINLPLib models.

QPLIB's triangular quadratic format requires an off-diagonal coefficient
to be halved when forming the symmetric matrix in `x'Ax/2`. The reader
checks this convention and the objective sign independently against each
bundled library solution: the exact values are 234 and 13,067 before sign
reversal. These supplied feasible solutions are not asserted to be proved
global optima. See the [QPLIB format documentation](https://qplib.zib.de/doc.html).

The files in `data/` were downloaded from QPLIB on 2026-10-02. They retain
their original contents. QPLIB is provided by Zuse Institute Berlin and
GAMS under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The instance pages identify Stefan Vigerske and BicMac as their respective
donors. The `.gms` copies make the quadratic coefficient convention easy
to inspect; the executable benchmark reads `.qplib` and `.sol`.

## Methods and limits

The three grid methods receive the same deterministic greedy minimum-degree
tree decomposition. SCIP constructs its own internal representation and
does not receive that decomposition. The recorded width is the width of
the supplied grid decomposition,
an upper bound on treewidth. A resource refusal with that decomposition
does not prove that no better ordering or representation could succeed.

The four methods are:

- Corrected geometric grids with min-marginal pruning.
- The same geometric grids without pruning.
- Uniform corrected grids without pruning.
- Single-thread SCIP, using an epigraph constraint for the quadratic
  objective and an absolute gap target matching the exact methods.

The default suite runs all twelve cases at absolute tolerance `1/50`,
and the random path and two curvature cases additionally at `1/1000`.
Each of the resulting 60 solver runs has a two-second solver limit.
The exact implementation also has a 20,000 aggregate table-state limit
per stage and a 24-stage limit. SCIP has a 256 MB internal memory limit.
Every run uses a fresh subprocess; an outer wall limit of 14 seconds
includes input construction, certificate serialization, and verification.
Subprocesses run sequentially and are killed and collected on an outer
timeout. BLAS and solver thread counts are one.

SCIP's primal and dual bounds remain explicitly labeled numerical.
Separately, its incumbent coordinates are rounded for integer variables
and clipped to the box, then their objective is recomputed exactly as a
rational feasible upper bound. This repair is legitimate because the
models have no coupled constraints. It does not certify SCIP's dual bound.

Exact-method outputs include replayable gzip-compressed certificates and
the independent verifier's actual result. Every small-case certificate
must enclose the exact reference optimum. Solver time, certificate-check
time, decomposition time, worker time, and subprocess wall time are
reported separately. A run that reaches a limit keeps its last valid
bounds when available; it is not counted as solved at the requested
tolerance.

Memory is the worker's Linux `/proc/self/status` `VmHWM`, including the
interpreter, imported libraries, construction, solving, and verification.
The raw `getrusage` value is retained separately because some launch paths
preserve an ancestor's previous high-water value. These are process peaks,
not isolated memory consumed by DP tables. Certificate checking follows
solving in the same worker, so the peak includes both.

The curvature diagnostics report numerical eigenvalues and exact maximum
positive diagonal entries. They do not estimate or certify global
quadratic growth constants. Runtime differences on this shared machine
are descriptive; no statistical performance claim rests on a single run.

## Reproduction

From the repository root, with Python, NumPy, and PySCIPOpt installed:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python research-20261002-decomposition/solver/extra-benchmarks/run_benchmarks.py --run

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python research-20261002-decomposition/solver/extra-benchmarks/run_extensions.py --run
```

The script writes exact references, instance metadata, environment and
source hashes and snapshots, every per-run result, and an aggregate
`results.json` under `results/`. It fails if a small exact certificate
excludes its reference optimum, or if a consumed source or input changes
during the suite. The extension script writes `extension-results/` with a
small dimension sweep and original/reduced affine-recourse comparison.
It uses the same worker, limits, and measurement conventions. Its generated
family has a known analytic optimum and is labeled as a designed example.
All bundled inputs permit offline reproduction. Only this topic-specific
experiment is authorized; no project-wide or CI check is part of it.

Recorded findings are in [FINDINGS.md](FINDINGS.md).
