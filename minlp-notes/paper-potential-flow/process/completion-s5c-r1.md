# Independent Stage 5c review — R1

## Overall verdict

**Accept the frozen Stage 5c section. No major or minor findings.** I found no defect in the stated mathematical results, polynomial bit bounds, original-parameter recovery, or the inspected literature comparisons. This verdict concerns the stage's theorem-and-proof deliverable; it does not assert that a general quantifier-elimination or network-optimization implementation has been tested.

I read the review instructions first, then all 600 lines of `complexity/sections/10-weighted-blocks.tex`, its integration, the material dependencies listed below, the two Stage 5c evidence files, and the diagnostic source. I did not read author, lead, peer, adjudication, or historical review reports; I did not coordinate with other reviewers or spawn agents. My only repository write is this report.

The initial and final source SHA256 values were both:

`fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`

The path checked was `paper-potential-flow/complexity/sections/10-weighted-blocks.tex`. Both checks match the supplied frozen hash.

## Verdict for every new result

| Result | Verdict | Basis |
| --- | --- | --- |
| `lem:a-wblk-local`, Conditional block values | Pass | Block independence, exact coefficient-box projection, fixed-dimensional maximization graphs, continuity bounds, and separate local algebraic recovery are justified. |
| `lem:a-wblk-univariate`, Uniform rational approximation on an interval | Pass | The primitive squarefree annihilator, complex exceptional set, short bands, analytic panels, interpolation error, and dense rational output all have the claimed polynomial bit bounds. |
| `cor:a-wblk-scalar-sum`, Sums of scalar semialgebraic responses | Pass | A common rational interval partition avoids introducing one algebraic variable per summand. The enclosure and rational-argument error budgets are sufficient. |
| `thm:a-wblk-line`, Weighted bounded blocks on an affine nomination line | Pass | The scalar result applies to all three coefficient models. Local optimizer recovery and coefficient rounding give feasible original scenarios within the claimed tolerance. |
| `cor:a-wblk-line-polynomial`, Fixed dense piecewise-polynomial laws | Pass | Fixed-dimensional elimination permits growing numerical degree under dense encoding; the flow and law Lipschitz estimates remain valid. The statement correctly restricts this extension to fixed laws. |
| `thm:a-wblk-hybrid`, A fixed total rank in the noncactus blocks | Pass | The exceptional core retains only `d + κ + 1` coordinates, including one total value coordinate. Exact box projection precedes growing-degree cactus approximation. Optimization, recovery, and rounding remain polynomial. |
| `cor:a-wblk-hybrid-box`, Balanced boxes with fixed support and exceptional rank | Pass | The resistance-independent face reduction applies, does not increase exceptional rank, and permits rational lifting. The face-selection error is within the allocated budget. |

The final subsection's several-parameter question and literature comparison also pass. They delimit an unproved interface in the present algorithms without claiming impossibility, new hardness, or a need for exact Square-Root Sum comparison.

## Mathematical and algorithmic checks

### Conditional graphs and coefficient elimination

For `lem:a-wblk-local` (lines 25–101), the components attached to the vertices of a block partition the original vertex set. Their nomination sums therefore provide the correct balanced local nomination independently of other blocks' coefficients and circulations. A blockwise spanning tree gives rational objective weights and affine physical-flow coordinates; a fundamental-cycle coordinate on a chord equals its chord flow. The total-positive-nomination bound consequently bounds all retained circulation coordinates, including after aggregation.

I checked the full proof of `lem:a-blk-boxlp` in `03-block-rank.tex`. Its support-function representation replaces an unbounded coefficient count by a fixed-dimensional support direction. It enumerates only realizable signs of the polynomial columns, then performs fixed-dimensional elimination. It does not enumerate all coefficient-box corners or introduce a variable for every coefficient or maximum. The resulting formula describes all attainable values, which is stronger than describing only local optima and is needed by the hybrid theorem.

