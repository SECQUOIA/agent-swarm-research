# Rational SOS descent under a strict Hessian certificate

Date: 2026-09-28. Status: primary-literature audit complete; the two derived
lemmas below independently reviewed. A separate construction gives a
negative answer in four variables. This note assesses the prior results
and the scope of that advance; publication priority is not established.

A later [three-variable construction](ternary-rational-sos-convex-counterexample.md)
settles the remaining dimension in this certificate class. Its
[additional prior audit](three-variable-rational-sos-descent-prior.md)
records the closer quaternary-quartic comparisons. The affirmative
two-variable result below therefore gives the matching dimension lower
bound.

Let $F\in\mathbb Q[x_1,\ldots,x_n]$ have degree four and minimum zero.
Suppose

\[
 y^{\mathsf T}\nabla^2F(x)y
 =w(x,y)^{\mathsf T}Mw(x,y),\qquad
 w=(y,x\otimes y),\qquad M\in\mathbb S_{++}^{n+n^2}(\mathbb Q).
 \tag{1}
\]

The question is whether $F$ must be a sum of squares of rational
polynomials of degree at most two. Assumption (1) already implies global
strong convexity, so its zero $a$ is unique. It does **not** provide a
positive definite Gram matrix for $F$ on $(1,x,x_ix_j)$: every positive
semidefinite Gram matrix for $F$ annihilates the nonzero monomial vector
at $a$.

The [four-variable construction](rational-sos-convex-descent-algebra.md)
answers the question negatively while preserving (1). The sources
examined do not supply this combination of properties. They settle
important nearby questions: totally real descent holds; odd-degree
descent fails; strictly positive forms can fail rational descent; and an
interior SOS certificate descends. Below, the hypotheses in (1) give an
affirmative answer in two variables and whenever $a$ is rational. Those
affirmative cases follow from existing tools and are not claimed new
research results.

## What the established descent theorems say

