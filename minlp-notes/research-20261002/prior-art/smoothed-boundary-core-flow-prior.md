# Prior-art audit: core-only smoothing with boundary flow recourse

Date: 2026-10-02. This focused comparison covers the current
[boundary-core flow draft](../new-direction/smoothed-boundary-core-flow.md),
which has passed fresh independent full-proof and arithmetic/output reviews.
It is distinct from the completed
[interior-core theorem](../new-direction/smoothed-interior-core-flow.md).
This is a focused literature comparison, not a publication-priority claim.

## Candidate and its added scope

The feasible set is a continuous core box times a fixed bounded integral
network-flow set. The objective has a fixed-degree polynomial core term and
separable polynomial arc costs, each convex in its own flow variable for
every core value. Core variables change costs only; they do not change flow
balances or bounds. A finite rational law perturbs only the core linear
coefficients. Unlike the interior theorem, the draft allows optimal core
points on any box face and has no all-noise interiority premise. It also
allows persistent ties among arbitrarily many optimal flows. The claimed
expected bound is

```text
f_d(k) [3+(1+k/2)L/(2 sigma)]^k poly_d(I),
```

with a base-only finite law, exact output on every draw, and a same-draw
fallback. Its sample-bit budget is `f_d(k) poly_d(I)`, rather than the
interior theorem's polynomial-in-input `log M` guarantee. The two reviews
above cover the stated theorem; this audit assesses only its prior-art scope.

## Optimal-flow intervals and face tests

At a core point, an exact optimum flow and its node potentials give each arc
an adjusted convex cost. The integer minimizers of each adjusted cost form
an interval. Restricting every arc to that interval gives exactly the set
of feasible flows optimal at the query: the potential term sums to a
constant over feasible flows, and equality in the sum of nonnegative
separable gaps holds exactly when every arc lies in its interval. This is a
standard consequence of separable convex flow duality and residual
optimality; the exact TU flow algorithm in Hochbaum and Shanthikumar
supports the underlying recourse operation. The interval representation
itself is derived directly in the draft rather than attributed to a new
theorem from that paper.

The deterministic face certificate then uses the restricted flow problem
to minimize each inward core derivative over **all** flows tied at the
query. Its additional quantitative step bounds the distance from an
arbitrary feasible flow to this tied-flow set by the sum of violations of
the arc intervals, using a conformal cycle decomposition. Convexity in each
arc coordinate makes those derivative costs convex on the relevant
minimizer intervals (with explicit treatment of singleton and two-point
intervals). First outside marginals and derivative margins then show that
all global optimizers in a retained hull lie on the tested face.

These components are close to standard primal-dual flow optimality,
complementary slackness, and circulation decomposition. The composition
that matters for this candidate is using one exact restricted-flow oracle
to represent all tied labels, minimize inward derivatives over them, and
certify a global face under core-only perturbations. The source comparison
does not establish that this composition is new.

## The core outer search and parametric-flow boundary

The search uses the same semiconcave corrected-grid count as the
[interior theorem](smoothed-interior-core-flow-prior.md): expected
near-optimal core tuples depend on `k` and `L/sigma`, not on the number of
feasible flows. The new draft checks all `3^k` core faces and controls two
types of exceptional noise: proximity to polynomial flow-chart boundaries
on each face, and small inward normal derivatives. A fixed-dimensional
polynomial margin argument converts distance from a chart zero into a
positive reduced-cost margin. The chart family is used only to choose a
base-only precision budget; the algorithm does not enumerate all flows or
all charts.

The strongest parametric warning remains Gajjar and Radhakrishnan's
Theorem 1 for planar directed-acyclic shortest paths: a one-parameter
shortest-path lower envelope can have `n^{Omega(log n)}` breakpoints with
`O(log^3 n)`-bit integer edge coefficients. This is also a unit-flow
minimum-cost-flow instance. It rules out assuming a small complete
parametric-flow envelope from low parameter dimension alone. It does not
rule out pointwise exact flow queries, the draft's optimal-flow interval
certificate, or its expected finite-noise search; the draft never builds
the full envelope. The verified statement and source limitations are in
the [parametric-flow audit](parametric-flow-breakpoint-prior.md).

