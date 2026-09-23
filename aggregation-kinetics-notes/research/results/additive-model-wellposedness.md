# Global mass-conserving solutions for the time-dependent additive model

Date: 2026-09-07. Status: standard existence argument, not a novelty claim. Scope: existence with a finite initial second size moment; uniqueness is not asserted. Independent review is recorded in [additive-existence-proof.md](../reviews/additive-existence-proof.md).

This note supplies a nonempty solution class for [the additive log-size results](general-additive-log-coupling.md) and their [pathwise extension](pathwise-additive-log-coupling.md). It also allows measurable time-dependent rates and daughter laws. Those results may retain their conditional statements for initial data with only finite count and mass; the construction proved here additionally assumes a finite second size moment.

## 1. Assumptions and conclusion

Let \(E=(0,\infty)\). Let \(\lambda,\sigma:[0,\infty)\to[0,\infty)\) be measurable and locally integrable. Let \(B_t\) be a measurable kernel of finite positive measures on \((0,1)\): for each Borel \(A\), \(t\mapsto B_t(A)\) is measurable. Assume, for almost every \(t\),
\[
B_t((0,1))=2,\qquad \int_{(0,1)}\theta B_t(d\theta)=1.
\tag{1}
\]
One may choose arbitrary valid versions at exceptional times. No density, time continuity, lower bound on daughter fractions, or logarithmic moment is assumed.

The equation is
\[
\begin{aligned}
\langle f,n_t\rangle={}&\langle f,n_0\rangle\\
&+\frac12\int_0^t\lambda(s)\iint(x+y)
       [f(x+y)-f(x)-f(y)]\,n_s(dx)n_s(dy)\,ds\\
&+\int_0^t\sigma(s)\int
       \left[\int f(\theta x)B_s(d\theta)-f(x)\right]n_s(dx)\,ds .
\end{aligned}
\tag{2}
\]
Here \(n_0\) is a finite nonnegative measure on \(E\) satisfying
\[
N_0=\int n_0(dx)<\infty,\quad
m=\int x\,n_0(dx)<\infty,\quad
M_{2,0}=\int x^2n_0(dx)<\infty.
\tag{3}
\]
For the nontrivial case assume \(N_0,m>0\); zero data have the zero solution.

**Existence theorem.** There is a global nonnegative measure solution of (2), for every bounded Borel \(f\), with \(t\mapsto n_t\) continuous in total variation. Write
\[
\Lambda(t)=\int_0^t\lambda(s)\,ds,\qquad
\Sigma(t)=\int_0^t\sigma(s)\,ds.
\]
For every finite \(t\),
\[
\int x\,n_t(dx)=m,\qquad
N(t)=N_0\exp\{\Sigma(t)-m\Lambda(t)\},
\tag{4}
\]
and
\[
M_2(t)\le M_{2,0}\exp\{2m\Lambda(t)\}.
\tag{5}
\]
There is no atom at zero because the measures live on \(E\), and the proof establishes uniform tightness away from zero on every finite time interval. All integrals in (2) are finite on finite time intervals.

Equation (1) specifies the expected daughter measure. If one also wants an eventwise binary split into complementary fractions, impose the corresponding symmetry/realizability condition on \(B_t\). The analytical statement only uses (1), exactly as the log-size arguments do.

## 2. Bounded-kernel approximation

For integers \(r\ge1\), replace \(x+y\) by
\[
k_r(x,y)=\min(x+y,r),
\qquad K_t^r(x,y)=\lambda(t)k_r(x,y).
\tag{6}
\]
Keep fragmentation and the initial measure unchanged. This retains the additive offspring size \(x+y\); it only bounds the collision rate.

Here are construction details needed when the daughter kernel is merely measurable in time. Use the weighted measure norm
\[
\|\mu\|_{w}=\int(1+x^2)\,|\mu|(dx).
\]
On bounded balls the approximate coagulation vector field is locally Lipschitz in this norm, with an integrable time factor proportional to \(r\lambda(t)\). This follows from
\[
1+(x+y)^2\le2(1+x^2)+2(1+y^2)
\]
and the bilinear difference identity. The fragmentation operator is bounded with norm at most \(3\sigma(t)\), since
\[
\int(1+\theta^2x^2)B_t(d\theta)\le2+x^2\le2(1+x^2).
\]

All time integrals here are **weak kernel integrals**, defined on Borel sets and then extended by integration. A signed kernel \(G_t\) with integrable weighted variation defines a signed measure \(\int_a^bG_t\,dt\) and satisfies
\[
\left\|\int_a^bG_t\,dt\right\|_w
\le\int_a^b\|G_t\|_w\,dt.
\tag{7}
\]
Countable additivity follows from dominated convergence applied to the positive and negative variations. Setwise measurability is preserved by the gain, loss, and daughter kernels. Thus Picard iteration on continuous weighted-variation paths gives a local solution by the usual contraction estimate. Its integral is a continuous weighted-variation path by (7).

