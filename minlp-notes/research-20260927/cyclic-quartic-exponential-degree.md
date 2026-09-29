# Strongly convex integer quartics with exponentially large zero degree

Date: 2026-09-28. Status: construction and quantitative proof independently
reviewed; publication priority remains unestablished.

**Theorem.** For every integer $n\geq2$, one can construct in time
polynomial in $n$ an integer quartic $F_n$ in $n$ variables such that:

- $F_n$ is a sum of $n+2$ squares of integer quadratic polynomials.
- $\nabla^2F_n(x)\succeq I$ everywhere, and the Hessian has an exact
  rational positive definite Gram certificate.
- The unique zero $p$ has coordinate field degree
  \[
    [\mathbb Q(p):\mathbb Q]
      =d_n:=\frac{2^{n+1}-(-1)^{n+1}}3.
  \]
- The first coordinate alone has degree $d_n$. All coordinates lie in
  $(1/2,2)$.
- Every coefficient of $F_n$ has $O(\log(n+1))$ bits, and at most
  $O(n^2)$ monomials occur. The displayed integer square factors also
  have $O(\log(n+1))$ coefficient bits.

The degree sequence begins $3,5,11,21,43,85,171,\ldots$ for
$n=2,3,4,\ldots$. Thus the feasible point can have degree asymptotic to
$(2/3)2^n$ even though one globally strongly convex integer quartic
defines it, its coefficients are small, and convexity has a rational
certificate. This strengthens the previous independent cubic-block
lower bound $3^{\lfloor n/2\rfloor}$.

The subsequently [reviewed rational square compression](cyclic-quartic-square-compression.md)
gives an alternative integer quartic with all these properties using
only $n+1$ quadratic squares. It adjusts the rational regularization
parameter and preserves the same zero. The explicit $n+2$-square
construction below remains the baseline proof; no minimum-square
claim is needed here.

The arithmetic degree is not a lower bound for exact decision or for
all exact output formats. The zero below has a short expression using
a rational power with a binary-encoded exponent. Dense univariate
minimal-polynomial output is exponentially long. A rational translation
also gives this obstruction for an ordinary sparse minimal-polynomial
list, as detailed below, but a circuit or rational-power representation
need not be long.

## A cyclic system of rational quadratics

Put $m=n+1$, $\sigma=(-1)^m$, and

\[
 d=\frac{2^m-\sigma}{3},\qquad
 s_i=\frac{(-2)^i-1}{3}\quad(0\leq i<m),\qquad
 a=2^{1/d},\qquad p_i=a^{s_i}.
 \tag{1}
\]

The integer $d$ is positive and odd. The $s_i$ are integers, $s_0=0$,
and $s_1=-1$. We treat $x_0=1$ as a constant and use
$x_1,\ldots,x_{m-1}$ as the $n$ variables. All cyclic indices below
are taken modulo $m$.

Define

\[
 k_i=\begin{cases}
  0,&0\leq i<m-2,\\
  \sigma,&i=m-2,\\
  -\sigma,&i=m-1,
 \end{cases}
 \qquad
 q_i(x)=x_i^2-2^{k_i}x_{i+1}x_{i+2}.
 \tag{2}
\]

Every coefficient belongs to $\{0,1,-1,-2,-1/2\}$. The exponent
identity

\[
 2s_i-s_{i+1}-s_{i+2}=d k_i
 \tag{3}
\]

holds with cyclic indices. For the indices without a wrap, it is the
recurrence $2s_i=s_{i+1}+s_{i+2}$. The final two instances use
$s_m=\sigma d$ and $s_{m+1}=-2\sigma d-1$ before the cyclic
identification. Since $a^d=2$, (3) gives $q_i(p)=0$ for every $i$.

For all $i<m$, $|s_i|<d$. Hence

\[
  \frac12<p_i<2,
  \qquad \frac14<w_i:=p_i^{-2}<4.                  \tag{4}
\]

The polynomial $T^d-2$ is irreducible by Eisenstein's criterion at two.
Since $p_1=a^{-1}$ and every $p_i$ is an integer power of $a$,

\[
 \mathbb Q(p_1,\ldots,p_n)=\mathbb Q(a),
 \qquad [\mathbb Q(a):\mathbb Q]=d.                \tag{5}
\]

Its unique real embedding is consistent with the odd degree and with
the arithmetic restriction for rational convex singleton zero sets.

## A positive definite exposing quadratic

Consider the real linear combination

