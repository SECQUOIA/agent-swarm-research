# A parameterized scalar-output frontier from one sparse Lorentz cone

Status: Proved; independently audited; targeted primary-source screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction and parameter accounting; moderate on novelty

## Main theorem

Fix \(K\geq3\), let \(q=2^r\), and let \(0<\delta\leq\delta_0\).
There is an SOCP with one high-dimensional Lorentz cone, row and column
sparsity \(s=\Theta(q)\), and a designated scalar optimizer coordinate
\(w^*\), such that estimating \(w^*\) to additive error \(c\delta\) solves
2-Forrelation. Full classical SQ access to every input matrix and
right-hand side is simulable with constant hidden-query overhead.

Put

\[
 \alpha_K=\log\frac{K+1}{K-1},\qquad
 \ell=\frac{\log(1/\delta)}{3\alpha_K}+O(1).
\]

Every bounded-error classical SQ algorithm for the scalar output uses

\[
 \boxed{
 Q=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right).}          \tag{1}
\]

Thus, up to the displayed polynomial denominator,

\[
 \boxed{
 Q=\exp\!\left(\Omega(K\log s\log(1/\delta))\right).}       \tag{2}
\]

A public normalized tilt of the objective makes the **optimal value
itself** carry the same decision. Approximating that value to additive
\(\Theta(\delta/\sqrt K)\) for 2-Forrelation, or
\(2^{-O(k)}\delta/\sqrt K\) for fixed \(k\)-Forrelation, has the same lower
bound. Thus the construction is not limited to state or optimizer-coordinate
output. The stronger value scale follows because the norm of the tilted
objective direction is an exactly public clock-only scalar, not an unknown
instance-dependent remainder.

The same sparse data also give a scalar-inequality LP
\(-\mathbf1\leq Mx\leq\mathbf1\). At its explicit analytic center, the
standard LP barrier has Hessian \(2M^TM\), and an explicitly SQ-accessible
objective makes the squared Newton decrement carry the same
\(\Theta(\delta/\sqrt K)\) signal. For the unperturbed objective, the entire
central path is a scalar multiple of \(M^{-1}e\); the coordinate lower bound
persists for approximate centering-subproblem gap
\(2^{-O(k)}\delta^2/K\). Thus the Newton conclusions are already lower
bounds for sparse LP path following, not only SOCP.

Unlike the companion solution-distribution lower bound, (1) has no leading
\(\delta^2\) rare-event penalty and needs no vanishing-failure output
contract. It is an ordinary bounded-error reduction to a classical number.
The ambient dimension is \(N=\Theta(Tq^\ell)\), so (1) is
\(\widetilde\Omega(\sqrt N)\). The exponent in (2) is in the sparsity
\(s\), not in the ambient dimension \(N\).

## Cyclic inverse history

Take 2-Forrelation on \(n=r\ell\) bits. Decompose each of its three global
Hadamards into \(\ell\) public \(r\)-qubit Walsh--Hadamard layers, with the
two hidden diagonal sign gates between them. After at most one public
identity padding gate, the forward circuit has even length

\[
 T=3\ell+O(1).
\]

Complete it to a \(3T\)-clock unitary \(U\): run the circuit forward for
\(T\) transitions, hold its final state for \(T\) transitions, and run the
transpose gates in reverse for the final \(T\) transitions. Then
\(U^{3T}=I\), and a block-diagonal gauge change maps \(U\) to a cyclic
shift tensor the identity. Every row and column of \(U\) has at most \(q\)
nonzeros.

Set

\[
 \gamma=\frac{K-1}{K+1},\qquad
 M=\frac{I-\gamma U}{1+\gamma}.
\]

The singular values of \(M\) are

\[
 \frac{|1-\gamma\omega|}{1+\gamma},\qquad \omega^{3T}=1.
\]

The even clock length supplies both \(\omega=1\) and \(\omega=-1\), so

\[
 \|M\|=1,\qquad \sigma_{\min}(M)=K^{-1},\qquad
 \kappa(M)=K.                                               \tag{3}
\]

For the public basis vector \(e=|0,0^n\rangle\), write

\[
 z_0=\gamma^{3T},\qquad
 S=\sum_{t=0}^{3T-1}\gamma^{2t}.
\]

The exact inverse history and its public norm are

\[
 x^*=M^{-1}e
 =\frac{1+\gamma}{1-z_0}
   \sum_{t=0}^{3T-1}\gamma^tU^te,                          \tag{4}
\]

\[
 R=\|x^*\|
 =\sqrt{K\frac{1+z_0}{1-z_0}}.                            \tag{5}
\]

On clock times \(I=\{T,\ldots,2T-1\}\), the data state in (4) is the final
Forrelation state \(V|0^n\rangle\). If

\[
 S_I=\sum_{t=T}^{2T-1}\gamma^{2t},\qquad
 p=\frac{S_I}{S},\qquad z=\gamma^{2T},
\]

then exactly

\[
 p=\frac{z}{1+z+z^2}.                                     \tag{6}
\]

Choose the nearest allowed \(T\) to
\(\log(1/\delta)/\alpha_K\). Allowed values have constant gaps and
\(\gamma\geq1/2\), so

