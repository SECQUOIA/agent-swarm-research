<!-- Written to disk by the root from the structured return value of author of track repro-cops in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Clean reproduction of the COPS family: chain50–400 and catmix100–800

Track: repro-cops. Date: 2026-10-02. Worktree: `/workspace/minlp-notes-clean`, a detached checkout at commit c3514f03. Output folder: `research-20260929/publication/reproduction/cops/`, with `manifest.json`, `logs/`, `patches/` and `scripts/`.

## Result

**Every certificate, primal point and independent verification of the 8 instances was reproduced from the clean checkout. All certified numbers match the recorded values exactly.**

- **Runs.** 52 measured commands, all with exit code 0:
  - the authors' certificates and their primal points;
  - the cops-verification and catmix-recheck reviewers' independent code;
  - the primal-chain track and its reviewer.
- **Outputs.** Every regenerated output file is bit-identical to the committed file, with two kinds of exception:
  - wall-clock timing fields;
  - the metadata field `source_point` in `points/chainN_generator.json`, which records an absolute path.
- **Logs.** Every JSON object and text line of every log occurs in the committed reference log, once timing is removed.
- **Fixes.** Four portability fixes were needed (patches 01–04). None touches the mathematics.
- **New finding.** Several displayed bound decimals exceed their certified doubles; see "Displayed decimals" below.

## Method

1. **Commands.** I took the commands from the instance note (`open-instances-wave2/cops/report.md` §2–3, §5), the reviews (`reviews/cops-verification/verification-report.md` §5, `reviews/catmix-recheck.md` "Commands run"), and the primal-chain report and review (`publication/primal/chain/report.md`, `publication/reviews/primal-chain-review-r1.md`).
   - I reran only the final commands that produce a claimed number.
   - I did not rerun superseded coarser grids or the failed explorations in `explore/`.
2. **Main runs.** These ran in the worktree, one process per slot, two slots, with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1` and `PYTHONDONTWRITEBYTECODE=1`.
   - Each command ran under `/usr/bin/time -v` (wall time, CPU time, peak RSS), with `uptime` recorded at start and end.
   - Runner scripts: `scripts/run_measured.sh` and `scripts/run_queue.sh`. Queues: `scripts/queue_phase{0,1}_{A,B}.txt`. Per-run files: `logs/NAME.{log,time,meta}`.
   - An earlier agent in this role launched these queues (13:52–17:00) and was then interrupted. I checked every output.
   - Two of the runs, `a_catmix_bound_100` and `v_catmix_dp_100_cfgA`, ran under `bwrap` with the main tree replaced by an empty tmpfs.
3. **Comparison.** `scripts/build_manifest.py` compared each log with the committed reference logs. It parses all JSON objects (exact float equality after dropping keys containing "seconds") and the normalized text lines (timings, paths and assert line numbers removed). It also compared every output file with its HEAD blob.
4. **Sandboxed audit.** 46 runs, `logs/s_*`, 20:14–20:33.
   - **Tree.** I built a fresh tree, `/tmp/cops_patchcheck`: `git archive HEAD` of the 5 cops directories, plus patches 01–04 applied in order.
   - **Sandbox.** All 43 short commands, and the first 150 s of the 3 long command types, were rerun there under `bwrap`, with both `/workspace/minlp-notes` and `/workspace/minlp-notes-clean` hidden. File opens were traced with `strace -f -e trace=openat,open`.
   - **Outcome.** All 43 complete reruns produced output identical to the main runs. The 3 startup audits started normally and were stopped by `timeout` (exit 124), as intended. Their progress lines equal the main runs'.
   - **Inputs.** The traced opens are the source of each command's input list (with sha256) in the manifest. The strace files are in `logs/strace/sandbox_audit_strace.tar.gz`.
   - **Timing.** Audit timings include strace overhead and machine load 46–106, so they are not used.
5. **Displayed decimals.** `scripts/exact_display_checks.py` uses only `fractions.Fraction`. It compares each certified double, taken exactly, with its displayed decimal, and recomputes the gaps against the exact primal enclosures. Output: `logs/exact_display_checks.{json,log}`.

**Model files.** I used the cached OSIL files; sha256 values are in `manifest.json` → `osil_models`.

| file | sha256 |
|---|---|
| chain50 | f6b2b409…8f3e34 |
| chain100 | 45cb3020…ea6a64 |
| chain200 | 634acc62…3f01 |
| chain400 | 7cd93486…8bb9 |
| catmix100 | 9f5b5bae…1e61 |
| catmix200 | 9194135d…0767 |
| catmix400 | 3dfc4d7f…32a8 |
| catmix800 | 40b572a4…bc04 |

- The minlplib-status track fetched the current `https://www.minlplib.org/osil/<name>.osil` on 2026-10-02 (`publication/minlplib-status/data/part_a.json`). All 8 are sha256-identical to the cache and dated 2019-06-25.
- No MINLPLib `.sol` file or other gitignored input is read by any cops command; the strace audit confirms this.

