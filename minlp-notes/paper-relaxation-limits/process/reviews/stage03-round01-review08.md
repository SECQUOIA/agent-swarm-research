# Stage 3, round 1 — reviewer 08

- **Verdict:** PASS.
- **Findings:** None. I found no demonstrable major or minor defect in the assigned frozen Stage 3 mathematics. This verdict does not certify publication priority or settle the questions expressly left open.

**Coverage**

I reviewed these complete files in `process/snapshots/stage03-round01/sections/`:

- `04-incidence-interiority.tex`;
- `05-feedback-frequency.tex`;
- `06-treewidth-two.tex`;
- `07-positive-boxes.tex`;
- `08-exact-complexity.tex`;
- `appendix-structural-auxiliary.tex`;
- `appendix-positive-box-predecessors.tex`.

I read the shared envelope/distribution, deficiency, easy-term and positive-box-transfer foundations in `01-foundations.tex`; the dyadic construction, harmonic laws, finite bounds and leading asymptotics used from `02-universal-positive.tex`; and `appendix-positive-couplings.tex`. I checked the relevant bibliography and notation. Accepted signed-bilinear mathematics and the unrelated cubic certificates were not re-audited. Introduction and abstract integration belongs to Stage 6 and is outside this assignment.

I read `process/stage-03-review-assignment.md`, `process/review-protocol.md`, `process/stage-03-author-assignment.md`, the complete author coverage ledger, all Stage 3 rows of `process/scope-proposal.md`, and `process/existing-idea-development.md`. I compared the manuscript with the mapped canonical incidence-sparsity, incidence-growth, marginal-floor, joint-growth, feedback, frequency-two, frequency-two-optimization, convex-cardinality, treewidth-two, binary-payoff, positive-box, positive-box-sharp, positive-box-lower and single-product-hardness results. I also read the mapped asymmetric, independent, fixed-mixture, balanced-orientation, unequal-box, structural-auxiliary, general-radix and rational-power notes, including their later corrections. No current-round peer report was read, and no subagent was used.

All required substantive additions are represented: the later bipartite family approaching 3/2; both distinct forest lemmas; the asymmetric predecessor and exact failed all-high inequality; fixed-mixture optimality; the coefficient-regularity refinement; and the general-radix cutoff extension. I did not treat a stronger later estimate as invalidating an earlier valid estimate.

**Independent verification**

1. **Incidence laws and radix attainment.** I reconstructed the incoming ownership law as a partition of each high variable's relevant incidences into at most `r` rounds. The circular arcs are feasible even when an individual failure probability exceeds its owner's anchor mean: the missing length fits outside the anchor interval. Shared low anchors create no conflict because only the owned high coordinates require exclusive assignment. The outgoing reduced-polynomial argument correctly compares total deficiencies under every common-marginal law; it does not assume that an arbitrary degree bound supplies a simultaneous individual-term law. Zero `r` or `s` is handled by omitting the corresponding component.

   For the radix family, I checked the upper-tail rearrangement, both profile means, digit-reversal hit counts and transitive digit shifts, the factor-elimination neighbor count, and the `K_(L,b)` minor. The treewidth equality uses `b >= L`. The stronger degeneracy/orientation lower family uses `L=k+1` with `k>=2`; the deepest factors' degree/outdegree two is compatible exactly in that range. These give supremum limits, without asserting finite attainment of the limiting constants.

2. **Uniform asymptotics and parameter dependence.** In the marginal-floor law, `m_q <= q < 1` makes completion valid; clipping is treated separately before the exponential union estimate. The finite integral is positive, and its upper and lower estimates imply the claimed asymptotic. The floor restriction applies to normalized evaluation means on the original envelope domain.

   For joint growth, write `h=min(k,phi(q))`. Its divergence forces both `k` and `q` to diverge, so the separate upper-bound relative errors vanish uniformly along every allowed sequence. For the lower law, `L=floor(h)` satisfies `L/h -> 1`. Since `L<=phi(q)`, the floor in `b=floor((q/2)^(1/L))` still gives `b >= (1-o(1)) log(q)`, hence `L/b -> 0`. The same instance obeys dimension, degree, width and both marginal-strip restrictions. The proof neither substitutes the simplified dyadic formula outside its cutoff range nor implies a fixed-small-width asymptotic.

