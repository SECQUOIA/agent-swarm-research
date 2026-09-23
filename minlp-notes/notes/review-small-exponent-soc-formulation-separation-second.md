# Second independent audit of the small-exponent conic separation

Date: 2026-09-05. Reviewer: `binary_formulation_review`.

**Verdict: PASS.** I independently checked
[the conic formulation separation](small-exponent-soc-formulation-separation.md),
including attained strong duality, zero interpolation weights, exact segment
selection, rational standard-form size, and applicability of the MILP encoding
lower bound. No correction was needed.

## Homogeneous primal-dual value representation

For `theta>0`, division by `theta` produces a feasible point of each original
conic program. Their attained common value `v` lies between the two scaled
objectives. Equality of those objectives therefore forces `t=theta v`.
Conversely, scaling any attained optimal pair supplies a feasible lift for
every positive `theta`.

The zero case is a separate necessary check and is handled correctly. Fix
original feasible primal and dual points `z0` and `(u0,s0)`. If `theta=0`,
then `Az=0` and `A^T u=-s`. Therefore

```
c^T z=(A^T u0+s0)^T z=s0^T z>=0,
b^T u=(Az0)^T u=-z0^T s<=0.
```

Their imposed equality forces `t=0`, and setting all homogeneous variables
to zero supplies a lift. The argument does not require bounded primal or
dual feasible sets, nor bounded optimal witnesses. It excludes precisely the
unwanted nonzero recession outputs that a primal-only homogenization could
admit.

All products in the actual constraints multiply `theta` by fixed original
data. The equation `c^T z=b^T u` is linear; no product between a primal and
dual variable is imposed. For products of second-order cones and free or
nonnegative coordinate spaces, writing the dual cone costs only a constant
factor in description size.

## Repeated squaring, strict feasibility, and dual attainment

The constraints are `(z_i,1/2,z_(i-1))` in the rotated cone

```
K_rot={(u,v,w): u>=0, v>=0, 2uv>=w^2}.
```

They imply `z_i>=z_(i-1)^2` and nonnegativity of every `z_i`. With fixed
`z_0=a in (0,1)`, induction gives `z_i>=a^(2^i)`; equality at every stage
attains the minimum `a^(2^B)`.

Strict feasibility is available with polynomial-bit witnesses, for example

```
z_i=a+i(1-a)/(B+1),    i=0,...,B.
```

All these numbers lie in `(0,1)` and increase strictly, so
`z_i>z_(i-1)>z_(i-1)^2`. Duplicating cone coordinates and imposing linear
consistency equations gives rational conic standard form with linearly many
nonzero coefficients.

The needed imported duality statement is explicit in
[Boyd–Vandenberghe, *Convex Optimization*](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf),
Section 5.9.1, printed page 265: strict feasibility for convex generalized
inequalities implies strong duality and attained dual optimum. I read that
statement and the standard-form dual in Example 5.12. The assumptions apply
here, and primal attainment was established directly.

There is also a direct independent certificate of dual attainment. Set
`v_i=a^(2^i)`, `v_0=a`, and

```
lambda_B=1,
lambda_i=2v_i lambda_(i+1),     i=B-1,...,1.
```

For each stage the vector

```
d_i=lambda_i (1,2v_(i-1)^2,-2v_(i-1))
```

belongs to the self-dual rotated cone. Its cone determinant is zero and
its first two coordinates are nonnegative. Pairing with the primal cone
coordinate gives the nonnegative affine expression

```
lambda_i[z_i+v_(i-1)^2-2v_(i-1)z_(i-1)].
```

Summing telescopes to `z_B-v_B` on the affine subspace `z_0=a`: all
intermediate coefficients cancel by the recursion, the coefficient of
`z_B` is one, and the expression vanishes at `z_i=v_i`. This is a finite
dual cone certificate attaining the same value as the primal chain.
Its coordinates may have long rational encodings; they are feasible
witnesses, not data written into the formulation.

Use of rotated cones introduces no irrational numerical coefficients.
For example `z_i>=z_(i-1)^2` also has the ordinary SOC representation
`||(2z_(i-1),z_i-1)||_2<=z_i+1`. More generally, the rotated cone above
has the rational representation `||(2w,u-2v)||_2<=u+2v`. Thus either a
rotated-cone primitive or an ordinary Lorentz-cone convention preserves
the stated rational encoding.

## Segment selection and both graph inclusions

The four binary variables index sixteen distinct segments. Every continuous
selector is bounded above by all four matching literals. At any integral
index, fifteen selectors are forced to zero and the sum-to-one equation
forces the matching selector to one. For unselected segments,
`0<=w_j<=lambda_j` forces `w_j=0`, hence both interpolation weights vanish.
The homogeneous value representation then forces `X_j=Y_j=0`, even if
some internal homogeneous conic variables are nonzero.

For the selected segment, write its local interpolation weight as `w in
[0,1]`. The projected input and chord height are exactly

```
x=(1-w)(j/16)^D+w((j+1)/16)^D,
t=(j+w)/16.
```

The input endpoints increase from zero to one, so the segment union covers
the entire domain. Concavity puts the root function above this chord.
Monotonicity bounds it by `(j+1)/16`, which is at most `t+1/16`.
Both the exact graph value and every permitted output lie in the same
interval `[t,t+1/16]`. This proves exact graph containment and the required
two-sided vertical error bound. The endpoints `a=0,1` use exact linear
equalities and need no strict-feasibility argument.

## Encoding separation

There are only a constant number of value gadgets, each with `O(B)`
three-dimensional cones, variables, and nonzero rational coefficients.
The constants `j/16`, `1/2`, and all selector coefficients have constant
bit length. Dualizing transposes a sparse matrix and adds cone coordinates;
it does not insert the tiny optimum as a coefficient. Thus a structured
cone-list representation has `O(B)` numerical data and a sparse indexed
representation has `O(B log(B+2))` total bits. Both are polynomial in the
binary exponent length.

I also reread the imported
[rational MILP barrier](small-exponent-rational-formulation-barrier.md).
It applies to the same domain and the same error `1/16`, allows arbitrary
continuous auxiliaries and unrestricted integer variables, and gives
encoding length `Omega(D)`. Fixing the integer witness affects the LP's
right-hand-side numerator but not its basis determinant. Row-wise denominator
clearing bounds the determinant bit length by a constant times total
formulation encoding. The small positive LP optimum at most `2^(-D)`
therefore gives the claimed lower bound. Its four-binary upper construction
has encoding `O(D)`, so the MILP order is `Theta(D)`.

Putting `D=2^B` establishes the exponential encoding separation between
rational MILP and rational MISOCP at the same fixed graph accuracy, while
four binaries suffice in either construction. It is a separation of
formulation descriptions, not a polynomial-time exact conic optimization
algorithm or a polynomial bound on the encoding of every feasible witness.
The argument uses established conic duality and repeated-squaring tools;
novelty of the quantitative application is a separate source question.