\[
 G_*(x)=\sum_{i=0}^{m-1}w_iq_i(x).
\]

Set $X_i=x_i/p_i$, including $X_0=1$. Equation (3) gives the exact
identity

\[
 G_*(x)=\sum_iX_i^2-\sum_iX_{i+1}X_{i+2}
       =\frac12\sum_i(X_i-X_{i+1})^2.               \tag{6}
\]

This is the energy of a cycle with its zeroth coordinate fixed at one.
It is nonnegative and zero precisely when every $X_i=1$. In particular,
the common real zero set of the rational quadratics (2) is exactly
$\{p\}$. The constant relation $q_0=1-x_1x_2$ avoids the unwanted
rational origin that occurs in a plain repeated-squaring chain.

For later quantitative estimates, write $x=p+u$, put $h_0=0$, and set
$h_i=u_i/p_i$ for $i>0$. The elementary anchored path estimate is

\[
 \|h\|_2^2\leq n^2\sum_i(h_i-h_{i+1})^2.          \tag{7}
\]

Indeed each $h_j$ is the sum of $j\leq n$ consecutive differences
starting at zero; Cauchy--Schwarz followed by summing over $j$ gives
(7). The cycle difference operator has norm at most two. Combining
these facts with (4) yields

\[
 G_*(p+u)=u^{\mathsf T}H_*u,
 \qquad \frac1{8n^2}I\preceq H_*\preceq8I.          \tag{8}
\]

Thus $G_*$ is stationary at $p$ and has a positive definite quadratic
part. Its coefficients are not generally rational. The construction
below approximates only its weights inside the exact rational space
of vanishing quadratics, so the zero is preserved exactly.

## Jacobian and residual bounds

Write the exact expansions

\[
 q_i(p+u)=b_i^{\mathsf T}u+u^{\mathsf T}T_i u,
 \qquad J=(b_i^{\mathsf T})_{i=0}^{m-1}.
\]

The three indices in each cyclic quadratic are distinct because
$m\geq3$. Its homogeneous quadratic matrix consists of a possible
diagonal entry 1 and a disjoint off-diagonal block with entries
$-2^{k_i}/2$. Terms involving $x_0$ become constant or linear.
Consequently

\[
 \|T_i\|_2\leq1,
 \qquad \|b_i\|_2<7<8.                            \tag{9}
\]

For the gradient bound, each row has at most three nonzero entries,
each of absolute value at most four, by (2) and (4).

Let $S$ be the cyclic shift $(Sz)_i=z_{i+1}$, and let
$E:\mathbb R^n\to\mathbb R^m$ insert a zero in coordinate zero.
With $D_p=\operatorname{diag}(p_1,\ldots,p_n)$,

\[
 J=\operatorname{diag}(p_0^2,\ldots,p_{m-1}^2)
       (2I-S-S^2)E D_p^{-1}.                       \tag{10}
\]

The factorization

\[
 2I-S-S^2=(2I+S)(I-S)
\]

and the triangle inequality give
$\|(2I+S)z\|_2\geq\|z\|_2$. Apply (7) to $E D_p^{-1}u$,
then use (4) on both diagonal matrices in (10). This proves

\[
 \|Ju\|_2\geq\frac1{8n}\|u\|_2,
 \qquad J^{\mathsf T}J\succeq\nu^2I,
 \quad \nu:=\frac1{8n}.                           \tag{11}
\]

The system therefore has a full-rank Jacobian at its zero with an
inverse-polynomial lower bound. No exponentially small root-separation
estimate is used.

## Explicit rational precision and integer output

Choose the integers and rational parameters

\[
 M=10^6n^5,\qquad \varepsilon=M^{-2},\qquad
 Q=32mM^2,\qquad \mu=\frac1{16n^2},\qquad L=9.
 \tag{12}
\]

Compute integers $z_i$ satisfying

\[
 \left|\frac{z_i}{Q}-w_i\right|\leq\frac1Q
       =\frac{\varepsilon}{32m},
\]

and define the rational vanishing quadratic

\[
 G(x)=\sum_i\frac{z_i}{Q}q_i(x).
\]

It has the exact translated expansion
$G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu$. From (8)--(12),

\[
 \|\ell\|_2\leq\frac{8m}{Q}=\frac\varepsilon4,
 \qquad \|H-H_*\|_2\leq\frac mQ=\frac\varepsilon{32},
 \qquad \mu I\preceq H\preceq LI.                  \tag{13}
\]

