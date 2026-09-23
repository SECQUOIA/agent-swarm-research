# A C1 cohomological no-sharing theorem for full product-ball Lorentz factorizations

Status: Proved; literature-screened; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

## Main result

Let

\[
 C=(B_2^s)^k,\qquad M=(S^{s-1})^k,
 \qquad p=s-1,
\]

where \(k\geq1\) and \(s\geq3\).  The full extreme slack is

\[
                  S_a(x,z)=1-\langle x_a,z\rangle,
 \qquad a\in[k],\quad x\in M,\quad z\in S^p.                \tag{1}
\]

Suppose that it has a globally labelled \(C^1\) factorization through
\(L\) three-dimensional Lorentz cones,

\[
 S_a(x,z)=\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad A_i:M\to Q_3,\quad B_i^a:S^p\to Q_3.               \tag{2}
\]

Then

\[
                              \boxed{L\geq ks}.             \tag{3}
\]

The polynomial coordinate-square factorization attains equality.  Thus in
every ball dimension \(s\geq3\), the exact globally \(C^1\) full-slack
\(Q_3\)-factor count is \(ks\).  This removes the analytic/quasianalytic
hypothesis completely: flat vertex-mediated switching can invalidate
channelwise continuation, but it cannot reduce the full-slack count.

More generally, let (2) use Lorentz factors \(Q_{m_i}\) with
\(3\leq m_i\leq d\), and let \(D_{\rm amb}=\sum_i m_i\).  If
\(3\leq d<s+1\), then the simultaneous exact frontier is

\[
\begin{aligned}
 L_{\min}&=k\left\lceil {s\over d-2}\right\rceil,\\
 (D_{\rm amb})_{\min}
 &=k\left(s+2\left\lceil {s\over d-2}\right\rceil\right),\\
 (\nu_{\rm ambient})_{\min}
 &=2k\left\lceil {s\over d-2}\right\rceil.                 \tag{3a}
\end{aligned}
\]

If \(d\geq s+1\), the simultaneous exact triple is

\[
 (L_{\min},(D_{\rm amb})_{\min},(\nu_{\rm ambient})_{\min})
                  =(k,k(s+1),2k).                           \tag{3b}
\]

Thus the complete analytic capped-Lorentz frontier also holds for arbitrary
globally \(C^1\) selected factors.

The result is additive for heterogeneous products
\(\prod_{a=1}^kB_2^{s_a}\) under the same uniform cap
\(c=d-2\).  Put \(p_a=s_a-1\), and define

\[
 h_a=\begin{cases}
 1,&c\geq p_a,\\
 \lceil s_a/c\rceil,&c<p_a,
 \end{cases}
 \qquad
 \tau_a=\begin{cases}
 p_a,&c\geq p_a,\\
 s_a,&c<p_a.
 \end{cases}                                               \tag{3c}
\]

Then the simultaneous exact frontier is

\[
 L_{\min}=\sum_ah_a,\qquad
 (D_{\rm amb})_{\min}=\sum_a(\tau_a+2h_a),\qquad
 (\nu_{\rm ambient})_{\min}=2\sum_ah_a.                    \tag{3d}
\]

The proof is pointwise and topological.  It does not attempt to continue a
channel across an open zero set.  Instead, positivity turns every contact
channel into a positive-semidefinite rank-one form, different source blocks
cannot use the same channel at the same point, and the top cohomology classes
of the \(k\) sphere factors force all \(k\) blocks to need an extra channel
simultaneously somewhere.

## 1. Contact Hessian channels

Write

\[
 Q_3=\{(t,y)\in\mathbb R\times\mathbb R^2:t\geq\|y\|_2\}.
\]

For \(u,v\in T_{x_a}S^p\), define

\[
 H_i^a(x)(u,v)
 :=-\left\langle D_aA_i(x)[u],DB_i^a(x_a)[v]\right\rangle. \tag{4}
\]

