# Review r2 of `scip-rule-fidelity/note.md`

Reviewer: independent research agent (did not write the material), confirming
review round 2, 2026-10-03. Code: [`r2-code/`](r2-code/). Logs:
[`r2-logs/`](r2-logs/). The note, the stream's code and logs, and the r1
artifacts were not edited. Nothing was committed and the git state was not
changed.

## Verdict

**Minor fixes.** The round-1 issues are all addressed, and every changed
number reproduces from the raw data:

- M1: the 91% statement is gone as evidence. The new dynamism table
  reproduces exactly from the raw dumps with independent code.
- m1: the Gurobi wording is now correct, and the conditional bracket claims
  and the maximum `0.09847245955656159` reproduce.
- m5: the explanation of the four `waterund32` records is genuine, not a
  rationalisation. An exact check confirms it, and it also confirms that
  no other zero-rate ray in the 371 records reaches `S`.

One new minor issue remains (N1). The revised note says the causes of most
dynamism aborts "remain undetermined". However, the saved dumps already show
the immediate cause for most first-piece aborts:

- Only `A` is below the threshold, and `A` is not a cancellation result.
- The test depends on the length of the ray, which does not affect the cut.

Open question 1 omits this mechanism. The other new items are optional or
nits.

## Status of round-1 items

| # | Status | Evidence |
|---|---|---|
| M1 | Resolved; see N1 for a remaining gap | 91.1% now described only as the split between pieces (Section 6, Summary item 4). The table reproduces exactly from raw dumps with independent code: 1,799 first-piece aborts, quantiles `2.98645758e-34 / 4.61594214e-18 / 4.55819518e-16`, 493 (27.4%) below `1e-25`; 175 on 4b, `1.08080140e-20 / 4.32021883e-17 / 7.96814357e-16`, 4 (2.3%) (`r2-logs/dyn_summary.log`). All 1,974 sampled records match the analysis files in `lp`, `cons` and failing ray. My own recomputation of `A, B, C` from the dumped eigen data agrees with SCIP's dumped values to `4.1e-16` relative. 36/138 and the median `7.59782506e-18` agree with `logs/dynamism_after_r1.log`. The wording claims no more than the data show. Open question 1 and Solver relevance were rewritten as asked. |
| m1 | Resolved | Statuses 175/47/10 confirmed. Table kinds: 602 exact, 233 kkt3, 176 Gurobi-closed, 46 bracket, 10 upper with "infeasible" report. The 46 brackets have a largest upper ratio estimate of `0.09847245955656159`. Moving them to their upper estimates shifts the mean by `0.000580` and leaves the quartiles unchanged. All 10 "infeasible" records are in the table with ratio `≤ 1e-4`; 10/1,067 = 0.94 pp (`r2-logs/check_numbers.log`). `waterund25` k=410: my own exact rational bisection on the dumped data, with the exact constant term, gives a boundary cost of `0.15618498137992642`. The ray's rate (`3.57e-6`) is above the floor, so this value does not depend on the floor convention. "Feasible upper bound, not global optimality" is the correct description. |
| m2 | Resolved | 16 optimal / 4 time limits; median `6.780e-10`, max `8.906e-05` (`pooling_digabel18` k=351, `kkt3`, Gurobi lower). The three time-limited incumbents agree to `≤ 6.7e-8`, and `blend029` k=15 has none. |
| m3 | Resolved | `2.842e-14` (scaled) and `1.436e-13` (relative), both at `ex7_3_3` k=0, `κ = 0.198`. Generator records all have `κ = 0`, so the maximum over the 7,945 records is unchanged. |
| m4 | Resolved | 4,785 records, 207 without rays: first sample 10 `lukvle10` + 49 `space25a`; second sample 148 `space25a`. |
| m5 | Resolved; see N2 (optional) | Selection reproduced independently (my reimplementation of the table definition): 1,067 table records, 371 below 0.5. The four `waterund32` records are genuine. See "Check of the four `waterund32` records" below. |
| m6 | Resolved | Summary item 4, Section 6 heading and Open question 4 now say "checkable" and "lower bounds". |
| m7 | Resolved | Both bisection maxima are now marked "in this sample". The sibling links `#43-scips-own-root-finder-can-halve-a-step-observation` and `#81-scips-root-corners-are-mostly-dual-degenerate` match headings in `scip-set-selection/note.md`. |
| m8 | Resolved | 34 time limits / 30 optimal confirmed. The dumps are 2.20·10^9 bytes (2.05 GiB), so "2.1 GB" is acceptable. |
| m9 | Resolved | `ex1264`: before the restart, 4 expressions, max LP 77, counters up to 18. At LP 113, `e2` and `e5` are new expression addresses with counter 0. `ex1264` and `squfl010-040persp` restarted. No "lifetime" or "never reset" wording is left. |
| o1–o3 | Addressed | "small in the median"; degeneracy sentence with the sibling §8.1 link; Open question 6. |
| Header | Accurate | `git log` shows the note in commit `d91d8d98b`. The revision exists only as working-tree changes. |

