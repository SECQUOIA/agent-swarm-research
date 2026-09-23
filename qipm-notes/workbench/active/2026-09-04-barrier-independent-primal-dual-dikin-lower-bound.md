# Barrier-independent bounded-Dikin lower bounds: the primal--dual theorem and the primal obstruction

Status: Proved and independently audited for logarithmically homogeneous primal--dual barriers; the
parameter-only primal projection is disproved, while an objective-nondegenerate
all-barrier extension remains open  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the stated theorem and explicit primal-projection
counterexample; the refined open problem is stated separately

## Main conclusion

The \(\Omega(\sqrt{k}\log(1/\epsilon))\) bounded-Dikin lower bound can be
made independent of the chosen barrier for the homogenized \(k\)-cube and
products of \(k\) balls, provided the algorithm is measured in the
**primal--dual product metric** of an arbitrary logarithmically homogeneous
self-concordant barrier and its conjugate. Starting at an exact central
point, the theorem applies to **every feasible primal--dual output** with
duality gap at most \(\epsilon\), not only to a later central point. It does
not extend to a parameter-only statement in the primal metric: an explicit
product-ball central path below has dimension-free primal length while its
dual projection carries the \(\sqrt{k}\) scale.

The positive result follows from two established facts:

1. Nesterov--Todd's primal--dual central path is
   \(\sqrt2\)-geodesic for every logarithmically homogeneous
   self-concordant barrier.
2. The same paper identifies each central point as the analytic center of
   the corresponding feasible duality-gap sublevel set.
3. An active vertex of the bounded \(k\)-cube forces barrier parameter at
   least \(k\).  For the canonical homogenization of a product of \(k\)
   positive-dimensional balls, restriction to the corresponding
   \(\ell_\infty\) cone gives the sharper homogeneous bound \(k+1\).

There is also a formulation-independent consequence for one smooth,
positively curved body.  If an exact affine lift uses a product of
definable proper cones of dimension at most \(d\), the universal curvature
theorem forces at least
\(\lceil (N-1)/(d-2)\rceil\) non-ray operational factors.  A product of
two-dimensional interior sections then forces every, possibly coupled,
logarithmically homogeneous barrier on that operational cone to have
parameter at least twice this number.  The theorem below therefore turns
the curvature-capacity result into an arbitrary-barrier primal--dual
movement lower bound over *all* such cone dictionaries, not only Lorentz
or PSD dictionaries.

The resulting lower bound is geometric, not an inference from the usual
short-step upper bound.

## 1. General primal--dual theorem

Let \(K\) be a regular cone and let \(F:\operatorname{int}K\to\mathbb R\)
be an arbitrary \(\nu\)-logarithmically homogeneous self-concordant
barrier:
\[
                       F(\alpha x)=F(x)-\nu\log\alpha.                 \tag{1}
\]
Let \(F_*\) be its conjugate barrier on \(K^*\), and equip
\(\operatorname{int}(K\times K^*)\) with
\[
                         \widehat F(x,s)=F(x)+F_*(s).                  \tag{2}
\]
Consider any strictly feasible conic primal--dual pair and its exact
central path \(z(t)=(x(t),s(t))\). In the standard convention,
\[
                         s(t)=-{1\over t}F'(x(t)),                     \tag{3}
\]
and logarithmic homogeneity gives
\[
                    \langle x(t),s(t)\rangle={\nu\over t}.             \tag{4}
\]

Nesterov--Todd's Theorems 4.1 and 5.2 imply
\[
 \operatorname{len}_{\widehat F}
       (z|_{[t_0,t_1]})
     =\sqrt\nu\log{t_1\over t_0}
     \leq\sqrt2\,
       d_{\widehat F}\bigl(z(t_0),z(t_1)\bigr).                         \tag{5}
\]
Consequently every piecewise smooth primal--dual path joining these
central endpoints has length at least
\[
 d_{\widehat F}\bigl(z(t_0),z(t_1)\bigr)
 \geq\sqrt{\nu\over2}\log{t_1\over t_0}
 =\sqrt{\nu\over2}\log{
   \langle x(t_0),s(t_0)\rangle
  \over
   \langle x(t_1),s(t_1)\rangle}.                                      \tag{6}
\]

