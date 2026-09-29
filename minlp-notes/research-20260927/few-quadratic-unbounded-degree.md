# Three convex quadratics can force unbounded algebraic degree

Date: 2026-09-28. Status: constructive proof and extensions independently
reviewed; boundary interpretation remains subject to integration review.

This note constructs singleton feasible sets of three rational convex
quadratic inequalities with arbitrarily large algebraic degree. Independent
blocks give an explicit univariate witness-degree lower bound.

**Proposition.** Let $p\in\mathbb Q[t]$ be irreducible of degree $d>1$, with
exactly one real root $\alpha$. There are three rational quadratic
polynomials $q_1,q_2,q_3$ in $d-1$ variables, each with positive definite
Hessian, such that

\[
 \{x\in\mathbb R^{d-1}:q_i(x)\leq0\ (i=1,2,3)\}
 =\{(\alpha,\alpha^2,\ldots,\alpha^{d-1})\}.
\]

Each individual sublevel set is a full-dimensional ellipsoid. In particular,
taking $p(t)=t^d-2$ for any odd $d\geq3$ gives singleton feasibility
instances whose unique feasible point has degree $d=n+1$, while the number
of constraints and the dimension of their Hessian span are at most three.
For this binomial family, the rational coefficients can be chosen with bit
length polynomial in $d$, and the construction can be carried out using a
polynomial number of bit operations.

## A rational space of quadratic forms

Assume $p$ is monic, and write

\[
 v(t)=(1,t,\ldots,t^{d-1})^{\mathsf T}.
\]

Let $C\in\mathbb Q^{d\times d}$ be the companion matrix with ones on the
superdiagonal and the negatives of the coefficients of $p$ in its last row.
For every root $\beta$ of $p$,

\[
 Cv(\beta)=\beta v(\beta).
\]

Consider the real vector space

\[
 \mathcal L=\{B\in\mathbb S^d:
       v(t)^{\mathsf T}Bv(t)\equiv0\pmod {p(t)}\}.
\]

Polynomial division by $p$ expresses this condition as homogeneous rational
linear equations in the entries of $B$. Thus $\mathcal L$ has a rational
basis, and its rational matrices are dense in $\mathcal L$.

The roots of $p$ are distinct. List its nonreal roots as conjugate pairs

\[
 \beta_1,\overline{\beta_1},\ldots,
 \beta_s,\overline{\beta_s},\qquad d=2s+1.
\]

The Vandermonde determinant shows that

\[
 v(\alpha),\quad
 \operatorname{Re}v(\beta_1),\operatorname{Im}v(\beta_1),\quad\ldots,\quad
 \operatorname{Re}v(\beta_s),\operatorname{Im}v(\beta_s)
\]

is a real basis of $\mathbb R^d$. Define a real symmetric bilinear form
$B_*$ by declaring its matrix in this basis to be
$\operatorname{diag}(0,1,1,\ldots,1,1)$. It is positive semidefinite, has
kernel $\mathbb Rv(\alpha)$, and satisfies

\[
 v(\alpha)^{\mathsf T}B_*v(\alpha)=0,
 \qquad
 v(\beta_j)^{\mathsf T}B_*v(\beta_j)=1-1+2\mathrm i\,0=0.
\]

The same holds at the conjugate roots. Therefore $B_*\in\mathcal L$.

Let

\[
 U=\operatorname{span}_{\mathbb R}\{
       \operatorname{Re}v(\beta_j),\operatorname{Im}v(\beta_j):1\leq j\leq s
      \}.
\]

The restriction of $B_*$ to $U$ is positive definite. By density and the
openness of positive definiteness on this fixed subspace, choose
$B\in\mathcal L\cap\mathbb Q^{d\times d}$ whose restriction to $U$ is
positive definite. The matrix $B$ itself need not be positive semidefinite.

## A rational pencil with an irrational positive semidefinite member

Define rational symmetric matrices

\[
 Q_0=C^{\mathsf T}BC,\qquad
 Q_1=-(C^{\mathsf T}B+BC),\qquad Q_2=B,
\]

and let $Q(\lambda)=\lambda_0Q_0+\lambda_1Q_1+\lambda_2Q_2$. At
$\lambda_*=(1,\alpha,\alpha^2)$,

