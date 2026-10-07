# Review round 2: `three-var-completeness/note.md`

Reviewer: independent research agent (wrote neither the note nor the round-1
review). Date: 2026-10-03. "Reviewed" here means checked by another research
agent, not journal peer review. The note and the stream's code were not
edited, and no git state was changed. Reviewer code is in `reviews/r2-code/`,
logs in `reviews/r2-logs/`. The reviewer code does not import the stream's
code; `r2_reporting.py` and `r2_rounded_theta.py` only read the stream's logs.

## Verdict

**Minor fixes.** All 12 round-1 issues are fixed correctly. The new
zero-parameter cases of Proposition 2.10 are right: my own exact computation
reproduces every minor the note states, and the one-sided tangency argument
covers the contacts that reach a vertex. I found no error in a proved
statement and no new error in the revised text. One new minor issue remains.
It predates the revision and sits in a paragraph that the revision edited: the
sentence about exact contacts at the searched positions rests on 24 of the
265 post-processed configurations, because the other 241 solves returned no
value. Two small reporting updates are also suggested (N2, N3).

## Status of the round-1 issues

| # | r1 issue | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Zero parameters in Prop. 2.10 | Fixed | `r2_zero_params.py`: in all eight zero-parameter cases (S2 and S4 with `d1 = 0`, `d2 = 0`, `d1 = d2 = 0`; S3 and S5 with `h = d1 = 0`), `q` is in the kernel, and the 9 x 9 minor without the `z` column is `2k/d3`, `2k/(d2+k)`, `2k/(d1+k)`, `2` (S2/S4) and `-2k/d3`, `-2k/(d2+k)` (S3/S5). These are the note's values, with the same signs. Exact rank is 9 at 25 random rational points in each case. Each contact lies on the stated vertex or edge. The one-sided argument is correct: at a vertex zero, the restriction of each summand to the tangent edge is nonnegative and zero at the vertex, so its one-sided derivative is `>= 0`; the derivatives sum to zero, so both vanish. These are the only zero-parameter cases: S1 has `h > 0`, and `d1 < d2` forces `d2 > 0` on S3/S5. |
| 2 | Boundary-example range; `d_i = 0` exception | Fixed | `r2_reporting.py`: 34 stored examples, 30 with a vertex contact; their `R_D` values run from `-1.73883e-3` to `-9.36692e-6`, and every stored square coefficient is `>= 4.6e-5`. The `d_i = 0` exception follows from Corollary 2.4 (ii), because the square coefficients are `d_i^2`. |
| 3 | Solver relevance | Fixed | The claim is now limited to three-variable box QPs, and the dual-aggregate caveat is stated. "Halves the strict sign patterns" is right: 4 of the 8 strict patterns have positive product. |
| 4 | "outside the hull" | Fixed | The Summary says "outside `H3+`". |
| 5 | Fit residuals are squared | Fixed | `fit_family.py` returns scipy's `least_squares` cost, `0.5 * sum((v/|v|_2 - p/|p|_2)^2)`, so the distance is `sqrt(2c)`. `fit_all`, `fit_more` and `fit_stratum_examples` all call this function. The 8 retest costs `3.2e-7` to `3.73e-3` give distances `8.0e-4` to `0.0864`; "about `8e-4` to `0.09`" is correct. The caveat that a local fit does not bound the distance to the whole family is appropriate. |
| 6 | `-7.0e-9` ray not re-solved | Fixed | The Summary, Sec. 2.8 and Sec. 7 say this. The five re-solved rays and their ranges (stored `-1.37e-10` to `1.04e-11`; re-solved `-4.91e-8` to `1.65e-10`, with sign changes) match `logs/check_min_rR_dense.txt`. |
| 7 | `project_probe` description | Fixed | The rows are split. Logged `sep(y0)` values are `3.5e-9` to `1.5e-8` (`l1`) and `-7.9e-3` to `-1.3e-3` (`l2`). |
| 8 | Untested kernels | Fixed | The negative-square case has been added. |
| 9 | 265 vs 264 | Fixed (the explanation could be more complete; see N2) | `r2_reporting.py`: 312 retest records; 265 with search cost `<= 1e-6`; 264 with retest cost `< 1e-6`; 264 tested against `R` (min `6.88e-9`, 8 with `R_D` value `< -1e-6`). The one failure is the configuration the note names, with costs `1.48e-9` and `2.535309231191649e-6`. |
| 10 | Nishijima attribution | Fixed | `sources/nishijima-2602.23725.txt`, lines 391-408. Lemma 2.4 (i) covers intersections, (ii) inverse images under linear maps, and (iii) dual cones. The paper cites Netzer-Plaumann, "Spectrahedral shadows", in *Geometry of LMIs* (Birkhauser 2023), Theorem 3.5 (ref. [26]). Images, Minkowski sums (images of products) and exposed faces (intersection with a hyperplane, then (i)) are now justified separately and correctly. |
| 11 | "at most one coordinate" | Fixed | `r2_reporting.py` enumerates all 8 sign patterns. The 4 with positive product need 0 or 1 complementation; the 4 with negative product can never become all positive. The new proof sentence is correct: two negative edges of a triangle share a vertex, and complementing it flips exactly those two. |
| 12 | Draft counts | Fixed | Labelled as an unverifiable reconstruction. |

