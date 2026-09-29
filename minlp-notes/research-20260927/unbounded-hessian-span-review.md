# Adversarial review of the feasible-point radius extension

Date: 2026-09-27. Status: independent proof review completed. This review
finds no gap in the radius theorem or its feasibility consequences under the
assumptions below. Publication priority remains unestablished. The reviewer
did not devise the radius extension and did not edit its primary proof.

## Claim reviewed

Let `F` be a nonempty set defined by explicitly encoded rational affine
equalities and inequalities and rational convex quadratic inequalities in
`R^n`. There are no input coordinate bounds. Let `N>=2` be the total binary
input length and let

```
h = dim_Q span{Q_i},
```

where the `Q_i` are the native constraint Hessian matrices. Then `F` contains
a point whose coordinates have magnitude at most
`2^{N^{O(h+1)}}`. The exponent is effective and uniform over all such inputs.
The statement bounds the magnitude of a real feasible point. It does not
assert that a rational feasible point exists.

The parent proof is in
[unbounded-hessian-span.md](unbounded-hessian-span.md). The relevant earlier
argument is [hessian-span-reduction.md](hessian-span-reduction.md).

## Independent proof audit

**Existence of the point used in the proof.** The set `F` is closed. Its
intersection with the norm sublevel set through any one of its points is
nonempty and compact. Therefore

```
theta = min_{x in F} ||x||^2
```

exists. This step needs nonemptiness but no known norm bound. The norm
objective is strictly convex, so its minimizer is unique.

**Active restriction.** At a minimum-norm point `x*`, keep the active
quadratic inequalities, keep all original affine equalities, turn active
affine inequalities into equalities, and delete the inactive rows. If the
enlarged set contained a point with smaller norm, a sufficiently short segment
from `x*` toward it would satisfy every deleted row and improve the original
objective. Thus the minimum norm is unchanged. Convexity of every retained
quadratic is used here. This step would not be valid for general nonconvex
quadratic systems.

Choose a basis of the retained Hessian span, write each retained Hessian as a
rational linear combination of that basis, and impose the resulting affine
polynomial differences as equalities. All these differences vanish at `x*`.
This additional restriction keeps the optimum. Rational elimination gives
`x=x0+Vu`, with `V` of full column rank and all coefficients of polynomial
binary length in `N`. Neither these equations nor their coefficient bounds
contain the coordinates of `x*`.

After restriction, the retained complete quadratic polynomials have span at
most `h`. The restricted objective

```
f(u)=||x0+Vu||^2
```

has Hessian `2 V^T V`, which is positive definite when free variables remain.
It is therefore coercive. If no free variables remain, the retained point is
rational with polynomial-size coordinates and the radius conclusion follows
directly.

**No ball and no objective perturbation are needed.** For each
`0<epsilon<1`, minimize `f(u)` subject to every retained quadratic being at
most `epsilon`. The original retained point is strictly feasible. Coercivity
gives an optimizer, and Slater's condition for this relaxed problem gives
nonnegative KKT multipliers. Every relaxed optimizer satisfies
`f(u)<=theta`, since the original point is available as a competitor.
Consequently all such optimizers lie in one compact set, even though its
radius is not yet numerically known.

This is not circular: compactness is used to prove convergence; the later
algebraic bound supplies a radius computable from the input. Every sequence
of relaxed optimizers with `epsilon` tending to zero has a subsequence
converging to an unrelaxed feasible optimizer. Their values therefore converge
to `theta`. In fact uniqueness implies convergence of the points too.

**Sparse multipliers and primal elimination.** On the restricted affine
space, the constraint gradients are combinations of at most `h` polynomial
gradients with rational coefficient vectors. Conic Caratheodory applied only
to active rows preserves stationarity with at most `h` nonzero multipliers;
complementarity is preserved because all selected rows are active. There is
no ball multiplier in this version.

The stationarity matrix is

```
M = 2 V^T V + sum_i lambda_i Qtilde_i.
```

It is positive definite for all nonnegative multipliers. Thus its determinant
is positive and the primal variables can be eliminated by its adjugate. The
resulting polynomial system must retain feasibility of every original
retained row, including rows whose multipliers have been discarded. Its
degrees are `O(n+1)` and its coefficient bit lengths are polynomial in `N`.
The determinant expansion and common-denominator bounds in the earlier
note apply without change; the number of expanded monomials need not be
polynomial in `N` for variable `h`.

Choose one multiplier support along a sequence with `epsilon` tending to
zero. The two-block quantified formula expressing arbitrary approach of its
KKT values to a real scalar defines exactly `{theta}`. Its block sizes are
one and at most `h+2`: the second block contains `epsilon`, the objective
value, and the supported multipliers. The coefficient-sensitive elimination
bound used in the earlier theorem therefore supplies a nonzero integer
annihilating polynomial for `theta`, with degree and coefficient bit lengths
`N^{O(h+1)}`. This use of quantifier elimination remains an explicit theorem
dependency; the reviewer did not rederive that general elimination theorem.

