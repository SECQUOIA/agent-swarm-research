# Independent composition review: sparse monotone implicit graphs

Date: 2026-10-02. Verdict: **PASS** for the actual
[main theorem](../new-direction/smoothed-implicit-graph-constraints.md)
and its [oracle interface](../new-direction/implicit-graph-oracle-interface.md).
This review checks their composition and output meaning. It does not
establish priority or practical performance, and does not replace the
separate oracle and KKT/tail reviews.

## Parameterization, factor scopes, and noise

The full-real-hull bracket and positive derivative assumptions give one
dependent scalar root for every retained vector. Each equation depends
only on its own dependent coordinate and its retained support. The reduced
feasible domain is therefore exactly the mixed product box; no outside
feasibility condition depending on a queried bag is silently introduced.
Dependent roots at their interval bounds are legitimate: the implicit
function theorem still gives local smooth extensions, and those intervals
select the chart rather than impose additional retained constraints.

Replacing a dependent variable's entire bag subtree by its retained
support preserves running intersection. For each added retained variable,
that subtree meets its original subtree in a bag containing the constraint
scope. Unions of these connected subtrees remain connected. Original
factor assignments remain valid after their scope expansion, and the
stated `p'<=p max(1,k)` bound is conservative but sufficient.

Conditioning on all dependent noise is essential and valid. Retained
linear coefficients remain independent with their original finite law.
The reduced nonlinear function and its upper-curvature bound are then
fixed relative to them. All numerical bounds and sampling budgets are
uniform over dependent noise in its base support, so this conditioning
does not create a draw-dependent resolution or stopping budget.

## Approximate tables preserve a true global witness

Independent retained-coordinate rounding followed by the exact chart is
feasible. Shared dependent roots need not have identical rational
approximations in different bag evaluations: every certified row interval
contains the same exact graph value. Each assigned factor is counted once,
so summing row intervals gives `G-D<=H^-<=G`, with `D<=E`.

The lower-cost DP is exact rational arithmetic. Fixed-cell rounding gives
`LB_C=q_C^- - E` as a valid lower bound; an incumbent `m^-+D` is a
certified upper bound at the backtracked implicit feasible point. Thus a
retained cell has one globally consistent witness satisfying

```
G(witness)<=q_C^-+D<=U+E+D<=f*+2E+2D<=f*+4E.
```

This is the precise bridge to the probability count. Separate near-optimal
bag witnesses would not suffice. The original-domain conditional value
function used in that count is independent of the in-bag retained noise;
it is not defined using the adaptively retained domain. Hence adaptive
pruning does not invalidate independent multiplication of the coefficient
interval probabilities. The factor `1+n` follows from the tolerance `4E`.

## Closure and the finite-law budget

Certified gradient and Hessian errors are included twice where necessary:
once for the rational approximation and once when transporting from the
midpoint to the optimizer or patch. At the displayed cutoff, the gradient
enclosure has error at most `3 tau/4` from an active optimal derivative.
After the active original retained bounds and integer labels are fixed,
the remaining optimum is interior in its original continuous coordinates.
Point growth then gives reduced Hessian at least `2g_0 I`. The matrix
test retains slack at least `g_0/4`. The test itself is sound even when
the probabilistic good event fails.

The active-gradient KKT system has `k+2m` unknowns. Positive diagonal
`q_y` gives full constraint row rank. Its nullspace reduction is the true
reduced Hessian, so positive point growth makes the relevant polynomial
root nonsingular. The free equations do not involve the coefficient of
the fixed active coordinate; the remaining derivative has slope one in
that coefficient. This justifies the root-count/interval argument even
when other stationary components are singular or positive dimensional.
It is an intersection bound with positive growth, not conditioning on
that event.

The original polynomial graph, not the reduced algebraic function, is
passed to the scalar quantifier-based fallback. Degree remains fixed,
compactness is explicit, and the two quantified blocks merely gain the
dependent coordinates. Thus the already-reviewed base-factor/precision
separation applies. All cutoff constants precede the choice of `M`;
actual dependent-noise heights enter only polynomial bit factors.
The two failure events each have probability at most `rho`, uniformly
conditional on dependent noise. The same-draw fallback budget therefore
has the claimed expected cost.

## Exact feasibility and useful implicit output

Root brackets, implicit derivative intervals, and rational DP comparisons
avoid exact comparison of general algebraic objective values. The weak
separator on the accepted convex epigraph uses a valid affine lower
function, with both value and gradient errors charged. The GLS cleanup
allocates additional error to the algebraic feasible value; it does not
pretend that this value is rational.

An exactly feasible returned point consists of rational retained
coordinates and their unique scalar-root equations. Rational coordinate
enclosures alone are not asserted to satisfy the nonlinear equalities.
The chart's finite Lipschitz bound turns retained accuracy into ambient
accuracy with polynomially many extra bits. The same reconstruction is
used after fallback. This is a substantive exact-output contract rather
than an unimplemented exact-real oracle assumption.

## Significance and limits

Compared with the polynomial box theorem, the reduced objective may be
algebraic and the physical feasible set curved. The composition preserves
original-coordinate independent noise and exact nonlinear equality
feasibility. It therefore adds more than explicit polynomial substitution.
The inverse cubic actuator is a useful example: retained states and binary
modes can be chosen freely, and the dependent control is the unique
bounded solution of a local monotone equation. Its brackets hold even
when the binary coordinate is relaxed to its full interval.

The restriction is nevertheless strong: the model assumes a globally
valid product-domain parameterization with one selected inverse branch.
It does not handle arbitrary overlapping resource constraints, dependent
integer variables, or multiple branches. The relevant curvature is that
of the reduced objective. Poor inverse conditioning can enlarge it, and
dependent-coordinate noise itself contributes nonlinear retained
curvature. Increasing the noise scale therefore need not decrease `L/sigma`
without a residual geometry-dependent term. The theorem states its bound
using the actual uniform reduced `L`, so it does not hide this cost.

## Verification record

The reviewer read both actual artifacts in full and checked the displayed
inequalities, conditioning order, graph replacement, and output contract
directly. The local cubic brackets were checked algebraically:
`u+u^3+s/4+z/2-s_next` has derivative at least one, lower-endpoint value
at most `-8.25`, and upper-endpoint value at least `8.75` on the stated
boxes. No independent optimizer or DP diagnostic was run by this reviewer;
the main author owns the separately planned bracket/DP implementation.
No external source search, project-wide check, CI inspection, or index
edit was performed.
