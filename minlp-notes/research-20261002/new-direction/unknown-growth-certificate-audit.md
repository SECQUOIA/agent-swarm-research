# Certificate audit for unknown growth and arbitrary optimal sets

Date: 2026-10-02. Scope: concrete limits of two proposed certificate
representations, and an algebraic fact that may help another representation.
No external literature search was performed. This is not a complexity lower
bound for all optimization algorithms and makes no priority claim.

## Main findings

The existing full-domain corrected-grid certificate can require an inverse
square root of the requested accuracy in every flat coordinate even on a
connected nonconvex QP with treewidth three and curvature/growth ratio four.
Strict incumbent-based coordinate pruning does not remove this problem.

Exact stationary polytopes provide a finite description of the optimal set,
but explicitly listing those polytopes can require exponentially many pieces
on a connected family with the same fixed treewidth and conditioning. These
two facts rule out directly obtaining the desired unknown-growth FPT result
by combining the current grid certificate with explicit enumeration of all
optimal stationary pieces. They do not rule out a compact, factorized
algebraic certificate.

## 1. A connected nonconvex gadget

On `[0,1]^4`, define

```
F(x,y,u,v) = (x-y)^2 + u^2+v^2-3uv+(u+v)/2
            +(x-y)(u-v)/4.
```

Its optimal set is

```
S = {(t,t,0,0):0<=t<=1} union {(t,t,1,1):0<=t<=1},
f*=0.
```

To verify this and its growth constant, put

```
a=x-y,       b=u-v,       t=(u+v)/2,
r^2=min(t^2,(1-t)^2).
```

The squared distance to the displayed set is

```
dist((x,y,u,v),S)^2 = a^2/2 + 2r^2+b^2/2.
```

The mean of `x,y` lies in their interval, and the two possible mode points
are `(u,v)=(0,0),(1,1)`, so this distance formula holds throughout the box.
Direct calculation gives

```
F - (1/2)dist(.,S)^2
 = (3/4)a^2+(1/4)ab+b^2 + t(1-t)-r^2
 = (3/4)(a+b/6)^2+(47/48)b^2+t(1-t)-r^2
 >= 0.
```

The last term is nonnegative on `[0,1]`. The function is zero on the
displayed set; the inequality makes it positive elsewhere. At `x=y` and
`u=v=1/2`, the ratio of objective gap to squared distance is exactly `1/2`.
Thus the largest global growth constant is `g=1/2`.

Every diagonal Hessian entry is two, so `L=2` and `kappa=L/g=4`. The
Hessian is indefinite: the quadratic coefficient in direction
`(0,0,1,1)` is negative. The interaction graph is the complete graph on
four vertices, with treewidth three. Each partial derivative changes sign
on the box. Thus neither a nonpositive-diagonal endpoint reduction nor
global coordinate monotonicity removes the gadget's nonconvex variables.

The example is nevertheless easy to certify by the displayed algebraic
identity. Its purpose is to separate that possibility from the behavior of
the specified corrected-grid representation.

## 2. Arbitrary irregular grids still require dense flat projections

For coordinate grids containing the interval endpoints, let

```
d_i(v)=L ell_i(v)^2/8,
LB=min_grid [F(y)-sum_i d_i(y_i)],
```

with `ell_i(v)` the largest adjacent grid interval length. The
[conditional-margin lemma](projection-anchors.md), Section 8, states

```
LB <= f*+W_i(v)-d_i(v),
W_i(v)=min_{x_-i} F(v,x_-i)-f*.
```

Fix coordinate `i` at `v` and round the others at a conditional minimizer.
Their corrections cancel their rounding errors, while the fixed coordinate
has zero variance but still pays its correction. This proves the lemma
for unrelated, irregular coordinate grids; alignment is unnecessary.

In the gadget, `W_x(v)=W_y(v)=0` for every `v in [0,1]`. An endpoint of
any grid interval of length `Delta` therefore gives

```
LB <= -Delta^2/4.
```

Every feasible incumbent has value at least zero. A certificate of gap at
most `eps` consequently requires

```
Delta<=2sqrt(eps),
|G_x|, |G_y| >= ceil(1/(2sqrt(eps)))+1.
```

