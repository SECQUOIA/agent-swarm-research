Verdict: issues

# Review of the reproduction package (round 1)

Reviewer: independent review sub-agent (Claude), 2026-10-03.
Package: `research-20260929/publication/reproduction/`.
Working files: `publication/reviews/repro-package-r1/` (`PROGRESS.json`, `checks/`, `smoke/`, `5a/`, `5b/`).

## Summary

The package does what it claims for traceability and portability. There are no blockers. One issue is major: the list of files to commit does not mention that the package depends on uncommitted minor-fixes files. The other issues are minor documentation and map corrections.

- **Script edits are path-only.** The package's 152 edited scientific files change no numerical formula, constant or argument. I compared every changed line's numeric literals. I evaluated the old and new module-level path constants with `__file__` set to each script's real location. I replayed all 11 patches onto HEAD copies: 152 of 153 owned files are byte-identical to the working tree.
  - Three path constants changed on purpose: two GAMS tools found on `PATH`, and the COPS display checker moved from the clean worktree to this checkout.
  - The only non-path addition is `np.save` of the optcdeg2 multipliers. It writes extra output files and changes no value.
- **The "lnts center change"** is in `publication/primal/lnts/lnts_primal.py`. The minor-fixes agent made it (`reviews/minor-fixes/summary.md`, issue primal/lnts 1). It corrects an invalid Krawczyk step: the second step's centre must lie in the step-1 box Z, so it now uses `mid(Z)`. It changes no number in `open-instances-summary.md`, which uses the original first-wave lnts primal values. The minor-fixes check reports unchanged 25-digit objective displays. The package report handles it correctly but does not say who made it.
- **Relocated reruns match.** I built my own copy at `/tmp/rp-review-vL2EPk` from `git ls-files` plus `required-new-files.json`. The main tree, the clean worktree, the package's own smoke copy and the real OSIL cache were hidden with `bwrap`.
  - `prepare_inputs.py` restored 2063 inputs, all with the main tree's hashes, and verified 95 OSIL models. It rejected a tampered model.
  - Seven smoke checks exited 0 and matched the saved outputs except for timing fields: lnts50-tight, optcdeg2, chain50, ex6_2_7, powerflow0030p-stored, waterno2_06-cellslopes and audit-ghg_3veh.
- **Result and audit maps are sound.** All 43 summary rows and the audit map's 46 instances name existing files with matching hashes. The numbers I sampled are present in the saved outputs. All 131 classified pairs agree with `bound-audit/results.json`. Some rows name the wrong output file (issue 5).
- **Open discrepancies:**
  - (a) The water-audit difference comes from regenerated topopt p5 inputs, not from the report. **84/8/1 is correct; the audit report needs no change.**
  - (b) **No COPS number in `open-instances-summary.md` has to change** under its current wording. One change is conditional on the planned removal of the "no exactly feasible point" sentence (issue 7).
  - (c) The summary's powerflow0030p value is backed by the exact replay.

**Reviewer incident.** At 22:13:39 my first version of `checks/path_equiv.py` evaluated module-level expressions with Python builtins available. Four review scripts open their log for writing at module level, so this truncated four tracked files in `reviews/pindyck-review-checks/logs/`: `final_bound.log`, `hess_check.log`, `own_ranges.log` and `primal_check.txt`.
- I restored them within minutes with `git show HEAD:<path> > <path>`. Their SHA-256 hashes now equal the package manifest (a1e6a9c4…, f9632dd2…, a04d6cc6…, 3044586d…), and `git status` is clean for them.
- The checker now evaluates without builtins. Its rerun gave the same result and modified no file.
- No other file outside my review directory was written.

## Issues

### 1. major: the files-to-commit list omits the package's dependency on minor-fixes files

**Location:** `report.md` "Files that must be committed"; `required-new-files.json`; `manifest.json`.

**Evidence:** `manifest.json` hashes 18 files at their minor-fixes versions:
- five untracked `minor_review_check.py` files (in `publication/primal/{chain,dtoc5-lukvle10,lnts,powerflow}/` and `publication/primal/water-ann-kan/code/`), which are not in `required-new-files.json`;
- 13 tracked files modified by minor-fixes and not owned by the package: the five `publication/primal/*/report.md` files, `dtoc5-lukvle10/gaps.py` and the seven `water-ann-kan/points/*.point.json` files.

In my copy built from tracked files plus the required list, the manifest check finds 5 missing files (`copy_manifest_check.txt`). If the package is committed without the minor-fixes changes, `check_package.py` fails.

**Fix:** state in `report.md` that the package must be committed with, or after, the minor-fixes changes, naming `reviews/minor-fixes/FILES.json`. Alternatively, rebuild the manifest after the minor-fixes commit. Also name the minor-fixes agent as the author of the lnts centre change.

