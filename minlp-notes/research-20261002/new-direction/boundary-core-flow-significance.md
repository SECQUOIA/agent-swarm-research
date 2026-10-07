# Assessment: boundary-core smoothing with convex integer-flow recourse

Date: 2026-10-02. Scope: significance and limits of the actual
[boundary-flow theorem](smoothed-boundary-core-flow.md), its
[optimal-face certificate](flow-optimal-face-certificate.md), and the
[scoped prior audit](../prior-art/smoothed-boundary-core-flow-prior.md).
The general theorem has passed separate
[full proof](../reviews/smoothed-boundary-core-flow-adversary.md) and
[arithmetic/output](../reviews/boundary-core-flow-bit-adversary.md) reviews.
The sharper [bilinear specialization](smoothed-bilinear-core-flow.md) has
also passed its [independent review](../reviews/smoothed-bilinear-core-flow-review.md).
The [TU extension](smoothed-core-tu-recourse.md), including bounded
inequalities, has passed a [separate interface review](../reviews/smoothed-core-tu-recourse-review.md).
This assessment does not replace those proof reviews or establish
publication priority.

## 1. The added capability is exact core-only smoothing with constrained flows

The draft gives an exact solver for a sampled network MINLP with a small
continuous core and arbitrarily many native integer flow variables. Core
optima may lie on any box face. Native capacities are binary encoded,
the network need not have small width, and ties among exponentially many
flows may persist. Only core linear coefficients are perturbed.

The new certificate addresses a real gap in the preceding interior
theorem. At a boundary optimum there may be no single flow optimal on
any adjacent full-dimensional core box. The certificate represents the
entire optimal-flow set by tightened arc intervals, minimizes each inward
derivative over that set, and controls losing flows by their violations
of those intervals. It can therefore fix the core face before choosing
a flow for whole-core algebraic completion. It does not assume that
small noise isolates an integer label.

The comparisons are:

| Result | Perturbations and residual scope | Boundary and precision distinction |
| --- | --- | --- |
| Native-integer recourse | Core and residual coefficients; a general exact bound-stable integer oracle | Separates a winning label using excluded-label solves |
| Interior-core flow | Core only; convex separable network costs | Requires all optimal cores interior; retains its sharper explicit work and polynomial-in-input sampling-length bounds |
| Present boundary-flow draft | Core only; convex separable network costs | Allows arbitrary faces and ties; uses a larger `f_d(k)` precision and work factor |

The finite law is selected before sampling. Exactness holds on every
atom, including those sent to fallback; only the runtime bound is an
expectation. Output is an integer flow and a small-core common-root
algebraic representation, with an all-draw refinement bound. The full
global proof trace has an expected-size bound, not a uniformly compact
bound on every draw.

## 2. A substantial modeling family, with important boundaries

A useful concrete family is

\[
 F_0(v,z)=\phi(v)+\sum_a\psi_a(z_a)+v^TBz,
 \qquad z\text{ a bounded integer network flow},            \tag{1}
\]

with fixed-degree polynomial `phi` and convex polynomial arc costs
`psi_a`. The matrix `B` may couple every core coordinate to many arcs.
The joint objective can be nonconvex, although every fixed-core flow
problem is convex and exactly solvable. The core upper-curvature bound
comes from `phi` alone: large bilinear coefficients and native capacities
do not increase it. Their encoding and the localization precision remain
in the polynomial input factor. If `phi` is affine or separately concave,
endpoint recourse already gives an exact `2^k`-query method; meaningful
examples of the new search capability need positive core curvature.

There is also a useful aggregate-cost interpretation of (1). For convex
`phi`, put `Phi=phi+indicator_[0,1]^k`. Eliminating the continuous core gives
exactly

\[
 \sum_a\psi_a(z_a)-\Phi^*(-Bz-\gamma).
\]

