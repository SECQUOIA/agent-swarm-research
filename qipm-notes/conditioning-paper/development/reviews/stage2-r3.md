# Stage 2 independent review — reviewer 3

## Decision

No major mathematical, scientific, or attribution issues found. One minor notation issue should be corrected before later sections expand the use of both path parameters. Subject to that correction, Stage 2 is ready to proceed.

Reviewed `macros.tex`, all of `sections/02-setup.tex`, `sections/03-geometry.tex`, and `sections/04-widths.tex`, including the localization and canonical-constant arguments. The later introduction, classifications, spectra examples, solver consequences, and numerical evidence are intentionally outside this stage.

## MINOR — use distinct symbols for the two parameterized paths

Location: `sections/02-setup.tex`, lines 123–153, and the corresponding uses in the uniform-rate corollary and canonical-constant discussion.

The manuscript defines `x_F(mu)` as a function of the barrier parameter, then defines `x_F(g)` as a function of the primal gap using the same function name and the same scalar argument domain. This is understandable locally because the argument variable is named, but it creates an avoidable ambiguity when both parameterizations occur in the same display or when a numerical argument replaces the variable. For example, the existing corollary uses both `kappa_F(g)` and `kappa_F(x_F(mu))`, with the first also relying on an implicit gap reparameterization of the condition-number notation originally defined on points.

Action: keep `x_F(mu)` for the original path and introduce a distinct gap-parameterized point, such as `widehat x_F(g)=x_F(mu_F(g))`, together with `widehat H_F(g)` and/or an explicitly defined gap condition-number function. Apply the choice consistently. No theorem or constant needs to change.

## Independent mathematical checks

1. **Barrier facts and attained gaps.** The reciprocal square-root Hessian inequality follows from the stated third-derivative condition. Its upper-Hessian direction contradicts boundary divergence if a unit local direction exits before time one. The reciprocal-gradient integration gives semiboundedness with the correct sign. Dikin objective support is valid at every interior point. Differentiating centrality gives the positive gap derivative, and integrating `(1/g)' >= -1/mu^2` towards the analytic-center endpoint yields the stated lower gap bound. Existence uses compactness and a supporting affine lower bound on the barrier; the argument does not require a dual-feasibility assumption.

2. **Approximate containment.** For a unit local direction to the endpoint, the residual hypothesis gives `phi'(0)>=-rho`. Integrating the lower Hessian estimate gives `phi'(t)>=t/(1+t)-rho`. At `t0=(sqrt(nu)+rho)/(1-rho)`, its positive lower bound is `sqrt(nu)/(1+t0)`. Semiboundedness then yields exactly `(nu+2sqrt(nu)+rho)/(1-rho)`. The proof correctly treats an endpoint before `t0` separately and never differentiates at a boundary point.

3. **Difference-body and cross-barrier comparison.** The objective-decreasing sign of each closed Dikin vector supplies the inner inclusion even without centrality. The difference of two outer-contained sublevel vectors supplies the factor two. The Loewner directions and the constants attached to each barrier are correct. Dividing eigenvalue bounds gives the factor `16 C_F^2 C_G^2` in the condition-number comparison.

4. **Both spectral edges and the aspect ratio.** The longest chord from the iterate gives the stated minimum-eigenvalue bounds; objective support gives the maximum-eigenvalue lower bound. The homothetic copy of a fixed relative ball supplies the maximum-eigenvalue upper bound with the stated factor. The circumradius of the difference body equals the original sublevel diameter. Its centered inradius equals the minimum supporting-hyperplane width of the original sublevel, while its radial function is not generally its support function; the manuscript keeps this distinction correct.

5. **Uniform families.** Applying asymmetric containment at the analytic center and Dikin objective support proves `a_F>=Delta/(1+C_nu)`. The claimed common attained gap interval is therefore justified even for varying barriers with uniformly bounded parameters. The residual and instance-dependent constants are made explicit; the statement does not silently extend to arbitrary growing barrier parameters or residuals approaching one.

6. **Canonical specialization.** Centrality implies the existence of an equality multiplier because the gradient plus objective is orthogonal to the equality kernel; row independence is unnecessary. Pairing a fixed strict primal point with the positive dual slack bounds its largest coordinate or block eigenvalue. The complementarity identity and the direction of `g<=nu_can mu` give the stated optional upper conditioning constant. Strict complementarity is not being used implicitly.

7. **Localization.** Interpolating an optimum with a relative interior point gives a strict point below the prescribed compact level. A relative ball then exists inside that level. All reused containments are pointwise, and objective-decreasing rays remain bounded inside the compact lower sublevel. The proposition properly declines to assert existence of an unbounded-set analytic center or global path.

8. **Width profiles.** Both Courant–Fischer formulas are correctly written for increasingly ordered eigenvalues. Applying reciprocal-square inequalities gives the stated minimax profiles, and the subspace-intersection argument proves their ordering. At the extreme indices the radial profiles reduce to diameter and inradius. Directed exits have positive uniform lower bounds at a fixed interior point; their sign discontinuity does not obstruct the extrema argument. The longer-exit convention at objective-orthogonal lines correctly yields the exact longest-chord identity at the first index.

## Attribution and scientific scope

The geometry section explicitly credits the Xiong–Freund sublevel/Hessian antecedent and classical containment. The gap proposition expressly identifies its equivalence to Peña's gap parameterization. The manuscript does not claim first discovery of general inverse-square upper bounds, does not confuse Schur matrices with reduced primal Hessians, and does not infer runtime bounds from Euclidean eigenvalues. The Nesterov book locator is presented as Xiong–Freund's citation, while the actual constant used here has a self-contained proof. This is consistent with the source-access limits recorded in Stage 1.

No additional proof gaps or unsupported priority statements were identified in the authored sections.
