# Independent review of one-variable rational singleton spectrahedra

Date: 2026-09-28. Reviewed
[the classification note](one-parameter-spectrahedral-fields.md).
Verdict: the classification, the sharp matrix-size bound \(2d\), and
the polynomial encoding claim are correct under the stated input and
output conventions. This review does not establish novelty.

## Singular pencils and the arithmetic necessity

The rational common kernel \(K=\ker A\cap\ker B\) can be removed
by rational congruence. Symmetry makes the cross blocks zero and ensures
that the orthogonal complement is invariant. The reduced pair has no
common kernel over \(\mathbb R\) or \(\mathbb C\), since the real
and imaginary parts of a complex common vector are real common vectors.

For a nonreal parameter \(z\), a kernel vector for the reduced pencil
would satisfy
\(v^*Cv+(z-\alpha)v^*\widehat Bv=0\), with both quadratic forms
real and \(C\succeq0\). Its imaginary part and positive
semidefiniteness force \(Cv=0\); the original vector equation then
forces \(\widehat Bv=\widehat Av=0\). This is a contradiction.
Thus the reduced determinant is nonzero, with no nonreal root. The
feasible matrix is singular because positive definiteness would persist
on an interval. Its determinant therefore vanishes at \(\alpha\),
proving that \(\alpha\) is algebraic and totally real.

This reasoning handles identically singular original pencils; it does
not assume that either original coefficient matrix is invertible. The
alternative principal-minor argument is also valid: a nonzero minor
polynomial cannot have a nonreal zero, because the same argument on that
principal subpencil would give a common kernel and make its determinant
identically zero.

## Sharp lower bound

If the reduced feasible matrix has nullity at least two, its adjugate is
zero, so the determinant derivative vanishes. If its nullity is one,
write the perturbation in kernel/complement blocks. A nonzero scalar
kernel derivative \(\beta\) would give a positive Schur complement
for sufficiently small \(t\) with \(t\beta>0\): the linear term
dominates the quadratic coupling term, while the complementary block
remains positive definite. That would give a second feasible parameter.
Hence \(\beta=0\) and the determinant derivative again vanishes.

Since the determinant has rational coefficients, \(D(\alpha)=D'(\alpha)=0\)
implies \(f^2\mid D\) for the separable minimal polynomial \(f\)
of \(\alpha\). Therefore the reduced size, and hence original size,
is at least \(2\deg f\). The scalar and rational cases are covered;
a one-by-one affine pencil cannot have a singleton feasible parameter.
The proof applies to combined block-diagonal LMIs but not to auxiliary
scalar variables or nonlinear pencils, exactly as stated.

## Construction and encoding

The trace matrix satisfies \(G=V^TV\succ0\) because the field is
totally real. With the column convention for the multiplication matrix,
\(VM=\operatorname{diag}(\alpha_j)V\). Consequently the proposed
\(L_r(x)\) is rational, affine and symmetric, and its congruent
diagonal entries are \((\alpha_j-x)/(\alpha_j-r)\).

The two rational poles can be chosen on opposite sides of the selected
root without crossing another conjugate. Their selected diagonal entries
force opposite inequalities \(x\le\alpha\) and \(x\ge\alpha\).
All other diagonal entries are positive at \(x=\alpha\). This proves
the singleton property and corank two at a matrix size of \(2d\).
The determinant formula remains valid for a nonmonic input polynomial:
the leading coefficient cancels in each ratio.

Polynomial encoding follows without an algebraic matrix square root.
The companion matrix has a common denominator of \(O(\tau)\) bits;
its first \(2d-2\) powers have coefficient and denominator lengths
polynomial in \(d,\tau\). The two inverses have common-denominator
Cramer representations of polynomial length in \(d,\tau,\ell\).
Multiplying by the trace matrix preserves polynomial bit lengths. The
conservative stated bound \(O(d^2(\tau+\ell+\log(d+1)))\) is sufficient.
Rational isolating endpoints must avoid roots, as the construction
explicitly requires; standard algebraic-number input conventions allow
such endpoints, and refinement is possible when needed.

## Independent exact checks

An inline `python - <<'PY'` command using SymPy independently formed
the multiplication matrix, trace Gram matrix, and two pencils for

\[
 3x-6,\qquad 2x^2-4,\qquad x^3-3x+1,
 \qquad x^4-10x^2+1.
\]

The chosen isolating intervals were respectively \((1,3)\), \((1,2)\),
\((0,1/2)\), and \((0,1)\). Exact checks verified all leading
principal minors of \(G\) positive, symmetry of each \(L_r\),
the determinant identity
\(\det L_r=\det(G)f(x)/f(r)\), exactly one root in each interval,
and total reality. All checks passed, including both nonmonic inputs.
These calculations test implementation conventions and examples; the
general classification and size bound rely on the proof above.

The prior comparisons remain appropriately qualified. The all-real
spectrum implication is classical PSD-pencil theory. Neither this
review nor the unsuccessful literature search establishes originality
of the arithmetic formulation or its sharp size bound.

Targeted Markdown checks of this review were run after writing it.
No project-wide verification or CI inspection was performed.
