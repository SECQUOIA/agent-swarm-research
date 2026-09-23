# Independent review: a physical-bath threshold from three support points

Date: 2026-09-07. Reviewer: nucleation scout. Scope: the proposed total-variation theorem for arbitrary canonical energy laws with a nontrivial scaling limit. Core research notes were not edited.

## Verdict

The theorem is correct under the stated assumptions. No central limit theorem, density, moment bound, within-phase fluctuation model, or uniform tail estimate is needed. The proof handles discrete energy distributions, arbitrary positive bath exponents, arbitrary total-energy tuning, and the physical cutoff.

The three-support-point condition is essential to this formulation. A two-atom energy law can be reproduced exactly by tuning the total energy even when the bath exponent is arbitrarily small.

## Precise statement

Let P_N be probability laws of a real energy E. Fix β>0 and deterministic a_N∈R, b_N>0 with b_N→∞. Suppose

\[
 X_N=(E-a_N)/b_N\ \Rightarrow\ X,
\]

where X is a real probability law whose support contains at least three distinct points. Let c_N>0 be arbitrary. For a chosen total energy T_N define

\[
 L_N(E)=e^{\beta E}(T_N-E)_+^{c_N},
 \qquad
 \frac{dQ_N}{dP_N}=\frac{L_N}{Z_N},\quad Z_N=\mathbb E_{P_N}L_N,
\]

whenever 0<Z_N<∞. Interpret the likelihood as zero at and above the cutoff E=T_N.

There exists a sequence T_N for which TV(Q_N,P_N)→0 **if and only if**

\[
 \boxed{c_N/b_N^2\longrightarrow\infty.}
\]

With physical energy units this is equivalently c_N/(βb_N)²→∞ because β is fixed. The sufficient choice is T_N=a_N+c_N/β. The total-energy parameter T_N here should not be confused with temperature.

## Sufficiency: global bounded likelihood removes tail assumptions

Put x=E−a_N and choose T_N=a_N+c_N/β. Divide the likelihood by its positive value at E=a_N, obtaining

\[
 W_N(E)=
 \begin{cases}
 e^{\beta x}(1-\beta x/c_N)^{c_N},&x<c_N/\beta,\\
 0,&x\ge c_N/\beta.
 \end{cases}
\]

For every real x below the cutoff, log(1−y)≤−y with y=βx/c_N<1 gives

\[
 0\le W_N(E)\le1
\]

**globally**, including arbitrarily large negative x. Thus potential tails do not require moment control.

Weak convergence of X_N implies tightness, so x=O_{P_N}(b_N). If c_N/b_N²→∞ and b_N→∞, then x/c_N→0 in probability and x²/c_N→0 in probability. On the event |βx/c_N|≤1/2,

\[
 \log W_N
 =-\frac{\beta^2x^2}{2c_N}
 \left[1+O\!\left(\frac{|x|}{c_N}\right)\right].
\]

This event has probability tending to one and the displayed logarithm tends to zero in probability. Consequently W_N→1 in P_N-probability. The bound 0≤W_N≤1 implies E W_N→1 and E|W_N−1|→0. Hence the normalized laws converge in total variation. For example,

\[
 \frac12\mathbb E\left|\frac{W_N}{\mathbb EW_N}-1\right|
 \le\frac{1-\mathbb EW_N}{\mathbb EW_N}\longrightarrow0.
\]

For all sufficiently large N the expectation is positive, so the chosen physical-bath law is well defined. Multiplying back by the finite reference likelihood shows its original normalization is finite as well.

## Necessity: three likelihood values force weak curvature

Assume some arbitrary total-energy sequence gives TV(Q_N,P_N)→0. Set R_N=L_N/Z_N. Then E|R_N−1|→0. Choose deterministic ε_N↓0 slowly enough that

\[
 P_N(|R_N-1|>\varepsilon_N)\longrightarrow0.
\]

For example ε_N=max(√TV(Q_N,P_N),1/N) works, with an inessential constant in Markov's bound. On its complementary good set, for large N,

\[
 R_N>0,\qquad |\log R_N|\le2\varepsilon_N.
\]

The strict positivity ensures every selected good energy lies below the physical cutoff.

Choose three support points x1<x2<x3 of X, and three fixed disjoint bounded open intervals I1<I2<I3 around them. Choose the intervals sufficiently narrow that the gaps between successive intervals remain positive. Each interval has positive X-probability, so Portmanteau gives liminf P_N(X_N∈Ii)>0. Each interval therefore contains a good energy e_i,N for all sufficiently large N. This is an existence choice and requires neither an energy density nor an atom at the selected point.

