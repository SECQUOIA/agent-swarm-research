# Critique of dossier `chain-catmix.md` (chain50–400, catmix100–800)

Written 2026-10-04 by an independent critic. Nothing under `R/` (`research-20260929/`) or
`literature/` was edited, and no script was run in the main tree. All checks ran on copies in
`/tmp/critic-chaincatmix/`, one core each. Line numbers refer to the dossier file.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.** I tried to refute every bound,
point, gap and proof and could not. All corrections below are minor: wording, bookkeeping, one
over-stated consequence, one cost slip and one weak proposed resolution.

What I verified independently, with my own code (not the dossier's):

- **catmix primal values (exact).** My own OSiL reader (xml.etree, mult/incr expansion, decimals
  as Fractions) and a generic row solver read each pair of rows as a 2×2 linear system in the
  states. It assumes no P/Q structure. It checks every row exactly and asserts that all states
  are nonnegative and 0 ≤ u ≤ 1. I evaluated seven saved control vectors exactly:
  - `catmix100_u`, `catmix100_u_newton`, `catmix200_u`, `catmix400_u`,
    `catmix400_final_policy_u`, `catmix800_final_policy_u`, `catmix800_u_snap` and
    `catmix800_u`;
  - all floor/ceil values at 1e-30 equal the dossier's (Section 4.2) digit for digit;
  - the shifts J_{9a} − J_{c_N} are 1.1815e-17, 1.4195e-17, 9.466e-18 and 1.893e-17, as
    stated;
  - the variable bounds and objective (constant −1, coefficients on x1_N and x2_N) are as
    stated.
- **chain primal values (numerical, 90 digits).** I rebuilt each point from
  `points/chainN_generator.json` (t_i decimals, then the two quadratic roots). I evaluated it
  through the OSIL expression trees with my own OSnL evaluator: x_N = 3 and length = 4 to
  1e-90, the linear rows to 2.5e-91, and every objective lies inside the 40-decimal enclosure
  quoted in Section 4.1. This is not an exactness proof; the primal track and its r1 review
  provide that.
- **Gaps and displays (exact).** From the logged duals and the exact primal values I recomputed
  every Section 5 cell. They are correct:
  - every safe dual display is ≤ its double, and every primal display is ≥ its exact value;
  - absolute gaps: 9.6165e-15, 1.0058e-14, 9.4002e-15, 1.0014e-14, 1.84999e-13, 1.89584e-11,
    6.80597e-11 and 1.48445e-10;
  - relative gaps as stated.

  The Section 2 comparisons with the listed values (2.1e-10, 1.5e-10, 3.4e-10; 4.08e-8,
  2.27e-8, 2.97e-8, 6.19e-8; and the truncation reading) are also correct. The CC-2 and
  remark-3 differences against the authors' bounds are correct too.
- **Proofs.** I re-derived Lemmas C1, C2 and C3, Theorem C4 and Lemma C5 line by line, together
  with the new Proposition C6, Lemma M1, Lemma M6 and Proposition M8. Lemmas M2–M4 and
  Theorem M5 are also correct. The only defect is the "Consequently" clause of C6
  (Correction 1). Supporting checks:
  - **C6 at 50 digits.** For N = 3, 7, 50 and random end values with a strict chord, the
    constructed discrete catenary has length 4 to 1e-50 and f − B_N(V*, H*) = O(1e-50).
    I perturbed it 30 times per case, restoring the length exactly. Every perturbed chain had
    higher energy (by 4e-10 to 2e-12). For N = 3 the length fixes z_2, so the test is vacuous
    there.
  - **M1, M6 and M8, exact.** For 200 random rational u per N, under both c_N and 9a:
    det P ≥ 1 + a; P⁻¹ ≥ 0 and M ≥ 0; the column sums of M are ≤ 1 (the maximum is exactly 1,
    at u = 0); and M_{9a} ≥ M_{c_N} and P_{9a}⁻¹ ≥ P_{c_N}⁻¹ hold entrywise.
- **Codes.** I read for rigor:
  - `v_catmix_dp.py`: `peval_lo`, `qmin_lb` (the vertex test is padded by 1e-12),
    `dinkelbach`, the crude bound, cone verification, coverage of [0, 1], `fr_iv` and the final
    `dn`. I also checked that a NaN cannot pass silently, because `lbr` must be finite and
    `w ≥ 0` is asserted.
  - The recheck copies are byte-identical to the verifier's `v_catmix_dp.py` and
    `v_catmix_model.py`. The recheck driver asserts that every ray is dyadic with at most 30
    fractional bits.
  - The chain codes: both B&Bs, their root boxes, gradients, pruning tests and certified values.
    I found no validity problem.
- **MINLPLib listing rule.** In `R/bound-audit/pages.json`, on all 1,576 pages with at least
  three finite page duals, the `instances.html` dual equals the third-best page dual. Pages
  with fewer than three duals have no listed dual (Correction 6).

## Corrections (location, problem, evidence, fix)

1. **Line 269 (Proposition C6, "Consequently f*_N = inf over Ω_N of max_{V,H} B_N"): over-stated.**
   - *Problem.* C6 proves the exact reduction only on the strict-chord part of Ω_N. On the
     boundary (L equal to the chord), C6 does not apply, and "max" need not be attained.
   - *Evidence.* Hypothesis of C6: "satisfies the chord condition strictly".
   - *Fix.* State f*_N = inf over {(z_1, z_N): L > chord} of max_{V,H} B_N. Add one line:
     at a boundary point the slice minimum is the straight interior chain, and strict-chord
     points arbitrarily close have slice minima arbitrarily close to it, so the infimum is
     unchanged. Line 762 ("the discrete catenary is the unique global minimizer … for fixed end
     values") needs the same qualifier: "for end values with L above the chord". No bound is
     affected; the B&B uses only Theorem C4 and Lemma C5.
2. **Lines 334–339 (Remark): the scouting formula is not "the opposite sign convention".**
   - *Problem.* `R/theory-calibration/scouting.md` §2.4 item 5 writes
     S_k(z, v) = G(v) − v z + k c. The negative of the dossier's Φ_k is G − v z − k c.
   - *Evidence.* With +k c, S_k − S_{k+1} = Φ_{k+1} − Φ_k − 2c. The stage inequality then still
     holds but loses 2c per stage, so it is not exact on catenaries.
   - *Fix.* Say that the scouting note has a sign slip in its k c term (it should be −k c). Do
     not cite it as equivalent.
3. **Lines 457–461 and CC-7(b) (line 730): the verifier's evidence is not addressed, and the
   location is identifiable.**
   - *Problem.* The verifier inferred a grid-independent loss because the authors'
     "1e-5 + band" run and their "uniform 3e-6" run give bit-identical bounds
     (`logs/catmix100_bound_3e-06_200_1e-07.json` and `…band0.0685_0.0725_1e-06.json`: both
     −0.048069432038882705). The dossier does not mention this, and its "the band spacing
     there is 1e-6 throughout" does not apply near the trajectory.
   - *Evidence.* `make_grids` in `catmix_bound.py` drops all base and band rays inside the
     transported window's span ("the window replaces base rays in its span"). I rebuilt both
     grids on a /tmp copy:
     - in both runs, the 401–402 rays around θ* are the same window rays at every stage;
     - on the singular arc their spacing grows backward from 1.34e-7 (stage 70) through
       2.5e-7 (stage 50) to 6.49e-7 (stage 20);
     - the verifier's windows are 6.0e-8 (config A) and 3.0e-8 (config B).

     So the binding rays are identical in the two runs, which explains the identical bounds. The
     loss is interpolation in the stretched window, as Lemma M6 implies. The recheck's fit
     n_arc·C·d² with C ≈ 1.5 and the stage-sampled mean d² ≈ 1.4e-13 on stages 20–70 gives
     about 1e-11, the right order for 7.9e-12.
   - *Fix.* Replace "did not identify which part … band spacing 1e-6 throughout" with this
     explanation, and cite it in CC-7(b).
4. **Line 740 (CC-12): wrong cost arithmetic and an under-stated size.**
   - *Cost.* 46 + 20 + 45 + 46 min = 157 min ≈ 2.6 h, not 3.3 h.
   - *Size.* 2,647 rays × 800 stages × 8 bytes = 16.9 MB is the size of w alone. Saving
     (grid, w) as float64 needs about 34 MB; storing only w is enough, because the grids are
     reproducible from the command.
   - *Fix.* "about 2.6 h; about 17 MB for w (grids reproducible)".
5. **Line 723 (CC-2): the optional resolution would not certify the stated doubles, and the
   wording should state the cross-check's scope.**
   - *Problem 1.* `catmix_bound.py` stops when LB ≥ incumbent − 1e-14. On identical inputs it
     ran below the verifier's routine by up to 9.44e-15 per ray (mean 5e-16 to 1.3e-15 per
     stage; `logs/x{coarse,fine}100.log`). By Lemma M6, such deficits can add up over the N + 1
     stages: up to about 1e-12 in the worst case, plausibly about 1e-13 for catmix100. That is
     comparable to the catmix100 gap of 1.85e-13. So rerunning the authors' code on the
     recheck grids would give slightly weaker numbers, not the stated doubles.
   - *Problem 2.* The cross-check covered N = 100 on two test grids only.
   - *Fix to the wording.* "… agrees with it per stage within 1e-14 on identical test inputs
     (N = 100: all 99 stages on a 324-ray grid and 40 stages on a 2^-21-band grid) …".
   - *Fix to the resolution.* For a genuine two-code certification of the stated values, see
     Additional issue A2.
6. **Lines 108–113, 759 and the Section 0 cell "best page dual": state what MINLPLib's listed
   dual is.**
   - *Problem.* "Best listed dual 0.08–0.17 for chain" quotes ANTIGONE's single-solver page
     values. MINLPLib's own listed dual (`instances.html`, and `=bestdual=` in `minlplib.solu`)
     is −37.10, −77.46, −145.89 and −286.81.
   - *Evidence.* On every page with three or more duals (1,576 pages), the listed dual equals
     the third-best page dual, and the page bolds the top three. Pages with fewer than three
     duals have no listed dual; catmix has a single LINDO dual, hence "none". This is observed
     data, not a documented rule.
   - *Fix.* Write "the best dual bound reported on the MINLPLib instance pages (ANTIGONE)
     is 0.08–0.17; MINLPLib's listed dual bound, the third-best reported value, is −37.1 to
     −286.8; catmix has one reported bound and no listed dual".
7. **Line 133 ("MINLPLib's 1e-6 rule … |p−d|/min(|p|,|d|)"): the formula is unsourced.**
   - *Problem.* The formula comes from the COPS note. The MINLPLib documentation snapshot
     defines the solved mark as "at least 3 solvers claim global optimality (up to a relative
     optimal tolerance (gap) of 10^-6)" and gives no formula.
   - *Evidence.* The conclusions do not depend on the normalization: catmix800 is 1.294e-6
     with either min or max, and catmix100 is 8.515e-7.
   - *Fix.* Drop the formula or say "under either normalization". Phrase it as a comparison of
     gap size, not as what would earn a solved mark.
