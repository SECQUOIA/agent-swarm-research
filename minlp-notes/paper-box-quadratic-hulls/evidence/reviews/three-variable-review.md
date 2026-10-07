# Independent review of the three-variable mathematics

Reviewed Sections 02–05 and Appendices A/B on 6 October 2026. This review
checked the mathematical arguments independently, rather than treating the
research notes as a correctness certificate. No archived optimization
experiment was rerun. Literature contracts were confirmed by the designated
GPT Luna literature agent against the primary full texts.

## Findings

No substantive mathematical error or missing hypothesis was found in the
reviewed results. In particular:

- The integral bound proves closedness of the Gram-image cone despite its
  higher-degree coefficient cancellations. The displayed order unit is the
  image of interior Gram blocks under a surjective linear map. Its presence
  in the quadratic subspace supplies the boundedness needed for closedness
  of restriction of the dual cone and the exact extension statement.
- The mass-zero part of the positive-loop cone is retained. The arguments
  transferring normalized inequalities to homogeneous dual cones correctly
  handle zero-mass functionals by adding an evaluation functional.
- The diagonal-cap decomposition has the correct sign. The corresponding
  hull equality is valid in arbitrary dimension: conditional Bernoulli
  rounding changes one diagonal moment and preserves every other recorded
  first or second moment. The disjoint certificate cone has the analogous
  rounding property and permits pure positive diagonal slack.
- The two-variable reduction is sufficient for the zero-square-coefficient
  statement and for the stronger assertion that rounding any one coordinate
  of a feasible three-variable disjoint moment point produces a true
  positive-loop moment point.
- The sign-product reduction is correct. Its use of the BNW result is
  confined to objective-value exactness; it does not infer exactness of the
  whole moment hull from that result.
- The contact reconstruction in the strict family region proves an exposed
  ray of the full nonnegative quadratic cone. The disjoint-certificate
  exclusion uses the support restriction explicitly and does not rely on a
  degree truncation.
- The homogeneous family LMI handles positive, zero, and negative mass.
  The order-four copositive decomposition permits its nonnegative matrix to
  have zero diagonal by moving that diagonal into the PSD summand. The
  separation problem has a rank-one optimum by complete positivity, while
  the text correctly avoids claiming that an SDP solver returns such a
  factorization.
- Appendix B reconstructs all coefficients in each stated boundary regime.
  Every denominator is positive under the hypotheses. The argument covers
  zero slope parameters and endpoint tangencies, including whole zero
  edges. Tangent derivatives are inherited by nonnegative summands because
  the corresponding one-sided derivatives have one sign and sum to zero.
- The integral compact-base argument makes the finite sum of closed cones
  closed. Its characterization of extreme rays by normalized family limits
  is sound. The six-orientation reduction and the equivalence of the capped
  and uncapped completeness questions are valid. Completeness remains
  explicitly unproved and is not needed for the established theorems.

## Exact arithmetic checks

A targeted Python/SymPy calculation reconstructed the 27 localizing
matrices directly from the twenty rational moments and expanded the general
family identity. It exited with status zero and gave:

| Check | Result |
|---|---|
| Localizing block counts by order 1, 2, 3, 4 | 8, 12, 6, 1 |
| Minimum leading determinant of order 1 | `1/10000` |
| Minimum leading determinant of order 2 | `307/50000000` |
| Minimum leading determinant of order 3 | `154171/40000000000` |
| Minimum leading determinant of order 4 | `45063248771/10000000000000000` |
| First SOC type | 24 cases; minimum slack `2831/4000000` |
| Second SOC type | 48 cases; minimum slack `124813/12500000` |
| Minimum diagonal/cross RHS factor | `22/625` |
| Separating objective | `Lambda(p) = -1/40` |
| Parametric validity identity | Exact symbolic equality |

This was a new proof-arithmetic check, not an optimization run. It used
the displayed formulas and rational data without an SDP solver. No
project-wide check or CI inspection was performed.

## External theorem contracts

The literature agent confirmed:

1. Anstreicher–Burer Theorem 6 describes the two-dimensional box moment hull
   by the augmented PSD moment matrix and the box-product RLT constraints,
   including the diagonal caps.
2. Burer–Natarajan–Willemsen Theorem 1 applies for at most three variables,
   arbitrary diagonal and linear coefficients, and nonpositive symmetric
   off-diagonal coefficients. Its relaxation uses the augmented PSD moment
   matrix and all ordered componentwise upper constraints
   `Y <= m 1^T`. The conclusion is equality of objective values.

Those are exactly the contracts used in Section 05.

## Actionable minor correction

Sections 03–04 initially used calligraphic names for the disjoint cones and
evaluation functional while Section 02 defined their noncalligraphic
versions. The parent has arranged consistent calligraphic notation across
the manuscript. This is an exposition correction and does not alter the
arguments.

## Follow-up: the affine-square branch

The following clarification was checked independently and accepted. If
`q = ell^2` and `q(v) > 0` at every cube vertex, then the ray of `q` is
extreme in the nonnegative quadratic cone exactly when `ell` takes both
signs on the cube vertices, or equivalently its zero plane meets the cube
interior. Positive square coefficients are not needed for this particular
equivalence.

If every vertex value of `ell` has the same sign, affine interpolation
makes its absolute value bounded away from zero throughout the cube. Thus
`q` is strictly positive, lies in the interior of the quadratic cone, and
does not generate an extreme ray. If `ell` changes sign, its zero plane
has a relatively open planar patch inside the cube. In a decomposition
`q = p + r` into nonnegative quadratics, both summands vanish on that
patch. Polynomial divisibility gives `p = ell ell_p` for an affine factor
`ell_p`. Nonnegativity on both sides of the plane, together with
continuity, forces `ell_p` to vanish on the planar patch; hence
`ell_p = alpha ell`. Evaluating away from the plane gives `alpha >= 0`.
The same argument applies to `r`, proving extremality. The strict
vertex-positivity hypothesis is essential to the stated one-sign
argument, because a one-sign affine function can otherwise vanish on a
boundary face.
