# Frozen-study protocol: radial and point separation for convex GDP

Protocol prepared after development pilots and before the main algorithm
study on held-out seeds. The pre-freeze continuous-reference computation is
disclosed in [the development log](lbesh-development-log.md). This is a
repository protocol, not a claim of external preregistration.

## Questions and claim limits

The study asks whether disjunct-level radial separation (ESH) improves on
point tangents (ECP) enough to pay for root searches, under otherwise matched
implementations. The same affine cuts belong to the established perspective
OA family. Neither a new cut family nor uniform dominance is hypothesized.

Primary comparisons are matched ESH versus ECP within each formulation/tree
combination. Secondary comparisons concern hull versus big-M, single versus
multiple trees, reduced-NLP and fractional-user-cut ablations, and established
solvers. Exact quadratic conic hulls and separate continuous cone references
provide additional context. Success on a generated family does not establish
general solver superiority.

## Instances and split

Use all 51 fixed instances in `lbesh_research.instances.MANIFEST`: 18 pilot
and 33 held-out instances. These represent six families, two principal model
structures, three sizes, and fixed seeds. Allocation families share data
across function laws, and sizes share parameter prefixes. They are related
controls, not 51 statistically independent real applications. Report family,
size, and split rather than hiding this dependence in an aggregate.

Use the 27 historical convex GDP instances as a separate external set.
The independent source audit distinguishes compact smooth cases from models
with unbounded auxiliary variables or nonsmooth objectives; the latter are
numerical stress tests, not instances satisfying every theorem assumption.
Their original historical performance labels are not reused. Unsupported
inputs and interface failures remain visible and are distinguished from
unsolved supported problems. Cone references cover 42 generated instances;
the quadratic mixed-integer conic baseline covers the nine quadratic controls
and supported legacy models. No cone translation is supplied for trig.

## Methods, settings, and timing

Main generated study:

- Eight matched configurations: ESH/ECP, hull/big-M, single/multiple trees.
- GDPopt LOA; SHOT big-M; SHOT declared-convex epsilon-hull; Gurobi big-M;
  SCIP big-M. The declared-convex option is restricted to generated models
  with verified convexity; default SHOT hull behavior is supplementary.
- Exact quadratic hull with Gurobi, on its supported subset, reported
  separately rather than penalized for mathematically unsupported families.

Each primary run gets a 120-second solver limit, a 150-second whole-process
wall limit, and one solver thread. At most six experiment workers run at once.
BLAS/OpenMP thread counts are one. End-to-end wall time includes Python startup,
model building, preprocessing, interior NLPs, and solver work. Preserve raw
statuses, effective options, native GAMS fields/logs, complete witnesses, and
source/environment fingerprints. The SHOT feasibility settings were aligned
with the common checker during pilots; they are recorded, not silently
relaxed after a failed run.

Use reproducibly shuffled job orders, with seed 20260919 for the primary run.
Repeat the four single-tree ESH/ECP hull/big-M configurations on the 33 held-out
instances twice more, using order seeds 20260920 and 20260921. Keep each
repetition separate; never choose the fastest repeat. The solver's own seed
remains unchanged, so these repetitions assess runtime variation rather than
search-seed robustness.

Reduced-NLP and optional fractional-user-cut ablations are secondary and
must use the same declared instances and settings. Do not select their
instances based on which oracle wins. The NLP-free ablation still shares the
matched interior initialization; it is not an algorithm without NLP work.

Before supplementary runs, the exact follow-on schedule was saved in
`results/lbesh_development/supplementary_plan_v1.json`: 132 jobs per held-out
repeat; nine quadratic conic MICP jobs; 351 legacy jobs (eight matched
configurations, GDPopt LOA, SHOT big-M, Gurobi big-M, SCIP big-M, and the conic
hull adapter); and 144 secondary ablation jobs. The ablations use all 18 pilot
instances, each of the four single-tree configurations, and separately disable
integer-point NLP solves or enable fractional user cuts. This selection uses
the declared pilot split, not observed oracle winners. Their comparison uses
the corresponding primary pilot runs. The additional order seeds are
20260922 for conic controls, 20260923 for legacy cases, and 20260924 for
ablations. Unsupported conic inputs remain visible in the external table and
are excluded only from supported-subset conic comparisons.

## Validation and outcomes

An accepted numerical solve requires a complete primal witness that passes
the independent checker on a fresh original GDP, plus a solver-reported
global bound with a closed numerical gap. Primal row/bound tolerance is
`1e-6 + 1e-7 * max(1, abs(body), abs(bound))`; integrality tolerance is
`1e-6`. Objective comparisons use the original objective and sense. The
comparison gap is `1e-6 + 1e-4 * max(1, abs(objective))`.

These are numerical validations, not exact-arithmetic optimality
certificates. Local status, objective consensus, elapsed time below a cap,
and the best observed objective do not substitute for a global bound.
Any lower bound contradicting an independently validated feasible objective
outside tolerances requires investigation before including the run as solved.

For small supported generated models, compare with independent exhaustive
fixed-assignment convex solves. Preserve statuses, residuals, and unresolved
assignments. Inaccurate or failed reference solves cannot be promoted into
exact optimum references. Continuous cone dual values are explicitly
uncertified numerical estimates.

Audit every results file against its saved schedule, including wholly missing
methods or instances. Report invalid witnesses, unavailable/unsupported
methods, errors, timeouts, feasible open-gap runs, and numerical solves
separately.

## Analysis

Primary outcomes are numerical solved counts and end-to-end runtime. Use
paired common-solved comparisons for timing, and PAR10 on the full scheduled
set (a failure pays ten times the common wall cap). Report shifted geometric
means with a one-second shift, explicit denominators, family/size tables,
and repeated-run stability. Exclusions require a mathematical/input-scope
reason and must not depend on the outcome.

Use cut counts, interior/NLP counts, LP exit reasons, LP bounds, and measured
cut-generation time to explain outcomes. In single-tree mode `time_master`
includes callback work, while `time_nlp` and `time_cuts` overlap with it;
these times must not be summed or plotted as an additive decomposition.
An LP stalled or capped with residuals is not declared hull-feasible.

Do not infer broad statistical significance from related generated instances
or only three seeds. Negative and mixed findings are retained. A fresh
reviewer will audit the final data, analysis, and publication claims before
readiness is decided.
