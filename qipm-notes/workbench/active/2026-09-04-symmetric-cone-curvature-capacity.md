# Curvature capacity of symmetric-cone lifts

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the local Jordan-algebra lemma; novelty pending specialist review

## Headline theorem

Let \(C\subset\mathbb R^N\), \(N\geq2\), be a full-dimensional compact convex body
with \(0\in\operatorname{int}C\). Suppose that \(C\) has an exact lift
over a finite product of symmetric cones, allowing arbitrary affine
slices, projections, and unrestricted free variables. Decompose that
product into irreducible factors

\[
 K=K_1\times\cdots\times K_k.
\]

For factor \(K_s\), let \(r_s\) be its Jordan rank and \(a_s\) its
Peirce constant: every off-diagonal Peirce space of its simple Euclidean
Jordan algebra has real dimension \(a_s\). More locally, at any exposed
primal--polar contact where the paired boundary charts and the composed
semialgebraic factor selections are \(C^1\), let \(\mathcal K\) be the
mixed slack-curvature form defined in (19). Then

\[
 \operatorname{rank}\mathcal K
 \leq\sum_{s=1}^k a_sp_sq_s.                           \tag{0}
\]

If \(C\) has a relatively open \(C^2\) boundary neighborhood containing
a point of strictly positive curvature, the contact can be chosen so that
\(\operatorname{rank}\mathcal K=N-1\), and hence

\[
 \boxed{
 N-1\leq
 \sum_{s=1}^k a_s p_s q_s
 \leq
 \sum_{s=1}^k a_s\left\lfloor\frac{r_s^2}{4}\right\rfloor .}
                                                               \tag{1}
\]

Here \(p_s,q_s\) are the Jordan ranks of a complementary primal--dual
factor pair at one generic positively curved contact, and
\(p_s+q_s\leq r_s\). Thus a rank-\((p,q)\) contact in a simple
symmetric cone has exactly \(apq\) available mixed-curvature channels.
No strict-complementarity assumption is made.

If \(m_s=\dim K_s\), then

\[
 m_s=r_s+\frac{a_s}{2}r_s(r_s-1),
 \qquad
 a_s\left\lfloor\frac{r_s^2}{4}\right\rfloor
 \leq m_s-r_s\leq m_s-2                         \tag{2}
\]

for every non-ray irreducible factor. Consequently

\[
 \boxed{N-1\leq\sum_s(m_s-r_s)=M-\nu,}            \tag{3}
\]

where \(M=\sum_s m_s\) is the total cone-space dimension and
\(\nu=\sum_s r_s\) is both total Jordan rank and the optimal normal-barrier
parameter of the product.

The word *block* below always means an irreducible symmetric-cone factor.
Treating a reducible Cartesian product as one syntactic block would make a
block-count statement representation-dependent for no mathematical reason.

## Exact bounded-block consequences for the Euclidean ball

Suppose every irreducible factor has ambient dimension at most \(d\geq3\).
Equation (2) gives at most \(d-2\) curvature channels per factor, so every
such lift of a positively curved \(N\)-body obeys

\[
 k\geq\left\lceil\frac{N-1}{d-2}\right\rceil.       \tag{4}
\]

For the Euclidean ball this is sharp. A norm tree using Lorentz cones of
dimension at most \(d\) realizes equality, as described in
[the exact Lorentz note](2026-09-04-exact-lorentz-curvature-budget.md).
It also makes both inequalities in (2) equalities. Therefore, among *all*
products of irreducible symmetric cones with \(m_s\leq d\), not only among
Lorentz products, the exact optima for \(B_2^N\) are

\[
 \boxed{
 \begin{aligned}
 k_{\min}&=\left\lceil\frac{N-1}{d-2}\right\rceil,\\
 \nu_{\min}&=2\left\lceil\frac{N-1}{d-2}\right\rceil,\\
 M_{\min}&=N-1+2\left\lceil\frac{N-1}{d-2}\right\rceil.
 \end{aligned}}                                      \tag{5}
\]

