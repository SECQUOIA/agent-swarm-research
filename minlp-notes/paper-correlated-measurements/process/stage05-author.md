# Stage 5 author completion

Stage 5 is complete for the required five-reviewer gate. No original tracked
repository file, literature package, historical result, or unrelated paper was
modified. The 60-page combined technical draft builds with no undefined
references, LaTeX warnings, or overfull/underfull boxes. The abstract,
introduction, final discussion and submission package remain the explicitly
subsequent Stage 6 task; this report does not claim the full paper complete.

## Files authored or integrated

- `sections/05-computation.tex`: nine substantive empirical subsections;
  source-code reanalysis, evidence policy, ten scalar certificates and bound
  separations, all-diagonal positive/negative cases, spacing arithmetic,
  complete/partial packets, robust comparisons, fixed physical grids,
  five separators, and a new matched nested-anchor study.
- `appendices/computational-models.tex`: complete analytic sensitivity and
  spectrum definitions, independent balance/ODE check formulation, numerical
  proposal and exact-grid details, precise disposition of earlier experiments.
- `main.tex`: includes the two Stage 5 files. Existing accepted sections,
  appendices, macros and bibliography are unchanged.
- `supplement/README.md`, `pyproject.toml`, `uv.lock`, `archive-manifest.json`,
  `source-manifest.json`: standalone usage, dependencies, table/file map,
  frozen provenance and source/data hashes.
- `supplement/validate.py`, `replay_certificates.py`, `validate_models.py`,
  `fresh_experiments.py`, `reproduce.py`: portable validation and isolated
  numerical reproduction commands.
- `supplement/checks/stage02.py`, `stage03.py`, `stage04.py`: accepted finite
  checks adapted only to package-local helper/output paths. Stage 3's named
  audit helpers are included under `legacy/` and their old mains are not run.
- `supplement/legacy/`: byte-preserved measurement code, data and result
  subset, with individual original-path hashes. No adjacent storage,
  ODE-relaxation, tube, rational-flow or unrelated paper developments included.
- `supplement/source_kinetics/`: root's new exact full-ranking investigation,
  copied verbatim with README, CSV, standard-library generator, independent
  SymPy full-covariance checker and complete rational results.
- `supplement/results/`: fresh studies, model/proof/replay/full-validation
  evidence and a successful isolated block4 numerical-wrapper smoke test.
  Historical files remain under `legacy/` and are never overwritten.
- `process/coverage.md`: actual Stage 5 labels and full dispositions.

## New development and verified results

1. Root's public-source extension resolves the former floating D/A ranking
   uncertainty. Two enumerations give 2347 acquisition schedules; all 66
   formula/criterion/budget optima are unique. An independent 48-response
   covariance construction checks all 14,082 rational objective values.
   Only trace at budget3000 changes, with 3.112800396788% loss to the displayed
   precision; all eleven D and eleven conventional A choices agree exactly.
2. New nested study: n8,k3,p2 rational model, all56 common feasible schedules,
   four genuinely nested anchor sets. Exact feasible-mixture and support
   intervals establish strict tightening. All224 complete matrix Schur
   identities are independently checked through joint covariance congruences.
   The same known true optimum incumbent is used in all comparisons. A dense
   split lies between hierarchy members; the no-anchor hull still has an
   integrality gap. Short-window transfer can be uninformative. These outcomes
   prevent an unsupported universal ranking.
3. New block study: n8,d3,k3,L3 noncommuting rational model; all56 schedules,
   exact local prices and selected-covariance information. The sharp-far bound
   improves the same-incumbent relative certificate gap from12.4497% to11.4441%
   (upward displays). Archived d4/d16 L6 theoretical constants improve from
   .007274322 to .006754203; these are fresh constant comparisons and do not
   overwrite the old numerical certificates. Stored rho, dimensions, window,
   unit-noise model, rational permutation/transition form and noncommutativity
   are checked; rounded Q is separately a numerical diagnostic.
4. Independent sensitivity validation repeats all864 ODE sensitivity entries
   and16 high-precision matrix-exponential rows. Maximum differences are below
   1.65e-13 and1.48e-16. This is a diagnostic, not an interval ODE certificate.

## Validation completed

- All46 principal historical certificates replayed exactly:10memory,
  10fixed-split dense,10all-scalar,1all-diagonal,3spacing,4partial,3robust and
  5separator records. The replay checks actual rational bounds, price and
  witness fields, not solver status. One observed replay took128.92seconds.
- The full supplement suite passed in148.64seconds:159 frozen file hashes,
  Stage2/3/4 proof fixtures, allsource rankings, independent sensitivity and
  nested-model checks,46certificate replays and fresh exact block recomputation.
- Coordinator inspection then requested stronger explicit crosschecks. These
  were accepted and implemented: full matrix rather than determinant-only
  Schur equality; allscalar/diagonal common-model comparison to actual memory
  certificate data; archived block promise checks. A decimal-string SymPy
  parser issue found during that strengthening was corrected by explicit
  rational conversion. The strengthened model and block checks pass. The ten
  scalar and one diagonal cross-model comparisons also pass independently.
  Their record is `results/post-tightening-checks.json`.
- `reproduce.py block4` successfully ran the numerical producer in an isolated
  writable copy and exported a new result without modifying frozen inputs.
- The coordinator independently copied the supplement outside the repository,
  installed only base dependencies (confirmed Gurobi/CVXPY absent), and obtained
  a full pass in158.06seconds. A final refreshed strengthened suite is running
  under coordinator ownership; do not replace its result with author evidence.
- All certified table inequalities were checked for outward rounding. This
  corrected a last-digit all-diagonal lower display and one scalar-separation
  lower display during author development. Final build is clean at60pages.

## Limits retained, not unresolved positive claims

Historical timings are individual shared-machine measurements, some concurrent.
They are not controlled solver rankings. Decimal sensitivity provenance does
not validate physical generation. Temporal covariances are stipulated, local
rate-swap ambiguity remains, and robust guarantees cover only three supplied
scenarios. The full-block probes favor the dense bound and select the same
schedules as greedy; the fine-grid primary memory runs time out before their
first completed price. Separator n192b16 costs38.023seconds when exact
certification and shared work are included and still misses the .01target.
The synthetic all-diagonal fixed-point witness fails; it does not determine
that relaxation family's optimum. Earlier constants/results are explicitly
superseded rather than relabeled or hidden. No new primary-literature novelty
claim was introduced by this computational stage; established method attribution
remains in the accepted technical sections.