This statement is barrier-independent within the class (1). No symmetry,
self-scaledness, separability, or standard log barrier is assumed.

There is a stronger endpoint-set form. Define the feasible gap sublevel
\[
 \mathcal Z_\epsilon=
 \{(x,s)\in\operatorname{int}(K\times K^*):
   Ax=b,\ A^Ty+s=c\text{ for some }y,\ \langle x,s\rangle\leq\epsilon\}.
                                                                    \tag{6a}
\]
Nesterov--Todd's Theorem 5.1(c) says that, for
\(t_\epsilon=\nu/\epsilon\), \(z(t_\epsilon)\) minimizes
\(\widehat F\) on \(\mathcal Z_\epsilon\). Conjugacy and logarithmic
homogeneity also give the exact central value
\[
       \widehat F(z(t))=\nu\log t-\nu,
 \qquad
       \|\widehat F'(z)\|_{z,*}=\sqrt{2\nu}.                           \tag{6b}
\]
Let \(\Delta_0=\nu/t_0>\epsilon\). For every
\(z\in\mathcal Z_\epsilon\),
\[
\begin{aligned}
 \widehat F(z)-\widehat F(z(t_0))
   &\geq \nu\log{\Delta_0\over\epsilon},\\
 d_{\widehat F}(z(t_0),z)
   &\geq \sqrt{\nu\over2}\log{\Delta_0\over\epsilon}.
\end{aligned}                                                        \tag{6c}
\]
The second line follows by integrating the \(2\nu\)-barrier gradient
inequality along an arbitrary joining curve. Thus (6c) lower-bounds the
distance to the entire strictly feasible accurate set and does not require
the final point to be central.

## 2. Bounded-Dikin round corollary

Fix \(0<\rho<1\) and an integer \(m\geq1\). Suppose each outer round contains
at most \(m\) chords in \(\operatorname{int}(K\times K^*)\), each having
starting-point local norm at most \(\rho\) in the metric (2).
Self-concordant Hessian comparison bounds the Riemannian length of each
chord by
\[
                             -\log(1-\rho).
\]
If the trajectory starts at the exact central point of gap
\(\Delta_0>\epsilon\) and ends at any point of
\(\mathcal Z_\epsilon\), then (6c) gives
\[
 \boxed{
 T\geq{\sqrt{\nu/2}\log(\Delta_0/\epsilon)
          \over m\log(1/(1-\rho))}.}                                  \tag{7}
\]
An initial metric error can be subtracted from the distance numerator by
the triangle inequality. Equation (7) counts geometric moves only;
arbitrary computation between moves is allowed. Intermediate chords may
even violate the affine primal--dual equations; allowing them does not
weaken the lower bound.

This is an IPM movement lower bound, not an oracle-query lower bound.
It applies equally when the work used to choose each chord is quantum, but
it does not charge a quantum algorithm whose state evolution is not
represented by bounded product-Dikin moves. The endpoint contract is an
explicit or otherwise certified feasible primal--dual pair of gap at most
\(\epsilon\). A primal-only objective guarantee, a normalized state, an SQ
interface, or a scalar estimate does not by itself satisfy that contract.

## 3. Cube and product-ball specialization

The homogenization of \([-1,1]^k\) is the \(\ell_\infty\) cone
\[
 K_{\infty}^{k+1}
   =\{(\tau,x):\tau\geq |x_i|\text{ for every }i\}.                     \tag{8}
\]
Every logarithmically homogeneous self-concordant barrier on this cone has
\(\nu\geq k+1\). Hildebrand proves this sharp bound and gives the optimal
barrier
\[
 -\sum_{i=1}^k\log(\tau^2-x_i^2)+(k-1)\log\tau.
\]
Its restriction to \(\tau=1\) is the usual cube barrier, but (7) applies
to every barrier satisfying (1), not only this optimizer.

