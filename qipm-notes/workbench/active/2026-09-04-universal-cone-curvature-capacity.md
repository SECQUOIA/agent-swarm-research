# Universal dimension-minus-two curvature capacity of cone lifts

Status: Proved; literature-screened; independently audited twice
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the local linear-algebra lemma; novelty pending specialist review

## Result

Let \(C\subset\mathbb R^N\), \(N\geq2\), be a full-dimensional compact
convex body with \(0\in\operatorname{int}C\). Suppose it has an exact lift
over a product

\[
 K=K_1\times\cdots\times K_k
\]

of finite-dimensional proper cones, with arbitrary affine slices,
projections, and unrestricted free variables. Assume that the cones and
lift data are definable in one o-minimal structure. This includes
semialgebraic cones and, in \(\mathbb R_{\exp}\) with finitely many real
parameters, the usual exponential and fixed-exponent power cones. Let
\(m_i=\dim K_i\), and omit any one-dimensional ray factors, which have no
curvature capacity. If \(C\) has a relatively open \(C^2\) boundary
neighborhood containing a strictly positively curved point, then

\[
 \boxed{N-1\leq\sum_{i=1}^k(m_i-2).}                 \tag{1}
\]

More locally, at any exposed primal--polar contact where the regular factor
selections below are \(C^1\), define

\[
 L_i=T_{K_i}(A_i(x))\cap[-T_{K_i}(A_i(x))],\qquad
 L_i^*=T_{K_i^*}(B_i(y))\cap[-T_{K_i^*}(B_i(y))],
\]

and let \(c_i\) be the rank of the Euclidean pairing restricted to
\(L_i\times L_i^*\). Then

\[
 \operatorname{rank}\mathcal K\leq\sum_i c_i,
 \qquad c_i\leq m_i-2,                              \tag{2}
\]

where \(\mathcal K=Dx^TDy\) is the mixed slack-curvature form. Positive
curvature makes its rank \(N-1\).

Consequently, if every non-ray block has dimension at most \(d\geq3\),

\[
 k\geq\left\lceil\frac{N-1}{d-2}\right\rceil.       \tag{3}
\]

For the Euclidean ball, Lorentz norm trees attain equality. In fact, among
all products of definable proper cone blocks of dimension at most \(d\),
the simultaneous exact optima are

\[
 \boxed{
 k_{\min}=\left\lceil\frac{N-1}{d-2}\right\rceil,
 \qquad
 \nu_{\min}=2\left\lceil\frac{N-1}{d-2}\right\rceil,
 \qquad
 M_{\min}=N-1+2\left\lceil\frac{N-1}{d-2}\right\rceil.} \tag{4}
\]

Here \(M=\sum_i m_i\) is total cone-space dimension and \(\nu\) is the
optimal parameter of a logarithmically homogeneous self-concordant barrier
on the ambient product cone. This
barrier statement applies even to a coupled, nonseparable barrier on the
product; it is not limited to sums of chosen block barriers. For symmetric
cones, the finer Peirce theorem in
[the companion note](2026-09-04-symmetric-cone-curvature-capacity.md)
also resolves the capacity in terms of Jordan and complementary ranks.

## Regular factors from a general lift

Eliminate free variables by boundedness and pass to the minimal face of the
product cone containing the feasible slice. A face of a product is a product
of faces. In the linear span of each surviving face, the face is again a
proper cone and the reduced lift is proper. The full reduction, including
linearization of the affine output, is written out in
[the Lorentz note](2026-09-04-exact-lorentz-curvature-budget.md).

If a reduced face has dimension \(s_i\), the proof below gives capacity at
most \(\max\{s_i-2,0\}\), which is at most
\(\max\{m_i-2,0\}\). Thus it is enough to prove the theorem for a proper
lift

\[
 C=\{\pi z:z\in K,\ Mz=b\},
 \qquad w_0\in\operatorname{int}K,\quad Mw_0=b.       \tag{5}
\]

The minimum-norm primal fibers and minimum-norm attained dual multipliers
give factor maps

\[
 A(x)\in K,\qquad B(y)\in K^*,\qquad
 1-\langle x,y\rangle=\langle A(x),B(y)\rangle       \tag{6}
\]

on exposed points of \(C\) and \(C^\circ\). Slater's condition in (5)
gives dual attainment. The construction and the identity in (6) are
explicitly derived in the Lorentz note.

The particular minimal face above is definable. If \(\bar z\) lies in
its relative interior, it is described by
\[
 F(\bar z)=\{z\in K:\text{ for some }\epsilon>0,
 \ \bar z-\epsilon z\in K\}.
\]
Dual membership also has a first-order description in the common o-minimal
structure. The minimum-norm selections in (6) are therefore definable. Shrink the
assumed boundary patch to a nonempty open neighborhood of strict positive
curvature. Positive curvature excludes a nontrivial primal support face,
and smoothness gives a unique normal ray, so the paired primal and normalized
polar points are both exposed. Apply a finite definable \(C^1\)
stratification to the joint map
\(x\mapsto(y(x),A(x),B(y(x)))\). It supplies a dense open subset of this
patch on which all composed primal and polar factor maps are simultaneously
\(C^1\). Choose the contact there.

