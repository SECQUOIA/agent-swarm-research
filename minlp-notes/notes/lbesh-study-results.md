# LB-ESH study results: generated and external experiments

The first complete primary run supports a modest, qualified advantage for
ESH within this implementation. On the 33 held-out generated instances,
ESH single-tree solves all 33 with either formulation; ECP solves 32 with
hull and 31 with big-M. On identical common-solved cohorts, ESH's wall-time
shifted geometric mean is 4–11% lower in the four formulation/tree pairs.
Hull versus big-M and single versus multiple trees have larger conditional
timing effects than the ESH/ECP choice. The two additional single-tree
repetitions retain every accepted-status outcome and the modest timing
advantage. The exact quadratic conic baseline is substantially faster than
the tested LB-ESH configurations on the supported quadratic controls.
The completed external set gives no ESH advantage in accepted solve counts,
and its small timing differences change direction with tree mode. The pilot ablations show that reduced NLP solves are important for this
prototype's incumbent recovery, while optional fractional user cuts add no
observed coverage benefit. Numerical cone references support the reported
bounds within their stated limits. Separate baseline followups recover valid
witnesses after changing a solver feasibility tolerance or initial values,
showing why the original interface failures cannot support broad algorithm
rankings. All declared data are complete; this note reports the evidence and
its limits rather than a publication-readiness verdict.

The held-out set contains related generated controls, not 33 independent
applications. Family laws share allocation data and sizes share prefixes.
The 18 pilot instances and the full 51-instance set are reported separately
below. No hypothesis test, confidence interval, or independence claim is made.

## Completed data and numerical audit

The primary file contains exactly 663 unique scheduled records: 51 instances
and 13 methods. The reviewed analyzer checked the entire saved schedule and
frozen executable provenance, then re-evaluated every supplied witness on a
fresh original GDP. It found no disagreements with the saved feasibility
checks and no reported bounds or infeasibility statuses contradicting another
validated feasible witness. This initial audit covers all primary methods. A subsequent combined audit
covers the primary, both repeats, and nine quadratic conic runs: 936 records,
again with no validation disagreements or cross-witness contradictions.
The final combined audit includes all 1,464 benchmark records, 42 continuous
cone roots, and 14 complete 27-assignment enumerations. It freshly validates
all 174 feasible fixed-assignment witnesses and returns zero warnings.

Across the 663 records, 550 meet the numerical solve rule, 106 have a valid
primal witness but an open or unusable numerical gap, six have invalid
witnesses, and one hits the whole-process wall limit. No outcome is dropped.
The six invalid witnesses are Gurobi big-M on every medium and large trig
instance: four held-out and two pilot cases. Their original disjunct cost
rows violate the common checker tolerance; the largest recorded violation
is approximately `8.07e-6`, against `1.1e-6` for those rows. They remain
failures in the original results. The separately declared tighter-feasibility
sensitivity includes all nine trig cases and is reported separately below.

An accepted result means a numerically feasible original-model witness and a
solver-reported usable global bound closing the declared numerical gap. It
is not an exact-arithmetic certificate. In particular, the mapped raw status
`optimal` appears in 603 records, exceeding the 550 accepted numerical solves.
The analysis uses original-model feasibility and numerical bounds rather
than treating that status string as an optimality proof. Native GAMS fields
and logs remain available in the raw artifacts.

All benchmark runs use a 120-second solver limit, 150-second whole-process wall cap,
one solver thread, and at most six concurrent workers. Wall time includes
startup, construction, initialization, and solver work. PAR10 charges each
unaccepted result 1500 seconds; a single failure therefore has a large effect
on a 33-instance mean. All values below are seconds unless specified otherwise.

## Held-out outcomes, with pilot and full-set context

| Method | Held-out numerical solves | Pilot numerical solves | All numerical solves | Held-out PAR10 mean |
|---|---:|---:|---:|---:|
| ESH hull single | 33/33 | 18/18 | 51/51 | 6.06 |
| ECP hull single | 32/33 | 17/18 | 49/51 | 50.79 |
| ESH hull multi | 30/33 | 17/18 | 47/51 | 140.43 |
| ECP hull multi | 30/33 | 17/18 | 47/51 | 141.22 |
| ESH big-M single | 33/33 | 17/18 | 50/51 | 11.16 |
| ECP big-M single | 31/33 | 17/18 | 48/51 | 97.72 |
| ESH big-M multi | 29/33 | 17/18 | 46/51 | 188.64 |
| ECP big-M multi | 29/33 | 16/18 | 45/51 | 190.38 |
| GDPopt LOA | 11/33 | 6/18 | 17/51 | 1000.87 |
| SHOT big-M | 22/33 | 11/18 | 33/51 | 514.34 |
| SHOT declared-convex epsilon hull | 24/33 | 14/18 | 38/51 | 414.72 |
| Gurobi big-M, original settings | 24/33 | 15/18 | 39/51 | 420.20 |
| SCIP big-M | 25/33 | 15/18 | 40/51 | 372.16 |

