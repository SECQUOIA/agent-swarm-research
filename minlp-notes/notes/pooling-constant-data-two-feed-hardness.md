# Candidate: strong hardness with two pool feeds and constant numerical data

Date: 2026-09-05. Status: two independent full audits PASS. The theorem,
complete proof and supporting LP representation are promoted in
[the final result](../results/pooling-constant-data-two-feed-np-completeness.md).
This working note preserves the original construction plan and checks.

The target is one pool, one scalar upper quality, pool in-degree and
out-degree both two, input total out-degree at most two, output total
in-degree at most three, all flow lower bounds zero, and every numerical
quality/capacity/cost coefficient from a fixed finite set. The objective
threshold is an integer linear in network size. The proposed conclusion
would be strong NP-completeness. The key change is to encode the old
large objective threshold in a linear copy circuit, then maximize exact
contract completion instead of using a large penalty.

## 1. Normalize Matsui's positive factors into a fixed quality interval

Use the explicit Matsui instance already verified in
[the source-copy result](../results/pooling-one-pool-bypass-np-completeness.md).
Write `s=n+n^2`, `p=n^(n^4)`, `n>=5`, and `P4=p^(4n)`. The original
linear factors on simplex generators are integer-valued. Their common
constant is `u0=2P4-p`, and they satisfy

```
u0<=U_i<=u0+s p^(2n)+2s p^(3n),
V_i<=u0+s p^(2n),
K=4 p^(8n).
```

Let `D` be the largest power of two at most `u0/2`. Thus
`2D<=u0<4D`. Since `s<p^n`, the upper bound on `U_i` is less than
`5P4`; also `u0>P4`, so `D>P4/4`. Consequently `2<=U_i/D<20`.
Moreover `D<P4` and `V_i<3P4`, giving `D V_i<3p^(8n)<K`.

Replace factors `U,V` by `U/D,DV`, preserving their product. Define

```
a_i=U_i/D-1 in [1,19),
b_i=K-D V_i>0.
```

Every number still has polynomial binary encoding length. In particular
all `b_i` are positive integers. Define dyadic weights

```
r_i=(a_i-1)/32=(U_i-2D)/(32D) in [0,1).
```

The denominator `32D` is a power of two. Large source data will occur
only in the topology of binary averaging circuits, not as physical
quality, flow-bound or objective coefficients.

## 2. Constant-data linear signal circuits

Use the reviewed full/half closed-copy cycles with ordinary endpoint
qualities zero and three. Their middle qualities are `3/2` and one.
Every signal lies in `[0,2]`. Each requested port occurrence receives a
distinct gadget, as in the reviewed construction.

The following gates use only sources of quality three:

- `v=(u+w)/2`: exact supply two on one full positive `v` port and the
  two complementary half ports `1-u/2,1-w/2`.
- `w=u+v`, when all three signals lie in `[0,2]`: exact supply two on
  full positive ports `u,v` and a full complementary port `2-w`.
- `u=v`: exact supply two on `u,2-v`.
- `u<=v`: upper supply two, lower supply zero, on `u,2-v`.

A zero signal is forced by a zero-upper-supply source on one full
positive port. A unit signal is forced by an exact-one-supply source
on one full positive port. These signal values propagate around their
closed cycles. Full and half cycles for the same signal are coupled by
the reviewed exact-two, three-port source. No gate adds an implicit
nonphysical equation; each displayed equation follows from its source
supply and the already reviewed port identities.

For `c` a nonnegative integer with `c<2^L`, a dyadic multiplier
`y=(c/2^L)x` uses the bits `c_k` from least to most significant:

```
t_0=0,
t_(k+1)=(t_k+c_k x)/2,       k=0,...,L-1,
y=t_L.
```

The zero bit uses the zero signal as the second averaging child. Every
intermediate value lies in `[0,2]`, and induction gives the stated
multiplier. The construction has `O(L)` gates and port occurrences.
Boundary coefficients zero and one can instead use the zero signal or
an equality to the original signal.

To enforce a rational linear row on bounded signals, clear denominators
and write `sum_i c_i x_i<=d` with integer coefficients and constant.
Choose a power of two `B` strictly larger than
`sum_i |c_i|+|d|`. Compute `(abs(c_i)/B)x_i` and the constant
`abs(d)/B` using the unit signal. Sum the positive side and negative
side with partial-sum addition gates, placing the constant on the
appropriate side. Since every signal is at most two and
`B>sum|c_i|+|d|`, each total and partial sum is at most two. Compare
the two sums with one `<=` gate. An equality uses opposite comparisons
or one equality gate between those sums. This represents each row with
polynomially many gates in its binary encoding length. The zero row and
zero constants require no special numerical data.

This general circuit representation is an explicit construction to be
audited. The eventual hardness reduction only needs the homogeneous
source-cone rows, dyadic master-feed weights, and one objective-threshold
row described below.

## 3. Two actual pool feeds

Let `x_i` be the original source-cone signals and enforce `Cx<=0` with
the circuits. Introduce signals

```
T=sum_i x_i,
h=sum_i r_i x_i,
l+h=T.
```

All are in `[0,2]`, so the total-intake bound is enforced. The partial
sums defining `T` and `h` remain in `[0,2]` whenever the intended
assignment is feasible: `0<=r_i<=1` and `sum x_i<=2`. Conversely the
addition gates and final bounds enforce these equations exactly.

