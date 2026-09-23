# Joint saturation forces a covering by sphere factors

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; the cone-to-sphere bridge was audited separately

## Main theorem

Let \(P,D\) be compact connected \(C^1\) manifolds without boundary, of dimension \(n\),
and let \(\zeta:P\to D\) be a continuous contact correspondence. Suppose a
nonnegative kernel has globally labelled \(C^1\) factors over proper cones
\(K_i\):

\[
  s(x,z)=\sum_i\langle A_i(x),B_i(z)\rangle\geq0,
 \qquad A_i(x)\in K_i,\quad B_i(z)\in K_i^*.                \tag{1}
\]

Assume \(s(x,\zeta(x))=0\) for every \(x\), and that the contact mixed
pairing

\[
 H_x(v,w)=-\sum_i\langle dA_i(x)v,dB_i(\zeta(x))w\rangle,
 \qquad v\in T_xP,\quad w\in T_{\zeta(x)}D,                 \tag{1a}
\]

is nondegenerate. No derivative of \(\zeta\) is used.

Put

\[
                 c_i=(\dim K_i-2)_+,
 \qquad I_+=\{i:c_i>0\},
 \qquad S=\sum_i c_i.                                      \tag{2}
\]

The local mixed-curvature bound says \(S\geq n\). If equality holds, then
there are globally \(C^1\) submersions

\[
                         p_i:P\longrightarrow S^{c_i}
                         \qquad(i\in I_+)                   \tag{3}
\]

whose product map

\[
     p=(p_i)_{i\in I_+}:P\longrightarrow
                       \prod_{i\in I_+}S^{c_i}              \tag{4}
\]

is a finite covering. In particular:

1. if \(P\) is simply connected, no \(c_i\) equals one and (4) is a
   \(C^1\) diffeomorphism;
2. if \(P\cong S^n\), exactly one positive block occurs and its capacity
   is \(n\);
3. if \(P\cong(S^q)^k\), \(q\geq2\), exactly \(k\) positive blocks occur
   and every capacity equals \(q\).

Thus equality in a sum of independent local rank bounds has a global
integrability consequence: it determines the contact manifold, up to a
finite cover, as the product of the normalized cone-boundary spheres.

For the full slack of a bi-\(C^1\) strictly convex body, take
\(P=\partial C\), \(D=\partial C^\circ\), and let \(\zeta\) be normalized
supporting polarity. Then (1a) is the nondegenerate Euclidean pairing in
the two independent tangent charts. The sphere consequence gives
immediately

\[
 \boxed{
   \text{at least two positive blocks, or all }c_i<n
   \quad\Longrightarrow\quad S\geq n+1.
 }                                                           \tag{5}
\]

Unlike the earlier block-by-block proof, (5) needs no classification of
individual sphere submersions and has no exceptional Hopf dimensions.

For any globally labelled \(C^1\) cone factorization (1) of the weighted
all-active contact kernel of a product of balls, take

\[
 P=D=(S^{s-1})^k,
 \qquad s_\lambda(x,z)=\sum_{a=1}^k
                   \lambda_a(1-\langle x_a,z_a\rangle),     \tag{5a}
\]

where \(s\geq3\), \(\lambda_a>0\), and \(\sum_a\lambda_a=1\), with
\(\zeta(x)=x\). Its mixed pairing is the positive-definite weighted
product metric. Equality in total capacity,

\[
                         S=k(s-1),                           \tag{5b}
\]

therefore forces exactly \(k\) positive blocks, each of capacity \(s-1\)
and hence cone dimension \(s+1\). The separate Lorentz factors
\(Q_{s+1}^k\) attain this profile. Thus minimum total curvature capacity
admits no reduction or redistribution of the separate-block capacity
profile. It does not prove that each normalized block map depends on only
one ball; the covering diffeomorphism may mix the input factors. This is a
theorem about the fixed weighted contact kernel (5a). A full lift inherits
it only when globally labelled bi-\(C^1\) selected factors restrict to
this stratum.

## 1. Saturated blocks produce sphere maps

At a contact pair \((x,z)=(x,\zeta(x))\), write

