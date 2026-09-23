# No-sharing for analytic and support-irreducible product-ball Lorentz factorizations

Status: Proved; literature-screened; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

Role: Supporting regularity precursor.  The analytic and dense-dual-support
proofs remain valid, but the unrestricted \(C^1\) frontier is now proved by
the stronger top-class argument in
[A \(C^1\) cohomological no-sharing theorem for full product-ball Lorentz
factorizations](2026-09-04-c1-euler-no-sharing-product-balls.md).

## Main theorem

Let

\[
 C=(B_2^s)^k,
 \qquad s\geq3,\qquad k\geq2,\qquad p=s-1,
\]

and let \(M=(S^p)^k\) be its primal extreme-point manifold.  The extreme
points of the polar

\[
 C^\circ=\{(y_1,\ldots,y_k):\sum_a\|y_a\|_2\leq1\}
\]

are \(e_a\otimes z\), where \(a\in[k]\) and \(z\in S^p\).  Hence the full
extreme slack operator is the disjoint family

\[
                 S_a(x,z)=1-\langle x_a,z\rangle.             \tag{1}
\]

Suppose (1) has a globally labelled real-analytic factorization

\[
 S_a(x,z)=\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad
 A_i:M\to Q_3,\qquad B_i^a:S^p\to Q_3.                    \tag{2}
\]

Then

\[
                              \boxed{L\geq ks}.               \tag{3}
\]

The bound is exact.  The separate coordinate-square factorization is
real analytic and uses \(ks\) factors.  Therefore the analytic full-slack
selected-factor count, and the count for pure-\(Q_3\) lifts admitting such
analytic selections, are exactly

\[
                              L_{\rm an}=ks.                  \tag{4}
\]

The theorem closes the sharing question for analytic selected factors: the
smaller paired stereographic factorizations of a fixed positive-weight
contact stratum cannot extend analytically to the polar extreme components.

The same argument gives an exact all-cap Lorentz frontier.  Let every factor
be a Lorentz cone \(Q_{m_i}\), with \(3\leq m_i\leq d\).  If \(L\) is the
number of factors and \(D_{\rm amb}=\sum_i m_i\), then for \(3\leq d<s+1\),

\[
\begin{aligned}
 L_{\min}&=k\left\lceil {s\over d-2}\right\rceil,\\
 (D_{\rm amb})_{\min}
 &=k\left(s+2\left\lceil {s\over d-2}\right\rceil\right),\\
 (\nu_{\rm ambient})_{\min}
 &=2k\left\lceil {s\over d-2}\right\rceil .                \tag{4a}
\end{aligned}
\]

For \(d\geq s+1\), the exact triple is

\[
 (L_{\min},(D_{\rm amb})_{\min},
          (\nu_{\rm ambient})_{\min})=(k,k(s+1),2k).         \tag{4b}
\]

The minima are simultaneous.  Separate grouped Lorentz lifts attain (4a),
and one direct \(Q_{s+1}\) factor per source ball attains (4b).

There is also a strictly \(C^1\) version.  Call the factorization
**productively support-irreducible** if, for every productive pair
\[
 B_i^a\not\equiv0,\qquad A_i\wedge d_aA_i\not\equiv0,
\]
the set
\[
                  \{z\in S^p:B_i^a(z)\neq0\}
\]
is dense in \(S^p\), equivalently the zero set of \(B_i^a\) has empty
interior.  Conclusions (3), (4a), and (4b) remain exact for globally
labelled bi-\(C^1\) factorizations with this property.  Thus a smooth
counterexample can exist only by localizing some nonzero dual channel away
from an open patch; isolated or lower-dimensional vertex zeros do not help.

Without this support condition, the analyticity assumption is used once and
materially.  It rules out a channel whose projective Lorentz ray is assigned
to different source blocks
on disjoint regions separated by cone-vertex zeros.  More precisely, the
proof needs a quasianalytic identity theorem for the factor maps.  It
therefore extends to standard quasianalytic definable classes, but not by the
same argument to arbitrary \(C^\infty\) or arbitrary o-minimal selections.

## 1. Cylindrical zeros pin a channel's projective ray

For every \(a,z\), the slack vanishes on the whole cylinder

\[
                 \{x\in M:x_a=z\}.                           \tag{5}
\]

Every term of (2) is nonnegative.  Thus