The author's replay of `explain_mismatch.py` timed out. The note says so and
does not claim a rerun. The r1 rerun of that script was byte-identical to
`logs/explain_mismatch.log`, and the figures did not change, so no fresh run
is needed.

### Check of the four `waterund32` records (m5, focus b)

`r2-code/zero_rate_exact.py` imports no stream code. For each of the 371
records it does the following in exact rational arithmetic on the dumped
floats:

- Forms `q(s̄ + t p) = q0 + L t + M t²` for every non-fixed ray with rate at
  most `1e-9 max w`.
- Tests whether `S` is reached for some `t > 0`.

Results (`r2-logs/zero_rate_exact.log`):

- Exactly four records have a zero-rate ray that reaches `S`: `waterund32`
  k=651, 715, 1138 and 1292. My `L` values equal the note's
  (`−1.1606e-14`, `−7.7376e-15`, `−2.5792e-14`, `−1.1606e-14`), with `M = 0`.
  The steps `q0/|L|` are 2.10–6.85·10^18, as stated.
- In the other 367 records, no single zero-rate ray reaches `S`, even in
  exact arithmetic. So the "183 with no intersection" statement also holds
  exactly for single rays, not only in the floating-point full-space check.
  Among the 258 generated-cut records, 114 have a zero-rate determining ray,
  and none of those rays reaches `S`.
- Source of the drift: in each case the ray moves `t_x612` down from its
  upper bound 1425. `q` contains the term `t_x612 · t_x245` (or `t_x261`,
  `t_x252`) with coefficient 1. So `L` equals minus the LP value of the
  partner: `1.16e-14`, `7.7e-15` or `2.6e-14`. It is a single term, with no
  cancellation: `|L|` equals the sum of the absolute values of its terms.
- In the reduced space, the coordinate `Vrᵀ s̄` has rounding error of about
  `u·10^3 ≈ 10^-13`. This exceeds the drift, so the spectral reduction
  cannot see it.

The note's explanation is therefore correct: the drift exists in the dumped
data and lies below the reduction's rounding error. The four records are
failed attempts, so `z_C` comes from the model. N2 suggests a wording
refinement.

