<!-- Written to disk by the root from the structured return value of verifier round 1 of track eg-recheck in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review r1: eg-recheck (eg_disc2_s, re-certification of every leaf of run G)

Date: 2026-10-02. Independent verifier, review round 1. I did not write the track's code or the earlier review's certifier.

- Track folder: `research-20260929/publication/eg-recheck/` (report `report.md`).
- My code, data and logs: `research-20260929/publication/reviews/eg-recheck-r1/`.
- Only targeted checks were run, with at most 2 of my processes at once. No project-wide verification was run and no CI was consulted. No git commit was made. Nothing outside my folder was changed.

The earlier verifier in this role was cut off after reading files. It ran no checks and left no files, so this review starts from scratch.

## Verdict

**Verified, with minor issues only.** The report's central claim holds: the dual bound θ* = 5.642100574331458 for eg_disc2_s is certified on every leaf of all 8 parts of run G, and the leaves cover the instance's domain. I checked every substantive numerical claim with my own code:

- **Bookkeeping.** The certified boxes are exactly the leaves of the recorded trees: 1,114,361 leaves. Every chunk partition is complete, every leaf is certified with a positive margin, and the threshold is θ*.
- **Coverage.** Proved exactly, without using the tree.
- **Model.** The data the certifier used are identical to the cached OSIL model.
- **Independent re-certification.** A sample of 10,404 leaves of parts 0 and 2–7 was re-certified with my own outward-rounded interval code, with 0 failures. The sample includes the 300 tightest leaves of each part.

One caveat stays, and the report states it in Section 4: the certification of *all* leaves rests on the earlier review's certifier (`indep_cert.py`), which is rigorous under its assumptions A1 and A2. My interval re-certification removes these assumptions for the 10,404 sampled leaves only.

## 1. What I checked, and how

All code below is mine. It imports neither the certificate author's modules nor the track's scripts. `indep_cert` is imported in only two places:
- in `cmp_model.py`, to read its data arrays for comparison;
- in `indep_repro.py`, a reproducibility check that is labelled as such.

### 1.1 Model: the cached OSIL file vs. the data the certifier used

- `own_model.py` parses `~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil` into exact Fractions. It asserts the structure while parsing:
  - minimise objvar;
  - rows 0–23: objvar + (−h_k(x)) ≥ lb_k;
  - rows 24–27: side rows;
  - each h_k is a sum of 97 terms a·∏ exp(γ_i (μ_i + s_i x_i)²), plus linear terms in rows 24–25.
  
  A generic evaluation of the raw XML tree agrees with the structured decoding to 1.9e-49 (mpmath at 50 digits, 20 points × 28 rows).
- `cmp_model.py` compares this decoding with the arrays of `indep_cert.Model`, which reads the GAMS file. Everything is identical:
  - variable bounds and integrality;
  - every row constant and side bound (exact);
  - linear coefficients;
  - γ and scale per variable;
  - the multiset of the 97 terms (a, μ_1..7) in all 28 rows.
  
  Result: `MODEL DATA IDENTICAL`. **The certified model is the cached OSIL model.**

### 1.2 Bookkeeping (`own_bookkeeping.py`, `logs/own_bookkeeping.log`)

I re-derived each part's leaf list from `rec/rec_disc2_p*.npz` with my own loop: the closed processed boxes taken whole, then the slabs B \ R of every kept box. In all 8 parts:

- **The certified boxes are the leaves.** The boxes saved in the 38 chunk files equal my derived leaves box for box, in the same index order, together with the root boxes.
- **Chunk partition.** In each part, the chunk index sets together are exactly {0, …, n−1}.
- **Results.** Every saved `ok` is True and every margin is > 0. Run G has no pre-closed, open or tiny boxes, and processed = 1 + 2 × kept.
- **Logs.** All 38 chunk logs report θ* = 5.642100574331458 and 0 failures, totalling 1,114,361 / 1,114,361.
- **Report numbers.** The per-part numbers in the report's tables are reproduced exactly: leaves, closed boxes and slabs, +∞ leaves, certificate counts, smallest margins, smallest LP margins and CPU seconds (41,162 s in total). The leaf counts also match the earlier review's table.
- **Threshold.** The float 5.642100574331458 exceeds the decimal θ* by 6.27e-17. Every finite margin is ≥ 1.0e-9, so the float value is certified too.

