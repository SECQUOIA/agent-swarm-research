# Prior-art audit: point output for convex cubics on rational polytopes

Date: 2026-10-02. This audit compares the reviewed box theorem and its
polytope extension in [convex-cubic-point-oracle.md](../new-direction/convex-cubic-point-oracle.md)
and [convex-cubic-polytope-point-oracle.md](../new-direction/convex-cubic-polytope-point-oracle.md).
Both have passed their recorded actual-file reviews. The audit makes no
priority claim.

## Candidate scope and output

For an explicit rational polynomial of degree at most three, promised convex
on a bounded rational polytope, the candidate returns in deterministic bit
time polynomial in input length plus requested precision a feasible rational
point within `2^-q` of the optimizer set. It can instead approximate the
minimum-Euclidean-norm optimizer. It assumes convexity; it does not recognize
convexity, return exact active labels, or expand the optimum into algebraic
coordinates.

The proof supplies a computable rational error constant of polynomial bit
length. Its key cubic structure is an affine Hessian with one common kernel
on the feasible polytope. Symmetry of the constant third derivative controls
the Hessian action transverse to that kernel. The optimal set is then
described by a rational affine slice of the feasible polytope, even when the
slice's right-hand side contains the unknown, possibly irrational optimizer.
A rational Hoffman bound with input-height control turns the objective gap
into a point-distance bound. Standard weak convex optimization supplies the
value-accurate feasible point; the explicit error constant makes the
requested value tolerance polynomial in the input and `q`. The
minimum-norm selector uses Tikhonov regularization after that effective
bound is available.

## Strongest exact-output baseline: convex quadratic programming

Kozlov, Tarasov, and Khachiyan give an exact deterministic polynomial-time
algorithm for convex quadratic programming with rational linear constraints.
Their exact-solution definition includes the rational optimal value and an
attaining rational point; the quadratic matrix may be singular, so ties are
allowed. The original paper uses integer data, and denominator clearing
extends its statement to rational input. This is the direct degree-two
baseline; it does not cover cubic objectives. The local primary text and
source locators are recorded in
[`kozlov1980-the-polynomial-solvability-of-convex`](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md),
especially pp. 2–5.

For general rational convex objectives, the Grötschel–Lovász–Schrijver
oracle framework gives weak optimization from a weak separation oracle.
The project's reviewed polynomial-value interface applies it to explicit
fixed-degree polynomials by using rational gradients as tangent separators
and repairing approximate feasibility. This is an objective-gap result:
without a usable growth or error bound, a small gap need not put the point
near any chosen optimizer. The cubic candidate's effective point bound is
what closes that gap. The primary theorem locators are in
[`convex-patch-evaluation.md`](../new-direction/convex-patch-evaluation.md),
which cites GLS, Definition 2.1.10 and Corollary 4.2.7.

## Convex-polynomial error bounds: qualitative or different domain

Li's 2010 single-polynomial result treats a polynomial convex on all of
`R^n`. The exponent uses
`kappa(n,d)=(d-1)^n+1`; for degree three it is exponential in dimension.
The theorem supplies a function-dependent positive constant but does not
give an input-computable bit bound for that constant. More importantly, a
polynomial of degree at most three that is convex on all of `R^n` is in fact
quadratic: its Hessian is affine and positive semidefinite everywhere, so
every scalar quadratic form of the Hessian must have zero linear part. Thus
the nonquadratic cubic case on a bounded domain is outside Li's whole-space
class.

Li's 2013 polyhedral error-bound theorem treats `g + indicator_P` when `g`
is globally convex on `R^n`; it gives the same degree-dimension exponent
and an existential constant. Its polynomial-domain statement therefore
does not directly address a cubic that is convex only on `P`. The source
theorems and assumptions are summarized from the read primary texts in
[`convex-polynomial-error-bounds-prior.md`](convex-polynomial-error-bounds-prior.md),
with package locators for Li 2010 (Theorem 4.2 and Corollary 4.1, pp. 15–16)
and Li 2013 (Theorem 1, p. 12).

The project also has an independently reviewed qualitative lemma for any
compact-polytope convex polynomial: an existential constant gives growth
with exponent no worse than the degree. That result explicitly leaves the
constant's size and computability open; see
[`canonical-convex-fiber-regularization.md`](../new-direction/canonical-convex-fiber-regularization.md).
The new cubic proof is not a new qualitative error-bound principle. Its
source-level difference is a specific polynomial-bit construction of a
global constant for the promised cubic/polytope input.

A separate all-degree theorem is drafted for polynomials convex on all of
`R^n`; its global-convex premise is stronger than convexity only on the
bounded feasible polytope. It claims an effective degree-only growth bound
on a bounded rational polytope using Jensen's inequality and rational
unisolvent gradient rows. Li is the direct global-error-bound baseline for
that statement, with an existential constant and a dimension-dependent
exponent. The focused comparison, including the distinction from the
compact-polytope qualitative growth lemma, is in
[`globally-convex-polynomial-point-prior.md`](globally-convex-polynomial-point-prior.md).
The separate theorem's two independent actual-file reviews have now passed;
its theorem note links both reviews.

## Convexity recognition is a separate hard problem

