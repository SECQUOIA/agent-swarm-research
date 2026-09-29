# Independent review of the general quantitative singleton construction

Date: 2026-09-28. Scope: polynomial coefficient lengths and deterministic
polynomial construction time for the companion construction in
[general-algebraic-singleton-realization.md](general-algebraic-singleton-realization.md).
This reviewer did not develop that construction. A separate subreviewer
checked the rational projection and its coefficient bounds.

The complete construction and comparison consequence pass this review.
One runtime wording issue identified during review was corrected: the
bound polynomial in primitive degree and height applies after input
normalization. Reading and normalizing an arbitrary rational scalar
multiple takes time polynomial in the original input length; that length
need not be bounded by the primitive height.

The discriminant supplies a
polynomial bit bound for the inverse real Vandermonde matrix. This controls
the precision needed to approximate the real template. Exact rational
projection, an explicit affine spectral gap, and a rational triangle then
complete the construction. The argument needs a certified polynomial-time
complex-root approximation algorithm; an ordinary numerical root routine
alone would not justify its running-time claim.

## Input and root bounds

The relevant input is an explicitly listed dense irreducible polynomial

\[
 P(t)=a_dt^d+\cdots+a_0\in\mathbb Z[t],\qquad
 |a_j|\leq2^H,
\]

of degree $d>1$ with exactly one real root $\alpha$. Rational input
coefficients can be cleared and their common integer content removed in
polynomial time. The resulting height $H$ is polynomially bounded by the
original input length. Irreducibility in characteristic zero gives distinct
roots. The number of nonreal conjugate pairs is $s=(d-1)/2$, so $d$ is odd
and at least three. Sparse or arithmetic-circuit polynomial encodings are
not covered by this input-length claim.

Set

\[
 R=2^{H+1},\qquad K=dR^{d-1},\qquad
 J=2^{s+H(d-1)}K^{d-1}.
\]

The Cauchy bound gives $|\beta|\leq R$ for every root. Let $V$ be the
complex Vandermonde matrix with columns $v(\beta)$, and let $W$ replace
each conjugate pair by the real and imaginary parts of its upper-half-plane
column, retaining $v(\alpha)$ first. The nonzero integer discriminant gives

\[
 |\det V|\geq |a_d|^{-(d-1)},\qquad
 |\det W|=2^{-s}|\det V|
       \geq2^{-s-H(d-1)}.
\]

Each entry of $W$ has magnitude at most $R^{d-1}$, so
$\|W\|_2\leq\|W\|_F\leq K$. Bounding all but the smallest singular
value by $K$ yields $\|W^{-1}\|_2\leq J$. These estimates apply to the
real basis; treating the complex Vandermonde and the real basis as having
the same determinant would miss the factor $2^{-s}$.

Writing $N=d(d-1)/2$, the same determinant argument gives the conservative
root-separation bound

\[
 |\beta-\gamma|\geq
 \sigma:=2^{-H(d-1)}(2R)^{-N}
 \quad(\beta\ne\gamma).
\]

Indeed, every other factor in the Vandermonde product is at most $2R$;
using exponent $N$ instead of $N-1$ weakens the valid bound. A nonreal root
therefore has imaginary part of magnitude at least $\sigma/2$. Root
approximations with absolute error at most $\sigma/16$ identify the unique
real root by the threshold $|\operatorname{Im}z|<\sigma/4$, and identify
the roots in the upper half-plane by their positive imaginary parts. No
exact test of a numerically computed imaginary part against zero is needed.

## Template approximation and rational projection

Let $D_0=\operatorname{diag}(0,1,\ldots,1)$ and
$B_*=W^{-\mathsf T}D_0W^{-1}$. For the real span $U$ of the nonreal
columns,

\[
 \|B_*\|_2\leq J^2,\qquad
 u^{\mathsf T}B_*u\geq K^{-2}\|u\|_2^2\quad(u\in U).
\]

The second inequality follows by writing $u=W(0,c)^{\mathsf T}$: its
quadratic value is $\|c\|_2^2$, while $\|u\|_2\leq K\|c\|_2$.
This does not require $U$ to be orthogonal to the real eigenvector.

Put $A=d^2(2R)^{d-1}$. Rational root approximations of absolute error
$\zeta\leq1$ yield a rational matrix $\widetilde W$ with

