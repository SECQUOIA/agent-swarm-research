# Reproduction package completion

Date: 2026-10-03. Scope: packaging the results in
`open-instances-summary.md` and `bound-audit/audit-report.md`.
**Final integration is pending:** `manifest.json` has deliberately not been
rebuilt during review fixes. Finish the minor-fixes round 2 and integration
edits, then rebuild and check it as the last step before committing those
changes together with this package.

No experiment family was rerun. No commit, push, contact, project-wide
verification or CI inspection was performed.

## Result

The package now maps all **43 summary instances** and all **46 screened
audit instances** to saved scripts, inputs and outputs. The guide explains
which author's default computations are weaker than the summary's reviewer
certificates. It also distinguishes replaying a published certificate from
solving for new numerical multipliers.

The package contains:

- [README.md](README.md), with commands, software pins, runtimes, expected
  outputs, input preparation, and the limits of the claims;
- `result-map.json`, with all summary rows, historical listed values and
  file hashes; `audit-map.json` and `audit-instances.md`, with every screened
  instance, classified pair, exact enclosure and per-point command;
- `commands.json`, indexing **443 historical measured commands** and their
  output hashes, exits and recorded wall times;
- `manifest.json`, hashing **2349 saved scientific files**;
- `inputs/saved-inputs.tar.gz`, a **9,598,219-byte** archive of **2063** saved
  inputs ignored by Git, with per-member hashes and original source URLs;
- `inputs/osil-models.json`, pinning **95** OSIL files and their download
  source, and `tools/prepare_inputs.py` to restore/check inputs;
- `requirements.txt` and `environment.json`, recording Python 3.13.11 and
  the package versions used by the prior runs and this smoke check;
- all earlier patches and evidence, plus a separate remaining-portability
  patch and the new smoke logs and file-open traces.

The archived inputs include the first-wave `minlplib_sol/` files, audit
pages and screened points, audit-reviewer data, and the scout's saved
pages. Users need not force-add each ignored source file separately: the
archive restores them to the paths that the scripts expect.

## Fixes

The ten unmarked existing patches applied cleanly in sequence within each
track: control 01–03, COPS 01–04, small 01–02, water-audit 01. They fix
repository paths and OSIL cache paths, restore the missing
`catmix_primal_snap_eval.py`, and save the optcdeg2 multipliers that later
scripts use. The patch marked
`00-shared-ev-kan_iv-applied-by-another-track.patch` was skipped as instructed.
Its two target files still had old paths in this checkout, so the additional
portability patch includes those repairs without applying the marked patch.

`patches/01-remaining-portability.patch` records the remaining changes to
**60 files**: 55 Python scripts and five shell helpers. The changes locate
repository files from `__file__` or the shell script path, expand the current
user's model cache, and find optional GAMS executables through `PATH`.
They include ANN code snapshots, network reviewers, EG decoding, primal
checkers, the COPS exact-display checker, and optional GAMS/EG launchers.
Numerical formulas were not changed by this work.

All **11** retained patches, including the additional patch, were checked
and replayed against HEAD copies. They touch **153** files: 147 Python
files and six shell files. **152** resulting files equal the working tree
byte for byte. `publication/primal/lnts/lnts_primal.py` also contains a
separate change to the second Krawczyk evaluation's center made by the
minor-fixes agent (`publication/reviews/minor-fixes/summary.md`, primal/lnts
issue 1). That change was
preserved and is recorded in
`logs/non-packaging-working-tree-differences.json`; it is outside the
portability patches. The syntax and manifest checks include the actual
working-tree file. Its later primal construction was not run here.

Historical command logs and old queue runners retain their historical
absolute paths as provenance. They are not package entry points. Fixed
`/tmp` paths in exploratory profilers and optional diagnostics do not feed
the reported certificates; the README does not require those diagnostics.

## Smoke checks

