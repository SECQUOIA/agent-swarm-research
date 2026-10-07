# Empirical chapter source and claim accounting

Prepared 2026-10-05. Owned files are `sections/experiments.tex`,
`tables/empirical-protocols.tex`, `tables/empirical-branching.tex`,
`tables/empirical-finite-c1.tex`, and this report. No original notes or
results were edited. No experiment, optimizer, generator, Monte Carlo
simulation, or original summary script was executed. No literature search,
project-wide check, or CI inspection was performed. Standalone TeX
compilation is assigned to root after integration.

The chapter uses the completed Opus `EXPERIMENT-MAP.md`, Sol
`ARCHIVE-PROVENANCE.md`, portable archive README, figure caption, figure
metadata, and verification report. The figure is already a presentation
artifact; the chapter does not regenerate it. The archived original count
is 209 byte-exact files. `SOURCE-INVENTORY.json` records their paths, byte
counts, and SHA256 hashes. The existing read-only package check reports
218 hashes checked, 176 fit groups checked, and 230 figure observations
checked. These are the package author's checks, not new solver runs or
mathematical correctness certificates.

## Scope and safeguards incorporated

- Distinguish SCIP processed nodes, final leaves, and processed nodes of
  exact rational/Python models. Do not turn counts into runtime ratios.
- Explain SCIP's global absolute-gap stopping test, numerical incumbent
  offsets, exhausted-tree statuses, LP tolerance refusal, finite fit
  windows, and exclusion of limit records from fits.
- Keep `model` separate from default: supplied optimal incumbent,
  heuristics off, best-first order, propagation still on. The three changes
  are simultaneous; they are not individually identified interventions.
- Separate the two MINLPLib campaigns: S2 has 120 CPU seconds, S3 has 60.
  Preserve paired seed labels, instance bootstrap, shift 10, and different
  crash conventions. Limit node counts are observed unfinished work.
- Distinguish parameter-only and plugin branching arms, including the
  10.0.3 source/10.0.2 executable mismatch. Do not infer a solver
  recommendation from confidence intervals containing one.
- Keep sparse planted-support tests, root certification, removal-only
  tests, full C1, and global optimality distinct. A failed relaxation
  certificate is not an improved integer solution.
- State the exact violated sparse assumption `(log p)^6 <= n <= p`.
  It constrains sample size `n`, not support size `k`. Sparse tests have
  `p <= 3200`, `k <= 20`; asymptotic constants are not validated.
- Keep the stronger sparse `k=3`, nested-column, fixed-`log 200` ridge
  experiment separate from the `k=8`, ridge-varying-with-`p` C1 experiment.
  Gap-closing fractions use the numerical global optimum where enumerated.
- Treat retained `z_j=0` helper columns as values in lifted witnesses,
  not as branch fixings. Preserve the theorem's separate surviving-helper
  convention.
- State binary Gaussian normalization, independence, observed finite C1
  frequencies, all 330 decided outcomes, and censoring of tree counts.
  Distinguish planted-point box exactness (`2^-N`) from any vertex
  minimizing the relaxation, rounding, and box/orthant inactivity.
- C1 is sufficient for a linear variable tree under the stated incumbent
  or best-bound assumptions; its failure does not prove larger trees.
- Omit decomposition empirical studies S6/S7, whose central datasets are
  outside the selected portable archive. No practical speedup is claimed.

## Manuscript labels

| Label | Role |
|---|---|
| `sec:experiments` | Entire empirical chapter |
| `experiments:protocols` | Solver/data protocol and numerical semantics |
| `experiments:tolerance` | S1 formulations, fits, representation effects |
| `experiments:benchmark` | S2/S3 benchmark and synthetic kink evidence |
| `experiments:random` | S4/S5 random-design evidence |
| `experiments:tab-protocols` | Four principal SCIP cohorts and statuses |
| `experiments:fig-scaling` | Four-panel retained node-scaling figure |
| `experiments:eq-ratio` | Exact shifted per-instance ratio convention |
| `experiments:tab-branching` | Separate 120/60-second benchmark comparisons |
| `experiments:tab-finite-c1` | Sparse/BLS finite-cell passes with denominators |

## Portable source base and claim mapping