All unaccepted LB-ESH runs are feasible open-gap runs at the solver time
limit; none has an invalid witness. For the held-out baselines, the remaining
outcomes are 22 open-gap runs for GDPopt, 11 for SHOT big-M, nine for SHOT
hull, five open-gap plus four invalid-witness runs for Gurobi, and eight
open-gap runs for SCIP. The sole whole-process timeout is a pilot SCIP run.
The generated-suite results favor the tested LB-ESH configurations, but
shared generator structure, selected baseline formulations/settings, and the
separate external results below prevent a general solver-superiority claim.

The ESH/ECP timing comparison uses the same common-solved instances for both
methods, within one formulation and tree mode. The shift is one second:
`exp(mean(log(1 + wall_time))) - 1`. The ratio divides the two resulting means;
a ratio below one favors ESH. Conditional timing and full-set PAR10 answer
different questions and must be read together.

| Held-out pair | Common solved | ESH shifted mean | ECP shifted mean | ESH/ECP | ESH faster cases |
|---|---:|---:|---:|---:|---:|
| Hull single | 32/33 | 3.040 | 3.233 | 0.941 | 22/32 |
| Hull multi | 30/33 | 2.874 | 3.009 | 0.955 | 20/30 |
| Big-M single | 31/33 | 4.294 | 4.484 | 0.957 | 18/31 |
| Big-M multi | 29/33 | 4.991 | 5.591 | 0.893 | 21/29 |

On the pilot split, the respective ratios are 0.994 on 17 common solves,
0.970 on 17, 0.971 on 17, and 0.927 on 16. Pilot results are context, not an
additional independent confirmation of the held-out results.

Every ESH/ECP difference in accepted status across the full primary set is
listed here. ECP retains a feasible open gap at its limit in each case; there
are no primary cases with the opposite solved-status difference.

| Instance suffix | Split | Configuration | ESH accepted wall time | ECP wall time |
|---|---|---|---:|---:|
| `log.large.s130363` | Held-out | Hull single | 65.18 | 120.88 |
| `log.large.s130363` | Held-out | Big-M single | 113.67 | 120.79 |
| `log.large.s155921` | Held-out | Big-M single | 56.44 | 120.83 |
| `logsumexp.large.s104729` | Pilot | Hull single | 101.46 | 120.83 |
| `log.large.s104729` | Pilot | Big-M multi | 107.00 | 120.80 |

These are five method-instance outcomes on four instances. Several ESH
finishes are close to the limit; the additional repetitions below preserve
the held-out status differences.
In particular, the much larger single-tree PAR10 differences should not be
interpreted as comparable multiplicative speedups on commonly solved cases.

## Three-run held-out stability

The four single-tree configurations each have two further complete runs on
all 33 held-out instances. The solver seed is unchanged; job-order seeds
are 20260919, 20260920, and 20260921. These measure runtime variation across
three schedules on the same machine, not robustness to different solver
search seeds or new problem instances. No fastest-run selection is used.

Every one of the 132 method-instance combinations has the same accepted
category in all three runs. ESH solves all 33 with each formulation in each
run; ECP solves the same 32 hull and 31 big-M cases in each run. There are no
new invalid witnesses or contradictory bounds in the repeats.

| Single-tree method | Numerical solves, runs 1 / 2 / 3 | PAR10 means, runs 1 / 2 / 3 |
|---|---|---|
| ESH hull | 33 / 33 / 33 | 6.061 / 5.924 / 5.834 |
| ECP hull | 32 / 32 / 32 | 50.791 / 50.628 / 50.629 |
| ESH big-M | 33 / 33 / 33 | 11.164 / 10.868 / 10.649 |
| ECP big-M | 31 / 31 / 31 | 97.723 / 97.543 / 97.530 |

For a timing comparison with fixed membership across repetitions, require
both methods to solve the instance in all three runs. This gives the same
32 hull and 31 big-M instances as the primary common-solved cohorts.

| Formulation; fixed common count | Run 1 ESH / ECP means; ratio | Run 2 ESH / ECP means; ratio | Run 3 ESH / ECP means; ratio |
|---|---|---|---|
| Hull; 32 | 3.040 / 3.233; 0.941 | 2.983 / 3.138; 0.951 | 2.911 / 3.095; 0.941 |
| Big-M; 31 | 4.294 / 4.484; 0.957 | 4.141 / 4.377; 0.946 | 4.107 / 4.380; 0.938 |

