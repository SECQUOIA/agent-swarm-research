# Confirmation recheck of the second revision of "Consistency relaxations on tree decompositions"

Date: 2026-09-30. Note:
[`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
("the note"; second revision, 2057 lines; changes listed in its Section 12.2).
Earlier reports: [`consistency-review.md`](consistency-review.md) (the review) and
[`consistency-recheck.md`](consistency-recheck.md) (the recheck, which raised
the seven issues checked here). I did not write the note or either earlier
report.

**My checks.** My scripts and logs are in
[`recheck-consistency-confirm-checks/`](recheck-consistency-confirm-checks/).
They share no code with the author, the review or the recheck. The one
exception is `logs/scratch_reruns.log`: there I reran the author's changed
scripts in a scratch copy (`/tmp/confirm_cons/tc`, outside the repository) to
test that their logs reproduce.

**Earlier text.** The recheck's scratch copy `/tmp/recheck/tc/` still holds
the first-revision note and scripts. So I diffed the current note and scripts
against them line by line, rather than relying on quotations.

**Scope.** Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification and no CI. I did not edit the note, its scripts or its logs, and
I did not commit anything.

## Verdict in brief

**All seven fixes are applied, and applied correctly. No mathematical error
found.**

- **New arguments.** The revision adds two arguments that its header calls
  "not checked independently": the T1 limit bound (Section 3, Remarks) and
  Proposition 5.8(b). I checked both proofs step by step and tested both
  numerically. Both are correct.
- **Numbers.** Every number I recomputed agrees with the note.
- **Withdrawn claims.** They are clearly marked where they were made and in
  Section 12.
- **Remaining problems.** Six small points remain (Section 3):
  - one new sentence is false for small `n` ("so it grows with `c`");
  - one sentence in Section 10 states as fact what the note elsewhere labels
    numerical. A short proof, given below, would make it true.
  - The other four are about precision of wording.

| Recheck issue | Verdict |
|---|---|
| 1. "Attained only in trivial cases" (silent strengthening) | **fixed.** Withdrawn and marked in all five places. The T3 counts 515 / 93 / 247 reproduce with a formulation that shares no code with the note's (the dual measure LP). The new T1 limit bound is proved correctly, and its numbers check out. Finite-`K` strictness is labelled numerical everywhere except Section 10 (remaining problem 2). |
| 2. Emptied tree log | **fixed.** The log is non-empty. It matches the recheck's scratch log exactly apart from the 4 new lines, and a fresh scratch rerun reproduces it exactly. The `check_hp.py` change touches only log handling (diff), and `check_hp.log` reproduces exactly. |
| 3. Unaligned hp argument | **fixed, by a different and valid route.** The Bernstein-ellipse inclusion `E_rho(D) ⊂ E_rho(I)` is correct. It makes the relative distance irrelevant under the proposition's hypothesis. Proposition 5.8(b) and its counting are correct. The bound holds numerically for `rho = 2, 4, 8`. Labels agree across sections. |
| 4. Alfonsi et al. | **fixed.** Quotes and proposition numbers are checked against arXiv 1905.05663v1. One precision point: for `W_1` the paper assumes a bounded density *difference*, not bounded densities (remaining problem 3). |
| 5. GNS credit | **fixed.** I read GNS Lemma 3 and its proof in arXiv math/0611498v1: same construction as described, qualitative only. KMR's "a version of [4, Lemma 3]" is confirmed, and v1 is the only arXiv version. Crossref confirms both KMR (Math. Program. 209(1–2), 435–473, 2025) and GNS (Arch. Math. 89(5), 399–403, 2007). |
| 6. Corollary 5.5 | **fixed.** `q0`, `s_e`, "at most", the `theta <= 1` case and `max(16Mk/c, 16)^{k/2}` are all correct. I rederived them from [D, Lemma 3.1]. The stale constant is gone. |
| 7. Wording (a)–(g) | **fixed.** The one exception is item (d): its new sentence "so it grows with `c`" is false for `2 <= n <= 8` (remaining problem 1). |

## 1. Each fix, checked from scratch

### 1.1 Lower end of Theorem 3.1 (recheck issue 1)

**Withdrawal.** The diff shows that the false "attained exactly only in
trivial cases" now appears only inside correction notes:

- Section 3, Remarks: "That was wrong and is withdrawn";
- Section 12.1 item 6, which points forward to 12.2;
- Section 12.2 item 1.

The Summary (B), Section 7.4, the status table and Section 10 now give the
T3 attainment counts instead.

**T3 counts, recomputed independently** (`c1_tree_T3.py`). I used the same
random instances (seed 0, same draw order), but different formulations:

- the gap from the measure LP of Theorem 1.1 (the dual), not the split LP;
- each `2 dist(Phi_e, Band_e)` from the one-separator band LP of Theorem 2.1
  on the explicit value functions `U_e`, `L_e = f* - V_e`, not from a tree
  LP with a full class on the other edge;
- a Legendre basis instead of a Chebyshev one.

Results:

- lower end attained (to `1e-7`) in **515** of 900 cases;
- in **93** of these, both per-edge terms exceed `1e-4`;
- the per-edge sum is below the gap in **247** cases;
- the three logged examples agree to 10 digits (trial 2, degree 0:
  1.4297860847 against `2 dist_1` = 0.3156535776).

This also cross-checks the note's use of Theorem 2.1 inside Theorem 3.1's
lower bound: the band LP and the note's "full class on the other edge" LP give
the same numbers.

For degree 0 there are closed forms:

- `gap = f* - min a - min b - min c`;
- `2 dist_1 = f* - min a - min(b + c)`;
- `2 dist_2 = f* - min(a + b) - min c`.

They agree with the LPs to `9e-16`. Attainment is then an exact combinatorial
event, not a tolerance effect: 54 of the 300 degree-0 cases, 23 of them with
both edge terms positive. So "attained" is literally true in these instances.

**The T1 limit proof** (Section 3, Remarks). I checked each step:

- with `phi_1 = phi_2 = -p` and `r = |s| - p`, the three bags are `-r(s1)`,
  `r(s1) - r(s2) + K d^2` and `r(s2)`;
- `f* = 0`;
- both bands are single functions: `U_1 = L_1 = -|s1|` and
  `U_2 = L_2 = -|s2|`;
- the middle bag is at least `min_d (-Lip(r)|d| + K d^2) = -Lip(r)^2/(4K)`;
- `osc(r) = 2 E_n` for the best approximant.

So `2E_n <= gap <= 2E_n + Lip(r)^2/(4K)`, and the limit is proved.

**The T1 numbers** (`c2_t1_bound.py`: a Remez exchange for `E_{n/2}(sqrt t)`
on `[0, 1]`, which equals `E_n(|s|)`):

- `2E_4 = 0.1352417986` and `2E_8 = 0.0693794562`. These equal the review's
  R3 values.
- `Lip(r) = 1.401566` (`n = 4`) and `2.399963` (`n = 8`); the note gives
  1.40 and 2.40.
- The bound on `gap/2E_n` at `K = 100` is 1.03631 and 1.20755; at
  `K = 1000` it is 1.00363. The note gives 1.036, 1.208 and 1.0036.
- The 161- and 321-point grid values of `2E_4` are 1.06e-4 below Remez
  (relative). This matches "within about 1e-4".
- Finer grid LPs at `n = 4`, `K = 100` (middle-bag constraints restricted to
  a diagonal band; the solution was then checked against all grid
  constraints) give lower estimates of the continuum ratio:

  | Grid points | 161 | 321 | 641 | 1281 | 2561 |
  |---|---|---|---|---|---|
  | Ratio (lower estimate) | 1.0007 | 1.0131 | 1.0137 | 1.0148 | 1.0148 |

- The fixed split `-p*` evaluated directly gives 1.0348.
- So the continuum ratio lies in about `[1.015, 1.035]`. The note's "between
  about 1.013 and 1.036" is correct, if slightly wide.

**Sufficient condition for attainment.** The note says: if the enlarged
relaxation `Phi'` has an optimal split whose other components lie in their
classes, then `rho(Phi) = rho(Phi')`. This is correct and immediate. When the
supremum is attained (Proposition 1.2), the condition is also necessary.

### 1.2 The emptied log (recheck issue 2)

- **Script changes.** `diff` against the pre-revision copies shows:
  - in `check_hp.py`, only the log handling changed (`out = None` at import;
    `open` under `__main__`; `log()` writes only if `out` is set);
  - in `check_tree.py`, the same change plus the T3 attainment count.
- **Regenerated tree log.** `logs/check_tree.log` (3868 bytes) differs from
  the recheck's `check_tree_rerun_scratch.log` only by the 4 new attainment
  lines. So every number in Section 7.4 has a log again: the T1 table, T2,
  249, 1.7646 and 247.
- **Scratch reruns.** `check_tree.py` (21 s), `check_revision2.py` (61 s)
  and `check_hp.py` (6 s) all reproduce the repository logs exactly.
- **Import side effects.** Importing `check_hp` from `check_revision2.py`
  created no `check_hp.log` in the scratch copy, so the import no longer has
  side effects.
- **Other scripts.** `check_duality.py`, `check_pinch_rates.py` and
  `check_revision.py` still open their logs at import, but `grep` finds no
  module that imports them. Only `check_tree` and `check_hp` are imported.
  Leaving them is acceptable.
- **Section 11.** The regeneration is recorded there accurately.

### 1.3 Unaligned hp (recheck issue 3): Proposition 5.8(b)

The author did not switch to a geometric mesh. Instead the relative-distance
step was replaced by a different argument. I checked it.

- **Hypothesis.** Each piece's affine image extends analytically to
  `E_rho`, so each piece is analytic in a neighbourhood of its *closed*
  interval. `-|s - c0| +` (entire) satisfies this; `|s - c0|^{4/3}` does
  not. Both examples are stated correctly.
- **Inclusion `E_rho(D) ⊂ E_rho(I)` for `D ⊂ I`.**
  - In physical coordinates,
    `E_rho(I) = {z : |z - a_I| + |z - b_I| < |I| R}` with
    `R = (rho + 1/rho)/2`. The sum of the focal distances is twice the
    semi-major axis, `(|I|/2)(rho + 1/rho)`.
  - The triangle inequality gives `< |D| R + (|I| - |D|) <= |I| R`, because
    `R >= 1`. This is correct.
  - A random test of 2000 pairs of intervals and parameters gives a largest
    normalized focal sum on `∂E_rho(D)` of `1 - 2.5e-8`.
- **Cells away from `c`.** Each such cell inherits `M` and `rho` from its
  piece. So Proposition 5.5(a) (`2E_p <= 4M rho^-p/(rho - 1)`, from
  Trefethen's Theorem 8.2) applies however close the cell is to the kink.
  This removes the need for the relative-distance hypothesis. The recheck's
  objection (`rho` about 1.36 at level 4) assumed a singularity at `c0`,
  which this hypothesis excludes.
- **Kink cell.** `2E_1 <= 2E_0 = osc <= G (b - a) 2^-m`. Correct; `psi` is
  Lipschitz because each piece has a bounded derivative and `psi` is
  continuous.
- **Counting.**
  - `N = m(p + 1) + 2`.
  - `p = ceil(m log 2/log rho)` gives `rho^-p <= 2^-m` and
    `N <= beta_0 m^2 + 2m + 2`.
  - Solving the quadratic gives `m >= sqrt((N - 2)/beta_0) - 1/beta_0`.
  - `2^{1/beta_0} = rho` and `sqrt(N - 2) >= sqrt N - sqrt 2`.
  - So `gap <= C' exp(-b sqrt N)` with
    `C' = max(4M/(rho - 1), G(b - a)) rho e^{b sqrt 2}` and
    `b = sqrt(log 2 · log rho)`. All steps are correct.
- **Numerical test of the stated inequality** (`c3_prop58b.py`). I used the
  note's `psi`, `rho = 2, 4, 8`, `M` from the maximum modulus on each
  piece's ellipse, and `G = max|psi'| = 1.910`, for `m = 2..14`.
  - Both `gap <= max(4M rho^-p/(rho - 1), G(b - a)2^-m)` and
    `... <= C' exp(-b sqrt N)` hold in all 21 cases, with room: the bound
    exceeds the gap by factors of about 7 to 280.
  - Here the gap is an upper estimate: a grid LP re-evaluated on a 10x
    finer grid.
- **Per-cell factors** (independent Remez, relative self-check below
  `1e-9`):
  - on `[0.25, 0.375]` against `[0.125, 0.25]`, the ratios of `2E_p` for
    `p = 1..4` are 1.70, 0.70, 1.51, 0.70 for `psi`, and 2.05, 4.20, 53.68,
    180.66 for the `|s - c0|^{4/3}` variant;
  - these are exactly the note's values;
  - the level distances (0.047, 0.071; others 0.48–1.91) and "the kink cell
    dominates at every `m`" reproduce in the scratch rerun of
    `check_revision2.py`.
- **Labels.** They now agree across sections:
  - Proposition 5.8(b) is described as proved (or "gives an elementary
    bound") in Section 5.5, the Summary, Section 8, the status table and
    Section 10;
  - algebraic singularities at breakpoints are "not proved" in Section 5.5,
    Section 8, the status table and Section 10;
  - the geometric-mesh claim for that case is labelled "suggests ..., but
    this is not proved here".

### 1.4 Alfonsi et al. (recheck issue 4)

I read Section 5 of arXiv 1905.05663v1 (the text the recheck downloaded).

- **Proposition 5.1.** `I^N <= I <= I^N + K/N` for indicator test
  functions and a `K`-Lipschitz cost on `[0, 1]^2`. Correct.
- **Section 5.2.** "Let us now explain with a rough calculation why
  considering these test functions may lead to a convergence rate of
  `O(1/N^2)` when `c` is `C^1` with a Lipschitz gradient", and later
  "Unfortunately, such kind of a result is not obvious." Both quotes are
  accurate.
- **Proved rates.**
  - `W_1`: Proposition 5.7 and Corollary 5.8.
  - `W_2^2`: Proposition 5.9 and Corollary 5.10, with
    `rho_mu, rho_nu in L^inf`.
  - Both are proved through distribution functions.
  - The numbering and "two specific costs" are correct.
- **Precision point.** For `W_1` the paper assumes absolutely continuous
  marginals, at most `Q` sign changes of `F_mu - F_nu`, and
  `rho_mu - rho_nu in L^inf`. It adds that boundedness near the sign
  changes suffices. The note says "bounded densities", which states a
  stronger hypothesis than the paper needs (remaining problem 3). The key
  correction (the rates do not come from approximating Kantorovich
  potentials) stands.

### 1.5 GNS credit (recheck issue 5)

**GNS Lemma 3** (arXiv math/0611498v1, which I downloaded and read):

- For `f = f_1 + ... + f_r > 0` on `K^n`, it gives `f = h_1 + ... + h_r`
  with `h_j > 0` on `K^{I_j}`.
- The `r = 2` proof sets `h(y) = min_x f_1(x, y) - eps/2`.
- It shows `f_1 - h >= eps/2` and `f_2 + h >= eps/2`, then approximates `h`
  by a polynomial to within `eps/4`, with no degree bound.
- The note's Section 8 description is accurate.

**KMR** (arXiv 2303.14824v1):

- Its Lemma 11 is headed "a version of [4, Lemma 3]".
- Its reference [4] is GNS, Arch. Math. 89(5):399–403, 2007.
- The arXiv abstract page lists only `[v1]`.

**Crossref** confirms both records:

- KMR, *Mathematical Programming* 209(1–2), 435–473, 2025;
- GNS, *Archiv der Mathematik* 89(5), 399–403, 2007.

**Credit in the note.** The Summary (F), Section 8 (GNS entry, KMR entry,
novelty list) and the status table now credit the qualitative form to GNS
and the quantitative version to KMR. The unverified published lemma
numbering is disclosed.

### 1.6 Corollary 5.5 (recheck issue 6)

I rederived the corollary from [D, Lemma 3.1]. That lemma requires
`theta = 2^{-mu}` with `mu >= 0` and gives `(J + 1)(4/theta)^k` boxes, where
`J = max(0, ceil(log2(s0/h)))`.

- **Central cubes.** `r^2 = k h^2/4 = eps/M`.
- **Shell cubes.** `M r^2 <= M k theta^2 d^2/4 <= c d^2 <= w_min`.
- **Outer cubes.** `L(s) - U(t) <= -w(s) + G diam < 0`.
- **Level count.** `J + 1 <= log2(q0/h) + 2` once `h <= q0`.
- **Outer term.** `O((1 + G s_e k^{3/2}/(c rho_0^2))^k)`.
- **Two cases for `theta`.**
  - If `theta < 1`, then `2 theta` is still an admissible power above the
    threshold, so `theta > (1/2) sqrt(4c/(Mk))` and
    `(4/theta)^k < (16Mk/c)^{k/2}`.
  - If `theta = 1` (exactly when `c >= Mk/4`), the factor is
    `16^{k/2}`.
  - Hence `max(16Mk/c, 16)^{k/2}`.
- **"Nothing ties `c` to `M`".** Correct: by Lemma 4.2,
  `c <= (M + M_L)/2`, and `M_L` is free.
- **Where the change was made.** The diff shows the new factor in the
  corollary, the comparison paragraph, the Summary and the status table,
  with the `k >= 2` hypothesis added to the Summary.

### 1.7 Wording items (recheck issue 7)

- **(a)** The Summary (D) now makes the `C^{1,1}` band element conditional
  on completing Proposition 4.3, including its open-boundary hypothesis.
  Correct.
- **(b)** The lsc sketch after Proposition 1.3 is labelled "sketch" in the
  text and in the status table, and it is right:
  - the lsc hull keeps the infimum and the closed convex envelope;
  - `cl vex f(p) = min {∫ f dnu : mean nu = p}` holds for bounded lsc `f`:
    the right side is convex and lsc by weak* compactness and the
    portmanteau inequality, and it minorizes every lsc convex minorant by
    Jensen's inequality;
  - Sion's theorem needs only lower semicontinuity in the measures.
- **(c)** Reduced bands (backed by Corollary 3.4, which needs parent-side
  value functions) versus dual marginals (untested). Consistent in the
  Summary (E), Section 6, Section 10 and Section 12.
- **(d)** The looseness factors are right. From `check_revision2.log` and
  the review's R3 log:
  - 18.3 (`c = 8`, `n = 2`) to 71.7 (`c = 8`, `n = 32`) for
    `2 <= n <= 32`; R3's extra `n = 6` values (33.7–39.0) lie inside this
    range;
  - 105, 150, 330 at `n = 1`;
  - 51.0, 63.1, 107.5 at `n = 128`, from the lower estimates in
    `check_pinch_rates.log` (0.4855, 0.4209, 0.3257).
  - But the new lead-in sentence "so it grows with `c`" is false for small
    `n` (remaining problem 1).
- **(e)** At `n = 128` the values 0.49, 0.42, 0.33 are labelled as lower
  estimates, with upper estimates 0.50, 0.48, 0.53. These match
  `check_pinch_rates.log` (0.5022, 0.4754, 0.5330), in Sections 5.4 and 7.1
  and the E6 table.
- **(f)** The Summary now names [S]'s identities and derives the
  inequality from them. Correct.
- **(g)** The heuristic is flagged as weak in the Summary (C), Section 5.4,
  the status table and Section 10. "The limit may be smaller" is the only
  possible alternative: the band for `c > 0` contains the band for `c = 0`,
  so `n gap(c) <= n · 2E_n(|s|) -> 2 beta`.

## 2. Was anything silently strengthened? Are the withdrawn claims marked?

I went through the full diff between the first-revision note and the current
note.

- **Stronger statements.** Only two new statements are stronger than
  before:
  - Proposition 5.8(b), which is now proved (checked above);
  - the T1 limit, which is now proved (checked above).

  Everything else is equal or weaker: conditional wording for
  Proposition 4.3, "should" instead of "must", "weak heuristic", "lower
  estimates", and GNS credit that narrows KMR's.
- **Withdrawn claims, clearly marked:**
  - "only in trivial cases": Section 3 Remarks, 12.1 item 6, 12.2 item 1;
  - the "fixed relative distance" argument: Section 5.5 ("For dyadic
    bisection that is false"), 12.1 item 4, 12.2 item 3;
  - the Alfonsi "regularity of the cost" reading: Section 8 ("as the first
    version of this note said"), 12.1 item 5, 12.2 item 4;
  - "must use ... joint dual marginals": 12.1 item 7.
- **Two small overstatements introduced by this revision:** remaining
  problems 1 and 2 below.

## 3. Remaining problems (all minor)

1. **"so it grows with `c`" is false for small `n`.**
   - *Where.* Section 5.4, the paragraph added for item 7(d).
   - *Evidence.* The ratio `30(3 + c) n gap` falls with `c` for `n = 2, 3,
     4`. At `n = 2` it is 35.0, 25.0, 18.3 for `c = 0.5, 2, 8`. At `n = 8`
     it is not monotone (40.0, 36.5, 39.2). It grows with `c` only at
     `n = 1` and for `n >= 16`.
   - *Fix.* Drop "so it grows with `c`", or write "for `n >= 16` it grows
     with `c`".
2. **Section 10 states finite-`K` non-attainment in T1 as fact.**
   - *Where.* Section 10 says the lower end is attained "in T1 only in the
     limit `K -> inf`".
   - *The inconsistency.* The Summary, Section 3, Section 7.4 and the
     status table correctly label finite-`K` strictness as numerical only.
   - *Fix.* Either reword ("approached as `K -> inf`; strictness at finite
     `K` numerical"), or add the short proof below, which makes the
     sentence true.

   **Proof that `gap > 2E_n` for every finite `K > 0`.** I checked this
   argument; it is new, not in the note.

   *Setup.* Write `phi_e = -p_e` and `r_e = |s| - p_e`. Then

   ```
   rho(p_1, p_2) = -max r_1 + m_B + min r_2,
   m_B = min_{s1,s2} [r_1(s1) - r_2(s2) + K (s1 - s2)^2] <= min_s (r_1 - r_2).
   ```

   So `-rho >= X := max r_1 - min r_2 + max(r_2 - r_1)`.

   *Step 1: `X` bounds both oscillations.* Evaluate `max(r_2 - r_1)` at
   `argmax r_2`: this gives `X >= osc(r_2)`. Evaluate it at `argmin r_1`:
   this gives `X >= osc(r_1)`. Also `osc(r_e) >= 2E_n`, with equality only
   if `p_e = p* + const`, by uniqueness of the best approximation.

   *Step 2: equality forces the best approximant.* If `-rho = 2E_n`, then
   `r_e = r - c_e`, where `r = |s| - p*`. So `r_1 - r_2` is the constant
   `c_2 - c_1`.

   *Step 3: the middle bag then falls strictly below the bound.* `r` is
   Lipschitz and not constant, so `r'(s0) != 0` at some interior point
   `s0`. Moving `s1` a distance `delta` from `s0`, against the sign of
   `r'(s0)`, makes `r(s1) - r(s0) + K delta^2 < 0` for small `delta`. So
   `m_B < c_2 - c_1`, and `-rho > X >= 2E_n`, a contradiction.

   *Conclusion.* Every split has `-rho > 2E_n`. The supremum is attained
   (Proposition 1.2), so `gap > 2E_n`.

   *Numerical consistency.* The finer grids above give a ratio of at least
   1.0148 at `K = 100`. The grid ratio 1.0000 at `K = 1000` does not
   contradict the proof: on a grid, `delta` cannot be made small.
3. **Alfonsi et al., `W_1` hypothesis.**
   - *Where.* Section 8.
   - *Problem.* "bounded densities" should read "absolutely continuous
     marginals with bounded density difference `rho_mu - rho_nu`
     (boundedness near the sign changes of `F_mu - F_nu` suffices)". For
     `W_2^2`, "bounded densities" is right.
4. **"Analytic up to the breakpoint/kink" is ambiguous.**
   - *Where.* The Summary (D), Section 8, the status table and Section 10.
   - *Problem.* This shorthand can be read as covering
     `(s - c0)^{4/3}`, which is analytic on the open piece and continuous
     up to `c0`. Proposition 5.8 explicitly excludes that case.
   - *Fix.* "Each piece extends analytically across the breakpoint" (or
     "analytic in a neighbourhood of each closed piece") would match the
     hypothesis.
5. **Notation in Proposition 5.8(b).**
   - *The clash.* The letter `b` denotes both the right endpoint of
     `X_S = [a, b]` and the rate `sqrt(log 2 · log rho)`, in the same
     display. Rename one, for example the rate to `beta_1`.
   - *Also.* "If `c` becomes a cell boundary, (a) applies" is loose. Then
     every cell lies in one piece, so the inclusion argument (not (a),
     whose cells are whole pieces) bounds every cell.
6. **Status labels can now be updated.** The header, the Section 9
   preamble and the status table (Proposition 5.8(b); Theorem 3.1's T1
   limit) still say "not checked independently". This report checks both.
   Whoever maintains the note may update the labels, citing this report.

## 4. Commands run (targeted checks only)

In `reviews/recheck-consistency-confirm-checks/`, with `OMP_NUM_THREADS=1`:

```
python3 c1_tree_T3.py    # logs/c1_tree_T3.log; T3 counts via the measure LP and explicit-band LPs; 5 s
python3 c2_t1_bound.py   # logs/c2_t1_bound.log; Remez E_n(|s|), Lip(r), T1 bound, grid LPs to 2561 points; 22 s
python3 c3_prop58b.py    # logs/c3_prop58b.log; ellipse inclusion, Prop 5.8(b) inequality for rho = 2, 4, 8, Remez cell factors; 25 s
```

In a scratch copy `/tmp/confirm_cons/tc` of `theory-consistency/`, outside the
repository (results in `logs/scratch_reruns.log`):

```
python3 check_tree.py; python3 check_revision2.py; python3 check_hp.py   # each log diffed against the repository log: identical
diff /tmp/recheck/tc/<script> theory-consistency/<script>                # pre-revision scripts and note against current ones
```

Sources:

- arXiv 1905.05663v1, Section 5 (text in `/tmp/recheck/acel.txt`, from the
  recheck);
- arXiv 2303.14824v1 (text in `/tmp/recheck/kmr.txt`) and its abstract page
  (version list);
- arXiv math/0611498v1 (downloaded and read; not kept);
- Crossref records `10.1007/s10107-024-02071-6` and
  `10.1007/s00013-007-2234-z`;
- [D, Lemma 3.1] in `theory-decomposition/decomposition-certificates.md`.

Environment: Python 3.13.11, numpy 2.5.1, scipy 1.18.0 (HiGHS). No
project-wide verification, no CI inspection, no edits to the note or its
files, no commits.
