# Stage 6 author record

Status: author work complete; the required five independent stage reviews are
pending. No new mathematical claim is accepted by this record alone.

## Scope and source coverage

This stage implements the accepted flat-chain developments, strengthens the
computational comparisons, and adds `sections/08-computation.tex`. Accepted
sections 01–07 are unchanged. The implementation and computational notes, the
historical separator and compressed-formulation audits, and every item in
`computational-baseline-plan.md` are covered. Stage 7 introduction, literature
connections, integral-flow corollary, and final exposition are left for the next
stage. No other paper folder was edited.

The section distinguishes the usable exact parallel-path and flat-chain
separators from numerical general compressed formulations and the bounded-rank
verification prototype. It gives a two-supplier service-transportation
interpretation under the common balance and capacity assumptions. The data are
synthetic; no industrial validation or persistent-solver claim is made.

## Implementation and development

`code/network_simplex/flat_chain.py` now merges globally unobserved labels and
eliminates the residual profile. At zero observed labels it returns the original
flow as a shared default. At one or two labels it uses explicit interval tests
and recovery without constructing any circuit library. Three labels use the 16
reduced circuits and both proved bypass-balance repairs, giving unit flow and
product coefficients. Larger label sets use the reduced normal library and
finite inverse-basis recovery. Every basis is allowed: forcing the explicit
profile sum to the total branch flow would incorrectly exclude points with
positive residual branch flow.

Recovery stores observed groups and one default, then refines unused original
labels by their weights. Original-state `flow` queries and the former dense
profile accessors remain available; materializing dense arrays incurs output
cost. Observation indices and malformed observation records are validated.
The production exact oracle has no scientific-package dependency. Tuple normal
construction retains a dimension factor relative to the theorem's preindexed
bitmask operation count; this implementation detail is stated explicitly.

The old source is preserved in `verification/reference/stage06/`, with a hash
manifest, as a reproducible research reference rather than another public API.
The old `circuit_library` and `_profile_bases` helpers remain for historical
audits; the latter is unused by production. New tests target the new inverse
bases separately. The original benchmark builders and old measurement records
remain intact.

## Strong baseline controls

`strong_baselines.py` assembles full and globally merged disaggregation using
sparse block matrices. Optimization keeps every original simplex coordinate,
its objective, and any added original-coordinate row. Membership treats x, y,
and z as data, as the legacy membership builder already did; the actual changes
are efficient assembly, exact zero-state removal, and robust solver-status
handling. With exactly two positive states the added one-flow network baseline
substitutes the other state as x minus that flow and intersects both states'
bounds and observations. With one positive state it checks directly.

A fixed-y objective without coupled rows also receives the elementary baseline
of independent network optimizations, sharing an incidence matrix and the
unobserved-label cost. One additional aggregate-budget comparison disables this
separability. Its exact reference point is feasible and the unconstrained
optimum violates the chosen budget. This comparison concerns H intersected with
the budget, not the hull of the additionally constrained product graph.

The stronger baselines explicitly distinguish numerical statuses 0 and 2 from
solver failures. Exact bound and zero-weight checks do not make the numerical
LP answer an exact membership certificate; its aggregate-balance tolerance is
documented. The general compressed certificate statuses and exact dual-kernel
repair checks are also described without equating `numerically_feasible` with
certified membership.

## Measurements and interpretation

The reproducible generator is `paper_stage06.py`; raw results are in
`verification/stage06-benchmarks.json`. All 16 flat cases, three many-label
membership cases, and three optimization cases use one recorded warmup and
five repetitions with rotated method order. Build, solve, total, recovery, and
separate audit costs are retained where applicable, with raw records and
minimum/median/maximum summaries. The host was shared and not isolated. Exact
audits and numerical cut-support checks run outside timed components. No
production or benchmark algorithm changed after the recorded full run.