\[
             \langle A_i(x),B_i^a(x_a)\rangle=0
             \qquad(x\in M).                                \tag{6}
\]

Fix \(i,a\).  If \(B_i^a(u)\neq0\) is on the Lorentz boundary, its
complementary face in \(Q_3\) is one ray.  If it is interior, its
complementary face is just the vertex.  Equation (6) therefore says that,
on the entire fiber \(x_a=u\),

\[
 A_i(x)=0\quad\hbox{or}\quad A_i(x)
       \hbox{ lies on one ray determined only by }u.         \tag{7}
\]

For a tangent direction \(v_b\) in a different sphere block \(b\neq a\),
(7), including the interior case where the whole fiber maps to the vertex,
implies

\[
                         A_i\wedge d_bA_i=0                  \tag{8}
\]

on every such fiber.  This includes points where \(A_i=0\): a two-sided
derivative of a differentiable map into a pointed cone vanishes at the
vertex.

If \(B_i^a\) is not identically zero, its nonzero set contains a nonempty
open subset of \(S^p\).  Hence (8) holds on a nonempty open cylinder in the
connected real-analytic manifold \(M\).  The section
\(A_i\wedge d_bA_i\) of the corresponding analytic tensor bundle is real
analytic (equivalently, this can be checked in analytic product charts).
The analytic identity theorem gives

\[
 B_i^a\not\equiv0
 \quad\Longrightarrow\quad
 A_i\wedge d_bA_i\equiv0\quad\text{for every }b\neq a.       \tag{9}
\]

This is the no-sharing mechanism.  It uses the full polar extreme row, whose
zero set is a cylinder; it is invisible on one fixed weighted contact
stratum.

## 2. Productive channel sets are disjoint

Define the channels productive for block \(a\) by

\[
 I_a=\{i:B_i^a\not\equiv0
           \text{ and } A_i\wedge d_aA_i\not\equiv0\}.       \tag{10}
\]

If \(i\in I_a\), (9) makes \(A_i\wedge d_bA_i\equiv0\) for every
\(b\neq a\).  Therefore

\[
                              I_a\cap I_b=\varnothing
                              \qquad(a\neq b).               \tag{11}
\]

Channels outside \(I_a\) make zero mixed-curvature contribution to block
\(a\).  This is immediate if \(B_i^a\equiv0\).  Otherwise, if
\(A_i\wedge d_aA_i\equiv0\), then wherever \(A_i\neq0\), its derivative in
block \(a\) is radial:

\[
                              d_aA_i=\gamma A_i.              \tag{12}
\]

For fixed \(x\), the nonnegative function
\(z\mapsto\langle A_i(x),B_i^a(z)\rangle\) vanishes at \(z=x_a\), so its
first derivative vanishes there.  Equations (12) and (6) consequently give

\[
 -\langle d_aA_i(x)u,dB_i^a(x_a)v\rangle=0.                 \tag{13}
\]

If \(A_i(x)=0\), then \(dA_i(x)=0\); if \(B_i^a(x_a)=0\), then
\(dB_i^a(x_a)=0\).  Thus (13) remains true at either cone vertex.

Mixed differentiation of (1) now yields, for every \(x\in M\),

\[
 g_{S^p,x_a}
 =\sum_{i\in I_a}
      -d_aA_i(x)^*dB_i^a(x_a).                              \tag{14}
\]

Every summand has rank at most one.  Hence \(|I_a|\geq p\).

## 3. The sphere phase obstruction supplies the extra channel

Assume \(|I_a|=p\).  Since the left side of (14) has rank \(p\), rank
subadditivity is saturated at every point.  Every channel in \(I_a\) has
rank one everywhere.  In particular, neither \(A_i(x)\) nor
\(B_i^a(x_a)\) is zero anywhere.

Fix all primal blocks except \(x_a\).  Nonzero complementary Lorentz
vectors have unique phases, so for every \(i\in I_a\),

\[
\begin{aligned}
 A_i(x)&=\alpha_i(x)(1,p_i(x_a)),\\
 B_i^a(x_a)&=\beta_i(x_a)(1,-p_i(x_a)),
 \qquad p_i:S^p\to S^1.                                    \tag{15}
\end{aligned}
\]

