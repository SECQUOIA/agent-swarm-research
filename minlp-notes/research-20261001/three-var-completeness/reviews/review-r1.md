# Review round 1: `three-var-completeness/note.md`

Reviewer: independent research agent (did not write the note). Date:
2026-10-03. "Reviewed" here means checked by another research agent, not
journal peer review. The note and the stream's code were not edited. Reviewer
code is in `reviews/r1-code/`, logs in `reviews/r1-logs/`.

## Verdict

**Minor fixes.** I found no error in a proved statement. The proofs of the
duality remark, Lemmas 2.1, 2.3, 2.7, 2.8, 2.9, Proposition 2.2,
Corollaries 2.4 and 2.6, Theorem 2.5, Proposition 2.10, Theorems 4.2, 4.4,
4.6, Proposition 4.7, Lemma 4.8 and Remark 4.9 are correct as far as I checked.
BNW Theorem 1 is quoted with its exact hypotheses. The status labels are
right: proofs are labeled as proofs, external inputs are named, Conjecture 2.11
is labeled as a conjecture with numerical evidence, and the `COP(F_5)` probe is
labeled inconclusive. The issues below are a range gap in Proposition 2.10
(the claim survives), one overreaching sentence on solver relevance, and
several reporting inaccuracies in the numerical sections.

## Issues

| # | Severity | Location | Description | Required change |
| --- | --- | --- | --- | --- |
| 1 | Minor | Prop. 2.10 (S3, S5); `check_family_strata_symbolic.py` | The stated range `h = d1 < d2` with `d >= 0` includes `d1 = h = 0`. There the quoted minor `d1^2 (d1-d2)^2 / (...)` vanishes, and the script declares `d1` positive, so this case is not covered. The claim still holds: at `d1 = h = 0` the contact `b` moves to the origin (a vertex zero with a `y` tangency), and the system has rank 9 with minor `-2k/d3` (S3) or `-2k/(d2+k)` (S5) (`r1_s3_d1zero.py`). On S2 and S4, `d1 = 0` or `d2 = 0` turns `c` or `d` into a vertex contact. The minor `2k/d3` and the one-sided tangency argument still apply (reviewer rank checks at `d1 = 0` and `d1 = d2 = 0` give rank 9), but the proof only speaks of interior edge contacts. | Either restrict to `0 < h = d1 < d2` (and `d1, d2 > 0` on S2 and S4), or add the `d1 = 0` minor and one sentence noting that the contacts that reach a vertex are handled by the one-sided argument. |
| 2 | Minor | Sec. 2.6, paragraph after Prop. 2.10 | The note says "Numerically all of them lie outside `cl(D3)` (values over `R_D` between `-1.4e-4` and `-1.7e-3`)". The 30 stored boundary-stratum examples, including the dense run, range from `-9.4e-6` to `-1.74e-3`; `-1.4e-4` is the bound from the first run only. Also, stratum members with `d1 = 0` or `d2 = 0`, which the stated ranges allow on S2-S5, have a zero square coefficient and lie in `cl(D3)` by Corollary 2.4 (ii). | Correct the range. Say "all stored examples" and note the `d_i = 0` exception. |
| 3 | Minor | Summary, "Solver relevance" | "A solver which already imposes the disjoint system needs the family block only for triples whose objective cross coefficients have a positive product." Theorem 2.5 concerns a valid quadratic on the triple. In a model with more variables or constraints, the quadratic that matters on a triple is a dual aggregate of the objective and constraints, not the objective's cross coefficients. | Restrict the sentence to three-variable box QPs, or state it in terms of the aggregated (dual) quadratic. |
| 4 | Minor | Summary (a), "a point of `R` outside the hull must satisfy all three caps strictly" | "The hull" here must mean `H3+`. A point of `R` outside `K3` (the quadratic moment hull, the meaning of "hull" elsewhere in the Summary) can violate a cap, for example an atom plus diagonal slack. | Write "outside `H3+`". |
| 5 | Minor | Secs. 2.7-2.9, 7 (fit residuals `1e-28`, `4.8e-31`, `1e-16`, `3.1e-14`, `3e-7`-`4e-3`) | `fit_family.py` reports the `least_squares` cost `0.5 * ||v/|v| - p/|p| ||^2`, a squared distance. Read as distances, these are about `1e-14` (stratum examples) and `8e-4` to `0.09` (the 8 retest quadratics). The note never says the numbers are squared. | Define the residual, or report distances. My independent direct fit agrees: maximum relative coefficient error `<= 4.3e-8` on the 34 stratum examples and `<= 2.3e-6` on 42 SDP-derived rays (the size is due to the square roots in the fit). |
| 6 | Minor | Sec. 2.8 and Sec. 7 row "re-solve of the most negative stored `R` values" | The re-solved rays (`check_min_rR_dense.txt`) are stored examples with stored `R` values between `-1.4e-10` and `1.0e-11`. The ray that gave the reported dense-run minimum `-7.0e-9` was not stored and was not re-solved. The text implies values "of this size" were shown to change sign. | Say that the extreme ray itself was not re-solved. The conclusion that `-7e-9` is solver noise remains plausible for normalized data. |
| 7 | Minor | Sec. 2.9 table, row `project_probe.py` | In the `l1 0.03` run, every progress line in the log shows `sep(y0)` about `+1e-8` (the starting point is already in `H3+`). The perturbed objectives therefore mostly did not give "R_D-points outside the hull". Only the `l2 0.0` run matches the description (`sep(y0)` about `-1e-3`). | Correct the description of the `l1` run, or count only the `l2` run as evidence. |
| 8 | Minor | Sec. 2.8, "All other nonnegative kernels are convex or have a zero square coefficient" | The untested kernels also include those with a negative square coefficient (`stratum_enum.py` tests only `min_square > 1e-7` and `min_eig < -1e-9`). These are outside `P3+` and do not affect Conjecture 2.11, but the sentence is incomplete. | Add the negative-square case. |
| 9 | Minor | Sec. 2.7 vs Sec. 7 | Section 2.7 says 264 configurations reached residual `< 1e-6`. Section 7 says 265 were post-processed and 264 valid quadratics were retested. | Reconcile the counts, or explain the one that was dropped. |
| 10 | Cosmetic | Sec. 4.1 (S1) | Nishijima's Lemma 2.4 covers only intersections, preimages and dual cones. Linear images and Minkowski sums are shadows by definition, and exposed faces are intersections with a hyperplane. | Adjust the attribution. |
| 11 | Cosmetic | Cor. 2.6, "after complementing one coordinate or two coordinates" | Zero or one complementation suffices. Complementing two coordinates changes the signs exactly as complementing the third one does. | Write "after complementing at most one coordinate". |
| 12 | Cosmetic | Sec. 6, draft counts (24,944 rays, 337 outside) | These counts refer to the interrupted draft, which is not kept. I could not reproduce them from the surviving logs. | Optional: say that the draft is not preserved. |