Indeed, (4) and \(r_s\geq2\) for every positive-capacity factor give the
barrier bound in (5), while (3) gives \(M\geq N-1+\nu\). The Lorentz norm
tree attains all three bounds simultaneously. Ray factors have zero
capacity and can only increase \(k,M,\nu\). For \(d\leq2\), only products
of rays are available after irreducible decomposition, so no finite exact
lift of a positively curved body exists.

This says that complex, quaternionic, and exceptional symmetric-cone
blocks cannot improve on Lorentz blocks when the resource cap is the real
ambient dimension of each irreducible block. The conclusion concerns the
chosen conic representation and its ambient normal barrier. It is not an
intrinsic barrier lower bound for the projected ball and is not by itself a
universal IPM iteration lower bound.

There is now a strict global-regularity refinement.  If the primal and polar
factor selections are globally labelled \(C^1\) on the full paired
boundaries, the
[support-idempotent covering theorem](2026-09-04-symmetric-cone-support-orbit-rigidity.md)
shows that equality in (1) requires one full spin factor of dimension
\(N+1\), apart from a resource-dominated \(N=3\) real-PSD possibility.
Thus for \(3\leq d<N+1\), the globally bi-\(C^1\) optima replace \(N-1\)
by \(N\):
\[
 k_{\min}=\left\lceil{N\over d-2}\right\rceil,\qquad
 M_{\min}=N+2k_{\min},\qquad \nu_{\min}=2k_{\min}.
\]
There is no contradiction with (5): the semialgebraic lift reduction above
produces \(C^1\) selections only on a dense open contact stratum, while the
covering theorem needs them globally.

## The five simple families and their exact capacities

With the trace inner product on each Euclidean Jordan algebra, the
classification gives the following table. Low-rank coincidences between
matrix cones and spin factors do not affect the formulas.

| irreducible cone | Jordan rank \(r\) | Peirce constant \(a\) | real dimension \(m\) | maximum contact capacity \(a\lfloor r^2/4\rfloor\) | normal barrier \(\nu\) |
|---|---:|---:|---:|---:|---:|
| ray \(\mathbb R_+\) | 1 | 0 | 1 | 0 | 1 |
| Lorentz \(Q_m\), \(m\geq3\) | 2 | \(m-2\) | \(m\) | \(m-2\) | 2 |
| real PSD \(S_+^r\) | \(r\) | 1 | \(r(r+1)/2\) | \(\lfloor r^2/4\rfloor\) | \(r\) |
| complex Hermitian PSD \(H_+^r(\mathbb C)\) | \(r\) | 2 | \(r^2\) | \(2\lfloor r^2/4\rfloor\) | \(r\) |
| quaternionic Hermitian PSD \(H_+^r(\mathbb H)\) | \(r\) | 4 | \(r(2r-1)\) | \(4\lfloor r^2/4\rfloor\) | \(r\) |
| exceptional \(H_+^3(\mathbb O)\) | 3 | 8 | 27 | 16 | 3 |

For a formulation restricted to one matrix family with Peirce constant
\(a\), let

\[
 R_a(d)=\max\left\{r:
 r+\frac a2r(r-1)\leq d\right\}.
\]

Assume \(R_a(d)\geq2\). Then dimension-\(d\) blocks have capacity at most
\(a\lfloor R_a(d)^2/4\rfloor\), yielding

\[
 k\geq
 \left\lceil
 \frac{N-1}{a\lfloor R_a(d)^2/4\rfloor}
 \right\rceil,                                        \tag{6}
\]

and, since capacity/rank is increasing with \(r\),

\[
 \nu\geq
 \left\lceil
 \frac{R_a(d)(N-1)}{a\lfloor R_a(d)^2/4\rfloor}
 \right\rceil.                                        \tag{7}
\]

Equations (6)--(7) are lower bounds, not matching construction claims.
If \(R_a(d)=1\), that matrix family supplies only ray factors and admits no
finite exact lift of a positively curved body.
For the exceptional cone, each factor instead has capacity 16 and barrier
3, giving \(k\geq\lceil(N-1)/16\rceil\) and
\(\nu\geq3\lceil(N-1)/16\rceil\).