For
\[
                           C=\prod_{a=1}^k B_2^{s_a},
 \qquad s_a\geq1,                                                     \tag{9}
\]
use the canonical homogenization
\[
 K_C=\{(\tau,z_1,\ldots,z_k):\tau\geq0,\ \|z_a\|_2\leq\tau
       \text{ for every }a\}.
\]
Choose one diameter in each factor. Its intersection with the resulting
linear subspace is exactly the \(\ell_\infty\) cone
\(K_\infty^{k+1}\). Restricting a
logarithmically homogeneous barrier to this linear section preserves its
homogeneity coefficient and does not increase its self-concordance parameter.
The relative boundary of the section lies in \(\partial K_C\), so the
restriction retains the barrier blow-up property. Hildebrand's sharp cone
bound therefore gives
\[
                              \nu\geq k+1.                             \tag{10}
\]
For \(k=1\), this section is linearly isomorphic to
\(\mathbb R_+^2\), whose parameter lower bound is two; Hildebrand's stated
corollary for cone dimension at least three covers every \(k\geq2\).
Equations (7) and (10) prove, for fixed \(\rho,m\),
\[
                  T=\Omega\!\left(
                       \sqrt{k}\log{\Delta_0\over\epsilon}\right)      \tag{11}
\]
for every logarithmically homogeneous barrier on the canonical conic
homogenization of the product body, when movement is measured in its
primal--dual product metric.

The assumption \(\nu=O(k)\) makes (11) match the usual square-root
parameter scale. The lower bound itself uses \(\nu\geq k+1\).

## 4. Corollaries for the exact lift frontiers

The general theorem can be combined with the exact ambient barrier
parameters proved elsewhere in this workbench. These corollaries concern
the operational cone after any necessary minimal-face reduction. They
require strict primal and dual feasibility in that reduced cone.

An assumption-free dimension alternative is recorded separately in
[Dimension-only movement lower bounds for arbitrary product-cone
dictionaries](2026-09-04-dimension-only-arbitrary-cone-primal-dual-movement.md).
For every full-dimensional compact \(D\)-body and every product-cone lift
with operational block dimension at most \(d\), it gives the exact ledger
\(\nu\geq\Psi_d(D+1)\) and therefore coefficient
\(\sqrt{\Psi_d(D+1)/2}\), without curvature, definability, or regular
contact selections. Section 4.0 below is sharper on a smooth positively
curved body because it replaces ordinary block capacity \(d\) by
curvature capacity \(d-2\).

### 4.0 Universal bounded-dimension definable-cone lifts

Let \(C\subset\mathbb R^N\), \(N\geq2\), be full dimensional and compact,
with a relatively open \(C^2\) boundary patch containing a strictly
positively curved point. Translate an interior point to the origin before
taking the polar; this affine normalization changes neither block dimensions
nor curvature rank. Consider any exact finite-dimensional affine
lift of \(C\) over a product of proper cones that are definable in one
o-minimal structure.  Pass to the minimal operational face, omit zero
factors, and suppose every surviving factor has dimension at most
\(d\geq3\). Let \(q\) and \(r\) be the numbers of surviving non-ray and ray
factors, respectively.

The [universal dimension-minus-two curvature
theorem](2026-09-04-universal-cone-curvature-capacity.md) gives
\[
 q\geq \left\lceil{N-1\over d-2}\right\rceil .                    \tag{11U}
\]
For each non-ray factor, a two-dimensional linear section through an
interior point is a proper two-dimensional cone, hence isomorphic to
\(\mathbb R_+^2\). Taking the product of these sections together with the
full surviving ray factors gives an interior
\(\mathbb R_+^{2q+r}\) section of the operational product. Restricting any coupled
\(\nu\)-LHSC barrier to it preserves self-concordance, logarithmic
homogeneity, and boundary blow-up.  The sharp orthant lower bound therefore
gives
\[
 \nu\geq2q+r\geq2q\geq
 2\left\lceil{N-1\over d-2}\right\rceil .                         \tag{11V}
\]
Thus ray factors add rather than remove barrier cost and are irrelevant to
the displayed minimum.

