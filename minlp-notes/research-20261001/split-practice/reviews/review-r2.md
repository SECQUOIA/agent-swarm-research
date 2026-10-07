# Review r2 of `split-practice/note.md`

Date: 2026-10-03. Reviewer: independent research agent (review round 2,
confirming review). I did not write the note, its code or the round-1 review.
I did not edit `note.md`, the stream code, the stream logs or
`logs/machine_load_run2.txt`. My code is in [`r2-code/`](r2-code/) and its
outputs are in [`r2-logs/`](r2-logs/).

## Verdict

**Minor fixes.** No major problems remain.

- The revised lattice code is exact where the note says it is. It agrees with
  independent reference code on every test, including an independent exact
  minimum of `q` for 160 rational psd matrices.
- All changed numbers that I checked match the raw logs: the DM60 row, 2057 of
  2688, the per-`p` means, 5168 calls, 103 + 17 = 120 of 123, the Theorem 3
  table, and the nine rank-1 records.
- The Lemma A certificates are applied correctly. I recomputed all 17 new
  certificates independently and got the same values. The tolerance is
  adequate.
- The rewritten Theorem 3 discussion (Summary, §§8, 11, 12) now claims what the
  corrected rerun shows at the roots.
- One minor issue remains (new issue 1). The note understates the non-root
  results, and its phrase "These facts do not prove that shorter
  representatives are impossible" leaves open a reading that my check rules
  out at four of the six nearly closed neighbours. There, every exact
  maximizer in the returned coset is provably about as long as the returned
  vector. The large coefficients there therefore come from exact raw
  maximization on a rank-truncated neighbour, not from the implementation.

## Status of the round-1 issues

| r1 issue | Status | Evidence |
| --- | --- | --- |
| 1 (major) Theorem 3 framing | **Resolved at the roots; one residual point** (new issue 1) | Summary ¶2, §8, §11 and §12 now separate the raw objective from the implementation and no longer say that low rank makes Theorem 3 impractical. The rerun matches the logs: 98/98 root vectors pass the sanity check, with maximum coefficient median 5 and maximum 70. The non-root wording is too weak (new issue 1). |
| 2 Lemma A certificates | Resolved | `certify_ratio_r1.py` applies the bound correctly. I recomputed the 17 new certificates, and 9 finished ones, with my own code (Checks). |
| 3 DM60 best-known rule | Resolved | Own recomputation: 12 closed, mean closure 98.38%, mean SDP gap 9.912%. The note says 12 / 98.4 / 9.91. |
| 4 §7 column | Resolved | 2057 of 2688 (76.5%). The per-`p` means 0, 0.3, 14.9, 22.4, 22.5, 28.3, 20.1, 27.0, 22.4, 25.8, 22.0 match the table. The caption still needs one clarification (new issue 3c). |
| 5 Prop. C(c) | Resolved | The text now says `D ≥ 4` and gives equality at `D = 2, 3`. I checked the algebra by hand: `⌈D/2⌉/⌊D/2⌋ < D − 1` exactly when `D ≥ 4`. |
| 6 Prop. D remark | Resolved | The remark is restricted to the proved 0/1 case. The signed case is labelled unproved, and the box MIQP is referenced as §8. |
| 7 two meanings of `q` | Resolved | The X3C parameter is now `k` in §4 and in the §10 text and table. |
| 8 "only practical points" | Resolved | The claim is restricted to the stored selection and the `dmfam`/`dmplus` loops, and the BT10 rounds are mentioned. I confirmed that the two DM60 cut points are the only stored points where the families find no violation above `10⁻³` and the general separator does. |
| 9 completeness flag; echelon form | Resolved | `first_complete`, `second_complete` and `optimum_certified` are recorded, and `complete` requires both enumerations. `col_hnf` now returns the reduced HNF (checked against my own HNF). One optional code point remains (new issue 2). |
| 10 unresolved DM60 optimum | Resolved | The Summary and §6 say "11 established, 1 upper bound only". |
| 11–17 optional | Resolved | The two medians (0.152 over 17 values, 0.1545 over 15), 5168 calls (4768 + 400, none capped), the dense-cap ratios (+29.3%, +24.1%), Letchford's question, binary Corollary 6, the transcript attribution, `−2.0·10⁻⁷`, and "closes" are all in place. |

