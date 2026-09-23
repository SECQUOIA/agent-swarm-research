# Exact standard-slice barrier frontier for capped symmetric-cone ball lifts

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Headline theorem

Let \(B_2^N\), \(N\geq2\), have a proper affine lift over a product of
irreducible symmetric cones,

\[
 B_2^N=\{\pi w:w\in K,\ Aw=b\},\qquad
 K=\prod_{i=1}^sK_i,                                     \tag{1}
\]

with a relative Slater point \(w^\circ\in\operatorname{int}K\).  Suppose
every non-ray factor \(K_i\) has real dimension \(m_i\leq d\), and suppose
the lift admits globally labelled \(C^1\) primal and polar factor selections
on the paired boundary spheres.  Restrict the standard product Jordan
barrier

\[
                         F(w)=-\sum_i\log\det_i w_i        \tag{2}
\]

to the affine slice \(Aw=b\).  Write
\(\nu_{\mathrm{std,slice}}(F)\) for the smallest self-concordant-barrier
gradient parameter of this restricted barrier.

Then the exact optimum over this regularity class is

\[
 \boxed{
 \inf\nu_{\mathrm{std,slice}}=
 \begin{cases}
 \displaystyle\left\lceil {N\over d-2}\right\rceil,
      &3\leq d<N+1,\\[3mm]
 1,   &d\geq N+1.
 \end{cases}}                                             \tag{3}
\]

The first line is attained by the grouped Lorentz lift, and the second by
one direct \(Q_{N+1}\) factor.  The result concerns the particular standard
product barrier after affine restriction.  It is not a lower bound for an
arbitrary custom or coupled barrier on the same lifted domain, and it is
not by itself an iteration lower bound.

## Boundary order equals total primal nullity

Let \(X(x)=(X_i(x))_i\) be a selected feasible fiber over
\(x\in\partial B_2^N\).  Put

\[
 p_i(x)=\operatorname{rank}X_i(x),\qquad
 z_i(x)=r_i-p_i(x),\qquad Z(x)=\sum_i z_i(x),              \tag{4}
\]

where \(r_i\) is the Jordan rank of \(K_i\).  On the feasible segment

\[
                   w(t)=(1-t)X(x)+t w^\circ,\qquad t>0,   \tag{5}
\]

the \(i\)-th determinant has a zero of exact order \(z_i(x)\):

\[
                   \det_i w_i(t)=c_i(x)t^{z_i(x)}(1+O(t)),
                   \qquad c_i(x)>0.                       \tag{6}
\]

One direct proof applies the quadratic representation associated with
\((w_i^\circ)^{-1/2}\), reducing the interior endpoint to the Jordan unit.
The transformed \(X_i(x)\) is positive with the same rank, so the spectral
theorem gives
\(\det(\widetilde X_i+t e)=\prod_{j\leq p_i}(\lambda_j+t)t^{z_i}\).
The affine parameter in (5) differs only by an invertible rescaling near
\(t=0\), proving (6).

Consequently the one-variable restriction \(f_x(t)=F(w(t))\) obeys

\[
 f_x(t)=-Z(x)\log t+O(1),\quad
 f_x'(t)=-{Z(x)\over t}+O(1),\quad
 f_x''(t)={Z(x)\over t^2}+O(1).                           \tag{7}
\]

If the restricted barrier has gradient parameter \(\nu\), its defining
inequality along this feasible line is

\[
                         |f_x'(t)|^2\leq\nu f_x''(t).      \tag{8}
\]

Letting \(t\downarrow0\) in (7)--(8) proves the coordinate-invariant lower
bound

\[
                         \nu_{\mathrm{std,slice}}\geq Z(x)
                    \quad\text{for every }x\in\partial B_2^N. \tag{9}
\]

This is a boundary multiplicity statement, not an appeal to the ambient
normal parameter \(\sum_i r_i\), which can be strictly larger after
restriction.

## Curvature forces nullity

Let \(a_i\) be the Peirce constant of \(K_i\).  At the contact paired with
\(x\), let \(q_i\) be the Jordan rank of its dual factor.  Complementarity
gives \(q_i\leq z_i=r_i-p_i\).  The mixed Peirce-channel theorem and
nondegeneracy of the ball's tangent slack give

