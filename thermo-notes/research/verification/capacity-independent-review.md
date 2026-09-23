# Independent review of the conditional transport capacity certificate

Reviewer: independent subagent `capacity_review`. Date: 2026-09-06.

Reviewed file: `research/capacity-certificates.md` as supplied at the beginning of this review. The reviewer did not edit that file.

**Verdict:** the Cartesian capacity bounds, residual formulation, and Gaussian calculation are correct under the stated solvability and integrability assumptions. No mathematical error was found in these claims. The stiff Gaussian limit can be proved by a direct trial-function argument, given below. The proposed general-coordinate extension is correct with a specific tangent mobility and coarea-weighted operator; it needs more assumptions than a naive replacement of the Cartesian score. Novelty remains unverified.

## 1. Independent derivation and normalization

Let `J` be a divergence-free current with total flux one from `x=a` to `x=b`, and no lateral flux. Every admissible committor trial function `u` obeys

\[
\int J\cdot\nabla u=1.
\]

Integration by parts gives this identity, with the outward current through `a` equal to minus one and through `b` equal to one. Weighted Cauchy–Schwarz then gives

\[
1\le\left(\int w\nabla u^TD\nabla u\right)
\left(\int w^{-1}J^TD^{-1}J\right).
\]

Minimizing the first factor proves the required lower bound directly. No additional convention for Thomson's principle is needed.

For `K_x phi_x=s_x`, the proposed current has

\[
\partial_xJ_x+\nabla_y\cdot J_y
=\partial_x\nu_x-\nu_xs_x=0,
\]

and resistance

\[
R=\int_a^b\frac{1/d+g}{\rho}\,dx.
\]

Thus `C >= 1/R`. The projected trial function satisfies `rho d f'=U`, and its energy is `U`, proving the other direction. The longitudinal diffusion convention in `L=w^{-1} div(wD grad)` is consistent: there is no missing factor of two.

Replacing `w` by `c w` replaces `rho,C,U,Q` by `c rho,cC,cU,cQ`; it leaves `nu,g,f,r,Q/U` unchanged. All displayed inequalities therefore have the right normalization. To interpret capacity as a stationary transition frequency, normalize by the invariant mass of the **entire underlying process**, rather than by the transition strip alone unless that strip is the entire process. Normalized capacity counts completed transitions in one specified direction; counting both directions gives twice that value for a reversible stationary process. A basin-mass denominator defines a particular rate and is not generally the inverse equilibrium-initialized mean first-passage time.

## 2. Residual identity and spectral control

Direct differentiation gives

\[
Lf=\frac{1}{\rho\nu_x}\partial_x(\rho\nu_x d f')
=\frac U\rho s_x=d f's_x.
\]

Consequently,

\[
Q=U^2\int g/\rho,\qquad
R=1/U+Q/U^2.
\]

This reproduces `C >= U^2/(U+Q)` and `(U-C)/C <= Q/U`. If `h` is the exact committor, `e=f-h` has zero Dirichlet trace and `E(h,e)=0`, so `E(e)=U-C`. The stated upper bound on this error follows from the capacity lower bound.

For the direct residual estimate, `E(e)=-<r,e>_w`. Conditional centering of `r` allows subtraction of the conditional mean of `e`; the transverse negative-Sobolev estimate gives

\[
|\langle r,e\rangle_w|\le\sqrt{Q}\sqrt{\int w\nabla_ye^TM\nabla_ye}
\le\sqrt{Q\mathcal E(e)}.
\]

Hence `U-C <= Q`, as claimed. This weaker argument does not produce the rational lower bound.

If the conditional gap is at least `lambda`, the spectral inequality `K_x^{-1} <= lambda^{-1}` on mean-zero functions gives `g <= Var(s)/lambda`. One must use an actual lower gap bound. The conditional correlation formula follows from `K^{-1}=integral_0^infinity exp(-tK)dt` on the relevant subspace. Finite `g` and an appropriate spectral-domain interpretation suffice; a measured finite-time correlation integral alone is not a certified upper bound.

## 3. Gaussian calculation

Set `z=y-m(x)`. The score of `N(m,sigma^2)` is

\[
s_x=m'z/\sigma^2+(\sigma'/\sigma)(z^2/\sigma^2-1).
\]

