<!-- Written to disk by the root from the structured return value of agent 'author:eg-recheck' (workflow wf_a89a60b6-d10). -->

# eg_disc2_s: independent re-certification of every leaf of run G

Date: 2026-10-02. Track: eg-recheck. Folder:
`/workspace/minlp-notes/research-20260929/publication/eg-recheck/`.

This track was done in two passes. The first pass was interrupted by a usage limit before it could report. It replayed and recorded the run G trees and certified every leaf in 38 chunks. This second pass did four things:

- checked those results and the code path;
- ran the summary over all parts, which had never been run in full;
- ran the negative control, which had never been run;
- added a second, tree-free coverage check.

I then wrote this report. Only targeted checks were run. No project-wide verification was run and no CI was consulted. No git commit was made.

## 1. Result

The claimed dual bound **5.642100574331458** for eg_disc2_s is **verified on every leaf of all eight parts of run G under assumptions A1 and A2** by the earlier review's independent certifier. Review r1 also certified 10,404 leaves of parts 0 and 2–7, including the 300 tightest per part, with outward-rounded interval arithmetic and no libm assumption; that stronger check is a sample only.

- **Certification.** All **1,114,361** leaves were certified against θ* = 5.642100574331458 by the reviewer's independent certifier (`reviews/eg-retry-review-checks/indep_cert.py`). This is 979,044 leaves in parts 0 and 2–7 plus 135,317 in part 1. There were **0 failures**. 98,234 leaves have no feasible point with F < θ*: 85,685 were proved infeasible by a side row at the leaf itself, 373 were closed by a Farkas test excluding F < θ*, and 12,176 were closed after splitting (their pieces can include Farkas certificates).
- **Coverage within each part.** The leaves of each part cover that part:
  - The reviewer's tree-bookkeeping check passed on all 8 parts. Review r1 also supplied an exact tree-free guillotine proof (`../reviews/eg-recheck-r1/own_cover.py`, `../reviews/eg-recheck-r1/logs/own_cover.log`).
  - A new check that does not use the tree passed on all 8 parts: an exact volume identity plus 1,000,000 random points per part.
- **Coverage across parts.** The 8 parts cover the domain of the MINLPLib instance. The variable bounds were read from the OSIL file and compared with exact rationals.
- **Rigor.** The result is rigorous under the two stated floating-point assumptions of the certifier (Section 4). These are the same assumptions under which the review certified part 1. The sampling caveat in the review and in `open-instances-summary.md` ("other parts by a sample of 110,676 of 979,044 leaves") can now be removed.

**Correction to the counts in the task text.** Run G has **1,152,830 processed boxes**, not 1,152,830 leaves. The leaves are the closed processed boxes plus the slabs removed by domain reduction: **1,114,361**. Run G has no pre-closed, open or tiny boxes. In every part, processed = 1 + 2 × (number of split boxes).

## 2. Per-part results

The margin of a leaf is its certified lower bound minus θ*:

- for a row certificate, max_k (c_k + lower bound of row k) − θ*;
- for an LP certificate, the weak-duality value − θ*;
- +∞ for a leaf with no feasible point having F < θ* (side infeasibility, Farkas, or certification after splitting);
- for a leaf the certifier had to split, the minimum over the pieces.

Margins are computed exactly and printed as floats. The data are in `logs/summarize.log`.

