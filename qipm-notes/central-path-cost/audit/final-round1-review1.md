# Final full-manuscript review 1

**Verdict: no major issues and no minor issues requiring correction identified.**

I independently reviewed the complete current manuscript, including the abstract and introduction, every section and appendix, the bibliography, figure definitions and data, the verification scripts, and the standalone build instructions. I did not read other reviewers' reports or modify manuscript sources. This report also serves as the Stage 5 review. It does not treat any part of the manuscript as an excused future stage.

The manuscript now states a coherent collection of results with a reasonably precise boundary between classical ingredients and its contributions. Its most substantial arguments have complete proofs rather than numerical evidence in place of proofs. I found no unsupported inference from path length to finite-step lower bounds, no remaining mismatch between the weighted and unweighted metrics, and no unqualified claim that its constructions establish iteration lower bounds for an arbitrary interior-point algorithm.

## Mathematical review

### Foundations, exact distances, and allocation

I rechecked the normalization of self-concordance, the real Hessian convention for complex matrix spaces, the local chord estimates, and the conversion between intrinsic distance and bounded local moves. The hypotheses needed for this conversion are now present. Spectral lower bounds and radial upper bounds agree, including the factor from Hermitian dilation, rectangular zero singular values, and repeated spectral values. The Jordan argument accounts for the Peirce off-diagonal spaces and uses an a.e. eigenvalue argument rather than assuming simple spectra throughout a path.

The exact distance-to-accuracy problem has the correct active coordinates, objective signs, and range of accuracy. Its convexity/uniqueness statement is justified for the particular flattened logarithmic barrier. The general normalized scalar-barrier section does not inherit that convexity or uniqueness without proof; it only uses necessary optimality conditions there. The exact and logarithmic-surrogate allocation statements have consistent parameter and metric normalizations.

### Weighted centrality and scalar certificates

I rederived the prefix decomposition underlying the weighted active-rank functional, including the scale-dependent activation order. The proof bounds the norm of a sum by the sum of prefix norms, and the integration increments telescope to the stated functional. The limiting separated-activation construction establishes the stated fixed-order sharpness. The adjacent-exchange argument also gives the claimed extrema over the order of the scales. Ties do not create an undefined choice or affect the asserted conclusions.

The scalar same-accuracy comparison has the correct factor relating the optimal allocation multiplier to the comparison central point. The manuscript distinguishes the sharp scalar constant from a claim of sharpness of its product with the active-rank bound. The rational appendix establishes the advertised upper and lower bounds and localizes every maximizer; it does not assert uniqueness of the scalar maximizer. Its endpoint exclusions and stationary equation cover the entire permitted domain. The separate relaxed normalized-barrier constant has a different definition and a proved unique maximizer. These constants are not conflated.

The numerical-rank and tail results retain the necessary distinction between an exact active-rank theorem and sufficient spectral-tail schedules. The conic transfer explicitly identifies the induced barrier and scale. The determinant/rank-profile certificate and the family separating it from the exact distance are compatible with the earlier exact formulas.

### Finite sequences and barrier dependence

The dyadic instance is an exact rational family, with rounding controlled in the proof rather than silently replaced by continuous activation times. Its bit estimate and asymptotic length scales use the same family. The finite initial center, the interval containing the first accurate central point, and the gap at the constructed terminal time are consistent.

The growing-tube argument applies to arbitrary center labels, including the initial convention at minus infinity. Endpoint feasibility forces potential progress. Bounded moves limit that progress locally, so the lower bound is genuinely a finite-sequence statement, not merely a restatement of central arclength. The dependence on tube width and the range in which the ratio diverges are consistent. The unequal-scale statement correctly specifies its weighted metric and its narrower endpoint comparison.

For normalized scalar barriers, the normalization, full positive gradient range, and tail estimates support the ordered-profile argument. The nonmonotone family satisfies the stated scalar assumptions and has the growing parameter required for the square-root-rank supremum. No fixed-parameter conclusion is improperly drawn from that family. The discussion of general spectral lifts expressly avoids inferring self-concordance from the spectral-distance identity alone.

For the coupled barriers, the facet-collar hypotheses give the claimed one-sided lower comparison. The radial family has a global diagonal-metric comparison and a separately proved bound on the change in its effective activation time; both are needed for the same-accuracy upper bound and both are supplied. Its constants are uniform over the advertised family. The full-family dyadic lower bound uses that uniformity. The vertex-singular example now has the necessary rank restriction and the unused-coordinate argument is consistent with its different parameter.

