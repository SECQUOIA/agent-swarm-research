<!-- Written to disk by the root from the structured return value of verifier round 2 of track lit-control in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review: lit-control literature check, round 2

**Reviewer:** independent verifier for lit-control, round 2.

**Report reviewed:** the revised report returned by the author, to be written to `/workspace/minlp-notes/research-20260929/publication/literature/control/report.md`. I compared it with the round-1 review, `reviews/lit-control-review-r1.md`.

**My code, data and logs** are in `/workspace/minlp-notes/research-20260929/publication/reviews/lit-control-r2/`:
- `PROGRESS.json`
- `cmp_camshape.py` and `.log`: exact rational comparison of the MINLPLib and QPLIB camshape models
- `bound_rel.py` and `.log`
- `diffs.py` and `.log`: logged values against the certified optima
- `web/`: fetched pages, logs, snapshots, papers and model files, with `SHA256SUMS.txt`. Files over 1 MB were hashed and then deleted; see `web/DELETED_LARGE_FILES.txt`.

## Verdict: verified (no blocker, no major issue; 7 minor issues)

Both major issues from round 1 are resolved, and all 9 minor issues are fixed. The new facts in the report are correct at their stated locations, with the small exceptions listed below. I re-fetched every new source and checked each numerical claim with my own code.

I agree with the author's three corrections to the round-1 review:
- **SCIP version.** The stored SCIP logs say "SCIP version 9.2.1" and the directory listing dates them 2025-04-04. They are not 10.0.1.
- **COPT's optcdeg2 bound.** It is 283.407898545, which is weaker than MINLPLib's GUROBI bound 292.41713458.
- **Rounding shift of the camshape optimum.** It is not established. BARON's QPLIB_2738 incumbent, −4.28414710266608, lies only 1.9e-8 above the exact MINLPLib optimum.

My searches for further prior results found nothing new (Section 4).

The novelty labels are well supported by the evidence and the report states their caveats. The labels are:
- 10 new as far as found;
- camshape800: a prior global claim exists and is false;
- 7 partly known;
- camshape100: already solved globally in floating point.

## 1. Resolution of the round-1 issues

| round-1 issue | status | what I checked |
|---|---|---|
| **M1:** Mittelmann QPLIB benchmark and QPLIB camshape copies | resolved | Re-fetched cnconv.html; its sha256 is identical to the author's copy. Re-fetched all 30 logs: 25 are byte-identical to the author's, and for the other 5 the author stored excerpts. Re-queried the Wayback CDX: 7 distinct 200-status versions exist, so the author's 7 snapshots are complete; I re-fetched all 7 and they are identical. Every time, version and value in the new Section 3 table is confirmed (details in Section 2). |
| **M2:** Waki, Kim, Kojima and Muramatsu (2006) | resolved, apart from minor issue 2 | Preprint re-fetched; same sha256. Confirmed: problem (39) and "the second problem (5 of [3])" on printed p. 30; [3] is Coleman–Liao; Table 12 on p. 31 (order ω = 1, M = 600–1000, n = 1198–1998, ε_obj 3.4e-8, 2.5e-8, 5.9e-8, 1.4e-7, 6.3e-8, CPU 3.3–5.0 s); the sentence "theoretically guaranteed to provide bounds with the same quality as the dense relaxation" on p. 31; the perturbation \|p_j\| < 1e-5 on p. 21; added bounds and κ = 1e-5 for Tables 7–8 on p. 26. |
| Minor 1: QPLIB filter | fixed | Preprint p. 18: (1) instances solved by at least 30% of complete solvers within 30 s are discarded; (2) clustering, then one complete solver with a 120 s limit. |
| Minor 2: optcdeg2 "original source" | fixed | The bottom line names OPTCDEG2.SIF and OPTCNTRL.SIF and says Murtagh–Saunders was not read. |
| Minor 3: "identical to COPS 3.0" | fixed | Chain is now called an "equivalent reformulation". |
| Minor 4: Mattick–Mutschler gaps | fixed | Table 8: Gap Base 0.074–0.226 and Gap Ours 0.076–0.222. |
| Minor 5: GloMIQO | fixed | The GloMIQO 2.0 Test Set (8 Jul 2012) says "187 GLOBALLib Test Cases" without naming them. The ANTIGONE 1.0 Test Suite (1 May 2013), Table 4, PDF p. 21, lists camshape100–800, catmix100–800 and chain50–400; lnts does not appear, and p. 1 says trigonometric forms are excluded. |
| Minor 6: further tolerance artifacts | fixed | All differences recomputed with my own `diffs.py` (Section 3). |
| Minor 7: DTOC5.SIF SOLUTION lines | fixed | DTOC5.SIF re-fetched; values N = 10/100/500/1000/5000 confirmed (the file also has N = 50: 1.528586458855, which the report omits). |
| Minor 8: out-of-date open issue | fixed | The sentence is no longer in the report. |
| Minor 9: Müller et al. 2019 | fixed, apart from minor issue 3 | arXiv 1912.00356v1 re-fetched; same sha256. Confirmed camshape800 "best primal" −4.27431, lnts50 0.511237, and chain MILP bounds −115 to −343. |

