# Second independent review: fully contracted pooling with unbounded attachments

Date: 2026-09-05. Verdict: **PASS** for
[the candidate theorem](pooling-all-product-contracts-quasipolynomial.md).
The quasipolynomial bound and polynomial-size algebraic witness follow
under the stated exact-contract and redundant common-capacity assumptions.
Separate literature priority is not established.

## Exact physical equivalence, including zero flow

Exact input and output totals determine every pool arc locally as
`Y_i=a_i-sum_j z_ij` and `V_j=b_j-sum_i z_ij`. An absent pool arc
requires the corresponding expression to be zero; an allowed arc
requires its original lower/upper bounds. These substitutions preserve
all external contracts and pool-arc restrictions exactly. Each node
has at most two bypass variables, so the resulting rows are scalar
2VPI relations. All original bypass bounds remain finite.

The two global rational equalities are necessary and must be checked
before discarding pool balances. Summing local source/output equations
gives total pool conservation from the first equality. Summing all
exact output quality rows and using the second equality gives
`q*sum_j V_j=sum_i C_i Y_i`. These are identities on the proposed
local feasible set, not omitted constraints whose validity is assumed.
At a nonreceiving output, the ordinary quality row and `V_j=0` give
exactly the same identity as the parameterized version.

If the common throughput is positive, the scalar equality identifies
`q` with the actual convex average of nonnegative input flows. If it
is zero, all nonnegative feed and outlet flows vanish separately;
quality mass is zero and no concentration constraint is physically
needed. Choosing any value between the minimum and maximum quality
of allowed feeds is then harmless. At positive throughput that same
interval necessarily contains the mixture. Zero-capacity feed arcs
may widen this interval, but do not introduce a spurious feasible
physical state because the local intake bounds and mixing identity
still hold.

The redundant common upper capacity follows from
`sum_i Y_i<=sum_i a_i`, since every bypass flow is nonnegative.
The stipulated zero common lower bound is automatic. A pool missing
all inlets or all outlets forces all its arcs to zero; the stated
preprocessing correctly checks those arc bounds while retaining
external-node contracts. Zero total network supply, zero-demand
products with arbitrary declared quality, and an interval of constant
pool quality are all covered without dividing by throughput.

## Components and the parameter projection dependency

The bypass graph consists of paths, cycles, and isolated vertices,
even though the pool may connect these components through many arcs.
After the conservation identities above, their only remaining shared
quantity is the common scalar `q`. A detached bypass component may
still contain many pool feeds/outlets; it requires no additional
aggregate compatibility constraint.

I checked the cited
[one-parameter path theorem](one-parameter-path-projection-investigation.md)
and its two completed audits against this application. Its assumptions
hold directly: uniformly bounded scalar coordinates, coefficient
polynomials of degree at most one in a compact rational parameter
interval, and explicit input encoding. The crucial proof ingredients
are balanced composition with polynomial retained row counts, sign
partitioning of Fourier–Motzkin multipliers, and augmented minors that
preserve planar feasibility and redundancy, including lower-dimensional
fibers. The current pooling synthesis adds no extra path coordinate or
global dense row that would violate those assumptions.

A cycle is opened at one arc coordinate, producing two occurrences
of that same coordinate at the chain endpoints. Intersecting the
endpoint relation with `x=z` restores precisely the original cycle.
The equality adds only two fixed linear rows; the inherited coordinate
bounds keep the endpoint relation compact. Adding their minors to
the final sign refinement therefore makes cycle nonemptiness constant
on every open parameter cell, just as for a path. Boundary parameters
are checked separately and are not inferred from adjacent cells.

For an isolated input or output, the relevant eliminated flow is
constant. Check its bounds directly. A positive fixed outlet requires
`q=B_j`; a zero outlet imposes no quality equation on `q`. An absent
arc may instead make the prescribed throughput impossible. These
scalar equalities or constant tests fit the same parameter partition.

## Quasipolynomial time and one common witness field

