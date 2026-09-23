# Quality-scaled flows give polynomial contracted pooling feasibility

Date: 2026-09-05. Status: verified theorem; two independent complete
proof audits PASS. See the [first review](../notes/review-pooling-quality-scaled-path-flow.md),
[second review](../notes/review-pooling-quality-scaled-path-flow-second.md),
and [focused source assessment](../notes/pooling-quality-scaled-contracts-novelty.md).
No matching restricted theorem was found in the checked sources; separate
priority is not established.

**Later strengthening.** The [common-capacity algorithm](pooling-contracted-common-capacity-algorithm.md)
removes the redundant common pool-bound hypothesis below. It allows an
arbitrary common lower/upper throughput interval, with polynomial-degree
algebraic witnesses. This result retains the simpler quadratic-field
certificate for the original redundant-capacity class.

The fully contracted one-pool class admits a polynomial algorithm,
improving the previously reviewed quasipolynomial bound. Scaling a bypass
flow by its source quality minus the pool quality converts the local
system to an ordinary incidence-flow system with quadratic parameter
bounds. A degree-two bypass graph then needs only polynomially many
connected cut inequalities. This note proves the transformation and the
cut description separately so they can be reused with fixed boundaries.

## 1. Physical model and theorem

Use the exact model of the
[fully contracted investigation](../notes/pooling-all-product-contracts-quasipolynomial.md):
one pool, one conserved scalar quality, known rational input qualities
`C_i`, exact input supplies `a_i`, exact output demands `b_j`, and exact
output qualities `B_j`. All arc bounds are finite rational intervals
including nonnegativity. The bypass graph has maximum degree two.
The number of pool inputs and outlets is unrestricted. The common pool
throughput lower bound is zero and its upper bound is at least
`sum_i a_i`, so those common bounds are redundant. There are no
pool-to-pool arcs.

**Theorem.** Feasibility is decidable in polynomial rational
bit time. If feasible, an original feasible flow can be found whose
coordinates all belong to one real field of degree at most two over
the rationals and have polynomial encoding length. The degree bound
is an upper bound, not a claim that an irrational witness is necessary.

Check the necessary global constants

```
sum_i a_i = sum_j b_j,
sum_i C_i*a_i = sum_j B_j*b_j.                         (1)
```

As in the reviewed conservation proof, eliminate every pool feed and
outlet locally:

```
Y_i=a_i-sum_j z_ij,
V_j=b_j-sum_i z_ij.
```

An absent pool arc means its eliminated flow is zero. Its allowed
counterpart retains all individual flow bounds. Exact output quality is

```
sum_i (C_i-q)*z_ij = b_j*(B_j-q),                     (2)
```

where `q` is the pool concentration. Equations (1), all local input and
output conservation equations, and (2) imply both actual pool balances.
This identity is already independently reviewed; in particular it is
valid at zero throughput, where all nonnegative pool arc flows vanish.

If there is no allowed pool feed or no allowed pool outlet, force every
pool arc to zero, check its bounds, retain all external contracts, and
solve the remaining rational LP. Otherwise it suffices to search
`q` in the interval spanned by the allowed pool-feed qualities.

## 2. Separate singular quality values

Let `gamma_i(q)=C_i-q`. For every distinct input quality `C_i` in the
search interval, solve the original fixed-`q` physical LP. It includes
all actual pool arcs and both pool balances, which are linear at fixed
`q`. There are only polynomially many such cases, and all their
coefficients are rational. Include every search-interval endpoint.

It remains to consider the open intervals between these values. On any
one of them every `gamma_i` is nonzero with fixed sign. The following
change of variables is invertible on that interval:

```
w_ij=gamma_i(q)*z_ij,
z_ij=w_ij/gamma_i(q).                                 (3)
```

The transformed flows may be negative. The incidence-flow theorem used
below permits signed arc and node bounds; no nonnegativity assumption
is imposed on `w` itself.

## 3. Input rows and original arc bounds

Suppose input `i` has allowed feed bounds `[ell_i^P,u_i^P]`. Its total
bypass flow must lie in

```
A_i=a_i-u_i^P <= sum_j z_ij <= a_i-ell_i^P=D_i.
```

For an absent feed arc use `A_i=D_i=a_i`. Multiplication by
`gamma_i` gives an interval bound on `sum_j w_ij`, with endpoints
`gamma_i*A_i` and `gamma_i*D_i`, in the order dictated by its fixed
sign. These endpoints are affine in `q`.

