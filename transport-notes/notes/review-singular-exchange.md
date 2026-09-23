# Independent review: singular exchange and surface diffusion

Review date: 2026-09-06. Reviewer: `review_singular_exchange`.

The reduced-model resolvent, dispersion coefficient, quadratic-minimum crossover function, and stationary anomalous-variance coefficient are correct under the assumptions below. The coefficient for particles initially in the mobile state is half the stationary coefficient. An exact finite-bulk-diffusivity result is available when surface diffusion vanishes. The appended Schur-complement and spectral estimate also establishes a bounded finite-bulk correction when surface diffusion is positive. These checks do not establish novelty.

## Model and exact cell equation

Let the state space consist of one well-mixed bulk state `b` and a periodic wall coordinate `s` of length `P`. Let `A>0`, `K>0`, and `k(s)>=0`. The transition rate from `b` into `ds` is `K k(s) ds/A`, the reverse rate is `k(s)`, and surface diffusion has generator `Ds d_s^2`. Thus both adsorption and desorption vanish at a zero of `k`; equilibrium affinity remains constant. This is kinetic heterogeneity, not heterogeneity in equilibrium binding strength.

Write `Z=A+KP`. The invariant measure is

\[
\pi_b=A/Z,\qquad \pi_s(ds)=K\,ds/Z.
\]

The backward generator is

\[
Lf_b={K\over A}\int k(s)(f_s-f_b)\,ds,
\qquad
Lf_s=D_s f_s''+k(s)(f_b-f_s).
\]

With axial velocities `U` in the bulk and zero on the wall,

\[
V={UA\over Z},\qquad g_b=U-V,\quad g_s=-V.
\]

Let `H=-Ds d_s^2+k(s)` on periodic functions. In the cell equation `-L phi=g`, choose the additive constant so that `phi_b=0`. Then

\[
H\phi_s=-V,\qquad \phi_s=-V H^{-1}1.
\]

Integration of `Hq=1` gives `int kq=P`, which verifies the bulk cell equation because `(K/A)VP=U-V`. Consequently the velocity contribution to the effective axial diffusivity is exactly

\[
D_{\rm flow}=\langle g,\phi\rangle_\pi
={V^2K\over Z}\int H^{-1}1\,ds.
\tag{1}
\]

For `Ds>0` and nonzero nonnegative `k`, `H` is strictly positive on the compact wall. For `Ds=0`, finiteness of (1) requires `int 1/k<infinity`. Isolated exact zero-rate states at `Ds=0` support singular absorbing measures; all statements about the invariant measure refer to the absolutely continuous communicating class and initial distributions that do not charge those points.

Independent axial Brownian motion contributes its stationary average diffusivity. In particular, bulk axial diffusivity `Dx` with no wall axial diffusion adds `A Dx/Z`. Wall diffusion along `s` alone is distinct from axial wall diffusion.

## Full stationary covariance resolvent

For `p>0`, define

\[
q_p=(p+H)^{-1}1,\qquad I(p)=\int q_p\,ds.
\]

Since `H1=k`, `(p+H)^{-1}k=1-pq_p`. If `r=(p-L)^{-1}g`, its wall component is

\[
r_s=r_b-(pr_b+V)q_p.
\]

The bulk equation gives

\[
r_b={ (K/A)V I(p)\over 1+(K/A)[P-pI(p)]}.
\]

Taking the invariant inner product cancels the constant part and yields

\[
\widehat C(p)
=\int_0^\infty e^{-pt}\operatorname{Cov}_\pi(v(t),v(0))\,dt
={V^2K I(p)\over Z-KpI(p)}.
\tag{2}
\]

This independently confirms the claimed denominator. It must not be discarded in an exact finite-frequency formula. At a quadratic zero, its correction is lower order in the long-time and small-surface-diffusion asymptotics.

## Quadratic-minimum crossover

Suppose a single minimum has

\[
k(s)=\delta+a(s-s_0)^2+o((s-s_0)^2),\qquad a>0.
\]

Set

\[
\ell=(D_s/a)^{1/4},\quad \epsilon=\sqrt{aD_s},\quad z=\delta/\epsilon.
\]

The local rescaling `s-s0=ell x` gives `H=epsilon[-d_x^2+x^2+z]` to leading order. Hence

\[
I(0)\sim D_s^{-1/4}a^{-3/4}\mathcal C(z),
\quad
\mathcal C(z)=\int_{\mathbb R}(-\partial_x^2+x^2+z)^{-1}1\,dx.
\tag{3}
\]

