# MINLP theory notes (PSE-oriented)

Research notes on mixed-integer nonlinear optimization, guided by process systems
engineering. Mathematical review and novelty assessment are recorded separately.
“Independently reviewed” means checked by another research agent, not peer-reviewed
by a journal. An unsuccessful literature search does not establish novelty.

The September 21 continuation adds two solver-oriented results with code,
experiments, independent reviews and their negative findings.
[Envelopes of composite univariate subexpressions](results/composite-univariate-envelopes.md):
Gurobi, SCIP and BARON relax multi-term univariate expressions term by term
and fail on 20-variable separable quartic programs; a SCIP handler with
certified curvature and cuts valid for every slope solves all 48 test
instances in seconds and tightens the root relaxation on 35 of 81 comparable
MINLPLib instances, but as a Python plugin it solves 51 of 107 within 120 s
against 54 for native SCIP
([experiment record](notes/composite-univariate-envelopes-experiments.md)).
[Vertex binarization](results/separable-vertex-binarization.md) turns the
classical vertex property of separable concave structure into a cardinality
constraint on status binaries. It is provably solved in `2n+1`
branch-and-cut nodes on the repository's exponential lower-bound family,
where Gurobi and SCIP time out from `n = 24` on the original asymmetric
model; it is slower on random instances and is a targeted device only
([experiment record](notes/separable-vertex-binarization-experiments.md)).
Both records list solver errors observed in Gurobi and BARON.

The September 21 joint-convexification continuation studies
[row hulls](results/row-hull-separable-concave.md): the joint convex hull of
all separable concave terms on one linear row, used as root cuts for multi-row
models. For equal widths the hull is one min-sum inequality with a compact
extended form; a source check showed that it is the constant-capacity flow
cover polyhedron of Padberg, Van Roy and Wolsey in other variables, so the
contribution is the identification with arbitrary concave terms, inequality
rows, indicators with concave costs, a valid interval dynamic program for
general rows, and the computation. As static root cuts for unmodified solvers
the cuts raise solved instances within 300 s from 96 to 124 of 130 (Gurobi 13),
18 to 41 of 44 (SCIP 10) and 15 to 44 of 50 (BARON) on synthetic concave-cost
transportation and network-flow families; most of the gain comes from
equal-width families built to fit the closed form (with unequal widths Gurobi
goes from 72 to 77 of 80). They make easy instances slower; separating them on node boxes inside SCIP
was measured and does not pay (4–5 times slower than root-only). They are only
modestly stronger than the exhaustive closure of published tilted flow covers,
and apply structurally to 4.8% of MINLPLib
An independent code review found invalid cuts caused by a
pricing bug on two-decimal data; it was fixed and all affected runs repeated
([experiment record](notes/row-hull-experiments.md),
[theory review](notes/review-row-hull-theory.md),
[code review](notes/review-row-hull-code-experiments.md),
[MINLPLib scan](notes/row-hull-minlplib-scan.md)).

A second, exploratory line of the same continuation treats terms that share a
variable instead of a row:
[linking the auxiliary variables of univariate terms](results/shared-variable-term-links.md)
(`sin`/`cos` of one angle, several powers of one nonnegative variable) by exact
redundant relations. The hull theory is known (Ballerstein 2013); the automatic,
solver-independent reformulation is neutral or harmful on most of the 48
MINLPLib instances it applies to, but on the open water-network instances
`waterno2_06/09/12/18` it raises Gurobi's 30-minute dual bounds above the best
values listed by MINLPLib (uncertified single runs; BARON confirms the
direction but not the values) and yields a `waterno2_18` point with objective
5178.16 against the listed 5269.64, with all residuals bounded exactly in
rational arithmetic by `5.8e-11`. Replacing the link by the classical exact
hull of `(x, x^2, x^3)` (two cone constraints) raises those 30-minute bounds
further, by 21% to 130%, and also lifts `ghg_2veh` and `ex8_4_2` above their
listed best dual bounds. The record also documents a
SCIP 10 wrong optimum on `waterno2_02` and `waterno2_03`; an independent review
confirmed the bounds and validity and corrected two errors in the note. A
[pilot with bilinear items on a row](notes/row-hull-bilinear-items-pilot.md) was
negative.

The [certified-MINLP repair and replay record](notes/certified-minlp-repair-and-replay.md)
tracks the September 13 correction of the certificate pipeline: one exact
expression interpretation, rigorous nonlinear cuts, independent rational VIPR
proof replay, and separate complete/partial verdicts. It supersedes the earlier
269/289 acceptance claim and links the current experiments and limitations.
A [small complete example](code/minlp_solver_lab/certify/examples/quadratic/README.md)
can be replayed without a numerical solver. The
[solver discrepancy audit](notes/certified-minlp-solver-discrepancies.md)
checks actual invalid returned points and establishes the exact `clay0204m`
optimum with matching lower and feasible upper certificates.

The [convex GDP development record](notes/lbesh-development-log.md) tracks
the September 19 correction and development of logic-based extended
supporting hyperplanes. It identifies the cuts as established perspective OA,
records fresh theory and implementation reviews, and reports a completed
comparison of radial and point separation. Independent reviews accept
[publication readiness](notes/lbesh-publication-readiness.md) for a focused
computational study with modest impact and qualified claims. See the
[claim register](notes/lbesh-claim-evidence.md) and
[reproduction instructions](code/minlp_solver_lab/LBESH_RESEARCH.md).

The [September 12 evening closeout](notes/research-20260912b-closeout.md)
preserves the historical GDP and certified-MINLP results, superseded by their
respective development records. Its separate demonstration that MINLPLib's
`heatexch_gen1/2/3` are ill-posed (their guarded LMTD is unbounded) retains its
own scope.

The [September 12 closeout](notes/research-20260912-closeout.md) collects the
current continuation's results, independent reviews, software, source-access
limits and corrected claims. Its strongest theoretical candidate is a relative
PSD approximation set over feasible paths and rationally represented matroid
bases. Its implemented methods provide exact global certificates for correlated
measurement selection, including robust kinetic designs and a latent-separator
relaxation. A fixed-physical-grid comparison also records where calendar memory
becomes too expensive. The [contribution map](notes/research-20260912-contribution-map.md)
distinguishes verified mathematical scope, practical evidence and unresolved
publication priority. The [research log](notes/research-20260912-log.md)
preserves the investigation and negative results.

The [Lean topic index](formal/topics/README.md) maps formal coverage by topic.
The [recommended-topic verification sequence](formal/RECOMMENDED-TOPICS-PLAN.md)
tracks the September 17 campaign, beginning with sharp marginal-floor gaps.
[Certified MINLP](formal/topics/14-certified-minlp/README.md) is also complete;
[many-leaf reciprocal hulls](formal/topics/13-many-leaf-reciprocal/README.md)
are now complete too.
[Flat-chain network–simplex thresholds](formal/topics/15-flat-chain-threshold/README.md)
are complete and independently reviewed.
[Deterministic potential-flow certificates](formal/topics/16-potential-flow-certificates/README.md)
are complete and independently reviewed as well: they verify the remaining
certified-computation mathematics of Paper A's appendix, including separate-edge
Bregman intervals, posterior scenario recovery, complete support certificates for
linear goals, sharp conservation-aware curvature bounds, and the exact two-path
comparison.
[Arbitrary-grid one-switch minimax and sharp grid transfer](formal/topics/17-grid-switching/README.md)
is complete and independently reviewed as well. It builds a general
switching-control model — arbitrary mode count, arbitrary grid, arbitrary
horizon — and verifies the exact one-switch minimax value on every grid, the
sharp grid-transfer theorem and its certified coarsening, and the supporting
instance algorithms. Its rounding step is proved from Hall's marriage theorem,
since the network-flow route the sources use has no counterpart in the pinned
Mathlib.
[Positive-box multilinear gaps](formal/topics/18-positive-box/README.md)
are also complete: the package proves the aspect-ratio bounds
`max{2, rho} <= C_box(rho) <= rho + 2` for `rho > 1`, the finite-dimensional refinement,
and transfer to original boxes, including fixed coordinates.
[Structural multilinear gaps](formal/topics/19-structural-multilinear/README.md)
are complete: feedback, frequency-two and incidence-treewidth-two bounds,
including sharpness and the stated box extensions. The [scalar quadratic precision proofs](formal/topics/20-scalar-quadratic/README.md)
are also complete, including the sharp square law, rank and inertia laws, and
explicit finite linear constructions. The [DAG spectral approximation-set
proofs](formal/topics/21-dag-spectral/README.md) are complete, including the
original-input path construction, singular ranges, size and bit-work bounds,
and criterion consequences. The [represented-matroid spectral package](formal/topics/22-represented-matroid-spectral/README.md)
is complete as well: all 37 claims, the original-input base producer, exact
singular ranges, polynomial size and bit-work bounds, criterion selectors,
and uniform, partition, and graphic representations. Its 65 modules passed
independent review, the axiom audit, and individual kernel replays.
Topics 00–22 are complete within their listed scopes; topics 23–26 remain queued. The separately prioritized
[quadratic aggregation package](formal/topics/27-quadratic-aggregation/README.md)
is also complete: the main certificate equivalence, its HHC specialization,
and all three supporting lemmas are proved in 11 Lean modules, with
independent reviews, a 178-declaration axiom audit, and module kernel replays.
Its [consequences extension](formal/topics/28-quadratic-aggregation-consequences/README.md)
also verifies the closed-system and Shor equivalences, exact finite SDP
characterization, and two boundary examples in 10 new modules.
The [infinite-aggregation package](formal/topics/29-infinite-aggregation/README.md)
verifies actual HHC, exact good multipliers, indispensable strict rays and
the finite closed-hull obstruction in 18 further modules. Both extensions
have completed independent reviews and targeted machine checks.
The [documentation follow-up](notes/lean-verification-documentation-followup.md)
records the resulting source corrections, independent reviews and rebuilt papers.
Local work uses targeted checks.
CI handles project-wide verification; do not run it locally or check CI.
The [sequential paper-verification record](formal/COMPLETION-PLAN.md) tracks
completion of the standalone multilinear paper before the focused cubic-gap
paper. Each topic has its own source map, review, and verification evidence.
Start with the [multilinear paper](paper-multilinear-gap/README.md) or
the [cubic paper](paper-cubic-gap/README.md) for a self-contained distribution.

