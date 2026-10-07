# Review round 1: `scip-set-selection/note.md`

Reviewer: independent research agent (did not write the note, patch or code).
Date: 2026-10-03. Scope: the note, the patch
`patch/scip-10.0.3-setrule.patch`, the stream code and the raw logs. I did not
edit the note or the stream code, did not change git state, and started no
benchmark. All review code is in `reviews/r1-code/`, all review outputs in
`reviews/r1-logs/`. The only SCIP runs were short, targeted runs, described
under "Checks run".

## Verdict

**Minor fixes, with one major issue.**

All tables in Sections 6, 7 and 8.2 that I recomputed with my own parser from
the raw logs match the note exactly. I also confirmed the debug-solution
counts, the "omitted objective helper" correction, the patch's formulas and
the S-freeness proof. The no-go recommendation is supported. Its basis is
the comparison of the rules with each other and the root results, and these
are not affected by the major issue.

The major issue is a false fairness claim. Under `setrule = 0` the patch is
**not** behaviour-neutral in tree search. It captures every added
intersection-cut row so that it can count them, and this changes SCIP's
search path (shown deterministically on `tln7`). So the `scip`, `corner` and
`eff` full solves all differ from stock SCIP in the same way. The `off` runs
are stock SCIP. The note says that the default "reproduces SCIP exactly" and
that the `scip` rule uses an "unchanged code path". Both statements must be
corrected, and the full-solve comparisons against `off` need a caveat.

## Issues

### Major