Suppress N temporarily. Define

\[
 \Delta=e_3-e_1,\qquad
 \theta=\frac{e_2-e_1}{\Delta},\qquad
 q=\log\frac{T-e_1}{T-e_3}>0.
\]

The fixed separated intervals imply Δ=Θ(b_N) and θ∈[δ,1−δ] for some fixed δ∈(0,1/2). Both numerator and denominator in q are positive because the points are good.

Write g(E)=βE+c log(T−E) below the cutoff. The three good values obey g(e_i)=log Z+o(1). Comparing the endpoints gives

\[
 \boxed{cq=\beta\Delta+o(1),}\tag{1}
\]

so cq→∞, since Δ=Θ(b_N) and b_N→∞.

The middle-point excess above the endpoint chord is

\[
 g(e_2)-(1-\theta)g(e_1)-\theta g(e_3)
 =c\,f_\theta(q)\longrightarrow0,
\]

where

\[
 f_\theta(q)=\log[(1-\theta)e^q+\theta]-(1-\theta)q.
\]

The linear βE contribution cancels exactly. The remainder is nonnegative by concavity of log in the residual bath energy.

### Uniform lower bound on the chord defect

For q∈[0,1],

\[
 f_\theta''(q)=\frac{\theta(1-\theta)e^q}
 {[(1-\theta)e^q+\theta]^2}
 \ge\frac{\delta(1-\delta)}{e^2}.
\]

Since fθ(0)=fθ′(0)=0, this implies

\[
 f_\theta(q)\ge C_\delta q^2,
 \quad C_\delta=\frac{\delta(1-\delta)}{2e^2}.
\]

For q≥1, convexity and fθ(0)=0 imply fθ(q)/q≥fθ(1), giving

\[
 \boxed{f_\theta(q)\ge C_\delta\min(q^2,q)\quad(q>0).}\tag{2}
\]

Thus c min(q²,q)→0. In combination with cq→∞, this forces q→0: if q≥ε>0 along a subsequence, then min(q²,q)≥min(ε,1)q and the chord defect would diverge. We therefore have cq²→0. Equation (1) now yields

\[
 \frac{\Delta^2}{c}
 =\frac{cq^2}{\beta^2}[1+o(1)]\longrightarrow0.
\]

Since Δ=Θ(b_N), b_N²/c_N→0, proving necessity.

This proof did not assume c_N→∞ beforehand; it derives the stronger conclusion. It also did not assume the physical cutoff is far above the energy distribution. Good-likelihood point selection handles the cutoff directly.

## Sharp scope: two atoms defeat the necessity conclusion

Suppose P_N has precisely two atoms e1<e2, with arbitrary positive weights, and Δ=e2−e1. For **any** c>0 choose

\[
 T=e_2+\frac{\Delta}{e^{\beta\Delta/c}-1}.
\]

Then T>e2 and

\[
 \log\frac{T-e_1}{T-e_2}=\beta\Delta/c,
\]

so L(e1)=L(e2). Hence Q_N=P_N exactly. The theorem cannot replace “at least three support points” with mere nondegeneracy.

A two-point *scaling limit* with nonzero within-phase widths is subtler than an exactly two-atom law. The present proof does not determine its bath threshold; separate within-phase analysis is needed. This preserves the distinct role of the repository's two-phase results.

## Consequences and remaining interpretation limits

- If (E−a_N)/√N converges to a nondegenerate Gaussian or any real law with at least three support points, the optimized physical-bath threshold is c_N≫N. Only weak convergence is used, not the Gaussian shape or its moments.
- If E/N has a limiting law containing three distinct phase-energy atoms, the optimized threshold is c_N≫N². No central limit theorem inside the phases is needed.
- More generally b_N can be any diverging fluctuation scale with an appropriate weak limit. The threshold concerns total variation of the **complete energy law**, not just means, individual observables, local marginals, or logarithmic large-deviation rates.
- The target inverse temperature β is fixed and the only bath control optimized here is total energy. Allowing other changes to the physical bath density of states is a different problem.
- This review establishes correctness, not novelty. The elementary strict-concavity argument is distinctive in this proof, but comparisons with earlier finite-reservoir/ensemble-equivalence literature remain the responsibility of the main investigation.
