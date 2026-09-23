# Exact pooling optimization with a bounded bypass vertex cover

Promoted after two independent audits into the combined
[result](../results/pooling-bypass-structure-algorithm.md). This file preserves
the investigation and earlier candidate language.

Date: 2026-09-05. Status: complete mapping candidate awaiting independent
review. This is a structural corollary of the independently verified
[fixed-core block theorem](../results/fixed-core-block-polyhedral-optimization.md),
not a new quantifier-elimination algorithm. Literature priority for the
pooling corollary remains provisional.

## Main statement

Fix the number `p` of pools, the number `K` of quality attributes, and an
integer `c`. Standard pooling is exactly solvable in polynomial input bit
time if the bipartite input-output graph of bypass arcs has a vertex cover
of size at most `c`. The numbers of inputs, outputs, and bypass arcs are
unrestricted. In particular, any number of bypass arcs may share a fixed
number of input or output endpoints.

The model permits rational lower and upper bounds on input, pool, output,
and arc throughputs; lower and upper output quality specifications; and
rational linear arc costs. Flows are nonnegative, and finite rational flow
upper bounds must be supplied or derived from finite input or output
capacities. There are no pool-to-pool arcs and no unbounded family of binary
activation decisions. The algorithm returns an exact real-algebraic optimum
and an optimizer, or reports infeasibility.

A stronger statement holds. Fix additionally an integer `h>=1`. It suffices
that deleting at most `c` vertices from the bypass graph leaves connected
components of at most `h` vertices each. The vertex-cover case is `h=1`;
`c=0` gives bypass graphs with bounded component size. This joint extension
uses the same construction, with one local block per remaining component.

These are polynomial-time results for each fixed parameter tuple. No
fixed-parameter runtime or practical performance claim is made.

## 1. Standard concentration formulation

Let `I` be the inputs, `J` the outputs, and `ell=1,...,p` the pools. Write
`C_ia` for input quality `a=1,...,K`. Use nonnegative flows

```
y_iell : input i to pool ell,
v_ellj : pool ell to output j,
z_ij   : direct input-output bypass.
```

Missing arcs have flow zero. Pool concentration variables are `q_ella`.
The pool equations are

```
sum_i y_iell = sum_j v_ellj,
sum_i C_ia y_iell = q_ella sum_j v_ellj.
```

Input throughput is `sum_ell y_iell + sum_j z_ij`. Output throughput is
`sum_ell v_ellj + sum_i z_ij`. For an output upper quality bound `U_ja`,
its homogeneous constraint is

```
sum_ell (q_ella-U_ja) v_ellj + sum_i (C_ia-U_ja) z_ij <= 0.
```

The lower quality bound `L_ja` gives the same expression with coefficients
`L_ja-q_ella` and `L_ja-C_ia`. Throughput and individual arc bounds have
their usual interval form. Pool throughput can be measured as total outflow.
This is the standard perfect-mixing concentration formulation used in
Corollary 4 of the fixed-core result.

When there is at least one input, put every `q_ella` between
`min_i C_ia` and `max_i C_ia`. A positive-throughput pool has its true
quality in this interval. A zero-throughput pool may be given any value
there without changing its outgoing quality mass. Thus these bounds give
a compact core without excluding feasible flows. An instance with no inputs
has all flows zero and is checked directly against its lower bounds.

## 2. Partition the bypass graph

Choose input vertices `A subset I` and output vertices `B subset J` with

```
cI=|A|,  cJ=|B|,  cI+cJ<=c,
```

such that each connected component of the bypass graph after deleting
`A union B` has at most `h` vertices. Denote the component input and output
sets by `I_beta,J_beta`. Isolated vertices are components too. Every bypass
arc is of exactly one of four types:

- both endpoints in `A union B`;
- from `A` to `J_beta`;
- from `I_beta` to `B`;
- from `I_beta` to `J_beta` inside one component.

There is no bypass between different remaining components. In the
vertex-cover case every component is a singleton, so the last type is absent.

