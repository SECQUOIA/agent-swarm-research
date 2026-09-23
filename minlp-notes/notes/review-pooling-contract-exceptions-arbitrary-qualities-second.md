# Independent audit: arbitrary qualities with bounded contract exceptions

Date: 2026-09-05. Reviewer: `pooling_all_two_review`.
Verdict: PASS for the complete candidate theorem, including exact standard
economic optimization and polynomial-encoding original witnesses.

Promoted theorem: [arbitrary-quality contract-exception algorithm](../results/pooling-contract-exceptions-algorithm.md).
This audit checks the new rank-removal arguments separately from the
previous scalar and fixed-rank reviews. The active-product affine-space
idea was proposed by this reviewer; the author supplied the full synthesis
and exceptional-only branch. A separate reviewer should therefore also
audit this theorem before promotion.

## 1. An active ordinary product bounds parameter dimension

For an ordinary product with positive pool flow, exact mass and vector
quality give

```
v q + sum_i C_i z_i = b B,
v + sum_i z_i = b.
```

Since `v>0`, division expresses `q` as an affine combination of `B` and
the bypass input vectors, with coefficients summing to one. There are
at most two bypass inlets, so their affine hull has dimension at most
two. Nonnegative coefficients are not claimed or needed: the source
coefficients in this expression are negative. The actual pool balances
separately enforce that `q` is a convex combination of its intake vectors.

It is enough to enumerate positive-demand ordinary products and solve
the original model restricted to each resulting affine space. A branch
need not impose positive flow at its selected output, because all its
solutions still satisfy the complete original model. Every original
solution with an active ordinary product belongs to some enumerated
branch. Zero-demand products cannot serve as active anchors and are
correctly omitted. Products without pool arcs can harmlessly contribute
extra sound branches but are not needed for coverage.

Rational bases of dimension zero, one, or two have polynomial encoding.
Their intersection with the allowed-feed coordinate box yields finite
bounds on the affine coordinates by selecting independent coordinate
rows and applying a rational left inverse. Retaining every box row
preserves the intersection exactly. There is no unbounded hidden
parameterization or need to solve a high-dimensional hull problem.

## 2. Ambient dimension does not enter the nonlinear core

The fixed-rank chart proof only needs a fixed-dimensional parameterization
of `q`; it does not require all source vectors to lie in its affine space.
This distinction is necessary for the new theorem.

For arbitrary ambient dimension `K`, each nonzero vector `C_i-q` defines
a nonzero polynomial in integer `k` of degree at most `K-1` through
the moment-curve direction. At most `|I|(K-1)` integers are forbidden.
The proposed polynomial-size family covers every `q` unequal to all
source vectors. Its coefficients have polynomial bit lengths, even
though their magnitudes grow with `K`. Source-vector equality cases
are separately solved as original rational fixed-quality LPs. Zero
quality count is an LP and dimension-zero quality spaces are LPs.

After affine substitution with at most two parameters, each scaling and
each additional-coordinate coefficient `a_h` remains affine. The exact
identity producing `a_h w=f_h` is an ambient-vector identity; cancellation
does not assume any relation among source vectors. Its right-hand side
remains quadratic. All `K` coordinate equations are retained. Equal
projections and zero coefficient strata retain their parameter equations,
so no vector condition disappears.

There are polynomially many affine sign cells in parameter dimension
at most two. Each connected path/cycle cut crosses at most two internal
arcs. Candidate lists can grow with `K`, but their pairwise combinations
and constant-degree denominator clearing remain polynomial. Ambient
quality coordinates add rows and coefficient bits, not core variables.
The same observation applies to the global quality balances and
exceptional quality requirements. Thus the fixed-dimensional elimination
and common-field reconstruction arguments still apply.

## 3. Exceptional-only pool outlets

In the remaining branch every ordinary pool outlet is forced to zero,
including checking its lower bound. There are then at most `|E_J|`
possible active outlets. Retaining exceptional feeds, exceptional-incident
bypass flows, these outlets, and their fractions gives at most
`3|E_I|+4|E_J|` coordinates. Arcs shared by two exceptions are counted
once. If there are no exceptional pool outlets, forcing all pool arcs
to zero gives the original residual LP with external contracts retained.

For each ordinary input its intake is exact supply minus bypass total,
with an exact zero residual when no pool arc exists. Ordinary products
are bypass-only and retain all their exact vector quality equations.
These are rational linear constraints on at most two bypass variables.
The reviewed path/cycle endpoint projection therefore applies without
any symbolic quality parameter. Exceptional boundary flows remain core
coordinates; detached components are ordinary LP conditions.

Let `S,G` be total input throughput and vector quality mass, with
exceptional totals computed from their retained actual feed and bypass
arcs. The ordinary exact products account for all bypass arcs into
ordinary outputs. The retained bypass arcs into exceptional outputs
account for all other bypasses. Consequently

```
T=S-sum_ordinary b_j-sum_bypass_to_exception z_ij,
Q=G-sum_ordinary b_j B_j-sum_bypass_to_exception C_i z_ij
```

equal `sum_i y_i` and `sum_i C_i y_i` for every local lift. This is not
merely a consistency condition for some specially selected lift. It
also includes flows from exceptional inputs into ordinary products and
from ordinary inputs into exceptional products, since the sums partition
arcs by output endpoint.

Fractions satisfying `theta>=0`, `sum theta=1`, and `v_j=theta_j T`
therefore give actual pool mass conservation. At positive throughput,
the actual pool quality is `Q/T`, and `theta_j Q` is exactly the mass
delivered to output `j`. At zero throughput, nonnegative reconstructed
intakes all vanish and hence `Q=0`; arbitrary simplex fractions then
introduce no spurious quality mass. Conversely actual physical flows
supply these fractions when active, or any simplex point when inactive.
All exceptional quality inequalities use the full vector mass, so
arbitrary ambient dimension causes no loss of information.

## 4. Optimization, encoding, and limitations

Ordinary source and product throughputs are fixed. Standard economics
therefore consists of their constant contribution and the exceptional
core throughputs. This remains affine before adding the usual
objective-value variable. All branch constraints have bounded degree
and fixed core dimension. The number of branches, rows, coefficient
bits, and quality charts is polynomial in the original input length.

Each branch is sound and the branches cover every original feasible
flow. Their attainable-value union has an attained maximum because the
original bounded physical model with the quality box is compact. Strict
chart conditions must remain strict; the proof does not take invalid
closures across vanishing denominators. The exceptional-only branch
is a closed bounded formulation on flows and fractions.

The sampled optimal core and incidence or rational path lifting stay
in one polynomial-degree real algebraic field with polynomial coefficient
length. In the exceptional-only branch, reporting active quality uses
one division by `T`; inactive quality can be any rational allowed feed
vector. No claim of a quadratic field, practical runtime, dense arc-cost
optimization, or arbitrary contract exceptions follows.

The theorem retains exact ordinary flow and quality contracts, fixed
exception count, bypass degree two, and redundant common pool capacity.
It does remove the fixed quality count and fixed affine input rank.
This audit is mathematical; the earlier chart and physical mapping
checks support its dependencies, but I did not claim a numerical test
of the full arbitrary-dimensional algebraic optimizer. Literature
priority remains a separate qualified assessment.
