# Stage 3, round 1 — independent review 07

**Verdict: PASS.** No major or minor correction is requested. The additional review emphasis was algorithms, rational encoding, complexity, and output guarantees; the mathematical review covered the entire stage.

## Coverage

The reviewed manuscript is the frozen input under `process/snapshots/stage03-round01/`. I read all of:

- `sections/04-incidence-interiority.tex`;
- `sections/05-feedback-frequency.tex`;
- `sections/06-treewidth-two.tex`;
- `sections/07-positive-boxes.tex`;
- `sections/08-exact-complexity.tex`;
- `sections/appendix-structural-auxiliary.tex`;
- `sections/appendix-positive-box-predecessors.tex`.

Dependencies checked were the vertex-law, exact monomial-envelope, common-upper, deficiency, easy-term, and nonnegative-box-transfer arguments in `sections/01-foundations.tex`; the dyadic exact construction and cutoff, harmonic laws, finite degree bound, and degree/dimension leading asymptotics in `sections/02-universal-positive.tex`; and the relevant alternative dyadic/coupling material in `sections/appendix-positive-couplings.tex`. I checked the Stage 3 reference entries. I read the review protocol, author assignment, all Stage 3 scope rows and additions, the author row-to-label ledger, and the source-check records. Introductory and abstract integration belongs to Stage 6 and is not a missing Stage 3 deliverable.

The canonical sources consulted cover the four incidence/interiority results; feedback, frequency-two, frequency-two optimization, convex cardinality and width-two results; the general-factor counterexample; all three canonical positive-box results; and single-product hardness. I also read the substantive source notes for the asymmetric predecessor, independent low/high investigation, fixed-mixture comparison, coefficient regularity and balanced-orientation closure, both unequal-box examples, canonical forest pair laws, twin compression, forest-cover obstruction, width-three boundaries, radix capacity extension, rational powers, and rank-one precision. The manuscript preserves the later corrections: finite spreading replaces differentiation, the ambient balanced coins are restricted, the later bipartite lower endpoint is 3/2, and the generalized radix statement uses its own capacity cutoff.

I read `literature/AGENTS.md` before inspecting local primary material. Direct checks included:

- Camion's rectangular Eulerian-submatrix statement in Cornuéjols, Theorem 6.5, visually checked on printed p.76; the extracted Theorem 6.13 mixed balanced-matrix statement and its unit bounds. Their different scopes are respected.
- Hassin–Tamir, printed p.381, visually checked: Theorem 3.1 and the series-parallel construction support the block-decomposition input. The coloring invariant itself is proved locally.
- [Deza–Onn, Theorem 1.2 and Section 3](https://arxiv.org/html/1908.09278v1): the established convex-degree matching mechanism is properly attributed; the manuscript supplies its particular signed-cost, private-edge, and parallel-edge reduction.
- [Edmonds's original weighted-matching paper](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf), abstract and Section 1, for the weighted matching primitive.
- GLS, original first-edition text, Theorem 6.4.9 and its proof on printed pp.179–180, for exact rational optimization from strong separation. The manuscript supplies polynomial description and coordinate bounds.
- [Barrus, Theorem 2.1](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf/), whose fixed-degree graphic scope is narrower than the locally proved slab lemma; the manuscript does not confuse the two.
- Adams–Gupte–Xu, Proposition 4.1, visually checked on printed p.22, including its antecedent attribution; Del Pia–Khajavirad, Theorem 7, in local extracted text, for classical Berge-acyclic exactness.
- Altschuler–Boix-Adserà, visually checked published Section 7.2, Theorem 7.4, the subsequent logarithmic-accuracy question, and Corollary 7.5. The comparison is explicitly historical and restricted to rational bit complexity. [Published source](https://link.springer.com/article/10.1007/s10107-022-01868-7).

The standard PARTITION NP-completeness input and shared earlier source audits remain external classical inputs; I did not independently read Karp's complete scanned reduction or reprove the classical matching/ellipsoid theorems. These limits do not leave a new Stage 3 mathematical step unsupported. No report from this review round was read, and no manuscript file was edited.

## Findings

None. In particular, I found no unsupported claim of a compact lifted-polytope formulation, fixed-additive-error hardness, strong NP-hardness, universal finite-search conclusion, or exact finite-aspect-ratio optimality.

## Independent verification

1. **Orientation, radix, and joint limits.** Disjoint high-variable ownership makes each round compatible even when low anchors are shared. Capped-sum subadditivity supplies the incoming bound; the outgoing degree argument only needs a polynomial-level gap bound, as written. For general radix, the two capacities are the means of the stated integer profiles, and both profiles lie in the equality segments of the affine bound. Digit reversal and coordinatewise shifts give every leaf failure marginal exactly `1/m`. The elimination order and `K_(L,b)` minor prove the width claim in its stated range. For the joint construction, `b >= (1-o(1)) log q` and `L/b -> 0`, while the dimension, degree, width, and two-sided mean restrictions hold on the same family. No fixed-small-width asymptotic is inferred.

2. **Marginal completion and feedback.** The completion coefficient is in `[0,1]`, integrates to the exact missing failure mass, and includes zero failures. The clipped case makes a failure certain and is correctly separated from the exponential product bound. In feedback repair, each residual has mass `h_s`, each repaired law has the same `(F,i)` marginals, and conditioning leaves a forest with singleton separators. Thus there is one factor `2^f_F`, with no pathwise multiplication. The physical-product affine majorant stays inside the original scope. The flower inequality `AR + 1[R>=1] <= R+A` gives the exact stated hull value.

3. **Frequency two and cardinality.** Full column rank and the incidence count force every fractional slab component to be an odd half-valued cycle, including with dummy and parallel edges. Averaging preserves the coverage baseline because `E b_v(Z) >= b_v(p)`. For cardinality tables, a rounded cycle vertex incurs exactly its second-difference gap divided by the cycle length; adjacent-cardinality lower attainment and concavity of the local upper envelope give the required averaged inequality even for negative or nonmonotone convex tables.

4. **Both matching reductions and their outputs.** Selecting every negative failure-edge cost is valid because penalties are nonnegative. The hub/mate construction preserves the prize-collecting objective in both directions. For the edge-cover identity, a minimal nonnegative-cost cover is a star forest; choosing one star edge as a matching charges all remaining edges to distinct unmatched leaves. For the cardinality gadget, full mandatory coverage forces either the inactive edge or two endpoint slots. Cheapest-slot reassignment gives the telescoping degree costs. The `2W+1` bonus dominates any change of original matching cost, also for signed costs. These constructions recover an actual optimizing binary assignment, so they provide strong separation, not only an approximate numerical objective.

5. **Exact rational envelopes.** The dual rows `(1,z)` span the space, hence its attained optimal face has a vertex. Cramer's rule bounds each coordinate by `(n+1)! A`; this is a magnitude bound with polynomial encoding length, and clearing input denominators supplies polynomial rational precision. It works at boundary means. The separation oracle returns a violated vertex inequality, and GLS supplies an optimizing rational dual vector, hence a supporting affine minorant. Sorted threshold pieces supply a valid upper separator. Products and explicitly supplied convex tables have polynomial-bit vertex values. Grouped ratio enumeration uses the largest dual coefficients within each fixed count and gives `(n+1)^k` candidates, without an implicit fixed-precision assumption.

6. **Width two and boundaries.** I checked the seven series terminal cases and all parallel cases, including the direct-edge case and distinct factor-terminal colors. The XOR correction counts the shared factor once in series and the factor terminals once on a crossing parallel cycle. Block color swapping preserves articulation consistency. Camion applies because every Eulerian support decomposes into cycles of length divisible by four. TU, rather than balancedness alone, justifies arbitrary integer cardinality slabs. The positive-aspect flower estimates with `M=sqrt(n)` give the sharp limiting ratio two. The parity example has both the claimed minima and maxima; the independent-set generalization only claims payoff maxima. The pair-law residual, triangle obstruction, thinning/conditional compression, and signed forest gluing are valid at zero-probability conditioning states.

7. **Positive boxes.** In the coefficient proof, the finite change of the independent moments is bounded by `D h`, and the same-coin coupling gives `Delta O_j >= -B h`; these cancel the common-threshold decrease with the required sign. Boundary deletion restricts the fixed ambient distribution, including for odd ambient dimension. The order-two base uses the exact pair opposite-orientation probability, while overflow orders and Pascal identities close induction. Summing with nonnegative binomial coefficients proves `L+1+beta_N`; `L=0` causes no exception. Unequal-aspect transfer uses an affine bijection and a nonnegative expansion, with common upper attainment justifying the per-original-factor guarantee. The coarse and asymmetric proofs retain their separate valid estimates. Fixed-mixture optimality uses sequential limits and is properly restricted. The softened-coverage family has a positive finite hull gap and the claimed fixed-aspect limit. Both bipartite certificates have compatible marginals and nonnegative vertex residuals.

8. **Hardness and accuracy.** Doubling the PARTITION integers preserves the decision and gives an integral midpoint target. The quadratic expansion, positive remainder bound, variance separation, and explicit tilted-square identity yield a strict gap between `epsilon^2/8` and `epsilon^2/2`. All constructed numbers have polynomial binary length. Basic feasible laws give `n+1` states for threshold certificates and `n+2` for graph-hull membership, with polynomial-bit weights. The graph-hull upper condition holds on reduced instances. Choosing accuracy `epsilon^2/32` decides PARTITION; padding by fair `(1,1)` modes preserves rank, values, and weighted minima. The result concerns potentially exponentially fine accuracy, and keeps deterministic versus randomized assumptions distinct. The rational-power secant formulas and first/second-order expansions establish the final representation boundary.

I wrote and ran `verification/reviewer07/stage03-round01/check_exact.py`, with results saved in the adjacent `check_exact.json`. All computations use integer or `Fraction` arithmetic:

- all 729 cost vectors in `{0,1,3}^6` on `K4` satisfy the edge-cover/matching identity, comparing exhaustively enumerated covers and matchings;
- all 256 four-item PARTITION inputs from `{1,2,3,4}^4`, doubled as in the proof, pass 4,096 binary-vertex identity, remainder, primal/dual, and tilted-accuracy checks (104 YES and 152 NO instances);
- all 243 signed rational dual vectors from `{-3/2,0,5/3}^5` give identical full-enumeration and grouped-count optima for ratio groups of sizes three and two.

These finite checks supplement the preceding general derivations. I also independently read the final JSONL summary records confirming 3,000/212 balanced-class search counts and 300/281 TU search counts; I did not rerun those exploratory generators or treat their counts as universal results.

## Remaining limits

This review does not certify publication priority or absence of later antecedents. It does not determine the open exact constants at larger width, sharp planar constants, finite positive aspect ratio, or unequal-aspect bipartite frequency two. No new universal theorem is inferred from the finite tests. I did not independently rebuild or visually audit every page of the cumulative PDF; the review concerns mathematical correctness, stated algorithmic guarantees, source scopes, and Stage 3 coverage of the frozen text.