8. **Line 652: "their duals from 2014–2020" is wrong for chain.**
   - *Evidence.* The chain pages carry GUROBI duals dated 31 Jul 2025 and 07 Aug 2025, and
     SCIP duals dated 15 Feb and 17 Mar 2022 (`R/bound-audit/pages.json`). The control report
     says "2014–2025".
   - *Fix.* "duals from 2014–2025 (chain) and 2015–2020 (catmix)".
9. **Line 657 (Müller et al.): wrong source for the chain statement.**
   - *Problem.* The slug `muller2022-on-generalized-surrogate-duality-in` is the journal
     version, and its library full text has no per-instance tables.
   - *Evidence.* The chain data are in arXiv:1912.00356v1, Table 5
     (`R/publication/literature/control/sources/papers_rev1/mueller2019_arXiv1912.00356.pdf`).
     The table gives root gap-closed fractions against MILP relaxation values: chain50 0.34
     against −115.129, chain100 0.00 against −145.215, chain400 0.00 against −343.145. chain200
     is absent. The implied bounds are negative.
   - *Fix.* Cite the arXiv table, describe it this way, and do not mention chain200.
10. **Line 55 ("GAMS = OSIL … identical coefficients") overstates the cited evidence for chain.**
    - *Problem.* `exact_forms.py` (exact) covered catmix, methanol50 and lop97icx. For chain,
      `minlplib-status` has only `history.py` evidence: two rows differ structurally, and the
      rows are equal at 60-digit sample points.
    - *Evidence.* The exact identity does hold. `chain.gms` uses 0.5·h with h = 1/N, L = 4,
      a = 1 and b = 3. The OSIL constants are exactly 1, η ∈ {1e-2, 5e-3, 2.5e-3, 1.25e-3} and
      4, with η = 1/(2N).
    - *Fix.* Cite this inspection, not the status report.
