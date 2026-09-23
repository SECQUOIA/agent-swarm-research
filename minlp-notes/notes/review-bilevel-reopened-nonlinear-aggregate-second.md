# Second independent audit: convex polynomial aggregate coupling

Date: 2026-09-06. Subject:
[bilevel-reopened-nonlinear-aggregate.md](bilevel-reopened-nonlinear-aggregate.md),
Sections 1–10, including the refined residual bound and explicit response
modulus. The reviewer also checked the polynomial-upper-function interface
in Section 12 of the [response-constraint companion](bilevel-reopened-response-constraints.md).

**Verdict: PASS.** No mathematical correction was required. This is an
independent proof audit, including the inherited multiplier, repair, and
inverse-modulus interfaces. It does not establish publication priority or
practical performance of the real-algebraic algorithm.

## Model and inherited constants

Subtracting `f_i'(0)t` from each local cost and the same constant from its
linear incentive preserves the follower objective. Strict convexity of a
univariate polynomial on the interval makes its derivative strictly
increasing, even when the second derivative vanishes at isolated points.
Thus normalization supplies the required clipped inverses and positive
`G_i`. The sum of strictly convex local costs remains strictly convex after
adding a convex aggregate cost. The follower optimizer is therefore unique
on every nonempty feasible polytope.

The exact feasible-leader polytope depends only on the box and resource
matrix, so adding the aggregate objective does not alter it. The inherited
normal-cone proof needs a gradient bound, not separability. Its resource
multiplier bound therefore remains valid, including on degenerate feasible
faces and for equalities represented by opposite rows. The integer-minor
Hoffman repair bound is likewise unchanged.

The coordinate Bregman bound is preserved because the aggregate's Bregman
divergence is nonnegative on the convex aggregate box. A row-sum Hessian
bound supplies the asserted infinity-norm Lipschitz constant for its
gradient. The factor `sum_i ||U_i||_1` correctly bounds
`||U(z-q)||_1` by that factor times `||z-q||inf`. All coefficient-derived
constants have polynomial bit length for numerical dense degree, even when
their values are large. Convexity is required only at feasible leaders;
absolute coefficient bounds can safely be computed over the larger cube.

## Aggregate residual and its sharper form

Writing `a=gradient phi(x,w)` and `a_q=gradient phi(x,Uq)`, the frozen
box variational inequality implies

```
gradient F_x(q)^T(z*-q)
 >= -lambda^T C(z*-q)+(a_q-a)^T U(z*-q).
```

Combining this with convexity gives the claimed lower bound on `F_x(z*)`.
The multiplier sign is correct: since `Cz*<=b` and `lambda>=0`,
`lambda^T(Cq-Cz*) >= lambda^T(Cq-b)`. Hence approximate complementarity
and aggregate consistency bound `F_x(q)-F_x(z*)` from above by
`zeta+D rho`. Repairing to a feasible `y` adds at most `LK delta`.
Uniform convexity at the constrained minimizer then proves equation (3).

Retaining `||z*-q||inf` in the aggregate term is legitimate. With
`t=||y-z*||inf`, the triangle inequality gives

```
mu t^(P+1) <= a+b t,
a=LK delta+zeta+D rho K delta, b=D rho.
```

If `t` exceeded both `(2a/mu)^(1/(P+1))` and `(2b/mu)^(1/P)`, the two
right-hand terms would each be smaller than half the left-hand side.
This proves (3a), including cases in which either coefficient is zero.
When `delta=zeta=0`, `q` is feasible, so use `y=q`; direct division for
positive distance gives the sharper `(D rho/mu)^(1/P)` bound. Zero distance
needs no division and satisfies it automatically.

At zero residual the box VI is the full follower KKT system. Bounded
multipliers, bounded aggregates, and continuous clipped inverses permit
subsequence passage at changing leaders. Uniqueness identifies every limit,
proving response continuity and attainment of the upper minimum.

## Nonpolyhedral branch cover and fixed dimension

The polynomial arguments have a fixed number `r+s+k` of variables and
polynomial numerical degree. Pulling rational inverse-branch endpoints back
through these arguments creates polynomial hypersurfaces. Their realizable
sign conditions, including zero signs and conditions restricted to a
lower-dimensional `Q_0`, can be sampled in polynomial time in fixed
dimension. Connected-component enumeration is not needed here.

The sign vector determines a valid branch for each inverse. Forming a set
from that branch vector's **closed validity inequalities** is safe: any
added points continue to satisfy all chosen branch intervals. These sets
may be disconnected, may overlap, and may have irrational boundaries; none
of those facts invalidates the uniform branch approximation. Every point
of `Q_0` has a realizable sign vector, so the resulting polynomially many
sets cover it. Adjacent branches are valid at a shared endpoint. This
construction does not enumerate all arbitrary products of branch choices.

