# Critique of the dossier `primal-points.md` (second pass, revised 2026-10-04)

Critic: independent reviewer, 2026-10-04. Paths are relative to `research-20260929/` (R/) unless they start
with `paper-open-minlplib/`. My own small checks are in
`paper-open-minlplib/development/dossiers/primal-points-critique-checks/` (scripts and `logs/`). They ran on
copies under /tmp (`/tmp/ppcrit`). They import no research script, and I edited nothing under R/ or
literature/.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.** The mathematics holds: Theorem C, Propositions
A, A.1 and L, Lemma 0 and the explanatory lemma are correct. The 13 exactly feasible points, the water, ANN
and KAN points, and the eg_* and ex6_2_* re-proofs hold up under every check I could make. The gaps and the
directions of the 13-instance displays agree with the summary.

The corrections fall into four groups:
- one unsafe primal display (catmix100) and wrong trailing digits (catmix200), both taken from float-printed
  log fields;
- several overstatements of what was checked (the data reading of the dual codes, infeasibility under
  binary64 data, the "display rounding only" list, the independence of the new eg scripts);
- a wrong statement about prior work: Kearfott (1998) *is* in the local knowledge base and is the direct
  antecedent of method C2;
- some scope gaps in the method statements (Proposition B does not cover hvycrash; the model definition has
  no domain rule).

## 1. What I checked

**Proofs re-derived.**
- **Theorem C (Krawczyk test).** All four steps hold, including the width argument in step 3. Fix any B in
  the interval matrix 𝐁 with |B_ij| = |𝐁_ij|. As x ranges over the box X, the set Σ_j B_ij (x_j − y_j) is an
  interval of width Σ_j |𝐁_ij| W_j, because the x_j vary independently. So step 3 holds whether K is the
  interval-arithmetic result or only a superset of the united range. The remark that K ⊆ int X_dec ⊆ X′
  places the zero in X_dec is also correct.
- **Proposition A.** The sign rule in Q(√D) is correct. The case p² = q²D cannot occur for q ≠ 0, because D
  is not a square.
- **Proposition A.1 (chain).** Correct: Σ w u = 4N, Σ w s = 8N, Σ w t = 12N and Σ w/t = 4N.
- **Proposition L (lnts).** Correct. The coefficients c_0 − q and c_a/2 are algebraic and the exponents
  0, ±ia are distinct, so Baker's form of Lindemann–Weierstrass applies.
- **lukvle10 linearization.** Correct: λ² − ((3+2√2)/2)λ + ½ has roots 2.731 and 0.183, and
  2.731^999 ≈ 10^436.
- **Lemma 0 and the explanatory lemma.** Both correct.

**Numbers checked against sources.**
- **OSIL hashes.** I recomputed all 13 SHA-256 prefixes in §1.1, and they match.
- **13-instance tables.** All gap and enclosure cells in §§2, 4 and 5.1 match the track reports, the r1
  reviews and the summary. This includes the powerflow enclosure widths 2.28e-42 and 2.82e-42.
- **Water duals.** The duals hard-coded in `gaps_check_v2.py` equal `certified_bound_exact` in
  `cert_TT_w1_impl.json`.
- **Objective constants.** I grepped `constant=` over all 43 OSIL files of the families. The only
  occurrences are objective constants: powerflow0039p/r (2) and catmix (−1).

**Re-runs and independent checks.**
- **`eg_dyadic_check.py`.** I read the whole script and found no error. The exp bracket is valid: odd and
  even partial sums of the alternating series are evaluated at the integer endpoints yh and yl, then squared
  outward. A re-run in /tmp on eg_int_s gave identical output in 17 s.
- **eg points, third implementation.** My own reader with mpmath iv at 120 digits (`eg_mpiv.py`) gives the
  same smallest margins: 5.57445e-20 (eg_int_s e12), 7.80026e-20 (eg_disc_s e12) and 7.49189e-20 (eg_disc2_s
  e10).
- **`eg_iv_check.py` (corrected).** `copy_negate` is exact, and `DN`/`UP` give directed rounding. It now
  rests on the correct rounding of libmpdec's `exp`, which is not in T1.
