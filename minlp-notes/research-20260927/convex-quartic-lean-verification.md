# Focused Lean verification of the quartic example

Date: 2026-09-28. Status: the standalone file passed targeted Lean checking.
The proof is in
[ConvexQuarticIrrationalZero.lean](../formal/ConvexQuarticIrrationalZero.lean).
It uses the repository's existing pinned Lean 4.33.1 and Mathlib cache;
no dependency, toolchain, or project build configuration was changed.

## Verified statements

The definitions `quadratic` and `quartic` reproduce the displayed
polynomial \(A\) and
\(F=A^2+10000((x^2-y)^2+(y^2-2x)^2)\) in
[the mathematical note](convex-quartic-irrational-zero.md).

Lean verifies:

- `quartic_nonneg`: \(F(x,y)\ge0\) for all real \(x,y\).
- `quartic_eq_zero_iff`: \(F(x,y)=0\) if and only if
  \(x^3=2\) and \(y=x^2\).
- `quartic_le_zero_iff`: the same characterization for \(F(x,y)\le0\).
- `cube_two_bounds` and `cube_two_irrational`: every real solution of
  \(x^3=2\) lies strictly between one and two and is irrational.
- `quartic_zero_unique` and `quartic_has_zero`: the real zero exists and
  is uniquely \((2^{1/3},2^{2/3})\), with the first coordinate defined
  through real exponentiation.
- `quartic_pos_at_rationals` and
  `quartic_has_no_rational_nonpositive_point`: every rational pair gives
  a positive value; consequently the zero sublevel contains no rational
  point.
- `quartic_line_deriv`, `quarticFirst_line_deriv`, and
  `quartic_line_second_deriv`: formal differentiation of the original
  polynomial along every affine line, twice, identifies its second
  derivative with the displayed polynomial `hessianForm`.
- `hessian_sos_identity` and `hessianGapSOS_nonneg`: the exact
  [21-square rational certificate](convex-quartic-rational-sos.md) holds
  in the original coordinates and has nonnegative right-hand side.
- `quartic_second_deriv_lower_bound`: for every real \(x,y,a,b\),
  \[
    \left.\frac{d^2}{dt^2}F(x+ta,y+tb)\right|_{t=0}
                     \ge4096(a^2+b^2).
  \]
- `quartic_line_convex` and `quartic_convex`: the actual function
  \((x,y)\mapsto F(x,y)\) is globally convex, stated as
  `ConvexOn ℝ Set.univ` on `ℝ × ℝ`. The proof applies Mathlib's
  second-derivative convexity theorem on each affine line, then transfers
  its endpoint inequality to arbitrary points in the plane.

The zero characterization is proved directly from the three squared
residuals. It does not assume convexity or uniqueness from the mathematical
note. Irrationality uses Mathlib's theorem that a real root of an integer
power equation is irrational unless it is an integer, together with the
strict interval \((1,2)\). It does not assume irreducibility of the cubic
as an unproved hypothesis.

## Commands and observed results

From `formal/`, the command actually run was:

```sh
lake env lean ConvexQuarticIrrationalZero.lean
```

After adding the directional-derivative and rational-certificate proofs,
the same targeted command was rerun and exited with code zero and no
warnings. The later functional convexity bridge also passed the same
targeted command. The file prints the transitive axioms of six headline theorems.
Every output lists only
`propext`, `Classical.choice`, and `Quot.sound`:

```text
ConvexQuarticIrrationalZero.quartic_eq_zero_iff
ConvexQuarticIrrationalZero.quartic_zero_unique
ConvexQuarticIrrationalZero.quartic_has_zero
ConvexQuarticIrrationalZero.quartic_has_no_rational_nonpositive_point
ConvexQuarticIrrationalZero.quartic_second_deriv_lower_bound
ConvexQuarticIrrationalZero.quartic_convex
```

The checked source fingerprint, obtained with
`sha256sum formal/ConvexQuarticIrrationalZero.lean`, is:

```text
71930973ac11e67f5b223414bad754c6c112723acb99b2c0bd59e08f8d28dc61
```

## Scope and remaining work

The positive curvature bound is formalized through the actual second
derivative on every affine line. Thus the result is not just an identity
for a polynomial given the name `hessianForm`. Mathematically this is the
quadratic-form Hessian bound \(\nabla^2F\succeq4096I\). The Lean
file also proves the `ConvexOn` consequence. It does not package the
quantitative consequence into a named `StrongConvexOn` predicate or
identify a matrix of second partial derivatives. The stronger
constant \(4124\), coefficient-size bound, and literature comparison
retain their separate mathematical proofs, exact computation, and review.

No project-wide build, CI inspection, or separate kernel replay was run.
The standalone file is not imported into the canonical project aggregate.
The independent
[correspondence review](convex-quartic-lean-correspondence-review.md)
found that the zero-set definitions and statements match the mathematical
note and independently matched the original source fingerprint. An addendum
reviews the later derivative, SOS, and convexity extension separately. Successful Lean
checking verifies the formal statements; this separate review checks their
connection to the mathematical claim.