## Reduction from an arbitrary affine lift to regular slack factors

All regularity is obtained from the finite-dimensional lift; it is not
assumed of an arbitrary abstract factorization. First eliminate free
variables by boundedness, extend the affine output on the slice to a linear
map, and pass to the minimal face containing a relative-interior feasible
point. These steps are written out in
[the Lorentz proof](2026-09-04-exact-lorentz-curvature-budget.md).

Faces of a symmetric cone are exposed and are themselves cones of squares
in Peirce-1 subalgebras. A face of a product is a product of faces. After
replacing each factor by the corresponding face in its linear span, the
lift is proper. A rank-\(s\) face of a simple rank-\(r\) factor has the same
Peirce constant and capacity
\(a\lfloor s^2/4\rfloor\leq a\lfloor r^2/4\rfloor\);
rank-one faces are rays. Hence this reduction cannot weaken a bound stated
with the original factors.

Write the resulting proper lift as

\[
 C=\{\pi z:z\in K,\ Mz=b\},
 \qquad w_0\in\operatorname{int}K,\quad Mw_0=b.        \tag{8}
\]

Minimum-norm primal fibers and minimum-norm attained dual multipliers give
maps \(A\) and \(B\) on exposed primal and polar boundary points such that

\[
 A(x)\in K,\quad B(y)\in K^*,\qquad
 1-\langle x,y\rangle=\langle A(x),B(y)\rangle.        \tag{9}
\]

Concretely, \(A(x)\) is the unique minimum-norm point with
\(Mz=b,\pi z=x\). Strong duality and attainment follow from the interior
point \(w_0\); if \(\lambda(y)\) is the minimum-norm multiplier satisfying

\[
 M^*\lambda(y)-\pi^*y\in K^*,
 \qquad \langle b,\lambda(y)\rangle=1,
\]

then \(B(y)=M^*\lambda(y)-\pi^*y\), which proves (9) directly.

Choose fixed self-dual Euclidean-Jordan coordinates on every factor. If the
original lift uses a different ambient pairing, apply the primal linear
isomorphism and its inverse adjoint to the dual factor; equation (9) and all
ranks are unchanged. Thus both components of each factor pair may be viewed
in the same cone of squares with its trace inner product.

Symmetric cones and all finite affine systems over them are semialgebraic,
even when their numerical coefficients are arbitrary real numbers. The
minimum-norm graphs above are semialgebraic by real quantifier elimination.
The lifted body is therefore semialgebraic. Shrink the assumed \(C^2\)
boundary patch to a nonempty open neighborhood of strict positive curvature.
On this patch, the normal and normalized polar-contact maps are also
semialgebraic. Positive definite second fundamental form excludes a
nontrivial support face through the primal point, so that point is exposed;
\(C^1\) smoothness makes its normal ray unique, so the normalized polar
normal is exposed as well. A finite compatible semialgebraic stratification
supplies a dense open subset on which all composed primal and dual factor
maps are simultaneously \(C^1\). Choose the contact in this subset of the
already positively curved patch.

In local coordinates \(u\in\mathbb R^{N-1}\), write the paired contact as

\[
 x(u)\in\partial C,\qquad
 y(u)=\frac{n(u)}{\langle x(u),n(u)\rangle}\in\partial C^\circ,
 \qquad \langle x(u),y(u)\rangle=1.                   \tag{10}
\]

Decomposing (9) by irreducible factors and using self-duality makes every
summand nonnegative. Its diagonal sum is zero, so for every \(s,u\),

\[
 \langle X_s(u),Y_s(u)\rangle=0,
 \qquad X_s(u)=A_s(x(u)),\quad Y_s(u)=B_s(y(u)).       \tag{11}
\]

## The Peirce tangent-channel lemma

