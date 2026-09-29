# Quartic realization with the minimum number of power coordinates

Date: 2026-09-28. Status: quantitative proof independently reviewed.
The previously reviewed constructions remain unchanged.

The rational strongly convex quartic realization can use
$n=(d+1)/2$ coordinates instead of $d-1$, for an irreducible polynomial
of odd degree $d>1$ with exactly one real root. This number is optimal
when the prescribed zero is the truncated power point
$(\alpha,\ldots,\alpha^n)$. The lower bound does not concern arbitrary
other coordinate encodings of the same number field.

**Theorem.** Given a dense irreducible rational polynomial $p$ of degree
$d>1$ with exactly one real root $\alpha$, put $n=(d+1)/2$.
There is a deterministic polynomial-bit-time construction of a rational
quartic $F$ in $n$ variables such that

\[
 \nabla^2F(x)\succeq I,\qquad
 F^{-1}(0)=\{(\alpha,\ldots,\alpha^n)\}.
 \tag{1}
\]

The output includes an expression of $F$ as a sum of $n+1$ squares of
rational quadratics and a positive definite rational Hessian Gram matrix
on the basis $(y,x\otimes y)$. All outputs have polynomial bit length in
the original dense input. Among globally nonnegative rational quartics
with a unique zero equal to a truncated power point of $\alpha$, the
number $n$ cannot be smaller.

The new ingredient is a smaller positive semidefinite exposing matrix.
It comes from the nonnegative univariate polynomial $(T-\alpha)p(T)$,
rather than a companion-matrix sandwich. The subsequent perturbation
and sum-of-squares arguments are the already reviewed
[strongly convex quartic construction](general-strongly-convex-quartic-singleton.md)
and [rational Hessian certificate construction](sos-convex-quartic-realization.md).

## An exposing Gram matrix on fewer monomials

Normalize the input to a monic polynomial
$p=P/a_d$, where $P=\sum_{i=0}^d a_iT^i\in\mathbb Z[T]$ is primitive,
$a_d>0$, and $|a_i|\leq2^\tau$, with $\tau\geq1$.
Write $d=2s+1$ and $n=s+1$. Set

\[
 R=2^{\tau+1},\qquad
 \sigma=2^{-\tau(d-1)}(2R)^{-d(d-1)/2}.
 \tag{2}
\]

The coefficient root bound and the nonzero integer discriminant give
$|\beta|\leq R$ for every root and $|\beta-\beta'|>\sigma$ for
distinct roots. In particular each nonreal root has imaginary part of
absolute value greater than $\sigma/2$.

List the upper-half-plane roots as $\beta_j=u_j+iv_j$, for
$1\leq j\leq s$. Then

\[
 r(T):=\frac{p(T)}{T-\alpha}
   =\prod_{j=1}^s\bigl(T^2-2u_jT+|\beta_j|^2\bigr)>0
   \quad(T\in\mathbb R).
 \tag{3}
\]

For each factor use the positive definite Gram matrix

\[
 B_j=\begin{pmatrix}|\beta_j|^2&-u_j\\-u_j&1\end{pmatrix},
 \qquad
 b:=\frac{\sigma^2}{4(1+R^2)}.
\]

Its determinant is $v_j^2$, so

\[
 bI\preceq B_j,\qquad \|B_j\|_2\leq1+R^2.
 \tag{4}
\]

Let $v_k(T)=(1,T,\ldots,T^k)^{\mathsf T}$. Starting with
$G_0=[1]$, define recursively

\[
 G_j=S_j^{\mathsf T}(B_j\otimes G_{j-1})S_j,
 \qquad
 S_jv_j(T)=\begin{pmatrix}v_{j-1}(T)\\T v_{j-1}(T)\end{pmatrix}.
 \tag{5}
\]

The matrix $S_j$ has zero-one entries. Its column Gram matrix is diagonal
with endpoint entries one and interior entries two. Thus
$I\preceq S_j^{\mathsf T}S_j\preceq2I$, including the case $j=1$.
Equations (3)--(5) prove

