# Review r3: stream `intersection-literature` (confirmation round 3)

Reviewer: independent research agent. I did not write the material or the
earlier reviews. Date: 2026-10-02. No partial r3 file existed before this one.

Object: the revised `note.md` (Section 12 lists the changes), the changed script
`code/check_ky_cor312_counterexample.py` and its regenerated log, and every other
passage the revision touched (the header, §4.4, §11, §12, §13, and the
renumbering).

**Verdict: verified.** Both minor issues from r2 (n1, n2) are fixed correctly.
All four optional items were applied correctly. I found no new major or minor
issue.

## Status of the r2 issues

| r2 issue | Status | What I checked |
|---|---|---|
| **n1** wrong inequality in the infinite case of Remark 4.4 | **Fixed** | §4.4 now uses `c = w/M`. I rederived the step. Since `z_K = ∞`, `X = ∅`, so every `c` is valid, and `B ∩ cone(A) = ∅`. Hence `B_1 = ∅`, `cl(B_2) = B`, no ray of `cone(A)` meets `cl(B_2)`, and `D_1 = ∅`. Every limit ray goes into `D_2`, and each such ray avoids `cl(B_2)`, as Cor. 3.12' requires. (iii) on `D_2` holds because `c = w/M > 0` (Remark 4.4 assumes `w > 0`). KY's standing assumption `0 ∉ conv S(A, R^n_+, B)` holds vacuously. Cor. 3.12' then gives `ρ(p_j) ≤ w_j/M`, so by §4.1 `γ_V(p_j) ≤ w_j/M`, `α_j ≥ M/w_j` and `z_V(w) ≥ M`. Since `M` is arbitrary, `sup z_V = ∞ = z_K`. The caveat that KY must allow an empty `S(A, R^n_+, B)` is kept, and so is the fallback to the sfree note's direct proof. The old text is flagged in §4.4 and in the §11 row o1. A grep finds `c = Mw` only in those two historical remarks and in the §12 table |
| **n2** no statement about background processes | **Fixed** | §13 now has a "Background processes" paragraph and a `ps -ef` row. I ran `ps -ef \| grep -i intersection-literature`: no process of this stream is running. My own reruns below were foreground runs under `timeout 300` and have finished |

## Optional items from r2

- **o-a (tangency statement).** Applied correctly. For `q(λ) = λ_1 − λ_1^2 + (1 − λ_2)^2`,
  `∇q = (1 − 2λ_1, −2(1 − λ_2))`, so `∇q(0, 1) = (1, 0)`. With `x̄ ↔ 0`,
  `x̄ − t* = (0, −1)` and the product is 0, as stated. The note now says that for
  the discrete KY Examples 4.2 and 4.3 the hypothesis gives no information. I
  rechecked the supporting argument. Near an accumulation point `t*` of a
  discrete closed set `{q ≤ 0}` with `q ∈ C^1`: at each isolated point `b`,
  `q(b) ≤ 0`, while `q > 0` nearby off the set, so `q(b) = 0` by continuity. The
  same limit argument gives `q(t*) = 0`. So `t*` is a local minimizer and
  `∇q(t*) = 0`. Correct.
- **o-b (hand bound).** Applied. The script now says that the `1/8` bound comes
  from a hand case split and evaluates only the two rational bounds (`1/8` for
  `n ≤ 8`, `1/6` for `n ≥ 9`). The floating-point check is labelled "not a
  proof". My own independent float computation gives a minimum of 0.1878852 at
  `n = 7` (for `n < 200`). This matches the log value 0.187885.
- **o-c (OpenCitations self-record).** Recorded in §13. Chmiela et al. is
  counted with 5 genuine citers. No conclusion depends on this count.
- **o-d (layout).** Applied. The revision logs are now §11 and §12. The note
  ends with Checks actually run (§13), Limits (§14) and Open questions (§15).
  The header paragraph points to Section 11 for the round-1 revision and to
  Section 12 for the round-2 revision, which is correct. The §11 table says that
  its section numbers follow the round-1 numbering, so its "§11", "§12" and
  "§13" references are consistent. Every other `§10`/`Section 10` reference
  points to the sfree note, as intended.

## Reruns (targeted, by this reviewer)

From `code/`, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 300`:

| Command | Outcome |
|---|---|
| `python3 check_ky_cor312_counterexample.py > /tmp/r3_check_ky_cor312_counterexample.log`; `cmp` with `logs/` | exit 0; byte-identical |
| `python3 check_ky_gap_thm14.py > /tmp/r3_check_ky_gap_thm14.log`; `cmp` with `logs/` | exit 0; byte-identical |
| `python3 check_bcm_orbit.py > /tmp/r3_check_bcm_orbit.log`; `cmp` with `logs/` | exit 0; byte-identical |
| `python3 -c` (own float check: min over `n < 200` of the distance from `(1/2, 0)` to `(1 − 1/√n, −1/n)`) | 0.18788515937460776 at `n = 7` |
| `ps -ef \| grep -i intersection-literature` | no process of this stream |
| `grep` of `note.md` for section cross-references, `c = Mw`, and the old "Example 4.3 have" wording | old wording gone; remaining references consistent (see o-d above) |

I did not repeat the web searches or the source-locator checks. Review r2
checked those against the saved sources, and this revision did not change them.
I read the changed passages of §4.4 line by line. I also reread the unchanged
Claim 4.4a, Cor. 3.12', the Remark 4.4 finite case, the §7 table and the §8
items that mention Theorem 1. I found no inconsistency with the revised text.

## Remaining issues

None at major or minor level.

Optional, cosmetic only: the header says that the version after round 2 "has
not been re-reviewed". After this review, that sentence could point to
`reviews/review-r3.md`.
