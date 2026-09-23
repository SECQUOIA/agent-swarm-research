# SQ dequantization for generalized-power-cone Newton systems

Status: Proved conditional one-step theorem; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and reduction; moderate on apparent novelty of the SQ consequence

## Result

Consider a product of \(L\) high-dimensional generalized power cones

\[
 \mathcal G_{\alpha,m,n}
 =\left\{(x,z)\in\mathbb R_+^m\times\mathbb R^n:
       \prod_{i=1}^m x_i^{\alpha_i}\geq\|z\|_2
   \right\},
 \qquad \alpha_i>0,\quad\sum_i\alpha_i=1.
\]

For the standard \((m+1)\)-parameter generalized-power barrier, the inverse
Hessian is a positive diagonal matrix plus a rank-two correction, regardless
of \(m+n\).  More strongly, if

\[
 \lambda
 =\frac{\prod_i x_i^{2\alpha_i}}
        {\prod_i x_i^{2\alpha_i}-\|z\|^2}\geq1,
\]

then the inverse Hessian and its diagonal base are spectrally comparable
within a factor \(4\lambda\).  Consequently, the reduced Newton matrix for
\(L\) such blocks is a sparse matrix plus a rank-at-most-\(2L\) correction
with a stable small Woodbury core.

Under explicit SQ access to the current cone vectors and Newton right-hand
side, and with the block geometric means supplied as barrier-oracle scalars,
this gives exact squared-coordinate sampling from a relative-
\(\epsilon\) approximate reduced Newton direction in expected

\[
 \boxed{
 d^{O(\sqrt{\kappa_S}\log(L\Lambda\kappa_S/\epsilon))}
 \operatorname{poly}
 (L,\Lambda,\kappa_S,\epsilon^{-1},\log(1/\delta_f)) }
                                                               \tag{1}
\]

queries and arithmetic operations.  Here \(d\) bounds row and column
sparsity of the equality matrix, 
\(\Lambda=\max_\ell\lambda_\ell\), \(S\) is the sparse diagonal-base
normal matrix, 
\(\kappa_S=\kappa_2(S)\), and \(1-\delta_f\) is the success probability.
The cost is independent of the dimensions of the cone blocks.

This is a one-Newton-solve result, not an end-to-end classical IPM.  It does
not show how to maintain SQ access to all iterates or keep
\(\Lambda,\kappa_S\) bounded along a full central path.

## Exact barrier Hessian

For one block, put

\[
 p=\prod_{i=1}^m x_i^{2\alpha_i},\qquad
 r=\|z\|,\qquad
 \zeta=p-r^2,\qquad
 \lambda=\frac p\zeta,
\]

and use the Roy--Xiao barrier

\[
 F(x,z)=-\log(p-\|z\|^2)
        -\sum_{i=1}^m(1-\alpha_i)\log x_i.                  \tag{2}
\]

Let

\[
 a_i=\frac{\alpha_i}{x_i},\qquad
 k_i=1+(2\lambda-1)\alpha_i,
\]

embed \(a\) and \(z\) in their two disjoint coordinate groups, and define

\[
 D_0=\operatorname{Diag}\left(
       k_1x_1^{-2},\ldots,k_mx_m^{-2},\frac2\zeta I_n
      \right).
\]

Direct differentiation gives

\[
 \boxed{
 \begin{aligned}
 \nabla^2F
  =D_0
  &+4\lambda(\lambda-1)\bar a\bar a^T
   -\frac{4\lambda}{\zeta}
       (\bar a\bar z^T+\bar z\bar a^T)\\
  &+\frac4{\zeta^2}\bar z\bar z^T .
 \end{aligned}}                                               \tag{3}
\]

Thus \(H_F=D_0+UCU^T\) with two columns in \(U\), and the Woodbury identity
immediately gives

\[
 \boxed{H_F^{-1}=D_0^{-1}+\text{a rank-at-most-two correction}.} \tag{4}
\]

For reference,

\[
 D_0^{-1}\bar a
 =\left(\frac{\alpha_i x_i}{k_i}\right)_{i=1}^m\oplus0,
 \qquad
 D_0^{-1}\bar z=0\oplus\frac\zeta2z.                         \tag{5}
\]

Hence the inverse correction directions are formed from the current \(x\)
and \(z\), rather than inverse-coordinate vectors.

## Dimension-free diagonal comparison

