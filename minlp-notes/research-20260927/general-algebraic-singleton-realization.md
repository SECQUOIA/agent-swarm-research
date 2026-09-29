# Polynomial-time singleton realization for one-real-conjugate algebraic numbers

Date: 2026-09-28. Status: quantitative construction and comparison
consequence independently reviewed. This note makes the general construction in
[Three convex quadratics can force unbounded algebraic degree](few-quadratic-unbounded-degree.md)
effective. It does not change that note's sharper coefficient bounds for
binomials.

**Theorem.** Let an irreducible polynomial $p\in\mathbb Q[T]$ of degree
$d>1$ be given by its dense coefficient list, and suppose that it has
exactly one real root $\alpha$. A deterministic algorithm constructs three
rational quadratic polynomials $q_1,q_2,q_3$ in $d-1$ variables such that
each Hessian is positive definite and

\[
 \{x\in\mathbb R^{d-1}:q_i(x)\leq0\quad(i=1,2,3)\}
 =\{(\alpha,\alpha^2,\ldots,\alpha^{d-1})\}.
\]

Each individual sublevel set is a full-dimensional ellipsoid. The
algorithm uses a polynomial number of bit operations in the input length,
and its output has polynomial bit length. More explicitly, if the
primitive integer multiple of $p$ has coefficients of absolute value at
most $2^H$, then every output coefficient has bit length polynomial in
$d+H$, and the construction after primitive normalization takes time
polynomial in $d+H$.
Irreducibility and the number of real roots are promises in this statement;
the construction does not need to verify them.

The qualitative singleton argument is the earlier note's argument. The
additional content is a uniform choice of precision, a rational projection
that preserves the exact polynomial identities, and a rational triangle
whose size has a polynomial bit bound. No optimal exponent is claimed.

## Input normalization and elementary bounds

Clear denominators and divide by the content to write

\[
 P(T)=a_dT^d+\cdots+a_0\in\mathbb Z[T],\qquad
 a_d>0,\qquad |a_j|\leq2^H,\qquad H\geq1.
\]

These operations take polynomial bit time. If each original rational
coefficient has numerator and denominator bit length at most $b$, one can
take $H=O(db)$, so bounds polynomial in $d,H$ are polynomial in the dense
input length. From now on let $p=P/a_d$ be monic. Set

\[
 R=2^{H+1},\qquad s=(d-1)/2,\qquad
 K=dR^{d-1},\qquad
 J=2^{s+H(d-1)}K^{d-1}.
 \tag{1}
\]

The assumptions imply that $d$ is odd and $d\geq3$. The usual elementary
root bound gives $|\beta|\leq1+\max_{j<d}|a_j/a_d|\leq R$ for every
root $\beta$. All roots are distinct, since $P$ is irreducible in
characteristic zero.

For completeness, a separation bound follows directly from the nonzero
integer discriminant. With $m=d(d-1)/2$, define the positive dyadic number

\[
 \sigma=2^{-H(d-1)}(2R)^{-m}.
 \tag{2}
\]

For any two roots at distance $\delta$, the discriminant identity gives

\[
 1\leq|\operatorname{disc}(P)|
 \leq |a_d|^{2d-2}\delta^2(2R)^{2m-2}.
\]

Thus every two distinct roots are at distance greater than $\sigma$.
In particular, each nonreal root has imaginary part of absolute value
greater than $\sigma/2$. All logarithms of the bounds in (1)--(2) are
polynomial in $d,H$.

## A quantitatively controlled target form

Put $v(t)=(1,t,\ldots,t^{d-1})^{\mathsf T}$. List the roots in the upper
half-plane as $\beta_1,\ldots,\beta_s$, and form the real matrix

\[
 W=[v(\alpha),\operatorname{Re}v(\beta_1),
          \operatorname{Im}v(\beta_1),\ldots,
          \operatorname{Re}v(\beta_s),
          \operatorname{Im}v(\beta_s)].
\]

