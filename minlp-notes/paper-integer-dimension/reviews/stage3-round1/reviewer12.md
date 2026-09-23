# Stage 3, round 1 — reviewer 12

Primary lens: relative-error boundaries, residue classes, zero endpoints, truncated domains, and one-sided scope.

Major findings: 0
Minor findings: 0

I found no concrete major or minor defect in the material reviewed. This is a bounded independent assessment, not formal verification, an exhaustive priority determination, or a guarantee that no defect remains.

## Snapshot and coverage

I read the entire 1,564-line `sections/03-scalar-nonlinear.tex`, the process/protocol, stage task and lenses, bibliography, and coverage inventory. I checked all eleven canonical stage-3 developments and the stated supporting developments against the manuscript. I rechecked the relevant accepted dependencies: graph containment and the distinction between convex integer and binary linear lifts; parity contacts; finite disjunction; bounded binary products and shared prefixes; covariance/volume bounds; unconditional domination; and the scalar specialization and central-ball repair of the rational log-determinant allocation oracle. I independently reviewed the complete first and second stages in earlier rounds; unrelated portions of those sections were not reread for this stage.

Every reviewed snapshot hash matched the corresponding working file:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

Original-source comparison included all of `notes/relative-power-graph-integer-obstruction.md`, the hybrid compiler's grid/greedy proof, the rational-power source's elementary log/exp algorithm, and the conic-value and repeated-squaring portions of `results/small-exponent-milp-soc-encoding-separation.md`. The remaining proofs were reconstructed directly from the manuscript; this review does not claim a complete rereading of all underlying result and audit files. Previous review labels were not accepted as mathematical evidence.

## Findings

None identified. I found neither a false assertion nor a concrete missing proof obligation warranting a numbered finding.

## Relative-error assessment

I checked `prop:relative-power` and `eq:relative-truncated-law` in full.

For convex powers, the selected modulus depends only on the fixed exponent and relative tolerance. With `M^p + 1` witnesses, two integer indices are congruent modulo `M`, so the combination with weights `1/M` and `1 - 1/M` has an integer index. The smaller input is at most `y/M`; hence the combination's input is at most `2y/M`, while its output is at least `y^q/M`. The resulting ratio exceeds `1 + eta` by the chosen modulus. The argument uses finitely many witnesses and requires neither measurability, closure, bounded integer ranges, nor an endpoint witness at zero.

For concave powers, the denser separation `x/y <= M^(-2)` gives the ratio upper bound `M^(q-1) + M^(-q)`. Both terms tend to zero for every fixed `0 < q < 1`, so every `eta < 1` is excluded. At `eta >= 1`, the hypograph restricted to nonnegative outputs is convex and gives exactly the stated zero-count convex lift. Adding only `(0,0)` preserves convexity and supplies the zero endpoint. The text does not confuse this with a zero-binary linear formulation.

The one-sided scope is correct: the convex-power contradiction requires only an output upper bound and therefore does not obstruct the exact continuous epigraph of a convex power. The concave-power contradiction uses an output lower bound; its zero-count hypograph construction is consistent with that distinction. The diagonal product and fixed-positive-denominator slice transfers preserve graph containment, the relevant relative inequality, and the integer dimension.

On `[a,1]`, all selected geometric inputs and their convex combinations stay inside the domain. Distinct residue classes force `M^p >= 1 + floor(log_M(1/a))`. The geometric rectangles satisfy both ratio bounds, and `1/(1+eta) >= 1-eta` for every positive eta. Their union has logarithmically many binary codes relative to its number of rectangles, giving the claimed double-logarithmic order. The statement asserts neither equal leading constants nor rational polynomial-time compilation for arbitrary real q. The zero-error case is correctly separated.

## Full-stage reconstruction

The scalar chord argument correctly uses endpoint midpoint errors on compact parity spans, then interval-cover trimming. The three-piece refinement and finite maximal-packing bounds do not rely on differentiability. Jensen superadditivity follows from domination of the disjoint smaller tent kernels; the separable packing uses index distance and a finite lattice-ball deletion bound, without enumerating the packing in the construction.

