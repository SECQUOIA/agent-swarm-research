# Schur projection covers do not determine a rounding correction

Date: 2026-10-02. A short diagnostic for the open
[sparse negative-curvature target](negative-curvature-sparse.md).
This is an elementary convex example, not an algorithmic lower bound.

For `M>=0`, consider the positive definite energy matrix

\[
 P_M=\begin{pmatrix}M+1&-M\\-M&M+1\end{pmatrix}.
\]

Its eigenvalues are one and `2M+1`. Projection of an energy ellipsoid
onto either coordinate uses the Schur-complement coefficient

\[
 S_M=M+1-\frac{M^2}{M+1}=\frac{2M+1}{M+1}\in[1,2).
\]

Consequently each one-coordinate projection of
`{e:e'P_M e<=r^2}` has uniformly bounded radius in this projected
metric, independently of the large positive curvature.

Now round an interior point using unbiased errors of size `h` in each
coordinate. If the two signs are independent,

\[
 \mathbb E[e^TP_Me]=2(M+1)h^2.
\]

If they use the same random sign, `e=(h,h)` or `(-h,-h)`, then

\[
 \mathbb E[e^TP_Me]=2h^2.
\]

Both laws have identical coordinate marginals and zero mean. Choose
the point at `(1/2,1/2)` and `0<h<=1/2` to keep every outcome inside
the unit box. Thus even the coordinate feasibility and marginal
rounding laws agree; their correlations determine whether the error
depends on `M`.

This pinpoints the missing step in a separator-metric approach.
Small projected covers do not themselves supply a compatible joint
rounding law with a controlled convex-energy correction. The example
does not rule out correlated rounding, conditional convex elimination,
or finite-state algorithms using a richer representation. Indeed the
correlated law here solves the problem exactly, and the original
objective is convex with interaction width one.

The displayed calculations are direct two-by-two algebra. No numerical
experiment, external source search, project-wide check, or CI inspection
was used.
