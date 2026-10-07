# Coverage and limitations audit

This report implements the scope in `BRIEF.md`. It audits mathematical
coverage and overlap with the sources actually included by the five related
manuscripts. It is not a literature assessment. No experiments were rerun,
no knowledge-base operations were performed, and no project-wide checks or
CI inspection were used.

## Recommendation

Organize the paper around one construction: fresh graded bag and separator
partitions, affine slopes from the same current center, and a dynamic
program that returns a certified lower bound and a reconstructible
configuration. The proof should pass through aggregate copy error and
quadratic growth. This is the mechanism that handles arbitrary tree
decompositions and boundary minimizers without the false tree localization
property. Certified inexact solves, stable nonlinear dynamics, and rational
output should extend this same mechanism.

To cover the authorized developments coherently, the paper also needs three
short mathematical boundaries, rather than only a discussion paragraph:

1. The finite dyadic binary-tree counterexample to unrestricted sup-norm
   localization. This explains why the path localization proof cannot
   establish the main result on trees.
2. The pointwise Euclidean covering lower bound, together with the staircase
   and flat-bag examples. These explain why constant per-bag tolerance shares
   and sup-norm covering proxies cannot be advertised as a sharp general
   characterization of the new certificates.
3. The two-bag affine-constraint obstruction. This explains why feasible
   repair alone cannot replace constraint-aware slopes, and why the dynamics
   theorem needs adjoints and a first-derivative bound.

A compact appendix is a suitable home for the longer counterexample and
covering proofs. The level-synchronous lower bound is useful as a precise
comparison with a natural alternative refinement rule. It is not needed in
the main contraction proof. The old path GR theorem can be described as a
separate, more restrictive nested-refinement construction; the new theorem
does not establish GR's cumulative-refinement count on arbitrary trees.

Several-minimizer results must be separated from the affine relaxed-copy
construction. The current point-growth assumption forces a unique minimizer.
Coordinate-anchor and uniform-cell extensions use a different certificate
and do not extend the new theorem. A precise scope paragraph, referring to
the existing coordinate-grid manuscript, is sufficient. Reproducing those
algorithms would make this a second independent paper.

No topic-wide fatal flaw was found in the scoped results. The mathematical
risks are overstatement at the boundaries between the different certificate
models, not an identified failure of aggregate regridding.

## Authored disposition

After the initial audit, the root assigned this reviewer
`sections/limitations.tex` and `appendices/allocation.tex`. Both files are
written. The former includes the complete finite dyadic branching-tree
localization counterexample and the complete two-bag affine-constraint
lower bound. It states occurrence/factorization dependence, uniqueness,
product-box scope, compressed nonlinear output, and the distinction between
fixed-ratio counts and unknown-conditioning search budgets. The latter
includes the pointwise Euclidean theorem under its additional lower-gap
contract, a compact explicitly finite-state staircase example, and the
single-flat-bag sup-norm dimensional loss. The staircase does not extend
the continuous-box regridding theorem; its continuous variant remains
excluded because its source is a sketch.

The authored files do not reproduce LS, path GR, the exact-bag bracket
lower bound, coordinate-anchor algorithms, dense affine-retraction
algorithms, or the occurrence-free exploration. These are comparative
support or different constructions as classified below. The main
arbitrary-tree mechanism supersedes localization as the route used to
prove this paper's algorithmic claim. Their precise mathematical scopes
remain in this evidence map, rather than introducing multiple independent
refinement algorithms into the scientific manuscript.

## Categories used below

- **Include:** needed for the coherent scientific claim or an essential
  boundary. Restate and prove it, or give a short self-contained derivation.
- **Support:** useful background or comparison. State the precise scope and
  provenance; do not reproduce the entire independent development.
- **Superseded:** an earlier sufficient route replaced by a stronger or
  simpler construction for this paper. Preserve distinctions that the new
  construction does not imply.
- **Exclude:** a different certificate model, an unproved claim, an
  application-specific result, or an experiment not needed for this paper.

“Superseded” below never means that a false statement has become true, or
that regridding proves the behavior of another algorithm.

## Claim map: foundational certificate and consistency theory

The canonical sources here are
`research-20260929/theory-decomposition/decomposition-certificates.md`
and `research-20260929/theory-consistency/consistency-relaxations.md`.