\[
 v_s(T)^{\mathsf T}G_sv_s(T)=r(T),\qquad
 b^sI\preceq G_s,\qquad
 \|G_s\|_2\leq U:=[2(1+R^2)]^s.
 \tag{6}
\]

Define the $n\times(n+1)$ matrix $D_\alpha$ by

\[
 (D_\alpha z)_k=z_{k+1}-\alpha z_k\quad(0\leq k<n),
 \qquad Q_*=D_\alpha^{\mathsf T}G_sD_\alpha.
\]

Then $D_\alpha v_n(T)=(T-\alpha)v_s(T)$, so

\[
 v_n(T)^{\mathsf T}Q_*v_n(T)=(T-\alpha)p(T).
 \tag{7}
\]

In particular $Q_*\succeq0$ has kernel exactly
$\mathbb Rv_n(\alpha)$. Its affine quadratic block, corresponding to
vectors $z=(0,y)$, is positive definite. Indeed the inverse of
$y\mapsto D_\alpha(0,y)$ is triangular, with entries powers of
$\alpha$, and has operator norm at most $nR^{n-1}$. Hence

\[
 y^{\mathsf T}(Q_*)_{1:n,1:n}y\geq\gamma\|y\|_2^2,
 \qquad
 \gamma:=\frac{b^s}{n^2R^{2n-2}}>0,
 \qquad
 \|Q_*\|_2\leq W:=(R+1)^2U.
 \tag{8}
\]

Every bound and reciprocal in (2)--(8) has polynomial bit length.

## Rational approximation preserving every algebraic zero

Consider the rational linear space

\[
 \mathcal L=\{Q\in\mathbb S^{n+1}:\quad
          v_n(T)^{\mathsf T}Qv_n(T)\equiv0\pmod p\}.
 \tag{9}
\]

Equation (7) places $Q_*$ in $\mathcal L$. For $0\leq k<d$, define
$E_k$ from the coefficient of $T^k$ in the remainder of $T^{i+j}$
modulo $p$, at matrix position $(i,j)$. Then $\mathcal L$ is the
common kernel of the Frobenius linear forms $\langle E_k,Q\rangle_F$.
These forms are independent: for every $0\leq k<d$, some pair
$0\leq i,j\leq n$ has $i+j=k$, and at that entry the remainder
coefficient vector is the $k$th unit vector.

Consequently the rational matrix
$\Gamma_{k\ell}=\langle E_k,E_\ell\rangle_F$ is invertible, and

\[
 \Pi(T)=T-\sum_{k,\ell}E_k(\Gamma^{-1})_{k\ell}
                         \langle E_\ell,T\rangle_F
 \tag{10}
\]

is the exact Frobenius-orthogonal projection onto $\mathcal L$.
It is nonexpansive and fixes $Q_*$. The remainders involve powers only
through $2n=d+1$. All entries in (10) therefore have polynomial bit
length and can be computed by exact rational linear algebra in
polynomial time.

Here are explicit error bounds for approximating $Q_*$ before projection.
Approximate every root within $\zeta\leq\min\{1,\sigma/16\}$,
identify the real root and upper-half-plane roots by their separated
imaginary parts, and replace the approximate real root by its real part.
Use rational real and imaginary parts to form rational matrices $\widetilde B_j$,
$\widetilde G_j$, and $\widetilde D$ by (5) and the same formulas.
Put

\[
 \widetilde B=1+(R+1)^2,\quad
 V_G=(2\widetilde B)^s,\quad
 C_B=2R+3,\quad
 C_Q=V_G C_B[1+s(R+2)^2].
 \tag{11}
\]

The factor error satisfies
$\|\widetilde B_j-B_j\|_2\leq C_B\zeta$.
Recursion (5), with $\|S_j\|_2^2\leq2$, gives

