# Review r3 of the minor-sets note (confirmation round 3)

Reviewer: independent research agent. Date: 2026-10-02. Object: [`../note.md`](../note.md) as
revised on 2026-10-02 after [review r2](review-r2.md), plus the new and changed code
(`code/certify_embed_brackets.py`, `code/analyze.py`, the `code/minor_core.py` docstring), the new
logs (`logs/certify_embed_brackets.log`, `logs/analysis.log`, `logs/rerun_r2/`) and the author's
revision summary. "Reviewed" means checked by another research agent, not journal peer review. My
code is in [`r3-code/`](r3-code/) and its outputs are in [`r3-logs/`](r3-logs/). My scripts import
none of the stream's code.

**Verdict: minor fixes.** The r2 minor issue is fixed on the bilinear side, and the five optional
items are handled correctly. Every new number I checked reproduces: I recomputed the new exact
brackets with my own code and the new statistics with my own implementation. No major issue.

One minor issue remains, and it is the mirror image of the r2 issue. The rewritten headline now
says "**the two** certified full-dimensional minor instances". The note certifies a third one,
instance B (Section 6), whose orbit ratio, at least `0.9219403`, is *not* below the bilinear
second instance's `0.8347772`. So the headline comparison is still selective, now on the minor
side, and it contradicts the note's own Limits section, which lists A, B and S1 as exactly
certified.

## 1. Status of the r2 issues

| r2 issue | Status | Evidence |
| --- | --- | --- |
| Minor 1: the bilinear list omits the sfree second rational instance; the sfree values are numerical | **Fixed on the bilinear side**; a new selectivity on the minor side (Section 3, minor issue 1) | The Summary "Answer" and item 3, Section 9 and the 10.1 table now list `0.835`, `0.975` and `0.984`. The new script gives exact brackets for all three embedded instances. Its log reproduces byte for byte, and I confirmed each bracket independently (Section 2). The transcribed data match sfree Theorem 14, §8.5 and Proposition 16 exactly. Corollary 7 identifies the orbit bound of the embedded corner with sfree's family (A), `{C_F ∩ H : det F > 0}` (sfree §8.1). So the brackets are also exact brackets of sfree's `z_A`, as the note says. The rounding remarks in Section 9(b) are correct: the first and third brackets fix the five decimals `0.97539` and `0.98385`. The second bracket fixes four decimals (`0.8347663 → 0.83477`, `0.8347772 → 0.83478`). |
| Optional 1: S1 cosine `0.010` → `0.011` | **Fixed** | Exact `∇det(t*)·(v − t*) = 9/2, 1/8, 1, 1/2`; cosines `0.088235, 0.010525, 0.036711, 0.016769` (my inline check). Theorem 9 and the paragraph after it now say `0.011` and `0.011`–`0.088`. |
| Optional 2: "differ only in the fourth decimal" | **Fixed** | My parser of the three logs gives largest interval-end differences `0.00130` (r1, 4×4 max-margin) and `0.00100` (r2, 4×4 point rule), as the note now says. The r2 review's "at most `0.0005`" was indeed too low (`−0.050798` against `−0.0498`). |
| Optional 3: separate typical corner from mean; Wilcoxon and Bonferroni | **Fixed** | `analyze.py` reruns to a byte-identical `analysis.log`. My own implementation (Section 2) reproduces every Wilcoxon p-value, every sign-test p-value and every factor-8 adjustment in the table. The note's side claims also hold: there is exactly one zero difference per comparison (trial 50 on 3×3, trial 85 on 4×4); there are no tied `|d|`; scipy's default is the normal approximation without continuity correction; and the exact test differs by at most `0.0029` ("within 0.003"). The typical-corner and mean statements in Section 7.2 and Summary item 6 follow from the table. Small wording points are in optional item 2. |
| Optional 4: multiplier margins numerical (Summary item 5) | **Fixed** | Item 5 now says that the multiplier margins are computed numerically and the others exactly. This matches Section 7.3. |
| Optional 5: `minor_core.py` docstring | **Fixed** | `git diff` shows "four distinct indices (so no entry of the minor is diagonal)". The other changes in that file are the round-1 theorem renumbering. All 21 scripts compile. The S1 certificate imports `minor_core.py`, and its rerun log `logs/rerun_r2/certify_supp1_full.log` is byte-identical to `logs/certify_supp1_full.log`. |

