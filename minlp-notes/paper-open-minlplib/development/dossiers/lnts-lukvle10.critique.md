# Critique of the dossier `lnts-lukvle10`

Critic: independent reviewer, 2026-10-04. R below means `research-20260929/`.
Scripts and logs of this critique: `checks/lnts-lukvle10-critique/` (run only
from a scratch copy; the runs below used `/tmp/critic-lnts-r2`, one core).

## Verdict

**Corrections needed; nothing invalidates a claimed result.**

- Both certificates (Proposition 2 for lnts; Theorem 4 with Lemma 5 and the
  verifier's interval B&B for lukvle10) are sound. I re-derived every proof step
  and read the verifier's B&B code line by line.
- **Theorem 3 (lnts exact optimum) is correct.** I re-derived the proof and
  re-implemented the computation with different arithmetic and a different
  bracket. Both implementations agree for all four N. The independently proved
  primal points agree with the optimum to at most 3.5e-58.
- The main correction is an overclaim in L8 and in the proposed lukvle10
  wording. Saying the dual value agrees with f(x*) "to about 1e-19" is not
  supported. The rest are attribution, rounding-convention and citation fixes.

## What I checked

| check | how | result |
|---|---|---|
| Lemma 1, Prop. 2, Theorem 3 proofs | by hand: closed form of c, reflection identity, E1–E3 at θ*, S(μ*,ν*) = A(h*) + ν*B(h*), monotonicity, IVT enclosure | correct |
| Theorem 3 computation, second implementation | `thm3_iv.py`: mpmath `iv` at 130 digits (outward), c_j from an impulse simulation of the recursion (not the closed form), own bisection root, asymmetric bracket [ν − 3e-66, ν + 7e-66] | sign change for N = 50, 100, 200, 400; optimum enclosures of width 2.8e-65 to 2.3e-64, inside the dossier's 40-digit intervals |
| symmetry ansatz μ* = −ν*N/2 | free Newton on (μ, ν, h) without the ansatz, 80 digits | μ + νN/2 ≈ 1e-88; N·h equals the Theorem 3 value to 45 digits |
| Prop. 2 tightness | S − ν*B(h*) − A(h*) at the root | about 1e-135 (zero to working precision) |
| cross-check with the independent primal proof | stored 60-digit h enclosures in `primal/lnts/points/lnts<N>_point.json` | N·h encloses the optimum for all four N; the deviations are at most 3.5e-58 |
| dossier script | `lnts_exact_opt.py` rerun in scratch | reproduces the dossier log (0.67 s) |
| verifier lnts code | `v_lnts.py` | mpmath `iv.mpf(mpf)` conversion is outward (`convert_mpf_` with floor/ceiling), so the 50-digit check covers the exact 60-digit μ, ν, h2 |
| verifier lukvle10 B&B | `v_lukvle10_bnb.py` read in full | box reduction, monotone power ranges, mean-value form (centre inside box by monotone rounding), chain rule through P and P², pruning, stopping and summation are all valid |
| lukvle10 sum | 64-bit `iv` replay of the verifier's summation | lower end 352.2380254050784556541; display ...784 valid, ...785 not |
| λ̄, Hessian | `lukv_checks.py`, 40 digits | λ̄ = (3 − ln 2)/(4√2) = 0.40779781795634224; binary64 value lower by 5.65e-16; eigenvalues 2.3487, 2.5734 |
| multiplier deviation | verifier's binary64 λ (after replacement) vs the primal track's 40-digit KKT multipliers, j < 994 | max 2.04e-14, ℓ2 norm 2.9e-14 |
| numbers against sources | part_a.json, lnts_verify.json, lukvle10_bnb.json, gap-values.json, solver-run table, COPS and Göß–Burlacu–Martin full texts | all match except the items listed below |

## Corrections

**C1. L8 and the proposed lukvle10 wording overstate the numerical evidence.**
- *Location:* §8.2 L8 ("strong numerical evidence that, at these multipliers, the
  partial Lagrangian dual value equals f(x*) to about 1e-19"). Also the
  `proposed_resolution` of issue `lukvle10-duality-gap-wording` ("numerically
  the partial Lagrangian dual value agrees with f(x*) to about 1e-19").
- *Problem:* the 1.5e-19 agreement measures the Lagrangian at the KKT pairs, not
  its minimum.
  - `bnb()` in `v_lukvle10_bnb.py` initializes the incumbent at the p5 pair:
    `U = hi(prob.point(x0[0], x0[1]))`.
  - The middle group's UB, −0.1084888547261358341, is the value at the saddle
    pair (−0.1084888547261358344 with the binary64 λ̄, up to 64-bit rounding).
  - So ΣUB + Σλ is the partial Lagrangian evaluated at (near-)KKT pairs. It
    equals f(x*) to about 1e-19 because the Lagrangian is stationary there and
    |λ − λ_KKT| ≤ 2.0e-14. That holds for any near-KKT multipliers and says
    nothing about the minimum over R².
  - The dual value is known only to lie in [f(x*) − 1.42e-9, f(x*)].
  - The float searches support "no lower basin found" only to float accuracy,
    about 1e-16 per subproblem. The verifier ran one Nelder–Mead start per
    problem from a 1201² grid minimum; the authors ran 20 starts on a 1501² grid.
- *Fix:* replace with: "The remaining gap, at most 1.42e-9, equals the summed
  branch-and-bound tolerances. The B&B incumbents never fell below the
  Lagrangian values at the KKT pairs, and floating-point multistart searches
  found no lower point. The dual value is known only to within 1.42e-9 of
  f(x*), and global optimality of x* is not proved." Drop "to about 1e-19".

**C2. The lnts50 listed relative gap is rounded down.**
- *Location:* §2 table ("3.8e-5 rel."), §7 ("within 3.8e-5 relative").
- *Evidence:* exact (0.55466876 − 0.55464755)/0.55466876 = 3.8239e-5; with the
  optimum as primal, 3.8248e-5.
  - `integration-review-r2.md:86` flagged "within 3.8e-5" as false as a bound.
  - The summary (line 355) and READINESS (items 12 and 2) now use 3.9e-5.
- *Fix:* write 3.9e-5 (upward), or "about 3.82e-5".

**C3. The Göß arXiv paper is in literature/.**
- *Location:* §7 ("Göß, arXiv:2603.16505v1 ... not in literature/").
- *Evidence:* `literature/papers/go2026-clash-of-minlp-relaxations-piecewise/fulltext.md`.
  Table 4 is on p. 32, lnts rows at lines 942–945.
- *Fix:* cite `[[go2026-clash-of-minlp-relaxations-piecewise]]`, p. 32.

**C4. Theorem 3 is not entirely "new in this dossier".**
- *Location:* §3.1 heading of Theorem 3; §0 item 2.
- *Evidence:* two earlier project notes already state the zero-gap mechanism,
  without a closing argument or an enclosure.
  - `R/theory-coupling/coupling.md` §7.2 says the lnts three-row Lagrangian
    "has no duality gap" (concave image boundary, convexification argument).
  - `R/theory-consistency/consistency-relaxations.md` §5.1 calls lnts an exact
    affine split ("from the linear-tangent structure").
- *Fix:* the new parts are the following, and the earlier observation should be
  cited:
  - the explicit attaining control with μ* = −ν*N/2;
  - the scalar equation g(ν) = 0;
  - the rigorous enclosure.

**C5. The 7e-26 consistency figure is misattributed and too weak.**
- *Location:* §4 lnts "Alternative" and §8.1 L2 ("within 7e-26 of the optimum,
  consistent with their rounded interior controls").
- *Problem:* 7e-26 is the width of the stored 25-digit objective display, not an
  effect of the controls. Rounding the controls to 40 digits (error at most
  5e-41) changes h only at second order, about N·(5e-41)² ≈ 1e-79, because the
  point is optimal.
- *Evidence (misc_checks.log):* the stored 60-digit enclosures of h contain the
  optimum. N·h_enc − opt_lo lies within [−1.2e-59, 3.8e-59], [−8.8e-59, 1.2e-59],
  [−2.9e-59, 1.7e-58] and [−3.5e-58, 5.0e-59] for N = 50, 100, 200, 400.
- *Fix:* report this comparison instead. It cross-validates two independent
  proofs (Krawczyk primal and Theorem 3) to about 1e-58.

**C6. The size of |g| at the bracket ends is misstated.**
- *Location:* §8.1 L2 ("|g| ≈ 1e-58").
- *Evidence:* `lnts_exact_opt.log` gives 7.8e-59, 6.2e-58, 5.0e-57 and 4.0e-56
  for N = 50 to 400.
- *Fix:* "between 8e-59 and 4e-56".

**C7. The q range omits q_0 and q_995.**
- *Location:* §3.2 "Hypotheses actually used"; §8.2 L6.1; issue
  `lukvle10-hidden-hypotheses`.
- *Problem:* q_0 = −2λ_{−1} = 0 and q_995 = 0. The full range is [−0.8156, 0].
  `lukvle10_sum.py` computes q only for k = 1..994.
- *Effect:* none on validity, since q > −1 and q ≤ 0 still hold.
- *Fix:* state q_k ∈ [−0.8156, 0].

**C8. The L4 rounding excess is attributed to the wrong document.**
- *Location:* §8.1 L4.
- *Problem:* the 2.96e-17 and 3.26e-17 in `minor-fixes-review-r2.md:97` are
  measured on the verification report's 16-digit 1e-10-margin displays against
  the verifier's 60-digit h2. They do not come from `lnts_bound.py` output.
- *Evidence (misc_checks.log, exact):*
  - The author's JSON float duals all lie below the author's own N·h2, by
    1.7e-17 to 4.9e-17.
  - The open-instances report's 15-digit decimals exceed the author's N·h2 for
    lnts100 (+3.9e-16) and lnts400 (+1.6e-16).
- *Fix:* correct the attribution. The conclusion (never quote these values) is
  unchanged.

**C9. Agreement with the COPS values holds only under truncation.**
- *Location:* §7 ("agreeing with our optima to the printed digits").
- *Evidence:* the lnts50 optimum 0.5546688 rounds to 0.554669. COPS 2.0 prints
  5.54668e-01 for MINOS, SNOPT and LOQO. MINOS's violation is 2.5e-13, so COPS
  evidently truncates.
- *Fix:* "agree after truncation to six digits", or "to within one unit in the
  sixth digit".

**C10. The source of the summary's lukvle10 primal is misdescribed.**
- *Location:* §0 item 4; §5; §8.4.
- *Problem:* MINLPLib displays p5 as 352.2380254. The value 352.2380254064961
  is the verifier's 16-digit nearest display of p5's coordinate-evaluated
  objective, 352.23802540649613695, and is therefore rounded down. It is a valid
  upper bound on the optimum only because f(x*) ≤ 352.23802540649562264.
- *Fix:* adjust the wording. The recommendation to display 352.2380254064957 stands.

**C11. The p5 residual difference has a likely explanation.**
- *Location:* §1.2 ("The difference is unexplained").
- *Evidence:* the p5 `.sol` file has 15 decimals.
  - Rounding to 15 decimals (≤ 5e-16 per coordinate) gives row residuals up to
    about 4.4e-15.
  - The middle rows alone give 1 − 2(0.707106781186548)² ≈ −1.4e-15.
- *Fix:* "consistent with the 15-digit rounding of the .sol text; MINLPLib
  probably evaluates the full-precision point".

**C12. The L10 leaf count and recheck scope need correcting.**
- *Location:* §8.2 L10; issue `lukvle10-mpmath-dependency`.
- *Leaf count:* the B&B evaluated 329,233 boxes, of which about 164,634 are
  leaves (pruned or open; leaves = (boxes + 1)/2 under bisection). At the
  dossier's 2–4 ms per leaf, the re-bounding costs 6–11 CPU minutes, not 15–30.
- *Scope:* a leaf recheck must also
  - recheck the box-reduction radii, whose U uses `exp`/`log`;
  - confirm that the leaves tile the root box.
- *Simpler route:* rerun a scratch copy of `v_lukvle10_bnb.py` with `iv.exp`
  and `iv.log` replaced by integer-only interval enclosures. These follow by
  monotonicity from the existing point routines. No leaf dump is needed.
- *Fix:* correct the leaf count, cost and scope.

**C13. L9 uses the wrong perturbation size.**
- *Location:* §8.2 L9 ("|δλ| ≤ 2.4e-14").
- *Problem:* the second-order loss depends on the deviation from the exact KKT
  multipliers, not on the spread of the middle multipliers.
- *Evidence:* against the 40-digit KKT multipliers the deviation is max 2.0e-14,
  ℓ2 2.9e-14. The estimated loss is about 1e-27 to 1e-25.
- *Fix:* cite this deviation. The conclusion is unchanged.

**C14. The "width below 1e-60" claim does not match the printed digits.**
- *Location:* §3.1 table; §9.
- *Problem:* the displayed decimal intervals have 40 digits (width 1e-40). The
  widths 5.6e-62 to 4.5e-61 belong to the rational enclosures.
- *Fix:* print at least 62 digits, or state that the enclosure is rational.

## Additional issues

1. **Theorem 3 now has a second implementation** (minor; positive).
   - The dossier's integer arithmetic and my mpmath `iv` code use different
     trust bases, and they agree.
   - Both agree to about 1e-58 with the independently proved primal points.
   - The orchestrator should decide whether this critique counts as the
     required independent review, or whether a separate reviewer should still
     sign off. The CPU cost is seconds either way.
2. **"min ψ" in Lemma 5(3) should be "inf ψ"** (minor). φ, and hence ψ, jumps
   at |t| = 1. The lower bound m_ψ is still valid.
3. **The lnts100–400 p1 comparison remains open** (minor; as the dossier says).
   The lnts400 p1 has listed infeasibility 3e-10, comparable to lnts50's
   9e-10, so it is the most likely to lie below the optimum. The three .sol
   files are a seconds-long check.

## The dossier's proposed resolutions and cost estimates

| item | assessment |
|---|---|
| Adopt Theorem 3 (L2) | Supported. Proof and computation are confirmed here. Add the coupling.md attribution (C4) and the 60-digit primal cross-check (C5). |
| lukvle10 displays (L7; summary primal) | Correct. Use 352.2380254050784 and 352.2380254064957. |
| lnts50 p1 remark (L3) | Correct (4.245e-11 below the dual display, 4.30e-11 below the optimum). |
| Duality-gap wording (L8) | Needs C1: the proposed replacement sentence itself overclaims. |
| L9 refinement | Sound in outline. The cost (one person-day, under 15 CPU minutes) is plausible. The tail τ has an unknown Hessian, so choose r per problem from an interval Hessian. |
| L10 mpmath removal | Sound in outline. The leaf count is overestimated by 2×, and the scope omits the radius step and tiling (C12). |
| L11, 352.152 | Correct. The report says the 0.086 gap "sits in pairs 497–498"; this is also only a floating-point statement. |
| Hidden hypotheses (L6) | Correct, apart from the q range (C7). |

## Confirmed without change

- Model statements of both instances.
- All listed duals, primals, dates and metadata values in §2.
- Verifier margins, N·h2 and the 5.55e-13 bound against N·h2.
- gap-values.json cells and relative gaps (1.05e-12, 1.11e-12, 1.06e-12,
  1.06e-12; 4.03e-12).
- B&B statistics: box counts, radii, LB/UB, Σλ, open boxes, 300.35 s.
- λ̄ and the middle-pair value.
- The solver-run numbers.
- Göß–Burlacu–Martin Tables 11 and 17 (5811.5 s; SCIP gaps 0.0251–0.1033).
- COPS 2.0 and 3.0 values; LANCELOT lnts100 and lnts400 below the optimum.
- SIF SOLTN 1.03e-3 below the bound.
- Richardson extrapolation 0.55457088 with ratios 3.990 and 3.995.
- The Lindemann–Weierstrass argument.

## Commands run

All runs were in `/tmp/critic-lnts-r2` on copied inputs, with one core. No
script was run inside the repository, and nothing under R/ or literature/ was
modified.

- `OMP_NUM_THREADS=1 python3 thm3_iv.py 50 100 200 400` (11 s)
- `OMP_NUM_THREADS=1 python3 misc_checks.py`
- `OMP_NUM_THREADS=1 python3 lukv_checks.py`
- `OMP_NUM_THREADS=1 python3 lnts_exact_opt.py 50 100 200 400` (the dossier's
  script, rerun on a copy; 0.67 s)
- Inline 64-bit `iv` replay of the verifier's lukvle10 summation.