| Source claim | Category | Concrete coverage decision and reason |
|---|---|---|
| Decomposition Definition 1.2; validity Lemma 1.3; chain Lemma 1.4 | Include, with provenance | Define leaves, separator cells, affine minorants, convex child bounds, and all local tests. Prove validity. These are the contract of every output certificate. Already included in `paper-bb-complexity/sections/decomposition.tex`. |
| Common-slope unfolding Lemma 1.5 | Include | Prove the dynamic-programming recurrence, attainment and backtracking. The configuration permits intersecting boxes and does not require copy equality. This distinction drives every subsequent error estimate. |
| DP margin identity Lemma 1.1 | Include where used | It connects globally optimal margins to separator and bag projection margins in the consistency/covering results. Do not treat it as an algorithm for computing exact value functions. |
| Shell Lemma 3.1 and gradient telescoping Lemma 3.2 | Include, with provenance | These are essential proof ingredients. Explain the coordinatewise subtree-gradient sum; it uses assigned bag gradients, not value-function derivatives. Handle clipped boxes, empty separators and equal adjacent bags explicitly. |
| Known-center certificate Theorem 3.4 | Support / superseded as the main result | Briefly state the existence antecedent and its dependence on the supplied factorization. Its full proof is already included in `paper-bb-complexity/appendices/decomposition-proofs.tex`. The new construction removes knowledge of the center and branching from the aggregate constants. |
| Worst-case zero-slope Theorem 3.3 | Support | Useful only to place point growth against general accuracy dependence. It is not the central constructive theorem. |
| Spatial path lower bound and exponential separation Theorem 4.1; factorization examples in Section 4.1 | Support | Already included in the branch-and-bound paper. Use one concise motivating comparison with the same fixed local oracle. Do not reproduce its spatial geometric proof or suggest a solver-runtime lower bound. |
| Bag integral Lemma 2.2; width lower bound Proposition 2.3; flat-product Proposition 2.4; projection covering Theorem 2.5 | Support, except for the upgraded pointwise bound below | The pointwise Euclidean bound contains the fixed-radius projection argument. Use the flat-product example only to explain when simultaneous errors really force a shared budget. Do not add a second catalogue of size lower bounds. |
| Constant-separator Proposition 2.6 | Include as a short slope example | A constant minorant incurs a first-order error even with smooth data. This is the elementary reason to carry affine slopes; it also prevents an incorrect inference from cell placement alone. |
| Consistency Theorem 1.1; attainment Proposition 1.2; envelope Proposition 1.3; general bag relaxation Proposition 1.4 | Support | State the exact-bag consistency interpretation with established provenance. Distinguish a minimum of a bag convex envelope from a joint minimum of separately convexified factors. Do not claim the split duality itself as new. |
| One-separator band identity Theorem 2.1; cellwise Proposition 2.3 | Include | Prove the exact relation between the split gap and distance to the band of exact splits. This supplies the conceptual reason to approximate bands rather than individual value functions. |
| Tree sandwich Theorem 3.1; sequential exact splits Proposition 3.2; sequential bound Corollary 3.4 | Include the joint tree statement; support the sequential variant | The upper bound requires one joint exact split. This explains the consistency problem without promising that independently optimal edge choices combine. The sequential variant is not needed by aggregate regridding. |
| Per-edge failure Proposition 3.3 | Include | A short counterexample is necessary. Each individual band may contain a constant although the joint constant-class gap is positive. |
| Semiconcavity Lemma 4.1; interior pinch regularity Lemma 4.2; affine per-cell Proposition 5.4 | Include where used | Explain the regularity assumptions of the one-dimensional covering theorem. Higher-dimensional second-order claims need a pinch point in the cell or a smooth side; one-dimensional hypotheses do not transfer automatically. |
| Smooth band insertion Proposition 4.3 | Exclude as a proved theorem | The source labels it a sketch. It cannot support a new general smooth-band or hierarchy-rate theorem. |
| Affine exactness criterion Proposition 5.1 | Support | It says exactness requires global minimization of the adjusted bag functions, not only stationarity of a candidate. Useful as a one-paragraph structural comparison. |
| Piecewise constants Proposition 5.2; single-separator shell Corollary 5.5 | Support / superseded | Their precision contrast helps explain affine graded cells. The new aggregate theorem does not need exact child-side value-function smoothness or a single separator. |
| Polynomial-rate Proposition 5.5, kink lower bound Proposition 5.6, SOS-derived Corollary 5.7, hp Proposition 5.8 | Exclude detailed development | These address polynomial consistency and approximation rates, including claims already developed in `paper-sparse-sos`. They are not proof ingredients for constructing affine certificates. In particular the SOS-derived corollary does not independently explain the SOS upper rate. |
| Degree-of-freedom work Proposition 5.9 | Support | Retain its lesson that coefficient count is not computational work. Use the actual new incidence/oracle accounting instead of transplanting its product-of-cells count. |
| Heuristic solver rule, all floating-point experiments and numerical Bernstein constants | Exclude | They are not certified evidence for the new algorithms and are unnecessary to the theoretical contribution. |

