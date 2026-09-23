# Independent review of the monotone polynomial inverse approximation

Date: 2026-09-05. Reviewer: independent `inverse_audit_one` agent.
Verdict: **PASS**. The explicit dyadic choice noted below has been incorporated. No mathematical
obstruction was found in the approximation theorem or its stated box-follower
bilevel consequence. This review does not establish priority or certify the
separately developed resource-coupled extension.

Reviewed: [candidate lemma](certified-monotone-polynomial-inverse-approximation.md)
and the arrangement, polynomial optimization, and rational recovery steps of
the [existing bilevel algorithm](../results/bilevel-bounded-power-accuracy-bit-algorithm.md).
The review independently checks the proof; diagnostics are being handled by
the second auditor and are not counted here as independent evidence.

## Uniform inverse modulus

The interpolation argument is valid even with signed coefficients. Strict
increase puts all interpolation values of `g-g(a)` in `[0,mu]`; the basis
denominators are exactly `(h/D)^D j!(D-j)!`. Summing their reciprocals uses
`sum_j 1/[j!(D-j)!]=2^D/D!`. Applying the resulting absolute-value bound
at both zero and one gives the claimed lower bound on `mu`.

With `e=eta/4` and `delta=(e/(2D))^D/4`, an inverse increment at least `e`
would force a target increment at least `2 delta`. Thus intervals of target
length at most `delta` have inverse oscillation strictly less than `e`.
The bit length of `delta` is polynomial in numerical degree and accuracy
bits. No lower bound on the derivative is used.

For complete algorithmic specificity, the reviewed revision chooses `rho` as the **largest dyadic
number at most** `min(delta/[4(D+1)],1/16)`. This guarantees the polynomial
bound on `log(1/rho)` invoked later. Merely requiring the two upper bounds
allows unnecessarily tiny choices, although the intended efficient choice
is immediate. This is an encoding clarification, not a change of theorem.

## Critical values and the rational partition

The real formula in variables `u,v,s` describes exactly the real parts of
complex critical values. Splitting complex polynomial evaluation into real
and imaginary parts does not introduce extra solutions: each pair `u,v`
is precisely one complex root of `g'`. Although multiplicities and repeated
values are possible, the image remains a finite set of cardinality at most
`D-1`. The degree-one case correctly has no critical values.