\[
 R:=Q(\lambda_*)=(C-\alpha I)^{\mathsf T}B(C-\alpha I).
\]

The space $U$ is $C$-invariant. The map $C-\alpha I$ has kernel
$\mathbb Rv(\alpha)$ and image $U$, since its restriction to $U$ has
the nonzero eigenvalues $\beta_j-\alpha$ and
$\overline{\beta_j}-\alpha$. Hence

\[
 R\succeq0,\qquad \ker R=\mathbb Rv(\alpha).
\]

Moreover, $B\in\mathcal L$ and $Cv(\alpha)=\alpha v(\alpha)$ give

\[
 v(\alpha)^{\mathsf T}Q_i v(\alpha)=0
 \quad (i=0,1,2).
\]

The restriction of $R$ to the rational hyperplane
$H=\{z\in\mathbb R^d:z_0=0\}$ is positive definite: its only kernel
vector is a multiple of $v(\alpha)$, whose first coordinate is one.

Under the proposition's assumptions that $p$ is irreducible and $d>1$,
the same pencil also defines a singleton spectrahedron in two scalar
variables:

\[
 \{(s,t)\in\mathbb R^2:Q_0+sQ_1+tQ_2\succeq0\}
       =\{(\alpha,\alpha^2)\}.                         \tag{1}
\]

Its unique feasible matrix has corank one. To prove (1), write
$v=v(\alpha)$ and $w=Bv$. The vector $w$ is nonzero: otherwise each
rational row of $B$ would give a linear relation among
$1,\alpha,\ldots,\alpha^{d-1}$, forcing $B=0$, contrary to positive
definiteness on $U$.

The real vectors $w$ and $C^{\mathsf T}w$ are linearly independent. If
$C^{\mathsf T}w=\kappa w$, then $\kappa$ is a real eigenvalue of $C$,
so $\kappa=\alpha$. Pairing with every other right eigenvector
$v(\beta)$ gives $w^{\mathsf T}v(\beta)=0$. Also
$w^{\mathsf T}v=v^{\mathsf T}Bv=0$. The Vandermonde basis then forces
$w=0$, a contradiction.

For every $(s,t)$, the identity
$v^{\mathsf T}(Q_0+sQ_1+tQ_2)v=0$ holds. If this matrix is positive
semidefinite, it must annihilate $v$. Expanding that equation gives

\[
 0=(\alpha-s)C^{\mathsf T}w+(t-s\alpha)w.
\]

Independence of the two vectors yields $s=\alpha$ and $t=\alpha^2$.
Conversely, the matrix at this pair is $R\succeq0$, proving (1).

## Three rational ellipsoids and their unique intersection

Positive definiteness of $Q(\lambda)|_H$ holds throughout an open
neighborhood of $\lambda_*$. Within the affine plane $\lambda_0=1$,
choose three rational points $\mu_1,\mu_2,\mu_3$ in this neighborhood
whose triangle contains $\lambda_*$ in its relative interior. Such a
triangle exists by the density of rational points. There are positive real
numbers $\tau_i$, with $\sum_i\tau_i=1$, such that

\[
 \lambda_*=\sum_{i=1}^3\tau_i\mu_i.
\]

For $x\in\mathbb R^{d-1}$, put

\[
 z(x)=(1,x_1,\ldots,x_{d-1})^{\mathsf T},\qquad
 q_i(x)=z(x)^{\mathsf T}Q(\mu_i)z(x).
\]

These polynomials have rational coefficients. Their Hessians are twice the
restrictions $Q(\mu_i)|_H$, so each is positive definite. At
$x_*=(\alpha,\ldots,\alpha^{d-1})$, all three polynomials vanish.

If $q_i(x)\leq0$ for all $i$, then

\[
 0\leq z(x)^{\mathsf T}Rz(x)
     =\sum_{i=1}^3\tau_iq_i(x)\leq0.
\]

Thus $z(x)\in\ker R=\mathbb Rv(\alpha)$. Comparing first coordinates
gives $z(x)=v(\alpha)$, proving uniqueness.