**M1. The patch changes SCIP's search when the cuts are on, including `setrule = 0`.**
Location: Section 2 (Rule 0, "unchanged code path"), Section 3 ("defaults
reproduce SCIP exactly", "comparisons between rules are on equal terms"),
Section 7, Summary.

The patch calls `SCIPcaptureRow` on every added intersection cut
(statistics `Applied` / `Active` / `RootAppl`) and releases the rows only in
the new `nlhdlrExitQuadratic` callback. In SCIP 10.0.3, `lp.c` unlinks a
row from its columns only in `SCIProwFree` (`rowUnlink` has one call site),
so a cut row stays in memory and stays linked to its columns after the LP
or the cut pool drops it. Measured effect:

- `tln7`, cuts on, seed 0, 2000-node limit. The patched binary with
  `setrule = 0` gives 5939 dual LPs, 27844 iterations, dual bound 13.9974
  and primal bound 17.1. An unpatched SCIP 10.0.3, built from the tarball's
  `nlhdlr_quadratic.c` with build-lapack's flags and objects, gives 5550,
  25644, 14.1603 and 16.1. Both results repeat exactly on a rerun.
- The patched source with only the `SCIPcaptureRow` block removed matches
  the unpatched binary exactly. So the capture is the cause.
- Root-only runs (`limits/nodes = 1`) were identical, apart from timing, on
  all 13 instances checked: blend029, crudeoil_pooling_ct2, ex5_2_5,
  ex8_3_2, genpooling_meyer04, kall_circlespolygons_c1p11, nvs17,
  pointpack08, qp3, sssd16-07persp, st_e31, tln7 and waterund08. Three other
  full-set instances were identical at 2000 nodes: blend852, ex5_4_2 and
  kall_congruentcircles_c52.

Consequences:

- The rule comparisons (`scip` / `corner` / `eff`) are fair among themselves,
  because all three carry the capture.
- In the full solves, `off` is stock SCIP without cuts, while every cut-on
  setting is a perturbed SCIP with cuts. The perturbation can act like a
  seed change. It can also add a systematic cost, because column row lists
  keep growing with dead cut rows. Its size is not known.
- This affects the full-solve answer to "worth enabling" (Section 7.1–7.3,
  the Summary sentences comparing with cuts off) and the `scip` versus `off`
  numbers, including `tln7` seed 1, which `scip` solves at 283 s.
- The Section 6 root results appear unaffected.

Required change:

- Correct Sections 2, 3 and 7 and the Summary.
- State that all cut-on full solves include this instrumentation side
  effect, that root runs were unchanged on the checked instances, and that
  full-solve comparisons with `off` are therefore not stock-SCIP comparisons.
- Recommend that any future full-solve run count applied cuts without
  keeping rows alive, for example with a row-deletion event that reads
  `SCIProwGetNLPsAfterCreation` before release, or with the statistic
  switched off.
- The no-go conclusion for the two rules can stay, since it rests on rule
  comparisons and root bounds. The full-solve statements about cuts off
  versus cuts on should be marked as affected.

### Minor

**m1. The `st_glmp_fp2` reference solution is not optimal; say so, and add the facts that close the 73-row question.**
Location: Section 9.1, Summary.

- The supplied `st_glmp_fp2.p1.sol` (x1 = 0, x2 = x3 = 5.65, x4 = 1.35) is
  feasible for all OSiL constraints. Its objective is 7.6275, but
  `minlplib.solu` gives `=opt=` 7.3445454. The note implies this only
  generically.
- I independently re-evaluated all 73 reported intersection rows. Each row
  contains only `t_x1`, `t_x2` and `t_nlobjvar`. Every row has a positive
  `t_nlobjvar` coefficient. Every row was reported before any incumbent
  existed. With `t_nlobjvar = 7.6275` the smallest slack is 0.0175438, as the
  note says. Because the coefficient is positive, every row is satisfied for
  every feasible helper value `≥ x3·x4`.
- So the correction is right and hides no invalid cut. Please add these
  three facts: positive coefficients, reports before any incumbent, and a
  non-optimal reference point.
- The nine `overestimate_pow` messages are **local** secant rows of `x2²`.
  From their coefficients, the node domain is about x2 ∈ [6.4508, 6.4553]
  for one row and [6.4539, 6.4544] for the other. That excludes the
  supplied x2 = 5.65, so these are checker false alarms, not cut
  violations. They were preceded by "invalid local lower bound implication"
  errors that come from the infeasible debug point. They can be described
  as resolved rather than "not similarly certified".

**m2. Resolve the `kall_congruentcircles_c52` discrepancy.**
Location: Sections 7.3 and 9.1.

I reran `kall_congruentcircles_c52`, `eff`, seed 2 with the benchmark
binary. It reproduces the archived run exactly: 3830 nodes, objective
1.5371086884193. SCIP's `checksol` gives:

- "solution is feasible in original problem";
- maximum constraint violation `9.5·10^-7` (below the default feasibility
  tolerance `10^-6`);
- LP-row violation `1.3·10^-8`;
- bound violation `9.7·10^-10`.

The objective shortfall of `2.1·10^-6` is therefore tolerance-level
infeasibility of a solution SCIP accepts, not a validity problem. The same
effect occurs with SCIP's own rule in the debug runs. The note can replace
"merit a primal-feasibility check" with this result (log:
`reviews/r1-logs/kall_c52.eff.s2.log`).

**m3. Wrong range of median criterion gains in Section 8.**
"rule 1: median gain 1.25–1.65 on the dumps where it changed `λ`". In
`logs/dumps/checks_summary.md` the rule-1 medians are 1.049 (crudeoil),
1.068 (st_e31), 1.096 (ex8_3_2), 1.143 (tln7), 1.252, 1.513, 1.608, 1.619
and 1.651. The range is 1.05–1.65.

**m4. Section 4.4 reports search-optimality results for only two of the completed dumps.**
`logs/dumps/search_opt_*.out` also contains:

- `ex8_3_2`: C search within `10^-4` of the family optimum on 5 of 11
  corners; mean ratio 0.894, the same as SCIP's λ (0.894). The search gains
  nothing there on average.
- `st_e31`: 7 of 7.
- `waterund08`: 2 of 2.
- `kall_circlespolygons_c1p11`: 1 of 40, already discussed in Section 8.1.
- `tln7`: the run crashed with no `dim λ = 2` corners.

Report all of them, or state how the two shown were selected. "On these two
dumps the best angle was never outside the half circle" holds for all the
completed outputs (`best_outside_halfcircle = 0` everywhere).

**m5. The fairness facts for timing should be stated, including the mitigating ones.**
Location: Sections 7.3 and 10.

- The 300 debug-solution runs (first log at 20:10 on Oct 2) ran **during**
  the full benchmark (19:37 to about 21:30). This adds to the load the note
  describes.
- Two facts mitigate the load problem. `run_bench.py` orders jobs by
  instance, so all settings of an instance run close together in time. The
  median wall/CPU ratio of the full runs above 5 s is 1.22 / 1.21 / 1.21 /
  1.20 for `off` / `scip` / `corner` / `eff`.
- Add these points to the limits paragraph.

**m6. Clarify the base of the Section 6, finding 5 numbers.**

- The 76% / 79% shares of changed λ and the medians 1.43× / 1.04× are over
  all root instances with a change (267 instances), not the 251 compared
  instances. I reproduced them: 173928 / 228135 and 184473 / 233699.
- "about 0.45 ms per cut" is per *generated* cut. There are about 2.4
  searches per generated cut, so the cost is about 0.18 ms per search.

**m7. Section 2, item 4 states a corner-bound fact without its caveat.**
"Attains `z_K` on all 120 McCormick LP corners" is measured against the
stored `z_K`. The sibling streams show that the stored `z_K` is wrong on
some of these corners: 10 corners per `scip-rule-fidelity` Section 7.1, and
collinear-ray underestimates per `multiround` Section 1.3. The caveat
appears in item 5 and Section 4.4. Add it here as well, or point to it.

### Optional

**o1. Section 8.1 wording.**

- "has no basis in Theorem 1" is too strong. When zero-cost rays exist,
  maximizing the shortest zero-cost step is the natural first step toward a
  positive bound: a positive single-cut bound needs every zero-cost ray to
  have an infinite step.
- "never accepts a change" holds only when the zero-cost steps are below
  about 10^3. The acceptance test is `critbest > crit0·(1 + 10^-4) + 10^-12`,
  with weights floored at `10^-15`.

**o2. Multiplicity.**
The Section 8.2 split at 50% and the many uncorrected Wilcoxon p-values in
Sections 6–8 are exploratory. Saying so once would help, as Section 7.2
already does for the full solves.

**o3. Cross-reference the sibling degeneracy number.**
`scip-rule-fidelity` reports that 73% of sampled MINLPLib corners have
`z_K = 0`. This note reports that the criterion is attained at a zero-cost
ray in 82% of corners. The definitions differ. One sentence would prevent
readers from treating these as conflicting.

## Checks run, with outcomes

All commands ran with `OMP_NUM_THREADS=1`, at most 3 concurrent processes,
and under `timeout`.

1. **Patch provenance and build identity**
   (`reviews/r1-code/build_variants.sh`).
   - The tarball sha256 matches Section 10.
   - The patch applies with `patch -p1` to the tarball's
     `nlhdlr_quadratic.c`.
   - The two patch files differ only in header timestamps.
   - Compiling the patched file with build-lapack's flags gives an object
     **byte-identical** to the object in `build-lapack` (00:06 Oct 2, before
     all benchmarks). The same holds for `build-debugsol`.
   - So the binaries used are exactly the archived patch. The source file's
     later mtime (20:25 Oct 2) did not change its content.
2. **Patch review against Sections 2–3** (by reading the code).
   - The λ-restriction formulas (`buildLambdaCoefs`: Cases 1–3, Case 4
     pieces a/b, Case-4a condition) match the definition of `C_λ`. For
     `λ = x̂(s̄)/‖x̂(s̄)‖` the Case-4a condition coefficient equals SCIP's
     `−xextra/‖x̂‖`.
   - SCIP's λ is evaluated first (`crit0`). It is replaced only if
     `critbest > crit0(1 + 10^-4) + 10^-12`.
   - On failure the code falls back to SCIP's λ.
   - The 48-evaluation budget is 1 + 24 grid points + 23 golden-section
     evaluations.
   - Monoidal strengthening and the minimal representation are disabled
     only when λ changed.
   - `lambdaCoefsGood` mirrors SCIP's own (inverted-name) dynamism test:
     with the default `ignorebadrayrestriction = TRUE` it applies the test,
     as SCIP does.
   - With `setrule = 0` and no dump, `selectLambda` is not called, and the
     cut code path is SCIP's. The exceptions are the added clocks and the
     row capture (M1).
3. **S-freeness proof (Section 2).**
   - I checked the argument line by line. Cases 1–3 follow from
     Cauchy–Schwarz.
   - For Case 4, I verified `x̂_last − ŷ_last = √r` and
     `‖x̂‖² − ‖ŷ‖² = q`. I also verified that
     `‖x̂ − θe‖² − ‖ŷ − θe‖² = q − 2θ√r`, the Lagrangian dual
     `min_θ≥0 ‖ŷ − θe_last‖ + θλ_last`, the Slater condition, and the
     exclusion of `λ = −e_last` by the acceptance test.
   - The proof is correct.
   - Numerically (`r1-code/case4_closed_form.py`): the closed form of
     `φ_λ` matches SLSQP maximization over the cap to `1.1·10^-12` (1896
     cases). 20000 random points of `S` with random unit λ: none lies in
     `int C_λ`.
4. **Validation reruns (Section 4).**
   - `check_dump.py` on `ex5_2_5.r1` and `blend029.r2`: JSON output
     identical to the archived `.check.json`.
   - `check_scout_case4.py`: identical output (scout 1460 of 25943
     violations; SCIP formula 0).
   - `search_optimality.py` on `st_e31.r1` and `blend029.r1`: SUMMARY lines
     identical to the archived outputs (blend029: 39 of 39 within `10^-4`,
     mean C ratio 0.99999838, SCIP 0.852).
   - From `checks_summary.md`:
     - z_K checked on 408 corners, 9 spurious, 399 valid ✓.
     - 21 overshoots ✓.
     - 8 of 83057 final-cut rays shorter than 0.9 times the exact step ✓.
     - Decomposition error at most `9·10^-12` ✓.
   - Offline table (Section 4.4) matches the SUMMARY lines of both
     `offline_constlambda` logs ✓.
5. **Test-set construction** (`r1-code/check_selection.py`, own parser).
   - 489 screening logs; 368 with a generated cut; 347 with `RootAppl > 0`,
     equal to `testset_root.txt` ✓.
   - Pool of 260; `random.Random(20261001).sample` reproduces
     `testset_full.txt` ✓.
   - The 305 instances for the seed runs are the 302 complete instances with
     a reference plus 3 complete instances without one. This is consistent.
6. **Root tables recomputed** (`r1-code/recompute.py`, output
   `r1-logs/recompute.md`; own parser, no stream imports).
   - 4869 runs, all return code 0, no ERROR line.
   - No objective-sense mismatch between log and `instancedata.csv`.
   - The first LP value is identical across settings on every compared
     instance, so the RGC denominator is common.
   - All RGC values lie in [0, 1].
   - Every number in the Section 6 tables (n, mean and median RGC, CPU sgm,
     cut counts, search and intercut times, all paired rows, Wilcoxon p) and
     in the seed-noise table matches. The Wilcoxon p-values are insensitive
     to the zero-handling variant.
   - The only validity flag is `tricp` (`eff`, seed 2), as stated.
   - Heavy tail: in seed 0, the top 25 instances give 66% of the `scip`
     versus `off` RGC gain (median +0.0023). This is consistent with the
     note's "minority" statement.
   - Monoidal sensitivity (`r1-code/monoidal_sensitivity.py`): excluding
     the 17 instances where SCIP used monoidal strengthening leaves corner
     versus scip at −0.008 / −0.008 / −0.010 (p 0.041 / 0.041 / 0.008) and
     eff versus scip unchanged. The disabled strengthening does not explain
     rule 1's loss.
7. **Section 8.2 recomputed** (`r1-code/degeneracy_split.py`).
   - The rows for 97 / 151 / 248 instances, the Spearman values (+0.145,
     +0.031, −0.509) and the corner shares (81.6%, 9.2%, medians 0.11 and
     0.72) all match.
8. **Full-solve tables recomputed** (`recompute.py`).
   - 480 runs; return codes 479 × 0 and 1 × 255; 302 optimal, 177 time
     limit, 1 failure.
   - All per-seed and pooled solved counts, CPU and node sgms, all-solved
     subsets, the "exclude `ex5_4_2` s1" and "exclude `kall`" variants, and
     all paired ratios and instance-averaged Wilcoxon p-values match
     Sections 7.1–7.2.
   - Solved-set differences:
     - `corner`/`eff` versus `off`: only `ex5_4_2` s1 ✓.
     - `scip` versus searches: `scip` alone solves `tln7` s1; the searches
       alone solve `blend852` s1 and s2 ✓.
   - Solved runs above 150 s: blend852 off (219 s, 257 s), blend852 corner
     s2 (177 s), tln7 scip s1 (283 s). These are sensitive to the limit and
     to load.
   - The 255 failure is SCIP's own. The **unpatched** binary reproduces
     `ex5_4_2.off.s1` exactly: "(node 3643) unresolved numerical troubles
     in LP 3040", return code 255. Counting it as unsolved at 300 s is the
     standard choice. The statement that the searches' extra pair over `off`
     is exactly this failure is correct.
9. **Fairness of `setrule = 0`**
   (`r1-code/fairness_check.sh`, `r1-logs/fairness/SUMMARY.txt`).
   - 13 root-only and 4 runs to 2000 nodes, patched versus unpatched.
   - The `tln7` divergence was confirmed by repeating both runs and by a
     build without `SCIPcaptureRow` (M1). The no-capture run used the same
     command as `fairness_check.sh`, with `/tmp/r1chk/scip-nocapture`.
10. **Debug-solution audit**
    (`r1-code/recheck_glmp_rows.py`, `r1-code/check_debugsol_bounds.py`).
    - 300 solver logs plus 6 runner logs; 170 optimal / 129 time limit /
      1 failure.
    - 45 runs with ERROR; 215 unknown-variable warnings; 114699
      objective-bound warnings in 25 runs.
    - 73 intersection-row and 9 `overestimate_pow` messages, all on
      `st_glmp_fp2`.
    - 0 of 299 final and 0 of 286 root dual bounds exclude the reference;
      for the symmetry-enabled attempt, 0 of 42 and 0 of 40.
    - The three `kall_congruentcircles_c52` optimum discrepancies are as
      stated.
    - Symmetry-enabled attempt: 43 logs (22 corner, 21 eff); `kall` corner
      has no return-code footer; `ex5_4_2.eff` has return code 255; 16 + 7
      other-row messages ✓.
    - Row re-evaluation and local-row analysis: see m1.
11. **`kall_congruentcircles_c52` primal check:** see m2.
12. **Search statistics** (`r1-code/selstats.py`): see m6.
13. **Sibling consistency.**
    - `multiround` recommends keeping SCIP's set and finds per-term
      efficacy choice "never measurably worse, no demonstrated benefit".
      This note's eff ≈ scip and corner < scip at the root agree with that.
    - `scip-rule-fidelity` reports an inverted `ignorebadrayrestriction`
      semantics, mostly degenerate MINLPLib corners, and cites this note's
      Section 4.3. All of this is consistent.
    - No contradiction found. See o3 for a wording aid.
14. **Summary versus body and status labels.**
    - Summary numbers match the body.
    - The labels "proved" (Section 2), "numerical evidence" (Sections 4, 6,
      7, 8) and "incomplete validity check" (Section 9) are appropriate.
    - The stated limits are present and accurate: missing ordinary seed-0
      full solves (confirmed: `logs/full` has only s1 and s2), load
      12–200, CPU-time distortion and no quiet-machine rerun.
    - Exception: the "unchanged code path" claim (M1).
    - The "has not been reviewed" statements will need updating. The
      "Nothing here has been committed" statement was ignored as
      instructed.

All review binaries and temporary sources are under `/tmp/r1chk` and are
not part of the stream. No background process remains.