Appending the local maximality condition and eliminating the bounded number of remaining variables is valid. Compact coefficient fibers and continuous unique physical states ensure that every conditional maximum is attained. Zero columns, redundant cycle equations, bridges, singleton coefficient intervals, and lower-dimensional nomination domains are covered. In particular, selecting a closed flow-sign cell does not create a directional-model relaxation: at a zero edge flow both directional contributions vanish. A symmetric coefficient remains one original coordinate.

The local constants are correct: the nomination-to-flow estimate contributes the factor `1/2`, and the quadratic law contributes `2 β_U B_0`, giving exactly the displayed `K_B`. Aggregated nominations cannot have more total positive mass than the original nominations. Maximization over a common coefficient box preserves the fixed-profile Lipschitz bound. The absolute value bound and all rational constants have polynomial encoding length.

### Annihilator and complex exceptional parameters

I checked lines 131–170 in particular. A finite Boolean polynomial-sign formula defining a function graph cannot have every participating nonzero polynomial locally nonvanishing at an interior graph point: otherwise its truth value is constant in an open two-dimensional neighborhood. Excluding the finite roots of the parameter-only factors therefore forces a value-dependent factor to vanish. Removing content and repeated factors preserves those generic zeros; continuity extends the identity to the excluded real parameters and interval endpoints. Thus the construction gives a nonzero primitive annihilator with positive value degree even when the graph switches between different algebraic components.

The product has polynomial degree and bit size in the explicit dense input. Subresultants over `Q[t]` provide polynomial-size gcd and squarefree computations over `Q(t)`. Clearing denominators and primitive normalization do not require factoring into all irreducible components or selecting a globally irreducible branch. The resultant with the value derivative is nonzero precisely because the polynomial is squarefree over the characteristic-zero field `Q(t)`. Multiplying by the leading coefficient covers finite roots escaping to infinity as well as collisions.

The proposed elimination for exceptional real parts is real existential elimination of the real and imaginary equations, not unrestricted complex elimination of the auxiliary coordinate. Under that stated interpretation it returns exactly the finite set of real parts of complex roots. Its variable count is two and its numerical degree and coefficient lengths are polynomial. Isolating and comparing the resulting real algebraic coordinates therefore costs polynomial bit time. Repeated roots of the exceptional polynomial and distinct roots with coincident real parts require only ordinary distinct-root handling; no separation assumption is imposed. A constant exceptional polynomial correctly yields an empty list.

### Bands, disks, interpolation, and rational encoding

I independently checked the geometry and constants in lines 172–280. The merged exceptional bands have total length at most `4(E+1)ρ ≤ η/(16K)`. Any one component is at most that long, so a midpoint value approximation within `η/8` gives the asserted constant-piece error. Artificial endpoint bands ensure all remaining gaps have rational boundaries. An exceptional real part outside `[-1,2]` is too far away to defeat the stated disk bound.

The panel recurrence increases the distance scale by `33/32` until its final step. Its panel count is logarithmic in `1/ρ`; rational numerator and denominator lengths grow only polynomially over those steps. With `R = d(τ)/4`, the half-width satisfies `h ≤ R/16`. The entire closed disk stays at least `3ρ/4` away from every complex exceptional root, since distance to a complex number is at least distance to its real part.

Nonvanishing discriminant and leading coefficient give simple local roots throughout a neighborhood of the closed disk. A root bound makes the covering proper over compact subsets; simple connectivity then gives the required holomorphic branch. The continuous real graph cannot change among distinct roots on a connected panel. This permits branch changes in the short bands without assuming irreducibility or nonzero physical derivatives.

The lower bound for the leading coefficient follows by its factorization over the complex numbers. The explicit root bound `M` may be numerically very large, but its logarithm and rational encoding are polynomial in the input and accuracy bits. This is sufficient: the interpolation order is logarithmic in `M/η`. The contour remainder estimate is valid, including the separate zero-error treatment at interpolation nodes. The equally spaced-node Lagrange bound allows rational node errors `η/[8(2q)^q]`, whose requested precision is polynomial. Expanding products of polynomially many rational factors in one variable gives polynomial dense degree and coefficient length. No compositum of the node-value fields is needed.