For the harmonic oscillator `H0=-d_x^2+x^2`, the integrated Mehler kernel is

\[
\int_{\mathbb R^2}e^{-tH_0}(x,y)\,dx\,dy
=\sqrt{\frac{2\pi}{\sinh(2t)}}.
\]

The two-dimensional Gaussian integration is especially useful for checking factors of two: the exponent matrix has determinant one, so its integral is `2 pi`; the kernel prefactor is `[2 pi sinh(2t)]^-1/2`. Therefore

\[
\begin{aligned}
\mathcal C(z)
&=\sqrt{2\pi}\int_0^\infty {e^{-zt}\over\sqrt{\sinh(2t)}}\,dt\\
&={\sqrt\pi\over2}B\!\left({z+1\over4},{1\over2}\right)
={\pi\over2}{\Gamma((z+1)/4)\over\Gamma((z+3)/4)}.
\end{aligned}
\tag{4}
\]

Thus `C(0)=4.647476009400967`, and `C(z)~pi/sqrt(z)` as `z` tends to infinity. The latter recovers `I(0)~pi/sqrt(a delta)`.

The local asymptotic is appropriate as `Ds` and `delta` approach zero with bounded `z`. A claim uniform for all `delta>=0` is false for a general periodic rate profile: when `delta` remains fixed, the answer tends to the global integral `int 1/k`, which need not equal the local quadratic approximation. Matching to `z->infinity` requires `delta->0` as well. Multiple separated quadratic minima contribute additively to the leading singular integral.

A complete theorem for a general smooth profile should state uniform lower bounds on `k` away from the minima and uniform local Taylor remainders. The harmonic formula is exact; reduction of a general periodic profile is a localization asymptotic. Variational localization or resolvent convergence with an integrable outer bound can supply a rigorous proof. The numerical tests below support this reduction but do not replace that proof.

## Zero surface diffusion: stationary and injected ensembles differ

At `Ds=delta=0`,

\[
I(p)=\int {ds\over p+k(s)}\sim {\pi\over\sqrt a}\,p^{-1/2}.
\]

Equation (2) gives

\[
C(t)\sim {V^2K\over Z}\sqrt{\pi\over a}\,t^{-1/2}.
\]

Reversibility gives a positive spectral measure for `C`; standard Laplace asymptotics therefore apply without an oscillatory-tail ambiguity. For stationary initialization,

\[
\operatorname{Var}_\pi X(t)
=2\int_0^t(t-r)C(r)\,dr
\sim {8\over3}{V^2K\over Z}\sqrt{\pi\over a}\,t^{3/2}.
\tag{5}
\]

For initialization in the mobile state, let `m(t)=P_b(state(t)=b)`. Regeneration at a mobile-state observation gives

\[
\widehat m(p)={A\over p[Z-KpI(p)]}.
\]

For the mobile occupation time `T(t)`,

\[
\widehat{\mathbb ET}(p)=\widehat m(p)/p,
\qquad
\widehat{\mathbb ET^2}(p)=2\widehat m(p)^2/p.
\]

Expanding the exact transform and subtracting the squared mean gives

\[
\mathbb E_bX(t)=Vt+2V{K\over Z}\sqrt{\pi\over a}\,t^{1/2}+o(t^{1/2}),
\]

\[
\operatorname{Var}_bX(t)
\sim {4\over3}{V^2K\over Z}\sqrt{\pi\over a}\,t^{3/2}.
\tag{6}
\]

This factor-of-two difference is material for experiments using a bulk injection. Equations (5) and (6) cannot be interchanged. Independent bulk axial Brownian motion contributes only order `t` to the variance and leaves their leading terms unchanged.

The mechanism also exposes overlap with established trapping theory. A fresh wall visit samples `s` proportionally to `k(s)`, so its survival tail is proportional to `int k(s) exp[-k(s)t] ds`, which scales as `t^-3/2`. Visit durations have finite mean and infinite variance. A stationary wall observation instead samples `s` uniformly, giving a residual survival tail `t^-1/2`. This is the usual residual-life bias of renewal theory, not a new mechanism by itself.

## Exact finite bulk mixing result when surface diffusion vanishes

The well-mixed assumption can be removed exactly for `Ds=0`. Let a smooth bounded cross-section `Omega` have area `A` and perimeter `P`, transverse diffusivity `Db>0`, axial velocity `u(y)`, and adsorption rate `ka=Kk`. The stationary bulk density is `1/Z`, and the stationary wall density is `K/Z`. Here