Every component has at most `N^(O(log(N+1)))` parameter cells. Adding
the final planar feasibility refinement is only a polynomial factor:
there are polynomially many rows, degree-polynomial coefficient and
augmented-minor polynomials, and polynomially many roots per cell.
All breakpoints have polynomial algebraic degree and coefficient
height relative to the original input length.

In one parameter, components' partitions are overlaid by sorting the
union of their breakpoints. This operation sums cell counts rather
than taking their product. There are at most `N` components, so a
polynomial number of further membership or sign checks per resulting
cell preserves the quasipolynomial total bound. Coefficients and
root descriptions remain polynomial size throughout.

Rational samples between distinct algebraic endpoints have polynomial
bit length. A root-separation bound can be applied to each pair of
their degree/height-bounded defining polynomials; no product of all
quasipolynomially many boundary polynomials is required. Singleton
samples have the same polynomial algebraic degree and height. This
handles both interval and isolated feasible concentration choices.

After one feasible `q` is selected, every component uses the same
field `Q(q)`. No compositum of independently selected parameter fields
is formed. Original component LP vertices are ratios of determinants
of matrices whose entries are affine in that one parameter. Their
degrees and coefficient heights are polynomial in the full input.
The reviewed balanced interval lifting is constructive with the same
bound when retained as rational-function expressions; it does not
rely on a blanket claim that arbitrary repeated algebraic inversions
preserve small height. Summing bypass flows to recover `Y_i,V_j`
also has polynomial encoding length. Thus the full output witness,
not just its parameter, has polynomial size.

## Capacity counterexample and objective scope

For the two-source/two-product example, exact local rows give
`Y_clean=V_A=1/(2q)` and
`Y_dirty=V_B=1/(2(2-q))`. Individual unit capacities force
`1/2<=q<=3/2`, and the common throughput is
`1/(q(2-q))>=1`. At `q=1` all local rows are feasible, but a common
upper capacity `3/4` excludes every physical state. The example has
balanced global flow and attribute totals, so it specifically proves
that a nontrivial common pool cap is not implied by those identities.
It is a scope counterexample, not a hardness result.

All exact input supplies and output demands make standard production
costs and product revenues constant. The theorem is therefore a
feasibility algorithm. Arbitrary arc costs and nonconstant pool
processing costs would require information that the endpoint-only
projection does not retain, and are correctly excluded.

## Inspected implementation support

I inspected and independently reran
[check_all_product_contracts.py](../code/pooling_bypass_paths/check_all_product_contracts.py).
The original LP contains all actual pool arcs and both pool balances;
the comparison LP contains only local bypass rows plus the checked
global constants. It passed 235 fixed-concentration comparisons,
78 feasible, including cyclic bypass graphs and missing attachments.
The three controls for omitting global flow balance, omitting global
quality balance, and imposing a restrictive common capacity also
passed. These are numerical LP consistency checks with small rational
input data. They test the new elimination mapping, not a symbolic
parameter-partition implementation or the asymptotic complexity proof.

## Affine-rank-one multiattribute addendum

The proposed extension to arbitrarily many attributes of input affine
rank at most one is also valid. In rank one, compute rational
`C_i=C0+d*t_i` with `d!=0`. Every positive-demand output must have
`B_j=C0+d*t_j`; otherwise no convex mixture of source qualities can
meet its exact quality. Zero-demand output specifications are irrelevant.
Choose any coordinate with `d_k!=0` to compute the scalar coordinates
and check all remaining coordinates for consistency.

Exact output total flow cancels the constant vector `C0` from each
quality equation; the remaining vector equation is equivalent to its
single scalar `t` equation. The same cancellation applies to global
quality conservation. The pool concentration is represented by a
single scalar between the minimum and maximum allowed-feed `t_i`.
All transformations have polynomial rational bit length, so the
quasipolynomial algorithm applies unchanged. Rank zero leaves constant
quality: reject positive-demand products with a different vector,
then solve the resulting rational LP. No higher-rank extension follows
from this one-parameter argument.
