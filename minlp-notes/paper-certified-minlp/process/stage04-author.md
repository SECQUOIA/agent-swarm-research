# Stage 4 author report

Author: `/root/s1_author`. This report is completed after the generation, replay,
packaging, and extraction checks below. Historical artifacts and frozen source snapshots
remain unchanged. The stage adds experiment orchestration and analysis, not new
checker rules. Five independent reviews and separate corrections remain the
coordinator's next step.

## Frozen design and denominators

- Original selection: 299 model names; seven historical load errors and three
  historical curvature-screen exclusions; all ten reasons are visible in
  `tables/cohort-selection.csv` and the original screening JSON.
- Historical evidence: all 289 attempted records, authoritative current replay
  188 verified / 92 rejected / 9 missing. No gratuitous repeat of that roughly
  58 GB present-proof corpus was performed for timing.
- New generation: all 289 historical attempts in lexicographic scheduling order;
  OA and each exact-SCIP search receive requested 30-second budgets; at most
  default plus conservative fallback; one requested OA/SCIP/LP thread;
  six concurrent workers; hard 360-second process-group wall limit; no retries.
  Subproblem overruns, preprocessing, proof completion and checks are additional
  work covered by the outer cap. Proof completion retains its tool defaults;
  its banner reports 36 available threads. OMP/MKL/OpenBLAS variables are one.
- Frozen before launch: `experiments/PROTOCOL.md`, `run_uniform.py`,
  `scip-uniform.set`, and campaign `protocol.json` with all tool/model/source
  hashes and package, hardware and environment data.
- Separate replay: all 289 records, six workers, 1,200 seconds per record,
  internal kernel acceptance without optional external corroboration. This is a
  separate execution of the same checker, not a second internal implementation.
  Historical replay used both internal and external checking, so the protocols
  are not represented as identical.
- Deterministic completed-proof selection: canonical, else failed safe, else
  failed default, else missing; no bound-quality selection. `REPLAY-SELECTION.md`
  and its selector were frozen in `replay-protocol.json` before replay. Completed
  proof files surviving outer timeouts can be accepted independently and are
  reported separately from production success.

## Implementation and evidence files

`sections/06-experiments.tex` gives the standalone experimental methodology,
historical revalidation, exact reference metric, twelve proof-step audits, exact
returned-point and source-equivalence cases, and reproduction scope.

Paper-owned scripts under `experiments/`:

- `run_uniform.py`: wraps the unchanged producer with process-group caps,
  per-tool start/end events and captured outputs. It does not change proof
  arithmetic. SCIP receives the frozen settings file.
- `verify_protocol.py`: checks all frozen source, input, wrapper, settings and
  executable bytes again after generation.
- `select_replay.py`: makes a relative symlink view under the fixed candidate
  selection rule; retained failed completed proofs remain distinguishable.
- `analyze.py`: exact rational reference comparisons, complete cohort tables,
  producer/replay outcomes, phase totals, and cross-campaign bound comparisons.
- `audit_failed_steps.py`: bounded extraction of twelve first failed steps using
  the existing row parser; independent standard-library Fraction recombination
  of their source rows. Extracts alone can be checked without the huge proofs.
- `package_evidence.py`: streams canonical historical and new completed evidence
  into a compressed archive, hashing and comparing with frozen replay hashes in
  the same pass. It never makes a second uncompressed full proof tree. Fresh raw
  proofs are retained only for genuinely incomplete cases; redundant raw proofs
  are listed as omitted. Compact logs are copied with license banners redacted,
  recording original and distributed SHA-256 values. Original research files,
  models, mathematical output, and proof files are untouched.

The portable core's `reproduce.py` uses paths relative to its own location. Its
`small` command checks four complete bundles and reruns the exact source/primal
case audit without vendor tools. `summaries` recomputes compact historical and
fresh metrics; `verify` validates the archive manifests; `replay` drives a new
complete 289-record replay after bulk extraction. `README.md` distinguishes five
pinned checker dependencies from optional generator tools and the broader local
`uv.lock`, which is provenance rather than a portable installation recipe.

## Scientific audit conclusions