The fixed-dimensional margin is an additional obligation beyond the
interior result. The draft's separate review of this lemma establishes a
coefficient-height bound for a fixed-degree polynomial away from its zero
set, with a dimension-dependent factor. It is an internal proof review,
not a prior-art result. Its use is to ensure that nonzero marginal
polynomials stay uniformly away from zero over the retained hull; a
measure-zero or generic-tilt argument alone would not supply that finite
precision guarantee.

## Other close optimization precedents

Hooker's [partial-convex global optimization framework](https://doi.org/10.1007/11425076_4)
and Schöbel–Scholz's [few-continuous-variable mixed-integer method](https://doi.org/10.1016/j.ejor.2013.07.003)
are conceptual antecedents for searching a small continuous core while
solving discrete subproblems. Hooker uses discretization and convex
relaxations for specified classes; the Schöbel–Scholz local record is
abstract-only. Neither checked source states
the boundary-face, all-tied-flow certificate or the expected finite-noise
exact bound. Details and access status are recorded in the
[interior-flow prior audit](smoothed-interior-core-flow-prior.md).

Classical multiparametric methods describe full value-function regions.
Ding's parametric reduction for structured indefinite QPs and
Patrinos–Sarimveis' convex piecewise-quadratic critical-region traversal
establish such representations and searches, but do not give the current
finite-noise expected exact complexity. The Gajjar–Radhakrishnan lower
bound also shows why full region enumeration can be much larger than
point-query recourse.

Beier–Vöcking and Röglin–Vöcking establish random-cost gap and adaptive
precision methods for finite discrete optimization. Their feasible
decisions are discrete; Röglin–Vöcking's smoothed-time convention is a
high-probability tail / expected-power condition, not ordinary expected bit
time. They do not supply a continuous core search or characterize a whole
optimal-flow face. The reviewed internal
[native-integer recourse theorem](../new-direction/smoothed-native-integer-recourse.md)
uses a more general fixed integer feasible set and exact bound-stable oracle,
but perturbs residual as well as core coefficients and identifies one
residual label using excluded-label optimization. The present draft narrows
the residual class to convex-cost flows and tries to remove residual noise
by representing all ties at once. These are close internal results, not
external prior art.

The exact flow oracle, potential optimality conditions, interval minimizers,
and semiconcave grid count are established mechanisms. The candidate-specific
claim is the expected FPT composition for core-only finite noise with
arbitrary core faces, using facewise chart margins and an optimal-flow-set
derivative certificate. The conclusion remains conditional on the theorem's
stated assumptions and exact oracle interfaces. It does not cover core-dependent
balances, nonseparable flow costs, or nonconvex arc costs.

## Sources checked and limits

- Hochbaum and Shanthikumar (1990), Theorems 1.2 and 4.3; full primary text,
  exact TU flow optimization, binary-capacity scaling, and source status are
  recorded in the [flow-oracle audit](integer-convex-flow-recourse-prior.md).
- Gajjar and Radhakrishnan (2019), Theorem 1; full primary text and the
  shortest-path/unit-flow reduction are in the
  [parametric-flow audit](parametric-flow-breakpoint-prior.md).
- Hooker (2005), Ding (1996 thesis), Patrinos and Sarimveis (2011),
  Schöbel and Scholz (2014), Beier–Vöcking, and Röglin–Vöcking; precise
  comparisons and full-text/abstract-only status are in the
  [interior-flow prior audit](smoothed-interior-core-flow-prior.md).
- The candidate's
  [optimal-flow-face certificate](../new-direction/flow-optimal-face-certificate.md)
  and [fixed-dimensional margin review](../reviews/flow-boundary-margin-review.md)
  are internal mathematical materials, not external prior art.

No literature-KB or index files were changed. The focused sources do not
identify an equivalent theorem, but this bounded comparison does not
establish novelty.
