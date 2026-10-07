Verdict: issues

# Independent review of the publication integration, round 2

Reviewer: independent final verifier. Date: 2026-10-04. Scope: the responses to
[integration review r1](integration-review-r1.md) in `research-20260929/open-instances-summary.md` (S),
`research-20260929/bound-audit/audit-report.md` (A) and `publication/READINESS.md` (R), and the
package owner's response in `publication/reproduction/` (README.md, report.md, result-map.json,
commands.json, tools) and in the literature track reports. Paths are relative to `research-20260929/`
unless they start with `publication/`-relative names used inside R. Evidence is in
[integration-r2/](integration-r2/): `diff-*.txt` (diffs against the round-1 snapshots), `scratch/`
(my own exact checks), `lead-smoke/` (my relocated eg smoke run), and three helper folders
(`agent-licence/`, `agent-lit/`, `agent-repro/`). I did not edit any document.

## Summary

**All 15 round-1 issues are addressed, and no recomputed number is wrong.**
- **The baseline is sound.** The round-1 snapshots in `publication/integration/review-r1-before/` were taken 14 minutes after review r1. They reproduce every line number that r1 quotes: S:161–162 blank lines, S:163 "Martín", S:268, S:346, A:668, A:917, R:27, R:33, R:117, R:131.
- **Every diff hunk traces to an r1 item.** S changed in 13 hunks, A in 7 and R in the rows and sections listed in its response table. No closed-table, KAN, water or ann result cell changed. Every new number I recomputed exactly is correct, apart from the downward-rounded closeness figures (issue 2).
- **The tables now render.** markdown-it 4.0 parses 5 tables in S, including the 43-row literature table, 10 in A and 4 in R. No table row is orphaned.
- **The eg timing disagreement holds.** `eg-recheck/recheck_leaves.py:128,143,155` and `run_cert.py:45–62` use `time.time()`, which measures wall time.
  - The 38 NPZ `time` fields sum to 41,162.198 s. The printed whole seconds sum to 41,151.
  - The scheduler finished after 5,372 s (`logs/run_cert.out`).
  - The eg report's "CPU s" label is therefore wrong. R:144–149 states this correctly.
  - The same mislabel remains in several other places (issue 4).
- **The computing-environment section matches the sources.** I checked it against /proc/cpuinfo, /proc/meminfo, uname, /etc/os-release, `ldd`, `numpy.show_config()`, `environment.json`, `requirements.txt` and `environment-r1.json`.
  - The host has 18 cores and 36 CPUs; 49,321,416 KiB = 47.0366 GiB. The kernel and Ubuntu versions, AVX2/FMA/AVX-512, OpenBLAS 0.3.33.112.0, AVX512_SPR, glibc 2.39 and the pinned versions all match.
  - All 51 runtime-table values equal the `wall_s` fields of the cited `commands.json` records, in order. All 51 records have exit code 0 and output files with matching SHA-256 (`scratch/check_runtime.py`).
  - The shared-machine caveat and the incomplete original-run metadata are both stated, and the release licence is left to the user.
  - Two licence rows misstate their sources (issue 6).
- **The reproduction changes are correct.** The eg_disc2_s all-leaf evidence is mapped correctly: 1,114,361 leaves certified, 0 failures, 1,152,830 processed boxes, 38 chunks, and a 10,404-leaf interval sample. All of these were recomputed from logs and NPZ files.
  - All 54 EG command records and the 159 map paths resolve, and their hashes match.
  - The corrected README primal displays are at or above the exact objectives: eg_int_s by +9.1e-17, eg_disc_s by +9.4e-17.
  - I ran two of the three relocated eg smoke checks in my own disposable copy: the saved summary and the 29-leaf part-7 recheck. Both reproduce the recorded output.
- **What remains:**
  - one major packaging defect: `publication/literature/` is git-ignored;
  - eight minor issues: two summary sentences whose wording came from r1 itself, leftover "CPU" labels, stale bookkeeping in R, licence-row wording, remaining stale displays in track reports, package-map details, and small nits.

There are no blockers, 1 major issue and 8 minor issues.

### Round-1 items

