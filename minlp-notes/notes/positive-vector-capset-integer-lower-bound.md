# Positive vector graph contacts force a cap set modulo three

Date: 2026-09-05. Status: supporting lower bound; [independent full audit passes](review-positive-vector-capset-integer-lower-bound.md). This strengthens the general-integer lower estimate for the [reviewed positive-power vector family](positive-polynomial-vector-refinement-obstruction.md). The cap-set theorem itself is due to Ellenberg and Gijswijt and is not a new ingredient.

## 1. The contact residues are progression-free

Use

```
F_j(x)=(7/4)x^(D_j),   D_j=128*1024^(j-1),
x_j=1-64/D_j,   j=1,...,M,
K=[-1,1]^M.
```

Choose exact graph witnesses in an arbitrary admissible convex lift with `p` general integer variables, and denote their integer vectors by `z_j`.

The existing two-point proof shows that distinct witnesses cannot have the same residue modulo three: their weighted combination with coefficients `1/3,2/3`, placing the larger weight on the larger input, has integral coordinates and component error at least `2177/2144>1`.

Now take three distinct witness indices and let `j` be the smallest. If their integer residue vectors sum to zero in `F_3^p`, the uniform average of the three lifted witnesses has an integer vector. Its input satisfies

```
xi <=1-64/(3D_j).
```

Both larger selected inputs have component-j powers at least `15/16`, by the earlier Bernoulli estimate, whereas `xi^(D_j)<=3/67`. Hence this average also has component error at least

```
(7/4)[(2/3)(15/16)-3/67]=2177/2144>1.
```

This contradiction proves that the `M` distinct residues have no three distinct elements summing to zero. Over `F_3`, any solution with two equal elements has all three equal, so this is exactly the cap-set property: there is no nontrivial three-term arithmetic progression.

Therefore, if `cap(p)` denotes the maximum size of a cap set in `F_3^p`, every admissible lift satisfies

```
M<=cap(p).                                                (1)
```

No integer range, lift-size, measurability, or closedness assumption is needed. The argument uses only finitely many exact graph contacts and convex combinations whose integer coordinates remain integral.

## 2. An exponential cap-set bound gives a stronger integer lower bound

Ellenberg and Gijswijt's Theorem 4 states

```
cap(p)<=3 * #{alpha in {0,1,2}^p: sum_i alpha_i<=2p/3}.
```

I directly checked this theorem and its specialization to `F_3` in the [primary paper](https://arxiv.org/pdf/1605.09223), printed pages 2--3. Their polynomial method is credited in full; the application here is the graph-contact residue reduction above.

For any `0<t<1`, the monomial count is at most

```
t^(-2p/3)(1+t+t^2)^p.
```

Indeed each allowed multi-index has `t^(sum alpha_i-2p/3)>=1`, and summing over all multi-indices gives the bound. Define

```
c_* = min_(0<t<1) (1+t+t^2)t^(-2/3)
    = (1+t_*+t_*^2)t_*^(-2/3),
t_*=(sqrt(33)-1)/8,
c_*=2.755104613...<3.
```

The minimizing equation is `4t^2+t-2=0`. Combining with (1) yields the finite bound

```
M<=3 c_*^p,
p_conv>=max(0,ceil(log_(c_*)(M/3))).                     (2)
```

A simpler fully explicit constant is `c=14/5`: using `t=1/2` gives `(7/4)2^(2/3)<14/5`, so `M<=3(14/5)^p`. This improves the old `M<=3^p` asymptotic exponent. For small dimensions, the exact cap bound in (1) is stronger than the prefactor-three exponential estimate.

## 3. The first ternary attempt is already impossible

In `F_3`, a cap set has at most two elements, since its three elements sum to zero. Thus `M=3` requires `p_conv>=2`. The previously reviewed upper construction uses `ceil(log2(M+1))=2` binary variables, proving

```
p_conv=p_bin=2   when M=3.
```

This supplies a shorter proof of the independently checked [three-witness obstruction](positive-vector-three-witness-integer-obstruction.md). Pairwise midpoint compatibility still holds for every pair of graph points. The extra information comes from non-midpoint pair combinations and three-point barycenters, not a stronger midpoint estimate.

## Limits

This is a supporting strengthening, not an unbounded binary/general-integer separation. The cap-set upper bound has exponential base larger than two, and no matching small-integer convex lift is constructed. It also does not improve the original family's encoding convention: its degrees grow rapidly with the number of outputs. The new point is that a higher-order convex-combination obstruction can import finite-field extremal bounds into integer formulation lower bounds.
