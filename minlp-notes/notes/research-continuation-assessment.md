# Assessment of the 2026-09-05 research continuation

Research is now closed at the user's request; the [final closeout](research-continuation-closeout.md) supersedes historical running-task labels below. Mathematical review and
publication priority are separate: independent agents have checked the
proofs below, but there has been no external peer review. Bounded searches
do not prove novelty.

## Closing assessment

The final accuracy-bit bilevel theorem is a substantive algorithmic advance
within a clear structural scope: arbitrary many separable dense strictly
convex polynomial costs, but fixed leader and resource dimensions. It
removes positive-coefficient and quantitative-curvature assumptions while
returning exactly feasible rational leaders. Its constituent inverse,
error-bound, and algebraic-optimization methods are carefully attributed.
The two independent final-scope audits include the signed-cost transfer.

The two closing pooling algorithms resolve concrete restrictions left by
the previous work: arbitrary bypass graphs with two source-quality vectors
and supply intervals; and common lower/upper pool throughput bounds for
exactly contracted scalar degree-two networks. Neither claims the general
pooling problem becomes tractable. The existing pooling and resistive/AC
power-flow `∃R` results supply strong arithmetic-complexity classifications
under their exact model semantics, with qualified priority.

The energy maximization theorem and signed-path flow corollary are useful
supporting results. Their classical mechanisms warrant more modest novelty
claims. Earlier integer-precision results remain among the program's most
substantial formulation results. The closure inventory records the limits
of all these assessments and preserves unresolved questions without
claiming that open literature searches establish originality.

## Latest assessment

The most substantial newer advances are the coupled convex-vector formulation
results, the accuracy-bit bilevel algorithms and their coupling barriers,
and the pooling theorem with unrestricted qualities. Their scope now exceeds
several intermediate statements discussed below.

- [Curvature-rank formulation construction](../results/convex-vector-oracle-curvature-rank-precision.md)
  handles arbitrary unconditional oracle error bodies in polynomial rational
  bit time, with additive count `17+2ceil(log2 r)` for one input. The
  [coupled separable extension](../results/convex-separable-vector-oracle-curvature-rank-precision.md)
  uses `21n+2nceil(log2 r)`. This closes the earlier coupled-separable vector
  gap; unrestricted multivariate cross terms remain outside this theorem.
  The [exact degree-32 family](../results/convex-polynomial-box-error-exact-integer-gap.md)
  has `p_conv=n` and `p_bin=ceil(n log2 3)`, establishing unavoidable linear
  loss without a complexity assumption. The classical discrete count law
  and spanner/oracle ingredients are credited; the restricted polynomial
  transfer and uniform whole-formulation comparisons are the contributions
  being assessed for priority.
- [Power-cost bilevel approximation](../results/bilevel-bounded-power-accuracy-bit-algorithm.md)
  has polynomial dependence on accuracy bits and numerical local degree,
  with fixed leader dimension and many diagonal followers. This complements
  dense quadratic coupling hardness even arbitrarily near the identity.
  The contrast is particularly useful: conditioning, exact algebraic
  comparison, rational output length, and accuracy-bit complexity are
  separate issues. The [scope map](bilevel-response-complexity-map.md)
  records the distinction. General positive polynomial marginals and
  resource-coupled variants are current investigations, not yet part of
  this promoted statement.
- [Pooling with fixed contract exceptions](../results/pooling-contract-exceptions-algorithm.md)
  allows arbitrary feeds, outlets, and qualities of arbitrary rank. The
  active ordinary product restricts pool quality to a plane; the remaining
  case uses conservation and fixed output fractions. Degree-two bypasses
  then permit exact standard economic optimization. The matching
  [five-exception degree-three hardness](../results/pooling-five-exception-feasibility-hardness.md)
  uses fixed numerical alphabets. This is now the strongest positive
  contracted-pooling scope in this run. Exact ordinary contracts and
  redundant common pool bounds are substantive restrictions.