| r1 item | status | evidence |
|---|---|---|
| 1 literature table | resolved | S:165 is one table with 43 body rows of 3 cells (markdown-it; helper also used `pandoc -f gfm`) |
| 2 eg_disc2_s package coverage | resolved in the package; R not updated (issue 5) | README.md:255–300, result-map.json `all_leaf_recheck`, 54 `eg-recheck/` records; manifest deliberately stale |
| 3 environment, timings, licence | resolved; licence rows need two corrections (issue 6) | R:87–168, environment-r1.json, runtime-evidence-r1.json |
| 4 gap-source list | resolved | S:64–67 now matches every row in `integration/check_numbers.py` that uses a displayed dual: lnts, dtoc5, lukvle10, pindyck, eg ×3, chain (safe displays) and pricing050 |
| 5 eg_disc_s display | resolved | S:91–93. My own check: the display exceeds `float('5.760539610694994')` by 2.3820e-16 |
| 6 literature labels/wording | resolved (all 9 sub-items and the 3 paper bullets checked against the reports) | `agent-lit/findings.md`. Small residues in issues 7 and 9 |
| 7 SCIP scope | resolved, but one sentence overstates (issue 3) | S:297–303, A:940–943, `scip-bug/report.md:36, 92–108` |
| 8 rounding scale, spring bisection | resolved | S:273–276, A:670–676. `audit-ir/logs/xcheck_scip.log`: SCIP 0.846245664643154 vs exact 0.846245665643154, a difference of exactly 1.0e-9 |
| 9 model history | resolved | S:281–283, A:753–756, A:921–929, R:47. Nine instances, as in `minlplib-status/report.md` Table B1 |
| 10 review facts | resolved | R:49–53 match `solver-campaign-review-r1.md:10` (two major), `solver-campaign-r2/PROGRESS.json` (`"done": []`), `solver-analysis-review-r1.md` (2 major, 4 minor) and `minor-fixes-review-r2.md:38, 44–45` (1 major at `scip-bug/report.md:173`, 10 minor). The parent-check statements have no linked record (issue 9) |
| 11 R wording | resolved | R:16–19, 30, 36, 41 |
| 12 earlier closeness | restored, but rounded down (issue 2) | S:353–354 |
| 13 old SCIP incumbent | resolved | S:314–318. `solver-runs/point_checks.log:6`: deficit at least 1.5191e-7, row violation 7.7174e-10 |
| 14 audit details | resolved | A:285–287 (methanol50 LINDO 0.00802826, 15 Feb 2022, from saved page data); A:1381–1385 |
| 15 stale displays | partly resolved | README:242–243 and network:277 are fixed and valid; small:494–496 is fixed. Other stale displays remain (issue 7) |

## Issues

### Major

1. **The literature reports and their evidence are git-ignored, so the planned commit cannot include them** (major; packaging and publication integrity)
   - **Location:** `/.gitignore:2` (`literature/`); `publication/reproduction/files-to-commit.json`; R:182–187 (commit step).
   - **Evidence:**
     - `git check-ignore -v publication/literature/small/report.md` reports `.gitignore:2:literature/`.
     - Of the 320 paths in files-to-commit.json, 25 are ignored (list in `integration-r2/scratch/ignored_files_to_commit.txt`). They include all three literature reports, their `checks/` and `sources/` files, and the MATPOWER case files cited in R:162.
     - `git ls-files research-20260929/publication/literature` is empty.
     - S links these reports 44 times. R rows 33, 35, 36, 43, 44 and 48 rest on them. A plain `git add` of the dependency list refuses these paths, and a commit made without them leaves the novelty evidence and links missing.
     - The rule exists for the untracked root `literature/` collection, which does exist.
     - Round 1 did not detect this.
   - **Fix:**
     - Change `.gitignore` line 2 from `literature/` to `/literature/`, which still ignores the root collection.
     - Confirm with `git check-ignore --stdin < files-to-commit paths` that no listed path is ignored.
     - Add to R's commit step (R:182) and to "Release preparation still pending" (R:258): "publication/literature/ is currently ignored by .gitignore:2; narrow the rule to /literature/ before committing."
     - The `.gitignore` edit is the user's or package owner's decision; no reviewer made it.

### Minor

