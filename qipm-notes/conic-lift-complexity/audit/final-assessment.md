# Whole-manuscript review assessment

Root read all five independent whole-manuscript reports and checked their
findings against the source. Each reviewer personally read all 35 section
files and all four appendices. Reviewers 1 and 2 found no actionable issue.
Reviewers 3, 4 and 5 found the same missing integer-cap hypothesis in the
best capped norm-tree corollary; reviewer 3 also identified its repetition
in the independent-search construction. No reviewer identified a major
issue.

## Accepted correction

The missing integrality is a valid minor statement-scope omission.
For `N=4,d=3.5`, the written capped-tree formula yields parameter 3, but
allowed factors have dimension at most 3 and the optimal binary tree has
parameter 4. Likewise, the grouped search construction can produce a
dimension-4 factor despite a numerical cap of 3.5. The intended integer
statements and their proofs are valid.

A separate fixer must:

1. Explicitly require an integer Lorentz dimension cap in
   `cor:tree-cap-parameter` in `07-concrete-barriers.tex`.
2. Explicitly require an integer cap in the several-independent-search
   construction in `12d-query-output.tex`.
3. Add a short standing convention in `01-foundations.tex` that all
   cone-dimension and matrix-order caps are integers. Root's follow-up
   inspection found the same implicit convention in the Hermitian-cap
   example in `05-support-orbits.tex` and the discussion and order-cap
   proposition in `06-restricted-barriers.tex`. This one convention
   clarifies those uses without repeating qualifications in every
   consequence. It changes no intended mathematical model or proof.

The fixer must record the corrections and a clean qipm build in
`final-fixes.md`, preserving all historical review reports. Root will
inspect the corrected statements and final artifact before closing the
workflow. Since no accepted correction is major, another five-reviewer
round is not required by the requested process.

## Overall assessment

The reviews independently checked mathematical arguments, model and
quantifier distinctions, prior-work attribution, selected source coverage,
and organization. Three reviewers also completed isolated source-only
builds. Root independently verified that all 35 section files are included
exactly once and that the 201 linked workbench notes exactly match the
current active and parked inventory, with no broken source paths.

The manuscript's length reflects the comprehensive requested scope.
The bounded narrow-cap and nonsymmetric intervals are stated as proved
bounds rather than advertised as solved classifications. They do not
leave a proof of a claimed theorem unfinished. Novelty claims remain tied
to specific formulas and quantifiers and are qualified by the prior-work
comparison. Root accepts the reports' conclusion that no additional
substantive revision is supported by the issues identified in this cycle.
This records the outcome of the internal review, not an assertion of
infallibility, exhaustive historical priority, or journal acceptance.

## Closure

The separate final fixer applied all three accepted edits. Root inspected
each changed passage, the correction report, and the clean build results.
The final PDF has 183 pages, 499 unique labels and 87 references, with no
unresolved references, citation errors or final LaTeX warnings. Root also
independently checked the included-file set and inspected rendered pages
1, 42, 123, 135, 149 and 183. The corrected hypotheses and principal
formulas are legible and intact. Source and PDF hashes are recorded in
`root-final-artifact.json`.

All accepted findings are addressed. The required staged review cycles
and the separate five-reviewer whole-manuscript cycle are complete.
