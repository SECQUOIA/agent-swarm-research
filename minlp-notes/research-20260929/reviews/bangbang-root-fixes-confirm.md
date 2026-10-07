# Confirmation of the root's corrections to `theory-bangbang/report.md`

Date: 2026-09-30. Referee: independent. I did not write the report, its verification
([V] = `reviews/bangbang-verification/verification-report.md`) or the corrections.
Scope: the root's changes to the report (the new Section 9 and the inline changes), checked
against [V] and against `theory-bangbang/extension-n2.md` ([E]). [E] was reviewed in
`reviews/bangbang-n2-review.md` and confirmed in `reviews/ext-bangbang-n2-confirm.md`.

Method:

- I recovered the report text the root saved first (the `Write` call in the root session
  transcript) and diffed it against the current file. So every change is identified exactly.
- I checked every changed number against the verifier's logs, and one certificate value against
  the certificate data.
- I checked the citations against publisher and repository records.
- I rederived the changed mathematics by hand.
- I edited no file under review and ran none of the author's or the verifier's scripts.

## Verdict

**Fixes needed.**

- The corrections that were applied are faithful to [V], and the changed mathematics is correct,
  apart from one wording error in Proposition 3.1 (R4).
- No claim was strengthened, and the inline citations are right.
- Three of [V]'s requested fixes were not applied (R1–R3).
- The report is not yet consistent with [E], and neither Remark 3.3 nor the open-problem list
  points to it (R5).

## Item-by-item check

| Change | Faithful to [V]? | Check | Result |
|---|---|---|---|
| Status line | yes | — | OK |
| Summary: bullet on the independent verification | yes | Exact bound `293.87607509587509237940`; upper bound `293.8760750958750932772`; difference `8.98e-16`; author's bound `2.29e-12` below the exact value; author's point `5.96e-12` above the upper bound (`qcal_exact.json`, `primal_check.json`) | Numbers correct. But the bold headline two lines above still says "gap is **8.3e-12**" (R1) |
| Summary: "Numerical checks" paragraph | yes | Toy logs: box domain 68, 135, 270, 540, 1079 failing stages (0.272 → 0.270); reachable-set domain 0.068–0.070, one-sided | Correct; "at every N" is too broad (M2) |
| Proposition 1.2(2) | yes | Converse: along an optimal trajectory the terms sum to `f* = B`, each term is at least its infimum, so all are tight | Correct |
| Theorem 2.3(2), radius `δ_1` | yes | Rederived below | Correct; a leftover of the same kind remains (M1) |
| Remark 2.5 | yes | Citations verified (table below); `O((h^{1/2})/h) = O(h^{-1/2})` | Correct. The Sources section still has the old wrong entry (R3) |
| Proposition 3.1: regularity | partly | See R4 | Hypothesis attached to the wrong object |
| Proposition 3.1: robustness paragraph | yes | Matches [V] Part B | OK |
| Proposition 3.1: O–M relation | yes | `[ẋ] = b[u]`; `[ψ̇] = −(∇ℓ_1 + b_xᵀψ)[u] = w[u]`; so `q = [u](Qb)ᵀ − [u]wᵀ = [u](Qb − w)ᵀ`. This agrees with [E] Section 3 (`q = Δu·β_L`) | Correct |
| Proposition 3.2: "forces only `∫|β|²/|σ| < ∞`" | yes | Integrate the trace of the inequality on `(τ, τ+δ)`: bounded `P` bounds `∫Δ|β|²/(2|σ|)`. With `P` continuous at `τ`, `β(τ)` exists and must be 0 | Correct |
| Remark 3.3: the gap before `τ` | yes | Consistent with [E] Proposition 15 (the obstruction occurs in example C) | OK. The rest of the remark is out of date (R5) |
| Theorem 4.1 | yes | Window exactness is now an assumption; regularity added; tangency in (H3) redundant | Correct; one ambiguous symbol (M4) |
| Section 5.4 | yes | 34424 stages; 0.49992 ulp; 0 stages outside the widened domain (`states_check.json`) | Correct |
| Novelty paragraph | yes | Citations verified | OK; wording (M6) |
| Status table | yes | — | OK, except the Remark 3.3 row (R5) |
| Section 9 | mostly | — | Item 1 says the gap is now 9.0e-16, but the headline and Section 5.5 still say 8.3e-12. The last line ("being attempted") is out of date |

### Theorem 2.3(2): recheck

Put `K = Λ + ΔM_s`. Take a stage with `ū = u_−`; the case `u_+` is symmetric.

