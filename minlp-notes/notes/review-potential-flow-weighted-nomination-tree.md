# Independent review: weighted potentials with nomination uncertainty on trees

Date: 2026-09-05. Verdict: **PASS** for the explicitly constructed
family in [the candidate note](potential-flow-weighted-nomination-tree-hardness.md).
The result is ordinary NP-completeness and a constant absolute-error
obstruction. The elementary continuous quadratic-knapsack mechanism
is established; this review does not establish priority for the precise
passive-tree interpretation.

## Physical model and objective

Removing any edge of a tree determines its flow by the total nomination
on one side. In the stated orientation, leaf flow is `y_i` and backbone
flow from `v_i` to `v_(i+1)` is `sum_(j>i) y_j`. These are nonnegative,
and conservation at the root is exactly `sum y_i=K`. Thus the balanced
nomination box projects to precisely the displayed capped simplex.
There are no extra arc-capacity, pressure, or operating constraints.

Fixing one potential and recursively integrating the edge laws gives
the unique potential vector up to a common shift. All values are
rational for rational nominations, with polynomial binary encoding
length for the proposed certificates. If nonnegative absolute potentials
are desired, a sufficiently large common rational shift supplies them;
the result presupposes no fixed upper pressure limit.

Every backbone node and attached leaf is distinct. The objective has
coefficient `+1` at each backbone node and `-1` at each leaf, with zero
total coefficient. Therefore its gauge invariance and support size
`2n` are exact, and its value is exactly `sum y_i^2/w_i`. Backbone
pressure drops do not enter this objective. The graph has `2n` vertices,
`2n-1` edges, and maximum degree three (including the smaller endpoint
and one-item cases).

## Completeness and gap

Every summand satisfies `y_i^2/w_i<=y_i`, with equality precisely at
the two endpoints. Consequently equality with the upper bound `K`
holds exactly for a subset-sum witness. The mapping and its rational
resistances `1/w_i` have polynomial binary encoding length.

A capped-simplex point with two interior coordinates is not a vertex:
one may perturb those two coordinates by opposite sufficiently small
amounts while preserving the sum. Conversely, fixing all but at most
one coordinate at bounds leaves no nonzero two-sided feasible direction.
All vertices therefore have at most one interior coordinate. Since
the other coordinates and `K` are integers, that coordinate is also
an integer. It is called fractional in the draft only in the sense
of being strictly between its bounds, not in the arithmetic sense.

Convexity and compactness ensure that a maximum occurs at a vertex.
This proves NP membership for the stated family even when the decision
threshold is an arbitrary rational: a maximizing vertex has a rational
certificate of polynomial size, whose objective is checked exactly.
It does not assert NP membership for arbitrary potential networks.

In a no instance every vertex has one interior coordinate `r` with
`1<=r<=w_i-1`. The deficit is `r(w_i-r)/w_i`; the concave quadratic in
`r` takes its smallest value on that integer interval at an endpoint,
giving `(w_i-1)/w_i>=1/2`. Convex maximization is essential here: an
arbitrary interior point need not have an integer coordinate. Since
a maximizing vertex exists, the same deficit bound holds for the
global maximum, and hence for every feasible point. The example
`w=(2,2), K=1` attains the half-unit gap exactly.

An absolute value error at most `1/8` distinguishes the alternatives,
for example by comparison with `K-1/4`. A feasible returned nomination
within `1/8` of optimal also distinguishes them by exact evaluation.
For direct recovery, `m_i=min(y_i,w_i-y_i)` lies in `[0,w_i/2]`, so
`K-F=sum m_i(1-m_i/w_i)>=sum m_i/2`. A deficit strictly below `1/4`
puts the nearest-endpoint sum strictly within `1/2` of integer `K`,
forcing equality. This statement assumes the returned nomination is
feasible exactly; a feasibility-tolerance guarantee alone would require
an additional argument.

The resistance scaling by `prod w_i` has polynomial binary length and
preserves the decision problem after scaling the threshold. Neither
that scaling nor the unscaled constant absolute gap proves strong
hardness or a relative approximation barrier.

## Exact independent checks

[check_weighted_nomination_tree_review.py](../code/potential_flow_mpd/check_weighted_nomination_tree_review.py)
enumerated every capped-simplex vertex for 100 deterministic small
instances, including one-item cases, a yes instance, and the sharp
half-gap no instance. All 1,751 vertex states passed exact rational
conservation, edge-law, graph-degree, objective, and gap checks.
Another 2,000 rational convex combinations passed the physical mapping
and endpoint-distance inequalities; every point meeting the strict
rounding hypothesis rounded to the required integer sum. Exact subset
enumeration agreed with all 100 global vertex maxima. No floating-point
solver or tolerance was used.

## Source and scope check

The [2026 potential-flow survey](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf),
printed pages 9–10, defines nomination MPD for two specified nodes and
states its tractability on trees. I inspected the repository's full
text. Its two-terminal statement does not cover the growing-support
objective here, so there is no contradiction.

The primary-hosted [Liberti survey manuscript](https://www.lix.polytechnique.fr/~liberti/rairo18.pdf),
Section 4.3.6, presents the reduction using `sum x_i(1-x_i)` under a
weighted sum equality and credits Vavasis (1991), Section 4.2. The
indexed source text was accessible; direct PDF opening returned HTTP
403 in this audit. The present weighted version uses the same endpoint
forcing principle. This establishes an explicit prior-work caveat,
not a complete comparison with Vavasis's original book or all network
interpretations. Searches combining weighted potentials, nomination
uncertainty, trees, and hardness found no directly matching passive
tree statement, but that limited search does not establish novelty.

As an additional scope check, the explicit family has a pseudopolynomial
algorithm. For each possible interior index `i`, a subset-sum dynamic
program on all other weights lists reachable endpoint sums `s`. For
each `s` with `0<=K-s<=w_i`, evaluate the corresponding vertex deficit
`(K-s)(w_i-K+s)/w_i`; the smallest deficit gives the optimum. A simple
implementation uses `O(n^2 W)` reachability work plus exact rational
comparisons. This corroborates the ordinary-hardness interpretation
and should not be confused with a polynomial binary-time algorithm.