The smoke copy is `/tmp/repro-smoke-qg8quuvd`. It was made from the inventoried
working-tree files that the package requires, the new recovered script, the
input archive and the listed model files. It uses copied files, with no
symlink back to the main tree.

`bubblewrap` hid the main repository, the earlier clean worktree and the
original MINLPLib cache. Only the copied, hash-checked cache was mounted for
the checks. `strace` recorded file opens for each scientific command.
Commands ran sequentially with one BLAS/OpenMP thread and a 90-second
per-command cap.

**All 25 checks exited 0, matched their saved numerical outputs, and made
zero successful file opens in either source tree.** Their summed measured
wall time was **141.76 seconds**, excluding copying and input preparation.
Timing fields and checkout prefixes were normalized; numerical values were
not rounded or compared with a tolerance.

The checks cover lnts50 (author and tighter reviewer), dtoc5, camshape100,
optcdeg2 calibration recheck, lukvle10 preparation, chain50, the recovered
catmix800 primal evaluator, hvycrash, saved Gibbs certificates for both
ex6 instances, etamac, pricing050, pindyck, two EG primals, one small KAN
bound and its exact infeasibility proof, powerflow0030p fresh/stored
certificate paths, ANN primal evaluation, waterno2_06's period sum and
cell-slopes path calculation, and two audit certificates.

The EG, ANN and catmix checks are cheap primal checks, not new dual searches.
The water cell-slopes check validates all saved record corrections and the
exact path calculation, not new pair optimizations. The prior completed
COPS reproduction remains the evidence for the full long COPS runs.

The smoke driver initially stopped because I gave the catmix reference log
the wrong filename. I corrected that reference and resumed the existing
copy; completed scientific commands were not repeated. The final archive
adds 284 scout inputs to the 1779 used by the smoke copy. A separate isolated
input-restore check restored those 284 files and verified all 95 OSIL models,
without rerunning a scientific command.

Detailed commands, matches and traces are in `logs/smoke-results.json` and
`logs/smoke/`. `logs/final-input-restore.log` records the final restoration.

## Targeted commands and results

The following are the targeted commands actually run, from the repository
root unless stated otherwise. Inspection commands are not listed as tests.

| command | result |
|---|---|
| `git apply --check <patch>` followed by `git apply <patch>` for each of the ten unmarked existing patches | all applied; `logs/patch-application.json` |
| `python3 research-20260929/publication/reproduction/tools/finish_paths.py` | remaining Python paths fixed; separate patch recorded; final checker also includes the five shell edits |
| `python3 research-20260929/publication/reproduction/tools/build_package.py` | archive, input/software/file manifests and historical command catalogue generated; `logs/package-build.json` |
| `python3 research-20260929/publication/reproduction/tools/build_result_maps.py` | all referenced map paths exist; 43 summary / 46 audit instances; `logs/result-map-build.log` |
| `python3 research-20260929/publication/reproduction/tools/smoke.py` | started relocated copy and six checks; stopped on the bad reference filename |
| `python3 research-20260929/publication/reproduction/tools/smoke.py --resume /tmp/repro-smoke-qg8quuvd` | resumed twice as the two stored-certificate checks were added; 25 distinct successful commands in total |
| final `bwrap … -- python3 /tmp/repro-smoke-qg8quuvd/research-20260929/publication/reproduction/tools/prepare_inputs.py` | 284 added inputs restored; 95 OSIL hashes verified; exact argv in `logs/final-input-restore-command.json` |
| `python3 research-20260929/publication/reproduction/tools/check_package.py` | all hashes and maps checked; 147 Python AST checks and six `bash -n` checks passed; 11 patches replayed; inspected unrelated lnts change preserved; `logs/package-check.json` |
| `git diff --check -- <the 153 patch-owned scientific paths>` | passed; `logs/diff-check.log`; complete path list in the patch headers |