2. **The restored historical-closeness figures are rounded down** (minor; S:353–354, R:231)
   - **Evidence:** my exact check (`scratch/new_numbers.py`; the integration's own `review-r1-evidence.log` agrees):
     - camshape100: (−4.28414712174675 − (−4.28415233)) / 4.28414712174675 = **1.2157e-6**;
     - lnts50: (0.5546687649381 − 0.55464755) / 0.5546687649381 = **3.8248e-5**.
     - "Within 1.2e-6" and "within 3.8e-5" are therefore false as bounds, and S's convention rounds such quantities upward.
     - The wording came from r1's own suggested fix; the control report's "within 1.2e-6" (control:84) has the same defect.
   - **Fix:** at S:353–354, write "were already within 1.3e-6 (camshape100) and 3.9e-5 (lnts50) relative of closure". At R:231, write "1.3e-6 … 3.9e-5". Optionally change control:84 the same way.

3. **"The wrong claims occur only for some random seeds" is false for period 4** (minor; S:300–301; also A:940)
   - **Evidence:** `scip-bug/report.md:93` gives p4 wrong runs as 19/20 (wheel 10.0.2), 8/10, 8/10, **10/10 (bin 10.1.0)**, 9/10 (master), **10/10 (GAMS/SCIP 10.0.3)** and 8/10. On 10.1.0 and GAMS/SCIP every tried seed was wrong. This sentence came from r1's suggested text.
   - **Fix:**
     - At S:300–301, replace the sentence with: "Whether a run is wrong depends on the random seed and version: for example p0 is wrong in 4/10 seeds on 10.0.2 and 0/10 on master, while p4 is wrong in all 10 tried seeds on 10.1.0."
     - At A:940, change "seed-dependent wrong optimality claims" to "wrong optimality claims (seed- and version-dependent)".

4. **Wall time is still labelled CPU time in the eg track and the package** (minor; the r1-response disagreement is upheld)
   - **Evidence:**
     - The measurements are wall time: `eg-recheck/recheck_leaves.py:128–155` and `open-instances-wave3/eg/retry/egbb.py:335, 428` both use `time.time()`. `retry.md:385` itself gives run G as "12,378 s (38 min wall)", so its parts ran concurrently.
     - The "CPU" label remains at:
       - `eg-recheck/report.md:41` (column "CPU s"), :51 and :163;
       - `eg-recheck/summarize.py` output ("41162s CPU"; reproduced in my smoke run);
       - `reviews/eg-recheck-review-r1.md:56`;
       - `publication/reproduction/README.md:289` ("41,162 CPU s", newly written in the r1 response, contradicting R:147–149);
       - README:244 ("12,378 s total CPU").
   - **Fix:**
     - README:289: "The 38 chunk timing fields sum to about 41,162 s of per-chunk wall time (time.time()); up to 12 chunks ran concurrently, and the scheduler finished after 5,372 s."
     - README:244: "12,378 s (sum of part wall times; 38 min elapsed)".
     - The eg-recheck owner should relabel report.md:41/51/163 "wall s (summed over chunks)" and the summarize.py message, or add a note there.

5. **R was not updated after the package owner closed items 2 and 15, and nobody owns the manifest rebuild** (minor; R:51, R:221, R:234, R:266–267; `reproduction/report.md:215, 374`; README:274)
   - **Evidence:**
     - R still says items 2 and 15 "remain with the parallel owner" (R:266–267) and are "Excluded" (R:221, R:234).
     - The package response (`reproduction/report.md`, "Response to integration review r1") completed both. R:51 does not mention the all-leaf package coverage or the new manifest scopes.
     - The package report and README hand the manifest rebuild to "the integrating agent". R:196–200 hands it to "its owner/user". Each document defers to the other.
     - `manifest.json` has 0 eg-recheck entries and 14 changed hashes (`agent-repro/manifest_staleness.log`).
   - **Fix:**
     - R:221 and R:234: "Resolved by the package owner; see reproduction/report.md, Response to integration review r1 (README, result map, 54 EG command records, relocated smoke checks; manifest not yet rebuilt)."
     - R:266–267: "Items 2 and 15 were resolved by the package owner, except the track-report displays in integration-review-r2 issue 7."
     - R:51 caveats: add "eg_disc2_s all-leaf evidence is mapped; manifest scopes include eg-recheck/ and reviews/eg-recheck-r1/, but manifest.json is not yet rebuilt."
     - Name one owner in all three places. For example: "the user or package owner runs build_result_maps.py, rebuild_manifest.py and the default check_package.py at commit time (R open decision 3)".

6. **Two licence rows misstate the sources' terms** (minor; R:161, R:162; evidence in `agent-licence/findings.md`, with saved copies and hashes in `agent-licence/sources/`)
   - **The MINLPLib and QPLIB rows match their sources.**
   - **SIF.** The four control SIF files (DTOC5, LUKVLE10, OPTCDEG2, OPTCNTRL) were downloaded from `bitbucket.org/optrove/sif` (`literature/control/sources/MANIFEST.md:40–43`).
     - That repository's LICENSE is "MIT License, Copyright (c) 2022 Nick Gould, Dominique Orban, Philippe Toint", not BSD.
     - The files are byte-identical to the ralna/SIF copies, which are BSD-3. HVYCRASH.SIF came from ralna/SIF.
   - **MATPOWER.** The LICENSE and manual Section 1.2 say "In most cases, the data has either been included with permission or has been converted from data available from a public source". R drops "In most cases".
     - The cited manual 8.0b1 is a beta. Manual 8.1 has the identical text.
     - Section 1.3 asks publications that use MATPOWER or its data files to cite it. QPLIB's index page also asks for a citation.
   - **Fix:**
     - R:161: add "The four control SIF files were downloaded from bitbucket.org/optrove/sif (MIT licence, © 2022 the same authors); they are byte-identical to the ralna/SIF copies. Include the notice of the source actually redistributed." Also change "retain" to "retain or reproduce".
     - R:162: write "'in most cases' included by permission or converted from public sources", and cite manual 8.1, Section 1.2.
     - Add a sentence: "MATPOWER (manual Section 1.3) and QPLIB request citation when their data are used."

7. **Stale displays and wording remain in track and package reports** (minor; continuation of r1 item 15)
   - **Evidence:**
     - `literature/small/report.md:391` (eg_int_s 6.4531031593842274) and :468 (eg_disc_s 5.7605396164535106) lie below the exact objectives. :517 ("unless the separate full recheck has replaced it") is outdated.
     - `literature/network/report.md:279` (2233.821) and :281 (6963.795) lie below the exact objectives. :278 "10.8%" understates the exact gap of 10.812%.
     - `literature/control/report.md:34, 115, 511, 550` still say "Martín".
     - `reproduction/report.md:178–179` says "Some primal closure values are only tolerance feasible", which contradicts S:350–351 (all 13 now have exactly feasible points).
   - **Fix:**
     - Use S's displays: …2275, …5107, 914.012 (≤ 10.82%), 2233.821346, 6963.795181.
     - Change :517 to "every leaf is certified under A1/A2; 10,404 leaves are also certified without the libm assumption".
     - Use "Martin".
     - In the package report, write "the original closures used tolerance-feasible points; exactly feasible points now cover all 13 (publication/primal/)".
     - Alternatively, list these files in R:258 as superseded by S.

8. **Package map and command details** (minor; from `agent-repro/findings.md`, with 3b confirmed by the lead)
   - **Evidence:**
     - The `eg-recheck/record-p{k}` records list only `egbb.py` as input. The OSIL, `open-instances-wave3/sol/eg_disc2_s.p1.sol`, `ev.py` and `egfast`/`egtm` are missing.
     - The interval-sample records omit the OSIL and the `minF_p*.npy` files that sample C needs; the result map also omits them.
     - The eg_disc_s "lower bound" evidence in result-map.json cites the non-binding `disc9_p0.log` value 5.7605396106949955. The binding value is `disc9_p1.log`, 5.760539610694994.
     - The README does not state the eg_disc_s binary64 caveat (S:91–93).
     - `check_eg_relocated.py` overwrites the recorded `logs/integration-r1-eg*` evidence on every run and leaves about 120 MB in /tmp (`/tmp/repro-eg-integration-r1-81qsbigg` still exists).
     - README:293 does not name the bwrap/strace prerequisites.
   - **Fix:**
     - Add the missing inputs in `tools/eg_evidence.py` and rebuild the maps.
     - Select the minimum part bound for eg_disc_s in `build_result_maps.py`.
     - Copy S:91–93's sentence after README:245.
     - Give `check_eg_relocated.py` a fresh output directory by default and remove its temporary tree on success.
     - Name bwrap and strace at README:293.
     - Optionally note that the eight `disc2_9_p*.npz` final checkpoints are byte-identical by construction (empty queues).

9. **Small wording and metadata points** (minor)
   - **R:41:** "closure; For eg_disc_s" should read "closure; for eg_disc_s".
   - **S:192:** the eg_int_s row still says "CAMINO’s Gurobi optimality claim …", without 13.0.0 or the status caveat, and with a curly apostrophe where rows 193–194 use a straight one. Use the eg_disc_s wording (small:41, 446, 449 apply it to eg_int_s too).
   - **A:3:** the header still says "Updated 2026-10-03", although A:1383 records 2026-10-04 changes. Add "; response to integration review r1 on 2026-10-04".
   - **R:89–92:** add "as seen inside the WSL2 VM". Under WSL2, the core count and the 47 GiB MemTotal are what the VM exposes, not necessarily the physical host.
   - **R:47–53:** these rows say the parent orchestrator checked fixes (status r2, lit-small, solver-analysis, minor-fixes round 3, package), but no record is linked, and R:239 says these are recorded "as the user specified". Write "(reported by the orchestrating session; no saved check record)", or link a record.

## Final consistency and what is still missing for the paper

**What is consistent.** The eg numbers agree across S:53 and S:84–89, R:41 and R:144–149, `literature/small/report.md:494–496`, `eg-recheck/report.md`, reproduction README:255–300 and report.md:352–356: 1,114,361 leaves, 0 failures, 1,152,830 boxes, 10,404-leaf sample, A1/A2. The exceptions are the time labels (issue 4). The SCIP, audit-ir, status and solver statements agree between S, A and R. Every summary row in `result-map.json` equals the current S row: S changed only prose and literature rows after the 00:12 map build.

**Still missing for a computational paper, in addition to the issues above:**
1. **A persistent public archive with a DOI and a data/code-availability statement.** R mentions none, and the release licence (R open decision 4) is a prerequisite.
2. **The final map, manifest and default package check, and a commit that actually contains `publication/literature/` (issue 1).**
3. **Citation obligations in the paper's references:** MINLPLib (CC BY attribution), QPLIB and MATPOWER (citation requests), and the Göß–Burlacu–Martin publisher correction (S:211).
4. **Timing presentation.** The runtime table gives wall times from reproduction reruns on a shared machine. The paper should say so and should not present them as original or CPU times. No original per-certificate CPU times exist.
5. **Optional outward-facing decisions** noted in r1, which R does not yet list: whether to inform the MINLPLib maintainers about invalid listed bounds, and BARON about its two contradicted optimality claims.

Nothing here contradicts a stated scientific claim. Every certificate, gap and count that I or my helpers recomputed is correct.

## Commands run

The lead ran these from `research-20260929/publication/` unless noted. Saved data was read with exact `Fraction` arithmetic. Scientific scripts were run only in disposable /tmp copies, with at most 2 cores and one BLAS thread. No main-tree file outside `reviews/integration-r2/` and this review was written.

```sh
stat -c '%y %n' reviews/integration-review-r1.md integration/review-r1-before/* ../open-instances-summary.md ../bound-audit/audit-report.md READINESS.md reproduction/*.md
grep -n -F '<r1-quoted strings>' integration/review-r1-before/*.md     # snapshot fidelity
diff integration/review-r1-before/open-instances-summary.md ../open-instances-summary.md > reviews/integration-r2/diff-summary.txt
diff integration/review-r1-before/audit-report.md ../bound-audit/audit-report.md > reviews/integration-r2/diff-audit.txt
diff integration/review-r1-before/READINESS.md READINESS.md > reviews/integration-r2/diff-readiness.txt
git diff --no-index --word-diff=plain integration/review-r1-before/READINESS.md READINESS.md
grep -n "time\.\|process_time" eg-recheck/{recheck_leaves,run_cert}.py ../open-instances-wave3/eg/retry/egbb.py
python3 -B reviews/integration-r2/scratch/eg_times.py          # 38 NPZ: 41162.198 s; logs: 41151 s, 1114361/1114361, 0 failures
tail -3 eg-recheck/logs/run_cert.out                           # 5372 s
grep "model name\|cpu cores\|siblings" /proc/cpuinfo; grep MemTotal /proc/meminfo; uname -a; grep PRETTY /etc/os-release; ldd --version
python3 -c "import numpy; numpy.show_config()"; cat reproduction/environment.json reproduction/requirements.txt
python3 -B reviews/integration-r2/scratch/check_runtime.py     # 51/51 records and hashes; table order matches
python3 -B reviews/integration-r2/scratch/new_numbers.py       # 2.3820e-16; 1.2157e-6; 3.8248e-5; 1.5191e-7; 7.7174e-10; 1.0e-9; 47.0366
python3 -B reviews/integration-r2/scratch/render_tables.py ../open-instances-summary.md ../bound-audit/audit-report.md READINESS.md reproduction/README.md eg-recheck/report.md
sed -n 36,100p integration/check_numbers.py                    # dual source per gap cell (item 4)
cat integration/review-r1-evidence.log; grep -n ... scip-bug/report.md; sed -n 1,12p solver-runs/point_checks.log; cat audit-ir/logs/xcheck_scip.log
head reviews/solver-campaign-review-r1.md; cat reviews/solver-campaign-r2/PROGRESS.json; grep -n major reviews/minor-fixes-review-r2.md
python3 - (result-map rows vs current S rows: 0 mismatches; eg map entries)
sha256sum ../open-instances-wave3/eg/retry/logs/disc2_9_p*.npz; python3 -c 'np.load(...)'   # identical final checkpoints
git check-ignore -v publication/literature/{small,network}/report.md; git check-ignore --stdin < /tmp/ftc_paths.txt   # from repo root: 25 ignored
cd /tmp && .../integration-r2/lead-smoke/run_two_checks.sh   # copy of agent script: summary + part-7 recheck in /tmp/lead-eg-r2-UmTgZywD
#   OSIL sha256 = pin 8849e06b…3289; summary exit 0, 1.43 s, TOTAL 1114361 leaves, 0 failures; chunk-subset exit 0, 2.95 s, 29/29;
#   0 source-tree opens (strace). The script's final cp line failed (my sed edit left "$T"/), so logs were copied by hand:
cp /tmp/lead-eg-r2-UmTgZywD/{summary,chunk-subset}.log reviews/integration-r2/lead-smoke/smoke-out/
diff (non-timing lines) lead-smoke/smoke-out/{summary,chunk-subset}.log vs reproduction/logs/integration-r1-eg/  # identical
git status --short publication/eg-recheck publication/reviews/eg-recheck-r1 ../reviews/eg-retry-review-checks   # no new changes
rm -rf /tmp/lead-eg-r2-UmTgZywD /tmp/agent-repro-eg-r2-KeujILsM /tmp/agent-repro-eg-r2-driver.log
```

Helpers (read-only in the tree; their findings were copied into their folders by the lead and spot-checked):
- **Licence:** curl/WebFetch of the MINLPLib, QPLIB, CUTEst/SIF (GitHub and Bitbucket) and MATPOWER pages, LICENSE files and manuals 8.0b1/8.0/8.1; `pdftotext`, `diff`, `sha256sum`. Copies are in `agent-licence/sources/`.
- **Literature:** sed/grep/diff over S, the snapshot, the three literature reports, the status report, the eg report and R; `render_check.py`; `pandoc -f gfm`; `git check-ignore`.
- **Reproduction:** `verify_eg_counts.py`, `check_eg_displays.py`, `run_eg_smoke.sh` (all three smoke checks in `/tmp/agent-repro-eg-r2-KeujILsM`, under bwrap with strace, with `taskset -c 0,1`), `compare_smoke.py` and `manifest_staleness.py`.

These are targeted local checks, not CI. No solver, project-wide verification or CI inspection was run. There was no commit, push or outside contact.
