# Topological obstruction to globally smooth saturated cone factorizations

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Theorem

Let \(C\subset\mathbb R^N\), \(N\geq2\), be a compact convex body with
\(C^2\), strictly positively curved boundary \(M=\partial C\).  Normalize
\(0\in\operatorname{int}C\), and let \(y(x)\in\partial C^\circ\) be the
unique polar contact satisfying

\[
                    \langle x,y(x)\rangle=1.                     \tag{1}
\]

Suppose the slack on the full contact manifold has a globally \(C^2\)
factorization

\[
  1-\langle x,y(z)\rangle
   =\sum_{i=1}^k\langle A_i(x),B_i(z)\rangle,qquad x,z\in M,     \tag{2}
\]

where \(A_i(x)\in K_i\), \(B_i(z)\in K_i^*\), and every \(K_i\) is a
finite-dimensional proper cone of dimension \(m_i\).  Assume the universal
curvature budget is saturated:

\[
                    \sum_i(m_i-2)_+=N-1.                         \tag{3}
\]

Then the tangent bundle splits continuously (indeed \(C^0\), and more
regular if the factors are) as

\[
                    TM=\bigoplus_i E_i,qquad
                    \operatorname{rank}E_i=(m_i-2)_+.            \tag{4}
\]

The summands are mutually orthogonal for the positive mixed-curvature
metric.  In particular, every three-dimensional factor supplies a real line
subbundle of \(TM\).

Since \(M\) is diffeomorphic to \(S^{N-1}\), let \(q\) be the number of
three-dimensional factors.  If \(N\geq3\), each real line bundle on
\(S^{N-1}\) is trivial, so (4) supplies \(q\) pointwise independent vector
fields.  Adams's theorem therefore gives

\[
                    \boxed{q\leq\rho(N)-1,}                      \tag{5}
\]

where, writing \(N=(2a+1)2^{4c+d}\) with \(0\leq d\leq3\),

\[
                    \rho(N)=8c+2^d.                              \tag{6}
\]

For \(N=2\), the single tangent line is already trivial and (5) also holds.

### Even-dimensional-boundary corollary

Suppose \(N\geq3\) is odd, so \(M\simeq S^{N-1}\) is even-dimensional.
Then (4) has exactly one positive-rank summand.  Equivalently, there is a
unique positive-curvature block \(i_*\), and saturation forces

\[
                  m_{i_*}=N+1,\qquad m_i\leq2\quad(i\neq i_*).  \tag{6a}
\]

Consequently, if every block has dimension at most \(d<N+1\), no saturated
globally \(C^2\) factorization of the form (2) exists.  This obstruction
applies to every strictly positively curved \(N\)-body, not only the
Euclidean ball.

### All-three-dimensional corollary

If \(k=N-1\) and every factor has dimension three, (4) is a global frame of
\(TM\).  Hence \(S^{N-1}\) is parallelizable, which occurs exactly for

\[
                    N\in\{2,4,8\}                               \tag{7}
\]

among \(N\geq2\).  Therefore, for every other \(N\), an exact saturated
minimum-count three-dimensional-cone lift cannot admit globally \(C^2\)
primal and dual slack-factor selections on the whole contact manifold.
Every such representation must have selection singularities, chart changes,
or loss of the assumed global factorization regularity somewhere.

This is **not** a nonexistence theorem for the lift itself.  Standard norm
trees exist in every dimension; their partial-norm factor selections fail to
be \(C^2\) where a child group vanishes, exactly the type of escape allowed
by the theorem.

## Proof

For each block define

\[
                  g_i(x,z)=\langle A_i(x),B_i(z)\rangle.         \tag{8}
\]

Cone duality gives \(g_i\geq0\).  On the contact diagonal, (1)--(2) give
\(\sum_i g_i(x,x)=0\), so nonnegativity implies

\[
                         g_i(x,x)=0                              \tag{9}
\]

for every \(i\) and \(x\).

