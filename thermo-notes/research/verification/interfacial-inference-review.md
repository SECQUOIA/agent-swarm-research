# Independent review: interface inference in a nonlocal double-parabola model

Reviewer: `capacity_review`. Date: 2026-09-07. Scope: the precise candidate formulas and kernel constructions supplied by `ensemble_scout` and the root agent. No main research note was edited.

**Verdict:** the planar variational tension formula and its factor are correct. Positivity of the kernel gives a monotone global minimizer among planar profiles without requiring a decreasing kernel or a rearrangement theorem. The minimizer generally has a jump, which must be stated. Positive radial kernels with the same mass, second moment, and fourth moment can have different tensions at one common finite well stiffness. The sharp strong-well moment bounds and proposed smoothing construction check mathematically.

This is a deterministic variational-model result. Its Gaussian structure factor is a harmonic/Hessian response, not automatically an exact nonlinear Gibbs correlation. Novelty is not assessed here.

## 1. Model and admissible class

Let `J>=0` be an integrable, even, compactly supported kernel in `R^d`, with mass `J_0>0`. For an interface normal `n`, define its one-dimensional projection

\[
j(z)=\int_{n^\perp}J(zn+y)\,dy.
\]

Then `j` is even and nonnegative, with mass `J_0` and finite first moment. The energy per unit planar area is

\[
\mathcal F[m]=\frac a2\int_{\mathbb R}(|m|-1)^2dx
+\frac14\iint_{\mathbb R^2}j(x-y)[m(x)-m(y)]^2dxdy,
\qquad a>0.
\]

Consider measurable finite-energy profiles with limits `m(-infinity)=-1`, `m(+infinity)=1`. Clipping a profile to `[-1,1]` cannot increase either term. The global minimum discussed below is within this class of one-dimensional planar profiles.

Define `D_op=J_0 I-j*`, with Fourier multiplier

\[
D(k)=J_0-\widehat j(k)=J_0-\widehat J(kn)\ge0.
\]

Positivity and evenness give `0<=D(k)<=2J_0`. Finite second moment gives `D(k)=O(k^2)` near zero.

## 2. Elimination of the continuous field

Use the exact pointwise identity

\[
(|m|-1)^2=\min_{s\in\{-1,1\}}(m-s)^2.
\]

For a fixed binary sign field `s`, minimize

\[
\mathcal F_s[m]=\frac a2\|m-s\|_2^2+\frac12\langle m,D_{\rm op}m\rangle.
\]

The minimizer is

\[
m_s=G*s,
\qquad
G=a(a+D_{\rm op})^{-1}
=\frac a{a+J_0}\sum_{r=0}^\infty
\left(\frac{j*}{a+J_0}\right)^r.
\]

Here `G` is an even probability measure. Its first term is the atom `a/(a+J_0) delta_0`; the remaining terms have nonnegative integrable densities. Its first moment is finite: interpreting the series as a geometric mixture of sums of `j/J_0` increments bounds it by the expected number of increments times their finite mean absolute displacement.

For non-L2 fronts the displayed operator pairings require their difference-form interpretation. One rigorous route is to note that a binary field with the stated pointwise limits is constant outside a finite interval. Then `D_op s` is square integrable, and `m_s-s=-(a+D_op)^(-1)D_op s` belongs to L2. Completing the square in the difference `m-m_s` is legitimate. The reduced energy is

\[
\inf_m\mathcal F_s[m]
=\frac a4\iint G(dz)[s(x+z)-s(x)]^2dx.
\]

Equivalently it is a nonlocal binary perimeter with off-diagonal kernel

\[
K_{\rm eff}=\frac{a^2}{a+J_0}
\sum_{r=1}^\infty\frac{j^{*r}}{(a+J_0)^r}.
\]

The atom in `G` has no contribution to the difference energy, and `K_eff=aG` away from that atom.

## 3. Global planar minimality and profile regularity

For every binary front with these limits,

\[
\int_{\mathbb R}[s(x+z)-s(x)]dx=2z.
\]

The integrand is integrable because `s` agrees with a step outside a finite interval. Since the difference takes values in `{0,2,-2}`,