3. **Feedback and frequency two.** The reference law dominates every required `(F,i)` marginal entry by the claimed factor. Residual masses have matching sums and yield consistent conditional singleton marginals. Conditional forest gluing loses no additional factor along paths. For physical products, the affine majorant is defined within the original scope, so expansion does not alter the structural hypothesis.

   I reconstructed the slab rank count: full column rank gives `|J|<=|R|`, while integer tight residual degrees and two endpoints give the reverse inequality. Equality forces vertex-disjoint cycles; even cycles have a null perturbation, and odd cycles force half-values. Odd-cycle rounding preserves each edge marginal and yields coverage `1-1/(2l)`. Retaining the convex baseline `b_v` through averaging is essential and is done correctly. The cardinality proof uses exact lower-envelope affinity on each slab and upper-envelope concavity; the rounding excess is the local curvature gap divided by cycle length. Negative or nonmonotone convex tables cause no exception.

4. **Rational algorithms.** Both reductions handle arbitrary signed linear oracle costs. In the edge-cover construction, selected negative-cost edges zero their endpoints' penalties; the hub/mate construction handles isolated remaining vertices. The two comparison inequalities in the cheapest-edge/matching proof establish equality of optimal values. In the cardinality gadget, covering both mandatory vertices enforces either two active slots or the inactive edge, and slot reassignment selects the cheapest increments. The bonus `2W+1` exceeds every possible original-cost difference. The dual rows span the full affine-coordinate space, so an attained optimal face has a vertex; the stated determinant bound and rational encoding sizes suffice for exact separation-to-optimization. Boundary means do not require full dimensionality. The conclusion is correctly limited to the scalar graph hull.

5. **Width two and structural boundaries.** I checked each of the seven series terminal-type cases and all equal/mixed terminal parallel cases in the active/blocking invariant. Mixed even-parity components used for blocking cannot have a direct terminal edge. Parallel compositions activate compatible parities or block one component; the factor-terminal correction in cycle parity is correct. Block color swaps preserve the invariant. For either factor color, every Eulerian support decomposes into cycles whose lengths are multiples of four, giving precisely the Camion condition needed for arbitrary integer slabs.

   The fixed-positive-aspect flower proof holds with aspect ratio fixed while dimension grows; its tail split gives `H_n -> alpha > 0`. The six-variable parity example independently supplies both local extrema and both full extrema. The independent-set extension claims payoff maxima, not an unproved general width formula. The canonical-pair residual law, triangle residual obstruction, twin compression and signed forest gluing have the stated scopes. `K_(2,m)` and `K_(3,m)` obstruct their specified coloring methods, not the general gap theorems.

6. **Positive-box coefficients and predecessor proofs.** The pair base case uses the probability of opposite orientations, which remains `1/beta_N` on every restriction. Deterministic deletion retains the ambient distribution rather than conditioning or resampling its coins. For an extremum-spreading step, the exact changes of the two common-threshold moments are `-Bh` and `-Dh`; the independent-moment change is at most `Dh`; and coupling the same coins gives `Delta O_j >= -Bh`. Thus the complete finite change has the required sign. The sum-preserving step fixes `V_j`; boundary induction and the overflow order cover all remaining cases.

   Summing these inequalities with nonnegative cardinality coefficients gives the `L+1+beta_N` constant using only the ratio restriction at orders at least two. Affine deficiencies vanish, including `L=0`. Positive affine transfer to unequal boxes compares original and expanded term gaps in the correct direction and preserves the original factor's summed upper value. I checked the distinct symmetric and asymmetric estimates, the counterexample values, and both fixed-mixture test families. The order of limits in the latter is first epsilon to zero at fixed arity, then arity to infinity. Their conclusion is limited to fixed independent/fair-orientation mixtures.

   The physical radix lower bounds squeeze `H_L/L` to `epsilon*alpha` at each fixed positive aspect ratio and prove finite positivity. The unequal-box residual certificates and all attaining laws give the stated exact ratio and unit-coefficient rescaling; no finite search is used to claim the open upper bound 3/2.

