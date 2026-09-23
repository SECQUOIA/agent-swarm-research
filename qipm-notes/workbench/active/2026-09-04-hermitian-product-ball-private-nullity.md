# Private-nullity law for Hermitian PSD lifts of products of balls

Status: Proved; core, one-block theorem, and capped refinement independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), and let

\[
                 C=\prod_{a=1}^h B_2^{s_a},\qquad s_a\geq2.
                                                               \tag{1}
\]

Suppose the full extreme-row slack family has labelled \(C^1\) Hermitian
PSD factors

\[
  1-x_a^Tz=\sum_i\langle X_i(x),Y_i^a(z)\rangle,qquad
  \langle U,V\rangle=\operatorname{Re}\operatorname{tr}(UV),           \tag{2}
\]

where \(x\in\prod_aS^{s_a-1}\), \(z\in S^{s_a-1}\), and
\(X_i,Y_i^a\in H_+^{r_i}(\mathbb F)\).  At every simultaneous product
contact \(z=x_a\), put

\[
 z_i=\dim_{\mathbb F}\ker X_i(x),\qquad
 q_i=\operatorname {rank}_{\mathbb F}\sum_{a=1}^h
                       \lambda_aY_i^a(x_a),\qquad \lambda_a>0.
                                                               \tag{3}
\]

Then

\[
       \boxed{\displaystyle
          \sum_i z_i\geq h,\qquad \sum_iq_i\geq h.}                  \tag{4}
\]

If all block orders satisfy \(r_i\leq R\), put

\[
             a_{\mathbb F}=\dim_{\mathbb R}\mathbb F,
             \qquad b_{\mathbb F}=a_{\mathbb F}(R-1).
\]

The same pointwise argument gives the stronger sourcewise bound

\[
 \boxed{\displaystyle
   \sum_i z_i\geq
       \sum_{a=1}^h\left\lceil{s_a-1\over b_{\mathbb F}}\right\rceil,
   \qquad
   \sum_i q_i\geq
       \sum_{a=1}^h\left\lceil{s_a-1\over b_{\mathbb F}}\right\rceil.}
                                                                    \tag{4a}
\]

Thus one PSD block may serve several polar rows, but it must spend at least
one independent kernel direction per productive source ball.  The result is
pointwise and does not require ranks or active labels to remain constant.

If the primal factors in (2) are boundary points in the closure of one
strictly feasible affine lift slice, restriction of the standard product
log-determinant barrier satisfies

\[
                         \nu_{\rm std,slice}\geq h.                      \tag{5}
\]

Under the order cap, this sharpens to

\[
 \boxed{\displaystyle
   \nu_{\rm std,slice}\geq
       \sum_{a=1}^h\left\lceil{s_a-1\over b_{\mathbb F}}\right\rceil.}
                                                                    \tag{5b}
\]

This is sharp.  Put \(a=\dim_{\mathbb R}\mathbb F\) and

\[
                   p=\max_a\left\lceil{s_a\over a}\right\rceil.
                                                               \tag{6}
\]

There is a one-factor \(H_+^{p+h}(\mathbb F)\) lift with a globally
polynomial primal sheet, total boundary nullity \(h\), and exact restricted
standard-barrier parameter \(h\).  Hence (4)--(5) are exact whenever the
order cap is at least \(p+h\).

More strongly, on this fixed one-factor slice the optimum over **all**
nondegenerate self-concordant barriers, including coupled and
non-logarithmically homogeneous barriers, is exactly

\[
                         \boxed{\vartheta_{\rm opt}=h.}                 \tag{5a}
\]

Thus the lower value is intrinsic to the packed formulation, not an
artifact of using the standard log-determinant.

For \(\mathbb F=\mathbb R\), (4) is the private-nullity statement in
[PSD column packing shares full product-ball slack
rows](2026-09-04-psd-column-packing-product-balls.md).  The argument below
shows that it is field-independent and isolates the pointwise theorem from
the stronger capacity and order-cap questions.

## Proof of the private-nullity law

Fix \(x\in\prod_aS^{s_a-1}\).  Nonnegativity of every summand in (2) and
vanishing of the \(a\)-th slack at \(z=x_a\) give

\[
                  X_i(x)Y_i^a(x_a)=0\qquad(i,a).                         \tag{7}
\]