\[
 \|\widetilde G_s-G_s\|_2
 \leq2sC_B\zeta(2\widetilde B)^{s-1}
 \leq sC_B\zeta V_G.
\]

Also $\|\widetilde D-D_\alpha\|_2\leq\zeta$,
$\|\widetilde D\|_2\leq R+2$. Adding and subtracting
$\widetilde D^{\mathsf T}G_s\widetilde D$ therefore yields

\[
 \|\widetilde D^{\mathsf T}\widetilde G_s\widetilde D-Q_*\|_F
 \leq(n+1)C_Q\zeta.
 \tag{12}
\]

Let $a=(\alpha,\ldots,\alpha^n)$, and set
$K=(n+1)R^n$, so $\|v_n(\alpha)\|_2\leq K$.
For any positive rational $\varepsilon\leq1$, choose

\[
 \delta=\min\left\{1,\gamma/2,\frac\varepsilon{2K}\right\},
 \qquad
 \zeta\leq\min\left\{1,\sigma/16,
               \frac\delta{2(n+1)C_Q}\right\},
 \qquad
 Q=\Pi(\widetilde D^{\mathsf T}\widetilde G_s\widetilde D).
 \tag{13}
\]

Then $Q\in\mathcal L$ is rational and
$\|Q-Q_*\|_F\leq\delta/2$. The rational quadratic
$G(x)=(1,x)^{\mathsf T}Q(1,x)$ vanishes at $a$ exactly and has
translated form

