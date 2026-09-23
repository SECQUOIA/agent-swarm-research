# An exponential rational encoding separation between MILP and MISOCP

Date: 2026-09-05. Status: independently reviewed theorem. Two full proof
audits and a bounded source assessment are complete. The conic-duality construction is an application of
classical strong duality; no new duality principle is claimed.

The [rational MILP barrier](../notes/small-exponent-rational-formulation-barrier.md)
requires total encoding length `Theta(D)` for a fixed-error graph tube of
`x^(1/D)`, even though four binaries suffice. For `D=2^B`, the construction
below gives the same approximation with four binaries and a rational
mixed-integer second-order cone formulation using `O(B)` constant-size
coefficients, or `O(B log(B+2))` total bits in ordinary sparse encoding.

## A conic representation of a fixed optimum multiplied by a variable

Consider a finite-dimensional conic linear program and its dual,

```
P: min c^T z,       A z=b,         z in K,
D: max b^T u,       A^T u+s=c,     s in K*.
```

Assume both have attained optima with the same finite value `v`. For a
nonnegative variable `theta`, introduce conic variables `z,u,s` and impose

```
A z=theta b,          z in K,
A^T u+s=theta c,      s in K*,
c^T z=b^T u=t.                                         (1)
```

Then the projection onto `(theta,t)` is exactly

```
{(theta,t):theta>=0, t=theta v}.                       (2)
```

For `theta>0`, divide the primal and dual variables by `theta`. They are
feasible for the original primal and dual. Weak duality gives
`c^T z>=theta v>=b^T u`; the imposed equality forces (2). Conversely,
scale an attained primal-dual optimal pair by `theta`.

At `theta=0`, fix any feasible original primal `z0` and dual `(u0,s0)`.
For a solution of (1),

```
c^T z=s0^T z>=0,
b^T u=-z0^T s<=0.
```

Their equality implies `t=0`. Taking all three new variables zero supplies
such a solution. Thus no unwanted recession value appears at zero.
All constraints in (1) are conic linear: no product of two variables is
used. For a product of second-order cones and elementary free or nonnegative
cones, the primal and dual cone descriptions have comparable rational size.

## Exponentially small rational constants from short SOCPs

Fix a rational `a in (0,1)` with constant-size encoding and an integer `B>=1`.
Consider

```
min z_B,
z_0=a,
z_i >= z_(i-1)^2,       i=1,...,B.                    (3)
```

Each inequality is a rotated second-order cone constraint, with its second
cone coordinate fixed to `1/2`. The system has `O(B)` rational encoding
length in a structured explicit cone description. Its optimum is

```
v=a^(2^B).
```

Indeed all `z_i` are nonnegative, successive squaring gives the lower bound,
and setting each inequality to equality attains it. The explicit rational point
`z_i=a+i(1-a)/(B+1)` is strictly increasing and lies in `(0,1)`, so each
`z_i` strictly exceeds the preceding square. It gives strict conic
feasibility with polynomial-bit coordinates. Standard SOCP strong duality supplies an attained dual optimum.
Conversion to primal-dual conic standard form is linear in description size.
Applying (1) therefore represents the line `t=theta a^(2^B)`, `theta>=0`,
with `O(B)` rational conic encoding, without writing the exponentially long
rational number `a^(2^B)` as a coefficient.

The constants `a=0` and `a=1` are represented directly by `t=0` and
`t=theta`. No duality argument is needed for them.

An explicit dual certificate is also available. Put `v_i=a^(2^i)`,
`lambda_B=1`, and `lambda_i=2v_i lambda_(i+1)` for `i<B`.
For each squaring cone, the vector

```
lambda_i (1, 2v_(i-1)^2, -2v_(i-1))
```

belongs to its rotated second-order dual cone. Pairing it with
`(z_i,1/2,z_(i-1))` and summing over `i` telescopes to `z_B-v_B`, since
`z_0=a`. Each pairing is nonnegative and vanishes at the displayed primal
optimizer. This directly certifies dual attainment and the claimed value.
These certificate coordinates may have exponentially many rational bits;
they are witnesses, not coefficients written into the formulation.

## Four binary variables and a fixed-error root graph

Set `D=2^B` and let `a_j=(j/16)^D` for `j=0,...,16`. As in the rational
MILP upper bound, use four binary index bits to select one of 16 segments.
Continuous selectors `lambda_j>=0`, summing to one and bounded above by
the matching index literals, are forced to the selected unit vector.
Introduce `0<=w_j<=lambda_j` and nonnegative weights

```
r_j=lambda_j-w_j,         s_j=w_j.
```

For each segment, use two copies of (1)--(3) to represent

```
X_j=a_j r_j,             Y_j=a_(j+1) s_j.
```

These are conic linear representations of multiplication by fixed optimal
values, not bilinear equalities imposed as constraints. Set

```
x=sum_j (X_j+Y_j),
t=sum_j (j lambda_j+w_j)/16,
t<=y<=t+1/16.                                        (4)
```

Only the selected segment contributes. Its input runs from `a_j` to
`a_(j+1)` and its linear height from `j/16` to `(j+1)/16`. Concavity and
monotonicity of `f_D(x)=x^(1/D)` imply

```
t<=f_D(x)<=t+1/16.
```

Consequently (4) contains every exact graph point and admits only vertical
errors of magnitude at most `1/16`, with input projection exactly `[0,1]`.
There are a constant number of conic-value gadgets, each of size `O(B)`,
and exactly four declared binary variables. All numerical input coefficients
have constant bit length, apart from indexing information in the chosen
explicit encoding.

## Separation and encoding convention

In a structured cone-list encoding, the MISOCP description has `O(B)`
coefficients and constant-size rational numerical data. An ordinary sparse
matrix encoding adds at most the index overhead, giving `O(B log(B+2))`
bits. Either convention gives polynomial size in `B`.

In contrast, every rational MILP for the same fixed-error graph approximation
has encoding length `Omega(2^B)`, even with unrestricted integer variables.
The contrast is total formulation encoding, not the number of integers,
which is bounded by four in both constructions. It also does not claim
polynomial exact solution of the MISOCP: its rational optimum values can
have exponentially long explicit encodings.

Strong duality and polynomial-size repeated-squaring cone representations
are established. The specific quantitative separation has a bounded source assessment;
publication priority remains qualified.


The construction uses exact conic constraints and exact primal-dual
objective equality. It gives no tolerance-stable numerical solution claim.
In fact, any polynomial-size rational MILP outer approximation of these
conic constraints that contains the exact root graph must violate the
stated graph-error requirement somewhere, by the rational MILP lower bound.
This distinguishes approximate cone membership from the required vertical
error of the projected graph.


## Review and source scope

Both the [first audit](../notes/review-small-exponent-soc-formulation-separation.md)
and [second audit](../notes/review-small-exponent-soc-formulation-separation-second.md)
passed. They independently checked an explicit dual certificate for the
squaring chain, as well as ordinary conic strong duality. The
[first exact checker](../code/small_exponent_soc/check_first_review.py)
passed 105 rational primal/dual/strict-feasibility certificates and every
one of the 16 selector codes. The MILP lower and upper bounds have their
own two independent audits in the linked supporting theorem.

The [source assessment](../notes/small-exponent-soc-formulation-separation-novelty.md)
credits classical conic examples with exponential solution bit length,
logarithmic power-cone lifts, and repeated-squaring SOCPs. It found no
matching fixed-vertical-error root-graph comparison among the sources
checked. The retained contribution is the explicit formulation-encoding
separation with the same constant integer count; it is not a new conic
duality or power-lifting method.
