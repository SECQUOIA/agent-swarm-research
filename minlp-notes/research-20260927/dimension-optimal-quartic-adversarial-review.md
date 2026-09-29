# Independent review of the shortened quartic realization

Date: 2026-09-28. Status: passed the checks described below; no substantive
gap found. This is an independent mathematical review, not a formal proof
or a priority determination.

The reviewed source is
[Quartic realization with the minimum number of power coordinates](dimension-optimal-quartic-realization.md),
frozen at SHA256
39b285424e41cd5f3ac2eb262b810ba61140599dbf729779e386295c2729bad0.
The reviewer did not contribute to the arithmetic singleton construction.
The review reconstructed the quantitative argument and checked its uses of
the earlier [strong convexity proof](general-strongly-convex-quartic-singleton.md)
and [rational Hessian certificate proof](sos-convex-quartic-realization.md).
It does not re-establish every result cited by those earlier notes.

The claimed construction is valid for a dense irreducible rational
polynomial of degree greater than one with exactly one real root. Its
dimension lower bound is restricted to consecutive truncated power
coordinates. That restriction is essential to the statement reviewed here.

## 1. The smaller exposing matrix

Irreducibility in characteristic zero gives distinct roots. Exactly one
real root forces odd degree $d=2s+1$. The coefficient root bound and the
nonzero integer discriminant justify the displayed $R$ and $\sigma$ in
the source: all roots have modulus at most $R$, every pair is separated
by more than $\sigma$, and every nonreal root has imaginary part greater
than $\sigma/2$ in absolute value.

For a conjugate pair $u\pm iv$, the matrix

\[
 B=\begin{pmatrix}u^2+v^2&-u\\-u&1\end{pmatrix}
\]

has determinant $v^2$ and trace at most $1+R^2$. Consequently
$B\succeq bI$ for the source's
$b=\sigma^2/[4(1+R^2)]$. The recursive Gram construction is sound:
$S_j^{\mathsf T}S_j$ has endpoint entries one and interior entries two,
so induction gives

\[
 G_s\succeq b^s I,\qquad
 \|G_s\|\leq [2(1+R^2)]^s=U.
\]

It uses matrices of order at most $s+1$, not an explicitly formed tensor
product of exponentially growing order.

The matrix $D_\alpha$ maps the monomial vector to
$(T-\alpha)v_s(T)$. Thus
$Q_*=D_\alpha^{\mathsf T}G_sD_\alpha$ has kernel precisely
$\mathbb R v_n(\alpha)$ and represents $(T-\alpha)p(T)$, where
$n=s+1$. The affine block is positive definite. Indeed, the inverse
of the square restriction of $D_\alpha$ has entries among
$1,\alpha,\ldots,\alpha^{n-1}$ and norm at most $nR^{n-1}$.
This gives the stated affine-block gap

\[
 \gamma=\frac{b^s}{n^2R^{2n-2}}.
\]

The whole-matrix upper bound $(R+1)^2U$ also follows directly. No
orthogonal transformation or exact splitting-field computation is needed.

## 2. Exact rational projection and error control

The congruence constraints defining the rational matrix space are
independent even though the monomial vector was shortened. For every
$0\leq k<d$, there is an allowed pair $i,j\leq n$ with $i+j=k$.
The remainder of that monomial modulo the monic polynomial is exactly
$T^k$. A linear dependence among the remainder coefficient matrices
therefore has every coefficient zero.

Their Frobenius Gram matrix is consequently invertible, and the displayed
projection is the exact orthogonal projection onto the congruence kernel.
In particular it fixes $Q_*$ and cannot increase Frobenius error.
Off-diagonal matrix entries are counted twice by this inner product,
as required. Only powers through $2n=d+1$ occur, so the remainders,
Gram matrix, and inverse have polynomial rational bit length.

The approximation constants are conservative but sufficient. If a root
is approximated to error $\zeta\leq1$, then

\[
 \bigl||\widetilde\beta|^2-|\beta|^2\bigr|
 \leq(2R+1)\zeta,\qquad
 \|\widetilde B-B\|\leq(2R+3)\zeta.
\]

Writing $C_B=2R+3$ and $V_G=(2[1+(R+1)^2])^s$, the recursion gives
$\|\widetilde G-G\|\leq sC_B\zeta V_G$. Splitting the error in
$\widetilde D^{\mathsf T}\widetilde G\widetilde D$ into the Gram error
and the two errors in $D$ yields the source's

\[
 C_Q=V_GC_B[1+s(R+2)^2],\qquad
 \|\widetilde Q-Q_*\|_F\leq(n+1)C_Q\zeta.
\]

The stated choices of $\delta$ and $\zeta$ therefore give the desired
positive affine block and small gradient after projection. Specifically,
with $K=(n+1)R^n\geq\|v_n(\alpha)\|$, the translated gradient has norm
at most $2K\|Q-Q_*\|$, while the translated Hessian block remains at
least $\gamma I/2$. The projected quadratic vanishes exactly at the
target power point. Rounding without the congruence projection would
not preserve that equality.

The root-classification rule is safe: under $\zeta\leq\sigma/16$,
an approximate real root has imaginary part at most $\sigma/16$, while
an upper-half-plane root has imaginary part greater than $7\sigma/16$.
The threshold $\sigma/4$ separates them.

## 3. Shortened residuals and the Jacobian

The residual chain forces $x_j=x_1^j$ for every $j\leq n$.
The terminal residual then evaluates the original polynomial, because
each higher power through $d=2n-1$ is represented by
$x_nx_{k-n}$. Its only real common zero with the chain is the prescribed
power point.

