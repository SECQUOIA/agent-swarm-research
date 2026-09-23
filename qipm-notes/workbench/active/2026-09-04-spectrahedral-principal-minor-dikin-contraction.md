# Principal-minor contraction for spectrahedral Dikin metrics

Status: Proved and independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High; convexity, decay laws, and matching paths hostile-audited

## Result

Let
\[
        L(x)=L_0+\mathcal A x\succ0,\qquad
        F(x)=-\log\det L(x)                                      \tag{1}
\]
be an affine real symmetric or complex Hermitian pencil on an open convex
domain \(\Omega\).  Work on the affine hull on which
\(\nabla^2F\) is positive definite.  For an isometry
\(Q:\mathbb F^r\to\mathbb F^n\), define the compressed potential
\[
                 \psi_Q(x)=-\log\det(Q^*L(x)Q).                   \tag{2}
\]
Then
\[
                   \boxed{\nabla^2\psi_Q(x)\preceq\nabla^2F(x).} \tag{3}
\]

Moreover,
\[
        |D\psi_Q(x)[h]|
           \leq\sqrt r\,[D^2\psi_Q(x)[h,h]]^{1/2}
           \leq\sqrt r\,\|h\|_{F,x}.                              \tag{4}
\]
The first constant can be replaced by any sharper gradient parameter
\(\vartheta_Q\) known for the restricted compressed function:
\[
                    |D\psi_Q[h]|\leq
                    \sqrt{\vartheta_Q}\,\|h\|_{F,x}.              \tag{5}
\]

Consequently, for any \(x_0,x\in\Omega\),
\[
 d_F(x_0,x)\geq {1\over\sqrt{\vartheta_Q}}
 \left[\log{\det(Q^*L(x_0)Q)\over\det(Q^*L(x)Q)}\right]_+.        \tag{6}
\]
If a sequence from \(x_0\) reaches an endpoint satisfying the displayed
determinant ratio, and every forward chord has starting \(F\)-Dikin norm at
most \(\delta<1\), its number of chords obeys
\[
 T\geq {1\over\sqrt{\vartheta_Q}\,[-\log(1-\delta)]}
 \left[\log{\det(Q^*L(x_0)Q)\over\det(Q^*L(x)Q)}\right]_+.        \tag{7}
\]

This is a general inactive-auxiliary principle: a path may move through
every coordinate of the full pencil, but it cannot shorten the metric cost
of collapsing a fixed principal determinant.

## Proof

Extend \(Q\) to a unitary basis \((Q,Q_\perp)\).  In that basis write
\[
 L(x)=
 \begin{pmatrix}A(x)&B(x)\\B(x)^*&C(x)\end{pmatrix},
 \qquad A(x)=Q^*L(x)Q.                                           \tag{8}
\]
The determinant quotient gives
\[
 F(x)-\psi_Q(x)=-\log\det S(x),\qquad
 S(x)=C(x)-B(x)^*A(x)^{-1}B(x).                                  \tag{9}
\]
The matrix-fractional map \((A,B)\mapsto B^*A^{-1}B\) is jointly matrix
convex.  Since \(A,B,C\) are affine, \(S\) is matrix concave.  The function
\(-\log\det\) is convex and decreasing in the Loewner order, so its
composition with the positive-definite matrix-concave map \(S\) is convex.
Thus \(F-\psi_Q\) is convex, which proves (3).

For \(A=Q^*LQ\) and \(\dot A=Q^*(\mathcal Ah)Q\),
\[
 D\psi_Q[h]=-\operatorname{tr}(A^{-1}\dot A),\qquad
 D^2\psi_Q[h,h]=\operatorname{tr}
                    \bigl((A^{-1/2}\dot A A^{-1/2})^2\bigr).      \tag{10}
\]
Trace Cauchy--Schwarz proves the first inequality in (4), and (3) proves
the second.  Equation (5) is the same argument with a sharper restricted
gradient inequality.

