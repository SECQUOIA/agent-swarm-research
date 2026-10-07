# A continuous constraint obstruction with a fixed repair constant

Date: 2026-10-02. Status: proved and independently checked.

Adding local affine feasibility constraints and a Lipschitz feasible-repair
map does not preserve the objective-gradient-slope algorithm in
[`regridded-certificates/note.md`](../regridded-certificates/note.md).
The example below has three continuous variables, treewidth one, exact
convex objective models, fixed quadratic growth, fixed objective curvature,
and a repair constant of one. Nevertheless, every certificate using that
algorithm's slopes needs at least
`sqrt(2/3) L / sqrt(eps)` separator cells. Here `L` is an objective-gradient
and constraint-multiplier magnitude, which can grow arbitrarily.

This is an obstruction to the proposed slopes and the repair argument.
It is not an impossibility theorem for constrained optimization or for all
affine-slope certificates. A multiplier-aware slope gives an exact
certificate with one separator cell on the same example.

## 1. Instance and fixed parameters

For `L>0`, use variables `(x,s,y)` in `[-1,1]^3` and minimize

```
F(x,s,y) = (x^2+s^2+y^2)/2 + Lx-Ly
```

subject to the affine equalities

```
x=s,       y=s.
```

The root bag is `V_r={x,s}` and the child bag is `V_t={s,y}`. Assign
the equality `x=s` and objective

```
a_r(x,s) = (x^2+s^2)/2 + Lx
```

to the root. Assign `y=s` and

```
a_t(s,y) = y^2/2-Ly
```

to the child. The separator is `{s}`. Both bag objectives are convex, so
take their exact functions as the convex lower models. All local
optimization problems remain convex after imposing their local affine
constraints.

The feasible set is the diagonal

```
K = {(q,q,q): -1<=q<=1}.
```

The unique optimizer is zero, and on the feasible set

```
F(q,q,q)-F(0,0,0) = 3q^2/2 = ||(q,q,q)||_2^2/2.
```

Thus the constrained quadratic-growth constant is `g=1/2`, exactly.
Both bag gradients have Lipschitz constant at most `M=1`, independently
of `L`. The relaxation-error constant is `A0=0`. There are two bags,
treewidth is one, and each variable occurs in at most two bags. In
particular, `M/g=2` and every coefficient in the constraints is fixed.

The repair map

```
R(z) = ((z_x+z_s+z_y)/3) (1,1,1)
```

is the Euclidean projection onto `K` for `z` in the box. It preserves the
box and is 1-Lipschitz. If

```
A = [[1,-1,0], [0,-1,1]],
```

then the eigenvalues of `AA^T` are 1 and 3. Consequently

```
||z-R(z)||_2 <= ||Az||_2.
```

So the usual residual-to-feasible-distance repair bound also has constant
one. In the bag-copy formulation, local feasible copies are `(u,u)` and
`(v,v)`. Repairing both to the common value `(u+v)/2` gives

```
||(u,u)-(q,q)||_2^2 + ||(v,v)-(q,q)||_2^2 = (u-v)^2,
q=(u+v)/2.
```

Thus a repair bound measured against the separator-copy mismatch has
constant one as well.

## 2. An exact first-order certificate gap

The objective-gradient separator slope prescribed by the regridding
algorithm is

```
lambda_t(c) = partial_s a_t(c_s,c_y) = 0.
```

It is zero for every center, including the known optimizer.
The local equality `y=s` does not enter this partial derivative.

Suppose a separator cell contains `[0,h]`, with `0<h<=1`. Use local
feasible copies

```
z^r=(0,0),       z^t=(h,h).
```

Each copy lies in some local leaf. The root leaf meets the separator
cell at zero, and the child separator coordinate belongs to the cell.
This is a valid configuration for the natural constrained version of
the certificate: local convex programs enforce their assigned affine
equalities. With the prescribed slope its value is exactly

```
Phi = h^2/2-Lh.
```

Therefore `LB<=h^2/2-Lh` even though the center and incumbent can be the
exact optimizer, whose value is zero. The copy width contributes an
`Lh` error, despite fixed `M/g`, fixed repair constant, and zero local
relaxation error. A central shell cell `[0,h]` is one concrete instance;
the next section removes any shell or central-cell assumption.

