# Independent review: optimal surface mobility

Review date: 2026-09-06. Reviewer: `review_singular_exchange`.

The exact finite-bulk threshold, universal finite-floor constants, and zero-floor weak-flow optimizer in [optimal-surface-mobility.md](optimal-surface-mobility.md) are mathematically consistent. I checked the variational signs, endpoint derivative, convexity, singular threshold coefficient, and optimizer-limit arguments independently. Fresh symbolic integration and high-precision scalar optimization also confirm the proposed constants. Novelty remains unestablished.

The essential qualifications are that surface diffusivity is varied independently of the exchange profile and affinity; the zero-diffusivity corrector has a finite surface derivative at positive floor; and the physical near-onset asymptotic uses an ordered limit or controls the finite-floor shift of the exact threshold.

## Exact decreasing convex flow term

Use the invariant inner product and restrict to centered states. At positive rate floor, the transverse Dirichlet operator at zero surface diffusion, `A0`, is strictly positive. Its form includes bulk gradients and positive wall–bulk exchange. For `D=Ds>=0`,

\[
A(D)=A_0+D S,\qquad
\mathscr D(D)=\langle g,A(D)^{-1}g\rangle_\pi.
\]

The surface-gradient form is

\[
\langle\phi,S\phi\rangle_\pi={K\over Z}\int|h'|^2.
\]

One way to handle the changing form domain at `D=0` is to use the positive spectral measure of `B=A0^-1/2 S A0^-1/2` and `a=A0^-1/2 g`. In quadratic-form notation,

\[
\mathscr D(D)=\int_{[0,\infty)}{d\mu(\lambda)\over1+D\lambda}.
\tag{1}
\]

It follows that `mathscr D` is nonnegative, decreasing, and convex. For `D>0`,

\[
\mathscr D'(D)=-{K\over Z}\int|h_D'|^2,
\qquad
\mathscr D''(D)=2\int {\lambda^2\over(1+D\lambda)^3}\,d\mu(\lambda)\ge0.
\tag{2}
\]

The right derivative at zero is finite precisely when the corresponding first spectral moment is finite. In the present smooth positive-floor setting, the corrector `h0=f0|Gamma-V0/k_delta` belongs to `H1(Gamma)`, so this condition holds and its value is `-M_delta`, with `M_delta` defined in the development note.

If `M_delta>0`, the measure in (1) charges positive `lambda`, making the flow term strictly convex for every positive `D`. If `M_delta=0`, the measure is supported at zero, so the entire flow term is constant in `D`; this is more precise than merely saying its initial slope vanishes.

Since a nonnegative decreasing convex function has derivative tending to zero at infinity, the objective `ps D+epsilon^2 mathscr D(D)` has exactly the claimed behavior: its unique minimizer is zero for `epsilon^2<=ps/M_delta`, and it has a unique positive minimizer above that threshold. At equality, strict convexity still gives the unique zero minimizer. If `M_delta=0`, the unique minimizer is zero for every amplitude because `ps>0`.

The bulk trace in `M_delta` is essential. Replacing `h0` by `-V0/k_delta` requires the well-mixed reduction or a separate argument that the bulk trace is constant.

## Singular threshold coefficient

For one quadratic zero `k0(s0+x)=a x^2+o(x^2)` and `V0!=0`,

\[
\int|(1/k_\delta)'|^2ds
\sim\sqrt a\,\delta^{-5/2}
\int_{\mathbb R}{4y^2\over(1+y^2)^4}dy
={\pi\sqrt a\over4\delta^{5/2}}.
\]

The rate-independent bulk trace derivative contributes a bounded squared norm, and its cross term is bounded by a constant times the square root of the divergent reciprocal-rate derivative norm. Both are lower order. Thus

\[
M_\delta\sim {\pi B_0\sqrt a\over4\delta^{5/2}},
\qquad
\varepsilon_c^2\sim{4p_s\delta^{5/2}\over\pi B_0\sqrt a}.
\tag{3}
\]

For multiple minima, the leading expression for `M_delta` contains the sum of their `sqrt(a_j)` factors. The single universal `G(r)` used in the development note assumes one minimum; unequal curvatures generally produce a sum of differently scaled functions.

## Universal function and its derivatives

The proposed scaling is correct:

\[
r={aD_s\over\delta^2},\quad
\Lambda={\varepsilon^2 B_0\sqrt a\over p_s\delta^{5/2}},\quad
F_\Lambda(r)=r+\Lambda G(r),
\]

\[
G(r)=r^{-1/4}\mathcal C(r^{-1/2})
=\int_{\mathbb R}[-r\partial_y^2+1+y^2]^{-1}1\,dy.
\]

At `r=0`, put `f(y)=1/(1+y^2)`. Direct integration yields

