# Affine repair and constraint multipliers for regridded certificates

Date: 2026-10-02. Status: mathematical exploration; the affine-retraction
argument has been checked independently. No literature or novelty claim.

The [regridded-certificate proof](../regridded-certificates/note.md) extends
to a useful class of affine coupling constraints. The extra structure is a
known affine feasibility repair that maps the domain box into itself.
Constraint multipliers determined by this repair remove the first-order
objective change. A Hoffman bound without those multipliers does not
suffice, even for a convex two-bag problem.

## 1. Why a repair bound is insufficient

The [two-bag obstruction](constraint-obstruction.md) gives a smooth
convex objective, two local affine equalities, exact local relaxations, feasible
quadratic growth, and a box-preserving projection with a fixed Hoffman
constant. Nevertheless, the unmodified gradient slopes give a first-order
certificate gap. Every feasible repair retains that lower-bound gap.
Using the missing constraint multiplier removes it. This motivates the
multiplier rule below.

## 2. A sufficient affine-retraction assumption

Let the domain be the box `X`, and let

```
P = {x in X : Ax=b}.
```

Assume `A` has full row rank. Assign each row of the equality system to a
bag containing its scope. Write the block assigned to bag `t` as
`A_t x_Vt=b_t`; `A` denotes the stack of these blocks after embedding
their columns in the full variable space. Each local convex oracle also
enforces its assigned equalities. The constrained certificate and dynamic
program treat empty states as described in Section 3 below.

Assume there is a known right inverse `K`, satisfying `AK=I`, such that

```
R(x) = x-K(Ax-b)
```

maps `X` into `X`. Then `R` is an affine retraction onto `{x:Ax=b}` and
is a feasible repair on the domain. It satisfies

```
L = I-KA,
d = Kb,
R(x) = Lx+d,
L^2=L,  Ld=0,
||R(x)-x||_2 <= ||K||_2 ||Ax-b||_2.
```

The right inverse is supplied as part of this promise; the theorem does
not find one preserving the box. For rational box data, `A`, `b`, and
`K`, both `AK=I` and box preservation are exactly checkable. The minimum
and maximum of each affine output coordinate over `X` follow directly
from the signs of its coefficients.

The repair need not be an orthogonal projection. Assume quadratic growth
only on `P`, while the smoothness and lower-model assumptions of the
regridding note hold on `X`.

At a feasible center `c`, compute the multipliers

```
mu(c) = -K^T grad F(c).                         (2.1)
```

They satisfy `A^T mu(c)=(L^T-I)grad F(c)`. Form subtree slopes using
the modified bag gradients

```
grad a_t(c_Vt) + A_t^T mu_t(c).
```

The added affine terms vanish at all locally feasible bag points, so the
per-factor relaxation rule and local objective values do not change.
Only the separator slopes change. Choose an initial feasible center by
applying `R` to any point of `X`. At every stage, repair the minimizing
configuration's top-copy representative `x` to `y=R(x)`, evaluate the
incumbent at `y`, and use `y` as the next center.

## 3. Empty states in constrained certificates

An exact constrained local oracle returns either a finite minimum and an
attaining locally feasible point, or a proof that its box/equality
intersection is empty. The latter is a linear-feasibility claim. The
certificate must explicitly support an infeasible separator-cell state;
it must not use `+infinity` as the intercept of a finite affine minorant.

The bottom-up construction propagates these flags as follows. For a bag
leaf, a child whose every intersecting separator cell is flagged
infeasible makes the leaf unusable. Otherwise take the minimum child
intercept only over unflagged intersecting cells. For each own
separator-cell/leaf pair, skip unusable leaves and query the oracle on
the equality-constrained intersection. A separator cell is flagged
infeasible only when every such pair is unusable or has a certified empty
intersection. Its proof records those local failures and references the
child infeasibility proofs already constructed.

These rules are valid by induction: any feasible subtree assignment
would select a containing local leaf and a containing child separator
cell at every child. That selection cannot encounter a correctly flagged
state or an empty local intersection. Thus a flagged separator cell
contains no feasible subtree assignment. False negatives are harmless:
a finite state may still include separator values with no extension.

The initial feasible point ensures a finite root configuration exists.
Every finite local minimum is attained because its feasible set is a
closed subset of a compact box, and its objective is continuous. There
are only finitely many leaf and cell choices. Hence the finite root
minimum is attained, and backtracking it returns locally feasible bag
copies and finite child states. Consistent configurations at every
globally feasible point remain available, in particular at `x*`, so
`LB<=f*` still holds.

Infeasibility flags do not add cells. Their verification uses only the
same bag/separator incidence lists and at most the same number of local
convex-oracle calls, where an infeasible return also counts as a call.
As in the original note, a box count is not a bit count for serialized
local optimization or infeasibility proofs.

