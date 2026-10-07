# Point-output manuscript review R1

Reviewed on 2026-10-05. This is an internal, independent review of the
actual manuscript, not a reuse of the prewriting verdict. The primary
scope is `sections/02-points.tex` and `appendices/C-points.tex`, including
P1–P10. I also read `evidence/BRIEF.md`, `evidence/authoring/DECISIONS.md`,
`macros.tex`, `sections/01-models.tex`, the current
`sections/00-introduction.tex`, `sections/abstract.tex`, the relevant
discussion passages, the vetted literature report, and the two prewriting
reports. The requested `00-intro.tex` is named `00-introduction.tex` in the
actual manuscript.

I reconstructed the arguments from the manuscript. Two delegated read-only
audits separately checked the boundary constructions and the principal
core tools. No manuscript file was edited. No literature search, primary
source investigation, experiment, mathematical computation script,
historical checker, project-wide verification, or CI inspection was run.

The refreshed primary-file SHA-256 values are:

- `sections/02-points.tex`: `be289b143bf9614debcb1e5974170323baf1b6fbe0eeb5152158228b8affa6bf`
- `appendices/C-points.tex`: `067626b75785ca84375bdccba9d110b52cd9222813238e032f6104550dc54e95`

## Verdict and concrete repairs

I found no substantive mathematical defect or unresolved proof step in
P1–P10. The actual appendix contains the arguments that the source reports
previously delegated to repository notes. The formal global and cubic
theorems satisfy their stated output contracts, and the reductions retain
their necessary restrictions. The point chapter needs the following
integration and wording corrections before it is journal ready. These
are separate from theorem defects.

| Severity | Actual location | Concrete issue and repair |
| --- | --- | --- |
| Medium, encoding consistency | `sections/02-points.tex:573` and `:619`; `sections/01-models.tex:49` | Both example discussions claim input length `O(n log n)`. The declared polynomial encoding writes each full exponent vector, and the rational-matrix encoding counts all entries. There are `Theta(n)` monomials with `n` exponent entries, so these fixed-degree families use `Theta(n^2)` bits under that convention. Replace the claims by “the input length is polynomial in n,” or use the full-vector `O(n^2)` bound. The claimed superpolynomial lower bounds survive. |
| Medium, structural consistency | `sections/00-introduction.tex:385`–`:389`; `appendices/C-points.tex:1506` | The introduction attributes the active-multiplier rectangle obstruction to a path interaction graph. P10(b) contains the triangle on `x_(n-1), x_n, y`, and the actual theorem correctly claims treewidth two. Use “treewidth at most two,” or distinguish P9/P10(a)'s paths from P10(b). |
| Medium, missing bibliography integration | `sections/02-points.tex:161` | `Hoffman1952` is cited but absent from the current `references.bib`. Have the designated Luna literature owner add a vetted record. This does not invalidate the explicit Hoffman lemma, whose proof is complete and self-contained. |
| Low, abstract qualification | `sections/abstract.tex:10`–`:11` | The abstract says that global convexity gives polynomial-time fixed-optimizer approximation without a degree qualification. The input model permits binary exponents, while the theorem charges numerical degree D. State time `poly(L,D,q)`, or qualify polynomial time by fixed/unary degree. The actual theorem, the introduction's detailed statement, and the representation remark already have the correct qualification. |
| Low, exact output contract | `sections/00-introduction.tex:123`–`:125` | “Regularization selects the optimizer only with a parameter of exponentially many bits” compresses an approximation statement into wording that can suggest exact selection. For the stated family, every positive lambda gives `y_lambda<1`, so exact selection never happens. Say that regularization approximates the optimizer to accuracy `1/2` only with such a parameter. Proposition P8(c) already states the precise necessary condition. |
| Low, scale of the lower bound | `sections/02-points.tex:592` | “Exponentially longer than the inputs” can be read as an exponential lower bound in L. The proved lower bounds are exponential in n and superpolynomial in L; with full exponent vectors, `L=Theta(n^2)` for these examples. Use that precise distinction, as the introduction's final limitations paragraph already does. |
| Low, reference destination | `sections/02-points.tex:31`–`:32`; `sections/01-models.tex:323` | The rectangle format is attributed to `def:models-representations`, which lists optimizer encodings but no rectangle certificate. Cite `prop:points-rectangle` for this format, or add its definition to the cited model definition. |

