# Finite-count equilibria remain impossible beyond additive coagulation

Date: 2026-09-07. Status: candidate extension; core proof independently verified in [count-neutral-power-proof.md](../reviews/count-neutral-power-proof.md). A bounded literature comparison is below; no claim of settled publication novelty.

For the count-neutral family \(K(x,y)=x d(y)+y d(x)\), \(S(x)=m d(x)\), the additive case corresponds to constant \(d\). We obtain a nonstationarity extension for \(d(x)=x^\alpha\), \(0<\alpha\le1\). It requires only finite count and mass and allows parent-dependent binary daughter laws. However, the additive model's decreasing positive fractional moments do not extend unchanged: explicit atomic data reverse that monotonicity. Neither statement establishes global mass conservation for these more rapidly growing kernels.

## 1. Setting and result

Let \(0<\alpha\le1\), and consider
\[
K(x,y)=xy^\alpha+yx^\alpha,\qquad S(x)=m x^\alpha,\qquad x,y>0.
\tag{1}
\]
The expected daughter-fraction measure may depend measurably on the parent:
\[
B_x((0,1))=2,\qquad \int\theta B_x(d\theta)=1.
\tag{2}
\]
Actual binary mass-conserving splits satisfy (2); the proof only needs these expected-measure properties.

A stationary measure means a nonnegative measure \(n\) for which the usual coagulation-fragmentation weak vector field vanishes on every bounded Borel test. Assume
\[
0<N=\int n(dx)<\infty,\qquad 0<m=\int x\,n(dx)<\infty.
\tag{3}
\]
All event rates are then integrable, since \(D=M_\alpha=\int x^\alpha n(dx)<\infty\).

**Theorem 1.** No stationary measure satisfying (3) exists for (1)–(2). No negative moment, logarithmic moment, or moment above order one is required.

The case \(\alpha=0\) was established separately in [the additive nonstationarity result](invisible-kinetics-extension.md). Together the results exclude finite-count, finite-positive-mass equilibria throughout \(0\le\alpha\le1\).

**Corollary.** The same exclusion holds if the selection rate is \(S(x)=\sigma x^\alpha\), with any fixed \(\sigma\ge0\). Indeed, stationarity tested against one gives \(0=(\sigma-m)D\). Since \(D>0\), any prospective stationary state must have \(m=\sigma\), reducing it to Theorem 1. This excludes finite equilibria; it says nothing by itself about time-dependent existence or gelation.

## 2. A stationary jump balance permits the singular test

The number generator in this count-neutral class can be written
\[
(\mathcal L f)(x)=
x\int y^\alpha[f(x+y)-f(x)]\,n(dy)
+m x^\alpha\int[f(\theta x)-f(x)]B_x(d\theta).
\tag{4}
\]
Indeed, symmetry of the coagulation term and \(M_1=m\) show that \(\int\mathcal Lf\,dn\) is exactly the full population vector field on \(f\).

Its total jump rate is
\[
q(x)=xD+2m x^\alpha,\qquad \int q(x)n(dx)=3mD.
\tag{5}
\]
Define the probability \(\nu(dx)=q(x)n(dx)/(3mD)\). Let \(P(x,dz)\) be the jump transition kernel obtained from (4) by dividing its nonnegative gain kernel by \(q(x)\). Stationarity is the finite-measure identity
\[
\nu P=\nu.
\tag{6}
\]
This is an algebraic use of the embedded jump chain. No path construction, nonexplosion theorem, or time-dependent background solution is needed.

Now take \(g(x)=x^{-\alpha}\). Although \(\int g\,dn\) may be infinite, its integral under the jump-rate-weighted law is finite:
\[
3mD\int g\,d\nu
=D M_{1-\alpha}+2mN<\infty.
\tag{7}
\]
Equation (6), first tested on \(\min(g,L)\) and then passed to the limit by monotone convergence, gives \(\int Pg\,d\nu=\int g\,d\nu\). In particular the gain integral is finite. Consequently the signed cancellation
\[
\int \mathcal Lg(x)n(dx)=0
\tag{8}
\]
is justified. This is the reason the proof does not need a negative moment of the number distribution.

