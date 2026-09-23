# Independent review of the reopened network–simplex experiments

Date: 2026-09-07. Reviewer: independent subagent `/root/review_benchmarks`.

## Scope and verdict

This review covers `code/network_simplex_benchmarks/baselines.py`,
`code/network_simplex_benchmarks/run.py`, their recorded experiments, and the
computation note when available. The benchmark author did not write this review
or its additional verification script.

The three inspected LP formulations are mathematically consistent on the
generator's supported graph class. The present evidence supports an exact-hull
implementation and substantial formulation-size reduction. It does not support
a computational advantage of original-variable cutting planes over the
compressed extended formulation. In the original six-case recorded run, the
compressed EF is the fastest exact optimizer in every case. This negative
finding should remain part of the computational account.

## Formulation audit

The full EF uses one nonnegative flow for each explicit simplex state and the
residual state. Its flow equations and capacities are scaled by the state
weight. Summing those flows recovers the original flow, and observed products
are selected flow coordinates. Both original-flow and observed-product costs
are transferred to those coordinates correctly; explicit simplex costs remain
on the original simplex variables.

The metadata-based compressed EF retains the original flow, simplex, and
observed-product variables. For each observed state in a parallel-path block,
it uses one fewer independent path coordinate than the number of paths. The
last coordinate is the negative sum of the others. State interval bounds are
scaled by their weights; residual bounds are imposed on aggregate path
coordinates minus the observed-state coordinates. The reference-flow offsets
and arc-orientation signs in these bounds and observation equations are
correct. Unobserved states can share the normalized residual block flow.
Observed bridge products equal the bridge's fixed reference flow times the
state weight. The generator supplies a feasible reference and correct block
metadata; this baseline itself is not a general graph recognizer.

The McCormick baseline contains the four scalar-envelope inequalities (one as
the nonnegative product-variable bound), network balance, arc capacities, and
the simplex constraint. Its weaker objectives are therefore a meaningful
baseline for the same original variables and objective. Fixed simplex
coordinates are ordinary external affine constraints imposed consistently on
all compared models.

## Independent numerical verification

Command:

```sh
python code/network_simplex_review/check_benchmark_baselines.py
```

The independent script uses seeds 901–930 and four simplex regimes per seed:
free weights, all explicit weights zero, a simplex vertex, and random fixed
weights. It varies path length from one to four, paths per block from two to
six, and blocks from one to three. Observation patterns include empty
observations, all arc–state pairs, bridge observations, and sparse repeated-path
observations. Objectives include nonzero coefficients on simplex variables,
which the main benchmark does not use.

After the author's generator correction, all 120 support comparisons between
the full EF, metadata-based compressed EF, and general compressed EF passed.
The maximum absolute objective difference was `4.973799150320701e-14`.
All 360 recovered optimizers passed an independent full-EF membership LP and
all 360 passed general-compressed membership. Original objective
reconstruction agreed within `1e-7`, and McCormick objectives never exceeded the
hull objectives by more than `1e-7`. Auxiliary-variable counts agreed with
`sum_B (number_of_paths_B - 1) * number_of_observed_states_B`.

For general-compressed membership of numerical optimizers, the review adapter
snaps only bound violations below `1e-7` to the bound before the check. One
metadata-EF optimizer returned `2.0000000000000004` on an arc of capacity 2;
the general model correctly rejects this coordinate under its strict rational
domain check. This is a numerical-to-exact interface limitation, not a hull
counterexample. Balance and observation equations are still checked by the
membership LP. The benchmark's constructed membership points use exact
fractions and do not require this adapter.

These checks provide numerical regression evidence. They do not replace the
mathematical equivalence proof.

## Timing and claim boundaries

The initial inspected runner omitted `OriginalLP` construction, rational
reconstruction, and cut insertion from its reported cutting-plane component
sum, while the full and compressed EF timers included assembly. This was
reported to the author and corrected. The revised component sum includes
original LP construction, point reconstruction, and cut conversion/insertion,
in addition to preprocessing, LP solves, and separation. Independent cut-support
LPs and decomposition audits are deliberately excluded. Minor loop bookkeeping
is not measured, so this is a sum of selected implementation components.

