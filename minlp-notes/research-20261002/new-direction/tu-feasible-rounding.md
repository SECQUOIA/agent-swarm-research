# Feasible second-order rounding for aligned TU constraints

Date: 2026-10-02. Status: proved rounding lemma; no complete constrained
smoothed-work theorem is asserted.

The rounding step in
[the polynomial box theorem](smoothed-sparse-polynomial.md) extends to
totally unimodular constraints on an aligned grid. The rounding must be
correlated, and its objective bound needs curvature in all directions.
Conditional semiconcavity remains a separate issue, as the TU example in
[the constrained barrier](constrained-smoothing-barrier.md#3-a-tu-obstruction-to-the-coordinatewise-counting-argument)
shows.

Let

```text
P={x in [0,1]^n: Ax<=b},
```

where `A` is an integral totally unimodular matrix and `b` is integral.
Equalities may be represented by both inequality signs. For an integer
`j>=0`, set `h=2^(-j)`. Let `C=prod_i [k_i h,(k_i+1)h]` be a grid
cell contained in `[0,1]^n`, with each `k_i` integral, and let
`x in P intersect C`.
Then there is a random vector `Y` supported on the feasible corners of
`C` such that

```text
E Y=x,
E ||Y-x||_2^2 <= n h^2/4.                         (1)
```

Indeed, substitute `x=h(k+z)`. The cell-feasibility polytope becomes

```text
Az<=b/h-Ak,    0<=z<=1.
```

Its right-hand side is integral, and adjoining coordinate-bound rows
preserves total unimodularity. Every vertex is integral, hence belongs
to `{0,1}^n`. Expressing the transformed point as a convex combination
of these vertices gives the required distribution. For each coordinate,
the endpoint support and its preserved mean give

```text
E (Y_i-x_i)^2=(x_i-k_i h)((k_i+1)h-x_i)<=h^2/4.
```

This also covers coordinates fixed to grid nodes: fix them before the
argument, subtract their integral scaled contributions from the right
side, and give them zero variance. In particular, native integer labels
already fixed in a slice cause no difficulty. Fixing endpoints also
allows the distribution to stay in specified incident bag cells when a
point lies on grid boundaries. Since it never leaves those cells, it
preserves any already imposed whitelist of such bag cells.

Suppose a twice continuously differentiable objective and `L>=0` satisfy

```text
Hess F_0(z) <= L I
```

in the positive-semidefinite order throughout the original box. For
`F_gamma=F_0+gamma'x`, Taylor's bound along each segment from `x` to
`Y` gives

```text
E F_gamma(Y)
 <= F_gamma(x)+grad F_gamma(x)' E(Y-x)+(L/2)E||Y-x||^2
 <= F_gamma(x)+n L h^2/8.                         (2)
```

Thus at least one feasible corner has the usual second-order objective
bound. A fixed-cell lower-bound argument may use the existence of this
corner without constructing the distribution. A sparse grid dynamic
program can enforce affine constraints from their bounded bag scopes;
that observation alone does not bound its expected table sizes.

The full Hessian assumption in (2) cannot be replaced by the original
coordinatewise diagonal bound when rounding is correlated. For example,
take the TU equality `x_1=x_2` and objective `F_0=2x_1 x_2`. At
`x=(h/2,h/2)`, the only feasible corners of `[0,h]^2` are `(0,0)` and
`(h,h)`. The mean-preserving distribution assigns probability one half
to each. Its expected objective exceeds `F_0(x)` by `h^2/2`, although
both diagonal second derivatives are zero. The full Hessian upper bound
`L=2` makes (2) exact in this example.

Order constraints `x_i<=x_j` are a concrete class satisfying the matrix
and grid-alignment assumptions. Integral difference-constraint systems
also satisfy them on integer-aligned domains. Rational right-hand sides
need a compatible grid; clearing denominators may make its initial
numerical resolution large. The lemma does not remove that cost, bound
the number of polyhedral recourse pieces, or supply the constrained
semiconcavity/counting and exact-closure steps of a full extension.

An independent reader checked the completed lemma, including cell
integrality, mean preservation, whitelist boundaries, and the full-Hessian
counterexample. Its requested sign and grid-convention clarifications
are included above. This is an analytic lemma. No project-wide
verification, CI inspection, or literature search was performed.
