# Exact standard-slice barrier frontier under a Hermitian PSD order cap

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\in\{1,2,4\}\), and let \(R\geq2\).
Consider globally bi-\(C^1\) affine lifts of \(B_2^N\), \(N\geq2\), by
finite products of Hermitian PSD cones \(H_+^{r_i}(\mathbb F)\) with
\(r_i\leq R\).  Restrict the standard product Jordan log-determinant to the
lift's affine slice, and let \(\nu_{\rm std,slice}\) denote its smallest
gradient parameter.

Define

\[
                            b=a(R-1).                      \tag{1}
\]

Then the exact optimum in this regularity class is

\[
 \boxed{
 \nu_{\rm std,slice}^{\min}=
 \begin{cases}
 1,&N\leq b,\\
 1,&R=2,\ N=a+1,\\
 \left\lceil N/b\right\rceil,&\text{otherwise}.
 \end{cases}}                                             \tag{2}
\]

The second line consists exactly of the direct rank-two division-algebra
cones

\[
 H_+^2(\mathbb R)\cong Q_3\ (N=2),\qquad
 H_+^2(\mathbb C)\cong Q_4\ (N=3),\qquad
 H_+^2(\mathbb H)\cong Q_6\ (N=5).                        \tag{3}
\]

Thus the only time the local \((N-1)\)-dimensional tangent budget saves a
whole standard-slice barrier unit is when the single block is itself the
appropriate spin factor.  For real PSD order \(R\geq3\), in particular,
a hypothetical sharp map \(S^{R-1}\to\mathbb {RP}^{R-1}\) is ruled out by
the affine PSD pencil forced by the full ball slack, not by topology alone.

As in the symmetric-cone companion, (2) concerns the standard product
barrier after restriction.  It is not a lower bound for arbitrary custom
barriers or for IPM/QIPM iterations.

The real critical case is now additive across source balls.  For the full
slack of \((B_2^R)^b\), \(R\geq3\), over real PSD blocks of order at most
\(R\), the independently audited
[all-field sequential contact-range theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md)
constructs one simultaneous contact with total dual-range span, and hence
total primal nullity, at least \(2b\).  Therefore the globally bi-\(C^1\)
restricted standard-barrier optimum is exactly \(2b\), the sum of the
one-ball values in (2).  The proof permits arbitrary cross-source label
switching; it successively quotients each block by previously fixed contact
ranges and reapplies the real sole-factor obstruction above.

## Nullity lower bound

At a selected primal boundary fiber, write

\[
 p_i=\operatorname{rank}X_i,\qquad
 z_i=r_i-p_i,\qquad Z=\sum_i z_i.                         \tag{4}
\]

The determinant along a segment to a Slater point vanishes to exact order
\(z_i\).  Therefore the boundary-order lemma gives

\[
                              \nu_{\rm std,slice}\geq Z.   \tag{5}
\]

At the paired contact, let \(q_i=\operatorname{rank}Y_i\).  The real
cross-Peirce dimension is \(ap_iq_i\), complementarity gives \(q_i\leq
z_i\), and hence

\[
 \begin{aligned}
 N-1
   &\leq\sum_i ap_iq_i
    \leq\sum_i a(r_i-1)z_i
    \leq a(R-1)Z=bZ.                                     \tag{6}
 \end{aligned}
\]

Ray blocks, if separately included, have zero mixed channel and only
increase \(Z\).  Equation (6) gives

\[
               \nu_{\rm std,slice}\geq
                  \left\lceil{N-1\over b}\right\rceil.    \tag{7}
\]

If \(b\nmid N-1\), the right side of (7) already equals
\(\lceil N/b\rceil\).  It remains to analyze equality when

\[
                              N-1=Lb.                      \tag{8}
\]

## What equality would force

Suppose every selected boundary fiber had \(Z\leq L\).  Equations (6)--(8)
then force \(Z=L\) and equality in every blockwise inequality at every
contact.  As in the symmetric-cone nullity theorem, the integer nullities
are upper semicontinuous; their constant sum makes each \(z_i\) locally,
and hence globally, constant.

Every positive-nullity active block must satisfy

\[
                   r_i=R,\qquad p_i=R-1,\qquad q_i=z_i=1. \tag{9}
\]

