# Translation symmetry, sparse separators, and a dimension bound

Date: 2026-10-02. Status: the finite-difference proof passed an
[independent adversarial review](../reviews/translation-separator-growth-review.md)
with targeted exact-arithmetic checks. No external prior-art search or
originality claim is made.

## Main conclusion

The hypotheses of the [coordinate-face theorem](gauge-face-exploration.md)
strongly restrict the dimension when the optimal translation orbit has
positive length. Let `p` be the maximum bag size in a supplied tree
decomposition, let `L>0` be the upper coordinate-curvature bound, and let
`g>0` be the quadratic-growth constant in distance to the optimal set. Then

    n <= max{4p, 8p^2 L/g} <= max{4p, 8p^2 kappa},
    kappa=max{1,L/g}.

This is a structural limitation. At fixed width and fixed conditioning, the
class with a positive-length translation orbit cannot have arbitrarily many
variables. Absorbing dimension into these parameters can yield a formal
fixed-parameter consequence, but it does not describe a large-dimensional
family at fixed parameters.

The proof uses only finite differences, coordinate semiconcavity, and the
factorization. It does not assume twice differentiability, a Hessian, or
convexity of the objective.

## Assumptions

The feasible set is the nondegenerate continuous box
`X=product_i[a_i,b_i]`, with `a_i<b_i`. The objective is a sum of factors
whose scopes are contained in bags of size at most `p` in a tree
decomposition. Coordinate semiconcavity means that, with all other
coordinates fixed,

    u -> F(x_1,...,u,...,x_n)-L u^2/2

is concave on its interval. Translation invariance is assumed only on
feasible pairs:

    F(x+t 1)=F(x) whenever x,x+t 1 belong to X.

The optimal set is

    O=(s0+span{1}) intersect X,

has positive length, and satisfies

    F(x)-f* >= g dist(x,O)^2       for all x in X.

The symbol `O` distinguishes the optimal set from the separator used below.

## An interior optimum and a balanced separator

The feasible shifts along the optimal orbit form a closed interval of
positive length. Choose a shift strictly between its endpoints, obtaining
an optimum `x*`. Every coordinate of `x*` lies strictly between its box
endpoints. Thus every perturbation below is feasible for sufficiently small
positive `t`, including perturbations of size `p t` in either direction.
No objective is evaluated outside the box.

The primal graph joins variables that occur in a common factor. A tree
decomposition with maximum bag size `p` supplies a vertex separator `B`
with `k=|B|<=p` such that every connected component of the graph minus `B`
has at most `n/2` vertices. For completeness, assign each variable's unit
weight to one bag containing it, and take a weighted centroid of the bag
tree. Its bag is a suitable separator: every graph component outside that
bag lies within one component of the remaining tree, whose assigned weight
is at most `n/2`.

If `n<=4p`, the claimed conclusion already holds. Suppose `n>4p`.
The total number of vertices outside `B` exceeds `3n/4`. By adding graph
components until their total first reaches `n/4`, obtain a union `A` with

    n/4 <= |A| <= 3n/4.

The upper bound holds because each component has at most `n/2` vertices.

## Exact additivity of component perturbations

For a vertex set `U`, write

    Delta_U(t)=F(x*+t 1_U)-f*.

Every such increment is nonnegative when its argument is feasible. A factor
cannot contain vertices from two different components of the graph minus
`B`. Keeping the separator coordinates fixed therefore gives the exact
identities

    Delta_(V\B)(t)=sum_C Delta_C(t),
    Delta_A(t)=sum_(C contained in A) Delta_C(t),

where `C` ranges over those components. Each identity follows factor by
factor after subtracting its value at `x*`. Consequently,

    0 <= Delta_A(t) <= Delta_(V\B)(t).

Translation invariance, applied to two feasible points, gives

    Delta_(V\B)(t)=F(x*-t 1_B)-f*.

If `k=0`, this increment is zero. The lower growth bound below is strictly
positive, giving a contradiction. Hence only `k>=1` needs an upper estimate.

## Asymmetric rounding bounds the separator increment

Independently for each coordinate `i in B`, let a random perturbation `Z_i`
take values

    -t    with probability k/(k+1),
     k t  with probability 1/(k+1).

All other perturbations are zero. Each has mean zero and variance `k t^2`.
Successive application of coordinate semiconcavity gives

    E[F(x*+Z)-f*] <= (L/2) sum_(i in B) Var(Z_i)
                  = L k^2 t^2/2.

