# Open vertex regions are necessary for smooth full-slack sharing

Status: Proved  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

Role: Supporting structural lemma.  Open primal and dual vertex regions
are necessary for any channel that switches source ownership, but the
possibility of such switching no longer leaves the factor-count frontier
open: the stronger relative top-class theorem proves the same exact counts
for arbitrary globally labelled \(C^1\) factors.  See
[A \(C^1\) cohomological no-sharing theorem for full product-ball Lorentz
factorizations](2026-09-04-c1-euler-no-sharing-product-balls.md).

## Result

Let

\[
 C=(B_2^s)^k,\qquad M=(S^{s-1})^k,
 \qquad s\geq3,\qquad k\geq2,
\]

and write the full extreme slack of the product as

\[
 S_a(x,z)=1-x_a^Tz,
 \qquad a\in[k],\quad x\in M,\quad z\in S^{s-1}.             \tag{1}
\]

Suppose (1) has globally labelled \(C^1\) Lorentz factors

\[
 S_a(x,z)=\sum_{i=1}^L
       \langle A_i(x),B_i^a(z)\rangle,
 \qquad A_i(x),B_i^a(z)\in Q_3.                              \tag{2}
\]

Call channel \(i\) *productive for source block* \(a\) if its mixed
contact channel

\[
 H_i^a(x)=-d_aA_i(x)^*dB_i^a(x_a)                            \tag{3}
\]

is nonzero at some \(x\in M\).  If every productive primal factor obeys

\[
                 \operatorname{int}_M A_i^{-1}(0)=\varnothing,             \tag{4}
\]

then

\[
                              \boxed{L\geq ks}.               \tag{5}
\]

The separate coordinate-square factorization attains equality and has
nowhere-zero primal factors.  Thus (5) is exact in the class (4).

Equivalently, every globally \(C^1\) full-slack factorization with
\(L<ks\) must contain a channel that is productive for at least two source
blocks and whose primal factor is identically the Lorentz vertex on a
nonempty open subset of \(M\).  A lower-dimensional, nowhere-dense, or
isolated vertex locus cannot mediate factor sharing.

The same shared channel must also have an open dual vertex patch in every
source component for which it is productive.  Indeed, if the nonzero set of
some productive \(B_i^a\) were dense, the cylindrical ray identity would
make \(A_i\wedge d_bA_i=0\) on a dense set for every \(b\neq a\), hence
everywhere by continuity.  That channel could not then be productive for a
second block.  Thus any sub-\(ks\) construction must use genuinely
two-sided flat switching: open primal vertex regions and open dual vertex
patches, not merely thin singular loci.

This theorem isolates the only possible channelwise switching mechanism.
Smooth cone-valued maps can vanish on open sets and turn on flatly across
their boundaries, although the global top-class theorem cited above now
shows that finitely many such switches cannot reduce the full-slack count.

## 1. Contact channels

For every \(a\), (1) vanishes on the cylinder \(z=x_a\).  Nonnegativity of
the individual cone pairings gives

\[
             \langle A_i(x),B_i^a(x_a)\rangle=0              \tag{6}
\]

for every \(i,a,x\).  Mixed differentiation of (2) at contact gives

\[
 g_{S^{s-1},x_a}=\sum_{i=1}^L H_i^a(x).                      \tag{7}
\]

Every \(H_i^a(x)\) has rank at most one.  Indeed, if either contact factor
is the vertex, its derivative is zero: a two-sided derivative of a map from
a boundaryless manifold into a pointed cone belongs to both the cone and
its negative.  Otherwise both factors are nonzero complementary Lorentz
boundary vectors.  Locally write

\[
 A_i=\alpha_i(1,p_i),\qquad
 B_i^a=\beta_i(1,-q_i^a),\qquad p_i,q_i^a\in S^1.             \tag{8}
\]

The cylindrical identity (6) identifies the phases at contact.  On every
neighborhood where \(A_i\) and \(B_i^a\) are nonzero,

\[
 p_i(x)=q_i^a(x_a),\qquad
 H_i^a(x)=\alpha_i(x)\beta_i^a(x_a)
             (dq_i^a(x_a))^*dq_i^a(x_a).                    \tag{9}
\]

