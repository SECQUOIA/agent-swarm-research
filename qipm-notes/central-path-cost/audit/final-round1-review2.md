# Independent final manuscript review 2, round 1

Verdict: **no major issue found; two minor scope/precision corrections remain.**

I reviewed the current complete manuscript, including `main.tex`, macros, every section and appendix, bibliography, README, figure generator and data, all four verification scripts, and the current 50-page PDF's extracted text and standalone figures. I did not read other reviewers' reports or edit manuscript files. The root reviewer is separately auditing every PDF page visually.

## Valid findings

### MINOR 1 — State the barrier class explicitly in the abstract's exact-geometry claim

Location: `main.tex:12–14`, starting “Distance from the analytic center is exactly Euclidean ...”. The corresponding first results item in `sections/00-introduction.tex` would benefit from the same explicit qualification.

The abstract first announces specified barrier metrics, then states exact spectral flattening and a convex scalar allocation without identifying which specified barriers have these properties. The paper subsequently considers normalized scalar barriers and coupled barriers too. The strict convexity argument for the one-multiplier allocation is proved for the standard logarithmic spectral barriers in Theorem 3.4; Section 7 deliberately uses necessary KKT conditions without asserting convexity for general normalized scalar profiles. The coupled metrics are not covered by the exact Euclidean spectral-distance theorem either. The phrase “For equal standard barrier scales” in the following sentence scopes the Gamma result, but does not clearly scope the preceding exact-geometry assertion.

Repair: begin the exact-geometry sentence “For the standard logarithmic barriers, distance ...”. Apply the same short qualification to the first results item's domain-wide exact-geometry statement. This is an abstract/introduction scope repair, not a defect in the theorem statements or proofs.

### MINOR 2 — Include integer rounding in the introduction's distance-to-move-count comparison

Location: `sections/00-introduction.tex:15–16`: “The minimum number of such moves is comparable to metric distance, with explicit constants depending only on R.”

Read literally as two-sided multiplicative comparability for arbitrary endpoints, this fails near zero distance. On the scalar interval with `b(x)=-log(1-x^2)`, a move from zero to any `t>0` with `sqrt(2)t<R` has minimum count one, whereas its distance is `rho(t) -> 0`. No constant depending only on R can bound one by a constant times that distance. The formal corollary in Section 2 correctly retains the ceiling/additive rounding step, so the results are unaffected.

Repair: say “Metric distance bounds the minimum number of such moves up to constants depending only on R and one rounding step,” or equivalent wording retaining an additive one. No change to the formal local-step result is needed.

## Mathematical assessment

I found no incorrect theorem or unresolved proof gap after rechecking the following:

- Exact real Hessian normalization for rectangular real/complex matrix balls and Jordan intervals, repeated spectral values, ambient-curve lower bounds, frame attainment, exact gradient parameters, and weighted target allocation.
- Weighted prefix sharpness and ordering, the scalar KKT dilation, the rational upper/lower certificate, and localization of **every** scalar maximizer. No uniqueness of the standard scalar maximizer is assumed.
- Finite-rank objective-distribution bounds and target certificates, dyadic bit complexity, actual terminal accuracy, and discrete clipped potentials with backward/arbitrary labels and growing tube radii. The finite-start conversion used for the three-scale comparison is consistent with the analytic-center statements.
- Normalized scalar regularity and endpoint asymptotics; the distinction between necessary allocation KKT conditions and convex allocation; the exact **relaxed** safe-scale envelope; and the unique maximizer proof for that envelope. The relaxed class now explicitly requires local absolute continuity. The fixed smooth-barrier theorem does not claim that its best constant equals the relaxed envelope. The nonmonotone construction keeps its growing scalar parameter visible.
- Canonical universal/entropic cube barriers and their normalization; spectral transfer without claiming scalar self-concordance automatically transfers to matrix spaces; the regular full-facet lower theorem; and the exact parameters of dense and radial coupled examples. The uniform radial endpoint and same-accuracy upper bounds and same-dyadic discrete separation have compatible constants and hypotheses. The vertex-singular illustrative restriction now states `r>=2`.
- Negative conjugacy and projection signs, classical full feasible gap-set bounds, product-ball cone barrier provenance and the `k=1` case, and all four endpoint contracts in the same-instance completion theorem. The full gap-set comparison is appropriately attributed to Nesterov–Todd, including their allowance for intermediate affine infeasibility.
- Weighted exposed-minor contraction with arbitrary auxiliary fibers, the operational cone dimension argument (including coupled barriers), grouped/packed affine Hessians, exact norm-tree parameters and both limiting constructions, and heterogeneous source weights. The entropy specialization now includes the common objective weight.

The paper's full structure is coherent: exact primal geometry establishes the benchmark; ordered activation quantifies centrality; barrier changes identify its scope; primal–dual completion changes the output contract; formulation results give conditional ways to preserve lower bounds. The conclusion retains those distinctions. The stated novelty is qualified and sufficiently specific; it does not present classical spectral calculus, Lorentz inequalities, canonical barriers, or the Nesterov–Todd gap-set theorem as new.

## Literature and reproducibility checks

I checked the new modern context against primary author/publisher sources:

- Allamigeon–Benchimol–Gaubert–Joswig, *Log-Barrier Interior Point Methods Are Not Strongly Polynomial*, [author PDF](https://www.cmap.polytechnique.fr/~gaubert/PAPERS/LogBarrier.pdf), [publisher record](https://epubs.siam.org/doi/10.1137/17M1142132). Its trajectory-neighborhood assumptions support the appropriately qualified introduction.
- Allamigeon–Gaubert–Vandame, *No Self-Concordant Barrier Interior Point Method Is Strongly Polynomial*, [author preprint](https://arxiv.org/abs/2201.02186). The manuscript limits its comparison to that prescribed path-following model.
- Allamigeon–Dadush–Loho–Natura–Végh, *Interior Point Methods Are Not Worse than Simplex*, [author-institution manuscript and journal metadata](https://ir.cwi.nl/pub/35755). The 2025 journal citation is consistent, and the paper correctly distinguishes its affine-segment/straight-line resource from fixed-radius Hessian movement.

These checks supplement the primary Nesterov–Todd/Nesterov–Nemirovski and canonical-barrier texts checked in my previous stage reviews. I found no citation or attribution correction necessary in this round.

All four current scripts passed under `/home/sgusev/miniconda3/envs/qipm/bin/python`. In particular, the exact Fraction certificate passed every rational/series/radical and every-maximizer check; the radial centers were solved independently of the asserted tangent formulas, with maximum relative finite-difference error approximately `1.23e-9`. I reproduced both figures in an isolated temporary directory; the eight-row CSV reproduced byte-for-byte. Its largest reported relative quadrature error estimate was `3.60e-12` (correctly described as an estimate, not a rigorous enclosure). Both figure captions accurately distinguish the displayed finite-start endpoint/central lengths from minima over complete target sets. The existing final TeX log contains no warning, undefined-reference, overfull, or underfull entry.

The two minor wording repairs above are sufficient from this reviewer's perspective. I do not recommend another mathematical development stage on the basis of this review.
