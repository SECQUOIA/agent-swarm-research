# Stage 3, round 1: independent review 05

Reviewer: reviewer05. Date: 2026-09-07.

## Snapshot, scope, and recommendation

Frozen source: `process/snapshots/stage03-round01/`.
The manifest SHA-256 is
`0d1eb5b7c2a0869ef020289146fcd8c44227b95aef249b2ed3bb3bbdc3b0f956`.
All eight source entries independently match their recorded hashes.

I read the complete new section, all integration changes, bibliography, README,
and coverage record, and revisited the accepted compression, sampling,
attainment, low-rank cover, and convex-combination prerequisites used in the new
proofs. I compared the new section with the two canonical robustness and screening
results. I did not read other stage 3 reviews, coordinate findings, delegate,
or edit manuscript sources. Builds and diagnostic outputs are isolated under
`verification/reviewer05/stage03-round01/`.

**Recommendation: pass.** No major or minor correction is required on the
evidence checked. The two new refinements are justified: moving shared normals
do not change constant local KKT matrices, and the overlapping simplex cover
preserves the transition-union argument without needing a triangulation.

## Major findings

None found.

## Minor findings requiring correction

None found.

## Mathematical checks

Locations in this section refer to `sections/03-robustness-screening.tex` in
the frozen snapshot.

### Robustness and witness arithmetic: lines 13–209

The model fixes measurements separately for each criterion and explicitly permits
their combined rank and criterion count to grow. Its universal rows do not
filter the near-optimal set, and its budget uses the true nominal global value.

The measurement-fiber threshold lemma is correct in both directions. Existence
of a near-optimal point implies that the compact fiber's global minimizer is
within budget and has a polyhedral KKT representation. Conversely any feasible
fiber KKT candidate within the nominal budget is already a near-optimal point.
Thus fiber global comparison is unnecessary, while nominal global comparison
remains essential. The proof correctly avoids claiming that the resulting
adversary is stationary for the unrestricted follower.

The enlarged parameter box can be computed with polynomial encoding length from
compact-core polynomial bounds. Adding the measurement equations increases both
parameter and multiplier dimensions only by the fixed per-criterion count.
The candidate's value coordinate is its actual follower cost. Eliminating each
criterion separately before conjoining upper-row formulas prevents a growing
number of adversarial variables. One shared nominal-value variable then suffices.

At every feasible leader the near-optimal set is nonempty and compact. Therefore
its criterion maximum exists. The worst-value formula and the inherited infimum
construction handle finite values and attainment correctly even for moving
normals. Sampling one leader, nominal value, worst value, measurement, and fiber
candidate together gives the required common field; rational decoding recovers
all coordinates. Separate criterion requests do not promise a joint field for
unrelated witnesses. The irrational witness example has the stated endpoint
`1/sqrt(2)`.

Corollary 3.3 is a valid extension of Corollary 2.9. Constant local `Q_b,E_b,G_b`
give constant rational KKT inverses. Moving shared and measurement normals enter
effective costs and consistency equations, rather than those inverses. Candidate
and criterion degrees therefore depend only on numerical input degree and the
fixed dimensions. Each criterion has a fixed elimination depth; performing many
independent criterion computations does not turn that depth into the criterion
count. The final joint sampling and rational decoding preserve the bounded
degree. No attainment claim is silently imported.

### Attainment and negative examples: lines 213–320

The convex fixed-normal proof establishes continuity on the follower-feasible
leader domain, which is compact. Its Hoffman approximation applies only to
nonempty fibers. Strict convexity gives a unique continuous nominal minimizer
and continuous nominal value. Near-optimal response approximation is correctly
split into zero-budget and positive-budget cases: nominal solutions handle the
former, and convex mixing gives strict budget slack before Hoffman repair in
the latter. The diagonal-sequence argument recovers any boundary response.
Closedness plus this approximation property gives continuity of all worst
criteria and consequently robust attainment.

The positive-budget counterexample is algebraically consistent. I checked the
factorization, derivative, root `(1+sqrt(17))/16`, and the range restriction on
the derivative estimate. For `c>rho`, the cost increases then decreases to an
endpoint value above the budget, leaving only the initial interval sublevel
set. The estimate leading to `4x+a_c>a` has the correct direction and strictness.
Both versions have the asserted unattained infimum despite unique nominal
responses and a positive budget.