Fix \(x\in M\).  The Hessian of \(g_i\) on \(M\times M\) at \((x,x)\)
is positive semidefinite, because that point is a global minimum.  The
tangent diagonal \(\{(u,u):u\in T_xM\}\) has zero Hessian quadratic form
by (9), and hence lies in the kernel of the positive semidefinite Hessian.
More explicitly, write its blocks in the two tangent variables as

\[
             \begin{pmatrix}P&R\\R^T&Q\end{pmatrix}.
\]

The kernel identity on every \((u,u)\) gives \(P=-R\) and
\(Q=-R^T\).  Since \(P,Q\) are symmetric, \(R=R^T\), and since a principal
block of a positive semidefinite matrix is positive semidefinite,
\(-R=P\succeq0\).  The mixed block is
\(R(u,v)=\langle dA_i(x)u,dB_i(x)v\rangle\).  Thus

\[
 H_i(x)(u,v):=-\langle dA_i(x)u,dB_i(x)v\rangle                  \tag{10}
\]

is a symmetric positive semidefinite bilinear form on \(T_xM\).

Mixed differentiation of (2) gives

\[
       H(x):=\sum_iH_i(x),qquad
       H(x)(u,v)=\langle u,dy(x)v\rangle.                         \tag{11}
\]

The sign in (11) is positive.  If \(\nu(x)\) is the outward unit normal and
\(h(x)=\langle x,\nu(x)\rangle>0\), then

\[
 y(x)=\frac{\nu(x)}{h(x)},\qquad
 \langle u,dy(x)v\rangle
   =\frac{\langle u,d\nu(x)v\rangle}{h(x)}                       \tag{11a}
\]

for tangent \(u,v\).  With the outward-normal convention,
\(\langle u,d\nu(v)\rangle\) is the positive-sign second fundamental form
(it is the round metric on the unit sphere).  Strict positive curvature
therefore makes \(H(x)\) positive definite.  The universal tangent-pairing lemma gives

\[
             \operatorname{rank}H_i(x)\leq(m_i-2)_+.             \tag{12}
\]

Equations (3), (11), and rank subadditivity force equality in every bound at
every point:

\[
             \operatorname{rank}H_i(x)=(m_i-2)_+.                \tag{13}
\]

Let \(P_i(x)\) be the \(H(x)\)-self-adjoint endomorphism defined by

\[
             H(x)(P_i(x)u,v)=H_i(x)(u,v).                        \tag{14}
\]

Equivalently, in any local frame,
\(P_i=H^{-1/2}(H^{-1/2}H_iH^{-1/2})H^{1/2}=H^{-1}H_i\).  To spell out
the Parseval equality argument, factor each positive semidefinite whitened
matrix \(Q_i=H^{-1/2}H_iH^{-1/2}\) as \(Q_i=Z_iZ_i^T\), using
\(\operatorname{rank}Q_i\) columns.  By (3) and (13), concatenating the
\(Z_i\)'s gives a square matrix \(Z\), while \(\sum_iQ_i=I\) gives
\(ZZ^T=I\).  Thus \(Z\) is orthogonal, and the \(Q_i\)'s are mutually
orthogonal projections.  Hence the
\(P_i\)'s are continuous idempotents with pairwise-disjoint images and sum
to the identity.  Constant rank (13) implies that

\[
                         E_i=\operatorname{im}P_i                \tag{15}
\]

is a vector subbundle, and (4) follows.

Every ray from the interior point meets \(M\) exactly once, and
\(h(x)>0\) makes the radial direction transverse to \(M\).  Radial
projection therefore identifies \(M\) diffeomorphically with
\(S^{N-1}\).  For
\(N-1\geq2\), real line bundles are classified by their first
Stiefel--Whitney class in
\(H^1(S^{N-1};\mathbb Z_2)=0\); hence every rank-one \(E_i\) is trivial.
Choosing a nonzero section in each and using the direct sum in (4) produces
\(q\) independent tangent vector fields.  Adams's vector-field theorem gives
(5)--(6).  When \(q=N-1\), the tangent bundle is trivial.  Equivalently,
Adams's formula forces \(\rho(N)=N\), which occurs only for
\(N\in\{1,2,4,8\}\); under \(N\geq2\) this gives (7).  This is also the
classical Bott--Milnor--Kervaire parallelizable-sphere theorem.

