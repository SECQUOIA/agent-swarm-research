# Critique of the camshape dossier (`camshape.md`)

Critic: independent reviewer (a Claude agent in the same project; not a human
review). Date 2026-10-04. `R/` = `research-20260929/`, `P/` = `R/publication/`.
My checks are in `camshape-critique-checks/` (scripts, logs, README, input
hashes). I wrote them from scratch on copies in `/tmp/camcrit`, on one core, and
imported nothing from `checks/camshape/`, from the verifier's code or from the
authors' code. Input sha256 prefixes are identical to those in the dossier's
`checks/camshape/input_sha256.txt`.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.** Theorem 1 is
correct. I checked every proof step, and all of its numbers reproduce
independently. One framing problem is major: the dossier presents the MINOTAUR
(QPLIB_3177) result as a refutation "upgraded to a proof". It also leaves the
summary's "prior global claim false" label in place. Our certificate refutes
only the exact attainability of MINOTAUR's primal value. That value is a
smaller tolerance-level discrepancy than ANTIGONE's QPLIB_2738 value, which the
same documents call a tolerance artifact. The other findings are stale
cross-references, notation, and wording.

## What I checked

| item | how | result |
|---|---|---|
| Theorem 1, Lemmas 1–3, proof of (a)–(d) | read line by line | correct (details below) |
| v_n to 30 digits; floor/ceil at 14 decimals | own regex OSIL parser and template match; exact rational S_j; R, B, E in fixed point with directed rounding (scale 1e-120); enclosure width about 3e-120 (`mine.py`) | identical to the dossier's 30 digits and to the Theorem 1(d) table for all four n |
| E exactly feasible | own exact Fraction envelope; generic evaluation of every OSIL row and bound, n = 100, 200 (`exactfeas.py`) | zero violations; 63/127 active convexity rows; \|E_2 − E_1\| = 3.098e-4, 7.818e-5 |
| MINLPLib .gms = OSIL | own GAMS tokenizer; every row and bound against the OSIL template (`minlp_gms.py`) | identical, all four n |
| QPLIB copy optima | own tokenizer; template match; optimum via Theorem 1 plus the Lemma 3 hypotheses C1–C5 (a different route from the dossier's row evaluation) (`qplib.py`) | floors at 16 decimals identical to I-5; shifts 8.539e-7, 9.823e-6, 3.777e-5, 8.699e-5 |
| QPLIB reference points | exact evaluation in each copy | −5.97e-14, +1.48e-12, −8.154e-6, −3.272e-5 against the copy optima; violations 2.0e-14, 2.2e-14, 3.0e-10 (e401 = G_1), 3.0e-10 (e801 = G_1). Matches. |
| robust enclosures, η = 1e-14 | recomputed with my enclosure code (`robust_mine.py`) | all four printed endpoints identical |
| MINLPLib p1/p2 | exact evaluation (`evalpts.py`) | deficits and violations match Section 4.3. p2 violates 360 (n = 400) and 722 (n = 800) rows by more than 1e-12, most by about 1e-10. |
| COPS constants | mpmath, 50 digits (non-interval) | largest distance 5.03e-15 (c₂, n = 400); matches `cops_consts.json` |
| listed values (Section 2) | `R/bound-audit/pages.json` | all values, solvers, dates and infeasibilities match |
| campaign values (Section 7.1) | `P/solver-runs/results_table.md`, `point_checks.log` | match (1.23e-7, 4.80e-7; 5.4%–21.7%; SCIP −5.20341) |
| literature values | control report, COPS 2.0 text, MINOTAUR log | match, except the wording points below |
| continuous limit | mpmath | A* = 4.2728604777…, n(−v_n − A*) = 1.129, 1.128, 1.131, 1.131 |
| tightness of D_n(ε) | explicit ε-feasible points: G_j = ε chain, cap 2 + ε, slope α + 2ε (`tol_attain.py`, numerical) | each point reaches 87% of D_n(ε) for all six (n, ε) pairs |

### Proof check

- **Lemma 1.** The induction is correct (cU₀ = U₁, cU_{j−1−k} − U_{j−2−k} =
  U_{j−k}), and the indices of U stay at most n − 1.
- **Analytic C1 test.** The test is valid: 333/106 < π, cos is decreasing on
  [0, π], and the Taylor upper bound for cos holds.
- **Lemma 2 and the proof of (a).** Both are correct. The proof of (a) uses
  only G_1…G_{n−1}, the upper bounds, positivity and the slopes for j ≥ 2.
- **Lemma 3.** All cases are correct:
  - (i): α ≥ 0 is needed but not listed. It follows from C4 and ū ≥ 1.
  - (iii)–(iv): correct, using E_n = 2 and E_{n−1} ≤ 2.
  - Case A: w ≥ S follows from E ≤ R.
  - Case B1/B2: the j = 2 edge correctly uses C4.
  - AM–HM: correct.
- **Uniqueness and greatest element.** Both are correct.
- **Implicit hypotheses** (not errors):
  - The H coefficient equals c; (b) needs only c_H ≤ 2.
  - C1 is not needed for (b).
  - The statement "Parts (a) and (b) hold for any constants that satisfy
    (C1)–(C5)" is true for model (P_n) as written.

## Major issue

### M1. The MINOTAUR/camshape800 result is framed as a refutation; it only shows that the value is not exactly attainable

**Where:**

- Section 7.1, camshape800 bullet.
- I-6: its title ("upgrades the camshape800 refutation"), its text and its
  resolution.
- Section 9: the "May claim" and "Must not claim" bullets on MINOTAUR.
- Issue `camshape-I6` ("can be upgraded from 'strong evidence' to a proof").
- The dossier also leaves the summary label at `R/open-instances-summary.md`
  line 175 unchanged: "Prior global claim false (rigorously for the MINLPLib
  model; ...)".