These arguments cover constant functions, reducible annihilators, vanishing contents, real branch switches, nonreal branch points arbitrarily close to the interval, near poles outside the domain, merged bands, and an empty exceptional list.

### Sums, line optimization, and the polynomial-law extension

For `cor:a-wblk-scalar-sum` (lines 282–311), sorting all rational endpoints creates only polynomially many common intervals. Either valid adjoining polynomial can be used at a shared endpoint. After summation, the uniform error is at most `a = ε/16`, irrespective of signs or near cancellation among summands. A surrogate enclosure of width `ε/8` becomes a true enclosure of width at most `ε/4`. The algebraic sample loses at most `5ε/16`; moving to the stated nearby rational point costs at most `ε/4`. The bounds leave slack. The empty sum and constant case do not require division by a vanishing continuity coefficient.

For `thm:a-wblk-line` (lines 315–355), interval normalization preserves rational polynomial encoding. A singleton interval uses separate local computations and value enclosures. At the chosen rational parameter, exact local coefficient maximizers combine because blocks share the correct aggregate nominations and satisfy their cycle equations. Rounding inside each original coefficient interval costs at most `||c||_1 B_0^2 k δ`. In the symmetric model the shared coefficient is rounded once; in the directional model inactive coordinates may be selected and rounded independently. Fixed and singleton coefficients remain exact. Original-domain feasibility does not require preserving a sign cell after rounding.

For `cor:a-wblk-line-polynomial` (lines 362–396), I checked the fixed-law model in `04-laws.tex`. There are polynomially many affine breakpoint hyperplanes in a fixed number of variables. Substitution of affine flow coordinates into dense polynomials preserves polynomial dense encoding in fixed dimension. Continuity identifies the formulas on closed-cell overlaps, including breakpoints. Strict monotonicity still gives the acyclic difference-flow estimate. Absolute coefficient sums bound law values and one-sided derivatives on the bounded flow interval with polynomial bit length. The resulting global law Lipschitz bound is valid across all finitely many breakpoints. No lower bound on a nonzero derivative is needed. Sparse binary exponents and uncertain polynomial-law coefficients are correctly outside this corollary.

### Hybrid optimization, recovery, and nomination faces

For `thm:a-wblk-hybrid` (lines 410–510), the exceptional blocks retain exactly `κ` circulation coordinates. The coefficient-box projection uses `κ` cycle-linking rows plus one weighted value row, regardless of exceptional-edge count or objective support. Sign enumeration takes place in fixed dimension `d + κ`. The box lemma is applied to degree-two data before the cactus surrogate degree grows.

I checked the fixed-law and uncertain-coefficient cactus constructions, especially `lem:a-wcac-threshold`, `lem:a-wcac-candidates`, and the error/recovery paragraphs following them. Their local data depend only on aggregate nominations, so their use beside noncactus blocks is legitimate. The common partition uses realizable signs, including surrogate comparisons within each cycle; it does not enumerate cross-cycle candidate combinations. It supplies both required bounds: the conditional maximum is within `a` of the summed surrogate, and the selected feasible scenario is within `a` of that surrogate.

The final semialgebraic optimization has `d + κ + 1` variables. Denominator nonzero conditions remain in the formula. Open sign parts are handled by supremum decisions and a strictly smaller sampling threshold. Since every exceptional feasible value combines with the independent cactus choices, the stated physical and surrogate bounds apply to the entire optimization. The `5ε/16` sampling loss includes candidate selection.

Recovery of exceptional coefficients works for an arbitrary feasible algebraic core and prescribed value. The zonotope vertices can be enumerated through full-dimensional cells of the support-direction arrangement; this remains true for a lower-dimensional image. An affinely independent convex combination of at most `κ+2` such vertices is recovered by fixed-size linear algebra in the core's ordered field. Lifting that combination preserves every original interval and the prescribed cycle and value rows. Separate cactus extensions over the field of `z_*` do not require one common field for all cycle roots.

