# Certified screening from feasible graph samples

A convex combination of feasible graph samples gives an upper bound on the
violation of every suitably normalized support cut at the current relaxation
point. This permits skipping expensive support certification when the bound
is already below the activation threshold. The sampled direction LP supplies
the weights; screening does not solve another optimization problem.

The mathematical ingredients are standard convex combinations, dual norms,
and separation; this is an implementation certificate, not a new convex-duality
theorem. Background is in Boyd and Vandenberghe's
[*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/), on separation
and dual norms. The complete argument needed here follows.

Let \(D\) be the declared block domain and \(g:D\to\mathbb R^k\) its graph
coordinate map. Coordinates can include source variables and multiple
nonlinear features. Write \(C=\operatorname{conv}g(D)\), let \(p\) be the current
relaxation point, and choose positive coordinate scales \(s_1,\ldots,s_k\).
Assume each exact rational sample parameter \(t_i\) is in \(D\), with certified
enclosures

\[
  g_j(t_i)\in[\ell_{ij},u_{ij}].
\]

For any exact nonnegative weights summing to one, the point
\(z=\sum_i\lambda_i g(t_i)\) is in \(C\), and

\[
 L_j=\sum_i\lambda_i\ell_{ij}\le z_j\le
 U_j=\sum_i\lambda_i u_{ij},\qquad
 r_j=\frac{\max\{|p_j-L_j|,|p_j-U_j|\}}{s_j}.
\]

All displayed quantities are computed as rational numbers. In particular,
the residual uses the farther interval endpoint. Distance from \(p_j\) to the
interval itself would be a lower estimate and is unsafe for this purpose.

**Certificate and proof.** For a valid support inequality
\(a^Tx\le b\) on \(C\), feasibility of \(z\) implies

\[
 a^Tp-b\le a^T(p-z)\le
 \sum_j |a_j|s_jr_j.
\]

Consequently the following two conventions are valid:

| Screening norm | Required cut normalization | Certified upper bound |
| --- | --- | --- |
| `norm="1"` | \(\max_j s_j|a_j|\le1\) | \(\sum_j r_j\) |
| `norm="inf"` | \(\sum_j s_j|a_j|\le1\) | \(\max_j r_j\) |

The same argument applies to lower support inequalities by reversing signs.
It proves the certificate without requiring a closest point, optimal weights,
or a closed hull. If \(C\) is nonempty and compact, separation of the open
norm ball centered at \(p\) from \(C\) also gives the familiar equality between
distance to \(C\) and the strongest support-cut violation with the dual unit
normal constraint. To see the reverse inequality, let the distance be
\(\delta>0\), separate \(C\) from the open radius-\(\delta\) ball, and normalize
the separating normal in the dual norm. Its support gap is at least
\(\delta\); the preceding inequality bounds it by \(\delta\). At zero distance,
the zero normal attains zero. This equality explains the normalization but is
not needed by the implementation.

The direction LP in `solver/integration.py` bounds each coefficient on the
scaled graph coordinates independently in \([-1,1]\). It therefore uses
`norm="1"`. Substituting a maximum residual for the sum would be incorrect:
for the singleton graph \(C=\{(0,0)\}\) and query \((1,1)\), the maximum
residual is one while the permitted direction \((1,1)\) has violation two.
Coordinate offsets used by the direction LP cancel in \(p-z\).

For a certified upper bound \(R\), `can_skip` means exactly \(R\le\tau\), where
\(\tau\ge0\) is the supplied threshold. This rules out a normalized violation
**strictly larger** than \(\tau\) for this block at this query. Positive-tolerance
screening does not prove hull membership, original-model feasibility, an
objective-gap guarantee, or the absence of useful cuts at a later query. A
large bound is inconclusive. An exactly zero bound does supply an exact
convex-combination hull witness.

**Implementation and trust boundary.** `solver/screening.py` depends only on
the Python standard library. `SampleCache(bounds=..., rows=..., evaluate=...)`
owns an immutable domain specification and caches feature enclosures at exact
rational parameter points. `cache.bind(sample_points)` checks the finite box
and every supplied affine row exactly before evaluating new points. A row is
the coefficient tuple followed by its upper bound. An equality is represented
by its two opposite inequalities. The returned immutable `BoundSamples` is a
trusted in-process result, not an independently trusted serialized object.

