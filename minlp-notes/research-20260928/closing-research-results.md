# September 28 research results and scope closure

The user narrowed the task to finishing the ideas already underway and
starting no new directions. This record collects the resulting claims,
their verification, and their limits. It is not a claim that the surrounding
mathematical questions have all been resolved. Questions preserved in the
research notes are outside the completed claims, not prerequisites hidden
inside their proofs.

## Main contribution assessment

The strongest candidate is an unconditional quantitative transfer from dense
box kernels to the **ordinary sparse quadratic-module hierarchy**, without
assuming an attained polynomial separator dual. A second coherent result
classifies the sharp general rate for a specified hierarchy with large
private convex recourse blocks, and identifies regularity conditions that
restore a faster rate. Both concern finite relaxations used in global
optimization; neither establishes a general MINLP running-time improvement.

Publication priority remains unestablished. Earlier author slides already
assert the inverse-square sparse **preordering** rate, and the dense
ordinary-module kernel is prior. The notes withdraw the earlier broad rate
novelty assessment and compare the exact assumptions and conclusions in
the [ordinary-module source audit](solver/sparse-putinar-prior.md) and
[recourse source audit](solver/affine-recourse-upper-prior.md).

## Sparse box certificates and sharpness

For a running-intersection tree of bags of width at most `w`, write the
polynomial objective as a sum of bag polynomials. At moment order `R`,
ordinary local quadratic modules use squares and individual box generators
`1-x_i^2`, with each certificate term of degree at most `2R`. Separator
moments agree through degree `2R`.

The [exact-consistency theorem](solver/sparse-putinar-exact-consistency.md)
proves

\[
0\le f^*-\rho_R
 \le C_f\,O_{w,d}\!\left(\frac{\log^3 R}{R^2}\right),
\]

where `C_f` is the sum of local nonconstant Chebyshev coefficient norms
and `d` bounds local coordinate degree. The constants in this normalized
bound are independent of bag count and tree shape at fixed width and
degree. Total SDP size still increases with the number of bags.

The proof first constructs exactly compatible signed densities, bounds
their negative parts using weighted pseudomoment Cauchy--Schwarz, and adds
the same reference density in every bag. The corrected laws are positive
and glue exactly. Finite SDP duality gives a real sparse SOS certificate
at the displayed error. The [final independent audit](solver/signed-kernel-final-audit.md)
checks the full degree ledger and calibrates the conservative constants.

The [full-preordering theorem](solver/sparse-kernel-rounding.md) gives the
logarithm-free `O(R^-2)` rate and direct finite-grid rounding. That rate was
already publicly asserted in Magron's July 2025 and February 2026 slides;
the difference from the slower printed theorem remains unresolved. The
[fixed quadratic example](solver/quadratic-sharpness.md) proves an
`Omega(R^-2)` sparse gap even for actual local measures, while its dense
preordering is exact at order two. This isolates finite separator
information as a genuine obstruction.

An [exact finite-order analysis](solver/quadratic-exact-gap-frontier.md)
also proves, for both ordinary module and preordering,

\[
\rho_1=-\frac14,
\qquad
\rho_2=\frac83-\frac{14\sqrt3}{9}.
\]

At order one the local positivity relaxation adds error beyond the ideal
local-measure problem; at order two their values coincide. Explicit Gram
certificates and moment witnesses prove these facts; the order-two
witnesses are actual local measures. Agreement at higher
orders is only numerical evidence and is not part of the result.

## Private recourse: a sharp distinction

The private-block hierarchy increases degree only in the shared variables.
Its private degree is two, and its largest local PSD matrix has
`(p+1) binom(r+k,k)` rows for `p` private and `k` shared variables.
Redundant private quadratic bounds are essential. Convexity is required
in the private objective, and private variables must be continuous.

| Model and additional assumptions | Proved objective gap |
| --- | --- |
| Fixed private polytope; polynomial shared coefficients; convex private quadratic objective | `O(r^-2)` |
| Fixed private constraint matrix; affine shared-dependent RHS; complete recourse on the entire shared box | `O(r^-1)`, sharp in general |
| Same affine recourse, with the stated weighted Chebyshev regularity of projected optimal multipliers | `O(r^-2)` |
| Same affine recourse, with coordinatewise Lipschitz projected multipliers | `O(r^-2)`, sharp in a fixed regular example |

The [fixed-domain result](solver/partial-kernel-rounding.md) uses conditional
means and matrix Jensen. The [affine-recourse theorem](solver/affine-recourse-kernel-upper.md)
repairs those means using a uniform Hoffman bound. Its
[sharp example](solver/affine-recourse-rate-boundary.md) has objective
`-xy+z`, constraints `z>=y,z>=-y`, and separator `y`. The conditional
values are `-|y|` and `|y|`; polynomial moment agreement cannot communicate
the corner exactly. Actual local measures prove the lower bound for the
private-degree-two hierarchy as well as for the stated total-degree
preordering. Merging the bags, or splitting at `y=0`, gives exact order-two
certificates for this example.