The intersection of the rational isolating box with rational `P` contains `z_*`, hence is a nonempty rational polytope and has a polynomial-size rational feasible point. This handles affine equalities and lower-dimensional domains. Coefficient rounding remains inside the original intervals. The sum `K_b H_1 h + ||c||_1 B_0^2 k δ` bounds the remaining objective loss, even if rounding crosses branch boundaries or changes exceptional circulations. Together with the sampling loss it is strictly below `ε`.

For `cor:a-wblk-hybrid-box` (lines 512–531), I read the full nomination-face proof, including pruning, zero-objective block contraction, both perturbation limits, and rational disaggregation. Surviving blocks retain their ranks, so exceptional rank cannot increase. The face family is independent of law coefficients and remains complete for joint optimization. Each face has fixed nomination dimension. Selecting by the largest certified lower endpoint costs at most the chosen interval width in addition to the per-face scenario error; tolerance `ε/8` is ample. Rational disaggregation preserves the objective and original bounds. The balanced zero objective is treated by feasibility alone.

## Material dependencies actually inspected

- `01-preliminaries.tex`: the model and edge-orientation conventions; `thm:a-pre-existence` and its energy proof; the block-incidence and block-decomposition arguments; `lem:a-pre-attainment`; fixed-dimensional real elimination, sample-point representation, and exact/additive output conventions in `subsec:a-pre-computation`.
- `02-cactus.tex`: the smoothed grounded-Laplacian and adjoint derivation used in the nomination-face and coefficient-continuity arguments.
- `03-block-rank.tex`: the block-order maximum-principle argument and the complete `lem:a-blk-boxlp` proof, including support inequalities, realizable-sign enumeration, algebraic optimization, and zonotope lifting.
- `04-laws.tex`: the dense piecewise-polynomial input model and its fixed-law specialization.
- `07-weighted-cactus.tex`: the full statements and proofs of the affine cactus theorem and nomination-face theorem; local quadratic/radical charts; square-root panels; common partition and supremum optimization; nomination continuity; threshold elimination with ties; circulation candidates; selected-scenario recovery; and joint coefficient continuity. I also inspected the fixed-total-rank weighted reduction in `06-weighted.tex` where it uses the same box lemma.

The relevant polynomial elimination bound was checked against the original PDF of Basu's 2014 survey, Theorem 2.27 in Section 2.5.2, including its output structure, degree bounds, arithmetic count, and integer bit-size bounds. Its sampling discussion surrounding Theorem 2.16 (printed pp. 11–12) and the accompanying algebraic-representation discussion supports the fixed-dimensional sample interface. I used the survey's primary-source statement for this audit; I do not claim to have re-read the entire BPR book or all underlying algorithms.

## Literature evidence and inspected locators

