# Stage 1, round 2 — reviewer 10

**Verdict: PASS.** No substantive mathematical or editorial defect found.

## Coverage

I read the complete frozen `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex` under `process/snapshots/stage01-round02/`. I checked all 19 entries in its manifest against their SHA-256 hashes. I read the frozen finite checker after writing and running my independent calculation, and compared its stored histograms with mine. I checked the PDF metadata but did not perform a separate visual layout review or compilation.

Dependencies read: `results/mccormick-gap-degeneracy-bound.md`, `results/mccormick-hereditary-density-characterization.md`, and `results/positive-multilinear-degree-upper-bound.md`, especially its preliminary envelope, deficiency, independence, and box-transfer arguments. I read the Stage 1 coverage rows and stage boundaries in `process/scope-proposal.md`, the round-2 assignment, the review protocol, the round-1 adjudication, and the correction record. Future-stage results were not treated as missing Stage 1 content. I did not read any other round-2 report.

Following `literature/AGENTS.md`, I read relevant extracted primary-source sections and checked important equations directly by fresh extraction from their original PDFs:

- `[[luedtke2012-some-results-on-the-strength]] p.7-9` and `p.15`: recursive versus exact relaxation, vertex laws, Theorems 4–5 and the nonnegative-box restriction, and Theorem 8's even/odd coloring constants.
- `[[boland2017-bounding-the-gap-between-the]] p.3-6` and `p.10-12`: the 600 constant, half-integral cut identities and upper implication, exactness criterion, and the explicit predecessor attribution.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7`: Schur factorization, the real projective/Grothendieck inequality, and the weighted theorem's continuous density parameter. Fresh PDF extraction restored equations omitted by the stored markdown.

The publisher's [Szarek record](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality) confirms the cited bibliographic details. Its linked PDF returned HTTP 403. I therefore did not inspect Szarek's original proof; the sharp real Khinchin inequality is an external theorem input. I did not independently inspect the Misener–Smadbeck–Floudas predecessor or McCormick's original article. The manuscript accurately describes the former attribution as indirect.

## Findings

None. No major or minor finding IDs are assigned.

The accepted repairs A1–A6 are present and adequate: exact finite results now have a complete finite proof and witnesses; tolerance ranges make the target monotonicity valid; exact factor-one statements exclude empty effective support; the author manuscript is identified; the predecessor is acknowledged without implying direct access; and the introduction includes the nonnegative-box hypothesis.

## Independent verification

### Reconstruction of the universal arguments

1. **Vertex laws and deficiencies.** Independent endpoint sampling represents every multiaffine graph point using vertex graph points, so the graph hull equals the finite vertex hull. Its sections yield attained LP extrema and continuous piecewise-affine envelopes, including boundary points. Consecutive failure arcs on the circle attain the lower single-product formula even when their total length exceeds one. The common threshold law supplies all upper envelopes together. Subtracting the anchor's fixed expectation gives the stated nonnegative deficiency formula. Discarding affine supports is legitimate for the gap statements. Both independence cases retain the factor `(1-exp(-1))/2`, including zero deficiencies.

2. **Box transfer and certificates.** Positive affine expansion preserves the complete function's hull gap and can only increase the sum of the separate factor widths. Thus the direction of the original-versus-expanded inequality is correct. Nonnegative lower endpoints are essential for the common-threshold proof and are stated. The certificate definitions imply `f* >= T*`; substituting the two targets yields their claimed absolute and relative guarantees. The slopes in the incumbent are respectively 1 and `1-theta > 0`. The positive-optimum condition for granting the best relative incumbent handles the normalization boundary.

3. **Induced-cut characterization.** At a half-valued face, mixing an extremizing sign vector with its negative preserves every mean and gives `H = (max Q-min Q)/4 = R/2`, while `T=L/2`. Fixed coordinates equal to one contribute affine terms only. The cell proof is complete: the active equal/complement relations either fix a connected component, force its value to one-half through odd complement parity, or leave a perturbable parameter. Thus all cell vertices are on the stated grid. Concavity of `H` and affinity of `T` on each cell extend the grid bound to every point without division by a possibly zero gap.

4. **Density and degree constants.** From `s=u+v`, `t=u-v` on complementary supports, `Q(s)-Q(t)=2 v^T A u`. This establishes the cut/block-norm identity with its exact normalization. Khinchin and a locally maximal cut for squared weights give `R >= sum_i ||a_i||_2/4`. The flow network gives load bound exactly `rho`, since its relevant cut capacities are `m-|E(U)|+t|U|`. Weighted Cauchy–Schwarz then yields `L <= sqrt(rho) sum_i ||a_i||_2`. Counting both endpoints gives the improved maximum-degree constant 2. In the bipartite case all edges cross the prescribed partition, yielding the separate degree bound and its frustrated four-cycle equality case. The direct degeneracy proof uses each outgoing edge exactly once.

5. **Lower bound and quantifiers.** There are `2^(h-1)` vertex-sign classes and two exponential terms for each, giving exactly `h log 2` in the moment estimate. Optimizing the positive parameter gives `sqrt(2mh log 2)`. Extending a signing from a densest induced graph preserves its face witness. The whole-center coefficient supremum equals the induced supremum because arbitrary coefficients may be zeroed outside a face. Compactness on `L=1` and continuity of the whole-center range justify perturbing zero coefficients; continuity of `c*` is unnecessary. This argument does not imply equality of the two full-signing optima.

6. **Exactness, examples, and prior transfer.** `R=L` forces the positive and negative edge sets separately to be cuts, since both extremal signed-weight bounds must be attained. The even-cycle-intersection characterization of cuts gives the stated criterion on effective support. Coloring probabilities, complete-graph positive ratios, diluted-core example, scaling objection to weighted density, and degeneracy/arboricity comparisons check out. In the older transfer the adjacency pattern satisfies `beta=rho`, the pairing counts `2L`, and polarization bounds the full matrix norm by `4R`, yielding `4 K_G sqrt(rho)`. The weighted version of Davidson–Donsig avoids integer rounding. The Sidon comparisons follow from the zero mean of `Q`, and bipartite sign reversal makes its range symmetric.

### Exact finite calculation

Artifacts: `verification/reviewer10/round02/check.py` and `verification/reviewer10/round02/results.json`.

My calculation evaluates quadratic characters by integer matrix multiplication on all sign vectors, independently of the manuscript's cut masks and population counts. It enumerates every root-normalized signing for `K2` through `K7`. There are at most 21 signed unit summands in each matrix entry, so the signed 64-bit integer arithmetic used in this independent checker cannot overflow. Fractions are exact.

The minimum ranges are `[1, 2, 4, 4, 5, 8]`. All six range histograms agree with the frozen stored output; in particular the `K7` histogram is `{8: 3240, 10: 20664, 12: 8864}`, totaling 32768 representatives. I also extracted and executed the verbatim appendix program; it returned the same six minima.

I reconstructed the completeness argument: vertex switching is a bijection on sign vectors, the root star can always be made positive, and a switch preserving that star changes no edge. Hence the free-edge choices enumerate switching classes exactly once. Complementation covers all cuts while fixing the root side. The candidate range cannot exceed the number of edges because the difference of two cut indicators has entries in `{-1,0,1}`. The initialization therefore cannot suppress a candidate.

Direct evaluation of every listed witness gives quadratic extrema `(-1,3)`, `(-2,6)`, `(-4,4)`, `(-5,5)`, and `(-7,9)`. The extended six-vertex example gives `(-9,11)` and ratio `21/10` at the full center. Exhaustive induced-face checks give factor 3 for that extension. Finally, restriction and arbitrary signing extension prove `F_n=max_{2<=k<=n} M_k`, so the asserted all-face sequence follows analytically from the finite center table.

### Numerical counterexample search

I solved 600 vertex-law LPs covering 300 evaluation points on signed bilinear functions in dimensions 2–6, with seeded unequal means, half-integral boundary points, full centers, mixed integer weights, zero coefficients, and tiny positive coefficients. No violation of `T <= (max_W L_W/R_W) H` occurred at tolerance `1e-8`; the full-center identity also passed. These are floating-point checks of sampled cases, not a proof of the universal theorem.

## Remaining limits

The finite enumeration proves precisely the displayed full-signing problems through `K7`; it neither determines larger sizes nor solves the arbitrary-real coefficient extremal problem. The universal review is a mathematical reconstruction using the cited Khinchin and Schur/Grothendieck inputs, not a formal proof verification. Source access and layout limits are recorded above. None of these limits invalidates the manuscript's stated Stage 1 scope.
