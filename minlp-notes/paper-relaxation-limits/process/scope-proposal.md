# Scope and staged coverage proposal

Date: 2026-09-05. This is a repository inventory and authoring plan, not a fresh proof audit. Existing internal review labels are evidence to inspect, not mathematical certification.

## Paper scope

The core is the quantitative loss from separately convexifying interacting polynomial terms, and the size of spatial certificates under explicitly specified node oracles. The two main families use different signs and domains: positive multilinear gap comparisons are principally on nonnegative boxes; the strongest spatial transfer uses signed cubic XOR objectives on [-1,1]^n. The paper must not imply that the positive-gap lower examples themselves give the spatial lower bound.

Include all substantive core results and distinct proofs. Superseded constants can be explained compactly and their genuinely different arguments placed in appendices. Preserve exact witnesses and finite refinements. Do not reproduce historical agent conversation or discovery logs in the manuscript.

Rank-one conic lift size, FBBT, and scaling disjunctions are related supporting developments. Give a concise, accurately cited discussion explaining which other computational resource each concerns. They need not become full independent proof chapters in this paper. Rank-one optimization, pooling algorithms, integer-dimension approximation, Benders, and unrelated process-network complexity are outside the selected topic.

## Six authoring stages

Each numbered stage requires one author, 15 independent reviewers of the full assigned text and shared dependencies, a separate fixer for accepted issues, and another 15-review round whenever the coordinator judges that a major issue occurred. Only proceed when no major issue remains. Each reviewer has an additional focus but must inspect the whole assigned stage. The final review covers the complete cumulative manuscript.

1. **Foundations and signed bilinear comparison.** Create a compilable manuscript, notation contract, preliminary introduction, envelope/distribution lemmas, gap and oracle definitions, and the bilinear density theorem with elementary proof and correct older attribution.
2. **Universal positive multilinear laws.** Dyadic lower construction and exact hull value; sharp degree/dimension upper bound; optimized finite bound; coefficient removal; cubic witnesses and upper bound; equal means. Include distinct coarse arguments and exact numerical certificates in appendices.
3. **Structure and geometry.** Incidence orientations and variable-radix sharpness; marginal-floor/joint laws; feedback; frequency two and convex-cardinality factors; treewidth two; positive-box bounds and finite-dimensional refinement; unequal-box counterexample and exact single-product complexity boundary. This is the largest stage; use coherent subsections and appendices rather than removing results.
4. **Fractional-cardinality spatial certificates.** Base chord lower/upper tree bounds; SDP–RLT; self-contained moment positivity and higher SOS; unique-minimizer perturbation; coordinate product domains/univariate lifts; increasing concave relative-gap construction; explicit escape cuts and decomposition limits.
5. **XOR and reformulation-resistant certificates.** Classical signed-character input and its verified source conventions; exact quadratic moment hull transfer; occurrence-controlled family; bounded monomial lifts; arbitrary coordinate domains; finite order-two upper certificates; degree/region tradeoff; affine-branching obstruction.
6. **Complete paper integration.** Rewrite introduction/abstract around final contributions; reconcile notation and all source attributions; include supporting comparisons to rank-one/FBBT/scaling; close bounded unfinished derivations where justified; preserve genuine open questions; produce claim coverage and verification appendices and a complete bibliography. Then conduct the separate whole-paper 15-review/fix loop requested by the user, compile and inspect the PDF.

## Notation contract

