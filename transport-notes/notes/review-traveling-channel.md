# Independent review: traveling-channel dispersion

Date: 2026-09-06. Scope: independent mathematical review of the candidate in `exploration-soft.md`. This review validates the stated reduced-model theorem and supplies a simpler explicit representation. It does **not** establish literature novelty or exactness for the full moving-wall fluid problem.

## Verdict and qualifications

For a smooth, strictly positive periodic area and constant molecular diffusivity, the zero-throughput traveling-wave model has zero laboratory drift. Its longitudinal effective diffusivity is even in wave speed, strictly increasing in squared speed for every nonconstant area, and interpolates between the stated harmonic-area and cubic-area expressions. There is exactly one positive speed at which it equals the molecular diffusivity.

The potentially misleading statement “the transformed drift is −v” needs its convention stated: −v is the divergence-form advective velocity and the stationary mean velocity. The Itô drift is `d_s−v`. Omitting `d_s` from the backward generator would change the invariant law and invalidate the theorem. The current candidate note correctly includes this term.

The upper endpoint concerns the one-dimensional model. It is not an unrestricted high-frequency theorem for a real channel with transverse shear. Zero mean flux is also distinct from zero imposed pressure drop.

## Independent derivation of the coordinate change

Write `y=x−vt`, `a(y)=A(y)/Ā`, and assume

\[
q=v(A-\bar A),\qquad
(Ac)_t+\partial_x(qc-DAc_x)=0.
\]

In moving coordinates, the balance becomes

\[
\partial_t(Ac)=\partial_y(v\bar A c+DAc_y).
\]

Define

\[
s=S(y)=\int_0^y a(z)\,dz,\qquad S(y+L)=S(y)+L.
\]

The probability density with respect to `ds` is proportional to `Āc`, since `A dy=Ā ds`. Its equation is

\[
\rho_t=v\rho_s+(d\rho_s)_s,
\qquad d(s)=Da(y(s))^2.
\]

The invariant cell density is uniform, and the backward generator is

\[
\mathcal L f=d f_{ss}+(d_s-v)f_s.
\]

Its invariant mean velocity is `−v`. The laboratory coordinate equals `s+vt` plus a bounded periodic function. A bounded coordinate correction does not change the asymptotic drift or diffusivity: its variance is bounded and its covariance with a displacement of variance `O(t)` is `O(√t)`. Thus the laboratory drift is zero and its diffusivity equals that of the lifted `s` process.

## Corrector and energy

Let `χ` be a periodic corrector with arbitrary fixed additive constant. The harmonic-coordinate equation is

\[
\mathcal L(s+\chi)=-v.
\]

With `h=1+χ_s`, this becomes

\[
(dh)_s-vh=-v,\qquad \frac1L\int_0^Lh\,ds=1.
\tag{R1}
\]

The effective diffusivity is

\[
\mathcal D(v)=\frac1L\int_0^L d h^2\,ds.
\tag{R2}
\]

The usual corrector energy identity gives

\[
\mathcal D(v)=\langle d\rangle_s-\langle d\chi_s^2\rangle_s.
\]

At zero speed, `dh` is constant and (R1) gives

\[
\mathcal D(0)=\left\langle\frac1d\right\rangle_s^{-1}.
\]

## Explicit Fourier representation

The abstract spectral proof in the candidate is valid, but the one-dimensional problem permits a more explicit calculation.

Introduce a resistance coordinate with period `T_r`:

\[
r(s)=\int_0^s\frac{du}{d(u)},\qquad
T_r=\int_0^L\frac{du}{d(u)}.
\]

Here `r` and `T_r` have units of time divided by length; `T_r` is not the physical oscillation period. Put

\[
f(r)=d(s(r)),\quad
f_n=\frac1{T_r}\int_0^{T_r}f(r)e^{-2\pi inr/T_r}\,dr,
\quad \omega_n=\frac{2\pi n}{T_r}.
\]

Because `ds=f dr`, the mean coefficient is

\[
f_0=L/T_r=\mathcal D(0).
\]

Set `g=dh`. Multiplying (R1) by `d` transforms it to

\[
g_r-vg=-vf.
\]

For nonzero speed its unique periodic solution has coefficients

\[
g_n=\frac{v}{v-i\omega_n}f_n.
\]

For the zero mode this ratio is one. Formula (R2) and Parseval's identity therefore give the exact result

\[
\boxed{
\mathcal D(v)=\frac{L}{T_r}
+\frac{T_r}{L}\sum_{n\ne0}|f_n|^2
\frac{v^2}{v^2+\omega_n^2}.
}
\tag{R3}
\]

