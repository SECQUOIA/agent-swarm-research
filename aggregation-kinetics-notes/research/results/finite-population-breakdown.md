# Mass-distribution breakdown while particle count remains accurate

Date: 2026-09-06. Status: independently verified consequence of the independently checked fractional-moment theorem, conditional on its deterministic weak-solution class. Literature novelty remains unresolved. The birth–death formulas and Feller diffusion limit are classical tools, not proposed contributions.

## 1. Model and the two observation scales

Fix mass density m>0 and λ>0, and put b=λm. For each integer n≥1, a finite stochastic system starts with deterministic positive particle masses x_1,…,x_{L_0^n} whose sum is nm. Each unordered pair i<j merges at rate

\[
 \frac{\lambda}{n}(x_i+x_j).
\]

Each particle fragments at rate b into exactly two positive masses summing to its own mass. The split may follow any measurable, size-dependent probability law. It need not be equal or symmetric as an ordered pair. Standard independent event clocks define the Markov process. All results below are independent of the allocation of mass between daughters. They do depend on the fixed total mass through b=λm.

Write L^n(t) for particle count and

\[
 \mu_t^n=\frac1n\sum_{i=1}^{L^n(t)}\delta_{x_i(t)},\qquad
 c_n=\frac{L_0^n}{n},\qquad
 \rho_t^n(dx)=\frac{x\mu_t^n(dx)}m.
\]

The measure ρ_t^n is a probability distribution describing the particle size seen by a uniformly selected unit of material. Assume sup_n c_n<∞.

Let ν_t^n be the deterministic coagulation–fragmentation solution initialized **exactly** at μ_0^n, with kernel K(x,y)=λ(x+y), fragmentation rate b, and the same expected daughter law. We use the mass-conserving global weak-solution class of [the fractional-moment theorem](invisible-kinetics-extension.md), rather than asserting a new existence theorem. It has number c_n and mass m at every finite time. Set

\[
 \bar\rho_t^n(dx)=\frac{x\nu_t^n(dx)}m.
\]

The main conclusion is a separation of two time scales. The stochastic particle count per n remains close to its constant deterministic prediction on **every o(n) time interval**. Nevertheless, at time C log n for every C>1/(b log 2), the deterministic and stochastic mass-size cumulative distributions differ by an amount tending to their maximum possible discrepancy, one. The comparison starts from identical measures; no initial approximation error is involved.

## 2. Exact count process and concentration

**Proposition 1.** The count has the autonomous birth and death rates

\[
 \ell\longrightarrow\ell+1:\ b\ell,
 \qquad
 \ell\longrightarrow\ell-1:\ b(\ell-1),
 \qquad\ell\geq1.
 \tag{1}
\]

For deterministic L_0^n,

\[
 E L^n(t)=L_0^n+bt,
\qquad
 \operatorname{Var}L^n(t)=b(2L_0^n-1)t+b^2t^2.
 \tag{2}
\]

For every deterministic T≥0,

\[
 E\left[\sup_{0\leq t\leq T}
 \left|\frac{L^n(t)}n-c_n\right|^2\right]
 \leq
 \frac{8b(2L_0^n-1)T+10b^2T^2}{n^2}.
 \tag{3}
\]

Consequently, if T_n=o(n), then the supremum in (3) converges to zero in L² and in probability. In particular, this applies to T_n=C log n.

**Proof.** In any configuration,

\[
 \sum_{i<j}(x_i+x_j)=(\ell-1)\sum_i x_i
 =(\ell-1)nm.
\]

Thus total coagulation rate is b(ℓ−1), whereas total fragmentation rate is bℓ. These rates depend only on count. The full event rate is b(2ℓ−1); linear growth of the event rate and unit count changes imply nonexplosion, for example by comparison with a linear pure-birth event counter. The mass stays nm pathwise and every particle remains positive.

The count generator applied to ℓ and ℓ² gives respectively b and 4bℓ−b. The compensated process

\[
 M_t=L^n(t)-L_0^n-bt
\]

