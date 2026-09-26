# Topic inventory and current claim-to-evidence map

Integrated manuscript state, 2026-09-14. This current map supersedes the earlier
Stage 1 inventory; dated review and development records remain in `process/`.
Paths below are relative to this paper directory unless a repository-relative
path is explicitly identified. The manuscript covers certified convex-MINLP
bounds, their implementation and reliability, exact primal/source case audits,
and focused mathematical formalization. Unrelated repository topics are excluded.

## Mathematical and executable developments

| Development | Manuscript and source evidence | Exact scope |
|---|---|---|
| Loaded-expression semantics | Section 2; repository `code/minlp_solver_lab/certify/exact_model.py` | Rational interpretation of stored binary floating leaves and integer leaves; subsequent exact operations. Does not undo earlier Pyomo/Python rewrites or automatically recover source decimal meaning. |
| Domain/curvature contract | Sections 2 and 4; `convexity.py` in the same module directory | Original domains checked before cancellation; sufficient composition, exact quadratic, monomial, norm and one-variable fractional rules. Perspective shortcut disabled. No universal recognizer or general nonconvex support. |
| Rational cut correction | Section 3; `safecut.py` | Support/enclosure correction on bounded, half-line, free and fixed coordinates; singular/unsupported symbolic derivatives reject. Supporting-plane and support-minimization principles are established prior work. |
| Rational propagation and master identity | Sections 3–4; `driver.py` | Feasible-point preservation including integrality, objective constants/sense, complete variable and row matching. Partial checks expose no certified bound. |
| Complete restricted VIPR replay | Sections 3–4; `vipr.py` | Explicit assumption and incumbent semantics, exact rational inference, integrality-sensitive rounding and unsplitting, grammar and suffix checking, two-pass sparse replay. Executable remains unmechanized. |
| Representation repairs | Section 6 and Appendix B.3; `run_all.py`, `rational_text.py`, reporting/replay/summary interfaces | V2 repairs guarded long-integer conversion in producer normalization; V3 repairs long-rational parsing/serialization and optional binary64 displays. Mathematical proof, domain, curvature, propagation and matching rules unchanged. |
| Frozen replay and summaries | Sections 4 and 6, Appendix B; `recheck.py`, `summarize.py`, paper-owned `experiments/` | Before/after artifact integrity, full denominators, process-group caps, source/environment IDs, exact objective-sense/reference comparisons. Separate execution shares the same checker implementation. |
| Original-model primal/source audits | Section 6; `audit_solver_discrepancies.py` | Exact witness 6545 for `clay0204m`, matching lower bound; robust infeasible saved SBB/SHOT points; GAMS/Pyomo formula matching under common binary64 semantics. No compiler verification or unseen solver-cause claim. |
| Lean mathematical contract | Section 5; `formal/COVERAGE.md`, `formal/CertifiedMinlp/*.lean` | All 49 mathematical obligations: propagation, exact corrections, support calculus, curvature, structured proof checking, master matching, explicit nonlinear transfer, and primal completion. Derivative/enclosure and expression-identity evidence remain required; no benchmark artifact or Python verification. |
| Regression tests | Core current sources and V1/V2/V3 snapshots | Final 161 tests pass, including from extracted evidence. Restored V1/V2/V3 counts are 152/153/161. Tests are executable evidence, not a universal proof. |

## Scientific reading order

Section 6.1 leads with uniform capability (203/289 accepted replay versus 198
producer returns), signed differences from unverified references, exact primal
completion examples, and the descriptive 222-model catalogue. Section 6.2
classifies failures by what their witnesses establish: invalid submitted
inferences, sufficient nonlinear test failures, and exact original-variable
point/source audits. Section 6.3 synthesizes replay/generation costs, proof
storage, concurrency, and memory limits. Appendix B preserves the complete
frozen protocols, generated outcome/phase accounting, historical timing details,
and separate V1/V2/V3 repairs; Appendix A remains the reproduction entry point.
No numerical, software, formal, or generated-data claim changes with this
organization, and none of the versioned counts is merged into a new uniform run.

## Final experimental evidence

