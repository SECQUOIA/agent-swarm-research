# Projective rank-one contact kernels force Euclidean embeddings

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High under the explicit nowhere-zero factor hypothesis

## Main result

Let \(r\geq3\), put \(n=r-1\), and identify a point of
\(M=\mathbb{RP}^{n}\) with the rank-one projector \(P_x=xx^T\), where
\(x\in S^n\). Consider the strict-diagonal kernel

\[
             \kappa([x],[y])=1-\operatorname{tr}(P_xP_y)
                            =1-(x^Ty)^2.                    \tag{1}
\]

Suppose (1) has a globally labelled \(C^1\) factorization by \(L\)
three-dimensional Lorentz cones,

\[
 \kappa(u,v)=\sum_{j=1}^L\langle A_j(u),B_j(v)\rangle,
 \qquad A_j(u),B_j(u)\in Q_3\setminus\{0\}.                \tag{2}
\]

Then the Lorentz phases define a \(C^1\) embedding

\[
                         \mathbb{RP}^{n}\hookrightarrow\mathbb R^L.    \tag{3}
\]

Consequently

\[
 L\geq
 \begin{cases}
  r,&r\text{ is a power of two},\\
  2^{\lceil\log_2r\rceil}-1,&r\text{ is not a power of two}.
 \end{cases}                                                \tag{4}
\]

For the infinite family \(r=2^t+1\), \(t\geq1\), this becomes

\[
                             L\geq2r-3=2n-1.                \tag{5}
\]

Thus the projective contact topology can almost double the elementary
local rank bound \(L\geq n\). The conclusion is conditional on every
selected factor being nowhere zero. It is a theorem about the restricted
rank-one kernel (1), not a new second-order-cone representation or
nonrepresentation theorem for the full PSD cone or spectraplex.

For \(r=3\), the nowhere-zero fixed-contact count is exact:

\[
                              L_{\rm nz}=4.                  \tag{6}
\]

The obstruction tensorizes. For \(k\geq1\), positive weights
\(\lambda_a\), and

\[
 M_k=(\mathbb{RP}^{n})^k,\qquad
 \kappa_k(u,v)=\sum_{a=1}^k\lambda_a
       \bigl(1-(x_a^Ty_a)^2\bigr),                          \tag{6a}
\]

every nowhere-zero globally \(C^1\) \(Q_3^L\) factorization satisfies

\[
 L\geq\max\left\{kn+1, k\bigl(2^{\lceil\log_2r\rceil}-1\bigr)\right\}.
                                                                    \tag{6b}
\]

In particular, when \(r=2^t+1\),

\[
                             L\geq k(2r-3).                 \tag{6c}
\]

This is additive in the number of projective blocks, in sharp contrast to
the ordinary Euclidean embedding obstruction for a product of spheres.
Concatenating the single-block construction in Section 3 gives the finite
nowhere-zero upper bound

\[
              L\leq k\left({r(r+1)\over2}-2\right).         \tag{6d}
\]

## 1. Phase embedding

The kernel is nonnegative and vanishes exactly when \([x]=[y]\). Its
negative mixed derivative on the diagonal is twice the standard quotient
metric on \(\mathbb{RP}^{n}\), hence is positive definite.

Diagonal complementarity and the nowhere-zero hypothesis give unique
\(C^1\) normalizations

\[
 A_j(u)=a_j(u)(1,p_j(u)),\qquad
 B_j(u)=b_j(u)(1,-p_j(u)),                                  \tag{7}
\]

where \(a_j,b_j>0\) and \(p_j:M\to S^1\). Since

\[
 H^1(\mathbb{RP}^{n};\mathbb Z)=0\qquad(n\geq2),          \tag{8}
\]

every phase lifts to a real-valued \(C^1\) function,

\[
                     p_j=(\cos\theta_j,\sin\theta_j).
\]

The exact mixed derivative calculation gives

\[
  2g=\sum_{j=1}^L a_jb_j\,d\theta_j\otimes d\theta_j.      \tag{9}
\]

Thus \(\Theta=(\theta_1,\ldots,\theta_L):M\to\mathbb R^L\)
is an immersion. If \(\Theta(u)=\Theta(v)\), then every phase agrees, so
every summand in (2) is zero by (7). Equation (1) then gives \(u=v\).
Hence \(\Theta\) is injective. A compact injective immersion into a
Hausdorff manifold is an embedding, proving (3).

The integral coefficient in (8) matters. Although
\(H^1(\mathbb{RP}^{n};\mathbb F_2)\neq0\), maps to \(S^1=K(\mathbb Z,1)\)
are classified by integral \(H^1\), which vanishes because
\(H_1(\mathbb{RP}^{n};\mathbb Z)=\mathbb Z_2\).

## 2. The Stiefel--Whitney staircase

Suppose \(\mathbb{RP}^{n}\) has a \(C^1\) embedding in \(\mathbb R^L\),
and let \(\nu\) be its normal bundle of rank \(c=L-n\). If \(a\) generates
\(H^1(\mathbb{RP}^{n};\mathbb F_2)\), the stable tangent identity

\[
                  T\mathbb{RP}^{n}\oplus\varepsilon^1
                    \cong(n+1)\gamma^1
\]

gives

\[
                    w(\nu)=(1+a)^{-(n+1)}
                     =\sum_{j=0}^n {n+j\choose j}a^j.       \tag{10}
\]

