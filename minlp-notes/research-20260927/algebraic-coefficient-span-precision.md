# Sharper precision bounds over one number field

Date: 2026-09-27. Status: theorem argument; independent adversarial review
and a separate root-agent proof review found no unresolved gap. This note
sharpens the arithmetic step in the
[quantitative Hölder proof](hessian-span-holder-height-review.md). It does
not introduce a new elimination method or a new theory of heights.

The finite-quotient construction in the
[explicit elimination note](explicit-span-separation.md) works directly
over a number field. Tracking a joint coefficient norm at each place avoids
first encoding the field by a quantified primitive element. The consequence
is a stronger bound on a nonzero optimum or a terminal Slater margin: the
number-field degree and coefficient height enter linearly, outside the
exponent that depends on the Hessian span.

## 1. Quantitative statement

Fix a real embedding of a number field \(K\), and put
\(D=[K:\mathbb Q]\). Consider convex quadratic inequalities and affine
constraints, together with a convex quadratic objective, all with
coefficients in \(K\). Convexity is required at the fixed embedding only.
Suppose the feasible set is nonempty and the finite optimum \(\theta\)
is attained. Let \(S\ge2\) bound the number of variables, constraints,
and explicitly listed scalar input coefficients, and suppose every input
coefficient has absolute logarithmic Weil height at most \(B\ge1\).
Let \(h\) be the dimension over \(K\) of the span of the native
constraint Hessians; the objective Hessian is excluded. This dimension
equals the real span dimension at the fixed embedding, by the minor
criterion for matrix rank.

There is an absolute constant \(c\) such that

\[
 \begin{split}
 [K(\theta):K]&\le(2n+1)^{\min(h,n)},\\
 h_{\rm W}(\theta)&\le(B+1)S^{c(h+1)},\\
 \theta\ne0\quad\Longrightarrow\quad
 |\log|\theta||&\le D(B+1)S^{c(h+1)}.                 \tag{1}
 \end{split}
\]

The primitive integer minimal polynomial of \(\theta\) has degree at
most \(D(2n+1)^{\min(h,n)}\) and coefficient bit length at most
\(D(B+1)S^{c(h+1)}\), after increasing the same absolute constant.
Thus the exponent of \(D\) or \(B+1\) does not grow with \(h\).
The same height and selected-embedding magnitude bounds hold for each
coordinate of the minimum-norm optimizer. All its coordinates, together
with \(\theta\), generate an extension of \(K\) of degree at most
\((2n+1)^{\min(h,n)}\).

If the Hessian bound holds only after restriction to the affine hull of
the polyhedron, first take a free-coordinate affine chart over \(K\).
This incurs only an absolute polynomial factor in \(S\), and a linear
factor in \(B+1\), in the height bounds. The conclusions remain valid
with adjusted absolute constants.

For the terminal min-max problem in the Hölder proof, the original
polyhedron is bounded, so attainment is automatic. With \(m\ge1\) and
a common strict point, put

\[
 \theta=\min_{x\in P}\max_i q_i(x)<0.
\]

The epigraph adds one variable and affine objective and does not increase
the native Hessian span. A minimizer supplies a margin
\(\sigma=\min(1,|\theta|)\) satisfying

\[
 \log(1/\sigma)\le D(B+1)S^{c(h+1)}.                 \tag{2}
\]

No coordinate bound or epigraph bound needs to be added for this argument:
the epigraph optimum is already finite and attained. The statement is an
existence and encoding bound, not an implemented algorithm for manipulating
the field or computing a Slater point.

## 2. Joint local norms

Use absolute values \(|\cdot|_v\) on \(K\), with local weights
\(n_v=[K_v:\mathbb Q_v]\), normalized by the product formula. At a
complex place use the ordinary complex modulus and weight two. For a
finite coefficient vector \(c\), define its affine joint height by

\[
 H_{\rm aff}(c)=\frac1D\sum_v n_v
                  \log\max(1,\max_j|c_j|_v).
                                                               \tag{3}
\]

It is the projective height of \([1:c]\). It is unchanged on extension
of the ambient field, and it is at most \(\sum_j h_{\rm W}(c_j)\).
The use of a joint vector is essential: separately bounding every term
in a determinant and then summing their heights would give an unnecessary
factorial loss.

For a polynomial over \(K\), use the coefficient \(\ell_1\)-norm
at archimedean places and the maximum coefficient norm at other places.
Both are submultiplicative; at non-archimedean places the latter also obeys
the ultrametric triangle inequality. For a collection of polynomials
\(G_1,\ldots,G_s,A,B\), let \(C_v\) be the maximum of one and
these polynomial norms, and set

\[
 E=\frac1D\sum_v n_v\log C_v.                         \tag{4}
\]