Consequently every trajectory covered by Section 2 satisfies
\[
 \boxed{
 T\geq{
  \sqrt{\lceil(N-1)/(d-2)\rceil}\,
  \log(\Delta_0/\epsilon)
  \over m\log(1/(1-\rho))}.}                                      \tag{11W}
\]
This includes semialgebraic cones and, with the stated common definability,
standard exponential and fixed-exponent power cones.  It assumes no
symmetry, self-duality, separability of the chosen barrier, or globally
smooth boundary-factor selection: definable stratification supplies the
single regular contact used by the curvature theorem.  The conclusion is
still a primal--dual product-metric movement bound.  It is not a query
lower bound and does not apply to unrestricted long-step or state-only
quantum algorithms.

### 4.1 Globally regular capped Lorentz lifts

Let \(C=(B_2^s)^k\), \(s\geq3\), and consider a globally labelled
primal-and-dual \(C^1\) full-slack lift over Lorentz blocks of dimension at
most \(d\geq3\). Define
\[
 h_d=
 \begin{cases}
  \left\lceil s/(d-2)\right\rceil,&3\leq d<s+1,\\
  1,&d\geq s+1.
 \end{cases}                                                         \tag{11a}
\]
[The exact contact-regularity
theorem](2026-09-04-exact-product-ball-contact-regularity-premium.md)
gives at least \(kh_d\) full Lorentz components after facial reduction.
The intrinsic optimum over all
logarithmically homogeneous barriers on this product of symmetric cones is
its total Jordan rank. Thus every possibly coupled LHSC barrier \(G\) on
the operational cone satisfies
\[
                       \nu_G\geq2kh_d.                               \tag{11b}
\]
Applying (7), every bounded product-Dikin trajectory from a central point
of gap \(\Delta_0\) to a strictly feasible primal--dual point of gap at most
\(\epsilon\) obeys
\[
 T\geq{\sqrt{kh_d}\log(\Delta_0/\epsilon)
           \over m\log(1/(1-\rho))}.                                 \tag{11c}
\]
This is independent of which ambient LHSC barrier is chosen, including
barriers that couple all Lorentz factors.

### 4.2 The one-cone product-ball homogenization

The cone
\[
 \mathcal H_{k,s}
   =\{(t,y_1,\ldots,y_k):\|y_a\|_2\leq t\text{ for all }a\}
                                                                    \tag{11d}
\]
is the canonical homogenization used in Section 3. Its
[exact intrinsic LHSC barrier
parameter](2026-09-04-bounded-face-sharing-sharp-models.md) is \(k+1\):
the explicit spectral-norm restriction attains this value, and the
\(\ell_\infty\)-cone section proves optimality.
Consequently every LHSC barrier on this single cone gives
\[
 T\geq{\sqrt{(k+1)/2}\log(\Delta_0/\epsilon)
           \over m\log(1/(1-\rho))}.                                 \tag{11e}
\]
Collapsing \(k\) Lorentz factors into this one nonhomogeneous cone therefore
collapses factor count but not the square-root product-Dikin movement
scale. The
[one-sharing-cone disk synthesis](2026-09-04-one-sharing-cone-disk-qipm-separation.md)
realizes the same statement on a public-objective, hidden-two-sparse-
equality query family. For the explicit optimal barrier its normalized
projected central and predictor states are \(O(1)\)-query easy while
constant-accuracy scalar or explicit classical readout is
\(\Theta(k)\)-query hard. Those state claims do not extend to an arbitrary
barrier covered by (11e), and the query and movement costs are not
multiplied.

### 4.3 Globally regular real-PSD lifts

