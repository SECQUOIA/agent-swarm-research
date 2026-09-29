# Independent review of the unbounded integer extension

Date: 2026-09-27. Status: proof review completed with one corrected
background claim. No remaining gap was found in the small integer witness
theorem or its stated feasibility consequence. This is evidence from an
independent audit, not a formal proof or an established priority claim.

The reviewed construction is in
[unbounded-integer-frontier.md](unbounded-integer-frontier.md). The reviewer
did not devise its active-set projection construction. During review, the
reviewer proposed applying the imported integer-witness theorem directly to
one common quantified formula, avoiding an unnecessary elimination step in
the witness proof. The quantifier-free projection lemma remains a separate
valid consequence.

## Scope of the result

The input is an explicitly encoded rational system of affine equalities,
affine inequalities, and jointly convex quadratic inequalities in `(z,x)`,
where `z` has `k` integer coordinates and `x` has arbitrarily many continuous
coordinates. No coordinate bounds are part of the input. Let `N>=2` denote
its total binary length and let `h` be the dimension of the rational linear
span of the continuous `xx` Hessian blocks.

If a feasible integer assignment exists, the theorem gives one whose
coordinate bit lengths are at most

```
N^{O((h+1)(k+1)^4)}.
```

Together with the continuous-radius theorem and the bounded integer-projection
reduction in this batch, this gives exact feasibility and a feasible integer
assignment in polynomial Turing time for fixed `k,h`. It does not promise a
rational continuous feasible vector, an FPT running time, or a compact MILP
preserving every feasible integer assignment of the unbounded problem.

## Independent mathematical audit

### Active restriction and parameter-dependent affine equations

At a fixed feasible real parameter `z`, the continuous fiber is closed and
convex. Its squared norm has a unique minimizer `x*`. Keeping active
quadratic rows, turning active affine inequalities into equalities, and
deleting inactive rows preserves this minimum: any improvement in the
enlarged set would improve the original problem along a sufficiently short
segment from `x*`. Every deleted row is strict at the segment's initial
point. Strict convexity of the norm gives uniqueness in the enlarged convex
set too.

The continuous Hessian dependencies have rational coefficients of polynomial
bit length, independent of the numerical value of `z`. Subtracting the
corresponding combinations of active whole polynomials leaves equations
affine in `x`. Their coefficients are affine in `z`; their constant terms
are quadratic in `z`. All vanish at `x*`. Adding these equations therefore
preserves the norm optimum and makes the complete retained polynomials lie
in a space of dimension at most `h` after restriction. Merely spanning their
Hessians would not suffice for the later multiplier argument; the whole
polynomial identities are explicitly established.

### Rank charts cover exceptional parameters

For a chosen pivot minor of `B(z)x=d(z)`, Cramer's rule gives
`x=a(z)+V(z)u`. The free-coordinate rows of `V` are an identity matrix.
The conditions `delta(z)!=0`, `B(z)a(z)=d(z)`, and `B(z)V(z)=0` ensure
that the parameterization gives the complete affine solution space. The
pivot gives rank at least `r`; the `n-r` independent kernel columns give
rank at most `r`. Consistency follows from the particular solution.

All possible ranks and minors must be included. A generic-rank argument
alone can miss feasible parameters where the rank drops. The draft includes
these cases, including rank zero and no remaining continuous coordinates.
Its number of charts can be large; the proof never treats that number as
polynomial.

### Coercivity and sparse stationarity

On a valid chart, the norm objective has positive-definite Hessian
`2 V^T V`. Relaxing each retained quadratic row to at most `epsilon>0`
gives strict feasibility at the original point, a unique minimizer, and
ordinary nonnegative KKT multipliers. The objective at that minimizer is at
most `||x*||^2`; consequently the primal points stay bounded without any
known numerical radius. Every accumulation point as `epsilon` tends to zero
is feasible for the retained problem and has minimum norm. Uniqueness gives
convergence to `x*`.

