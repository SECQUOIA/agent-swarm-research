# Parametric path cuts and a possible pooling-capacity extension

Date: 2026-09-05. Status: completed. The symbolic path/cycle lemma passed
[an independent audit](review-parametric-path-cut-clamp.md); the complete
common-capacity extension in Sections 3–4 passed
[two](review-parametric-path-cut-pooling-capacity-extension.md)
[independent audits](review-parametric-path-cut-pooling-capacity-second.md).
It is promoted to [the verified result](../results/pooling-contracted-common-capacity-algorithm.md).
Section 2 preserves the earlier proposal; its proof obligations are now
resolved in Sections 3–4. The [source note](parametric-path-cut-box-truncation-source.md)
identifies the classical box-base formula and greedy rule.

## 1. Polynomial symbolic binary path minimization

Let `theta` have fixed dimension. On a path with binary labels
`x_1,...,x_n`, consider the energy

```
sum_i U_i(x_i;theta)
 + sum_(i=2)^n [a_i(theta) 1_(x_(i-1)=0,x_i=1)
                + b_i(theta) 1_(x_(i-1)=1,x_i=0)].
```

Assume `a_i,b_i>=0` on the parameter domain, and all terms are explicit
rational polynomials of fixed degree. The unary costs may have either
sign. This includes a directed minimum cut on a path with arbitrary
source/sink incident arcs after constant unary shifts.

Let `E_i(0),E_i(1)` be optimal prefix energies conditional on the final
label, and put `D_i=E_i(1)-E_i(0)`, `u_i=U_i(1)-U_i(0)`. Direct dynamic
programming gives

```
E_i(0)=E_(i-1)(0)+U_i(0)+min(0,D_(i-1)+b_i),
D_i=u_i+clamp(D_(i-1),-b_i,a_i),
D_1=u_1.
```

The second identity follows by subtracting the two prefix recurrences;
`min(D,a)-min(0,D+b)=clamp(D,-b,a)` for `a,b>=0`.

Set `P_i=sum_(h=1)^i u_h` and `Z_i=D_i-P_i`. Then

```
Z_1=0,
Z_i=clamp(Z_(i-1), -b_i-P_(i-1), a_i-P_(i-1)).       (1)
```

Every `Z_i` is therefore selected from the common list consisting of
zero and the two polynomial clamp endpoints for each preceding stage.
Add the polynomials `-P_i` to that list. The signs of all pairwise
differences fix every clamp choice, every increment of `E_i(0)`, and
the final choice `min(E_n(0),E_n(1))`. On each realizable sign cell the
minimum energy is one explicit polynomial, a sum of polynomially many
input terms. There are polynomially many cells in fixed parameter
dimension because the list has linear size and fixed degree. Equalities
and lower-dimensional cells are retained; arbitrary tie choices give
the same energy. Coefficient lengths remain polynomial.

For a cycle, condition on its first label, absorb its final incident
edge into the last unary term, and solve two paths. Comparing their
polynomial values over the common refinement remains polynomial.

This derivation concerns a binary submodular path energy. It does not
claim that generic bounded-treewidth parametric optimization has a
polynomial symbolic value function. The earlier Klee--Minty examples
involve different continuous constraints and do not refute (1).

The exact checker
[check_path_cut_clamps.py](../code/pooling_bypass_paths/check_path_cut_clamps.py)
passed 360 rational instances through nine path vertices. It compares
the accumulated clamp recurrence against enumeration of every original
binary labeling, including signed unary costs and sampled quadratic
parameter data. This verifies the recurrence independently of any flow
or pooling interpretation; it does not establish the proposed reduction
in the next section.

## 2. Possible use for a shared pooling-capacity bound

For scalar exactly contracted pooling, the reviewed transformation
`w_ij=(C_i-q)z_ij` gives bounded incidence flows and node divergence
intervals on bypass paths and cycles. Total bypass flow is

```
sum_ij z_ij = sum_inputs div(w)_i/(C_i-q).
```

Thus minimizing pool throughput is a linear objective on node
divergences, with coefficients `1/(C_i-q)`. Their relative order is
fixed between successive input qualities. A restrictive pool capacity
could be tested if this objective's exact parameter-dependent minimum
and maximum were available with polynomial encoding.

A route requiring a separate proof is the established base-polyhedron
description of feasible divergences. For unrestricted bounded arc flows,
the cut function is `f(S)=u(delta+S)-ell(delta-S)`. Intersecting its base
polyhedron with node bounds `alpha<=d<=beta` is expected to produce
the rank function

```
f_box(S)=min_T [ f(T)+beta(S\T)-alpha(T\S) ],          (2)
```