- 81 old accepted labels are revoked: 67 domain/curvature, 13 cut, one proof.
  Eleven other proof failures came from historical crashes. The total number of
  current rejected bundles is 92, not 81. Rejection does not establish a false
  final bound.
- Eleven first-failed linear steps have matching exact coefficients but
  overstrong upper right-hand sides, with positive residuals approximately
  1.55e-12 to 1.93e-10. The twelfth, smallinvDAXr5b200-220, combines incompatible
  inequality directions. The independent extracts certify these local failures,
  not correctness of the preceding proof prefixes.
- The historical risk2bpb cut fails a sufficient safe-intercept test by about
  1.17e-12; that does not prove that the affine inequality is globally false.
- The 7,987.954-second historical sum covers 188 accepted records. All 289
  records total 8,234.349 seconds, and campaign elapsed time is 1,465.381 seconds.
  Checker totals exclude hashing but include model/nonlinear/master/internal and
  external checks. They are not pure-kernel timings or serial elapsed times.
- Reference comparisons are exact signed normalized discrepancies. Historical
  near-reference counts are 52 at 1e-4 and 81 at 1e-2; 23 differences are negative
  and smaller than 6e-10 in magnitude. No such comparison certifies feasibility
  or optimality. Eighteen solver-objective flags are investigation candidates.
- Clay0204m's SBB printed point robustly violates two rows by 4.5 and 3. It has
  Integer Solution rather than unqualified global-optimality status. An exact
  rational original-model point at 6545 and matching checked lower bound prove
  the loaded model's optimum 6545.
- Risk2bpb's saved SHOT point violates b4=b5=0 by setting each to one. The source
  audit verifies GAMS/Pyomo formulas under a common exact binary64 interpretation
  with objective-variable elimination and explicit maps. It does not verify a
  GAMS compiler or recover historical solver memory. No unseen internal cause is
  attributed to a solver.
- The quadratic solver-free sample proves optimum 1/4 with 11 cuts and 39 proof
  derivations, and a directly checkable matching original feasible point.

## Validation already completed

- `pytest -q certify/tests -p no:cacheprovider` from the solver-lab directory:
  **152 passed in 2.57 seconds**, log `stage04-pytest.log`.
  Two preliminary unittest invocations used the wrong test runner/import cwd;
  they ran no valid suite. Their logs remain separate and are not test evidence.
- Preliminary portable-core run passed all four representative bundles, both
  source-equivalence comparisons, robust printed-point violations, exact primal
  evaluation and complete clay0204m lower-bound matching. Output was written to
  `/tmp/certified-minlp-small-prepackage`, not into the archived results.
- No newly discovered mathematical checker soundness defect. The bounded producer
  and report-representation repairs below leave inference and nonlinear rules unchanged.

## Completed campaign outcomes

- Primary generation: 289 attempts; 198 verified producer returns, 67 admission
  errors, eight producer rejections, four outer timeouts, and twelve worker
  errors. Elapsed generation 2,840.697 seconds. The postgeneration integrity
  audit verifies all 311 frozen source/model/tool/wrapper/settings entries.
- Primary separate replay: 203 verified, 19 rejected, 67 missing; no timeout or
  other replay error. Elapsed 533.541 seconds. Accepted checker calls sum
  2,791.064 seconds; all records sum 2,953.982 seconds. All four producer timeout
  survivors and one worker-error survivor verify. Complete attempt paths and
  statuses remain visible; replay success is not production success.
- Of nineteen primary rejections, eighteen concern the submitted discrete proof
  or rational grammar; one (tls12) is post-proof exact-bound reporting failure.
  The eighteen are thirteen domination failures, two non-rational +infinity
  tokens, two incompatible-direction linear inferences, and one gapped unsplit.
- Exact near-reference primary counts are 46 at 1e-4, 80 at 1e-2, and 25 negative
  differences. These are signed reference discrepancies, not optimality gaps.
- The three new external-viprchk-accepted/internal-rejected proofs are locally
  audited in `evidence/new-proof-step-extracts`. Two linear combinations contain
  nonzero upper-direction terms among lower-direction terms, without constant
  tautologies (steps 4082 and 1639). The third (step 26121) invokes integer
  branches u<=64 and u>=66, leaving integer activity 65 uncovered. This is an
  invalid supplied standalone disjunction rule; other original rows could in
  principle exclude 65, but the cited rule does not establish that. None of
  these findings proves that the final numerical bound is false.

