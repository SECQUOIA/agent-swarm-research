# Constant boundary nullity removes the need for global lift selections

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the stated constant-nullity theorem; deriving its
hypothesis from a barrier bound alone remains open

## Result

Let \(B_2^N\), \(N\geq3\), have a strictly feasible semialgebraic affine
lift over a finite product of irreducible symmetric cones \(K_i\), each of
dimension at most \(d<N+1\).  Let \(E\) be the set of all feasible lifted
points projecting to \(S^{N-1}\), and assume that \(E\) is compact.  For
\(w\in E\), write

\[
                 Z(w)=\sum_i z_i(w),                                    \tag{1}
\]

where \(z_i(w)\) is the Jordan nullity of its \(i\)-th cone coordinate.
Suppose

\[
              N-1=L(d-2),\qquad Z(w)=L\quad\text{for every }w\in E.     \tag{2}
\]

Then no such lift exists.

Equivalently, in the divisible capped case, every exact symmetric-cone
lift has some boundary fiber point whose total nullity differs from \(L\).
This conclusion does **not** assume a globally labelled \(C^1\) primal
selection.  The constant-nullity condition makes the block supports
intrinsic to each projected boundary point and produces the required
continuous global maps automatically.

For the restricted standard product Jordan barrier, a parameter bound
\(\nu_{\rm std,slice}\leq L\) implies only

\[
                              Z(w)\leq L\qquad(w\in E).                  \tag{3}
\]

It does not by itself prove the reverse inequality at boundary lift points
that lie on projection-singular branches.  Thus the theorem does not yet
remove all regularity assumptions from the exact standard-slice frontier.
It identifies the remaining issue precisely: an equality-saving lift must
contain a boundary point of nullity below \(L\) that is inaccessible to the
generic curvature sheets.

## 1. The boundary lift is connected and ranks are fixed

Projection \(\pi:E\to S^{N-1}\) is a continuous surjection.  Every fiber
is convex, hence connected.  If compact \(E\) had a separation into two
nonempty clopen sets, each connected fiber would lie in one side.  The two
images would then be disjoint compact sets covering the connected sphere,
a contradiction.  Hence \(E\) is connected.

