# Sequential verification of the recommended research topics

Requested on 2026-09-17. The user confirmed that the sequence includes both
the five ranked recommendations and all later recommendations.

Topics 12–21 are complete within their recorded scopes. Topic 15 finished
verification on 2026-09-19; topics 16–18 have completion records dated
2026-09-20. Topic 19 is complete, including its proofs, independent reviews,
and related source and manuscript updates. Topic 20 is complete, including
all 24 frozen claims, independent reviews, targeted machine checks and the
updated integer-dimension paper. Topic 21 is complete: all 33 frozen claims,
124 Lean modules, independent reviews, targeted machine checks, and updated
source notes and correlated-measurements paper. Topic 22 is complete:
all 37 claims, 65 Lean modules, independent reviews, targeted checks, and
updated source note and paper. Topics 23–26 remain queued; completing
topic 22 does not start another topic.
On 2026-09-22 the user selected the newly recommended quadratic aggregation
theorem ahead of that queue. It is recorded as topic 27 to preserve the
existing identifiers, and is complete: 12 obligations, 11 Lean modules,
independent statement reviews, targeted checks, and related source and paper
updates. No work on the next topic is implied by its completion.
The completion requirements below
continue to apply when the sequential formalization work resumes.

Only one topic may be active. Work on the next topic starts after the current
topic has complete mathematical coverage, independent statement review, and
passing targeted checks. Subagents may
work concurrently on independent obligations within the active topic.

Project-wide verification is handled by CI. Do not run it locally or inspect
CI status or logs. Local work uses targeted module builds, focused tests, and
topic-specific audits as needed. Record only checks actually run; a local
completion record must not claim an unobserved CI result. This rule supersedes
the local full-project verification requirement used by earlier packages.

The earlier completed sequence is preserved in [COMPLETION-PLAN.md](COMPLETION-PLAN.md).
The [topic index](topics/README.md) records both earlier and new packages.