## 2. Minor issues found in round 2

### 2.1 The author's camshape bound comparison ignores every upper bound

`checks/qplib_camshape_compare.py` reads bounds with `^(\w+)\.(lo|up|fx) = ...;` and `re.M`. In all eight files each bound pair sits on one line, for example `x1.lo = 1; x1.up = 1.00015482411709;`. So only the lower bounds were captured. The upper bounds were never compared or evaluated, including:
- the curvature limits on the d variables (±αθ);
- the r1 end bound.

The author's log confirms this: every reported "largest bound difference" is a lower bound (index 0).

My own exact rational comparison (`cmp_camshape.py`, `bound_rel.py`) covers all bounds:

| pair | rows matched (support, sense) | max relative coefficient difference | max relative bound difference | bound presence |
|---|---|---|---|---|
| camshape100 / 2738 | 201/201 | 1.31e-10 | 2.67e-10 (x102.lo, a d bound) | all match |
| camshape200 / 2480 | 401/401 | 2.24e-10 | 2.42e-10 | all match |
| camshape400 / 2703 | 801/801 | 2.16e-10 | **4.71e-10** (x1.up: 1.00000982052922 vs 1.000009821) | all match |
| camshape800 / 3177 | 1601/1601 | 1.22e-10 | 2.50e-10 (x1.up) | all match |

The report's "largest relative bound difference 2.4e-10", and "within 2.5e-10" in the structured summary, should read 4.7e-10. The conclusion stands: the copies are the MINLPLib models with constants rounded at the 1e-10 level. QPLIB_3177 is still at about 2.5e-10.

The point checks the report cites also hold when upper bounds are included:
- camshape100: p1 violates QPLIB by 3.03e-10, and the QPLIB point satisfies both models to 2e-14.
- camshape800: p1 violates QPLIB by 5.06e-10.

One effect the author's script missed: the QPLIB points for 2480 and 2703 violate MINLPLib's r1 upper bound, by 2.5e-11 and 4.7e-10. The report does not claim otherwise.

**Fix:** correct the number, and fix the regex (drop the `^` anchor).

### 2.2 Waki et al. Table 12 quoted slightly wrongly

- **ε_feas range.** The values are −2.2e-10, −8.1e-10, −1.6e-10, −6.8e-10 and −2.7e-10, so the range is −1.6e-10 to −8.1e-10, not "−2.2e-10 to −8.1e-10".
- **"M ≤ 1000".** The bottom line and summary table say "M ≤ 1000", but Table 12 tests only M = 600, 700, 800, 900 and 1000. The table on p. 30 with M = 6–30 is for problem (38).

Write "M = 600–1000".

### 2.3 Page location in Müller et al.

The camshape100 row (Table 4: MILP −5.0295, S = −4.92812 / −4.90792) is on PDF p. 40, not p. 41. camshape200–800 are on p. 41.

### 2.4 MINOTAUR's camshape800 claim: stronger evidence is available

**Context on camshape800.** The 3177 run closes at the root: 1 node, 3 s, "best bound estimate from remaining nodes = inf". On the smaller copies, the same MINOTAUR 0.4.1 runs to the 3 h limit with bounds −4.5374 (2738), −4.8494 (2480) and −5.1678 (2703), and gaps of 5.9%, 13.3% and 20.8%. Root fathoming at −4.2774 on the largest copy is therefore not credible even as a floating-point result; it looks like a solver error.

Adding this would support the report's word "false", as opposed to "tolerance artifact". The report applies the two terms unevenly:
- ANTIGONE's camshape100 "global minimum" −4.284302 also lies below the exact optimum. Its dual bound −4.284302 is valid.
- MINOTAUR's camshape800 value is likewise attainable only within tolerance: COPT's incumbent −4.277371 has a quadratic violation of only 2.98e-8.

State explicitly that "false" means false under exact feasibility, and give the evidence that the camshape800 claim is spurious.

### 2.5 MINOTAUR dtoc5: the default bounds can be inferred

`QuadHandler::addDefaultBounds` in the MINOTAUR source (github.com/coin-or/minotaur, master branch, fetched 2026-10-02) sets the default bound to 100 times the largest finite bound magnitude, or ±1000 if there is none. QPLIB_8585 has one bounded variable, x50001, fixed at 1. That gives [−100, 100]. The QPLIB solution has max \|x\| = 8.06, so the box contains the optimum.