Integrating (5) along an arbitrary piecewise \(C^1\) curve and minimizing
over curves proves (6).  A forward chord of starting local norm
\(\delta<1\) has Riemannian length at most \(-\log(1-\delta)\) by standard
self-concordant Hessian comparison.  The triangle inequality then proves
(7).

The isometry convention loses no generality.  If \(R\) is any full-column-
rank matrix and \(R=QH\) is a thin QR factorization, then
\(-\log\det(R^*LR)=-\log\det(Q^*LQ)-\log\det(H^*H)\).  The last term is
constant.  Thus (3)--(7) apply unchanged to an injective compression
\(R^*LR\), and its determinant ratio is independent of the chosen basis.

## Sharp specializations

### Low-rank spectral-norm objectives

For a matrix ball, take
\[
 L(X)=\begin{pmatrix}I_p&X\\X^*&I_q\end{pmatrix}.                 \tag{11}
\]
If \(U\in\mathbb F^{p\times r}\) contains the left singular vectors of a
rank-\(r\) objective, compress (11) to the active \(r\) row coordinates
and all \(q\) right coordinates.  Then
\[
 \psi_U(X)=-\log\det(I_r-U^*XX^*U).                               \tag{12}
\]
Although the principal LMI has order \(r+q\), the fixed identity block
makes (12) an \(r\)-parameter matrix-ball potential.  Thus
\(\vartheta_U=r\), not \(r+q\).  Combining (6) with active-minor Hadamard
and objective-gap AM--GM gives the independently audited bound
\[
 d_F(0,X)\geq\sqrt r
 \left[\log{r(\prod_{i=1}^rw_i)^{1/r}\over2\epsilon}\right]_+.    \tag{13}
\]
This matches the explicit rank-\(r\) central path up to universal
constants.

### Low-rank exposed PSD slacks

Let \(W\succeq0\) have rank \(r\), and write
\[
                    W=QDQ^*,\qquad D\succ0,                     \tag{14}
\]
where the columns of \(Q\) are orthonormal.  Suppose an endpoint satisfies
the exposed-slack gap bound
\[
                    \operatorname{tr}(WL(x))\leq\epsilon.       \tag{15}
\]
Put \(A(x)=Q^*L(x)Q\).  The positive-definite matrix
\(Z=D^{1/2}A(x)D^{1/2}\) has trace at most \(\epsilon\), so eigenvalue
AM--GM gives
\[
 \det D\,\det A(x)=\det Z
       \leq\left({\epsilon\over r}\right)^r.                    \tag{16}
\]
Applying (6) with \(\vartheta_Q=r\) yields
\[
 \boxed{
 d_F(x_0,x)\geq\sqrt r
  \left[
   \log{r\{\det D\,\det(Q^*L(x_0)Q)\}^{1/r}\over\epsilon}
  \right]_+.}                                                    \tag{17}
\]
The same substitution in (7) gives the corresponding forward-Dikin-chord
lower bound.  The constant is exact in (16): equality holds precisely when
\(D^{1/2}A(x)D^{1/2}=(\epsilon/r)I_r\).  This proof is unchanged over
real symmetric and complex Hermitian pencils.

