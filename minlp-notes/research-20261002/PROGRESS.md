# Research record

Date: 2026-10-02. The user requested completion of the current ideas and
extensions followed by a stop. Those lines are documented below and in the
[closeout](CLOSEOUT.md). The continuation is paused; no new directions were
started after that instruction.

## Decisions and current contribution assessment

The main line is certified sparse global optimization under quantitative
growth assumptions. It was selected after inspecting recent intersection-cut
work and the earlier decomposition results. The initial tree-localization
question exposed a real obstruction, but the more consequential opportunity
is a positive algorithm that avoids that obstruction.

The earlier [independent significance assessment](reviews/program-significance.md)
ranked the occurrence-dependent rational box-QP algorithm first and the
continuous-control nonlinear-dynamics bit theorem second. It also identified
simpler Bellman-DP baselines that limit finite-control variants.
Two subsequent reviewed results substantially change the program:
min-marginal filtering removes occurrence and the accuracy-dependent
exponent from the mixed-box QP algorithm, while a separate theorem gives
exact QP over bounded rational polytopes parameterized by negative inertia
and global conditioning. The
[fresh significance assessment](reviews/current-significance.md) ranks
the filtered sparse-grid result first, while identifying natural instance
families with defensible conditioning as a remaining need. The reviewed
perturbation bounds address part of that question for sampled objectives.
Neither mathematical review nor the current source search establishes
publication priority or competitive solver performance.

1. **Shared geometric grids:** [theorem](geometric-dp/theorem.md),
   [extensions](geometric-dp/extensions.md). A global lower bound follows from
   independent unbiased rounding and unary corrections for interpolation
   error. Repeated exact minimization of these corrected tables contracts
   squared distance under global quadratic growth. The method works on
   arbitrary supplied tree decompositions and with boundary minima. It
   handles compressed integer domains and eventually gives exact integer
   certificates. The approximate algorithm needs no growth constant.
2. **Arithmetic and model extensions:** certified rational approximate tables
   preserve the rate; sparse rational polynomials of bounded numerical degree
   have an explicit bit bound. Fully enumerated finite-state variables need
   no curvature or uniqueness assumptions of their own. Private recourse
   inherits upper curvature when its feasible set is independent of the
   gridded variables and a certified value/witness oracle is available.
3. **A real obstruction:** [counterexample](tree-localization/counterexample.md)
   disproves unrestricted localization for the earlier copy-based
   certificates, using finite dyadic partitions, standard chord relaxations,
   fixed conditioning, and exact slopes. It does not disprove localization
   restricted to a particular algorithm's reachable partitions. The older
   conjecture note has a scoped update.
4. **Rebuilt continuous certificates:** [theorem](regridded-certificates/note.md)
   gives aggregate distance contraction without per-bag localization. It
   recovers the earlier smaller final certificate size on general trees and
   permits boundary minima. The final cell count is linear in accuracy bits;
   total local convex-oracle calls are cubic in accuracy bits. The
   [inexact-oracle extension](regridded-certificates/inexact-oracles.md) retains
   the rate with certified local bounds and feasible points. Both versions
   have passed independent adversarial review. Their oracle costs are distinct
   from the coordinate-grid bit-complexity result.
5. **Supporting result:** [screening and percolation](new-direction/screening-percolation.md)
   gives expected polynomial exact indicator optimization in a regime with
   few potentially active variables. It is deliberately classified as modest:
   standard screening and branching-process ideas provide a restricted
   tractable regime, and do not solve the harder active-mediator problem.
6. **Exact mixed-integer quadratic optimization:** the
   [rational box-QP corollary](geometric-dp/exact-box-qp.md) uses standard
   rational-height bounds and reconstruction to recover the exact optimizer
   and value. At fixed width its bit complexity is polynomial in input size
   and the numerical curvature/growth ratio. It needs neither the growth
   constant nor integer-domain enumeration. Every unique quadratic optimum
   on a bounded mixed box has some positive growth constant, so termination
   extends beyond the polynomially conditioned subclass. Certificate
   validity does not depend on the growth promise.
7. **An exact-output boundary:** a reviewed
   [quartic path family](geometric-dp/algebraic-output.md) has fixed curvature,
   growth, and width, yet an optimizer coordinate needs exponentially many
   terms in its expanded minimal polynomial. The limitation concerns that
   output format; compact radical circuits and the exact optimum value are
   short in this example.
8. **Nonunique optima:** the reviewed
   [coordinate-anchor theorem](new-direction/projection-anchors.md) replaces
   pointwise growth by growth toward the optimal set. Work depends on
   coordinate-projection covering numbers; finite projections retain
   polylogarithmic accuracy dependence. This can include exponentially many
   optimal points. A diagonal quadratic shows that arbitrary optimal sets
   require inverse-square-root accuracy dependence for this particular
   correction-based certificate. The integer stopping rule remains exact
   with multiple optima. The reviewed
   [exact finite-optimum QP corollary](geometric-dp/exact-nonunique-box-qp.md)
   gives polynomial bit work at fixed width in input length, optimal
   coordinate-value count, and conditioning.
9. **Affine coupling constraints:** the reviewed
   [repair theorem](new-direction/affine-repair-exploration.md) combines a
   supplied box-preserving affine repair with multiplier-corrected separator
   slopes. Stable scalar linear dynamics have horizon-independent repair
   constants and permit [private finite controls](new-direction/mixed-stable-audit.md).
   The [raw-slope obstruction](new-direction/constraint-obstruction.md)
   proves why an objective-gradient slope plus a Hoffman repair estimate
   alone does not suffice. The positive result counts convex-oracle calls;
   general repair computation and bit costs remain explicit limitations.
10. **Fixed-parameter bit complexity:** the reviewed
    [regridded QP specialization](geometric-dp/regridded-qp-bit.md) uses affine
    Taylor lower models and exact corner solves. It gives
    `f(p,k,kappa) poly(I)` exact bit complexity for continuous rational box
    QP, where `kappa` uses the supplied full bag Hessian bound. The input
    exponent is absolute. Its polynomial-objective extension gives certified
    approximation with the same parameter structure and charged degree.
    This requires stronger curvature and occurrence assumptions than the
    coordinate-grid theorem; it is not FPT in treewidth alone.
11. **Stable nonlinear dynamics:** the reviewed
    [continuous-control theorem](new-direction/nonlinear-dynamics.md) uses
    affine outer strips for each dynamics graph, forward repair, and
    backward adjoints. A [bit theorem](new-direction/nonlinear-dynamics-bit.md)
    for fixed-degree rational polynomial data uses exact small LPs,
    rounded centers, and contraction-aware enclosures. It returns a compressed
    feasible trajectory and rational global bounds. Full expanded state
    fractions can have exponential length; that output is not promised.
12. **Feedback vertex set QP:** the reviewed
    [core-and-forest theorem](new-direction/fan-exploration.md) gives exact
    `f(r,kappa) poly(I)` bit complexity, with an absolute exponent, when
    deleting a supplied core of `r` coordinates leaves a forest. Growth
    and uniqueness are needed only for the optimal core; residual optima
    may form a continuum. A finite-face argument proves that a unique
    optimal core always has some positive growth constant. The algorithm
    uses the existing exact rational forest oracle and classical
    quadratic-growth box packing. The
    [focused audit](prior-art/regridded-qp-prior.md) records prior
    sign-restricted fixed-core tractability and prevents a broader novelty
    claim. A separate [fan obstruction](new-direction/weighted-drift-exploration.md)
    shows that weighted reconstruction alone cannot repair the present
    closed-cell certificate; boundary-touching incidences are essential
    to that example. Arbitrary occurrence-free bounded-treewidth FPT
    was subsequently addressed for product boxes by item 13 below; the
    closed-cell obstruction itself remains valid.
13. **Occurrence-free mixed-box QP:** the reviewed
    [filtered coordinate-grid theorem](new-direction/pruned-coordinate-grid.md)
    gives exact `f(p,kappa) poly(I)` bit complexity, with
    `kappa=max(1,L/g)` and an absolute input exponent. Exact min-marginals
    safely remove coordinate intervals, and global growth bounds the
    surviving hulls. Subsequent coordinate grids have
    `O(sqrt(kappa) log(n+2))` states independently of accuracy. The
    algorithm needs no occurrence bound or supplied growth constant.
    Earlier unsuccessful conditioning trials are capped before table
    allocation, preserving the FPT bound. Pruning history certifies the
    original domain. Two independent reviews and actual exact DP traces
    passed. The [prior-art audit](prior-art/minmarginal-prior.md) credits
    min-marginals, filtering, and adaptive grids; the
    [hardness review](reviews/pruned-grid-hardness-sanity.md) shows why the
    known width-two reduction does not preserve useful global growth.
14. **Few negative directions:** the reviewed
    [negative-inertia QP theorem](new-direction/negative-inertia-qp.md)
    gives exact `f(k,max(1,nu/g)) poly(I)` bit complexity over any bounded
    rational polytope, where `k` is negative inertia and
    `nu=max(0,-lambda_min(A))`. The reviewed strengthening from the original
    full-norm bound computes a rational negative-curvature bound within a
    factor two. Positive curvature affects precision, not this parameter.
    Fenchel square completion creates a small auxiliary problem
    with fixed-domain convex recourse and an explicit growth constant.
    An [independent slab derivation](new-direction/convex-modulator-qp.md)
    gives the same capability. The
    [rational normalization](new-direction/spectral-normalization.md)
    handles singular Hessians and preserves an exact PSD decomposition.
    Projected growth allows continuum recourse optima when their images
    coincide. The [source audit](prior-art/convex-recourse-prior.md)
    compares Del Pia's 2026 Turing approximation and older spectral
    branch-and-bound methods; those mechanisms are not claimed as new.
15. **Additional limits and quotient growth:** the reviewed
    [mode-wise growth barrier](new-direction/modewise-growth-barrier.md)
    encodes SUBSET SUM despite uniformly conditioned convex continuous
    slices, demonstrating why growth within each discrete mode cannot
    replace global growth. A reviewed
    [gauge-face construction](new-direction/gauge-face-exploration.md)
    handles one translation orbit of continuous optima. Its nonconvex
    application is to higher-degree objectives: a nontrivial positive
    translation orbit in a full box forces a quadratic Hessian to be PSD.
    A separate reviewed [separator limitation](new-direction/translation-separator-growth.md)
    bounds dimension by `max(4p,8p^2 L/g)` for a positive-length optimal
    translation orbit. It explains why fixed width and conditioning do not
    permit that symmetry regime in arbitrarily large dimension.
16. **Tied modes without a metric:** the reviewed
    [finite-mode corollary](new-direction/pruned-grid-finite-modes.md)
    needs projected growth only in gridded coordinates. Exact finite-state
    DP handles any tied optimal modes and their local feasibility rules.
    Rational heights are bounded uniformly from explicit local tables,
    without enumerating complete mode assignments. Nonpositive-diagonal
    quadratic coordinates can be restricted to endpoint modes by classical
    separate concavity. Exact recovery uses the saved incumbent, whose
    value may be smaller than that of the current grid center.
17. **Structured nonlinear and integer recourse:** the reviewed
    [approximate recourse theorem](new-direction/approximate-convex-recourse.md)
    retains the small auxiliary search with certified inner intervals and
    feasible witnesses. Separable convex quartics minus a supplied low-rank
    quadratic have a concrete polynomial-bit oracle: derivative bisection
    for continuous coordinates and discrete-difference bisection for integer
    coordinates. It permits arbitrary integer dimension and huge intervals.
    Pure integer objectives are recovered exactly once the certified gap is
    below their rational objective spacing. Continuous quartics receive
    approximation, not a rational exact-output promise. The
    [comparison](prior-art/separable-lowrank-minlp-prior.md) distinguishes
    rank-one binary min-cut and other exact low-rank baselines.
18. **Quantitative growth from linear noise:** the reviewed
    [perturbation theorem](new-direction/smoothed-linear-growth.md)
    proves high-probability global quadratic growth for any continuous
    objective on a compact set using scalar monotone optimizer responses
    and a weak-type maximal-slope bound. For box QP, mixed box QP, and
    continuous polytope QP, finitely many affine response candidates give
    a polynomial-bit rational sampling scheme. Exponentially many faces
    are counted but never enumerated. This gives high-probability
    polynomial exact work at fixed width or fixed negative inertia under
    explicit polynomial numerical-scale bounds. It is not an expected
    runtime theorem and concerns the perturbed objective. The
    [source audit](prior-art/smoothed-linear-growth-prior.md) compares
    qualitative generic growth and discrete isolation; priority remains
    unestablished. The [significance review](reviews/smoothed-growth-significance.md)
    identifies classical almost-everywhere growth arguments and narrows
    the contribution to explicit conditioning and finite-bit consequences.
    A reviewed [summed-response refinement](new-direction/summed-response-growth.md)
    improves the width dependence to
    `g >= rho sigma / [24 (sum_i w_i) (2+log(4n/rho))]`
    for uniform rational-grid noise. It requires at most one extra sampling
    bit per coordinate over the earlier sufficient grid size. Its linear
    example shows the necessary `1/n` scale and a logarithmic loss in
    this particular summed-slope certificate.
19. **Mixed polytopes with few negative directions:** the reviewed
    [MIQP extension](new-direction/negative-inertia-miqp.md) gives exact
    `f(m,k,max(1,nu/g)) poly(I)` work over a bounded rational mixed
    polytope with `m` integer coordinates. Del Pia's existing exact
    fixed-parameter convex MIQP algorithm supplies the inner oracle.
    The Fenchel lift retains integrality throughout; its continuous
    relaxation need not give the correct global value. Rational heights
    are bounded uniformly over integer slices without enumeration.
    No growth constant is supplied. A projected version permits ties
    when all optimal projections coincide.
20. **Arbitrary optimal sets with a supplied growth bound:** the reviewed
    [proximal grid](new-direction/proximal-growth-grid.md) and
    [exact recovery](new-direction/proximal-exact-recovery.md) give
    `f(p,kappa) poly(I)` exact mixed-box QP without uniqueness or a
    bound on optimal projections. A proximal term controls movement
    relative to a nearest optimum; fresh restricted boxes permit that
    optimum to change. Nearby-point recovery selects a box face and
    solves linear stationarity equations. A rational vertex-slack gap
    proves that extra selected bounds can be imposed simultaneously.
    This version requires a supplied valid conditioning bound. Its
    interval is promise-dependent, and an explicit false-bound example
    shows why final feasibility and value checks cannot validate it.
21. **Sharp random-tilt growth:** the reviewed
    [proximal tail](new-direction/proximal-growth-tail.md) removes the
    summed-response logarithm and proves
    `Pr(g* < eps) <= 2 eps sum_i phi_i w_i` for any continuous objective
    on a compact set. The constant two is sharp. A proximal-map area
    argument controls the bad-growth event directly; a separate expanding
    map proves the uniform-noise case. For QP, original and shifted
    stationary-face candidates bound every coefficient section of the bad
    event. This yields a fixed rational sampling law with a tail bound
    uniform in the growth threshold, including a controlled tie atom.
    The [prior audit](prior-art/proximal-growth-tail-prior.md) compares
    discrete isolation and generic growth; priority is unestablished.
22. **Expected exact QP work:** the reviewed
    [expected-work theorem](new-direction/expected-smoothed-qp.md) covers
    bounded rational polytopes with at most two negative Hessian eigenvalues.
    On a specified polynomial-bit linear-noise grid, it returns an exact
    optimizer and value on every sample and has expected bit work
    `poly(I) (1 + nu sum_i w_i / sigma)`. The adaptive solver is
    interleaved with exact active-face enumeration on the same sampled
    input. The retained-cell exponent is `k/2`; its capped moment is
    polynomial for `k <= 2`. The sampling size controls atoms against
    the fallback's combinatorial count, avoiding a precision circularity.
    This does not prove expected polynomial work for more negative
    directions, the uncapped solver, or the unperturbed objective.
23. **Expected cells without growth:** the reviewed
    [direct counting theorem](new-direction/smoothed-semiconcave-cells.md)
    uses necessary neighboring-grid comparisons to bound the probability
    that a point is near-optimal. Under independent linear noise, the
    resulting expected number of surviving cells is uniform across scales
    in every fixed dimension. A concrete nested cell algorithm therefore
    has expected logarithmic accuracy dependence in the exact point-oracle
    model. A convex-QP recourse application uses noise aligned with the
    low-rank factor, which is correlated in original coordinates. Its
    rational sampling grid depends on the requested accuracy; fixed-law
    exact optimization does not follow from this argument.
