# A lift-level topological penalty for contact-regular sparse cone lifts

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the covering-space reduction and count theorem

## Result

The topological obstruction in
[the smooth-factor note](2026-09-04-global-smooth-saturation-topology.md)
can be imposed directly on a cone lift, without assuming in advance that
some unspecified slack-factor selections are globally smooth.

Let \(C\subset\mathbb R^N\), \(N\geq3\), be a compact full-dimensional
convex body, contain the origin in its interior, and have \(C^3\), strictly
positively curved boundary. Consider a proper exact lift

\[
 C=\{Pz:z\in K,\ Ez=b\},\qquad
 K=K_1\times\cdots\times K_k,                         \tag{1}
\]

where every \(K_i\) is a finite-dimensional proper cone and the affine
slice meets \(\operatorname{int}K\).  Put \(M=\partial C\) and
\(M^\circ=\partial C^\circ\).  Define the primal and dual contact
incidences

\[
 \begin{aligned}
 \mathcal P&=\{(x,z)\in M\times K:Ez=b,\ Pz=x\},\\
 \mathcal D&=\{(y,\lambda)\in M^\circ\times\mathbb R^{\dim b}:
 b^T\lambda=1,\ E^T\lambda-P^Ty\in K^*\}.
 \end{aligned}                                                   \tag{2}
\]

Slater's condition and boundedness of the support problem ensure that every
dual contact has at least one certificate in \(\mathcal D\).

Call (1) **bi-contact-regular** if each incidence in (2) contains a
nonempty connected embedded \(C^2\) submanifold, called a contact sheet,
whose projection to \(M\), respectively \(M^\circ\), is a proper local
\(C^2\) diffeomorphism. The sheet need not be a connected component of the
whole incidence; this permits a smooth canonical selection inside a
positive-dimensional fiber. This is a condition on the contact geometry
of the lift and its conic dual certificates.

Write \(m_i=\dim K_i\).  The strongest conclusion is exact unsplitness in
every dimension: if a bi-contact-regular lift saturates the universal
curvature budget,

\[
                   \sum_i(m_i-2)_+=N-1,                          \tag{3}
\]

then exactly one block has positive capacity; it has capacity \(N-1\) and
cone dimension \(N+1\).  This is the lift-level consequence of the
independently audited canonical
[sphere-submersion theorem](2026-09-04-sphere-submersion-curvature-gap.md).

For comparison, a weaker conclusion that uses only the induced tangent
splitting is that, if \(q\) factors are three-dimensional, then

\[
                         \boxed{q\leq\rho(N)-1},                 \tag{4}
\]

where \(\rho\) is the Radon--Hurwitz function: if
\(N=(2a+1)2^{4c+d}\) with \(0\leq d\leq3\), then
\(\rho(N)=8c+2^d\). Thus this is the same Adams obstruction as for a
prescribed globally smooth factorization, but now its hypotheses can be
checked from the lift incidence itself.

The independently audited Steenrod--Dibag plane-field obstruction is much
stronger for general block ranks.  Put
\(n=N-1\) and \(s=\rho(N)-1\).  If \(s<n/3\), every saturated
bi-contact-regular lift has a unique dominant curvature block with rank at
least \(n-s\).  Therefore its cone dimension satisfies

\[
                         \boxed{m_*\geq N+2-\rho(N).}             \tag{5}
\]

The inequality \(s<n/3\) holds for every \(N\geq3\) except
\(N\in\{4,8,16\}\).  Hence, in all those dimensions, a block cap
\[
                         d<N+2-\rho(N)
\]
rules out saturation.  Integrality then strengthens the universal budget by
one unit:

\[
 S:=\sum_i(m_i-2)_+\geq N.                                      \tag{6}
\]

If \(k_+\) is the number of positive-capacity blocks and \(M_+\) their
total dimension, this gives, for every logarithmically homogeneous
self-concordant barrier of parameter \(\nu\) on the ambient product,

\[
 \boxed{
 k_+\geq\left\lceil\frac{N}{d-2}\right\rceil,\qquad
 M_+\geq N+2\left\lceil\frac{N}{d-2}\right\rceil,\qquad
 \nu\geq2\left\lceil\frac{N}{d-2}\right\rceil .
 }                                                               \tag{7}
\]

