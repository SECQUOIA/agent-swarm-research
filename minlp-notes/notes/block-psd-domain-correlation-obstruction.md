# A thin projected domain cannot be replaced by a product without a count loss

Date: 2026-09-05. Status: independently reviewed scope example.

The original independent-domain condition in the block PSD theorem is
substantive. Two rank-one scalar blocks after a rational change of
variables can have a formulation count arbitrarily smaller on their
actual thin domain than on its enclosing product box.

Let `L>=1`, `epsilon=4^(-L)`, and `delta=epsilon/16`. On the original
unit square take

```
f_1(x)=x_1^2,
f_2(x)=(x_1+delta x_2)^2,
```

with separate error tolerances `epsilon`. Both quadratics are convex.
Define the rational coordinates

```
z_1=x_1,
z_2=(x_1+delta x_2)/(1+delta).
```

Their image `Omega` is a full-dimensional parallelogram contained in
`[0,1]^2`, of area `delta/(1+delta)`. In the new variables the outputs
are the independent positive scalar blocks

```
g_1(z)=z_1^2,
g_2(z)=(1+delta)^2 z_2^2.
```

On the actual domain, at most `L` binaries suffice. Use the standard
one-coordinate square grid for `x_1`, with `L` bits and residual width
`2^(-L)`. Its shared square approximation `v` contains the exact square
graph and has error at most `epsilon/4`. Introduce a continuous variable
`0<=d<=2delta+delta^2` and set

```
w_1=v,       w_2=v+d.
```

Every exact graph point is included by taking `v=x_1^2` and
`d=2delta x_1x_2+delta^2 x_2^2`. Every admitted output satisfies

```
|w_1-f_1(x)|<=epsilon/4,
|w_2-f_2(x)|<=epsilon/4+2delta+delta^2<epsilon.
```

All rows and coefficients are rational with polynomial encoding length.
Thus `p_bin(g,Omega)<=L` by the exact affine change of variables.

In contrast, on the entire product square, each parity support has
coordinate diameter at most `2sqrt(epsilon)` in `z_1` and
`2sqrt(epsilon)/(1+delta)` in `z_2`, by the two quadratic midpoint
gaps. Its area is at most `4epsilon/(1+delta)`. Covering the unit square
therefore gives

```
p_conv(g,[0,1]^2)>=log2[(1+delta)/(4epsilon)]>2L-2.
```

The enclosing product problem thus needs at least `L-2` more integers
than the explicit formulation on the actual domain, an unbounded gap
with fixed dimensions and fixed block ranks. This does not contradict
the block theorem: its blockwise quotients preserve a product of domains
because the original coordinate blocks are independent. It also does
not contradict the general input-rank theorem, which explicitly retains
the domain-volume term before normalization.

The example explains why arbitrary copy-variable blocks or an arbitrary
linear transformation cannot silently be treated as independent original
blocks. No novelty claim is made for thin-domain effects in isolation.

The [independent audit](review-block-psd-unconditional-precision-second.md)
also verified this example.
