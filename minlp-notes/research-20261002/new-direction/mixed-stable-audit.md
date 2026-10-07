# Independent audit: finite controls in stable scalar dynamics

Date: 2026-10-02. Verdict: the private-control mixed extension is valid
under the assumptions below. This is a proof audit, not a literature or
novelty assessment. A second independent delegated audit found no
blocking issue.

The affine repair and multiplier argument in
[affine-repair-exploration.md](affine-repair-exploration.md) remains valid
for the dynamics

```
s_(t+1) = a s_t + b u_t,
|a|+|b| <= 1,  |a| < 1,
s_t in [-1,1],  u_t in U,
```

where `U` is a nonempty, explicitly enumerated finite subset of `[-1,1]`.
Use chronological path bags `{s_t,u_t,s_(t+1)}`. Each control belongs to
one bag. Only the two state coordinates are meshed; each bag cell also
specifies one exact control value. Separators contain only states.

## Assumptions that must carry over

Each bag objective has a continuously differentiable extension to its
full three-coordinate box, with gradient Lipschitz constant at most `M`.
The models on a fixed-control cell are continuous and convex in the
remaining state variables and have error at most `A0 width(B)^2/4`.
Here `width(B)` measures the continuous state cell. An attaining convex
oracle solves the local dynamics slice, or reports it empty.

The unique mixed feasible minimizer `x*` satisfies

```
F(x)-F(x*) >= g ||x-x*||_2^2,  g>0,
```

for every mixed feasible `x`, with the norm including both states and
controls. These are uniform assumptions across control assignments.
Bag-level smoothness cannot be replaced by a bound only on the summed
objective: cancellation among bag derivatives can hide large individual
constants. Likewise, quadratic growth separately within each control
assignment does not imply the displayed assumption.

## Feasibility and exact cancellation

Every configuration selects one admissible value of each private
control. Its top-copy representative `x` therefore already has admissible
discrete controls. Forward simulation retains `s_0` and all controls and gives a
feasible point `y=R(x)`. The coefficient condition preserves the state
box. An initial feasible center is obtained by choosing any `s_0` and
any admissible controls and simulating forward.

The same affine map `R(x)=Lx` exists on the continuous ambient box,
whether or not the selected controls are discrete. At a mixed feasible
center `c`, let `g_c` be the gradient of the supplied continuous
extension. Solve

```
A^T mu = (L^T-I)g_c
```

and form separator slopes from the modified bag gradients
`grad a_t(c_Vt)+A_t^T mu_t`. These gradients need not be derivatives
of a discrete value function. For the scalar dynamics the backward
recurrence in the affine-repair note computes the required multipliers.

Both `z^t` and `y_Vt` satisfy the bag dynamics with the selected control,
so multiplier terms vanish in their difference. The remaining global
linear term is

```
(L^T g_c) dot (x-y) = g_c dot L(x-Lx) = 0.
```

Consequently the exact identity from the continuous proof still holds:

```
Phi = F(y)
    + sum_t [a_t(z^t)-a_t(y_Vt)
             -grad a_t(c_Vt) dot (z^t-y_Vt)]
    - sum_t err_t.
```

No equality between the selected controls and the center controls was
used. Instead, full ambient smoothness gives

```
|T_t| <= M ||y_Vt-c_Vt||_2 ||z^t-y_Vt||_2
          + (M/2)||z^t-y_Vt||_2^2.
```

The second norm has zero control component; the first includes control
changes. A state-only first norm is invalid: `a_t(s,u)=Kus` has zero
state Hessian but its state gradient changes by `K(u-c_u)`.

## Direct repair bound and contraction

A sharper bound than the general affine-retraction estimate is available.
Put

```
delta_t = z^t_(s_t)-y_(s_t),
jump_t = z^t_(s_t)-z^(t-1)_(s_t)       (t>=1).
```

Then `delta_0=0`, `delta_t=jump_t+a delta_(t-1)`, and the successor-state
error in bag `t` is `a delta_t`. Finite geometric convolution therefore
gives, for the total bag error `E_y`,

```
E_y = (1+a^2) sum_t delta_t^2
    <= (1+a^2)/(1-|a|)^2 sum_(t>=1) jump_t^2
    <= D Q,
D = 2(1+a^2)/(1-|a|)^2.
```

The last inequality uses `|jump_t|<=width(B_(t-1))+width(D_t)`.
Each parent bag width appears once in this path sum. Here `Q` is the
sum of squared selected state-cell widths over bags and separators.

With `r=||y-c||_2`, including controls, shell grading gives exactly the
inequalities needed in the aggregate proof:

```
Q <= 12N h^2 + 12k theta^2 r^2,
|F(y)-Phi| <= M sqrt(kD) r sqrt(Q) + (MD/2+A0/4)Q,
```

provided `12D theta^2<=1`; here `k=2`. State distances in the grading
estimate are bounded by the full ambient distance, and controls have no
copy error. Thus every constant and contraction inequality in the
regridding note applies with `C0` replaced by `D`. In particular,

```
||y_j-x*||^2 <= ||y_(j-1)-x*||^2/9
                 + (10C/(9g))N h_j^2,
UBD-LB_j <= g B N h_j^2.
```

A consistent configuration at `x*` still proves `LB_j<=F(x*)`, since
its exact controls appear in the enumeration. Every minimizing
configuration obeys the estimate, including ties and configurations
that switch controls. The initial diameter bound remains valid with
`p=3` and `h_0=2`: there are `2N+1<=3N` global coordinates, each of
diameter at most two.

## Counts and limits

Let `q=|U|`, `m=4/theta`, and let `J` be the stopping-stage bound from
the regridding note. Each continuous bag partition is replicated for
its `q` control values. State separators require no such replication.
The counts are therefore

```
final leaves and separator cells: O(q N m^2 (J+1)),
total created leaves and cells:   O(q N m^2 (J+1)^2),
exact local convex-oracle calls:  O(q N m^2 (J+1)^3).
```

The shell-incidence factor is three because a separator has one state
coordinate. The continuous grid exponent is two, although the ambient
bag dimension used for diameter and multiplicity bounds remains three.
For a fixed number of private controls per bag, explicit enumeration
instead costs the product of their alphabet sizes. No claim about
discrete separators or unrestricted mixed problems follows here.

Horizon-independent conditioning requires `1-|a|` bounded away from
zero, as well as uniform `M/g` and `A0/g`. Small terminal-target costs
that distinguish exponentially close encoded trajectories do not give
an immediate hardness contradiction: their ambient quadratic-growth
constant can decrease exponentially. The result also retains the exact
oracle model and makes no bit-complexity claim.

Additional endpoint or path constraints require a separate proof that
repair preserves them. Exact identification of the optimal control
sequence requires a tolerance below a threshold involving alphabet
separation; objective-gap certification does not.

No numerical tests, project-wide verification, CI inspection, or
literature search were performed for this audit. The conclusions above
follow from the displayed algebra and the existing shell-incidence
proof.
