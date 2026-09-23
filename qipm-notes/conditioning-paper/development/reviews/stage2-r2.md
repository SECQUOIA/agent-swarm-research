# Stage 2 independent review — reviewer 2

## Decision

**No major issues identified.** I found no incorrect theorem, reversed matrix inequality, faulty minimax argument, or gap in the pointwise localization proof. One minor standalone-exposition correction is requested below. The mathematical stage can proceed once it is addressed.

Reviewed `macros.tex`, `sections/02-setup.tex`, `sections/03-geometry.tex`, `sections/04-widths.tex`, the author report, and the scope/literature record. The placeholder introduction, abstract and deferred example/algorithm sections are outside this stage review. Running `make -C conditioning-paper` succeeds and reports the PDF current.

## MINOR 1 — remove manuscript-provenance wording from the directed-exit introduction

Location: `sections/04-widths.tex`, first paragraph under “Directed exits and the sharper pointwise constant.”

The phrase “The original, center-dependent chord construction” refers to development history that a standalone reader has not been given. The following construction is fully defined and proved locally, so no historical reference is needed.

Fix: write “A center-dependent chord construction gives a second useful profile with the factor ...”, or refer explicitly to the earlier chord length definition. Keep repository provenance in the internal author notes. This is editorial and does not affect any theorem.

## Detailed mathematical checks

### Setup and standard facts

- The hypotheses exclude zero tangent dimension, a constant relative objective, singular tangent Hessians, and infeasible boundary optima. They fix the metric and unscaled Hessian consistently.
- The Dikin proof uses the upper bound on the one-dimensional second derivative only before the candidate first boundary time. If that time were less than one, two integrations would contradict barrier divergence. Closed containment follows because `P` is closed. The same proof remains valid when an exit time is infinite in the localization setting.
- The semiboundedness proof has the correct reciprocal-derivative sign. When the initial derivative is positive, convexity keeps it positive, and the barrier-gradient inequality forces its reciprocal to decrease at least linearly. Positivity before the endpoint gives the stated bound. No derivative at a boundary point is used.
- Objective support follows by minimizing the linear objective over the closed tangent Dikin ellipsoid. This is valid without centrality and correctly gives both the later maximum-eigenvalue lower bound and the gap differential inequality.

### Gap parameterization

- Compactness plus boundary divergence establishes existence of each minimizer; the positive-definite tangent Hessian gives uniqueness. Differentiating the stationarity equation yields the stated positive derivative of the gap.
- The endpoint arguments establish exactly `(0,a_F)`, including the nonconstant-objective argument that the analytic-center gap is strictly between zero and the full objective range.
- The integration of `(1/g_F)' >= -1/mu^2` gives `1/g_F(mu) <= 1/a_F + 1/mu`, with the direction shown in the manuscript. This proves the lower gap bound and the two-sided asymptotic gap–parameter relation without strict complementarity.
- The classical attribution agrees with the Peña Proposition 3.2 comparison verified in the Stage 1 repeat review. No novelty is assigned to this result.

### Approximate containment and difference bodies

- The normalized ray has initial derivative at least `-rho`. Integrating the lower Hessian inequality produces the displayed lower derivative bound. The choice `t0=(sqrt(nu)+rho)/(1-rho)` makes it positive; semiboundedness gives exactly `(nu+2 sqrt(nu)+rho)/(1-rho)`. The proof correctly splits off endpoints occurring before `t0`.
- Positivity of `mu` is stated and is essential when the objective-decreasing term is discarded. The residual is measured in the relative dual Hessian norm at the observed point, so the Cauchy–Schwarz step is justified.
- Only the objective-decreasing half of the Dikin ellipsoid enters `L(g)`. Symmetry of `L(g)-L(g)` recovers its full inner inclusion. The outer inclusion follows from subtracting the two translated containment bounds.
- At equal gap, `E_F ⊆ 2 C_G E_G` yields `H_G <= 4 C_G^2 H_F`. Interchanging the barriers gives the other displayed bound. The condition-number factor `16 C_F^2 C_G^2` follows correctly. The points need not have the same path parameter or position.

### Spectral edges, aspect ratio and uniformity

- The circumradius of the difference body is `D(g)`, not `D(g)/2`; the manuscript uses the correct factor. Its centered inradius is positive by the inner ellipsoid inclusion.
- Applying the ellipsoid sandwich separately to inradius and circumradius gives both aspect-ratio bounds. The one-sided chord construction sharpens the minimum-eigenvalue bounds from the difference-body constants to the claimed `C^2/ell^2` upper bound.
- Contracting a fixed interior ball toward an optimizer by `g/Delta` puts a ball of radius `rg/Delta` in the sublevel. Taking differences doubles that radius, which cancels the factor two in the outer containment and gives the stated maximum-eigenvalue upper bound.
- The support-function interpretation of minimum width is correct for a closed convex body. The objective-direction width is exactly `g/||c_V||` because the current point attains the upper sublevel objective and an optimizer attains the lower one.
- The analytic-center argument proves the newly explicit common interval for bounded-parameter barrier families. It uses the one-sided lemma directly with zero gradient, so no unavailable finite-parameter exact-center assumption is introduced. The residual-uniform and fixed-geometry quantifiers are correct.

### Canonical specialization and localization

- Strict primal feasibility supplies a positive lower coordinate/eigenvalue at a fixed feasible point. Centrality supplies a dual multiplier because the relative tangent is the equality nullspace. Complementarity then yields the bounded-slack estimate without requiring dual endpoint convergence. Squaring its norm and restricting the Hessian preserves the stated upper bound.
- Localization does not improperly import analytic-center or full-path existence. An interior point of a positive compact sublevel is obtained by interpolation from an optimizer to a relative interior point of `P`; a small relative ball lies inside that sublevel. The remaining proofs use closedness, compactness of the lower sublevel, and the same local barrier facts. Directed downhill exits are bounded because their entire feasible rays remain in that compact lower sublevel.

### Full-spectrum profiles

- The increasing eigenvalue order matches both displayed Courant–Fischer formulas. Applying the pointwise radial inequalities and taking positive reciprocal extrema yields the claimed `w_j^-` lower and `w_j^+` upper eigenvalue bounds.
- The subspace-intersection dimension argument proves `w_j^+ <= w_j^-`; the endpoint profiles correctly equal the circumradius and centered inradius.
- Directed exit times remain uniformly positive at a fixed interior point and uniformly bounded above by `ell(x)`. Thus the reciprocal minimax argument does not require their continuity. The equatorial sign convention is sufficient to identify the first directed profile exactly with `ell(x)`.

## Scientific positioning and completeness

The stage distinguishes its precise comparisons from established containment, gap parameterization, general conditioning bounds and the Xiong–Freund sublevel/Hessian analysis. It makes no exclusive priority assertion and does not overstate what the source-access record establishes. The revised general theorem strengthens the original canonical-only claim and incorporates observed-gap approximate centrality directly. Both original directed profiles and the new center-independent profiles are developed with proofs. I found no missing result needed for this stage's stated mathematical conclusions.

The subsequent stages should use these proved results without broadening them into invariant runtime claims or assuming the compact-sublevel localization supplies global path existence. Those boundaries are already stated correctly here; they are not additional corrections.
