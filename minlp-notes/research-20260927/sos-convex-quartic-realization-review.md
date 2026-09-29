# Independent review of rational Hessian certificates

Date: 2026-09-28. Scope: the construction, quantitative bounds, and exact
rational certificate in
[sos-convex-quartic-realization.md](sos-convex-quartic-realization.md).
This reviewer independently checked the stronger certificate after
completing the separate
[general quartic review](general-strongly-convex-quartic-review.md).

The construction passes this review. The positive definite block Gram
matrix, its explicit spectral gap, the change back to rational
coordinates, and the rational coefficient projection are correct. The
certificate can be computed and written with polynomially many bits.
No mathematical defect was found.

## The block Gram identity

For a symmetric matrix $T$ and vector $b$, the Hessian of
$(b^{\mathsf T}u+u^{\mathsf T}Tu)^2$ has constant part
$2bb^{\mathsf T}$, linear part

\[
 4(b^{\mathsf T}u)T+4b(Tu)^{\mathsf T}+4(Tu)b^{\mathsf T},
\]

and quadratic part

\[
 8(Tu)(Tu)^{\mathsf T}+4(u^{\mathsf T}Tu)T.
\]

With coordinates $(u\otimes y)_{(k,j)}=u_ky_j$, the matrix

\[
 D(b,T)_{i,(k,j)}=2b_kT_{ij}+4b_iT_{kj}
\]

represents the linear part through the Gram cross term
$2y^{\mathsf T}D(b,T)(u\otimes y)$. The factors two and four are
necessary: the two appearances of an off-diagonal Gram block contribute
the outer factor two.

Likewise, the quadratic block

\[
 8\operatorname{vec}T\operatorname{vec}T^{\mathsf T}+4T\otimes T
\]

represents the quadratic part. Its first term evaluates to
$8(y^{\mathsf T}Tu)^2$ and its second to
$4(u^{\mathsf T}Tu)(y^{\mathsf T}Ty)$. The ordering of the vectorization
in the note agrees with the ordering of the tensor monomials.

The two tensors defining $D(b,T)$ have Frobenius norms
$2\|b\|\|T\|_F$ and $4\|b\|\|T\|_F$. Thus
$\|D(b,T)\|_2\leq6\sqrt n\|b\|\|T\|_2$, as claimed.

## Positivity and a computable gap

Use the note's constants and write $D_0=L+nV$. For the full Gram blocks,

\[
 C\succeq2\varepsilon\nu^2I,
 \quad Q\succeq(4m^2-4\varepsilon n)I\succeq2m^2I,
 \quad\|D\|\leq6\sqrt n\,\varepsilon D_0.
\]

The inequality $H\otimes H\succeq m^2I$ uses $H\succeq mI$.
For the potentially indefinite residual matrices, the valid bound is
$T_j\otimes T_j\succeq-\|T_j\|_2^2I$. The note retains this negative
contribution; it does not infer convexity from an arbitrary square.

The stricter choice
$\varepsilon\leq\nu^2m^2/(36nD_0^2)$ gives

\[
 C-DQ^{-1}D^{\mathsf T}
 \succeq\left(2\varepsilon\nu^2-
           \frac{18n\varepsilon^2D_0^2}{m^2}\right)I
 \succeq\tfrac32\varepsilon\nu^2I.
\]

Hence the full Gram matrix is positive definite, including directions
that are not tensor monomials of the form $(y,u\otimes y)$. This is
stronger than pointwise nonnegativity of the Hessian biform.

Let $q=2m^2$, $s=3\varepsilon\nu^2/2$, and
$B_D=6n\varepsilon D_0$. Completing the block square gives

\[
 (v,w)^{\mathsf T}M(v,w)
 \geq s\|v\|^2+q\|w+Q^{-1}D^{\mathsf T}v\|^2.
\]

If $A=Q^{-1}D^{\mathsf T}$, then

\[
 \|v\|^2+\|w\|^2
 \leq(2+2\|A\|^2)
       (\|v\|^2+\|w+Av\|^2).
\]

This proves the stated lower bound for $M$, with
$\|A\|\leq B_D/q$. The triangular matrix $S_a$ transforms
$(y,x\otimes y)$ into $(y,(x-a)\otimes y)$, with the sign shown in
the note, and $\|S_a^{-1}\|\leq2+K$. Its congruence therefore gives
exactly the positive rational lower bound $\mu$ displayed there.
All its factors, including reciprocals, have polynomial bit length.

