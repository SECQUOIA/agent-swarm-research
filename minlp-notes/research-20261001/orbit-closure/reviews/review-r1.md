# Review r1 of stream `orbit-closure`

Reviewer: an independent research agent that did not write this material.
Date: 2026-10-03. Object of review: `../note.md` (879 lines, last modified
2026-10-02 20:58), `../CLOSEOUT.md`, the code in `../code/` and the logs in
`../logs/`. My scripts are in `r1-code/`, their outputs in `r1-logs/`. I did
not edit the note, the closeout, the code or the logs, and I did not rerun the
stopped Proposition 16 (B) box certificate or the stopped BP triangle run.

## Verdict

**Minor fixes needed.** I found no wrong theorem and no gap that changes a
result. The main answer holds: at the sfree Theorem 14 corner the closures of
(A), (B) and (BP) are strictly larger than `D`.

- The Theorem 9 points are in the stated closures. My own exact checker, which
  imports no stream code and uses a different coverage argument, accepts all
  five box certificates.
- The proofs of Lemma 1, Theorem 2, Proposition 3, Corollary 4, Proposition 5,
  Lemmas 6–8, Theorem 11, Proposition 12, Corollary 13 and Lemmas 15–16 are
  correct. Lemmas 7 and 8 need one added line each (issues 4 and 5).
- The proof of the main answer without certificates (Corollary 4 with sfree
  Theorem 14(3)) is also correct.

The issues to fix are:

1. The box verifier has a soundness hole. It accepts a false certificate when
   a ray is listed twice. The saved certificates do not use this.
2. Four lower bounds are rounded up and stated as certified. They are false in
   the 6th–8th digit (`0.97539` and `0.9953612`).
3. One count in Section 7 is wrong.
4. Two proofs each lack one line (Lemma 7 and the general claim of Lemma 8).

The other points are low-severity wording or reproducibility points. There
is no major issue.

## What a certificate proves, and whether the checks test it

**Box certificates (Lemma 15, families B and BP).** A completed cover shows the
following. Every parameter `X` in a chart has either `s̄ ∉ B_F` (`excl`), or
`a(B_F)^T λ̂ ≥ 1` (`cut`), or lies outside the family (`skip`, BP only). The
logic is sound:

- All the tested quantities are affine in `X`: `v^T Z v`, `d = v^T X v` and
  `n_j = −v^T X N_j v`.
- So nonnegativity of the kept form and positivity of `n_j` at the vertices
  extend to the box. `μ_j = max_vertices d/n_j` then bounds
  `v^T A(s̄ + μ p_j) v = d − μ n_j < 0` for every `μ > μ_j` in the whole box.
- Lemma 6(a) then gives `α_j ≤ μ_j` for every `X` in the box, not just at
  sampled points.
- The kept-boundary bound `L_j(S)/m^T S m` is linear-fractional. Its
  denominator is positive at the vertices, hence on the box, so its minimum is
  at a vertex. It is applied only in family BP, whose members all have
  `S ≻ 0`. This is where Lemma 8 is valid.

The domains are right:

- BP: every `S ≻ 0` has a trace-one multiple in the open unit disk of the `u`
  chart.
- B: Lemma 7 gives `t_1 = u^T S u > 0` for every member, and every `X` with
  `t_1 > 0` has a positive multiple on one of the seven facets.
- Positive multiples of `X` give the same set.

The charts also contain parameters outside the family (`det X ≤ 0` or
`|u| ≥ 1`). Certifying them as well is harmless.

**SDP certificates (Lemma 16, family A).** I checked the identity
`Σ_j ⟨a_j A_0 + A_j, Y_j⟩ = −⟨A_0, Q(a)⟩`. `Q` is affine in `a`, so PSD with
positive trace at the vertices extends to the piece. The cover is the closed
simplex `{a ≥ 0 : λ̂^T a ≤ 1}`, so every cut vector has `λ̂^T a > 1`.

**Verifiers.** `verify_box_cert.py` rebuilds the bisection trees, so it checks
coverage of whole charts (an infinite family), not samples. It checks each leaf
exactly. But it sums the per-ray bounds without checking that each ray is
counted once (issue 1). `verify_closure_cert.py` is correct for the three
saved certificates. Its unused `outside` pruning branch has a gap (issue 6).

## Issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| 1 | Minor (must fix) | `code/verify_box_cert.py` lines 225–259; note Summary item 1 and §9.1 ("independent verifier, which also rejects corrupted certificates") | In a `cut` leaf the verifier adds `λ̂_j·bound` once per entry of `lf['v']` and once per entry of `lf['kb']`. It does not reject a ray listed twice: under keys `"0"` and `"00"` (both `int` to 0), repeated in `kb`, or present in both `v` and `kb`. The probe `r1-code/probe_verifier_duplicates.py` halves `λ̂` in `boxcert_thm14_BP.json` to `(1/10, 0, 1/12)`. This point is **not** in `Cl_BP`: the exact BP set of `bp_lower.log` gives `a^T λ ≤ 0.722`. The verifier rejects the halved point as is (21 failures) but returns `ALL PASS`, exit 0, once every ray entry is duplicated (`r1-logs/probe_verifier_duplicates.log`). The saved certificates do not contain duplicates. My checker counts each ray once and asserts canonical keys, and it accepts all five. So Theorem 9 and §6.2 stand. | Reject non-canonical, duplicate or out-of-range ray keys and overlap between `v` and `kb`, or take one bound per ray. Add this mutation to `test_verify_box_cert.py`. The verifier is separate code by the same author, so call it a "separate verifier", not an "independent" one. |
| 2 | Minor (must fix) | Summary item 1 (`0.97539 ≤ z_cl,A`); Theorem 9(c) statement and proof (`0.97539 ≤ z_1,A`, `0.97539 ≤ z_1,B`); §4 table (`certified [0.97539, 0.98]`, twice); Proposition 10 (`0.9953612 ≤ z_cl,A`) | These lower bounds are rounded **up**, so as written they are false. The certified (A) set of sfree Theorem 14(3) has bound `0.9753853514` (`research-20260928b/sfree/logs/screen_rational2.log`, `A_best_cert`), and its bisection upper value is `0.9753853515`. So `z_1,A ≈ 0.9753854 < 0.97539`. The note's own §4 table shows `z_cl,A = 0.9753853`, which is below the "certified" `0.97539`. The exact LP value of Proposition 10 is `0.995361184… < 0.9953612` (my rerun of `closure_lower.py` gives the same rational). The sfree note wrote "`z_A = 0.97539` (certified lower bound …)" as a rounded value. Turning that into an inequality made it false. | Write `0.97538 ≤ …`, or give the exact certified value, in all four places. In Proposition 10 write `0.9953611 ≤ z_cl,A`. In §5 and §12 item 12 write "≈ 0.9953612". Round every certified bound in the safe direction. |
| 3 | Minor | §7, "Point-rule families" bullet | The note says "equals the best single cut in 15 of 16 cases (exception: adv8_1, BP)". The table, and the logs without `adv8_3`, contain 11 (P) values and 7 (BP) values, 18 in all. All (P) values are single = closure, and among (BP) only adv8_1 differs (`0.42377 → 0.44791`). | Write "17 of 18", or state what is counted. |
| 4 | Minor | Lemma 7, proof, first sentence | "Relative interiors add for convex sets with nonempty interior" needs `int C_F ≠ ∅` for the sliced `C_F`, so that `ri C_F = int C_F` and Lemma 6(b) applies to `s_τ`. This is true but not shown. The image of `s ↦ sym(F^T M(s))` is either all of `Sym_2`, or (if the linear part has a kernel) a plane that does not pass through `0`. If a kernel exists, `F^{-T}J` has zero `(2,2)` entry, and `0` in the image would need `(2,2)` entry 1. A plane not through the apex that meets the PSD cone is not a supporting plane, so it meets the interior. Hence `C_F ≠ ∅` implies `int C_F ≠ ∅`. The ratio-bound note (proof of Theorem B(5)) gives the same analysis. | Add this line or a citation. |
| 5 | Low | Lemma 8 ("I verified divisibility by `det S` … for every instance used") | The lemma claims a linear `L_j` in general, but the proof only checks the instances used. There is a one-line general proof. For 2×2 `S`, `S J^T S = −det(S) J`, so with `v = JSm`: `−v^T S N_j v = det(S) · m^T J N_j J S m`, and `L_j(S) = m^T J N_j J S m` is linear. The same identity gives `v^T S v = det(S) m^T S m`. At the Theorem 14 corner this reproduces `L_1 = −8b/3`. | Replace the per-instance check by this identity, or restrict the statement. |
| 6 | Low | `code/verify_closure_cert.py`, `outside` branch (lines 115–119) | Pruning a piece by a point `x ∈ X` with `a^T x < 1` at the piece's vertices is sound only if `x_j = 0` for every `j` with `λ̂_j = 0`. Those coordinates of `a` are free (unbounded) in the piece and are not tested. The verifier also reads `xpoints` from the top level, while the producer stores them under `instance`. No saved certificate has an `outside` piece, so no result is affected. | Check `x_j = 0` on the inactive coordinates and read `xpoints` from the right place, or remove the branch. |
| 7 | Low | Lemma 16 statement; Theorem 11(b) | Lemma 16 is stated for a polytope `Π`. Theorem 11(b) and the W-corner certificate use `Π × R_+` in `a_4`, which is valid because `Y_4 = 0`. The lemma's parenthesis "(`Y_j = 0` when `λ̂_j = 0`)" does not say why. | Say that coordinates with `Y_j = 0` may range over `R_+`. |
| 8 | Low | §3, BP paragraph | "An automorphism `M ↦ AMB^T` maps `C_I` to `C_F` with `F^T = B^{-1}A`". It is the **preimage** of `C_I` that is `C_F` with `F^T = B^{-1}A`. The image is `C_F` with `F^T = BA^{-1}` (sfree Lemma 10(2)). The rest of the paragraph uses the preimage correctly. | Reword. |
| 9 | Low | §6.1, numbering | Lemma 14 appears before Proposition 12 and Corollary 13. | Renumber. |
| 10 | Low | Corollary 13 and §13 ("Theorem B(5) (proved there, without a rate)") | The citations are correct: B(4) gives `z_A/z_K ≤ 160√ε/z_0` for `ε ≤ 1.024·10^-7`, and B(5) gives `z_B/z_K → 0`. The ratio-bound note marks B(4) "superseded by Theorem B2". B2 (computer-assisted, reviewed there) gives `z_B/z_K ≤ 137√ε/z_0` for every `ε`, hence `z_cl,B/z_K ≤ 411√ε/z_0`. | Optional: cite B2 for the rate, labelled computer-assisted. |
| 11 | Low | Proposition 10 proof; §13 | The 60 rounded cuts and the certified `μ_ij` are not saved. The certified bound can only be reproduced by rerunning numerical cut generation. I reran it and got the identical rational (`r1-logs/rerun_closure_lower.log`), but the bound cannot be checked independently from saved data. | Save the rational `X_i`, `μ_ij` with the log, and mention this in §13. |
| 12 | Low | §5 ("resumable with `--resume`") | The checkpoint is gzipped, so it must be unpacked before `--resume` works. | Say so. |

