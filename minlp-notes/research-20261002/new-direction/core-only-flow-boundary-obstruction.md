# A boundary obstruction to uniform-label closure under core-only noise

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/core-only-flow-boundary-obstruction-review.md).
This is a limitation of one proposed closure mechanism, not a
hardness result for core-only smoothing or network optimization.

The [native-integer recourse theorem](smoothed-native-integer-recourse.md)
perturbs both the continuous core and integer residual costs. A proposed
follow-up would perturb only the core, allow persistent residual ties, and
certify a chosen flow throughout a small core box by polynomial residual-cost
potentials. Core-boundary optima obstruct that test even with constant
curvature and strong projected growth.

## 1. A two-arc example

Let `v=(v_1,v_2)` range over `[0,1]^2`. Send one integral unit through two
parallel arcs, so the feasible residual labels are

```
Y={(1,0),(0,1)}.
```

Consider the convex-in-core quadratic

```
F_gamma(v,z)=.5(v_1^2+v_2^2)+gamma_1 v_1+gamma_2 v_2
              +v_1 z_1+v_2 z_2,
V_gamma(v)=.5||v||^2+gamma'v+min(v_1,v_2).                  (1)
```

The residual costs are linear, hence separable convex. The continuous core
changes only costs, not flow feasibility. The coordinate upper curvature is
`L=1`, all fixed coefficients and capacities are bounded, and the core
dimension is two.

Perturb only `gamma_1,gamma_2`, independently and uniformly on the `M`
equally spaced points of `[-1,1]`, with `M>=4` a power of two. The event

```
E={gamma_1>=1/2, gamma_2>=1/2}                              (2)
```

has probability exactly `1/16`: each upper half-interval contains exactly
`M/4` atoms. Its probability does not shrink when the sampling grid is made
finer.

On this event, the unique optimal core point is the origin. In fact

```
V_gamma(v)>= (.5+min_i gamma_i)||v||^2,                     (3)
```

because `v_i>=v_i^2` on the unit interval and `min(v_1,v_2)>=0`.
Equality of the best possible growth constant is attained at a unit
coordinate vector whose noise coefficient is least. Thus projected core
growth is `g=.5+min_i gamma_i>=1`, and `L/g<=1`. Both residual labels are
optimal at the origin. Full point growth at one mixed optimizer fails,
but that is exactly the persistent-tie setting the proposed extension seeks
to allow. Growth to the full optimal set still has the constant in (3),
since for each feasible flow its matching origin point is optimal and the
distance to that set is exactly the core norm.

## 2. No full core box admits a uniformly optimal label

Let `D=[0,a] times [0,b]`, where `a,b>0`, however small. At `(a,0)`, the
unique optimal flow is `(0,1)`; at `(0,b)`, it is `(1,0)`. The core-only
linear perturbation cancels from these label comparisons. Consequently no
single flow is optimal throughout `D`.

This also rules out every valid polynomial-potential certificate for such a
flow on that box, independently of how the potentials are represented. For
the candidate `(1,0)`, the residual cycle changing the flow to `(0,1)` has
cost `v_2-v_1`, which is negative at `(a,0)`. The other candidate has reverse
cycle cost `v_1-v_2`, negative at `(0,b)`. Potential terms cancel around
these cycles, so no choice of potentials can make all reduced costs
nonnegative throughout `D`.

The equality of the two core cost polynomials at the origin is caused by a
boundary face. Their ambient normal gradients differ there, even though
the origin remains optimal on the positive-probability event (2).
A claim that generic optimal core points avoid every chart boundary cannot
ignore this possibility. Restricting to the zero-dimensional core face
does not by itself justify a certificate on a full adjacent core box.

## 3. The corrected-grid search does not remove the obstruction

At dyadic side length `h>0`, the origin cell `[0,h]^2` has least corner
value zero, which is the exact global optimum on `E`. Its corrected lower
bound with `e=kLh^2/8=h^2/4` is `-h^2/4`. Hence it survives every level
of the core search used in the native-integer theorem. The retained core
hull therefore has positive width in both coordinates and contains this
cell. No uniformly optimal flow certificate can pass on that hull at any
finite refinement depth.

This is not the zero-curvature endpoint special case: `L=1`. The optimizer
and projected growth are already well behaved. The failure comes from
using one residual label on a full box around a boundary core optimum.

To see why the same rare-fallback calculation cannot simply be reused,
replace the network by a chain of `m` stages, each containing two parallel
unit-capacity arcs and carrying one integral unit. Only the first stage has
the costs in (1); all later arc costs are zero. There are exactly `2^m`
feasible integer flows, with input length `O(m log(m+1))` apart from the chosen
noise bits. The conditional value (1), its growth, and the closure failure
are unchanged. A strategy that insists on the uniform-label test and then
literally enumerates all residual labels at its cutoff does `2^m` fallback
work on an event of probability `1/16`.

Thus that particular proof and fallback strategy cannot have the desired
expected FPT bound under core-only noise. The example is itself easy:
the origin and any flow are globally optimal on `E`, as (3) certifies.
No general computational lower bound, nor a barrier to other exact
certificates, follows from it.

## 4. What a positive follow-up still needs

A theorem assuming a verified interior location for all optimal core points
avoids this particular boundary obstruction. A general result would instead
need a sound certificate fixing the relevant core face or a lower-bound
certificate that combines several optimal labels near the boundary.
Exact polynomial sign tests for one flow's reduced costs alone do not
provide either step.

The subsequent [optimal-flow face certificate](flow-optimal-face-certificate.md)
provides the second route by using all tied flows and controlling losing
flows. Its [core-only smoothing theorem](smoothed-boundary-core-flow.md)
handles arbitrary core faces. This does not invalidate the narrower
single-label obstruction above.

The main all-coordinate-noise theorem remains unaffected. Its full growth
event separates competing integer labels, and its bound-restricted recourse
test verifies that separation before completing the continuous core.

## Verification

The formulas above passed the [independent analytical review](../reviews/core-only-flow-boundary-obstruction-review.md),
including the exact atom probability and the strategy-specific scope.
The later [boundary-search diagnostic](check_boundary_core_flow_search.py)
tests all 64 atoms of an eight-point two-dimensional noise law, including
the example here and its closure by the new face certificate. The reviewer
did not rerun that author-side diagnostic. Scoped document checks passed;
no general optimizer or external literature search was needed for this
diagnostic.