The checker first flagged the separate lnts center change during byte
comparison. After inspecting and recording it, the checker requires exactly
that preserved difference and rejects unexpected differences. No source
change was discarded to make the packaging check pass.

The saved population files independently give 1633 instances, 2816 points,
11086 solver bounds, and 19 invalid pairs on 15 instances. The scout gives
283 candidates and 146 remaining open candidates. These are data checks,
not new experiments. No CI results are claimed.

## Open issues and limits

1. **New numerical solve versus exact replay.** `pf_cert.py powerflow0030p`
   returns **576.8905424271796** with the pinned stack, as in the prior
   network reproduction log. The saved original multipliers replay to
   **576.893412298800469849…**, supporting the summary's safe lower
   **576.8934122988004**. The package directs users to that replay. Numerical
   reoptimization overwrites its output certificate, so it belongs in a
   disposable copy.
2. **Original numerical builds are incomplete.** GAMS 54.3 is recorded, but
   the original CONOPT and BARON builds are not. Some audit SOCP scripts
   save enclosures rather than raw optimizer multipliers, so exact
   regeneration of every historical enclosure endpoint is not guaranteed.
   Their saved programs, models, points, outputs and independent checks
   are present. No missing original build or multiplier was fabricated.
3. **Display provenance is resolved.** None of the five unsafe COPS strings
   appears in the summary. The package's three unsafe catmix table displays
   are corrected; detailed notes outside this task retain their rounding
   caveats. The water-audit rerun regenerated topopt p5 with a different QR
   basis and a different exactly feasible point (10.33547432783171797… with
   one BLAS thread). Four p5 displays then fail, giving 80 / 12 / one.
   The committed certificate has objective 10.335474327803234…; the report's
   84 / eight / one is correct for that point. The eight other failures are
   quotations and the skip is a histogram row. Class, margins and verdict
   are unchanged. The documented regeneration pins one BLAS thread with the
   recorded stack; it does not reproduce the committed basis across builds.
   The summary and audit report were not edited here.
4. **Verification qualifications remain.** KAN certificates concern R and
   its OSIL models are exactly infeasible. The original closures used tolerance-feasible points; exactly
   feasible points now cover all 13 (publication/primal/). The eg_disc2_s all-leaf certification rests on
   A1/A2; the separate interval check without a libm assumption samples
   10,404 leaves. SCIP error causes and historical literature claims retain their
   original uncertainty. This package does not broaden those claims.
5. **Model download availability.** The OSIL manifest pins the exact bytes
   and the official source. If MINLPLib replaces or removes a model, input
   preparation fails instead of silently changing the experiment. The
   archive includes the ignored reviewer model copies, but it does not
   vendor the entire external model cache.

There is a saved script/input/output trace for every summary instance and
audit classification. What remains incomplete is exact numerical-build
provenance for some historical optimizer searches, not a missing result
table or an unrecorded scientific experiment that this task should repeat.

## Files that must be committed

No files were staged or committed. `required-new-files.json` gives every
currently untracked package file, its SHA-256 and whether Git ignores it.
The required groups are:

- this report, `README.md`, `PROGRESS.json`, `audit-instances.md`, both result
  maps, the command/software/file manifests, and `requirements.txt`;
- all new `tools/` files, `patches/01-remaining-portability.patch`,
  `inputs/` (including the archive), and `logs/` (including smoke traces);
- the prior untracked `cops/report.md`, which completes that track's record;
- `research-20260929/open-instances-wave2/cops/explore/catmix_primal_snap_eval.py`.

The applied modifications to the scientific scripts and the portable COPS
exact-display checker also need to be included when the package is committed.
The separate lnts center change is a minor-fixes change and must accompany
the package. The manifest also depends on the minor-fixes files listed below. Original ignored
inputs outside reproduction need not be added separately if the archive
and restoration script are committed.

No background job remains. `PROGRESS.json` records the review response and
the final manifest step owned and completed by this integration implementation task on 2026-10-04.

