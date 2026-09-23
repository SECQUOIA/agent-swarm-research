# Independent audit: cactus uncertainty hulls

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate: `notes/potential-flow-cactus-uncertainty-hulls.md`.

## Verdict

The separate-monotonicity theorem, interval-hull equality, signed-flow
extension, exact theta counterexample, and resulting characterization
of connected simple cactus graphs pass independent mathematical review.

The continuous-law statement does not need unbounded law ranges.
Continuous strict increase and a zero at zero already suffice for
existence and uniqueness of the unconstrained passive state. The compactness
and smoothing details below fill out the candidate's abbreviated argument.
The author was notified of this observation and of the scope concerning
additional operational feasibility constraints.

This audit establishes mathematical correctness, not priority. In
particular, resistance monotonicity and graph topology have a substantial
literature that requires a separate focused comparison.

## Physical existence, uniqueness, and continuity

Use an incidence matrix `A` with positive entries at edge tails.
The physical equations are

```
Ax=b,       A^T pi=g(x,theta).
```

Connectedness and balanced nominations make the affine flow space
nonempty. For every continuous strictly increasing law with `g(0)=0`,
its primitive `G(x)=integral_0^x g(t)dt` is strictly convex and
coercive. Explicitly, with
`c=min{g(1),-g(-1)}>0`,

```
G(x)>=c(|x|-1)   for |x|>=1.
```

The sum of edge primitives therefore has a unique minimizer on the
closed affine flow space. Its first-order conditions give the physical
potential equations. Connectedness makes potentials unique after one
reference potential is fixed. Bounded laws such as a hyperbolic tangent
cause no failure of this argument.

There is also a useful state bound independent of resistance magnitudes.
Orient each nonzero physical flow in its actual direction. Its potential
strictly decreases in that direction, so the directed support is acyclic.
Its flow decomposition has only source-to-sink paths; each edge's absolute
flow is at most the total positive nomination. This is valid for
asymmetric laws as well, because strict increase and `g(0)=0` make
the signs of flow and potential drop agree.

For compact nomination and parameter sets, those flow bounds are uniform.
Joint continuity of the finitely many edge-law families bounds all
potential drops on that compact flow range. Along a fixed spanning tree,
it bounds every normalized potential. Given a convergent sequence of
parameters and nominations, any convergent subsequence of these bounded
states satisfies the limiting equations. Uniqueness identifies the limit.
Thus the physical state and every pressure or flow objective are continuous.
In particular, all compact-set extrema used in the theorem exist.

For an affine parameter family, continuity jointly in flow and parameters
follows from continuity of the finitely many coefficient functions.
A nondegenerate parameter interval permits expressing each coefficient
as the difference of two continuous endpoint laws; a singleton parameter
has no monotonicity issue.

## Smooth adjoint calculation and cactus signs

First assume every law is smooth with strictly positive flow derivative.
Fix all nominations and all parameters except one scalar `theta`, affecting
only edge `e` through `g_e(x,theta)=g_base(x)+theta f(x)`.
Write `D=diag(partial_x g)`, a positive diagonal matrix. Differentiation
and elimination of the flow derivative give

```
A D^(-1) A^T pi' = A D^(-1) e_e f(x_e).
```

For objective `F=pi_s-pi_t`, let the normalized adjoint solve
`A D^(-1) A^T h=e_s-e_t`. Its edge currents are
`j=D^(-1)A^T h`, and hence

```
F'=j_e f(x_e).
```

This verifies the candidate's sign convention explicitly. Smooth dependence
on the parameter follows from the invertible reduced weighted Laplacian.

On a cactus, the adjoint has zero current outside the unique block route
from `s` to `t`: each attached component has a single attachment and
no adjoint source. A route bridge carries unit current in the route
direction. Within a route cycle, the two entrance-to-exit paths are
parallel positive-resistance chains. Each carries strictly positive
current from entrance to exit. Thus each edge's current is either
identically zero or has a sign fixed by topology and the chosen edge
orientation, independently of all physical nominations and law parameters.

