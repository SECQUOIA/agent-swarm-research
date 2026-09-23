# Independent audit: profitable flow in acyclic generalized pooling

Date: 2026-09-04. Reviewed draft: `results/pooling-triviality-polynomial.md`.

**Outcome:** the single-output decomposition, polynomial LP sign test, and output-count
approximation bound are correct for the stated model. I found no unresolved mathematical
issue. This is an independent agent audit, not journal peer review or a certification
of literature priority.

## Source model

I read the source's model and visually checked the original PDF equations and remark:
[[gupte2017-relaxations-and-discretizations-for-the]] p.4-6. Its graph is a finite DAG,
with inputs, pools, and outputs; pool-to-pool arcs are allowed. The capacity constraints
are upper bounds on nonnegative arc flows and input, pool, and output throughput.
Only outputs carry prescribed quality intervals. Pooling is lossless linear blending.
Remark 2.2 on PDF p.6 asks whether zero optimal value can be detected in polynomial time.

These assumptions matter. Positive minimum flows, fixed charges, intermediate quality
restrictions, losses, and nonlinear blending are outside the audited theorem. Consistent
output intervals and nonnegative capacities ensure the zero flow is feasible, as the
source explicitly assumes. All complexity statements require rational encoded data.

## Destination decomposition

For a feasible physical flow, define `h_j(v)` by the draft's reverse recursion on
positive-throughput pools, with indicator boundary values at outputs and zero at
inactive pools. The values lie in `[0,1]`. A positive-flow path cannot end at a pool:
balance would provide a positive outgoing arc. Acyclicity makes every such continuation
terminate at an output. Consequently the destination probabilities sum to one at every
positive-throughput pool and at every output.

The construction must use the probability at the **head** of each arc:
`y^j_uv=y_uv h_j(v)`. I checked both conservation identities independently.
Every incoming arc of a pool is scaled by the same factor `h_j(v)`, while the sum
of its outgoing scaled arcs is `h_j(v)` times its original throughput by recursion.
The same common scaling multiplies its incoming quality mass, so its original quality
vector still satisfies every tracking equation. This works simultaneously for all
quality coordinates and permits signed specification values.

At a zero-throughput pool every incident flow is zero. At a pool with positive original
throughput but zero destination probability, the component has zero incoming flow and
zero total outgoing flow; nonnegativity then makes all component outgoing arcs zero.
There is therefore no exception involving an arbitrary inactive quality value.

Output `j` receives its original incoming arc flows in component `j`. Every other
output receives zero. All output requirements remain satisfied. Since each component
is coordinatewise at most the original flow, every upper capacity remains satisfied.
Finally, every positive-flow arc has a head whose probabilities sum to one, giving
`y=Σ_j y^j`. Linear costs therefore sum, and negative total cost implies a negative
single-output component.

## Exact single-output flow projection

With only output `j` active, summing pool quality balances cancels internal quality
flows. The total quality mass arriving at `j` is exactly
`Σ_i λ_ik s_i`, where `s_i` is input `i`'s total outflow. Hence the proposed aggregate
quality inequalities are necessary.

They are also sufficient. Given an LP flow, process pools in topological order and
assign each positive-throughput pool the weighted average of its incoming qualities.
All outgoing arcs then carry that same assigned quality, and every tracking equation
holds. The aggregate input mass identity ensures output `j` satisfies its quality
limits. This argument allows arbitrary splitting and recombination before the unique
output; such internal routing does not change total input quality mass. Direct
input-output arcs are included automatically.

If total output flow is zero, no positive arc flow can exist in this DAG by pool
conservation and the input/output orientation. Other zero-flow outputs satisfy their
multiplied quality inequalities. Thus the LP is exactly the single-output feasible
flow projection, rather than merely a relaxation.

## Complexity and quantitative statement

There are at most `|J|` LPs, each with polynomially many rational variables and
constraints. Finite upper capacities make their flow regions bounded. Rational LP
optimization decides whether an optimum is negative or zero; a numerical tolerance
alone cannot establish equality with zero.

A rational negative LP solution supplies a polynomial-bit flow witness. Once this
flow is fixed, quality recovery is a triangular linear system with rational coefficients
on the active pools. Standard rational linear algebra gives a polynomial-bit solution;
there is no need to enumerate exponentially many input-output paths. At inactive pools
one may set any fixed finite quality. The decomposition used for the existence proof
need not itself be computed from an unknown optimal pooling solution.

If an empty output set is allowed, every feasible flow is zero by acyclicity and
balance, and triviality is immediate. Otherwise each single-output LP includes zero,
so every `z_j≤0`. Feasibility of a single-output solution in the original model gives
`z*≤z_best`; decomposition and summation give

```
z* ≥ Σ_j z_j ≥ |J| z_best,
```

hence `z*≤z_best≤z*/|J|≤0`. This is a sign test and an output-count approximation,
not an assertion that the original optimal value equals the best single-output value.

## Additional sign-test simplification

I independently derived the same shortest-path reduction later reported by the root
and another reviewer. For the sign question, remove zero-capacity nodes and arcs.
Every remaining capacity is positive. Let `δ_ij` be the minimum path cost from input
`i` to output `j` in this DAG. For each output, solve a blending LP over reachable
inputs with `γ≥0`, `Σ_i γ_i=1`, the output quality intervals imposed on `Σ_i λ_iγ_i`,
and objective `Σ_i δ_ijγ_i`.

A negative LP solution can be routed along chosen shortest paths and scaled by a
sufficiently small positive rational factor to satisfy all positive capacities.
The resulting single-output ordinary flow is physically realizable by the preceding
argument and retains negative cost. Conversely, decompose any negative single-output
ordinary flow into input-output paths. Normalize by output throughput; replacing each
used input-output route by a minimum-cost route can only decrease its cost, giving a
negative feasible blending objective.

The shortest paths have at most `|N|−1` arcs. Their rational costs, the blending LP
solution, and a scaling factor chosen as the minimum positive capacity/load ratio
have polynomial encoding length. Thus positive capacities influence the sign test
only through whether they are zero. This conclusion would fail in the presence of
positive lower flow requirements.

## Prior-art qualification

The draft correctly separates the known standard-pooling output-count approximation
from its proposed extension across an arbitrary acyclic network of pools. I have not
independently completed an exhaustive literature review of the generalized extension.
The mathematical result should retain the draft's qualified priority status.
