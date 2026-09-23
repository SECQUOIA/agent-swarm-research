# Independent review: principal slices and determinant lower bounds

Date: 2026-09-20. Reviewer: lift/product implementation agent, independent of
these modules' authors. Reviewed `LowerPrincipal.lean` and
`LowerDeterminant.lean`, with source inspection of `PrincipalMinor`,
`LowerPullback`, `LowerContact`, `LowerVolume`, and the affine quadratic
identity in `LowerNegativeSlice`.

Verdict: **PASS** for R2, R3, the lower-bound portion of R6, and the
positive-rank exclusion of exact finite integer graph lifts. This review
does not cover the separate graph upper construction or its asymptotic
assembly.

## Actual principal slice

`graph_principal_pullback` starts with the original `HasGraphLift` and
constructs the translated coordinate slice `l + T*x`. Selected coordinates
range over `[0,u_i-l_i]`; every complementary coordinate remains at its
original lower endpoint. The domain proof checks both selected and
complementary coordinates, using non-strict box bounds for this restriction.
The original integer dimension is unchanged. Continuous auxiliaries and
integer indices remain unrestricted, and no closedness of the original
carrier is introduced.

The quadratic expansion computes the new affine coefficients and proves
that the actual restricted Hessian is `H.submatrix f f`. The coordinate
map `f : Fin d -> Fin n` is injective. Thus the domain is an actual
`d`-dimensional coordinate box, not an independently assumed quadratic
model. Symmetry is inherited from the original real Hermitian matrix.

`exists_principal_coordinate_rank` reindexes the proved nonzero principal
minor of cardinality `H.rank` by `Fin H.rank`. The determinant is preserved
by the same row and column equivalence. This supplies the rank-sized
injection used in `graph_rank_lower`, without an extra minor hypothesis
on that headline theorem. Rank zero is allowed in the existence theorem
through the empty principal minor; positive dimension is required before
any division by dimension or precision obstruction.

## Constant and power conversion

The volume bound used in `LowerDeterminant` is

`V <= 2^p * 2^d * (12 * sqrt(d) * eps)^(d/2) / sqrt(Delta)`.

Here `Delta = abs(det M) > 0`, and the factor 12 is the contact factor 3
times the midpoint tolerance factor 4. Rearranging gives exactly

`eps >= Delta^(1/d) * V^(2/d) / (48 * sqrt(d)) * 2^(-2p/d)`.

The coefficient in `determinantErrorConstant` matches this expression,
including the denominator 48. `determinant_volume_log_lower` proves the
logarithmic rearrangement using positive arguments throughout.
`error_lower_of_log_lower` converts back using real powers, with the
negative exponent and the real coercion of `p` in the correct places.
No natural-number subtraction truncates the exponential decay.

For the principal box, the measure is evaluated exactly as the product
of the selected original side lengths. Each length is positive under
the full-dimensional box hypothesis. No ambient `n`-dimensional volume,
extra Jacobian, or omitted coordinate width enters this `d`-dimensional
calculation. Consequently `principalErrorConstant` is the paper's stated
constant for every specified nonsingular principal minor, not merely
for one existentially selected minor.

The constant in `graph_rank_lower` is chosen before `eps` and `p`. The
conclusion therefore holds uniformly for every positive tolerance and
every admissible finite integer count, as required for an additive
logarithmic lower bound.

## Boundary cases and review correction

All determinant/log conversions require `d > 0` and a nonzero determinant.
Compactness makes the volume finite; positive volume makes its real value
strictly positive. The actual-lift wrapper first proves `eps > 0` from
`eps >= 0`: if `eps = 0`, the positive-dimensional contact-volume bound
forces the domain to have zero volume. In particular, no logarithm of
zero is used to exclude an exact lift.

The first reviewed principal wrapper assumed strictly positive tolerance.
I requested the missing zero-tolerance bridge. The final source now has
`graph_principal_error_pos`, permits `eps >= 0` in
`graph_principal_error_lower`, and proves
`no_exact_graph_of_positive_rank`. This closes the R3/R6 boundary case.
The formulas also permit `p = 0`. Negative tolerances are outside the
stated error model.

## Targeted verification

Both commands were run by this reviewer from `formal/`, with
`PATH="$HOME/.elan/bin:$PATH"` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.QuadraticPrecision.LowerDeterminant` — passed.
- `lake build --wfail Formal.QuadraticPrecision.LowerPrincipal` — passed.

A source scan of these two modules found no `sorry`, `admit`, or custom
`axiom` declarations. The final package's axiom audit and kernel replay
are separate checks; this review did not run project-wide verification
or inspect CI.

Reviewed source SHA-256 values:

- `LowerPrincipal.lean`: `b97148598eb68f3b00b632941336b318051ed253d812a09a07b0e5ad8436d384`
- `LowerDeterminant.lean`: `669a8924123dda76239a18fd74e74587e7e9330dea34385bffabc0201dbd0334`