## Response to review round 1

The independent review is `publication/reviews/repro-package-review-r1.md`;
its supporting evidence is in `publication/reviews/repro-package-r1/5a/`
and `5b/`. I checked the cited script usage, saved files, QR basis selection
and certificate endpoints before making the changes. I agree with all nine
issues. No summary or audit-report edit was made, and no experiment family
was repeated.

1. **Manifest and commit dependencies.** `tools/rebuild_manifest.py` is the
   single command that refreshes only `manifest.json`. `build_package.py`
   uses that builder instead of a second manifest implementation. The main
   manifest remains byte-identical to the prior inventory. The default
   checker reports missing files, stale expected/actual SHA-256 values and
   unlisted cross-directory inputs, then fails. The latest check lists 11
   such entries, as expected while other agents edit the track files.
   `files-to-commit.json` includes the scientific patches, package files,
   minor-fixes handoff and review evidence. `required-new-files.json` now
   includes the missing new minor-fixes scripts and new package files.
2. **Commands.** The catmix400/800 snap commands include the required
   `2e-3` threshold. The README and result-map commands use the four-instance
   lnts and camshape reviewer batches. A warning explains that commands
   overwrite saved logs and should run in a disposable copy.
3. **Water-audit explanation.** I reran `check_display.py` only in disposable
   copies of the reviewer's 5a saved fixtures: committed evidence gives
   **84/8/1**, regenerated evidence gives **80/12/1**. I checked the saved
   one- and two-thread QR certificates: both are proved feasible and their
   objective endpoints differ from the committed certificate. The one-thread
   point falls outside the report's p5 interval; the other two fit. No
   topopt optimization was repeated. The README pins one BLAS thread and
   explains the four extra display failures and the limits of determinism.
4. **Numeric maps.** Catmix400/800 now include their final bound logs,
   lukvle10 includes `lukvle10_prep.json`, EG includes the `.retry.sol`
   primals, and water rows include both `vsum.log` and `vsum2.log`. The maps
   explicitly pair saved-precision numbers with source files and quantities.
   The checker requires each whole numeric token in its mapped file and
   rejects an absent number or a mere prefix. It checked **2,423 numeric
   references** across **43 summary** and **46 audit** instances. Summary
   prose and outward rounded displays are retained in `reported_row`; this
   check verifies the literal saved evidence, not rounding correctness.
5. **COPS displays and summary conclusion.** The README uses safe lower
   displays −0.048059145600671712, −0.048069432031144562 and
   −0.048055901479675652. `cops/report.md` names the COPS verification report
   instead of claiming the unsafe strings occur in the summary, and uses
   the safe catmix800 policy width **≤ 1.49e-10**. I reran the reviewer's
   saved-file arithmetic in the isolated copy. **No COPS number in the
   summary must change under its current wording.** If integration removes
   the sentence saying no exactly feasible chain point was constructed and
   measures the gaps against the exact points or 60-digit KKT values,
   chain100's gap is **1.00276e-14**. Then change `same to 1e-14` to
   `within 1.1e-14` and `≤ 1.0e-14` to `≤ 1.1e-14`; the review also calls
   for reducing the tolerance-feasible closure count by four. This is an
   integration handoff, not a summary edit by this task.
6. **Portability.** The three authorized scout/census scripts now resolve
   imports relative to `__file__`. `patches/02-scout-census-portability.patch`
   records those changes. The manifest builder explicitly hashes the
   imported `research-20260922/scouting/minlplib-open-data/osil.py` and census
   script. Relocated hvycrash and scout/census import checks passed. The
   builder was exercised only in the disposable copy. All **12 patches**
   replayed; **154 of 156** files match the working tree. The two inspected
   differences are the minor-fixes lnts center change and a comment-only
   `nn_exact.py` clarification; both remain outside portability patches.
