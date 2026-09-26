# Candidate: polynomial pooling optimization with bounded contract exceptions

Date: 2026-09-05. Status: complete scalar-quality candidate. Two
independent audits,
[benders_review](review-pooling-bounded-contract-exceptions-benders.md) and
[pooling_all_two_review](review-pooling-bounded-contract-exceptions-second.md),
report PASS for the stated scalar model and exact optimization conclusion
(fixed number of exceptional external nodes, redundant common pool bounds).
Separate literature priority is provisional.

The proposed theorem allows one pool, arbitrarily many pool feeds and
outlets, and degree-two bypasses. All but a fixed number of external
nodes have exact flow contracts; contracted outputs also have exact
quality specifications. The remaining nodes may have ordinary interval
requirements. Standard economic profit can vary and is optimized exactly.
The common pool-throughput bounds must be redundant.

## 1. Precise model

Let `I` and `J` be inputs and outputs, with known rational scalar input
qualities `C_i`. There is one pool and no pool-to-pool arc. Arbitrarily
many input-pool and pool-output arcs are allowed. Every individual arc
has finite rational lower and upper bounds including nonnegativity.
The bypass graph, containing only direct input-output arcs, has maximum
degree two.

Designate exceptional node sets `E_I subset I` and `E_J subset J`, with
`s=|E_I|+|E_J|` fixed independently of the input size. Every input outside
`E_I` has exact total supply `a_i`; every output outside `E_J` has exact
demand `b_j` and exact quality `B_j`. At exceptional inputs use arbitrary
rational lower/upper supply bounds. At exceptional outputs use arbitrary
rational lower/upper demand and quality bounds. Zero-demand exact quality
means its homogeneous quality-mass equality.

The common pool-throughput lower bound is zero, and its upper bound
is redundant. A sufficient certificate is that the upper bound is at
least the minimum of three readily computed bounds: the sum of valid
input-throughput upper bounds, the sum of allowed pool-feed arc
capacities, and the sum of allowed pool-outlet arc capacities. An
omitted common bound can equivalently be supplied with this finite
value. Individual pool arc bounds are retained. Source throughput
upper bounds are finite and can also be computed by summing capacities
of incident arcs. No nonredundant common pool restriction is included.

The objective is ordinary profit: output unit revenues times actual
output throughput, minus input unit production costs times actual input
throughput. All coefficients are rational. Unrestricted separate costs
on individual arcs or on common pool throughput are outside this theorem.

**Candidate theorem.** For fixed `s`, feasibility and exact maximum
profit are computable in polynomial rational bit time, with an exact
real-algebraic optimal original flow when feasible. The number of feeds,
outlets, contracted nodes, and distinct scalar input qualities may grow.
The exponent may depend on `s`; no practical runtime or strongly
polynomial guarantee is asserted.

If the pool has no allowed feed or no allowed outlet, force every pool
arc to zero, reject incompatible positive lower bounds on those arcs,
retain the external requirements, and solve the ordinary rational LP.
Below both kinds of pool arc exist. A valid compact concentration range
is the interval spanned by the allowed feed qualities. Inactive pools
can be assigned any value in that interval.

## 2. A fixed set of original boundary coordinates

Retain the pool arc incident to each exceptional node, when present,
and every bypass arc incident to an exceptional node. There are at most
`s` retained pool arcs and `2s` retained bypass arcs. Denote this set of
bypass arcs by `H`. An arc joining two exceptional nodes is retained
only once. Keep the pool concentration `q` as well.

For an exceptional input let

```
A_i = y_i + sum_j z_ij,
```

where a missing feed has `y_i=0`. For an exceptional output let

```
D_j = v_j + sum_i z_ij,
M_j = q*v_j + sum_i C_i*z_ij,
```

where a missing outlet has `v_j=0`. Every expression uses retained
coordinates only. Preserve all their node and arc bounds and all
exceptional-output quality inequalities `lower_j D_j<=M_j<=upper_j D_j`.
These are polynomials of degree at most two.