### 2. minor: README catmix primal commands lack a required argument

**Location:** `README.md` lines 163–164.

**Evidence:** `catmix_primal_snap.py` reads `thr = float(sys.argv[2])`, so `python3 catmix_primal_snap.py 400` raises `IndexError`. `commands.json` and `cops/report.md:157` use `catmix_primal_snap.py 400 2e-3` and `800 2e-3`.

**Fix:** add `2e-3` to both commands.

### 3. minor: per-instance README commands overwrite shared saved evidence

**Location:** `README.md` lines 82–85 (`v_lnts.py N`, "same file") and lines 87–90 (`v_camshape.py N`).

**Evidence:** both scripts write all their arguments' results to one file (`logs/lnts_verify.json`, `logs/camshape_verify.json`). Running `v_lnts.py 50` replaced the four-record saved file with a single record in my copy. Run one instance at a time, as the README shows, and only the last instance remains. Other commands also rewrite tracked evidence in place, for example `chain_bound.py` (`logs/chainN_bound.json`) and `run_kraw.py` (`logs/kraw_<point>.json`). The README warns about this only for `pf_cert.py`.

**Fix:** give the saved forms `python3 v_lnts.py 50 100 200 400` and `python3 v_camshape.py 100 200 400 800`. Add one sentence: commands write into the saved `logs/`, so run them in a disposable copy, or check `git diff --stat` and restore afterwards.

### 4. minor: the README does not explain the water-audit 80/12/1 rerun, and the topopt p5 certificate depends on the thread count

**Location:** `README.md` lines 484–487; `report.md` "Open issues" item 3.

**Evidence:** see `repro-package-r1/5a/findings.md`. The checker and `audit-report.md` are identical in the clean worktree, HEAD and the working tree. The water-audit chain (`water-audit/tools/chain_c.sh`) reran `cert_topopt.py` before running `audit.py classify` and `check_display.py`.
- `cert_topopt.py` picks its basis by QR column pivoting, so the result depends on the BLAS thread count.
- With 1 thread, as the README prescribes, the exactly feasible repaired p5 point has objective 10.33547432783171797…. The committed point has 10.335474327803234…. A 2-thread run gives a third valid point.
- The audit's four p5 displays `[10.33547432780, 10.33547432781]` (`audit-report.md` lines 94, 217, 550, 805) are correct for the committed certificate, but fail against the regenerated one.
- The other eight printed failures are the quotations explained at `audit-report.md` lines 1167–1170. The skip is the histogram row at line 158.
- I reproduced both counts in the scratch copies: 84/8/1 with committed inputs, 80/12/1 with regenerated ones.

**Correction:** `audit-report.md` needs none; its 84/8/1 is correct. The package README should replace the bare 80/12/1 versus 84/8/1 statement with:

> The rerun regenerated the topopt p5 certificate. `cert_topopt.py` chooses its basis by pivoted QR, which depends on the BLAS thread count, so it found a different exactly feasible point (objective 10.3354743278317…). The four topopt p5 displays then fail. With the committed certificate, `check_display.py` gives the report's 84/8/1. Class, margins and verdict are unchanged.

Optionally, `audit-report.md` line 217 could note that the repaired point depends on the chosen basis.

### 5. minor: some result-map rows name an output that does not contain the reported number

**Location:** `result-map.json`.

**Evidence:**
- **catmix400 and catmix800:** the map lists `tree400_final.json` and `tree800_final.json`, which do not contain the bounds −0.04805654782467129 and −0.04805590147967565. Those are in `reviews/catmix-recheck-checks/logs/catmix400_final.log` and `catmix800_final.log`.
- **lukvle10:** the primal 352.2380254064961 is in `reviews/open-instances-verification/logs/lukvle10_prep.json`, which is not listed.
- **eg_*:** the primals are in `open-instances-wave3/eg/retry/sol/*.retry.sol`, which are not listed.
- **waterno2_09–24:** the sums are in `reviews/waterno2-verification/logs/vsum.log` and `reviews/waterno2-recheck/logs/vsum2.log`. Only the period `cert_TT` files are listed.

All the files exist and are in the manifest, so this is a map completeness problem, not missing evidence.

**Fix:** add these outputs to the corresponding rows.

### 6. minor: README catmix table uses three of the five unsafe decimal strings

**Location:** `README.md` lines 174–177.

**Evidence:** the table gives −0.04805914560067171 (catmix200 author), −0.04806943203114456 (catmix100 reviewer) and −0.04805590147967565 (catmix800 recheck) as bounds. These are shortest binary64 representations above the exact binary64 bounds, so they are not valid lower bounds. The chain table at lines 144–146 carries a caveat; the catmix table does not. `cops/report.md` lines 65 and 69 also say two of these strings are in the summary, but they are not in `open-instances-summary.md`.