Lucas's parity criterion says

\[
                    {n+j\choose j}\equiv1\pmod2
                    \quad\Longleftrightarrow\quad n\mathbin{\&}j=0.    \tag{11}
\]

Let \(m=\lceil\log_2(n+1)\rceil=\lceil\log_2r\rceil\). The largest
\(0\leq j\leq n\) satisfying (11) is

\[
                         j_*=2^m-1-n=2^m-r.                 \tag{12}
\]

Indeed, \(j_*\) is the binary complement of \(n\) in its first \(m\)
bits, and any use of the next bit exceeds \(n\). Since a rank-\(c\) bundle
has \(w_j=0\) for \(j>c\), (10)--(12) give

\[
                         L=n+c\geq n+j_*=2^m-1.             \tag{13}
\]

Independently, no compact \(n\)-manifold embeds in \(\mathbb R^n\), so
\(L\geq n+1=r\). Combining this with (13) proves (4). When
\(n=2^t\), equivalently \(r=2^t+1\), equation (13) is (5).

For \(n=2\), the characteristic-class bound gives only \(L\geq3\), but
\(\mathbb{RP}^2\) cannot embed in \(\mathbb R^3\): every compact embedded
hypersurface in Euclidean space is two-sided and orientable, whereas
\(\mathbb{RP}^2\) is not. Thus (3) gives \(L\geq4\) when \(r=3\).

For completeness, apply the same calculation to (6a). The integral group
\(H^1(M_k;\mathbb Z)\) vanishes, so the joint phases again lift and embed
\(M_k\) in \(\mathbb R^L\). If \(a_\alpha\) is the degree-one mod-two
generator of the \(\alpha\)-th factor, the stable normal class is

\[
 w(\nu)=\prod_{\alpha=1}^k(1+a_\alpha)^{-(n+1)}.            \tag{13a}
\]

The monomial \(\prod_\alpha a_\alpha^{j_*}\) has nonzero coefficient and
degree \(kj_*\). Hence the normal rank is at least \(kj_*\), so
\(L\geq kn+kj_*=k(2^m-1)\). Combining this with the compact-manifold bound
\(L\geq kn+1\) proves (6b).

## 3. A finite smooth upper bound

Let

\[
                 D=\dim\operatorname{Sym}_0(r)
                   ={r(r+1)\over2}-1
\]

and use the normalized Veronese embedding

\[
 X([x])=\sqrt{r\over r-1}\left(xx^T-{I\over r}\right)
                  \in S^{D-1}.                             \tag{14}
\]

Then

\[
        \kappa([x],[y])={r-1\over r}\bigl(1-X([x])^TX([y])\bigr).        \tag{15}
\]

The compact image \(X(M)\) is a proper subset of \(S^{D-1}\). Choose a
point of the sphere outside the image and apply stereographic projection.
The standard chord identity and scalar paraboloid maps into \(Q_3\) give a
globally \(C^\infty\), nowhere-zero factorization with

\[
                         L=D-1={r(r+1)\over2}-2.             \tag{16}
\]

Explicitly, if \(c(u)=1-q^TX(u)\), the stereographic coordinates are
\(F=(f_1,\ldots,f_{D-1})\), use the scalar paraboloid maps

\[
 U(t)=\left({1+t^2\over2},{1-t^2\over2},t\right),\qquad
 V(t)=\left({1+t^2\over2},-{1-t^2\over2},-t\right),
\]

and take

\[
 A_i(u)=\sqrt{r-1\over r}\,c(u)U(f_i(u)),\qquad
 B_i(v)=\sqrt{r-1\over r}\,c(v)V(f_i(v)).                  \tag{16a}
\]

The identities
\(1-X(u)^TX(v)=c(u)c(v)\|F(u)-F(v)\|^2/2\) and
\(\langle U(t),V(w)\rangle=(t-w)^2/2\) verify the constant in (15).

For \(r=3\), (16) gives \(L=4\), matching the projective-plane
nonembedding lower bound and proving (6).

## 4. Literature boundary

The tangent-bundle identity and Stiefel--Whitney obstruction for real
projective space are classical. The parity step (11) is Lucas's theorem.
Fawzi proved that \(\mathbb S_+^3\) has no finite second-order-cone lift in
[*On representing the positive semidefinite cone using the second-order
cone*](https://doi.org/10.1007/s10107-018-1233-0). That theorem concerns a
full cone representation and is strictly stronger in a different scope;
it neither implies nor is implied by the finite, restricted contact-kernel
count studied here.

A targeted search found the classical embedding and nonembedding theory of
real projective spaces and the SOC nonrepresentability literature, but no
source deriving a projective-space embedding from globally smooth,
nowhere-zero Lorentz phases of (1). The phase-to-embedding bridge and its
conditional contact-factor lower bound therefore appear new, subject to
specialist review.

## Audit record

An independent hostile audit checked the integral \(H^1\) phase lift, the
mixed-metric sign and factor two, injectivity of the joint phase map, the
inverse Stiefel--Whitney series, Lucas parity and the maximal index
\(j_*=2^m-1-n\), the projective-plane nonembedding, the normalized
Veronese constants, the stereographic channel count, and the distinction
from full-cone SOC nonrepresentability. No substantive defect was found.
The product formula (6b) was separately audited using the Kunneth
cohomology ring and the external product of the inverse normal classes.