- **`ex62_check.py`.** Re-run: output identical. The atanh tail bound and the handling of ln, divide and
  product are correct.
- **lnts50 p1.** My own evaluation gives N·h = 0.55466876489565, which is 4.247e-11 below N·h₂. Confirmed.
- **New: chain p1 points.** I evaluated MINLPLib's chain p1 points at 80 digits (evidence only; files
  fetched 2026-10-04, hashes in `logs/chain_p1.log`). They lie 6.41e-12, 1.58e-11, 1.30e-11 and 1.37e-10
  above the certified duals.
- **optcdeg2 data reading.** `bangbang-verification/v_qcal_exact.py` (dual) and `v_primal.py` (primal)
  both use the decimal reading: Fr(4,10000), Fr(8,10⁵) and so on, with `iv.mpf(n)/d`.

## 2. Corrections

**C1. §5.3 table (line 607) and §3.6 catmix row: catmix100/200 primal values have float-artifact digits;
the catmix100 value is not an upper bound.**
- *Problem.* The values −0.0480694320309595635… and −0.0480591455801143916… are `float(J)` printed with
  20 digits. They come from the "exact J =" field of `publication/reproduction/cops/logs/v_catmix_model_all.log`,
  and also from `reviews/cops-verification/verification-report.md` lines 255, 364–365 and 387.
- *Evidence.* The same log line holds the exact enclosure ends:
  - catmix100: −0.048069432030959562924734533987703…;
  - catmix200: −0.048059145580114393563745030822862….

  The dossier's catmix100 value is **5.75e-19 below** the exact objective of the point, so it is not an upper
  bound. Its digits are wrong from the 18th significant digit on. The catmix200 value lies 1.96e-18 above
  the exact objective, but its digits are wrong after …11439. The catmix400 and catmix800 values are correct
  (`logs/catmix_digits.log`). The summary's gap cells are unaffected, because they use
  `exact_display_checks.json`.
- *Fix.* Use −0.04806943203095956292… and −0.04805914558011439356…, or the upward displays
  −0.0480694320309595629 and −0.0480591455801143935. In §3.6, cite the "J enclosure" field, not "exact J".
  Add the cops-verification lines to the PP-4 list.

**C2. §0, line 39 ("Every primal and dual proof reads each decimal string … as the exact rational"):
overclaim.**
- *Evidence.* §8.1 says that only the chain and dtoc5 dual codes were checked. I also confirmed optcdeg2 (see
  §1) and the wave-2-small verifier, which uses `osilx.py` and keeps decimals as strings (ex6_2_*, etamac,
  pricing050, hvycrash). The powerflow, camshape, catmix, waterno2, ANN, KAN, eg and pindyck dual codes have
  not been checked.
- *Why it matters.* Several gaps are at or below the 1e-16 relative level of a binary64 perturbation of the
  data:
  - optcdeg2 3e-18;
  - pricing050 2.3e-17;
  - ex6_2_5 3e-17;
  - pindyck 4.6e-17;
  - dtoc5 8.7e-17;
  - etamac 1.7e-16;
  - camshape and hvycrash 0.

  For these, a dual read under one convention and a primal read under another would not bound a single
  model's optimum.
- *Fix.* Say "every primal proof, and the dual codes checked so far (chain, dtoc5, optcdeg2, wave-2-small)".
  Make the confirmation by the dual dossiers a precondition, at least for the instances listed above.

**C3. §0, line 42, and PP-1: infeasibility under binary64 data is asserted beyond the evidence.**
- *Evidence.*
  - `binexact.log` covers only the 13 instances. My survey (`logs/binex.log`) confirms that waterno2, ANN,
    KAN, catmix and eg contain many non-binary64-exact constants, but no one evaluated their points under
    (c).
  - For eg, which has only inequality rows, PP-1 itself says that the rows "may still hold". With objvar
    margins near 6e-20 and data changes near 1e-15, the outcome is undetermined, not "not feasible".
  - The camshape exact optima and the hvycrash identity are also reading-(b)-specific. For example,
    50·fl(4.37e-3) − 0.2185 = −1.24e-17. Yet only lnts and lukvle10 are named as reading-independent.
