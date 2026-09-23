# Second independent review: two pools and two outputs

Date: 2026-09-05. Verdict: **PASS** for the proposed NP-hardness reduction,
including upper quality bounds only and the one-pool/single-bypass variant.
No mathematical defect was found. Novelty remains a separate literature
question. Strong NP-hardness and approximation hardness are not established.

Reviewed: [candidate reduction](pooling-two-pools-two-outputs-investigation.md),
as present on 2026-09-05. This review covers the simplified version using
one distinguished upper quality bound. The reviewer also checked the earlier
version using a coordinate and its negative to force equality; the equality
is unnecessary, and its removal is valid.

## 1. Primary hardness source and polynomial preparation

The reviewer independently read Sections 2–3 and Theorem 3.1 of
[Matsui's primary manuscript](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf).
The construction uses bounded base variables `x_i,y_ij` in `[0,1]`.
Its other variables are affine functions of these and can be substituted
out. The two product factors are strictly positive throughout the feasible
polytope. The decision threshold is positive. The paper explicitly bounds
the bit lengths of the large coefficients and threshold polynomially in
the source size. Thus its theorem supplies exactly the bounded positive
product problem used by the proposed reduction, without assuming all
auxiliary variables themselves lie in the unit cube.

For nonempty bounded `P0`, strict positivity and compactness imply the
rational LP optimum `u_min` is positive. Exact rational LP returns it with
polynomial bit length. Consequently multiplying `U` by `2/u_min` and `V`
by `u_min/2` preserves the product and has polynomial encoding cost even
if `u_min` is very small. The normalized `U` satisfies `U>=2`.

Adding `V<=K` is safe in both directions: it only removes points, and
every old yes witness obeys `V<=K/U<=K/2`. This step establishes the
nonnegative mixture reward `b=K-V` required later. If either LP feasibility
test fails, a zero-cost instance with positive target is a valid fixed no
instance with the required topology.

The simplex embedding is an affine bijection between the old feasible
polytope and its image. For `s` bounded base variables,
`z_i=w_i/s` and `z_0=1-sum_i z_i`; the old cube ensures `z_0>=0`.
Conversely, `z_i<=1/s` and simplex nonnegativity recover the cube bounds
on `w_i=s z_i`. Affine constants become coefficients multiplying
`sum_i z_i=1`. The number of variables and rows, and all coefficient bit
lengths, remain polynomial. The proof correctly does not assume that
unrestricted simplex vertices satisfy the encoded inequalities.

## 2. Every active mixture satisfies every polytope row

Let `T>0` be the mixing-pool throughput. Its input proportions are a
simplex point, regardless of the signs of any input quality coefficients.
For row `A_r z<=d_r`, assigning anchor quality exactly `d_r` cancels the
anchor's contribution from the first output inequality. The resulting
condition is `(A_r z-d_r)y_1<=0`. The second output gives
`(A_r z-d_r)y_2<=0`.

Because `y_1+y_2=T>0`, at least one condition forces the row. This works
when either output is inactive and when `d_r` or some `A_ri` is negative.
All rows must be imposed at both outputs, and the anchor must lie exactly
on each row bound. These properties are present in the construction and
are essential to this part of the proof.

It follows that every positive-throughput solution has `z in P`, hence
`a(z)>=1` and `b(z)>=0`. Individual `a_i` or `b_i` may still be negative;
the argument never uses their individual signs. In particular, positive
and negative inlet costs cannot create an extra profitable regime outside
the encoded polytope.

## 3. Exact maximum-profit formula with one upper bound

The distinguished output-1 inequality is `a(z)y_1<=y_1+h=D_1`.
Since `a(z)>=1`, division is valid and gives `y_1<=D_1/a(z)`.
With `D_1<=1` and `D_2=y_2<=1`, the exact inlet-cost identity gives

```
profit = b(z)(y_1+y_2)
       <= b(z)(D_1/a(z)+D_2)
       <= b(z)(1+1/a(z)).
```

The nonnegative mixture reward is used in both inequalities. No positive
flow lower bound, forced output filling, or quality equality is assumed.

For any `z in P`, the proposed reverse construction has
`y_1=1/a`, `y_2=1`, `h=1-1/a`, and `x_i=(1+1/a)z_i`.
These quantities are nonnegative because `a>=1`. The anchor and all
outgoing arcs use at most one unit, the two outputs each receive one,
the mixing pool uses at most two, and every variable intake uses at most
two. Every row coordinate is feasible because `z in P`; the distinguished
output-1 inequality holds at equality. The output-2 distinguished bound
is redundant by the convex-mixture property. Thus every claimed value is
attainable within all stated capacities.

At `a=1`, the anchor flow is zero and the construction is still valid.
At `b=0`, its profit is zero. If the mixing pool is inactive, anchor-only
flow may remain feasible in the simplified construction, but it has zero
profit. This is correctly handled by comparison with a nonnegative
right-hand maximum. Compactness of `P` and `a>=1` ensure attainment.

Therefore the exact maximum-profit formula in the draft is correct.

## 4. Decision threshold and model restrictions

For any normalized feasible point, `a=U-1>0`, so

```
b(1+1/a)>=K
<=> (K-V)U >= K(U-1)
<=> UV<=K.
```

The direction of the threshold is correct, including equality. Together
with the exact maximum formula, this gives a many-one polynomial reduction
from Matsui's decision problem. The pooling decision in minimum-cost form
uses target `-K`. The large rational source coefficients prevent a strong
NP-hardness conclusion from this construction alone.

Adding a common rational shift to every input quality and both output
bounds of one coordinate preserves each output constraint by mass
conservation. Pool qualities shift by the same amount when active;
inactive-pool qualities have no effect. A shift computed from the finite
list of coordinate values and bounds makes them all nonnegative with
polynomial bit length. Thus signed intermediate qualities do not violate
the final nonnegative-data variant. The shift does not introduce lower
quality bounds or change the flow capacities.

The anchor pool has one inlet and one outlet. Eliminating it produces
exactly one bypass arc from its original input to output 1 with capacity
one. The anchor input and output capacities supply the same restrictions,
and its quality vector is unchanged. Hence the one-pool, two-output,
single-bypass variant is equivalent. The theorem concerns counts of all
pools, including degree-one pools, as allowed by the standard formulation.

The additional economic and capacity variants also pass. Choosing
`B>=max(0,max_i b_i)`, charging `B-b_i` per unit at variable inputs and
`B` at the anchor, and paying `B` per output unit preserves profit because
total input flow equals total output flow. These production costs and
revenues are all nonnegative. Output capacities alone imply `h<=1`,
`T<=2`, and `x_i<=2`, so the stated source and pool capacity bounds are
redundant. Fixing both output demands at one preserves the optimum because
the reverse construction already fills them and the upper-bound argument
still applies.

The proposed tree-topology strengthening is correct as well. With `m`
variable inputs the undirected graph is connected, has `m+5` vertices and
`m+4` edges: the variable-input leaves attach to `L`, output 2 is another
leaf at `L`, and the remaining path is `L--output 1--H--anchor`. It is
therefore a tree, and every input has out-degree one. This is a statement
about the physical pooling network, not the polynomial constraint-incidence
graph, whose structure need not have bounded treewidth as qualities grow.

## 5. Independent exact checks

The [separate reviewer checker](../code/pooling_two_pools_two_outputs/independent_review.py)
fixes rational compositions and enumerates all vertices of the original
three-flow LP in `(y_1,y_2,h)` using rational arithmetic. It includes
the original output quality inequalities, inlet capacity restrictions,
and all output/arc capacities. It does not impose output saturation or
distinguished-quality equality.

The check passed 78 exact LP instances, including compositions outside
the encoded polytope, negative individual distinguished-quality and reward
coefficients, the boundaries `a=1` and `b=0`, and the same models after
strictly positive quality shifts. All excluded compositions forced zero
mixing-pool throughput. Thirty-six additional rational checks verified
the source/pooling threshold equivalence, including exact equality.

A deliberate negative control omits the polytope-row constraints from
output 1. An excluded composition then earns profit five, whereas its
profit is zero in the correct formulation. Thus the independent check
detects a concrete failure of mixture enforcement.

These finite checks corroborate the capacity and sign arguments. They do
not replace the general proof or certify asymptotic hardness on their own.