- For compact box B and scalar function f, use vex_B f and cav_B f for lower convex and upper concave envelopes. Define H_B(f;x)=cav_B f(x)-vex_B f(x).
- For a specified factorization f=sum_e f_e, define T_B(f;x)=sum_e[cav_B f_e(x)-vex_B f_e(x)]. T depends on the factorization; H does not. For signed bilinear terms this is the McCormick gap. State T>=H>=0; form ratios only when H>0.
- Use E for factor supports, a_e>=0 for positive coefficients, d for maximum degree, n for original dimension. Delete affine summands when discussing gaps, retaining them for optimization values. Coefficient removal may change dimension.
- Use rho_G for maximum induced edge density, rho_B for box aspect ratio, w for incidence treewidth, f_F for the number of feedback variables, nu for frequency, and delta for the lower normalized marginal. Do not reuse rho for three unrelated quantities.
- Unit-cube means and physical positive-box coordinates are different. Write z_i=ell_i+(u_i-ell_i)p_i when passing to endpoint means p_i. Zero-lower scaling preserves incidence; positive affine expansion may not preserve factor structure.
- Define R_d (degree supremum), C_n (dimension supremum), W_w/D_w/P_w (structural suprema), C_delta (marginal floor), C_box(rho_B). The joint asymptotic holds as the minimum controlling parameter tends to infinity, not for fixed width.
- For spatial results use r for node order (degree 2r), K for demand, T_* for pruning threshold, epsilon for absolute tolerance, theta for relative tolerance. Explicitly define whether an oracle imposes linear moment inequalities or their localizers.
- Count certified final regions in arbitrary covers. Ordinary complete split trees have at least this many leaves; discarded regions from propagation must also be certified or accounted for. Bounds concern the stated oracle and branching coordinates, not unrestricted algorithms.
- A node's exact quadratic moment hull is the hull of its full coordinate domain, not of its feasible graph. In the lifted theorem this distinction is essential even when the objective is linear.

## Core source-to-claim coverage

Paths below are relative to the repository root. Every row should receive one or more final manuscript labels in the coverage ledger.

### Stage 1

| Source | Coverage |
| --- | --- |
| results/mccormick-gap-degeneracy-bound.md | Cut-range and half-integral identities; 4 sqrt(rho_G), 4 sqrt(degeneracy), 2 sqrt(max degree); stronger bipartite bound; zero-support conventions; complete/bipartite examples and local versus global cut distinctions. |
| results/mccormick-hereditary-density-characterization.md | Per-graph worst coefficient gap between max{1,sqrt(rho_G/(2 log 2))} and 4 sqrt(rho_G); full signings; localization at {0,1/2} points; nonzero coefficient restriction; established Schur-multiplier implication and explicit elementary transfer. |
| results/positive-multilinear-degree-upper-bound.md, preliminary sections | Vertex-law envelope characterization, common upper attainment, nonnegative deficiency identity, and correct original-versus-expanded gap inequality. |

### Stage 2

| Source | Coverage |
| --- | --- |
| results/positive-multilinear-gap.md | Sparse dyadic unit-coefficient counterexample; exact hull formula s+(L-s)2^-s with cutoff conditions; arbitrary/nested partitions distinction; original conjecture resolution; dense predecessor and homogeneous reduction where distinct. |
| results/positive-multilinear-degree-upper-bound.md | Distinct dyadic-coupling O(log d) proof and tail-integral lemma, retained compactly in appendix; nonnegative-box transfer. |
| results/positive-multilinear-sharp-degree-growth.md | Harmonic coupling; explicit universal finite bound; leading constant one for log d/log log d; matching dimension interpolation; valid global distributions independent of factor/objective. |
| results/positive-multilinear-second-order-upper.md | Optimized cutoff M; integral fixed point; Lambert-W finite certificate; denominator log log d-log log log d+o(1); no matching second-order lower claim. |
| results/positive-multilinear-coefficient-removal.md | Cloning equality of both full envelopes; random coefficient sampling uniform over all clone vertices; homogeneous, unit coefficients and strictly interior means preserve degree-based supremum; no fixed-dimensional or small-size assertion. |
| results/positive-cubic-gap.md | Finite 18-, 24-, 192-variable exact certificates, homogeneous/interior variants, predecessor 8/3 orientation upper proof where distinct. |
| results/positive-cubic-analytic-family.md | Scalar affine minorant, positivity certificate, limiting 483/223 and certified improvement 1610000/743033; distinguish finite attainment from supremum. |
| results/positive-cubic-two-level-family.md | Two means >=1/2; limit 243/115; exact 32-variable 135/67; explicit 52-variable homogeneous unit-coefficient interior witness with bound 2700/1343. |
| results/positive-cubic-rounding-upper-bound.md | Global mixture 18O/31+6I/31+7B/31 and 31/12 upper; mixture-family optimality is not global optimality of the cubic gap constant. |
| results/positive-multilinear-equal-marginals.md | Exact finite-dimensional maximization formula, dimension-free degree optimization, sharp factor two, classical elementary-symmetric envelopes. |