## What was checked and how

### Proofs (by hand)

- **Duality remark.** The argument that `W` meets the interior of `K` is correct. The generators `x_i L(x_j,x_k)^2` and `(1-x_i) L(x_j,x_k)^2` force the cubic `2 x 2` moment matrix to be zero, and the degree-4 monomials follow. Closure of `R`: since `u` is in `int R_D` and in every `F_g`, segments from `u` show `cl R = cl R_D ∩ F`. Closedness of the sum uses Lemma 2.7, which comes later in the note but does not depend on the remark.
- **Lemma 2.1, Proposition 2.2.** Correct. The homogenization step removes the recession directions `D`. In the closedness argument, evaluation at the center bounds the cap multipliers.
- **Lemma 2.3.** Correct. `delta_i` is the coordinate functional of the pure monomial `x_i^2` in `V`, so `l + t delta_i` changes only `l(x_i^2)`. `l ∘ rho_i` changes only `x_i^2 -> l(x_i)`.
- **Corollary 2.4.** (i): every RLT inequality in BNW's Proposition 2 (Anstreicher-Burer Theorem 2) is `l` of a generator, except `X_ii <= x_i`, which is a cap. (ii): `(1-x_3) w L^2` is a generator with `3 in B`, and the recession case works as stated. (iii): the KKT expansion is correct. (iv) and the converses are correct. `H3+` is a subset of `R` because family members have nonnegative square coefficients.
- **Theorem 2.5.** The complementation case analysis is correct. BNW Theorem 1 (`sources/...2504.03996v3.txt`, lines 366-378 and 513) reads: for `n <= 3` the relaxation `min{Q • X + c^T x : X <= x e^T, [[1,x^T],[x,X]] psd}` is tight for every `(Q, c)` with nonpositive off-diagonal `Q`, for problem (1) `min x^T Q x + c^T x` over `[0,1]^n`. This is exactly the statement quoted in the note, including `Q_ij = q_ij/2`. The feasibility of `y'` for BNW's relaxation is correct (`Y_ij <= m_i` is `l(x_i(1-x_j)) >= 0`). I did not re-prove BNW Theorem 1. My independent numerical test of it is below.
- **Corollary 2.6, Lemma 2.7.** Correct, using that `P3+` is pointed. The six copies are `S = {z}` or `S = {x,y}` for each choice of the special coordinate (also checked by enumeration).
- **Lemmas 2.8, 2.9.** Correct.
- **Proposition 2.10.** The extremality argument is correct: values, interior-edge derivatives, and one-sided tangency at vertex zeros. See issue 1 for the boundary of the parameter range.
- **Sec. 2.10, rank-2 step.** Correct. Complementing coordinates flips the sign of `w_i`, and BNW Lemma 4 (line 1773) has the stated hypotheses: rank 2, `X >= x x^T`, feasible for (2).
- **Part (b).** I checked BKT's Lemma 2.3, Theorem 2.13, Example 3.4, Remark 3.2, Theorem 3.7, Proposition 3.11, Theorem 3.15 and Remarks 3.16-3.17 in `research-20260925/publication-sources/bodirsky-kummer-thom-jems-1509.txt` against their use in (S2)-(S4).
  - The lexicographic order on `Q^5` is allowed. Positive definiteness of `f(w) = T(eps^w)/T(1)` does not depend on the order, and Theorem 2.13 holds for any divisible ordered group. With this order, `xi_k = eps^{2e_1-2e_{k+1}}` is a positive infinitesimal.
  - Theorem 4.2: the evaluation identity, the transfer of copositivity of `H` to `H'`, and the positive square coefficients are correct.
  - Theorem 4.4: the perturbation argument near a simple ray is correct.
  - Theorem 4.6 and Proposition 4.7: the face and projection steps are correct.
  - Lemma 4.8: `L_f` is `R'`-linear, hence real-linear, which is all that (S2) needs.
  - Remark 4.9 is correct. The `G*` table matches Shaked-Monderer (Lemma 7.1 and Theorem 7.3 of the paper; the corrigendum proves that `T_5` is SPN).

