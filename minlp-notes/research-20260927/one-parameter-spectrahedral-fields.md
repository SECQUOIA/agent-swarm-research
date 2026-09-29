# Singleton rational spectrahedra in one variable

Date: 2026-09-28. Status: self-contained proof and independent review complete.
This is a supporting arithmetic classification, not a claimed new main
contribution. Its ingredients are classical positive semidefinite pencil
theory and the trace form of a totally real number field.

## Classification and sharp matrix size

**Theorem.** For a real number $\alpha$, the following are equivalent:

1. There are rational symmetric matrices $A,B$ of some finite size such
   that $\{x\in\mathbb R:A+xB\succeq0\}=\{\alpha\}$.
2. The number $\alpha$ is algebraic and all roots of its minimal polynomial
   over $\mathbb Q$ are real.

If these conditions hold and $d=[\mathbb Q(\alpha):\mathbb Q]$, the
smallest possible matrix size is exactly $2d$. A representation of that
size can be constructed by rational arithmetic from the minimal
polynomial and a rational open interval isolating $\alpha$. Its coefficient
bit lengths are polynomial in the degree and input bit lengths.

The theorem concerns an affine pencil in **one scalar variable with no
auxiliary variables**. Rational spectrahedral shadows and spectrahedra in
more variables have different arithmetic possibilities.

## Necessity, including identically singular pencils

Suppose $A+\alpha B\succeq0$ and this is the only feasible parameter.
Let $K=\ker A\cap\ker B$, which is a rational subspace. Choose rational
bases of $K$ and $K^\perp$. The resulting rational congruence writes the
pencil as a zero block on $K$ and a symmetric pencil

\[
 \widehat A+x\widehat B
\]

on $K^\perp$. The latter pencil has no nonzero common kernel vector.
Indeed, $A$ and $B$ annihilate $K$ and, by symmetry, preserve $K^\perp$;
a common kernel vector of the restrictions would belong to both
$K^\perp$ and $K$. Its feasible set is still $\{\alpha\}$.

Set $C=\widehat A+\alpha\widehat B\succeq0$. For any nonreal
$z\in\mathbb C$, suppose that

\[
 (C+(z-\alpha)\widehat B)v=0,
 \qquad v\in\mathbb C^r\setminus\{0\}.
\]

Taking the complex inner product with $v$ gives

\[
 v^*Cv+(z-\alpha)v^*\widehat Bv=0.
\]

Both quadratic forms are real. The imaginary part implies
$v^*\widehat Bv=0$, and then $v^*Cv=0$. Positive semidefiniteness gives
$Cv=0$, so the original equation gives $\widehat Bv=0$ and
$\widehat Av=0$. The real or imaginary part of $v$ would be a nonzero
real common kernel vector, a contradiction.

Consequently

\[
 D(x)=\det(\widehat A+x\widehat B)\in\mathbb Q[x]
\]

is nonzero and all its complex roots are real. The matrix $C$ is singular:
otherwise it is positive definite, and positive definiteness persists on
an open parameter interval around $\alpha$. Thus $D(\alpha)=0$, proving
that $\alpha$ is algebraic and its minimal polynomial is real-rooted.

An alternative proof avoiding common-kernel reduction uses principal
minors. If every nonzero principal-minor polynomial were positive at
$\alpha$, all would remain nonnegative on a neighborhood, contradicting
the singleton assumption. A nonzero principal minor vanishing at
$\alpha$ is real-rooted by the same complex-kernel argument.

## The lower bound of twice the algebraic degree

We show that $\alpha$ is a multiple root of $D$. If
$\operatorname{rank}C\leq r-2$, the adjugate of $C$ vanishes, so

\[
 D'(\alpha)=\operatorname{tr}(\operatorname{adj}(C)\widehat B)=0.
\]

Otherwise $C$ has rank $r-1$. In a real orthonormal basis adapted to its
kernel, write

\[
 C+t\widehat B=
 \begin{pmatrix}
   C_1+tE & tb\\
   tb^{\mathsf T} & t\beta
 \end{pmatrix},\qquad C_1\succ0.
\]