### Stage 3

| Source | Coverage |
| --- | --- |
| results/positive-multilinear-incidence-sparsity-gap.md | Oriented variable/factor outdegrees r,s give r+min{s,B(s+1)}+kappa; distinct incoming ownership and outgoing threshold/degree arguments. Earlier open treewidth-two sentence is stale. |
| results/positive-multilinear-incidence-sharp-growth.md | Variable-radix exact hull 1+(L-1)/b; digit reversal attainment; exact treewidth; W(k)>=k, D(k),P(k)>=k+1; all three asymptotic to k; sharp intermediate coupling parameter. |
| results/positive-multilinear-marginal-floor-gap.md | Exact-marginal completion law; finite integral bound; sharp log(1/delta)/log log(1/delta); one-sided and two-sided strips; normalized evaluation-point restriction, not a changed envelope domain. |
| results/positive-multilinear-joint-gap-growth.md | One lower family meets dimension, degree, width and marginal restrictions simultaneously; uniform joint leading constant; degeneracy/orientation alternatives. |
| results/positive-multilinear-feedback-gap.md | Universal law domination; local-law repair and conditional forest gluing; factor 2^f_F on arbitrary nonnegative boxes without positive expansion; sharp f_F=1. |
| results/positive-multilinear-frequency-two-gap.md | Dual multigraph with dummy vertices, half-integral degree-slab decomposition, odd-cycle loss with baseline retained; sharp g/(g-1), bipartite scalar exactness and 3/2. |
| results/positive-multilinear-frequency-two-optimization.md | Exact rational scalar convex-envelope/minorant oracle from prize-collecting edge cover and LP duality; no polynomial-size lifted polytope claim. |
| results/convex-cardinality-frequency-two-gap.md | Multiaffine interpolants of discrete convex cardinality sequences; common upper attainment; sharp odd-girth bounds; common-aspect positive products and matching optimization. |
| results/positive-multilinear-treewidth-two-exact.md | Full series-parallel active/blocking invariant; one-sided factor coloring; Camion two-TU-row corollary; exact gap two; cardinality and common-ratio positive-box extensions with sharpness. |
| results/binary-factor-width-two-counterexample.md | Six fair variables and three nonnegative multilinear factors give exact factorwise width ratio three at incidence treewidth two and variable frequency two. Include parity/complement laws and the independent-set payoff family with incidence width max{2,tw(G)}; distinguish payoff maxima from width ratios in the general family and mixed-sign expansions from positive monomials. |
| results/positive-multilinear-positive-box.md | Earlier independent/orientation low/high analysis and finite bound 4R+6+2/R; superseded as a bound, retain separate proof only in appendix. |
| notes/positive-box-asymmetric-upper-predecessor.md | Distinct superseded asymmetric low/high proof of2+(rho_B+1)/(1-3/sqrt(rho_B)) forrho_B>=64, giving leading constant one before the coefficient proof. Retain compact appendix derivation. |
| notes/positive-box-independent-investigation.md; notes/positive-box-investigation.md | Exact all-high counterexample to independent factor2 at deviations(1/2,49/100,1/100); earlier67 bound can be derived within the general coarse argument without duplication. Two test families prove rho_B+2 optimal only for fixed independent/fair-orientation mixture with per-term guarantees; not optimality of the true polynomial gap. |
| results/positive-multilinear-positive-box-sharp.md | Coefficient induction via finite spreading; rho_B+2; unequal-box positive affine transfer; no box-inclusion shortcut. |
| notes/review-positive-box-balanced-orientation-closure.md | Actual completed theorem in a review note: rho_B+beta_N, beta_N=2-2/N (even), 2-2/(N+1) (odd); restriction of fixed ambient balanced law, not resampling after deleting coordinates. Include proof. |
| notes/positive-box-rho-plus-two-proof.md | Distinct coefficient-regularity cardinality corollary giving L+3 under stated coefficient-ratio hypotheses; exact counterexample to arbitrary Schur-concavity/spreading; inspect and finish any bounded missing argument before promotion. |
| results/positive-multilinear-positive-box-lower.md | Fixed-rho lower family with softened coverage; exact termwise formula and matching-order hull estimate; max{2,rho_B} lower; rho_B+O(1), not exact finite-rho value. |
| notes/multilinear-frequency-two-positive-box-obstruction.md | Explicit three-variable unequal-aspect bipartite example with ratio 7/6; does not disprove universal 3/2 in that larger class. |
| notes/multilinear-frequency-two-positive-box-investigation.md | Later exact bipartite epsilon family with ratio2(epsilon+3)/(3epsilon+4) approaching3/2; unit-coefficient rescaling; two-term upper2; signed arbitrary-box forest gluing; conflict-color upper bound and bipartite upper2; weighted exponential representation. Exact bipartite supremum lies in[3/2,2] and remains open; numerical searches establish no universal bound. |
| results/positive-box-single-monomial-hardness.md | Exact midpoint envelope NP-complete on arbitrarily narrow unequal rational boxes; graph-hull membership; fixed number of aspect-ratio types algorithm; positive rank-one MOT/logarithmic-precision consequence under explicit bit model; factorwise gap is one here. |
| notes/multilinear-treewidth-two-investigation.md | Distinct auxiliary lemmas: canonical forest pair law via residual2Q-P attains half the optimal union deficiency, general nonnegative payoff half guarantee and triangle residual obstruction; identical factor-neighborhood variable compression preserves both lower values and adds the same nonnegative amount to both widths. Include full short proofs in an appendix. The stronger two-chordal-bipartite-class finite search is not an analytic theorem. |
| notes/multilinear-incidence-width-investigation.md | Forest-cover coloring barrier at incidence K_(2,m), with private coordinates for distinct supports; general local-payoff sharpness of feedback domination. Other promoted results are covered by canonical rows. |
| notes/multilinear-treewidth-three-investigation.md | K_(3,m) obstruction to extending the all-cycle coloring invariant, although all-ones incidence is TU; width-three balanced/TU searches are finite evidence only; planar idea remains open. |
| notes/generalized-monomial-gap-obstruction.md | A one-variable, two-term positive rational-power family has unbounded relative width on a fixed interval; logarithmic reparameterization makes that particular comparison exact. Include the short proof as a boundary of multilinearity. |