Conic Caratheodory is applied to the coefficient vectors of the retained
whole polynomials, using only rows with positive multipliers. It preserves
the aggregate stationarity gradient using at most `h` rows. The selected
rows remain active, so complementarity would also be preserved. The final
formula does not need to impose complementarity: its candidate points are
checked directly against every original row.

For every nonnegative supported multiplier vector, the stationarity matrix
is positive definite. Adjugates therefore give an actual rational point
`X(z,lambda)`. The primal points can converge even when the multipliers
diverge; no multiplier bound is asserted or used.

### Exact bounded-approximation formula

The decisive formula has the form

```
exists R>0, for all t>0, exists lambda>=0:
    some chart/support is valid,
    ||X(z,lambda)||^2 <= R,
    every original constraint has violation <= t.
```

Multiplier vectors can be padded to `max(1,h)` coordinates across all
charts. In the forward direction, one original chart and one support from a
convergent subsequence suffice. In the reverse direction, the chart and
support may vary with `t`: this causes no problem. Choose `t=1/j`; every
resulting point lies in the same ball and meets every original row to error
at most `1/j`. A convergent subsequence gives an exactly feasible point of
the fixed fiber. Thus placing the finite disjunction inside the three
common quantifier blocks is valid.

Two safeguards are essential to this proof as written. The radius is chosen
before the universal error tolerance, and all original rows are tested,
including rows deleted in constructing a candidate chart. These prevent
uncontrolled limits or spurious active-set certificates. The formula's
truth is established separately for each fixed free parameter `z`; it does
not take limits in the integer coordinates.

### Degree, height, and the imported witness theorem

A determinant of a matrix of polynomial entries has degree bounded by its
dimension times the entry degree. Coefficient bit lengths grow by the
lengths of products and the logarithm of the number of summands. Here matrix
sizes, initial degrees, and initial coefficient bit lengths are polynomial
in `N`. The logarithm of the number of possible monomials in at most `N`
variables of polynomial degree is also polynomial in `N`. Thus the chart
minors, stationarity adjugates, rational point numerators, and common
denominators all retain degree and coefficient bit bounds `N^{O(1)}`.

Clearing rational input coefficients uses a common integer denominator of
polynomial bit length. Substituted inequalities use an even power of the
rational-point denominator, together with its nonzero guard. Multiplication
by an unsigned denominator would be invalid on negative-denominator charts.
The draft avoids that error.