24. **Arbitrary optimal sets on mixed polytopes:** the reviewed
    [polytope recovery theorem](new-direction/proximal-polytope-recovery.md)
    gives exact `f(m,k,max(1,nu/g0)) poly(I)` work with a supplied valid
    full-distance set-growth bound `g0`. Integer agreement, small
    inequality slacks, a bounded stationary polytope, and a rational
    vertex gap identify a face containing an optimum. Every feasible
    solution of its linear stationarity system has the optimal value.
    Lower-dimensional polytopes, redundant rows, and disconnected flat
    optimal sets are included. The final checks still depend on the
    validity of the supplied growth promise.
    Luo–Sturm's primary Theorem 3.3, now retrieved and checked, already
    establishes qualitative full-set growth on bounded continuous
    polyhedra; finitely many integer slices extend that existence statement
    to the mixed case. This classical fact supplies no useful quantitative
    conditioning bound by itself.
25. **Exact cell closure under aligned noise:** the reviewed
    [algebraic closure theorem](new-direction/smoothed-exact-cell-closure.md)
    gives expected `f(k,1+nu diam(X)/sigma) poly(I)` exact bit work
    for bounded continuous rational QP with arbitrary negative inertia.
    A convex-QP optimizer and independent active constraints yield a
    quadratic formula valid on a rational critical region. Cells contained
    in one such region are solved exactly. Every unresolved near-optimal
    cell forces the factor noise into a thin neighborhood of a fixed
    hyperplane. Base-data bounds select the terminal stage and rational
    sampling grid before the draw; an exact fallback includes all remaining
    atoms and degeneracies. There is no growth assumption or precision
    circularity. The perturbation is aligned with the factor, generally
    correlated in original coordinates. The two-direction growth-moment
    theorem remains useful for its sharper numerical dependence; item 27
    supplies a different independent-coordinate extension to every rank.
26. **Expected exact nonlinear integer optimization:** the reviewed
    [separable low-rank theorem](new-direction/smoothed-integer-low-rank.md)
    handles any number of integer coordinates on binary-encoded product
    intervals. The objective is a sum of convex rational quartics minus
    a supplied low-rank concave quadratic. Independent rational noise is
    applied in its factor coordinates. Monotone discrete differences give
    exact recourse without enumerating labels. One common noise denominator
    makes the original objective lattice spacing proportional to `1/M`;
    the certified final gap is proportional to `1/M^2`. A single base-data
    choice of `M` therefore gives exactness on every draw and the finite-grid
    expected cell bound. No growth, uniqueness, fallback, or resampling is
    required. The numerical projected-range/noise factor remains explicit.
    Binary and explicitly listed domains have deterministic fixed-rank
    baselines; long encoded intervals are the relevant additional regime.
27. **Exact QP under independent ambient noise:** the reviewed
    [ambient extension](new-direction/smoothed-ambient-cell-closure.md)
    permits any negative inertia and independently perturbs every original
    linear coefficient. A complementary-minor cube-volume estimate handles
    the dependent projected coefficients without assuming conditional
    independence. Local events have uniformly bounded scalar section
    complexity, allowing transfer to one fixed polynomial-bit noise law.
    Unresolved cells force proximity to fixed ambient hyperplanes; their
    probability pays for an exact fallback on the same draw. Every draw
    returns an exact optimum. Expected work is polynomial for each fixed
    inertia when the displayed numerical factors are polynomially bounded;
    its `n^{O(k)}` dependence is not the aligned model's FPT guarantee.
    Full and interface reviews found no substantive gap, and root
    independently checked the volume, section-count, normal-pullback,
    normalization, and base-only arithmetic arguments. The
    [new prior audit](prior-art/smoothed-cell-closure-prior.md) identifies
    Ding's classical parametric global-QP reduction as a close antecedent,
    narrowing the proposed addition to the smoothed exact-work analysis.
28. **Independent Gaussian-like noise with an FPT bound:** the reviewed
    [Gaussian theorem](new-direction/smoothed-gaussian-cell-closure.md)
    gives expected `f(k,nu diam(X)/sigma) poly(I)` exact work for continuous
    rational polytope QP. Gaussian projection makes the factor vector
    independent of the residual; a density-weighted lattice sum eliminates
    the auxiliary support width and ambient dimension powers. A bounded
    rejection sampler defines one independent finite rational law with
    controlled scalar distribution error. A base-only support/precision
    loop and event-section bounds transfer both expected search work and
    the fallback budget. Every finite draw is solved exactly. The theorem
    does not claim a Turing-model exact algorithm on real Gaussian input.
29. **General constrained MIQP under uniform ambient noise:** the reviewed
    [mixed closure theorem](new-direction/smoothed-miqp-cell-closure.md)
    gives expected `f(m) C^k (1+H_amb) poly(I)` work, where `m` is integer
    dimension. At most `2m` exclusion solves find the best other integer
    assignment. Its value gap and a projected-diameter Lipschitz bound
    certify a cell's fixed-label formula. A failed certificate near the
    optimum implies two near-optimal original labels, controlled by the
    [isolation lemma](new-direction/integer-label-isolation.md). Nonsmooth
    mixed recourse still has a valid upper model from every active witness.
    Exact convex MIQP is an established charged oracle; the numerical
    ambient factor and its `n^{O(k)}` dependence remain explicit.
30. **Separable mixed closure with unrestricted integer dimension:** the
    reviewed [product-domain theorem](new-direction/smoothed-mixed-separable-closure.md)
    covers convex piecewise quadratics minus supplied low-rank concave
    coupling. Integer neighbor differences and continuous derivative
    thresholds supply a globally valid polyhedral region in polynomial
    work, including long integer intervals and ties. Expected exact work
    is FPT under aligned noise and fixed-rank polynomial under uniform
    ambient noise, with the stated numerical ratios. Fresh review required
    explicitly rational breakpoints; root independently verified that
    rational polynomial pieces alone do not guarantee rational optima.
31. **Sparse expected exact QP without growth assumptions:** the reviewed
    [bag-cell theorem](new-direction/sparse-bag-cell-smoothed-qp.md)
    allows arbitrary negative inertia and variable occurrence on continuous
    product boxes. Compatible coordinate rounding preserves all original
    optimizers through overlapping cell whitelists. Sparse DP min-marginals
    give an actual near-optimal witness for each retained cell; independent
    bag noise then bounds expected state counts. Original-bound gradient
    signs and a PSD test provide a sound exact closure certificate on every
    draw. A base-only cap and finite law make failed closure rare enough to
    pay for exact active-face enumeration. Expected work is
    `C^p [4+(1+n/2)Ls/(2sigma)]^p poly(I)`, an XP bound in bag size.
    Root independently checked the complete proof and the finite-law
    budget. The [hardness comparison](new-direction/sparse-smoothed-hardness-sanity.md)
    exhibits exponentially small NO-instance gaps in the known width-two
    reduction and substantial threshold-crossing probability under larger
    noise; it makes no claim about all possible reductions.
32. **Expected exact FPT for constrained MIQP:** the separately reviewed
    [Gaussian composition](new-direction/smoothed-gaussian-miqp.md)
    gives `f(m,k,1+nu diam(P)/sigma) poly(I)` expected bit work on bounded
    rational mixed polytopes. The integer-gap closure certificate combines
    with the Gaussian-weighted local count without assuming smooth mixed
    recourse. Conditional scalar isolation adds `2 delta` per breakpoint,
    while the continuous-region event uses ambient probability transfer.
    Their combined failure budget pays for the same-draw exact fallback.
    The gap threshold grows with trial support, but the cutoff satisfies
    `J(t) <= J(0)+2t`, so sampling precision remains a base-only polynomial
    choice. Root independently read the complete composition and rechecked
    this support inequality and both probability budgets. Every finite
    draw is exact; no unperturbed-objective or real-Gaussian input guarantee
    is asserted.
33. **Sparse expected exact MIQP with arbitrary integer dimension:** the
    reviewed [mixed bag-cell theorem](new-direction/sparse-bag-cell-smoothed-miqp.md)
    extends item 31 to product mixed boxes. Power-of-two integer steps
    refine to unit resolution, then integer cells become singleton values.
    Rounding remains compatible across overlapping bag whitelists, and
    the real extension used for curvature is kept distinct from feasible
    mixed neighbor comparisons. Every integer must be fixed from a
    singleton hull before continuous PSD closure is invoked. The finite
    growth tail and active-gradient margins use integer-label/continuous-
    face counts only through base-only logarithmic precision budgets.
    Expected work has the same fixed-width polynomial form, with numerical
    integer widths retained. Root independently read the complete proof;
    two separate reviews and exact mixed DP checks found no substantive gap.
34. **Anisotropic Gaussian closure preserves separability:** the reviewed
    [extension](new-direction/anisotropic-gaussian-separable-closure.md)
    gives expected exact `f(k,1+beta diam(X)/sigma) poly(I)` work for
    separable convex rational piecewise quadratics minus a supplied
    rank-`k` concave quadratic, with arbitrary integer dimension. An exact
    rational row change and diagonal metric preserve the original unary
    terms. Anisotropic grids remove small factor singular values from the
    expected count; their effect remains polynomial in input precision.
    Full row rank after preprocessing is explicit, and `beta=alpha ||T||^2`
    refers to supplied concave curvature, not intrinsic negative curvature.
    Root independently read the complete proof; a fresh review and a second
    normalization/mesh review passed. The finite Gaussian-like law is
    base-chosen, and every draw is solved exactly.
35. **A precise obstruction to exact polynomial certificates:** the reviewed
    [box-preordering example](new-direction/box-preordering-growth-obstruction.md)
    has no finite full box-preordering certificate at any degree, despite
    point quadratic growth and treewidth four. Connected chains retain
    fixed rational coefficients and `L/g <= 61/5` in arbitrary dimension.
    A separate connected example has a segment of optima. Finite rectangular
    subdivision does not remove the local quadratic-jet obstruction.
    This applies only to the specified unmultiplied certificate family:
    the note also proves a classical Pólya-style vanishing-multiplier escape
    and checks an explicit degree-30 certificate. Root independently checked
    the proofs and chain extension; a separate adversarial review passed.
    The [prior-art audit](prior-art/box-quadratic-jet-certificate-prior.md)
    credits the established Horn/SPN and local-global principles.
36. **A direct sparse certificate discovers its own margin:** the reviewed
    [geometric copositivity theorem](new-direction/geometric-copositive-certificate.md)
    returns a verified `sigma` in `[g/16,g)` for a strictly copositive
    homogeneous quadratic, in `f(p,L/g) poly(I)` work. Relative rounding
    controls only diagonal curvature; homogeneity reduces all scales to
    one normalized grid, and an owned-variable OR flag avoids separate
    anchor solves. Verification checks complete DP minima and needs no
    growth promise. The state/trial count is independent of requested
    accuracy and coefficient-height-driven exact recovery. A second grid
    minimum yields a two-sided condition-sensitive search for `g != 0`;
    no general boundary-case termination is claimed. The non-SPN example
    accepts its first eight-node grid with `sigma=3/40`, demonstrating a
    certificate outside the obstructed family in item 35. Root independently
    read and checked both branches; fresh adversarial review passed.
37. **Direct mixed-box candidate and growth certification:** the reviewed
    [physical-shell theorem](new-direction/mixed-shell-certificate.md)
    verifies a proposed rational QP solution and discovers a valid physical
    margin with `L/sigma <= max(32,12L/g)`. Its construction and verification
    take `f(p,max(1,L/g)) poly(I)` work. Feasible lattice grids preserve
    both means and the shell threshold; a polynomial number of separate
    physical shells avoids a range-dependent state count raised to bag
    size. Below the bottom shell, only continuous coordinates move and KKT
    signs justify radial completion. Correct unique candidates necessarily
    have positive growth in this quadratic setting, so the procedure
    terminates without receiving `g`. The all-nonpositive-diagonal case has
    a separate classical endpoint-DP certificate. Root independently checked
    the complete integrated proof, including the substantive scale correction;
    three fresh reviews passed, including an independent full shell-DP
    diagnostic. The reviewed
    [normalized predecessor](new-direction/geometric-box-point-certificate.md)
    is retained with its potentially severe parameter inflation explicit.
    Candidate discovery and arbitrary optimal sets remain outside this result.
38. **A supplied full optimal fiber can be certified:** the reviewed
    [coordinate-fiber extension](new-direction/geometric-product-face-certificate.md)
    verifies that `{v} x Y` is exactly the optimal set, and discovers a
    physical distance-to-set margin in `f(p,max(1,L/g)) poly(I)` work.
    Active and free coordinates may both be continuous or lattice-valued.
    Exact two-label unary reduction makes the constant-on-fiber check
    complete; free variables then need only endpoint labels, with no
    additional rounding variance. All shell thresholds and flags concern
    active coordinates. Uniform continuous KKT checks justify the inner
    completion with free variables held fixed. Correctness of the supplied
    fiber implies positive growth automatically in this quadratic setting.
    Root independently read the complete native-coordinate extension and
    rechecked the two-label reduction and endpoint branch; fresh review
    passed. The earlier normalized continuous-active result is retained.
    No discovery of general optimal sets is claimed.
39. **A quantitative limit on positivity-preserving curvature reduction:**
    the reviewed [scaled-Horn construction](new-direction/psd-extraction-curvature-obstruction.md)
    has bag size five, growth `1/100`, and Hessian negative curvature at
    most eight. For every decomposition into a PSD matrix, an entrywise
    nonnegative matrix, and a copositive residual, the residual's first
    diagonal is at least `7d^2/8`. The prescribed homogeneous grid rule
    therefore needs more than `d/2` states at acceptance, despite fixed
    original negative-curvature/growth bounds and `O(log d)` input length.
    This obstructs that reduction and grid rule, not general optimization.
    Joint handling of a sign-changing residual remains possible, and a
    simple diagonal rescaling gives uniformly bounded conditioning for
    this family. Root independently read and checked the full construction,
    actual-grid consequence, and coordinate-change escape. Fresh review
    passed; the audit distinguishes the quantitative bound from classical
    Horn-orbit and minimal-zero irreducibility results.
40. **A direct certificate for polynomial mixed-box candidates:** the
    reviewed [nonlinear shell theorem](new-direction/nonlinear-shell-certificate.md)
    gives sound global optimality and growth certification for a supplied
    rational candidate and explicit fixed-degree polynomial factors. Under
    point growth `g>0`, construction and verification take
    `f_d(p,max(1,L/g)) poly(I)` work, returning
    `L/sigma <= max(32,20L/g)`. Sequential coordinate semiconcavity bounds
    outer-shell rounding. A coefficient Taylor-tail bound sets an inner
    radius where a quadratic boundary DP proves twice the required margin,
    leaving one margin after the remainder. Higher derivatives affect
    logarithmic radius cost rather than an extra numerical parameter.
    Root independently read the complete proof and requested two corrected
    qualifications: the sign needed in the core guarantee, and inclusion
    of curvature data in input size. A separate reviewer independently
    confirmed these fixes and the polynomial-time curvature-verification
    requirement. Full proof and bit reviews passed. Rational candidates,
    checked full-hull curvature, and explicit bounded-degree encoding remain
    essential; continuous uniqueness alone need not imply positive growth.
41. **Rectangular exact certification can require excessive precision:**
    the reviewed [quartic construction](new-direction/implicit-optimum-precision-obstruction.md)
    has constant coefficients, width two, global strong convexity, and
    fixed `L/g=112/27`. Its rational optimum contains a doubly exponentially
    small coordinate. Any rational rectangle containing that optimum and
    verifying the weak active-gradient sign everywhere has an endpoint
    with exponentially many ordinary numerator/denominator bits. The exact
    derivative minimum is attained at a rectangle corner, so stronger range
    arithmetic cannot fix this format. Short recurrence and relational
    proofs remain available. Root independently checked all constants,
    growth/Hessian bounds, and the endpoint argument; fresh review passed.
    The result constrains proposed implicit-output formats, not all exact
    algorithms or compact certificates.
42. **Polynomial optimization with logarithmic precision cost:** the
    reviewed [pruned-grid extension](new-direction/polynomial-pruned-grid-extension.md)
    gives certified mixed-box approximation in `f_d(p,kappa) poly(I+q)`
    for explicit fixed-degree rational polynomial factors. On native-integer
    boxes it finds an exact optimizer by refining below the original
    coefficient-denominator value spacing. The predecessor already proves
    the semiconcave rounding, contraction, and filtering mechanism; the
    extension supplies the polynomial table-arithmetic and exact-integer
    consequences. Full-hull curvature must be checked, including between
    integer labels, and unique continuous minima need not have positive
    growth. Root read the complete proof; independent review passed. The
    [literature audit](prior-art/polynomial-pruned-grid-prior.md) compares
    bounded-treewidth LP approximations and fixed-dimension polynomial
    FPTASs without claiming priority.
    Composing exact integer discovery with the pure-lattice shell search
    additionally returns a checked growth margin satisfying
    `L/sigma <= max(32,12L/g)` at the same parameterized cost. The polynomial
    proof is audited; no separate polynomial pruning implementation is
    claimed, because the existing diagnostic's local tables are quadratic.
