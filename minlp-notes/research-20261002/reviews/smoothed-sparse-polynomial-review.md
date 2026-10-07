# Independent composition review: smoothed sparse polynomial optimization

Date: 2026-10-02. Verdict: **PASS after the trace-size and weak-optimization
interface corrections.** The final actual main file, both exact-fallback
proofs, and the repaired evaluator have been reread. This review concerns the actual
[main theorem](../new-direction/smoothed-sparse-polynomial.md),
[finite-noise tails](../new-direction/polynomial-finite-noise-tails.md),
and [convex-patch evaluation](../new-direction/convex-patch-evaluation.md).
It is separate from a priority or practical-performance assessment.

## 1. Nonlinear rounding and sparse computation

The polynomial extension of the cell lower bound is valid. Sequential
mean-preserving rounding applies coordinate semiconcavity on the full
continuous hull at every intermediate point. It bounds the total increase
by `n L h_j^2/8`; it does not assume cancellation of nonlinear cross terms.
Integer nodes do not move. Shared nested partitions preserve every bag
whitelist and any designated bag cell, including points on shared cell
boundaries. Thus the conditional cell lower bound remains valid after
earlier pruning, and every original optimizer survives.

For each retained cell there is one globally consistent feasible grid
witness with value at most `f*+2E_j`. The exact separator-key dynamic
program computes these witnesses and bag min-marginals without taking
Cartesian products of neighboring row lists. Binarization bounds the
number of incident messages. Generating children and their corners costs
a constant to the bag size times the number of retained parent cells;
deduplication and sorting add polynomial overhead. The analysis counts
the deterministic complete grid, while the algorithm generates only the
needed sparse lists. This distinction is sufficient to turn the expected
survivor count into an expected work bound.

## 2. Conditional noise count

The value function `V_B` minimizes over a fixed original outside domain,
including its integer restrictions. For each coordinate, subtracting the
quadratic upper-curvature term leaves an infimum of concave functions,
which is concave. `V_B` is independent of all noise coefficients in its
bag. Neighbor comparisons for a fixed bag tuple therefore restrict each
bag coefficient to an interval whose endpoints do not involve the other
bag coefficients. Independence can be used exactly as written.

The interval width is `L*a + 4E_j/a`. There are at most three exceptional
nodes in each clipped coordinate grid and at most `w_i/a` regular ones.
Using the finite-grid interval mass bound and multiplying independent
constraints gives the stated product bound. It remains valid if its
individual upper bounds exceed one. At fine integer levels, spacing is
one and the cells are points; the integer singleton transition does not
introduce extra grid values or invalidate the incidence bound.

`M>=2^J` makes every atomic correction `w_i/(M*a_i,j)` at most one.
The conditional count never conditions the noise on previous pruning
decisions. Summing over all fixed full-grid tuples is therefore legitimate
even though the algorithm's retained lists depend on the sample.

## 3. Exact closure and quantitative stopping

Intersected coordinate hulls contain every original optimizer. Integer
coordinates are fixed only from singleton hulls. The continuous gradient
enclosure uses the full-box Hessian row bound, so it remains valid even
before integer coordinates are fixed. A strict gradient sign throughout
the hull forces the corresponding original continuous bound by the
first-order condition in each optimizer's integer slice. This rule is
not valid for integer coordinates and is correctly restricted to the
continuous ones.

Once integers and certified active continuous bounds are substituted,
the midpoint test subtracts both Hessian variation `T*r` and the proposed
modulus `g_0`. Strict positivity of that rational matrix implies uniform
Hessian lower bound `g_0 I` on the remaining box. The box still contains
all original optimizers and lies in the original feasible domain. Its
strongly convex constrained minimizer is consequently the unique global
optimizer. None of these acceptance steps trusts a probabilistic growth
or active-margin assertion.

For stopping analysis, retained witnesses have distance at most
`h_j*sqrt(nL/g_0)/2` from the unique optimizer. Adding cell width gives
the stated safe hull radius factor `A=2+nL/g_0`. The three mesh thresholds
ensure respectively:

- native integer labels are singleton values within one quarter of the
  optimal label;
- the continuous gradient enclosure error, including its midpoint-to-
  optimizer variation, is at most `tau/2`;
- the midpoint Hessian test has strict slack at least `g_0/2` after all
  active continuous coordinates are fixed.

The last step uses two-sided Taylor expansion only in the coordinates
that are interior in the original continuous face. It does not assume
full Hessian positivity at a boundary optimizer. This is a substantive
difference from the earlier deterministic convex-patch theorem.

