# Independent review of additive-kernel existence proof

Date: 2026-09-07. Reviewer: `/root/closure_direction/review_rigidity`.

Reviewed proof design supplied by `closure_direction`, followed by the complete written version of [additive-model-wellposedness.md](../results/additive-model-wellposedness.md) on this date. The written proof incorporates the construction and limiting arguments checked below, with no substantive defect found. Scope: existence, positivity, conservation of first mass moment, moment bounds, and compactness. Uniqueness is not claimed here.

## Verdict and precise assumptions

The proposed proof is sound with weak measure integrals throughout. The principal care points are positivity of the time-dependent Picard construction, exclusion of dust at zero, and avoiding an unjustified Bochner differential equation in total variation when daughter atoms move with time. None requires additional regularity of the daughter kernel.

The hypotheses checked are:

- \(\lambda,\sigma\ge0\) almost everywhere and \(\lambda,\sigma\in L^1_{\mathrm{loc}}([0,\infty))\). Nonnegativity must be explicit; local integrability alone would not suffice.
- \(t\mapsto B_t\) is a measurable kernel of finite nonnegative measures on \((0,1)\): \(t\mapsto B_t(A)\) is measurable for every Borel set \(A\), and, almost everywhere,
  \[
  B_t((0,1))=2,\qquad \int_0^1\theta\,B_t(d\theta)=1.
  \]
- The initial measure \(\mu_0\) is finite and nonnegative on \((0,\infty)\), with finite moments
  \[
  N_0=\int1\,d\mu_0,\quad m=\int x\,d\mu_0,\quad M_{2,0}=\int x^2\,d\mu_0.
  \]
- The coagulation kernel is \(K_t(x,y)=\lambda(t)(x+y)\). Fragmentation sends a parent \(x\) to the offspring measure obtained from \(B_t\) by \(\theta\mapsto\theta x\), at selection rate \(\sigma(t)\).

Write \(\Lambda(t)=\int_0^t\lambda(s)\,ds\) and \(\Sigma(t)=\int_0^t\sigma(s)\,ds\). The zero initial measure is a separate trivial case.

## A positive construction for each truncated kernel

Set \(K_t^{(n)}(x,y)=\lambda(t)\min(x+y,n)\), and use the weight \(w(x)=1+x+x^2\). The manuscript uses the equivalent weight \(1+x^2\); both make the first-moment functional bounded and give the same proof. The weighted total-variation norm is \(\|\eta\|_w=\int w\,d|\eta|\). For a measurable family of signed measures \(\eta_t\), define its time integral weakly on Borel sets, provided \(\int\|\eta_t\|_w\,dt<\infty\). Countable additivity follows by dominated convergence, and

\[
\left\|\int_s^t\eta_u\,du\right\|_w
\le\int_s^t\|\eta_u\|_w\,du.
\tag{1}
\]

This estimate does not require strong measurability in weighted TV. It also makes the indefinite integral continuous in that norm. For example, moving atoms \(\delta_{\theta(t)x}\) may fail strong measurability in TV, while their weak time integrals are perfectly legitimate finite measures. Such paths need not have a TV derivative.

A concrete positivity argument is available. On a local interval, choose \(R>\|\mu_{\mathrm{initial}}\|_w\) and work in the closed set of continuous nonnegative measure paths with \(\sup_t\|\mu_t\|_w\le R\). Let

\[
H_n(t)=nR\lambda(t)+\sigma(t),\qquad
\ell_n[\mu_t](x)=\lambda(t)\int\min(x+y,n)\,\mu_t(dy).
\]

Then \(0\le\ell_n[\mu_t](x)\le nR\lambda(t)\). Write \(G_n[\mu_t]\) for the coagulation gain and \(J_t[\mu_t]\) for the fragmentation gain, including their rates. The damped integral map is

\[
\begin{aligned}
\Psi(\mu)_t={}&e^{-\int_0^tH_n}\mu_0\\
&+\int_0^t e^{-\int_s^tH_n}
\left\{G_n[\mu_s]+J_s[\mu_s]
+[nR\lambda(s)-\ell_n[\mu_s]]\mu_s\right\}\,ds.
\end{aligned}
\tag{2}
\]