Only first derivatives of the factors occur.  Mixed differentiation of
(2), first in \(x_a\) and then in \(z\), gives

\[
                         g_{S^p,x_a}=\sum_{i=1}^L H_i^a(x). \tag{5}
\]

Every \(H_i^a(x)\) is symmetric positive semidefinite and has rank at most
one.  To see this without a hidden nonvanishing assumption, first note that
contact positivity gives

\[
                 \langle A_i(x),B_i^a(x_a)\rangle=0.        \tag{6}
\]

If either contact factor is the cone vertex, its derivative is zero: a
two-sided derivative of a differentiable map into a pointed cone belongs to
both \(Q_3\) and \(-Q_3\).  If one factor is interior, (6) forces the other
to be the vertex.  These cases give \(H_i^a=0\).

In the remaining case both factors are nonzero boundary points.  Locally
they have the complementary form

\[
 A_i=\alpha_i(1,q_i),\qquad
 B_i^a=\beta_i^a(1,-q_i),\qquad q_i\in S^1,                \tag{7}
\]

with positive scales.  Differentiating the equality of the two contact
phases along the diagonal and using \(q_i^TDq_i=0\) yields

\[
 H_i^a(x)=\alpha_i(x)\beta_i^a(x_a)\,omega_i^a(x)
                    \otimes\omega_i^a(x),                  \tag{8}
\]

where, after orienting \(S^1\),

\[
            \omega_i^a=\langle Jq_i,D_aq_i\rangle
            \in T_{x_a}^*S^p.                              \tag{9}
\]

This proves the asserted positivity and rank bound.  It also gives a
canonically oriented nonzero covector wherever \(H_i^a\neq0\); no square
root or arbitrary orientation of a rank-one line is needed.

Call \(i\) active for block \(a\) at \(x\) when \(H_i^a(x)\neq0\), and put

\[
                         N_a(x)=\#\{i:H_i^a(x)\neq0\}.       \tag{10}
\]

Equation (5) and the rank-one bound imply

\[
                                  N_a(x)\geq p.              \tag{11}
\]

## 2. Pointwise no-sharing needs no continuation

At a fixed point, a channel cannot be active for two different source
blocks.  Indeed, suppose \(H_i^a(x)\neq0\).  Then
\(B_i^a(x_a)\neq0\).  On the entire cylinder with this value of \(x_a\),
(6) puts \(A_i\) either at the vertex or on the single complementary
Lorentz ray determined by \(B_i^a(x_a)\).  Since \(A_i(x)\neq0\), its
projective phase is locally constant in every block direction \(b\neq a\).
Formula (8), or the same radial-derivative calculation before normalization,
therefore gives

\[
              H_i^a(x)\neq0\quad\Longrightarrow\quad
              H_i^b(x)=0\quad(b\neq a).                    \tag{12}
\]

Consequently

\[
                              \sum_{a=1}^kN_a(x)\leq L.      \tag{13}
\]

This is weaker than analytic global no-sharing: the same label may still
serve different blocks on disjoint regions separated by vertex zeros.  The
cohomological cover argument below is precisely what survives that switching.

## 3. The top-class cover obstruction

Assume for contradiction that

\[
                            L\leq k(p+1)-1.                  \tag{14}
\]

By (11), (13), and (14), at every \(x\in M\) at least one block has exactly
\(p\) active channels.  Hence the closed sets

\[
                         E_a=\{x\in M:N_a(x)=p\}             \tag{15}
\]

cover \(M\).  Closedness follows because each active locus
\(\{H_i^a\neq0\}\) is open and \(N_a\geq p\).

For each \(p\)-element label set \(J\subseteq[L]\), let

\[
 E_{a,J}=\{x\in E_a:\{i:H_i^a(x)\neq0\}=J\}.               \tag{16}
\]