## New issues

| # | Severity | Location | Description | Required change |
| --- | --- | --- | --- | --- |
| N1 | Minor (predates the revision) | Sec. 2.7, second bullet ("With the contact conditions imposed exactly at the positions found, only two configurations outside the six admit `p(0) > 1e-4`"); Sec. 7 row `postprocess_positions.py` | In `logs/postprocess_positions.jsonl`, the exact-contact maximization of `p(0)` returned no value (`maxp0 = null`) for 241 of the 265 configurations. Only 24 have a value: 19 at or below `1e-4` and 5 above. The main log `postprocess_positions.txt` contains 224 Clarabel panic messages, and 229 of its 241 records have no value, so most of these are solver failures, not infeasibility. The sentence therefore covers only the 24 solved cases. The exact contacts were also imposed at positions rounded to 4 decimals (see N2). The main conclusion does not depend on this sentence: it rests on `positions_retest.py`, which tests the valid quadratics directly (264 tested, none missing). | State that 241 of the 265 exact-contact solves returned no value (mostly Clarabel panics), so the "only two" statement covers the 24 configurations with a solved value. Alternatively, rerun those solves at the full-precision positions in `blocking_positions_*.json`. |
| N2 | Cosmetic | Sec. 2.7 (265/264 reconciliation) | The note does not give the cause of the cost increase. `blocking_positions.py` prints `theta` rounded to 4 decimals, and both `positions_retest.py` and `postprocess_positions.py` read these rounded values from the `.txt` logs; the `.json` logs keep full precision. My independent re-solve (`r2_rounded_theta.py`) of the excluded configuration gives cost `9.2e-10` at the full-precision `theta` and `2.535e-6` at the rounded `theta`, which is exactly the retest value. Five other configurations also have higher costs at the rounded positions (up to `8.9e-8`) but stay under the cutoff. | Add one sentence: the retest used the 4-decimal positions from the text logs, and the excluded configuration passes at full precision (`9.2e-10`). Optionally, test that configuration's quadratic as well. |
| N3 | Cosmetic | Sec. 7, 2026-10-03 table, row `check_boundary_rank_symbolic.py`; Process hygiene | The rerun of the S1 script did not fail; it needs a little more than 180 s. With `timeout 1200` it finished in 3 min 15 s (exit 0) and printed the minors stated in Proposition 2.10 (`r2-logs/rerun_check_boundary_rank_symbolic.txt`). | Optional: record that the script completes in about 195 s with the stated minors. |
| N4 | Cosmetic, optional | Sec. 2.6, paragraph after the strata table | In the zero-parameter cases the zero set contains a whole edge: for example, `q(x,0,0) = d1^2 x^2` vanishes identically when `d1 = 0` on S2/S4 or when `h = d1 = 0` on S3/S5. The proof does not need isolated zeros, so this is not an error. However, the table lists only point contacts, and Sec. 2.8 says the enumeration "misses zero segments". | Optional: note that these members have a zero edge, so they lie outside the point-contact enumeration (and inside `cl(D3)`, as already stated). |

## Review of the diff