Caveat: the benchmarked revision, v0.4-50-g456fd8cc, may differ from master.

The dtoc5 closure was also root-only (1 node). That is plausible here, since the project's certificate shows that a convex (Lagrangian) relaxation is exact for this instance. This narrows the open issue "the default bound values ... are not stated".

### 2.6 Wording: "MINLPLib optimizer"

"The MINLPLib optimizer violates the QPLIB model by only about 5e-10" (camshape800) refers to MINLPLib point p1. That point violates MINLPLib camshape800 itself by 3.9e-10 (row e1562), so it is not the project's exactly feasible optimizer. Write "MINLPLib point p1".

### 2.7 Wording: CONOPT's 8.7e-6

The 8.7e-6 is the value in CONOPT's "Infeasibility" column for its input point (8.7007237331E-06). That is CONOPT's aggregate measure, not necessarily the largest row violation. The log also does not state that the input point is ANTIGONE's incumbent, though that is the natural reading.

## 3. Claims I verified (my own fetches and code)

**Benchmark page and history**
- cnconv.html (17 May 2026), confirmed:
  - solvers BARON 25.12.10, ANTIGONE 1.1, SCIP 10.0.1, MINOTAUR 0.4.1, COPT 8.0.4;
  - 102 instances, 3 h limit, 8 threads, "All problems were solved GLOBALLY";
  - rows 2738: ANTIGONE 852; 3177: MINOTAUR 3; 8585: MINOTAUR 1005.
- Snapshot timeline, all as reported:

  | page date | entries for our instances |
  |---|---|
  | 3 Dec 2021 | 2738: ANTIGONE 1857, Octeract 3.6.0 37; 3177: MINOTAUR 0.2.1 19; 8803: MINOTAUR 1641. The header says only "at least one solver succeeded". |
  | 7 Jan 2023 | 2480: Octeract 4.5.1 6853; 2738: ANTIGONE 1857, Octeract 8; 3177: MINOTAUR 0.3.0 5. "solved GLOBALLY" first appears. |
  | 9 Mar 2024 | 2738: ANTIGONE 1857, Octeract 4.7.1 17; 3177: MINOTAUR 0.4.0 16. No 2480 row. |
  | 21 Aug 2024 | 2738: ANTIGONE 744; 3177: MINOTAUR 6 |
  | 4 Apr 2025, 11 Jul 2025, 28 Sep 2025 | 2738: ANTIGONE 744; 3177: MINOTAUR 3 |

**Logs**
- MINOTAUR:
  - 3177: "Optimal solution found", −4.2774, 1 node;
  - 8585: two default-bound warnings (99983 and 99997 variables), 5.3897, 1004.60 s;
  - 8803: "status of presolve: Detected infeasibility".
- ANTIGONE:
  - 2738: "Termination Status : Global minimum", −4.284302 / −4.284302, OptCR 0; CONOPT polishes to −4.28414626579;
  - 2480: −4.601964; 2703: −4.969835; 3177: −5.170263;
  - 8585 and 8803 stop after pre-processing with no result.
- BARON:
  - camshape copies: −4.28414710266608, −4.27849246237069, −4.27565886682199, −4.51546318707998;
  - 8585: 5.38966688447816 (bound 2e-5); 8803: 293.876075074557;
  - both 8585 and 8803 print "Globality is therefore not guaranteed".
- COPT:
  - incumbents −4.284189915, −4.278677725, −4.276430314, −4.277371318, 293.880662592 and 5.389829024;
  - bounds 0.761858180 (8585), 283.407898545 (8803) and −4.385442317 (2738).
- SCIP 9.2.1, camshape400 primal: −4.33023953971002.

**Distances from the certified optima** (`diffs.py`, exact decimals). All match the report:

| solver and instance | difference from the certified optimum |
|---|---|
| ANTIGONE camshape100 | −1.549e-4 |
| COPT camshape100 / 200 / 400 / 800 | −4.28e-5 / −1.78e-4 / −7.42e-4 / −3.10e-3 |
| SCIP camshape400 | −5.46e-2 |
| MINOTAUR camshape800 | −3.13e-3 |
| BARON camshape800 | −0.241 |
| BARON dtoc5 | −5.23e-6 |
| BARON optcdeg2 | −2.13e-8 |
| Müller camshape800 | −3.59e-5 |
| GUROBI optcdeg2 | −1.459 |
| BARON camshape100 | +1.91e-8 |

**Model identity**
- My diff of MINLPLib dtoc5.gms and optcdeg2.gms against QPLIB_8585.gms and QPLIB_8803.gms, comment lines removed: identical apart from the solve block and, in 8803, a `Positive Variables x50001,x100004;` line. Both files fix those two variables at 0. The sha256 values equal the author's.
- The OSIL constants of camshape400 and camshape800 (1.99999017956722; ub 1.00000982052922 and 1.0000024612497) equal the .gms constants.