- It leaves the control literature report unchanged too: "a published global
  claim exists and is false"; "first correct global result".

**Problem:**

- **What is proved.** No exactly feasible point of the QPLIB_3177 .gms model
  (or of a binary64 transcription with the same structure) has a value at or
  below −4.27735.
- **MINOTAUR's dual side is consistent with our result.** Its claim implies a
  dual bound of about −4.2774. That bound is below the exact copy optimum
  −4.2741871514717434, so our certificate does not contradict it.
- **MINOTAUR's value is tolerance-reachable.** An explicit point that violates
  every row and bound of QPLIB_3177 by at most 9.7e-9 reaches −4.27735
  (`antigone_eps.log`, numerical). At 1e-8 it reaches −4.277445
  (`minotaur_eps.log`). At 1e-6 it reaches −4.527.
- **ANTIGONE needs more.** The same construction needs 2.9e-8 to reach
  ANTIGONE's −4.2843015 on QPLIB_2738.
- **Rigorous minimum violations.** By the D_n(ε) bounds in the solvers dossier,
  MINOTAUR's value needs violations above about 8.5e-9, and ANTIGONE's needs
  violations above about 2.6e-8.
- **Consequence.** MINOTAUR's discrepancy is the smaller tolerance-level
  discrepancy of the two. The project calls ANTIGONE's a "tolerance artifact"
  and counts camshape100 as "already solved globally in floating point".
- **The solvers dossier already says this.** Its §3.4 Consequences states that
  both values "are therefore consistent with 1e-6-tolerance points, and
  neither alone proves a bounding error".
- **Category error in the summary.** The summary's phrase "rigorously for the
  MINLPLib model" is a category error, because MINOTAUR never solved the
  MINLPLib model.

**Fix:**

1. State that the certificate shows only that MINOTAUR's value is not
   attainable under exact feasibility, and that MINOTAUR's implied dual bound
   is not contradicted.
2. Put MINOTAUR (QPLIB_3177) in the same class as ANTIGONE (QPLIB_2738) and
   BARON 26.5.27 (camshape100/200): reported optima below the exact optimum,
   reachable with violations of about 1e-8, 3e-8 and 1e-10.
3. Present the root closure (1 node, remaining-node bound +∞, while the same
   version cannot close the smaller copies in 3 h) as separate, circumstantial
   evidence of a possible bounding defect. It is not proved.
4. Relabel camshape800 in the summary and the literature report as a prior
   global claim on the rounded copy whose value is not exactly attainable, with
   a suspect closure. Use "first exact optimum" instead of "first correct
   global result".