Zero-capacity factors only increase ambient dimension and do not weaken the
barrier bound.  Relative to the unrestricted curvature result, (6) is a
genuine lift-level regularity penalty for every
\[
 N\geq3,\qquad N\notin\{4,8,16\},\qquad d<N+2-\rho(N).
\]

For odd \(N\), \(\rho(N)=1\), so the conclusion is sharper in form: every
saturated bi-contact-regular lift has exactly one positive-capacity block,
that block has dimension \(N+1\), and all other blocks have dimension at
most two.  Thus the earlier odd-dimensional cap threshold \(d<N+1\) is the
special case of (5).

For arbitrary products of three-dimensional proper cones, the independently
audited
[saturated-factor submersion theorem](2026-09-04-saturated-factor-submersion-obstruction.md)
closes the parallelizable-sphere exceptions left by the abstract
tangent-bundle count.  For every \(N\geq3\),

\[
                              k\geq N.                          \tag{8}
\]

No strict convexity, boundary smoothness, or dual smoothness of the cone
factors is needed.  For Lorentz factors
\[
 Q_3=\{(u,v,w):u\geq\sqrt{v^2+w^2}\},
\]
an explicit
bi-contact-regular \(Q_3^N\)-lift exists.  Hence the simultaneous optima
within this regular Lorentz-product class are

\[
                 \boxed{k_{\min}=N,\qquad M_{\min}=3N,\qquad
                        \nu_{\min}=2N.}                          \tag{9}
\]

Here \(\nu\) is the parameter of a logarithmically homogeneous
self-concordant barrier on the ambient product, including a coupled one.
The standard product Lorentz barrier attains \(2N\).

Thus every \(N-1\)-block lift of \(B_2^N\) over arbitrary
three-dimensional proper cones, for every \(N\geq3\), must have a primal or
dual contact-incidence defect: no smooth compact sheet can project
nonsingularly over the whole contact sphere.  A singularity, ramification
point, nonproper escape, or failure to form a manifold is unavoidable on
at least one side.

The exact unsplitness conclusion after (3) removes every dimension and cap
exception from the earlier tangent-splitting bounds.  Therefore, for every
\(N\geq3\) and every cap \(3\leq d<N+1\), a bi-contact-regular lift satisfies

\[
 \sum_i(m_i-2)_+\geq N,\qquad
 k_+\geq\left\lceil{N\over d-2}\right\rceil,\qquad
 M_+\geq N+2\left\lceil{N\over d-2}\right\rceil.                \tag{9a}
\]

For Lorentz products, the grouped-coordinate construction in the
[smooth Lorentz factorization note](2026-09-04-smooth-q3n-ball-factorization.md)
attains these bounds and the matching full-ambient barrier value
\(2\lceil N/(d-2)\rceil\). Thus (9a), rather than the earlier
Radon--Hurwitz threshold, is the final sharp capped result under
bi-contact regularity.

## Proof

Set \(n=N-1\geq2\). For either selected contact sheet, a local
diffeomorphism has open image. A proper map from a manifold to a Hausdorff
manifold is closed, so its image is also closed. Since the base is
connected, the nonempty image is the whole base. A proper local
diffeomorphism is then a covering map.

The boundary of a strictly convex body is diffeomorphic to \(S^n\), as is
the polar boundary. Since \(S^n\) is simply connected for \(n\geq2\), every
connected covering of either boundary is one-sheeted. The two contact
sheets in the definition are therefore globally \(C^2\)-diffeomorphic
to their respective bases.

Invert the primal projection and write its second coordinate as \(A(x)\).
Invert the dual projection and write its second coordinate as
\(\lambda(y)\).  Define

\[
             B(y)=E^T\lambda(y)-P^Ty\in K^*.                    \tag{10}
\]

For every \(x\in M\) and \(y\in M^\circ\), equations (1), (2), and (10)
give

\[
 \langle A(x),B(y)\rangle
 =\langle EA(x),\lambda(y)\rangle-\langle PA(x),y\rangle
 =1-\langle x,y\rangle.                                        \tag{11}
\]

The \(C^3\) positive-curvature hypothesis makes
the normalized polar-contact map \(x\mapsto y(x)\) \(C^2\).  Consequently,
the block coordinates of \(A(x)\) and \(B(y(x))\) give globally \(C^2\)
primal and dual slack factors on the full contact manifold.

