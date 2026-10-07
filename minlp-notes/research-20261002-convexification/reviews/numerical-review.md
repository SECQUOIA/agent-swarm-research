# Internal numerical certificate review

This is an internal review by an agent separate from the implementation
authors. It is not external peer review or formal verification. The scope is
`solver/certified.py`, `solver/screening.py`, and
`theory/quadratic_polygon.py`, including the support kernel's binding to the
imported star oracle. The star algorithm has a separate mathematical review.

The review combined source inspection and independently derived analytic
fixtures. Producer/replay agreement alone was not used to establish validity.
The historical endpoint-sliver handling in
`code/univariate_envelopes/uenv/curvature.py` and the floating-point margin
assumptions in the earlier curve-hull report were also read.

## Finding and resolution

One concrete interface defect was found during review: the producer accepted
`max_depth=300`, but replay rejected proofs deeper than 256. For the feature
`x` on `[0,1]`, the row `x >= 2^-270`, and target `2^-271`, the producer returned
a complete 543-cell proof that its checker rejected. The cut itself was valid;
the certificate interface was inconsistent. The author fixed this by requiring
integer budgets with `max_depth <= 256` and `max_cells <= 1,000,000`, matching
the checker. The final independent regression rejects the old inconsistent
request and successfully generates and replays a depth-256 boundary case.

No invalid cut or unsafe skip was found in the reviewed arithmetic or analytic
fixtures. This conclusion has the trust and domain boundaries below.

## Mathematical and implementation checks

**Coefficient semantics and export.** Coefficients are converted to the
binary64 values actually exported, then interpreted as exact rationals. The
support expression uses those values. Stored SymPy floating constants are
also interpreted exactly. The right-hand side is rounded downward and is
checked against the rational local bound. Tests cover positive and negative
values, subnormal rounding, and a rational proposal whose binary64 value
differs from the rational input.

**Polynomial cover and affine rows.** Substitution into the tensor Bernstein
basis uses exact rational arithmetic, including shifted boxes with negative
bounds. The basis functions are nonnegative and sum to one, so the smallest
coefficient is a lower bound. A binary split covers both closed half-boxes;
their shared boundary is retained. A row excludes a whole box only when its
exact minimum is strictly greater than its right-hand side. An active row
boundary cannot be discarded. Degenerate boxes and inconsistent rows have
explicit fixtures. Without a target, a valid whole-box bound may be returned
before an empty row domain is discovered; that is not a claim of nonemptiness.

**Elementary intervals and domains.** Rational interval operations are exact.
Arb receives exact rational endpoints as `fmpq`; its outward `lower()` and
`upper()` results are converted by their exact mantissa/exponent, without an
intervening binary64 conversion. The installed python-flint 0.9.0 method
documentation explicitly specifies these rounding directions. Monotone
functions use endpoint bounds; sine, cosine, and cosh use a ball containing
the entire interval. Fractional powers require the stated nonnegative-base
domain, with strict positivity for negative exponents.

Every supplied original feature must pass whole-cell evaluation before the
scalar combination is simplified, including features with zero weight.
Fixtures retain unevaluated cancelled reciprocals and logarithms and require
refusal at their singularities. A peak at distance `2^-300` from an endpoint
checks that no endpoint sliver is replaced by its endpoint value. A positive
logarithm at `1+2^-200` checks preservation of rational endpoint information.
The implementation has no continuity-based sliver omission.

**Combined scalar and second derivative.** The code first takes valid natural
interval bounds and then optionally strengthens them with the bound for the
combined scalar function. If the scalar is twice differentiable on a cell
and its second derivative is at most `M`, its value is at least
`min(g(a),g(b)) - max(0,M)*(b-a)^2/8`. The sign and the nonnegative clamp are
correct. Endpoint lower bounds and a second-derivative upper bound are used.
Unsupported derivatives and unresolved derivative domains retain the natural
bound; they do not justify removing endpoints. Analytic checks include
`exp(x)-x`, whose one-cell chord bound is `1-e/8`, a concave logarithmic
example, exact cancellation of exponential features, and a nonsmooth
absolute-value example for which an endpoint-only bound would be invalid.

