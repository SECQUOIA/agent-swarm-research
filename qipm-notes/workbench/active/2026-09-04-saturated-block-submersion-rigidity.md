# Saturated cone blocks induce sphere submersions

Status: Proved; independently reconstructed and hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High under the stated bi-\(C^1\) factor-selection hypothesis; literature novelty not yet screened

Role: Independent reconstruction and hostile audit of the factor-to-submersion
bridge.  Its headline rigidity conclusion is subsumed by the canonical,
primary-source-screened note
[Sphere submersions force a strict curvature-capacity gap](2026-09-04-sphere-submersion-curvature-gap.md).
The details below are retained as a separate verification, especially the
proper-\(C^1\) fibration route and the independent primal/polar chart argument.

## Main result

Let \(C\subset\mathbb R^N\), \(N\geq2\), be a compact convex body with
\(0\in\operatorname{int}C\).  Assume that both

\[
                  M=\partial C,\qquad M^\circ=\partial C^\circ
\]

are compact embedded \(C^1\) hypersurfaces.  This is the natural
*bi-\(C^1\)* hypothesis: in convex-geometric terms it makes both \(C\) and
\(C^\circ\) smooth and strictly convex.  In particular,
\(M,M^\circ\simeq S^{N-1}\), but no positive curvature and no differentiable
Gauss/contact map are assumed.

Suppose the full primal--polar slack has a global \(C^1\) factorization

\[
  1-\langle x,y\rangle
    =\sum_{i=1}^k\langle A_i(x),B_i(y)\rangle,
 \qquad x\in M,\ y\in M^\circ,                         \tag{1}
\]

where \(A_i:M\to K_i\), \(B_i:M^\circ\to K_i^*\), and \(K_i\subset E_i\) is a
finite-dimensional proper cone of dimension \(m_i\).  For a fixed block put

\[
 H_i(x,y)(u,v)=-\langle dA_i(x)u,dB_i(y)v\rangle.
\]

Assume this block attains its universal mixed-rank capacity at every
contact pair \((x,y)\), \(\langle x,y\rangle=1\):

\[
              \operatorname{rank}H_i(x,y)=m_i-2=:r>0.           \tag{2}
\]

Choose any \(\ell_i\in\operatorname{int}K_i^*\), set

\[
 D_i=\{a\in K_i:\ell_i(a)=1\},\qquad
 p_i(x)=\frac{A_i(x)}{\ell_i(A_i(x))}.                          \tag{3}
\]

Then:

1. neither \(A_i(x)\) nor \(B_i(y)\) vanishes at a contact pair;
2. \(p_i(x)\in\partial D_i\), where \(D_i\) is a compact
   \((m_i-1)\)-dimensional convex body and
   \(\partial D_i\) is topologically \(S^r\);
3. \(dp_i(x)\) has rank exactly \(r\) at every \(x\);
4. although no regularity of \(\partial K_i\) was assumed, surjectivity and
   constant rank force \(\partial D_i\) to be a \(C^1\) embedded
   hypersurface; and
5. \(p_i:M\to\partial D_i\simeq S^r\) is a proper surjective \(C^1\)
   submersion.

Thus every positive-capacity block in a globally smooth saturated cone
factorization produces a genuine sphere submersion

\[
                            S^{N-1}\longrightarrow S^{m_i-2}.   \tag{4}
\]

The \(C^1\) proper-submersion theorem of Earle and Eells gives a locally
trivial \(C^0\) fibration, which is all the later homotopy argument needs.
Thus \(C^2\) regularity is unnecessary throughout.

## Differential proof

Fix a contact pair \(x\in M\), \(y\in M^\circ\) with
\(\langle x,y\rangle=1\), and abbreviate \(A=A_i(x)\), \(B=B_i(y)\).
Cone duality and (1) give

\[
 \langle A_i(x'),B_i(y')\rangle\geq0,
 \qquad \langle A_i(x),B_i(y)\rangle=0.                        \tag{5}
\]

Holding either variable fixed and differentiating its nonnegative scalar
function at the diagonal minimum gives, separately,

\[
       \langle dA_i(x)u,B\rangle=0,
       \qquad
       \langle A,dB_i(y)v\rangle=0                             \tag{6}
\]

for all \(u\in T_xM\), \(v\in T_yM^\circ\).  These separate identities are
important: no differentiability of the contact correspondence is being
used.

