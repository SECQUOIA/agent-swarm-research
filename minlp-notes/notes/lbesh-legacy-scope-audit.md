# Scope audit of the 27 legacy GDP instances

Date: 2026-09-19. This is a structural audit before the new legacy runs.
Historical outcomes are not used to select instances or classify scope.

All 27 registered models have convex objectives and convex nonlinear
inequalities in their required direction on their effective domains. All
pass the current flat-XOR structure extractor. They are useful as an external
numerical stress set. **They are not uniformly smooth, explicitly bounded
models to which the full compact-box convergence theorem can be applied
without qualification.** No optimization was performed for this audit.

The machine-readable audit is
[legacy_scope.json](../code/minlp_solver_lab/results/lbesh_development/legacy_scope.json).
It records each source file and hash, the registry hash, relevant data hashes,
all original and post-extraction bounds, every nonlinear constraint's
structural convexity certificate, objective certificates, and per-instance
scope flags. The reproducible checker is
[lbesh_legacy_scope.py](../code/minlp_solver_lab/lbesh_legacy_scope.py).
The instance set is exactly the 27 distinct names in historical
`results/gdp_final.jsonl`; no historical status, runtime, or objective is read.

## What was checked

Every nonlinear inequality was oriented as a convex function bounded above;
two-sided nonlinear rows were forbidden. The actual expression trees support
the following certificates:

- Every quadratic constraint and objective has a diagonal positive
  semidefinite quadratic matrix. The checker verifies the nonnegative
  diagonal and zero off-diagonal structure exactly in the extracted numeric
  coefficients; small matrix eigenvalues are supplementary diagnostics.
- The batch models use positive sums of exponentials of affine expressions,
  plus affine terms. Their convexity holds on all real arguments.
- Farm area rows are `area / width - length <= 0`, with positive area.
  Their convexity and smoothness require positive width. This condition
  follows from explicit affine constraints and is installed in variable
  bounds by the current extraction pass.
- The six `l2` layout objectives are positive sums of Euclidean norms in
  auxiliary distance variables. These functions are finite and convex
  everywhere, but ordinary gradients do not exist at a zero distance pair.
  Their subgradients are bounded; nonsmoothness must not be described as
  unbounded norm gradients.

The extractor independently rejects unsupported structural features such as
OR disjunctions, nested/disconnected active disjuncts, repeated disjunct
membership, nonlinear equalities, SOS constraints, and nonfixed GDP indicators
inside disjunct rows. All 27 extractions succeeded. This is a structural
acceptance result, not a claim that all solver interfaces support all models.

There are **18 instances with nonlinear disjunct constraints**, all quadratic.
The other nine have only affine disjunct constraints. The nonquadratic
nonlinearities in this legacy set are global rows or objectives. Consequently,
this set still cannot establish an advantage for general nonquadratic
*disjunct-level* separation.

## Per-instance scope

The table uses three conservative analytic classifications. `A` means the
extracted original variables have finite bounds and smooth functions, and
there is no unbounded automatic objective epigraph. `B` has the same smooth,
compact original-variable domain but introduces an unbounded automatic
epigraph. `C` is a broader numerical stress case with the indicated missing
hypothesis. These are data classifications; `A` does **not** certify strict
anchors, numerical separation, master solves, or single-tree oracle contracts.