In the following table, `A/` means
`reproducibility/archive/research-20260928b/bb-complexity/`.
Every copied source is independently identified by the inventory and
checksums; section labels below identify the submission text using it.

| Claim or display | Retained original sources | Scope and interpretation |
|---|---|---|
| Solver versions, recorded environment, S1 gap/seed/budgets | `A/solver-validation/results/meta.json`, `run_one.py`, `sweep.py`; `A/minlplib-branching/results/meta.json`; `A/robust-branching-points/results/meta.json` | `experiments:protocols`, `experiments:tolerance`; S1 Ipopt version unrecorded; no software universality claim |
| Four principal cohort sizes/statuses | `A/solver-validation/results/runs.jsonl`; `A/minlplib-branching/results/runs.jsonl` core only; `A/robust-branching-points/results/minlplib.jsonl`, `synthetic.jsonl`; `VERIFICATION-REPORT.json` | `experiments:tab-protocols`: S1 2134 =1655 gaplimit+420 optimal+59 nodelimit; S2 core855=797 optimal+57 timelimit+1 crash; S3 benchmark2052=1943 optimal+104 timelimit+5 crash; S3 kinks3840=2024 gaplimit+1816 optimal |
| Synthetic objective definitions and expression form | `A/solver-validation/instances.py` lines1–184, generated `cip/` files | `experiments:tolerance`; h, q, hidden-zero, sphere/plane, exponential constraints, aligned/transversal McCormick definitions included; asymmetric boxes and exact decimal formulation coefficients retained in archive |
| Global absgap semantics, feasibility-scale offsets, tolerance refusal | `A/solver-validation/run_one.py`; retained `results/tolerance_probe.log`, `results/runs.jsonl`; `EXPERIMENT-MAP.md` S1 numerics | `experiments:protocols`; no rigorous epsilon certificate assertion |
| Figure records, curves, selected instances, markers, displayed fits | `A/solver-validation/results/runs.jsonl`, `runs_fits.json`; new `presentation/figure-metadata.json`, `FIGURE-CAPTION.md`, `plot_node_scaling.py` | `experiments:fig-scaling`: exactly230 observations,19 instance/setting curves,14 named instances; no averaging/pooling; root includes existing `figures/node-scaling.pdf` |
| One-/two-dimensional exponent groups, quartic fit discrepancy, isolated additive fits | `A/solver-validation/results/summary.md` model rows; `runs_fits.json`; `analyze.py` fit function | `experiments:tolerance`: powers 0.50–0.52 and 1.01–1.05; the latter fits span 1–2 decades, though full available sequences span 2–3. Quartic powers 0.49–0.51; qflat1 model 0.31/0.33 versus toy 0.25/0.24; additive 9,10,40,92. Finite fits only. |
| Fit filtering and windows | `A/solver-validation/analyze.py`; `ARCHIVE-PROVENANCE.md` Figure protocol | Tail last5 available eligible eps<=1e-3, wide eligible eps<=1e-2, >=3points and >=.99 decades; limits/errors excluded, optimal retained; early limit stops censor sequences |
| Final leaves/integral bound | `A/solver-validation/results/summary.md` lines182 onward, `thm_bounds.json`, raw `runs.jsonl`; `VERIFICATION-REPORT.json` model_leaf_ratios | Seven applicable instances; minimum1.59; iso2 6.84–9.78,linediag2 15.88–23.65,qflat2a 6.76–9.41; numerical consistency only |
| Representation and propagation examples | `A/solver-validation/instances.py`, `run_one.py`, `results/summary.md` ring2/noexpand,condisk2,isofbbt2 rows | Ring2 expanded model37439 at1e-6 vs noexpand1; shared condisk2 one node; isofbbt2 15 over1e-2..1e-7 outside quadratic gap hypothesis; no escaped fixed-oracle lower bound claim |
| Aligned/transversal McCormick counts and lock reduction | `A/solver-validation/instances.py`, `run_one.py`, `results/summary.md` mccaxis2/mccdiag2 rows | At1e-7:LP3,x-only external45,both-variable external10469; settings change search/propagation as caption states; lock reduction changes allowed operations |
| S2 selection, screening, record accounting | `A/minlplib-branching/{selected.txt,candidates.csv,select_candidates.py,select_benchmark.py,features.py}`; `results/{meta.json,runs.jsonl,screen.jsonl,trace.jsonl,trace2.jsonl}` | 57 selected relatively easy instances;24 integer;5no continuous branching;855core+171optional+228sweep+486screen+171trace+16trace2=1927; only855core in principal comparison |
| S2 point/seed/default tolerance parameters | `A/minlplib-branching/run_one.py`, `runner.py`, `results/meta.json` | Default pull.75,width-trigger.5,clamp.2; matching seed labels0–2; zero requested gaps; default numerics; knobs can also affect selection scoring |
| S2 ratios/intervals/statuses/seed spread/completed-only subset | `A/minlplib-branching/results/summary.md` lines5–15,40–50,59–85; `results/runs.jsonl`; `analyze.py` | `experiments:tab-branching`; shift10,5000instance resamples seed1,normal-approx two-sided Wilcoxon; default spread1.51 among56 completed3-seed instances; no-clamp complete-only1.08 on41 is selection-conditioned |
| Boundary-chain diagnostic | `A/minlplib-branching/results/trace.jsonl`, `trace2.jsonl`, `summary.md`; mapped original branching-point note mechanism paragraph | 10 of 16 LP/no-clamp failing instances have the LP value on a bound in 42–100% of bounded continuous branchings. Concrete traces override the erroneous source-summary count of 11; explanatory diagnostic, not an independent treatment effect. |
| S3 60-second campaign, plugin/parameter arms | `A/robust-branching-points/{scip_run.py,runner.py,minlplib_jobs.txt}`; `results/{minlplib.jsonl,meta.json,summary.md}` lines3–40 | Separate2052runs; point/selection source read from10.0.3,executable10.0.2; default/plugin not identical; randomclamp[.1,.3],recentering.2 |
| S3 ratios and missing-seed policy | `A/robust-branching-points/summarize.py` lines61–95; `results/summary.md` lines26–40 | Ratio omits full paired instance with any missing count, typicallym56; no-clamp2.00CI1.43–2.96; recentre/default.92CI.71–1.14,plugin-LP.94CI.86–1.01; full171 status denominator retained |
| S3 synthetic kink counts/spread | `A/robust-branching-points/{scip_run.py,synthetic_jobs.txt}`; `results/{synthetic.jsonl,summary.md}` Synthetic kink instances block |3840 =16x12x5x4; propagation/weak-dual/heuristics disabled; 1D a1/6 clipping3,7,9,13 vsrecentre5; McCormick sameposition7190 vsplugin recentre21 at1e-8; ordinaryrandom LP clamp near.0102 mean766 range7–3443 vsfixed26 |
| Exact rational kink record | `A/spatial-face-exact/kink_exact_runs.py` lines20–51; `kink_exact_runs.log`; `A/robust-branching-points/exact2d.log` |19537 is processed model nodes, not leaves; no comparison of per-node costs with SCIP; exact source runs were not executed here |
| Sparse cell generator/decision normalization | `A/sparse-regression/{code/core.py,code/exp_c1.py,code/make_tables.py,code/regen_tables.py}` and cell files listed below |Gaussian X,per-entry sigma.5,b1,k8,nround(alpha*k*logp),lambda1.5sigma sqrt(2nlogp)/b; support objective unnormalized; numerical primal/dual classification |
| Sparse displayed C1/root counts | Exact raw locators and overlay below; independent standard-library reader verified only the eight displayed cells | `experiments:tab-finite-c1`(a); no unresolved decisions,8seeds1000–1007 each; roots0/8; nominal/realized alpha distinction explicit |
| Sparse revision31 decisions | `A/sparse-regression/data/c1_redecided.jsonl`; `VERIFICATION-REPORT.json` sparse_redecided |30passes,1failure; redecision resolves earlier cap labels,not exact arithmetic |
| Sparse removal/fullC1 rule exceptions | `A/sparse-regression/data/rule_p100_k6.jsonl`, `rule_p200_k8.jsonl`; `VERIFICATION-REPORT.json` sparse_rule_exceptions |3of72 cases; p100,alpha1,seed4000:largestz13,frac23; p100,alpha1.25,seed4001:13,17; p200,alpha1.25,seed4005:17,23; removal passes while fullC1fails |
| Stronger sparse root gap closing | `A/sparse-regression/stronger-relaxations/{code/exp_mech.py,code/summ.py,data/table_n20.md,data/mech_n20_k3.jsonl,data/opt_mech_n20_k3.jsonl,data/dong_n20.jsonl}` | Separate k=3 nested experiment, fixed log200 ridge; fractions 51%,25%,12%,3% for p=40,80,160,320. Numerical enumerated global OPT; medians condition on relative perspective gap>1e-4, with 7,8,8,8 contributing runs from 8 recorded seeds per cell. |
| Stronger sparse helper witness | `A/sparse-regression/stronger-relaxations/data/table_n40.md` line8; `mech_n40_k3.jsonl`, `opt_mech_n40_k3.jsonl`; `code/cbound.py`; original thresholds note Section7 |n40,p3200,6/8 C1-certified retainedinstances,4/6L2inexact via explicit feasiblevalues; no fullzbexactnessclaim |
| Binary generator and node/certificate tests | `A/binary-least-squares/{code/core.py,code/exp_c1.py,code/exp_trees.py}`; `data/c1.jsonl` |A=sqrt(rho/N)H,M=betaN,independentstandardH,w,binaryxstar;incumbentxstar,best-first,FWlowerboundnumerically evaluated |
| Binary C1 cells/full330 decisions | `A/binary-least-squares/data/tables.txt` Table7.2 startsline50; rows54,56,61,63,68,70,77,78; `data/c1.jsonl`; `VERIFICATION-REPORT.json` | `experiments:tab-finite-c1`(b); squareN100/200/400/800 denominators8/8/6/4,missingcellsdashes; limitingtheta1/4notmeasured; tallN8000/2at.1,2/2at.12 |
| Binary tiny-root probabilities | `A/binary-least-squares/data/tables.txt` Table7.1a; `data/root.jsonl`, `code/exp_root.py` |GridN2,4,6,8,beta1,2,rho1,4,16,64;20000trialspercell; planted box optimumvsanyvertexevent separate |
| Binary tree counts/caps | `A/binary-least-squares/data/tables.txt` Table7.3 startsline104; `data/trees_b1.jsonl`, `trees_b1_256.jsonl`; original tree code |rho4logN;mostfrac44,97,509,15765 atN32,64,128,256;6,6,6,4seeds;staticN256all4capped100000; no asymptoticgrowthproof/runtimeclaim |
| Statistical theorem limitations | `AUDIT-DISCRETE.md` Scope corrections and Existing empirical evidence; `REVIEW-NNLS-R1.md`; final `sections/regression.tex` and `sections/binary-least-squares.tex` |Exactnlog^6condition;C1sufficiencyversusnecessity;helperconvention;binaryclasslowerboundvacuity at testedN; compare only to proved limitingconstants |