| Primary source and locator | Established conclusion | Relevance to (1) |
| --- | --- | --- |
| [Hillar, 2009, Theorems 1.2 and 1.4](https://arxiv.org/pdf/0704.2824) | An invertible real Gram matrix for a rational polynomial can be replaced by a rational one. SOS representations over a totally real number field descend to $\mathbb Q$. | The Hessian and $F$ are different Gram problems. A field with one real embedding need not be totally real. |
| [Quarez, 2009 preprint, Theorem 3.1](https://arxiv.org/pdf/0907.2336) | Constructive descent over a totally real Galois field, with at most $(4[K:\mathbb Q]-3)m$ rational squares starting from $m$ squares. | Improves certificate length; retains the field restriction. |
| [Scheiderer, 2016, Theorem 1.2 and Proposition 1.6](https://ems.press/content/serial-article-files/32129) | A trace-form proof extends totally real descent to algebras and quadratic modules, without a Galois assumption. | Taking traces across complex embeddings does not preserve positivity. |
| [Peyrl–Parrilo, 2008, Proposition 8](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf) | A numerical Gram matrix with a sufficient strict eigenvalue margin can be rounded and projected to an exact rational certificate. | Justifies rationalizing a strict Hessian Gram; gives no automatic strict margin for the Gram problem of $F$. |
| [Davis–Papp, 2022, Theorem 2.6](https://arxiv.org/pdf/2105.11369) | Rational interior weighted SOS polynomials have rational dual certificates and rational SOS decompositions. | The zero-minimum polynomial is on the boundary of the ordinary SOS cone. |

The [local Davis–Papp full text](../literature/papers/davis2022-dual-certificates-and-efficient-rational/fulltext.md)
was read for Theorem 2.6 and its proof. The other sources above were read
from their primary PDFs. Rational positive weights in a Gram or SOS
identity can be absorbed into rational squares using the four-square
theorem; a rational Cholesky factor is not required.

[Ahmadi–Parrilo, Theorem 3.1, proof of (c)$\Rightarrow$(b)](https://arxiv.org/pdf/1111.4587)
proves the SOS form of the first-order convexity inequality by Taylor
integration. At a minimizer with value zero this gives an SOS for $F$
over $\mathbb R$. Substituting an irrational minimizer can introduce
irrational coefficients, so this argument alone does not descend the SOS.

## Known counterexamples do not establish the requested counterexample

[Scheiderer, Theorem 2.1](https://ems.press/content/serial-article-files/32129)
constructs rational forms that are real SOS but not rational SOS. His
Theorem 4.1 classifies all such nonnegative ternary quartics: each is a
product of four complex lines in general position. This classification
is used below. His Lemma 4.5 gives another sufficient descent condition:
the space spanned by possible SOS summands is defined over $\mathbb Q$.
That condition is sufficient, not necessary.

The old question about odd-degree fields has a negative answer. In the
[2018 preprint of Laplagne, Theorem 5.1](https://arxiv.org/pdf/1810.04215),
the displayed example is a **sextic** in four variables, SOS over
$\mathbb Q(\sqrt[3]2)$ but not over $\mathbb Q$. Theorem 4.1 of that
preprint proves descent for a sum of just two squares over an odd-degree
extension. These statements should not be confused. The journal PDF
of the 2020 publication returned HTTP 403 during this audit; theorem
numbers here refer to the accessible preprint.

A simpler **quartic** over the same cubic field is explicitly reproduced
and proved in [Laplagne, 2024, Section 3.1 and Proposition 3.1](https://arxiv.org/pdf/2312.16801).
The paper attributes this example to Capco–Laplagne–Scheiderer. Its
Theorem 3.4 constructs a strictly positive homogeneous quartic in eight
variables that is real SOS but not rational SOS. Thus neither odd field
degree nor strict pointwise positivity suffices in general. “Strictly
positive” for this homogeneous form means positive away from the origin.

The displayed quartic from Section 3.1 is not convex. For its restriction
$g(x_1,x_2,x_3)=f(1,x_1,x_2,x_3)$, exact differentiation gives

\[
 \nabla^2g(0)=
 \begin{pmatrix}16&32&64\\32&32&16\\64&16&64\end{pmatrix}.
 \tag{2}
\]

Its first $2\times2$ principal minor is $-512$. The eight-variable
construction restricts at $y=0$ to $f+x_2^4$, which has the same Hessian
at $(x_0,x_1,x_2,x_3)=(1,0,0,0)$ in these directions. It too is
nonconvex. These exact witnesses exclude both displayed examples from (1).
They do not rule out other constructions or rational affine sections.

[Capco–Scheiderer, 2020, introduction and Section 3](https://www.impan.pl/shop/en/publication/transaction/download/product/113947)
discuss rational descent and the then-open strictly positive cases.
Laplagne's later result is necessary when assessing their open questions.
Their introduction reports the negative odd-degree result; the explicit
quartic formula used here was checked in Laplagne's later primary paper.

The recent [Keshari–Ojha–Patra preprint](https://arxiv.org/pdf/2508.07060)
was also checked: Theorem 1.2 concerns one-variable semialgebraic sets
with boundary in the coefficient field and their natural generators.
Theorems 5.2–5.3 give strictly positive compact-set certificates, and
Theorem 9.3 descends an Archimedean property under a zero-dimensional
quotient assumption. These are not a degree-four unconstrained descent
theorem for (1).

## A precise consequence of the strict Hessian Gram

**Lemma 1.** Retain the rational quartic and Hessian identity (1), but
temporarily allow any minimum value. Let $a$ minimize $F$ and put
$m=F(a)$. Then
$F-m$ has a real positive definite Gram matrix in the basis

\[
 z_a(x)=\big((x_i-a_i)_i,
             ((x_i-a_i)(x_j-a_j))_{i\le j}\big).
 \tag{3}
\]

Consequently:

1. If $a\in\mathbb Q^n$ and $m=0$, then $F$ is rational SOS.
2. If $m>0$, then $F$ has a positive definite Gram matrix on the full
   degree-at-most-two monomial basis and is rational SOS, even if $a$ or
   $m$ is irrational.

**Proof.** Write $u=x-a$. Taylor's formula gives

\[
 F(a+u)-m=\int_0^1(1-t)
 \begin{pmatrix}u\\(a+tu)\otimes u\end{pmatrix}^{\mathsf T}
 M\begin{pmatrix}u\\(a+tu)\otimes u\end{pmatrix}\,dt.
 \tag{4}
\]

There is a matrix $T_t$, affine in $t$, that maps the monomial vector
$z=(u_i,u_iu_j)_{i\le j}$ to the vector in (4). Its action on an
arbitrary coefficient-space vector $(b,c)$ is

\[
 T_t(b,c)=(b,a\otimes b+tEc),
 \tag{5}
\]

where $E$ duplicates the off-diagonal quadratic coordinates into the
ordered tensor coordinates and is injective. Set
$J=\int_0^1(1-t)T_t^{\mathsf T}MT_t\,dt$.
If $(b,c)^{\mathsf T}J(b,c)=0$, strict positivity of $M$ and continuity
imply $T_t(b,c)=0$ for every $0<t<1$. The first block gives $b=0$;
the second then gives $Ec=0$, hence $c=0$. Thus $J\succ0$.

When $a$ is rational, $T_t$ has rational polynomial entries, so $J$ is
rational. A rational $LDL^{\mathsf T}$ factorization and four-square
decompositions of its positive diagonal entries give rational squares.
If instead $m>0$, the Gram matrix $\operatorname{diag}(m,J)$ is positive
definite on $(1,z_a)$. Translation is an invertible real change of the
full monomial basis. Hillar's interior descent theorem now applies to
the rational polynomial $F$. $\square$

For $m=0$, (3) is a basis of
$\{q\in\mathbb R[x]_{\le2}:q(a)=0\}$. If $a$ is irrational this
hyperplane is not defined over $\mathbb Q$: its normalized evaluation
normal has coordinates $(1,a_i,a_ia_j)$. Therefore one cannot simply
apply rational density inside that face. This observation does not
prove nonexistence of a rational Gram matrix on a smaller face. Indeed,
the repository's [explicit irrational-zero example](convex-quartic-rational-sos.md)
already is a rational SOS with a strict Hessian certificate.

## The two-variable case follows from the ternary-quartic classification

**Lemma 2.** If $n=2$ in (1) and $\min F=0$, then $F$ is rational SOS.

**Proof.** Let $F_4$ be the homogeneous degree-four part of $F$ and let
$C\succ0$ be the principal block of $M$ indexed by $x\otimes y$.
Comparison of terms of degree two in $x$ gives

\[
 y^{\mathsf T}\nabla^2F_4(x)y=(x\otimes y)^{\mathsf T}C(x\otimes y).
\]

Euler's identity therefore yields, for $x\ne0$,

\[
 12F_4(x)=x^{\mathsf T}\nabla^2F_4(x)x
 =(x\otimes x)^{\mathsf T}C(x\otimes x)>0.
 \tag{6}
\]

Homogenize $F$ to a nonnegative rational ternary quartic $\widehat F$.
Its affine chart has exactly one zero, by strong convexity. Equation
(6) excludes zeros on the line at infinity. Thus $\widehat F$ has
exactly one real projective zero.

Suppose $F$ were not rational SOS. Homogenization and dehomogenization
preserve rational SOS for polynomials of degree at most four, so
$\widehat F$ would not be rational SOS. Scheiderer's Theorem 4.1 then
expresses $\widehat F$ as a product of four distinct complex lines in
general position. None can be a real line: at a real point of that line
away from its intersections with the others, a simple real factor
changes the sign of the product. The lines consequently form two
complex-conjugate pairs. The intersection of each pair is a real
projective point, and general position makes the two intersections
distinct. This gives two real projective zeros, a contradiction.
$\square$

The proof needs no effective factorization or certificate size bound.
It uses the dimension-specific classification; it does not extend that
classification to quartics in four or more homogeneous variables.

## Arithmetic nonattainment: established mechanism and specific advance

The four-variable construction supplies a rational $F$ satisfying (1)
with minimum zero but no rational SOS. Applying Lemma 1 to $F+\epsilon$
shows that every rational $\epsilon>0$ gives an interior rational SOS.
Thus the usual SOS lower-bound SDP

\[
 \sup\{\gamma:F-\gamma=v^{\mathsf T}Qv,\ Q\succeq0\},
 \qquad v=(1,x_i,x_ix_j)_{i\le j},
 \tag{7}
\]

has a real optimal solution of value zero and a strictly feasible Gram
matrix at every negative rational bound. Rational Gram certificates
approach zero but cannot certify it exactly. This is arithmetic failure
of attainment after restricting certificates to $\mathbb Q$, not a
real SDP duality gap or a failure of numerical convergence.

The broad phenomenon “Slater holds and the rational optimal value has
no rational optimizer” is not by itself the new contribution. It already
follows from the older real-SOS/non-rational-SOS forms. To see this, let
$p$ be any such rational form of degree $2d$, let $u$ list the degree-$d$
monomials, and set $R=u^{\mathsf T}u$. Consider

\[
 \min\{t:p+tR=u^{\mathsf T}Qu,\ Q\succeq0,\ t\ge0\}.
 \tag{8}
\]

A real Gram matrix $Q_0$ for $p$ gives an optimizer at $t=0$ and strictly
feasible matrices $Q_0+tI$ for $t>0$. At every positive rational $t$,
interior descent yields a rational feasible Gram matrix. A rational
optimizer at zero would give a rational SOS for $p$, a contradiction.
This is an elementary consequence of the prior counterexamples and
interior descent, rather than a separate prior theorem being asserted.

The specific addition is failure of rational certification at the true
minimum of a globally strongly convex quartic with a strict rational
Hessian Gram certificate, using the ordinary constant perturbation in
(7). The algebraic construction and its exact checks must establish
these properties independently of this literature comparison. The
results alone do not prove a complexity lower bound, a numerical
instability claim, or the absence of useful rational certificates of
other types.

The two-variable argument originally left a gap below the four-variable
counterexample. The later three-variable construction closes it within
the stated full positive definite Hessian Gram class. Neither this
dimension boundary nor the lack of a matching search result establishes
priority.

## Search and verification record

Searches on 2026-09-28 included combinations of `rational SOS`,
`SOS-convex`, `strongly convex`, `odd degree`, `Hillar`, `Scheiderer`,
`Laplagne`, and `descent`, followed by the primary sources and their
citation chains. Follow-up searches included `sos convex rational not
rational`, `SOS-convex rational SOS`, and `sum of squares rational Slater
attainment`. The queries did not locate a prior counterexample satisfying
(1). Search results about convex polynomials that fail **real** SOS or
SOS-convexity do not give the required arithmetic separation. No
numerical optimization experiment was used as proof.

Primary PDFs were downloaded to a temporary directory and read using
`pdftotext -layout`. The final JEMS version of Scheiderer's paper was
used for theorem and lemma numbering. The AMS PDF of Laplagne's 2020
paper was inaccessible; the accessible 2018 preprint and 2024 paper
were read instead. No inaccessible source is counted as examined.

An inline `python -` command using SymPy exactly verified the three-square
identity of Laplagne's quartic modulo $\alpha^3-2$, the Hessian in (2),
its minor $-512$, and the unchanged witness after adding $x_2^4$.
Those checks establish identities and disprove convexity of the displayed
examples. They do not independently verify the papers' proofs of
nonexistence of rational SOS decompositions.

Only targeted checks for this note were run. No project-wide tests or
CI checks were run. A [fresh independent review](rational-sos-convex-descent-prior-review.md)
checked Lemmas 1–2, the comparison SDP (8), and Scheiderer's published
Theorem 4.1. The review requested two
precision fixes, now incorporated: specify positive semidefinite Gram
matrices in the zero-kernel observation, and explicitly relax the
minimum-zero normalization in Lemma 1. The reviewer did not re-review
the separate four-variable construction. An inline `python -` check of
this note and the review passed their relative links, final newlines,
display delimiters, whitespace, and control characters. The targeted
`git diff --check --` command for these two Markdown files also passed.