Let \(N\geq3\) and \(R\geq2\), and consider an exact lift of \(B_2^N\)
over operational
real PSD blocks \(\mathbb S_+^{r_i}\), \(2\leq r_i\leq R\), whose full
slack has globally labelled primal and dual \(C^1\) contact factors. For
\(N\geq4\), the
[support--Grassmannian
theorem](2026-09-04-psd-support-grassmannian-submersion.md) gives
\[
             \sum_i\left\lfloor{r_i^2\over4}\right\rfloor\geq N.
\]
The same strict inequality holds for the three-ball \(N=3\) by the
[separate \(\mathbb S_+^3\)-saturation
exclusion](2026-09-04-psd3-saturation-exclusion.md). It is false for \(N=2\):
the direct \(\mathbb S_+^2\cong Q_3\) representation has capacity
\(N-1=1\).

The [PSD order-cap
ledger](2026-09-04-psd-order-cap-qipm-ledger.md) puts
\(c_R=\lfloor R^2/4\rfloor\) and writes
\(N=q c_R+t\), \(0\leq t<c_R\). The exact rank-budget envelope is
\[
 V_R(N)=qR+
 \begin{cases}
 0,&t=0,\\
 \lceil2\sqrt t\rceil,&t>0.
 \end{cases}                                                         \tag{11f}
\]
The intrinsic LHSC parameter of a product of real PSD cones, even for a
coupled barrier, is its total Jordan rank. Hence
\[
                 \nu_G\geq\sum_i r_i\geq V_R(N),                     \tag{11g}
\]
and (7) yields
\[
 T\geq{\sqrt{V_R(N)/2}\log(\Delta_0/\epsilon)
           \over m\log(1/(1-\rho))}.                                 \tag{11h}
\]
For \(N=2\), the valid replacement is \(V_R(N-1)=V_R(1)=2\).
Equation (11f) is the exact optimum of the integer capacity-to-rank
ledger; it does not assert that an exact ball lift attains every ledger
value.

The three transfers can be summarized as follows.

| Operational formulation | arbitrary-LHSC parameter floor | product-metric coefficient |
|---|---:|---:|
| globally \(C^1\) capped Lorentz lift | \(2kh_d\) | \(\sqrt{kh_d}\) |
| one \(\mathcal H_{k,s}\) cone | \(k+1\) | \(\sqrt{(k+1)/2}\) |
| globally \(C^1\) real-PSD lift, \(N\geq3\) | \(V_R(N)\) | \(\sqrt{V_R(N)/2}\) |

These primal--dual results and the fixed-primal results are complementary,
not interchangeable. On the grouped Lorentz slice, the restricted
standard barrier has parameter \(kh_d\) and the fixed-barrier determinant
argument gives \(\Omega(\sqrt{kh_d}\log(\Delta/\epsilon))\) distance to
the primal accurate set. On the slice \(t=1\) of
\(\mathcal H_{k,s}\), the restricted standard barrier has parameter \(k\)
and the same fixed-primal argument gives
\(\Omega(\sqrt{k}\log(k/\epsilon))\). Those theorems allow a primal-only
accurate endpoint but fix the restricted barrier. Equations (11c), (11e),
and (11h) allow every ambient LHSC barrier but require a central start,
the primal--dual product metric, and a strictly feasible primal--dual
gap certificate.

The distinction is especially important for PSD Schur lifts. Their
ambient product cone can have parameter \(\sum_i r_i\), while fixing scale
variables can leave a restricted standard barrier of parameter only the
number of packed groups. Equation (11h) uses the former ambient intrinsic
parameter and must not be quoted as a lower bound in the latter restricted
primal metric.

## 5. Why this does not project to a parameter-only primal theorem

Nesterov--Todd explicitly distinguish the two settings. Their
primal--dual path is \(\sqrt2\)-geodesic, but immediately after Corollary
5.1 they state that they do not know how to prove the analogous result for
the primal central path in the cone metric. Thus (5) cannot be projected
to a primal distance lower bound: projection can shorten Riemannian length,
and the dual component may carry an essential part of the obstruction.