For fixed `c`, one can find such a deletion set by enumerating subsets of
at most `c` graph vertices and checking component sizes. The running time
is polynomial in graph size; no supplied cover or separate graph theorem
is required. If no such set exists, this structural algorithm makes no
claim about the pooling instance. In particular, failed recognition is not
an infeasibility certificate.

## 3. Core and local blocks

The core consists of:

```
q_ella              for all pools and qualities,
y_iell              for i in A,
v_ellj              for j in B,
z_ij                for i in A and j in B.
```

Only existing flow arcs need variables; alternatively fix missing arcs to
zero. Put their individual finite arc bounds in the core domain. Along with
the concentration bounds, this makes the core a compact rational box. Its
dimension is at most

```
r = pK + p(cI+cJ) + cI cJ <= pK + pc + c^2.
```

The block for component `beta` contains all remaining flows incident to that
component:

```
y_iell        for i in I_beta,
v_ellj        for j in J_beta,
z_ij          for i in I_beta, j in J_beta,
z_ij          for i in A, j in J_beta,
z_ij          for i in I_beta, j in B.
```

Each flow is owned by exactly one core or block. The block dimension is at
most

```
d <= ph + ch + h^2.
```

For a vertex cover, the sharper bound is `d<=p+c`: a singleton input has
its pool inflows and bypasses to `B`, while a singleton output has its pool
outflows and bypasses from `A`.

Inside each block impose all its individual arc bounds, all input
throughput bounds for `i in I_beta`, and all output throughput and quality
bounds for `j in J_beta`. Every flow in such a noncover input or output
constraint belongs to this same block. Given the core, these constraints
are linear in the block variables. Their coefficients are constant or
affine in `q`. Every block coordinate has its finite rational box bounds,
as required by the fixed-core theorem. The blocks may be empty; the theorem
already handles that case.

## 4. Fixed number of aggregate constraints

Only constraints at the pools or at the deleted graph vertices remain.
The pool mass equations become

```
sum_beta [sum_{i in I_beta} y_iell - sum_{j in J_beta} v_ellj]
= sum_{j in B} v_ellj - sum_{i in A} y_iell.
```

The pool quality equations become

```
sum_beta [sum_{i in I_beta} C_ia y_iell
          - q_ella sum_{j in J_beta} v_ellj]
= q_ella sum_{j in B} v_ellj - sum_{i in A} C_ia y_iell.
```

There are `p(1+K)` equations. Their block coefficient matrices are affine
in the core; their right-hand sides have degree at most two in the core.
Pool throughput bounds are the two inequalities per pool on

```
sum_{j in B} v_ellj + sum_beta sum_{j in J_beta} v_ellj.
```

For each covered input `i in A`, impose its two throughput inequalities on

```
sum_ell y_iell + sum_{j in B} z_ij
+ sum_beta sum_{j in J_beta} z_ij.
```

For each covered output `j in B`, impose its two throughput inequalities on

```
sum_ell v_ellj + sum_{i in A} z_ij
+ sum_beta sum_{i in I_beta} z_ij.
```

Its upper quality inequality for attribute `a` is

```
sum_beta sum_{i in I_beta} (C_ia-U_ja) z_ij
<= -sum_ell (q_ella-U_ja) v_ellj
   -sum_{i in A} (C_ia-U_ja) z_ij.
```

Its lower quality inequality replaces `C_ia-U_ja` with `L_ja-C_ia`
and `q_ella-U_ja` with `L_ja-q_ella`, with the same left/right placement.
The right-hand side remains a polynomial of degree at most two in the core.
These are aggregate constraints, not local block constraints: an arbitrary
number of remaining components may feed a covered output.

The total aggregate row count, counting each interval as two inequalities,
is at most

```
p(1+K) + 2p + 2cI + 2cJ(1+K).
```