### 1.3 Coverage, proved exactly without the tree (`own_cover.py`, `logs/own_cover.log`)

The method is a recursive guillotine decomposition over the certified boxes and the root box of each part, using exact float comparisons only.
- At each node, I find a coordinate cut such that every leaf of the node lies entirely on one side of it. Integer coordinates are cut between consecutive integers.
- The node box is split into two closed halves, which together cover it.
- At a node with a single leaf, that leaf must contain the node box.

This proves "every point of the root box lies in a leaf". It does not use the tree records or a volume argument.

Results:
- **All 8 parts.** The proof succeeds, with 2n − 1 nodes for n leaves: the certified boxes form a guillotine partition of each root.
- **Domain.** Each root contains the exact OSIL continuous box (exact Fraction comparisons) and the full i5 and i6 ranges. The i7 ranges [20,23], [24,27], …, [48,50] are disjoint, consecutive and span [20, 50]. **So the leaves cover the whole OSIL domain.**
- **Negative controls on part 7.** Dropping the largest leaf makes the proof fail, and so does shrinking one leaf by 1 ulp in one coordinate.

### 1.4 Independent rigorous re-certification of a sample (`own_ia.py`, `own_sample.py`)

My certifier uses numpy float64 interval arithmetic with outward rounding after every operation: nextafter, plus a 1e-300 pad against flushed subnormals.

**exp is not taken from libm.** It is computed as 2^k·exp(r), with:
- ln 2 enclosed by two doubles, checked exactly by a rational Taylor bound;
- exp(r) from the degree-14 Taylor polynomial in interval Horner form, plus the Lagrange remainder (≤ 1.6e-19 for |r| ≤ 0.35; 1e-18 used).

Every OSIL decimal is enclosed by its two neighbouring doubles.

**Assumptions.** These are IEEE-754 facts only:
- numpy's +, −, ×, ÷ round to nearest;
- `nextafter` is exact;
- `ldexp` is exact for normal results.

**Bounds.** For each box I intersect three enclosures:
- the natural interval extension;
- the first-order mean-value form;
- the second-order Taylor form with an interval Hessian.

The objective rows used are the 4 with the highest float value at the box centre. Any subset of rows gives a valid bound, so this choice is a heuristic that cannot affect soundness. All 4 side rows are always included.

**Certificate.** A box is certified if max over the chosen rows of (lb_k + h_k).lo ≥ a double ≥ θ*, or if a side row is unsatisfiable on the box. Otherwise the box is bisected; integer coordinates are split at integers.

**Sanity tests** (`test_ia.py`, evidence for the implementation): 0 violations against mpmath for:
- the exp enclosure (26,007 arguments);
- row enclosures at points and over random boxes;
- gradient and Hessian enclosures.

Results for parts 0 and 2–7. Logs: `logs/own_sample_A.log`, `logs/own_sample_B.log`, `logs/own_sample_C.log`. Per part, the sample is the 300 leaves with the smallest recorded margin ("tight"), 1,000 random leaves, and the 200 leaves with the lowest float F at a feasible sample point ("lowest-F").

| part | distinct leaves | certified by my code | pieces | my smallest piece margin | tight set includes every leaf with recorded margin ≤ |
|---|---|---|---|---|---|
| 0 | 1,462 | 1,462 | 8,764 | 2.1e-6 | 4.7e-3 |
| 2 | 1,490 | 1,490 | 12,846 | 2.4e-4 | 9.2e-3 |
| 3 | 1,493 | 1,493 | 15,871 | 2.6e-6 | 6.0e-3 |
| 4 | 1,495 | 1,495 | 22,773 | 1.9e-4 | 8.1e-3 |
| 5 | 1,492 | 1,492 | 37,646 | 3.6e-5 | 1.6e-2 |
| 6 | 1,489 | 1,489 | 11,949 | 7.7e-4 | 3.8e-2 |
| 7 | 1,483 | 1,483 | 7,365 | 9.7e-4 | 7.2e-2 |
| **total** | **10,404** | **10,404 (0 failures)** | 117,214 | | |