The [Lean verification project](formal/README.md) formally proves the exact
integer-versus-binary counts for the fixed-degree convex box family, including
rational linear realizations. Its [coverage record](formal/COVERAGE.md) and
[verification report](formal/VERIFICATION.md) identify the checked claims and
reproducible build, axiom-audit, and kernel-replay commands.

The 2026-09-07 network–simplex continuation develops observation-sensitive
compressed hulls, complete exact separators, sharp rank-three coefficient bounds,
and exponential coefficient growth on sparse series–parallel networks. A
fixed-state flat-chain theorem gives a complementary positive result. The
[paper-readiness record](notes/network-simplex-paper-readiness.md) collects the
proofs, independent reviews, implementation evidence, measured limitations, and
remaining boundaries.

The switching-control continuation completed on 2026-09-07 has a
[paper-readiness record](notes/cia-reopened-paper-readiness.md): exact minimax
values on arbitrary one-switch grids, exact algorithms for small switch budgets
with minimum dwell times, sharp grid transfer, stronger general bounds, and a
verified correction to a published lower bound. Proofs, implementations,
independent reviews, source comparisons, and unresolved questions are linked there.

The later [bilevel continuation](notes/bilevel-reopened-closeout.md) develops
exact robustness to near-optimal follower choices, certified dense-quadratic
screening, nonlinear aggregate approximation, and response-dependent upper
constraints. It also adds exact scalar tariff algorithms and records independent
reviews, computational evidence, and qualified literature comparisons.
The [nonconvex follow-up](notes/bilevel-nonconvex-closeout.md) adds an exact
global-response implementation with nonconvex aggregate costs, repeated
benchmarks, and an audited classical-literature comparison. It distinguishes
large populations with few response types from costly heterogeneous cases.

The potential-flow continuation requested on 2026-09-06 is complete. Its
[paper-readiness record](notes/potential-flow-paper-readiness.md) collects the
new results, independent reviews, 19 passing validation commands, implemented
solvers and certificates, and remaining boundaries. The
[continuation log](notes/potential-flow-reopened-status.md) records its scope.
The earlier continued research program was closed on 2026-09-05. Its
[current closeout and verification record](notes/research-continuation-closeout.md)
identifies the completed results, corrections, review evidence, and questions
retained as unresolved. The
[earlier closeout](notes/research-closeout.md), [research log](notes/log.md), and
[historical continuation status](notes/reopened-run-status.md) preserve the
preceding work; the current closeout supersedes their running-task labels.

## Results and current investigations

The September 22 continuation develops these theoretical results:

- [Four aggregations for strict three-quadratic PDLC hulls](results/four-aggregation-strict-pdlc.md)
  removes the regularity and infinity assumptions from the published
  four-aggregation bound by inward compactification and a strict limiting
  argument. It covers every positive dimension, including dependent triples;
  the existing four-necessary example proves sharpness in dimensions at
  least three. The closed hull of the strict set has four oriented SOC
  constraints. Independent reviews and a primary-source priority audit are
  recorded; no efficient multiplier algorithm is established.
- [Infinite quadratic aggregation under hidden hyperplane convexity](results/infinite-quadratic-aggregation-hhc.md)
  gives an explicit four-variable, three-constraint example answering
  Conjecture 3.1 in the inspected Blekherman–Dey–Sun preprint. Its ordinary
  hull requires uncountably many good aggregation rays, and even its closed
  hull has no finite good aggregation description. A small SDP lift remains
  possible. Independent proof and novelty reviews distinguish this obstruction
  from established SDP exactness and earlier infinite-aggregation examples.
  [Lean verification](formal/topics/29-infinite-aggregation/README.md)
  now covers HHC, spectral goodness, strict-ray uncountability, and the finite
  closed-hull obstruction; the hull formula, SDP lift, and stronger arbitrary
  quadratic obstruction remain outside that formal scope.
- [Indicator quadratic hardness at bandwidth two](results/indicator-quadratic-treewidth-two-hardness.md)
  proves exact NP-completeness for Hessians arbitrarily close to identity
  on a chain of triangles. One construction has an input-independent Hessian
  and a constant absolute gap with large coefficients; another has unit
  penalties and bounded linear coefficients but a potentially exponentially
  small gap. The results complement tree algorithms and do not contradict
  existing approximation guarantees. Independent review and 3,072 exact
  support-QP checks are recorded. A
  [reviewed fixed-data message construction](notes/research-20260922-constant-data-messages.md)
  gives exponentially many indispensable exact quadratic formulas and a
  matching, horizon-independent support-pruning accuracy law. Its
  unconditioned objective is easy; it is a representation lower bound.
- [Exact smoothed indicator messages under spectral bounds](results/smoothed-spectral-indicator-messages.md)
  constructs complete bounded-parameter message dictionaries and an exact
  optimizer in polynomial expected bit time for fixed-treewidth positive
  definite indicator QPs with polynomial numerical bounds. Independent
  penalty perturbations use only logarithmically many random bits per
  coordinate. Two independent proof reviews and exact adversarial checks
  support the construction; novelty remains provisional. The algorithm
  enumerates nearly optimal supports through additive approximation oracles.
  It requires neither diagonal dominance nor bounded biconnected blocks.
  Earlier [scalar](results/smoothed-indicator-block-dp.md) and
  [direct treewidth](results/smoothed-fixed-treewidth-indicator-dp.md)
  constructions remain documented, along with a
  [planar region bound](notes/research-20260922-higher-dimensional-smoothing.md)
  and [all fixed support-count moments](notes/research-20260922-envelope-higher-moments.md).
  No practical speedup is claimed; additive approximation alone is already
  available from deterministic grid methods.

Priority remains provisional. The
[continuation record](notes/research-20260922-continuation.md) distinguishes
these contributions from classical corollaries, screened directions, and
reviewed supporting work and documented open questions.

The [2026-09-22 corrective audit](notes/review-minlp-developments-20260922.md)
records a ten-agent review of the developments below, the errors corrected,
and targeted verification. Historical positive review verdicts are qualified
by that record.

- [Cluster-free spatial branch-and-bound at nondegenerate constrained minima](results/cluster-free-branch-and-bound-constrained-minima.md)
  (2026-09-22, proof by the root agent, literature check and one
  independent review, followed by a corrective audit): with second-order pointwise convergent relaxations of objective
  and constraints, the fixed KKT multipliers give
  `L(Z) >= f* + (gamma/4) dist(Z, z*)^2 - c_2 w(Z)^2` for every box near a
  minimizer satisfying LICQ, strict complementarity and second-order
  sufficiency, whether or not the box contains the minimizer; hence the number
  of unfathomable, interior-disjoint boxes with all side lengths in
  `[delta/2, delta]` is locally bounded independently of tolerance and scale,
  assuming an optimal incumbent (or incumbent error below the tolerance).
  This supplies a mixed-bound substitute for the neighborhood convergence
  condition discussed by Kannan and Barton (2018), rather than a total search-tree
  or runtime guarantee. Numerical illustration on a
  nondegenerate and a degenerate example. A
  [later source comparison and simpler proof](notes/research-20260922-error-bound-transfer.md)
  identifies the central inequality as an application of classical
  exact-penalty growth and removes LICQ and strict complementarity under
  feasible quadratic growth and a linear error bound. The novelty assessment
  is narrowed accordingly.