The finitely many nonempty \(E_{a,J}\) form a clopen partition of the
compact set \(E_a\): the \(p\) active channels at a point remain active
nearby, and within \(E_a\) no additional one can appear.  They are therefore
pairwise disjoint compact sets and admit pairwise disjoint open
neighborhoods.

The decisive extra fact is that the angular covectors on \(E_{a,J}\) depend
only on \(u=x_a\).  Fix \(x\in E_{a,J}\).  Openness of
\(H_i^a\neq0\), for all \(i\in J\), gives a product neighborhood of \(x\)
on which all those channels remain active.  Varying only \(u\) shows that
every \(B_i^a(u)\) remains a nonzero boundary vector on an open
neighborhood of \(x_a\).  Its normalized phase

\[
                            q_i^a(u)\in S^1
\]

is therefore defined there.  Moreover, the \(p\) angular forms
\(\langle Jq_i^a,Dq_i^a\rangle\), \(i\in J\), form a coframe at \(x_a\):
the corresponding \(p\) positive rank-one forms are the only terms in (5),
and their sum has rank \(p\).  Coframe independence persists after
shrinking the neighborhood.

Compactness of \(E_{a,J}\) now gives an open neighborhood
\(P_{a,J}\) of \(\pi_a(E_{a,J})\) in \(S^p\) on which

\[
 Q_{a,J}=(q_i^a)_{i\in J}:P_{a,J}\longrightarrow (S^1)^p  \tag{17}
\]

is a local diffeomorphism.  This neighborhood is necessarily proper.  If
it were all of \(S^p\), compactness would make (17) a finite covering of the
torus.  That is impossible for \(p\geq2\): \(S^p\) is simply connected,
whereas the universal cover of \((S^1)^p\) is noncompact.

Every proper open subset of the connected closed oriented \(p\)-manifold
\(S^p\) has zero ordinary top real cohomology: each component is a
noncompact \(p\)-manifold.  Hence a generator
\(u\in H^p(S^p;\mathbb R)\) restricts to zero on \(P_{a,J}\).  Choose the
previous pairwise disjoint neighborhoods of the compact sets \(E_{a,J}\)
small enough that

\[
                W_{a,J}\subseteq\pi_a^{-1}(P_{a,J}),
 \qquad U_a:=\coprod_J W_{a,J}\supseteq E_a.
\]

Writing \(u_a=\pi_a^*u\), disjointness of the union gives

\[
                              u_a|_{U_a}=0.                  \tag{18}
\]

The sets \(U_1,\ldots,U_k\) cover \(M\).  The standard relative cup-product
lemma now gives

\[
                              u_1\smile\cdots\smile u_k=0.  \tag{19}
\]

For completeness, lift each class in (18) to
\(H^p(M,U_a;\mathbb R)\).  Their relative cup product lies in
\(H^{kp}(M,\bigcup_aU_a;\mathbb R)=H^{kp}(M,M;\mathbb R)=0\), and its image
in absolute cohomology is the left side of (19).  But the Kunneth formula
gives

\[
 u_1\smile\cdots\smile u_k
       \neq0\in H^{kp}((S^p)^k;\mathbb R),
\]

contradicting (19).  This proves (3) without a parity restriction.  When
\(p\) is even, the shorter Euler-class version follows from
\(e(\pi_a^*TS^p)=2u_a\); the local-diffeomorphism argument is what also
handles odd \(p\).

## 4. Arbitrary Lorentz dimension caps

Let channel \(i\) take values in \(Q_{m_i}\) and put

\[
                         r_i=m_i-2,\qquad 1\leq r_i\leq c:=d-2. \tag{19a}
\]

At a nonzero complementary contact, the normalized Lorentz phase lies in
\(S^{r_i}\), and the calculation in (8) becomes

\[
 H_i^a=\alpha_i\beta_i^a(Dq_i^a)^*Dq_i^a,
 \qquad \operatorname{rank}H_i^a\leq r_i.                  \tag{19b}
\]

