# Independent review of the common field for an algebraic SOCP witness

Date: 2026-09-28. Status: no unresolved gap found in the field-degree,
height, or representation argument reviewed here. This is an extension
and dependency review, not a novelty determination or a formal proof.

The proposed bound is valid for the unique minimum-norm point of a
nonempty affine SOCP over one explicitly represented real number field.
The whole point and the input field generator admit one rational univariate
representation of length \(N^{O(h+1)}\). A supplied box is unnecessary
for this encoding statement. An unknown auxiliary box can be removed from
the algebraic argument because its rows are eventually inactive.

The input field is \(K=\mathbb Q(\alpha)\), given by a dense irreducible
integer polynomial, a rational real-root isolator, and explicit power-basis
vectors for all coefficients. Its degree \(D\) is at most the total input
length \(N\). The parameter \(h\) is the span dimension over \(K\) of
the squared cone residual Hessians. All cone sign rows must be retained.
No statement here applies to separate succinct encodings of coefficients
whose joint field has not been supplied.

The reviewed dependencies are Sections 2.1--2.2 of
[the algebraic-threshold note](algebraic-threshold-misocp.md), Sections
2--5 of [the field-precision note](algebraic-coefficient-span-precision.md),
Sections 4--8 of [the nonconvex certificate note](nonconvex-hessian-span-frontier.md),
and the ordered coefficient-extraction proof in
[the optimizer note](ordered-perturbation-optimizer.md). The argument below
also independently checks the proposed simplification of the unknown-box
proof in [the attainment note](nonconvex-attainment-and-optimizer.md).

## 1. A single perturbation selects the minimum-norm point

Let \(C\) be the original nonempty closed feasible set. The function
\(\|x\|^2\) attains its minimum on \(C\): compare a minimizing sequence
with one feasible point and use compactness of a bounded subsequence.
Write this minimum as \(c^2\). All norm-minimizers lie in the closed
ball of radius \(c\). Their Hessian lifts

\[
w=(x,y)\in P,\qquad F_j(w)=\tfrac12x^TB_jx-y_j=0
\quad(1\le j\le h)
\]

therefore form a compact set. Choose an integer \(R\) such that this
whole set lies strictly inside \([-R,R]^{n+h}\). Neither \(R\),
\(c\), nor a norm-minimizer is encoded in the auxiliary algebraic
systems that will survive the limit.

Choose small integer-coefficient generic quadratic perturbations
\(P_0,\ldots,P_h\), using only affine charts of the original
polyhedron \(P\). For \(\eta>0\), minimize

\[
\|x\|^2+\eta P_0(w)
\]

over \(P\cap[-R,R]^{n+h}\) with
\(|F_j(w)+\eta^2P_j(w)|\le\eta\). One fixed exact norm-minimizer
is feasible for every sufficiently small \(\eta\). The perturbed
problem is compact. Every limit of its minimizers as \(\eta\downarrow0\)
is exactly feasible; uniform convergence of the objective and comparison
with that exact norm-minimizer give limiting norm \(c\).

All such limits lie strictly inside the auxiliary box. If boundary
minimizers existed for arbitrarily small \(\eta\), compactness would
give a boundary cluster point, a contradiction. Thus **all auxiliary box
rows are inactive for sufficiently small \(\eta\)**. This argument
works for every fixed finite perturbation tuple; it does not require its
coefficients or the eventual threshold to be uniform in \(R\).

Select a convergent sequence, then one active affine chart and one oriented
band support along a subsequence. The chart uses original rows only.
Its coefficients belong to \(K\) and have polynomial encoding length;
the unknown \(R\) occurs in none of them. A supplied original box,
if present, remains part of \(P\) and is included in the original input.

The genericity lemma supplies independent active nonlinear gradients,
an invertible multiplier Hessian, and an invertible bordered KKT matrix.
Both invertibility conditions are needed; independence of the gradients
alone would not justify the reduced nonsingularity assertion. At most one
orientation of each band is active, so the support has size \(s\le h\).
Adjugate substitution gives a nonsingular system in these \(s\)
multiplier variables, with degree \(a=N^{O(1)}\).