- [Global resistance correlation](../results/potential-flow-global-correlation-arc-validation.md)
  preserves an LP description for exact cactus arc-capacity feasibility,
  directly extending an existing cycle lemma. Yet
  [total-flow maximization](../results/potential-flow-global-correlation-total-flow-hardness.md)
  and [minimum source-to-sink potential](../results/potential-flow-global-correlation-energy-design-hardness.md)
  are strongly hard under bounded data and a constant accuracy gap.
  The [polynomial-law design extension](../results/potential-flow-correlated-polynomial-cycle-design.md)
  gives a broad complementary algorithm when cycle parameter sets are
  independent. These are precise structural and arithmetic results;
  inherited MaxCut, energy, and circuit mechanisms are not claimed new.

All listed milestones have two independent proof audits and qualified source
assessments. None has external peer review, and absent search matches do not
establish publication priority. The long record below retains earlier
comparisons and the wider results that motivated the current work.

## Earlier comparisons and wider scope

1. **Exact pooling algorithms and a complementary hardness boundary.** The
   fixed-core block theorem is a broadly useful constructive result. Its
   general theorem permits many variables and inequalities while keeping
   three structural dimensions fixed. Two pooling corollaries answer the
   fixed-input and fixed-quality portions of an explicit fixed-pool question
   in the final Haugland (2016) paper. The proof uses established real-algebraic
   and support-function tools; its value is the combined structure and the
   tractable pooling classes. The algorithm can have a large polynomial
   exponent and is not claimed practical or fixed-parameter tractable.
   Two independent proof audits passed. A separate reduction now proves
   NP-hardness with just two pools and two outputs when qualities grow,
   completing the fixed-terminal direction negatively. Two independent
   audits passed there too. Bounded later-literature searches found no
   matching results; publication priority remains qualified. A further
   one-pool, one-quality bypass construction now gives NP-completeness with
   upper bounds only, input out-degree two, output in-degree three, and
   upper flow bounds at most four. Two audits passed, including its explicit
   exact penalty. Related hardness was
   already asserted in prior work, so its explicit reduction and precise
   restrictions carry the claim. The structured bypass algorithm using
   vertex integrity and affine quality rank also passed two audits and
   subsumes both original pooling corollaries.
   The latest reduction is substantially stronger: one pool with two
   actual feeds and two outlets remains strongly NP-complete using fixed
   finite physical-data alphabets and zero lower flows. Binary averaging
   circuits encode large rational coefficients through network topology;
   a bounded contract-completion objective replaces the earlier large
   penalty. Two independent full audits and original-network checks passed.
   Input out-degree two and output in-degree three are retained. External
   input count grows, so the positive fixed-input theorem is unaffected.
   This strengthens the numerical restrictions of the earlier pooling hardness results.
   Exact threshold hardness does not by itself supply an approximation
   gap, numerical robustness, or a no-FPTAS theorem.
   The new complementary degree-two bypass theorem gives polynomial
   feasibility, algebraic reconstruction, and exact optimization with a
   fixed number of retained objective arc coordinates. Two full audits
   passed. Combined with the same physical hardness circuit retaining its
   exact contracts, this gives a sharp feasibility boundary at output
   total degree two versus three when input total degree is at most two.
   The positive theorem allows arbitrarily many qualities; the hard side
   uses a fixed numerical alphabet. Dense bypass profit remains outside
   the endpoint projection theorem. This is a useful structural completion
   of the one-pool direction, with the exact-contract qualification essential.
   A reviewed supporting obstruction,
   [Klee–Minty path plus one aggregate slab](klee-minty-rank-one-slab-hardness.md),
   shows why path-local constraints cannot simply replace independent
   blocks in the positive fixed-core theorem. A rank-one concave quadratic
   constraint suffices for ordinary NP-completeness in that class, even
   with fixed local path coefficients. Broad rank-one quadratic hardness
   and exponential shadows are prior results; the explicit identity and
   restricted structure are retained without a broad novelty claim.
