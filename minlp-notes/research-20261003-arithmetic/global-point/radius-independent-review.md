# Independent review of the integrated-Hessian radius construction

Date: 2026-10-03. This review checks the proposed explicit radius for a
globally convex rational polynomial on an arbitrary rational polyhedron.
The review is independent of the main write-up. Its exact-arithmetic
diagnostics test finite examples; the arguments below establish the
general claims.

The construction is valid, with the qualifications and conventions stated
below. In particular, it does not need to expand a polynomial after an
affine change of coordinates. Its bit bound is polynomial in the explicit
sparse input length and the **numeric** degree bound `D`, not necessarily
in the binary encoding length of `D`.

## Tangent-quadratic lower bound

Let `D>=max(2,deg f)` and `K=(D+1)D^(D+2)`. Fix `a,x` and write

```text
h(t)=f(a+t(x-a))-f(a)-t grad f(a)'(x-a).
```

Global convexity gives `h>=0`, `h(0)=h'(0)=0`, and
`0<=h(j/D)<=h(1)` for `j=0,...,D`. The Lagrange numerator at node `j/D`
is a product of `D` factors with roots in `[0,1]`. Its coefficient of
`t^2` has absolute value at most `binom(D,2)`. The absolute denominator
is `j!(D-j)!/D^D>=D^(-D)`. Thus the second derivative at zero of each
basis polynomial has absolute value at most `D^(D+2)`. Interpolation
and the triangle inequality give

```text
h''(0)<=K h(1),
f(x)>=f(a)+grad f(a)'(x-a)+(x-a)'H(a)(x-a)/K.       (1)
```

Integrate in `a` over `[0,1]^n`, which has volume one. The result is

```text
f(x)>=q(x)=c+ell'x+x'Mx/K,
M=integral H(a) da,
ell=integral [grad f(a)-2H(a)a/K] da,
c=integral [f(a)-grad f(a)'a+a'H(a)a/K] da.          (2)
```

These formulas fix the factor of two in the linear coefficient. All
integrals are evaluated directly on sparse monomials. For a monomial
`a^alpha`, its integral is `product_i 1/(alpha_i+1)`. Differentiation,
multiplication by one or two coordinate variables, and coefficient
collection produce at most a polynomial number of terms. The product
denominators have polynomial binary length in the input and `D`.

## Common kernel and the affine part

The matrix `M` is positive semidefinite. If `v'Mv=0`, continuity and
nonnegativity imply `v'H(a)v=0` throughout the cube. Polynomial identity
then extends this equality to all `a`. Because every `H(a)` is positive
semidefinite, `H(a)v=0` everywhere. The converse is immediate. Thus
`ker M` is exactly the common Hessian kernel.

Let `Pi` be the orthogonal projector onto `range M`, computed with
rational linear algebra, and set `w=-(I-Pi)grad f(0)`. Integration of
the directional derivative along `ker M` gives

```text
f(x)=f(Pi x)-w'x,             (I-Pi)ell=-w.          (3)
```

The normalization in (3) matters: a vector whose directional derivative
is `-1` is not necessarily the affine-slope vector. The review uses the
projected gradient, which has the required normalization directly.

## Finiteness certificate and sublevel bounds

Assume `P={x:Bx<=b}` is nonempty. Consider the rational feasibility LP

```text
w=B'lambda+Mz,             lambda>=0.               (4)
```

If (4) is infeasible, Farkas' lemma gives a direction `d` with
`Bd<=0`, `Md=0`, and `w'd>0`. Formula (3) gives
`f(a+td)=f(a)-t w'd` for every feasible `a` and `t>=0`, proving
unboundedness below. The homogeneous direction can be scaled to satisfy
`w'd>=1`, so a rational certificate is computable by an ordinary LP.

If (4) is feasible, let `v=Mz`. Choose a rational `rho>0` no larger
than the least positive eigenvalue of `M`, divided by `K`. When `M=0`,
use `rho=1`; every projected vector is then zero. For all feasible `x`,
write `r=||Pi x||_2` and set

```text
beta=c-lambda'b,
A=||Pi ell-v||_1.
```

The one-sided bound `w'x<=lambda'b+v'Pi x` and (2) imply

```text
f(x)>=beta-A r+rho r^2.                             (5)
```

This proves boundedness below and therefore establishes the equivalence
between finiteness and (4), before attainment has been assumed.

For a feasible rational `a`, put `F=f(a)` and

```text
T=1+(A+|F-beta|+1)/rho.
```

If `r>T`, then `r>1` and `rho r-A>|F-beta|+1`, contradicting
`rho r^2-A r<=F-beta`. Thus `f(x)<=F` implies `r<=T`.
The affine component has the two separate bounds

```text
w'x<=lambda'b+||v||_1 T,
w'x=f(Pi x)-f(x)>=f(0)-||grad f(0)||_1 T-F.          (6)
```

Consequently

```text
W=1+|lambda'b|+||v||_1 T+|f(0)|+||grad f(0)||_1 T+|F|
```

bounds `|w'x|` on the specified sublevel set. The sublevel restriction
is essential. The rational example `f(s,t)=s^2-t`, `P={t<=0}`,
`w=(0,1)`, `lambda=1`, and `(s,t)=(0,-1)` refutes the unrestricted
absolute-value bound printed as equation (22) in the source audited
[here](../literature/source-audit.md): that bound would read `1<=0`.
Equations (5)--(6) use only valid one-sided inequalities.