The vertex cases still give zero.  Strict convexity of the Lorentz cone
still gives a unique complementary ray, so the pointwise no-sharing
implication (12) is unchanged.

Define the active capacity of source block \(a\) by

\[
                    C_a(x)=\sum_{i:H_i^a(x)\neq0}r_i,
 \qquad T=\sum_{i=1}^Lr_i.                                  \tag{19c}
\]

Rank in (5) and pointwise disjointness give

\[
                 C_a(x)\geq p,\qquad \sum_aC_a(x)\leq T.   \tag{19d}
\]

Suppose \(c<p\) and \(T\leq k(p+1)-1\).  Then the closed sets
\(E_a=\{C_a=p\}\) cover \(M\).  Partition each \(E_a\) into its finitely
many clopen exact-active-label strata \(E_{a,J}\).  On such a stratum,
\(\sum_{i\in J}r_i=p\); equality in the rank bound forces every
\(Dq_i^a\) to have rank \(r_i\), and the joint phase map is locally
diffeomorphic on a neighborhood of \(\pi_a(E_{a,J})\):

\[
Q_{a,J}:P_{a,J}\longrightarrow\prod_{i\in J}S^{r_i}.
                                                                  \tag{19e}
\]

Here the phase domain is rigorous even when a dual factor has a large vertex
set.  For each \(i\), take the interior in \(S^p\) of
\(\{u:B_i^a(u)\in\partial Q_{m_i}\setminus\{0\}\}\).  An active contact
point projects into this interior: keep all other primal blocks fixed and
vary \(x_a\); the primal factor remains nonzero nearby, while continuity
keeps the dual factor nonzero, so complementarity forces it to remain on the
boundary.  On the intersection of these open phase domains, full rank of
the product differential is an open condition.  Compactness of
\(E_{a,J}\) therefore supplies the stated open \(P_{a,J}\).

The phase neighborhood \(P_{a,J}\) is proper.  Otherwise compactness makes
(19e) a covering.  If some \(r_i=1\), the target has infinite fundamental
group and its universal cover is noncompact.  If every \(r_i\geq2\), both
domain and target are simply connected, so the covering would be a
diffeomorphism; but \(|J|\geq2\), since every \(r_i\leq c<p\), and a product
of two or more positive-dimensional spheres has nonzero intermediate
integral cohomology while \(S^p\) does not.

The proper-neighborhood and relative top-class proof of Section 3 now
applies verbatim and contradicts \(u_1\cdots u_k\neq0\).  Therefore

\[
                              T\geq k(p+1)=ks.               \tag{19f}
\]

The exact factor count needs one additional integer case.  Pointwise rank
and the cap give

\[
                         N_a(x)\geq \left\lceil{p\over c}\right\rceil.
                                                                  \tag{19g}
\]

If \(c\nmid p\), the right side already equals
\(\lceil(p+1)/c\rceil=\lceil s/(d-2)\rceil\), and pointwise disjointness
gives the desired additive count.  If \(p=tc\), suppose instead that
\(L\leq k(t+1)-1\).  The closed sets where block \(a\) has exactly \(t\)
active labels cover \(M\).  On every exact-label stratum, rank \(p=tc\)
forces all \(t\) channels to have \(r_i=c\) and the product phase map

\[
                            S^p\dashrightarrow(S^c)^t       \tag{19h}
\]

to be locally diffeomorphic near its projection.  Here \(t\geq2\) because
\(c<p\), so the same covering obstruction and top-class argument apply.
Consequently

\[
                   L\geq k\left\lceil{s\over d-2}\right\rceil. \tag{19i}
\]

Since

\[
                         D_{\rm amb}=T+2L,
\]

(19f) and (19i) give the first two lower bounds in (3a).  A product of \(L\)
Lorentz cones has optimal ambient barrier parameter \(2L\), including
coupled ambient barriers by restriction to its \(2L\)-orthant section, so
(19i) gives the third.