\[
\int[s(x+z)-s(x)]^2dx
=2\int|s(x+z)-s(x)|dx\ge4|z|.
\]

Therefore every admissible profile has energy at least

\[
\sigma=a\int|z|G(dz)=\int|z|K_{\rm eff}(z)dz.
\]

The binary step `s=sgn(x)` attains the translation inequality for every `z`. Its continuous-field minimizer `m_*=G*sgn` is nondecreasing because its distributional derivative is `2G>=0`. It is odd apart from an irrelevant choice at the origin and has the correct signs on the two half-lines. Consequently the auxiliary binary field is its actual minimizing sign, and `F[m_*]=F_s[m_*]`. This proves global planar minimality, not merely stationarity of a guessed profile.

A material regularity qualification is necessary. For an integrable kernel `j`, the atom in `G` gives

\[
m_*(0+)={a\over a+J_0},\qquad
m_*(0-)=-{a\over a+J_0}.
\]

Thus the minimizer has a jump of size `2a/(a+J_0)`. The functional has no local gradient penalty that would forbid this. If profiles are required to be continuous, the same value is an infimum obtained by smoothing the jump, but the displayed profile does not attain it in that class. The statement concerns integrable kernels; singular limiting kernels can contribute additional zero-displacement atoms and change this jump formula.

## 4. Fourier coefficient and strong-well limit

The reduced Fourier multiplier is `aD/(a+D)`. With the convention `fhat(k)=integral exp(-ikx)f(x)dx`, the step has Fourier amplitude `2/(ik)` away from zero. The zero-frequency singularity is harmless because `D(k)=O(k^2)`. Hence

\[
\boxed{\sigma(a)=\frac{2a}{\pi}\int_0^\infty
\frac{D(k)}{a+D(k)}\frac{dk}{k^2}.}
\]

This matches the real-space perimeter calculation. The integral converges at both zero and infinity. Monotone convergence as `a` increases gives

\[
\sigma_\infty=\int|z|j(z)dz,
\qquad
\frac{a}{a+2J_0}\sigma_\infty
\le\sigma(a)\le\sigma_\infty.
\]

The lower comparison follows pointwise from `D<=2J_0`. A stronger estimate with `J_0` replacing `2J_0` requires an additional Fourier-positivity assumption and must not be used for arbitrary nonnegative radial kernels.

For a radial kernel in three dimensions, let `r` have its normalized radial mass distribution. Uniform angular averaging gives

\[
\widehat J(kn)=J_0\mathbb E\,\operatorname{sinc}(kr),
\qquad
\sigma_\infty=\frac{J_0}{2}\mathbb E r.
\]

## 5. Sharp radial moment bounds and explicit different tensions

Fix support `0<=r<=R`, second moment `mu=E r^2`, and fourth moment `nu=E r^4`, in the nondegenerate feasible range `mu^2<nu<R^2 mu`.

Hölder interpolation gives

\[
\mu\le(\mathbb E r)^{2/3}\nu^{1/3},
\qquad
\mathbb E r\ge\mu^{3/2}/\sqrt\nu.
\]

Equality is attained by radial masses at `r=0` and `r=sqrt(nu/mu)`, with nonzero-radius probability `mu^2/nu`.

For the upper bound, set `t=r^2`, `T=R^2`, and

\[
t_*=(T\mu-\nu)/(T-\mu).
\]

The quadratic polynomial matching `sqrt(t)` and its derivative at `t_*`, and matching `sqrt(t)` at `T`, majorizes `sqrt(t)` on `[0,T]`. Indeed its Hermite interpolation remainder has the sign of `(t-t_*)^2(t-T)` because the third derivative of `sqrt(t)` is positive. Continuity handles `t=0`. Taking expectations yields the sharp upper bound realized by a measure on `{t_*,T}` with the prescribed first two moments of `t`.

For `R=1`, `mu=1/2`, `nu=3/8`, the lower extremizer has probabilities `1/3,2/3` at radii `0,sqrt(3)/2`; the upper extremizer has probabilities `2/3,1/3` at radii `1/2,1`. Their first radial moments are

