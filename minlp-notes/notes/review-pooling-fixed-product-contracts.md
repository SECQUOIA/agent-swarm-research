# Independent review: fixed product contracts and unbounded pool feeds

Date: 2026-09-05. Verdict: **PASS** for the main feasibility and standard
economic optimization theorem in
[the full draft](pooling-fixed-product-contracts-algorithm.md).
The optional sparse-intake-cost extension is valid with the explicit
coordinate retention described below. Literature priority remains
separate from this mathematical audit.

## Local intake elimination

Exact total input supply gives `Y_i=a_i-sum_j z_ij`. With bypass
degree at most two, each inlet lower/upper bound becomes a linear row
on at most two bypass coordinates. If the input has no pool arc,
`Y_i=0` is the exact remaining source balance. Conversely these rows
and bypass bounds recover a valid intake and the exact source supply.
Inputs with no bypass arcs give only constant checks and constant
intakes. A positive external supply with no usable output arc is
rejected by its local equation, not silently discarded.

At a nonreceiving output, its exact demand and exact quality are
precisely the displayed linear total-flow and attribute-mass equations.
They again have at most two bypass coordinates. At zero demand,
nonnegative flows vanish and the homogeneous quality equations have
zero right-hand side; no positive-flow requirement is introduced.

## The two conservation identities

Let `H` consist of bypass arcs into pool-receiving outputs. Substituting
the intake equations and partitioning all bypass arcs by destination
gives

```
sum_i Y_i - T
 = sum_(j outside J_P) (b_j-sum_i z_ij),

sum_i C_ik Y_i - Q_k
 = sum_(j outside J_P) (b_j B_jk-sum_i C_ik z_ij).
```

Every term on the right vanishes by a retained local product contract.
These exact identities establish that the global pool total and every
attribute mass are functions of the boundary coordinates alone. There
is no dense aggregate constraint left to impose after projection.
Merely fixing nonreceiving demands would establish the first identity
but would not fix the second; exact quality contracts are essential.

This also justifies independently solving detached bypass components
that contain pool-feeding inputs. Their individual recovered intakes
may vary, but their total intake and total attribute masses are fixed
by the same component-wise conservation identities. Independent choices
cannot change the quantities seen by the core.

Nonnegative intake bounds imply `T>=0`. If `T=0`, every intake is zero
and the attribute identity gives `Q_k=0` even for signed attribute
values. Thus cancellation in the formula for `Q` cannot produce a
spurious nonzero mass at zero pool throughput.

## Core dimension, projection, and equivalence

There are at most `2r` arcs in `H`, because each receiving output has
bypass degree at most two. Its `r` pool outlet flows and `r` outlet
fractions give at most `4r` core variables. Receiving outputs are
defined by allowed pool arcs, including zero-capacity ones, so the
count and the exact-contract assumptions do not change with the
eventual flow pattern.

Deleting only those receiving output nodes leaves paths, cycles, and
isolated vertices in the bypass graph. A path meets the deleted set
through at most two boundary arcs. Its input relations already contain
the eliminated-intake bounds, and its output relations contain exact
product equations. They are constant-coefficient scalar 2VPI relations,
so the previously reviewed bounded polygon composition applies.
A cycle broken at one receiving output has two different endpoint arc
coordinates even though their deleted endpoint node is the same.
No-boundary components need only rational LP feasibility and recovery.

All core quality masses are `theta_j*Q_k` plus receiving bypass mass.
These are quadratic polynomials in fixed dimension. The number of
attributes adds rows, not variables. Fraction simplices, finite arc
bounds, and closed capacity/quality rows make the projected core
compact. Fixed-dimensional algebraic decision or optimization supplies
an exact sample with polynomial encoding length. Affine path recovery
stays in its common real-algebraic field. Recovered intakes are affine
expressions in the resulting bypass flows.

At `T>0`, set pool quality `q_k=Q_k/T`. This is in the same algebraic
field and has polynomial representation length by exact field
arithmetic. Its outgoing mass is `q_k*v_j=theta_j*Q_k`. At `T=0`,
all pool flows and masses are zero; legal outlet fractions are harmless
and an arbitrary admissible inactive-pool quality can be chosen. Thus
each lifted core point is an original physical feasible state. The
reverse construction uses actual outlet fractions at positive throughput
and any simplex vector at zero. Both directions preserve every node,
pool, arc, and quality requirement in the draft's model.

For `r=0`, all pool intakes are forced to zero. Checking only the
pool/incident-arc bounds against zero and retaining every external-node
contract leaves an ordinary bounded rational LP, as stated. This
preprocessing does not discard product requirements that still need
to be met by bypass flow.

## Objective and scope

All input production costs multiply prescribed totals `a_i`, and all
nonreceiving revenues multiply prescribed demands `b_j`. Their sum is
constant. Receiving revenue, pool-throughput cost, and costs on the
fixed set of pool-output arcs depend only on the retained coordinates.
Consequently compact core optimization gives exact global economic
optimization, and every subsequent path lift preserves its value.

Arbitrary separate intake costs become a potentially dense bypass
objective after substitution; arbitrary bypass costs are already dense.
The theorem correctly excludes them. For a fixed number of designated
intake costs, retain each such input's at most two incident bypass
coordinates before projection. Its intake then becomes an affine
function of the enlarged fixed core. Fixed many designated bypass
costs use the earlier path-cut extension directly. This clarifies the
optional sparse-support statement without changing the main theorem.

No fixed input-quality alphabet, affine quality rank, or feed count
is used anywhere in the proof. In contrast, finite bounds, exact
source totals, exact nonreceiving demand and quality, one pool, and
fixed outlet count are substantive assumptions. The argument does not
extend them to interval contracts or arbitrary unbounded attachments.

The new proof is a conservation reduction to the already independently
checked projection and algebraic tools. I subsequently inspected
[the author's substitution checker](../code/pooling_bypass_paths/check_fixed_product_contracts.py)
and its original/substituted fixed-split LP formulations. The recorded
[log](../code/pooling_bypass_paths/fixed_product_contracts_output.txt)
reports 90 comparisons (180 LP solves), with 63 feasible fibers,
covering one to three attributes, forced-zero feeds, zero pool capacity,
and zero outlet fractions. Its separate control confirms that treating
an upper-only nonreceiving quality specification as an exact mass
can create a false feasible substituted instance. These numerical LP
checks support the new mass and objective identities; they do not
test endpoint elimination or a complete global algebraic solver.