All three are attained simultaneously.  Partition the \(s\) coordinates of
each source ball into
\(h=\lceil s/(d-2)\rceil\) nonempty groups \(G\) of size at most \(d-2\),
and use

\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
                   {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(z)&=\left({1+\|z_G\|^2\over2},
                  -{1-\|z_G\|^2\over2},-z_G\right)
                  \in Q_{|G|+2}.                            \tag{19j}
\end{aligned}
\]

Their pairing is \(\|x_G-z_G\|^2/2\).  Concatenating groups and source
balls gives (3a), with inactive dual factors at the cone vertex.

If \(c\geq p\), (19d) gives \(T\geq kp\), pointwise no-sharing gives
\(L\geq k\), and hence \(D_{\rm amb}\geq k(p+2)=k(s+1)\).  One direct
\(Q_{s+1}\) factor per source ball,
\(A_a(x)=(1,x_a)\) and
\(B_a^b(z)=\mathbf1_{a=b}(1,-z)\), attains (3b).

### Heterogeneous dimensions

The same proof gives (3c)--(3d).  Let
\(R=\{a:c<p_a\}\).  Pointwise disjointness gives
\(C_a(x)\geq p_a\).  If total capacity were below
\(\sum_a\tau_a=\sum_ap_a+|R|\), then at every point some \(a\in R\)
would have \(C_a(x)=p_a\).  These closed loci cover the product.  On each
exact-label stratum the phase capacities sum to \(p_a\), with every
individual capacity strictly smaller than \(p_a\).  The proper phase
neighborhood and relative cup argument would force
\(\prod_{a\in R}u_a=0\), contradicting the Kunneth theorem.  This proves
the capacity part of (3d).

For factor count, pointwise rank gives the baseline
\(\lceil p_a/c\rceil\) for \(a\in R\), and one for \(a\notin R\).
The only sources where this is below \(h_a\) form

\[
 D=\{a:c<p_a\text{ and }c\mid p_a\}.                       \tag{19k}
\]

If \(L<\sum_ah_a\), then at every point some \(a\in D\) has exactly
\(p_a/c\) active labels.  Those closed loci cover the product.  On every
exact-label stratum, full rank forces all active labels to have capacity
\(c\), and the joint phase map is locally diffeomorphic into
\((S^c)^{p_a/c}\).  Since \(c<p_a\), this product has at least two factors,
so its phase neighborhood is proper.  The relative cup argument now
contradicts \(\prod_{a\in D}u_a\neq0\).  If \(D\) is empty, the pointwise
count already gives \(\sum_ah_a\).

For attainment, use one direct \(Q_{p_a+2}\) block when \(c\geq p_a\),
and \(\lceil s_a/c\rceil\) grouped factors when \(c<p_a\).  This
simultaneously attains all three quantities in (3d), including every last
smaller coordinate group.

### Structural lower bound for smooth strictly convex factors

The lower-bound proof is not Euclidean-specific.  Let
\(K_a\subset\mathbb R^{p_a+1}\), \(p_a\geq2\), be compact strictly convex
bodies containing the origin in their interiors.  Assume their primal and
polar boundaries \(X_a=\partial K_a\) and
\(Y_a=\partial K_a^\circ\) are compact connected \(C^1\) manifolds of
extreme points, the normalized contact map

\[
 \gamma_a:X_a\longrightarrow Y_a,
 \qquad \langle x,\gamma_a(x)\rangle=1,
\]

is a \(C^1\) diffeomorphism, and the mixed contact form

\[
             G_{a,x}(u,v)=\langle u,D\gamma_a(x)[v]\rangle \tag{19s}
\]

is nondegenerate.  Suppose the full rows
\(1-\langle x_a,y\rangle\), \(y\in Y_a\), have globally labelled \(C^1\)
Lorentz factors with common primal maps on \(\prod_aX_a\).