## 4. Exact cancellation and aggregate drift

Use the regridding note's notation `Q`, `E`, `k`, `p=w+1`, and
`C0=k(k-1)p`. In this section distinguish

```
E_x = sum_t ||z^t-x_Vt||_2^2,
E_y = sum_t ||z^t-y_Vt||_2^2,
a = max_t ||A_t||_2,
chi = ||K||_2 a,
D = C0 (1+sqrt(k) chi)^2.
```

The ordinary aggregate copy bound still gives `E_x<=C0 Q`. Local
feasibility gives

```
||Ax-b||_2^2
  = sum_t ||A_t(x_Vt-z^t)||_2^2
 <= a^2 E_x.
```

Hence `||y-x||_2<=chi sqrt(E_x)`. Minkowski's inequality for the stacked
bag vectors and the occurrence bound give

```
sqrt(E_y) <= sqrt(E_x)+sqrt(k)||y-x||_2,
E_y <= D Q.                                      (3.1)
```

Let `Phi` be the original relaxed configuration value, with the modified
separator slopes. The telescoping identity gives exactly

```
Phi = F(y)
    + sum_t [a_t(z^t)-a_t(y_Vt)
             -grad a_t(c_Vt) dot (z^t-y_Vt)]
    - sum_t err_t.                              (3.2)
```

To check the linear cancellation, let the modified bag gradients be
`g_t=grad a_t(c_Vt)+A_t^T mu_t(c)`. Their global sum is
`L^T grad F(c)`. Equality feasibility at both `z^t` and `y_Vt` means
`g_t dot(z^t-y_Vt)=grad a_t(c_Vt) dot(z^t-y_Vt)`.
The difference between the sum of these linear terms and the separator
telescoping terms is

```
(L^T grad F(c)) dot (x-y)
  = grad F(c) dot L(x-R(x))
  = 0.
```

The last equality uses `L^2=L` and `Ld=0`. No stationarity of `c` or the
minimizer, multiplier bound, or orthogonality of the repair is needed.

Writing `r=||y-c||_2`, equation (3.2) gives

```
|F(y)-Phi|
 <= M sqrt(k) r sqrt(E_y) + (M/2)E_y + (A0/4)Q
 <= M sqrt(kD) r sqrt(Q) + (MD/2+A0/4)Q.          (3.3)
```

Shell grading around `c` likewise gives

```
Q <= 6N h^2 + 3(2k-1) theta^2 r^2
                 + 6 theta^2 E_y.
```

Here bag and separator copy-error sums are at most `2E_y`; they need not
be exactly `2E_y`, since repaired private coordinates may change. Under
`12D theta^2<=1`, absorb the last term to obtain

```
Q <= 12N h^2 + 12k theta^2 r^2.                  (3.4)
```

Equations (3.3) and (3.4) are precisely the two inequalities needed in the
original aggregate-contraction proof, with `C0` replaced by `D`.
Consequently all its displayed choices of `B0`, `eta`, `C`, `B`, and
`theta` remain valid after that replacement. The feasible iterates obey

```
||y_j-x*||_2^2 <= ||y_(j-1)-x*||_2^2/9
                  + (10C/(9g))N h_j^2,
UBD-LB_j <= g B N h_j^2.
```

For fixed `k,w,M/g,A0/g,chi`, the final certificate size is
`O(N(4/theta)^p(J+1))`, the total number of created boxes is
`O(N(4/theta)^p(J+1)^2)`, and the number of local convex-oracle calls is
`O(N 3^p(4/theta)^p(J+1)^3)`, with the same logarithmic stopping-stage
bound as in the regridding note. Empty constrained pairs can be skipped
and cannot increase the incidence count.

These are certificate and local-oracle counts. In addition, every stage
requires applying the global repair and applying `K^T` to a gradient to
obtain the multipliers in (2.1). General dense
systems can make those operations expensive. No claim that the whole
algorithm uses only bounded-dimensional oracles, or any bit-complexity
claim, follows merely from this theorem.

## 5. A concrete class: stable linear state dynamics

Let `T>=1`, with states `s_0,...,s_T` and controls `u_0,...,u_(T-1)`, all
in `[-1,1]`. Impose

```
s_(t+1) = a s_t + b u_t,
|a|+|b| <= 1,
|a| < 1.
```

Use path bags `{s_t,u_t,s_(t+1)}`. Then `p=3`, `w=2`, and `k<=2`,
independently of the horizon. Each equality has exactly one bag.

The affine repair leaves `s_0` and all controls fixed and recomputes the
states by forward simulation. It preserves the box by the displayed
coefficient condition and fixes every feasible trajectory. If

```
r_t = s_(t+1)-a s_t-b u_t,
e_t = R(s,u)_(s_t)-s_t,
```