Write

\[
 E_i=\ker X_i(x),\qquad U_{ia}=\operatorname{Ran}Y_i^a(x_a)\subseteq E_i,
 \qquad U_{i,-a}=\sum_{d\ne a}U_{id}.                                  \tag{8}
\]

The identity in (7) is cylindrical: while its row index \(d\) is fixed,
it remains true as every unrelated primal block \(x_a\), \(a\ne d\),
varies.  Differentiating in such an \(x_a\)-direction gives

\[
                    dX_i(x)[u_a],U_{id}=0\qquad(d\ne a).              \tag{9}
\]

Adapt coordinates to
\(\operatorname{Ran}X_i(x)\oplus E_i\).  The only part of
\(dX_i[u_a]\) that can enter the mixed derivative of (2) is its
off-diagonal map

\[
              B_{ia}(u_a):E_i\longrightarrow\operatorname{Ran}X_i(x).
                                                                        \tag{10}
\]

Equation (9) says that \(B_{ia}(u_a)\) annihilates \(U_{i,-a}\).  The
off-diagonal part of \(dY_i^a[v_a]\) maps
\(\operatorname{Ran}X_i(x)\) into \(U_{ia}\).  Consequently the
\(i\)-th contribution to the \(a\)-th mixed slack form factors through

\[
              U_{ia}/(U_{ia}\cap U_{i,-a}).                             \tag{11}
\]

Set

\[
             d_{ia}=\dim_{\mathbb F}
                 U_{ia}/(U_{ia}\cap U_{i,-a}).                          \tag{12}
\]

If every \(d_{ia}\) were zero for a fixed source \(a\), every factor's
mixed form for that row would vanish.  This contradicts mixed
differentiation of the left side of (2), whose restriction to
\(T_{x_a}S^{s_a-1}\) is the nondegenerate Euclidean metric.  Therefore

\[
                         \sum_i d_{ia}\geq1\qquad(a=1,\ldots,h).       \tag{13}
\]

For fixed \(i\), choose a complement
\(P_{ia}\subseteq U_{ia}\) to \(U_{ia}\cap U_{i,-a}\).  These
subspaces are jointly independent.  Indeed, if \(\sum_av_a=0\) with
\(v_a\in P_{ia}\), then

\[
            v_a=-\sum_{d\ne a}v_d\in U_{ia}\cap U_{i,-a},
\]

so \(v_a=0\) for every \(a\).  Hence

\[
 \sum_a d_{ia}\leq
 \dim_{\mathbb F}\sum_aU_{ia}=q_i
 \leq\dim_{\mathbb F}E_i=z_i.                                      \tag{14}
\]

Summing (13) over \(a\), then applying (14), proves (4).

For the capped refinement, the real rank of the \(i\)-th mixed channel in
row \(a\) is at most

\[
 a_{\mathbb F}\,\operatorname{rank}_{\mathbb F}X_i(x)\,d_{ia}
       \leq a_{\mathbb F}(R-1)d_{ia}.
\]

Indeed, if \(d_{ia}>0\), then \(U_{ia}\ne0\) lies in \(\ker X_i(x)\), so
\(\operatorname{rank}_{\mathbb F}X_i(x)\leq r_i-1\leq R-1\); if
\(d_{ia}=0\), the channel vanishes.  Since the sum of the row-\(a\) mixed
channels is the rank-\((s_a-1)\) sphere metric,

\[
  \sum_i d_{ia}\geq
       \left\lceil{s_a-1\over a_{\mathbb F}(R-1)}\right\rceil.
                                                                    \tag{14a}
\]

Summing (14a) over the sources and using (14) proves (4a).

The equality
\(\operatorname {Ran}(\sum_a\lambda_aY_i^a)=\sum_aU_{ia}\) used in
(14) holds because all weights are positive and all summands are PSD.
Thus, whenever the row factors are genuine affine-slice dual certificates,
the same argument lower-bounds the Jordan rank of the dual exposing slack
for every positive weighted simultaneous-contact objective.  Combined with
[the exposed-rank Dikin theorem for symmetric
cones](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md), it
gives a path-independent standard-barrier distance coefficient at least

\[
 \sqrt{\sum_{a=1}^h
       \left\lceil{s_a-1\over a_{\mathbb F}(R-1)}\right\rceil}
\]

