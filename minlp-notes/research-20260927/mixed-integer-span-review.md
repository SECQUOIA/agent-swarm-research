# Independent review of the mixed-integer Hessian-span consequence

Date: 2026-09-27. Reviewer: `mixed_integer_span_review`.

The compact rational LP approximation route is sound, conditional on the
native-Hessian-span value bound proved and separately reviewed in
[the value note](hessian-span-reduction.md) and
[its review](hessian-span-review.md). It avoids a delicate mixed-integer
weak-oracle invocation. The useful conclusion is stronger than fixed-integer-
dimension feasibility: for fixed continuous Hessian-span dimension, one obtains
a polynomial-size MILP with the same feasible integer projection and with no
new integer variables. The LP's continuous coordinates need not be exactly
feasible for the quadratic system.

This review began before the author's draft was available. The author supplied
the proposed sawtooth route; I checked it independently, located direct prior
art, and identified the stronger integer-projection conclusion. Thus the
projection formulation was developed in discussion, not reviewed in isolation.
I subsequently reread the complete
[author's draft](mixed-integer-span-frontier.md), including its additional
optimal-integer-assignment recovery argument. No substantive gap was found;
the conditional qualification concerns the separately reviewed value theorem.

**Hypotheses and uniformity.** Let the original variables be
`(z,x) in Z^k x R^n`, with explicit finite rational coordinate bounds, rational
affine constraints, and rational quadratic inequalities `q_i(z,x) <= 0`.
Every quadratic must be jointly convex in `(z,x)`. Let `h` be the rational
linear-span dimension of the continuous Hessian blocks `Q_i,xx`.

For any allowed integer vector `z`, substitution produces a convex quadratic
system of bit length bounded by one polynomial in the original input length
`N`, uniformly in `z`: its coordinates have polynomial bit length because
the supplied bounds do. Define `v_z(x)` as the maximum of zero and all native
and affine violations, including both signs of affine equalities, over the
original continuous coordinate box. Its minimum `alpha_z` is attained.
The epigraph objective is linear, the epigraph's native continuous Hessian
span is at most `h`, and a rational upper bound for `v_z` supplies its missing
epigraph-coordinate bound. The value theorem therefore gives one effective
threshold

```
alpha_z = 0  or  alpha_z >= Delta = 2^(-N^{C(h+1)})
```

for all allowed integer vectors, with a sufficiently large universal constant
`C`. No union bound or enumeration of integer vectors is required. The
epigraph problem is nonempty even if the original fiber is infeasible, so the
nonemptiness assumption of the value theorem causes no circularity.

An asymptotic effective bound suffices for an existence theorem about an
algorithm: a universal constant can be fixed once from the quantitative
elimination estimates. A practical implementation still needs a concrete,
usable bound. Merely observing a large gap in numerical examples would not
supply this uniform threshold.

**The continuous lift.** Put `T(s)=min(2s,2(1-s))` on `[0,1]` and

```
V_m(s) = sum_{j=1}^m 4^(-j) T^j(s),
F_m(s) = s - V_m(s),
eta_m = 4^(-(m+1)).
```

`F_m` is the affine interpolation of the square on the dyadic grid of mesh
`2^(-m)`. On a cell `[a,b]` its error is exactly `(s-a)(b-s)`, so
`0 <= F_m(s)-s^2 <= eta_m`. Consequently `F_m-eta_m` is a convex lower
approximation of the square with error at most `eta_m`.

The chain

```
g_0=s,
0 <= g_j <= 2g_{j-1},
g_j <= 2(1-g_{j-1})     (j=1,...,m)
```

uses continuous variables only. Its projection together with
`t >= s-sum_j 4^(-j)g_j-eta_m` is exactly
`t >= F_m(s)-eta_m`.

Here is the important adversarial point: the upper bounds alone do not force
`g_j=T(g_{j-1})` for an arbitrary feasible chain. One must prove that this
chain maximizes the discounted sum when all upper bounds are tight. The
Lipschitz constant of `V_r` is at most
`sum_{j=1}^r 4^(-j)2^j = 1-2^(-r)`. Thus the function
`u+V_{r}(u)` is strictly increasing. Backward induction proves that every
optimal first choice is `u=T(s)`, and the tail repeats this argument. This
proves the projection identity, including all feasible nonsaturating chains.
Writing an equality for the chain without this argument would be a gap.

This lift is established approximation technology. In particular,
[Beach, Burlacu, Bärmann, Hager, and Hildebrand (2024), Definition 6 and
Proposition 2](https://link.springer.com/article/10.1007/s10589-023-00543-7)
give a continuous sawtooth epigraph relaxation using the same chain and
several shifted levels. Their stronger version has error `2^(-2m-4)`.
The present single-level version is sufficient and has a short independent
proof. Neither the tent interpolation nor its logarithmic-size LP epigraph
should be claimed as a new contribution.

**Rationality and bit lengths.** A rational PSD matrix has a rational
weighted-square decomposition obtained by symmetric rational elimination:

```
q(u) = affine(u) + sum_j d_j l_j(u)^2,   d_j >= 0,
```

with at most the ambient dimension many forms. Determinant bounds give
polynomial coefficient bit lengths. Square roots of eigenvalues or irrational
Cholesky entries are unnecessary. Singular matrices require skipping a zero
PSD pivot and its zero row; alternatively use a rational symmetric pivoting
implementation. A zero row must not be divided by.

For a rational interval `l_j(u) in [a,b]`, write
`l_j(u)=a+(b-a)s`. Then

```
l_j(u)^2 = (b-a)^2 s^2 + 2a(b-a)s + a^2.
```

Only the square is approximated. The error is at most
`d_j(b-a)^2 eta_m`, regardless of the sign of `a` or of the form's values.
Forms constant on the box can be handled exactly; dividing by `b-a=0` is
unnecessary. Sum these weights to allocate a common depth or individual
depths so that the total error per row is at most `epsilon < Delta`.
Every needed depth is polynomial in `N+log(1/epsilon)`.

There are polynomially many square terms before approximation. Depth `m`
uses `O(m)` variables and rows, and each dyadic coefficient has `O(m)`
bits. Even the total `O(m^2)` coefficient storage remains polynomial in
`log(1/epsilon)`. Together with the uniform gap, the full rational LP has
encoding length `N^{O(h+1)}`. All new variables are continuous. Enlarging
the input box or relaxing the affine rows is unnecessary.

Full joint convexity is used here, not just in an oracle convenience: the
full matrices must have nonnegative weighted-square decompositions. A
continuous PSD block alone does not justify this construction. For example,
`q(z,x)=zx` is affine in each continuous fiber and hence has continuous
Hessian span zero, while its full Hessian is indefinite and its graph has
no exact continuous LP lift. This example diagnoses the proof limitation;
it is not a hardness theorem for every possible slice-convex extension.

**Exact integer projection and output.** For each quadratic construct a
lower approximation `q_i^-` satisfying, throughout the original box,

```
q_i^- <= q_i <= q_i^- + epsilon.
```

Keep the affine constraints and bounds exactly, and require each lifted
`q_i^- <= 0`. Every truly feasible point admits the lift. Conversely, an
integer vector `z` occurring in the lifted MILP has a continuous witness
whose original row violations are at most `epsilon`; hence
`alpha_z <= epsilon < Delta`, forcing `alpha_z=0`. Therefore the original
and lifted systems have exactly the same feasible integer vectors.

This implication does not require `k` to be fixed. Fixing `k` permits
polynomial-time exact MILP feasibility using the established fixed-integer-
dimension algorithms. A returned integer vector has an exactly feasible
original fiber. The returned rational continuous coordinates can violate
the original quadratics slightly. The irrational singleton in the value
note shows why the latter caveat is necessary, rather than a proof defect.

The equality is between integer projections, not between full feasible sets
or their convex hulls. In particular, the construction does not produce a
small LP description of the integer hull. It does preserve optimization of
any linear objective depending only on the original integer variables.
An objective depending on continuous variables needs a separate value or
threshold argument; the feasibility lift by itself does not preserve it.

**Optimal integer assignment recovery.** The author's additional argument
supplies that separate result for a jointly convex quadratic objective.
A rational objective-threshold row enlarges the continuous Hessian span by
at most one, so the construction decides threshold feasibility exactly.
For a feasible integer fiber, the value theorem itself bounds its optimum's
annihilator using only the original native Hessian span; it does not count
the objective Hessian.

If `P` and `Q` are nonzero integer annihilators with degrees at most `D` and
coefficient bits at most `H`, then

```
R(t) = Res_u(P(u), Q(u-t))
```

is nonzero. Over the complex numbers it is, up to a nonzero constant, the
product of `alpha-beta-t` over all pairs of roots with multiplicity. Shared
roots of `P` and `Q` produce powers of `t`, not an identically zero
resultant. Its degree is at most `D^2`. Expanding `Q(u-t)` costs at most
`O(D)` extra bits per coefficient, and the Sylvester determinant gives
coefficient bits `O(DH+D^2+D log D)`. After removing powers of `t`, a
reciprocal Cauchy bound separates every nonzero root difference from zero.
This is uniform over all integer fibers without finding their polynomials.

Consequently distinct slice optima are separated by
`sigma=2^(-N^{O(h+1)})`. Initialize threshold bisection using a strict lower
bound, for example `a=-M-1`, and upper bound `b=M`, where the objective's
absolute value over the box is at most `M`. Preserve
`a < theta* <= b`. Once `b-a < sigma`, any exactly feasible integer fiber
returned at threshold `b` is optimal: a larger slice optimum would differ
from the global optimum by at least `sigma`.

The threshold oracle has to use the longer threshold's encoding size when
choosing its own precision. The draft correctly claims only polynomial
time for fixed `k,h` here; naively substituting a threshold of length
`N^{O(h+1)}` into another such bound can give an exponent quadratic in
`h`, so repeating the sharper feasibility exponent without further work
would be unjustified. This procedure outputs an optimal integer assignment,
not an exact algebraic continuous optimizer or its minimum polynomial.

**Older results and significance.**
[Del Pia, *Convex quadratic sets and the complexity of mixed integer convex
quadratic programming*, Theorem 3](https://arxiv.org/abs/2311.00099)
already gives exact optimization with fixed-parameter tractability in the
integer dimension for a jointly convex quadratic objective over a rational
mixed-integer polyhedron. Rational threshold feasibility therefore covers
one convex quadratic inequality plus arbitrary affine rows. It does not
state the many-quadratic, bounded continuous-Hessian-span result. Its
stronger exact optimizer output in its own class must be acknowledged.

[Khachiyan and Porkolab (2000), Theorem 1.2](https://doi.org/10.1007/s004549910014)
allows a convex set defined by a quantified semialgebraic formula, but its
polynomial-time specialization fixes the total free and quantified
dimension. Substituting all growing continuous coordinates as existential
variables does not directly supply the present bound. I read the local
full text `literature/papers/khachiyan2000-integer-optimization-on-convex-semialgebraic/fulltext.md`.

The added contribution, if the span theorem survives wider review, is the
parameter-controlled threshold that turns established outer approximations
into exact discrete representations. The approximation technology and
fixed-integer-dimension MILP algorithms are prior work. This yields a
credible theoretical capability, but no practical approximation depth or
solver speedup has been established. Search queries on mixed-integer convex
quadratic complexity, few quadratic constraints, Hessian span, and sawtooth
epigraphs did not identify an identical stated theorem; this is a limited
search and does not establish priority.

**Audit of the earlier oracle route.**
[Basu, arXiv:2110.06172v6, Theorem 5.8](https://arxiv.org/pdf/2110.06172v6)
provides an alternative weak mixed-integer optimization route. I inspected
the source's model definitions, Theorems 5.7--5.8, and surrounding remarks.
The theorem needs a full-dimensional ball centered at a mixed-integer point
in an optimal fiber, not merely the fiber-only interior condition used
earlier in its Definition 4.1. Its bit-rounding discussion refers to the
established ellipsoid literature rather than giving every estimate.

For an application to the violation objective on a product box, eliminate
fixed continuous coordinates. Tighten each integer coordinate interval to
its integer endpoints first, and then pad those endpoints by `1/4`. The
padding preserves exactly the allowed integers and supplies a full-space
ball around a continuous box center in every allowed integer fiber. Padding
raw rational bounds can add an integer: `[1/10,1]` padded by `1/4` admits
zero. Nonlinear and affine row constraints belong in the violation objective,
not in the hard domain for this argument. Rational quadratic evaluations
and active-piece subgradients have polynomial bits in the query length.
These repairs make the route plausible, but the explicit LP reduction is
more transparent and is the route approved by this review.

**Targeted verification.** Ran

```
python research-20260927/check_mixed_integer_span_review.py
```

All checks passed, including after extending the targeted script for the new
optimization claim. Exact `Fraction` arithmetic checked interpolation values,
sharp midpoint errors, tail-slope bounds, and tangent identities on all 511
dyadic cells through depth eight, and signed-interval normalization on 774
exact samples. SymPy checked root-difference resultants for two different
quadratics, an identical pair with shared roots, and a repeated-factor case.
These finite checks challenge the indexing, sign, scaling, and resultant
formulas. They do not prove the general induction, the quantitative value
bound, general coefficient-height estimates, matrix-elimination complexity,
or Lenstra's theorem. No
floating-point solver result is used as proof. No Lean build, project-wide
checks, or CI inspection was performed.