- [Convex hull of a bounded two-variable monomial with real exponents on a wedge](results/monomial-wedge-envelopes-real-exponents.md)
  (2026-09-22, proofs by the root agent, numerical check and one
  independent review, followed by a corrective audit): extends Belotti (Math. Program. 2025)
  from positive to negative and mixed-sign exponents with `a_1 + a_2 != 0`,
  addressing his question on negative exponents; six principal regimes, each envelope being the
  cap or floor of one of four candidate functions (the monomial, the affine
  corner interpolant, a power of a linear form, a power of the monomial),
  selected by quasi-convexity type and the sign of `beta` and `beta - 1`.
  Separate cases treat a zero exponent and degree zero; the latter requires
  distinguishing the ordinary convex hull from its closure.
- [Aggregation certificates for a trivial convex hull of a quadratic system](results/quadratic-aggregation-trivial-hull-certificate.md)
  (2026-09-21, theorem and corollaries independently reviewed): proves
  Conjecture 3.3 of Blekherman, Dey and Sun (SIAM J. Optim. 2024): under hidden
  hyperplane convexity and nonemptiness, the convex hull of `{f_i < 0}` is the whole space if and
  only if no nonzero nonnegative aggregation has a positive semidefinite quadratic part
  other than a negative constant. Only hyperplanes near infinity need convex
  images; corollaries for closed systems, complete aggregation certification,
  an SDP decision procedure, triviality of the Shor relaxation exactly when the
  hull is trivial, and checkable hypotheses for two or three quadratics (PDLC of
  the quadratic parts, with the scope qualification in Corollary 5); an example
  shows hidden convexity of the homogenized map alone does not suffice.
  The theorem guarantees existence of a nontrivial convex aggregation for a
  proper hull, not that globally convex aggregations describe the entire hull.
  The main theorem and its three supporting lemmas now have
  [Lean proofs](formal/topics/27-quadratic-aggregation/README.md).
  The [consequences extension](formal/topics/28-quadratic-aggregation-consequences/README.md)
  adds Corollaries 1, 3 and 4, Lemma 4, and the strict-feasibility and
  relaxation-strength counterexamples; other ancillary claims remain outside
  the verified scope.
- [Links between univariate terms that share a variable](results/shared-variable-term-links.md)
  (2026-09-21, exploratory, independently reviewed with corrections applied):
  redundant exact relations between auxiliary variables; mixed results, large
  uncertified dual-bound gains on the `waterno2` family with Gurobi, and a
  documented SCIP 10 solver error.
- [Row hulls of separable concave terms](results/row-hull-separable-concave.md)
  (2026-09-21 joint-convexification continuation): closed-form hull for
  equal-width rows (equivalent to the Padberg–Van Roy–Wolsey constant-capacity
  description; extended here to inequality rows and to indicators with concave
  variable costs), a valid residual-interval inequality and interval dynamic
  program for general rows, a three-variable example where row hulls see
  nothing, and solver experiments including cut-generation, model-construction
  and solve time (instance generation excluded). Theory
  and code independently reviewed with corrections applied (including a
  pricing bug that gave invalid cuts; fixed and rerun); computational claims
  qualified by unfavorable cases and a 4.8% MINLPLib structural reach.
- [Joint weighted potential optimization on cacti](results/potential-flow-joint-weighted-cactus-accuracy-bits.md)
  (2026-09-06 continuation): a fixed number of affine load factors permits
  arbitrary weighted potential objectives and independent continuous resistance
  intervals, with polynomial input-and-accuracy-bit additive optimization and
  rational original-scenario recovery. The number of cycles is unrestricted.
  A twice-reviewed nomination-face reduction also permits full balanced load
  boxes when objective support is fixed. With fixed rational nominations,
  exact optimal rational resistance profiles are polynomial-time computable,
  including under rational arc capacities; exact scalar comparison of the
  total objective remains a separate radical-sum question. Fixed-factor
  capacity filters allow algebraic feasible output. Both full proof reviews
  passed; the [source comparison](notes/potential-flow-reopened-weighted-literature.md)
  credits prior cycle formulas, approximate algebraic summation, and resistance
  uncertainty models. No matching combined theorem was found in the inspected
  primary sources; publication priority remains qualified.
- [Original-instance envelope certificates](notes/potential-flow-certified-envelope-pipeline.md)
  (2026-09-06 continuation): a numerical producer and standard-library exact
  verifier now check the original graph, uncertainty data, envelope construction,
  target interval, and recovered endpoint scenario. Conservation-aware goal
  witnesses tighten the bounds without another physical-flow solve. Ten bounded
  benchmarks passed, including 80 edges, a resistance ratio of one million,
  near-zero flows, and a documented quadratic adaptation of an open water-network
  topology. Two independent implementation reviews passed. These are certified
  achieved errors, not a production-scale performance or hydraulic-calibration
  claim; the convex and electrical projection mechanisms are established.
- [Capacity witnesses and resistance sensitivity](results/potential-flow-capacity-rational-witness-boundary.md)
  (2026-09-06 continuation): ordinary positive-width upper capacities can force
  an irrational resistance already on a simple series-parallel rank-two network,
  unlike the fixed-nomination cactus rational-feasibility result. A reviewed
  all-graph Lipschitz estimate gives explicit rational-rounding budgets when
  capacity slack is available. Exact examples and independent checks cover zero
  flows, flow reversals, and nonconvex upper-pressure filters.

Research was reopened on 2026-09-04 and closed on 2026-09-05. Entries marked
"reopened run" belong to that completed continuation.