### Re-runs of the stream's code

Exact checks were run in place. Numerical runs used a copy of `code/` in `/tmp` with new seeds, so the stream's `logs/` was not touched. All runs used `OMP_NUM_THREADS=1` and `timeout`.

| Command | Outcome |
| --- | --- |
| `check_rounding_map.py` | PASS (81 cases); `r1-logs/rerun_check_rounding_map.txt` |
| `check_boundary_rank_symbolic.py` | Same minors as the note (S1, and on `d1 = 2h`) |
| `check_family_strata_symbolic.py` | Same minors as the note; output identical to the stream's log |
| `check_apex_bookkeeping.py`, `check_boundary_members.py` | PASS |
| `sanity.py` | `R_D` `-0.0281`, `R` `-5.1e-10`, min over 48 compositions `-7.8e-10` (reproduced) |
| `signclass.py 5 300 sub` | 300 rays, min over `R_D` `-5.7e-9`, BNW `-6.9e-10`, 0 below `-1e-6` |
| `signclass.py 6 300 sup` | 300 rays, 0 outside `cl(D3)`, BNW below `-1e-6` on 90, min over `R` `6.5e-12` |
| `family_neighborhood.py 7 20 2 1`; `8 60 5 2` | 40 rays / 18 outside `cl(D3)` / 0 missing; 300 / 25 / 0 |
| `check_rounding_hull.py 9 60` | 30 of 60 points outside `H3+`; all satisfy the caps strictly (gap `>= 3.2e-3`); after rounding `>= -8.1e-9` |
| `stratum_enum.py 0 30 20 20 101 _r1` | 214 types; script ran without errors |
| `stratum_enum.py 0 1 30 60 202 _r1b` (all types, new seed) | 6,418 types, 221,909 kernels, 92,198 nonnegative, 506 tested, 58 outside `cl(D3)`, 0 missing (min over `R` `-9.1e-10`); the rays outside come from the same six types as in the note; no nonnegative kernel in the submodular class; 18 stored examples fit family members (`fit_stratum_examples.py`, max cost `1.4e-30`) |

