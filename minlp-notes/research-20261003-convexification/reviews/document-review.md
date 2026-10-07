# Independent integrated-document review

The mathematical, implementation, primary-campaign, and matched-repair
portions of the integrated document have been reviewed. This is internal
independent review, not external peer review or formal verification.

## Mathematical and implementation consistency

The support, original-row aggregation, closure, and rounding arguments match
their stated premises. Nonnegative multipliers are required for inequality
sides; the minimization epigraph and maximization hypograph use the correct
opposite signs. The complete row family describes the projected joint-graph
relaxation. The `x^2 = 1/4` example correctly shows why this need not give the
original feasible-set hull.

The polytope proof covers singular and lower-dimensional cases by choosing a
global minimizer on an optimal face of minimal dimension. A singular reduced
positive-semidefinite Hessian gives a constant direction reaching a smaller
face, so a nonsingular bordered stationary system must contain some optimum.
This justifies complete rational enumeration and its emptiness conclusion.
The fixed-dimension complexity and unrestricted-dimension MaxCut reduction
are stated separately.

The constrained-star proof handles both signs of leaf curvature and all
affine envelope switches. Its gain corollary correctly uses common center
coordinates of pair minimizers and compactness. The exact `1/128` overlap
example, its local representing measures, expanded inequality, covariance
calculation, and qualification against a dense moment relaxation were checked.
The tree-gluing discussion requires complete separator marginals, and does
not confuse scalar binary means with the joint law of a vector separator.

The separation reviewer independently checked `document/separation.tex`
against the finite-grid implementation and its coordinate-cone extension.
The document correctly distinguishes a positive-tolerance distance certificate,
an exact rational cut, an optional binary64 export that may lose strict
separation, and a bounded run that returns unresolved. Enumeration cardinality
limits do not promise wall-clock or face-enumeration limits.

The implementation chapter matches the reviewed source-model, domain,
support, and row-conversion interfaces. Source-domain witnesses are common
to all modes. Original affine implications are replayed. The submitted DAG,
later numerical SCIP operations, and complete solve certification remain
separate. The report also distinguishes the theorem's one-sided sufficient
rounding bounds from the exporter's conservative requirement for two finite
bounds when a coefficient changes.

The corrected discovery implementation is described separately from the
original frozen experiment. It abandons unfinished discovery without claiming
coverage. Bounded practical cut generation is not presented as the complete
finite separation API. Single symbolic calls remain nonpreemptive.

## Primary evidence reconciliation

The independent metric reviewer checked every primary numerical claim in
`document/evidence.tex` and the topic README, program, closeout, and verification
record against the archived records and separate audits. This includes:

- 282 completed jobs in 1,338.6 seconds; 25 of 30 new holdout models solved
  in each mode, with the same five unsolved cases.
- Summed integration and preparation times of 170.57, 187.02, and 187.12
  seconds for baseline, all, and auto; the work, coverage, and bound tables.
- 123 replayed recorded cuts, 271 checked incumbents, 14 rejected tamper
  controls, and four preserved unknown worker cut logs.
- The absence of added cuts on the five common unsolved cases and the
  positive, clearly labeled constructed root-only example.
- The 25 repair groups and 75 matched jobs, selected by the recorded defect
  criterion before corrected outcomes, with all modes retained.

The report gives the unfavorable practical result and recommends native
SCIP as the default. It does not turn equal solve counts, isolated bound
improvements, or successful certificate replay into a general speed claim.
The prospective and repair populations cannot be spliced together as one
new prospective comparison.

## Findings from document review

The abstract initially described the new experiment without giving its
completed adverse result. It now states the same 25/30 solves, greater summed
time for the cut modes, and the native default recommendation.

The program initially attributed earlier losses to graph-auxiliary
reformulation. The earlier matched control also solved 19 cases, while the
cut modes solved 18; those counts do not isolate reformulation as the cause.
The primary author removed that unsupported causal claim.

The claim map had stale campaign status text. Its author updated both the
completed primary comparison and the separately completed repair validation.
One imprecise reference to enlarging a nonlinear expression was also replaced
with the actual obligation to preserve the source nonlinear remainder.

The matched-repair table was checked against the independently audited raw
records and summary. All 75 jobs completed in 754.5 seconds, with 42 recorded
cuts and 67 returned-incumbent checks, no errors, and no unknown cut logs.
Every mode solved the same 4/8 selected full application models and 4/7
selected diagnostics. The report correctly shows zero improved full-run
bounds from cut modes in this cohort and preserves the adverse diagnostic
comparison on `waterno2_06`.

All six measured discovery overruns are marked incomplete. The displayed
maxima reconcile to the raw summary: 3.618 ms discovery, 29.529 ms callback,
and 23.611 ms total soft-budget excess. A minor rounding discrepancy in the
last displayed number was corrected. Single nonpreemptive operations remain
an explicit limitation, and discarded analysis is not called completed
coverage.

The final source and root summaries count the two current cohorts separately
before reporting 165 replayed recorded cuts and 338 passing numerical
incumbent checks. Four missing original logs remain unknown. The 75 selected
repair jobs do not replace original results or form another prospective
holdout. The same native-default decision follows from both comparisons;
no general benefit or complete SCIP certification is claimed.

All mathematical, implementation, and evidence findings are resolved. The
completed PDF has 25 pages. Text extraction confirmed that the final repair
section matches the reviewed source; rendered pages 20–21 were inspected for
table readability, missing text, and the final decision and certification
boundaries. No display defect was found. The commands were:

```sh
pdfinfo research-20261003-convexification/document/main.pdf
pdftotext -layout research-20261003-convexification/document/main.pdf /tmp/v2-review-final-pdf.txt
pdftoppm -f 20 -l 21 -r 90 -png research-20261003-convexification/document/main.pdf /tmp/v2-review-report
```

The report author's successful final build and link checks are documented in
[document/VERIFICATION.md](../document/VERIFICATION.md). The independent
[metric review](document-metrics-review.md) reconciles every reported numerical
claim. The final reviewed report, root completion records, core implementations,
review notes, and campaign evidence are pinned in
[final-review-manifest.json](final-review-manifest.json).

The recorded completion applies to the five stated program deliverables and
their supported classes. General efficient unrestricted-dimensional support,
arbitrary feasible-set hulls, and whole-solver exact certification remain
explicitly different objectives. There is no unresolved finding or required
work remaining within this review's agreed scope.