**Turning height into radius.** If the annihilating polynomial has coefficient
bit length at most `H`, its nonzero leading integer coefficient has magnitude
at least one. Cauchy's upper root bound gives `theta<=1+2^H`. Hence the
minimum-norm point satisfies

```
|x_j| <= sqrt(theta) <= 2^{H+1}
```

for every coordinate. This also covers `theta=0`. A sufficiently large
effective uniform bound `H=N^{C(h+1)}` therefore supplies the asserted
coordinate box. No active set needs to be discovered in order to write that
box from `N` and `h`.

## Consequences checked and boundaries retained

Appending the computed box preserves continuous feasibility. Applying the
boxed exact-decision theorem then gives polynomial Turing time for each
fixed `h`, including sets with empty interior. A direct composition of the
existing bounds gives the conservative explicit complexity
`N^{O((h+1)^2)}`. A linear-in-`h` exponent would need more careful separate
tracking of dimensions, degrees, and coefficient height.

If only the integer coordinates are explicitly bounded, their binary lengths
are polynomial in the original input. Substitution of any such integer vector
leaves a continuous system of uniform polynomial input length. Applying the
radius theorem to every nonempty slice gives one uniform continuous box
preserving all feasible integer assignments. The bounded integer-projection
theorem then applies when the original quadratic Hessians are jointly PSD.
No enumeration of integer vectors is needed. The resulting rational MILP has
polynomial size for fixed `h` and no new integer variables.

The following distinctions remain necessary:

- The radius is an existence bound; feasible sets can still be unbounded.
- The point whose existence is proved can be irrational. The polynomial-size
  radius does not provide an exact rational continuous witness.
- Slice convexity is enough for the radius and continuous decision argument.
  Full joint convexity is still needed for the particular compact polyhedral
  approximation in the mixed-integer projection theorem.
- Integer bounds have not been removed by this argument.
- Exact rational-threshold decisions can use a newly computed box after
  adding the threshold inequality. Preserving all values of a continuous
  objective with one fixed box requires a separate argument and is not a
  consequence of a feasible-point radius alone.

## Prior work and the lower-bound check

The local full text of Bienstock, Del Pia, and Hildebrand,
[*Complexity, Exactness, and Rationality in Polynomial Optimization*](https://arxiv.org/abs/2011.08347),
Example 6.1, explicitly gives the convex system

```
y_1 >= 2,
y_{i+1} >= y_i^2  (i=1,...,n-1).
```

It forces `y_n>=2^{2^{n-1}}` and is attributed there to Ramana and Khachiyan.
The nonzero constraint Hessians are the independent coordinate matrices on
the first `n-1` coordinates, so this system has `h=n-1`. It shows why no
polynomial-bit universal radius independent of the structural parameter can
be asserted. This is a classical example, not a new lower-bound construction.

The same paper, Sections 3 and 6, distinguishes exact feasible points,
near-feasible rational certificates, and encoding-size issues. Its
fixed-ambient-dimension statements do not directly cover this theorem's
arbitrarily large ambient dimension and fixed matrix-span dimension. The
separate [prior-work audit](hessian-span-prior.md) gives the more substantial
comparisons with few-quadratic algorithms, algebraic-degree results, and
mixed-integer convex quadratic theory. This limited additional search found
no immediate equivalent radius theorem, but it does not establish novelty.

## Verification record

The reviewer independently read the Hessian-span value proof, the boxed
exact-feasibility proof, and the integer-projection proof through its main
reduction, then made a final pass over the saved primary draft
`unbounded-hessian-span.md`. The active restriction, norm coercivity, relaxed-limit argument,
support sparsification, Cauchy bound, uniform integer-slice substitution, and
classical squaring example were checked symbolically. The named local prior
full text was searched with `rg` and its relevant sections read. Internet
searches covered convex-quadratic small-solution bounds, few quadratic
inequalities, and Hessian-span feasibility; only the named primary source is
used for the comparison above.

No numerical experiment, Lean proof, or implementation of the elimination or
ellipsoid algorithms was performed. These would establish different forms of
evidence; numerical instances cannot verify the uniform symbolic theorem.
Targeted document checks were `git diff --check --
research-20260927/unbounded-hessian-span-review.md` and an inline Python check
of this file's final newline, trailing whitespace, and control characters;
both passed. No project-wide checks or CI inspection were run.

The author also proposed a shorter radius-only argument using the established
Grigoriev--Pasechnik sampling theorem. The geometric reduction is sound: after
the active affine restriction, the common zero set of the at most `h` basis
quadratics is nonempty and every point in it is retained-feasible. A small
algebraic sample from that zero set therefore bounds the minimum norm from
above, even if the sample violates a deleted inactive row. Turning the
sample's bounded rational-univariate representation into a coordinate bound
requires root separation or resultant elimination to control nonzero
denominators. This alternate route establishes the radius once its cited
sampling-height bound is supplied; it does not alone establish the stronger
minimum-norm-value annihilator claim. The primary proof above does not depend
on this alternate route.