At zero speed, use the displayed continuous extension. This is an explicit positive sum; there is no eigenvalue problem left to solve. In particular, no assumption of reflection symmetry or small area variation entered the derivation.

## Consequences and strictness

Parseval also gives

\[
\frac{T_r}{L}\sum_n|f_n|^2
=\frac1L\int_0^L d(s)\,ds.
\]

Every nonzero-frequency summand in (R3) is strictly increasing in `v²`. For nonconstant area, at least one such summand is present. Consequently

\[
\mathcal D(0)<\mathcal D(v)<\mathcal D(\infty)
\quad (0<|v|<\infty),
\]

with

\[
\mathcal D(0)=\frac{D}{\bar A\langle A^{-1}\rangle_x},
\qquad
\mathcal D(\infty)=\frac{D\langle A^3\rangle_x}{\bar A^3}.
\]

Dominated convergence applies because `Σ|f_n|²` is finite. This proves the large-speed limit even without a smooth asymptotic expansion.

For `z=v²`, all derivatives of positive order have alternating signs:

\[
(-1)^{m+1}\frac{d^m\mathcal D(\sqrt z)}{dz^m}>0,
\qquad m\ge1,
\]

for a nonconstant profile. In particular the response is strictly increasing and strictly concave in squared speed. Differentiation at zero is legitimate since the nonzero frequencies are bounded away from zero.

Strict Jensen inequalities place the endpoints on opposite sides of `D`. Continuity and strict monotonicity give exactly one positive crossing. A constant area is the necessary exception: then `q=0` and `𝒟(v)=D` for every speed.

For sufficiently smooth `d`, (R3) further yields

\[
\mathcal D(\infty)-\mathcal D(v)
=\frac{\langle d(d_s)^2\rangle_s}{v^2}
+o(v^{-2}).
\]

The coefficient follows from `f_r=d d_s` and Parseval. In the original area coordinate it is `4D³⟨a³(a_y)²⟩_y`. The limit and this correction have different regularity requirements; the correction must not be asserted for a discontinuous profile.

## Independent numerical check

I solved (R1) directly as the periodic boundary-value problem

\[
g_s=(v/d)g-v,\qquad g(0)=g(1),
\]

using SciPy collocation with tolerance `10⁻¹⁰`, and independently evaluated (R3) using a 32,768-point Fourier grid in the resistance coordinate. The deliberately asymmetric test profile was

\[
d(s)=1+0.65\cos(2\pi s)+0.15\sin(4\pi s),\quad L=1.
\]

Its harmonic and arithmetic means are approximately `0.732979404237` and `1`, respectively.

| Speed | Direct boundary-value result | Fourier result |
|---:|---:|---:|
| 0.1 | 0.733090253095 | 0.733090255072 |
| 1 | 0.743583493319 | 0.743583495299 |
| 10 | 0.939261960191 | 0.939261962163 |
| 100 | 0.999000320121 | 0.999000321987 |
| −1 | 0.743583493318 | 0.743583495299 |
| −10 | 0.939261960191 | 0.939261962163 |

All collocation solves reported success. Agreement is within `2.0×10⁻⁹`; the small common discrepancy is consistent with the numerical coordinate integration. This checks the sign convention, direction invariance for an asymmetric profile, and the endpoint trend. It supplements the proof rather than establishing it.

## Limits of the claim and possible follow-up

- The prescribed `q=v(A−Ā)` follows from continuity plus zero spatial mean flux. A traveling channel with zero imposed pressure drop generally has a different integration constant and need not fall under this theorem.
- Constant `D` and local Fickian closure are substantive assumptions. Transverse equilibration, shear dispersion, and moving-wall hydrodynamics must be checked before making quantitative experimental predictions. A speed-dependent or position-dependent closure coefficient requires a new analysis; the area-moment formulas cannot simply be retained.
- The mathematical large-speed limit can be approached while preserving the reduced approximation in a suitable joint slender-channel limit. At fixed geometry, arbitrarily increasing speed does not justify the approximation.
- The formula shows that the entire speed-response curve sees only the Fourier powers `|f_n|²` in the resistance coordinate. This suggests nonuniqueness of shape inference. However, arbitrary phase changes do not automatically produce channels with the same prescribed physical `D` and wavelength: conversion back to physical area imposes an additional square-root moment constraint. Any explicit indistinguishable-shape construction must verify that constraint.

No counterexample to the reduced-model theorem was found. Its practical relevance and novelty remain separate questions for the fluid-model and literature reviews.