## 3. A strictly positive inverse-power drift

For each parent, Jensen's inequality under the probability \(B_x/2\) gives
\[
\int\theta^{-\alpha}B_x(d\theta)\ge2^{1+\alpha}.
\]
Thus the fragmentation part of (8) is at least
\[
2mN(2^\alpha-1).
\tag{9}
\]
This permits an infinite daughter inverse moment initially; under the prospective stationary identity its integrated gain must instead be finite by (7)–(8).

The coagulation contribution is \(-L\), where
\[
L=\iint xy^\alpha[x^{-\alpha}-(x+y)^{-\alpha}]\,n(dx)n(dy)\ge0.
\]
We claim
\[
L\le\alpha mN.
\tag{10}
\]
To verify this, symmetrize in \(x,y\), set \(s=x+y\) and \(u=x/s\), and write the symmetrized integrand as \(s C_\alpha(u)/2\), with
\[
\begin{aligned}
C_\alpha(u)={}&
u(1-u)^\alpha(u^{-\alpha}-1)\\
&+(1-u)u^\alpha((1-u)^{-\alpha}-1).
\end{aligned}
\]
Concavity of \(z^\alpha\), for \(0<\alpha\le1\), implies
\[
u^{-\alpha}-1\le\alpha(u^{-1}-1).
\]
Apply it to both terms to obtain
\[
C_\alpha(u)\le\alpha\{u^{1+\alpha}+(1-u)^{1+\alpha}\}\le\alpha.
\]
Integration gives (10), since \(\frac12\iint(x+y)n(dx)n(dy)=mN\).

Combining (9)–(10) proves
\[
\int\mathcal Lg\,dn
\ge c_\alpha mN,\qquad
c_\alpha=2(2^\alpha-1)-\alpha
\ge(2\log2-1)\alpha>0.
\tag{11}
\]
This contradicts (8) and proves Theorem 1. The coefficient is a convenient positive bound; no sharpness claim is made.

### The multiplicative endpoint

At \(\alpha=1\), \(K=2xy\), \(S=mx\), and \(\nu=xn/m\) is precisely the mass probability. Its embedded jumps coagulate with probability \(1/3\), adding an independent size with law \(\nu\), and fragment with probability \(2/3\), using the number-biased daughter fraction. Since \(1/x\) is \(\nu\)-integrable, fragmentation at least doubles its conditional value. The stationarity identity would give
\[
3\mathbb E_\nu(1/X)
=\mathbb E[1/(X+Y)]+2\mathbb E[1/(X\Theta)]
\ge4\mathbb E_\nu(1/X),
\]
an immediate contradiction.

## 4. Positive fractional-moment decay fails

Take equal splitting, choose \(R>1\), and set
\[
n_R=\delta_1+R^{-1}\delta_R.
\]
Its mass is two, its count is \(1+R^{-1}\), and every moment is finite. Let \(0<p<1\). Direct substitution into the generator gives
\[
\begin{aligned}
\left.\frac{dM_p}{dt}\right|_{n_R}
={}&A_p(1+R^{\alpha+p-1})\\
&+(1+R^{\alpha-1})[(1+R)^p-1-R^p],\\
A_p={}&2^p+2^{2-p}-4
       =\frac{(2^p-2)^2}{2^p}>0.
\end{aligned}
\tag{12}
\]
If \(0<\alpha\le1\) and \(p>1-\alpha\), the first line tends to positive infinity as \(R\to\infty\), whereas the second line stays bounded and negative. Therefore \(M_p\) has positive instantaneous drift for sufficiently large \(R\).

In particular, the half moment and the associated number/mass affinity need not decrease when \(\alpha>1/2\). For the explicit choice \(\alpha=1\), \(p=1/2\), \(R=64\),
\[
\left.\frac{dM_{1/2}}{dt}\right|_{n_{64}}
=27\sqrt2+2\sqrt{65}-54>0.
\tag{13}
\]
For instance \(\sqrt2>1.414\) and \(\sqrt{65}>8.062\) already give a positive lower bound. The exact generator calculation is reproduced in [the verification script](../verification/count_neutral_power.py).