2. **Integer precision for quadratic and smooth systems.** This direction
   now offers the broadest theoretical characterization in the run. The
   quadratic noncommutative-rank law determines the exact leading
   integer-dimension coefficient, allows
   arbitrary convex lifts and unbounded integers, and supplies a matching
   compact MILP. It unifies the graph and scalar laws and disproves maximum
   scalar-pencil rank as a proposed answer through the cross-product example.
   Two full proof audits and a separate source audit passed.
   The algebraic rank machinery is established; the
   connection to formulation precision is the apparent new contribution.
   A separately reviewed rational construction now gives deterministic
   polynomial bit complexity and uniform polynomial input-size overhead.
   A finite maximum-determinant covariance characterization handles arbitrary
   unequal quadratic accuracies within a dimension-only additive term;
   two audits passed. Its deterministic polynomial bit-time optimizer also
   passed two full audits, including a rational Jacobi implementation and
   all rounding steps. It constructs a rational MILP with only
   `O(n log(n+1))` more binaries than the minimum integer dimension among
   arbitrary convex lifts. This remains one of the broadest
   algorithmic formulation results in the run. It does not promise
   a practically competitive runtime. A matching complexity barrier in the
   dimension exponent passed two audits: additive or multiplicative
   `O(n^(1-delta))` guarantees are impossible unless `P=NP`, even under a
   positive-optimum promise. Correlated ellipsoidal output budgets and
   arbitrary symmetric convex output-error bodies have reviewed extensions.
   The latter requires a rational strong separation oracle and known inner
   and outer radii; output dimension does not enter the additive count.
   Del Pia's July 2026 rational Jacobi theorem is now explicitly credited
   as a directly applicable established numerical ingredient.
   Two further audits passed the input-rank refinement: the overhead is
   `O(r log(r+1))`, where `r` is the exact rank of the stacked Hessians.
   Exact affine quotienting and rational zonotope rounding remove input
   directions used only by affine terms. The ordinary input/output sizes
   still enter the running time and continuous formulation size.
   For nonnegative diagonal Hessians in the original box coordinates,
   a separate trace-allocation theorem improves the overhead to `5r+1`.
   Both mathematical audits and a source assessment are complete. The
   trace lower bound and shared scalar grids avoid the dimension-log
   loss in the general Frobenius-covariance benchmark; they do not improve
   that earlier benchmark beyond its documented impossibility example.
   A further positive separable polynomial theorem has now passed two
   audits and a dedicated source comparison. The finite overhead is
   `2 sum_i log2(D_i)+4r+1`; dense degrees may grow. A power transformation
   is used only for the lower-bound supports, while the rational upper
   formulation uses original-coordinate Taylor bands and shared prefix
   powers. This extends near-minimal integer construction beyond quadratic
   systems with `O(r)` overhead at any fixed degree. Established radix
   polynomial approximation methods are credited explicitly.
   The latest twice-reviewed results improve this further: pure powers
   admit `6.5r+1` overhead independent of degree, and positive mixtures
   admit `O(r+sum_i log log(D_i+2))` overhead. Both are compact rational
   constructions polynomial in dense degrees and support unconditional
   output-error bodies. The pure-power construction combines established
   positive resolvent approximation with exact interpolation using shared
   binary digits. The mixture lower bound chooses a coordinate transform
   through a supporting scalarization of the allocation optimum.
   A separate twice-reviewed example shows that coefficient-sum allocation
   itself misses order `log log D` in one dimension. The new curvature
   measure now supplies the missing information for scalar functions.
   Certified integration and indexed quantiles give a compact scalar
   construction within seven binaries of the true optimum. Ordered
   midpoint-incompatible sets, Jensen superadditivity, and an integer-grid
   packing argument extend this to dense positive polynomial scalar sums
   with `12r` overhead, or independent outputs with `9r`. Both final scopes
   passed two audits. The finite comparison extends further to arbitrary
   continuous convex summands. The subsequent curvature-rank theorems listed
   above resolve the coupled-separable vector scope. A separate growing-output
   example remains useful because individual scalarizations and midpoint
   tests alone do not supply that stronger comparison.
   The latest circuit-based construction strengthens the pure-power
   statement to every binary-encoded rational exponent greater than one,
   with `7r+1` overhead and size polynomial in the exponent bit lengths.
   Sparse positive mixtures retain the log-log count with the same encoding
   improvement. Both final scopes passed two independent audits. The
   compiler and computed-output interpolation have direct predecessors;
   the whole-formulation guarantee is the contribution under investigation.
   PSD blocks and bounded-width independent integer features also have
   sharper reviewed bounds, with forest Laplacians as a concrete example.
   A separate twice-reviewed theorem gives an exponential rational
   encoding separation: the fixed-error root graph `x^(1/2^B)` requires
   `Theta(2^B)` MILP bits but only polynomial-size rational MISOCP encoding,
   with four binaries sufficient in both. It demonstrates a limitation of
   integer-count guarantees when exponents approach zero. Classical conic
   numerical-complexity examples and power lifts are credited. The conic
   construction uses an exact optimality face and has no numerical-stability
   claim; its value is the precise encoding comparison.
   These guarantees bound formulation construction and integer count.
   Optimization of the resulting MILP remains a separate computational
   task; small nonlinear rank alone does not make arbitrary coupled
   feasible sets tractable.

   The smooth-map extension passed two independent audits. A classical
   oscillatory-integral bound supplies the missing local volume argument,
   with noncommutative matrix evaluations handling simultaneous outputs.
   Full local rank determines the exact coefficient; fixed-degree polynomial
   maps then have compact MILPs. General smooth maps have a local/global
   rank sandwich, not an unrestricted equality claim. A reviewed scalar
   constant-Hessian-rank theorem gives an exact coefficient even when the
   null spaces rotate. A reviewed perspective transfer covers
   quadratic-over-linear systems without extra binaries.