| Cohort or audit | Frozen result | Files |
|---|---|---|
| Population | 299 selected names; seven historical load and three screen exclusions; all 289 attempted names retained | `tables/cohort-selection.csv`; core screening snapshot |
| Historical complete replay | 188 verified, 92 rejected, nine missing; no timeout or mutation. Earlier accepted labels numbered 269; 81 were revoked | `tables/historical-summary.json`, `historical-cases.csv`; original/replay records in core |
| Historical rejection reasons | 67 domain/curvature, 13 cut checks, 12 discrete proof failures; eleven overstrong exact right-hand sides, one direction conflict | `evidence/proof-steps/`, `proof-step-checks.json`; full proofs in bulk |
| Historical costs | Accepted proof bytes 38,826,726,525; accepted checker seconds sum 7,987.954; all-record sum 8,234.349; elapsed 1,465.381 | `tables/historical-summary.json`; historical timing record |
| Primary V1 uniform generation | 289 attempts: 198 accepted returns, 67 admission errors, eight rejected, four outer timeouts, twelve worker errors | `experiments/uniform-20260913/`; `tables/production-analysis.json` |
| Primary V1 separate replay | 203 verified, 19 rejected, 67 missing; includes five producer-failure/timeout survivors; elapsed 533.541 seconds | `tables/uniform-summary.json`, `uniform-cases.csv`; frozen primary records |
| New invalid-step audits | Two mixed-direction combinations and one nonexhaustive integer disjunction, despite external acceptance | `evidence/new-proof-step-extracts/`, `new-proof-step-summary.json` |
| V2 producer repair | All twelve affected names regenerated and all twelve selected bundles separately verified | `experiments/producer-repair-20260913/`; `tables/repair-summary.json` |
| V3 reporting repair | Exactly two affected completed `tls12` proofs verified without new optimization; one is a primary artifact | `experiments/reporting-repair-20260914/`; same repair summary |
| Descriptive bound catalogue | 222 models from 405 accepted records; selections: 162 historical, 51 primary, nine V2. Matching input SHA and objective sense required | `tables/bound-catalog.json`, `.csv`, `experiments/bound_catalog.py` |
| Exact primal completion | Quadratic optimum 1/4 and `clay0204m` optimum 6545 | Four core representative bundles and source/primal audit |

A new full V3 replay of primary fixed artifacts is expected to yield 204/18/67
because of the targeted reporting correction. This is not another completed
uniform replay and does not replace frozen V1 counts. Near-reference metrics
are exact signed discrepancies from unverified reference strings, never certified
optimality gaps without original feasible witnesses. The catalogue is a union
of distinct protocols, not a uniform success rate. Recorded times on a shared
machine do not rank competing algorithms.

## Deliverables and verification

- `main.tex`, `sections/`, `references.bib`, `tables/`: complete standalone paper.
- `formal/`: standalone pinned Lean/mathlib project with 27 modules. The 24
  added modules passed targeted warning-free builds and a transitive audit of
  1,112 declarations. Current hashes are in
  `formal/verification/extension-SHA256SUMS-2026-09-25`; the historical
  `extension-SHA256SUMS` records commit `875a71ab`. The earlier three-module,
  95-declaration kernel replay is historical. No project-wide verification or
  CI inspection was run for the extension.
- `supplement/certified-minlp-core.tar.gz`: 6,478,681 bytes, current portable
  checker, all 289 models, versioned snapshots, compact records, audits,
  tests, representative proofs, and reproducible tables/catalogue.
- `supplement/certified-minlp-certificates.tar.gz`: 30,664,561,063 bytes;
  93,713,729,595 uncompressed regular-file bytes, 5,207 manifest entries, fully
  read back and checked in Stage 4. It has not been reread in Stages 5 or 6.
- `supplement/archives.json`: authoritative current core/bulk hashes. The core
  was last rebuilt during Stage 5 correction for the campaign-table caption;
  earlier dated stage reports retain
  their historical hashes and are not the current index.
- `README.md`, `certified-minlp-paper-source.tar.gz`: source/build/reproduction
  delivery, kept separate from core and bulk. No public DOI or upload claimed.

The exact mathematical proofs are self-contained in the manuscript. Supporting
repository notes document provenance but are not prerequisites to understanding
or building it. The two current evidence maps are review aids; dated author,
review, adjudication, correction, and validation records remain unchanged.
