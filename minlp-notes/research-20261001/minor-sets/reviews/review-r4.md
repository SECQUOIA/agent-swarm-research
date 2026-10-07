# Review r4 of the minor-sets note (confirmation round 4)

Reviewer: independent research agent. Date: 2026-10-03. Object: [`../note.md`](../note.md) as
revised on 2026-10-03 after [review r3](review-r3.md), the changed code
(`code/certify_embed_brackets.py`, `code/analyze.py`) and the new logs (`logs/*_rev3*`,
`logs/check_analysis_rev3.log`, `logs/process_check_rev3.log`). Scope: confirmation only. I checked
the round-3 minor issue and the two round-3 optional items, and looked for errors introduced by the
revision. I did not re-review unchanged material. "Reviewed" means checked by another research
agent, not journal peer review. My code is in [`r4-code/`](r4-code/), outputs in
[`r4-logs/`](r4-logs/). My script imports none of the stream's code.

**Verdict: verified.** The round-3 minor issue is fixed, both optional items are handled correctly,
and I found no new error. One optional wording point remains (below); it does not need another
round.

## 1. Status of the round-3 items

| r3 item | Status | Evidence |
| --- | --- | --- |
| Minor 1: headline counted "the two certified full-dimensional minor instances" and omitted certified instance B | **Fixed** | Every place that repeats the comparison now names A and S1 as the worst instances of the two rational searches and states B's bracket: Summary "Answer", Summary item 3, Section 9 (sfree bullet), the 10.1 and 10.2 rows, and 10.3. `grep` finds no remaining "two certified" wording. Section 7.4 supports "worst instances of the two rational searches": `search_cex` ratios range from `0.4495` (A); `search_supp1` worst is `0.778` (S1); A and B both come from `search_cex`. The text is consistent with Limits, which lists A, B, S1, the embedded instances and the 24 rounded corners as certified. B's bracket is correct (Section 2). The conclusion is now scoped to the selected instances A and S1, and the note says explicitly that B has a smaller gap than the bilinear second rational instance and that no uniform ordering or worst-case comparison is claimed. This is supported. |
| Optional 1: cost-one check of `t*`; print certificates | **Fixed** | The script now checks `t* = s̄ + Pλ` with `λ ≥ 0` and `w·λ = 1` exactly: `λ = (1/2, 1/2, 0)`, `(6/7, 1/7, 0)`, `(1, 0, 0)`, which match the barycentric weights found in r3. It prints the rational `F^T` and `Y_v` and exits nonzero on a failed check. I parsed the six printed certificates from `logs/certify_embed_brackets_rev3.log` and checked them with my own exact checker: all six bracket ends hold. |
| Optional 2: Wilcoxon reliance; second multiplicity | **Fixed** | Summary item 6, Section 7.2 (caveat paragraph and conclusions) and Limits now say that the 3×3 typical-corner claims rest on the Wilcoxon test alone with its symmetry caveat, and that the 4×4 nearest-to-SCIP claim rests on the sign test. The factor-16 values in `analysis_rev3.log` are right: 3×3 nearest-to-SCIP Wilcoxon `0.0180`, 4×4 sign test `0.0355`, 3×3 max-margin Wilcoxon `0.0492` (just below 0.05, as stated). The adjusted 3×3 sign test `0.1349` is correctly quoted as `0.13`. `analysis_rev3.log` differs from `analysis.log` only in the factor-16 additions and the two label lines. |

The new "Revision after review round 3" entry (Section 10.3) and the run table (Section 11.4)
describe the changes accurately. The renumbering of process hygiene to Section 11.5 is carried
through (Section 10.1 row, Limits). The `git diff` of the two scripts shows only the described
changes (cost-one check, certificate printing, exit code, the factor-16 columns and labels).

## 2. Independent checks

- **Instance B, exact** (`r4-code/r4_minor.py`, log `r4-logs/r4_minor.log`, ALL PASS).
  - `det s̄ = 29/4 > 0`; `det[p_1 … p_4] = 1005/4 ≠ 0`.
  - `z_K = 1`: exact enumeration of the critical points of `det(s̄ + Pλ)` on the relative interiors
    of all faces of `{λ ≥ 0, Σλ ≤ 1}` (sympy, rationals; no singular face occurred). The minimum is
    `0`, attained only at `t* = (0, 0, −6, −6)`, with `λ = (1/3, 2/3, 0, 0)`, cost 1. This agrees
    with `μ = 1/3` in `certify_cex_B.log`.
  - Lower end `0.9219403`: my own SDP (Clarabel) at `z = 9219403/10^7`, `F^T` rounded to
    denominators `10^10`; exactly checked `det F^T > 0`, `sym(F^T M(s̄)) ≻ 0` and
    `sym(F^T M(v)) ⪰ 0` on the vertices of `T_z`.
  - Upper end `0.9219593`: my own dual SDP at `z = 9219593/10^7`, `Y_v` rounded and projected
    exactly onto `{Σ_v M(v) Y_v = 0}`; every `Y_v` positive definite (exact). Since
    `Σ_v ⟨sym(F^T M(v)), Y_v⟩ = ⟨F, Σ_v M(v) Y_v⟩ = 0` for every `F`, no orbit set contains
    `T_z`.
  - Sharpness: at `z_orbit ± 5·10^-6` (with `z_orbit ≈ 0.9219503` from `certify_cex_B.log`) one
    of the two SDP margins is negative, so the bracket is close to tight.
  - Exact comparison: `0.8347772 < 0.9219403` and `0.9219593 < 0.9753853`, so B lies strictly
    between the bilinear second instance and sfree Theorem 14, as the note says.