when the intersection is nonempty. A sorted-cost greedy formula would
then express each divergence support value through polynomially many
values of (2) on cost prefixes. Each such minimization is a binary
submodular path/cycle energy: rewrite the cut as
`sum_(out cut)(u-ell)+sum_(v in T) div(ell)_v` and collect its unary
terms. Section 1 would supply a polynomial symbolic description.

The original proposal left formula (2), its support-function use, and
physical capacity recovery unproved. Sections 3–4 below now discharge
those obligations, with primary attribution and two independent audits.
Feasibility of local paths alone still does not enforce the shared pool
capacity; the added support inequalities are necessary to repair that
omission.

## 3. Completion: the bounded-divergence rank formula

This section supplies the previously missing argument in Section 2. Let
`ell<=u` be finite signed arc bounds on a directed graph, and let
`alpha<=beta` be finite node-divergence bounds. Write

```
f(S)=u(delta+ S)-ell(delta- S),
D={div(w): ell<=w<=u, alpha<=div(w)<=beta}.
```

Assume `D` is nonempty. The bounded-flow divergence polytope before node
bounds is the base polyhedron `B(f)`: its inequalities are
`d(S)<=f(S)` and `d(V)=0`. Necessity follows by summing divergences;
sufficiency is the usual circulation-cut criterion for prescribed
node divergences. In particular `f` is submodular, `f(empty)=f(V)=0`.

Define

```
g(S)=min_(T subset V) [f(T)+beta(S\T)-alpha(T\S)].     (3)
```

Then `g` is a normalized submodular function with `g(V)=0`, and

```
D=B(g).                                               (4)
```

Here is a direct proof including the normalization that the earlier
outline left implicit. The function of `(S,T)` minimized in (3) is
submodular on the product of two Boolean lattices. Its `f(T)` term is
submodular. Each node's remaining two-label term takes values
`0,beta_v,-alpha_v,0` at `(0,0),(1,0),(0,1),(1,1)` respectively,
so its submodularity inequality is exactly `alpha_v<=beta_v`.
Partial minimization over `T` preserves submodularity: apply product
submodularity to minimizing pairs and use their union and intersection
as candidates. For any `d in D`,

```
d(S)=d(T)+d(S\T)-d(T\S)
     <=f(T)+beta(S\T)-alpha(T\S).
```

Thus `d(S)<=g(S)` for every `S`. At `S=empty,V`, this inequality
and the choices `T=empty,V` show `g(empty)=g(V)=0`.
It follows that `D` is contained in `B(g)`. Conversely, `g(S)<=f(S)`
by taking `T=S`, so `B(g)` is contained in `B(f)`. The choices
`T=empty` at `S={v}` and `T=V` at `S=V\{v}` give
`d_v<=beta_v` and `d_v>=alpha_v`. This proves (4).

For any cost vector `c`, order vertices so
`c_1>=...>=c_N`, and let `S_k={1,...,k}`. The classical greedy base
vector is

```
d_k=g(S_k)-g(S_(k-1)).
```

Submodularity proves `d in B(g)` by the diminishing-increments
inequality, and telescoping gives

```
max_(d in D) c.d
 =sum_(k=1)^(N-1) (c_k-c_(k+1))*g(S_k),               (5)
```

since `g(V)=0`. The same formula applied to `-c` gives the minimum.
Ties may be ordered arbitrarily. The argument is an application of
established base-polyhedron intersection and greedy optimization tools;
no new general submodular theorem is claimed.

## 4. Exact common pool-capacity extension

Consider the physical model and signed-flow transformation in the
[reviewed contracted pooling result](../results/pooling-quality-scaled-path-flow.md).
There is one pool, arbitrary many rational scalar input qualities,
exact source supplies and exact product demands and qualities, and a
bypass graph of maximum degree two. All individual arc bounds remain,
including positive feed and outlet lower bounds. Replace the redundant
common pool bounds by **any finite rational interval** `[L_P,U_P]`
with `0<=L_P<=U_P`. Missing common bounds can be bounded by the physical
arc capacities. The following derivation establishes polynomial-bit
exact feasibility with this interval. Standard node economics remains
constant under the exact external throughput contracts.

If the pool has no usable feed or outlet, force all its arcs to zero,
check their bounds, reject if `L_P>0`, and solve the remaining original
rational LP. Thus the inactive-pool preprocessing preserves the common
lower bound explicitly.

