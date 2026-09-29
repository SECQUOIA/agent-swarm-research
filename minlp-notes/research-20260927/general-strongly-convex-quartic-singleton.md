# Strongly convex rational SOS quartics with prescribed algebraic zeros

Date: 2026-09-28. Status: construction independently reviewed.

**Theorem.** Let an irreducible $p\in\mathbb Q[T]$ of degree $d>1$ be
given by its dense coefficient list, and suppose that it has exactly one
real root $\alpha$. A deterministic polynomial-time algorithm constructs
a rational quartic $F$ in $d-1$ variables, together with an expression as
a sum of $d$ squares of rational quadratic polynomials, such that

\[
 \nabla^2F(x)\succeq I\quad\text{for every }x\in\mathbb R^{d-1},
 \qquad
 F^{-1}(0)=\{(\alpha,\alpha^2,\ldots,\alpha^{d-1})\}.
 \tag{1}
\]

The expanded quartic and its rational sum-of-squares representation both
have polynomial bit length. If the primitive integer normalization of
$p$ has coefficient bit length $\tau$, the construction after that
normalization takes time polynomial in $d+\tau$. Total time, including
normalization, is polynomial in the original rational input length.

For rational $\alpha$, the univariate polynomial
$(x-\alpha)^2+(x-\alpha)^4$ has the same properties. Thus every real
algebraic number with exactly one real conjugate occurs as a coordinate
of the unique zero of a globally strongly convex rational SOS quartic.
Here SOS means a sum of squares of polynomials whose coefficients are
themselves rational, without irrational square-root weights.

The construction uses the effective rational quadratic pencil from
[Polynomial-time singleton realization](general-algebraic-singleton-realization.md).
A rational member of that pencil vanishes at the desired point, has a
uniformly positive quadratic part, and can have an arbitrarily small
gradient there. Squaring it supplies positive curvature far from the
point. Small squares of additional vanishing quadratics supply positive
curvature near it. The estimates below account for their possible
negative curvature away from the point.

## Vanishing quadratics with an invertible Jacobian

Normalize the input to

\[
 P(T)=a_dT^d+\cdots+a_0\in\mathbb Z[T],\qquad
 a_d>0,\qquad |a_i|\leq2^\tau,\qquad\tau\geq1,
\]

and put $p=P/a_d=T^d+\sum_{i=0}^{d-1}c_iT^i$. Write
$n=d-1$ and $a=(\alpha,\ldots,\alpha^n)$. As in the effective
singleton construction, let

\[
 R=2^{\tau+1},\qquad K=dR^{d-1},\qquad
 \sigma=2^{-\tau(d-1)}(2R)^{-d(d-1)/2}.
 \tag{2}
\]

Every root has absolute value at most $R$, and distinct roots are at
distance greater than $\sigma$. These elementary bounds follow from
the coefficient root bound and the nonzero integer discriminant.

With the convention $x_0=1$, define $n$ rational quadratics by

\[
 \begin{aligned}
 r_j(x)&=x_1x_j-x_{j+1} &&(1\leq j<n),\\
 r_n(x)&=x_1x_n+\sum_{i=0}^{n}c_i x_i.
 \end{aligned}
 \tag{3}
\]

Every $r_j$ vanishes at $a$. In fact their common real zero set is
already $\{a\}$: the first $n-1$ equations force $x_j=x_1^j$, and the
last then becomes $p(x_1)=0$.

Let $J$ be their Jacobian at $a$, with rows $g_j^{\mathsf T}$, where
$g_j=\nabla r_j(a)$. Its determinant is

\[
 \det J=p'(\alpha)\ne0.
 \tag{4}
\]

One way to check the sign as well as the value is to replace the first
column basis vector by
$w=(1,2\alpha,\ldots,n\alpha^{n-1})^{\mathsf T}$. This change of
basis has determinant one. The first $n-1$ entries of $Jw$ are zero,
and the last is $p'(\alpha)$. The minor consisting of the first $n-1$
rows and the last $n-1$ columns is triangular with diagonal $-1$.
Expansion along the first column gives (4).

Every entry of $J$ has absolute value at most $3R^n$. Hence

\[
 \|J\|_2\leq\|J\|_F\leq3nR^n\leq V:=3K,
 \qquad \|g_j\|_2\leq V.
\]

Since $p$ is monic,
$|p'(\alpha)|=\prod_{\beta\ne\alpha}|\alpha-\beta|\geq\sigma^n$.
The product formula for singular values and (4) give the rational bound

\[
 \sigma_{\min}(J)\geq
 \nu:=\frac{\sigma^n}{V^{n-1}}>0,
 \qquad J^{\mathsf T}J\succeq\nu^2I.
 \tag{5}
\]

Both $\nu$ and $\nu^{-1}$ have polynomial bit length; a coarse bound on
$\log(1/\nu)$ is $O(d^3(\tau+\log d))$.

Translate by $a$ for the proof, without changing the rational coordinates
used in the output. Each residual has the exact expansion