\[
 M_i(x,z)(v,w)
   =-\langle dA_i(x)v,dB_i(z)w\rangle,
 \qquad
 \sum_iM_i(x,z)(v,w)=H_x(v,w).                              \tag{6}
\]

Every summand in (1) is nonnegative by cone duality, while their contact
sum is zero. Hence
\(\langle A_i(x),B_i(z)\rangle=0\) for every block at every contact.

The pairing on the right is nondegenerate by hypothesis. Every channel
satisfies

\[
                         \operatorname{rank}M_i\leq c_i.    \tag{7}
\]

If \(S=n\), equality holds throughout rank subadditivity, so

\[
                         \operatorname{rank}M_i=c_i         \tag{8}
\]

at every contact pair. For \(c_i>0\), (8) excludes the cone vertex on
both sides. Choose \(\ell_i\in\operatorname{int}K_i^*\), normalize

\[
 \widehat p_i(x)={A_i(x)\over\ell_i(A_i(x))},               \tag{9}
\]

and let \(J_i\) be the boundary of the compact base
\(K_i\cap\{\ell_i=1\}\). Because each nonnegative individual pairing
vanishes at the contact point, its two fixed-variable first derivatives
vanish:

\[
 \langle dA_i(x)v,B_i(z)\rangle=0,
 \qquad
 \langle A_i(x),dB_i(z)w\rangle=0.                         \tag{9a}
\]

Thus the mixed channel factors through the two ray quotients. The quotient
tangent calculation gives

\[
 d\widehat p_i(x)v=0
 \quad\Longleftrightarrow\quad
 dA_i(x)v\in\mathbb R A_i(x),
 \qquad \operatorname{rank}d\widehat p_i=c_i.              \tag{10}
\]

No manifold regularity of \(J_i\) is being assumed here.  As the boundary
of a compact convex body with interior, \(J_i\) is a topological
\(c_i\)-sphere.  The constant-rank theorem supplies, through every
\(x\in P\), a local \(c_i\)-dimensional transversal on which
\(\widehat p_i\) is a \(C^1\) embedding.  Compose its image with any radial
homeomorphism \(J_i\to S^{c_i}\).  Invariance of domain makes that embedded
image relatively open in \(J_i\).  Hence the full image of
\(\widehat p_i\) is open in \(J_i\); it is also compact, and is therefore all
of the connected boundary \(J_i\). Its regular image charts make \(J_i\) a
\(C^1\) hypersurface, and radial projection from an interior base point
gives a \(C^1\) diffeomorphism \(\rho_i:J_i\to S^{c_i}\). Define
\(p_i=\rho_i\circ\widehat p_i\). Since \(d\rho_i\) is invertible, (10)
also describes \(\ker dp_i\), and (3) follows. This is the abstract form
of the separately audited factor-to-submersion lemma.

Blocks with \(c_i=0\) have \(M_i=0\) under saturation by (7), so they play
no role in the remaining argument.

## 2. The common-kernel lemma

Fix \(x\in P\), and put \(z=\zeta(x)\). Suppose

\[
                         v\in\bigcap_{i\in I_+}\ker dp_i(x). \tag{11}
\]

By (10), for each positive block there is a scalar \(\alpha_i\) such that

\[
                         dA_i(x)v=\alpha_iA_i(x).            \tag{12}
\]

For fixed \(x\), the nonnegative function