- *Fix.* Write: "under (c) the equality-defined points (dtoc5, chain, powerflow) are not exactly feasible
  (checked or immediate); the others are not established to be feasible; the hvycrash and camshape exact
  values and all zero or 1e-16-level gaps are statements about (b)".

**C4. §7, line 649 ("Kearfott (1998, 2014) … not in the local knowledge base and were not read"): false
for Kearfott 1998.**
- *Evidence.* `literature/papers/kearfott1998-on-proving-existence-of-feasible/fulltext.md` exists (30.6 kB).
  It describes the following:
  - Hansen's technique of holding n − m coordinates fixed;
  - choosing them by Gaussian elimination with complete pivoting (its Method 1), or by near-tangency to the
    null space (Method 2);
  - verifying *small* boxes around approximate feasible points found by floating-point solvers;
  - handling points with many active bound constraints.

  This is exactly the C2 scheme: QR-chosen fixed variables, active constraints fixed, Krawczyk on the square
  system around p1.
- *Fix.* Read it and cite Hansen (1992, §12.3) and Kearfott (1998) directly as the antecedent of C2. Keep
  the Füllner et al. comparison. Say that C2 differs only in using exact rational fixing, active
  multi-variable inequalities as equalities, a 1e-45 box and an independent re-proof. Kearfott 2014 and
  Domes–Neumaier 2015 are indeed absent.

**C5. §8.2 "listed displays" row (line 728) and PP-5 caution (line 805): lnts50 is wrongly listed as
"below the dual only through display rounding"; the chain cases were not evaluated.**
- *Evidence.* The dossier's own `lnts_p1_check.log` shows that lnts50 p1 itself lies 4.25e-11 below N·h₂.
  The chain p1 objectives were not evaluated in the dossier. My evaluation (`logs/chain_p1.log`) shows that
  they lie above the duals, so for chain the rounding explanation holds (as evidence).
- *Fix.* List six displays (lnts100, lnts400, lukvle10, chain50/100/200) as rounding-only, citing
  lnts_p1_check, the lukvle10 p5 evaluation and chain_p1. State that the lnts50 display lies below for both
  reasons.

**C6. §3.3 Proposition B (line 312), its "Uses" (line 331) and §8.1 (line 698): hvycrash is not covered.**
- *Problem.* Proposition B needs each defining row to be affine in the new variable. The hvycrash row alg_k,
  −1/r − cos θ/(D r³) = 0, is not affine in r_k. Its solution r_k = √(−cos θ_k/D_k) needs a separate
  argument: on the region where −cos θ_k/D_k > 0 and r_k ≠ 0, which the intervals establish, the row holds
  identically.
- *Fix.* Generalize Proposition B to "x_k := φ_k(x_<k), with r_k(x_<k, φ_k(x_<k)) = 0 an identity on a
  domain that the enclosures prove is entered". Alternatively, treat hvycrash as its own case.

**C7. §3.7 chain (line 521): "Hence 2–3 free indices give no rational parametrization" is unproved, and it
contradicts the dossier's own advice.**
- *Problem.* For three free indices, "no rational parametrization" is exactly the genus-1 claim. A plane
  cubic is rationally parametrizable when it is singular. Neither smoothness nor genus has been shown, and
  genus says nothing about whether rational points exist.
- *Fix.* Delete the sentence. Keep only the proved part: in any rational point all s_i, and hence all t_i,
  are rational.

**C8. §0, line 15: "Five independent r1 reviews verified them [the 13]".**
- *Problem.* Four reviews cover the 13: lnts, dtoc5-lukvle10, chain and powerflow. The fifth,
  water-ann-kan, covers the water, ANN and KAN points.
- *Fix.* Reword accordingly.

**C9. PP-3, line 773: evidence misattributed.**
- *Evidence.* The summary (lines 103 and 155) and READINESS (lines 44 and 45) say that the mpmath-iv
  assumption applies only to the **ANN and KAN** points. READINESS lines 31 and 40 already credit the
  reviewers' own intervals for lnts and powerflow. The mpmath assumption for lnts, powerflow and lukvle10
  appears in the *track reports'* "Proved" sections.
