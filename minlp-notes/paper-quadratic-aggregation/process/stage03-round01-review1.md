# Stage 3, round 1: independent review 1

Verdict: mathematical content is acceptable; correct one minor development-
record inconsistency. No major issue identified. This review covers all
stage-3 manuscript additions and the exact-check script, with particular
attention to actual versus closed Shor projections. It does not certify the
deferred formal-consequences or frontier contributions.

## Major findings

None.

## Minor findings

1. **Stale live coverage status and stage number.**
   `process/coverage.md:207–212` still labels stage 2 as awaiting its five
   reviews and says that stage 3 remains unwritten. This contradicts both
   the current additions immediately above and `PROCESS.md`, which records
   stages 1–2 accepted and stage 3 authored. `coverage.md:238–239` also
   assigns portable formal packaging to stage 5 although the revised process
   assigns it to synthesis, stage 7. The same obsolete stage-5 packaging
   number remains in the live `FORMAL-VERIFICATION.md` planning paragraph.
   **Fix:** update the live coverage status to accepted stage 2 / authored
   stage 3 and refer to “the synthesis stage” for future packaging (or use
   stage 7 consistently). Historical author reports need not be rewritten.
   This is a documentation consistency issue, not a mathematical defect.

## Detailed mathematical assessment

### Closed systems, regimes, and finite SDP characterization

The closed-system properness equivalence uses exactly strict feasibility
and AHC, and only the appropriate hull inclusion and nonconstant convex
aggregate argument. It does not silently identify the ordinary closed-system
hull with the closure of the strict-system hull. The separate n>=2 emptiness
and n>=3 full-description qualifications are correct. Perturbing a strict
homogeneous feasible point at t=0 to nonzero t justifies the emptiness
equivalence, and the image-separation argument does not need closedness.

The trace reduction to 2n+1 objectives is valid. PSD plus zero trace forces
zero matrix, and the two signed objectives for each linear coordinate force
that coordinate to vanish everywhere on the compact feasible slice. The
empty-slice branch is present, and the text does not infer exact zero from
small floating-point values or assert a bit-complexity result.

### Shor closure and whole-space equivalence

Independently checked each identity and implication in
`prop:shor-closure`:

- Writing X=xx^T+Y identifies membership with `-f(x)` in
  `C=image(PSD)+R_+^m`, with the correct sign of the orthant.
- The dual cone is exactly K, and the bipolar theorem gives the closure
  rather than membership in a possibly nonclosed C.
- The proof of `cl(C)+int(C) subset int(C)` is valid: a sufficiently close
  cone point supplies the claimed ball containment, and conic convexity
  gives closure under addition and positive scaling.
- The quadratic mixing identity has a **positive** covariance term
  `t(1-t)g(x-x0)`, which belongs to C. Strict feasibility places `-f(x0)`
  in its interior. Hence points on the open segment from an aggregate-
  feasible point to x0 have actual Shor lifts. This proves closure equality.
- In the trivial-certificate case, extrapolating to `2x-x0` and taking
  t=1/2 correctly puts the arbitrary target x in the actual projection.
  The argument establishes `P_SDP=R^n`, not merely dense projection.
- The converse uses properness of a nonconstant convex quadratic sublevel
  set. The subsequent AHC hull corollary has all needed feasibility
  assumptions and does not imply full relaxation exactness.

Both nonclosed-projection examples are correct. In the two-row example,
zero first covariance diagonal at x1=0 or 1 forces zero covariance cross
entry. This excludes x1=0 entirely and leaves precisely x2<=-1/2 at x1=1.
For every interior x1, the displayed rank-one covariance realizes any x2.
In the compact four-row variant, the aggregate PSD condition is exactly
lambda1=lambda3. This gives the stated closed aggregation strip; the lift
with X12=-3/4 gives its half-open part, while x1=1 permits exactly
[-1,-1/2]. The original T is compact since x1 is bounded away from zero;
the displayed strict feasible point satisfies all four strict rows.
Thus the compact variant addresses the standing compactness convention
in the cited Kojima–Tunçel source. No HHC assertion is made for that variant.

