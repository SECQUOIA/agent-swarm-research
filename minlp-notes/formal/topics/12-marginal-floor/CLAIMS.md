# Sharp marginal-floor multilinear gaps: claim inventory

Source: [the result note](../../../results/positive-multilinear-marginal-floor-gap.md).
This inventory fixes the full mathematical scope. It is not a verification
record: an obligation is complete only when the coverage map names a checked
declaration proving it with the stated hypotheses. Existing foundations below
are reusable; they do not already prove the new floor-dependent theorem.

Throughout, `T` is the sum of the individual monomial graph-hull widths and `H`
is the actual polynomial graph-hull width on the original box. The unit-cube
result quantifies over every finite coordinate set, finite support family and
nonnegative coefficient family. Allowing zero coefficients is harmless and
covers the stated positive-coefficient class by deleting zero terms. Constants
and affine terms are allowed and have zero width. Ratios are formed only when
`H > 0`; the multiplicative inequality must also cover `H = 0`.

## Definitions and foundational obligations

| ID | Mathematical obligation | Existing support / remaining bridge |
|---|---|---|
| MF-01 | Define the set of actual ratios with `0 < δ < 1`, cube means `x_i ≥ δ`, and `H > 0`; define `C(δ)` as its supremum over all finite dimensions and degrees. | Follow `degreeRatios` and `degreeSupremum` in [Suprema.lean](../../Formal/MultilinearGap/Suprema.lean); the floor class is new. |
| MF-02 | Prove the ratio class is nonempty throughout `0 < δ < 1`, and bounded above before using real `sSup` inequalities. | A single bilinear monomial at both means `(1+δ)/2` gives a positive-width ratio equal to one; the finite theorem supplies boundedness. |
| MF-03 | Increasing the floor shrinks the ratio class, so `C` is antitone on `(0,1)`. For `δ > 1/2`, deduce `C(δ) ≤ C(1/2)`. | New set-inclusion and conditional-supremum argument. |
| MF-04 | Individual gap equals `min(u,S)` for a minimum-mean anchor `u` and the sum `S` of all other failure means, including singletons; empty terms have zero gap. | `monomial_hullGap_of_min_coordinate`, `monomial_hullGap`, `empty_monomial_hullGap` in [MonomialEnvelope.lean](../../Formal/MultilinearGap/MonomialEnvelope.lean). |
| MF-05 | The common threshold law simultaneously attains the upper envelopes of all nonnegative monomials. The polynomial hull gap is the maximum weighted expected anchor deficiency over laws with the required means. | `positive_polynomial_maximum_general`, `coupling_gap_bound_general` in [GeneralGaps.lean](../../Formal/MultilinearGap/GeneralGaps.lean), together with endpoint attainment in [Attainment.lean](../../Formal/MultilinearGap/Attainment.lean). The bound needs only the inequality; an explicit maximum formulation covers the source's stronger prose claim. |
| MF-06 | All anchor deficiencies are nonnegative for every admissible law; summing and mixing cannot lose the guarantees assigned to other term classes. | `monomial_deficiency_nonneg` and the law-mixture identities. |

## Finite upper bound and common law

For `0 < δ ≤ 1/2`, set

```
B = max 2 (log (1/δ))
τ = δ/B²
L = log ((1+τ)/τ)
κ = 2/(1-exp(-1))
I = ∫ z in 0..1, 1-exp(-1/(L*(z+B⁻²)))
```