7. **Strict smoke checks.** All **25 checks** were rerun sequentially from
   `/tmp/repro-smoke-yc6t9u18`, with one BLAS/OpenMP thread and affinity limited
   to four CPUs. All exited 0, matched every selected reference line in order,
   and made zero successful opens in either source tree. Summed measured
   command time was **138.65 s**. The copy restored **2,063 inputs** and
   verified **95 OSIL hashes**. Only timing values are masked; historical
   checkout paths are rebased. Single-instance references use documented,
   fixed line ranges within batch logs. Standard output and error share one
   ordered stream, and Python runs unbuffered so warning positions match.
   Empty, shortened, duplicated, reordered and changed non-JSON output is
   rejected. No long dual search or full census was run.

The 18 minor-fixes files already required by the original manifest are:

- `publication/primal/chain/{minor_review_check.py,report.md}`;
- `publication/primal/dtoc5-lukvle10/{minor_review_check.py,report.md,gaps.py}`;
- `publication/primal/lnts/{minor_review_check.py,report.md}`;
- `publication/primal/powerflow/{minor_review_check.py,report.md}`;
- `publication/primal/water-ann-kan/code/minor_review_check.py` and
  `publication/primal/water-ann-kan/report.md`;
- `publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json` and
  `kan_r3_h1_n4.point.json`, `kan_r3_h1_n5.point.json`, `kan_r3_h1_n9.point.json`,
  `kan_r5_h1_n3.point.json`, `kan_r5_h1_n5.point.json`, `kan_r5_h1_n8.point.json`.

Paths above are relative to `research-20260929`. Commit these with, or after,
all changes named in `publication/reviews/minor-fixes/FILES.json`, including
round 2, the lnts center repair and `nn_exact.py`, and the integration changes
to `open-instances-summary.md` and `bound-audit/audit-report.md`. The package
also requires its imported OSIL parser, the three new portability edits and
all applied scientific script edits. Original ignored inputs remain in the
archive; EG `.retry.sol` files are already archived. The file list records
these dependencies without changing any file owned by another agent.

If integration changes summary table rows, run
`python3 research-20260929/publication/reproduction/tools/build_result_maps.py`
first so the maps retain the final wording. After **all** track, integration
and package edits are finished, run from the repository root,
**as the last step before committing together**:

```bash
python3 research-20260929/publication/reproduction/tools/rebuild_manifest.py
python3 research-20260929/publication/reproduction/tools/check_package.py
```

If anything covered by the manifest changes afterwards, run both again.
Do not rerun `build_package.py` or scientific experiments to refresh hashes.
The default package check must pass; the intentional stale-manifest failure
recorded during this response does not satisfy that final check.

Targeted commands actually run for this response:

| command | result |
|---|---|
| `python3 research-20260929/publication/reproduction/tools/build_result_maps.py` | map files rebuilt; `logs/review-r1-map-build.log` |
| `python3 research-20260929/publication/reproduction/tools/smoke.py` | 25/25 strict relocated checks; `logs/review-r1-smoke-run.log`, `logs/smoke-results.json`, per-check logs, diffs and strace |
| disposable `python3 -B <5a-copy>/check_display.py` for committed and rerun fixtures | 84/8/1 and 80/12/1; exact argv in `logs/review-r1-evidence-check.log` |
| isolated `bwrap … python3 <copy>/publication/reviews/repro-package-r1/5b/cops_summary_check.py` | saved-file arithmetic agrees with 5b; full argv in `logs/review-r1-evidence-commands.json`, output in `logs/review-r1-cops-check.log` |
| `python3 research-20260929/publication/reproduction/tools/check_review_response.py` | comparison, numeric-token and stale-manifest regressions pass; `logs/review-r1-regressions.log` |
| `python3 research-20260929/publication/reproduction/tools/check_relocated_paths.py` | new imports and builder pass only in the isolated copy; exact subprocess argv in `logs/review-r1-relocated-paths.json` |
| `python3 research-20260929/publication/reproduction/tools/check_package.py --checks maps syntax patches smoke` | targeted groups pass: 2,423 numbers, 150 Python / six shell syntax checks, 12 patch replays, 25 smoke checks; `logs/review-r1-package-check.log` |
| `python3 research-20260929/publication/reproduction/tools/check_package.py` | exit 1 as required: 11 stale/unlisted manifest entries; `logs/review-r1-stale-manifest-check.log` |
| `git diff --check -- research-20260929/publication/reproduction research-20260929/open-instances-scout/hvycrash_check.py research-20260929/open-instances-scout/structure.py research-20260929/treewidth-census/census.py` | whitespace check; `logs/review-r1-diff-check.log` |