Each original bypass bound `ell_ij<=z_ij<=u_ij` likewise becomes an
interval bound on `w_ij` whose endpoints are the two affine polynomials
`gamma_i*ell_ij` and `gamma_i*u_ij`, in the appropriate order.

Direct each bypass edge from its input to its output, keeping this
orientation even when its transformed flow is negative. An input's
net outgoing transformed flow is exactly `sum_j w_ij`, so the preceding
input rows are interval bounds on node divergence.

## 4. Output rows become node equations and single-arc bounds

Equation (2) becomes

```
sum_i w_ij=R_j(q),  R_j(q)=b_j*(B_j-q).               (4)
```

It is an exact node-divergence condition at the output: its net outgoing
flow is `-R_j(q)`. All coefficients of the transformed node-arc matrix
are therefore constants in `{0,1,-1}`.

Let the allowed outlet bounds be `[ell_j^P,u_j^P]`, or `[0,0]` if the
outlet is absent. Its total bypass flow must satisfy

```
L_j=b_j-u_j^P <= s_j=sum_i z_ij <= b_j-ell_j^P=U_j.    (5)
```

We now use the output bypass degree bound to encode (5).

### Two bypass inlets with unequal input qualities

Write their input qualities as `C_1!=C_2`, their transformed flows as
`w_1,w_2`, and `gamma_h=C_h-q`. Equations (3)--(4) imply

```
w_1+w_2=R_j(q),
w_1 = gamma_1*[R_j(q)-gamma_2*s_j]/(C_1-C_2).         (6)
```

The second identity follows either by solving the two equations for
the original bypass flows, or by substituting
`w_2=R_j-w_1` in `s_j=w_1/gamma_1+w_2/gamma_2`.

The coefficient of `s_j` in (6) is
`-gamma_1*gamma_2/(C_1-C_2)`, which is nonzero and has fixed sign on the
current quality interval. Consequently (5) is exactly equivalent to
putting `w_1` between the two endpoints

```
P_L(q)=gamma_1*[R_j(q)-gamma_2*L_j]/(C_1-C_2),
P_U(q)=gamma_1*[R_j(q)-gamma_2*U_j]/(C_1-C_2).         (7)
```

They are rational polynomials of degree at most two. Their lower/upper
order is fixed on the interval. Add these two bounds to either chosen
one of the output's incident arcs. Equation (4) remains; no condition
on the second arc is discarded.

### Two bypass inlets with equal input qualities

If both qualities equal `C`, put `gamma=C-q`. The quality equation
instead fixes `gamma*s_j=R_j(q)`. Thus (5) is equivalent to the pure
parameter condition that `R_j(q)` lies between `gamma*L_j` and
`gamma*U_j`, ordered by the fixed sign of `gamma`. These are affine
inequalities in `q`. Keep (4) and the original transformed arc bounds.
There is no division by `C_1-C_2` in this case.

### One or zero bypass inlets

With one inlet from input `i`, (5) gives an additional arc interval
whose endpoints are `gamma_i*L_j` and `gamma_i*U_j`. Together with
(4) this is exact.

With no bypass inlet, check `L_j<=0<=U_j`. Equation (4) becomes the
pure parameter equality `R_j(q)=0`. Equivalently this is the zero
divergence equation at an isolated output node. These cases include
zero output demand and absent outlet arcs.

## 5. One incidence system on each quality interval

For each transformed arc there are constantly many lower and upper
capacity candidates, all rational polynomials of degree at most two:
the original arc interval and at most one extra interval from its
receiving output. Its effective lower bound `ell_e(q)` is the maximum
of its lower candidates, and its effective upper bound `u_e(q)` is the
minimum of its upper candidates. Keep these short candidate lists.
No additional capacity-branch parameter partition is needed.

Record every pure parameter condition from Section 4. Consistency of
an arc interval means that every lower candidate is at most every upper
candidate. These are constantly many quadratic inequalities per arc.
The complete remaining system is

```
ell_e(q) <= w_e <= u_e(q),
alpha_v(q) <= div_w(v) <= beta_v(q),                 (8)
```

on the original bypass graph. Here `div_w` is outgoing minus incoming
flow. The node bounds are affine in `q`; arc bounds are specified by
the short quadratic candidate lists. For outputs the node interval is the singleton
`{-R_j(q)}`. Input bounds are those from Section 3.

The transformation, including all sign and zero cases, is an exact
fixed-parameter equivalence. It does not rely on any objective selecting
a preferred feasible flow.