- *Fix.* Correct where the understatement occurs.

**C10. §0 line 36, §3.6 line 465 and §9: the five claims are not "single implementation" in every case.**
- *Evidence.* For hvycrash, the authors (`hvycrash.py`, mpmath iv at 50 digits) and the verifier each proved
  a different point. For pindyck, both the authors and the reviewer enclosed the s_t with intervals. All of
  these use mpmath iv. etamac, pricing050 and optcdeg2 are verifier-only.
- *Fix.* "rest on mpmath iv (no mpmath-free re-proof); etamac, pricing050 and optcdeg2 rest on a single
  implementation".

**C11. §9 first "May claim" bullet (line 848): "an upward rounding of a rigorous enclosure".**
- *Problem.* pricing050 is a maximization problem, and its display is rounded downward.
- *Fix.* "rounded in the conservative direction (upward; downward for pricing050)". The artifact definition
  ("below a certified lower bound") similarly needs "above a certified upper bound" for pricing050. The
  hvycrash p1 and p2 values lie *above* the constant −0.2185, so they are "impossible values", not deficits.

**C12. §3.5 (eg): "the decision variables are the exact decimals of the binary64 search point".**
- *Evidence.* The `.retry.sol` strings, such as 0.564219345763436, are `repr` (shortest round-trip) strings.
  They are not the exact binary64 values. `verify_primal.py` computed objvar at these strings, read as
  decimals, and `eg_dyadic_check.py` proves feasibility of that decimal point.
- *Fix.* "the shortest-repr decimal strings of the binary64 search point, read as exact decimals".

**C13. §1.1 definition (lines 65–75): no domain rule.**
- *Problem.* The definition must require every expression to be defined at the point: denominators nonzero,
  ln and power bases positive, sqrt arguments nonnegative. Otherwise "x ∈ F" is ambiguous for hvycrash
  (division by r and r³), ex6_2_* (ln, divide) and lukvle10 (power). The hvycrash identity explicitly uses
  r ≠ 0.
- *Fix.* Add one bullet stating this rule.

**C14. PP-2 resolution and cost (line 769), and §9 third bullet (line 854): the new dossier proofs are not
yet independently reviewed.**
- *Problem 1: shared author and design.* `eg_dyadic_check.py` and `eg_iv_check.py` were written by the same
  agent and share the same reader logic, so they are two arithmetic back-ends rather than independent
  implementations in the sense of T2. The same holds for `ex62_check.py` and the catmix400 exact rerun.
- *Problem 2: unlogged test.* The "304 arguments against a 120-digit reference" exp test has no saved log or
  script. The script's own self-test checks only five identities.
- *Partial review here.* My code reading, the re-run and the mpmath-iv cross-check together amount to a
  first independent check of the eg points. It is not a review of the package.
- *Fix.* Treat "cite in the reproduction package" as "add, save the exp test and log, and have them
  reviewed". The cost is about 1–2 hours of review, not 1 minute.
- *Wording.* In line 854, "interval-based existence proof" does not fit waterno2, dtoc5 or chain, whose
  proofs are exact algebraic, and lukvle10 is a forward rational definition.

**C15. §9 explanatory lemma (line 901 ff.) and PP-10: two inaccuracies.**
- *hvycrash pairing.* hvycrash is paired with the lemma, but its p1 and p2 values deviate *upward* (−0.21413
  > −0.2185). A lower-bound lemma cannot explain them. Move hvycrash out of that sentence.
- *Summary sentence missed.* PP-10 flags only the open-instances report. The authoritative summary itself
  (lines 312–314) says the camshape p2 deficits arise "because the chain amplifies violations up to about
  600-fold". 600 × 3e-10 = 1.8e-7, which is far below the observed 8e-6 and 3e-5. That sentence must also
  be corrected or made qualitative.

**C16. §0 and §2: credit for the lnts50 p1 evaluation.**
- *Evidence.* The value 0.55466876489565 and the violation 9.1e-10 are already recorded in
  `reviews/open-instances-verification/verification-report.md` line 122.