The initial numeric check caught a shortened powerflow endpoint in my new
explicit mapping; I corrected it to the complete token. Patch replay also
caught the concurrent `nn_exact.py` comment change, which I inspected and
recorded. Final targeted groups passed. No project-wide verification or CI
inspection was run; no commits, pushes or outside contact occurred.

## Response to integration review r1

I accepted items **2** and **15** of
`publication/reviews/integration-review-r1.md`. The package now traces the
stored eg_disc2_s all-leaf evidence. The historical retry sample is labelled
as history. The current result is **1,114,361 certified leaves, zero
failures, under A1/A2**; **1,152,830 counts processed boxes**. Exact coverage
and the separate **10,404-leaf** interval sample without a libm assumption
remain distinct claims. No full certification or tree-generation run was
repeated.

The README lists the stored inputs, commands, outputs and expected results.
`result-map.json` includes the eight recorded trees, all 38 chunk NPZs and
logs, reviewer-derived leaves, coverage/model/bookkeeping evidence and
interval-sample outputs. `commands.json` adds **54** EG records, including
the historical expensive commands, which are explicitly marked not to
repeat for packaging. `tools/build_result_maps.py` preserves this index
when it rebuilds the maps. It now selects result tables by their header;
the first rebuild exposed duplicate instances from the newly added
per-KAN gap and literature tables. The corrected rebuild maps each of the
43 summary instances exactly once and retains the 46 audit instances.

Manifest scopes now include `publication/eg-recheck/` and
`publication/reviews/eg-recheck-r1/`. The standalone EG review and the two
corrected literature reports are explicit manifest dependencies. The stored
EG data in those scopes are tracked, so they do not need a new archive.
**The main `manifest.json` was rebuilt on 2026-10-04 by this integration
implementation task**, after all covered edits and the result-map rebuild.
The default `check_package.py` passed. The selected-group results below
are historical; the final default result is recorded in the r2 response.

The README's eg_int_s and eg_disc_s primal displays are now
**6.4531031593842275** and **5.7605396164535107**, respectively, both rounded
up from the saved `.retry.sol` objectives. The named waterno2_06 row in
`literature/network/report.md` now uses **282.888038** and **≤ 1.68%**. Its
former 282.888 primal display was below the exact point objective as well
as having a downward-rounded gap. The small-model report now gives the
all-leaf result with its assumptions and exact coverage proof. Each report
has a one-line response note. **Nine exact rational checks passed**, using
saved point objectives and the exact lower certificate; the water gap was
also checked against one and both outward-rounded displays. Fractions and
directions are saved in `logs/integration-r1-displays.json`.

The disposable copy was `/tmp/repro-eg-integration-r1-81qsbigg`, also
recorded in `logs/integration-r1-eg-smoke.json`. Bubblewrap hid both
source checkouts and the original cache; the copied OSIL model matched its
pinned SHA-256. Three sequential checks passed in **7.13 s** total:
the saved all-leaf summary, **29/29** interleaved leaves of part 7 through
`recheck_leaves.py` (including its tree-coverage check), and **64/64** leaves
(eight per part) with the unchanged certifier. Exact row-margin replay also
agreed. All three checks made **zero successful source-tree opens**, as
recorded by strace. The driver limited affinity to four CPUs and set one
BLAS/OpenMP thread. Scientific scripts ran only in the disposable copy.

