# A bag min-marginal obstruction for stable scalar dynamics

Date: 2026-10-02. Status: scoped exploration with explicit counterexamples.
No algorithmic lower bound or literature claim.

The independent ambient-noise argument for
[sparse box QPs](../new-direction/sparse-bag-cell-smoothed-qp.md) does not
extend to the [stable scalar dynamics model](../new-direction/nonlinear-dynamics.md)
by retaining its conditional bag semiconcavity and endpoint-rounding
lemmas. Both lemmas can fail for rational quadratic dynamics, fixed
derivative bounds, and a horizon of two. Independence of the noise inside
a bag survives conditioning; a finite upper-curvature bound for the
conditional objective does not.

## 1. A two-stage inverse-square obstruction

Take three state intervals `I_0=I_1=I_2=[0,1]`, two control intervals
`U_0=U_1=[-1,1]`, and

```
s_1 = phi_0(s_0,u_0) = u_0^2,
s_2 = phi_1(s_1,u_1) = u_1^2.
```

These maps preserve the stated boxes and satisfy the uniform bounds

```
|partial_s phi_t| = 0,
|partial_u phi_t| <= 2,
||Hess phi_t||_2 = 2.
```

There are no constraints besides these equalities and intervals. The
bags are `B_0={s_0,u_0,s_1}` and `B_1={s_1,u_1,s_2}`. Start with the
ambient linear objective

```
F_gamma = gamma_s0 s_0 + gamma_u0 u_0 + gamma_s1 s_1
          + gamma_u1 u_1 + gamma_s2 s_2,
```

where all five coefficients are independent draws from the same noise
law. Condition on the two coefficients outside `B_1`. For every `y` in
`[0,1]`, the bag point `(s_1,u_1,s_2)=(y,0,0)` is feasible. Its exact
min-marginal is

```
V_gamma(y,0,0) = C_gamma + gamma_s1 y - |gamma_u0| sqrt(y),
C_gamma = min(0,gamma_s0).
```

Indeed, the outside fiber has `u_0` equal to either square root of `y`,
and `s_0` is free in `[0,1]`. The term produced by the outside coefficient
is part of the conditioned function; it cannot be absorbed into the
remaining independent linear noise on the bag.

Write `c=|gamma_u0|`. For `0<h<=1/2`, the three points with `y=0,h,2h`
lie on a feasible coordinate segment. Their second difference is

```
V_gamma(0,0,0) + V_gamma(2h,0,0) - 2 V_gamma(h,0,0)
  = c (2-sqrt(2)) sqrt(h).
```

An upper-curvature constant `L` in the `s_1` coordinate would require
this difference to be at most `L h^2`. The ratio is

```
c (2-sqrt(2)) h^(-3/2),
```

which diverges whenever `c>0`. Equivalently, at every `y>0` the nonlinear
term has second derivative `c/(4 y^(3/2))`. Thus no finite uniform upper
coordinate-curvature bound exists, even after conditioning on all noise
outside the bag and even along a feasible coordinate segment. Extending
the min-marginal by `+infinity` away from its feasible bag projection
does not repair this failure.

For continuous uniform noise this event has probability one. For the
common rational endpoint law

```
gamma_i in {-sigma + 2 sigma k/(M-1): k=0,...,M-1},
sigma>0, M a power of two, M>=2,
```

zero is absent: it would require `2k=M-1`, whose right side is odd.
Consequently, the obstruction holds on **every draw** from that law.
This conclusion does not concern rare bad conditioning draws.

## 2. Uniform quadratic growth does not remove the obstruction

Keep the same dynamics and add the base objective

```
F_0 = s_0^2 + u_0^2 + s_1^2 + u_1^2 + s_2^2.
```

Let `0<sigma<=1/2`. Parameterize feasible trajectories by
`z=(s_0,u_0,u_1)` in the product box `[0,1] x [-1,1]^2`. The reduced
perturbed objective is

```
f_gamma(z) = s_0^2 + gamma_s0 s_0
  + (1+gamma_s1)u_0^2 + u_0^4 + gamma_u0 u_0
  + (1+gamma_s2)u_1^2 + u_1^4 + gamma_u1 u_1.
```

Its Hessian is at least the identity for every draw. Convex-box
first-order optimality therefore gives a unique minimizer `z*` and
`f_gamma(z)-f_gamma(z*) >= ||z-z*||_2^2/2`, including when the minimum
is on the boundary. The feasible embedding

```
E(s_0,u_0,u_1) = (s_0,u_0,u_0^2,u_1,u_1^2)
```

satisfies `||E(z)-E(z*)||_2^2 <= 5 ||z-z*||_2^2`. Hence the original
ambient objective has feasible quadratic growth with the uniform
constant `g=1/10`. Its ambient Hessian is `2I`, and its state derivatives
are uniformly bounded by `5/2`. All these constants are independent of
the draw.

Nevertheless, the same conditional slice has min-marginal

```
V_gamma(y,0,0) = C_gamma + (1+gamma_s1)y + y^2
                - |gamma_u0| sqrt(y),
```