Let \(V\) be a simple Euclidean Jordan algebra of rank \(r\), Peirce
constant \(a\), cone of squares \(K\), and trace inner product. Let
\(X,Y:U\to K\) be \(C^1\) maps satisfying
\(\langle X(u),Y(u)\rangle=0\). At \(u=0\), positivity and orthogonality
give a common Jordan frame \(c_1,\ldots,c_r\) in which

\[
 X(0)=\sum_{i\in I}\lambda_i c_i,
 \qquad
 Y(0)=\sum_{j\in J}\mu_j c_j,
 \qquad \lambda_i,\mu_j>0,\quad I\cap J=\varnothing. \tag{12}
\]

Put \(p=|I|\), \(q=|J|\); the unused frame elements explicitly allow
\(p+q<r\). Let

\[
 V=\bigoplus_{1\leq i\leq j\leq r}V_{ij},
 \qquad V_{ii}=\mathbb Rc_i,
 \qquad \dim V_{ij}=a\quad(i<j)                       \tag{13}
\]

be the orthogonal Peirce decomposition.

For any tangent direction \(h\), the projection of \(DX(0)[h]\) onto the
kernel Peirce algebra generated by \(\{c_i:i\notin I\}\) vanishes. Indeed,
for every positive element \(w\) of that algebra,
\(\langle X(th),w\rangle\geq0\) for both signs of small \(t\), and the
value at zero is zero. Its derivative is therefore zero. The positive cone
spans the kernel algebra, proving the claim. The same argument applies to
\(DY(0)[h]\). This argument does not require locally constant rank.

It follows by orthogonality of (13) that the only Peirce spaces on which
the two derivatives can have a nonzero inner product are

\[
 E_{IJ}=\bigoplus_{i\in I,\,j\in J}V_{ij},
 \qquad \dim E_{IJ}=apq.                              \tag{14}
\]

Positive orthogonal elements in a Euclidean Jordan algebra are Jordan
complementary, so \(X(u)\circ Y(u)=0\). Differentiate this identity and
project onto \(V_{ij}\), \(i\in I,j\in J\). Since multiplication by
\(c_i\) or \(c_j\) is one half the identity on \(V_{ij}\),

\[
 \mu_j(DX(0)[h])_{ij}+\lambda_i(DY(0)[h])_{ij}=0.     \tag{15}
\]

Therefore, for tangent directions \(h,\ell\),

\[
 \begin{aligned}
 -\langle DX(0)[h],DY(0)[\ell]\rangle
 &=\sum_{i\in I,j\in J}\frac{\mu_j}{\lambda_i}
 \left\langle(DX(0)[h])_{ij},(DX(0)[\ell])_{ij}\right\rangle.
                                                               \tag{16}
 \end{aligned}
\]

This is a positive-semidefinite Gram form of rank at most \(apq\), and

\[
 apq\leq a\left\lfloor\frac{r^2}{4}\right\rfloor.   \tag{17}
\]

If either factor is zero, its derivative is zero: a two-sided derivative at
the vertex of a pointed cone belongs to both \(K\) and \(-K\). Thus (16)
also covers zero factors. Residual frame directions do not overlap in the
two derivatives, which is why strict complementarity is unnecessary.

The channel number \(apq\) is exact, not merely an upper estimate. For
\(z\in V_{ij}\), the inner derivation

\[
 D_z=4[L_z,L_{c_i}]
\]

satisfies \(D_zc_i=z\), \(D_zc_j=-z\). The Jordan automorphism
\(\exp(tD_z)\) preserves the cone and complementarity. Applying independent
first-order rotations in every \(V_{ij}\), \(i\in I,j\in J\), gives
\((DX)_{ij}=\lambda_i z\) and \((DY)_{ij}=-\mu_jz\). It therefore realizes
a positive Gram form on all of the \(apq\)-dimensional space (14).

## From contact channels to boundary curvature

Differentiate the two-variable slack factorization

\[
 1-\langle x(u),y(v)\rangle
 =\sum_s\langle X_s(u),Y_s(v)\rangle                 \tag{18}
\]