The last inequalities follow since $\varepsilon/32\leq1/(16n^2)$
and $\varepsilon\leq1$.

Put

\[
 \Phi=G^2+\varepsilon\sum_iq_i^2,
 \qquad A=2\sum_i z_iq_i,
 \qquad
 F_n=A^2+\sum_i\left(\frac{2Q}{M}q_i\right)^2
       =4Q^2\Phi.                                  \tag{14}
\]

The polynomial $A$ has integer coefficients because $2q_i$ does.
Moreover $2Q/M=64mM$ is an even integer. Thus every displayed square
factor in (14) is an integer quadratic. There are $m+1=n+2$ factors.
All vanish at $p$.

## Global strong convexity

For completeness, the regularization estimate is repeated with these
parameters. Decompose $\Phi(p+u)$ into homogeneous parts of degrees
two, three, and four in $u$, and set $r=\|u\|_2$ and

\[
 D=L+8m=8n+17\leq17n\quad(n\geq2).
\]

The quadratic part has Hessian at least $2\varepsilon\nu^2I$.
For symmetric $T$ and a vector $b$,

\[
 \left\|\nabla^2\bigl(2(b^{\mathsf T}u)
                                   (u^{\mathsf T}Tu)\bigr)\right\|_2
 \leq12\|b\|_2\|T\|_2r.
\]

Equations (9) and (13) therefore bound the cubic Hessian norm by
$12\varepsilon Dr$. The quartic part satisfies

\[
 \nabla^2\Phi_4\succeq4(\mu^2-\varepsilon m)r^2I.
\]

This retains the potentially negative contribution from squares of
indefinite quadratic parts $T_i$; these squares are not assumed convex.
The explicit parameters satisfy

\[
 \varepsilon\leq1,\qquad
 \varepsilon\leq\frac{\mu^2}{2m},\qquad
 \varepsilon\leq\frac{\nu^2\mu^2}{36nD^2}.          \tag{15}
\]

For the final inequality, its right-hand side is at least
$1/(170459136n^9)$, whereas $\varepsilon=1/(10^{12}n^{10})$.
The middle inequality follows directly from $m=n+1\leq3n/2$.
Completing the scalar square now gives

\[
 \begin{aligned}
 \nabla^2\Phi
 &\succeq(2\varepsilon\nu^2-12\varepsilon Dr+2\mu^2r^2)I\\
 &\succeq\left(2\varepsilon\nu^2-
                    \frac{18\varepsilon^2D^2}{\mu^2}\right)I
 \succeq\frac32\varepsilon\nu^2I.                 \tag{16}
 \end{aligned}
\]

The extra factor $n$ in (15) is not needed for (16), but will supply
the Gram certificate below. Multiplication by $4Q^2$ yields

\[
 \nabla^2F_n\succeq
     \frac{3Q^2}{32M^2n^2}I
   =\frac{96m^2M^2}{n^2}I\succeq I.               \tag{17}
\]

Since $F_n$ is nonnegative and zero at $p$, strong convexity makes $p$
its unique zero and unique minimizer. The independent common-zero
argument from (6) gives the same uniqueness. Positive definiteness of
$H$ ensures a nonzero quartic leading part, so the degree is exactly
four.

## Rational SOS-convexity certificate

The Gram construction in
[Rational Hessian certificates](sos-convex-quartic-realization.md)
depends only on the bounds for the translated quadratics, rather than
on their original companion-matrix source. Applying its formulas with
$m$ residuals, $n$ variables, and the bounds (9), (11), (13) gives a
Hessian Gram matrix on $(v,u\otimes v)$ with block estimates

\[
 C\succeq2\varepsilon\nu^2I,
 \quad R\succeq2\mu^2I,
 \quad \|B\|_2\leq6\sqrt n\,\varepsilon D.
\]

Its Schur complement is at least

\[
 2\varepsilon\nu^2-
        \frac{18n\varepsilon^2D^2}{\mu^2}
 \geq\frac32\varepsilon\nu^2>0                   \tag{18}
\]

by (15). Thus the Hessian has a positive definite Gram matrix. After
the translation is removed, its entries can be approximated by
rationals and projected onto the exact rational coefficient equations,
as in that reviewed construction. Positive definiteness survives this
projection. All bounds here, including $\|p\|\leq2\sqrt n$, are
polynomial in $n$ and their positive reciprocals are polynomial as well.
Consequently this produces a polynomial-size rational positive definite
Gram certificate in polynomial bit time. The same holds after scaling
by $4Q^2$.

