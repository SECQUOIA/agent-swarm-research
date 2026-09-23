# Optimal finite good-aggregation accuracy

Status: complete. All ten [frozen claims](CLAIMS.md) are covered by fifteen
modules, independent reviews, warning-free targeted builds, a 232-declaration
axiom audit, and all fifteen kernel replays. See [VERIFICATION.md](VERIFICATION.md).
The claims fixed the required scope from
[the reviewed accuracy note](../../../notes/research-20260922-aggregation-accuracy.md)
before implementation. This is the second package explicitly selected by
the user, following the completed [exact hull and SDP package](../30-infinite-aggregation-hull/README.md).

For every `r≥2`, this package studies finite weak good-aggregation
relaxations of the same quadratic system. It verifies the uniform
Euclidean Hausdorff approximation rate `Theta(N^-2)`, the stated explicit
upper and lower constants, rational cut constructions, and logarithmic
coefficient bit bounds. The lower bound covers arbitrary interior and
extreme good multipliers, with arbitrary positive rescalings.

The Hausdorff distance is extended-valued, so unbounded relaxations have
infinite error. The best error is an infimum over families of at most `N`
cuts; no existence of an optimal family is assumed. The metric is the
Euclidean metric on the full `2r` original variables, not the supremum
metric inherited from a raw function type or pair type.

The [source inventory](SOURCE-REVIEW.md), [coverage map](COVERAGE.md), and
[review record](REVIEW.md) track these distinctions. The separate
single-objective proposition and support-function theorem in Section 4 of
the source note are excluded. The package makes no numerical solver,
conditioning, runtime, iteration-count, or branch-and-bound claim.

The [paper supplement](../../../paper-quadratic-aggregation/formal-aggregation-accuracy.tex)
and [formal account](../../../paper-quadratic-aggregation/sections/94-formal-aggregation-accuracy.tex)
state the exact results. The independent supplement builds cleanly to two pages.

Public results include `optimalError_bounds`, `optimalError_theta`,
`exists_family_for_tolerance`, `necessary_family_budget`,
`hausdorffError_rationalCuts_le`, and `rationalCuts_log_encoding` in
namespace `InfiniteAggregation`. The rational construction has error at
most `20*sqrt(2)/N²` using at most `N` cuts for `N≥3`.
