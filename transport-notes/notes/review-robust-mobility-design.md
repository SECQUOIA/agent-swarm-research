# Independent review: mobility placement before and after observing defects

Reviewed 2026-09-07 by `review_localization`.

Both scalar theorems in [robust-mobility-design.md](robust-mobility-design.md) are correct: the sharp expected optimum when one mobility field must serve all offsets, and the different expected exponent when the offset is observed before choosing the field. The lower bound for the first theorem covers arbitrary budget-dependent L¹ coefficients, including increasingly narrow spikes and arbitrarily rapid oscillations. The adaptive expectation limit has the required uniform control near coalescing zeros.

This review establishes mathematical validity within the scalar compact ensemble. The finite-transverse-bulk extensions have since been independently proved in [review-robust-finite-bulk.md](review-robust-finite-bulk.md), under its fixed-geometry, positive-bulk-diffusivity and nonzero-mean-velocity assumptions. Mathematical verification does not establish novelty.

## Statements verified

For `k_c(s)=(c+cos s)²`, with `c` uniform on `[-2,2]`, and the smooth-test variational definition

\[
J_c(D)=\sup_f\left\{2\int f-\int k_cf^2-\int D|f'|^2\right\},
\qquad D\in L^1,\quad D\ge0,\quad\int D=M,
\]

write

\[
\Phi(M)=\inf_D\mathbb E J_c(D),\qquad
\Psi(M)=\mathbb E\inf_DJ_c(D).
\]

Then

\[
\Phi(M)\sim C_0Z_w^{5/4}M^{-1/4},\qquad
Z_w=4^{-4/5}\,2B(3/10,1/2),
\tag{1}
\]

and

\[
\Psi(M)\sim\frac{C_*2^{6/5}}4B(1/2,1/5)M^{-1/5},
\qquad C_*=12(3/80)^{1/5}.
\tag{2}
\]

Here `C0=(pi/2) Gamma(1/4)/Gamma(3/4)`. One asymptotically optimal predetermined shape is

\[
D_M(s)=M\frac{|\sin s|^{-2/5}}{2B(3/10,1/2)}.
\tag{3}
\]

Its integrable singularities do not violate the L¹ budget; their point values have no effect. The theorem concerns this unrestricted budget class. It is not a theorem with a fixed pointwise mobility cap or prescribed fabrication scale.

## The unrestricted lower bound is sound

The most important issue is whether an M-dependent microstructure could improve on minimizing a fixed-shape approximation. The dual argument in the source note rules this out without any such assumption.

Restrict offsets to a fixed compact subinterval of `(-1,1)`. Their roots form two disjoint compact arcs E, away from the extrema of cosine. On these arcs set

\[
\rho(r)=|\sin r|/4,\quad a(r)=\sin^2r,\quad
w(r)=\rho(r)a(r)^{-3/4},\quad
Z_E=\int_Ew^{4/5},\quad d_E=w^{4/5}/Z_E.
\]

The reference d_E need only be defined by this smooth positive formula on a slightly larger neighborhood of E. Its integral outside E is irrelevant because it specifies test-field widths, rather than the competing mobility coefficient.

Fix `psi in C_c^infinity(R)`, and use at every retained root r the test

\[
h_r(s)=(Md_E(r)a(r))^{-1/2}
\psi\left(\frac{s-r}{\ell_r}\right),\qquad
\ell_r=(Md_E(r)/a(r))^{1/4}.
\]

For small M, the two root tests for each offset have disjoint supports. The root-coordinate change of variables has density `rho(r)dr`, including the disorder factor 1/4. Uniform Taylor expansion of the potential on the retained arcs gives

\[
\mathbb E\left[2\int h_c-\int k_ch_c^2\right]
=M^{-1/4}Z_E^{5/4}(2I_\psi-V_\psi)+o(M^{-1/4}),
\tag{4}
\]

where `I_psi=integral psi` and `V_psi=integral y²psi²`. The cubic Taylor remainder contributes O(1) for these fixed tests and arcs, so it is negligible relative to `M^(−1/4)`.

I independently checked the derivative exponents. The squared derivative at one root has prefactor `M^(−3/2)d_E^(−3/2)a^(−1/2)`. Thus

\[
G_M(s):=\mathbb E|h_c'(s)|^2
=M^{-3/2}\int_E\rho(r)d_E(r)^{-3/2}a(r)^{-1/2}
\left|\psi'\left(\frac{s-r}{\ell_r}\right)\right|^2dr.
\]

When the integrand is nonzero, `|s−r|=O(M^(1/4))`. In the change of variables `y=(s−r)/ell_r`,

\[
\left|\frac{dr}{dy}\right|=\ell_r[1+O(M^{1/4})]
\]

uniformly, because `ell_r'=O(M^(1/4))` on the extended arcs. The resulting coefficient is

\[
M^{-5/4}\rho(s)d_E(s)^{-5/4}a(s)^{-3/4}
=M^{-5/4}Z_E^{5/4}.
\]

Truncating the r integral at the endpoints of E can only decrease the transformed integral of the nonnegative squared derivative. Outside the shrinking neighborhoods of E, it is zero. It follows that

\[
\sup_sG_M(s)\le M^{-5/4}Z_E^{5/4}
\left[\int|\psi'|^2+o(1)\right].
\tag{5}
\]

This is a uniform bound over the entire wall, including the arc edges. No derivative of the actual competing design appears anywhere.

For every admissible D, the test-field variational inequality and its budget give

\[
\mathbb E J_c(D)\ge
\mathbb E\left[2\int h_c-\int k_ch_c^2\right]
-M\sup_sG_M(s).
\]

Combining (4) and (5), taking the infimum over all D, and then taking the harmonic-oscillator variational supremum over fixed compact smooth psi yields

\[
\liminf_{M\downarrow0}M^{1/4}\Phi(M)\ge C_0Z_E^{5/4}.
\]

Expanding the retained offset interval to `(-1,1)` gives the lower bound in (1). The order of limits is valid: first M tends to zero for fixed arcs and fixed test, then the test supremum is taken, then the arcs expand. There is no exchange of a design infimum with a resolvent supremum.

## The singular predetermined shape supplies the upper bound

The normalized shape in (3) is smooth near the two roots for every fixed `|c|<1`, except at the measure-zero fold offsets. Local variable-coefficient quadratic bracketing therefore gives

\[
M^{1/4}J_c(Md_*)\longrightarrow
C_0\sum_{c+\cos r=0}d_*(r)^{-1/4}|\sin r|^{-3/2}.
\]

The rest of the wall contributes a bounded scalar term at each fixed offset because its potential is bounded below. Large mobility values there cause no problem for this upper bound: derivative energy can simply be discarded on those pieces.

Crucially, `d_*>=b>0` globally. Form ordering gives `J_c(Md_*)<=J_c(Mb)`. The uniform random-offset bounds in [the disorder review](review-random-kinetic-barriers.md) give an integrable envelope for `M^(1/4)J_c(Mb)`, proportional near the folds to `|1−|c||^(−3/4)`. Dominated convergence is justified. Changing from offset to root position gives

\[
\lim_{M\downarrow0}M^{1/4}\mathbb E J_c(Md_*)
=C_0\int w(s)d_*(s)^{-1/4}ds=C_0Z_w^{5/4}.
\]

The unbounded coefficient has a natural closed weighted form: it is measurable, integrable, and bounded below by a positive constant times M, and all smooth periodic tests have finite energy. The singular coefficient is not being interpreted through an unjustified classical derivative at its two exceptional points.

The claim about unrestricted bounded smooth approximations is also valid. Clip and smooth the shape while preserving a uniform positive lower bound, then normalize its integral. Their fixed-shape constants converge to the optimum by dominated convergence against the integrable weight w. A diagonal small-M choice attains the same asymptotic infimum. This does not impose one common numerical upper bound on the entire approximating sequence.

## The adaptive expectation and its fold layer

For each fixed `|c|<1`, the previously independently verified two-well allocation theorem gives

\[
j_M(c):=\inf_DJ_c(D)
\sim C_*2^{6/5}(1-c^2)^{-4/5}M^{-1/5}.
\tag{6}
\]

The exponent `−4/5` at a fold is integrable, but that alone would not justify averaging. The three trial bounds in the source note close this gap.

For an inside distance `t=1−|c|>=L M^(2/7)`, the root separation is comparable to `sqrt(t)` and each local quadratic curvature to t. A half-budget optimal quadratic profile has width `R` comparable to `(M/t)^(1/5)`. The ratio `R/sqrt(t)` is bounded by a small fixed constant when L is sufficiently large. The profiles therefore fit disjoint neighborhoods where uniform quadratic potential comparisons hold. Their interior and adjacent reciprocal-potential contributions are bounded by `C/(tR)`. The remaining local contribution is `Ct^(−3/2)`, and

\[
\frac{t^{-3/2}}{M^{-1/5}t^{-4/5}}
=M^{1/5}t^{-7/10}\le L^{-7/10}.
\]

Hence `j_M(c)<=CM^(−1/5)t^(−4/5)` uniformly in this regime.

For `|t|<=L M^(2/7)`, place all mobility uniformly on a radius `K M^(1/7)` interval about the fold, with K sufficiently large, and zero elsewhere. The mobility there is of order `M^(6/7)`. Rescaling distance by `M^(1/7)` makes both the diffusion and the quartic potential of order `M^(4/7)`. On the fixed rescaled interval the parameter `t/M^(2/7)` ranges in a compact set, and the Neumann operator is uniformly coercive: its derivative coefficient is positive and none of its nonnegative potentials is identically zero. The integrated interior inverse is therefore at most `CM^(−3/7)`. The interval endpoints lie beyond all nearby roots with a fixed scaled margin; the reciprocal-potential integral outside is also at most `CM^(−3/7)`. Neumann bracketing suffices for this upper bound, regardless of the abrupt jump to zero mobility outside.

For the outside distance `t<=−L M^(2/7)`, discard derivative energy to obtain `j_M(c)<=integral 1/k_c<=C|t|^(−3/2)`.

These three bounds imply on both sides of each fold

\[
M^{1/5}j_M(c)\le C|t|^{-4/5}\qquad(t\ne0),
\tag{7}
\]

which is integrable. In the central layer this follows from `|t|<=L M^(2/7)`; on the outside it follows from `|t|>=L M^(2/7)`. Away from the folds the required bounds are uniform by the same fixed-neighborhood trial construction, or by positive potential.

Dominated convergence applied to (6) and (7) proves (2). The central fold layer has probability `O(M^(2/7))` and response at most `CM^(−3/7)`, so its contribution is `O(M^(−1/7))`, smaller than the leading adaptive mean. This is a bound on that layer, not a complete next-order expansion.

## Numerical constants and scope

Independent evaluations of the beta and gamma expressions give:

| Design | Leading mean coefficient | Budget exponent |
|---|---:|---:|
| Uniform predetermined mobility | 19.2932034451649 | −1/4 |
| Optimal predetermined mobility | 18.3860636501143 | −1/4 |
| Mobility chosen after observing c | 22.4046282307491 | −1/5 |

Thus the predetermined optimum improves the uniform leading constant by `4.70186196724%`, and

\[
\Psi(M)/\Phi(M)\sim1.21856579293469\,M^{1/20}.
\]

The exponent change is verified, but its small power makes the asymptotic ratio converge slowly. These formulas by themselves provide no quantitative error bound at a given finite budget.

The lower-bound proof also remains valid for a scalar relaxation in which the mobility is a finite nonnegative measure: the test fields are smooth and (5) bounds their averaged derivative square pointwise. This observation excludes a better leading constant from atomic concentration in that precise variational relaxation. It does not assign a physical diffusion process to an atomic mobility measure.

The scalar arguments here directly apply to the exactly well-mixed bulk model. The required estimates uniform over disorder for the finite-bulk design extensions are supplied in [review-robust-finite-bulk.md](review-robust-finite-bulk.md). A constant-mobility disorder remainder estimate or a fixed-realization design estimate alone would not have justified that extension.