Any block with \(z_i=0\) has \(X_i\) interior at every primal contact, so
diagonal complementarity makes \(Y_i\) identically zero on the entire dual
sphere.  Its full slack term vanishes.  An active ray would have positive
nullity but zero curvature and would make (6) strict.  Thus the full slack
reduces to exactly \(L\) active order-\(R\) terms.

The primal support maps have target

\[
 \operatorname{Gr}_{R-1}(\mathbb F^R)
       \cong\mathbb F P^{R-1},\qquad
 \dim_{\mathbb R}\mathbb F P^{R-1}=b.                    \tag{10}
\]

Every partial mixed form has rank \(b\), so the joint support map is a
same-dimensional finite covering

\[
                    S^{Lb}\longrightarrow
                       (\mathbb F P^{R-1})^L.             \tag{11}
\]

If \(L>1\), (11) is impossible.  For real \(R=2\), the target has circle
factors and noncompact universal cover.  In all other cases, pass to the
compact simply connected universal covers; a product of at least two
positive-dimensional closed manifolds has nonzero intermediate mod-two
cohomology, unlike a sphere.

If \(L=1\), the target itself must have sphere universal cover.  Complex
and quaternionic projective spaces have intermediate \(H^2\) and \(H^4\),
respectively, except for
\(\mathbb CP^1=S^2\) and \(\mathbb HP^1=S^4\).  These give the complex and
quaternionic cases in (3).  Every
\(\mathbb RP^{R-1}\) has sphere universal cover, so the real family needs
one more argument.

## An even-quadratic obstruction for real order \(R\geq3\)

Assume \(L=1\), \(\mathbb F=\mathbb R\), and \(R\geq3\).  After exchanging
primal and dual if necessary, the rank-one sheet has support map
\[
                         S^{R-1}\longrightarrow\mathbb {RP}^{R-1}       \tag{12}
\]
equal to the universal double cover, while the other sheet has rank
\(R-1\).  The rank-one matrices over any nonempty projective open set span
\(\mathbb S^R\): a quadratic form that vanishes there vanishes identically.
Choose finitely many points in that open set whose rank-one factors form a
basis of \(\mathbb S^R\).  Pairing the complementary sheet against those
fixed factors gives the affine functions \(1-x\cdot y_\ell\).  Inverting
this fixed basis therefore forces the rank-\((R-1)\) sheet to be one affine
pencil globally:

\[
                 X(x)=C_0+\sum_{j=1}^{R}x_jC_j\succeq0,
                 \qquad \operatorname{rank}X(x)=R-1
                 \quad(x\in S^{R-1}).                    \tag{13}
\]

There are no residual terms: the preceding equality analysis made every
zero-nullity block's dual sheet identically zero.

The spherical average \(C_0\) is positive definite.  Indeed, a vector in
its kernel would lie in every \(\ker X(x)\), while the kernel lines in
(13) sweep all of \(\mathbb {RP}^{R-1}\).  Congruence-normalize \(C_0=I\)
and homogenize:

\[
                         \mathcal L(t,x)=tI+\sum_jx_jA_j. \tag{14}
\]

The irreducible sphere quadric divides its determinant,

\[
       \det\mathcal L(t,x)
          =(t^2-\|x\|^2)P(t,x),                           \tag{15}
\]

for a homogeneous polynomial \(P\) of degree \(R-2\).  At a boundary point
\((1,x)\), rank \(R-1\) gives
\(\operatorname{adj}\mathcal L=\rho(x)k(x)k(x)^T\), where
\(\rho(x)>0\) and \(k(x)\) is a unit kernel vector.  Differentiating (15)
and using \(C_0=I\) yields

\[
 \rho=2P(1,x),\qquad
 \rho\,k(x)^TA_jk(x)=-2x_jP(1,x),
\]

and therefore

\[
                         x_j=-k(x)^TA_jk(x).              \tag{16}
\]

Because \(R-1\geq2\), the kernel-line map (12) lifts to a diffeomorphism
\(h:S^{R-1}\to S^{R-1}\); choose \(k(x)=h(x)\).  Define

\[
        \Phi:S^{R-1}\to\mathbb R^R,\qquad
        \Phi_j(u)=-u^TA_ju.                               \tag{17}
\]