### Checkable hypotheses and counterexamples

The hyperplane-restriction perturbation formula has the correct mixed-term
coefficient. Stable convexity gives AHC by convergence; the Dines and
three-form PDLC consequences preserve their dimension conditions. The
Schur-complement comparison between the spans of A and Q uses a genuinely
negative constant trivial aggregate, hence correctly requires strict
feasibility at that step.

The AHC-not-HHC and HHC-not-stable examples have the claimed midpoint
obstructions. The four-row ordinary-hidden-convexity example has the stated
convex images, trace obstruction, and bounded planar projection. Both
linear image maps used in its four- and three-row variants are injective,
so their hyperplane midpoint obstructions follow. The three-row proper
affine bound and unbounded feasible line are consistent. The closed-system
example has an interior convex hull, only trivial convex aggregates, HHC,
and no good closed-system multipliers: the strictly negative scalar block
and indefinite 2x2 block contribute two negative eigenvalues. Its BDS
comparison uses the correct G-based good-multiplier definition. The strip
example's strict hull and Shor witness are correct.

### Application and exact checks

The local-margin/global-validity distinction is correct. A tangent at any
box point separates that point; a tangent at a box minimizer excludes the
whole box by the first-order optimality inequality. The DD and affine
minimum lifts define a linear program and optimize exactly the stated
margin over normalized DD aggregates. Degenerate box sides do not break
the formula. The rational weighted-square identity proves PSD.

Signed affine equality multipliers are legitimately added to the exact
affine estimator. The common normalization includes equality-only
certificates and prevents the exhibited unbounded-margin scaling.
Conditional rows retain their supporting conjunction. The rational example's
estimator identities, root lifted witness, definite aggregate, tangent,
activation witnesses, DD interval, two increasing margin pieces and optimum
1/35 all check out. The normalized comparison with weights (2,1) is correct.
Pure-bilinear curvature and common-Shor limitations are accurately stated.

The standard-library script checks actual rational coefficient identities
and stated finite witnesses; it is not represented as proof of universal
geometric statements. No solver performance or unverified novelty claim
is inferred from it.

## Literature and integration checks

Read the updated bibliography, literature followups, coverage additions and
root closure audit. Rechecked the primary Fujie–Kojima text at Conditions
1.2/1.4 and Theorem 2.1: the manuscript imports the qualified closure
equality correctly, and its epsilon-I Slater construction works. Rechecked
Kojima–Tunçel's standing compactness and Theorem 4.2 in the primary extract;
the cited unqualified equality and omitted-closure dual identity are indeed
there. The paper's independent proof and limited comparison are justified.
Rechecked BDS v2 Theorem 2.24/Remark 2.25 against the primary extract.
The thesis definition of stable convexity matches the manuscript, and the
local Berthold–Witzig primary text supports the limited local-proof and
nonlinear-aggregation attribution. Polyak and Dong access/version limits
are accurately separated in the literature record; this reviewer did not
make a new exhaustive novelty search or inspect their PDFs afresh.

`main.tex` includes the three new mathematical sources but does not input
the deferred formal-consequences fragment. The stage-3 destination map
covers the authorized canonical consequences and application.

## Checks actually run

- Read all stage-3 mathematical additions, the complete rational-check
  script, author report/snapshot, bibliography, relevant literature/coverage
  updates, current main input list and process plan.
- Targeted primary-text `rg`/`sed` reads in `/tmp/fk.txt`,
  `/tmp/quadratic-paper-literature/kt.txt`, BDS v2, the Sheriff thesis
  extraction, and the local Berthold–Witzig full text.
- `python3 paper-quadratic-aggregation/supplement/check_examples.py`:
  **PASS**.
- Independently compared SHA-256 hashes of all 13 files recorded in
  `stage03-author-snapshot.json`: all match.
- Searched the dedicated final `build/stage03/main.log` for warnings,
  undefined references and overfull/underfull boxes: no matches.

No redundant Lean run, project-wide check, CI inspection, source edit,
subagent, or other current reviewer-report read was performed.