3. **Exact structured bilevel optimization.** A new direction now has two
   full audits, a separate growing-degree and exact-output audit, and a
   source comparison. Fixed leader dimension, resource-row counts, and
   aggregate-output count suffice for polynomial optimistic bilevel
   optimization with many follower variables. Positive diagonal local
   quadratic costs coexist with a nonconvex aggregate follower cost.
   Compressed KKT responses are compared globally through a second
   quantified copy; stationarity is not treated as sufficient by itself.
   Fixed constraint normals give response-graph closure and attainment,
   even with polynomial moving bounds. Exact optimizer coordinates share
   one polynomial-size algebraic representation. Dense or unary-encoded
   polynomial degrees may grow. This is a promising broadly applicable
   positive result, with classical multiplier compression and real-algebraic
   methods credited. A direct cubic-response Square-Root-Sum example
   explains why arbitrary strictly convex local costs are outside the
   theorem; nonpositive local curvature has stronger Boolean obstructions.
   The extension to fixed-dimensional positive-definite quadratic local
   blocks also passed two full audits. Local inequality counts may grow;
   independent active-normal lists and joint sign conditions keep the
   response description polynomial without multiplying all block choices.
   The final infimum-and-attainment theorem also passed two audits with
   polynomially varying local and shared constraint normals. It covers
   optimistic selection and pessimistic constraints imposed on every
   global follower response, with the worst upper objective. Explicit
   nonattainment examples prevent an unjustified universal optimizer claim.
   The complementary scalar-leader hardness theorem now passed two full
   final-scope audits: no upper constraints, an affine upper objective,
   a fixed unit-box follower domain, and a fixed positive-definite follower
   Hessian suffice for NP-completeness. The follower optimum is unique, and
   the lower objective has a jointly convex sum-of-squares representation.
   The precise box/SPD/no-upper restriction is the candidate contribution;
   scalar-leader hardness, Boolean response paths, and gap amplification
   have established predecessors. A stronger pair of results has now
   resolved the conditioning question: exact threshold remains NP-complete
   with follower Hessian condition number below two and all coefficients
   bounded in magnitude by two, while fixed leader dimension admits an
   additive algorithm polynomial in input bits, condition number, and
   inverse normalized error. Both final statements passed two audits.
   The negative gap is exponentially small, so it obstructs dependence on
   accuracy bits rather than contradicting the inverse-error algorithm.
   Diagonal scaling and weak-feedback convex energies are prior methods;
   the explicit relative-coordinate estimate and restricted hardness
   reduction carry the candidate contribution. This paired boundary is
   stronger than the earlier ill-conditioned construction.