The saturated smooth-factor theorem now splits \(TM\) into the orthogonal
curvature subbundles contributed by the blocks.  Every three-dimensional
block contributes a line subbundle.  Real line bundles on \(S^n\),
\(n\geq2\), are trivial, so the \(q\) line summands supply \(q\) independent
tangent vector fields.  Adams's theorem gives (4).

For the dominant-block statement, let
\[
 TS^n=\bigoplus_iE_i,\qquad r_i=\operatorname{rank}E_i=(m_i-2)_+.
\]
Steenrod's plane-field theorem, in the form verified by Dibag, says that a
tangent subbundle of rank \(R\leq n/2\) forces \(R\) pointwise independent
tangent vector fields.  Applying this to the direct sum over any subset of
the \(E_i\)'s gives
\[
0<\sum_{i\in I}r_i\leq n/2
 \quad\Longrightarrow\quad
 \sum_{i\in I}r_i\leq s.                                      \tag{11a}
\]
If \(s<n/3\), a partial-sum argument forces a unique
\(r_*>n/2\): if every \(r_i\leq n/2\), the first partial sum exceeding
\(n/2\) is at most \(2s\), while its complementary rank is either zero or
at most \(s\), making that partial sum at least \(n-s\), a contradiction.
The large block is unique because the total rank is \(n\).  Its complement
has rank at most \(s\), so \(r_*\geq n-s\).  Saturation identifies
\(m_*=r_*+2\), proving
(5).  The Radon--Hurwitz arithmetic giving the three exceptions is recorded
and audited in
[the Steenrod companion note](2026-09-04-steenrod-effective-curvature-capacity.md).

For the odd-dimensional strengthening, \(n=N-1\) is even.  Suppose the
saturated splitting has at least two positive-rank summands, and group it
as

\[
                         TS^n=E\oplus F                         \tag{12}
\]

with \(0<\operatorname{rank}E,\operatorname{rank}F<n\).  Since \(S^n\) is
simply connected, both bundles are orientable.  Their Euler classes vanish
because

\[
 H^{\operatorname{rank}E}(S^n;\mathbb Z)
 =H^{\operatorname{rank}F}(S^n;\mathbb Z)=0.
\]

The Whitney product formula would then give
\(e(TS^n)=e(E)\smile e(F)=0\), contradicting
\(\langle e(TS^n),[S^n]\rangle=\chi(S^n)=2\).  Hence there is exactly one
positive-rank summand.  Saturation makes its rank \(n\), so the corresponding
block satisfies \(m_i-2=n\).  This is the \(\rho(N)=1\) specialization of
(5), with the additional explicit statement that every other block has
zero capacity.

More generally, suppose \(s<n/3\) and
\(d<N+2-\rho(N)\).  The dominant block required by (5) is forbidden.  The
universal theorem gives \(S\geq N-1\), equality is now impossible, and
\(S\) is integral; hence \(S\geq N\).  Since every positive block
contributes at most \(d-2\),
\(k_+\geq\lceil N/(d-2)\rceil\).  Finally,
\(M_+=S+2k_+\) and the coupled product-barrier bound is \(\nu\geq2k_+\),
which proves (7).

If all blocks are three-dimensional, the local curvature-capacity theorem
first gives \(k\geq n\).  At equality every mixed channel has rank one.
For an arbitrary proper three-dimensional cone, normalize the corresponding
primal factor into a compact planar cone base.  Its boundary is a
topological circle, even if it has corners.  Rank-one saturation makes the
normalized map have rank one everywhere; the constant-rank theorem and
one-dimensional invariance of domain make it locally open.  Since
\(n\geq2\), composing with a homeomorphism to \(S^1\) lifts to a continuous
real-valued locally open map on compact \(S^n\), which is impossible at a
maximum.  Thus equality is impossible and \(k\geq n+1=N\).  The
corresponding \(M\geq3N\) and \(\nu\geq2N\) bounds follow from \(m_i=3\)
and the general lower bound \(\nu(\prod_iK_i)\geq2k\).

