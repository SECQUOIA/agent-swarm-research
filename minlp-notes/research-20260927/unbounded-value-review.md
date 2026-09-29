# Independent review of unbounded-domain value optimization

Date: 2026-09-27. Reviewer: `unbounded_value_review`.

The extension in [the saved manuscript](unbounded-value-optimization.md) is
correct for an explicitly represented rational convex QCQP over a rational
polyhedron, with weak inequalities and affine
equalities. If the feasible set is nonempty and the objective has finite
infimum, that infimum is attained and has an integer annihilating polynomial
of degree and coefficient bit length `N^{O(h+1)}`. Here `h` counts the span
of the native constraint Hessians and excludes the convex objective Hessian.
No input coordinate bounds or original constraint qualification are needed.
The manuscript's additional algebraic-recognition argument also gives
deterministic polynomial-time exact value recovery for fixed `h`.

This audit independently read the existing
[bounded value proof](hessian-span-reduction.md), the
[unbounded small-point theorem](unbounded-hessian-span.md), and the primary
attainment and perturbation source. It then checked the proposed extension
step by step. The audit found no substantive gap in that argument. This is
a proof audit, not a novelty determination or a test of a solver
implementation.

## The new convergence step

The required prior result is Luo and Zhang,
[*On the Extensions of Frank--Wolfe Theorem*](https://papers.tinbergen.nl/97122.pdf),
October 1997 report. I read Theorem 1 on printed page 3 and its proof,
and Corollary 2 on printed pages 6--7. Theorem 1 says that feasibility under
arbitrarily small positive right-hand-side perturbations implies exact
feasibility for a finite system of convex quadratic inequalities. Corollary
2 gives attainment whenever the convex quadratic objective has finite
infimum on a nonempty such system. Affine rows have zero Hessians; affine
equalities can be encoded by their two signs. These statements do not
require bounded feasible sets or Slater's condition. The report credits the
attainment statement to Terlaky's earlier work, so attainment is not a new
contribution of this research.

Fix an attained optimizer and apply the active affine restriction in the
bounded value proof. Its segment argument does not use boundedness. Adding
the affine differences between active quadratics and their Hessian-basis
combinations preserves the optimizer and the objective value. Rational
elimination gives unrestricted coordinates `u` and retained convex rows
`q_i(u)`, whose whole polynomials span a space of dimension at most `h`.
Write `theta` for their exact minimum of the restricted objective `q_0`.

For `0 < epsilon < 1`, define

```
w_epsilon = min {q_0(u) + epsilon ||u||^2 : q_i(u) <= epsilon}.
```

The old optimizer is strictly feasible. The objective has positive definite
Hessian and is coercive, so the regularized minimum and KKT multipliers
exist. The upper estimate

```
w_epsilon <= theta + epsilon ||u*||^2
```

gives `limsup w_epsilon <= theta`. It does not give a common bound on
the regularized minimizers, and none should be asserted without another
argument.

Suppose the lower limit were below `theta`. There would be a fixed
`delta > 0` and a sequence `epsilon_j` decreasing to zero with minimizers
satisfying

```
q_i(u_j) <= epsilon_j,
q_0(u_j) <= q_0(u_j) + epsilon_j ||u_j||^2 <= theta - delta.
```

Apply Luo--Zhang's perturbation theorem to the retained rows together with
the convex row `q_0 - theta + delta <= 0`. This row has zero violation
along the sequence and hence also satisfies every positive perturbation.
The theorem would give an exactly retained-feasible point with objective
at most `theta-delta`, a contradiction. Therefore
`w_epsilon -> theta`.

The possibly irrational number `theta-delta` occurs only in this
qualitative contradiction. It is not a coefficient in the rational KKT
formula used for the quantitative bound. Thus this argument neither
assumes nor conceals a bound on the encoding of the unknown optimum.

## Sparse KKT elimination

The remaining proof is the bounded argument with its ball row removed.
All of the following details are necessary and remain valid:

- Compress native multipliers using the rational coefficient vectors of
  the whole-polynomial identities, and use only rows active in the
  regularized problem. This preserves both stationarity and
  complementarity with at most `h` nonzero multipliers.
- Keep every retained row in the primal feasibility formula, including
  rows outside the chosen support. An arbitrary Hessian basis does not
  replace the original inequalities.
- The stationarity matrix is
  `Q_0 + 2 epsilon I + sum_i lambda_i Q_i`, which is positive definite.
  Adjugate reconstruction is therefore valid and its determinant is
  strictly positive. Squared-denominator clearing preserves inequalities.
- Every point of the resulting polynomial system reconstructs a global
  optimum of the regularized convex problem. Sufficiency, not merely
  necessity, of the KKT conditions supplies this direction.
- One support occurs along a sequence tending to zero. It need not occur
  for all small parameters. The scalar limit formula uses one universal
  tolerance and at most `h+2` existential variables: the regularization
  parameter, its optimal value, and the multipliers.

The case of a zero-dimensional affine restriction must be treated before
the determinant formula; then the selected optimizer is rational with
polynomial bit length. The case `h=0` also causes no difficulty. Its retained
affine quadratic rows become identically zero after the affine restriction,
and an empty multiplier support suffices.

I separately inspected the integer coefficient-height clause of Basu's
survey, Theorem 2.27, in the local source
`research-20260925/publication-sources/basu-2014-author-survey.txt`.
With two quantifier blocks of sizes `1` and at most `h+2`, and one free
variable, both degrees and coefficient bit lengths are `N^{O(h+1)}`.
Determinants and adjugates start with polynomial-bit coefficients: a common
denominator for the polynomially many restricted input coefficients has
polynomial bit length, and all expanded denominators divide a power of
that denominator of degree `O(n)`. This avoids an unjustified bound on an
arbitrary list of expanded rational coefficients.

The limit formula defines a singleton. At least one of the nonzero output
polynomials must vanish there, since otherwise all signs would be constant
on a neighborhood. Upper and reciprocal Cauchy bounds then control the
magnitude of a finite optimum and its distance from zero when nonzero.
Multiplier divergence and divergence of regularized primal minimizers do
not affect any of these steps.

## Exact decision consequences and their limits

Suppose the effective finite-value bound is
`|theta| <= B = 2^{N^{C(h+1)}}`, with `C` chosen sufficiently large.
First use the exact unbounded-domain feasibility algorithm to test the
native constraints. If they are feasible, test them again with the convex
objective-threshold row `q_0 <= -B-1`. Feasibility of this second system
implies that the original infimum is minus infinity: a finite infimum below
`-B` is ruled out by the value bound. Conversely, an objective unbounded
below passes every finite threshold. This separates infeasible, finite, and
unbounded instances.

The threshold row increases the native Hessian span by at most one. Its
coefficient length is polynomial in `N` for fixed `h`; the unbounded-domain
feasibility theorem therefore gives polynomial Turing time for fixed `h`.
Composing parameter-dependent bit bounds can increase the exponent, so
this reduction alone should not be described as retaining an
`N^{O(h+1)}` running-time bound without a separate accounting.

For a finite instance, supplied rational objective thresholds can likewise
be decided exactly. Rational bisection between the value bounds approximates
the optimum to a requested additive accuracy in polynomial time for fixed
`h` and polynomial requested precision. These decision and approximation
steps alone do not
return an exact optimizer, produce a rational feasible point, or
construct an exact algebraic representation of the value. The existence
of a small annihilator is a separate assertion from an algorithm finding
that annihilator.

All convexity assumptions remain material. In particular, adding a small
positive multiple of `||u||^2` does not make an arbitrary indefinite
quadratic objective convex. The proposed proof cannot be extended to an
indefinite objective merely by invoking the same regularization.

## Review of the saved manuscript and exact value recovery

I subsequently read the complete saved
[unbounded-value manuscript](unbounded-value-optimization.md), including
its added exact-value algorithm, and the
[algebraic-recognition audit](algebraic-recognition-source-review.md).
The final argument is sound. The manuscript chooses a strict magnitude
bound `|theta| < B`; consequently its cutoff `q_0 <= -B` is valid,
just as the slightly more conservative `-B-1` cutoff above is valid with a
nonstrict bound.

I also directly read Algorithm (1.16), Explanation (1.18), and Theorem
(1.19) in the
[Kannan--Lenstra--Lovasz primary source](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf),
printed pages 240--241. The theorem recovers the minimal polynomial from
known degree and coefficient bounds and a sufficiently accurate rational
approximation. Its precision and bit complexity are polynomial in the
degree bound and coefficient bit length; Explanation (1.18) handles numbers
of magnitude greater than one. Thus the application does not need to assume
the optimum lies in the unit interval.

The manuscript's elementary factor-height estimate was checked
independently. If an integer annihilator has degree at most `D` and
coefficient magnitudes at most `2^H`, its primitive minimal-polynomial
factor has integer cofactor by Gauss's lemma. Its leading coefficient has
magnitude at most `2^H`; all its roots have magnitude at most
`2^(H+1)` by Cauchy's bound. Expanding the product over at most `D` roots
therefore bounds every coefficient by
`2^((D+1)H+2D)`. This supplies the minimal-polynomial height required by
recognition, even though the annihilator itself is not computed.

Every bisection query concerns the same original optimal value. There is
therefore no consistency issue in combining increasingly precise
approximations. The needed number of accuracy bits is polynomial in `D,H`,
which is polynomial in the original input size when `h` is fixed.

Finally, I checked the audit's conjugate-selection argument directly. For
a recovered irreducible integer polynomial, the discriminant is a nonzero
integer. Its product formula, an upper coefficient bound, and Cauchy's root
radius bound give a lower bound on every pairwise root distance with
polynomial logarithmic size. An approximation within one eighth of that
separation bound gives an interval of half that bound's length containing
the selected value and no other root. This produces the claimed exact real
algebraic representation, rather than only an unspecified conjugacy class.

One wording correction was sent to the author: the active affine
restriction creates a *reduced* problem, not necessarily an enlarged one,
because active affine inequalities become equations. This does not change
the segment proof. No mathematical correction was needed. The final
manuscript does not claim recovery of an optimizer or an unbounded ray.

## Verification record

The mathematical verification was symbolic: independent reconstruction of
the convergence contradiction, multiplier compression, determinant
elimination, coefficient-height argument, and threshold reduction; direct
inspection of the stated primary source and the local quantitative
elimination source. No numerical experiment or finite sample could verify
the universal perturbation claim used here. No project-wide checks or CI
inspection were performed. Novelty and the strength of the comparison
with earlier few-quadratic algorithms require their separate literature
assessment.

Targeted command actually run: `python -` with an inline script checking
this review's final newline, trailing whitespace, and relative Markdown
links. The check passed initially and was rerun after the saved-manuscript
audit; all five link occurrences passed. This was a document check and
provides no additional verification of the mathematical statements.