## Exact sparse table locators and calculation

The base directory here is `A/sparse-regression/data/`. Load
`c1_p200_k8_t1.5.jsonl` before sorted `c1_scaleP_*.jsonl`, following the
retained `regen_tables.py`/`make_tables.py` convention. Apply each loader's
deduplication key `(p,k,rule,n,seed,b,alpha-if-no-rule)`, then retain the
first `(p,k,n,seed)` row and group by `(p,k,rule,n)`. Replace only `c1 ==
"capped"` with the redecision keyed by `(p,k,rule,n,seed)` in
`c1_redecided.jsonl`. Do not overwrite decided base records.

| Cell `(p,k,rule,n)` | First-retained raw lines in seed1000–1007 order | C1/root passes |
|---|---|---|
| `(100,8,"1.5",55)` | `c1_scaleP_k8_t1.5.jsonl`:19,20,21,22,25,29,27,28 |8/8;0/8|
| `(100,8,"1.5",64)` | same:32,31,34,33,35,39,36,38 |8/8;0/8|
| `(200,8,"1.5",64)` | `c1_p200_k8_t1.5.jsonl`:10,7,20,11,12,13,16,14 |8/8;0/8|
| `(200,8,"1.5",74)` | same:15,19,18,17,21,46,28,22 |8/8;0/8|
| `(400,8,"1.5",72)` | `c1_scaleP_k8_t1.5.jsonl`:73,81,74,75,76,77,78,79 |6/8;0/8|
| `(400,8,"1.5",84)` | same:80,86,82,83,84,85,88,87 |8/8;0/8|
| `(1600,8,"1.5",89)` | same:129,130,131,132,133,134,135,136 |7/8;0/8|
| `(1600,8,"1.5",103)` | same:137,138,140,139,141,142,143,145 |8/8;0/8|