## New issues

### Minor

**1. The non-root Theorem 3 results are understated, and their cause is left open.**

*Location:* §8 paragraph "The corrected non-root results remain mixed …";
§12 "Exactness and rank" ("Returned splits at some non-root rational
neighbours …"); §4 *Consequence* ("Exact reduction removes the old
implementation's coefficient blow-up (§8)", without restriction); Limits,
fourth bullet.

*Description.*
- From `logs/thm3_r1.jsonl`, all 13 returned non-root vectors have maximum
  coefficients from 30 to 69,618,975.
  - 8 are not violated at the stored point.
  - The other 5 have normalized violation at most `8.2·10⁻⁶` (median
    `2.8·10⁻⁸`), so they are useless as cuts.
  - "Some" in §12 should therefore be "all".
- The note says these facts "do not prove that shorter representatives are
  impossible". I tested this directly (`r2-code/r2_nonroot.py`,
  `r2-logs/r2_nonroot.jsonl`) and found that the long vectors are forced:
  1. I rebuilt each pivot-row neighbour with my own code. All 13 logged
     vectors reproduce their logged exact values.
  2. I computed the integer kernel of the factor `P` independently (sympy LLL).
  3. I bounded every vector of the returned maximizer coset `v + ker_ℤ P` from
     below, by projecting orthogonally to the first `d − 1` reduced kernel
     vectors.
- Result at four of the six nearly closed neighbours, where both enumeration
  flags are complete:

  | Point | Every coset member has norm at least | Returned vector |
  | --- | --- | --- |
  | `dm_QUTO_t2_n30_p25_s0__DM__cut` | `1.13·10⁴` | `1.15·10⁴` |
  | `dm_QUTO_t2_n30_p25_s0__DM__cut_trace` | `1.015·10⁸` | `1.018·10⁸` |
  | `bt_n20_p16_s2__BT__cut` | `7.49·10⁵` | `7.49·10⁵` |
  | `bt_n50_p25_s0__BT__cut` | `1.47·10⁴` | `1.47·10⁴` |

  - On these neighbours, no short exact maximizer exists. The returned vector
    is within 1.5% of shortest.
  - At the stored point their values (`298` to `5.8·10⁸`) come almost
    entirely from the eigen-directions that the rank truncation discarded
    (`λ_{r+1}` from `2.7·10⁻⁷` to `1.7·10⁻⁴`).
  - So the failure comes from exact raw maximization on a rank-truncated
    neighbour. It does not come from the shortening code.
- For the open points the bound covers only the returned coset. Their second
  enumerations are capped, so other near-optimal images were not all checked.
  The bounds there are 779–4496 at the four `bt_n20` vectors, and weak
  elsewhere.
- For the two `bt_n30_p0_s1` vectors the bound (71 and 7.6) is inconclusive.

*Required change.*
- In §8, replace "These facts do not prove that shorter representatives are
  impossible" with the result above. Suggested wording: "At four of the six
  nearly closed neighbours, every exact maximizer in the returned coset is at
  least as long as `1.1·10⁴`–`1.0·10⁸`, within 1.5% of the returned vector;
  the stored-point values come from the discarded eigenvalues. Elsewhere the
  question is open."
- State the normalized violations (≤ `8.2·10⁻⁶`) of the five violated open-point
  vectors.
- In §12, write "all 13 non-root returned splits have coefficients ≥ 30; 8 are
  not violated at the stored point".
- In §4 *Consequence* and in Limits, restrict "removes the coefficient blow-up"
  to the roots.

This does not change the note's main conclusions. It strengthens them: the
problem at these points is the raw objective together with rank truncation.

### Optional

**2. A capped second enumeration can drop the first minimizer.**
`thm3_exact` adds the C-enumeration minimizer `(val, z)` to the candidate list
only when the second enumeration found nothing. If the second enumeration hits
its cap after collecting some points, `z` may not be checked exactly. Every
collected point lies within `10⁻⁹(1+|val|)` of `val`, so the loss is at most
that much, and no claim in the note changes. Fix: always append `(val, z)`.

