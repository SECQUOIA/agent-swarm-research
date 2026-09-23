# Saturated symmetric-cone factors induce idempotent-orbit coverings

Status: Proved; primary-source-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Headline theorem

Let \(C\subset\mathbb R^{n+1}\), \(n\geq1\), be a compact convex body with
\(0\in\operatorname{int}C\).  Assume that

\[
                         P=\partial C,\qquad D=\partial C^\circ
\]

are \(C^1\), strictly convex hypersurfaces.  Suppose the full slack has a
globally labelled bi-\(C^1\) factorization over irreducible symmetric cones:

\[
  1-\langle x,z\rangle
   =\sum_{i=1}^k\langle X_i(x),Y_i(z)\rangle_i,
 \quad X_i(x),Y_i(z)\in K_i .                              \tag{1}
\]

Write \(V_i\) for the simple Euclidean Jordan algebra whose cone of squares
is \(K_i\), \(r_i\) for its Jordan rank, and \(a_i\) for its Peirce constant.
Set

\[
                 c_i=a_i\left\lfloor {r_i^2\over4}\right\rfloor . \tag{2}
\]

The local Peirce-channel theorem gives

\[
                              \sum_i c_i\geq n.             \tag{3}
\]

If equality holds, then every positive-capacity block has fixed balanced
complementary Jordan ranks

\[
 p_i\in\{\lfloor r_i/2\rfloor,\lceil r_i/2\rceil\},
 \qquad q_i=r_i-p_i,                                       \tag{4}
\]

at every primal--polar contact.  Its primal support idempotent defines a
\(C^1\) submersion

\[
 \sigma_i:P\longrightarrow \mathcal I_{p_i}(V_i),
 \qquad \sigma_i(x)=\operatorname{supp}X_i(x),             \tag{5}
\]

where \(\mathcal I_p(V)\) is the compact connected orbit of rank-\(p\)
idempotents.  Its tangent space and dimension are

\[
 T_e\mathcal I_p(V)=V(e,{1\over2}),\qquad
 \dim\mathcal I_p(V)=a p(r-p)=a p q=c_i.                  \tag{6}
\]

More strongly, the joint support map

\[
 \Sigma:P\longrightarrow\prod_{i:c_i>0}\mathcal I_{p_i}(V_i),
 \qquad \Sigma(x)=(\sigma_i(x))_i                         \tag{7}
\]

is a finite covering.  Since \(P\cong S^n\), classification of the simple
Euclidean Jordan algebras and of their idempotent orbits then gives:

> **Global saturation rigidity.** Saturation has exactly one
> positive-capacity factor.  If \(n\neq2\), that factor must be a rank-two
> spin factor, hence a Lorentz cone of dimension \(n+2\).  If \(n=2\), the
> only additional topological possibility is the real cone
> \(\mathbb S_+^3\), whose balanced support orbit is
> \(\mathbb {RP}^2\) with universal cover \(S^2\).             \(\tag{8}\)

Thus, in contact-sphere dimension at least three, a product of
higher-rank symmetric cones cannot globally integrate a sharp local Peirce
budget.  Local channel capacity and globally realizable capacity are
different invariants.

The exceptional \(\mathbb S_+^3\) case in (8) is a necessary topological
possibility, not a construction claim for a ball slack factorization.

## From mixed slack to the support differential

Fix \(x\in P\), and let \(z\in D\) be its unique contact point, so
\(\langle x,z\rangle=1\).  Strict convexity and \(C^1\) smoothness make this
contact correspondence a homeomorphism between \(P\) and \(D\).  In
independent local charts, mixed differentiation of (1) gives the
nondegenerate tangent pairing

\[
 \langle u,v\rangle
   =\sum_i H_i(u,v),\qquad
 H_i(u,v)=-\langle dX_i(x)u,dY_i(z)v\rangle_i.             \tag{9}
\]

Indeed, \(T_xP=z^\perp\), \(T_zD=x^\perp\), and the Euclidean pairing
between these two \(n\)-planes has zero kernel because
\(\langle x,z\rangle=1\).