The modest aggregate timing direction persists in these three schedules.
For individual instances, the median maximum/minimum wall-time ratio across
the three runs is 1.063 for ESH hull, 1.066 for ECP hull, 1.057 for ESH big-M,
and 1.059 for ECP big-M. The largest individual ratio is 1.239. These ranges
show meaningful runtime variability relative to small pairwise differences;
they are descriptive ranges, not confidence intervals or significance tests.
Multi-tree configurations were not repeated under this protocol, so their
primary timing differences do not receive this repetition evidence.

## Family, size, formulation, and tree effects

The next tables use only the held-out split. Cells give ESH/ECP shifted wall
mean ratios, followed by the common-solved count. The family table includes
all six families, and the size table includes all three sizes. No family or
size is selected on the basis of its result.

| Family; scheduled instances | Hull single | Hull multi | Big-M single | Big-M multi |
|---|---:|---:|---:|---:|
| Exp; 6 | 0.994 (6) | 0.944 (6) | 0.975 (6) | 0.871 (6) |
| Log; 6 | 0.883 (5) | 0.950 (4) | 0.972 (4) | 0.872 (4) |
| Logsumexp; 3 | 0.781 (3) | 0.857 (2) | 0.930 (3) | 0.864 (2) |
| Quadratic; 6 | 1.000 (6) | 0.989 (6) | 0.990 (6) | 1.003 (6) |
| Reciprocal; 6 | 0.922 (6) | 0.937 (6) | 0.894 (6) | 0.866 (5) |
| Trig; 6 | 1.016 (6) | 0.998 (6) | 0.982 (6) | 0.860 (6) |

| Size; scheduled instances | Hull single | Hull multi | Big-M single | Big-M multi |
|---|---:|---:|---:|---:|
| Small; 11 | 0.969 (11) | 0.959 (11) | 1.014 (11) | 0.987 (11) |
| Medium; 11 | 0.984 (11) | 0.952 (11) | 1.002 (11) | 0.889 (11) |
| Large; 11 | 0.877 (10) | 0.951 (8) | 0.865 (9) | 0.789 (7) |

The first repetition shows little ESH timing advantage on quadratic controls
and several near-ties or small reversals. Larger ratios of saved time appear
on some nonquadratic families and large instances, but the large-instance
common cohorts also omit more failures. These small dependent groups do not
establish that nonquadraticity or size causes an ESH advantage. In particular,
ESH is slightly slower for held-out trig hull single in this repetition.

The following contrasts keep the oracle fixed and again use identical
common-solved held-out cohorts. Their denominators differ from the oracle
comparisons above, so they are descriptive comparisons of the implementation,
not an additive decomposition of algorithmic effects.

| Contrast; ratio direction | ESH ratio (common count) | ECP ratio (common count) |
|---|---:|---:|
| Hull / big-M, single | 0.648 (33) | 0.652 (31) |
| Hull / big-M, multi | 0.508 (29) | 0.468 (29) |
| Single / multi, hull | 0.893 (30) | 0.866 (30) |
| Single / multi, big-M | 0.736 (29) | 0.676 (29) |

Hull has lower conditional wall time in each of these contrasts. Single-tree
also has lower conditional wall time and closes more held-out instances than
its multi-tree counterpart. This indicates that the overall architecture and
formulation are substantial parts of the observed result; the separator alone
does not account for the performance of the complete method.

## Recorded work on matched cohorts

Each cell below gives the arithmetic mean for ESH / ECP on the exact
common-solved held-out cohort from the corresponding timing pair. Every
listed metric is present for every member of its stated cohort. Means can
be influenced by a few difficult cases; medians and exact instance lists
are preserved in the accompanying `cohorts.json`.

| Configuration; common count | Cuts | LP iterations | Reduced NLP solves | Nodes | Cut-generation seconds |
|---|---:|---:|---:|---:|---:|
| Hull single; 32 | 877.9 / 940.0 | 41.1 / 45.5 | 16.09 / 20.88 | 231.3 / 291.7 | 0.1501 / 0.0226 |
| Hull multi; 30 | 477.9 / 507.6 | 35.1 / 38.5 | 5.93 / 6.50 | 1026.9 / 1279.0 | 0.0638 / 0.0098 |
| Big-M single; 31 | 1268.3 / 1419.7 | 44.0 / 58.0 | 24.94 / 28.97 | 592.7 / 652.9 | 0.2130 / 0.0348 |
| Big-M multi; 29 | 632.7 / 773.6 | 37.9 / 51.4 | 11.55 / 12.48 | 4253.9 / 4998.1 | 0.0888 / 0.0162 |

On these four cohorts, ESH generates approximately 6–18% fewer cuts and uses
fewer LP iterations, reduced NLP solves, and nodes in the arithmetic mean.
Its measured cut-generation time is approximately 5.5–6.6 times ECP's.
The data therefore show the anticipated cost tradeoff: more work inside the
radial separator accompanies less work elsewhere. This association does not
isolate a causal effect for each component, and a cut count alone would hide
the extra separation work.