\[
\mathbb E r_{\rm low}=1/\sqrt3,
\qquad\mathbb E r_{\rm high}=2/3.
\]

Their limiting tensions are `J_0/(2sqrt3)` and `J_0/3`. At the **same finite** stiffness `a=20J_0`, the rigorous comparison already separates them:

\[
\sigma_{\rm low}(20J_0)\le0.288676J_0,
\qquad
\sigma_{\rm high}(20J_0)\ge\frac{10}{33}J_0
\approx0.303030J_0.
\]

Thus finite-stiffness separation is established without relying on an asymptotic-only difference or oscillatory numerical quadrature. Any `a>12.929J_0` suffices by the same comparison.

## 6. Smooth kernels with exact matched moments

The proposed convolution construction is valid. Let `Z_epsilon` be an independent isotropic smooth probability bump supported in a ball of radius `epsilon`, with moments `z_2,z_4`. In three dimensions,

\[
\mathbb E|X+Z|^2=\mathbb E|X|^2+z_2,
\]

\[
\mathbb E|X+Z|^4=\mathbb E|X|^4
+\frac{10}{3}\mathbb E|X|^2z_2+z_4.
\]

Choose base moment targets

\[
\mu_b=\mu-z_2,
\qquad\nu_b=\nu-\frac{10}{3}\mu_bz_2-z_4,
\]

and construct the two respective extremizers on radius `R-epsilon`. For sufficiently small epsilon the targets remain in the strict feasible region. Convolving each radial measure with the same bump produces smooth, radial, nonnegative kernels of support at most `R`, with exactly the same prescribed mass, second moment, and fourth moment.

Both families converge weakly to their respective distinct shell measures. The tension is continuous under this convergence: its spectral integrand is dominated near zero using `D(k)<=J_0 mu k^2/6`, and at large k using `D(k)<=2J_0` and the factor `k^(-2)`. Dominated convergence therefore preserves the finite-a strict gap for sufficiently small smoothing radius.

These kernels are nonnegative, but may vanish on parts of the support ball. If “positive” is intended to mean strictly positive at every interior radius, mix in a common small smooth radial density positive throughout the ball and retune the remaining moment targets. The strict feasibility inequalities and the tension gap are open conditions, so that strengthened construction also works. Nonnegativity is all the variational proof needs.

## 7. Precisely what bulk information is matched

For the same `a,J_0,mu,nu`,

\[
D(k)=J_0\left(\frac{\mu k^2}{6}-\frac{\nu k^4}{120}+O(k^6)\right).
\]

Thus the harmonic bulk covariance

\[
S_{\rm harm}(k)=\frac1{\beta[a+D(k)]}
\]

has the same expansion through order `k^4` for the two kernels. This is finite low-wave-number information. The full functions `S_harm(k)` are different, and complete knowledge of that function determines `D(k)` and hence the tension exactly within this model. A nonidentifiability claim must therefore concern the stated finite collection of bulk summaries, not the entire structure factor.

The model's Hessian expression is a linear-response or harmonic formula. It does not equal the exact Gibbs structure factor of the nonlinear double-parabola theory without further approximation or a separate argument. Also, because `D(k)` remains bounded at large k, a literal continuum Gaussian field has white-noise ultraviolet behavior. A finite-temperature nonlinear Gibbs construction needs a specified cutoff or regularization. The deterministic variational functional and its interface minimization do not require that statistical interpretation.

## 8. Optional finite-band certificate

If `D(k)` is known exactly on `[k_0,K]`, define its contribution to the tension by the same integral. Positivity gives a lower bound. For radial three-dimensional kernels with known `J_0,mu`, the omitted pieces satisfy

\[
0\le\sigma-\sigma_{[k_0,K]}
\le\frac{J_0\mu k_0}{3\pi}
+\frac{4aJ_0}{\pi(a+2J_0)K}.
\]

The low-frequency term uses `D(k)<=J_0 mu k^2/6` and `aD/(a+D)<=D`; the high-frequency term uses `D<=2J_0`. These factors check exactly. The result is a deterministic bound for exact band data. Measurement uncertainty would need to be propagated separately.

