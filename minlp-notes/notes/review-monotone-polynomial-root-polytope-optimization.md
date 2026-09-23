# Independent review: exact monotone polynomial-root optimization

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS for the promised strict-monotonicity and dense-degree input model. The author applied both wording clarifications recorded below, and I verified the final text; neither changed the mathematics.

Reviewed [the full candidate](monotone-polynomial-root-polytope-optimization.md) and directly checked the cited factor inequality. This is an independent proof and bit-complexity review, not a priority assessment.

## Thresholds, vertex attainment, and boundary cases

For a strictly increasing continuous H with its root in [a,b], the root is at least z exactly when H(z)<=0, and at most z exactly when H(z)>=0. Affine dependence on theta makes the respective existential tests rational LP minima and maxima. Both signs and inclusion of equality are correct.

At any feasible parameter point, decompose theta into a convex combination of vertices and evaluate all H-values at its root. A weighted average of zero contains values of both weak signs. Their vertex roots bracket the original root. Thus the global extrema are attained among finitely many vertex roots without any extra differentiability or attainment argument. A derivative may vanish at a root; the theorem does not require a positive derivative lower bound.

The initial endpoints satisfy the bisection invariants by the promises. A maximum at a or b and a minimum at either endpoint cause no special failure. Equality is sent to the correct branch. Strict monotonicity on a<b excludes the zero polynomial and degree zero. The t=0 case is correctly separated as ordinary root isolation.

## Uniform vertex-polynomial data

After rowwise denominator clearing, every vertex of a bounded polytope has t independent active normals, even if the polytope has smaller affine dimension. Cramer's rule gives the displayed common determinant denominator and numerator bounds. Clearing the h_j denominators and multiplying by that determinant produces a nonzero integer polynomial with coefficient magnitudes at most `(t+1)*Delta*P0`. The constant-in-the-parameters term h0 correctly contributes the extra summand.

The logarithms of the denominator products, factorial determinant bound, and polynomial height are polynomial in the original input. They are computable explicitly without enumerating vertices. The statement should call the output bound a **polynomial coefficient bit length**, not a polynomial numerical coefficient height: H0 itself can be exponentially large. This wording correction was sent to the author.

## Squarefree product and separation

For two vertex polynomials, including identical polynomials, their product has degree at most 2D and height at most `(D+1)*H0^2`. Its primitive squarefree part is an integer factor: factorization into primitive irreducibles and Gauss's lemma show that retaining one copy of each factor divides the original product over the integers, up to its integer content. Repeated or shared roots therefore disappear without changing the set of distinct roots being separated.

The exact factor inequality used in the draft is stated in [Theorem 1.2 of the linked primary research paper](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD): an integer factor's coefficient l1 norm is bounded by 2 to the factor degree times the product polynomial's coefficient l2 norm. Applying it to the squarefree part and then bounding l2 norm by square-root dimension times height gives the proposed H_s. It applies without a monicity assumption.

For a squarefree degree-n integer polynomial, its discriminant is a nonzero integer. In its root-product formula, isolate the selected root-pair distance delta. The other root differences are at most `T=2*(1+H_s)` by Cauchy's bound, including complex roots. The leading coefficient contributes at most `H_s^(2n-2)`. Thus

    delta >= T^[-(n^2+n-4)/2].

For 2<=n<=2D, the exponent magnitude is at most 4D^2. The proposed `sigma=T^(-4D^2)` is therefore a valid conservative lower bound. If n=1, there is no pair of distinct roots. The use of squarefree parts handles multiple roots such as those possible when the derivative vanishes at the unique real root.

The bit length of H_s is `O(D+log(D+1)+log(H0))`. Hence the denominator of sigma has `O(D^2*(D+log(D+1)+log(H0)))` bits. These bounds remain polynomial when D grows in dense encoding. No hidden exponential-degree field construction occurs.

## Exact maximizing-vertex extraction

The final minimizing LP at the lower endpoint l returns a vertex whose root lies in [l,qmax]. Both it and qmax are vertex roots satisfying the uniform separation bound. A bracket narrower than sigma therefore forces equality. The minimum proof at the upper endpoint is the exact symmetric argument.

Lexicographic minimization over the original LP's optimal face uses at most t additional rational LPs. Each step selects a smaller face, and the final singleton is a vertex of the original polytope. For a completely explicit accumulated encoding bound, note that every intermediate coordinate optimum occurs at an original P vertex. Its rational value therefore has the original Cramer bit bound, rather than a recursively growing bound from the augmented LP. This clarification is useful in the prose, although the algorithm already has polynomial bit complexity.

After k bisections, each rational endpoint has polynomial bit length in k and the original bracket. Horner evaluation of a degree-D h_j at such an endpoint produces rational data of polynomial bit length in D, k, and the input. The number k is polynomial by the displayed sigma bound. The LPs, lexicographic recovery, and final degree-at-most-D univariate root isolation consequently all run in polynomial rational bit time. Roots at the rational endpoints can be recognized exactly; other roots outside [a,b] do not interfere with selecting its unique root.

## Scope

The algorithm assumes the uniform monotonicity and bracket promises; it does not establish them. It does not apply to unrestricted branches, complex root optimization, sparse binary exponents, or piecewise formulas without an additional partition argument. The unrestricted parameter dimension appears only in rational LP and determinant bounds, so no fixed-dimensional quantifier elimination is being used implicitly.

No mathematical defect was found. With the two wording clarifications above, the theorem supports the intended correlated polynomial-law applications, provided those applications separately verify the monotonicity and piecewise representation hypotheses.

## Requested extension: a fixed rational partition

The author additionally proposed allowing H to be continuous and polynomial on each interval of a supplied rational partition of [a,b], with coefficients affine in theta on every piece, and retaining the uniform strict-increase and root-bracket promises. The conceptual extension passes. Its final integrated wording should retain the following details.

Remove duplicate breakpoints and empty intervals. Every positive-width piece, evaluated at any feasible profile, is nonconstant because H is strictly increasing on the whole bracket. In particular, its vertex-profile polynomial is nonzero. A root at a partition breakpoint belongs to either adjacent closed piece by continuity; it is therefore among the roots controlled by the same vertex-piece polynomial height bound. There is no need to compare that breakpoint to arbitrary roots using an unrelated rational height estimate.

Clear all encoded piece coefficients with one denominator and use their maximum coefficient bound. The number of pieces is part of the input; this still gives polynomial log-height. With D the largest piece degree, any pair of vertex roots belongs to a pair of degree-at-most-D vertex-piece polynomials. The exact same squarefree-product separation bound applies. LP evaluation chooses the known piece of its rational test point; either adjacent piece gives the same value at a breakpoint by the continuity promise.

Vertex attainment and the final lower-bracket optimizing-vertex argument use only scalar monotonicity and affine parameter dependence, so they do not change. For the returned vertex, evaluate H at rational breakpoints and locate its unique root interval by sign tests. Return a breakpoint exactly if its value is zero; otherwise isolate the unique root of the corresponding polynomial inside the sign-changing interval. All coefficients and tests remain polynomial in total dense input size and D. No comparison of exponentially many branches is introduced.