**Library data**
- QPLIB pages: LCQ, donor Ruth Misener, and the stated sizes for 2738/2480/2703/3177; 8803 solinfeasibility 1.7525e-15.
- qplib.solu: all six entries marked `=best=`, with the stated values.
- QPLIB listing scan of the 134 continuous instances: the only size match to catmix100 is QPLIB_3337. Its model (objective −1e8, different rows) is not catmix, so no catmix copy was found. This is evidence only, as the report says.

**Sources**
- Manifest: 127 rows, all sha256 match, no missing or unlisted files.

## 4. My searches for missed sources (none found)

- **Mittelmann MINLP benchmark history.** Wayback snapshots of minlp.html from 2022 to 2024, and compare.txt and nontrivial.txt from 2024 to 2025, plus the live files. camshape100 entered the benchmark between Oct 2024 and Mar 2025, after Octeract had left. So Octeract's "solved all problems" (April 2023) did not include it. This is consistent with the report's statement that the 2023 compare.txt lacks camshape100.
- **COIN-OR GAMSlinks global benchmarks (2008–2012).** These cover discrete MINLPLib only; none of our instances appears.
- **SparsePOP.**
  - The distribution has `optControl2.m`, which is the DTOC5 source model with bounds ±1e10.
  - The 2005 SparsePOP report (optimization-online 1091) has no optimal-control results.
  - Waki et al. remains the relevant citation.
- **Papers and reports grepped for our names and QPLIB IDs, with 0 hits:**
  - the SCIP 9.0 report (arXiv 2402.17702) and SCIP 10.0 report (2511.18580);
  - Parabolic relaxation Part II (2208.03625);
  - Learning to relax QCQPs (2501.03954);
  - the sublevel moment-SOS hierarchy (2101.05167);
  - the Tez thesis (Sabancı);
  - the Edinburgh thesis (handle 1842/42202);
  - Zenodo record 17714454.
- **WebSearch:** 8 queries on MINOTAUR, camshape, dtoc5/optcdeg2, catmix/chain/lnts, lukvle10, Octeract, SDP relaxations of discrete optimal control, and catalyst mixing global optimality.

## 5. Commands run (targeted; outcomes recorded)

**Manifest**
- python sha256 check of `sources/MANIFEST.md`: 127/127 match, 0 missing, 0 unlisted.

**Mittelmann QPLIB benchmark** (`curl`, sequential, at least 1 s apart)
- cnconv.html: identical to the author's copy.
- 30 logs `cnconv_logs/{ant,bar,cop,mnt,sci}_results/QPLIB_{2738,2480,2703,3177,8585,8803}.*`: all succeeded.
- Log directory listings for the file dates.
- Wayback CDX: the first attempt returned "Temporarily Offline"; the second succeeded. Then the 7 `id_` snapshots: all succeeded and are identical to the author's.

**Model files**
- QPLIB .gms and .sol for the 6 IDs; qplib.solu; instances.html; pages for 3177, 3337 and 2758.
- MINLPLib .gms for dtoc5, optcdeg2 and camshape100–800; camshape100–800 p1 .sol files.
- All succeeded.

**Sources and searches**
- Papers: Waki 988.pdf, QPLIB 5846.pdf, the ANTIGONE and GloMIQO test-suite PDFs (Wayback), arXiv 1912.00356v1, DTOC5.SIF (bitbucket optrove), and the candidate papers in Section 4. All succeeded.
- Mittelmann bench.html; Wayback CDX and snapshots for minlp.html, compare.txt and nontrivial.txt; the live compare.txt, nontrivial.txt and select.txt.
- GAMSlinks benchmark index and MINLP pages; the SparsePOP GitHub tree and examples.
- MINOTAUR QuadHandler.cpp (GitHub raw).
- WebSearch: 8 queries.

**Text extraction**
- `pdftotext -layout` with page-located Python and grep on all fetched PDFs.
- grep of the logs for statuses, bounds and incumbents.

**My own checks**
- `python3 cmp_camshape.py N q` for (100, 2738), (200, 2480), (400, 2703) and (800, 3177) → `cmp_camshape.log`.
- `python3 bound_rel.py` → `bound_rel.log`.
- `python3 diffs.py` → `diffs.log`.
- `diff` of the dtoc5/optcdeg2 files against QPLIB_8585/8803 with comments stripped.
- grep of the cached OSIL constants for camshape400 and camshape800.
- Python scan of the QPLIB listing.

**Not done**
- No GAMS or solver runs, no background jobs; no processes of mine remain.
- No project-wide checks, no CI inspection, no git operations.
- Other tracks' processes were not touched.
