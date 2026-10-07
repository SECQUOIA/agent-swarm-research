# Source reconciliation for values, points, and exact arithmetic

Date: 2026-10-03. Scope: the arithmetic-complexity continuation in this
directory. This is a primary-source comparison and a check of the
implications used by this project. It does not establish publication
priority or certify every result in the cited papers.

The main correction to the earlier discussion is that polynomial-time
objective-gap approximation for globally convex polynomials on arbitrary
rational polyhedra is already the subject of Slot, Steurer, and Wiedmer.
The project's point-distance result needs a separate effective error
bound. Its gradient-invariance representation has direct prior antecedents.
The September exact-arithmetic notes had already examined Hesse's
Redemption; its omission was in the October 2 global-point prior audit,
not in all previous research.

## Source record and exact locators

The source read is Lucas Slot, David Steurer, and Manuel Wiedmer,
*Hesse's Redemption: Efficient Convex Polynomial Programming*,
[arXiv:2511.03440v1](https://arxiv.org/abs/2511.03440v1), submitted
2025-11-05. The version history checked on 2026-10-03 lists v1 only.
The [full PDF](https://arxiv.org/pdf/2511.03440v1) and
[HTML](https://arxiv.org/html/2511.03440v1) were read, including the
structure proof, constrained radius proof, exact-witness appendix, and
ellipsoid appendix. Page references below are printed PDF pages.

| Locator | Relevant assertion |
| --- | --- |
| Theorem 1.1, p. 3; proof pp. 19–26 | Global convexity and rational polyhedral constraints imply either unboundedness or attainment at an optimizer with polynomially bounded logarithmic norm. |
| Corollary 1.2, p. 3; Algorithm 1, p. 20 | Polynomial-time unboundedness detection and feasible objective-gap approximation. |
| Theorem 1.3, pp. 3, 14 | Rational directions split the objective into a nonlinear quotient and an affine term; the quotient has a strongly convex quadratic lower bound. |
| Proposition 4.2, pp. 14, 17–18 | The coefficient matrix of the partial derivatives computes invariant and affine directions. |
| Proposition 4.9, pp. 16–17 | An everywhere singular Hessian gives a common direction of linearity. |
| Lemmas 5.1–5.3, pp. 19–26 | Recession LP, quotient bounds, and lifting provide the optimizer radius. |
| Proposition 3.2, p. 13; Appendix D, pp. 29–33 | Bounded-radius convex value optimization, including rational affine-hull reduction. |
| Table 1, p. 5; Appendix C, pp. 28–29 | Approximate and exact decisions are separated; Lemma C.3 concerns univariate quartics. |

The input uses rational coefficients and unary degree/exponent data, not
an unrestricted arithmetic-circuit representation. A supplied strong
convexity modulus is not required. Global convexity remains a promise;
the algorithm does not recognize arbitrary polynomial convexity.

## What follows directly, and what needs an additional theorem

Compare the source with the October 2
[global point theorem](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md).

1. **Objective-gap optimization is prior.** Corollary 1.2 is broader in
   domain than the bounded-polytope value interface. The latter must be
   presented as an ingredient, not as a new general value algorithm.

2. **A bounded optimizer is enough to preserve the minimum-norm
   selector.** If the source gives an attaining point of norm at most
   `R`, then the minimum-norm optimizer also has norm at most `R`.
   Intersecting the original polyhedron with `[-R,R]^n` therefore
   preserves both the optimum value and that selector. Applying the
   existing bounded point theorem to this intersection is a direct
   corollary once a usable rational radius is provided. Removing the
   supplied box should not be advertised as independent of this prior
   radius theorem.

3. **Translation-invariance rows are prior structure.** Let `C_f` have
   one row for each coefficient vector in the gradient polynomial.
   Then `C_f d=0` means that the directional derivative of `f` along
   `d` is the zero polynomial. This is precisely the coefficient-map
   construction in Proposition 4.2. The October 2 sampled-gradient
   matrix has the same kernel by unisolvence. Replacing its sampled
   rows by coefficient rows is useful for sparse input, but the
   identification of this invariant space should be credited to the
   prior structure theory.

4. **The affine description of the optimizer set also has old
   qualitative ingredients.** If `y,z` minimize a globally convex
   polynomial on a convex set, convexity makes the polynomial constant
   on `[y,z]`. The univariate polynomial identity extends this to the
   whole line. A direction constant on one line is a global invariance
   direction for such a polynomial. Consequently
   `argmin_P f = P intersect (y + ker C_f)`.
   Li 2010, Lemma 2.2(2), already records propagation of a constant
   direction; Lemma 4.2 records extension from a segment to its affine
   hull. This slice description is not, by itself, the quantitative
   contribution.

5. **The source's quadratic lower bound is not an error bound around
   an optimizer.** For example, `t^4 >= t^2 - 1/4` is a strongly convex
   quadratic lower bound, while `t^4/t^2` tends to zero at its optimizer.
   No positive quadratic-growth modulus at that optimizer follows.
   Nor does a norm bound determine a regularization schedule for a
   minimum-norm selector. The current derivation still needs an
   input-computable bound
   `dist(x,S) <= Gamma (f(x)-f*)^(1/D)` with polynomial control of
   `log Gamma`. Hesse's Redemption does not state this point-output
   contract. That statement of scope is not a claim that no alternate
   derivation from prior work exists.

6. **Strong convexity is a simpler special case.** If a rational
   positive modulus is supplied, the ordinary inequality
   `f(x)-f* >= (mu/2)||x-p||^2` already converts value accuracy to point
   accuracy. The global-point theorem's role is to remove that
   supplied-modulus requirement, including nonunique optima and flat
   Hessians.

For the constrained cubic result, the distinction is different. The
[cubic theorem](../../research-20261002/new-direction/convex-cubic-polytope-point-oracle.md)
assumes convexity only on the feasible polytope and obtains an effective
`1/4` distance exponent and a fixed minimum-norm selector. A cubic
globally convex on all of Euclidean space is quadratic: its affine
Hessian cannot vary while remaining positive semidefinite along every
line. The genuinely cubic domain-convex case is thus outside the global
premise of Hesse's Redemption. Its bounded-domain value subroutine is
classical; the additional claim is the effective point bound.

## Other primary comparisons

**Ahmadi–Chaudhry–Zhang.** Their
[arXiv v2 manuscript](https://arxiv.org/html/2311.06374v2),
*Higher-Order Newton Methods with Polynomial Work per Iteration*, has
Lemma 4 on positive semidefinite matrix-polynomial integration and
Lemma 5 on a unique minimizer when the Hessian is positive definite
somewhere. The proof of Lemma 5 supplies the global tangent-quadratic
lower bound used by Hesse's Redemption, Lemma 2.1. This is a direct
antecedent of an averaged tangent-quadratic construction. Its
higher-order iteration analysis does not supply the present general
polyhedral minimum-norm-selector bit bound. Credit the tangent bound
even if this project gives a different elementary proof and constant.

**Li's error bounds.** The local primary packages contain the full
author manuscripts, rechecked here:
[Li 2010](../../literature/papers/li2010-on-the-asymptotically-well-behaved/paper.md),
Theorem 4.2 and Corollary 4.1, pp. 15–16, and
[Li 2013](../../literature/papers/li2013-global-error-bounds-for-piecewise/paper.md),
Theorem 1, pp. 12–13, and Corollary 1, p. 14. They provide global
convex-polynomial error bounds with exponent
`1/((D-1)^n+1)` and a function-dependent constant. The latter source
includes polyhedral constraints. These theorem statements do not give
the input-computable polynomial-bit constant needed here. Neither
absence of that guarantee in a statement nor comparison with its
weaker displayed exponent establishes novelty.

**Yang remains a priority-sensitive source gap.** The
[publisher record](https://doi.org/10.1137/070689838) and first-page
preview confirm direct relevance to unconstrained and polyhedral
convex-polynomial error bounds. The full primary paper was not
accessible in this audit's initial attempts. Searches also surfaced
a later survey attributing a `1/D` exponent to this paper. That is a
lead to verify against the primary text, not theorem-level evidence
used in the present proofs. The [access record](yang-source-status.md)
documents the bounded primary-source search and remaining questions.
In particular, the paper must not imply
that a degree-only exponent is new merely because Li's displayed
exponent depends on dimension. The potential distinction is
effectivity, coefficient-size control, and the output contract.

**Exact rational quadratic output.** Kozlov–Tarasov–Khachiyan's
[read primary source](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md)
already supplies polynomial-time exact convex QP solutions. It is
stronger than Cauchy output at degree two. Convexity recognition and
promise-problem optimization remain distinct; the
[Ahmadi–Hall primary package](../../literature/papers/ahmadi2018-on-the-complexity-of-detecting/paper.md),
Theorem 2.3 and Remark 2.1, gives the relevant cubic-box recognition
obstruction.

## Exact arithmetic is compatible with the value theorem

The September 27–28
[exact quartic upper bound](../../research-20260927/strong-convex-quartic-posslp-upper.md)
assumes a supplied rational global strong-convexity modulus, or a
checkable positive definite Hessian Gram that produces one. It reduces
strict and weak order comparisons of the unconstrained optimum and
optimizer coordinates to a single PosSLP instance. Equality has an
upper bound; the claimed matching lower bounds concern order
comparisons. These promises must remain attached to the classification.

There is no conflict with an ordinary polynomial-time value or point
Cauchy oracle. A Cauchy oracle costs polynomial time in the number of
requested bits. Exact sign decisions can require exponentially many
bits of ordinary approximation. The September construction instead
stores Newton refinement as a short arithmetic circuit and invokes
PosSLP for its sign. This is an output/computation-model distinction,
not evidence that either guarantee is false.

The
[multivariate quartic singleton](../../research-20260927/general-strongly-convex-quartic-singleton.md)
also does not contradict Hesse's Redemption, Lemma C.3. The lemma is
univariate. A rational globally strongly convex quartic in several
variables can have rational minimum value and an irrational unique
optimizer without violating it. Table 1's unresolved general quartic
exact-witness entry is not a theorem precluding such an example.
The separate [exact-prior comparison](exact-prior.md) records the
arithmetic-circuit, algebraic-degree, and root-separation antecedents.
The [constrained-extension comparison](constrained-prior.md) checks
essential-variable extraction, proximal Newton convergence, and the
arithmetic models of the structured box and flow QP subroutines.

## Source-level corrections required by any transferred proof

The following are checks of the displayed formulas in **v1**, with
repairs or a narrower interpretation. They do not establish failure
of its principal conclusions.

1. **Affine-slope normalization, Proposition 4.2 proof, p. 17.**
   The proof chooses `v` with `[grad f]v=-1`, orthogonal to the
   translation kernel, then uses it as the affine slope in
   `f(x)=f(x_U)-v'x`. The required slope is `v/||v||^2`.
   For `f(x,t)=x^2-2t`, that choice is `v=(0,1/2)`, whereas the
   affine slope in the displayed decomposition is `(0,2)`.
   The corrected slope remains rational and polynomially encoded.

2. **Absolute value, equation (22), pp. 23–24.** From
   `w=A'lambda+U'z`, `lambda>=0`, and `Ax<=b`, one obtains the upper
   bound `w'x <= lambda'b + z'Ux`, not the same bound for `|w'x|`.
   For `f(x,t)=x^2-t` on `t<=0`, take `U=(1,0)`, `w=(0,1)`,
   `lambda=1`, `z=0`, and `b=0`. At `(0,-1)`, the printed absolute
   bound would read `1<=0`. The upper bound is enough for the
   quadratic bound on `||Ux||`. On a relevant sublevel set, a lower
   bound follows instead from `w'x=f(x_U)-f(x)>=q(Ux)-f(a)`.
   Combining those bounds repairs the required sublevel argument.

3. **Quadratic normalization, Proposition 4.1 proof, p. 15.**
   After the correct tangent bound with coefficient
   `lambda_min(H(a))/(4D^2)`, the next display calls
   `mu=lambda_min(H(a))/(2D^2)` and places `mu||x-a||^2` in `q`.
   The consistent strongly convex quadratic has coefficient
   `mu/2`. The earlier overview uses the consistent coefficient.
   Moreover, an eigenvalue of a rational matrix need not be rational.
   To obtain the stated rational `q`, use a positive rational lower
   bound `ell<=lambda_min(H(a))` of polynomial bit length and set
   `mu=ell/(2D^2)`. The determinant/trace bound or Corollary 4.8
   supplies such a bound. These adjustments preserve the intended
   encoding estimate; the factor check alone does not disprove the
   stronger printed inequality by a counterexample.

4. **Sparse input under affine substitution, Proposition 4.2,
   pp. 17–18, and Appendix D.** A polynomial-size sparse coefficient
   list need not stay sparse under a dense rational change of
   coordinates when degree varies. A power of a dense linear form
   can have exponentially many monomials even with unary degree.
   Thus the claim that the expanded transformed polynomial has
   polynomial encoding does not follow merely from polynomial
   coefficient bit lengths. Fixed degree avoids this issue. For
   variable degree, preserve evaluation by composition or work with
   sparse coefficient rows and integrated Hessians in the original
   coordinates; do not silently charge expanded output as small.
   A concrete globally convex family is
   `f(x)=sum_i x_i^(2r)` in `n=2r>=4` variables, transformed by the
   rational orthogonal matrix `U=I-(2/n)11'`. Every entry of `U`
   is nonzero. Each even monomial `y^(2 beta)`, `sum beta_i=r`,
   has positive coefficient in `f(Uy)`: its coefficient is a
   positive multinomial factor times a sum of products of even
   powers. There are `binom(3r-1,r)>=2^r` such monomials.
   This refutes automatic preservation under arbitrary orthogonal
   substitution, not the possibility of selecting another basis.

5. **Convexity in Proposition 3.2.** Its displayed statement says
   polynomial, while the proof uses convexity to separate sublevel
   sets by the gradient. Its use here is restricted to promised
   convex objectives. It must not be cited as a general polynomial
   optimization algorithm. For `f(t)=-t^2`, level `-1`, the point
   `y=0` violates the level while `x=1` satisfies it, and the zero
   gradient at `y` cannot give the claimed strict separator.

The current continuation's radius and coefficient-row arguments
should be read in their own right, with these source antecedents
credited. A corrected proof in this project does not silently amend
the external source.

## Claim discipline and verification

The supported contribution statement is an effective point-output
theorem and an explicit separation of output models, accompanied by
exact-comparison results under stated promises. It is not a claim to
have introduced convex value optimization, rational invariant-space
computation, qualitative error bounds, or the first algebraic
irrationality examples. Publication priority remains unestablished.

The source checks used `rg`, scoped `sed` reads, full-PDF extraction
with `pdftotext -layout`, and primary-source web access. An initial
HTML extraction attempt failed because `bs4` was unavailable; PDF
extraction succeeded. The downloaded v1 PDF had 515,986 bytes and
SHA-256
`bc74956ba2d79ee6154c1a3c7d4b1d67518126e71d6ee3289d5ba12ab58042f3`.
Two independent research agents rechecked the five transfer cautions
against the primary text. These are internal reviews, not external
peer review. The targeted command
`python3 -B research-20261003-arithmetic/literature/check_source_formulas.py`
passed all five checks, including 67 rational sublevel points and
396 positive even-monomial coefficients. The source audit explains
which checks are counterexamples and which check normalization or
representation bookkeeping. None is a universal proof check.
A scoped inline Python check passed final-newline,
trailing-whitespace, and relative-link checks. The command
`git diff --check -- research-20261003-arithmetic/literature` also
passed. These document checks do not validate mathematical proofs.
No project-wide verification or CI inspection was performed for this
audit.
