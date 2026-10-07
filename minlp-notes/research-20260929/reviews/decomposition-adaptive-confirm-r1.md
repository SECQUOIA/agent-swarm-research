# Second confirmation review: `extension-adaptive.md` after the round-1 fixes

Date: 2026-09-30. Note checked:
[`../theory-decomposition/extension-adaptive.md`](../theory-decomposition/extension-adaptive.md),
as revised after the confirmation review
[`ext-decomposition-adaptive-confirm.md`](ext-decomposition-adaptive-confirm.md). I also
checked the scripts and logs it cites in
[`../theory-decomposition/adaptive/`](../theory-decomposition/adaptive/). I did not write
the note or either earlier review. I did not edit the note and did not commit anything. My
script and logs are in
[`decomposition-adaptive-confirm-r1-checks/`](decomposition-adaptive-confirm-r1-checks/).
All runs were single-threaded (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`)
and are targeted checks of this note only. I ran no project-wide verification and did
not consult CI.

## Verdict: fixes needed (minor)

**All six items of the confirmation review are handled correctly.** I checked each one
from scratch and recomputed every number that changed. The two errors (R1, R2) are
fixed, and the four optional points are applied accurately. The one item not applied
(the pointer to `../dp_certificate.py` of [D]) is a justified refusal.

**One new statement is stronger than the data.** The Summary and the status table now
say that, at `c = 0`, the consistent point locates `x*` in sup norm "to at most `6 s`".
The earlier wording was "about `6 s`". The note's own exact-slope log gives `8 s` at
level 4 for `n = 16, 32, 64` (Section 2, item N1). This is a one-line fix and changes no
conclusion.

Two further points are optional (Section 3). I also note one pre-existing imprecision in
the Summary that no earlier review raised (Section 4).

| # | Item of the confirmation review | Fix in the note | Verdict |
|---|---|---|---|
| R1 | shell level count in Theorem B.2(b) and Proposition B.6(b) | `J + 1` with `J = max(0, ceil(log2(1/h_0)))`; bounds on `L` proved; central cube clipped; scan extended | **correct** |
| R2 | "at most about `22 n`" | "at most about `26 n` for `n <= 64` (`22 n` at `n = 32, 64`)", effective `rho` at most about `2.5 sqrt(n)`, learned-slope maxima added | **correct**; one optional nuance (Section 3) |
| 3 | processed-count ratios | both ranges given; the oracle pass has the exact incumbent too | **correct** |
| 4 | RC wording, `n = 4` and `n = 8` | new bullets; new `check_rc_cycle.py` | **correct**; rerun identical |
| 5 | localization range; `N_dec/Psi` | "from level 6 on (up to `11 s` at levels 3–5)"; `eps -> 0` qualifier and fixed-`eps` caveat | random-`c` part **correct**; the `c = 0` part became "at most `6 s`", which is **wrong at level 4** (N1) |
| 6 | boundary-centre nuance | A.5 paragraph states the discontinuity and its harmlessness for `l_r` | **correct** |
| — | not applied: closed test in `../dp_certificate.py` of [D] | recorded as unchecked in Section D | **acceptable** |

## 1. Item-by-item check

### R1: level count in Theorem B.2(b) and Proposition B.6(b)

**Theory.**

- *Lemma 3.1 of [D].* It has `J = max(0, ceil(log2(s0/h)))` and at most
  `(J + 1)(4/theta)^kk` pieces. With `s0 = 1` this is the `J` now used in Theorem B.2(b).
- *Where the old bound fails.*
  - If `h_0 <= 1`, then `J + 1 < log2(1/h_0) + 2`.
  - If `1 < h_0 <= 2`, then `J + 1 = 1 <= log2(1/h_0) + 2`.
  - If `h_0 > 2`, then `log2(1/h_0) + 2 < 1`, and it is negative for `h_0 > 4`.

  So the note's statement "an upper bound on `J + 1` only for `h_0 <= 2`" is exact.
  `h_0 > 2` is equivalent to `alpha^2 K d < eps/2`.
- *The example.* `alpha = 0.1`, `eps = 1/2`, `K = 2`, `d = 1` gives `h_0 = 7.071` and
  `log2(1/h_0) + 2 = -0.822`. Confirmed.
- *Central cube.* For `h_0 > 1` the central cube of the shell partition around the
  corner `0` is clipped to `[0,1]^d`. Its relaxed minimum is
  `-d alpha^2 min(h_0,1)^2/(4(1+alpha)) >= -d alpha^2 h_0^2/(4(1+alpha)) >= -eps/(2K)`.
  So the bound stated in the proof still holds.
- *Proposition B.6(b), the bounds on `L = J + 1`.*
  - If `J >= 1`, then `L < log2(1/h_0) + 2 = (1/2) log2(K d alpha^2/(2 eps)) + 2`, and
    this is at most `(1/2) log2(K d/(2 eps)) + 2` because `alpha <= 1`.
  - If `J = 0`, then `L = 1`. The upper bound holds because `K d/(2 eps) >= 2` when
    `K >= 2`, `d >= 1` and `eps <= 1/2`.

  The three comparisons in the proof are unchanged except for `L`. They remain correct
  with `L = J + 1`.
- *Downstream.* The factor `log(K d/eps)` in the bound becomes `C^{w+1} log(K/eps)`,
  because `log d` is absorbed into `C^{w+1}` and `K/eps >= 4`. Theorem B.2(c) is
  unaffected: `J + 1 ~ (1/2) log2 K` for fixed `d`, `alpha`, `eps`.

**Computation.**

- `check_phi_loss.py` reruns to an identical log. With `L = J + 1` it reports 0 of
  2,880 cases above the displayed constant, and at most 0.307 times the constant. With
  the old `L` it reports 89 cases, the smallest `h_0` among them 4.08, and up to 1.357
  times the constant. The quoted `eps = 1e-6` values (`3.29, 4.65, 5.13, 5.44`, the flat
  bag values, and the lower bounds) are unchanged.
- My own scan (`indep_r1_checks.py`, part 2) does not import the author's script. It
  covers 23,920 cases: a grid plus 20,000 random draws with `alpha` in `[1e-7, 1]`,
  `eps` in `[1e-10, 1/2]`, `K` up to `10^6` and `d` up to 200.
  - With `L = J + 1`, each of the three part-wise comparisons of the proof holds
    separately in every case.
  - The sum is at most 0.286 times the displayed constant.
  - `1 <= L <= (1/2) log2(K d/(2 eps)) + 2` holds in every case.
  - With the old `L`, 182 cases fail, all with `h_0 >= 4.4`, by up to a factor 1.357.
- Part 1 of my script builds the actual shell partitions of `[0,1]^d` around the
  corner with `dp_certificate.shells` (`d = 1, 2, 3`, `theta = 1, 1/2, 1/4`, 13 values
  of `h_0` from `1e-3` to 50).
  - The piece count is at most 0.25 times `(J + 1)(4/theta)^d`.
  - The central piece is `[0, min(h_0,1)]^d`.
  - Every other piece has `w(B) <= theta dist_inf(B, 0)`.
  - The old bound is below the actual count, for example at `h_0 = 4.1, 7.07, 50`.

The status table marks both rows, and Section F item 1 describes the change accurately.

### R2: split leaves per bag per level

**Exact slopes.** Recomputed from `logs/oracle_eps1e-6.log`:

- Per-level maxima: `8.82, 19.11, 25.86, 22.66, 22.32 n`, at levels 4, 5, 5, 6, 6.
- Plateau: `21.0–21.5 n` at `n = 16` and `21.1–22.0 n` at `n = 32` (levels 7–11), and
  `19.8–20.3 n` at `n = 64` (levels 8–12).
- Effective `rho = sqrt(max)/2`: `1.48, 2.19, 2.54, 2.38, 2.36` times `sqrt(n)`.

"At most about `26 n` for `n <= 64` (`22 n` at `n = 32, 64`)" and "at most about
`2.5 sqrt(n)`" are right. The Summary, the status table, A.3, A.4, C.1, D and the command
table all use the new wording. No stale "at most about `22 n`" remains outside the
revision history of Section F, which carries a forward pointer.

**Learned slopes.**

- `logs/scaling_eps1e-4.log` gives `10.32, 19.11, 29.31, 22.70 n`.
- The C.2 LS runs give `19.79, 24.18, 29.22, 45.00 n`. All three `n = 16` LS maxima are
  at level 11.
- C.1's "at levels 4–10 it is `14–26 n`" is right (14.4–25.85).

### Item 3: processed-count ratios

Recomputed from the tables:

| Runs | processed / size, or ratio |
|---|---|
| C.1 restart table | 21.72, 23.54, 16.88, 22.16 |
| C.2 LS runs | 22.83, 22.30, 16.76, 15.51 |
| single passes | 3.96–6.21 |
| LS over the oracle pass | 6.52, 6.43, 5.03, 5.33 |

The new paragraph in C.1 gives these ranges correctly. It says that the oracle pass also
has the exact incumbent, so the factor 5.0–6.5 is not the cost of the restarts alone.
Correct.

### Item 4: RC wording (Section A.5)

- *`n = 4`.* "Stops at round 13 (the 14th round, counting round 0; 111,573 boxes)" is
  correct.
- *`n = 8`, from `logs/rc_zero_eps1e-6_tol.log`.*
  - The centre error is `0.25–10 h_j` at rounds 0–9 and `12–16 h_j` at rounds 10–15.
  - The incumbent is `1.013e-6` from round 14.
  - Round 14 has gap `1.59e-6`. The cycle `9.21e-7`/`1.54e-6` starts at round 15.
  - The error is `4096 h_j` at round 23.
- *`check_rc_cycle.py`.* It repeats `rc_lib.run_rc` with the same partition, slopes, DP,
  tolerance and incumbent rule. My rerun gives a log byte-identical to the author's
  (about 2 minutes).
  - The centre errors alternate between `9.7656e-4` and `1.2207e-3` from round 15.
  - `|xhat_j - xhat_{j-2}|_inf` is `3.66e-4, 5.11e-6, 1.46e-6, 4.18e-7` at `j = 16..19`.
  - So "from round 15 the centre alternates between two nearly fixed points" is
    accurate, and so are the quoted `5e-6` (round 17) and `4e-7` (round 19).

### Item 5: localization range and `N_dec/Psi`

- *Random instances.* In the final LS pass of `logs/random_n*_eps1e-4.log`,
  `|x^cons - x*|_inf/s_i` is 3.11–7.23 from level 6 on and at most 11.01 at levels 3–5.
  The new Summary and status-table wording is correct.
- *`c = 0`.* See N1 below: "about `6 s`" became "at most `6 s`", which the logs
  contradict at level 4.
- *`N_dec/Psi`.* For one flat bag, `N_dec/Psi >= (u/ceil(u))^d/V_d` with
  `u = sqrt(alpha/eps)`. This is at least `1/(2^d V_d) = Gamma(d/2+1)/(4 pi)^{d/2}` for
  `eps <= alpha` and tends to `1/V_d` as `eps -> 0`. With `lgamma`,
  `Gamma(d/2+1)/(4 pi)^{d/2} < 1` exactly for `d = 1..62` (0.691 at `d = 62`, 1.10 at
  `d = 63`). The new sentences are correct. An optional refinement is in Section 3.

### Item 6: boundary centres in RC

- `logs/check_rc_sensitivity.log` (widened test): `1e-9` moves of the twelve `±1`
  coordinates give 25,673–25,718 pairs instead of 25,612, and every move changes `l_r` by
  less than `1e-9` (largest `9.25e-10`).
- My recount of the round-1 partitions (`indep_r1_checks.py`, part 5) matches the note.
  - For all twelve `±1` coordinates, not only the four named in Section F, the partition
    has 11,357–11,369 leaves and 241 cells instead of 11,333 and 240, and the smallest
    leaf width is `1.0e-9`.
  - Interior coordinates leave the partition unchanged.
  - The example "11,360" in A.5 is coordinate 1.

The paragraph now says that the partition is discontinuous in a boundary centre but
`l_r` is not. Correct.

### Section F and the command table

The new subsection has one entry per issue, each with its check, and lists the targeted
commands. The numbers in it agree with my recomputations. Forward pointers were added to
the superseded first-round bullets (the second and third bullets of item 8). The
header status line was
updated.

### The item not applied

The confirmation review pointed out that `../dp_certificate.py` of [D] uses the same
closed intersection test. The reviser declined to investigate, because this concerns
[D], and Section D already records it as unchecked. I accept this.

- The only [D] numbers this note uses are the "shells [D]" columns of C.1. They come from
  [D]'s `E1`, which uses `c = 0`, `xs = np.zeros(n)` exactly, and `h = 2^{-j}`
  (`run_experiments.py`). All box edges are therefore exact binary fractions, and those
  columns are not exposed to the rounding problem.
- The concern applies to [D]'s runs with non-dyadic centres (Sections 5.2–5.3). It
  belongs in a review of [D].

## 2. Remaining problem

**N1 (minor; introduced in this revision). "At most `6 s`" at `c = 0` fails at level 4.**

- *Where.* Summary, Task 1, last bullet: "In sup norm it locates `x*` to at most `6 s`
  for every tested `n` (`c = 0`)". Status table, Conjecture A.7 row: "at most `6 s` at
  `c = 0`".
- *Data.* In `logs/oracle_eps1e-6.log` (exact slopes), `dxinf/s_i` at level 4
  (`s_4 = 1/8`) is 8.00 for `n = 16, 32, 64`. There the consistent point has a coordinate
  at `±1`. From level 5 on it is 3.99–6.02 for all `n`, and at levels 1–3 it is at most
  4.
- *Learned slopes at `c = 0`.* The `c = 0` runs of `logs/scaling_eps1e-4.log` also give
  8.00 at level 4 (`n = 16, 32`) and 11.98 at the stopping level 11 of `n = 4`.
- *Cause.* Section F item 5 justifies "at most" by the values at `n = 4, 8`. Those are
  the levels 8–12 values quoted in C.1. For the random instances the note already excludes
  the early levels ("from level 6 on, up to `11 s` at levels 3–5"). The `c = 0` statement
  needs the same kind of qualifier.
- *Suggested wording.* "In the exact-slope runs with `c = 0` it locates `x*` to at most
  `6 s` from level 5 on (`8 s` at level 4 for `n >= 16`)". Use the same qualifier in the
  status table.
- *Impact.* No conclusion changes. Conjecture A.7 is about `O(s)` independent of `|T|`,
  and the level-4 value is the same for `n = 16, 32, 64`.

## 3. Optional points

- **Contrast between exact and learned slopes (R2 text).**
  - Section F item 2 says "the bound holds only for the exact-slope runs". The status
    table and A.4 contrast "`26 n` with exact slopes" with "up to `45 n` with learned
    slopes".
  - The `26 n` bound is for `c = 0`. The random-`c` oracle runs, which also use exact
    slopes, reach `27.86 n` (seed 0) and `27.16 n` (seed 1) at `n = 16`, level 5
    (`logs/random_n16_eps1e-4.log`). The `45 n` comes from a random-`c` run with learned
    slopes *and* a learned incumbent.
  - The Summary is correctly scoped ("`c = 0`, `n <= 64`"). A fairer contrast at
    `n = 16` with random `c` would be `27.2–27.9 n` for the exact-slope oracle against
    `29.2–45.0 n` for LS.
- **`N_dec/Psi` for fixed `eps`.**
  - The note says that the `w^{Theta(w)}` order holds "as `eps -> 0`", and that for
    fixed `eps` the proven bound `Gamma(d/2+1)/(4 pi)^{d/2}` is below 1 for `d <= 62`.
    Both statements are true.
  - That bound is itself of order `w^{Theta(w)}`: about `(d/(8 pi e))^{d/2}`; `8.8e3` at
    `d = 80` and `9.3e15` at `d = 120`. So the order statement holds for every
    `eps <= alpha`. Only the threshold (`d >= 63`) is unfavourable.
  - The bound is also the worst case over `eps <= alpha`. For a particular `eps` the
    proven bound is `(u/ceil(u))^d/V_d`, which equals `1/V_d` when
    `sqrt(alpha/eps)` is an integer.
  - The current wording undersells the result. It does not overclaim.

## 4. Pre-existing imprecision (not part of this round)

**Summary, Theorem B.2 bullet: "a certificate of size
`O(K ((alpha d/eps)^{d/2} + C^d log(K/eps)))` exists".**

- *The construction.* Theorem B.2(b) uses `theta <= 2/sqrt(alpha d)`, so its shell term
  is `2 (J + 1)(4/theta)^d` with `4/theta` up to `4 sqrt(alpha d)`. That is
  `(sqrt(alpha d))^{Theta(d)}`, not `C^d` with an absolute `C`.
- *Example.* Take `alpha = 1`, `eps = 1/2`, `d = 1024`.
  - Then `theta = 1/16`, and the shell term is `2 (J + 1) 64^d`.
  - The fat-slice term is `(alpha d/eps)^{d/2} = 45.25^d`.
  - As `K` grows, the displayed form therefore needs `C >= 64`. At `d = 4096` it needs
    `C >= 128`.
- *What the proof supports.*
  `O(K ((alpha d/eps)^{d/2} + (C max(1, sqrt(alpha d)))^d log(K/eps)))`.
- *Impact.* Nothing else is affected. Theorem B.2(c) keeps `d` fixed, and in
  Proposition B.6(b) the factor is absorbed by `Phi_2`. The fix is to change the
  Summary's `C^d`, or to say that `C` depends on `d`.

## 5. Commands run

From `theory-decomposition/adaptive/` (reruns of the author's scripts; logs written to
`decomposition-adaptive-confirm-r1-checks/logs/`):

| Command | Result |
|---|---|
| `python3 check_phi_loss.py` | identical to `logs/check_phi_loss.log` (under 1 s) |
| `python3 check_rc_cycle.py 19` | identical to `logs/check_rc_cycle.log` (about 2 min) |

From `reviews/decomposition-adaptive-confirm-r1-checks/`:

| Command | Log | Result |
|---|---|---|
| `python3 indep_r1_checks.py` | `logs/indep_r1_checks.log` | part 1: actual shell partitions satisfy the `J + 1` count; the old bound is below the count for `h_0 > 4`. Part 2: B.6(b) holds with `L = J + 1` in 23,920 cases (max 0.286 of the constant; each of the three comparisons holds); the old `L` fails in 182 cases (`h_0 >= 4.4`, up to 1.357). Part 3: `Gamma(d/2+1)/(4 pi)^{d/2} < 1` exactly for `d <= 62`. Part 4: split maxima, plateau, learned-slope maxima, localization by level (N1), processed ratios, RC `n = 8` rounds. Part 5: round-1 RC partitions under `1e-9` moves |

I also ran the part 5 recount once inline before adding it to the script, with the same
result. Total CPU time was about 3 minutes, single-threaded.