The selected sequence has one common limiting tuple. For an affine SOCP,
convexity makes its original-coordinate limit the unique minimum-norm
point \(x^*\). This uniqueness is used only for canonical selection.
The same encoding proof gives some norm-minimizer for a general nonempty
closed weak quadratic system, without convexity.

## 2. The relative degree bounds the entire optimizer field

Use the fixed chart, fixed support, and fixed primal subsequence above.
Let \(A\) be one common denominator for all coordinate outputs and
\(B_j\) the corresponding numerators. The selected roots have \(A\ne0\).
For every \(b=(b_1,\ldots,b_n)\in K^n\), replace the output numerator
by \(\sum_j b_jB_j\). This does not alter the reduced equations,
the chosen sequence, the limit \(x^*\), or the multiplier degree bound.
It can alter coefficient heights.

The field finite-quotient lemma gives a **nonzero** annihilator over
\(K\) of degree at most

\[
L=(a+1)^s
\]

for every \(\sum_jb_jx_j^*\). Each coordinate is consequently
algebraic over \(K\). Since the characteristic is zero, a
\(K\)-linear combination of these coordinates generates
\(E=K(x_1^*,\ldots,x_n^*)\). Applying the same degree bound to that
combination gives

\[
[E:K]\le L,\qquad [E:\mathbb Q]\le DL=:J.
\]

Multiplying separate coordinate degrees is unnecessary and would give a
weaker bound. More fundamentally, coordinate degree bounds alone do not
prove the displayed assertion: \(\sqrt2\) and \(\sqrt3\) each have
degree two over \(\mathbb Q\), but together generate degree four.
The uniform quantifier over linear combinations of one fixed tuple is
the essential extra fact.

The constant output \(\alpha\) belongs to \(K\). Adding a term
\(b_0\alpha\) to any output changes its numerator by \(b_0\alpha A\)
and does not increase the required multiplier degree. This observation
will supply an absolute primitive element containing the input generator.

No optimization assertion at another embedding is used. The perturbation
and compactness arguments operate at the selected real embedding. The
annihilators and field extensions are algebraic consequences of the
resulting fixed tuple.

## 3. Local heights remain polynomial in the explicit field input

The polynomial coefficient vectors of the reduced system include all
formal-parameter coefficients. At archimedean places use their coefficient
\(\ell_1\)-norms; at finite places use maximum coefficient norms.
The input's explicit representation gives polynomial Weil heights, and
fixed-count affine elimination and determinant substitution give averaged
logarithmic local norm budget \(E_0=N^{O(1)}\). This estimate uses
submultiplicative polynomial norms, not a sum of heights of all expanded
determinant monomials.

The finite-quotient determinant and coefficient extraction give an
annihilator \(P\in K[T]\) with

\[
\deg P\le L,\qquad
H_{\rm aff}(\operatorname{coeff}P)
\le L(a(s+1)+1)E_0+\log(L!)+L\log3=:W.
\]

For each coordinate \(\beta\), the local Cauchy bound and the product
formula yield \(h_{\rm W}(\beta)\le W+\log2\). Its absolute degree is
at most \(DL\), so its primitive integer minimal polynomial obeys

\[
\log\|p_\beta\|_\infty
\le DL(W+2\log2)=N^{O(h+1)}.
\]

This remains true when \(D\) grows: \(D\le N\), and products of a
fixed number of bounds of the form \(N^{C(h+1)}\) retain that form.
No normal closure is taken. Coefficient extraction over \(K\) cannot
create a zero final annihilator because each extraction takes the first
nonzero coefficient polynomial, before the next limiting operation.