Fixed-dimensional quantifier elimination is applicable with growing dense
degree. Expanding `(u+iv)^k` introduces polynomially many terms and binomial
coefficients of polynomial bit length. A univariate description of the
finite image can be isolated, filtered, and refined to rational brackets
with polynomial bit length. These are established algorithmic imports;
[Basu's primary-author survey, Theorem 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf)
states the required degree and coefficient-size bounds for quantifier
elimination. Fixed variable counts make those bounds polynomial here.

The padded intervals have total length at most `delta`, including endpoint
padding. Their merged components therefore have inverse oscillation less
than `e`; an `e`-accurate rational inverse value at each midpoint gives
error less than `2e` everywhere in that component. Monotone bisection
produces such a rational value by shrinking a response bracket, so it does
not require a derivative bound near flat points.

For a complementary gap `[a,b]`, every retained critical real part lies
at least `rho` behind one of its boundary components. Merging overlapping
intervals preserves that statement. Critical real parts outside `[-1,2]`
are more than one away from `[0,1]`. These facts prove the stated lower
bound `min(tau-a+rho,b-tau+rho)` on real-part distance, hence also on
complex distance. Real parts of nonreal critical values must be included;
the construction correctly does so.

## Holomorphic branches and approximation error

On either half of a gap the geometric panel construction has half-width
at most `d(tau)/64`. Its rational denominators grow by only polynomially
many factors of 32 or 33. There are `O(log(1/rho))` panels per gap.

The derivative upper bound `L` is sufficient to find a rational response
center `z0` with `|g(z0)-tau|<=d/64` using response bisection. It is not
being used as an inverse Lipschitz constant. This center remains strictly
inside the response interval. Every critical value is at distance at least
`63d/64` from `t0=g(z0)`, whereas the chosen analytic radius is `d/4`.

The asserted single inverse branch follows from properness, not merely
from absence of real critical points. Restrict the polynomial map to the
preimage of a slightly enlarged disk still containing no critical value.
It is a finite unramified covering. A connected component of a covering
of a simply connected disk maps bijectively onto that disk; the inverse
is holomorphic by the nonvanishing derivative. This proves the needed
neighborhood of the closed Cauchy disk. The inverse branch containing
`z0` agrees with the real increasing inverse along the real panel.

The bound on `M` dominates the elementary root bound for `g(z)-t` on the
disk, where `|t|<2`. The panel-to-radius ratio is at most `1/8`.
Using the weaker ratio `1/2`, the omitted Taylor tail is at most
`M*2^(-q)<=eta/4` for the stated choice of `q`; the claimed `eta/2`
bound is therefore conservative. The proof handles zeros of `g'` on the
original real interval by constant pieces around the corresponding
critical values.

## Exact rational encodings

Translating the polynomial to the rational point `z0` and clearing
denominators produces integer `A_h,Q` of polynomial bit length, with
`A_1!=0`. The recurrence for `c_n` is correct. A product of `h` earlier
coefficients whose indices sum to `n` has denominator dividing
`A_1^(2n-h)` after factoring `Q^n`. Division by the additional `A_1`
leaves a denominator dividing `A_1^(2n-1)`, since `h>=2`. This proves
the displayed common-denominator representation without a positivity
assumption on any coefficient.

Cauchy's bound gives polynomial bit length for the numerators over those
common denominators. Intermediate convolutions also have polynomial bit
length: a term contains at most `q` factors, and a coefficient sum has at
most `2^(q-1)` positive-index compositions before accounting for the
polynomially many values of `h`. Their logarithms are polynomial. Exact
truncated polynomial arithmetic therefore suffices; there is no hidden
unit-cost operation on exponentially encoded rational numbers.

The number of pieces, their degrees, rational breakpoints, and expanded
coefficients are all polynomial in the dense input and accuracy bits.
At shared endpoints both neighboring branches obey the same uniform
bound; continuity of the approximating function is not needed.

## Bilevel transfer and limits

An arbitrary strictly convex univariate polynomial cost has a strictly
increasing polynomial derivative on the follower interval. Normalizing
that derivative by its positive endpoint difference preserves rational
polynomial encoding. Its clipped inverse is the unique box response.

Substituting affine leader loads into the new rational breakpoints yields
polynomially many hyperplanes. With fixed leader dimension, the earlier
cell enumeration remains polynomial. On each closed cell the selected
response approximants give a rational polynomial objective with a uniform
error bound, including all cell boundaries. The degree and coefficient
bits supplied by the present lemma meet the requirements of the earlier
fixed-dimensional algebraic optimization step.

The earlier rational recovery uses a convex combination of rational cell
vertices and rounds its barycentric weights. It therefore preserves exact
leader feasibility, including lower-dimensional cells. The derivative
bound used for recovery concerns the rational approximating objective,
whose coefficient bits are controlled here. It never assumes the true
response is Lipschitz. Signed affine upper objectives cause no problem
because their coefficient absolute values determine the response error
budget.

The transfer establishes additive optimization in accuracy bits, with
fixed leader dimension and dense polynomial local costs. It does not
give exact arithmetic for sums of algebraic responses, exact feasibility
for response-dependent upper constraints, polynomial dependence on a
sparsely encoded degree, or a resource-coupled theorem without its own
dual and residual analysis. No such stronger claim is needed by the
reviewed statement.

## Independent source-comparison check

The [bounded source comparison](monotone-polynomial-inverse-approximation-novelty.md)
is appropriately limited. I independently opened the published text on the
cited mirrors. [Farouki, Sections 1–3](https://www.scribd.com/document/373920033/rerwe)
assumes a positive derivative, discusses series reversion and its convergence
radius, and gives a least-squares inversion algorithm. Section 1 also
explicitly discusses uniform convergence of Bernstein inverse approximants;
therefore uniform approximation itself is not new. The relevant distinction
is the complete polynomial bound in accuracy bits with rational piecewise
output and possible derivative zeros.

[Walsh, Theorem 1 and the following paragraph](https://paperzz.com/doc/7111378/a-polynomial-time-complexity-bound-for-the-computation-of...)
establishes polynomial bit complexity for the singular part and states that
polynomial bounds for a requested number of subsequent terms follow, while
omitting that latter analysis. The comparison correctly credits this prior
algebraic-series arithmetic. Neither checked passage states the combined
global partition and uniform rational representation theorem reviewed here.
That observation does not establish priority against uninspected literature.