- By Lemma 2.2, exactness needs `Σ_t ≥ Δ|g_t|²/(2K)`.
- For `|t_t − τ| ≤ δ_1`, `Σ_t ≤ |σ(t_t)| + c(h + e_h) ≤ γ_2δ_* + c(h + e_h) = Δ|β(τ)|²/(4K) + c(h + e_h)`.
- Let `b_min² := min_{|t−τ|≤δ_β} |β(t)|²`. By continuity on a compact interval,
  `b_min² > |β(τ)|²/2`. Then `|g_t| ≥ b_min − c(h + e_h)`, and
  `Δ|g_t|²/(2K) ≥ Δ|β(τ)|²/(4K) + m − c'(h + e_h)`, with
  `m := Δ(b_min² − |β(τ)|²/2)/(2K) > 0`.
- So every such stage fails once `(c + c')(h + e_h) < m`. That is about `2δ_1/h = Θ(1/h)` stages.

The correction is right, and "with a margin" is justified.

Leftover (M1): the step `|σ(t_t)| ≤ γ_2|t_t − τ|` uses (W2), which holds only "near `τ`". So
`δ_1` must also lie inside that neighbourhood: `δ_1 = min(δ_*, δ_β, δ_σ)`. Alternatively, state
(W2)'s upper bound on `|t − τ| ≤ δ_*`. This gap was present before and is of the same kind as the
one [V] fixed.

## Required fixes

**R1. Gap in the Summary headline and Section 5.5 ([V] Part A, fix 1, not applied).**

- Line 27 still reads "The refined primal point is 293.87607509588105 ... so the gap is
  **8.3e-12**".
- The Section 5.5 table still has "gap | 8.3e-12 (2.8e-14 relative)".
- The text below the table still says "the effect of repairing that exactly was not bounded". [V]
  bounded it: a rigorously feasible point exists, and its value is 5.96e-12 lower.

The new Summary bullet gives the correct figures, so the Summary now states two different gaps.

Suggested headline: "The certified lower bound is **293.8760750958728**. The verifier's rigorously
feasible point gives `f* ≤ 293.87607509587509328`, so the gap is **2.3e-12**. The author's float
point 293.87607509588105 satisfies the rows only to 8.9e-16 and is 6.0e-12 higher."

In Section 5.5, replace the gap row and the "not bounded" sentence the same way.

**R2. `p_v(3092)` ([V] Part A, fix 3, not applied).**

Section 5.3 still says the refinement gave `p_v(3092) = 6e-12`. In
`logs/optcdeg2_qcal_data.npz`, `pv[3092] = 7.599e-12`, as [V] reports. Change it to 7.6e-12.

**R3. Sources section still misattributes a paper.**

Lines 582–585 still list "Alt et al. (COAP, s10589-017-9948-z) (title from memory)" and the
univaq PDF. Both are Scarinci–Veliov (COAP 69(2) 403–422). Remark 2.5 now says so, so the Sources
section contradicts it. Replace the entry with the verified references in the table below.

**R4. Proposition 3.1: the regularity hypothesis is on the wrong object.**

- [V] asks that `S_t` be continuous up to `τ` from each side and `C¹` in `x`. That is the time
  derivative in `r = ℓ_0 + ℓ_1u + S_t + S_xᵀg`. It is needed so that `r` and `∇_x r` have one-sided
  limits at `τ`.
- The report says instead that `S` is "continuous in `t` up to `τ` from each side and `C¹` in `x`
  there". "`C¹` in `x`" adds nothing to "`C²` in `x`", and continuity of `S` in `t` does not give
  the limits the proof needs.
- Proof step (1) still combines the two sides into one function `r(τ,·,·)`. Under one-sided
  regularity it has to work on each side separately.

Suggested hypothesis: "`r` and `∇_x r` extend continuously to `t = τ` from each side (for example,
`S_t`, `S_x`, `S_xt` and `S_xx` do), and `r(τ±,·,u) ≥ 0` near `x*(τ)` for all `u ∈ U`."

Suggested step (1): "On each side, `r(t, x*(t), u) = σ(t)(u − u*(t))` by exactness and
`S_x = ψ`, so `r(τ±, x*(τ), u) = 0` for every `u`." This is the argument of [E] Theorem 1,
step 2. It also shows that one side is enough.

**R5. Consistency with `extension-n2.md`: pointers missing and claims out of date.**

[E] was reviewed, revised and confirmed (`reviews/ext-bangbang-n2-confirm.md`: "Verified ... a
few minor edits remain; none changes a conclusion"). The report still presents the question as
open and never points to [E], except for the out-of-date last line of Section 9.

Out-of-date statements:

- Remark 3.3, the scalar sketch: the blow-up is labelled "(a conjugate point)". By [E]
  Corollary 7, if `−D/Δ² < η_L < 0`, the maximal solution blows up in the layer after `τ` even
  though the bang-bang second-order sufficient condition holds. [E] Theorem 1 does not use
  `n ≥ 2`, and [E] says that "the scalar sketch in [R] has the same gap".
- Remark 3.3, the conjecture: "(`n ≥ 2`) a tangential solution exists iff `P̂` is bounded (no
  conjugate point)". [E] answers it in the local formulation: a solution exists iff `η_L > 0`, for
  any `n` (Theorems 1–2, Corollary 3). [E] refutes the "no conjugate point" reading
  (Corollary 7; example B, `n = 2`: `η_L = −0.429`, `D = 3.066`, `F''(τ) = 1.350`).
