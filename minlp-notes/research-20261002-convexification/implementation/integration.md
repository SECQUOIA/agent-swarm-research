# Solver integration and its limits

The implementation in `solver/integration.py` adds certified global linear
inequalities at SCIP's root node. Native SCIP constraints enforce the original
model and every admitted auxiliary definition. There is no Python feasibility
handler, propagation rule, spatial branching rule, or local cut. This removes
the repeated per-node envelope construction, interval trimming, and primal
completion paths used in the older experimental handler.

This is a bounded experimental solver component, not an unrestricted nonlinear
model importer or a complete graph-hull separation algorithm. In particular,
the certificates validate the added inequalities. SCIP's primal feasibility,
presolve, node bounds, and termination remain numerical.

## Four comparable modes

`baseline` builds the admitted original model. `control` introduces shared
auxiliary variables with native defining equalities and adds no custom cuts.
`all` applies the separator to every admitted block, subject to fixed work
limits. `auto` uses the same reformulation and first filters block candidates:

- A univariate block needs two nonlinear coordinates or a composite atom with
  at least two nonlinear operations.
- A two-variable block needs an original affine domain row; one bilinear
  coordinate is enough. The simplex example therefore remains eligible.
- A detected quadratic star with at least two leaves is eligible.

These structural rules are a heuristic selection policy, not a prediction of
runtime improvement. Auto additionally requires a larger sampled violation
and stops attempting a block after two unsuccessful certification attempts.
That last rule can miss cuts at subsequent relaxation points.

Polynomial blocks can reuse an exact convex combination of feasible graph
samples. At each new query, the implementation recomputes its scaled L1
distance upper bound. A sufficiently small bound proves that no cut in the
current coefficient normalization can exceed the selected violation threshold
at that query. It does not prove graph-hull membership or the absence of useful
cuts at future queries. The mixture proposals come from the direction LP's
dual multipliers; there is no second optimization problem. Only its sparse
positive support is evaluated exactly. Exact domain checking can reject a
sample admitted by floating-point grid filtering.

The direction LP bounds every scaled coefficient in `[-1,1]`. The associated
distance is consequently L1. The actual exported binary64 coefficients are
contracted, when needed, to satisfy `max_j scale_j*abs(c_j) <= 1` in exact
rational arithmetic. This keeps the screening normalization valid after
floating-point coefficient conversion.

## Source and solver binding

The mathematical input convention is the exact binary64 values loaded by the
existing OSiL reader. It is not exact interpretation of decimal XML text.
Original source trees are retained in the output and used for replay. Two
different source trees never share an auxiliary merely because symbolic
algebra simplifies them to the same expression: their domains can differ.

The importer follows a conservative admission policy in every mode:

1. Preserve and check source domain restrictions before simplification.
   Every denominator, logarithm argument, square root, and fractional or
   negative power must have a proved domain throughout the declared box.
   A model that relies on such a function to narrow its declared domain can
   be refused. Original affine constraints are not used to infer unproved
   variable bounds.
2. Fold a constant arithmetic subtree exactly only when its final result is
   representable in binary64. This fixes, for example, `1e16 + 1 - 1e16`
   without rounding the intermediate sum. Keep original source metadata.
3. Reconstruct the exact coefficients stored in the constructed PySCIPOpt
   expression DAG and compare each full original row with its source
   interpretation. Refuse the entire model consistently in all modes when
   these differ. The result has status `source_model_mismatch`, a diagnostic,
   and no primal value, bound, or cuts. Ordinary decimal coefficient
   arithmetic can trigger this conservative restriction.
4. Compare each auxiliary's native expression with its exact source feature.
   An unequal atom remains native and cannot supply a certified auxiliary.
   Check rewritten rows again after substituting admitted source features;
   if rewriting changes a row, retain its admitted original native form.
5. Reject finite declared variable bounds or constraint sides reaching SCIP's
   infinity sentinel, NaN, reversed bounds, and incorrectly signed infinite
   sides. They must not silently become unbounded solver domains.