For self-contained reading, it would also help to define the interaction
graph when it first appears: variables are vertices, and variables that
occur together in a nonzero monomial are joined. The factor scopes in the
proof supply bags containing these monomials. State that a tree decomposition
with bags of at most three vertices proves treewidth at most two. The
actual bag constructions already establish the advertised bounds.

## Independent proof reconstruction

| Result or tool | What was checked and why the step is valid |
| --- | --- |
| Convex value interface, `02:117`, `C:328` | LP identifies universally tight rows, not merely rows active somewhere. Positive-slack witnesses give a rational relative interior point. The free-coordinate chart has an identity submatrix, so the reduced polytope has a rational inner ball and a polynomial-bit outer radius. The capped epigraph has an explicit inner ball and exact rational separation. The GLS output is repaired by `hat u=r0*u/(r0+epsilon)`; rowwise feasibility and the objective-loss bound are proved. Evaluation occurs only at feasible rational points, including on lower-dimensional original domains. |
| Sparse evaluation, `C:51` | Each original sparse monomial is evaluated after the rational affine map, and the gradient follows by the chain rule. Query arithmetic, majorants, and their encoding lengths are polynomial in numerical D and query length. The proof never constructs the potentially exponential expansion. The Householder example independently demonstrates why expansion would lose the bound. |
| Hoffman constant, `02:166`, `C:191` | The projection normal uses a nonnegative combination of active inequality rows and an unrestricted combination of equality rows. Elimination preserves nonnegative inequality coefficients and produces independent rows. Cauchy–Binet and the entry bound give the claimed least singular-value bound. Dotting with the feasible displacement makes the inequality contribution nonpositive. No step uses rationality of the right-hand sides or of the projection; irrational optimizer slices are covered. |
| Minimum-norm selection, `02:185`, `C:458` | Coercivity of the regularized objective gives attainment. Comparison with p bounds its minimizer's norm. Projection onto the possibly unbounded optimal set has error at most `2R`; this justifies the necessary `4R` factor. Projection of the origin onto S then gives the squared-distance estimate. A regularized gap of `tau*epsilon^2/4` supplies the other half of the distance budget. The bounded-optimal-set factor-two variant is also valid. |
| P1 bounded global theorem | It is a valid corollary of the global modulus and selector, with compactness supplying attainment and `R=max(1,n*rho)` bounding every feasible point. It does not require the unbounded-domain radius argument. |
| P2 global structure, `C:523` | The univariate interpolation estimate yields a tangent quadratic minorant. Termwise cube integration preserves sparse polynomial complexity. Nonnegative Hessian quadratic forms identify the integrated Hessian kernel with the common Hessian kernel. The affine slope along that kernel is retained; only the kernel directions orthogonal to that slope are invariance directions. All projectors and constants are rational and computable. |
| P2 boundedness and radius, `C:609` | The LP `w=A^T lambda+Mz`, `lambda>=0`, is feasible exactly in the bounded case. An infeasible LP gives a rational recession direction normalized by `w^T d=1`; the objective decreases exactly linearly along it. In the feasible case the quadratic minorant bounds the transverse component. Convexity at zero supplies the lower bound on the remaining linear coordinate that the inequalities alone cannot supply. Integer Hoffman replaces every sublevel point by an equally good bounded representative. The explicit formula has a uniform margin of at least one below R, so compact limits also have norm below R; attainment is not assumed when computing the radius. |
| P2 global distance modulus, `C:706` | The Bregman polynomial is nonnegative everywhere, and its value along the feasible segment is bounded by the objective gap. Midpoint convexity plus extrapolation bounds directional gradients on the unit cube using only a radius for p; x may be arbitrarily far away. Tensor interpolation bounds the gradient's coefficient rows without enumerating its grid. At zero gap the bounded-line polynomial argument gives exact invariance. Thus S is exactly the rational-row affine slice through Np, and integer Hoffman supplies the computed constant on the whole unbounded P. |
| P2 final output, `C:819` | The regularized minimizer lies in the computed radius box. The bounded value interface gives an exactly feasible rational point near the same minimum-norm optimizer at every precision. A smaller point tolerance and a separate lower value bound give the optional value enclosure at that same returned point. All bit lengths are polynomial in `L,D,q,q_f`. |
| P3 cubic theorem, `C:886`–`:1046` | The actual affine hull is reduced before PSD is inferred from domain convexity. Reflection makes the center Hessian dominate every boundary Hessian, identifying the common kernel. Cubic Taylor's exact tensor symmetry gives the transverse fourth-root estimate without optimizer interiority. The center gradient row retains possible linear change along the kernel and gives the exact optimal slice. Integer principal minors bound the least positive center eigenvalue; affine and zero-dimensional branches are handled. The selector penalizes the original norm, so it selects the original minimum-norm point. |
| P4 exact active bound | The averaging tree has disjoint residual-row supports and norm below `3/4`, giving its uniform strong convexity. Normalized leaf roots and the root average are exact. The one-sided sign test handles equality by KKT at theta=0, and theta=1 is excluded by its derivative. Coefficient magnitudes, box widths, diagonal Hessian bound, and treewidth two are preserved. Easy point output follows from a supplied constant curvature modulus. |
| P5 selector versus some optimizer | The quartic amplifier's explicit Hessian identity bounds its negative part without division by a vanishing amplitude. Its optimal set is exactly the stated segment or singleton, so appending y=1 always gives an easy optimizer while the minimum-norm y-coordinate encodes the arithmetic answer. |
| P6 any-optimizer SRS | The trace proof correctly shows that an integer sum of positive square roots forces every radicand to be a square; no large field is computed. After that preprocessing, exactly one sign amplitude is positive. Paired amplifiers yield a unique endpoint coordinate. The unit-box affine maps preserve factor scopes; the claimed nonconstant coefficient and diagonal-Hessian bounds and the explicit treewidth-two decomposition are valid. |
| P7 any-optimizer PosSLP | Bounded numerator/denominator pairs preserve gate ratios and positive denominators without writing gate values. The output signal has the sign of `2A-1`, including A=0. The weighted triangular residual objective has the claimed Hessian lower bound: the scaled lower-triangular derivative matrix has row/column bounds, and the remaining residual-Hessian term is absorbed by geometric weights. After final scaling, coefficient magnitudes stay bounded while bit lengths remain polynomial. No treewidth bound is asserted. The constant-accuracy and Las Vegas consequences match their stated algorithms. |
| P8 precision and regularization | The cubic base is uniformly strongly convex; boundary derivatives force its optimizer's x-coordinates into the interior. The squared recurrence gives the double-exponentially small final coordinate. The quartic amplifier remains convex and uniquely forces y=1. The feasible point with y=0 proves the modulus lower bound. Regularized stationarity gives `y_lambda=x_n,lambda^2/(x_n,lambda^2+lambda)` and the same coordinate bound; accuracy at most `1/2` forces the denominator-bit lower bound. Setting y=1 independently gives easy point approximation. |
| P9 expanded algebraic output | The original `[1,2]^n` example is not claimed convex. The manuscript's added constant-bit narrow box is a valid repair: the residual Jacobian has inverse norm at most two, residuals are bounded by `15/128`, and the Hessian is at least `I/32` there. Eisenstein after translation proves degree `2^(n-1)`, and the no-cancellation sign induction proves the exact support count. The sparse lower bound applies to the minimal polynomial, with the nonminimal-multiple limitation stated. |
| P10 rectangles | Both Hessian and growth estimates are valid. Any enclosing rectangle strictly inside the open box needs a positive final lower endpoint below the tiny rational optimizer coordinate. In the multiplier example the exact corner minimum forces the same positive lower endpoint, even for degenerate rectangles or boundary contact. The denominator bound follows directly. The short correlated recurrence/contraction certificates certify the same optimizers and are not excluded by the rectangle lower bounds. |