At every nonexceptional input eliminate its intake locally as
`Y_i=a_i-sum_j z_ij`, retaining the allowed inlet bounds or `Y_i=0`
if its inlet is absent. At every nonexceptional output eliminate its
outlet as `V_j=b_j-sum_i z_ij`, retaining its bounds or `V_j=0` when
absent. The output's exact quality equation becomes

```
sum_i(C_i-q) z_ij = b_j(B_j-q).                      (1)
```

Every local row involves at most two neighboring bypass coordinates.

## 3. Global conservation supplies exactly two core equations

Impose

```
sum_(i outside E_I) a_i + sum_(i in E_I) A_i
 = sum_(j outside E_J) b_j + sum_(j in E_J) D_j,       (2)

sum_(i outside E_I) C_i*a_i + sum_(i in E_I) C_i*A_i
 = sum_(j outside E_J) B_j*b_j + sum_(j in E_J) M_j.  (3)
```

Both are core equations; (2) is linear and (3) has degree at most two.
For any bypass assignment satisfying all local rows and these equations,
summed pool intake equals total input throughput minus total bypass
throughput. Summed pool outlet equals total output throughput minus the
same bypass throughput. Equation (2) therefore gives actual pool flow
conservation.

For quality, sum (1) over all nonexceptional outputs and add the actual
mass expressions `M_j` at exceptional outputs. Equation (3) then gives

```
q * sum_all_outputs pool_outlet
 = sum_all_inputs C_i * pool_intake.
```

This is the actual pool quality balance. If pool throughput is zero,
nonnegativity forces every pool arc to zero; no division by throughput
or extra concentration requirement is needed. If throughput is positive,
this equation makes `q` its actual weighted-average quality. The common
pool-capacity bounds are automatic by the stated redundancy assumption.

Conversely every original feasible flow satisfies (1)--(3). Thus the
remaining difficulty is exact elimination of the residual bypass paths,
without losing their retained boundary flows.

## 4. Quality-scaled incidence flow inside each residual component

At every distinct input quality `q=C_i` in the search interval, solve
the original fixed-concentration LP, including the actual pool balances
and the original economic objective. These are polynomially many
rational LPs and cover all singular values of the transformation below.

On an open interval between successive input quality values, set

```
gamma_i(q)=C_i-q,
w_ij=gamma_i(q) z_ij.
```

Every gamma is nonzero with fixed sign. For each retained bypass arc,
keep an additional transformed coordinate `w_ij` and impose its bilinear
link to its original flow. The core now has at most `1+5s` variables.

For internal nodes use the exact
[quality-scaled flow transformation](pooling-quality-scaled-path-flow.md).
Its input rows become intervals on node divergence, with affine bounds
in `q`. Equation (1) becomes the exact output node equation
`sum_i w_ij=b_j(B_j-q)`. If an output has two bypass inlets with unequal
source qualities, its outlet-flow interval becomes an additional interval
on one selected incident transformed arc, with quadratic polynomial
endpoints in `q`. Equal source qualities give parameter-only conditions
instead. One or zero inlet cases are treated directly. Original bypass
bounds become affine transformed bounds. Signed transformed flows are
permitted throughout.

Delete the exceptional nodes. Every remaining component is a path,
cycle, or isolated node. Remove each retained boundary arc from its
internal component and shift its signed prescribed `w_ij` contribution
from the adjacent node-divergence interval. Preserve every original or
derived capacity bound on such a boundary arc as a core inequality.
A retained arc joining two exceptional nodes needs no interior projection.

Each component is now an incidence-flow problem with interval node
imbalances, bounded internal arcs, and at most two fixed boundary
coordinates. Its node bounds are affine in `q` and linear in these
boundary coordinates. Every internal arc has constantly many lower
and upper candidates that are polynomials of degree at most two in `q`.

## 5. Polynomial cut projection

For fixed transformed arc bounds `ell<=u` and node-divergence intervals
`alpha<=beta`, incidence feasibility is equivalent to the two Hoffman
inequalities for every node subset `S`:

```
sum_S alpha <= u(delta_plus(S))-ell(delta_minus(S)),
sum_S beta  >= ell(delta_plus(S))-u(delta_minus(S)).   (4)
```

