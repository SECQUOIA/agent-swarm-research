# Critique of dossier `dtoc5-optcdeg2.md` (dtoc5 and optcdeg2)

Written 2026-10-04 by an independent critic. Nothing under `R/` (`research-20260929/`) or
`literature/` was edited, and no script was run in the main tree. All checks ran on copies in
`/tmp/critic2-dtoc5-optcdeg2/`, one core each. Line numbers refer to the dossier file.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.** I tried to refute both certificates
and both primal points and could not:

- **dtoc5.** The dual identity and the bracket hold. My own code (not the dossier's) evaluated
  d(λ̂) by two routes:
  - the closed form, with each division term rounded up on the grid 10^-80;
  - the completed-square identity f(x̂) − d(λ̂) = Σ(squares), with each term rounded up on the grid
    2^-400.

  Both give d(λ̂) ≥ 5.38967211918114046742396649913627186883131268933631; they agree to 2.5e-76.
  Both confirm the dossier's gap of 7.205e-43 and the localization radius sqrt(gap/h) = 1.898e-19.
  The committed point satisfies λ̂_t < 0 for t ≤ T−2 (min û_t = 1.46e-5) and λ̂_{T−1} = 0.
- **optcdeg2, lower bound.** I re-derived Lemma 2 (telescoping), Lemma 4 (y- and u-elimination:
  A2, B0, K2, K1', K0, F) and the rigor of `v_qcal_exact.py`'s univariate minimizer:
  - Sturm isolation, sign-change brackets and the slack bound G ≥ min(G(l), G(r)) − M2·w²;
  - the superset R*;
  - stage 0 and the terminal term;
  - floor-summing.

  I also read `v_states.py`: branch choice, Newton-from-below for g⁻¹, outward rounding. All are
  correct. Further checks:
  - **Falsification search.** For 197 stages (both switch windows, the min-v region, both ends, 150
    random), an independent search tried to find a point below the exact stage minimum m_t.
    It computes min_y ρ from the definition by an exact parabola fit, samples v over V_t, tries five
    u values and refines by golden-section search. It found **no violation**; the best values found
    lie within 2.8e-29 of m_t.
  - **Stage losses.** I recomputed all 49,999 stage losses exactly. They are all ≥ 0 at the
    2^-300-rounded trajectory and sum to 8.97808636864563e-16, as the reviewer's diagnostic found.
  - **Data claims.** All dossier statements about the npz data hold: q_0 = −34.100, q_N = 0.2863,
    p^v_1 = 124.09, p^v_3092 = 7.60e-12, p^v_N = 0.5952523741, p^y_N = −3.857e-4, c = v̄,
    q ≡ 0 on 3091..47291, minimum A2 = 1.999989e-4. Both q-recursions with κ_H = 1 and κ_T = 0.05
    reproduce the stored q exactly.
- **optcdeg2, primal.** I reviewed `optcdeg2_primal_int.py` line by line and re-ran a copy:
  - floor/ceil scaling, the interval square and the interval product with a positive constant are
    correct;
  - the intermediate value theorem argument and the feasibility checks are complete;
  - the result reproduces the log.
- The reruns of `v_states.py` and `v_qcal_exact.py` (`rerun_reviewer_*.json`) are identical to the
  stored logs, apart from run time.

## Corrections (location, problem, evidence, fix)

1. **Lines 24, 526, 694: the objective display "± 5e-64" is wrong.**
   - *Problem.* `optcdeg2_primal_int.py` prints J_lo and J_hi truncated to 45 decimals. The stated
     ±5e-64 (or "+4.8e-64") around the 45-decimal string does not contain the enclosure.
   - *Evidence.* With 70 decimals, J ∈ [293.8760750958750932772142114247080159340995594910468423450803583390…,
     …3394867…]. That is 4.7e-47 above the displayed …559491. The check
     `display + 5e-64 >= J_hi` is False.
   - *Fix.* Write J = 293.876075095875093277214211424708015934099559491047 (all digits shown are
     correct; enclosure width 4.7e-64), or give the endpoints. The 20-decimal upper bound
     293.87607509587509327722 is unaffected.
2. **Line 871 (Table 10.4): unsafe display of the exact lower bound.**
   - *Problem.* "same calibration, exact | 293.87607509587509238" is rounded **up**.
   - *Evidence.* The certified value is 293.87607509587509237940(55…); see `bound_str` and the
     diagnostic's 25-digit LB. 293.87607509587509238 lies inside [LB, UB], so it is not a proved
     lower bound.
   - *Fix.* Use 293.87607509587509237, consistent with the dossier's own "every display is on the
     safe side".
3. **Lines 884–886 and DO-11 (line 799 onward): "all other stage losses below 1e-24" is false at
   stage 47290.**
   - *Evidence.* My exact recomputation of all stage losses, at the same 2^-300-rounded trajectory as
     `diag_stage_losses.py`:
     - stage 3091: 8.9777e-16;
     - **stage 47290: 4.0776e-20**;
     - all others ≤ 7.2e-25.
   - *Why.* p^v_{47291} = −9.72e-16 and u_47290 = 0.0951. So the affine u-term costs
     h·|p^v|·(1/5 − u) = 4.08e-20.
   - The same wrong sentence is in `R/reviews/bangbang-verification/verification-report.md`
     (A.5). The saved `diag_stage_losses.log` is tail-only and does not support it.
   - *Fix.* Say "below 1e-24 except stages 3091 (9.0e-16) and 47290 (4.1e-20)".
   - Two cost corrections:
     - DO-11: after polishing p^v_{3092}, stage 47290 would limit the gap, so p^v_{47291} needs
       polishing too.
     - Figure 6: an exact all-stage loss computation takes about 23 s, not 4 min.
4. **Line 587 and line 739 (DO-4): the diagnostic trajectory is not exactly feasible.**
   - *Problem.* The trajectory is rounded to 2^-300 at each step and uses u_47290 truncated to 25
     digits.
   - *Evidence.* My replica gives v_N = 3.1e-31 ≠ 0.
   - *Fix.* Write "a 2^-300-rounded, near-feasible version of the certified trajectory". It remains
     a valid consistency check: all losses are ≥ 0, and they sum to J − LB.
5. **Lines 42 and 599 (and line 813): "textually identical" to QPLIB_8585 is contradicted by the
   cited log.**
   - *Evidence.* `checks/qplib_dtoc5_optcdeg2_identity.log` gives different sha256 hashes
     (4fc80f6b… vs 2b29e517…). After comment removal, the files still differ in `m.tolproj`
     formatting and in the solve statement (NLP vs QCP).
   - *Fix.* Write "identical apart from comment lines and the solve statement", as the dossier
     already does for optcdeg2/QPLIB_8803.
6. **Line 280 and line 843: the uniqueness of the dtoc5 minimizer does not need an exact KKT pair.
   It follows from the dossier's own localization.**
   - Reduce the problem to y_1..y_T, with u_t = (y_t − y_{t+1})/h + 4y_t². The reduced Hessian
     satisfies zᵀ∇²f z / (2h) = Σ_{t=1}^{T−1}(1 + 8u_t) z_t² + Σ_t (∇u_t·z)².
   - This is positive definite wherever 1 + 8u_t > 0: if z_1..z_{T−1} = 0, then ∇u_{T−1}·z = −z_T/h.
   - All minimizers lie in a box of radius about 4e-19 around x̂. On that box u_t ≥ −4e-14 for
     every t, since û_t ≥ −2e-26 and Δu ≤ 2·4e-19/h.
   - So f is strictly convex on a convex set containing every minimizer. Attainment then gives a
     unique minimizer.
   - *Fix.* Either add this paragraph and state uniqueness as proved, or delete "would require an
     exact KKT pair". The "must not claim uniqueness" item then changes accordingly.
7. **Lines 626–627: wrong slugs for Lincoln–Rantzer.**
   - The slugs `rantzer2005-…` and `rantzer2006-…` are Rantzer's solo switching-systems papers.
   - The Lincoln–Rantzer paper is `lincoln2006-relaxing-dynamic-programming` (IEEE TAC 51(8) (2006)
     1249–1260; in the knowledge base since 2026-09-12, status read).
   - *Fix.* Cite that slug. Cite the Rantzer papers only as Rantzer.
8. **Line 786 (DO-9): "None is in literature/" is now outdated.**
   - `krotov1967-sufficient-conditions-for-the-optimality` (Doklady 172(1):18–21) and
     `mangasarian1966-sufficient-conditions-for-the-optimal` (SIAM J. Control 4:139–152) are now
     present with read full text. Both were added on 2026-10-04, after the dossier's check files.
   - `arrow1970-public-investment-the-rate-of` exists only as an unread metadata stub.
   - Jeyakumar–Rubinov–Wu, Leitmann–Stalford, Maurer–Pickenhain, Osmolovskii–Lempio,
     Maurer–Osmolovskii, Tamminen and Sydsæter et al. are still absent.
   - *Fix.* Update DO-9 and cite the two new slugs.
9. **Line 604: Waki et al. locators are preprint pages.**
   - "problem (39), p. 30, Table 12" are printed pages of Research Report B-411. Table 12 is on
     p. 31. They are not pages of SIAM J. Optim. 17:218–242, which `R/publication/literature/control/report.md`
     lists as not read.
   - The caveats should travel with the citation: SeDuMi floating point; a random objective
     perturbation |p_j| < 1e-5; possibly added bounds; Table 12 prints no objective values.
   - *Fix.* Label the locators as preprint pages and add the caveats.
10. **Line 609: "The DTOC5.SIF SOLUTION lines are tolerance artifacts" overstates the source.**
    - The control report says "tolerance artifacts **or come from a different version of the
      model**".
    - The evidence is floating point and concerns the h variant.
    - *Fix.* Keep both alternatives and label the evidence "floating point".
11. **Lines 399 and 434: equality versus lower bound.**
    - Lemma 4: with R* "any interval containing" the vertex set, the formula gives m_t ≥ min(…), not
      m_t = min(…). Equality holds only for the exact set.
    - Theorem 2: B = Σ⌊m_t⌋ should be B = ⌊m_0⌋ + Σ⌊m̃_t⌋ + ⌊m_N⌋. Here m̃_t ≤ m_t are the computed
      rigorous lower bounds; the bracket slack is ≤ 9.5e-29 per seeded bracket.
    - Likewise, "exact certificate value" (line 548) means the rigorous evaluation of the
      certificate, not the exact infimum.
12. **Lines 111 and 136: "optimal trajectory" and "the optimal control is bang-bang" describe the
    certified feasible point, not a proved property of the optimizer.**
    - *Fix.* Say "on the certified trajectory".
    - Optionally prove near-bang-bang structure (see A3 below).
13. **Line 537: "because repairing the rows lowers the value" is a heuristic explanation.**
    - The rigorous point is not the float point with its rows repaired. It has exact ±1/5 controls
      and a re-solved u_47290.
    - The verified fact is only that it lies 5.96e-12 below the float value.
    - *Fix.* State the fact, and give "row violations of about 1e-16 times costates of about 100" as
      a plausible explanation.
14. **Line 538: incomplete.** The first-wave point 293.876075095886 also violates the rows by
    8.9e-16, not only the bound by 1.1e-17 (first-wave verification report).
15. **Line 303 versus Table 10.4: inconsistent affine numbers.**
    - The affine float-screening loss of 0.6258 (refined costates) does not match the certified
      first-wave affine bound 293.2500703 (first-wave multipliers), whose gap is 0.6260. The two
      differ by 2.4e-4.
    - *Fix.* Say which multipliers each number uses.
16. **Lines 817–819: imprecise wording in the may-claim sentences.**
    - "zero up to rounding of the data" should read "at most 7.3e-43 (zero if an exact KKT pair
      exists, which is not proved)".
    - "an interval of width 7.3e-43 around 5.3896721191811404674239664991362718688313": this
      40-decimal value lies 1.3e-42 *below* the interval. Give the endpoints instead.

## Assessment of the dossier's issue list

- **DO-1 is minor, not major.**
  - The display 5.38967211918114 is already independently verified (first verifier) and is listed
    in the reproduction README with the reviewer command `v_dtoc5.py` (18 s).
  - That command is deterministic. Regenerated multipliers that differed in their last bits would
    move d(λ) by about 1e-24, far inside the 4.67e-16 display margin.
  - The new exact certificate is a real improvement: no mpmath, a bracket of 7.3e-43, and replay
    from a committed file. It is not the repair of a major gap.
  - Its independent review is now partly done: the critic's two-route recomputation above, plus a
    re-derivation of Proposition 1.
- **DO-2, DO-5, DO-6, DO-7, DO-8, DO-10: agreed.**
- **DO-3: agreed, with one addition.** `v_states.py` and `v_qcal_exact.py` (and `v_dtoc5.py`)
  write into their own `logs/` directories, and `v_qcal_exact.py` also needs the author's
  `optcdeg2_qcal_stage_lb.npy`. The replay instructions must say to run on copies. The README
  already marks regeneration as optional ("if generating the final calibration again is desired").
- **DO-4: agreed.**
  - Correct the "exactly feasible trajectory" wording (correction 4).
  - Add the critic's 197-stage falsification search as further partial evidence.
  - The cost estimate (half a day of agent work, under 1 min of compute) is plausible. A
    search-based check of all stages, by contrast, would take about 1.5 h on one core.
- **DO-9: outdated** (correction 8).
- **DO-11: correct cost, incomplete diagnosis** (correction 3). Stage 47290 is the next limit
  (4.1e-20), and changing u_3091 requires re-running the 1.5 s primal proof.

## Additional issues

- **A1.** Stage-47290 loss: see correction 3. The wording in the source verification report needs
  the same fix.
- **A2.** Uniqueness of the dtoc5 minimizer is provable in one paragraph (correction 6).
- **A3 (optional strengthening, cheap).**
  - On stages 3091..47290, q_t = q_{t+1} = 0, so ρ_t is affine in u with slope h·p^v_{t+1}.
  - For any global minimizer, the sum of all stage losses is at most UB − B ≤ 8.98e-16. Since
    m̃_t ≤ min_{u'} ρ_t(x_t, u'), the loss at stage t is at least h·|p^v_{t+1}|·(1/5 − u_t).
  - With min |p^v_{t+1}| = 4.37e-4 on t = 3092..47289, every global minimizer has
    u_t ≥ 1/5 − 5.2e-9 there.
  - This would make "the optimal control is bang-bang on the middle arc" a proved statement, to
    5.2e-9. The head and tail arcs need a similar argument with K2 ≠ 0.
  - Cost: about 1 hour of agent work and seconds of compute.

## Targeted checks run (critic; all in /tmp/critic2-dtoc5-optcdeg2, one core)

| command | result |
|---|---|
| `python3 my_dtoc5.py` (own code, 3.3 s) | rows exact; f(x̂) equals the stored rational; d(λ̂) ≥ …1268933631 by two routes (agreement 2.5e-76); gap 7.205e-43; radius 1.898e-19; only û_{T−1} < 0 |
| `python3 my_data.py` | all npz data claims confirmed; q-schedules reproduce the stored q exactly |
| `python3 prim.py` (copy of `optcdeg2_primal_int.py` plus 70-digit output, 1.2 s) | log reproduced; the ±5e-64 display is refuted (correction 1) |
| `python3 q/falsify.py` (21 s; imports a /tmp copy of `v_qcal_exact.py` for m_t only) | 197 stages, 0 violations; best − m_t ≤ 2.8e-29 |
| `python3 q/losses.py` (23 s) | all 49,999 losses ≥ 0; sum 8.97808636864563e-16; stage 47290 = 4.08e-20 |
| `diff` of `rerun_reviewer_*.json` against stored logs | identical (apart from run time) |
| `grep` census of the OSIL copies | 99,998 objective coef 2e-5; 49,999 coef 8e-5; 49,999 linear −2e-5; one `mult="2">-4e-4`; hashes ac7b2d94…, 6a9bcd91… |

These are targeted local checks only. No CI or project-wide verification was run or inspected.