**Quadratic polygon support.** Exact intersections recover the vertices of
the bounded rational row domain. Vertex values, interior stationary points
of convex edge restrictions, and a feasible positive-definite interior
stationary point suffice. For a singular positive-semidefinite Hessian, an
interior minimum extends along a null direction to the boundary; omitting a
separate singular-interior candidate is therefore sound. An indefinite or
negative-semidefinite quadratic cannot require a strict interior minimum.
Fixtures cover all these cases, a clipped triangle, a segment, a singleton,
and an empty domain. Expected optima come from completing squares or direct
one-dimensional inequalities.

**Screening norm and strict threshold.** A feasible graph-sample convex
combination supplies an upper bound on distance to the hull. Interval sample
values use the largest possible residual at either enclosure endpoint, not
the midpoint. For the scaled infinity distance the dual condition is
`sum_j scales[j]*abs(normal[j]) <= 1`; for the scaled L1 distance it is
`max_j scales[j]*abs(normal[j]) <= 1`. Thus a bound at most the threshold rules
out violations strictly greater than the threshold. Equality can occur and
is tested explicitly. Samples just outside an affine row are rejected by
exact arithmetic. Negative numerical weight proposals are clipped and the
remaining weights normalized exactly.

**Replay and mutation.** The checker binds supplied expected expressions,
box, rows, and exported coefficients before checking evidence. It does not
evaluate expression text supplied by the certificate. Subdivision coverage,
row exclusions, local lower bounds, and the exported right-hand side are
rechecked. The imported quadratic and star oracles receive those same exact
expected inputs. Fixtures reject changed domains, coefficients, rows,
expressions, child counts, split indices, local bounds, and oracle bounds.
Screen replay reevaluates samples through the caller's trusted original
graph evaluator and binds the original query and norm policy.

## Trust and scope boundaries

- Replay shares bound and geometry routines with the producers. It is a
  checkable implementation with regression evidence, not an independently
  implemented or formally verified arithmetic kernel. Python, SymPy's
  symbolic transformations, python-flint/Arb, and their documented contracts
  remain trusted dependencies.
- The kernel preserves the domains of the expressions it receives. It cannot
  recover domain restrictions already erased before a caller supplied those
  expressions. The solver integration's original-expression preservation and
  screening eligibility are covered by a separate integration review.
- Caller-supplied affine rows must be valid restrictions of the intended
  model. A support certificate is conditional on that binding. A trusted
  screening evaluator must reject points that violate additional original
  nonlinear restrictions; the screen cannot infer these from box and rows.
- The in-process sample cache is trusted state. A caller must not change its
  graph or domain while reusing it. Serialized evidence has a stricter replay
  path that reevaluates original graph samples.
- Unsupported expressions, unresolved singularities, or exhausted work
  budgets return no cut. This does not establish hull membership. Positive
  threshold screening likewise makes no exact hull-membership claim.
- These checks certify individual inequalities and screening evidence. They
  do not certify SCIP's complete solve, tolerances, or final dual bound, and
  they make no solver-speed claim.

## Targeted verification

The independent script is
[`test_numerical_review.py`](test_numerical_review.py). The command run was:

```sh
/tmp/minlp-convexification-env/bin/python research-20261002-convexification/reviews/test_numerical_review.py
```

The final run passed **31 tests**, after the budget fix, with SymPy 1.14.0 and
python-flint 0.9.0. Output is retained in
[`numerical-review-checks.txt`](numerical-review-checks.txt). Only topic-specific
checks were run; no project-wide checks or CI inspection were performed.

The final reviewed SHA-256 values are:

| File | SHA-256 |
| --- | --- |
| `solver/certified.py` | `876bee204eafe1fa4a29d79357243dec27c0a3328fb565fb5b10d87daec3dec6` |
| `solver/screening.py` | `2a98eee1c7719127bdbeb95e6660ab9d8d952a3c116f6e11216f07cc95377b8e` |
| `theory/quadratic_polygon.py` | `7172e3c900631068198580608c2dcf01678d65379b007d36d28fa55ecad1e31b` |
| `theory/quadratic_star.py` (import binding and analytic fixture) | `669aefecc4cc4470f12552a835956337ad6536f6189ef0cebee6542c94398fde` |
| `reviews/test_numerical_review.py` | `fc580df7295b6e8dc5bf3e75a67a9f96347bd25f9b52ff68b31034636743f84f` |
