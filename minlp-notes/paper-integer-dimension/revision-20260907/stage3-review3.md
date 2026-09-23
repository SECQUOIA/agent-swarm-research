# Stage 3 independent review 3

**No supported major or minor issue identified.** No manuscript edits were made and no other stage 3 review or root adjudication was consulted.

## Coverage and mathematical checks

Read all 1,593 lines of the frozen `reviews/revision-stage3-round1/source/sections/03-scalar-nonlinear.tex`, including every proof, example, unnumbered estimate and computational qualification. Read the author/literature reports as leads. Used the previously independently checked parity, disjunction, covariance-volume and rational allocation lemmas as dependencies; their mathematical interfaces match the scalar section's uses.

The review reconstructed the chord refinement, maximal scalar packing and Jensen superadditivity proofs; both directions of the truncated-curvature comparison and its endpoint potential; the high-degree examples; indexed circuit compilation; signed-coefficient panel certification, root-separation termination, Gaussian error/conditioning and inverse quantiles; seven-bit and hybrid eleven-bit constructions; separable product packing; positive allocation; dense and sparse power constructions; relative-error obstructions; and both root-encoding results.

Particular checks for this review's supplemental lens:

- **Supporting scalarization:** strict positive feasibility supplies the normal-cone qualification. At positive coordinates unconditional downward closure forces nonnegative normal components; zero output rows can be removed from the normal without changing its supporting value. The scalarized allocation has the same optimum, and its multipliers and nonlinear homeomorphisms are used only in the lower proof. The algorithm does not require their computation or rational encoding.
- **Sparse polynomial input:** the layer curvature bound is uniform in numerical degree. The sparse implementation evaluates only listed exponents, uses common dyadic endpoint precision, and controls downward value error and upward chord error separately. Its explicit bands contain the exact graph and are dominated by the allocated unconditional error vector. The layer and cell index are the only integer coordinates.
- **Rational exponents:** checked both the integer rounded-power bisection and rational log/exponential series algorithm. The exact final power has numerical exponent `M=O(L)`, rather than the potentially enormous original exponent. For exponents approaching one, the scale `s=min(1,alpha-1)` appears in both allocation and precision; its logarithmic encoding cost is polynomial. Reversed or repeated inverse knots retain graph coverage through a continuous polygonal input path with exact endpoints.
- **Separable counts:** the incompatible product packing loses at most `6^r` in the sum model. Combining it with the three local cell bounds gives the stated finite, positive dense and general convex dense overheads; the proof never enumerates the packing.
- **Other delicate boundaries:** the signed-curvature quadrature proof does not use positivity of coefficients; zero curvature is handled before root arguments. Mass-accurate knots allow targets slightly above total mass. The root-MILP denominator lower bound is independent of the frozen integer witness magnitude. The conic-value gadget handles zero weight, and the repeated-square dual certificate cancels the intermediate coordinates with the claimed value.

No transfer from an existence theorem to a polynomial encoding claim was left implicit in these arguments. The reciprocal approximation explicitly permits numerical-degree cost, while the later sparse and rational-exponent algorithms establish the stronger encoding model separately.

## Independent source evidence

- Read the primary Sagraloff–Mehlhorn preprint, Theorem 36 on PDF p.41, from the cached original. Its integer-polynomial bit bound includes both root isolation and requested refinement; square-free preprocessing is explicitly present in the manuscript. Checked the version at https://arxiv.org/abs/1308.4088v2.
- Read the original Bonito–Pasciak manuscript, PDF pp.14–15, equation (37) and Lemma 3.4. Substituting `lambda=1/t` gives the credited positive resolvent terms. The scalar paper proves its own rational rounding and endpoint normalization rather than assigning those guarantees to this predecessor. Source: https://arxiv.org/abs/1307.0888.
- Read Avis et al., local extracted pp.7–8, Lemma 1 and its acyclic-gate proof: fixed Boolean inputs force Boolean internal values through continuous linear constraints, precisely the compiler's imported principle.
- Read Teles et al., original PDF pp.6–8 (printed 232–234), Remarks 1–4: radix disaggregation, recursive monomial products and truncation are accurately credited.
- Checked NIST DLMF Section 3.5(v), equations (3.5.18)–(3.5.20), for positive Gaussian weights and exactness: https://dlmf.nist.gov/3.5#v. The additional rational-conditioning argument is supplied locally.
- Read Wang's local discussion around Theorem 18, Remark 19 and Corollary 21: short conic power representations are established antecedents, consistent with the manuscript's limited attribution. The current LinA comparison now includes convex-corridor continuity and oracle work per segment, which this reviewer checked against its original PDF in stage 1.

These checks support the manuscript's precise contribution and computational-scope statements; they do not constitute a formal proof certificate or an exhaustive absence-of-prior-work claim. No numerical tests were needed to resolve a suspected defect, and no redundant test suite was added.

## Optional preferences

None required for acceptance.
