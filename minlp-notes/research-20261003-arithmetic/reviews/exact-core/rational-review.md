# Independent audit of rational-optimizer coordinate hardness

Date: 2026-10-03.

**Finding:** the rational-optimizer PosSLP lower bound is supported by the
proofs inspected. I found no substantive error. This is a fresh reconstruction
of the compiler, quartic realization, and their composition; I did not use the
earlier reviews as evidence. The result concerns exact coordinate comparison,
not exact comparison of a perturbed minimum under a rational-optimizer promise.

## Scope

I inspected these notes:

- [Coordinate comparison theorem](../../../research-20260927/rational-optimizer-posslp-coordinate-comparison.md).
- [Quaternion sign compiler](../../../research-20260927/quaternion-circuit-posslp-reduction.md).
- [Quaternion quartic realization](../../../research-20260927/unit-quaternion-circuit-quartic-realization.md).
- [Quantitative full Hessian Gram construction](../../../research-20260927/sos-convex-quartic-realization.md).

The general PosSLP upper reduction is a separate dependency. This audit checks
that the supplied full positive definite Gram satisfies its stated curvature
interface; it does not independently reprove the separation and Newton
arguments used for the upper reduction. Publication priority is outside this
audit.

## Quaternion compiler

The conjugations and projection have the stated orientation. In particular,
the rotation sends the third imaginary axis to the first, so the commutator
of first-axis and rotated first-axis signals has a **positive** leading first
coordinate after rotation. There is no hidden sign reversal in the product
simulation.

The identity

\[
 [q,r]-1=2(0,v\times u)\bar q\bar r
\]

is exact. Multiplicativity of quaternion norm yields both the commutator
bound and its cubic remainder bound. The projection formula follows by
expanding multiplication and using unit norm. The bound on its vector error
is valid when the scalar part is nonnegative and the vector norm is at most
one half, as required in every use.