If \(A=0\), two-sided differentiability of a map into the pointed cone
\(K_i\) gives \(dA_i(x)u\in K_i\cap(-K_i)=\{0\}\) for every \(u\).
Thus \(H_i(x,y)=0\), contrary to (2).  The same argument applies if \(B=0\).
Hence both are nonzero.  A nonzero dual-cone vector pairs strictly
positively with every point of \(\operatorname{int}K_i\), so (5) places
\(A\) on \(\partial K_i\).  Since \(\ell_i\) is strictly positive on
\(K_i\setminus\{0\}\), (3) is well-defined and lies on \(\partial D_i\).

Write \(A_i=\alpha_i p_i\), with \(\alpha_i=\ell_i(A_i)>0\).  From (6),
\(\langle p_i,dB_i(y)v\rangle=0\), and therefore

\[
 \begin{aligned}
 H_i(x,y)(u,v)
  &=-\langle d\alpha_i(u)p_i+\alpha_i\,dp_i(u),dB_i(y)v\rangle\\
  &=-\alpha_i\langle dp_i(u),dB_i(y)v\rangle.                 \tag{7}
 \end{aligned}
\]

Consequently

\[
                    \operatorname{rank}H_i(x,y)
                    \leq\operatorname{rank}dp_i(x).            \tag{8}
\]

The affine hull of \(D_i\) has dimension \(m_i-1=r+1\).  If \(dp_i(x)\)
had rank \(r+1\), the submersion theorem, applied with this affine hull as
target, would make the image of \(p_i\) contain a relatively open
\((r+1)\)-dimensional set.  This is impossible because the entire image lies
in \(\partial D_i\), which has empty interior in that affine hull.  Hence
\(\operatorname{rank}dp_i\leq r\).  Combining this with (2) and (8) proves

\[
                         \operatorname{rank}dp_i=r.             \tag{9}
\]

This argument uses no smoothness, strict convexity, symmetry, homogeneity,
or self-duality of the lifting cone.

## Why a nonsmooth cone boundary does not create a loophole

The boundary of every compact convex body with nonempty interior in
\(\mathbb R^{r+1}\) is homeomorphic to \(S^r\), by radial projection from an
interior point.  At \(x\in M\), the constant-rank theorem supplies an
\(r\)-dimensional local transversal \(\Sigma\) on which \(p_i|_\Sigma\) is a
\(C^1\) embedding.  Compose this embedding with any homeomorphism
\(\partial D_i\simeq S^r\).  Invariance of domain says that
\(p_i(\Sigma)\) is relatively open in \(\partial D_i\).

It follows that \(p_i(M)\) is open in \(\partial D_i\).  It is also compact,
hence closed.  Since \(r>0\) makes \(\partial D_i\simeq S^r\) connected,

\[
                              p_i(M)=\partial D_i.               \tag{10}
\]

Moreover, each point of \(\partial D_i\) has a relative neighborhood equal
to one of the embedded \(C^1\) transversal images.  These charts are
compatible with the unique embedded-submanifold structure inherited from
the ambient affine hyperplane.  Thus \(\partial D_i\) is itself a \(C^1\)
embedded hypersurface, and (9) says exactly that \(p_i\) is a submersion
onto it.  Radial projection from an interior point of \(D_i\) is then a
\(C^1\) diffeomorphism \(\partial D_i\to S^r\): its differential has radial
kernel, while the radial direction is transverse to the boundary.
In particular, a polyhedral cone of dimension at least three
cannot be an everywhere capacity-saturating block in such a factorization:
the conclusion would incorrectly force the boundary of its polytope base
to be smooth.

## Dimension obstruction for a proper sphere submersion

Let \(p:S^n\to S^r\) be a \(C^1\) submersion with \(0<r<n\).  Properness is
automatic.  A proper \(C^1\) submersion is a locally trivial \(C^0\) bundle
by the finite-dimensional specialization of Earle--Eells, with closed
fiber \(F^f\), \(f=n-r>0\).  This avoids appealing to a \(C^1\)-smoothing
argument.  The more familiar \(C^2\) Ehresmann theorem gives the same
conclusion.

If \(r=1\) and \(n\geq2\), simple connectivity lifts \(p\) through
\(\mathbb R\to S^1\).  The lifted real function has a maximum on \(S^n\),
where its derivative, and hence \(dp\), vanishes.  Thus \(r=1\) is
impossible.

Suppose \(r\geq2\).  The homotopy exact sequence and the simple connectivity
of \(S^r\) first show that \(F\) is connected.  For
\(1\leq j\leq r-2\),

\[
             \pi_{j+1}(S^r)=0,\qquad \pi_j(S^n)=0,
\]

so exactness gives \(\pi_j(F)=0\).  Hence \(F\) is
\((r-2)\)-connected.  If \(f\leq r-2\), Hurewicz would give
\(H_f(F;\mathbb Z_2)=0\), contradicting the mod-two fundamental class of
the closed connected \(f\)-manifold \(F\).  Therefore

