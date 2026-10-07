# Third confirmation review: `extension-adaptive.md` after the round-2 fixes

Date: 2026-09-30. Note checked:
[`../theory-decomposition/extension-adaptive.md`](../theory-decomposition/extension-adaptive.md),
as revised after the second confirmation review
[`decomposition-adaptive-confirm-r1.md`](decomposition-adaptive-confirm-r1.md). I also checked
the new script `check_localization.py`, its log, the change to `ls_lib.py`, and the logs the
revision cites in [`../theory-decomposition/adaptive/`](../theory-decomposition/adaptive/). I did
not write the note or any earlier review. I did not edit the note and did not commit anything.
My script and logs are in
[`decomposition-adaptive-confirm-r2-checks/`](decomposition-adaptive-confirm-r2-checks/). All
runs were single-threaded (`OMP_NUM_THREADS=1`, and for the rerun also
`OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`) and are targeted checks of this note only. I ran no
project-wide verification and did not consult CI.

## Verdict: verified

**All four items of the second confirmation review are handled correctly.** I checked each one
from scratch and recomputed every number that changed. N1 is fixed with the suggested
qualifier. Both optional points and the pre-existing Summary imprecision are applied
accurately. The related change to Conjecture A.7 is correct and weakens the conjecture; it does
not strengthen it. No item was left unapplied. I found no statement that became stronger than
its support.

Two optional wording points remain (Section 2). Neither affects a conclusion.

| # | Item of the second confirmation review | Fix in the note | Verdict |
|---|---|---|---|
| N1 | "at most `6 s`" at `c = 0` failed at level 4 | Summary and status table: "in the exact-slope runs with `c = 0`, at most `6 s` from level 5 on (`8 s` at level 4 for `n >= 16`)"; A.5 and C.1 give the level ranges, the learned-slope values and the stopping case; new `check_localization.py` | **correct** |
| — | related: Conjecture A.7 without a live box | the conjecture now requires a live box; clarification paragraph | **correct** |
| 2 | `26 n` (exact slopes) against `45 n` (learned slopes) mixed `c = 0` with random `c` | `26 n` scoped to `c = 0`; random-`c` exact-slope value `27–28 n` added; A.3 and D say `c = 0` | **correct**; one optional wording point (O1) and one optional pointer (O2) |
| 3 | `N_dec/Psi` of order `w^{Theta(w)}` for every `eps <= alpha` | stated in Proposition B.6(a) with proof; Summary, B.1 and status table updated | **correct** |
| 4 | Summary `O`-form of Theorem B.2(b) | `(C max(1, sqrt(alpha d)))^d` with an absolute `C` | **correct** |

## 1. Item-by-item check

### N1: sup-norm localization at `c = 0`

**Logs.** I recomputed `|x^cons - x*|_inf/s_i` with `s_i = 2^{1-i}` from the author's logs
(`indep_r2_checks.py`, part 1).

- *Exact slopes* (`logs/oracle_eps1e-6.log`):
  - Levels 1–3: 0.91, 2.00, 4.00 for every `n`.
  - Level 4: 4.00, 6.00, 8.00, 8.00, 8.00 for `n = 4, 8, 16, 32, 64`. At `n >= 16`, `dxinf` is
    1.00 there, so the consistent point has a coordinate at `±1`.
  - Levels 5 and later: 3.99–4.00, 4.99–5.00, 5.98–6.02 (three times).
- *Learned slopes, `c = 0`* (`logs/scaling_eps1e-4.log`, final pass):
  - Levels 0–1 are below 1.
  - Levels 2–4 equal the exact-slope values (8.00 at level 4 for `n = 16, 32`).
  - From level 5 on the ratios are 2.99–6.02, except 11.98 at the stopping sublevel 11 of
    `n = 4`.

**Full-precision rerun.** I reran `check_localization.py 16 8`. This covers the exact-slope runs
`n = 4, 8, 16` and the learned-slope runs `n = 4, 8`, including the `n = 4` stopping case. It
took under a minute. All 71 output lines equal the corresponding lines of the author's
`logs/check_localization.log`, apart from timings. In particular:

- the ratios are exactly 4, 5, 6 from level 5 on, and 8 at level 4 for `n = 16`;
- the sizes (2,914, 29,228, 153,584; 2,841, 21,473) equal the logs;
- at the stopping sublevel 11 of the learned-slope run at `n = 4`, the ratio is 12.000000 and
  all leaves of the minimizing configuration have level 10.

Because `s_11 = s_10/2`, `12 s_11 = 6 s_10`, as the note says. The code change in `ls_lib.dp`
only records the leaf index per bag along the same back-tracking path that builds the
consistent point, and `run_ls` stores its level (`conf_lev`). It does not change any computed
number.

