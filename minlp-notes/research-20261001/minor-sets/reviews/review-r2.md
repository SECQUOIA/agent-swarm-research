# Review r2 of the minor-sets note (confirmation round)

Reviewer: independent research agent. Date: 2026-10-02. Object: [`../note.md`](../note.md) as
revised on 2026-10-02 after [review r1](review-r1.md), the changed code in [`../code/`](../code/),
the new logs, and the author's revision summary. "Reviewed" means checked by another research
agent, not journal peer review. My code is in [`r2-code/`](r2-code/) and its outputs are in
[`r2-logs/`](r2-logs/). None of my scripts imports the stream's code, apart from the one SCIP
smoke test, which reruns the stream's own script.

**Verdict: minor fixes.** Four of the five r1 minor issues are fixed correctly, and all six optional
items are handled. One minor issue remains, a residue of r1 minor issue 2: the headline comparison
with the bilinear case lists only two of the three certified bilinear instances. I found no major
issue. All proofs check out under their stated hypotheses. Every certificate and statistic I
recomputed with my own code agrees with the note, and no stream process is running.

## 1. Status of the r1 issues

| r1 issue | Status | Evidence |
| --- | --- | --- |
| Minor 1: no process-hygiene statement | **Fixed** | Section 11.3 now says the 2026-10-01 runs had no `timeout`, and lists how each was bounded. I checked each fact against the code. `exp_random.py` needed 595, 670 and 560 draws (its `.out` files). `adversarial.py` has `maxiter=700`. `exp_lp.py` and `test_core.py` set `limits/time` 60. `scip_probe.py` and `scip_fidelity.py` set `limits/nodes` 1, and `scip_fidelity.py` sets `maxroundsroot` 5. `minor_core.FamilySolver.best` uses a fixed number of iterations. jsonl records are flushed one at a time. Limits has a matching line. No stream process was running when I started or when I finished. |
| Minor 2: "with larger gaps" and the bilinear comparison | **Partly fixed** | The general claim is withdrawn. The new Section 7.3 paragraph describes the sfree search accurately: I checked `sfree/code/adversarial_ratio.py` (same grazing formula, `q(s̄) > 1e-6`, no other margin) and sfree §8.6 (`0.4526` at vertex violation `≈ 9·10^-4`; `0.028` at `≈ 10^-7`). One problem remains in the headline and in Section 9; see Section 3, minor issue 1. |
| Minor 3: Summary item 4 drops the hypothesis of Proposition 5 | **Fixed** | Summary item 4 now states the hypothesis. The duplicated-ray example after Proposition 5 is correct, and sfree Lemma 3 does give a minimizer with linearly independent projected rays when the minimum is attained. |
| Minor 4: LP comparisons without uncertainty | **Fixed** | The new table reproduces (Section 2). The rounding is correct even in the borderline cells: with the author's bootstrap at six decimals, `+0.022495`, `−0.020496` and `+0.014508`. The conclusions now follow the data. Small wording points are in optional item 3. |
| Minor 5: Proposition 1 includes untested `nlhdlr_quadratic` | **Fixed** | Summary item 1, Section 2, the "Scope of proved" paragraph, Limits and open question 6 all say "source reading, not tested". I re-read `nlhdlr_quadratic.c`. Line 3406 sets `auxvar = NULL` for a constraint root, and lines 1066–1071 define Case 1 as `w = 0, κ = 0`. The reading is right, and so is the label. |
| Optional 1–6 | **Handled** | The docstring theorem numbers now match (diff checked). `certify_ratio.py` no longer promises margins, and `rounded_margins.py` is new (checked in Section 2). "Four distinct indices" is used in the note. Section 8 is reworded correctly: `−A = Σ μ_i g_i g_i^T` gives at most two inequalities `g_i^T X g_i ≥ 0`. The "bisection upper" remark matches `certify_cex_A.log` (`0.4495352780` against `0.4495357065`). The Muñoz–Serrano locator is right: arXiv:1911.12341v2 Theorem 7 is cited by Muñoz–Paat–Serrano as `[24, Theorem 2.1]`, and `[24]` is Math. Program. 192. |