where now `C_gamma=min_{s_0 in [0,1]}(s_0^2+gamma_s0 s_0)`. Its second
difference divided by `h^2` is
`2+|gamma_u0|(2-sqrt(2))h^(-3/2)`. The failure is therefore compatible
with the deterministic dynamics certificate's smoothness, stability,
box invariance, and uniform feasible-growth assumptions.

The use of reset dynamics is not essential to the local obstruction.
With all state and control intervals equal to `[-1,1]`, take

```
phi_0(s,u) = (s^2+u^2)/4,
phi_1(s,u) = s u/4.
```

Both maps depend on both inputs, preserve the boxes, and satisfy
`a=b=H=1/2`. Along the feasible coordinate segment `(s_1,u_1,s_2)=(y,0,0)`
for `0<=y<=1/4`, the preceding fiber is a circle of radius `2 sqrt(y)`
contained in `[-1,1]^2`. Its minimum ambient linear cost is
`-2 sqrt(gamma_s0^2+gamma_u0^2) sqrt(y)`. The same obstruction follows.

## 3. Exact feasible endpoint rounding also fails

For `s_next=u^2`, a product grid cell may meet the true graph while
having no feasible corner. On a dyadic mesh of width `1/4`, consider

```
u in [1/2,3/4],       s_next in [1/2,3/4].
```

The graph meets this cell, for example at
`(u,s_next)=(23/32,529/1024)`. At its control endpoints, the graph states
are `1/4` and `9/16`, neither of which is a state endpoint of this cell.
Every corner is therefore infeasible. A free initial-state coordinate
does not change that fact. Mean-preserving rounding to corners of the
containing product cell has no feasible support.

There is also a quantitative failure of a mesh-squared grid correction.
Use a one-stage instance with `u in [-1,1]`, `s_next in [0,1]`,
`s_next=u^2`, and objective `(u-1/3)^2`. Its true minimum is zero. On
the common ambient endpoint mesh `h=2^(-2m)`, `m>=1`, exact feasible
grid points satisfy

```
u=k/2^(2m),       u^2=ell/2^(2m),
k^2=ell 2^(2m).
```

Thus `k` must be divisible by `2^m`, and the feasible control values are
exactly the multiples of `2^(-m)` in `[-1,1]`. Their distance from `1/3`
is at least `2^(-m)/3`, with equality attained. The exact feasible grid
minimum is therefore

```
min_grid (u-1/3)^2 = 2^(-2m)/9 = h/9.
```

No fixed multiple of `h^2` bounds this discretization error. The base
objective has constant upper curvature two. This example concerns the
exact dynamics on the ambient endpoint grid; graph strips, forward
repair, or a different choice of grid require their own proof.

## 4. What this does and does not exclude

The feasible set in this model is the continuous image of the connected
product domain for `(s_0,u_0,...,u_(T-1))`. It is connected, as is every
coordinate projection. A disconnected entire bag projection is therefore
not an available obstruction under box invariance and the absence of
additional constraints. Fixed-bag predecessor fibers can still be
disconnected, as the two square roots above show.

Eliminating states avoids inverse predecessor fibers, but in general
does not preserve bounded treewidth of the reduced primal graph. For example, the
stable box-invariant maps

```
s_(t+1)=s_t/2+u_t^2/4,       s_t in [0,1], u_t in [-1,1]
```

give

```
s_T = 2^(-T)s_0 + (1/4) sum_(j=0)^(T-1) 2^(-(T-1-j)) u_j^2.
```

The allowed terminal cost `s_T^2` then has a nonzero mixed monomial
`u_i^2 u_j^2` for every distinct pair of controls. Its ordinary reduced
primal graph contains a clique of size `T`; exponential coefficient
decay does not remove these exact dependencies. This is an example of
lost sparsity, not a claim that every dynamics instance loses sparsity
or that no specialized reduced representation is possible. The reset
maps in Section 1 themselves retain short memory. A bounded reset
interval or another proved finite-memory structure can avoid this
particular growth of reduced treewidth. Expanding the square still gives
factors involving at most two controls; their complete interaction graph
is the source of the large required bags.

These examples block a direct use of the box theorem's conditional
semiconcavity and feasible endpoint-rounding steps. They do not rule out
a different smoothed dynamics theorem, exact cell closure, or the
existing strip-and-repair certificate. Any replacement argument must
handle the changing predecessor fibers and exact dynamics explicitly.

## 5. Targeted verification

The formulas above are proved directly. A scoped exact-rational Python
check verified the infeasible cell corners, the displayed feasible
interior point, the exact feasible-grid characterization and value
`h/9` for `m=1,...,5`, the absence of zero in endpoint noise grids
of sizes `2,4,8,16`, and 20 rational interior midpoint witnesses to the
square-root curvature failure. An independent mathematical review found
no blocker.

Commands actually run:

- `python -` with the inline exact-rational checks described above: passed.
- `python -` with a scoped trailing-whitespace and final-newline check:
  passed.
- `git diff --no-index --check /dev/null research-20261002/reviews/stable-dynamics-bag-obstruction.md`:
  no whitespace diagnostics; exit status one records the new file.

No project-wide verification or CI inspection was performed.
