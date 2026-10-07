# Significance of the all-scale core value oracle

Date: 2026-10-02. This is an independent significance and scope assessment
of the reviewed [all-scale theorem](all-scale-core-value-oracle.md), read
together with its [actual-file review](../reviews/all-scale-core-value-oracle-review.md).
It is not another proof review or a publication-priority claim.

## 1. The substantial gain

The theorem gives a useful global-optimization contract for a small
nonconvex core coupled to a large convex polynomial residual problem.
For one sampled objective, a caller can request arbitrarily many accuracy
levels. Each request returns a feasible rational point and a certified
global value interval of width at most `2^-q`. Expected bit work is

```
f_d(k) (1+L/sigma)^k poly_d(I+q),
```

where the polynomial exponent does not grow with the core or residual
dimension. Residual curvature may vanish, residual optimizers may be
nonunique, and no residual noise is required. The numerical search
parameter uses the original upper core-coordinate curvature `L`.

The fixed noise law is important. It is chosen once from the base input,
has polynomial binary length, and works when later requests exceed its
sampling precision by an arbitrary amount. Correctness holds even at
exceptional atoms. Those draws use an exact fallback; they are not
discarded or resampled.

This is stronger than a separate expected node bound at each mesh size.
One random work factor bounds all refinement levels and all requested
precisions. Its truncated first moment and the same-draw fallback cost
are both controlled. An adaptive solver can therefore retain the sampled
objective while requesting tighter certificates. For a precision chosen
adaptively from the sample, the pathwise bound remains valid; an expected
bound for that adaptive stopping policy still has to account for its
random requested precision.

The output has operational content beyond an abstract optimal value:
the interval upper endpoint is the objective of the returned feasible
point. A solver can expose a certified incumbent and absolute global gap
without locating a particular residual optimizer.

The now-reviewed [core-coordinate addendum](core-only-noise-core-oracle.md)
also returns a core within `2^-q` of one fixed globally optimal core,
with the same expected parameter dependence. Its retained-hull test
contains both the incumbent and every optimal core; a separate small
growth-tail event pays for consistent exact selection when that test
fails. This makes the small nonlinear decisions themselves available
to arbitrary precision. Residual witnesses still need not converge to a
selected residual optimizer.

## 2. What is new relative to the local antecedents

The closest internal predecessor is the
[one- and two-coordinate value theorem](core-only-noise-value-oracle.md).
It already has the same fixed-law, all-accuracy output contract. Its
point-growth argument charges a cell count of order `(L/g)^(k/2)` against
a growth tail of order `g`. Truncating this bound pays for exact fallback
when `k<=2`, but does not give the claimed expected bound in larger
dimensions. The new proof controls the actual geometry of near-optimal
core sets instead of taking this high inverse moment. It removes a real
dimension restriction. It need not improve the sharper numerical bound
already available when `k<=2`.

The geometric step bounds the supremum, over all scales, of a padded
near-optimal-hull determinant divided by `h^k`. Convex conjugacy places
each such hull inside the inverse image of a small dual ball. A maximal
covering argument for the resulting Aleksandrov measure gives a weak
`1/T` tail in every dimension. A compact two-block formula then transfers
this all-scale event to a single finite grid. The independent review
identified and resolved an important format issue: the determinant is
encoded with polynomially many QR equations, rather than factorially
many expanded monomials.

Convex conjugacy, the Aleksandrov measure, covering lemmas, quantifier
elimination, and convex weak optimization are classical. The specific
contribution is their composition into this cell-count and fixed-law
complexity theorem. The [focused source audit](../prior-art/all-scale-core-value-oracle-prior.md)
compares the checked external antecedents and does not establish
publication novelty.

