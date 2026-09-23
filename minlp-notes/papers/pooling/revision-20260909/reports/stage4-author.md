# Stage 4 author pass: standalone manuscript

Author development completed on September 9, 2026. This is the version for five independent Stage 4 reviews and subsequent separate correction. It is not an acceptance or external peer-review statement.

## Outcome and contribution hierarchy

The manuscript now leads with existential-real completeness, follows with restricted physical hardness and matched structural/contract algorithms, and treats response geometry and isolated rank-one costs/convexification as supporting contributions. The introduction explains the prior result, remaining issue, and specific advance, instead of repeating a fourteen-row inventory. Its seven-row table covers the physical classifications; the detailed contract table in Section 5 retains the individual hypotheses.

The degree comparison is explicitly feasibility versus feasibility with positive contracts allowed: degree-two products give polynomial feasibility, while degree-three products give strong NP-completeness for the same one-pool/two-feed/two-outlet interface and input-degree bound. The zero-lower-bound economic threshold result is distinguished as a further refinement. The overview consistently distinguishes actual mixing feeds from external bypass sources, total degrees from bypass degrees, NP certificates from polynomial algorithms, polynomial dependence for fixed parameters from FPT, and isolated matrix blocks from coupled physical pooling.

## Source and structural changes

Files developed:

- `sections/00-introduction.tex`: replaced abstract and introduction, shortened physical boundary table, explicit primary antecedent credit and new roadmap.
- `sections/06-synthesis.tex`: replaced the long technical catalogue by interpretation, supporting theorem conclusions, and the remaining degree-two question. Every retained mathematical claim points to a complete manuscript proof or a stated published result.
- `appendices/A-response-geometry.tex`: moved the former physical path, response, local/global geometry, LP hull, coordinate-port, dense-slab and arithmetic-limit proofs here, preserving stable labels and all claimed guarantees. Added a forward reference for the cost interaction-rank terminology.
- `figures/vertex-forcing-interface.tex`: new native TikZ diagram of the physical one-pool interface and its forced flows. It shows the sole undirected cycle and distinguishes sources, pool and products.
- `appendices/B-rank-one-costs.tex`: moved the complete fixed-interaction-rank, rank-one-cost and quality-multiplier oracle arguments; added complete general-cost hardness, unit-margin repair/penalty, rational-threshold certificate, quadratic-field optimizer, and fixed-dimension algorithm proofs.
- `appendices/C-rank-one-convexification.tex`: added complete correlation-face, affine inverse, exact conic transfer, nonpolyhedrality, quantitative rounding/slice transfer, approximate LP and shifted-slack SDP arguments.
- `main.tex`: includes the three appendices before the bibliography. The author block remains empty. No journal, submission, or acceptance metadata was invented.
- `bibliography.bib`: removed all thirteen unpublished-note entries; repaired Boveroux/LRS years and source-version metadata; added the published Jalilian–Kocuk article, Peeters and Gillis–Glineur.
- `README.md` and `source-index.md`: replaced stale completion/proof-dependency claims with current scope, review status, build requirements and exact disposition of all thirteen notes.

Sections 1–5 were not edited. Their source bytes match `revision-20260909/stage3-accepted/sections/` exactly. The shared `main.pdf` was not overwritten.

## Complete proof coverage

The full former Section 6 was read and analytically checked. Its retained proofs cover the following chains.

1. The telescoping sum is nonnegative exactly off the endpoint vertices; its exposing objective separates every vertex by its distinct last coordinate.
2. Capacity and midpoint quality rows give precisely the scaled Klee–Minty strips. Relay reset contracts copy the free flow, giving a two-quality physical realization.
3. Source/reset-throughput rewards use the already proved rational Hoffman bound to remove the linear contracts with polynomially encoded positive revenues. This exact penalty applies to the path LP, not to the nonlinear pool interface.
4. Distinct unique vertex optima give exponentially many affine price regimes. Boundary-sign arguments force distinct line factors in any quantifier-free formula in price and value alone. Neither statement limits compact extended representations or pointwise LP optimization.
5. Degree-two pool-free row support survives Fourier–Motzkin elimination, giving the individual-coordinate port obstruction, without restricting arbitrary linear images.
6. The physical interface is affinely parameterized by `(x,z)` with `z >= t-t^2`. Ordinary costs give exactly the stated vertex-forcing objective. Perturbation derivatives are strictly negative on every incident edge; the tangent cone argument transfers to physical coordinates.
7. The midpoint/parity argument gives the exact integer dimension of the finite optimal set; a binary-label convex hull attains the upper bound. The full feasible hull is instead an explicit polynomial LP, and an optimal *vertex* is physically feasible.
8. Three-quality relay and nongeometric supply extensions retain the exact identities. The lower-pool-contract deletion counterexample is retained, preventing an unjustified penalty extension.
9. The dense-slab reduction rounds endpoint bits with an explicit error, preserves nonempty compact domains, and uses polynomial-length padding for fixed local coefficients. It proves ordinary abstract NP-completeness, not strong physical path hardness.
10. The projected-box cost algorithm enumerates slice vertices through segments, minimizes each rational function in total mass, handles total zero and degenerate intervals, and recovers one quadratic field. Greedy scalar costs and quality-multiplier rank are proved separately.
11. The rank-one matrix-parameter two-LP argument and rank-two positive-product comparison retain their objective and dense-base-polytope scope. Convex quadratic singleton leaves encode Square-Root Sum; this is an arithmetic implication, not an NP-hardness claim.

