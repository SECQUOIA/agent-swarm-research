# Confirmation review (round 1) of `theory-bangbang/window-exactness.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
report or the first review. I read the revised report in full, the first
review (`reviews/window-exactness-review.md`), the parts of [R]
(`theory-bangbang/report.md`: Theorem 2.3, Remark 2.5, Theorem 4.1) and [E]
(`theory-bangbang/extension-n2.md`: Section 3, Lemma 10, Section 6.2) that
the revised text cites, and the Osmolovskii–Veliov text that the reviser
downloaded (`/tmp/ov2020.txt`, Sections 4 and 5). I checked each of the ten
review items from scratch and recomputed every number that changed. Check
scripts and logs: `reviews/window-exactness-confirm-r1-checks/`.

## Verdict

**All ten items are resolved correctly. Every changed number reproduces with
independent code. The three refusals are justified. No theorem was
strengthened.** Two Summary sentences added in the revision state slightly
more than was checked or proved (issues 1 and 2 below). Both are one-line
wording fixes. There is also a pre-existing rounding slip in the
Section 7.6 table (issue 3). Issues 4–6 are optional.

## 1. Item-by-item check

| # | review item | what I checked | result |
|---|---|---|---|
| 1 | `l_0` closed form | Re-derived Theorem C(iii): summing `C_M h |d_t|^2/2` with `|d_t| <= h|b||omega| e^{C_g (t-n) h}` gives `C_M |b|^2 l e^{2 C_g l}`. `C_g = 0` needs `a` and `b` both state independent. Summary, (iii) and Section 7.3 now say so, with "`l_0 - o(1)`" and `Omega(1/h)`. Checked the new exact toy formula `(h^2 omega^2/2)[h(b-1-n) - k]` in rational arithmetic at `N = 1000, 4000, 8000` (`c5`): formula minus direct simulation is exactly 0 (the extra `h sigma_n omega` is `<= 2.7e-16`). `k/h` is an integer at all three `N`, so all three are exact ties. The text ("resolves this tie by rounding"; 251, 1000, 2000 against 251, 1001, 2000) is correct. | resolved |
| 2 | Proposition D scope and rate | Re-checked the proof: the sandwich `P^tr <= Phat <= Lyapunov` on `[s+K', N]`; `eta_{t-1} = eta_t - (eta_t + O(h))^2/m_t + O(h)`; `m_t <= C_3 (t - s)`; the harmonic-sum contradiction; the rate choice `delta = (log 1/h)^{-1/2}`, `theta^2 = 8 C_3 (C + C_1 + 1)/log(1/h)` (then `J/(K'+1) >= h^{-1/2}` and the log term `>= C + C_1 + 1`); the drop-the-pushes step to `b`; and the exact LQ window change. The `(b - s) h -> 0` extension is valid, with `limsup <= 0` only. The statement now requires exactness over `R^n x U` and a bounded exit offset. The `1/log(1/h)` rate is labelled heuristic. | resolved (one Summary sentence, issue 1) |
| 3 | Section 7.6 index | Own scalar and 2x2 recursions (`c1`). Toy `k = 0.5`: `b^T Phat_{s+1} b - b^T w` = 0.2936, 0.2421, 0.2222, 0.2046, 0.1790, 0.1816, 0.1516 (the table). The old formula gives 0.343, 0.290, 0.259, 0.234, 0.207. A−: 0.2016, 0.1854, 0.1544, 0.1414, — (break at `s+1`), 0.1247, 0.1148 (the new row). The old A− quantity gives 0.220 … 0.126. The break patterns (toy `k = 0.5`, `k = 0.1`, A−) match. The law comparison holds: 4–17% below the toy values, 10–21% above the A− values. | resolved |
| 4 | "exact in principle", `Theta(1/h)` | Summary, Theorem C(iii), Section 6 ("Long windows"), status table: `Omega(1/h)`, necessary only. No residual `Theta(1/h)` for this claim. | resolved; refusal justified (Section 2) |
| 5 | Section 7.5 attributions | Own `sigma(t)` by ODE integration, five-point `P'`, [E]'s `continuous_family` as input (`c2`, `c4`). `sup Delta|beta|^2/(2|sigma|)` = 2.446 (A), 4.169 (A−), 3.234 (A0', `eps = 0.02`), 17.36 (A0', `eps = 0.1`, attained before the switch; 2.74 on the last arc), against `inf lambda_min(M)` = 0.04 and 0.2. Anisotropic residual `<= 2.6e-8` on the last arc and `<= 4.4e-8` before the switch and in the layer, so "equality outside the layer" is correct. Scalar toys: 0.365 and 0.437 against 0.7. Labels now read "consistent with". | resolved (one Summary sentence, issue 2) |
| 6 | Entry-reduction radius | New Lemma 0.1(3): for `r/4 <= |d| < r/2`, Lemma 0.2 without the first-order term gives `>= -C h^2 - C h^2|d| + (h mu'/2)|d|^2 >= h[mu' r^2/32 - C h (1 + r)]`, using `|beta_t| = O(h)` from (P4) with `s_t <= C_W h`, `e_h <= C_e h`. The drift argument (`2 G h |W| -> 0`) is correct. Theorem B step 1 cites it with `s_t <= (C_1 + K + 1) h`. The Proposition 2.1 lower bound is now per stage on all of `D_t x U` (Lemma 0.2 on `B_t`, (P6) outside), so it needs no reduction. | resolved |
| 7 | 7.5 table `2e-5` | `logs/n2_azero.json`: `1.844e-5 h^3` at `eps = 0.1`, `N = 4000`, `K = 2`. Every other entry of the table and the Schur-certificate columns match the log. The cases listed as having indefinite `H_FF` (`K <= 2`, `eps = 0.1`; `K <= 16` and `K <= 8` at `eps = 0.02`) match the log, and they are exactly the cases with a positive single-direction deficit. | resolved |
| 8 | Rate wording | `c_*` is a specific small constant (Summary, Theorem A remark, Section 8, status table). Re-derived the two constraints on `c_*` in zones (i)–(ii). The zone (ii) constant uses `4 L C_sigma`, which is more conservative than needed and still correct. "Suffices" is used, and [R, Remark 2.5] is described correctly (O(h) gives O(1) failing stages; `h^{1/2}` gives `O(h^{-1/2})`). The vertex-margin bullet now assumes `e_h = o(sqrt h)`. I checked that this suffices: `|beta_t| = o(sqrt h)` near the switch makes the cross term `o(h)`, and farther out it is absorbed as in zone (ii). | resolved |
| 9 | Minor wording | "Inexact terminal term" (Summary, 7.2, Section 8), marked as a clarification of [R]. "Along any sequence of grids …, for all small `h`" (Consequence paragraph, Section 8). The Section 6 gap is `O(h^2)` in general and `Theta(h^2)` only with an interior or small-margin stage. optcdeg2 is marked outside (SH) in Summary item 3 and in the remark after Theorem B. `delta_sigma` is in (P5) and in `delta_2`. | resolved |
| 10 | Literature | Checked against the paper's text. Theorem 5.1 gives `C h` in `W^{1,1} x L^1 x W^{1,1}`. The norm is `||x||_{1,1} := |x(0)| + ||xdot||_1`, so `||x||_inf <= ||x||_{1,1}` holds as stated. The proof uses only the residuals of (5.1)–(5.3). The paper's setting matches the report's description: Lagrange cost with `p_N = 0`, (C1) Lipschitz in `t`, (C3) a-priori closeness. Corollary 4.2 needs (4.9) with `mu_0 < mu`. The O–M sign agrees with [E, Section 3]: `x_bar(tau+) = b Delta u xi`, `[H_x] = -w^T Delta u`, so `2[H_x] x_bar_av xi = -Delta^2 kappa_tau xi^2`, and with `eta_L = b^T Q b - kappa_tau` this reproduces [E]'s `Omega = (D + Delta^2 eta_L) xi^2`. The revision's check values reproduce from its log (`<= 5.2e-10`). The novelty statement is suitably qualified. | resolved |

Extra item (convexification bullet, Section 6). The gap identity
`J(zbar) - LB = J_zero(ubar) - min J_zero + (k/2) h^2 (1 - ubar_n^2)` is
correct. The Summary says the bound "is tighter than every window
certificate tested", but the revision compared it only on grids with an
interior stage. I added the other Section 7.3 grids (`c3`). At `N = 500` the
convexification gap is 0 (rounding level), a tie with the exact window. At
`N = 2000` it is `2.0e-5 h^2`, against window deficits of 0.018–0.0136
`h^2`. So the sentence holds on all tested grids (with a tie at `N = 500`).

## 2. Judgment of the refusals

1. **No `O(1/log(1/h))` upper bound for Proposition D.** Acceptable. The
   review asked only that the rate be labelled heuristic, and it is. The
   proved rate `O((log 1/h)^{-1/2})` is correct.
2. **"Whole remaining horizon with `Phi` at the exit is trivially exact"
   not adopted.** The reviser is right. Take a window `[a, N)` with `a > 0`
   and a free entry `x_a in D_a`. Then `beta_W = min_{D_a} (V_a - S_a)`,
   where `V_a` is the tail value function. This equals `J_W(zbar)` only if
   `xbar_a` minimizes `V_a - S_a` (and the tail of `zbar` is optimal). That
   is not automatic: a family whose curvature exceeds that of `V_a` in some
   direction makes `V_a - S_a` concave there. Only `[0, N)` with entry
   `x_0` is exact exactly when `f* = J(zbar)`. The revised wording claims
   no more than this.
3. **Reviewer's reproductions, the `eps = 0.02` Schur certificates and an
   anisotropic version of Theorems A–C were not redone.** Acceptable. The
   text cites the reviewer where it uses the reviewer's numbers, and it
   labels the anisotropic extension "plausible, not written out". My
   anisotropic-margin check (item 5) supports that label: with `M = 2 eps I
   + (Delta/(2|sigma|)) beta beta^T`, the anisotropic Schur term
   `Delta beta^T M^{-1} beta / 2` is strictly below `|sigma|`, so a margin
   exists.

## 3. Remaining problems

1. **Summary item 4 attaches the proved rate to the wrong case (residual of
   review item 2).** The Summary says the bound holds "when the window's
   exit lies `o(1/h)` stages after the switch (Proposition D). The proof
   shows that the exit curvature `b^T P_b b` exceeds `b^T w` by at most
   `O((log(1/h))^{-1/2})`." Proposition D proves this rate only for a
   bounded exit offset `b - s <= K`. For `(b - s) h -> 0` it proves only
   `limsup <= 0`: with `K'` growing, `log(J/(K'+1))` can grow arbitrarily
   slowly. The statement of Proposition D and the status table say this
   correctly; the Summary does not. *Fix:* "For an exit a bounded number of
   stages after the switch, the proof shows …".
2. **Summary item 2 generalizes an unchecked hypothesis claim.** It says
   [E]'s examples A and A0 have families that "lie outside (SH) (Section
   7.5)". Section 7.5 checked one family (`continuous_family`, `eps = 0.02`,
   `delta_1 = 0.1`, i.e. [E]'s *clin*) on example A, plus A− and A0', which
   are not [E]'s examples. [E]'s example A0 (`rho = 1, c = 0.2`) was not
   checked. Neither were [E]'s other tangential families on A and A0
   (*cmax*, *clin.02*; *rmax* is a discrete family, so (SH) does not apply
   to it). The claim is very likely true: maximal global-form solutions have
   equality in (G), and at `eps = 0` `lambda_min(M) = 0`. But it is not
   verified. *Fix:* "whose family checked in Section 7.5 (example A) lies
   outside (SH)", or run `revision_checks.py sh` on A0 and *cmax*.