- [Polynomial construction with near-minimal integer dimension](results/quadratic-nonlinear-input-rank-precision.md)
  (2026-09-05 continuation): for rational quadratic systems and arbitrary
  rational output tolerances, a deterministic polynomial bit-time algorithm
  builds a rational MILP using at most `O(r log(r+1))` more binaries than
  the minimum integer dimension of any convex lift, including unrestricted
  integers, where `r` is the rank of the stacked Hessians. Two full proof
  audits passed for both the original construction and this input-rank
  refinement. Established metric selection and
  geodesic algorithms are credited; the whole-formulation guarantee is the
  apparent new contribution. No practical runtime claim is made.
  A reviewed [approximation-hardness theorem](results/quadratic-integer-precision-approximation-hardness.md)
  rules out additive or multiplicative `O(n^(1-delta))` construction
  guarantees for any fixed `delta>0`, unless `P=NP`, even when the optimum
  integer count is positive. The dimension exponent is therefore nearly sharp.
  The doubly reviewed [general output-norm extension](results/quadratic-general-norm-output-precision.md)
  permits arbitrary symmetric convex error bodies supplied by a rational
  strong separation oracle and known inner and outer radii. Its additive
  binary-count guarantee is independent of the number of outputs.
  For [diagonal convex quadratic systems](results/diagonal-psd-quadratic-linear-dimension-precision.md)
  with componentwise tolerances, two audits verified the sharper bound
  `p_out <= p_conv + 5r + 1` and its polynomial rational construction.
  For [positive rational powers](results/rational-power-compiled-integer-precision.md)
  with exponents greater than one, two full audits verified
  `p_out <= p_conv + 7r + 1`, improving to `6.5r+1` when all exponents are
  at least two. Formulation size is polynomial in the binary exponent
  encoding. The [sparse positive polynomial mixture theorem](results/sparse-positive-polynomial-circuit-precision.md)
  gives `p_out <= p_conv + 4.5r + sum_i ceil(log2(ceil(log2(D_i))+1)) + 1`,
  also with polynomial size in sparse binary exponent lengths.
  Both results permit unconditional convex error budgets with the stated
  oracle access. Circuit compilation and interpolation are established;
  the comparison against arbitrary convex lifts is the candidate
  contribution. For a [scalar sum of dense positive polynomials](results/separable-convex-graph-linear-dimension-precision.md),
  the reviewed bound improves to `p_out<=p_conv+12r`, with no degree
  overhead; independent scalar outputs admit `9r`. The same theorem gives
  finite, unrestricted-size comparisons for all continuous convex
  separable functions. A [scalar curvature algorithm](results/compiled-curvature-quantile-precision.md)
  supplies the compact construction through certified indexed knots.
  The broader [dense convex polynomial theorem](results/convex-polynomial-compiled-integer-precision.md)
  removes coefficient-sign and curvature-monotonicity restrictions: the
  polynomial rational construction uses at most `p_conv+11` binaries in one
  variable, `p_conv+16r` for scalar separable sums, and `p_conv+13r` for
  independent outputs. Both full proof audits passed.
  A paired [nonconvex polynomial theorem](results/polynomial-graph-binary-integer-degree-gap.md)
  proves the boundary is substantive: two general integers suffice for an
  explicit one-variable family, while its binary count grows logarithmically
  with degree. Every dense scalar polynomial admits a compact construction
  with additive overhead `12+ceil(log2 D)`, matching that worst-case order.
  The reviewed [coupled convex-vector theorem](results/convex-vector-curvature-rank-precision.md)
  gives `p_conv+12+ceil(log2 r)` for one input, where `r` is the rank of
  output curvatures, independent of output count and polynomial degree.
  Its [polyhedral error-body extension](results/convex-vector-facet-curvature-rank-precision.md)
  uses `+13+ceil(log2 r)`; weighted one-norm error needs only the constant 13.
  For [arbitrary unconditional oracle bodies](results/convex-vector-unconditional-compiled-precision.md),
  `+14+ceil(log2 m)` suffices with `m` outputs, using a rational inscribed
  box in the final MILP. A stronger [oracle-body curvature-rank theorem](results/convex-vector-oracle-curvature-rank-precision.md)
  replaces the output-count dependence by `17+2ceil(log2 r)`.
  For [coupled separable inputs](results/convex-separable-vector-oracle-curvature-rank-precision.md),
  the overhead is `21n+2nceil(log2 r)`; explicit facet bodies have the
  sharper [separable bound](results/convex-separable-vector-curvature-rank-precision.md).
  The [nonconvex vector construction](results/polynomial-vector-compiled-integer-precision.md)
  instead has overhead `12+ceil(log2(sum_j D_j))`. All have two proof audits;
  established scalarization, basis selection, and shared-knot methods are credited.
  An explicit [exact-count family](results/convex-polynomial-box-error-exact-integer-gap.md)
  shows that linear overhead in input dimension can be necessary:
  degree-32 convex outputs with unit box error have `p_conv=n` and
  `p_bin=ceil(n log2 3)`. This is an unconditional optimal-count separation.
  Further reviewed bounds cover
  [PSD coordinate blocks](results/block-psd-unconditional-error-precision.md)
  and [independent integer linear features](results/independent-integer-feature-quadratic-precision.md),
  including a linear-overhead [forest Laplacian case](results/forest-laplacian-quadratic-precision.md).
  A reviewed [encoding separation](results/small-exponent-milp-soc-encoding-separation.md)
  shows why integer count and rational formulation size are different:
  fixed-error graphs of `x^(1/2^B)` require `Theta(2^B)` rational MILP bits,
  but admit polynomial-size rational MISOCPs. Four binaries suffice in
  both constructions; the conic guarantee uses exact feasibility.
- [Exact bilevel robustness to near-optimal follower choices](results/bilevel-near-optimal-response-robustness.md)
  (2026-09-06/07 continuation): fixed leader, local-block, aggregate, resource,
  and per-criterion measurement dimensions permit polynomial exact robust
  feasibility, infimum computation, attainment decision, and algebraic
  adversarial witnesses. Follower dimension and upper-criterion count may grow;
  aggregate follower costs may be nonconvex. Two full proof audits passed.
  [Certified surrogate screening](results/bilevel-surrogate-screening-exact-optimization.md)
  solves dense quadratic followers exactly using at most `M*3^t` recovery LPs,
  where `t` counts uncertified statuses per surrogate cell. A computable
  perturbation neighborhood bounds `t` by `(r+1)q`, with `q` the vertex
  transition multiplicity. Both theorem and corollary passed two audits.
  [Convex polynomial aggregate coupling](results/bilevel-convex-aggregate-accuracy-bit-algorithm.md)
  extends global accuracy-bit approximation beyond separable followers.
  The [upper-constraint extension](results/bilevel-response-constraint-accuracy-bit-algorithm.md)
  covers polynomial objectives and constraints: unconditional bicriteria
  guarantees and exact rational feasibility under explicit tightening
  conditions. Both results have two full proof audits. The
  [scalar quadratic implementation](notes/bilevel-reopened-quadratic-algorithm.md)
  supplies exact response-path certificates and a complete aligned rank-one
  tariff sweep; recorded experiments are synthetic, not industrial validation.
  Known robustness, screening, and parametric-QP mechanisms are credited;
  the structural complexity combinations retain qualified novelty claims.
- [Exact global bilevel optimization with many follower variables](results/bilevel-fixed-aggregate-response-algorithm.md)
  (2026-09-05 continuation): a fixed number of leader variables, resource
  rows, and aggregate outputs permits polynomial exact optimistic bilevel
  optimization. The follower has positive diagonal quadratic local costs
  and a possibly nonconvex polynomial aggregate cost. Polynomial degree
  may grow under the stated dense or unary encoding. Two full audits and
  a separate exact-arithmetic audit passed. Global follower optimality is
  imposed by comparing all compressed stationary responses; it is not
  inferred from stationarity alone. Earlier resource-allocation methods
  are credited, and the full theorem's priority remains provisional.
  The doubly reviewed [quadratic-block extension](results/bilevel-fixed-block-response-algorithm.md)
  allows fixed-dimensional positive-definite local quadratic programs
  with arbitrarily many local polyhedral rows.
  The reviewed [full constraint-matrix variant](results/bilevel-compressed-response-infimum-semantics.md)
  permits polynomially varying normals and pessimistic follower choices.
  It computes exact infima and decides attainment, including cases with
  no optimizer.
  A complementary [well-conditioned NP-completeness theorem](results/bilevel-well-conditioned-box-exact-hardness.md)
  has one continuous leader, no upper constraints, an affine upper objective,
  and a unique quadratic follower response on a fixed unit box. The follower
  Hessian has condition number below two, and coefficient magnitudes are
  bounded by two. Its gap is exponentially small. The reviewed
  [additive approximation algorithm](results/bilevel-conditioned-box-additive-algorithm.md)
  runs in time polynomial in input size, condition number, and `1/epsilon`
  for fixed leader dimension, with error `epsilon*||a||_1` for follower
  objective coefficients `a`. Thus conditioning does not remove the barrier
  to polynomial dependence on accuracy bits. Both results have two audits.
  In contrast, [diagonal power-cost followers](results/bilevel-bounded-power-accuracy-bit-algorithm.md)
  admit rational additive optimization in time polynomial in input size,
  accuracy bits, and numerical maximum power, for fixed leader dimension.
  Dense or unary growing powers are covered. The reviewed
  [fixed-resource extension](results/bilevel-fixed-resource-accuracy-bit-algorithm.md)
  permits arbitrary dense strictly convex polynomial local costs, including
  signed coefficients, with fixed leader and resource dimensions. Its
  rational leader is exactly feasible; response-dependent upper constraints
  remain excluded. Both full extension audits passed. The
  [bilevel scope map](notes/bilevel-response-complexity-map.md) separates
  these exact, approximate, and representation guarantees.
  A reviewed [leader-interaction boundary](results/bilevel-leader-vertex-integrity-boundary.md)
  gives exact polynomial optimization when deleting a fixed leader core
  leaves components of fixed size. Even a path is weakly NP-complete when
  the component size is unrestricted. Identical local factors can also
  produce exponentially many pieces in an explicit elimination message.
- [Exact optimization with a fixed nonlinear core and small blocks](results/fixed-core-block-polyhedral-optimization.md)
  (2026-09-05 continuation): polynomial bit-time global optimization with
  fixed core dimension, local polyhedral block dimension, and aggregate
  constraint dimension. It gives exact pooling algorithms for fixed inputs
  and pools with unrestricted outputs, qualities, and bypasses; and for fixed
  pools and qualities with unrestricted inputs and outputs without arbitrary
  bypasses. Both proof audits passed. These answer the corresponding
  fixed-pool questions in Haugland (2016); later-literature priority is still
  being checked. The exponent depends on the fixed dimensions.
  The reviewed [bypass-structure theorem](results/pooling-bypass-structure-algorithm.md)
  unifies both corollaries: fixed pool count, affine quality rank, and bypass
  vertex integrity suffice, allowing arbitrarily many quality attributes
  and suitably structured bypasses.