The matching construction introduces
\(q_i=(u_i,v_i,w_i)\in Q_3\), imposes
\[
 u_i+v_i=1,\qquad \sum_i(u_i-v_i)=1,\qquad x_i=w_i,
\]
and projects exactly to \(B_2^N\).  On the boundary,
\(u_i-v_i=x_i^2\), so every primal boundary fiber is unique and polynomial.
The normalized dual multipliers
\[
 \lambda_i(y)=y_i^2/2,\qquad \lambda_0(y)=1/2
\]
form a global smooth dual contact sheet.  Thus the lift is
bi-contact-regular and attains (9).  Full details and the independent audit
are in
[the smooth \(Q_3^N\) ball note](2026-09-04-smooth-q3n-ball-factorization.md).

## Concrete sufficient conditions

The incidence definition is more structural than an assumed choice of
factors, but it is still a genuine regularity restriction.  Here are useful
ways to verify it.

1. **Unique nonsingular contact fibers.**  If every primal contact fiber is
   a singleton, \(\mathcal P\) is a \(C^2\) manifold, and the derivative of
   \(\mathcal P\to M\) is nonsingular everywhere, then this projection is a
   global \(C^2\) diffeomorphism.  The same statement for normalized dual
   certificates verifies the dual side.  Uniqueness alone is not enough.

2. **Finite nonsingular contact fibers.**  Singleton fibers can be replaced
   by a proper finite-sheeted nonsingular incidence.  Simple connectivity
   separates it into global sheets, and any connected sheet supplies the
   required factor choice.  Thus finite algebraic ambiguity is harmless;
   branching is the relevant obstruction.

3. **Smooth active-stratum KKT systems.**  For either fiber, one may select
   the unique minimizer of a coercive strongly convex objective such as
   squared Euclidean norm.  If, at every contact, the active cone strata
   have fixed \(C^3\) local descriptions, strict complementarity keeps that
   active set locally fixed, and the resulting classical KKT Jacobian is
   nonsingular, the implicit-function theorem gives a local
   \(C^2\) solution graph. If the unique selection exists at every contact,
   these local graphs agree on overlaps; their graph over the compact base
   is a proper global contact sheet. The same applies to a relative
   analytic-center
   selection when its active-face family is smooth and its KKT Jacobian is
   nonsingular.  Neither an analytic center nor strong convexity removes an
   active-stratum singularity by itself.

