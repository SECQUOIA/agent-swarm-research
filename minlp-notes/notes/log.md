# Research log

Working log for the MINLP-theory-for-PSE research effort. Newest entries at the bottom.
Results that survive verification are written to `results/`. Negative results, dead ends,
and novelty-check outcomes are kept here so that they are not repeated.

## 2026-09-04 — session start

- Repository state: only `literature/` (177 paper packages, no synthesized results).
- Compute: conda env `minlp-notes` (Python 3.12, gurobipy 13.0.3 academic WLS license,
  scipy, sympy, cvxpy, pyomo, networkx). BARON via GAMS at `~/.local/opt/gams/...`.
- Launched agents: open-problem miner over the literature base; two brainstormers
  (convexification; algorithms/duality/complexity/MIOCP); novelty check on the
  "integer-multiplicity / scaling disjunction" idea (below).

### Candidate direction A: scaling disjunctions (integer multiplicity, discrete sizes)

Observation: if a unit model is scale-invariant in its extensive variables
(X = lambda * xi for a per-unit point xi, intensive variables T shared and not scaled),
then for any discrete or continuous set of admissible scales Lambda the set
F = {(lambda, lambda*xi, T) : lambda in Lambda, (xi,T) in S} is a union of affine
images of Lambda, so conv(F) = conv(F_{lambda_min} ∪ F_{lambda_max}). Consequences:
integrality of a multiplicity variable n costs nothing in the hull; discrete standard
sizes vs. continuous sizes have the same hull; identical parallel units aggregate to
n * conv(S) (Minkowski sum), Shapley–Folkman bounds the residual gap; a nonhomogeneous
count-only cost f(n) separates as its convex envelope over Lambda; explicit
2-disjunct (Balas) extended formulation, linear if conv(S) is polyhedral.
Relation to known results: affine dependence on one variable => hull determined by two
facets is the mechanism behind envelopes of (n-1)-convex functions
(Jach–Michaels–Weismantel 2008) and McCormick; the disjunctive/discrete-scale form,
the aggregation statement, and the PSE consequences appear to be new — novelty check pending.

## 2026-09-04 — session summary (stopped at user's request: usage limit)

### Results obtained (see `results/`)

1. `rank-one-row-column-hardness.md` — **strong NP-hardness** of linear optimization over
   rank-one matrices with row and column sum bounds (U^row ∩ U^col), resolving the conjecture of
   Dey–Kocuk–Santana (JOGO 2020). Reduction from maximum edge biclique via the parametrization
   W = r cᵀ/S, fixed row/column for constants, dummy rows/columns to decouple Σr = Σc. Also:
   PARTITION variant, corollary "no efficiently constructible compact hull unless P = NP",
   polynomial algorithm for fixed n1 (or n2). Refereed (fixes applied), numerically checked
   (`code/rank_one_hardness/`, ALL OK), novelty-checked (no prior resolution found).
2. `mccormick-gap-degeneracy-bound.md` — McCormick vs hull gap ratio for bilinear functions is at
   most 4√d(G) (degeneracy) and 2√2·√Δ(G), replacing Boland et al.'s 600√n; tight up to constants.
   Proof: signed cut range = max_S ‖A_{S,T}‖_{∞→1}, Khintchine (Szarek), greedy colouring along a
   degeneracy ordering. Refereed (constant improved 4√2 → 4 per referee), novelty-checked.
3. `point-packing-relaxations-anstreicher-conjecture-4.md` — proofs of all four parts of
   Anstreicher's (JOGO 2009) Conjecture 4 (RLT = 2; SDP = 1 + 1/(n−1); RLT+SYM = 1/2; SDP+SYM =
   (1/4)(1 + 1/⌊(n−1)/4⌋)) by single-pair RLT bounds and an averaging (Welch-type) argument for
   SDP, with explicit attaining points. Numerically matched for n ≤ 14. **Not yet refereed or
   novelty-checked.**
4. `scaling-disjunctions-hull.md` — convex hulls of integer-multiplicity / discrete-size structures
   with shared intensive variables: hull = hull of the two extreme scales; explicit linear/conic
   extended formulation; polyhedral hull of the n·T bilinear structure; count-only cost separation;
   several types over an integral count polytope. The convex extensive-only core is known (Wu et al.
   arXiv:2602.04123, Feb 2026); the intensive-variable/discrete-size/cost-separation parts appear
   new but are elementary. **Not refereed; Theorem 4's proof sketch needs tightening.**

### Interrupted / pending