5. With this framing, fetching `QPLIB_3177.nl` (I-6) is not needed for any
   paper claim (see C9).

## Corrections

**C1. Stale cross-references to the solvers dossier.**

- **Problem.** The dossier cites "Propositions 2, 3, 12". In the current
  `solvers.md` (03:52), Proposition 3 is the general exact lower bound,
  Proposition 4 covers BARON's camshape claims, Proposition 5 is D(ε), and
  Proposition 15 covers the QPLIB copies and the MINOTAUR/ANTIGONE claims.
- **Where.** Section 6 (verification row and status table), I-3, I-5, I-6,
  Section 10 item 3, and the evidence of issue `camshape-I3`.
- **Fix.** Replace 2 → 4, 3 (for D_n) → 5, and 12 → 15.

**C2. Notation clash for the omitted row.**

- **Problem.** Section 1.4 writes "|r_2 − r_1| ≤ αΔθ" and I-7 writes "αθ".
  Elsewhere α denotes the slope bound 1.5Δθ (Section 1.2 table). Taken
  literally, the stated row is 1.5Δθ² and wrong.
- **Fix.** Write |r_2 − r_1| ≤ α (= 1.5Δθ).

**C3. Novelty sentence in Section 9 ("May claim") lacks a qualifier.**

- **Problem.** The sentence says "first proofs of global optimality for
  camshape200, camshape400 and camshape800". The dossier's own I-8/I-9
  resolution says "(exact)". BARON 26.5.27 claims optimality on camshape200
  with a valid dual within 4.80e-7 relative in 23 s, and Octeract was listed
  for the rounded copy.
- **Fix.** Write "first exact (rigorous) proofs of global optimality" and
  credit the tolerance-level results.

**C4. Section 8, I-9 (stale-page sentence).**

- **Problem.** The text says the gaps are "stale ... for n = 200 ..., though
  not for n = 400/800". For n = 400, BARON's one-hour dual −4.62237809041 is
  much tighter than the best listed −4.97265746 (8.1% versus 16.3% relative to
  v_400), so the n = 400 listing is also stale, although the gap is still
  large. Only for n = 800 does BARON (−5.14464) fail to improve on the listing
  (GUROBI −5.12584).
- **Fix.** Reword accordingly.

**C5. D_n(ε) is an upper bound, and it is nearly attained.**

- **Where.** Sections 1.3, 4.3, I-3 and 9.
- **Problem 1.** The text calls D_n(ε) the "worst-case deficit" and the p2
  deficits "29% of what that tolerance permits". In fact D_n(ε) is a rigorous
  upper bound. My explicit ε-feasible points attain 87% of it in every case
  (numerical), for example:
  - 5.2825e-7 of 6.0447e-7 (n = 100, ε = 1e-10);
  - 2.4492e-5 of 2.8043e-5 (n = 400, ε = 3e-10);
  - 9.8231e-5 of 1.1255e-4 (n = 800, ε = 3e-10).
- **Problem 2.** "About 0.6 n²ε" holds for small ε only. For QPLIB_3177, the
  solvers dossier gives D(1e-6) = 0.2776, which is about 0.43 n²ε.
- **Fix.**
  - Say "rigorous upper bound D_n(ε) ≈ 0.6 n²ε for ε ≲ 1e-8; explicit
    ε-feasible points attain about 87% of it".
  - Give the p2 ratios as 29% of D_n and 33% of the attained value.
  - Say "row and bound violations", because D_n also relaxes bounds.

**C6. ANTIGONE margin uses the printed value as exact.**

- **Problem.** Sections 7.1 and 9 state "1.557e-4" and "1.56e-4" below the
  QPLIB_2738 optimum and "1.549e-4" below v_100. MINOTAUR is treated with the
  upper end of its printed interval, so ANTIGONE should be too. With
  −4.2843015, the margins are at least 1.552e-4 and at least 1.544e-4.
- **Fix.** Use these values, which match solvers dossier Proposition 15
  (≥ 1.552322e-4).

**C7. COPS LOQO agreement (Section 7.1).**