The Max-Cut transfer uses a budget large enough to include the entire unit cube.
Convexity bounds the quadratic criterion by its maximum at binary vertices,
where it equals cut size. The robust threshold `K-1` exactly complements the
integer cut threshold `K`. A violating binary vector supplies membership of the
complement in NP on this restricted family, so the coNP-completeness statement
has the right decision direction and scope.

### Enclosure, closure certificates, and recovery: lines 325–524

Subtracting the paired variational inequalities gives the claimed ellipsoid.
Completing the square and applying the directional Cauchy–Schwarz bound gives
the correct signs and factors of one half. In particular, the true gradient
center is `ghat+p/2`, while the response center is `y-Q^{-1}p/2`.

The maximum defining `eta_P` is attained at a vertex because its quadratic is
convex and the cell is a compact polytope in fixed dimension. Vertex enumeration
also supplies the affine extrema, so the stated screening implementation need
not call extra LPs for those extrema. The strict gradient tests force the
correct lower or upper bound. The `F` label means zero gradient and permits
zero-gradient bound points in later reconstruction.

The weaker closure certificates are sound. A nonnegative affine function that
is not identically zero is positive throughout the relative interior, including
for lower-dimensional cells. The paired strict-somewhere conditions therefore
give interiority there. Continuity of the true response, derived from the two
variational inequalities, extends zero gradient to the closure. The analogous
bound-label extensions use the same argument. The strict-somewhere conditions
cannot be dropped and are retained.

Every completed assignment uses the true dense principal submatrix `Q_FF`.
It is invertible even when the certified free set is large, with polynomial
rational elimination cost. The recovery LP checks all remaining true KKT signs
and weak bounds and includes the original upper rows. Thus it is sound. For
completeness, an ambiguous coordinate can be labeled by its true gradient sign,
using `F` when the gradient is zero. This includes zero-gradient bound ties.
Compactness of each cover polytope gives attained rational LP optima.

The `M*3^t` bound counts only recovery LPs and explicitly excludes cover
construction and screening. The total fixed-rank-surrogate bound incorporates
those polynomial costs. A failed whole-cell assignment guess is correctly kept
available on a smaller feasible part during recovery; it is not used as an
infeasibility certificate.

### New simplex cover and explicit radius: lines 528–626

The leader projection is injective on each surrogate graph cell because the
surrogate response and aggregate are unique. The relative-interior kernel
argument correctly extends injectivity to its affine hull, bounding cell
dimension by leader dimension.

All affinely independent vertex subsets of size at most `r+1` form a polynomial
simplex cover in fixed dimension. The accepted finite-convex-hull reduction
proves coverage; overlapping simplices are harmless for both certificates and
the union of recovery LPs. These simplices introduce no new vertices, so their
transition-coordinate union has size at most `(r+1)q`.

A coordinate outside that union has strictly positive nominal margins of the
kind appropriate to its original clipping label. The minimum `sigma` is taken
over a finite rational list and extends over each simplex by affine
interpolation. The empty-list convention is safe because in that case there
are no margins requiring preservation.

The induced infinity norm and symmetry give the stated spectral estimates for
`m0` and `L0`. The radius first preserves positive definiteness and then makes
both response and gradient perturbation bounds at most `sigma/2`. Consequently
every nontransition label is sound on the entire simplex. Those norm-based
certificates need not be rediscovered by the ellipsoid tests. All constructions
have polynomial bit complexity for fixed dimensions, while the simplex cover
can increase the polynomial exponent. The result makes no claim of a uniform
large neighborhood or automatically bounded transition multiplicity.

### Inner/outer bounds and limitations: lines 631–693

The signed directional formula gives the correct inner sufficient and outer
necessary row conditions. Outward rational radius rounding preserves both.
Minimizing lower objective enclosures over outer LPs gives a global lower bound;
minimizing upper enclosures over inner LPs gives a truly feasible leader and an
upper bound when an inner LP is feasible. Empty outer LPs certify infeasibility,
whereas empty inner LPs do not. Representing equalities by both signs does not
remove the acknowledged failure of inner approximations to find exact equalities.