If $\beta\neq0$, choose sufficiently small nonzero $t$ with
$t\beta>0$. Then $C_1+tE\succ0$ and the Schur complement

\[
 t\beta-t^2b^{\mathsf T}(C_1+tE)^{-1}b
\]

is positive. This gives another feasible parameter, a contradiction.
Therefore $\beta=0$, which again gives $D'(\alpha)=0$. For $r=1$ the
same argument is the scalar fact that a nonzero affine function cannot
be nonnegative at exactly one point.

Let $f$ be the minimal polynomial of $\alpha$. Characteristic zero gives
separability, and $D(\alpha)=D'(\alpha)=0$ implies $f^2\mid D$. Hence

\[
 2d\leq\deg D\leq r\leq\text{size}(A).
\]

This bound counts the total size if several LMIs are combined as a block
diagonal pencil. Allowing auxiliary scalar variables is outside its scope.

## A rational construction of size twice the degree

Now let $f$ be irreducible of degree $d$, with distinct real roots
$\alpha_1<\cdots<\alpha_d$, and let $\alpha=\alpha_k$. In the power
basis $1,\alpha,\ldots,\alpha^{d-1}$ of $F=\mathbb Q(\alpha)$, let
$M$ be the rational matrix of multiplication by $\alpha$. Define the
rational trace Gram matrix

\[
 G_{ij}=\operatorname{Tr}_{F/\mathbb Q}(\alpha^{i+j}),
 \qquad 0\leq i,j<d.
\]

Let $V_{j,i}=\alpha_j^i$ be the real Vandermonde matrix. Then

\[
 G=V^{\mathsf T}V\succ0,
 \qquad VM=\operatorname{diag}(\alpha_1,\ldots,\alpha_d)V.
\]

For a rational number $r$ with $f(r)\neq0$, define

\[
 L_r(x)=G(M-xI)(M-rI)^{-1}.
\]

This is a rational symmetric affine pencil. Indeed,

\[
 L_r(x)=V^{\mathsf T}
  \operatorname{diag}\!\left(
       \frac{\alpha_1-x}{\alpha_1-r},\ldots,
       \frac{\alpha_d-x}{\alpha_d-r}\right)V.       \tag{1}
\]

Choose rational numbers $r_-<\alpha<r_+$ such that $\alpha$ is the
only root of $f$ in $[r_-,r_+]$, and neither endpoint is a root. We claim

\[
 \operatorname{diag}(L_{r_-}(x),L_{r_+}(x))\succeq0
 \quad\Longleftrightarrow\quad x=\alpha.           \tag{2}
\]

For the $k$th diagonal entry in (1), the first block requires
$x\leq\alpha$ and the second requires $x\geq\alpha$. At $x=\alpha$,
both ratios are nonnegative for every $j$: if $j<k$, all relevant
numerators and denominators are negative, and if $j>k$, they are all
positive. The $k$th entries are zero. This proves (2), including the
extreme-root and rational cases without separate constructions.

The unique feasible matrix in (2) has corank exactly two. Its determinant
is

\[
 \frac{\det(G)^2}{f(r_-)f(r_+)}f(x)^2,
\]

where the same formula applies to a nonmonic $f$ because its leading
coefficient cancels in each ratio. This attains the lower bound.

## Encoding and exact computation

Suppose an integer minimal polynomial of degree $d$ has coefficient bit
length at most $\tau$, and $r_-,r_+$ have numerator and denominator bit
length at most $\ell$. Normalizing the polynomial to be monic gives a
companion multiplication matrix with rational entries of $O(\tau)$ bits.
The trace entries can be computed as

\[
 G_{ij}=\operatorname{tr}(M^{i+j}).
\]