\[
G(0)=\pi,\qquad
G'(0)=-\int|f'|^2=-{\pi\over4},
\qquad
G''(0)=2\int{(f'')^2\over1+y^2}={21\pi\over16}.
\tag{4}
\]

These identities were independently checked with symbolic integration. Although the source `1` is not in `L2(R)`, its potential-weighted version `(1+y^2)^-1/2` is in `L2`; the same positive spectral-measure argument applies. Finiteness of the derivative moments in (4) justifies the second-order expansion at zero without claiming convergence of a full perturbation series.

Strict convexity gives `Lambda_c=4/pi`. For the limiting function,

\[
r^*(\Lambda)\sim{4\over21}\left({\Lambda\pi\over4}-1\right)
\quad\text{as }\Lambda\downarrow4/\pi,
\]

\[
r^*(\Lambda)\sim\left({\Lambda\mathcal C(0)\over4}\right)^{4/5}
\quad\text{as }\Lambda\to\infty.
\tag{5}
\]

The first follows from the derivative expansion in (4). The second can be proved by rescaling the minimization problem and using `G(r)~C(0)r^-1/4`; differentiating an uncontrolled relative asymptotic is unnecessary.

## Why physical minimizers converge

For each fixed `r>0`, the verified surface-exchange asymptotic gives convergence of the normalized finite-profile flow term to `G(r)`. At `r=0`, the exact zero-surface-diffusion formula and `int 1/k_delta~pi/sqrt(a delta)` give the matching limit `G(0)=pi`. The normalized bounded bulk correction is `O(delta^1/2)`.

The normalized flow terms are decreasing in `r`, and `G` is continuous on `[0,R]`. Pointwise convergence of such monotone functions to a continuous limit is uniform on every compact interval, as a finite-grid comparison shows. This handles the endpoint `r=0`, which is outside a statement of the harmonic crossover restricted to bounded `delta/sqrt(Ds)`.

The normalized total objective is at least `r`. Testing `r=0` gives a uniform upper bound on its minimum for fixed `Lambda`, and hence a common compact interval containing all minimizers. Uniform convergence there and uniqueness of the limiting minimizer imply convergence of the physical scaled minimizer for every fixed `Lambda`, including `Lambda=4/pi`.

This proves convergence of optimizer values. It does not give a relative onset law in an arbitrarily shrinking interval around threshold. The expansion in (5) describes the limiting function: for physical systems, one may first send `delta` to zero at fixed `Lambda`, then approach the limiting threshold. A simultaneous limit with `Lambda-4/pi` comparable to the finite-`delta` shift in the exact threshold must keep that shift and control the approximation error.

The zero-floor weak-flow result follows by the same compactness argument after setting `L=(A0 epsilon^2/(4ps))^(4/5)` and rescaling `Ds=Lx`. Nonnegative flow dispersion bounds `x` from above, the singular scalar term excludes `x` tending to zero, and the limit `x+4x^-1/4` has its unique minimum at `x=1`.

## Independent high-precision numerical checks

I evaluated the gamma formula at 50 decimal digits and found minimizers by bisection using its exact digamma derivative. With `eta=Lambda pi/4-1`, the table compares the positive optimum with the onset approximation `(4/21)eta`.

| eta | optimum r | ratio to onset approximation |
|---:|---:|---:|
| 0.01 | 0.0019286709057581 | 1.012552225523 |
| 0.001 | 0.00019071989517554 | 1.001279449672 |
| 0.0001 | 0.00001905006099978 | 1.000128202489 |

The ratio of the computed optimum to `(Lambda C(0)/4)^(4/5)` was `0.890973430607` at `Lambda=10^3`, `0.992944824534` at `10^6`, and `0.999554146478` at `10^9`. These checks confirm the scalar coefficients and asymptotic directions. They do not constitute a numerical verification of the full coupled bulk–surface threshold.

The exact convexity and surface-corrector threshold are standard consequences of an affine reversible Dirichlet form. Their application here and the fractional scaling constants may be useful, but this review makes no claim that those consequences or constants are new to the literature.


For the periodic benchmark `k_delta=delta+2(1-cos s)`, the developing agent supplied an exact derivative integral that I also checked algebraically. With `k=A-B cos s`, integration of `(k′/k^3)′` gives `int k′^2/k^4=(A J3-J2)/3`, where `Jn=int k^-n`. The standard elementary integrals then give `pi A B^2/(A^2-B^2)^(5/2)`. Thus

\[
\int|(1/k_\delta)'|^2ds
={4\pi(\delta+2)\over[\delta(\delta+4)]^{5/2}},
\quad
\Lambda_c(\delta)
={(\delta+4)^{5/2}\over4\pi(\delta+2)}
={4\over\pi}[1+\delta/8+O(\delta^2)].
\]

This exact reduced-model example exhibits a nonzero finite-floor threshold shift. It supports the need to distinguish the limiting onset expansion from a simultaneous physical limit in a shrinking threshold window.
