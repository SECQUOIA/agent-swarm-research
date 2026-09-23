# Independent review: spectral normalization, slices, and boundary cases

Result: passed. Reviewed `Spectral.lean`, `SpectralSlice.lean`,
`SpectralConvex.lean`, `AffineBoundary.lean`, and `OutputReflection.lean`.
No proof-source changes were made during this review.

## Spectral representation and counts

The hypothesis is `H.IsHermitian` over the real numbers, hence actual symmetry
of the given Hessian. `spectral_quadratic` derives the square decomposition
from Mathlib's spectral theorem for this matrix. `spectral_rank` identifies
its actual matrix rank with the number of nonzero eigenvalues. There is no
assumed decomposition or independently supplied rank certificate.

The normalization uses the explicit enclosing radius
`1 + ∑ i, |v i| * max |l i| |u i|`. It is positive even for a zero functional,
a zero-dimensional input, or a degenerate box. The normalized coordinate is
proved to lie in `[0,1]` for every point in the original box. These bounds
are enclosing bounds, not exact extrema: the proof does not claim that the
normalized coordinate attains either endpoint. This distinction does not
affect the upper construction or the leading binary-count coefficient.

`normalizedLinear_square` retains the affine correction terms exactly.
`spectral_signed_decomposition_nonzero` therefore represents the actual
polynomial, including its arbitrary linear and constant terms, using exactly
`rank H` nonzero square coefficients. The positive radius multiplies each
eigenvalue by a strictly positive factor. Separate sign and zero equivalences
prove that no eigenvalue sign changes and no zero/nonzero direction is lost.
`spectral_negative_count`, `spectral_positive_count`, and
`rank_eq_inertia_sum` establish the corresponding exact counts.
`spectralAffineMap` and `spectralNormalizedMap` are actual affine maps,
not arbitrary functions with informal linearity claims.

## Negative slice

`negativeEmbedding` is built from the actual negative eigenvectors and is
injective. Applying the spectral coordinate map recovers every negative
parameter and gives zero in the other eigendirections.
`negativeEmbedding_quadratic` computes the restricted quadratic form.
`negativeEmbedding_coercive` chooses a strictly positive lower bound on the
finitely many negated negative eigenvalues and obtains the correct negative
quadratic bound. The empty negative family is covered and imposes no false
positive-dimensional conclusion.

`negativeEmbedding_small_box` constructs a positive parameter radius whose
translated image lies in the original closed box. Its strict hypotheses
`l i < u i` are explicit and are appropriate for the full-dimensional
lower bound. The translation is the box midpoint. No negative slice,
coercivity constant, or box inclusion is assumed. `negativeSliceMap` is an
actual affine map and remains injective after translation. These are slice
foundations; their composition with parity contacts and the precision lower
bound is handled by the separate lower-bound assembly.

## Affine and convex boundary cases

`AffineBoundary.lean` gives explicit finite row systems for all box bounds
and the graph/epigraph/hypograph residual. The graph equality uses two
inequalities. The counts are exactly `2*n+2` for graphs and `2*n+1` for
epigraphs or hypographs, with no auxiliary variables or integer coordinates.
The feasibility equivalences cover empty, degenerate, and zero-dimensional
boxes. Full unbounded output rays are retained for epigraphs and hypographs.

For a convex function, the exact epigraph is represented as a convex lift;
for a concave function the exact hypograph is represented similarly.
These declarations correctly make no finite-linearity claim.
`SpectralConvex.lean` proves convexity of the actual quadratic polynomial
from nonnegative eigenvalues and concavity from nonpositive eigenvalues,
with arbitrary affine terms and any convex domain. Zero negative inertia
therefore gives an exact zero-integer convex epigraph; zero positive inertia
gives an exact zero-integer convex hypograph. Positive-error finite linear
approximations require the separate folding/upper construction.

## Output reflection

`outputReflection` changes only the output sign. Its affine preimage keeps
the same integer dimension, continuous auxiliary dimension, and actual
inequality count. The relaxation equivalence and the two transfer theorems
preserve complete unbounded output rays and the same one-sided tolerance.
They do not replace epigraph containment by containment of graph points.

## Targeted verification

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.AffineBoundary Formal.QuadraticPrecision.Spectral Formal.QuadraticPrecision.SpectralSlice Formal.QuadraticPrecision.OutputReflection
lake build --wfail Formal.QuadraticPrecision.SpectralConvex Formal.QuadraticPrecision.SpectralSlice Formal.QuadraticPrecision.OutputReflection
lake env lean -DwarningAsError=true /tmp/topic20-spectral-review.lean
```

The targeted builds and temporary independent elaboration passed. The latter
checked zero-functional normalization, a zero-dimensional exact affine graph,
and infeasibility of an inverted box. It printed the axioms of 14 principal
spectral, slice, boundary, and reflection declarations; each used only
`propext`, `Classical.choice`, and `Quot.sound`.

This review did not run project-wide verification or inspect CI.
