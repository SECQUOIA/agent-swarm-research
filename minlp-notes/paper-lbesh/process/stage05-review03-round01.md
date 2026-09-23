# Stage 5 whole-manuscript review, reviewer 03, round 1

Date: 19 September 2026. Independent review of the frozen complete manuscript and delivery described by `stage05-author.md` and `stage05-round01-source-sha256.json`. No other current final-review report was consulted. No manuscript or research source was edited.

## Verdict

**No major issue found; accept the scoped scientific work after one minor correction to the definition of recorded separation time.** The paper presents a defensible matched computational investigation rather than a new cut family. Its modest empirical benefit, substantial negative ablation, conditional theoretical statements, limitations of floating-point runs, and relationship to close prior work are consistent across the full manuscript. I do not see a mathematical or empirical defect requiring a new method or a new computational campaign for the stated contribution. This judgment is not a prediction of a particular journal's acceptance.

## Required minor correction

### M1. The recorded cut timer is narrower than “total cut-generation time”

**Severity: minor, factual measurement-definition issue.**

- `sections/abstract.tex:2` says “mean total cut-generation time increases by factors of 5.5--6.6.”
- `sections/results.tex:24` calls this the mean “total cut-generation time per run,” and the figure caption at line 32 repeats that scope.
- `sections/algorithm-and-implementation.tex:75` describes separately recorded construction/NLP/cut times without defining which cut work this particular timer includes.
- In `code/minlp_solver_lab/lbesh/solver.py:307–345`, the timer starts inside `_esh_cuts` at line 312 and accumulates at line 345. It measures that routine's row checks, boundary searches and linearization/coefficient work. It excludes initial tangents (`_initial_cuts`, around lines 589–667), tangents at NLP solutions (`_cuts_at_solution`, around lines 551–576), work outside the routine in `_separate_point` (from line 348), and installing transformed cuts in the master/callback. An AST check found no other update to `time_cuts` besides its initialization and the accumulation in `_esh_cuts`.

The numeric comparison is correct for the recorded field. Fresh arithmetic on the primary held-out common-solved records gives mean-time ratios 6.632235, 6.505443, 6.128555 and 5.479943 for hull single, hull multi, big-M single and big-M multi, respectively. The problem is the unqualified word “total”: readers can reasonably take it to include all generation of the cuts counted elsewhere in the same table.

**Fix:** Define `time_cuts` once as cumulative time inside the row-separation routine and name its exclusions. Replace “total cut-generation time per run” with “recorded row-separation time per run,” or another equally precise term, in the abstract, results and caption. Align the figure title/table label if necessary, or make their abbreviation explicitly refer to that definition. Preserve the existing warning that this is not a per-cut cost ratio and that timers overlap. No changed numeric result or optimization rerun is needed; rebuild/regenerate/package the corrected presentation normally.

## Whole-manuscript scientific assessment

### Contribution, prior work and interpretation

The main question is clear: whether rowwise boundary search pays for its extra expense when embedded in the same GDP solver machinery as direct point tangents. The paper attributes established ESH/ECP, perspective cuts, hull/big-M formulations and solver architectures to prior work. It makes no priority claim for a new cut family, first GDP/ESH combination, or new universal convergence result. The matched implementation and evidence are the contribution, accompanied by explicit theoretical contracts and representation diagnostics that help interpret it.

I freshly spot-checked the local primary SHOT article and the computational perspective-cut article against the discussion of ESH, primal NLP heuristics, single/multiple-tree methods and existing perspective-cut studies. These support the paper's narrow attribution. The SHOT repository resource is identified as software documentation rather than treated as a new mathematical article. I found no new factual doubt that required an additional internet search during this final pass. This is not a claim to have exhaustively ruled out all related publications.

The modest timing improvements are not overstated: equal external accepted counts, family reversals, small/related strata, changed scheduling with unchanged search seeds, selection on common-solved cohorts, cone-interface failures, mixed conic coverage, and the absence of a general conic-OA comparison are visible. The paper does not infer a population speedup or a causal mechanism from aggregate counters. The much poorer no-integer-NLP ablation is prominently retained, with interior NLP initialization correctly distinguished from recovery NLPs.

### Mathematical checks

I reread the complete model/cut section, guarantees overview, full separation appendix and oracle-diagnostic appendix, and checked the principal derivations:

- Bounded perspective closure, including the explicitly retained inactive origin for empty terms; separation of original integrality from term-set convexification; sparse-copy equivalence; and the distinction between separate disjunction hulls and the full GDP hull.
- Complete tangent characterization and valid bounded-box big-M coefficients; the conditional objective lift and the fact that it is not an implemented compact artificial epigraph.
- The strict-interior radial margin, coefficient bound and finite rowwise compactness/packing argument; continuity of weighted residuals at zero weights; residual-calibrated omission versus a fixed denominator threshold.
- The repair argument, intersection counterexample, compact cluster-point value argument and conditional single-tree old-cut/auxiliary-work contract. None silently asserts a linear objective-error bound or a prototype-wide exact convergence guarantee.
- Coefficient/evaluation error allowances; exact boundary versus numerical exterior endpoints; and the explicit lack of a floating-point domain/convexity guarantee after normalization by small selection weights.
- Fixed-anchor invariance under the stated equivalent-row transformation, point-cut weakening, scalar/Newton recurrence and strict transient comparison, centered ellipsoid calculation and off-center non-dominance examples.

No false implication or missing assumption was found in these arguments. The concise overview agrees with the appendix statements. The model/cone appendix is consistent with the stated bounded domains, zero-weight closure, scalar exponential-cone representations and quadratic perspective lift.

### Actual solver and evidence

The manuscript continues to distinguish mathematical statements from the implemented numerical contract: rowwise roots, common initialization, ECP fallback, a fixed normalization cutoff, limited LP phase, optional user cuts, integer-point NLP recovery, scaled acceptance and the different outer/inner tolerances. Finite gap acceptance is not called an exact certificate. The failure statuses and interface limitations remain visible.

I rechecked the overall accounting and presentation against the compact study evidence and the checks from my earlier reviews: 1,464 records in eight benchmark batches, separately 420 cone-reference calls, 51 generated controls with the 18/33 split, 27 external models, three single-tree schedules, distinct primary and follow-up outcomes, and the declared reference chronology. The primary/repetition cohorts, numerical ranges in the abstract, common-solved timing qualifications, and means versus medians agree across text and tables. The paper does not count related seeds or scheduling repetitions as independent samples. The newly recomputed timer ratios are reported above; the timer's scope is the only new factual correction found.

### Organization, readability and package

The main text supplies enough mathematical context for the computational question while moving the full derivations and model/reproduction detail to appendices. The discussion and conclusion explain both relevance and limitations. All 17 tables and the appendix descriptions are consistent with the narrative. I visually inspected the rendered page 19 as an additional layout spot check; the table and surrounding text are legible and unclipped. This is not an all-page visual certification.

The README and reproduction appendix correctly separate a local-reference manuscript build, table regeneration, saved-witness revalidation and a fresh optimization campaign. They do not claim a fresh-environment installation or repeated performance experiments. Solver licenses, external packages and the reused pinned environment are acknowledged. The package is appropriately standalone for its paper/proof/evidence use while separately shipping the frozen research archive. I verified every one of the 68 frozen source/delivery hashes in the Stage 5 fingerprint. Consequently earlier accepted relocation results apply to unchanged bytes; I did not present those checks as newly rerun in this review.

## Checks actually performed and limits

- Read the Stage 5 author handoff/fingerprint; all manuscript sections and appendices; all 17 generated tables; current README/reproduction instructions; literature ledger; selected primary local literature; and relevant solver timer/cut code.
- Used a standard-library Python SHA-256 loop to verify all 68 entries of `process/stage05-round01-source-sha256.json`: all matched.
- Used an AST inspection of `solver.py` to identify all `time_cuts` writes; confirmed only initialization and `_esh_cuts` accumulation.
- Recomputed the four primary paired arithmetic-mean `time_cuts` ratios from compact records; results above retain the manuscript's rounded numerical range.
- Rendered PDF page 19 with `pdftoppm -f 19 -l 19 -scale-to 1400 -png -singlefile paper-lbesh/main.pdf /tmp/lbesh-stage05-review03-page19`, then visually inspected that temporary image.
- Read-only searches and numbered source inspections supplied the cited locations. One attempted read used the incorrect prefix `paper-lbesh/code/...`; I corrected it to the repository's `code/...` path. No conclusion relies on the failed read.
- No optimizer run, full witness audit, source build, table regeneration, fresh dependency installation, project-wide test, CI inspection or new exhaustive literature review was performed. The scope was full scientific rereading plus targeted independent checks, not a redundant rerun of the previously audited campaign.
