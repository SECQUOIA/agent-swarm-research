# When lateral mobility fails to regularize kinetic trapping

Research note, 2026-09-06. Derived independently from the model in [exploration-interfaces.md](exploration-interfaces.md). The separate reviewer validated the finiteness criterion, the natural domain conventions, the local gamma coefficients, compact-wall localization, and the quadratic-mobility finite-bulk bound; see [review-degenerate-mobility.md](review-degenerate-mobility.md). A compact-wall localization proof and a global numerical convergence check are included. Literature novelty remains unresolved.

## Model and interpretation of a degenerate operator

Use the constant-affinity bulk–surface exchange model in the interface note, replacing constant surface diffusivity by `D(s)`. The reversible surface generator must be `(D f′)′`, not `D f″`, to preserve uniform surface equilibrium. The relevant surface operator and extended inverse functional are

\[
H=-\partial_s[D(s)\partial_s]+k(s),\qquad
J=\lim_{z\downarrow0}\langle1,(H+z)^{-1}1\rangle.
\tag{1}
\]

In the well-mixed reduced model, the flow dispersion is exactly `D_flow=(KV²/Z)J`, with the notation of the interface note. We use the limit definition because `H` need not have a spectral gap or an `L²` inverse. The equality is interpreted through the reversible Green–Kubo or energy formula. With finite transverse bulk diffusion, a nonnegative Schur-complement remainder is added. Thus `J=∞` still implies infinite full-bulk dispersion when `V≠0`, but transferring a finite asymptotic coefficient to finite bulk requires a separate bound on that remainder. The final section supplies that bound for quadratic mobility and quadratic exchange zeros; other degenerate exponents require a separate argument.

Take a compact periodic wall, a finite number of isolated zeros, and assume `k,D` are positive and bounded away from zero outside fixed neighborhoods of these points. Near a particular zero at `s=0`, suppose

\[
k(s)\asymp a|s|^m,\qquad D(s)\asymp e|s|^n,
\quad a,e>0,\quad m,n\ge0.
\tag{2}
\]

Here `e=εb` in the small-mobility notation. For local asymptotic coefficients, replace comparability by `k(s)=δ+a|s|^m[1+o(1)]` and `D(s)=e|s|^n[1+o(1)]`, with regularity and uniform remainders sufficient for localization. Comparability alone proves thresholds, not precise constants.

Define the self-adjoint realization by the closed quadratic form