| Instance | Class | Qualification |
|---|---|---|
| `gdplib.batch_processing` | C | Ten cycle-time upper bounds absent; automatic epigraph unbounded. |
| `gdplib.positioning` | B | Smooth quadratic objective; epigraph compactness needs an argument. |
| `gdplib.small_batch` | B | Smooth exponential objective; epigraph compactness needs an argument. |
| `pyomo.circles.Circles2D3` | B | Smooth quadratic objective; epigraph compactness needs an argument. |
| `pyomo.circles.Circles2D3_modified` | B | Same qualification. |
| `pyomo.circles.Circles3D4` | B | Same qualification. |
| `pyomo.constrained_layout.CLay0203.l1` | C | Six distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0203.l2` | C | Six distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.constrained_layout.CLay0204.l1` | C | Twelve distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0204.l2` | C | Twelve distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.constrained_layout.CLay0205.l1` | C | Twenty distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0205.l2` | C | Twenty distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.constrained_layout.CLay0303.l1` | C | Six distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0303.l2` | C | Six distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.constrained_layout.CLay0304.l1` | C | Twelve distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0304.l2` | C | Twelve distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.constrained_layout.CLay0305.l1` | C | Twenty distance auxiliaries lack upper bounds. |
| `pyomo.constrained_layout.CLay0305.l2` | C | Twenty distance auxiliaries lack upper bounds; norm objective nonsmooth; epigraph unbounded. |
| `pyomo.farm_layout.FLay02` | A | Affine propagation makes widths at least 1 and bounds the enclosure. |
| `pyomo.farm_layout.FLay03` | A | Same positive-width qualification. |
| `pyomo.farm_layout.FLay03_alt_1` | A | Propagated widths are at least 5. |
| `pyomo.farm_layout.FLay03_alt_2` | A | Propagated widths are at least 1. |
| `pyomo.farm_layout.FLay04` | A | Propagated widths are at least 3. |
| `pyomo.farm_layout.FLay05` | A | Propagated widths are at least 1. |
| `pyomo.farm_layout.FLay06` | A | Propagated widths are at least 1. |
| `pyomo.small_lit.basic_step` | A | Finite box, quadratic inequalities, linear objective. |
| `pyomo.small_lit.ex1_Lee` | B | Smooth quadratic objective; epigraph compactness needs an argument. |

Totals: 8 class A, 6 class B, and 13 class C. Thus 14 original-variable
domains are compact and smooth after extraction; only 8 extracted lifted
models have the corresponding explicit box data. The JSON's
`smooth_compact_analytic_scope_as_extracted` refers to these analytic data
assumptions only, as its top-level qualification states.

## Domain and theorem qualifications

**Farm layout.** The raw builder gives each width a variable lower bound of
zero and leaves the enclosure variables without explicit upper bounds.
However, its affine `width_bounds` rows impose the positive supplied lower
bounds, while `length_cons` and `width_cons` impose enclosure upper bounds.
The observed extraction pass transfers those facts into the box. Hence the
raw-box statement is false, while the post-extraction compact, positive-width
statement is true. On a box whose width lower bound is `w_min > 0`, the
reciprocal derivative has magnitude at most `area / w_min**2`. No solver
performance information is needed for this classification.

**Batch processing.** The extracted cycle-time variables have finite lower
bounds but no upper bounds. The nonlinear time row itself implies
`cycleTime_log[i] <= log(HorizonTime / ProductionAmount[i])`: each positive
summand is at most the positive right-hand side. Thus the original feasible
set has a finite box after an explicitly justified domain tightening.
That tightening is not part of this audit or the frozen benchmark models.
An unbounded master box cannot silently inherit this feasible-set argument.

**Layout auxiliaries.** Each distance auxiliary is constrained below by both
signed coordinate differences. It has no upper bound in the builder or the
observed extractor output. Replacing each distance by its absolute coordinate
difference preserves geometry and cannot increase either positive-weight
objective. Consequently finite distance upper bounds derived from the
coordinate boxes give an optimization-equivalent bounded formulation.
They do not describe the full original feasible set and are not installed
here. For `l1`, a proof that uses only the compact projection onto nonlinear
coordinates is another possible extension; it is not the current full-box
hypothesis.

**Norm objectives.** Non-overlap guarantees positive separation in an actual
feasible layout, but relaxed masters can place centers together and choose
zero auxiliary distances. Ordinary derivative formulas are undefined there.
The extractor's compilation probe produces zero-distance derivative warnings
on all six `l2` cases. A selected bounded-subgradient oracle, or an exact norm
epigraph/conic representation, can handle these convex objectives. Neither
the existence of bounded subgradients nor separation of feasible rectangles
proves that the current smooth numerical oracle handles every relaxed point.
Retain numerical failures and invalid witnesses rather than removing these
instances based on outcomes.