The mean search and NLP savings are concentrated in cases with larger work
counts; they are not uniform across instances. In the hull single-tree
cohort, median nodes are 9 for ESH versus 8 for ECP, median reduced NLP solves
are 4.5 versus 4, and median recorded master time is 0.336 versus 0.290 seconds.
Hull multi-tree median nodes also reverse, at 14.5 versus 13.5, while median
NLP counts tie at two. Cut counts and LP iterations have lower medians for
ESH in all four pairs, but some search/NLP medians are tied or slightly worse.

Interior-NLP counts are identical within each paired cohort: mean counts
19.41, 17.97, 18.97, and 17.45, respectively. Their mean times are approximately
0.86–0.94 seconds per run. Matched ECP deliberately shares ESH's interior
initialization. These results compare separator choices within this code;
they do not measure an optimized standalone ECP implementation that could
omit that initialization.

Component times overlap. In single-tree mode, `time_master` includes callback
NLP and cut-generation work. None of the component times above or in the
artifacts is added into a timing decomposition. GDP root-search function
counts were not recorded, and the separate diagnostic's counts are not
imputed to these GDP runs.

All 33 held-out ESH hull LP phases finish with the recorded reason `stalled`,
for both tree modes. ECP hull records 30 `stalled` and three
`no_separating_cuts` exits. The largest recorded final perspective residuals
are approximately `1.20e-5` for ESH hull and `6.21e-6` for ECP hull. Each big-M
configuration records 32 stalled exits and one iteration-limit exit; its
perspective-residual field is not applicable. These LP phases are useful
initial outer approximations, but their exit reasons and residuals do not
establish hull feasibility or equality with a cone relaxation. The completed
same-hull continuous-cone comparison below addresses that separate numerical
question within the reference solvers' precision limits.

The [fixed-geometry oracle diagnostic](lbesh-oracle-diagnostic.md) supplies
an independently reviewed explanation of row-representation sensitivity and
root-search overhead. It also includes an off-center example with no cut
dominance. It is distinct from this GDP evidence and does not establish that
its selected geometry explains every benchmark outcome.

## Exact quadratic conic baseline

The separately scheduled exact bounded quadratic hull formulation with Gurobi
returns accepted numerical solves on all nine quadratic controls: six
held-out and three pilot cases. Here exactness describes the mathematical
reformulation; the returned solutions and bounds remain numerical.
Every LB-ESH configuration also solves these nine cases, so the following
wall-time comparisons use identical complete cohorts and need no failure
exclusions. They compare the primary LB-ESH runs with the separately
scheduled conic baseline; their end-to-end times include the respective
interfaces and initialization costs.

| Method | Held-out shifted wall mean, 6 cases | All quadratic shifted wall mean, 9 cases |
|---|---:|---:|
| Exact conic hull, Gurobi | 0.449 | 0.455 |
| ESH hull single | 2.283 | 2.280 |
| ECP hull single | 2.283 | 2.272 |
| ESH hull multi | 2.166 | 2.157 |
| ECP hull multi | 2.191 | 2.173 |
| ESH big-M single | 3.830 | 3.692 |
| ECP big-M single | 3.868 | 3.828 |
| ESH big-M multi | 4.240 | 4.285 |
| ECP big-M multi | 4.225 | 4.275 |

The conic formulation is the stronger practical choice in this comparison:
its all-nine shifted wall mean is roughly one fifth of ESH hull single's.
Thus the primary table's advantage over generic baseline formulations does
not extend to this supported exact conic alternative. The study does not
establish that the conic formulation is faster on every quadratic GDP, nor
that a conic translation exists for every nonquadratic row. The completed
continuous cone reference has a different role: it compares relaxation
bounds for supported formulations rather than competing as a mixed-integer
solver. In particular, an LP-versus-cone hull comparison must use the same
hull target; a big-M versus hull difference includes a structural relaxation
difference.

## External legacy set and input scope

The complete external schedule contains all 351 runs: 27 historical models
and 13 methods. The combined audit of generated runs, repetitions, quadratic
controls, and this external set covers 1,287 records with no validation
disagreements or cross-witness bound/status contradictions. The original
external outcomes remain visible: 239 numerical solves, 38 feasible open-gap
runs, four invalid witnesses, 61 errors, seven runs without a witness, and
two explicitly unsupported conic inputs. These counts concern the original
scheduled interfaces, before the separate initialization followup.

Apply the frozen differentiability and adapter contracts to the model
expressions, rather than selecting successful runs. All six constrained-layout
`l2` models contain Euclidean-norm objectives that are nonsmooth at zero.
They form one stress stratum, including the two that happen to solve with
LB-ESH. The other 21 models form the stratum without these norm objectives;
this label does not itself prove every theoretical assumption. The conic
adapter supports 25 legacy models and explicitly excludes
`gdplib.batch_processing` and `gdplib.small_batch`, whose exponential rows
are outside that adapter's scope. There are 19 models in the intersection
of the conic-supported and no-norm strata. Membership is fixed by these
expressions and scope rules, not by observed winners.