Every entry has absolute value at most $R^{d-1}$, so
$\|W\|_2\leq\|W\|_F\leq K$. If $V$ is the complex Vandermonde matrix
with conjugate roots adjacent, then

\[
 |\det W|=2^{-s}|\det V|
 =2^{-s}\frac{|\operatorname{disc}(P)|^{1/2}}{a_d^{d-1}}
 \geq2^{-s-H(d-1)}.
\]

The product formula for singular values now gives

\[
 \|W^{-1}\|_2\leq
 \frac{\|W\|_2^{d-1}}{|\det W|}\leq J.
 \tag{3}
\]

Let $D=\operatorname{diag}(0,1,\ldots,1)$ and define

\[
 B_*=W^{-\mathsf T}DW^{-1},\qquad
 U=W(\{0\}\times\mathbb R^{d-1}).
\]

Then $B_*\succeq0$, its kernel is $\mathbb Rv(\alpha)$, and

\[
 \|B_*\|_2\leq J^2,\qquad
 u^{\mathsf T}B_*u\geq K^{-2}\|u\|_2^2\quad(u\in U).
 \tag{4}
\]

Indeed, if $u=W(0,y)$, then $u^{\mathsf T}B_*u=\|y\|_2^2$ and
$\|u\|_2\leq K\|y\|_2$.

Consider the rationally defined real vector space

\[
 \mathcal L=\{B\in\mathbb S^d:
        v(T)^{\mathsf T}Bv(T)\equiv0\pmod {p(T)}\}.
\]

The form $B_*$ belongs to $\mathcal L$: its value at $v(\alpha)$ is zero,
and its value at $v(\beta_j)$ is $1+\mathrm i^2=0$. The same holds at
the conjugate roots. A polynomial vanishing at all the distinct roots is
divisible by $p$ over $\mathbb C$, hence has zero remainder here.

## Exact rational projection with polynomial-size coefficients

For $0\leq\ell\leq2d-2$, compute the remainder

\[
 T^\ell\bmod p(T)=\sum_{r=0}^{d-1}r_{\ell r}T^r.
\]

For $0\leq r<d$, let $E_r\in\mathbb S^d(\mathbb Q)$ have entries

\[
 (E_r)_{ij}=r_{i+j,r},\qquad 0\leq i,j<d.
\]

Then, with the full Frobenius inner product,

\[
 \mathcal L=\{B\in\mathbb S^d:
              \langle E_r,B\rangle_F=0\quad(0\leq r<d)\}.
\]

Using the full matrix inner product counts the off-diagonal entries twice,
as required by $v(T)^{\mathsf T}Bv(T)$. These $d$ equations are independent:
$(E_r)_{0j}=\delta_{rj}$ for $0\leq j<d$. Their rational Gram matrix

\[
 \Gamma_{rt}=\langle E_r,E_t\rangle_F
\]

is therefore positive definite. The Frobenius-orthogonal projection is

\[
 \Pi_{\mathcal L}(T)=T-
       \sum_{r,t=0}^{d-1}E_r(\Gamma^{-1})_{rt}
                                \langle E_t,T\rangle_F.
 \tag{5}
\]

The remainder coefficients have polynomial bit length. To see this
directly, start with the remainders $1,T,\ldots,T^{d-1}$ and repeatedly
multiply by $T$ and reduce the leading term. There are at most $d-1$
additional steps. Denominators divide $a_d^{d-1}$, and coefficient
magnitudes are bounded by $(d2^H)^{d-1}$, or by one for the initial
remainders. Hence their numerators and denominators have
$O(d(H+\log d))$ bits after using this common denominator.

It follows that all entries of $E_r$, $\Gamma$, and $\Gamma^{-1}$ have
polynomial bit length. For the inverse, clear the rational denominators
and apply the determinant and cofactor formulas with Hadamard's bound;
the matrix size is $d$. Exact rational linear algebra computes (5) in
polynomial bit time. No numerical conditioning bound on $\Gamma$ is
needed: the operation is exact and, in real Frobenius norm,

