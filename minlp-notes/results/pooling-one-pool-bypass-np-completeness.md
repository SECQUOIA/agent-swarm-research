# Pooling with one pool and a fixed quality dimension is NP-complete with bypasses

Date: 2026-09-05. Status: two independent mathematical reviews PASS; novelty qualified.

The reduction and the NP upper bound prove NP-completeness with one pool,
one physical quality allowing lower and upper bounds, and arbitrary direct arcs. The
pool has only two outgoing arcs. All other outputs receive bypass flow
only. Fixed source supplies and fixed output demands are used essentially
in the current gadgets. Equivalently two quality coordinates with only
upper bounds suffice. No claim covers upper-flow-bound-only instances.

## A four-port copy and quality-conversion gadget

Fix distinct rational quality values `alpha,beta` and put
`gamma=(alpha+beta)/2`. Make two output nodes `A,B`, each with exact demand
4 and exact quality `gamma`. Each output has three incoming arcs: an
`alpha`-quality port, a `beta`-quality port, and an arc from one common
`gamma`-quality input. The common input has exact total supply 4. The
endpoint ports have capacity 2 and the two middle arcs have capacity 4.

The mass and quality equalities at `A` force its two endpoint port flows
to coincide: writing them `u,v` and its middle flow `m_A`, subtract
`gamma` times mass balance from quality balance to obtain
`(alpha-gamma)u+(beta-gamma)v=0`, hence `u=v=x`. Then
`m_A=4-2x`. At `B`, its endpoint flows similarly coincide at `x'` and
`m_B=4-2x'`. Exact common supply gives `m_A+m_B=4`, hence `x+x'=2`.

Thus the four endpoint ports carry

```
A-alpha: x,       A-beta: x,
B-alpha: 2-x,     B-beta: 2-x,          0<=x<=2.            (G)
```

Conversely every `x in [0,2]` gives these feasible port and middle flows.
Ports mean input-to-output arcs whose source node is assigned when gadgets
are joined. A source may serve several ports only when their quality
labels coincide.

Join a `B-alpha` port of one gadget to an `A-alpha` port of the next by
making them the two outgoing arcs of a new `alpha`-quality input with
exact supply 2. Their sum is 2, so the next gadget's parameter is the
same `x`. A chain of `(alpha,beta)=(0,2)` gadgets therefore provides any
polynomial number of separate ports carrying `x` and `2-x`, all of quality
2. The unused initial and final quality-0 ports, and any unused quality-2
ports, are supplied by private inputs with upper capacity 2 and no lower
bound. They impose no further restriction on `x`.

A final gadget with `(alpha,beta)=(0,a_i)`, for any `a_i!=0`, converts the
same chain signal into ports of quality `a_i`. Assign its `B-beta` port
to an input `i` of quality `a_i` and exact supply 2, and give input `i`
one additional arc into the sole pool. The bypass port carries `2-x_i`,
so the pool intake from `i` is exactly `x_i`. Its `A-beta` port can be
supplied privately as above. Thus a free signal is copied to an actual
mixing-pool intake with any nonzero prescribed quality.

## Encoding homogeneous bounded-coefficient linear constraints

Consider a system `C x<=0` with integer coefficients, on variables
`0<=x_i<=2`. For a row `c`, create one input of quality 2. For each
positive coefficient `c_i`, assign `c_i` distinct signal ports carrying
`x_i` as outgoing arcs of this input. For each negative coefficient,
assign `-c_i` ports carrying `2-x_i`. Give this input upper capacity

```
2 * sum_{i:c_i<0} (-c_i).
```

Its total outflow is
`sum_i c_i x_i + 2 sum_{c_i<0}(-c_i)`, so this capacity is exactly the
desired inequality. Every port is used once. An equality may be encoded
as two inequalities. Repeated ports are supplied by extending the signal
chains. The number of gadgets is linear in the sum of absolute row
coefficients, plus the number of variables. Thus the construction is
polynomial when those integer coefficients are polynomially bounded.

All source nodes just described are ordinary inputs; all gadget nodes are
ordinary outputs. There are no additional pools or pool-to-pool arcs.
The constraint graph may be complicated, but every physical arc points
from an input directly to an output, except for the designated pool arcs.