- Agent "Test Sager–Zeile CIA conjecture" (open problem #6): wrote `code/cia_tv_conjecture/cia_tv.py`
  (row-generation exact solver for θ^max with TV budget), no results table produced yet.
- Agent "Explore Luedtke multilinear conjecture" (open problem #13): code in
  `code/multilinear_ratio/` (exact envelope LP, families, multistart search); partial log
  `run_experiments.log` (79/136 families): largest ratio found 1.8 (K9, bilinear positive, which
  equals the known 2 − 2/χ value); no counterexample to the bounded-ratio conjecture so far; 3-uniform
  families gave ≤ 1.67. No README yet.
- Referee/novelty pass still needed for results 3 and 4.
- Next candidates (from `notes/candidate-directions.md`): Anstreicher Conjecture 5 (ORD),
  common-factor products with product bounds, multi-attribute mixer hull, stagewise Shapley–Folkman
  bound for nested Benders, FBBT fixed-point complexity.

### Environment

conda env `minlp-notes` (`~/miniconda3/envs/minlp-notes/bin/python`): gurobipy 13 (academic WLS),
scipy, sympy, cvxpy+Clarabel, pyomo, networkx.

## 2026-09-04 — resumed research and independent audits

The user requested sustained investigation, up to 15 subagents, stronger results,
and correction of any existing errors. Research and independent review proceed
in separate agent assignments. No external publication or journal refereeing has
occurred; prior uses of “refereed” in result status lines have been corrected.

### Corrections to the previous session

- Point-packing Conjectures 4 and 5 were resolved by Khajavirad (2024),
  https://arxiv.org/abs/2404.03091 . The local note is a rediscovery. Its main
  formulas are correct, with several explanatory mistakes corrected. See
  `notes/audit-packing.md`.
- The original scaling cost-separation theorem is false when intensive and
  extensive coordinates are coupled. A compact example has true minimum cost
  1 versus claimed 0. Replaced it with a correct lifted extensive-only theorem
  and an independently reviewed characterization: with scales 0<s<M,
  universal scale-cost separation holds exactly when the per-unit convex hull
  is a Cartesian product. See `notes/audit-scaling.md` and
  `notes/review-scaling-characterization.md`.
- Rank-one hardness proof survives review. Corrected solver/bit-model and
  process-cost qualifications; strengthened its algorithm to FPT and its
  decision classification to NP-completeness with rational certificates.
- Bilinear gap proof survives review. Improved the row-norm constant, then
  strengthened degeneracy to maximum induced edge density via fractional
  orientations. See `notes/audit-mccormick.md` and
  `notes/review-mccormick-density.md`.

### Stronger results recorded so far

- A correlation-polytope face of the zero-lower/unit-upper rank-one hull gives
  unconditional exact SOCP/SDP lift lower bounds. Independent mathematical
  and source checks passed. A quantitative stability extension is under review.
- Root's saturated-margin repair lemma gives entrywise distance at most
  2(2-r0-c0), hence an exact linear penalty removing the old reduction's two
  positive lower bounds. Strong NP-hardness therefore persists with all lower
  bounds zero and upper bounds one. Independently reviewed; 2,000 exact
  rational checks passed across total-flow regimes below, at, and above one.
- Restricted FBBT limiting bounds encode monotone arithmetic circuits,
  yielding PosSLP-hard constant-accuracy approximation. A separate family
  forces doubly exponential primitive propagation counts. Proofs independently
  checked; a dedicated novelty audit is ongoing.
- A multiscale positive-multilinear construction may disprove the universal
  gap conjecture. Root simplified the original all-subsets construction to
  disjoint blocks at each scale, requiring only linearly many unit-coefficient
  monomials. Two independent proof reviews and a novelty audit are ongoing.
- Common-factor products with a fixed number of linking constraints, and a
  CIA total-variation conjecture counterexample, are being developed and reviewed.

These entries record progress, not blanket novelty certification. Detailed
assumptions, review outcomes, and sources reside in the linked result/audit files.

### Further verified developments and novelty corrections

- **Positive multilinear conjecture:** two independent reviewers confirmed a
  sparse, unit-coefficient construction with n=2^L+L variables, 2^(L+1)-2
  monomials, and exact hull gap H_L=s+(L-s)/2^s, where
  (L-s+1)/2^(s+1)<=1<=(L-s+2)/2^s. The termwise gap is L, so the exact ratio
  is asymptotic to ln(n)/ln(ln(n)). The nested dyadic construction uses
  bit-reversal leaf sets and random XOR shifts to attain the upper certificate.
  See `results/positive-multilinear-gap.md` and two independent review notes.
  Literature checks include coverage functions and directed-hypergraph cuts,
  not only MINLP terminology; no prior matching resolution found so far.
- **CIA:** an exact counterexample refutes the published total-variation
  conjecture. The full continuous one-switch minimax value is
  T max{1/3,(n-1)^2/[n(2n-1)]}, n>=3, proved constructively and independently
  reviewed. Uniform controls with several switches also admit exact continuous
  and discrete formulas. A dedicated search screened 29 citing records and
  found no prior matching correction, with full-text limitations recorded.
- **Approximate rank-one hulls:** quantitative stability transfers fine outer
  approximation to correlation hulls. Independent review improved the transfer
  factor to A_m=m(184m+6). At error <=1/A_m, LP size is exponential; a direct
  signed-correlation projection and shifted LRS slack prove stretched-exponential
  SDP order already at error <=1/(2A_m). All use uniform entrywise-l1 outer
  distance and unit upper/zero lower margins. Separate primary-source and
  conic-duality audits passed; equivalent-object novelty screening is ongoing.
- **Graph-density novelty downgrade:** Davidson–Donsig's Schur-multiplier
  characterization plus Grothendieck and polarization already imply the
  square-root hereditary-density order. The local proof improves the transferred
  constant and gives an elementary explicit McCormick statement, but the order
  and qualitative graph-family characterization must not be presented as new.
  The old-theorem transfer itself was independently reviewed.
- **Common-factor hull:** the full reciprocal-anchor star has an explicit
  call-function envelope hull, exact rational separation, and at most 2n+3-point
  constructive decomposition. Root independently reviewed the finished proof;
  all mathematical checks passed. Convex-order joins and lift-zonoid thresholds
  are classical and credited. Polynomial weak optimization is already elementary;
  the potentially distinct contribution is the explicit exact rational oracle
  and decomposition. The fixed-linking-row algorithm also credits earlier
  parametric bounded-LP basis enumeration.

No result has been externally peer-reviewed or submitted. “No prior result
found” records a bounded search, not proof of priority. Research continues.

### Sharp multilinear characterization and additional completed results

The positive-multilinear direction now gives a sharp leading-order answer,
not just a counterexample. A harmonic conditional-failure distribution,
combined with threshold and independent couplings using optimized weights,
proves that the worst ratio R(d) for maximum monomial degree d satisfies

```
R(d) ~ ln d / ln ln d.
```

The worst ratio C(n) by number of variables likewise satisfies
`C(n) ~ ln n / ln ln n`. Both leading constants are one. The bounds cover
original, unexpanded term-by-term relaxations on every finite nonnegative
box. A single coupling works simultaneously for every monomial up to the
degree bound, without using objective coefficients. The sparse dyadic
family supplies the matching lower bound. Two independent reviewers and root
read the full upper proof and found no unresolved mathematical issue; see
`results/positive-multilinear-sharp-degree-growth.md` and its three review links.
The canonical overview and lower proof are in `results/positive-multilinear-gap.md`.
A dedicated primary-literature audit is extending beyond MINLP terminology to
simultaneous Fréchet bounds, directed cuts, and dependence coupling.

Other completed work:

- CIA now has an exact three-mode finite-grid formula for all N>=2 and an
  especially small published-conjecture witness n=7,N=3: 11/7>3/2.
  Independent proof and exact enumeration checks passed.
- The integer reciprocal-anchor hull has exact compressed rational membership,
  separation, and decomposition independent of the number of integer scalar
  values. Binary leaves do not change the convex hull. Independently reviewed;
  a test with 10^12 possible scalar values used only a few envelope pieces.
- Fixed interaction-rank costs admit exact rank-one margin optimization in
  polynomial time for fixed rank. This yields a fixed-quality-count per-pool
  Lagrangian subproblem oracle. Independent review and 160 exact comparisons
  passed; the result credits earlier zonotope and low-rank optimization methods.
- Corrected the legacy point-packing verifier: published ceiling symmetry,
  actual conjecture formulas on their valid ranges, solver-status validation,
  and removal of the misleading incomplete ordering option. Relevant checks
  passed for n=2..14 and formula/boundary checks through n=30.

Next investigations include cubic positive gap constants, sharper finite-degree
couplings, and finite-n multiple-switch CIA behavior. Established results remain
saved separately from these new conjectures. Research continues.

### Structural multilinear bounds and further exact certificates

- The cubic worst ratio now has independently reviewed bounds
  `7443345/3445256 <= R(3) <= 8/3`. The lower certificate checks all 274625
  count states exactly. The upper bound uses one coefficient-independent
  random-orientation coupling. Homogenization and random thinning preserve
  fixed-degree suprema with unit coefficients when dimension may increase;
  these reductions have their own independent audit.
- An optimized harmonic cutoff gives a reviewed finite-degree bound with
  denominator `ln ln d - ln ln ln d + o(1)`. No matching second-order lower
  bound is claimed. The leading asymptotic constant remains one.
- A reviewed structural theorem gives a sharp gap ratio `3/2` when each
  variable appears in at most two nonlinear monomials. More precisely the
  bound is `g/(g-1)` for dual odd girth g, and bipartite dual graphs give
  equality of scalar gaps. The proof retains the coverage baseline through
  a degree-slab decomposition and odd-cycle rounding. Its box scope is the
  unit cube or zero lower bounds; positive lower bounds need a separate proof.
  See `results/positive-multilinear-frequency-two-gap.md`.
- Deleting f variable nodes to leave an incidence forest yields gap ratio
  at most `2^f` on every nonnegative box. The constant is sharp for f=1;
  higher-f sharpness for positive monomials is not established. See
  `results/positive-multilinear-feedback-gap.md` and its independent audit.
- The global two-switch CIA bound is independently reviewed, including 600
  exact-rational constructed schedules. It proves exact values T/4 for
  four through six modes and first finite-mode correction `-2T/(3n)`.
  The stronger equal-total formula and a computer-assisted four-mode prefix
  lemma also passed independent checks. A general exact formula is being
  developed and is not yet treated as verified.
- A reviewed one-variable generalized-power example shows that positivity
  and bounded exponents alone cannot extend the multilinear gap theory.
  The ratio diverges like `0.615935748.../epsilon`; logarithmic coordinates
  remove the cancellation in this particular example. This is a useful scope
  obstruction, with no novelty claim.

The strongest newly proposed extensions are a general exact two-switch CIA
formula and an analytic cubic lower family. They remain candidates pending
independent review. All mathematical status and literature qualifications are
kept in their individual files. Research continues.

### Exact two-switch formula and positive-box structural obstruction

The stronger continuous CIA two-switch theorem now passed two independent
agent audits and a full root proof review:

```
F_(n,2)(T) = T max{1/4, (n-1)^3/[n(3n^2-3n+1)]}, n>=4.
```

This settles the seven-mode boundary and proves uniform controls are worst-case
for all n>=8, for arbitrary measurable relaxed profiles. The analytic proof
uses aggregate reaches after excluding each possible final mode. It supersedes
the earlier computational four-mode reach argument and the weaker global
finite-n bound. All remain saved for their independent derivations and checks.
The dedicated novelty audit found no matching prior result, including searches
across scheduling and discrepancy terminology; inaccessible texts and other
search limitations remain documented.

The cubic analytic family has also passed independent exact audit. Its simple
bound is `R(3)>=483/223`; positive slack in the same Bernstein certificates
improves this to `1610000/743033`. These are supremum lower bounds from a
finite-family approximation, not an assertion that the family ratios converge
to either exact number. The upper bound remains `8/3`.

Root found and an independent reviewer verified a sharp scope obstruction for
bipartite frequency-two exactness on positive boxes: `xy+xyz` over
`[1,2]^2 x [1,3]` at `(5/4,5/4,5/2)` has exact ratio `7/6`. Six affine
vertex certificates and four rational distributions prove every envelope
value. This refutes the bipartite exactness extension, but leaves a possible
universal 3/2 bound on such boxes open. See
`notes/multilinear-frequency-two-positive-box-obstruction.md`.

Further investigations are active in bounded incidence density, higher switch
budgets, pooling triviality, and network-polytope bilinear hulls. Candidate
claims remain separate from reviewed results.

### Sharp incidence and marginal-floor characterizations

The structural multilinear work now determines three further sharp growth laws.
Worst ratios by incidence treewidth, incidence degeneracy, and minimum maximum
incidence-orientation outdegree are all asymptotic to k, with leading constant
one. The upper bound uses disjoint ownership rounds and the degree theorem.
A variable-radix lower family has exact ratio L/[1+(L-1)/b] and exact incidence
treewidth L. Letting b grow gives the matching leading constant. Independent
review checked both gap certificates and graph structure. Exact fixed-k values
remain open. A separate degeneracy-two example has ratio 15/7>2, disproving an
earlier tentative degeneracy bound while leaving the treewidth-two question open.
See `results/positive-multilinear-incidence-sharp-growth.md`.

Root developed a second sharp parameter theorem: when every unit-box mean is at
least δ, the worst ratio is asymptotic to ln(1/δ)/ln ln(1/δ), independently of
degree and dimension. A normalized density, clipping, and exact marginal
completion produce one simultaneous coupling. Two independent full reviews
passed, including the two-sided interior strip and normalized nonnegative-box
extension. Fixed-δ finiteness was already elementary; only the sharp growth and
constant are proposed contributions. See
`results/positive-multilinear-marginal-floor-gap.md` and its novelty screen.

A joint theorem combining dimension, degree, width, and interiority is now
written and under independent audit. It needs a single lower family satisfying
all restrictions; taking a minimum of separate sharp upper bounds would not
suffice. No pending synthesis claim is treated as reviewed yet.

Additional completed developments:

- The cubic upper bound improved to 31/12 and passed independent exact review.
  A separate simple two-level family has exact limiting ratio 243/115. Its
  32-variable member has exact ratio 135/67, and padding yields a fully explicit
  52-variable homogeneous cubic with all coefficients one, strict interior
  means, and ratio at least 2700/1343>2. All have independent audits. The strongest
  overall cubic lower remains the earlier analytic family's improvement of
  483/223; these simpler witnesses serve a different purpose.
- Pooling triviality is polynomial for the source's upper-capacity acyclic
  generalized model. The shortest-path blending test, at-most-K+1-path profitable
  witness, and polyhedral conic hull passed independent review. The destination
  disaggregation was found in Boland–Kalinowski–Rigterink (2016); the result is
  explicitly presented as consequences of established machinery, not a new
  decomposition. The capacitated convex hull remains different.
- Sparse network–simplex hulls inherit transportation universality already with
  two simplex coordinates on four-layer DAGs. Unit capacities and unit flow
  still allow product-coordinate facet coefficients beyond every polynomial
  bound in model size. Both independent audits passed. This is a qualified
  transfer of known universality, not a hard-separation or multiplier lower bound.
- On positive boxes, a bipartite frequency-two family with unit coefficients
  has ratio approaching 3/2. Bipartite conflict graphs have upper bound two
  by gluing local laws within a color class. The gap between these bounds and
  general nonbipartite frequency-two positive-box behavior remain unresolved.

The joint multilinear theorem has now passed independent review. With
`q=min{n,d,1/δ}` on the branch q>=exp(e), and
`min{k,ln q/ln ln q}` tending to infinity, the worst ratio is asymptotic to
that minimum, with leading constant one. A variable-radix family simultaneously
satisfies dimension, degree, treewidth, unit-coefficient, and two-sided marginal
restrictions. Review corrected a limiting-quantifier ambiguity by explicitly
excluding the logarithmic expression's pole near q=e. See
`results/positive-multilinear-joint-gap-growth.md`.

The exact equal-marginal companion is also reviewed: complete homogeneous
polynomials attain the finite-dimensional worst ratio, and uniform marginal
means always give ratio at most two. This is explicitly credited as a consequence
of Sherali's classical envelope theorem. Thus two distinct marginal levels are
necessary and sufficient for examples with ratio above two; the new two-level
cubic construction provides sufficiency.

### Three-switch completion and further scope results

The exact continuous three-switch CIA formula is now independently reviewed:
`F_(n,3)=T max{1/5,1/[n((n/(n-1))^4-1)]}`, n>=5. The plateau is n=5..11;
uniform relaxed controls are worst-case for n>=12. The general four-block reach
proof is computer-assisted, with 179 finite and ten polynomial certificates;
the symmetry reduction, semantic inequalities, independent matrix generation,
and every certificate passed review. The heavy-mode argument and final transfer
are analytic and separately reviewed. The arbitrary-block one-sided bound also
passed review, including its equal-total two-sided consequence and sharp first
many-mode correction. General all-budget two-sided exactness remains open here.

Other useful work retained:

- Arbitrary discrete-convex cardinality factors with variable frequency two
  satisfy the sharp odd-girth gap theorem. This restores bipartite exactness
  for original positive products on common-aspect-ratio boxes. The polynomial
  scalar-envelope oracle is explicitly a classical matching consequence.
- A generic nonnegative local-payoff bound of two at incidence treewidth two
  is false: six fair bits and three parity factors give ratio three, including
  literal local/full envelope widths. The factors have signed multilinear
  coefficients; the positive-monomial treewidth-two question stays open.
- Cyclic pooling sign and conic-hull consequences were independently verified.
  A closed circulation makes the claimed universal invertibility in the checked
  2015 BKR manuscript false; the main flow-projection equivalence is repairable.
  No statement about the uninspected final-version proof is made.
- The QCQP multiplicity thresholds were already strengthened in a later 2024
  paper to hull exactness at k>=m, with existing sharpness examples. The local
  open-problem row was corrected. No new theorem is claimed.

The fixed strictly positive box question now has a reviewed uniform upper bound:
with R=max{4,max_i upper_i/lower_i}, the gap ratio is at most 4R+6+2/R,
independent of degree and dimension. Root then found a variable-radix lower
family whose actual ratio tends to ρ on a fixed aspect-ratio-ρ box. That lower
proof is undergoing its final independent audit; it would establish sharp
linear order in the box aspect ratio. Its full derivation is already saved.

### Sharp aspect-ratio theorem

The positive-box result strengthened from linear order to an exact leading
constant. For ρ>=64 the reviewed upper bound is

```
C_box(ρ) <= 2 + (ρ+1)/(1-3/sqrt(ρ)) = ρ+3sqrt(ρ)+O(1).
```

Root's fixed-aspect variable-radix family has actual ratio tending to ρ as its
dimension grows. Its exact termwise gap and two-sided hull estimates passed a
separate full audit. Together these prove `C_box(ρ)~ρ`, with leading constant
one. The upper proof handles arbitrary strictly positive coordinate intervals
whose maximum endpoint ratio is at most ρ, and passed two fresh independent
reviews. See `results/positive-multilinear-positive-box-sharp.md` and
`results/positive-multilinear-positive-box-lower.md`. Exact fixed-ρ constants
remain open. Dedicated primary-literature screening is ongoing.

A reviewed companion establishes NP-completeness of exact midpoint-envelope
threshold evaluation for a single unit-coefficient monomial on unequal rational
boxes contained in any fixed `[1,1+η]^n`, η>0. The proof is PARTITION-based with
a vanishing additive gap; it makes no strong-hardness or fixed-accuracy claim.
Thus uniform quality guarantees and exact evaluation complexity are separate.

The positive treewidth-two question now has a proposed series-parallel coloring
proof undergoing two independent audits. The previous generic nonnegative-factor
route was disproved and remains documented. Further work continues on general
switch budgets, exact positive-box constants, and disjunctive formulation scope.

### Final closure at the user's request — 2026-09-04

The user requested completion of current proofs, verifications, and documentation,
then a stop. No further research directions were opened. This entry supersedes
intermediate pending-review labels above; the final state is indexed in
`notes/research-closeout.md` and assessed in `notes/research-status.md`.

The final positive-box theorem is `max{2,rho}<=C_box(rho)<=rho+2`, with two
completed fresh proof reviews and a separate lower audit. Its finite-dimensional
balanced-orientation refinement also passed a closing independent audit after
resolving induction under restrictions of one fixed ambient law. The earlier
coarse and asymmetric proofs remain as predecessors. Fixed-mixture optimality
is retained with its restricted scope; the exact worst polynomial ratio is open.

The exact incidence-treewidth-two constant is now two, including the stated
convex-cardinality/common-aspect positive-box extensions. Both complete proof
reviews and a focused novelty screen passed. The two auxiliary forest and
compression lemmas also received a final written independent audit. Width-three
experiments are closed, with their outcomes explicitly distinguished from proof.

The universal CIA heavy-mode theorem and exact full-to-one-sided minimax identity
passed final independent audit. Together with the reviewed arbitrary-block bound,
they give the all-profile general upper, sufficient exact plateau, and sharp
first many-mode correction for every fixed switch budget. The exact three-switch
law retains its explicitly computer-assisted four-block reach dependency. The
final CIA literature note covers these stronger scopes without claiming priority.

The single-monomial reduction's positive rank-one transport/AMIN precision
consequence passed a dedicated source and proof audit. A focused later-literature
check found no matching resolution of the published logarithmic-precision
question. The conclusion is in the rational bit model, with a small additive gap;
no stronger accuracy or unit-cost arithmetic hardness is asserted.

The P-split coordinate-effect note is fully audited, including its last two
strengthenings. The original rational two-ball witness survives every valid
convex auxiliary-only strengthening with the same coordinate epigraph links.
After a fixed rational orthogonal coordinate change of the complete model, the
tightest auxiliary-image convexification is exact, with an explicit conic repair.
Source-theorem corrections and the separate exact ball-relaxation formula remain
preserved with their own audits and scope limits.

Final housekeeping corrected stale current review/open-problem labels, repaired
relative links in a copied predecessor, checked document/artifact links and Python
syntax, and ran `git diff --check`. Useful unresolved ideas remain explicitly open
and are excluded from verified-result claims. All research assignments are closed;
the run is stopped. No external peer-review or definitive priority claim is made.

## Session 2026-09-04 (evening): new directions after closeout

The user reopened the research run and asked for new, more impactful results.
Two brainstorming agents and one literature agent were used to select targets
different from the closed programs.

- **Pooling degree bounds.** Open problems 2 and 3 of Boland, Kalinowski,
  Rigterink (JOGO 2017) are answered: the one-quality standard pooling problem
  is strongly NP-hard with all in-degrees at most two (outputs even in-degree
  one) and, separately, with all out-degrees at most two (inputs even
  out-degree one); pools have degree pattern `(2,2)`, which is the smallest
  hard pattern. Reduction from `{1,2}`-weighted capacitated orientation
  (Asahiro et al. 2011) via a bipartite subdivision lemma. Gurobi cross-check
  passed; one referee review passed with corrections (applied). See
  `results/pooling-one-quality-degree-two-hardness.md` and
  `notes/pooling-degree-two-novelty.md`. Remaining open: all four degree bounds
  at most two simultaneously; two pools.
- **Spatial branch-and-bound lower bound.** Drafted an unconditional
  `2^{Ω(n)}` leaf lower bound for any variable-branching spatial B&B with
  separable (chord/McCormick/αBB) relaxations on a separable concave QP with
  one knapsack equality, at fixed tolerance `ε < 1/4`, independent of the
  branching rule; matching `O(2^n)` upper bound. Sanity checks passed. Review
  and novelty search in progress. See
  `results/spatial-bb-exponential-lower-bound.md`.
- **Geoffrion Property (P) conjecture (1972).** An agent is developing a
  counterexample without compactness plus a positive sufficient condition.
- Candidate directions recorded from brainstorming for later: lower bounds on
  the number of binaries in ε-accurate MIP relaxations of `x^2` and `xy`
  (sawtooth optimality); exact big-M-equals-hull criterion for one indicator
  row over a box; Khajavirad's open three-plus-loop path hull; non-monotone
  separable on/off hull; dwell-time CIA constants; minimum-number-of-matches
  approximability; potential-based flow MPD on cactus graphs; hardness of
  deciding McCormick exactness.

Update (2026-09-05, usage limits approaching): the pooling result passed three
reviews; the spatial B&B bound passed one review with corrections (theorem
statement fixed to `min`, scope `k, n-k = Θ(n)`). Four agent investigations
(Geoffrion Property (P), MIP-relaxation binary lower bounds, all-degrees-two
pooling, MPD on cactus graphs) were still running; their outputs, if present,
are unreviewed drafts. See `notes/reopened-run-status.md`.

## 2026-09-05 — continuous research resumed

The user requested continued autonomous research until interruption or usage
limits, prioritizing impactful new results and independent verification.
The root agent reopened the four unfinished lanes and added a formulation
complexity lane. The following are completed milestones; research continues.

- **Pooling:** `results/pooling-all-degrees-two.md` proves strong NP-hardness
  with one quality, all four degrees exactly two, unit capacities, and bounded
  costs. Every feasible flow rounds in polynomial time to integral pure modes
  without losing profit, giving an exact independent-set reduction. Profit
  maximization has no PTAS. Two independent audits passed, including primary
  source checks. Verification includes 140 nonconvex instances, 89 exhaustive
  mode/matching instances, and 5,152 independent original-flow LP branches.
  Hardness survives fixed positive purity tolerance; the reviewed extension
  and a weighted integer-capacity structural lemma are retained in notes.
- **Bilinear interaction graphs:** `results/bilinear-graph-binary-complexity.md`
  proves that fractional vertex cover is the exact leading coefficient of
  integer dimension versus logarithmic accuracy. Arbitrary convex lifts and
  unrestricted integer ranges satisfy the lower bound by classical parity
  combined with a coordinate-width/volume argument. Shared binary expansion
  with residual McCormick bounds matches it; unequal product accuracies have
  finite LP bounds within an additive graph-dependent constant. Two audits
  passed, including rational preprocessing. Code checked 226 weighted LP
  allocations and 306 extrema of explicit projected formulation fibers.
  Prior shared discretizations, vertex covers, geometric triangle lower
  bounds, and the midpoint method are explicitly credited in a source audit.
- **Spatial B&B:** a second audit repaired infimum/attainment wording and
  objective-bound-tightening cover accounting in the earlier result. The new
  `results/spatial-bb-sdp-rlt-exponential-lower-bound.md` permits full SDP,
  RLT, and equality products. Independent proof review and 809 checks passed.
  Jarre's earlier binary B&B result is credited; the continuous arbitrary-box
  model here is distinct. Higher-order SOS and asymmetric-objective extensions
  remain under investigation and review.
- **Scalar formulation draft:** the preexisting square/product result passed
  independent review, with inaccurate rounded constants, multidimensional
  polyhedral upper-bound wording, and a hypograph statement repaired. The
  parity extension gives general integer-dimension bounds. A scalar quadratic
  Hessian-rank law is a new proof candidate under independent review.
- **Geoffrion:** a SOC-representable counterexample and positive sufficient
  conditions passed independent audit. They disprove the precise common-
  optimizer P-prime implication without compactness, but do not refute the
  informal computational Property P conjecture. The distinction is explicit
  in `results/geoffrion-property-p-conjecture.md` and the open-problem index.
- **Cactus potential flows:** exact single-source/sink comparison is
  Square-Root-Sum equivalent. The elementary rational gadget, upper reduction,
  integer-resistance scaling, and degree-three triangle construction passed
  independent review and 120 checks. A separate literature audit distinguished
  known series-parallel reduction operations from exact zero-gap bit comparison,
  including relevant 2026 followup work. Promotion of the result is underway;
  a multi-entry approximate algorithm is an unverified continuation.

New constructive directions include multi-entry cactus optimization and
fixed-input/fixed-pool decomposition. They are not yet recorded as verified
theorems. Publication priority for every new statement remains qualified;
none of the bounded searches proves absence from all literature.

## 2026-09-05 — broader structural results during continuous research

The earlier milestone's pending labels are superseded by the following
completed work. The research goal remains active.

- The fixed-core/small-polyhedral-block theorem passed two proof audits.
  Its pooling corollaries give exact polynomial bit-time algorithms for fixed
  inputs and pools, and for fixed pools and qualities without arbitrary
  bypasses. Reading the final Haugland (2016) primary paper resolved an
  apparent conflict with a preliminary 2014 abstract: the final paper asks
  precisely these parameter questions.
- A complementary reduction from positive linear-product optimization proves
  NP-hardness with two pools and two outputs, upper quality bounds, and
  capacities one or two. Two audits passed, including independent original
  flow solves and source checks. The number of qualities grows. The result
  completes the fixed-terminal branch negatively without a strong-hardness
  claim. Facial quality specifications also received a reviewed universal
  integrality characterization and a restricted bypass-compatible algorithm.
- The cactus additive algorithm passed two audits and was generalized to
  bounded maximum cycle rank within each block. The generalized proof also
  passed two audits: an objective perturbation resolves flat electrical
  adjoint paths and leaves only boundedly many free nominations. Both
  algorithms have polynomial bit complexity, with a parameter-dependent
  exponent. Joint resistance uncertainty and exact arc-capacity validation
  are being reviewed as further consequences of fixed-core elimination.
- Scalar quadratic rank and one-sided inertia precision laws passed review.
  A more general simultaneous-quadratic theorem now identifies half the
  noncommutative Hessian-space rank as the exact leading coefficient. One
  audit passed and a second is running. An elementary Hall/permanent argument
  supplies the volume estimate without operator capacity. A separate source
  audit found no matching theorem but credits the established algebraic and
  mixed-integer convex machinery.
- Higher-order spatial SOS, product-domain, and relative-gap extensions passed
  review. A known clique cut closes their original family and is recorded
  prominently as a limitation. A stronger sparse-XOR construction survives
  all quadratic inequalities of each node box; a further monomial-lift
  extension is under independent review. No claim extends those cuts to
  arbitrary higher-degree localizers or the convex hull of the feasible
  lifted graph.

All useful candidates, failed routes, proof audits, source limits, and
verification scripts are retained locally. The working impact assessment
is `notes/research-continuation-assessment.md`.

## 2026-09-05 — finite formulation construction and broader flow laws

Continuous research produced the following further verified milestones.

- **Near-minimal integer dimension in polynomial bit time.**
  `results/quadratic-weighted-precision-polynomial-construction.md` gives
  a deterministic rational MILP construction for arbitrary rational
  quadratic systems and unequal rational tolerances, within
  `O(n log(n+1))` binaries of the minimum unrestricted-integer convex-lift
  dimension. Two full proof audits passed, including the finite-bit
  implementation. The underlying maximum-determinant covariance law also
  passed two audits. A self-contained rational orthogonal Jacobi routine
  closes the spectral computation step. Separate source comparison credits
  older anisotropic metric selection, geodesic methods, and operator
  scaling; the whole-formulation approximation guarantee is the apparent
  new contribution. Practical runtime is not claimed.
- **Smooth maps.** The local noncommutative-rank lower bound passed two
  audits. It combines the established mixed-Hessian oscillatory estimate
  with matrix evaluations and the parity mechanism. The global Hessian-span
  upper bound matches it under specified rank equality, including the full
  local rank case. Fixed-degree polynomial maps have compact formulations.
  A scalar constant-Hessian-rank theorem and a positive-perspective transfer
  passed their independent audits. Examples show why global Hessian-span
  rank is not an exact invariant for arbitrary smooth maps. A separate
  reviewed rational quadratic theorem gives polynomial encoding and uniform
  input-size overhead; a circuit-PIT reduction is retained as a conditional
  representation-dependent observation.
- **Pooling with bypasses.** One pool and one physical quality give
  NP-completeness under the precise fixed-contract model; the explicit
  reduction and its NP-membership lemma each passed two audits. Related
  hardness was already asserted in the literature, so no first-hardness
  claim is made. The new exact algorithm for fixed pool count, affine
  quality rank, and bypass vertex integrity also passed two audits,
  including 375 exact symbolic mapping checks. It subsumes both earlier
  pooling algorithms. A degree-four hardness refinement passed review;
  degree three and an exact penalty removing lower flow bounds are under
  further investigation.
- **General passive laws.**
  `results/potential-flow-polynomial-law-uncertainty.md` passed two audits.
  Only maximum block cycle rank is fixed: dense polynomial degrees, piece
  counts, and independent affine coefficient counts may grow. Continuous
  laws and polynomial-time validation of uniform strict monotonicity are
  included. Pressure optimization is additive; arc-flow extrema and
  rational capacity comparisons are exact.
- **Fractional powers and arithmetic.**
  `results/potential-flow-fractional-power-arc-barrier.md` gives a reviewed
  single-cycle Square-Root-Sum reduction for exact arc comparison, with a
  separate source audit and 103 independent checks. Conversely,
  `results/potential-flow-fractional-additive-optimization.md` passed two
  audits: positive rational approximation plus the structural algorithm
  gives certified additive pressure and edge-flow optimization for a fixed
  finite family of rational exponents in `(1,3)`, with joint nomination and
  resistance uncertainty. Established quadrature is credited; rational
  encoding, network error propagation, and witness recovery are explicit.
  The distinction between exact thresholds and additive precision is retained.

The goal remains active. Current work includes correlated output-error
budgets, sharper bypass restrictions, exact penalties for flow contracts,
and uncertainty-hull structure on cactus graphs. All reviewed statements
retain their stated scope and qualified publication-priority assessments.

## 2026-09-05 — constant-data pooling and formulation rank refinement

Further research and independent reviews produced these milestones.

- **Strong one-pool hardness with fixed physical constants.**
  `results/pooling-constant-data-two-feed-np-completeness.md` proves strong
  NP-completeness with one scalar upper quality, exactly two pool feeds
  and two outlets, input out-degree at most two, output in-degree at most
  three, and zero lower flows. All physical coefficients lie in fixed
  finite sets; the threshold is linear in network size. Binary averaging
  circuits encode the large rational source data in topology, and a
  contract-completion objective eliminates the large exact penalty used
  earlier. Both complete audits passed. Independent verification compiles
  actual flow and quality constraints, including negative controls, rather
  than adding the intended gate identities to the solver. The proof also
  provides a bounded-degree direct-blending representation of rational LP
  systems. The precise fixed-quality bypass question in Haugland–Hendrix
  (2016) is answered negatively; the later broad hardness assertion by
  Baltean-Lugojan–Misener is credited. No approximation gap or numerical
  robustness follows automatically from strong exact-decision hardness.
- **Nonlinear input rank and general output norms.**
  `results/quadratic-nonlinear-input-rank-precision.md` gives polynomial
  rational MILP construction within `O(r log(r+1))` binaries of the
  minimum unrestricted-integer convex-lift dimension, where `r` is
  stacked-Hessian rank. It includes symmetric output-error bodies with a
  rational strong separation oracle and known inner and outer radii.
  Both distinct audit records are saved. Exact affine quotienting,
  rational zonotope rounding, and the volume-corrected lower bound remove
  affine-only input directions from the overhead. Del Pia's July 2026
  rational Jacobi theorem is credited in the underlying algorithm sources.
- **Discrete flow topology boundary.**
  `results/potential-flow-discrete-arc-capacity-hardness.md` and
  `results/potential-flow-series-parallel-arc-validation.md` each passed
  two full audits. Exact robust arc validation is polynomial at block
  cycle rank at most two and coNP-complete already at rank three under
  independent discrete resistance uncertainty. The positive result uses
  classical circuit sign structure. Older nonlinear tolerance work remains
  a publication-priority caveat.
- **One convex network for fixed-nomination resistance uncertainty.**
  `results/potential-flow-series-parallel-envelope-optimization.md`
  passed two independent audits. On arbitrary series-parallel graphs,
  fixed nominations and independent resistance uncertainty admit a
  target-specific envelope network, a linear-size SOCP formulation,
  polynomial binary-precision approximation, and rational endpoint-scenario
  recovery. This removes the block-rank restriction for that fixed-nomination
  task. It does not assert an exact arithmetic algorithm or an unbounded-rank
  algorithm for uncertain nominations. A dedicated source audit found no
  matching computational theorem but retained inaccessible, directly
  relevant older nonlinear-circuit references as a novelty limitation.
- **Relative-error scope limitation.** The independently reviewed
  `notes/relative-power-graph-integer-obstruction.md` shows that pure
  relative graph accuracy for `x^q`, `q>1`, on a domain approaching zero
  requires infinitely many integer coordinates at every finite tolerance.
  On `[a,1]` with fixed positive tolerance, the necessary and sufficient
  integer count has order `log log(1/a)`. This is a supporting consequence
  of the established integer-residue method, not a claimed new method.

The research goal remains active. Current candidates include a smaller
integer-count overhead for positive separable polynomials, an exact
series-parallel topology characterization for arc uncertainty hulls, and
a tractable bilevel class with many convex follower variables.


## 2026-09-05: compact power precision and weighted-output boundaries

- Promoted the compact pure-power theorem after two complete independent
  audits, including its certified positive rational approximation lemma.
  Its rational MILP uses at most `6.5r+1` more binaries than any convex lift;
  degree affects dense construction size but not this integer overhead.
- Promoted the positive polynomial mixture theorem after two full audits.
  A supporting scalarization gives a degree-free allocation lower bound;
  dyadic endpoint layers give `O(r+sum log log(D_i+2))` binary overhead.
  A separate twice-reviewed example proves a matching-order limitation of
  coefficient-sum allocation, not an overhead lower bound for all algorithms.
- Saved and reviewed unconditional PSD-block, forest Laplacian, and
  independent integer-feature precision refinements. Their product-domain
  and row-width assumptions remain explicit; correlated thin domains
  cannot be replaced by enclosing product boxes without losing guarantees.
- Promoted scalar-leader SPD-box bilevel NP-completeness after final rereads
  by two independent reviewers. No upper constraints are needed; the affine
  upper objective has a zero-versus-two gap. Joint convexity of the full
  lower objective uses its retained leader-only quadratic term.
- Promoted weighted-potential one-cycle discrete-resistance hardness and
  recorded the twice-reviewed tree nomination hardness boundary. Growing
  objective support is essential to the latter comparison with pairwise
  pressure algorithms. The convex knapsack reduction mechanism is credited.
- Corrected the pressure-gap scaling scope: multiplying all resistances
  can amplify potential objectives to fixed absolute gaps while preserving
  flows. It supplies no analogous fixed-gap arc-flow claim.
- The exact rational Bregman certificate refinement passed an independent
  audit and corruption tests under normal and optimized Python. Original
  uncertainty-scenario interpretation still requires the envelope mapping
  to be checked separately from the deterministic energy certificate.
- Two independent audits are checking the fixed-objective-support tree
  algorithm. A bounded-block-rank extension is unresolved because inactive
  blocks can contribute algebraic functions of several shared nominations.

Research remains active. Current priorities include a sharper mixed-power
benchmark, conditioning-sensitive bilevel complexity, and support-parameter
algorithms for weighted potential objectives.


### Weighted objectives: completed support-parameter algorithms

Both independent audits passed the fixed-support tree theorem and the
fixed-total-cycle-rank/support extension. They are promoted to
`results/potential-flow-fixed-support-weighted-tree.md` and
`results/potential-flow-fixed-support-global-rank.md`. The tree theorem has
exact rational outputs and permits finite resistance choices; the cyclic
theorem has exact algebraic outputs and requires continuous intervals.
The tree hardness result is now promoted to
`results/potential-flow-weighted-tree-np-completeness.md`: a rational-QP
certificate argument gives membership for the full arbitrary-support tree
class, and the existing comb reduction gives NP/coNP-completeness. Two
independent reviewers checked this extension. A computable objective-current
sign-pattern parameter is being investigated as a stronger positive scope.


### Sparse and fractional powers: verified circuit construction

Promoted `results/rational-power-compiled-integer-precision.md` after two
full audits through all rational exponents `alpha>1`. The bound is
`p_out<=p_conv+7r+1`, with `6.5r+1` for `alpha>=2`; construction size is
polynomial in binary exponent length. A scaled curvature bound treats
exponents close to one, and certified rational log/exp evaluation supplies
inverse knots. The generic compiler and interpolation have direct prior
work and are credited explicitly.

Promoted `results/sparse-positive-polynomial-circuit-precision.md` after two
full audits. It retains the positive-mixture log-log degree overhead while
replacing dense power recurrences with polynomial-size sparse endpoint
computations. No numerical integration assumption enters either theorem.
The previous explicit Stieltjes construction remains documented as a
reviewed alternative, though the compiler provides the stronger input scope.

The scalar accuracy-dependent curvature benchmark and a rational encoding
barrier for exponents tending to zero are separate candidates under review.


### Bilevel conditioning: verified positive and negative boundary

Promoted the conditioned-box additive algorithm and well-conditioned exact
hardness after two full independent audits each. The positive result uses
saturation cells, a maximum-volume row basis, and exact linear optimization
of direct leader cost; its time is polynomial in input bits, condition
number, and inverse normalized accuracy for fixed leader dimension.
The negative result has a scalar leader, no upper constraints, a unit-box
follower, coefficient magnitudes at most two, and Hessian condition below
two. Its exponentially small gap excludes polynomial accuracy-bit
optimization. Independent exact rational QP/KKT tests complement the
weighted relative-coordinate proof. Prior network scaling and convex
residual-energy approximations are explicitly credited.


### Tight rational encoding barrier and conic separation

The root-authored small-exponent note passed two independent full audits.
For the fixed-error graph of `x^(1/D)`, any rational MILP needs `Omega(D)`
total encoding length, even with arbitrarily many unrestricted integer
variables. Row-wise denominator accounting sharpens the initial coarse
bound. A four-binary, 16-piece construction gives the matching `O(D)` upper.

A separate root-authored conic construction also passed two full audits
and is promoted to `results/small-exponent-milp-soc-encoding-separation.md`.
For `D=2^B`, a homogeneous primal-dual optimal-value representation and
repeated-squaring SOCPs give polynomial rational encoding with the same
four binaries. Exact primal/dual certificates and every selector code were
checked independently. Classical conic numerical compression, power lifts,
and duality are credited. The statement concerns exact conic constraints;
polynomial-size rational polyhedral outer approximations cannot preserve
the same root-graph error by the linear lower bound.

### Pooling endpoint projection and feasibility classification

Promoted `results/pooling-degree-two-boundary-projection.md` after two full
audits, including exact reconstruction and fixed-support optimization.
Its endpoint polygon composition avoids the dense-cost path obstruction.
The contracted constant-data circuit gives a complementary strongly
NP-complete feasibility class at output degree three, while degree two is
polynomial with one pool, two feeds/outlets, and input degree at most two.
Positive exact contracts are retained on the hard side. The fixed-quality
reset construction and its 252 exact original-network certificates remain
as a supporting obstruction to a simplistic quality-alphabet argument.


### Shape-sensitive scalar and separable near-minimum construction

Promoted `results/compiled-curvature-quantile-precision.md` after two complete
independent audits, including the integration dependency. Dense positive
scalar polynomials admit polynomial rational construction with
`p_out<=p_conv+7`. Mass-accurate quantiles suffice; no poorly conditioned
inverse-density assumption is needed.

Promoted `results/separable-convex-graph-linear-dimension-precision.md` after
two full audits. Dense positive polynomial scalar sums admit `12r` overhead,
and independent outputs admit `9r`. A simpler midpoint-tent superadditivity
argument improves the initial feature-distance proof and its constants.
Finite real-coefficient, unrestricted-size comparisons hold for arbitrary
continuous convex summands with `7r` and `4r`. Classical chord approximation,
coding, and compilation ingredients are credited. The arbitrary convex
polynomial compact extension and vector refinement boundary remain separate
active investigations with their own review records.

### Dense convex polynomials without coefficient restrictions

Promoted `results/convex-polynomial-compiled-integer-precision.md` after two
full independent proof audits. Its scalar additive count is 11; separable
sums and independent outputs give 16r and 13r. The signed monotone-curvature
integration lemma is included in both dependency reviews. Exact checks
covered 70 rounding bounds, 14 greedy/dynamic-program comparisons with
2,040 chord decisions, and 11 concatenated indices. The source assessment
credits optimal greedy segmentation (including LinA), certified integration,
and circuit compilation; the succinct near-minimum comparison is the
candidate contribution. The paired nonconvex logarithmic-degree barrier
and compact upper bound remain under final independent review.

### A matching nonconvex degree barrier and a new pooling contract theorem

Promoted `results/polynomial-graph-binary-integer-degree-gap.md` after both
full audits. A rational Bernstein approximation to an M-period triangle
wave has a two-integer formulation at fixed tolerance, but needs at least
ceil(log2 M) binaries. The compact upper for every dense scalar polynomial
is p_conv+12+ceil(log2 D); its degree dependence is sharp in worst-case
order. These are bounds on optimal formulations, not on a surrogate count.

Promoted `results/pooling-fixed-product-contracts-algorithm.md` after two
full audits and 180 LP-fiber checks. Fixed pool outlet count, degree-two
bypasses, exact source supplies, and exact nonreceiving product contracts
permit arbitrary feeds and quality dimension. Conservation removes the
otherwise dense pool aggregates. A stronger fully contracted theorem with
unbounded outlets is being developed through a transformed network flow;
its newer polynomial claim is still under review.

Updated the passive-flow scope map with weighted-flow rank-two hardness,
cactus optimizer/value distinctions, discrete realization versus interval
realization, convex minimization versus maximization, and the three graph
classes in the universal resistance-hull hierarchy. Each indexed statement
has its own proof, audit, and source qualifications.

### Coupled outputs and structured design: verified milestones

Indexed the new single-input curvature-rank and unconditional-body precision
results. Box/facet rank bounds and the oracle-body product-box bound each
passed two full audits. Source reviews located exact antecedents for
barycentric spanners, proportional fairness, common-knot vector SOS2, and
implicit sorted selection; the proposed contribution is the uniform compact
comparison against arbitrary convex general-integer lifts. Nonconvex vector
construction is now also promoted with logarithmic total-degree overhead.

The root's affine-strip path projection lemma passed an independent full
review and 1,200 exact comparisons with original-coordinate propagation.
It is supporting classical difference-constraint elimination with explicit
parameter and encoding control. The related pooling quality-scaled theorem
was separately promoted after two reviews; fixed contract exceptions and
fixed affine quality rank are under further audits.

The root's monotone-polynomial root optimization lemma passed two full
reviews, including the fixed-breakpoint extension. It uses LP threshold
search below a uniform vertex-root separation bound to return an exact
rational optimizing vertex. Review corrected 'polynomial height' to
'polynomial coefficient bit length' and made the original-face Cramer bound
explicit in lexicographic LP extraction. Its source assessment recommends
supporting arithmetic positioning, not a new general optimization paradigm.

Updated the flow map with exact-capacity and within-cycle correlated-polytope
design, few-measurement convex maximization, and the region-convexity
characterizations. Verified the new bilevel structural boundary, including
exponential message size with identical factors. No claim of a false prior
PWL closure theorem is made: explicit intermediate representation can grow.

### Stronger closed milestones and next investigations

Promoted the exact convex degree-32 count family after two independent
reviews: p_conv=n and p_bin=ceil(n log2 3), with unit box error and fixed
numerical data. Root checked72 middle-slice vertices,2048 exact mixtures,
and390 product-contact pairs. The familiar discrete ternary count law is
credited; the continuous convex polynomial transfer is the scoped result.

Promoted the strongest pooling contract-exception algorithm with arbitrary
quality count and rank. Both full audits verify the active-product affine
plane case and the exceptional-only output fraction case. The separately
promoted five-exception fixed-data feasibility reduction supplies the sharp
output-degree-two versus three boundary. Variable filler sources in an
early hardness outline were caught and repaired by exact complementary
source grouping before the final claims passed review.

The power-cost bilevel theorem is promoted with numerical degree P variable:
only leader dimension is fixed, and time is polynomial in input bits, P,
and accuracy bits. Its sparse-binary degree obstruction concerns rational
output length. Positive polynomial inverse approximation and a one-resource
extension are being investigated next. The full Vigneron primary manuscript
was retrieved, and its bit-model approximation discussion is explicitly
credited rather than incorrectly omitted from the comparison.

Promoted global-correlation flow and energy hardness and the corresponding
arc-feasibility algorithm with direct prior attribution. The any-graph
energy-maximization SOCP companion is under separate audits. A link scan
checked2,304 local artifacts with no missing targets; git diff --check passed.

## 2026-09-05 (later) — new direction: existential theory of the reals

The user reopened the goal and asked for more impactful, genuinely new
results. After a survey of the repository, status checks on pooling
approximation (only Dey–Gupte's n vs n^(1-eps) is known), on the HENS
minimum-number-of-matches problem (single interval is APX-hard with a
6/5+eps approximation by Chen–Li–Liang 2025; multi-interval constant factor
open), and on OA/information-complexity theory (Basu et al. conjectures 1
and 3 untouched), the root chose a new complexity direction.

- **Pooling is ∃R-complete (draft).** `results/pooling-existential-theory-of-reals.md`
  reduces ETR-INV (Abrahamsen–Adamaszek–Miltzow 2018) to Haugland's Pooling
  Problem with one quality attribute, source qualities in {0,1}, lower and
  upper terminal bounds, no direct arcs, and objective-forced saturation.
  Consequences: pooling is not in NP unless NP = ∃R; rational instances can
  require optimal flows of arbitrary algebraic degree. The gadget script
  `code/pooling_existential_reals/build_and_check.py` passed seven Gurobi
  checks (including 1/√2 and golden-ratio solutions). Two proof audits and a
  novelty audit are running; the three ∃R sources are being ingested into
  the literature base.

Update (2026-09-05, later): the first proof audit
(`notes/review-pooling-existential-reals-1.md`) passed with corrections:
the slack bound had to count inversion arcs `(P_x,t)` in `M` (a genuine
error, found with a Gurobi counterexample), `M ≤ 2m+1`, costs lie in
`{0,-1,-2}`, pools have in-degree at most two, and the algebraic-degree
corollary now uses the linear-extension clause of Abrahamsen–Miltzow's
Theorem 1 (unique threshold-feasible flow with a value of the same degree
as `α`). All applied; the checker was aligned with the text (diluent and
slack capacities `B`, inverse pools always created, certified `OPTIMAL`
status asserted) and passes. The novelty audit
(`notes/pooling-existential-reals-novelty.md`) found no prior `∃R`
statement for pooling or any blending network; it credits Schaefer 2013
(unit ball), Schaefer–Štefankovič 2017, and Poss–Kurtz–Goerigk–Henke
(arXiv:2608.21574, Theorem 4) for unstructured QCQP, and Haugland–Hendrix
2015 for an implicit degree-two irrational optimum. The three `∃R` sources
were ingested into the literature base
(`literature/runs/2026-09-05-etr-inv-open-copies/`).

A sharper one-pool theorem was drafted:
`results/pooling-one-pool-bypass-existential-reals.md`. One pool with
bypass arcs and unboundedly many attributes is `∃R`-complete (auxiliary
sources pin products of pool proportions; additions are attribute columns);
one pool without bypasses (Haugland's terminal-subset LPs) or with fixed
attributes (linear fibers) is in `NP`. Its checker
`one_pool_build_and_check.py` passed eight Gurobi cases. Two audits are
running. The brainstorm of alternative directions is kept in
`notes/candidate-directions-2026-09-05.md`.

Update (2026-09-05, evening): the user asked to finish and verify the
current ideas without starting new ones. Status of the current ideas:

- General pooling `∃R` theorem: both audits applied; bounded-data chain
  variant (Theorem 1′) audited (`notes/review-pooling-existential-reals-bounded.md`,
  PASS WITH CORRECTIONS, applied). The one-attribute upper-bound-only
  version is recorded as open: a literature check of Miltzow–Schmiermann
  (TheoretiCS 2024) shows that addition plus a single concavely curved
  inequality such as `x·y ≤ 1` is not known to be `∃R`-complete (their
  FOCS 2021 text states this explicitly), and one-attribute upper bounds
  only produce constraints of that type.
- One-pool bypass theorem: audits A and B passed with minor corrections
  (citation precision, explicit capacity constraints with bypass arcs,
  Boland et al. scope); applied.
- Power flow: `results/ac-power-flow-existential-reals.md` drafts
  `∃R`-completeness of the resistive power-flow model (voltage times
  linear current within injection bounds) by the same gadget method, and
  of AC feasibility via an energy argument that zero reactive injections
  force equal angles on resistive lines. Checker
  `code/power_flow_existential_reals/dc_resistive_build_and_check.py`
  (resistive QCQP and full rectangular AC model). Two proof audits and a
  novelty audit are running; results will be applied before closing.

Update (2026-09-05, night): both power-flow audits found a genuine gap in
the first draft of Theorem 2: with per-line angle limits expressed on
principal differences in rectangular coordinates, an `n`-cycle (`n ≥ 4`)
with equally spaced unit voltages has zero reactive injection everywhere
but unequal angles, so Lemma 4 failed as stated. Fix applied: Theorem 2
now uses real (polar) angles with real-difference limits, membership in
`∃R` is proved by a winding-number crossing count on fundamental cycles,
and a rectangular variant with bus-angle boxes `|θ_i − θ_ref| ≤ π/4` is
stated. Credits added per the novelty audit
(`notes/power-flow-existential-reals-novelty.md`): Lavaei–Low 2012
Appendix B Case 2 (resistive/zero-reactive reduction without angle
limits), Dörfler–Chertkov–Bullo 2013 (cohesive-solution uniqueness),
Gan–Low 2014 (the resistive model), Jeeninga–De Persis–van der Schaft
(LMI decision for the loads-only case). Theorem 1 (resistive model) and
the reduction passed both audits, one in exact arithmetic. A follow-up
audit of the corrected Theorem 2 and Section 1 is running.

Closing update (2026-09-05, night): audit C
(`notes/review-power-flow-existential-reals-C.md`) passed the corrected
power-flow Theorem 2 and its `∃R`-membership proof with clarification-only
corrections; audit B's final part concurs. All corrections are applied,
the checker passes eight cases with certified zero-angle bounds on the
small instances, and README and status notes are updated. Per the user's
instruction, no new directions were started; the session's current ideas
(pooling `∃R`-completeness, its one-pool and bounded-data variants, and
resistive/AC power-flow `∃R`-completeness) are finished and verified.


## Final continuation closeout (2026-09-05)

The user requested finishing every already-started direction, thorough
verification, and then a stop without new ideas. The resulting
[closeout](research-continuation-closeout.md) supersedes all historical
running and unfinished statuses. The inventory reconciled the older
precision, spatial, Benders, FBBT, pooling, and flow notes with their
reviews; earlier closed CIA and multilinear lanes were not restarted.

Final developments: twice-audited signed-polynomial inverse approximation;
fixed-resource accuracy-bit bilevel optimization for arbitrary dense
strictly convex local costs; two-source-quality pooling with source supply
intervals and arbitrary bypass topology; exactly contracted degree-two
pooling with restrictive common lower/upper throughput bounds; the verified
any-graph energy-maximization/certificate result; and a reviewed signed-path
weighted-flow corollary. All final-scope reviews passed. The ETR pooling
and power-flow results received a closing scope/certificate audit.

A feature-curve note's missing affine-term exclusion was corrected and
independently checked. Source comparisons and exact angle semantics were
made more precise. Useful negative results, unsupported extensions, and
inaccessible-source priority limitations remain explicit. No new direction
was started during closure. Research has stopped as requested; the final
closeout links verification evidence and the remaining open questions.


## 2026-09-21 — joint convexification of interacting terms: row hulls

- Direction set by the user: joint convexification of interacting nonlinear
  terms (shared variables, conservation constraints).
- Chosen object: the joint hull of separable concave terms on one linear row
  ("row hull"); motivation: the Shapley–Folkman gap that the repository's
  spatial branch-and-bound lower bounds show cannot be closed by branching.
- Findings: [results/row-hull-separable-concave.md](../results/row-hull-separable-concave.md),
  [experiments](row-hull-experiments.md), [theory review](review-row-hull-theory.md),
  [source check that Theorem 2 is the Padberg–Van Roy–Wolsey description](row-hull-ktr-overlap-check.md),
  [MINLPLib scan](row-hull-minlplib-scan.md).
- Negative or limiting results kept: general-width closed form weak; dense
  rows and aggregated node-pair rows gain little; tilted flow cover closure
  recovers 85–100% of the bound; easy instances slower; MINLPLib reach 4.8%;
  mixed convex–concave rows not vertex generated (a concave minorant of `x^3`
  on its envelope gap is the chord itself, so the device gives nothing there);
  triangle rows of difference variables give `s_ij + s_jk + s_ik <= 2`, not
  implied by SDP+RLT on the hexagon, but averaged over triples it is weaker
  than the known SDP value for point packing with five or more points.
- Separation on node boxes: 5–29 times fewer nodes in a minimal
  branch-and-bound, but measured in SCIP it reduces nodes by at most 1.3–3.4
  times and is 4–5 times slower than root-only separation (negative; recorded
  in the experiment record).
- Follow-up pilot: [row hulls with bilinear items](row-hull-bilinear-items-pilot.md):
  exact 6n-variable state form, McCormick-plus-row inexact for random
  directions, no bound gain on blending and pooling pilots (negative).
- Shared-variable line: [term links](../results/shared-variable-term-links.md)
  with [literature note](shared-variable-terms-literature.md). Closed on the
  user's instruction to finish open work and start nothing new. Independent
  [review](review-shared-variable-term-links.md) applied: two errors corrected
  (pricing050 sign, volume number). Open ends left explicitly: no rule for when
  to add a link, no hull cuts, uncertified bounds.
- Closeout of the 2026-09-21 joint-convexification continuation: row hulls
  (reviewed twice, pricing bug fixed and rerun), bilinear-item pilot (negative),
  term links (exploratory). Nothing was committed to git by the agent.
- Term links, closing step: BARON corroboration (direction only), polished
  `waterno2_18` point 5178.159 feasible to `5.7e-11`; node-box separation for
  row hulls measured in SCIP (negative).
- Term links, rule step: reference-exponent choice is a conditioning matter
  (`ex8_4_7` solves with a positive reference, otherwise within noise); an
  evidence-based selection rule is recorded in the results note, marked as an
  observation, not a validated policy; `abs` support added, all 48 instances covered.
- Term links, last step: exact rational residual check of the `waterno2_18`
  point (largest violation `32325/2^49`, less than `5.8e-11`). The objective
  and residual arithmetic are exact; this is a point meeting a `1e-8`
  feasibility tolerance, not an exact feasible-point certificate. The dual
  bounds remain uncertified. This corrects the earlier claim of an exact
  primal improvement.
- Term links, exact-hull step: the two-cone hull of `(x, x^2, x^3)` added in
  Gurobi for the `{2, 3}` pair (19 instances at 60 s, six at 1800 s) dominates
  the relation link on every water instance and lifts `ghg_2veh` and `ex8_4_2`
  above the listed best dual bounds; the "not pursued" label of the SCIP pilot
  is withdrawn. Hull-run incumbents were not saved or verified.

## 2026-09-21 (late) — aggregation certificates for quadratic systems

- Direction survey: screening agents on indicator-quadratic hulls, intersection-cut
  closures and monomial envelopes were cut off by the session quota; the
  cluster-problem/domain-reduction screen completed (Kannan–Barton open question on
  whether bound tightening raises convergence order; no lower bounds on node counts
  exist in that literature) and is kept as a candidate direction.
- Chosen target: Conjecture 3.3 of Blekherman–Dey–Sun (SIAM J. Optim. 2024): under
  hidden hyperplane convexity, `conv(S) = R^n` iff no nontrivial convex aggregation
  exists. Proved in
  [results/quadratic-aggregation-trivial-hull-certificate.md](../results/quadratic-aggregation-trivial-hull-certificate.md)
  by sweeping a supporting hyperplane to infinity and a uniform separation constant
  between the polyhedral cone of aggregated quadratic parts and the PSD cone. Only
  the hyperplanes `{alpha^T x = s t}`, `s -> infinity`, need convex images.
  Corollaries: closed systems with feasible strict system; complete aggregation
  certification (empty / whole space / proper hull) under HHC; SDP decision procedure.
  A separable example shows hidden convexity of `f^h` alone does not suffice.
- Web check: no later resolution found (Blekherman–Dunbar arXiv:2405.18282 does not
  treat it). One independent adversarial review passed (cosmetic fixes applied,
  [record](review-quadratic-aggregation-certificate.md)).
- Additions after review: Corollary 4 (the projected Shor SDP relaxation is the whole
  space iff the hull is, under the same hypotheses) and Corollary 5 (for `m = 2` no
  hypothesis; for `m = 3`, `n >= 3`, PDLC of the quadratic parts `A_i` alone suffices,
  via Polyak's theorem and the perturbation form `M_i(s) -> A_i` of the hyperplanes
  near infinity; general "robust hidden convexity"). Second review of these two
  corollaries requested.
- 2026-09-22: second review (Corollaries 4–5) applied: the Fujie–Kojima parenthetical
  was wrong (exact equality fails; corrected with a hypothesis-free Lemma 4 proving
  `P_SDP = R^n` iff all convex certificates are trivial when `S` is nonempty).
  Added the closed-system example `{x_1 x_2 = 1, |x_1| <= |x_2|}` showing that
  Corollary 1 needs a feasible strict system and that the `Q_lambda != 0`
  hypothesis of BDS Theorem 2.23 is necessary. Literature: Sheriff's "stable
  convexity" names the Corollary 5 hypothesis. Screens recorded:
  [cluster problem / domain reduction](screen-cluster-problem-domain-reduction.md),
  [HEN minimum matches](screen-hen-minimum-matches.md),
  [monomial envelopes](screen-monomial-envelopes.md) (Belotti's `n > 2` lower
  envelope already resolved by Yang–Zhang 2026; ledger row 17 updated).
  Next direction chosen: monomial envelopes with negative or mixed exponents
  (ratio terms) on wedges, and box hulls with value bounds.
- 2026-09-22 (cont.): monomial wedge envelopes for real exponents proved
  ([results/monomial-wedge-envelopes-real-exponents.md](../results/monomial-wedge-envelopes-real-exponents.md)):
  regimes II (both negative), III.A (mixed, `kappa < 1`), III.B1 (mixed,
  `kappa > 1`, `beta >= 1`), III.B2 (mixed, `kappa > 1`, `0 < beta < 1`) added to
  Belotti's I.1/I.2. Mechanism: chord function `phi` (minorant in Case A,
  majorant in Case B) and ray function `H` (convexity by sign pattern) swap
  roles. Numerical LP check over all regimes passed. Review and literature
  check launched.
- Wedge envelopes: independent review passed (presentational fixes applied,
  [record](review-monomial-wedge-envelopes.md)); literature check found no prior
  treatment. A proposed `beta = 0` extension was added as trivial; the later
  ten-agent audit found its ordinary-hull formula false and replaced it with
  distinct ordinary and closed hull descriptions (see the result's Remark 2).
- 2026-09-22 (cont.): cluster problem. Theorem: under LICQ, strict complementarity,
  SOSC and second-order pointwise relaxations, `L(Z) >= f* + c_1 dist(Z,z*)^2 - c_2 w(Z)^2`
  for all boxes near `z*`; a local count for interior-disjoint boxes at a
  comparable scale is independent of `eps` and width with an optimal incumbent
  ([results/cluster-free-branch-and-bound-constrained-minima.md](../results/cluster-free-branch-and-bound-constrained-minima.md)).
  Literature check: Kannan–Barton 2017/2018 and Kannan's thesis leave it open;
  Neumaier 2004 has an unproved remark. Illustration (`code/cluster_problem/`):
  nondegenerate example keeps at most 6 open boxes over the tested `eps`, degenerate example grows
  like `eps^{-1/4}`. Review launched.
- Cluster theorem: independent review passed (mathematics confirmed, adversarial
  numerics found no counterexample; eight wording/scope corrections applied, including
  a verified example showing the literal Kannan–Barton neighborhood property fails for
  standard αBB schemes while the mixed bound holds;
  [record](review-cluster-free-branch-and-bound.md)). Current idea finished; no new
  direction started at the user's request.

## 2026-09-22 — ten-agent corrective audit

At the user's request, ten subagents audited the aggregation, wedge,
clustering, row-hull and shared-variable developments. The
[audit record](review-minlp-developments-20260922.md) supersedes unqualified
earlier review verdicts. Main aggregation and six principal wedge proofs
survived; ancillary claims, boundary cases, and a clustering counterexample
needed substantive corrections. Unsupported domain-reduction guarantees and
overbroad joint-epigraph claims were removed. An endpoint-rounding bug capable
of invalid row-hull pricing was fixed, with a regression. The illustration's
root-only open-box counter was also corrected.

Only targeted checks were run. The record distinguishes proof inspection,
exact witness checks, sampled numerical comparisons, and the historical
benchmark evidence. No project-wide verification, CI inspection, or solver
benchmark rerun was performed. No new research direction was started.

## 2026-09-22 — Lean verification of quadratic aggregation

- Completed [topic 27](../formal/topics/27-quadratic-aggregation/README.md):
  Theorem 1 under asymptotic hyperplane convexity, the HHC specialization,
  and all three supporting lemmas. The original topic identifiers 22–26
  remain queued; the user selected this newer result first.
- The 12 frozen claims map to 11 modules. Targeted warning-free builds,
  the axiom audit of 178 declarations, and all 11 kernel replays passed.
  Independent source and statement reviews found no unresolved issue.
- Strict feasibility bounds the aggregate constant before coefficient
  normalization. A single compact subsequence yields a nonzero PSD
  aggregate, avoiding the original spectral estimates. The source note
  and the developing paper record this equivalent proof.
- Corollaries, examples, numerical scripts, and literature priority remain
  outside the formal scope. No project-wide verification or CI inspection
  was performed. See the [verification record](../formal/topics/27-quadratic-aggregation/VERIFICATION.md).

## 2026-09-22 — continuing theoretical research

The user authorized a new open-ended research continuation. The
[progress record](research-20260922-continuation.md) tracks its current
results, supporting investigations, corrections, and verification scope.

- Proved an explicit HHC example requiring infinitely many good quadratic
  aggregations, answering Conjecture 3.1 in the inspected BDS preprint.
  Independent reviewers strengthened the construction to four variables
  and checked its strict/closed distinction. The
  [result](../results/infinite-quadratic-aggregation-hhc.md) includes the
  indispensable continuum of rays and a finite SDP lift; established SDP
  exactness is explicitly credited.
- Developed [bandwidth-two indicator-QP hardness](../results/indicator-quadratic-treewidth-two-hardness.md)
  with near-identity Hessians. Separate constructions establish a fixed
  Hessian with a large-coefficient constant gap and unit penalties with
  bounded linear coefficients but fine-precision hardness. A fresh review
  and exact enumeration of 3,072 support QPs found no error; priority is
  qualified against hybrid Gaussian inference and recent banded algorithms.
- Corrected the clustering result's novelty assessment after finding its
  central inequality in established exact-penalty theory. The
  [simpler proof and source record](research-20260922-error-bound-transfer.md)
  passed independent review and removes unnecessary named regularity
  assumptions under a linear error bound and feasible quadratic growth.
- Preserved screened moment-interface and oracle-transfer arguments as
  supporting work. Their pending reviews and substantial classical overlap
  are explicit. The sharp Gram-map HHC criterion passed fresh review; its
  main matrix inequality is classical fidelity theory.

Research remains active. No project-wide verification or CI inspection was
performed in this continuation. Exact example checks do not certify
universal proofs or novelty.

## 2026-09-22 — Lean verification of aggregation consequences

- Completed [topic 28](../formal/topics/28-quadratic-aggregation-consequences/README.md):
  Corollaries 1, 3 and 4, Lemma 4, and the two recommended boundary examples
  with actual HHC, including an algebraic proof of Dines' two-form theorem.
- Ten new modules, 158 audited declarations, warning-free targeted builds,
  and all module kernel replays passed; independent semantic reviews found
  no unresolved issue. The Shor converse uses strict open-set separation
  and provides actual PSD witnesses without a closed-image assumption.
- Updated the source note and provided a nine-page consequences supplement;
  numerical solvers and other ancillary claims remain outside the scope.
  The separately recommended infinite-aggregation package is next in the
  [authorized sequence](../formal/QUADRATIC-AGGREGATION-EXTENSIONS.md).

## 2026-09-22 — sharp four-aggregation bound and message follow-up

- Completed the [four-aggregation theorem](../results/four-aggregation-strict-pdlc.md)
  for strict PDLC systems in every positive dimension, including dependent
  triples. Positive definite inward perturbations reduce the proof to the
  published bounded regular theorem. Independent reviews checked the final
  compactification and strict limit; priority remains qualified. The existing
  four-necessary example and its exact witness calculations establish
  sharpness in dimensions at least three.
- The [fixed-data message note](research-20260922-constant-data-messages.md)
  proves exponential exact representation size and a matching support-pruning
  accuracy law. A fresh review confirmed the proofs and clarified classical
  covering antecedents. This is conditional-message complexity; its
  unconditioned objective is easy.
- Targeted coordinator commands passed:
  `python3 code/research_20260922/check_four_aggregation_pdlc.py` and
  `python3 code/research_20260922/check_constant_data_messages.py`.
  They verify finite algebraic cases, not the universal proof or priority.
- Research continues on smoothed exact-message bounds. No project-wide
  verification, CI inspection, or Lean work was performed for these results.

## 2026-09-22 — Lean verification of infinite aggregation

- Completed [topic 29](../formal/topics/29-infinite-aggregation/README.md):
  actual HHC for all `r≥2`, spectral good-multiplier classification,
  indispensable strict rays with uncountably many distinct rays, and the
  finite weak good-aggregation obstruction for the closed hull.
- All 18 modules passed warning-free targeted compilation, the
  248-declaration transitive axiom audit, and individual kernel replays.
  Independent semantic reviews found no unresolved issue.
- Updated the source note and added a clean two-page paper supplement.
  Both packages in the [authorized extension sequence](../formal/QUADRATIC-AGGREGATION-EXTENSIONS.md)
  are complete: 28 new modules and 406 audited declarations. No project-wide
  verification or CI inspection was run. The exact hull formula, general
  Gram-map theorem, arbitrary-quadratic obstruction and quantitative bounds
  remain outside the recommended formal scope.

## 2026-09-22 — Exact infinite-aggregation hull in Lean

Completed [topic 30](../formal/topics/30-infinite-aggregation-hull/README.md):
eight claims, ten modules, 93 audited declarations, all kernel replays and
independent semantic reviews. A new direct two-point proof works for all
`r≥2`, replacing the formal dependency on a general BDS hull theorem.
The strict/closed formulas, actual SDP lifts, weak-system hull and all-good
intersections are verified. Updated the source note and built a clean
two-page supplement. Only targeted checks were run; accuracy is next.

## 2026-09-22 — Finite aggregation accuracy in Lean

Completed [topic 31](../formal/topics/31-aggregation-accuracy/README.md):
ten frozen claims, fifteen modules, 232 audited declarations, all kernel
replays, and independent reviews. The metric is genuinely Euclidean; the
error is extended Hausdorff distance and the optimum is an infimum without
assumed attainment. Verified both stated constants, the inverse-square
rate, explicit tolerance families, exact rational cuts and logarithmic
coefficient sizes. A finite-grid lower proof gives a stronger constant
and implies the source bound. Updated the source and built a clean two-page
supplement. Both user-selected packages 30–31 are complete; no project-wide
checks or CI inspection were run.

## 2026-09-22 — Exact smoothed messages and larger separators

- Consolidated [exact smoothed block dynamic programming](../results/smoothed-indicator-block-dp.md). Separate and fresh integrated reviews found no mathematical gap in full-support elimination, expected work, finite-grid smoothing, bit costs, or the additive objective certificate. The integrated review also showed that deterministic grid dynamic programming already supplies additive approximation; the certificate is not a new approximation frontier.
- The coordinator ran `python3 code/research_20260922/check_smoothed_block_dp.py`: nine exact instances passed, including 66 complete message-envelope comparisons, 892 support QPs, inactive atoms, negative penalties, and evaluations outside retained formulas' winning regions. The checker does not test asymptotic or probabilistic claims.
- Two fresh reviews accepted the [planar region bound](research-20260922-higher-dimensional-smoothing.md), including corner curvature and graph counting. A separate review accepted the [treewidth-two message construction](research-20260922-planar-message-algorithm.md), subject to explicitly fixing the decomposition before noise. Its first-moment analysis alone gives high-probability work, not expected work.
- A [monotone finite-grid transfer](research-20260922-finite-grid-planar.md) passed independent review, including conditional higher-moment transfer and atomic duplicate formulas. A newer VC-dimension argument is now being reviewed; it may directly control all fixed moments with a polynomial-size grid and extend expected exact message construction to every fixed treewidth. These latter claims are not yet integrated or finally reviewed.
- All checks were topic-specific. No project-wide verification or CI inspection was performed for this research. Concurrent formal-verification work is recorded separately.

## 2026-09-22 — Spectral smoothed messages: reviewed closeout

- Completed [exact smoothed indicator messages under spectral bounds](../results/smoothed-spectral-indicator-messages.md). The theorem constructs all subtree message dictionaries on prescribed bounded separator boxes and an exact optimizer for fixed-treewidth positive definite indicator QPs, with polynomial expected bit complexity under explicit numerical bounds. A power-of-two noise grid of at least `2n` points uses `O(log n)` random bits per coordinate. Correctness holds for every realization.
- The final proof uses the classical sandwich inequality to bound expected near-optimal support counts, certified approximate first-difference enumeration, and a parameter net. It requires neither diagonal dominance nor algebraic cell decomposition. Two fresh independent reviews checked the complete construction, conditional spectral bounds, bit costs, and all-tie coverage. The final priority audit identifies established ingredients and leaves publication priority unresolved.
- Preserved the reviewed scalar algorithm, direct fixed-treewidth construction, planar region bound, higher-moment theorem, general finite-grid transfer, and higher-gap oracle conversion as supporting or quantitatively different results. Their scope and relationship to the final construction are explicit.
- Closed the outstanding moment-control and span-three reviews and applied their clarifications. Reviewed the coefficient-magnitude obstruction: fixed conditioning and width two do not justify a uniform encoded-input polynomial smoothing bound over arbitrarily large linear costs and penalties unless NP is contained in ZPP.
- Coordinator targeted runs passed: `check_envelope_higher_moments.py` (2,295 exact distribution cases); `check_nearopt_enumeration.py` (3,276 counting cases and 12,420 adversarial enumeration runs); `check_oracle_all_messages.py` (80 exact parameter families and 1,132 net points); and `check_moment_control.py` (exact small-degree witnesses). All are under `code/research_20260922/`. A topic-only Markdown scan passed on 65 files. These tests support finite identities and algorithm invariants, not publication priority or the universal probability proof.
- Updated the [continuation closeout](research-20260922-continuation.md) and README. No project-wide tests or CI inspection were run for this research. The user requested finishing existing topics without starting new ones; all current proof and review work is now closed, and further research is stopped.

## 2026-09-22 — Represented-matroid spectral verification complete

Completed [topic 22](../formal/topics/22-represented-matroid-spectral/README.md):
all 37 frozen claims in 65 Lean modules, with independent statement and
execution-cost reviews. The actual original-input producer computes row
reduction and rational factors, uses an owner-count profile coordinate,
cached Bird determinants, tensor Lagrange interpolation, and deletion to
return original bases. It proves both relative PSD inequalities, exact
singular ranges, polynomial output size and charged bit work at fixed
information dimension, exact criterion selection, and explicit uniform,
partition, and graphic subclasses including labelled multigraphs.

The topic-only runner passed the warnings-as-errors build, a 1,680-declaration
axiom audit, three execution examples, all 65 individual kernel replays,
and stable-source hashes. Updated the source note and paper; the 67-page
manuscript built without warnings, and its PDF, source archive, and hashes
were refreshed. The numerical supplement was unchanged. No project-wide
verification or CI inspection was run, and no further topic was started.