For completeness, positivity can be retained during the contraction. On a nonnegative ball \(\|\mu\|_w\le H\), the loss rate
\[
\ell_\mu(t,x)=\lambda(t)\int k_r(x,y)\mu_t(dy)+\sigma(t)
\]
is at most \(c(t)=r\lambda(t)H+\sigma(t)\). Add \(c(t)\mu_t\) to the vector field and use the scalar integrating factor for \(-c(t)\). The resulting gain is nonnegative, including \((c-\ell_\mu)\mu\). On a sufficiently short interval this positive integral map sends the ball into itself and is a contraction. Repeating gives a nonnegative maximal solution \(n^r\).

This argument deliberately does not assert a Bochner differential equation in the space of measures. For example, a moving atomic daughter law can be measurable as a kernel without being strongly measurable in total variation. Weak kernel integrals provide the needed construction and norm estimates.

## 3. Bounds independent of the cutoff

The approximate equation permits the tests \(1,x,x^2\), since its kernel is bounded in size and the solution has finite \(w\)-norm. Exact cancellation gives
\[
\begin{aligned}
(N^r)'&=-\frac{\lambda(t)}2\iint k_r(x,y)n_t^r(dx)n_t^r(dy)
                +\sigma(t)N^r,\\
(M_1^r)'&=0.
\end{aligned}
\]
Consequently
\[
N^r(t)\le N_0e^{\Sigma(t)},\qquad M_1^r(t)=m.
\tag{8}
\]
Also \(\int\theta^2B_t(d\theta)\le1\). The identity
\((x+y)^2-x^2-y^2=2xy\) gives
\[
\begin{aligned}
(M_2^r)'&=\lambda(t)\iint k_r(x,y)xy\,n_t^r(dx)n_t^r(dy)
 +\sigma(t)\left(\int\theta^2B_t(d\theta)-1\right)M_2^r\\
&\le 2\lambda(t)mM_2^r.
\end{aligned}
\]
Thus
\[
M_2^r(t)\le M_{2,0}e^{2m\Lambda(t)}.
\tag{9}
\]
These bounds prevent finite-time growth of the weighted norm and extend each approximate solution globally. They require no initial third moment.

Fix \(T<\infty\), and abbreviate
\[
N_*=N_0e^{\Sigma(T)},\qquad M_{2,*}=M_{2,0}e^{2m\Lambda(T)}.
\]
The total variation of the coagulation event coefficient is at most three times its rate. Therefore, for \(0\le s\le t\le T\),
\[
\|n_t^r-n_s^r\|_{\rm TV}
\le3N_*\int_s^t[m\lambda(u)+\sigma(u)]\,du.
\tag{10}
\]
This is a uniform modulus of continuity, because the time factors are integrable.

## 4. No loss of particle count at zero

The second moment controls large particles but does not by itself exclude a number measure concentrating near zero. The following comparison closes that gap.

Let \(P^F_{s,t}\) be the positive linear propagator for pure fragmentation with the same \(\sigma,B\). Its adjoint on bounded Borel tests is
\[
(P^{F,*}_{s,t}f)(x)
=e^{\Sigma(t)-\Sigma(s)}
  \mathbb E\left[f\left(x\prod_{s<\tau_j\le t}\Theta_j\right)\right].
\tag{11}
\]
The times form an inhomogeneous Poisson process of intensity \(2\sigma(u)\,du\); at time \(u\), the fraction has law \(B_u/2\). The empty product is one. This formula follows from the convergent weak Dyson expansion of the bounded fragmentation operator, or directly by conditioning on the finitely many jump times.

Variation of constants for the approximate equation yields
\[
n_t^r=P^F_{0,t}n_0+\int_0^tP^F_{s,t}Q_s^r(n_s^r)\,ds.
\tag{12}
\]
This is a weak-measure identity. It follows by substitution of the same convergent expansion and Fubini; it does not require differentiability of a time-dependent backward test.

If \(f\) is nonnegative and nonincreasing, then so is \(P^{F,*}_{s,t}f\). For any such \(g\),
\[
g(x+y)-g(x)-g(y)\le0.
\]
Pairing (12) with \(f\) gives
\[
\langle f,n_t^r\rangle\le\langle P^{F,*}_{0,t}f,n_0\rangle.
\tag{13}
\]
Use one marked Poisson process over \([0,T]\), and let
\(D_t=\prod_{\tau_j\le t}\Theta_j\). It has finitely many marks almost surely, all strictly positive, so
\[
D_t\ge D_T>0 \quad(0\le t\le T)\quad\text{almost surely}.
\]
Taking \(f(x)=\mathbf1_{\{0<x<\varepsilon\}}\) in (13) proves
\[
\sup_{r,\ 0\le t\le T}n_t^r((0,\varepsilon))
\le e^{\Sigma(T)}\int\mathbb P(xD_T<\varepsilon)n_0(dx)
\longrightarrow0
\quad(\varepsilon\downarrow0).
\tag{14}
\]
The last step is dominated convergence and uses only finite initial count. Arbitrarily small fractions and infinite negative logarithmic moments are allowed. The finite clock, not a uniform positive fraction bound, excludes finite-time dust here.

