# Convex GDP supporting-hyperplane development

Started 2026-09-19. Scope: develop and independently verify this topic for a
publication; do not write the paper. The prior method and benchmark notes are
historical evidence, not an accepted publication package.

## Decisions and acceptance criteria

1. Identify the contribution relative to perspective cuts, ESH, logic-based
   outer approximation, disjunctive cut strengthening, and conic GDP methods.
   A new acronym or an unsuccessful literature search does not establish
   novelty. Negative computational findings remain in the record.
2. State complete assumptions and proofs for all theoretical claims. Separate
   exact-arithmetic claims from numerical solver contracts and tolerance-based
   feasibility/optimality.
3. Repair extraction, separation, incumbent, and termination behavior before
   freezing experimental code. Unsupported inputs must be refused explicitly.
4. Predeclare controlled instances and held-out seeds. Compare cut policies
   within the same solver, and include established solvers and exact conic
   hulls where applicable. Report preprocessing, failures, timeouts, and paired
   results; independently validate original-model primal witnesses.
5. Have fresh agents review final theory, implementation, and experimental
   interpretation. Address findings and rerun affected targeted checks.
6. Produce a reproducible research package and a claim/evidence ledger. Judge
   publication readiness from the resulting evidence, not the initial plan.

## Work allocation

- Theory author: full convergence contracts, perspective-cut identity,
  fractional separation residuals, and correction of old proof statements.
- Implementation author: original `lbesh` package and contract regressions.
- Literature investigator: primary-source comparisons and claim boundaries.
- Instance author: deterministic nonquadratic GDP families and witnesses.
- Benchmark author: fresh-process harness, independent primal validation,
  raw records, and unbiased summaries.
- Conic baseline author: exact quadratic hull implementation and equivalence
  checks.
- Coordinator: environment/licensing, experiment scheduling, integration,
  result interpretation, and later independent-review assignments.

Authors are not the final independent reviewers of their own work.

## Resource and environment policy

The machine exposes 36 logical CPUs and about 30 GiB RAM. At the initial
inspection about 23 GiB was available; other work is running on the machine.
Use one solver thread per run, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
and `MKL_NUM_THREADS=1`. Broad experiment batches initially use at most six
workers. Reassess available memory before large batches. Do not run repository
wide verification or inspect CI logs.

Use the existing solver-lab environment and committed `uv.lock`:

```sh
cd code/minlp_solver_lab
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH \
uv run --frozen --no-sync python -m lbesh_research.environment \
  --out results/lbesh_development/environment.json
```

Executed successfully: the direct Gurobi API and GAMS SHOT, SCIP, Gurobi,
and BARON solved their probe problems; Ipopt also solved its continuous probe.
The nonlinear probe has the known optimum `-log(2)` and all returned points
passed the explicit numerical feasibility/objective check. Dependency
versions, platform, executable paths, baseline commit, and lockfile hash are
recorded in the output. License credentials and identifiers are not recorded.

## Early findings

- LB-ESH's affine cuts are perspective outer-approximation cuts; their
  validity is not a new cut-family result.
- The old 27-instance benchmark has nonlinear disjunct rows in 18 instances,
  all quadratic. The new study must exercise nonquadratic disjunct rows.
- The historic scorer counts a below-consensus objective as solved. Correct
  scoring alone is insufficient: historic records do not retain independent
  original-model feasibility evidence.
- The old single-tree termination path can report infeasibility merely
  because no reduced NLP incumbent was obtained, and it does not enforce a
  closed gap before reporting optimality.
- The old review's suggested objective-error estimate from separate Slater
  points needs additional joint regularity; its restriction on subgradient
  choice in the radial separation argument is also too strong. The theory
  note will give proofs and counterexamples.

This log is an active development record. Completion and publication
readiness have not yet been established.

## Pilot protocol and review progress