The nominal `alpha=1.5/1.75` columns correspond to those integer sample
sizes; realized alpha is `n/(8 log p)`. For `(1600,89)`, seeds1000,1001,
1002,1003,1006 use overlay lines14,13,15,16,17, all `C1`. For `(1600,103)`,
seeds1000,1001,1002,1004,1005,1007 use overlay lines19,18,21,20,22,23,
all `C1`. No other displayed cell requires the overlay. C1 failures in the
first nominal column occur at `(400,72)` seeds1003/1006 and `(1600,89)`
seed1004. Every displayed base root flag is false.

## Corrections and review findings incorporated

1. The qflat2a all-half-decade model leaf/bound range is6.76–9.41, not the
   note's full-decade-only7.4–9.4 range.
2. The sparse source sentence saying the removal half fails whenever full
   C1 fails is false in3/72 archived cases. The chapter states the exceptions.
3. `EXPERIMENT-MAP.md` S3 calls rational19537 a leaf count. The actual
   counter increments on every popped node in `kink_exact_runs.py` and
   returns that total. The chapter says processed model nodes; root was
   notified to correct any other uses.
4. The direct S2 no-clamp ratio is2.184885799809008 in the verification
   report. It rounds to2.18 at two decimals. Double-rounding source2.185
   gave2.19; independent empirical review caught this, and table/prose now
   use2.18.