- Remark 3.3, last sentence: "the relation to this construction is not worked out". This
  contradicts the new paragraph after Proposition 3.1 and [E] Section 3. There, the maximal
  tangential calibration is the Osmolovskii–Maurer rank-one jump with `D(H)` set to 0.
- Also out of date:
  - the Section 6 open list ("Existence of tangential strict calibrations for `n ≥ 2`");
  - the Summary's "Still open" line ("only a scalar sketch");
  - the status-table row "conjecture for `n ≥ 2` open";
  - Section 9's "being attempted in `extension-n2.md`".

Suggested addition at the end of Remark 3.3:

> *Status after `extension-n2.md`* (reviewed in `reviews/bangbang-n2-review.md` and confirmed in
> `reviews/ext-bangbang-n2-confirm.md`). The setting is one regular switch, fixed `x_0` and a free
> endpoint. Let `Q` be the last-arc Lyapunov solution, and put `η_L = bᵀ(Q(τ+)b − w)` and
> `D = |σ̇(τ)|Δ`.
>
> - In the local formulation, where the singular condition is imposed only near `τ`, a
>   tangential strict quadratic calibration exists iff `η_L > 0`, for any `n` (Theorems 1–2,
>   Corollary 3).
> - The "no conjugate point" reading is false. If `−D/Δ² < η_L < 0`, the bang-bang second-order
>   sufficient condition holds, yet no exact calibration that is `C³` on a uniform tube after the
>   switch exists (Corollary 7; example B). Theorem 1 does not use `n ≥ 2`, so the label "a
>   conjugate point" in the scalar sketch above is wrong in the same way.
> - In the global form of Proposition 3.2, the obstruction before `τ` does occur. In example C
>   (`η_L > 0`), no global-model calibration exists, and no `S` satisfies (H3) of Theorem 4.1
>   with an exact terminal term (Lemma 14, Proposition 15; the blow-up is a floating-point
>   result).
> - The local calibrations do not by themselves supply (H3) or (H5) (`extension-n2.md`,
>   Sections 4.1 and 7).

In the same remark, replace "(a conjugate point)" and "the relation ... is not worked out" to
match.

Suggested Section 6 open items:

- a transfer theorem for local tangential calibrations ([E] Section 8; Theorem 2's calibrations
  violate the far-region condition in examples A and C);
- written-out proofs for several switches and for the global model ([E] Theorems 8 and 9 are
  sketches);
- the borderline case `η_L = 0`;
- (H5) beyond LQ-structured data ([E] Section 7, Propositions 12–13);
- the remaining items as before.

Also update, to match:

- the Summary's "Still open" line;
- the status-table row for Remark 3.3, for example: "scalar sketch (existence part) after `τ`;
  gap before `τ`; the `n ≥ 2` question is answered in the local formulation, and its 'no
  conjugate point' reading refuted, in `extension-n2.md`";
- the last line of Section 9.

## Recommended minor edits

- **M1.** Theorem 2.3(2): add `δ_σ`, the neighbourhood of (W2), to the minimum (see the recheck
  above).
- **M2.** Summary toy: write "at N = 500 … 8000, with the box domain `|x| ≤ 2`" instead of "at
  every N" (the N = 500 value is 0.272). Add [V]'s observation that with the exact reachable set
  as the domain, where `B_r ⊂ D_t` fails, the window is one-sided and four times shorter
  (0.068–0.070). It is still of fixed duration.
- **M3.** Corollary 2.4: add [V]'s minor note. For `n = 1`, `ℓ_1 ≡ 0` and state-dependent `b`,
  "fail only where SGM fails" also needs (W5), because `β(t) = b'(x*)ψ(t) ≠ 0` for `t ≠ τ`.
- **M4.** Theorem 4.1: write `∂_tS` instead of `S_t` in the parenthetical, because `S^h_t` is
  the discrete family there. Consider moving the added regularity into (H3). Also add a pointer to
  [E] Section 4.1: (H3) implies the global-model inequality (Lemma 14), and example C shows that
  (H3) can fail with an exact terminal term even when `η_L > 0` (float blow-up).
- **M5.** Section 5.7: add one sentence saying that family A's failure on optcdeg2 (`w = 0`) is
  the SGM failure of Section 5.2, not a test of the window law ([V]).
