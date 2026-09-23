# Second audit: exact product contracts remove dense pool balances

Date: 2026-09-05. Reviewer: `pooling_all_two_review`. Full proof PASS.
Reviewed the complete [standalone draft](pooling-fixed-product-contracts-algorithm.md),
including its preprocessing, encoding, zero-throughput case, exact
reconstruction, economic objective, and stated exclusions.

## Assumptions and core

There is one pool, no pool-to-pool arc, a fixed number `r` of receiving
outputs, and bypass graph degree at most two. The receiving set contains
every output having an allowed pool arc, including zero-capacity arcs.
Every input has exact total supply `a_i`. Every nonreceiving output has
exact total demand `b_j` and an exact quality vector `Cbar_j`. All arc
and pool flow bounds are finite rational data. The number of inputs,
pool feeds, nonreceiving outputs, and quality coordinates can grow.

Keep every pool-output flow `v_j`, its outlet fraction `theta_j`, and
every bypass arc flow `z_ij` entering a receiving output. There are at
most `4r` retained variables. A zero-receiver pool is handled separately:
all pool flows vanish, inconsistent positive lower bounds are rejected,
and the remaining problem is a rational LP.

## Eliminate individual pool feeds locally

For an input with a pool arc, conservation determines its intake as

```
y_i = a_i-sum_(bypass arcs from i) f_ij.
```

Its upper and lower feed bounds are two-variable-per-inequality rows in
the at most two bypass flows. If the input has no pool arc, impose
`y_i=0`, which is the exact local supply equation. Other bypass-arc
bounds remain. These rows have constant rational coefficients; no
unknown pool-quality parameter enters them.

Every nonreceiving output has only its at most two bypass inlets.
Demand and exact quality rows are therefore ordinary two-variable
linear relations. Delete the receiving output nodes, treating their
incident bypass arcs as retained boundary coordinates. Every remaining
boundary component is a scalar path. Components without boundaries,
including cycles, are independent rational LP feasibility problems.

The reviewed exact endpoint projection applies to these static paths.
An isolated input with a pool arc simply has `y_i=a_i`; its feed bounds
must still be checked. An isolated input without a pool arc is feasible
only if its exact supply is zero. These are ordinary local cases.

## Verify both aggregate identities

Define, using only retained coordinates,

```
T = sum_i a_i - sum_(j nonreceiving) b_j - sum_(i,j receiving) z_ij,
Q_k = sum_i C_ik*a_i - sum_(j nonreceiving) Cbar_jk*b_j
      - sum_(i,j receiving) C_ik*z_ij.
```

For any lifted local feasible solution, exact input supply gives
`sum_i y_i=sum_i a_i-sum_all_bypass f_ij`. Exact demands at the
nonreceiving outputs then give `sum_i y_i=T`. The same calculation with
quality mass, using their exact quality contracts, gives
`sum_i C_ik*y_i=Q_k` for every quality coordinate.

Conversely these identities hold for every local lift, regardless of
which feasible internal bypass flows the path algorithm chooses. Thus
no dense pool sum was silently discarded: it is an affine consequence
of the exact local contracts and the retained boundary flows.

## Mixing, zero throughput, and quality rows

Impose nonnegative fractions with `sum theta_j=1` and
`v_j=theta_j*T`, together with all pool and receiving-output bounds.
At positive `T`, pool concentration is `q_k=Q_k/T`, and quality mass
sent to output `j` is exactly `theta_j*Q_k`. Receiving quality rows are
therefore polynomials of degree at most two in the retained variables.
Arbitrarily many attributes add rows but no further variables.

At `T=0`, the local nonnegative feed bounds and `sum_i y_i=T` imply
every `y_i=0`, hence every `Q_k=0`. Thus all pool-output flows and all
outgoing quality masses vanish, and any simplex outlet fraction is
harmless. A pool concentration can be assigned any admissible value
without affecting flow feasibility. Positive lower pool or outlet
bounds are still enforced and can make the instance infeasible.

The forward map uses the original outlet fractions at positive flow.
The reverse map lifts the path interiors, reconstructs all feed flows,
and uses the identities above to verify actual mixing at the pool.
This proves exact feasible projection under the stated contracts.

## Optimization and scope

For standard source production costs `c_i` and output revenues `R_j`,
profit is

```
-sum_i c_i*a_i + sum_(j nonreceiving) R_j*b_j
+sum_(j receiving) R_j*(v_j+sum_i z_ij).
```

It is a constant plus a linear core objective. Fixed-dimensional
semialgebraic optimization and the existing common-field path lift
therefore apply. The feasible core is closed and bounded, so every
nonempty instance attains its optimum. This covers the ordinary
source-cost/output-price objective; arbitrary unrelated costs on many
internal bypass arcs are not included.

The exact nonreceiving quality contracts are used as equalities of
actual quality mass, not merely as upper specifications. Replacing
`Cbar_jk*b_j` by an upper bound on that mass would invalidate the
aggregate identity. Likewise, variable total source supplies or
unfixed nonreceiving demands need additional retained information or
a separate argument. No such relaxation is part of this audit.

The draft's bounded additional-cost-coordinate remark is also valid.
For an additional cost on an intake `y_i` that was locally eliminated,
retain its at most two incident bypass coordinates (or retain the entire
input node and `y_i`) and cut the paths there. A fixed number of such
exceptions adds only a fixed number of core variables. For a designated
bypass arc, the usual path or cycle cut applies directly. This does not
extend to an unbounded number of unrelated intake costs.