| ID | Mathematical obligation | Existing support / remaining bridge |
|---|---|---|
| MF-07 | `B ≥ 2`, `τ > 0`, `L > 1`, `κ > 0`; the integrand defining `I` is continuous on `[0,1]`, and `0 < I ≤ 1`. | New scalar analysis. Positivity of `easyConstant = 1-exp(-1)` is already proved in [EasyTerms.lean](../../Formal/MultilinearGap/EasyTerms.lean). |
| MF-08 | `h(t)=1/(L*(t+τ))` is positive and integrates to one on `[0,1]`. Establish every integrability/measurability fact used below. | New shifted-density normalization. Existing `harmonicDensity` is a different function. |
| MF-09 | For every high-coordinate failure mean `0 ≤ p < 1/2`, `q_p=min(1,p*h)` satisfies `0 ≤ q_p ≤ 1`; its integral `m_p` satisfies `0 ≤ m_p ≤ p < 1/2`. | New clipping argument, using MF-08. |
| MF-10 | The correction coefficient `(p-m_p)/(1-m_p)` is well defined and lies in `[0,1]`; corrected `q'_p=q_p+((p-m_p)/(1-m_p))*(1-q_p)` lies in `[q_p,1]` and integrates exactly to `p`. This includes `p=0`. | New scalar completion identity plus integral linearity. |
| MF-11 | Low successes `1[t≤x_i]` and conditionally independent high failures with probabilities `q'_p(t)` define one finite Bernoulli law with exactly all required means. | [IntegratedLaws.lean](../../Formal/MultilinearGap/IntegratedLaws.lean) and threshold integrals in [Couplings.lean](../../Formal/MultilinearGap/Couplings.lean). The new law must be explicit and depend only on `x,δ`, not the objective coefficients. |
| MF-12 | For every finite set of high coordinates, with summed failure mean `S`, conditional union probability is at least `1-exp(-S*h(t))`. Handle separately the case some `p*h(t) ≥ 1`, where that failure is certain. | `prod_le_exp_neg_failure_sum` supplies the unclipped exponential bound. The clipped case is new and essential. |
| MF-13 | For a monomial with exactly one low coordinate of mean `u`, its expected deficiency is the integral over `[0,u]` of its conditional high-failure union. Consequently it is at least `∫₀ᵘ (1-exp(-S/(L*(t+τ)))) dt`. | Adapt `harmonicLaw_unique_low_deficiency` in Couplings; its current statement is specialized to the old harmonic law. |
| MF-14 | For `a ≥ 0`, `y > 0`, prove `(1-exp(-a*y))/min(1,y) ≥ 1-exp(-a)` by concavity for `y ≤ 1` and monotonicity for `y ≥ 1`. | New general scalar inequality; `one_sub_exp_neg_ge` illustrates the convex-exponential argument. |
| MF-15 | For each hard term, substitute `t=u*z`, use `u ≥ δ`, `ε=τ/u ≤ B⁻²`, and MF-14 to prove deficiency at least `I*min(u,S)`. Treat `S=0` without dividing by zero. | New substitution and integral comparison; the assertion is simultaneous for the law from MF-11. |
| MF-16 | Independent rounding captures at least `min(u,S)/κ` for every term with no low coordinate or at least two low coordinates, including zero-gap terms. | `independent_deficiency_high`, `independent_deficiency_second_low`, `bernoulli_easy_gap` in EasyTerms. Classify exactly `x_i≤1/2` as low; the threshold equality must be covered. |
| MF-17 | Mix the common law with independence in proportions `(1/I):κ`; means remain exact and every term receives deficiency at least its individual gap divided by `1/I+κ`. | Existing [Mixture.lean](../../Formal/MultilinearGap/Mixture.lean) gives three-component machinery; a two-component specialization suffices. Handle constants separately or use the general monomial-upper formulation. |
| MF-18 | For all nonnegative-coefficient multilinear polynomials and all means above the floor, `T ≤ (1/I+κ)*H`. Deduce `C(δ) ≤ 1/I+κ`; combine with MF-03 for finiteness on all `(0,1)`. | New terminal theorem combining the law with GeneralGaps. This must mention actual graph-hull widths, not an assumed surrogate objective. |

## Sharp asymptotics

All limits here are as the real variable `δ` tends to zero from above. A
sequence-only theorem at dyadic floors is insufficient without an interpolation
or floor-selection argument for every sufficiently small real `δ`.