- **Printed certificates of the embedded sfree instances** (same script): the six certificates in
  `logs/certify_embed_brackets_rev3.log` are valid for `[0.9753853, 0.9753864]`,
  `[0.8347663, 0.8347772]` and `[0.9838465, 0.9838468]`.
- **Reruns.** `certify_embed_brackets.py` (exit 0, ALL PASS, 6.5 s) reproduces
  `logs/certify_embed_brackets_rev3.log` byte for byte; stderr has the two cvxpy accuracy warnings
  the note mentions. `analyze.py` reproduces `logs/analysis_rev3.log` byte for byte. The r3
  reviewer script `r3_lpstats.py` reproduces `logs/lpstats_rev3_confirmation.log`. An inline
  exact binomial computation gives sign-test p-values `0.016858`, `0.054076`, `0.0022214` and the
  ×8 and ×16 values above.

## 3. Issues

### Major

None.

### Minor

None.

### Optional

1. **One-sided certificates of the 24 rounded corners.** Summary "Answer" and Section 9 say that the
   12 rounded adversarial corners and 12 rounded random misses "are also certified" and that
   their gaps are not uniformly larger than the bilinear gaps. Those certificates are one-sided
   (`z_K ≥ z_lo` and `z_orbit ≤ z_up`, so only an exact *upper* bound on the ratio;
   `logs/certify_ratio_*.log`, `logs/verify_misses.log`). Which of them has a gap smaller than a
   bilinear gap therefore rests on the numerical lower bounds from explicit sets, for example
   `0.9185` and `0.99994`. The statement is true, and B alone proves the non-uniformity exactly.
   A short clause would avoid the impression that this part is exact, for example "(exact ratio
   upper bounds; the lower bounds are numerical)". The same applies to the Limits wording
   "Exact certificates exist for … the 12 adversarial corners and the 12 random misses", which
   predates this round.
2. Cosmetic: the header line "This revision has not been independently re-reviewed" (top of the
   note and Section 10.3) becomes stale once this review is recorded.

## 4. Checks actually run (by this reviewer)

All from `research-20261001/minor-sets/` with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1`, every Python job in the foreground under `timeout`, one at a time.
Targeted checks only; no project-wide verification, no CI.

| Command | Outcome |
| --- | --- |
| `/proc/*/cwd` scan and `ps` (start) | no stream process running |
| `git diff` of `note.md`, `code/analyze.py`, `code/certify_embed_brackets.py`; `diff logs/analysis.log logs/analysis_rev3.log` | changes as described in Section 10.3; only factor-16 additions and labels in the log |
| `cd code; timeout 600 python3 certify_embed_brackets.py > ../reviews/r4-logs/rerun_certify_embed_brackets.log` | exit 0, ALL PASS; identical to `logs/certify_embed_brackets_rev3.log` |
| `cd code; timeout 300 python3 analyze.py > ../reviews/r4-logs/rerun_analysis.log` | exit 0; identical to `logs/analysis_rev3.log` |
| `cd reviews/r3-code; timeout 300 python3 r3_lpstats.py ../../logs .. > ../r4-logs/rerun_r3_lpstats.log` | exit 0; identical to `logs/lpstats_rev3_confirmation.log`; ×16 values `0.0492`, `0.0180`, `0.0355` |
| `cd reviews/r4-code; timeout 900 python3 r4_minor.py ../../logs/certify_embed_brackets_rev3.log > ../r4-logs/r4_minor.log` | exit 0, ALL PASS (B: `z_K = 1`, both bracket ends exact; six printed certificates valid). A first run failed the B upper check because of a bug in my script (float `z` in the exact projection); fixed and rerun. |
| inline `timeout 300 python3 -c` debugging the B dual SDP (imports my script) | the SDP itself was fine (margin `7.0·10^-8`); it wrote a `__pycache__` in `r4-code/`, which I deleted |
| inline `python3 -c` exact binomial sign tests | `0.016858` (×8 `0.1349`), `0.054076`, `0.0022214` (×16 `0.0355`) |
| `grep` over `note.md` for the comparison wording, B, section references | all repetitions consistent; no stale "two certified"; references to 11.4/11.5/10.3 correct |
| `head`/`tail` of `logs/certify_ratio_adv_m01_s1.log`, `logs/verify_misses.log` | rounded-corner certificates give exact ratio upper bounds only (optional item 1) |
| `/proc/*/cwd` scan (end) | no process of this stream or of mine running |