\[
 z=\Theta(\delta^2),\qquad p=\Theta(\delta^2),\qquad
 \ell=\frac{\log(1/\delta)}{3\alpha_K}+O(1).               \tag{7}
\]

## One-cone SOCP and its Newton system

Consider

\[
 \begin{aligned}
 \max_{x,u}\quad &2e^Tu\\
 \text{s.t.}\quad &u=Mx,\\
 &(1,u)\in Q_{N+1}.
 \end{aligned}                                             \tag{8}
\]

Its unique primal optimizer is \(u^*=e,\ x^*=M^{-1}e\). After eliminating
\(u\), its Lorentz barrier is

\[
 \phi(x)=-\log(1-\|Mx\|^2).
\]

At the public analytic center \(x=0\), the reduced Newton matrix and first
direction for objective multiplier \(\eta>0\) are

\[
 H_0=2M^TM,\qquad
 d_\eta=\eta(M^TM)^{-1}M^Te=\eta M^{-1}e.                 \tag{9}
\]

Thus the normalized first Newton direction is exactly the hard inverse
state. The entire nonzero central path has the same direction:

\[
 x(\eta)=a(\eta)M^{-1}e,\qquad
 \frac{a}{1-a^2}=\eta.                                    \tag{10}
\]

Moreover,

\[
 H_0=\frac{2}{(1+\gamma)^2}
 \bigl((1+\gamma^2)I-\gamma(U+U^T)\bigr),                 \tag{11}
\]

so \(H_0\) is positive definite, has condition \(K^2\), sparsity at most
\(2q+1\), and itself has a constant-overhead full-SQ interface. This is
also a direct sparse SPD first-Newton-system family, not an access gap
between conic data and its normal equations.

## A literal sparse optimizer coordinate

For each \(t\in I\), let \(i_t=(t,0^n)\) be the corresponding coordinate
of \(x\), and define

\[
 a_t=\frac{\gamma^t}{R\sqrt{S_I}}.                         \tag{12}
\]

Append free accumulator variables using the three-sparse chain

\[
 y_T=a_Tx_{i_T},\qquad
 y_{t+1}=y_t+a_{t+1}x_{i_{t+1}},\qquad
 w=y_{2T-1}.                                               \tag{13}
\]

This adds \(O(T)\) public rows and variables. Each row has at most three
nonzeros, each selected \(x\)-column gains one incidence, and every new
row and column norm is public. The augmented sparsity remains
\(\Theta(q)\), and its full SQ interface is a public mixture of the
original and accumulator rows.  These accumulator variables are free linear
directions with no added cone barrier; equivalently, they may be eliminated
after defining the designated coordinate.

Let

\[
 \Phi=\langle0^n|V|0^n\rangle
\]

be the 2-Forrelation amplitude. Equations (4), (5), and (12) give

\[
 \boxed{w^*=\sqrt p\,\Phi,\qquad \|a\|_2=R^{-1}.}           \tag{14}
\]

Under the standard promise

\[
 \Phi\geq3/5
 \quad\text{or}\quad
 |\Phi|\leq1/100,
\]

(14) has an additive promise gap
\(\Theta(\sqrt p)=\Theta(\delta)\). Therefore an
additive-\(c\delta\) estimate of the literal optimizer coordinate \(w^*\)
decides 2-Forrelation.

## Objective-gap transfer

Let \((\widehat x,\widehat u,\widehat w)\) be exactly feasible for the cone,
\(u=Mx\), and the accumulator chain, with maximization gap at most \(\tau\):

\[
 2-2e^T\widehat u\leq\tau.
\]

Since \(\|\widehat u\|\leq1\),

\[
 \|\widehat u-e\|^2\leq\tau.
\]

Using (3), (5), and (14),

\[
 |\widehat w-w^*|
 \leq\frac{\|\widehat x-x^*\|}{R}
 \leq K_{\mathrm{eff}}\sqrt\tau,                          \tag{15}
\]

where

\[
 K_{\mathrm{eff}}
 =\frac{\|M^{-1}\|}{R}
 =\sqrt{K\frac{1-z_0}{1+z_0}}
 \leq\sqrt K.                                             \tag{16}
\]

Because \(p=\Theta(\delta^2)\), a sufficiently small universal \(c_0\) in

\[
 \boxed{\tau\leq c_0\delta^2/K}                            \tag{17}
\]

keeps \(\widehat w\) on the correct side of the Forrelation promise gap.
Thus (1) also lower-bounds returning the designated coordinate of any
exactly feasible \(\tau\)-optimal SOCP point. Ordinary bounded success
probability is enough. Approximate equality or cone feasibility needs a
separate residual budget and is not included in (17).

## Query reduction and quantum side

The randomized query lower bound for 2-Forrelation is

\[
 \Omega(2^{n/2}/n)
 =\Omega(q^{\ell/2}/(r\ell)).                              \tag{18}
\]

Every sparse-entry, sparse-location, row/column sampling, or norm query to
the augmented SOCP data is simulated with a constant number of queries to
the hidden sign tables. Hadamard transition rows are public uniform
distributions; diagonal sign transitions have public locations and
magnitudes; all accumulator information is public. This proves (1).