- [The pooling problem is complete for the existential theory of the reals](results/pooling-existential-theory-of-reals.md)
  (2026-09-05; completed proof audits and closing reconciliation): Haugland's
  pooling threshold decision problem with one quality attribute, source
  qualities in `{0,1}`, and lower/upper terminal bounds is `∃R`-complete by a gadget reduction from
  ETR-INV. Hence it is not in `NP` unless `NP = ∃R`, and rational instances
  can require optimal flows of arbitrary algebraic degree. Two independent
  proof audits passed with corrections (applied); no matching statement was
  found in the inspected primary sources. General QCQP completeness is
  established and credited. A bounded-data variant
  (capacities, bounds, qualities, and costs from a fixed finite set; the
  objective threshold remains instance-dependent,
  in-degree at most two, out-degree at most three) passed a separate audit.
  The [one-pool sharpening](results/pooling-one-pool-bypass-existential-reals.md)
  (two audits passed with minor corrections, applied) shows that a single
  pool with bypass arcs and unboundedly many attributes is already
  `∃R`-complete, whereas one pool without bypasses or with fixed attributes
  is in `NP`. Whether one attribute with upper bounds only suffices is
  recorded as open. The attempted upper-only gadget route is incomplete;
  its connection to concave-only constraint systems is not an equivalence
  proof or a necessity result for other possible reductions.
- [AC power flow feasibility is `∃R`-complete](results/ac-power-flow-existential-reals.md)
  (2026-09-05; three audits, corrections applied): the resistive
  power-flow model with power-injection bounds (voltage times linear
  current) is `∃R`-complete by the same gadget technique. Under the stated
  real angle-difference restrictions, zero reactive injections force equal
  angles across purely resistive lines, so full AC
  feasibility is `∃R`-complete even with resistive lines, zero reactive
  injections, degree three, and fixed finite data. This sharpens the
  NP-membership doubt of Bienstock and Verma (2019) into a conditional
  impossibility; their specific lossless fixed-magnitude system is not
  covered. The audits caught and the text now handles a real subtlety:
  angle limits must be on real angle differences (or bus-angle boxes),
  since principal-difference limits admit winding solutions on cycles;
  membership in `∃R` for real angles is proved by a winding-number
  crossing count.
- [Two pools and two outputs already give NP-complete pooling](results/pooling-two-pools-two-outputs-hardness.md)
  (2026-09-05 continuation): with an unrestricted number of qualities, only
  upper quality bounds and capacities one or two suffice. The network is a
  tree with one mixing pool and one pure anchor pool. Two proof audits passed.
  This answers the fixed-terminal portion of Haugland's fixed-pool question
  negatively; a reviewed split-fraction certificate gives NP membership.
  Strong hardness is not claimed.
- [Quadratic systems and noncommutative rank](results/quadratic-system-noncommutative-rank-complexity.md)
  (2026-09-05 continuation): half the noncommutative rank of the Hessian
  space gives the exact leading integer-dimension coefficient as accuracy
  improves, for arbitrary convex lifts and for matching compact MILPs.
  This unifies and strengthens the graph and scalar laws below. Two proof
  audits passed; a separate primary-source audit
  found no matching theorem. The reviewed
  [rational construction](results/quadratic-ncrank-rational-construction.md)
  gives deterministic polynomial bit-time construction and uniform
  polynomial input-size overhead around the sharp precision coefficient.
  A reviewed [perspective transfer](results/perspective-integer-precision.md)
  gives the same sharp law for quadratic-over-linear systems.
- [Smooth nonlinear maps and local rank](results/smooth-map-local-rank-integer-complexity.md)
  (2026-09-05 continuation): noncommutative Hessian rank at one point gives
  an integer-precision lower bound through a classical oscillatory-integral
  estimate. Full rank gives the exact coefficient of half the input
  dimension. Fixed-degree polynomial maps have matching compact MILPs in
  that case. Two proof audits passed. General smooth
  maps have only a local/global rank bound, with counterexamples to equating
  the answer to global Hessian-span rank. The reviewed
  [constant scalar Hessian-rank theorem](results/constant-hessian-rank-smooth-precision.md)
  gives the exact coefficient even when the Hessian null spaces rotate.
- [Finite weighted quadratic precision](results/quadratic-weighted-covariance-precision.md)
  (2026-09-05 continuation): one maximum-determinant covariance problem
  characterizes integer dimension for arbitrary unequal output accuracies,
  within an additive term depending only on dimension. Two audits passed.
  The benchmark is geodesically convex; its reviewed polynomial bit-time
  optimizer supplies the construction listed above.
- [Strong NP-completeness with one pool and constant physical data](results/pooling-constant-data-two-feed-np-completeness.md)
  (2026-09-05 continuation): one scalar upper quality, exactly two pool
  feeds and two pool outputs, zero lower flow bounds, input out-degree at
  most two, and output in-degree at most three suffice. Qualities,
  capacities, costs, and revenues lie in fixed finite sets; the objective
  threshold is linear in network size. Two full audits and independent
  physical-network checks passed. Binary copy circuits and a contract
  completion objective strengthen the earlier large-coefficient reduction.
  Total external input count is unbounded. No approximation-gap or
  numerical-robustness guarantee is claimed; publication priority is being
  checked separately from the established broad one-pool hardness claim.
  A reviewed [linear-fiber certificate lemma](results/fixed-parameter-linear-fibers-np-membership.md)
  supplies NP membership despite potentially irrational mixing parameters.
  The complementary [degree-two bypass algorithm](results/pooling-degree-two-boundary-projection.md)
  gives polynomial feasibility and exact optimization with a fixed number
  of objective arc coordinates, even with many qualities. With one pool,
  two feeds and two outlets, and input total degree at most two, output
  degree two permits polynomial feasibility, while output degree three is
  strongly NP-complete. The hard feasibility side uses explicit positive
  flow contracts; all-zero lower bounds would make feasibility trivial.
  A further [product-contract algorithm](results/pooling-fixed-product-contracts-algorithm.md)
  allows arbitrarily many feeds and qualities when the outlet count is fixed.
  Exact source supplies and exact contracts at products not receiving pool
  flow reduce shared balances to a fixed boundary. It permits standard
  production costs and product revenues, with exact algebraic optimization.
  The stronger [contract-exception theorem](results/pooling-contract-exceptions-algorithm.md)
  allows arbitrarily many feeds, outlets, and qualities of arbitrary rank.
  A fixed number of external nodes may depart from exact flow and product
  quality contracts; shared pool bounds must be redundant. Degree-two
  bypass structure then permits exact standard economic optimization.
  Both full audits passed.
- [Contracted degree-two pooling with common throughput bounds](results/pooling-contracted-common-capacity-algorithm.md)
  admits polynomial exact feasibility with arbitrary common lower and upper
  pool bounds and individual arc lower bounds. It requires exact source and
  product contracts and scalar or affine-rank-one qualities. Both extension
  audits passed; witnesses may have polynomial algebraic degree.
- [Pooling feasibility with two source-quality vectors](results/pooling-two-source-qualities-convex-feasibility.md)
  is polynomial with arbitrary bypass topology, variable source supplies,
  exact product contracts, and restrictive upper pool capacities. Two final
  proof audits passed. A shared convex quadratic constraint gives exact
  rational feasibility; positive outlet or common pool lower bounds are
  outside this theorem.
- [Global energy maximization on any connected graph](results/potential-flow-global-energy-maximization.md)
  permits a global rational resistance polytope and fixed nominations.
  The reviewed conic formulation produces a rational additive-optimal
  resistance profile, with exact rational certificates for proposed designs.
  This is supporting theory based on classical energy concavity and duality;
  minimizing the same energy under global correlations can be strongly hard.