### Stage 4

| Source | Coverage |
| --- | --- |
| results/spatial-bb-exponential-lower-bound.md | Concave quadratic optimum 1/4; arbitrary real coordinate splits; box-cover witness argument; separable underestimators; matching exponential upper and polynomial fixed-demand-level certificate; charged objective-based tightening and feasibility tolerance (state the small-tolerance range explicitly); second-order chord error and exact scope of chord/McCormick/alphaBB claim. Reconcile stale claims that SDP behavior is open with later results. |
| results/spatial-bb-sdp-rlt-exponential-lower-bound.md | Full augmented PSD, all pairwise box RLT and equality products; explicit feasible constructed moments; same cover lower with degree-one strengthening. |
| results/spatial-bb-higher-sos-exponential-lower-bound.md | Fractional-cardinality pseudomoment positivity, equality identities, arbitrary repeated slack products, degree/order tradeoff; unique optimizer perturbation and increasing concave allocation corollary. |
| results/spatial-bb-product-domain-exponential-lower-bound.md | Arbitrary nonempty disconnected coordinate sets; all univariate valid polynomials/equalities through degree; scalar nonlinear auxiliary branching and explicit degree pullback. |
| process/univariate-lift-refinement.md (paper-local completion, accepted Stage 4) | Endpoint-interpolation transfer eliminates the rD degree loss for coordinatewise graph auxiliaries, retaining originals and the specified local polynomial oracle. Includes everywhere-finite nonpolynomial functions, explicit lifted objective degree/full-graph agreement, global relative transfer and coupled-cut exclusions. Independently checked by the author, coordinator and all 15 Stage 4 reviewers; see the acceptance record. |
| results/spatial-bb-relative-gap-exponential-lower-bound.md | Fixed-size direct-product blocks; global coupled SOS tensor positivity; fixed relative tolerance and increasing strictly concave distinct costs; unique optimizer/no permutation symmetry; decomposition escape. |
| notes/spatial-bb-known-clique-cut.md | Explicit globally valid quadratic cut closes the fractional-cardinality root; essential motivation for a different cubic family. |

