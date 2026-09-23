# Three positive-power outputs already rule out a one-integer lift

Date: 2026-09-05. Status: independently checked supporting refinement; [the review](review-positive-vector-three-witness-integer-obstruction.md) passed. This records why the first nontrivial ternary-code attempt does not separate binary and general-integer formulations. The subsequent [cap-set argument](positive-vector-capset-integer-lower-bound.md) gives a shorter proof and a higher-dimensional extension.

Use the family from [the reviewed vector refinement obstruction](positive-polynomial-vector-refinement-obstruction.md), with at least three components:

```
F_j(x)=(7/4)x^(D_j),   D_j=128*1024^(j-1),
x_j=1-64/D_j,
K=[-1,1]^M.
```

For `M=3`, the stronger conclusion is

```
p_conv=p_bin=2.
```

The previously reviewed finite upper construction uses `ceil(log2(M+1))=2` binaries. It remains to rule out one general integer, including unbounded integer labels and unrestricted convex lifts.

## 1. Far-apart integer labels already contradict a two-point chord

For selected witness inputs `x_j<x_l`, the earlier Bernoulli estimate gives `x_l^(D_j)>=15/16`. For any chord weight `t in [2/3,4/5]` on the higher input, the combined input satisfies

```
xi=(1-t)x_j+t x_l <=1-64/(5D_j).
```

Since `exp(v)>=v^2/2` for `v>0`,

```
xi^(D_j)<=exp(-64/5)<=25/2048.
```

Thus the component-j chord error is at least

```
(7/4)[(2/3)(15/16)-25/2048]=8785/8192>1.       (1)
```

Suppose two integer witness labels differ by `q>=3`. There is a rational weight `t=k/q` in `[2/3,4/5]`: take `k=ceil(2q/3)` (the cases `q=3,4` are direct; for `q>=5`, `k<=(2q+2)/3<=4q/5`). Their convex combination has an integer label, regardless of which label is attached to the higher input, contradicting (1). Therefore every pair of selected witness labels must differ by at most two. Equal labels are also impossible by the previously established two-thirds chord obstruction.

Three distinct witness labels must consequently be three consecutive integers.

## 2. The middle fiber excludes three consecutive labels

Take the midpoint of the lifted graph witnesses carrying the two extreme labels. Its integer label is the middle label. It can therefore be combined with the third exact graph witness by an arbitrary convex weight while retaining an integer label.

Let `x_j` be the smallest of the three selected inputs. If its graph witness carries the middle integer label, combine it with weight `1/3` and the extreme-label midpoint with weight `2/3`. If it carries an extreme label, combine the extreme-label midpoint with weight `2/3` and the middle-label exact witness with weight `1/3`. In either case the resulting point has an integer label, weight exactly `1/3` on the smallest input, and total weight `2/3` on larger selected inputs.

Those larger inputs all have component-j powers at least `15/16`, whereas the new input obeys `xi<=1-64/(3D_j)`. The earlier bound `xi^(D_j)<=3/67` therefore gives error at least

```
(7/4)[(2/3)(15/16)-3/67]=2177/2144>1.
```

This contradicts the allowed output error. Hence no convex lift with one unrestricted integer variable exists, proving the claim.

## Interpretation

All pairwise exact graph midpoints remain admissible, as established in the original note. Nevertheless a midpoint in an integer fiber can be mixed again with a graph witness in that same fiber. This second convexification creates a forbidden non-midpoint error. It is not enough to check the pairwise integer points on segments between assigned graph labels.

The argument treats arbitrary integer labels, not merely the labels `0,1,2`. It proves neither a general constant binary/general gap nor optimal integer counts for larger numbers of components. Its value is to close the smallest apparent ternary-code opportunity in the existing family.