Singular qualities and search endpoints still use the original rational
fixed-quality LP, now with the common pool interval. On each remaining
open quality interval, first partition at the roots of all arc-bound
candidate comparisons. Their degrees are at most two, so this uses
polynomially many cells and makes the effective signed bounds `ell,u`
explicit quadratic polynomials. Node bounds `alpha,beta` are affine.
Retain every pure parameter condition and every connected circulation
cut from the reviewed result. These conditions certify `D(q)!=empty`;
formula (3) is used only on this feasible parameter set.

Let `A=sum_i a_i` be the fixed total source supply and set

```
c_i(q)=1/(C_i-q)   at input vertices,
c_j(q)=0          at output vertices.
```

For every transformed feasible flow,

```
Z=sum_(ij) z_ij=sum_i div(w)_i/(C_i-q)=c(q).div(w),
T_pool=A-Z.                                           (6)
```

The order of these costs is fixed on each open quality interval:
all denominators have fixed nonzero signs, and pairwise differences
between input costs have constant numerator `C_j-C_i` and denominator
`(C_i-q)(C_j-q)`. Costs equal to zero at outputs are ordered by the
same signs. Coincident input qualities simply give tied costs.

For each of the at most `N-1` greedy prefix sets in (5), evaluate (3)
symbolically. Expanding the cut gives

```
f(T)=sum_(e out of T) (u_e-ell_e)+sum_(v in T) div(ell)_v.
```

The first term is a directed path/cycle cut with nonnegative capacities
`u_e-ell_e`; the remaining terms in (3) are unary label costs. All are
quadratic polynomials on the current cell. Section 1 therefore gives
its exact minimum as a quadratic polynomial on polynomially many
univariate sign cells. Apply this to the prefix orders for both `c`
and `-c`, and take the common refinement of all their univariate
breakpoints. This is a union of polynomially many root sets, so it
remains polynomial, not a product enumeration. Disconnected components
can be minimized separately and their values added. Isolated vertices
are included. All ties and zero-dimensional cells are retained.

On each resulting cell, (5) explicitly gives `Z_max(q)` and `Z_min(q)`
as rational functions with polynomial coefficient length and polynomial
degree. A common denominator is the product of the nonzero factors
`C_i-q`; repeated factors need not be retained. Multiplying and summing
polynomially many quadratic numerators increases degree only linearly
in the number of inputs and bit length polynomially. The denominator's
sign is known on the cell.

The possible values of `Z` form exactly the closed interval
`[Z_min(q),Z_max(q)]`, because the feasible signed-flow polytope is
nonempty and compact and its linear image in one dimension is an
interval. Consequently the original common pool bound is feasible
exactly when

```
Z_min(q)<=A-L_P,    Z_max(q)>=A-U_P.                  (7)
```

After multiplying by the known-sign denominators, these are univariate
polynomial inequalities of polynomial degree and coefficient length.
Together with the retained local conditions and cell signs, they can
be solved by exact real-root isolation and sign testing in polynomial
rational bit time. Open interval endpoints and isolated feasible roots
are handled explicitly; no approximate margin is assumed.

This proves the decision bound. For a constructive witness, select a
feasible rational interval sample or a represented real-algebraic
boundary point `q`. Its degree and encoding length are polynomial,
although the earlier degree-at-most-two guarantee is no longer asserted.
At this `q`, the greedy formula constructs divergence vectors attaining
`Z_min` and `Z_max`. Every coordinate is a difference of two quadratic
polynomial values from (3), hence lies in `Q(q)` with polynomial
encoding length. Realize each divergence by a bounded-flow feasibility
algorithm: shift by `ell`, add the usual source/sink imbalance arcs,
and use Edmonds--Karp augmentations with exact ordered-field arithmetic.
The algorithm has polynomially many augmentations independent of capacity
magnitudes. All capacities and computed flow coordinates are sums and
differences of polynomially represented elements of `Q(q)`, so their
bit lengths remain polynomial.

Choose any value in the nonempty intersection of
`[Z_min,Z_max]` and `[A-U_P,A-L_P]`. For example take the larger of
`Z_min` and `A-U_P`. If the extrema differ, take the corresponding
convex combination of the two realizing flows; if they agree, use either.
The combination coefficient is one quotient in `Q(q)` and has polynomial
encoding length. Convexity preserves all signed-flow bounds and node
rows while enforcing the common pool interval. Divide by the nonzero
`C_i-q`, recover all local feeds and outlets, and use the already proved
global conservation identities to recover an original physical witness.
Singular-quality witnesses instead come from the original rational LPs.

This completes the specific common-capacity route proposed in Section 2.
It does not claim arbitrary contract intervals, dense arc-profit
optimization, or unrestricted degree-two pooling tractability. Those
would require further arguments and are outside this closure.
