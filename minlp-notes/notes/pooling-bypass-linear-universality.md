# Candidate representation lemma for direct blending networks

Date: 2026-09-05. Status: unreviewed extension; not used by a promoted
theorem. Novelty unclaimed.

**Reviewed successor.** The binary-gate representation has now been
fully composed and independently audited as part of the
[constant-data two-feed result](../results/pooling-constant-data-two-feed-np-completeness.md).
Its supporting corollary gives exact projections for arbitrary rational
linear systems on `[0,2]^m`, using one upper quality, fixed finite
quality/capacity data, input out-degree two and output in-degree three.
The paragraphs below preserve the earlier investigation rather than the
final strongest statement.

The [bypass copy gadget](pooling-one-pool-bypass-copy-hardness.md) suggests
a broader representation result: a bounded rational linear system can be
represented through the flows of a direct blending network with a single
physical quality, input quality values only `0,1,2`, and every output
having exact quality one. Fixed supplies and demands are permitted. This
is a representation of linear programs, not a hardness claim for their
feasibility.

The already described gadget represents systems on signals in `[0,2]`
with bounded integer coefficients: chains provide copies of each signal
and its complement; capacity inputs encode sums of those port flows.
Without another step, making one port per coefficient unit is only
pseudopolynomial for general binary-encoded coefficients.

## Binary halving circuits avoid coefficient replication

Let `0<=x<=2`, and let a nonnegative integer `c` have binary bits
`c_0,...,c_(L-1)`, starting with the least significant bit. Introduce
signals `t_0,...,t_L` and impose

```
t_0=0,
2 t_(k+1) = t_k + c_k x,       k=0,...,L-1.
```

Every intermediate value lies in `[0,2]`, since each is the average of
two values in that interval. Induction gives

```
t_L = (c/2^L) x.
```

Every defining equality uses coefficients of magnitude at most two.
Hence it can be encoded by the basic copy and capacity gadgets with a
constant number of ports per recurrence. An equality is represented by
two inequalities, or an appropriate exact source supply.

For a homogeneous integer row `sum_i c_i x_i<=0`, choose one common bit
length `L` for the row and compute `t_i=(|c_i|/2^L)x_i` by these circuits.
The original row is equivalent to

```
sum_{c_i>0} t_i - sum_{c_i<0} t_i <= 0.
```

It therefore uses only one positive or complementary port per nonzero
coefficient. The number of auxiliary signals, recurrence rows, and ports
is polynomial in the binary encoding of the original row. Rational
coefficients can first be multiplied by a positive common denominator;
the resulting integer bit lengths remain polynomial.

An inhomogeneous row `sum c_i x_i<=d` is handled with the same normalized
sum and a capacity shifted by `d/2^L`. If this capacity would be negative,
the row is already impossible for signals in `[0,2]` when its normalized
lower bound exceeds the right-hand side; such an instance can be mapped
to an explicitly infeasible fixed network. Homogeneous cones are enough
for the pooling reduction and avoid this minor case entirely.

Thus arbitrary rational homogeneous cones intersected with `[0,2]^n`
appear to have polynomial-size direct-blending representations with just
three input quality values. Combined with the quality-conversion gadget,
this would allow the generic normalized positive-product reduction to be
used without Matsui-specific coefficient bounds. The current hardness
draft retains the simpler source-specific bounded-coefficient route.

## Verification still needed

The binary recurrence algebra is immediate, but the complete representation
statement still needs a separate audit of the joint auxiliary-signal
construction, port count, and rational preprocessing. No result is claimed
verified on the basis of this note. Potential relevance includes explaining
why arbitrary bypass graphs need not retain the simpler structure of
ordinary one-commodity network flow, even with very few quality values.

## Possible bounded-degree refinement

Another unreviewed extension replaces a row input with many outgoing ports
by a balanced averaging circuit. If its intended port flows are
`f_1,...,f_m in [0,2]`, pad them with zeros to `2^h` leaves. At each
binary tree node impose `2v=u+w`, so the root is
`v_root=sum_j f_j/2^h`. All auxiliary signals remain in `[0,2]`.
The original row capacity `sum f_j<=B` becomes one root-port capacity
`v_root<=B/2^h`.

Each averaging equality, represented by opposite inequalities, uses at
most four unit-coefficient signal ports because the coefficient of `v`
is two. Complement leaves `2-x_i` can be substituted directly, with their
constant terms absorbed into the source capacity. The resulting row
inputs would have out-degree at most four. Other input types in the copy
network have out-degree at most two, and every gadget output has
in-degree three. Thus the bypass graph may have maximum degree four
while retaining the same hardness construction.

This would distinguish bounded degree from the constructive bounded
vertex-cover and bounded-component-size assumptions. The averaging
identities are straightforward, but a full bounded-degree construction
and two independent reviews are still required before making that claim.