The normalized Hessian \(D_0^{-1/2}H_FD_0^{-1/2}\) is the identity outside
the span of \(D_0^{-1/2}\bar a\) and \(D_0^{-1/2}\bar z\).  Define

\[
 A_\alpha(\lambda)
 =\sum_{i=1}^m\frac{\alpha_i^2}{k_i}.
\]

On normalized versions of the two orthogonal vectors, the Hessian is

\[
 Q_{\alpha,\lambda}=
 \begin{pmatrix}
  1+4\lambda(\lambda-1)A_\alpha
  &-4\lambda\sqrt{\dfrac{A_\alpha(\lambda-1)}2}\\[6pt]
  -4\lambda\sqrt{\dfrac{A_\alpha(\lambda-1)}2}
  &2\lambda-1
 \end{pmatrix}.                                             \tag{6}
\]

Since

\[
 k_i=1+(2\lambda-1)\alpha_i\geq2\lambda\alpha_i,
\]

we have

\[
 A_\alpha(\lambda)\leq\frac1{2\lambda}.
\]

The trace and determinant of (6) therefore satisfy

\[
 \operatorname{tr}Q_{\alpha,\lambda}
 =2\lambda+4\lambda(\lambda-1)A_\alpha\leq4\lambda,
\]

\[
 \det Q_{\alpha,\lambda}
 =2\lambda-1-4\lambda(\lambda-1)A_\alpha\geq1.             \tag{7}
\]

Both eigenvalues are positive.  Equation (7) and the trace bound imply

\[
 \frac1{4\lambda}I\preceq Q_{\alpha,\lambda}
 \preceq4\lambda I.
\]

Together with the untouched orthogonal complement, this proves

\[
 \boxed{
 \frac1{4\lambda}D_0\preceq H_F\preceq4\lambda D_0,
 \qquad
 \frac1{4\lambda}D_0^{-1}\preceq H_F^{-1}
 \preceq4\lambda D_0^{-1}.}                                \tag{8}
\]

The bound is independent of \(m,n\), and the distribution of the power
weights \(\alpha\).  It also quantifies the
only relevant radial degeneration: 
\(\lambda=p/(p-r^2)\) diverges as the point approaches the curved cone
boundary.  Arbitrary imbalance among the positive coordinates is absorbed
by the diagonal base.

## Sparse-plus-low-rank reduced Newton system

For a product of \(L\) blocks, put

\[
 \mathcal D=\bigoplus_{\ell=1}^L D_{0,\ell}^{-1}.
\]

Equations (4) and (8) permit a signed factorization

\[
 H^{-1}=\mathcal D+RJR^T,
 \qquad \operatorname{rank}R\leq2L,                         \tag{9}
\]

where \(J\) is diagonal with entries in 
\(\{+1,-1\}\).  The two-dimensional eigendecomposition used to obtain each
block of \(R\) also gives

\[
 \left|\mathcal D^{-1/2}(H^{-1}-\mathcal D)
                    \mathcal D^{-1/2}\right|
 \preceq4\Lambda I.                                        \tag{10}
\]

Let \(A\) have full row rank and at most \(d\) nonzeros per row and column.
The reduced normal matrix is

\[
 N=AH^{-1}A^T=S+(AR)J(AR)^T,
 \qquad S=A\mathcal DA^T.                                  \tag{11}
\]

The base \(S\) is at most \(d^2\)-sparse, and (8) implies

\[
 \boxed{
 \frac1{4\Lambda}S\preceq N\preceq4\Lambda S.}            \tag{12}
\]

After normalizing by \(S\), (10) bounds the unsigned correction norm by
\(4\Lambda\).  Thus the signed Woodbury core has dimension at most \(2L\)
and condition number 
\(O(\Lambda^3)\), by the same identity used for Lorentz cones:

\[
 (J+W^TW)^{-1}
 =J-JW^T(I+WJW^T)^{-1}WJ.                                  \tag{13}
\]

In particular, indefinite cancellation introduces no unlisted stability
parameter when \(\Lambda\) is bounded.

## SQ access and algorithm

Assume SQ/query/norm access to every current \(x_\ell,z_\ell\), the public
power-weight vectors \(\alpha_\ell\), and to the Newton right-hand side \(b\),
queryable barrier scalars
\(p_\ell,\zeta_\ell,\lambda_\ell\), and public spectral bounds for \(S\).
The normalized two-dimensional update subspace in (6) is especially simple:

- the positive-coordinate direction has entries proportional to
  \(\alpha_i/\sqrt{k_i}\); and
- the radial direction is \(z/\|z\|\).

The first direction can be sampled from SQ access to \(\alpha\) by accepting
an \(\alpha_i^2\)-sample with probability \(1/k_i\); because
\(1\leq k_i\leq2\lambda\), the overhead is at most \(2\lambda\).
The scalar \(A_\alpha\) is estimated by the same sampler.  The required
\(2\times2\) eigenproblems depend only on \(A_\alpha,\lambda\).  Their
normalized eigenvectors \(e_j\) are linear combinations of the two
orthogonally supported directions above, so they have SQ access without
forming the potentially ill-conditioned coordinatewise product
\((\alpha_i x_i/k_i)_i\).

To justify access after applying the equality matrix, put

\[
 C=A\mathcal D^{1/2},\qquad S=CC^T.
\]

If \(\theta_j,e_j\) is a nonzero eigenpair of the normalized inverse
correction in (10), the corresponding reduced correction column is
\(\sqrt{|\theta_j|}\,Ce_j\).  Let

\[
 \beta_j=\|\Pi_{\operatorname{row}(C)}e_j\|.
\]

The nonzero singular values of \(C\) are the square roots of the eigenvalues
of \(S\).  Hence the rectangular sparse-transform sampler obtains
\(SQ(Ce_j)\) in expected

\[
 O(d\kappa_S/\beta_j^2)
\]

raw trials.  No unlisted visibility promise is needed for an approximate
solve: in whitened coordinates,

\[
 \|S^{-1/2}Ce_j\|=\beta_j.
\]

Discarding all columns with \(\beta_j<\tau\) changes the unsigned normalized
correction by at most \(8L\Lambda\tau^2\), because there are at most \(2L\)
columns and \(|\theta_j|\leq4\Lambda\).  Taking
\(\tau^2=\eta/(8L\Lambda)\), and capping the rejection sampler at the
corresponding polynomial number of trials, either supplies the required SQ
column or discards it within the perturbation budget.  Rejection rates also
supply the needed approximate column norms.  This is the step that prevents
a nearly-null \(Ce_j\) from introducing a hidden dimension-dependent access
parameter.

When \(z=0\), so that \(\lambda=1\), the normalized radial direction is
undefined but its correction coefficient is zero; the direction is simply
omitted.

Choose a Chebyshev polynomial \(P\) satisfying

\[
 \|I-SP\|\leq\eta,
 \qquad
 \deg P=O(\sqrt{\kappa_S}\log(1/\eta)).                    \tag{14}
\]

Sparse-walk expansion supplies local row and column access to \(P\).  Estimate
the at-most-\(2L\)-dimensional Woodbury Gram matrix and right-hand side with
unbiased SQ inner-product estimators, solve the small system classically, and
form the resulting linear combination of \(Pb\) and the corrected columns.
Equations (10)--(13) make all perturbation and rejection costs polynomial in
\(L,\Lambda,\kappa_S\).

The raw sparse-transform mixture construction then samples exactly from the
squared coordinates of the fixed approximate vector in ideal real
arithmetic, without requiring exact component norms.  Taking

\[
 \eta=\epsilon/\operatorname{poly}(L,\Lambda,\kappa_S)
\]

gives (1), a coordinate oracle, and relative Euclidean error at most
\(\epsilon\).  As in the Lorentz theorem, an exact norm oracle is not obtained;
the norm can be estimated from rejection rates.

The scalar-access assumption is substantive.  SQ access to \(x\) alone does
not reveal the exact geometric mean
\(p=\prod_i x_i^{2\alpha_i}\) in dimension-independent time.  It can be
estimated by uniformly sampling \(\log x_i\) when a bounded log-range is
promised in the uniform-weight case, or by sampling according to
\(\alpha_i\) with the corresponding weight-access oracle.  The resulting
precision cost must be included in the polynomial factor.  Without either
such a range promise or a maintained barrier-oracle scalar, exact acquisition
can cost \(\Omega(m)\), eliminating the claimed dimension independence.

The access contract is stronger than ordinary \(SQ(x,z)\) because it also
grants the barrier scalars.  A comparison with a quantum Newton solver is
matched only if that solver is granted the analogous scalar oracles.
Constructing such a scalar data structure from an explicit iterate may itself
cost linear time; that setup cost is outside the one-solve oracle bound (1).