43. **Exact implicit output through a verified convex subproblem:** the
    reviewed [convex-patch construction](new-direction/implicit-convex-patch-certificate.md)
    fixes integer labels by an additional sound min-marginal filter, then
    certifies strong convexity on a retained rational continuous box.
    Its unique constrained minimizer is the original exact optimum;
    its KKT system provides a compact implicit representation with
    certified arbitrary-precision evaluation. Construction and output
    size are `f_d(p,kappa) poly(I)`, and `q`-bit position/value evaluation
    costs `f_d(p,kappa) poly(I+q)`. The runtime hypothesis includes
    continuous Hessian positivity at the growth scale, automatic at
    interior optima but stronger than point growth at the boundary.
    The patch can touch original bounds and avoids whole-box active-sign
    tests. Fresh review corrected an overstrong unconditional polynomial
    output-size statement; root independently checked that correction,
    integer-filter timing, Hessian bounds, and evaluation conditioning.
    Three exact patch fixtures and a distinct integer-halo fixture passed.
    The [prior-art comparison](prior-art/implicit-convex-patch-prior.md)
    credits established KKT, interval, and convexification ingredients.
44. **The preordering obstruction already occurs at width two:** the
    reviewed [fan construction](new-direction/fan-preordering-growth-obstruction.md)
    strengthens item 35. A nonnegative rational congruence of the Horn
    matrix, plus `I/100`, has exact growth `1/100`, bag size three, and
    coordinate-curvature/growth ratio `202`. An integer positive-definite,
    entrywise-nonnegative separator excludes SPN membership and hence every
    finite-degree exact unmultiplied box-preordering identity. Connected
    chains retain width two and ratio at most `206`; their local separators
    remain strictly negative. Root read the full construction and checked
    the congruence, growth equalities, jet logic, and chain argument.
    Fresh independent review and exact determinant/decomposition checks
    passed. The non-SPN fan is classical, as the
    [primary-source audit](prior-art/spn-graph-prior.md) records. This is a
    sharper conditioned example, not a new fan theorem or a general
    optimization lower bound.
45. **Expected exact sparse polynomial optimization:** the reviewed
    [main theorem](new-direction/smoothed-sparse-polynomial.md) extends
    item 33 to explicit fixed-degree polynomial factors on mixed boxes.
    Under one base-chosen finite independent linear-noise law, expected
    bit work is `C^p [4+(1+n/2)L w_max/(2sigma)]^p poly_d(I)` and every
    draw is solved exactly. No growth, uniqueness, integer-dimension,
    or full boundary-Hessian promise is imposed. Sequential semiconcavity
    preserves the sparse cell count. Integer singleton recovery and
    verified active-bound elimination expose a free continuous block
    on which a rational strong-convexity certificate closes the search.
    The usual exact output is that verified subproblem; exceptional
    draws use an exact algebraic fallback on the same sample.
    The [finite-law interface](new-direction/polynomial-finite-noise-tails.md)
    uses two-block quantifier elimination for a height-independent scalar
    component bound and nonsingular-root counting for active margins.
    The [fallback](new-direction/polynomial-exact-fallback.md) defines the
    lexicographically selected optimum through scalar two-block formulas,
    with base-only exponential work and polynomial dependence on sampled
    coefficient bits. A separately checked symbolic-perturbation proof
    supports the same fallback interface.
    The [evaluation lemma](new-direction/convex-patch-evaluation.md)
    gives polynomial-bit position and value approximation, including
    boundary optima, using classical rational ellipsoid optimization.
    Root read all complete proofs and both fallback routes. Independent
    reviews and distinct exact DP/budget diagnostics passed.
    Two substantive presentation/interface fixes were independently
    rechecked: only the compact patch descriptor has a per-successful-draw
    polynomial size bound; the full pruning record has an expected bound.
    Also, GLS weak optimization returns near-feasible points and compares
    against an eroded body. A proved homothety and rational box projection
    now give the promised exactly feasible point and value interval.
    The [literature audit](prior-art/sparse-smoothed-polynomial-prior.md)
    confirms that qualitative generic global growth already covers mixed
    boxes, and that the exact-algebraic and convex ingredients are classical.
    The proposed advance is their finite-noise sparse expected-work
    composition. Fixed width, explicit encoding, numerical scale control,
    and the distinction between implicit and expanded output remain
    essential. A simple original-objective gap `delta+sigma sum_i w_i`
    is also certified, without claiming a better approximation rate.
    A separate [significance assessment](new-direction/smoothed-sparse-polynomial-significance.md)
    identifies nonlinear continuous discovery and boundary closure as the
    substantive gains over the quadratic predecessor. Root independently
    checked its vanishing-noise example: constant local curvature and
    `sigma=n^-2` on `[-1,1]^n` give polynomial expected work at fixed
    width while perturbation oscillation is at most `2/n`. The sampled
    objective, fixed-width dependence, and unimplemented full solver
    remain explicit limitations.
46. **A proved limitation and a conditional route to better width dependence:**
    the reviewed [connected quartic construction](new-direction/global-error-cell-barrier.md)
    forces at least `(5n/(6p))^(p/2)` retained cells on every draw for
    item 45's actual global-error retention and whole-hull closure rules.
    Degree, coordinate curvature, widths, and noise scale are fixed.
    This rules out FPT in bag size for those rules, while the instances
    themselves are easy by endpoint DP. Root independently read the proof
    and checked the full-whitelist induction, actual interaction width,
    failure of closure, and later scheduled fallback. The companion
    [local-error note](new-direction/local-error-recourse-interface.md)
    gives a star quadratic where a bag-local correction discards the
    unique optimizer. Certified conditional recourse with local absolute
    error would remove the dimension factor in the expected count;
    efficiently computing that recourse is unresolved. The exact star
    calculation and the sufficient interface passed independent checks.
    A later positive-definite star supplement has fixed `L/g`, yet
    normalized conditional grid error varies by `(d-1)h^2` with `d^2`
    leaves and still causes false local-budget pruning. Root read and
    rechecked its exact spectrum and min-marginal formulas. This removes
    positive definiteness as a repair for that deterministic message
    argument; a global convex solver handles the example immediately,
    and no smoothed or general runtime lower bound is claimed.
47. **Deterministic boundary output and its limits:** the reviewed
    [enclosure theorem and nearby-minimum construction](new-direction/deterministic-boundary-output.md)
    give certified coordinate enclosures and objective bounds in
    `f_d(p,kappa) poly(I+q)` under point growth alone. This is an
    approximation consequence of existing pruning, not a new finite
    uniqueness certificate. A constant-condition, width-two quartic has
    another strict local minimum satisfying KKT, strict complementarity,
    and second-order sufficiency at doubly exponentially small distance
    from the global optimizer. Root independently checked the reduction,
    Schur complement, interiority, and distance estimate. The obstruction
    concerns a symmetric stationary-point isolation neighborhood; this
    example has a short correlated algebraic certificate. A separate
    reviewed [cubic construction](new-direction/convex-active-set-radical-comparison.md)
    reduces Square Root Sum to one exact active-bound decision with
    treewidth two, `L<=5`, and growth `g=1/32`. Root rechecked the balanced
    averaging, strong convexity, and decision equivalence. The result
    clarifies the output contract and does not claim NP-hardness or
    difficulty producing an implicit convex descriptor. The
    [completed source comparison](prior-art/convex-active-set-radical-prior.md)
    distinguishes the reduction from prior radical comparison, zero
    testing, and exact real-arithmetic results; no priority claim follows.
48. **A constrained parameterization corollary and a feasibility barrier:**
    reviewed [polynomial graph equalities](new-direction/smoothed-polynomial-graph-constraints.md)
    extend item 45 through bounded-depth explicit substitution. Ancestor
    expansion gives bag size at most `max(1,k^D)p`; conditioning on all
    dependent-coordinate noise leaves independent free-coordinate noise.
    The law and all bounds are chosen before either draw. The theorem
    charges pullback curvature and excludes further restrictions on the
    free product domain. Root read the full proof and independent review,
    including running intersection and coefficient-height separation.
    Exact rational free approximants map to exactly feasible rational
    graph points. Two examples show why a bounded inverse alone preserves
    neither conditional independence nor the original curvature scale.
    The separate [affine feasibility reduction](new-direction/constrained-smoothing-barrier.md)
    has width at most three, bounded coefficients, an always-feasible zero
    point, and a linear objective. Every draw of inverse-polynomial
    objective noise preserves the SUBSET SUM answer. A general constrained
    analogue of item 45 would therefore give zero-error expected-polynomial
    SUBSET SUM, not directly `P=NP`. A TU example separately defeats only
    the coordinate-neighbor counting argument. Both reductions were read
    independently; positive implicit-graph and simplex-block extensions
    are recorded in items 49 and 51 below.
49. **Resource and probability-simplex blocks:** the reviewed
    [simplex theorem](new-direction/simplex-block-smoothed-extension.md)
    extends item 45 to disjoint continuous simplex blocks plus native-
    integer intervals, with polynomial factors coupling different blocks.
    Under one base-chosen finite ambient-noise law, expected work is
    `C^p [4+(2+n/2)L max(1,w_max)/(2sigma)]^p poly_d(I)`, with exact
    output on every draw. Feasible corners of a clipped dyadic cube span
    its simplex intersection. Correlated mean-preserving block rounding
    uses a block Hessian upper bound, rather than merely its diagonal.
    Counts on original faces use tangent directions; conditioning on
    anchor coefficients handles near-optimal tuples, while direct counting
    of transformed noise tuples handles dependent multiplier coordinates.
    Strict derivative and derivative-difference tests identify original
    faces without a positive-coordinate slack assumption. A rational
    strong-convexity test closes on a relative polytope, whose inradius,
    exact projection, and GLS repair give polynomial-bit evaluation.
    Root independently read and checked the entire proof and both types
    of noise argument. Two independent reviews and distinct exact DP,
    finite-law, and projection diagnostics passed. Substantive fixes
    rechecked independently include derivative bounds on the enclosing
    coordinate box, a complete relative-polytope evaluator, and omitting
    both absolute-gradient tests on original equality-simplex blocks.
    Their equality multiplier has no margin requirement. Whole-block bags,
    product constraints, fixed degree, and numerical scale bounds remain
    material. The [prior audit](prior-art/simplex-block-smoothed-prior.md)
    credits the established ingredients and does not establish priority.
50. **Expected exact optimization through a small core and tractable recourse:**
    the reviewed [recourse theorem](new-direction/smoothed-box-stable-recourse.md)
    gives expected work `8^k [3+(1+k/2)L/(2sigma)]^k poly(I)` for
    continuous unit-box QP. Fixing a supplied core of size `k` must leave
    exact polynomial-bit global recourse under every rational coordinate
    restriction. True corner values need only the core rounding budget.
    A new excluded-region certificate uses at most `2n` additional
    recourse calls and a global core-gradient bound to confine every
    relevant residual optimum. Original-bound signs and a constant-Hessian
    test then close with an exact rational convex-QP solve. The cutoff
    depends only on base data; it avoids reconstructing rationals at a
    precision that depends circularly on the noise denominator. Every
    sample is solved exactly, with rare same-draw face enumeration.
    Root helped derive the excluded-region step, then checked the complete
    draft; a separate researcher independently reviewed all formulas and
    the finite-law composition. The review specifically checks omission
    of artificial excluded slabs at clipped original bounds. Distinct
    exact diagnostics cover containment, ties, singular cases, and budgets.
    Deleting the core to a forest gives a concrete expected FPT corollary
    using Del Pia--Khajavirad's established oracle, including nonconvex
    residuals with unbounded negative inertia. This does not give FPT in
    treewidth, polynomial recourse for general sparse polynomials, or a
    mixed-variable extension. The [focused external comparison](prior-art/smoothed-box-stable-recourse-prior.md)
    credits exact forest DP, conditional value functions, optimization-based
    bound tightening, low-dimensional global search, and discrete smoothing.
    It identifies the finite-law expected exact composition as the candidate
    contribution, without establishing publication priority or solver speedup.
51. **Sparse monotone implicit graph constraints:** the reviewed
    [main theorem](new-direction/smoothed-implicit-graph-constraints.md)
    permits mixed retained coordinates and continuous dependent variables
    defined by local scalar polynomial equations. Uniform positive
    derivative floors and endpoint brackets give one root throughout
    the retained real box. After bag expansion, expected work is
    `C^p [4+(1+n)L w_max/(2sigma)]^p poly(I)` under one finite ambient
    noise law, with exact output on every draw. Unlike explicit
    substitution, reduced costs may be algebraic. Rational lower bag
    costs with total error at most the rounding budget preserve every
    optimizer and give consistent witnesses within four times that budget.
    Certified approximate gradients and Hessians close a convex patch.
    Graph-assisted two-block elimination and nonsingular bordered KKT
    roots supply uniform finite-law tails without expanding algebraic
    charts. A rational weak separator, GLS repair, and upper value
    enclosures give certified evaluation. Root read all proofs and wrote
    a [full composition review](reviews/implicit-graph-composition-review.md);
    a second independent composition review and separate oracle/KKT
    reviews passed. Root rechecked the stated degree bound, global
    dependent-interval derivative premise, and certificate-verification
    qualification. The nonlinear diagnostic uses approximate bag costs,
    not an exact algebraic comparison oracle. Exact feasible approximants
    consist of rational retained coordinates and their unique root
    equations; rounded physical coordinates are not claimed feasible.
    The [prior audit](prior-art/implicit-monotone-actuator-prior.md)
    compares the actual model with implicit-state global optimization.
    Global coverage, one root per dependent coordinate, and pullback
    curvature are material restrictions. A cubic actuator example with
    binary modes illustrates the added nonlinear constrained capability.
52. **Continuous order polytopes with overlapping constraints:** the reviewed
    [composition](new-direction/smoothed-sparse-order-polynomial.md)
    gives expected work
    `C^p p! (p+1) [2+nH(p+1)/(2sigma)]^p poly_d(I)` for sparse
    polynomial objectives on `0<=x<=1, x_i<=x_j`. Directed cycles are
    allowed. Common-threshold rounding preserves every order relation
    and specified bag cell. The
    [chamber count](new-direction/order-polytope-cell-count.md)
    represents each conditional fiber by affine copy maps on at most
    `p!` bag-order chambers. Their number need not be enumerated.
    The [face certificate](new-direction/order-polytope-face-closure.md)
    uses linear optimization to certify active equalities from a gradient
    enclosure. A paired-noise fiber count controls small exposure gaps
    without unique multipliers or a conditional-density assumption.
    Rational convex-patch evaluation and isotonic feasibility repair give
    exact implicit output with a same-draw algebraic fallback. Root read
    all three proofs and independently checked the geometry, gap
    perturbation, finite-grid counts, Hessian scaling, and bit interfaces.
    The [completed-text review](new-direction/order-polytope-independent-review.md)
    passed with distinct exact checks on chains, forks, cycles, and
    degenerate face gaps. Rechecked corrections include tautological-row
    removal, the physical-coordinate copy factor, and additional fallback
    precision for Euclidean error. The parameter `H` is a full Hessian
    upper bound; only continuous variables are covered. This is fixed-width
    polynomial work, not FPT in width or a general TU/affine theorem.
    The [completed prior audit](prior-art/order-polytope-smoothed-prior.md)
    credits Stanley's classical geometry and Bach's common-quantile
    coupling. Root rechecked the distinctions between fixed-width and
    FPT bounds, and between unknown-growth and supplied-growth results.
    The binary extension is item 54 below.
53. **Dense nonlinear recourse with a small continuous core:** the reviewed
    [polynomial theorem](new-direction/smoothed-polynomial-box-recourse.md)
    gives expected work `8^k [3+(1+k)L/(2sigma)]^k poly_d(I)` for fixed-
    degree continuous box polynomials. A supplied core of size `k` has
    upper diagonal curvature `L`; every rational residual subbox must
    admit certified lower values and feasible rational completions in
    polynomial bit work at arbitrary requested accuracy. Verified convex
    residual Hessians supply this oracle without strong convexity.
    Approximate corner calls give incumbent error `2e` and retained
    witnesses of error `4e`, with `e=kLh^2/8`. Certified lower bounds on
    excluded residual slabs transfer containment across the core hull;
    the explicit `7g_0 r^2/16` margin exceeds the transfer error.
    Uniform nonlinear gradient and Hessian tests then close a strongly
    convex patch. One base-chosen finite ambient-noise law pays for the
    rare same-draw algebraic fallback. Every draw has exact implicit
    output; usual descriptors have polynomial size and evaluation cost,
    while complete proof records and exceptional outputs have expected
    bounds. Root read the whole proof and independently checked the
    constants, empty-core case, and final rational tangent certificate.
    The [fresh review](reviews/smoothed-polynomial-box-recourse-review.md)
    passed; the nonlinear diagnostic includes an irrational optimizer.
    A [checked structural family](new-direction/polynomial-recourse-rank-separation.md)
    has one core variable and dense quartic recourse, while every fixed
    PSD quadratic convexifier requires rank at least the residual
    dimension. Root rechecked its boundary kernel proof, interior-core
    optimum, and nonlinear entropy-correction caveat. The
    [assessment](new-direction/polynomial-box-recourse-significance.md)
    and [prior audit](prior-art/smoothed-polynomial-box-recourse-prior.md)
    credit classical partial-convex search and convex optimization.
    Core discovery, convexity certification, full ambient noise, and
    implicit output remain material premises. Core-only noise with
    residual optimal fibers is a separate unresolved target.