\[
V={1\over Z}\int_\Omega u(y)\,dy.
\]

The bulk cell field obeys

\[
-D_b\Delta\phi_b=u-V,
\qquad
D_b\partial_n\phi_b=Kk(\phi_s-\phi_b).
\]

The wall cell equation gives `phi_s=phi_b-V/k`, so the bulk problem reduces to

\[
-D_b\Delta\phi_b=u-V,
\qquad D_b\partial_n\phi_b=-KV.
\tag{7}
\]

Its compatibility condition holds because `int(u-V)=KPV`. Crucially, this Neumann problem is independent of `k(s)`. Integration by parts in `Dflow=<g,phi>` gives the exact identity

\[
D_{\rm flow}
={D_b\over Z}\int_\Omega|\nabla\phi_b|^2\,dy
+{KV^2\over Z}\int_{\partial\Omega}{ds\over k(s)}.
\tag{8}
\]

This holds whenever the reciprocal-rate integral is finite, including a positive regularization `delta>0`. The entire dependence on heterogeneous kinetics is the second term. The first term includes finite bulk mixing and is nonnegative. Consequently the `delta^-1/2` divergence and its coefficient are exact at any fixed positive transverse diffusivity when surface diffusion is absent.

For `Ds>0`, the wall equation involves `H^-1(k phi_b)` and no longer reduces to (7). The appended proof below supplies the needed uniform estimate and establishes the same leading dispersion crossover for finite bulk mixing. This review does not derive finite-bulk long-time anomalous prefactors from (8), since divergence of a static cell problem alone does not determine a temporal prefactor.

## Numerical checks performed independently

Double-integrating the Mehler representation by `scipy.integrate.quad` matched (4) to relative errors below `2e-13` at `z=0,1,10`.

A periodic centered finite-difference solve used `P=2 pi`, `a=1`, `k(s)=delta+2(1-cos s)`, and 40,000 mesh points. The table reports `I_numeric/[Ds^-1/4 C(z)]`.

| z | Ds=1e-2 | Ds=1e-4 | Ds=1e-6 |
|---|---:|---:|---:|
| 0 | 1.00263112 | 1.00024726 | 1.00002517 |
| 1 | 0.98847443 | 0.99881421 | 0.99988122 |
| 10 | 0.89452162 | 0.98773161 | 0.99875241 |

These were fresh computations by this reviewer, independent of the developing agent's computations. They check the local coefficient and scaled parameter, but are not mesh-convergence tests and do not independently test the ensemble-dependent variance coefficients.

## Novelty cautions and primary literature leads