- **Vigneron:** inspected the original local `literature/vigneron-2011-algebraic-sums-manuscript.pdf`, Sections 2.1 and 2.3, Theorem 6, and Section 3.2 (printed pp. 5–10). The hypotheses use nonnegative algebraic functions of constant description complexity. The scheme forms common level-set arrangements and approximates summands; the stated bit-model extension retains polynomial dependence on `1/ε`. This supports the manuscript's comparison and its attribution of approximate summation as an existing principle. The bibliography correctly identifies the October 21, 2011 manuscript locators. [Author manuscript](https://antoinevigneron.github.io/manuscripts/rational.pdf).
- **Borcea–Bøgvad–Shapiro:** inspected arXiv:math/0409353v2, Definitions 2–6 and Theorems 2–3 on printed pp. 2–3. The approximation targets the dominant root off a locus including the equimodular discriminant, pole locus, and slow-growth set; exponential convergence is asserted away from that locus. These statements do not themselves provide the new lemma's uniform original-coordinate, rational-bit, selected-branch interface through exceptional parameters. The citation is accurately limited. [Original v2 PDF](https://arxiv.org/pdf/math/0409353v2).
- **Yomdin:** inspected arXiv:1406.1719v2, Definitions 5.1–5.2 and Theorem 5.6 with its proof, PDF pages 23–25. The approximation concerns polynomial mappings approximating a set parametrization, and its complexity is a degree-based sum. The logarithmic-cubed bound for planar sets is accurately described without converting it into a rational-coefficient bit algorithm. [Original v2 PDF](https://arxiv.org/pdf/1406.1719v2).
- **Binyamini–Novikov:** inspected arXiv:1802.07577v2, Theorem 1 and its preceding algebraic lemma on printed p. 2; Section 1.5 on polynomial asymptotic notation; and Definition 33 in Section 4.1 on semialgebraic complexity, printed p. 27. The chart-count and semialgebraic-complexity bounds are polynomial in the stated geometric parameters for fixed ambient dimension. Their complexity definitions use real polynomial descriptions and do not state rational coefficient-height bounds. The manuscript's distinction is supported and does not claim that a stronger algorithm is impossible. [Original v2 PDF](https://arxiv.org/pdf/1802.07577v2).
- **Petras:** inspected the publisher abstract, retrieved through the indexed ScienceDirect publisher page after direct page opens failed. It describes algorithms enclosing integrals or functions for piecewise analytic inputs, with complexity qualifications tied to function representation. That is sufficient for the modest attribution in lines 546–548. I did not inspect or rely on a detailed Petras rate theorem. [Publisher abstract](https://www.sciencedirect.com/science/article/pii/S0377042701005866).

No inspected passage in Stage 5c claims a new classical interpolation, root-isolation, or complex-branch principle. Its unresolved several-parameter discussion is explicitly about what the present proof interfaces establish. This review is a comparison against the specified primary statements, not an exhaustive priority search across all approximation theory.

## Integration and diagnostic evidence

I inspected `complexity/main.tex`, the new bibliography entries, and the unchanged introduction/abstract/conclusion files for integration context. The new section is included once before the conclusion. The introduction and conclusion remain prior-stage placeholders; I do not treat that existing manuscript-wide status as a Stage 5c defect.

I read `process/completion-s5c-build.json` and `process/completion-s5c-checks.json`. The build record reports return code zero, a PDF, and no errors, undefined references/citations, duplicate labels, or overfull boxes. I independently recomputed all current input hashes in both manifests: there were no mismatches. I inspected this build evidence; I did not run a second LaTeX build.

I read all of `verification/check_s5c_scalar_approximation.py` and independently ran it with the recorded Python interpreter and `-O`. It passed and reproduced the recorded fixture results. The script's SHA256 is `ae633732ca9ea4f47986eb2d46ab0c35590f0bc8fdbfad5767a8d2d11ca4985e`, matching both recorded executions.

The four fixtures are the implicit quintic, a real branch switch, nearby nonreal branch points, and a nearby external pole. The run checked geometry on 3,826 panels, interpolated 35 selected panels, and checked 595 rational sample enclosures, as well as band and exact symbolic identities. Runtime checks use explicit exceptions and therefore remain active under `-O`.

The limitations are material and accurately disclosed: the graph and exceptional-root oracles are supplied for these examples; the script does not implement general graph-to-annihilator construction or general real quantifier elimination. Only selected panels are interpolated, and sampled approximation checks alone would not prove a uniform estimate. The manuscript's contour and Lipschitz arguments supply that proof. The diagnostics also do not implement the general coefficient-box elimination, hybrid network optimizer, or rational recovery algorithm. No theorem verdict above rests on treating these finite diagnostics as such an implementation.

## Findings and repairs

**Major findings: none. Minor findings: none. Required repairs: none.**

There are no optional suggestions necessary to this acceptance. The verification limitations and scope of the literature inspection are stated above so they are not mistaken for stronger evidence.