The primary text of
[Khachiyan--Porkolab (2000)](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1 on page 208, was checked directly. For convex solution sets of
first-order formulas it bounds optimal integer coordinates by
`l*d^{O(k^4) product_i O(n_i)}` bits, independently of the number of
predicates. Feasibility uses an extra integer coordinate fixed to zero, as
explained immediately before that theorem. Applying it to block sizes
`1,1,max(1,h)` gives the claimed witness bound. The formula's total length
can be large; this application bounds a witness and does not construct the
formula algorithmically. Proposition 2.1 on page 211 separately supports
the stated quantifier-free degree and height bounds.

The result requires convexity of the integer-coordinate projection. Joint
PSD Hessians supply it. Merely convex continuous slices suffice for the
projection formula, but do not justify this integer-witness step.

### From a witness bound to exact feasibility

The effective bound supplies an integer-coordinate box retaining at least
one feasible assignment when one exists. For fixed `k,h`, substituting any
integer vector in that box gives a continuous instance of uniformly
polynomial encoding length. The reviewed continuous-radius theorem supplies
a common continuous box preserving nonemptiness of each retained fiber.
The existing bounded MILP reduction then applies. The procedure computes
conservative size bounds from the input and parameters; it does not
enumerate the charts or possible integer assignments.

This composition proves the claimed fixed-parameter polynomial-time
statement. It can increase the exponent, so the conservative choice not to
state a sharp final running-time exponent is appropriate. Its dependence on
the two earlier constructive reductions must remain explicit.

## Correction found during review

The first draft said that the projected set could be nonclosed under the
joint-PSD assumptions. That background assertion was incorrect. Linear
images of sets defined by finitely many convex quadratic inequalities are
closed; affine equations can be written as two affine inequalities. An
independent primary exposition is
[Bertsekas's 2007 convex-analysis slides](https://web.mit.edu/dimitrib/www/Convex_Slides_2007.pdf),
PDF page 64, following the quadratic set-intersection result. The author
corrected the statement. The proof does not depend on this closedness
theorem, and its bounded-approximation argument remains valid for the broader
slice-convex projection lemma.

## Significance, novelty, and verification limits

The imported integer-witness theorem is established prior work. The
candidate contribution is reducing the quantified continuous information
from arbitrarily many primal coordinates to at most `h` multiplier
coordinates per chart, while controlling coefficient sizes at exceptional
parameter values. The existing one-quadratic results discussed in the
primary note remain stronger on that special class. This audit did not
establish priority for the new structural parameterization.

The exact script
[check_unbounded_integer_review.py](check_unbounded_integer_review.py)
checks three boundary examples: a parameter-dependent rank drop with a
diverging generic chart, a jointly convex constraint requiring diverging
KKT multipliers to reach its feasible point, and inequality clearing on
negative-denominator charts. The targeted command

```
python research-20260927/check_unbounded_integer_review.py
```

passed. These checks illustrate why the safeguards matter; they do not
verify the general quantifier-elimination or integer-witness theorems.
Targeted inline Python checks of the two review files' final newlines,
trailing whitespace, and control characters also passed. The scoped command
`git diff --check -- research-20260927/unbounded-integer-review.md research-20260927/check_unbounded_integer_review.py`
returned no errors; the inline checks cover these newly created files.
No implementation of the theoretical algorithm, Lean proof, project-wide
verification, or CI inspection was performed.

## Follow-up objective extension and review provenance

After completing the feasibility review, this reviewer proposed the extension
to rational linear objectives depending only on the integer variables.
Consequently this review is not independent evidence for that proposed
extension. A fresh reviewer was assigned to it. That reviewer subsequently
proposed the stronger case of a rational convex quadratic objective depending
only on the integer variables. The present reviewer independently checked
that strengthening as follows.

Choose a positive integer `L` clearing all coefficients of the objective
polynomial and write `p(z)=L f(z)`. Then `p(z)` is integral on integer
assignments. Add an integer epigraph coordinate `w` and the inequality
`p(z)-w<=0`. This is jointly convex and has zero continuous `xx` Hessian,
so the parameter `h` is unchanged. Minimizing integer `w` is equivalent to
minimizing `p`; if bounded below, its feasible integer values have a least
element. The optimization version of the imported witness theorem bounds an
optimal `(z,w)` using the augmented input, before any threshold is added.

With a bound `B` on optimal `|w|`, the feasibility test `p(z)<=-B-1`
classifies unboundedness after original feasibility is known. In the finite
case, the optimum lies in `[-B,B]`. Integer threshold bisection uses
polynomially many feasibility calls of polynomial encoding length for fixed
`k,h`. Every threshold adds a jointly convex quadratic with zero `xx`
Hessian. A feasible integer assignment at the least feasible threshold has
exactly that integer objective value. Division by `L` gives the original
rational optimum.

No gap was found in this strengthening. Its convexity and dependence only on
integer coordinates are essential to this argument; no claim for objectives
depending on continuous variables follows. The separate objective review
records the fresh reviewer's contribution and checks of the final statement
in [integer-linear-optimization-review.md](integer-linear-optimization-review.md).
The present reviewer also read the saved strengthened corollary, including
the integer epigraph and threshold-bisection algorithm, and found no mismatch
between that statement and the argument checked above.