4. **Potential optimization with bounded block cycle rank.** The cactus
   algorithm now extends to interacting cycles and arbitrarily many blocks.
   A perturbed electrical-adjoint argument reduces each active block to
   polynomially many faces of bounded dimension. Two proof audits and a
   separate source comparison passed. It returns a feasible rational
   nomination and certified additive value interval in polynomial bit time,
   with an exponent depending on the block cycle rank. The exact
   Square-Root-Sum classification explains why exact pressure comparisons
   need a different claim. Joint resistance uncertainty and exact arc-flow
   capacity validation also passed two proof audits and are promoted. The
   latter gives exact robust feasibility when flow capacities are the only
   additional operating constraints; it does not optimize over a subset of
   scenarios already constrained by capacities or potential limits. A
   dedicated source audit confirms that per-arc validation and some exact
   cycle cases are established; the candidate novelty is the broader
   structural joint-uncertainty guarantee. Dense piecewise-polynomial laws
   and affine coefficient uncertainty passed two proof audits and are
   promoted. Positive rational approximation also gives an independently
   verified additive algorithm for fixed fractional powers, while exact
   capacity comparison retains the radical-sum barrier. Discrete two-point
   resistance uncertainty creates a different boundary: high-precision
   pressure optimization is NP-hard already at block cycle rank two,
   whereas the corresponding continuous interval problem is polynomial.
   Exact arc validation under discrete resistance uncertainty has a sharper
   reviewed boundary: polynomial at block cycle rank at most two and
   coNP-complete already at rank three. The positive series-parallel
   monotonicity mechanism has classical circuit antecedents; priority
   against older nonlinear tolerance analysis is still unresolved.
5. **All-degree-two pooling hardness.** The unit-capacity, constant-data
   reduction closes a sharply stated structural boundary. Its conversion of
   arbitrary continuous flows to integral pure modes and its positive-purity
   robustness make it stronger than a fragile feasibility gadget. Two proof
   reviews and extensive independent checks passed. This is a crisp
   complexity result, although it does not itself supply a solution method.
6. **Additional integer-precision results.** The bilinear graph fractional-cover
   law and the quadratic rank/inertia laws give formulation-independent
   benchmarks, including unrestricted integer variables and arbitrary convex
   lifts. Matching compact formulations give the lower bounds practical
   meaning for discretization design. Prior midpoint arguments, approximation
   geometry, and signed-square constructions are credited. The graph's finite
   unequal-accuracy LP guarantee is stronger than a uniform asymptotic alone.
7. **Spatial B&B with stronger node relaxations.** SDP, RLT, and higher-order
   SOS extensions show that strengthening a node oracle does not automatically
   cure poor spatial certificates. Unique-optimum and auxiliary-variable
   variants make the model less dependent on symmetry or a particular syntax.
   These are unconditional but model-specific lower bounds on simple problems;
   a direct valid coupled inequality solves the examples. They should not be
   advertised as hardness of the optimization problem itself. A sparse-XOR
   construction now removes the quadratic-cut weakness and survives
   branching on arbitrary bounded-degree monomial lifts. Both new statements
   passed two audits. Their exact node hull is the quadratic hull of the box,
   not the feasible lifted graph; general linear aggregation branches remain
   outside the claim.

The Geoffrion P-prime counterexample and reviewed facial-quality integrality theorem
are useful supporting results with more modest impact. The former does not
refute the informal computational Property P conjecture. That distinction
was checked against the primary paper and retained explicitly.

## Work still being developed

- An absolute-sum output-error norm and broader error-body models are being
  investigated beyond the reviewed correlated ellipsoidal budgets.
- Bypass graphs with maximum degree two remain a possible tractable
  boundary; the verified hardness has output degree three.
- The spatial affine-branching obstruction is documented and reviewed. It
  explains failure of the current proof, not an algorithm defeating the
  fixed-gap lower bound.
- Cactus uncertainty sets may be replaced exactly by their interval hulls
  for pressure extrema. A rank-two counterexample and a possible exact
  graph characterization passed proof review, but a directly relevant
  older nonlinear-circuit paper remains unavailable, leaving broad novelty
  unresolved. A discrete arc-capacity hardness extension is under two audits.

Each result and investigation file records its current proof and source
status; this note ranks directions rather than replacing those details.
