# Independent S4a review R2

Verdict: **PASS with one minor wording correction; no mathematical major found.**

Reviewed `complexity/sections/06-weighted.tex` in full. Its SHA-256 was `89f5f2ecd4491b7f8401e602e7f6cb7d67b97e447fb31a73925da7a2f852cb48`, matching the frozen assignment. Line references below refer to that version. I did not read the S4a author report, lead notes, checks report, or other reviewers' reports. I did not change the manuscript, shared build outputs, literature knowledge base, or commits. The result and supporting-note files were leads only, not evidence that their claims had already been proved.

## Findings

### Minor M1: say explicitly which data must be positive

Locations: lines 697–698 in the universal hull theorem; lines 943–944 in the quadratic region theorem; lines 978–979 in the power-law extension.

The first two locations promise “positive rational data”; the third promises “Positive rational resistance and nomination witnesses.” Read literally, this can impose positivity on nominations or objective coefficients. Nonzero balanced nominations necessarily have both signs, and the displayed constructions do have signed nominations and, where relevant, signed objective coefficients.

Repair: say “rational nominations and objective coefficients, with strictly positive rational resistances” in the hull theorem, and “rational nominations and strictly positive rational resistances” in the two region theorems. Preserve the existing polynomial encoding qualification for the quadratic results and its explicit absence for the real-power extension.

This is a statement-clarity issue, not a defective construction or a mathematical major. The introductory conventions, proofs, and examples make the intended scope clear. No other required correction was found.

## Independent mathematical audit

### Trees and rational certificates (lines 18–224)

The identity `c^T pi = w^T A^T pi`, with `Aw=c`, gives the displayed weighted cut-sum formula. Endpoint elimination is valid for both intervals and explicitly listed finite sets because the objective is linear in each resistance when nominations are fixed.

The quadratic-maximizer certificate lemma is sound, including singular stationary systems. On a minimal face containing a maximizer in its relative interior, the stationary equations are rational linear equations. Their intersection with the original bounded polytope is nonempty and has a rational vertex of polynomial encoding length. The quadratic is constant on that stationary set. Enumerating independent tight inequalities and solving the corresponding stationary systems also covers lower-dimensional polytopes, vertices, and nonisolated maxima.

The comb reduction correctly realizes coefficients +1 on backbone vertices and −1 on leaves, with maximum degree three. The objective is bounded above by K, and equality forces every withdrawal to an endpoint. At a capped-simplex vertex the sole possible nonendpoint coordinate is integral. Its deficit is at least 1/2 in a no instance. This proves the weak existential threshold reduction, the strict violation reduction at K−1/4, and the stated absolute-error obstruction. The rounding argument is valid: deficit below 1/4 bounds total rounding movement below 1/2, so integrality forces the rounded sum to be K. Multiplication by the product of capacities has polynomial binary length and makes all resistances integral. The pseudopolynomial enumeration includes endpoint vertices and correctly has arithmetic cost O(n²K).

For membership on arbitrary trees, a maximizing closed sign cell has polynomially described rational quadratic data. A polynomial-bit rational maximizer supplies either a weak attainment certificate or, when a strict violation exists, a strict violation certificate. This does not require listing all cells in the certificate. It does not incorrectly generalize rational states to cyclic graphs.

Zero-weight contraction preserves the remaining cut flows and permits rational greedy disaggregation. On the contracted directed tree, positive differential resistances make the adjoint strictly decrease along each directed path. The saturation conditions therefore give the stated one-pivot face family. Fixed-coordinate and lower-dimensional cases remain covered. Uniform smoothing and selection of one closed face justify existence of an original maximizer there. The count k≤2p−2 correctly charges marked degree-two vertices to nonzero objective coefficients, in addition to the leaf/branch count. The algorithm is XP, as stated, and does not imply FPT.

### Fixed global rank and signed paths (lines 228–347)

Pruning zero-objective leaves is exact and retains disaggregation information. The suppression formulas P=k−1+r′ and the support bound are correct, including returning paths and a marked pure cycle.

