# Stage 4 independent review 2

Reviewed the frozen `reviews/revision-stage4-round1/source`: all 1,308 lines of `sections/04-vector.tex`, including every proof and example; the complete abstract, introduction, conclusion and bibliography; and the scalar, contact and rational-oracle dependencies used by this stage. I also read the author and literature reports as leads and compared the stage changes with the previous frozen source. I did not consult other Stage 4 reviews or edit the manuscript.

## Findings

No supported major or minor issues identified. No optional changes requested. The integrated claims retain the finite/algorithmic distinction, the dense-encoding and oracle hypotheses, and the input-dimension dependence of separable results. The unresolved one-input box question is clearly separate from the proved theorems. The blank author block is intentional and is not a finding.

## Coverage and decisive checks

- Reconstructed level refinement, finite cover trimming, common-partition rank selection with repeated endpoints, deterministic mass-query ordering, and the hybrid interval metadata. Common denominators combine only polynomially many fixed endpoint denominators and dyadic precisions. The potentially exponential number of cells is accessed by index rather than enumerated. The directed rounded bands retain both graph inclusion and the full output-error guarantee.
- Checked original-output curvature spanners, rational determinant exchange, box/facet scalarization, and the maximum-product allocation argument. Selecting original convex functions preserves nonnegative gaps despite signed representation coefficients. The approximate product solution's factor-seven support bound is sufficient for the stated compiler constant.
- Checked the fixed-grid feasible-spanner lemma in detail. Cofactors and the initial determinant bound every later objective uniformly. The chosen grid precedes all exchanges. Rounding followed by the displayed central repair produces an exactly feasible point, loses at most `1/4` in each signed objective, and gives a fixed polynomial-length denominator. Exchanges multiply the determinant by more than two; its fixed upper bound controls their number. Thus the proof controls total bit complexity, not just individual calls measured in a growing input.
- Verified the positive-polar separator's two outcomes. The support point is exactly in the original body; a violated support inequality therefore separates the whole positive polar. Otherwise division by `1+tau` gives an actual polar point within the declared distance. The explicit inner ball, coordinate bounds and independent seeds satisfy the spanner hypotheses. The pulled-back separator of the effective body is nonzero at exterior queries.
- Recomputed the effective-image inclusions and rounding budget. Rounding the coordinates of the nonlinear image, rather than arbitrary output coordinates, gives the required inner-band error. In the compiled oracle construction, the chord contribution is `13/64` of the inner polytope, rounding adds `1/16`, and the final half-polytope band gives `49/64`. No body-oracle constraint survives in the final MILP.
- Checked shared separable curvature rows, the product packing/deletion argument, and every finite and compiled constant in the separable table. Checked all power-layer thirds, cap-set and repeated-convexification arguments; all integer sections in the exact degree-32 product example; the hinge and Bernstein perturbation margins; nonconvex polynomial peak/trough separation; signed-polynomial overlays; tilted-body convexity and conditioning; and both box and Euclidean conditioning transfers. The counterexamples do not overstate a fixed-condition or one-input unconditional separation.

## Independent primary-source checks

Read the actual cached primary passages, not merely the author's audit:

- Awerbuch–Kleinberg, Section 2.3, Propositions 2.2/2.4 and determinant replacement proof (PDF p.4): exact spanners and optimization-based exchanges are established ingredients.
- Plevrakis–Hazan, published Section 3.3 (PDF p.8): approximate optimization combined with the inherited spanner construction is explicitly discussed. The updated published locator is correct; the [official proceedings page](https://proceedings.neurips.cc/paper/2020/hash/565e8a413d0562de9ee4378402d2b481-Abstract.html) confirms the authors and NeurIPS 2020 volume.
- GLS, printed p.172, Definitions (5)–(7), p.177 Theorem (3.1), and p.178 Corollaries (3.4)–(3.5). I also inspected the original page image: weak optimization compares against every point of the actual body, and the separator normal convention is norm **at least** one. Infinity-norm normalization and the one-dimensional padding used here satisfy those contracts.
- Lyu–Hicks–Huchette, Proposition 1 (preprint pp.7–8), explicitly merges breakpoints into one SOS2 formulation. The cited [version 2304.14542v1](https://arxiv.org/abs/2304.14542v1) was checked online. Kelly–Maulloo–Tan's logarithmic network objective and proportional-fairness inequality (printed p.239) support the attributed first-order principle.
- Ellenberg–Gijswijt, Theorem 4 and its proof (preprint pp.2–3), supplies precisely the imported monomial bound. Hartman's definition and framework (printed pp.707–708) and Averkov–Weismantel's Theorem 1.1 (preprint p.2) support the stated classical attribution and Helly qualification.

This is an independent mathematical and source review, not formal verification or a guarantee against every possible peer-review criticism.