The new Sections 10.2 and 11.3 describe the revision accurately. The only change to `analysis.log`
since the commit is the 10-line paired-statistics block (`git diff`). The two modified files under
`reviews/r1-logs/` carry r1-reviewer timestamps (19:10–19:12, before round 2) and add only a cvxpy
warning and extra lines. The author did not touch them in this round.

## 2. Independent recomputations

All checks were targeted. I ran no project-wide checks and did not consult CI.

- **Embedded sfree brackets, exact** (`r3-code/r3_embed.py`, my own code; `r3-logs/r3_embed.log`,
  ALL PASS). For each instance, embedded as `M = [[w, x], [y, 1]]`:
  - I enumerated faces in affine coordinates with sympy and found `min q = 0` on `T*`, attained
    only at `t*`. The script also reports singular faces instead of skipping them, and none has
    a critical set with value `≤ 0`.
  - `t*` has barycentric weights `(0, 1/2, 1/2, 0)`, `(0, 6/7, 1/7, 0)` and `(0, 1, 0, 0)`, so
    it has cost 1 and `z_K = 1`. The author's script hard-codes `t*` and does not check this
    step (optional item 1).
  - For the lower ends I solved my own SDP and rounded `F` to rationals. Exactly checked:
    `sym(F^T M(s̄)) ≻ 0` and `sym(F^T M(v)) ⪰ 0` on the vertices of `T_{z_lo}`.
  - For the upper ends I solved my own SDP, rounded the `Y_v`, projected them exactly onto
    `{Σ_v M(v) Y_v = 0}`, and checked exactly that each `Y_v` is positive definite at `z_up`.
  - All six bracket ends of the note hold: `[0.9753853, 0.9753864]`, `[0.8347663, 0.8347772]`,
    `[0.9838465, 0.9838468]`. At the upper ends the SDP margins are only `4·10^-8`, `7·10^-8`
    and `1·10^-8`, so the brackets are tight.
- **Rerun of the author's script.** `timeout 1200 python3 certify_embed_brackets.py` gives a log
  byte-identical to `logs/certify_embed_brackets.log` (ALL PASS, 8.3 s).
- **LP statistics** (`r3-code/r3_lpstats.py`; `r3-logs/r3_lpstats.log`). The script computes:
  - Wilcoxon p-values: my own normal approximation with zeros dropped and the tie-corrected
    variance, scipy's default, and scipy's exact test on the nonzero differences;
  - sign-test p-values from my own binomial sum;
  - Bonferroni adjustments with factor 8 and, as a sensitivity check, factor 16;
  - the interval-end differences against both earlier reviews.

  The values are as in Section 1. With factor 16, which covers picking the better of two tests
  per comparison, the nearest-to-SCIP typical-corner claim still holds: 3×3 Wilcoxon `0.018`,
  4×4 sign test `0.036`. The 3×3 max-margin Wilcoxon becomes `0.049`.
- **Rerun of `analyze.py`.** The output is byte-identical to `logs/analysis.log`.
- **Proofs.** I re-read the proofs of Proposition 1 (coordinates, rotation action, polar
  uniqueness), Proposition 3(1) (the `G = cI` step), Proposition 5 (radical and signature
  argument, `s̄ ∈ span P_J`, the tangent-edge part), Theorem 8(4), Proposition 10,
  Proposition 11 (all four step-length computations and the bound `((16 + 2√73)/3)√δ`), and
  Corollary 7 against sfree §8.1. I found no gap. None of these proofs changed in this round.

## 3. Issues