**3. Small wording fixes.**
- (a) §8, root paragraph: "certified numerically by the post-check below"
  should be "above".
- (b) §4: "*Consequence* (heuristic, supported by §6)": the supporting data
  are in §8.
- (c) §7 table: the caption says "mean over open instances". That holds for
  the closure columns. "Mean rounds" and "rounds where only general splits
  were violated" average over all 10 instances per `p`. Over open instances
  only, `p = 5` and `p = 10` give 37.9/35.2 rounds and 31.4/27.5 general-only
  rounds. Say which average is used.

**4. The two rank-1 rationalizations agree, and this could be said.**
The rerun records (`thm3` and `rank1_grid` in `logs/thm3_r1.jsonl`) give
identical denominators, vectors, exact values and stored values for the
pivot-row and first-column neighbours at all 10 rank-1 roots. The main
`thm3_exact` itself returns maximum coefficient 1–5 at the nine fractional
ones. The note's "their vectors need not agree" is true in general, but here
they do agree. Saying so answers the rationalization question for rank 1.

## Answers to the author's questions

- **Two completeness flags.** Correct.
  - `first_complete` and `second_complete` are returned and logged, and
    `complete` is their conjunction. `optimum_certified` is true only for
    exact `−¼`.
  - With `max_nodes = 1` I get `complete = first = False` and `second = True`
    (`r2-logs/r2_lattice.txt`).
  - The 14 capped second enumerations are 7 roots and all 7 open points. At
    the 7 roots the exact value is within `10⁻⁹` of `−¼` (at most
    `9.4·10⁻¹³` above it), so raw optimality on the neighbour holds to
    `10⁻⁹` by Proposition C(a). The capped flag does not weaken any root
    conclusion.
  - At the open points the capped flags mean that near-optimal images were
    not all examined. The note states this.
- **Numerical certification tolerance.** Adequate.
  - Lemma A's bound is applied after scaling by `Y₀₀`, with
    `ε = max(0, −λ_min(S)) + 10⁻⁹`. The derivation
    `ratio ≤ 1/(4‖w‖²) + ε` is correct.
  - The 17 new certificates have excess at most `2.3·10⁻⁹`. All 17 survive a
    `10⁻⁸` tolerance, and 16 survive `10⁻⁹`.
  - The largest excess among all 110 certified records is `7.6·10⁻⁷`, at a
    finished record, with the same vector up to sign. It comes from the clipping
    difference: that point has eigen slack `4.7·10⁻⁶`.
  - So `10⁻⁶` is not a tuned threshold: the counts are unchanged from `10⁻⁵`
    down to `10⁻⁶`.
- **Two rank-1 rationalizations.** At all 10 rank-1 roots they give the same
  vectors (optional issue 4). The separate check finds coefficients ≤ 4 and
  supports 5–12. I recomputed `pᵀv = −D/2`, the exact `−¼` and the stored
  values for all nine records with my own code.
- **Remaining non-root failures.** See new issue 1. At least four of the eight
  failures are inherent to the exact maximizer of the rank-truncated neighbour,
  not to the reduction code.

## Checks run (by the reviewer)