This depends only on the fixed parameters. Convert aggregate inequalities
to equations with bounded scalar slack blocks. Explicit rational bounds for
the slack values follow by interval arithmetic from the finite flow boxes
and concentration boxes. The number of summands is polynomial, so these
bounds have polynomial bit length.

Every original linear arc cost belongs either to the core objective or to
one local block objective. No new coupling is introduced by the objective.
The resulting instance has fixed core dimension, fixed local block
dimension, a fixed number of aggregate rows, and polynomial coefficients
of degree at most two. If no local blocks remain, solve the fixed-dimensional
core directly, or append one scalar block fixed to zero.

## 5. Exactness and algorithm

Given a physical feasible pooling flow, put its arc flows into their uniquely
assigned core or block coordinates. Use the actual average quality in every
positive-throughput pool and any boxed quality in every inactive pool.
All listed local and aggregate constraints are then satisfied, and the
objective is unchanged.

Conversely, the block and core flows from the constructed model satisfy
every original arc bound and every input/output throughput and output
quality constraint by Sections 3 and 4. The aggregate equations are exactly
the original pool mass and quality equations. Positive-throughput pools
therefore have their correct mixed concentration; inactive pools transmit
no flow and create no exception. Pool capacity bounds are also enforced.
Thus the reformulation has exactly the same feasible flows and cost values
as standard pooling.

Apply Theorem 1 of the fixed-core block result with

```
r <= pK+pc+c^2,
d <= max(1,ph+ch+h^2),
k <= p(1+K)+2p+2cI+2cJ(1+K),
D=2.
```

It gives polynomial bit complexity, exact algebraic optimizer recovery,
and infeasibility detection. The cover search and construction are themselves
polynomial. This proves both structural statements, subject to independent
review of this mapping.

## 6. Scope and comparison

The earlier corollary allowed only a fixed number of bypass arcs by moving
all their flows into the core. A bounded bypass vertex cover permits an
unbounded number of arcs while keeping each remaining local block small.
The bounded-component extension also allows an unbounded matching of bypass
arcs, which has no bounded vertex cover. The more general deletion condition
combines these cases.

Arbitrary bypass graphs are not covered: after deleting a fixed number of
vertices they may still contain arbitrarily large connected components.
Bounding only the number of pools and quality attributes does not make the
local block dimensions or aggregate row count fixed for such graphs.

The algebraic algorithm and its complexity are inherited from the
[fixed-core theorem](../results/fixed-core-block-polyhedral-optimization.md).
The proof here is the pooling-specific structural decomposition. The
[existing bypass literature audit](pooling-single-quality-bypass-novelty.md)
compares the unrestricted bypass model with prior pooling claims; it does
not establish priority for this vertex-cover or bounded-component result.
A targeted search for this precise structural corollary remains necessary
before a literature novelty claim.

## 7. Graph terminology and targeted novelty search

The stronger deletion condition is equivalently bounded **vertex integrity**
of the bypass graph. This standard graph parameter is

```
iota(G) = min_W ( |W| + max_component |V(component of G-W)| ).
```

A fixed bound on `iota` supplies fixed `c,h`, and a fixed pair `c,h` supplies
`iota<=c+h`. Thus the main structural statement can also be stated as:
standard pooling is polynomial-time exactly solvable for fixed pool count,
quality count, and bypass-graph vertex integrity. The graph parameter and
its general graph-algorithm uses are established terminology; see
[Bentert, Heeger, and Koana, Fully Polynomial-time Algorithms Parameterized
by Vertex Integrity Using Fast Matrix Multiplication](https://arxiv.org/abs/2403.01839)
(abstract inspected). The pooling mapping above does not use their algorithms.

On 2026-09-05, searches combining pooling with `vertex cover`, `vertex
integrity`, `bypass`, `connected components`, and polynomial complexity found
no directly matching pooling theorem. The nearby
[Baltean-Lugojan and Misener article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/)
develops single-quality parametric methods under its specified flow-availability
relaxations; the source distinction is documented in the existing local
novelty audit. This limited targeted search does not establish priority.
