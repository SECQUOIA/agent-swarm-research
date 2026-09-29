# Prior-art audit for general algebraic realization by convex quartics

Date: 2026-09-28. Status: scoped primary-source audit; publication priority
is not established. This note does not independently verify the general
construction's quantitative proof.

The sources examined below do not state the full realization theorem
under review. They do establish important ingredients: polynomial
convexification, positive definite Hessian Gram matrices, and large
algebraic degrees in quartic optimization. The proposed distinction must
therefore be the combined arithmetic realization, not any of those
ingredients separately. Failed searches do not establish novelty.

## Exact claim being compared

The candidate in
[the general quartic construction](general-strongly-convex-quartic-singleton.md)
and [the Hessian certificate construction](sos-convex-quartic-realization.md)
has the following scope. Given an irreducible rational polynomial of
degree $d>1$ with exactly one real root $\alpha$, construct a rational
quartic $F$ in $d-1$ variables such that

\[
 F^{-1}(0)=\{(\alpha,\alpha^2,\ldots,\alpha^{d-1})\},
 \qquad \nabla^2F(x)\succeq I\quad\text{on }\mathbb R^{d-1}.
\]

The output includes a rational SOS expression for $F$ and a positive
definite rational Gram matrix for
$y^{\mathsf T}\nabla^2F(x)y$ on the basis $(y,x\otimes y)$. The intended
algorithm and both certificates have polynomial bit complexity in the
dense rational input. Rational $\alpha$ is handled separately.

The degree of $F$ is fixed; its number of variables grows with $d$.
Its minimum is exactly the rational number zero. The positive definite
Gram matrix represents the Hessian biform, not $F$ itself. SOS-convexity
and an SOS representation of $F$ are separate properties.

The necessary field restriction is already discussed in
[the singleton field audit](singleton-field-characterization-prior-independent.md).
For an unconstrained rational strongly convex polynomial it also follows
directly from the gradient equations: the unique minimizer is the unique
real critical point, and every real embedding of its coordinate field
preserves those equations. The field therefore has exactly one real
embedding. This argument concerns actual real embeddings, not odd degree
alone. The candidate supplies a fixed-degree effective converse with
prescribed coordinates and rational minimum.

The explicit bivariate example and the comparison with Hesse's Redemption
and the 2026 Ahmadi–Hall work are handled in
[the explicit-example audit](convex-quartic-root-audit.md) and related
notes. They are not repeated here.

## Elementary baselines that weaken broader novelty claims

Ordinary rational SOS quartics already encode every one-real-root input
by a direct quadratic lifting. Write
$p(T)=T^d+\sum_{i=0}^{d-1}c_iT^i$, put $n=d-1$, and set $x_0=1$.
The quadratics

\[
 r_j=x_1x_j-x_{j+1}\quad(1\leq j<n),\qquad
 r_n=x_1x_n+\sum_{i=0}^{n}c_ix_i
\]

have the prescribed power point as their only common real zero.
Consequently $\sum_jr_j^2$ is already a polynomial-size rational SOS
quartic with that unique zero. This is an elementary reduction, not a
claim of a new result. It does not establish convexity: for $p(T)=T^3-2$,

\[
 G(x,y)=(x^2-y)^2+(xy-2)^2,
 \qquad
 \nabla^2G(0,0)=\begin{pmatrix}0&-4\\-4&2\end{pmatrix}
\]

is indefinite. Strong convexity and SOS-convexity are substantive extra
requirements.

Even a rational strongly convex univariate quartic can trivially have an
irrational minimizer when its minimum need not be rational. For example,
$h(t)=t^4+t^2+t$ has $h''(t)=12t^2+2\geq2$ and its derivative
$4t^3+2t+1$ is irreducible over $\mathbb Q$. At its unique root $a$,
$h(a)=a^2/2+3a/4$ is irrational: a rational value would give a quadratic
equation for the degree-three number $a$. Thus an irrational minimizer
alone is a substantially weaker target than the candidate.

## Primary sources examined