\[
 G(a+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \qquad
 H\succeq mI,\quad\|H\|_2\leq L,\quad\|\ell\|_2\leq\varepsilon,
 \tag{14}
\]

where $m=\gamma/2$ and $L=W+1$ suffice. For the gradient bound use
$Q_*v_n(\alpha)=0$ and
$\|\ell\|_2\leq2\|Q-Q_*\|_2K$.

The precision in (13) is polynomial in $d,\tau$ and
$\log(1/\varepsilon)$. Certified complex root approximation has
polynomial bit complexity at this precision; the
[earlier effective construction](general-algebraic-singleton-realization.md)
records the precise primary algorithm used. Recursion (5) has polynomial
matrix sizes and polynomially many exact rational operations. No
exponentially large tensor product is formed.

## Enough quadratic equations in the shorter coordinate list

Write $p(T)=\sum_{k=0}^d c_kT^k$, with $c_d=1$.
Define $x_0=1$ and

\[
 \phi_k(x)=\begin{cases}
 x_k,&0\leq k\leq n,\\
 x_nx_{k-n},&n<k\leq d=2n-1.
 \end{cases}
\]

Let

\[
 R_j=x_1x_j-x_{j+1}\quad(1\leq j<n),
 \qquad R_n=\sum_{k=0}^d c_k\phi_k,
 \qquad
 \kappa=1+\sum_{k=n+1}^d|c_k|,
 \qquad r_j=R_j/\kappa.
 \tag{15}
\]

These rational quadratics vanish at $a$. Their common real zero is
exactly $a$, since the first equations impose the powers of $x_1$ and
the terminal equation becomes $p(x_1)=0$.
The same tangent-column argument as in the earlier quartic proof gives
the exact determinant

\[
 \det J=\frac{p'(\alpha)}{\kappa^n},
 \tag{16}
\]

where $J$ is the Jacobian of the scaled residuals $r_j$ at $a$.
Their translated quadratic parts $T_j$ satisfy $\|T_j\|_2\leq1$:
each product $x_nx_{k-n}$ has quadratic-part norm at most one,
and (15) accounts for the sum of its coefficient magnitudes.

A sufficient bound for $\|J\|_2$ and each gradient norm is
$V=4n(d+1)R^{n+1}$. Indeed each unscaled terminal gradient is a sum
of at most $d+1$ vectors of length at most $2R^n$, with coefficients
of magnitude at most $R$; the consistency rows satisfy a smaller bound.
Division by $\kappa\geq1$ does not increase them. By root separation,

\[
 J^{\mathsf T}J\succeq\nu^2I,
 \qquad
 \nu=\frac{\sigma^{d-1}}{\kappa^nV^{n-1}}>0.
 \tag{17}
\]

All constants and reciprocals still have polynomial bit length.

## Applying the verified quartic and Hessian-certificate lemmas

Choose a dyadic rational $t>0$ so that $\varepsilon=t^2$ satisfies

\[
 \varepsilon\leq\min\left\{1,\frac{m^2}{2n},
       \frac{\nu^2m^2}{36n(L+nV)^2}\right\}.
 \tag{18}
\]

Construct $G$ by (13), and output

\[
 F=\left(\frac{G}{t\nu}\right)^2+
                          \sum_{j=1}^n\left(\frac{r_j}{\nu}\right)^2.
 \tag{19}
\]

Equations (14), (15), and (17) are exactly the hypotheses of the
reviewed quartic perturbation estimates. They give
$\nabla^2F\succeq(3/2)I$. Equation (18) also meets the stronger
condition for a positive definite Hessian Gram matrix. The exact
rational projection of that Gram matrix, already proved in the
Hessian-certificate note, supplies the claimed rational certificate in
polynomial bit time. The quartic is nonnegative and vanishes at $a$;
strong convexity makes that zero unique. Its degree is four because
$H\succ0$ makes the leading part of $G^2$ nonzero.

The bit-complexity claim is in the original dense rational input.
Primitive normalization is polynomial time. All explicit powers and
precision exponents above have polynomial bit length, and all matrix
sizes are polynomial in $d$. The smallest singular-value bound (17),
the exposing gap (8), and (18) require only polynomially many precision
bits. Expanding (19) has at most $O(n^4)$ monomials. The SOS and Hessian
certificates likewise have polynomial size.

## Sharpness for the prescribed power point

Suppose a rational polynomial $F$ of degree at most four is globally
nonnegative and has exactly one zero, equal to
$(\alpha,\ldots,\alpha^q)$. Restrict it to the real moment curve:

\[
 h(T)=F(T,T^2,\ldots,T^q)\in\mathbb Q[T].
\]

This polynomial is nonnegative and is not identically zero, since
otherwise $F$ would vanish on the entire curve. It has a zero at
$\alpha$ of even multiplicity at least two. Since $p$ is the minimal
polynomial of $\alpha$, it follows that $p^2$ divides $h$. Therefore

\[
 2d\leq\deg h\leq4q,
 \qquad q\geq\lceil d/2\rceil=(d+1)/2.
 \tag{20}
\]

This lower bound does not assume convexity, SOS structure, or a
certificate representation. It establishes optimality only for the
specified consecutive-power coordinates. It leaves open whether a
different embedding of the same field can use fewer variables.

The positive univariate Gram construction and rational projection are
established kinds of arguments; no independent novelty claim is made
for those techniques. The proposed contribution is the combined
effective realization and sharp coordinate count in this prescribed
format. The [fresh independent quantitative review](dimension-optimal-quartic-adversarial-review.md)
found no mathematical defect. The root also reconstructed the complete
argument independently. A precise prior comparison remains necessary
before making any publication-priority claim. The earlier
$d-1$-variable theorem is retained as a separately verified construction.

## Targeted checks

An author-side inline `python - <<'PY'` command using SymPy checked the
recursive Gram identities for one, two, and three symbolic nonreal
quadratic factors; the exact $(T-\alpha)^2$ multiplication identity;
the residual Jacobian determinant with generic symbolic coefficients in
degrees three, five, and seven; and exact congruence projection for
$T^d+2T+2$ in those degrees. The same command checked local links,
display delimiters, whitespace, and final newline. All checks passed.
These finite symbolic cases check indexing and identities; they do not
establish the uniform spectral or bit bounds, which require the proof
and its independent review. No project-wide or CI check ran.