Thus a low-dimensional aggregate of a constrained integer flow enters
through a concave term. If `phi(v)=v^TQv/2`, with `Q` positive definite,
and every feasible flow and allowed noise have their unconstrained core
minimizer inside the supplied box, this becomes

\[
 \sum_a\psi_a(z_a)-\tfrac12(Bz+\gamma)^TQ^{-1}(Bz+\gamma).
\]

The concave quadratic has rank at most `k`. In general the box instead
gives the clipped conjugate, and core noise induces correlated flow
coefficients after elimination. This is an interpretation of the stated
model, not a capacity-independent theorem for every low-rank concave
quadratic flow problem: enlarging and rescaling the core domain to realize
an arbitrary unrestricted conjugate can put flow capacities and coupling
magnitudes back into `L/sigma`.

The general theorem allows more nonlinear `f_a(v,z_a)` than (1), but its
parameter dependence must be read honestly. The allowed cost `v^2 z_a^2`
on a native interval `[0,U]` can require `L>=2U^2`. Thus capacity magnitude
may re-enter the numerical parameter `L/sigma`. Binary-capacity dependence
is polynomial **at fixed core curvature/noise ratio**, not a guarantee
that every cost model has a capacity-independent ratio.

There is no positive residual strong-convexity modulus assumption. Flat
costs and integer ties are allowed. The stronger premise is that each
arc cost is convex in its scalar flow on its full native real interval
for **every** core point. Convexity only at sampled queries is not enough
for the derivative and chart arguments. The polynomial degree is fixed;
the theorem is not an oracle result for arbitrary black-box smooth costs
or a bound with the same input exponent for unrestricted encoded degree.

The feasible network is fixed. Core variables alter costs, not balances,
supplies, or arc bounds. Ordinary capacity-design or core-dependent-demand
models therefore do not automatically fit. Cross-arc nonlinear costs,
general integer side constraints, and nonconvex arc costs likewise require
a different exact recourse and certificate argument. The interval and
cycle certificate uses network structure, not merely tractability of one
conditional subproblem.

## 3. Small core noise gives controlled original-objective error

Let `(v_gamma,z_gamma)` be an exact optimum of the sampled objective and
let `(v_0,z_0)` minimize the unperturbed objective. On the unit core box,

\[
 0\le F_0(v_\gamma,z_\gamma)-F_0(v_0,z_0)
 \le\gamma^T(v_0-v_\gamma)\le k\sigma.                     \tag{2}
\]

This bound is independent of native flow widths because those
coefficients are not perturbed. More explicitly, if `m_gamma` is the
sampled optimal value and `B_gamma=sum_i max(gamma_i,0)`, then

\[
 [\,m_\gamma-B_\gamma,\ F_0(v_\gamma,z_\gamma)\,]            \tag{3}
\]

contains the original optimal value and has width at most `k sigma`.
The algebraic output can be refined to a rational feasible core and
certified intervals with any requested additional error. The residual
flow stays exactly feasible because its constraints do not depend on
the core. This does not assert recovery of the unperturbed optimizer or
its integer label.

Weak noise is not free: substituting `sigma` of order `epsilon/k` in the
expected work factor gives inverse-accuracy dependence of order
`(1+O(k^2 L/epsilon))^k`, in addition to `f_d(k)` and input factors.
It is not logarithmic-accuracy exact optimization of the original problem.
An inverse-polynomial noise scale gives fixed-`k` polynomial work and a
small additive original-objective error, without an empirical speed claim.

This is also not the first additive approximation mechanism for the model.
A deterministic full core grid and exact recourse already give objective
error at most `kLh^2/8` from the same coordinate-curvature interpolation.
At fixed dimension this uses roughly `(1+sqrt(kL/epsilon))^k` grid tuples,
potentially a better inverse-accuracy exponent. The present gain is exact
optimization of a single sampled instance, with only small core
perturbations, ties preserved, and a capacity-independent regret bound
when the model has a capacity-independent `L`.

## 4. What is proved, plausible, and still needed for use