For an added cut, the certificate is computed for the exact binary64
coefficients requested from SCIP and a right-hand side rounded downward from
the certified rational bound. After SCIP builds the row, its stored columns,
coefficients, constant, sides, and local/global flag are checked again.
Aggregation is disabled for participating variables. Any altered coefficient
or missing nonzero column causes rejection, including a column eliminated by
a numerical presolve fixing. No proof of that fixing is assumed. Saved
evidence includes both the source columns and actual transformed columns.

These checks do not establish a fully verified SCIP solve or verify SCIP's
later internal numerical transformations.

## Discovery and support computation

The detector splits additive source expressions, separates scalar multipliers,
and extracts bounded nonlinear atoms. It groups functions sharing one
variable, pairs occurring in an atom or an original affine row, and supported
quadratic stars from overlapping pairs. It retains native enforcement of all
remaining expressions.

The default polynomial degree limits are eight in one variable and four in
two variables. General elementary atoms are univariate and must pass the
certificate kernel's expression/domain checks. Supported quadratic stars
contain a center, leaf squares, and center-leaf terms, with no leaf-leaf
quadratic interaction. Only existing original affine rows whose variables
belong to a block restrict its certificate domain.

The support backend uses exact polygon enumeration for bivariate quadratics,
exact piecewise quadratic elimination for supported stars, rational Bernstein
bounds for other small polynomial blocks, and the elementary interval backend
for supported curves. Every unsuccessful budget-limited search is an
incomplete attempt, not an infeasibility or hull-membership decision.

Direction proposals use cached sampled graph coordinates and a small HiGHS
LP. Constrained polygons also receive exact vertices, a centroid, and edge
midpoints. Constrained stars receive exact coordinate-extremum samples. These
seeds cover cases where equality constraints or a slender feasible set leave
no feasible tensor-grid samples. A failed quadratic proposal can add the
oracle's exact minimizer and repeat the direction LP, with at most three
exchange rounds. This bounded exchange does not establish complete separation.

Default limits are 256 atoms, 64 blocks, eight coordinates per block, five
root callback rounds, 24 cuts, six cuts per round, and 128 certification cells
with depth at most 16. Candidate sampling uses 65 univariate grid points or
a 13-by-13 bivariate grid; larger stars use deterministic low-discrepancy
samples and box corners. Feature caps can omit expressions. Exact feasible
seeds and exchange points supplement these samples.

## Costs and native code

The function-level wall clock begins before reading the model. Reading,
discovery, source/model auditing, and construction consume the requested
budget; SCIP receives its remainder. Callback costs are included in SCIP's
solve time and must not be added to solve wall time a second time. Separate
counters record proposal, screening, certification, and row insertion costs.
The separator checks a budget of the smaller of two seconds and 15% of the
requested run limit, between bounded atomic operations. These are soft
budgets: an in-progress symbolic calculation, LP, support oracle, or SCIP call
can overrun. The campaign supervisor supplies the separate process limit.

Interpreter startup and imports precede `run_instance`; the benchmark runner
also records process wall time. Optional C compilation is explicit, and its
process cost must be counted when used. SCIP and HiGHS are compiled native
code. The optional polynomial sampler is described in
[native-kernel.md](native-kernel.md); it proposes directions only and never
certifies cuts. This implementation is not a native C SCIP nonlinear handler.
The default small grids generally retain the vectorized NumPy sampler.

SCIP, HiGHS, and benchmark BLAS execution are configured for one thread.
The default relative gap limit is `1e-4`. Samples and repeated-query data are
cached per block; `Config(cache_samples=False)` disables those integration
caches, support-point exchange, repeated-point skipping, and automatic
screening together. This ablation does not isolate the effect of caching
alone. `Config(merge_stars=False)` disables star merging.
Neither switch removes native model enforcement.

## Running and targeted verification

From the repository root, with the existing solver environment:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/solver/run.py instance.osil auto --time-limit 30 --output run.json
PYTHONPATH=research-20261002-convexification code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261002-convexification/solver/test_integration.py research-20261002-convexification/solver/test_model_binding.py
```

The targeted command above was run after the final input checks: **32 tests
passed**. The focused tests cover actual SCIP row emission and replay, source/native
coefficient mismatch, catastrophic constant cancellation, distinct source
domains, constant infeasibility, thin equality domains, star discovery, and
finite bounds that exceed SCIP's representable domain convention. The final
review records additional independent tests.
No project-wide local verification or CI inspection was performed.
