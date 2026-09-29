# A sharper algebraic degree bound from the Hessian span

Date: 2026-09-27. Status: complete proof; independent adversarial review
and targeted exact checks found no gap. This note applies classical
multihomogeneous Bezout theory. It
does not claim a new root-counting theorem.

Let a rational convex quadratic program in `n` continuous variables have
a nonempty feasible set and an attained finite optimal value. Let `h` be
the dimension of the linear span of its native constraint Hessian matrices;
the objective Hessian is excluded. Define

\[
 \mathcal B(n,h)=
 \max_{0\le s\le\min(h,n)}2^s\binom ns.                    \tag{1}
\]

The value-degree argument below proves that the optimal value has algebraic
degree at most \(\mathcal B(n,h)\), without Slater's condition or an assumption
that the complete complex KKT system is zero-dimensional. Combining the
same argument with the ordered perturbation construction proves the stronger
statement

\[
 [\mathbb Q(x_1^*,\ldots,x_n^*):\mathbb Q]
       \le \mathcal B(n,h),                                \tag{2}
\]

where `x*` is the unique minimum Euclidean norm optimizer. The objective
value belongs to this same field. The ordered perturbation construction
and its convergence proof are documented separately in
[the optimizer note](ordered-perturbation-optimizer.md); the degree argument
here states precisely the hypotheses it uses from that construction.

The [sharpness note](multihomogeneous-degree-sharpness.md) proves that the
bound is attained by both the value and the joint optimizer field for every
admissible pair `n,h`, even with positive definite Hessians, strict
feasibility, and a compact feasible set. Its proof uses the classical
generic degree and Hilbert irreducibility; it supplies no useful coefficient
size bound for those examples.

For the actual selected KKT support of size `s` after rational affine
elimination to dimension `d`, the stronger bound is
\(2^s\binom ds\). The maximum in (1) is necessary when the support is
unknown: \(2^s\binom ns\) can decrease with `s`. For example, when
`n=h=3`, the support sizes two and three give bounds 12 and 8. A maximizing
index is

\[
 s_*=\min\!\left(h,\left\lfloor\frac{2n+1}{3}\right\rfloor\right).
\]

Thus \(\mathcal B(n,h)\le3^n\), and it is polynomial in `n` for fixed `h`.
The conventions \(\binom00=1\) and an empty support cover `n=0` and `h=0`.

## 1. Regular roots in a parameterized polynomial system

The specialization step needs care. Counting roots of every individual
rational specialization does not by itself bound the degree of a limit:
even rational numbers can converge to a transcendental number. We instead
construct one polynomial identity over the entire parameter space.

Let \(t=(t_1,\ldots,t_p)\), let \(y=(y_1,\ldots,y_m)\), and suppose

\[
 F_1,\ldots,F_m,A,C\in\mathbb Q[t,y],\qquad
 D(t,y)=\det(\partial F_i/\partial y_j).
\]

Assume a uniform multihomogeneous Bezout bound `B` for the number of
isolated common roots of `F` over an algebraic closure of
\(K=\mathbb Q(t)\). A regular root means `F=0` and `D` nonzero.

**Parameter lemma.** If at least one real specialization has a regular root
with `A` nonzero, there is a nonzero polynomial
\(R\in\mathbb Q[t,w]\), of degree at most `B` in `w`, such that

\[
 R(t,C(t,y)/A(t,y))=0                                      \tag{3}
\]

at every real specialized regular root at which `A` is nonzero. The full
complex common-zero set may have additional positive-dimensional components.

**Proof.** Consider the localized algebra

\[
 E=K[y,1/(DA)]/(F_1,\ldots,F_m).                           \tag{4}
\]

Over an algebraic closure of `K`, every point of (4) has invertible
Jacobian. The Jacobian criterion makes each such point reduced and
zero-dimensional. An affine algebraic set has finitely many irreducible
components, so this open set consists of finitely many isolated reduced
points. Consequently `E` is either zero or a finite reduced `K`-algebra.
In the latter case its dimension `r` is the number of these points, hence
\(r\le B\). Localization removes every positive-dimensional component:
none can contain a point with an invertible square Jacobian.

Here `E` cannot be zero. A real regular root with `A` nonzero extends,
by the implicit function theorem, to a real analytic root for all
parameters in a neighborhood. If (4) were zero, the identity `1=0` in
that localization, after clearing its finitely many parameter denominators,
would rule out such roots outside the zero set of one nonzero polynomial
in `t`. That zero set contains no real open neighborhood.

Multiplication by the class of `C/A` on the `r`-dimensional vector space
`E` has a monic characteristic polynomial
\(\chi(w)\in K[w]\) of degree `r`. Cayley--Hamilton gives
\(\chi(C/A)=0\) in `E`. Clear the coefficient denominators to obtain a
nonzero \(R(t,w)\in\mathbb Q[t,w]\), with \(\deg_wR=r\le B\).
The algebra identity, with its finitely many denominators cleared, shows
(3) at all specialized regular roots with `A` nonzero outside the zero
set of some nonzero parameter polynomial `e(t)`.