The signed-flow convention and a proof by adding root arcs are given
in the linked transformation note. If an induced subset is disconnected,
its node sums and cut terms add over its connected components. Thus only
connected subsets need be tested. A path or cycle has only quadratically
many such subsets, including the entire component.

Each
connected path/cycle cut crosses at most two internal edges. Substitute
every combination of their lower/upper candidate endpoints in (4);
there are constantly many combinations. Add every lower-candidate versus
upper-candidate consistency inequality for each internal edge. The
result is equivalent to using the effective maximum lower and minimum
upper bounds. The construction covers isolated internal nodes and paths
whose two boundary arcs meet the same exceptional node. This gives polynomially many quadratic rows directly on
each original input-quality sign interval.

This description has polynomial rational coefficient lengths: only
constant-degree products, divisions by fixed nonzero differences of
input qualities, and polynomially many sums occur. All remaining core
conditions have degree at most two and dimension at most `1+5s`.

## 6. Exact global decision, optimization, and recovery

For each nonempty parameter cell, use fixed-dimensional real-algebraic
decision on its core equations, physical bounds, and projected cut rows.
Open interval endpoints remain strict constraints; singular concentration
values have already been handled by the original LPs. Polynomially many
cells and fixed-dimensional algebra give polynomial total bit complexity.

The economic objective reduces to

```
sum_(j outside E_J) R_j*b_j - sum_(i outside E_I) c_i*a_i
 + sum_(j in E_J) R_j*D_j - sum_(i in E_I) c_i*A_i.    (5)
```

It is affine in the original core flow coordinates. Optimize it exactly
by eliminating the fixed number of core coordinates from the formula
for its attainable values on each cell, then taking the union with the
attainable values of the singular fixed-concentration LPs. There are
polynomially many univariate descriptions of polynomial degree and
encoding length. The original feasible set, with concentration in the
chosen closed interval, is compact and closed. Therefore the union has
an attained largest value whenever it is nonempty. Select that value
and sample a core point in a cell attaining it.

It is not valid simply to close every open parameter cell and optimize
its raw polynomial rows at the boundary: after a coefficient vanishes,
those rows can lose information. The attainable-value procedure and
separate singular LPs avoid that issue.

Given a core sample, solve each residual signed incidence system over
its common represented real-algebraic field. Lower-bound shifts and
circulation algorithms use sums and exact comparisons. Alternatively,
its incidence matrix gives vertex coordinates that are rational linear
combinations of the sampled node and arc bounds. All transformed flows
therefore have polynomial encoding in the same field. Recover internal
bypass flows by one division `z_ij=w_ij/(C_i-q)` per arc, and recover
nonexceptional pool arcs from the local supply/demand identities. The
core already contains exceptional pool arcs. Equations (2)--(3) verify
the reconstructed physical pool, including its zero-flow case.

The algebraic core has polynomial degree and encoding because its
variable count is fixed. No unrelated parameter fields are combined.
This proves exact constructive feasibility and optimization, conditional
on the independently reviewed transformation and cut lemma.

## 7. Scope and current status

The theorem concerns a fixed number of exceptions to exact external flow
and product-quality contracts. It is stronger than the fully contracted
constant-profit case, but does not settle general one-pool feasibility
with arbitrary supply and product intervals. It does not cover a
nonredundant common pool-throughput bound or unrestricted separate arc
costs. A fixed number of additional cost-bearing arcs can be handled by
retaining their endpoints as further exceptional nodes while preserving
any existing contracts there.

The earlier generic one-parameter polygon theorem already gives a safe
quasipolynomial route to the same fixed-exception model: replace Section
5 by its balanced parameter-cell decomposition, then use the same fixed
core and attainable-value optimization. The incidence transformation is
the additional physical structure that gives the proposed polynomial
bound. Both routes require the exact conservation identities, not merely
a bounded number of aggregate rows.

Fresh full proof audits and the targeted primary-source comparison are
in progress. The circulation theorem and algebraic algorithms are
established tools; separate priority for this physical pooling
classification remains provisional.