\[
 \|\Pi_{\mathcal L}(T)-B_*\|_F\leq\|T-B_*\|_F.
 \tag{6}
\]

## Computing the target to sufficient precision

Set

\[
 A=d^2(2R)^{d-1}.
\]

Choose certified dyadic approximations to the roots with absolute error
at most $\zeta$, where

\[
 \zeta\leq
 \min\left\{\frac{\sigma}{16},
              \frac1{128dJ^3AK^2}\right\}.
 \tag{7}
\]

The required number of precision bits is $O(d^2(H+\log d))$. The unique
real root is identified by the condition that the approximate imaginary
part has absolute value less than $\sigma/4$. The upper half-plane roots
are identified by approximate imaginary part greater than $\sigma/4$.
These tests are separated from their thresholds by (2) and (7). Replace
the approximate real root by its real part, and use the selected upper
half-plane approximations to form the rational real matrix $\widetilde W$
in the same way as $W$.

For $j\leq d-1$, the elementary difference-of-powers identity gives

\[
 |\widetilde\beta^j-\beta^j|
 \leq j(2R)^{j-1}\zeta.
\]

It follows that
$\|\widetilde W-W\|_F\leq A\zeta$. In particular this error is at most
$1/(2J)$, so $\widetilde W$ is invertible and

\[
 \|\widetilde W^{-1}\|_2\leq2J,\qquad
 \|\widetilde W^{-1}-W^{-1}\|_2\leq2J^2A\zeta.
\]

Compute the rational symmetric matrix

\[
 T=\widetilde W^{-\mathsf T}D\widetilde W^{-1}
\]

exactly. Applying the preceding inequalities to the difference of the
two products, and using $\|X\|_F\leq\sqrt d\|X\|_2\leq d\|X\|_2$,
gives

\[
 \|T-B_*\|_F\leq6dJ^3A\zeta<\frac1{16K^2}.
\]

Now put $B=\Pi_{\mathcal L}(T)$. It is rational and satisfies the
polynomial remainder identities exactly. By (4) and (6),

\[
 \|B\|_2\leq2J^2,\qquad
 u^{\mathsf T}Bu\geq\frac1{2K^2}\|u\|_2^2\quad(u\in U).
 \tag{8}
\]

All these rational computations have polynomial bit complexity. The
root approximations have polynomially many bits; forming powers up to
$d-1$ preserves a polynomial bit bound; and rational matrix inversion,
multiplication, and (5) preserve that bound for matrices of polynomial
size. This argument uses determinant bounds for exact rational inverses,
so it does not assume that an arbitrary sequence of unreduced rational
operations has small intermediate expressions.