### Primal-dual geometry and formulations

The negative-pairing conjugate has the correct derivative and Hessian signs. The projector identity remains valid when equality constraints are rank deficient. The primal and dual progress formulas sum to the barrier parameter with consistent signs.

The full feasible-gap-set distance theorem is explicitly classical, and its domain permits intermediate affine infeasibility as stated. The three different movement scales use the same dyadic problem and a finite initial center. The full-gap endpoint argument controls an arbitrary accurate feasible endpoint, while the plotted exact endpoint quantity is correctly identified as an endpoint distance. The barrier with small primal motion permits positive, accuracy-dependent objective weights and has a unique optimizer; it is not incorrectly presented as a fixed-objective uniform limiting assertion.

The weighted Jordan support-minor bound retains every inactive fiber and has the correct inverse-scale factors in the dual norm and logarithmic gap. Its full-cone asymptotic matching does not claim an upper bound on an arbitrary affine slice. The arbitrary-cone dimension argument uses the operational minimal face and an explicit affine lift. The two-dimensional sections justify the parameter contribution, and the integer packing function has the advertised edge cases, including rays.

The grouped and PSD completion calculations retain off-diagonal curvature rather than replacing the full Hessian by its diagonal restriction. Exact parameters and centers agree with the Schur-complement calculations. The norm-tree domain has its positive-sheet conditions, its two possible root parameters have explicit upper and lower arguments, and the heterogeneous-weight entropy formula includes the common scale in the equal-weight specialization. The accuracy ranges in the resulting count comparisons are uniform as claimed.

## Prior work, novelty, and exposition

I checked the relevant primary sources during this review and the preceding independent stage reviews: the Nesterov--Todd primal-dual metric and gap-set results, the Nesterov--Nemirovski comparison theorem and spectral-norm-cone construction, Lorentz's norm inequality, the self-scaled-barrier classification, the infinity-norm-cone parameter lower bound, and the cited canonical cube barriers. Their use in the manuscript is consistent with their hypotheses and normalization. In particular, the optimal shared-coordinate product-ball barrier is not claimed as an original construction.

For the final introduction I additionally checked the primary accounts of the 2018 log-barrier lower bound, the 2022 arbitrary-self-concordant-barrier result, and the 2025 straight-line complexity result. The manuscript correctly separates their algorithmic/neighborhood complexity settings from its exact metric comparisons and bounded-local-move statements. Its novelty paragraph is qualified and enumerates concrete results; it does not claim that central-path metric inefficiency, general barrier-dependent complexity, or neighborhood lower bounds are new topics.

The abstract, introduction, body, figure captions, and interpretation section describe the same scope. Reader-facing definitions now cover the spectral/Jordan notation used in the proofs. The divisions between endpoint distance, an entire accuracy target, central arclength, tube counts, and full primal-dual gap reduction remain explicit at the points where they matter. I found no unresolved placeholder, missing theorem dependency, or contradictory quantifier requiring repair.

## Independent verification and reproducibility

I ran the complete advertised verification target with the qipm interpreter. All four verification scripts completed successfully, including the exact rational scalar certificates. I did not treat these successful runs as substitutes for the proof checks above.

I also performed checks independently of the author scripts:

- For all eight rows of `data/dyadic-lengths.csv`, recomputed the dyadic exponents using exact rational arithmetic and checked the stored endpoint and full primal-dual formulas. Independently integrated the primal central speed on a uniform 20,001-point grid; all comparisons agreed within relative error below `2e-6`.
- Solved 18 independently generated weighted allocation and first-accurate-center problems, including a tied-weight/tied-scale example. Checked feasibility, the componentwise scalar dilation comparison, and the resulting same-accuracy arclength bound using independent root finding and quadrature. All checks passed.
- Checked LaTeX label/reference consistency: 180 distinct labels and 230 resolved reference uses, with no duplicate labels or missing references.
- Inspected the current build log: a complete 50-page PDF, with no reported undefined references, multiply defined labels, warnings, or overfull boxes. I avoided a competing build in the shared output directory.

The figure program clearly separates exact formulas from numerical quadrature. Its data and captions do not present finite-size slopes as proofs of asymptotic theorems. The README distinguishes the optional Python diagnostics from compilation of the supplied manuscript and figure artifacts.

## Required corrections

None identified. This is a positive correctness and completeness assessment of the current manuscript, not a guarantee of journal acceptance or an assertion that no uncited related work exists.