- **M6.** Novelty paragraph: "Related prior work that must be cited:" should read "Related prior
  work:". Add the full references below to the Sources section.
- **M7 (nit).** The exact lower bound is `…5092379(40)`; "293.87607509587509238" rounds it up
  in the 20th digit. For a lower bound, truncate (for example `…509237`). The bracket of 9.0e-16
  is unaffected.
- **M8 (format).** The Remark 3.3 line that begins "does. The scalar sketch ..." and the
  Section 5.4 lines are overlong. Rewrap them.

## Citations checked

| Report citation | Verified details | Source |
|---|---|---|
| Alt–Baier–Lempio–Gerdts 2013 | W. Alt, R. Baier, F. Lempio, M. Gerdts, *Approximations of linear control problems with bang-bang solutions*, Optimization 62(1) (2013) 9–32, DOI 10.1080/02331934.2011.568619. The abstract gives order h for adjoint and switching function, controls equal off a set of measure O(h), order 1 in L1; a slope condition is assumed. | eref.uni-bayreuth.de/63114 |
| Alt–Felgenhauer–Seydenschwanz | *Euler discretization for a class of nonlinear optimal control problems with control appearing linearly*, COAP 69(3) (2018) 825–856, DOI 10.1007/s10589-017-9969-7. Mayer cost, control appearing linearly, control bounds only; Hölder-type estimates, improved under a stronger second-order condition. | ideas.repec.org |
| Scarinci–Veliov | *Higher-order numerical scheme for linear quadratic problems with bang–bang controls*, COAP 69(2) (2018) 403–422, DOI 10.1007/s10589-017-9948-z | ideas.repec.org |
| Osmolovskii–Lempio 2002 | *Transformation of quadratic forms to perfect squares for broken extremals*, Set-Valued Anal. 10 (2002) 209–232, DOI 10.1023/A:1016588116615 | web search (Bayreuth eref 63407) |
| Maurer–Osmolovskii 2003 | Control Cybern. 32(3) (2003) 555–584. The report gives only the year; add the venue in Sources. | geodesic.mathdoc.fr CC_2003_32_3_a8 |
| Maurer–Pickenhain 1995 | *Second-order sufficient conditions for control problems with mixed control-state constraints*, JOTA 86 (1995) 649–667, DOI 10.1007/BF02192163 | web search (Springer) |

The inline citations in Remark 2.5, after Proposition 3.1 and in the novelty paragraph are
correct. Only the Sources section is wrong (R3) or incomplete (M6).

## Claims not strengthened

- Every changed statement is equal to or weaker than the original: a converse restricted to
  attained `f*`, a smaller radius, a rate marked unverified, extra hypotheses, window exactness
  assumed, and a sketch marked incomplete.
- The new numbers match [V]'s logs.
- The status line says "verified with fixes", and Section 9 lists what [V] did not check.
- One overstatement of completeness remains. Section 9 says the root applied [V]'s findings, but
  R1–R3 and M3 were not applied.

## Commands run

These are targeted checks only: no project-wide verification, no CI inspection, no commits, no
edits to files under review. `OMP_NUM_THREADS=1` was set for the one numpy read.

1. Extracted the root's first saved text of `report.md` from the root session transcript (the
   `Write` tool call) into a scratch file in `/tmp`, ran `diff` against the current file, then
   deleted the scratch file.
2. `python3` reads of `reviews/bangbang-verification/logs/{qcal_exact,primal_check,states_check}.json`
   and `window_toy_k-0.5_{box,reach}.json`.
3. `OMP_NUM_THREADS=1 timeout 60 python3 -c ...` to print `pv[3090:3095]` from
   `theory-bangbang/logs/optcdeg2_qcal_data.npz`.
4. `grep` of `report.md` for out-of-date items and for references to [E].
5. Read [E], `reviews/bangbang-n2-review.md` (relevant parts) and
   `reviews/ext-bangbang-n2-confirm.md`.
6. Web: the Bayreuth eref record 63114; RePEc records for COAP 69(3) and 69(2); searches for
   Osmolovskii–Lempio, Maurer–Osmolovskii (2003) and Maurer–Pickenhain (1995).

## Sources

- https://eref.uni-bayreuth.de/63114
- https://ideas.repec.org/a/spr/coopap/v69y2018i3d10.1007_s10589-017-9969-7.html
- https://ideas.repec.org/a/spr/coopap/v69y2018i2d10.1007_s10589-017-9948-z.html
- https://eref.uni-bayreuth.de/63407 (Osmolovskii–Lempio record, via search)
- https://geodesic.mathdoc.fr/item/CC_2003_32_3_a8/
- https://link.springer.com/article/10.1007/BF02192163