**Software.** Python 3.13.11, mpmath 1.3.0, numpy 2.5.1, scipy 1.18.0, sympy 1.14.0, pyscipopt 6.2.1 (SCIP 10). Machine: 36 cores, shared. Load during the main runs was 5–20.

## Per-instance results

"=" means the reproduced value equals the recorded value in every displayed digit, and the underlying double or JSON object is bit-identical to the committed one. Times are wall-clock times of the main runs. Times in parentheses are the original runs' times from the notes.

| instance | certificate (authors) | independent verification | primal point and checks | match |
|---|---|---|---|---|
| chain50 | `chain_bound.py 1e-14 50`: 5.072261493982863, 11,121 boxes, 0 unresolved =; 11.6 s (13 s) | `v_chain_bnb.py`: 5.072261493982863, 36,689 boxes, min leaf 5.07226149398286276 =; 71.7 s (50 s) | KKT 5.0722614939828723164 =; exact point in Q(√R): objective ∈ [5.0722614939828723164454381769845467731843, …844] =; gap 9.58e-15 =; reviewer exact check = | yes; display caveat |
| chain100 | 5.0697846107387505, 15,329 boxes =; 15.7 s (18 s) | 5.0697846107387505, 52,955 boxes =; 100.8 s (79 s) | objective ∈ […059056713, …714] =; gap 1.01e-14 = | yes |
| chain200 | 5.068917341793162, 21,057 boxes =; 20.7 s (25 s) | 5.068917341793162, 75,385 boxes =; 143.1 s (122 s) | objective ∈ […416891, …892] =; gap 9.34e-15 = | yes; display caveat |
| chain400 | 5.068621694604009, 27,843 boxes =; 28.8 s (34 s) | 5.068621694604009, 104,945 boxes =; 194.8 s (154 s) | objective ∈ […607014, …015] =; gap 9.78e-15 = | yes |
| catmix100 | `catmix_bound.py 100 1e-5 200 1e-7 0.0685 0.0725 1e-6`: −0.048069432038882705, 161,155,292 interval evaluations =; 17.5 min (21 min) | `v_catmix_dp.py` config A −0.048069432031981114 = (13.2 min); config B −0.04806943203114456 = (46.0 min, original 39 min) | authors' primal −0.0480694320309596 =; compose check =; Newton point −0.048069432030979596104 =; bracket 1.65e-13 = | yes; display caveat (config B value) |
| catmix200 | −0.04805914560067171, 250,442,346 evaluations =; 28.8 min (32 min) | config A −0.04805914559907277 =; 20.2 min (19.5 min) | −0.0480591455801144 = | yes; display caveat (authors' value) |
| catmix400 | −0.048056547950296354, 394,390,574 evaluations =; 50.0 min (47 min) | `recheck_dp.py` final −0.04805654782467129 =; 45.2 min (43 min) | −0.0480565477566116 =; policy point −0.0480565477559440726 (exact rational) = | yes |
| catmix800 | −0.048055901841076894, 612,572,184 evaluations =; 76.7 min (70 min) | final −0.04805590147967565 =; 46.1 min (43 min) | `_snap` −0.0480559013308475 = (via patch 04); policy point −0.0480559013312308003 =; bracket ≤ 1.49e-10 | yes; display caveat (recheck value) |

**Also reproduced (all "yes"):**
- chain: model/KKT `chain_model.py 50 100`; the 4-million-case calibration float check (`min relative F 0.0`); the verifier's structure check, lemma check (200,000 cases, min gap 1.673e-31, residual 7.97e-51), adversarial check (−2.524e-29, rounding on the equality manifold) and theorem check.
- chain primal track: `build_points.py`, `verify_points.py` (its `logs/verify.log` is byte-identical to the main tree's) and `scip_crosscheck.py`.
- chain primal reviewer: `rev_chain_exact.py`, `rev_negative_controls.py`, `rev_side_checks.py`.
- catmix: `catmix_model.py 100 200` (−0.04806939756886153, which rounds to the note's −0.04806939757); `catmix_primal_snap.py 400/800`; the stage-bound self-test (margin −1.332e-15); the verifier's and rechecker's model, self-test and OSIL cross-check scripts; `policy_exact.py 400/800`.

**Totals.**
- 52 runs: 21,630 s wall, summed over runs (6.01 h), and 21,629 s CPU (all single-threaded).
- Elapsed: 3 h 08 min on 2 slots.
- By family: chain 814 s (13.6 min) and catmix 20,816 s (5.78 h).
- Largest peak RSS: 2.0 GB (`v_catmix_dp_100_cfgB`).
- Runtimes match the notes within about ±25%, which is expected on a shared machine.
- Per-run values, including load at start and end, are in `manifest.json` → `runs`.

## Displayed decimals that are not themselves proved bounds

Each bound is a binary double d, proved to satisfy optimum ≥ d. The notes display the shortest decimal that rounds to d (Python `repr`). That decimal is a valid bound only if it is ≤ d. Exact rational comparison found 5 displayed values above their doubles:

| value as displayed | where | display − double | safe display (17 significant digits, rounded down) |
|---|---|---|---|
| chain50 5.072261493982863 | COPS author note and verification report | +2.54e-16 | 5.0722614939828627 |
| chain200 5.068917341793162 | note, review | +3.32e-16 | 5.0689173417931616 |
| catmix200 authors' −0.04805914560067171 | note | +1.32e-18 | −0.048059145600671712 |
| catmix100 verifier config B −0.04806943203114456 | COPS verification report | +1.37e-18 | −0.048069432031144562 |
| catmix800 recheck −0.04805590147967565 | catmix-recheck.md | +1.46e-18 | −0.048055901479675652 |

- The primal-chain track had already flagged chain50 and chain200. The three catmix cases are new.
- The other displayed values (chain100, chain400, authors' catmix100/400/800, verifier catmix200, recheck catmix400) are valid as displayed.
- The summary's own range displays (5.06862 … 5.07226; −0.04806944 … −0.04805591) are valid.
- The gaps are unaffected at their stated precision: 9.58e-15, 1.01e-14, 9.34e-15, 9.78e-15, 1.65e-13 all reproduce. The catmix800 policy bracket needs the outward display 1.49e-10; 1.48e-10 understates it.
- Against the displayed chain400 value, the gap is 1.0014e-14 rather than "≤ 1.0e-14". The latter holds against the certified double.
- For the paper, use rounded-down displays.

## Failures in the clean checkout and fixes

1. **Reviewer scripts read the main tree (patch 01).**
   - Affected: 8 scripts in `reviews/cops-verification/` and `reviews/catmix-recheck-checks/`, which open the authors' outputs by the absolute path `/workspace/minlp-notes/research-20260929/...`.
   - Elsewhere this fails with FileNotFoundError. On this machine it silently reads the main tree instead of the checkout under test.
   - Fix: paths relative to `__file__`.
2. **User-specific OSIL path (patch 02).**
   - Affected: 6 scripts with the literal `/workspace/local-home/.cache/minlplib/minlplib/osil/...`.
   - Fix: `os.path.expanduser("~/.cache/minlplib/minlplib/osil")`. On this machine it is the same file.
   - Apply after patch 01 (overlapping hunks).
3. **Primal-chain scripts read and write the main tree (patch 03).**
   - Affected: `build_points.py`, `verify_points.py`, `scip_crosscheck.py` and the reviewer's `rev_chain_exact.py`.
   - These use absolute main-tree paths for reading *and writing* (`points/`, `logs/verify.log`). Run unpatched from a clean checkout on this machine, they would overwrite the main tree's point files.
   - Fix: script-relative paths.
4. **Missing script (patch 04).**
   - `logs/catmix800_primal_snap.{json,txt}`, the catmix800 primal −0.0480559013308475 in the note, came from an unsaved inline snippet.
   - Fix: `explore/catmix_primal_snap_eval.py`, recovered from the wave-2 transcript. It rewrites both files byte-identically.

**Patch status.**
- Each patch file starts with an explanation header.
- Checked: all four apply cleanly, in order, as separate `git apply` calls, to a HEAD copy of the 5 directories.
- Checked: patches 01, 03 and 04 pass `git apply --check` against the main tree.
- Patch 02 must be applied after 01. The main tree's files in these directories are identical to c3514f03 (only `publication/primal/chain/report.md` was added), so the sequence applies there too.

**Undocumented or fragile steps (documented here, not patched):**
- `verify_points.py` *appends* to `logs/verify.log`. Delete that file first to get a file equal to the committed one.
- `v_catmix_dp.py` and `recheck_dp.py` read `logs/catmixN_theta_traj.npy`, which `v_catmix_selftest.py N` writes, so run the self-test first. The trajectories are also committed, and the regenerated ones are byte-identical.
- `catmix_bound.py` reads `logs/catmixN_u.npy`, written by `catmix_primal.py`. These are committed and regenerated byte-identically.
- `build_points.py` stores the absolute source path in the `source_point` field. It is never read, but it makes the generator file depend on the checkout location.
- Not reproducible: the primal-chain author's one-off negative control (`logs/negative_control.log`), because its code was not saved. The reviewer's saved `rev_negative_controls.py` covers the same perturbations and was reproduced.
- The reviewer's one-off `rev_gap_vs_display.log` (9.62e-15, 1.01e-14, 9.41e-15, 1.01e-14) is reproduced exactly by `scripts/exact_display_checks.py`.
- The committed `reviews/cops-verification/logs/chain_lemma.log` ends with a traceback from the reviewer's first adversarial test. The review documents this. The current script runs the fixed test and prints the value of `chain_lemma_adv.log`.
- Correction to the task description: `publication/primal/chain/` and `publication/reviews/primal-chain-r1/` are tracked at c3514f03, and their scripts are identical to the main tree's. The committed points and logs were moved aside (`_main_tree_copy/`) so that the runs regenerated them.

**Other findings.**
- Nondeterminism: none found. All `.npy`, `.txt` and point files are bit-identical, and all JSON results are equal float for float.
- Runner bug in this track's own scripts: the "exit=" values in the `logs/queue_*.out` files always read 0, because `$(date)` reset `$?`. The `.meta` files record the real exit codes and are the ones used. Both runner scripts are now fixed.

## How to reproduce (from a clean checkout; R = research-20260929)

0. **Setup.**
   - Download the 8 OSIL files to `~/.cache/minlplib/minlplib/osil/`: `curl -O https://www.minlplib.org/osil/{chain50,chain100,chain200,chain400,catmix100,catmix200,catmix400,catmix800}.osil`, one at a time with a 1 s delay. Check the sha256 values above.
   - From the repository root, apply the patches in order: `git apply patches/01-…`, then `02-…`, `03-…`, `04-…`.
   - `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`.
1. **Authors' certificates and primal points** (`cd R/open-instances-wave2/cops`):
   - `python3 chain_model.py 50 100`
   - `python3 chain_bound.py 1e-14 N` for N = 50, 100, 200, 400 (12–29 s each)
   - `(cd explore && python3 calibration_random_check.py)`
   - `python3 catmix_model.py 100 200`
   - `python3 catmix_primal.py N` for N = 100, 200, 400, 800 (9–68 s)
   - `cd explore && python3 catmix_primal_snap.py 400 2e-3 && python3 catmix_primal_snap.py 800 2e-3 && python3 catmix_primal_snap_eval.py 800 && python3 catmix_stage_lb_selftest.py && cd ..`
   - `python3 catmix_bound.py N 1e-5 200 1e-7 0.0685 0.0725 1e-6` for N = 100, 200, 400, 800 (18, 29, 50 and 77 min)
2. **Independent verification of chain50–400 and catmix100/200** (`cd R/reviews/cops-verification`):
   - `python3 v_chain_checks.py struct`, `… lemma 200000` (67 s), `… lemma 0 adv`, `… theorem`
   - `python3 v_chain_bnb.py 1e-14 N` for N = 50, 100, 200, 400 (72–195 s)
   - `python3 v_catmix_model.py 100 200 400 800`
   - `python3 v_catmix_selftest.py 100`, `python3 v_catmix_selftest.py 200`
   - `python3 v_catmix_primal.py 100`, `python3 v_catmix_newton.py 100`
   - `python3 v_catmix_dp.py 100 15 0.0695 0.0717 19 200 24` (13 min)
   - `python3 v_catmix_dp.py 100 16 0.0697 0.0715 20 300 25` (46 min, 2 GB)
   - `python3 v_catmix_dp.py 200 15 0.0695 0.0717 19 200 24` (20 min)
3. **Independent recheck of catmix400/800** (`cd R/reviews/catmix-recheck-checks`):
   - `python3 osil_crosscheck.py 400 800`, `python3 v_catmix_model.py 400 800`, `python3 v_catmix_selftest.py 400`, `python3 v_catmix_selftest.py 800`
   - `python3 recheck_dp.py 400 13 --sband 0.0703 0.0710 21 40 310 --sband 0.0695 0.0717 19 40 310 --win 200 24 logs/catmix400_theta_traj.npy --win-skip 56 288 --tree logs/tree400_final.json --save-traj logs/catmix400_final_policy_traj.npy --save-u logs/catmix400_final_policy_u.npy` (45 min)
   - `python3 policy_exact.py 400 logs/catmix400_final_policy_u.npy`
   - `python3 recheck_dp.py 800 13 --sband 0.0703 0.0710 21 95 600 --sband 0.0695 0.0717 19 95 600 --sband 0.060 0.0695 17 570 650 --win 200 24 logs/catmix800_theta_traj.npy --win-skip 112 576 --tree logs/tree800_final.json --save-traj logs/catmix800_final_policy_traj.npy --save-u logs/catmix800_final_policy_u.npy` (46 min)
   - `python3 policy_exact.py 800 logs/catmix800_final_policy_u.npy`
4. **Exact chain points** (`cd R/publication/primal/chain`):
   - `rm -f logs/verify.log`
   - `python3 build_points.py N` for N = 50, 100, 200, 400
   - `python3 verify_points.py 50 100 200 400`
   - `python3 scip_crosscheck.py 50 100 200 400`
5. **Chain-point reviewer** (`cd R/publication/reviews/primal-chain-r1`):
   - `python3 rev_chain_exact.py 50 100 200 400`
   - `python3 rev_negative_controls.py`
   - `python3 rev_side_checks.py 50 100 200 400`
6. **Optional:** `python3 publication/reproduction/cops/scripts/exact_display_checks.py`, for the exact display and gap checks. It reads the outputs from the worktree path that is hard-coded in the script.

Steps 2–5 depend on step 1's outputs only through committed files, which step 1 regenerates identically. Step 2 needs its self-tests to run before `v_catmix_dp.py`, and step 3 needs its self-tests before `recheck_dp.py`. The total is about 6 h single-threaded, or about 3.1 h on 2 processes.

## Caveats

- **Inputs of the long runs.** For `catmix_bound.py`, `v_catmix_dp.py` and `recheck_dp.py`, the input lists come from 150 s startup traces, with N substituted for the other sizes. These scripts read their inputs at startup, and the patched code contains no reference to `/workspace/minlp-notes` (checked by grep).
- **Hidden main tree.** Two of the long main runs ran fully with the main tree hidden. The others ran in the worktree with patches 01, 03 and 04 applied (patch 02 does not change which file is read on this machine).
- **Timing.** Timings come from a shared machine and are indicative only.
- **Scope.** Superseded exploratory runs (coarser grids, `explore/` failures, the recheck grid-design runs) were not rerun.
- **What "verified" means here.** It refers to the reviewers' independent code, which was rerun. This track wrote no new mathematics.