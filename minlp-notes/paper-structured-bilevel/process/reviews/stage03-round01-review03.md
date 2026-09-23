# Stage 3, round 1 — independent review 03

Snapshot: `process/snapshots/stage03-round01`.
Manifest SHA256: `0d1eb5b7c2a0869ef020289146fcd8c44227b95aef249b2ed3bb3bbdc3b0f956`.
The digest and all eight listed file hashes were independently verified.

**Recommendation: PASS. No actionable major or minor findings.**

I read the complete new section, integration changes, bibliography additions, README, and coverage inventory. I rechecked the relevant accepted response, field-degree, and convex-combination prerequisites against the new uses. The exact-response section is byte-identical to the section I reviewed in stage 2; the foundations change is layout only, and the appendix adds attribution rather than changing its recovery proof. I did not consult any other current stage 3 report, delegate, edit manuscript sources, or substitute historical PASS records for this review. Later-stage experiments and accuracy theorems are not current omissions.

## Robust semantics and quantified construction

**Locators:** `sections/03-robustness-screening.tex:49`, `thm:nearoptimal-robust`; line 63, `lem:measurement-threshold`; lines 116–177, criterion/domain/worst-value formulas and witness recovery.

The measurement-fiber equivalence is correct in both directions. A near-optimal response supplies a nonempty compact measurement fiber whose minimum meets the same budget. Conversely, a feasible fiber KKT candidate meeting the true budget is already a near-optimal response, regardless of whether it is globally optimal on that fiber. A global fiber minimizer supplies the completeness witness. This does not require the arbitrary adversarial response to satisfy stationarity for the unrestricted follower.

The construction retains the true nominal global value in a separately eliminated graph. Replacing that value by an arbitrary nominal stationary value would enlarge the uncertainty set incorrectly; the manuscript does not make that replacement. The compact enlarged parameter domain is justified by polynomial-bit bounds on the polynomial measurement entries and uniform coordinate bounds. Adding the measurement equations changes only a fixed number of shared rows and parameters, so the moving-normal response machinery applies even when their rank drops.

The domain formula has an existential true nominal value and separately eliminated bad-criterion predicates. Empty follower fibers therefore cannot become robustly feasible through vacuous universal quantification. Empty measurement fibers contribute no candidate. Every upper row is tested against the original near-optimal set; upper rows never filter that set before the adversary acts.

Each criterion's quantified response variables are eliminated before the growing conjunction of upper rows is formed. The worst-objective construction uses a fixed number of copies and one shared nominal value. Thus the number of criteria enlarges the description and number of separate computations, but does not create a growing-dimensional quantified formula. The maximum exists at each feasible leader by compactness, while the leader infimum and its attainment remain separate questions.

Joint recovery adds one thresholded fiber candidate realizing the worst objective. It returns a genuine near-optimal witness with that criterion value; no claim is made that it realizes another criterion's worst value. Rational decoding stays in the sampled field. The separate encodings for independently requested witnesses avoid an unjustified common-field compositum bound.

## Constant local matrices and algebraic degree

**Locator:** line 185, `cor:robust-degree`.

The extension to moving shared normals is valid. Only the local Hessian and local active/equality normals enter the local KKT matrix. Shared resource normals and measurement normals enter the effective linear cost, multipliers, and consistency equations. Constant local matrices therefore give rational constant inverses and polynomial response formulas in the compressed coordinates, even when shared normals change rank.

With fixed input degree, candidate and substituted criterion degrees remain bounded independently of follower and criterion counts. A fixed number of elimination steps along each dependency chain preserves a degree bound depending only on those degrees and fixed variable dimensions. Running many independent criterion computations does not multiply these degrees. This is precisely the distinction needed for the existing Basu–Pollack–Roy degree bounds to apply. The corollary correctly limits joint output to one leader/witness pair and makes no additional attainment assertion.

## Attainment and robustness boundaries

**Locators:** line 213, `prop:robust-attainment`; line 258, `ex:positive-budget-nonattainment`; line 295, `prop:robust-measurement-hardness`.

