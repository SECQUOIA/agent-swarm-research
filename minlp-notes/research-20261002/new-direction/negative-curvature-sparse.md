# Sparse box QP parameterized by negative curvature

Date: 2026-10-02. Status: a consequential open algorithmic target and
checked structural ingredients. No general theorem or novelty claim is
asserted here. The full scalar-message closure route was ruled out by the
[stable-recurrence example](scalar-message-growth-obstruction.md).

For a rational continuous-box quadratic

```
F(x)=x'Hx/2+b'x+c,
nu=max(0,-lambda_min(H)),
```

the target is exact complexity `f(p,max(1,nu/g)) poly(I)`, where `p` is
the supplied largest bag size and `g` is global quadratic growth. Start
with a unique optimizer; arbitrary optimal sets and a growth-independent
certificate are further questions. Negative inertia may grow with the
instance, and large positive curvature should affect encoding length
only. This would complement both the current sparse `L/g` theorem and
the [few-negative-directions theorem](negative-inertia-qp.md).

This target is continuous. Setting `nu=0` already leaves convex integer
QP in the mixed case, so an unrestricted mixed extension needs a separate
tractability argument.

## 1. The exact convex-part energy has the desired conditioning

Suppose first that `s` is the unique global optimizer and
`F(x)-f*>=g||x-s||^2`. Write `d=x-s`. First-order optimality on the
convex box gives `grad F(s)'d>=0`; exact quadratic expansion therefore
implies

```
F(x)-f* >= d'Hd/2.
```

Take a convex combination of this inequality and point growth, with
weights `g/(g+nu)` and `nu/(g+nu)`. The result is

```
F(x)-f* >= [g/(2g+2nu)] d'(H+2nu I)d.                 (1)
```

For `nu>0`, `P=H+2nu I` is positive definite. Thus global growth in
the exact convex-part metric is controlled by `nu/g`, regardless of
the largest positive eigenvalue. For a general compact optimal set,
the same inequality holds with `s` chosen as a Euclidean nearest
optimizer; in particular it implies growth toward the set in the
`P` metric as well. This follows because KKT holds at each optimizer
and the assumed set-growth inequality applies to that nearest point.

The identity is a useful ingredient, not a sparse algorithm. Whitening
by `P^(1/2)` generally makes the box constraints dense. Independent
coordinate rounding does not preserve cancellations in `d'Pd`.
Conditional sparse LDL coordinates preserve local equations, but their
grid shifts depend on separator values and can generate many distinct
states. A state count cannot be inferred just from (1).

## 2. Moreau smoothing fixes curvature but loses the factorization

For `lambda>nu`, define

```
E_lambda(c)=min_(x in X) [F(x)+lambda||x-c||^2/2].      (2)
```

Each evaluation is an exact strongly convex rational QP when `lambda`
and `c` are rational. Completing the square shows that
`E_lambda(c)-lambda||c||^2/2` is concave. Its upper coordinate
curvature is therefore `lambda`. Under growth toward the full optimal
set `S`, elementary squared-distance minimization gives

```
E_lambda(c)-f* >= g_E dist(c,S)^2,
g_E=g lambda/(2g+lambda),
lambda/g_E=2+lambda/g.                               (3)
```

Taking `lambda` within a constant factor of `nu` gives exactly the
desired numerical parameter. An approximate rational spectral bound,
as in the existing negative-inertia theorem, suffices; exact irrational
eigenvalues need not be input.

The obstacle is sparsity. On an unconstrained or fixed-active-set
branch, the envelope Hessian involves an inverse of `H+lambda I`; in
the unconstrained case it is

```
lambda H(H+lambda I)^(-1).
```

That matrix is generally dense even for a tridiagonal `H`. Exact
convex recourse is polynomial-time per evaluation, but does not supply
the bounded-width finite tables needed by the filtered-grid theorem.
Keeping latent convex variables instead restores local equations, not
automatically a bounded separator representation. The
scalar-message counterexample is a warning against asserting complete
quadratic-message closure from small separator dimension alone.

## 3. An easy baseline: the regime nu<2g

There is a useful baseline which needs no treewidth bound. It is an
existing-style consequence of weak convexity and quadratic growth,
and should not be promoted as the sought sparse theorem.

Let `c` be feasible and let `y` attain (2). Choose a nearest optimizer
`s` to `y`; write `Delta_y=F(y)-f*`. Weak convexity and the proximal
KKT inequality give

```
Delta_y <= lambda||c-y|| dist(y,S)+(nu/2)dist(y,S)^2.
```

If `a=1-nu/(2g)>0`, growth yields

```
a sqrt(Delta_y) <= (lambda/sqrt(g))||c-y||.
```

The inequality is immediate when `Delta_y=0`; otherwise divide by
its positive square root. Comparing the proximal objective at `y`
and `c` also gives

```
Delta_c-Delta_y >= (lambda/2)||c-y||^2.
```

Consequently the exact convex proximal iterations satisfy

```
Delta_y <= [C/(1+C)] Delta_c,
C=2lambda/[g(1-nu/(2g))^2].                           (4)
```

This proof permits arbitrary optimal sets and applies on any bounded
convex polytope, not only a box. Its contraction rate depends on the
margin below `nu/g=2`. With a trusted quantitative promise it provides
a route to the existing exact recovery step. It is not an independently
valid global certificate when the growth estimate is guessed.

The threshold is sharp for this mechanism. On `[0,1]`,

```
F(x)=nu x-(nu/2)x^2
```

has unique optimizer zero and valid `g=nu/2`, but `x=1` is stationary
and remains a fixed point of every proximal map with `lambda>nu`.
Thus the substantive sparse target includes ratios at and above two,
where globally convergent proximal iteration no longer follows.

## 4. The actual structural question

Can a bounded-width certificate retain the PSD energy in (1) exactly,
and discretize only concave energy, with a state count controlled by
`p` and `nu/g`? Such a method must handle consistency of separator
variables without densely whitening the original box or enumerating
complete conditional value functions.

The currently known metric bound and convex oracle do not answer this.
Nor does replacing a numerical positive-curvature bound by a new
uncontrolled separator-condition parameter. A useful next proof must
show how the positive energy controls accumulated disagreement between
local representations, or produce a bounded-size global representation
which avoids that disagreement. This is the open step worth pursuing.

These identities were derived directly. They neither depend on external
literature priority nor establish a practical solver speedup. The
current contribution of this note is to isolate the numerical advantage,
the easy baseline, and the precise sparse-representation gap.
An [independent review](negative-curvature-sparse-review.md) checked the
metric inequality, envelope identities, proximal contraction, constrained
boundary cases, and the sharp-threshold example. No general sparse
algorithm follows from those checks.