An explicit positive gap is available before rational approximation.
In the imported block estimate set $q=2\mu^2$, $s=(3/2)\varepsilon\nu^2$,
and $B_0=6n\varepsilon D$. Then $s<q$, $B_0/q<1$, and
$2+\|p\|\leq3n$. Completing the block square and removing the
translation therefore bounds the smallest eigenvalue of the unscaled
Gram matrix in the original coordinates below by

\[
 \beta=\frac{s}{36n^2}
       =\frac1{1536M^2n^4}.                       \tag{18a}
\]

Approximating that matrix within $\beta/4$ in Frobenius norm and
projecting onto its exact rational coefficient equations leaves a
positive definite rational certificate. This makes the inverse-polynomial
precision requirement explicit.

This paragraph imports the explicitly proved Gram identity,
Schur-complement estimate, and rational affine-projection argument;
it does not infer SOS-convexity from ordinary convexity. It requires
no exact SDP feasibility oracle. The bit procedure for approximating
$p$ and the weights is given next and avoids a dense degree-$d$ input.

## Polynomial-time construction without expanding the minimal polynomial

The integer $d$ and every $s_i$ have $O(n)$ bits. To approximate the
weights, use

\[
 w_i=\exp\!\left(-\frac{2s_i}{d}\log2\right).
\]

The rational exponent multiplier has absolute value less than two.
For an integer $N\geq1$,

\[
 L_N=2\sum_{j=0}^{N-1}\frac{3^{-(2j+1)}}{2j+1}
 \quad\text{satisfies}\quad
 0<\log2-L_N<9^{-N}.                               \tag{19}
\]

Choose $N$ with $9^N\geq256Q$. The argument error is then at most
$1/(128Q)$. Both the true argument and its rational approximation lie
in $[-2,2]$. The exponential function has derivative less than nine
there, so the resulting error is less than $1/(8Q)$.

For a rational argument $z\in[-2,2]$, truncate the exponential Taylor
series after degree $K\geq2$. The absolute tail is at most

\[
 \frac{2^{K+2}}{(K+1)!}.
\]

Choose $K$ to make this at most $1/(8Q)$. Both $N$ and $K$ are
$O(\log Q)=O(\log(n+1))$. The resulting rational approximation to
$w_i$ is within $1/(4Q)$. Round its product with $Q$ to the nearest
integer $z_i$. This guarantees an error at most $3/(4Q)<1/Q$ in
$z_i/Q$, as required, without deciding a comparison at an algebraic
rounding boundary.

All computations in (19) and the finite Taylor series use rational
arithmetic on polynomial-bit integers; the degree-$d$ polynomial is
never expanded. The same method approximates $p_i=\exp((s_i/d)\log2)$
to any inverse-polynomial tolerance needed for the Gram certificate.

Finally, $M,Q$ are polynomial in $n$, and (4) gives
$|z_i|\leq4Q+1$. The residuals have two terms each, so $A$ has at
most $2m$ terms with coefficient magnitude polynomial in $n$.
Expanding (14) gives $O(n^2)$ monomials and coefficients of polynomial
magnitude. This proves the stated $O(\log(n+1))$ coefficient-bit
bound and polynomial-time output construction.

## Dense and ordinary sparse output consequences

The first coordinate $p_1=a^{-1}$ has primitive minimal polynomial
$2T^d-1$, which is sparse even though its degree is exponential.
Thus the original coordinates alone give no lower bound for ordinary
sparse minimal-polynomial output.

Translate just the first coordinate by one:

\[
 \widetilde F_n(y_1,x_2,\ldots,x_n)
       =F_n(y_1-1,x_2,\ldots,x_n).
\]

The unique first coordinate becomes $1+a^{-1}$, whose primitive
minimal polynomial is

\[
 2(T-1)^d-1.                                      \tag{20}
\]

Translation preserves irreducibility. Every one of its $d+1$
coefficients is nonzero: the positive-degree coefficients are signed
twice the corresponding binomial coefficients, and the constant term
is $-3$ because $d$ is odd. Hence both dense and ordinary sparse
monomial-list minimal-polynomial representations require at least
$d+1$ terms.