### Limits section (§13) and Summary

- **Limits.** §13 is honest about the important points:
  - the factor `≈ 1.128` is numerical, and only `1.1166` is certified;
  - finiteness of `ρ_A`, `ρ_B` at the Theorem 14 corner is not proved;
  - the Proposition 16 (B) result is numerical, and its certificate is
    incomplete;
  - the (B) single-cut values are heuristic;
  - the instances are few;
  - Theorem 11(c) depends on sfree Lemma 10(4) only for the equality case;
  - Corollary 13 depends on the ratio-bound note.

  §13 should also list issue 1 (the verifier's current status) and issue 11.
- **Summary.** The Summary matches the body except for the rounded bounds of
  issue 2. "Together with sfree Theorem 14(3) this already proves the main
  answer without any certificate" is correct: sfree Theorem 14(3) proves
  `z_B < z_K` for the supremum, by compactness, so (BP) ⊆ (B) and (A) follow.
- **Incomplete Proposition 16 (B) certificate.** §5 reports it as numerical
  evidence only, with the true counts (`247,393` processed, `171,528`
  queued, exit 143), and no claim depends on it. The Summary claims only (A)
  at that corner. This is handled correctly.

### Use of the ratio-bound note

I checked each statement against `../ratio-bound/note.md`:

- **Lemma S.** SCIP's set is `C_F` with `F^T = R_θ`,
  `(sin θ, cos θ) = x̂/‖x̂‖`, `x̂ = ((x − y)/2, (w + 1)/2)`. The note uses it
  correctly.
- **Theorem A.** `z_A/z_K ≥ 1/((1 + √2)D)` for `D ≥ 1`. At the W-corner with
  `w_ε`, `z_K = 2` and `D = sqrt(X~Y~/q̄) = sqrt((2/ε)²/2) = √2/ε`, which
  gives `(2 − √2)ε ≤ z_1,A(w_ε)` for `ε ≤ √2`. Correct; the range `ε ≤ √2` is
  implicit.
- **Theorem B(4) and B(5).** Statements and numbering match. The
  automorphism of Corollary 13 is Lemma N of that note.
- **Status.** The ratio-bound note's round-2 review verdict is "Verified".

## Checks run

All commands were run with `OMP_NUM_THREADS=1` (and
`PYTHONDONTWRITEBYTECODE=1`, so that nothing was written into `code/`), with
`timeout`, and at most three processes at a time. These are targeted checks. I
ran no project-wide checks and did not consult CI.

| # | Command (from `orbit-closure/code/` unless stated) | Outcome |
|---|---|---|
| 1 | `python3 verify_box_cert.py ../logs/boxcert_{thm14_B,thm14t_B,thm14_BP,thm14t_BP,thm14w_B}.json` | ALL PASS, exit 0 for each (5.7, 17.6, 0.4, 0.6, 10.9 s); leaf counts as in the note; `r1-logs/rerun_verify_boxcert_*.log` |
| 2 | `python3 verify_closure_cert.py ../logs/closure_cert_{thm14_A,prop16_A,wcorner_A_A}.json` | ALL PASS, exit 0 (25, 92, 1 pieces, 0 pruned); `r1-logs/rerun_verify_closure_cert_*.log` |
| 3 | `python3 test_verify_box_cert.py ../logs/boxcert_thm14_B.json ../logs/boxcert_thm14_BP.json` | 16 of 16 mutations rejected, originals accepted; `r1-logs/rerun_test_verify_box_cert.log` |
| 4 | `python3 r1-code/indep_box_check.py CERT FAMILY λ̂` (from `reviews/`) for the five box certificates, with `λ̂` typed in from the note | PASS for all five. Instance data equal the note's corner. Coverage holds by a different method from the stream's tree rebuild: leaves lie in the chart, volumes add up exactly, interiors are pairwise disjoint. Every leaf is rechecked from the definitions with `F^T = X M(s̄)^{-1}`, with the `L_j` forms derived and checked as polynomial identities, and each ray counted once. Counts: thm14t_B 8070 cut / 2253 excl; thm14_B 2530 / 725; thm14w_B 5518 / 1543; thm14t_BP 420 cut / 6 skip; thm14_BP 33 / 5. `r1-logs/indep_box_*.log` |
| 5 | `python3 r1-code/indep_misc_check.py` | ALL PASS. Lemma 16 certificates: order-free bisection cover, exact volume sum, PSD and trace conditions, instance check. Theorem 11(b) integer certificate (`R = [[14, 18], [18, 85]]`). Theorem 11(a): identities `7a + 6b`, `−8b/3`, `4a/9`, and the rational orbit set with `α_2, α_3 ≥ 367/759`. The `2539/10000` (BP) set. §6.2: `min q = 6480592821/4840070400112 > 0` by my own face enumeration; ratio `1.11663`. Theorem 9 sums. `r1-logs/indep_misc_check.log` |
| 6 | `python3 r1-code/indep_wcorner_bp.py` | Theorem 11(c), numerical. At `S = I`, `a_1 + a_2 = 0.207106781187 = (√2 − 1)/2`, by kept vectors and by direct pencil membership. Kept-vector and pencil values agree on 200 random `S` (difference `≤ 6·10^-5`, from the bisection cap). The minimum over 40,000 random `S` is `0.2071096`. Nelder–Mead from 60 starts gives `0.207106781187` at `S = I`. Near the disk boundary the minimum is `1.33`. The case (iv) bound has minimum `0.7516 > 3/4`, and case (v) has minimum `G_1 = 0.410 > 0.2887`, with no violations. `r1-logs/indep_wcorner_bp.log`. A first version missed the kept-boundary vector near singular `S` and reported a spurious minimum `0.043`; adding the isotropic directions of `Z` (the point made in §9.1) fixed it |
| 7 | `python3 r1-code/probe_verifier_duplicates.py` | Issue 1: the false point `(1/10, 0, 1/12)` with duplicated ray entries is accepted (exit 0); without duplicates it is rejected; `r1-logs/probe_verifier_duplicates.log` |
| 8 | `python3 closure_lower.py` | The same exact rational as the stream's log, `= 0.995361184…`, PASS, 51.9 s; `r1-logs/rerun_closure_lower.log` |
| 9 | Python reads of `logs/closure_survey_*.jsonl`, `factor_scan_thm14.jsonl`, `factor_edge_thm14.jsonl`, `closure_at_*`; `grep` of the sfree logs | §4 and §7 tables match the logs except the count of issue 3. Factor scan maximum is `1.12832` at `w = (0.55, 0, 0.45)`, median `1.0`, 90% quantile `1.0099`. The sfree certified (A) value is `0.9753853514` (issue 2) |
| 10 | `ps` and `ls -lt` after the work | No process of mine was running. No file in `code/` or `logs/` was modified |

Not run: the Proposition 16 (B) box certificate and the BP triangle search (as
instructed), `verify_wcorner.py`, `thm14_factor.py`, `bp_lower.py`,
`zk_lower.py`, `loop_rank2.py`, and the numerical scans. I rechecked the exact
data of the third through fifth of these independently (checks 5–6) instead
of rerunning them.