The rank-one equality forces \(dp_i\) to have rank one everywhere.  Thus
\(p_i:S^p\to S^1\) is a submersion.  Since \(p=s-1\geq2\), \(S^p\) is
simply connected; \(p_i\) lifts to a real-valued function on the compact
sphere and must have a critical point.  This contradiction proves

\[
                               |I_a|\geq p+1=s.               \tag{16}
\]

Summing (16) over the pairwise disjoint sets (11) proves (3).

The notation \(p_i(x_a)\) in (15) does not assume separability.  Equation
(9), together with nowhere-vanishing in the saturated case, says that the
normalized projective ray of \(A_i\) has zero derivative in every block
\(b\neq a\).  Each complementary product fiber is connected, so the
normalized ray factors through \(x_a\).

## 4. Exact frontier under an arbitrary Lorentz dimension cap

Now let channel \(i\) use \(Q_{m_i}\), and put

\[
                              r_i=m_i-2.                     \tag{16a}
\]

The cylindrical-zero and analytic-continuation proof in Sections 1--2 is
dimension-free for Lorentz cones: every nonzero boundary vector of
\(Q_{m_i}\) has a unique complementary ray.  Define \(I_a\) exactly as in
(10), using the ambient wedge in \(\mathbb R^{m_i}\).  The sets \(I_a\)
remain pairwise disjoint, channels outside \(I_a\) have zero block-\(a\)
mixed curvature, and the Lorentz tangent-pairing bound gives

\[
                       \sum_{i\in I_a}r_i\geq p=s-1.         \tag{16b}
\]

Suppose equality holds in (16b).  Pointwise rank saturation normalizes every
productive factor to a submersion

\[
                          S^p\longrightarrow S^{r_i}.        \tag{16c}
\]

To state the saturation step precisely, define the productive subkernel

\[
 K_a(x,z)=\sum_{i\in I_a}\langle A_i(x),B_i^a(z)\rangle .
\]

It is nonnegative term by term and vanishes on the diagonal \(z=x_a\).
Equation (14) says that its diagonal mixed form is the full sphere metric:
all channels outside \(I_a\) have zero mixed-curvature contribution.  Thus,
when equality holds in (16b), \(K_a\) satisfies exactly the hypotheses of
the saturated-block rigidity theorem; this is not an application to the
rank inequality alone.

The [saturated-block rigidity theorem](2026-09-04-joint-saturated-block-covering-rigidity.md)
says that their product is a local
diffeomorphism from \(S^p\) to \(\prod_{i\in I_a}S^{r_i}\).  Compactness
makes it a covering.  Simple connectivity and cohomology force exactly one
positive-capacity target, with \(r_i=p\).  Equivalently, a saturated source
sphere can use only one \(Q_{p+2}=Q_{s+1}\) factor.

If \(d<s+1\), that factor is forbidden.  The integer improvement over
(16b) is therefore

\[
                       \sum_{i\in I_a}r_i\geq s.             \tag{16d}
\]

Since \(r_i\leq d-2\), each source block needs

\[
 |I_a|\geq h:=\left\lceil{s\over d-2}\right\rceil,
 \qquad
 \sum_{i\in I_a}m_i
 =\sum_{i\in I_a}r_i+2|I_a|\geq s+2h.                      \tag{16e}
\]

Disjointness gives the lower bounds in (4a).  Each Lorentz factor has exact
ambient barrier parameter two, so the factor-count bound also gives
\(\nu_{\rm ambient}\geq2kh\).

For \(d\geq s+1\), (16b) gives at least one productive factor and productive
ambient dimension at least \(p+2=s+1\) per source block.  Disjointness gives
the three lower bounds in (4b).

All bounds are attained.  In the small-cap regime, partition the \(s\)
coordinates of each ball into \(h\) groups \(G\) of sizes
\(1\leq |G|\leq d-2\) summing to \(s\), and use

\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
                   {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(z)&=\left({1+\|z_G\|^2\over2},
                  -{1-\|z_G\|^2\over2},-z_G\right)
                  \in Q_{|G|+2}.                            \tag{16f}
\end{aligned}
\]

Their pairing is \(\|x_G-z_G\|^2/2\).  Concatenating groups and then source
balls gives (4a), with inactive dual components set to zero.  For the
large-cap regime, \(A_a(x)=(1,x_a)\) and
\(B_a^b(z)=\mathbf1_{a=b}(1,-z)\) in \(Q_{s+1}\) give (4b).  These maps are
polynomial, and the corresponding product lifts are strictly feasible.