## 4. Finite-noise interfaces and one base-only budget

The two-block formula in the tail note defines good point growth exactly,
including equality at a positive threshold. Native integer membership is
a finite disjunction of linear equalities; it increases atom count but
not the number of quantifier blocks. Its description can be exponential
while its logarithm remains polynomial in the binary base input.

The reviewer independently rendered and inspected Renegar's primary
Theorem 1.1, printed page 330. It gives the required output-format bound
for two quantified blocks and one free scalar, uniformly in arbitrary
real coefficients. It also separates integer coefficient height from
format complexity in the bit bound. Hence the scalar component count is
independent of thresholds and of fixed noise values, including hybrid
continuous/discrete sections. Identically zero output polynomials are
handled by constant signs. The successive marginal replacement argument
therefore transfers the continuous growth tail to the one finite law,
including its atoms.

The active-gradient argument also checks. On each original face and
integer assignment, conditioning away one active coefficient makes the
free stationary equations independent of it. Positive point growth
makes the relevant free Hessian nonsingular. The bound counts only these
isolated roots; other singular or positive-dimensional stationary sets
do not invalidate the isolated-root Bezout count. Each root supplies an
interval of length `2tau`. The union bound is for the intersection with
positive growth, rather than a conditional probability divided by the
probability of positive growth.

With `rho=1/(4B)`, the continuous portions of each bad-event bound are
at most `rho/2`; the chosen lower bounds on `M` make their atomic portions
at most `rho/2`. Their sum is at most `1/(2B)`. The cutoff and law are
chosen in order from base quantities, before sampling. `J` and `log M`
have polynomial base bit length. There is no sampling-precision equation
to solve and no resampling of an exceptional draw.

## 5. Exact fallback and coefficient-height dependence

The reviewer read the complete constructive fallback before its move to
the companion construction file. Its all-draw interface is valid.
Adding a symbolic even-degree perturbation makes each face's stationary
ideal have pairwise coprime leading monomials and an explicit finite
monomial quotient. Multiplication matrices have controlled Laurent
degrees and coefficient heights. Normalizing their characteristic
polynomials before specialization captures every bounded stationary
limit, including limits on a smaller face and continua of original
minimizers. Enumerated Cartesian products may contain spurious root
combinations, but they are filtered for feasibility and cannot beat the
true optimum; at least one original optimizer is included.

The algebraic-integer norm bounds correctly separate a nonzero value
difference from zero and handle equality with rational box endpoints.
Their precision is a base-only exponential times a polynomial in added
coefficient bits. The same applies to explicit determinant computation,
univariate root isolation, comparison, and later refinement. Thus the
fallback does not put sampling precision into an exponential exponent.
Its expected cost and output size are paid for by the rare-event bound.
The reviewer also read the final shorter
[lexicographic fallback](../new-direction/polynomial-exact-fallback.md).
Compactness gives a unique lexicographically selected optimizer even
when the minimizer set is a continuum. Each coordinate, and the value,
is defined by a scalar singleton formula with two quantified blocks.
Renegar's actual primary bit and height bounds separate the coefficient
length from the base-only exponential format factor. The product of the
nonconstant output atom polynomials contains the singleton as a root;
univariate isolation and sign testing select it. All coordinate formulas
refer to the same canonical full vector, so independently represented
coordinates cannot come from different optima. This actual-file proof
passes too. Its final feasibility contract correctly clips continuous
approximations, identifies integer roots exactly, and combines a
gradient-controlled approximation with the separately refined value
lower bound.

## 6. Output representation and evaluation

The main note correctly distinguishes three size claims:

1. A successful patch's compact descriptor has polynomial bit length in
   the base input, including the polynomially many sampling bits. Its
   uniform dyadic grid endpoints, substitutions, derivative bounds, and
   rational matrix certificate all have that size.
2. The complete global pruning/DP proof record has the stated expected
   work and size bound. It is not necessarily polynomial on every
   successful draw, and the compact descriptor alone does not prove
   original global optimality.
3. An exceptional algebraic output can have exponential size. It is
   correct on that same draw and is charged through the fallback budget.

For a valid patch, the capped epigraph is a full-dimensional compact
convex body even when its minimizer is on the boundary. The stated ball
around `(midpoint,V+1)` lies inside it, because the epigraph height there
exceeds every possible function value on the box. Its inner and outer
radii have polynomial rational encoding. Value, gradient, membership,
and separation queries at rational points have polynomial bit complexity
at fixed degree. The linear epigraph objective is globally Lipschitz;
the original polynomial need not be convex outside the box.