\[
 \begin{aligned}
 N-1
 &\leq\sum_{i\ {\rm nonray}}a_i p_iq_i\\
 &\leq\sum_{i\ {\rm nonray}}a_i(r_i-1)z_i\\
 &\leq\sum_{i\ {\rm nonray}}(m_i-2)z_i\\
 &\leq(d-2)Z(x).                                          \tag{10}
 \end{aligned}
\]

The second line also covers \(z_i=0\): complementarity then gives \(q_i=0\).
For \(z_i>0\), use \(q_i\leq z_i\) and \(p_i\leq r_i-1\).  The third line
follows from

\[
 m_i=r_i+{a_i\over2}r_i(r_i-1),\qquad
 a_i(r_i-1)\leq m_i-2.                                   \tag{11}
\]

Ray blocks have no mixed-curvature channel and are omitted from the first
three sums; their nonnegative nullity is harmless in the last bound.
Equations (9)--(10) already give

\[
 \nu_{\mathrm{std,slice}}
       \geq\left\lceil{N-1\over d-2}\right\rceil.          \tag{12}
\]

## Excluding the divisible equality case

For \(3\leq d<N+1\), the desired lower bound in (3) differs from (12) only
when

\[
                   N-1=L(d-2)                            \tag{13}
\]

is divisible by \(d-2\).  Suppose for contradiction that the restricted
barrier's selected boundary fibers all satisfy \(Z(x)\leq L\).  Equation
(10) forces

\[
                              Z(x)=L                       \tag{14}
\]

at every boundary point and equality throughout (10).

Each nullity \(z_i(x)\) is integer-valued and upper semicontinuous.  Since
their finite sum is constant in (14), every \(z_i\) is locally constant:
near a fixed point, upper semicontinuity makes all \(z_i\) no larger, and
the constant sum prevents any strict decrease.  Connectedness makes every
nullity constant globally.

Equality in the blockwise inequalities of (10)--(11) is rigid.  Every block
with positive nullity has

\[
 q_i=z_i=1,\qquad p_i=r_i-1,\qquad r_i=2,\qquad m_i=d.    \tag{15}
\]

Indeed, equality in \(a_ip_iq_i\leq a_i(r_i-1)z_i\) gives the first two
rank statements, while

\[
 (m_i-2)-a_i(r_i-1)
   =(r_i-2)\left(1+{a_i(r_i-1)\over2}\right)              \tag{16}
\]

shows that equality in (11) requires \(r_i=2\).  Thus every active block is
a \(d\)-dimensional spin factor \(Q_d\), exactly \(L\) such blocks are
active, and no ray has positive nullity.

At every contact, each active rank-one Lorentz block uses all of its
\(d-2\) mixed channels.  Normalizing its boundary ray therefore gives a
\(C^1\) submersion

\[
                             S^{N-1}\longrightarrow S^{d-2}. \tag{17}
\]

The joint normalized support map is a same-dimensional local
diffeomorphism

\[
                       S^{N-1}\longrightarrow(S^{d-2})^L. \tag{18}
\]

It is a finite covering.  If \(L>1\), product cohomology contradicts the
intermediate-cohomology vanishing of a sphere when \(d-2\geq2\): the target
is then simply connected, so the covering is a diffeomorphism.  If
\(d-2=1\), the target is a torus; its universal cover is noncompact, so it
cannot have the compact simply connected sphere \(S^{N-1}\), \(N-1\geq2\),
as a covering space.  If \(L=1\), equation (13) gives \(d=N+1\), contrary
to the strict cap assumption.  This excludes (14).  Hence some boundary
point has integer nullity \(Z(x)\geq L+1\), and (9) sharpens (12) to

\[
                    \nu_{\mathrm{std,slice}}
                       \geq\left\lceil{N\over d-2}\right\rceil. \tag{19}
\]

The constancy argument is why global labels and global \(C^1\) regularity
matter.  With only a generic smooth stratum, active blocks can switch across
singular seams and the covering proof does not apply.

## Matching grouped Lorentz barrier

Partition the \(N\) coordinates into
\[
                         k=\left\lceil{N\over d-2}\right\rceil            \tag{20}
\]
groups \(G\) of size at most \(d-2\).  The grouped lift is

\[
                    s_G\geq\|x_G\|^2,\qquad \sum_Gs_G=1,  \tag{21}
\]