Finally, a strictly convex rational quadratic has a rational minimizer. Its
minimum cannot equal zero here, since that would make its only zero the
irrational point $x_*$. Each minimum is therefore strictly negative, and
each set $q_i\leq0$ is a full-dimensional ellipsoid.

## Uniform coefficient bounds for the binomial family

Let $a\geq2$ be an integer and $d\geq3$ an odd integer. This section gives
an explicit construction for $p(t)=t^d-a$. The construction does not require
irreducibility; when $a$ is prime, Eisenstein proves that the resulting
singleton has degree $d$.

Put

\[
 \alpha=a^{1/d},\qquad
 D=\operatorname{diag}(1,\alpha,\ldots,\alpha^{d-1}),\qquad
 B_*=D^{-1}\left(I-\frac1d\boldsymbol1\boldsymbol1^{\mathsf T}\right)D^{-1}.
\]

This is a suitable real target in $\mathcal L$. It is positive semidefinite
with kernel $\mathbb Rv(\alpha)$. For a nontrivial $d$-th root of unity
$\zeta$, the vector $D^{-1}v(\alpha\zeta)$ is
$(1,\zeta,\ldots,\zeta^{d-1})^{\mathsf T}$. Its entries and their squares
both sum to zero, because $d$ is odd. Thus

\[
 v(\alpha\zeta)^{\mathsf T}B_*v(\alpha\zeta)=0.
\]

The real span of the nonconstant Fourier vectors is
$\boldsymbol1^\perp$, so $U=D\boldsymbol1^\perp$. Since
$1\leq\alpha^j<a$ for $0\leq j<d$,

\[
 \|B_*\|_2\leq1,\qquad
 u^{\mathsf T}B_*u\geq a^{-2}\|u\|_2^2\quad(u\in U).
\]

The Frobenius-orthogonal projection onto $\mathcal L$ has a direct rational
formula. Index rows and columns from zero. For $0\leq r<d$, let $E_r$
have entry one where $i+j=r$, entry $a$ where $i+j=r+d$, and zero
elsewhere. Reduction modulo $t^d-a$ gives

\[
 \mathcal L=\{B\in\mathbb S^d:\langle E_r,B\rangle_F=0
                           \ (0\leq r<d)\}.
\]

These matrices have disjoint supports, so they are pairwise orthogonal, and

\[
 D_r:=\|E_r\|_F^2=(r+1)+a^2(d-r-1),\qquad d\leq D_r\leq da^2.
\]

Consequently

\[
 P_{\mathcal L}(T)=T-\sum_{r=0}^{d-1}
                  \frac{\langle E_r,T\rangle_F}{D_r}E_r
\]

is an explicit rational orthogonal projection. It preserves symmetry.

Choose a power of two $M$ with $16da^2\leq M<32da^2$. Approximate the
entries of $B_*$ by a symmetric matrix $T$ on the common grid
$M^{-1}\mathbb Z$, with entrywise error at most $1/M$, and set
$B=P_{\mathcal L}(T)$. One can compute the required approximations by
bisection for $a^{1/d}$ followed by rational interval arithmetic. Choosing a
grid point from an interval of length less than $1/M$ avoids any need to
decide an exact rounding tie. The required precision has
$O(\log(da))$ bits after the binary point, and the arithmetic takes time
polynomial in $d+\log a$.

Projection is nonexpansive in Frobenius norm and fixes $B_*$, so

\[
 \|B-B_*\|_2\leq\|B-B_*\|_F
 \leq\|T-B_*\|_F\leq\frac dM\leq\frac1{16a^2}.
\]

In particular,

\[
 \|B\|_2\leq2,\qquad
 u^{\mathsf T}Bu\geq\frac1{2a^2}\|u\|_2^2\quad(u\in U).
\]

For each entry of $B$, the projection subtracts a single correction with
denominator $MD_r$. Both this denominator and its numerator are bounded by
a fixed polynomial in $d$ and $a$. Each entry of $B$ therefore has
$O(\log(da))$ bits.

The rational triangle can also be chosen explicitly at polynomial
precision. Here $\|C\|_2=a$. If $z_0=0$ and $y=(C-\alpha I)z$, the first
$d-1$ coordinate equations give