The last statement already has a direct parity witness for uniform weights.
Group \(m=2M\) positive
coordinates into pairs.  Choose public positive constants \(a,b,c,d\) with

\[
 a^2+b^2=c^2+d^2,\qquad ab\ne cd,
\]

and encode a hidden bit \(h_j\) by setting pair \(j\) to \((a,b)\) or
\((c,d)\).  The SQ norm is the same for every bit string, and an SQ sample
first chooses a uniformly random pair; its within-pair outcome can be
simulated with one query to that pair's bit.  On the other hand,

\[
 \prod_{i=1}^{2M}x_i=(ab)^{M-|h|}(cd)^{|h|},
\]

so exact knowledge of \(p\) determines \(|h|\), and therefore its parity.
The randomized parity query lower bound gives \(\Omega(M)=\Omega(m)\), even
with the full SQ interface.  Thus the barrier-scalar oracle cannot silently
be derived from ordinary SQ access.

The obstruction also applies to constant relative accuracy when no log-range
bound is imposed.  Take
\((a,b)=(\sqrt{1-e^{-2\gamma M}},e^{-\gamma M})\) for a fixed
\(\gamma>0\), and
\((c,d)=(2^{-1/2},2^{-1/2})\).  Adjacent Hamming weights then change
\(p=(\prod_i x_i)^{1/M}\) by a constant factor asymptotic to \(e^\gamma\).
A sufficiently accurate constant-relative estimate again determines
\(|h|\) and its parity, while the SQ norm remains public and constant.
The price is precisely the excluded \(\Theta(M)\) log-coordinate range.

## Exponential-cone boundary

The ordinary power cone and exponential cone are three-dimensional.  Any
inverse Hessian for one such block is diagonal plus a correction of rank at
most three for the trivial reason that the whole block has dimension three.
For a product of \(L\) ordinary blocks, the correction rank is \(O(L)\), so
there is no few-large-block conclusion when \(L\) grows with the input.

The high-dimensional logarithm cone

\[
 \operatorname{cl}\left\{(u,v,w):v>0,\ w>0,
 u\leq v\sum_i\log(w_i/v)\right\}
\]

is a genuine aggregated exponential-cone analogue.  Its standard barrier

\[
 -\log\left(v\sum_i\log(w_i/v)-u\right)
 -\log v-\sum_i\log w_i
\]

has a diagonal-plus-rank-at-most-three Hessian: writing
\(s=v\sum_i\log(w_i/v)-u\), both 
\((\nabla s)(\nabla s)^T/s^2\) and the off-diagonal part of
\(-\nabla^2s/s\) lie in the span of the \(u\) coordinate, the \(v\)
coordinate, and \((1/w_i)_i\).  Hence its inverse is also diagonal plus rank
at most three.  This algebra is useful, but a dimension-free comparison like
(8) requires additional normalized-slack and access parameters.  No
parameter-free SQ theorem is claimed here for the logarithm cone.

## Novelty boundary and consequence

The barrier (2) and its parameter are due to
[Roy--Xiao](https://doi.org/10.1007/s11590-021-01748-7).
[Kapelevich--Andersen--Vielma](https://arxiv.org/abs/2201.04121) give a
closed-form inverse-Hessian operator for the radial power cone.
[Chen--Goulart](https://arxiv.org/abs/2305.12275) explicitly prove and exploit
augmented-sparse Hessian structure for generalized power, power-mean, and
relative-entropy cones.  Therefore neither the low-rank algebra nor sparse
classical factorization is new.

A targeted primary-source search found no sample-query or quantum-inspired
Newton-direction sampler using this nonsymmetric-cone structure.  The
defensible apparent novelty is the combination of the dimension-free
comparison (8), stable signed Woodbury reduction, and exact SQ output sampler.
It extends the Lorentz exclusion principle to a genuinely nonsymmetric,
high-dimensional cone:

> A fixed number of large generalized power cones cannot by itself
> yield a dimension-polynomial QIPM advantage for one Newton-state sample
> when radial eccentricity, sparse-base conditioning, and the stated
> iterate-SQ and barrier-scalar access are controlled.

The barrier parameter is \(m+1\), so the outer path-following iteration count
still grows with the number of positive coordinates.  The theorem removes a
putative quantum advantage in the dense Newton solve; it does not remove that
outer-iteration dependence or the cost of constructing and updating the SQ
data structures.
