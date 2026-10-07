# Internal document consistency review

This review checks the integrated report against its mathematical arguments,
implemented contracts, and retained evidence. It is performed by a research
agent separate from the report and implementation authors. It is not
external peer review, formal verification, or a novelty determination.

Status: **closed after final document and evidence review**. The mathematical
claims, source-binding contract, empirical tables, abstract, conclusion,
claim map, topic overview, and closeout agree with the reviewed implementation
and retained evidence. No unresolved claim-consistency blocker remains. The
computational outcome supports keeping the separator experimental; it does
not establish a generally beneficial solver activation policy.

## Mathematical claim assessment

The support theorem states the compactness and continuity assumptions needed
for a complete closed-hull description. A finite generated collection is
correctly described as an outer approximation. The report distinguishes an
exact support oracle for a supplied direction from a complete separation
algorithm, and continuous support from the tighter mixed-integer hull.

The final-row proposition and the optional coefficient-rounding correction
have the correct inequality direction. They apply to the exact values of the
coefficients actually submitted, not the ideal direction before rounding.
Bernstein conversion, nonnegative basis weights, complete closed-cell
coverage, and strict row exclusion agree with the certificate implementation.
The optional chord correction uses an upper second-derivative bound and the
required `max(0,M)` clamp. The report does not turn failed domain checks,
resource exhaustion, or failed direction search into feasibility claims.
The separate [numerical review](numerical-review.md) covers the arithmetic
implementation and analytic tests; those checks were not repeated here.

The screening theorem correctly pairs scaled L1 distance with coordinatewise
normal bounds, and scaled infinity distance with a sum bound on the normal.
Its conclusion excludes violations **strictly greater** than the threshold.
The text correctly requires feasible graph samples, distinguishes a larger
block domain from the full model, and reserves hull membership for exactly
zero residual. It does not claim that block-hull membership implies nonlinear
feasibility or membership in the full simultaneous hull.

The polygon proof covers boundary minima, positive-definite interior minima,
and the singular positive-semidefinite case through a constant-value line
that reaches the boundary. Segment, singleton, and empty domains are covered
by the algorithm without an unmentioned nondegeneracy hypothesis. The stated
cubic arithmetic-operation count agrees with pair enumeration followed by
full-row feasibility checks. It is not presented as a solver runtime bound.

The constrained-star proof correctly derives piecewise affine conditional
minimizers for every sign of leaf curvature. The factored endpoint comparison
in the nonpositive-curvature case is affine after fixing the bound envelopes;
no irrational quadratic switch is needed. Each conditional rule remains
valid at a closed-piece endpoint, including ties. Intersecting the projected
leaf domains is exact because leaves are independent conditional on the
center. The source retains all input rows and rejects unsupported leaf
coupling. The initial draft omitted explicit rationality of objective and
row coefficients. The author corrected that hypothesis in both the section's
model definition and the merger-gain corollary; the corrected text was read.

The sharp merger-gain corollary is correct for the stated assembled domain
and fixed pair directions. Equality in the sum of individual lower bounds
requires every term to attain its own minimum at a common center. Compactness
then makes disjoint minimizing-center sets equivalent to a strictly positive
gain. The attained star minimum is the largest valid constant for that one
summed direction. The text does not claim that this chooses directions or
predicts solver runtime.

The overlap witness, `1/128` sharp gap, expanded sparse cut, and parameterized
family agree algebraically. The proof separates the incompatible local
representing measures from constraints on the original box. The comparison
is against complete pair hulls, not merely McCormick inequalities. Its
limitation concerning dense PSD plus the nonedge McCormick inequalities is
also correct: saturated positive edge covariances force `Cov(x,z)=1/5`, hence
`E[xz]=3/5 > E[x]=1/2`. The report makes no general dominance claim over SDP
or RLT.

Full separator marginals and the running-intersection property are sufficient
for tree gluing by conditional distributions on compact Euclidean Borel
spaces. Equal first and second moments do not supply that premise. The
binary-scalar, finite-support Vandermonde, and pure bilinear forest special
cases are consistent with the theorem. The companion constrained example is
carefully limited to separate block interval propagation; it does not claim
to defeat global presolve or automatically discover the extra separator
statistic.

## Final implementation claim assessment

The report correctly describes a research separator with native nonlinear
enforcement, rather than a native nonlinear handler or a complete solver
certificate. It distinguishes heuristic work selection from certified
screening, keeps support domains global, and states the cooperative rather
than hard nature of callback timing limits.

The initial integration draft overstated star discovery: it said affine-row
center structure was checked at discovery. The inspected implementation
generated candidates from the quadratic graph and could retain a leaf-leaf
row; the exact support dispatcher subsequently refused an unsupported star.
This is conservative for validity. The author revised the text to distinguish
quadratic-graph candidate discovery from the support oracle's affine-row
eligibility check; the corrected text was read.

The final source-model admission and actual SCIP-row auditing were read
against the final implementation. All four modes check the original source
domains on the complete declared box before simplification and compare the
exact source function with the assembled native coefficients. The report
states the resulting applicability restriction: a valid model may be refused
when declared bounds do not establish a domain that other constraints would
imply. Constant folding is limited to exactly representable results;
auxiliary definitions and rewritten rows have their own comparisons. An
unproved whole-model import returns `source_model_mismatch` without a bound
or cut. Unsupported variable exponents can instead fail in the inherited
builder, as the retained experiment records show.

