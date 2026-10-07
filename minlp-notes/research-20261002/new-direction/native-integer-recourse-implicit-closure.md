# Optional implicit closure for native integer recourse

Date: 2026-10-02. Status: passed
[independent review](../reviews/smoothed-native-integer-recourse-review.md).
This is the sharper core-processing alternative to the
[expanded algebraic-output theorem](smoothed-native-integer-recourse.md).
Its nonlinear closure was independently reviewed before the main theorem
was simplified to use an exact algebraic solve of the entire core slice.

Use precisely the main theorem's input, exact oracle, core search, and
competing-label certificate. Retain its notation `k,L,G,D_j,c_j,z_j,e_j`.
Instead of paying the additional parameter-only algebraic factor `A_d(k)`,
one can return a compact convex core patch with expected work

```
8^k [3+(1+k/2)L/(2sigma)]^k poly_d(I).                       (1)
```

The ordinary branch's descriptor has polynomial length and admits
`poly_d(I+t)`-time feasible point/value evaluation. The fallback remains
the main theorem's same-draw algebraic enumeration; only its expected work
and evaluation guarantee is used in this sharper bound. The proof trace
has expected size (1). The stronger explicit-output contract in the main
theorem is available by paying its additional `A_d(k)` factor.

## 1. Sound nonlinear closure

After the competing-label certificate passes, every original optimum lies
in `D times {z}`. Let `f(v)=F_gamma(v,z)`. Compute uniform rational bounds
on the original real bounding box

```
M_1>=max{1,max_(i in C) sum_(j in C) sup |partial_ij F_0|},
T>=max{1,max_(i in C) sum_(j,l in C) sup |partial_ijl F_0|}.
```

At a core patch midpoint `m`, with largest half-width `r_Q`, fix a coordinate
at its original lower bound when that bound lies in its interval and
`partial_i f(m)-M_1 r_Q>0`. Use the negative-gradient counterpart at an
original upper bound. These whole-patch sign certificates preserve every
global optimizer. No derivative test is used on an integer coordinate.

After substitution, check by rational linear algebra that

```
Hess_(J_f) f(m)-(T r_Q+g_0)I is positive definite.           (2)
```

This certifies Hessian modulus `g_0` on the remaining box, whose unique
constrained minimizer is an exact global optimizer. If no coordinate
remains, return the verified point. The [convex-patch evaluator](convex-patch-evaluation.md)
supplies feasible rational approximants and objective enclosures; the
integer label stays exact.

## 2. Cutoff and finite law

For stopping analysis, suppose full point growth is at least `g_0`, and
each active core-bound gradient has magnitude greater than `tau`. Put
`A_0=2+kL/g_0`. The main retained-witness proof gives
`D_j` within core infinity radius `A_0 h_j` of the optimum and
`||(c_j,z_j)-a||^2<=e_j/g_0`. A sufficient cutoff is

```
h_j<=min{1/(4A_0), g_0/(16GA_0),
         tau/(8M_1 A_0), g_0/(4T A_0)}.                    (3)
```

The first two inequalities are the main label-identification cutoff.
Once its certificate passes, the midpoint gradient error and patch-radius
error sum to at most `2M_1 A_0h_j<tau/2`. All active core coordinates are
therefore fixed. A free coordinate cannot pass a strict sign test because
its gradient vanishes at the contained optimizer. On the remaining free
face, growth gives Hessian at least `2g_0 I` at the optimizer. Its two
variation costs total at most `2T A_0h_j<=g_0/2`, proving (2).

In addition to the main growth tail, use the active-core-gradient tail

```
K=max{1,k 3^k R_Z max(1,d-1)^k},
Pr{g_*>0 and some active core gradient has magnitude<=tau}
       <=K(tau/sigma+1/M).
```

Fix each candidate integer label and core face for a union bound, then
condition on all noise except the tested active core coefficient. Positive
growth makes free stationary roots nonsingular; there are at most
`max(1,d-1)^k` per face. The active gradient changes with slope one in the
unconditioned noise. This is the [established finite-grid argument](polynomial-finite-noise-tails.md);
it does not condition on the optimizer-selected label.

With the main base fallback budget `B`, choose

```
rho=1/(4B),   g_0=rho sigma/(2S),   tau=rho sigma/(2K).
```

Let `J` satisfy (3), and choose the least power of two

```
M>=max{2,2^J,4n C_tail/rho,2K/rho}.
```

The growth and active-gradient failure events each cost at most `rho`.
The same-draw fallback then has polynomial expected work. All precisions
are base-only with polynomial binary length. The usual branch uses only
polynomial-time derivative, matrix and convex-evaluation work after the
core queries, which proves (1).

## 3. Verification

The [native recourse review](../reviews/smoothed-native-integer-recourse-review.md)
checked this original nonlinear closure, its cutoff, active-gradient union,
finite-law budgets, and evaluation contract. The revised main theorem
does not need these active-gradient or Hessian steps.

The author's command

```sh
python3 -B research-20261002/new-direction/check_native_integer_recourse.py
```

checks this implicit variant on a coupled two-arc flow with nonconvex
quartic core. Capacity `7` closed at level 11 after 53 generated cells and
118 exact flow calls; capacity `2^80+7` closed at level 86 after 409 cells
and 849 calls. Both retained at most four cells per level. All 967 calls
passed rational residual-potential checks and both tied-label guards
prevented premature exclusion. The fixture oracle solves its scalar
quadratic flow problem directly; no capacity enumeration, general flow
algorithm, full finite-law experiment or algebraic fallback was tested.