With the stated signed potential perturbation, adjoint currents have strictly monotone differences along each unmarked path. Their potentials have a single peak or valley, with a possible two-vertex plateau. A horizontal level therefore requires at most two free internal coordinates. This gives the claimed bounded nomination dimension. Uniform convergence follows from the flow bound, compactness, and uniqueness; the argument does not need a numerical perturbation size.

I checked the use of the Section 3 parametric box LP lemma. After retaining all global circulation variables, the core dimension and aggregate dimension are fixed. Cycle equations and objective are linear in the resistance leaves. The lemma's support-function formula, enumeration of realizable sign vectors, fixed-dimensional quantifier elimination, and convex-combination recovery of leaves do not enumerate exponentially many arbitrary resistance corners. The optimizing leaves and core remain in one polynomial-size algebraic field. Removed-nomination disaggregation and state recovery use arithmetic and comparisons in that same field.

The fixed-nomination corollary correctly removes the support restriction. This is a global-rank result, not an unbounded-total-rank cactus theorem. It promises algebraic scenarios when cycles remain, and explicitly excludes finite resistance sets. Those distinctions are necessary and correctly stated.

### One-cycle discrete potential gadget (lines 349–435)

I independently verified the three rational q values, the signed cycle equation, and the completed-square objective. The physical root is unique and has signs (+,−,−). The series replacement has effective resistance `12+(12/K) sum a_i sigma_i`; it reaches the unique objective peak exactly for a target subset.

Subtracting the equation at q=−1/4 yields the displayed denominator. Its upper bound gives `|q+1/4|≥1/(20K+12S)`, hence the stated Δ. The robust limit is below the peak and above all no-instance values, so strict violations correspond to yes instances. Equality in existential attainment is preserved.

The first common resistance scaling makes the two fixed sides and all series choices positive integers. The additional factor produces gap 3nK, at least 3. Absolute-error-one comparison with the peak minus 3/2 therefore separates the cases. Both factors have polynomial binary length; no strong-hardness claim is justified or made.

For NP membership, guessing a finite resistance choice gives a one-variable piecewise rational quadratic cycle equation. Its unique root has degree at most two, with polynomial encoding length. All potentials and the weighted objective belong to the same quadratic field. Exact weak and strict comparisons are polynomial. The witness is the discrete choice together with deterministic algebraic verification, not an assertion that the physical state is rational.

### Rank-two discrete flow gadget and total absolute flow (lines 437–573)

The outer conservation equations, the selected square-root branch a(q), positivity of all five flows, and the cross equation are consistent. The latter has exactly one root in (0,3). I checked all three rational states and both cycle equations independently. The completed-square objective has its unique peak at a=q=9/8.

The divided-difference bound uses 0<a′<1 and q+q*<5 correctly. It gives the stated lower bound in H and a no-instance objective deficit larger than the conservative Δ=1/(4H²). Resistance scaling only clears denominators and does not enlarge this flow gap. Nomination scaling by 16H² scales flows and the objective, producing gap at least four. The theorem expressly acknowledges that this last step loses the small-nomination restriction.

The positive-coefficient objective follows from conservation at vertex 0, with the correct +36 shift. For unit cost on every edge, the long outer path and cross path have the stated effective resistances. All physical flows are positive for every allowed choice. The orientation is acyclic, including all subdivision vertices, so total absolute flow equals total directed flow. I independently verified the identity `nF+36n+8`, the peak `(63n+16)/2`, the counts `14n+4` edges and `14n+3` vertices, global rank two, and maximum degree three. The displayed common multiplier clears every denominator. These are genuine unit coefficients on all edges, not zero-cost padding.

For membership, the fixed-global-rank algebraic evaluator with singleton intervals has polynomial bit complexity. Absolute flow becomes affine on each closed sign cell. Thus both existential weak attainment and complements of robust upper bounds have polynomial verification. No unbounded-rank algebraic-comparison assumption is hidden here.

### Cactus flow regions, scenarios, and scalar values (lines 575–669)