\[
 r_j(a+y)=g_j^{\mathsf T}y+y^{\mathsf T}A_jy,
 \qquad \|A_j\|_2\leq1.
 \tag{6}
\]

Here $A_1=e_1e_1^{\mathsf T}$ for the square $x_1^2$; all other
quadratic parts are $(e_1e_j^{\mathsf T}+e_je_1^{\mathsf T})/2$.
The bound includes the terminal residual $r_n$.

## A rational vanishing quadratic with a small gradient

We record the quantitative information used from the earlier pencil.
It is constructed in polynomial time from $p$ and consists of rational
symmetric matrices $Q_0,Q_1,Q_2$ of size $d$. For
$z(x)=(1,x_1,\ldots,x_n)^{\mathsf T}$, write

\[
 G_{u,v}(x)=z(x)^{\mathsf T}(Q_0+uQ_1+vQ_2)z(x).
\]

For every real pair $(u,v)$, $G_{u,v}(a)=0$. At the special pair
$(\alpha,\alpha^2)$,

\[
 G_{\alpha,\alpha^2}(a+y)=y^{\mathsf T}H_*y,
 \qquad H_*\succeq\gamma I,
 \qquad\gamma=\frac1{2K^4}.
 \tag{7}
\]

Explicit bounds from that construction are obtained by setting

\[
 \begin{aligned}
 s&=(d-1)/2,&
 J_0&=2^{s+\tau(d-1)}K^{d-1},& M&=dR,\\
 S&=2J_0^2(2M+1),&
 L_*&=2J_0^2(M+R)^2.&
 \end{aligned}
\]

They satisfy

\[
 \|Q_1\|_2+\|Q_2\|_2\leq S,
 \qquad \|H_*\|_2\leq L_*.
 \tag{8}
\]

For the second inequality, the full matrix at $(\alpha,\alpha^2)$ is
$(C-\alpha I)^{\mathsf T}B(C-\alpha I)$, with
$\|C\|_2\leq M$ and $\|B\|_2\leq2J_0^2$.

Suppose that rational $u,v$ satisfy
$\max\{|u-\alpha|,|v-\alpha^2|\}\leq\delta$. The rational quadratic
$G=G_{u,v}$ still vanishes at $a$, and its exact translated expansion is

\[
 G(a+y)=\eta^{\mathsf T}y+y^{\mathsf T}Hy.
\]

By (8) and $\|z(a)\|_2\leq K$,

\[
 \|H-H_*\|_2\leq S\delta,
 \qquad \|\eta\|_2\leq2SK\delta.
 \tag{9}
\]

Set

\[
 m=\gamma/2,\qquad L=L_*+1.
 \tag{10}
\]

For any positive rational tolerance $\varepsilon\leq1$, it suffices to
choose

\[
 \delta=\min\left\{\frac\gamma{2S},
                     \frac\varepsilon{2SK}\right\}.
 \tag{11}
\]

Then (7)--(10) give

\[
 H\succeq mI,\qquad \|H\|_2\leq L,
 \qquad\|\eta\|_2\leq\varepsilon.
 \tag{12}
\]

These choices are effective. Compute a certified rational approximation
$\widehat\alpha$ with error at most $\delta/(4R)$, and set
$u=\widehat\alpha$, $v=\widehat\alpha^2$. Since $\delta\leq1$,
$|\widehat\alpha+\alpha|\leq3R$, so both parameter errors are at most
$\delta$. The certified root procedure cited in the earlier note uses
polynomial bit time in the requested precision. No exact computation of
$a$, $\eta$, or $H$ is required by the algorithm.

## The global Hessian estimate

The following calculation applies to the exact translated expansions
(6) and (12). Put

\[
 \Phi(x)=G(x)^2+\varepsilon\sum_{j=1}^n r_j(x)^2,
 \qquad D=L+nV.
 \tag{13}
\]

At $x=a+y$, separate $\Phi$ into its homogeneous parts of degrees two,
three, and four in $y$. Write $r=\|y\|_2$. The degree-two part satisfies

\[
 \nabla^2\Phi_2
 =2\eta\eta^{\mathsf T}+2\varepsilon J^{\mathsf T}J
 \succeq2\varepsilon\nu^2I.
 \tag{14}
\]

For a vector $b$ and a symmetric matrix $A$,

\[
 \nabla^2\bigl[2(b^{\mathsf T}y)(y^{\mathsf T}Ay)\bigr]
 =4\bigl[b(Ay)^{\mathsf T}+(Ay)b^{\mathsf T}
                         +(b^{\mathsf T}y)A\bigr].
\]

Its norm is at most $12\|b\|_2\|A\|_2r$. Using
$\|\eta\|_2\leq\varepsilon$, $\|g_j\|_2\leq V$, and
$\|A_j\|_2\leq1$ therefore gives

\[
 \|\nabla^2\Phi_3\|_2
 \leq12\bigl(\|\eta\|_2L+
          \varepsilon\sum_j\|g_j\|_2\|A_j\|_2\bigr)r
 \leq12\varepsilon Dr.
 \tag{15}
\]