**Fix:** use the safe forms −0.048059145600671712, −0.048069432031144562 and −0.048055901479675652, or add the same caveat as the chain table. Correct `cops/report.md` lines 65 and 69 to name the COPS verification report instead of the summary.

### 7. minor: COPS findings for the summary and detailed notes

**Location:** `open-instances-summary.md` lines 33–34 and 43–46; see `repro-package-r1/5b/findings.md`.

**Evidence:** all OSIL models minimize.
- Chain duals: `5.06862` ≤ chain400 L = 5.0686216946040092…, and `5.07226` ≤ chain50 L = 5.0722614939828627….
- Chain gaps against the summary's double primal points: 9.63e-15, 9.90e-15, 9.34e-15 and 9.81e-15, all ≤ 1.0e-14.
- Catmix duals: `−0.04806944` and `−0.04805591` are below both the author and verifier bounds.
- Catmix gaps: 1.6497e-13 ≤ 1.65e-13 for N = 100, and 1.484e-10 ≤ 1.5e-10 for N = 800.
- None of the five unsafe strings appears in the summary.

**Corrections to `open-instances-summary.md`:**
- None under the current wording.
- Conditional: the integration notes ask to remove the lines 43–46 statement that no exactly feasible chain point was constructed. If line 33 is then measured against the exact chain points or the 60-digit KKT value, chain100's gap is 1.00276e-14. In that case change `same to 1e-14` → `within 1.1e-14` and `≤ 1.0e-14` → `≤ 1.1e-14`, and reduce line 181's count of tolerance-feasible closures ("13 of them") by four.
- Optional: the listed-dual column `0.0826` is the listed 0.08256615 rounded to nearest. The outward form is `0.0825–0.1745`.

**Detailed notes, not the summary:** the understated gaps and the unsafe-string locations are listed in `5b/findings.md`. Examples:
- `open-instances-wave2/cops/report.md` lines 19–26: 9.4e-15→9.7e-15, 9.9e-15→1.0e-14, 9.0e-15→9.4e-15, 7.9e-12→8.0e-12, 1.9e-10→2.0e-10 and 5.1e-10→5.2e-10;
- the same note's relative gaps at lines 280–283: 1.6e-10→1.7e-10 and 4.0e-9→4.1e-9;
- `reviews/catmix-recheck.md` lines 36–37 widths: 6.8e-11→6.9e-11 and 1.48e-10→1.49e-10. The package's `cops/report.md` repeats 1.48e-10.

### 8. minor: remaining absolute paths and an unhashed cross-directory input

**Location:** scripts listed by `grep -rln /workspace/local-home --include=*.py research-20260929`; `manifest.json` scopes.

**Evidence:** no script with an absolute path is named in `result-map.json`, `audit-map.json` or `commands.json`, and none is a README entry point.

Should be fixed, or marked historical in the README:
- `open-instances-scout/hvycrash_check.py` (in the manifest). It is the author's structural check behind hvycrash's "objective constant" claim. The summary row is also backed by portable `hvycrash.py`, which passed its smoke check, and `v_hvycrash.py`. It has one hard-coded `sys.path` line.
- `open-instances-scout/structure.py` (in the manifest).
- `treewidth-census/census.py`. It produces `census_merged.json`, upstream of the scout's 283 candidates, which the summary reports at line 177. It is not a rerun target, but it has one hard-coded line.

No fix needed, because none produces a number in the summary or the audit report:
- `theory-bangbang/singular/catmix_trap.py` (singular-arc theory);
- `publication/solver-runs/driver.py` (separate campaign, owned by another session; GAMS path);
- `publication/literature/network/checks/*.py` (literature cross-checks of prose claims);
- `publication/minlplib-status/history.py` (GAMS);
- the review directories under `publication/reviews/`, and `reviews/*-checks` for theory notes outside the two documents;
- `publication/reproduction/control/tmp/stage1/`, a tracked historical staging copy.

Separately, the first-wave bound scripts (`lnts_bound.py`, `camshape_bound.py`, `dtoc5_bound.py`, `optcdeg2_bound.py`, `osil_eval.py`) import `research-20260922/scouting/minlplib-open-data/osil.py`. That directory is outside the manifest scopes and is not mentioned in the README. `smoke.py` copies it explicitly.

**Fix:** add `research-20260922/scouting/minlplib-open-data/osil.py` to the manifest and mention it in the README. Make the scout and census files portable, or label them historical.

### 9. minor: the smoke comparison is permissive

**Location:** `tools/smoke.py` `main()`.

**Evidence:**
- When the output contains a JSON object, the code requires only that each object occurs among the reference's objects, and it ignores non-JSON lines.
- Otherwise it requires only that each output line occurs among the reference lines, so an empty output would pass.