| Result | Main advantage | Restriction or weaker output |
| --- | --- | --- |
| [All-scale core value theorem](all-scale-core-value-oracle.md), with its reviewed core-output addendum | Arbitrary core dimension; only core noise; arbitrary convex polynomial residual fibers; selected-core refinement | No residual-coordinate distance or small expanded algebraic output; product-box model |
| [Strongly convex residual theorem](core-only-noise-boundary-recourse.md) | Exact implicit optimizer and coordinate refinement, including changing residual faces | Supplied uniform residual strong convexity |
| [Polynomial box recourse theorem](smoothed-polynomial-box-recourse.md) | Exact implicit optimizer under general convex residual recourse | Perturbs residual as well as core coefficients |
| [Bilinear flow theorem](smoothed-bilinear-core-flow.md) and [TU extension](smoothed-core-tu-recourse.md) | Exact finite algebraic optimizer/value output; integer recourse; arbitrary ties and core faces | Separable convex costs and a proved exact structured integer oracle |
| [Certified integer-recourse value corollary](core-value-certified-recourse.md) | Value certificates without identifying a stable integer label | Reviewed baseline has `k<=2`; the saved all-core extension is awaiting review; the conditional oracle is assumed |

The TU theorem remains stronger in its own structured class: it returns
an exact algebraic optimizer and value, with controlled representation
and refinement cost on every draw. For a quadratic core its output can
be rational even when native separable costs have higher degree. The
all-scale continuous theorem instead admits arbitrary dense, nonseparable
convex polynomial recourse and requires only certified approximate
conditional values. These are distinct capabilities.

The core-coordinate addendum has its own
[completed review](../reviews/core-only-noise-core-oracle-review.md).
Its selected-core Cauchy name remains weaker than the TU result's
finite expanded algebraic optimizer, and it does not control residual
coordinate distance without an additional premise.

## 3. Comparison with deterministic accuracy grids

For the same product model, the deterministic corrected full grid already
gives an additive `epsilon` objective certificate using, up to dimension
constants,

```
(1+sqrt(k L/epsilon))^k
```

conditional queries. Each query has bit cost polynomial in the input and
the accuracy bits. Thus the new result is not the first certified
approximation method for this class. Its improvement is the expected
dependence on accuracy for one fixed perturbed objective: polynomial in
`log(1/epsilon)`, rather than a grid-size power of `1/epsilon`.

The distinction matters when interpreting the noise. Write the sampled
objective as `F_c(v,z)=F_0(v,z)-c'v`, with `|c_i|<=sigma`. A feasible
`epsilon`-optimal sampled point satisfies

```
F_0(v,z)-min F_0 <= epsilon + sum_i |c_i|
                 <= epsilon + k sigma.                    (1)
```

This follows by comparing the sampled objective at that point and an
original optimum; the range of `c'v` on the unit core box is
`sum_i |c_i|`. There is no residual-dimension factor.

The oracle also supplies a directly checkable original-objective interval.
If `[a,U]` is its sampled interval and `U=F_c(v,z)`, then

```
[a+sum_i min(c_i,0), U+c'v]
```

contains the original optimal value. Its upper endpoint is attained by
the same feasible point, and its width is at most `epsilon+k sigma`.

Choosing `sigma` of order `epsilon/k` to force small original-objective
regret makes the expected search factor of order
`(1+kL/epsilon)^k`, before dimension constants. This does not improve the
ordinary worst-case deterministic approximation bound. The theorem is
most useful when the perturbed instance is itself the target, when its
linear prices are naturally uncertain at scale `sigma`, or when the
certified regret in (1) is acceptable.

## 4. Relation to low-rank convexification

The result is not merely an invocation of a fixed low-rank quadratic
convexifier on the original objective. For example,

```
F(v,z)=v z^2,   (v,z) in [0,1]^2,
```

has convex residual fibers and zero core-coordinate curvature. Adding
`alpha v^2/2` produces a Hessian determinant

```
2 alpha v - 4 z^2,
```

which is negative at interior points with sufficiently small positive
`v`, for every finite `alpha>=0`. Thus no finite quadratic on this
designated core makes the full objective convex. This is a class
separation, not a hard optimization instance.

Conversely, a low-rank concave quadratic supplies an important application
through the existing [Fenchel recourse construction](approximate-convex-recourse.md).
For `F(x)=G(x)-alpha ||Tx||^2/2`, introduce a core `a` and minimize

```
G(x) - alpha a'Tx + alpha ||a||^2/2 - c'a.
```