Its explicit four-coordinate bag table has at least `Omega(eps^-1)`
entries. This lower bound is exponential in the requested accuracy bits.
It holds even when an exact optimal candidate of value zero is already
known.

Any strict min-marginal deletion rule that preserves all global optimizers
retains the full `x` and `y` intervals: every coordinate value occurs in an
optimizer. More directly, each adjacent interval has a conditional lower
bound at most zero and hence at most the incumbent. Even if one of the two
optimal mode components is selected by a separate valid method, its `x`
and `y` projections are still `[0,1]`. Fixing `u=v=0` or `u=v=1` leaves
the same corrected-grid obstruction for `(x-y)^2`.

This is a lower bound for the given global grid-and-correction certificate.
It does not apply to convexity certificates, exact elimination, rotations,
or other algebraic lower bounds. In particular, the displayed identity
already supplies a short certificate for this example.

## 3. Exponentially many flat components at the same fixed parameters

Take `m` copies of the gadget, with variables `(x_i,y_i,u_i,v_i)`, and
connect consecutive copies by defining

```
F_m = sum_i F(x_i,y_i,u_i,v_i)
      +(1/16) sum_{i=1}^{m-1} (u_i-v_i)(u_(i+1)-v_(i+1)).
```

The domain is `[0,1]^(4m)`. Its optimal set is the Cartesian product of
the two segments in each gadget. It therefore has exactly `2^m` connected
components, each an `m`-dimensional polytope.

The conditioning remains `L=2`, `g=1/2`, and `kappa=4`. To prove this,
write `a_i,b_i,t_i,r_i` as above. The squared distance to the proposed
product set is the sum of the gadget squared distances. The chain term
satisfies

```
(1/16) sum_i b_i b_(i+1) >= -(1/16) sum_i b_i^2.
```

Subtracting half the squared distance and completing squares now gives
the lower bound

```
F_m-(1/2)dist(.,S_m)^2
 >= sum_i [(3/4)(a_i+b_i/6)^2
           +(11/12)b_i^2+t_i(1-t_i)-r_i^2]
 >= 0.
```

The proposed set has value zero, so it is exactly the optimal set. Equality
in the growth ratio occurs when one pair has `u_i=v_i=1/2`, all other
mode pairs are at their equal endpoints, and every `x_i=y_i`. Thus `g=1/2`
is again sharp. The added terms change no diagonal Hessian entry. The
negative direction with equal changes in one `u_i,v_i` pair also remains,
because all difference variables `b_i` vanish along that direction.
The maximum absolute Hessian row sum is at most `23/4`, uniformly in `m`.
Symmetry gives `||Hessian F_m||_2<=23/4`, so the full-Hessian/growth ratio
is at most `23/2` as well.

The graph is connected and has a path decomposition of bag size four:

```
G_1, C_1, G_2, C_2, ..., C_(m-1), G_m,
G_i={x_i,y_i,u_i,v_i},
C_i={u_i,v_i,u_(i+1),v_(i+1)}.
```

Every interaction is covered and every variable's bags are consecutive.
Each gadget already contains a four-clique, so the treewidth is exactly
three.

Any convex polytope contained in `S_m` lies within one connected component.
In particular, a polytope containing optimal points with different mode
choices would contain a segment that changes some equal endpoint pair
through an interior value, which is outside `S_m`. Hence an exact
description of `S_m` as a union of convex polytopes needs at least `2^m`
nonempty members.

This proves that explicitly enumerating optimal stationary polytopes cannot
have `f(p,kappa) poly(I)` complexity in general. A compact representation
can still exploit the product structure; the component count does not
exclude such a method.

## 4. A useful algebraic fact, with its remaining cost

For any bounded rational mixed box QP, fix an integer assignment and a
continuous box face. Form the stationary polytope by imposing the fixed
face values, the box bounds, and stationarity in the remaining free
coordinates. Whenever this polytope is nonempty, the quadratic is constant
on it: differences of two stationary points lie in the kernel of the free
Hessian, and the quadratic expansion has zero change.

Every global optimizer belongs to the stationary polytope of its own
integer assignment and smallest continuous face. Conversely, any such
polytope whose constant value equals `f*` consists entirely of optimizers.
Thus the full optimal set is a finite union of rational stationary
polytopes. This assertion does not require uniqueness or nonsingular free
Hessians.