## Exact rational projection and precision

The projection must impose an equation for every monomial that occurs as
a product of two entries of $(y,x\otimes y)$, including coefficients
that are zero in the Hessian biform. The note does this. Each ordered
matrix entry belongs to precisely one product monomial. The corresponding
symmetric zero-one matrices consequently have disjoint supports and are
Frobenius-orthogonal. Full matrix inner products automatically count
off-diagonal entries twice.

Thus the displayed affine projection is exact, fixes the algebraic Gram
matrix $M_x$, and contracts Frobenius error. Approximating $M_x$ within
$\mu/4$ before projection gives a rational matrix with lower eigenvalue
at least $3\mu/4$. The affine system is consistent because $M_x$ already
satisfies it; there is no need to solve a separate semidefinite feasibility
problem.

The required approximation precision is effective, not merely an appeal
to density. Each entry of $M_x$ is a univariate polynomial
$P_{ij}(\alpha)$ in the real root, with polynomial degree and rational
coefficient lengths. These polynomials can be formed explicitly in
polynomial time from the rational quadratics. If their degrees are at
most $D_1$ and their coefficient absolute sums at most $C_1$, then on
$[-R-1,R+1]$ their derivatives have magnitude at most

\[
 \Lambda=D_1C_1(R+1)^{D_1-1}.
\]

The binary length of $\max\{1,\Lambda\}$ is polynomial. For a Gram
matrix of dimension $N=n+n^2$, a certified rational root approximation
with error less than

\[
 \min\left\{1,
       \frac{\mu}{4N\max\{1,\Lambda\}}\right\}
\]

suffices when the rational matrix $T$ is obtained by exact evaluation at
that approximation. Entrywise error is less than $\mu/(4N)$, giving
Frobenius error less than $\mu/4$. No exact algebraic translation is
needed for the output.

Projection does not cause uncontrolled denominator growth. Each entry is
changed by only its own monomial's correction; that correction sums at
most $N^2$ rational entries and divides by an integer at most $N^2$.
Even clearing all denominators by their product gives a polynomial bit
bound. There are $O(N^2)$ entries and monomial equations, so both the
certificate size and exact construction time are polynomial.

## Rational square factors and scope

An exact rational $LDL^{\mathsf T}$ factorization of the positive
definite certificate has positive rational diagonal entries. Its factors
have polynomial bit length by determinant bounds on rational elimination.
These give a rational weighted SOS for the Hessian biform.

The note's conversion of positive rational weights to ordinary rational
squares is also constructive. For a weight $a/b>0$, expand the positive
integer $ab$ in binary. An even binary power $2^{2j}$ contributes
$(2^j/b)^2$; an odd power $2^{2j+1}$ contributes two copies of that
square. Thus $a/b$ uses at most twice the bit length of $ab$ rational
squares, all of polynomial encoding length. Integer factorization or
irrational Cholesky factors are unnecessary. Since every resulting
biform factor is linear in $y$, these factors also give a rational
polynomial matrix SOS representation of the Hessian.

The normalized quartic remains rational SOS and has exactly the prescribed
zero. Its stronger epsilon bound also satisfies the earlier ordinary
strong-convexity conditions, so the standard normalization gives Hessian
at least $3I/2$. For a rational target $a$, the separate univariate
quartic $(x-a)^2+(x-a)^4$ has positive definite rational Hessian Gram

\[
 \begin{pmatrix}2+12a^2&-12a\\-12a&12\end{pmatrix}
\]

on $(y,xy)$, with determinant $24$. This covers the rational case in
the final characterization. No decision-complexity or publication-priority
claim follows from the certificate construction.

## Targeted verification

An inline `python - <<'PY'` command using SymPy verified the full
block-Gram identity for a generic symmetric matrix and vector in two
variables, the algebraic affine shift, and the exact disjoint-support
coefficient projection. It also checked the rational-weight binary-square
formula for three positive rational weights. All checks passed.

An initial affine-shift check compared structurally different but equal
symbolic expressions. Expanding the difference corrected that checker;
the mathematical identity and the construction were unchanged. The
general positivity and complexity statements follow from the estimates
above, rather than from finite examples. A separate inline
`python - <<'PY'` document check passed for this review's local links,
display delimiters, final newline, whitespace, and control characters.
No project-wide verification or CI inspection was performed.