## 6. Interval-node flow feasibility needs only connected cuts

For a directed graph, signed arc bounds `ell<=u`, and node-divergence
intervals `alpha<=beta`, system (8) is feasible exactly when every
vertex subset `S` satisfies

```
sum_(v in S) alpha_v <= u(delta^+(S))-ell(delta^-(S)),
sum_(v in S) beta_v  >= ell(delta^+(S))-u(delta^-(S)).  (9)
```

This is the established circulation criterion with interval node
imbalances. A primary reference is Schrijver, *Combinatorial
Optimization*, [Part I, Corollary 11.2i, printed page 175](https://www.lamsade.dauphine.fr/~cornaz/Enseignement/M2_MODO/DATA/A1.PDF).
That source allows arbitrary real, including negative, bounds. The
sign convention there uses incoming minus outgoing imbalance; (9)
uses outgoing minus incoming.

For completeness, add a new root and an arc from the root to every
vertex `v`, with bounds `[alpha_v,beta_v]`. Flow conservation at `v`
sets this root-arc flow equal to its original divergence. The root's
conservation follows because original divergences sum to zero.
Hoffman's circulation cuts excluding the root give the second inequality
in (9). Taking complements of cuts containing the root gives the first.
Thus (9) is both necessary and sufficient.

It is enough to test connected induced vertex subsets of the original
underlying graph. For an arbitrary `S`, let `S_1,...,S_t` be the
connected components of its induced subgraph. There are no edges
between different `S_h`. Both node sums and all entering/leaving cut
terms in (9) therefore add over these components. Their separate
inequalities imply the inequality for `S`.

On a path, connected subsets are contiguous vertex intervals. On a
cycle they are cyclic intervals and the whole vertex set. There are
`O(n^2)` such sets per component. An isolated vertex is its own one
connected set. Across all bypass components, at most `O(N^2)` connected
cut sets are required. The whole component inequalities are retained;
they enforce the possibility that its total node divergence is zero.

## 7. Polynomial parameter decision and quadratic witnesses

Each connected path or cycle set has at most two edges in its cut.
For its first inequality in (9),

```
u(delta^+S)-ell(delta^-S)
```

is the minimum over all choices of one upper candidate on each outgoing
cut arc and one lower candidate on each incoming cut arc. Hence the
inequality is equivalent to requiring it for every such candidate
combination. There are constantly many combinations because at most
two cut arcs occur and every candidate list has constant length.

Likewise, the right side of the second inequality in (9) is the maximum
over its lower-outgoing/upper-incoming candidate combinations, so that
inequality is equivalent to requiring it for all those combinations.
No active-capacity choice or disjunction remains. Whole-component and
isolated-node cuts have no crossing edge and need just their node sums.

Consequently each open interval between input qualities has an explicit
conjunction of polynomially many univariate inequalities of degree at
most two: all these candidate-cut inequalities, all pure parameter
conditions, and every lower-versus-upper candidate comparison. There
are `O(N)` initial quality intervals and `O(N^2)` connected cuts in each.
All rational coefficients have polynomial bit length: only
constant-degree products, division by fixed nonzero rational quality
differences, and polynomially many sums are used.

Exact quadratic-root isolation, comparison, and sign testing therefore
decide the common feasible parameter set in polynomial rational bit
time. Include every cell boundary, including isolated feasible roots.
At original singular input qualities use the rational LPs from Section
2. Nothing requires examining exponentially many flow bases or
subsets of vertices.

If feasible away from singularities, choose a rational sample in a
feasible open interval, or a feasible algebraic boundary point. Every
boundary is a root of a rational polynomial of degree at most two, so
the selected parameter has degree at most two and polynomial encoding
length. At a singular input quality it is rational.

At this one parameter, solve the signed incidence feasibility problem
and recover `z_ij=w_ij/(C_i-q)`, then all eliminated pool arcs. A
polynomial-time circulation algorithm over the represented ordered
field, or an exact LP method, gives the required transformed flow.
The incidence matrix is rational and totally unimodular; its feasible
vertex coordinates are rational linear combinations of bounds in the
single field `Q(q)`. Their representation lengths are polynomial.
Dividing by nonzero `C_i-q` stays in that same field and retains
polynomial encoding length. At singular values solve the original
rational LP instead. This proves the stated quadratic-field witness
bound and constructive recovery.

The common pool throughput bounds remain the explicit redundant ones
of Section 1. The capacity counterexample in the earlier investigation
still applies to any attempt to omit a restrictive common throughput
bound.

## 8. A reusable fixed-boundary cut description

The cut lemma also applies when some arcs at the endpoints of residual
paths have prescribed transformed flows. Remove each such boundary arc
from the internal graph and subtract its signed prescribed contribution
from both divergence bounds of the adjacent node. Thus a boundary flow
`t` with outgoing-minus-incoming sign `sigma` changes that node's
interval to `[alpha_v-sigma*t,beta_v-sigma*t]`. Keep every original or
newly derived capacity bound on this boundary arc as a separate retained
coordinate constraint. For a fixed number of boundary coordinates, (9)
gives polynomially many rows that are linear in those coordinates and
quadratic in `q`. Use every constant-size internal capacity-candidate
combination as in Section 7. No parameter partition involving the
boundary coordinates is needed.

This is the ingredient needed for bounded exceptions to the exact
source or product contracts. Additional boundary coordinates can
reconnect to physical flow variables by
`w_ij=(C_i-q)z_ij`, a bilinear equation. A complete pooling extension
must still account for its remaining global mass and quality balances;
the cut description alone does not supply those identities. That
extension is completed in the [contract-exception algorithm](pooling-contract-exceptions-algorithm.md).

## 9. Attribution and limitations

The signed circulation criterion, its algorithm, and connected-cut
additivity are established network-flow tools. The result combines those tools with (3)--(7) for this physical
pooling class. The generic one-parameter path theorem remains useful for
broader parameterized 2VPI relations; the present physical structure
permits a stronger bound.

This theorem is about exact contracted feasibility. Standard source
costs and product revenues are constant when every total throughput is
fixed. It does not establish unrestricted dense-cost optimization or general
pooling feasibility. Nonredundant common capacities are handled by the
[later support-function extension](pooling-contracted-common-capacity-algorithm.md),
with a polynomial-degree rather than quadratic-field witness bound. The
focused source assessment above records the priority limits.

## 10. Verification

The new checker
[check_quality_scaled_cuts.py](../code/pooling_bypass_paths/check_quality_scaled_cuts.py)
passed 247 transformed-cut comparisons against the original physical
fixed-quality LP, with 86 feasible fibers. The transformed bounds,
connected cuts, and all-candidate min/max expansions are evaluated in
exact rational arithmetic. The original LP includes all actual feed
and outlet arcs and both pool balances; its feasibility checks use
numerical HiGHS. Another 84 singular-quality cases use the explicit
original rational-LP branch rather than dividing by zero.

The checker also tested 84 independent small signed path/cycle systems,
including negative lower and upper bounds and interval node imbalances.
Connected-cut tests agreed with enumeration of every vertex subset and
with ordinary LP feasibility. This checks the cut sign convention,
whole-component conditions, and connected-set enumeration separately
from the physical scaling. The retained
[test output](../code/pooling_bypass_paths/quality_scaled_cuts_output.txt)
states these distinctions. These finite checks support the mapping and
cut implementation; the mathematical proof establishes the full
parameter-domain algorithm and bit complexity.

## 11. Arbitrary many attributes of affine input rank at most one

The same polynomial result holds for arbitrarily many conserved quality
coordinates when all input-quality vectors have affine rank at most
one. This reduction was independently checked in both reviews of the
earlier contracted synthesis and does not change the flow argument.

For rank one, compute rational vectors `C_0,d`, with `d!=0`, and
rational scalars `t_i` such that `C_i=C_0+d*t_i`. Every positive-demand
product vector must lie in this same affine line; reject an inconsistent
one. Write each remaining product vector as `B_j=C_0+d*tbar_j`.
At zero demand its stated vector is immaterial because all incoming
flows are zero and its quality equations are homogeneous.

Exact local mass conservation cancels the `C_0` terms. Any coordinate
with nonzero entry in `d` then makes the vector quality equation
equivalent to the single scalar equation in `t_i,tbar_j`. The other
coordinates follow automatically. The global vector conservation check
similarly reduces to total mass conservation plus this one scalar
conservation identity. Pool concentration has the form `C_0+d*q`.
Apply the scalar algorithm with `q` in the interval spanned by the
allowed feed scalars. All reductions use polynomial-bit rational linear
algebra, and the quadratic-field witness bound is unchanged.

For rank zero, all input qualities equal a fixed vector. Reject any
different positive-demand product quality. All remaining mixing
constraints are redundant given flow conservation, and a rational LP
decides feasibility. No analogous claim for affine rank two or higher
follows from this argument.