- **Problem.** The printed values 4.28414 and 4.27568 agree with
  −v_n = 4.2841471… and 4.2756885… only by truncation. Rounding gives 4.28415
  and 4.27569.
- **Fix.** Write "agree with −v_n truncated to five decimals".

**C8. Section 1.1, "two edge rows".**

- **Problem.** GAMS `camshape.gms` has three edge equations: convex_edge1,
  convex_edge3 and convex_edge4 (G_1, G_n and H).
- **Fix.** Write "three edge rows".

**C9. Cost estimate in I-6 and issue `camshape-I6`.**

- **Problem.** The dossier estimates "network fetch ... plus an exact parse and
  certificate run of about 2–5 min". This omits writing and validating a
  reader for AMPL .nl quadratic expression graphs, which may be in binary
  format. It is also unknown whether the file can be obtained: it sits under
  Mittelmann's `cnonconvex/` path and is not in any cache.
- **Fix.** After M1, drop this computation and keep the structural assumption
  stated.

**C10. Section 1.4, "Table B".**

- **Problem.** The camshape rows are in Table B2 of
  `P/minlplib-status/data/tables.md`.
- **Fix.** Cite Table B2.

**C11. Section 9, p2 sentence (optional sharpening).**

- **Problem.** "Violate the convexity rows by 3.0e-10" is imprecise.
- **Fix.** Write "maximum violation 3.0e-10 (row G_1); 360 (n = 400) and 722
  (n = 800) rows are violated by more than 1e-12, most by about 1e-10". This
  shows systematic use of the tolerance (`evalpts.log`).

## Minor additional issues

- **Theorem 1 hypotheses.** State exactly what each part uses:
  - (a) needs C1, c₀ > 0, ū > 0 and ℓ > 0;
  - (b) needs C2–C5 and c_H ≤ 2 (H coefficient = c in the files);
  - α ≥ 0 follows from C4 and C5.
- **Independent reproduction.** Several items the dossier marks "this dossier
  only" are now reproduced by separate code from a different author agent:
  - .gms = OSIL;
  - the QPLIB copy optima (by a different proof route);
  - the reference-point evaluations;
  - the η = 1e-14 enclosures.

  The status table can say "reproduced by an independent implementation". It
  is still not a human review, and `check_gms.py` was not read line by line.
- **QPLIB_2738 reference point.** It lies 6.0e-14 below the copy optimum, so it
  too is not exactly feasible (violations 2e-14). "Near-optimal" is fine, but
  say "tolerance-feasible at 2e-14".
- **Supporting evidence for D_n.** LANCELOT's COPS 2.0 values at violations of
  3–5e-6 exceed the exact optima by 0.018/0.077/0.174/0.583. At the same
  violation levels, my explicit ε-feasible points reach deficits of
  0.023/0.097/0.214/0.644. So the LANCELOT values are fully explained by
  tolerance. This is numerical evidence only, and it assumes that COPS
  measures violation on the same row scaling.

## Assessment of the dossier's own issues

- **I-1, I-2, I-4, I-8, I-10, I-11, I-12:** correct and sufficient.
- **I-3:** correct, with the C5 wording. The cross-reference should be
  Proposition 5 (C1).
- **I-5:** correct. My different-route recomputation confirms all four copy
  optima and both reference-point artifacts. The "under 1 h review" estimate is
  reasonable.
- **I-6:** the numbers are correct, but the framing is not (M1), and the cost
  estimate is optimistic (C9).
- **I-7:** correct. The mpmath dependence is stated correctly. A rational
  Taylor bound for cos and π would remove it cheaply.
- **I-9:** correct in substance, but the n = 400 wording needs fixing (C4).

## Commands run (targeted; no project-wide checks, no CI)

All were run in `/tmp/camcrit`, one core, each under 2 s:

- `python3 mine.py 100 200 400 800`
- `python3 exactfeas.py`
- `python3 minlp_gms.py`
- `python3 qplib.py`
- `python3 robust_mine.py`
- `python3 evalpts.py`
- `python3 tol_attain.py`
- `python3 minotaur_eps.py`
- `python3 antigone_eps.py`

Logs are in `camshape-critique-checks/`. These are my targeted checks; no CI
results are involved.