If the auxiliary box contains `Tx+c/alpha` for every feasible `x` and
every allowed `c`, eliminating `a` gives

```
F(x)-c'Tx-||c||^2/(2 alpha).
```

Independent auxiliary tilts then mean correlated noise in the original
variables along the selected low-rank directions. Rescaling the auxiliary
box to a unit box changes both curvature and noise scale: a width `s_i`
contributes core curvature `alpha s_i^2`. This interpretation does not
give a parameter depending only on rank, nor does the current product-box
theorem automatically cover an arbitrary coupled residual polytope.
The numerical geometry and the certified residual domain must be stated.

## 5. Solver implications and remaining limits

The ordinary search is comparatively direct: dyadic core cells, certified
conditional values at corners, corrected lower bounds, incumbent updates,
and a second filtering pass. The proof's measure and algebraic exceptional
sets are not objects the solver must construct. Certified primal-dual
intervals from a suitable convex solver could implement the conditional
interface; the current polynomial-time foundation uses rational convex
weak optimization and feasible repair.

Several limits remain material.

- The theorem assumes a supplied core and verified curvature and residual
  convexity information. It is not an efficient general recognition
  procedure for those properties. The certification cost is part of the
  model.
- The finite distribution is constructed for the base instance. It is not
  a theorem for an arbitrary coarse rounding grid or arbitrary atoms.
  Its sampling precision is polynomial in the input, but the cell cap
  and rare exact fallback can be exponentially large. Expected bounds
  do not give a practical worst-case runtime guarantee.
- A value Cauchy name is not a finite algebraic description or an exact
  equality test. Positive gaps can eventually be separated; equality of
  the optimum to a threshold is not decided merely by requesting more
  intervals.
- A feasible objective-gap sequence can move among residual solutions.
  Flat fibers and poor residual conditioning prevent objective accuracy
  from implying coordinate accuracy.
- The numerical ratio `L/sigma` is a genuine parameter. Its binary
  encoding alone does not bound the expected search factor. Scaling the
  model changes the relevant curvature and noise geometry.
- The diagnostics establish selected geometric and oracle interfaces.
  They are not a production implementation of the all-draw algebraic
  fallback, premise recognizer, or end-to-end convex solver.

## 6. Most consequential next question

The next capability should be coupled feasibility with a useful certified
cell relaxation, rather than a stronger claim about selecting residual
coordinates. Real MINLP models often let a small nonlinear decision block
change the feasible recourse set. The present rounding argument holds a
residual point fixed while moving the core, so it cannot simply be reused
on such models.

The concrete question is: for a rational coupled feasible set, can each
small core cell be given a polynomial-time convex lower problem and a
feasible incumbent whose error is `C h^2`, with `C` a stated, useful
numerical model parameter? The all-scale counting mechanism can then be
tested against that certificate, rather than assuming the projected value
function has the old curvature bound. Even convex recourse fibers alone
do not establish that bound when their domains move with the core.

The active coupled-feasibility lane investigates a rank-`k` convexifier
and whole-cell convex relaxations. That is a meaningful extension, but
its constant may be a convexifier strength `alpha`, not the original
coordinate `L`. For example,
`F(v,z)=v^2/2+z^2/2+M v z` has `L=1` and residual modulus one, while
adding `alpha v^2/2` makes it jointly convex only if
`alpha>=M^2-1`. A correct extension should expose this cost, preserve
feasible output under lower-dimensional constraints, and keep its
finite-law and precision claims explicit. This is the most direct route
from the current value theorem to a broader constrained solver capability;
it is being developed and reviewed separately.

## Assessment record

I read the all-scale theorem and its completed review, the core-coordinate
addendum and its completed review, the earlier value
theorem, the strong-recourse boundary theorem, the relevant polynomial
recourse and Fenchel interfaces, the exact bilinear/TU results, and the
saved certified-integer-recourse corollary and review. The source
comparison uses the focused literature audit. The regret interval and
the two Hessian comparisons above were checked directly. No mathematical
diagnostic was rerun for this prose assessment, and no new independent
proof review is asserted. Only this assessment's local formatting and
links were checked; no index edits, project-wide checks, or CI inspection
were performed.