| part | i7 range | processed boxes | leaves (closed + slabs) | certified | failures | no feasible F < θ* (+∞ margin) | smallest margin (leaf kind, certificate) | smallest LP margin | review (sample size; smallest LP margin) | CPU s |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | [20, 23] | 119,873 | 117,177 (59,937 + 57,240) | 117,177 | 0 | 4,946 | 2.566e-5 (slab, row) | 4.506e-5 | 13,699; 2.4e-4 | 4,145 |
| 1 | [24, 27] | 134,607 | 135,317 (67,304 + 68,013) | 135,317 | 0 | 8,626 | 1.011e-9 (closed box, LP) | 1.011e-9 | all; 1.0e-9 | 5,239 |
| 2 | [28, 31] | 178,085 | 178,707 (89,043 + 89,664) | 178,707 | 0 | 17,734 | 4.592e-5 (closed box, row) | 3.777e-4 | 19,696; 6.6e-4 | 7,383 |
| 3 | [32, 35] | 223,449 | 221,118 (111,725 + 109,393) | 221,118 | 0 | 23,794 | 1.707e-5 (slab, LP) | 1.707e-5 | 23,916; 3.5e-4 | 8,396 |
| 4 | [36, 39] | 222,097 | 210,365 (111,049 + 99,316) | 210,365 | 0 | 20,705 | 2.829e-6 (slab, row) | 1.712e-4 | 22,925; 6.7e-4 | 7,284 |
| 5 | [40, 43] | 155,279 | 145,223 (77,640 + 67,583) | 145,223 | 0 | 13,281 | 1.401e-7 (closed box, row) | 5.989e-5 | 16,281; 9.9e-4 | 6,352 |
| 6 | [44, 47] | 82,919 | 77,361 (41,460 + 35,901) | 77,361 | 0 | 6,885 | 4.150e-5 (closed box, row) | 9.899e-4 | 9,509; 1.1e-3 | 1,740 |
| 7 | [48, 50] | 36,521 | 29,093 (18,261 + 10,832) | 29,093 | 0 | 2,263 | 1.061e-4 (closed box, row) | 2.169e-3 | 4,650; 1.0e-2 | 623 |
| **total** | [20, 50] | **1,152,830** | **1,114,361** | **1,114,361** | **0** | 98,234 | 1.011e-9 (part 1); 1.401e-7 over parts 0 and 2–7 | | 245,993 | 41,162 |

The leaf counts per part match the review's table exactly (review Section 5).

Which certificate closed each leaf, counted at the leaf itself:

| part | row | side-row infeasible | LP | Farkas | certified after splitting |
|---|---|---|---|---|---|
| 0 | 76,296 | 4,003 | 4,565 | 1 | 32,312 |
| 1 | 85,734 | 7,117 | 3,486 | 4 | 38,976 |
| 2 | 108,566 | 15,248 | 5,301 | 93 | 49,499 |
| 3 | 131,290 | 20,779 | 5,010 | 221 | 63,818 |
| 4 | 123,371 | 18,590 | 2,266 | 42 | 66,096 |
| 5 | 89,194 | 11,923 | 774 | 7 | 43,325 |
| 6 | 47,334 | 5,906 | 355 | 5 | 23,761 |
| 7 | 17,197 | 2,119 | 180 | 0 | 9,597 |

"Certified after splitting" means the certifier bisected the leaf, up to depth 24, and certified every piece.

**Consistency with the review.**

- In every part, the smallest LP margin over all leaves is at most the review's smallest LP margin over its sample, as it must be. Part 1 is identical (1.011e-9).
- The reviewer's `verify_tree.py`, run unchanged with sample fraction 0, certifies only the 2,000 tightest closures per part. On parts 0–5 it reproduces the review's smallest LP margins: 2.3998e-4, 1.011e-9, 6.598e-4, 3.491e-4, 6.665e-4 and 9.861e-4.
- On parts 6 and 7 the review's minimum came from its 10% random sample, which this run did not include. These runs give 0.0316 and 0.0571 instead.

**The tightest-margin leaves outside part 1 have loose bounds.** The smallest margin outside part 1 is 1.4e-7, at part 5 leaf 69407. Leaf numbers here and in `tight_leaves.log` and `inspect_leaf_p5_69407.log` are positions in the concatenation of chunk files, not positions in `verify_tree.py`'s leaf list; this same box is leaf 56587 in that list. There, the certifier's affine lower bound for row e11 lands just above θ*. However:

- the float minimum of F over that box is θ* + 2.02;
- the author's own bound for the box had a margin of 0.48 (`logs/inspect_leaf_p5_69407.log`);
- for the 10 smallest-margin leaves in each of parts 0 and 2–7, the float minimum of F exceeds the certified bound by at least 0.22 (`logs/tight_leaves.log`).