3. **Section 7.6 table, toy `k = 0.1`, `N = 4000`: 0.214 should read
   0.213.** The report's own log (`logs/toy_rmax.json`) has 0.213455, and
   my code gives 0.213455. This slip predates the revision.

Optional (pre-existing wording; no result depends on these):

4. Summary, "What still works": the maximal recursion "is exact when
   `|kappa_tau|` is small compared with a quantity that decays slowly"
   reads as a proved sufficient condition. What is shown is a necessary
   condition (at an interior stage the recursion continues only if
   `kappa_tau + eta_hat_1 > 0`), plus float exactness on the tested grids.
   Suggest "is exact on all tested grids when …; continuing past an
   interior stage requires `|kappa_tau| < eta_hat_1`".
5. The Consequence paragraph and Section 8 say "`B = f*` fails". Theorem C
   proves `B <= J(zbar) - c h^2`, which contradicts `B = f*` only if
   `f* = J(zbar)`. Theorem C itself says "if `f* = J(zbar)`". Suggest "the
   certificate cannot prove optimality of `zbar` (`B <= J(zbar) - c h^2`)".
6. Section 7.3, "here `a = 0`, `b = 1`": in the toy, `a(t)` is also the
   target in the running cost (Section 7.1). Suggest "drift `a = 0`". Also,
   Theorem A is stated under (SH), which includes (T), while [V]'s family B
   violates (T). The stage part of Theorem A does not use (T), and for
   family B (`beta = 0`, `kappa_t = 1/2`) stage exactness is immediate. One
   clause saying this would make Summary item 2 airtight.