5. The sparse logarithmic-sixth-power assumption constrains `n`, not `k`.
   The exact manuscript condition is `(log p)^6 <= n <= p`.
6. Helpers at a lifted root witness have `z_j=0`; they are not branch-fixed
   variables. The prose now states that distinction.
7. Independent empirical review requested the stronger sparse `k=3`,
   nested-design, fixed-`log200` ridge protocol and global OPT denominator.
   These are now explicit, with the conditional median rule preserved.
8. Binary root planted/vertex events, Gaussian independence, and the exact
   tiny-system grid are explicit. C1 failure is never used as a tree lower
   bound.
9. Independent empirical review counted the boundary diagnosis directly
   in both retained trace files: 10 of the 16 failed instances have shares
   42–100%, not the source summary's 11. The qualifying names are
   `ann_peaks_exp`, `ex6_2_8`, `hs62`, `inscribedsquare03`, `ex8_5_3`,
   `oil2`, `kriging_peaks-full010`, `st_e03`, `supplychainp1_030510`,
   and `wastewater05m1`. The remaining six do not meet that diagnostic
   range; `ex4_1_5` has no bounded continuous branchings.
10. The two-dimensional optimal-set model fit windows span one or two
    decades. The complete available sequences span two or three; the
    source map conflated these. `sphere3`/`conexp4` tail windows are
    1e-3..1e-4, their wide windows 1e-2..1e-4, and `plane3` has no tail
    fit and a wide window 1e-2..1e-3. Prose now separates fit span from
    sequence span and makes the optimal-set/ambient dimension distinction.
11. The aligned McCormick discussion now references `sec:geometry`, where
    that mechanism is proved, rather than the separate positive-secant-gap
    face-exact chapter.

`AUDIT-DISCRETE.md` and `REVIEW-NNLS-R1.md` are incorporated for all
planted/global distinctions, safe probabilistic regimes, incumbent/order
qualification, and finite-size limits. `REVIEW-PWE-R1.md` is respected:
the empirical chapter makes no new PWE error claim or rescue theorem.
It relies on the proved regression chapter for the root criterion and
does not restate or judge the published theorem.