in front of \(\log(1/\epsilon)\), with the exact finite constant determined
by that theorem's exposed eigenvalues and reference minor.

For an affine lift with relative Slater, join the selected boundary fiber
to an interior fiber.  The \(i\)-th Jordan determinant vanishes to exact
order \(z_i\).  The one-dimensional barrier-gradient inequality therefore
gives \(\nu_{\rm std,slice}\geq\sum_i z_i\), and (5) follows from (4).

## Sharp one-block construction

Choose real-linear isometries \(\mathbb R^{s_a}\hookrightarrow\mathbb
F^p\), and write the embedded ball coordinates as the columns
\(w_a\in\mathbb F^p\) of \(W\in\mathbb F^{p\times h}\).  Introduce
\(S\in H^h(\mathbb F)\) and impose

\[
       Z=\begin{pmatrix}S&W^*\\W&I_p\end{pmatrix}\succeq0,
       \qquad S_{aa}=1\quad(a=1,\ldots,h).                              \tag{15}
\]

Schur complementation gives \(D=S-W^*W\succeq0\), so the diagonal
constraints imply \(\|w_a\|^2\leq1\).  Conversely, any product-ball point
is feasible by taking

\[
                         S=W^*W+\operatorname{Diag}(\delta_a),
                         \qquad \delta_a=1-\|w_a\|^2.                  \tag{16}
\]

Interior points admit \(D\succ0\).  At a product extreme every diagonal
of \(D\) is zero; positivity forces \(D=0\).  Thus the boundary fiber is
unique, polynomial, and has nullity \(h\).

For a row \(a\), embed \(z\) as \(\widetilde z\in\mathbb F^p\) and set

\[
 v_a(z)=\binom{e_a}{-\widetilde z},\qquad
 Y^a(z)={1\over2}v_a(z)v_a(z)^* .                                      \tag{17}
\]

Then, on the boundary sheet \(S=W^*W\),

\[
                    \langle Z,Y^a(z)\rangle
                     ={1\over2}\|w_a-\widetilde z\|^2
                     =1-x_a^Tz.                                       \tag{18}
\]

Finally, on the affine slice,

\[
                       -\log\det Z=-\log\det(S-W^*W).                  \tag{19}
\]

Self-concordance follows because (19) is the affine restriction of the
standard order-\((p+h)\) PSD barrier to matrices whose lower block is
\(I_p\).  Its sharper gradient parameter is \(h\).  To see this, use the
affine translations and congruences of the matrix epigraph to move any
\((S,W)\) to \((D,W)=(I_h,0)\).  In a direction
\((A,U)\),

\[
 D(t)=I_h+tA-t^2U^*U,qquad
 F'(0)=-\operatorname{Re}\operatorname{tr}A,qquad
 F''(0)=\operatorname{Re}\operatorname{tr}(A^2)+2\|U\|_F^2.           \tag{20}
\]

The squared local dual norm of the gradient is therefore exactly \(h\).
Restricting further to the diagonal equations in (15) cannot increase that
norm, so the slice parameter is at most \(h\).  The boundary-nullity lower
bound at a product extreme is \(h\), proving exactness.

To prove the arbitrary-coupled lower bound (5a), project the packed domain
onto \(W\).  For a fixed interior \(W\), the completion fiber is

\[
 \left\{D\in H_{++}^h(\mathbb F):
       D_{aa}=1-\|w_a\|^2\right\}.                                    \tag{21}
\]

It is nonempty and bounded: Hermitian positivity gives
\(|D_{ab}|^2<D_{aa}D_{bb}\).  Therefore exact partial minimization of any
\(\vartheta\)-self-concordant barrier over the completion fiber produces a
\(\vartheta\)-self-concordant barrier on
\(\prod_a\operatorname{int}B_2^{s_a}\).  Restrict that projected barrier
to one radial line in each ball.  The resulting affine section is the
\(h\)-cube \((-1,1)^h\), whose corner has \(h\) independent active facets;
the Nesterov--Nemirovskii facet lower bound gives
\(\vartheta\geq h\).  Together with the standard-barrier upper bound, this
proves (5a).