| Method | All numerical solves / 27 | Without norm objectives / 21 | Norm-objective stress / 6 | Original errors |
|---|---:|---:|---:|---:|
| ESH hull single | 19 | 17 | 2 | 4 |
| ECP hull single | 19 | 17 | 2 | 4 |
| ESH hull multi | 20 | 18 | 2 | 4 |
| ECP hull multi | 20 | 18 | 2 | 4 |
| ESH big-M single | 20 | 18 | 2 | 4 |
| ECP big-M single | 20 | 18 | 2 | 4 |
| ESH big-M multi | 20 | 18 | 2 | 4 |
| ECP big-M multi | 20 | 18 | 2 | 4 |
| GDPopt LOA | 12 | 12 | 0 | 8 |
| SHOT big-M | 16 | 12 | 4 | 7 |
| Gurobi big-M | 12 | 12 | 0 | 7 |
| SCIP big-M | 19 | 13 | 6 | 7 |
| Exact supported conic formulation | 22 | 17 | 5 | 0 |

The conic row has two unsupported inputs among the 21 no-norm models;
its supported-scope count is 22/25, not 22/27. Its other unaccepted outcomes
are two feasible open-gap farm cases and one invalid witness on
`CLay0204.l2`, with original linear distance-row violations. The invalid
conic witness is rejected even though its solver status is `optimal`.

Four norm-objective models trigger the same nonfinite-gradient error in
every LB-ESH configuration: `CLay0204.l2`, `CLay0205.l2`, `CLay0304.l2`,
and `CLay0305.l2`. `CLay0203.l2` and `CLay0303.l2` solve, but remain in
the same nonsmooth stress stratum. GDPopt has Ipopt failures on all six
norm-objective models and subproblem-status errors on the two batch models.
These are limitations of the tested differentiable implementation/interfaces;
their errors do not establish infeasibility of the original models.

All seven farm inputs produce writer division-by-zero errors in each of the
three original GAMS big-M interfaces, accounting for 21 errors. All three
GAMS methods also return incomplete batch-processing witnesses, because the
unused original variable `storageTankSize_log[10]` remains undefined. The
common full-witness rule rejects those three records. This makes a direct
ranking of the original full-set PAR10 values misleading as a statement about
solver search performance. The separate followup declares all seven farms
plus batch processing, crossed with the three GAMS methods: 24 new records
with explicit initial values and unchanged algebra, bounds, solver options,
and validation. It will not replace these original interface outcomes.

ESH and ECP have the same accepted solve count in every matched external
configuration. Their common-solved timing differences are small and mixed.
The following pairs remove all six norm-objective models by expression-based
scope, including the successful ones; the full-set ratios are retained in
the artifacts.

| Configuration | Common solved, no-norm stratum / 21 | ESH shifted wall mean | ECP shifted wall mean | ESH/ECP |
|---|---:|---:|---:|---:|
| Hull single | 17 | 2.575 | 2.537 | 1.015 |
| Hull multi | 18 | 3.139 | 3.238 | 0.969 |
| Big-M single | 18 | 2.976 | 2.946 | 1.010 |
| Big-M multi | 18 | 2.267 | 2.341 | 0.969 |

Thus the generated-suite accepted-count advantage does not extend to the
external set. On common externally solved cases, single-tree ESH is slightly
slower and multi-tree ESH slightly faster in this one run. The protocol does
not repeat the external set, and differences of this size should not be
called robust speed improvements.

On the 19 models within both no-norm and conic-adapter scope, all eight
LB-ESH/conic timing comparisons share the same 17 commonly solved cases.
The conic shifted mean is 0.928 seconds; the eight LB-ESH means range from
2.225 to 3.255 seconds. Conic/LB-ESH ratios therefore range from 0.285 to
0.417 on those common cases. This is conditional timing, not dominance in
coverage: the conic formulation leaves `FLay05` open, while several LB-ESH
configurations solve it; `FLay06` remains open. Unsupported exponential
models and nonsmooth stress cases are not used to manufacture a conic
failure penalty in this supported-scope speed comparison.

## Pilot ablations

All 144 declared pilot ablation runs are complete: 18 pilot instances, the
four single-tree configurations, and two separate changes. The default
comparisons use those same 18 primary pilot instances. This is a secondary,
unrepeated study on the pilot split, not a new held-out test.

| Single-tree configuration | Default numerical solves / 18 | Without integer-point NLPs / 18 | Fractional user cuts enabled / 18 |
|---|---:|---:|---:|
| ESH hull | 18 | 1 | 18 |
| ECP hull | 17 | 0 | 17 |
| ESH big-M | 17 | 0 | 17 |
| ECP big-M | 17 | 0 | 17 |

