# Objective-rank-adaptive central and shortest paths on spectral-norm matrix balls

Status: Exact central path, global shortest-path reduction, movement bounds, and arbitrary-path lower bounds independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the explicit-barrier theorem; QIPM implications are deliberately conditional

## Main result

Let \(\mathbb F=\mathbb R\) or \(\mathbb C\), let
\(C,X\in\mathbb F^{p\times q}\), and assume \(p\le q\) after transposing
if necessary.  On the open spectral-norm ball
\[
                 \mathbb B_{p,q}=\{X:\|X\|_{\rm op}<1\},           \tag{1}
\]
use the classical barrier
\[
                    \phi(X)=-\log\det(I_p-XX^*).                   \tag{2}
\]
The real-valued pairing is
\(\langle C,X\rangle=\operatorname{Re}\operatorname{tr}(C^*X)\).
The barrier parameter is \(p\), although the ambient real dimension is
\(pq\) in the real case and \(2pq\) in the complex case.

Consider
\[
                  \min_{\|X\|_{\rm op}<1}-\langle C,X\rangle.      \tag{3}
\]
If \(C\ne0\) and its nonzero singular values are
\(w_1\ge\cdots\ge w_r>0\), then the exact primal central path has
singular vectors equal to those of \(C\), singular values
\[
 x_i(\eta)=r(\eta w_i),
 \qquad
 r(z)={z\over1+\sqrt{1+z^2}},                                     \tag{4}
\]
and zeros in every remaining singular direction.  With a dot denoting
\(d/d\log\eta\), its squared speed is
\[
 \boxed{
  \|\dot X(\eta)\|_{X(\eta)}^2
   =r_{\rm eff}(\eta)
   :=\sum_{i=1}^r\left(1-{1\over\sqrt{1+(\eta w_i)^2}}\right).}    \tag{5}
\]
Thus the primal path depends on a soft count of the objective's resolved
singular directions, not on the matrix dimensions or even on the barrier
parameter \(p\).

For the accuracy statements below, fix \(0<\epsilon\le1\).  For an exact rank-\(r\) objective normalized by
\(\|C\|_{\rm op}\le1\), an \(\epsilon\)-objective-accurate central point
is reachable from the analytic center with
\[
 L_{\rm P}\le {\|C\|_F\over\sqrt2}
       +\sqrt r\left[\log{r\over\epsilon}\right]_+
 \le\sqrt{r/2}+\sqrt r\left[\log{r\over\epsilon}\right]_+.       \tag{6}
\]
For a rank-\(r\) partial isometry this is
\(\Theta(\sqrt r\log(r/\epsilon))\).  An arclength schedule therefore
uses
\[
 O_R\!\left(\sqrt r[1+\log(r/\epsilon)]\right)                     \tag{7}
\]
primal Dikin chords of radius \(R<1\), rather than the generic
\(O_R(\sqrt p\log(p/\epsilon))\) barrier-parameter ledger.

This rank dependence is sharp even if one abandons the central path.  Every
primal path from the analytic center to an \(\epsilon\)-accurate point obeys
\[
 d_\phi(0,X)\ge \sqrt r
 \left[\log{r(\prod_{i=1}^r w_i)^{1/r}\over2\epsilon}\right]_+.
                                                                    \tag{7a}
\]
For equal nonzero singular values, (7a) matches (6) up to universal
constants.

More generally, the exact distance from zero to any endpoint is the
Euclidean norm of its singular values after the scalar metric transform
\(\rho\) in (32A).  Distance to the \(\epsilon\)-objective sublevel is
therefore the strictly convex water-filling problem (32Q), with the
dimension-free \(\sqrt2\)-equivalent Lambert-\(W\) surrogate (32T)--(32V).
Following the central path can cost a sharp
\(\Theta(\sqrt{\log r})\) factor more than the shortest path to the same
central endpoint, and can be still less efficient when the endpoint itself
may vary over the accuracy sublevel.

The same theorem holds for a product of spectral balls after pooling all
singular values of all objective blocks.  It is an exact movement theorem
for this unconstrained support-objective family, not a generic low-rank
QIPM runtime theorem.

## 1. Exact singular-value central path

Take a compact SVD
\[
                         C=U\operatorname{Diag}(w_i)V^*.           \tag{8}
\]
Von Neumann's trace inequality gives
\[
                 \langle C,X\rangle
                 \le\sum_iw_i\sigma_i(X),                         \tag{9}
\]
with equality when the nonzero singular directions align with \(U,V\).
The barrier is a spectral function,
\[
                  \phi(X)=-\sum_{j=1}^p\log(1-\sigma_j(X)^2).      \tag{10}
\]
Hence minimizing
\(\phi(X)-\eta\langle C,X\rangle\) reduces to independent scalar
problems
\[
                 \min_{0\le x<1}-\log(1-x^2)-\eta w_ix.           \tag{11}
\]
Strict convexity makes the central point unique.  Its active coordinates
satisfy
\[
                     \eta w_i={2x_i\over1-x_i^2},                  \tag{12}
\]
which is equivalent to (4); coordinates with \(w_i=0\) equal zero.

The path also has the basis-free formula
\[
 X(\eta)=
 \eta\bigl(I_p+\sqrt{I_p+\eta^2CC^*}\bigr)^{-1}C.                 \tag{13}
\]
This identity is useful for matrix-function and block-encoding access, but
does not make its implementation free.

## 2. Effective singular-direction speed

Along the aligned singular subspace, (10) is a sum of the scalar barriers
\(-\log(1-x_i^2)\).  Directional second differentiation in the ambient
matrix space therefore gives
\[
 \|\dot X\|_X^2
 =\sum_i {2(1+x_i^2)\over(1-x_i^2)^2}\dot x_i^2.                  \tag{14}
\]
Differentiating (12) with respect to \(\log\eta\) yields
\[
                       \dot x_i={x_i(1-x_i^2)\over1+x_i^2}.        \tag{15}
\]
Equations (14)--(15) give
\[
 {2x_i^2\over1+x_i^2}
       =1-{1\over\sqrt{1+(\eta w_i)^2}},                           \tag{16}
\]
proving (5).  Equivalently,
\[
 r_{\rm eff}(\eta)
   =\operatorname{tr}\!\left[
       I_p-(I_p+\eta^2CC^*)^{-1/2}\right].                         \tag{17}
\]

For the conic homogenization
\[
 \mathcal S_{p,q}=\{(t,X):\|X\|_{\rm op}\le t\},
 \qquad
 F(t,X)=(p-1)\log t-\log\det(t^2I_p-XX^*),                        \tag{18}
\]
the barrier parameter is \(p+1\).  Imposing \(t=1\) recovers (2).  The
general primal--dual speed-splitting theorem then gives the exact conjugate-
dual speed along the conic central path:
\[
                   \|\dot s(\eta)\|_{s(\eta),*}^2
                      =p+1-r_{\rm eff}(\eta).                      \tag{19}
\]
Thus a low-rank objective can move in only \(r\) primal singular
directions while the dual projection carries essentially all of an ambient
\(p+1\) product-metric lower bound.

## 3. Accuracy and the singular-value distribution law

The optimum value of (3) is \(-\|C\|_*=-\sum_iw_i\).  The central primal
error is exactly
\[
                   E(\eta)=\sum_{i=1}^r w_i[1-r(\eta w_i)].        \tag{20}
\]
Put
\[
 Q_1(\eta)=\sum_i\min\{\eta w_i,1\},
 \qquad
 Q_2(\eta)=\sum_i\min\{(\eta w_i)^2,1\}.                          \tag{21}
\]
The scalar inequalities proved in the companion product-ball note give
\[
 (2-\sqrt2){Q_1(\eta)\over\eta}
       \le E(\eta)\le {Q_1(\eta)\over\eta},                       \tag{22}
\]
and, for any \(0\le\eta_0<\eta_1\),
\[
 \sqrt{1-1/\sqrt2}\int_{\eta_0}^{\eta_1}
       \sqrt{Q_2(\eta)}{d\eta\over\eta}
 \le L_{\rm P}(\eta_0,\eta_1)
 \le\int_{\eta_0}^{\eta_1}
       \sqrt{Q_2(\eta)}{d\eta\over\eta}.                         \tag{23}
\]
This is a constant-factor exact law in terms of the objective singular-
value distribution.  The closed-form breakpoint antiderivative in the
[vector product-ball note](2026-09-04-primal-dual-speed-splitting-product-ball-counterexample.md)
applies verbatim after replacing coordinate weights by singular values.

For exact rank \(r\), (20) gives \(E(\eta)\le r/\eta\).  Take
\(\eta_f=r/\epsilon\).  On \(0<\eta\le1\), (5) and
\(1-(1+z^2)^{-1/2}\le z^2/2\) give
\[
                 r_{\rm eff}(\eta)\le{\eta^2\over2}\|C\|_F^2.    \tag{24}
\]
For \(1\le\eta\le\eta_f\), simply use
\(r_{\rm eff}(\eta)\le r\).  Integration proves (6).