I made a stricter line-level comparison of all 25 saved smoke logs, after normalizing paths and timings. Every output line occurs in its reference, and every log is non-empty. The single-instance runs are subsets of multi-instance references. The claim holds, but the code does not enforce it.

**Fix:** also require non-empty output and compare the non-JSON lines.

### Confirmed with no issue

- **powerflow0030p (5c):** the stored-certificate replay gives L = 576.893412298800469849159…, with `L == bound_exact`. The summary's 576.8934122988004 ≤ L. The primal 576.8934134704 ≥ obj(p1) = 576.89341347037138687. `open-instances-wave3/logs/powerflow0030p.sdpcert.json` is unchanged from HEAD. A fresh `pf_cert.py` gives 576.8905424271796, a weaker but different numerical solve, as the package states. The summary value rests on the replay of the saved multipliers.
- **ex6_2_7 smoke:** the reference `small/logs/A16_…out` shows `"sec": 73.4`, while the tracked BB JSON and both reruns show `50.0`. This is a timing field from an earlier regeneration; the node count and all values are identical.
- **Recovered `catmix_primal_snap_eval.py`:** it rewrites the saved outputs byte-identically, according to `cops/report.md`. Its smoke check matched.

## Commands run

All commands were run from `/workspace/minlp-notes` unless stated. They were sequential, used one BLAS thread, and needed at most about 4 CPU cores. These are targeted checks only; no project-wide verification was run and CI was not inspected.

```bash
# 1. Diffs
git diff --stat -- research-20260929; git diff --numstat -- research-20260929
# compared numeric literals in removed and added lines of the 152 owned files (inline python; no differences except shell paths)
python3 research-20260929/publication/reviews/repro-package-r1/checks/path_equiv.py   # 130 constants equal; 3 intended differences
#   (first version truncated four pindyck logs; restored with:)
for f in final_bound.log hess_check.log own_ranges.log primal_check.txt; do p=research-20260929/reviews/pindyck-review-checks/logs/$f; git show HEAD:$p > $p; done
# independent patch replay: HEAD copies of the 153 owned paths into /tmp/rp-patchreplay-Ua8L (git init), then
git apply --unsafe-paths <control 01-03, cops 01-04, small 01-02, water-audit 01, patches/01-remaining-portability>
# compared with the working tree: only publication/primal/lnts/lnts_primal.py differs (centre change)

# 2. Relocated copy, input restore and smoke reruns
# copy of git ls-files research-20260929 research-20260922/scouting/minlplib-open-data + required-new-files.json -> /tmp/rp-review-vL2EPk; 95 OSIL -> $T/osil
checks/sandbox.sh $T $T/minlp-notes python3 research-20260929/publication/reproduction/tools/prepare_inputs.py   # restored 2063, verified_osil 95
# restored-vs-main-tree hash comparison: 0 mismatches; tampered alkyl.osil -> AssertionError "cache model differs"
python3 research-20260929/publication/reviews/repro-package-r1/checks/run_smoke.py   # 7 checks, all exit 0
diff <(normalized mine) <(normalized package smoke log / historical reference)   # only timing fields differ
# stricter line-subset comparison of all 25 package smoke logs against references (inline python)

# 3. Maps
# inline python: existence and hash of every file in result-map.json (43 rows) and audit-map.json (46 instances);
# numbers searched in outputs; 131 pair classes compared with bound-audit/results.json; 14 sampled pairs checked against their enclosures
grep -c <number> <output>   # lukvle10, chain200, catmix200/800, pindyck, eg_int_s, kan_r5_h1_n3, waterno2_09/24

# 4. Absolute paths
grep -rln /workspace/local-home --include=*.py research-20260929
# intersected with map scripts, manifest .py and commands.json scripts; grep of research-20260922 imports

# 5. Discrepancies
checks/sandbox.sh ... python3 run_root.py powerflow0030p        # (5c) in the relocated copy
(cd 5a/scratch/committed && python3 -B check_display.py)         # ok 84, failed 8, skipped 1
(cd 5a/scratch/rerun && python3 -B check_display.py)             # ok 80, failed 12, skipped 1
# delegated agent, 5a: cert_topopt.py p5 with 1 and 2 BLAS threads in a scratch copy (136 s and 114 s)
# delegated agent, 5b:
OMP_NUM_THREADS=1 python3 5b/cops_summary_check.py > 5b/cops_summary_check.log   # about 1 s, saved files only

# 6. Commit list
# inline python: manifest/map/commands.json paths versus tracked + required-new-files + archive members;
# untracked non-ignored files; manifest hash check in the relocated copy (copy_manifest_check.txt)
```

The 5a and 5b investigations were run by delegated agents. I checked their key results myself: I reran `check_display.py` in both scratch copies and spot-checked the 5b log.