Consequently a productive channel supplies a point at which the relevant
dual phase has nonzero derivative.

## 2. One channel cannot productively serve two blocks

Assume channel \(i\) is productive for distinct blocks \(a,b\).  By (9),
there are points \(u,v\in S^{s-1}\) and neighborhoods \(U\ni u\),
\(V\ni v\) on which \(B_i^a,B_i^b\) are nonzero boundary vectors and the
phase maps \(q_i^a,q_i^b\) are nonconstant.  Choose smaller nonempty open
sets \(U'\subseteq U\), \(V'\subseteq V\) for which

\[
                         q_i^a(U')\cap q_i^b(V')=\varnothing. \tag{10}
\]

Such sets exist: a phase map with nonzero derivative has a nontrivial local
arc as its image, so one may first choose a pair of unequal image points and
then shrink by continuity.

Now take any \(x\in M\) with \(x_a\in U'\) and \(x_b\in V'\).  If
\(A_i(x)\neq0\), (6) and uniqueness of the complementary ray in \(Q_3\)
would force its normalized phase to equal both \(q_i^a(x_a)\) and
\(q_i^b(x_b)\), contradicting (10).  Hence

\[
 A_i=0\quad\hbox{on}\quad
 \{x:x_a\in U',\ x_b\in V'\},                               \tag{11}
\]

a nonempty open subset of \(M\).  Under (4), this is impossible.
Therefore the productive index sets

\[
 I_a=\{i:H_i^a\not\equiv0\}                                 \tag{12}
\]

are pairwise disjoint.

Notice that this argument handles vertices without normalizing through
them.  It also identifies exactly why arbitrary smooth factors evade the
argument: a shared channel must switch ownership through an open vertex
region such as (11).

There is a dual support consequence that needs no assumption (4).  Suppose
\(i\) is productive for \(a\), and the nonzero set of \(B_i^a\) is dense
in \(S^{s-1}\).  For every \(b\neq a\), the cylindrical ray argument gives

\[
                         A_i\wedge d_bA_i=0                  \tag{12a}
\]

on the dense union of fibers where \(B_i^a(x_a)\neq0\).  The left side is
continuous, so (12a) holds on all of \(M\).  If the same channel were
productive for \(b\), formula (9) at a productive point would instead make
\(A_i\wedge d_bA_i\neq0\).  Therefore a channel productive for two blocks
has a nondense nonzero dual locus, equivalently a nonempty open dual vertex
patch, in each productive component.

## 3. Every source block needs \(s\) productive channels

Put \(p=s-1\).  Equation (7) and the rank-one bound first give

\[
                              |I_a|\geq p.                    \tag{13}
\]

Suppose equality holds.  At every \(x\), the rank inequality

\[
 p=\operatorname{rank}g_{S^p,x_a}
   \leq\sum_{i\in I_a}\operatorname{rank}H_i^a(x)
   \leq p                                                       \tag{14}
\]

is saturated.  Thus every \(H_i^a(x)\) has rank one everywhere.  Neither
contact factor can be the vertex at any point.  The normalized phase in
(9) is therefore a global \(C^1\) map

\[
                         q_i^a:S^p\longrightarrow S^1         \tag{15}
\]

whose derivative has rank one everywhere.  This is impossible for
\(p\geq2\): simple connectivity lifts \(q_i^a\) to a real-valued \(C^1\)
function on the compact sphere, and that lift has a critical point.
Therefore

\[
                              |I_a|\geq p+1=s.                \tag{16}
\]

The disjointness of the \(I_a\) now gives

\[
 L\geq\sum_{a=1}^k|I_a|\geq ks,
\]

which proves (5).

## 4. Matching construction and precise frontier

For completeness, let

\[
 U(t)=\left({1+t^2\over2},{1-t^2\over2},t\right),\qquad
 V(t)=\left({1+t^2\over2},-{1-t^2\over2},-t\right).
\]

Then \(U(t),V(t)\in Q_3\) are nonzero and

\[
                         \langle U(t),V(u)\rangle
                              ={1\over2}(t-u)^2.
\]

The \(ks\) factors

\[
 A_{b,j}(x)=U((x_b)_j),\qquad
 B_{b,j}^a(z)=\mathbf 1_{a=b}V(z_j)
\]