The actual introduction's detailed global theorem retains sparse input,
numerical degree D, arbitrary rational polyhedra, and minimum-norm
selection. Its cubic theorem retains bounded polytopes and possible lower
dimension. Its hardness discussion correctly distinguishes exact active
labels, minimum-norm selection, and any-optimizer constant accuracy. The
formal hypotheses therefore match those introduction passages; the
discrepancies are the local wording items listed above.

Normal-polynomial coefficients, LLL margin certificates, and the recourse
FPT/expected-work hypotheses now belong to `sections/10-recourse.tex` and
Appendix I. The root confirmed that a fresh recourse reviewer owns those
proofs. This review checks the shared cubic/value/Hoffman interfaces that
they consume, not the recourse theorem itself.

## Exact source contracts still requiring the designated literature owner

The mathematical constructions above are local proofs. Their computational
subroutines and prior-work attributions still need a final source-contract
record from Luna. I did not inspect or research primary literature.

- `lem:points-gls`, `C:303`–`:326`: the exact GLS 1988 weak optimization,
  weak separation, circumscribed-body, and oracle-composition contracts.
  The author supplies locators (2.1.10), (2.1.13), (2.1.16), Corollary
  (4.2.7), General Assumption (1.2.1), and Section 4.1. Confirm the returned
  rational point/tolerance convention and polynomial bit-work composition,
  rather than merely the abstract equivalence of optimization and
  separation. Also confirm rational LP primal/dual polynomial-bit output
  at Theorem (6.4.12)/Section 6.5 and rational Gaussian elimination at
  Section 1.4. The current literature report contains no GLS contract row.
