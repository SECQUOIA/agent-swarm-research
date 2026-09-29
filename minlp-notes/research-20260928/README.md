# September 28 research continuation

This continuation is closed at the user's request to finish the current
ideas and start no new directions. The
[closing record](closing-research-results.md) collects the final claims,
verification, corrected source comparisons, and limitations. No new work
is underway. The previous continuation's results were resources for this
work, without constraining its direction.

The leading candidates concern quantitative sparse polynomial optimization.
For ordinary box quadratic modules, a reviewed kernel argument gives error
`O(log^3(r)/r^2)`. A common correction of signed densities removes an extra
dependence on the number of bags from the bound per total coefficient norm.
The exact construction, degree accounting, and source comparisons are
documented separately; publication priority remains unestablished.

The companion full-preordering rate is inverse-square, and a fixed quadratic
proves this exponent sharp. Magron's July 2025 and February 2026 author slides
already publicly state the inverse-square sparse preordering rate for two
bags, so that rate is not claimed as first established here. For convex
private subproblems, the new notes distinguish fixed private domains from
affine recourse: the proved upper rates are inverse-square and inverse-order,
respectively. A three-variable affine-recourse example proves the latter
exponent sharp. Branching at its active-set change makes both branches exact
at order two. These are statements about specified relaxations, not general
MINLP runtime bounds.

- [Sparse kernel theorem](solver/sparse-kernel-rounding.md): unconditional
  `O(r^-2)` convergence for the full local box preordering, finite grid
  rounding, and a sparse SOS certificate consequence. An earlier author
  presentation already states the rate.
- [Sharp fixed quadratic](solver/quadratic-sharpness.md): `Omega(r^-2)`
  error with two bags of size two, even with exact local measures; the
  dense hierarchy is exact at order two. An
  [exact finite-order analysis](solver/quadratic-exact-gap-frontier.md)
  gives explicit matching certificates and moment witnesses at orders
  one and two; higher-order equality is not claimed.
- [Ordinary sparse Putinar theorem](solver/sparse-putinar-kernel.md):
  `O(log^3(r)/r^2)` using ordinary local quadratic modules; an
  [exact-consistency strengthening](solver/sparse-putinar-exact-consistency.md)
  makes the bound per total coefficient norm uniform in the number of bags.
  The [dedicated prior audit](solver/sparse-putinar-prior.md) compares the
  exact cones, degree conventions, and earlier public rate assertions.
- [Large private convex blocks](solver/partial-kernel-rounding.md): shared
  degree increases while private degree stays two, giving inverse-square
  convergence with a hierarchy exponent controlled by shared dimension.
  Necessary private quadratic bounds and convexity limitations are explicit.
- [Affine recourse upper bound](solver/affine-recourse-kernel-upper.md):
  complete recourse and a fixed constraint matrix give inverse-order
  convergence by Hoffman repair. The [sharp boundary example](solver/affine-recourse-rate-boundary.md)
  identifies an obstruction caused by the absolute-value separator message.
- [Regular recourse multipliers](solver/active-region-rates.md): weighted
  multivariate Chebyshev regularity, or coordinatewise Lipschitz regularity,
  restores inverse-square convergence in the same private-degree-two
  hierarchy. Strict convexity alone is insufficient.
- [Polynomial constraints](solver/general-constraints-kernel.md): global
  Hölder repair gives `O(r^-alpha)` for the specified strengthened
  preordering and `O((log(r)/r)^alpha)` for ordinary constrained modules.
  The global geometric assumption and prior slack-lifting comparison are
  explicit; efficient global repair is not asserted.
- [Exact rational certificates](solver/rational-sparse-certificates.md):
  quantitative slack gives polynomial-size rational certificates and a
  theoretical construction algorithm in the expanded SDP dimensions.
  This specializes established rational-certification methods.
- [Numerical rate checks](solver/numerical-rate-check.md): independently
  reviewed low-order experiments support the contrasting rate patterns;
  solver residuals and uncertified grid approximations are recorded.
- [Independent prior comparison](solver/prior-independent.md): closest
  sparse-rate and generalized-moment results, including the distinction
  between finite SDP duality and unattained polynomial separator duals.
- [Finite-state extension](solver/mixed-discrete-extension.md): keeps
  finite labels unchanged while smoothing continuous coordinates; the
  independent review and targeted exact checks are complete.
- [Graph-constrained control rounding](applications/graph-constrained-rounding.md):
  reviewed topology-dependent rates and a quantitative transition as
  relaxed relay-mode mass vanishes. This is a focused control result;
  application and novelty qualifications are stated in the note.
- [Exact arithmetic investigations](algebra/README.md): sign-circuit
  compilation, binary optimizer extraction, and degenerate-convexity
  obstructions. Generic adaptive compilation has passed a fresh
  cross-branch proof review; its literature status remains qualified.
  [Lean coverage](algebra/formal-coverage.md) verifies local algebraic
  lemmas, not the compiler or complexity theorem.
- [Deterministic and law repair](structural/repair-probe.md): equality
  of optimal repair constants on trees, with hard-constraint limitations;
  a supporting synthesis of established ingredients.
- [Submodular boundary investigation](submodular/README.md): exact
  counterexamples and prior comparisons, retained as modest negative work.
- [Convex-form epigraphs](certificates/convex-form-epigraph.md): a
  reviewed consequence of established conic representation theorems and
  a documented correction to an unqualified slide statement; no small
  or rational lift is established.
- [Curvature-based convex covers](solver/branching-curvature-atlas.md):
  a strict positive Hessian complement permits a local low-dimensional
  subdivision bound; the [degeneracy barrier](solver/branching-degeneracy-barrier.md)
  shows that pointwise negative inertia alone is insufficient.
- [Adaptive multiplier coefficients](certificates/universal-multiplier.md):
  a reviewed sharp scale obstruction at fixed degree, without a universal
  adaptive-degree conclusion.

Negative results, rejected approaches, and unresolved questions are retained
where informative. They mark the limits of the completed results; they are
not active assignments. Only targeted checks were run locally; their commands
and limits are recorded in the topic notes and the
[root research log](root-research-log.md).

Independent review means review by a separate research agent, not journal
peer review. An unsuccessful literature search does not establish novelty.