The evaluator is supplied by the integration and is part of the trusted graph
definition. It must enclose the **original declared feature vector** at the
exact input point; approximate sampled feature values cannot replace it.
The current adapter enables screening only for original expression trees
recognized as polynomials, and evaluates their rational monomials directly.
The available `certified.feature_intervals` function also supplies exact
polynomial evaluation and rigorous univariate elementary-function enclosures;
using the latter in solver screening would additionally require preserving the
original elementary-expression domain. If the declared domain includes
additional restrictions not represented by the box and affine rows, the
evaluator must certify those restrictions or reject the point. In particular,
symbolic cancellation must not silently remove an original expression-domain
restriction when claiming a certificate for the original graph. A deliberately
enlarged block domain instead defines a weaker hull, and its screen only rules
out cuts for that declared hull.

Source points intended to satisfy an equality can fail the exact check after
floating-point conversion. For example, the exact binary values of `0.1` and
`0.9` do not sum to the rational number one. Such points are rejected. Exact
convex combinations of rational polygon vertices provide feasible alternatives;
a rejected point does not establish that the domain is empty.

`screen_convex_combination(query, samples, proposed_weights, scales=...,
threshold=..., norm="1")` performs no optimization. Every finite proposal is
converted to its exact rational value, negative weights are clipped to zero,
and the remaining mass is normalized exactly. Even a poor LP proposal yields
a valid, possibly weak, witness. All-nonpositive weights, nonfinite inputs,
invalid scales, and dimension mismatches are rejected. LP failure or rejection
must leave separation undecided; it must not count as a successful screen.

Physical direction coefficients are rounded toward zero until the exact
weighted normal bound remains at most one. Thus the normalization applies to
the actual floating-point coefficients passed to cut certification and SCIP,
including division-rounding effects when removing coordinate scaling.

The returned `ScreenCertificate` retains the exact bound, normalized weights,
norm, scales, query, domain, sample enclosures, and activation threshold.
`.can_skip` compares rational numbers, including the exact binary value if a
floating threshold was passed. `.to_dict()` serializes this evidence only when
needed. `replay_screen` takes the expected query, domain, evaluator, scales,
norm, and threshold from the caller, reevaluates all original graph witnesses,
and compares the complete result. It does not trust saved feature enclosures
or saved domain data. Replay shares the arithmetic with the producer and is
not a formally verified independent checker.

Caches must be discarded or rebuilt if the graph or declared domain changes.
In particular, source samples feasible at a parent node may be infeasible
after local bounds shrink. Current integration blocks use fixed global domains
and root separation, so this rule does not require local-domain bookkeeping.
`upper_float` is available for reporting a rational bound to a numerical API;
it rounds upward, including underflow, and returns positive infinity on
overflow. Decisions should use the exact bound whenever possible.

**Work and limits.** With \(n\) bound samples and \(k\) graph coordinates, each
mixture requires \(O(nk)\) rational operations, plus normalization and validation.
This is an arithmetic operation count, not a uniform bit-complexity bound:
denominators and graph-evaluation costs matter. Sample evaluation is reused
across callbacks and the existing direction LP supplies dual weights. Acquiring
a new mixture incurs that LP cost; a cached mixture can be evaluated at a later
query before another LP and can then skip both direction search and support
work. Actual savings require measurement in the solver campaign.
A cached valid support cut can also supply the opposite bound on hull distance
by dividing its positive violation by the appropriate dual norm. That follows
from the same inequality and requires the cut to be recertified for its actual
exported coefficients and declared domain; no unchecked LP objective is a
distance certificate.

The targeted command actually run was:

```sh
PYTHONPATH=research-20261002-convexification/solver python -m pytest -q research-20261002-convexification/solver/test_screening.py
```

It passed 37 tests. These check dual-norm selection, interval uncertainty,
exact floating-weight repair, coordinate scaling, equality-constrained source
points, reuse of evaluations, exact threshold comparison, outward export,
existing LP dual weights, and replay mutations of witnesses and expected model
data. The first invocation without `PYTHONPATH` failed during import collection;
the command above is the supported root-directory invocation. No project-wide
or CI checks were run for this component.