The drafted proof establishes its conditional expected-FPT statement
through exact certificates, a base-only finite sampling budget, and a
same-draw fallback. Its chart universe can be exponential, but is used
only to choose bounds; the ordinary algorithm does not enumerate it.
The prior audit appropriately separates this from enumerating a full
parametric-flow envelope, which need not be small even with one core
parameter. The classical flow oracle and optimality ingredients are not
new results of this investigation.

The reviewed bilinear specialization restores the sharper work factor
`[8^k Q+c_d^k] poly(I)` and polynomial-in-input sampling length. Its
adjusted chart marginals are affine in the core, extrema over a box are
computed at endpoints, and inward-derivative recourse costs are linear.
A direct rational coefficient bound replaces the general polynomial
chart-margin elimination. This sharper conclusion is specific to the
bilinear cost structure; it is not asserted for all polynomial costs.

The reviewed TU extension supplies a second concrete advance. Its compact
adjacent-slope dual, exact optimal-coordinate intervals, and conformal
unit-circuit proximity replace the network potentials and cycle argument.
It allows fixed TU equalities and fixed TU inequalities on finite native
boxes, the latter through explicitly bounded zero-cost slacks. Consecutive-
ones resource matrices give a natural application: each integer activity
uses an interval of an ordered resource list, with fixed requirements or
capacities. This describes a useful TU input format, not a claim that
such interval models have no equivalent network representation. The
extension still excludes arbitrary integer side constraints and core-
dependent feasibility.

A particularly direct model takes `phi(v)=||v||^2/2`. Eliminating the unit
core gives separable convex native costs plus

```
sum_(j=1)^k rho((Bz)_j+gamma_j),
rho(s) = 0             if s>=0,
         -s^2/2        if -1<=s<=0,
         s+1/2         if s<=-1.
```

This is an exact model of `k` concave clipped-quadratic aggregate costs
over the bounded TU integer set. Only the aggregate shifts are randomly
perturbed. Here `L=1` for every `B` and every capacity: clipping makes the
interpretation valid without an interior-range premise or enlargement
of the core box. The unrestricted negative-quadratic interpretation above
still needs its separate range qualification.

There is no production implementation or performance evidence in the
draft. The small exact diagnostics test certificate soundness and failure
guards. A usable implementation still needs a genuine polynomial-time
convex-cost flow routine with binary capacities, exact potential and
interval extraction, rational polynomial identity/sign tests, a certified
small-core algebraic solver, and controlled arithmetic at the required
precision. Repeated one-unit augmentation or exhaustive fixture-label
enumeration does not supply the promised general oracle.

The bounds on chart margins and the worst-case cutoff may be extremely
conservative. An implementation can stop as soon as its exact certificate
passes, but practical calibration of `L`, the perturbation scale, and
arithmetic precision remains necessary. Theoretical fixed-parameter
tractability alone does not show that these bounds are numerically useful
for a particular network instance.

The clearest research advance is therefore a broader exact certificate
for constrained integer recourse under core-only smoothing, including
boundary optima. The main remaining questions are implementing and
calibrating that certificate, extending the reviewed specializations and
identifying further constrained recourse classes with comparable optimal-set
certificates. None of these conclusions requires a general novelty or
hardness claim.

## Verification record

This assessment read the full boundary theorem, deterministic certificate,
and scoped prior audit. It independently derived (2)--(3), checked the
curvature/capacity counterexample, conjugate interpretation, and endpoint-
grid approximation baseline,
and distinguished the general parameter factor from the now-reviewed
affine-chart specialization. A subsequent actual-file TU review checked
the equality interfaces and finite-slack inequality reduction. The clipped-
quadratic formula follows by minimizing each scalar quadratic on `[0,1]`. Mathematical and arithmetic
review status is reported as of the reading, not inferred from the
existence of an author diagnostic. A scoped inline Python check passed
for local links, math delimiters, whitespace, and control characters.
No external search, project-wide checks, CI inspection, or index edits
were performed.