Finally fix any specialized regular root with `A` nonzero, including a
parameter value with `e(t)=0`. The implicit function theorem supplies a
nearby analytic branch, along which both `D` and `A` remain nonzero.
Parameter points with `e(t)` nonzero are dense in that neighborhood.
Equation (3) holds there and extends to the fixed root by continuity.
This proves (3) without excluding any regular specialized root. \(\square\)

The proof also works for no parameters. It uses only the existence of the
characteristic polynomial, not an algorithm to construct it. In particular,
this lemma supplies no coefficient-height estimate.

## 2. Limits in a prescribed order

For one parameter, suppose regular roots at nonzero
\(\varepsilon_\nu\to0\) have output \(w_\nu\to w^*\). Write the
polynomial from (3) as

\[
 R(\varepsilon,w)=\varepsilon^a P(w)+O(\varepsilon^{a+1}),
 \qquad P\ne0,
\]

using the smallest power of `epsilon` with a nonzero coefficient.
Dividing by \(\varepsilon_\nu^a\) and passing to the limit proves
\(P(w^*)=0\), with \(\deg P\le B\).

For two parameters, suppose there are nonzero
\(\varepsilon_\nu\to0\), and for each `nu` nonzero
\(\delta_{\nu,j}\to0\), such that regular selected roots have outputs

\[
 w_{\nu,j}\longrightarrow w_\nu\quad(j\to\infty),
 \qquad w_\nu\longrightarrow w^*\quad(\nu\to\infty).
                                                               \tag{5}
\]

All limits in (5) are finite. First take the lowest nonzero coefficient
of `delta` in \(R(\varepsilon,\delta,w)\):

\[
 R=\delta^a S(\varepsilon,w)+O(\delta^{a+1}),\qquad S\ne0.
\]

At each fixed \(\varepsilon_\nu\), division and the inner limit give
\(S(\varepsilon_\nu,w_\nu)=0\). This remains true if specialization
makes all coefficients of `S` zero. Now take the lowest nonzero coefficient
of `epsilon` in `S`; division and the outer limit give a nonzero
\(P\in\mathbb Q[w]\) with \(P(w^*)=0\) and \(\deg P\le B\).
Clearing rational denominators makes `P` integral if desired.

There is no need for a quantitative rule relating the two parameters,
bounded multipliers, or nonsingularity at the limiting point.

## 3. Apply the lemma to full KKT equations

Use the native active affine restriction from
[the Hessian-span proof](hessian-span-reduction.md), with rational coordinates
\(x=x_0+Vu\), `d` free variables, and whole native constraint polynomials
spanning a space of dimension at most `h`. For the optimizer conclusion,
the restriction must preserve the lexicographic pair
\((q_0(x),\|x\|^2)\); this is the version established in the ordered
perturbation note. The following argument also applies directly to the
single-parameter value construction of
[the explicit elimination note](explicit-span-separation.md).

For the two-parameter construction use objective
\(q_0(x_0+Vu)+\varepsilon\|x_0+Vu\|^2\), with native inequalities
\(q_i(x_0+Vu)\le\delta\). Select a minimal nonnegative representation
of the negative objective gradient by gradients of active native rows.
Its support `J` has size \(s\le\min(h,d)\), positive multipliers, and
linearly independent gradient columns. For notational simplicity write
the restricted polynomials again as
\(q_i(u)=\tfrac12u^TQ_i u+a_i^Tu+c_i\). The equations in `u,lambda` are

\[
 \begin{aligned}
 F^{\rm stat}(u,\lambda)
   &=\nabla q_0(u)+2\varepsilon V^T(x_0+Vu)
                     +\sum_{i\in J}\lambda_i\nabla q_i(u)=0,\\
 F^{\rm act}_i(u,\lambda)&=q_i(u)-\delta=0\quad(i\in J).
 \end{aligned}                                               \tag{6}
\]

There are `d+s` equations in `d+s` variables. At every selected root
their Jacobian is

\[
 \begin{pmatrix}M&G\\G^T&0\end{pmatrix},\qquad
 M=Q_0+2\varepsilon V^TV+\sum_{i\in J}\lambda_iQ_i,
 \quad G=(\nabla q_i)_{i\in J}.                             \tag{7}
\]

Because `V` has full column rank and \(\varepsilon>0\), `M` is positive
definite. The columns of `G` are independent. The Schur complement
\(-G^TM^{-1}G\) is therefore negative definite. Thus (7) is invertible,
including `s=0` with an empty lower block.

