# Confirmation of the second revision of `theory-bangbang/report.md`

Date: 2026-09-30. Referee: independent. I did not write the report, the
verification, the round-1 confirmation or either revision. Scope: the 14
round-1 items (R1–R5, M1–M7) and the reviser's list of applied changes
(Section 9.2 of the report). Scripts and logs:
`reviews/bangbang-root-fixes-confirm-r1-checks/` (`c_checks.py`,
`logs/c_checks.log`).

## Verdict

**All 14 items are applied correctly, and every changed number reproduces.
One new sentence in Remark 3.3 claims more than [E] supports, and it is
false for the global form (issue 1). Two small edits remain (issues 2
and 3).** Nothing is refused, so there are no refusals to judge. Apart from
issue 1, no claim was strengthened.

I recomputed the numbers with my own script from the raw stored files: the
certificate JSON, the verifier's `primal_check.json` and `qcal_exact.json`,
the certificate data `.npz`, the refinement and exploration logs, and the
verifier's toy logs. I did not reuse the reviser's `revision2_checks.py`. I
checked the bibliographic data against Crossref, the mathdoc record, and the
first page of the univaq PDF and of the Maurer–Osmolovskii PDF. I re-derived
the revised proofs (Proposition 3.1, Theorem 2.3) line by line.

## Item-by-item check

| item | result |
|---|---|
| R1 gap | Correct. In exact rationals, the quoted upper bound minus the stored double 293.8760750958728 is 2.2865e-12 (7.78e-15 relative). The upper end of the verifier's enclosure gives the same value, and the quoted upper bound 293.87607509587509328 lies above that end (by 2.8e-18). The author's float point is 5.956e-12 above the enclosure end and 8.242e-12 above the bound. The Summary, the Section 5.5 table and the Section 5.5 text now use 2.3e-12. The "not bounded" sentence is replaced by the verifier's result that repairing the rows lowers the value. 8.3e-12 appears only as the value the earlier version used. |
| R2 `p_v(3092)` | Correct. `pv[3092]` in `optcdeg2_qcal_data.npz` is 7.599e-12, `refine_primal.log` gives 6.185e-12 and `explore1.log` gives −1.151e-3. The certificate script computes the costates backward from the refined controls (`pv[t]` at index `t`), so the `.npz` value is the certificate data. The stage-3091 loss before refinement was 7.28e-8 (explore1, `kh > 0`). |
| R3 Sources | Correct. Crossref gives DOI 10.1007/s10589-017-9948-z as Scarinci–Veliov, COAP 69(2) 403–422. Page 1 of the univaq PDF shows the same paper. The "Alt et al. … (title from memory)" entry is gone, and the Sources section now agrees with Remark 2.5. |
| R4 Prop. 3.1 | Correct. The one-sided regularity is now on `∂_tS` and `∇_x∂_tS`; `S`, `S_x` and `S_xx` are continuous; and `r ≥ 0` is assumed for `t ≠ τ`. I re-derived the proof on each side. Step 1 gives `r(t,x*(t),u) = σ(t)(u − u*(t)) → 0`. Step 2 gives zero gradient at the interior minimum of `r^+(τ,·,u) ≥ 0`. Step 3 uses the `u`-slope `∇_xσ_S = ∇ℓ_1 + b_xᵀS_x + S_xx b`, which contains no `∂_tS`. Step 4 gives `S_xx b − w`. Each step holds. Section 0 now writes `∂_tS`. |
| R5 Remark 3.3 and pointers | Applied. The label "a conjugate point" and the phrase "not worked out" are removed. The three points of [E] match [E]'s Summary, Theorems 1–2, Corollaries 3 and 7, Lemma 14 and Proposition 15, including the numbers (`η_L = −0.429`, `D = 3.066`, `F'' = 1.350`; Example C `η_L = +0.202`, `t_b = 0.352`, float). The Summary, the Section 6 open list, the status table and the end of Section 9.1 now point to [E]. One new sentence goes too far: see issue 1. |
| M1 Thm 2.3 | Correct. (W2) is stated on `|t − τ| ≤ δ_σ`, and part (2) uses `δ_1 = min(δ_*, δ_β, δ_σ)`. In part (1), for `s ≤ min(δ_σ, γ_1μ/(4ΔL²))`, `(a+b)² ≤ 2a² + 2b²` gives `ΔL²s²/μ ≤ γ_1 s/4`, which yields the stated inequality. Part (2): `γ_2 s ≤ γ_2δ_* = Δ|β(τ)|²/(4(Λ+ΔM_s))`. On the closed interval `|t − τ| ≤ δ_β`, `|β|² > |β(τ)|²/2`, which gives a uniform margin. |
| M2 toy | Correct. Box domain: the affine family fails on 68, 135, 270, 540 and 1079 stages (0.272, then 0.270, 0.270, 0.270 and 0.26975 time units), symmetric about the switch (e.g. `[−539, 539]`). Reachable set: 17, 35, 69, 136 and 274 stages (0.068–0.070), all at relative stages ≤ 0. The tangential family fails on 0 stages in both cases. |
| M3 Cor. 2.4 | Correct. For affine `S`, `β(t) = b'(x*)ψ(t) = −w_t`, which vanishes at `τ` and is generally nonzero elsewhere, so (W5) is needed. |
| M4 Thm 4.1 | Applied. The parenthetical names `∂_tS`, and the Scope paragraph matches [E, Lemma 14, Proposition 15]. Example C has constant `b` and affine `ℓ_1` ([E, Section 6.1]), so Lemma 14 covers every `S` there. See issue 2 for a remaining gap in the regularity list. |
| M5 Sect. 5.7 | Correct. With `s1 = 3091.395` and `s2 = 47290.738`, the head arc is 1.2366, the tail arc is 1.0837, and their sum is 2.3203. |
| M6 novelty and Sources | Correct. The text now says "Related prior work". Crossref confirms Osmolovskii–Lempio (SVA 10(2–3) 209–232), Maurer–Pickenhain (JOTA 86(3) 649–667, same title), Alt–Baier–Lempio–Gerdts (Optimization 62(1) 9–32) and Alt–Felgenhauer–Seydenschwanz (COAP 69(3) 825–856). The mathdoc record confirms Maurer–Osmolovskii, Control Cybern. 32(3) 555–584. For the title, see issue 3. |
| M7 truncation | Correct. 293.876075095875092379 ≤ 293.87607509587509237940. The quoted upper bound minus the exact value is 9.006e-16; the enclosure end minus the exact value is 8.978e-16. No rounded-up form ("…09238") remains. |