## 5. Compactness and passage to the equation

At infinity,
\[
n_t^r((A,\infty))\le m/A,\qquad
\int_{(A,\infty)}x\,n_t^r(dx)\le M_{2,*}/A.
\tag{15}
\]
Together with (14) and the count bound, these give uniform tightness of the finite measures on \(E\). Combine this with (10) and Arzelà–Ascoli in a metric for narrow convergence, for example a bounded-Lipschitz metric after the coordinate change \(x\mapsto\log x\). A subsequence converges narrowly, uniformly on \([0,T]\), to a continuous nonnegative measure curve \(n_t\).

The first-moment tails in (15), and the elementary bound
\(\int_{(0,\varepsilon)}x\,n_t^r(dx)\le\varepsilon N_*\), show that
\[
\int x\,n_t(dx)=m.
\]
Lower semicontinuity gives (5). A diagonal choice over integer \(T\) supplies a curve on the entire half-line.

To pass the equation, first fix a bounded continuous \(f:E\to\mathbb R\). For each time \(s\), the fragmentation test
\[
x\longmapsto\int f(\theta x)B_s(d\theta)-f(x)
\]
is bounded and continuous in \(x\), by dominated convergence in \(\theta\). Narrow convergence therefore passes that term at each fixed time, despite mere measurability in \(s\). Its absolute value is bounded by \(3\|f\|_\infty N_*\), which is integrable after multiplication by \(\sigma(s)\).

For coagulation, put \(\Delta f(x,y)=f(x+y)-f(x)-f(y)\). The continuous integrand \((x+y)\Delta f\) has at most linear growth. Products of the finite measures converge narrowly. Uniform control of the relevant large-size tail follows from
\[
\begin{aligned}
\iint(x+y)\mathbf1_{\{x+y>A\}}\,n_t^r(dx)n_t^r(dy)
&\le A^{-1}\iint(x+y)^2n_t^r(dx)n_t^r(dy)\\
&\le\frac{2N_*M_{2,*}+2m^2}{A}.
\end{aligned}
\tag{16}
\]
This controls both unbounded integrands and removal of the cutoff \(k_r\). Small-size tightness ensures there is no escape from the open state space. The full absolute coagulation contribution is bounded by \(3\|f\|_\infty mN_*\lambda(s)\). Dominated convergence in time proves (2) for bounded continuous tests.

The resulting curve is a measurable kernel in \(t\). Its coagulation and fragmentation terms are signed kernels with total variation bounded by the integrable right side of (10). Define their time integrals as signed measures. Equality against all bounded continuous tests identifies those signed measures, so (2) holds also for every bounded Borel test. Taking variation yields the same modulus (10) for the limiting curve, hence total-variation continuity.

Finally take \(f=1\) in (2). The conserved mass gives
\[
N'(t)=\{\sigma(t)-m\lambda(t)\}N(t)
\]
almost everywhere, whose integrating-factor solution is (4). This proves the theorem.

## 6. What this closes, and what it does not

For constant \(\lambda>0,\sigma\ge0\) and fixed \(B\), every initial measure with finite count, positive finite mass, and finite second size moment has at least one background solution needed by the existing log-size and auxiliary-process theorems. No initial or daughter logarithmic moment is added. The same existence statement is available for the measurable time-dependent extension.

The higher moment is a sufficient condition used to pass mass through the approximation. This note does not claim that it is necessary, nor that existence for finite count and mass alone fails. Removing it would require an additional tail estimate, such as a suitable superlinear uniformly integrable moment. Uniqueness of the nonlinear population equation is not proved here. Conditional conclusions valid for every mass-conserving weak solution remain distinct from uniqueness of that solution.

The daughter law here depends on time and scales with the parent size, but its fraction distribution is independent of the parent. This does not prove existence for an arbitrary merely measurable parent-dependent fraction kernel \(B_{t,x}\). Such a kernel need not map continuous tests to continuous functions of \(x\), so the narrow-limit step above would require a different argument. Results stated conditionally for that broader controlled model retain their explicit background-solution assumption.

## 7. Prior work and attribution

Truncation, moment bounds, tightness, and weak convergence are standard coagulation-fragmentation existence tools. The purpose here is to check their application to the exact coefficients and measure-valued daughter assumptions used in this repository.

For an openly accessible stochastic construction in the pure-coagulation setting, see M. Deaconu, N. Fournier, and E. Tanré, *A pure jump Markov process associated with Smoluchowski's coagulation equation*, Annals of Probability **30** (2002), 1763–1796, [open author PDF](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). Section 3, Theorem 3.1, Corollary 3.3, and the subsequent approximation proof were inspected. That paper does not include the present fragmentation term, and Corollary 3.3 imposes a finite third moment on the initial number measure. It therefore should not be cited as directly establishing the precise theorem above.

No assertion of a new existence theorem is intended. This self-contained specialization avoids relying on a prior theorem whose time dependence, atomic daughter laws, or moment assumptions have not been checked.