The convex fixed-normal proof treats the relevant feasible-leader domain relatively. Closed constraints and uniform boundedness make that domain compact. Hoffman repair and uniqueness give continuity of the nominal minimizer and value there. For a positive budget, mixing any near-optimal response with the nominal minimizer produces strict budget slack; repair and continuity transport the mixture to nearby fibers. Taking the mixing weight to zero gives the required approximation property. At a zero budget, the limiting near-optimal set is the singleton nominal response, which nearby nominal minimizers approximate even if nearby budgets are positive. These two cases justify continuity of every criterion maximum and hence robust attainment.

The positive-budget counterexample's factorization and derivative are correct. At `c=rho=1/16`, the budget set is `[0,(1+sqrt(17))/16] union {1}`. For larger `c` it is a single interval with a strictly smaller first endpoint: the objective rises to one interior maximum, then decreases to the endpoint value `c>rho`, so it cannot cross the budget again. This establishes the claimed nonclosed robust feasible domain.

The unconstrained robust objective counterexample also works. On the relevant interval, `f_rho'(z)>z/4` and `h(z)<z`. Integrating between the two first crossings yields `4x+a_(rho+x)>a`, while the values tend to `a` as `x` decreases to zero. At zero the isolated near-optimal response at one makes the worst value one. Thus this infimum is unattained despite unique nominal optima and strictly positive budget.

The Max-Cut transfer is correct. The budget `N/2` includes the entire unit cube for the diagonal follower. Convexity of the quadratic criterion puts its maximum at a binary vertex, where it equals cut size. Since that maximum is integral, universal satisfaction of `G<=K-1` is equivalent to absence of a cut of size at least `K`; a violating binary vector certifies the complement. The proposition does not equate growing numbers of independent affine rows with a single unrestricted quadratic criterion.

## Screening enclosure and whole-cell certificates

**Locators:** line 358, `lem:screening-enclosure`; lines 389–463, vertex bound, labels, and closure refinements.

I derived the sign of the variational-inequality combination independently. With `e=z-y` and `p=Ey`, it gives `e^T Q e+p^T e<=0`. Completing the square gives the stated ellipsoid, and its signed directional support gives both coordinate and gradient enclosures. In particular, using direction `Q e_i` yields gradient center `ghat_i+p_i/2` and radius `sqrt(Q_ii eta_P)/2`; those signs and matrices are correct.

The cell-wide bound maximizes a convex quadratic over vertices of a compact polytope in fixed ambient dimension. Lower-dimensional cells and singletons still have sufficient row-basis vertex descriptions. Affine extrema and rational square-root comparisons make the displayed certificates exact.

The strict gradient tests distinguish forced bounds from zero-gradient bound degeneracy. The `F` label means a zero-gradient equation, so retaining weak box bounds in subsequent LPs is consistent. For the closure refinements, each affine nonnegative slack that is not identically zero is positive throughout the relative interior. Interiority or strict gradient sign is therefore obtained there, and continuity extends the resulting response/gradient equality to the closure. This remains valid in a lower-dimensional affine hull. Removing the strict-somewhere conditions would invalidate the reasoning; the text retains them.

## Dense recovery and perturbation neighborhood

**Locators:** line 466, `thm:screening-recovery`; line 526, neighborhood construction; line 583, `cor:screening-neighborhood`.

Recovery uses the true dense Hessian in every free equation and every bound-gradient test. All its principal submatrices are invertible, including when the free set is large; ordinary rational linear algebra has polynomial bit complexity. Each completed status assignment produces a bounded rational LP in cover coordinates. Soundness follows from complete true box KKT conditions. Completeness assigns zero-gradient ambiguous coordinates to `F` and positive/negative-gradient coordinates to their forced bounds, so boundary ties are retained.

The sum of recovery calls is at most `sum_P 3^(t_P)<=M 3^t`. The manuscript explicitly excludes cover construction and screening from that LP count and includes their costs in the total bit bound. No unproved bound on the number of free coordinates is used. A failed whole-cell guessed assignment is correctly retained as potentially valid on a smaller part of the cell.

The replacement of triangulation by overlapping simplices is sound. Projection of a surrogate graph cell onto the leader is injective. A kernel direction in its affine hull would create two nearby points with identical projection in a relative-interior neighborhood, so cell dimension is at most `r`. Every cell point belongs to a convex hull of at most `r+1` affinely independent original vertices. Enumerating all those subsets gives a polynomial cover for fixed dimensions, without introducing vertices or requiring compatibility of a triangulation.