## Claim map: adaptive and covering extensions

The two adaptive sources are
`research-20260929/theory-decomposition/extension-adaptive.md` and
`research-20260929/theory-decomposition/adaptive-matching.md`.
The exact-bag extension is
`research-20260929/theory-decomposition/covering-upper-half.md`.

| Source claim | Category | Concrete coverage decision and reason |
|---|---|---|
| Adaptive Lemma A.1, inside–outside min-marginals | Support | A concise recurrence explains what a refinement rule can test without enumerating configurations. It is not needed by fresh regridding. Avoid reproducing an unrelated pruning algorithm in the main construction. |
| Permanent-pruning Lemma A.2; uniform-width estimate A.3; lagged-slope estimate A.4; LS Theorem A.5 | Support / superseded as the chosen algorithm | LS is valid under the additional monotonicity assumption and finds a certificate without knowing the minimizer. It creates more boxes because all live bags share the same level and global deficit. These proofs are not needed for the new nonnested contraction. |
| LS lower bound Proposition A.6 | Include as a scoped comparator, preferably appendix | The actual nonconvex quartic/bilinear path family, fixed termwise alphaBB oracle, and level-synchronous rule force `Omega(n^2 log(1/eps))` leaves for `n >= 63` in the stated small-accuracy regime, whereas `O(n log(n/eps))` certificates exist. The consistent witness eliminates all slope terms, so arbitrary slopes or a better incumbent rule do not remove the bound. It is a lower bound for LS, not all adaptive algorithms. |
| Adaptive conjecture A.7 | Superseded in its unrestricted-tree reading | Path localization with stationarity is proved in the matching note. Unrestricted tree localization is disproved by the finite-certificate construction. State both facts; do not preserve the old conjecture as an unresolved unrestricted claim. |
| Local-solver Remark A.8; other relaxed-gradient slope rules | Exclude | One is a sketch and both add an oracle or variant unnecessary to the authorized construction. |
| Fixed tolerance proxy lower bound B.1 | Support | It establishes a lower half with a width-dependent power of bag count. The stronger pointwise Euclidean bound is the better standalone statement. |
| Staircase Theorem B.2 | Include, preferably appendix | It is a mixed binary/continuous path with only one “fat” bag at each optimum. It proves that a constant allocation `sum eps_t = eps` can overstate necessary certificate size by `N^{d/2}/log N`, `d=w-1`. The exponent of bag count cannot be fixed independently of width in that proposed lower comparison. Its continuous-separator variant is only a sketch and should be excluded. |
| Pointwise covering Theorem B.3 | Include | State admissible functions `e_t` on bag projections, required pointwise only along globally near-optimal assignments. Prove the Euclidean variable-radius bound `N_dec >= sup_eta Phi_2`; retain the weaker sup-norm version only for comparison. This identifies the right shared-error distinction. |
| Flat-bag and staircase sup-norm loss B.6 | Include one compact flat-bag example; support staircase repetition | The gap sums over coordinates, so sup-norm proxies can lose a factor of order `w^{Theta(w)}` even with one bag. Euclidean covering removes this specific loss. The source gives lower bounds and limiting ratios of the displayed bounds; it does not prove an exact limiting value of the actual optimal ratio. |
| One-edge covering upper bound B.4 | Superseded by exact-bag tree upper theorem | It remains a useful special case of the band argument. No separate full proof is needed after the stronger one-dimensional tree result. |
| Revised covering conjecture B.5 | Include as a precise open boundary | Its general relaxed-certificate upper half remains open. Point growth makes the order comparison trivial up to structural constants, but does not settle degenerate optimal sets. Do not describe the paper as a complete covering characterization. |
| Matching Lemma 1 and path GR Theorem 2; LS localization Corollary 4 | Support | The path proof additionally assumes `grad F(x*)=0` and uses two boundary edges in a local exchange. It establishes a distinct nested-refinement algorithm, not a general-tree premise for regridding. If its theorem is stated as a result of this paper, include the complete lengthy exchange proof; otherwise give a narrowly attributed comparison and do not adopt its count for the new algorithm. |
| GR unknown-constants Corollary 3 | Superseded for the new algorithm | Retain the indispensable budget-before-work principle in the new dovetailing proof. The new schedule must budget its own incidence and oracle work, rather than reuse a created-box budget to claim an oracle bound. |
| Conditional tree Remark 3.3, fixed point in slope error | Support | The conditional statement remains correct. Independence from tree size alone is not enough: the localization constant must close the lagged-slope fixed point. No unconditional tree GR theorem follows. |
| Few-leaf tree sketch and restricted branching/conditioning conjecture 7 | Exclude as results | The few-leaf complexity sketch was not completed, and the earlier `sqrt(L)` GR base was withdrawn. A restricted localization conjecture or GR-reachable-partition property remains open; neither is required by the new proof. |
| Matching rule `bd` lower bound Proposition 6 | Support | It proves `Omega(n^(3/2) log(1/eps))` separator cells only for the specified one-dimensional exact-bag quadratic path, exact value functions, the graded split and discount `w_e/(2n)`. It does not cover all bracket rules or dimensions `w >= 2`. Include only if the bound-driven covering rule is discussed as an algorithmic comparator. |
| Covering exact pointwise Lemma 0 | Include | Reduced one-sided separator errors, and any bag errors, must jointly be admissible everywhere. This is the bridge between lower allocation and exact-bag consistency. Reduced and original value functions are not interchangeable. |
| Covering graded exact split Theorem 1 | Include | The edge weights depend on numbers of descendant edges. The resulting margin-discounted bound is joint and valid on trees. It repairs the failure of independent original-band choices. |
| Covering bag-error Theorem 1'; leafwise Lemma 1' | Include a concise extension | These show exactly where the exact-bag theorem stops short of a covering theorem for local relaxed certificates. Leaf errors and closed-cell pieces need their own statement. |
| Optimal discount Proposition 1.3 | Include as a short limitation | On the chain of copies no split admits that form of bound with discount greater than `1/(2n)`. This rules out silently replacing the equal edge share by a constant discount. It is about that bound form, not all certificates. |
| Sharp one-dimensional kink concentration Lemma 2 | Include | The constants are 4, not the older 8. Use either the proved older constants consistently in the upper theorem or redo the accounting before claiming sharpened theorem constants. |
| Exact-bag tree Theorem 3; bound-driven Corollary 3.2; certificate-size comparison Corollary 3.3 | Include | Trees with one-dimensional separators have a covering upper bound under semiconcavity/semiconvexity and Lipschitz assumptions. Computing the exact value functions is outside the new convex-oracle construction. The comparison requires each separator to be contained in its child's gap coordinates. |
| One-edge band placement failure Proposition 4 | Include, combined with the consistency counterexample | The failure is a placement criterion that tests each original band alone. It is not a failure of every edge-by-edge choice of cells or of jointly optimizing values on the resulting cells. |
| Aligned-certificate Proposition 5 | Support, with contract warning | Its equality to a leafwise split relaxation requires aligned projections, suitable cell slopes, and omission of boundary-only pairs in both local and child tests. It is not the unchanged all-touching configuration model. The size estimate and general irregular-allocation realization remain sketches/open. |