The source audit identified a substantive qualification: the rational
GLS weak-optimization theorem returns an approximately feasible point
and compares against an inner parallel body, rather than directly
returning the exactly feasible point first asserted in this interface.
The reviewer read the final saved repair and the relevant primary GLS
weak-optimization definition, Corollary 4.2.7, and oracle Turing-model
conventions. The invocation now matches that source.

Write `r_K` for the known epigraph inradius. Moving a true optimizer
toward the known interior-ball center with weight `epsilon/r_K`
produces a point in the eroded body and raises its objective by at most
`epsilon*(2W+1)/r_K`. With `epsilon<=r_K/2`, that eroded body is
nonempty, so the weak optimizer cannot correctly return the emptiness
alternative. Its returned last coordinate therefore gives lower bound
`t-[1+(2W+1)/r_K]*epsilon`. Projecting the returned rational spatial
point onto the box is nonexpansive relative to a nearby feasible epigraph
point. The gradient bound then gives an exactly feasible value at most
`t+(G+1)*epsilon`. The resulting interval has width at most
`[G+2+(2W+1)/r_K]*epsilon`, exactly as asserted.

The final oracle includes the box, upper-cap, and lower-epigraph
separators, with rational infinity-norm normalization. Translation by
the rational epigraph center supplies the circumscribed-body input to
GLS. All constants and query answers have polynomial encoding length.
This establishes the required polynomial-bit evaluation interface;
the corrected argument does not assume the raw weak-optimization output
is feasible.

Strong convexity and a certified gap
`min(2^-q,(g_0/2)2^-2q)` give the claimed coordinate and objective
accuracy with polynomial dependence on `log(1/g_0)`.
It would be incorrect to use the earlier grid evaluator's numerical
`L/g_0` dependence here. The algebraic fallback supports the analogous
base-exponential refinement bound for every exceptional draw.

The expectation claim is for the sampled problem under one specified
finite law. It does not give a deterministic polynomial all-draw runtime
or FPT dependence on bag size. Numerical integer widths remain in the
expected cell-count factor.

The subsequently added original-objective consequence is valid. If `a`
is a sampled-objective lower bound and a feasible rational point `y` has
sampled gap at most `delta`, then
`a-max_X gamma'x` is an original-objective lower bound, and its gap to
`F_0(y)` is at most `delta+sigma*W`. In particular, an exact sampled
optimizer has original regret at most `sigma*W`. Taking
`sigma=epsilon/(2W)` and `delta=epsilon/2` gives an every-draw original
additive certificate. The fallback's explicit clipping and gradient-bound
procedure supplies the required feasible rational approximation even on
exceptional draws. Substitution into the expected count retains numerical
inverse-accuracy dependence; this is not a new improved approximation rate.

## 7. Targeted checks actually run

The reviewer ran

```sh
python research-20261002/reviews/check_smoothed_polynomial_review.py
```

The [persistent diagnostic](check_smoothed_polynomial_review.py) passed
four exact rational budget fixtures, including cutoff depth 3433 and
4006 noise bits. It verifies both probability allocations, the expected
fallback payment, atomic terms at representative levels, and all three
closure inequalities. Three additional finite laws include an actual
endpoint atom where a linear objective is constant on its whole interval.
That atom has neither strict active-gradient signs nor positive Hessian,
so a same-draw exact fallback is necessary. Exact finite-law growth and
active-gradient counts satisfy their bounds.
Three additional exact cases verify the weak-optimization cleanup for
points lying outside both the box and epigraph, including boxes of width
`2^-200`. Projection and the lower-bound correction give the requested
certified gap in all three. These cases specifically exercise the
repaired contract rather than pretending the oracle returned a feasible
point.

These tests do not rerun the author's nonlinear sparse-DP fixture,
implement general quantifier elimination, or establish expected runtime
by experiment. The primary-source rendering command was
`pdftoppm -f 2 -singlefile -scale-to 2000 -png` on the local Renegar PDF;
the resulting page image was inspected. The GLS definition, corollary,
and oracle Turing-model conventions were read in the local primary text.
Scoped whitespace, paired-delimiter, and local-link checks passed for
the final review. No project-wide verification,
CI inspection, external source search, or index edits were performed.