If `f(x_e(theta_0))=0` anywhere, the entire physical state at
`theta_0` satisfies every constitutive equation at every other value
of this one parameter. The only changed term is zero. State uniqueness
then makes that state constant over the entire interval. Otherwise
continuity of the physical flow and `f` prevents the basis value from
changing sign. Consequently `F'` has one weak sign throughout the
parameter interval. This proves separate monotonicity, including the
constant and off-route cases. Other parameters may affect the same edge;
holding them fixed leaves the argument unchanged.

## Continuous laws and uniform limiting arguments

A precise surrogate for each original edge family is its convolution
with a smooth compactly supported mollifier, minus that convolution's
value at zero, plus a positive linear term tending to zero. This retains
the zero at zero and the affine one-edge parameter structure. Convolution
preserves monotonicity, and the added linear term makes the derivative
strictly positive. Thus the smooth theorem applies to every surrogate
throughout the same parameter box.

The surrogate laws converge uniformly on bounded flow ranges and compact
parameter sets. The physical-flow bound above is independent of the
surrogate. Its normalized potentials are uniformly bounded by the same
spanning-tree argument. A compactness-and-uniqueness contradiction therefore
shows uniform convergence of surrogate states and objectives on every
compact parameter and nomination set.

For each fixed choice of other coordinates and nominations, restrict
to the one varying parameter interval. Each surrogate objective is either
nondecreasing or nonincreasing there. One of these two directions occurs
on an infinite subsequence; a constant function can be assigned either
direction. The uniform limit along that subsequence has the same weak
monotonicity. No derivative of the limiting nonsmooth function is needed,
and no consistency of directions between different coordinate fibers is
asserted.

## Endpoint movement and nomination uncertainty

Take a global maximum over a parameter box. Separate monotonicity lets
one move its first coordinate to an endpoint without decreasing the value.
Global optimality forces equality. Repeat for every coordinate. Every
intermediate point is still a global maximum, so subsequent changes in
monotonicity direction cannot invalidate the argument. The minimum follows
identically.

An arbitrary compact scalar uncertainty set contains its attained minimum
and maximum. Its product is contained in the interval box and contains
all of that box's vertices. The two inclusions and the endpoint optimizer
prove exact equality of extreme values.

For joint uncertainty over any compact set of balanced nominations,
first choose a joint optimizer and keep its nominations fixed during
endpoint movement. This proves the joint-extremum conclusion without
claiming that the nomination-optimized value function is separately
monotone. Additional flow or potential feasibility restrictions are not
part of the statement: filtering out physical scenarios using such
restrictions could make endpoint movement infeasible.

## Signed edge-flow objectives

Once nominations are fixed, net injections into every cactus block are
fixed by cutting its attached components. A bridge flow is consequently
fixed. On a cycle with a coherent orientation, all flow solutions have
the form `x_e=q+c_e`; its physical circulation solves

```
sum_e g_e(q+c_e,theta)=0.
```

This left side is continuous and strictly increasing in `q`. Its
limits at sufficiently large positive and negative `q` have opposite
signs, even when individual laws are bounded. It has a unique root.

A varying parameter outside the target cycle has no effect on its
flows. For one inside, if its coefficient function vanishes at any
root, that same root solves the equation for all parameter values.
Otherwise its sign along the continuous root curve is fixed. For
`theta'>theta`, evaluating the new cycle equation at the old root
changes its value by `(theta'-theta)f(q+c_e)`. Strict increase of
the cycle equation then orders the new and old roots in the opposite
direction. This proves separate flow monotonicity directly for continuous
laws, without needing smoothing. Every cycle edge has the same scalar
circulation change up to its fixed orientation. The same endpoint argument
proves the stated signed-flow hull equality.

## Exact theta obstruction

I independently checked the gadget's flow balances, both cycle equations,
the scalar root equation, and the objective identity, including exact
symbolic arithmetic. With the candidate's edge order and nomination
convention, the four ordinary flows and cross flow give balances
`(4,-4,3,-3)`. The two outer path drops agree identically. The remaining
cycle equation is exactly

```
(12 theta+1)z^2+10z-23=0.
```

For every positive `theta`, its unique positive root lies between zero
and two: the polynomial is negative at zero, positive at two, and
strictly increasing on the nonnegative half-line. Thus all five specified
flows have the assumed positive signs. The terminal drop is

```
pi_0-pi_1=2+(z-1)^2/6.
```