With paired local charts

\[
 x(u)\in\partial C,\qquad
 y(u)=\frac{n(u)}{\langle x(u),n(u)\rangle}
       \in\partial C^\circ,
 \qquad \langle x(u),y(u)\rangle=1,                  \tag{7}
\]

put \(A_i(u)=A_i(x(u))\) and \(B_i(u)=B_i(y(u))\).
Every block slack

\[
 g_i(u,v)=\langle A_i(u),B_i(v)\rangle               \tag{8}
\]

is nonnegative, and \(g_i(u,u)=0\) because the sum of these nonnegative
terms is the zero diagonal slack.

## Local dimension-minus-two lemma

Let \(K\subset E\) be an \(m\)-dimensional proper cone and let
\(A,B:U\to K\times K^*\) be \(C^1\). Assume

\[
 g(u,v)=\langle A(u),B(v)\rangle\geq0,
 \qquad g(u,u)=0.                                    \tag{9}
\]

At \(u=0\), write \(a=A(0)\), \(b=B(0)\).

First suppose \(a,b\neq0\). For every tangent direction \(h\), the scalar
function \(t\mapsto\langle A(th),b\rangle\) is nonnegative and vanishes at
zero. Its two-sided derivative is zero, hence

\[
 DA(0)[h]\in b^\perp.                                \tag{10}
\]

Similarly,

\[
 DB(0)[h]\in a^\perp.                                \tag{11}
\]

The Euclidean pairing restricted to \(b^\perp\times a^\perp\) has rank
exactly \(m-2\). Indeed, the linear map

\[
 b^\perp\longrightarrow(a^\perp)^*,
 \qquad v\longmapsto\langle v,\mathord\cdot\rangle
\]

has kernel

\[
 b^\perp\cap(a^\perp)^\perp
 =b^\perp\cap\operatorname{span}\{a\}
 =\operatorname{span}\{a\},                         \tag{12}
\]

because \(\langle a,b\rangle=0\). Its domain has dimension \(m-1\),
which proves the claim. It follows that

\[
 \operatorname{rank}\bigl(DA(0)^TDB(0)\bigr)\leq m-2. \tag{13}
\]

If \(A,B\) are \(C^2\), the sign is also controlled. Since
\(g\geq0\) and \(g(0,0)=0\), its full
Hessian at \((0,0)\) is positive semidefinite. Since
\(g(u,u)=0\), every diagonal tangent vector \((h,h)\) has zero quadratic
form and therefore lies in the kernel of that Hessian. Writing

\[
 \nabla^2g(0,0)=
 \begin{pmatrix}P&R\\R^T&Q\end{pmatrix},
\]

the kernel identities give \(P=-R\), \(Q=-R^T\), and symmetry of
\(P,Q\) gives \(R=R^T\). Thus

\[
 -D_uD_vg(0,0)=-R\succeq0.                           \tag{14}
\]

Because the mixed derivative of the bilinear factor is
\(R=DA(0)^TDB(0)\), equations (13)--(14) show that a single block
contributes a positive-semidefinite mixed-curvature form of rank at most
\(m-2\). This sign refinement is not needed for the rank theorem.

If \(a=0\), then \(DA(0)=0\): every two-sided directional derivative lies
in both \(K\) and \(-K\), and pointedness makes it zero. Likewise, \(b=0\)
implies \(DB(0)=0\). Such a block contributes no mixed curvature. This also
handles one-dimensional ray faces, where complementary factors cannot both
be nonzero.

Equivalently, (10)--(11) say that the derivative images lie in the
linealities of the tangent cones at \(a,b\), which are contained in the two
supporting hyperplanes. The proof needs no smoothness, strict convexity,
self-duality, homogeneity, or symmetry of the lifting cone itself.

## Summing the blocks

Differentiate (6) once in each boundary variable:

\[
 \mathcal K:=Dx(0)^TDy(0)
 =\sum_i\bigl(-D_uD_vg_i(0,0)\bigr),                 \tag{15}
\]

Every summand has rank at most \(m_i-2\) by (13), so ordinary matrix-rank
subadditivity proves (2); no sign is required. On a common \(C^2\) stratum,
(14) additionally makes every summand positive semidefinite. From (7),

\[
 \mathcal K=
 \frac{1}{\langle x(0),n(0)\rangle}Dx(0)^TDn(0),    \tag{16}
\]

so it is a positive multiple of the second fundamental form. Strict
positive curvature gives rank \(N-1\), proving (1).

Under \(m_i\leq d\), equation (3) follows immediately. Also

\[
 M=\sum_i m_i
 \geq N-1+2k.                                       \tag{17}
\]

The norm-tree construction partitions \(N-1\) as
\(N-1=\sum_i(m_i-2)\) with \(m_i\leq d\), so it attains both lower bounds
on block count and total cone dimension in (4). At the root, its Lorentz
scalar coordinate is fixed affinely to one; no additional ray factor or
inequality is used.

## Ambient barrier consequence

