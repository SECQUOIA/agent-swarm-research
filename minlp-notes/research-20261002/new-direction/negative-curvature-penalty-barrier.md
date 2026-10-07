# Large positive penalties do not repair the subset-sum growth ratio

Date: 2026-10-02. Status: a direct four-dimensional construction with an
[independent review](../reviews/negative-curvature-penalty-barrier-review.md)
finding no substantive gap. This is a limitation of one proposed hardness
reduction, not a hardness result for the
[negative-curvature algorithmic target](negative-curvature-sparse.md).
No novelty claim is made.

## Construction

Let `B>=3` be an integer and let `M,c>0` be rational. All four variables
`(s_1,s_2,z_1,z_2)` are continuous and belong to `[0,1]`. Define

```
r_1 = s_1-z_1/2,
r_2 = s_2-s_1/2-((B-1)/(4B))z_2,
r_T = s_2-1/4,
F = M(r_1^2+r_2^2+r_T^2)
    + c[z_1(1-z_1)+z_2(1-z_2)].
```

This is the two-item instance `a_1=B,a_2=B-1` from the
[mode-wise barrier](modewise-growth-barrier.md), with both binary
variables relaxed to intervals and given concave endpoint penalties.
Its interaction graph has the path bags `{s_1,z_1}` and
`{s_1,s_2,z_2}`, so the largest bag has size three and its treewidth is
two. The variable count is four; there are no discrete variables.
All coefficients have encoding length polynomial in the encodings of
`B,M,c`.

Every term in `F` is nonnegative on the box. A zero requires binary
`z_1,z_2` and all three residuals zero. The latter equations imply

```
B z_1+(B-1)z_2=B.
```

For `B>=3`, its only binary solution is `(1,0)`. Hence the unique global
optimizer and value are

```
x*=(s_1,s_2,z_1,z_2)=(1/2,1/4,1,0),       f*=0.
```

## A fractional witness invisible to every positive penalty

Put `q=1-1/B` and take

```
y=(1/(2B),1/4,1/B,1).
```

The point belongs to the box and has `r_1=r_2=r_T=0`. Direct evaluation
gives

```
F(y)=c(B-1)/B^2=cq/B,
||y-x*||^2=1+(5/4)q^2.
```

Therefore every constant `g>0` satisfying the global point-growth
inequality `F(x)>=g||x-x*||^2` throughout the box must obey

```
g <= cq/[B(1+(5/4)q^2)].                             (1)
```

This bound is independent of `M`: the fractional witness satisfies the
penalized affine equations exactly.

A positive global growth constant does exist for each fixed instance.
Here is a local argument, followed by compactness. Near `x*`, put
`e_1=1-z_1` and `e_2=z_2`, so `0<=e_i<=1/2`. Then
`z_1(1-z_1)+z_2(1-z_2)>= (e_1+e_2)/2 >= (e_1^2+e_2^2)/2`.
Writing `d_i=s_i-s_i*`, the residual equations give

```
d_1=r_1-e_1/2,
d_2=r_2+d_1/2+((B-1)/(4B))e_2.
```

These linear identities bound `||x-x*||^2` by a fixed finite multiple
of `r_1^2+r_2^2+e_1^2+e_2^2`. The positive coefficients `M,c` therefore
give local quadratic growth. Outside such a neighborhood, the ratio
`F(x)/||x-x*||^2` has a positive minimum by compactness and uniqueness.
Thus (1) reflects a small growth constant, not a failure of growth to
exist.

## The negative curvature cannot vanish as the penalty grows

Let `H` be the Hessian of `F`, and define
`nu=max(0,-lambda_min(H))`. If `A` is the three-by-four matrix of the
linear residual coefficients, then

```
H=2M A^T A-2c diag(0,0,1,1).
```

The first term is positive semidefinite, so `nu<=2c`.
Now use the nonzero direction, in the same coordinate order,

```
v=((B-1)/2,0,B-1,-B).
```

Each residual's linear part vanishes on `v`: `Av=0`. Consequently

```
v^T H v = -2c[(B-1)^2+B^2],
||v||^2 = (5/4)(B-1)^2+B^2,
nu >= 2c[(B-1)^2+B^2]/[(5/4)(B-1)^2+B^2]
    >= (8/5)c.                                      (2)
```

A Rayleigh direction need not itself be a feasible displacement from
the box optimizer: `nu` is defined by the ambient Hessian. In this
example the direction is also parallel to `y-x*`, up to sign and scale.

Combining (1) and (2), every admissible global growth constant satisfies

```
nu/g >= (8/5) B [1+(5/4)q^2]/q >= (8/5)B.            (3)
```

Thus the negative-curvature/growth ratio grows without bound with `B`,
and can grow exponentially in its binary encoding length. This holds
for every positive penalty weight `M`, even when `M` depends on `B` and
is arbitrarily large, and for every positive concavity weight `c`.

## What the example establishes

A natural attempted reduction starts from hard binary affine equations,
relaxes the binaries to intervals, adds a concave endpoint penalty, and
uses a large positive quadratic penalty for the affine equations. This
example shows why merely increasing that positive weight cannot provide
a uniform `nu/g` guarantee for the subset-sum construction. A nearly
integral fractional point can satisfy every affine equation while
remaining far from the unique integral solution. The endpoint penalty
at that point is small; scaling its coefficient also scales the negative
curvature.

This four-variable family is not computationally hard. It neither rules
out the proposed algorithm parameterized by bag size and `nu/g` nor
proves that every possible hardness reduction must fail. It identifies
an explicit obstruction which a different reduction would have to avoid.

## Verification

The displayed calculations are exact algebra. A targeted inline
`python3 - <<'PY'` command using `fractions.Fraction` checked 882 instances:
every `B` from 3 through 100, `M in {1/1000,1,10^6}`, and
`c in {1/13,1,100}`. It verified the unique binary zero, the fractional
witness's objective and squared distance, the residual-null Rayleigh
direction and its parallelism with the witness displacement, both
Rayleigh bounds, and the displayed growth-ratio expression. All checks
passed. These checks support the formulas; the proof covers all stated
parameters. The independent review checked the full written algebra
and scope; it did not rerun these author checks.
No external literature search, project-wide verification, or CI inspection
is part of this note.