The first pilot uses five small instances with seed 104729, the eight matched
LB-ESH/ECP configurations, GDPopt LOA, SHOT big-M/hull, and the applicable
quadratic conic baseline. Its command was:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH \
uv run --frozen --no-sync python -m lbesh_research.benchmark \
  --instances lbesh.exp.small.s104729,lbesh.log.small.s104729,lbesh.reciprocal.small.s104729,lbesh.quadratic.small.s104729,lbesh.logsumexp.small.s104729 \
  --methods all --time-limit 30 --wall-limit 60 --threads 1 --parallel 4 \
  --out results/lbesh_development/pilot_small_v1.jsonl
```

All 40 LB-ESH/ECP runs passed the independent original-model feasibility and
numerical gap checks. These are development measurements, not final timing
evidence: code review was still active. The pilot exposed inconsistent hull
initializations in the GAMS adapter, tolerance mismatches, and weak SHOT hull
bounds when convexity was not recognized. These require separate handling;
interface failures are not evidence of an algorithmic advantage. The default
SHOT hull behavior is retained, and a distinct declared-convex hull baseline
is being evaluated only for analytically verified generated models.

The scale pilot uses the ten corresponding medium/large instances with the
same seed and eight core configurations, 60-second solver limits, 90-second
wall limits, one thread, four workers. Output:
`results/lbesh_development/pilot_scale_v1.jsonl`.

Independent mathematical review accepted the qualified theory after four
precision corrections. Independent implementation reviews found and prompted
repairs for fixed-variable mutation, disjunct-indicator hull semantics,
unsupported active components, and conditional objectives. Their notes
preserve the findings and tests; acceptance applies only to the documented
supported scope and never means exact numerical certification.

Review showed that all initial 42 generated instances have standard conic
representations. Before any performance evaluation of the additional family,
the design was extended by nine trigonometric allocation instances using
`(1-cos(1.5*z))/(1-cos(0.75))` on `0 <= z <= 1/1.1`. This function is
increasing and convex throughout the full declared domain. This exercises
smooth expression oracles for which the package supplies no standard cone
translation; no impossibility of a conic formulation is claimed. Existing
parameters and seeds are unchanged.

### Pre-freeze reference-pass deviation

The coordinator's authorization for the conic-reference agent ambiguously
said to solve all 42 roots while the intended timing was after review and
freeze. The agent ran those continuous reference solves before receiving the
hold clarification. This file is retained as
`results/lbesh_development/general_conic_roots.json`. The agent inspected
aggregate statuses/residuals, not held-out objective values, and reported no
parameter tuning. The original seed split is retained rather than selecting
replacement seeds. These are predeclared held-out algorithm experiments,
not a claim that every reference computation was blind. A frozen reference
rerun is required before final use.

## Source freeze and main study

After independent review corrections, the coordinator reran the topic checks.
The first combined unittest command contained the wrong module name
`lbesh_research.test_independent_conic`; 66 actual tests passed and that one
import failed. The missing module was then run with its correct name,
`lbesh_research.tests.test_independent_conic`, together with the opt-in real
adapter checks (13 tests passed). The isolated general-cone suite added six
passing tests. Total: 85 executed test methods passed; the import typo was
not a test failure and was not hidden by rerunning unrelated suites.

Commands, from the solver lab, with the environment variables recorded above:

```sh
uv run --frozen --no-sync python -m unittest \
  lbesh.tests.test_publication_contracts \
  lbesh.tests.test_independent_solver_review \
  lbesh_research.tests.test_conic \
  lbesh_research.test_independent_conic \
  lbesh_research.test_harness \
  lbesh_research.test_independent_harness \
  lbesh_research.test_instances_independent
LBESH_RUN_SOLVER_REVIEW=1 uv run --frozen --no-sync python -m unittest \
  lbesh_research.tests.test_independent_conic \
  lbesh_research.test_independent_harness_solvers
uv run --project lbesh_research/conic_reference_env --frozen --no-sync \
  python -m unittest lbesh_research.test_conic_reference \
  lbesh_research.test_conic_reference_independent