\[
                         z'\longmapsto
              \langle A_i(x),B_i(z')\rangle
\]

vanishes at the contact point \(z\). Its derivative in every two-sided
tangent direction \(w\in T_zD\) is therefore zero:

\[
                         \langle A_i(x),dB_i(z)w\rangle=0.  \tag{13}
\]

Equations (12)--(13) imply

\[
                         M_i(x,z)(v,w)=0                    \tag{14}
\]

for every positive block and every \(w\). The zero-capacity channels also
vanish. Summing (14) in (6) gives

\[
                         H_x(v,w)=0
                         \qquad(w\in T_zD).
\]

Nondegeneracy of the contact pairing forces \(v=0\). Hence

\[
                         \bigcap_{i\in I_+}\ker dp_i(x)=\{0\}.             \tag{15}
\]

This is the key joint step that is invisible when the blocks are studied
one at a time.

## 3. From local diffeomorphism to finite covering

The derivative of (4) has kernel (15). Its source and target dimensions
are equal because

\[
                 \dim P=n=S=\sum_{i\in I_+}c_i.
\]

Thus \(dp(x)\) is an isomorphism at every point, and the inverse-function
theorem makes \(p\) a local \(C^1\) diffeomorphism. Its image is open. It
is also compact, hence closed, and the target is connected. Therefore
\(p\) is onto. A proper local diffeomorphism is a finite covering, proving
the main assertion.

Suppose now that \(P\) is simply connected. A capacity-one map
\(p_i:P\to S^1\) lifts through \(\mathbb R\to S^1\); the real-valued lift
has an extremum on compact \(P\), contradicting submersivity. Hence every
positive \(c_i\geq2\), so the product target in (4) is simply connected.
Its connected covering by \(P\) has one sheet, and (4) is a \(C^1\)
diffeomorphism.

## 4. Sphere and product-sphere rigidity

For \(n=1\), the identity \(\sum_i c_i=1\) already forces exactly one
positive capacity, equal to one. If \(P\cong S^n\) with \(n\geq2\), a
product of two or more positive-dimensional spheres
has nonzero cohomology in an intermediate degree, whereas \(S^n\) does
not. Thus (4) can be a diffeomorphism only when it has one factor, proving
the second conclusion and (5).

If \(P\cong(S^q)^k\), \(q\geq2\), compare rational cohomology rings in
(4). For a connected graded algebra \(H\), write

\[
                       QH=H^+/(H^+)^2
\]

for its graded vector space of indecomposables. The ring
\(H^*((S^q)^k;\mathbb Q)\) has exactly \(k\) indecomposable generators,
all in degree \(q\). The ring
\(H^*(\prod_iS^{c_i};\mathbb Q)\) has one indecomposable generator in
degree \(c_i\) for each factor. A graded-ring isomorphism preserves these
dimensions degree by degree. Therefore there are exactly \(k\) targets and
every \(c_i=q\), proving the third conclusion.

More generally, for any simply connected compact \(P\), saturation is
possible only if its cohomology ring is that of a product of spheres in
the capacity degrees. Failure of this necessary condition makes the local
integer bound strict: \(S\geq n+1\).

## 5. Consequences and limits

- The strict sphere gap is elementary once the separate factor-to-sphere
  maps are constructed. Browder's fiber theorem and the Hopf-invariant-one
  theorem remain useful classifications of individual sphere submersions,
  but they are unnecessary for a saturated collection.
- For a product-sphere contact manifold, the theorem determines the entire
  saturated capacity multiset, not only the allowed capacity of one block.
- The theorem does not improve the all-\(Q_3\) lower bound beyond one
  excess channel when \(S>n\). Exact saturation is what makes (4)
  same-dimensional; near saturation need not produce a covering.
- The conclusion assumes globally labelled \(C^1\) factor selections.
  It does not assert that every abstract cone lift admits such selections.
- The normalized cone bases are spheres only after saturation supplies
  their regular image charts. No smoothness of the original cone boundary
  is assumed.

## Literature and novelty boundary

The inverse-function and covering-space steps are classical. The
factor-to-sphere bridge is proved in
[Saturated cone factors force sphere-to-sphere submersions](2026-09-04-saturated-factor-submersion-obstruction.md),
and the independent sphere-submersion route is retained in
[Sphere submersions force a strict curvature-capacity gap](2026-09-04-sphere-submersion-curvature-gap.md).

A targeted search found classical results on submersions, coverings,
sphere fibrations, and cone/slack factorizations, but no result assembling
the normalized maps of all saturated cone factors into the covering (4).
The joint common-kernel lemma, its cone-factorization application, and the
resulting exact capacity profiles therefore appear new, subject to
specialist review.

## Audit record

An independent hostile audit first identified and rejected an overly
narrow convex-boundary formulation that could not support the product-
sphere application. After reformulation for abstract contact kernels, it
checked the fixed-variable derivative identities, quotient ranks,
zero-capacity blocks, common-kernel argument, finite-covering step,
capacity-one exclusion, sphere and product-sphere cohomology, and both the
strictly convex and weighted product-ball specializations. The re-audit
passed with no remaining mathematical defect.