is a square-integrable martingale with predictable quadratic variation

\[
 \langle M\rangle_t=\int_0^t b(2L^n(s)-1)\,ds.
\]

Taking expectations gives (2), including

\[
 E M_T^2=b(2L_0^n-1)T+b^2T^2.
\]

Doob's L² inequality and |u+v|²≤2u²+2v² give (3). All moment calculations can first be stopped at a finite count and then unstopped using the linear-rate comparison. ∎

The finite count is not exactly neutral: the missing self-pair produces a drift b in L, or b/n in the normalized count. Mean-field neutrality discards that finite correction. The variance is more important than this drift at logarithmic times, but both normalized effects vanish there.

Concentration here is absolute. Relative count accuracy and the statement that order-n particles remain are valid, for example, when c_n tends to a positive constant; they need not hold if c_n→0.

## 3. A nearly maximal mass-CDF discrepancy at logarithmic times

For probability measures α,β on (0,∞), define

\[
 d_{\rm CDF}(\alpha,\beta)
 =\sup_{R>0}|\alpha((0,R])-\beta((0,R])|.
\]

Its largest possible value is one. Unlike total variation between an empirical measure and a density, this metric does not automatically give maximal error merely because one measure is atomic.

**Theorem 2.** Fix C>1/(b log 2). There is a fixed p∈(0,1), independent of n, such that

\[
 \eta:=bC\kappa_p-(1-p)>0,
 \qquad\kappa_p=3-2^p-2^{1-p}.
\]

At T_n=C log n, every realization satisfies

\[
 d_{\rm CDF}(\rho_{T_n}^n,\bar\rho_{T_n}^n)
 \geq 1-c_n^{1-p}n^{-\eta}.
 \tag{4}
\]

Thus the mass-CDF discrepancy tends to one pathwise, uniformly over all initial configurations with bounded c_n and all admissible binary daughter laws. At the same time (3) shows

\[
 \sup_{t\leq T_n}|L^n(t)/n-c_n|\longrightarrow0
 \quad\text{in }L^2.
 \tag{5}
\]

The assertion (4) also holds with the expected stochastic mass distribution Eρ_{T_n}^n in place of a single realization.

**Proof.** Every finite particle has size at most the total physical mass nm, so

\[
 \rho_t^n((0,nm])=1
 \tag{6}
\]

pathwise for every time. The fractional-moment result gives

\[
 M_p(\nu_t^n)\leq M_p(\nu_0^n)e^{-\kappa_pbt}.
\]

Hölder's inequality and the exactly matched initial number and mass give

\[
 M_p(\nu_0^n)\leq c_n^{1-p}m^p.
\]

For x≤nm, x≤(nm)^{1-p}x^p. Therefore

\[
 \bar\rho_t^n((0,nm])
 \leq\frac{(nm)^{1-p}}m M_p(\nu_0^n)e^{-\kappa_pbt}
 \leq(nc_n)^{1-p}e^{-\kappa_pbt}.
 \tag{7}
\]

Since κ_p/(1−p)→log 2 as p↑1, the strict condition on C permits a **fixed** p<1 with η>0. Setting t=C log n in (7) and comparing with (6) proves (4). No n-dependent exponent limit or uniformity in p is needed. Taking expectation preserves (6), so the same argument applies to the expected empirical measure. ∎

This is a mass-localization obstruction. The deterministic equation eventually places almost all material in particles larger than the entire finite system could contain, although its particle-count prediction remains accurate. It proves that uniform-in-time mean-field accuracy cannot extend through all logarithmic horizons in this metric. It does **not** prove accuracy at earlier growing times, locate the first breakdown time, or identify the sharp threshold constant.

The normalized total-variation distance \(\sup_A|\rho(A)-\bar\rho(A)|\) is at least the CDF distance and hence also tends to one. With the signed-measure norm \(\sup_{|f|\leq1}|\int f\,d(\rho-\bar\rho)|\), the corresponding lower bound is twice (4). The CDF statement is the substantive formulation.