This observation concerns those selected leaves only. Independent r1 floating-point searches found a feasible point in part 0 at F − θ* ≈ 0.0066, near x = (0.3238, 1.0, 0.7863, 1.2655, 11, 35, 23). The smallest values found in parts 0, 2, 3, 4, 5, 6 and 7 were 0.0066, 0.30, 0.29, 0.51, 0.99, 1.77 and 2.77 (`../reviews/eg-recheck-r1/logs/local_min.log`). These are numerical evidence, not certified regional minima.

**Threshold.** θ* was passed as the string "5.642100574331458" and converted with `Fraction`, so the test is against that exact decimal. All 38 chunk logs say so. The binary float with the same literal is 6.3e-17 larger than the decimal. Every finite margin is at least 1.0e-9, so the float value is certified too.

## 3. Method

1. **Replay and recording of run G.**
   - `run_record.sh` ran the reviewer's `record_run.py` unchanged on all 8 parts: `eg_disc2_s 1e-9 25000 <out> k 8`. That script is the author's `egbb.BB.run` with recording lines added.
   - It recorded every processed box: the box, the reduced box, the kept flag, the split coordinate and the bound.
   - `compare_logs.py` compared every progress line and the final `B&B:` and certified-bound lines with the original `open-instances-wave3/eg/retry/logs/disc2_9_p*.log`. All 8 parts are identical apart from timings (`logs/compare_logs.log`: "ALL IDENTICAL"). So the recorded trees are the run G trees.
2. **Certification of every leaf.**
   - `recheck_leaves.py` is a copy of the reviewer's `verify_tree.py`. It differs only in three ways: it takes every leaf instead of a sample, split into interleaved chunks (leaf index ≡ chunk mod nchunks); it records margins; and it saves per-leaf results. The diff is in `logs/diff_verify_tree.txt`.
   - `margin_cert.py` subclasses the reviewer's `Certifier`. Its copied methods differ from the originals only in lines marked `# MARGIN`, which record the certificate type and margin. `check_copy.py` prints the diff and asserts that no unmarked line changed (`logs/check_copy.log`, rc 0). The certification decisions are unchanged.
   - 38 chunks were run: parts 0–7 in 4, 5, 6, 7, 7, 5, 3 and 1 chunks, written to `res/p<k>_c<c>.npz` and `logs/cert_p<k>_c<c>.log`.
   - The scheduler `run_cert.py` also ran the unchanged `verify_tree.py` on every part (`logs/verify_tree_p*.log`).
3. **Summary.** `summarize.py` checks the following and prints per-part counts, certificate types and margins (`logs/summarize.log`):
   - in each part, the chunk index sets together are exactly {0, …, n−1}, with no index missing or repeated;
   - every chunk's coverage flag is true;
   - there are no failures and no open or tiny boxes;
   - the 8 root boxes cover the OSIL domain.
4. **Second coverage check, new in this pass.** `coverage_check.py` (Section 5).
5. **Controls.** `negative_control.py`, `coverage_check.py … drop`, `tight_leaves.py`, `check_exp.py` and `check_independence.py` (Section 6).

## 4. Independence and assumptions

**What the certification path runs.** `check_independence.py` certified 128 leaves through the same path as `recheck_leaves.py`, then listed every module loaded from the repository: `indep_cert`, `gms_model`, `margin_cert`, and the script itself. It asserts that none of the author's modules is loaded (`egbb`, `egfast`, `egtm`, `egdata`, `eg_model`, `kan_iv`, `ia`, `osilx`, `ev`, `eg_bb`, `eg_bb2`, `eg_run`). A static import scan of `margin_cert.py`, `recheck_leaves.py`, `indep_cert.py`, `gms_model.py` and `verify_tree.py` finds none of them either (`logs/check_independence.log`).

**Who wrote the code.** The review wrote `indep_cert.py` and `gms_model.py` separately from the author's code (review Section 5). The md5 sums of `indep_cert.py`, `gms_model.py`, `verify_tree.py`, `record_run.py` and `data/eg_disc2_s.gms` were recorded before the first pass started. They are unchanged now, and the files are dated 2026-09-30, the review's date.

**What is shared with the author.**
- The tree shapes. This is by design. The tree is only a proposed partition: its coverage is checked, and each leaf is certified on its own, so the author's code does not need to be correct.
- The instance itself. `gms_model.py` reads the MINLPLib GAMS file. The review checked this reading exactly against the author's OSIL decoding (`check_decode.py`). Here, `summarize.py` also reads the variable bounds from the OSIL file with `xml.etree`.
- Not shared: the LP multipliers. The certifier gets its own from scipy's HiGHS and uses them only as proposals.