once in \(u\) and once in \(v\), then use (16). This gives

\[
 \mathcal K:=Dx(0)^TDy(0)
 =\sum_s G_s,
 \qquad G_s\succeq0,
 \qquad \operatorname{rank}G_s\leq a_sp_sq_s.        \tag{19}
\]

For the normalization in (10), tangent-normal orthogonality gives

\[
 \mathcal K=
 \frac{1}{\langle x(0),n(0)\rangle}Dx(0)^TDn(0),     \tag{20}
\]

the second fundamental form up to a positive scalar and a change of local
coordinates. It has rank \(N-1\) at a strictly positively curved point.
Rank subadditivity in (19) proves (1).

Finally, (2) follows from the dimension formula and

\[
 \left\lfloor\frac{r^2}{4}\right\rfloor
 \leq\frac{r(r-1)}2\qquad(r\geq2).
\]

Summing proves (3), (4), and (5).

## Literature boundary

[Faraut and Korányi, *Analysis on Symmetric
Cones*](https://doi.org/10.1093/oso/9780198534778.001.0001), especially
Chapters III--V, is the primary source for the spectral theorem, Peirce
decomposition, face structure, simple-algebra classification, and dimension
formula. An accessible optimization treatment records the orthogonal Peirce
decomposition and direct-sum reduction in
[Lourenço, Fukuda, and Fukushima](https://optimization-online.org/wp-content/uploads/2009/07/2350.pdf).
[Güler and Tunçel](https://doi.org/10.1007/BF01584844) prove that the optimal
normal-barrier parameter of a homogeneous cone equals its Carathéodory
number; for symmetric cones this is Jordan rank and is additive on products.
[Gouveia, Parrilo, and
Thomas](https://arxiv.org/abs/1111.3164) supply the general
lift/slack-factorization framework.

The closest quantitative block-lift results found were the fixed-size real
PSD lower bounds of [Fawzi and Parrilo](https://arxiv.org/abs/1311.2571),
which concern primarily polytope support patterns, and the single-PSD-block
algebraic-boundary bounds of [Fawzi and Safey El
Din](https://arxiv.org/abs/1705.06996).
[Helton and Nie](https://arxiv.org/abs/0709.4017) use boundary curvature
to give sufficient and necessary conditions for semidefinite
representability, but do not lower-bound the size or number of lifting
blocks. [Scheiderer's semidefinite-extension-degree
framework](https://arxiv.org/abs/2004.04196) controls maximum PSD block
size rather than the number of fixed-size blocks; his later
[positive-curvature SOCR theorem](https://arxiv.org/abs/2509.17121) is an
existence theorem and is complementary to the quantitative lower bound
here. Targeted searches for Peirce
decomposition plus slack factorization, differential or curvature lower
bounds for symmetric-cone lifts, and positive-curvature block extension
complexity found no statement of (1), (3), or (5). The theorem should be
called apparently new pending specialist review; an open-literature search
cannot establish priority.

## Audit checklist

- Verify the common-frame consequence of positive orthogonality and the
  differentiation of Jordan complementarity in (15).
- Check that the two-sided positivity argument kills the complete
  kernel-algebra derivative, without a constant-rank assumption.
- Check every residual Peirce space when \(p+q<r\).
- Verify the normalization and sign in (18)--(20).
- Verify that \(D_z=4[L_z,L_{c_i}]\) is a derivation with the stated action,
  so the claim that capacity is exact is justified.
- Check all classification constants, the monotonicity used in (7), and the
  exact simultaneous optima in (5).
- Search specifically for differential slack-factor and second-fundamental-
  form lower bounds for arbitrary symmetric-cone lifts.

The independent hostile audit checked the common-frame and residual-space
arguments, all coefficients and signs in the differentiated Peirce identity,
the exact-channel inner derivations, minimal-face and self-dual-coordinate
reductions, classification constants, barrier identification, and all three
ball optima. It found no counterexample. Its requests concerning \(N=1\),
exposure, and selection of the positive-curvature regular locus have been
incorporated.