\[
 z_{j+1}=\alpha z_j+y_j,\qquad \|z\|_2\leq ad\|y\|_2.
\]

Consequently

\[
 z^{\mathsf T}Rz\geq\frac1{2a^4d^2}\|z\|_2^2\quad(z\in H).
\]

The coefficient matrices satisfy

\[
 \|Q_0\|_2\leq2a^2,\qquad
 \|Q_1\|_2\leq4a,\qquad
 \|Q_2\|_2\leq2.
\]

Thus every $\lambda=(1,u,w)$ with

\[
 \max\{|u-\alpha|,|w-\alpha^2|\}
 \leq3e,\qquad e:=\frac1{100a^5d^2}
\]

has $Q(\lambda)|_H\succ0$. Indeed, its distance from $R|_H$ in operator
norm is at most $3(4a+2)e<1/(2a^4d^2)$.

Choose $c\in\mathbb Q^2$ within $e/16$ of $(\alpha,\alpha^2)$ in maximum
norm, using a common binary denominator polynomial in $a$ and $d$. The
triangle with vertices

\[
 c+(-e,-e),\qquad c+(2e,-e),\qquad c+(-e,2e)
\]

contains $(\alpha,\alpha^2)$ in its interior. All its vertices are within
distance $3e$ of that point and have $O(\log(da))$ bits. Its barycentric
weights at $(\alpha,\alpha^2)$ are all greater than $1/4$: the last two
weights are $(1+\delta_1/e)/3$ and $(1+\delta_2/e)/3$, where
$|\delta_j|<e/16$, and the first weight is their complement to one.
Adjoining a first coordinate equal to one gives $\mu_1,\mu_2,\mu_3$.

For a companion matrix of $t^d-a$, multiplication by $C$ or $C^{\mathsf T}$
permutes and scales matrix entries. Hence every entry of $Q_0,Q_1,Q_2$ is a
sum of at most two scaled entries of $B$. Every entry of $Q(\mu_i)$ is a
sum of three such terms. These are a fixed number of rational operations
on numbers with $O(\log(da))$ bits. The final quadratic coefficients thus
have $O(\log(da))$ bits, and the three dense quadratics have total encoding
length $O(d^2\log(da))$. All construction steps take time polynomial in
$d+\log a$.

The Hessian span is exactly three when $t^d-a$ is irreducible. Any real
linear dependence between these rational Hessians would give a rational
dependence. Since the three triangle vertices are affinely independent,
this would give a rational combination
$\theta_0Q_0+\theta_1Q_1+\theta_2Q_2$ whose affine Hessian vanishes.
The associated affine polynomial vanishes at the power-basis point, so all
its coefficients are zero and the whole matrix combination is zero.

For $\beta_j=\alpha\exp(2\pi\mathrm i j/d)$, positivity of $B$ on $U$
gives $v(\beta_j)^{\mathsf T}Bv(\overline{\beta_j})>0$. Evaluating the
matrix relation on this pair yields

\[
 \theta_0\alpha^2-2\theta_1\alpha\cos(2\pi j/d)+\theta_2=0.
\]

For $d\geq5$, two distinct cosines force $\theta_1=0$, and the
irrationality of $\alpha^2$ then forces $\theta_0=\theta_2=0$. For $d=3$,
the equation is
$\theta_0\alpha^2+\theta_1\alpha+\theta_2=0$, so the power basis gives the
same conclusion.

## Independent blocks and an explicit witness-degree lower bound

Fix odd $d\geq3$ and choose distinct primes $a_1,\ldots,a_k$ not dividing
$d$. Apply the construction to each $\alpha_i=a_i^{1/d}$ and take the
Cartesian product of the singleton feasible sets. The resulting system has
$3k$ rational convex quadratic inequalities, $n=k(d-1)$ variables, and
Hessian-span dimension $h=3k$, because the independent block spans have
disjoint matrix supports. Its unique feasible point generates

\[
 K=\mathbb Q(\alpha_1,\ldots,\alpha_k),\qquad [K:\mathbb Q]=d^k.
\]