The conventions for absolute heights and their independence of the
ambient field were checked against Silverman's
[2024 Arizona Winter School notes, Definitions 4.4--4.5 and Proposition 4.6,
printed pages 13--14](https://swc-math.github.io/aws/2024/2024SilvermanNotes.pdf).
The local Cauchy and determinant estimates are derived in the linked
field-precision note; those sources are not asserted to prove this SOCP
extension.

## 4. A short representation can include the input generator

Put \(e=[E:\mathbb Q]\le J\). Distinct embeddings of \(E\) disagree
on at least one member of \((\alpha,x_1^*,\ldots,x_n^*)\), because
these elements generate \(E\). Each pair therefore defines one proper
linear hyperplane of coefficient choices where their images of

\[
\gamma=c_0\alpha+\sum_{j=1}^n c_jx_j^*
\]

coincide. A grid with each \(c_j\in\{0,\ldots,\binom J2\}\)
contains a point outside all \(\binom e2\) hyperplanes. Indeed, each
hyperplane meets at most one grid point after all but one coefficient
are fixed, and a union bound is strictly smaller than the whole grid.
The resulting \(\gamma\) has \(e\) distinct embedding images and
generates \(E/\mathbb Q\). The case \(J=1\) permits \(\gamma=0\),
which generates \(\mathbb Q\).

The coefficient bit lengths are \(O(\log J)=O((h+1)\log N)\).
Applying the same output-height argument with numerator
\(c_0\alpha A+\sum_jc_jB_j\) gives a minimal polynomial for
\(\gamma\) of degree at most \(J\) and coefficient bits
\(N^{O(h+1)}\). Its intended real root has a rational isolating interval
of polynomial length in these bounds, by root separation for a squarefree
integer polynomial.

For completeness, the coordinate expressions also have short coefficients.
Multiply \(\gamma\) and each desired element
\(\beta\in\{\alpha,x_1^*,\ldots,x_n^*\}\) by the leading
coefficients of their primitive minimal polynomials to obtain algebraic
integers \(A_0\) and \(B_0\). Their conjugate magnitudes are bounded
by \(2^{\operatorname{poly}(J,H)}\), where \(H=N^{O(h+1)}\)
bounds the polynomial coefficient bits. Write
\(B_0=\sum_{r=0}^{e-1}d_rA_0^r\) and take traces after multiplying
by \(A_0^s\), for \(0\le s<e\). The resulting integer matrix has
entries \(\operatorname{Tr}(A_0^{r+s})\), and the right-hand side has
entries \(\operatorname{Tr}(B_0A_0^s)\). Its entries have
\(\operatorname{poly}(J,H)\) bits. The trace pairing is nonsingular
because \(E/\mathbb Q\) is separable and the powers of \(A_0\)
form a basis. Cramer's rule, then scaling back, gives each desired element
as a degree-below-\(e\) rational polynomial in \(\gamma\), with
\(\operatorname{poly}(J,H)\) coefficient bits.

There are at most \(N+1\) desired elements. The complete representation
therefore has length \(N^{O(h+1)}\), and explicitly includes \(\alpha\).
Its input-field isolator can consequently be checked in the same selected
real embedding as every original cone sign and squared residual. This is
an existence and size argument; it does not by itself provide a witness
recovery algorithm or an efficient search of the primitive-element grid.

## 5. Adversarial and exact checks

A separate subreviewer independently verified the primitive-element
implication and the integer-grid bound. Their checks emphasized that
the annihilator must be nonzero and that the tuple cannot change with
the linear combination. Separability is substantive: the analogous
assertion fails for some purely inseparable extensions in positive
characteristic. Number fields satisfy the required hypothesis.

An exact inline SymPy check used \(K=\mathbb Q(\sqrt2)\),
\(\beta=2^{1/4}\), and \(\gamma=\sqrt2+\beta\). It verified
irreducibility of

\[
p_\gamma(T)=T^4-4T^2-8T+2,
\]

and the identities, modulo this polynomial,

\[
\beta=\frac{2\gamma^3-\gamma^2-3\gamma-10}{9},\qquad
\sqrt2=\frac{-2\gamma^3+\gamma^2+12\gamma+10}{9}.
\]

The command computed the resultant of \(X^4-2\) and
\(T-X-X^2\), inverted \(2T+1\) modulo the resultant, and asserted
the fourth-power, square, and sum identities. This checks one nontrivial
relative-to-absolute field representation. It does not verify the
universal perturbation, height, or complexity bounds.

A targeted inline Python document check passed for the final newline,
trailing whitespace, control characters, paired math delimiters, and all
five local Markdown links. These checks concern document integrity only.

The mathematical review found no gap in the proposed extension. It relies
on the previously reviewed effective genericity and finite-quotient lemmas;
it does not replace their full proofs. No Lean formalization,
project-wide verification, CI inspection, or priority claim is asserted.
