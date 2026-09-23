# Additive coagulation has a finite log-size correction at every constant fragmentation rate

Started 2026-09-06. Status: candidate extension with [independent full proof review](../reviews/general-additive-log-proof.md) complete. This strengthens [the critical-rate theorem](log-size-poisson-limit.md). It does not require constant particle count. Novelty must be assessed against the more general additive-coagulation and pure-fragmentation literature.

## Setting

Let n_t be a global nonnegative mass-conserving weak solution, with finite initial count N_0>0 and mass m>0, for

\[
 K(x,y)=\lambda(x+y),\quad \lambda>0,
 \qquad S(x)=\sigma\ge0.
\]

Put b=λm. The expected daughter fractions have a size-independent measure B on (0,1), with total count two and first fraction moment one. Define Θ~B/2 and Y=log Θ. Sizes are nondimensionalized by a fixed reference size. No logarithmic moments are assumed unless explicitly stated.

The count balance is exact:

\[
 N(t)=N_0e^{(\sigma-b)t}.
\tag{1}
\]

Let η_t=n_t/N(t), π_t=x n_t/m, and ρ_t=(log)#η_t. Here η and π are the number and mass probability laws.

## Theorem 1: separation of the two sampling laws

For every 0<p<1, write

\[
 \mathcal A_p(t)=\frac{M_p(t)}{N(t)^{1-p}m^p}
 =\int\left(\frac{d\pi_t}{d\eta_t}\right)^p d\eta_t,
 \qquad a_p=1+p-2^p>0.
\]

Then

\[
 \boxed{\quad
 \mathcal A_p(t)\le\mathcal A_p(0)
 e^{-[b a_p+\sigma a_{1-p}]t}.
 \quad}
\tag{2}
\]

In particular, the Hellinger affinity between η and π is

\[
 \mathcal A_{1/2}=\frac{H(t)}{\sqrt{mN(t)}},\qquad H=M_{1/2},
\]

and its square decreases at least at rate κ(b+σ), where κ=3−2√2:

\[
 \frac{H(t)^2}{N(t)}
 \le\frac{H_0^2}{N_0}e^{-\kappa(b+\sigma)t}.
\tag{3}
\]

These are relative sampling-law statements. Outside the critical case σ=b, they do not imply that raw material mass escapes to infinity. For example, strong fragmentation may drive both sampling laws toward small raw sizes while their relative weighting separates.

**Proof.** The [sharp pair inequality](invisible-kinetics-extension.md) and daughter Jensen inequality give

\[
 M_p'\le\{-b(2-2^p)+\sigma(2^{1-p}-1)\}M_p.
\]

The same bounded truncation argument is valid on every finite time interval, using M_p≤N(t)^{1-p}m^p and (1). Subtracting (1−p)N'/N from the logarithmic growth bound gives

\[
 -b[(2-2^p)-(1-p)]
 +\sigma[(2^{1-p}-1)-(1-p)]
 =-b a_p-\sigma a_{1-p}.
\]

One can avoid dividing by M_p by applying an integrating factor directly. This proves (2). Since a_1/2=κ/2, squaring proves (3). ∎

The coefficient in (2) is the largest uniform instantaneous coefficient for a fixed p over all initial populations and binary daughter laws: monodisperse initial data and equal splitting attain every inequality at time zero. The Hellinger/Rényi interpretation is established information geometry; the dynamical inequality is the statement under investigation.

## Theorem 2: uniform finite-cost Poisson coupling

Let Z_0~ρ_0, let J_t be Poisson with mean 2σt, and let Y_j be independent copies of Y, independent of J and Z_0. Define

\[
 \bar\rho_t=\operatorname{Law}(Z_0+\textstyle\sum_{j=1}^{J_t}Y_j).
\]

For every t there is a monotone coupling Z_t≥barZ_t with respective laws ρ_t and barρ_t. Its expected displacement is exactly the extended transport cost, and

\[
 W_1(\rho_t,\bar\rho_t)=\int_0^t a(s)\,ds
 \le C_0(1-e^{-\kappa(b+\sigma)t}),
\tag{4}
\]

where