For this structured family, the coherent sparse-\(M\) oracle and the source
sign oracles are constant-query equivalent: a designated clock-transition
entry reveals each hidden sign. A quantum algorithm estimates \(\Phi\) to
constant additive accuracy with \(O(1)\) hidden queries, then multiplies by
the public \(\sqrt p\) to estimate \(w^*\) within \(O(\delta)\). Its public
circuit has \(O(n)=\operatorname{polylog}N\) gates. Hence

\[
 \boxed{
 Q_{\rm quantum}=O(1)\ \text{hidden queries and }\operatorname{polylog}N
 \ \text{gates},\qquad
 Q_{\rm classical}=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right).} \tag{19}
\]

The quantum bound uses the source-equivalent structured Forrelation
realization. A generic QLSA followed by amplitude estimation of the
\(\Theta(\delta)\) overlap would instead require order \(1/\delta\) state
preparations. No generic constant-query claim is made for arbitrary
matrices with the same condition and sparsity.

## Fixed-\(k\) near-linear ambient-dimension upgrade

The same scalar construction can use \(k\)-Forrelation for any fixed
admissible constant \(k\). Its forward circuit has

\[
 T=(k+1)\ell+O(k),
\]

so choosing the plateau mass \(p=\Theta(\delta^2)\) gives

\[
 \ell=\frac{\log(1/\delta)}{(k+1)\alpha_K}+O_k(1).          \tag{20}
\]

For the standard promises

\[
 |\Phi_{n,k}|\leq\alpha_k=2^{-5k-1}
 \quad\text{or}\quad
 |\Phi_{n,k}|\geq\beta_k=2^{-5k},
\]

the same accumulator obeys \(w^*=\sqrt p\,\Phi_{n,k}\). Thus its additive
promise gap is \(2^{-O(k)}\delta\), and an objective gap

\[
 \tau\leq 2^{-O(k)}\delta^2/K                              \tag{21}
\]

suffices for the optimizer-coordinate decision. The randomized source
lower bound yields

\[
 \boxed{
 Q=\Omega_k\!\left[
 \left(\frac{q^\ell}{r\ell}\right)^{1-1/k}
 \right]
 =\exp\!\left(\Omega_k(K\log s\log(1/\delta))\right).}      \tag{22}
\]

Since \(N=\Theta_k(Tq^\ell)\), this is
\(\widetilde\Omega_k(N^{1-1/k})\), arbitrarily close to linear in ambient
dimension for a sufficiently large fixed \(k\). Quantumly, the source
circuit and constant-gap estimation use \(2^{O(k)}\) hidden queries and
\(\operatorname{polylog}N\) public gates, still constant-query for fixed
\(k\). This extension combines the joint conditioning--sparsity--precision
exponent with a near-linear ambient-dimension lower bound.

## Value-only strengthening by a small objective tilt

The accumulator also turns the construction into an optimal-value lower
bound. Let

\[
 h=\sqrt p,\qquad g=M^{-T}a.
\]

For every feasible point, elimination of the equality constraints gives

\[
 w=a^Tx=a^TM^{-1}u=g^Tu.
\]

Replace the objective of (8) by

\[
 \max\ e^Tu+\lambda w,\qquad
 \lambda=\theta h/K,                                      \tag{23}
\]

where \(\theta>0\) is a sufficiently small public constant. Maximizing a
linear functional over the unit ball gives the exact optimal value

\[
 \boxed{
 \operatorname{OPT}_\lambda
 =\|e+\lambda g\|,\qquad
 \operatorname{OPT}_\lambda^2
 =1+2\lambda h\Phi+\lambda^2\|g\|^2.}                     \tag{24}
\]

Here

\[
 e^Tg=a^TM^{-1}e=h\Phi,\qquad
 \|g\|\leq\|M^{-1}\|\,\|a\|
 =K_{\mathrm{eff}}\leq\sqrt K.                            \tag{25}
\]

Suppose the source promise is

\[
 |\Phi|\leq\alpha
 \quad\text{or}\quad
 |\Phi|\geq\beta,
\]

with \(0\leq\alpha<\beta\). In the low case,

\[
 |\operatorname{OPT}_\lambda^2-1|
 \leq(2\theta\alpha+\theta^2)\frac{h^2}{K},                \tag{26}
\]

whereas in the high case,

\[
 |\operatorname{OPT}_\lambda^2-1|
 \geq(2\theta\beta-\theta^2)\frac{h^2}{K}.                 \tag{27}
\]

Taking, for example, \(\theta\leq(\beta-\alpha)/4\) leaves a
\(\Theta(\theta(\beta-\alpha)h^2/K)\) gap between the squared-value
intervals. Since \(\operatorname{OPT}_\lambda=1+O(\theta)\), additive
approximation of the value and its square differ by only a constant factor.
Consequently, value accuracy

\[
 \boxed{
 \epsilon_{\mathrm{val}}
 =c\,\theta(\beta-\alpha)\frac{p}{K}}                      \tag{28}
\]

