# Quadratic aggregation verification extensions

The user authorized all recommended follow-up work on 2026-09-22, including
implementation, independent review, targeted verification, and related note
and paper updates. Topic 27's completed core package remains unchanged.

Only one extension topic is active at a time. Work within the active topic
may be delegated to independent agents. Complete its source obligations,
semantic review, and targeted checks before starting the next package.

| Topic | Scope | Status |
|---|---|---|
| 28 | Closed-system consequence (Corollary 1), Shor consequence (Corollary 4), unconditional Shor characterization (Lemma 4), exact finite SDP characterization (Corollary 3), and the two recommended boundary examples with actual HHC | Complete; 12 claims, 10 modules, independent reviews, targeted checks and paper supplement |
| 29 | The explicit infinite-aggregation construction: HHC, classification of good multipliers, indispensable rays for strict descriptions, and finite impossibility for closed descriptions | Complete; 12 claims, 18 modules, independent reviews, targeted checks and paper supplement |
| 30 | Exact strict and closed hulls of the infinite-aggregation example, actual PD/PSD lifts, hull of the weak system, and all-good intersection equalities | Complete; eight claims, ten modules, 93-declaration audit, independent reviews and paper supplement |
| 31 | Optimal finite good-aggregation accuracy, including uniform Hausdorff bounds and rational constructions with coefficient-size bounds | Complete; ten claims, fifteen modules, 232-declaration audit, independent reviews and paper supplement |

Topic 28 includes the exact mathematical SDP characterization recommended
as a later addition, so it does not remain an untracked optional task.
It does not claim a verified numerical SDP solver or a complexity bound.

The full good-aggregation hull-description theorem behind Corollary 2 and
the classical convexity theorems behind Corollary 5 were explicitly deferred
in the recommendation. The general sharp Gram-map theorem, arbitrary
quadratic-description obstruction, quantitative aggregation-accuracy bounds,
and numerical experiments were not among the original recommended formalization
targets. The user subsequently authorized the exact-hull/SDP and aggregation-accuracy
packages (30 and 31). The other deferred results remain outside this sequence.

Every package receives frozen claims, declaration coverage, independent
reviews, a verification record, and source fingerprints. Local checks are
restricted to the active modules and related documents. Do not run
project-wide checks or inspect CI. Preserve concurrent manuscript work;
paper supplements may record verified results independently of the main
manuscript's separate staged review.

The initial two extension packages (28 and 29) are complete. Together they add 28
modules and 406 audited declarations. Their verification records and paper
supplements preserve the distinction between the proved scope and the
explicitly deferred work above.

The user explicitly clarified that the next two packages are exact hull/SDP,
then aggregation-accuracy bounds, rather than represented matroids. Complete
both within their frozen scopes, including independent review and related
source and paper updates. No work on topic 22 is authorized by this continuation.

The two subsequently selected packages (30 and 31) are complete: 25 new
modules and 325 audited declarations. Both have clean two-page paper
supplements and full targeted verification records. The quantitative work
includes arbitrary good cut families and exact rational coefficient sizes;
it excludes the separate single-objective proposition and solver claims.