### Relative moment separation and the omitted diagonal

The physical upper size bound also gives, pathwise,

\[
 M_p(\mu_t^n)\geq m(nm)^{p-1}=m^pn^{p-1}.
\]

Combining this with the deterministic moment estimate yields

\[
 \frac{M_p(\mu_{T_n}^n)}{M_p(\nu_{T_n}^n)}
 \geq c_n^{p-1}n^\eta.
\]

This is a divergent relative discrepancy, not a nonvanishing absolute moment error. The deterministic denominator is positive because the solution has positive conserved mass.

One can locate the finite correction exactly. If \(\mathscr D_p(\mu)\) is the continuum weak drift of the p-th moment evaluated at an empirical measure μ, then the finite generator satisfies

\[
 \mathcal G_nM_p(\mu)
 =\mathscr D_p(\mu)
 +\frac{\lambda(2-2^p)}nM_{p+1}(\mu).
\]

The correction removes the negative diagonal contribution in the continuum double integral, because a physical particle cannot coagulate with itself. Its formal factor 1/n alone gives no uniform smallness when large particles develop. Fragmentation contributes exactly its continuum linear drift, so it requires no analogous correction.

## 4. Classical diffusion on the later count time scale

**Proposition 3.** If c_n→c≥0, then

\[
 Z_n(\tau):=L^n(n\tau)/n
 \ \Rightarrow\ Z(\tau)
\]

on every finite time interval in the usual Skorokhod path space, where Z is the nonnegative diffusion

\[
 dZ=b\,d\tau+\sqrt{2bZ}\,dW,\qquad Z(0)=c.
 \tag{8}
\]

In particular,

\[
 E Z(\tau)=c+b\tau,
 \qquad\operatorname{Var}Z(\tau)=2bc\tau+b^2\tau^2.
 \tag{9}
\]