At most $2d-2$ matrix powers, rational matrix products, and two rational
matrix inversions suffice. Determinant bounds for these operations give
coefficient bit lengths polynomial in $d,\tau,\ell$; for example a
conservative bound $O(d^2(\tau+\ell+\log(d+1)))$ suffices. These
operations therefore take polynomially many bit operations. This is an
explicit construction from an algebraic-number representation; it does
not assert a new algorithm for finding minimal polynomials from arbitrary
oracles.

## Meaning for exact optimization

The classification supplies a small arithmetic test case for rational
conic formulations: a scalar algebraic constant can be imposed by a
rational LMI without auxiliary variables exactly when it is totally real.
The required matrix size also grows at least linearly in its algebraic
degree. In particular, $\sqrt2$ is admissible and needs size four, whereas
$\sqrt[3]2$ cannot be forced in one scalar variable by any rational LMI.

The two-variable singleton pencil in
[the three-quadratic construction](few-quadratic-unbounded-degree.md)
admits numbers with exactly one real conjugate. Its extra variable is
therefore essential for every nonrational number in that construction.
This observation does not by itself improve an optimization algorithm or
establish complexity hardness. It distinguishes representation classes
that would otherwise appear interchangeable.

## Prior results and novelty qualification

- Liang, Li, and Bai, *Trace minimization principles for positive
  semi-definite pencils*, Linear Algebra and its Applications 438 (2013),
  3085–3106, [author PDF](https://web.cs.ucdavis.edu/~bai/publications/lianglibai13.pdf).
  Lemma 3.8(2), printed page 3095, proves that finite eigenvalues of a
  positive semidefinite Hermitian pencil are real, including singular
  pencils. This already supplies the spectral ingredient of the necessity
  proof. The paper also identifies earlier antecedents for nonsingular
  second matrices. Our elementary argument is included to make the exact
  arithmetic implication and singular case transparent.
- Nguyen and Nguyen, *Positive semidefinite interval of matrix pencil and
  its applications for the generalized trust region subproblems* (2023),
  [primary preprint](https://arxiv.org/pdf/2302.14352).
  Theorems 1–4 classify positive semidefinite parameter sets using
  congruence and Jordan structure, including singleton cases. A separate
  prior audit is checking whether its statements or cited predecessors
  explicitly include the arithmetic classification or minimum size.
- Hillar's [2010 BIRS slides](https://www.birs.ca/workshops/2010/10w5119/files/hillarbirstalk20100302.pdf),
  slide 18, raise a fixed-variable algebraic-number realization question.
  This historical question is not evidence that the present specialization
  remains open. The notation on that slide also requires care when
  comparing affine, homogeneous, and projected representations.
- The trace-form construction is classical linear algebra over number
  fields. In a totally real field its positivity is the Vandermonde
  identity used above. No theorem about realizing totally real algebraic
  numbers as eigenvalues of rational symmetric matrices is needed here.

The sources examined so far do not establish priority for the formulation
with minimum size $2d$. Neither the classification nor the size statement
is claimed novel. The wider source comparison is recorded in
[the singleton-field prior audit](singleton-field-characterization-prior.md).

## Verification record

The proof was derived independently by the author and the root agent,
using different treatments of identically singular pencils. A separate
[adversarial review](one-parameter-spectrahedral-fields-review.md)
checked the full classification, singular-pencil reduction, sharp minimum
size, and polynomial encoding claim. It found no substantive correction
and independently checked four further exact examples. The review
supports correctness; it does not establish novelty.

Targeted command actually run:

```text
python research-20260927/check_one_parameter_spectrahedral_fields.py
```

It passed 12 exact singleton constructions from five irreducible
polynomials of degrees one through four, including a nonmonic quadratic,
all choices of real conjugate, and rational endpoints. For each example,
the checker uses rational principal minors and exact real-root isolation
to certify feasibility at exactly the selected conjugate. A negative
constant times $f(x)^2$ is the full determinant, excluding every other
parameter. It also verifies corank two, an identically singular pencil
with a removable common kernel, and four simple-root examples with a
positive-definite side. These finite checks do not prove the universal
theorem, its lower bound, or its asymptotic bit estimate. No project-wide
verification or CI inspection was run.