Pulling the dual factors back by \(\gamma_a\), contact differentiation gives
\(G_a=\sum_iH_i^a\).  Every nonzero Lorentz contact channel is the same PSD
phase Gram form as (19b); hence the assumed nondegeneracy makes \(G_a\)
positive definite of rank \(p_a\).  The contact zeros are still cylinders,
so pointwise row-disjointness is unchanged.  Each \(X_a\) is
\(C^1\)-diffeomorphic to \(S^{p_a}\).  Capacity-saturated phase products
therefore lie over proper local-diffeomorphism domains exactly as above, and
the relative product of the top classes of the \(X_a\)'s gives the same
contradiction.

Thus the heterogeneous quantities in (3c) give valid **lower bounds** for
these products of strictly convex bodies:

\[
 L\geq\sum_ah_a,\qquad
 \sum_i r_i\geq\sum_a\tau_a,\qquad
 D_{\rm amb}\geq\sum_a(\tau_a+2h_a),\qquad
 \nu_{\rm ambient}\geq2\sum_ah_a.                         \tag{19t}
\]

No matching construction is asserted for general \(K_a\); the grouped
paraboloid construction is specific to balls.  The nondegeneracy assumption
is essential as stated: \(C^1\) strict convexity alone need not make
\(D\gamma_a\) nonsingular.

## 5. Exact regularity premium over semialgebraic norm-tree lifts

For products of balls there is a matching nonsmooth comparison frontier.
Consider proper exact affine lifts over products of Lorentz cones
\(Q_{r_i+2}\), with \(1\leq r_i\leq c\), but do not require globally
\(C^1\) contact selections.  The lift and its slack-factor selections may
be chosen semialgebraically by the cone-factorization correspondence and
definable choice.  A finite semialgebraic stratification supplies one
common point of \(\prod_aS^{p_a}\) at which all selected primal factors and
all row-specific dual factors are \(C^1\) on open neighborhoods.

At that point, the contact Gram identity and pointwise no-sharing argument
of Sections 1--2 apply.  Each source row uses disjoint active capacity at
least \(p_a\) and at least

\[
                         h_a^{(0)}=\left\lceil{p_a\over c}\right\rceil
                                                                  \tag{19l}
\]

active factors.  Consequently

\[
 T:=\sum_i r_i\geq T_0:=\sum_ap_a,
 \qquad
 L\geq L_0:=\sum_ah_a^{(0)},                               \tag{19m}
\]

and

\[
 M_{\rm amb}\geq T_0+2L_0,
 \qquad
 \nu_{\rm ambient}\geq2L_0.                               \tag{19n}
\]

These bounds are simultaneous and exact.  For each source ball, partition
\(p_a=s_a-1\) into \(h_a^{(0)}\) positive integers at most \(c\).  A rooted
norm tree whose internal nodes have these excess arities has \(s_a\)
leaves: a node of excess arity \(r\) combines \(r+1\) child norms in one
\(Q_{r+2}\) constraint.  Separate trees therefore use total capacity
\(p_a\), exactly \(h_a^{(0)}\) factors, and ambient dimension
\(p_a+2h_a^{(0)}\).  Their auxiliary norm selections are semialgebraic and
piecewise smooth, but generally fail global \(C^1\) regularity when a
subtree norm vanishes.

Comparing (3c)--(3d) with (19l)--(19n) gives the exact global-selection
regularity premium.  With

\[
 R=\{a:c<p_a\},\qquad
 D=\{a:c<p_a\text{ and }c\mid p_a\},
\]

globally labelled bi-\(C^1\) extreme-contact factors add

\[
 \Delta T=|R|,\qquad
 \Delta L=|D|,
 \qquad
 \Delta M_{\rm amb}=|R|+2|D|,
 \qquad
 \Delta\nu_{\rm ambient}=2|D|.                             \tag{19o}
\]