There is also a useful extreme sufficient condition on the primal side.  If
*every* fiber over all of \(C\), not just over \(\partial C\), is a
singleton, its inverse lift map is affine.  Indeed, if \(A(x)\) and \(A(x')\)
are the unique lifts, then

\[
       tA(x)+(1-t)A(x')
\]

is a lift of \(tx+(1-t)x'\); uniqueness forces it to equal
\(A(tx+(1-t)x')\).  Thus a globally one-to-one convex lift automatically
has a smooth primal factor map.  A separate dual regularity condition is
still required.

## Why strict convexity, definability, and analytic centers do not suffice

The standard two-stage Lorentz lift of \(B_2^3\) is

 \[
 (t,x_1,x_2)\in Q_3,\qquad (1,t,x_3)\in Q_3.                    \tag{13}
\]

On the sphere, its lifted boundary fiber is unique:

\[
                         t=\sqrt{x_1^2+x_2^2}.                  \tag{14}
\]

Both factors are strictly convex, the lift is semialgebraic, and a
singleton fiber is its own analytic center.  Nevertheless, near either
pole \((0,0,\pm1)\), the primal contact incidence is the graph

\[
             (x_1,x_2)\longmapsto\sqrt{x_1^2+x_2^2},            \tag{15}
\]

which has a cone point and is not even \(C^1\).  Thus the incidence
projection fails the regularity hypothesis exactly where the partial norm
vanishes.  Larger Lorentz norm trees contain the same local model whenever
a child group vanishes.  They attain the unrestricted \(N-1\) count in all
dimensions and therefore show that no lift-level penalty such as (8) can
hold without a hypothesis that excludes this branching/nonsmoothness.

This example simultaneously proves that the following conditions, alone or
in combination, are insufficient:

- unique fibers only on the smooth boundary;
- strict convexity and smoothness of every cone factor away from its apex;
- semialgebraicity or o-minimal definability of the lift; and
- choosing the relative analytic center of each contact fiber.

Definability guarantees finite smooth stratifications and hence generic
smooth selections, but not one stratum covering the entire contact sphere.
The topological obstruction lives precisely in the unavoidable transition
set between those strata.

## Scope and literature boundary

The cone-lift/slack-factor identity is the framework of
Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).  Robinson's
strong-regularity theory guarantees locally single-valued Lipschitz
solutions of generalized equations, but Lipschitz regularity alone is not
being used as a substitute for the \(C^2\) hypothesis here; the KKT
criterion above deliberately invokes a smooth fixed active stratum and a
nonsingular classical Jacobian.  See Robinson,
[*Strongly Regular Generalized
Equations*](https://doi.org/10.1287/moor.5.1.43).  The covering-space step
is standard, and the vector-field obstruction is Adams's theorem as cited
in the smooth-factor note.  The arbitrary-rank plane-field input is
Dibag, [*Almost-complex substructures on the
sphere*](https://doi.org/10.1090/S0002-9939-1976-0423248-5), Lemma 2.1,
which records Steenrod's equivalence between tangent \(R\)-plane fields and
\(R\)-frames for \(2R\leq n\).

A targeted search found work on cone factorizations and on parametric conic
KKT regularity, but no source deriving a sparse-cone count penalty from the
topology of the primal and dual contact incidences.  The count theorem and
the regularity dichotomy therefore appear new, subject to specialist
review.  The result is intentionally scoped: it does not strengthen the
unrestricted exact lift count, because norm trees exhibit the necessary
contact singularities.

## Independent audit record

The hostile audit verified the following points.

- The added compact-body and \(0\in\operatorname{int}C\) hypotheses are
  necessary for the stated polar normalization. Slater's condition gives
  dual attainment for each finite support problem, and the sign
  \(E^T\lambda-P^Ty\in K^*\) yields
  \(\langle A(x),B(y)\rangle=1-\langle x,y\rangle\) exactly.
- The definition uses a contact sheet rather than requiring a connected
  component of the whole incidence. This is the condition actually needed
  by the proof and makes the KKT-selection criterion valid even when the
  underlying contact fiber has positive dimension. Properness makes the
  local-diffeomorphism image closed; local invertibility makes it open; and
  simple connectivity then makes the connected cover one-sheeted.
- \(C^3\) boundary regularity makes the normalized polar-contact map \(C^2\),
  so the inverse contact sheets really do produce the \(C^2\) factors needed
  by the diagonal-Hessian argument.
- The Adams index is \(\rho(N)-1\) for \(S^{N-1}\). For odd \(N\), the
  Euler-class argument excludes every proper positive-rank splitting, and
  the integrality, block-count, coordinate-count, and barrier inequalities
  (6)--(7) follow with the stated cap; the all-three-dimensional consequences
  (8)--(9) were checked separately. The \(\nu\) claim is only for an
  ambient-product logarithmically homogeneous self-concordant barrier,
  including a coupled one; it is not a projected-body barrier lower bound.
- An independent topology audit checked that the proper nonsingular contact
  sheets produce exactly the global splitting needed by the
  Steenrod--Dibag theorem.  It separately verified the subset-sum
  obstruction, the \(s<n/3\) dominant-block argument, the exception list
  \(\{4,8,16\}\), and the strict capacity, count, dimension, and barrier
  consequences under \(d<N+2-\rho(N)\).
- The factor-integrability audit verified the normalized-base submersion
  contradiction for arbitrary three-dimensional proper cones, including
  cornered bases and \(N=4,8\), under only globally labelled \(C^1\)
  factors.  It also checked
  the explicit \(Q_3^N\) affine lift, its unique polynomial boundary fibers,
  the normalized smooth dual sheet, Slater point, and the simultaneous
  \(k=N\), \(M=3N\), and ambient-product \(\nu=2N\) optima.
- In the \(B_2^3\) norm-tree lift, the boundary equations force
  \(t=\sqrt{x_1^2+x_2^2}\). At the poles the inverse of the incidence
  projection is not \(C^1\), so the example genuinely violates contact
  regularity despite singleton fibers and smooth Lorentz factors away from
  their apices.

The primary-source screen covered cone-lift/slack-factorization work,
spectrahedral-shadow boundary geometry, smooth parametric/KKT solution
maps, and SOC-lift obstructions. It found no theorem combining contact
incidence regularity, curvature-capacity saturation, and the
Adams/Euler tangent-bundle obstruction. The apparent novelty assessment
therefore survives the audit, subject to specialist review.