**Text.** The Summary, the status table, Section A.5 (obstacle 2) and the C.1 bullet state
exactly these values and level ranges. The Summary and status-table wording is the suggested
qualifier. The random-instance range ("`3–7 s` from level 6 on, up to `11 s` at levels 3–5")
is still correct: the recomputed values are 3.11–7.23 from level 6 on, including the stopping
sublevels, and 4.52–11.01 at levels 3–5. Section F item 5 of round 1 has a forward pointer.

**Conjecture A.7.** The clarification is correct.

- Without a live box, "all live boxes have side `<= s`" holds for every `s > 0`, so the old
  statement forced `x^cons = x*`. The logs have `dxinf > 0` at every stopping sublevel.
- With a live box `B`, `l_r <= MM(B) < UBD - eps`. Every box of a minimizing configuration has
  min-marginal at most the configuration value `l_r`, and at least `l_r`, so it is live and has
  side `<= s`.
- The added hypothesis narrows the statement, so the conjecture is weaker than before. The
  parenthesis "as in LS at a sublevel whose stop test fails" was already the intended scope.
- The conjecture still ranges over all certificates (any partition, slopes and incumbent). This
  is much broader than the LS data, but "possibly with an additional hypothesis" already hedges
  it. This is not a new issue.

### Item 2: exact against learned slopes

Recomputed from the logs (part 1–2 of my script):

| Runs | Split per bag per level, maximum over levels |
|---|---|
| `c = 0`, exact slopes, `n = 4..64` | `8.82, 19.11, 25.86, 22.66, 22.32 n` |
| `c = 0`, LS, `n = 4..32` | `10.32, 19.11, 29.31, 22.70 n` (`n = 16` at level 11) |
| random `c`, oracle, `n = 16` | 445.8 and 434.5 at level 5, that is `27.86 n` and `27.16 n` |
| random `c`, LS, `n = 16` | `29.22 n` and `45.00 n`, both at level 11 |

The Summary, the status table (Proposition A.6 row), the paragraph after the proof of
Proposition A.6, Sections A.3 and D and the command table now quote these values with the
right scope. The oracle runs start at `x*`, so they have the exact incumbent; the note says so
for C.2 and in the Summary ("in LS, which also learns its incumbent").

### Item 3: `N_dec/Psi` for every `eps <= alpha`

- *`Psi` for one flat bag.* With `|T| = 1` the only allocation is `eps_1 = eps`. Since
  `E(eta) = [0,1]^d` for every `eta`, the supremum is at `eta = 0`. The covering number of
  `[0,1]^d` by sup-norm cubes of side `r` is exactly `ceil(1/r)^d`: a grid of `ceil(1/r)` points
  per axis with spacing `> r` needs one cube per point. So `Psi = ceil(u)^d` with
  `u = sqrt(alpha/eps)`.
- *Lower bound.* The volume argument for `N_dec >= u^d/V_d` uses no bound on `eps`. Hence
  `N_dec/Psi >= (u/ceil(u))^d/V_d`, which is at least `1/(2^d V_d)` when `u >= 1`, equals `1/V_d`
  for integer `u`, and tends to `1/V_d` as `eps -> 0`. `1/(2^d V_d) = Gamma(d/2+1)/(4 pi)^{d/2}`.
- *Order.* `Gamma(x+1) >= (x/e)^x` gives `1/(2^d V_d) >= (d/(8 pi e))^{d/2}`, and
  `Gamma(x+1) <= x^x` (for `x >= 1`) gives an upper bound `(d/(8 pi))^{d/2}`. So the bound is of
  order `w^{Theta(w)}`.
- *Numbers* (part 3, `lgamma`). Below 1 exactly for `d = 1..62` (0.691 at `d = 62`), 1.098 at
  `d = 63`, `8.78e3` at `d = 80`, `9.28e15` at `d = 120`. The lower bound
  `(d/(8 pi e))^{d/2}` holds for `d = 1..199`.

Proposition B.6(a), its proof, the Summary, Section B.1 and the status table state this
correctly. The "`d >= 63`" threshold is stated as the only caveat, which is accurate.

### Item 4: Summary `O`-form of Theorem B.2(b)

- *Review example.* `alpha = 1`, `eps = 1/2`: `4/theta = 64`, fat base 32 and
  `sqrt(alpha d/eps) = 45.25` at `d = 1024`; 128, 64 and 90.51 at `d = 4096`. Confirmed.