This is an instantaneous generator counterexample to a proposed universal monotonicity inequality. It does not claim a global mass-conserving trajectory from these data. If a sufficiently regular local mass-conserving solution exists, (12) is its initial moment derivative. Since count and mass are conserved on such an interval, the same sign applies to the normalized fractional affinity.

The nonstationarity theorem therefore survives beyond the additive model even where its positive-moment Lyapunov function fails. The proof uses a jump-rate-weighted singular test instead.

## 5. Critical multiplicative literature and an essential boundary

Hung V. Tran and Truong-Son Van, *Coagulation-Fragmentation equations with multiplicative coagulation kernel and constant fragmentation kernel*, [open arXiv:1910.13424, version 3](https://arxiv.org/pdf/1910.13424). Inspected Section 1.3–1.4, Proposition 4.3, and Remark 4.4.

Their convention is \(K(x,y)=xy\) and a constant binary breakup kernel, which corresponds to selection \(S(x)=x/2\) and uniform daughter fractions. Substituting \(n_t=m c_{2mt}\) maps their critical mass-one equation to our \(\alpha=1\) uniform-split model at mass \(m\). Their Proposition 4.3 constructs stationary Bernstein transforms at this critical mass.

Those equilibria have **infinite particle count**, so they do not contradict Theorem 1. This follows directly from their formulas. If \(F\) is the stationary Bernstein transform and \(G=1-F'\), their equation is
\[
\frac{G(q)}{(1-G(q))^3}=Cq,\qquad C>0.
\]
As \(q\to\infty\), \(1-G(q)\sim(Cq)^{-1/3}\), hence
\[
F(q)\sim\frac32 C^{-1/3}q^{2/3}\longrightarrow\infty.
\]
Since \(F(q)=\int(1-e^{-qx})n(dx)\), monotone convergence gives \(N=\infty\). At \(q=0\), \(F'(0)=1\), so the mass is finite and positive.

Their construction uses the Bernstein-function results of Degond, Liu, and Pego, *Coagulation–Fragmentation Model for Animal Group-Size Statistics*, Journal of Nonlinear Science **27** (2017), 379–424, [open paper](https://sites.math.duke.edu/~jliu/pdf/Degond_Liu_Pego_2017.pdf). We do not claim that the critical stationary family is new.

The same Tran–Van paper distinguishes well-posedness of its transformed equation from existence of mass-conserving population measures. Its stated population existence theorem, Theorem 1.8, covers a subcritical mass range with a second-moment condition. It must not be read as a global existence theorem for every finite-count critical initial population. This note makes no such inference.

Laurençot, *Stationary solutions to coagulation-fragmentation equations* (2019), [open primary paper](https://www.numdam.org/item/10.1016/j.anihpc.2019.06.003.pdf), treats stationary existence for a different principal range: \(K=x^a y^b+x^b y^a\) with \(a+b<1\). Our nonstationarity result has exponents \(a=\alpha,b=1\) and lies outside that theorem. This comparison does not exhaust the critical homogeneous literature.

The bounded search located the exact critical multiplicative stationary construction above, but did not locate the arbitrary-parent-law, finite-count exclusion (11) over the full interval \(0<\alpha\le1\). The general jump-chain invariance argument and convexity tools are standard. A further adversarial literature audit is needed before treating the resulting specialized theorem as publishably novel.

## 6. Limits and retained open questions

No finite-count stationary counterexample was found for \(0\le\alpha\le1\); the theorem excludes one. Allowing infinite count already admits the known critical multiplicative equilibria. Allowing kernels or fragment rules outside the hypotheses remains a different question.

For \(\alpha>1\), \(M_\alpha\) need not be finite, and the inverse-power test may fail to be integrable under the jump-rate-weighted law. Also the concavity step in (10) reverses. The current proof does not cover this regime. For negative \(\alpha\), small-particle event rates introduce a different integrability and possible shattering problem. Neither range is resolved here.

For \(0<\alpha\le1\), the absence of a finite equilibrium does not prove full separation of number and mass laws, convergence to boundary measures, a Poisson log-size approximation, or an almost-sure final coagulation event. Those conclusions need additional estimates and a justified global solution class.