For the quartic part, the identity

\[
 \nabla^2(y^{\mathsf T}Ay)^2
 =8(Ay)(Ay)^{\mathsf T}+4(y^{\mathsf T}Ay)A
 \tag{16}
\]

shows two different bounds. When $A=H\succeq mI$, it is at least
$4m^2r^2I$. For a general $A_j$, the first term in (16) is positive
semidefinite but the second need not be. Its lower bound is
$-4\|A_j\|_2^2r^2I$. Thus

\[
 \nabla^2\Phi_4\succeq4(m^2-\varepsilon n)r^2I.
 \tag{17}
\]

In particular, the argument does not assume that the square of an
indefinite quadratic form is convex.

Choose $\varepsilon$ to satisfy

\[
 0<\varepsilon\leq
 E:=\min\left\{1,\frac{m^2}{2n},
                    \frac{\nu^2m^2}{36D^2}\right\}.
 \tag{18}
\]

Adding (14), the negative of (15), and (17), then completing the square
in $r$, yields the following global estimate:

\[
 \begin{aligned}
 \nabla^2\Phi(a+y)
 &\succeq
    \bigl(2\varepsilon\nu^2-12\varepsilon Dr+2m^2r^2\bigr)I\\
 &=\left[2m^2\left(r-\frac{3\varepsilon D}{m^2}\right)^2
        +2\varepsilon\nu^2-
                          \frac{18\varepsilon^2D^2}{m^2}\right]I\\
 &\succeq\frac32\varepsilon\nu^2 I.
 \end{aligned}
 \tag{19}
\]

The last line follows from the last inequality in (18). This is uniform
over all real $y$, so it proves global strong convexity, including the
region between the local and large-radius estimates.

## Rational SOS output and polynomial complexity

All quantities in (18) are positive rationals with polynomial bit
length. Choose the smallest nonnegative integer $N$ such that
$2^{-2N}\leq E$, and set

\[
 t=2^{-N},\qquad\varepsilon=t^2.
\]

This square dyadic choice satisfies (18), has polynomial bit length,
and can be found by exact rational comparisons. Now compute $G$ using
(11). Output

\[
 F(x)=\frac{\Phi(x)}{\varepsilon\nu^2}
     =\left(\frac{G(x)}{t\nu}\right)^2
        +\sum_{j=1}^n\left(\frac{r_j(x)}\nu\right)^2.
 \tag{20}
\]

Every polynomial inside a square has rational coefficients. There are
$n+1=d$ squares. Since $H$ is positive definite, the degree-four part
of $G^2$ is nonzero, so $F$ has degree exactly four. Equation (19) gives
$\nabla^2F\succeq(3/2)I$, which proves the slightly weaker normalization
in (1). All summands vanish at $a$, so $F(a)=0$. As a sum of squares,
$F$ is nonnegative; strong convexity makes its minimizer and zero unique.
The common-zero argument following (3) also verifies uniqueness directly.

The bounds are uniform in the original dense input. All quantities in
(2), (5), and (7)--(11) have polynomial bit length. More specifically,
$\log(1/\nu)$, $\log(1/\varepsilon)$, and $\log(1/\delta)$ are
$O(d^3(\tau+\log d))$; all other displayed bounds need no more bits.
Thus refining $\alpha$ to the precision required by (11) takes
polynomial bit time. The earlier construction provides $Q_0,Q_1,Q_2$
in polynomial bit time and with polynomial-size rational entries.
Forming $G$, the residuals (3), and the rational factors in (20) uses
a polynomial number of rational operations on polynomial-size data.
Expanding a sum of $d$ squared quadratics produces at most
$O(d^4)$ distinct monomials, so an ordinary expanded coefficient list
also has polynomial size and can be computed in polynomial time.

The affine translation by $a$ is only a device for proving (19).
Neither the output polynomial nor its SOS representation contains
algebraic coefficients or requires the algorithm to express that
translation exactly.

## Scope and verification

The input representation is a dense rational polynomial promised
irreducible with exactly one real root. A sparse or circuit encoding of
that polynomial is outside the stated input-length bound. No optimal
coefficient or runtime exponent is claimed.

This result strengthens the existence of several convex quadratic
inequalities defining a singleton to one globally strongly convex
nonnegative quartic defining the same singleton. The sum-of-squares
identity certifies nonnegativity; global strong convexity follows from
the separate Hessian estimate (19). No claim of SOS-convexity is needed.

The [independent review](general-strongly-convex-quartic-review.md) checks
the complete construction, including the small-gradient approximation,
the negative quartic Hessian contribution, the rational SOS normalization,
and all bit bounds. Its targeted symbolic checks verify both Hessian
identities, the Jacobian determinant for symbolic degrees three through
five, and a regression example showing that a squared indefinite
quadratic need not be convex. All checks passed.

An inline `python - <<'PY'` document check verified this note's whitespace
and local links; it passed. No project-wide verification or CI inspection
was run. No publication-priority claim is made.