```

`source_v1.tar.gz` archives 357 source/data/instruction files and has SHA-256
`6c9eaf9898f04d08a12381879ab9bae79f83b800f0db9e4cc696ccbff6be84ad`.
Its adjacent manifest records every file hash. Later analysis and diagnostic
programs live outside the frozen solver/harness package and will be archived
separately. The main algorithm study is launched with:

```sh
uv run --frozen --no-sync python -m lbesh_research.benchmark \
  --instances all \
  --methods lbesh-esh-hull-single,lbesh-esh-hull-multi,lbesh-esh-bigm-single,lbesh-esh-bigm-multi,lbesh-ecp-hull-single,lbesh-ecp-hull-multi,lbesh-ecp-bigm-single,lbesh-ecp-bigm-multi,gdpopt-loa,gams-shot-bigm,gams-shot-hull-convex,gams-gurobi-bigm,gams-scip-bigm \
  --time-limit 120 --wall-limit 150 --threads 1 --parallel 6 \
  --order-seed 20260919 --out results/lbesh_development/main_generated_v1.jsonl
```

The saved schedule contains 663 jobs. Results remain provisional until the
schedule is complete, witnesses and bounds are audited, repeated runs are
compared, and fresh reviewers assess the final interpretation.

## Supplementary schedule and scope audit

While the frozen main batch was running, the remaining planned comparisons
were made concrete in `supplementary_plan_v1.json`, without selecting cases
from observed oracle wins: two 132-job held-out timing repeats, nine exact
quadratic conic MICP controls, all 27 historical names with 13 methods (351
jobs), and the 18 declared pilot cases with eight single-tree ablations
(144 jobs). Limits remain 120 solver seconds / 150 process seconds, one
thread, and at most six workers. `lbesh_study_queue.py` waits for all 663
primary records, checks frozen executable hashes, and runs these batches
sequentially. Queue syntax validation passed with
`python -m py_compile lbesh_study_queue.py`.

The independent legacy audit and its fresh second review corrected the
old blanket boundedness description: eight compact smooth extracted
models, six compact smooth original domains needing an epigraph argument,
and thirteen broader stress cases. All 27 remain in the numerical set;
classification is based on mathematical input scope, not solver outcome.
The current protocol now makes this distinction.

The actual-oracle diagnostic is complete and freshly reviewed. It calls
the frozen ESH root-search code, rather than substituting analytic roots.
Its scalar and 896 geometry checks support a qualified representation
sensitivity mechanism while accounting for root work and non-dominance.
The standalone final analysis is undergoing an independent code review;
no incomplete-study performance conclusion is used.

## Reviewed analysis and numerical sensitivity

The standalone analyzer passed 31 author/independent targeted checks after
fresh review repaired diagnostic completeness, source fingerprints, ablation
pairing, and supplementary/reference coverage. A separate fresh auditor
prepared an independent standard-library calculation of final counts, gaps,
paired times, and PAR10; final data approval remains pending.

Partial primary data exposed original-row feasibility residuals above the
common threshold in all three medium trigonometric GAMS/Gurobi cases and
one large case. Native logs confirm general nonlinear solving and residual
warnings. The separate audit distinguishes documented expression
disaggregation from the unobserved exact auxiliary-error trace. No primary
data, settings, or acceptance tolerances were changed.

An outcome-triggered sensitivity was declared after the source freeze, while
the main study was still running: all nine trig instances, only
`feasibilitytol=1e-8`, unchanged time/thread/gap/checker settings, order seed
20260926. This is an explicit supplementary follow-up, not a prespecified
primary comparison. Its external adapter and five author/seven fresh tests
passed independent review before solver execution. It waits until the full
existing queue completes, so solver concurrency remains at most six. The
plan, wrapper provenance, option files, and native parameter confirmation
are retained separately. No best-of replacement is allowed.

## Completed primary study and follow-up decisions

The 663-job primary study, two 132-job timing repeats, nine quadratic
conic controls, and 351-job legacy study are complete. The primary
independent audit revalidated original-model witnesses and matched 2,172
summary fields without a disagreement or bound contradiction. A second
calculation matched the reported cohort membership and 4,032 telemetry
fields. The repeated single-tree solve outcomes are identical; timing
variation and the common-solved selection are reported explicitly.

Legacy GAMS runs exposed two avoidable interface issues: the seven farm
models start with unset widths that the expression checker temporarily
evaluates at zero, and the batch model contains an unused trailing tank
variable omitted by the GAMS solution map. A separate 24-job follow-up
initializes these values before calling the unchanged frozen adapter.
It covers all eight affected models with SHOT, Gurobi, and SCIP. Equations,
bounds, big-M values, solver options, and acceptance rules remain unchanged.
The original errors and invalid witnesses are retained. The follow-up
requires independent review before execution and is reported separately.
Native no-incumbent outcomes and nonsmooth-objective stress failures do not
justify additional initialization repairs.

The 144-job ablation batch and frozen cone references remain in progress.
A fresh scientific reviewer is assessing the full contribution independently
of the authors; final numerical and scientific acceptance await those data
and the two declared follow-ups.

## Final numerical verification

All 1,464 benchmark jobs and 420 cone-reference calls are complete. The final
analysis in `analysis_v1` includes all eight benchmark files, both reference
files, complete schedules, source fingerprints, witnesses, native solver
records, derived tables, and figures. It reports zero audit warnings.
The independent final audit matched all 6,122 summary/pair fields and all
33 follow-up pairs (660 additional fields), checked the remaining derived
cohorts, and accepted the final results narrative. Every one of the 174
optimal fixed-assignment cone witnesses passed fresh original-model
validation. No unresolved bound contradiction or material reporting issue
remains. Two inaccurate continuous-root statuses remain explicit.

The last analyzer revision, SHA-256
`3c207d4c570fe77a65b844f7fb5a5649f7a073755e58579bccbd04ed4db011da`,
passed 59 targeted author/independent tests. These tests cover the additional
initialization provenance gate and the CSV export correction; they are
separate from the 85 pre-freeze solver/harness/reference test methods.
Exact commands and test composition are preserved in the review notes.
The final targeted documentation-link check found no missing local targets,
and `git diff --check` passed for the tracked topic changes. No project-wide
verification or CI inspection was used.

The dedicated native-record review accepted both supplementary studies.
The trig tolerance study has nine feasible witnesses and six closed gaps.
The initialization study has 23 feasible witnesses and 11 accepted closed
gaps. Its invalid Gurobi `FLay05` witness remains rejected. The batch Gurobi
native log reports a closed gap, but the GAMS statistics export omits the
bound; the declared scorer therefore retains a missing-bound outcome.
SHOT normal completion with a loose bound is likewise not counted as solved.
The frozen SHOT version-field parser misses a multiline banner; the reviewer
recovered version 1.1 and git a81275b4 from the retained native logs.

The negative integer-point-NLP ablation received an additional solver-free
diagnosis and fresh scientific review: 53 stalls without accepted incumbents,
nine stalls with valid incumbents and open gaps, nine time limits without
incumbents, and one accepted optimum. No false optimum or infeasibility
claim was found. The absent candidate traces limit a more specific causal
diagnosis; this limitation remains in the final interpretation.

The fresh final scientific reviewer accepted the completed topic for a
focused computational and methodological publication. No further experiment
or development is required for the stated claims. The contribution has
modest impact and concerns the tested NLP-assisted policy; new-cut-family,
new-framework, and broad solver-superiority claims remain excluded. The
readiness assessment and claim register now reflect this final decision.

The completed research bundle retains the frozen sources, later analysis
and audit programs, pinned environments, all topical notes, raw logs and
witnesses, and final tables. A per-file hash manifest and archive checksum
make it inspectable. Intermediate and failed exports remain labeled as
such; they do not replace the final `analysis_v1` evidence.
