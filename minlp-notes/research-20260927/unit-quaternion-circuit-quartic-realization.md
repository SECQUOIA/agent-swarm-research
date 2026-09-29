# Realizing rational unit-quaternion circuits by strongly convex quartics

Date: 2026-09-28. Status: passed
[independent adversarial review](unit-quaternion-circuit-quartic-independent-review.md).
This is a construction theorem; no
complexity lower bound for quaternion circuit signs is assumed.

## Statement

A circuit has \(s\ge1\) gates in topological order. Each gate is
an explicit rational unit quaternion, the product of two earlier gates,
or the inverse of an earlier gate. Gates may be reused and the two
parents of a product may coincide. Let \(p_i\in\mathbb Q^4\)
be the value of gate \(i\). The input lists generators and operations,
not the expanded fractions of all gate values.

**Theorem.** In deterministic polynomial time in that input, one can
construct a rational quartic \(F\) in \(N=4s\) real variables,
\(N+1\) rational quadratic square factors, and a full positive
definite rational Hessian Gram, all of polynomial total bit length,
such that
\[
 F\ge0,\qquad F^{-1}(0)=\{p\},\qquad
 p=(p_1,\ldots,p_s),\qquad
 \nabla^2F(X)\succeq\tfrac32 I\quad(X\in\mathbb R^N).
 \tag{1}
\]
In particular the unique minimizer is rational and belongs to
\([-1,1]^N\). Its expanded fraction encoding need not be short.
The input unit-norm conditions are checked by rational arithmetic.

The proof uses the previously reviewed
[quantitative quartic realization and Hessian certificate](sos-convex-quartic-realization.md).
The new work here is a quadratic exposing form for arbitrary shared
unit-quaternion circuits, with polynomial quantitative bounds.

## 1. Residuals and elementary norm identities

Identify a quaternion with its four real coordinates, use conjugation
\(q\mapsto\bar q\), and use the Euclidean norm. The usual
identities are
\[
 |ab|=|a||b|,\qquad a^{-1}=\bar a\quad(|a|=1),\qquad
 \langle c,ab\rangle=\langle a,c\bar b\rangle.
 \tag{2}
\]
Left and right multiplication by a unit quaternion are orthogonal real
linear maps.

Introduce a four-coordinate variable \(X_i\) for every gate.
Its vector residual is
\[
 r_i(X)=
 \begin{cases}
 X_i-c_i,&\text{constant gate},\\
 X_i-X_aX_b,&\text{product gate},\\
 X_i-\bar X_a,&\text{inverse gate}.
 \end{cases}
 \tag{3}
\]
These are \(N\) rational scalar polynomials of degree at most two.
Their common real zero is exactly \(p\), by induction over the
gates. Put \(q_i(X)=|X_i|^2-1\). All \(q_i\) also vanish
at \(p\).

At \(p\), the residual Jacobian \(J\) is block lower triangular
with identity diagonal blocks. Thus \(\det J=1\). Each scalar
residual gradient has norm at most three: a product has its own
coordinate derivative and at most two unit-norm parent rows; repeated
parents give a row of norm at most two on that parent. Each scalar
residual quadratic part has symmetric matrix norm at most one. For
distinct parents its two off-diagonal blocks are half a signed
permutation matrix. For a repeated parent the quaternion square has
components
\((w^2-x^2-y^2-z^2,2wx,2wy,2wz)\), whose quadratic matrices
also have norm one.

Consequently, with
\[
 V=4N,\qquad \nu=V^{-(N-1)},
 \tag{4}
\]
we have \(\|J\|_2\le\|J\|_F\le3\sqrt N\le V\),
and \(J^{\mathsf T}J\succeq\nu^2 I\). The latter follows
by bounding all other singular values by \(V\) and using their
product \(|\det J|=1\). These rational bounds have polynomial
bit length.

## 2. A positive quadratic form exposing the circuit point

Define the following quadratics with, for the moment, exact gate values
as coefficients:
\[
 E_i=q_i-2\langle p_i,r_i\rangle-
 \begin{cases}
 0,&\text{constant gate},\\
 q_a+q_b,&\text{product gate},\\
 q_a,&\text{inverse gate}.
 \end{cases}
 \tag{5}
\]
Every \(E_i\) has zero value and gradient at \(p\).
For a product gate this follows from the exact identity
\[
 E_i=|X_i-p_i|^2-|X_a-p_i\bar X_b|^2.
 \tag{6}
\]
Indeed \(p_i=p_ap_b\), so \(p_a=p_i\bar p_b\).
Writing \(U=X-p\), the centered expression is
\[
 E_i(p+U)=|U_i|^2-|U_a-p_i\bar U_b|^2.
 \tag{7}
\]
The second term is negative semidefinite and bounded below by
\(-2(|U_a|^2+|U_b|^2)\). When \(a=b\), this is
\(-4|U_a|^2\); (6)--(7) still hold exactly.

For an inverse gate the centered expression is
\(|U_i|^2-|U_a|^2\), and for a constant gate it is
\(|U_i|^2\). Thus no exposing form couples its current gate
quadratically to an earlier gate.