Each integer-valued Jordan nullity \(z_i\) is upper semicontinuous.  Since
their finite sum is constant on \(E\), every \(z_i\) is locally constant:
near \(w\), upper semicontinuity gives
\(z_j(w')\leq z_j(w)\) for all \(j\), and equality of the sums forces
equality term by term.  Connectedness makes every block nullity constant
on all of \(E\).

## 2. Supports are constant on each convex fiber

Fix \(x\in S^{N-1}\) and \(w,w'\in E_x\).  Their segment lies in the same
convex fiber.  Every point on it has the same rank in every block.  For
positive elements of a symmetric cone, the support idempotent of a positive
combination is the join of the endpoint supports.  If the ranks of both
endpoints and their midpoint agree, those supports must coincide.  Thus

\[
                    \operatorname{supp}w_i
                    =\operatorname{supp}w_i'\qquad(i=1,\ldots,k).      \tag{4}
\]

The support map on \(E\) is continuous because the ranks are constant.
Since a continuous surjection from compact \(E\) to the Hausdorff sphere is
a quotient map, (4) gives unique continuous descended maps

\[
                   \sigma_i:S^{N-1}\longrightarrow\mathcal O_i,       \tag{5}
\]

where \(\mathcal O_i\) is the fixed-rank idempotent orbit of \(K_i\).

## 3. Generic curvature forces Lorentz blocks

Semialgebraic choice supplies primal and dual slack-factor selections that
are \(C^1\) on a common dense open subset of the contact sphere.  Strict
feasibility supplies the dual certificates by strong conic duality; any
free lift variables are annihilated by the dual equality equations and do
not enter the cone pairing.  At such a contact, let \(I_+\) denote the
non-ray factors and
\(Z_+=\sum_{i\in I_+}z_i\).  The Peirce mixed-curvature chain is

\[
 N-1
 \leq\sum_{i\in I_+} a_ip_iq_i
 \leq\sum_{i\in I_+} a_i(r_i-1)z_i
 \leq\sum_{i\in I_+}(m_i-2)z_i
 \leq(d-2)Z_+
 \leq(d-2)Z.                                                        \tag{6}
\]

Equations (2) and (6) make every inequality an equality.  Every
positive-nullity active factor is therefore a rank-two spin factor of full
dimension \(d\), with primal and dual Jordan ranks one and nullity one.
Equality also forces every ray nullity to vanish.  There are exactly \(L\)
active non-ray factors.  A zero-nullity block is primal
interior on all of \(E\), so diagonal complementarity makes its dual slack
factor vanish.  Hence the entire full slack is carried by the \(L\)
Lorentz factors.

The descended maps (5) for those factors combine to

\[
                 \Sigma:S^{N-1}\longrightarrow(S^{d-2})^L.            \tag{7}
\]

## 4. Full slack makes the descended map injective

Suppose \(\Sigma(x')=\Sigma(x)\).  Choose any lift point above \(x'\) and
any dual certificate for the supporting row indexed by \(x\).  In every
active Lorentz block, equality of the primal support ray makes it
complementary to the dual factor at \(x\).  All zero-nullity blocks have
zero dual factor.  The cross slack therefore vanishes:

\[
                              1-(x')^Tx=0.                              \tag{8}
\]

Thus \(x'=x\), so \(\Sigma\) is injective.

By (2), source and target in (7) have the same dimension.  Invariance of
domain makes the image open; compactness makes it closed.  The target is
connected, so \(\Sigma\) is a homeomorphism onto the full product.  If
\(L>1\), a product of positive-dimensional spheres is not a sphere, by its
intermediate cohomology (with the circle case also detected by fundamental
groups).  If \(L=1\), equality of dimensions gives \(d=N+1\), contrary to
the cap.  This proves the theorem.

## 5. Heterogeneous product-ball extension

The same argument has a sharp nonvacuous product version.  Let

\[
 C_{\rm prod}=\prod_{a=1}^h B_2^{s_a},\qquad
 M_{\rm prod}=\prod_{a=1}^h S^{p_a},\qquad
 p_a=s_a-1\geq1,\qquad n=\sum_a p_a.                    \tag{9}
\]

Let \(E_{\rm prod}\) be the set of all feasible lift points above the
simultaneous extreme stratum \(M_{\rm prod}\).  Under the same strict
feasibility, semialgebraicity, cone-dimension cap \(d\), and compactness
assumptions, suppose

\[
                       n=L(d-2),\qquad Z(w)=L
                       \quad(w\in E_{\rm prod}).          \tag{10}
\]

Then necessarily

\[
                  \boxed{\ \{p_a:a\in[h]\}
                         =\{\underbrace{d-2,\ldots,d-2}_{L\ {\rm times}}\}\ }.
                                                               \tag{11}
\]

Indeed, \(M_{\rm prod}\) is connected and its lift fibers are convex, so
Sections 1--2 again descend every block support.  On a common dense open
subset of the simultaneous contact stratum, mixed differentiation of all
rows gives the product metric.  The equality chain (6), with \(N-1\)
replaced by \(n\), forces exactly \(L\) full-dimensional \(Q_d\) blocks
of nullity one.  Ray nullities vanish and every other dual row factor is
zero exactly as before.  The descended support map is

\[
             \Sigma_{\rm prod}:M_{\rm prod}
                      \longrightarrow(S^{d-2})^L.         \tag{12}
\]

If two source points have the same support tuple, evaluating the dual
certificate for row \(a\) at the other source point gives
\(1-(x_a')^Tx_a=0\) for every \(a\).  Thus the points agree.
Invariance of domain makes (12) a homeomorphism.  The graded
indecomposable quotient of mod-two cohomology records one generator in
each sphere dimension, including degree one, and proves (11).

The exceptional profile (11) is attained by the standard separate
Lorentz lift: it has \(h=L\), every source ball has dimension \(s_a=d-1\),
and one \(Q_d=Q_{s_a+1}\) block serves each source.  Thus the product
theorem is an exact rigidity statement, not a universal impossibility.
In particular, for a homogeneous product of \(s\)-dimensional balls,
constant-nullity capacity equality is possible only when \(d=s+1\) and
\(L=h\).  No cross-source sharing survives at equality.

## 6. A useful accessibility corollary

The constant-nullity hypothesis follows from a barrier bound under the
following explicit additional condition.  Call a point \(w\in E\)
**contact-accessible** if there are regular contact points \(x_j\to\pi(w)\)
and locally \(C^1\) primal/dual selections with selected primal values
\(w_j\to w\).  If every point of \(E\) is contact-accessible and
\(\nu_{\rm std,slice}\leq L\), then (6) gives \(Z(w_j)\geq L\), while
upper semicontinuity gives

\[
                  Z(w)\geq\limsup_jZ(w_j)\geq L.                        \tag{13}
\]

Together with (3), this yields (2), so the lift is impossible.  A family
of local \(C^1\) sheets passing through every point of \(E\) implies
accessibility.  A single global selection proves accessibility only for
the points in its image and is not enough when a boundary fiber has other
points.  The condition allows sheet changes and need only hold pointwise
through limiting regular contacts.

## Scope

Compactness of \(E\), semialgebraicity, and exact constant total nullity
are used essentially.  Compactness makes the descended support map a
quotient construction; semialgebraicity supplies the generic differentiable
factor selections; constant nullity fixes ranks and forces support
uniqueness across convex fibers.

No claim is made that an arbitrary affine lift has compact boundary fibers
or that every such fiber point is contact-accessible.  A nonsmooth lift can
have lower-dimensional projection-singular branches.  Showing that a
standard-barrier equality bound rules those branches out, or constructing a
counterexample that uses them, is the remaining route to an unconditional
theorem.

The local curvature chain and equality classification are from
[Exact standard-slice barrier frontier for capped symmetric-cone ball
lifts](2026-09-04-symmetric-cone-standard-slice-barrier-frontier.md).  The
new contribution here is the fiberwise support descent (4)--(5), which
replaces a chosen global primal sheet by an intrinsic continuous map.

## Independent hostile audit

The audit checked connectedness of \(E\) from compactness and connected
convex fibers, upper semicontinuity plus constant total nullity, the
support-of-a-sum argument in a Euclidean Jordan algebra, continuity and
quotient descent of constant-rank supports, and semialgebraic generic
primal/dual choices.  It rederived every equality case in (6), including
the disappearance of ray and zero-nullity dual factors, and verified that
full cross slack makes the descended Lorentz support map injective.
Invariance of domain and the sphere-versus-product obstruction then give
the claimed contradiction.

The audit also checked the accessibility limit using upper
semicontinuity.  It corrected the scope statement: accessibility of every
fiber point requires local sheets through every point, not merely one
global single-valued selection.  Free lift variables cause no additional
term after the dual equality equations, and strict feasibility provides
the supporting dual certificates used in the proof.

The heterogeneous extension was checked by replacing the round contact
sphere with its simultaneous product-sphere stratum.  The same equality
chain and ray deletion apply, the full row family makes the product support
map injective coordinate by coordinate, and the mod-two indecomposable
quotient proves the exact multiset condition (11).  The direct
\(Q_d=Q_{s_a+1}\) attainment has \(s_a=d-1\), as required by
\(p_a=d-2\).