The new header line about commit `c3514f03` is correct (`git log` on the stream directory). The
changed code differs only in comments and docstrings, except for the new `paired()` function in
`analyze.py` and the new `rounded_margins.py` (checked with `git diff`). The regenerated
`analysis.log` differs from the committed one only by the 10 added lines.

## 2. Independent recomputations

All checks are targeted. I ran no project-wide checks and did not consult CI.

- **Instances A and S1, exact** (`r2_exact.py`). I typed the data in from the note text.
  - My own exact face enumeration finds `min det = 0` on `T*`, attained only at `t*`. No face is
    singular.
  - `λ* = (2/3, 1/3, 0, 0)` with `ν = (0, 0, 3/2, 5/2)`, `σ = 1/6` (A), and `λ* = e_1` with
    `ν = (0, 1/36, 2/9, 1/9)`, `σ = 2/9` (S1).
  - Instance A: `∇det(t*)·d = 0` and `det d = 72`. My own sympy computation gives exactly the
    note's five `κ`-intervals, and their intersection is empty.
  - I parsed the dual certificates at `9/20` (A) and `779/1000` (S1) from the logs and re-verified
    them exactly: each `Y_V` is symmetric positive definite and `Σ_V V Y_V = 0`. The small `z = 1`
    certificate printed in the note text also verifies.
  - My own SDP without preconditioning, rounded to rationals, gives an `F` whose set contains
    `T_z` exactly at `z = 0.4495347` (A) and `z = 0.7780998` (S1). These are the note's lower
    bracket ends.
  - SCIP's value, computed by bisection on the *literal* Case-1 formula of Section 2 (not on
    `C_U`), is `0.135800286706` (A) and `0.31214177124` (S1). Both agree with the note's `C_U`
    values to 12 digits, which is a further check of Proposition 1.
  - S1 transversality: `∇det(t*)·(v − t*) = 9/2, 1/8, 1, 1/2`. The cosines are
    `0.0882, 0.0105, 0.0367, 0.0168`. The second rounds to `0.011`, not `0.010` (optional item 1).
- **LP paired statistics** (`r2_lpstats.py`): my own bootstrap (seed 12345, 20000 resamples),
  `scipy.stats.binomtest` and a Wilcoxon signed-rank test. Means, medians, better/worse counts and
  sign-test p-values equal the note's table. My intervals differ from the note's by at most
  `0.0005`. The worst 10% of corners carry 65% (3×3) and 71% (4×4) of the max-margin set's total
  loss. Without them, the mean difference is still negative (`−0.030`, `−0.021`). So "dominated by
  a minority of corners with large losses" is a fair summary.
- **Rounded adversarial corners** (`r2_margins.py`). I rounded each corner to denominator `10^4`,
  as `certify_ratio.py` does.
  - I computed the grazing, second-order and apex margins exactly from the definitions in the
    `adversarial.py` docstring.
  - I computed `ν_3, ν_4` from my own 40-digit minimizer of the rays-{1, 2} problem.
  - All twelve margin vectors equal those in `rounded_margins_adv_*.log`. The smallest margins
    are `0.010014`–`0.010874` for the 1% runs and `0.050083`, `0.054556` for the 5% runs.
  - The rays-{1, 2} cost is within a factor `1.00000101` of the exact lower bound `zK_lower_exact`
    in `certify_ratio_adv_*.log`. Single rays and the other pairs cost at least `1.0017`. This
    confirms support {1, 2} for every rounded corner.
- **Section 7.3 numbers.** The ten final ratios, the exact ratio bounds (`0.20033` … `0.91850`,
  and `0.32638`, `0.84583`), the active margins (grazing in the two best runs, apex in both 5%
  runs) and the invalid starts all match the jsonl files and the logs.
- **SCIP fidelity smoke test with a new seed** (`scip_fidelity.py 2 4`): 13 of 13 applied
  `interminor` cuts matched the predicted `C_U` cuts, with largest coefficient difference
  `2.2·10^-16`. One model was skipped because it had no separation round, as the note describes.
- **Reruns of the revision.** `rerun_r1/certify_cex_A.log`, `certify_supp1_full.log` and
  `scaling_example.log` are byte-identical to the original logs. `embed_check.log` differs only by
  one cvxpy warning, as stated.
