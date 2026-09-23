# Exact radial distance and centrality tax on every Jordan spectral interval

Status: Core, unequal-scale, fixed-profile, activation-order, and
same-accuracy refinements independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the calculations; priority not claimed

## Result

Let \(V\) be any Euclidean Jordan algebra of rank \(R\), with cone of
squares \(K\), unit \(e\), and standard trace inner product. This includes
Lorentz, real/complex/quaternionic PSD, and exceptional Albert factors.
For the cone barrier \(F_\alpha(x)=-\alpha\log\det x\), the same spectral
argument first gives the classical radial formula
\[
 d_{F_\alpha}(e,x)
   =\sqrt\alpha\left(\sum_{i=1}^R\log^2\lambda_i(x)\right)^{1/2}.
                                                                    \tag{0}
\]
More generally one applies (0) to the relative spectrum after the
quadratic-representation isometry sending the reference point to \(e\).
This exact part extends blockwise to every classified self-scaled barrier.

The nontrivial active-rank centrality comparison needs a bounded problem.
On the symmetric spectral interval
\[
             \Omega=\{x\in V:-e\prec_Kx\prec_Ke\},
\]
use the scaled standard log-determinant potential
\[
 \Phi_\alpha(x)
 =-\alpha\log\det(e-x^2)
 =-\alpha\log\det(e-x)-\alpha\log\det(e+x),
 \qquad \alpha>0.                                               \tag{1}
\]
For \(\alpha\geq1\), it is the restriction of the classified blockwise
self-scaled barrier on \(K\times K\) with equal weights. The
Hessian-metric statements hold for every positive scale.

Define
\[
 \rho(t)=\int_0^t{\sqrt{2(1+u^2)}\over1-u^2}\,du,\qquad0\leq t<1.
                                                                    \tag{2}
\]
If \(\lambda_1(x),\ldots,\lambda_R(x)\) are the Jordan eigenvalues of
\(x\), then the exact center-to-point Hessian-metric distance is
\[
 \boxed{\displaystyle
d_{\Phi_\alpha}(0,x)
   =\sqrt{\alpha}\left(\sum_{i=1}^R
                  \rho(|\lambda_i(x)|)^2\right)^{1/2}.}          \tag{3}
\]
Thus arbitrary Peirce/off-frame motion cannot shorten a radial spectral
path. The formula depends on cone rank, not cone dimension or Peirce
constant.

More generally, if eigenvalues are arranged in decreasing order and
\(\rho\) is extended oddly, the same proof gives the global contraction
\[
 d_{\Phi_\alpha}(x,y)\geq\sqrt\alpha\,
   \|\rho(\lambda^\downarrow(x))-
             \rho(\lambda^\downarrow(y))\|_2.                   \tag{3a}
\]
Equality holds when the endpoints share an ordered Jordan frame and one
interpolates linearly in their \(\rho\)-coordinates.

Now let \(c\in V\) have nonzero Jordan eigenvalues
\(\mu_1,\ldots,\mu_r\), where
\(|\mu_1|\geq\cdots\geq|\mu_r|>0\). The central path for
\[
                \min_{x\in\Omega}-\langle c,x\rangle
\]
has the same Jordan frame as \(c\), with active eigenvalues
\[
 \lambda_i(x(\eta))
  =\operatorname{sgn}(\mu_i)\,
       r\!\left({\eta|\mu_i|\over\alpha}\right),\qquad
 r(z)={z\over1+\sqrt{1+z^2}},                                  \tag{4}
\]
and zero inactive eigenvalues. If \(L_{\rm cent}(0,\eta_f)\) denotes its
arc length from the analytic center to \(x(\eta_f)\), then
\[
 \boxed{\displaystyle
 d_{\Phi_\alpha}(0,x(\eta_f))
 \leq L_{\rm cent}(0,\eta_f)
 \leq\Gamma_r\,d_{\Phi_\alpha}(0,x(\eta_f)),}                   \tag{5}
\]
where
\[
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
            ={1\over4}\log r+O(1).                              \tag{6}
\]
The order \(\Gamma_r=\Theta(\sqrt{\log r})\) is sharp whenever the cone
rank is at least \(r\). Hence the largest same-endpoint tax for following
this exact central path is controlled by the **active spectral rank**
\(r\), not the full cone rank \(R\).