The union of transition coordinates at a simplex's vertices has size at most `(r+1)q`. Outside that union, the retained original cell label supplies strictly positive rational margins at every vertex. Affine interpolation propagates them to the entire simplex. The minimum margin is positive, with the stated empty-list convention.

The radius arithmetic is correct. The reciprocal induced infinity norm of the surrogate inverse is a valid lower bound on its least eigenvalue. The perturbation bound implies positive definiteness of the true matrix. The two response/gradient estimates are respectively at most `2 eps R/m0` and `2 eps R(1+L0/m0)`. The stated radius makes both no larger than `sigma/2`, preserving every nontransition status. The simplex enumeration may enlarge the polynomial exponent, and the manuscript says so. Arbitrary residual rank and signs do not invalidate the argument.

## Bounds, negative examples, and integration

**Locators:** line 629, `subsec:screening-bounds`; line 668, `ex:screening-conservatism`.

The signed directional bounds give an inner sufficient row and an outer necessary row in the stated directions. Minimizing a lower objective enclosure over outer LPs yields a global lower bound; minimizing an upper enclosure over inner LPs gives a true-feasible leader and upper bound. Empty outer LPs certify infeasibility, while empty inner LPs and outer minimizers have the weaker interpretations stated. Exact upper equalities and restrictive upper rows are not silently covered by a small-error guarantee.

The conservatism example has response `x*1/(1+eps)` and identically zero true gradient. Nevertheless, the whole-cell coordinate radius is positive while its center vanishes at zero, preventing either free-coordinate test. Bound tests also fail. The all-free guessed assignment is therefore a valid independent improvement, not evidence that the ellipsoid tests certify it. The scalar switching example correctly moves the threshold from `1/2` to `(1+eps)/2`.

The coverage map assigns all stage 3 results and negative findings to explicit labels, including the two new developments. Quantifier-elimination theorems remain distinct from implemented screening/recovery mechanisms and later experiments. The new appendix attribution identifies an actual shared-direction predecessor rather than claiming the support arrangement itself as new. The prose explains the two different model extensions before their mathematics and preserves their different output conventions. I found no additional integration or readability correction needed for this stage.

## Verification and review limits

Artifacts are confined to `verification/reviewer03/stage03-round01/`:

- `snapshot-check.json`: manifest and eight file-hash validations.
- `check_stage03.py`, `checks.json`: fresh code importing no author or historical reviewer implementation. Exact checks cover the positive-budget factorization and derivative bounds, a nonstationary measurement-fiber witness, rejection of an empty fiber, a five-vertex Max-Cut example against all 243 ternary cube points, and dense screening against an original-coordinate exhaustive status oracle. The dense instance has signed residual, radius `1/192`, perturbation norm `1/384`, vertex transition count one, and transition unions of size at most two. It passed 81 signed directional checks and 72 certificate checks at selected points. These counts describe different checks, not a combined verification score.
- `build/` and `build.log`: fresh isolated latexmk build of the complete frozen source, producing 27 pages. The final log has no warnings, undefined citations/references, or overfull/underfull boxes. Initial-pass citation warnings in the combined transcript resolve on later passes.

I inspected the actual canonical robustness and screening arguments and their stated restrictions, not their historical review verdicts. Relevant Basu–Pollack–Roy degree and sampling facts were checked against the original PDF during my prerequisite review. For integration I checked the added support-arrangement locator against `[[gritzmann1993-minkowski-addition-of-polytopes-computational]] p.13-14`, and inspected the near-optimal complexity paper's discussion of separate adversaries. This is not a comprehensive new publication-priority search or a fresh original-PDF audit of every screening citation.

The finite diagnostics supplement the analytical proof checks. They do not implement general quantifier elimination, enumerate arbitrary-dimensional surrogate covers, experimentally validate the asymptotic bit bounds, or replace the universal relative-interior and simplex-cover arguments. I did not rerun benchmark studies or visually inspect all 27 rendered pages. None of those is used as evidence that an unproved stage 3 statement holds.
