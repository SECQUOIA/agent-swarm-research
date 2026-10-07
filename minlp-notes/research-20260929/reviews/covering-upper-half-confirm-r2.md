# Confirmation review (round 2): `covering-upper-half.md` after the second revision

Date: 2026-09-30. Note checked:
[`../theory-decomposition/covering-upper-half.md`](../theory-decomposition/covering-upper-half.md),
as revised after the round-1 confirmation review
([`covering-upper-half-confirm-r1.md`](covering-upper-half-confirm-r1.md)). I also
checked its new and changed scripts and logs in
[`../theory-decomposition/covering/`](../theory-decomposition/covering/). The parts
of [D] (`decomposition-certificates.md`) used by the revision are Definition 1.2,
Lemmas 1.4 and 1.5, Proposition 2.4 and Theorem 2.5. For [C]
(`instance-dependent-node-complexity.md`), the revision uses Section 1.1. I also
checked the arXiv abstract of Ruozzi–Tatikonda.

I did not write the note or either earlier review. I edited no note and no root
file, and I committed nothing. My scripts and logs are in
[`covering-upper-half-confirm-r2-checks/`](covering-upper-half-confirm-r2-checks/).
All runs were single-threaded (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`).
They are targeted checks of this note only. I ran no project-wide verification and
did not consult CI.

## Verdict: verified

All nine round-1 items (M1, M2, T1–T6, O1) are fixed correctly. I rechecked each
one from scratch, by hand and by rerunning or recomputing the numbers. None was
declined. T6 was adopted in a different form from the one suggested. The arXiv
abstract supports that form: the suggested wording covered only one of the
abstract's two uses of graph covers.

The revision strengthens two results, Lemma 2 (sharp constants `(4, 4)`) and
Corollary 3.3 (factor `2 ceil(sqrt(M/alpha)/2)`). Both are proved correctly, and
both proofs are complete. No other statement goes beyond what the note proves or
computes. The new remark after Theorem 3 is labelled as a sketch, and its steps are
correct.

Three trivial points remain (Section 3). None affects a result, and none needs
another review round.

## 1. The round-1 items, rechecked

**M1 (Proposition 5, slope clause). Fixed correctly.**

- *Statement.* The first bullet now requires one of two slope conditions:
  - the slope of the balanced minimizer of the closed-cell bracket `g'_{e,D}` (half-width `tau' w_e`);
  - or any slope whose bracket, minimized over the intercept alone, is at most `eps/(2n)`.

  The intercepts stay maximal.
- *Proof.* The proof now says where the slopes enter. I checked the chain:
  - Theorem 3's validity argument, with `h = 4r/tau'`, gives `g'_{e,D} <= (16/tau' + 1/2) M_e r^2 - tau' w_min` for interior cells, and `2 G_e r + (5/2) M_e r^2 - 2 tau' w_min` for the others.
  - With balanced intercepts, both suprema on each cell equal half of that cell's intercept-minimized bracket. So edge `e` contributes at most `max_D g' <= eps/(2n)` in Lemma 1'.
  - Raising intercepts to their maximal values never lowers `rho~`, so `l_r >= f* - eps/2 - eps/2`.
- *Counterexample paragraph.* It is correct. With `n = 1`, `theta' = 1/2` and `psi' = lambda s`. A constant minorant on `[0, ell]` gives `beta = 0`, since the leaf function `lambda s + M s^2/2` is increasing there. The root minimum on that cell is `-lambda ell + M ell^2/2` for `ell <= lambda/M`.
- *The note's check.* `check_prop5_slopes.py` implements this model correctly. It uses the R3-adapted `B'` above and exact minima of quadratics on intervals. My rerun is identical to the log:
  - gaps of 1.6, 5.2, 33.9 and 280 `eps` with constant minorants;
  - gap 0 with slope `lambda`;
  - gaps of 0.494–0.498 `eps` with the extreme allowed slopes.

  For small `eps`, the largest gap with constant minorants comes from cells away from 0, not from the cell at 0. The text claims only a lower bound from the cell at 0, so it is consistent with this.
- *Independent `n = 2` test (my code, `indep_prop5_n2.py`).* The note tests only `n = 1`, where the bag terms vanish trivially. So I tested a two-edge path with quadratic bags:
  - Setup: exact value functions, cells from the R3 rule adapted to `tau' = 1/7` with tolerance `eps/4`, and exact leaves aligned with the cells. The middle bag has leaves `D1 x D2`. The certificate value `l_r` is exact (box minima of quadratics). There are three instances: two tilted ones and Proposition 4 with `beta = 1`, `kappa = 10`. Each is run at `eps = 1e-2, 1e-3, 1e-4`.
  - With the slope clause: the balanced brackets are at most `3.1e-6 <= eps/4`. The gaps are 0 (balanced slopes), at most `0.49964 eps` (extreme allowed slopes, four combinations) and at most `0.476 eps` (random allowed slopes). All are within the proven `eps/2`.
  - With constant minorants: the tilted instances fail, with gaps up to `18.2 eps`. The untilted Proposition 4 instance passes (at most `0.002 eps`). This matches the note's wording "can fail".

**M2 (Section 5). Fixed correctly.** The lead sentence is now restricted to
`kappa > 2 beta`, and the `kappa = 2 beta` case is named. I rederived the reduced-band
width, `beta(kappa - 2 beta)/(kappa - beta) s1^2`. It is zero on `|s1| <= 1/2` when
`kappa = 2 beta`. `check_prop4.log` shows width `1.39e-17` there. The "no affine
function" argument covers both cases.

**T1 (Lemma 2). Fixed, and the lemma is strengthened correctly.** I checked the new
proof step by step.

- *Reduction.* `U_c = U - (M/2)(s-c)^2` is concave, `L_v = L + (M/2)(s-c)^2` is convex, and `phi = L_v - U_c` is convex. `U_c'` differs from `U'` by `-M(s - c)`, so `Delta_U` is the slope drop of `U_c`. Likewise `Delta_L` is the slope rise of `L_v`, and `Delta_U + Delta_L = phi'(beta-) - phi'(alpha+)`.
- *Upper bound.* The chord-slope bounds on `[beta, c+h]` and `[c-h, alpha]` hold for convex `phi`. So does `phi(alpha) + phi(beta) >= 2 phi(c)`. Together with `phi(c ± h) <= M h^2` and `phi(c) = -w(c)`, they give `4 w(c)/h + 4 M h`.
- *Sharpness.* Every convex `phi <= M(s-c)^2` comes from an admissible pair. I checked both slope cases of the family:
  - The first case is the line through `(h, M h^2)`, with slope at least `2Mh`, so it stays below the parabola for `v <= h` by convexity of the difference.
  - The second case is the tangent from `(a, -W)`, with `v0 = a + sqrt(a^2 + W/M)`.

  Both kinks lie inside `[alpha, beta]`, so the rise is `2k`. As `delta -> 0`, `2k` tends to `4W/h + 4Mh`, including `W = 0` (`4Ma -> 2Mh`). Taking `M = 0`, and then `W = 0`, shows that neither coefficient can be lowered.

  The supremum is not attained: equality in all three convexity steps would force `phi` to be affine. So "supremum" is the right word.
- *Consequences.* The kink remark (`8 sqrt(M w(c))`, `w(c) >= J^2/(64 M)`) is correct. Section 4 still uses `(8, 8)`, so Theorem 3 and R3 are unchanged.
- *Sketch after Theorem 3.* I checked every step with `h = 4nr`:
  - `h >= 4r`, so `D ⊂ [c_m - h/2, c_m + h/2]`;
  - `B = (8n + 1/2) M r^2 - w_min/(2n)`;
  - the split threshold is `(16 n^2 + n) M r_j^2 - 2 eps`;
  - `sqrt(16n^2 + n) <= 4n + 1/8`, which gives `4n + 2` cells per interval;
  - there are `2n` near-boundary cells per end per level, which gives `4n J'_e`.

  The labelled bound `1 + (4n+2) J~_e N_e + 4n J'_e` follows.
- *Numbers.* My reruns of `check_kink_concentration.py` and `check_kink_sharp_lp.py` are identical to their logs. The first 15 lines of the kink log match the round-1 reviewer's rerun, apart from its trailing timing lines. The quoted figures are right: random pairs at most 0.5475; family ratios 0.95–0.98 at `delta = 1e-2` and 0.999995–0.999998 at `1e-6`; `U - L >= -6.6e-16`; LP ratios 0.74–0.80, 0.969–0.970 and 0.9961.
- *Independent check (`indep_lemma2_sharp.py`, my code, exact arithmetic on max-of-affine `phi`).*
  - 20,000 random convex `phi` shifted exactly below the parabola: largest ratio 0.935.
  - Differential evolution in five settings (2–4 pieces): the ratio approaches 1 from below. The largest value is `1 - 9.1e-13`, and it never exceeds 1.
  - The pairs `(3.9, 4)` and `(4, 3.9)` are violated by admissible members of the family, as claimed.

**T2 (Section 5). Fixed correctly.** The margin-and-curvature sentence now names R3
and B.4's rule, and `bd`'s sliver test is described separately. The claim that `bd`
does not refine at a pinch point where `psi_e` is locally affine is right. The
bracket with `l = psi_e` is `-2 min_D w_e/(2n) <= 0`. I also rederived
`psi_1 = (kappa beta/(4(kappa + beta)) - 3 beta/2) s1^2`. (A step in the stated
reason is missing; see Section 3, item 3.)

**T3. Fixed correctly.** The logged maximum is `-7.08e-05` (D2, `eps = 1e-3`).
`<= -7.0e-5` now appears in Section 4, in the Section 10 table and in the round-1
entry.

**T4. Fixed correctly.** From `check_naive_failure.log`, only `n = 2`, `eps = 1e-2`
drops by more than a factor 10: `6.07e-3 -> 3.59e-4` (`m = 129`) and
`6.64e-3 -> 4.15e-4` (`m = 257`). The other drops at `eps = 1e-2` are as quoted.
The `eps = 1e-3` rows with `n = 2, 3` do not change.

**T5 (notation). Fixed correctly.** A search finds no remaining use of `D` or `D'`
as a discount. `L_t` now means only the lower value function, and the leaf family is
`Leaves_t`. `tau` and `tau'` are used consistently in the proofs of Theorems 1
and 1', Lemma 1' and Proposition 5. `l_c` has the same meaning in the proofs of
Theorem 3 and Corollary 3.3, and `l_e` remains the length of `I_e`. The notation
item in Section 0 is accurate.

**T6 (Ruozzi–Tatikonda). Adopted in a better form than suggested.** I fetched
`export.arxiv.org/abs/1002.3239`. The abstract contains both quoted phrases:

- "a combinatorial characterization of these optima based on graph covers";
- "This limitation of convergent and correct message-passing schemes is characterized by graph covers".

It also contains "can be too restrictive in both theory and practice". The dates are
v1 17 Feb 2010 and v3 1 Dec 2012. The note's four-point summary is accurate. The
round-1 suggestion covered only the second use of graph covers, so the reviser's
choice is justified.

**O1 (Corollary 3.3). Adopted and correctly sharpened.**

- *Source of the leaf inequality.* Lemma 1.4 of [D] with the Theorem 2.5 hypothesis gives, for `x in E(eta)`, leaves `B_t ∋ x_{V_t}` with `alpha sum_t sum_{i in K_t} a_i^{B_t}(x) <= eps + eta`. All terms are nonnegative, so `alpha a_i^{B_t}(x) <= eps + eta` for each `i in K_t`.
- *One coordinate.* [C], Section 1.1 gives `a_i >= d_i^2`, where `d_i = min(y_i - l_i, u_i - y_i)`. So `x_i` lies in `[lo, lo + l_a] ∪ [hi - l_a, hi]`. Hence `2 |Leaves_t|` intervals of length `l_a` suffice, and each is covered by `ceil(sqrt(M_e/alpha)/2)` intervals of length `l_c`.
- *Summing.* The size in Definition 1.2 is at least the sum of `|Leaves_t|` over the non-root bags, and `2 ceil(x/2) <= x + 2`.
- *"What this settles".* The claim "`O(|T| log) (sqrt(M/alpha) + 2)` times the size of a smallest certificate" is right. The additive terms `n` and `8n sum_e J'_e` are absorbed because every bag has at least one leaf, so `N_dec >= n + 1`.

**Logs that were only reread.** No script other than the three new or changed ones
was modified after round 1. The file timestamps agree: `check_bd_coarsening.py`
16:44, `check_prop4.py` 16:43, `path_cells.py` 15:57, and the three new or changed
scripts 17:21–17:22, each before its log. The round-1 reviewer reran the other
scripts, and their outputs were identical to the logs.

## 2. Nothing strengthened without proof

The revision states that only Lemma 2 and Corollary 3.3 were strengthened, and that
Proposition 5's condition was corrected. That matches the text. The sharper
Theorem 3 constants appear only as a labelled sketch in four places: Summary item 3,
the remark after Theorem 3, "What this settles" and Section 9. The novelty wording
for the sharp Lemma 2 is qualified: "I did not find this statement or its sharp
constants. No new search was run in revision round 2."

## 3. Remaining trivial points (optional)

1. **Summary, "Numerical checks", Lemma 2 bullet; Section 10 round-2 table.** The
   Summary says the families "come within a ratio of `0.999998` of it for every
   tested `(w(c), M, h)`". The `(W, M, h) = (0.05, 2, 0.4)` case gives `0.999995` at
   `delta = 1e-6`. Section 7.2 gives the correct range, `0.999995–0.999998`. The
   Section 10 row, "ratio up to `0.999998` for all five", has the same ambiguity. Use
   `0.999995` in both places, or give the range.
2. **Section 7.2 and the docstring of `check_kink_sharp_lp.py`: "so the interpolant
   stays below `M s^2`".** The script sets `bounds[m] = (-W, -W)`, which replaces the
   bound `phi(0) <= -M ds^2/4`. When `W < M ds^2/4`, the LP optimum can exceed
   `M s^2` between grid points. By my check (`lp_interpolant_check.py`), this happens
   in 4 of the 18 runs:
   - `W = 0` at `m = 8, 64, 512`, by `2.2e-3`, `3.4e-5` and `5.4e-7`;
   - `(W, M, h) = (0.01, 5, 1)` at `m = 8`, by `5.1e-3`.

   No conclusion changes. The LP still stays below the bound on this slightly larger
   set, and the explicit family proves sharpness. Restrict the sentence, or impose the
   bound only where it is compatible (for example, report `W = 0` separately).
3. **Section 5, "`psi_1` and `psi_2` are nonzero multiples of `s1^2` and `s2^2`,
   so `bd` refines near 0" (also the T2 revision entry).** Being a nonzero multiple
   of `s^2` is not enough by itself. `bd` refines because the whole sliver
   `psi_e ± w_e/4` is strictly curved on one side:
   - edge 1: `[-2 beta s1^2, (kappa beta/(2(kappa + beta)) - beta) s1^2]`, both coefficients negative;
   - edge 2: `[(3 beta/2 - beta kappa/(2 beta + kappa)) s2^2, 2 beta s2^2]`, both coefficients positive (the first exceeds `beta/2`).

   So no affine function fits in the sliver near 0. The conclusion holds for all
   `kappa >= 2 beta`, and `check_prop4.py` confirms that `bd` refines. Only the stated
   reason is incomplete.

One optional wording point: "The slope condition is needed" (Summary item 6 and the
heading of the Section 6 paragraph) is supported in the sense that the cell
condition alone is not sufficient. The example does not show that this particular
slope condition is necessary. "A condition on the slopes is needed" would be
exact.

## 4. Checks run

My scripts are in `reviews/covering-upper-half-confirm-r2-checks/` and my logs in its
`logs/` subfolder. The note's scripts were run from
`theory-decomposition/covering/`, with output written to my `logs/` folder. All runs
were single-threaded. These are targeted checks only: no project-wide verification
was run, and no CI result is reported here.

| Command | Log | Result |
|---|---|---|
| `python3 check_prop5_slopes.py` (note's script) | `rerun_check_prop5_slopes.log` | identical to the author's log; exit 0 |
| `python3 check_kink_concentration.py` (note's script) | `rerun_check_kink_concentration.log` | identical to the author's log; its first 15 lines equal the round-1 rerun; exit 0 |
| `python3 check_kink_sharp_lp.py` (note's script) | `rerun_check_kink_sharp_lp.log` | identical to the author's log; exit 0 |
| `python3 indep_lemma2_sharp.py` (my code, 13 s) | `indep_lemma2_sharp.log` | 20,000 random convex `phi`: max ratio 0.935; differential evolution: sup approaches 1 from below (largest `1 - 9.1e-13`); `(3.9, 4)` and `(4, 3.9)` violated; exit 0 |
| `python3 indep_prop5_n2.py` (my code, 5 s) | `indep_prop5_n2.log` | `n = 2`, three instances, `eps = 1e-2, 1e-3, 1e-4`: balanced brackets `<= 3.1e-6`; gap 0 (balanced), `<= 0.49964 eps` (extreme allowed slopes), `<= 0.476 eps` (random allowed slopes); constant minorants up to `18.2 eps` on tilted instances; exit 0 |
| `python3 lp_interpolant_check.py` (my code) | `lp_interpolant_check.log` | LP values equal the note's; the interpolant exceeds `M s^2` in 4 of 18 runs, by up to `5.1e-3` (item 3.2) |
| `curl export.arxiv.org/abs/1002.3239` | none | abstract and dates as quoted in Section 8 |

Checked by hand:

- the Lemma 2 proof and both cases of the sharpness family;
- the kink remark;
- the `(4, 4)` sketch after Theorem 3;
- the Proposition 5 proof with the slope clause, and the `n = 1` counterexample;
- Corollary 3.3 against Lemma 1.4 and Theorem 2.5 of [D] and Section 1.1 of [C];
- the reduced-band width in Section 5;
- the sliver coefficients of Proposition 4;
- the log figures for T3 and T4.

Scope: my `n = 2` test uses quadratic instances with interior partial minimizers, so
all value functions are exact quadratics. It tests Proposition 5 end to end,
including maximal intercepts, but not bag relaxation errors. The round-1 review
tested those through Lemma 1' directly.

## 5. Literature

I checked only the arXiv abstract page of Ruozzi–Tatikonda (arXiv:1002.3239), to
confirm the revised paraphrase. I ran no novelty searches. The note's novelty
statements remain qualified, and the revision did not strengthen them.