This translation preserves integer SOS structure, the global Hessian
bound, and rational SOS-convexity. Because the quartic degree stays
four, each original monomial expands into at most five terms with
constant-size binomial factors. Thus the translated quartic still has
$O(n^2)$ terms and $O(\log(n+1))$ coefficient bits. The lower bound
concerns output as an ordinary minimal-polynomial coefficient list;
(20) itself is succinct in a shifted basis or arithmetic circuit, and
the algebraic coordinate has a short rational-power description.

## Supporting convex quadratic formulation

The same point is the intersection of $n+1$ rational ellipsoids with
small coefficients. This follows directly from the exposing combination
and does not require the quartic regularization. Set

\[
 \tau=\frac\mu2=\frac1{32n^2},\qquad
 c_i=\frac{z_i}{Q},\qquad C=\sum_i c_i,\qquad W=\sum_iw_i,
 \qquad R_i=G+\tau q_i.
\]

Each $R_i$ has quadratic matrix at least $\mu I-\tau I=(\mu/2)I$
by (9) and (13), and $R_i(p)=0$. Define the real weights

\[
 \lambda_i=\frac1\tau\left(w_i-\frac{Wc_i}{\tau+C}\right).
\]

The $c_i$ are positive by their approximation to $w_i>1/4$, so
$\tau+C>0$. Moreover,

\[
 \begin{aligned}
 \tau(\tau+C)\lambda_i
 &=\tau w_i+w_i\sum_j(c_j-w_j)-(c_i-w_i)W\\
 &\geq\frac\tau4-\frac{8m}{Q}
  =\frac1{128n^2}-\frac\varepsilon4>0.
 \end{aligned}
\]

Since $\sum_i\lambda_i=W/(\tau+C)$, the definition gives
$\sum_i\lambda_iR_i=G_*$. Therefore

\[
 \{x:R_i(x)\leq0\ \text{for every }i\}=\{p\}.
\]

Every individual sublevel is a full-dimensional ellipsoid. Indeed its
quadratic part is positive definite, and a zero gradient at $p$ would
make $p$ its rational unique minimizer, contradicting (5). Its minimum
is therefore strictly below its value zero at $p$.

Positive denominator clearing makes all these quadratic polynomials
integral with $O(\log(n+1))$ coefficient bits. The corollary gives
another small native convex QCQP representation of the same
high-degree feasible point; the main theorem uses only one quartic
inequality and supplies its own rational Hessian certificate.

## Relationship to prior results and negative attempts

