# Independent audit: coupled convex worst-case performance on a cactus

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently checked
[the convex-performance hardness candidate](potential-flow-cactus-convex-performance-hardness.md).
The bounded-resistance network realizes a rational cube, and the stated
convex quadratic objective has maximum exactly equal to the unweighted
Max-Cut optimum. Strong NP-hardness, the constant additive-error
consequence, and restricted-family NP/coNP membership are justified.
The Max-Cut mechanism is classical; this audit does not assign novelty
to convex quadratic maximization over a box.

## Independent cube coordinates in the physical network

Bridges in the chain separate the unit source from the unit sink, so
each carries exactly one unit. Every triangle consequently has effective
unit injection at its entrance and unit withdrawal at its exit. The
shared articulation structure introduces no resistance dependence into
these effective nominations.

The direct path and alternate path have the same potential difference.
Both carry positive flow because their passive directions agree and
their total through-flow is positive. Writing the direct flow as `x_i`
gives

```
beta_i x_i^2=4(1-x_i)^2,
x_i=2/(2+sqrt(beta_i)).
```

This strictly decreasing continuous function maps `[1,16]` onto
`[1/3,2/3]`. Thus `z_i=3x_i-1` ranges over `[0,1]`; different triangles
choose these coordinates independently. Conversely, every point of
the cube is realizable, with
`beta_i=4((2-z_i)/(1+z_i))^2` in `[1,16]`. The two Boolean endpoints
are realized by resistances 16 and one and have rational physical flows.

The graph has `3n` vertices and `4n-1` edges for `n` triangles. Separate
entrance and exit attachment vertices keep maximum degree at most three;
the third vertex of each triangle has degree two. It is simple and a
cactus, with one independent cycle per block. Direct and alternate arcs
can all be oriented from entrance to exit, with bridges connecting
consecutive blocks, giving an acyclic orientation. All its physical
flows are positive for every allowed resistance scenario.

The alternate edges have resistance two, bridges resistance four, and
direct resistance ranges are `[1,16]`. All network numerical data are
therefore bounded constants, including the only two nonzero nominations
`+1,-1`.

## Exact Max-Cut objective

The relation `z_i-z_j=3(x_i-x_j)` proves the objective identity

```
9 sum_(ij in E(H))(x_i-x_j)^2
=sum_(ij in E(H))(z_i-z_j)^2.
```

It is convex and nonnegative on the entire flow space because it is a
sum of squares of linear expressions. On a binary vector each term is
one exactly when that edge crosses the cut, and zero otherwise.

For any point of a cube, hold all but one coordinate fixed. Convexity in
that scalar coordinate implies that at least one endpoint has value no
smaller. Repeating over all coordinates gives a vertex with no smaller
value. Hence maximizing over the full physically attainable cube is
exactly maximizing cut size, not merely bounded below by it. Compactness
ensures attainment.

I directly checked the cited
[Del Pia, Dey, and Molinaro paper, Section 1.1](https://arxiv.org/pdf/1407.4798).
It records the classical unweighted Max-Cut decision formulation
`sum(x_i+x_j-2x_ix_j)>=K` on binary vectors. This equals the squared
difference formulation there because a Boolean square equals its base.
The network reduction uses this established NP-complete source problem.

## Strong hardness, thresholds, and membership

Restrict nontrivial source thresholds to `0<=K<=|E(H)|`; thresholds
outside that range are immediately decided. Thus all source thresholds
have polynomial numerical magnitude. Expanding the flow objective gives
coefficient `9 deg_H(i)` on `x_i^2` and coefficient `-18` on a cross
monomial for each edge of `H`. These are integers of polynomial
magnitude. Alternatively the explicit sum-of-squares list uses only
the fixed coefficient nine. Converting all numerical data to unary
therefore preserves polynomial reduction size. This proves strong
NP-hardness in the usual sense.

The optimum is an integer. For the decision threshold `K`, yes instances
have maximum at least `K` and no instances at most `K-1`. For robust
upper limit `K-1/2`, a yes Max-Cut instance supplies a strict violation;
a no instance satisfies the limit for every scenario. These are the
correct existential and universal threshold directions.

Within the stated hardware-and-objective family, a binary endpoint
selection is a complete certificate: some such selection attains the
maximum, and its flow coordinates and cut value are rational and
polynomial-time computable. This proves NP membership for existential
threshold attainment and coNP membership for robust upper-limit
satisfaction on this family. The candidate correctly avoids claiming
these membership statements for every cactus with arbitrary algebraic
cycle bounds and arbitrary coupled quadratic performance functions.

An objective estimate with absolute error at most one quarter identifies
the integer maximum by nearest-integer rounding. This yields the stated
fixed-accuracy NP-hardness without scaling resistances or nominations.
Normalizing the objective by its growing possible range changes this
error statement, and the candidate makes no normalized fixed-error claim.

## Structural interpretation and reproduced checks

Physical independence of cactus blocks coexists with coupling in the
performance function. If that performance separated by cycle coordinate,
the endpoint choices could be made independently. Here the comparison
graph `H` explicitly couples different blocks, producing the familiar
convex-box maximization problem. This does not contradict the parallelotope
flow-region theorem, endpoint worst-case existence, the linear-objective
scenario algorithm, or convex minimization under interval resistances.

I reran
`code/potential_flow_mpd/cactus_convex_performance_hardness_checks.py`.
It passed 5,184 exact rational grid states across all 64 simple
comparison graphs on four vertices, checking the cube realization,
objective identity, endpoint cut values, and interior domination.
These checks supplement the explicit reduction; they do not establish
literature priority.

No substantive defect remains in the proposed boundary or its stated
complexity qualifications.