## Remaining issues

**1. Remark 3.3 (lines 435–437): "the blow-up in the scalar sketch is
decided by the sign of `η_L`" is false for the global form.** The scalar
sketch is about `P̂`, the maximal backward solution of the Proposition 3.2
inequality on the whole horizon, that is, the global form. In that form the
singular term also acts on the last arc. So `P̂ ⪯ Q`, and what matters near
`τ+` is `η̂ = bᵀ(P̂b − w) ≤ η_L`, not `η_L` ([E, Theorem 8] uses `η̂`). [E]
also says that in the global form, conjugate points of the relaxed LQ
problem "can appear on both arcs" ([E, Summary item 3]). [E] claims only
that the scalar sketch "has the same gap": a blow-up can occur while the
second-order sufficient condition holds. The direction `η_L < 0 ⇒ blow-up`
does hold, since `P̂ ⪯ Q_ε`. The converse fails.

A scalar example (my `c_checks.py`; float, not certified). Take `ẋ = u`,
`|u| ≤ 1` (`Δ = 2`), cost `∫x²/2 + Φ(x(T))` with
`Φ = −0.9x²/2 + 0.399x`, `x(0) = 1.01`, `τ = 1` and `T = 2`. The extremal is
`u = −1` then `u = +1`. The minimum-principle signs hold, and
`σ̇(τ) = −0.01`, so `D = 0.02`. Then:

- `b = 1` and `w = 0`, so `η_L = Q(τ+) = −0.9 + 1 = 0.1 > 0`;
- `F''(τ) = 0.42`, by formula and by finite differences, so the SSC holds
  and [E, Theorem 2] gives local calibrations;
- the global-form `P̂` (`Ṗ = −1 + P²/|σ|`, `P(T) = −0.9`) blows up to `−∞`
  at `t = 1.587` (`ε = 0`) and at `t = 1.596` (`ε = 0.01`, `η_ε = 0.06`),
  after `τ`.

*Fix:* replace the sentence with something like: "The argument does not use
`n ≥ 2`, so the scalar sketch has the same gap: `η_L < 0` forces the blow-up
even when the SSC holds. In the global form of the sketch, `P̂` lies below
the Lyapunov solution and can also blow up when `η_L > 0`, at a conjugate
point of the relaxed LQ problem ([E, Summary item 3; Theorem 8]). In the
local formulation the sign of `η_L` decides." Line 447 ("the scalar sketch
is complete after `τ`") is fine: the sketch states a dichotomy near `τ+`, not
which case occurs.

**2. Theorem 4.1 parenthetical (lines 488–490): the regularity list does not
support the redundancy remark.** The remark "tangency in (H3) is redundant …
Proposition 3.1 then forces it" now depends on Proposition 3.1's revised
hypotheses. Those require `∂_tS` and `∇_x∂_tS` to extend continuously to
`τ` from each side. Theorem 4.1 asks only that `∂_tS` be `C¹` in `x` and
`S_xx` be Lipschitz in `t`, and says nothing about continuity of `∂_tS` in
`t`. Step (c), `∇²_xρ_t = h[r_xx + O(h + e_h)]`, also compares a difference
quotient of `S_xx` in `t` with `∇²_x∂_tS`, so it too uses time continuity of
`∇²_x∂_tS` (one-sided at `τ`). This gap partly predates the revision and
does not affect any conclusion. *Fix:* add "`∂_tS`, `∇_x∂_tS` and
`∇²_x∂_tS` continuous in `(t,x)` on each side of `τ`" to the parenthetical,
or say "given the regularity of Proposition 3.1".

**3. Sources, Maurer–Osmolovskii title (line 710): nit.** The linked PDF
(matwbn, page 1) prints the title as *Second order optimality conditions for
bang–bang control problems*. The mathdoc record, which the entry copies,
drops "optimality". Use the printed title, or note that the record shortens
it.

## Commands run

All from `reviews/bangbang-root-fixes-confirm-r1-checks/`, with
`OMP_NUM_THREADS=1`. These are targeted checks only; I ran no project-wide
verification and inspected no CI.

1. `OMP_NUM_THREADS=1 timeout 120 python3 c_checks.py > logs/c_checks.log`
   (reads stored results only, and integrates one scalar ODE; under a few
   seconds).
2. `cat logs/revision2_checks.log` in `theory-bangbang/`: the reviser's log.
   I read it for comparison only. My own values agree with it.
3. `curl` of `api.crossref.org/works/<DOI>` for the five DOIs in Sources, of
   the mathdoc record `CC_2003_32_3_a8`, and of the univaq and matwbn PDFs.
   I read page 1 of each PDF with `pdftotext`, in `/tmp`, and deleted the
   files afterwards.
