# Frozen short-run convexification protocol

Frozen on 2026-10-02 before running the new solver integration. The purpose is
to measure supported mechanisms, failures, overhead, and a held-out application
slice. This small, short-run experiment cannot establish a broad runtime win.

The synthetic cases are defined in `cases.py`: two balanced quartic models,
a cubic moment curve, exponential/logarithmic/trigonometric curves, a simplex
product, a quadratic vector on a simplex, overlapping products, a three-variable
star with incompatible pair marginals, an affine
control, a redundant convex control, and a binary-product control. Their
explicit feasible witnesses and analytically known optima provide independent
checks. No synthetic instance is selected by its observed outcome.

The 24 held-out MINLPLib instances are frozen in `holdout-selection.json`.
Selection excludes every instance named in the earlier univariate v2/v3
benchmark files and curve-hull result directory (123 names). From the remaining
cached OSiL instances, retain files of at most 150,000 bytes with at most 80
variables and 120 constraints, a quadratic or general nonlinear constraint,
and at least two nonfixed variables with finite declared bounds. Select the
first 24 in increasing SHA256 order of `convexification-holdout-v1:` plus the
instance name. This produces 24 instances from 279 eligible instances. The
filter uses model metadata and parser support, without consulting new-handler
applicability or optimization outcomes. This is held out from the two named
earlier campaigns, not a claim that these public instances were never used
anywhere in the repository. Before any new optimization outcome, the coordinator
expanded the originally proposed six instances to 24 using the unchanged ranking
to improve coverage. The first six remain marked as the initial subset.
The archived metadata classifies 11 of the 24 as having integer variables and
seven as convex; this intentionally retains controls where new cuts may not
help.

Four previously studied instances form a separate diagnostic suite, frozen before
new outcomes: `btest14`, `waterno2_06`, `ghg_2veh`, and `chp_partload`. Their
results are never included in the held-out population summary.

Compare four modes on every instance: the original model (`baseline`), the
same auxiliary reformulation used by the new methods with native equalities
but no new cuts (`control`), all supported blocks (`all`), and automatic block
selection (`auto`). Retain reformulation and rejected-block costs. Use seed 0,
one SCIP thread, one BLAS/OpenMP thread, relative gap tolerance 1e-4, and a
six-second soft total integration budget including model analysis, preprocessing,
certification, and solving. Each worker has a hard 20-second process timeout;
imports and independent checking are recorded separately in outer wall time.
Discovery, model construction, and individual support calls are nonpreemptive,
so their observed totals may exceed the soft budget. Retain and report these
overshoots. If a worker is killed before its JSON result is written, its cut
count is unknown; an absent cut log must never be interpreted as zero cuts or
successful replay.
Run one worker at a time. The environment already hosts unrelated optimization
jobs, so subsecond timings are descriptive and cannot support speed claims.

Record root bounds from the full runs. Also run a two-second, one-node version
of each mode on the 24 held-out instances and five mechanism cases:
`quartic_balance_8`, `exp_pair`, `simplex_quadratic_vector`, and
`overlapping_products`, plus `star_marginal_inconsistency`. Root-only results distinguish the effect of root cuts
from later search. Root and full budgets are separate; the full solver is not
warm-started from root-only results.

Run caching ablations only if caching is implemented: `all` and `auto` with
caching disabled on those same five mechanism cases at the six-second budget.
The `cache_samples=False` configuration also disables support-point exchange,
repeated-point skipping and automatic screening. The `no_cache` phase therefore
changes the combined reuse policy; it is not an isolated timing measurement of
sample caching, and differences must not be attributed to caching alone.
The optional compiled sampling kernel is evaluated in the separate, bounded
35-case NumPy-versus-C microbenchmark saved in
`../implementation/native-kernel-benchmark.json`, including compilation and
preparation costs. The coordinator authorized this targeted ablation before
campaign outcomes. Campaign workers do not compile or load the optional C
backend; its separate measurements cannot establish faster complete solves.
Do not substitute a different algorithm and call it a native implementation.

For the star case, also run `all` and `auto` with star merging disabled at
six seconds. The analytical comparison has exact pair-hull lower bound zero
and true minimum 1/128; native SCIP and the generic separator may obtain
different numerical bounds, so the theorem is reported separately from the
solver outcome. This case and ablation were added before new solver outcomes,
after the coupled-theory agent supplied the exact construction.
The comparison concerns the two local pair hulls with their stated shared
moments. It does not assert dominance over a full dense PSD/RLT lift, which can
recover the incompatible-marginal example.

Repeat seed 1 on the first three held-out instances and
`quartic_balance_8`, `exp_pair`, and `simplex_quadratic_vector` if the aggregate
budget leaves time after the primary and ablation runs. This subset is fixed
before seeing results. These small repeats can identify sensitivity; they do
not estimate a population effect precisely.

The campaign has a 30-minute aggregate wall cap, including managed worker
startup and saved output. Save timeout/error records and do not silently
replace unfavorable instances. Repeat only after an identified correctness
or instrumentation defect, preserving the original output and recording the
reason and amended implementation hashes.

For every successful run save the exact input model fingerprint, implementation
hashes, original variable values, solver status, root and final numerical dual
bounds, primal objective, nodes, cuts, selection/caching statistics, and timing.
Evaluate original bounds, integrality, expression domains, objective and every
row independently of the model builder. These residual checks are numerical,
with scaled tolerance 1e-5. Check numerical dual bounds against known synthetic
optima or archived MINLPLib feasible bounds with an explicit tolerance; neither
that comparison nor a cut certificate certifies the solver's dual bound.

Replay every saved new cut certificate in a fresh process, binding its domain,
features, coefficients and auxiliary variables to the actual original model.
Report failed or missing binding/replay records separately; never count an
unreplayed cut as certified. Also test tampered coefficients and bindings.
Retain all raw records, logs, and source hashes. Verification is restricted to
this topic; no project-wide tests or CI inspection are part of this protocol.