## 9. Follow-up: finite-block response and an exponential remainder

The finite-block certificate proposed by the root is correct. Let `H=a+D_op`, let `I_L` denote the indicator of `[0,L]`, and define the deterministic bulk linear susceptibility

\[
\chi_L=\frac1L\langle I_L,H^{-1}I_L\rangle.
\]

Since `H^{-1}=G/a`, convolution and interval overlap give

\[
\chi_L=\frac1{aL}\int(L-|z|)_+G(dz)
=\frac1a\mathbb E_G(1-|Z|/L)_+.
\]

Consequently

\[
\boxed{\sigma_L:=a^2L(1/a-\chi_L)
=a\mathbb E_G\min(|Z|,L)\uparrow\sigma.}
\]

There is no missing factor of two from the two endpoints of the block. This formula follows directly from the interval-overlap identity and the independently checked expression `sigma=a E_G|Z|`.

For a projected interaction supported in `[-R,R]`, the renewal law is a compound geometric sum

\[
Z=X_1+\cdots+X_N,\quad |X_j|\le R,
\quad P(N=n)=(1-p)p^n,
\quad p=\frac{J_0}{a+J_0}.
\]

The empty sum is zero, representing the resolvent atom. For a positive integer `m` and `L=mR`,

\[
\begin{aligned}
0\le\sigma-\sigma_L
&=a\mathbb E(|Z|-mR)_+\\
&\le aR\mathbb E(N-m)_+\\
&=aR\sum_{k=m+1}^\infty p^k
=J_0R p^m.
\end{aligned}
\]

Thus

\[
\boxed{\sigma_{mR}\le\sigma\le
\sigma_{mR}+J_0R\left(\frac{J_0}{a+J_0}\right)^m.}
\]

The response interpretation can be stated entirely within deterministic variational theory. Linearizing about the uniform positive phase gives the positive operator `H`; its response to a small block source is `H^{-1}I_L`. Since `H^{-1}` is positive and has L-infinity operator norm `1/a`, sufficiently small bounded sources preserve the positive branch, on which the local potential is exactly quadratic. No assertion about the exact nonlinear finite-temperature covariance is needed.

This is an exact model-specific certificate for exact response data and known `a,J_0,R`. Uncertainty in `chi_L` propagates with multiplier `a^2L`; the exponentially small theoretical remainder does not eliminate that measurement error. The generic window-covariance overlap identity is established structure, and this review makes no novelty claim for it.

## 10. Finite inclusion identity, checked separately

For a finite-volume measurable region `Omega` in the full spatial dimension, let `s=2 1_Omega-1`, `H=a+D_op`, and `G=aH^{-1}`. Eliminating the continuous field while fixing this binary label gives

\[
\inf_m\mathcal F_s[m]
=\frac a2\langle s,(I-G)s\rangle
=2a\langle1_\Omega,(I-G)1_\Omega\rangle.
\]

The constant-background terms cancel because `G1=1`. Defining

\[
\chi_\Omega=|\Omega|^{-1}
\langle1_\Omega,H^{-1}1_\Omega\rangle,
\]

one obtains exactly

\[
\boxed{E_{\rm relaxed}(\Omega)
=2a^2|\Omega|(1/a-\chi_\Omega).}
\]

For an integrable nonnegative kernel of mass `J_0`, the atom of `G` has mass `a/(a+J_0)`. If `a>J_0`, that mass exceeds one half, so for every binary label field

\[
s(x)(G*s)(x)\ge\frac{a-J_0}{a+J_0}>0
\]

almost everywhere. The relaxed field is consequently sign-compatible, and the identity is also the exact minimum of the original double-parabola functional within the prescribed sign sector. Without that sufficient condition, the algebraic fixed-label relaxation remains valid but may not respect the designated region's signs.

This is a restricted formation-energy identity for a chosen region. It does not identify an optimized droplet shape, a critical nucleus, or a nucleation barrier. No external-field extension was needed for this verification.