### Stage 5

| Source | Coverage |
| --- | --- |
| results/spatial-bb-quadratic-cut-exponential-lower-bound.md | General 2^(m T_*/Delta) cover transfer from degree-4r pseudoexpectations; exact degree-two realization from signed moments; random 3XOR occurrence deletion; OPT>=1/8 and 2^(7n/1024) at absolute 1/16 or relative 1/2; coordinate sets; sensitivity bounds; finite order-two Bernstein certificate. |
| results/spatial-bb-monomial-lift-exponential-lower-bound.md | Signed monomial supports <=D, arbitrarily many coordinates including originals; degree 4rD hypothesis; all graph identities through available degree; exact quadratic moment hull of lifted box; parity-rank cover count 2^(m T_*/(Delta D)); pair/clause factorable QCQP; N<=17n; coordinate sets; 48^n upper; D versus polynomial region count, with original/lifted dimension distinction. |
| process/order-one-monomial-refinement.md (paper-local completion, accepted Stage 5) | The author, coordinator and all15independent reviewers verified the extension of bounded monomial lifts to r>=1,rD>=2 and the order-one quadratic-formulation upper certificate using only full-box quadratic moment realization; the unlifted cubic still needs r>=2 and the distinct Bernstein proof remains. |
| notes/spatial-bb-affine-branching-barrier.md | Balanced halfspace defeats preserved root moments; linear order requires linearly many substitutions but keeps half the witnesses; method obstruction only, not an affine-tree upper bound. |

### Stage 6 supporting discussion

| Sources | Scope |
| --- | --- |
| results/point-packing-relaxations-anstreicher-conjecture-4.md | Include the compact self-contained derivation of the four RLT/SDP point-packing values, with updated symmetry secants, explicit attaining moment matrices, RLT redundancy and dimension-scaled averaging. These are established Khajavirad 2024 results, not new conjecture resolutions. Numerical n<5 symmetry values are exploratory and need not become exact claims. |
| results/mip-relaxation-binary-lower-bounds.md; results/bilinear-graph-binary-complexity.md | Briefly distinguish the adjacent integer-precision resource: binary assignment covers and parity classes control approximation accuracy, whereas spatial results count oracle-certified regions. These belong primarily to topic1 and are not full additional theorem chapters here. |
| results/rank-one-correlation-face-conic-lower-bounds.md; results/rank-one-correlation-face-stability.md; results/rank-one-approximate-sdp-lower-bound.md | Separate resource: exact and fine approximate global lift size. Correlation face and entrywise-l1 accuracy O(m^-2); arbitrary real/nonuniform lifts; no direct inference about tree size from lift size. |
| results/fbbt-monotone-system-hardness.md; results/fbbt-doubly-exponential-convergence.md | Separate resource: PosSLP-hard limiting-bound approximation and 2^(2^n-1) primitive-update count. PosSLP is not known NP-hard; primitive contractor and fair-update scope; no claim about accelerated global contractors. |
| results/scaling-disjunctions-hull.md; notes/audit-scaling.md; notes/review-scaling-characterization.md | Representation changes can remove artificial gaps: two-endpoint scaling hull, common intensive-variable caveat; original cost-factorization theorem was false and corrected. Explain only relevant implication with clear attribution to classical disjunctive machinery. |
| notes/common-factor-p-split-rotation-gap.md; notes/common-factor-p-split-correction.md; notes/common-factor-p-split-balls.md | Coordinate dependence and an auxiliary-image scope boundary; distinguish convexifying the auxiliary image from the complete feasible graph. Include the retained-box counterexample to the published universal nonexactness statement, local directional repair, exact two-ball basic projection and Hausdorff loss, rational coordinate comparison and final exact-image strengthening. These short distinct derivations may be in a supporting appendix. |