The general adsorption–desorption Taylor-dispersion framework is established in [Levesque, Bénichou, Voituriez, and Rotenberg, Taylor Dispersion with Adsorption and Desorption (2012)](https://arxiv.org/abs/1211.5224). Equation (1) is a specialized cell-problem evaluation within that framework; its derivation alone is not sufficient novelty.

Mobile–immobile transport with distributed exchange rates is established in [Salamon, Fernàndez-Garcia, and Gómez-Hernández, Modeling mass transfer processes using random walk particle tracking (2006)](https://doi.org/10.1029/2006WR004927), which explicitly discusses multiple immobile domains, kinetic sorption, and distributions of rates. The `Ds=0` model is directly in that family.

Relevant open literature includes [Rate equations, spatial moments, and concentration profiles for mobile-immobile models with power-law and mixed waiting time distributions (2022)](https://arxiv.org/abs/2204.01044), [Effective drift and diffusion of a particle jumping between mobile and immobile states (2011)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3181143/), and [Apparent anomalous diffusion and non-Gaussian distributions in a simple mobile–immobile transport model with Poissonian switching (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9257594/). These sources make generic claims of novelty for heavy-tail dispersion or initialization dependence unsafe. Their exact scope relative to the present finite-mean, infinite-variance residence distribution still requires full-text comparison.

The potentially distinctive object is the explicit spatial-diffusion regularization of a smooth zero of the exchange rate, including the harmonic-oscillator crossover and its quantitative connection to measured axial dispersion. Targeted searches in this review did not identify that exact result. Search failure is not evidence sufficient to call it publishable. The finite-bulk theorem established below, broader geometric universality, and precise comparison with multirate mass-transfer models could strengthen the case.

## Additional independent review: bounded finite-bulk correction for positive surface diffusion

The parent agent proposed a shorter proof through an `L2` bound on the exchange flux. I checked the signs, operator positivity, trace estimate, and spectral localization independently. The argument is sound under the assumptions stated here and closes the previously identified finite-bulk correction gap.

Assume `Omega` is a fixed bounded connected smooth cross-section, `Db>0`, `u` belongs to `L2(Omega)`, `K>0` is fixed, and

\[
k_\delta(s)=\delta+k_0(s),\qquad \delta\ge0,
\]

where `k0` is nonnegative and `C2` on the periodic wall, with finitely many nondegenerate quadratic zeros and no other zeros. All constants below may depend on these fixed data, but not on sufficiently small positive `Ds` or on `delta`. Write

\[
H=-D_s\partial_s^2+k_\delta,\quad h=H^{-1}1,\quad J=\int h\,ds,
\quad B={KV^2\over Z}.
\]

Then

\[
0\le D_{\rm flow}-BJ\le C.
\tag{9}
\]

In particular, every divergent leading asymptotic of `J` transfers unchanged to the finite-bulk dispersion coefficient. The quadratic crossover has the same prefactor as in the well-mixed model; the mean velocity uses the actual bulk integral `V=int u/Z`.

**Step 1: exact elimination of the wall field.** The reversible cell variational principle is

\[
ZD_{\rm flow}=\sup_{b,w}\left\{
2\int_\Omega(u-V)b-2KV\int_{\partial\Omega}w
-D_b\int_\Omega|\nabla b|^2
-KD_s\int_{\partial\Omega}|w'|^2
-K\int_{\partial\Omega}k_\delta(w-b)^2
\right\}.
\]

Here boundary occurrences of `b` denote its trace. Maximizing in `w` gives `w=H^-1(k_delta b-V)` and therefore

\[
\begin{aligned}
ZD_{\rm flow}=KV^2J+\sup_b\{&2\int_\Omega(u-V)b
-2KV\int_{\partial\Omega}k_\delta h b\\
&-D_b\int_\Omega|\nabla b|^2
-K\langle b,(k_\delta-k_\delta H^{-1}k_\delta)b\rangle_{\partial\Omega}\}.
\end{aligned}
\tag{10}
\]

The last quadratic form is nonnegative because it equals

\[
\inf_w\left[D_s\int|w'|^2+\int k_\delta(w-b)^2\right].
\]

Also `H1=k_delta`, so that form annihilates constants. Integration of `Hh=1` gives `int k_delta h=P`. Together with `int_Omega(u-V)=KPV`, this makes the linear term invariant under adding a constant to `b`. Taking `b=0` proves the lower bound in (9).

**Step 2: a uniform spectral lower bound.** Choose a smooth fixed partition with `sum_j chi_j^2=1`, one function near each zero and one supported away from all zeros. Near zero `s_j`, `k0(s)>=c_j(s-s_j)^2`; on the remaining support, `k0>=kappa>0`. For a function `f` supported within a local coordinate interval and extended by zero,

\[
\int[D_s|f'|^2+c_j(s-s_j)^2|f|^2]\,ds
\ge\sqrt{c_jD_s}\int|f|^2\,ds.
\]

This follows by expanding the nonnegative square `int|sqrt(Ds) f'+sqrt(c_j)(s-s_j)f|^2`. Partition localization gives the exact identity

\[
\langle f,Hf\rangle
=\sum_j\langle\chi_jf,H\chi_jf\rangle
-D_s\int\sum_j|\chi_j'|^2|f|^2.
\]

The localization error is `O(Ds)||f||^2`. Consequently, for sufficiently small `Ds`,

\[
\lambda_{\min}(H)\ge\delta+c_*\sqrt{D_s},\qquad c_*>0.
\tag{11}
\]

The same argument works for multiple wall components if each component either has the specified isolated zeros or has a positive lower bound on `k0`. A component with identically zero `k0` does not satisfy the assumptions and cannot be silently included.

**Step 3: uniform `L2` exchange-flux bound.** Since `h=H^-1 1`, (11) gives

\[
\|h\|_2\le {\sqrt P\over c_*\sqrt{D_s}}.
\]

Multiply `Hh=1` by `k_delta h` and integrate around the wall. Two integrations by parts yield

\[
\|k_\delta h\|_2^2+D_s\int k_\delta|h'|^2
=P+{D_s\over2}\int k_0''h^2.
\tag{12}
\]

The right-hand constant is `P`, not `int h`, because `int k_delta h=P`. The derivative term on the right has the positive sign displayed. Dropping the nonnegative derivative term on the left and bounding the remaining term gives

\[
\|k_\delta h\|_2^2
\le P+{\|k_0''\|_\infty P\over2c_*^2}.
\tag{13}
\]

No pointwise estimate on `k_delta h` is required.

**Step 4: bounded bulk optimization.** Fix the gauge `int_Omega b=0`. Poincare and trace inequalities imply

\[
\left|\int_\Omega(u-V)b-KV\int_{\partial\Omega}k_\delta h b\right|
\le M\|\nabla b\|_{L^2(\Omega)},
\]

where `M` is uniform by (13). Discard the nonpositive Schur term in (10), and maximize `2Mx-Db x^2` over `x>=0`. This gives

\[
0\le D_{\rm flow}-BJ\le {M^2\over ZD_b},
\]

which proves (9).

The proof requires fixed positive `Db`; its bound is not uniform as bulk diffusivity vanishes. It proves the bounded correction to the static effective diffusivity, not a uniform approximation of the full time-dependent propagator. The general-profile scalar asymptotic (3) still requires its own localization argument. Equation (9) cleanly separates that scalar issue from the finite-bulk coupling, and the exact harmonic coefficient (4) remains independently verified.

## Sharper conclusion: convergence of the finite-bulk correction

The parent's subsequent refinement is also correct. In fact, the bounded remainder in (9) converges to the bulk term in (8):

\[
D_{\rm flow}={KV^2\over Z}J+
{D_b\over Z}\int_\Omega|\nabla b_0|^2+o(1),
\tag{14}
\]

where `b0` is the solution of (7). This holds as `Ds` approaches zero, uniformly with respect to the additive nonnegative floor `delta`; the fixed-data assumptions above remain in force.

First, the bound `J=O(Ds^-1/4)` can be established without assuming the full crossover asymptotic. Set `r=Ds^1/4` and let `N_r` be the union of radius-`r` intervals around the finitely many zeros. Its length is `O(r)`, and `int_(wall minus N_r) 1/k_delta=O(1/r)`. Since

\[
\langle h,Hh\rangle=J,\quad
\|h\|_2^2\le J/\lambda_{\min}(H),\quad
\int k_\delta h^2\le J,
\]

Cauchy–Schwarz on the near and far regions gives

\[
J\le C\sqrt{J}\left[\sqrt{r/\lambda_{\min}(H)}+r^{-1/2}\right]
\le C\sqrt{J}\,D_s^{-1/8}.
\]

Therefore `J<=C Ds^-1/4`, uniformly in `delta>=0`.

The spectral bound now gives the sharper estimate

\[
D_s\|h\|_2^2\le {D_sJ\over\lambda_{\min}(H)}=O(D_s^{1/4})\longrightarrow0.
\]

Using `int k_delta h=P` in (12),

\[
\|k_\delta h-1\|_2^2
=\|k_\delta h\|_2^2-P
\le {D_s\over2}\|k_0''\|_\infty\|h\|_2^2
=O(D_s^{1/4}).
\tag{15}
\]

Thus the bulk linear functional in (10),

\[
L_D(b)=\int_\Omega(u-V)b-KV\int k_\delta h b,
\]

converges in the dual norm of mean-zero `H1(Omega)` to

\[
L_0(b)=\int_\Omega(u-V)b-KV\int b.
\]

Let `S_D(b)=<b,(k_delta-k_delta H^-1 k_delta)b>`. It satisfies `S_D>=0`, and for each fixed smooth bulk test field,

\[
S_D(b)=\inf_w\left[D_s\int|w'|^2+\int k_\delta(w-b)^2\right]
\le D_s\int|(b|_{\partial\Omega})'|^2.
\]

The upper limit of the supremum in (10) is therefore no greater than `sup_b[2L0(b)-Db int|grad b|^2]`: discard the nonnegative `K S_D`, then use convergence of the load in the energy dual norm. The lower limit is no smaller than this value: insert any fixed smooth test field, pass to the limit, and use density of smooth fields in `H1(Omega)`. No boundary derivative of the limiting solution is needed.

The limiting supremum equals `Db int|grad b0|^2` by the weak Neumann problem (7), proving (14). This convergence concerns the regular bulk correction. It does not assert that `J` minus its leading local asymptotic is bounded, nor does it improve the still separate approximation of `J` by the harmonic expression.

## Closing the scalar localization proof

The scalar crossover (3) can also be proved under the stated `C2` and isolated-quadratic-zero assumptions. The following comparison closes the finite-interval convergence gap in the initial localization outline. It was developed independently in response to `direction_interfaces`' proposed Dirichlet–Neumann bracketing.

Let

\[
q_\infty=(-\partial_x^2+x^2+z)^{-1}1\quad\text{on }\mathbb R,\qquad z\ge0.
\]

The Mehler semigroup applied to the constant function gives

\[
q_\infty(x)=\int_0^\infty
\frac{e^{-zt}}{\sqrt{\cosh(2t)}}
\exp\left[-\frac{x^2}{2}\tanh(2t)\right]dt.
\tag{16}
\]

Splitting this integral at any fixed positive time proves

\[
q_\infty(R)=O(R^{-2}),\qquad
q_\infty'(R)=O(R^{-3})<0,\qquad
\int_{|x|>R}q_\infty(x)dx=O(R^{-1}),
\]

uniformly for `z` in bounded nonnegative sets. The same estimates are in fact bounded uniformly for all `z>=0`; only relative asymptotics later require bounded `z`.

Let `phi` be the even positive solution of

\[
\phi''=(x^2+z)\phi,\qquad \phi(0)=1,\quad\phi'(0)=0.
\]

On `[-R,R]`, the Dirichlet and Neumann solutions with unit source are exactly

\[
q_R^{\rm D}=q_\infty-q_\infty(R)\frac{\phi}{\phi(R)},
\qquad
q_R^{\rm N}=q_\infty-q_\infty'(R)\frac{\phi}{\phi'(R)}.
\tag{17}
\]

Symmetry and the two respective endpoint conditions verify these expressions. Positivity and monotonicity of `phi` give

\[
\int_{-R}^R\frac{\phi}{\phi(R)}\,dx\le2R.
\]

For the Neumann correction, monotonicity implies that the integral of `phi` over `[0,R/2]` does not exceed its integral over `[R/2,R]`, while

\[
\phi'(R)=\int_0^R(x^2+z)\phi(x)dx
\ge\frac{R^2}{4}\int_{R/2}^R\phi(x)dx.
\]

Consequently `int_0^R phi/phi'(R)<=8/R^2`. The integrated Dirichlet correction in (17) is `O(R^-1)` and the integrated Neumann correction is `O(R^-5)`. Together with the whole-line tail estimate, this proves

\[
\int_{-R}^Rq_R^{\rm D}dx\longrightarrow\mathcal C(z),\qquad
\int_{-R}^Rq_R^{\rm N}dx\longrightarrow\mathcal C(z),
\tag{18}
\]

uniformly for bounded `z>=0`.

To apply this result to a general wall profile, choose disjoint fixed neighborhoods of the zeros `s_j`. Given sufficiently small `eta>0`, shrink them so that

\[
(a_j-\eta)(s-s_j)^2\le k_0(s)\le(a_j+\eta)(s-s_j)^2.
\]

The functional `J=sup_f[2 int f-int(Ds|f'|^2+k_delta f^2)]` admits Dirichlet–Neumann bracketing at the neighborhood endpoints. Imposing zero values at the cuts restricts its variational domain and gives a lower bound. Allowing independent interval fields enlarges the domain and gives the sum of Neumann problems as an upper bound. The complementary intervals contribute at most their total length divided by a fixed positive lower bound on `k0`, hence only `O(1)`.

On each near interval, potential ordering bounds the result between harmonic Dirichlet and Neumann problems with curvatures `a_j+eta` and `a_j-eta`, respectively. Rescaling takes the fixed interval to radius `R` tending to infinity; (18) applies. Send `Ds` to zero first and then `eta` to zero. Continuity of (4), uniformly on compact scaled-floor intervals, proves

\[
J=D_s^{-1/4}\sum_j a_j^{-3/4}
\mathcal C\!\left(\frac\delta{\sqrt{a_jD_s}}\right)
+o(D_s^{-1/4})
\tag{19}
\]

uniformly when `0<=delta/sqrt(Ds)<=M` for each fixed finite `M`.

This supplies the previously outstanding general-profile scalar argument. Combined with (14), it establishes the full finite-bulk leading crossover under the explicit assumptions. It does not extend the relative crossover uniformly to fixed positive `delta`.