I checked the local truncated-mass estimate, the telescoping potential estimate, and the two curvature/allocation counterexamples. The mass inverse has an explicit positive rational conditioning scale away from both endpoints. The compiled mass-knot routine also treats targets beyond total mass; consecutive returned knots need not be monotone because their enclosed mass is controlled and the polygonal input path covers the interval.

The signed-curvature integration proof supplies both parts needed for polynomial complexity: only polynomially many failed panels at each depth, and a polynomial depth bound obtained from separation from complex roots. Subinterval disks remain within the certified parent disks. Gaussian positivity and exactness bound the quadrature error, while the explicit weight and derivative bounds control rational evaluation. I checked these analytic estimates from the proof but did not implement the complete adaptive integration algorithm.

The hybrid compiler's grid perturbation argument handles duplicate rounded knots by choosing the last original knot at a rounded left endpoint. Exact feasibility is monotone in the right endpoint, so greedy extension is legitimate. Failure to finish within `9D` cells gives the lower estimate needed to absorb all curvature-splitting pieces. The global index and fixed denominators avoid enumerating the potentially long local partitions.

The indexed compiler forces internal Boolean values only after external bits are integral, which suffices for the formulation. Its endpoint products use those forced values without new declared integers. The baseline powers, layer selectors, and sparse rounded-power constructions preserve graph containment and have the stated signs and error margins. The dense/sparse complexity distinction is maintained.

The supporting normal in the degree-independent lower bound can be made nonnegative using unconditionality; zero rows do not change its support value. The transformed supports are measured in their own cube, not assumed to preserve original volume. Supporting multipliers are proof devices and need not be found by the construction.

For inverse powers, the scaled Jensen inequality remains valid for `1 < alpha < 2`, including intervals touching zero. The first power-coordinate cell is handled separately from the bounded-curvature cells. The rational inverse algorithm has polynomial dependence on exponent bit length; its final exact powering exponent is only `O(L)`. The Stieltjes construction instead explicitly permits numerical-degree dependence. Its positive rational normalization gives exact endpoints, and the denominator bounds support the reciprocal gadgets without additional binaries.

The rational MILP encoding lower bound freezes an arbitrary integer witness but bounds only the basis denominator. A witness of large magnitude changes integer right-hand-side numerators and cannot evade that denominator bound. Splitting free variables and passing to standard form supplies an optimal basic solution without assuming a vertex of the original free-variable polyhedron. The four-binary upper has a constant number of coefficients, each of length `O(D)`.

Finally, the conic-value lemma handles zero interpolation weight explicitly. The repeated-squaring dual cone vectors cancel intermediate variables and telescope to the claimed objective difference. Their possibly long coordinates are witnesses rather than encoded coefficients. The MISOCP statement correctly distinguishes structured coefficient counts from sparse index encoding and does not claim a numerically stable or exact-output optimization algorithm.

## Primary-source and verification limits

I inspected the cached Sagraloff–Mehlhorn Theorem 36 for polynomial root isolation/refinement complexity after square-free preprocessing, and Simchowitz et al. Lemma 2.1 for the factor-two chord/midpoint comparison. Those locators support the uses made here. The accepted allocation oracle was rechecked directly in the current stage-2 section. I did not freshly verify every bibliography entry or every historical attribution, inspect the compiled PDF, or undertake a publication-priority search. Explicitly later-stage vector developments were not treated as missing stage-3 proofs.

## Executed independent check

I wrote and ran `verification/reviewer12-stage3-boundaries.py` using exact rational arithmetic. It checks the convex-power residue ratio for integer exponents, the concave-power ratio for square roots by squaring positive quantities, integer mixtures of congruent vectors including negative indices, the relative rectangle inequalities, and the four-binary root interpolation bounds by raising them to integer powers.

Result: **PASS — 200 convex ratios, 50 concave ratios, 131 residue mixtures, 1,134 rectangle error checks, and 1,680 root-cell bounds.** These finite checks supplement the general proofs and do not establish their universal quantifiers on their own.