I read `git diff -- research-20261001/three-var-completeness/note.md` (base:
commit `d91d8d98b`) and the diff of `code/check_family_strata_symbolic.py`.
Besides the r1 fixes, the revision adds a status paragraph, the
Conjecture 2.11 numbering note, the definition of fit cost, the revision table,
and new Sec. 7 rows. The numbering note is correct: in the committed version
the conjecture was Conjecture 2.9, and `three-var-computation/note.md` uses
2.11 and records the old 2.9. The status paragraph's statement that stream
material was committed outside this program is accurate: `git log` lists
`c3514f03e` and `d91d8d98b` for `note.md`. In the script, the symbol
assumptions changed to `h` real and `d1, d2 >= 0`; the new cases do not divide
by `d1`; and the expected-minor assertion compares exact expressions. The
generic S2-S5 minors are unchanged. I found no new mathematical or numerical
error. The sampler totals are unchanged (36,398 rays, 1,371 outside
`cl(D3)`, ten samplers).

Summary and Limits are consistent with the body. The Summary's "for all
parameters in each stratum" now has the support of the zero-parameter
checks. It makes no claim that boundary rays lie outside `cl(D3)`, so the
`d_i = 0` exception does not affect it. Limits still name floating-point SDPs,
the BNW dependence, point zeros only, and the BKT dependence.

## Checks run

All runs used `OMP_NUM_THREADS=1`, an explicit `timeout`, and at most two
processes at a time. They were run from `three-var-completeness/reviews/`,
except the stream's S1 script, which was run from `code/` and writes only to
stdout. No process was left running (checked with `pgrep`). No project-wide
checks were run, and CI was not inspected.

| Command | Outcome |
| --- | --- |
| `timeout 1200 python r2-code/r2_zero_params.py` | ALL PASS (25 s). S2-S5 generic and all eight zero-parameter cases: `q` in the kernel; all ten 9 x 9 minors factored; exact rank 9 at 25 rational points per case; contacts on the stated faces; grid minimum of `q` `>= -6e-14` (sanity check). Every minor stated in the note is reproduced. On S2/S4 the minor without the `z^2` column is the constant `-1`, and on S3/S5 it is `(d1-d2)^2/d2^2`. Both are nonzero on the whole range, including the zero-parameter cases. |
| `timeout 580 python r2-code/r2_s1.py` (rows scaled to polynomials) | S1: `q` in the kernel. The minor without row 0 and column 0 is `d2 h^2 (d1-2h)(d2-h)^2 d3^4`; this equals the note's minor times the row scalings `d1 d2^3 d3^6`. Exact rank 9 at 20 generic rational points and at 20 points with `d1 = 2h`. An earlier unscaled version timed out at 900 s (the log was overwritten). |
| `timeout 1200 python check_boundary_rank_symbolic.py` (stream script, unchanged, from `code/`) | exit 0 in 3 min 15 s; same minors as the note and as the r1 rerun. |
| `timeout 120 python r2-code/r2_reporting.py` | Issue 2: 30 boundary examples, range `-1.73883e-3` to `-9.36692e-6`. Issue 5: distances `8.0e-4` to `0.0864`. Issue 9: 265 / 264 / 264, one failure (the named configuration). Post-processing: 241 of 265 without a value, 224 Clarabel panics in the main log (N1). Issue 11: sign-pattern table. |
| `timeout 300 python r2-code/r2_rounded_theta.py` (own inner SDP, cvxpy + Clarabel) | Excluded configuration: `9.2e-10` at the full-precision `theta`, `2.535e-6` at the rounded `theta`. Five other configurations: `4.4e-10`-`3.4e-9` at full precision, up to `8.9e-8` rounded (N2). |
| Read: `sources/nishijima-2602.23725.txt` (Lemma 2.4, ref. [26]); `logs/check_family_strata_symbolic_r1_revision.txt`; `logs/check_review_r1_reporting.txt`; `logs/check_min_rR_dense.txt`; `logs/project_probe_*`; `logs/fit_more.txt`; `code/fit_family.py`, `blocking_positions.py`, `positions_retest.py`, `postprocess_positions.py`, `check_review_r1_reporting.py` | Consistent with the note, except as stated in N1 and N2. The stream's audit script `check_review_r1_reporting.py` checks what it claims to check. |
