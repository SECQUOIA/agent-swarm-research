# Residual-convex cubics: fixed face kernels and a remaining point-output gap

Date: 2026-10-02. Status: completed structural claims, passed a
[fresh independent actual-file review](../reviews/residual-convex-cubic-boundary-review.md).
This closes the present exploration. It proves neither a full
point-oracle extension nor an obstruction to every such extension.

The positive [cubic full-point theorem](cubic-core-full-point-oracle.md) assumes
a supplied quadratic convexifier in the core variables. Here we retain only
convexity of every residual fiber. The examples below show why its uniform
error bound and a naive approximate-core substitution do not transfer directly.
The underlying fixed-kernel and Hoffman arguments are adaptations of the
reviewed [convex cubic point theorem](convex-cubic-point-oracle.md), not new
general error-bound principles.

## 1. Setup and a fixed kernel on each core face

Let `F(v,z)` be an explicitly represented rational polynomial of total degree
at most three, with `v in [0,1]^k` and `z in [0,1]^n`, `n>=1`. Suppose
`z -> F(v,z)` is convex for every core `v`. Positive-width rational boxes can
be normalized this way; fixed coordinates are substituted. Let `I` include
the polynomial and box encoding. Convexity is a promise, not a recognition
claim.

The residual Hessian

```
H(v,z) = nabla_zz^2 F(v,z)
```

is affine in all its arguments and positive semidefinite throughout the
product. Fix a face `A` of the core cube. Let `c_A` be its relative center,
let `c_z=(1/2,...,1/2)`, and set

```
H_A = H(c_A,c_z),       K_A = ker H_A.
```

Reflection about the relative center preserves `A x [0,1]^n`, so affinity
gives, for every `(v,z)` in that product,

```
H(v,z) + H(2c_A-v,1-z) = 2H_A,
0 <= H(v,z) <= 2H_A.                                  (1)
```

In particular `K_A` lies in every residual Hessian kernel on this face.
Suppose each free coordinate of `v` lies in `[delta,1-delta]`, where
`0<delta<=1/2`. For `delta<1/2`, write
`v=2delta c_A+(1-2delta)w` with `w in A`. Then

```
H(v,c_z) >= 2delta H_A.                                (2)
```

For `delta=1/2`, the same statement follows from `v=c_A`. A zero-dimensional
face satisfies (2) as well. Equations (1)--(2) show

```
ker H(v,c_z) = K_A       for v in relint A.             (3)
```

The kernel is therefore rational and constant on the relative interior of
each core face. Its dimension can increase at the boundary of that face.
If `lambda_A` is the smallest positive eigenvalue of nonzero `H_A`, the
smallest positive eigenvalue of `H(v,c_z)` is at least
`2delta lambda_A`.

## 2. The residual optimizer slice has only one varying row

Define the vector polynomial

```
g_A(v) = nabla_z F(v,c_z).
```

Its degree in `v` is at most two. For a fixed `v in relint A`, let `y` be
any minimizer of its residual fiber. The optimizer-slice identity from the
convex cubic theorem, followed by (3), gives

```
S_v = argmin_(z in [0,1]^n) F(v,z)
    = {z in [0,1]^n:
         H_A(z-y)=0,  g_A(v)'(z-y)=0}.                 (4)
```

This includes affine fibers, for which `H_A=0`, and nonunique optimizer
sets. The right-hand sides may be irrational. Only one row of the equality
matrix depends on the core.

Consider all square minors of

```
B_A(v) = [ H_A ; g_A(v)' ; I_n ].                      (5)
```

Signs of active box normals do not affect the absolute values of these
minors. A minor not using the `g_A` row is constant. A minor using it is
linear in that row, so every minor is a polynomial of degree at most two
in `v`. There are at most `2^(3n+1)` row/column selections. Each minor has
rational coefficients of polynomial binary length in `I`: a determinant
uses at most `n!` terms, and only one factor in each term can depend on `v`.
Thus the family has a polynomial logarithmic size and bounded degree.
This does not give permission to enumerate the family in polynomial time.

## 3. A conditional polynomial-bit error bound

Here is the precise consequence of controlling those minors. Suppose
`delta` satisfies the condition in Section 1, and a rational `0<mu<=1`
is a lower bound on the absolute value of every minor of (5) which is
nonzero at this particular `v`. Minors vanishing at `v` are allowed.
Replace each supplied margin by a dyadic lower bound within a factor of
two, and reuse `delta,mu` for these bounds. This preserves the assumptions
and gives margin encodings of length `O(1+log(1/delta)+log(1/mu))`, even
if the originally supplied rational encodings were unnecessarily long.
Choose a rational `C>=1` bounding all entries of (5) on `A`; a coefficient
sum bound suffices and has polynomial binary length. Put

```
H_* = (nC)^(n-1)/mu.
```

Every independent stack `R` of equality rows and active box normals has
a nonzero square column minor of absolute value at least `mu`.
Cauchy--Binet and `||R||_2<=nC` therefore give

```
sigma_min(R) >= mu/(nC)^(n-1).
```

The projection proof of the Hoffman bound in the predecessor then gives