- *Fix.* The new element is only the comparison with N·h₂. Say so.

**C17. Minor numerics.**
- *Parenthetical relative gaps (§5.1).* The values are rounded inconsistently: 0039r is given as
  "(6.699e-10)", which rounds 6.69912e-10 down, while the dossier's own log prints 6.700e-10. 0039p is given
  as "(6.323e-10)", which rounds up. The displayed upper bounds are unaffected.
- *Swapped-root objective.* "Objective 6.326" for the swapped chain root was measured for chain50 only.
- *T4.* T4 omits the geometric tail bound for atanh, which ex62_check and the lukvle10 crosschecks use.

**C18. T3 ("each family has at least two readers").**
- *Problem.* For the etamac and pricing050 exact points, the only reader is `osilx.py` together with the
  verifier's template matching. The authors' readers evaluated different, inexact points.
- *Fix.* State this as part of the single-implementation caveat.

## 3. Additional issues (not raised by the dossier)

- **A1 (minor): float-printed catmix digits elsewhere.** The cops-verification report propagates the same
  float-printed catmix digits. `publication/solver-runs/references.json` labels the catmix100 reference
  primal −0.048069432030979596 as an "exact feasible upper enclosure", while `exact_display_checks.json`
  calls the same value a reviewer Newton point (evidence). It is still a valid upper bound on v*, because the
  exact author point is lower. Add both to the PP-4 owner list.
- **A2 (minor; supports PP-1): precedent for reading (b).** Exact MIP solvers store the input data as
  rationals and treat the floating-point data as an approximation:
  - Cook et al. 2011: "storing the input data as rational numbers";
  - Eifler et al. 2023: "rational input data … floating-point approximation";
  - Hoen–Gleixner 2025: "rational input data".

  These are local knowledge-base files. Citing them makes reading (b) a recognized convention rather than
  an ad-hoc choice.
- **A3 (minor): artifact list incomplete or uneven.** The §9 table takes three campaign points but omits
  others from the same `solver-runs/report.md` table (lines 297–307): BARON camshape400 (8.15e-6 below),
  BARON and GUROBI camshape800 (0.094 and 0.023 below, violations 3.3e-7 and 9.7e-7), GUROBI chain50
  (2.0e-7 below) and the pricing050 points. Either cite that table or state the selection rule.

## 4. The dossier's issue list and cost estimates

- **PP-1.** Severity "major, not invalidating" is right. The resolution is sufficient only together with C2
  and C3, because the dual-side reading is unconfirmed for most families. The cost estimates are plausible
  for the primal side (dtoc5 and chain in seconds; powerflow about an hour). They omit the primal side of
  water, ANN, KAN, catmix and eg under (c), and they omit any dual-side work, which a (c) claim would need.
- **PP-2.** The defect and its fix are correctly described, and the eg points hold: there are three
  implementations now, counting mine. The 1-minute cost is too low (see C14).
- **PP-3.** The substance is correct. The evidence needs correction (C9 and C10). The cost estimates are
  plausible. "Save the pricing050 vector, under 1 minute" needs a small script change first, because
  `v_pricing050.py` does not write coordinates.
- **PP-4.** Line references verified. Add the items in A1 and the summary line in C15.
- **PP-5.** The lnts50 addition is correct and verified. The caution needs correction (C5).
- **PP-6, PP-7, PP-8, PP-11.** Correct.
- **PP-9.** Correct, but the dossier itself repeats the unproved claim (C7).
- **PP-10.** Correct, but it misses the summary's "600-fold" sentence (C15).

## 5. Bottom line for the paper

The core primal claim stands:
- all 31 closed instances have exactly feasible points under reading (b);
- the 13 formerly tolerance-only closures, waterno2, ANN and KAN rest on T1–T4 with independent
  mpmath-free re-proofs;
- five claims rest on mpmath iv.

Before the dossier is used, it should be corrected for C1 (an unsafe display), C2 and C3 (the reading
claims), C4 (prior work) and C5 (the artifact caution), and the remaining items should be tidied.
