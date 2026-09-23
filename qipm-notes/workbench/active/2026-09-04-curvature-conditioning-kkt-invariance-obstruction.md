# Why factor-conditioning blowup is not yet a QIPM condition-number lower bound

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Summary

The conditioned approximate-curvature theorem proves that an under-capacity
family must lose a Euclidean factor regularity bound such as

\[
        {L\sqrt H\over\mu}=\Omega(\epsilon^{-1/2}),               \tag{1}
\]

up to the stated block-count and remainder factors.  This does not yet give
a QIPM Newton/KKT condition-number lower bound.  The quantities in (1) are
not invariant under cone-coordinate isomorphisms, whereas the
barrier-scaled Newton Schur complement is invariant.

A two-coordinate Lorentz boost makes the mismatch explicit.  It can send
both vectors in a complementary primal/dual boundary pair to arbitrarily
small Euclidean norm, while leaving the standard-barrier scaled Schur
complement exactly unchanged.  The boost is sparse, so this is not merely a
dense-coordinate pathology.  Any valid QIPM tradeoff needs an intrinsic
condition measure, or an explicit normalization/access model that forbids
this reparameterization.

## Barrier-scaled Schur invariance

Consider a conic equality system

\[
                  Az=b,\qquad z\in K,                             \tag{2}
\]

with a logarithmically homogeneous barrier \(F\) on \(K\).  Let
\(G\) be a linear cone automorphism and assume

\[
                  F(Gz)=F(z)+c_G                                  \tag{3}
\]

for a constant \(c_G\).  In the new coordinates

\[
 z'=Gz,qquad A'=AG^{-1},                                         \tag{4}
\]

the barrier Hessians satisfy

\[
 H' :=\nabla^2F(z')=G^{-T}HG^{-1},qquad H=\nabla^2F(z).         \tag{5}
\]

Consequently the primal Newton Schur complement is exactly invariant:

\[
 \boxed{
 A'(H')^{-1}(A')^T
 =AG^{-1}(GH^{-1}G^T)G^{-T}A^T
 =AH^{-1}A^T.}                                                    \tag{6}
\]