Here is a field-degree proof that also identifies a coordinate of that
degree after a rational change of variables. The discriminant of
$t^d-a_i$ has no prime divisors outside those dividing $d a_i$. Therefore
the field generated by the first $i-1$ radicals is unramified at $a_i$.
The compositum of extensions unramified at a prime remains unramified there.
At any prime ideal above $a_i$, its normalized valuation of $a_i$ is one,
so $t^d-a_i$ is Eisenstein. Successively adjoining the radicals therefore
multiplies the degree by $d$ at every step. The discriminant and local
ramification facts used here are standard; see Milne,
[Algebraic Number Theory](https://www.jmilne.org/math/CourseNotes/ANTc.pdf),
Chapters 3, 6, and 7, especially Corollary 7.52 and Proposition 7.55.

The same argument works over $F=\mathbb Q(\zeta_d)$, because this cyclotomic
field is unramified outside the primes dividing $d$. Thus

\[
 [F(\alpha_1,\ldots,\alpha_k):F]=d^k.
\]

The monomials $\prod_i\alpha_i^{j_i}$ with $0\leq j_i<d$ form an
$F$-basis. Since $F$ contains the $d$-th roots of unity, this extension is
Galois, with all independent substitutions
$\alpha_i\mapsto\zeta_d^{j_i}\alpha_i$. The resulting $d^k$ images of

\[
 s=\alpha_1+\cdots+\alpha_k
\]

are distinct: equality between two would be a nontrivial $F$-linear
relation between the distinct basis monomials $\alpha_i$. Hence $s$ has
degree $d^k$ over $F$. Since $s\in K$ and $[K:\mathbb Q]=d^k$, it also has
degree exactly $d^k$ over $\mathbb Q$.

Set $R=1+\sum_i a_i$. Replace the first coordinate of the first block by
$R$ plus the sum of the first coordinates of all blocks, and retain every
other coordinate. This is an invertible rational affine change of variables.
Its linear part and inverse have entries in $\{0,1,-1\}$. It preserves
convexity, the number of constraints, and the dimension of the Hessian span.
The unique feasible point now has one coordinate $R+s$ of degree

\[
 d^k=\left(\frac nk+1\right)^k
     =\left(\frac{3n}{h}+1\right)^{h/3}.
\]

Moreover, its minimal polynomial has a nonzero coefficient at every degree.
Every conjugate $\sigma(s)$ satisfies $|\sigma(s)|<\sum_i a_i<R$, so
$R+\sigma(s)$ has positive real part. Each real linear factor and each
quadratic factor from a conjugate pair therefore has strictly alternating
coefficient signs. Their product has strictly alternating signs as well.
Thus even a sparse coefficient-list encoding needs $d^k+1$ nonzero terms.

The block constraints can be made into full-dimensional ellipsoids. Before
mixing, let $q_1,\ldots,q_m$, $m=3k$, denote the block quadratics. The
positive weights $\tau_j$ obtained from the block triangles satisfy
$\tau_j>1/4$ and $\sum_j\tau_j=k$. Their weighted sum is nonnegative,
with its only zero at the product point. Set

\[
 \varepsilon=\frac1{8k},\qquad
 q'_i=q_i+\varepsilon\sum_{j=1}^m q_j.
\]

The sum of the block Hessians is positive definite on the full space, so
every $q'_i$ has positive definite Hessian. The matrix
$I+\varepsilon\boldsymbol1\boldsymbol1^{\mathsf T}$ is invertible, so
mixing preserves the Hessian-span dimension. The new positive weights

\[
 \eta_i=\tau_i-\frac{\varepsilon k}{1+3k\varepsilon}
       =\tau_i-\frac1{11}>\frac18
\]

satisfy $\sum_i\eta_iq'_i=\sum_i\tau_iq_i$. Hence the mixed inequalities
still have exactly the same singleton feasible set. Rationality and
irrationality of the singleton again show that each individual ellipsoid
has nonempty interior. Apply the affine coordinate change above afterward.

The resulting input still has polynomial bit length. For fixed $k$ and
fixed radicands, its dense encoding length is $O_k(d^2\log d)$. Mixing may
sum constants with different rational denominators; only polynomial bounds,
not the individual-block $O(\log(da))$ bound, are needed at this step.

These instances rule out an output bound $f(h)N^C$, with a universal
constant $C$, for a solver required to return every feasible coordinate by
an explicit coefficient list of its univariate minimal polynomial. They
also give a degree obstruction for an explicit dense univariate
representation of the whole point. Here $N$ is the input bit length and
$h$ is the Hessian-span dimension. To see this, fix $k>2C$, then let $d$
grow through odd primes different
from the fixed $a_i$. The input length is $O_k(d^2\log d)$, whereas the
required coefficient-list length is at least $d^k+1$. Since $h\leq3k$,
$f(h)$ is bounded by a constant depending on this fixed $k$ along the
family.

The conclusion depends on the output format. A tower of algebraic
extensions or an arithmetic expression with radical gates can represent
these particular points compactly. This is a lower bound for explicit
univariate witnesses, not a lower bound for the decision problem or for
all exact witness encodings.

## Which real algebraic coordinates can occur?

A real algebraic number $\alpha$ can occur as a coordinate of a singleton
defined by rational convex polynomial inequalities if and only if its
minimal polynomial has exactly one real root. Three strictly convex
quadratic inequalities suffice for every irrational such $\alpha$, by the
proposition above. A rational $\alpha$ is isolated by the two intervals
$(x-\alpha-1)^2\leq1$ and $(x-\alpha+1)^2\leq1$.

For necessity, let $x_*$ be an algebraic singleton and
$K=\mathbb Q(x_{*,1},\ldots,x_{*,n})$. The inequalities active at $x_*$
alone have feasible set $\{x_*\}$. Otherwise, the segment from $x_*$ toward
another point satisfying them remains feasible for the active constraints
by convexity, and its sufficiently short initial portion satisfies all the
inactive constraints by continuity, contradicting uniqueness.

Every real embedding of $K$ maps $x_*$ to a real point satisfying the same
active polynomial equalities, since their coefficients are rational. It
must therefore fix the whole coordinate vector, hence all of $K$. Thus
$K$ has exactly one real embedding and odd degree. For any coordinate
$\alpha$, the extension $K/\mathbb Q(\alpha)$ has odd degree. Every real
embedding of $\mathbb Q(\alpha)$ extends to a real embedding of $K$: apply
it to the coefficients of a primitive element's odd-degree minimal
polynomial, which has a real root. Therefore $\alpha$ has exactly one real
conjugate. The algebraicity assumption on $x_*$ causes no restriction for
rational polynomial systems: an isolated real semialgebraic point defined
over $\mathbb Q$ has algebraic coordinates, by real quantifier elimination.

## Scope and verification

For a single block, the field generated by the feasible coordinates has
degree $d$: the first coordinate is $\alpha$ and all other coordinates are
powers of $\alpha$. For a prime $a$, the binomial $t^d-a$ is irreducible
by Eisenstein at $a$, and has exactly one real root for odd $d$.

Targeted verification: an inline `python - <<'PY'` command using SymPy
checked the companion identity, the explicit rational projection, the
factorization of the quadratic pencil, and vanishing modulo \(t^d-2\), all
with exact rational arithmetic for \(d=3,5,7\). All checks passed. An initial
version of the check compared unexpanded symbolic expressions structurally;
expanding the difference corrected that check.

The retained targeted command
`python research-20260927/check_few_quadratic_unbounded_degree.py` also passed.
It checks degrees $3,5,7,9$ with radicands $2,3$ using exact arithmetic:
rational projection, root relations, stationarity, positive definite
Hessians, and Hessian-span dimension three. It also checks a degree-nine
sum of two cubic radicals and the ten nonzero coefficients after translation.
The independent proof audit is recorded in
[few-quadratic-unbounded-degree-adversarial.md](few-quadratic-unbounded-degree-adversarial.md).
The later planar-pencil corollary was separately reviewed through its
left-eigenvector and Vandermonde argument; that argument requires the
stated irreducibility assumption. No additional computational check was
needed for this proof-only addition.

This is a verified construction for this repository's boundary analysis.
It makes no publication-priority claim; equivalence to prior results has
not been ruled out.

No project-wide checks or CI checks were run for this note. Its mathematical
claims rely on the proof above; numerical feasibility experiments are not
used in the argument.