- The sample includes every extreme leaf named in the report. For example, the part 5 leaf with recorded margin 1.4e-7 needed 287 pieces in my code, and my smallest bound there was θ* + 0.31.
- The lowest-F group includes the part 0 leaves next to the near-optimal point of Section 2, issue 5.
- **Part 1** (outside this track's scope; the earlier review re-certified all of it): all 300 random leaves are certified. Of the 10 tightest leaves, 4 are certified and 6 hit the 3,000-piece cap (`logs/own_sample_E.log`). This is expected: near the optimum, F(x*) − θ* = 5.6e-9 and several rows are active, so a max-of-rows interval bound cannot reach θ*. LP multipliers are needed there, which `indep_cert` uses.

### 1.5 Soundness consistency of all recorded certificates (`own_consistency.py`, `logs/own_consistency.log`; float evidence)

The test covers every one of the 1,114,361 leaves.
- I evaluated F and the side rows at the leaf centre and at 4 random points of the leaf.
- A recorded margin mg requires F(p) ≥ θ* + mg at every feasible point. For row certificates at the leaf itself, it requires this at every point.

**Result: no violation in any part.** The smallest slack F(p) − (θ* + mg) at feasible points per part is:

| part | smallest slack |
|---|---|
| 0 | 3.2e-4 |
| 1 | 1.1e-5 |
| 2 | 6.0e-4 |
| 3 | 1.4e-4 |
| 4 | 8.9e-5 |
| 5 | 5.6e-5 |
| 6 | 1.7e-5 |
| 7 | 7.0e-4 |

A first run had a bug: the violation measure was initialised to 0, so no point counted as feasible. Its log is kept as `logs/own_consistency_bug_viol_init.log`; its row-certificate part was valid. The run above is the corrected one.

### 1.6 Reproducibility of the recorded results (`indep_repro.py`, `logs/indep_repro.log`; not independent)

- I ran the earlier review's `indep_cert.Certifier` unchanged, without the track's `MarginCertifier` wrapper, on 100 random leaves per part. All 800 were certified.
- For the 502 of them recorded as row certificates at the leaf itself, I recomputed max_k (c_k + rmin_k) − θ* exactly from the certifier's enclosures. All 502 equal the recorded margins.
- I also read `margin_cert.py` against `indep_cert.py`. The changes only record the certificate type and margin; the certification decisions are unchanged, as `check_copy.log` also shows.
- `git` shows that `rec/`, `res/` and `reviews/eg-retry-review-checks/` are unchanged since c3514f03 and HEAD. `indep_cert.py` was last changed in a0b2eebe.

### 1.7 Not re-derived

I did not redo the earlier review's full error analysis of `indep_cert.py` (A1). I spot-checked parts of it by hand:
- the Taylor remainder formulas: φ''' = φ p (p² + 6b) and φ'''' = φ (p⁴ + 12 b p² + 12 b²), with their R2 and R4 bounds;
- the quadratic-term bound;
- the padding constants for the t-ranges, the exponent sums and the 97-term sums against the required multiples of u.

All of these are correct. A2 (numpy exp error ≤ 1e-14 relative) remains a sampled assumption: 1.5 M arguments by the track and 25,000 by the earlier review.

## 2. Issues (all minor)

1. **The headline and the suggested integration wording omit the A1/A2 qualifier.** Section 1 says the bound is "verified on every leaf", and the proposed text for `open-instances-summary.md` says "re-certified with independent code". The certification of all leaves is rigorous only under A1 (a hand-checked error analysis) and A2 (sampled exp accuracy). Section 4 says so, but the headline should too. Suggested wording:

   > verified: all 1,114,361 leaves of run G re-certified with the earlier review's independent certifier (rigorous under its assumptions A1, A2); coverage proved exactly; 10,404 leaves of parts 0 and 2–7, including the 300 tightest per part, also certified with outward-rounded interval arithmetic and no libm assumption (publication/reviews/eg-recheck-review-r1.md)

2. **"98,234 leaves were proved to contain no feasible point" overstates.** The leaves with margin +∞ split as follows:
   - 85,685 were closed by side-row infeasibility at the leaf itself;
   - 373 were closed by the Farkas test, which proves only that there is no feasible point with F < θ*, not that the leaf is infeasible;
   - 12,176 were closed after splitting, and their pieces may include Farkas pieces.
   
   Suggested wording: "98,234 leaves have no feasible point with F < θ*; 85,685 of them were proved infeasible directly".

3. **The leaf numbering convention is not stated.** "Part 5 leaf 69407" and the leaf numbers in `logs/tight_leaves.log` and `logs/inspect_leaf_p5_69407.log` are positions in the concatenation of the chunk files. They are not indices in the part's leaf list as `verify_tree.py` builds it. The 1.4e-7 leaf is index 56587 of part 5 (the same box).

4. **The Git bullet in Section 8 is out of date.** The second-pass files are committed in 514a788f. Only `report.md` is untracked now.

5. **Near-optimal points outside part 1** (informational, float evidence). The remark "small margins outside part 1 are loose bounds, not near-optimal regions" is right for the tightest-margin leaves. However, part 0 has feasible points with F − θ* = 0.0066, at about x = (0.3238, 1.0, 0.7863, 1.2655, 11, 35, 23); `logs/local_min.log`. The smallest float values of F − θ* found per part are:

   | part | 0 | 2 | 3 | 4 | 5 | 6 | 7 |
   |---|---|---|---|---|---|---|---|
   | float min of F − θ* | 0.0066 | 0.30 | 0.29 | 0.51 | 0.99 | 1.77 | 2.77 |

   The paper should not imply that parts 0 and 2–7 are all far from θ*.

6. **Coverage proof** (a suggestion). The report's coverage proof relies on the tree bookkeeping in `verify_tree.py`. Its tree-free check (volume identity plus random points) is only a cross-check, as the report correctly says. The exact tree-free guillotine proof in Section 1.3 can now be cited as well.

There are no correctness problems with the counts, the threshold, the chunk bookkeeping, the coverage, or the model used.

## 3. Status of the report's claims

| claim | status |
|---|---|
| 1,114,361 leaves (979,044 in parts 0 and 2–7 + 135,317 in part 1); 1,152,830 processed boxes; processed = 1 + 2 × split boxes | verified (own code) |
| every leaf certified against θ* = 5.642100574331458, 0 failures | verified from the recorded results (own code). Reproduced on 800 random leaves with the unchanged `indep_cert`. Independently re-certified on 10,404 leaves of parts 0 and 2–7 (own interval code). Rigorous for all leaves under A1/A2. |
| the chunks partition each part's leaf list | verified (own code) |
| the leaves cover each part; the parts cover the OSIL domain | **proved** (own exact guillotine proof) |
| the certified model is the MINLPLib instance | verified: OSIL data identical to the certifier's data |
| per-part margins, certificate counts, CPU | verified (own code), except the "proved infeasible" wording (issue 2) |
| the certification path does not load the author's modules | consistent with my reading of the imports of `indep_cert.py`, `gms_model.py`, `verify_tree.py`, `recheck_leaves.py` and `margin_cert.py` |
| the replayed trees are the run G trees (`compare_logs.log`) | not re-run; the bound does not depend on it, because coverage and certification are checked on the boxes themselves |
| negative controls, tight-leaf float minima | read; consistent with my own float evidence |

## 4. Commands run

All Python runs used `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1` and were started from `research-20260929/publication/reviews/eg-recheck-r1/`.

| command | outcome |
|---|---|
| parse the predecessor transcript (`wf_a89a60b6-d10/agent-a822c5761b47f4b46.jsonl`) | it read files only; no checks run, no files left |
| `timeout 580 python3 own_model.py` | OSIL decoded; XML vs decoding 1.9e-49 |
| `timeout 580 python3 cmp_model.py` | MODEL DATA IDENTICAL |
| `timeout 590 python3 own_bookkeeping.py` | ALL GOOD; per-part numbers equal the report's |
| `grep` over the 38 `logs/cert_p*_c*.log`; inline min of `min_lp_margin` per part | θ* string in all 38; 0 failures; 1,114,361 / 1,114,361 |
| inline `prove_cover` on part 7 with 2 negative controls | covered; both controls fail as intended |
| `timeout 590 python3 own_cover.py` | COVERAGE PROVED (8 parts and domain) |
| `timeout 590 python3 test_ia.py`; inline ln 2 check and 4 tight leaves | 0 violations; ln 2 enclosure proved; 4/4 certified |
| `setsid nohup timeout 3000 python3 own_consistency.py` (run twice; first run had a bug) | NO VIOLATION |
| `setsid nohup timeout 7000 python3 own_sample.py 0,2,3 300 1000 0 20000 A` | 3,890 / 3,890 certified |
| `setsid nohup timeout 7000 python3 own_sample.py 4,5,6,7 300 1000 0 20000 B` | 5,184 / 5,184 certified |
| `setsid nohup timeout 7000 python3 own_sample.py 0,2,3,4,5,6,7 0 0 200 20000 C` | 1,400 / 1,400 certified |
| `own_sample.py 1 50 300 50 20000 D` | stopped by me (piece cap too large); no result |
| `setsid nohup timeout 3000 python3 own_sample.py 1 10 300 0 3000 E` | part 1: 300/300 random; 4 of the 10 tightest certified, 6 at the cap (expected) |
| inline union of samples A, B and C | 10,404 distinct leaves, all certified |
| `timeout 590 python3 indep_repro.py 100` | 800/800 reproduced; 502 margins identical |
| `timeout 590 python3 local_min.py` | part 0 float min F − θ* = 0.0066; other parts ≥ 0.29 |
| inline count of +∞ leaves by certificate | side 85,685; Farkas 373; split 12,176 |
| inline `Fraction` comparison of the θ* float and decimal | +6.27e-17 |
| `git status`, `git diff --quiet c3514f03 HEAD`, `git log`, `md5sum` | rec, res and reviewer checks unchanged; report.md the only untracked file of the track |
| `ps` / `pgrep` at the end | no processes of this review left running |

## 5. Files (in `publication/reviews/eg-recheck-r1/`)

- **Code.**
  - `own_model.py`, `cmp_model.py`: model reading and comparison.
  - `own_bookkeeping.py`: bookkeeping check.
  - `own_cover.py`: coverage proof.
  - `own_ia.py`, `test_ia.py`, `own_sample.py`: interval certifier, its tests and the sample runs.
  - `own_consistency.py`, `local_min.py`: float evidence.
  - `indep_repro.py`: reproducibility check.
- **Data.**
  - `leaves_p*.npz`: derived leaves with the recorded margins.
  - `minF_p*.npy`: per-leaf smallest feasible F from the consistency test.
  - `sample_{A,B,C,E}_p*.npz`: per-leaf results of the sample runs.
- **Logs** (`logs/`): `own_model.log`, `cmp_model.log`, `own_bookkeeping.log`, `own_cover.log`, `test_ia.log`, `own_consistency.log`, `own_consistency_bug_viol_init.log`, `own_sample_{A,B,C,E}.log`, `own_sample_D_killed.log`, `indep_repro.log`, `local_min.log`.
- `PROGRESS.json`.

Implementation clarification (2026-10-04, integration review r2 issue 4): the 41,162 s labelled CPU seconds above is wall time summed over chunks (time.time()), with 5,372 s scheduler elapsed wall time; the review findings and stored timing data are unchanged.