- *Derivation in Section F.* `ceil(v) <= v + 1 <= sqrt(2) v` for `v >= 1/(sqrt(2) - 1) = 2.414`,
  and `ceil(v) <= 3` otherwise. `4/theta < max(8, 4 sqrt(alpha d)) <= 8 max(1, sqrt(alpha d))`.
  `J + 1 <= (1/2) log2(K d/(2 eps)) + 2` holds for `alpha <= 1` and every `eps <= 1` (the proof in
  Proposition B.6(b) uses `eps <= 1/2` only in the case `J = 0`, where `L = 1` and the bound
  holds anyway). The factor `log d` is absorbed into `C^d` because `log2(K/eps) >= 1`. The
  remaining `3K` leaves and cells are `O(K log(K/eps))`. So the corrected form is right, with an
  absolute `C`.
- *Scan* (part 4, my own code). The scan covers 22,695 cases: a grid plus 20,000 random draws,
  with `alpha` from `1e-7` to 1, `eps` from `1e-10` to 1, `K` up to `10^6` and `d` up to 20,000.
  - With `C = 16`, the bound of Theorem B.2(b) is at most 0.733 times the corrected form.
    The note reports 0.69 on its own 720 cases, which is consistent.
  - The old form with `C = 16` is below the bound in 782 cases.
  - At `alpha = 0.1`, `eps = 1`, `d = 4096` the old form is too small by `2^6806` (`K = 2`) and
    `2^6807` (`K = 1024`). This matches the note's "up to `2^6807`" on its grid.

Theorem B.2 itself, B.2(c) (fixed `d`) and Proposition B.6(b) are unaffected, as the note
says.

### Bookkeeping

- The header now cites the second confirmation review.
- Section F has a round-2 subsection with one entry per item, a "Not changed" line and the
  targeted commands.
- Section E has the three new command rows, lists `check_localization.py` and records the
  `ls_lib` change.
- Forward pointers were added to round-1 items 2 and 5.
- The last sentence of round-1 item 5 ("state the `w^{Theta(w)}` loss of `Psi` as
  `eps -> 0`") is superseded by round-2 item 3 without a pointer. This is harmless in a
  revision log.

## 2. Optional points

- **O1. "`29 n` with learned slopes (`c = 0`)".** The Summary ("With learned slopes it reaches
  `29 n` at `n = 16`"), the status table, the paragraph after Proposition A.6 and round-2
  item 2 describe the `c = 0` run of `logs/scaling_eps1e-4.log` by its slopes only. In the
  same sentences, the random-`c` runs are described as "LS, which also learns its incumbent".
  - The `c = 0` run is also LS with restarts.
  - At the split levels of its final pass the incumbent is `2.7e-5` to `5.8e-5` above
    `f* = 0`, that is `0.27–0.58 eps`.
  - It uses `eps = 1e-4`, while the exact-slope runs use `1e-6`.

  Section C.2 shows that a learned incumbent alone costs 2–16% on the random instances. The
  wording therefore suggests that the step from `25.9 n` to `29 n` comes from the slopes,
  which is not established. Suggested wording: "In LS (learned slopes and incumbent) it
  reaches `29 n` at `n = 16`". No number changes.
- **O2. Where the `27–28 n` value is stated.** The Summary cites "Sections C.1, C.2" for the
  random-`c` exact-slope value `27–28 n`, but C.2 gives only the oracle sizes, not their split
  counts. The value appears in A.4, the status table, Section E and Section F. One clause in
  the last bullet of C.2 would make the citation accurate: "the oracle pass peaks at `27.9 n`
  and `27.2 n` at level 5".

## 3. Commands run

From `theory-decomposition/adaptive/` (rerun of the author's new script; log copied to
`decomposition-adaptive-confirm-r2-checks/logs/`):

| Command | Result |
|---|---|
| `python3 check_localization.py 16 8` | all 71 lines equal the corresponding lines of `logs/check_localization.log` (timings aside); under a minute |

From `reviews/decomposition-adaptive-confirm-r2-checks/`:

| Command | Log | Result |
|---|---|---|
| `python3 indep_r2_checks.py` | `logs/indep_r2_checks.log` | Part 1–2: localization ratios by level and split maxima from the four logs (N1, item 2). Part 3: `Gamma(d/2+1)/(4 pi)^{d/2}` below 1 exactly for `d <= 62`; `8.78e3` at `d = 80`, `9.28e15` at `d = 120` (item 3). Part 4: Theorem B.2(b) bound against the old and corrected Summary forms in 22,695 cases (item 4) |

Before writing the script I ran the same computations inline once, with the same results. The
script does not import the author's code. Total CPU time was under two minutes,
single-threaded.