obtained by an affine slice of \(Q_{|G|+2}\) for every group.  Restricting
the standard Lorentz product barrier gives

\[
                     F_{\rm grp}(s,x)
                        =-\sum_G\log(s_G-\|x_G\|^2).       \tag{22}
\]

Each summand in (22) is a standard self-concordant barrier with exact
gradient parameter one, so restriction to the final sum equation has
parameter at most \(k\).  Exactness follows by taking

\[
 s_G={1\over k},\qquad
 \|x_G\|^2={1\over k}-\epsilon                            \tag{23}
\]

and letting \(\epsilon\downarrow0\).  Equivalently, the squared local dual
gradient norm on the tangent space of \(\sum_Gs_G=1\) is

\[
 k-\frac{(\sum_Gq_G)^2}
          {\sum_Gq_G(s_G+\|x_G\|^2)},\qquad
 q_G=s_G-\|x_G\|^2,                                      \tag{24}
\]

which tends to \(k\) in (23).  This proves equality in the first line of
(3).

For \(d\geq N+1\), the direct Lorentz slice has

\[
                            F_{\rm dir}(x)=-\log(1-\|x\|^2). \tag{25}
\]

It has exact parameter one: it is the affine restriction of the standard
Lorentz barrier and its one-dimensional boundary order is one.  This proves
the second line of (3).

## Scope and QIPM interpretation

The ambient product normal parameter of the grouped construction is \(2k\),
whereas the exact parameter of its displayed restricted barrier is \(k\).
Thus the exact cap-dependent short-step envelopes differ by a factor
\(\sqrt2\) if one analysis can work directly with the reduced affine-slice
barrier.  Neither parameter alone specifies per-iteration linear-system
cost, conditioning, state preparation, output materialization, or oracle
access.  The theorem should therefore be used as a formulation/barrier
ledger, not as an unconditional quantum speedup or lower bound.

The proof applies verbatim to any \(C^1\), strictly convex \(N\)-body with
globally labelled bi-\(C^1\) lift factors and contact sphere \(S^{N-1}\);
only the explicit upper construction and hence exact optimum are
Euclidean-ball-specific.

## Relation to other notes

The local Peirce inequality used in (10) is proved in
[Curvature capacity of symmetric-cone lifts](2026-09-04-symmetric-cone-curvature-capacity.md).
The global joint-map argument is developed in
[Saturated symmetric-cone factors induce idempotent-orbit
coverings](2026-09-04-symmetric-cone-support-orbit-rigidity.md).
The grouped construction, its exact reduced parameter, and its sparse
Newton graphs are also recorded in
[Exact ball-cap latent-treewidth Pareto frontier](2026-09-04-ball-cap-latent-treewidth-pareto.md).

## Audit checklist

- Verify exact determinant order \(z_i\) in (6) for every simple EJA,
  including the Albert algebra.
- Check that the one-dimensional asymptotic (7) forces the full restricted
  barrier parameter to be at least \(Z(x)\).
- Check all inequalities and equality cases in (10)--(16), especially ray
  factors and blocks with \(z_i=0\).
- Verify that constant total nullity plus upper semicontinuity fixes every
  block nullity globally.
- Check the Lorentz joint-map covering argument when some other factors
  remain interior along the boundary.
- Verify the exact grouped-slice parameter (24), including restriction to
  the final affine equality.
- Preserve the distinction between the standard restricted barrier,
  arbitrary custom barriers, and the ambient normal-barrier parameter.

## Independent hostile audit

Two independent audits checked the determinant-order argument for every simple EJA,
including the Albert algebra, and verified that the one-dimensional
gradient ratio tends to the total Jordan nullity.  It rederived the entire
curvature--nullity chain, including rays and zero-nullity blocks, and
confirmed that equality forces fixed rank-one \(d\)-dimensional Lorentz
blocks.  It also checked upper semicontinuity, the joint-covering
obstruction in both the circle and higher-sphere cases, and the exact Schur
correction (24) for the grouped lift.

A logical wording issue was corrected after the audit: because a
self-concordance parameter is real, it is not enough merely to rule out
\(\nu\leq L\).  The proof now rules out \(Z(x)\leq L\) at every boundary
point, produces a point with integer \(Z(x)\geq L+1\), and only then invokes
(9).  This yields the stated integer lower bound on the real-valued barrier
parameter.