For constant `D_y`, a mean-zero Poisson solution is

\[
\phi_x=\frac{m'}{D_y}z+
\frac{\sigma'}{2D_y\sigma}(z^2-\sigma^2).
\]

Applying the Ornstein–Uhlenbeck operator separately to its linear and centered quadratic modes gives exactly the displayed score. Its transverse velocity is `D_y phi_y=m'+(sigma'/sigma)z`, and therefore

\[
g=(m'^2+\sigma'^2)/D_y.
\]

For constant width `sigma^2=1/(beta kappa)`, the gap is `D_y/sigma^2=beta kappa D_y`, while `Var(s)=m'^2/sigma^2`. Their ratio is exactly `m'^2/D_y`; the gap bound is sharp in this example. Increasing stiffness does not reduce this certificate's relative interval width. The next argument proves that a persistent actual projection error can occur as well.

## 4. A rigorous stiff Gaussian capacity limit

Assume a finite interval `[a,b]`, positive bounded `rho,d,D_y` with positive lower bounds, and enough smoothness that the functions below and their first derivatives are bounded. Here `D_y` may depend smoothly on `x`. Let

\[
w_\epsilon(x,y)=\rho(x)\mathcal N(m(x),\epsilon^2)(y),
\quad
A=D_y+d m'^2,
\quad d_{\rm eff}=dD_y/A,
\]

and define

\[
C_0=\left[\int_a^b\frac{dx}{\rho d_{\rm eff}}\right]^{-1},
\qquad f'=\frac{C_0}{\rho d_{\rm eff}},
\qquad \alpha_* =\frac{d m'f'}{A}.
\]

The transport bound already proves `C_epsilon >= C_0` for every positive `epsilon`.

Choose a Lipschitz cutoff `chi_delta` equal to zero at both endpoints and equal to one outside endpoint layers of width `delta`, with `|chi_delta'| <= constant/delta`. Put `alpha_delta=chi_delta alpha_*`. The function

\[
u_{\epsilon,\delta}(x,y)=f(x)+\alpha_\delta(x)(y-m(x))
\]

has the exact Dirichlet data. Its Gaussian energy is exactly

\[
\mathcal E_\epsilon(u)=
\int_a^b\rho\{d(f'-\alpha_\delta m')^2+D_y\alpha_\delta^2
+d\epsilon^2(\alpha_\delta')^2\}\,dx.
\]

Completing the square yields

\[
\mathcal E_\epsilon(u)-C_0
=\int_a^b\rho\{A(\alpha_\delta-\alpha_*)^2
+d\epsilon^2(\alpha_\delta')^2\}\,dx
\le c_1\delta+c_2\epsilon^2/\delta+c_3\epsilon^2.
\]

Taking `delta=epsilon` for sufficiently small `epsilon` proves

\[
\boxed{C_0\le C_\epsilon\le C_0+O(\epsilon).}
\]

If `alpha_*(a)=alpha_*(b)=0`, the uncut `alpha_*` is already admissible and gives the stronger upper error `O(epsilon^2)`. Trial functions need not lie between zero and one; truncating them to that interval preserves the boundary values and cannot increase energy.

This is a direct proof of the claimed **capacity** limit. It does not, by itself, prove convergence of the full stochastic process or its effective generator. The limiting value agrees with the capacity of the stated effective diffusivity and fixed stationary marginal. It establishes asymptotic sharpness of the lower certificate and an actual stiffness-independent projection error whenever `m'` is nonzero on a set of positive measure. The effective diffusivity itself has substantial prior art in constrained and narrow-channel diffusion.

## 5. General scalar coordinate: a precise valid extension

Let `xi` be smooth with nonvanishing gradient, `D` positive definite, and all absorbing boundaries be entire fibers `xi=a,b`. Assume no other boundary, or compatible reflecting walls as specified below. Write

\[
n=\nabla\xi,\quad a(z)=n^TDn,\quad
B=D-Dn(n^TDn)^{-1}n^TD.
\]

The matrix `B` is tangent: `Bn=0`. It is the inverse resistance metric restricted to tangent vectors, extended by zero in the normal direction. It is generally **not** the Euclidean projection `PDP` when `D` has normal–tangent coupling.

Use coarea disintegration

\[
\rho(x)=\int_{\Sigma_x}\frac{w}{|n|}\,d\sigma,
\qquad d\nu_x=\frac{w}{\rho(x)|n|}\,d\sigma,
\quad \bar a(x)=\langle a\rangle_{\nu_x}.
\]

Let `f` minimize the projected energy, so `rho bar(a) f'=U`, and set `r=L(f composed with xi)`. Its conditional mean vanishes, provided integration of divergence across fibers has no omitted wall term. On each fiber define

\[
K_x\phi=-q_x^{-1}\operatorname{div}_{\Sigma_x}
(q_xB\nabla_{\Sigma_x}\phi),
\qquad q_x=w/|n|.
\]

Suppose `K_x phi_x=r` is solvable with finite integrated energy. Then the current

\[
J=\frac wU\{D\nabla(f\circ\xi)+B\nabla\phi\}
\]

is divergence-free. The tangent-current divergence identity is

\[
\operatorname{div}(wB\nabla\phi)
=|n|\operatorname{div}_{\Sigma_x}(q_xB\nabla_{\Sigma_x}\phi)
=-wr.
\]

The uncorrected current has unit fiber flux, and the correction has zero normal flux. The resistance cross term vanishes because `n^T B=0`. Moreover `BD^{-1}B=B`, giving

\[
R=1/U+Q/U^2,\qquad
Q=\int_a^b\rho\langle r,K_x^{-1}r\rangle_{\nu_x}\,dx.
\]

Thus precisely the same rational certificate holds. This derivation verifies the proposed extension with explicit geometry, rather than the Cartesian score formula.

For reflecting lateral walls, a sufficient simplifying condition is `n_wall dot D grad(xi)=0`, together with zero lateral correction flux. Otherwise the baseline current already violates reflection and the fiber correction requires an inhomogeneous boundary condition. Imposing homogeneous fiber Neumann conditions in that case is wrong.

## 6. Adversarial boundaries and counterexamples

- **Disconnected fibers:** zero total conditional mean is insufficient for a Neumann solve; the residual must be orthogonal to every componentwise constant mode. For example, take two disconnected hidden channels, `rho=d=1`, `x in [0,1]`, and conditional masses `p_1=1/2+eta cos(2 pi x)`, `p_2=1-p_1`, with `0<eta<1/2`. No hidden transfer is possible. The exact parallel capacity is `C=sum_i (integral_0^1 dx/p_i)^(-1)=sqrt(1-4 eta^2)<1=U`. A naive pseudoinverse that discards the unresolved componentwise score produces `g=0` and the false claim `C=U`. The original theorem avoids this through its Poisson solvability assumption.
- **A varying support:** the displayed score and homogeneous reflecting condition assume a fixed transverse domain. Moving hard walls introduce boundary transport terms. One cannot substitute a changing-width uniform distribution into the Cartesian score formula and ignore its moving support.
- **Uncontrolled estimation:** an approximate Poisson solve need not produce a divergence-free current. Substituting its energy as if it were exact can overstate a lower bound. One needs a genuinely feasible reconstructed current, a certified upper bound on `g`, or an explicit residual correction.
- **Lower-bound equality:** in a smooth connected product strip with complete Dirichlet fibers, finite-coefficient equality in the lower bound requires the proposed current to be proportional to the true gradient current. Its longitudinal gradient would be independent of `y`, forcing the committor to depend only on `x` because its endpoint values are constant. Then its transverse current is zero. Hence nonzero `g` normally gives a strict lower bound at finite width, despite its proven stiff-limit sharpness.
- **Degenerate integrals:** finite positive projected resistance and finite correction resistance should be stated when presenting positive formulas involving `U,Q`. Infinite correction resistance yields only the trivial lower bound zero. If `U` itself is zero, the residual ratios are not defined and should not be used.

## 7. Targeted prior-art check

The full primary article [Bradley, Physical Review E 80, 061142 (2009)](https://doi.org/10.1103/PhysRevE.80.061142), accessible as an [author-uploaded article](https://www.researchgate.net/publication/43020218_Diffusion_in_a_two-dimensional_channel_with_curved_midline_and_varying_width_Reduction_to_an_effective_one-dimensional_description), derives asymptotic one-dimensional diffusion with contributions from channel-midline and width slopes. Its expansion regime and hard-wall setup differ from the fixed-marginal Gaussian capacity construction. This is strong evidence against claiming the geometry-induced diffusivity reduction itself as new; it does not establish prior publication of the finite-parameter conditional-current certificate. This review did not complete a theorem-level novelty audit of the latter, which remains necessary.

## 8. Follow-up: periodic hard-channel bound

The parent requested an independent check of the proposed hard-channel consequence. It is correct, including the period and invariant-volume normalization.

Let `m,W` be smooth functions of period `ell`, with `W>0`, and define the periodic cell

\[
\Omega=\{0<x<\ell,\ m(x)-W(x)/2<y<m(x)+W(x)/2\}.
\]

Let angle brackets mean the ordinary spatial average over `[0,ell]`. The cell area is `A=ell<W>`. For reflected Brownian motion with isotropic diffusivity `D`, the effective longitudinal diffusivity has the standard cell variational form

\[
D_{\rm eff}=\frac{D}{A}\inf_{\chi\ \mathrm{periodic}}
\int_\Omega|e_x+\nabla\chi|^2.
\]

Equivalently, define the conductance `G` as the minimum of `D integral|grad u|^2` over functions satisfying `u(x+ell,y)=u(x,y)+1`. Then

\[
D_{\rm eff}=\ell^2G/A=\ell G/\langle W\rangle.
\]

A periodic current with unit flux across each section obeys `integral J dot grad u=1`. Its resistance `R=integral |J|^2/D` therefore gives `G>=1/R` by the same Cauchy–Schwarz argument used above.

For the proposed current,

\[
J_x=1/W,\qquad
J_y=\frac{1}{W}\left[m'+\frac{W'}W(y-m)\right],
\]

its divergence is `-W'/W^2+W'/W^2=0`. On the top wall its slope `J_y/J_x=m'+W'/2` matches the wall tangent; the analogous bottom-wall slope is `m'-W'/2`. Thus the reflecting condition holds exactly for any finite slopes. Its flux is exactly one, and direct integration gives

\[
R=\frac1D\int_0^\ell\frac{1+m'^2+W'^2/12}{W}\,dx.
\]

For the upper bound, restrict the cell potential to depend only on `x`; minimization gives `G<=D/(integral dx/W)`. Therefore

\[
\boxed{
\frac{D}{\langle W\rangle\left\langle(1+m'^2+W'^2/12)/W\right\rangle}
\le D_{\rm eff}\le
\frac{D}{\langle W\rangle\langle1/W\rangle}.}
\]

There is no narrow-channel or small-slope assumption. Both bounds equal `D` for a straight constant-width channel. Large slopes can make the lower bound weak but cannot invalidate it. The statement extends to Lipschitz wall graphs with square-integrable indicated resistance, using weak currents. Discontinuous widths with vertical wall segments are outside this argument without an additional construction.

For a symmetric channel `m=0`, writing `W=2 epsilon zeta` gives

\[
D_{\rm lower}/D=
[\langle\zeta\rangle\langle\zeta^{-1}\rangle]^{-1}
\left[1+\epsilon^2\frac{\langle\zeta'^2/\zeta\rangle}
{3\langle\zeta^{-1}\rangle}\right]^{-1}.
\]

This matches Equation (120) in [Mangeat, Guérin and Dean, *Dispersion in two dimensional channels—the Fick–Jacobs approximation revisited*](https://mangeatm.fr/papers/mangeat_guerin_2017_dispersion.pdf), which identifies that expression with Zwanzig's resummation. The inspected discussion around that equation treats it as an approximation, not as this rigorous all-slope lower bound. That observation is a useful novelty lead, **not** proof that an earlier bound is absent elsewhere.

The parent also reports that Legoll–Lelièvre (2009) explicitly discusses stiff projection failure. The stiff-limit section above should therefore be used as a verified illustration and sharpness proof, with that prior art acknowledged, rather than as a discovery of the underlying failure mechanism.