Treat `u` and `lambda` as separate variable blocks. Each of the `d`
stationarity equations has block degrees at most `(1,1)`; each of the
`s` active equations has block degrees at most `(2,0)`. The classical
multihomogeneous Bezout bound for their isolated complex roots is

\[
 [U^dL^s](U+L)^d(2U)^s=2^s\binom ds.                       \tag{8}
\]

One may homogenize in the two blocks using these upper degrees. Every
regular affine root remains an isolated root in its affine chart; other
roots or positive-dimensional components in the product of projective
spaces do not invalidate the isolated-root upper bound.

For the value result, fix a support occurring along the sequence in the
single-parameter proof and apply Sections 1--2 to its regularized objective
output. This gives degree at most (8).

For the optimizer result, the ordered perturbation construction gives the
following stronger data. For each outer \(\varepsilon_\nu\), its inner
minimizers converge as \(\delta\to0\) to the unique minimizer of
\(q_0+\varepsilon_\nu\|x\|^2\) on the retained feasible set. These
outer minimizers converge to `x*`. There are finitely many supports: for
each outer index select an inner subsequence with a constant support, and
then select an outer subsequence with that same support `J`. This choice
is made before choosing the output.

For any \(c\in\mathbb Q^n\), use polynomial output
\(c^T(x_0+Vu)\), so `A=1` in the parameter lemma. The ordered limits
give degree at most (8) for \(c^Tx^*\). In particular all coordinates
are algebraic. A finite extension of `Q` generated by finitely many
algebraic numbers has a primitive element that is a rational linear
combination of those numbers. Applying the same bound to that combination
proves the joint field degree bound (2).

If `d=0`, the rational affine chart contains only one point, giving degree
one directly. Since `d` is at most `n`, (8) is at most (1). The proof does
not assert that every point of a positive-dimensional optimal face has
bounded algebraic degree: that face can contain transcendental points.
The minimum norm optimizer is the fixed canonical selection used here.

## 4. Coefficient heights and mixed-integer fibers

This degree argument does not replace the coefficient-height proof in
the explicit elimination and ordered perturbation notes. Those arguments
produce coordinate annihilators of degree and coefficient bit length
\(N^{O(h+1)}\). The primitive integer minimal polynomial of a coordinate
divides its height-controlled annihilator. A standard integer factor-height
bound therefore gives coefficient bit length \(N^{O(h+1)}\) for that
minimal polynomial as well, while Sections 1--3 improve its degree to
at most (1). It is not necessary for the same elimination construction
to supply both optimal bounds.

If a rational mixed-integer convex quadratic problem has an attained finite
optimum, fix an optimal integer assignment. Its continuous fiber has
rational coefficients, continuous dimension `n`, and Hessian span at most
`h`. The optimal value and a minimum norm continuous optimizer of this
fiber consequently lie in a field of degree at most (1), independently
of the number or magnitude of integer variables. A uniform coefficient
height bound still needs control of the assignment's bit length. The
[unbounded mixed-integer theorem](mixed-integer-attainment-frontier.md)
provides such control when the integer dimension and `h` are fixed.

## 5. Prior results, significance, and verification scope

[Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*,
Theorem 2.2, Corollary 2.5, and Section 3.2](https://arxiv.org/abs/0802.1233)
give the generic QCQP count \(2^s\binom ds\). Their stated nongeneric
extension assumes a zero-dimensional complete KKT system. The isolated-root
multihomogeneous bound used in (8) already allows additional components;
an accessible primary statement is
[Dedieu, Malajovich, and Shub, *On the Curvature of the Central Path of
Linear Programming Theory*, Section 5, Theorem 5.1](https://arxiv.org/abs/math/0312083),
which credits Morgan and Sommese. The separate
[prior audit](multihomogeneous-degree-prior.md) records the exact comparison.

The contribution within this research package is the use of native Hessian
span, active affine restriction, canonical ordered perturbations, and one
polynomial identity valid at all regular parameter specializations. Those
steps bring the classical count into a nongeneric convex setting with no
Slater assumption and arbitrarily many native constraints. The local
Jacobian argument and characteristic-polynomial construction are standard
algebraic tools. The separate sharpness proof establishes the worst-case
degree for the class, not equality for each individual degenerate instance.
No claim of a new Bezout theorem or a new generic QCQP formula is intended.

The refinement gives a smaller exact algebraic representation bound and
can reduce a priori degrees in algebraic recognition. It does not by itself
provide a faster practical algorithm: height bounds, precision requirements,
and access to the canonical optimizer still matter. The
[independent review](multihomogeneous-degree-review.md) checked the parameter
specialization, joint-field argument, and the required ordered-limit
construction. Its exact checks cover a regular root beside a line component,
a regular exceptional fiber, ordered coefficient extraction, and the
maximizing support formula. The sharpness note records its separate
finite-field certificate for an explicit degree-four convex example.
These computations do not replace the general proofs. No project-wide or
CI checks were run for this note.