- [Potential optimization with bounded cycle rank in every block](results/potential-flow-bounded-block-rank.md)
  (2026-09-05 continuation): the cactus additive algorithm extends to
  interacting cycles, arbitrary shifted nomination intervals, and arbitrarily
  many blocks. Two proof audits and a separate source audit passed. The
  polynomial exponent depends on the maximum block cycle rank. The
  [joint resistance-uncertainty extension](results/potential-flow-joint-resistance.md)
  and [exact arc-capacity validation](results/potential-flow-exact-arc-capacity.md)
  also passed two proof audits. The latter decides all rational flow limits
  exactly, despite the separate arithmetic barrier for pressure comparisons.
  A reviewed [fractional-power boundary](results/potential-flow-fractional-power-arc-barrier.md)
  shows that exact arc comparison is already Square-Root-Sum-hard on one
  cycle for certain fixed fractional powers. Law representation matters.
  The [dense polynomial-law extension](results/potential-flow-polynomial-law-uncertainty.md)
  also passed two audits. It permits continuous piecewise laws, growing
  dense degrees, and independent affine coefficient uncertainty.
  The reviewed [fractional-power additive algorithm](results/potential-flow-fractional-additive-optimization.md)
  covers fixed finite exponent families in `(1,3)`, including different
  exponents on different edges, with joint nomination/resistance uncertainty.
  In contrast, reviewed [discrete-resistance hardness](results/potential-flow-discrete-resistance-hardness.md)
  shows that independent two-point resistance sets make high-precision
  pressure optimization NP-hard already on a graph with block cycle rank two.
  For discrete uncertainty, [exact arc validation](results/potential-flow-discrete-arc-capacity-hardness.md)
  is coNP-complete at block cycle rank three, whereas the reviewed
  [series-parallel theorem](results/potential-flow-series-parallel-arc-validation.md)
  gives polynomial exact validation at block cycle rank at most two.
  Classical nonlinear-circuit monotonicity is credited; priority relative
  to older tolerance-analysis work remains unresolved.
  With fixed nominations, the doubly reviewed
  [single-network uncertainty algorithm](results/potential-flow-series-parallel-envelope-optimization.md)
  removes the rank restriction on series-parallel graphs: a target-specific
  modified network gives the exact extremum identity, a linear-size SOCP,
  polynomial-bit additive approximation, and an endpoint resistance witness.
  The [flow complexity map](notes/potential-flow-complexity-map.md)
  distinguishes exact arithmetic, nomination uncertainty, discrete
  resistance choices, block rank, and different physical laws.
  For weighted potential objectives, [discrete resistance optimization is
  NP-complete already on one cycle](results/potential-flow-weighted-potential-cycle-hardness.md)
  with fixed nominations. With growing objective support, nomination
  optimization is [NP-complete on degree-three trees](results/potential-flow-weighted-tree-np-completeness.md)
  with fixed resistances. Both boundaries have two proof audits and retain
  explicit attribution to their established reduction ingredients.
  The reviewed [fixed-support tree algorithm](results/potential-flow-fixed-support-weighted-tree.md)
  returns exact rational optima with nomination and finite or interval
  resistance uncertainty. Fixed total cycle rank and fixed objective support
  also permit [exact algebraic optimization](results/potential-flow-fixed-support-global-rank.md)
  under resistance intervals; two full audits passed for each algorithm.
- [Spatial B&B beyond all quadratic box cuts](results/spatial-bb-quadratic-cut-exponential-lower-bound.md)
  (2026-09-05 continuation): sparse cubic instances need exponentially many
  certified spatial regions even with high-order box preorderings and the
  exact quadratic moment hull of every node box. The reviewed
  [monomial-lift extension](results/spatial-bb-monomial-lift-exponential-lower-bound.md)
  permits branching on arbitrary bounded-degree monomial auxiliaries,
  including a standard quadratic formulation with a linear objective.
  Two proof audits passed. Classical XOR pseudomoments are credited; the
  hull granted here is the box hull, not the hull of the feasible lifted graph.
- [Polynomial additive optimization of cactus potential flows](results/potential-flow-cactus-additive-optimization.md)
  (2026-09-05 continuation): arbitrary rational interval nominations on a
  quadratic passive cactus admit polynomial bit-time additive approximation,
  with a feasible rational nomination and a certified optimal-value interval.
  A new structural reduction leaves at most two free aggregate loads in one
  cycle. Two proof audits and a separate source audit passed. The result
  concerns MPD without imposed potential or arc-flow bounds; exact threshold
  comparison has a separate arithmetic barrier below.
- [Pooling with all four degrees exactly two](results/pooling-all-degrees-two.md)
  (2026-09-05 continuation): strong NP-hardness with one quality, unit
  capacities, and bounded constant costs. A polynomial rounding theorem
  converts every feasible flow into integral pure modes without losing profit,
  giving an exact independent-set reduction and a no-PTAS result. Two
  independent reviews and separate original-flow numerical checks passed.
  This closes the degree restriction left open by the preceding local result.
  A reviewed positive-purity-tolerance extension is linked.
- [Integer dimension of bilinear graph approximation](results/bilinear-graph-binary-complexity.md)
  (2026-09-05 continuation): fractional vertex cover gives the exact leading
  coefficient of the minimum integer dimension as accuracy improves. The
  lower bound permits unrestricted integer ranges and arbitrary convex lifts;
  a compact shared binary discretization matches it. Unequal accuracies have
  finite LP bounds within an additive graph-dependent constant. Two proof
  reviews passed; primary-literature comparison found no matching theorem,
  with known parity and discretization mechanisms credited.
- [Quadratic rank and integer dimension](results/quadratic-rank-integer-complexity.md)
  (2026-09-05 continuation): for a scalar quadratic graph on a box, half the
  Hessian rank is the exact leading integer-dimension coefficient as accuracy
  improves, regardless of signature. A maximal-simplex volume bound covers
  arbitrary convex lifts; a compact signed-square construction matches it.
  Independently reviewed, with established approximation geometry credited.
  The [one-sided extension](results/quadratic-inertia-one-sided-integer-complexity.md)
  gives half the negative inertia for epigraphs and half the positive inertia
  for hypographs. It also gives an exact convex-lift precision law for the
  product epigraph. Independently reviewed.
- [Exact cactus potential comparison](results/potential-flow-cactus-square-root-sum.md)
  (2026-09-05 continuation): single-source/sink quadratic cactus MPD threshold
  comparison is polynomial-time equivalent to Square-Root Sum. Hardness holds
  on degree-three triangle cacti with integer resistances and unit bookings.
  Proof and novelty audits are separate and complete. This is an exact
  arithmetic barrier, not NP-hardness or an approximation lower bound.
- [Spatial B&B lower bounds with full SDP and RLT](results/spatial-bb-sdp-rlt-exponential-lower-bound.md)
  (2026-09-05 continuation): exponentially many spatial boxes remain necessary
  at fixed tolerance even with a full second-moment SDP, all box RLT cuts,
  and equality products. Independently reviewed and numerically checked.
  Prior binary B&B lower bounds are explicitly distinguished from the
  arbitrary continuous split model here. The reviewed
  [higher-order SOS extension](results/spatial-bb-higher-sos-exponential-lower-bound.md)
  retains exponential covers through specified linear moment orders,
  including an asymmetric objective with a unique optimizer. Product-domain
  and local polynomial auxiliary extensions are linked from the investigation.
- [Scalar formulation binary and integer lower bounds](results/mip-relaxation-binary-lower-bounds.md)
  (2026-09-05 continuation): the previously unreviewed square/product draft
  passed independent review, with scope and wording repairs. The square
  has an exact binary optimum; the product has matching-order bounds. The
  established parity method extends lower bounds to unbounded general integers.
- [Geoffrion common-optimizer compactness boundary](results/geoffrion-property-p-conjecture.md)
  (2026-09-05 continuation): a reviewed SOC-representable counterexample
  separates the exact Property P-prime conditions despite Slater feasibility
  and attained individual maxima. Positive sufficient conditions are included.
  This does **not** refute the informal computational Property P conjecture;
  its contribution is a narrower structural clarification.
- [One-quality pooling with degree-two pools](results/pooling-one-quality-degree-two-hardness.md)
  (reopened run): open problems 2 and 3 of Boland, Kalinowski, and Rigterink
  (2017) are answered. With one quality, the standard pooling problem is
  strongly NP-hard when all in-degrees are at most two (outputs even of
  in-degree one) and, separately, when all out-degrees are at most two
  (inputs even of out-degree one); pools have the smallest hard degree
  pattern `(2,2)`, and the remaining layer needs degree only three. Reduction
  from `{1,2}`-weighted capacitated orientation. Gurobi cross-check and two
  independent reviews passed for the main theorems, and a third review
  passed the degree-three refinement. Novelty audit in
  [the companion note](notes/pooling-degree-two-novelty.md).
- [Exponential lower bound for spatial branch-and-bound](results/spatial-bb-exponential-lower-bound.md)
  (reopened run): for a separable concave QP with one knapsack equality, any
  variable-branching spatial B&B with separable (chord, McCormick, αBB)
  relaxations needs `2^{Ω(n)}` leaves to certify a fixed tolerance when the
  knapsack level is a constant fraction of `n`, whatever the branching rule;
  a matching `O(2^n)` tree exists, and fixed levels are polynomial. One
  independent review passed with corrections (applied); a novelty search
  found no prior spatial-B&B tree-size lower bound of this kind.