**Rigor.**
- Every final certificate test is exact rational arithmetic (`fractions.Fraction`): the row bound, side-row infeasibility, LP weak duality and the Farkas test.
- The data fed to these tests are float64 enclosures with a-posteriori error padding: the natural enclosure and the order-2/3 Taylor-model affine bounds. They are **not** outward-rounded interval arithmetic. Their soundness rests on two assumptions:
  - **A1.** The padding constants in `indep_cert.py` dominate the float rounding errors. The review derived and checked this error analysis by hand (Sections 4–5); it is not machine-checked.
  - **A2.** numpy's `exp` has relative error at most 1e-14. This is supported by sampling only. `check_exp.py` (numpy 2.5.1 with AVX512 dispatch) found a maximum relative error of 1.315e-16 (1.18 ulp) over 1,506,237 arguments. These covered uniform [−700, 0], uniform [0, 20], small |x|, and neighbours of k·ln2/2 (`logs/check_exp.log`). The review sampled 25,000 more.
- Under A1 and A2, the certification of every leaf is a proof. The smallest margin is 1.0e-9 absolute, about 1.8e-10 relative to θ*. This is several orders of magnitude above the float error scale of the enclosures (padding of about 1e-12 relative). Small errors in the padding constants would therefore not change any decision. This is a robustness remark, not part of the proof.
- Relaxing the integer coordinates to intervals inside a leaf is sound.

## 5. Coverage