For the small-signal generator, the transverse hypothesis gives
\(2|yz|\le4096x^4\). Combining this with the commutator remainder gives
the displayed \(65x^3\) error. The resulting interval
\(x^2\le x'\le6x^2\), positive scalar part, and preserved transverse
bound hold together; the proof does not assume away a potential sign change.
Two additional useful facts are that the input constant has
\(0<x_0<2^{-19}\), and \(6x_0<2^{-16}\).

I independently bounded all four signal operations. Their error constants
can be taken to be, respectively,

\[
 B,\qquad 18B^2,\qquad144B^3,\qquad396B^4.
\]

Each fits inside the claimed update \(2^{20}B^4\). The scalar parts
of intermediate products and commutators remain positive under
\(B\delta\le2^{-30}\), so these estimates do not invoke the projection
outside its domain. The multiplication remainder has order at least
\(a+b+1\), including when one leading coefficient is zero.

The homogeneous numerator/denominator representation is essential. It
keeps the two inputs to an addition at the same formal order, and gives the
same positive coefficient factor, eight, to numerator and denominator.
For multiplication that factor is four. Thus the final numerator coefficient
is an integer of the form \(DW\), with \(D>0\) and \(W=2V-1\ne0\).
No lower bound on a nonzero rational numerator has been silently assumed:
the leading coefficient is an actual nonzero integer.

The closed form

\[
 \log_2 B_T=(41\cdot4^T-20)/3
\]

and the choice of \(2T+2\) generator iterations give
\(B_T\delta<1/2\), with the much stronger stated margin. Hence the
final coordinate is nonzero and has the sign of \(W\), even after exact
cancellation at earlier gates.

All sizes are sizes of shared directed acyclic circuits. Neither
\(B_T\), nor the formal orders, nor the extremely small rational
\(\delta\) must be expanded to build the output circuit. The number
of raw quaternion gates is linear in the number of compiler macro calls
and generator iterations. The upper reduction for quaternion-coordinate
signs also respects this representation: common positive denominators and
four integer numerator circuits suffice at each gate.

## Quartic realization

The residual Jacobian is block lower triangular with identity diagonal,
including a multiplication gate whose two parents coincide. Its determinant
is one. The bounds on scalar residual gradients and quadratic matrices hold
for both distinct parents and a repeated parent. The determinant and operator
norm bounds therefore supply the stated rational lower singular-value bound
\(\nu=(4N)^{-(N-1)}\).

The exposing identity deserves special attention because quaternion
multiplication is not commutative. With the factors in the order used in
the note, it is correct:

\[
 E_i=|X_i-p_i|^2-|X_a-p_i\bar X_b|^2.
\]

The equality \(p_i\bar p_b=p_a\) uses unit norm. Translation then
gives the stated centered quadratic identity. This remains valid for
\(a=b\); in that case the negative term is bounded by \(4|U_a|^2\).
For any sharing pattern, a fixed parent can lose at most
\(4\sum_{i>j}\omega_i\le4\omega_j/15\). Consequently

\[
 (11/15)\omega_* I\preceq H_*\preceq I
\]

holds as a matrix inequality in all directions, rather than only along
solutions of the circuit equations.

Rounding the coefficients multiplying the residuals leaves the exact point
in the zero set. This is different from rounding the residual equations
themselves. The estimates
\(\|H-H_*\|\le8s\eta\) and \(\|\ell\|\le12s\eta\)
follow from the scalar quadratic norm bounds and the block residual
Jacobian norm bound of three. The chosen tolerances imply
\(H\succeq\omega_*I/4\), \(H\preceq2I\), and the required
gradient bound.

The forward rounding algorithm does not expand gate fractions. If previous
absolute Euclidean approximation errors are at most \(e\le1\),
unit norm of the exact inputs gives the multiplication error
\(2e+e^2\le3e\). Coordinate rounding adds at most \(2h\).
Thus \(e_i\le h(3^i-1)\), and the specified mesh requires only
\(O(s+\log(1/\eta))\) bits, in addition to input coefficient bits.
Here “norm errors” in the source should be read as norms of the vector
approximation errors, not merely errors in the norms of the vectors.

## Full Gram certificate and curvature

The dependency gives a certificate on the full vector
\((y,u\otimes y)\). I reconstructed the coefficient identity, including
the cross block

\[
 D(b,T)_{i,(k,j)}=2b_kT_{ij}+4b_iT_{kj}
\]

and the lower block
\(8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
+4T\otimes T\). The latter need not be positive semidefinite for an
individual indefinite residual matrix. The proof retains its negative
contribution and dominates it using the positive exposing matrix.

The stated choice of \(\varepsilon\) gives
\(Q\succeq2\gamma^2I\) and

\[
 C-DQ^{-1}D^{\mathsf T}
 \succeq(3/2)\varepsilon\nu^2I.
\]

This proves positive definiteness of the **entire** Gram, not just
positivity of its biform on rank-one tensor vectors. Completing the block
square also directly gives
\(y^{\mathsf T}\nabla^2F_0y\ge(3/2)\varepsilon\nu^2\|y\|^2\).
After scaling, the advertised \((3/2)I\) Hessian bound follows without
requiring a comparable lower bound on the entire scaled Gram.

The translation by the unknown exact optimizer only appears in the
certificate construction, where the optimizer is efficiently approximable.
The quantitative lower Gram bound loses a polynomially describable factor
depending on \(\|p\|\le\sqrt{s}\). All bounds still have polynomial
logarithmic size.

The rational affine projection is valid: different coefficient equations
have disjoint supports among ordered Gram entries. Consequently their
constraint matrices are Frobenius-orthogonal, the displayed projection
is exact, and it is nonexpansive. Approximating the real Gram more accurately
than its quantitative margin preserves positive definiteness after this
projection. The needed precision is polynomial, and this step never calls
an exact semidefinite feasibility oracle.

## Composition and representation promises

The unique common zero of the residuals is precisely the original list of
gate values. The additional quadratic square does not move that zero.
The sum of squares therefore has minimum zero, its sole minimizer is this
gate list, and no change of coordinates affects the selected output sign.
Every coordinate is rational and lies in \([-1,1]\).

The polynomial, the \(N+1\) quadratic factors, and the rational full
Hessian Gram have polynomial total encoding length. The optimizer fractions
need not: their expansion is neither an input to nor an output of the
reduction. The existence of the short generating circuit is sufficient for
the construction.

The optional normalization of the full Gram is also effective. For Gram
dimension \(m=N+N^2\), the rational number
\(\rho=\det H/(\operatorname{tr}H)^{m-1}\) is positive and is a
valid lower eigenvalue bound. Its encoding has polynomial length.
Multiplication of the objective by a sufficiently large integer square
preserves rational square factors and has polynomial encoding length.

The rational-optimizer promise is used only as a restriction of the
constructed instances. The proof gives no recognition algorithm for that
promise. It does not imply NP-hardness, a separation from P, or a
rational-optimizer promise for a later objective perturbation. These scope
distinctions in the source theorem are correct and should be retained in
the paper.

## Targeted verification

I wrote and ran the independent exact diagnostic
[check_rational_lower.py](check_rational_lower.py):

```text
python research-20261003-arithmetic/reviews/exact-core/check_rational_lower.py
```

It passed two generator steps with exact rational arithmetic; 36 signed,
zero-leading-coefficient, and cancellation cases for the signal operations;
symbolic exposing identities for a four-gate circuit with a repeated parent,
an inverse, and reused gates; the Jacobian determinant; the weighted matrix
margin; exact zero preservation after coefficient rounding; a full Hessian
Gram identity and Schur margin; and exact rational coefficient projection.

Those finite checks support the identities and do not replace the uniform
inequalities or polynomial encoding arguments above. No project-wide checks
or CI inspection were performed.