The integer-point-NLP ablation has zero reduced NLP solves, but still performs
369 interior NLP solves across each configuration's 18 cases. It is not an
algorithm without NLP work. Across its 72 records there are 62 `stalled`
statuses, nine time limits, and one accepted numerical optimum. Of the stalled
runs, 53 have no accepted incumbent and nine have a validated incumbent but
an open gap. All nine time-limit runs lack an accepted incumbent. The sole
accepted case is ESH hull on `lbesh.log.small.s104729`. None of the 72 records
is an interface error or an invalid returned witness; failure to produce an
accepted incumbent remains an unsuccessful outcome.

These results show that integer-point NLP recovery is practically important
in this frozen implementation. They do not establish that convex GDP
algorithms mathematically require NLP subproblems. Nor do the retained logs
identify the rejected candidate and cut history for every stall, so the data
do not justify attributing every failure to one numerical tolerance. Fast
early stalls must not be presented as runtime improvements. The default
versions solve 69 of the corresponding 72 pilot runs. The separate
[solver-free diagnosis](lbesh-nonlp-ablation-diagnosis.md) records what the
retained states and implementation can establish about these failures.

Fractional user cuts are actually generated in the enabled ablation. Counts
below are the recorded cuts submitted through that callback, over all 18
scheduled instances. Timing uses the identical common-solved default/variant
cohort; the ratio is user-cuts-enabled / default.

| Configuration | Common solved | User-cuts/default shifted wall ratio | Recorded user cuts | Instances with user cuts / 18 |
|---|---:|---:|---:|---:|
| ESH hull | 18 | 1.000 | 1,763 | 17 |
| ECP hull | 17 | 1.006 | 1,487 | 18 |
| ESH big-M | 17 | 1.006 | 16,435 | 18 |
| ECP big-M | 17 | 1.016 | 17,864 | 18 |

There is no accepted-count gain and no persuasive timing benefit in this
pilot comparison. The additional cuts therefore do not justify a claim that
the optional fractional callback improves the tested default. Small timing
differences across these separately scheduled batches remain descriptive.

## Same-hull cone roots and exhaustive small references

All 42 supported generated continuous hull roots and all 14 small
fixed-assignment enumerations have been computed with the separate cone
implementation. Trig has no supplied cone translation and is explicitly
outside this reference set. The cone model represents the same bounded
hull target as the LB-ESH hull LP; no big-M bound is compared as if its
structural relaxation difference were an oracle approximation error.

Clarabel reports `optimal` for 40 roots and `optimal_inaccurate` for two.
For the 40 `optimal` roots, define the diagnostic quantity

`(cone dual estimate - LP bound) / max(1, abs(cone primal objective))`.

It compares floating-point values and is not a certified distance to the
exact hull optimum. The recorded primary LP bounds are identical across
single and multi-tree modes for each oracle on every supported instance,
so those duplicated LP phases are not treated as extra observations.

| Hull separator; 40 optimal-status references | Minimum normalized difference | Median | Maximum | Absolute normalized difference at most 1e-4 |
|---|---:|---:|---:|---:|
| ESH | 1.43e-7 | 1.10e-6 | 1.32e-4 | 39/40 |
| ECP | 4.69e-8 | 1.07e-6 | 2.78e-4 | 39/40 |

The largest difference for each separator is the pilot
`lbesh.logsumexp.large.s104729`. All 40 differences are positive. This is
numerical consistency with an outer approximation; it does not make stalled
or capped LP phases hull-feasible, prove equality, or certify their bounds.
The close median values also do not support uniform superiority of one
separator's final LP bound.

The two inaccurate-status roots are retained separately. For
`lbesh.log.medium.s104729`, the cone primal and dual residuals are
`5.83e-10` and `2.63e-9`, with absolute cone primal/dual gap `1.67e-7`.
For `lbesh.reciprocal.large.s104729`, they are `7.20e-11` and `8.82e-10`,
with gap `1.92e-7`. Their raw ESH/ECP LP comparisons remain in the artifact,
but they do not enter the 40-root precision summary or become certified
references. Even the 40 optimal-status cone duals remain uncertified
floating-point estimates.

Each of the 14 small enumerations contains all 27 distinct assignments.
Across 378 fixed-assignment solves, 174 report optimal and 204 report
infeasible, with no unresolved assignments. All 174 returned feasible
witnesses pass fresh original-model validation, also confirmed by the
independent data reviewer. Every one of the 182 accepted primary results
on these 14 instances agrees with its enumeration's best feasible objective
within the declared comparison tolerance. The largest discrepancy uses
approximately 1.32% of that tolerance. This supplies independent numerical
support from a different formulation and solver. It is not an exact
infeasibility certificate for the other assignments or an exact optimum
certificate for the enumeration.

