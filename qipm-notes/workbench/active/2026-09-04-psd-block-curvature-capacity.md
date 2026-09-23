# A curvature-capacity lower bound for block-diagonal PSD lifts

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the local matrix lemma; moderate on novelty

## Result

Let \(C\subset\mathbb R^N\) be a full-dimensional compact convex body
with \(0\in\operatorname{int}C\), and suppose it has an exact extended
formulation over

\[
 K=\prod_{i=1}^k S_+^{r_i},
\]

allowing arbitrary affine slices, projections, and unrestricted free
variables. Suppose \(C\) has a relatively open \(C^2\) boundary
neighborhood containing a point of strictly positive curvature. Then

\[
 \boxed{\sum_{i=1}^k
   \left\lfloor\frac{r_i^2}{4}\right\rfloor\geq N-1.}    \tag{1}
\]

In particular, if \(2\leq r_i\leq d\) for every block, where \(d\geq2\),

\[
 \boxed{k\geq
 \left\lceil
 \frac{N-1}{\lfloor d^2/4\rfloor}
 \right\rceil.}                                         \tag{2}
\]

There is a sharper contact-rank statement. At a generic smooth
primal/polar contact, let \(X_i,Y_i\in S_+^{r_i}\) be the primal and dual
slack factors, and put

\[
 p_i=\operatorname{rank}X_i,\qquad
 q_i=\operatorname{rank}Y_i.
\]

Complementarity gives \(p_i+q_i\leq r_i\), and the mixed boundary
curvature satisfies

\[
 \boxed{N-1\leq\sum_i p_iq_i
 \leq\sum_i\left\lfloor\frac{r_i^2}{4}\right\rfloor.}    \tag{3}
\]

For \(r_i=2\), \(S_+^2\) is linearly isomorphic to \(Q_3\), every block
has capacity one, and (2) becomes the exact \(N-1\) Lorentz-block lower
bound. For larger PSD blocks, (1) is a lower bound; no matching general
upper construction is asserted.

## Regular slack factors

The reduction and regularity steps are the same as in
[the Lorentz curvature-budget
proof](2026-09-04-exact-lorentz-curvature-budget.md):

1. Boundedness eliminates unrestricted free variables.
2. Passing to the minimal face of \(K\) makes the lift proper. A face of
   \(S_+^{r_i}\) is another PSD cone \(S_+^{s_i}\) embedded on a fixed
   subspace; retaining the original \(r_i\) only weakens the final bound.
3. Minimum-norm primal fibers and minimum-norm attained dual
   certificates give semialgebraic factor maps
   \[
   A:\operatorname{ext}C\to K,\qquad
   B:\operatorname{ext}C^\circ\to K
   \]
   satisfying
   \[
   1-\langle x,y\rangle
   =\sum_i\operatorname{tr}(A_i(x)B_i(y)).               \tag{4}
   \]
4. Since an exact finite PSD lift is semialgebraic, a \(C^2\) exposed
   boundary patch and its normalized polar-contact map admit
   semialgebraic charts. Stratification supplies a common dense open
   locus on which all composed factor maps are \(C^1\) and their ranks
   are fixed.

Choose paired charts \(x(u)\in\partial C\) and
\(y(u)\in\partial C^\circ\), normalized by
\(\langle x(u),y(u)\rangle=1\). Set

\[
 X_i(u)=A_i(x(u)),\qquad Y_i(u)=B_i(y(u)).
\]

Every term in (4) is nonnegative and their diagonal sum is zero, so

\[
 \operatorname{tr}(X_i(u)Y_i(u))=0
 \quad\Longrightarrow\quad
 X_i(u)Y_i(u)=0                                         \tag{5}
\]

for every block and every \(u\) in the patch.

## The PSD tangent-channel lemma

Let \(X,Y:U\to S_+^r\) be \(C^1\) and satisfy \(X(u)Y(u)=0\) on an open
set. Fix \(u=0\), and write

\[
 p=\operatorname{rank}X(0),\qquad
 q=\operatorname{rank}Y(0).
\]

The ranges \(P=\operatorname{im}X(0)\) and
\(Q=\operatorname{im}Y(0)\) are orthogonal, so \(p+q\leq r\). With
\(R=(P\oplus Q)^\perp\), choose an orthonormal basis in which

\[
 X(0)=
 \begin{pmatrix}A&0&0\\0&0&0\\0&0&0\end{pmatrix},
 \qquad
 Y(0)=
 \begin{pmatrix}0&0&0\\0&B&0\\0&0&0\end{pmatrix},
 \qquad A\succ0,\ B\succ0.                              \tag{6}
\]

For a direction \(h\), positivity for both signs of a local parameter
implies that the compression of \(\dot X_h=DX(0)[h]\) to
\(\ker X(0)\) vanishes. Indeed,
\(v^T X(th)v\geq0\) and \(v^TX(0)v=0\) force
\(v^T\dot X_hv=0\) for every \(v\in\ker X(0)\); polarization then kills
the full kernel compression. The same argument applies to \(Y\).
Consequently,

\[
 \dot X_h=
 \begin{pmatrix}
 *&C_h&D_h\\
 C_h^T&0&0\\
 D_h^T&0&0
 \end{pmatrix},
 \qquad
 \dot Y_h=
 \begin{pmatrix}
 0&E_h&0\\
 E_h^T&*&F_h\\
 0&F_h^T&0
 \end{pmatrix}.                                        \tag{7}
\]

Differentiating \(XY=0\) and reading its \(P\times Q\) block gives

