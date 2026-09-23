# Stage 3 independent review 03, round 01

Reviewer: `/root/reviewer03`. Date: 19 September 2026.

## Verdict

No major issue identified. The stage supports the deliberately narrow matched computational contribution and retains the evidence that limits it. Approve after the minor effective-settings clarification below. I did not consult other current Stage 3 reviews, edit manuscript/research sources, spawn agents, or treat the reserved Stage 4 packaging and narrative as missing Stage 3 work.

## Major issues

None.

## Minor actionable issue

1. **Distinguish outer gap targets from actual inner-master settings, and disclose the conic feasibility settings.** `sections/experimental-design.tex:18` gives relative 1e-4 and absolute 1e-6 “solver gap targets” under the heading “effective settings,” but the prototype sets its actual Gurobi master to `MIPGap=1e-6` and `MIPGapAbs=1e-8` at the main tolerances (`code/minlp_solver_lab/lbesh/solver.py:98–99`). Its outer acceptance target is the stated 1e-4/1e-6. The exact conic adapter additionally sets both `FeasibilityTol=1e-8` and `IntFeasTol=1e-8` (`code/minlp_solver_lab/lbesh_research/conic.py:358–361`), whereas line 18 currently mentions only `NonConvex=0`. Add these short exceptions, or an explicit settings table, so readers do not infer equal inner-master gaps or default conic feasibility tolerances across the contextual baselines. No rerun is needed: the options are already frozen and preserved, the paired ESH/ECP comparison shares them, and the manuscript already limits cross-solver claims.

## Experimental validity and interpretation

I checked the complete experimental-design/results sections, model and computational appendices, new empirical oracle subsection, generated tables, scripts, compact data/provenance, new bibliography entries and author report.

The following potentially material issues are handled correctly:

- The 51 controls are 45 allocation instances plus six region instances; the 18/33 split and shared streams/prefixes are explicit. They are not represented as independent applications or independent statistical samples.
- The pre-freeze continuous-reference exposure is disclosed rather than erased. `notes/lbesh-development-log.md:125–145` supports the chronology: trig was added before observing its performance; the earlier reference pass inspected aggregate status/residual information without held-out-objective tuning. The reported reference pass is separately frozen. “Held out” is qualified accordingly.
- All 1,464 records, failures and follow-ups remain distinct. The primary, repeats, conic, external, ablation and outcome-triggered follow-up denominators reconcile. There is no fastest-repeat or best-follow-up selection.
- Timing uses matched common-solved cohorts and a stated one-second shift; full-schedule PAR10 is reported separately. The manuscript does not equate failure-penalized means with conditional speedups.
- Unchanged solver search seeds, at most six concurrent workers, other machine work, short timings, related models, unrepeated multi-tree/external observations and common ECP interiors are disclosed.
- The five status advantages are accurately described as five method–instance outcomes on four controls. Near-limit finishes are visible, and the conditional 4–6% single-tree effect is not presented as a large or broadly proven improvement.
- Cut-generation time is explicitly total time per run, not per-cut time. The paired mean versus median differences and overlapping callback timers prevent a false additive or instancewise causal explanation.
- Exact quadratic cone solves are a materially unfavorable comparison for the prototype and are prominently retained. Continuous root checks target the same hull; inaccurate cone statuses and noncertified duals/infeasibilities remain qualified.
- The external scope is fixed by expressions, not successful outcomes. All six norm cases remain in the stress stratum, including the successful cases. The 21 no-norm stratum is not mislabeled as satisfying every theorem. Conic scope is 25, and supported/no-norm overlap is 19 with 17 common solved comparisons.
- Original writer failures, incomplete witnesses, the follow-up recovery, missing exported batch bound despite native closure, and SHOT's legacy nonconvex classification are explained. The manuscript does not turn interface failures into proof of algorithmic inferiority.
- No-integer-NLP recovery retains interior NLP work and its 69/72 versus 1/72 outcome is explicit. The absence of candidate/cut histories limits diagnosis. Optional user cuts retain actual cut counts and their lack of accepted-count gain.
- Acceptance formulas match the independent original-model checker and `summarize.assessed`; valid numerical witnesses and global-bound usability are required, rather than merely mapped `optimal` status. Independent aggregation is correctly distinguished from an independently written feasibility checker.

## Formulations and diagnostic checks

The five allocation cost derivatives, common domain [0,10/11], trig curvature range, monotonic epigraph bound, fixed-charge/operating tradeoff, and primal witness argument are consistent. The region witness and variation bound are valid; the 9n epigraph bound follows from coordinate differences bounded by three. The stated random draw order reproduces the stored coefficient digests.

The SOC product identity and four perspective epigraph laws are correct. At zero weights, the positive aggregate cost coefficients close the possible auxiliary slack freedom. The region cone budget likewise forces inactive auxiliaries to zero. The exact quadratic lift uses an equality slack and finite scaled copies consistently. Separate disjunction hulls are not claimed to give the complete GDP hull. The external A/B/C classification matches the retained structural audit and does not import missing compactness or smoothness into the theoretical claims.

The empirical oracle subsection accurately distinguishes actual `_esh_cuts` execution with analytic wrappers from the expression compiler, a box-only scalar starting master from the theorem's optional anchor tangent, geometric from representation-dependent residual tolerances, and measured evaluations from full solver runtime. Its centered geometry, prescribed anchor, fallback exclusion, non-dominance control and microsecond-timing limitations are all stated.

## Checks actually run

1. Read-only source inspections using `cat`, `sed`, `nl`, `rg`, and Python across all Stage 3 sections, scripts, generated table fragments, data, provenance, relevant notes, and targeted implementation paths (`benchmark.py`, `conic.py`, `solver.py`, `validation.py`, `summarize.py`).
2. Independently verified all 47 files against `process/stage03-author-source-sha256.json`.
3. Independently checked every `inputs`, `raw_source_sha256`, and `data_sha256` entry in `data/provenance.json` against its actual file. All matched.
4. Compared the entire compact `data/records.json` to the frozen final analysis `records` list: all 1,464 records matched exactly, including values and classifications.
5. Copied the paper into a `tempfile.TemporaryDirectory` and ran `scripts/regenerate.py --no-figures` there. All 17 table fragments, `records.csv`, and `table_values.json` matched the frozen paper bytes exactly (19 outputs).
6. Ran `scripts/check_evidence.py` in the same isolated copy. It passed all narrative/batch/cohort/repetition/LP/reference/oracle checks and all 51 independently reconstructed parameter streams. This is not another primal witness validation.
7. Primary web spot checks: [CVXPY Solver Features](https://www.cvxpy.org/tutorial/solvers/index.html) explicitly supplies the exponential cone zero-scale slice cited by the appendix; [SCIP 10.0](https://arxiv.org/abs/2511.18580) confirms the new reference's title, lead author and 2025 date.

The temporary copy was removed automatically. No optimizer call, broad benchmark rerun, LaTeX build, project-wide test, CI inspection or fresh witness audit was performed. The already recorded full fresh audit is accurately described by the paper; this review adds independent source/data correspondence and standalone regeneration checks rather than claiming to duplicate it.