The only numerical algebraic subroutine is certified complex root
isolation and approximation. For integer polynomials, a deterministic
algorithm runs in bit time polynomial in degree, coefficient bit length,
and requested precision. One suitable primary reference is
Mehlhorn, Sagraloff, and Wang,
[*From approximate factorization to root isolation with application to cylindrical algebraic decomposition*](https://arxiv.org/pdf/1301.4870v2),
Journal of Symbolic Computation 66 (2015), 34--69, Theorem 5. It supplies
isolating disks for all complex roots and refines them to radius below
$2^{-N}$ in $\widetilde O(d^3+d^2H+dN)$ bit operations. Its univariate
algorithm is deterministic; the randomized multivariate applications are
separate. Certified centers can be rounded to dyadic rationals after
requesting a few additional precision bits. Only a polynomial bound is
used here. An independent polynomial-time basis is Neff,
[*Specified precision polynomial root isolation is in NC*](https://www.sciencedirect.com/science/article/pii/S0022000005800613),
Journal of Computer and System Sciences 48 (1994), 429--463.

## An explicit positive-definiteness margin and rational triangle

Let $C$ be the rational companion matrix with ones on the superdiagonal
and the negatives of the coefficients of monic $p$ in its last row.
Thus $Cv(\beta)=\beta v(\beta)$ for every root. Define

\[
 Q_0=C^{\mathsf T}BC,\qquad
 Q_1=-(C^{\mathsf T}B+BC),\qquad Q_2=B,
\]

and $Q(\lambda)=\lambda_0Q_0+\lambda_1Q_1+\lambda_2Q_2$. At
$\lambda_*=(1,\alpha,\alpha^2)$,

\[
 F_*:=Q(\lambda_*)=(C-\alpha I)^{\mathsf T}B(C-\alpha I).
\]

The companion eigenbasis shows that
$\operatorname{image}(C-\alpha I)=U$ and
$\ker(C-\alpha I)=\mathbb Rv(\alpha)$. Thus (8) implies
$F_*\succeq0$ with kernel $\mathbb Rv(\alpha)$.

There is a direct gap bound on the affine-variable subspace
$G=\{z\in\mathbb R^d:z_0=0\}$. If $y=(C-\alpha I)z$ and $z\in G$,
the first $d-1$ equations give

\[
 z_{j+1}=\alpha z_j+y_j\qquad(0\leq j<d-1).
\]

Iterating from $z_0=0$ and applying Cauchy--Schwarz gives
$\|z\|_2\leq dR^{d-1}\|y\|_2=K\|y\|_2$. Consequently

\[
 z^{\mathsf T}F_*z\geq\frac1{2K^4}\|z\|_2^2
       \qquad(z\in G).
 \tag{9}
\]

Set $M=dR$, so $\|C\|_2\leq M$, and set

\[
 S=2J^2(2M+1).
\]

By (8),

\[
 \|Q_0\|_2\leq2J^2M^2,\qquad
 \|Q_1\|_2\leq4J^2M,\qquad
 \|Q_2\|_2\leq2J^2,
\]

so $S$ bounds $\|Q_1\|_2+\|Q_2\|_2$. Let

\[
 e=2^{-\lceil\log_2(16K^4S)\rceil}.
 \tag{10}
\]

This rational number and its reciprocal have polynomial bit length, and
$3eS\leq3/(16K^4)<1/(2K^4)$. In view of (9), every point
$\lambda=(1,u,w)$ with
$\max\{|u-\alpha|,|w-\alpha^2|\}\leq3e$ satisfies
$Q(\lambda)|_G\succ0$.

Refine the unique real root approximation, if necessary, to error

\[
 |\widehat\alpha-\alpha|\leq e/(128R).
\]

This still requires only $O(d^2(H+\log d))$ precision bits. The rational
center $c=(\widehat\alpha,\widehat\alpha^2)$ then satisfies
$\|c-(\alpha,\alpha^2)\|_\infty<e/16$, since
$|\widehat\alpha+\alpha|\leq3R$. Use the three rational triangle
vertices

\[
 c+(-e,-e),\qquad c+(2e,-e),\qquad c+(-e,2e).
 \tag{11}
\]

Each vertex is within $3e$ of $(\alpha,\alpha^2)$. This point is in the
triangle's interior: writing $\delta=(\alpha,\alpha^2)-c$, its last two
barycentric coordinates are
$(1+\delta_1/e)/3$ and $(1+\delta_2/e)/3$, and the first is their
complement to one. All three exceed $1/4$. Adjoin the first coordinate
one to the vertices in (11), obtaining $\mu_1,\mu_2,\mu_3$ and positive
weights $\tau_i$ such that

\[
 \sum_i\tau_i=1,\qquad \sum_i\tau_i\mu_i=\lambda_*.
\]

The weights are used only to prove correctness; the algorithm does not
compute or output them.

## Completion of the construction and bit bound

For $z(x)=(1,x_1,\ldots,x_{d-1})^{\mathsf T}$, output

\[
 q_i(x)=z(x)^{\mathsf T}Q(\mu_i)z(x)\qquad(i=1,2,3).
\]

Their Hessians are $2Q(\mu_i)|_G\succ0$. Since $B\in\mathcal L$ and
$Cv(\alpha)=\alpha v(\alpha)$,

\[
 v(\alpha)^{\mathsf T}Q_jv(\alpha)=0\qquad(j=0,1,2).
\]

Thus $x_*=(\alpha,\ldots,\alpha^{d-1})$ satisfies all three equalities.
If $q_i(x)\leq0$ for all three indices, then

\[
 0\leq z(x)^{\mathsf T}F_*z(x)
       =\sum_i\tau_iq_i(x)\leq0.
\]

The kernel of $F_*$ and the first coordinate of $z(x)$ force
$z(x)=v(\alpha)$. This proves the singleton statement. Each $q_i$ has a
rational unique minimizer because its Hessian is rational and positive
definite. Its minimum is at most zero, and equality would make its unique
zero the irrational point $x_*$. Its minimum is therefore negative, so
its sublevel set is a full-dimensional ellipsoid.

For clarity, all precision and size choices depend only on $d,H$, rather
than on a root separation or spectral gap supplied as additional input.
The logarithms of $R,K,J,A,S,\sigma^{-1},e^{-1}$ and the reciprocal of
the permitted error in (7) are $O(d^2(H+\log d))$. The root computation
therefore takes polynomial bit time. All later operations are a
polynomial number of exact rational polynomial and matrix operations in
dimensions at most $d$, on inputs of polynomial bit length. Determinant
bounds give polynomial bit length for their outputs. Finally, forming
the three $Q(\mu_i)$ and their $O(d^2)$ quadratic coefficients preserves
these bounds. This proves the stated polynomial construction and total
encoding bound.

## Consequence for exact sum comparison

Suppose $\alpha_1,\ldots,\alpha_k$ are given by dense irreducible rational
polynomials $p_i$, each of degree $d_i>1$ with exactly one real root, and
let $b\in\mathbb Q$. Construct the three quadratics for each block and
add the affine budget

\[
 \sum_{i=1}^k x_{i,1}\leq b.
\]

The block constraints force
$x_i=(\alpha_i,\ldots,\alpha_i^{d_i-1})$, so the resulting native
rational convex quadratic system is feasible exactly when

\[
 \alpha_1+\cdots+\alpha_k\leq b.
\]

It has $\sum_i(d_i-1)$ variables, $3k$ quadratic inequalities, and one
affine inequality. Its Hessians are positive semidefinite after embedding
the blocks in the full variable space, and their span has dimension
$h\leq3k$. The affine budget contributes the zero Hessian. Construction
time and output size are polynomial in the entire comparison input,
with an absolute polynomial exponent. Rational summands can be moved
into $b$, and rationally weighted sums are handled by changing only the
affine budget.

Thus exact comparison for sums of these algebraic numbers reduces by a
polynomial-time many-one reduction to exact native PSD quadratic
feasibility, with parameter $h\leq3k$. In particular, an algorithm with
running time $f(h)N^C$ and an absolute exponent $C$ would yield an
algorithm of the same parameterized form for this comparison problem
with parameter $k$.

This is an arithmetic benchmark for the feasibility problem. It does not
prove that the comparison problem is hard in any complexity class, and
does not prove a decision lower bound or exclude an FPT algorithm. The
restriction to one real conjugate is essential to this construction;
ordinary irrational square roots have two real conjugates, so this is
not a reduction of unrestricted sum-of-square-roots comparison. The
explicit univariate witness-size obstruction in the earlier note remains
a separate conclusion about output representations.

## Verification scope

The proof uses the exact companion and projection identities and the
displayed perturbation bounds. The
[independent review](general-algebraic-singleton-review.md) checks the
complete proof, the root-isolation source, and the comparison consequence.
It also records exact rational checks on three non-binomial examples,
including nonmonic cubic and quintic input: the projection and remainder
identities, positive leading principal minors for every affine Hessian,
and certified real-root-interval containment in the chosen triangle all
passed. Numerical complex-root approximations only proposed candidates
for those finite checks; they are not a substitute for the certified
root algorithm used in the theorem.

The targeted formatting command
`git diff --no-index --check /dev/null research-20260927/general-algebraic-singleton-realization.md`
passed. No project-wide verification or CI inspection was run. This note
makes no publication-priority claim.