## Claim map: regridding and nearby extensions

| Source claim | Category | Concrete coverage decision and reason |
|---|---|---|
| `regridded-certificates/note.md`, Sections 2–6: aggregate drift, shell absorption, current-center error estimate, contraction and termination | Include as the central theorem | These are the essential arbitrary-tree proof. Track the total squared bag-copy error, not the largest copy distance. The generalized valid continuous convex bag model with width-squared error is enough; vertex exactness is unnecessary. |
| Same note Section 7: shell-incidence and local oracle counts | Include | Preserve separate final-size, created-box and convex-oracle counts: one, two and three powers of the stage logarithm, respectively. Use actual separator dimension `q` in the incidence factor `3^q`; do not assume every separator is a proper subset unless explicitly required. |
| Same note Section 8: unknown structural/conditioning constants | Include | Certificate validity is independent of the proof threshold for grading. Budget every counted operation before it occurs. Factor evaluation costs and oracle-internal work remain additional inputs or excluded costs. |
| `inexact-oracles.md`, Sections 2–6 | Include | Certified local lower/upper pairs plus exactly feasible points imply one local objective error per selected bag after backtracking. Gradient/slope errors and incumbent upper errors need separate budgets. There is no multiplier equal to the total number of solved leaf–cell pairs. |
| Same note Section 7: rational reconstruction | Include | Touching pairs may be lower-dimensional faces. Eliminate fixed coordinates exactly and certify the final reconstructed point's objective gap. Small numerical displacement alone does not imply feasibility or the required accuracy. No generic polynomial bit bound follows for arbitrary convex functions. |
| `tree-localization/counterexample.md` | Include, full proof in appendix | Fixed `k=3,w=1,Delta=2`, fixed positive growth and full bag curvature bounds, exact slopes and `theta=0` still permit every minimizing configuration to have root distance more than `K W`, for any fixed `K`. The proof realizes its auxiliary wells by finite actual dyadic partitions and valid concave-quadratic chords. This is not only a generic objective perturbation. |
| `new-direction/constraint-obstruction.md` | Include, full short proof | Exact convex local models and a box-preserving repair of constant one do not cancel the first-order loss. For zero objective-gradient slope every partition needs at least `sqrt(2/3) L/sqrt(eps)` separator cells. A multiplier slope `-L` yields an exact one-cell certificate. |
| `new-direction/affine-repair-exploration.md`, affine-retraction theorem | Support | A supplied box-preserving affine retraction gives computable multipliers and exact first-order cancellation. It introduces full-row-rank/right-inverse promises and possibly dense global repair work. The stable-linear case is the `H=0` limit of the dynamics proof; the general dense affine result is not needed as another main theorem. |
| Same note, infeasibility flags | Include | Constrained local domains can be empty. Use finite intercepts or explicit infeasibility states with inductive evidence, not infinite affine intercepts. The dynamics proof needs this contract. |
| `new-direction/nonlinear-dynamics.md` | Include | Stable scalar box-invariant dynamics, affine outer strips, backward adjoints, forward repair, adjusted-gradient cancellation and aggregate contraction form one coherent extension. State continuous controls, no extra terminal/state constraints, and horizon-uniform derivative/growth bounds. |
| `new-direction/nonlinear-dynamics-bit.md` | Include | Rational fixed-degree polynomial data permit exact local LPs, rational centers, certified forward enclosures and compressed feasible recurrence output. Include the rounding/contraction and precision accounting. Numerical conditioning is a numerical parameter; valid stability, invariance and soundness-critical curvature promises are not discovered by dovetailing. |
| Dynamics example and exponentially long rational trajectory | Include | One explicit uniformly bounded nonlinear family makes the scope concrete. The map `s -> s^2/4` demonstrates why polynomial bit work cannot promise expanded rational coordinates at every stage. Do not claim feasible nonlinear equality after ordinary rounded-state output. |
| `geometric-dp/regridded-qp-bit.md` | Support / optional short specialization | This is genuinely the same affine regridding mechanism specialized to rational quadratics: corner local solves, width-squared Taylor error and common denominators. Its approximate bit bound can support the finite-precision discussion. Its exact recovery/height theorem is a separate endpoint beyond the requested approximation/dynamics result and should not become another main development. |
| `new-direction/weighted-drift-exploration.md` | Support as occurrence limitation | The fixed-center fan example has a constant negative lower-bound gap under the prescribed coefficient allocation and closed-intersection rules, at arbitrarily fine core mesh. Averaging copies cannot fix the lower bound itself. It does not prove nontermination of moving-center regridding or impossibility under other slopes, partitions, decompositions or factor allocations. |
| `new-direction/positive-overlap-exploration.md`, laminar-copy lemma and soundness | Support | Omitting both classes of touching pairs in a common dyadic hierarchy removes coordinatewise accumulated drift on a product box. It changes the certificate contract; boundary completeness needs its own proof and does not automatically hold with equalities. |
| Same note, isotropic affine-model obstruction | Support as the stronger occurrence caution | Even with zero drift and positive overlap, replicated coarse widths can yield a fixed negative gap for the specified affine Taylor models on an easy convex star QP. Thus positive overlap alone does not remove occurrence from aggregate model error. It is not an optimization lower bound or nontermination proof. |
| Same note, anisotropic aggregate estimate and Cartesian-product counting barrier | Exclude detailed construction; support the limit | Coordinatewise grading with canonical Hessian allocation repairs the aggregate estimate, but an explicit rectangular cover needs `Omega(log(1/h)^p)` boxes. It does not establish an occurrence-free FPT bit theorem. This is a separate proposed representation change. |
| `new-direction/mixed-stable-audit.md` | Exclude as a main extension | It requires exact local enumeration and global mixed point growth; separate growth within control assignments is insufficient. Enumerated state counts enter exponentially unless domains are bounded. The canonical dynamics theorem is continuous-control; no mixed theorem follows automatically. |
| `new-direction/nonlinear-shell-certificate.md` and other candidate/unknown-growth shell developments | Exclude | These certify a supplied polynomial candidate through different quadratic/coordinate-grid closure machinery. They are not the affine separator regridding theorem and are already part of a separate later development. |

