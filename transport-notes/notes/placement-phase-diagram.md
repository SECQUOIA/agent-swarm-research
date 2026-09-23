# Three phases of optimal mobility placement near a finite exchange-rate minimum

Research extension, 2026-09-06, verified within the stated mathematical model. The parent agent proposed the three-phase solution below; this note independently derives its nonnegative mobility profiles, exact objective values, global certificates and transition laws. A [separate independent review](review-placement-phase-diagram.md) confirms the formulas, completeness, uniqueness and physical optimum-value localization. Literature novelty is separate from mathematical verification.

The underlying transport model and budget-constrained placement result are documented in [optimal mobility placement](optimal-mobility-placement.md). Here both the spatial placement and total amount of mobility are optimized. A positive exchange-rate floor creates two transitions: mobility first appears in two patches away from the kinetic minimum, and those patches subsequently meet at the minimum.

## Dimensional and dimensionless problems

Consider the whole-line local rate k(s)=δ+as², with δ>0 and a>0. For a nonnegative integrable mobility D(s), define the scalar inverse functional by

\[
 J(D)=\sup_{f\in C_c^\infty(\mathbb R)}
 \left\{2\int f-\int[D|f'|^2+(\delta+as^2)f^2]\right\}.
\]

Infinite values are allowed; this variational definition avoids choosing an operator realization for every degenerate coefficient. The isotropic surface-transport objective is

\[
 \inf_{D\ge0}\left[\int D(s)ds+V^2J(D)\right], \tag{1}
\]

where V is the mean tracer speed. In the channel model, the surface contribution to total axial diffusivity is K/Z times this expression. The whole-line problem is a local design problem, not a normalized equilibrium model on an infinite wall.

Set

\[
 x=s\sqrt{a/\delta},\qquad
 D(s)=\frac{\delta^2}{a}d(x),\qquad
 \eta=\frac{|V|\sqrt a}{\delta^{3/2}}.
\]

Then (1) equals δ^{5/2}a^{-3/2} times

\[
 \mathcal F(\eta)=\inf_{d\ge0}
 \left[M(d)+\eta^2\mathcal J(d)\right],\qquad
 M(d)=\int_{\mathbb R}d(x)dx, \tag{2}
\]

\[
 \mathcal J(d)=\sup_f\left\{2\int f-
 \int[d|f'|^2+(1+x^2)f^2]\right\}.
\]

The dimensions are consistent: δ^{5/2}a^{-3/2} has dimensions length³/time, matching ∫Dds and V²J. Multiplication by K/Z, of dimensions inverse length, gives an axial diffusivity.

## Dual certificate and what must be checked

Write k(x)=1+x² and f(x)=1/k(x). For any integrable finite-energy field h with |h′|≤1/η,

\[
 M(d)+\eta^2\mathcal J(d)
 \ge\eta^2\int(2h-kh^2)
 +\int d(1-\eta^2|h'|^2)
 \ge\eta^2\int(2h-kh^2). \tag{3}
\]

Such a field is the weighted least-squares projection of f onto the Lipschitz constraint: maximizing the last integral is equivalent to minimizing ∫k(h−f)². No abstract minimax interchange is needed below. We give an explicit h and d that saturate (3) by satisfying

\[
 -(dh')'+kh=1,\qquad
 d\ge0,\qquad d(1-\eta^2|h'|^2)=0. \tag{4}
\]

The flux dh′ is continuous at every join and vanishes at the support endpoints. The fields have integrable tails, finite weighted energy and bounded derivatives. Cutoff and mollification justify their use in (3) for every d∈L¹. The weak equation gives 𝒥(d)=∫h. Thus (4) is a global optimality certificate, not only a stationarity condition.

## Phase I: no mobility

The maximum magnitude of f′ is 3√3/8, attained at x=±1/√3. Therefore

\[
 \eta_1=\frac8{3\sqrt3},\qquad
 0\le\eta\le\eta_1:\quad
 d_*=0,\quad h_*=f,\quad\mathcal F(\eta)=\pi\eta^2. \tag{5}
\]

The optimum is unique up to null sets. At the threshold, the complementary multiplier vanishes only at two points; these points cannot carry nonzero Lebesgue-integrable mobility mass.

## Phase II: two separated shoulder patches

For

\[
 \eta_1<\eta<\eta_2,\qquad \eta_2=\frac3{\sqrt2},
\]

let S be the unique solution of

\[
 \eta=S\left(1+\frac{S^2}{4}\right),\qquad
 \frac2{\sqrt3}<S<\sqrt2.
\]

Define

\[
 \Delta=\sqrt{3S^2-4},\qquad
 l=\frac{S-\Delta}{2},\qquad r=\frac{S+\Delta}{2}.
\]

On the positive half-line the optimum is

\[
 h_*(x)=
 \begin{cases}
 \dfrac{3S}{2\eta}-\dfrac x\eta,&l\le x\le r,\\
 \dfrac1{1+x^2},&x\notin[l,r],
 \end{cases}
\]

\[
 \boxed{d_*(x)=\frac14(x-l)^2(x-r)^2\,
 \mathbf1_{l<x<r}.} \tag{6}
\]

Extend both functions evenly to x<0. Mobility appears around the locations of the largest reciprocal-rate gradient, not at the kinetic minimum x=0.

The endpoint and zero-flux conditions give

\[
 l^2+4lr+r^2=2,\qquad l+r=S,
\]

and the endpoint chord slope is exactly −1/η. With m=S/2,

\[
 \eta[1-k(x)h_*(x)]=(x-l)(x-r)(x-m)=d_*'(x).
\]

Since h′=−1/η, this is (4). The quartic formula makes nonnegativity and zero endpoint flux explicit. The points l and r straddle 1/√3, and the derivative of f has magnitude below 1/η outside the active interval. Hence the global slope constraint holds.

The exact mobility mass and integrated inverse field are

\[
 M_* =\frac{\Delta^5}{60},\qquad
 J_* =\pi-2(\arctan r-\arctan l)+\frac{2\Delta S}{\eta}. \tag{7}
\]

Thus the exact parametric minimum is

\[
 \mathcal F(\eta)=\frac{\Delta^5}{60}+\eta^2
 \left[\pi-2(\arctan r-\arctan l)+\frac{2\Delta S}{\eta}\right]. \tag{8}
\]

## Phase III: the patches meet at the minimum

For η≥η₂, let R≥√2 be the unique solution of

\[
 \eta=\frac{(1+R^2)(6+R^2)}{8R}.
\]

Set C=R/η+1/(1+R²). Then

\[
 h_*(x)=
 \begin{cases}
 C-|x|/\eta,&|x|\le R,\\
 (1+x^2)^{-1},&|x|>R,
 \end{cases}
\]

and, with z=|x|,

\[
 \boxed{d_*(x)=
 \frac{z(R-z)^2(2Rz+R^2-2)}{8R}\,
 \mathbf1_{z<R}.} \tag{9}
\]

The coefficient is nonnegative exactly on this branch R≥√2. For R>√2 it vanishes linearly at the center and quadratically at the outer endpoints. Its support has two open halves whose closures meet at x=0; the value at the center is still zero. A statement that the optimizer becomes strictly positive across the center would be incorrect.

On 0<x<R,

\[
 d_*'=\eta[1-(1+x^2)(C-x/\eta)].
\]

Flux is zero at 0 and R. Therefore the cusp of h creates no point source. Outside the support, the reciprocal-rate slope satisfies |f′|≤1/η. The global certificate (4) holds.

The exact objective is obtained from

\[
 M_* =\frac{R^3(9R^2-10)}{240},\qquad
 J_* =\pi-2\arctan R+\frac{2R}{1+R^2}+\frac{R^2}{\eta}, \tag{10}
\]

\[
 \mathcal F(\eta)=M_*+\eta^2J_*.
\]

At η=η₂, R=√2 and C=1. The shoulder branch has l=0, r=√2 and yields precisely the same h and d. Thus the two formulas join without a discontinuity in the design or cost. Above the transition C<1, explaining the linear central mobility cusp through d′(0+)=η(1−C)>0.

## Completeness and uniqueness

Each η≥0 is covered by one of the three branches, and each branch has an admissible pair saturating the same global lower bound. Therefore no alternative number or arrangement of patches can improve the value.

For equality, (3) forces d=0 almost everywhere wherever |h′|<1/η. On each remaining open interval, h′ is a nonzero constant, and variation in h forces the distributional equation (4). Integrating that equation from the zero exterior flux uniquely determines d. In the central branch, continuity of flux at x=0 and nonnegativity of d force the center flux to vanish: h′ has opposite signs on the two sides. Thus no unaccounted integration constant remains. These conditions recover (6) or (9), proving uniqueness up to null sets.

Degenerate mobility may disconnect surface-diffusion paths at the center or patch endpoints. The variational statement does not require pathwise transmission there. Coupling to the mobile bulk still connects the physically sampled states. Requiring a strictly positive mobility floor, a bounded derivative, a maximum mobility, or a fabrication length changes the admissible class and the exact optimizer.

## Critical onset and large-η limit

As η decreases to η₁ from above,

\[
 \Delta^2\sim2\sqrt3(\eta-\eta_1),\qquad
 M_*\sim\frac{[2\sqrt3(\eta-\eta_1)]^{5/2}}{60}. \tag{11}
\]

The performance gain initially grows even more slowly. By the projection identity,

\[
 \pi\eta^2-\mathcal F(\eta)
 =\eta^2\int k(h_*-f)^2
 =2\int_l^r\frac{(d_*')^2}{1+x^2}dx
 \sim\frac{\Delta^7}{560}. \tag{12}
\]

To check the coefficient, put x=l+Δt. Then d′=Δ³t(t−1)(t−1/2), k→4/3, and ∫₀¹t²(1−t)²(t−1/2)²dt=1/840. Equations (11)–(12) give mass onset exponent 5/2 and benefit onset exponent 7/2. The small benefit close to threshold is a quantitative reason to avoid overstating the practical effect of first activating tiny mobility patches.

For η→∞,

\[
 R\sim2\eta^{1/3},\qquad
 M_*\sim\frac65\eta^{5/3},\qquad
 \boxed{\mathcal F(\eta)\sim\frac{36}{5}\eta^{5/3}.} \tag{13}
\]

This recovers the previously verified zero-floor joint-placement result after dimensional rescaling. The leading flow-induced cost is five times the mobility mass.

## Exact no-placement criterion in a finite channel

There is a direct finite-bulk interpretation of the first threshold. Suppose the full velocity field scales as u=εu₀, and take δ>0. Let f₀ be the unit-amplitude, rate-independent bulk Neumann corrector from the main theorem, with V₀=(∫Ωu₀)/Z. The no-surface-diffusion wall corrector is

\[
 h_0=\varepsilon\left(f_0|_\Gamma-\frac{V_0}{k_\delta}\right).
\]

For a nonnegative mobility perturbation m(s), the directional derivative of the total isotropic diffusivity at D=0 is

\[
 \frac KZ\int_\Gamma m(s)[1-|h_0'(s)|^2]ds.
\]

When h₀′ is bounded, convexity gives the exact criterion

\[
 \boxed{D=0\text{ is globally optimal precisely when }
 \|h_0'\|_\infty\le1.} \tag{14}
\]

In the well-mixed bulk model this reduces to |V|‖(1/kδ)′‖∞≤1. For kδ=δ+as² it gives η≤8/(3√3). Uniform-mobility optimization instead averages the squared wall-corrector gradient; unrestricted placement is controlled by its maximum. The f₀Γ term cannot generally be omitted in an exact finite-bulk criterion.

## Compact-wall and finite-bulk limit

For a fixed compact wall with one quadratic minimum, kδ=δ+k₀ and k₀(s)=as²[1+o(1)] locally, the whole-line diagram predicts the leading joint limit δ→0 and V=ηδ^{3/2}/√a, with η fixed. The entire imposed flow amplitude must scale with V; a fixed zero-mean shear is not included. The localization length is √(δ/a), and the predicted optimal mobility mass is O(δ^{5/2}).

The optimized surface excess satisfies

\[
 \inf_D D_{\rm eff}-D_{\rm base}
 \sim\frac KZ\frac{\delta^{5/2}}{a^{3/2}}\mathcal F(\eta),\qquad \eta>0. \tag{15}
\]

For an upper bound, place the exact local coefficient within the shrinking neighborhood, using potential comparison with nearby quadratic curvatures. Its kh field remains bounded, so the finite-bulk remainder is O(V²)=O(δ³), lower order than δ^{5/2}. For a lower bound, truncate the whole-line Lipschitz certificate inside a fixed local neighborhood and use it for every admissible D. The derivative of the cutoff tail is bounded, while the allowed physical slope 1/|V| diverges; the certificate remains feasible. Potential comparison followed by shrinking the local Taylor error gives the same leading value. This is the same controlled-localization mechanism as in the reviewed fixed-budget theorem.

Equation (15) concerns the optimum value. For a nonsymmetric finite profile, proving convergence of the complete optimizing coefficient requires an additional compactness or stability argument and is not claimed here. The transition locations and critical exponents above are exact for the quadratic local problem. Inferring a shrinking experimental critical window for a finite profile requires controlling its threshold shift and Taylor remainder. At η=0 the objective has the direct zero-mobility solution; an asymptotic equivalence to a zero leading term is not intended.

## Independent numerical checks

This agent solved the discrete weighted Lipschitz-projection problem directly, starting from f=1/(1+x²), without prescribing active intervals or using the analytic field as an initial guess. The interval was [−5,5], with equally spaced nodes; the objective was a rectangle-rule approximation of ∫k(h−f)² and every adjacent field difference was constrained by |h_{i+1}−h_i|≤Δx/η. SLSQP used the exact objective gradient.

| η | Nodes | Maximum field error at nodes | Discrete projection loss |
|---:|---:|---:|---:|
| 1.2 | 201 | 0 | 0 |
| 1.8 | 201 | 5.84×10⁻⁸ | 0.0003631697 |
| 1.8 | 401 | 2.11×10⁻⁷ | 0.0003630374 |
| 3.0 | 201 | 9.75×10⁻⁶ | 0.0385792564 |
| 3.0 | 401 | 7.13×10⁻⁶ | 0.0386087075 |

The small field error need not decrease monotonically because the analytic patch endpoints do not generally lie on grid nodes. These computations confirm the inactive, separated-patch and meeting-patch solutions through an optimization route distinct from substituting into the differential equation.

Separate 40-digit quadrature of the gain identity gave gain/(Δ⁷/560)=0.999783617 at η−η₁=10⁻³ and 0.999997835 at η−η₁=10⁻⁵. The ratio F(η)/[(36/5)η^{5/3}] was 0.98941697 at η=10³ and 0.99989353 at η=10⁶. These checks confirm the onset and large-η coefficients without subtracting nearly equal total objective values.

The separate reviewer also optimized the **primal mobility coefficient directly from zero**, using 1,200 finite-volume cells and a nonnegative face mobility. At η=1.4 it selected zero mobility; at η=1.8 and 3 it recovered the separated and meeting-patch profiles with maximum coefficient errors 4.64×10⁻⁶ and 1.11×10⁻⁵. Its [reproducible script](../scripts/check-placement-phase-review.py) and [review table](review-placement-phase-diagram.md) provide details. The parent's additional [phase checks](../scripts/check_placement_phases.py) are recorded in [JSON results](../results/placement-phase-checks.json). These optimization checks are distinct from direct substitution of the proposed solution into its equation.

## Novelty and remaining verification

The certificate is a weighted Lipschitz projection and has close connections to established optimal-conductivity and compliance-design methods. The [placement prior-art audit](optimal-mobility-placement-prior-art.md) is therefore essential. The generic dual method, concentration of mobility where gradients are large, and the existence of an optimization threshold are not broad novelty claims.

The candidate specific result is the complete finite-floor transport phase diagram: the two thresholds 8/(3√3) and 3/√2, the explicit separated and meeting-patch profiles, and the 5/2 and 7/2 activation laws. The [independent review](review-placement-phase-diagram.md) confirms the exact formulas, positivity, fluxes, global optimality, uniqueness, full-bulk no-placement criterion and compact/full-bulk optimum-value localization. This supports verified status within the stated model. It does not establish novelty, exact finite-profile topology, or the practical attainability of the unrestricted mobility designs.