Independence preserves the zero mean and the same variance at each rounding
step. Interior feasibility allows the required positive perturbation `k t`.

Every value inside this expectation is nonnegative by global optimality.
The event that every separator coordinate takes value `-t` has probability

    (k/(k+1))^k >= 1/3,

using `(1+1/k)^k<=e<3`. Retaining only that event in the expectation yields

    F(x*-t 1_B)-f* <= 3L k^2 t^2/2.

This estimate avoids the exponential dependence on separator size that would
result from assigning equal probabilities to `-t` and `+t`.

## Growth gives the dimension bound

Distance to the optimal segment is at least distance to its containing
affine line. Orthogonal projection onto that line gives

    dist(x*+t 1_A, x*+span{1})^2
      = t^2 |A|(n-|A|)/n
      >= 3n t^2/16.

Combining growth, component additivity, translation, and the rounding bound,

    3g n t^2/16 <= Delta_A(t) <= 3L k^2 t^2/2.

Cancel the positive `t^2`. This gives

    n <= 8k^2 L/g <= 8p^2 L/g.

Together with the initial case `n<=4p`, this proves the stated bound.

## Interpretation and algorithmic limits

For a smooth graph energy, the analogous reasoning is a familiar separator
test for a Poincare or spectral-gap inequality: a vector nearly constant on
large graph components changes only through a small separator. A substantial
global gap is incompatible with a large graph and uniformly bounded local
curvature. Here finite differences give that conclusion for nonconvex,
possibly nonsmooth objectives with coordinate upper curvature. No novelty
claim follows from this comparison.

For example, the graph quartic family in the coordinate-face note has
`L=2 max_degree` and `g=lambda_2/2`, where `lambda_2` is the graph Laplacian's
smallest positive eigenvalue. Fixed-width examples can grow in size by
allowing this conditioning ratio to grow. The theorem excludes keeping both
parameters bounded as dimension increases.

The coordinate-face theorem's factor involving `n` in the effective
conditioning can now be bounded by a function of `p,kappa` for positive-length
orbits. This observation alone does not turn an accuracy exponent depending
on `p` into a uniform polynomial exponent. In particular, a uniform grid
with cost `eps^(-O(n))` remains exponential in requested accuracy bits.
A uniform fixed-parameter corollary in bit accuracy still requires a proved
growth-controlled refinement bound, such as a bounded number of retained
cells per level, together with suitable arithmetic and representation
assumptions. If such a method has work
`f(n,kappa) poly(input length + requested accuracy bits)`, substituting the
dimension bound gives a corresponding `f'(p,kappa)` bound. The source of
that consequence is bounded dimension, not a new way to solve arbitrarily
large sparse instances at fixed width and conditioning. This note proves
the dimension obstruction only; it does not claim a new refinement analysis,
arithmetic implementation, or bit-complexity theorem.

The positive-length assumption is essential to this proof: a singleton
optimal orbit may lie on the box boundary, where the signed perturbations
are infeasible. It is also necessary for the dimension conclusion. On
`[0,1]^(2m)`, consider the affine objective

    F(x)=sum_(i<=m) x_i + sum_(i>m)(1-x_i).

It is translation invariant because its linear coefficients sum to zero.
Its unique optimum has its first `m` coordinates zero and its last `m`
coordinates one. The translation orbit through this optimum intersects the
box only at that point. For every feasible point, each coordinate's slack
from its optimal endpoint dominates the square of that slack. Thus global
growth holds with `g=1`; `L=1` is a valid upper curvature bound, and the
unary factorization has `p=1`. The dimension `2m` is arbitrary at these fixed
parameters. The argument also does not cover arbitrary curved optimal
manifolds or multiple distinct optimal translation orbits.

## Verification record

The [independent review](../reviews/translation-separator-growth-review.md)
checked interior feasibility, the balanced separator, exact component
additivity, feasible-pair translation, asymmetric rounding, the empty
separator case, and the constants. It found no mathematical gap and supplied
the boundary counterexample above.

The reviewer ran one targeted inline Python calculation using
`fractions.Fraction`. It passed the mean, variance, and all-minus probability
checks for each separator size `k=1,...,100`. It also checked a nine-variable
sparse quartic example with a two-variable separator, exhaustively enumerating
all four asymmetric perturbation outcomes. That example passed feasibility,
component additivity, translation equality, expectation and all-minus bounds,
and the orbit-distance estimate. The linked review records the command and
exact instance.

These finite checks support the algebra; the proof establishes the general
bound. No project-wide verification, CI inspection, performance measurement,
or external literature search was run for this result.
