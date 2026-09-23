# Independent review: finite-population breakdown at logarithmic times

Reviewed 2026-09-06 by a separate mathematical reviewer. This review checks the proposed finite-population extension of [the fractional-moment theorem](../results/invisible-kinetics-extension.md), including the formulas communicated by its developing author. It makes no literature-novelty claim.

**Verdict.** The count formulas, diffusion scaling, and pathwise mass-CDF separation are correct under the assumptions below. The logarithmic time is a sufficient separation scale, not a proved sharp onset time. The mass-CDF statement avoids the uninformative empirical-versus-continuous total-variation issue.

## 1. Precise assumptions

Fix $\lambda,m>0$ and write $b=\lambda m$. For each integer $n$, a finite initial collection of positive masses has total mass $nm$ and deterministic count $L_0^n\ge1$. Each unordered pair of distinct particles of masses $x,y$ coagulates at rate $\lambda(x+y)/n$. Each particle fragments into two strictly positive, mass-conserving daughters at rate $b$. The split distribution can be arbitrary, subject to the measurability needed to define the process. The usual jump-process construction is understood.

The associated deterministic measure solution $\nu_t^n$ starts from the exact empirical initial measure and belongs to the mass-conserving weak-solution class of Theorem 3 in the linked note. Existence in that class is an assumption here, as it is in the underlying theorem; the present argument is not a new existence proof.

## 2. Exact count chain

For a state with $L$ particles,

$$\sum_{i<j}\frac{\lambda(x_i+x_j)}n
=\frac\lambda n(L-1)\sum_i x_i=b(L-1).$$

The upward count rate is $bL$. Thus $L$ is an autonomous birth-death chain on $\{1,2,\ldots\}$ with generator

$$\mathcal A f(\ell)=b\ell[f(\ell+1)-f(\ell)]
+b(\ell-1)[f(\ell-1)-f(\ell)].$$

No split-law information enters. Linear birth rates give nonexplosion, for example by comparison with a pure birth chain with rates $b\ell$; downward jumps cannot themselves accumulate without intervening upward jumps. Moment calculations can first be stopped and then justified by this comparison.

The generator gives

$$\mathcal A\ell=b,\qquad \mathcal A\ell^2=4b\ell-b.$$

Consequently, for deterministic $L_0$,

$$\mathbb E L_t=L_0+bt,\qquad
\operatorname{Var}(L_t)=b(2L_0-1)t+b^2t^2.$$

In particular, the finite model has a positive count drift even though the continuum count is constant. The omitted self-pairs explain the difference.

Writing $M_t=L_t-L_0-bt$ gives a square-integrable martingale with predictable quadratic variation

$$\langle M\rangle_t=\int_0^t b(2L_s-1)\,ds,$$

and therefore

$$\mathbb E\sup_{s\le T}|M_s/n|^2
\le\frac4{n^2}\{b(2L_0-1)T+b^2T^2\}.$$

If $c_n=L_0^n/n$ is bounded and $T_n=o(n)$, this and $bT_n/n\to0$ prove

$$\sup_{s\le T_n}|L_s^n/n-c_n|\longrightarrow0
\quad\text{in probability}.$$

Convergence of $c_n$ is unnecessary for this statement. This is absolute concentration; it need not be concentration relative to $c_n$ if $c_n\to0$.

## 3. Diffusion time scale

If $c_n\to c\in[0,\infty)$, define $Z_n(\tau)=L_{n\tau}^n/n$. Its generator, at lattice point $z=\ell/n$, is

$$\mathcal A_n f(z)=bn^2z[f(z+1/n)-f(z)]
+(bn^2z-bn)[f(z-1/n)-f(z)].$$

Taylor expansion on compact sets gives

$$\mathcal A_n f(z)\longrightarrow bf'(z)+bzf''(z).$$

At $z=1/n$, the downward coefficient is zero, so the same formula is valid without introducing a jump outside the state space. The martingale representation is

$$Z_n(\tau)=c_n+b\tau+M_{n\tau}/n,$$

with bracket

$$\int_0^\tau [2bZ_n(u)-b/n]\,du.$$

The moment bounds above give compact containment on every bounded $\tau$ interval. After stopping on a compact set, the bracket increments are bounded by a constant times the interval length, and jump sizes are $1/n$. The martingale tightness argument therefore yields continuous subsequential limits, each solving the displayed limiting martingale problem. The nonnegative diffusion

$$dZ_\tau=b\,d\tau+\sqrt{2bZ_\tau}\,dW_\tau,
\qquad Z_0=c,$$

