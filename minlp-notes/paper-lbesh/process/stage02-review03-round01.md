# Stage 2 independent review 03, round 01

Reviewer: `/root/reviewer03`. Date: 19 September 2026.

## Verdict

No major issue found. Approve the Stage 2 mathematics and implementation account after three minor numerical-description corrections below. These are corrections to what the frozen implementation checks and to the limits of its floating-point interpretation. They do not invalidate the exact-arithmetic propositions or establish a defect in the retained benchmark outcomes.

I read no other current Stage 2 review, changed no manuscript/research source, and spawned no agents. The lead separately asked me to assess normalized hull points leaving their box; issue 3 records my independent assessment of that concern.

## Major issues

None identified.

## Minor actionable issues

1. **Nonfinite-value checks are narrower than stated.** `sections/algorithm-and-implementation.tex:15–16` refers to a finite usable anchor and says “Nonfinite violations or fallback coefficients raise an evaluation error.” The explicit finite check in `code/minlp_solver_lab/lbesh/solver.py:316–318` applies to the candidate value. The anchor test at line 321 and bisection comparisons at lines 327–331 do not check finiteness; a NaN midpoint value follows the nonpositive branch. Fallback coefficient finiteness is checked at lines 341–343. Change the sentence to distinguish nonfinite candidate values and fallback coefficients from unchecked intermediate evaluations, and avoid implying a certified finite-anchor test. A short qualification in the following paragraph is enough. This is a documentation correction for the frozen code, not a request to silently alter the experimental solver.

   A targeted solver-free probe confirmed the difference: a fake row returning finite values at the anchor/candidate, NaN at every intermediate point, and finite tangent coefficients returned one cut without raising. It ended at the exterior endpoint. The probe does not model a valid mathematical convex oracle and is not evidence that a benchmark produced NaNs; it checks the documented implementation failure contract only.

2. **An approximate exterior endpoint is not exactly a boundary point.** `sections/algorithm-and-implementation.tex:20` says the rowwise line search's “boundary point belongs to the boundary of that row's sublevel set,” immediately following the finite bisection rule at line 15. The code uses `z = point(hi)` (`solver.py:334`), which can remain strictly outside the row set. Say that the *exact root* lies on that individual row boundary and that the implementation linearizes at its approximate exterior endpoint. Preserve the useful distinction from the full multirow disjunct. The approximate-root validity discussion in `separation-theory.tex` already provides the right mathematical explanation.

3. **State the numerical box issue for normalized hull points.** `sections/algorithm-and-implementation.tex:14,20` and the numerical/input scope discussion at lines 66–71 should explicitly qualify the direct normalization. `solver.py:369–381` computes `nu/lambda` without projecting or verifying membership in the term's box. Scaled-bound feasibility errors may therefore be amplified when lambda is near the cutoff. For example, for original upper bound one, lambda = 1.01e-6 and nu = lambda + 1e-6 give an upper-scaled-bound residual 1e-6 but normalized point approximately 1.9901. A function certified convex and safely evaluable on the stated box need not have valid supporting tangents at such a point; finite function/gradient values alone do not settle that question. Add a concise statement that the exact results presume in-domain points, while the frozen numerical routine does not certify that premise after normalization. The current text already disclaims certified floating-point cuts, so this is a missing specific qualification, not a major claim reversal. I found no recorded counterexample, invalid cut, or contradictory bound caused by this risk, and did not infer one from the possibility.

## Mathematical review

I independently checked every displayed proof in the four Stage 2 section files against its hypotheses.

- The bounded-domain perspective identity, coefficient differentiation, inactive-origin convention and all-tangent equivalence are correct. The empty-term qualification avoids confusing closure of an empty positive-weight feasible lift with the intended inactive point.
- The separate-disjunction hull proof correctly groups convex combinations, preserves the continuous versus original-integer distinction, and does not assert the hull of the entire GDP intersection.
- The bounded epigraph proposition correctly preserves an optimal lift rather than every original epigraph point; the implementation limitation is stated.
- The ESH margin follows from the anchor supporting inequality and the gradient bound along the segment. Both transformed and untransformed normal bounds are adequate for the compact packing arguments.
- Integral and residual-calibrated fractional finite rejection are conditional on retained valid cuts and old-cut-feasible candidate points. Fixed positive cutoff termination and its weaker residual guarantee are correctly distinguished. No hull conclusion is improperly applied to fractional big-M points.
- The repair formula and weighted bounds are correct for nonempty terms with suitable anchors. The square-root intersection example correctly defeats a linear objective-error inference from separate-term interiors.
- Value convergence uses compactness and vanishing residuals, preserves original integrality in the integral case, and supplies no unsupported rate or fixed-tolerance exact result.
- The single-tree theorem states the substantial solver/lazy-cut contracts needed by its proof, including repeated callbacks and optional refinement, and explicitly avoids asserting them for the frozen numerical implementation.
- The arithmetic relaxation loses at most 2E in generating violation as stated; subtracting later stored-cut tolerance gives the claimed packing margin.
- Fixed-anchor representation invariance, same-point ECP weakening, scalar recurrence/transient, Newton expansion, centered ellipsoid comparison, and the two opposite disk witnesses are algebraically correct and appropriately limited.

## Source correspondence checked

Read `process/stage02-author.md` and all four new sections with numbered lines, then inspected relevant methods in `lbesh/solver.py`, all master construction/cut/integrality methods in `lbesh/master.py`, and extraction/bounds/scope paths in `lbesh/structure.py`.

The following manuscript details agree with the source: rowwise rather than max-row bisection; full affine tangent constants; shared ESH/ECP anchor initialization; four deterministic anchor starts and the stated slack/strictness thresholds; 31 initial tangent attempts; default LP/integer cutoff 1e-6 versus optional node cutoff .05; no residual-calibrated cutoff in the frozen code; LP residual diagnostics include all positive weights; six-entry stagnation comparison and 200-iteration cap; multi-tree NLP-solution cuts versus single-tree heuristic submission; integer-assignment caching and failed-NLP nonexclusion; normalization and full primal validation; original objective recomputation and epigraph reset; symmetric internal gap test; error/status distinctions; and overlapping component timers.

The nonlinear epigraph's absent upper bound, optional user cuts' absent total cap, and unverified old-lazy-cut-feasible generation premise are all identified rather than hidden behind the mathematical theorems.

## Checks actually run and limits

- Read-only `cat`, `sed`, `nl`, and `rg` inspections of the four manuscript sections, author record, and targeted implementation modules.
- A single inline probe under `code/minlp_solver_lab/.venv/bin/python`, importing `LBESH` and calling `_esh_cuts` on an object built with `__new__` and a fake row. It checked the finite-intermediate-evaluation failure contract described in issue 1, without constructing a master, invoking an optimizer or editing a file. Result: one finite cut returned; no error raised.
- The normalization example in issue 3 is direct arithmetic, not an observed solver candidate.

No LaTeX build, benchmark rerun, original-model witness audit, project-wide check, or CI inspection was performed. No new literature assertion was introduced; the review concerns elementary derivations and correspondence to local frozen sources.