For comparison with the capped lower bound, partition the coordinates of
each source ball into groups of at most \(b_{\mathbb F}\) real coordinates.
For each group, use one Schur-complement epigraph block of order at most
\(R\), and fix the sum of its scalar epigraph variables to one within that
source.  This gives the standard-barrier upper bound

\[
 \nu_{\rm std,slice}\leq
       \sum_{a=1}^h\left\lceil{s_a\over b_{\mathbb F}}\right\rceil.
                                                                    \tag{21a}
\]

The lower and upper ledgers differ by at most one per source, and only when
\(b_{\mathbb F}\mid(s_a-1)\).  For one source the exact resolution is in
[The exact Hermitian PSD standard-slice barrier frontier for a Euclidean
ball](2026-09-04-hermitian-psd-standard-slice-barrier-frontier.md).  A
simultaneous additive resolution of every divisible source is not claimed
here.

## Scope

The lower bounds require differentiable labelled factors at the product
contact; global rank constancy and support-map topology are unnecessary.
The boundary-nullity barrier conclusion additionally requires the selected
primal factors to belong to the closure of the same strictly feasible
affine slice.  The stronger arbitrary-barrier conclusion (5a) concerns the
specific one-block packed slice (15); it is still not an iteration lower
bound.

The construction shows that factorwise no-sharing is false: one Hermitian
PSD factor serves all \(h\) slack-row families.  What cannot be shared is
the private kernel dimension charged by (11)--(14).

An independent hostile audit verified (7)--(14), including rank-changing
PSD factors, kernel--kernel derivative compression, and the complex and
quaternionic extensions with \(\mathbb F\)-dimensions and real trace
pairing.  It also checked the real-linear embeddings, quaternionic Schur
calculus, transitive epigraph normalization, exact gradient norm, and
boundary-nullity lower bound in the one-block construction.  It found no
correction.

A separate hostile audit checked the capped refinement.  Differentiating
the cylindrical matrix identity \(X_iY_i^d=0\) makes the off-diagonal
primal derivative annihilate \(U_{i,-a}\); the row-\(a\) mixed channel
therefore factors through a real Hom space of dimension
\(a_{\mathbb F}\operatorname{rank}_{\mathbb F}(X_i)d_{ia}\).  This proves
(14a), and joint independence of the private complements gives (4a) and
(5b).  For (21a), a group of at most
\(a_{\mathbb F}(R-1)\) real coordinates embeds isometrically in
\(\mathbb F^{R-1}\); one order-\(R\) Schur epigraph block per group and
one scalar-sum equation per source give precisely the stated standard
restricted-barrier upper bound.  The lower and upper ceilings and their
divisibility gap are stated correctly.

A further hostile audit checked the exposed-dual-rank strengthening in
(3)--(4a).  For positive weights, the kernel of
\(\sum_a\lambda_aY_i^a\) is the intersection of the kernels of the PSD
summands, so its range is exactly \(\sum_aU_{ia}\), even when the row
supports overlap.  The jointly independent private complements therefore
charge \(\sum_a d_{ia}\) to the exposed rank \(q_i\).  Subject to the
explicit affine-slice-certificate hypothesis above, the coefficient
\(\sqrt{\sum_a\lceil(s_a-1)/(a_{\mathbb F}(R-1))\rceil}\) then follows
directly from the exposed-rank Dikin theorem; its remaining finite scale is
the theorem's reference-minor constant.

The bounded-fiber partial-minimization argument is the field-uniform version
of the independently audited real theorem
[*The one-block PSD product-ball lift has intrinsic barrier parameter
\(b\)*](2026-09-04-one-block-psd-packing-coupled-barrier.md).  Exact partial
minimization with bounded fibers is Chares, *Cones and Interior-Point
Algorithms for Structured Convex Optimization Involving Powers and
Exponentials*, Theorem 5.2.1.  Complex and quaternionic completion fibers
obey the same spectral positivity and boundedness proof.

A second hostile audit checked this coupled extension in the real Euclidean
model underlying \(H^h(\mathbb F)\): boundedness from Hermitian
Cauchy--Schwarz, existence and uniqueness of the fiber minimizer, the
Schur/envelope derivatives preserving self-concordance and its gradient
parameter, the radial-cube lower bound, and the quaternionic Jordan
determinant/real-trace conventions.  It found no correction.