## Several minimizers: exact boundary

The inequality used by the main regridding proof,
`F(x)-f* >= g ||x-x*||^2` with `g>0`, forces uniqueness: any other
minimizer has zero objective gap and hence equals `x*`. This should be said
once near the hypotheses. Replacing the distance by distance to the entire
optimal set is not a syntactic change. A fresh center can lie near one
optimizer while distant optimal components retain coarse cells and depress
the lower bound. The pointwise contraction argument does not supply a
retained union of centers or a progress charge for discovering components.

The related files found by scoped search do contain real several-minimizer
developments, but their representations are different:

| Source | Category | Exact result and why it is outside the new main theorem |
|---|---|---|
| `new-direction/projection-anchors.md` | Support, exclude detailed proof | Shared coordinate grids use a separable interpolation correction and retained coordinate anchors. Under set growth, failed solves can be charged to optimal coordinate values; finite projections yield polylogarithmic accuracy dependence, and compact projections yield covering-number work. A separable double well can have exponentially many optimizers but only two optimal values per coordinate. The source explicitly says it is not an extension of the relaxed-copy certificate model. |
| Projection-anchor integer stopping | Exclude | Exact integer table comparisons can force zero interpolation correction. This does not prove exact continuous reconstruction or an affine relaxed-copy integer theorem. |
| Projection-anchor diagonal-segment obstruction | Support with precise model | `F=(x_1-x_2)^2` has a continuum of optimizers and uniform set growth, yet that corrected-grid formula needs `Omega(eps^(-1/2))` nodes per coordinate. It is a formula-specific lower bound; a different convex certificate solves the example immediately. |
| `new-direction/nonunique-anchor-compression.md` | Support / superseded for manuscript exposition | Uniform filtered unions have `O(a_i(1+sqrt(n kappa)))` coordinate states and remove the width-dependent accuracy exponent, but keep `n^(p/2)` table work. The stronger bound parameterized only by width, maximum optimal-coordinate count and conditioning remains open. A separable convex quadratic has `Theta(sqrt(n))` qualifying nodes per coordinate despite one optimal coordinate value, so a fine `O(a_i)` cover of all qualifying nodes cannot be assumed. |
| `geometric-dp/exact-nonunique-box-qp.md` | Exclude | Exact rational height/recovery transfers for finite optimal sets belong to the coordinate-grid manuscript. They do not remove the point-growth hypothesis from affine separator contraction. |