Ahmadi and Hall prove that deciding whether a rational cubic is convex on a
rational box is strongly NP-hard (Theorem 2.3, printed p. 3); they also show
coNP-completeness by checking the affine Hessian at box vertices (Remark
2.1, p. 3). Their Proposition 2.7 extends strong NP-hardness to every fixed
degree at least three. This is a recognition result, not a lower bound for
optimization when convexity is already promised or certified. It does mean
that the candidate's convexity promise must remain explicit: a general
polynomial-time convexity recognizer cannot be silently included in its
solver claim unless `P=NP`.

The checked primary text was Ahmadi and Hall's author-posted
[arXiv v2 PDF](https://arxiv.org/pdf/1806.06173v2)
(arXiv:1806.06173v2, 13 March 2019), corresponding to their 2020
*Mathematical Programming* article, DOI
[10.1007/s10107-019-01396-x](https://doi.org/10.1007/s10107-019-01396-x).
The arXiv v2 package is now read locally at
[`ahmadi2018-on-the-complexity-of-detecting`](../../literature/papers/ahmadi2018-on-the-complexity-of-detecting/paper.md):
Theorem 2.3 and Remark 2.1 are on p. 3, and Proposition 2.7 is on p. 11.
The journal identity is separately recorded as metadata-only; the result
here is supported by the read arXiv manuscript, not by a claimed reading of
the journal-formatted version.

## Low-dimensional polynomial perturbation algorithms

Kannan and Rademacher study minimizing an arbitrary convex function `f`
plus a degree-d polynomial `p` supported on `k` variables over a convex
body. Their Theorem 4 in §3 returns a feasible point with objective error
at most `epsilon * range_K(p)` using a low-dimensional grid; its stated
cost is

```text
O((k d^2 / sqrt(epsilon))^k) (T(f,K) + T_tilde(K)),
```

where `T(f,K)` is the cost of solving the unperturbed convex problem and
`T_tilde(K)` is the near-isotropic rounding cost. This is a close general
algorithmic antecedent for perturbations or nonconvex corrections carried
by a small set of coordinates. It does not provide distance to the optimizer
set, a minimum-norm selector, or polynomial bit complexity in `q` when the
absolute target error is `2^-q`: substituting that target makes the displayed
grid factor exponential in `k q`. It also uses an oracle/rounding cost
model, rather than the candidate's deterministic rational Turing bound.
The candidate is narrower in degree and convexity structure, but stronger
in its point-distance guarantee and dependence on requested precision.

The primary source inspected was the author-hosted
[full PDF](https://www.math.ucdavis.edu/~lrademac/fplusp.pdf), Kannan and
Rademacher, “Optimization of a Convex Program with a Polynomial
Perturbation,” *Operations Research Letters* 37(6) (2009), 384–386,
DOI [10.1016/j.orl.2009.07.002](https://doi.org/10.1016/j.orl.2009.07.002).
Theorem 4 is on author-PDF p. 4. The read local source note is
[`kannan2009-optimization-of-a-convex-program`](../../literature/papers/kannan2009-optimization-of-a-convex-program/paper.md).
Its exact runtime has the factor
`O((k d^2/sqrt(epsilon))^k) * (T(f,K)+T_tilde(K))`; the paper gives no
standalone rational bit-operation bound for those subroutines.

## Boundary and assessment

The clearest degree boundary in the checked sources is exact polynomial-bit
point output for convex quadratics versus weak value optimization for
general convex functions. Li's global error bounds give qualitative
polynomial error exponents under global convexity, while Ahmadi–Hall explain
why box convexity recognition becomes hard at degree three. The candidate
fills a more specific promised-input gap: deterministic point-distance and
minimum-norm Cauchy output for box- or polytope-convex cubics with an
effective, polynomial-bit error constant.

A separate reviewed candidate,
[`cubic-core-full-point-oracle.md`](../new-direction/cubic-core-full-point-oracle.md),
uses a supplied quadratic convexifier and partial finite noise to give
full-point Cauchy output for convexifiable cubics. It selects the
minimum-norm point in the optimal fiber of the lexicographically first
optimal core and has expected work
`f(k)(1+alpha/sigma)^k poly(I+q)`. The fresh actual-file review
[`cubic-core-full-point-independent-review.md`](../new-direction/cubic-core-full-point-independent-review.md)
passed. Its `alpha=0` branch specializes to the jointly convex-on-`P`
selected-core theorem
[`joint-convex-core-point-oracle.md`](../new-direction/joint-convex-core-point-oracle.md)
in the degree-three setting; its additional scope is the nonconvex sampled
objective after supplying a quadratic convexifier. This audit's external
comparisons apply to that branch through the same Kannan–Rademacher and
generic-tilt boundaries; they do not establish a match for the full
convexifiable-cubic completion theorem.

This is a scoped prior-art assessment, not a claim of first publication.
The source evidence supports the distinction between exact quadratic
output, weak convex value oracles, existential growth bounds, hard
convexity recognition, and the candidate's effective cubic point-distance
bound. It does not establish that no equivalent cubic theorem exists.

## Source-access notes

- Li 2010, Li 2013, GLS 1988, and Kozlov–Tarasov–Khachiyan 1980 have
  read local primary-text packages linked above.
- Ahmadi–Hall's arXiv v2 and Kannan–Rademacher's author PDF are read in the
  local primary-text packages linked above. The distinct journal-formatted
  Ahmadi–Hall record remains metadata-only and was not needed for the
  source-grounded comparison.
- Yang 2009, “Error Bounds for Convex Polynomials,” is an existing
  metadata/abstract-only package. I did not rely on its theorem details;
  its exact statements and any effectivity result remain unchecked.

No KB index or topic file was edited for this audit.