All source identities are distinct unless a merge is explicitly specified.
Each midpoint source serves exactly the two outputs of its own gadget.
Each chain-link source serves exactly the two joined quality-0 ports.
Each conversion source serves exactly its `B-beta` port and its own pool
intake arc. Each row source serves only the ports allocated to its row.
Every remaining private source serves just one unused port. Equal quality
values do not identify source nodes. These conventions exclude unintended
routes or unintended sharing of supply constraints.

## Source family with suitable bounded constraint coefficients

Use Matsui's explicit positive-product family from
[METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf),
Sections 2–3 and Theorem 3.1. Its base polytope `Omega(M)` has variables
`w=(r_i,s_ij) in [0,1]^(n+n^2)`, the McCormick constraints

```
s_ij<=r_i, s_ij<=r_j, s_ij>=r_i+r_j-1  (i!=j),
s_ii=r_i, M r=1,
```

where `M` is a zero-one matrix and `n>=5`. Set `s=n+n^2`, use simplex
coordinates `z_1,...,z_s,z_0` with `w_h=s z_h`, and impose
`sum z_i=1`. Transforming each base inequality and homogenizing at
`T=sum_i x_i` gives exactly a system `C x<=0` with polynomially bounded
integer coefficients. For example a cube bound becomes `s x_h<=T`, a
McCormick lower bound becomes `s x_ij>=s x_i+s x_j-T`, and each source
equation becomes `s sum_i M_ri x_i=T`. The coefficients have magnitude
at most `s+1`; the row count and total coefficient sum are polynomial.
For `T>0`, these rows hold if and only if `z=x/T` lies in the embedded
`Omega(M)`.

No LP normalization or large-coefficient safe cut is needed for this
source family. To see this explicitly, write Matsui's factors as

```
p=n^(n^4),
X=sum_i p^i r_i,
Y=sum_ij p^(i+j) s_ij,
U=2p^(4n)-p+Y+2p^(2n)X,
V=2p^(4n)-p+Y-2p^(2n)X,
K=4p^(8n).
```

The source decision is `min_{Omega(M)} U V<=K`, which is NP-hard.
At every unrestricted simplex generator (corresponding to `w=0` or
`w=s e_h`),

```
U >= 2p^(4n)-p > 2,
V <= 2p^(4n)-p+s p^(2n) < K.
```

The second bound uses `s<p^(2n)` and `p>=2`; these follow immediately
from `n>=5` and `p=n^(n^4)`. Therefore the coefficient vectors of the
linear functions `a=U-1` and `b=K-V` on the simplex satisfy
`a_i>1,b_i>0` individually. Their binary encoding lengths are polynomial,
although their magnitudes are large. Positive `V` on the source polytope
is established in Matsui's proof.

## Completing the pooling reduction

Make a signal chain for each simplex coordinate and use the conversion
gadget to enforce pool intake `x_i` from an input of quality `a_i`.
Encode all the homogeneous rows `C x<=0` through quality-2 capacity
inputs as above. Pool `L` has upper capacity 2 and feeds just two
additional outputs, each with upper capacity 1. One private anchor input
of quality zero can bypass directly into output 1, with upper capacity 1.
Output 1 has upper quality bound 1 and no lower quality restriction;
output 2 has a redundant upper bound at least `max_i a_i`. The only
arcs entering these two outputs are the stated pool arcs and anchor arc.

Give the pool intake arc from input `i` cost `-b_i`; every gadget arc and
other arc has cost zero. Thus profit is `sum_i b_i x_i`.

When `T=sum x_i>0`, the copy network enforces `z=x/T` in the source
polytope, and pool quality is `a(z)`. Exactly as in the reviewed
two-pool/two-output reduction, output 1 implies `y_1<=D_1/a(z)`, so

```
profit=b(z)T <= b(z)(1+1/a(z)).
```

Conversely choose any source point `z` and set `T=1+1/a(z)`,
`x_i=Tz_i`, `y_1=1/a(z)`, `y_2=1`, and anchor flow `1-1/a(z)`.
All `x_i` are at most 2. The homogeneous source rows hold, so every
constraint-source capacity holds. Fill each copy gadget with its
displayed signal assignment; all its fixed demands and supplies hold.
This constructs a feasible full pooling solution with the stated profit.
If `T=0`, all signal variables are zero, every homogeneous row holds,
and all gadget flows still have their feasible complementary values;
profit is zero. Thus the exact maximum is

