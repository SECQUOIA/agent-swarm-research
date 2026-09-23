# Independent review of stationary nonexistence for power kernels

Date: 2026-09-07. Reviewer: /root/closure_direction/review_rigidity. Scope: the proof design supplied by the closure_direction agent for \(K(x,y)=xy^\alpha+yx^\alpha\), \(0<\alpha\le1\), with mass-conserving binary fragmentation. This is a mathematical proof review, not a novelty certification.

## Verdict

The proposed contradiction is correct. The auxiliary embedded-chain argument justifies the unbounded negative-power test without assuming a negative moment of the number measure. The symmetrized coagulation estimate has the stated factor and sign. The resulting strict positive gap excludes every nonzero stationary state having finite particle number and finite positive mass under the stated assumptions.

No higher moment, negative moment, daughter density, or parent-continuity assumption is needed. The daughter law may be a merely measurable parent-dependent expected measure. This stationary argument does not establish existence or uniqueness of the time-dependent equation.

## Assumptions and stationary measure identity

Let \(E=(0,\infty)\), \(0<\alpha\le1\), and let \(n\) be a nonnegative measure with
\[
0<N=\int n(dx)<\infty,\qquad
0<m=\int x\,n(dx)<\infty.
\]

For each parent \(x\), let \(B_x\) be a measurable kernel of nonnegative measures on \((0,1)\), satisfying
\[
B_x((0,1))=2,\qquad \int\theta\,B_x(d\theta)=1.
\]

These are conditions on the expected daughter measure; no stronger joint daughter-pair law is used. The coagulation kernel is \(K(x,y)=xy^\alpha+yx^\alpha\), and the selection rate in the critical case is \(S(x)=mx^\alpha\).

Put \(D=M_\alpha=\int x^\alpha n(dx)\). Since \(x^\alpha\le1+x\), it is finite; positivity of \(m\) implies \(D>0\). Consequently all gain and loss measures in the stationary bounded-test equation are finite. In particular, total coagulation event intensity is \(mD\), while total fragmentation event intensity is also \(mD\).

After symmetrizing the coagulation gain, stationarity becomes
\[
\begin{aligned}
\int [xD+2mx^\alpha]f(x)\,n(dx)
={}&\iint xy^\alpha f(x+y)\,n(dx)n(dy)\\
&+m\int x^\alpha\int f(\theta x)\,B_x(d\theta)n(dx).
\end{aligned}
\tag{1}
\]

Every coefficient is nonnegative and finite for bounded \(f\). If stationarity is initially stated only for bounded continuous tests, those tests identify the two finite Borel measures in (1), so the identity extends to all bounded Borel tests. Mere measurability of \(x\mapsto B_x\) suffices for this step.

## Embedded-chain invariance and the negative-power test

Define
\[
q(x)=xD+2mx^\alpha,\qquad
\rho(dx)=\frac{q(x)n(dx)}{3mD}.
\]

The denominator is correct because \(\int q\,dn=mD+2mD=3mD\). The probability transition kernel is
\[
P(x,A)=\frac{xD}{q(x)}
\int\mathbf1_A(x+y)\frac{y^\alpha n(dy)}D
+\frac{2mx^\alpha}{q(x)}
\int\mathbf1_A(\theta x)\frac{B_x(d\theta)}2.
\tag{2}
\]

Equation (1) states precisely that \(\rho P=\rho\). This is a flux-normalized embedded jump chain, not a claim that \(n/N\) is invariant for that discrete-time kernel.

Take \(g(x)=x^{-\alpha}\). Although \(\int g\,dn\) need not be finite,
\[
\int q(x)g(x)\,n(dx)
=D M_{1-\alpha}+2mN<\infty,
\tag{3}
\]

because \(0\le1-\alpha<1\) and \(x^{1-\alpha}\le1+x\). At \(\alpha=1\), \(M_{1-\alpha}=N\).