It remains to prove the even-dimensional-boundary corollary.  Put
\(n=N-1\), which is even and at least two.  Suppose (4) had at least two
positive-rank summands.  Choose one of them, say \(E\), and let \(F\) be
the direct sum of all the others.  Then

\[
                    TM=E\oplus F,\qquad
                    0<\operatorname{rank}E,\operatorname{rank}F<n. \tag{16}
\]

Because \(M\simeq S^n\) is simply connected, both real bundles are
orientable.  Their Euler classes lie in intermediate cohomological degrees,
so

\[
 e(E)\in H^{\operatorname{rank}E}(S^n;\mathbb Z)=0,
 \qquad
 e(F)\in H^{\operatorname{rank}F}(S^n;\mathbb Z)=0.             \tag{17}
\]

The Whitney product formula now gives \(e(TM)=e(E)\smile e(F)=0\).
This contradicts

\[
                  \langle e(TM),[M]\rangle=\chi(S^n)=2.        \tag{18}
\]

Thus exactly one \(E_i\) has positive rank; there must be one because the
ranks sum to \(n\).  Equations (3) and (13) then give
\((m_{i_*}-2)_+=n\), hence \(m_{i_*}=N+1\), while all other blocks have
\((m_i-2)_+=0\), proving (6a) and the block-cap consequence.

## Scope and literature boundary

The hypothesis is deliberately global and concerns **factor selections**,
not merely existence of a cone lift.  Standard lift-to-slack arguments give
definable selections and common smooth strata locally; they do not guarantee
one globally \(C^2\) choice across the contact manifold.  The conclusion is
therefore an unavoidable-regularity statement, not an extra block-count
lower bound for unrestricted lifts.

The exact lift/factorization framework is due to Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).  Adams proved that
the maximum number of independent vector fields on \(S^{N-1}\) is
\(\rho(N)-1\) in
[*Vector Fields on Spheres*](https://doi.org/10.2307/1970213), *Annals of
Mathematics* 75 (1962), 603--632.  The parallelizable-sphere consequence is
also in Bott--Milnor,
[*On the Parallelizability of the
Spheres*](https://doi.org/10.1090/S0002-9904-1958-10166-4), and Kervaire,
[*Non-Parallelizability of the \(n\)-Sphere for \(n>7\)*](https://doi.org/10.1073/pnas.44.3.280).
The Euler-class product formula and the identity
\(\langle e(TM),[M]\rangle=\chi(M)\) used in (16)--(18) are classical;
see Milnor--Stasheff,
[*Characteristic Classes*](https://doi.org/10.1515/9781400881826),
Sections 9 and 11.  In particular, the purely topological statement that
\(TS^{2a}\) has no proper positive-rank direct summand is known.  The new
candidate contribution here is its consequence for saturated smooth cone
slack factorizations, not that topological lemma itself.

A targeted search found no source combining smooth cone/slack
factorizations, curvature-budget saturation, and tangent-bundle splitting.
There is a separate literature on Parseval frames for vector bundles, for
example Ballas--Needham--Shonkwiler,
[*On the Existence of Parseval Frames for Vector
Bundles*](https://arxiv.org/abs/2312.13488), but it starts from a bundle and
studies frame existence; it does not derive an orthogonal splitting from a
cone slack factorization.
The topology used after (4) is classical; the apparently new step is that a
saturated globally smooth cone factorization canonically creates these
tangent subbundles.  Novelty remains subject to specialist review.

The independent audit checked the Hessian diagonal-kernel argument, the
sign and normalization in (11)--(11a), pointwise full rank, continuity and
idempotence of the projection fields, line-bundle triviality including the
separate circle case, radial diffeomorphism, and the Adams arithmetic.  A
second hostile audit checked the Euler-class strengthening, including
orientability, zero-rank factors, Whitney multiplicativity, and the odd-\(N\)
edge cases, and found no mathematical error.  The theorem remains strictly
a global-selection regularity obstruction; it does not imply nonexistence
of the underlying lift.