11. **Line 520 (final designs, N = 400/800): incomplete for reproduction.**
    - *Missing.* Base 2^-13; the band stage ranges 40–310 and 95–600; the window-skip ranges
      56–288 and 112–576; and, for N = 800, an extra 2^-17 band on [0.060, 0.0695] at stages
      570–650.
    - *Evidence.* `R/reviews/catmix-recheck-checks/logs/catmix{400,800}_final.log`;
      `catmix-recheck.md`, lines 298–299.
    - *Fix.* Add these, or cite the exact commands.
12. **Line 453 ("Its logged per-stage loss is ≤ 9.99e-15"): the initial stage is not logged.**
    - *Evidence.* In `catmix_bound.run`, `worst_loss` is not updated after the initial
      `stage_lb` call.
    - *Fix.* "logged for N of the N + 1 minimizations; the initial one uses the same
      tolerance". The conclusion is unchanged.
13. **Line 315 ("L_N is the binary64 target (60-digit KKT value − 1e-14)"): imprecise source of
    the target.**
    - *Evidence.* The authors' target is float(25-digit KKT string) − 1e-14. The verifier's is
      float(50-digit evaluation of the double-rounded primal vector) − 1e-14. Both give the same
      four doubles.
    - *Fix.* State both.

## Additional issues

