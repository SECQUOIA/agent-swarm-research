# Independent review: an upper-bound blending path with exponential price response

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: Sections 3–5 of the
[degree-two bypass investigation](pooling-degree-two-bypass-investigation.md)
pass this final audit.** This includes nonnegative output prices, uniform
removal of source lower bounds, and the quantifier-free total-degree
consequence. The physical path embedding was checked earlier in my
[path-LP investigation](parametric-path-lp-investigation.md).

For `j<n`, the normalized positive-port weights sum to less than `1/15`.
With the final weight in `[-1/15,1/15]`, all prefix-defined output revenues
are positive and less than 2. Only the last output revenue varies. Grouping
revenue by its source gives the coefficient difference
`R_j-R_(j-1)=w_j` on the rightward flow. The complementary constant is
`C0=sum_j R_(j-1)s_j`; it contains no final revenue and is therefore
independent of the parameter. All input production costs can be zero.

The relaxed physical model has exactly `N=2n` arc variables. Its internal
quality inequalities, after cancellation of the midpoint specification,
are predecessor-right flow minus current-left flow at most zero. This
remains true after the common quality normalization. Nonnegativity,
individual arc bounds, input capacities, and output capacities likewise
have coefficient entries in `{-1,0,1}`. Hence the previously audited
error-bound constant specializes correctly to `H=N^N`.

The source right-hand sides `s_j` are rational rather than integer after
normalization. This causes no difficulty: the singular-value argument
requires integer coefficient rows, not integer right-hand sides. Source
coefficient rows remain unscaled zero-one rows, so their negative-equality
residuals are precisely the nonnegative source deficits. Every other
positive residual vanishes at a relaxed feasible flow. The maximum
residual is at most their sum, and the nonempty exact-source polytope
therefore admits the stated repair within `H delta` in the `l_1` norm.

The entire bypass component is linear. Thus restoring the source contracts
requires no radial repair or assumption about a positive pool throughput.
Each arc's base revenue coefficient lies in `[0,2]` uniformly in the
parameter, giving revenue loss at most `2H delta`. Adding `M=2H+1`
to every output revenue rewards total source throughput by `M` through
mass conservation. A relaxed point with positive deficit is strictly
dominated by its exact-source repair. An exact-source point has zero
deficit and receives the constant offset `M sum_j s_j`. This proves
the asserted optimal-value identity uniformly on the whole parameter
interval, rather than only at the selected vertex witnesses.

The penalty has `O(n log n)` bits. It changes neither arcs nor capacities
nor quality rows. Every positive source lower bound can consequently be
deleted, all output lower bounds were already zero, and every remaining
flow upper bound is at most one. The graph is still a path with input
and output degrees at most two. There are no pools in this component.

The resulting price-response function is a fixed vertical translation
of the primary shadow value, so it retains every one of its `2^n`
nonempty affine regions. For either its graph or epigraph, every point
on an open graph segment must lie on the zero set of a defining nonzero
polynomial: otherwise all signs, and therefore every Boolean formula
of those signs, are locally constant. The product of the defining
polynomials vanishes on the whole segment, hence on its entire line.
Each distinct segment line is a distinct linear factor, proving the
lower bound on the sum of degrees. Identically zero polynomials must
first be replaced by their constant truth values. The finite price
interval retains all the exposed regions, as checked in the primary
construction audit.

No further numerical test is needed to justify this penalty constant;
floating-point tests with its large magnitude would not establish the
uniform error bound. The author's exact physical primal/dual certificates
and the parallel reviewer's exact shadow checks corroborate the underlying
family. This audit establishes correctness of the packaging, not novelty
of the underlying shadow theorem, NP-hardness of the LP family, or a
complexity classification for pooling with degree-two bypasses. Compact
circuits, extended descriptions, and polynomial pointwise optimization
remain compatible with the lower bound.

## Added coordinate-port representation corollary

Section 7 also passes this independent check, with its scope restricted
to feasibility projections of pool-free bypass networks. At maximum
degree two, each node throughput or quality row has at most two arc
variables; individual arc bounds have one. Multiple attributes and
lower bounds add rows without enlarging their supports. A global
objective-threshold inequality is not included in this statement,
because it need not have this sparsity.

Fourier–Motzkin elimination preserves the two-variable-per-inequality
property. Every paired positive/negative row has at most one variable
other than the eliminated one, so its resulting inequality has at most
two surviving variables. Rows not containing the eliminated variable
retain their support. Repetition gives an exact finite description of
the coordinate projection, although its row count can grow rapidly.
Equalities can first be replaced by opposite inequalities.

The nonnegative three-dimensional simplex has an open facet with normal
`(1,1,1)`. In any finite halfspace description, some defining row must
be tight at a relative interior point of this facet; otherwise that
point would be interior to the full-dimensional set. Such a row must
annihilate every tangent direction within the facet, and its nonzero
normal is therefore proportional to `(1,1,1)`. No two-variable row can
satisfy this requirement. Hence this simplex cannot be represented by
three designated individual arc flows of any degree-two pool-free
bypass network.

The reviewed degree-three circuit construction can represent every
rational linear system on signals in `[0,2]`, including this simplex,
by designated full ports. This gives the claimed sharp distinction for
that coordinate-port representation property. I requested that the
draft say bounded signals explicitly: unrestricted negative or unbounded
systems cannot be represented verbatim by nonnegative finite-capacity
arc coordinates. The corollary does not concern arbitrary linear-image
representations, projections conditioned on dense objective thresholds,
or the computational complexity of degree-two pooling.