## Proof dependencies requiring fresh verification

1. Vertex-law envelope facts, positive common upper attainment, and definition of factorization-dependent T are shared by every gap result. All subsequent couplings must preserve the full original mean vector simultaneously.
2. Dyadic exact hull and variable-radix exact hull are different parameter regimes. Do not substitute the simpler 1+(L-1)/b formula at b=2 when its assumptions fail.
3. Harmonic bounds require valid probabilities, exact normalization, correct inactive-mass estimate, uniform asymptotic choices and rational dimension/degree interpolation. The finite Lambert-W bound does not establish second-order sharpness.
4. Graph results need separate audits of half-integrality with parallel/dummy edges, retained coverage baseline, local-law gluing, and the full series/parallel boundary invariant. For treewidth two, inspect original Camion and series-parallel source statements; do not cite balancedness as if it implied TU.
5. Positive-box coefficient proof uses a finite minimum/maximum spreading step. Generic Schur-concavity is false. The balanced-orientation refinement fixes an ambient law under restriction. Unequal physical aspect ratios invalidate some exact structural/cardinality formulas.
6. Coefficient removal must control sampled polynomial uniformly over all clone vertices and then transfer both envelopes; concentration for a single point is insufficient.
7. Fractional-cardinality SOS proof needs homogeneous reduction and Gram positivity with every degree restriction checked. Product-domain proofs use endpoint membership without compactness assumptions. Relative-gap tensor positivity must cover globally coupled square polynomials, not just blockwise ones.
8. Strongest spatial source dependency is Schoenebeck Theorem 12/Lemma 13: verify density assumptions, probability quantifiers, signed-character moments through the full needed degree, and positivity conventions directly in the full primary proof. The local literature index currently did not list a Schoenebeck package; retrieve the author manuscript if necessary. The elementary occurrence-deletion proof and signed-moment realization must also be rechecked.
9. Lifted spatial positivity consumes original degree 4rD, not 2rD. Exact quadratic realization need not respect the graph, but the pseudoexpectation must respect every imposed graph identity under polynomial pullback. The parity-rank witness count is essential when supports overlap or repeat.
10. Single-product NP membership needs bounded rational vertex-distribution certificates; exact envelope hardness and high-precision MOT hardness do not imply hardness at fixed additive error.

## Genuine open boundaries and bounded development opportunities

- Exact R(3), exact finite rho_B constants, and matching second-order asymptotics remain open. Reconcile the strongest certified cubic lower 1610000/743033 throughout.
- Exact W(k) for k>=3, k-class balanced/TU row partitions, and planar sharp constants remain open. The finite searches are not proofs. D(k),P(k)>=k+1 already disprove a naive exact-k conjecture for those other width measures.
- Frequency-two gap on arbitrary unequal-aspect positive boxes remains open; bipartite equality is already false. Common-ratio/cardinality theorems give a complete restricted result.
- Arbitrary affine spatial branching, high-degree auxiliary branches beyond degree accounting, localizers of all coupled quadratic cuts, and hulls of the feasible graph remain outside the lower bounds.
- Bounded additions worth attempting while writing: derive and verify the coefficient-regularity cardinality corollary explicitly; consolidate finite-dimensional balanced orientation; supply self-contained finite cubic rational certificates and independent moment/degree checks; remove stale open/constant statements. These develop existing ideas without pretending that publication readiness requires solving every open problem.