If \(C\) is a rank-\(r\) partial isometry, then every \(w_i=1\).  For
\(1\le\eta\le r/\epsilon\), each summand in (5) is at least
\(1-1/\sqrt2\), so
\[
 L_{\rm P}(1,r/\epsilon)
 \ge\sqrt{(1-1/\sqrt2)r}\log{r\over\epsilon}.                     \tag{25}
\]
This proves the matching order claim.

## 4. Numerical rank and full-gap variants

The exact rank may be replaced by an accuracy-dependent numerical rank.
Assume \(\|C\|_{\rm op}\le1\), and choose \(m\ge1\) such that the nuclear
tail satisfies
\[
                         \sum_{i>m}w_i\le{\epsilon\over2}.          \tag{26}
\]
Then \(\eta_f=2m/\epsilon\) gives \(E(\eta_f)\le\epsilon\), and
\[
 L_{\rm P}(0,\eta_f)
 \le \sqrt{m+\epsilon^2/4\over2}
      +\sqrt{2m}\log{2m\over\epsilon}.                            \tag{27}
\]
Thus the movement count depends on the nuclear-tail numerical rank, not on
\(p\).

There is also a conic full-gap version.  If
\[
                     \left(\sum_{i>m}w_i^2\right)^{1/2}
                       \le{\epsilon\sqrt m\over p+1},              \tag{28}
\]
then the central point at \(\eta_g=(p+1)/\epsilon\) has ambient
primal--dual gap exactly \(\epsilon\), while
\[
 L_{\rm P}(0,\eta_g)
 \le \sqrt{m+m\epsilon^2/(p+1)^2\over2}
       +\sqrt{3m/2}\log{p+1\over\epsilon}.                        \tag{29}
\]
The dual path supplies the complementary movement required by (19).

For a product \(\prod_a\mathbb B_{p_a,q_a}\) with the sum barrier and
block objective \((C_a)_a\), pool the singular values of all \(C_a\) in
(20)--(27).  The slice parameter is \(P=\sum_ap_a\), while exact or
numerical objective rank is the corresponding pooled count.  The same
reduced path holds after any shared-scale grouping because fixing the scales
gives literally the same barrier.  For the full-gap variant, a grouping into
\(g\) spectral cones has ambient parameter \(\nu_{\rm amb}=P+g\); replace
\(p+1\) by \(\nu_{\rm amb}\) in (28)--(29).

## 5. Bounded-Dikin schedule

Define cumulative primal arclength
\[
              \mathcal L(\eta)=
              \int_0^\eta\sqrt{r_{\rm eff}(u)}{du\over u}.         \tag{30}
\]
For \(0<R<1\), put \(\ell_R=\log(1+R)\) and choose successive parameters
by
\[
 \mathcal L(\eta_j)
   =\min\{j\ell_R,\mathcal L(\eta_f)\}.                            \tag{31}
\]
Output the exact centers (13).  Every intervening central arc has length at
most \(\ell_R\).  Since
\[
             \log(1+\|X'-X\|_X)\le d_\phi(X,X')
\]
and geodesic distance is no larger than arc length, every forward chord has
starting Dikin norm at most \(R\).  Hence
\[
 N_R\le
 \left\lceil{L_{\rm P}(0,\eta_f)\over\log(1+R)}\right\rceil.       \tag{32}
\]
Equations (6), (27), or (29) give exact-rank, numerical-rank, or full-gap
versions of the schedule.

### 5.1 An explicit noncentral singular-coordinate schedule

The central path is not always the shortest useful primal path.  Define the
scalar metric coordinate
\[
 \rho(x)=\int_0^x{\sqrt{2(1+t^2)}\over1-t^2}\,dt,
 \qquad 0\le x<1.                                                  \tag{32A}
\]
Since
\[
 {1\over1-t}\le {\sqrt{2(1+t^2)}\over1-t^2}
                 \le {\sqrt2\over1-t},
\]
we have
\[
       \log{1\over1-x}\le\rho(x)
          \le\sqrt2\log{1\over1-x}.                              \tag{32B}
\]

Let \(\tau_m=\sum_{i>m}w_i\), choose any \(m\) with
\(\tau_m<\epsilon\), and put \(b_m=\epsilon-\tau_m\).  Define the target
singular values
\[
 x_i^*=1-\min\left\{1,{b_m\over mw_i}\right\}\quad(i\le m),
 \qquad x_i^*=0\quad(i>m).                                       \tag{32C}
\]
Their objective error is at most
\[
 \sum_{i\le m}w_i(1-x_i^*)+\tau_m
 =\sum_{i\le m}\min\{w_i,b_m/m\}+\tau_m
 \le b_m+\tau_m=\epsilon.                                       \tag{32D}
\]
Put \(\ell_i=\rho(x_i^*)\), and follow
\[
 X(s)=U\operatorname{Diag}\!\left(
       \rho^{-1}(s\ell_1),\ldots,\rho^{-1}(s\ell_m),0,\ldots
                                  \right)V^*,\qquad0\le s\le1. \tag{32E}
\]
By the diagonal Hessian formula (14), this path has constant speed
\((\sum_{i\le m}\ell_i^2)^{1/2}\).  Therefore its exact length and a
convenient upper bound are
\[
 L_{\rm SC}(m)
  =\left(\sum_{i\le m}\rho(x_i^*)^2\right)^{1/2}
  \le\sqrt2\left[
       \sum_{i=1}^m\log_+^2{mw_i\over b_m}\right]^{1/2}.          \tag{32F}
\]
Partitioning (32E) by arclength produces forward Dikin chords of radius
at most \(R<1\) using
\[
 N_R^{\rm SC}\le
 \left\lceil {L_{\rm SC}(m)\over\log(1+R)}\right\rceil.          \tag{32G}
\]
One may minimize (32F) over all \(m\) with \(\tau_m<\epsilon\).  In the
exact rank-\(r\) case, choosing \(m=r\) gives the simpler bound
\[
 L_{\rm SC}\le\sqrt2
       \left[\sum_{i=1}^r\log_+^2{rw_i\over\epsilon}\right]^{1/2}.
                                                                    \tag{32H}
\]
This construction is a feasible barrier-geometric path, not a central path
or a generic affine-constrained IPM trajectory.  It is useful here because
it gives an explicit upper counterpart to the arbitrary-path lower bounds
below and separates barrier movement from the requirement of centrality.

The separation can be asymptotically strict.  Fix \(m\ge3\), choose
\(T\ge\log m\), put \(\epsilon=me^{-T}\), and define
\[
 S_m=\sum_{j=1}^{m-1}j^{-3/2},\qquad
 a_i={T\over S_m}\sum_{j=1}^{i-1}j^{-3/2},\qquad
 w_i=e^{-a_i}.                                                     \tag{32I}
\]
Thus \(a_1=0\), \(a_m=T\), and \(w_m=\epsilon/m\).  The central point at
\(\eta_f=e^T=m/\epsilon\) has error at most \(\epsilon\).  On the interval
\(a_j\le\log\eta\le a_{j+1}\), the first \(j\) summands in (5) are at least
\(c_0=1-1/\sqrt2\).  Its central-path length therefore satisfies
\[
 L_{\rm P}(1,e^T)\ge {\sqrt{c_0}\,T\over S_m}
                      \sum_{j=1}^{m-1}{1\over j}.                 \tag{32J}
\]

For the noncentral path (32E), take the exact-rank choice \(b_m=\epsilon\).
Then \(1-x_i^*=e^{a_i-T}\).  Since \(S_m\ge1\),
\[
 \begin{aligned}
 L_{\rm SC}
 &\le\sqrt2\left[\sum_{i=1}^m(T-a_i)^2\right]^{1/2}\\
 &\le\sqrt2\,T\left(1+4\sum_{j=1}^{m-1}{1\over j}\right)^{1/2}.
                                                                    \tag{32K}
 \end{aligned}
\]
The second inequality uses
\(\sum_{j=i}^{m-1}j^{-3/2}\le2/\sqrt{i-1}\) for \(i\ge2\).
Because \(S_m\le\zeta(3/2)\), (32J)--(32K) give
\[
 {L_{\rm P}(1,e^T)\over L_{\rm SC}}
                         =\Omega(\sqrt{\log m}).                  \tag{32L}
\]
For the concrete choice \(T=2\log m\), hence \(\epsilon=1/m\), the exact
central path has length \(\Omega(\log^2m)\), while the explicit feasible
path has length \(O(\log^{3/2}m)\).  This is a continuous path-length
separation.  It does not by itself lower-bound discrete methods whose
iterates need only lie near selected central points.  The next subsection
shows that (32E) is globally shortest to its chosen endpoint, but that
endpoint need not be the closest \(\epsilon\)-accurate endpoint.