Equation (16) says \(\Phi\circ h=\operatorname{id}_{S^{R-1}}\).  But
\(\Phi(-u)=\Phi(u)\), whereas the diffeomorphism \(h\) is onto.  If
\(h(x)=u\) and \(h(x')=-u\), then (17) gives
\(x=\Phi(u)=\Phi(-u)=x'\), contradicting
\(u=h(x)\ne h(x')=-u\).  Hence the real sole-factor equality is impossible
for every \(R\geq3\).

It follows that, outside the three order-two cases (3), not all boundary
fibers can have \(Z\leq L\).  Some boundary fiber has integer
\(Z\geq L+1\), and (5) gives

\[
                         \nu_{\rm std,slice}\geq
                            \left\lceil{N\over b}\right\rceil.           \tag{18}
\]

## Matching construction

One order-\(R\) Hermitian block can encode any real coordinate group of
size \(g\leq b=a(R-1)\).  Embed the group vector as
\(w_G\) in a fixed real \(g\)-dimensional subspace of
\(\mathbb F^{R-1}\), and impose

\[
                 \begin{pmatrix}s_G&w_G^*\\w_G&I_{R-1}\end{pmatrix}
                    \succeq0,\qquad \sum_Gs_G=1.           \tag{19}
\]

The Schur complement and Jordan determinant are

\[
                 s_G\geq\|w_G\|^2,\qquad
 \det\begin{pmatrix}s_G&w_G^*\\w_G&I\end{pmatrix}
                    =s_G-\|w_G\|^2.                       \tag{20}
\]

Partition \(N\) coordinates into \(\lceil N/b\rceil\) groups.  The
restricted standard product barrier is the sum of one-parameter
paraboloid barriers

\[
                         -\sum_G\log(s_G-\|w_G\|^2),       \tag{21}
\]

and its exact parameter after \(\sum_Gs_G=1\) is the number of groups.
If \(N\leq b\), this gives parameter one.  In the three exceptional cases
(3), the rank-two Hermitian cone is a Lorentz cone and its direct ball
slice also has parameter one.  These constructions prove every upper bound
in (2).

## Scope and literature boundary

The proof assumes an actual strictly feasible affine lift whose globally
\(C^1\) selected primal boundary fibers lie in the closure of the affine
slice carrying the barrier.  A bare slack factorization does not define a
restricted barrier.  The result allows arbitrary affine equations and
projections but not the loss of the global factor selections.

The Hermitian support-map differential and projective-space classification
are developed in
[Saturated PSD factors induce Grassmannian
submersions](2026-09-04-psd-support-grassmannian-submersion.md).
The determinant-nullity lemma and standard-slice parameter convention are
in
[Exact standard-slice barrier frontier for capped symmetric-cone ball
lifts](2026-09-04-symmetric-cone-standard-slice-barrier-frontier.md).

Kummer's [*Two results on the size of spectrahedral
descriptions*](https://arxiv.org/abs/1506.07699), Theorem 2.1, gives
matrix-size lower bounds for a **direct real spectrahedral description** of
a quadratic body, including \(r\geq N/2\) for \(B_2^N\) and sharper bounds
at powers of two.  That result is adjacent but does not treat projected
products of Hermitian cones or the restricted standard-barrier parameter
optimized here.

The even-quadratic inverse obstruction (16)--(17) appears to be a new
ball-slack consequence of combining affine PSD pencils with the universal
projective support cover.  A targeted search found no statement of this
standard-slice frontier or its equality classification.  Priority remains
subject to specialist review.

An independent hostile audit checked the piecewise arithmetic, every
equality case in (6), zero-nullity and ray factors, the projective-product
covering obstruction, the real affine-pencil reconstruction, the adjugate
differentiation in (16), and the real/complex/quaternionic Schur
constructions.  It found no correction.  A second independent hostile audit
rechecked the field-specific channel dimensions, covering cases, global
affine-pencil reconstruction, even-quadratic contradiction, and
quaternionic determinant construction.  It also passed without a
substantive correction.

## Audit checklist

- Verify the coefficient \(a(R-1)\) in (6) over all three division
  algebras and the equality ranks in (9).
- Check that zero-nullity blocks really vanish from the full two-variable
  slack after diagonal complementarity.
- Check every covering case in (11), including real \(R=2\).
- Verify that the rank-one sheet spans all Hermitian matrices and forces
  the complementary sheet affine when \(L=1\).
- Check divisibility of the determinant by the homogeneous sphere quadric,
  the adjugate derivative in (16), and existence/surjectivity of the lifted
  kernel vector \(h\).
- Verify the quaternionic Schur complement and Jordan determinant in
  (19)--(20).
- Preserve the standard-restricted versus custom-barrier distinction.
