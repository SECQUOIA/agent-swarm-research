# Common-field bounds for an attained fractional optimum

Date: 2026-09-28. Status: independent proof review completed; no gap was
found under the assumptions below. A separate arithmetic review checked
the selected-support height calculation and the integer-grid argument over
the base field. This note supplies the field and encoding bounds for
fractional optimizer recovery. It does not by itself supply an algorithm
for deciding attainment or computing an optimizer.

The proof extends [the common-range witness lemma, Section 3](common-range-witness-recovery.md#3-a-classical-low-dimensional-arithmetic-bound)
using [the finite-quotient lemma over a number field](algebraic-coefficient-span-precision.md#3-the-finite-quotient-lemma-over-k).
The joint-field and trace arguments follow the same principles as
[the algebraic SOCP witness review](algebraic-socp-witness-field-review.md).
The crucial quantitative difference from a fixed-Hessian-span argument is
that the entire KKT system has at most twice the retained dimension.
The corresponding field, height, sublevel, and maximum-of-ratios statements
in [the fractional recovery note](common-range-fractional-witness.md),
Sections 1--4 and 7--8, were also checked; no material correction remains.

## 1. Precise assumptions and conclusion

Let \(F\subseteq\mathbb R^n\) be defined by explicitly encoded rational
native convex quadratic inequalities, or rational native SOC constraints,
and rational affine rows. Its rational input length, including two affine
functions \(f,d\), is \(N\ge2\). In an SOC row retain both its squared
polynomial inequality and the sign of its right-hand side. Write
\(H_i\) for the resulting native quadratic Hessians and set

\[
 K_0=\bigcap_i\ker H_i,\qquad
 K'=K_0\cap\ker(d_x^T),\qquad
 r=\operatorname{codim}K'\le\operatorname{codim}K_0+1.       \tag{1}
\]

Assume \(d(x)>0\) for every \(x\in F\), and that the finite minimum
\(\theta=\min_F f/d\) is attained. Its exact description consists of
a primitive irreducible integer polynomial of degree \(D\), maximum
coefficient bit length \(H\ge1\), and a rational isolating interval
selecting the intended real root. All field statements refer to this real
embedding of \(K=\mathbb Q(\theta)\).

Choose a rational invertible split

\[
 x=T_1u+T_0v,\qquad u\in\mathbb R^r,\qquad
 \operatorname{range}T_0=K'.                              \tag{2}
\]

Fix the split produced by rational linear algebra; its entries and inverse
have \(N^{O(1)}\) bits. Let \(u^*\) minimize \(\|u\|^2\) over the
projection of the optimal set, and let \(v^*\) minimize \(\|v\|^2\)
in the optimal fiber over \(u^*\). Both points exist and are unique.
Their existence is proved below, including closedness of the projection.
This sequential choice need not minimize the norm of \(x\) in the
original coordinates.

There are computable functions \(A,B\) and an **absolute** constant
\(C\), independent of \(n,r,D\), such that

\[
 \begin{split}
 [K(u^*):K]&\le3^{2r},\\
 K(u^*,v^*)&=K(u^*),\\
 [\mathbb Q(\theta,x^*):\mathbb Q]&\le D3^{2r},\\
 \operatorname{heightbits}(x_j^*)&\le A(r,D)(N+H+1)^C.
 \end{split}                                               \tag{3}
\]

Here heightbits means the maximum coefficient bit length of the primitive
integer minimal polynomial. The same height bound holds for \(u^*,v^*\).
The tuple \((\theta,x^*)\) has one rational univariate representation
of total length at most \(B(r,D)(N+H+1)^C\), including a polynomial
representing \(\theta\). A rational box with radius of this bit length
contains the selected point itself.

Thus \(D\le g(p)\) and \(H\le g(p)N^{C_0}\), for structural
parameters \(p\) and absolute \(C_0\), imply a bound
\(g_1(p,r)N^{C_1}\) with absolute \(C_1\). No factor
\(N^{C_r}\) is hidden in this conclusion. An unnecessarily long supplied
isolating interval does not increase these existence bounds; an algorithm
reading it must, of course, count its encoded length.

## 2. Constant rational fiber rows survive the optimal level

The denominator is independent of \(v\): write \(d=d_0(u)\) and
\(f=f_v^Tv+f_0(u)\), with rational affine data. Every original row has
the form \(C_iv\le b_i(u)\), with constant rational \(C_i\) and
rational quadratic \(b_i\), because every Hessian kills \(T_0\).
The equality defining the optimal level is

\[
             f_v^Tv=\theta d_0(u)-f_0(u).                 \tag{4}
\]

Encode (4) by its two weak inequalities. The entire optimal set becomes

\[
                   C'v\le b_\theta(u),                   \tag{5}
\]

where \(C'\) is still constant **rational**. Each right-hand coefficient
is \(a+b\theta\), with rational \(a,b\) of polynomial bit length.
Each right-hand side has degree at most two in \(u\).

Positivity of \(d\) makes this set exactly the optimizers. Independently,
it is the intersection of the closed convex set \(F\) with an affine
hyperplane at the selected embedding, and is nonempty by attainment.
No positive uniform lower bound on \(d\) is required.

Apply Farkas' lemma to (5). The projection is exactly

\[
 U_\theta=\{u:P_j(u)\le0\ (1\le j\le S)\},\qquad
 P_j=-\lambda_j^Tb_\theta,                               \tag{6}
\]

where the \(\lambda_j\) generate the extreme rays of
\(\{\lambda\ge0:(C')^T\lambda=0\}\). A ray has support at most
\(\operatorname{rank}C'+1\), and minors of this rational matrix give
a rational generator of polynomial bit length. Therefore every
coefficient of every \(P_j\) can be written

\[
 a+b\theta,\qquad \operatorname{bit}(a),\operatorname{bit}(b)\le B_0,
 \qquad B_0\le N^{C_2},\qquad \log(S+1)\le N^{C_2},        \tag{7}
\]

for an absolute \(C_2\). Clearing denominators separately in each
projected row also gives (7); no common denominator across this
exponential family is needed. The family is used only for bounds.

Equation (6) proves closedness, and projection preserves convexity.
Consequently the nonempty set \(U_\theta\) has a unique minimum-norm
point. General projections of closed convex sets need not be closed; the
constant-matrix argument is essential here.

## 3. One low-dimensional perturbation over \(K\)

Assume first \(r\ge1\). Choose integer quadratics
\(Q_0,Q_1,\ldots,Q_S\) and put

\[
 F_{j,\varepsilon}=P_j+\varepsilon^2Q_j-\varepsilon,
 \qquad
 g_\varepsilon=\|u\|^2+\varepsilon Q_0.                  \tag{8}
\]

The genericity argument in the rational witness proof works over \(K\).
For each selected set of at most \(r\) rows, proper algebraic bad loci
exclude dependent constraint gradients and singular full bordered KKT
matrices; for \(r+1\) rows another bad locus excludes a common zero.
Their degrees are bounded solely in terms of \(r\). This uses generic
quadratics, not convexity of the individual projected polynomials.

For nonzero \(\varepsilon\), the map from perturbation coefficients to
the selected constraint and objective coefficients is surjective. Thus
each pulled-back bad polynomial is nonzero in \(K[\varepsilon,Q]\).
Choose one nonzero coefficient in \(\varepsilon\) from each such
polynomial. Their product over all relevant row subsets is a nonzero
polynomial over \(K\), of degree at most

\[
                         (S+1)^{r+1}G(r),                \tag{9}
\]

with computable \(G(r)\). A nonzero polynomial over any characteristic
zero field of total degree at most \(M\) cannot vanish on the whole
integer grid \(\{0,\ldots,M\}^m\). We may therefore choose the
\(Q_j\) with integer coefficient bits

\[
                  b_Q\le O(r\log(S+1))+\log(G(r)+1)+O(1). \tag{10}
\]

After this choice, only finitely many nonzero \(\varepsilon\) are
exceptional. Neither the product nor the grid is constructed.

Take an unknown integer \(R>\|u^*\|_\infty+1\). Minimize
\(g_\varepsilon\) on \([-R,R]^r\) subject to
\(F_{j,\varepsilon}\le0\). The point \(u^*\) satisfies these rows
for all sufficiently small positive \(\varepsilon\). Compactness gives
perturbed minimizers. Every cluster point as \(\varepsilon\downarrow0\)
is in \(U_\theta\); comparison with \(u^*\) and uniform objective
convergence imply that it has minimum norm. Uniqueness forces every such
limit to be \(u^*\).

All perturbed minimizers are consequently strictly inside the box for
sufficiently small \(\varepsilon\). Otherwise boundary minimizers
would have a boundary cluster point. Thus the unknown radius occurs in
no eventual KKT equation or coefficient estimate.

Choose a sequence of nonexceptional \(\varepsilon\downarrow0\) and
one active subset recurring along a subsequence. Its size is \(s\le r\).
The full KKT equations in \(y=(u,\lambda)\) are

\[
 F_{i,\varepsilon}(u)=0\ (i\in I),\qquad
 \nabla g_\varepsilon(u)+
                  \sum_{i\in I}\lambda_i\nabla F_{i,\varepsilon}(u)=0.
                                                               \tag{11}
\]

There are \(q=r+s\le2r\) equations and root variables. Their total
degree in \(y\) is at most two; their degree in \(\varepsilon\) is
at most two. The selected root is nonsingular by the full bordered
condition. The upper-left Hessian block need not be invertible. The
multipliers need not remain bounded as \(\varepsilon\downarrow0\).

## 4. All-place heights with an absolute input exponent

Write \(h_{\rm W}\) for absolute logarithmic Weil height, using
natural logarithms. From the polynomial for \(\theta\),
\(h_{\rm W}(\theta)\le H\log2+\log(D+1)\) is a conservative
bound. Each coefficient in (7) therefore satisfies

\[
 h_{\rm W}(a+b\theta)
       \le O(B_0+H+\log(D+1)+1).                        \tag{12}
\]

The selected \(s\le r\) rows contain only \(O(r^3)\) coefficients.
Their joint affine height is at most the sum of those coefficient heights.
At each place use the polynomial coefficient \(\ell_1\)-norm for
archimedean places and maximum coefficient norm for finite places, treating
\(\varepsilon\) as a formal indeterminate. Let \(E\) be the averaged
logarithmic maximum of these norms over the KKT polynomials, \(A=1\),
and one output \(B=u_j\), also including one in the maximum. Integer
differentiation factors and the perturbations contribute only
\(b_Q+O(\log(r+1))\), up to a factor depending on \(r\). Thus

\[
 E\le A_0(r)\bigl(B_0+H+\log(D+1)+\log(S+1)+1\bigr).       \tag{13}
\]

This is where the support restriction matters. Taking the joint height of
**all** \(S\) projected rows could accumulate different finite-place
denominators and lose the desired bound. We select the at-most-\(r\)
rows before taking the joint coefficient norm. No numerical bound on
\(\varepsilon\), the multipliers, or \(R\) enters (13).

Apply the field finite-quotient lemma directly to (11), eliminating all
\(q\) variables with degree parameter two. Put

\[
 L=3^q\le3^{2r},\qquad T=2(q+1),\qquad
 W=L(T+1)E+\log(L!)+L\log3.                             \tag{14}
\]

It yields a nonzero \(P\in K[w]\) annihilating the selected finite
limit \(u_j^*\), with degree at most \(L\) and affine coefficient
height at most \(W\). The proof extracts coefficients from a determinant
in formal perturbation parameters. Such extraction decreases every local
norm; the product formula and local Cauchy bounds give

\[
 [K(u_j^*):K]\le L,\qquad h_{\rm W}(u_j^*)\le W+\log2.     \tag{15}
\]

No optimization property is required at the other embeddings of \(K\).
They are used only for coefficient norms. A normal closure and a field
norm are unnecessary.

If \(p_j\) is the primitive integer minimal polynomial of \(u_j^*\),
its degree is at most \(DL\). The identity between Mahler measure and
Weil height gives directly

\[
 \log\|p_j\|_\infty
       \le DL\bigl(W+2\log2\bigr).                      \tag{16}
\]

This avoids an unsupported assumption that taking an irreducible factor
decreases coefficient height. Equations (7), (13), and (14) show that (16)
is \(A_1(r,D)(N+H+1)^C\) with an absolute \(C\). The dependence on
the incoming coefficient bit lengths is linear before the final rational
linear algebra, rather than a power whose exponent depends on \(r\).

## 5. Joint degree and the affine fiber

All coordinates in (15) refer to the same fixed tuple \(u^*\), support,
and root sequence. Replace the output by any \(K\)-linear form in
\(u\). Its degree remains one in the eliminated variables, so the
relative degree bound stays \(L\); its coefficient height may change.
Since the coordinates are algebraic, the primitive element theorem gives
such a form generating \(E_*=K(u^*)\). Rational coefficients already
suffice to avoid the finitely many equal-image hyperplanes. Therefore

\[
                         [E_*:K]\le L.                   \tag{17}
\]

We do not multiply coordinate degrees. Repeating the argument with
different limiting points would not justify (17).

The fiber \(C'v\le b_\theta(u^*)\) is a nonempty closed polyhedron.
At its unique minimum-norm point choose independent active row normals
whose span contains \(v^*\). The normal-cone optimality condition and
conic Caratheodory give such rows. Then

\[
             v^*=(C'_I)^T\bigl(C'_I(C'_I)^T\bigr)^{-1}
                                                   b_{\theta,I}(u^*).
                                                               \tag{18}
\]

Use the empty set if \(v^*=0\). Every matrix entry in (18) is rational
of \(N^{O(1)}\) bits by minor bounds, even though the number of rows
in \(I\) can grow with \(n\). Each coordinate of \(v^*\) is a
polynomial of degree at most two in \(u^*\), with coefficients
\(a+b\theta\) of polynomial rational bit length. Hence it belongs
to \(E_*\), and ordinary sum and product height inequalities give

\[
 h_{\rm W}(v_j^*)\le A_2(r)\bigl(N^{C_3}+H+\log(D+1)+W+1\bigr)
                                                               \tag{19}
\]

for absolute \(C_3\). Bounding a sum by its number of original terms
only adds an absolute polynomial factor in \(N\); collecting monomials
first gives the displayed bound. With absolute degree at most \(DL\),
(19) gives the required integer minimal-polynomial height bound. Rational
transformation (2) preserves the same form of bound, with at most another
absolute polynomial factor in \(N\).

If \(r=0\), the projection is the empty tuple, \(L=1\), and (18)
directly gives \(v^*\in K^{n}\) and the same height estimates. This
also covers a purely affine optimal fiber. No perturbation lemma in zero
variables is needed.

## 6. One short representation that includes \(\theta\)

Let \(e=[E_*:\mathbb Q]\le D3^{2r}\). The tuple
\((\theta,u_1^*,\ldots,u_r^*)\) generates \(E_*\). The product of
equal-image linear forms for distinct field embeddings has degree at most
\(e(e-1)/2\). The integer-grid argument provides integer coefficients
of at most \(O(\log(e+1))\) bits for a primitive linear combination
\(\gamma\) of this tuple. In degree one use the immediate rational
representation.

The height inequalities and (15) bound \(h_{\rm W}(\gamma)\) by the
same \(A(r,D)(N+H+1)^C\) form. Its minimal polynomial has a coefficient
bound of that form as well. Multiply \(\gamma\) by its leading
coefficient to obtain an algebraic integer primitive element \(\beta\).
Similarly scale each coordinate of \((\theta,u^*,v^*,x^*)\) by its
own minimal-polynomial leading coefficient to make it integral. There is
no need to multiply leading coefficients across all ambient coordinates.

For each scaled coordinate \(a\), solve for its representation in the
basis \(1,\beta,\ldots,\beta^{e-1}\) using

\[
 T_{ij}=\operatorname{Tr}_{E_*/\mathbb Q}(\beta^{i+j}),
 \qquad b_i=\operatorname{Tr}_{E_*/\mathbb Q}(a\beta^i).
                                                               \tag{20}
\]

The matrix and right-hand side are integers; separability makes \(T\)
nonsingular. Cauchy bounds for every conjugate of the scaled coordinates
and \(\beta\) bound their entries by polynomial bit lengths in \(e\)
and the preceding height bound. Cramer's rule does the same for the
rational coordinate coefficients. Divide back by each coordinate scale.
The degree \(e\) depends only on \(r,D\), and the number of coordinates
is at most polynomial in \(N\), so these matrices and all printed
coefficients have the stated absolute-exponent length bound.

Integer-polynomial root separation supplies an isolating interval for the
chosen real \(\beta\) with polynomially many bits in its degree and
coefficient bound. The result includes a coordinate polynomial for
\(\theta\). Cauchy bounds also give a box containing this particular
\(x^*\), rather than merely some feasible point.

## 7. Nonempty sublevels and a maximum of ratios

The arithmetic proof does not need optimality. It applies to any nonempty
equality level \(F\cap\{f-\theta d=0\}\), and it also applies to
any nonempty sublevel

\[
                    F\cap\{f-\theta d\le0\}.             \tag{21}
\]

For (21), append just the one corresponding row in (5). Its normal on
\(v\) is rational; its right-hand side has the same coefficient form.
The set is closed and convex, and all subsequent arguments are unchanged.
The canonical point refers to this sublevel, whether or not \(\theta\)
is the optimal value. This distinction is useful when bounding witnesses
uniformly before an attainment decision has been made.

More generally, consider

\[
                 \Phi(x)=\max_{1\le j\le m}\frac{f_j(x)}{d_j(x)},
                 \qquad d_j>0\text{ throughout }F.        \tag{22}
\]

Include all rational affine numerators and denominators in the input length
\(N\). Retain the span of all denominator directions by using

\[
 K'=K_0\cap\bigcap_j\ker d_{j,x}^T,
 \qquad
 r\le r_0+\ell,\qquad r_0=\operatorname{codim}K_0,          \tag{23}
\]

where \(\ell\) is the rank of their restrictions to \(K_0\). The
rank of the full denominator gradients is also a valid upper bound on
\(\ell\). For a known algebraic \(\theta\), its sublevel is defined
by all the weak inequalities

\[
                        f_j-\theta d_j\le0.               \tag{24}
\]

After the split, their \(v\)-normals are the constant rational numerator
rows, and their right-hand sides are affine in \(\theta\) and in
\(u\). Thus (3) holds for the canonical point of every nonempty
sublevel (24), with the new \(r\). If \(\theta\) is the attained
minimum, this sublevel is exactly the optimal set. Requiring every
individual ratio to equal \(\theta\) would be incorrect. The number
\(m\) of ratios is part of \(N\), not a separate parameter; only
their retained denominator rank affects \(r\).

For fixed integer coordinates of bit length at most \(M\), rational
substitution increases coefficient lengths and transformed input length
by an absolute polynomial in \(N+M\). If the chosen eliminated kernel
annihilates the full native Hessians, including integer-continuous blocks,
and every continuous denominator gradient, the constant matrix in (5)
is uniform in that substitution. More generally one can recompute the
continuous split after substitution under a uniform rank bound. Consequently
one computable

\[
                         B=A(r,D)(N+M+H+1)^C              \tag{25}
\]

bounds the coordinate-polynomial bits and the log radius of a canonical
witness in **every nonempty** substituted sublevel. Empty sublevels require
no witness. This uniform statement does not assume that an optimal integer
assignment has already been identified, and is the encoding fact needed
by a bounded-integer attainment test. The integer-size bound and that test
remain separate algorithmic inputs.

## 8. Verification, example, and limits

The proof uses established perturbation, finite-quotient, height, and
primitive-element machinery. The primary
[Jeronimo--Perrucci--Tsigaridas paper](https://arxiv.org/pdf/1112.0544)
was consulted: its Theorem 1 and Theorem 12 provide nearby arithmetic bounds
and treat unbounded components with compact minimizing sets. The extension
over \(K\) and the explicit joint-degree bound here follow the local
lemmas and calculations above; they are not attributed directly to those
source statements. No novelty claim is made.

A rational SOC example checks that an extension beyond the value field
can be necessary. In variables \((t,x,v)\), impose

\[
 \|(1,1)\|\le t,\qquad
 \|(1+t/2,1,t/2)\|\le x,\qquad
 \|(2x,t+2)\|\le t+4,\qquad v\ge x+t.                    \tag{26}
\]

The first three rows force \(t=\sqrt2\) and
\(x=\sqrt{3+\sqrt2}\). Minimize \(t/(1+t)\); its denominator is
positive throughout this set and its attained value is
\(\theta=2-\sqrt2\). The common nonlinear range is the \((t,x)\)
plane. The canonical fiber point is \(v^*=x+t\). The value field has
degree two, whereas the tuple field has degree four, generated by
\(\beta=x\) with polynomial \(X^4-6X^2+7\) and isolating interval
\((2,9/4)\). Its coordinate polynomials are

\[
             t=\beta^2-3,\qquad
             \theta=5-\beta^2,\qquad
             v^*=\beta^2+\beta-3.                        \tag{27}
\]

The targeted symbolic command recorded below checked the squared residuals,
their Hessians, irreducibility and root isolation, and these identities.
It does not prove the universal bounds.

For the optimal-witness interpretation, attainment is assumed. The encoding
argument only needs the relevant level or sublevel to be nonempty, and its
threshold must be an explicitly represented algebraic number. An FPT
recovery theorem additionally needs a coefficient-sensitive feasibility
oracle, a certified approximation procedure for this same canonical point,
and algebraic recognition with certified bounds. Enumerating the implicit
Farkas rows or genericity grid is not an FPT procedure. Applying a norm cone
to all original coordinates can increase the common range to \(n\);
the sequential construction avoids that step. If the denominator direction
is not retained, the optimal row can have algebraic coefficients on the
eliminated variables, so the rational-matrix fiber argument used here no
longer applies as stated. Positivity of \(d\) and retention of SOC signs
are needed for the optimization interpretation.

Verification record: an inline `python` command using SymPy checked (26)
and (27), and an inline `python` document check tested this file's local
links, paired math delimiters, final newline, and trailing whitespace.
Only these targeted checks were run. Project-wide verification and CI
status or logs were not inspected; no formal proof assistant was used.