54. **Binary and continuous order constraints:** the reviewed
    [mixed theorem](new-direction/smoothed-mixed-order-polynomial.md)
    gives expected work
    `C^p q! (q+1) [2+3NH/(4sigma)]^q poly_d(I)` with unrestricted
    binary dimension, `N` continuous coordinates, and at most `q`
    continuous coordinates in any supplied bag of size at most `p`.
    Common-threshold rounding fixes binary labels. A monotone scalar
    transport fixes endpoints and maps each conditional witness across
    its closed order-simplex face. This gives feasible upper supports
    even where the mixed projection is nonconvex or the value jumps.
    Along the count's disjoint zero-one directions, transported squared
    length is at most `N`, giving the improved count above. Exact closure
    fixes every binary label before applying continuous LP exposure;
    a counterexample proves that reversing these steps is unsound.
    The finite-law proof unions over binary slices without conditioning
    on the selected label. Original-bound propagation precedes feasible
    approximation repair, preserving binary zeros. Root read the entire
    final proof and the [fresh review](reviews/smoothed-mixed-order-review.md),
    and independently checked the directional improvement, bag-binary
    noise constant, and singleton-first certificate. Distinct author
    and reviewer exact diagnostics passed. The theorem covers implications
    and continuous activation bounds, but retains a full Hessian premise
    and fixed-width polynomial rate. Arbitrary integer ranges and general
    affine constraints remain excluded.
55. **Exact native-integer recourse with expanded algebraic output:** the
    reviewed [main theorem](new-direction/smoothed-native-integer-recourse.md)
    couples a continuous unit-box core of size `k` to a fixed bounded
    integer polytope. Exact rational conditional optimization must remain
    polynomial under arbitrary integer coordinate-bound restrictions.
    Expected work under one finite ambient-noise law is
    `[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)`, after the reviewed
    constant-base improvement in item 58. At most `2r` restricted oracle calls cover
    every label different from the incumbent. A gap exceeding the
    Lipschitz transfer error certifies one label throughout the retained
    core hull. The corresponding whole core slice contains a global
    optimizer; exact algebraic optimization on that slice completes the
    problem without a Hessian or active-gradient test. The exact box
    solver has a constant exponential base and an absolute coefficient-
    height exponent. Every draw returns integer labels and
    isolating-polynomial representations of core coordinates and value
    of size `c_d^k poly_d(I)`. Only search and proof traces have expected
    size bounds. A growth-only tail pays for rare same-draw label
    enumeration. Native numerical widths enter logarithmic precision
    budgets, not the parameter factor. Root read the complete original
    and simplified proofs and independently checked the exclusion
    constants, format/height separation, and all-draw output bound.
    The [fresh review](reviews/smoothed-native-integer-recourse-review.md)
    passed with distinct exact diagnostics. The
    [constant-base transfer review](reviews/constant-base-core-transfer-review.md)
    separately verifies completion, output, tie comparisons, and fallback;
    root read the changed argument and this review. The
    [source-backed flow/TU corollary](prior-art/integer-convex-flow-recourse-prior.md)
    uses Hochbaum--Shanthikumar's classical exact separable-convex oracle;
    endpoint tangent extensions cover its outside-interval queries.
    Network residual potentials give short rational optimality proofs.
    The core changes costs only, not balances or feasibility. An
    [optional implicit variant](new-direction/native-integer-recourse-implicit-closure.md)
    preserves the sharper count without the algebraic processing factor.
56. **Core-only noise with changing strongly convex residual faces:** the
    reviewed [full theorem](new-direction/core-only-noise-boundary-recourse.md)
    assumes a verified uniform residual Hessian bound `H_RR>=mu I`.
    It retains `8^k[3+(1+k)L/(2sigma)]^k poly_d(I)` expected work while
    perturbing only core coefficients. No residual interiority, stable
    active pattern, positive residual multiplier margin, or explicit
    selector is supplied. Strong monotonicity gives a Lipschitz selector
    and lifts projected growth to full growth. A
    [three-block active-stratum formula](new-direction/core-noise-active-stratum-tube.md)
    encloses stationary-noise images of pattern boundaries in nonzero
    polynomial zero sets of degree `2^poly_d(I)`. The classical
    Basu--Lerario singular-algebraic tube theorem, followed by exact grid
    jitter, bounds proximity with coefficient-height-independent constants.
    On a stable face ball, the
    [small-multiplier lemma](new-direction/small-residual-multiplier-curvature.md)
    permits weak residual bounds to remain free: their multiplier
    derivatives have small Schur-complement contribution. Large signs
    are fixed by ordinary whole-patch tests, and a rational full-Hessian
    test closes. The algorithm never constructs the eliminated sets or
    discovers a branch. Three base-only bad-event budgets pay for exact
    fallback on the same draw. Root read the entire theorem and supporting
    proofs, independently rederived the restored modulus and probability
    constants, and checked Basu--Lerario Theorem 1.1 directly in the
    primary PDF. The
    [composition review](new-direction/core-only-noise-boundary-recourse-independent-review.md)
    and [supporting review](new-direction/core-noise-boundary-lemmas-independent-review.md)
    passed. The separately reviewed
    [interior antecedent](new-direction/core-only-noise-strong-recourse.md)
    remains documented. Uniform `mu` also gives a fixed rank-`k`
    quadratic convexifier of scale `M+M^2/mu`; the numerical gain is
    preserving original `L`, not a new separation from all low-rank
    convex differences. Merely convex or strictly convex residuals
    remain outside this closure; the
    [rotating-fiber counterexamples](new-direction/core-only-noise-rotating-fiber.md)
    and [selector interface](new-direction/affine-convex-fiber-certificate.md)
    record the remaining limitations. The
    [focused prior audit](prior-art/core-only-noise-boundary-recourse-prior.md)
    credits parametric sensitivity, generic tilts, low-rank convexification,
    exact parametric-QP regions, and the classical tube theorem; it does
    not establish publication priority.

57. **Limits of residual regularization and qualitative error bounds:** the
    reviewed [quartic construction](new-direction/regularization-point-precision-obstruction.md)
    is jointly convex on a box, has bounded rational coefficients and
    `O(n)` monomials, and has a unique optimizer. Its uniformly strongly
    convex chain creates a positive coordinate of size at most
    `2^(-2^(n-1))`; a final square transfers that scale to an order-one
    optimal coordinate. The exact isotropic Tikhonov path needs at least
    `2^n` ordinary rational parameter bits for constant point accuracy.
    At a point distance one from the optimizer, the objective gap is at
    most `2^(-2^n)`. Hence any global bound `dist<=C gap^theta` requires
    `log_2(C)/theta>=2^n`. This is superpolynomial in the stated
    `O(n log n)` input length. The
    [conditional rate note](new-direction/canonical-convex-fiber-regularization.md)
    independently proves an existential degree-only exponent on compact
    polytopes by affine-section geometry, transverse cancellation,
    univariate interpolation, and a polyhedral angle bound. Its constant
    can have the same precision obstruction. The
    [main investigation](new-direction/core-only-noise-regularization-limit.md)
    also separates discontinuous canonical fiber selection from the
    need for one finite noise law across all requested accuracies.
    Root read all proofs and the
    [independent review](new-direction/regularization-limit-independent-review.md),
    rechecked the Hessian identity, chain recurrence, growth argument,
    and projection estimates, and found no blocker. The original quartic
    is easy by fixing its last coordinate and solving the strongly convex
    chain; no general hardness or impossibility of compact exact output
    follows. The [focused prior comparison](prior-art/convex-polynomial-error-bounds-prior.md)
    checks Li's primary definitions and constrained error bounds; Yang's
    directly related paper remains abstract-only. No novelty finding is made.
58. **An exact constant-base polynomial component interface:** the reviewed
    [construction](new-direction/polynomial-component-primitive-limit.md)
    optimizes any explicit fixed-degree rational polynomial on a closed
    rational `k`-box in `c_d^k poly_d(H)` deterministic bit work, including
    degenerate inputs. A pure-power deformation supplies a finite free
    quotient algebra. Moment-curve linear forms separate bounded limit
    vectors and expose every escaping branch. Characteristic-polynomial
    derivatives recover all coordinates in one common real-root
    representation, after multiplicity cancellation. Feasible spurious
    candidates from other forms cannot invalidate the minimum. Memoized
    normal forms and fixed-variable determinant interpolation preserve
    a constant exponential base; value-resultant comparisons handle exact
    ties. The [independent review](reviews/polynomial-component-primitive-limit-review.md)
    passed; root read the full construction and rechecked completeness,
    reconstruction and the bit ledger. These are classical algebraic
    mechanisms, with the strongest matching complexity comparison still
    under investigation, not an established original algebraic algorithm.
    The [strong-field composition](new-direction/strong-field-component-polynomial.md)
    applies this interface after strict coordinate monotonicity pins
    original bounds. Independent bad sites form components of the primal
    monomial graph. Weights `a_i=c_d` for continuous coordinates and
    native label counts for integers give expected work
    `poly_d(I+b)[1+sum_i a_i q_i/(1-4 Delta max_i a_i q_i)]` when the
    denominator is positive. A stronger explicit noise condition bounds
    it away from zero. Separate
    [composition](reviews/strong-field-component-polynomial-review.md) and
    [arithmetic-budget](reviews/strong-field-polynomial-budget-review.md)
    reviews passed; root checked both. Every draw is solved exactly,
    including singular atoms. Output retains one algebraic representation
    per component and their symbolic value sum, with expected polynomial
    numerical refinement. No efficient arbitrary comparison of that sum
    is claimed. The large numerical perturbation is a material limitation;
    this is not a weak-noise or original-objective guarantee.
59. **Core-only perturbations with tied integer flows and interior core:**
    the reviewed [theorem](new-direction/smoothed-interior-core-flow.md)
    keeps `[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)` expected work
    and `c_d^k poly_d(I)` algebraic output on every draw, perturbing only
    the small continuous core. Every optimal core point must be interior
    throughout the noise cube; residual flow ties are permitted. The
    selected integer flow's rational shortest-path tree lifts to polynomial
    potentials. Exact non-strict reduced-cost tests over the retained box
    prove uniform optimality, including identically zero ties. The
    analysis-only universe of all labels and trees has a polynomial
    logarithmic size. Cross-label gradient images of its chart boundaries
    have lower dimension and a base-only algebraic degree bound. A
    finite-grid tube estimate and projected-growth tail force closure;
    the same-draw fallback remains exact. Root read the whole proof,
    [full review](reviews/smoothed-interior-core-flow-review.md), and
    [constant-base transfer review](reviews/constant-base-core-transfer-review.md).
    The computational `c_d^k` factor is distinct from the larger
    analysis-only quantifier-elimination degree bound. Independent cyclic
    and serial-network diagnostics include persistent ties and zero-cost
    cycles. A [two-arc boundary obstruction](new-direction/core-only-flow-boundary-obstruction.md)
    gives a fixed `1/16` event with good core growth but no flow uniformly
    optimal on any retained origin box. Adding zero-cost stages makes a
    literal enumeration fallback expensive. This is not a hardness result:
    the example has an elementary certificate. General boundary closure
    remains active work. The [prior comparison](prior-art/smoothed-interior-core-flow-prior.md)
    credits the exact flow oracle, parametric methods, partial-convex
    search and smoothed discrete precedents without establishing priority.
60. **Constant-distance convex point output contains Square Root Sum:**
    the reviewed [two-copy construction](new-direction/convex-point-radical-comparison.md)
    strengthens the earlier exact active-bound comparison. Oppositely
    signed strongly convex cubic copies produce complementary nonnegative
    auxiliary coordinates. A degree-four nonnegative coupling, with a
    division-free global Hessian certificate, forces a new coordinate to
    zero or one according to the source comparison. Every optimizer has
    that endpoint; after direct equality preprocessing the optimizer is
    unique. Field-trace transitivity and positivity justify the equality
    test using integer square roots without factorization. The primal
    graph has treewidth two, and coefficients and coordinate curvature
    remain bounded after unit-box normalization. Distance `1/4` in
    Euclidean or maximum norm suffices. Deterministic polynomial point
    evaluation would imply Square Root Sum in P; always-correct expected
    polynomial work gives a Las Vegas algorithm. Adjoining an independent
    noisy core preserves the comparison on every draw, placing a precise
    condition on general merely-convex residual point-output extensions.
    Full point conditioning is not controlled, and value approximation
    remains available. Root read the whole proof, independently checked
    all construction steps, and read the
    [full review](reviews/convex-point-radical-review.md) and
    [assessment](new-direction/convex-point-comparison-assessment.md).
    The latter also proves an unconditional output-size statement:
    prime-radical coordinates have `2^n` distinct real conjugates, so
    Descartes' rule forces at least `2^(n-1)+1` nonzero coefficients in
    any explicitly listed rational defining polynomial. This does not
    apply to circuit or joint implicit representations. The
    [prior comparison](prior-art/convex-point-radical-prior.md) identifies
    Etessami--Yannakakis's related strong-approximation reductions for
    unique Nash equilibria; root checked the actual local Theorem 4
    statement. No NP-hardness, computational impossibility, or publication
    priority is inferred. The simpler
    [canonical-selector antecedent](new-direction/canonical-selector-radical-comparison.md)
    and its [review](new-direction/canonical-selector-radical-independent-review.md)
    remain documented with their narrower scope.
61. **Core-only smoothing with arbitrary network-flow core faces:** the
    reviewed [boundary theorem](new-direction/smoothed-boundary-core-flow.md)
    removes item 59's interiority premise. Exact optimal-flow potentials
    describe all tied winners by tightened arc intervals. On those
    intervals, inward derivative costs are convex; two-label intervals
    use linear interpolation. A conformal-cycle argument bounds distance
    to the tied-flow set by `r` times total interval violation. The
    [deterministic certificate](new-direction/flow-optimal-face-certificate.md)
    combines derivative minima, first outside marginals, and a Taylor
    bound to fix a core face without enumerating the tied labels.
    Facewise stationary-noise images and normal-coordinate interval
    probabilities control its margins. A separate fixed-dimensional
    elimination argument turns distance from chart zeros into a uniform
    positive value bound. This requires `f_d(k) poly_d(I)` sampling and
    query bits; they are charged throughout the proof. Expected work is
    `f_d(k)[3+(1+k/2)L/(2sigma)]^k poly_d(I)`, with exact algebraic output
    and refinement on every draw. Root read the entire proof and all
    reviews, and independently rederived the geometry, margin, cutoff
    and expected-work calculations. Root caught a mismatch between the
    chart family and inherited artificial-source sign tests. The revised
    algorithm tests original-arc intervals and marginals only; root and
    the independent reviewer rechecked this correction. The
    [certificate review](reviews/flow-optimal-face-adversary.md),
    [full composition review](reviews/smoothed-boundary-core-flow-adversary.md),
    [arithmetic review](reviews/boundary-core-flow-bit-adversary.md), and
    [margin audit](reviews/flow-boundary-margin-review.md) all pass.
    Distinct static and complete finite-law diagnostics cover boundary
    closure, persistent ties and same-draw fallback. The
    [prior comparison](prior-art/smoothed-boundary-core-flow-prior.md)
    credits separable-flow duality, circulation decomposition, parametric
    optimization, tube bounds and partial-convex search. The result keeps
    feasibility independent of the core and does not cover arbitrary
    coupled integer recourse. Curvature can itself grow with capacities,
    so the binary-capacity statement is conditional on the displayed
    `L/sigma` parameter. No practical performance or priority claim is made.
    The subsequently reviewed
    [bilinear corollary](new-direction/smoothed-bilinear-core-flow.md)
    restores `[8^k(3+(1+k/2)L/(2sigma))^k+c_d^k] poly_d(I)` and ordinary
    polynomial sampling precision. An affine polynomial's distance from
    its cube-restricted zero set bounds its value through its smallest
    nonzero coefficient; if it has no zero, a vertex denominator bound
    applies. Online sign and identity tests are polynomial work, and
    only the final core solve contributes `c_d^k`. Root independently
    checked this argument and the
    [fresh review](reviews/smoothed-bilinear-core-flow-review.md), including
    its separate arithmetic audit. Here the core objective alone supplies
    `L`, even with nonlinear scalar flow costs. The
    [significance note](new-direction/boundary-core-flow-significance.md)
    preserves the deterministic approximation baseline and distinguishes
    exact perturbed optimization from benefits to the original objective.