The minimum and maximum cycle functions are continuous and strictly increasing; each summand remains strictly increasing through its zero breakpoint. Their roots bound all attainable circulations and are realized by rational resistance endpoints, including for finite sets. Connectedness gives the full interval for continuous boxes; independent blocks give the Cartesian product. For finite choices it is the convex hull that equals this box image, not the finite attainable set itself.

Linear objective coefficients select cycle endpoints independently. Hence an exact optimizing rational resistance scenario needs no ordering of independent radical sums. The selected physical roots can be represented separately and approximated with a valid summed error budget.

The SRS reduction has direct flow `1/(1+sqrt(a_i))` and contribution `(a_i−1)x_i=sqrt(a_i)−1`. It preserves the weak ≤ convention, including equality. Removing a_i=1 terms, handling trivial adjusted thresholds, and doubling resistances are correct. The fixed output with direct resistance 8 and alternate total 2 has value 1. Thus exact scalar comparison is SRS-hard even though scenario choice is trivial. The manuscript correctly does not turn this into NP-hardness or claim a polynomial common-field representation at arbitrary cactus rank.

### Hull hierarchy and quadratic restoration (lines 671–891)

The positive endpoint arguments use separate monotonicity with other coordinates fixed; they do not incorrectly require one common direction over the entire box or after optimization over nominations. The zero-basis argument for a continuous affine one-edge parameter is valid. Shared parameters across edges remain excluded.

Every simple non-tree contains the required subdivided triangle, and every noncactus contains the required theta. Series splitting preserves the gadget states. The explicit resistance restoration gives a conservation-feasible comparison flow with the stated bounded energy; extra flows are correspondingly small. Restriction to the selected subgraph induces balanced nominations, allowing application of the nomination Lipschitz estimate. I checked all three error budgets and the rank-two comparison energy `91657/16`. The single-edge pressure-to-flow estimate cancels the selected resistance, so subdivision does not invalidate the bound. Polynomial rational splitting and the displayed restoring integers have polynomial encoding length.

For the last hierarchy row I inspected the invoked Section 5 series-parallel statement and its K4-subdivision restoration argument. Section 6 uses that result within its stated simple-graph, one-varying-resistance scope.

The approximate endpoint recovery loses at most 2δ per coordinate and therefore at most ε/2 overall. It is expressly conditional on a suitable fixed-scenario evaluator, avoiding an unsupported algorithm for arbitrary continuous laws or an exact comparison of independent pressure radicals.

### Entire regions and nonlinear powers (lines 893–1098)

The deletion argument has the correct minus sign in the energy identity. Its terminal drop P(q) is strictly decreasing. Except in the constant-state case, both own-edge flow and terminal potential difference are injective scalar coordinates on their respective regions. Convexity then forces the endpoint segment, justifying use of strict interior objective advantage to disprove convexity.

The cactus flow positive direction, tree potential/joint positive directions, and projection argument for joint nonconvexity are valid. Thickening fixed resistance intervals preserves the two chord endpoints while excluding a positive-distance chord point. The proof only gives existence of rational positive widths and appropriately makes no polynomial encoding claim for them.

For every fixed real γ>0 other than 1, the energy is strictly convex and coercive. I independently differentiated the theta equation: a′(0)=5/8 and a″(0)=(γ−1)/32. This uses positive outer flows near the expansion point, so nonsmoothness of the cross-edge power at zero for some exponents is irrelevant. One then chooses a strictly positive q interval. The triangle potential derivative is nonconstant for every permitted γ. Each curvature argument supplies a linear separating objective with a strict interior advantage. Energy restoration, uniform continuity, and rational perturbation preserve that advantage on larger graphs. These are qualitative arguments; no algebraic or accuracy-bit algorithm for arbitrary real γ is inferred.

The closing Ohmic rank-one inverse formula has the correct derivative sign and positive denominator. It proves separate scalar-objective monotonicity on every graph and does not assert convexity of whole state regions.

## Scope and primary sources checked