Apply invariance first to \(g\wedge j\), then let \(j\to\infty\) by monotone convergence. This proves
\[
\int Pg\,d\rho=\int g\,d\rho<\infty.
\]

Thus both the gain and the loss integrals of \(g\) are finite, even if some individual daughter laws have infinite negative-power moments on an \(n\)-null set of parents. It is now legitimate to subtract them and obtain
\[
\int q(x)[Pg(x)-g(x)]\,n(dx)=0.
\tag{4}
\]

There is no hidden use of a negative moment of \(n\), nor an unjustified subtraction of two infinite quantities.

## Fragmentation lower bound

The fragmentation part of the left side of (4) is
\[
F=m\int\left[\int\theta^{-\alpha}B_x(d\theta)-2\right]n(dx).
\]

The probability law \(B_x/2\) has mean \(1/2\). Convexity of \(\theta\mapsto\theta^{-\alpha}\), with extended-valued Jensen if necessary, gives
\[
\int\theta^{-\alpha}B_x(d\theta)\ge2^{1+\alpha}.
\]

Hence
\[
F\ge2mN(2^\alpha-1).
\tag{5}
\]

Finiteness needed to compare this to the coagulation term is already supplied by the invariant-chain argument, rather than being an additional daughter assumption.

## Coagulation loss and its constant

The coagulation contribution is \(-L\), with
\[
L=\iint xy^\alpha
\left[x^{-\alpha}-(x+y)^{-\alpha}\right]n(dx)n(dy)\ge0.
\tag{6}
\]

It is finite even before the sharper estimate, since it is bounded by \(M_{1-\alpha}D\). Write \(s=x+y\) and \(t=x/s\in(0,1)\). Symmetrizing gives
\[
2L=\iint s\,C_\alpha(t)\,n(dx)n(dy),
\]
\[
\begin{aligned}
C_\alpha(t)={}&t^{1-\alpha}(1-t)^\alpha
+(1-t)^{1-\alpha}t^\alpha\\
&-t(1-t)^\alpha-(1-t)t^\alpha.
\end{aligned}
\]

For \(0<\alpha\le1\), concavity of \(z^\alpha\) gives \(z^\alpha-1\le\alpha(z-1)\). Apply it at \(z=1/t\) and \(z=1/(1-t)\) to obtain
\[
\begin{aligned}
C_\alpha(t)
={}&t(1-t)^\alpha(t^{-\alpha}-1)
+(1-t)t^\alpha((1-t)^{-\alpha}-1)\\
\le{}&\alpha\left[(1-t)^{1+\alpha}+t^{1+\alpha}\right]
\le\alpha.
\end{aligned}
\]

Therefore \(2L\le\alpha\iint(x+y)\,dn\,dn=2\alpha mN\), or
\[
L\le\alpha mN.
\tag{7}
\]

The factor of two from symmetrization is essential and has been handled correctly.

## Strict contradiction

Combining (4), (5), and (7) yields
\[
0=F-L\ge mN\left[2(2^\alpha-1)-\alpha\right]>0.
\]

The last inequality is strict for every \(\alpha>0\): \(2^\alpha\ge1+\alpha\log2\) gives the lower bound \(\alpha(2\log2-1)>0\). This establishes the stated stationary nonexistence theorem throughout \(0<\alpha\le1\), including the endpoint \(\alpha=1\).

The proof does not cover \(\alpha=0\) by this test, because the positive gap then vanishes and \(g=1\). Nor does it cover \(\alpha>1\), where both the moment finiteness and concavity steps change.

## A direct coefficient corollary

If the model instead specifies an arbitrary constant coefficient \(S(x)=\sigma x^\alpha\), with \(\sigma\ge0\), every prospective finite-count, finite-positive-mass stationary state must satisfy, by testing one,
\[
0=(\sigma-m)D.
\]