| ID | Mathematical obligation | Existing support / remaining bridge |
|---|---|---|
| MF-19 | Eventually `B=log(1/δ)`; `B→∞`, `L=B+2*log B+o(1)`, `L/B→1`, `L/B²→0`, and `log L/log B→1`. | New real-parameter limits; existing [AsymptoticScalars.lean](../../Formal/MultilinearGap/AsymptoticScalars.lean) provides analogous logarithmic estimates. |
| MF-20 | Prove `I ≤ (1+log L)/L` by `1-exp(-a)≤min(1,a)`, replacing the shifted denominator by the unshifted one away from zero, and splitting at `1/L`. | New integral estimate. The expression `1/(L*z)` at `z=0` must be handled almost everywhere or by splitting; Lean defines division by zero, so the informal pointwise inequality cannot be used blindly there. |
| MF-21 | Prove `I ≥ log L/(L*(1+L/B²))-(L-1)/(2*L²)` by restricting to `[1/L,1]`, using `1-exp(-a)≥a-a²/2`, and integrating the reciprocal and reciprocal-square bounds. | New integral lower bound, with all denominator signs established. |
| MF-22 | Squeeze to obtain `I/(log L/L)→1`; then `(1/I+κ)/(log(1/δ)/log(log(1/δ)))→1`. | New scalar limit, including eventual positivity of the normalizing scale. |
| MF-23 | In the dyadic family with `ell≥1`, all coordinate means lie in `[2⁻ell,1-2⁻ell]`; coefficients are one. Its termwise gap is `ell` and its hull gap is positive in the range used. | Construction and positivity already exist; the explicit two-sided mean bounds are new. |
| MF-24 | Its actual ratio divided by `ell/log₂ ell` tends to one. | `tendsto_exact_family_ratio_normalized` in [ExactAsymptotics.lean](../../Formal/MultilinearGap/ExactAsymptotics.lean). |
| MF-25 | With `ell=floor(log₂(1/δ))`, eventually `ell≥2`, `ell→∞`, and `δ≤2⁻ell`; insert this actual witness into the floor ratio class. Prove `(ell/log₂ ell)/(log(1/δ)/log(log(1/δ)))→1`. | New real-to-natural floor estimates and composition of MF-24. Do not reuse the dimension-budget `witnessLevels` without proving it has these different properties. |
| MF-26 | Squeeze the actual supremum to prove `C(δ)/(log(1/δ)/log(log(1/δ)))→1`. | New headline theorem combining MF-18, MF-22, and MF-25. Upper and lower leading constants are both exactly one. |

## Two-sided strip and nonnegative boxes

| ID | Mathematical obligation | Existing support / remaining bridge |
|---|---|---|
| MF-27 | Define the strip ratio class and supremum for `0<δ≤1/2`; establish nonemptiness/boundedness and inclusion in the one-sided floor class. | New definitions and set inclusions. The strip is empty for `δ>1/2`; no supremum claim is intended there. |
| MF-28 | MF-25's selected dyadic witnesses also belong to the strip class; squeeze to prove the same normalized limit one for its supremum. | MF-23 supplies both inequalities. This does not assert equality of the two suprema for a fixed `δ`. |
| MF-29 | For a finite box `0≤l_i≤u_i`, affine rescaling preserves the actual polynomial graph-hull width, including fixed coordinates. | `boxHullGap_eq_of_mem` in [BoxTransfer.lean](../../Formal/MultilinearGap/BoxTransfer.lean). |
| MF-30 | Expanding each rescaled monomial gives nonnegative coefficients; the sum of the expanded individual widths is at least the original termwise width. | `boxPolynomialCoefficient_nonneg`, `supportPolynomial_box_expansion`, `boxTermwiseGap_le_expansion` in BoxTransfer. The inequality direction matters. |
| MF-31 | If every nonfixed coordinate satisfies `(x_i-l_i)/(u_i-l_i)≥δ`, choose a cube parameter above the floor mapping to `x`, and apply MF-18 to the expansion. Deduce the finite bound for the original, unexpanded termwise relaxation. | New floor-preserving choice of parameter and a floor-aware transfer theorem; the existing degree transfer alone does not state this result. |
| MF-32 | Cover boxes with some or all coordinates fixed, zero endpoints, zero expansion coefficients, constant/affine polynomials, and vanishing hull gap. | Assign parameter `δ` to every fixed coordinate and the usual quotient elsewhere. The existing box map already permits degeneracy, so explicit dimension-reduction machinery is unnecessary. |

## Suggested proof boundaries and review checks

Keep the new development under `Formal/MultilinearGap`, with modules separating
shifted density and marginal repair, the common-law finite bound, real-parameter
asymptotics, and the terminal supremum/box statements. The exact file names can
follow implementation needs. Reuse the finite-law and original-hull semantics
rather than creating a second probability or envelope framework.

`integratedBernoulli` requires probabilities in `[0,1]` for every real parameter,
although only `[0,1]` is integrated. Extend the shifted density outside that
interval, for example by evaluating it at a clamped parameter. Prove agreement
on the integration interval. The unextended rational formula is not globally
positive and therefore cannot directly satisfy that interface.

Review must specifically check the clipping branch, the exact marginal equality,
the quantifier saying one law handles every monomial, the zero-deficiency cases,
the real-floor interpolation, and fixed-coordinate normalization. Each is a
possible place for a formal theorem to become weaker than the written claim.
An assumed density normalization, assumed hard-term gain, or assumed asymptotic
estimate cannot replace the corresponding new proof while claiming full scope.

The source's novelty screen, review history, numerical experiments, and possible
publication priority are not Lean obligations. Neither the source nor this scope
claims a uniform bound from positive box endpoints alone, exact optimization or
separation, or an approximation guarantee for constrained MINLP.
