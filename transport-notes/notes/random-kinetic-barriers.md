# Random kinetic barriers: zero statistics and coalescing defects

Research note, 2026-09-06. The calculations below concern the wall contribution to dispersion in the constant-affinity model of [exploration-interfaces.md](exploration-interfaces.md). The Gaussian zero statistics are direct consequences of classical Kac–Rice theory. The proposed contribution is their combination with singular transport, especially the moment transition caused by coalescing kinetic zeros. Independent mathematical review is complete; see [review-random-kinetic-barriers.md](review-random-kinetic-barriers.md). The targeted [prior-art audit](random-barrier-prior-art.md) found no exact match, while identifying established bifurcation-dominated moment scaling; this is not proof of novelty.

## Model and fixed-realization limit

Write

\[
H_D=-D\partial_s^2+g(s)^2,\qquad
J_D=\langle1,H_D^{-1}1\rangle.
\]

Use a compact periodic wall, or a bounded interval with reflecting endpoints whose values of `g` are nonzero. Here `D>0` is constant surface diffusivity. The well-mixed flow dispersion is `BJ_D`, where `B=KV²/Z` is independent of the kinetic field when affinity is fixed. Statements about the finite-bulk model require the corresponding remainder estimate.

For a fixed smooth realization with finitely many simple interior zeros `s_j`, the local quadratic-zero result gives

\[
D^{1/4}J_D\longrightarrow C_0 S_L,
\quad S_L=\sum_{s_j\in[0,L]}|g'(s_j)|^{-3/2},
\quad C_0=\frac{\Gamma(1/4)^2}{2\sqrt2}=4.6474760094\ldots.
\tag{1}
\]

If there are no zeros the limit is zero. Formula (1) holds sample by sample. Taking expectations requires an additional uniform-integrability argument.

## Exact Gaussian marked-zero statistics

Let `g` be a stationary real Gaussian process of mean `μ`, variance `σ₀²>0`, derivative variance `σ₁²>0`, with almost surely `C¹` paths and the usual Kac–Rice/Bulinskaya regularity. Assume its zero set is almost surely locally finite and simple. The centered covariance has derivative zero at the origin, so `g(s)` and `g′(s)` are independent. Thus the conditional slope at `g=0` remains `V∼N(0,σ₁²)`.

Applying marked Kac–Rice first to bounded nonnegative marks and then using monotone convergence gives, including possible infinite values,