If the combined coefficient vector is \(c\), and each polynomial has
at most \(M\ge1\) monomials, then

\[
 E\le H_{\rm aff}(c)+\log M.                         \tag{5}
\]

The archimedean local weights sum to \(D\). There is no contribution
of \(\log M\) at non-archimedean places.

## 3. The finite-quotient lemma over \(K\)

Let \(G_1,\ldots,G_s,A,B\in K[t_1,\ldots,t_r,\lambda]\)
have multiplier degree at most \(a\ge1\). Assume the nonsingular-root,
nonzero-denominator, and finite ordered-limit hypotheses of the
[ordered-perturbation lemma](ordered-perturbation-optimizer.md#5-elimination-with-ordered-coefficient-parameters),
with a fixed finite number of coefficient parameters. For the application
here there are two, whose order of limits is fixed. Put

\[
 L=(a+1)^s,\qquad T=a(s+1),\qquad
 W=L(T+1)E+\log(L!)+L\log3.                           \tag{6}
\]

There is a nonzero \(P\in K[w]\) annihilating the selected finite
limit \(\theta\), with

\[
 \deg P\le L,\qquad H_{\rm aff}(\operatorname{coeff}P)\le W.
                                                               \tag{7}
\]

To prove the arithmetic assertion, deform
\(G_i\) to \(G_i+\beta\lambda_i^{a+1}\). The quotient basis
consists of monomials whose individual multiplier exponents are below
\(a+1\); it has size \(L\). A basis monomial times \(A\) or
\(B\) has total multiplier degree at most \(T\). Each reduction
strictly decreases that degree. Consequently, after multiplication by
\(\beta^T\), both multiplication matrices have polynomial entries,
each with local coefficient norm at most \(C_v^{T+1}\).

At an archimedean place this follows by summing the absolute coefficients
in the reduction tree. A branch has at most \(T\) replacements, and
each replacement increases that sum by at most \(C_v\). At a
non-archimedean place term collection and branching use maxima, so the same
bound holds without any branching-count factor.

Introduce \(\zeta\) and form

\[
 H=\det\bigl(w\beta^T M_A-\beta^T M_B
                                  -\zeta\beta^T I_L\bigr).  \tag{8}
\]

Its leading \(\zeta\) coefficient is \((-\beta^T)^L\), so it
is nonzero. At an archimedean place,

\[
 \|H\|_v\le L!\,3^L C_v^{L(T+1)};
\]

at a non-archimedean place,

\[
 \|H\|_v\le C_v^{L(T+1)}.                            \tag{9}
\]

The norms in (9) apply to all coefficient parameters as indeterminates.
They do not involve the values or magnitudes of those parameters.

The algebraic and real-limit parts of the existing lemma apply verbatim
over \(K\) at the fixed real embedding: take the first nonzero
\(\zeta\) coefficient, then the first nonzero deformation coefficient,
and then the first nonzero coefficient of each original parameter in the
required inner-to-outer order. Nonsingularity continues the selected root
under the deformation. The nonzero denominator ensures that extracting
the lowest \(\zeta\) coefficient removes permanent undefined-value
factors without losing that branch. The ordered finite limits then give
\(P(\theta)=0\). None of these steps assumes nonsingularity of other
components or bounded multipliers.

Every extraction selects a subvector of coefficients. Thus it cannot
increase any local norm or the affine joint height. Summing the logarithms
of (9) proves (7). No normal closure, field norm, or primitive-element
representation is needed. Other field embeddings need not preserve any
optimization property; they are used only to measure coefficients.

## 4. From a polynomial over \(K\) to numerical separation

Write \(P(w)=p_m w^m+\cdots+p_0\), with \(p_m\ne0\). Its
projective coefficient height satisfies

\[
 H_{\rm proj}(P)=\frac1D\sum_v n_v\log\max_i|p_i|_v
 \le H_{\rm aff}(\operatorname{coeff}P)\le W.        \tag{10}
\]

At every place of an extension containing a root, the Cauchy root bound
gives

\[
 \max(1,|\theta|_v)
 \le c_v\max_i|p_i/p_m|_v,
 \qquad
 c_v=\begin{cases}2,&v\text{ archimedean},\\1,&\text{otherwise}.
 \end{cases}
\]

The maximum on the right includes \(p_m/p_m=1\). The product formula
for \(p_m\), followed by summation of these bounds, proves

\[
 h_{\rm W}(\theta)\le H_{\rm proj}(P)+\log2\le W+\log2.
                                                               \tag{11}
\]

Also \([K(\theta):K]\le m\le L\), hence the rational degree is
at most \(DL\). The primitive integer minimal polynomial \(p_\theta\)
of rational degree \(e\) satisfies

\[
 \log\|p_\theta\|_\infty
 \le e\,h_{\rm W}(\theta)+e\log2
 \le DL(W+2\log2).                                  \tag{12}
\]

Here \(\log M(p_\theta)=e h_{\rm W}(\theta)\), and expansion in
the roots bounds every coefficient by \(2^e M(p_\theta)\).

For numerical separation, a stronger estimate avoids the extra factor
\(L\) in (12). Suppose \(\theta\ne0\), remove powers of \(w\)
from \(P\), and rename the remaining constant term \(p_0\ne0\).
For any two nonzero coefficients,

\[
 h_{\rm W}(p_i/p_j)\le H_{\rm proj}(P)\le W.
\]

At the fixed real embedding, every \(\gamma\in K^*\) satisfies
\(|\log|\gamma||\le D h_{\rm W}(\gamma)\). Apply the ordinary
Cauchy bound to \(P\) and to its reversal. This gives

\[
 |\log|\theta||\le D W+\log2.                      \tag{13}
\]

This step is why the field degree enters linearly. The polynomial need
not be irreducible, and \(K\) need not be normal over \(\mathbb Q\).

## 5. Arithmetic of the convex-quadratic reduction

The active affine restriction and ordered regularization in the
[optimizer note](ordered-perturbation-optimizer.md) use only linear
algebra over the input field and convex analysis at its chosen embedding.
They therefore apply over \(K\). At the attained minimum-norm
optimizer, retain active inequalities, turn active affine rows into
equalities, and impose the affine differences between active quadratics
and a basis of their Hessians. This preserves the lexicographic minimum
of the objective and original-coordinate squared norm. A free-coordinate
chart \(x=x_0+Vu\) leaves whole constraint polynomials spanning at
most \(h\) dimensions.

Only a fixed number of linear-algebra stages occurs: computing Hessian
dependences, forming the resulting affine equations, and computing an
affine chart. If restriction to the initial polyhedral affine hull is
needed, it adds one more stage. Each matrix has dimension bounded by an
absolute polynomial in \(S\), and the total number of its entries is
bounded by another such polynomial. Cramer's rule gives the height bound

\[
 h_{\rm W}(\det M)
 \le r\sum_{i,j}h_{\rm W}(M_{ij})+\log(r!)
\]

for an \(r\times r\) matrix. The bound follows from the local maximum
of its entries and the determinant expansion. Inverses use the same
bound, by invariance of height under reciprocation. Products and finite
sums in each stage preserve linear dependence on the preceding height
bound. It follows that the restricted quadratic coefficients, \(x_0,V\),
and the coefficients of \(\|x_0+Vu\|^2\) all have height

\[
 B'\le S^{c_0}(B+1),                                \tag{14}
\]

for an absolute \(c_0\); their number is at most \(S^{c_0}\).
There is no iteration of this coefficient growth once per multiplier.

Minimize the objective plus \(\varepsilon\|x_0+Vu\|^2\) on the
exact restricted feasible set, and then relax all remaining rows by
\(\delta>0\). Take \(\delta\downarrow0\) for each fixed
\(\varepsilon>0\), followed by \(\varepsilon\downarrow0\).
Strict convexity gives the inner convergence; comparison with the
minimum-norm exact optimizer gives the bounded outer sequence. Minimal
active-gradient support fixes at most \(s\le\min(h,d)\) independent
gradients along nested subsequences, where \(d\le n\) is chart
dimension. The selected multiplier Jacobian is negative definite, exactly
as in the linked proof.

The adjugate KKT polynomials have multiplier degree \(a=2d\). Use
\(A=\Delta^2\) and either an objective numerator or an
original-coordinate numerator \((x_{0j}\Delta+(Vp)_j)\Delta\).
The same ordered limits give \(\theta\) or the selected coordinate.

For completeness, their joint local norm budget (4) is polynomial in
\(S\) and linear in \(B+1\), even though the expanded polynomials
can have many monomials. Let \(U_v\ge1\) be the maximum magnitude of
the finitely many scalars in (14), explicitly including the regularizer
Hessian \(2V^TV\), its linear vector \(2V^Tx_0\), and the constants
\(2\) and \(1/2\). These additional entries satisfy the same polynomial
height and count bounds. Then

\[
 \frac1D\sum_v n_v\log U_v\le S^{c_1}(B+1).        \tag{15}
\]

At an archimedean place, each entry of the KKT matrix and linear vector
has polynomial coefficient norm at most \((S+2)U_v\). Thus its
determinant and every adjugate-vector coordinate have norm at most
\(d!((S+2)U_v)^d\). At a non-archimedean place the corresponding
bound is \(U_v^d\). Forming each cleared active constraint, objective
numerator, or coordinate numerator uses only polynomially many additions
and products of at most two such determinant-size expressions and a
bounded number of scalars. Consequently the \(C_v\) for the KKT
polynomials satisfy

\[
 \log C_v\le
 \begin{cases}
 (2d+3)\log U_v+O(d\log(S+2)),&v\text{ archimedean},\\
 (2d+3)\log U_v,&v\text{ otherwise}.
 \end{cases}
\]

After summing, this yields

\[
 E\le S^{c_2}(B+1).                                 \tag{16}
\]

Substitute (16) into (6). Since \(L=(2d+1)^s\), \(T=2d(s+1)\),
and \(s\le h\), equations (11)--(13) prove all the scalar bounds
in (1). The cases \(d=0\) and \(s=0\) give points over \(K\)
and degree-one equations directly.

For the joint optimizer field, use the same fixed nested support for every
coordinate and every \(K\)-linear combination of them. Changing that
linear combination changes coefficient heights but never the degree
bound \(L\). The primitive element theorem in characteristic zero
provides a \(K\)-linear combination generating the joint coordinate
extension, so its degree over \(K\) is at most \(L\). The objective
value belongs to that same field.

## 6. Consequence for the Hölder constant

The existing quantitative facial-reduction proof fixes one field with
\(D\le N^{O(h+1)}\), keeps every face coefficient in that field with
height \(B\le N^{O(h+1)}\), and uses only polynomially many scalar
coefficients, \(S\le N^{O(1)}\). Its Hoffman constants and curved-step
constants already have logarithms bounded by \(N^{O(h+1)}\).
Equation (2) replaces the terminal-margin estimate and gives

\[
 \operatorname{dist}(x,F)\le C v(x)^{2^{-h}},\qquad
 \log_2\max(1,C)\le N^{O(h+1)}.                     \tag{17}
\]

The original constant assembly has at most \(m+h\) steps and adds their
logarithmic bounds, so it preserves this improvement. This conclusion
depends on the independently reviewed geometric and common-field facial
arguments in the linked Hölder note. This note checks their arithmetic
terminal step; it does not independently reprove all those arguments.

The exponent \(2^{-h}\) is unchanged. The improvement concerns a
uniform bound on the constant and hence the precision needed by possible
certification or penalty constructions. It does not establish a practical
numerical speedup.

## 7. Sources and verification limits

Absolute and projective heights, the product formula, and independence of
the ambient number field were checked against Joseph H. Silverman's
[2024 Arizona Winter School notes, Definitions 4.4--4.5 and Proposition 4.6,
printed pages 13--14](https://swc-math.github.io/aws/2024/2024SilvermanNotes.pdf).
That section also relates minimal-polynomial coefficients to root heights.
The local Cauchy estimates and determinant bounds used here are derived
explicitly above from these standard definitions. Their use is not a
novelty claim.

The finite staircase quotient, multiplication matrices, deformation, and
ordered coefficient extraction are inherited from the two linked
elimination notes and their prior comparisons with Canny and
Grigoriev--Pasechnik. The contribution of this note is the precision
refinement for the current Hessian-span argument. We do not claim that
direct arithmetic elimination over number fields is new, or that the
displayed constants or degree bound are sharp.

A further primary-source check examined Krick--Pardo--Sombra,
[*Sharp estimates for the arithmetic Nullstellensatz*, introduction and
Section 1.1](https://arxiv.org/pdf/math/9911094), especially printed pages
5--7. They explicitly extend their arithmetic results to number fields
without field-dependent height bounds, and organize coefficient estimates
through local heights. Their problem is an arithmetic Nullstellensatz,
whereas this note retains a selected finite limit of a convex KKT system.
This comparison reinforces that local number-field arithmetic is established
machinery; the present refinement is its application after Hessian-span
compression, with the particular ordered-limit argument proved above.

The [independent review](algebraic-coefficient-span-review.md) checks the
full saved argument, including the linear dependence on \(D\) and
\(B\), the ordered limits over one real embedding, the common optimizer
field, and the epigraph application. The reviewer requested that the local
input norm explicitly include the regularizer Hessian and linear vector;
the saved proof now does so. A separate root-agent reread independently
checked the local reduction and determinant norms, coefficient extraction,
both Cauchy bounds, fixed-count affine arithmetic, and the final composition
of constants, and found no gap.

A targeted inline Python command checked this note's final newline,
trailing whitespace, control characters, paired math delimiters, and all
relative Markdown links. These document checks passed; they do not verify
the mathematical theorem. No numerical calculation or Lean formalization
is asserted to establish the universal bound. No project-wide verification
or CI inspection was performed.