## New issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| N1 | minor | Summary item 4 ("the causes of most aborts remain undetermined"); Section 6, dynamism paragraph ("the cause and conditioning of those cuts remain undetermined"); Open question 1 | The dumps already show the immediate cause for most first-piece aborts. The note's diagnostic tests only one mechanism: the ray has no negative-eigenspace component, so `A` and `B` are both noise. Data (`r2-logs/dyn_summary.log`): (1) In 1,270 of 1,799 sampled first-piece aborts (70.6%), only `A` is below `10^-15·max`. Over all 34,834 first-piece aborts in the dumps, the share is 80.6%. (2) In 1,209 of those 1,270, `A = Σ|θ_i|(v_iᵀr)²` is not a rounded zero of its own computation: it exceeds `64u` times its absolute evaluation (median ratio about `1/u`), so `v_iᵀr` shows no cancellation. (3) Replacing `r` by `λr` maps `(A, B, C)` to `(λ²A, λB, C)` and leaves the cut unchanged. SCIP does not normalise the rays; it only drops entries `≤ 1e-9`, and a TODO at `nlhdlr_quadratic.c:819` suggests scaling them. With a rescaled ray, 1,728/1,799 sampled (96.1%) and 31,926/34,834 of all first-piece aborts (91.7%) would pass the test; the median best ratio is about 0.5. So most aborts come from a short negative-eigenspace component of the ray relative to the LP point, not from rounded zeros or ill-conditioned restrictions. Still undetermined: whether those short components are themselves LP noise (the median largest quadratic-variable ray entry is `1.9e-5` in the sample and `1e-6` in the population), and whether the cuts would be safe. A forward-error test over all 1,799 finds the tiny entry within `64u` of its absolute evaluation in 520 (28.9%). Measured on all 1,799, the r1/author-style test gives 359 (20.0%), so 36/138 is not far off. | State the tiny-entry pattern and the scale dependence of the test. Reword "causes … remain undetermined" to say what remains open: whether the short ray components are noise, and whether the cuts are safe. Add ray scaling to Open question 1. Optionally replace the 138-record diagnostic by the full 1,799-record sample. |
| N2 | optional | Section 5.2 (four `waterund32` records); revision table row m5 ("real tiny drift"); Summary item 3 ("four have tiny drift lost in the reduced-space test") | The drift is the LP value, about `10^-14`, of the bilinear partner of `t_x612`. Such a value is at LP-tolerance level and plausibly a rounded zero. In the exact dumped-data model these four corners are degenerate (`z_K = 0` with exact zero rates). In the true LP corner the outcome is undetermined. The Summary's phrasing does not say that these four rays do reach `S` in the dumped data. | Say where the drift comes from. Replace "real" with "present in the dumped LP values". Say that these rays reach `S` in the dumped data. Optionally state that an exact single-ray check finds no intersection on any zero-rate ray of the other 367 records. |
| N3 | nit | Section 6, diagnostic description ("in Case 4, the ray's linear component") | `dynamism_after_r1.py` tests the whole `w(ray)`: the zero-eigenvalue terms `vb_i·(v_iᵀr)`, the linear terms and the auxiliary-variable term. | Say "`w(ray)`". |
| N4 | nit | Summary item 3 ("exact certificates are identified in Sections 5 and 7.1"); Section 5 ("at most ±0.9 percentage points") | Section 5 contains one exact feasible-point check, an upper bound for one record, not a `z_K` certificate. The 10 "infeasible" records use the two-ray value, which is an upper bound on `z_K`. Their ratios are therefore lower bounds and can only move up: the fractions below 0.5 and 0.9 can only fall, by at most 0.94 pp. | Say "exact checks". Replace "±" with a one-sided bound. |

## Checks run

All checks were targeted and local. No project-wide verification, CI, SCIP
build, SCIP run or Gurobi run. `OMP_NUM_THREADS=1`, at most 4 worker
processes, `timeout` on every run. No stream code was imported. The stream's
analysis files and `logs/gurobi_zk*.jsonl` were read as data. No background
process is left.

| Command (from `reviews/r2-code/`, `python3 -B`) | Outcome |
|---|---|
| `dyn_recompute.py ../r2-logs/dyn_recompute.jsonl` (4 processes, 45 s; output then gzipped) | 38,105 dynamism aborts in all MINLPLib dumps; every one has an `nbadray` increment and a ratio `≤ 1e-15`. 1,974 sampled aborts identified, all matching the analysis files. `A, B, C` recomputed in SCIP's order agree with the dump to `4.1e-16`. |
| `dyn_summary.py ../r2-logs/dyn_recompute.jsonl.gz` → `r2-logs/dyn_summary.log` | M1 table reproduced exactly. Population figures, tiny-entry patterns, forward-error test and ray-rescaling test as in N1. The rerun on the gzipped file is byte-identical. |
| `zero_rate_exact.py` → `r2-logs/zero_rate_exact.log`, `.jsonl` | 1,067 / 371 selection reproduced. Exact single-ray intersections on zero-rate rays occur only in the four `waterund32` records; values match the note. |
| `check_numbers.py` → `r2-logs/check_numbers.log` | m1–m4, m8 and m9 numbers confirmed, including an independent exact root for `waterund25` k=410. |
| Inline inspection of the four `waterund32` rays (exact `Fraction` arithmetic) and of eight tiny-`A` aborts (dumped values) | Drift equals the partner LP value; tiny-`A` aborts have quadratic-variable ray entries of order `1e-9` to `1e-6` and well-balanced `(A, B, C)` after rescaling. |
| Reading: `git diff` of `note.md` and code; `check_revision_r1.py`; the new logs; `nlhdlr_quadratic.c` lines 1230–1720, 2043–2110, 2590–2665, 805–835 | No other new errors found. Summary, Section 5, Section 6, Limits and Open questions are consistent with the body. Generator mechanism counts (58/99, 120/167) match the after-r1 logs. |