Let \(p=\operatorname{rank}X_i(x)\) and
\(q=\operatorname{rank}Y_i(z)\).  Positivity and zero pairing imply Jordan
complementarity, and the Peirce tangent calculation gives

\[
       \operatorname{rank}H_i\leq apq
       \leq a\left\lfloor{r^2\over4}\right\rfloor=c_i.     \tag{10}
\]

If \(\sum_i c_i=n\), rank subadditivity in (9) forces equality in every
inequality in (10), at every contact.  Hence \(p+q=r\), the two ranks are
balanced, and \(\operatorname{rank}H_i=c_i\).  Along the contact graph the
ranks are locally constant.  To see this without assuming it, Jordan rank
is lower semicontinuous on the cone.  Both \(p\) and \(q\) are therefore
lower semicontinuous, while \(p+q=r\); neither can change locally.  The
connected contact graph fixes one choice of \(p_i\) globally.

For a positive element \(X\) of constant rank \(p\), its support idempotent
\(e\) is a \(C^1\) function of \(X\).  Locally the zero eigenvalue cluster is
separated from the positive eigenvalues, so this follows directly from
Euclidean-Jordan spectral functional calculus with a smooth scalar cutoff.
Equivalently, it follows from the constant-rank implicit equations

\[
                             e^2=e,\qquad X\circ e=X.       \tag{11}
\]

Differentiate (11).  The idempotent equation puts
\(de\in V(e,1/2)\).  Write the derivative of \(X\) in the orthogonal Peirce
decomposition

\[
 V=V(e,1)\oplus V(e,{1\over2})\oplus V(e,0),
 \qquad dX=A+B+0.                                          \tag{12}
\]

The \(V(e,0)\) compression vanishes because a two-sided curve in the cone
has zero derivative in the kernel Peirce algebra.  Taking the
\(V(e,1/2)\) component of the derivative of \(X\circ e=X\) yields

\[
                        L_X(de)={1\over2}B.                 \tag{13}
\]

The map \(L_X\) is invertible on \(V(e,1/2)\).  In a Jordan frame with
\(X=\sum_{j\leq p}\lambda_jc_j\), \(\lambda_j>0\), it acts by
\(\lambda_j/2\) on every cross-Peirce space \(V_{j\ell}\),
\(j\leq p<\ell\).  Consequently

\[
                  d\sigma_i(x)u=0
        \quad\Longleftrightarrow\quad
 \operatorname{proj}_{V(e,1/2)}dX_i(x)u=0.                \tag{14}
\]

Only the primal and dual cross-Peirce components pair in (9).  Thus

\[
                  \operatorname{rank}H_i
                    \leq\operatorname{rank}d\sigma_i(x)
                    \leq\dim V(e,{1\over2})=apq.           \tag{15}
\]

Saturation makes all inequalities equalities, proving that each (5) is a
submersion.  Notice that neither matrix coordinates nor a differentiable
Gauss map were used.

## Why the joint map is a covering

If \(d\Sigma(x)u=0\), equation (14) kills the primal cross-Peirce component
in every block.  Therefore \(H_i(u,v)=0\) for all \(i\) and every
\(v\in T_zD\).  Nondegeneracy of the sum in (9) gives \(u=0\).  Since

\[
 \dim P=n=\sum_i c_i
          =\dim\prod_{i:c_i>0}\mathcal I_{p_i}(V_i),       \tag{16}
\]

\(d\Sigma\) is an isomorphism everywhere.  A local diffeomorphism from the
compact connected manifold \(P\) has open and closed image and is proper;
hence (7) is a finite covering of the connected target.

For \(n\geq2\), \(S^n\) is simply connected and is therefore the universal
cover of the target.  A target with an \(S^1\) factor is impossible because
its universal cover is noncompact.  All remaining simple-EJA idempotent
orbits have compact simply connected universal covers.  Lifting (7) gives

\[
 S^n\cong\prod_{i:c_i>0}\widetilde{\mathcal I}_{p_i}(V_i). \tag{17}
\]

There can be only one positive-dimensional factor: with two or more, the
mod-two top class of one factor, tensored with unit classes on the others,
would give nonzero cohomology in a degree strictly between \(0\) and \(n\).
For \(n=1\), dimension alone leaves one \(S^1\) orbit.