All checks ran from `research-20261001/split-practice/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, under `timeout`, one process at a
time. These are targeted checks of this stream only. I ran no project-wide
checks and did not inspect CI. No process of mine is left running (checked
with `pgrep -af r2-code`; it matched only its own shell).

| Check | Command | Outcome |
| --- | --- | --- |
| Changed numbers from raw logs (own script, no stream imports) | `timeout 900 python3 reviews/r2-code/r2_numbers.py` → `r2-logs/r2_numbers.txt` | Exit 0. DM60: 12 closed, 98.38%, 9.912%. The integral final point of `dm_LIN_t3_n60_p50_s0` (−279.780163) replaces the incumbent (−279.381094). DM30 and BT50 rows unchanged. BT10: 2057/2688 (76.5%); per-`p` means as in the table; general-only splits have support 2–10, max coefficient 6, 91 with support ≤ 3, median violation 0.0071, max 0.2228. 5168 `sep_ratio` calls (4768 `bt` + 400 `btfam`), 0 capped. Normalized: 103 finished (83/13/7), 120 finished or certified (99/14/7), 17 new (16 roots + 1 open), uncertified bounds 180, 198, 7. Theorem 3: every table cell reproduced; exact stored-point `q` recomputed for all 111 vectors, 0 mismatches. Rank-1: 9/9 with `pᵀv = −D/2`, exact `−¼`, coefficients ≤ 4, supports 5–12. |
| Exact lattice code against independent reference code | `timeout 1500 python3 reviews/r2-code/r2_lattice.py` → `r2-logs/r2_lattice.txt` | Exit 0. `col_hnf`: 300 matrices (entries up to `10²⁰`); `MU = [H|0]`, Bareiss `det U = ±1`, `H` equal to my own reduced HNF (different algorithm; HNF is unique). `lll_rows_exact`: 120 bases (entries up to `10³⁰`, graph lattices as in `thm3_exact`, near-dependent rows); same lattice by exact solve, LLL(3/4) by freshly computed GSO. `shorten_mod_kernel`: 150 scrambled cosets; coset preserved in all; brute-force shortest in 147, worst squared-norm ratio 1.2. `thm3_exact`: 160 random rational psd matrices of rank 1–3; `q` equal to my exact rational Fincke–Pohst minimum in 160/160, and the returned `v` reproduces `q` exactly. Forced cap: flags as described above. |
| Lemma A certificates, independent enumeration (all `w` with both signs; best `v₀` by direct evaluation of `q_Y` at the stored matrix) | `timeout 1500 python3 reviews/r2-code/r2_certify.py` → `r2-logs/r2_certify.txt` | Exit 0. All 17 capped records with bound ≤ 3 (16 roots with bound 2, `bt_n50_p0_s0__BT__cut` with bound 3) are certified, with the same bound and the same excess as the log to 3 significant digits (max `2.26·10⁻⁹`). The three remaining capped records have bounds 180, 198 and 7 as logged. Of 12 random finished records, 9 are recomputed and certified, and 3 have bounds 4, 5 and 46 (> 3), not enumerated by me. |
| Non-root Theorem 3 vectors: neighbour rebuild, independent integer kernel, coset shortening (sympy LLL, δ = 0.99, five embedding weights), projection lower bound, eigen-split of the stored value | `timeout 1500 python3 reviews/r2-code/r2_nonroot.py` → `r2-logs/r2_nonroot.jsonl`, `.out` | Exit 0. 13/13 logged exact values reproduced on my rebuilt neighbours. Stronger LLL shortening never gives a stored-point violation where the stream's vector has none. Lower bounds on coset members as in new issue 1. Stored values of the failing nearly closed vectors are dominated by the discarded-eigenvalue part. |
| Rank-1 rationalizations | inline `python3 -c` over `logs/thm3_r1.jsonl` (not saved) | `thm3` and `rank1_grid` identical at all 10 rank-1 roots (optional issue 4). |
| Code reading | `git diff -- research-20261001/split-practice/`; full read of `lattice.py`, `rerun_thm3_r1.py`, `certify_ratio_r1.py`, `check_rank1_short_r1.py`, `test_revision_r1.py`, and the diffs of `summ_points2.py`, `summ_loop_bt.py`, `summ_sep2.py`, `exp_separate.py` | Graph-lattice preconditioning keeps `U` unimodular (LLL is unimodular on rows `[eᵢ | 10⁶·M_{·i}]`). The common-denominator check uses `q(z) = zᵀA₂z − 2zᵀA₂c₂`, and its constant term vanishes because `cᵀAc = w₀ᵀGw₀/4 = X₀₀/4`. The swap update of the incremental GSO follows the standard formulas. Babai plus the affine embedding preserves the coset (asserted in the code). Found optional issue 2. |
| Note text | full read of the revised note | Found new issues 1 and 3. Checked Prop. C(c), Prop. D and Prop. E. The stored-point dense-exception claim holds (only the two DM60 cut points). The author's saved logs report `test_lattice.py`, `check_props.py` and `test_revision_r1.py` passing; I did not rerun them. |