Nor does the active-face theorem by itself prove path length. It gives the
global parameter lower bound \(\nu\geq k\), whereas the generic barrier
axioms provide only
\[
             \|F'(x)\|_{x,*}\leq\sqrt\nu
\]
and hence an upper, not a lower, bound on central-path speed.

There is also a sharp obstruction to arguments using only Dikin
containment and determinant growth. At
\[
                         x_\delta=(1-\delta)\mathbf1
\]
in the cube, where \(0<\delta\leq1\), let
\(P=\mathbf1\mathbf1^T/k\) and consider the positive matrix
\[
 H_\delta={2\over k\delta^2}P+{2\over\delta^2}(I-P).                   \tag{12}
\]
It satisfies
\[
 (H_\delta^{-1})_{ii}
   =\delta^2\left(1-{1\over2k}\right)<\delta^2,                         \tag{13}
\]
so its unit ellipsoid fits inside every active upper-facet halfspace.
It also fits inside the opposite cube facets. Nevertheless
\[
              \|\mathbf1\|_{H_\delta}
                ={\sqrt2\over\delta},                                 \tag{14}
\]
with no \(\sqrt k\) factor. More precisely,
\(\det H_\delta=2^k/(k\delta^{2k})\).

One may also choose the pointwise gradient
\[
                         g_\delta={1\over k\delta}\mathbf1,
\]
for which
\[
                          g_\delta^TH_\delta^{-1}g_\delta={1\over2}.    \tag{15}
\]
Thus active-facet containment, determinant growth, and the
\(\nu\)-gradient inequality are jointly consistent at each point with only
\(\Theta(\log(1/\epsilon))\) diagonal metric length. Any primal-only proof
must use the global integrability and third-derivative content of
self-concordance, not just these pointwise ingredients. Equations
(12)--(15) are a proof-method countermodel, not the Hessian of a claimed
global barrier.

The usual determinant comparison also loses exactly the missing factor:
self-concordance gives
\[
 \left|{d\over dt}\log\det F''(x(t))\right|
 \leq 2k\|\dot x(t)\|_{x(t)},
\]
while the \(k\) shrinking facet widths force only a
\(\Theta(k\log(1/\epsilon))\) log-determinant change. Dividing the two
quantities yields merely \(\Omega(\log(1/\epsilon))\).

There is now also a **global** counterexample to the parameter-only
projection, not merely the pointwise proof-method obstruction above.  The
[exact primal--dual speed-splitting
note](2026-09-04-primal-dual-speed-splitting-product-ball-counterexample.md)
proves for every LHSCB central path the Pythagorean formula
\[
       \|\dot x\|_x^2+\|\dot s\|_{s,*}^2=\nu,
\]
and identifies the two terms as orthogonal projections determined by the
affine tangent space.  For the optimal \((k+1)\)-barrier on
\(\mathcal H_{k,s}\), a weighted product-ball objective has exact primal
speed
\[
 \sum_{a=1}^k\left(1-{1\over\sqrt{1+(\eta w_a)^2}}\right).
\]
With one visible weight this is less than one, whereas the dual squared
speed is at least \(k\).  Thus the primal endpoint distance is at most
\(\log(\eta_1/\eta_0)\), even though the product endpoint distance is at
least \(\sqrt{(k+1)/2}\log(\eta_1/\eta_0)\).  Taking all weights positive
but sufficiently small except for one gives a unique product-vertex
optimizer and the same separation at any prescribed accuracy.  The
ambient parameter alone therefore cannot control primal movement.

## 6. Status of the original all-barrier question

The following statement, as originally posed, is false without an objective
nondegeneracy condition:

> Every \(\nu=O(k)\) self-concordant barrier on the \(k\)-cube or a product
> of \(k\) balls places its analytic center at primal barrier-metric
> distance \(\Omega(\sqrt k\log(1/\epsilon))\) from the
> \(\epsilon\)-optimal set.