## Classification of the sole support orbit

The finite-dimensional simple Euclidean Jordan algebras give the following
complete list.  Here \(p+q=r\) is balanced.

| simple EJA | support-idempotent orbit | real dimension | when its universal cover is a sphere |
|---|---|---:|---|
| spin factor of dimension \(m\geq3\) | \(S^{m-2}\) | \(m-2\) | always |
| \(H_r(\mathbb R)\), \(r\geq3\) | \(\operatorname{Gr}_p(\mathbb R^r)\) | \(pq\) | \(r=3\), with universal cover \(S^2\to\mathbb {RP}^2\) |
| \(H_r(\mathbb C)\), \(r\geq3\) | \(\operatorname{Gr}_p(\mathbb C^r)\) | \(2pq\) | never |
| \(H_r(\mathbb H)\), \(r\geq3\) | \(\operatorname{Gr}_p(\mathbb H^r)\) | \(4pq\) | never |
| \(H_3(\mathbb O)\) | \(\mathbb OP^2=F_4/\operatorname{Spin}(9)\) | \(16\) | never |

The order-two real, complex, and quaternionic Hermitian algebras are spin
factors and belong in the first row.  Likewise, the formal
\(H_2(\mathbb O)\) projective-line case is the spin factor \(Q_{10}\), not
an additional exceptional simple algebra.

For \(H_r(\mathbb R)\), the universal cover is the oriented Grassmannian.
At \(r=3\), the balanced orbit is \(\mathbb {RP}^2\), covered by \(S^2\).
For \(r\geq4\), balanced \(p,q\geq2\); the homotopy sequence of

\[
 SO(p)\times SO(q)\longrightarrow SO(p+q)
       \longrightarrow\operatorname{Gr}_p^+(\mathbb R^{p+q})
\]

gives nonzero \(\pi_2\).  If \(p,q\geq3\), the kernel of
\(\mathbb Z_2\oplus\mathbb Z_2\to\mathbb Z_2\) contains the diagonal
element.  If one rank is two, the kernel contains the nonzero even elements
of \(\pi_1(SO(2))=\mathbb Z\).  This excludes a sphere of dimension
\(pq\geq4\).

For complex Grassmannians of order at least three,
\(H^2(-;\mathbb Z)\cong\mathbb Z\), while their real dimension is at least
four.  For quaternionic Grassmannians of order at least three,
\(H^4(-;\mathbb Z)\cong\mathbb Z\), while their real dimension is at least
eight.  Finally, \(\mathbb OP^2\) has nonzero middle cohomology
\(H^8(\mathbb OP^2;\mathbb Z)\cong\mathbb Z\).  None is a sphere.  These
observations prove (8).

## The \(H_3(\mathbb R)\) exception needs at least three rays

The sole non-spin possibility in (8) is already strictly dominated in all
three usual resource ledgers.  Suppose \(n=2\), the unique
positive-capacity factor is \(H_3(\mathbb R)_+\), and write the remaining
ray summands as

\[
                         a_j(x)b_j(z),\qquad a_j,b_j\geq0. \tag{17a}
\]

The support map \(\sigma:S^2\to\mathbb {RP}^2\) is the universal double
cover.  Let \(\tau\) be its nontrivial deck involution and let
\(\gamma:P\to D\) be contact polarity.  At the cross pair
\((\tau x,\gamma(x))\), the \(H_3(\mathbb R)\) term is zero: \(X(\tau x)\)
and \(X(x)\) have the same support idempotent, while
\(Y(\gamma(x))\) lies in its complementary face.  Strict convexity and
\(\tau x\neq x\) give

\[
                 1-\langle\tau x,\gamma(x)\rangle>0.       \tag{17b}
\]

Put \(\beta_j(x)=b_j(\gamma(x))\) and

\[
 U_j=\{x\in S^2:\beta_j(x)>0,\ a_j(\tau x)>0\}.            \tag{17c}
\]