**Ahmadi, Chaudhry, and Zhang, Higher-Order Newton Methods with Polynomial
Work per Iteration (2023 preprint; v2 examined).** Read Sections 2–4,
especially Lemmas 2–3 and Theorem 3. Lemma 2 proves that
$\|x\|^2+\|x\|^{2k}$ is interior SOS-convex using a positive definite
Hessian Gram matrix and a Schur-complement argument. Lemma 3 and Theorem 3
justify SOS-convexifying a Taylor polynomial with positive definite
Hessian at its center by adding a sufficiently large centered even norm
power. For cubic Taylor polynomials this power is four. This is direct
prior for the Gram/interiority and regularization techniques.
[Primary text](https://arxiv.org/html/2311.06374v2).

The arithmetic gap remains. Centering at the prescribed irrational point
can introduce irrational coefficients. Centering at a rational point
generally changes the desired minimizer: the added term
$t\|x-c\|^4$ has gradient $4t\|a-c\|^2(a-c)$ at $a$, nonzero for $t>0$
and $a\ne c$. The inspected results do not supply the candidate's rational
vanishing space that permits perturbing coefficients while preserving
the zero exactly. Nor do their stated results prescribe arbitrary
one-real-embedding fields or the candidate's rational bit bounds.

**Zhu and Cartis, Sufficiently Regularized Nonnegative Quartic Polynomials
are Sum-of-Squares (2026, arXiv v1).** Read the introduction, the model
definition, Theorem 1.1, and Theorem 2.1 with its proof; inspected the
stated role of Theorem 2.3. Their model is a cubic plus
$\sigma\|s\|^4/4$. They study when subtracting its attained minimum yields
an SOS polynomial. Theorem 2.1 gives a sufficient matrix condition at a
stationary point and an SOS representation of the translated difference.
Theorem 1.1 recalls the preceding convexification work.
[Primary text](https://arxiv.org/html/2601.20418v1).

These are relevant quartic SOS constructions, but subtracting an unknown
minimum need not preserve rational coefficients. Their displayed SOS
certificate also depends on the stationary point. The inspected results
do not prescribe its coordinate field or retain a specified rational
zero level while regularizing. This comparison does not challenge their
algorithmic results; it separates the arithmetic output requirements.

**Nie and Ranestad, Algebraic Degree of Polynomial Optimization (2008
preprint).** Read the introduction and Section 3.1, including Example
3.1. The generic unconstrained degree bound for an objective of degree
$D$ in $n$ variables is $(D-1)^n$. Their four-variable quartic example
attains algebraic degree $81$. It is not globally convex: its displayed
$x_1^2$ coefficient is $-13$, so the Hessian at zero has a negative
diagonal entry. [Primary PDF](https://arxiv.org/pdf/0802.1233).

Generic algebraic degree counts complex critical points. It does not
give arbitrary prescribed fields, a rational minimum, or rational
convexity certificates. Large degree alone is nevertheless an
established phenomenon and should not be presented as the new feature.

**Bienstock, Del Pia, and Hildebrand, Complexity, exactness, and rationality
in polynomial optimization (2020 report).** Read the introduction and
Section 3, Example 1 and Observation 3. They give the rational cubic
$h(y)=2y_1^3+y_2^3-6y_1y_2+4$, which has unique minimizer
$(\sqrt[3]2,\sqrt[3]4)$ on the nonnegative orthant. Adding a rational box
and imposing $h\leq0$ gives an irrational singleton.
[Primary PDF](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf).

This is close prior for the exact cubic point and rational zero level.
The cubic is not globally convex or globally nonnegative; for example,
its Hessian at the origin is indefinite. The constraints and restricted
domain matter. This example is not a universal globally convex quartic
realization theorem.

**Kurdyka and Spodzieja, Convexifying positive polynomials and sums of
squares approximation (2015 preprint).** Theorem 5.5 and Corollary 5.7
were read in the preceding singleton audit. The former obtains strong
convexity by multiplying a polynomial bounded positively away from zero
by a sufficiently large power of $1+\|x\|^2$, under additional leading-form
conditions. The latter uses a positive perturbation for nonnegative
polynomials. [Primary PDF](https://arxiv.org/pdf/1507.06191).

The strict positivity hypothesis prevents direct application to the
desired zero. The perturbation changes zeros, and the multiplication
increases degree. These theorems therefore do not directly give the
candidate's fixed-degree zero-preserving result.

## Search scope and remaining uncertainty

The followup searched combinations of convex/strongly convex/SOS-convex
quartics with rational coefficients, irrational minima or zeros,
prescribed minima, algebraic numbers, number fields, one real embedding,
and universality. Representative literal queries included
`"convex polynomial" "number field"`,
`"polynomial" "one real embedding" convex`,
`"strongly convex" "prescribed" polynomial zeros`,
`"convex" "quartic" "Galois"`, and
`polynomial convexification "preserve" "minimizers" quartic`.
Citation following from Zhu–Cartis led to the particularly relevant
Ahmadi–Chaudhry–Zhang primary text.

Search results on convex quartic *regions* or determinant curves were
not treated as globally convex polynomial functions. Results on
homogeneous forms were not assumed to transfer by homogenizing a
nonhomogeneous convex polynomial. Search snippets and unavailable texts
were not counted as inspected theorems.

The conservative statement supported by this audit is: the inspected
primary sources establish neighboring constructions and several key
techniques, but none states the full rational, zero-preserving,
SOS-convex degree-four realization with prescribed one-real-conjugate
coordinates and polynomial bit bounds. This is a scoped comparison,
not proof of publication priority or exhaustiveness.

## Targeted verification

The elementary baseline calculations above were checked with SymPy:
the Hessian of $G$ at the origin is indefinite; $h'=4t^3+2t+1$ is
irreducible and has exactly one real root; reducing $h$ modulo $h'$
gives $t^2/2+3t/4$. The targeted commands actually run were a
`python - <<'PY'` block containing those exact SymPy assertions and a
trailing-whitespace check on this file, plus
`git diff --check -- research-20260927/general-quartic-realization-prior.md`.
All passed; because this is a newly added file, the direct whitespace
check was also used. No project-wide verification or CI inspection was run.
The general construction and its Hessian certificate require their
separate mathematical reviews.