```
dist_2(z,S_v)
 <= H_* ||[H_A; g_A(v)'](z-y)||_2.                    (6)
```

The proof allows arbitrary real equality right-hand sides and coefficients;
the supplied minor bound replaces the predecessor's integer determinant
bound.

For clarity, explicit conservative constants finish the argument. Set
`M=max(1,max_i sum_j |(H_A)_ij|)` and `M_*=2M`. If `H_A` has positive
rank, let `D>=1` clear its denominators and put

```
lambda_0 = D^(-n) M^(-(n-1)),
lambda_* = 2delta lambda_0,
R_0 = max(1,96 M_* n/lambda_*^2),
Gamma = H_* [1+(M+2M_* n)R_0].                       (7)
```

The rational number `lambda_0` bounds `lambda_A` from below by the
principal-minor argument in the predecessor. For
`E=F(v,z)-min_w F(v,w)` with `0<=E<=1`, its cubic transverse estimate
implies

```
||P_(K_A^perp)(z-y)||_2 <= R_0 E^(1/4).
```

Its affine-row estimate also gives
`|g_A(v)'(z-y)| <= E+2M_* sqrt(n)||P_(K_A^perp)(z-y)||_2`.
Together with `||H_A||_2<=M` and (6), these prove

```
dist_2(z,S_v) <= Gamma E^(1/4).                       (8)
```

If `H_A=0`, each residual fiber on `A` is affine. Then (6) directly
gives (8) with `Gamma=H_*`, since the affine equality residual is `E`.
All constants in (7)--(8) have binary length polynomial in
`I+log(1/delta)+log(1/mu)`. This is a conditional bound. It is not an
algorithm to find or certify suitable margins at an unknown optimal core.

## 4. Two direct obstructions to naive transfers

First take

```
F(v,z)=v z^2,       (v,z) in [0,1]^2.                 (9)
```

Every residual fiber is convex. For `v>0`, its unique optimizer is `z=0`;
at `z=1`, the distance to the optimizer is one while the objective gap
is `v`. Hence no finite constant `Gamma` and fixed exponent `a>0` can
satisfy `dist(z,S_v)<=Gamma gap^a` uniformly over all `v>0`.
At `v=0` the entire residual interval is optimal. Moreover, the Hessian
of `F+alpha v^2/2` is

```
[ alpha   2z ]
[  2z     2v ].
```

At `v=0,z>0` its determinant is negative for every finite `alpha`.
Continuity also gives negative determinants at nearby interior points.
Thus this example lies outside the joint-convexifier premise. Its actual
optimizer is trivial; it is not a complexity lower bound.

Second take, for a fixed `gamma>1`,

```
F_gamma(v,z)=gamma v-v^2 z,    (v,z) in [0,1]^2.       (10)
```

The residual fiber is affine. Every `v>0` has unique residual optimizer
`z=1`. The projected objective is `gamma v-v^2`, whose unique minimizer
on `[0,1]` is `v=0`. The full optimal set is `{0} x [0,1]`, and its
minimum-norm point is `(0,0)`. Therefore solving each residual fiber
exactly at any sequence of positive approximate cores tending to zero
returns points tending to `(0,1)`, not the minimum-norm optimizer.
Such `gamma` form a positive-probability interval under symmetric uniform
core noise with support radius greater than one. No quadratic core
convexifier exists here either: the residual Hessian is zero and the
cross derivative is `-2v`, which makes the full Hessian indefinite for
`v>0` regardless of its core diagonal.

This specifically defeats minimum-norm selection by approximate-core
substitution. The returned sequence still tends to a different fixed
global optimizer and approaches the full optimal set. Consequently it
does not refute an arbitrary selected-point Cauchy oracle.

## 5. What remains unresolved

Rational input heights alone do not lower-bound the nonzero values of
the minor polynomials at an unknown algebraic core. Computing a Hoffman
constant at a rational approximate core does not repair this: a minor can
vanish at that approximation while being tiny and nonzero at the true
core. The exponential family in (5) is useful for a coarse geometric
description, but testing every member would lose the requested work bound.

A full extension would need a sound, efficiently checkable way to control
the relevant margins or bypass them, together with a quantitative analysis
under the same finite noise law. A statement that margins hold with high
probability cannot by itself justify incorrect point output on exceptional
atoms. The fallback must be activated by a sound stopping or verification
rule.

The completed result is therefore limited: residual-convex cubics have a
fixed rational kernel on each relative core face, their residual optimizer
slices involve one quadratic varying row, and supplied face/minor margins
give a polynomial-bit error bound. Whether those facts yield the inherited
smoothed full-point work bound without joint convexification remains open
in this exploration. No hardness reduction has been established.

## Verification

The claims are algebraic and do not depend on numerical experiments.
The independent review checked the full note, including the constants,
dyadic margin normalization, and the examples' limited implications.
Targeted inline `python3` checks passed for local Markdown links, code
fences, and trailing whitespace in this note and its review. Link checking
excluded code blocks and spans to avoid treating matrix notation as links.
No optimization experiments, project-wide checks, or CI inspection were
performed. The exploration is closed at the scope stated above.