\[
Q[f]=\int[D|f'|^2+k|f|^2]ds
\]

obtained as the closure of smooth periodic functions in the norm `Q[f]+||f||²`. No absorbing boundary condition or extra killing is imposed at a zero. This is the natural conservative diffusion form before adding `k`.

For `n<1`, a finite-energy function retains a common trace across the zero because `∫D^{-1}ds` is finite. For `n≥1`, the point has zero energy capacity for lateral diffusion: `∫D^{-1}ds` diverges, so a jump can be approximated at arbitrarily small diffusion cost. The form does not impose communication across the zero. Bulk adsorption/desorption can still connect the surface regions. Initial atoms at the exact zero are outside the absolutely continuous stationary class and require separately specified point-state behavior. The stationary measure discussed here gives such points zero mass.

## Exact criterion for finite dispersion

The energy dual characterization is

\[
J=\sup_f\left\{2\int f\,ds-Q[f]\right\}.
\tag{3}
\]

Equivalently, `J<∞` if and only if the integral functional is bounded in the energy norm: `(∫f)²≤C Q[f]`. Under (2), a zero contributes a finite `J` exactly when

\[
\boxed{m<1\quad\hbox{or}\quad n<3.}\tag{4}
\]

Thus for a smooth quadratic kinetic zero, `m=2`, any fixed positive mobility prefactor regularizes `J` if `n<3`; it fails for `n≥3`. This is also the reduced-model flow-dispersion threshold when `V≠0`. Zero mean velocity removes this particular kinetic contribution.

For smooth nonnegative mobility profiles, the usual isolated zero is quadratic (`n=2`) and still regularizes the dispersion, but with a different singular scaling. A quartic zero (`n=4`) does not regularize it at any positive prefactor. Thus “surface diffusivity is nonzero almost everywhere” is insufficient to conclude that a finite Taylor coefficient exists. When `D` and `k` share a quadratic spatial factor, the `n=2` case is directly applicable. The floor `δ` in the crossover below is an independently added exchange pathway; assuming that it simultaneously adds a floor to `D` would define a different crossover problem.

### Finiteness

If `m<1`, Cauchy–Schwarz gives `(∫f)²≤(∫k^{-1})∫kf²` near the zero. Away from the zeros, the potential controls the integral normally.

For `n<3`, choose a fixed point `r>0` in a nondegenerate annulus. On the positive half-neighborhood, integration by parts gives

\[
\int_0^r f(s)ds=r f(r)-\int_0^r s f'(s)ds.
\]

Therefore

\[
\left|\int_0^r[f(s)-f(r)]ds\right|^2
\le\left(\int_0^r\frac{s^2}{D(s)}ds\right)
\int_0^r D(s)|f'(s)|^2ds.
\tag{5}
\]

The first factor is finite exactly for `n<3`. The anchored value `f(r)` is controlled by the standard one-dimensional trace estimate on the annulus, where `D,k` are positive. Apply this estimate to both sides and every zero, then pass from smooth functions to the form closure. This proves `J<∞`.

### Divergence

For `m>1,n>3`, take a smooth nonnegative bump of height one supported at distances comparable to `ρ` from zero, with width comparable to `ρ`. Its integral is of order `ρ`, while its energy is at most `C(eρ^{n−1}+aρ^{m+1})`. Optimizing its scalar amplitude gives

\[
J\ge c\frac{\rho^2}{e\rho^{n-1}+a\rho^{m+1}}\to\infty.
\tag{6}
\]

For the borderline `n=3,m≥1`, use a smooth cutoff approximation to `f(s)=1/s` on `[ρ,r]`. Then `∫f∼log(r/ρ)`, the derivative energy is `O(e log(r/ρ))`, and the reaction energy is bounded for `m>1` or `O(a log(r/ρ))` for `m=1`. The ratio `(∫f)²/Q[f]` diverges. Endpoint cutoff contributions are at most of the same or smaller order. If `m=1,n>3`, the same `1/s` test has bounded derivative energy and logarithmic potential energy; it also diverges. These tests can be supported on one side of the zero and do not rely on choosing a transmission condition there.

## Small mobility scaling for a quadratic zero

For `m>1,n<3` and a pure local power law, balance diffusion and reaction with

\[
\ell=(e/a)^{1/(m+2-n)},\qquad \lambda=a\ell^m.
\]

The predicted leading singular integral is

\[
J\sim e^{-(m-1)/(m+2-n)}a^{-(3-n)/(m+2-n)}C_{m,n}(\delta/\lambda),
\tag{7}
\]

where

\[
C_{m,n}(z)=\left\langle1,
[-\partial_x|x|^n\partial_x+|x|^m+z]^{-1}1
\right\rangle_{\mathbb R}.
\]

The inverse is an extended energy inverse when needed. It is finite near zero by (4) and at infinity because `m>1`. Formula (7) is exact for the whole-line power-law model. The appended localization proof transfers it to a compact wall under precise coefficient assumptions, with independent review completed. Multiple isolated defects contribute additively if their local layers remain separated.

For `m=2`, the zero-floor scaling is

\[
J\asymp e^{-1/(4-n)}a^{-(3-n)/(4-n)},\qquad n<3.
\]

For `2<n<3`, the local zero-floor Poisson solution is expected to obey

\[
h(s)\sim\frac{s^{2-n}}{e(n-2)}\quad(s\downarrow0).
\tag{8}
\]

This follows from the natural zero-flux integration of `−(e s^n h′)′≈1`. Reaction is lower order here because `m+2−n>0`. The integral remains finite for `n<3`, but `h` fails to belong to `L²` when `n≥5/2`. Thus requiring an `L²` Poisson solution would give an incorrectly restrictive dispersion criterion. A finite reversible Green–Kubo integral requires the energy condition, not an `L²` corrector.

## Exact quadratic-mobility crossover

Set `m=n=2`. Then `ℓ=√(e/a)`, `λ=e`, and `ζ=δ/e`. The local whole-line problem reduces to

\[
[-\partial_x x^2\partial_x+x^2+\zeta]h=1.
\]

The two half-lines decouple in the natural form and contribute equally. On `x>0`, put `y=xh`. Direct differentiation yields

\[
\left[-\frac{d^2}{dx^2}+1+\frac\zeta{x^2}\right]y=\frac1x,
\qquad \int_0^\infty h\,dx=\int_0^\infty\frac{y(x)}x\,dx.
\tag{9}
\]

The energy transformation follows by expanding `(y′−y/x)²`; its cross term cancels the `y²/x²` term after integration by parts. It selects the Friedrichs realization of the inverse-square Schrödinger operator. The forcing `1/x` is interpreted in the corresponding energy dual, using cutoff limits.

Write `ν=√(1/4+ζ)`. The normalized generalized eigenfunctions of `−d²/dx²+ζ/x²` are `√(κx)J_ν(κx)`, with eigenvalue `κ²`. Their transform of the forcing is independent of `κ`:

\[
F_\nu=\int_0^\infty t^{-1/2}J_\nu(t)dt
=2^{-1/2}\frac{\Gamma(\nu/2+1/4)}{\Gamma(\nu/2+3/4)}.
\]

The Bessel Mellin integral is standard; see [NIST DLMF §10.22, Eq. 10.22.43](https://dlmf.nist.gov/10.22.E43). Spectral Parseval and `∫_0^∞(1+κ²)^{-1}dκ=π/2` give the full-line coefficient

\[
\boxed{C_{2,2}(\zeta)=\frac\pi2
\left[\frac{\Gamma(\nu/2+1/4)}{\Gamma(\nu/2+3/4)}\right]^2,
\quad \nu=\sqrt{\tfrac14+\zeta}.}\tag{10}
\]

Consequently the candidate compact-wall asymptotic is

\[
\boxed{J\sim\frac1{\sqrt{ae}}C_{2,2}(\delta/e).}\tag{11}
\]

At zero floor, `C₂,₂(0)=π²/2=4.934802200544679…`. At a large scaled floor, `C₂,₂(ζ)∼π/√ζ`, recovering `π/√(aδ)`. The crossover floor is now `δ∼e`, compared with `δ∼√(aD_s)` for nondegenerate mobility. The large-ζ match requires `δ→0` when interpreting a local approximation to a fixed global rate profile.

As an elementary check at `ζ=0`, the half-line solution of (9) is

\[
y(x)=e^{-x}\int_0^x\frac{\sinh t}{t}dt
+\sinh x\int_x^\infty\frac{e^{-t}}t dt.
\]

Numerically integrating `2∫_0^{100} y(x)/x dx` gives `4.914800866257112`; adding the leading tail `2/100` gives `4.934800866257112`, consistent with (10), with the remaining error of order `100^{-3}`. This independently checks the coefficient against a real-space Green function, but is not a proof of global-profile localization.

## Literature boundary and remaining work

Surface diffusion in Taylor dispersion is established: [Dill and Brenner, *A general theory of Taylor dispersion phenomena: III. Surface transport* (1982)](https://doi.org/10.1016/0021-9797(82)90239-9), and [Levesque et al., *Taylor Dispersion with Adsorption and Desorption* (2012)](https://arxiv.org/abs/1211.5224). Neither general framework is new here.

Weighted Hardy inequalities and domain questions for degenerate diffusion are established mathematical subjects; [Robinson, *The weighted Hardy constant* (2021)](https://arxiv.org/abs/2103.07848) is a relevant primary source. The elementary criterion (4) is best presented as a transport application of weighted energy duality, not as the discovery of weighted Hardy theory.

The later literature audit found a direct route to (10) through a known Brownian exponential-functional identity. Thus the local gamma formula should be treated as an explicit transport corollary, not an independently novel special-function result. Independent review has validated the coefficient, and the appended sections provide compact-wall localization and a smooth global-profile numerical check. The broader transport novelty audit remains open. The appended general zero-floor coefficient and quadratic-mobility finite-bulk bound have passed independent review.

Specifically, let `A_u^(μ)=∫_0^u exp[2(B_v+μv)]dv`. The geometric Brownian representation of the quadratic-mobility diffusion gives

\[
C_{2,2}(\zeta)=\sqrt{\pi/2}\int_0^\infty
e^{-\zeta u/2}\mathbb E[(A_u^{(1/2)})^{-1/2}]du.
\]

[Matsumoto and Yor (2005), Theorem 4.12, PDF page 15](https://www.emis.de/ft/46813) gives `A_T^(μ)` at an independent exponential time as a beta variable divided by twice an independent gamma variable. Taking its negative half moment with exponential rate `ζ/2` and drift `μ=1/2` recovers (10). This provides an additional independent derivation and materially narrows the novelty claim. The compact-wall constant-affinity transport interpretation, domain threshold, and finite-bulk implications need assessment as a combined contribution.

## Compact-wall localization proof

This proof was added after the initial note, using an independently proposed partition argument from the reviewer. Assume `D_e(s)=e d_0(s)` with `d_0(s)/|s|^n→1` at the unique zero, `k_δ(s)=δ+k_0(s)` with `k_0(s)/(a|s|^m)→1`, and `m>1,n<3`. On closed sets away from zero, `d_0,k_0` have positive lower bounds. The coefficients are fixed as `e→0`, except for the displayed factors and floor. Then (7) holds, uniformly when `δ/λ` stays in a fixed compact subset of `[0,∞)`.

Choose nonnegative smooth functions `χ,ξ` with `χ²+ξ²=1`, with `χ=1` close to zero and supported inside `|s|<r`, and `ξ` vanishing in a smaller neighborhood. The transition annulus stays away from zero. Direct expansion gives the partition identity

\[
Q[u]=Q[\chi u]+Q[\xi u]
-\int D_e(\chi'^2+\xi'^2)u^2ds.
\]

On the transition annulus `k_0≥c_r>0` and `D_e≤C_r e`, so

\[
Q[u]\ge(1-C_r e)\{Q[\chi u]+Q[\xi u]\}.
\tag{12}
\]

The source decomposes exactly as `∫u=∫χ(χu)+∫ξ(ξu)`. Relaxing the compatibility between `χu` and `ξu` therefore gives

\[
J\le(1-C_r e)^{-1}(J_{\rm inner}[\chi]+J_{\rm outer}[\xi]),
\tag{13}
\]

where the two functionals use their respective localized energy domains. The outer term is bounded uniformly by `∫ξ²/k_0 ds=O_r(1)`.

Given `η>0`, choose `r` small enough that both local coefficient ratios lie between `1−η` and `1+η`. Inner test functions extend by zero to the whole line; their energy is at least

\[
(1-\eta)\int(e|s|^n|f'|^2+a|s|^m f^2)ds
+\delta\int f^2ds.
\]

Because `0≤χ≤1`, replacing `f` by `|f|` and then the source `χ` by 1 can only increase the variational supremum. Rescaling `s=ℓx` therefore bounds the inner term by

\[
J_{\rm inner}[\chi]\le\frac{\ell/\lambda}{1-\eta}
C_{m,n}\!\left(\frac\zeta{1-\eta}\right).
\tag{14}
\]

Since `ℓ/λ→∞` for `m>1`, the outer `O_r(1)` term vanishes after scaling, and (13)–(14) give the upper limit. For the lower limit, insert any compactly supported whole-line test function, rescaled by `s=ℓx`, into the global variational problem. The coefficient ratios converge locally to one; optimizing over the whole-line form core yields `liminf J/(ℓ/λ)≥C_m,n(ζ)`. This uses only the energy completion and does not require an `L²` inverse.

Finally let `η→0`. Continuity of the finite integral-dual resolvent at `ζ=0` follows from monotone spectral convergence, and on `ζ>0` from the resolvent identity. For any sequence of scaled floors in a compact interval, take a convergent subsequence and apply the same upper and lower arguments; this proves uniformity on that interval. Thus the whole-line coefficient in (7), including the explicit gamma coefficient (10), transfers to the stated compact-wall setting. The argument does not claim uniformity for arbitrarily large `δ/λ`.

## Global-profile numerical check with mesh refinement

Take a circle `−π≤s<π`, `k_0(s)=d_0(s)=4 sin²(s/2)`, `D_e=e d_0`, and `δ=eζ`. Then `a=1`. Symmetry reduces the problem to `0<s<π` with zero flux at `π` and the natural endpoint at zero. In logarithmic coordinate `t=log s`, multiply the equation by `s`:

\[
-\partial_t[p(t)\partial_t h]+w(t)h=s,
\quad p=e d_0(s)/s,\quad w=s(e\zeta+k_0(s)).
\]

A conservative centered finite-volume solve used cell-centered uniform `t` points between `log√e−24` and `logπ`, exact midpoint reaction/source coefficients, face values of `p`, and zero face flux at both truncated endpoints. The integral was evaluated as `J=2Σs_j h_j Δt`. The logarithmic lower truncation lies more than ten orders of magnitude below the inner scale.

| e | ζ | √e J, 12,000 cells | √e J, 24,000 cells | Exact limiting coefficient |
| ---: | ---: | ---: | ---: | ---: |
| 10⁻² | 0 | 4.940982260 | 4.940982282 | 4.934802201 |
| 10⁻⁴ | 0 | 4.934863879 | 4.934863882 | 4.934802201 |
| 10⁻⁶ | 0 | 4.934802813 | 4.934802814 | 4.934802201 |
| 10⁻² | 1 | 2.605936991 | 2.605936992 | 2.605941085 |
| 10⁻⁴ | 1 | 2.605941117 | 2.605941093 | 2.605941085 |
| 10⁻⁶ | 1 | 2.605941126 | 2.605941095 | 2.605941085 |
| 10⁻² | 10 | 0.959243857 | 0.959243879 | 0.969989917 |
| 10⁻⁴ | 10 | 0.969880810 | 0.969880810 | 0.969989917 |
| 10⁻⁶ | 10 | 0.969988830 | 0.969988827 | 0.969989917 |

The mesh differences are small compared with the finite-`e` discrepancy, except where that discrepancy is already near numerical accuracy. This supports the predicted coefficient, scaling, and finite-floor crossover for a smooth compact-wall example. It does not independently test the full bulk–surface stochastic process or its time-dependent covariance.

## General zero-floor coefficient

The zero-floor coefficient in (7) also admits a candidate closed form for every `m>1` and `0≤n<3`. Define

\[
d=m+2-n,\quad r=\frac{m-1}{d}\in(0,1),\quad q=d/2,
\quad\beta=-\frac12-r,\quad \nu=\frac{n-1}{d}.
\]

Then

\[
\boxed{C_{m,n}(0)=
2\pi d^{-1-2r}\csc(\pi r)
\left[\frac{\Gamma(1/d)}{\Gamma(m/d)}\right]^2.}\tag{15}
\]

Positivity is explicit because `0<r<1`. Equivalently `−3/2<β<−1/2`; this range is equivalent to `m>1,n<3`, matching the separate energy criterion. The expression is algebraically identical to `−2π d^(2β)[Γ(1/d)/Γ(m/d)]²/cos(πβ)` used in the derivation below.

For a derivation on `x>0`, let `t=x^q/q` and set `p=(m+n)/d`. The homogeneous solutions of the original operator are

\[
u(x)=x^{(1-n)/2}I_\nu(t),\qquad
v(x)=x^{(1-n)/2}K_\nu(t).
\]

The order `ν` is signed. The first solution has the natural no-flux branch at zero; the second decays at infinity. Their weighted Wronskian is `x^n(uv′−u′v)=−q`. Thus the positive Green function is

\[
G(x,y)=q^{-1}(xy)^{(1-n)/2}
I_\nu(t_{\min})K_\nu(t_{\max}).
\tag{16}
\]

Under the change `Y=(qt)^{p/2}h`, the resulting Green bilinear form becomes that of `−d²/dt²+1+(ν²−1/4)/t²`, with source `q^β t^β`. Its normalized Bessel modes are `√(κt)J_ν(κt)`. For `n≥1`, this is the usual Friedrichs branch (including the no-logarithm branch at `n=1`). For `n<1`, it is the scale-invariant branch with exponent `1/2+ν<1/2`; this is not the Friedrichs extension. One must use the original Green function or this specified Bessel realization. A naive integration-by-parts transformation of the energy would drop a nonvanishing, possibly divergent boundary term when `n<1`.

The source transform is

\[
\int_0^\infty\sqrt{\kappa t}J_\nu(\kappa t)t^\beta dt
=\kappa^{-\beta-1}2^{\beta+1/2}
\frac{\Gamma(1/d)}{\Gamma(m/d)}.
\]

The standard Bessel Mellin formula is applicable because `ν>−1/2`, its integrand is integrable at zero, and its oscillatory integral converges at infinity. Finally,

\[
\int_0^\infty\frac{\kappa^{-2\beta-2}}{1+\kappa^2}d\kappa
=-\frac\pi{2\cos(\pi\beta)}.
\]

Multiplying by `q^{2β}`, the squared source-transform coefficient, and the factor two for both half-lines proves (15), provided the stated Bessel resolution is used. For `n<1`, the global source is even and the natural full-line solution restricts to the same no-flux half-line branch.

Checks: `(m,n)=(2,0)` reduces to the previously derived harmonic-oscillator constant `4.6474760094`; `(2,2)` gives `π²/2`; as `n→3−` with `m=2`, (15) diverges as `2/(3−n)`, consistent with the local `1/s` threshold.

A separate logarithmic-coordinate finite-volume solve of the pure power-law problem, with 50,000 cells on `−40<log x<log120` and a leading outer tail correction, gave:

| m | n | Numeric full-line integral | Formula (15) |
| ---: | ---: | ---: | ---: |
| 2 | 1 | 4.550505757 | 4.550505679 |
| 2 | 1.5 | 4.608819978 | 4.608819809 |
| 2 | 2.5 | 6.477405351 | 6.477383734 |
| 3 | 1 | 3.437593024 | 3.437592909 |
| 3 | 2 | 4.011361582 | 4.011361552 |
| 4 | 2.5 | 5.475172771 | 5.475172885 |

These checks support the formula but do not establish literature novelty. Independent review confirmed the signed-order Bessel realization for `n<1` and checked six additional cases against converged original-coordinate boundary-value solves; see the review note.

## Finite bulk correction for quadratic mobility

The finite-bulk qualification at the start can be closed for `m=n=2` using a logarithmic supersolution. Assume `d_0,k_0` are fixed `C²` profiles with finitely many isolated quadratic zeros at the same positions, positive elsewhere. Near each zero,

\[
d_0(s)=b s^2+o(s^2),\quad d_0'(s)=2bs+o(s),
\quad k_0(s)=a s^2+o(s^2),\qquad a,b>0.
\]

Let `D_e=e d_0`, `k_δ=δ+k_0`, and `h_δ=H_δ^{-1}1`. We will show a uniform bound on `k_δh_δ` for small `e>0` and every `δ≥0`.

For the exact local coefficients, use

\[
Q(s)=\frac1{2eb}\log\!\left(1+\frac{eb}{a s^2}\right).
\]

Writing `z=a s²/(eb)`, direct differentiation gives

\[
[-\partial_s(ebs^2\partial_s)+as^2]Q
=\frac{1-z}{(1+z)^2}+\frac z2\log(1+1/z).
\tag{17}
\]

Since `log(1+1/z)≥2/(2z+1)`, the right side is at least

\[
\frac{z^3+2z+1}{(1+z)^2(2z+1)}\ge\frac15.
\]

For the last inequality, five times the numerator minus the denominator is `3z³−5z²+6z+4`, whose derivative `9z²−10z+6` is positive. Also `as²Q≤1/2`, `|ebs Q′|≤1`, and `|ebs²Q″|≤9/8`. Consequently small relative errors in the two coefficients and in `d_0′` preserve a strictly positive lower bound in (17), uniformly in `e`, throughout a sufficiently small fixed neighborhood.

Choose a fixed nonnegative cutoff `χ` equal to one near zero and supported inside that neighborhood. In its transition annulus, `Q,Q′,Q″` are bounded uniformly in `e`, while `k_0` has a positive lower bound. Adding a sufficiently large constant `M`, independent of `e`, gives a global positive supersolution

\[
H_0(M+\chi Q)\ge c>0.
\]

For finitely many separated zeros, sum the corresponding localized functions. Near a zero, `D_e Q′=O(s)` tends to zero; hence the logarithm creates no point flux or delta term in the weak formulation. Both `Q` and its energy are locally integrable, and the comparison is valid in the natural form domain. Positivity then yields

\[
h_0\le c^{-1}(M+\chi Q),\qquad
\|k_0h_0\|_\infty\le C.
\]

For a positive floor, comparison gives `0≤h_δ≤h_0` and `δh_δ≤1`; therefore

\[
\boxed{\|k_\delta h_\delta\|_\infty\le1+C}
\tag{18}
\]

uniformly in small `e` and all `δ≥0`.

The exact finite-bulk Schur-complement identity in the interface note now applies with this variable-mobility operator. Its nonnegative boundary form follows by minimizing `∫D_e|w′|²+∫k_δ(w-f_Γ)²`; it annihilates constants. In addition `∫k_δh_δ=P` by integration of the natural zero-flux equation. For fixed positive transverse bulk diffusivity, the bulk trace and Poincaré inequalities bound the residual linear functional using (18). Maximizing the resulting quadratic bound proves

\[
\boxed{D_{\rm flow}=\frac{KV^2}{Z}J+O(1)}
\tag{19}
\]

uniformly for small `e`, with all other bulk geometry and velocity data fixed. Thus the compact-wall quadratic-mobility gamma crossover transfers unchanged to finite transverse bulk diffusion. The proof is not uniform as bulk diffusivity tends to zero, does not prove an analogous bounded remainder for all `n<3`, and does not by itself supply time-dependent anomalous prefactors. Independent review confirmed the supersolution, weak-domain conditions, comparison bounds, and bulk remainder estimate.