There is also a basis-free multiscale version that is not weakened by tiny
positive eigenvalues of \(W\).  Define
\[
 Z_0=D^{1/2}Q^*L(x_0)QD^{1/2},qquad
 \lambda_1(Z_0)\geq\cdots\geq\lambda_r(Z_0)>0.                  \tag{18}
\]
For a fixed \(m\), let the columns of \(U_m\) be top \(m\) eigenvectors of
\(Z_0\), and compress \(L\) by the injective matrix
\(R_m=QD^{1/2}U_m\).  At the endpoint,
\[
 \operatorname{tr}(R_m^*L(x)R_m)
 \leq\operatorname{tr}(D^{1/2}Q^*L(x)QD^{1/2})
 =\operatorname{tr}(WL(x))\leq\epsilon.                         \tag{19}
\]
Hence determinant AM--GM and the full-column-rank extension of (6) give
the exposed-rank profile
\[
 \boxed{
 d_F(x_0,x)\geq
 \max_{1\leq m\leq r}\sqrt m
 \left[
  \log{m\{\lambda_1(Z_0)\cdots\lambda_m(Z_0)\}^{1/m}
       \over\epsilon}
 \right]_+.}                                                     \tag{20}
\]
Ky Fan's variational principle and determinant interlacing show that the
chosen top eigenspace maximizes the compressed trace and determinant at the
start among all \(m\)-dimensional subspaces.  If \(L(x_0)=I\) and
\(d_1\geq\cdots\geq d_r\) are the positive eigenvalues of \(W\), then
\(\lambda_i(Z_0)=d_i\).  Thus (20) becomes
\[
 d_F(x_0,x)\geq
 \max_{1\leq m\leq r}\sqrt m
 \left[\log{m(d_1\cdots d_m)^{1/m}\over\epsilon}\right]_+.     \tag{21}
\]
This is the PSD analogue of the singular-value rank-profile bound for a
spectral-norm ball.

### Exact asymptotic exposed-spectrum laws

Assume now that \(L(x_0)=I\), write \(L_\epsilon=\log(1/\epsilon)\), and
let the positive eigenvalues of \(W\) be decreasing.  Formula (21) can be
optimized explicitly for two standard decay profiles.

For geometric decay \(d_i=e^{-a(i-1)}\), with fixed \(a>0\), the size-\(m\)
expression in (21) is
\[
 \sqrt m\left[L_\epsilon+\log m-{a(m-1)\over2}\right]_+.         \tag{22}
\]
Its continuous maximizer satisfies
\[
 m_*={2\over3a}\{L_\epsilon+\log m_*+a/2+2\}
     ={2L_\epsilon\over3a}+O_a(\log L_\epsilon).                 \tag{23}
\]
Consequently, if the finite rank contains the maximizing scale,
\(r\geq(2/(3a)+o(1))L_\epsilon\), then
\[
 \max_{m\leq r}\sqrt m
   \left[\log{m(d_1\cdots d_m)^{1/m}\over\epsilon}\right]_+
 =\left\{{2\over3}\sqrt{2\over3a}+o_a(1)\right\}
    L_\epsilon^{3/2}.                                           \tag{24}
\]
In particular, any truncation with \(r\geq c_aL_\epsilon\) for a suitable
constant \(c_a>0\) gives the order
\(\Omega_a(L_\epsilon^{3/2})\).  If \(r=o(L_\epsilon)\), the unconstrained
optimizer is unavailable and (22), maximized only over \(m\leq r\), is the
correct finite-rank statement.

For polynomial decay \(d_i=i^{-\beta}\), with fixed \(\beta>1\), Stirling's
formula gives, uniformly at a diverging optimizing scale,
\[
 \log{m(d_1\cdots d_m)^{1/m}\over\epsilon}
 =L_\epsilon-(\beta-1)\log m+\beta+o(1).                         \tag{25}
\]
Thus
\[
 m_*=\{e^{(2-\beta)/(\beta-1)}+o_\beta(1)\}
          \epsilon^{-1/(\beta-1)},                              \tag{26}
\]
and, provided \(r\geq m_*\), the optimized lower envelope is
\[
 \left\{2(\beta-1)e^{(2-\beta)/(2(\beta-1))}+o_\beta(1)\right\}
       \epsilon^{-1/[2(\beta-1)]}.                              \tag{27}
\]
Already \(r\geq c_\beta\epsilon^{-1/(\beta-1)}\), for any fixed sufficiently
large \(c_\beta>0\), gives the same order.  For fixed finite \(r\) and
\(\epsilon\to0\), both decay laws eventually cross over to the capped
\(\sqrt r\log(1/\epsilon)\) regime; (24) and (27) are joint
accuracy--rank asymptotics.