has unique law, including when $c=0$. Hence the convergence holds in the usual Skorokhod path topology on each bounded time interval. Equivalently, $2Z/b$ is a squared Bessel process of dimension two.

An independent exact-distribution check is available. Put $Y=L-1$. It is critical linear birth-death branching with per-capita rates $b,b$ and immigration rate $b$. With

$$F_t(s)=1-\frac{1-s}{1+bt(1-s)},$$

its count probability-generating function is

$$\mathbb E[s^{L_t}]
=\frac{sF_t(s)^{L_0-1}}{1+bt(1-s)}.$$

Taking $t=n\tau$ and $s=e^{-\theta/n}$ gives the limiting transform

$$\mathbb E[e^{-\theta Z_\tau}]
=\frac1{1+b\tau\theta}
\exp\left(-\frac{c\theta}{1+b\tau\theta}\right),$$

which agrees with the diffusion and yields mean $c+b\tau$ and variance $2bc\tau+b^2\tau^2$.

## 4. Fractional-moment input and CDF separation

Theorem 3 gives, for $0<p<1$,

$$M_p(\nu_t^n)\le M_p(\nu_0^n)e^{-b\kappa_pt},
\qquad \kappa_p=3-2^p-2^{1-p}.$$

I checked the pair inequality and its calculus proof in that theorem. The second-derivative sign reduction is correct, including the monotonicity of its ratio $R$. The bounded truncation argument requires only finite count and mass, exactly as stated. Hölder yields

$$M_p(\nu_0^n)\le c_n^{1-p}m^p.$$

Define the mass probability measures

$$\rho_t^n=\frac{x\mu_t^n(dx)}m,
\qquad \bar\rho_t^n=\frac{x\nu_t^n(dx)}m,
\qquad \mu_t^n=\frac1n\sum_i\delta_{x_i(t)}.$$

Each physical mass is at most $nm$, pathwise and for all times. Thus $\rho_t^n((0,nm])=1$. In contrast,

$$\bar\rho_t^n((0,nm])
\le\frac{(nm)^{1-p}}mM_p(\nu_t^n)
\le c_n^{1-p}n^{1-p}e^{-b\kappa_pt}.$$

Since

$$\lim_{p\uparrow1}\frac{\kappa_p}{1-p}=\log2,$$

every fixed $C>1/(b\log2)$ admits a fixed $p<1$ sufficiently near one for which $\eta=bC\kappa_p-(1-p)>0$. At $T_n=C\log n$,

$$\sup_{R>0}|\rho_{T_n}^n((0,R])-\bar\rho_{T_n}^n((0,R])|
\ge1-c_n^{1-p}n^{-\eta}.$$

For bounded $c_n$, this converges to one, the maximum possible CDF distance. There is no probabilistic exceptional set in the bound. The initial microstates may depend arbitrarily on $n$, provided the stated mass and count constraints hold; no initial empirical convergence is required.

The chosen witness $R=nm$ depends on $n$. The conclusion is about a supremum over thresholds and does not assert discrepancy at one fixed, $n$-independent threshold. It nevertheless gives a substantive distributional discrepancy, since the same threshold separates virtually all physical mass from virtually all deterministic mass. It also implies maximal asymptotic total variation under the convention $\sup_A|\rho(A)-\bar\rho(A)|$, but total variation alone can already be maximal for discrete-versus-continuous measures at fixed times. The CDF formulation is therefore preferable.

## 5. Additional checked consequences

The finite population has the pathwise lower bound

$$M_p(\mu_t^n)\ge m(nm)^{p-1}=m^pn^{p-1}.$$

Consequently the same time choice yields

$$\frac{M_p(\mu_{T_n}^n)}{M_p(\nu_{T_n}^n)}
\ge c_n^{p-1}n^\eta.$$

This is a relative moment discrepancy; an absolute fractional-moment difference is not asserted.

For completeness, the exact coagulation correction between the finite empirical generator applied to $M_p$ and the continuum weak drift evaluated at $\mu$ is

$$\frac{\lambda(2-2^p)}nM_{p+1}(\mu).$$

Indeed, the diagonal pair contribution in the continuum double integral is negative and equals $-\lambda(2-2^p)M_{p+1}(\mu)/n$. Removing self-pairs adds the displayed positive term. The nominal factor $1/n$ does not imply a uniform small correction as the size distribution spreads.

The reviewed argument supplies an upper bound on a time by which approximation in mass CDF must fail. It does not prove accurate approximation before that time, the sharp coefficient of a breakdown time, or any novelty claim relative to existing finite-size and coagulation-fragmentation literature.