For pure \(Q_3\) lifts, \(c=1\), so every \(p_a\geq2\) belongs to both
sets.  The semialgebraic norm-tree frontier uses
\(\sum_a(s_a-1)\) blocks and capacity, whereas global \(C^1\) selections
require \(\sum_as_a\) blocks and capacity.  This is an ambient-formulation
comparison, not an intrinsic barrier or IPM iteration lower bound for the
projected body.

## 6. A sharp support-regularity corollary

There is also a useful \(C^1\) result in every dimension \(s\geq3\).  Assume
that each dual factor \(B_i^a\) is either identically zero or has dense
nonzero locus in \(S^p\), equivalently its vertex-zero set has empty
interior.  Then

\[
                              L\geq ks                       \tag{20}
\]

for both parities of \(s\).

Indeed, whenever \(B_i^a(u)\neq0\), cylindrical complementarity gives

\[
                         A_i\wedge D_bA_i=0\qquad(b\neq a)
\]

on the full cylinder \(x_a=u\).  Density and continuity extend this identity
to all of \(M\).  The productive channel sets are therefore globally
disjoint exactly as in the analytic proof.  Each block needs at least \(p\)
channels by (5).  Equality with \(p\) would make all \(p\) rank-one channels
nonzero everywhere and produce a submersion \(S^p\to S^1\).  Since
\(p\geq2\), this phase map lifts to a real-valued function on the compact
sphere and has a critical point, a contradiction.  Thus every block needs
at least \(p+1=s\) globally disjoint productive labels.

This hypothesis is no longer needed for the exact count, but it gives the
stronger channelwise conclusion that globally productive label sets for
different source blocks are disjoint.  The flat
\(\mathbb R_{\exp}\)-definable witness in the companion analytic note shows
why this stronger conclusion fails without the support hypothesis, even
though the top-class argument still proves the same total count.

## 7. Exact construction and optimization scope

With

\[
 U(t)=\left({1+t^2\over2},{1-t^2\over2},t\right),\qquad
 V(t)=\left({1+t^2\over2},-{1-t^2\over2},-t\right),
\]

one has \(U(t),V(t)\in Q_3\) and
\(\langle U(t),V(u)\rangle=(t-u)^2/2\).  The \(ks\) factors

\[
 A_{b,j}(x)=U((x_b)_j),\qquad
 B_{b,j}^a(z)=\mathbf1_{a=b}V(z_j)                           \tag{21}
\]

sum to (1), so (3) is exact.

For a pure-\(Q_3\) lift possessing the global \(C^1\) primal and dual
extreme-contact selections in (2), every \(s\geq3\) therefore forces at
least \(ks\) cone blocks.  Within this regular-lift class the matching
coordinate-square formulation has ambient cone dimension \(3ks\), and the
unchanged ambient product has optimal barrier parameter \(2ks\), even for
coupled ambient barriers, by restriction to its \(2ks\)-orthant section.
These are formulation-level statements.  They are not intrinsic barrier or
IPM iteration lower bounds for the projected product of balls.

## 8. Scope and literature screen

The proof requires the globally labelled factor maps only to be \(C^1\).
It does not assume analytic continuation, unique lift fibers, or nonzero
factors.  It applies to the full family of polar extreme rows; a single
fixed positive-weight contact slack does not provide the cylindrical
pointwise no-sharing relation (12).

There is no parity restriction.  The first Euler-class proof only handled
even \(p\), but the proper phase-neighborhood argument kills the ordinary
top class of \(S^p\) in every dimension.  The scope that remains essential
is regularity and selection: norm-tree lifts may have fewer blocks because
their natural contact factors become singular where intermediate norms
vanish and do not meet the global \(C^1\) hypothesis.