\[
 a(s)=\frac\lambda{N(s)}\iint x\log(1+y/x)n_s(dx)n_s(dy),
 \qquad
 C_0=\frac{\lambda H_0^2}{\kappa(b+\sigma)N_0}
 \le\frac b{\kappa(b+\sigma)}.
\tag{5}
\]

The transport cost permits laws with infinite first absolute log moment, as in the critical theorem. Under finite first moments it is ordinary W_1.

### Proof

Normalize the weak log-size equation by N(t). Coagulation contributes −bρ plus its upward remainder, fragmentation contributes 2σE[shift]ρ−σρ, and differentiating the normalization contributes −(σ−b)ρ. The result is

\[
 \frac d{dt}\langle\phi,\rho_t\rangle
 =2\sigma\langle\mathbb E[\phi(\cdot+Y)-\phi(\cdot)],\rho_t\rangle
 +\frac\lambda{N(t)}\iint x[\phi(\log(x+y))-\phi(\log x)]n_t(dx)n_t(dy).
\tag{6}
\]

The remainder has total variation at most 2b and mass zero. Its value on an increasing bounded continuous test is nonnegative. Its absolute value on a one-Lipschitz bounded test is at most λH(t)²/N(t), by log(1+r)≤√r. Equation (3) makes that bound integrable over the entire time axis, even when the unnormalized half moment increases.

The bounded-test Duhamel identity for the Poisson semigroup, the monotone-quantile coupling, and increasing clips from the critical proof apply without further changes. They give exact cost ∫a(s)ds. Integrating (3) gives (4)–(5). ∎

At σ=b, C_0=H_0²/(2κmN_0), recovering the earlier theorem. No denominator becomes singular at σ=0 because b>0.

## Consequences for scaling limits

If σ>0 and E(Y²)<∞, set μ=EY and ν_2=E(Y²). Without any initial log-moment assumption,

\[
 \frac{Z_t-2\sigma\mu t}{\sqrt t}
 \Longrightarrow\mathcal N(0,2\sigma\nu_2).
\tag{7}
\]

With E|Z_0|<∞ this convergence holds in ordinary W_1. More generally, any weak limit of the comparison law under a deterministic centering and a scale tending to infinity transfers to the nonlinear law, since the scaled displacement is bounded in mean by C_0 divided by that scale.

The number-weighted log-size drift depends on σ and the daughter law, while the coagulation coefficient affects the bounded correction. This does not mean coagulation is negligible in raw-size mass observables. Its effect can be carried by a very small number of very large particles.

For equal splitting, the typical number log size has drift −2σ log2 and Gaussian variance rate 2σ(log2)². The count separately grows or decays at rate σ−b. These statements include the critical, subcritical-count, and supercritical-count regimes of the same additive model.

## Pure additive coagulation as a consistency check

When σ=0, the comparison law is just ρ_0 and the normalized equation consists only of the upward remainder. Therefore ρ_t is stochastically increasing in t. For s≤t, the same clipped-test argument gives

\[
 W_1(\rho_s,\rho_t)=\int_s^t a(r)\,dr
 \le C_0e^{-\kappa bs}.
\]

Use a common uniform variable in the quantile representations. Its quantiles increase in t, and their total expected increase from time zero is at most C_0. The limit is finite almost surely and defines a proper limiting log-size law ρ_infinity. Monotone convergence gives

\[
 W_1(\rho_t,\rho_\infty)\le C_0e^{-\kappa bt}.
\]

This is consistent with the known normalized additive-coagulation limits, including a heavy raw-size tail and diverging arithmetic mean. It is not presented as a newly discovered pure-coagulation phenomenon; the novelty question is the general nonlinear coupling certificate and its common derivation across σ.

## Assumptions that remain necessary

Mass-conserving global weak solutions are assumed. The selection rate is constant, and the daughter fraction measure is independent of parent size. The proof does not cover arbitrary changes of these coefficients. Finite count and mass suffice for the moment-free transport result; log-moment assumptions are added only for the particular means or ordinary W_1 conclusions that need them. The pure-fragmentation limits and semigroup tools require attribution; none of the scaling limits should be described as pointwise convergence to a lognormal density.
