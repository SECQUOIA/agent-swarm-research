# Stage 2 independent review 4

**Verdict: no major issues found.** The new results have complete arguments in their intended parameter ranges. I identified one minor domain clarification. I did not read any other Stage 2 review reports or communicate with other reviewers.

Reviewed: all of `03-sharp-centrality.tex`, `03a-distribution.tex`, `03b-discrete.tex`, and `appendix-scalar-certificate.tex`; both verification scripts; the Stage 1 metric/allocation interfaces; source-map and literature additions; the final build log. Future sections and temporary front matter were excluded.

## Minor issue

- **Specify the positive parameter in the pointwise distribution inequality.** In `sections/03a-distribution.tex`, Proposition “Distribution law,” equation `eq:Q1` contains `Q_1(eta)/eta`, and the proof uses `z>0`, but the proposition does not explicitly say `eta>0` for this first inequality. The subsequent length inequality explicitly allows its lower endpoint to be zero, and the central path includes the analytic center, so the distinction deserves one phrase. Repair: write “For `eta>0`, ...” before the first inequality, or define its value at zero by continuity. The latter limit is `sum_i w_i`. This is a minor domain issue, not a problem with the estimate.

## Detailed mathematical assessment

### Weighted sharp constant and scalar dilation

- Independently checked the weighted prefix decomposition, the weighted Cauchy--Schwarz constant, and the endpoint metric equality. The signed Jordan ordering remains fixed within each factor, and equal scales inside each factor are used correctly.
- The sharpness construction has strictly decreasing `c_i=1/(sqrt(S_i)+sqrt(S_{i-1}))`, so it enforces the requested strict activation order even for arbitrary positive scales. Its approximation error is bounded for each fixed scale vector, and its endpoint distance is exactly `M Gamma`; the limiting ratio is `Gamma`.
- The scale-range identity is correct. For the adjacent-exchange proof, `u<=v`, `u+v>=T`, and `u,v<T` imply the claimed comparison of distances from `T/2`; concavity then has the stated direction. The separate zero-prefix case is necessary and is included.
- Differentiating the scalar profile gives the displayed velocity. Both integrable tail estimates and the constant-shift asymptotic are correct. The scalar ratio tends to one at both endpoints and exceeds one inside, which proves attainment without a uniqueness assertion.
- The allocation-to-central comparison correctly uses `eta=lambda/2`. It bounds each central transformed coordinate by the corresponding optimizer coordinate times `c_star`; the first accurate center occurs no later. The manuscript correctly does not claim that `c_star Gamma` is an exact arclength supremum.

### Rational scalar certificate

- Checked the identity `dE/dlog(y)=E-K` independently from `p=b' composed with rho^{-1}`. The comparison function for `K<1`, its squared-polynomial sign, the improved `K<107/200` region, and the integrated inequalities all have the correct direction.
- The strict upper proof handles `1<=E<=2` and `E>2` separately, with valid strict logarithm bounds. Attainment supplies the strict bound on the maximum, rather than only a pointwise weak supremum bound.
- The lower witness uses two different strict inequalities in the right order: `P(w_0)<Y(v_0)A(v_0)` forces `W(v_0)>w_0`, and the other inequality supplies the claimed ratio. The finite series tail is an upper bound and rational squaring is applied only to positive quantities.
- Ran `scripts/verify_scalar_certificate.py` with `/home/sgusev/miniconda3/envs/qipm/bin/python`. Every exact assertion passed, including the three stated margins and both series/radical enclosures. The script uses only exact arithmetic; its assertions reproduce the manuscript's finite certificate rather than replacing an analytic premise.

### Distribution, tails, and determinant bounds