62. **Convex quartic point evaluation also contains PosSLP:** the reviewed
    [arithmetic-circuit reduction](new-direction/posslp-convex-point-extraction.md)
    represents each integer circuit value by a bounded numerator and
    positive denominator using fixed quadratic gates. A final gate has
    the sign of `2A-1`, handling zero source output without a decision
    oracle. Geometric weights make the gate-residual quartic strongly
    convex on the entire signed box: normalized Jacobian row and column
    bounds control the positive term, and a geometric sum controls all
    nonlinear Hessian losses, including arbitrary fanout and repeated
    inputs. The weights and expanded polynomial have polynomial encoding
    length; exact circuit values are never expanded. Two opposite bound
    tests and the already reviewed paired quartic then force a unique
    optimizer's designated coordinate to one iff `A>0`. Constant point
    accuracy decides PosSLP. Common positive scaling bounds coefficient
    magnitudes, but there is no bounded-treewidth claim or controlled full
    point-growth modulus. Root read and rederived the entire construction
    and the [fresh review](reviews/posslp-convex-point-review.md), which
    includes distinct new-gate diagnostics. The independent noisy-core
    consequence gives a Las Vegas, rather than deterministic, conclusion
    from expected polynomial work. The
    [prior comparison](prior-art/convex-point-posslp-prior.md) identifies
    existing PosSLP reductions to strong approximation of unique Nash
    equilibria and exact semidefinite feasibility. It does not claim
    PosSLP is provably strictly harder than Square Root Sum. The possible
    contribution is the box-convex quartic minimizer/output class; no
    NP-hardness, value-approximation obstruction, or publication priority
    is established.

63. **One finite core-noise law supports all objective precisions:** the
    reviewed [value-oracle theorem](new-direction/core-only-noise-value-oracle.md)
    handles one or two nonconvex core variables with arbitrary convex
    polynomial residuals. Each query returns a feasible rational point
    and a certified global interval of width `2^-q`, with expected work
    `(1+L/sigma) poly_d(I+q)`. It needs no residual modulus or residual
    perturbation, and supplies no optimizer-distance guarantee. Approximate
    corner solves of width `e=kLh^2/8` give a global interval `[U-2e,U]`
    and a `4e` witness in each retained cell. Projected growth bounds
    generated cells at every level by `512 max(1,L/g)^(k/2)`. A cap before
    generation, linear list operations, and the finite-law tail
    `P(g<t)<=kt/sigma+C_0/M` make its truncated moment and fallback cost
    polynomial for `k<=2`. One base choice `M>=C_0 B` controls the atoms;
    no mesh-spacing condition or accuracy-dependent resampling is needed.
    A single random factor bounds all query precisions simultaneously.
    Root read the complete proof and
    [fresh independent review](reviews/core-only-noise-value-review.md),
    and independently rechecked the count, cap, moments and bit budgets.
    Distinct exact diagnostics examine cell certificates and finite-law
    atoms. The cap proof does not extend directly to larger cores; its
    failed moment bound is not a hardness result. The
    [focused prior audit](prior-art/core-only-noise-value-oracle-prior.md)
    compares Kelner–Nikolova's rotated low-rank quasi-concave model,
    parametric convex optimization, and the project's earlier grid
    counts. Root read the comparison; priority remains unresolved.
64. **Core-only smoothing over bounded TU integer systems:** the reviewed
    [TU extension](new-direction/smoothed-core-tu-recourse.md) replaces
    network recourse by fixed TU equalities and inequalities, retaining
    both item 61's general and bilinear bounds. Piecewise-linear
    interpolation on integer grid cells and TU integrality establish a
    compact adjacent-slope dual at each optimal native label. After
    fixed-column and dependent-row preprocessing, that dual is pointed;
    its TU vertices have polynomial base height. A fixed multiplier box
    permits polynomial-time vertex extraction. Active-basis polynomial
    charts replace tree potentials, including bases using artificial
    box rows; only original adjusted marginals need remain valid over
    the retained core region. The whole optimal set again consists of
    tightened coordinate intervals. A conformal unit-circuit charging
    argument supplies the same `r`-proximity estimate as for flows.
    The inequality corollary adds explicit finite zero-cost slacks whose
    binary lengths are polynomial and whose core derivatives vanish.
    Root read and rederived the replacement interfaces and the
    [independent review](reviews/smoothed-core-tu-recourse-review.md),
    including the separate slack audit. The author's exact TU diagnostics
    were inspected independently without redundant reruns. The
    [prior comparison](prior-art/tu-equality-separable-convex-prior.md)
    credits established TU recourse and duality; Graver's primary text
    remains unavailable, so its precise circuit locator is not claimed.
    The circuit proof is self-contained. Core-dependent feasibility and
    general integer matrices remain outside the result. The
    [assessment](new-direction/boundary-core-flow-significance.md)
    gives a clipped-quadratic aggregate interpretation with `L=1` for
    arbitrary coupling magnitudes and capacities. Practical value and
    publication priority remain unestablished.
65. **All-scale geometry removes the value oracle's two-core limit:** the
    reviewed [theorem](new-direction/all-scale-core-value-oracle.md) gives
    `f_d(k)(1+L/sigma)^k poly_d(I+q)` expected work for any core size,
    with merely convex polynomial residuals and one finite core-only law
    supporting every accuracy. Let `S_h` be the `kLh^2/2` near-optimal core
    set and pad its convex hull by `[-h/4,h/4]^k`. Disjoint grid cubes and
    a maximum-simplex determinant give a single all-scale factor `W`
    bounding every generated level. The conjugate of the projected value,
    plus `||c||^2/(2L)`, defines a locally finite pushforward measure.
    Fenchel residual bounds place each translated padded hull inside
    the inverse image of an open coefficient ball. A `5r` covering
    argument gives the tail `P(W>T)<=f(k)(1+L/sigma)^k/T` under continuous
    noise. Carathéodory witnesses, one shared universal competitor, and
    quadratic QR equations express the event with two polynomial-size
    quantifier blocks. Their section count transfers the tail to one
    finite law with polynomial sampling bits, including singular atoms.
    Integrating the capped tail and paying for same-draw exact fallback
    proves a common expected work bound for all query precisions.
    The [fresh adversarial review](reviews/all-scale-core-value-oracle-review.md)
    caught a false polynomial-size claim for the expanded determinant.
    The compact QR replacement preserves the intended format. Root read
    the full corrected proof and review and independently rederived the
    volume comparisons, measure inclusion, open-ball safeguard, constants,
    quantifier structure and cap accounting. A distinct exact diagnostic
    checks the new geometry and singular-measure cases. The
    [prior comparison](prior-art/all-scale-core-value-oracle-prior.md)
    distinguishes classical ingredients and nearby smoothed optimization
    from the proposed composition; priority remains unresolved. This
    strengthens item 63's value output, not the special TU theorem's exact
    optimizer output. No efficient residual optimizer-coordinate oracle
    or practical speedup is claimed.
    The [independent significance assessment](new-direction/all-scale-core-value-significance.md)
    compares exact TU output, the deterministic objective-accuracy grid,
    low-rank convexification and the capacity-independent `k sigma`
    regret. Root read and checked its interval and class-separation
    calculations. A simpler reviewed
    [continuous-noise comparator](new-direction/continuous-core-noise-value-oracle.md)
    gives value intervals valid for every completion of finitely revealed
    prefixes of persistent random bitstreams. Per-scale continuous counts
    and a summable weighted trace give a common work factor without
    fallback. Root read its proof and
    [review](reviews/continuous-core-noise-value-review.md); this is a
    distinct random-real input model and a modest consequence of the
    earlier count, not a replacement for the finite-law result.
    The reviewed [integer-oracle corollary](new-direction/core-value-certified-recourse.md)
    also transfers the value guarantee to any fixed bounded integer
    domain with an already proved certified polynomial conditional
    solver. Integer-membership disjunctions enlarge the analysis format
    only exponentially in base size; the all-scale event still has two
    blocks. Label enumeration and the generic core fallback supply a
    base-only exponential completion factor. Root read the all-dimensional
    extension and its [separate review](new-direction/core-value-certified-recourse-independent-review.md).
    The returned label supports the certified objective gap; no stable
    or exactly optimal label is promised, and a general integer polytope
    does not automatically supply the required oracle.
66. **Efficient coordinates of a fixed globally optimal core:** the
    reviewed [output addendum](new-direction/core-only-noise-core-oracle.md)
    strengthens item 65 with Euclidean core error at most `2^-q` while
    retaining the feasible objective-gap output and the same expected
    bound. Its generic algebraic fallback fixes a core-first lexicographic
    optimizer independently of query accuracy. All retained hulls contain
    every optimal core and the feasible incumbent, so a rational squared
    diameter test certifies error to that selected core on every draw.
    Replacing `L` by `L+sigma` handles zero curvature. A base threshold
    `g_0=sigma/(2kB)` supplies a terminal depth polynomial in `I+q`.
    If the actual hull remains too large, exact fallback handles the
    draw. One enlarged finite noise law makes this extra event have
    probability at most `1/B`, with no union over precisions. Combined
    with the all-scale count event, it preserves the common expected
    work factor. The [fresh review](reviews/core-only-noise-core-oracle-review.md)
    and root independently checked containment, the rational diameter
    bound, the actual generic selector formulas, and fallback refinement.
    The simpler `k<=2` proof retains its sharper linear `1+L/sigma`
    factor. Ordinary residual witnesses need not converge, and their
    coordinates have no optimizer-distance promise. The original
    unperturbed optimum is not recovered by this smoothing statement.
67. **Coupled linear feasibility with one core-noise law:** the reviewed
    [value theorem](new-direction/coupled-polytope-core-value-oracle.md)
    and [core extension](new-direction/coupled-polytope-core-oracle.md)
    give expected `f_d(k)(1+alpha/sigma)^k poly_d(I+q)` evaluation
    on a bounded rational polytope when `F+alpha||v||^2/2` is convex
    there. The [convex interface](new-direction/convex-polytope-value-interface.md)
    derives a rational relative affine hull and inner ball, repairs weak
    outputs by rational LP, and supplies a tangent LP dual certificate.
    Whole-cell packing works even for a singleton core projection; the
    projected near-optimal set comes from a compact joint sublevel,
    without a continuity assumption on a partial value function.
    Separate [value](reviews/coupled-polytope-core-value-review.md),
    [interface](reviews/convex-polytope-value-interface-review.md), and
    [core](reviews/coupled-polytope-core-oracle-review.md) reviews passed.
    Root read the complete proofs and reviews, rechecked the constants,
    and identified a sign clarification in the compact projected-growth
    argument; the corrected `gamma=-(c+2epsilon a)` was independently
    rederived. The supplied `alpha` can substantially exceed the box
    theorem's `L`; fiber convexity alone is insufficient. The
    [focused comparison](prior-art/coupled-polytope-core-value-oracle-prior.md)
    credits classical alphaBB and Kannan--Rademacher's convex objective
    plus low-dimensional polynomial perturbation algorithm. The
    distinction is the fixed finite-law, all-precision certified bit
    guarantee; priority is not established.
68. **Exact QP output from core and value Cauchy names:** the reviewed
    [corollary](new-direction/qp-core-cauchy-reconstruction.md) proves
    expected exact rational optimization for the box PSD-residual model
    at the inherited `L` bound, and for the coupled convexifier model
    at the inherited `alpha` bound. A lexicographic optimizer is a
    vertex of its stationary-face polytope, giving uniform polynomial
    rational height without inverting a singular residual Hessian.
    After fixing the finite law, one polynomial-precision query and
    continued fractions recover its exact core and value; exact convex
    QP completes the fiber. A short rational face-enumeration fallback
    preserves expected postprocessing cost. Root read the completed
    proof and [arithmetic review](reviews/qp-core-cauchy-reconstruction-review.md),
    including the infeasible-candidate rejection correction. The
    coupled transfer received its own fresh check after item 67 passed.
    This is an interface and parameter consequence, not a claim of the
    first exact all-dimensional smoothed-QP theorem.
69. **Ordinary-polynomial selected coordinates for noisy convex objectives:**
    the reviewed [theorem](new-direction/joint-convex-core-point-oracle.md)
    returns a feasible rational point, certified value interval, and
    distance `2^-q` to one fixed optimal core in expected `poly_d(I+q)`
    work. The objective is jointly convex on a bounded rational polytope;
    only requested coordinates receive independent finite linear noise.
    A buffered near-optimal sublevel has a known relative inner ball.
    Exactly `2k` convex weak optimizations give outward coordinate bounds,
    whose diameter is an every-draw certificate. Failure at any precision
    lies in one small projected-growth event, paid for by the fixed law
    and exact fallback. There is no numerical inverse-noise or curvature
    factor; all magnitudes enter through input bit lengths. Root read
    the full [review](new-direction/joint-convex-core-point-oracle-review.md)
    and independently rechecked the homothety, GLS errors, diameter and
    common-event constants. Full optimizer-distance output requires
    perturbing every coordinate. The
    [prior comparison](prior-art/joint-convex-core-point-oracle-prior.md)
    separates ordinary convex value optimization from this selected-point
    guarantee and records the qualitative generic-tilt antecedents.
70. **Deterministic strong approximation for convex cubics:** the reviewed
    [box theorem](new-direction/convex-cubic-point-oracle.md) computes
    feasible rational points within `2^-q` of the optimizer set and of
    its fixed minimum-original-norm point in `poly(I+q)` bit time.
    Convexity on the supplied rational box is a premise; no global
    convexity, uniqueness or positive Hessian modulus is assumed.
    The affine Hessian has a common rational kernel. Cubic symmetry,
    an explicit integer-row Hoffman estimate valid for irrational
    offsets, and rational eigenvalue-height bounds give a computable
    polynomial-bit fourth-root error constant. An explicit Tikhonov
    schedule then selects the minimum-norm optimizer with only
    `poly(I)+O(q)` parameter bits. The
    [full review](reviews/convex-cubic-point-oracle-review.md) and
    [focused Hoffman review](new-direction/convex-cubic-point-hoffman-review.md)
    passed; root independently rederived the main constants and the
    saved canonical schedule. The quartic PosSLP construction gives
    a conditional contrast, not a proved complexity separation. External
    novelty remains unresolved in the
    [source audit](prior-art/convex-cubic-point-oracle-prior.md).
    The [general-polytope extension](new-direction/convex-cubic-polytope-point-oracle.md)
    also passed a [full review](reviews/convex-cubic-polytope-point-review.md)
    and a [focused preprocessing review](new-direction/convex-cubic-polytope-preprocessing-review.md).
    Its rational inball gives reflected Hessian domination, and all
    polytope normals enter the explicit Hoffman constant. Homothety
    restores exact feasibility after weak optimization. Root independently
    checked the complete proof, including the added affine-objective
    error constant and the explicit value-error budget.
71. **Full selected optimizer output for convexifiable cubics:** the
    reviewed [completion theorem](new-direction/cubic-core-full-point-oracle.md)
    strengthens item 67 to full Euclidean point distance, preserving
    `f(k)(1+alpha/sigma)^k poly(I+q)` expected work under the same
    finite core-only noise model. For a chosen optimal core `a`, the
    auxiliary convex objective `T_a=F_c+(alpha+1)||v-a||^2/2` has
    exactly that optimal fiber as its minimizer set. Rational Hessian,
    gradient and core rows give a polynomial-bit error constant uniform
    in the unknown irrational slope. Effective regularization selects
    the minimum-original-norm point in that fiber. Completion consumes
    only a short dyadic core approximation, including on rare fallback
    draws, preserving expected postprocessing cost. The
    [full](new-direction/cubic-core-full-point-independent-review.md) and
    [focused bit](reviews/cubic-core-completion-bit-review.md) reviews
    passed; root read both and independently checked the constants,
    zero-rank case, tied-core selector, perturbation budget and objective
    interval. Total degree three and the supplied joint convexifier are
    material assumptions. The
    [assessment](new-direction/convex-cubic-point-significance.md)
    distinguishes this full-point capability from the exact-QP baseline
    and the cubic exact-active-label and quartic point barriers.