## 5. Matching analytic full-slack \(Q_3\) factorization and lift

Let

\[
\begin{aligned}
 U(t)&=\left({1+t^2\over2},{1-t^2\over2},t\right),\\
 V(t)&=\left({1+t^2\over2},-{1-t^2\over2},-t\right).
\end{aligned}                                                 \tag{17}
\]

Then \(U(t),V(t)\in Q_3\) and

\[
                         \langle U(t),V(u)\rangle
                         ={1\over2}(t-u)^2.                  \tag{18}
\]

Index \(ks\) channels by \((b,j)\in[k]\times[s]\), and set

\[
 A_{b,j}(x)=U((x_b)_j),
 \qquad
 B_{b,j}^a(z)=
 \begin{cases}
 V(z_j),&b=a,\\
 0,&b\neq a.
 \end{cases}                                                  \tag{19}
\]

Summing (18) gives

\[
 \sum_{b,j}\langle A_{b,j}(x),B_{b,j}^a(z)\rangle
 ={1\over2}\|x_a-z\|_2^2
 =1-x_a^Tz.                                                   \tag{20}
\]

All maps are polynomial.  The corresponding affine lift is the Cartesian
product of the smooth coordinate-square lifts for the individual balls; it
is strictly feasible and has globally polynomial primal boundary factors
and analytic, possibly zero, dual factors on every polar extreme component.
No normalization of an identically zero inactive dual component is claimed.
Explicitly, writing the \((b,j)\)-th cone variable as
\(q_{b,j}=(r_{b,j},u_{b,j},v_{b,j})\in Q_3\), impose

\[
 r_{b,j}+u_{b,j}=1,\qquad
 \sum_{j=1}^s(r_{b,j}-u_{b,j})=1,\qquad
 x_{b,j}=v_{b,j}.
\]

The cone inequalities say
\(r_{b,j}-u_{b,j}\geq x_{b,j}^2\), so this projects exactly to
\(\sum_jx_{b,j}^2\leq1\).  Interior points admit strict inequalities in
every channel, while at \(x_b\in S^{s-1}\) all inequalities are equalities
and the unique fiber is precisely \(q_{b,j}=U(x_{b,j})\).  This directly
checks strict feasibility and the claimed polynomial boundary selection,
rather than relying only on the abstract factorization theorem.

## 6. Barrier and QIPM consequence

Within this analytic full-contact pure-\(Q_3\) formulation class, the exact
factor count is \(ks\).  The unchanged ambient product \(Q_3^{ks}\) has
optimal self-concordant barrier parameter

\[
                              \nu_{\rm ambient}=2ks,          \tag{21}
\]

even among coupled barriers, and the standard product Lorentz barrier
attains it.  This is an ambient-cone statement, not an intrinsic barrier
lower bound for \(C\), its projected image, or its affine feasible slice,
and it is not by itself an IPM iteration lower bound.
Indeed, choosing a two-dimensional Lorentz section in every factor gives an
orthant section \(\mathbb R_+^{2ks}\), whose barrier lower bound is
\(2ks\); restriction to a linear section shows that coupling the ambient
barrier cannot lower this number.

The distinction from the fixed-contact result is sharp.  For a fixed
positive weight vector, paired stereographic charts use only
\(ks-\lfloor k/2\rfloor\) smooth contact factors.  Requiring simultaneous
analytic extension to all polar extreme components restores the separate
\(ks\) count.

## 7. The exact regularity boundary

Real analyticity is stronger than the proof needs.  Its only global use is
the implication from vanishing on a nonempty open cylinder to global
vanishing of the tensor

\[
                       A_i\wedge d_bA_i.                    \tag{22}
\]

Consequently the theorem and its proof hold verbatim when the factor maps
belong to a quasianalytic differential algebra in local charts: the class
must be closed under differentiation and multiplication, and a member that
vanishes on an open set of a connected domain must vanish everywhere.  Two
useful consequences are:

1. globally \(C^\infty\) semialgebraic factor maps are Nash, hence real
   analytic, so the exact lower bound \(L\geq ks\) **does** apply to them;
2. it also applies to globally \(C^\infty\) factor maps definable in a fixed
   polynomially bounded o-minimal expansion of the real field, by Miller's
   quasianalyticity theorem.