- **Proofs.** I re-read every proof, including the parts r1 checked. I re-derived the following,
  with no gap found:
  - Proposition 5: both cases of sfree Theorem 4 with `ρ = 3`, the radical and signature argument
    on `T`, and `s̄ ∈ span P_J`.
  - Lemma 6, the `C_F = C_{F'}` argument of Proposition 3(1), and Lemma 2(2).
  - Proposition 10 and the four bounds of Proposition 11, including
    `((16 + 2√73)/3)√δ` for `δ ≤ 1/4`.
  - The robustness argument of Theorem 8(4).
  - The duplicate-minor claim of Section 2: transposition gives polar factor `U^T`, and
    `sym(M U^T) ⪰ 0 ⟺ sym(U^T M) ⪰ 0`.

## 3. Issues

### Major

None.

### Minor

1. **The headline comparison with the bilinear case is selective.** The Summary "Answer", Section 9
   and the Section 10 table say: "the certified full-dimensional minor instances have larger gaps
   than the certified bilinear instances of the sfree note (orbit ratios `0.45` and `0.78` against
   `0.975` and `0.984`)". The sfree note certifies a third bilinear instance, its "second rational
   instance" (sfree §8.5, `z_A = 0.83477`, a 16.5% gap). Its strictness is certified exactly for
   family (A), the family that corresponds to the minor orbit by Corollary 7. This note itself
   lists it in Corollary 7. Leaving it out makes the contrast look larger than it is: the smallest
   certified bilinear ratio is `0.835`, not `0.975`.

   The sfree values `0.97539`, `0.83477` and `0.98385` are also numerical. sfree certifies only the
   strict inequality `z_A < z_K`, with floating-point lower bounds from explicit sets. The minor
   values, by contrast, are exact brackets. The narrower claim stays true with all three instances
   (`0.45, 0.78 < 0.835`), so only the wording needs to change.

   Fix: write "against `0.835`, `0.975` and `0.984` (sfree numerical values; there the strict gap
   is certified)" in the Summary, Section 9 and the Section 10 table.

### Optional

1. Theorem 9 and the paragraph after it give the second cosine as `0.010`. It is
   `0.010525 → 0.011`, so the range should read `0.011`–`0.088`.
2. Section 7.2 says the reviewer's intervals "differ only in the fourth decimal". They differ by up
   to `0.0013`: `−0.0247` against `−0.0260` for the 4×4 max-margin upper end, and `−0.0450`
   against `−0.0439` for the 3×3 point-rule lower end. Write "differ by at most 0.0013 (different
   resamples)".
3. Statistics wording in Section 7.2 and Summary item 6. For the nearest-to-SCIP tie-break on 4×4,
   the sign test (`p = 0.0022`) survives a Bonferroni adjustment over the eight comparisons
   (`0.018`). A Wilcoxon signed-rank test gives `p = 0.001` (3×3) and `0.012` (4×4). So "better in
   more corners than worse" is fairly well supported. Only the *mean* gain is not established on
   4×4. In the other direction, the max-margin set on 4×4 has a sign-test `p = 0.70` but a
   Wilcoxon `p = 0.042` against it. The note's "suggested, not established" is conservative and
   not an overclaim. Separating "typical corner" from "mean" would be more precise.
4. Summary item 5 says the rounded 0.200 corner "still has all margins at least 1%" right after
   "certified exactly". The multiplier margins are numerical, as Section 7.3 says. For this corner
   they are 2.30 and 2.50, so nothing depends on it. A parenthetical "(multiplier margins
   numerical)" would avoid a misreading.
5. The `minor_core.py` docstring still says "four distinct entries". r1 optional item 3 was applied
   to the note only.

## 4. Assessment of the main claims