Every generated cut is checked against a separately assembled full EF using a
floating-point LP support optimization with tolerance `1e-7`. The separator's
arithmetic and returned decomposition checks use exact fractions. Calling the
support LP audit itself an exact certificate would overstate the evidence.
Rational reconstruction of numerical LP iterates is deliberately fail-fast:
the runner checks proximity and exact network balance. This is a benchmark
adapter, not a general robust numerical-to-rational reconstruction procedure.

The original membership experiments compared the separator only with the
uncompressed full EF. The author added the general compressed model to both
optimization and membership, including its own preprocessing. The final
membership comparison shows no consistent advantage over that compressed LP.
Reported CSR array storage is not peak process or solver memory. Fixed seeds
make instances and objective values reproducible; individual timings remain
machine- and load-dependent.

All instances are synthetic chains of parallel-path blocks. The optimization
experiments have no outer mixed-integer model or application linking rows
beyond fixed simplex weights. With free simplex weights, linear optimization
over this standalone hull admits a simplex-vertex optimizer. Consequently,
these are implementation and formulation comparisons, not evidence of
industrial solver speedups or representative application difficulty.

## Final-snapshot review

The revised runner and `notes/network-simplex-reopened-computation.md` were
reviewed after the timing correction, generator random-stream separation, and
general compressed solver integration. The recorded six-case run has 85 cuts,
including 23 transportation-subset cuts; its objective values, row counts, and
reported membership comparisons match the computation note. The compressed
formulations remain faster than the cut loop in all six optimization cases.

An independent rerun of the quick benchmark passed both optimization cases and
both membership cases. Its record is
`code/network_simplex_review/benchmark-review-quick.json`. Timing fluctuations
are expected and are not presented as failures to reproduce the results.

No unresolved mathematical model-equivalence or substantive benchmark-accounting
issue was found within this scope. The independent general-solver integration
checks cover generated parallel-path graphs; review of that solver on arbitrary
graphs belongs to its separate implementation review.

## Independent review of the five-repetition study

The same reviewer subsequently inspected `repeats.py`, the timing instrumentation
added to the LP baselines and general compressed model, the five-run
`repeated-results.json`, and the computation note's observed-rank section.
The study is accepted as a descriptive comparison of these synthetic instances.

The repeated optimization uses precisely the same seed, graph parameters,
objective RNG, objective ordering, and fixed weights as the largest original
case. Both general compressed models receive the same objective and bounds.
The original version is selected by the default `eliminate_observed=False`;
the additional version passes `True` explicitly. Membership uses the same exact
constructed point for all four methods. Each case has an unrecorded warmup,
followed by five recorded complete constructions and solves. Membership order
rotates; optimization method order is fixed. The latter is a limitation for
fine timing comparisons, but does not invalidate the stated descriptive ranges.

Both general compressed timers include symbolic preprocessing and, where
selected, observed-coordinate elimination. Their numerical assembly timers
include objective and bound conversion as well as matrix creation; the engine
timer surrounds the HiGHS call. Full-EF assembly and solve are timed similarly.
Total timers include result adaptation. The cutting total includes preprocessing,
original LP construction, all 43 LP solves, all 43 separator calls, rational
reconstruction, and cut insertion. The distinction between component sums and
literal wall time remains explicit. No substantive direct computation phase is
omitted from the claimed comparison.

The largest case's 42 cuts receive a fresh numerical full-EF support audit before
the repetitions. Disabling these independent audit solves during repeated
measurements is appropriate: they are verification overhead, not part of the
separation algorithm. Every repetition still checks objective agreement and its
final exact decomposition; the eliminated formulation's optimizer is separately
reconstructed and checked with the exact separator. The saved repeated runs
all have 42 iterations and consistent cut-family counts.

The reviewer recomputed all 74 reported median/minimum/maximum summaries from
the individual runs, checked five runs per case, nonnegative timing components,
build-component identities, formulation sizes, and the once-only audit count.
Every check passed. The computation note's tables match the saved summaries.
Auxiliaries decrease from 48 to 15 for optimization and from 60 to 29 for
membership, as claimed.

An independent execution also passed:

```sh
python code/network_simplex_benchmarks/repeats.py --repetitions 1 \
  --output code/network_simplex_review/repeated-review-one-run.json
```