Set
\[
 \omega_i=16^{-(i-1)},\quad
 \omega_*=16^{-(s-1)},\quad E^*=\sum_{i=1}^s\omega_i E_i.
 \tag{8}
\]
Write \(E^*(p+U)=U^{\mathsf T}H_*U\). A fixed block
\(U_j\) receives its positive contribution \(\omega_j|U_j|^2\).
Each later gate contributes at worst \(-4\omega_i|U_j|^2\)
to the preceding lower bounds, and
\(\sum_{i>j}\omega_i\le\omega_j/15\). All remaining
contributions in (7) are nonpositive for the upper bound. Therefore
\[
 \frac{11}{15}\omega_* I\preceq H_*\preceq I.
 \tag{9}
\]
This is a matrix bound for arbitrary real directions, including all
shared-parent patterns.

## 3. Rounding coefficients without moving the zero

Replace only the four coordinates of each \(p_i\) multiplying
\(r_i\) in (5) by rational approximations with coordinate error
at most \(\eta\). Keep every residual and every \(q_i\)
exact. Call the resulting weighted form \(G\). It still has
\(G(p)=0\), because all these residuals vanish there.

In centered coordinates write
\[
 G(p+U)=\ell^{\mathsf T}U+U^{\mathsf T}HU.
 \tag{10}
\]
The scalar quadratic residual bounds from Section 1 give
\(\|H-H_*\|\le8s\eta\). The four-row residual Jacobian
at one gate has operator norm at most three. The norm of its coefficient
error is at most \(2\eta\), so
\(\|\ell\|\le12s\eta\). Using the coarser sum of \(s\)
weights in these estimates is sufficient.

For any prescribed \(0<\varepsilon\le1\), choose
\[
 \eta\le\min\{1,\omega_*/(32s),\varepsilon/(16s)\}.
 \tag{11}
\]
Equations (9)--(11) imply
\[
 \gamma I\preceq H\preceq2I,\qquad
 \|\ell\|\le\varepsilon,\qquad \gamma=\omega_*/4.
 \tag{12}
\]

The needed approximations can be computed without expanding gate
fractions. Round every coordinate to a dyadic grid of mesh \(h\).
If earlier quaternion norm errors are at most \(e\le1\),
multiplication gives error at most \(2e+e^2\le3e\), and
rounding adds at most \(2h\). Inversion is conjugation and obeys
the same bound. Constant gates have rounding error at most \(2h\).
Induction gives every error at most \(h(3^s-1)\). Choose a
dyadic \(h\le\eta/(2\cdot3^s)\). This validates the
assumption \(e\le1\) and gives coordinate error below \(\eta\).
The number of bits retained is polynomial in the circuit input and
\(\log(1/\eta)\).

## 4. Applying the quantitative realization theorem

Choose a positive dyadic square \(\varepsilon=t^2\) satisfying
\[
 \varepsilon\le\min\left\{1,\frac{\gamma^2}{2N},
       \frac{\nu^2\gamma^2}{36N(2+NV)^2}\right\},
 \tag{13}
\]
and construct \(G\) using (11). Define
\[
 F(X)=\left(\frac{G(X)}{t\nu}\right)^2+
                \sum_{i=1}^s\sum_{j=1}^4
                   \left(\frac{r_{ij}(X)}\nu\right)^2.
 \tag{14}
\]
The hypotheses of the reviewed realization theorem are now satisfied:
the residual quadratic matrices have norm at most one, their gradients
have norm at most \(V\), their Jacobian has smallest singular
value at least \(\nu\), and (12)--(13) give the exposing-form
and gradient-error bounds. That theorem proves the global curvature
bound in (1) and a full positive definite Hessian Gram.

Its rational certificate construction also applies here. The center
satisfies \(\|p\|\le\sqrt s\le N\), and is approximable
to any polynomially specified precision by Section 3. The centered
Gram has a lower bound with polynomial logarithmic encoding in
\(N,\gamma,V,\nu,\varepsilon\). Translation to the original
coordinates preserves such a bound. Approximate this Gram rationally
and project exactly onto the rational affine equations matching the
Hessian coefficients. The reviewed nonexpansive projection argument
preserves positive definiteness and supplies polynomial-size rational
output. It never asks for the expanded exact coordinates of \(p\).

Every rational constant in (4), (8), and (11)--(14) has polynomial bit
length. There are polynomially many monomials at fixed degree four.
Equation (14) supplies the \(N+1\) short rational square factors.
The residuals' unique zero proves the zero-set claim, completing the
construction.

## Scope and verification status

This theorem does not make arbitrary bounded arithmetic circuits
realizable. The unit-norm multiplication identity (6) is essential
to the proof. It permits reused inputs and inversion, and needs no
distinctness or algebraic independence of gate values.

The [initial literature comparison](quaternion-circuit-posslp-prior.md)
records classical matrix-circuit simulations and near-identity group
commutators. No publication-priority claim is made for this realization.
Its relevance to exact optimization hardness depends on a separate
sign reduction, which is not proved in this note. The already reviewed
circle construction establishes a special rational-output obstruction.

The root derived the matrix bounds directly and checked the interface
to the full-Hessian realization theorem. The independent reviewer
reconstructed the complete argument, including arbitrary shared
parents, rounding, and the rational Gram construction. No substantive
correction was required. The compiler author separately read the
realization proof and found no defect.

The independent reviewer wrote and ran
\(\texttt{python research-20260927/check_quaternion_realization_independent.py}\).
Exact symbolic identities and an eight-gate rational circuit passed,
including repeated parents, an inverse, the weighted positive margin,
and the zero and error bounds after rounding. The root read the review
and checked its analytical estimates without repeating the finite run.
These checks do not establish novelty or replace the general proof.
No Lean formalization, project-wide verification, or CI check was run.