\[
 C_hB+AE_h=0,\qquad E_h=-A^{-1}C_hB.                    \tag{8}
\]

For two tangent directions \(h,\ell\), the only overlapping blocks in
the trace product from (7) are the \(P\times Q\) blocks. Hence

\[
 \begin{aligned}
 -\operatorname{tr}(\dot X_h\dot Y_\ell)
 &=-2\operatorname{tr}(C_hE_\ell^T)\\
 &=2\operatorname{tr}(A^{-1}C_hBC_\ell^T)\\
 &=2\left\langle
 A^{-1/2}C_hB^{1/2},
 A^{-1/2}C_\ell B^{1/2}
 \right\rangle_F.                                      \tag{9}
 \end{aligned}
\]

Thus the negative mixed derivative is a positive-semidefinite Gram form
whose rank is at most \(pq\). If \(p=0\) or \(q=0\), the corresponding
factor is at the PSD-cone vertex; its derivative is zero because the cone
is pointed, so the same rank-zero conclusion holds. The unused space
\(R\) in (6)--(7) shows that strict complementarity is not required.

This proves the tangent-channel capacity bound

\[
 \operatorname{rank}\!\left(
 -D_uD_v\,\operatorname{tr}(X(u)Y(v))\big|_{u=v=0}
 \right)
 \leq pq
 \leq\left\lfloor\frac{r^2}{4}\right\rfloor.             \tag{10}
\]

## From tangent channels to boundary curvature

Apply (9) blockwise to (4). The negative mixed derivative of the left
side is

\[
 \mathcal K=Dx(0)^TDy(0),
\]

so

\[
 \mathcal K
 =\sum_i 2\,L_i^*L_i,\qquad
 \operatorname{rank}L_i\leq p_iq_i,                     \tag{11}
\]

Here \(L_i[h]=H_i^{-1/2}C_{i,h}J_i^{1/2}\), where
\(H_i=X_i(0)|_{P_i}\succ0\) and \(J_i=Y_i(0)|_{Q_i}\succ0\); these are
the matrices denoted \(A,B\) in the single-block calculation (6)--(9).
Rank subadditivity gives

\[
 \operatorname{rank}\mathcal K\leq\sum_i p_iq_i.        \tag{12}
\]

If \(n(u)\) is the outward unit normal,
\(h(u)=\langle x(u),n(u)\rangle>0\), and
\(y(u)=n(u)/h(u)\), then

\[
 \mathcal K
 =\frac1{h(0)}Dx(0)^TDn(0).                             \tag{13}
\]

This is the second fundamental form up to a positive scalar. At a
strictly positively curved point it has rank \(N-1\). The common regular
factor locus is dense, while strict positive curvature persists on an
open neighborhood, so a regular positively curved contact can be chosen.
Equations (10)--(13) prove (1)--(3).

## Barrier consequence

The homogeneous-cone theorem of
[Güler and Tunçel](https://doi.org/10.1007/BF01584844) identifies the
optimal normal-barrier parameter with symmetric-cone rank. Hence

\[
 \nu_{\rm normal}=\sum_i r_i.
\]

Under the cap \(2\leq r_i\leq d\), (1) implies

\[
 \nu_{\rm normal}
 \geq
 \frac{N-1}{
 \max_{1\leq r\leq d}\lfloor r^2/4\rfloor/r}
 =
 \Omega\!\left(\frac Nd\right).                         \tag{14}
\]

For \(d=2\), this specializes exactly to
\(\nu_{\rm normal}\geq2(N-1)\), attained by the \(Q_3\) norm tree.
For \(d=1\), a product of \(S_+^1=\mathbb R_+\) factors is polyhedral and
cannot lift a positively curved body exactly; formulas (2) and (14) are
not intended for that zero-capacity case.
As before, these are ambient representation costs, not intrinsic
barrier or universal IPM iteration lower bounds for the projected body.

## Literature boundary

[Gouveia, Parrilo, and Thomas](https://arxiv.org/abs/1111.3164) establish
the general lift/slack-factorization framework.
[Fawzi and Parrilo](https://arxiv.org/abs/1311.2571) study lower bounds
for products of fixed-size PSD blocks, primarily for combinatorial
polytopes and via support-pattern methods.
[Fawzi and Safey El Din](https://arxiv.org/abs/1705.06996) lower-bound
the single-block PSD rank of convex bodies through the algebraic degree
of the polar boundary. These works do not state the local
\(pq\)-curvature capacity (9), the weighted product-block lower bound
(1), or its positive-curvature corollary.

A targeted search for PSD rank of Euclidean balls, curvature lower
bounds for semidefinite lifts, block-diagonal PSD extension complexity,
and mixed derivatives of PSD slack factorizations found no matching
theorem. The result should be described as apparently new pending a
broader specialist review.

## Audit checklist

- Verify the zero-kernel compression claim in (7), including
  nonconstant-rank paths.
- Verify that no \(P\)-\(R\) or \(Q\)-\(R\) term survives the trace in
  (9).
- Verify the order and signs in (8)--(9).
- Check that a minimal face \(S_+^{s_i}\) cannot evade the bound stated
  using the original \(r_i\).
- Search for existing differential lower bounds on block-PSD lifts of
  smooth positively curved bodies.

The independent audit checked the tangent-channel lemma, nonconstant-rank
and non-strictly-complementary cases, regularity transfer, and barrier
corollary, and found no counterexample. Its \(d=1\) and homogeneous-cone
citation requests have been incorporated.
