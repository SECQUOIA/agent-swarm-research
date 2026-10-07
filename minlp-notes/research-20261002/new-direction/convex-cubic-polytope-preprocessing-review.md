# Focused review of the convex cubic polytope preprocessing

Reviewed Sections 2 and 4 of
[convex-cubic-polytope-point-oracle.md](convex-cubic-polytope-point-oracle.md)
on 2026-10-02, together with their encoding and distance-conversion
dependencies and the completed affine branch in Section 3. No
unresolved issue was found in the affine-hull reduction, rational
interior ball, generalized Hoffman estimate, or polynomial-bit bounds.
The full theorem composition and weak-output repair have a separate
reviewer.

For an input inequality `C_i x<=b_i`, universal tightness is equivalent
to `min_(x in P) C_i x=b_i`, or maximum slack zero. Merely attaining
equality at some feasible point is insufficient. Exact rational linear
programming decides the required condition in polynomial bit time.

The universally tight rows define exactly the affine hull. Choose a
feasible strict-slack witness for each non-universally-tight row and
average the witnesses. Every non-universally-tight inequality is
strict at the average, because all witness slacks are nonnegative and
its own witness has positive slack. A sufficiently small relative
neighborhood in the space of universal equalities is therefore feasible.
This proves the affine-hull claim. If there are no non-universally-tight
rows, the feasible set is the affine solution space itself; boundedness
then forces dimension zero. Redundant universal rows need no
strict-slack witnesses.

Rational elimination yields a polynomial-bit particular solution and
basis. Taking the free original coordinates as reduced coordinates
puts an identity submatrix in `V`, makes the parametrization injective,
and shows directly that the reduced polytope is bounded. Its full
dimension follows from the affine-hull argument. Substitution into a
fixed-degree cubic preserves polynomial encoding length. Convexity
then implies positive semidefiniteness of the reduced Hessian; it need
not imply that of the original ambient Hessian.

The proposed radius LP has positive optimum because the reduced
polytope is full-dimensional. Its feasible center lies in the bounded
polytope, and `0<=rho<=1`, so the optimum is attained. Rational LP
provides a center and positive radius of polynomial binary length.
The inequality `||a_i||_2<=||a_i||_1` proves that the stated Euclidean
ball is contained in the polytope. Coordinate LPs and formula (4)
give a rational outer radius. In particular, `log(1/rho)` is
polynomially bounded, and `R` and the reflection factor `1+R/rho`
have polynomial encoding length. No margin is assumed at an optimizer.

The edge cases are covered: feasibility is checked first; zero
remaining dimension returns the unique point; transformed zero rows
with negative right-hand side are infeasible, and other zero rows can
be discarded. Under the stated boundedness promise, all coordinate
extrema are finite. If boundedness is to be checked instead, coordinate
LPs detect its failure; an unbounded slack LP can also be rejected
immediately. Unboundedness is outside this theorem's input class.

The general-polyhedron Hoffman estimate is correct. For the projection
onto a nonempty equality slice, its displacement is a sum of equality
row normals and nonnegative multiples of active inequality normals.
Conic elimination modulo the equality row space leaves at most `s`
independent integer rows. If the displacement is nonzero, their Gram
determinant is a positive integer, while their largest singular value
is at most `s C_*`. Hence their smallest singular value is at least
`(s C_*)^(-(s-1))`. Active inequality normals have nonpositive inner
products with the displacement because the original point is feasible.
The remaining equality terms give (10). The zero-displacement case is
immediate. Redundant rows, lower-dimensional slices, and irrational
right-hand sides cause no difficulty; boundedness and full dimension
are unnecessary for this lemma.

Clearing denominators of both equality and inequality normals makes
the stated integer constant applicable. The separate factor `D` in
the residual estimate is necessary and is present. All resulting
matrix heights, eigenvalue bounds, and powers in (11) have polynomial
binary length. The factor `W` in (12) bounds `||V||_2`, so reduced-space
distance bounds imply the original Euclidean distance guarantee.
No orthonormal basis or inverse singular-value estimate is needed.

The affine branch also supplies the promised constant. With integer
`A=D g_c'`, integer inequality normals `B`, and their common height
`C_*`, the same Hoffman lemma gives

```
dist_2(x,S) <= W (s C_*)^(s-1) D [f(x)-f*].
```

Thus `Gamma_P=max(1,W (s C_*)^(s-1)D)` proves the requested fourth-root
bound when the gap is at most one. A constant objective can use
`Gamma_P=1`; the zero-dimensional case is immediate. The saved
revision explicitly includes this affine constant and uses
non-universally-tight rows when selecting strict-slack witnesses.

Verification was analytic reading of the saved draft and independent
derivation of these statements. No tests, external searches,
project-wide verification, or CI inspection were performed.