The point assembled from topmost copies is `(0,0,h)`. Its Euclidean
repair is `(h/3,h/3,h/3)`, with objective value `h^2/6`. Hence

```
F(R(0,0,h))-Phi = Lh-h^2/3.
```

Geometric repair costs only `O(h)` in distance but has a first-order
objective cost whose coefficient is not controlled by objective
curvature. The unconstrained proof's exact cancellation of copy terms
does not cancel this additional repair cost.

## 3. A cell-count lower bound for arbitrary partitions

Consider any constrained certificate with constant child cell minorants
`l_D(s)=beta_D`. Allow arbitrary finite box partitions in both bags and
arbitrary convex child bounds satisfying the original cell-minorant
condition. Local certificate inequalities are imposed on the locally
feasible points of each leaf. The lower bound therefore covers the
objective-gradient-slope algorithm and is independent of its choices of
bag partitions or child-bound implementation.

For any `u,v` in the same separator cell `D`, validity at child point
`(v,v)` gives

```
beta_D <= v^2/2-Lv.
```

Choose a root leaf containing `(u,u)`. At its feasible point `(u,u)`,
the root certificate inequality and the child cell-minorant condition
give

```
l_r <= u^2+Lu+beta_D <= u^2+v^2/2-L(v-u).          (1)
```

Using lower models below the exact objectives can only strengthen this
upper bound on `l_r`.

Suppose the certificate proves tolerance `eps`, so that `l_r>=-eps`.
Fix `0<r<=1` and set `J=[-r,r]`. For each separator cell let
`[u,v]=D intersect J` when that intersection is nonempty. Equation (1)
implies

```
L length(D intersect J) <= eps+3r^2/2.
```

The separator cells cover `J` with disjoint interiors. Summing their
intersection lengths gives

```
|P_t| >= 2rL/(eps+3r^2/2).
```

For `0<eps<=3/2`, choose `r=sqrt(2eps/3)` to obtain

```
|P_t| >= sqrt(2/3) L/sqrt(eps).                    (2)
```

Thus even for fixed `L=1`, the required count grows as
`eps^(-1/2)`. For fixed accuracy it grows linearly in `L`, while all the
growth, curvature, incidence, and repair constants above stay fixed.
This is a lower bound on all certificates with these slopes, not just
a failed partition or a poor choice of starting point.

More generally, if a common separator slope `lambda` is used, the same
argument gives

```
|P_t| >= sqrt(2/3) |L+lambda|/sqrt(eps).
```

When `L+lambda<0`, interchange `u` and `v` in (1). The quadratic terms
are still at most `3r^2/2`. This formulation identifies slope error
relative to the constrained value-function slope as the relevant
quantity.

## 4. What a constrained extension must change

The child value function is

```
phi_t(s)=s^2/2-Ls,
```

whose derivative at the optimizer is `-L`, although
`partial_s a_t=0`. Using `lambda=-L` and `beta=0` on the single cell
`[-1,1]` is a valid child minorant. The root objective plus this child
bound, restricted to `x=s`, is `s^2`, whose minimum is zero. One leaf
per bag and one separator cell therefore give an exact certificate.

The constraint multipliers at zero make the missing term explicit.
With the equality convention `F+mu_1(x-s)+mu_2(y-s)`, stationarity
gives `mu_1=-L` and `mu_2=L`. Their magnitudes grow while the affine
constraint geometry and repair constants remain fixed.

Accordingly, a constrained theorem cannot retain the original slopes
and infer second-order repair cost from quadratic growth, objective
curvature, and a Lipschitz repair map alone. A successful extension
needs another mechanism, such as constraint-aware slopes with a
controlled error, a stronger objective-aware repair property, or an
explicit first-order parameter and a different complexity bound.
This example alone does not rule out efficiently computing the exact
constraint-aware slope, which is immediate here.

## 5. Verification scope

An independent agent checked the growth constant, repair estimates,
first-order gap, and partition-independent argument. A targeted exact
rational check verified the displayed objective, repair, and pair-bound
identities over finite rational grids. The command actually run was
`python3 - <<'PY'` with an inline script; it completed 729 projection
checks and 441 copy-pair checks without failure. These checks support
the algebra and do not replace the proof. No project-wide or CI checks
were run.
