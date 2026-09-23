# Independent Stage 1 review: fractional moments and full mathematical audit

Recommendation: accept Stage 1 after a minor clarification. **MAJOR issues: 0. MINOR issues: 1.**

I independently read `main.tex`, `sections/model.tex`, `sections/fractional-moments.tex`, `appendices/wellposedness.tex`, `references.bib`, and `development/COVERAGE.md`. I did not consult other current reviews or treat research notes as proof authority. The absence of material scheduled for later stages is intentional and is not a finding.

## Finding

**MOM-01 — MINOR — State the local loss-rate bound used in the comparison proof.**

Location: `appendices/wellposedness.tex:34–48`, equations `eq:signed-loss` and `eq:loss-duhamel`, and the “preceding setting” of `lem:weighted-comparison` at line 66.

The general signed-loss setting assumes only that the time integral of `a_s(x)` is finite for each fixed `x`. The displayed justification of the integrating-factor identity then restricts to `x <= R` and uses an integrable time bound for the multiplication operator. Pointwise time integrability does not imply that bound. For example, on `0 < x < 1`, set `a_s(x) = x^{-1} 1_{0<s<x}`, and set the rate to zero elsewhere. Every fixed-size time integral is at most one, but for `0 < s < R < 1`, the supremum over `0 < x <= R` is `1/s`, which is not integrable near zero.

This is a mismatch between the stated generality and the provided justification, not a counterexample to the integrating-factor identity or to the population theorem. The additive application does have the stronger bound, as the manuscript correctly observes at line 147. The comparison calculation and its application are sound.

Fix: include as an explicit assumption of the preliminary setting that, for every finite `T,R`, there is `h_{T,R} in L^1(0,T)` with `sup_{0<x<=R} a_s(x) <= h_{T,R}(s)` almost everywhere. This is the simplest repair and changes none of the applications. Alternatively, give a justification of the integrating-factor identity that handles the weaker pointwise assumption.

## Checked mathematical content

- **Pair inequality:** The reduction to `g(u) >= 1`, both endpoint values, the expression for the sign of `g''`, and the monotonicity of `R` are correct. The numerator of its final expression decreases because its exponent is greater than one; both denominator factors increase. Together with the endpoint derivative data, the one-change argument establishes strict interior inequality. Equality for positive sizes occurs precisely on the diagonal.
- **Fractional tests:** The bounded truncations are concave and subadditive. Their coagulation defects have the claimed uniform bound. The daughter lower bound follows from the decreasing ratio `f_R(z)/z`, and the upper bound follows from Jensen applied to `b_{t,x}/2`. The resulting space-time bounds need only locally bounded count and conserved finite mass. Monotone convergence on the left and dominated convergence on the right are justified without a second-moment assumption.
- **Controlled rates and normalization:** The count equation and the Radon–Nikodym derivative of mass sampling relative to number sampling have the correct factors. Differentiating the normalization gives exactly `-a_p b - a_{1-p} sigma`. The half-moment square has exponent `-kappa C`, with no missing factor of mass or two. Diverging total activity implies total-variation separation by the overlap inequality.
- **Sharpness:** Monodisperse initial data with equal splitting attain both instantaneous bounds. The claimed right derivative at zero is justified by weighted-variation continuity: the coagulation fractional-moment integrand is bounded by `xy^p + yx^p`, making its polarized functional continuous in that norm; equal-split fragmentation is a constant multiple of `M_p`. Setting either control to zero establishes separate sharpness. The text correctly limits this conclusion to uniform bounds with prefactor one, rather than claiming the best asymptotic exponent for a fixed model.
- **Critical consequences:** The critical exponent, its unique maximum at one half, both fixed-window bounds, and the two weak limits are correct. The moving-window limits use the correct endpoint slopes `log 2`, and may use different fractional orders for number and mass. The exclusion of the endpoint speed and the distinction between long-time escape and finite-time mass loss are appropriate.
- **Perturbed rates:** The lower coagulation bound has the correct sign because the fractional defect is nonpositive. The upper selection bound and the algebraic factorization of `gamma_p` are correct. Choosing `p` close to one proves the sufficient condition `s_* < 2am`. The argument makes no unwarranted claim of threshold optimality.
- **Existence and uniqueness:** Apart from MOM-01's general-lemma wording, the weak-kernel integral construction, positive majorant, weighted loss cancellation, polarization, and Gronwall estimate are valid. The cutoff Picard construction works with weak kernel integrals despite the absence of strong measurability of moving atoms. The second- and third-moment estimates, cutoff forcing bound, uniform stability coefficients, passage to bounded Borel tests, and subsequent initial-data truncation are coherent. Weighted-variation convergence preserves count and mass and handles merely measurable daughter kernels. No unsupported passage of such kernels through narrow convergence is used.

The two current literature descriptions are consistent with their primary sources: Cepeda treats a parent-independent law of relative fragment sizes and a homogeneity-moment framework, while Deaconu–Fournier–Tanré constructs the mass-weighted pure-coagulation process. I checked [Cepeda's text](https://arxiv.org/html/1301.1934v2) and the [Deaconu–Fournier–Tanré paper](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). Neither citation is being used to substitute for the manuscript's existence proof.

No additional mathematical defect or unsupported Stage 1 substantive claim was found. Adding a sentence about the sharpness example's right derivative would be an optional exposition improvement, not a separate issue.