\[
\mathbb E\sum_{g(s_j)=0}\psi(|g'(s_j)|)
=L p_g(0)\mathbb E[|V|\psi(|V|)],
\quad
p_g(0)=\frac{e^{-\mu^2/(2\sigma_0^2)}}{\sqrt{2\pi}\sigma_0}.
\tag{2}
\]

Consequently

\[
\boxed{\frac{\mathbb E S_L}{L}
=p_g(0)\,\sigma_1^{-1/2}
\frac{2^{-1/4}\Gamma(1/4)}{\sqrt\pi}<\infty.}
\tag{3}
\]

No independence between distinct zeros is used. Stationarity is sufficient for this expectation; ergodicity is not needed.

The intensity of zeros is `ρ₀=p_g(0)σ₁√(2/π)`. At a zero chosen according to the stationary zero-point Palm distribution, the slope magnitude `R=|g′|` has density

\[
f_{\mathrm{zero}}(r)=\frac r{\sigma_1^2}e^{-r^2/(2\sigma_1^2)},\qquad r>0.
\]

Thus the transport mark `W=R^{-3/2}` has the exact tail

\[
\boxed{\mathbb P_{\mathrm{zero}}(W>w)
=1-\exp\left[-\frac{w^{-4/3}}{2\sigma_1^2}\right].}
\tag{4}
\]

Its `q`th moment is finite exactly when `q<4/3`. More directly,

\[
\mathbb E S_L^2\ge\mathbb E\sum_j|g'(s_j)|^{-3}
=L p_g(0)\mathbb E|V|^{-2}=\infty.
\tag{5}
\]

This proves infinite variance of the limiting zero sum on every interval of positive length. It does not prove a stable limit on long walls. Small slopes can arise in strongly correlated close pairs, and global dependence may survive at arbitrary distances.

## Counterexample to exchanging disorder average and small diffusivity

Local Gaussian nondegeneracy alone is insufficient even for the mean. On a circle of length `L=2π`, take

\[
g(s)=A\cos s+B\sin s,\qquad A,B\overset{\rm iid}{\sim}N(0,1).
\]

This is a smooth stationary Gaussian process. At every point `(g,g′)` is a nondegenerate standard Gaussian vector. For `R=(A²+B²)^{1/2}>0`, there are two simple zeros and `S_L=2R^{-3/2}`, whose mean is finite by the Rayleigh density `r e^{-r²/2}`. Nevertheless the constant variational test gives

\[
J_D=\sup_f\{2\!\int f-\!\int[D(f')^2+g^2f^2]\}
\ge\frac{L^2}{\int g^2}=rac{2L}{R^2}.
\tag{6}
\]

Hence `E J_D=∞` for every `D>0`, although `E[lim D^{1/4}J_D]<∞`. Rare nearly vanishing amplitudes produce global weak killing, a different mechanism from local near-tangencies. Conditions controlling small-ball probabilities of the whole random field are required for a Gaussian annealed theorem. A mixing assumption excludes this particular example but still needs quantitative estimates before limits can be exchanged.

## Local fold scaling

A generic merger of two zeros has the local form

\[
g(x)=b(x^2-r^2),\qquad b>0.
\]

Set `ℓ=(D/b²)^{1/6}`, `λ=D^{2/3}b^{2/3}`, and `μ=r²/ℓ²`, allowing negative `μ` to represent a minimum which does not cross zero. Then the exact whole-line scaling is

\[
J_{\mathrm{fold}}=D^{-1/2}b^{-1}\mathcal C(\mu),
\quad
\mathcal C(\mu)=\left\langle1,
[-\partial_y^2+(y^2-\mu)^2]^{-1}1\right\rangle_{\mathbb R}.
\tag{7}
\]

The function is finite and positive for every real `μ`. At positive large `μ`, two separated harmonic neighborhoods yield

\[
\mathcal C(\mu)\sim\frac{C_0}{\sqrt2}\mu^{-3/4},
\qquad \mu\to+\infty.
\tag{8}
\]

At negative large `μ`, put `a=|μ|`, rescale `y=√a z`, and divide the equation by `a²`. The diffusion coefficient becomes `a^{-3}` and the potential is `(1+z²)²`, bounded away from zero. The variational upper bound and compactly supported tests give

\[
\mathcal C(-a)\sim\frac\pi2 a^{-3/2}.
\tag{9}
\]

In particular `∫ℝ C(μ)^q dμ` is finite exactly when `q>4/3`. A simple zero with slope magnitude `v=2br` has harmonic width `(D/v²)^{1/4}`. The separated-zero approximation fails when this is comparable to `r`, namely `|v|` of order `D^{1/6}b^{2/3}`. Treating the two divergent marks as independent defects at that scale is incorrect.

## A compact ensemble without amplitude collapse

Choose the exact periodic family

\[
g_c(s)=c+\cos s,\quad 0\le s<2\pi,
\qquad c\sim\mathrm{Uniform}[-2,2].
\]

Its mean squared amplitude is `c²+1/2≥1/2`, excluding (6). For each `D>0`, `J_D(c)` is finite and continuous on the compact parameter interval, so all disorder moments exist.

For fixed `|c|<1`, both zeros have slope magnitude `√(1-c²)` and

\[
J_D(c)\sim2C_0D^{-1/4}(1-c^2)^{-3/4}.
\tag{10}
\]

For fixed `|c|>1`, `J_D(c)→∫(c+cos s)^{-2}ds`, which is finite. At `c=±1`, a quartic zero gives a `D^{-1/2}` response. Near either endpoint, let `t=1-|c|` and `b=1/2`. Uniformly for `t/(D^{1/3}b^{1/3})` in a fixed compact set, localization gives

\[
J_D(c)\sim D^{-1/2}b^{-1}\mathcal C\left(\frac{t}{D^{1/3}b^{1/3}}\right).
\tag{11}
\]

The parameter layer has probability of order `D^{1/3}` and response of order `D^{-1/2}`. This produces different moment exponents above and below `q=4/3`.

The limiting random variable `W=lim D^{1/4}J_D(c)` is zero with probability `1/2`. Its positive part starts at `2C₀`. For `w≥2C₀`, its tail is exactly

\[
\mathbb P(W>w)=\frac12\left[1-\sqrt{1-(2C_0/w)^{4/3}}\right]
\sim2^{-2/3}C_0^{4/3}w^{-4/3}.
\]

This explicit limiting law helps distinguish a broad disorder distribution from a stable sum law, which is not asserted here.

### Moment theorem and its uniform bounds

The following moment formula follows from (10)–(11) and the uniform bound established below. Independent review checked all coefficients and supplied a separate Neumann-bracketing proof of the uniform envelope and the critical logarithmic matching.

For `0<q<4/3`,

\[
\boxed{\mathbb E J_D^q\sim
\frac{2^q C_0^q}{4}
B\!\left(\frac12,1-\frac{3q}4\right)D^{-q/4}.}
\tag{12}
\]

At `q=4/3`,

\[
\boxed{\mathbb E J_D^{4/3}\sim
\frac{2^{1/3}C_0^{4/3}}6
D^{-1/3}\log(1/D).}
\tag{13}
\]

For `q>4/3`,

\[
\boxed{\mathbb E J_D^q\sim
2^{q-4/3}D^{1/3-q/2}
\int_{\mathbb R}\mathcal C(\mu)^q d\mu.}
\tag{14}
\]

Thus

\[
\mathbb E J_D\sim\frac{C_0^2}{\sqrt\pi}D^{-1/4},\qquad
\operatorname{Var}J_D\sim2^{2/3}D^{-2/3}\int\mathcal C^2,
\tag{15}
\]

and `Var(J_D)/(E J_D)²` grows as `D^{-1/6}`. This is a statement about disorder among walls in this ensemble. It is not a long-wall stable limit or a claim about particle displacement being non-Gaussian.

To justify averaging, the needed global bound is, for `|t|<t₀` and `D` small,

\[
J_D(c)\le C\begin{cases}
D^{-1/2}(1+t/D^{1/3})^{-3/4},&t\ge0,\\
D^{-1/2}(1+|t|/D^{1/3})^{-3/2},&t<0.
\end{cases}
\tag{16}
\]

Outside the two fold neighborhoods, the corresponding bounds are `CD^{-1/4}` on the zero-containing region and `C` elsewhere.

Here is an energy proof of (16). The lowest eigenvalue obeys

\[
\lambda_1(H_D)\ge c D^{2/3}(1+t/D^{1/3})^{1/2}\quad(t\ge0),
\qquad \lambda_1(H_D)\ge cD^{2/3}\quad(|t|\le D^{1/3}).
\tag{17}
\]

Near the fold, make the smooth coordinate change `y=2sin(x/2)` after placing its center at `x=0`. This changes the local potential exactly to `(y²/2-t)²` and leaves both the mass and diffusion weights bounded above and below. A fixed partition of unity separates this neighborhood from the remaining wall, where the potential has a fixed positive lower bound. Its gradient errors are `O(D)`, smaller than the lower bounds in (17). After the fold rescaling, the required local coercivity is that of `−∂²+(y²−μ)²`. For bounded `μ`, its lowest eigenvalue has a positive lower bound by compactness and confinement. For large `μ>0`, divide into neighborhoods of `±√μ` of width proportional to `√μ` and their complement. On each neighborhood `(y²−μ)²≥c μ(y∓√μ)²`; harmonic-oscillator coercivity is of order `√μ`. The complement has potential at least `cμ²`; partition errors are `O(μ^{-1})` and are absorbed. This proves (17), including for locally supported functions after extension by zero.

Since the energy `Q_D[f]` bounds both `∫g_c² f²` and `λ₁∫f²`,

\[
Q_D[f]\ge\tfrac12\int(g_c^2+\lambda_1)f^2,
\qquad
J_D(c)\le2\int\frac{ds}{g_c(s)^2+\lambda_1}.
\tag{18}
\]

For `t≥D^{1/3}`, the two root neighborhoods give an integral bounded by `C/(√t√λ₁)≤CD^{-1/4}t^{-3/4}`. The central and outer parts are bounded by the same expression since `λ₁≤Ct²` in that regime; one may use the explicit lower bound in (17) in the denominator of (18). For `|t|≤D^{1/3}`, fold rescaling bounds the integral by `CD^{-1/2}`. For `t≤−D^{1/3}`, use directly `Q≥∫g_c² f²` and `∫1/g_c²≤C|t|^{-3/2}`. These estimates prove (16).

For (12), the rescaled bound on the inside is at most `C t^{-3q/4}`, integrable exactly below the threshold. On the outside it is also bounded by `C|t|^{-3q/4}`: write `|t|=D^{1/3}z` and use `z^{3/4}(1+z)^{-3/2}≤C`. Dominated convergence gives the beta integral. For (14), rescale `t=D^{1/3}b^{1/3}μ` at each fold and use (16) as an integrable envelope. Contributions outside fixed fold neighborhoods are lower order. The logarithmic endpoint (13) additionally uses the separated-zero asymptotic uniformly when `D^{1/3}/t→0` and `t→0`; the same harmonic localization with scale ratio `D^{1/4}t^{-3/4}→0` proves this. Integrating `t^{-1}` over `D^{1/3}≪t≪1` gives `(1/3)log(1/D)` and the coefficient in (13).

## Literature boundary

Kac–Rice identities and Gaussian zero-count fluctuations are classical. A modern primary source is [Assaf, Buckley and Feldheim, *An asymptotic formula for the variance of the number of zeroes of a stationary Gaussian process*](https://arxiv.org/abs/2101.04052), which also explains why zero correlations require more than one-point statistics. The weighted formulas above are applications of that established framework, not new probabilistic identities.

Squared random potentials themselves are established: [Kirsch and Raikov, *Lifshits Tails for Squared Potentials* (2017)](https://arxiv.org/abs/1704.01435) studies the integrated density of states for the square of an alloy-type random field. That spectral low-energy observable and disorder model differ from the source-integrated resolvent `J_D` and the small-diffusivity moment problem here. This distinction alone does not establish novelty.

The function `H^{-1}1` is already central to localization-landscape theory; see [Arnold, David, Filoche, Jerison and Mayboroda, *Computing spectra without solving eigenvalue problems*](https://arxiv.org/abs/1711.04888). Its use as a source problem is not new. The targeted [prior-art audit](random-barrier-prior-art.md) found no exact match for the compact-ensemble theorem, but identifies close conceptual precedents that must be attributed. No stable law, general Gaussian annealed asymptotic, or universal random-medium theorem is claimed.


## Numerical evidence supplied by the parallel calculation

The parent calculation recorded the periodic finite-difference and parameter-quadrature checks in [coalescing-zero-checks.json](../results/coalescing-zero-checks.json). The full-wall results are:

| D | `D^{1/4} E J_D` | `D^{2/3} E J_D²` |
| ---: | ---: | ---: |
| 10⁻³ | 9.876 | 63.3922 |
| 10⁻⁵ | 10.696 | 62.90665 |
| 10⁻⁷ | 11.202 | 62.81445 |
| 10⁻⁹ | 11.527 | 62.79553 |

The predicted mean coefficient is `C₀²/√π≈12.18595`. Independent numerical integration of the pair problem, with leading asymptotic tails beyond `−30<μ<200`, gave `∫C²≈39.555184`, hence the predicted second-moment coefficient `2^{2/3}∫C²≈62.7899403`. Refining the full-wall calculation at `D=10⁻⁹` gave `62.79524`. These are numerical estimates, not certified constants. The slow mean convergence is consistent with a relative correction of order `D^{1/12}`; its coefficient and expansion are not proved here.


Additional parameter-moment checks reuse the periodic solver with 32,768 cells on the half-wall and 70 Gauss nodes on each adapted parameter interval. For the critical moment, `D^{1/3} E J_D^{4/3}/log(1/D)` equals `3.71683, 2.65554, 2.31164` at `D=10⁻³,10⁻⁶,10⁻⁹`, approaching the predicted `1.62860` slowly. For `q=3`, `D^{7/6} E J_D³` equals `314.487,272.077,267.265`; these support a finite positive limiting coefficient but do not independently certify its pair-integral value.


The broad competition between enhanced response and shrinking parameter probability is established in [Berry, Keating and Schomerus, *Universal twinkling exponents for spectral fluctuations associated with mixed chaology* (2000)](https://www.lorentz.leidenuniv.nl/beenakkr/mesoscopics/fulltext/schomerus00.pdf), especially equations (18)–(19), and in [Keating et al., *Periodic orbit bifurcations and scattering time delay fluctuations* (2007)](https://arxiv.org/pdf/nlin/0701025). Those papers study spectral or Wigner time-delay observables. The defensible candidate contribution here is the particular positive integrated-resolvent theorem, its uniform estimates and constants, and its constant-affinity transport consequence. Rare bifurcations dominating different moments is not a new general mechanism.