The cycle identity and exponential degree have a classical graph
antecedent. The grounded determinant of the directed Laplacian
$2I-S-S^2$ is $d=(2^m-(-1)^m)/3$.
[Lonc, Parol, and Wojciechowski, *On the number of spanning trees in directed circulant graphs*,
Networks 37 (2001), 129–133](https://onlinelibrary.wiley.com/doi/10.1002/net.2)
proves that the maximum number of directed spanning trees in the
two-generator circulant class is $\lfloor(2^m+1)/3\rfloor$, which is
the same integer. Tanaka's
[2026 revision of *Spanning trees in directed square cycles*](https://arxiv.org/pdf/2503.12561v2),
Theorem 4.2, identifies this exact fixed-root count with the Jacobsthal
number $J_m$; Theorem 1.1 credits the eigenvalue-product count to
Wojciechowski and Fellows (1989). The determinant count and its
exponential growth are not claimed new. The
[grounded-cycle prior audit](cyclic-grounded-energy-prior.md) checks
the tree-orientation convention and distinguishes the directed square
cycle from the undirected cycle supplying the energy.

Likewise, sparse binomial systems and positive Laplacian energies are
established objects. The [binomial and sandpile prior audit](cyclic-quadratic-toric-prior.md)
identifies the normalized equations with a directed sandpile firing
system and compares them with Eisenbud--Sturmfels partial characters
and the finite character-group description of toppling ideals. It also
proves directly that dehomogenization makes every coordinate a unit
and gives the coordinate ring $\mathbb Q[t,t^{-1}]/(t^d-2)$, so no
unjustified saturation or primeness assumption is needed. The potential contribution here is
their quantitative assembly into one globally strongly convex integer
SOS quartic with an exponentially large singleton zero field, small
coefficients, and a rational Hessian certificate. A search that fails to
find this exact assembly does not establish novelty.

The degree is larger than what comes from independent cubic examples,
but it does not establish an exact maximum in every dimension. The
[independently checked degree bound](quartic-zero-degree-adversarial.md)
shows that a rational SOS quartic with a unique real zero and a positive
definite Hessian there has joint zero-field degree at most $2^n-1$.
For a globally convex such polynomial, the same note improves the bound
to $2^n-3$ for $n\geq3$ and $2^n-5$ for $n\geq4$, using
Cayley--Bacharach and a reduction of flat directions. Thus this family
has the largest possible exponential base and comes within a factor
tending to $3/2$ of those general upper bounds. It attains the exact
maxima three, five, and eleven in dimensions two, three, and four.
The subsequently reviewed
[five-variable bound](five-variable-positive-base-bound.md) proves the
exact maximum 21 in dimension five, also attained here. These maxima
concern globally convex rational SOS quartics with a zero and positive
definite Hessian there. The upper bounds are separate results and do
not enter this construction's proof.

The [network degree bound](cyclic-quartic-noncirculant-search.md)
establishes an exact maximum within the strongly connected quadratic
binomial systems underlying this construction. Generalizing the cycle
to another two-out graph cannot increase the degree. The proof combines
the full exponent-lattice index with classical interlace-polynomial
identities; it also covers every minimum-size binomial system with
nonzero coordinates and a corank-one positive semidefinite exposing
combination. This restricted optimality does not extend the general
quartic upper bounds just stated.

High algebraic degree here does not require an exponentially ill-conditioned
Hessian at the zero. From the displayed sum of squares,
$\nabla^2\Phi(p)=2\ell\ell^{\mathsf T}+2\varepsilon J^{\mathsf T}J$.
The bounds $\|\ell\|\leq\varepsilon$, $\|J\|_F^2\leq64m$, and
$J^{\mathsf T}J\succeq\nu^2I$ give a condition number at most
$(1+64m)/\nu^2=O(n^3)$. Scaling to $F_n$ leaves it unchanged.
This is a local conditioning statement at the minimizer, not a uniform
upper Hessian bound on all of $\mathbb R^n$.

For $n\geq3$, the naive chain $x_{i+1}=x_i^2$ ending in
$x_n^2=2x_1$ encodes a nonzero point of degree $2^n-1$, but its origin
is also a common zero. For the sparse power set
$\{0,1,2,4,\ldots,2^{n-1}\}$ and minimal polynomial
$T^{2^n-1}-2$, all rational quadratic relations vanish at the origin:
no positive pair sum of those exponents is a multiple of $2^n-1$.
Thus every rational quadratic vanishing at that algebraic point has
zero constant term. Any rational SOS quartic vanishing there also
vanishes at the origin. This explains why simply squaring those
relations cannot give the desired convex singleton. The cyclic
construction includes the nonzero constant relation $1-x_1x_2$ and
avoids that obstruction. The restriction $n\geq3$ matters: for
$n=2$, the exponent pair $1+2=3$ supplies the additional relation
$x_1x_2-2=0$.

## Verification status

An initial exact inline SymPy check verified the cyclic exponent and
wrap identities, $|s_i|<d$, full Jacobian-symbol rank, and the grounded
determinant formula for $n=2,\ldots,12$. The determinant calculation
is supporting evidence; the field degree is proved by (5), and all
spectral bounds above have direct proofs.

The retained [exact checker](check_cyclic_quartic_exponential_degree.py)
was run with

```text
python research-20260927/check_cyclic_quartic_exponential_degree.py
```

It passed all precision and curvature parameter inequalities for
$n=2,\ldots,80$, and exact cyclic, Jacobian, determinant, and energy
identities for $n=2,\ldots,12$. It constructed the actual integer
quartics for $n=2,\ldots,6$ by the certified rational log/Taylor
procedure. For these cases it independently checked each weight
interval by exact rational powering against $w_i^d=2^{-2s_i}$,
integrality and degree of every output, and the nonzero coefficient
count of the translated minimal polynomial. The expanded outputs had
respectively 15, 31, 50, 72, and 98 monomials, with maximum coefficient
bit lengths 118, 131, 139, 146, and 151. These finite checks support the
formulas and implementation; the universal conclusions use the proofs
above.

The completed [fresh adversarial review](cyclic-quartic-fresh-review.md),
[independently reconstructed root audit](cyclic-quartic-exponential-degree-root-audit.md),
and [contributor quantitative audit](cyclic-quartic-quantitative-review.md)
found no blocking defect. The fresh review also constructed an exact
rational Hessian Gram certificate for $n=2$, checked its polynomial
identity, and verified positive definiteness by its six leading principal
minors. These reviews do not establish publication priority or replace
the separate audits of the cited general degree bounds. No project-wide
verification or CI inspection has been run.