Logs: `r1-logs/rerun_*.txt` and `r1-logs/stream_reruns/`.

### Independent reviewer code (does not import the stream's code)

`r1_common.py` contains my own `R_D` (27 localizing matrices on the 20-monomial functional), `R` (24 family LMIs, built from the family note's `b, B`), exact `P3+` separation (six order simplices, `COP_4 = PSD + NN`), and a cube minimum by face enumeration.

| Check | Outcome |
| --- | --- |
| `r1_exact.py` (sympy) | ALL PASS: Lemma 2.3 parts 1-3 with fully symbolic `L` (60 + 81 cases); family identity, cross coefficients, and the LMI identity `l(q) = h^2 + 2h b.v + v.Bv`; exactly 6 of the 24 copies can have all cross coefficients positive (`S = {z}` or `{x,y}`); Lemma 2.9 formula; S1-S5: family member in the kernel, generic rank 9, and exact rank 9 at 40 rational points per stratum (including `d1 = 2h` on S1, and `d1 = 0` and `d1 = d2 = 0` on S2 and S4); Theorem 4.2 evaluation identity with formal `f` |
| `r1_s3_d1zero.py` | S3 and S5 at `d1 = h = 0`: rank 9 (minor `-2k/d3`, `-2k/(d2+k)`); see issue 1 |
| `r1_sdp_checks.py bnw 4 300` | BNW Theorem 1, `n = 3`: 300 random submodular instances, max normalized gap (box min minus SDP (2)) `2.6e-9`; adversarial Nelder-Mead over submodular data (12 starts x 600 evaluations) `1.1e-8`. Controls: the same search without the sign condition finds a gap `0.25`, and flipping one cross coefficient gives gaps up to `0.12` |
| `r1_sdp_checks.py moments 3 150`, `moments 5 400` | 51 points of `R_D` outside `H3+` (exact `P3+` separation down to `-0.012`). On all of them: min over the four sign orthants with `q12 q13 q23 <= 0` `>= -1.6e-8` (Theorem 2.5, adversarial over `q`); caps strict (gap `>= 3.4e-4`); setting any `Y_ii = m_i` gives separation `>= -2e-10` (Cor. 2.4 (iv)). 550 minimizers of random and family-based objectives over `R`: smallest separation from `H3+` `-3.8e-8` (no point of `R` outside `H3+`) |
| `r1_sdp_checks.py moments 2 150` (earlier sampler version, perturbed family objectives over `R_D`) | No point of `R_D` outside `H3+` was produced (perturbed objectives are usually not valid, so their minimizers are hull points); superseded by the runs above. The same effect explains issue 7 |
| `r1_sdp_checks.py stored 1 60` | 76 stored rays outside `cl(D3)` (34 stratum examples, 9 from `signclass` sup, 33 from `explore_psd`): all valid (cube minimum `>= -1.2e-11`); my `R_D` values all `<= -4.9e-6`; my `R` values `>= -4.8e-9`; every ray fits a single family copy directly (see issue 5) |

### Labels, Summary, corrections, reproducibility

- The Summary agrees with the body apart from issues 3 and 4. The sampler totals add up: 36,398 rays, 1,371 outside `cl(D3)`, 10 samplers. The calibration rates (0.07%, 8%, 1.2%, 14%) match the table.
- I checked the Section 6 corrections against the logs where possible. The rerun numbers are correct (120/7, 60/0, 80/37). The position search covered 35 + 37 + 32 = 104 configurations for part 0 and 312 in total. The draft-level counts could not be checked (issue 12).
- The Section 7 table matches the logs I opened: `fit_all` (66 rays, `3.1e-14`, 57 five-contact + 9 S1); `check_nond3_blocked` (66/66); the `signclass` summaries; `stratum_enum` and dense summaries; `sos_subst` values; `check_rounding_*`. Exceptions: the `project_probe` description (issue 7) and the `check_min_rR_dense` scope (issue 6).
- No reviewer process was left running.