One explicit rational choice of `rho` is also available. Clear the
denominators of `M` with a positive integer `E`, write `N=EM`, let
`r0=rank M>0`, and set `S=max(1,n max_ij |N_ij|)`. The product of the
positive eigenvalues of `N` is the sum of its `r0`-order principal
minors, a positive integer. Every eigenvalue is at most `S`. Hence

```text
rho=1/(K E S^(r0-1))                                (7)
```

is valid and has polynomial binary length. No algebraic eigenvalue
computation is needed.
The main theorem uses the weaker exponent `n-1` in place of `r0-1`
and a positive formula also when `M=0`; this remains valid because
`Pi=0` in that case.

## Lifting bounded invariants to a bounded feasible point

Let `A0=Q[M;w']` be integer, with positive integer `Q`. Scale each row
of `B` by a positive multiplier so that `B` is integer too. Let `C>=1`
bound the absolute entries of both matrices. For `n>=1`, put
`H0=(nC)^(n-1)`.

For every nonempty slice `P_t={x in P:A0x=t}` and every `a in P`,

```text
dist_2(a,P_t)<=H0 ||A0a-t||_2.                      (8)
```

For completeness, project `a` onto the closed convex slice and call
the projection `p`. Its normal `a-p` has a conical representation by
active inequality normals and signed equality normals. Choose a
linearly independent subcollection. The coefficient norm in that
representation is at most `||(a-p)||_2/sigma_min`, where `sigma_min`
is the smallest singular value of the independent row matrix. The
inner product of `a-p` with any active inequality normal is nonpositive,
since `a` is feasible for the inequalities. Taking the inner product
with `a-p` therefore bounds the squared distance by the equality
coefficient norm times `||A0(a-p)||_2`.

An independent integer row matrix has Gram determinant a positive
integer. Its singular values are at most `nC`, so its smallest singular
value is at least `(nC)^(-(r1-1))`, where `r1<=n` is its row rank.
This proves (8), including degenerate and lower-dimensional polyhedra.
The no-row case has zero normal and zero distance.

For any `y in P` with `f(y)<=F`, equations (5)--(6) give

```text
||A0y||_1<=Q(n^2 max_ij |M_ij| T+W).
```

Apply (8) to the slice through `y`. It contains a representative `y'`
with

```text
||y'||_2<R,
R=1+||a||_1+H0[||A0a||_1+Q(n^2 max_ij |M_ij| T+W)]. (9)
```

Equality of the `M` components implies `Pi y'=Pi y`; equality of the
`w` components and (3) then imply `f(y')=f(y)`. The radius controls a
representative of every relevant objective value, not every feasible
point or every optimizer.

A minimizing sequence can be chosen in the sublevel `f<=F` unless
`a` already minimizes. Its representatives lie in a compact ball and
remain feasible. Continuity gives an attaining limit. In either case
an optimizer has norm at most `R`; therefore the unique minimum-norm
optimizer does too. Intersecting `P` with `[-R,R]^n` preserves both the
optimal value and this selector. Rational LP solutions, matrix
operations, coefficient integrals, and every displayed scalar have
polynomial bit cost in the sparse input length and numeric `D`.

The zero-variable case is handled directly. The zero-rank case uses
the convention following (4). Empty `P` is handled before (4).

## Review of the complete theorem

The complete [theorem](theorem.md) was also checked against the radius
construction. Its stronger error bound on the original unbounded
polyhedron is valid: the Bregman interpolation bounds use only the
bounded optimizer `p`, and no step uses a bound on the arbitrary
feasible point `x`. In particular, `h(2(c-p))` is evaluated within
the box controlled by `||p||_infinity`, while interpolation along
`x-p` uses its objective gap rather than its norm.

The regularization schedule in the main theorem correctly uses
`4R tau` in the distance estimate. A nearest optimizer `s` to
`x_tau` need not lie in the radius ball, but
`||s-x_tau||<=||p-x_tau||<=2R`. Hence
`||s||+||x_tau||<=4R`, as required. The stated choice of `tau`
gives `dist(x_tau,S)<=epsilon^2/(8R)` and then
`||x_tau-p||<=epsilon/2`; objective accuracy
`tau epsilon^2/4` supplies the remaining `epsilon/2`.
This avoids assuming that every optimizer is bounded by `R`.

The simultaneous value enclosure uses the Lipschitz bound only on
the convex truncated polytope containing both `p` and the returned
point. Its objective lower endpoint is valid for the original problem
because the radius reduction preserves the optimum. These implications
remain conditional on the cited convex value interface; the radius
diagnostics do not implement that interface.

## Targeted verification

The companion script
[check_radius_construction.py](check_radius_construction.py) uses exact
fractions. It checks the interpolation derivative constant, integrated
quadratic coefficients and lower bounds on explicit convex fixtures,
the common-kernel decomposition, rank-zero and positive-rank radius
branches, unboundedness directions, and the equation (22)
counterexample. Its finite checks do not replace any of the general
arguments above or implement a general optimizer.

Command run: `python3 research-20261003-arithmetic/global-point/check_radius_construction.py`.
Result: passed 9 interpolation degrees, 455 integrated-quadratic and
affine-decomposition checks, 121 sublevel invariant checks, a closed-form
integration check, 5 radius fixtures, a bounded-representative example
with unbounded sublevel, the source absolute-value counterexample,
and an unboundedness certificate. The script was rerun after matching
the main theorem's weaker dimension-uniform curvature constant;
the counts and outcome were unchanged.
No project-wide verification or CI inspection was performed.