7. **Complexity and rational-power boundary.** The product expansion and nonnegative remainder give separated YES/NO intervals of widths controlled by `epsilon^2`. Doubling the PARTITION numbers preserves feasibility and makes the target integral. Basic distributions give the stated polynomial rational certificates. The graph-hull reduction separately checks its upper endpoint. Enumeration by ratio-group counts is exact, including signed dual potentials. The tilted square identity proves the weighted rank-one oracle result directly; padding meets the dimension-based input-bit convention without changing the value. The deterministic and randomized assumptions remain distinct, and no strong or fixed-additive-error hardness is claimed. The rational-power curvature, secant widths and leading Taylor coefficients give divergence only in the original coordinate; logarithmic reparameterization makes this example's widths equal.

I wrote and ran an independent exact checker, `verification/reviewer08/stage03-round01/check.py`. Its output is in `check.json` beside it. It passed 270 ambient-coefficient vectors, 74 global-extremum spreading moves, 270 coefficient-regularity vectors, and 649 radix cutoff instances. The coefficient cases include dimensions 2 through 7, proper restrictions, odd ambient dimensions, deterministic means and `L=0`. The radix cases cover every `b=2,...,12`, `L=2,...,60`, including cutoffs outside the simplified `b>=L` formula. These are exact rational checks of finite cases, not proofs of the universal statements.

**Primary-source verification and remaining limits**

I read `literature/AGENTS.md` and the coordinator/author source records before local source use. I directly checked the following source passages:

- Cornuejols, printed pp.76 and 82: Camion's rectangular Eulerian-submatrix criterion and the distinct mixed balanced-integrality theorem. I also visually inspected p.76 in the original.
- Hassin–Tamir, printed p.381 in the original scan: Theorem 3.1 and the series-parallel setup, with attribution to Dirac and Duffin.
- [Barrus, Theorem 2.1](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf): its graphic fixed-degree scope is narrower than the manuscript's locally proved slab lemma.
- [Deza–Onn, Theorem 1.2 and Section 3](https://arxiv.org/html/1908.09278v1): the convex-degree matching mechanism is established prior work. I read the complete matching proof.
- [Edmonds's original matching paper](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf): checked the source identity; weighted matching itself is used as a classical primitive, not re-proved in this review.
- GLS, printed p.179, Theorem 6.4.9 and its separation-to-optimization proof: the well-described rational-polyhedron formulation matches the use here.
- Adams–Gupte–Xu, original manuscript p.22, Proposition 4.1: visually checked the common-ratio envelope formulas and their prior attribution. Sherali's local extracted Section 3 confirms its elementary-symmetric scope; its displayed formulas are imperfectly extracted, so I do not claim a new complete visual audit of Sherali.
- Del Pia–Khajavirad, Section 3, Theorem 7: checked the standard-linearization/Berge-acyclicity statement. The local extraction is noisy; the manuscript's scalar gluing proof is independently complete.
- Karp, original printed pp.94 and 97 in the authorized reprint: visually checked the completeness statement and PARTITION definition. Replacing signed entries by absolute values is justified through the equivalent zero signed-sum condition; zero entries can be deleted.
- Altschuler–Boix-Adsera, local primary Section 2 and Section 7.2, including a visual check of the precision question after Theorem 7.4: the manuscript correctly distinguishes the source's arithmetic-operation convention from its own rational-bit hardness consequence.

I traced the width-three counts to the saved 3,000-support and 300-support search summaries and inspected the relevant generator/oracle routines, but did not independently rerun those exploratory searches or audit every implementation detail. They are presented as finite evidence only. I did not rebuild the frozen manuscript or perform a complete PDF layout review. None of these limits supplies a mathematical objection to the locally proved statements. Exact larger-width constants, the finite-aspect optimum, the unequal-aspect bipartite constant, and later-literature priority remain unresolved as stated.