The flat grid covers lengths 8, 32, 128, and 512, feasible and McCormick-feasible
infeasible points, boundary weights (1/2,1/2), and interior weights (1/3,1/3).
It includes the retained unreduced exact oracle, new reduced oracle, vectorized
positive-state LP, and the one-flow LP on the two-positive-state face. General
initial and observed-eliminated models were also remeasured on all eight cases
at lengths 8 and 32. Both membership-only and recovery-inclusive exact queries
are measured directly.

The main sparse optimization instance has 43 arcs, 128 labels, and 36 products.
Only 11 labels occur anywhere. Full/global/initial/eliminated variable counts
are 5,675/644/255/222. Their median total times are approximately
35.71/7.44/6.95/8.32 milliseconds. Repeated cutting takes about 310.53
milliseconds and 42 cuts. Global state merging explains much of the original
full-versus-compressed difference; a cut loop does not win this comparison.

The all-labels-observed control has 111 arcs, 64 labels, and 192 products.
Full and global models both have 7,279 variables, while initial compression
has 495 and observed elimination has 367 with no auxiliaries. Corresponding
median totals are 52.30/56.02/12.01/20.30 milliseconds. This control separates
the local graph advantage from removing globally unused labels. The one budget
control retains the same size ordering and again favors compact LPs over the
repeated-cut implementation. Independent network solves attain the uncoupled
objectives but multiple solver calls are slower than the best joint compact LP.

The stronger LPs reverse the earlier long-chain boundary interpretation. At
512 gadgets on the feasible boundary face, the positive-state and one-flow LP
medians are 14.36 and 12.90 milliseconds, compared with 16.93 for the new exact
oracle. On feasible interior queries the new oracle is faster at the largest
length, while infeasible interior ranges overlap widely. No universal speed
ordering is supported. At 1,024 labels the global-merger membership LP is also
faster than both general compressed variants and the exact graph separator.
These negative results are retained because they identify what the structural
methods actually add: model-size savings and exact constructive certificates,
with runtime depending on the workload and implementation.

Five generated LaTeX table files come exclusively from the full-run JSON.
`verification/stage06-tables.py` checks the case grid and recomputes every stored
timing summary before rendering. Its headers identify the data hash. Solver
matrix byte counts exclude Python objects, factors, and process peak memory.

## Verification

The exact commands, logs, outcomes, and frozen hashes are in
`verification/stage06-validation.json`. The combined suite passes 21 tests.
New tests cover arbitrary observations, zero weights, sparse labels among many
original coordinates, no-library execution through two observed labels, every
new rank-three inverse basis, and the interior-residual regression. Both
three-label bypass repairs receive exact global cut-validity checks; the
four-label coefficient-two obstruction exercises the general library. Cut
validity checks maximize over exact path–simplex vertices on small graphs.

Baseline tests compare free- and fixed-y objectives on varied multigraphs,
including loops, parallel arcs, and isolated vertices; they test all-original-y
objective preservation, coupled original-coordinate rows, conflicting observed
entries, and solver failure handling. Numerical comparisons do not prove exact
optimality. A separate root check supplies 60 further numerical comparisons
with free y and three coupled x/y/z rows.

Previously independent audits were rerun on the changed implementation. The
flat audit passed 233 numerical path-hull comparisons, 192 exact decompositions,
and 708 exact violated cuts. The parallel-path audit passed its random-graph
and hypersimplex cases. The compressed audit passed 600 objective comparisons,
758 membership comparisons, and 476 exactly checked Farkas cuts; structural
integration recovered coefficient ratios 2, 5, and 21. The legacy baseline
audit passed 120 support cases, 360 full membership queries, and 360 compressed
membership queries. These finite checks support implementation correctness;
the manuscript's proofs establish the general results.

SciPy and HiGHS citations were verified against SciPy's official citation page
and the HiGHS project/publisher information. Runtime versions are retained in
the measurement file, with the bundled HiGHS version independently read from
the installed SciPy extension in `stage06-environment.json`.

The final manuscript builds with `latexmk -gg -pdf -interaction=nonstopmode
-halt-on-error main.tex`, without warnings or undefined references. Known scope
limits are explicit in the text. No unresolved substantive issue is known to
the author; five independent reviews must assess the frozen stage next.