### 5.2 Exact center-to-point distance and endpoint water filling

The singular-coordinate construction is globally shortest when its endpoint
is fixed.  Let \(\sigma_1(X),\ldots,\sigma_p(X)\) be the singular values of
\(X\).  Then
\[
 \boxed{
 d_\phi(0,X)=
 \left[\sum_{i=1}^p\rho(\sigma_i(X))^2\right]^{1/2}.}             \tag{32M}
\]

For the lower bound, put \(f(s)=-\log(1-s^2)\), and use the Hermitian
dilation
\[
 {\cal S}(X)=\begin{pmatrix}0&X\\X^*&0\end{pmatrix},\qquad
 g(\lambda)=-{1\over2}\log(1-\lambda^2).
                                                                    \tag{32N}
\]
The eigenvalues of \({\cal S}(X)\) are the pairs
\(\pm\sigma_i(X)\), together with zeros, and
\(\phi(X)=\operatorname{tr}g({\cal S}(X))\).
For a Hermitian \(S\), perturbation \(K\), and a spectral basis chosen to
diagonalize \(K\) inside repeated eigenspaces, the spectral-trace Hessian is
\[
 D^2\operatorname{tr}g(S)[K,K]
 =\sum_\alpha g''(\lambda_\alpha)|K_{\alpha\alpha}|^2
 +2\sum_{\alpha<\gamma}
 {g'(\lambda_\alpha)-g'(\lambda_\gamma)
    \over\lambda_\alpha-\lambda_\gamma}|K_{\alpha\gamma}|^2,      \tag{32O}
\]
with the continuous divided-difference convention.  Since \(g\) is convex
on \((-1,1)\), every off-diagonal term is nonnegative.  Along an absolutely
continuous matrix path, the diagonal contributions of the paired
eigenvalues \(\pm\sigma_i\) give, almost everywhere,
\[
 \|\dot X\|_X^2
 \ge\sum_i f''(\sigma_i)\dot\sigma_i^2
 =\left\|{d\over dt}\rho(\sigma(X))\right\|_2^2.                  \tag{32P}
\]
This statement remains valid at repeated and zero singular values by the
within-eigenspace perturbation rule.  Integrating (32P) and using Euclidean
endpoint distance proves the lower half of (32M).  For the reverse
inequality, fix an SVD of \(X\) and move each singular value linearly in
its \(\rho\)-coordinate, as in (32E).  Formula (14) gives constant speed
\(\|\rho(\sigma(X))\|_2\), proving equality.  The complex case uses the
real Hessian and absolute squares in (32O).

More generally, the same argument gives
\[
 d_\phi(X,Y)\ge
 \|\rho(\sigma(X))-\rho(\sigma(Y))\|_2.                           \tag{32M1}
\]
Equality holds whenever \(X\) and \(Y\) admit a common singular frame with
the same ordering: interpolate their \(\rho\)-coordinates linearly in that
frame.  Thus \(\rho\circ\sigma\) is a global \(1\)-Lipschitz map, every
fixed-singular-frame slice is a Euclidean orthant in \(\rho\)-coordinates,
and the distance between any two points of the central path is exactly the
Euclidean distance between their transformed singular-value vectors.

Consequently, if \(0<\epsilon<\|C\|_*\), the globally shortest distance to
the objective sublevel is exactly
\[
 \boxed{
 L_{\rm opt}(\epsilon)=
 \min_{\substack{0\le x_i<1\\
          \sum_{i=1}^r w_i(1-x_i)\le\epsilon}}
       \left[\sum_{i=1}^r\rho(x_i)^2\right]^{1/2}.}               \tag{32Q}
\]
Indeed, von Neumann's inequality shows that every feasible matrix endpoint
has
\(\sum_iw_i[1-\sigma_i(X)]\le\epsilon\).  Nonobjective singular values only
increase (32M), while aligning the remaining singular vectors with those
of \(C\) attains equality for any chosen \(x_i\).