An objective supported on one factor gives only
\(O(\log(1/\epsilon))\) primal distance for the ordinary product barrier.
Even requiring a unique optimizer does not make a bound uniform over
objectives: positive weights below the requested accuracy scale leave most
factors metrically inactive.  A viable statement must include quantitative
objective scale, such as a precision-dependent exposed-factor count or the
geometric-mean scale in the support-minor theorem.

The remaining open question is narrower: for a quantitatively nondegenerate
objective that exposes every factor at the requested accuracy, does every
\(\nu=O(k)\) self-concordant barrier force
\(\Omega(\sqrt{k}\log(1/\epsilon))\) primal distance?  No counterexample to
that refined statement was found.  The tempting coupled surrogate
\[
                     \log\sum_i{1\over 1-x_i}
\]
has only logarithmic diagonal growth, but it fails self-concordance when
one summand has small softmax weight: the normalized third derivative is
unbounded. Likewise
\[
 -\sum_i\log s_i+(k-1)\log\sum_i s_i
\]
compresses the diagonal singularity but fails the required global
self-concordance. These failures concern the refined uniformly active
question; they are no longer needed to refute the parameter-only statement.

A plausible route is a tangent-barrier compactness theorem: rescale an
arbitrary barrier at a nondegenerate vertex, extract a barrier on the
orthant tangent cone, and prove that its radial logarithmic residue is at
least \(k\). Neither the active-face parameter theorem nor Hildebrand's
projective cross-ratio bound presently supplies this residue statement.

## 7. Literature boundary

Primary sources:

- Yu. E. Nesterov and M. J. Todd,
  [On the Riemannian Geometry Defined by Self-Concordant
  Barriers](https://doi.org/10.1007/s102080010032), especially Theorems
  4.1, 5.2 and Corollary 5.1.
- Yu. Nesterov and A. Nemirovski,
  [Primal Central Paths and Riemannian Distances for Convex
  Sets](https://doi.org/10.1007/s10208-007-9019-4). For bounded convex
  sets they prove an \(O(\nu^{1/4})\) primal central-path/geodesic efficiency
  comparison. It does not give the dimension-explicit
  \(\Omega(\sqrt{k}\log(1/\epsilon))\) vertex-distance statement posed here.
- R. Hildebrand,
  [A lower bound on the optimal self-concordance parameter of convex
  cones](https://optimization-online.org/2011/06/3068/), especially
  Corollary 6.2 for the \(\ell_\infty\) cone.
- Y. T. Lee and M.-C. Yue,
  [Universal Barrier is \(n\)-Self-Concordant](https://arxiv.org/abs/1809.03011),
  for the sharp universal \(O(n)\) upper parameter.

The first source already identifies the primal-versus-primal--dual gap, and
the second gives the strongest general bounded-domain primal comparison found
in this search without closing that gap at the requested scale.
The general target-set geometry in (6a)--(7) is an explicit extraction of
Nesterov--Todd's Theorem 5.1 and Corollary 5.1, not a new literature claim;
the contribution of this note is the sharp canonical product-ball
specialization and the exact boundary between its primal--dual and
primal-only scope.
The literature search found no theorem closing the refined,
objective-nondegenerate gap for all barriers on cubes or products of balls.
The separate speed-splitting note gives an explicit global counterexample to
the broader parameter-only projection and records its more limited novelty
boundary.

The universal bounded-dimension corollary in Section 4.0 was independently
hostile-audited. The audit checked minimal operational-face reduction and
zero/ray accounting, existence of the two-dimensional proper-cone sections,
restriction of a coupled LHSC barrier to the resulting interior orthant
section, the exact factor \(\sqrt{\nu/2}\), and transfer of the definable
generic-contact theorem without a global smooth factor selection. The ray
coordinates must remain in the section; with \(r\) surviving rays the exact
orthant bound is \(\nu\geq2q+r\), as stated in (11V).
