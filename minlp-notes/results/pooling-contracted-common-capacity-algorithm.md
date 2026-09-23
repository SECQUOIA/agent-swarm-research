# Contracted degree-two pooling with common throughput bounds

Date: 2026-09-05. Status: verified theorem. Two independent complete
extension audits passed: [first](../notes/review-parametric-path-cut-pooling-capacity-extension.md)
and [second](../notes/review-parametric-path-cut-pooling-capacity-second.md).
The symbolic path lemma also has its [own audit](../notes/review-parametric-path-cut-clamp.md).
The [source assessment](../notes/parametric-path-cut-box-truncation-source.md)
identifies the established box-base and greedy formulas; the
[pooling comparison](../notes/pooling-quality-scaled-contracts-novelty.md)
records the bounded novelty assessment. No general new submodular
optimization theorem or exhaustive priority claim is made.

**Theorem.** One-pool pooling with one scalar conserved quality, exact
source supplies, exact product demands and qualities, and bypass maximum
degree two admits polynomial-bit exact feasibility and physical witness
recovery with arbitrary common pool throughput lower and upper bounds.
The number of inputs, outputs, and distinct rational input qualities is
unrestricted. All individual finite rational arc bounds, including positive
lower bounds, remain. A witness lies in one real algebraic field of
polynomial degree and encoding length. The result also applies to the
previously established affine-rank-one quality compression.

This removes the redundant common-capacity hypothesis of the
[earlier contracted theorem](pooling-quality-scaled-path-flow.md).
The earlier quadratic-field bound is not claimed for this stronger class.
Standard source costs and product revenues are constant under the exact
throughput contracts; arbitrary arc-cost optimization is not included.

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
or pooling interpretation. The physical reduction is proved separately below.

## 2. The bounded-divergence rank formula

Let
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
g(S)=min_(T subset V) [f(T)+beta(S\T)-alpha(T\S)].     (2)
```

Then `g` is a normalized submodular function with `g(V)=0`, and

```
D=B(g).                                               (3)
```

Here is a direct proof including the normalization that the base-polyhedron identity requires. The function of `(S,T)` minimized in (2) is
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
`d_v<=beta_v` and `d_v>=alpha_v`. This proves (3).

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
 =sum_(k=1)^(N-1) (c_k-c_(k+1))*g(S_k),               (4)
```

since `g(V)=0`. The same formula applied to `-c` gives the minimum.
Ties may be ordered arbitrarily. The argument is an application of
established base-polyhedron intersection and greedy optimization tools;
no new general submodular theorem is claimed.

## 3. Exact common pool-capacity algorithm

Consider the physical model and signed-flow transformation in the
[reviewed contracted pooling result](pooling-quality-scaled-path-flow.md).
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
formula (2) is used only on this feasible parameter set.

Let `A=sum_i a_i` be the fixed total source supply and set

```
c_i(q)=1/(C_i-q)   at input vertices,
c_j(q)=0          at output vertices.
```

For every transformed feasible flow,

```
Z=sum_(ij) z_ij=sum_i div(w)_i/(C_i-q)=c(q).div(w),
T_pool=A-Z.                                           (5)
```

The order of these costs is fixed on each open quality interval:
all denominators have fixed nonzero signs, and pairwise differences
between input costs have constant numerator `C_j-C_i` and denominator
`(C_i-q)(C_j-q)`. Costs equal to zero at outputs are ordered by the
same signs. Coincident input qualities simply give tied costs.

For each of the at most `N-1` greedy prefix sets in (4), evaluate (2)
symbolically. Expanding the cut gives

```
f(T)=sum_(e out of T) (u_e-ell_e)+sum_(v in T) div(ell)_v.
```

The first term is a directed path/cycle cut with nonnegative capacities
`u_e-ell_e`; the remaining terms in (2) are unary label costs. All are
quadratic polynomials on the current cell. Section 1 therefore gives
its exact minimum as a quadratic polynomial on polynomially many
univariate sign cells. Apply this to the prefix orders for both `c`
and `-c`, and take the common refinement of all their univariate
breakpoints. This is a union of polynomially many root sets, so it
remains polynomial, not a product enumeration. Disconnected components
can be minimized separately and their values added. Isolated vertices
are included. All ties and zero-dimensional cells are retained.

On each resulting cell, (4) explicitly gives `Z_max(q)` and `Z_min(q)`
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
Z_min(q)<=A-L_P,    Z_max(q)>=A-U_P.                  (6)
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
polynomial values from (2), hence lies in `Q(q)` with polynomial
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

This completes the common-capacity algorithm.
It does not claim arbitrary contract intervals, dense arc-profit
optimization, or unrestricted degree-two pooling tractability. Those
would require further arguments and are outside this closure.


## 4. Verification and scope

The symbolic recurrence checker passed 360 exact rational path instances.
The first independent extension checker,
[check_box_divergence_support_review.py](../code/pooling_bypass_paths/check_box_divergence_support_review.py),
passed 128 bounded-flow systems, 3,076 subset rank values, 256 support
extrema, and 512 capacity-intersection interpolations. The second,
[check_box_rank_support_second.py](../code/pooling_bypass_paths/check_box_rank_support_second.py),
passed 36 networks with 146 vertices, 672 subset-support comparisons,
288 signed objectives, and 864 interpolated witnesses. These exact tests
check the new support and interpolation identities; the original
physical transformation has its separate two audits and physical-LP
comparisons in the earlier contracted theorem.

For multiple conserved attributes of affine input rank at most one,
apply the rational affine-line compression already proved in Section 11
of that theorem. It changes no physical flow or common throughput bound,
so the present scalar algorithm applies without modifying the capacity
argument. This does not remove arbitrary quality rank from this result.

The box-truncation formula and greedy optimization rule are classical.
Shioura, Shakhlevich, and Strusevich (2013), Theorems 1–2 and equation
(11), state the needed formulas in their
[primary paper](https://eprints.whiterose.ac.uk/id/eprint/78189/10/shakhlevich1.pdf).
The contribution under consideration is the exact pooling specialization,
its polynomial symbolic support construction, and recovery with a
restrictive common throughput interval. The source review found no
matching restricted pooling theorem in the checked papers.