On a continuation interval the lower endpoint and initial measure are changed accordingly. Every integrand in (2) is nonnegative. The map remains in the ball and is a contraction when \(\int(\lambda+\sigma)\) over the interval is sufficiently small, with the size depending on \(n,R\). Indeed, \(w(x+y)\le2w(x)+2w(y)\), so the coagulation gain is bounded by \(2n\lambda R^2\) in weighted norm. The remaining positive coagulation term is bounded by \(n\lambda R^2\). The fragmentation gain is bounded by \(2\sigma R\), since

\[
\int w(\theta x)\,B_t(d\theta)
=2+x+x^2\int\theta^2B_t(d\theta)\le2+x+x^2\le2w(x).
\]

The same bounds after bilinear polarization give local Lipschitz continuity of the integral map. Measurability of all kernels follows from measurability of \(B\) and the TV-continuous input paths, using the usual monotone-class argument. Uniform convergence in weighted norm preserves this measurability.

The fixed point solves the original truncated weak integral equation because the damping terms cancel. This supplies positivity without presuming that direct signed Picard iterates preserve it. It also supplies the local solution in a space where the first two moment tests are justified.

## Moment estimates and global continuation

The tests \(1,x,x^2\) are bounded linear functionals on the weighted-measure space. Their scalar integral identities follow by Fubini; no limiting use of unbounded test functions is necessary at this stage. The moment functions are absolutely continuous even though the measure path need not be TV differentiable.

First mass is conserved exactly, because both truncated coagulation and fragmentation conserve it eventwise. Number obeys

\[
(N_n)'(t)=\sigma(t)N_n(t)
-\frac{\lambda(t)}2\iint\min(x+y,n)\,\mu_t^n(dx)\mu_t^n(dy)
\le\sigma(t)N_n(t).
\]

Therefore \(N_n(t)\le N_0e^{\Sigma(t)}\). For the second moment, the coagulation event increment is \(2xy\), while the fragmentation increment is nonpositive because \(\theta^2\le\theta\). Consequently

\[
(M_{2,n})'(t)
\le\lambda(t)\iint(x+y)xy\,\mu_t^n(dx)\mu_t^n(dy)
=2m\lambda(t)M_{2,n}(t).
\]

Thus

\[
M_{2,n}(t)\le M_{2,0}e^{2m\Lambda(t)}.
\tag{3}
\]

These uniform bounds control the weighted norm on every finite time interval. For each fixed \(n\), they allow the local construction to continue globally. They also prove that first-moment conservation was not obtained from a limiting equation that might already have lost mass.

## Excluding dust uniformly in truncation and time

For any bounded nonnegative decreasing Borel function \(f\), its coagulation event bracket satisfies

\[
f(x+y)-f(x)-f(y)\le0.
\]

The pure-fragmentation propagator preserves the cone of such functions. Its backward action from time \(t\) to time \(s\) is

\[
U^*_{t,s}f(x)=e^{\Sigma(t)-\Sigma(s)}
\mathbb E f\!\left(x\prod_{j:\,s<\tau_j\le t}\Theta_j\right),
\tag{4}
\]

where the points \(\tau_j\) have intensity \(2\sigma(u)\,du\), and the mark at time \(u\) has law \(B_u/2\). Formula (4) follows either from the bounded linear fragmentation equation or its absolutely convergent weak Dyson series.

Variation of constants, treating truncated coagulation as an integrable signed forcing, gives the domination

\[
\langle f,\mu_t^n\rangle
\le\langle U^*_{t,0}f,\mu_0\rangle.
\tag{5}
\]

For full rigor, derive this identity by weak Dyson expansion and scalar Fubini, or by the weak linear propagator identity. Do not simply differentiate a time-dependent backward test in a Banach norm without proving the needed derivative exists.

Couple all products for \(t\le T\) using one marked Poisson process on \([0,T]\). Since its intensity is finite and every mark lies in \((0,1)\), its terminal product \(P_T\) is strictly positive almost surely, and \(P_t\ge P_T\). Taking \(f(x)=\mathbf1_{(0,\varepsilon)}(x)\) in (5) yields