Equations (17a)--(17b) show that the open sets \(U_j\) cover \(S^2\).
They are antipodal-free with respect to \(\tau\).  Indeed, diagonal slack
zero gives \(a_j(x)\beta_j(x)=0\); if both \(x\in U_j\) and
\(\tau x\in U_j\), the first membership gives \(\beta_j(x)>0\), hence
\(a_j(x)=0\), while the second gives \(a_j(x)>0\), a contradiction.

Equivalently, \(U_j\cup\tau U_j\) descends to an open subset of
\(\mathbb {RP}^2\) on which the double cover has a section.  The Schwarz
genus of \(S^2\to\mathbb {RP}^2\) is three: if
\(\alpha\in H^1(\mathbb {RP}^2;\mathbb F_2)\) classifies the cover, then
\(\alpha^2\neq0\), so the standard cup-length lower bound requires at least
three section domains.  Therefore at least three ray blocks are active.
Every \(H_3(\mathbb R)\) saturation has the resource floor

\[
                       (k,M,\nu)\geq(4,9,6),               \tag{17d}
\]

whereas the spin factor \(Q_4\) has \((k,M,\nu)=(1,4,2)\).

In particular, the \(H_3(\mathbb R)\) exception is impossible if every ray
slack summand vanishes.  It is also impossible when the factor maps and
contact polarity are real analytic: on the connected analytic contact
sphere, \(a_j(x)b_j(\gamma(x))\equiv0\) forces one analytic factor to vanish
identically, so every ray summand vanishes on all of \(P\times D\).  This
analytic exclusion is not asserted for merely \(C^1\) factors.

For the round three-ball, a stronger companion theorem now removes this
exception even with arbitrary finitely many \(C^1\) ray factors.  Finite ray
status patterns force the rank-two PSD sheet to be a finite \(C^1\)
selection of affine pencils; a first-jet gluing lemma makes it one global
pencil.  Its determinant would be a timelike linear form times the sphere
quadric, leading to an impossible real symmetric \(3\times3\) Clifford
pencil.  The full proof, including the local stereographic pencil showing
why globalization is essential, is in
[The apparent \(\mathbb S_+^3\) saturation exception is
impossible](2026-09-04-psd3-saturation-exclusion.md).  That algebraic
argument is ball-specific and is not asserted for a general \(C^1\)
strictly convex three-body.

Combining the companion with (8) gives the dimension-uniform ball
classification