## 4. Was anything strengthened?

New material in the revision and its status:

- Lemma 0.1(3): proved; proof checked (item 6).
- Proposition D: the `(b - s) h -> 0` extension and the explicit rate are
  proved as stated. The Summary sentence in issue 1 is the only
  overstatement.
- Section 0.3 rate remark and the Section 10 entry on Osmolovskii–Veliov:
  match the paper's text. The report correctly says that the transfer to
  terminal costs and to the toys (which have a jump in `a(t)`) is not
  checked.
- O–M paragraph after Remark 1.4: correct. It weakens the novelty claim
  appropriately.
- Section 7.5 *Hypotheses* paragraph and Section 7.1 margin sentence:
  numbers reproduced.
- Section 6 convexification bullet: correct, and it holds on all tested
  grids.
- Section 7.3 exact fixed-duration formula: exact.
- Summary item 2's "whose families lie outside (SH)": not fully checked
  (issue 2).

No theorem, proposition or numerical claim was made stronger than its proof
or check, apart from issues 1 and 2.

## 5. Commands run and files

All from `reviews/window-exactness-confirm-r1-checks/` with
`OMP_NUM_THREADS=1`. These are targeted checks only: no project-wide
verification, CI not inspected, nothing committed.

1. `python3 c1_rmax.py` → `logs/c1_rmax.{log,json}` (own toy KKT search and
   own scalar and 2x2 maximal recursions; [E]'s `solve_kkt` imported
   read-only for A−; about 2 minutes).