All residuals, including the chain residuals, are divided by
$\kappa=1+\sum_{k>n}|c_k|$. Their translated quadratic matrices have
norm at most one. This normalization is necessary when the terminal
polynomial has large coefficients.

Before scaling, the Jacobian determinant equals $p'(\alpha)$.
One direct check uses the tangent vector
$(1,2\alpha,\ldots,n\alpha^{n-1})$: the first $n-1$ rows annihilate it,
and the last row evaluates to $p'(\alpha)$. The complementary chain
minor has the required unit magnitude and sign. After scaling,

\[
 \det J=\frac{p'(\alpha)}{\kappa^n}.
\]

The proposed $V=4n(d+1)R^{n+1}$ bounds the Jacobian norm and each
row-gradient norm. There are $d-1$ other roots in the product for
$p'(\alpha)$, even though only $n$ coordinates remain. The source uses
this correct exponent. Hence

\[
 \sigma_{\min}(J)\geq
 \frac{\sigma^{d-1}}{\kappa^nV^{n-1}}=\nu.
\]

Replacing $d-1$ by $n$ in this step would not be justified; no such
replacement appears in the frozen note.

## 4. Strong convexity, certificates, and bit complexity

The chosen square dyadic $\varepsilon=t^2$ meets both hypotheses of
the earlier strong convexity argument:

\[
 \varepsilon\leq \frac{m^2}{2n},\qquad
 \varepsilon\leq
 \frac{\nu^2m^2}{36n(L+nV)^2}.
\]

Applying that argument to
$F=(G/(t\nu))^2+\sum_j(r_j/\nu)^2$ gives the claimed lower Hessian
bound, with slack. The unique common zero of its square summands is
the target. Since the leading quadratic part of $G$ is positive
definite, the resulting polynomial has degree exactly four.

The Hessian certificate argument also survives the dimension change.
Its constant block is at least $2\varepsilon\nu^2I$, its quadratic
block at least $2m^2I$, and the mixed block has norm at most
$6\sqrt n\,\varepsilon(L+nV)$. The stated choice of $\varepsilon$
leaves a strictly positive Schur complement. Translation preserves a
quantified positive gap. Rational approximation followed by exact
projection onto all coefficient equations gives a positive definite
rational Hessian Gram matrix. These equations include monomials whose
required coefficients are zero. The claim concerns the Hessian Gram
matrix on $(y,x\otimes y)$, not a positive definite Gram matrix for
$F$ itself, which has a zero.

Every logarithmic precision parameter is polynomial in $d$ and the
coefficient height. The recursive rational arithmetic has polynomial
matrix dimension and polynomial denominator growth. Coefficient
projection requires polynomial-size rational linear algebra. The
dense input convention matters: a polynomial number of monomials in
$n=O(d)$ is polynomial in this input size.

For the numerical root step, this review examined the primary source
[Mehlhorn, Sagraloff, and Wang, Theorem 5](https://arxiv.org/pdf/1301.4870v2),
printed page 19. It provides certified isolation of all roots of an
integer polynomial and refinement to prescribed dyadic precision in
polynomial bit complexity. This is enough for the construction; no
randomized bivariate specialization procedure is required.

The polynomial-time claim is under the stated input promises.
It neither requires computing the splitting field nor hides a number
of root approximations exponential in $d$.

## 5. Scope of the dimension lower bound

For a rational nonnegative quartic with the prescribed unique zero,
set $h(T)=F(T,T^2,\ldots,T^q)$. The uniqueness of the zero and the
injectivity of this power curve imply that $h$ is not the zero
polynomial. Nonnegativity gives $h(\alpha)=h'(\alpha)=0$.
Irreducibility first gives $p\mid h$. Writing $h=pg$, separability and
$h'(\alpha)=0$ give $g(\alpha)=0$, hence $p^2\mid h$.
Therefore

\[
 2d\leq\deg h\leq4q,\qquad q\geq\lceil d/2\rceil.
\]

This argument does not require convexity or an SOS representation.
It does require the nonzero restriction and consecutive power
coordinates. It does not prove a dimension bound for arbitrary
coordinate encodings, an optimal algebraic-degree bound for quartic
optimization, or a complexity lower bound for solving the constructed
instances.

## 6. Targeted verification and remaining limits

The review ran exact SymPy calculations, separate from the author's
checks:

- Generic terminal Jacobian determinants were checked against
  $p'(\alpha)$ in degrees 3, 5, 7, 9, and 11.
- Large-coefficient terminal residuals tested the common normalization;
  exact positive-definiteness checks bounded their quadratic matrices.
- For the genuinely irrational target $\alpha=2^{1/5}$, an explicit
  positive definite factor Gram matrix was multiplied by $D_\alpha$.
  Its polynomial identity was checked modulo $\alpha^5-2$.
  After 120 exact rational bisections, rational approximation and exact
  congruence projection preserved the polynomial identity and gave
  positive affine-block principal minors.
- The rational projection was checked for idempotence and orthogonality
  on an independent test matrix.
- For four rational root-factor families, exact matrix calculations
  checked the recursive polynomial identity, both Gram bounds, the
  affine-block gap, the kernel identity, and the stated approximation
  error bounds. Those examples test matrix lemmas; their polynomials
  were not used as irreducible theorem instances.

All these checks passed. They test selected algebraic identities and
estimates, not their universal validity; the preceding arguments supply
the general reasoning. The review also checked local document links,
whitespace, and the frozen source hash. No project-wide verification,
CI inspection, or Lean proof was run. The review required no mathematical
change to the frozen source.

Novelty and the strongest possible formulations remain separate research
questions. In particular, an independent family with much larger
algebraic degree per coordinate would not contradict this construction
or its restricted truncated-power lower bound.