The resource residual, complementarity residual, aggregate residual, and
objective are polynomial in the same fixed number of variables. Their
degrees and coefficient encodings stay polynomial after composition.
Compactness ensures attained cell optima. A fixed-dimensional optimality
formula with a second copy of the variables suffices for exact algebraic
optimization. Comparing the polynomially many algebraic cell values does
not require adjoining all follower inverse values to one algebraic field.

## Rational recovery and the full error ledger

Preserving a nonlinear branch equality could require irrational output.
The manuscript correctly preserves only the rational polytope `Q_0`.
Every point of that compact polytope lies in the convex hull of at most
`r+s+k+1` rational vertices. Enumeration in fixed dimension and algebraic
sign tests find such a simplex, including when the polytope is a point or
lies on a proper affine subspace. Rational barycentric rounding gives an
arbitrarily close rational member of the same polytope with polynomial
precision cost. No nonlinear branch membership is asserted afterward.

The inverse argument modulus is sound. For `d<=P` and `eta<=1/2`,
`(eta/(2d))^d >= (eta/(2P))^P`. The inherited interpolation inequality
therefore gives the stated common `alpha`; clipping does not invalidate
the lower bound on argument displacement needed for an output displacement.
The polynomial-argument Lipschitz bound transfers coordinate recovery
distance to that argument bound.

At the valid algebraic winner the true residual allowances are
`2S eta`, `2k Lambda S eta`, and `2A eta`. Between that point and its
rational recovery, the true clipped response changes by at most `eta`.
Consequently the resource residual changes by at most `2S eta`, and the
aggregate residual by at most `2A eta`, giving the stated factors four.

The complementarity transfer needs both terms in the manuscript's product
difference identity. The changed residual contributes at most
`2k Lambda S eta`. The changed multiplier contributes at most
`k Lambda S eta`, because the **absolute** old true residual is bounded
by `Ebar=S+sup ||b||inf`. This handles arbitrarily negative inactive slack;
bounding only its positive violation would not suffice. The resulting
factor five is correct.

The chosen inverse tolerance implies `K delta<=tau/2` and bounds the
nonlinear term in (3) by `tau/2`. Comparing the polynomial objective at its
valid algebraic argument with the true objective at the recovered leader
costs at most `epsilon/16+||c||_1(2eta+tau)`, as stated. The upper
comparison with a true optimal lift and the lower comparison using exact
leader feasibility prove both requested output guarantees. All required
precision logarithms are polynomial, including the factor
`(tau/2)^(P+1)`. The argument never evaluates an invalid branch polynomial
at the rounded point and never claims a rational exact follower response.

## Leader-response modulus in Section 10

For two feasible leaders, their old follower optima violate the other
resource right-hand sides by at most `B_b Delta`. Hoffman repair supplies
points `y,y'` feasible at the opposite leaders and within `K B_b Delta`.
The displayed comparison of objectives uses optimality at the first
leader, two changes of leader of cost at most `T_x Delta`, and two repairs
of cost at most `L K B_b Delta`. Its direction is correct and its total is
`2(T_x+L K B_b)Delta`.

Apply the Bregman bound at the second constrained optimum to its feasible
competitor `y`, then add the repair distance. This proves (9). It needs no
strong curvature or Slater condition. The bound also holds when any of
`Delta`, `B_b`, or `T_x` is zero, with the displayed zero terms understood
literally.

## Polynomial upper-function interface

The companion's Section 12 interface is valid for the aggregate graph.
Substituting branch polynomials into an explicitly listed upper monomial
gives total degree at most `D_up max(1,d_p)` in the fixed-dimensional
compressed variables. Expansion, coefficient growth, and optimization
therefore remain polynomial in numerical degree and explicit input size;
the number of follower coordinates does not become an algebraic dimension.

On a valid branch, inverse error at most `1/4` places `p` inside
`[-1,2]^N`. For an upper polynomial monomial, summing partial derivative
absolute bounds gives exactly the conservative constants

```
L_x=sum |a_(alpha,beta)| |alpha|_1 2^|beta|_1,
L_z=sum |a_(alpha,beta)| |beta|_1 2^|beta|_1.
```

The segment between the true recovered response and the polynomial response
at the original valid algebraic point stays in this enlarged box. Thus the
mean-value estimate bounds the change by
`L_x h+L_z(2eta+tau)` without evaluating an invalid branch at recovery.
This supports the polynomial-upper extension with the companion's stated
margin qualifications. It does not remove the obstruction to unrestricted
exact upper-feasible rational output.

This review does not re-audit the companion's entire tightening theorem;
its conclusion here is that the nonlinear aggregate graph supplies the
required approximation and rational-recovery interface.