then `e_0=0` and `e_(t+1)=a e_t-r_t`. The finite geometric convolution
has Euclidean operator norm at most `1/(1-|a|)`. Thus

```
||K||_2 <= 1/(1-|a|),
max_t ||A_t||_2 = sqrt(1+a^2+b^2),
chi <= sqrt(1+a^2+b^2)/(1-|a|).
```

These constants are independent of `T`. Repair, transpose application,
and multipliers can all be computed by forward or backward recurrences,
in `O(T)` arithmetic per stage. More explicitly, if `g` is the global
objective gradient, the multiplier recurrence is

```
mu_(T-1) = -g_(s_T),
mu_(t-1) = a mu_t-g_(s_t)       (t=T-1,...,1).
```

It makes every adjusted intermediate and final state derivative zero.
The remaining adjusted derivatives on `s_0` and the controls are exactly
`L^T g`, as required by (2.1).

For a concrete nonconvex objective with uniform constants, take
`a=b=1/2` and

```
F(s,u) = s_0^2
       + sum_(t=0)^(T-1) [s_(t+1)^2+u_t^2-u_t^4/4].
```

Assign `s_0^2` to the first bag. Then `F(x)>=3||x||_2^2/4` on the whole
box, so its feasible optimum is uniquely zero with `g=3/4`. Bag
gradients have Lipschitz constant `M=2`. The unary control factors are
nonconvex near the domain endpoints. Standard alphaBB parameter `1/2`
convexifies them and gives `A0=1/2`: one relaxed unary factor per bag,
with all quadratic factors kept exact. The
repair has `||K||_2<=2`, `chi<=sqrt(6)`, and every constant in the theorem is
independent of the horizon.

The constrained objective itself is nonconvex. Vary only the final
control, keeping preceding controls and states fixed and changing
`s_T` by `b` times the control change. This is a feasible direction with
second derivative

```
2(1+b^2)-3u_(T-1)^2 = 2.5-3u_(T-1)^2.
```

It is negative when `|u_(T-1)|>sqrt(5/6)`. Such trajectories exist away
from the final-state box boundary, for example with preceding states
and controls zero. At `u_(T-1)=15/16`, the final state is `15/32` and
the displayed second derivative is exactly `-35/256`.

The theorem permits arbitrary stage factors meeting the same smoothness,
relaxation, and feasible quadratic-growth assumptions. Eliminating the
states substitutes increasingly long affine combinations of the controls
into later stage factors and generally destroys the original small
factor scopes. The local constrained formulation retains those scopes.

## 6. What remains outside this argument

A general Hoffman repair for `Ax=b` intersected with a box is usually
piecewise affine, rather than one affine retraction preserving the box.
The cancellation in (3.2) requires one linear part that works for all
configurations at the stage. A derivative or active set for the repair
at the center alone does not supply that identity.

For inequalities, nonnegative multipliers introduce terms involving
their slack at the repaired point and at the local copies. A bound on
repair distance does not control those first-order terms. Converting
inequalities to equalities with box-constrained slack variables does not
automatically supply a box-preserving affine retraction. Thus the result
above is a concrete sufficient class, not a general polyhedral extension.

## 7. Checks performed

The affine-retraction algebra, drift estimate, and dynamics
specialization were checked independently by a delegated reviewer. Its
inline numerical checks passed 160 dynamics cases, including negative
`a`, checking box preservation, the repair bound, the multiplier identity,
and the linear cancellation. The largest multiplier-identity residual
was `7.03e-16`. These checks support the algebra and do not implement the
constrained certificate algorithm.

Another fresh adversarial reviewer passed 300 exact-rational
configuration-identity and repair-bound checks and found no mathematical
blocker. Its requested clarifications about the occurrence bound and the
oracle's certified infeasibility returns are included above.

The parent research agent also ran the targeted command

```
python research-20261002/new-direction/check_affine_repair.py
```

It passed 24 explicit dynamics-matrix checks at horizons
`1,2,3,8,16,32`, with coefficient pairs
`(0.5,0.5),(-0.5,0.5),(0.8,-0.2),(0,0.7)`. These checked `AK=I`,
retraction idempotence, the row absolute-sum bound ensuring whole-box
preservation, the operator-norm bound on `K`, and normal cancellation.
Another 240 valid configurations with locally feasible copies and the
quartic objective checked the corrected-slope telescoping identity,
repair and aggregate-drift bounds, and the error bound. The largest
telescoping residual was `7.11e-15`. The artifacts are
[check_affine_repair.py](check_affine_repair.py) and
[check_affine_repair.json](check_affine_repair.json).

No project-wide verification, CI inspection, literature search, or
implementation of the constrained regridding algorithm was performed.