There is also a uniform rational height bound for every stationary-face
value, not only the optimal one. With the notation of
[the exact-recovery proof](proximal-exact-recovery.md), a vertex uses an
independent system of scaled stationarity rows and bound rows. Its common
coordinate denominator is at most `R=DH`. Its objective therefore has
reduced denominator at most `V=DR^2`. Every point of that stationary
polytope has this same value. Distinct stationary-face values are separated
by at least `1/V^2`.

This does not itself produce a compact global certificate. To verify a
candidate value by explicit stationary-face comparison, one must still
exclude every nonempty face or integer slice with a lower stationary value.
The finite height bound gives a value gap, but neither controls the number
of faces nor compresses their feasibility conditions. Section 3 shows why
enumerating the optimal pieces is already too expensive at fixed width
and conditioning.

The unresolved step is a way to represent and compare these stationary
possibilities using the decomposition, while preserving a polynomial
exponent independent of width and without retaining fine grids along every
optimal projection. None of the preceding lemmas supplies that step.

## 5. A factorized certificate already handles the obstruction family

The family in Section 3 also supplies a concrete positive control. Let
`deg_i` be the degree of vertex `i` in the gadget chain. The following
identity is exact:

```
F_m = sum_i (a_i+b_i/8)^2
      +sum_i (95/64-deg_i/32)b_i^2
      +(1/32)sum_(i,i+1) (b_i+b_(i+1))^2
      +(1/2)sum_i [u_i(1-u_i)+v_i(1-v_i)].
```

Every coefficient of a square is positive, and every remaining term is
nonnegative on the box. Each term is supported by one of the size-four
bags in Section 3. The identity therefore certifies the exact value zero
using a linear number of local terms, without a growth estimate.

Its zero conditions are also a compact description of the full optimum
set: the positive square coefficients force `b_i=0` and `a_i=0`, while
the two bound-product terms force `u_i,v_i` to be endpoints. Thus each
pair independently chooses its common endpoint and each flat pair remains
continuous. This representation keeps all `2^m` components implicit.

Equivalently, the maximal diagonal certificate in
[flat-direction-certificates.md](flat-direction-certificates.md) uses
`D_(u_i,u_i)=D_(v_i,v_i)=1`, with all other entries zero. The square
terms above decompose `H+D` into positive-semidefinite bag factors.
This is an existing-style diagonal Lagrangian certificate, not a new
general exactness theorem. The example is therefore a limitation of the
grid and explicit-enumeration strategies, not evidence against compact
global certificates.

A consequential next target is to construct or rule out bounded-size
factorized certificates beyond this diagonal class. The same accompanying
note gives an explicit escape from a bounded-diagonal-shift obstruction:
cell-dependent shifts with only logarithmic coefficient bit length yield
logarithmically many slabs, even though their numerical magnitudes grow
as inverse accuracy. A complexity argument must permit that behavior
rather than silently introducing the shift norm as another parameter.
Neither example establishes a complete certificate mechanism for all
conditioned bounded-width QPs.

## Verification

An independent reviewer checked the nonconvex gadget, its sharp growth
constant, indefinite Hessian, positive diagonal curvature, and the
arbitrary-grid obstruction. That reviewer also confirmed the connected
family, its path decomposition, component count, and full-Hessian norm bound.
The separate [gadget proof](nonconvex-certificate-barrier.md) and
[exact checker](check_nonconvex_certificate_barrier.py) record 6,561 growth
checks and 400 arbitrary-grid witnesses, all passing.

The targeted command `python3 -` used `fractions.Fraction` and passed:

- 1,500 rational growth inequalities for one through five connected gadgets;
- 62 zero-valued component samples;
- five sharp-growth examples and running-intersection checks;
- 50 pairs of irregular coordinate grids satisfying the stated gap bound.

An additional inline `python3 - <<'PY'` check using exact fractions
verified Section 5's factorized identity on 100 rational points for chains
of one, two, three, and five gadgets. The algebraic expansion proves the
identity for every chain length; the check covers both endpoint and
internal degree coefficients.

These checks support the explicit identities; they do not establish a
general computational lower bound. No project-wide verification, CI
inspection, or external search was performed.