- `AhmadiChaudhryZhang2024`, proof of Lemma 5, for the credited tangent
  quadratic minorant. The manuscript's weaker explicit bound is proved
  locally and does not depend on that sharper bound.
- `AhmadiHall2020`, Theorem 2.3, for strong NP-hardness of recognizing
  cubic convexity on boxes; `EY2010`, for the exact strong-approximation
  equilibrium comparison; `TarasovVyalyi2008`, for arithmetic-circuit
  comparison to exact SDP feasibility. Verify these precise contracts,
  not adjacent convexity-recognition or residual-approximation claims.
- Add the vetted `Hoffman1952` bibliography entry. The explicit constant
  and irrational-right-hand-side extension are proved here.
- `AllenderEtAl2009`: check whether the cited Square Root Sum interface is
  membership in `P^PosSLP` or a direct many-one reduction. `02:445` says
  “reduces to PosSLP” while the vetted report elsewhere uses oracle
  membership. The manuscript's own closure theorem supplies the direct
  consequence if needed; attribute the two ingredients separately when
  that is the actual source contract.

The current Li2010/Li2013 and Slot–Steurer–Wiedmer attributions agree with
the vetted report's theorem numbers and version limitations. Yang 2009
is treated cautiously: the manuscript claims no checked exponent or
effectivity conclusion from its unavailable theorem text. No novelty
verdict in this review follows from a missing search hit.

## Targeted document checks actually run

I ran two inline Python document-parsing checks; neither performed
mathematical computation. The first collected all manuscript TeX labels
and checked only `ref`/`eqref` uses in the two assigned files. The second
parsed bibliography keys and checked only citation uses in those files.

- Assigned-label check: 30 distinct references in `02-points.tex`, 41 in
  `C-points.tex`; no missing labels.
- Assigned-citation check: 12 distinct keys in `02-points.tex`, with only
  `Hoffman1952` missing; both keys in `C-points.tex` exist.
- Used `nl`, `sed`, `rg`, and `sha256sum` to read and refresh the actual
  files and report precise locations.

No compilation, CI check, or project-wide verification was performed by
this review. Once the listed integration corrections and literature
contract vetting are complete, the reviewed point-output theorem/proof
scope is ready for journal preparation.