There is a separate \(C^1\) route that needs no identity theorem.  If the
factorization is productively support-irreducible, then for every
\(i\in I_a\), equation (8) holds on the dense union of fibers with
\(B_i^a(x_a)\neq0\).  The tensor \(A_i\wedge d_bA_i\) is continuous, so it
vanishes on all of \(M\).  This proves the instance of (9) needed for every
productive channel.  Every later step uses only \(C^1\) regularity,
including the capped-block argument.  Therefore all exact counts in (3),
(4a), and (4b) hold under this support condition.

This observation sharply localizes any remaining smooth escape: a channel
that is productive for two source balls must have a dual component whose
zero set contains an open patch.  Merely allowing the primal factor to hit
the Lorentz vertex, or allowing a dual component to vanish on a thin set,
cannot enable sharing.

Arbitrary smoothness, and o-minimal definability without polynomial
boundedness, do not supply this continuation principle.  Here is an explicit
smooth switching witness.  Put

\[
 h(t)=\begin{cases}e^{-1/t^2},&t>0,\\0,&t\leq0,\end{cases}
 \qquad \tau=(x_a)_1,
\]

choose \(b\neq a\), let \(U\) be as in (17), and fix
\(q_0=U(0)\in\partial Q_3\setminus\{0\}\).  The maps

\[
 A(x)=h(\tau)U((x_b)_1),
 \qquad B^a(u)=h(-u_1)q_0                              \tag{23}
\]

are \(C^\infty\), cone-valued, and definable in
\(\mathbb R_{\exp}\).  They satisfy the entire cylindrical complementarity
condition

\[
                       \langle A(x),B^a(x_a)\rangle=0
                       \quad(x\in M),                         \tag{24}
\]

and \(B^a\not\equiv0\).  Nevertheless
\(A\wedge d_bA\not\equiv0\): on \(\tau>0\), it is a positive scalar
multiple of \(U((x_b)_1)\wedge dU((x_b)_1)\) in a generic block-\(b\)
direction.  Thus the local-to-global implication (9) is false in the
\(C^\infty\) category, even for o-minimal smooth maps.

The witness (23) is deliberately only a counterexample to the continuation
lemma; it is not a factorization of the full slack operator with fewer than
\(ks\) channels.  This left arbitrary smooth factors open at the stage of
this precursor argument.  The later relative top-class theorem cited at
the start of the note closes that gap and proves the same lower bound under
arbitrary globally labelled \(C^1\) selections.

## 8. Literature screen and scope

