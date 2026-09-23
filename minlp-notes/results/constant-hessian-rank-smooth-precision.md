# Constant Hessian rank gives the exact smooth scalar precision coefficient

Date: 2026-09-05. Status: independently reviewed; see
`notes/review-constant-hessian-rank-smooth-precision.md`.
Affine gradient fibers are established geometry. The proposed result is
the resulting mixed-integer graph precision law; priority is unestablished.

## Statement

Let `B` be a bounded closed full-dimensional box in `R^n`, and let `f`
be real `C^infinity` on an open neighborhood `U` of `B`. Suppose

```
rank ∇²f(x)=r    for every x in U.
```

Use the whole-graph, uniform vertical-error definitions of `p_conv`
and `p_bin` in `smooth-map-local-rank-integer-complexity.md`.

**Theorem.** As `ε` decreases to zero,

```
p_conv(ε)=p_bin(ε)=(r/2)log2(1/ε)+O_(f,B)(1),
```

meaning both minima have that asymptotic expansion. The upper bound is
a union of `O_(f,B)(ε^(-r/2))` bounded polyhedra, encoded using the
logarithm of that many binary codes. No formulation size polynomial in
`log(1/ε)` is claimed. The null space of the Hessian may vary with `x`. Formulation coefficients
may be arbitrary fixed real numbers; no preprocessing or coefficient
bit-complexity claim is made.
For `r=0`, `f` is affine on `B` and the exact graph needs no integers.

The lower bound is the independently reviewed local scalar rank bound
from `smooth-map-local-rank-integer-complexity.md`. The proof below
supplies the upper bound even when the global Hessian span has rank
larger than `r`.

## The established geometric ingredient

A scalar function whose Hessian has constant rank has locally affine
fibers of its gradient map. This is the scalar form of the relative
nullity foliation of its graph. It is stated, for example, in Nicola,
*Boundedness of Fourier integral operators on Fourier Lebesgue spaces
and affine fibrations*, Definition 1.1 and the paragraph following it,
printed page 3,
[open author manuscript](https://arxiv.org/pdf/0805.4122).
That paper also uses a half-scale decomposition transverse to affine
fibers in Fourier-integral estimates. The affine-fiber geometry and
that scale are not claimed new here. We give a local derivation to
make the linear formulation construction explicit.

## A partial Legendre coordinate chart

At any point, choose `r` coordinates `u` so the principal Hessian
`f_uu` is invertible; write the other coordinates as `v in R^(n-r)`.
For a symmetric matrix of rank `r`, such a principal minor exists.
After shrinking the neighborhood, the map

```
(u,v) -> (p,v),    p=f_u(u,v),
```

is a smooth diffeomorphism. Write its inverse as `(u(p,v),v)` and
restrict the parameter domain to an open product of boxes. Define the
local partial Legendre expression

```
g(p,v)=f(u(p,v),v)-p^T u(p,v).
```

This is a differential coordinate change; it does not require convexity
or a global maximizing definition of the Legendre transform. The usual
chain rule gives

```
g_p=-u,
g_v=f_v,
g_vv=f_vv-f_vu(f_uu)^(-1)f_uv.
```

The last matrix is the Hessian's Schur complement. Since the full
Hessian and its `uu` block both have rank `r`, it is zero. Therefore
on the product chart

```
g(p,v)=b(p)^T v+c(p),
u(p,v)=-Db(p)^T v-∇c(p).                                (1)
```

Here `b,c` are smooth. For each fixed `p`, (1) is affine in `v`, and

```
∇f(u(p,v),v)=(p,b(p)),
f(u(p,v),v)=p^T u(p,v)+b(p)^T v+c(p).                   (2)
```

Thus the same affine function

```
ell_p(u,v)=p^T u+b(p)^T v+c(p)
```

agrees with both `f` and its gradient along the entire local fiber.
The coordinate map is only used to select finitely many affine
functions and polyhedral cells; it is not imposed as a nonlinear
constraint in the final lift.

## Polyhedral tubes around fibers

Choose closed smaller parameter boxes `P_0,V_0` strictly inside the
open chart, and a slightly larger closed `P_1` inside that chart,
with `P_0` in its interior. Smoothness and compactness give constants
`L,M,η>0` such that:

- `||u(p,v)-u(p',v)||_infinity<=L||p-p'||_infinity` for
  `p,p' in P_1`, `v in V_0`.
- All points `(u(p,v)+delta,v)` with `p in P_1`, `v in V_0`,
  `||delta||_infinity<=η` lie in `U`, as do their segments from
  `(u(p,v),v)`.
- The Hessian norm of `f` is bounded on this compact neighborhood.

Replace `L` by a positive larger constant if needed. For small `h>0`,
cover `P_0` by `O(h^(-r))` parameter cubes of radius `h`, with centers
`p_nu in P_1`. Define the input polytope

```
C_nu(h)={(u,v):v in V_0,
                  ||u-u(p_nu,v)||_infinity<=Lh}.          (3)
```

This is a polytope because `u(p_nu,v)` is affine in `v`. Every point
in the image of `P_0 times V_0` lies in at least one such polytope,
by the Lipschitz bound.

For any `(u,v)` in (3), put `q=(u(p_nu,v),v)`. This point is on the
central fiber, so (2) says that `f-ell_(p_nu)` and its gradient vanish
at `q`. Taylor's theorem on the segment from `q` to `(u,v)` gives

```
|f(u,v)-ell_(p_nu)(u,v)|<=C h²                         (4)
```

with `C` independent of `h` and `nu`. The displacement has only `r`
coordinates, all of size at most `Lh`. Choosing `h<=η/L` ensures the
whole segment stays in the bounded-derivative neighborhood. Notice
that this estimate holds on the entire polytope (3), not just on
points whose gradient parameters belong to its parameter cube.

## Finite covering and binary encoding

The interiors of images of smaller parameter products cover `B`.
Compactness gives finitely many such charts. Take the maximum of their
error constants and the minimum of their valid small widths. Their
polyhedra (3), intersected with the original box, still cover `B` and
number `O(h^(-r))`. On each one impose the affine output band

```
|w-ell_(p_nu)(x)|<=ε/2.
```

Choose `h` proportional to `sqrt(ε)` so that (4) is at most `ε/2`.
Every exact graph point is contained, and every admitted point has
vertical error at most `ε`. The resulting finite union has
`O(ε^(-r/2))` bounded polyhedral members.

Use a distinct binary code for each member and its convex-hull
extended formulation. If the common code vector is integral, every
member with positive weight has the same code; distinctness leaves
one member. This is an exact union encoding with

```
p_bin<=ceil(log2(number of members))
      <=(r/2)log2(1/ε)+O_(f,B)(1).
```

Together with the local lower bound this proves the theorem. ∎

## Examples and limits

The Euclidean norm on `[1,2]^n` has constant Hessian rank `n-1`, so its
graph precision coefficient is `(n-1)/2`. Its Hessian null line rotates
with the input. In two dimensions, angular-sector approximations give
the same coefficient directly.

The positive-domain function `x²/t` has constant Hessian rank one,
so the coefficient is one half. A separate perspective construction
in `notes/perspective-integer-precision-investigation.md` can exploit
its rational structure for a compact upper bound; the present general
smooth theorem does not provide that compactness.

The theorem assumes constant rank on a neighborhood of the whole box.
It does not settle rank-changing singularities, nor does it claim that
the maximum pointwise Hessian rank alone always determines smooth
scalar precision. More generally, it does not establish a matching
upper bound from pointwise noncommutative rank for vector maps.