Let \(q\) and \(r\) be the numbers of non-ray and ray factors, respectively,
in an arbitrary product of proper cones. In each non-ray factor choose a
two-dimensional linear subspace
through an interior point. Its intersection with the cone is a
two-dimensional proper cone and is therefore linearly isomorphic to
\(\mathbb R_+^2\). The product of these sections together with the full ray
factors is \(\mathbb R_+^{2q+r}\).

Because each section contains an ambient interior point,
\(\operatorname{ri}(K_i\cap L_i)=\operatorname{int}(K_i)\cap L_i\), and
every relative-boundary point of the section lies on \(\partial K_i\).
Restriction therefore preserves the barrier blow-up property, as well as
self-concordance and logarithmic homogeneity.

The resulting product section meets the interior of every operational
factor. The restriction of any \(\nu\)-logarithmically homogeneous
self-concordant barrier on the full product is a barrier with the same
parameter on this section. The optimal parameter on
\(\mathbb R_+^{2q+r}\) is \(2q+r\), so

\[
 \nu\geq2q+r\geq2q.                                   \tag{18}
\]

This also follows from the general Carathéodory-number lower bound of
Güler and Tunçel: pointwise Carathéodory numbers add on products and every
interior point of a non-ray proper cone needs at least two extreme
directions. Equation (18) makes explicit that ray factors contribute one
more unit each and cannot help minimize the parameter.

In the dimension-capped positive-curvature setting, (3) and (18) give

\[
 \nu\geq
 2\left\lceil\frac{N-1}{d-2}\right\rceil.            \tag{19}
\]

The Lorentz norm tree has the summed rank-two barriers and attains (19),
proving the barrier optimum in (4). This is an ambient representation cost,
not an intrinsic barrier lower bound for the projected body.

## Scope and literature boundary

O-minimal definability is used only to manufacture common \(C^1\) factor
strata from arbitrary affine lift data. The local lemma applies to any
proper cone and any factor maps already known to be \(C^1\). A common
\(C^2\) stratum gives the optional blockwise positivity refinement (14).

[Gouveia, Parrilo, and
Thomas](https://doi.org/10.1287/moor.1120.0575) prove the general
lift/slack-factorization theorem. Existing cone-rank work typically studies
specific cone families or combinatorial slack patterns. Targeted searches
for differential slack factorizations, second fundamental forms of cone
lifts, curvature versus arbitrary cone-block dimension, and
dimension-minus-two extension-complexity bounds found no matching theorem.
The result should be described as apparently new pending specialist review;
an open-literature search cannot establish priority.

[Güler and Tunçel](https://doi.org/10.1007/BF01584844), Proposition 4.1,
give the general Carathéodory-number lower bound used in (18).
[Hildebrand](https://doi.org/10.1007/s10107-012-0576-1), Corollary 3.2,
independently states the universal bound \(\nu\geq2\) for every regular cone
of dimension at least two.

The o-minimal extension uses definable \(C^1\) stratification; see
[van den Dries--Miller](https://doi.org/10.1215/S0012-7094-96-08416-1).
[Wilkie](https://doi.org/10.1090/S0894-0347-96-00216-0) proves the
o-minimality of \(\mathbb R_{\exp}\).

The closest complementary results found in the literature are
[Scheiderer's 2025 SOC-representability
theorem](https://arxiv.org/abs/2509.17121), which proves existence of a
finite SOC lift for compact semialgebraic Nash-smooth strictly curved
bodies but gives no block-count bound, and
[Saunderson's product-cone obstruction](https://doi.org/10.1137/19M1245670),
which is based on neighborliness and face chains rather than local
curvature. Fixed-size PSD/SOC, algebraic-boundary, and zero-pattern lower
bounds likewise do not imply (1). No direct collision was found.

## Audit checklist

- Verify that compatible definable \(C^1\) stratification of the chosen
  minimum-norm selections is sufficient and that a positive-curvature point
  remains available.
- Verify the minimal-face reduction for non-exposed faces of arbitrary
  definable cones and the claimed definability of those faces.
- Check the rank \(m-2\) of the restricted hyperplane pairing, including
  the zero-factor and ray cases.
- Check the Hessian-kernel argument establishing blockwise positive
  semidefiniteness on a common \(C^2\) stratum. This is a refinement, not a
  prerequisite for rank subadditivity.
- Verify the two-dimensional-section and arbitrary coupled-product-barrier
  argument in (18)--(19).
- Search for existing smooth-factorization-rank or differential
  extension-complexity results that imply (1).

The independent hostile audit checked the affine-lift and possibly
nonexposed minimal-face reductions, definable regularity, exposure of the
paired contact, hyperplane-pairing rank, zero/ray/two-dimensional cases,
mixed-derivative summation, and all exact ball optima. It also verified the
barrier restriction argument for coupled product barriers and searched the
open literature. A second hostile audit independently checked the same
items and the o-minimal exponential/power-cone extension. No counterexample
or matching prior theorem was found. The audits'
clarifications that \(C^1\) suffices for the rank theorem and that blockwise
positive semidefiniteness is optional have been incorporated.