## Separate baseline followups

Both followups were declared after the original source freeze in response to
observed interface or feasibility problems. Their scopes were fixed before
execution: all nine trig cases for the tolerance change, and all eight
affected legacy models with each of the three GAMS solvers for initialization.
They are separate supplementary studies. No followup replaces an original
record or enters a best-of-two method result.

For the nine trig instances, changing only Gurobi's `FeasibilityTol` to
`1e-8` produces nine original-model-valid witnesses, compared with three in
the original batch. The three medium cases also close the declared numerical
gap, raising accepted solves from three to six. All three large cases remain
valid but open at the 120-second solver limit. The complete paired timing
table shows mixed timing changes; it is not a general speedup claim.

| Trig size / seed | Original outcome | Tighter-tolerance outcome | Original wall seconds | Followup wall seconds |
|---|---|---|---:|---:|
| small / 104729 | solved | solved | 1.267 | 1.724 |
| small / 130363 | solved | solved | 26.833 | 1.267 |
| small / 155921 | solved | solved | 1.318 | 1.670 |
| medium / 104729 | invalid witness | solved | 5.677 | 4.980 |
| medium / 130363 | invalid witness | solved | 10.843 | 14.960 |
| medium / 155921 | invalid witness | solved | 8.338 | 3.775 |
| large / 104729 | invalid witness | feasible, open gap | 121.556 | 121.345 |
| large / 130363 | invalid witness | feasible, open gap | 121.532 | 121.297 |
| large / 155921 | invalid witness | feasible, open gap | 121.435 | 121.871 |

The legacy followup changes only initial values: farm widths start at their
existing positive affine lower bounds, and an unused trailing batch storage
variable starts at its existing bound. Model algebra, declared bounds, solver
options, and validation tolerances remain fixed. The original 24 records
contain 21 writer errors and three invalid incomplete witnesses. Initialization
allows all 24 solver calls to return, yielding 23 valid witnesses and 11
accepted numerical solves. This diagnoses substantial interface sensitivity.

| Initialized GAMS baseline | Scheduled | Valid witnesses | Numerical solves | Feasible, open or unusable gap | Invalid witnesses |
|---|---:|---:|---:|---:|---:|
| Gurobi big-M | 8 | 7 | 4 | 3 | 1 |
| SCIP big-M | 8 | 8 | 7 | 1 | 0 |
| SHOT big-M | 8 | 8 | 0 | 8 | 0 |

The remaining invalid witness is Gurobi on `FLay05`, with an active nonoverlap
row residual about `7.94e-6` against `1.1e-6`. The numerical solve counts
also retain the declared interface limitation: for batch processing, Gurobi's
native log reports objective `679365.3263389`, bound `679307.9309222`, and
gap `0.0084%`, but GAMS exports `OBJEST=NA`. The unchanged gate therefore
does not accept a closed gap from that record. This is missing interface
bound information despite a native closed-gap report, not evidence of a
solver failure to close its gap. No native-log value is substituted into the
declared result. SHOT's normal termination on several farm cases likewise
does not imply a closed gap: retained logs identify its default nonconvex
classification and loose bounds. This followup does not change that option.

Fresh independent reviews checked the native GAMS statistics, solver options,
source and plan hashes, and original-model witnesses for
[all nine tolerance pairs](lbesh-review-gurobi-sensitivity.md) and
[all 24 initialization pairs](lbesh-review-legacy-initialization.md).
The native versions are GAMS 54.3.1, Gurobi 13.0.2, SCIP 10.0.3, and
SHOT 1.1, git `a81275b4`. SHOT's initialization-wrapper version field is
null because of a parser limitation; the retained log identifies the version.
These followups qualify the original baseline rankings without changing the
matched ESH/ECP comparison.

## Reproduction and artifacts

Run from `code/minlp_solver_lab`; the following completed command revalidated
all 663 primary records and returned zero audit warnings:

```bash
.venv/bin/python lbesh_study_analysis.py \
  results/lbesh_development/main_generated_v1.jsonl \
  --primary results/lbesh_development/main_generated_v1.jsonl \
  --out results/lbesh_development/analysis_primary_v1 \
  --oracle-diagnostic results/lbesh_development/oracle_diagnostic.json \
  --plots
```

The complete primary-plus-repetitions export (663 primary and 2 x 132
repetition records, without the later conic batch) is preserved separately
in `analysis_repeats_v1`. After the quadratic conic batch completed, the following
combined command revalidated all 936 records, again returning zero warnings:

```bash
.venv/bin/python lbesh_study_analysis.py \
  results/lbesh_development/main_generated_v1.jsonl \
  results/lbesh_development/repeat_heldout_v1_r2.jsonl \
  results/lbesh_development/repeat_heldout_v1_r3.jsonl \
  results/lbesh_development/quadratic_conic_v1.jsonl \
  --primary results/lbesh_development/main_generated_v1.jsonl \
  --out results/lbesh_development/analysis_repeats_conic_v1 \
  --oracle-diagnostic results/lbesh_development/oracle_diagnostic.json \
  --plots
```