These lower laws are attainable in concrete spectrahedral families, but
not universally.  For a finite list \(d_1,\ldots,d_r\), consider
\[
 \Omega_r=(0,2)^r,\qquad
 L(q)=\operatorname{Diag}(q_1,\ldots,q_r,2-q_1,\ldots,2-q_r),    \tag{28}
\]
with center \(q^0=\mathbf1\), and expose only the first \(r\) diagonal
entries with
\(W=\operatorname{Diag}(d_1,\ldots,d_r,0,\ldots,0)\).  The objective gap
to the boundary infimum is \(\sum_i d_iq_i\).  The product logdet metric is
Euclidean in the scalar coordinates
\[
 \varrho(q)=\int_q^1\sqrt{t^{-2}+(2-t)^{-2}}\,dt,\qquad0<q\leq1,
 \quad
 \log{1\over q}\leq\varrho(q)\leq\sqrt2\log{1\over q}.           \tag{29}
\]
Choose
\[
                  q_i^*=\min\left\{1,{\epsilon\over rd_i}\right\}.
                                                                    \tag{30}
\]
Then \(\sum_i d_iq_i^*\leq\epsilon\), and linear interpolation from zero
to \((\varrho(q_i^*))_i\) in the \(\varrho\)-coordinates is a feasible path
of exact length
\[
 \left(\sum_i\varrho(q_i^*)^2\right)^{1/2}
 \leq\sqrt2\left[\sum_i\log_+^2{rd_i\over\epsilon}\right]^{1/2}. \tag{31}
\]
Taking \(r=\lceil m_*\rceil\) makes (31)
\(O_a(L_\epsilon^{3/2})\) in the geometric case and
\(O_\beta(\epsilon^{-1/[2(\beta-1)]})\) in the polynomial case.  Together
with (24) and (27), these are matching feasible-path examples up to fixed
constants.  For the polynomial estimate, writing
\(i=rt\) makes
\(\log_+(rd_i/\epsilon)\) a fixed constant minus
\(\beta\log t\); the square is integrable on \(0<t\leq1\), so the sum in
(31) is \(O_\beta(r)\).  These exponents agree exactly with the independently
audited spectral-ball laws for geometric and polynomial singular-value
decay.  The spectral-ball factor \(2\epsilon\) changes only lower-order
terms here.

The matching paths are noncentral diagonal paths for specially constructed
box spectrahedra.  The rank-profile theorem alone supplies no matching upper
bound for a general affine pencil, and no central-path upper is being
claimed here.

Thus every SDP objective or dual certificate whose primal objective gap is
exactly, or is lower-bounded by, \(\operatorname{tr}(WL(x))\) compiles a
rank-\(r\) exposed-slack condition directly into a path-independent
standard-logdet movement bound.  This is the spectrahedral specialization
of the exposed-rank mechanism in the symmetric-cone note, while (3) adds
the point needed for affine restrictions and inactive auxiliary
coordinates.

### Packed PSD and completion slices

If \(L(x)\) itself is a PSD slack or completion matrix and an endpoint
argument forces a \(q\times q\) principal determinant to shrink, take
\(\vartheta_Q=q\) in (6)--(7).  All off-support or completion coordinates
remain available to the path, but (3) shows that they cannot reduce the
principal-minor metric cost.  This isolates the common mechanism behind the
packed-PSD and chordal/spectral fixed-slice lower bounds in the workbench.

## Scope and prior-art boundary

