# Independent whole-paper review 07

**Verdict: PASS.** No major or minor findings. The frozen manuscript supports its stated conclusions, with the distinctions between resources and the limitations recorded in the statements. No repair is required by this review.

## Coverage

The target was `process/snapshots/whole-round01/main.pdf`, 111 pages, independently verified SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. I read the entire mathematical manuscript in its frozen LaTeX source, including every proof, displayed finite checker, appendix, abstract, introduction, synthesis and bibliography. Specifically, the files read were `main.tex`, `macros.tex`, `references.bib`, and all of these files under frozen `sections/`:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I also read the frozen review protocol and whole-paper assignment, reviewer-focus record, scope proposal, claim-coverage ledger, Stage 6 author record and correction log, README and process description. I used the frozen primary-source and author-validation records as source locators, not as proof or as substitutes for checking. The ledger's topic coverage agrees with the manuscript: predecessor arguments with distinct content remain in the appendices; exploratory searches and unresolved questions are not promoted to theorems. The additional scaling focus did not narrow the reading.

For scaling provenance I also consulted `../results/scaling-disjunctions-hull.md`, `../notes/audit-scaling.md` and `../notes/review-scaling-characterization.md`. These were contextual cross-checks. The verdict rests on the frozen manuscript and independent reasoning, not previous PASS labels. I did not read other reports from this final round or delegate any part of this review.

I read `../literature/AGENTS.md` before accessing originals. Direct primary-source inspection included the following passages; page numbers are PDF pages unless otherwise stated:

| Source | Directly inspected material |
| --- | --- |
| Balas (1998), local original | Pages 5–7: Theorem 2.1, its proof, and boundedness consequence. |
| Wu et al. (2026), local original | Pages 11–12: aggregation setup, Assumption 1, Lemmas 2–3 and Theorem 3. |
| Starr (1969), original in `/tmp/minlp-relaxation-limits-sources/` | Pages 12–13, printed 35–36: Appendix 2, including the Shapley–Folkman lemma and proof. |
| Davidson–Donsig, local original | Theorem 1.2; pages 6–7, Theorems 2.3–2.4 and adjacent lemmas on patterns and weighted bounds. |
| Boland et al., local original | Pages 1–4: definitions, dimensional bounds, half-grid reduction and exact cut-range statement. |
| Luedtke et al., local original | Page 22: Conjecture 1 and its context. |
| Sherali (1997), local original | Pages 8–9, printed 252–253: equation (13), Theorem 3 and proof setup. |
| Cornuéjols, original in `/tmp/minlp-relaxation-limits-sources/` | Theorems 6.5 and 6.13: Eulerian criterion and the signed balanced-matrix system. |
| Hassin–Tamir, original in `/tmp/minlp-relaxation-limits-sources/` | Pages 3–4, printed 381–382, visually: Theorem 3.1 and series/parallel construction conventions. |
| Altschuler–Boix-Adserà, local original | Input/precision conventions and Section 7.2, Theorem 7.4, Corollary 7.5 and the logarithmic-precision question. |
| Potechin (2019), local original | Knapsack equations, Theorem 1 and attribution to Grigoriev. |
| Schoenebeck, author full version | Pages 7–11: Definition 10, Theorems 11–12, Lemma 13 and proof; pages 17–19: expansion input and associated proof. |
| Kronqvist et al., local P-split original | Pages 4–7 and 15–16: retained domain, sharing convention, assumptions, Definition 4, Corollary 3, Theorem 6 and proof. |
| Khajavirad (2024), primary HTML | Definitions of RLT/SDP and tightened bounds, Proposition 1(i–ii), Proposition 3 and their proofs. See [arXiv v1](https://arxiv.org/html/2404.03091v1). |
| Fawzi–Parrilo, local original | Page 3: Theorem 1 and conversion between Lorentz cones and fixed-size PSD blocks. |
| Lee–Raghavendra–Steurer, original in `/tmp/minlp-relaxation-limits-sources/` | Page 23 and pages 32–34: quantitative estimate, pseudo-density application, Theorems 5.3–5.4. |
| Braun et al., original in `/tmp/minlp-relaxation-limits-sources/` | Page 18: hard pair and Theorem 6(i). |
| Etessami–Yannakakis, original in `/tmp/minlp-relaxation-limits-sources/` | Pages 26–28: Theorem 5.2 and circuit/sign/amplification proof. |
| Belotti et al., local original | Page 14: Theorem 4.1 and the infeasibility caveat. |
| Stewart et al., local original | Pages 21–22: Section 4.1, equation (18) and conditioning argument. |
| Esparza et al., local original | Page 34: Theorem 7.1 and proof. |
| Lubin et al., local original | Page 12: midpoint lemma and proof. |
| Beach et al., local original | Page 21: approximation-error table and conventions. |

This table identifies actual direct inspection, not a claim that every page or every prerequisite of these external papers was read.

## Findings

None. In particular, I found no failure of the scaling characterization, no omitted zero-scale assumption, no loss of a needed shared-coordinate condition, and no unjustified transfer of a spatial conclusion to another computational resource.

## Independent verification

### Scaling and perspectives

I reconstructed the endpoint argument by holding the intensive pair fixed and interpolating only the extensive scale. This explains both why the two endpoint hull is sufficient and why projecting away the intensive coordinates changes cost separability. The fixed-count averaging argument preserves the common intensive coordinate: a count-
`n` point averages to `(n, n xi, T)`. Thus arbitrary labelled copies add no additional hull points. The zero-count convention and singleton scale case are handled explicitly.

For the conic lift, I checked the potentially dangerous zero-multiplier slice independently. A feasible homogeneous direction at multiplier zero can be added to every feasible lifted point. Its projected direction is therefore a recession direction of the projected convex set. Compactness forces this projected direction to vanish, even if the auxiliary lift itself is unbounded. This justifies the zero-slice projection used in the disjunctive formulation.

I checked the eliminated bilinear description at zero lower load and at signed intensive endpoints. There is no hidden division by the lower load. An independently written exact rational program enumerates every intersection of four displayed facet hyperplanes and tests all inequalities. For four parameter choices, including lower load zero and wholly negative intensive intervals, its vertex set equals exactly the six claimed endpoint atoms. This is finite corroboration of the elimination proof, not a universal proof by enumeration.

For the nonseparable scale-cost example, I reconstructed the six-atom LP. The mean-scale constraint gives `p_0=p_2`; the required difference of the extensive and intensive means forces `p_2>=1/2`; the cost is therefore at least one, and an attaining law gives equality. Exact basis enumeration independently returned one. The separately convexified cost gives zero at the same point, so the comparison is strict.

For extensive-only separability I checked the size-biased distribution used for the lower bound and the product distribution used for attainment. When the mean scale is zero, nonnegative scales force all mass onto zero; the separate boundary argument is necessary and is present. The finite cost need not be convex before taking its lower convex envelope.

The rectangularity characterization has the required interior scale `0<s<M`, with `M` the maximum allowed scale. A diagnostic cost vanishing only at `s` forces a representing law onto that slice. I reconstructed the resulting fibre contraction and its iteration toward each prescribed intensive coordinate; closedness supplies the limit and hence rectangularity. Conversely, rectangularity supplies a common intensive pair at every scale, and decomposing that pair into the original compact set proves attainment. Endpoint-only scale sets would make the characterization false without the interior-scale hypothesis; the manuscript explicitly treats that boundary. The integral count hull uses integrality of its vertices and does not require an integer-decomposition property. The Shapley–Folkman estimate uses at most `min(d,n)` exceptional summands, with the stated diameter, Lipschitz and normalization assumptions; arbitrary linking constraints are correctly excluded.

### Whole-paper proof checks

I reconstructed the vertex-law representation and half-grid cut reduction, the density upper/lower arguments, and the common-law positive rounding bounds. I checked harmonic normalization, zero deficiencies, the Lambert-W regime, dyadic/radix attainment, and the restricted meaning of mixture optimality. The cubic scalar slack is a valid lower bound and is not misrepresented as an attained optimum. Finite integer count certificates range over every count state, not only the atoms in their proposed attaining law.

For the structural chapters I checked ownership restrictions, feedback restoration on the original factor scopes, the retained shifted baseline in frequency two, and all series/parallel boundary cases in the width-two coloring invariant. The balanced/TU dependency has the correct mixed-system hypotheses. Positive-box expansion retains one ambient correlated law; coefficient induction uses the physical aspect bounds consistently. The exact single-product reduction preserves polynomial rational encoding and a nonzero decision gap; a factorwise ratio of one does not imply easy scalar envelope evaluation.

For the cardinality chapters I followed the harmonic positivity argument, equality multipliers, repeated slack products and degree accounting, including integer and zero boundary cases. The global tensor argument establishes positivity for coupled squares. Coordinatewise graph interpolation is an affine substitution in the formal lifted coordinates, which is why it avoids a degree loss for that family. Full-graph agreement of the objective and the specified oracle remain necessary and stated.

For XOR I checked the signed-character Gram construction, the positive source width constant, deletion and occurrence accounting, and the degree budgets `4r` and `4rD`. Exact quadratic moment realization is over the full node box and need not lie on the lifted graph; the manuscript states that distinction. The lifted witness count uses parity rank and the union of supports of a basis. The order-one quadratic formulation and the original cubic order-two certificate are distinct arguments with their own hypotheses. I reconstructed the Bernstein upper certificate and verified that the affine-branching discussion is an obstruction to the method, not an affine-tree lower bound.

For the supporting appendices I checked point-packing upper bounds and attaining moments, the P-split counterexample under the source's retained domain and sharing rules, the repaired feasible-direction criterion, and rational rotation identities. I reconstructed correlation-face stability and kept exact conic size separate from approximate sandwich complexity. The FBBT limiting argument retains a nonempty limit, and the primitive-update recurrence does not imply a lower bound for accelerated contractors. Integer parity and binary-assignment covers are correctly distinguished from spatial region covers. The synthesis and abstract preserve these distinctions.

### Exact checks and build

Artifacts are confined to `verification/reviewer07/whole-round01/`. The independently authored `check_independent.py` and its JSON/log outputs record:

- exact facet/vertex verification for four bilinear scaling instances;
- exact LP basis enumeration for the scale-cost example;
- execution of both finite cubic checker blocks extracted directly from the frozen appendix, including all `7^3+9^3+65^3` three-group states and all displayed two-group states;
- execution of the frozen finite-signing checker, recovering the listed normalized values through `K_7`;
- symbolic reconstruction of the two scalar eliminations and all five Bernstein rows, with minimum certified slack `901/120000`;
- an independent symbolic check of the two-level square/slack identity.

All passed. These checks use integer/rational arithmetic and exact symbolic identities. I did not run numerical optimization or use floating-point positivity as evidence for a theorem.

I copied only the frozen TeX inputs into my own `verification/reviewer07/whole-round01/build/` and ran `latexmk` there with that directory explicitly set as the working directory. All 31 copied inputs match their frozen originals. The build succeeds, produces 111 pages, and contains no warning, overfull-box or undefined-reference messages. The rebuilt and frozen PDFs have identical `pdftotext -layout` output. `build-integrity.json` records these checks.

I visually inspected rendered frozen PDF pages 1, 3, 21, 85–87, 94–97 and 111. These cover the opening narrative, dense scalar formulas, the complete finite cubic program, scaling appendix and bibliography. The inspected pages are readable without clipping or missing equations. I also inspected the relevant rendered Balas, Starr and Hassin–Tamir source pages, including the scanned graph-theoretic source whose text extraction was unhelpful.

## Remaining limits

This is an independent mathematical review, not a formal proof-assistant verification. I read every manuscript proof, but did not reprove entire external theories such as matching algorithms, Grothendieck's inequality or the general PSD-rank lower bound from first principles. Direct-source inspection is limited to the passages listed above. I did not independently retrieve and settle the historical Coniglio-source identification; the manuscript treats it as unresolved provenance rather than a necessary theorem input. I did not visually inspect all 111 rendered PDF pages, and identical extracted text is not a pixel-level equivalence test.

The finite computations do not establish the universal claims. Those were assessed by reconstructing the written arguments and attempting endpoint, scope and coupling counterexamples. Open constants and structural extensions remain explicitly open, including the exact cubic supremum, the positive-box bipartite frequency-two interval and higher-width extensions. They are not missing proofs of conclusions asserted here.