Commands actually run from the repository root (stdout/stderr saved in the
listed logs):

| command | result / evidence |
|---|---|
| `python3 -B research-20260929/publication/reproduction/tools/build_result_maps.py` | first attempt failed on duplicate table rows; corrected rebuild passed, 43 summary / 46 audit instances; `logs/integration-r1-map-build.log` |
| `python3 -B research-20260929/publication/reproduction/tools/check_integration_displays.py` | 9 exact rational checks passed; `logs/integration-r1-display-check.log`, `logs/integration-r1-displays.json` |
| `python3 -B research-20260929/publication/reproduction/tools/check_eg_relocated.py` | 3 relocated checks passed; no full recheck; `logs/integration-r1-eg-run.log`; exact subprocess argv, timings and hashes in `logs/integration-r1-eg-smoke.json` |
| `python3 -B research-20260929/publication/reproduction/tools/check_package.py --checks maps syntax patches smoke` | passed: 2,425 numeric references, 54 EG commands, 150 existing Python / 6 shell syntax checks plus 23 EG Python scripts and package tools; 12 patch replays, 154 identical outputs and the two previously inspected differences preserved; 25 existing smoke records revalidated and 3 new EG checks validated; `logs/integration-r1-package-check.log` |
| `git diff --check -- research-20260929/publication/reproduction research-20260929/publication/literature/network/report.md research-20260929/publication/literature/small/report.md` | passed; `logs/integration-r1-diff-check.log` |

An inline `python3 -B -` check also checked all 17 authored text files,
including untracked files, for trailing whitespace; it passed. Its exact
stdin and the command argv above are retained in
`logs/integration-r1-commands.json`.

The 25 earlier scientific smoke commands were not rerun; their retained
outputs were revalidated by the selected package check. No historical
`*.prev.md` file was changed, and the README and result/audit maps do not
source a number from one. `open-instances-summary.md`,
`bound-audit/audit-report.md` and `publication/READINESS.md` were not edited.
There is no disagreement with the two assigned findings. No project-wide
verification, CI inspection, commit, push or outside contact occurred.


## Response to integration review r2

All nine findings in integration-review-r2.md were checked against saved
evidence and accepted. Exact Fraction checks confirm the upward EG and
water primal displays and historical closeness bounds. The original
closures used tolerance-feasible points; exactly feasible points now
cover all 13 in publication/primal/.

The command index now names the recorded-tree OSIL, listed point and
producer modules, plus OSIL and sample C minF inputs for the interval
samples. The result map selects eg_disc_s part 1, the smaller bound. The
README retains its exact-decimal-versus-binary64 qualification and labels
EG timing totals as summed wall time. The relocated smoke tool writes
fresh output, requires bwrap/strace and removes its scientific copy.
It preserves the original integration-r1 smoke records.

Literature reports, checks, logs and SHA-256 source manifests are commit
dependencies. Source copies stay local and untracked; the paper data
release must not redistribute copyrighted sources. No release licence
was chosen, and no staging, commit, push or outside contact occurred.

This integration implementation task owns the final rebuild. On
**2026-10-04**, after all covered edits were final, it ran
**build_result_maps.py**, then **rebuild_manifest.py**, then the
**default check_package.py**, followed by the three targeted relocated
EG smoke checks; all passed. The 25 earlier smoke records were
revalidated by the default check. Scientific execution was confined to
disposable copies with at most four CPU cores and one BLAS/OpenMP thread.
Exact commands and outputs are recorded in
[publication/integration/commands.md](../integration/commands.md) and
[review-r2-package-check.log](../integration/review-r2-package-check.log).
These are targeted local checks; no CI or project-wide verification ran.
There is no disagreement with the review.