The squared problem in (32Q) is strictly convex: \(\rho'>0\),
\(\rho''\ge0\), and
\[
                    (\rho^2)''=2[(\rho')^2+\rho\rho'']>0.         \tag{32R}
\]
Its unique endpoint has \(0<x_i<1\), an active error constraint, and a
unique multiplier \(\lambda>0\) satisfying
\[
       2\rho(x_i)\rho'(x_i)=\lambda w_i\quad(1\le i\le r),
 \qquad \sum_iw_i(1-x_i)=\epsilon.                               \tag{32S}
\]
Thus one scalar search for \(\lambda\), followed by independent coordinate
inversions, finds the globally distance-minimizing endpoint.  The
\(\rho\)-linear path to it is globally shortest and can be partitioned
into the forward-Dikin schedule (32G).  If
\(\epsilon\ge\|C\|_*\), the value is zero; \(\epsilon=0\) is a boundary
limit of infinite distance.

There is also a simple logarithmic water-filling surrogate.  Set
\(s_i=-\log(1-x_i)\), and define
\[
 D_{\log}(\epsilon)=
 \min_{\substack{s_i\ge0\\\sum_iw_ie^{-s_i}\le\epsilon}}
                       \left(\sum_i s_i^2\right)^{1/2}.           \tag{32T}
\]
The scalar bounds (32B) imply the dimension-free comparison
\[
             D_{\log}(\epsilon)\le L_{\rm opt}(\epsilon)
                         \le\sqrt2\,D_{\log}(\epsilon).           \tag{32U}
\]
The unique logarithmic optimizer has
\[
 s_i=W(\gamma w_i),\qquad
 \sum_iW(\gamma w_i)=\gamma\epsilon,                              \tag{32V}
\]
where \(W\) is the principal Lambert function and \(\gamma>0\) is unique.
This follows from the KKT equation
\(s_i=\gamma w_ie^{-s_i}\); every coordinate is positive when
\(0<\epsilon<\|C\|_*\).

The same value characterizes the optimal number of bounded primal Dikin
moves, up to constants depending only on the chosen radius.  Let
\(T_R^\star(\epsilon)\) be the minimum number of feasible chords from zero
to any \(\epsilon\)-accurate endpoint, allowing arbitrary noncentral
intermediate points, subject only to
\(\|X^{j+1}-X^j\|_{X^j}\le R<1\).  Then
\[
 {L_{\rm opt}(\epsilon)\over-\log(1-R)}
 \le T_R^\star(\epsilon)
 \le\left\lceil{L_{\rm opt}(\epsilon)\over\log(1+R)}\right\rceil. \tag{32V1}
\]
For the lower bound, the straight segment associated with each chord has
Riemannian length at most \(-\log(1-R)\), so their concatenation has length
at least the endpoint distance.  For the upper bound, take the unique
water-filled endpoint (32S), follow its globally minimizing
\(\rho\)-linear path, and partition by arclength \(\log(1+R)\); the
self-concordant inequality
\(\log(1+\|\Delta\|_{\rm start})\le d_\phi\) makes every forward chord
valid.  Thus (32Q), or (32T) within \(\sqrt2\), is a matched geometric move
complexity for this explicit family.  It is not a runtime or oracle-query
bound.

For a product of matrix balls, pool all objective singular values in
(32Q)--(32V1).  Product-metric distances add in squares, and the fixed-SVD
\(\rho\)-linear path is blockwise, so the exact distance reduction and
bounded-move characterization are unchanged.

The exact distance also quantifies the largest possible same-endpoint
centrality tax.  Put \(a_i=-\log w_i\), use \(s=\log\eta\), and let
\[
 v_i(s)={d\over ds}\rho(x_i(e^s))
   =\left(1-{1\over\sqrt{1+e^{2(s-a_i)}}}\right)^{1/2}.           \tag{32W}
\]
Because the weights are ordered, \(v_1(s)\ge\cdots\ge v_r(s)\ge0\).
For any decreasing nonnegative vector \(v\), set
\(\alpha_i=\sqrt i-\sqrt{i-1}\).  Its prefix decomposition gives
\[
 \|v\|_2
 \le\sum_{j=1}^r\sqrt j\,(v_j-v_{j+1})
 =\sum_{i=1}^r\alpha_iv_i,\qquad v_{r+1}=0.                       \tag{32X}
\]
Integrating (32X) and applying Cauchy--Schwarz proves, for every central
endpoint \(X(\eta_f)\),
\[
 \boxed{
 d_\phi(0,X(\eta_f))\le L_{\rm P}(0,\eta_f)
 \le\Gamma_r\,d_\phi(0,X(\eta_f)),}
 \quad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
 =1+{1\over4}\log r+O(1).                                       \tag{32Y}
\]
Indeed, \(\int v_i(s)\,ds=\rho(x_i(\eta_f))\), so (32M) identifies the
last Euclidean norm with the exact endpoint distance.

The factor \(\Gamma_r=\Theta(\sqrt{\log r})\) is sharp.  In (32I), take
\(T\ge\sqrt{m/\log m}\), for example \(T=m\), and use the central endpoint
at \(s_f=T\).  Write \(b_i=T-a_i\).  Equation (32J) gives
\(L_{\rm P}=\Omega(T\log m)\), while
\[
 \|\rho(x(e^T))\|_2
 \le\sqrt2\left[
       \left(\sum_i b_i^2\right)^{1/2}
       +\log(1+\sqrt2)\sqrt m\right]
 =O(T\sqrt{\log m}).                                             \tag{32Z}
\]
Here \(b_1=T\), \(b_i\le2T/\sqrt{i-1}\), and for \(z\ge1\),
\(1-r(z)\ge[(1+\sqrt2)z]^{-1}\).  Thus the ratio in (32Y) is
\(\Theta(\sqrt{\log m})\).  Both this central endpoint and (32C) are in
the sublevel with \(\epsilon=me^{-T}\).  The upper bound in (32Y) compares
the central arc only with the distance to its own endpoint; it does not
upper-bound the ratio to \(L_{\rm opt}(\epsilon)\), whose minimizing
endpoint can differ.

Nevertheless, the worst same-accuracy-set ratio has the same sharp order.
Let \(\eta_\epsilon\) be the first central parameter whose primal objective
error is at most \(\epsilon\), and let \(L_{\rm CP}(\epsilon)\) be the
central arclength from zero to \(X(\eta_\epsilon)\).  Define
\[
 c_\star=\max_{y>0}{p^{-1}(yp'(y))\over y},\qquad
 p(y)=b'(\rho^{-1}(y)),\quad b(x)=-\log(1-x^2).                 \tag{32Z0}
\]
The independently audited scalar analysis in
[`2026-09-04-exact-scalar-centrality-dilation.md`](2026-09-04-exact-scalar-centrality-dilation.md)
proves \(1<c_\star<69/50\).  Then
\[
 \boxed{
 L_{\rm CP}(\epsilon)
 \le c_\star\Gamma_r L_{\rm opt}(\epsilon)
 <{69\over50}\Gamma_r L_{\rm opt}(\epsilon)
 =O(\sqrt{\log r})\,L_{\rm opt}(\epsilon).}                       \tag{32Z1}
\]
For reference, the following earlier exact-coordinate argument gives the
slightly weaker self-contained certificate
\(\kappa_0=1.391010896\ldots\), the unique root in \((1,2)\) of
\(\log[\kappa_0(\kappa_0-1)]+2-\kappa_0=0\).  Put
\(b(x)=-\log(1-x^2)\), let \(x(y)=\rho^{-1}(y)\), and define
\[
 p(y)=b'(x(y)).
 \qquad
 p'(y)=\rho'(x(y)).                                               \tag{32Z2}
\]
The key scalar lemma is
\[
                         p(\kappa_0y)\ge yp'(y),\qquad y\ge0.     \tag{32Z3}
\]
For completeness, for \(y>0\) put \(E(y)=yp'(y)/p(y)\ge1\).  Direct differentiation,
with \(x=x(y)\), gives
\[
 {dE\over d\log y}
 =E-{y^2(1-x^2)\over2x^2(1+x^2)}\ge E-1.                        \tag{32Z3a}
\]
The inequality uses
\[
 \rho(x)\le B(x):=\sqrt2x\sqrt{1+x^2\over1-x^2}.
\]
Indeed, \(B(0)=0\), and, for \(u=x^2\),
\[
 {B'(x)\over\rho'(x)}
 ={1+2u-u^2\over(1+u)\sqrt{1-u}}\ge1,
\]
because the difference after squaring is
\(u(3+3u-3u^2+u^3)\ge0\).  Integrating (32Z3a) gives
\(E(ty)\ge1+t(E(y)-1)\) for \(t\ge1\), and hence
\[
 \log{p(ay)\over p(y)}
 \ge\log a+(a-1)(E(y)-1).
\]
For fixed \(a\in(1,2)\), the right side minus \(\log E(y)\) is minimized
over \(E\ge1\) at \(E=1/(a-1)\), with value
\(\log[a(a-1)]+2-a\).  The definition of \(\kappa_0\) proves (32Z3).
The defining left side is strictly increasing on \((1,2)\), so this root
is unique; the case \(y=0\) follows by continuity.

Let \(y_i^\star=\rho(x_i^\star)\) be the exact optimizer in (32Q), and
let \(\lambda\) be its multiplier in (32S).  At central parameter
\(\eta=\lambda/2\), write the transformed central coordinates as
\(y_i^{\rm c}\).  The two first-order systems give
\[
 p(y_i^{\rm c})=y_i^\star p'(y_i^\star).                         \tag{32Z4}
\]
Since \(p'\) is increasing, \(p(y)\le yp'(y)\), so
\(y_i^{\rm c}\ge y_i^\star\) and this central point is already
\(\epsilon\)-accurate.  Definition (32Z0) gives the exact comparison
\(y_i^{\rm c}\le c_\star y_i^\star\); equation (32Z3) also gives the weaker
bound \(y_i^{\rm c}\le\kappa_0y_i^\star\).  The first accurate central point
occurs no later and is coordinatewise no larger, so its exact distance
from zero is at most
\(c_\star\|y^\star\|_2=c_\star L_{\rm opt}(\epsilon)\).  Applying (32Y)
proves (32Z1).

This order is attained.  Use (32I) with \(T=m\) and
\(\epsilon=me^{-T}\).  At \(s=T-1\), all but \(O(\sqrt m)\) indices have
\(b_i=T-a_i\ge1\), hence \(z_i=e^{s-a_i}\ge1\).  Since
\(z[1-r(z)]\ge z/(1+z)\ge1/2\),
\[
 E(T-1)\ge {e\over2}(m-O(\sqrt m))e^{-T}>me^{-T}=\epsilon         \tag{32Z5}
\]
for all sufficiently large \(m\), while \(E(T)\le me^{-T}\).
Therefore the first accurate central parameter lies in
\((T-1,T]\).  Truncating (32J) only removes \(O(\sqrt m)\) final indices,
so
\[
 L_{\rm CP}(\epsilon)=\Omega(m\log m).                            \tag{32Z6}
\]
The explicit endpoint (32C) is exactly \(\epsilon\)-accurate and (32K)
gives \(L_{\rm opt}(\epsilon)\le O(m\sqrt{\log m})\).  Thus
\[
 \sup_{\substack{w_1\ge\cdots\ge w_r>0\\
                  0<\epsilon<\sum_iw_i}}
 {L_{\rm CP}(\epsilon)\over L_{\rm opt}(\epsilon)}
                         =\Theta(\sqrt{\log r}).                  \tag{32Z7}
\]
This is an arclength-versus-shortest-path theorem.  It does not assert that
every discrete method maintaining a central-neighborhood condition needs
that many bounded chords.

### 5.3 A discrete central-neighborhood round separation

The \(T=m\) instance above also separates bounded-Dikin round counts under
a precise central-neighborhood contract.  Let \(s_\epsilon=\log
\eta_\epsilon\).  Consider any feasible iterates \(Z_0,\ldots,Z_N\) with
arbitrary real central labels satisfying only
\[
 Z_0=0,
 \qquad \|C\|_* -\mathop{\rm Re}\operatorname{tr}(C^*Z_N)
                         \le\epsilon,                            \tag{32Z8}
\]
such that, for fixed \(R<1\) and \(\delta<\infty\),
\[
 \|Z_{k+1}-Z_k\|_{Z_k}\le R,\qquad
 d_\phi(Z_k,X(e^{s_k}))\le\delta.                                \tag{32Z9}
\]
Then
\[
                       N=\Omega_{R,\delta}(m\log m).              \tag{32Z10}
\]

To prove this, every round has
\[
 d_\phi(X(e^{s_k}),X(e^{s_{k+1}}))
 \le C_{R,\delta}:=2\delta-\log(1-R).                            \tag{32Z11}
\]
Indeed, the middle iterate-to-iterate distance is at most
\(-\log(1-R)\), and the endpoint terms are at most \(\delta\).

Actual endpoint accuracy forces the final reference label past the clipped
region; no stopping-label assumption is needed.  In the sharp instance,
\(w_1=1\).  The Fan--von Neumann inequality and (32Z8) give
\(\sum_iw_i[1-\sigma_i(Z_N)]\le\epsilon\), and hence
\(\sigma_1(Z_N)\ge1-\epsilon\).  The contraction (32M1),
the tube condition, and (32B) give
\[
 y_1(s_N):=\rho(r(e^{s_N}))
 \ge\rho(1-\epsilon)-\delta
 \ge m-\log m-\delta.                                          \tag{32Z11a}
\]
By (32W), \(y_1(s)=\int_{-\infty}^s v_1(u)\,du\).  The elementary bound
\(v_1(u)\le e^u/\sqrt2\) for \(u\le0\), together with \(v_1\le1\),
therefore gives
\[
 s_N\ge m-\log m-\delta-1/\sqrt2>a_J                           \tag{32Z11b}
\]
for all sufficiently large \(m\).  The last inequality follows from
\[
 m-a_J={m\over S_m}\sum_{j=J}^{m-1}j^{-3/2}
                      =\Theta(m^{2/3}).
\]
The analytic-center start also makes any starting label harmless.  By
(32Z9) and the exact center distance,
\(\|y(s_0)\|_2=d_\phi(0,X(e^{s_0}))\le\delta\).  If \(s_0\le0\), then
\({\cal P}(s_0)=0\).  If \(s_0>0\), the first coordinate has derivative at
least \(v_0\) on \([0,s_0]\), so \(s_0\le\delta/v_0\).  Since
\(a_2=m/S_m\to\infty\), this implies
\[
                         {\cal P}(s_0)=O_\delta(1).              \tag{32Z11c}
\]

The exact two-endpoint formula (32M1) applies with equality to the two
centers.  For a round with \(s_{k+1}>s_k\), if
\(s_k\in[a_j,a_{j+1})\), the first \(j\) transformed
singular-value velocities (32W) are at least
\[
                         v_0=\sqrt{1-1/\sqrt2}.
\]
Consequently,
\[
                 s_{k+1}-s_k\le {C_{R,\delta}\over v_0\sqrt j}.  \tag{32Z12}
\]

Let \(J=\lfloor m^{2/3}\rfloor\), let
\(q(s)=|\{i:a_i\le s\}|\), and define the clipped progress potential
\[
 {\cal P}(s)=\int_0^{\min\{\max\{s,0\},a_J\}}\sqrt{q(u)}\,du.      \tag{32Z13}
\]
For \(j\le J\), consecutive thresholds satisfy
\[
                     a_{j+1}-a_j={m\over S_m\,j^{3/2}}
                                      \ge {1\over S_m}.           \tag{32Z14}
\]
Here is a symmetric bound that also handles backward and clipped jumps.
Put
\(F(s)=\min\{\max\{s,0\},a_J\}\) and
\(y_i(s)=\rho(r(e^{s-a_i}))\).  Coordinate monotonicity gives, for every
pair \(s,t\),
\[
 \|y(F(s))-y(F(t))\|_2\le\|y(s)-y(t)\|_2\le C_{R,\delta}.        \tag{32Z14a}
\]
Order the clipped endpoints as \(\ell<u\), and put \(j=q(\ell)\ge1\).
The first \(j\) coordinate derivatives are at least \(v_0\), so
\(u-\ell\le C_{R,\delta}/(v_0\sqrt j)\).  If \(n=q(u)-q(\ell)\), the
spacing (32Z14) gives
\[
 n\le1+{C_{R,\delta}S_m\over v_0\sqrt j}
      \le B_{R,\delta}<\infty.
\]
Consequently every round, in either label direction, satisfies
\[
 |{\cal P}(s_{k+1})-{\cal P}(s_k)|
 \le(u-\ell)\sqrt{j+n}
 \le {C_{R,\delta}\over v_0}\sqrt{1+B_{R,\delta}}
 =O_{R,\delta}(1).                                              \tag{32Z14b}
\]
But
\[
 {\cal P}(a_J)
 ={m\over S_m}\sum_{j=1}^{J-1}{1\over j}
 =\Omega(m\log m).                                               \tag{32Z15}
\]
Since (32Z11b) places \(s_N>a_J\), summing the absolute per-round progress
bounds and using
\({\cal P}(s_N)-{\cal P}(s_0)={\cal P}(a_J)-O_\delta(1)\) proves
(32Z10).

In contrast, (32V1), (32K), and (32Z1)--(32Z6) give
\[
                  T_R^\star(\epsilon)=\Theta_R(m\sqrt{\log m}).  \tag{32Z16}
\]
Hence fixed-radius central-neighborhood path following has a sharp
\(\Omega_{R,\delta}(\sqrt{\log m})\) round overhead over the optimal
noncentral bounded-Dikin sequence on this family.  This theorem concerns
the standard barrier, the explicit support objective, geodesic
central-neighborhood radius, and arbitrary central labels.  It is not a
lower bound for every possible IPM neighborhood definition or for quantum
query complexity.
The data of the lower family are sparse in the natural singular frame:
\(C=\operatorname{Diag}(w_1,\ldots,w_m)\) has only \(m\) nonzero entries,
and the conic homogenization adds only the equality \(t=1\).  The theorem
therefore isolates the central-neighborhood movement contract rather than
dense input formation, but it does not assign a sparse-oracle cost to the
spectral cone itself.

The proof also quantifies a growing tube.  Keep \(R<1\) fixed, allow
\(\delta=\delta_m\), and put
\[
 C_m=2\delta_m-\log(1-R).
\]
Since \(S_m\le\zeta(3/2)\), (32Z14b) gives the explicit per-round bound
\[
 |\Delta{\cal P}|
 \le {C_m\over v_0}
       \sqrt{2+{C_m\zeta(3/2)\over v_0}}
 =O(C_m\sqrt{1+C_m}).                                          \tag{32Z16a}
\]
Applying the same clipped argument between the analytic center and the
starting reference center gives
\({\cal P}(s_0)=O(\delta_m\sqrt{1+\delta_m})\).  Moreover, (32Z11a)--
(32Z11b) still force \(s_N>a_J\) whenever
\(\delta_m=o(m^{2/3})\).  In that regime the starting correction is
\(o(m\log m)\), and therefore
\[
 N=\Omega_R\!\left(
 {m\log m\over C_m\sqrt{1+C_m}}
 \right).                                                       \tag{32Z16b}
\]
Because unrestricted noncentral movement costs
\(\Theta_R(m\sqrt{\log m})\), the central-neighborhood overhead still
diverges whenever
\[
                         \delta_m=o((\log m)^{1/3}).             \tag{32Z16c}
\]
This is a quantitative robustness statement, not a claim for arbitrarily
wide neighborhoods.

The geodesic-tube hypothesis includes the usual fixed Newton-decrement
neighborhood.  Define
\[
 f_\eta(Z)=\phi(Z)-\eta\mathop{\rm Re}\operatorname{tr}(C^*Z),
 \qquad
 \lambda_\eta(Z)=\|\nabla f_\eta(Z)\|_{Z,*}.                    \tag{32Z17}
\]
For any standard self-concordant function with an interior minimizer
\(Z_\eta^\star\),
\[
 \|Z-Z_\eta^\star\|_Z
 \le {\lambda_\eta(Z)\over1-\lambda_\eta(Z)}.                 \tag{32Z18}
\]
Indeed, if \(D=Z_\eta^\star-Z\) and \(q=\|D\|_Z\), Hessian comparison
along the segment gives
\[
 -\langle\nabla f_\eta(Z),D\rangle
 =\int_0^1 D^*\nabla^2f_\eta(Z+tD)D\,dt
 \ge {q^2\over1+q},
\]
whereas local Cauchy--Schwarz bounds the left side by
\(\lambda_\eta(Z)q\).  This proves (32Z18).  Here
\(Z_\eta^\star=X(\eta)\), and the linear objective means that
\(\nabla^2f_\eta=\nabla^2\phi\).  Therefore, if
\(\lambda_\eta(Z)\le\beta<1/2\), the straight-segment metric bound yields
\[
 d_\phi(Z,X(\eta))
 \le -\log\!\left(1-{\beta\over1-\beta}\right)
 =:\delta_\beta
 =\log{1-\beta\over1-2\beta}.                                 \tag{32Z19}
\]
Substituting \(\delta=\delta_\beta\) into (32Z10) proves the directly
IPM-facing corollary
\[
 N=\Omega_{R,\beta}(m\log m)                                   \tag{32Z20}
\]
for every sequence of forward-
\(R\) Dikin steps satisfying
\(\lambda_{e^{s_k}}(Z_k)\le\beta<1/2\) and returning an actually
\(\epsilon\)-accurate final iterate, when started at the analytic center.
Thus the
\(\Omega(\sqrt{\log m})\) overhead applies to this conventional
short-step central neighborhood, not only to a neighborhood defined by
geodesic distance.  The fixed-radius, standard-barrier, and
explicit-family qualifications remain in force; no monotonicity of the
reference labels is required.
Combining (32Z19) with the growing-tube bound also permits
\(\beta=\beta_m\uparrow1/2\): the overhead still diverges whenever
\[
 \log{1-\beta_m\over1-2\beta_m}
                         =o((\log m)^{1/3}).                    \tag{32Z20a}
\]

There is also a direct feasible primal--dual transfer to the conic
homogenization (18).  Impose the affine slice \(t=1\), start its primal
component at \(X=0\), and suppose each full primal--dual product-Dikin
chord has norm at most \(R\).  Its primal component then satisfies the
same forward \(R\)-bound, because the restriction of the conic primal
Hessian to \(\Delta t=0\) is exactly \(\nabla^2\phi\), while the other
primal and dual squared norms are nonnegative.  If the iterates are
primal--dual feasible and the final duality gap is at most \(\epsilon\),
weak duality makes the final primal point \(\epsilon\)-accurate.  Therefore
any such sequence whose primal component satisfies the fixed-decrement
condition in (32Z20) also needs
\[
                         \Omega_{R,\beta}(m\log m)              \tag{32Z20b}
\]
full primal--dual chords.  This is a lower bound for the stated feasible
path-following contract, not for infeasible-start or unbounded-update QIPMs.

The primal decrement condition itself follows from a standard scaled
primal--dual centrality residual.  Write the conic primal cost as
\(c=(0,-C)\), the equality as \(t=1\), and a dual slack as
\(q=c-A^*y\), so its matrix component is always \(q_X=-C\).  If
\(z=(1,X)\), \(\mu>0\), and
\[
                 \|q+\mu\nabla F(z)\|_{z,*}\le\beta\mu,        \tag{32Z20c}
\]
then restriction of covectors to the tangent slice \(\Delta t=0\) and
duality of the induced Hessian metric give
\[
 \lambda_{1/\mu}(X)
 =\left\|\nabla\phi(X)-{1\over\mu}C\right\|_{X,*}
 \le {1\over\mu}\|q+\mu\nabla F(z)\|_{z,*}
 \le\beta.                                                      \tag{32Z20d}
\]
Therefore (32Z20b) applies verbatim when its explicit primal decrement
hypothesis is replaced by (32Z20c).  This is the conventional feasible
primal--dual short-step residual, with central label
\(s=-\log\mu\).

## 6. A matching path-independent low-rank lower bound

The same \(\sqrt r\) dependence is necessary for every primal path, not
only for the central path.  The key fact is a metric-contraction lemma for
row compression.  If \(U\in\mathbb F^{p\times r}\) has orthonormal columns,
define
\[
 \psi_U(X)=-\log\det(I_r-U^*XX^*U).
                                                                    \tag{32a}
\]
Then, throughout \(\mathbb B_{p,q}\),
\[
                 \nabla^2\psi_U(X)\preceq\nabla^2\phi(X),
 \qquad
                 |D\psi_U(X)[H]|\le\sqrt r\,\|H\|_X.             \tag{32b}
\]

Here is a self-contained proof.  Use the standard positive-definite lift
\[
 L(X)=\begin{pmatrix}I_p&X\\X^*&I_q\end{pmatrix}\succ0,
 \qquad -\log\det L(X)=\phi(X).                                  \tag{32c}
\]
After extending \(U\) to a unitary basis and reordering coordinates, the
principal submatrix on the active \(r\) row coordinates and all \(q\) right
coordinates is
\[
 L_U(X)=\begin{pmatrix}I_r&U^*X\\X^*U&I_q\end{pmatrix},
 \qquad -\log\det L_U(X)=\psi_U(X).                              \tag{32d}
\]
The determinant quotient gives
\[
                  \phi(X)-\psi_U(X)=-\log\det S(X),              \tag{32e}
\]
where \(S\) is the Schur complement of \(L_U\) in \(L\).  A Schur
complement \(C-B^*A^{-1}B\) is matrix concave in the positive-definite
block matrix \(\bigl(\begin{smallmatrix}A&B\\B^*&C\end{smallmatrix}\bigr)\):
this is the joint matrix convexity of \(B^*A^{-1}B\).  Since
\(-\log\det\) is convex and order reversing, \(-\log\det S\) is convex.
Thus (32e) proves the Hessian inequality in (32b).  Finally, \(\psi_U\)
is the pullback of the \(r\)-self-concordant matrix-ball barrier, so
\[
 |D\psi_U[H]|\le\sqrt r\,[D^2\psi_U[H,H]]^{1/2}
                 \le\sqrt r\,\|H\|_X,
\]
which completes the lemma.

Now let \(C\) have rank \(r\ge1\), compact SVD as in (8), and positive
singular values \(w_1,\ldots,w_r\).  Define
\[
                 \overline w_g=\left(\prod_{i=1}^r w_i\right)^{1/r}.
                                                                    \tag{32f}
\]
If a feasible \(X\in\mathbb B_{p,q}\) has objective error at most
\(\epsilon\), then
\[
 \boxed{
  d_\phi(0,X)\ge \sqrt r
     \left[\log{r\overline w_g\over2\epsilon}\right]_+.}          \tag{32g}
\]
Indeed, take \(U\) to contain the left singular vectors of \(C\), define
\(z_i=\operatorname{Re}(u_i^*Xv_i)\), and apply Hadamard's inequality to
\(D_U=I_r-U^*XX^*U\):
\[
 \det D_U
  \le\prod_{i=1}^r(1-\|X^*u_i\|^2)
  \le\prod_{i=1}^r(1-z_i^2)
  \le2^r\prod_{i=1}^r(1-z_i).                                    \tag{32h}
\]
Set \(e_i=w_i(1-z_i)\ge0\).  Objective accuracy says
\(\sum_ie_i\le\epsilon\), so AM--GM gives
\[
 \psi_U(X)\ge
 r\log{r\overline w_g\over2\epsilon}.                           \tag{32i}
\]
Also \(\psi_U(X)\ge0=\psi_U(0)\).  Integrating (32b) along any curve
from zero to \(X\), then taking the infimum over curves, proves (32g).

Consequently, any primal sequence from zero with forward Dikin chords
\(\|X^{j+1}-X^j\|_{X^j}\le R<1\) and an \(\epsilon\)-accurate endpoint
must have
\[
 T\ge {\sqrt r\over-\log(1-R)}
       \left[\log{r\overline w_g\over2\epsilon}\right]_+.          \tag{32j}
\]
For a product of matrix balls, apply the compression lemma blockwise, pool
all nonzero objective singular values, and let \(r\) be their total count.
The sum of the active barriers has gradient norm at most \(\sqrt r\) in the
full product metric, so (32g)--(32j) remain unchanged.

For a rank-\(r\) partial isometry, the arbitrary-path lower bound (32g)
matches the central-path upper and lower bounds (6), (25) up to universal
constants.  Thus the objective-rank dependence is intrinsic to this
explicit family: it is neither an artifact of following the central path
nor replaceable by the ambient slice parameter \(p\).

The same proof gives a stronger multiscale form that is not degraded by
tiny tail singular values.  Order \(w_1\ge\cdots\ge w_r\), and for
\(1\le m\le r\) put
\[
                     \overline w_{g,m}
                       =\left(\prod_{i=1}^m w_i\right)^{1/m}.
                                                                    \tag{32k}
\]
Compressing to only the first \(m\) left singular vectors and repeating
(32h)--(32i) gives the rank-profile bound
\[
 \boxed{
 d_\phi(0,X)\ge
 \max_{1\le m\le r}\sqrt m
   \left[\log{m\overline w_{g,m}\over2\epsilon}\right]_+.}        \tag{32l}
\]
Indeed, the sum of the first \(m\) directional errors is at most the total
objective error \(\epsilon\).  The top \(m\) weights maximize the geometric
mean over all size-\(m\) subsets, so no other subset improves this proof.
The product-ball version follows by sorting the pooled nonzero singular
values.

There is no dimension-free reverse comparison between (32l) and the exact
value (32Q).  Fix
\[
 0<c<\log(2/\sqrt e),\qquad
 s_i={c\over\sqrt i},\qquad
 H_{r,1/2}=\sum_{i=1}^r i^{-1/2},\qquad
 \epsilon={1\over2},                                             \tag{32l1}
\]
and take
\[
 \alpha={\epsilon\over cH_{r,1/2}},\qquad
 w_i=\alpha s_i e^{s_i}.                                        \tag{32l2}
\]
The weights are positive and decreasing.  In the logarithmic water-filling
problem (32T), the multiplier \(\gamma=1/\alpha\) makes
\(s_i=\gamma w_ie^{-s_i}\) and
\(\sum_iw_ie^{-s_i}=\epsilon\).  Hence
\[
             D_{\log}(\epsilon)=c\sqrt{\sum_{i=1}^r{1\over i}}
                              =\Theta(\sqrt{\log r}),             \tag{32l3}
\]
and (32U) gives the same order for \(L_{\rm opt}\).

On the other hand, for every \(m\le r\),
\[
 {m\overline w_{g,m}\over2\epsilon}
 ={m(m!)^{-1/(2m)}
       \exp\!\left({c\over m}\sum_{i=1}^mi^{-1/2}\right)
    \over2H_{r,1/2}}
 \le {e^{c}\sqrt e\over2}\sqrt{m\over r}<1.                       \tag{32l4}
\]
Here \(m!\ge(m/e)^m\) and \(H_{r,1/2}\ge\sqrt r\).  Thus the entire
right-hand side of (32l) is zero while the exact shortest distance diverges.
The rank-profile bound is therefore a useful explicit certificate, not a
constant-factor characterization; the exact water-filling value
(32Q), or its \(\sqrt2\)-equivalent surrogate (32T), is the intrinsic
distribution-sensitive quantity.

For example, if the nuclear tail after \(m\) is at most \(\epsilon/2\) as
in (26), while the first \(m\) weights are all at least \(w_*>0\), then
the upper schedule (27) and arbitrary-path lower bound (32l) bracket the
movement by
\[
 \sqrt m\left[\log{mw_*\over2\epsilon}\right]_+
 \le d_\phi(0,X)\le L_{\rm P}(0,2m/\epsilon)
 \le \sqrt{m+\epsilon^2/4\over2}
       +\sqrt{2m}\log{2m\over\epsilon}.                           \tag{32m}
\]
Thus, when \(w_*\) is bounded below, the
\(\Theta(\sqrt m\log(m/\epsilon))\) numerical-rank scale is also
path-independent.  Without such a scale condition, a point near the
analytic center may already meet the absolute-error target, so no lower
bound of that order is possible.

Two distributions illustrate that (23), (32Q), and (32l) give tight laws
beyond hard rank.

**Geometric decay.**  Let \(w_i=e^{-a(i-1)}\), where \(a>0\) is fixed,
and put \(L=\log(1/\epsilon)\).  If \(L/a\ge2\) and the truncation rank is
at least the indices used below, choose \(m=\lfloor L/a\rfloor\).  Then
\[
 \overline w_{g,m}=e^{-a(m-1)/2},\qquad
 \log{m\overline w_{g,m}\over2\epsilon}\ge {L\over2},             \tag{32n}
\]
so (32l) gives
\[
                  d_\phi(0,X)\ge {L^{3/2}\over2\sqrt{2a}}.        \tag{32o}
\]
Conversely, take
\[
 M=\left\lceil {L+\log(2/(1-e^{-a}))\over a}\right\rceil .        \tag{32p}
\]
The nuclear tail after \(M\) is at most \(\epsilon/2\), so (27) gives a
central path of length \(O_a(L^{3/2})\).  Therefore geometric singular
decay has the path-independent tight law
\[
                         L_{\rm opt}(\epsilon)=\Theta_a(L^{3/2}), \tag{32q}
\]
provided the finite truncation contains \(\Theta_a(L)\) singular values.
For \(a=\log2\), this recovers and strengthens the dyadic central-path law
from the vector product-ball note: arbitrary primal detours cannot improve
its order.

**Polynomial decay.**  Let \(w_i=i^{-\beta}\) for fixed \(\beta>1\).
For \(\eta\ge1\), comparison with tail integrals gives
\[
 Q_1(\eta)\le A_\beta\eta^{1/\beta},\qquad
 Q_2(\eta)\le B_\beta\eta^{1/\beta},                              \tag{32r}
\]
where one may take
\(A_\beta=2+1/(\beta-1)\) and \(B_\beta=2+1/(2\beta-1)\).
Hence \(\eta_f=(A_\beta/\epsilon)^{\beta/(\beta-1)}\) is
\(\epsilon\)-accurate by (22), and (23) yields
\[
 L_{\rm P}(0,\eta_f)\le {\sqrt{\zeta(2\beta)}\over\sqrt2}
  +2\beta\sqrt{B_\beta}\,[\eta_f^{1/(2\beta)}-1]
  =O_\beta\!\left(\epsilon^{-1/[2(\beta-1)]}\right).              \tag{32s}
\]
For the reverse bound, set
\[
 m=\left\lfloor(4\epsilon)^{-1/(\beta-1)}\right\rfloor           \tag{32t}
\]
and assume \(m\ge1\) and the truncation rank is at least \(m\).  Since
\((m!)^{-\beta/m}\ge m^{-\beta}\), the logarithm in (32l) is at least
\(\log2\).  Up to the harmless floor for sufficiently small \(\epsilon\),
\[
 d_\phi(0,X)=\Omega_\beta\!\left(\epsilon^{-1/[2(\beta-1)]}\right).
                                                                    \tag{32u}
\]
Thus polynomial singular decay has a tight, log-free
\(\Theta_\beta(\epsilon^{-1/[2(\beta-1)]})\) movement law.  The absence
of a logarithm is genuine: new singular directions become active gradually,
rather than all \(m\) directions remaining active over the same logarithmic
parameter interval.

## 7. Does this give a meaningful QIPM variation?

It suggests a precise but narrow variation: **singular-activity-adaptive
path following**.  Instead of increasing \(\eta\) at the generic
\(1+\Theta(1/\sqrt p)\) rate, choose checkpoints by (31), using the
effective count (17).  When only \(r\ll p\) singular directions are visible
at the requested scale, this reduces the number of primal metric moves from
the generic \(\widetilde O(\sqrt p)\) ledger to
\(\widetilde O(\sqrt r)\).

For the present unconstrained support problem, however, this is not by
itself a useful quantum optimization algorithm:

- Formula (13) solves every central point directly.  If a classical
  low-rank factorization or SVD of \(C\) is already given, a compact
  rank-\(r\) representation costs only \(O((p+q)r)\) data, and an IPM is
  unnecessary.
- With only a block encoding of \(C\), (13) is a singular-value transform.
  Preparing a normalized state proportional to \(X(\eta)\) may be possible
  without materializing all \(pq\) entries, but its cost depends on the
  block-encoding normalization, approximation degree, success amplitude,
  and the smallest singular value that must be resolved.  The movement
  theorem does not bound any of these.
- A classical matrix output still costs \(\Omega(pq)\) entries in the worst
  case, while a rank-factor output costs \(\Omega((p+q)r)\).  A quantum-state
  output has a different contract and cannot be compared directly.
- Adding generic affine constraints destroys the simultaneous singular-vector
  reduction used in (9)--(13).  The theorem extends only to constraints that
  preserve the same spectral subspace decomposition, or to product blocks
  that remain uncoupled after equality elimination.

The most plausible QIPM use is therefore as an adaptive predictor or
checkpoint rule inside a structured matrix-ball subproblem whose objective
singular spaces are cheaply available and whose output is compact or
quantum.  Establishing an end-to-end advantage would require a separate
oracle construction and conditioning/readout analysis.

## 8. Literature and novelty boundary

The spectral-norm cone barrier, its fixed-scale restriction, and their exact
parameters are classical; see Nesterov--Nemirovskii, *Interior-Point
Polynomial Algorithms in Convex Programming*, Proposition 5.4.6, and the
local [shared spectral-cone
note](2026-09-04-spectral-norm-product-sharing.md).  Von Neumann's trace
inequality and singular-value functional calculus are also classical.
The spectral-trace Hessian formula behind (32O) is a specialization of
Lewis and Sendov,
[“Twice Differentiable Spectral Functions”](https://doi.org/10.1137/S089547980036838X)
(SIAM J. Matrix Anal. Appl. 23, 2001); an
[author-hosted copy](https://people.orie.cornell.edu/aslewis/publications/01-twice.pdf)
is openly available.

Nesterov and Nemirovski,
[“Primal Central Paths and Riemannian Distances for Convex Sets”](https://doi.org/10.1007/s10208-007-9019-4),
prove a general \(O(\nu^{1/4})\) bounded-domain central-path/geodesic
comparison.  Nesterov and Todd,
[“On the Riemannian Geometry Defined by Self-Concordant Barriers”](https://doi.org/10.1007/s102080010032),
give the general self-concordant Riemannian and primal--dual distance
framework used by the companion speed-splitting note.  Neither source
states the exact standard matrix-ball distance (32M), the objective
water-filling reduction (32Q)--(32V), or the sharp
\(\Theta(\sqrt{\log r})\) spectral-profile centrality tax (32Z7).  The
metric here is the real Hessian metric of (2); it is not being identified
with the Bergman distance.

Hirai, Nieuwboer, and Walter,
[“Interior-Point Methods on Manifolds: Theory and Applications”](https://doi.org/10.1007/s10208-026-09756-8)
(2026), develop self-concordance and Newton/path-following theory when the
optimization domain is itself a Riemannian manifold.  Their framework is
adjacent but different: the metric there is part of the base manifold,
whereas the present metric is the Euclidean matrix-ball barrier Hessian.
Their results do not supply the transformed-singular-value distance,
objective water filling, or central-versus-noncentral separation here.

There are substantially broader LP lower-bound frameworks.  Allamigeon,
Benchimol, Gaubert, and Joswig prove exponential log-barrier central-path
complexity ([arXiv:1708.01544](https://arxiv.org/abs/1708.01544));
Allamigeon, Gaubert, and Vandame extend strong-polynomiality obstructions to
self-concordant-barrier IPMs
([arXiv:2201.02186](https://arxiv.org/abs/2201.02186)); and Allamigeon,
Dadush, Loho, Natura, and Végh define straight-line complexity as the
minimum number of segments traversing a wide central neighborhood
([arXiv:2206.08810](https://arxiv.org/abs/2206.08810)).  Those results are
stronger in generality or worst-case growth, but use different LP,
neighborhood, and segment models.  They do not state the exact
spectral-ball distance-to-accuracy law or the matched
\(\Theta(\sqrt{\log r})\) central-versus-optimal forward-Dikin separation
proved here.

The local [path-independent spectral-ball lower-bound
note](2026-09-04-spectral-ball-dikin-iteration-lower-bound.md) treats
full-row-rank support objectives and proves an endpoint lower bound in terms
of total exposed row rank.  The present result is complementary: it computes
the exact central path for arbitrary singular-value weights and shows that
low or numerical objective rank yields a smaller upper movement ledger.  Its
active-compression potential also makes the exact-rank dependence sharp for
arbitrary paths, including when the objective rank is much smaller than the
ambient row dimension.

A targeted local and open-web search did not locate formulas (5), (17), the
constant-factor distribution law (22)--(23), the numerical-rank schedule
(26)--(32), the objective-rank endpoint theorem (32g), or the matched
spectral-profile laws (32l)--(32u) for spectral-norm balls.  It also did
not locate the exact distance/water-filling theorem, optimal bounded-Dikin
move sandwich, or sharp same-endpoint and same-accuracy centrality
distortions.  The spectral Hessian formula and convexity of negative log
determinant of a Schur complement are classical.  The safe candidate
contribution is their exact objective-rank- and spectral-profile-adaptive
matrix-ball synthesis, including the shortest-path reduction, matched
geometric move complexity, arbitrary-path bounds, and primal-versus-dual
interpretation—not a new barrier, spectral Hessian formula, Bergman metric
identity, or generic QIPM runtime speedup.  Priority remains subject to a
specialist literature review.

## Independent audit record

An independent hostile audit verified the SVD reduction and basis-free
formula (13), strict central-point uniqueness, the ambient directional
Hessian calculation in (14)--(16), the rectangular null directions, and the
conic primal--dual complement (19).  It also checked the \(Q_1/Q_2\)
distribution laws, exact- and numerical-rank bounds, full-gap tail variant,
Dikin schedule, and complex real-trace convention.  The audit found and
repaired two presentation defects: the accuracy results now explicitly
assume \(0<\epsilon\le1\), so every split at \(\eta=1\) is valid, and the
missing inequality symbol in (6) was restored.  No substantive defect
remains within the stated explicit-family scope.

A follow-up hostile audit verified the matching arbitrary-path lower bound
in Section 6.  It checked the determinant quotient and Schur-complement
convexity argument, the Hessian domination and pullback gradient estimate,
the complex real-Hessian convention, active-minor Hadamard and AM--GM steps,
product pooling, and the forward-Dikin denominator.  The audit found no
defect and confirmed that the \(\sqrt r\) theorem supersedes the weaker
\(r/\sqrt p\) determinant-height bound.

A second follow-up hostile audit verified the rank-profile corollary and
both decay examples.  In particular, it checked the top-subset geometric-
mean maximization, the constants in the geometric tail cutoff, the
polynomial \(Q_1/Q_2\) integral comparisons and endpoint choice, the
direction of the factorial/geometric-mean inequality, and the finite-rank
and small-\(\epsilon\) provisos.  No correction was needed.

A third hostile audit verified the noncentral singular-coordinate schedule
(32A)--(32H): the ambient Hessian restriction, scalar metric-coordinate
bounds, strict endpoint feasibility and error, exact constant-speed length,
and forward-Dikin conversion.  It found only a missing LaTeX delimiter in
(32E), which was repaired.  A separate audit then verified the multiscale
separation (32I)--(32L), including its indexing, constants, exact
\(\epsilon\)-endpoint convention, harmonic-sum lower bound, and continuous-
path-only caveat.  The insertion initially suffered a text-escaping defect;
the whole block was replaced, and control-character, duplicate-tag, and
diff checks now pass.

A fourth independent hostile audit verified the exact distance and sharp
same-endpoint centrality tax in (32M)--(32Z).  At a repeated positive
singular value, compressing the dilation perturbation to the positive and
negative eigenspaces gives opposite copies of the Hermitian singular-value
perturbation, so their diagonal Hessian terms sum to
\(f''(\sigma_i)\dot\sigma_i^2\).  At zero, the enlarged zero eigenspace
contains the Hermitian dilation of the null-to-null perturbation; its paired
eigenvalue derivatives are the first derivatives of the zero singular
values.  Thus (32P) holds almost everywhere for real and complex absolutely
continuous paths, including rank changes.  The audit also checked the
decreasing-velocity prefix decomposition, the exact
\(\Gamma_r^2=\sum_i(\sqrt i-\sqrt{i-1})^2\) coefficient, and the
\(T=m\) instance in (32I): its central length is
\(\Omega(m\log m)\), its own endpoint distance is
\(O(m\sqrt{\log m})\), and (32Y) supplies the matching upper ratio.  No
correction was required.

A fifth hostile audit, independently duplicated, verified the
same-accuracy theorem (32Z1)--(32Z7).  It checked both scalar slack bounds,
the original log-coordinate comparison, the \(O(\sqrt m)\) terminal-index
count, the exact
\(\epsilon=me^{-T}\) convention, and placement of the first accurate
central parameter in \((T-1,T]\).  Both audits confirmed the sharp
\(\Theta(\sqrt{\log r})\) ratio and its arclength-only scope.

Two independent hostile audits also verified the optimal bounded-Dikin
sandwich (32V1) and the discrete central-neighborhood separation
(32Z8)--(32Z16), including the strengthened arbitrary-label version.
They checked the center-to-iterate triangle bound, exact
two-center distance, per-round log-parameter advance, initial negative-
label crossing, reverse and clipped jumps, threshold spacing, clipped
progress potential, and the
comparison (T_R^\star=\Theta_R(m\sqrt{\log m})\).  No defect was found.

A further hostile audit verified the Newton-decrement corollary
(32Z17)--(32Z20).  It checked the iterate-based local-norm direction in
(32Z18), the stationarity sign, both self-concordant Hessian comparisons,
the exact radius
\(\delta_\beta=\log((1-\beta)/(1-2\beta))\), and the substitution into the
discrete theorem.  No correction was needed.

Two hostile audits then verified the removal of all reference-label
progress assumptions.  They checked the clipped-coordinate contraction,
the uniform absolute progress bound for backward and cross-zero jumps, the
fact that actual \(\epsilon\)-accuracy forces \(s_N>a_J\), and the fact
that an analytic-center start forces only \(O_\delta(1)\) initial clipped
progress.  Thus (32Z8)--(32Z20) require neither monotone labels nor assumed
start/end labels.  No correction was needed.

A constant audit first verified the log-coordinate improvement from
\(3\sqrt2\Gamma_r\) to \(2\sqrt2\Gamma_r\).  The later exact-coordinate
argument in (32Z2)--(32Z4) supersedes that estimate with
\(\kappa_0\Gamma_r\); its separate audit is recorded below.

A hostile audit independently rederived the elasticity identity
(32Z3a), the auxiliary bound \(\rho\le B\), the scalar dilation inequality
(32Z3), and the use of the exact water-filling multiplier at
\(\eta=\lambda/2\).  It confirmed the
\(\kappa_0\Gamma_r\) same-accuracy constant with no correction.  This is
a certified uniform bound, not a claim that \(\kappa_0\) is the exact
smallest scalar constant.

The later exact scalar-dilation theorem was independently hostile-audited.
It proves that (32Z0) attains its maximum and that
\(c_\star<69/50\), using a two-regime elasticity estimate and exact
rational log-series margins.  It also rechecks the same KKT scale
\(\eta=\lambda/2\).  Thus (32Z1) now uses the exact scalar variational
constant; uniqueness of its numerically observed stationary point is not
needed or claimed.

A hostile audit also verified the growing-tube tradeoff
(32Z16a)--(32Z16c), including the virtual analytic-center start correction,
the \(o(m^{2/3})\) endpoint condition, and the
\(o((\log m)^{1/3})\) threshold for a diverging centrality overhead.  It
repaired three LaTeX transcription defects; subsequent validation passed.

A final hostile audit verified the feasible primal--dual transfer
(32Z20b).  It checked the \(t=1\) Hessian restriction, domination by the
full product metric, and the weak-duality conversion from final gap to
primal accuracy.  The same audit verified the sign, \(\mu\)-scaling, and
pullback dual-norm contraction in the standard centrality-residual
formulation (32Z20c)--(32Z20d).  No correction was needed.