The independent final empirical reviewer reports no remaining blocker and
pins the section at SHA256
`455ef17d3c7ec4042e93d2b3d01f8e283813e6db9942c13debbdea17a5c47350`.
The corresponding review report is
`REVIEW-MANUSCRIPT-EXPERIMENTS-R1.md`; its findings are incorporated above.
The section and tables are held at that reviewed version for integration.

## Final source snapshots consulted

The brief, authoring conventions, architecture decision, incoming audits,
issues, and latest literature-key file were reread at completion. Their
pending-status text is treated as a process ledger, not as the final
mathematical verdict; the current architecture decision and completed
independent findings govern the chapter. `LITERATURE.md` was not yet present
at that read. This chapter adds no literature or novelty claim and needs
no additional literature query.

| Internal evidence file | SHA256 at completion read |
|---|---|
| `INCOMING-AUDITS.md` |`cbe217fa88ebc01ab1c459f7297cac88f113b45641ef2753c6287a31cf2a6066`|
| `ISSUES.md` |`a38de34ffe8b2848b96e9e8848bf5c3f638d933286d8b46bea4d10ee057cdb0f`|
| `ARCHITECTURE-DECISION.md` |`591b610a5b6b2db7caffdbbbd3f2557ba05fa1f5f36ea9d34b44e793f3a184ef`|
| `LITERATURE-KEYS.md` |`1f841a7418c628966d9c0d3e274bd04aa3c3c685b012f702a1466ab93bf5cb56`|
| `EXPERIMENT-MAP.md` |`dbfdd47c6aba5b5b5558d15a50c5f4f7c5645a30d09ac2167dcb4b16865bdfa8`|
| `ARCHIVE-PROVENANCE.md` |`f6837dd46b1fa5c5dc825729c2aadaf94af5f73f7f9c532ae256fd706796e0cb`|
| `AUDIT-DISCRETE.md` |`dccb99fdcf630e21e4135120423f9b25b16cbc2250430151a50a5844fa4174b0`|
| `REVIEW-NNLS-R1.md` |`7111c6e8eee6f5c62f12f3faf646e51a19e46a8c2e6924e52c7ab282bf796014`|
| `REVIEW-PWE-R1.md` |`ecc60aeeee585acb5894a8d1d75630e8b9a57fec3286f871c9b9310e524a0a38`|

## Targeted checks actually performed

- Scoped `rg`, `rg --files`, `cat`, `sed -n`, `nl -ba`, and `wc -l` reads
  on the assigned evidence, archived records/scripts/summaries, and chapter
  files. No original code was imported or executed.
- `python3 -I - <<'PY'` with an inline standard-library-only reader
  (`collections`, `glob`, `json`, `pathlib`) checked the eight displayed
  sparse cells by the documented deduplication/redecision rules. Assertions
  confirmed eight cells, eight seeds per cell, no unresolved outcomes, and
  the reported C1/root counts; exit status0. This read-only arithmetic was
  performed by the supporting reviewer and did not solve any node.
- `python3 -I - <<'PY'` with `pathlib` and `hashlib` read the internal
  evidence snapshots and printed byte counts/SHA256; exit status0. It
  wrote no files and imported no repository code.
- Local `view_image` inspection of the existing node-scaling PNG confirmed
  caption panel/axis/marker descriptions and the displayed series. No plot
  or data were regenerated.
- The existing package `VERIFICATION-REPORT.json` was read; its successful
  checks are distinguished above from checks performed in this assignment.
- Independent final empirical review checked all displayed table cells,
  nine benchmark ratios/intervals, the 230/19/14 figure metadata and source
  locators, the ten qualifying trace instances, and the stronger-sparse
  filtered medians by read-only arithmetic. The filtered medians are
  0.5107707694, 0.2537720062, 0.1154809093, and 0.03275410284 with
  7,8,8,8 contributors. No optimizer or original analysis script was run.

No TeX build was run by this author; integration compilation remains
root's targeted check. No CI check was inspected or represented as run.

## Concrete integration requests

The chapter already inputs all three owned table files and the existing
`figures/node-scaling.pdf`. Root's standalone build should resolve the
section references and check float placement and table widths. The source
unit correction for19537 should be retained in the coverage/review ledger.
No further experiment, new archive source, bibliographic addition, or
mathematical development is required for this chapter's stated claims.