The same change sends a linear objective to \(c'=G^{-T}c\), preserves
primal residuals, and is an isometry between the corresponding barrier
local norms.  Thus an algorithm or preconditioner formulated in the local
barrier metric sees the same Newton geometry.  A raw Euclidean Hessian or
KKT condition number need not be invariant, but that only records the
chosen coordinates.

## Sparse Lorentz boost

Let

\[
 Q_m=\{(x_0,x_1,x_\perp):x_0\geq
       \sqrt{x_1^2+\|x_\perp\|_2^2}\},\qquad m\geq3,              \tag{7}
\]

and take the complementary boundary rays

\[
                 a=e_0+e_1,qquad b=e_0-e_1.                     \tag{8}
\]

For \(\lambda>0\), define \(G_\lambda\) to be the identity on
\(\operatorname{span}\{e_2,\ldots,e_{m-1}\}\) and, on
\(\operatorname{span}\{e_0,e_1\}\),

\[
 G_\lambda={1\over2}
 \begin{pmatrix}
  \lambda+\lambda^{-1}&\lambda-\lambda^{-1}\\
  \lambda-\lambda^{-1}&\lambda+\lambda^{-1}
 \end{pmatrix}.                                                    \tag{9}
\]

This symmetric matrix preserves
\(x_0^2-x_1^2-\|x_\perp\|^2\) and the future sheet, so it is an automorphism
of \(Q_m\).  It obeys

\[
 G_\lambda a=\lambda a,qquad G_\lambda b=\lambda^{-1}b.         \tag{10}
\]

Under a cone-coordinate change, primal and dual factors transform as

\[
                 A\mapsto G_\lambda A,qquad
                 B\mapsto G_\lambda^{-T}B.                       \tag{11}
\]

Since \(G_\lambda\) is symmetric, (10) gives

\[
 G_\lambda a=\lambda a,qquad
 G_\lambda^{-T}b=G_\lambda^{-1}b=\lambda b.                     \tag{12}
\]

Thus both Euclidean base-factor norms are multiplied by \(\lambda\), and
can be made arbitrarily small.  Pairings are unchanged:

\[
 \langle G_\lambda A,G_\lambda^{-T}B\rangle
 =\langle A,B\rangle.                                             \tag{13}
\]

The boost changes only two coordinates and is the identity on all transverse
directions.  Such factor maps occur explicitly: for transverse
\(u,v\in\mathbb R^{m-2}\), take

\[
 A(u)=(\sqrt{1+\|u\|^2},1,u),\qquad
 B(v)=(\sqrt{1+\|v\|^2},-1,-v).                                  \tag{13a}
\]

They lie on the primal and dual Lorentz boundaries, have the base values
(8), and have transverse isometric derivatives. Moreover,

\[
 \langle A(u),B(v)\rangle
 =\sqrt{1+\|u\|^2}\sqrt{1+\|v\|^2}-1-u^Tv\geq0,
\]

by Cauchy--Schwarz, with equality when \(u=v\). Their Euclidean
first-derivative norms are unchanged by the boost while the lower base-norm
bound \(\mu\) scales by \(\lambda\).  Contracted
second-derivative quantities of the form
\(\langle D^2A[h,h],b\rangle\) are also invariant under (11).  Hence the
ratio in (1) can be inflated by \(\lambda^{-1}\) without changing a single
slack value or intrinsic barrier-scaled Newton system.

The standard Lorentz barrier

\[
                 F(x)=-\log(x_0^2-x_1^2-\|x_\perp\|^2)           \tag{14}
\]

satisfies (3) with \(c_G=0\), so (6) applies exactly.  The contrast with a
raw Euclidean condition number is visible even at \(z=e_0\):
\(\nabla^2F(e_0)=2I\), while

\[
 \nabla^2F(G_\lambda e_0)=2G_\lambda^{-2}                        \tag{15}
\]

has condition number \(\lambda^{-4}\) for \(0<\lambda<1\).  This apparent
ill-conditioning disappears under the inverse coordinate map and leaves
the Schur complement (6) unchanged.

The full augmented KKT matrix is not literally spectrally invariant in a
raw Euclidean norm. It transforms by congruence:

\[
 \begin{pmatrix}H'&(A')^T\\A'&0\end{pmatrix}
 =
 \begin{pmatrix}G^{-T}&0\\0&I\end{pmatrix}
 \begin{pmatrix}H&A^T\\A&0\end{pmatrix}
 \begin{pmatrix}G^{-1}&0\\0&I\end{pmatrix}.          \tag{16}
\]

Thus an unscaled augmented-system solver can see a different Euclidean
condition number. Likewise, \(A'=AG^{-1}\) mixes the two boosted columns
and can change coefficient magnitudes, row norms, block-encoding
normalization, and data-oracle costs. The boost preserves sparsity only up
to a constant-factor change in those two columns; sparsity alone does not
make the two quantum access models equally costly.

## Consequence and remaining route

Equation (12) is a rigorous obstruction to reading the Euclidean
factor-conditioning contrapositive as an intrinsic QIPM cost.  It does not
show that every under-capacity approximate lift has a well-conditioned
QIPM realization, nor that a representation-specific QLSA has unchanged
complexity. It shows that the present quantities cannot by themselves
lower-bound the barrier-scaled Schur condition number, and that any
full-KKT or access-cost conclusion must charge the coordinate
representation explicitly.

Two routes remain legitimate:

1. fix a representation/access normalization and prove that the permitted
   preconditioners cannot undo its degeneration; or
2. replace \(\mu,L,H\) by quantities optimized over cone automorphisms and
   measured in a barrier/projective metric, then relate those quantities to
   a barrier-scaled Schur or full-KKT spectrum.

The boundary factors in the curvature theorem do not themselves carry a
finite barrier Hessian, so the second route needs a controlled approach from
the central path.  No such intrinsic comparison is proved here.

## Audit record

The independent audit verified the boost eigenvectors, preservation of the
Lorentz form and future sheet, primal/dual inverse-transpose transformation,
barrier-Hessian covariance, exact Schur invariance, and the
\(\lambda^{-4}\) raw Hessian condition number. It also corrected the sign
in (13a), so the displayed maps form a genuine nonnegative kernel with zero
diagonal. The audit added the full-KKT congruence and the
sparsity/coefficient/access caveats above; these prevent the obstruction
from being overstated as invariance of every representation-specific QIPM
cost.