For a product of Jordan factors with a common scale \(\alpha\), pool the
active eigenvalues and the same statements hold with sums over all
factors.  Unequal self-scaled weights admit an explicit scale-sensitive
interpolation bound.  Index all active eigenvalue channels in increasing order
of their activation thresholds
\(a_i=\log(\alpha_i/w_i)\), where \(\alpha_i\) is the scale of the
channel's factor, and put
\[
 S_i=\sum_{k\leq i}\alpha_k,\qquad S_0=0,\qquad
 \Gamma_{\boldsymbol\alpha,a}^2
   =\sum_{i=1}^r{\alpha_i\over
            (\sqrt{S_i}+\sqrt{S_{i-1}})^2}.                     \tag{7}
\]
Then
\[
 L_{\rm cent}\leq\Gamma_{\boldsymbol\alpha,a}\,
                   d_\Phi(0,x(\eta_f)),\qquad
 \Gamma_{\boldsymbol\alpha,a}\leq\sqrt r.                     \tag{7'}
\]
Equal scales recover \(\Gamma_r\) exactly.  The order \(\sqrt r\) is
attainable over admissible unequal scales, already on products of
rank-one EJAs, so it cannot be uniformly improved without controlling the
scale profile.  More strongly, for every fixed positive ordered scale
profile, \(\Gamma_{\boldsymbol\alpha,a}\) is the exact supremum over
objectives and terminal central parameters; the supremum may require a
limiting separation of activation thresholds.

For one EJA, and for common-scale products after pooling the nonzero
weights \(w_i=|\mu_i|\), the exact distance to objective error
\(\epsilon\in(0,\sum_iw_i)\) is the same scalar water-filling problem:
\[
 \boxed{\displaystyle
 L_{\rm opt}(\epsilon)
 =\sqrt\alpha\min_{\substack{0\leq x_i<1\\
                    \sum_iw_i(1-x_i)\leq\epsilon}}
             \left(\sum_i\rho(x_i)^2\right)^{1/2}.}              \tag{7a}
\]
The unique endpoint satisfies
\[
 2\alpha\rho(x_i)\rho'(x_i)=\lambda w_i,\qquad
 \sum_iw_i(1-x_i)=\epsilon.                                    \tag{7b}
\]
If \(\alpha\geq1\) and every forward chord has starting Dikin norm at most
\(\delta<1\), the optimal number \(T_\delta^\star(\epsilon)\) obeys
\[
 {L_{\rm opt}(\epsilon)\over-\log(1-\delta)}
 \leq T_\delta^\star(\epsilon)
 \leq\left\lceil{L_{\rm opt}(\epsilon)\over\log(1+\delta)}
       \right\rceil.                                            \tag{7c}
\]

Let \(L_{\rm CP}(\epsilon)\) stop the central path at its first
\(\epsilon\)-accurate point.  Define the exact scalar dilation
\[
 c_\star=\max_{y>0}{p^{-1}(yp'(y))\over y},\qquad
 p(y)=b'(\rho^{-1}(y)),\quad b(x)=-\log(1-x^2).
\]
The independently audited
[`exact scalar-dilation note`](2026-09-04-exact-scalar-centrality-dilation.md)
proves \(1<c_\star<69/50\).
The stronger same-accuracy comparison is
\[
 L_{\rm CP}(\epsilon)
 \leq c_\star\Gamma_rL_{\rm opt}(\epsilon)
 <{69\over50}\Gamma_rL_{\rm opt}(\epsilon),                   \tag{7d}
\]
and the worst ratio over active eigenvalue lists and accuracies is
\(\Theta(\sqrt{\log r})\). Thus the sharp centrality tax survives unchanged
from rectangular matrix balls to every EJA type.

There is also a discrete short-step separation.  On the standard-scale
sharp family, every forward-\(R\)-Dikin sequence that starts at the
analytic center, returns an actually \(\epsilon\)-accurate point, and
stays in a fixed geodesic tube—or in a fixed Newton-decrement
neighborhood—of arbitrarily labeled central points needs
\(\Omega(r\log r)\) rounds.  An unrestricted noncentral sequence needs
only \(\Theta(r\sqrt{\log r})\).  No monotonicity of the reference
central parameters is assumed.

## 1. Spectral Hessian proof of the exact distance

Put \(f(t)=-\log(1-t^2)\). Then
\(\Phi_\alpha(x)=\alpha\,\operatorname{tr}f(x)\) and
\[
             f''(t)={2(1+t^2)\over(1-t^2)^2}=\rho'(t)^2.         \tag{8}
\]
Along an absolutely continuous path \(x(t)\), choose a Jordan frame
diagonalizing \(x(t)\), and diagonalize the derivative inside every
repeated-eigenvalue Peirce algebra. The spectral Hessian formula has
diagonal part
\[
 \alpha\sum_i f''(\lambda_i)\dot\lambda_i^2
\]
and off-diagonal Peirce terms whose coefficients are divided differences
of the increasing function \(f'\). Convexity of \(f\) makes all those
coefficients nonnegative. Consequently, almost everywhere,
\[
 \|\dot x\|_{\Phi_\alpha,x}^2
 \geq\alpha\sum_i f''(\lambda_i)\dot\lambda_i^2
 =\alpha\left\|{d\over dt}
       (\rho(\lambda_1),\ldots,\rho(\lambda_R))\right\|_2^2.     \tag{9}
\]
Use the odd extension of \(\rho\) in the last expression. Jordan
eigenvalues are locally Lipschitz, so the formula remains valid across
repeated and zero eigenvalues almost everywhere.

Integrating (9) and applying the Euclidean endpoint inequality proves the
lower half of (3). For the reverse inequality, fix a Jordan frame for
\(x\), keep it fixed, and move every eigenvalue linearly in its
\(\rho\)-coordinate. All off-diagonal Peirce velocities vanish, and (9)
is equality with constant speed. This proves (3), including the Albert
algebra because only its spectral theorem and Peirce decomposition are
used.

## 2. Central path and the \(\Gamma_r\) upper bound

The first-order equation is
\[
 \alpha\,{2x\over e-x^2}=\eta c
\]
in Jordan functional calculus. It proves (4). Put
\[
 s=\log\eta,\qquad a_i=\log{\alpha\over|\mu_i|},
\]
and define the scaled radial coordinates
\[
 y_i(s)=\sqrt\alpha\,
   \rho\!\left(r(e^{s-a_i})\right).
\]
Direct differentiation gives
\[
 \dot y_i(s)=\sqrt\alpha\,
 \left(1-{1\over\sqrt{1+e^{2(s-a_i)}}}\right)^{1/2}.             \tag{10}
\]
Since \(a_1\leq\cdots\leq a_r\), these nonnegative velocities are
decreasing in \(i\). For every decreasing nonnegative vector \(v\), set
\(\delta_j=v_j-v_{j+1}\), \(v_{r+1}=0\). The prefix decomposition and
triangle inequality give
\[
 \|v\|_2
 \leq\sum_{j=1}^r\sqrt j\,\delta_j
 =\sum_{i=1}^r(\sqrt i-\sqrt{i-1})v_i.                          \tag{11}
\]
Integrating (11), then applying Cauchy--Schwarz, yields
\[
 L_{\rm cent}
 \leq\Gamma_r\|(y_i(s_f))_i\|_2.
\]
Equation (3) identifies the last norm with the endpoint distance, proving
(5). The asymptotic in (6) follows from
\(\sqrt i-\sqrt{i-1}=1/(\sqrt i+\sqrt{i-1})\).

## 3. Exact objective-sublevel distance and optimal Dikin moves

The Fan--Theobald--von Neumann inequality for EJAs gives
\[
 \langle c,x\rangle\leq\sum_i|\mu_i|\,|\lambda_i(x)|
\]
after arranging magnitudes in decreasing order. Hence objective accuracy
implies \(\sum_iw_i(1-|\lambda_i(x)|)\leq\epsilon\). Formula (3) shows
that inactive eigenvalues only increase distance. Conversely, choose the
Jordan frame of \(c\), give each active eigenvalue the sign of \(\mu_i\),
and set all inactive eigenvalues to zero. This realizes every scalar
choice in (7a), proving the exact reduction.

The squared objective in (7a) is strictly convex because
\[
 (\rho^2)''=2[(\rho')^2+\rho\rho'']>0.
\]
Every coordinate is strictly between zero and one, and the error
constraint is active. Its KKT equations are (7b); the factor \(\alpha\)
can of course be absorbed into \(\lambda\).

The \(\rho\)-linear fixed-frame path to the water-filled endpoint is
globally shortest by (3). Partitioning it into arclength pieces
\(\log(1+\delta)\) makes every forward chord have starting Dikin norm at
most \(\delta\). Conversely, the straight segment associated with one
such chord has length at most \(-\log(1-\delta)\). Concatenation and (7a)
prove (7c).

For the same-accuracy comparison, put \(y=\rho(x)\),
\(b(x)=-\log(1-x^2)\), \(x(y)=\rho^{-1}(y)\), and
\[
                   p(y)=b'(x(y)),\qquad p'(y)=\rho'(x(y)).
                                                                    \tag{11a}
\]
The function \(p'\) is increasing and convex.  Indeed,
\[
 {d\over dy}p'(y)={x\over1+x^2}+{2x\over1-x^2},
\]
whose derivative with respect to \(x\) is
\[
 {1-x^2\over(1+x^2)^2}+{2(1+x^2)\over(1-x^2)^2}>0.
\]
For the sharper dilation estimate define
\[
 E(y)={yp'(y)\over p(y)}\geq1.
\]
Direct differentiation, with \(x=\rho^{-1}(y)\), gives
\[
 {dE\over d\log y}
 =E-{y^2(1-x^2)\over2x^2(1+x^2)}\geq E-1.                     \tag{11b}
\]
The last inequality follows from
\[
 \rho(x)\leq\sqrt2\,x\sqrt{1+x^2\over1-x^2};
\]
both sides vanish at zero, and the ratio of the right derivative to
\(\rho'(x)\), after writing \(u=x^2\), is
\[
 {1+2u-u^2\over(1+u)\sqrt{1-u}}\geq1,
\]
as follows by squaring and simplifying to
\(u(3+3u-3u^2+u^3)\geq0\).

For comparison, let \(\kappa_0=1.391010896\ldots\) be the unique root in
\((1,2)\) of
\(\log[\kappa_0(\kappa_0-1)]+2-\kappa_0=0\).  Integrating (11b) gives
\[
 E(ty)\geq1+t(E(y)-1)\qquad(t\geq1),
\]
and therefore
\[
 \log{p(\kappa y)\over p(y)}
 \geq\log\kappa+(\kappa-1)(E(y)-1).
\]
For \(\kappa=\kappa_0\), the right side is at least \(\log E(y)\) for
every \(E(y)\geq1\); its minimum occurs at
\(E=1/(\kappa_0-1)\), and the defining equation for \(\kappa_0\) makes
that minimum zero.  Hence
\[
                         p(\kappa_0y)\geq yp'(y).               \tag{11c}
\]

Let \(y_i^\star=\rho(x_i^\star)\) be the exact optimizer in (7a), with
multiplier \(\lambda\).  At central parameter \(\eta=\lambda/2\), its
coordinates \(y_i^{\rm c}\) satisfy
\[
 p(y_i^{\rm c})={\lambda w_i\over2\alpha}
                 =y_i^\star p'(y_i^\star).                    \tag{11d}
\]
Since \(p(y)\leq yp'(y)\), while the definition of \(c_\star\) supplies the
exact reverse comparison at \(c_\star y\), one has
\(y_i^\star\leq y_i^{\rm c}\leq c_\star y_i^\star\).
This central point is already accurate.  The first accurate point occurs
no later and is coordinatewise no larger, so its exact distance is at
most \(c_\star L_{\rm opt}(\epsilon)\).  Equation (5) proves (7d), with
all \(\sqrt\alpha\) factors cancelling.  The certified constant
\(\kappa_0\) from (11c) remains a weaker self-contained bound.

## 4. Sharpness

Every rank-\(r\) EJA contains the diagonal Jordan subalgebra generated by
a Jordan frame, isomorphic to \(\mathbb R^r\). Choose
\[
 S_r=\sum_{j=1}^{r-1}j^{-3/2},\qquad
 a_i={T\over S_r}\sum_{j=1}^{i-1}j^{-3/2},\qquad
 |\mu_i|=\alpha e^{-a_i}.                                      \tag{12}
\]
At the central endpoint \(s_f=T\), the same scalar estimates as for the
spectral matrix ball give
\[
 L_{\rm cent}=\Omega(\sqrt\alpha\,T\log r),\qquad
 d_{\Phi_\alpha}(0,x(e^T))
   =O(\sqrt\alpha\,[T\sqrt{\log r}+\sqrt{r}]),                  \tag{13}
\]
with constants independent of the EJA type. Taking
\(T\geq\sqrt{r/\log r}\) proves a
\(\Theta(\sqrt{\log r})\) ratio. Since (3) excludes all noncommuting
shortcuts, this proves sharpness in the full Jordan domain, not only in
the diagonal subalgebra.

For the sharper same-accuracy lower example, take \(T=r\),
\(|\mu_i|=\alpha e^{-a_i}\), and
\(\epsilon=\alpha r e^{-T}\). At log-parameter \(T-1\), all but
\(O(\sqrt r)\) scalar channels have \(e^{T-1-a_i}\geq1\), so the central
error is still above \(\epsilon\); at \(T\) it is at most \(\epsilon\).
Truncating the harmonic lower estimate in (13) therefore leaves
\[
 L_{\rm CP}(\epsilon)=\Omega(\sqrt\alpha\,r\log r).
\]
The explicit logarithmically allocated endpoint has error exactly
\(\epsilon\) and distance
\(O(\sqrt\alpha\,r\sqrt{\log r})\). This proves the lower half of the
\(\Theta(\sqrt{\log r})\) same-accuracy claim in (7d).

### 4.1 Discrete central-neighborhood round separation

The same family gives a discrete, rather than merely arclength,
separation for the standard scale \(\alpha=1\); here choose all
\(\mu_i=+e^{-a_i}\), so \(c\succeq0\).  Let
\(s_\epsilon\) be the first log-parameter whose central point is
\(\epsilon\)-accurate.  Fix \(R<1\) and \(\delta<\infty\), and consider
feasible iterates \(z_0,\ldots,z_N\), starting at \(z_0=0\), such that
\(z_N\) is \(\epsilon\)-accurate and, for arbitrary real labels \(s_k\),
\[
 \|z_{k+1}-z_k\|_{\Phi,z_k}\leq R,\qquad
 d_\Phi(z_k,x(e^{s_k}))\leq\delta.                              \tag{13b}
\]
For (12) with \(T=r\) and \(\epsilon=re^{-T}\), every such sequence
obeys
\[
               N=\Omega_{R,\delta}(r\log r),                    \tag{13c}
\]
whereas the optimal unrestricted noncentral bounded-Dikin sequence has
\[
               T_R^\star(\epsilon)=\Theta_R(r\sqrt{\log r}).    \tag{13d}
\]
The statement also holds after pooling eigenvalue channels from a
common-scale product of EJAs.

Indeed, one round changes the two labeled centers by points at distance at
most
\(C_{R,\delta}=2\delta-\log(1-R)\).  The centers have a shared Jordan
frame, so equality in (3a) gives their exact two-center Euclidean distance in
\(\rho\)-coordinates.  Put
\(\ell_k=\min\{s_k,s_{k+1}\}\).  If
\(\ell_k\in[a_j,a_{j+1})\), the first \(j\) coordinate velocities
throughout the interval between the labels are at least
\(v_0=\sqrt{1-1/\sqrt2}\), and hence
\[
 |s_{k+1}-s_k|\leq {C_{R,\delta}\over v_0\sqrt j}.              \tag{13e}
\]
Set \(J=\lfloor r^{2/3}\rfloor\),
\(q(s)=|\{i:a_i\leq s\}|\), and
\[
 \mathcal P(s)=\int_0^{\min\{\max\{s,0\},a_J\}}\sqrt{q(u)}\,du.
                                                                    \tag{13f}
\]
Because
\(a_{j+1}-a_j=r/(S_rj^{3/2})\geq1/S_r\) for \(j\leq J\), (13e)
shows that one round crosses only \(O_{R,\delta}(1)\) thresholds and
changes \(\mathcal P\) by \(O_{R,\delta}(1)\) in absolute value.  A
crossing involving labels below the first active threshold is also
bounded by the first \(\rho\)-coordinate.  On the other hand,
\[
 \mathcal P(a_J)={r\over S_r}\sum_{j<J}{1\over j}
                 =\Omega(r\log r).
\]
It remains to derive the required endpoint progress from the actual
iterates rather than assume it through their labels.  At the start,
(3a) and \(z_0=0\) give \(Q(s_0)\leq\delta\), so
\(\mathcal P(s_0)=O_\delta(1)\).  At the end, all eigenweights in (12)
are positive and \(w_1=1\).  Fan--Theobald--von Neumann gives
\[
 \sum_iw_i-\langle c,z_N\rangle
 \geq\sum_iw_i(1-\lambda_i^\downarrow(z_N)).
\]
Every term on the right is positive.  With
\(\epsilon=re^{-r}\), accuracy therefore implies
\(\lambda_1^\downarrow(z_N)\geq1-re^{-r}\), and hence
\[
 \rho(\lambda_1^\downarrow(z_N))\geq r-\log r.
\]
Applying (3a) to the final tube and writing
\(Q(s)=\rho(r(e^s))\) gives
\[
 Q(s_N)\geq r-\log r-\delta.
\]
Since \(Q(s)\leq Q(0)+s\) for \(s\geq0\), this forces
\(s_N\geq r-\log r-\delta-Q(0)>a_J\) for large \(r\).
Telescoping absolute progress changes now proves (13c), even with
backtracking and without any endpoint-label assumption.
Equations (7c), (7d), and the matching endpoint construction give
(13d).  This is a theorem for fixed geodesic-radius neighborhoods, not
for every IPM neighborhood definition.

The geodesic-tube hypothesis contains the conventional fixed
Newton-decrement neighborhood.  For
\[
 f_\eta(z)=\Phi(z)-\eta\langle c,z\rangle,\qquad
 \lambda_\eta(z)=\|\nabla f_\eta(z)\|_{\Phi,z,*},
\]
self-concordant Hessian comparison along the segment from \(z\) to the
minimizer \(x(\eta)\) gives
\[
 \|x(\eta)-z\|_{\Phi,z}
 \leq{\lambda_\eta(z)\over1-\lambda_\eta(z)}.
\]
Hence, if \(\lambda_\eta(z)\leq\beta<1/2\),
\[
 d_\Phi(z,x(\eta))
 \leq\log{1-\beta\over1-2\beta}=:\delta_\beta.                 \tag{13g}
\]
Substituting \(\delta_\beta\) in (13c) proves
\[
 N=\Omega_{R,\beta}(r\log r)                                   \tag{13h}
\]
for every sequence of forward \(R\)-Dikin steps that starts at the
analytic center, maintains
\(\lambda_{e^{s_k}}(z_k)\leq\beta<1/2\) for arbitrary reference labels,
and returns an actually \(\epsilon\)-accurate iterate.  This is a direct
short-step iteration lower bound for the explicit standard-barrier
family, not a quantum-query lower bound.

## 5. Unequal self-scaled weights: explicit interpolation and sharp worst case

For a product \(V=\prod_jV_j\) with
\[
 \Phi(x)=\sum_j\alpha_j\Phi_1(x_j),
\]
Riemannian products and (3) give
\[
 d_\Phi(0,x)^2
   =\sum_j\alpha_j\sum_k\rho(|\lambda_{jk}(x_j)|)^2.             \tag{14}
\]
The central path still separates spectrally, with arguments
\(\eta|\mu_{jk}|/\alpha_j\).  After ordering activation thresholds, write
its coordinate velocities as \(\sqrt{\alpha_i}h_i(s)\), where
\(h_1(s)\geq\cdots\geq h_r(s)\geq0\).  With \(h_{r+1}=0\), the prefix
decomposition and triangle inequality give
\[
 \left(\sum_i\alpha_ih_i^2\right)^{1/2}
 \leq\sum_{j=1}^r\sqrt{S_j}(h_j-h_{j+1})
 =\sum_{i=1}^r(\sqrt{S_i}-\sqrt{S_{i-1}})h_i.                  \tag{15}
\]
Integrate, put \(q_i=\int h_i\), and apply weighted Cauchy--Schwarz:
\[
 L_{\rm cent}
 \leq\left[\sum_i{(\sqrt{S_i}-\sqrt{S_{i-1}})^2\over\alpha_i}
       \right]^{1/2}
       \left(\sum_i\alpha_iq_i^2\right)^{1/2}.
\]
The first factor is exactly (7), and the second is the endpoint distance
(14).  Each summand in (7) is at most one, proving (7').  There is also a
useful logarithmic refinement.  For \(i\geq2\), put
\(t_i=\alpha_i/S_{i-1}\).  The \(i\)-th summand of (7) is
\[
 { \sqrt{1+t_i}-1\over\sqrt{1+t_i}+1}
 =\tanh\!\left({1\over4}\log{S_i\over S_{i-1}}\right)
 \leq {1\over4}\log(1+t_i)
 ={1\over4}\log{S_i\over S_{i-1}},
\]
where the inequality is \(\tanh z\leq z\).  Since the first summand equals
one,
\[
 \boxed{\displaystyle
 \Gamma_{\boldsymbol\alpha,a}^2
 \leq1+{1\over4}\log{S_r\over S_1}
 \leq1+{1\over4}\log{S_r\over\alpha_{\min}}.}                  \tag{15a}
\]
Here \(S_1=\alpha_1\) is the scale of the **first-activated** channel; it
need not equal \(\alpha_{\min}\).  The second inequality is the safe
order-free corollary.

There is an exact finite-\(r\) envelope at fixed total scale ratio.  Put
\[
 Z={1\over4}\log{S_r\over S_1}.
\]
The increments
\(z_i=\frac14\log(S_i/S_{i-1})\), \(i\geq2\), are nonnegative and sum to
\(Z\).  Concavity of \(\tanh\) on the positive half-line and Jensen's
inequality give
\[
 \boxed{\displaystyle
 \Gamma_{\boldsymbol\alpha,a}^2
 \leq1+(r-1)\tanh\!\left({1\over4(r-1)}
                    \log{S_r\over S_1}\right)
 \leq\min\!\left\{r,\,
           1+{1\over4}\log{S_r\over S_1}\right\}.}              \tag{15b}
\]
Equality in the first bound holds exactly when the cumulative masses are
geometric, \(S_i/S_{i-1}\) constant for \(i\geq2\).  Rescaling all
\(\alpha_i\) makes such profiles compatible with any common lower bound on
the classified scales.  Replacing \(S_1\) by \(\alpha_{\min}\) in the
right-hand side of the first inequality in (15b) gives a weaker but
order-free version.

For classified scales \(\alpha_i\geq1\), this is at most
\(1+\frac14\log S_r\).  Here \(S_r\) is the active weight-rank mass,
bounded by the total block weight-rank mass and hence by the conventional
two-copy product-barrier parameter up to its fixed normalization.

For common scales, (7) is exactly \(\Gamma_r^2\), and (15a)--(15b) have
the correct leading term \(\frac14\log r\).  For cumulative-geometric
scales, (15b) is exact.  The construction (16) has this geometry up to
constant factors and therefore realizes
\(\Gamma_{\boldsymbol\alpha,a}^2=\Theta(r)\) when its fixed geometric
ratio is bounded away from one.

The coefficient in (7) is not merely a convenient upper bound: it is the
exact profilewise supremum.  Fix any ordered positive vector
\(\boldsymbol\alpha=(\alpha_1,\ldots,\alpha_r)\), and write
\[
 \beta_i=\sqrt{S_i}-\sqrt{S_{i-1}},\qquad
 c_i={\beta_i\over\alpha_i}
    ={1\over\sqrt{S_i}+\sqrt{S_{i-1}}}.                          \tag{15c}
\]
The numbers \(c_1>\cdots>c_r>0\) are strictly decreasing.  For the scalar
sigmoid \(h\) and its integral \(Q\) below, choose \(M\to\infty\) and set
\[
 u_i=Q^{-1}(Mc_i),\qquad
 |\mu_i|=\alpha_i e^{u_i},\qquad s_f=0.                         \tag{15d}
\]
The activation thresholds are \(-u_1<\cdots<-u_r\), so the prescribed
scale order is unchanged.  At the endpoint the unscaled radial
displacements are
\[
 q_i=Q(u_i)=Mc_i,
\]
and hence weighted Cauchy--Schwarz in (15) is exactly tight:
\[
 d_\Phi^2=M^2\sum_i\alpha_i c_i^2
          =M^2\Gamma_{\boldsymbol\alpha,a}^2.                   \tag{15e}
\]

It remains to check the prefix triangle inequality.  The scalar profile
satisfies
\[
 \int_{\mathbb R}|h(t)-\mathbf 1_{\{t>0\}}|\,dt<\infty,
 \qquad Q(u)=u+\kappa+o(1)\quad(u\to\infty).
\]
Thus \(u_i=Mc_i-\kappa+o(1)\), and every consecutive threshold separation
tends to infinity.  Replacing the translated sigmoids by their step
profiles changes total arclength by only
\(O_{\boldsymbol\alpha}(1)\).  The step profiles activate one weighted
prefix at a time, so summation by parts gives
\[
 \begin{aligned}
 L_{\rm step}
 &=\sum_{i=1}^r\beta_i u_i\\
 &=M\sum_i{\beta_i^2\over\alpha_i}
      +O_{\boldsymbol\alpha}(1)
  =M\Gamma_{\boldsymbol\alpha,a}^2
      +O_{\boldsymbol\alpha}(1).
 \end{aligned}                                                   \tag{15f}
\]
Combining (15e)--(15f) with the upper bound (7) proves
\[
 \boxed{\displaystyle
 \sup_{\substack{\mu,\eta_f\\a_1<\cdots<a_r}}
 {L_{\rm cent}(0,\eta_f)\over
      d_\Phi(0,x(\eta_f))}
 =\Gamma_{\boldsymbol\alpha,(1,\ldots,r)}                      \tag{15g}
\]
for every fixed ordered positive scale profile, already on a product of
rank-one EJAs.  Here the objectives in (15d) enforce that activation order;
the notation on the right records the prescribed order.  For \(r>1\), the smooth
sigmoid generally approaches rather than attains the supremum.  The limit
also uses growing objective dynamic range, so (15g) is a geometric
sharpness theorem, not an input-efficient complexity lower bound.

For a fixed **unordered multiset** of channel scales, the worst activation
order is also explicit: activate scales in nondecreasing order.  Conversely,
nonincreasing order minimizes the coefficient.  To see this, fix a preceding
mass \(S>0\) and two adjacent masses \(a\leq b\).  With
\(\psi(t)=\tanh(t/4)\), their contribution in the order \(a,b\) is
\[
 \psi\!\left(\log{S+a\over S}\right)
 +\psi\!\left(\log{S+a+b\over S+a}\right).                       \tag{15h}
\]
The two arguments have fixed sum
\(\log[(S+a+b)/S]\).  Moreover,
\[
             (S+a)(S+b)\geq S(S+a+b),
\]
so the split generated by putting \(a\) first is at least as close to the
equal split as the one generated by putting \(b\) first.  Since
\(\psi\) is increasing and concave, the symmetric sum in (15h) is largest
for the closer split.  If the pair starts the order, its first contribution
is always one and the second is larger when the smaller mass comes first.
Adjacent exchanges now prove
\[
 \max_{\pi}\Gamma_{\pi(\boldsymbol\alpha)}=
       \Gamma_{\boldsymbol\alpha^\uparrow},\qquad
 \min_{\pi}\Gamma_{\pi(\boldsymbol\alpha)}=
       \Gamma_{\boldsymbol\alpha^\downarrow}.                   \tag{15i}
\]
Together with (15g), this completely characterizes the supremum when the
scales are fixed but objectives may choose their activation order.

The \(\sqrt r\) order is sharp.  It suffices to use a product of \(r\)
rank-one EJAs.  Let
\[
 h(u)=\sqrt{1-{1\over\sqrt{1+e^{2u}}}},\qquad
 Q(u)=\int_{-\infty}^uh(v)\,dv=\rho(r(e^u)).
\]
Fix \(B\geq4\), take \(U\) large, set \(u_i=UB^{r-i}\), and stop at
\(s_f=0\).  Put
\[
 H=Q(u_1),\qquad
 \sqrt{\alpha_i}={H\over Q(u_i)},\qquad
 |\mu_i|=\alpha_i e^{u_i}.                                    \tag{16}
\]
Then \(\alpha_i\geq1\), the activation threshold is \(-u_i\), and every
final radial displacement equals \(H\).  Thus the endpoint distance is
\(H\sqrt r\).  On each of the disjoint intervals
\([ -u_i+M,-u_{i+1}-M]\) (and \([-u_r+M,0]\) last), the \(i\)-th speed is
at least \(\sqrt{\alpha_i}h(M)\).  For fixed \(M>0\), large \(U\), and
the elementary bound \(Q(u)=\Theta(u)\) for \(u\geq U\), each interval
contributes \(\Omega(H)\).  Hence
\[
              L_{\rm cent}=\Theta(Hr),\qquad
 {L_{\rm cent}\over d_\Phi(0,x(1))}=\Theta(\sqrt r).           \tag{17}
\]
For these geometrically growing scales, \(\alpha_i\) dominates the
preceding prefix sum, so \(\Gamma_{\boldsymbol\alpha,a}=\Theta(\sqrt r)\)
as well.  Thus (7) captures the correct worst-case scale sensitivity.

The objective-sublevel theorem also has a fully weighted form:
\[
 L_{\rm opt}(\epsilon)
 =\min_{\sum_iw_i(1-x_i)\leq\epsilon}
       \left(\sum_i\alpha_i\rho(x_i)^2\right)^{1/2}.            \tag{18}
\]
Its logarithmic surrogate minimizes \(\sum_i\alpha_i s_i^2\), and its
unique KKT point is
\[
 s_i=W\!\left({\gamma w_i\over\alpha_i}\right),\qquad
              \sum_i\alpha_i s_i=\gamma\epsilon.               \tag{19}
\]
The exact-coordinate proof (11a)--(11d) is unchanged: weighted endpoint
KKT gives
\(2\alpha_i y_i^\star p'(y_i^\star)=\lambda w_i\), while the central
equation at \(\eta=\lambda/2\) gives
\(\alpha_ip(y_i^{\rm c})=\lambda w_i/2\).  Thus
\(y_i^\star\leq y_i^{\rm c}\leq c_\star y_i^\star\), and therefore
\[
 L_{\rm CP}(\epsilon)
   \leq c_\star\Gamma_{\boldsymbol\alpha,a}
                    L_{\rm opt}(\epsilon).                      \tag{20}
\]
This order is sharp uniformly over unequal classified scales.  In (16),
choose \(\epsilon\) to be the central objective error at \(\eta=1\).
Strict monotonicity makes this the first accurate central point; (17)
gives central length \(\Theta(Hr)\), while that same feasible endpoint
shows \(L_{\rm opt}(\epsilon)\leq H\sqrt r\).  Hence the worst
same-accuracy ratio is \(\Theta(\sqrt r)\).

The same example has a discrete version.  Fix \(M>0\), take \(U\) large
enough that every core interval
\[
 I_i=[-u_i+M,-u_{i+1}-M]\quad(i<r),\qquad
 I_r=[-u_r+M,0]
\]
is nonempty, and let the central labels satisfy only
\(s_0\leq-u_1+M\) and \(s_N\geq0\); intermediate labels may backtrack.
Suppose iterates remain within geodesic distance \(\delta\) of
their labeled centers and use forward Dikin chords of radius \(R<1\).
As in (13), consecutive centers are at distance at most
\(C_{R,\delta}=2\delta-\log(1-R)\).  The \(i\)-th radial coordinate gains
\(\Omega(H)\) across \(I_i\).  Define scalar progress as the sum of each
core's clipped \(i\)-th radial-coordinate gain.  Choose \(U\) so that
every full-core gain exceeds
\(C_{R,\delta}\).  A label jump can then meet at most two core intervals:
crossing three would fully cross the middle one and violate the
center-distance bound.  The sum of the at most two clipped coordinate
increments in one round has absolute value at most
\(\sqrt2C_{R,\delta}\).  The scalar progress changes by
\(\Omega(Hr)\) between the initial and final labels, so telescoping
absolute changes proves
\[
       N=\Omega_{R,\delta}(Hr).                                 \tag{21}
\]
The \(\rho\)-linear path to the same accurate endpoint uses only
\(O_R(H\sqrt r)\) chords.  Thus unequal-scale
central-neighborhood following, even without monotone labels, can have a sharp
\(\Omega(\sqrt r)\) round overhead over an explicit noncentral sequence.

The sharp family is geometric rather than an input-efficient lower-bound
instance: its scale dynamic range and objective magnitudes are exponential
in \(r\).  Consistently, (15a) shows that a \(\sqrt r\) tax requires
\(\log(S_r/\alpha_{\min})=\Omega(r)\).  For polynomially bounded
self-scaled weights the tax remains \(O(\sqrt{\log S_r})\).

## Scope and prior-art boundary

The affine-invariant distance formula on symmetric cones, Jordan spectral
calculus, and spectral Hessian divided-difference formula are classical.
In particular, symmetric-cone invariant Riemannian/Finsler geometry is
developed by [Bae and Lim
(2001)](https://doi.org/10.1515/form.2001.026), while the EJA spectral
differentiability machinery used here is adjacent to [Baes
(2007)](https://doi.org/10.1016/j.laa.2006.11.025) and [Sun and Sun
(2008)](https://doi.org/10.1287/moor.1070.0300).  Direct conic use of
spectral-function barriers is also treated by [Coey, Kapelevich, and
Vielma (2022)](https://doi.org/10.1287/moor.2022.1324).  The Bergman
metric on bounded symmetric domains is another nearby but different
geometry: its familiar radial coordinate is hyperbolic, whereas (2) is
the Hessian coordinate of the particular barrier (1).

A targeted search through 2026-09-04 found classical work on those
ingredients and on algebraic/Euclidean curvature of central paths, but no
source for the exact \(\rho\)-distance of (3), the objective-sublevel
water filling (7a), or the sharp active-rank \(\Gamma_r\) same-accuracy
tax uniformly across EJA types.  The same screen did not locate the
weighted profilewise constant (15g), its activation-order theorem (15i),
or the continuous/discrete central-neighborhood separations.  The
candidate contribution is this synthesis and its sharp constructions.
This is an **unlocated-result**
claim only, not a priority or novelty claim; specialist review remains
necessary.

This is a geometric theorem for the explicit fixed barrier (1). It is not
an iteration lower bound without a bounded-move hypothesis, not a runtime
claim, and not a statement about arbitrary coupled self-concordant
barriers.

## Audit targets

1. Check the Jordan spectral Hessian normalization and the exact
   \(\sqrt\alpha\) factors in (3), (9), and (10).
2. Check the central first-order equation and argument
   \(\eta|\mu_i|/\alpha\).
3. Check repeated/zero eigenvalues and the Albert-algebra scope.
4. Check the prefix inequality, sharp construction, and common-scale
   product extension.
5. Check the unequal-scale profilewise supremum, total-ratio envelope,
   activation-order theorem, and exponential-range caveat.
6. Check the exact objective-sublevel reduction, KKT equations, chord
   constants, and the same-accuracy \(c_\star\Gamma_r\) comparison.
7. Check both discrete central-neighborhood progress arguments without
   assuming monotone labels.

## Independent hostile audit

The audit checked the standard-trace normalization of the Jordan spectral
Hessian: its diagonal term is
\(\alpha\sum_i f''(\lambda_i)\dot\lambda_i^2\), and every off-frame Peirce
coefficient is a divided difference of the increasing function \(f'\).
It confirmed the almost-everywhere repeated/zero-eigenvalue argument and
that no associativity beyond EJA spectral calculus is used, so the Albert
case is valid. The cone and interval distance formulas have the stated
\(\sqrt\alpha\) scaling and the quadratic-representation normalization.

The audit also checked the central equation, the argument
\(\eta|\mu_i|/\alpha\), the \(\sqrt\alpha\) velocity, the prefix inequality,
the asymptotic for \(\Gamma_r\), and the sharp family including the
condition \(T\geq\sqrt{r/\log r}\). Common-scale products pool correctly.
For unequal scales the weighted velocities need not remain ordered, while
the displayed \(\sqrt r\) estimate follows from the integrated
\(\ell_1\)-to-\(\ell_2\) bound. It returned **PASS** with no mathematical
correction.

The subsequently added objective-sublevel extension was independently
re-audited.  Fan--Theobald--von Neumann gives the correct inequality
direction, and alignment in the frame of \(c\) realizes every scalar
choice, so (7a) is exact in every EJA.  Strict convexity of \(\rho^2\)
keeps every active coordinate in \((0,1)\), and its KKT equation has the
stated factor \(2\alpha\).  The global self-concordant displacement bounds
\(\log(1+\|\Delta\|_x)\leq d(x,x+\Delta)\) and the forward chord estimate
\(-\log(1-\delta)\) give both sides of (7c).

For (7d), the final sharpened proof uses exact radial coordinates.
Writing \(p(y)=b'(\rho^{-1}(y))\) and \(E(y)=yp'(y)/p(y)\), direct
calculus gives
\(dE/d\log y\geq E-1\).  The auxiliary estimate needed for this step,
\(\rho(x)\leq\sqrt2x\sqrt{(1+x^2)/(1-x^2)}\), follows by comparing
derivatives; after squaring, the difference reduces to the nonnegative
polynomial \(u(3+3u-3u^2+u^3)\) on \([0,1)\).  Integration and minimization
over \(E\geq1\) give
\(p(\kappa_0y)\geq yp'(y)\), where
\(\log[\kappa_0(\kappa_0-1)]+2-\kappa_0=0\).  The endpoint KKT system and
the central system at \(\eta=\lambda/2\) therefore imply
\(y_i^\star\leq y_i^{\rm c}\leq\kappa_0y_i^\star\).  Combining exact
distance with (5) gives \(\kappa_0\Gamma_r\), with all
\(\sqrt\alpha\) factors cancelling.  This is a certified proof constant,
not a claim of optimality.
The \(T=r\) threshold family remains inaccurate at \(T-1\) but accurate at
\(T\); deleting its final \(O(\sqrt r)\) channels does not change the
harmonic lower order, while the aligned allocated endpoint has distance
\(O(\sqrt\alpha\,r\sqrt{\log r})\).  This verifies the matching
\(\Theta(\sqrt{\log r})\) same-accuracy ratio.  No correction was needed.

The unequal-scale and discrete extensions were then independently
hostile-audited.  Ordering the unscaled sigmoid profiles \(h_i\), rather
than the weighted speeds, gives the weighted prefix decomposition (15).
Weighted Cauchy--Schwarz yields
\[
 \sum_i{(\sqrt{S_i}-\sqrt{S_{i-1}})^2\over\alpha_i}
 =\sum_i{\alpha_i\over(\sqrt{S_i}+\sqrt{S_{i-1}})^2},
\]
so (7)--(7') have the correct scales and recover \(\Gamma_r\) for equal
weights.  In (16), every endpoint displacement is \(H\); the geometrically
separated threshold intervals each contribute \(\Theta(H)\), while
\(\alpha_i\) dominates its preceding prefix.  This proves both
\(\Theta(Hr)\) arclength and \(\Theta(\sqrt r)\) sharpness.

The weighted logarithmic surrogate has KKT equations (19), while the
exact-coordinate argument applies blockwise because both endpoint and
central KKT systems carry the same factor \(\alpha_i\).  The same
\(p(\kappa_0y)\geq yp'(y)\) comparison therefore proved the earlier
certified constant \(\kappa_0\Gamma_{\boldsymbol\alpha,a}\); the exact
definition of \(c_\star\) and its audited \(69/50\) certificate now sharpen
this to (20).  Taking the
error at \(\eta=1\) is legitimate:
strict decrease of central objective error makes this exactly the first
accurate parameter.  For the discrete common-scale theorem, triangle
comparison gives the center-to-center budget
\(2\delta-\log(1-R)\); the first \(j\) sigmoid speeds then imply (13e).
Before \(J=\lfloor r^{2/3}\rfloor\), threshold gaps are uniformly bounded
below, each round changes the potential \(\mathcal P\) by \(O_{R,\delta}(1)\),
and \(\mathcal P(a_J)=\Omega(r\log r)\).  The optimal unrestricted count
follows from (7c), (7d), and the matching endpoint.  The common-scale EJA
pooling and all stated neighborhood/monotonicity qualifications are
correct.  Two malformed TeX tokens were repaired; no mathematical change
was needed.

The refinement (15a) also checks: its summand is exactly
\((\sqrt{1+t_i}-1)/(\sqrt{1+t_i}+1)\), bounded by
\(\frac14\log(1+t_i)\), and the logarithms telescope.  Hence a
\(\Theta(\sqrt r)\) weighted-prefix constant requires
\(S_r/S_1=\exp(\Omega(r))\); with polynomial scale dynamic range the tax
remains logarithmic in the active weight-rank mass.

The unequal-scale discrete paragraph was also checked independently.  The
core intervals in (21) are ordered and disjoint.  A center jump meeting
three of them must fully cross the middle interval, whose one-coordinate
gain was chosen larger than the center-distance budget.  Hence at most two
intervals contribute in one round, and the sum of their clipped coordinate
increments is at most \(\sqrt2C_{R,\delta}\) by the Euclidean
\(\rho\)-coordinate distance.  The scalar clipped progress changes by
\(\Omega(Hr)\) from the initial to the final label, so telescoping its
absolute changes proves \(\Omega_{R,\delta}(Hr)\) even when labels
backtrack.  The fixed-frame \(\rho\)-linear geodesic has
length \(H\sqrt r\), and the standard chord partition gives the stated
\(O_R(H\sqrt r)\) comparator.  No additional correction was needed.

A further independent audit made the order dependence explicit:
\(S_1=\alpha_1\) is the first-activated scale and need not equal
\(\alpha_{\min}\); substituting \(\alpha_{\min}\) gives the safe order-free
corollary in (15a).  Writing each summand as
\(\tanh[\frac14\log(S_i/S_{i-1})]\) and applying Jensen verifies the exact
fixed-ratio envelope (15b).  Equality holds for cumulative-geometric
scales.  Common scales recover the correct
\(\frac14\log r+O(1)\) behavior, while fixed-ratio geometric scales give
the sharp \(\Theta(r)\) squared factor.

The exact profilewise statement (15c)--(15i) received a separate hostile
audit.  It verified that \(c_i\) is strictly decreasing, so
\(Q^{-1}(Mc_i)\) preserves the prescribed activation order, and that the
endpoint distance is exactly \(M\Gamma_{\boldsymbol\alpha,a}\).  The
\(L^1\) error between a translated sigmoid and its step profile is finite
and translation-independent; hence the arclength error is
\(O_{\boldsymbol\alpha}(1)\), while the step arclength telescopes to
\(M\Gamma_{\boldsymbol\alpha,a}^2+O_{\boldsymbol\alpha}(1)\).
This proves the supremum in (15g).  For the ordering theorem, the two
adjacent log increments have fixed sum, the smaller-first order is closer
to an equal split, and concavity of \(\tanh\) gives the larger
contribution.  The first pair is handled separately, and adjacent
exchanges prove (15i).  The audit returned **PASS**.

The analytic-center/actual-accuracy upgrade in Section 4.1 was also
hostile-audited.  The ordered-eigenvalue contraction (3a) follows from the
same almost-everywhere EJA spectral derivative formula as (3), including
repeated spectra and the Albert algebra.  For the explicitly positive
sharp objective, Fan--Theobald--von Neumann and positivity of each
\(1-\lambda_i^\downarrow\) force the final largest eigenvalue to at least
\(1-re^{-r}\).  The tube contraction and \(Q(s)\leq Q(0)+s\) then force
the final reference label beyond \(a_J\), while the analytic-center tube
bounds initial progress.  The clipped progress proof permits arbitrary
label backtracking.  Finally, standard self-concordant Hessian comparison
gives exactly
\(\delta_\beta=\log[(1-\beta)/(1-2\beta)]\) for
\(\beta<1/2\), verifying (13g)--(13h).  The audit returned **PASS**.

The final \(\kappa_0\) sharpening was checked independently by two agents.
They verified the derivative identity for \(E=yp'/p\), the auxiliary
\(\rho\)-bound, the integration and minimization over \(E\geq1\), and the
root \(\kappa_0=1.391010896\ldots\).  They also checked that the
block scale \(\alpha_i\) cancels from the endpoint and central KKT equations
at \(\eta=\lambda/2\), so the same sandwich applies to common and unequal
self-scaled weights.  The audits returned **PASS**.  The constant is
certified but is not claimed optimal.

The later exact scalar-dilation theorem was independently hostile-audited.
It proves that the functional-inverse ratio defining \(c_\star\) attains
its maximum and that \(c_\star<69/50\), using a two-regime elasticity
argument with exact rational margins.  The audit also rechecked the
\(\eta=\lambda/2\) scale cancellation for unequal \(\alpha_i\).  Hence
(7d) and (20) now use the exact scalar variational constant rather than the
older sufficient \(\kappa_0\).  Uniqueness of the numerically observed
maximizer is not claimed.