I mapped the manuscript coverage to these ten result leads: weighted tree NP-completeness; fixed-support weighted trees; weighted tree sign patterns; fixed-support global rank; weighted-potential cycle hardness; weighted-arc rank-two hardness; cactus flow regions and optimization; weighted-potential tree characterization; weighted-arc cactus characterization; cactus region convexity characterization. I also consulted the signed-path decomposition, cactus uncertainty hull, and power-law region extension notes. I did not import the separate unbounded-rank weighted-cactus approximation results into S4a's claims.

Relevant dependencies read included the Section 1 incidence, existence, block/cycle, continuity, output, and arithmetic conventions; Section 2 adjoint, saturation, smoothing, and Lipschitz arguments; Section 3 bounded faces and parametric box LP with leaf recovery; Section 5 pressure theta, continuous-law envelope/separate-monotonicity statements, and arc-hull characterization. Section 4's evaluator is used only through the explicitly scoped conditional endpoint-recovery statement.

Primary-source checks:

- Del Pia, Dey, and Molinaro, local author manuscript: `[[pia2016-mixed-integer-quadratic-programming-is]] p.3`, Section 2.2, Theorem 3. Checked the optimal rational-linear-system assertion in the original PDF using fresh `pdftotext` extraction. It supports the certificate attribution; the manuscript also supplies its own proof.
- Levi, Perakis, and Romero: `[[levi2014-a-continuous-knapsack-problem-with]] p.2`, Proposition 1 (printed p.368). Checked the original PDF's Subset Sum endpoint mechanism. It is an appropriate antecedent, not a source for the network restrictions or the manuscript's explicit 1/2 gap.
- Labbé, Plein, and Schmidt: `[[labbe2020-bookings-in-the-european-gas]] p.12-p.14`, opening of Section 5 and tree flow/potential formulas. The manuscript's limited attribution to preceding pairwise tree algorithms is appropriate.
- Aßmann et al.: `[[amann2018-deciding-robust-feasibility-and-infeasibility]] p.16-p.17`, Section 4.2, and `p.20-p.21`, Proposition 4.9 and Lemma 4.10. Checked the cycle lemma against the original PDF. These support fixed-nomination resistance linearity on trees and the scalar cycle interval principle, without establishing the new weighted claims themselves.
- Basu survey: `[[basu2014-algorithms-in-real-algebraic-geometry]] p.16`, Theorem 2.27. Fresh extraction from the original PDF confirmed the polynomial-count, degree, and coefficient-bit bounds used in the fixed-dimensional dependency. I did not independently re-audit every algorithm in the Basu–Pollack–Roy book; its local full-text extraction is corrupted. The Section 1 sample-point primitive and standard ordered algebraic-field operations remain explicit external algorithmic dependencies.
- Wang and Hasler: `[[hasler1997-convexity-of-resistive-circuit-characteristics]] p.13`, Theorem 4, and `p.21`, conclusion. These concern scalar source-to-response curvature; the conclusion proposes other circuit parameters as further work. The scope distinction in Section 6 is accurate. The primary EPFL source was also located online at [Convexity of Resistive Circuit Characteristics](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download).
- Brandenberg and Stursberg preprint: `[[brandenberg2025-extremal-solutions-for-network-flow]] p.3-p.4`, differential-flow definition, and `p.19`, Theorem 18. The linear fixed-network polytope and its universal nondegeneracy characterization differ from the nonlinear resistance-attainable state images here.
- Vavasis (1990): verified bibliographic identity and NP result from the [publisher record](https://www.sciencedirect.com/science/article/pii/002001909090100C) and the author's publication record; I did not obtain or claim a full reading of that article. The directly checked Del Pia theorem and independent proof cover the needed assertion.

The separate 1993 nonlinear-tolerance source was not available in full and was not treated as checked. The manuscript openly preserves this limitation and makes no exhaustive priority claim. This review is not an exhaustive novelty search.

An independent in-memory exact-rational check verified the triangle states/objective, all three weighted theta states and cycle equations, the total-flow identity for multiple path lengths, and the restoration energy/error constants. No repository verification script or prior checks report was used.