The lift/factorization correspondence is due to Gouveia, Parrilo, and
Thomas, *Mathematics of Operations Research* 38 (2013), DOI
[10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).  Fawzi's
general second-order-cone obstruction is in *Mathematical Programming*
(2019), DOI
[10.1007/s10107-018-1233-0](https://doi.org/10.1007/s10107-018-1233-0).
For the covering-space, top-cohomology, and relative cup-product facts, see
Hatcher, [*Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).
The semialgebraic definable-choice and finite-stratification facts used in
Section 5 are standard; see Bochnak, Coste, and Roy,
[*Real Algebraic Geometry*](https://doi.org/10.1007/978-3-662-03718-8).

Targeted searches did not locate the contact-Hessian open-cover argument,
the top-class cup-product lower bound for full product-ball Lorentz
factorizations, the arbitrary-\(C^1\) capped frontier, or the support-dense
channelwise theorem.  Novelty is plausible pending specialist review.

## 9. Independent hostile audit

An independent hostile audit passed the full \(Q_3\) proof.  It checked that
mixed differentiation uses only \(DA_i\) and \(DB_i^a\), vertex derivatives
vanish by pointedness, nonzero contact channels give the exact PSD rank-one
square (8), and cylindrical complementarity proves pointwise cross-row
disjointness without continuation.  It also checked lower semicontinuity of
\(N_a\), the finite clopen compact exact-label strata, and the relative cup
product.

The audit separately passed the parity-removing step.  Openness of the
active Hessians supplies the needed product neighborhood on which the dual
factors remain nonzero boundary vectors.  The \(p\) phase differentials form
a coframe, so (17) is locally diffeomorphic.  A global such map would be an
impossible covering of the torus; a proper open sphere subset has zero
ordinary top cohomology.  Thus the classes \(u_a\), rather than only the
even-sphere Euler classes, vanish on the cover pieces, and the proof works
for every \(p\geq2\).

The arbitrary-cap extension in Section 4 passed a second independent audit.
For a capacity-saturated stratum, positivity and
\(\sum_i r_i=p=\operatorname{rank}g\) force every partial rank bound to be
an equality and make the joint phase derivative invertible.  A global
covering of \(\prod_iS^{r_i}\) by \(S^p\) is impossible: an \(S^1\) factor
gives a noncompact universal cover, while with all \(r_i\geq2\) the covering
would be a diffeomorphism and contradict intermediate cohomology.  This
verifies \(T\geq k(p+1)\).  When the cap \(c\) divides \(p\), the analogous
exact-active-label cover forces the extra factor; when it does not,
pointwise counting already gives the same ceiling.  The resulting lower
bounds for \(L\), \(D_{\rm amb}=T+2L\), and the ambient product-barrier
parameter match the grouped construction, including the residual group.

A separate hostile audit passed the structural strictly-convex extension.
It verified the \(C^1\) pullback by \(\gamma_a\), the identity
\(\sum_iH_i^a=G_a\), positivity and full rank forced by the Gram sum,
cylindrical pointwise no-sharing, and the proper-domain/top-class argument.
It also confirmed the stated lower-bound-only scope and the need to assume
nondegeneracy of the contact differential.
The same audit checked the heterogeneous corollary: a one-unit deficit in
total capacity covers the product by exact-capacity loci from the
small-cap sources, while a deficit in factor count covers it by the
divisible-cap exact-count loci.  The corresponding subproducts of sphere
fundamental classes remain nonzero, and the direct/grouped construction
attains the resulting additive formulas (3c)--(3d).

The semialgebraic comparison in Section 5 was audited as well.  Definable
choice supplies labelled semialgebraic slack factors for a proper Lorentz
lift, and finite stratification gives a common point where all primal and
row-dual selections are \(C^1\) on open neighborhoods.  The pointwise Gram
and no-sharing argument therefore gives the additive baseline capacity and
factor counts even though the selections can be singular elsewhere.  A
rooted tree with internal excess arities \(r_j\in[1,c]\) has
\(1+\sum_jr_j\) leaves, so partitioning \(p_a\) verifies the exact norm-tree
attainment.  Subtracting the two exact heterogeneous frontiers gives
\(\Delta T=|R|\), \(\Delta L=|D|\), and consequently the dimension and
ambient-barrier premiums in (19o), with no hidden residual-group case.