- [Positive multilinear gap](results/positive-multilinear-gap.md):
  A [standalone paper and Lean bundle](paper-multilinear-gap/README.md)
  contains the conjecture disproof, exact dyadic gap, and sharp leading
  degree/dimension asymptotics, with a focused PDF and reproducible proofs.
  The result resolves the universal-constant conjecture and gives the
  sharp asymptotic worst ratio `ln d / ln ln d` by degree and
  `ln n / ln ln n` by dimension,
  with leading constant one. Sparse unit-coefficient lower examples and the
  [matching universal coupling](results/positive-multilinear-sharp-degree-growth.md)
  passed two independent reviews and root review. No prior resolution found in
  targeted searches; priority remains qualified. A reviewed
  [finite bound](results/positive-multilinear-second-order-upper.md) improves
  the lower-order loss without claiming a matching second-order lower bound.
  The [joint characterization](results/positive-multilinear-joint-gap-growth.md)
  combines dimension, degree, incidence width, and distance of the evaluation
  point from box faces, with a single lower family meeting every restriction.
- [Cubic positive multilinear gaps](results/positive-cubic-gap.md):
  exact certificates show that degree three already permits ratios above two;
  a reviewed [analytic family](results/positive-cubic-analytic-family.md)
  proves `483/223 <= R(3) <= 31/12`, with a small certified improvement of
  the lower bound to `1610000/743033` recorded in its proof.
  The [improved upper bound](results/positive-cubic-rounding-upper-bound.md)
  uses a reviewed mixture of three global couplings. The
  [focused cubic paper and Lean package](paper-cubic-gap/README.md) collects
  these bounds, fixed-mixture optimality, and exact finite witnesses with
  a complete mathematical claim map and verification records.
  [Coefficient removal](results/positive-multilinear-coefficient-removal.md)
  transfers fixed-degree suprema to homogeneous unit-coefficient polynomials
  when dimension may grow. Independently reviewed.
  A [simple explicit witness](results/positive-cubic-two-level-family.md)
  uses 52 variables, homogeneous cubic terms, unit coefficients, and strictly
  interior means. [Equal means](results/positive-multilinear-equal-marginals.md)
  always give ratio at most two, as a reviewed consequence of classical envelopes.
- [Frequency-two multilinear gaps](results/positive-multilinear-frequency-two-gap.md):
  sharp ratio `3/2` when each variable occurs in at most two nonlinear terms,
  with an odd-girth refinement and exactness for bipartite dual graphs.
  Independently reviewed; unit boxes and zero lower bounds only.
  A [three-variable counterexample](notes/multilinear-frequency-two-positive-box-obstruction.md)
  shows that bipartite exactness fails with positive lower bounds.
  The [convex-cardinality extension](results/convex-cardinality-frequency-two-gap.md)
  restores the sharp bounds on positive boxes with a common aspect ratio and
  includes a classical matching-based scalar-envelope oracle.
- [Feedback-variable multilinear gaps](results/positive-multilinear-feedback-gap.md):
  deleting `f` variable nodes to leave an incidence forest gives ratio at most
  `2^f`, independently of degree. Sharp for `f=1`; independently reviewed.
- [Sharp incidence-treewidth and sparsity growth](results/positive-multilinear-incidence-sharp-growth.md):
  the worst gap ratio is asymptotic to `k`, with leading constant one, by
  incidence treewidth, degeneracy, or minimum maximum orientation outdegree.
  A variable-radix construction and a matching coupling bound are independently
  reviewed. Unit boxes and zero lower bounds only. The separately reviewed
  [exact treewidth-two theorem](results/positive-multilinear-treewidth-two-exact.md)
  gives sharp constant two through a partition into two totally unimodular
  incidence matrices; larger fixed-width values remain open.
- [Sharp growth near lower box faces](results/positive-multilinear-marginal-floor-gap.md):
  with every normalized mean at least `delta`, the worst gap is asymptotic to
  `ln(1/delta)/ln ln(1/delta)`, independently of degree and dimension.
  Leading constant one; two independent reviews passed. The same asymptotic
  holds when all means lie in `[delta,1-delta]`.
- [Sharp positive-box aspect-ratio growth](results/positive-multilinear-positive-box-sharp.md):
  on strictly positive boxes, `max{2,rho} <= C_box(rho) <= rho+2`, where `rho`
  bounds every upper/lower endpoint ratio. Both upper-proof reviews and the
  separate lower-proof audit passed; degree and dimension are unrestricted.
  [Single-monomial hardness](results/positive-box-single-monomial-hardness.md)
  shows that exact envelope evaluation can still be NP-complete on narrow
  unequal boxes. It does not claim hardness at fixed additive accuracy.
  Its positive rank-one multimarginal optimal-transport consequence answers
  a published logarithmic-precision question negatively in the rational bit
  model unless P=NP. The [source and proof audit](notes/review-rank-one-mot-precision.md)
  and [later-literature check](notes/rank-one-mot-precision-later-literature.md)
  are complete; publication priority remains unestablished.
- [Rank-one correlation face and conic lower bounds](results/rank-one-correlation-face-conic-lower-bounds.md):
  a correlation-polytope face in the hull with zero lower bounds and unit capacities;
  unconditional lower bounds on exact SOCP and SDP lifts. Independently reviewed.
- [Rank-one hardness with zero lower bounds](results/rank-one-zero-lower-hardness.md):
  a quantitative repair lemma and exact penalty prove strong NP-hardness with only
  unit capacities. Independently reviewed; exact rational checks passed.
- [Rank-one optimization complexity](results/rank-one-row-column-hardness.md):
  strong NP-completeness, rational decision certificates, and an algorithm fixed-parameter
  tractable in the smaller matrix dimension. Independently reviewed.
- [Bilinear relaxation gap and graph density](results/mccormick-gap-degeneracy-bound.md):
  bounds `4√ρ`, `2√Δ`, and a sharper bipartite bound, where `ρ` is maximum induced
  edge density. Independently reviewed. [Graph-by-graph characterization](results/mccormick-hereditary-density-characterization.md)
  follows up with matching order, which is also a consequence of older Schur-multiplier
  theory; it is retained as an elementary proof and explicit MINLP application.
- [Low-interaction-rank flow costs](results/rank-one-low-rank-costs.md):
  polynomial exact optimization for fixed interaction rank and an exact pool
  Lagrangian subproblem oracle for a fixed number of qualities. Independently
  reviewed; earlier low-rank optimization methods are credited.
- [Pooling triviality and the uncapacitated conic hull](results/pooling-triviality-polynomial.md):
  a polynomial sign test for acyclic generalized pooling, a profitable witness
  using at most `K+1` paths for `K` qualities, and an exact polyhedral conic hull.
  Independently reviewed. These are explicit consequences of established
  destination-disaggregation machinery; the capacitated convex hull is different.
- [FBBT limiting-bound hardness](results/fbbt-monotone-system-hardness.md):
  constant-accuracy approximation is PosSLP-hard for a restricted feasible bilinear
  family. Independently reviewed; the [literature assessment](notes/fbbt-novelty.md)
  records the prior mechanisms and remaining priority limits.
- [Doubly exponential primitive-FBBT iteration bound](results/fbbt-doubly-exponential-convergence.md):
  a small circuit creates extremely slow interval propagation. Independently reviewed;
  the statement concerns the specified primitive contractors.
- [Rank-one face stability](results/rank-one-correlation-face-stability.md):
  quantitative face rounding and exponential approximate LP size at entrywise
  error of order `m^-2`. Independently reviewed.
- [Approximate SDP lower bounds](results/rank-one-approximate-sdp-lower-bound.md):
  stretched-exponential SDP order is necessary at the same `m^-2` error scale.
  Independently reviewed; precise constants and metrics are in the theorem.
- [Switching-control conjecture and sharp one-switch theorem](results/cia-uniform-switching-obstruction.md):
  exact counterexamples and a sharp continuous one-switch minimax formula for
  arbitrary numbers of modes. The [three-mode finite-grid result](results/cia-exact-three-mode-one-switch.md)
  gives exact values for every grid size. Independently reviewed; no prior
  resolution found in targeted searches.
- [Exact one-switch minimax on arbitrary finite grids](results/cia-finite-grid-one-switch-minimax.md):
  an explicit formula takes `O(N^2)` rational operations and constructs a worst
  control with two component types and at most three phases. It includes all
  `n>=3` and nonuniform grids; five modes and nine unit cells give `17/5`.
  Independent mathematical and implementation reviews passed.
- [Exact algorithms for a fixed switch budget](results/cia-fixed-switch-budget-algorithm.md):
  one-switch instance optimization takes `O(nN)` arithmetic operations and
  two-switch optimization takes `O(nN^2)`. A subset dynamic program permits
  repeated modes and mode-specific minimum dwell times. Exact implementations
  and public-profile benchmarks are independently checked.