### Major

None.

### Minor

1. **The headline comparison is still selective, now on the minor side.** The Summary "Answer",
   Section 9 (first bullet) and the author's result list say: "The two certified full-dimensional
   minor instances have larger gaps than all three certified bilinear instances of the sfree
   note: orbit ratios `0.45` and `0.78` against `0.835`, `0.975` and `0.984`."

   The note certifies a third full-dimensional minor instance, instance B (Section 6;
   `logs/certify_cex_B.log`, ALL PASS, `det[p_1 … p_4] = 1005/4 ≠ 0`). Its exact orbit bracket is
   `[0.9219403, 0.9219593]`, so its gap of about 7.8% is *smaller* than that of the bilinear
   second instance (ratio at most `0.8347772`, a gap of at least 16.5%). The note's own Limits
   section says "Exact certificates exist for instances A, B, S1, …". Section 7 also certifies
   12 rounded adversarial corners and 12 random misses exactly. Some of them, with ratios
   `0.91850`, `0.84583` and most random misses, have smaller gaps than `0.835`, and others have
   much larger ones.

   So "the two certified full-dimensional minor instances" is a miscount. The comparison holds
   only for the two instances picked as the worst of their searches. The statement in the
   results list, "the statement concerns these instances only", is right in substance, but the
   note's sentence does not say which instances or that they were picked. This is the same kind
   of selectivity that r2 minor issue 1 raised for the bilinear side. The round-3 revision gave
   this sentence more weight ("Both sides are exact", "which the script checks"), which makes the
   omission more visible.

   Fix (wording only): for example, "Instances A and S1 (Theorems 8 and 9, the worst instances of
   the two searches) have larger gaps than all three certified bilinear instances … (instance B,
   also certified, has orbit ratio `0.922`, between the bilinear values `0.835` and `0.975`)".
   Make the same change in Section 9, and in the 10.2 row if it is restated there.

### Optional

1. `certify_embed_brackets.py` prints "(so `z_K = 1`)" after checking that `min det = 0` on `T*`
   only at the hard-coded `t*`. It does not check that `t*` has cost 1, that is, that `t*` lies
   on the far face. The fact is true (my barycentric check above), and sfree proves it, but the
   script's conclusion does not follow from its printed checks alone. `certify_cex.py`, by
   contrast, checks `t0 = μ v_1 + (1 − μ) v_2`. One exact line would close this. Unlike
   `certify_cex_A.log`, the new log also does not print the certificates (`F` and `Y_v`).
   Printing them would let a reader check the brackets without rerunning the SDP solvers.
2. Section 7.2 says the Wilcoxon test is used "only as supporting evidence about the typical
   corner", and Limits calls it "only indicative". But for the 3×3 programs the typical-corner
   statements rest on it alone after adjustment: the nearest-to-SCIP gain has sign test `0.43`
   adjusted, and the max-margin loss has sign test `0.13` adjusted. It would be more accurate to
   say this directly, for example "on 3×3 this rests on the Wilcoxon test, with the symmetry
   caveat above".

   Choosing, for each size, whichever of the two tests stays below 0.05 is a mild second
   multiplicity. The nearest-to-SCIP conclusion survives a factor of 16 (`0.018`, `0.036`), so
   the note could say so. The 3×3 max-margin Wilcoxon becomes `0.049` under that factor.

## 4. Assessment of the main claims