Five formerly cited note results are now proved in the manuscript:

- General-cost biclique reduction: dummy margin totals decouple the two graph boxes, alternating linear minimization selects binary supports, and the nonedge penalty has an explicit no-instance gap.
- Unit upper/zero lower refinement: repair handles total mass below, at, and above one; an exact linear margin penalty shifts the optimum and retains strong hardness.
- Certificates/algorithms: paired box-slice vertex patterns give one quadratic field for an optimizer. Rational thresholds use minimization of a rational quadratic to obtain a rational witness; no rational-optimizer inference is made. One small dimension admits `d 2^d poly(m,n,B)` enumeration.
- Exact conic lower bounds: trace equality selects identical binary margins, the pair section selects complementary binary vectors, the total-mass section selects full paired atoms, and the affine inverse proves an isomorphism. Cone size transfers through sections and projections; scalar factors are counted. Nonpolyhedrality is proved directly.
- Uniform approximate bounds: the full rounding proof establishes the same `A_m=m(184m+6)` as previously quoted. The LP proof uses the published fixed-factor sandwich theorem. The SDP proof states the published quantitative pseudo-density inputs, proves the `q+1` valid-slack factorization with facial reduction and duality, shifts the centered-square slacks in sign coordinates, and preserves the logarithm in `exp(Omega((m/log m)^(2/13)))`.

No essential new proof is delegated to an unpublished companion note. Published algorithmic and extension-complexity theorems are explicitly identified as external established inputs; their full research proofs are not reproduced.

## Disposition of adjacent material

The original thirteen-entry source index was preserved as `reports/stage4-original-source-index.md`. The replacement index records original source paths, inspected SHA256 hashes, and the new manuscript location or removal reason for each entry.

Five rank-one notes were incorporated as described above. Eight unused adjacent model comparisons were removed: common-factor fixed linking, reciprocal-anchor one-leaf compatibility, full reciprocal-anchor separation, integer reciprocal-anchor separation, sparse network–simplex universality, cycle/theta network–simplex hulls, parallel-path subset cuts, and power-flow algebraic complexity. Their actual source models and claims were inspected for this disposition. None supplies a premise of a retained physical pooling or rank-one theorem. Their repository files remain unchanged. Removing these comparisons does not assert that the separate results are false; it avoids presenting unrelated, unproved-in-this-paper claims as manuscript contributions.

The global face penalty corollary from the stability note is not imported because it was neither claimed in the previous Section 6 nor needed for any retained result. The stronger direct slice-distance argument proves all previously stated approximation guarantees without it.

## Primary literature and novelty decisions