- **A1 (minor): the four new proofs have now had an independent read.**
  - I read C6, the M1 proof, M6 and M8 line by line and checked each numerically or exactly.
    All are correct, apart from Correction 1.
  - M8 was also checked against the GAMS text (`catmix.gms`): ode2 expands to the coefficient
    −9 on u·x2, so c = 9a exactly. Only the c-terms differ from the OSIL file.
  - CC-1 and CC-11 can be closed after Correction 1, unless the paper wants a second read.
- **A2 (minor; optional new computation): genuine two-implementation certification of the
  stated catmix doubles.**
  - Save w per stage from the record runs (CC-12).
  - Then check each stage target-first: prove min_u W^{(i)}(M(u) r_j) ≥ w^{(i−1)}_j with the
    authors' interval machinery, branching until each target is proved. The current
    incumbent-and-tolerance loop is not suitable.
  - This would certify exactly the stated values with the second code.
  - *Cost.* About 2.6 h of reruns with saving, about 1–2 h of coding, and a checking run of
    roughly the authors' original 21–70 min per instance (single thread). That run time is an
    estimate; it may be longer where the verifier's slack is only about 1e-16.
- **A3 (minor): two older primal displays are not valid upper bounds.**
  - `R/reviews/catmix-recheck.md` (summary table) prints −0.048056547756611555 (catmix400) and
    −0.048055901330847467 (catmix800 `_snap`). These are rounded to nearest and lie 1.45e-19
    and 1.14e-19 below the exact objectives.
  - The "exact J = …" strings in `policy_exact_{400,800}.log` are binary64 renderings, 3.3e-18
    and 2.5e-18 above the exact values. That is harmless for an upper bound, but they are not
    exact.
  - The dossier's own displays are correct. Add the two invalid strings to the "must not use"
    list.

## On the dossier's own issue list

- **CC-1 and CC-11.** The proofs are correct (A1). Apply Correction 1 to C6.
- **CC-2.** The diagnosis is right. The wording needs the scope, and the optional resolution
  does not achieve its aim (Correction 5, A2).
- **CC-3, CC-4, CC-5, CC-8, CC-9, CC-10 and CC-13.** Agreed. The numbers check out, and the
  pruning patch reproduces 11,121/15,329/21,057/27,843 boxes with 61/53/64/62 infeasible.
- **CC-6.** Agreed. Note that the improvement for chain is established only for chain100–400.
- **CC-7.** (a) is correct (2^-9 → 2^-11 is a quartering). (b) is correct but should use the
  explanation in Correction 3.
- **CC-12.** Fix the cost (Correction 4).

## Commands run (targeted; copies under /tmp/critic-chaincatmix; one thread)

- `python3 catmix_exact_critic.py 100:catmix100_u.npy` and the six other vectors, with the
  critic's `osil_generic.py` (log: `catmix_exact_critic.log`).
- Variable-bound and objective check of the four catmix OSIL files (inline script).
- `python3 chain_osil_eval.py`: the critic's OSnL evaluator at 90 digits, run on the
  reconstructed exact chain points.
- Exact gap and display recomputation (inline script).
- `python3 c6_check.py`: Proposition C6 at 50 digits.
- Exact random-u checks of M1, M6 and M8 (inline script).
- Rebuilding the authors' catmix100 grids (`make_grids` on a copy of `catmix_bound.py`) and
  comparing the band run with the uniform 3e-6 run.
- Scan of the MINLPLib listing rule over `R/bound-audit/pages.json`.
- `pdftotext` of the Müller et al. arXiv copy.