- [Sharp switch-preserving grid transfer](results/cia-sharp-grid-transfer.md):
  uniform-grid restriction costs less than one grid width for each fixed input,
  without increasing switches. The universal constant is sharp; two modes admit
  a sharp half-width schedule transfer even on nonuniform grids. Established
  support-preserving rounding is credited.
- [Five-cell, three-mode, two-switch minimax](results/cia-five-interval-two-switch-minimax.md):
  the exact error is one cell width. Two independent integer enumerations prove
  the upper bound, contradicting the published Corollary 5 lower bound of `8/7`
  cell widths for these parameters.
- [Exact two-switch rounding](results/cia-exact-two-switch-worst-case.md):
  for arbitrary measurable controls and `n>=4` modes, the worst error is
  `T max{1/4, (n-1)^3/[n(3n^2-3n+1)]}`. Four through seven modes give
  `T/4`; uniform relaxed controls are worst-case from eight modes onward.
  Three independent proof reads passed, alongside exact rational checks.
  No prior matching formula found in the qualified literature audit.
- [Exact three-switch rounding](results/cia-exact-three-switch-worst-case.md):
  for `n>=5`, the worst error is `T max{1/5, 1/[n((n/(n-1))^4-1)]}`.
  The all-mode reach proof uses independently audited exact finite and symbolic
  certificates; the heavy-mode and transfer arguments are analytic.
  An [arbitrary-block bound](results/cia-arbitrary-block-one-sided-bound.md)
  supplies a general one-sided rounding guarantee.
- [General switching-control reduction and bounds](results/cia-universal-heavy-mode-rounding.md):
  a reviewed analytic heavy-mode theorem gives the exact identity
  `F_(n,k-1)=max{T/(k+1),G^-_(n,k)}` for `1<=k<n`, with repeated modes
  allowed in the one-sided problem. The [global consequence](results/cia-arbitrary-switch-global-bound.md)
  gives an exact plateau for `k+1<=n<=k(k+1)/2` and the sharp first
  correction in `1/n` for every fixed switching budget and arbitrary profiles.
  Exact finite-mode values outside the proved ranges remain open.
- [Stronger general bounds from the four-block seed](results/cia-seeded-arbitrary-switch-bound.md):
  a maximum/minimum-mass removal argument improves the general one-sided bound
  and proves the additional exact case `F_(16,4)(T)=T/6`. The general higher-budget
  exact formula remains open; an invalid event-relaxation route is documented.
- [Fixed-linking-row common-factor optimization](results/common-factor-fixed-linking-optimization.md):
  exact polynomial-time scalar-product optimization for fixed linking dimension,
  including integer multiplicities. Independently reviewed; close prior mechanisms credited.
- [Reciprocal-anchor hull](results/common-factor-reciprocal-anchor-full-hull.md):
  an explicit hull, exact rational separation, and constructive decomposition
  for arbitrarily many box-bounded leaves. Independently reviewed; classical
  convex-order foundations credited. [Small-block obstructions](results/common-factor-reciprocal-anchor-hulls.md)
  explain why intersecting individual leaf hulls fails. The independently reviewed
  [integer-anchor extension](results/common-factor-integer-anchor-hull.md) has an exact
  rational oracle polynomial in the encoded range, and also permits binary leaves.
- [Observation-sensitive network–simplex hulls](notes/network-simplex-observed-rank-elimination.md)
  (2026-09-07 continuation): a sparse exact extended formulation needs one
  auxiliary coordinate per independent cycle entirely unobserved by an active
  simplex label. If every such unobserved subgraph is a forest, an explicit
  original-variable hull suffices on arbitrary graphs. Independent proof and
  implementation reviews passed. Reduced RLT reconstruction and simplex
  disaggregation are established and credited. The
  [general compressed implementation](code/network_simplex_compressed/README.md)
  combines exact rational model construction with numerical LP solves and
  separately verified rational Farkas cuts. Numerical feasibility is not an
  exact certificate. [Repeated synthetic benchmarks](notes/network-simplex-reopened-computation.md)
  favor compression over full disaggregation and repeated cutting; additional
  observed-coordinate elimination reduces size but did not reduce total runtime
  on those cases.
- [Bounded-rank network–simplex coefficients](results/network-simplex-bounded-rank-hull.md)
  (2026-09-07 continuation): an explicit original-variable separator has
  parameter-dependent preprocessing and input-linear arithmetic work at fixed
  maximum block cycle rank. Its integer flow/product coefficient bound depends
  only on that rank. The sharp rank-three bound is two, witnessed by a
  unit-capacity K4 example with seven observed products. Independent full proof
  review and exact/numerical checks passed. Normal-fan and network-matrix
  foundations are classical; this is not a new general separation-complexity
  result.
- [Exponential coefficients on sparse series–parallel networks](results/network-simplex-series-parallel-coefficient-growth.md)
  (2026-09-07 continuation): a Fibonacci construction forces product-facet
  coefficient ratios exponential in a parameter while using only linearly many
  network arcs, simplex states and observed products. Capacities and total flow
  are one; the graph can be simple, planar, and maximum degree three. Independent
  proof audits and original-state witness checks passed. The number of states
  grows. Conversely, [fixed-state flat chains](results/network-simplex-flat-chain-fixed-states.md)
  admit an explicit original-variable separator and a state-count-only
  coefficient bound even with arbitrarily many cycles. Two explicit simplex
  coordinates need only 41 precomputed circuit tests. This positive theorem and
  the simple-graph negative extension both passed independent review.
- [Sparse network–simplex hull obstruction](results/network-simplex-universality.md):
  arbitrary rational polytopes arise as coordinate sections already with two
  simplex coordinates on four-layer networks. Even unit capacities and unit flow
  permit facet coefficients exceeding every polynomial bound in model size.
  Independently reviewed; this transfers classical transportation universality.
- [Cycle and theta network hulls](results/network-simplex-cycle-theta-hull.md):
  exact original-space hulls and constructive separation for networks assembled
  from those blocks, with arbitrary simplex dimension. Two independent audits
  passed; rational-arithmetic and output-size limits are explicit.
  The reviewed [parallel-path extension](results/network-simplex-parallel-path-hull.md)
  permits arbitrarily many internally disjoint paths per block, with exact
  transportation cuts and polynomial max-flow separation.
- [Coordinate dependence of disjunctive epigraph relaxations](notes/common-factor-p-split-rotation-gap.md):
  a rational two-ball family has unbounded error even with the tightest convex
  hull in its chosen auxiliary function space. A fixed rational orthogonal
  coordinate change makes that construction exact. The entire retained domain
  is transformed, and all proof sections passed independent audit.
  A separate [published P-split theorem counterexample](notes/common-factor-p-split-correction.md)
  and [exact ball-relaxation formula](notes/common-factor-p-split-balls.md) are retained.
- [Scaling disjunctions](results/scaling-disjunctions-hull.md):
  corrected hull results and an exact characterization of universal cost separation.
  Original cost-separation claim was false; counterexamples are retained. Replacements
  independently reviewed; core results overlap known literature.
- [Point-packing relaxations](results/point-packing-relaxations-anstreicher-conjecture-4.md):
  corrected proofs of known formulas. The conjectures were already resolved by
  Khajavirad (2024); this is a rediscovery, not a novelty claim.
- [Generalized-power obstruction](notes/generalized-monomial-gap-obstruction.md):
  two positive one-variable terms already have an unbounded termwise gap ratio.
  This reviewed scope counterexample concerns the original variables; logarithmic
  reparameterization removes this particular obstruction. No novelty claim.

## Repository layout

- `results/`: statements, proofs, scope, sources, and verification status.
- `notes/`: independent audits, research directions, negative findings, and [research log](notes/log.md).
- `code/`: verification scripts; some require the `minlp-notes` conda environment.
- `literature/`: local paper knowledge base; see its `README.md` and `AGENTS.md`.
  This directory is excluded from version control.

Exploratory notes retain failed approaches and open conjectures. Consult each
file's final status; they are not all claims of verified new contributions.

The [exact aggregation hull package](formal/topics/30-infinite-aggregation-hull/README.md)
now verifies the strict and closed hull formulas, finite SDP lifts, and
weak-system hull equality, with a direct two-point proof already in four
variables. The [accuracy package](formal/topics/31-aggregation-accuracy/README.md)
also verifies the explicit Euclidean Hausdorff bounds, optimal inverse-square
rate, exact rational cut constructions and logarithmic coefficient sizes.
These two follow-ups add 25 modules and 325 audited declarations, with
independent reviews and successful targeted builds and kernel replays.