At the two positive rational resistance values `23/108` and `71/12`,
the roots are respectively `3/2` and `1/2`. The reverse pressure
objective equals `-49/24` at both endpoints. At the interior resistance
`1`, its root is one and the reverse objective equals `-2`. The exact
gap is therefore `1/24`. Moreover the positive root decreases strictly
with resistance, so this is the unique interior maximizer on that interval.
This refutes separate monotonicity and the hull property using only one
uncertain resistance.

## Every noncactus simple graph inherits the obstruction

The graph reduction is valid. A connected simple noncactus graph has a
biconnected block that is neither an edge nor a simple cycle. Such a
block contains a theta subdivision. To see this directly, take a cycle.
A chord already supplies the third path. If the block has a vertex
outside the cycle, an outside component has at least two distinct cycle
attachments, since otherwise its unique attachment is a cut vertex.
A path through that component between two attachments, together with
the two cycle arcs, supplies the theta.

At most one of the three branch-to-branch paths can have no internal
vertex, because the graph is simple. Thus two paths have internal vertices
to serve as the objective terminals. Each of their four nonempty segments
can receive positive rational resistances summing to the corresponding
gadget resistance. All inserted vertices have zero nomination, so their
series quadratic resistances add exactly. The third path's fixed
resistances can sum to a rational `d<23/108`, with a single remaining
edge carrying the shifted uncertainty parameter. Both shifted endpoints
and the shifted interior value are positive.

Restore every original edge outside this selected theta subdivision with
a common resistance `M`. Zero nominations at all remaining vertices make
the theta-supported competitor feasible. For each of the three parameter
values, its energy is bounded independently of `M`. Optimality of the
physical flow yields

```
(M/3) sum_(outside theta) |x_e|^3 <= C.
```

Thus every extra-edge flow tends to zero. Theta-edge flows are uniformly
bounded, either by total positive nomination or by their fixed positive
energy coefficients. Normalize a theta potential. Paths within the theta
bound all its other potentials by its bounded flows and fixed resistances.
Potentials at vertices outside the theta need not stay bounded, and the
argument does not require that.

Any convergent subsequence of the theta states satisfies the original
theta balances in the limit, because all omitted incident flows vanish,
and satisfies its constitutive equations. Uniqueness identifies the limit
with the exact gadget state. Every subsequence has that same limit, proving
convergence of the three objective values.

For sufficiently large finite `M`, each error is below `1/96`. The
interior-versus-either-endpoint difference then remains at least
`1/24-2/96=1/48>0`. A sufficiently large rational integer `M` exists.
This proves the claimed graph characterization with rational data.
It is an existence argument and does not assert a polynomial bit bound
on `M`, nor is such a bound needed for this characterization.

## Follow-up audit: polynomially encoded restoration

The author's subsequent quantitative appendix also passes review. It
strengthens the preceding qualitative argument. The feasible `z=1` flow
has outer flows `1,3,3,1` and energy `(10+tau)/3<6` at all three tested
total cross resistances. Thus each extra-edge flow is at most
`(18/M)^(1/3)`. The physical edge-flow bound `14` is conservative: total
positive nomination is only seven, but fourteen remains valid.

The restricted theta flow has induced balanced nomination `b'`. Its
coordinate magnitudes are at most `14 deg_theta(v)`, and restricting
the extra-edge incidence contributions gives
`||b'-b||_1<=2m_extra(18/M)^(1/3)`. The balanced box containing both
nominations has the earlier nomination-Lipschitz theorem's total-load
bound `B=28m_theta`. The chosen objective path has resistance sum `2/3`,
so its Lipschitz constant is `(112/3)m_theta`. Multiplication yields
pressure error at most

```
(224/3)m_theta m_extra (18/M)^(1/3)
 <=75m^2(18/M)^(1/3).
```

With `M=18(10000m^2)^3`, this is at most `75/10000<1/96`.
The explicit integer has `O(log m)` bits. Positive equal resistance
splits on each selected path and the shifted cross-edge endpoints also
have polynomial encoding length. Hence the strengthened restoration
does supply polynomially encoded data; it no longer needs an
unquantified sufficiently large resistance. This supplements the
qualitative characterization without altering its hypotheses.