The matrix-fractional convexity and the convexity of
\[
        F-\psi_Q
        =\log\det(Q_\perp^*L^{-1}Q_\perp)
\]
are classical matrix-convexity facts; the latter identity follows from
block inversion.  They appear, for example, in the supplemental exercises
to Boyd and Vandenberghe,
[*Convex Optimization*](https://github.com/cvxgrp/cvxbook_additional_exercises),
in the equivalent form \(\log\det(P^TX^{-1}P)\).

The candidate contribution is not this convexity fact.  It is the explicit
Hessian contraction (3), the sharper restricted-parameter form (5), and
their use as a path-independent endpoint-to-Dikin-iteration compiler for
spectrahedral formulations with inactive auxiliary coordinates.  A targeted
search found the underlying convexity and extensive work on principal
minors, but no source stating this combined bounded-move theorem.  Priority
remains subject to specialist review.

The theorem is for the fixed standard log-determinant metric, feasible
interior paths, and uniformly bounded forward Dikin chords.  It is not a
lower bound for arbitrary barriers, infeasible or unbounded local-norm
steps, per-iteration arithmetic, quantum queries, or output materialization.

## Audit targets

1. Check the determinant quotient and which complementary compression of
   \(L^{-1}\) equals \(S^{-1}\).
2. Verify the convex-decreasing composed with matrix-concave argument over
   real and complex affine pencils.
3. Check the trace-gradient parameter and the sharper
   \(\vartheta_Q\) substitution.
4. Check both directions of the distance and Dikin-chord conversion.
5. Verify that the matrix-ball specialization legitimately uses
   \(\vartheta_Q=r\), despite the compressed LMI order \(r+q\).

## Independent hostile audit

The audit verified the determinant quotient
\(\det L=\det A\,\det(C-B^*A^{-1}B)\).  The Schur complement is
matrix concave, and composing it with the convex Loewner-decreasing
function \(-\log\det\) proves that \(F-\psi_Q\) is convex over both
\(\mathbb R\) and \(\mathbb C\).  Thus the Hessian contraction (3) is
correct.  Trace Cauchy--Schwarz gives the rank-\(r\) gradient constant,
and any sharper gradient inequality for the compressed potential
substitutes exactly as in (5).  Integrating it gives (6), while standard
forward self-concordant Hessian comparison gives the
\(-\log(1-\delta)\) chord constant in (7).

The matrix-ball compression has a fixed identity block, so its
determinant reduces to the rank-\(r\) potential in (12); inactive
directions may make its Hessian semidefinite but do not change the
gradient parameter.  For a PSD exposure, determinant AM--GM applied to
\(D^{1/2}Q^*LQ D^{1/2}\) gives (16) with the stated exact equality case.
For the multiscale profile, \(R_m=QD^{1/2}U_m\) is injective,
its endpoint trace is at most \(\operatorname{tr}(WL)\), and its start
determinant is the product of the top \(m\) eigenvalues of \(Z_0\).
The full-column compression differs from an isometric compression only
by a constant determinant, so (20)--(21) follow with no basis or
real/complex normalization defect.  No correction was required.

### Decay-law and matching-path audit

A second independent hostile audit differentiated the continuous
geometric objective in (22).  Its stationarity equation is exactly (23);
at the optimizer the bracket equals \(am_*-2\), which gives the constant
\((2/3)\sqrt{2/(3a)}\) in (24).  Stirling's formula gives (25), and
stationarity sets its bracket to \(2(\beta-1)\), yielding both the cutoff
and constant in (26)--(27).  Integer rounding is absorbed by the displayed
little-\(o\) terms, and the stated finite-rank crossovers are correct.

For the diagonal box, each endpoint term satisfies
\[
 d_iq_i^*=\min\{d_i,\epsilon/r\}\leq\epsilon/r,
\]
so the total objective error is at most \(\epsilon\).  The coordinate
\(\varrho\) exactly Euclideanizes the product Hessian metric, and on
\(0<q\leq1\) its integrand lies between \(1/q\) and \(\sqrt2/q\).
Therefore the interpolated path is feasible, has the exact length stated
in (31), and obeys its upper bound.  With the geometric cutoff every
summand is \(O_a(L_\epsilon^2)\) and \(r=O_a(L_\epsilon)\).  With the
polynomial cutoff,
\(\log_+(rd_i/\epsilon)=\log_+(C_\beta-\beta\log(i/r))+o(1)\);
the square is integrable on \((0,1]\), so the sum is \(O_\beta(r)\).
This verifies the matching exponents and all endpoint and metric constants.
No correction was required.
