# Saturated cone factors force sphere-to-sphere submersions

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

Role: Audited low-regularity bridge and rank-one stepping stone.  The
canonical full rigidity theorem, including Browder--Serre classification and
the exact cap-dependent frontier, is
[Sphere submersions force a strict curvature-capacity gap](2026-09-04-sphere-submersion-curvature-gap.md).

## Theorem

Let \(M\) be the contact boundary of a compact \(C^2\), strictly positively
curved body in \(\mathbb R^{n+1}\), so \(M\) is diffeomorphic to \(S^n\).
Suppose its exact slack on the full contact manifold has globally labelled
\(C^1\) factors

\[
 s(x,z)=\sum_{i=1}^k\langle A_i(x),B_i(z)\rangle,\qquad
 A_i(x)\in K_i,\quad B_i(z)\in K_i^*,                         \tag{1}
\]

where each \(K_i\) is a finite-dimensional proper cone. Put

\[
                         r_i=(\dim K_i-2)_+
\]

and assume the universal curvature budget is saturated:

\[
                              \sum_i r_i=n.                    \tag{2}
\]

Then every positive-capacity block \(r_i>0\) canonically induces a
\(C^1\) submersion

\[
                              p_i:S^n\longrightarrow S^{r_i}. \tag{3}
\]

No smoothness of \(\partial K_i\) is assumed. Its required \(C^1\)
regularity is forced along the entire normalized base boundary by
saturation and global factor regularity.

In particular, if \(n\geq2\), no saturated factorization (1)--(2) can
contain even one three-dimensional block:

\[
                         r_i=1\quad\Longrightarrow\quad
                         \text{contradiction}.                 \tag{4}
\]

This is stronger than counting three-dimensional summands using Adams's
vector-field theorem: (4) also applies when the other saturated blocks have
arbitrary dimensions, and it closes the parallelizable-sphere exceptions.

## Step 1: saturation gives full-rank mixed channels

At a contact \(x\), nonnegativity of all cone pairings and zero total slack
give

\[
                         \langle A_i(x),B_i(x)\rangle=0.        \tag{5}
\]

Define the mixed tangent channel

\[
                    M_i(x)=-dA_i(x)^*dB_i(x):T_xM\to T_x^*M.  \tag{6}
\]

Mixed differentiation of the slack says that \(\sum_iM_i(x)\) is the
positive mixed-curvature metric, hence has rank \(n\). The universal
tangent-pairing lemma gives

\[
                         \operatorname{rank}M_i(x)\leq r_i.
\]

Together with (2), rank subadditivity forces

\[
                         \operatorname{rank}M_i(x)=r_i         \tag{7}
\]

for every \(i,x\). This argument uses no symmetry or positivity of the
individual channels.

If \(r_i>0\), neither \(A_i(x)\) nor \(B_i(x)\) can be zero. Indeed, the
two-sided derivative of a cone-valued \(C^1\) map at the cone vertex lies
in \(K_i\cap(-K_i)=\{0\}\), which would make the corresponding side of
(6) zero and contradict (7).

## Step 2: normalization and the exact rank of \(dp_i\)

Fix \(i\) with \(r=r_i>0\), write \(m=\dim K_i=r+2\), and choose
\(\ell\in\operatorname{int}K_i^*\). The affine base

\[
 D=\{z\in K_i:\ell(z)=1\}
\]

is a compact \((r+1)\)-dimensional convex body. Define

\[
                 p(x)={A_i(x)\over\ell(A_i(x))}.                \tag{8}
\]

Since \(B_i(x)\neq0\) and (5) holds, \(A_i(x)\) is not interior to \(K_i\).
Thus

\[
                              p(M)\subseteq J:=\partial D,      \tag{9}
\]

and \(J\) is topologically \(S^r\).

Fixed-variable nonnegativity also gives

\[
 dA_i(T_xM)\subseteq B_i(x)^\perp,\qquad
 dB_i(T_xM)\subseteq A_i(x)^\perp.                              \tag{9a}
\]

Consequently (6) factors through

\[
 \overline {dA_i}:T_xM\to B_i(x)^\perp/\operatorname{span}A_i(x),
 \quad
 \overline {dB_i}:T_xM\to A_i(x)^\perp/\operatorname{span}B_i(x).
\]

Both quotient spaces have dimension \(m-2=r\), and their induced pairing
is nondegenerate. Equation (7) therefore forces
\(\operatorname{rank}\overline {dA_i}=r\).

We claim

\[
                              \operatorname{rank}dp(x)=r       \tag{10}
\]

everywhere. Direct differentiation gives, with \(a=A_i(x)\) and
\(X=dA_i(x)\),

\[
 dp(x)u={Xu\over\ell(a)}
       -{a\,\ell(Xu)\over\ell(a)^2}.
\]

Hence

\[
 dp(x)u=0
 \iff Xu\in\operatorname{span}a
 \iff \overline {dA_i}(x)u=0.
\]

It follows directly that
\(\operatorname{rank}dp(x)=\operatorname{rank}\overline {dA_i}=r\).

The rank cannot be \(r+1\): the submersion theorem would make \(p\) map a
neighborhood of \(x\) onto a relatively open subset of the
\((r+1)\)-dimensional affine hull of \(D\), whereas (9) lies in the
boundary of a convex body and has empty interior there. This proves (10).

## Step 3: constant rank forces a smooth full boundary

Although \(J\) was initially only a topological sphere, (10) forces enough
regularity. At every \(x\), the constant-rank theorem supplies an
\(r\)-dimensional local transversal \(T_x\subset M\) on which \(p\) is a
\(C^1\) embedding. Its image is a regular embedded \(r\)-disk contained in
\(J\).