```
max( {0} union { (K-V(z))U(z)/(U(z)-1) : z in P } ),
```

and comparison with `K` is equivalent to `UV<=K`. An empty source
polytope permits only zero pool throughput and has profit zero, so no
separate LP feasibility preprocessing is needed.

The same objective can use production costs attached to inputs, rather
than distinct costs on a shared input's outgoing arcs. Move the cost
`-b_i` to the private input serving the conversion gadget's `A-beta` port;
its only outflow is `x_i`. Set the original pool-intake cost to zero.
This leaves profit unchanged. Finally add a common charge
`B>=max_i b_i` to all input costs and pay revenue `B` on every output's
total inflow. Total mass conservation cancels these added terms, so both
production costs and revenues can be nonnegative.

## Exact model scope and NP-completeness

The gadget uses one physical quality, with exact bounds at gadget
outputs. Duplicating its negative as a second coordinate converts all
quality bounds to upper bounds. Coordinate shifts and positive scaling
can put all quality data into `[0,1]` without changing the proof.
This base construction uses source/input and output lower flow bounds.
The [reviewed stronger construction](pooling-one-pool-upper-bounds-np-completeness.md)
removes all positive lower flow bounds and all lower quality bounds,
and bounds input out-degree by two and output in-degree by three.
The result shows that unrestricted bypass
coupling defeats fixed-pool/fixed-quality tractability in this capacitated
model; it does not contradict the constructive theorem with a bounded
bypass vertex cover or bounded bypass component size.

Two independent reviewers checked gadget composition, signal signs,
port uniqueness, source coefficient bounds, and the original pooling model.
Both reviews passed: [first](../notes/review-pooling-one-pool-bypass-copy.md),
[second](../notes/review-pooling-one-pool-bypass-copy-second.md). The [full-network checker](../code/pooling_bypass_copy/check_copy_reduction.py)
has passed 27 original-model global solves, comparing twelve small linear
cones and shifted copies against exact rational vertex reference values,
plus empty-polytope, zero-reward, and `a=1` boundary cases.
The tested model contains only the constructed arcs, node flow bounds,
one pool's blending equality, and original output quality inequalities.
No copied equality or cone row is added directly. Removing the lower
supply bound at midpoint inputs changes a deliberately chosen reference
profit from 10 to 20, detecting a concrete failure of signal copying.
The [log](../code/pooling_bypass_copy/check_output.txt) is retained. These
computations support the independently reviewed mathematical proof.
An independent rerun and targeted cases passed another 28 original-network
global solves. A separate reviewer implementation passed 56 copy-network
projection LPs and 110 full pooling LPs at fixed compositions, including
60 compositions excluded by the source cone. The latter are fixed-
composition checks and do not claim global nonlinear solves.

The [reviewed NP-membership lemma](fixed-parameter-linear-fibers-np-membership.md)
places fixed-pool/fixed-quality pooling with finite flow bounds in NP,
including arbitrary bypasses. It applies to this construction. Thus:

**Theorem.** The standard pooling decision problem is NP-complete with
one pool, one physical quality having lower and upper output bounds,
arbitrary bypass arcs, and rational finite lower/upper flow bounds.
Hardness holds with only two outgoing arcs from the pool. Equivalently,
two quality coordinates with only upper quality bounds suffice, and all
quality values and bounds can lie in `[0,1]`. Exact source supplies and
exact output demands are permitted. Ordinary NP-completeness is claimed;
strong NP-completeness is not claimed. Upper-flow-bound-only hardness is
established separately by the linked stronger construction.

Prior literature already contains a broad assertion of hardness when
capacities are restored in the one-pool/single-quality bypass class. The
[source comparison](../notes/pooling-single-quality-bypass-novelty.md) discusses
Baltean-Lugojan and Misener, Remark 4.6, explicitly. The contribution
documented here is an explicit reviewed reduction with precise
restrictions, and the matching NP upper bound. A first-in-literature
claim is not justified.