\[
                  f\geq r-1,\qquad
                  \boxed{r\leq\frac{n+1}{2}}.                  \tag{11}
\]

The inequality cannot be improved using this elementary argument alone: the classical
Hopf fibrations \(S^3\to S^2\), \(S^7\to S^4\), and
\(S^{15}\to S^8\) attain equality.  They are topological counterexamples to
any blanket claim that a proper-rank saturated block is impossible.  No
claim is made here that all or any of these Hopf maps can occur as one
block of a cone slack factorization.

Combining (4) and (11), every capacity-saturating block of rank \(r<n\) in
the cone factorization satisfies

\[
                 r\neq1,\qquad r\leq\frac{n+1}{2},
                 \qquad n=N-1.                                 \tag{12}
\]

There is a much sharper classical classification.  Browder's fiber theorem
says that the connected fiber of a bundle whose total space is a sphere has
the homotopy type of \(S^d\), with

\[
                              d\in\{1,3,7\}.
\]

Here the fiber is a closed manifold of geometric dimension \(f=n-r\).
Its mod-two top homology is nonzero, so homotopy equivalence to \(S^d\)
forces \(f=d\).  The Serre spectral sequence for

\[
                         S^d\simeq F\longrightarrow S^n
                                      \longrightarrow S^r
\]

has only four potentially nonzero groups.  The two intermediate generators
can cancel only through

\[
             d_r:E_r^{0,d}\longrightarrow E_r^{r,0},
\]

which forces \(r=d+1\).  Therefore a proper sphere submersion exists only
for

\[
                  \boxed{(n,r)\in\{(3,2),(7,4),(15,8)\}}.      \tag{12a}
\]

The Hopf maps show that all three dimension pairs occur.  This is a
classification of possible dimensions, not of bundles up to equivalence.

## Exact unsplitness in every dimension

Now assume the whole curvature budget is saturated:

\[
                   \sum_i(m_i-2)_+=n=N-1.                      \tag{13}
\]

Bi-\(C^1\) smoothness and strict convexity make the normalized contact
correspondence \(\gamma:M\to M^\circ\) a homeomorphism.  At a contact pair
\((x,\gamma(x))=(x,y)\), differentiability of the two boundaries gives

\[
                 T_xM=y^\perp,\qquad T_yM^\circ=x^\perp.
\]

The Euclidean pairing between these two \(n\)-planes is nondegenerate: if
\(u\in y^\perp\) annihilates \(x^\perp\), then
\(u\in\operatorname{span}\{x\}\), and \(\langle x,y\rangle=1\) forces
\(u=0\).  Mixed differentiation of (1), in independent primal and polar
charts, therefore gives

\[
             \sum_iH_i(x,y)(u,v)=\langle u,v\rangle             \tag{13a}
\]

of rank \(n\).  Rank subadditivity and (13) force every positive-capacity
block to satisfy (2) at every contact.  Notice that this proof neither
differentiates the contact map nor invokes a second fundamental form.

There is also still a genuine tangent-bundle splitting.  Regard each
\(H_i(x,\gamma(x))\) as a continuous bundle map

\[
 L_i:TM\longrightarrow\gamma^*T^*M^\circ,
 \qquad
 (L_iu)(v)=H_i(u,v).
\]

The sum \(L=\sum_iL_i\) is the nondegenerate pairing in (13a), hence a
bundle isomorphism.  Since
\(\sum_i\operatorname{rank}L_i=n\), the image bundles
\(\operatorname{im}L_i\) are in direct sum and fill
\(\gamma^*T^*M^\circ\).  Therefore

\[
             TM=\bigoplus_i E_i,\qquad
             E_i:=L^{-1}(\operatorname{im}L_i),\qquad
             \operatorname{rank}E_i=m_i-2.                    \tag{13b}
\]

This splitting is continuous, which is sufficient for the Steenrod
subset-sum theorem.  Unlike the positive-curvature construction, it need
not be orthogonal and does not identify \(E_i\) with the nonzero directions
of a positive-semidefinite form.  The stronger conclusion below does not
need the splitting.

Apply (12a) to every positive block.  If
\(n\notin\{3,7,15\}\), no proper positive rank \(0<r_i<n\) is possible, so
some block has rank \(n\).  If \(n=3,7,15\), every proper positive rank
allowed by (12a) is respectively \(2,4,8\).  A sum of copies of
\(2,4,8\) cannot equal respectively \(3,7,15\).  Hence in these dimensions
too there is a rank-\(n\) block.  It exhausts the saturated budget, proving:

\[
 \boxed{
 \begin{gathered}
 N\geq3,\\
\text{global bi-\(C^1\) factor selections and curvature saturation}
 \Longrightarrow
 \text{one unique positive block of rank \(N-1\)},\\
 m_*=N+1,\qquad m_i\leq2\ \ (i\neq *).
 \end{gathered}}                                               \tag{15}
\]

Thus (15) upgrades the earlier \(C^2\), positive-curvature
\(N-O(\log N)\) dominant-block bound to an exact bi-\(C^1\) unsplitness
theorem in every dimension.  The Hopf dimensions do not escape: their only
proper allowed target ranks \(2,4,8\) are even and cannot sum to the odd
source ranks \(3,7,15\).

If every positive-capacity block has dimension at most \(d<N+1\), (15)
rules out equality in the universal integer budget.  Therefore, for
\(N\geq3\),

\[
 S:=\sum_i(m_i-2)_+\geq N,
 \quad
 k_+\geq\left\lceil\frac{N}{d-2}\right\rceil,
 \quad
 M_+\geq N+2\left\lceil\frac{N}{d-2}\right\rceil,             \tag{16}
\]

and every logarithmically homogeneous self-concordant barrier on the
ambient product has

\[
                    \nu\geq2\left\lceil\frac{N}{d-2}\right\rceil. \tag{17}
\]

For three-dimensional blocks this gives the exact smooth count \(k\geq N\)
for all \(N\geq3\), recovering the rank-one phase obstruction as a special
case.

## Escape routes and counterexample audit

- The standard Lorentz norm tree saturates the local count but its natural
  contact selections lose smoothness or hit the cone vertex when a child
  group vanishes.  This is exactly an excluded hypothesis, not a
  counterexample.
- The globally smooth \(Q_3^N\) coordinate-square construction has one
  excess block.  Its individual rank-one channels vanish at coordinate
  poles, so no block satisfies the everywhere-saturation hypothesis.
- Corners of an arbitrary cone base do not defeat the proof: constant rank,
  invariance of domain, compactness, and connectedness force the ray map to
  reach every corner, which is incompatible with constant rank there.
- The Hopf fibrations demonstrate that (11) is sharp for one smooth map,
  but Browder's dimension list and the saturated-sum arithmetic exclude a
  product profile made only of proper-rank blocks.

## Relation to the earlier topology theorem

The earlier global saturation theorem uses the positive mixed-curvature
forms to split \(TS^n\) into subbundles.  The present result uses information
that the abstract splitting forgets: every block integrates to a normalized
primal ray map onto the entire cone-base boundary.  Browder's theorem then
turns those submersions into the exact full-block conclusion (15).

## Regularity audit and \(B_p^N\)

The sphere-submersion theorem itself requires only:

1. \(M\) and \(M^\circ\) are embedded \(C^1\) hypersurfaces, so their
   independent tangent spaces exist;
2. \(A_i\) and \(B_i\) are globally \(C^1\); and
3. the block mixed rank equals \(m_i-2>0\) at each contact.

Strict positive curvature, \(C^2\) boundaries, and a differentiable Gauss
map are not needed.  Properness follows from compactness.  The fibers of a
\(C^1\) submersion form a \(C^1\) foliation, so the proper-\(C^1\)
fibration theorem applies and supplies the homotopy exact sequence used
above.

For every \(1<p<\infty\), both \(\partial B_p^N\) and
\(\partial(B_p^N)^\circ=\partial B_q^N\), \(q=p/(p-1)\), are embedded
\(C^1\), strictly convex hypersurfaces.  Therefore the sphere-submersion
theorem applies to global \(C^1\) slack factors for every such \(p\),
including the ranges \(1<p<2\) and \(2<p<\infty\) where one side need not
have everywhere nondegenerate \(C^2\) curvature.

For the low-regularity fibration statement, see C. J. Earle and J. Eells,
Jr., [“Foliations and fibrations,” *Journal of Differential Geometry* 1
(1967), 33--41](https://doi.org/10.4310/jdg/1214427879), especially their
proper \(C^1\) foliation criterion.  It yields \(C^0\) local triviality,
which is sufficient here.

For the fiber classification, see W. Browder,
[*“Fiberings of spheres and \(H\)-spaces which are rational homology
spheres,”* Bulletin of the AMS 68 (1962), 202--203](https://doi.org/10.1090/S0002-9904-1962-10747-2).
Its Theorem 1 gives the fiber homotopy types \(S^1,S^3,S^7\); the short
Serre-spectral-sequence argument above determines the corresponding sphere
target dimensions.