- Xiang et al. (IOS 2026, DOI `10.5281/zenodo.19984634`) are credited in the introduction for the existing product-LP zero-optimum test, including pool-to-pool arcs. The paper contributes a direct physical proof and its stated interpretation; it does not claim the first sign algorithm.
- The introduction credits broad one-pool capacitated hardness to Baltean–Lugojan and Misener, Remark 4.6, and gives their no-feed-availability/no-pool-capacity/fixed-demand assumptions. It frames our advance as the simultaneous restrictions, not broad first one-pool hardness.
- Haugland and BKR antecedents retain the source-specific questions established in accepted Sections 2–4. The two-pool result allows growing attributes and inputs; no scalar fixed-parameter implication is asserted.
- Dey–Kocuk–Santana's primary author manuscript explicitly conjectures hardness of the exact simultaneous row/column margin set after Theorem 4, Section 3.1. Appendix B proves that precise conjecture. The matching source is https://www2.isye.gatech.edu/~sdey30/RankonePool.pdf (also https://optimization-online.org/wp-content/uploads/2019/02/7056.pdf).
- Jalilian–Kocuk: published article is Optimization and Engineering 27(1), 317–367 (2026), online July 31, 2025, DOI `10.1007/s11081-025-09997-6`. Its exact SOC theorem is **Theorem 2 in the published 51-page PDF**, not Theorem 1; the latter locator belongs to the 2023 preprint. The bibliography and Section 6 use the published locator and https://research.sabanciuniv.edu/id/eprint/52174/1/Improved.pdf. The source explicitly says the exact construction is exponential. Compact relaxations and computational results in that paper are not confused with a polynomial exact hull.
- Gillis–Glineur (JGO 58(3), 439–464, 2014, DOI `10.1007/s10898-013-0053-2`) supplies an explicit rank-one/biclique antecedent. Their squared Frobenius rank-one approximation of a possibly signed matrix differs from our linear objective and simultaneous margin bounds. Appendix B credits that relationship.
- Peeters (Discrete Applied Mathematics 131(3), 651–654, 2003, DOI `10.1016/S0166-218X(03)00333-0`) is the primary NP-completeness source for maximum edge biclique. Publisher/University metadata and the original paper identify René Peeters.
- Existing Klee–Minty shadows (Gärtner et al.), midpoint/parity lifting bounds (Lubin et al.), and fixed-rank projected-box methods (Punnen et al.; Hladík et al.) retain explicit credit. The physical realizations and variable-total margin algorithm are distinguished from those antecedents.
- Fawzi–Parrilo, Theorem 1, supplies fixed-order PSD bounds and the SOC conversion. Lee–Raghavendra–Steurer's 46-page full manuscript supplies Theorem 1.1 and the quantitative equation (3.11)/Theorem 5.3 inputs. The author publication page identifies STOC 2015; bibliography now gives year 2015, proceedings pages 567–576 and DOI `10.1145/2746539.2746599`, while explicitly retaining full-manuscript theorem/equation locators. The author PDF is https://www.dsteurer.org/paper/sdpsize.pdf.
- Braun–Fiorini–Pokutta–Steurer is cited by Theorem 6(i) in the full author manuscript; no page number tied to a different PDF version is used.
- Boveroux et al.: ORBi record https://orbi.uliege.be/handle/2268/345162 dates the preprint 2026 and its availability May 19, 2026. The 17-page PDF contains four authors; repository staff metadata lists only local authors. The bibliography retains the four PDF authors and adds the verified year. Sections 3.1/3.3 remain version-specific locators.

Fresh targeted primary-source searches combined pooling/ETR, rank-one row-column hardness, pooling/correlation-polytope and matrix-cost complexity. They found the direct Dey/Jalilian comparisons and the adjacent Gillis antecedent, without identifying a prior result for the two stated physical ETR classes or a closer exact margin-set hardness result. This is bounded search evidence, not exhaustive priority certification. The strongest priority claim remains qualified and scoped to the precise physical restriction classes. Correlation-polytope lower-bound machinery is expressly credited, with the face/quantitative transfer proved here.

## Verification and limits

A genuinely isolated source copy is built at `checks/stage4-author-build/source/`; it contains `main.tex`, `bibliography.bib`, all sections, appendices and native figures, and no dependency on repository-root research notes or literature PDFs. Command:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The final source build has no unresolved citations or cross-references, no duplicate labels, no LaTeX/BibTeX warnings, and no overfull or underfull boxes. The two previous empty-year bibliography warnings and the eight previous bibliography underfulls are gone. The first output-directory build could pick up the shared historical `main.bbl`, so the reported validation uses the isolated source copy and its own regenerated bibliography.

Distinct exact-arithmetic checks run in this pass:

- `stage4-author-physical.log`: 4,482 checks of original physical bounds, mixing, conservation, economics and certificates for descending and relay paths, nongeometric supplies, endpoint/midpoint flows, and varied clean flows.
- `stage4-author-unit-penalty.log`: 2,000 rational repairs and objective-penalty checks, with 1,184 totals below one, 214 equal to one, and 602 above one.
- `stage4-author-face-stability.log`: every equal-total quarter-grid margin pair for one and two paired indices, 85 and 38,165 pairs, checking exposure and all rounding/distance constants.
- `stage4-author-rank-one-costs.log`: 160 exact rational/radical comparisons (111 feasible, 49 infeasible), plus irrational-optimum, zero-only-total and singleton-total regressions.

These finite checks provide distinct regression confidence for the physical map, exact penalty, quantitative rounding and radical optimizer. They do not establish asymptotic complexity, external extension-complexity theorems, or solver performance. No empirical speedup, general strongly polynomial algorithm, general FPT algorithm, uniform physical tolerance gap, or full-pooling inference from an isolated block is claimed.

Rendered visual evidence is retained under `checks/stage4-author-build/render/`. The front matter, physical table, synthesis, all appendix pages and bibliography were inspected as contact sheets; the table, new interface figure, representative equations and bibliography were inspected at readable page scale. Final build/page totals and hashes are in `checks/stage4-author-build/validation.json`.

## Remaining work

No unresolved mathematical issue was identified in this author pass. The precise fixed-pool/fixed-quality-rank/degree-two-bypass question with unbounded attachments and general interval contracts remains openly classified as unresolved by this paper. Five independent Stage 4 reviews and the separately assigned correction stage remain to be performed. Root owns the final whole-manuscript validation, shared PDF refresh and portable delivery packaging.