- The scalar error and velocity constants are correct. The early-time integration, head/tail estimates, and the no-tail schedules retain the necessary `eta_f>=1` assumptions. The conic-gap paragraph concerns the primal projection and explicitly avoids inferring a dual movement bound.
- The logarithmic-allocation counterexample has precisely the stated multiplier. Its weights are decreasing, its target excludes zero, and its exact distance grows at least as `c sqrt(sum 1/i)`. The estimates show that both versions of the rank certificate vanish: the stronger version requires sufficiently large rank and the proof states this.
- The compressed determinant argument is sound: after an orthonormal change of basis, the compression is principal; the complementary Schur complement is matrix concave; negative log determinant is convex and order reversing. Its Hessian comparison and pulled-back gradient estimate follow. Hadamard and the objective residual bound then give the factor-two certificate.
- The geometric and polynomial decay statements explicitly require enough channels as accuracy varies. Their lower bounds use indices inside the available range, while their upper estimates remain valid if the finite sequence is shorter than the preferred truncation. The polynomial upper bound integrates gradual activation and does not introduce an unproved logarithm improvement.

### Rational family and arbitrary finite sequences

- The dyadic data have the stated ordinary rational bit lengths. The rounding error is uniformly bounded; summation by parts prevents its accumulated contribution from spoiling the central-length lower bound. The two different ranges `i<=sqrt(r)` and `j<=r^(2/3)` serve the allocation and central-arc lower bounds respectively and are used consistently.
- The first accurate parameter window follows from the exact normalized error estimates, not from the surrogate central duality gap. The terminal coordinate and logarithmic target bounds have the correct direction.
- For the tube proof, clipping decreases the center-to-center distance because every transformed coordinate is increasing. The early thresholds have the necessary fixed separation; the potential uses only that early interval. The one-jump bound controls absolute changes and therefore allows arbitrary backtracking.
- Actual accuracy forces the terminal label beyond the clipping boundary. The initialization bound `P(s_0)<=Gamma_r delta_r/v_0=o(r log r)` follows under the stated growing-tube assumption. No prescribed endpoint labels are silently imported into this theorem. Allowing the analytic-center label `-infinity` correctly handles a zero-radius tube.
- The displayed divergent-ratio regime follows from the denominator `C_r sqrt(1+C_r)`, and the distinction between that regime and the broader admissible `delta_r=o(r^(2/3))` is retained.
- The decrement-to-tube proof derives the forward local norm bound from convexity and the one-dimensional self-concordant inequality; its restriction `beta<1/2` makes the segment estimate applicable. The restriction-of-covectors argument uses the right norm direction.
- The matrix/Jordan extension can indeed use the largest spectral coordinate for the terminal condition and spectral contraction for arbitrary intermediate points; it does not assume that the iterates share the objective's frame.
- The unequal-scale construction intentionally has an additional parameter-crossing assumption. Each disjoint core has a uniformly positive fraction of `H_0` as its coordinate gain. A permitted jump cannot cross three cores in positive length, and the two-coordinate estimate is bounded by `sqrt(2) C`. The fixed-endpoint comparison is thus valid without an objective-accuracy claim.

As additional numerical checks (not proofs), the standard-geometry script passed its 80 weighted cases, exhaustive five-channel permutations, sharpness convergence, and 401 scalar bounds. Independent exact-rational dyadic construction at ranks 32, 128, 512, and 2048 gave first-accuracy offsets between -0.038 and 0 and early-threshold gaps greater than `log(2)`, consistent with the asymptotic argument.

## Attribution, completeness, and build

The Lorentz attribution is appropriately limited to the classical decreasing-rearrangement norm/prefix inequality; the translated-profile realization remains a separate theorem. The text retains the Stage 1 Nesterov--Todd and Nesterov--Nemirovski distinctions and makes no unjustified broad priority claim. The audit transparently records the additional primary-source screen and the later-stage attribution issue for primal--dual gap sets. I found no mandatory literature correction within the completed Stage 2 scope.

The final LaTeX log reports a 20-page output with no undefined references, warnings, or overfull boxes. I did not rebuild in the shared output directory. The proof order and cross-references are coherent. No mandatory substantive omission was identified in the Stage 2 developments listed in the source map.