for a sufficiently small universal \(c\) decides the source promise.
For 2-Forrelation this is \(\Theta(\delta^2/K)\). For the fixed-\(k\)
promise \(\alpha_k=2^{-5k-1},\ \beta_k=2^{-5k}\), choose
\(\theta=2^{-O(k)}\); then (28) is
\(2^{-O(k)}\delta^2/K\).

All coefficients introduced by (23) are public, and the objective has only
the two displayed nonzero blocks \(e\) and \(w\). Hence the same sparse and
full-SQ input simulation applies. A bounded-error classical value
approximation would solve Forrelation directly, so its query lower bound is
(1), or (22) for fixed \(k\). This is a conventional value-output contract:
it needs neither exact-feasible iterate output nor a sampling guarantee.

The structured quantum algorithm estimates \(\Phi\) to error
\(o(\beta-\alpha)\). From (24)--(25), omitting the nonnegative quadratic
term changes the squared value by at most

\[
 \lambda^2\|g\|^2\leq\theta^2p/K.
\]

Choosing \(\theta\ll\beta-\alpha\), it can therefore output
\(\sqrt{1+2\lambda h\widehat\Phi}\) within (28), using \(O(1)\) hidden
queries for 2-Forrelation and \(2^{O(k)}\) for fixed \(k\). Thus the
near-linear fixed-\(k\) separation also holds for the optimal value, not
only a designated optimizer coordinate.

### Public norm normalization gives a larger value gap

The small tilt above is a robust fallback that uses only the bound in
(25). For this clock family, however, \(G=\|g\|\) is itself an exactly
public scalar. This permits a stronger normalization.

To fix the gauge convention, let \(G_t\) be the transition applied from
clock \(t-1\) to clock \(t\), let

\[
 W_0=I,\qquad W_t=G_tG_{t-1}\cdots G_1,
 \qquad W=\sum_{t=0}^{3T-1}|t\rangle\!\langle t|\otimes W_t.
\]

The reverse part of the clock makes the cyclic product the identity. If
\(S|t-1\rangle=|t\rangle\) is the public cyclic shift, then

\[
 W^TUW=S\otimes I,
 \qquad
 W^TMW=m\otimes I,
 \qquad
 m=\frac{I-\gamma S}{1+\gamma}.                           \tag{28a}
\]

For \(t\in I=\{T,\ldots,2T-1\}\), the hold construction has \(W_t=V\).
Define the public clock vector

\[
 \bar a=\sum_{t\in I}\frac{\gamma^t}{R\sqrt{S_I}}|t\rangle.
\]

The original-basis vector \(a\) therefore factorizes in the history gauge:

\[
 W^Ta=\bar a\otimes V^T|0^n\rangle,
 \qquad
 W^Tg=(m^{-T}\bar a)\otimes V^T|0^n\rangle.              \tag{28b}
\]

It follows that

\[
 \boxed{
 G=\|g\|=\|m^{-T}\bar a\|
 =\frac{1+\gamma}{1-\gamma^{3T}}
   \left\|\sum_{j=0}^{3T-1}\gamma^j(S^T)^j\bar a\right\|.} \tag{28c}
\]

This is a finite clock-only expression and can be precomputed without a
hidden-function query. Its needed bounds are also exact. First,

\[
 \langle0|m^{-T}\bar a\rangle
 =\bar a^Tm^{-1}|0\rangle
 =\frac{(1+\gamma)\sqrt{S_I}}
        {(1-\gamma^{3T})R}
 =\sqrt{S_I/S}=h,
\]

where \(R=(1+\gamma)\sqrt S/(1-\gamma^{3T})\). Hence \(G\geq h\).
Second,

\[
 G\leq\|m^{-1}\|\,\|\bar a\|
 =K/R
 =\sqrt{K\frac{1-\gamma^{3T}}{1+\gamma^{3T}}}
 \leq\sqrt K.                                             \tag{28d}
\]

There is a matching lower bound. Put \(b=m^{-T}\bar a\). For
\(0\leq t<T\), the vector \(\bar a\) vanishes and
\((m^Tb)_t=(b_t-\gamma b_{t+1})/(1+\gamma)=0\). Since
\(b_0=h\), this gives \(b_t=h\gamma^{-t}\), and therefore