sum to \(\|x_a-z\|^2/2=1-x_a^Tz\).  Their primal vertex sets are empty,
so the lower bound is attained within (4).

At the channelwise level there is the following sharp dichotomy:

* either \(L\geq ks\);
* or at least one productive factor has a nonempty open primal vertex
  region and switches source ownership across such regions.

This lemma alone does not exclude the second alternative.  The later
top-class cover argument excludes its use in a sub-\(ks\) full
factorization and supplies the unrestricted \(C^1\) lower bound.

## 5. Capped-Lorentz extension

The open-vertex argument is not special to \(Q_3\).  Let channel \(i\)
take values in \(Q_{m_i}\), put \(r_i=m_i-2\), and assume
\(3\leq m_i\leq d\).  A nonzero Lorentz boundary vector still has a unique
complementary ray.  If one channel is productive for distinct source
blocks \(a,b\), productivity supplies nonconstant local normalized
boundary-ray maps for both blocks.  Choose two small neighborhoods with
disjoint ray images.  On their product cylinder the common primal factor
must be the vertex.  Hence condition (4) again makes the productive sets
\(I_a\) pairwise disjoint.

The mixed-channel capacity bound is now

\[
                    \sum_{i\in I_a}r_i\geq s-1.              \tag{17}
\]

If equality holds, rank saturation normalizes the productive factors to
submersions from \(S^{s-1}\) onto \(S^{r_i}\).  Their product is a covering
of \(\prod_{i\in I_a}S^{r_i}\).  Fundamental groups exclude a circle
factor, and integral cohomology excludes a product of two or more
positive-dimensional spheres.  Thus equality in (17) is possible only for
one factor with \(r_i=s-1\), namely one \(Q_{s+1}\).

Consequently, if \(3\leq d<s+1\), put

\[
                         h=\left\lceil{s\over d-2}\right\rceil.
\]

Every source block has capacity at least \(s\), at least \(h\) productive
factors, and productive ambient dimension at least \(s+2h\).  Disjointness
of the \(I_a\) gives the simultaneous exact minima

\[
 L_{\min}=kh,\qquad
 (D_{\rm amb})_{\min}=k(s+2h),\qquad
 (\nu_{\rm ambient})_{\min}=2kh.                           \tag{18}
\]

Grouped coordinate-square Lorentz factors attain all three.  If
\(d\geq s+1\), one direct \(Q_{s+1}\) factor per source ball attains the
simultaneous exact triple

\[
             (L_{\min},(D_{\rm amb})_{\min},
                    (\nu_{\rm ambient})_{\min})
                    =(k,k(s+1),2k).                          \tag{19}
\]

Here the barrier parameter is for the unchanged ambient Lorentz product;
the lower bound \(2L\) remains valid for coupled barriers by restriction to
a product of two-dimensional orthant sections.  Equations (18)--(19) make
no intrinsic barrier claim about the projected body or affine slice.

## Audit checklist

The proof uses only first derivatives.  It does not invoke analytic
continuation, divide by a factor at a vertex, or assume that inactive dual
factors can be normalized.  Productivity forces both contact factors to be
nonzero before phases are introduced.  The open vertex region in (11) is a
full product cylinder in the remaining coordinates, not merely a contact
slice.  Finally, the extra channel in (16) comes from the global phase
submersion obstruction and not from an Euler-class claim, so it also covers
parallelizable source spheres.

For the capped extension, the productive rank bound is the dimension
\(m_i-2\) of the quotient transverse to a complementary ray pair.  At
equality, rank saturation forces every normalized factor used in the
covering argument to be nonzero everywhere; no vertex is normalized.
The strict upgrade from \(s-1\) to \(s\) uses integrality only after the
single allowed capacity-\((s-1)\) factor has been excluded by the cap.
Finally, the factor, dimension, and barrier lower bounds are simultaneous:
they follow respectively from \(|I_a|\geq h\),
\(\sum_{i\in I_a}(r_i+2)\geq s+2h\), and the orthant-section inequality
\(\nu\geq2L\).  The grouped construction realizes a partition of all
\(s\) coordinates into exactly \(h\) nonempty groups of size at most
\(d-2\), so it attains each bound without a residual-capacity gap.