The included version of `paper-decomposition-aware/sections/optsets.tex`
already develops the stronger, submission-ready boundary: a continuous
two-minimizer counterexample (lines 21–69), uniform-cell bounds (109–163),
all-optima endpoint descriptions for coordinatewise concave quadratics
(167–299), and diagonal-Lagrangian optimal-set discovery (302 onward).
These actual included statements take precedence over earlier exploration
notes when comparing claims. In particular the earlier coordinate-anchor
algorithm is not itself present as a main theorem in that manuscript.

## Actual overlap with existing included manuscripts

Only sources reachable through the current `main.tex` input graph were used
for this comparison. A matching keyword in an unused draft or evidence file
does not establish manuscript overlap.

| Existing manuscript | Actual included overlap | Boundary for this paper |
|---|---|---|
| `paper-bb-complexity` | `sections/decomposition.tex` includes the certificate definition and validity (lines 22–151), common-slope intercept recurrence (155–168), known-center existence theorem (170–228), fixed-termwise path separation (232–292), and stored-size/query/checking distinctions (294 onward). The corresponding proofs are in the included `appendices/decomposition-proofs.tex`. | Restate the certificate contract and essential shell/telescoping lemmas with provenance. The new contribution is construction without the minimizer, aggregate arbitrary-tree error, inexact contracts and constrained/finite-precision extensions. Do not claim the representation separation or known-center existence anew. The adaptive pointwise covering, staircase and sup-norm-loss results are not already in this included decomposition section. |
| `paper-decomposition-aware` | Shared-coordinate interpolation corrections and exact finite-state DP in `sections/grids.tex`; adaptive grading/filtering in `growth.tex`; exact recovery in `exact.tex`; recourse, constraints and nonunique sets in their included sections. Certified inexact recourse filtering appears in included `recourse-local.tex`, with error-oscillation accounting in `appendix-recourse-convex.tex`. | Its globally consistent grid assignments differ from the incompatible-copy affine certificate. It already owns the coordinate-grid, recourse and several-minimizer algorithms. New inexact theory must specify its changed contract: local convex solves, affine separator residuals and selected-configuration accumulation. |
| `paper-certified-support-cuts` | Included `03-composition.tex` proves strict local-hull gaps, interleaving/alternation and persistent gaps after finitely many moment matches; its gluing discussion and `A-composition.tex` treat when local measures glue. Included `06-certification.tex` treats safe finite-precision cut export; `A-separation.tex` treats certified support-oracle weak separation. | These are antecedents for consistency and numerical certification, not the fresh affine regridding algorithm. Do not reproduce the local-hull families, support-direction algorithm, campaigns or quadratic-block machinery. Exact matching of separator distributions is not implied by a finite affine/moment test class. |
| `paper-sparse-sos` | Included setting, kernel, ordinary-rate, sharpness, recourse and regularity sections develop quantitative polynomial/moment consistency. Included `09-certificates.tex` proves short exact rational Gram certificates and the constructive rounding/correction procedure (theorem at line 45; correction at 173 onward). | Cite or briefly contrast degree refinement with local affine cells. Neither the SOS upper rates nor short rational Gram certificates are new here. Finite-precision affine LP output has a different representation and proof. Do not transplant hierarchy rates to the exact-bag split model without per-bag error accounting. |
| `paper-open-minlplib` | Included `04-split.tex` gives path split validity (19–64), value-function minorants (65–75), affine splits (76–88), windows (90–100), and cellwise slopes (102–118). Subsequent theorems concern named instances; included `G-proofs-split.tex` contains their proofs. | Affine/cellwise path splitting is an explicit antecedent. The new general construction does not certify those instance-specific numbers, strengthen those instances, or establish a practical speedup. Exclude the application-specific split identities, computational tables and solver comparisons. |