| Claim | Label | Finding |
| --- | --- | --- |
| SCIP's minor set is `C_U` (Proposition 1); the `nlhdlr_quadratic` part is source reading | proved / source reading | Correct; unchanged since r2 (r2 smoke test 13/13) |
| Orbit, point-rule and BCM families; support; pencil (Lemma 2, Propositions 3–5, Lemma 6) | proved | Correct; re-read |
| Corollary 7 and the new exact brackets of the embedded sfree instances | proved / computed exactly | Correct; brackets independently re-certified (Section 2) |
| Instances A, B, S1 (Theorems 8, 9; instance B) | computed exactly | Unchanged since r2's independent re-verification; the S1 rerun is byte-identical |
| Propositions 10, 11 | proved | Correct; re-read |
| "The two certified full-dimensional minor instances have larger gaps than all three certified bilinear instances" | computed exactly | True for A and S1, but the count is wrong and the comparison is selective: instance B (`≥ 0.9219`) does not beat the bilinear `0.835` (minor issue 1) |
| LP statistics (Section 7.2, Summary item 6) | numerical | Independently reproduced; conclusions follow; small wording point (optional 2) |
| Adversarial and random corners (Sections 7.1, 7.3) | numerical, certified after rounding | Unchanged; r2 re-verified the margins |
| Novelty | qualified | Appropriately hedged; unchanged |
| Solver relevance | low, mostly negative | Fair; no overclaim |
| Process hygiene | stated | Accurate; no stream process running at the start or end of this review |

## 5. Checks actually run (by this reviewer)

I ran everything from `research-20261001/minor-sets/` with `OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`, every Python job under `timeout`, and at most
one job at a time. One job ran in the background: the author's bracket script. It finished (exit
0) before I continued. The load average was 73–105 on 36 cores. All checks are targeted; I did not
consult CI.

| Command | Outcome |
| --- | --- |
| `/proc/*/cwd` scan (start) | no process in the stream directory |
| `git status` / `git diff` on the stream directory (`analyze.py`, `minor_core.py`, `analysis.log`, `reviews/r1-logs/`) | changes as described in Section 10.2; the `r1-logs` changes predate round 2 |
| `cd code; timeout 1200 python3 certify_embed_brackets.py > ../reviews/r3-logs/rerun_certify_embed_brackets.log` | ALL PASS, 8.3 s; `diff` with `logs/certify_embed_brackets.log`: identical |
| `cd reviews/r3-code; timeout 900 python3 r3_embed.py > ../r3-logs/r3_embed.log` | ALL PASS: `z_K = 1` (unique `t*`, cost 1), and both bracket ends exactly certified for all three embedded instances; empty stderr |
| `cd code; timeout 300 python3 analyze.py > ../reviews/r3-logs/rerun_analysis.log` | identical to `logs/analysis.log`; empty stderr |
| `cd reviews/r3-code; timeout 300 python3 r3_lpstats.py ../../logs .. > ../r3-logs/r3_lpstats.log` | Wilcoxon (own approximation = scipy default; exact within `0.0029`), sign tests and the ×8 adjustments as in the note; one zero difference per comparison; ×16 sensitivity as in Section 2; interval differences `0.00130` (r1), `0.00100` (r2) |
| `diff logs/certify_supp1_full.log logs/rerun_r2/certify_supp1_full.log` | identical |
| `timeout 120 python3 -c "py_compile …"` over `code/*.py` (bytecode to `/tmp`, then deleted) | 21 files, no compile error |
| Inline `timeout 60 python3 -c …` (exact S1 products and cosines) | `9/2, 1/8, 1, 1/2`; `0.088235, 0.010525, 0.036711, 0.016769` |
| `sed`/`grep` over sfree §8.1 (family (A)), §8.5 (Theorem 14, second instance), Proposition 16, Summary | data in `certify_embed_brackets.py` match; family (A) = `{C_F ∩ H : det F > 0}`; sfree values numerical, strictness certified; sfree certified no other bilinear instance |
| `grep` over `note.md` for "certified", "instance B", old wording | instance B certified (Section 6, Limits) but omitted from the headline count (minor issue 1); old wording survives only in the historical tables of Section 10 |
| `/proc/*/cwd` scan and `ps` (end) | no process in the stream directory; none of my jobs running |

Not rerun: the SCIP fidelity check, the experiments of Sections 7.1–7.4, and the certificates of
instances A and B. Their code is unchanged apart from docstrings (`exact_tools.py` is unmodified),
and r1 and r2 reproduced them.