\[
\sup_{n,\,t\le T}\mu_t^n((0,\varepsilon))
\le e^{\Sigma(T)}\int\mathbb P(xP_T<\varepsilon)\,\mu_0(dx)
\longrightarrow0.
\tag{6}
\]

Dominated convergence uses \(x>0\), \(P_T>0\), and finite \(N_0\). No uniform lower bound on daughter fractions is needed. Allowing an atom at zero in \(B_t\), or infinite fragmentation clock intensity on a finite interval, would invalidate this particular argument.

## Compactness and passage to the limit

For the truncated paths, (1) and the event norms imply

\[
\|\mu_t^n-\mu_s^n\|_{\mathrm{TV}}
\le\int_s^t[3\lambda(u)mN_n(u)+3\sigma(u)N_n(u)]\,du.
\tag{7}
\]

The right side gives an equicontinuity modulus uniform in \(n\). At infinity, finite mass gives \(\mu_t^n([R,\infty))\le m/R\). Combined with (6), this proves uniform tightness on the state space \((0,\infty)\), rather than only on its closure. Bounded number, tightness, and equicontinuity yield a subsequence converging narrowly at every time, uniformly on each compact time interval in a metric for narrow convergence. A diagonal extraction handles all finite horizons. One can apply the usual finite-measure version of Prokhorov and metric Arzelà–Ascoli, or embed bounded finite measures into probability measures by adding a cemetery atom.

Equation (3) provides uniform first-moment integrability at infinity:

\[
\int_{x>R}x\,\mu_t^n(dx)\le M_{2,n}(t)/R.
\]

At zero the first moment is at most \(\varepsilon N_n(t)\). Thus the limiting measure conserves first mass \(m\). Its second moment satisfies (3) by lower semicontinuity.

For bounded continuous \(f\), the additive coagulation bracket is continuous in both parent states and bounded in absolute value by \(3\|f\|_\infty\). Product measures converge narrowly. Uniform control of its linear growth follows from

\[
\iint(x+y)\mathbf1_{\{x+y>R\}}\,\mu_t^n(dx)\mu_t^n(dy)
\le\frac{2N_n(t)M_{2,n}(t)+2m^2}{R}.
\tag{8}
\]

This also controls replacement of \(\min(x+y,n)\) by \(x+y\). The time integrands are dominated by \(3\|f\|_\infty\lambda(t)mN_n(t)\), an integrable bound on compact intervals.

For each fixed time, the fragmentation adjoint

\[
x\longmapsto\int f(\theta x)\,B_t(d\theta)-f(x)
\]

is bounded continuous in \(x\), by dominated convergence in the finite measure \(B_t\). No continuity in time is required. Its integrals converge by narrow convergence and are dominated in time by \(3\|f\|_\infty\sigma(t)N_n(t)\). Therefore the limiting path satisfies the full weak integral equation.

The TV modulus (7) passes to the limit by lower semicontinuity of total variation under narrow convergence of signed differences. A narrowly continuous finite-measure path is a measurable kernel, so the full equation can equivalently be expressed as an equality of finite signed measures using weak time integrals. Neither formulation asserts a strong TV derivative.

## Additional check and limitations

Once existence and conservation of first mass are established, the untruncated number equation closes exactly:

\[
N'(t)=[\sigma(t)-m\lambda(t)]N(t),
\qquad N(t)=N_0e^{\Sigma(t)-m\Lambda(t)}.
\]

This is a useful consistency check and a sharper bound for the limit. It must not be assumed for the truncated kernels, whose number equation is different.

The proof establishes existence in the finite-number, finite-first-moment class with the displayed second-moment bound and weak-integral time regularity. It makes no uniqueness assertion. The finite second moment is used concretely for uniform first-moment integrability and coagulation-tail passage; removing it would require another argument. No new literature novelty is asserted for this existence construction.

The argument is for a selfsimilar daughter-fraction law \(B_t\) independent of parent size. An arbitrary merely measurable parent-dependent law \(B_{t,x}\) is outside its scope: the pure-fragmentation propagator need not preserve decreasing tests, the common-product dust comparison need not hold, and its adjoint need not map continuous tests to continuous functions of \(x\). This report does not extend the proof to that controlled model. No third-moment construction is needed for the present theorem.