## Verification artifacts

Use `/home/sgusev/miniconda3/envs/minlp-notes/bin/python` where dependencies require networkx or gurobipy; root reports that environment has numpy/scipy/sympy/networkx/gurobipy. Verify license-dependent code separately. Exact checks are supporting evidence, never replacements for general proofs.

- Bilinear: code/mccormick_degeneracy/audit_cut_identity.py, check_cut_inequality.py, kn_pm1_ratio.py.
- Universal/cubic: code/multilinear_ratio/dyadic_exact.py, multiscale_counterexample.py, universal_coupling.py, cubic_integer_certificate.py, verify_cubic_bounds.py, verify_cubic_analytic_family.py, verify_cubic_two_level.py, verify_cubic_rounding_upper.py; code/verify_multilinear_second_order.py.
- Structural: code/verify_multilinear_variable_radix.py, audit-multilinear-feedback-law.py, multilinear_frequency_two_verify.py, audit-frequency-two-cycle-rounding.py, multilinear_convex_cardinality_verify.py, audit_convex_cardinality_matching.py, search_series_parallel_factor_colors.py; width-three and TU searches remain exploratory.
- Box/interiority: code/audit-marginal-floor-coupling.py, audit-positive-box-coefficients.py, audit-positive-box-67.py, multilinear_frequency_two_positive_box_search.py, audit_single_monomial_hardness.py. Search/optimization logs identify candidate constants but are not proof certificates.
- Spatial: code/spatial_bb_lower_bound/check_lower_bound.py, check_sdp_rlt_strengthening.py, check_higher_sos.py, check_relative_gap.py. Stronger XOR/lift notes mainly contain analytic source-derived checks; write narrow independent symbolic checks where they add confidence, rather than resampling generic instances.
- Supporting: code/fbbt-hardness-check.py, code/rank_one_hardness/audit_face_stability.py, code/scaling_disjunctions/bilinear_multiplicity_hull.py.

## Literature inventory and handling

Read literature/AGENTS.md before using the knowledge base (done for this inventory). Do not hand-edit its generated index.md or references.bib. User-supplied originals may be read but not redistributed. Verify source claims from fulltext and important equations from originals, then cite exact primary metadata in a paper-local bibliography. Do not promote unread packages to read based on metadata.

Local packages include Luedtke–Namazifar–Linderoth (positive conjecture, classical bilinear bounds), Boland et al. (cut-range criterion and signed gap), Sherali (symmetric envelopes), Adams–Gupte–Xu (positive common-ratio product envelopes), Davidson–Donsig (Schur multiplier density), Del Pia/Khajavirad multilinear polytope papers, Duffin (series-parallel networks), Grigoriev/Laurent/ Kunisky–Moore (fractional-cardinality moments), Jarre (SDP branch-and-bound predecessor), and general branch-and-bound/cutting-plane comparisons.

Important primary sources presently linked directly from notes and requiring direct inspection/package discovery: Schoenebeck full version; Cornuejols packing/covering manuscript (Camion Thm 6.5, balanced mixed integrality Thm 6.13); Hassin–Tamir and Eppstein series-parallel recognition; Barrus fractional realizations; Edmonds matching/convex costs; Coniglio ICLR 2026 spatial midpoint result. Spatial novelty files correctly acknowledge predecessors; do not repeat the README's older suggestion that no related spatial lower bound exists.

Useful audit records: notes/positive-multilinear-novelty.md, positive-multilinear-degree-novelty.md, multilinear-structural-novelty.md, multilinear-treewidth-two-novelty.md, multilinear-marginal-floor-novelty.md, positive-multilinear-aspect-ratio-novelty.md, spatial-bb-strengthening-novelty.md, review-rank-one-mot-precision.md, rank-one-mot-precision-later-literature.md, research-open-thread-audit.md, research-closeout.md, research-continuation-closeout.md. Review-note families linked in each canonical result should be checked for past corrections; they are not journal references.