The general lift/factorization correspondence is due to Gouveia, Parrilo,
and Thomas, *Mathematics of Operations Research* 38 (2013), DOI
[10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).  Fawzi's
second-order-cone-rank obstruction is in *Mathematical Programming* 2019,
DOI [10.1007/s10107-018-1233-0](https://doi.org/10.1007/s10107-018-1233-0).
Aubrun, La Piana, and M\"uller-Hermes study positive linear maps factoring
through direct sums of Lorentz cones in
[*Factorization through Lorentz cones*](https://arxiv.org/abs/2606.27825).
For the semialgebraic-smooth corollary, a \(C^\infty\) semialgebraic map on
a Nash manifold is Nash, hence real analytic; see Bochnak, Coste, and Roy,
*Real Algebraic Geometry*, Proposition 8.1.8, DOI
[10.1007/978-3-662-03718-8](https://doi.org/10.1007/978-3-662-03718-8).
The quasianalyticity of smooth functions definable in polynomially bounded
o-minimal structures is due to Miller, *Proceedings of the American
Mathematical Society* 123 (1995), DOI
[10.1090/S0002-9939-1995-1257118-1](https://doi.org/10.1090/S0002-9939-1995-1257118-1).

Targeted searches did not locate the analytic cylindrical-zero continuation
argument, the productive-channel partition (10)--(11), or the exact analytic
full product-ball count (4).  Novelty is plausible pending specialist review.
The result does not claim the same count for arbitrary \(C^1\), arbitrary
smooth, or arbitrary o-minimal selections.  It does include smooth
semialgebraic and, more generally, the polynomially bounded o-minimal smooth
classes described above, as well as productively support-irreducible
bi-\(C^1\) selections.  Unique continuation or dense dual support, not mere
differentiability or definability, is the step that prevents vertex-mediated
channel switching.

## 9. Independent hostile audit

An independent audit checked the cases hidden by a nowhere-zero
normalization argument.  If a cone-valued differentiable map hits the
Lorentz vertex on the boundaryless manifold \(M\), every two-sided
directional derivative belongs to both \(Q_3\) and \(-Q_3\), so it is zero.
Thus (8) remains valid at vertices and no division by \(A_i\) is used in
the analytic-continuation step.  If the dual vector is interior, its
complementary face is the vertex, which gives the same wedge conclusion.

The audit also rederived the mixed-curvature deletion in (13).  On the
nonvertex locus, \(A_i\wedge d_aA_i=0\) makes \(d_aA_i\) radial, while
first-order optimality of the nonnegative function
\(z\mapsto\langle A_i(x),B_i^a(z)\rangle\) at \(z=x_a\) makes the radial
pairing with \(dB_i^a\) zero.  At either vertex one derivative is already
zero.  Finally, if \(|I_a|=p\), the rank inequality is saturated pointwise,
so every one of the \(p\) channels is rank one and neither contact factor
can vanish anywhere.  Normalized complementarity then gives a genuine
global phase map \(S^p\to S^1\) of rank one everywhere, contradicting the
lift-to-\(\mathbb R\) maximum argument for \(p\geq2\).

The matching side was checked independently as well: (18) expands exactly,
the affine constraints displayed after (20) project to the full Cartesian
product of balls and have unique polynomial fibers on every primal extreme
point, and inactive dual factors in (19) are legitimately the cone vertex.
The \(2ks\) barrier statement concerns the unchanged ambient product and is
certified against coupled barriers by its \(2ks\)-orthant section; it makes
no assertion about a barrier after projection or restriction to the affine
slice.

No step upgrades quasianalytic unique continuation to the merely \(C^1\) or
arbitrary \(C^\infty\) category.  The explicit flat switch (23) shows why.
The exact \(ks\) conclusion is therefore correctly limited to analytic or
the stated quasianalytic selected factors and to full extreme-slack
factorization, not the smaller fixed-weight contact restriction.

The capped-block extension was audited separately.  For a productive
\(Q_{m_i}\) channel, the tangent pairing passes through the
\((m_i-2)\)-dimensional quotient of the two complementary boundary rays,
so its rank bound is exactly \(r_i=m_i-2\).  Equality in (16b) saturates
every channel pointwise.  Normalization therefore gives submersions to
\(S^{r_i}\), and their product is a covering of
\(\prod_{i\in I_a}S^{r_i}\).  Since \(p\geq2\), fundamental groups exclude
an \(S^1\) factor, while integral cohomology excludes a product of two or
more positive-dimensional spheres from being covered by \(S^p\).  The only
saturated possibility is one block with \(r_i=p\).

Thus a cap \(d<s+1\) forbids capacity \(p=s-1\) and forces the integer
upgrade \(\sum_{i\in I_a}r_i\geq s\).  Together with
\(r_i\leq d-2\), this independently yields at least
\(h=\lceil s/(d-2)\rceil\) productive factors and productive ambient
dimension at least \(s+2h\) per source block.  Disjointness of the
productive sets makes these bounds additive over the \(k\) blocks.  The
orthant-section argument gives \(\nu\geq2L\), including coupled ambient
barriers.  Group sizes summing to \(s\) and bounded by \(d-2\) always exist
for this \(h\), so (16f) attains all three small-cap minima simultaneously;
one direct \(Q_{s+1}\) block per ball similarly attains the large-cap
triple.  Setting \(d=3\) recovers \(L=ks\), ambient dimension \(3ks\), and
\(\nu=2ks\), as required.

The support-irreducible \(C^1\) extension was also checked independently.
For each nonzero dual component, (8) holds on the dense set
\(\{x:B_i^a(x_a)\neq0\}\); since \(A_i\wedge d_bA_i\) is continuous, this
is sufficient for (9).  Sections 2--4 thereafter use only first
derivatives, cone complementarity, rank saturation, and sphere topology.
In particular, no normalization is applied at a dual zero, and equality in
the capacity bound forces all factors being normalized to be nonzero by
rank saturation itself.  The \(Q_3\) and capped-Lorentz exact frontiers
therefore hold with the stated dense-support hypothesis under genuine
\(C^1\) regularity.