| Order | Package | Scope | Status |
|---|---|---|---|
| 12 | [Marginal-floor gaps](topics/12-marginal-floor/README.md) | Finite bound, leading-constant-one asymptotic, two-sided strip, and original nonnegative boxes | Complete; checks passed |
| 13 | [Many-leaf reciprocal-anchor hull](topics/13-many-leaf-reciprocal/README.md) | Exact hull, finite witnesses, normalization, rational evaluation and separation with complexity | Complete; targeted checks passed |
| 14 | [Certified-MINLP mathematical soundness](topics/14-certified-minlp/README.md) | Propagation, correction tables, discrete inference invariant, unconditional transfer, curvature tests, and executable inference checking | Complete; targeted checks passed |
| 15 | [Flat-chain network–simplex threshold](topics/15-flat-chain-threshold/README.md) | Complete three-label unit-coefficient result, four-label obstruction, constructive recovery and stated complexity | Complete; targeted checks passed |
| 16 | [Deterministic potential-flow certificates](topics/16-potential-flow-certificates/README.md) | Bregman intervals, goal certificates, zero-curvature cases, completeness/convergence and exact examples | Complete; targeted checks passed |
| 17 | [Switching control](topics/17-grid-switching/README.md) | Arbitrary-grid one-switch minimax and sharp grid transfer, including the supporting algorithm and certificate claims | Complete; targeted checks passed |
| 18 | [Positive-box multilinear gaps](topics/18-positive-box/README.md) | Aspect-ratio upper and lower bounds, finite-dimensional refinement and original-box interpretation | Complete; targeted checks passed |
| 19 | [Structural multilinear gaps](topics/19-structural-multilinear/README.md) | Feedback-variable, frequency-two and incidence-treewidth-two bounds and stated sharpness/box extensions | Complete; targeted checks and independent reviews |
| 20 | [Scalar quadratic precision](topics/20-scalar-quadratic/README.md) | Rank and inertia laws, unrestricted-integer lower bounds and matching explicit approximation constructions | Complete; 57 modules, independent reviews and targeted checks passed |
| 21 | [DAG spectral approximation sets](topics/21-dag-spectral/README.md) | Relative PSD sandwich, exact singular ranges, feasible-path construction, size and bit complexity, criterion consequences | Complete; 33 claims, 124 modules, independent reviews and targeted checks passed |
| 22 | [Represented-matroid spectral approximation sets](topics/22-represented-matroid-spectral/README.md) | Rational representation, profile construction, feasible bases, spectral guarantee and stated complexity | Complete; 37 claims, 65 modules, independent reviews and targeted checks passed |
| 23 | Structured bilevel manuscript | Remaining mathematical claims of the complete manuscript, including exact/approximate algorithms and boundaries | Queued; unfinished |
| 24 | Power-flow manuscript | Remaining mathematical claims, including reduction semantics, graph restrictions and quantitative/algebraic consequences | Queued; unfinished |
| 25 | Pooling complexity | Developed hardness and tractability results, reduction semantics, certificate/encoding claims and structural boundaries | Queued; unfinished |
| 26 | Integer-dimension manuscript | Remaining mathematical claims beyond the completed exact-count package and the completed scalar quadratic scope of topic 20 | Queued; unfinished |
| 27 | [Quadratic aggregation certificates](topics/27-quadratic-aggregation/README.md) | Main asymptotic-HC equivalence, HHC specialization, and three supporting lemmas; selected ahead of topics 22–26 | Complete; 12 claims, 11 modules, independent reviews and targeted checks passed |
| 28 | [Quadratic aggregation consequences](topics/28-quadratic-aggregation-consequences/README.md) | Closed-system and Shor equivalences, exact finite SDP characterization, and two boundary examples | Complete; 12 claims, 10 new modules, independent reviews and targeted checks passed |
| 29 | [Infinite aggregation under HHC](topics/29-infinite-aggregation/README.md) | Actual HHC, spectral goodness classification, indispensable strict rays and finite closed-hull obstruction | Complete; 12 claims, 18 modules, independent reviews and targeted checks passed |
| 30 | [Exact infinite-aggregation hulls](topics/30-infinite-aggregation-hull/README.md) | Strict/closed formulas, actual SDP lifts, weak-system hull and all-good intersections | Complete; eight claims, ten modules and targeted checks passed |
| 31 | [Finite aggregation accuracy](topics/31-aggregation-accuracy/README.md) | Euclidean Hausdorff bounds, rational constructions, coefficient sizes and tolerance budgets | Complete; ten claims, fifteen modules and targeted checks passed |

The authorized [quadratic aggregation extension sequence](QUADRATIC-AGGREGATION-EXTENSIONS.md)
is complete within its stated scope. The deferred full hull theorem,
general Gram-map result and single-objective proposition remain separate.
The exact-hull and quantitative packages 30–31 were subsequently selected
and are now complete.

## Package requirements

Each topic receives a numbered directory under `topics/` containing:

- `README.md`: scope, source notes/manuscript, proof modules, status and navigation.
- `CLAIMS.md`: the complete frozen mathematical obligation list and dependencies.
- `COVERAGE.md`: obligation-to-declaration map, including boundary and representation cases.
- `REVIEW.md`: independent semantic/proof review and resolution of findings.
- `VERIFICATION.md`: actual commands, results, logs and source fingerprints.

Proof sources remain in the canonical `Formal/` tree except for the existing
standalone certified-MINLP project, whose own checks and coverage are retained.
All proof modules must be imported and audited. No unfinished theorem, custom
axiom, or native-computation axiom may substitute for a proof. An algorithmic
claim is not complete merely because its output is sound on selected examples;
the advertised correctness, termination and complexity obligations must be mapped.

Mathematical verification does not establish novelty, bibliographic priority,
external peer review, physical validation, or historical runtime measurements.
Software claims require an explicit connection to the verified definitions;
proving an implication with an unverified software-produced premise does not
verify the producer or parser. Any remaining scope limitation must be stated
and must not be labeled complete.