\[
 \|\widetilde W-W\|_F\leq A\zeta.
\]

This follows by factoring the difference of powers up to degree $d-1$.
If $A\zeta\leq1/(2J)$, the inverse perturbation formula gives

\[
 \|\widetilde W^{-1}\|_2\leq2J,\qquad
 \|\widetilde W^{-1}-W^{-1}\|_F
       \leq2J^2\|\widetilde W-W\|_F.
\]

Consequently, for the exactly computed rational template
$T=\widetilde W^{-\mathsf T}D_0\widetilde W^{-1}$,

\[
 \|T-B_*\|_F\leq6J^3A\zeta.
\]

The author's weaker bound with an extra factor $d$ is also valid. In
particular, choosing $\zeta\leq(128dJ^3AK^2)^{-1}$ gives error less
than $1/(16K^2)$, and also ensures the inverse perturbation hypothesis.
The integer and fractional precision involved is polynomial in $d,H$:
$\log J$, $\log A$, and $\log(1/\zeta)$ have polynomial bounds.

The exact projection has no hidden rank or denominator obstruction. Define
the symmetric remainder matrices $E_r$ by

\[
 (E_r)_{ij}=[t^r]\bigl(t^{i+j}\bmod(P/a_d)\bigr).
\]

Then $\mathcal L=\{B:\langle E_r,B\rangle_F=0\text{ for every }r\}$.
The matrices $E_r$ are independent because $(E_r)_{0j}=\delta_{rj}$ for
$0\leq j<d$. Their Gram matrix is therefore positive definite. Using the
full Frobenius inner product counts symmetric off-diagonal entries twice,
as required by $v(t)^{\mathsf T}Bv(t)$.

For an explicit denominator bound, put $D=|a_d|^{d-1}$ and
$L=(d-1)(H+1)$. All matrices $A_r=DE_r$ are integral and have entries
of magnitude at most $2^L$. To see this, let $R_j$ be the coefficient
vector of the remainder of $t^j$, and set $u_k=a_d^kR_{d-1+k}$. Starting
with $u_0=e_{d-1}$, polynomial reduction gives

\[
 (u_{k+1})_i=a_d(u_k)_{i-1}-a_i(u_k)_{d-1},
 \qquad (u_k)_{-1}=0.
\]

Thus $u_k$ is integral and has maximum norm at most $2^{k(H+1)}$;
multiplication by the remaining power of $a_d$ proves the bound on $A_r$.
This argument includes nonmonic polynomials.

Write $T=S_0/q$ with integral $S_0$, positive integer $q$, and
$q,|(S_0)_{ij}|\leq2^b$. Such a common representation with polynomial
$b$ follows from the adjugate formula for $\widetilde W^{-1}$. Let

\[
 G_{rs}=\langle A_r,A_s\rangle_F,
 \qquad h_r=\langle A_r,S_0\rangle_F.
\]

The projection is

\[
 B=P_{\mathcal L}(T)
   =T-\frac1q\sum_r A_r(G^{-1}h)_r.
\]

We have $|G_{rs}|\leq d^2 2^{2L}$ and $|h_r|\leq d^2 2^{L+b}$.
Cramer's rule bounds each projected entry using denominator $q\det G$
and numerator

\[
 (S_0)_{ij}\det G-
       \sum_r(A_r)_{ij}\det G^{(r)},
\]

where $G^{(r)}$ replaces column $r$ by $h$. Determinant bounds give
$O(b+d^2(H+1)+d\log(d+1))$ bits for both. Exact elimination computes
the projection in polynomial time. Numerical conditioning of the Gram
matrix is irrelevant to this exact rational calculation.

Orthogonal projection fixes $B_*$ and contracts Frobenius error. Hence

\[
 B|_U\succeq\frac1{2K^2}I_U,
 \qquad \|B\|_2\leq2J^2.
\]

Positivity is required on $U$; the construction correctly does not require
the rational matrix $B$ itself to be positive semidefinite.