| Claim | Label | Finding |
| --- | --- | --- |
| SCIP's minor set is `C_U` (Proposition 1); `nlhdlr_quadratic` part is source reading | proved / source reading | Correct; labels now right; smoke test with a new seed 13/13 |
| Orbit, point-rule and BCM families (Lemma 2, Propositions 3, 4) | proved | Correct |
| Support statement (Proposition 5, Summary item 4) | proved | Correct with the hypothesis, which the Summary now states |
| Lemma 6, Corollary 7 | proved | Correct |
| Instance A, instance S1 (Theorems 8, 9) | computed exactly | Independently re-verified (my face enumeration, `κ`-intervals, dual and primal certificates, literal SCIP formula) |
| Propositions 10, 11 | proved | Correct |
| Random and LP corners (Sections 7.1, 7.2) | numerical | Statistics reproduced independently; wording now matches the data |
| Adversarial 0.200 at 1% margins, rounded margins (Section 7.3) | numerical, certified after rounding | Margins re-verified independently; the comparison with the bilinear search is now correctly withdrawn |
| Larger gaps than the certified bilinear instances (Summary, Section 9) | computed exactly | True, but the list of bilinear instances is incomplete (minor issue 1) |
| Novelty | qualified | Appropriately hedged |
| Solver relevance | low, negative | Fair; no overclaim |
| Process hygiene | stated | Accurate; no process left |

## 5. Checks actually run (by this reviewer)

I ran everything from `research-20261001/minor-sets/` under `timeout`, at most 2 processes at a
time, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`. The machine had load average about 127 on
36 cores. All checks are targeted; I did not consult CI.

| Command | Outcome |
| --- | --- |
| `git log` / `git diff --stat` / `git diff --word-diff` on the stream directory | Changes as described in Section 10 of the note; code changes are docstrings plus `paired()` and `rounded_margins.py`; `analysis.log` has only the 10 added lines |
| `diff logs/X logs/rerun_r1/X` for `certify_cex_A`, `certify_supp1_full`, `scaling_example`, `embed_check` | Identical apart from one cvxpy warning in `embed_check` |
| `cd reviews/r2-code; timeout 900 python3 r2_exact.py ../../logs` | `r2-logs/r2_exact.log`: ALL PASS (A and S1 as in Section 2); empty stderr |
| `cd reviews/r2-code; timeout 300 python3 r2_lpstats.py ../../logs` | `r2-logs/r2_lpstats.log`: statistics as in Section 2 |
| `cd reviews/r2-code; timeout 900 python3 r2_margins.py ../../logs` | `r2-logs/r2_margins.log`: all twelve rounded corners' margins equal the stream's logs; support {1, 2} confirmed |
| `cd code; timeout 600 python3 scip_fidelity.py 2 4` | `r2-logs/r2_scip_fidelity_smoke.log`: 13 of 13 applied cuts matched, worst coefficient difference `2.2e-16` |
| Inline `timeout 120 python3 -c ...` (author's bootstrap, seed 0, six decimals) | Every rounded value in the Section 7.2 table is correct |
| Inline `timeout 60 python3 -c ...` (S1 cosine) | `0.010525` (optional item 1) |
| `grep`/`sed` over `exp_random.py`, `exp_lp.py`, `test_core.py`, `scip_probe.py`, `scip_fidelity.py`, `adversarial.py`, `minor_core.py`, `logs/exp_random_*.out` | Process-hygiene facts of Section 11.3 confirmed |
| `sed`/`grep` over sfree §8.5–8.6, sfree Summary, Lemma 3, Theorem 4, `sfree/code/adversarial_ratio.py` | Section 7.3 description accurate; the sfree certified instances are Theorem 14, the second rational instance (0.83477) and Proposition 16 (minor issue 1) |
| `grep`/`sed` over `nlhdlr_quadratic.c` (SCIP 10.0.3, read only) | `auxvar = NULL` for a constraint root (line 3406); Case 1 is `w = 0, κ = 0` |
| `grep`/`sed` over `1911.plain.txt` and `2211.05185.plain.txt` | arXiv v2 Theorem 7 = MPS `[24, Theorem 2.1]`, `[24]` = Math. Program. 192 |
| `/proc/*/cwd` scan at the start and at the end | No process in the stream directory; all my jobs ran in the foreground and finished |

Not rerun: the full experiments of Sections 7.1–7.4. Their code is unchanged apart from
docstrings, and r1 reproduced them. Instance B was not rerun either: its certificate and log are
unchanged, and r1 re-verified it independently.