Since \(D>0\), stationarity forces \(\sigma=m\). The preceding contradiction then applies. Thus the no-stationary-state conclusion holds for every fixed selection coefficient \(\sigma\ge0\) in this family: the critical coefficient is a necessary stationarity condition, not an extra assumption that permits other finite stationary states outside it.

This excludes finite-count equilibria only. It does not exclude stationary measures with infinite particle number, states with zero physical mass, a mass source or sink, modified daughter-number assumptions, or equations on a different state space with additional boundary fluxes.

## Novelty and interpretation

The invariant-flux measure and monotone-convergence justification are standard Markov-kernel tools. The proof's useful substantive step is the explicit negative-power drift comparison, particularly the bound \(L\le\alpha mN\). Whether this stationary obstruction is already known for some or all of the specified kernel family requires a separate literature comparison. This review gives no publication-novelty verdict.

## Final audit of the written result and supporting calculation

On 2026-09-07 I read the complete [power-kernel manuscript](../results/count-neutral-power-kernels.md), including its arbitrary-coefficient corollary, multiplicative endpoint, atomic counterexample, and critical stationary-family comparison. The theorem text matches the proof checked above. No mathematical correction was needed.

For equal splitting and \(n_R=\delta_1+R^{-1}\delta_R\), the two self-coagulation terms sum to
\[
(2^p-2)(1+R^{\alpha+p-1}).
\]

The cross-coagulation term is
\[
(1+R^{\alpha-1})[(1+R)^p-1-R^p].
\]

Since the initial mass is two, fragmentation contributes
\[
2(2^{1-p}-1)(1+R^{\alpha+p-1}).
\]

Adding these establishes equation (12) of the manuscript, with
\[
A_p=2^p+2^{2-p}-4=(2^p-2)^2/2^p>0
\quad(0<p<1).
\]

For \(p>1-\alpha\), its positive first term diverges as \(R\to\infty\). The cross term tends to \(-1\) when \(0<\alpha<1\), and to \(-2\) when \(\alpha=1\), so the claimed eventual positivity follows. This is not a claim that every finite test radius has positive drift.

The special value \(\alpha=1,p=1/2,R=64\) gives exactly \(27\sqrt2+2\sqrt{65}-54\). I read and ran the [verification script](../verification/count_neutral_power.py). Its direct atomic sums agreed with the closed formula in all four checks. The rational bounds \(707/500<\sqrt2\) and \(4031/500<\sqrt{65}\) certify the strictly positive lower bound \(151/500\). Two general-\(\alpha\) checks printed negative derivatives at their chosen finite radii, consistently with the manuscript's asymptotic-only positivity assertion. No global mass-conserving dynamics is inferred from this instantaneous generator calculation.

I independently inspected the kernel convention and Proposition 4.3/Remark 4.4 in [Tran–Van, arXiv:1910.13424v3](https://arxiv.org/pdf/1910.13424). Their coagulation kernel is \(xy\); their constant breakup kernel gives selection \(x/2\) and uniform fractions. Accordingly, if their critical mass-one solution is \(c_\tau\), substitution \(n_t=m c_{2mt}\) produces \(K=2xy\) and selection \(mx\). Both quadratic coagulation and linear fragmentation acquire the same factor \(2m^2\), confirming the rescaling.

For the stationary transform relation \(G/(1-G)^3=Cq\), the relevant branch has \(G\to1\) as \(q\to\infty\). Therefore \(F'=1-G\sim(Cq)^{-1/3}\), and integration gives \(F(q)\sim(3/2)C^{-1/3}q^{2/3}\). Its divergence implies infinite particle number by monotone convergence in the Bernstein representation, whereas \(F'(0)=1\) gives finite unit mass before rescaling. This confirms the manuscript's essential distinction between known infinite-count equilibria and the finite-count states excluded here. It does not upgrade transformed-equation well-posedness to a global population-solution theorem.

The current developments have been fully reviewed within this scope. No further parameter regimes or new directions were pursued in this final audit.