\[
 \boxed{\text{For }B_2^N,\ \sum_i c_i=N-1
 \ \Longrightarrow\ \text{the unique positive block is }Q_{N+1}.}     \tag{17d'}
\]

Finite ray factors may remain, but they have zero curvature capacity and
cannot replace or split the Lorentz block.

## Rigidity of the dimension-minus-barrier ledger

For a simple factor of dimension \(m\), rank \(r\), and Peirce constant
\(a\),

\[
 m-r={a\over2}r(r-1),\qquad
 c=a\left\lfloor{r^2\over4}\right\rfloor\leq m-r.         \tag{17e}
\]

Equality in (17e) holds for a positive-capacity factor exactly when
\(r=2\), that is, when the factor is a spin factor.  Since the local theorem
gives \(n\leq\sum_i c_i\leq\sum_i(m_i-r_i)=M-\nu\), equality
\(M-\nu=n=N-1\) forces every positive factor to be a spin factor and also
forces capacity saturation.  The covering theorem then leaves one positive
factor, necessarily \(Q_{N+1}\).  Conversely, this direct Lorentz factor
attains equality.  Rank-one ray factors may be appended because they add
one to both \(M\) and \(\nu\).

Therefore the complete dichotomy is

\[
 \boxed{
 \begin{array}{ll}
 M-\nu=N-1,
   &\text{one positive block }Q_{N+1}\text{, plus possible rays},\\[1mm]
 M-\nu\geq N,
   &\text{every other globally bi-}C^1\text{ symmetric-cone factorization}.
 \end{array}}                                             \tag{17f}
\]

At \(N=3\), the \(H_3(\mathbb R)\) topological exception lies in the second
line already, since its own \(m-r\) is three.

## Sharp block-cap frontier for the Euclidean ball

Let \(N=n+1\geq2\), and suppose every positive-capacity irreducible
symmetric-cone factor has real ambient dimension at most \(d\).
For every such factor of dimension \(m_i\) and Jordan rank \(r_i\geq2\),

\[
        c_i\leq m_i-r_i\leq m_i-2\leq d-2.                \tag{18}
\]

If \(3\leq d<N+1\), saturation \(\sum_i c_i=N-1\) is impossible by (8):
the required spin factor has dimension \(N+1\); at \(N=3\), the only extra
\(\mathbb S_+^3\) possibility has dimension six and also violates the cap.
Therefore integrality gives

\[
                              \sum_i c_i\geq N.             \tag{19}
\]

Let \(k_+\) count positive-capacity factors, \(M=\sum_i m_i\), and let
\(\nu=\sum_i r_i\) be the optimal ambient normal-barrier parameter of the
symmetric-cone product.  Equations (18)--(19) imply

\[
 \boxed{
 \begin{aligned}
 k_+&\geq\left\lceil{N\over d-2}\right\rceil,\\
 M&\geq N+2\left\lceil{N\over d-2}\right\rceil,\\
 \nu&\geq2\left\lceil{N\over d-2}\right\rceil.
 \end{aligned}}                                           \tag{20}
\]

All three bounds are attained simultaneously.  Partition the \(N\)
coordinates into groups \(G\) of size at most \(d-2\) and use one Lorentz
factor \(Q_{|G|+2}\) per group.  The polynomial factors

\[
 A_G(x)=\left({1+\|x_G\|^2\over2},
              {1-\|x_G\|^2\over2},x_G\right),\qquad
 B_G(z)=\left({1+\|z_G\|^2\over2},
             -{1-\|z_G\|^2\over2},-z_G\right)             \tag{21}
\]

satisfy

\[
 \langle A_G(x),B_G(z)\rangle={1\over2}\|x_G-z_G\|^2,
 \qquad \sum_G\langle A_G(x),B_G(z)\rangle=1-\langle x,z\rangle. \tag{22}
\]

Equivalently, the affine lift uses variables \(s_G\) and constraints

\[
 \left({1+s_G\over2},{1-s_G\over2},x_G\right)\in Q_{|G|+2},
 \qquad \sum_Gs_G=1.                                      \tag{23}
\]

The cone constraints say \(s_G\geq\|x_G\|^2\), so the projection is
exactly \(B_2^N\), the lift is strictly feasible over every interior point,
and the boundary fiber is unique.  Thus its factor sheets are globally
\(C^1\), as required.

If \(d\geq N+1\), one direct \(Q_{N+1}\) factor instead gives

\[
                           (k_+,M,\nu)=(1,N+1,2).           \tag{24}
\]

Hence (20) and (24) are the exact all-cap frontier within the global
bi-\(C^1\) symmetric-cone factorization class.  Ray factors have zero
capacity; total factor count is at least \(k_+\), and the optima use no ray
factors.  The normal-barrier ledger concerns the chosen ambient product and
does not by itself imply an iteration lower bound for an IPM or QIPM.

## Scope and relation to exact lifts

The theorem assumes globally labelled \(C^1\) primal and dual factor
selections on the entire paired boundaries.  A semialgebraic affine lift
supplies simultaneous \(C^1\) selections on a dense open contact stratum,
which is enough for the local inequality (3), but not automatically on the
whole sphere.  Thus (19)--(20) are a strict regularity-class frontier, not
an unconditional lower bound for every exact symmetric-cone lift.

The local theorem, including arbitrary affine slices, projections, free
variables, minimal-face reduction, and non-strict complementarity, is proved
in [Curvature capacity of symmetric-cone lifts](2026-09-04-symmetric-cone-curvature-capacity.md).
The matrix special cases and their exact low-order constructions are in
[Saturated PSD factors induce Grassmannian submersions](2026-09-04-psd-support-grassmannian-submersion.md).
The ball-specific elimination of the remaining real order-three case is in
[The apparent \(\mathbb S_+^3\) saturation exception is
impossible](2026-09-04-psd3-saturation-exclusion.md).
The universal cone-base version is in
[Sphere submersion curvature gap](2026-09-04-sphere-submersion-curvature-gap.md).
The resulting exact parameter lower bound for the standard product Jordan
barrier after affine restriction is in
[Exact standard-slice barrier frontier](2026-09-04-symmetric-cone-standard-slice-barrier-frontier.md).

## Literature boundary

[Faraut and Korányi, *Analysis on Symmetric
Cones*](https://doi.org/10.1093/oso/9780198534778.001.0001), especially
Chapters III--V, is the primary reference for the spectral theorem, Peirce
decomposition, automorphism orbits of idempotents, dimension formula, and
classification of simple Euclidean Jordan algebras.  Nomura's
[Grassmann manifold of a JH-algebra](https://doi.org/10.1007/BF02099191)
identifies the tangent space of a fixed-rank idempotent manifold with its
Peirce-\(1/2\) space and develops its homogeneous Riemannian geometry.
[Baes, *Spectral functions and smoothing techniques on Jordan
algebras*](https://doi.org/10.1016/j.laa.2006.11.025) supplies a modern
spectral-calculus reference supporting the separated-cluster \(C^1\)
support map used above.
[Schwarz, *The genus of a fiber
space*](https://www.mathnet.ru/eng/mmo120) supplies the sectional-genus
cup-length obstruction used in (17a)--(17d).

The classical descriptions of the matrix idempotent orbits as real,
complex, and quaternionic Grassmannians are reviewed, with a separate
topological audit, in the PSD companion above.  The exceptional orbit is
\(F_4/\operatorname{Spin}(9)=\mathbb OP^2\); its middle cohomology is part
of the standard three-cell description of the Cayley projective plane.

A targeted search for differential slack factorizations together with
idempotent manifolds, Peirce support maps, or Grassmannian/projective-plane
covering obstructions found no source stating the joint covering theorem,
the classification (8), or the strict globally regular budget (19).
Priority therefore remains subject to specialist review.

## Audit checklist

- Verify that support idempotents vary \(C^1\) on a constant-Jordan-rank
  \(C^1\) cone-valued family, including the exceptional algebra.
- Check (13), especially the factor \(1/2\), and verify that
  \(L_X:V(e,1/2)\to V(e,1/2)\) is invertible.
- Verify that vanishing of every support differential kills every mixed
  Peirce channel and hence proves injectivity of the joint map.
- Check connectedness and universal covers of every balanced idempotent
  orbit, including \(H_3(\mathbb R)\) and \(H_3(\mathbb O)\).
- Check that the orbit table is exhaustive after removing low-rank
  matrix/spin-factor coincidences.
- Keep the \(\mathbb S_+^3\) case as a topological possibility only.
- Check the equality case in \(c\leq m-r\) and the dichotomy (17f).
- Distinguish the global bi-\(C^1\) theorem from the generic local
  regularity obtained from an arbitrary semialgebraic lift.

## Independent hostile audit

The auditor rederived the mixed Peirce rank bound and checked that saturation
forces balanced strict complementarity at every contact.  It verified the
lower-semicontinuity argument for global rank constancy, the
separated-cluster \(C^1\) support map, the factor \(2L_X\) in (13), and the
equality of the support differential's kernel with the cross-Peirce
derivative's kernel.  It then independently checked the joint local
diffeomorphism and covering argument.

The audit also exhausted the simple-EJA classification.  It verified the
spin-factor sphere, the \(H_3(\mathbb R)\) double-cover exception, the
nonzero \(\pi_2\) obstruction for all larger real balanced
Grassmannians, the intermediate \(H^2\) and \(H^4\) classes in the complex
and quaternionic cases, and the \(0,8,16\) cell dimensions of
\(\mathbb OP^2\).  It specifically checked the \(n=1\) circle case
separately and confirmed that the theorem does not assert global factor
regularity for an arbitrary affine lift.  No mathematical correction was
required.

A second hostile audit rechecked the whole theorem and the exact capped
frontier.  Both audits also verified the \(H_3(\mathbb R)\) refinement:
the cross-contact slack constructs an antipodal-free open cover, the
Schwarz-genus lower bound requires three active rays, and the analytic
zero-product principle removes the exception when all factor data and
contact polarity are analytic.
