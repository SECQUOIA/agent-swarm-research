# Optimal placement of a limited surface-mobility budget

Independent mathematical review, 2026-09-06. The parent agent proposed the whole-line quadratic profile. This note independently verifies its constants, global optimality, and uniqueness, and supplies localization and finite-bulk extensions. Literature novelty is being audited separately; mathematical verification is not a novelty claim.

## Exact quadratic model

Let `a,M>0`. For a nonnegative Lebesgue-integrable mobility `D` on the real line with `∫D=M`, define

\[
 J(D)=\sup_{f\in C_c^\infty(\mathbb R)}
 \left\{2\int f-\int\bigl(D|f'|^2+ax^2f^2\bigr)\right\}.
 \tag{1}
\]

An infinite value is allowed. This test-function definition avoids assuming an inverse exists for every admissible coefficient. For the optimal coefficient below it agrees with the natural closed-form inverse functional. For arbitrary measurable coefficients, an operator interpretation requires a specified closed realization; the optimization proof itself only uses (1).

Set

\[
 R=\left(\frac{80M}{3a}\right)^{1/5},\qquad y=\frac{|x|}{R}.
\]

Then the unique optimal coefficient, up to changes on sets of measure zero, is

\[
 \boxed{D_*(x)=\frac{aR^4}{8}y(1-y)^2(1+2y)\,\mathbf1_{y<1}.}
 \tag{2}
\]

Its inverse field and minimum are

\[
 h_*(x)=
 \begin{cases}
 (9-8y)/(aR^2),&0\le y\le1,\\
 1/(ax^2),&y>1,
 \end{cases}
 \qquad
 \boxed{J(D_*)=\frac{12}{aR}
 =12\left(\frac3{80}\right)^{1/5}a^{-4/5}M^{-1/5}.}
 \tag{3}
\]

The optimizer is zero exactly at the kinetic zero and outside its finite support. It has a linear cusp near the kinetic zero and vanishes quadratically at the support endpoints. Thus mobility is concentrated around the trapping defect while retaining zero pointwise mobility at its center. No continuity or transmission of individual diffusion paths across the center is assumed. The conservative form can separate the two half-lines at that zero, while exchange with the bulk still connects the physical states. Initial point masses at the exact kinetic zero require separate state-space conventions and are not part of stationary dispersion with absolutely continuous equilibrium measure.

### Direct checks

Write `p(y)=y(1−y)²(1+2y)=y−3y³+2y⁴`. On `0<x<R`,

\[
 D_*h_*'=-Rp(y),\qquad
 p'(y)+y^2(9-8y)=1.
\]

Hence `−(D_*h_*′)′+ax²h_*=1` there. The flux is zero both at `x=0` and `x=R`, so neither the cusp of `h_*` nor its change of slope at `R` creates a point source. Outside the support, `ax²h_*=1`. The negative half-line follows by symmetry. This proves the equation distributionally on the whole line.

The needed integrals are

\[
 \int_0^1p(y)dy=\frac3{20},\qquad
 \int D_*dx=\frac{3aR^5}{80}=M,
\]

\[
 \int_{|x|<R}h_*dx=\frac{10}{aR},\qquad
 \int_{|x|>R}h_*dx=\frac2{aR}.
\]

The energy components are `∫D_*h_*′²=12/(5aR)` and `∫ax²h_*²=48/(5aR)`, whose sum is `∫h_*`. Independent symbolic checks reproduced these identities and the exact unit PDE residual.

### Global certificate

The weak equation gives, for any compact smooth `f`,

\[
 2\int f-Q_{D_*}[f]=\int h_*-Q_{D_*}[f-h_*]\le\int h_*.
\]

Smooth cutoffs and mollification of `h_*` attain the upper bound in the limit. Therefore `J(D_*)=∫h_*`.

The field `h_*` is globally Lipschitz, with

\[
 c:=\|h_*'\|_\infty=\frac8{aR^3},\qquad
 |h_*'|=c\ \text{on }0<|x|<R,
\]

while outside the support `|h_*′|=2/(a|x|³)<c`. For every admissible `D`,

\[
 J(D)\ge2\int h_*-\int ax^2h_*^2-\int D|h_*'|^2
 \ge2\int h_*-\int ax^2h_*^2-Mc^2
 =J(D_*).
 \tag{4}
\]

Using `h_*` in this inequality is legitimate: truncate its integrable tail, then mollify. The derivatives can be kept bounded by `c+o(1)` and converge almost everywhere, so the `D` term converges by dominated convergence for every `D∈L¹`.

For equality, (4) first forces `D=0` almost everywhere outside `[-R,R]`, since the squared-slope inequality is strict there. It also forces `h_*` to maximize the quadratic functional for `D`. Variation by smooth functions yields `−(Dh_*′)′+ax²h_*=1`. On either open half-interval, the nonzero constant slope determines `D` by one integration. The flux must join the zero exterior flux continuously at `±R`; these conditions give precisely (2). This proves uniqueness almost everywhere.

As an independent sensitivity check,

\[
 \frac{dJ_{\min}}{dM}=-\frac{64}{a^2R^6}=-\|h_*'\|_\infty^2.
\]

The optimization is unrestricted apart from nonnegativity and the integral budget. A prescribed positive lower bound, pointwise upper bound, derivative penalty, or fabrication length changes the problem and is not included in the theorem. If strict positivity or smoothness is required without a fixed quantitative bound, the same value is an infimum: smooth positive integrable majorants of `D_*` can have total mass approaching `M`; normalizing their mass to `M` gives coefficients dominating `(1−o(1))D_*`, which squeezes their `J` to (3). Such restricted classes need not attain the infimum.

## A compact wall with one quadratic kinetic zero

Let `Γ` be a fixed smooth periodic one-dimensional wall, with arclength coordinate `s=0` at its only zero. Assume `k(s)>0` elsewhere, is bounded below away from every neighborhood of zero, and

\[
 k(s)=a s^2[1+o(1)]\quad(s\to0),\qquad a>0.
\]

Let `J_Γ(D)` be the periodic counterpart of (1), with `∫_ΓD=M`. No global positive mobility background is imposed. Then

\[
 \boxed{\inf_DJ_\Gamma(D)
 \sim C a^{-4/5}M^{-1/5},\qquad
 C=12(3/80)^{1/5},\quad M\downarrow0.}
 \tag{5}
\]

This is an optimum over all admissible placements, not merely over a family of prescribed shapes.

Fix a small local radius `r` and `η∈(0,1)` so that

\[
 a_-s^2\le k(s)\le a_+s^2\quad(|s|<r),
 \qquad a_\pm=(1\pm\eta)a.
\]

For the lower bound, use the whole-line certificate `h_*` for curvature `a_+` and budget `M`, multiplied by a smooth cutoff that is one on `|s|<r/2` and zero at `r`. For small `M`, all cutoff changes occur in its `1/(a_+s²)` tail. Their effect on `2∫h−∫kh²` is bounded independently of `M`, and their slopes are bounded independently of `M`. The large central slope `c∼M^{-3/5}` remains the global slope bound. Thus (4) yields, uniformly in the admissible placement,

\[
 J_\Gamma(D)\ge C a_+^{-4/5}M^{-1/5}-O_{r,\eta}(1).
\]

For the upper bound, place the exact coefficient (2), with curvature `a_-` and budget `M`, inside `|s|<R<r`, and use zero mobility elsewhere. Its zero endpoint flux makes the inside and outside variational problems independent in the natural form. Potential ordering bounds the interior contribution by `10/(a_-R)`. The exterior has no diffusion, so its contribution is exactly `∫_{|s|>R}1/k`, bounded above by `2/(a_-R)+O_r(1)`. Therefore

\[
 \inf_DJ_\Gamma(D)\le C a_-^{-4/5}M^{-1/5}+O_{r,\eta}(1).
\]

Divide by `M^{-1/5}`, let `M→0`, and then let `η→0` to prove (5). The weak Taylor assumption proves a relative asymptotic; it does not prove an additive bounded error between `J_Γ` and its leading term.

For comparison, distributing the same budget uniformly gives surface diffusivity `M/P` and hence the previously verified quadratic-zero law

\[
 J_\Gamma(M/P)\sim\mathcal C(0)a^{-3/4}P^{1/4}M^{-1/4}.
\]

Optimal placement therefore changes the divergence exponent from `1/4` to `1/5`. The ratio of the optimized value to the uniform value tends to zero as `M^{1/20}`. This is a slow asymptotic improvement, despite the exponent change; finite-budget benefits require quantitative evaluation.

## Several separated quadratic zeros

For finitely many zeros with local curvatures `a_j>0`, the leading budget allocation and minimum are

\[
 M_j=M\frac{a_j^{-2/3}}{\sum_i a_i^{-2/3}},\qquad
 \boxed{\inf_DJ_\Gamma(D)
 \sim C\left(\sum_j a_j^{-2/3}\right)^{6/5}M^{-1/5}.}
 \tag{6}
\]

The upper bound uses disjoint local designs with these budgets. The lower bound repeats the compactly supported dual tests independently around each zero. If `m_j` is the mobility budget in the corresponding fixed neighborhood, the sum of the local bounds is `Σ_j C a_{j,+}^{−4/5}m_j^{−1/5}−O(1)` with `Σm_j≤M`. Minimizing this explicit convex expression yields (6). A zero local budget gives an infinite local functional and is covered by a limit. The zeros must remain a fixed positive distance apart as `M→0`.

## Finite transverse bulk mixing

The exact Schur-complement identity in [the surface-exchange note](exploration-interfaces.md) continues to hold when constant surface mobility is replaced by `D(s)`. In its notation,

\[
 D_{\rm flow}(D)=B J_\Gamma(D)+\mathcal R(D),\qquad
 B=KV^2/Z,\qquad \mathcal R(D)\ge0.
 \tag{7}
\]

Take a fixed bounded connected smooth cross-section, fixed positive bulk diffusivity, square-integrable axial flow, and the constant-affinity exchange model. For the localized trial designs used in (5) or (6), the remainder is bounded independently of `M`. Consequently, for `V≠0`,

\[
 \boxed{\inf_D D_{\rm flow}(D)
 \sim B C\left(\sum_j a_j^{-2/3}\right)^{6/5}M^{-1/5}.}
 \tag{8}
\]

Here the infimum optimizes the full bulk–surface dispersion, which can have a different finite-budget optimizer from the scalar functional. Equation (8) follows by a scalar lower bound for every design and a full-bulk upper bound for the explicit localized trial designs. If `V=0`, this singular mechanism is absent and (8) is not an asymptotic equivalence for the residual bulk dispersion.

To check the upper bound, let `h=H_D^{-1}1` on the compact wall. Inside each trial support, comparison with the local quadratic field gives

\[
 0\le h\le h_{*,a_-},\qquad
 kh\le\frac{a_+}{a_-}\max_{0\le y\le1}y^2(9-8y)
 =\frac{27a_+}{16a_-}.
\]

Outside the trial supports, `D=0` and `kh=1`. Thus `kh` is uniformly bounded. The Poincare and trace bounds in the Schur-complement formula give `0≤\mathcal R(D)≤C_bulk`, independently of `M`. Positivity comparison can be applied separately on each local interval because the mobility has natural zero-flux endpoints.

In fact, along these trial designs the regular bulk remainder converges to the rate-independent zero-mobility bulk remainder. The bounded function `kh−1` is supported on intervals of total length `O(M^{1/5})`, so it tends to zero in `L²(Γ)`. This makes the bulk linear functional converge in its energy-dual norm. For every fixed smooth bulk test field `f`, the surface Schur penalty satisfies

\[
 0\le S_D[f]\le\int_\Gamma D|\partial_s f_\Gamma|^2
 \le M\|\partial_s f_\Gamma\|_\infty^2\to0.
\]

Dropping the nonnegative penalty proves the upper limit of the bulk supremum; inserting smooth tests and using density proves its lower limit. This establishes convergence. It does not assert a bounded gap between the optimized full dispersion and `B` times the optimized scalar functional for an arbitrary nonsymmetric rate profile.

## Scope and review status

The exact profile, constant, dual optimality proof, uniqueness, compact-wall leading optimum, multiple-defect allocation, and finite-bulk leading optimum have been independently derived in this review. The calculations use only the unrestricted integral mobility budget and the constant-affinity reversible model. The power of these conclusions depends on that design freedom; externally fixed backgrounds or fabrication constraints are separate problems.

The whole-line model is a local optimization model, not a normalized stationary system on an infinite wall. The compact-wall theorem supplies the physical connection. These results do not establish novelty in optimal conductivity, compliance optimization, optimal diffusion, or transport design literature. A publication claim must wait for that audit and further independent review of the extensions recorded here.

## Independently checked extension to any power-law zero

The parent subsequently proposed the following generalization. The reviewer independently checked its differential equation, nonnegativity, budget, integral, optimality certificate, and allocation exponents. Let `m>1` be any real exponent and replace `ax²` in the whole-line problem by `a|x|^m`. Define

\[
 R=\left[\frac{M(m+2)^2(m+3)}{a(m+1)}\right]^{1/(m+3)},
 \qquad y=|x|/R,\qquad
 c=\frac{m(m+2)}{aR^{m+1}}.
\]

The unique optimizer and its inverse field are

\[
 \boxed{D_*(x)=\frac{aR^{m+2}}{m(m+2)}
 [y-(m+1)y^{m+1}+my^{m+2}]\,\mathbf1_{y<1},}
 \tag{9}
\]

\[
 h_*(x)=
 \begin{cases}
 \bigl[(m+1)^2-m(m+2)y\bigr]/(aR^m),&y\le1,\\
 1/(a|x|^m),&y>1.
 \end{cases}
\]

The exact minimum is

\[
 \boxed{J_{\min}=\frac{m^2(m+1)}{(m-1)aR^{m-1}}
 =C_m a^{-4/(m+3)}M^{-(m-1)/(m+3)},}
 \tag{10}
\]

\[
 C_m=\frac{m^2(m+1)}{m-1}
 \left[\frac{m+1}{(m+2)^2(m+3)}\right]^{(m-1)/(m+3)}.
\]

For verification, put `p_m(y)=y−(m+1)y^{m+1}+my^{m+2}`. The factor `p_m(y)/y` decreases from one to zero because its derivative is `−m(m+1)y^{m−1}(1−y)`. Thus the coefficient is nonnegative. Directly,

\[
 p_m'(y)+y^m[(m+1)^2-m(m+2)y]=1,
 \qquad
 \int_0^1p_m(y)dy=\frac{m(m+1)}{2(m+2)(m+3)}.
\]

These identities give the weak equation and `∫D_*=M`. The inside integral of `h_*` is `(m²+2m+2)/(aR^{m−1})` and the outside integral is `2/[(m−1)aR^{m−1}]`, summing to (10). Fluxes vanish at the center and support endpoints. The global Lipschitz bound is `|h_*′|≤c`, with equality inside the support; outside it the slope is at most `m/(aR^{m+1})=c/(m+2)`. The same dual proof and uniqueness argument apply without change. The sensitivity identity is again `dJ_min/dM=−c²`.

The restriction `m>1` ensures integrability of the whole-line tail; no integer value or `C^m` assumption is required. The local condition needed to transfer the result to a compact wall is simply

\[
 k(s)=a|s|^m[1+o(1)]
\]

at an isolated zero, with positive lower bounds away from its neighborhoods. The preceding cutoff and potential-ordering proof then gives (10) as the leading compact-wall optimum. A uniform budget placement has exponent `−(m−1)/(m+2)`, whereas the optimum has exponent `−(m−1)/(m+3)`.

For finitely many separated zeros with the same order `m` and coefficients `a_j`, the optimal leading allocation is

\[
 M_j=M\frac{a_j^{-2/(m+1)}}{\sum_i a_i^{-2/(m+1)}},
\]

\[
 \inf_DJ_\Gamma(D)\sim
 C_m\left(\sum_j a_j^{-2/(m+1)}\right)^{2(m+1)/(m+3)}
 M^{-(m-1)/(m+3)}.
 \tag{11}
\]

This follows by minimizing the sum of the local values (10) under the budget constraint. The finite-bulk proof also extends: on the local model,

\[
 \max kh_*=(m+1)\left(\frac{m+1}{m+2}\right)^m,
\]

so potential comparison bounds `kh` uniformly on the localized trial designs. Their support length tends to zero, and their bulk remainder again remains bounded and converges to the zero-mobility bulk remainder. As before, a separate review of the localization and bulk extension is appropriate; the whole-line general-power formulas have been directly independently checked here.

## Corollary: joint optimization when surface diffusion is isotropic

There is an additional physical cost if the same surface diffusivity acts both along the perimeter and along the channel axis. In a translationally invariant channel, let the surface generator contain

\[
 \partial_s(D(s)\partial_s)+D(s)\partial_x^2.
\]

The equilibrium surface measure remains `K ds/Z`. The longitudinal Brownian contribution is therefore `(K/Z)∫D=(K/Z)M`. Its noise has zero quadratic covariation with transverse motion, so it adds to the flow contribution. With a fixed bulk longitudinal molecular diffusivity, the total coefficient is

\[
 D_{\rm eff}=\frac{A D_b^x}{Z}
 +\frac KZ\bigl[M+V^2J_\Gamma(D)\bigr]+\mathcal R(D).
 \tag{12}
\]

The remainder is the same nonnegative bulk-flow term as in (7). A fixed anisotropic relation between longitudinal and transverse surface diffusion would change the budget cost; (12) specifically assumes equal diffusivities.

For the exact whole-line quadratic model, optimize both placement and total budget. From (3), minimizing `M+V²J_min(M)` gives

\[
 R_*=2\left(\frac{|V|}{a}\right)^{1/3},\qquad
 M_*=\frac65a^{-2/3}|V|^{5/3},\qquad
 V^2J(D_*)=5M_*.
\]

Consequently,

\[
 \boxed{\inf_{D\ge0}\left[\int D+V^2J(D)\right]
 =\frac{36}{5}a^{-2/3}|V|^{5/3}.}
 \tag{13}
\]

The coefficient itself is still (2), evaluated at `R_*`. An equivalent global certificate is the slope constraint `|h′|≤1/|V|`: for every such field,

\[
 \int D+V^2J(D)
 \ge V^2\left(2\int h-\int ax^2h^2\right)
 +\int D\bigl(1-V^2|h'|^2\bigr).
\]

At the proposed optimum, the last term vanishes and the inequality is saturated. Thus joint optimization is not merely a stationary-point calculation. The case `V=0` has the zero-mobility optimum and is interpreted directly rather than through the displayed slope constraint.

On a compact wall with one quadratic zero, (13) becomes a weak-flow asymptotic. Specify a fixed velocity shape `u_0` with nonzero cross-sectional mean and let `u=εu_0`, so `V=εV_0`, with `ε→0`. Fixed positive bulk diffusivity and all other model data are held fixed. Then

\[
 \boxed{\inf_DD_{\rm eff}
 =\frac{A D_b^x}{Z}
 +\frac{36K}{5Z}a^{-2/3}|V|^{5/3}[1+o(1)].}
 \tag{14}
\]

For the upper bound use the localized profile with `R=R_*`. Its bulk remainder is `O(ε²)`, which is smaller than `ε^{5/3}`. For the lower bound, nonnegativity of the remainder reduces the problem to the scalar objective. The explicit trial has cost `O(|V|^{5/3})`, so any potentially better design has `M=O(|V|^{5/3})→0`. Apply the compact-wall lower asymptotic (5) and minimize `M+V² C a^{−4/5}M^{−1/5}` to recover (14). The leading budget is `M∼M_*`; this also follows by rescaling that strictly convex one-variable objective. General local Taylor remainders justify the displayed relative error, not an additive `O(ε²)` error for the entire optimized excess.

If mobility is instead constrained to be uniform, optimizing its magnitude balances `M` against `V²M^{−1/4}` and gives excess of order `|V|^{8/5}`. Spatial placement therefore changes the optimized weak-flow exponent from `8/5` to `5/3`. Small mean velocity by itself is insufficient for (14): the complete flow amplitude must become small as specified, since a fixed strong zero-mean shear can retain a substantial bulk dispersion term.

This corollary and its constants were independently checked after the parent proposed them. It is an application of the principal placement theorem, with the same unresolved literature-novelty boundary.