The inserted-row check requires exact coefficients and effective side after
the explicit variable mapping and rejects dropped variables, numerical
fixings, aggregation, and locality changes. The replay checks the recorded
mapping, source features, domain, and inspected row. The text does not claim
to reconstruct or certify every later internal solver transformation. Native
construction and the runtime capture of the actual row remain part of the
documented trust boundary.

## Attribution and evidence boundaries

The report explicitly attributes simultaneous graph support, rigorous
Bernstein validation, low-dimensional quadratic hull foundations, box-forest
support, and measure consistency to existing work. The affine-row star
extension is a documented supported class rather than an established
first-result claim. Detailed source priority is covered by the separate
literature audit, not inferred from these proofs.

The final report consistently distinguishes checked individual cuts,
replayable artifacts, numerical solver bounds, and numerical primal residuals.
The adverse experimental result now appears in the abstract, conclusion,
topic and document overviews, closeout, and claim map. The repository overview
paragraph also keeps native SCIP as the default. The topic overview's screen
description was corrected from "below" to "at most" the threshold, preserving
the theorem's strict-violation distinction.

## Final empirical assessment

The direct evidence check reads raw records without importing the campaign's
summary or replay implementations. It verifies the following against the
report and saved summaries:

| Population | Selected per mode | Admitted per mode | Solved baseline/control/all/auto | Recorded cuts all/auto |
| --- | ---: | ---: | --- | --- |
| Synthetic | 13 | 13 | 12 / 13 / 13 / 13 | 89 / 72 |
| Held out | 24 | 20 | 19 / 19 / 18 / 18 | 230 / 106 |
| Historical | 4 | 1 | 0 / 0 / 0 / 0 | 24 / 24 |

The three held-out structured refusals are `syn15m`, `cvxnonsep_psig30r`, and
`syn10hfsg`. The fourth unavailable held-out case, `cvxnonsep_pcon40r`, raises
an inherited-builder error for variable exponents. These are importer
limitations shared by all modes, not native SCIP failures. The selected
denominator stays 24, while solver-behavior comparisons concern the 20
admitted models. The historical population is kept separate.

The raw records confirm `genpooling_lee2` as the lost held-out solve in both
cut modes, the reformulation control as already sufficient for the synthetic
quartic solved-count gain, and the poorer historical `waterno2_06` bounds.
The report's one-node counts match direct comparison of the raw numerical
bounds: `all` has 3 better, 15 tied, and 2 worse; `auto` has 3 better, 14 tied,
and 3 worse, with 4 unavailable cases in either comparison. These comparisons
use the declared `1e-6` bound-scale tolerance, not exact mathematical order.

The primary integration-time totals match raw sums. The main table labels
them as available in-process timings rather than total worker time. Separate
outer times retain the failed worker costs. Automatic selection's lower
candidate-LP and callback totals are not promoted to a complete-solver gain.
The screen has only 2 accepted skips among 506 queries. Star merging adds
cost on the displayed diagnostic even though its exact support theorem is
strictly stronger than the chosen pair-hull formulation. The combined
`no_cache` ablation is correctly described as changing exchange, screening,
repeat checks, and caching together. Six-second shared-host runs and the
small fixed repeat subset do not establish population-level speed claims.

The native sampling table matches the retained 35-case benchmark, including
the slower quadratic cases. Both C and Python sampler hashes match the
benchmark record. Its warmed kernel timings and 0.268-second build cost are
separate from solver timings. The main campaign does not load that backend,
which the report states explicitly.

Across all phases there are 316 unique scheduled records and 1,082 recorded
cuts. The 308 replay run IDs exactly match the raw records containing saved
model representations. All 1,082 recorded cuts pass; all 12 tamper controls
are rejected. The direct review also verifies all 101 frozen manifest hashes.
The eight missing model/cut outputs remain explicitly omitted from successful
replay coverage. Their traces place the variable-exponent failure before
optimization, but the report properly retains unknown logged cut counts.
The 36 structured import refusals are retained with their model records.

All 270 checked incumbents pass the numerical residual test, and no checked
root or final dual value conflicts with its declared reference. The text
does not turn these checks into exact primal feasibility or global-bound
certificates. No hard process timeout or omitted campaign job appears in
the completed record. The stated 443.6-second supervised wall time agrees
with `completion.json`.

## Review procedure

Read `document/main.tex` and the included `screening.tex`, `star.tex`,
`overlap.tex`, `integration.tex`, and `literature.tex`; compared their claims
with the theory notes, current implementation, and the prior numerical review.
The final pass also read the completed evidence section, all overview and
closeout conclusions, raw campaign records, final summary, replay output,
independent metric-audit output, and native benchmark. The targeted command
actually run was:

```sh
python research-20261002-convexification/reviews/check_document_evidence.py
```

It passed. Its retained output is
[`document-evidence-checks.json`](document-evidence-checks.json), and the script
does not import the producer's counting functions. Arithmetic tests and the
full certificate replay were not rerun in this document pass; the existing
recorded replay was inspected and reconciled with the raw run IDs and counts.
The report author performed the focused LaTeX build separately.

The final reviewed sources and evidence are pinned in
[`document-review-hashes.json`](document-review-hashes.json). In particular,
`document/main.tex` has SHA-256
`c5adbd621e49e57420f96c17c586c562c3ba56864637cde41386eb1af927513a`,
and `document/evidence.tex` has SHA-256
`ded3dcbc7d03b2c7c560e7068beb7a472866f9f99d2a405f79437c42787f552d`.
The reviewed PDF is the author's 22-page final build. Only topic-specific
checks were run; no project-wide verification or CI inspection was performed.
