# Spectral upper specialization review

Reviewed `SpectralUpper.lean` against the signed-square representation and the
actual linear-system constructors. The reviewer authored the generic assembly
but did not author the spectral specialization. The generic assembly receives
a separate review in `upper-construction.md`.

The graph theorem uses exactly the nonzero eigenvalue index set, whose cardinality
is the matrix rank. The epigraph counts the negative normalized coefficients;
the explicit equivalence in `Spectral.lean` identifies these with the negative
eigenvalues. The hypograph applies output reflection to the negated signed-square
sum and counts positive eigenvalues of the original matrix. Its error weight is
unchanged because absolute values remove the coefficient negation.

The decomposition is for the actual polynomial `xᵀHx/2 + aᵀx + b`. The original
box constraints are included in the finite system. Normalized coordinates are
proved to lie in the unit interval from those constraints; they are not an
additional assumption. The radius is positive even when a box coordinate is
fixed. Rank zero yields an empty square family and an exact affine formulation.
Empty boxes are allowed by the upper statements, with their expected vacuous
containment.

The displayed graph and epigraph row bounds follow from the actual constructors,
not abstract convex carriers. Continuous-coordinate bounds follow from the
corresponding generic auxiliary counts. Output reflection preserves both kinds
of coordinates and the actual row count.

No mathematical or scope defect found. This was a source review; the author
reported the targeted `lake build --wfail Formal.QuadraticPrecision.SpectralUpper`
passed. Final recorded topic verification remains separate.

The final size wrappers were also reviewed. The epigraph has exactly
`2n + k_-(11+10L) + (r-k_-)(3L+3) + 2` rows and
`k_-(3+2L) + (r-k_-)(L+1)` real auxiliary coordinates. The hypograph
replaces `k_-` by `k_+`. The subtype split in `count_sum_ite` partitions the
nonzero eigenvalue family; the complement count is therefore `r-k`, not
`n-k`. All counts include component outputs and the original box as stated.
The reflected hypograph uses the same stored coordinates and row count.
No issue found in the added wrappers.