72. **Effective strong approximation for globally convex polynomials:** the
    [fixed-degree theorem](new-direction/globally-convex-polynomial-point-oracle.md)
    proves `dist(x,S)<=Gamma gap^(1/D)` on a bounded rational polytope,
    with `Gamma` rational, polynomial-time computable and of polynomial
    bit length. It gives deterministic `poly_D(I+q)` approximation to
    the fixed minimum-norm optimizer. Global convexity on all of `R^n`
    is essential: interpolation controls the Bregman polynomial on an
    extrapolated line, and a global Jensen inequality bounds directional
    derivatives at rational sample points. A polynomial-size unisolvent
    grid makes those gradients a known rational matrix whose zero slice
    is exactly the optimizer set. RHS-uniform Hoffman bounds complete
    the effective estimate, even for irrational optima and lower-dimensional
    domains. The already-current core-completion transfer extends this
    to globally core-convexifiable fixed-degree objectives, preserving
    expected `f_D(k)(1+alpha/sigma)^k poly_D(I+q)` work and the one
    finite noise law. Two fresh reviews
    ([first](new-direction/globally-convex-polynomial-point-oracle-review.md),
    [second](new-direction/globally-convex-polynomial-point-scout-review.md))
    passed. Root independently checked the full proof and corrections,
    including explicit interpolation constants, the zero-gap argument,
    affine objectives, canonical schedule, short-core composition and
    zero-core branch. The
    [source audit](prior-art/globally-convex-polynomial-point-prior.md)
    identifies Li's constrained qualitative bound as a direct antecedent;
    it does not establish novelty of the effective constant. This
    direction began before the user's stop instruction and was completed
    within that instruction's allowed scope.
73. **A verifiable higher-degree convexifier class:** the reviewed
    [affine-power theorem](new-direction/affine-power-core-point-oracle.md)
    treats a supplied PSD quadratic plus positive rational weighted even
    powers of rational affine forms and an affine term. A direct scalar
    Bregman estimate controls rational affine-form residuals, giving a
    polynomial-bit `1/D` distance constant and the same full-point core
    completion. Its [review](reviews/affine-power-core-point-review.md)
    passed; root read the complete proof and review and rechecked the
    constants. This is now an explicit-certificate class of item 72,
    with a useful direct proof, rather than a second general theorem.
    It supplies and verifies a representation; no decomposition algorithm
    for arbitrary convex polynomials is claimed.
74. **Closed weaker residual-cubic exploration:** the reviewed
    [boundary note](new-direction/residual-convex-cubic-boundary.md)
    proves a fixed rational residual Hessian kernel on each relative
    core face. Only one optimizer-slice row varies, so every relevant
    minor has degree at most two. Supplied face/minor margins yield
    polynomial-bit fiber error constants. The examples `v z^2` and
    `gamma v-v^2 z` disprove a uniform fiber error constant and naive
    minimum-norm completion at approximate cores. They do not prove
    point-oracle hardness. The
    [independent review](reviews/residual-convex-cubic-boundary-review.md)
    and root passed the structural claims and corrected margin-bit
    accounting. An efficient margin certificate and a full smoothed
    point algorithm remain unproved. This line is documented and stopped.

The [nonlinear-frontier assessment](new-direction/nonlinear-frontier-significance.md)
independently separates the shared search mechanism from its polynomial
discovery, candidate-verification, and implicit-output consequences. It
ranked sparse smoothed polynomial optimization as the next higher-potential
target. Item 45 now supplies its finite-noise tail, exact same-draw fallback,
and output/evaluation proofs. Its deterministic boundary-certificate target
remains open; significance and practical implications continue to be assessed.

A complementary reviewed [strong-field theorem](new-direction/strong-field-component-qp.md)
uses strict coordinate monotonicity to pin bounds in mixed box QP. The
unfixed sites form independent random components. If their exact weighted
probabilities satisfy `4 Delta max_i(a_i q_i)<1`, component enumeration
has the displayed expected cost, including the reciprocal subcritical
margin. A sufficient stronger condition makes that margin at least one
half and gives expected polynomial work without a width or inertia
parameter. The noise must dominate interaction variation and integer
label counts; large capacities therefore impose a large numerical noise
requirement. Root read and checked the complete proof, singular-face
enumeration, review, and [source audit](prior-art/strong-field-component-qp-prior.md).
This is preserved as a distinct strong-noise result using standard
persistence and component-counting ingredients. It is not a general
improvement in the noise dependence. Item 58 now supplies the reviewed
fixed-degree polynomial extension with structured algebraic output.

Supporting work on the unresolved negative-curvature parameter includes
the reviewed [Jacobi/clipping calculation](new-direction/jacobi-copositive-residual.md)
and [articulation elimination baseline](new-direction/articulation-copositive-elimination.md).
Root read both complete proofs. The former exactly characterizes optimal
diagonal scaling of a supplied residual and preserves its margin under
positive-entry clipping; existence and discovery of a useful residual
remain open. The latter gives unconditional `2^p poly(I)` strict-copositivity
recognition for bounded biconnected-block size, including rational failure
witnesses. Fresh review checked singular supports, branching, and the
original-subtree determinant argument that controls bit lengths. Neither
is promoted as a new general treewidth algorithm or as an established
original contribution. The [focused prior audit](prior-art/articulation-jacobi-width3-prior.md)
identifies Ikramov's exact forest algorithm as the articulation theorem's
`p=2` baseline, and Bomze--Eichfelder's one-entry truncation as prior
copositivity-preserving clipping. The reviewed clipping note preserves the
exact growth value, which is a stronger conclusion. Johnson--Reams and
Bomze's later block criterion remain compared only through verified
abstracts; their missing full texts are explicitly recorded.

The [significance review](reviews/significance.md) treats the shared-grid
result as a meaningful conditioned algorithmic advance over the local
predecessor, with practical value unproved. Its product-domain and global
growth assumptions matter. The [oracle lower bound](geometric-dp/oracle-limits.md)
shows the conditioning exponent is unavoidable for a point-oracle model at
fixed dimension, using a classical hidden-well argument. It is neither an
explicit-polynomial complexity lower bound nor a novelty claim.

## Reviews and verification

The main shared-grid argument has an independent derivation and an
[adversarial proof review](reviews/geometric-dp-adversary.md). The tree
counterexample has a separate [adversarial review](reviews/tree-localization-adversary.md).
The arithmetic/model extensions, continuous regridding theorem, and its
inexact-oracle extension have also passed separate adversarial reviews. These
reviews are evidence, not journal peer review or formal proof checking.

Targeted commands actually run, by the research agents unless stated otherwise:

| Command | Result and scope |
| --- | --- |
| `python3 research-20261002/geometric-dp/checks/exact_checks.py` | Passed six analytic families and 42 stages; 142,348 full-grid assignments and 294 rounding laws checked in exact fractions. |
| `python3 research-20261002/geometric-dp/checks/grid_geometry_checks.py` | Passed 250 grids, 1,883 vertices, and 36 parameter cases. |
| `python3 research-20261002/geometric-dp/checks/float_scale.py` | Completed size/timing observations at 16, 64, and 128 variables; not certified bounds. |
| `python research-20261002/tree-localization/check_counterexample.py` | Passed finite matrix/formula checks through depth seven and evaluated large-depth amplification; no full finite-certificate DP enumeration. |
| `python research-20261002/regridded-certificates/check_core.py` | Passed 480 occurrence-tree drift checks, 500 constant cases, and 180 configurations including branching and boundary minima; floating-point algebra checks, not full DP verification. |
| `python3 -B research-20261002/new-direction/check_screening.py` | Passed 70 rational instances and 5,080 support bounds, with additional heterogeneous and boundary cases. |
| `python3 research-20261002/geometric-dp/checks/exact_box_qp_checks.py` | Passed 199 rational quadratic cases, including 30 mixed or integer cases; 5,931 continuous faces, 144 integer slices, 2,228 height checks, and 199 value plus 505 coordinate reconstructions. A separate analytic fixture handles an integer interval of more than `2*10^80` values without enumeration. |
| `python3 research-20261002/geometric-dp/checks/exact_nonunique_qp_checks.py` | Passed recovery of eight optima in continuous and mixed variants, 384 anchor rounds, 896 source grids, and 12,715 coordinate checks, plus rational correction/factor/message divisibility. |
| `python research-20261002/geometric-dp/checks/regridded_affine_checks.py` | Passed 20,340 shell boxes, ten successive centers, 714 corner minima including 40 ties, 494 intersections, and 310 Taylor probes; checks local arithmetic invariants rather than full DP execution. |
| `python3 research-20261002/new-direction/projection_anchor_checks.py` | Passed nine rational continuous double-well runs, one exact integer run on a 2,049-value interval using 513 final nodes, and six irregular-grid diagonal-obstruction checks. |
| `python research-20261002/new-direction/check_affine_repair.py` | Passed 24 dynamics matrices and 240 locally feasible copied configurations; floating-point checks of repair, multiplier cancellation, and error bounds. |
| `python research-20261002/reviews/affine-repair-review-check.py` | Passed 300 exact rational configuration identities and repair/drift bounds, plus the example's reduced nonconvexity calculation. |
| `python3 research-20261002/new-direction/check_nonlinear_dynamics.py` | Passed 200 exact rational configurations, including 632 nonzero graph residuals and 439 copy mismatches; all telescoping residuals were exactly zero. |
| `python3 -B research-20261002/new-direction/check_core_box_bb.py` | Passed 14 adaptive core-refinement instances, 930 boxes, and 855 exact residual calls; compared every level's bounds to full active-face enumeration. Includes aspect ratio 1,024, indefinite residuals, continuum residual optima, and zero positive core curvature. This is a small reference implementation, not the cited forest oracle. |
| `python research-20261002/new-direction/check_pruned_grid.py > research-20261002/new-direction/check_pruned_grid-results.json` | Passed nine instances and 70 adaptive stages, with 26,589 bag states and 526 filtered intervals. Every coordinate min-marginal was compared against 21,034 exhaustive assignments on nine reference grids and an explicit two-bag trace, not on every adaptive grid. Stage checks separately cover objective reconstruction, bag agreement, global bounds, contraction, and retained centers/incumbents. The unknown-growth cap, exact recovery, and a standalone history verifier are proved and reviewed but not implemented in this checker. |
| `python research-20261002/new-direction/check_spectral_normalization.py` | Passed 12 exact rational matrix cases and 29 rotations, including singular mixed inertia, repeated negative eigenvalues, and an ill-conditioned oblique range. Separate reviewers checked 196 rotation blocks and three additional small-norm matrices. |
| `python research-20261002/new-direction/check_convex_modulator.py` | Passed seven refinement levels and 13 exact slab solves at a nondyadic optimum, plus inertia/deletion and dense-residual examples. Fresh review separately tested a lower-dimensional polytope with flat residual directions, premature reconstruction rejection, and exact Fenchel recovery. |
| `python research-20261002/new-direction/check_negative_inertia_qp.py` | Passed five fixtures and ten actual B&B runs, with 416 distinct auxiliary calls, 428 cells, 259 pruned cells, and four premature reconstruction rejections. All approximate gaps were at most `1/4096`. Uses a small exhaustive active-face reference oracle and fixture-specific height bounds; does not implement the general polynomial-time convex oracle or general height computation. |
| `python research-20261002/new-direction/check_approximate_recourse.py` | Passed 100 integer-oracle comparisons to exhaustive enumeration, a mixed quartic run with 82 calls over ten levels, and exact pure integer recovery on an interval containing `2^40+1` integers with 166 calls over 41 levels. These are validation fixtures, not competitive benchmarks. |
| Inline exact-arithmetic Python checks recorded in `new-direction/negative-inertia-miqp.md` and its review | Passed 242 growth comparisons, 399 cell/lift checks, 11 corner calls, 12 retained-cell checks, and two premature reconstruction rejections. Recovered a nondyadic optimum at level four. A continuous-relaxation countercheck confirms the need to retain integrality in recourse. |
| Inline exact-arithmetic Python checks recorded in the proximal grid and recovery notes | The grid fixtures passed 36 stages, 2,661 assignments, and 72 nearest-optimum containment checks. Author recovery checks covered 16 cases across eight families; fresh review covered 37 snapping cases, 112 stationary-polytope vertices, and 20 extra snaps. These are small reference checks, not a general polynomial-time implementation. |
| `python research-20261002/new-direction/check_expected_smoothed_qp.py` | Five exact fallback fixtures passed. This verifies candidate enumeration on those examples, not the full adaptive solver or an empirical expected-runtime claim. |
| `python research-20261002/new-direction/check_polytope_recovery_review.py` | Eight exact recovery cases passed, with 13 stationary vertices, ten recovered vertices, and four extra snaps. Includes redundant rows, lower-dimensional constraints, coupled facets, and disconnected optimal faces. |
| `python research-20261002/new-direction/check_smoothed_cells.py` | Passed 30 exact-rational lower-envelope instances in dimensions one through four, 120 levels, 928 cells, 13,056 corner calls, and 17,630 complete-grid nodes. Checks local bounds, global gaps, and survivor incidence; the expectation theorem rests on its probability proof. |
| `python research-20261002/new-direction/check_smoothed_cells_review.py` | Independent exact checks passed six levels and 81 noise vectors on a nonsmooth two-dimensional example with unequal widths: 1,425 near-optimal events, 1,287 necessary-interval checks, 3,979 processed cells, and 1,414 survivors. Does not establish an expected-runtime benchmark. |
| `python research-20261002/new-direction/check_proximal_polytope_fenchel.py` | End-to-end exact reference diagnostic passed 310 proximal stages, 6,416 recourse calls, and final face recovery on two disconnected optimal segments with coupled and redundant constraints. Uses a supplied growth bound and small-instance reference oracles. |
| `python research-20261002/new-direction/check_smoothed_cell_closure.py` | Passed 13 fixtures, 45 levels, and 629 cells: 168 exact closures, 365 ordinary prunes, and five same-draw fallbacks at deliberately small caps. Checked 110 active-basis formulas and 96 gradient-image implications, including coupled rank three. The recourse oracles are fixture-specific reference implementations. |
| `python research-20261002/new-direction/check_exact_cell_closure_review.py` | Independent exact checks passed four degenerate fixtures and 208 corner queries, with 34 closures and 52 unresolved retained cells. Includes lower-dimensional critical regions and an endpoint noise atom that requires the fallback. |
| `python research-20261002/new-direction/check_smoothed_integer_low_rank.py` | Passed 124 exact recourse comparisons, one interval `[-2^100,2^100]` with known optimum `2^80`, and 756 lattice-value checks. Seven cell fixtures covered 73 draws, including 15 ties, 448 levels, 2,437 cells, 8,434 corner calls, and 246 further lattice checks. All final witnesses matched exhaustive small-instance optima; these are correctness fixtures, not runtime benchmarks. |
| `python research-20261002/new-direction/check_ambient_noise_review.py` | Independent exact checks passed 84 complementary-minor identities, 14 ambient-normal pullbacks, 27 local-event line sections with 81 finite-grid discrepancy checks, and 27 polygon-area probability comparisons. These validate the new geometry and finite-noise lemmas on fixtures, not a full ambient solver or a runtime benchmark. |
| `python research-20261002/new-direction/check_integer_label_isolation.py` | Root's exact enumeration passed eight fixtures, 2,112 noise draws including 247 ties, 558 conditional line envelopes, 4,151 breakpoint witnesses, and 40 probability comparisons. Checks the elementary isolation ingredient for the mixed-integer extension; it is not a solver benchmark. |
| `python research-20261002/new-direction/check_gaussian_cells.py` | Passed 108 numerical weighted-lattice fixtures, four exact covariance/frame identities, 18 rational exponential-weight checks, 12 enumerable finite-law analogues, and three exact support/precision budgets. The last used a 1,000-bit curvature bound. These test probability and sampling ingredients, not the full QP solver or an infinite Gaussian sum by enumeration. |
| `python research-20261002/new-direction/check_smoothed_miqp_closure.py` | Passed 23 exact coupled mixed fixtures, 134 levels, 463 cells, 90 whole-cell gap closures, 152 prunes, 137 gap-event implications, and 84 continuous-region implications. Rejects a matching-corner-label counterexample and tests same-draw fallback with a deliberately zero cap. Uses small explicit slice oracles. |
| `python research-20261002/new-direction/check_mixed_separable_closure.py` | Passed ten exact mixed fixtures, 34 levels, 174 cells, 34 closures, 93 prunes, and four fallbacks at small caps. Checked 25 active-witness upper models at a nonsmooth tie, 47 gradient-image implications, and a `2^40+1`-value integer interval solved in 40 binary-search comparisons. Final optima matched independent small-instance enumeration. |
| `python3 -B research-20261002/new-direction/check_sparse_bag_cells.py` | Passed five instances and 16 stages, with 2,295 exact min-marginals, 2,807 rounding atoms, 392 retained witnesses, 951 removed cells, and three exact closures, plus a boundary-only fixture. Uses exhaustive small grids and face enumeration as independent references. |
| `python3 -B research-20261002/new-direction/check_sparse_bag_noise.py` | Passed eight exact finite-noise cases and 238 bag tuples, including 45 empty coefficient intervals. Checks the necessary local-event and probability bounds, not asymptotic runtime. |
| `python research-20261002/new-direction/check_gaussian_miqp_budget.py` | Passed six synthetic rational-bound fixtures and 63 exact support-budget trials, including the sharp `J(t)=J(0)+2t` growth case, a 1,000-bit curvature bound, and large integer ranges. Tests budget arithmetic, not the optimization oracle. |
| `python research-20261002/new-direction/check_gaussian_miqp_review.py` | Independent checks passed five complete weighted-law fixtures, 3,333 exact draws, 84 ties, and 20 scalar isolation bounds, including an optimized continuous variable for each label. Rational event counts use a conservative analytic Gaussian-CDF discrepancy bound; this is a small law, not the theorem's finer sampler. |
| `python3 -B research-20261002/new-direction/check_sparse_mixed_bag_cells.py` | Passed four mixed instances and 19 stages: 444 min-marginals matched exhaustive grid references, 1,171 rounding atoms stayed feasible, 151 retained witnesses met the bound, 115 cells were removed, six integer fixes were sound, and three cases closed exactly. Includes a tied PSD case that correctly remains unclosed. The shared checker changed, so the continuous regression was rerun and passed. |
| `python research-20261002/new-direction/check_anisotropic_gaussian.py` | Passed four exact normalizations, four rational Jacobi rotations, 120 anisotropic grid levels, 169 interior interval bounds, and 91 inactive-coordinate cases, including a 200-bit curvature ratio. Checks normalization and mesh ingredients, not a full sampled solver. |
| `python3 -B research-20261002/new-direction/check_box_preordering_growth.py` | Passed five rational principal minors and the negative separator, eight connected chains with 36 restrictions, 1,024 growth identities, 9,216 connected-flat cases, all 46,376 degree-30 multiplier coefficients, and 1,281 independently expanded coefficient identities. The all-degree nonmembership conclusion rests on the local-jet proof. |
| `python3 -B research-20261002/new-direction/check_geometric_copositive.py` | Passed six positive fixtures, ten positive search trials, 39,908 exact bag assignments, ten positive-grid comparisons with exhaustive enumeration, 1,330 variance checks, six boundary/negative checks, and four refined negative-witness trials. Includes a branching decomposition, a `10^50` cross coefficient, and the non-SPN example. These are finite certificate diagnostics, not performance benchmarks. |
| `python research-20261002/new-direction/check_geometric_box_point.py` | Passed five positive normalized-metric fixtures, seven search trials, 50 exact rounding identities, 150 radial certificate probes, and two nonunique cases. Independent review separately checked 69 certificate/radial probes and 163 rounding atoms. This predecessor retains its stated metric and scale limitations. |
| `python3 -B research-20261002/new-direction/check_mixed_shell_certificate.py` | Independent review ran the final exact diagnostic: 1,276 scalar rounding cases, 156 mixed-shell/inner-radial cases, 289 endpoint/scale cases, and three obstruction families passed. The checker enumerates small shell grids; it does not implement the sparse mixed OR-DP. The author also ran the script with `python`. |
| `python research-20261002/reviews/check_mixed_shell_review.py` | Separate review passed 47 full shell-DP comparisons with exhaustive enumeration, two threshold-necessity fixtures, and 162 endpoint-growth checks. A `2^40` side ratio used at most 14 coordinate labels; a `2^200` cross/linear coefficient retained `L=2`. These are finite implementation checks, not general runtime benchmarks. |
| `python3 -B research-20261002/new-direction/check_geometric_product_face.py` | Passed six finite certificates from 208 endpoint-grid entries, 70 exact rounding identities, 280 radial growth checks, 18 two-label reductions with 81-bit endpoints, and 378 further mixed-fiber/inner-region cases. Includes a free integer interval with over one million labels. This checker enumerates small tables and rounding laws; it does not implement sparse DP. |
| `python research-20261002/reviews/check_psd_extraction_dual.py` | Independent review checked the universal rational PSD dual identity, 31 principal minors, 77 exact acceptance-threshold implications including `d=2^200`, and three actual grid counts. Separate exact inline diagnostics checked 500 Horn-ray equalities, 100 signed-ray identities, 1,000 growth samples, and 100 sign-changing-residual witnesses. Universal conclusions rest on the matrix proof. |
| `python3 -B research-20261002/new-direction/check_nonlinear_shell_certificate.py` | Author and independent reviewer ran the exact diagnostic: six positive fixtures in seven trials, three rejected wrong-candidate trials, 49 sparse DP tables matching exhaustive minima, 2,154 bag assignments, 145 rounding cases, and 66 core cases passed. A separate reviewer diagnostic passed 495 sequential-rounding cases and 1,141 atoms, including 314 cases with genuine higher-order expectation terms. These are correctness fixtures, not solver benchmarks. |
| `python3 research-20261002/new-direction/check_implicit_optimum_precision.py` | Passed 120 rational configurations at horizons 1, 2, 3, 5, and 8; 45 rectangular sign checks; recurrence/denominator checks; both conditioning ratios; and exact shifted-Hessian certificates on those configurations. The exponential-size statement is proved for every horizon, not inferred from these tests. |
| `python3 -B research-20261002/reviews/check_implicit_convex_patch_review.py` | Independent review passed three exact closed-box Hessian certificates in dimensions 5, 10, and 18 using endpoints of at most 12 denominator bits. All three boxes fail the separate terminal active-gradient sign test. A mixed fixture checked that individual-label filtering removes the integer unit-interval halo. These test the added closure steps, not a full polynomial pruning implementation. |
| `python research-20261002/reviews/check_fan_preordering_review.py` | Independent exact review checked the Horn congruence, LDL reconstruction and five positive pivots, the full interaction graph, five chain decompositions with 119 bags, 31 restricted separating traces, and the growth/curvature formulas. The arbitrary-degree conclusion rests on the origin-jet proof, not degree enumeration. |
| `python research-20261002/reviews/check_articulation_review.py` | Independent exact review passed four support edge cases, 12 shared-articulation stars, nine chains up to 64 edges, 14 lifted nonpositive witnesses, and one early private-block failure with reverse lifting. Includes singular strictly copositive private matrices and a positive residual `2^-80`. These fixtures test the elimination contracts; the universal bit bound rests on the original-subtree proof. |
| `python3 -B research-20261002/new-direction/check_smoothed_sparse_polynomial.py` | Passed six sparse quartic stages on a mixed path with bag size two: 126 bag min-marginals matched exhaustive allowed-grid minima, 27 retained witnesses met the bound, and 42 cells were removed soundly. Checked 12 rounding atoms, 117 growth points, and 54 genuinely nonlinear cross-term rounding cases. Closure fixed an integer and an active continuous bound before certifying the remaining Hessian; the original continuous Hessian is indefinite. Does not implement the sampler, algebraic fallback, or ellipsoid evaluator. |
| `python research-20261002/reviews/check_smoothed_polynomial_review.py` | Independent checks passed four exact budget fixtures, including cutoff depth 3,433 and 4,006 noise bits, verifying both probability allocations, fallback payment, atom corrections, and closure thresholds. Three finite laws include an actual atom with a whole interval of optima requiring fallback; three further cases check GLS feasibility cleanup, including a 200-bit thin box. These are finite arithmetic checks, not an experimental proof of expected runtime. |
| Inline exact-`Fraction` star calculation recorded in `local-error-recourse-interface.md` | Checked nine bag rows, the grid incumbent, and the optimizer-containing cell. The local budget `1/8` is insufficient for its min-marginal `23/32`; the original global budget `33/16` is sound. The connected state-count lower bound is an all-noise algebraic proof, not an empirical runtime claim. |
| `python research-20261002/reviews/check_deterministic_boundary_output.py` | Author and reviewer passed four symbolic identities, 100 rational bisections isolating the one-link secondary local minimum, and 243 enclosure-budget fixtures. These check the new algebra and stopping thresholds, without rerunning the predecessor DP. |
| `python3 -B research-20261002/new-direction/check_convex_active_set_radicals.py` | Author checks passed 14 construction fixtures including a 400-bit radicand, 54 decomposition bags, 14 exact LDL/curvature certificates, and 12 perfect-square KKT comparisons including equality. Independent review checked the arbitrary-radical proof without rerunning this diagnostic. |
| `python3 research-20261002/new-direction/check_polynomial_graph_constraints.py` | Author and reviewer passed 1,125 exact rounding/curvature cases, a depth-two overlapping decomposition, and three finite-noise obstruction fixtures. The inherited sampler, fallback, and convex evaluator are not implemented by this diagnostic. |
| Inline exact-rational constraint reduction check recorded in `constrained-smoothing-barrier.md` | Checked 103 SUBSET SUM instances from six weight lists, every binary assignment, feasible state bounds, and the uniform objective separation. Found 60 feasible nonzero labels. The general reduction rests on the proof. |
| `python3 -B research-20261002/new-direction/check_simplex_sparse_dp.py` | Author checks passed eight stages, 513 exact min-marginals matching exhaustive compatible assignments, 140 retained witnesses, 267 removals, 20 feasible rounding atoms, and 336 growth probes. Closure fixed an integer, a tight budget, and a zero coordinate before certifying the tangent Hessian. This is a correctness fixture, not a benchmark. |
| `python3 -B research-20261002/reviews/check_simplex_patch_review.py` | Independent review passed 668 exact finite-noise draws, 154 face/multiplier bounds, 75 zero-multiplier incidences, three rational interior balls, and 27 exact projection/KKT checks, including a 200-bit thin equality patch. These checks target the new probability and evaluator interfaces. |
| `python research-20261002/reviews/check_box_stable_recourse.py` | Author checks passed four noisy nonconvex-forest fixtures, 20 exact excluded-slab solves, original-bound clipping and tied-mode guards, and three base-only finite-law budgets including extreme rational scales. The fixture uses face enumeration as a reference oracle, not an implementation of the forest algorithm. |
| Inline `python - <<'PY'` exact recourse review diagnostic, seed `2026100217` | Independent review checked 600 rational two-variable QPs. All 548 successful localization and uniform-gradient/PSD closures matched the exact optimum; 11,508 sampled conditional slices stayed in their certified patches. Separate counterexamples show why center-only gradient tests and continuous derivative signs for binary variables would be unsound. |
| `python research-20261002/new-direction/check_smoothed_implicit_graph.py` | Author checks passed five approximate-DP stages on a cubic-actuator instance: 296 lower-cost min-marginals matched brute force, 82 retained witnesses met the true `4E` bound, and 120 cells were removed soundly. Checked 18 rounding atoms, 81 real-hull root brackets, 326 nonpoint brackets, and 18 separate nonzero-dependent-noise value refinements; verified reduced Hessian at least `2I` after mode fixing. Independent code inspection passed. DP/closure used zero noise; noisy pruning, GLS, and fallback were not implemented. |
| `python research-20261002/reviews/check_implicit_graph_tail_kkt_review.py` | Independent review checked 36 exact KKT determinant fixtures, a nonlinear graph root, 16 finite-law strips, and a degenerate singular case. These check the graph/KKT interface rather than the generic elimination algorithm. |
| `python3 -B research-20261002/new-direction/check_order_polytope_review.py` | Independent checks passed 297 finite-noise draws, 969 forced equalities, 494 active-gap checks, 213 zero-gap incidences, 6,831 gap-Lipschitz checks, 275 face/proposal probability comparisons, and 1,754 feasible common-threshold rounding atoms. Chain, fork, and cycle fixtures use exact reference enumeration; no full sparse expected-work solver is implemented. |
| `git diff --check -- research-20260929/theory-decomposition/adaptive-matching.md` | Passed after root added the scoped conjecture update. |
| `python3 -B research-20261002/new-direction/check_native_integer_recourse.py` | Author checks completed nonlinear flow/core refinement at capacities `7` and `2^80+7`, with at most four retained cells and 118/849 exact recourse calls. All 967 calls passed residual-potential certificates. Verified exact algebraic point/value representations and a flat-core case where label exclusion succeeds but positive-Hessian closure cannot. Uses a scalar reference flow oracle, not the general TU algorithm or finite-law sampler. |
| `python research-20261002/reviews/check_native_integer_recourse_review.py` | Independent checks passed 1,215 label-gap tests, 2,430 restricted exact enumerations, and 5,040 endpoint comparisons covering 420 valid whole-interval certificates. Separate 1-, 23-, and 200-bit width budgets and algebraic point/value enclosures at 8/32/96 bits passed. These tests validate mechanisms and arithmetic, not asymptotic performance. |
| `python research-20261002/reviews/check_core_only_strong_recourse.py` | Author checks passed four nonlinear core-only closure fixtures, 14 excluded slabs, 538 rational bisections, 27 growth lifts, and two patches clipping a residual optimum with 400-bit interior distance. Demonstrates why a numerical interior-slack premise is unnecessary; no full ellipsoid or fallback implementation. |
| `python research-20261002/reviews/check_core_only_boundary_recourse.py` | Author exact checks passed two weak-multiplier releases, three sound residual fixings, seven changing-pattern/KKT cases, a core-vertex closure with indefinite ambient Hessian, and nine three-event finite-law budgets through 400-bit fallback factors. Independent composition review checked the general proof without rerunning the fixture. |
| Inline exact checks recorded in `core-noise-active-stratum-tube.md` and `small-residual-multiplier-curvature.md` | Authors checked six tube/jitter identities and 600 one-dimensional finite-grid cases, plus derivative, multiplier, Young-inequality and restored-modulus identities. These do not experimentally verify the higher-dimensional tube theorem; its primary source and application were read independently. |
| Inline symbolic and exact-rational checks recorded in `regularization-point-precision-obstruction.md`, `core-only-noise-regularization-limit.md`, and `canonical-convex-fiber-regularization.md` | Authors checked the quartic Hessian and regularized stationarity identities for dimensions 1–5, chain bounds for dimensions 1–8, 72 precision thresholds, 13 moving-core schedules, 240 interpolation/regularization cases, and two coupled stationarity identities. Root and an independent reviewer checked the general proofs separately. These are method counterexamples and conditional bounds, not optimization benchmarks. |
| `python3 -B research-20261002/new-direction/check_polynomial_primitive_limit.py` | Author's exact-rational diagnostic passed seven systems, nine forms, eight finite limits and ten quotient-matrix relations. Includes nonradical and positive-dimensional cases, escaping branches, a pole-hiding rejection, a feasible spurious candidate and exact algebraic value comparison. It is not the full general solver or a complexity benchmark. |
| `python3 -B research-20261002/new-direction/check_strong_field_polynomial.py` | Author and independent composition reviewer passed 388 exact comparisons, 864 pins, 81 threshold equalities, 18 split draws, 489 derivative probes, 29 rational refinements and 34 weighted bad-site patterns on four graphs. A shared exact separable-cubic oracle checks composition, not the general algebraic solver; sampled derivative probes supplement the full interval proof. |
| `python3 -B research-20261002/new-direction/check_interior_core_flow.py` | Author checked eight noise atoms on one- and 80-stage networks, including `2^79` persistent tied winners: 480 oracle queries, 10,535 interval sign tests and 10,363 identity costs passed. Regular draws closed by level three; endpoint atoms with two optimal cores exercised the failure branch. Uses analytic flow classes, not general flow optimization or full label enumeration. |
| `python research-20261002/reviews/check_interior_core_flow_charts.py` | Independent cyclic-network checks passed 205 charts, 104 interval certificates, 1,768 competing-flow comparisons, 683 identity reduced costs and 33 tied optima. Tests forward/reverse arcs and arborescences through tight zero-cost cycles. |
| `python3 -B research-20261002/new-direction/check_convex_point_radicals.py` | Author checked 11 exact source comparisons, seven decompositions with 190 bags, and 35 endpoint/tie cases, including 1,000-bit positive amplitude scales. These fixtures supplement the symbolic reduction; they do not solve general Square Root Sum. |
| `python research-20261002/reviews/check_convex_point_radical_review.py` | Independent amplifier checks passed 80 Hessians, all 560 principal minors, 2,160 directional identities/bounds, five singular cases and endpoint tests through 200-bit amplitudes. The amplitudes test the formulas; they are not computed optimizers of specific difficult source instances. |
| Inline exact checks recorded in `canonical-selector-radical-comparison.md` | Author checked five symbolic identities and 80 optimal-set fixtures, including a 400-bit positive amplitude. The independent review and root checked the proof separately; this narrower family permits easy selection of some optimizer while its minimum-norm selector contains the comparison. |
| `python3 -B research-20261002/reviews/check_flow_face_review.py` | Independent certificate checks passed 703 feasible tightened boxes, 3,942 exact proximity comparisons, and 54 derivative/Taylor checks. Covers directed cycles, self-loops, sharp distance factors, two-label interpolation, tied winners with different normal derivatives, and the outside-label guard. These are static certificate fixtures. |
| `python3 -B research-20261002/new-direction/check_boundary_core_flow_search.py` | Author checked all 64 atoms of an eight-point two-core noise law: 60 boundary closures, including 16 persistent-tie closures, and four same-draw fallback cases. Checked 1,428 cells, 1,099 potential/interval sets and 120 accepted face inequalities. Uses exact two-label quadratic reference formulas, not the general flow oracle, elimination routine or sampler. |
| Inline exact `Fraction` diagnostic recorded in `smoothed-bilinear-core-flow-review.md` | Independent review passed 125 cube-restricted affine zero-distance inequalities and 50 empty-zero-set vertex bounds, including boundary-only zeros and 80-bit data. A separate arithmetic reviewer checked polynomial sampling precision and output bounds. No flow-search fixture was repeated. |
| `python research-20261002/reviews/check_posslp_gate_review.py` | Independent new-gate checks passed four signed/zero circuit fixtures, 41 normalized pairs, 447 local vertex bounds, 688 derivatives and 32 exact normalized Hessian LDL checks. The previously checked quartic comparison mechanism was not retested. These validate identities and bounds, not general circuit-sign computation or optimizer performance. |
| Inline exact grid diagnostic, saved as `research-20261002/new-direction/check_core_value_grid.py` | Independent review passed 108 refinement stages, 5,656 cell lower bounds and 2,131 sound prunes. Checks approximate-corner intervals and feasible witnesses against exact small references. The saved script records the previously executed inline diagnostic; it was not rerun merely to persist the file. |
| `python research-20261002/reviews/check_core_value_cap_review.py` | A separate reviewer checked 18 finite laws, 7,154 exact draws and 108 threshold-tail bounds, including zero-growth endpoint atoms. Tests capped moments and fallback payment; the fixture's zero-curvature objective would use the theorem's direct endpoint branch, so this is not a full algorithm simulation. |
| `python3 -B research-20261002/new-direction/check_core_tu_recourse.py` | Author checked 495 TU minors, preprocessing correspondences, 24 recourse queries, 166 exact optimal-interval sets, 1,188 proximity bounds, 1,158 conformal circuit steps and 7,840 symbolic marginal evaluations. Covers signed and rank-zero matrices, tied optima, box-active dual bases and charts invalid away from their query. Independent review inspected the checker without rerunning it. |
| `python3 -B research-20261002/new-direction/check_all_scale_core_geometry.py` | Author checked four fixtures, 1,030 near-optimal nodes, 7,770 padded Fenchel/inverse-gradient inequalities, 15 maximum-simplex packing bounds, two signed QR witnesses and a singular pushforward-measure case. Includes nonlinear wells, tied noise atoms and dimension three. Exact rational geometry checks supplement the proof; they do not implement the general recourse solver or quantifier elimination. |
| `python3 -B research-20261002/new-direction/check_core_hull_oracle.py` | Author checked five fixtures and 35 stages, including six stages retaining an old incumbent, 24 sound value/core outputs, 116 rejected diameter tests and 48 combined-law budgets. Covers tied endpoints and flat optimal cores. The distinct diagnostic checks the new output contract, not the algebraic fallback. |
| `python research-20261002/new-direction/check_continuous_core_value.py` | Author checked 33 levels, 417 cells, 63 nested coefficient prefixes, 16,716 corner/completion bounds, 2,466 cell lower bounds, 1,390 near-optimal witnesses and 144 global prefix certificates. Dimensions one through three include a quartic residual with zero optimal Hessian and both encodings of dyadic coefficients. These exact tests concern the continuous-bitstream comparator, not the finite-law sampler. |
| `python research-20261002/new-direction/check_coupled_polytope_cells.py` | Author checked 108 levels, 391 generated cells, 337 tangent LP duals, 246 noncorner witnesses and 108 global value intervals. Another 81 error-box repairs checked coupled feasibility and core/value accuracy through 200-bit requests. Includes relative dimensions zero through two and a 101-bit thin domain. Uses exact small face enumeration, not general GLS or quantifier elimination. |
| `python3 -B research-20261002/new-direction/check_joint_convex_core_hull.py` | Author checked 36 fixtures, 108 buffered-sublevel ball points, 216 weak-extremum enclosures and 36 certified hulls. Includes five core coordinates, 100-bit thin diagonal polytopes, 40-bit accuracy and slightly infeasible weak outputs. These test the coordinate certificate, not a general convex solver or fallback. |
| `python3 -B research-20261002/new-direction/check_convex_cubic_point_oracle.py` | Author-side diagnostic owner checked eight fixtures: 1,050 cubic-symmetry/gap identities, 465 fourth-root distance bounds, 546 optimizer-slice equivalences, 24 precision scales, 162 irrational-offset Hoffman bounds and 216 nonunit/fixed-coordinate normalization checks. Includes a 101-bit affine-kernel slope and counterexamples to omitting the gradient row or demanding quadratic growth. Reviewers and root checked the general proof separately without duplicating the fixture. |
| `python3 -B research-20261002/new-direction/check_convex_cubic_polytope.py` | Author-side diagnostic owner checked six affine-hull fixtures, 24 universal-row classifications, four inball LP vertices, 45 reflection/Hessian bounds, 810 exact feasible repairs, 1,080 general-row Hoffman bounds and 91 original-norm embedding comparisons. Includes an oblique triangle where the cubic is not convex on its bounding box. Uses small enumerated LP bases; the box identities were not duplicated. |
| `python3 -B research-20261002/new-direction/check_cubic_core_completion.py` | Author checked three irrational-core fixtures in exact radical arithmetic: 60 rational-row checks, 42 lifted error bounds, nine actual rational completion solves and tangent certificates, nine perturbation budgets, five tied-core selector checks and 12 rank-zero checks. Short core vectors used up to 297 dyadic denominator bits. Tests composition, not a general core oracle or stochastic runtime. |
| `python3 -B research-20261002/new-direction/check_global_convex_point.py` | Root's distinct exact diagnostic passed 168 interpolation checks for degrees 2–5, 84 derivative reconstructions/bounds, 2,165 unisolvent entries, 72 Bregman extrapolations, 1,680 global Jensen checks, 420 sampled-gradient residual bounds and 175 zero-gap invariance checks. A four-variable quartic with one flat direction tests sample points outside the feasible box and large extrapolation parameters. This checks new proof ingredients, not a general convex optimizer or the canonical solver. |
| `python3 -B research-20261002/new-direction/check_affine_power_point_bounds.py` | Author checked 2,500 scalar Bregman inequalities, 16 rational root bounds including 101-bit small weights, and 252 canonical completion budgets through 80-bit requests. The general proof and output composition received a separate actual-file review; no general optimizer was implemented. |
| `python research-20261002/reviews/check_polynomial_box_recourse.py` | Author checks passed a genuinely nonlinear convex-residual fixture with a provably irrational optimizer: five excluded slabs, 109 exact rational bisections, four directly checkable tangent certificates, and closure at stage 42. Includes wrong-bound-direction and empty-core guards. The fixture uses rational bisection, not an implementation of GLS or the full core search. Root and a separate reviewer checked the proof independently without rerunning this fixture. |
| Inline `python3 - <<'PY'` rank-separation checks recorded in `polynomial-recourse-rank-separation.md` | Author checked 15 exact rational endpoint/interior inequalities across five residual dimensions and three coupling scales. The rank lower bound and entropy-correction caveat were checked algebraically by independent researchers, including root. |
| `python3 -B research-20261002/new-direction/check_mixed_order_transport.py` | Author checks passed 2,187 exact triangle minima from 729 finite-noise draws on three meshes, 8,019 transported central differences, 100 noise-interval tests, 2,433 near-optimal tuples, three complete-law count bounds, and 138 rounding checks. Uses an exhaustive analytic triangle reference, not the full sparse algorithm. |
| `python research-20261002/reviews/check_mixed_order_transport_review.py` | Independent checks passed 238 transports, 42 directional curvature comparisons, and 40 binary-preserving repairs. Verified nonconvex projection and premature-exposure counterexamples. These distinct tests do not implement fallback or establish general complexity. |
| `python3 -B research-20261002/new-direction/check_strong_field_components.py` | Author and reviewer checked 324 component-versus-whole optimization comparisons, 96 bad-site patterns, three exact expected-cost bounds, and two known singular fixtures. The same enumerator is used on both sides, so that comparison validates persistence and separation. Separate reviewer calculations covered eight weighted component expectations, including 81-bit integer-label counts. |