Only `l` and `h` receive actual pool-intake conversion gadgets, with
endpoint qualities one and 33, respectively. Both are positive, so the
reviewed closed-full-cycle argument applies. Their exact-two source
supplies force actual pool intakes to equal `l,h`. Original `x_i` signals
remain wholly within the direct copy network. The pool's quality mass is

```
l+33h=T+32h=sum_i a_i x_i.
```

The two primary outputs and anchor are unchanged: the pool serves two
unit-capacity outputs, the first has upper quality one and a zero-quality
anchor of capacity one, and the second has redundant upper quality 33.
The pool's upper capacity is two. Thus its maximal radial throughput for
an active source mixture is `1+1/a(z)`, with `a(z)>=1`.

Finally enforce the affine signal inequality

```
sum_i b_i x_i >= K
```

by the binary circuit construction. No large physical objective
coefficient is used. A feasible contracted network must have positive
original signal total. Setting `z=x/T` then yields `z in P` and
`b(z)T>=K`. Since `T<=1+1/a(z)`, this holds for some network flow
exactly when

```
b(z)(1+1/a(z))>=K
iff (U(z)/D)(D V(z))<=K
iff U(z)V(z)<=K.
```

The converse chooses the maximal feasible radial throughput and fills
all circuit signals and copy flows. Unlike the earlier penalty setup,
this exact-contracted network need not be feasible at zero intake; the
positive threshold circuit intentionally excludes it. No Hoffman error
bound is needed in the final step below.

## 4. Reduce input degrees while keeping constant capacities

A degree-three averaging or full/half-coupling source has port capacities
`(2,1,1)` and exact supply two. A degree-three addition source has port
capacities `(2,2,2)` and exact supply two. Split either source into three
same-quality sources of exact supplies `c_h`, each feeding its original
port and one common collector. The collector's exact demand is
`sum_h c_h-2`, respectively two or four. Its upper quality equals the
common source quality and is redundant. Complementary flows prove exact
projection in both directions, as in the reviewed source splitter.

All inputs now have total out-degree at most two, all outputs have total
in-degree at most three, and the sole pool has exactly two inputs and
two outputs. Every upper flow bound belongs to `{0,1,2,3,4}`. The full
input-quality alphabet is contained in

```
{0, 1/2, 1, 3/2, 3, 33/2, 33}.
```

Every output upper quality bound also belongs to this fixed set. Divide
all qualities by 33 if values in `[0,1]` are desired; the resulting
finite alphabet is fixed independently of the source instance.

## 5. Delete every positive lower flow bound by contract completion

Let `Ew=e` list all exact input-supply and exact output-demand contracts
in the final network, including constant-generation and collector nodes.
Each `e_j` belongs to `{1,2,3,4}`; zero contracts can be omitted.
Their corresponding upper bounds `Ew<=e` remain in the model. Delete
all positive lower flow bounds. Give the new objective

```
maximize sum_j E_j w,
threshold S=sum_j e_j.
```

Each summand is at most `e_j`, and every deficit is nonnegative.
Therefore an upper-only feasible flow reaches `S` if and only if it
satisfies every exact contract. Its remaining physical constraints and
all circuit port implications are then precisely those of the
contracted instance. Thus reaching `S` is equivalent to the original
positive-product yes answer. The objective is an ordinary linear arc
profit with coefficients at most two: an arc can be incident to at most
one contracted input and one contracted output. The threshold is at
most four times the number of contracted nodes.

For standard economics, give a contracted input production cost minus
one, other inputs zero, and a contracted output revenue one, others
zero. Add one to every input cost and every output revenue. Total mass
conservation cancels this offset. All resulting input costs belong to
`{0,1}` and output revenues to `{1,2}`, and the objective still equals
contract completion exactly. No publication, approximation or penalty
argument is needed for this equivalence.

The transformed instance has polynomial size and all numerical input
values bounded by a fixed constant except `S`, which is polynomial in
network size. Even unary encoding is polynomial. Its decision problem
is in NP by the reviewed one-pool/one-quality linear-fiber certificate.
If every construction detail passes independent review, this proves
strong NP-completeness under the target restrictions.

Strong hardness here concerns the exact rational decision problem. It
does not provide an inverse-polynomial completion gap between yes and
no instances, an approximation barrier, or robustness to fixed feasibility
tolerances. Binary averaging chains can encode very small flow differences
despite their constant local coefficients. No such gap claim is needed
for strong NP-completeness.

## Review obligations

The highest-priority checks are the Matsui normalization inequalities,
polynomial binary-circuit encoding, bounded partial sums, joint full/half
signal cycles, actual two-feed interface, threshold circuit equivalence,
constant-data source splitting, and completion-objective economics.
Original-network checks must enforce only physical arcs and node/quality
constraints, never the intended circuit equations directly.

The [author checker](../code/pooling_bypass_copy/check_constant_data.py)
has passed 12 original-network global contract-completion solves. They
include feasible and infeasible thresholds, an empty source slice, an
equality slice, and the `a=1` boundary. The solver receives only physical
arcs, supplies, demands and upper quality rows. Its normalized objective
is minus the sum of contract deficits, exactly completion minus its known
constant upper bound. It verifies the fixed numerical palette and all
claimed degree bounds. Relaxing just the threshold-comparison input's
upper supply from two to four changes an infeasible threshold into an
attainable completion target. The
[log](../code/pooling_bypass_copy/constant_data_output.txt) is retained.
The [first full review](review-pooling-constant-data-two-feed.md) and
[second full review](review-pooling-constant-data-two-feed-second.md)
both PASS. They retain the independent network constructors, exact
arithmetic checks, source normalization checks and their distinct global
versus fixed-quality physical solve counts.