## Essential proof chains and checks at integration

1. **Unconstrained construction.** Certificate validity and unfolding;
   attained local minima; top-copy reconstruction; exact gradient
   telescoping; occurrence-based aggregate copy error; shell-width
   absorption; current-center error estimate; point-growth contraction;
   stopping gap; shell count; actual incidence and oracle work. Branching
   disappears from the aggregate incidence inequalities because running
   intersection plus occurrence bounds the total shared-coordinate
   incidence. It does not disappear by an unsupported maximum-norm claim.
2. **Inexact extension.** Valid certified local lower bounds; exactly
   feasible returned points; backtracking pays one error per bag; aggregate
   slope residual times aggregate edge drift; certified upper evaluation;
   the modified contraction and stopping constants. Never sum all queried
   pair errors or count inherited child error a second time.
3. **Consistency and covering.** Exact-bag split duality; band identity;
   joint tree distinction; graded exact split; margin discount; one-dimensional
   kink concentration; exact-bag covering upper theorem. Separately, the
   relaxed-certificate chain inequality gives pointwise Euclidean lower
   allocation. No step currently converts arbitrary admissible allocations
   into a matching relaxed-certificate upper bound.
4. **Dynamics.** Box invariance; valid Taylor outer strips; residual bound;
   bounded backward adjoints; cancellation on the entire repaired state
   coordinate subspace; stable forward repair; aggregate repaired-copy
   error and multiplier residual; constrained DP/infeasibility validity;
   contraction. A tangent-space or Hoffman-distance estimate alone cannot
   replace the cancellation.
