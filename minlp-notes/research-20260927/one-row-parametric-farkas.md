# Eliminating one parameter-dependent row of a linear system

Date: 2026-09-28. Status: supporting lemma; independently checked in the
[common-range fractional review](common-range-fractional-review.md).
No novelty claim is made. The main fractional theorem has a simpler proof
that retains one additional denominator direction; this lemma records
an alternative that preserves the original retained dimension.

Let \(C\) be a constant rational matrix, \(b(z,u)\) a vector of quadratic
polynomials, \(a(t)\) a vector affine in the scalar \(t\), and
\(\beta(z,u,t)\) a polynomial of degree at most two. Consider the system

\[
 C v\le b(z,u), \tag{4}
\]

\[
 a(t)^T v\le\beta(z,u,t). \tag{5}
\]

All its explicitly stored rational data have total length \(N\). The statement
below applies without convexity assumptions on the parameter variables.

## Exact elimination

We give an exact quantifier-free description of feasibility of (4)--(5)
at any real \((z,u,t)\). It has at most exponentially many atoms,
but every atom has degree at most three and individual coefficient
bit length \(N^{O(1)}\).

### Native Farkas rays

Let

\[
                      \Lambda_0=\{\lambda\ge0:C^T\lambda=0\}.
 \tag{6}
\]

Its extreme rays have supports of size at most
\(\operatorname{rank}C+1\). Choose rational ray generators by
minors and normalize each separately. All have polynomial-bit
coefficients. Farkas' lemma says that (4) is feasible exactly when

\[
                       r^Tb(z,u)\ge0
                       \quad\text{for every extreme ray }r.
 \tag{7}
\]

The cone lies in the nonnegative orthant, so it is pointed; there is
no additional lineality case. The zero cone contributes no conditions.

### A dual polyhedron with constant matrix

For fixed \(t\), define

\[
                   \Lambda_t=\{\lambda\ge0:C^T\lambda=-a(t)\}.
 \tag{8}
\]

This polyhedron is pointed. If it is nonempty, it has vertices and
is the sum of the convex hull of those vertices and its recession
cone \(\Lambda_0\).

Farkas' lemma for (4)--(5) asks that

\[
             \lambda^Tb(z,u)+\mu\beta(z,u,t)\ge0
 \tag{9}
\]

for every \(\lambda,\mu\ge0\) satisfying
\(C^T\lambda+\mu a(t)=0\). The case \(\mu=0\) is exactly
(7). If \(\mu>0\), divide by \(\mu\), obtaining a member of
\(\Lambda_t\). Under (7), every recession contribution in (9)
is nonnegative. Thus all these remaining inequalities are equivalent
to

\[
                    \lambda^Tb(z,u)+\beta(z,u,t)\ge0
                    \quad\text{for every vertex of }\Lambda_t.
 \tag{10}
\]

If \(\Lambda_t\) is empty, there are no positive-\(\mu\) Farkas
certificates, and (10) is vacuous. This includes an unbounded linear
objective in the eliminated fiber; no finite optimizer of that linear
program is being assumed.

### Vertex supports give affine formulas in the threshold

A vertex of \(\{\lambda\ge0:C^T\lambda=-a(t)\}\) has a support
\(I\) whose corresponding columns of \(C^T\), equivalently rows
of \(C\), are linearly independent. Conversely, a feasible vector
with such a support is a vertex. Enumerate every independent row set
\(I\). For each, fix a nonsingular coordinate minor of \(C_I^T\)
and solve those coordinates for \(\lambda_I(t)\), setting the
other coordinates to zero.

The inverse matrix is constant and rational. Consequently every
coordinate of \(\lambda_I(t)\) is affine in \(t\), with
polynomial-bit rational coefficients. Retain the guards

\[
                     \lambda_I(t)\ge0,\qquad
                     C^T\lambda_I(t)=-a(t).
 \tag{11}
\]

The second guard checks all nonpivot coordinates, so rank-deficient
matrices and threshold-specific compatibility are covered. A guard
can be true only at a single threshold; such cases are retained.
Zero coordinates cause no problem: the surviving support is still
independent. Include \(I=\varnothing\), with \(\lambda_I=0\)
and guard \(a(t)=0\). It supplies \(\beta\ge0\) when the
extra row has zero normal.

For every independent set \(I\), impose the implication

\[
 \bigl(\lambda_I(t)\ge0\ \wedge\ C^T\lambda_I(t)=-a(t)\bigr)
 \ \Longrightarrow\
                  \beta(z,u,t)+\lambda_I(t)^Tb(z,u)\ge0.
 \tag{12}
\]

Together, (7) and (12) are an exact description of the projection
of (4)--(5). The guards are affine in \(t\). The consequent has
degree at most three: an affine function of \(t\) multiplies a
quadratic function of \((z,u)\). All determinant denominators are
constant, so each implication can be cleared into polynomial atoms
without changing signs unexpectedly. The number of row subsets is at
most exponential in the input dimensions, while each determinant
and polynomial expansion has polynomial coefficient bit length.

This is stronger than a generic parameter-dependent elimination bound:
the degree does not grow with the number of eliminated linear
variables. It uses the fact that exactly one threshold row varies.
No claim is made that enumerating all the supports is efficient.

## Verification and role

The independent reviewer reconstructed the Farkas decomposition, guarded
vertex formulas, empty-dual case, zero-normal row, rank-deficient matrices,
and coefficient bounds. Exact rational calculations compared the formula
with independent Fourier--Motzkin feasibility in 600 systems of one or
two eliminated variables and one to four rows; all comparisons passed.
These calculations support the edge cases; Farkas' lemma and the proof
above establish the general statement.

The lemma uses standard linear programming duality and basic feasible
solutions. Its useful feature here is a degree bound independent of the
number of eliminated variables. It does not provide a polynomial-size
explicit projection. No project-wide verification or CI inspection was run.
