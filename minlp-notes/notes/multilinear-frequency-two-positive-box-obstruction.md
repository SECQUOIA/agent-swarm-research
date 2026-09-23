# Positive lower bounds destroy bipartite frequency-two exactness

Date: 2026-09-04. Status: exact certificate independently verified; see [the audit](review-multilinear-frequency-two-positive-box-obstruction.md). This is a scope counterexample, not a publication-novelty claim.

The unit-box bipartite exactness theorem in
[the frequency-two result](../results/positive-multilinear-frequency-two-gap.md)
does not extend to arbitrary boxes with positive lower bounds. Already

```
f(x,y,z) = xy + xyz,
(x,y,z) in [1,2] x [1,2] x [1,3],
(xbar,ybar,zbar) = (5/4,5/4,5/2)
```

has termwise gap divided by hull gap equal to `7/6 > 1`.
Every variable appears in at most two nonlinear terms. The dual multigraph
has two term vertices joined by the two shared variables x,y, and one leaf
for z, so it is bipartite.

## Exact envelope certificates

Write x=1+a, y=1+b, z=1+2c. The normalized means are
`(a,b,c)=(1/4,1/4,3/4)`. Since every function below is multilinear, its
convex and concave envelopes can be calculated by distributions on the
eight binary vertices with these prescribed means.

The following affine bounds hold at all eight binary vertices and therefore
throughout the cube:

```
xy       >= 1+a+b,
xyz      >= 2a+2b+3c,
f        >= 4a+4b+4c,
f        <= 2+8a+4b+2c.
```

Their mean values are respectively `3/2`, `13/4`, `5`, and `13/2`.
Each bound is attained by a distribution with the required means:

| Function and bound | Binary states and their probabilities |
|---|---|
| xy lower | 000, 001, 011, 101, each with probability 1/4 |
| xyz lower | 001 with probability 3/4; 110 with probability 1/4 |
| f lower | 001 with probability 1/2; 011 and 100 each with probability 1/4 |
| f upper | 000 with probability 1/4; 001 with probability 1/2; 111 with probability 1/4 |

Thus the exact hull interval is `[5,13/2]`. For completeness, individual
upper affine bounds are `xy <= 1+2a+b` and `xyz <= 1+6a+3b+2c`.
They are attained by the same distribution listed for the upper bound of f.
Their sum is therefore the exact termwise upper value `13/2`. The termwise
lower value is `3/2+13/4=19/4`. Consequently

```
tbtgap = 13/2 - 19/4 = 7/4,
chgap  = 13/2 - 5    = 3/2,
tbtgap/chgap = 7/6.
```

The obstruction is incompatibility of the shared (a,b) distribution. The xy
lower bound requires no mass at a=b=1, while the displayed optimum for xyz
uses positive mass there to place both high factors with low z. Separate
local convex-envelope laws need not agree on shared variables.

This example refutes only the all-positive-box extension of bipartite
exactness. It does not refute a universal `3/2` bound on such boxes. The
unit-box and zero-lower-bound theorems remain valid.

A later [positive-box investigation](multilinear-frequency-two-positive-box-investigation.md)
gives a reviewed three-variable family whose bipartite ratio approaches 3/2.