Choose any radial homeomorphism \(h:J\to S^r\). The restriction
\(h\circ p|_{T_x}\) is a continuous injection between \(r\)-manifolds.
Invariance of domain makes its image open in \(S^r\). Thus
\(p(T_x)\) is relatively open in \(J\). It follows that \(p(M)\) is open
in \(J\). It is compact and hence closed; since \(J\cong S^r\) is
connected for \(r>0\),

\[
                                  p(M)=J.                       \tag{11}
\]

The relatively open embedded patches \(p(T_x)\) cover \(J\). Their overlap
maps are \(C^1\), being transitions between regular parametrizations of the
same embedded subsets of the ambient affine space. They therefore give
\(J\) a compatible \(C^1\) embedded-hypersurface structure for which \(p\)
is a submersion.

This induced sphere is the standard \(C^1\) sphere. To see this explicitly,
choose \(c\in\operatorname{int}D\) and consider radial projection

\[
                    \rho:J\to S^r,\qquad
                    \rho(z)={z-c\over\|z-c\|}.                 \tag{12}
\]

It is a \(C^1\) bijection. At \(z\in J\), let \(\nu(z)\) be the supporting
normal of the now-\(C^1\) convex boundary. Since \(c\) is interior,

\[
                         \langle\nu(z),z-c\rangle>0.            \tag{13}
\]

The kernel of \(d\rho(z)\) in the ambient affine space is the radial line
\(\operatorname{span}(z-c)\). Equation (13) says that this radial vector is
not tangent to \(J\). Hence \(d\rho|_{T_zJ}\) is injective, and equal
dimensions make it invertible. Thus \(\rho\) is a \(C^1\) diffeomorphism.
Composing \(p\) with \(\rho\) proves (3).

## Step 4: a rank-one block is impossible

If \(r_i=1\), (3) is a \(C^1\) submersion

\[
                              p_i:S^n\to S^1.
\]

For \(n\geq2\), the domain is simply connected, so \(p_i\) lifts through
the universal cover \(\mathbb R\to S^1\) to a real-valued \(C^1\) function
\(\theta_i:S^n\to\mathbb R\). Compactness gives a maximum of \(\theta_i\),
where \(d\theta_i=0\). This contradicts the submersion property and proves
(4).

## Consequences and scope

For the Euclidean ball \(B_2^N\), \(n=N-1\).  Concretely, let
\(K_1,\ldots,K_{N-1}\) be arbitrary closed, pointed, full-dimensional
cones in \(\mathbb R^3\).  If globally labelled \(C^1\) maps

\[
 A_i:S^{N-1}\to K_i,\qquad B_i:S^{N-1}\to K_i^*
\]

obey

\[
 1-\langle x,y\rangle
   =\sum_{i=1}^{N-1}\langle A_i(x),B_i(y)\rangle
 \qquad(x,y\in S^{N-1}),                                      \tag{14}
\]

then \(N\leq2\).  Thus for \(N\geq3\) an exact globally \(C^1\)
factorization by arbitrary three-dimensional proper cones needs at least
\(N\) blocks.  More strongly, any mixed saturated profile cannot contain
even one three-dimensional factor.

These assumptions are minimal for this proof.  Strict convexity,
\(C^1\) or \(C^2\) regularity of a cone or its dual boundary,
self-duality, and separately assumed nonzero complementary pairs are not
needed.  Nonzero pairs follow from the full mixed-channel rank forced by
saturation.  The \(C^1\) hypothesis is on the selected factor maps, not on
the cones.  The restriction \(N\geq3\) is essential: for \(N=2\), the disk
itself is a one-\(Q_3\) affine section and the circle phase need not lift to
a single-valued real function.

The theorem is conditional on global factor selections. It does not assert
that a cone lift supplies such selections, nor does it rule out nonsmooth
norm-tree lifts. The companion
[globally smooth \(Q_3^N\) construction](2026-09-04-smooth-q3n-ball-factorization.md)
shows that one extra three-dimensional block is sufficient for the ball and
that rank dropouts then occur exactly where the submersion obstruction
requires them.

For \(r_i>1\), (3) converts cone-factor saturation into the classical
topology problem of sphere-to-sphere submersions.  The canonical companion
applies Browder's fiber theorem and the Serre spectral sequence to complete
that classification and prove exact unsplitness.  This note deliberately
retains the independently audited bridge proof and the elementary rank-one
obstruction.

## Literature boundary

The constant-rank theorem, invariance of domain, radial parametrization of
convex-body boundaries, and covering-space lift are classical. A targeted
search found no source deriving the submersions (3) from saturation of a
cone-factor curvature budget. The apparently new step is the chain

\[
 \text{saturated tangent pairing}
 \Longrightarrow \operatorname{rank}dp_i=r_i
 \Longrightarrow S^n\to S^{r_i}\text{ submersion}.
\]

Novelty remains subject to specialist review. The induced-boundary
regularity argument is included explicitly because assuming a smooth cone
boundary would materially weaken the result.

The closest recent title found in the screen was Aubrun--La
Piana--Müller-Hermes,
[*Factorization through Lorentz cones*](https://arxiv.org/abs/2606.27825).
That paper studies when positive linear maps factor through direct sums of
Lorentz cones, including low-dimensional and square-based cones.  It does
not impose global \(C^1\) contact selections, derive normalized boundary-ray
submersions, or state the saturated ball-slack obstruction above.

An independent hostile audit verified the vertex case, the quotient-pairing
rank argument, the exact formula for \(dp_i\), the constant-rank and
invariance-of-domain steps on an initially nonsmooth convex boundary, and
the radial transversality argument (13). No error was found. Classification
of the possible higher-dimensional submersions in (3) is delegated to the
companion sphere-submersion note rather than asserted here.