1. **Tree bookkeeping, proof (reviewer's logic).** I reread the logic in `verify_tree.py`. It ran inside every one of the 38 chunk runs (`cov_ok` and `nbad_red` are saved in every result file) and once per part as the unchanged script. It checks that:
   - the root box contains the part's domain;
   - every reduced box lies in its box and has integral integer ends;
   - children recomputed from the reduced box and split coordinate are a valid split: integer [a, m] and [m+1, b]; continuous, a bisection with a shared face;
   - the multiset of generated boxes equals the multiset of popped boxes.

   Result on every part: equal (119,873 / 134,607 / 178,085 / 223,449 / 222,097 / 155,279 / 82,919 / 36,521 boxes), 0 bad reduced boxes, and 0 open, tiny or pre-closed boxes. By induction over the tree, the closed boxes, taken whole, together with the domain-reduction slabs cover the root box. Integer slabs start at the next integer.
2. **Tree-free cross-check, new in this pass (`coverage_check.py`, `logs/coverage_check.log`).** It uses only the saved leaf lists and root boxes. In all 8 parts:
   - every leaf lies in the root box, has lo ≤ hi, and has integral integer bounds;
   - **Exact volume identity.** Measure = ∏ continuous widths × ∏ (number of integer points). All coordinates are at least 0.25, so they are exact multiples of 2^−54, which is asserted. Volumes are therefore computed in exact Python integers. The leaf volumes sum exactly to the root volume.
   - Each of **1,000,000 random points** per part (continuous uniform, integers uniform) lies in **exactly one** leaf: 0 points uncovered and 0 in two leaves.

   If the leaf interiors are disjoint, the volume identity implies coverage. Disjointness follows from the tree check and is supported by the random-point test. So this is an independent cross-check; the original proof is item 1. Review r1 subsequently supplied an exact tree-free guillotine coverage proof (`../reviews/eg-recheck-r1/own_cover.py`, `../reviews/eg-recheck-r1/logs/own_cover.log`; review Section 1.3). It checks disjointness and coverage by recursively partitioning the boxes, without using the recorded tree.

   Negative control: with the largest leaf of each part removed (`logs/coverage_check_drop.log`), the volume identity fails in all 8 parts, and 7–16 of 20,000 random points per part are uncovered.
3. **The parts cover the instance's domain** (`summarize.py`, OSIL file read with `xml.etree`, exact `Fraction` comparisons):
   - The OSIL bounds are x1 ∈ [.3, .6], x2 ∈ [.4, 1], x3 ∈ [.4, 1], x4 ∈ [.7, 1.5], i5 ∈ [10, 20], i6 ∈ [30, 40] and i7 ∈ [20, 50].
   - In every part, the root box contains the exact continuous bounds, and i5 and i6 span their full ranges.
   - The i7 ranges [20,23], [24,27], [28,31], [32,35], [36,39], [40,43], [44,47] and [48,50] are integral, disjoint and consecutive, and span [20, 50].
4. **Chunk bookkeeping.**
   - In every part, the union of the chunk index sets is exactly {0, …, n−1}, with no index missing or repeated.
   - All 38 chunk logs report "theta* = 5.642100574331458" and 0 failures, totalling 1,114,361 / 1,114,361.
   - `git status` shows no changes to the committed `rec/` and `res/` files since the first pass.

## 6. Controls and evidence checks

- **Negative control** (`negative_control.py`, never run in the first pass; run now: `logs/negative_control.log`, "CONTROLS PASSED"). The primal point x* is exactly feasible with F(x*) = 5.6421005799711068.
  - Boxes of relative size 1e-2 to 1e-8 around x* (integers fixed): with θ = F(x*) + 1e-6 and θ = F(x*) + 1e-9, all 8 boxes are refused.
  - Positive control: with θ = θ* − 1e-6 the result is [False, True, True, True], the same as the review. The largest box exceeds the depth limit of 12 used in the control.
  - End to end: exactly one leaf of part 1 contains x*. It was certified for θ* in the full run and is refused at θ = F(x*) + 1e-9.
- **Float minimization of the tightest leaves** (`tight_leaves.py 10`, `logs/tight_leaves.log`; evidence, not proof). For the 10 leaves with the smallest margins in each part (80 in total), SLSQP was run from 24 starts each, with and without the side rows. No float minimum fell below a certified bound. The smallest gap was 3.67e-9, in part 1 next to the optimum. In parts 0 and 2–7 the smallest gaps were 0.22–2.86.
- **exp assumption A2**: see Section 4.
- **Comparison with the author's bounds** on closed boxes (`logs/summarize.log`). The independent margin is at least the author's on 28–37% of closed boxes. Where it is smaller, the median ratio is 0.71–0.93. No closure depends on the author's code.

## 7. Runtime

- **Recordings** (author's B&B replayed with recording, 8 processes at once): 334–3,442 s per part, 14,540 s in total.
- **Certification**: 38 chunks, 41,162 s CPU in total (21–44 ms per leaf). The scheduler's wall time was 5,372 s, with at most 12 processes of this track (the first pass's budget).
- **Total wall time** of the first pass: about 1 h 34 min (2026-10-01 22:54 to 2026-10-02 00:28).
- The machine was shared and the load average reached about 240, so all times are inflated.
- In this pass, each of `summarize.py`, `negative_control.py`, `tight_leaves.py` and `coverage_check.py` finished within about 10 minutes, with at most 3 processes running at once.

## 8. Files

All paths are relative to this folder.

- **Scripts.**
  - `run_record.sh`, `run_cert.py`: replay and scheduling.
  - `recheck_leaves.py`, `margin_cert.py`: certification, as copies of the reviewer's code with recording added.
  - `summarize.py`, `coverage_check.py` (new): summary and coverage.
  - `compare_logs.py`, `check_copy.py`, `check_independence.py`, `check_exp.py`, `negative_control.py`, `tight_leaves.py`, `inspect_leaf.py`: checks and controls.
- **Data.**
  - `rec/rec_disc2_p0..7.npz`: recorded trees, 43 MB.
  - `res/p<k>_c<c>.npz`: per-leaf results, including boxes, certificate type, margin and the author's bound; 38 files, 37 MB.
- **Logs** (`logs/`).
  - `rec_disc2_p*.log`, `compare_logs.log`
  - `cert_p*_c*.log`, `verify_tree_p*.log`, `run_cert.out`, `run_record.out`
  - `summarize.log`, `coverage_check.log`, `coverage_check_drop.log`
  - `negative_control.log`, `tight_leaves.log`, `check_copy.log`, `check_independence.log`, `check_exp.log`
  - `diff_verify_tree.txt`, `inspect_leaf_p5_69407.log`
- **Git.** The first pass's scripts, `rec/`, `res/` and logs are already committed (c3514f03). The second-pass files are committed in 514a788f; this report and the current minor-fix files are working-tree changes. This revision made no commit.

## 9. Commands run

All Python runs used `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`, from this folder.

**First pass** (from its transcript; outputs checked in this pass):

| command | outcome |
|---|---|
| `setsid nohup ./run_record.sh` (PID 83844): 8 × `timeout 30000 python3 ../../reviews/eg-retry-review-checks/record_run.py eg_disc2_s 1e-9 25000 rec/rec_disc2_p<k>.npz <k> 8` | all 8 recorded; processed counts as in Section 2 |
| `python3 compare_logs.py > logs/compare_logs.log` | ALL IDENTICAL apart from timings |
| `setsid nohup python3 run_cert.py` (PID 92787): 8 × `timeout 7200 python3 ../../reviews/eg-retry-review-checks/verify_tree.py rec/rec_disc2_p<k>.npz eg_disc2_s 5.642100574331458 0.0 0` and 38 × `timeout 14400 python3 recheck_leaves.py rec/rec_disc2_p<k>.npz eg_disc2_s 5.642100574331458 <c> <nchunks> res/p<k>_c<c>.npz` | all rc 0; finished after 5,372 s; 0 failures in every chunk |
| `python3 check_copy.py > logs/check_copy.log` | rc 0; only `# MARGIN` lines differ |
| `python3 check_exp.py > logs/check_exp.log` | max relative error 1.315e-16 over 1,506,237 arguments |
| `python3 check_independence.py > logs/check_independence.log` | rc 0; no author modules loaded |
| `python3 inspect_leaf.py 5 69407 > logs/inspect_leaf_p5_69407.log` | margin 1.4e-7 reproduced; row e11 |
| `diff` of `verify_tree.py` and `recheck_leaves.py` → `logs/diff_verify_tree.txt` | only the stated changes |
| `tight_leaves.py` and `summarize.py` on partial results (output not saved) | superseded by the runs below |

**This pass:**

| command | outcome |
|---|---|
| `pgrep -af "record_run\|recheck_leaves\|run_cert\|verify_tree\|..."` | no stray processes from the first pass |
| `md5sum indep_cert.py gms_model.py verify_tree.py record_run.py data/eg_disc2_s.gms` (in `reviews/eg-retry-review-checks/`) | identical to the sums recorded before the first pass |
| `python3 -c` Fraction comparison of 5.642100574331458 as a float and as a decimal | float − decimal = 6.27e-17 |
| `setsid nohup timeout 3000 python3 summarize.py > logs/summarize.log` | RESULT: every leaf of every part certified; the parts cover the domain |
| `setsid nohup timeout 5400 python3 negative_control.py > logs/negative_control.log` | CONTROLS PASSED |
| `setsid nohup timeout 5400 python3 tight_leaves.py 10 > logs/tight_leaves.log` | no contradiction; smallest gap 3.67e-9 |
| `timeout 580 python3 coverage_check.py 2000` (smoke test, not saved) | passed |
| `setsid nohup timeout 5400 python3 coverage_check.py 1000000 > logs/coverage_check.log` | ALL COVERAGE CROSS-CHECKS PASSED |
| `setsid nohup timeout 3000 python3 coverage_check.py 20000 drop > logs/coverage_check_drop.log` | fails in all 8 parts, as intended |
| `grep` over the 38 `logs/cert_p*_c*.log` (threshold, failures, totals, smallest LP margin per part) | 38/38 at θ* = 5.642100574331458; 0 failures; 1,114,361 / 1,114,361 |
| `grep` over `logs/verify_tree_p*.log` | coverage True on all 8 parts; 2000/2000 certified per part |
| `pgrep` at the end | no processes of this track left running |

## 10. Caveats and suggested integration

- The proof rests on A1 (a hand-checked float error analysis) and A2 (a sampled exp accuracy). This is the same standing as the review's independent certificates for eg_int_s, eg_disc_s and part 1 of eg_disc2_s.
- Suggested wording for the integration step (I did not edit these files):
  - In `open-instances-summary.md`, change the eg_disc2_s status from "verified (part with the optimum fully; other parts by a sample of 110,676 of 979,044 leaves)" to "verified (all 1,114,361 leaves of all 8 parts of run G re-certified with the earlier review's independent certifier, rigorous under A1 and A2; coverage proved exactly, including the r1 tree-free proof; 10,404 leaves in parts 0 and 2–7 also certified with outward-rounded interval arithmetic and no libm assumption; publication/eg-recheck/report.md; publication/reviews/eg-recheck-review-r1.md)".
  - Make the matching change to the header of `open-instances-wave3/eg/retry.md`.
- Where the counts are quoted, use "1,152,830 processed boxes, 1,114,361 leaves".


## Commands run (from the agent's structured return)

- `pgrep -af "record_run|recheck_leaves|run_cert|verify_tree|run_record|negative_control|tight_leaves" -> no stray processes`
- `md5sum indep_cert.py gms_model.py verify_tree.py record_run.py data/eg_disc2_s.gms (reviews/eg-retry-review-checks) -> unchanged from the sums recorded before the first pass`
- `python3 -c Fraction comparison of 5.642100574331458 as float and decimal -> float exceeds decimal by 6.27e-17`
- `setsid nohup timeout 3000 python3 summarize.py > logs/summarize.log -> all parts certified, domain covered`
- `setsid nohup timeout 5400 python3 negative_control.py > logs/negative_control.log -> CONTROLS PASSED`
- `setsid nohup timeout 5400 python3 tight_leaves.py 10 > logs/tight_leaves.log -> no contradiction, smallest gap 3.67e-9`
- `timeout 580 python3 coverage_check.py 2000 (smoke test) -> passed`
- `setsid nohup timeout 5400 python3 coverage_check.py 1000000 > logs/coverage_check.log -> ALL COVERAGE CROSS-CHECKS PASSED`
- `setsid nohup timeout 3000 python3 coverage_check.py 20000 drop > logs/coverage_check_drop.log -> fails in all 8 parts as intended`
- `grep over logs/cert_p*_c*.log -> 38/38 at theta*=5.642100574331458, 0 failures, 1,114,361/1,114,361; per-part smallest LP margins`
- `grep over logs/verify_tree_p*.log -> coverage True on all parts`
- `First pass (from transcript, outputs checked): run_record.sh (8 x record_run.py), compare_logs.py, run_cert.py (8 x verify_tree.py, 38 x recheck_leaves.py), check_copy.py, check_exp.py, check_independence.py, inspect_leaf.py 5 69407`

## Response to review

Review: `../reviews/eg-recheck-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. A1/A2 absent from headline and integration | Added A1/A2 at the first result claim and in proposed summary wording; distinguished the assumption-free 10,404-leaf r1 sample. |
| 2. Infeasibility overclaim | Recounted saved results: 98,234 exclude F < θ*, of which 85,685 are directly side-infeasible, 373 Farkas and 12,176 split. Corrected text, margin definition and table heading. |
| 3. Leaf numbering | Stated chunk-concatenation numbering and the equivalent part-5 leaf-list index 56587; inspected the review's box comparison. |
| 4. Stale Git bullet | Verified 514a788f contains second-pass files and updated the historical status. |
| 5. Near-optimal regions outside part 1 | Qualified the statement to the selected tightest-margin leaves and added r1's numerical per-part minima. |
| 6. Tree-free coverage proof | Added the independent exact guillotine proof and its code/log locations. The original volume/random-point check remains labelled a cross-check. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/eg-recheck/minor_review_check.py > research-20260929/publication/eg-recheck/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.

### Round 2: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r1.md](../reviews/minor-fixes-review-r1.md). Issue numbers below refer to that review.

| issue | resolution |
|---|---|
| 5 | Corrected integration to eg_disc2_s and 1,152,830 processed boxes; independently recounted the saved results. |
| 22 | Added the exact tree-free coverage proof to the headline coverage bullet. |

Own exact checks and saved-source evidence: [check_r2.log](../reviews/minor-fixes/check_r2.log). The full response is [response-r2.md](../reviews/minor-fixes/response-r2.md); exact commands and results are in [commands.md](../reviews/minor-fixes/commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.
