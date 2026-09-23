# Audit: finite-resistance flow realization and existential capacity design

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I checked
[the discrete flow-realization candidate](potential-flow-discrete-flow-realization.md).
The prescribed-flow Subset-Sum observation arose during this reviewer's
preceding flow-region audit; the author developed the directed positive
target, capacity-design, and precision-gap formulation here. This record
checks that complete proof and its extensions. A separate agent's audit
provides review independent of that original observation. No novelty is
assigned to the elementary discrete-linear-feasibility mechanism.

## Prescribed-flow feasibility and NP certificates

For a given rational flow, conservation is checked first. Its signed
quadratic basis values are then known rationals. With interval
resistances, the equations
`A^T pi=diag(x_bar|x_bar|)beta` and the rational interval bounds are a
linear feasibility system. One potential reference per connected
component removes irrelevant constants. Zero flow on an edge imposes
zero potential difference there, which is handled correctly. No bound
on cycle rank is needed for this LP statement.

For finite sets, the certificate consists of one explicitly listed
option index for each uncertain edge. All resulting target drops are
rational, and checking that they are potential differences is rational
linear algebra. Their total bit length remains polynomial. Since the
target itself is prescribed rational data, there is no need to certify
an irrational physical state. Feasible target equations characterize
the actual unique passive state. This proves NP membership on arbitrary
graphs within the stated positive-resistance model.

## Single-cycle reduction

The long path and the direct arc are both oriented from source to sink.
For `n>=2`, they form a simple cycle with `n+1` vertices and `n+1`
edges. Every vertex has degree two. This orientation is acyclic; the
existence of an undirected cycle does not imply a directed one.

The all-one target flow has source nomination two, sink nomination minus
two, and zero elsewhere. Its two source-to-sink drops are

```
theta=n+sum_i a_i sigma_i,  D=n+K.
```

Equality is exactly the target subset equation. All target flows are
positive, all resistances are positive integers, and every uncertain
edge has two distinct options. The fixed direct resistance is permitted.
No operating bounds or additional nominations are used to obtain this
equivalence.

The fixed preprocessing triangles are correct. Two long-edge choices
`{1,2}` permit total three and hence realize the target with direct
resistance three. Choices `{1,3}` on both long edges give only totals
two, four, or six, so the same direct resistance yields a no instance.
They preserve the simple cycle, all-one target, and fixed nominations.
Small `n` and immediately decided target cases can therefore be handled
without leaving the claimed class. NP-hardness and the rational
certificate establish NP-completeness.

## Existential unit capacities

For every resistance selection, conservation gives one flow `p` on the
long path and one flow `z` on the direct arc, with `p+z=2`. Their common
potential difference has the same sign as each passive path flow. Both
flows are therefore strictly positive. The capacities `p<=1`, `z<=1`
then hold exactly when `p=z=1`. The conclusion is unchanged for
absolute-value capacities.

Thus an existentially capacity-feasible selection is precisely a target
realization. For the broader fixed-nomination single-cycle capacity
problem, guessing the finite resistance options leaves a scalar
strictly increasing piecewise-quadratic cycle equation. Sorting its
rational breakpoints and solving its relevant quadratic or linear piece
gives an exact degree-at-most-two flow encoding. Every rational capacity
comparison is polynomial. This proves the stated NP membership without
claiming it for arbitrary-rank nonlinear capacity design.

This existential problem differs from robust validation. Testing that
all scenarios obey all capacities can use independent worst-case
single-arc computations, but those computations do not find one scenario
that obeys every capacity simultaneously.

## Precision gap

The displayed long-path flow

```
p=2sqrt(D)/(sqrt(theta)+sqrt(D))
```

satisfies `theta p^2=D(2-p)^2` and lies strictly between zero and two.
Rationalizing its displacement from one gives exactly

```
|p-1|=|D-theta|/(sqrt(D)+sqrt(theta))^2.
```

In a no instance the numerator is a positive integer. Both `D` and
`theta` are at most `M=n+S+K`, so their denominator is at most `4M`.
The lower bound `|p-1|>=1/(4M)` follows with the stated direction.

Because `z=2-p`, maximum arc load equals `1+|p-1|`, and maximum
absolute deviation from the all-one target equals `|p-1|`. The
corresponding yes optima are one and zero; no optima are separated by
at least `1/(4M)`. These functions are convex in the flow vector,
but the attainable finite-scenario set is not convex. The gap has
polynomial binary length and supports the claimed hardness for
polynomial dependence on requested accuracy bits. It supplies no
fixed-normalization constant-error or strong-hardness conclusion.

## Interval relaxation and convexification

After taking the interval hull of every uncertain set, the long-path
total resistance ranges continuously over `[n,n+S]`. For every
nontrivial source instance `0<=K<=S`, the desired value `n+K` is
available. Thus all such interval instances realize the target,
including no instances of the finite problem. The target lies in the
cactus interval flow region and hence in the finite-scenario convex
hull, while it need not be an actual finite scenario.

For a convex capacity set, containment of every scenario is equivalent
to containment of its convex hull. Intersection with that set has no
such equivalence. This explains precisely why the positive robust
validation and flow-hull statements coexist with this existential
hardness. The corrected membership scope of the flow-region theorem
is appropriate.

## Exact checks and conclusion

I checked the physical equal-drop equation and rationalized deviation
identity symbolically, verified both preprocessing triangles by exact
integer enumeration, and checked 1,008 deterministic cycle/target/gap
cases with `2<=n<=7`. All passed. These checks supplement the explicit
proof and are not a numerical network-design algorithm.

The theorem consistently distinguishes exact target realization,
existential capacity design, robust validation, and interval membership.
No substantive defect remains in the stated construction or extensions.