The output directory is preserved; use a new name for a replay. Primary raw
SHA-256 is `42500b65dc585d4652b13bd925ebf7f3f55c8d17a2e6b30caf07d99341af0a0d`.
The primary and repetition/conic export analyzer SHA-256 is
`96c0ca65fe6f7f0f1fd771202d8065d7537adef794d6e63cbc08835cc5e2899a`.
The full output records the schedule hash, frozen source/plan hashes,
environment versions, exact command, and complete denominators.

- [Audited analysis JSON](../code/minlp_solver_lab/results/lbesh_development/analysis_primary_v1/analysis.json)
  and adjacent CSV files preserve all statuses, witnesses' validation issues,
  per-run telemetry, stratified summaries, and matched ESH/ECP comparisons.
- [Matched-cohort statistics](../code/minlp_solver_lab/results/lbesh_development/analysis_primary_v1/cohorts.json)
  preserve every instance membership, mean, median, and structure contrast
  used in this note. Reproduce these descriptive queries with
  `.venv/bin/python results/lbesh_development/analysis_primary_v1/derive_cohorts.py`.
  The query script consumes the audited table without changing validation
  decisions and records its own and its input's hashes.
- [Repetition and quadratic-context statistics](../code/minlp_solver_lab/results/lbesh_development/analysis_repeats_conic_v1/stability_context.json)
  preserve the fixed three-run cohorts, every instance's three times and
  statuses, and quadratic comparisons with all primary methods. Reproduce
  them with
  `.venv/bin/python results/lbesh_development/analysis_repeats_conic_v1/derive_stability_context.py`.
  The combined `analysis.json` and adjacent `repetitions.csv` preserve all
  individual audited outcomes and input hashes.
- [Legacy scope statistics](../code/minlp_solver_lab/results/lbesh_development/analysis_legacy_v2/legacy_scope.json)
  preserve all scope memberships, outcome categories, and matched comparisons.
  Reproduce them with
  `.venv/bin/python results/lbesh_development/analysis_legacy_v2/derive_legacy_scope.py`.
  The complete legacy-inclusive command, input hashes, and 1,287 audited rows
  are in the adjacent `analysis.json`. Its analyzer hash is
  `3c207d4c570fe77a65b844f7fb5a5649f7a073755e58579bccbd04ed4db011da`.
  This independently reviewed update fixes CSV serialization of missing LP
  reasons and accepts the separately declared initialization wrapper; it does
  not alter solver runs or numerical assessments. The incomplete first export
  `analysis_legacy_v1` is retained and explicitly marked; use `v2` for tables.
- [Ablation and reference statistics](../code/minlp_solver_lab/results/lbesh_development/analysis_planned_v1/ablations_references.json)
  preserve all pilot cohorts, callback counts, root statuses/residuals, and
  enumeration objective comparisons. Reproduce them with
  `.venv/bin/python results/lbesh_development/analysis_planned_v1/derive_ablations_references.py`.
  The adjacent `analysis.json` audits all 1,431 originally planned benchmark
  records plus the frozen references, with `--require-complete-study` and
  zero warnings; it records the complete command and hashes.
- PDF, SVG, and PNG exports include primary outcomes, full-set family timing,
  and the separate oracle diagnostic. These primary figures use all 51
  instances; the held-out-only numbers leading this note are the tables above.

The final [complete analysis](../code/minlp_solver_lab/results/lbesh_development/analysis_v1/analysis.json)
contains all eight benchmark files, all 1,464 records, and both reference
files, with `--require-complete-study`, zero warnings, and the reviewed
`3c207d4c570fe77a65b844f7fb5a5649f7a073755e58579bccbd04ed4db011da`
analyzer. Its `command` field preserves the exact invocation; the same
complete command is in [the research README](../code/minlp_solver_lab/LBESH_RESEARCH.md).
The final output includes the CSV tables and PDF/SVG/PNG figures. Earlier
stage exports remain intact.

The unchanged legacy, ablation/reference, and repetition query scripts were
copied to `analysis_v1` and rerun on that final analysis. Their outputs are
`legacy_scope.json`, `ablations_references.json`, and `stability_context.json`.
The new [followup paired table](../code/minlp_solver_lab/results/lbesh_development/analysis_v1/followups.json)
and adjacent `followups.csv` preserve all 33 paired records, including failures,
objectives, bounds, times, and original-model residual assessments. Reproduce
it from the lab with
`.venv/bin/python results/lbesh_development/analysis_v1/derive_followups.py`.
Each derived query records its own source hash and the final analysis hash.
No analysis step performed optimization, project-wide checks, or CI inspection.