This includes all three membership sizes, the fresh 42-cut full-EF support
audit, warmups, and the largest optimization comparison. The optimizer result
agrees across formulations and has an exactly verified decomposition. The
separate record preserves the published five-run data unchanged.

The practical conclusions are correctly limited: initial general compression
has median optimization time 6.35 ms versus 193.58 ms for full disaggregation
and 278.21 ms for cutting; observed-coordinate elimination reduces model size
but increases median total time to 7.62 ms. Elimination also fails to improve
median total membership time in the three recorded cases. Large timing ranges
at 1,024 states demonstrate environmental variability; five repetitions are
not a statistical performance study or evidence of application-scale speedups.
There is no unresolved substantive issue in the repeated-study accounting or
the reported negative elimination-runtime result.

## Independent review of the fixed-two-state flat-chain study

The reviewer additionally inspected `flat_repeats.py`, its full-EF and general
compressed adapters, and the computation note's final flat-chain section. This
study concerns a different graph class from the parallel-path-block benchmarks.
Its full-EF comparator is especially important: with two explicit states,
disaggregation already has size linear in the number of gadgets.

The input construction is correct. For the feasible point, weighted state
branch flows are both `1/4`, and opposite arc allocations sum to the specified
aggregate `1/4` on each arc. The selected observations agree with those state
allocations. For the outside point, observations alternating between states
force each weighted branch flow to be at least `3/10`, contradicting aggregate
branch flow `1/2`. Every individual observation satisfies its McCormick
inequalities. The same exact rational point, observations, unit capacities, and
unit-flow balances reach all four implementations; incidence conventions are
adapted consistently.

An initial acceptance check treated every unsuccessful LP solve as outside.
The reviewer requested explicit infeasibility status to exclude numerical or
iteration failures. The author corrected this: all three LP methods require
status 2 on outside cases and record their statuses. The full five-repetition
study was rerun after that correction.

The timing comparison includes every substantive requested computation phase:
fresh constructors for all methods; symbolic elimination where enabled;
numerical matrix, objective, and bound conversion; the LP solve; and exact
online separation. The cold 41-circuit library cost is recorded separately
before warmups. The first feasible warmup records the first decomposition call,
which includes lazy profile-basis construction. Five subsequent repetitions
use these cached state-dimension libraries. Method order rotates. Exact
separation without decomposition and separation with decomposition are measured
as separate calls; no difference of noisy measurements is called an isolated
decomposition cost. Exact certificate audits and once-only numerical cut-support
LPs are deliberately outside the selected timing components.

Independent selected-length reproduction:

```sh
python code/network_simplex_benchmarks/flat_repeats.py --lengths 8 128 \
  --repetitions 1 --output code/network_simplex_review/flat-review-one-run.json
```

All four selected cases passed after the explicit-status correction, including
outside statuses, numerical full-EF support audits of returned cuts, and exact
decomposition audits on feasible points. The saved one-run record is separate
from the author's five-run data.

The interpretation is appropriately limited. The exact flat oracle can reduce
construction-plus-solution time on these few-state controlled patterns, while
the full-EF compiled solve can be faster than exact online separation after
matrix construction is excluded. This comparison does not establish an
advantage over a persistent LP, native callbacks, or representative application
instances. Both feasible/outside patterns use two nonzero explicit weights and
a zero residual weight; they are not broad coverage of the state-weight domain.

Final-record acceptance: the reviewer recomputed all 136 summary records from
the refreshed five-run JSON, checked all 120 LP statuses, all eight Markdown
table rows, build/total timing identities, and all four cut-support audits.
Every check passed. The recorded cold circuit-library cost is 22.32 ms. For
512 feasible gadgets the median totals are 83.63 ms for full EF, 108.38 ms for
initial compression, 433.36 ms after observed-coordinate elimination, and
18.83 ms for the exact flat oracle (22.20 ms with decomposition). The full LP
engine takes 11.05 ms versus 18.21 ms for exact online separation, confirming
the stated limitation of the construction-plus-solution advantage. The final
study is accepted; no substantive model-equivalence, verification, or timing
accounting issue remains within this review's scope.
