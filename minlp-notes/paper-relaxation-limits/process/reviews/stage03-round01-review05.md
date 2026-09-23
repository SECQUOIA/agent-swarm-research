# Stage 3, round 1 — reviewer 05

**Verdict: MINOR.** I found no major defect in the Stage 3 mathematics, proof dependencies, algorithms, or required coverage. One example needs a harmless parameter restriction for its exact treewidth statement.

## Coverage

Reviewed the frozen input `process/snapshots/stage03-round01/`, specifically all of:

- `sections/04-incidence-interiority.tex`;
- `sections/05-feedback-frequency.tex`;
- `sections/06-treewidth-two.tex`;
- `sections/07-positive-boxes.tex`;
- `sections/08-exact-complexity.tex`;
- `sections/appendix-structural-auxiliary.tex`;
- `sections/appendix-positive-box-predecessors.tex`.

Read the shared envelope definitions, vertex-law representation, common upper attainment, easy-term estimate, and box transfer in `sections/01-foundations.tex`; the degree/dimension bounds and exact dyadic construction in `sections/02-universal-positive.tex`; and `sections/appendix-positive-couplings.tex`. Checked the Stage 3 bibliography entries and relevant macros. The unrelated signed-bilinear and cubic refinements are not additional premises of the new structural arguments.

Read the review protocol, Stage 3 author/reviewer assignments, all Stage 3 scope rows and later additions, the author source-to-label ledger, and `process/existing-idea-development.md`. Compared the substantive canonical proofs and linked developments named in those rows, including the later unequal-box family, both forest auxiliary lemmas, asymmetric predecessor, fixed-mixture optimality, fixed-ambient coefficient refinement, general-radix observation, and rank-one precision correction. I did not read peer reports from this review round and did not delegate.

Every required Stage 3 development has a corresponding statement or proof in the frozen text. In particular, the later bipartite lower endpoint is correctly retained as 3/2; the older 7/6 example remains a distinct rational certificate. The superseded positive-box proofs are preserved as distinct proofs. The coefficient-regularity candidate has a complete summation argument, and the general-radix extension includes attainment rather than only a surrogate estimate. Abstract/introduction integration and later spatial sections were outside this review.

Primary-source inspection was independent of accepting the coordinator's conclusions:

- Read Cornuéjols's Theorems 6.5 and 6.13 in the [author manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf), and visually inspected the original printed p.76. The first has the required rectangular Eulerian-submatrix scope; the second has the restricted mixed unit-right-hand-side scope used only in the alternative monomial argument.
- Visually inspected Hassin–Tamir's original printed p.381, Theorem 3.1 and the terminal recursion. The browser endpoint failed, but the already downloaded original scan was available. It supports the block decomposition input, not the paper's new coloring invariant. [Author scan](https://www.math.tau.ac.il/~hassin/sp.pdf).
- Read Barrus's setup and Theorem 2.1, including the distinction between fixed graphical degree sequences and the manuscript's independently proved slabs. [Original](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf).
- Read Edmonds's original abstract and Section 1 for the weighted matching primitive, and Deza–Onn's Theorem 1.2 and full Section 3 reduction. The manuscript appropriately proves its own signed-cost/private-edge/parallel-edge gadget. [Edmonds](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf), [Deza–Onn](https://arxiv.org/html/1908.09278v1).
- Read GLS Theorem 6.4.9 and the separation-to-optimization proof passage in the available original text, including the general well-described-polyhedron scope. The finite dual bound in the manuscript supplies the needed rational encoding control.
- Read the local Del Pia–Khajavirad Theorem 7 and its proof for the classical Berge-acyclic exactness comparison. Read/visually inspected Adams–Gupte–Xu Proposition 4.1 on original manuscript p.22. The latter explicitly attributes the classical product envelopes to earlier work; no new-envelope priority claim is made here.
- Visually inspected Karp's original pp.94 and 97 in the authorized reprint: the completeness theorem and PARTITION definition are present. Its signed-integer formulation is equivalent to positive integers by taking absolute values and dropping zeros in the signed-sum formulation.
- Visually inspected the original Altschuler–Boix-Adserà Section 7.2 page containing Theorem 7.4, the precision question, and Corollary 7.5. The comparison is faithful to its rational-bit qualifications and does not assert exclusion of fixed-error approximation. [Published article](https://link.springer.com/article/10.1007/s10107-022-01868-7).

Read `literature/AGENTS.md` before using local originals. These are checks of the relevant statements and passages, not claims of reading every page of every external work or reconstructing weighted matching and the ellipsoid method from first principles.

## Findings

**R05-01 — MINOR: specify `m >= 2` for the exact treewidth of the forest-coloring obstruction.**

Location: frozen `sections/appendix-structural-auxiliary.tex`, lines 99–103, paragraph beginning “In `K_{2,m}`”. The text says its treewidth is two without restricting `m`. At `m=1`, `K_{2,1}` is a tree and has treewidth one; adding the stated private variable keeps it a tree. The unbounded-color argument and all main theorems are unaffected.

Repair: write “In `K_{2,m}`, for `m >= 2`, …”, or replace “treewidth is two” by “treewidth is at most two”. The former preserves the intended exact-width example.

No other demonstrable issue found.

## Independent verification

The following checks are supplementary to reconstructed general proofs.

1. **Ownership and radix counts.** Incoming ownership requires distinct labels only at each high variable, so shared low anchors do not create incompatible assignments. The degree alternative correctly bounds a reduced polynomial's hull by the original deficiency under every law. For radix attainment, I checked the profile capacities, their bracketing of one, all pointwise equality cases including `l < s` and `l = s`, the mixture mass, and digit-reversal prefix coverage. The complete-bipartite minor really has `L-1` ancestral factors plus `a_L` on one side. Its `K_{L+1}` branch sets require and receive `b >= L`. The descending elimination creates no unrelated factor adjacency. The degeneracy/orientation lower construction correctly needs `k >= 2` because its deepest factors have degree/outdegree two.

2. **Marginal floor and joint limit.** The completion coefficient is in `[0,1]`; clipping makes the failure union certain if any unclipped probability exceeds one. The `S/u` inequality gives the stated integral without an extra loss. The lower construction has dimension `m+L`, degree `m/b+1`, and both endpoint distances at least `1/m`. The floor choice is uniform when the minimum controlling parameter diverges. It does not establish a fixed-small-width asymptotic.

3. **Repair, slabs, and baseline.** The repair residual has mass `1-1/C`, and each outside coordinate's residual states sum to the same feedback-state mass. Conditioning then leaves singleton separators on a forest. This costs one factor `C`, not a product along paths. In the degree slab, full column rank and the two-incidences count force equality throughout, giving disjoint half-valued odd cycles. Rounding yields coverage `1-1/(2l)`; combining this with convexity of the maximum marginal preserves the coverage baseline. For convex cardinality factors the rounding loss is exactly the local second difference divided by `2l`.

4. **Coloring and TU transfer.** Checked all seven series terminal-type cases and every parallel case against the active/blocking requirements. Mixed-terminal compositions need the special blocking rule and the direct-edge exception; both are present. In an Eulerian row-class submatrix, edge-disjoint cycle decomposition counts all ones, and the stronger all-cycle property makes their number divisible by four. This establishes the needed TU transfer for arbitrary integer slabs. The `K_{3,m}` example correctly distinguishes this stronger cycle property from TU and balancedness. The planar Hall argument is valid on every edge subset of a simple bipartite planar graph.

5. **Optimization.** Negative edge costs can be fixed to one because uncovered penalties are nonnegative. The hub construction preserves the prize-collecting optimum. Inclusion-minimal edge covers are disjoint stars; the selected matching and cheapest-edge charges give both directions of the asserted value identity. The slot gadget enforces two-endpoint activation and the `2W+1` bonus dominates every possible original-cost difference. The dual polyhedron is pointed, a finite optimal face has a vertex, and the zero-one basis matrix supplies the stated factorial coordinate and polynomial bit bounds, including boundary means.

6. **Positive boxes.** The induction decreases a global minimum and increases a global maximum; it does not use the false arbitrary-spreading assertion. The finite Lipschitz comparison works with dependent orientation coins. Restricting the same ambient law preserves the opposite-pair probability and all deterministic-coordinate recurrences. Coefficient summation leaves only `a_{j+1}(C_j-P_j)` for `j >= 2`; these nonnegative deficiencies permit the regularity bound and handle `L=0`. Unequal-box transfer correctly compares original-factor gaps with expanded gaps and sums deficiencies through common upper attainment. The softened-coverage bounds give an actual ratio limit and finite positive hull gaps. I also checked the low/high predecessor estimates, asymmetric crossing strips, both fixed-mixture limiting families, and unequal-box vertex residuals/attaining laws.

7. **Complexity and boundaries.** The PARTITION expansion has nonnegative remainder bounded by `epsilon^2/8`; the NO variance is at least one because the doubled target is integral. The basic-law certificates have at most `n+1` or `n+2` states as appropriate. The tilted square identity gives the weighted-oracle precision barrier directly. Padding preserves rank, means, costs, and optimal values. The rational-power second derivative and Taylor coefficients have the claimed signs. The exact parity example has local minima zero as well as maxima one, so it is a width counterexample; the independent-set extension deliberately claims payoff maxima only.

New independent checkers and their saved outputs are under `verification/reviewer05/stage03-round01/`:

- `check_combinatorics.py` / `.json`: exact enumeration of all 4,096 simple bipartite supports with three variable and four factor vertices; 3,845 admit width-two elimination and every such support admits the required all-cycle coloring. Width testing explores available eliminations with clique fill. Also 319 rational radix profile/cutoff cases (`b=2,...,12`, `L=2,...,30`), 294 integer prefix-hit cases, five explicit prescribed elimination orders, 10,920 odd-cycle subsets at lengths 3 through 13, and all 64 parity assignments. All passed.
- `check_moments_matching.py` / `.json`: 210 exact rational ambient-orientation/coefficient-regularity cases with `N=2,...,7`, proper restrictions, deterministic means and `L=0`; both printed arbitrary-spreading values; and 100 integer matching-gadget optima compared with exhaustive original binary optimization, including parallel edges and signed costs. All passed. NetworkX's weighted matching was used on integer weights; the moment calculations use `Fraction` and interval integration, with no floating-point LP.

These enumerations validate the stated finite cases. They do not prove the universal graph theorem, coefficient inequality, or general radix theorem; the analytic arguments above remain necessary.

## Remaining limits

I found no unresolved nonclassical premise of a Stage 3 theorem. External weighted-matching and rational-oracle equivalence are accepted classical inputs after checking their scopes; their entire algorithmic proofs were not re-audited. I did not repeat the author's complete PDF build/layout pass or the exploratory width-three searches. The frozen proofs, rather than those search records, support the universal results.

This review does not certify publication priority. Exact `W_k` for `k >= 3`, universal larger-width row partitions, sharp planar constants, the exact finite-aspect positive-box constant, and the unequal-aspect bipartite supremum remain correctly open. The fixed-mixture limitation is not global optimality, and the single-product hardness result does not establish strong NP-hardness or hardness at fixed additive error.
