# S1 lead adjudication

All five independent reviews are complete. Reviewers 1, 2, and 5 requested no corrections. Reviewers 3 and 4 independently identified the same minor source/terminology issue in the algebraic sampling primitive. No reviewer identified a major issue.

The lead read all three current foundation sections and all five reports. I accept the common finding: the primitive should state the cited connected-component sampling guarantee rather than describe samples in decomposition cells. This is minor because every current application only requires a point satisfying a nonempty quantifier-free formula, with a common real univariate representation. The component guarantee supplies exactly that. No face count, degree bound, recovery proof, or theorem conclusion relies on constructing those cells.

Required correction S1-C1: replace the first sampling guarantee in `prim:a-pre-sample-points` with samples meeting every semialgebraically connected component of every realizable sign condition of the input polynomials. Retain the polynomial fixed-dimension bit bound and common real univariate representation. Check nearby wording and all invocations for consistency. Rebuild Paper A and refresh the stage build evidence.

The literature comparisons and the expanded corpus map withstand the stage review. Current SRS-status corroboration is recorded in the literature screen; a new citation is optional, since the mathematical background already cites appropriate primary sources.

No five-reviewer repeat is required by the user's process because no valid major issue was identified. A separate correction agent must implement S1-C1 and the lead must verify it before closing the stage.

## Stage accepted

The separate correction agent implemented S1-C1 and rebuilt Paper A cleanly. The lead verified the revised primitive, checked the four downstream uses described in the correction report, and confirmed that all recorded input hashes match the current source. S1 is complete with no outstanding accepted findings. Stage 2 may begin.
