# Good-multiplier classification review

Reviewer: cone-geometry agent. Date: 2026-09-22.

This independent review covers `GoodMatrix.lean`, `Inertia.lean`,
`GoodSpectral.lean`, `GoodConvex.lean`, `GoodBlock.lean`, and `Good.lean`, with
`Model.lean` and the reused spectral definitions read for context. The source
is Section 3 of `results/infinite-quadratic-aggregation-hhc.md`; the relevant
frozen obligations are I01 and I04–I06.

## Actual matrix and polynomial

The model uses the three polynomials
`u·u-1`, `v·v-1`, and `1/2-u·v`, with Euclidean dot products explicitly
expanded as finite sums. It does not substitute the function-space supremum
norm for Euclidean length.

`homogeneousMatrix` uses `none` for the homogenizing coordinate and separate
`inl`/`inr` coordinates for the two spatial vectors. The two diagonal blocks
have entries `w0` and `w1`; their matching off-diagonal entries are `-w2/2`.
The scalar block is `w2/2-w0-w1`, and every spatial/homogenizing cross-entry
is zero. Therefore its quadratic form has cross-term `-w2*u·v`, with exactly
the factor of two required by a symmetric matrix.

`homogeneousMatrix_quadratic` proves this expansion for every matrix-coordinate
vector, and `homogeneousMatrix_eq_homAggregate` identifies it with the actual
homogeneous aggregation in the original `(u,v,t)` variables. `GoodBlock`
defines the actual `2×2` matrix
`[[w0,-w2/2],[-w2/2,w1]]`, proves its quadratic formula, and expresses the
homogeneous form as the sum of `r` copies of this block and its one scalar
block. Grouping the spatial coordinates by pair gives precisely the source's
block decomposition. No hypothetical matrix or unproved spectral surrogate
replaces the original aggregate.

## Eigenvalues and multiplicity

`negativeInertia` is the cardinality of the indices of negative eigenvalues in
the Hermitian spectral decomposition. It is not the cardinality of the set of
distinct eigenvalue values. The reused `spectral_quadratic` theorem diagonalizes
the actual matrix using its unitary eigenvector basis. Mathlib's
`Matrix.IsHermitian.charpoly_eq` and `roots_charpoly_eq_eigenvalues` identify this
indexed list with the characteristic-polynomial roots, with multiplicity.

The new dimension arguments are sound. If every nonzero vector in a linear
parameterization is strictly negative, projection onto the negative spectral
coordinates is injective: a vector with zero negative coordinates would have
nonnegative quadratic value. Its domain dimension is therefore at most the
number of negative eigenvalues. Conversely, the genuine negative spectral
subspace has strictly negative quadratic value at every nonzero point. If a
form is nonnegative on a scalar functional's kernel, that functional is
injective on the negative spectral subspace, whose dimension is then at most
one. These arguments require no unproved inertia formula.

## Discriminant obstruction and boundary cases

Under nonnegative weights, failure of `w2²≤4*w0*w1` gives an explicit negative
direction for the `2×2` block. The case `w0=0` is handled separately, so the
proof does not divide by a possibly zero leading coefficient. Replicating
this direction independently in each spatial coordinate gives a negative
quadratic form equal to a strictly negative scalar times `sum_i y_i²`.
This is negative for every nonzero `y∈R^r`. The actual homogeneous matrix
therefore has at least `r` negative eigenvalues. The assumption `r≥2` is used
exactly when this contradicts the permitted count of at most one.

The explicit block theorem proves PSD if and only if the discriminant
condition holds, under nonnegative weights. Its sufficiency proof also
handles a zero leading diagonal: the discriminant then forces the off-diagonal
to vanish. Equality in the discriminant is allowed; no positive-definiteness
or invertibility assumption enters.

For every nonzero cone multiplier, `w0+w1>0`. Otherwise nonnegativity gives
`w0=w1=0`, and the discriminant forces `w2=0`. The inequality
`w2≤w0+w1` then gives
`w2/2-w0-w1≤-(w0+w1)/2<0`. This includes cone-boundary rays and coordinate
rays. The homogeneous form is nonnegative on `t=0`, so it has at most one
negative eigenvalue; the vector supported on `t` supplies a strictly negative
value, so it has exactly one. The zero multiplier is excluded precisely where
strict scalar negativity or nontrivial goodness requires it.

## Convexity, strict hull validity, and goodness

`Good` retains the source definition: nonzero nonnegative weights, at most one
negative eigenvalue of the actual homogeneous matrix, and strict negativity
of the aggregate on every point of the ordinary convex hull. It does not
define goodness to mean membership in the proposed cone.

The discriminant implies nonnegativity of the leading quadratic form.
`aggregate_jensen_gap` proves the exact Jensen gap, including cancellation of
the constant term when the combination coefficients sum to one. This yields
convexity of the aggregate on the full variable space. A nonzero nonnegative
aggregation is strictly negative on the strict feasible set. Its strict
sublevel set is convex, hence contains the ordinary convex hull. The proof
does not replace that hull by its closure, extend strict inequalities by
continuity, or assume a general good-aggregation hull theorem.

For `r≥2`, `good_iff_goodCone` proves both directions of the requested
classification. The forward direction derives the discriminant from the
spectral obstruction; the reverse direction supplies both the spectral bound
and actual strict hull validity. It has no HHC, supplied hull formula,
separation oracle, PSD assumption on the original system, or unproved
classification premise. Stronger auxiliary statements in dimensions zero or
one do not erase the necessary `r≥2` premise from this equivalence.

## Review status and checks

The semantic review found no mathematical defect. An initially missing
explicit `2×2` PSD equivalence and repeated-block interface was reported to
the author and supplied in `GoodBlock.lean`; the additions were reviewed.
The author reported warning-free targeted builds of `Good.lean` and
`GoodBlock.lean`; implementation is complete. No mathematical or frozen-scope
issue remains in the reviewed Lean files.

The goodness paragraph in paper section
`92-formal-infinite-aggregation.tex` was also compared with the code. Its
definition, matrix, multiplicity, classification, and hull-validity explanation
agree with the formal statements. The wording “outside the displayed cone”
was flagged for clarification: the lower inertia bound applies to nonnegative
weights violating the discriminant inequality; strict scalar negativity inside
the cone additionally requires a nonzero weight. The requested wording makes
these domains explicit.

No author-owned files were edited, no compilation was duplicated, and no
project-wide checks or CI inspection were performed. Root owns the final
package compilation, axiom audit, and kernel verification record.