5. **Bit output.** Rational width-squared objective models, rational strips
   and exact bounded-dimensional LPs; exact lower-bound DP; rational
   backtracking; recurrence-defined feasible output; certified forward
   enclosures and upper objective values; controlled rational reset of
   centers; bit-length and operation budgets. The exact-real theorem alone
   does not prove any of these representation facts.

The localization counterexample's essential chain is also important:
uniform spectrum; bounded-occurrence decomposition; exact convex-square
factorization plus legitimate concave-unary chord relaxations; amplified
auxiliary minimizer; finite dyadic partitions uniformly approximating that
auxiliary objective over **all** configurations; auxiliary growth forcing
**every** minimizing configuration away from zero. Omitting the realization
step would leave only an unrelated perturbation example. Conversely, the
counterexample neither proves a certificate-size lower bound nor shows that
GR reaches its partitions.

## Strongest limitations that should appear explicitly

- Point growth is an instance assumption that forces uniqueness and may be
  small because of a distant nearly optimal local minimum. The theory does
  not verify this global promise.
- The factorization, bag assignment, bag-gradient bounds, occurrence count
  and local lower models are supplied and consequential. Global Hessian
  conditioning alone does not control those local quantities.
- The arbitrary-tree result constructs fresh partitions. It does not bound
  nested refinement, monotone lower bounds, or retained historical boxes.
- Final certificate size, cumulative construction, number of convex calls,
  internal solver work, bit work and serialized proof size are distinct.
  State exactly which each theorem bounds.
- Approximate primal feasibility is insufficient. Lower-dimensional touching
  faces require exact handling; nonlinear repaired states should be emitted
  through their exact recurrence, with enclosures used for evaluation.
- Nonlinear dynamics require a supplied valid graph enclosure, stable
  box-invariant simulation and first-derivative control. A smaller grading
  ratio cannot repair an underestimated enclosure curvature.
- Neither the false localization statement, the fan obstructions, the
  exact-bag bracket-rule lower bound nor the diagonal-segment grid example is
  a universal lower bound for global optimization.
- General degenerate-set relaxed-certificate covering and occurrence-free
  FPT construction remain unproved. Several-minimizer coordinate-grid
  theorems do not silently fill these gaps.
- Unknown-conditioning search bounds total work by the budget of a
  sufficient trial. An earlier winning coarse-ratio trial can have a later
  stage than the sufficient trial; the sharp final-size count for a
  sufficient fixed-ratio run is not automatically a count for the search's
  winning output. The serialized winning output is bounded by the counted
  search budget.

## Local verification record

This audit used scoped file reads and `rg` searches of the named research
directories and included manuscript sources. Two exploratory read commands
used stale/mistyped filenames and returned “No such file or directory”; the
correct source paths were subsequently read. They had no effect on files.
No experiment or theorem-checking script was run. The targeted command
`git diff --check -- paper-separator-certificates/sections/limitations.tex
paper-separator-certificates/appendices/allocation.tex
paper-separator-certificates/evidence/AUDIT-SCOPE.md` passed. A temporary
TeX wrapper in `/tmp/separator-limitations-lfeo5n0o/` included only macros,
model, limitations and allocation. It compiled with
`pdflatex -interaction=nonstopmode -halt-on-error check.tex`; after the
initial two passes reported changed labels, the third pass completed with
no warnings, unresolved references or overfull/underfull boxes. The
allocation author also compiled a targeted model/allocation wrapper and
ran a scoped whitespace check. These are local manuscript checks, not CI
results.