The [regular-multiplier theorem](solver/active-region-rates.md) explains
when the slower rate is avoidable. A kernel commutator controls the part of
the optimal dual multiplier acting on shared variables. Explicit interval
and tensor certificates justify its bound for pseudomoments, including
frequencies outside the simpler total-degree moment estimate. It changes
neither the SDP nor its private degree. Strict convexity alone does not
imply the required multiplier regularity. Classical parametric-QP
sensitivity supplies useful sufficient conditions, but is not itself a
new result here.

These theorems could support lower bounds for nonconvex polynomial master
decisions coupled to large convex QPs. Grid/QP dynamic programming already
provides a competing approximation method with related exponents. The
proved addition is control of the specified SDP at every feasible
pseudomoment point. Practical advantage needs usable constants, numerical
conditioning, and application evidence; those benefits are not claimed.

## Polynomial constraints and exact arithmetic consequences

The [polynomial-constraint result](solver/general-constraints-kernel.md)
adds localizing matrices and assumes a **global** error bound

\[
\operatorname{dist}(x,K)
 \le H\left(\sum_j(-g_j(x))_+^2\right)^{\alpha/2},
\qquad 0<\alpha\le1.
\]

It proves `O(R^-alpha)` with box-preordering products times individual
constraints, and `O((log R/R)^alpha)` for ordinary constrained modules.
The direct proof controls squared constraint violation before globally
repairing a law onto `K`. The sharper ordinary bound uses a certified
kernel displacement estimate; it improves the logarithmic factor in an
earlier coefficient-based bound.

The [prior comparison](solver/general-constraints-prior.md) credits the
May 2026 slack-lifting theorem: composing that theorem with the sparse box
rate already gives a closely related constrained bound. Global geometry
can be much worse than each bag's local geometry, so the new argument does
not uniformly dominate earlier sparse effective Positivstellensätze. No
cheap global projection, preservation of integer decisions, or constrained
SDP dual attainment is inferred from this primal result.

Two supporting consequences are also complete:

- The [finite-state extension](solver/mixed-discrete-extension.md) preserves
  discrete labels exactly while smoothing continuous box coordinates. Its
  state-summed separator equations and zero-mass pruning are explicit.
  It does not cover arbitrary label-dependent continuous domains.
- The [rational-certificate result](solver/rational-sparse-certificates.md),
  for rational input data, turns a real certificate with quantitative slack into exact rational
  Grams of polynomial encoding length and gives a theoretical polynomial
  construction in the **expanded SDP dimensions**. It specializes
  established strict-feasibility rational SOS methods; it is not a new
  general rational-certification algorithm.

## Other completed investigations

These results are retained with separate significance assessments rather
than combined into an inflated main claim.

- [Exact sign compilation](algebra/README.md) gives a polynomial-size
  arithmetic sign circuit for adaptive integer sign logic and a precise
  binary-extraction consequence. Independent reviews, a reference DAG
  implementation, and local Lean lemmas support distinct parts of the
  argument. The complete compiler and complexity theorem are not
  formalized in Lean; priority remains qualified.
- [Graph-constrained control rounding](applications/graph-constrained-rounding.md)
  proves topology-dependent discrepancy rates and a transition as relaxed
  relay-mode mass vanishes. It is a focused control result with explicit
  graph and time-discretization assumptions.
- [Curvature-based convex covers](solver/branching-curvature-atlas.md)
  give `O(epsilon^(-k/2))` convex pieces under a strict positive Hessian
  complement. A [fixed smooth counterexample](solver/branching-degeneracy-barrier.md)
  shows that one negative eigenvalue alone can retain the ambient
  approximation exponent. The claims count convex pieces, not solver time.
- [Deterministic and law repair](structural/repair-probe.md) identifies
  matching optimal repair constants on trees. Its ingredients are largely
  established transport and error-bound tools.
- [Convex-form epigraphs](certificates/convex-form-epigraph.md) give a
  consequence of existing conic-representation theorems and correct an
  unqualified slide statement. No small or rational conic lift follows.
- [Adaptive multiplier coefficients](certificates/universal-multiplier.md)
  satisfy a sharp scale-growth obstruction at fixed degree. A universal
  adaptive-degree theorem is not proved.
- [Submodular investigations](submodular/README.md) retain exact
  counterexamples, corrected numerical exploration, and prior comparisons.
  They do not settle the broader one-frustrated-edge complexity question.

The abstract product-domain screening produced no separate theorem. No
extension beyond the documented domains is claimed, and that screening is
closed without opening another line of research.

## Verification and stopping boundary

Important claims have separate adversarial proof reviews and source
comparisons. Corrections are incorporated in the statements; historical
notes identify superseded claims. Targeted exact computations check
identities, finite degree ledgers, moment witnesses, and counterexamples.
The [numerical experiments](solver/numerical-rate-check.md) report solver
residuals and distinguish finite-grid estimates from certified optima.
Positive reviews and finite computations do not replace the mathematical
proofs or establish publication priority.

Commands and their actual outcomes are recorded in the topic notes and
[root log](root-research-log.md). Only targeted local verification was
performed; no project-wide checks or CI inspection were used. Research-agent
review is not journal peer review.

The current ideas are closed at the scope of their stated results. No new
research direction is authorized by this completion. The remaining
limitations describe what the results do not establish, rather than
unfinished steps needed to make their proved conclusions valid.