This is a critical branching diffusion with immigration, equivalently a rescaled squared Bessel process of dimension two. The diffusion is independent of the daughter law and the initial mass allocation given c and m. Such birth–death–immigration limits are established theory; see [Giorno and Nobile (2021), Section 2](https://www.mdpi.com/2227-7390/9/16/1879), which treats linear birth–death immigration and Feller-type diffusion. A direct specialization is provided next so that no scaling convention is left implicit.

### Direct verification

The shifted count Y=L−1 has birth rate b(Y+1) and death rate bY: critical linear branching with immigration b. A single critical birth–death family has generating function

\[
 u_t(z)=1-\frac{1-z}{1+bt(1-z)}.
\]

It solves ∂_tu=b(u−1)², u_0=z. Independent families initiated by Poisson immigration at rate b give the exact transition generating function

\[
 E[z^{Y_t}\mid Y_0=y]
 =\frac{u_t(z)^y}{1+bt(1-z)}.
 \tag{10}
\]

Indeed the immigration factor is
\(\exp\{b\int_0^t[u_s(z)-1]ds\}=[1+bt(1-z)]^{-1}\).

Substitute t=nτ and z=e^{−θ/n} in (10). For L_0/n→c, the Laplace transform of L(nτ)/n converges to

\[
 E[e^{-\theta Z(\tau)}]
 =\frac1{1+b\tau\theta}
 \exp\left\{-\frac{c\theta}{1+b\tau\theta}\right\}.
 \tag{11}
\]

The same convergence holds for transitions with any sequence of scaled starting states converging to a finite value, uniformly on bounded starting-state sets. The Markov property therefore identifies all finite-dimensional limiting laws.

For completeness, the scaled martingale decomposition is

\[
 Z_n(\tau)=c_n+b\tau+\mathcal M_n(\tau),\qquad
 \langle\mathcal M_n\rangle_\tau
 =\int_0^\tau(2bZ_n(s)-b/n)ds.
 \tag{12}
\]

The nonnegative submartingale Z_n obeys compact containment because
\(\Pr(\sup_{\tau\leq T}Z_n(\tau)>R)\leq(c_n+bT)/R\).
Stopping at level R makes the bracket rate in (12) uniformly bounded. The martingale isometry for increments between bounded stopping times then gives a bound proportional to their time separation; the deterministic drift has the same property. This verifies the stopping-time tightness criterion. Jumps have size 1/n, so every limit is continuous. Thus the finite-dimensional convergence above upgrades to path convergence.

Alternatively, the scaled generators satisfy, uniformly on bounded state sets for C^3 test functions,

\[
 \mathcal A_nf(z)
 =bnz\,n[f(z+1/n)-f(z)]
 +b(nz-1)n[f(z-1/n)-f(z)]
 \longrightarrow bf'(z)+bzf''(z).
\]

The limiting generator and the Laplace transition law (11) are those of (8). One may construct the limit directly as

\[
 Z(\tau)=\frac b2\big[(\sqrt{2c/b}+B_1(\tau))^2+B_2(\tau)^2\big]
\]

for two independent standard Brownian motions. Itô's formula gives drift b and quadratic variation 2bZ,dτ; its Laplace law is (11). This construction also verifies (9). ∎

## 5. Literature comparison and limits of the claim

The potential contribution is the simultaneous statement (4)–(5) for critically balanced additive coagulation and arbitrary constant-rate binary fragmentation, with exactly matched initial empirical data. Each individual tool is elementary or established. Several close lines of prior work prevent broader novelty claims.

- [Kumar and Mondal, *Finite–N scaling, gelation cutoff, and matched asymptotics for Smoluchowski coagulation equation* (2026), Section 3](https://doi.org/10.1186/s13661-026-02222-y), explicitly discusses logarithmic finite-size effects for the additive kernel in **pure coagulation**, associated with depletion to few clusters. Its openly accessible text was inspected. Therefore neither logarithmic finite-size scaling nor the finite-total-mass cutoff is new by itself. When c_n tends to a positive constant, our statement keeps order-n particles through the breakdown interval by critical fragmentation and measures the error through the mass CDF. No claim here relies on that paper's matched-asymptotic assertions as rigorous stochastic identities.
- [D’Orsogna, Lei, and Chou, *First assembly times and equilibration in stochastic coagulation-fragmentation* (2015), open author copy](https://www.math.ucla.edu/~tchou/pdffiles/JCP_LEI.pdf), studies finite systems with a maximum cluster size and finds discrepancies between stochastic and mass-action descriptions. This establishes relevant prior art for failure of mass-action predictions under finite-size constraints. The retrieved abstract concerns different rates, equilibrium and assembly times; the full model still needs detailed comparison before excluding overlap with the present theorem.
- [Giorno and Nobile, *Time-Inhomogeneous Feller-Type Diffusion Process in Population Dynamics* (2021)](https://doi.org/10.3390/math9161879), provides an openly accessible primary reference for birth–death–immigration diffusion approximation. The count formulas and diffusion in Sections 2 and 4 are not novelty candidates.

Searches on 2026-09-06 included “critical birth death immigration process diffusion approximation,” “additive coagulation fragmentation logarithmic finite mean field,” “coagulation fragmentation additive birth death,” and “coagulation fragmentation mass mean-field long-time approximation.” This bounded search found adjacent mechanisms but no inspected source stating the combined constant-count/logarithmic-mass-CDF conclusion. This is a limited negative search, not proof of novelty.

The theorem inherits the deterministic weak-solution assumptions of the fractional-moment result. It does not establish a propagation-of-chaos theorem, a matching lower bound on the breakdown time, a sharp moving-front speed, or validity with a minimum indivisible particle mass. If a minimum size makes binary splitting impossible for small particles, then the constant fragmentation rate and autonomous count law must change.

## 6. Independent verification

An independent agent verified all finite-count identities, the diffusion normalization, the support/moment bound, the CDF interpretation, and the additional moment correction. Its durable report is [finite-population-breakdown-review.md](../reviews/finite-population-breakdown-review.md). The fractional-moment result used in (7) has its separate independent review linked in its source note. No simulation is needed for the exact support obstruction or count algebra.