**Objective epigraphs.** An original finite box does not bound the newly
introduced epigraph from above. The theory note's
[epigraph section](lbesh-development-theory.md#6-epigraphs-and-compactness)
provides an optimization-equivalent finite bound or a separately justified
candidate-boundedness route. Those qualifications apply to class B as well as
to class C models with nonlinear objectives. This audit does not certify
finite termination of arbitrary single-tree callback candidate sequences.

## Provenance and interpretation

The exact tested models are the local registered builders, not claims of
bit-for-bit identity with published formulations. Their source docstrings
record the following benchmark provenance:

- [Batch processing](../code/minlp_solver_lab/instances/gdplib_src/gdplib/batch_processing/batch_processing.py)
  cites Ravemark (1995) and Vecchietti–Grossmann's LOGMIP work (1999).
- [Positioning](../code/minlp_solver_lab/instances/gdplib_src/gdplib/positioning/positioning.py)
  cites Duran–Grossmann (1986) and Gavish–Horsky–Srikanth (1983).
- [Small batch](../code/minlp_solver_lab/instances/gdplib_src/gdplib/small_batch/gdp_small_batch.py)
  identifies Example 4 of Kocis–Grossmann (1988).
- [Circles](../code/minlp_solver_lab/instances/pyomo_examples_src/examples/gdp/circles/circles.py)
  traces the problem to Lee–Grossmann (2000), but explicitly describes the
  modified and three-dimensional data as later example variants.
- [Constrained layout](../code/minlp_solver_lab/instances/pyomo_examples_src/examples/gdp/constrained_layout/cons_layout_model.py)
  links the benchmark description and attributes the data to Sawaya (2006).
  It explicitly identifies `l1` as the distance used in the paper; `l2` is a
  model variant, not an additional independent application.
- [Farm layout](../code/minlp_solver_lab/instances/pyomo_examples_src/examples/gdp/farm_layout/farm_layout.py)
  attributes the principal examples to Sawaya (2006), labels the alternate
  data as variants, and documents modeling interpretation choices.
- [Basic step](../code/minlp_solver_lab/instances/pyomo_examples_src/examples/gdp/small_lit/basic_step.py)
  identifies the example in Section 3.2 of Papageorgiou–Trespalacios (2017).
  [ex1_Lee](../code/minlp_solver_lab/instances/pyomo_examples_src/examples/gdp/small_lit/ex1_Lee.py)
  identifies Example 1 of Lee–Grossmann's nonlinear GDP algorithms paper.

These are provenance statements from the model sources, not a new literature
review. Related layout metric variants and related circle examples should not
be counted as statistically independent application families. Historical
stored optima and source comments about optima are not certificates and were
not used in this audit.

## Reproduction and review

Targeted command, from `code/minlp_solver_lab`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python lbesh_legacy_scope.py
```

Result: all 27 builds, all oriented-expression certificates, and all structure
extractions passed; counts are 27 convex effective-domain models, 14 compact
smooth original-variable boxes, 8 compact smooth extracted lifts, 6 nonsmooth
objectives, and 7 raw reciprocal-box singularities corrected by affine bound
propagation. Dependencies: Python 3.13.11, Pyomo 6.10.1, NumPy 2.5.3, and SymPy
1.14.0. No optimization solver was invoked. No project-wide checks or CI
inspection were performed.

A fresh independent reviewer rebuilt all 27 instances, compared the saved
audit fields against fresh extraction, and independently counted all 552
nonlinear constraints. All were upper-bounded in the original models, and
none was omitted. The reviewer checked the original farm and layout sources,
reproduced the 8/6/13 scope split, and found no classification defects.
The independent command was a one-thread `.venv/bin/python -` structural
check; it invoked no optimizer. This review verifies the fixed-set scope
classification, not feasibility, solver correctness, or numerical certificates.