Both small-perturbation examples are correct. In the rank-one symmetric example,
the displayed ellipsoid tests fail for every coordinate although the complete
all-`F` assignment immediately verifies the true affine response. In the scalar
example the upper switching point moves from `1/2` to `(1+eps)/2`, making unchanged
surrogate status reuse unsound on part of the old cell. These examples support
the stated limits without turning conservative screening into a hardness claim.

## Source, integration, and coverage checks

The new section covers the canonical measurement-fiber, robustness, attainment,
Max-Cut, perturbation, whole-cell screening, exact recovery, quantitative
neighborhood, and approximate-bound developments. Its coverage table identifies
the two new refinements and keeps stage 6 experiments and total measured costs
as later obligations. No current stage omission was found.

The appendix's added attribution agrees with the local primary text:
`[[gritzmann1993-minkowski-addition-of-polytopes-computational]] p.13-14`,
Algorithm 2.3.6, Theorem 2.3.7, and Corollary 2.3.10, describe shared support
direction arrangements, compatible maximizing summand vertices, and polynomial
binary complexity in fixed dimension. The manuscript distinguishes its
polynomially varying core and common-field recovery from that predecessor.

The added related-work claims were checked against the cited primary records:

- [Liu et al., PMLR](https://proceedings.mlr.press/v32/liuc14.html) supports the
  variational-inequality safe-screening attribution and bibliography metadata.
- [Dantas–Gribonval, inspected v3 record](https://arxiv.org/abs/1812.06635v3)
  describes structured dictionary approximation with safe original-support
  screening and confirms the journal reference.
- [Arnström–Axehill, v2](https://arxiv.org/abs/2003.07605v2) describes identifying
  working-set subproblem sequences for every parameter and supports the
  parameter-region complexity attribution.
- [Besançon–Anjos–Brotcorne, Section 2](https://arxiv.org/html/2011.00824)
  explicitly gives the objective-robust near-optimal variant through an
  epigraph formulation; its complexity discussion is separated from a
  fixed-structural-dimension optimization theorem.

The two publisher DOI pages for the 2021 robustness and 2019 screening papers
failed in the browser. Their accessible primary arXiv records were used instead.
No bibliographic change is inferred from that access failure. The older
literature audit was used for source context, not as a substitute for the new
mathematical review.

## Build, visual checks, and diagnostics

The clean isolated README build succeeded with exit code zero:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

It produced a 27-page PDF with no final warnings, undefined references/citations,
or overfull/underfull boxes. I visually inspected all new-section pages 13–22,
the changed appendix ending, and bibliography pages 25–27. Formulas, screening
table, indices, accents, and citations are readable without clipping or overlap.
The source-level prerequisite changes were also inspected; the earlier short
lemma pagination and redundant Adler–Beling URL suggestions have been addressed.
The final reference list has 20 entries.

I reran the two README diagnostics with their outputs redirected into the
private verification folder; both exited zero. The robustness diagnostic checks
measurement-fiber examples, nonstationary adversaries, the positive-budget
polynomial identity, and the finite Max-Cut transfer cases. The screening
diagnostic checks 24 instances/61 cells against full assignment enumeration,
including 918 directional checks, singleton degeneracy, weak closure, and the
eight-coordinate transition example with observed ambiguity two. Their raw JSON
outputs are retained as `nearoptimal-diagnostic.json` and
`screening-diagnostic.json`. These are reruns of existing diagnostics, not new
independent implementations or general proof certification.

## Limits and optional suggestions

The general quantifier-elimination algorithms and every external predecessor
were not reimplemented or re-proved. The new constant-degree and simplex-cover
claims were assessed from their full proofs and accepted prerequisites; the
finite diagnostics do not independently establish those general claims.
Unwritten later stages are not omissions from this stage gate.

Optional final-layout suggestion: keep the statement of Theorem 3.1 together
if practical; its final witness-field qualification currently continues on
page 14. The qualification is present and clear, so this does not require a
stage correction.