## Bounded software repairs and separate cohorts

V1 is the frozen original uniform producer/checker. V2 repairs twelve observed
producer normalization failures caused by Python's 4,300-digit decimal integer
conversion guard: `canonicalize_fractions` now parses and serializes through
existing FLINT `fmpq`, leaving the global guard enabled. The only production
module change from V1 to V2 is `certify/run_all.py`; a long positive/negative and
reducible-rational regression is added. **153 tests passed in 2.03 seconds**.
Every one of the twelve affected names was regenerated with the same search
budgets, settings, concurrency, and outer cap in
`experiments/producer-repair-20260913`: twelve verified producer outcomes and
twelve verified separate replay outcomes. Generation elapsed 478.703 seconds;
replay elapsed 62.473 seconds. Original primary failures remain in its full
denominator. The repeated names are not conflated with historical arithmetic
errors merely because the counts coincide.

V3 repairs a further exact rational-text boundary. The primary tls12 proof and
the secondary tls12 default proof pass nonlinear checks, exact master identity,
and the entire proof kernel, then fail on a 4,326-digit report conversion.
The protocol audits all nineteen primary rejections and all secondary attempt
reports, identifying precisely these two affected completed proofs. The new
`certify/rational_text.py` converts rational strings through FLINT and preserves
exact decimal reference semantics through Decimal; Fraction arithmetic remains
unchanged. Driver result serialization, replay/reference parsing, summary
serialization, and optional producer floating displays use this boundary.
Nonrepresentable optional binary64 displays are None, leaving exact strings
authoritative. The global digit guard remains enabled. Unused imports are
removed. Production changes are restricted to rational_text, driver, run_all,
recheck, and summarize; exact_model, convexity, safecut, and vipr bytes are
unchanged, as is driver's model/cut/master validation logic.

Both affected proofs pass full targeted replay under V3 in
`experiments/reporting-repair-20260914`, with no further optimization:
73.015 and 72.942 checker seconds, 73.431 seconds elapsed with two workers.
The source integrity report confirms no checker change during those replays.
**161 tests pass in 2.17 seconds** in the final suite, including >5,000-digit
positive and negative rational parsing/serialization, exact decimal references,
invalid/nonfinite input, both objective senses through actual complete
certificate checks, and producer success with an exact bound outside binary64
range. The two repair layers are ordinary representation defects, not changes
to mathematical proof rules. The final source diff and audit are archived.

The saved V1 primary replay remains 203/19/67. A fresh V3 replay of the same
fixed artifacts is expected to be 204/18/67 because tls12 now reports its
already-checked bound. The README makes this explicit; original counts are not
silently rewritten. Complete module/test snapshots for V1, V2, V3 and their
manifests are distributed. The actual V2/V3 execution wrappers were preserved
before portable path corrections, with exact hashes checked against their
frozen protocols; the primary wrapper never changed. `frozen-wrapper-integrity.json`
records all three matches. Top-level portable wrappers use supplied local
paths, while the frozen snapshots reproduce actual recorded orchestration.

## Catalog, packaging, and final validation

`bound_catalog.py` validates equal input-model SHA and objective sense, then
selects the strongest exact signed normalized bound across 405 verified records
(188 historical, 203 primary, 12 producer repair, two reporting repair). It
produces 222 distinct model entries: 162 selected historical records, 51 primary,
and nine producer-repair records. All candidates remain in JSON with exact
bounds and proof hash/path provenance. This is a useful merged evidence catalog,
not a success rate from one protocol. No reference primal or master solution is
used as a certificate.

The final standalone Section 6 includes all relevant historical/new experimental
outcomes, timing boundaries, versioned repairs, invalid-point/source audits,
local failed-inference witnesses, and catalog scope. Generated tables come from
`analyze.py`, `analyze_repairs.py`, and `bound_catalog.py`; saved-record summaries
preserve original denominators. Clean build:

```
# In a fresh source copy containing main.tex, references.bib, sections/, tables/:
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The source-copy build at `build/stage04-clean/main.pdf` succeeds without
undefined citations/references or overfull boxes; log
`process/stage04-author-clean-build.log`. An earlier output-directory build
picked up the repository's stale main.aux/bbl; its citation warnings are not the
final build result. The fresh source-copy build resolves this tooling issue.

The archive streamer preserves original completed mathematical artifacts and
compares source hashes in the same read. Compression starts only after all timed
runs finish. Compact source/table/doc staging is refreshed after bulk streaming,
so the final core includes final portable scripts and V3 modules rather than its
earlier staging copy. The source-copy audit matches all 27 current module/test
files to both core and V3 snapshot. Historical and all new completed proofs,
including rejected attempts, are present in bulk; redundant raw fragments are
omitted where completed versions exist. All omission decisions are inventoried.

Final packaging and extraction are complete. The bulk archive was streamed
back through gzip/tar, independently recomputing all 5,207 member hashes and
symlink targets: all match the manifest, covering 93,713,729,595 regular-file
bytes. The readback took 365.189 seconds and creates no extracted full corpus.
`process/stage04-bulk-readback.json` records the result.

The final core is 6,464,606 compressed bytes (33,886,577 uncompressed), and bulk
is 30,664,561,063 compressed bytes. Their exact SHA-256 values are:

- Core: `031a8a47f296d7fd8f484d3ad695c9476a8f316498a8ef5f2d5ecd03d7b287a6`.
- Bulk: `88c23497c2d20c76b3ac25cfc2c60a529aecb35da98e8de00213f4513ed314d4`.

Paths are `supplement/certified-minlp-core.tar.gz` and
`supplement/certified-minlp-certificates.tar.gz`; `supplement/archives.json` and
`README.md` provide the machine/readable index. The proof archive is large
because rejected completed historical proofs and completed fallback attempts
are retained for audit, rather than reporting accepted evidence alone.

The final core was extracted at
`/tmp/certified-minlp-extracted-final/minlp-certified-evidence`. Its 3,779-entry
manifest verifies, and the final 30 script/table/document files match their
paper-owned originals. Reproduction uses Python 3.13.11 in a fresh environment
containing exactly pip plus the five pinned checker packages. PYTHONPATH is
unset; PATH is `/usr/bin:/bin`; gurobipy is absent and gurobi_cl, IPOPT, SCIP,
viprchk, viprcomp are absent from PATH. The environment report is
`stage04-extracted-environment.json`. From the extracted working directory:

```
env -u PYTHONPATH PATH=/usr/bin:/bin /tmp/certified-minlp-review-env/bin/python reproduce.py verify
env -u PYTHONPATH PATH=/usr/bin:/bin /tmp/certified-minlp-review-env/bin/python reproduce.py small --out /tmp/certified-minlp-extracted-small-final
```

All four complete bundles pass; both original-model source/primal audits pass;
all twelve historical and three new local failed-step extracts recompute their
stated defects. Fresh saved-record summaries preserve all original outcomes.
`analyze.py`, `analyze_repairs.py`, and `bound_catalog.py` run outside the repo
and regenerate all thirteen data/TeX outputs byte-for-byte; only the new analysis
input manifest is intentionally path/environment-specific. Logs and comparison
JSON are under `process/stage04-extracted-*`.

A second fresh environment adds only the optional pytest dependency and runs
all distributed tests from the extracted lab under the same restricted PATH:
**161 passed in 2.67 seconds**. The final core refresh added explicit repair
replay instructions; its final manifest was reverified and all executable/data
bytes matched the already tested version. No vendor tool, inaccessible repo
path, or user literature PDF is needed for the advertised checker-only examples,
audits, summaries, catalog, or tests.

No unresolved mathematical/software defect was found in the admitted checker
contract during this stage. Scientific limitations are explicit: sufficient
admission/cut checks can reject valid models/inequalities; source semantics and
the software trust base remain scoped; mixed-direction/gapped submitted
inferences do not prove false final bounds; reference differences do not prove
optimality; shared-machine times and merged catalog coverage are not controlled
comparative solver claims. Five independent Stage 4 reviews are the next step.