The needed root subroutine is available in Mehlhorn, Sagraloff, and Wang,
[*From Approximate Factorization to Root Isolation with Application to
Cylindrical Algebraic Decomposition*, Theorem 5](https://arxiv.org/pdf/1301.4870),
PDF page 19. For integer coefficients bounded by $2^H$, it provides all
complex isolating disks and refinement below $2^{-N}$ in
$\widetilde O(d^3+d^2H+dN)$ bit operations. The proof explicitly handles
nonmonic input by normalizing the leading coefficient. The univariate
procedure in Section 2 uses certified approximation and deterministic
factorization; random choices belong to the later multivariate
application. Requesting a few extra bits permits dyadic rounding of disk
centers without exceeding the requested error. The precision above
therefore gives polynomial bit time for the required subroutine.

## Affine gap and triangle

Let $C$ be the companion matrix, and use $G_0=\{z:z_0=0\}$ for the
affine direction space. For $y=(C-\alpha I)z$, $z\in G_0$, the first
$d-1$ equations imply

\[
 z_j=\sum_{i<j}\alpha^{j-1-i}y_i,
 \qquad \|z\|_2\leq K\|y\|_2.
\]

Since $y\in U$, the aggregate matrix
$\mathcal R=(C-\alpha I)^{\mathsf T}B(C-\alpha I)$ satisfies

\[
 z^{\mathsf T}\mathcal Rz\geq
       \frac1{2K^4}\|z\|_2^2\quad(z\in G_0).
\]

This estimate uses only $|\alpha|\leq R$ and applies to negative real
roots as well. Put $M=dR$ and $S=2J^2(2M+1)$. Then
$\|C\|_2\leq M$ and $\|Q_1\|_2+\|Q_2\|_2\leq S$ for the
companion pencil. Take $e$ as the reciprocal of the smallest power of two
at least $16K^4S$. This gives both $e\leq1/(16K^4S)$ and polynomial
encoding length.

Also require $\zeta\leq e/(128R)$, and form
$c=(\widehat\alpha,\widehat\alpha^2)$ from the rational real-root
approximation. The error in each coordinate is less than $e/16$, because
$|\widehat\alpha^2-\alpha^2|\leq3R\zeta$. The three vertices

\[
 c+(-e,-e),\qquad c+(2e,-e),\qquad c+(-e,2e)
\]

contain $(\alpha,\alpha^2)$ in their interior. If
$\delta=(\alpha,\alpha^2)-c$, the weights are

\[
 \frac13-\frac{\delta_1+\delta_2}{3e},\qquad
 \frac{1+\delta_1/e}{3},\qquad
 \frac{1+\delta_2/e}{3}.
\]

They are all greater than $1/4$. Every vertex is within maximum distance
$3e$ of the target, so its affine pencil restriction differs from
$\mathcal R|_{G_0}$ by less than
$3eS\leq3/(16K^4)<1/(2K^4)$. All three affine Hessians are positive
definite. Matrix products and the three parameter substitutions preserve
polynomial coefficient length and take polynomial time.

## Comparison consequence and scope

The reduction for sums uses $k$ dense irreducible polynomials of the stated
type and a rational budget $t$. Apply the construction independently and
add the affine row $\sum_i x_{i,1}\leq t$. The product of the block
systems is their single product point, so the new system is feasible
exactly when $\sum_i\alpha_i\leq t$. Embedded block Hessians are
positive semidefinite, their span has dimension at most $3k$, and the
affine budget adds no Hessian direction. Rational summands, if allowed,
can first be subtracted from the budget.

This is a polynomial reduction of a precisely specified comparison
problem. It does not establish hardness for that comparison problem or
an FPT lower bound for native positive-semidefinite feasibility. The
singleton system has no strict feasible point, which is consistent with
the exact boundary behavior the reduction addresses.

## Targeted verification

An inline `python - <<'PY'` command using SymPy checked the nonbinomial
inputs $t^3+t^2+t-1$, $2t^3+2t-1$, and $3t^5+2t^3+2t-2$. It checked
irreducibility and the count of real roots, constructed rational template
matrices, applied the exact Gram projection, and checked all final
quadratic remainder identities. Exact rational leading principal minors
certified the positive definiteness of every affine Hessian. Certified
rational real-root intervals proved that each triangle contains the target
pair in its interior. All three examples passed, including both nonmonic
inputs.

Numerical complex-root approximations were used only to propose the
rational matrices in those finite checks. Their exact remainder,
positive-definiteness, and triangle checks are independent certificates
for these examples. They do not replace the general root-algorithm
complexity theorem required by the proof. No project-wide verification
or CI inspection was performed. A separate inline `python - <<'PY'`
document check passed for this review's local links, display delimiters,
final newline, whitespace, and control characters.