\[
 \begin{aligned}
 G^2&\geq\sum_{t=0}^{T-1}b_t^2
 =\frac{1-z}{1+z+z^2}\frac{\gamma^2}{1-\gamma^2}\\
 &=\frac{1-z}{1+z+z^2}\frac{(K-1)^2}{4K}
 =\Theta(K),                                               \tag{28d'}
 \end{aligned}
\]

for the chosen \(z=\Theta(\delta^2)\) and a sufficiently small fixed
\(\delta_0\). Hence \(G=\Theta(\sqrt K)\), and
\(\lambda_{\rm n}=\Theta(K^{-1/2})\).

There is no hidden coefficient blowup in either formulation. Since every
singular value of \(m^{-T}\) is at least one,
\(G\geq\|\bar a\|=1/R\). Thus \(\lambda_{\rm n}\leq R/2\) and the
eliminated objective coefficient obeys
\(\|\lambda_{\rm n}a\|=\lambda_{\rm n}/R\leq1/2\).

Now use the same objective as (23), but choose the public coefficient

\[
 \lambda_{\rm n}=\frac{1}{2G}.
\]

The exact squared optimal value is

\[
 \boxed{
 \operatorname{OPT}_{\rm n}^2
 =\|e+\lambda_{\rm n}g\|^2
 =\frac54+\frac{h}{G}\Phi.}                              \tag{28e}
\]

Because \(|\Phi|\leq1\) and \(h/G\leq1\),
\(\operatorname{OPT}_{\rm n}\) lies between \(1/2\) and \(3/2\). Under the signed promise
\(|\Phi|\leq\alpha\) or \(|\Phi|\geq\beta\), the distance of
\(\operatorname{OPT}_{\rm n}^2\) from the public baseline \(5/4\) is at
most \(\alpha h/G\) or at least \(\beta h/G\), respectively. Thus either
sign in the high case is handled by taking the absolute deviation from the
baseline. Additive value accuracy

\[
 \boxed{
 \epsilon_{\rm val}=c(\beta-\alpha)\frac{h}{G}
 =\Theta\!\left((\beta-\alpha)\frac{\delta}{\sqrt K}\right).} \tag{28f}
\]

decides the source promise. For 2-Forrelation it is enough to require
\(\Theta(\delta/\sqrt K)\) accuracy. For fixed \(k\)-Forrelation it is
enough to require \(2^{-O(k)}\delta/\sqrt K\) accuracy. This strictly
improves the sufficient accuracies in (28), while retaining them as a
fallback.

This scale is optimal, up to constants, for every readout supported on the
same hold plateau. Indeed, let \(\bar c\) be any clock vector supported on
\(I\), and put \(b=m^{-T}\bar c\). The same homogeneous recurrence gives
\(b_t=b_0\gamma^{-t}\) for \(0\leq t<T\), so

\[
 \frac{|b_0|}{\|b\|}
 \leq
 \left(\sum_{t=0}^{T-1}\gamma^{-2t}\right)^{-1/2}
 =\Theta\!\left(\frac{\delta}{\sqrt K}\right).             \tag{28f'}
\]

In the history gauge, a public original-basis readout on coordinates
\((t,0^n)\), \(t\in I\), has data factor \(V^T|0^n\rangle\). Its
Forrelation-dependent overlap after inverse transpose is therefore
\(b_0\Phi\), while the direction norm is \(\|b\|\). Equation (28f') says
that no constant-scale objective tilt built from an arbitrary
plateau-supported readout can have a larger asymptotic value signal. The
choice (12) attains this bound by (28d)--(28f).

Equivalently, parameterize the theorem by the requested value accuracy
\(\varepsilon\), with \(\varepsilon\sqrt K\) below a small constant. Taking
\(\delta=\Theta(\varepsilon\sqrt K)\) gives

\[
 \ell=\frac{\log(1/(\varepsilon\sqrt K))}{3\alpha_K}+O(1),
 \qquad
 Q=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right).          \tag{28g}
\]

Up to the displayed polynomial term, this is

\[
 Q=\exp\!\left(
 \Omega\!\left(K\log s\,
 \log\frac{1}{\varepsilon\sqrt K}\right)\right).         \tag{28h}
\]

If \(\kappa_H=K^2\) denotes the condition number of the reduced Newton
Hessian, the exponent is
\(\Omega(\sqrt{\kappa_H}\log s\,
\log(1/(\varepsilon\kappa_H^{1/4})))\). This is the direct
conditioning--sparsity--accuracy frontier for the optimal value and, by
(30), for the squared Newton decrement.

Full SQ access is unchanged: \(G\), \(h\), and \(\lambda_{\rm n}\) are
public, and the objective still has only the \(e\) and \(w\) blocks. The
structured quantum source algorithm outputs
\(\sqrt{5/4+(h/G)\widehat\Phi}\), so the same constant or \(2^{O(k)}\)
hidden-query upper bound meets (28f).

## The Newton decrement is the hard optimal value

The tilted value has a direct QIPM interpretation. Eliminate \(u,w\) from
the tilted problem and use the objective multiplier \(\eta>0\). At the
public analytic center \(x=0\), the barrier Hessian and objective gradient
are

\[
 H_0=2M^TM,\qquad
 \nabla F_\eta(0)=-\eta(M^Te+\lambda a).                  \tag{29}
\]

Since

\[
 M^Te+\lambda a=M^T(e+\lambda g),
\]

the squared Newton decrement is exactly

\[
 \boxed{
 \Lambda_\eta^2
 =\nabla F_\eta(0)^TH_0^{-1}\nabla F_\eta(0)
 =\frac{\eta^2}{2}\|e+\lambda g\|^2
 =\frac{\eta^2}{2}\operatorname{OPT}_\lambda^2.}           \tag{30}
\]

The supports of \(M^Te\) and \(a\) lie in public, disjoint clock regions.
Their norms are public, their conditional sampling rules are explicit, and
a value query uses at most one hidden sign query. Thus the Newton
right-hand side in (29), as well as the sparse SPD matrix \(H_0\) in (11),
has full SQ access with constant hidden-query overhead.

Consequently, the lower bounds (1) and (22) also apply to estimating the
Newton decrement at an exact public analytic center to additive squared
accuracy

\[
 \boxed{2^{-O(k)}\eta^2\delta/\sqrt K}.                  \tag{31}
\]

Here the normalized coefficient \(\lambda_{\rm n}\) is used. The original
small-tilt argument independently gives the weaker fallback accuracy
\(2^{-O(k)}\eta^2\delta^2/K\).

This is stronger than merely hiding a hard direction behind conic
preprocessing: even a classical routine handed the reduced Newton matrix
and right-hand side directly cannot evaluate this standard path-following
diagnostic within (31) using fewer queries. The structured quantum
Forrelation routine estimates it with the same \(2^{O(k)}\) hidden-query
bound as the optimal value.

## Scalar-inequality LP corollary

The hard Newton diagnostic does not require a Lorentz cone. Consider the
linear program with symmetric box constraints

\[
 \max_x\ c^Tx,\qquad
 -\mathbf 1\leq Mx\leq\mathbf 1,\qquad
 c=M^Te+\lambda_{\rm n}a.                                \tag{31a}
\]

It consists only of scalar inequalities. Its constraint matrix is the
stack of \(M\) and \(-M\), so its row and column sparsity is \(\Theta(q)\),
and its full SQ interface has the same constant hidden-query overhead as
\(M\). The objective vector in (31a) also has direct full SQ access: the
supports of \(M^Te\) and \(a\) are public and disjoint, their norms and
mixture weight are public, and an entry query uses at most one hidden sign
query.

The standard logarithmic barrier is

\[
 \phi_{\rm box}(x)
 =-\sum_i\log(1-(Mx)_i)-\sum_i\log(1+(Mx)_i).
\]

Its unique analytic center is the public point \(x=0\), and

\[
 \nabla^2\phi_{\rm box}(0)=2M^TM=H_0.                    \tag{31b}
\]

For objective multiplier \(\eta\), use
\(c=M^T(e+\lambda_{\rm n}g)\) to obtain the exact squared decrement

\[
 \boxed{
 \Lambda_{\eta,{\rm LP}}^2
 =\frac{\eta^2}{2}\|e+\lambda_{\rm n}g\|^2
 =\frac{\eta^2}{2}
   \left(\frac54+\frac{h}{G}\Phi\right).}                \tag{31c}
\]

Thus estimating the squared Newton decrement of a sparse LP at an exact,
explicit analytic center to additive accuracy
\(2^{-O(k)}\eta^2\delta/\sqrt K\) has the same classical SQ lower bounds
(1) and (22), even when the sparse SPD Hessian and Newton right-hand side
are handed to the algorithm directly. Its condition number is \(K^2\).
The structured quantum Forrelation algorithm estimates (31c) with
\(2^{O(k)}\) hidden queries.

For the unperturbed extended-form objective \(2e^Tu\), equivalently
\(c=2M^Te\) after eliminating \(u=Mx\), the first LP Newton direction is
exactly \(\eta M^{-1}e\), so the normalized hard-direction lower bound
survives as well. In fact, the entire unperturbed LP central path is hard.
In the coordinates \(u=Mx\), separability and strict convexity force

\[
 u(\eta)=\rho(\eta)e,qquad
 \frac{\rho}{1-\rho^2}=\eta,qquad
 x(\eta)=\rho(\eta)M^{-1}e.                              \tag{31d}
\]

Thus its normalized nonzero central-path iterate is exactly the inverse
history state. If the public accumulator is retained, its path coordinate
is \(w(\eta)=\rho(\eta)h\Phi\); for any fixed public \(\eta>0\), estimating
that literal coordinate to additive \(\Theta(\delta)\) has lower bound (1),
and estimating the fixed-\(k\) version to additive
\(2^{-O(k)}\delta\) has lower bound (22).

This central-path statement is stable under an ordinary barrier-subproblem
gap. In \(u\)-coordinates, define

\[
 F_\eta(u)=-\sum_i\log(1-u_i^2)-2\eta e^Tu.
\]

Its Hessian is diagonal and bounded below by \(2I\) throughout the box.
Hence

\[
 F_\eta(\widehat u)-F_\eta(u(\eta))\leq\tau
 \quad\Longrightarrow\quad
 \|\widehat u-u(\eta)\|\leq\sqrt\tau.
\]

For \(\widehat x=M^{-1}\widehat u\), the accumulator error is at most
\(K_{\rm eff}\sqrt\tau\leq\sqrt{K\tau}\). Therefore, at any fixed
\(\eta>0\), returning the designated coordinate of a barrier point with

\[
 \tau\leq2^{-O(k)}\delta^2/K                               \tag{31e}
\]

also has lower bounds (1) and (22). This is an end-to-end approximate
centering-output contract, not only an exact-path statement. As in (17),
the retained accumulator equality must be exact, or the coordinate must be
computed directly as \(a^T\widehat x\); an approximate equality residual
requires a separate budget.

The price, as for the bounded-cone norm tree, is a barrier parameter
\(\Theta(N)\). More precisely, the generic sum rule applied to the \(2N\)
inequality logs gives the valid bound \(2N\), while direct differentiation
shows that each paired interval barrier \(-\log(1-u_i^2)\) is a
one-self-concordant barrier, giving parameter \(N\) for the displayed box
barrier. The value of (31a) itself is not asserted to encode Forrelation;
the LP conclusions concern its central-path iterate, first Newton direction,
and Newton decrement, not a claim of polylogarithmically many LP-IPM
iterations.

## Bounded-cone-dimension corollary

The optimal-value theorem does not intrinsically require one large Lorentz
block. Let \(D\) be the smallest power of two at least the dimension of
\(u\), and pad \(u\) to \(D\) leaves with public zero coordinates. Introduce
a balanced binary norm tree. For
each internal node \(v\) with child values \(z_{v,0},z_{v,1}\), impose

\[
 (t_v,z_{v,0},z_{v,1})\in Q_3,
\]

where bottom-level child values are coordinates of \(u\), higher-level
child values are the corresponding \(t\)'s, and the root first coordinate
is fixed to one. The projection of these constraints onto \(u\) is exactly

\[
 \|u\|_2\leq1.
\]

Indeed, recursively feasible tree values imply
\(t_v^2\) dominates the squared norm of all leaves below \(v\), while
choosing every \(t_v\) equal to that subtree norm proves the converse.
If a strict standard product-cone form is desired, copy each shared
\(t_v\) into its two cone occurrences and add a public two-sparse consensus
equality.

This exact lift uses \(O(N)\) copies of \(Q_3\). Every tree row and variable
has constant incidence, so the augmented maximum row/column sparsity is
still \(\Theta(q)\); its SQ interface adds only a public component. The
feasible projection in \((x,u,w)\), and therefore the optimizer coordinate,
tilted optimal value, promise gaps, and lower bounds (1), (22), and (28),
including the stronger normalized gap (28f), are unchanged.

Thus the optimal-value separation also holds for an SOCP whose every cone
has dimension three. In fact, a balanced tree also preserves the first
Newton identity.

To see this, after identifying the consensus copies, write the product
barrier as

\[
 \Psi(t,u)
 =-\sum_{v\ {\rm internal}}
 \log\!\left(t_v^2-z_{v,0}^2-z_{v,1}^2\right),             \tag{32}
\]

with the root \(t\) fixed to one. On the slice \(u=0\), this barrier has a
unique analytic center \(t^\circ\): the domain is bounded, the barrier
diverges at its boundary, and the summands are strictly convex in the
relevant tree variables. Tree automorphisms make \(t^\circ\) constant on
each depth. More explicitly, number the root by depth zero and let
\(L=\log_2D\). If \(t_d^\circ\) is the common value at depth
\(d=0,\ldots,L-1\), then

\[
 (t_d^\circ)^2
 =\frac{D-2^d}{2^d(D-1)},\qquad t_0^\circ=1.             \tag{32a}
\]

Indeed, putting \(y_d=2^d t_d^2\) turns the slacks into the gaps
\(y_d-y_{d+1}\), with the bottom gap \(y_{L-1}\). Minimizing the resulting
weighted log barrier under the condition that these gaps sum to one makes
the depth-\(d\) gap equal to \(2^d/(D-1)\), which gives (32a). Thus the
center and every Hessian entry there have explicit public access.

Every leaf sign flip preserves (32), while the balanced-tree automorphism
group acts transitively on leaves. Therefore, at \((t^\circ,0)\),

\[
 \nabla_t\Psi=0,\qquad
 \nabla^2_{ut}\Psi=0,\qquad
 \nabla^2_{uu}\Psi=c_DI                              \tag{33}
\]

for a positive public scalar \(c_D\). The first two identities also follow
directly because every leaf occurs quadratically in its bottom cone; the
last follows from transitivity (and is explicitly
\(c_D=2/(t^\circ_{\rm bottom})^2=2(D-1)\)).

Substituting \(u=Mx\), the reduced Hessian block at the public analytic
center is exactly

\[
 H_{xx}=c_DM^TM,\qquad H_{xt}=0.                            \tag{34}
\]

For the unperturbed objective \(2e^Tu\), the first \(x\)-Newton direction
is consequently

\[
 d_x=\frac{2\eta}{c_D}M^{-1}e,                             \tag{35}
\]

so its normalized state is the same hard inverse state as in (9). For the
tilted objective, the squared decrement becomes

\[
 \Lambda_\eta^2
 =\frac{\eta^2}{c_D}\|e+\lambda g\|^2
 =\frac{\eta^2}{c_D}\operatorname{OPT}_\lambda^2.          \tag{36}
\]

The tree-variable Hessian block is a public constant-degree
tree-of-triangles sparse matrix, (34) is the same sparse SPD clock block up
to a public scalar, and the cross block vanishes. Hence the direct full-SQ
Newton-matrix, right-hand-side, hard
direction, and hard-decrement reductions survive with only
three-dimensional cones. The decrement scale in (36) must be retained:
for the fixed-\(k\) promise, the corresponding additive squared accuracy is

\[
 \boxed{2^{-O(k)}\eta^2\delta/(c_D\sqrt K)}.             \tag{37}
\]

The small-tilt fallback has the weaker scale
\(2^{-O(k)}\eta^2\delta^2/(Kc_D)\).
Thus, at the same value of \(\eta\), the normalized-tilt scale is (31)
divided by \(c_D\). Equivalently, choosing the
public path multiplier larger by a factor \(\sqrt{c_D/2}\) recovers the
numerical scale in (31). The optimal-value and normalized-direction
statements do not incur this factor.

The remaining cost is structural: there are \(D-1\) Lorentz blocks, so the
standard product barrier has parameter \(2(D-1)=\Theta(N)\), rather than
the parameter-two barrier of the single Lorentz cone. Thus this lift does
not by itself give a
polylogarithmic-iteration QIPM, even though its first Newton solve and
decrement retain the separation. No condition-number bound for the full
lifted Hessian, including its public tree block, is asserted here.

This linear ambient-barrier cost is asymptotically unavoidable among all
exact bounded-cone-dimension SOC lifts, not merely an artifact of the
binary tree.  The
[SOC-granularity theorem](2026-09-04-soc-granularity-barrier-tradeoff.md)
shows that any exact lift of an \(N\)-dimensional ball by Lorentz blocks of
dimension at most \(d\), even with arbitrary free variables and affine
projections, needs \(\Omega(N/d)\) blocks.  Since a product of \(k\)
Lorentz cones has optimal ambient normal-barrier parameter \(2k\), every
constant-\(d\) formulation pays \(\Theta(N)\) at this level.  This does not
rule out eliminating the lift and using a dense small-parameter barrier on
the projected ball.

## Scope and novelty boundary

The unperturbed SOCP (8) has public optimal value two, but the normalized
tilt (28e) supplies the strongest value-only strengthening; the small tilt
(23) remains an independent fallback. Neither result asks
for explicit output of all \(N\) variables. The main Newton theorem uses
one high-dimensional Lorentz block; the norm-tree corollary preserves its
first-Newton and value separations with bounded-size cones but increases
the natural barrier parameter to \(\Theta(N)\). Exact feasibility is part of the
optimizer-coordinate contract in (17), but not the optimal-value contracts
in (28) and (28f).

The fixed-condition Grønlund--Larsen scalar-observable transfer in the
companion note already shows that a literal SOCP optimizer coordinate can
be classically hard. The new content here is the simultaneous explicit
\((K,s,\delta)\) frontier, removal of the rare-event prefactor and
vanishing-failure caveat from the precision-sensitive sampler theorem, and
the \(\tau=\Theta(\delta^2/K)\) end-to-end objective-gap translation. The
public clock-norm tilt further upgrades the same family to a matched-access
optimal-value separation at accuracy \(\Theta(\delta/\sqrt K)\). A targeted
primary-source search covered
[Grønlund--Larsen's inverse-sampling separation](https://arxiv.org/abs/2411.02087),
[Bansal--Sinha's \(k\)-Forrelation lower bound](https://arxiv.org/abs/2008.07003),
[Montanaro--Shao's sparse matrix-function entry lower bounds](https://arxiv.org/abs/2311.06999),
the
[Kerenidis--Prakash--Szilágyi SOCP QIPM](https://arxiv.org/abs/1908.06720),
[Apers--Gribling's LP value-query lower bound](https://arxiv.org/abs/2311.03215),
and the newer
[Mori--Kikuchi--Benedetti--Rosenkranz sparse-QLS lower bound](https://arxiv.org/abs/2601.16697).
It found the ingredients but no prior theorem combining a literal sparse
SOCP optimizer coordinate with the joint conditioning--sparsity--precision
lower exponent, the public clock-norm objective tilt, or the exact
Newton-decrement identity (30). The closest value-output result is the LP lower bound of
Apers--Gribling; because LP is already a special case of SOCP, and a
nonnegative ray is a face of \(Q_3\), bounded cone dimension by itself cannot
support a novelty claim. Likewise, the balanced norm tree is an elementary
repeated use of the Lorentz norm inequality, not a claimed-new representation.
Mori et al. lower-bound quantum state preparation for sparse linear systems,
not classical full-SQ estimation of a Newton decrement or conic optimal value.
The box LP and its elementary ray-shaped central path are not claimed as new
geometric constructions; the apparently new LP content is the
access-preserving Forrelation transfer to a literal central-path coordinate
and squared Newton decrement with the joint \((K,s,\delta)\) accounting.
The raw use of a Feynman clock to lower-bound a matrix-function scalar is also
not claimed as new. This screen supports apparent novelty only of the
access-preserving conic wrapper, joint frontier, objective tilt, and decrement
identity; it cannot establish priority.

Here \(K\) is the condition number of \(M\), and the reduced first-Newton
Hessian has condition \(K^2\).  No claim is made about the condition number
of an unreduced augmented KKT matrix containing the free accumulator
equalities.  The objective tilt changes the Newton right-hand side but not
that reduced Hessian.