2. `python3 c2_sh.py` → `logs/c2_sh.{log,json}` (own `sigma` by ODE; [E]'s
   `continuous_family` as the tested input; about 1 minute).
3. `python3 c3_convex_lb.py` → `logs/c3_convex_lb.{log,json}`
   (convexification gap on all Section 7.3 grids; seconds).
4. `python3 c4_aniso_pre.py` → `logs/c4_aniso_pre.{log,json}` (anisotropic
   margin before the switch and in the layer; about 1 minute).
5. `python3 c5_fixed_duration.py` → `logs/c5_fixed_duration.{log,json}`
   (exact rational check of the Section 7.3 formula; about 1 minute).
6. Read-only inspection of the report's logs `logs/n2_azero.json`,
   `logs/toy_rmax.json`, `logs/toy_plus.json`, `logs/revision_*.log`, and of
   `/tmp/ov2020.txt` (the reviser's text version of Osmolovskii–Veliov).
   No web searches.

## 6. Limits

- Proof checks are by hand, for logic and the order of constants; I did not
  re-derive every numeric constant (for example the 128 in `K_0`).
- The two-state checks are float screening, like the report's. I did not
  re-run face enumerations or the Schur certificates. I checked only the
  logged values and the changed entries.
- I did not check [E]'s example A0 or the *cmax* family against (SH)
  (issue 2).
- Literature: no new searches. I checked only the Osmolovskii–Veliov
  statements that the revision cites, against the paper's text.