The agents' own notes preserve smaller inline algebra and enumeration checks.
Root also ran an inline Markdown check restricted to `research-20261002`:
102 local links resolved initially; after subsequent additions, a second
scoped scan resolved 194 links with no trailing whitespace. Those counts
refer to the files present at each scan. Code fences were excluded from
link parsing. Root's scoped `git diff --check -- README.md
research-20260929/theory-decomposition/adaptive-matching.md` also passed.
After the later additions, root checked 97 topic Markdown files and 384
local links. The first scan found one incorrect relative link to the
convex-QP literature package; after correcting it, all links resolved and
no trailing whitespace remained. These are document checks only.
After the ambient, Gaussian, mixed, and sparse additions, root's scoped
scan checked 142 topic/index Markdown files and 899 local file links;
all resolved and no trailing whitespace remained. An intermediate scan
had encountered one review link whose target was still being written;
the completed-note scan resolved it. The scoped tracked-file
`git diff --check` also passed again. No mathematical tests were repeated
solely for these documentation updates.
After items 34--36, root checked the four indices and six associated
theorem/review files: all 508 local file links resolved and no trailing
whitespace remained. The first parser also matched a mathematical product
as a link; restricting it to file extensions removed that false positive.
The same scoped tracked-file `git diff --check` passed. These were document
checks, with no repeated mathematical tests or CI checks.
After items 37--44, root checked 19 selected index, theorem, review, and
prior-art files: all 580 local file links resolved and no trailing
whitespace remained. The scoped tracked-file `git diff --check` also
passed. No mathematical test was repeated solely for those index updates.
For item 45, root checked 16 selected index, theorem, review, and prior-art
files: all 612 local file links resolved and no trailing whitespace
remained. The scoped tracked-file `git diff --check` passed again. Root
also read the actual GLS weak-optimization definition and source interface
when independently checking the feasibility repair. Mathematical
diagnostics were not repeated solely for the documentation update.
For items 46--48, root checked 15 selected index, theorem, review, and
prior-art files: all 609 local links resolved and no trailing whitespace
remained. The scoped tracked-file `git diff --check` passed. Root also
read the complete new proofs and rederived their principal identities;
the agents' recorded mathematical diagnostics were not rerun solely to
update the indices.
During items 49--52, an intermediate scoped scan checked 15 selected
documents and 638 local links. The completed scan checked 21 selected
index, theorem, review, and prior-art files and resolved all 686 local
links, with no trailing whitespace. The scoped tracked-file
`git diff --check` passed again. These were document checks; mathematical
diagnostics remained the distinct author and reviewer runs recorded above.
The general claims rest on the proofs, not finite experiments. No Lean work,
project-wide verification, or CI inspection has been performed for this
continuation.

For items 53--54 and the supporting strong-field result, root's inline
Markdown scan checked 17 selected index, theorem, review, and prior-art
files: all 682 local file links resolved and no trailing whitespace
remained. The scoped tracked-file `git diff --check` passed. Root also
read the new rotating-fiber counterexample and independently rederived
its Hessian obstruction and set-relative growth bound. No mathematical
fixture was rerun merely to update the indices.
For items 55--56, root checked 20 selected index, theorem, review, and
prior-art files: all 715 local file links resolved and no trailing
whitespace remained. The scoped tracked-file `git diff --check` passed.
Root's independent verification also included the actual primary
Basu--Lerario theorem, the finite-grid transfer, and the simpler exact
small-core output argument. These were proof and document checks;
the distinct computational commands are recorded above.
For items 57–58, root's inline scan checked 13 selected index, theorem,
and review documents and resolved all 694 local links, with no trailing
whitespace or invalid control characters. The scoped tracked-file
`git diff --check` passed. Root read the new proofs and reviews; the
authors' mathematical fixtures were not rerun for index maintenance.
For items 59–60 and the constant-base recourse update, root checked
17 selected documents and all 767 local links; no trailing whitespace
or invalid control characters were found. The scoped tracked-file
`git diff --check` passed. Proof reviews and primary-statement checks
are described in the corresponding entries; no mathematical fixtures
were repeated solely for these index edits.
For items 61–64, root checked 22 selected index, theorem, review and
prior-art documents and resolved all 841 local Markdown links, with no
trailing whitespace or invalid control characters. An initial scanner
mistook a formula inside a code fence for a link; excluding code fixed
the scanner, and the rerun passed without a document change. The scoped
tracked-file `git diff --check` passed. Root read the completed proofs
and reviews and independently rechecked their principal arguments;
the recorded mathematical fixtures were not rerun for index maintenance.
For items 65–66 and their continuous-noise and integer-oracle companions,
root checked 15 selected documents and all 824 local links; no trailing
whitespace or invalid control characters were found. The scoped tracked
`git diff --check` passed. Root independently reread the actual formula
encoding correction, core-selector source and fresh reviews. These
document checks did not duplicate the authors' distinct geometric,
coefficient-prefix or hull diagnostics.
For items 67–70, root checked 17 selected index, theorem and review
documents and resolved all 850 local links, with no trailing whitespace
or invalid control characters. The scoped tracked-file
`git diff --check` passed. Root read the completed reviews, including
the QP coupled addendum and cubic minimum-norm corollary, and independently
rechecked their proofs. The authors' distinct computational diagnostics
were recorded without rerunning them solely for index maintenance.
At the requested closeout, root checked 36 explicitly selected index,
theorem, review, assessment and prior-audit documents. All 1,001 local
links resolved; code fences, whitespace, control characters and the
new root diagnostic's Python syntax passed. The scoped tracked-file
`git diff --check` also passed. Root read both global-polynomial reviews,
the affine-power review and the residual-cubic closing review, and
independently rechecked their completed proofs. The only new mathematical
run by root in this closing phase was the interpolation/unisolvent/Jensen
diagnostic recorded above. All active research and review lanes finished;
the unresolved extension remains documented rather than claimed solved.

## Literature process and current limits

Luna agents are performing the external literature research. A single reusable
Luna agent with maximum reasoning effort processes all identified additions
through `/workspace/local-home/repo/skills/literature/SKILL.md`; it alone ingests and
regenerates the ignored local KB. Batches are processed sequentially while
mathematical work continues.

The initial comparison has already found a strong September 2026 prior:
Del Pia and Khajavirad, *Treewidth and the complexity of box-constrained
quadratic programs*, arXiv:2609.35595. Its exact continuous quadratic forest
algorithm prevents claiming that tree-based box-QP optimization itself is
new. Other comparison lanes include continuous DCOP, iterative dynamic
programming, treewidth approximation schemes, exact indicator QP, and
graph-structured sensitivity. The [grid audit](prior-art/geometric-grid-prior.md)
and [sensitivity audit](prior-art/tree-sensitivity-audit.md) record primary
sources and precise comparisons. The DDDP original was retrieved and read:
its recentered corridor search does not provide the global lower certificate
used here. KB ingestion continues sequentially; unresolved full texts remain
identified rather than inferred from abstracts.

The ingester archived the first ten completed addition rounds in the
[batch report](../literature/runs/2026-10-02-minlp-identified-priors-r1-r10-progress/run.md).
It records 42 outcomes: 39 new packages, one full-text promotion, one source
added to an existing package, and one duplicate candidate rejected. The
knowledge-base check passed with a documented pre-existing warning. Later
batches are recorded separately; unresolved journal full texts are not
silently replaced by conference versions or related theses.

The certificate audit required a substantive source correction. The exact
multivariate Bernstein theorem and algorithm locators initially assigned
to Boudaoud--Caruso--Roy (2008) belong to Richard Leroy's distinct 2009
manuscript. A misleadingly labeled repository page exposed the latter
PDF. The audit now distinguishes them: the 2008 article remains unread,
and its official abstract supports only the stated univariate result.
A second Luna reader checked Leroy's primary text and the corrected
locators independently. That reader also checked Scheiderer's Corollary
3.17 against the retrieved primary PDF; it supplies a local-global
membership criterion, not a degree or complexity bound. Full-text
promotions are routed through the sole literature ingester.

No originality claim is established. An unsuccessful search cannot establish
priority. Strongest-source comparisons, exact assumptions, missing full texts,
and any source-driven reductions in the claimed contribution must remain in
the final research notes.
