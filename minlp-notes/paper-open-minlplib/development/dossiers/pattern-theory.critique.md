# Critique of the dossier `pattern-theory` (revision r2)

Critic: independent reviewer, 2026-10-04. `R/` means `research-20260929/`.
Scripts and logs of this critique: `checks/pattern-theory-critique/`. They
read only copies placed in `/tmp/ptcrit` (pages.json, fetched.json,
candidates.json, census_merged.json, results_table.csv, gap-values.json, two
OSIL files). No research script was imported or run, nothing under `R/` or
`literature/` was edited, one core was used, and no project-wide check was
run.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.**

- No certificate depends on the theory in this family. The validity lemmas
  that the certificates do use (Lemma 1(a)–(d), Lemma 1′, Propositions 3 and
  4) are correct as stated, up to two technical gaps (C3, C16).
- Every coverage count reproduces with a third, independent implementation:
  1633 → 1257 → 596 → 360 → 294 → 155; 146 scout instances with the stated
  bands; 29 closures and 12 other paper instances among the 155; `fct`.
- Every number in Tables 5.2 and 5.3 that I checked matches its source.
- The dossier says its revision "re-derived every proof independently and
  found no error". Two errors remain:
  - a wrong hypothesis in the pinch-regularity remark (C2);
  - a proof step that produces non-real split constants (C3).
- Several numeric or attribution statements need fixing:
  - chain's census width is 2N+1, not N+1 (C1);
  - the listing-dual count is 1564 plus 4 exceptions under display rounding,
    not 1565 plus 3 (C4);
  - the FAQ quotation comes from a different source than cited (C5);
  - the recheck verdict is misquoted (C6);
  - the lnts width is not explained by `h` (C7).
- Three interpretive readings of the solver evidence go beyond the data:
  - powerflow0039 polar vs rectangular: GUROBI ranks the two forms in the
    opposite order to SCIP (C8);
  - BARON's camshape iteration counts (C9);
  - the "window" wording for optcdeg2 and catmix (C12).

## What I checked

| check | how | result |
|---|---|---|
| Lemma 1(a)–(d) | by hand | correct; F_t domain technicality (C16) |
| lnts use of Lemma 1(d) | against first-wave report §3.2–3.3 (w_j, c_j rational and h-independent; A, B decreasing; ν ≥ 0) | correct |
| Lemma 1′ and the cone induction | by hand; COPS report §3 change of variables `y_i = Q(u_i)x_i`; verifier's DP uses the same principle (verification report 2b, 2d) | correct; the displayed (verifier) catmix duals also rest on Lemma 1′ |
| Proposition 2(a)–(c) | by hand, including the shared-coordinate induction and sign convention | correct |
| Proposition 3 | by hand | correct |
| Proposition 4 and Remark 2 | by hand; LP check on 242 random layered graphs with +∞ edges (`ext_checks.py`) | validity correct; Remark 2 true, but its proof uses −∞ constants (C3) |
| Theorem 5 (extended values) | every step by hand (a, b finite, a + b ≥ 0, shift, clip, deviation ≤ δ); 395 random separators with ±∞ band edges (`ext_checks.py`): max deviation 1.0e-14 | correct |
| Theorem 5, Consequence 3 | against consistency note Lemma 4.2 and calibration note §2.3 | wrong hypothesis (C2) |
| Theorem 6 | by hand (weak duality on head and tail; osc argument) | correct |
| Proposition 7 | by hand: f* = 1, B = 0, V_1 ≡ 1, Γ_2 ≡ 1, bands contain 1 and 0 | correct |
| Proposition 8(a)(b) | by hand, including `2√(2ε/M)·|λ|/(4ε) = |λ|/√(2Mε)` | correct |
| funnel and bands | own code (`recount.py`, Decimal arithmetic) | all counts reproduce; S filter removes nothing from the 294 |
| listing dual = third-best | own code (`listing.py`), strict half-unit display rounding | 1564 + 4 exceptions, not 1565 + 3 (C4) |
| MINLPLib definitions | documentation snapshot l.105–119; MINLPLib site fulltext l.43 | S quote correct; FAQ quote mis-sourced (C5) |
| census widths | census_merged.json | chain: 101/201/401/801 = 2N+1 (C1); others as stated |
| lnts width attribution | own factor-incidence graph of lnts50 (`fw.py`) | min-degree 11 with and without h; min-fill 11 → 7 (C7) |
| Table 5.2 | pages.json (best listed duals and solvers), exact_display_checks.json, gap-values.json | all 15 rows match; every gap cell ≥ exact |
| Table 5.3 and node counts | results_table.csv, SCIP and BARON logs (`Total no. of BaR iterations`) | numbers match; interpretation issues C8, C9 |
| review quotations | consistency, calibration, face-exact, cell-slopes reviews | one misquote (C6) |
| Proposition 2(b) lukvle10 numbers | first-wave report §7 | box counts belong to the author's certificate, not the displayed dual (C10) |

## Corrections

**C1. chain's census nonlinear-primal width is 2N+1, not N+1.**
- *Location:* §0 item 7(iv); §1.2 table (chain row, "census: N+1"); §1.2
  width fact 2; PT-7(ii) and its evidence.
- *Evidence:* `census_merged.json` gives `tw_nlprimal_ub` = 101, 201, 401,
  801 for chain50/100/200/400 (= n_nl − 1 = 2N+1). The dossier's own
  `logs/r2_checks.log` §E prints "census tw_nlprimal_ub: 101" for chain50.
- *Fix:* replace "N+1" by "2N+1 (one clique on all 2N+2 nonlinear
  variables)". The corrected value 1 is right: the chain50 objective is
  `product(sum(x_i·sqrt(1+u_i²) …), constant)`, giving 51 disjoint pairs.

**C2. Pinch-regularity hypothesis is wrong.**
- *Location:* §3.7, Consequence 3 ("If `V_τ` is semiconcave and `Γ_τ`
  semiconvex …").
- *Evidence:* consistency note Lemma 4.2 assumes `U` semiconcave and `L`
  semiconvex. Here `L = f* − Γ_τ`, so `Γ_τ` must be **semiconcave**. The
  calibration note §2.3 says it directly: "This needs `V_t` and `Γ_t` to be
  semiconcave".
- *Counterexample to the dossier's version:* two bags on [−1, 1], with
  `F_1(s) = |s|` and `F_2 ≡ 0`. Then `Γ_1 = |s|` is convex (hence
  semiconvex), `V_1 ≡ 0` is semiconcave, and 0 is an interior pinch point,
  but `Γ_1` is not differentiable there.
- *Fix:* "If `V_τ` and `Γ_τ` are both semiconcave near an interior pinch
  point (equivalently `U_τ` is semiconcave and `L_τ` is semiconvex), …".

**C3. Proposition 4, Remark 2 proof uses non-real constants.**
- *Location:* §3.6 Remark 2: "set `c_{t,D} = −d_t(D)`".
- *Problem:* the definition allows `b_t = +∞` (empty cell pairs). Then
  cells that cannot be reached from the left have `d_t(D) = +∞`, so
  `c_{t,D} = −∞`. That is not a real-valued split. The proof also needs
  `b_t > −∞`.
- *Evidence:* the claim itself is true. An LP over finite constants attains
  SP in all 242 random layered graphs with +∞ edges (`ext_checks.py`).
- *Fix:* assume `b_t > −∞`. Use the finite potentials
  `p_t(D) = min(d_t(D), M_t)`, with `M_t = K + Σ_{s≤t} min(finite b_s)` and
  `K` large. They satisfy all reduced-cost inequalities, are exact on the
  shortest path, and make the last-layer minimum equal to SP.

**C4. Listing dual versus third-best bound: the counts are off.**
- *Location:* §2.1 ("In 1565 of 1568 … up to the listing's display
  rounding"; three exceptions); §6 S-mark row.
- *Evidence:* `r2_checks.py` §B uses a 1e-4 relative tolerance, which is
  not display rounding. With a strict test (half a unit in the listing's
  last digit), 1564 of 1568 match the finite third-best bound
  (`listing.py`). Four match only when `inf` entries are counted:
  ball_mk4_15, chp_shorttermplan2c, **nuclear10a** and powerflow0057r.
  - nuclear10a: the listing shows −12.3336. The finite third-best is
    −12.3337117. With SCIP's `inf` counted, the third-best is XPRESS
    −12.33361376.
- *Fix:* say 1564 + 4. The conclusion (all 1568 agree once `inf` is
  counted) stands.

**C5. The FAQ quotation is mis-sourced.**
- *Location:* §2.1, "The FAQ adds that they are 'just the best value as
  computed in some run …'".
- *Evidence:* this sentence is not in
  `vigerske2026-minlplib-documentation-database-snapshot-2026`. It is in
  `literature/papers/vigerske2026-minlplib-a-library-of-mixed/fulltext.md`
  l.43, the site FAQ ("Last updated: 2026-07-29").
- *Fix:* cite the site slug for the FAQ.

**C6. The recheck verdict is misquoted.**
- *Location:* §6, Theorems 5–6 row: "`consistency-recheck.md` ('Correct as
  revised')".
- *Evidence:* the recheck's verdict is "Fixes needed, all small; no proof is
  wrong". "Correct as revised" heads its list of specific items.
- *Fix:* quote the verdict.

**C7. The lnts width is not explained by `h`.**
- *Location:* §1.2 width fact 1: "lnts's factor-incidence width (11–12)
  comes from the hub variable `h`".
- *Evidence:* I rebuilt the census-style factor-incidence graph of lnts50
  (`fw.py`). Min-degree gives width 11 both with and without `h`; min-fill
  gives 11 with `h` and 7 without. The stage itself (px, py, vx, vy, θ plus
  row and term nodes) already gives a heuristic width of 7–11.
- *Fix:* "lnts's factor-incidence bound (11–12) is a heuristic upper bound.
  The global `h` lies in every separator, and the certificate handles it by
  monotonicity." Drop "comes from".

**C8. powerflow0039 polar versus rectangular overreads SCIP alone.**
- *Location:* §5.3 Reading 2; PT-2 "For it".
- *Problem 1:* "the formulation, not the search, decided" holds for SCIP only.
  - GUROBI ranks the forms the other way: polar 41,765.71 against
    rectangular 41,618.49 (`results_table.csv`).
  - BARON failed on the polar model (capability failure).
  - SCIP's polar run found no primal point.
- *Problem 2:* "carry the same optimum" is not proved. The two OSIL files
  are different models. Their certified enclosures overlap:
  - 0039p: [41869.05148485, 41869.05151133];
  - 0039r: [41869.05148327, 41869.05151133].
- *Fix:* "For SCIP, the rectangular model gave 41,745.9 and the polar model
  2; GUROBI gave the opposite order (41,765.7 polar, 41,618.5 rectangular).
  The pairing of solver and formulation matters. The certified optimum
  enclosures of the two models overlap."

**C9. BARON's camshape iteration counts do not isolate relaxation
strength.**
- *Location:* §0 item 4; §5.3 Reading 3 ("This points to its relaxation
  and range reduction, not to search"); PT-2 ("it reflects a stronger
  relaxation").
- *Evidence:* BARON's dual equals its own incumbent on both instances, and
  both incumbents lie below the exact optimum:
  - camshape100: −4.28414764756 < −4.28414712175;
  - camshape200: −4.27850228570 < −4.27850023299.

  So BARON pruned against an invalid cutoff, with tolerance-based range
  reduction. The 3 and 723 BaR iterations measure how fast it closed
  against that cutoff, not relaxation strength alone.
- *Fix:* "consistent with a strong relaxation and range reduction; BARON
  terminated against an incumbent below the exact optimum, so its iteration
  counts are not clean evidence".

**C10. lukvle10 box counts belong to a different certificate than the
displayed dual.**
- *Location:* §3.11 lukvle10 row ("tail 48,628 boxes; middle group 4643;
  others 900–3800 each"); §1.2 ("34 distinct 2-D pair problems").
- *Evidence:* first-wave report §7.2–7.5. These counts and the grouping are
  the author's certificate (352.238025369202). The displayed dual
  352.2380254050784 is the verifier's: its own multipliers, its own interval
  B&B, pair tolerance 1e-12.
- *Fix:* attribute the counts to the author's certificate, or report the
  verifier's counts.

**C11. The rule-(b) gap definition contradicts the fct case.**
- *Location:* §2.2(b): "(∞ if the signs differ or one value is 0)".
- *Problem:* as written, `p = d = 0` gives ∞. That would make fct open and
  contradict "fct … best single-solver gap 0". The code returns 0 when
  `p = d`.
- *Fix:* "0 if `p = d`; otherwise ∞ if the signs differ or one value is 0".

**C12. "Where the split cannot be exact, a small exact window" is
misleading.**
- *Location:* §3.0 last sentence; §1.1 class-A description; §9 "May claim"
  bullet 2.
- *Problem:*
  - In optcdeg2 the affine split cannot be exact, and the remedy was a
    quadratic class, not a window.
  - catmix uses a nonlinear (chord) value-function class.

  This conflicts with the dossier's own PT-3 facts.
- *Fix:* "where an affine split cannot be exact, a richer split class
  (quadratic for optcdeg2, field-type for chain, concave chord minorants for
  catmix) or a small exact window (the lukvle10 tail, chain's end values)".

**C13. The "May claim" wording for Theorem 5 and Proposition 8 drops
hypotheses.**
- *Location:* §9 bullets 3 and 4; §3.0 ("the loss at one separator is
  exactly twice the distance").
- *Theorem 5:* the identity holds when both sides of the separator are
  minimized exactly (the merged windows in the definition of `Δ_τ`). With
  restricted classes elsewhere, only the lower bound of Theorem 6 holds.
- *Proposition 8:* the cell count needs a one-dimensional separator, exact
  stage minima, and the slope and band-width conditions near the pinch
  point.
- *Fix:* add these hypotheses to the claim sentences.

**C14. The PT-13 conditional strengthening has insufficient hypotheses.**
- *Location:* PT-13 ("Suppose a global minimizer has interior states on an
  arc and a fractional control at a stage …").
- *Problem:* interior states on the arc alone do not force the arc's
  slopes. The costate recursion (Proposition 2(c); calibration note Theorem
  3.1(3)) determines `p_t` from `p_{t+1}`. It therefore needs:
  - C¹ data;
  - interior states at every stage between the arc and the stage that pins
    the remaining terminal freedom (the fractional stage, or the end);
  - `f*` attained at that minimizer, which is known only numerically.
- *Fix:* state these hypotheses or drop the conditional. The dossier's
  recommended wording ("the costate-affine split cannot be exact …; a
  quadratic split closes the gap") is enough for the paper. See also X3.

**C15. The exactness "iff" needs attainment.**
- *Location:* §3.0 ("The bound is exact iff one feasible point minimizes
  every stage problem"); §4 (same).
- *Fix:* add "(the 'only if' direction needs `f*` attained)", as §3.4
  already says.

**C16. Technical points in Lemma 1.**
- *Location:* §3.2.
- *Domain:* `F_t : K_t → R` is defined only on `K_t`, but (a) and (d)
  minimize over enclosures `K′_t ⊇ proj_t(Z)` or sets `Y ⊇ Z` that may
  leave `K_t`. Define `F_t` on `R^{d_t}`, or require `K′_t ⊆ dom F_t`.
- *Wording:* in (d), "Splits are the case in which the `h_k` are the copy
  rows" should say "Affine splits".

**C17. PT-6: the confirmation-pass estimate is too low.**
- *Location:* PT-6 ("about one reviewer-hour"); §6 restatement row.
- *Evidence:* C2 and C3 survived the dossier's own re-derivation. The r2
  numerical checks use only finite (box) data, so they do not exercise the
  extended-valued and constrained cases that make these restatements new.
- *Fix:*
  - budget 2–4 reviewer-hours;
  - name Consequence 3, Remark 2, Lemma 1′ and the extended-value proofs of
    Theorems 5–6 in the scope;
  - optionally include `ext_checks.py` (395 extended-valued separators, max
    deviation 1.0e-14; 242 graphs for Remark 2, 0 failures).

**C18. "May claim" bullet 1 lists too few assumptions.**
- *Location:* §9: "under the stated assumptions (A1/A2 for the three eg_*
  instances)".
- *Problem:* the interval certificates also assume correct outward rounding
  of the libraries used (mpmath iv, ivnp). For lukvle10, both certificates
  share mpmath's interval exp/log (first-wave report §7.5, "Limitation").
- *Fix:* "(A1/A2 for eg_*; correct outward rounding of the interval
  libraries used)", or refer to the assumptions table.

## Additional issues

**X1 (minor). The pattern omits derived enclosures.**
- *The gap:* the certificates derive their own bounds for free states where
  the stage problems need them:
  - optcdeg2's stage minimization runs over the first-wave interval
    enclosures `V_t`;
  - lukvle10 reduces each pair problem to a proved box (§7.3);
  - chain derives the domain of `(z_1, z_N)`;
  - camshape uses bound propagation.
- *Why it matters:* the root log lists "bound propagation for free
  variables" as part of the successful pattern. The paper's interpretation
  stresses free variables.
- *Fix:* add "valid enclosures for unbounded states where the stage
  problems need them (Lemma 1(a) with `K′_t`)" to the pattern statement.

**X2 (minor, user decision). Venue for the band results.**
- *The issue:* Theorems 5–6 and Propositions 7–8 are the consistency note's
  headline "new as far as found" results. Proving them in this paper makes
  it their venue.
- *Recommendation:*
  - main text: Lemma 1, Lemma 1′, Proposition 2(b)(c), Proposition 3, and
    Proposition 4 (validity);
  - one short explanatory subsection: Theorem 5 and Proposition 8, with
    their hypotheses;
  - Theorem 6 and Proposition 7: an appendix, or cite them.
- If the consistency note is to appear separately, cite it instead.

**X3 (minor). Cite the reviewed singular-stage result.** Calibration note
Proposition 4.1 (singular stages obstruct exact affine calibrations) was
reviewed as correct, with the F4 caveat that the "positive gap" consequence
needs dual attainment. It is the reviewed counterpart of the unreviewed
PT-13 conditional. Its own text links it to catmix's bilinear singular arc.
If the paper explains why affine splits fail, cite Proposition 4.1 with its
hypotheses (interior states and controls, C¹ data, unique slopes, `f*`
attained). Do not add a new conditional statement.

**X4 (minor). The optional PT-2 experiment does not test what it claims.**
- Adding certified enclosures as bounds changes both the relaxations and the
  branching, so the runs cannot separate "relaxation" from "branching".
- The dtoc5 and lnts certificates use no enclosures, so there would be
  nothing to add for them.
- The expected inference should be "free variables matter", not
  "relaxation versus branching". The 7–14 CPU-hour estimate is right for
  one or two solvers.

**X5 (minor). Define the family counts.** "7 of the 17 families" counts
waterno2, KAN and ANN alongside the closures. Among the closed families
(14, counting ex6_2_* and powerflow as one family each), 6 follow the
staged pattern. State which population is meant.

**X6 (minor). "Third-best" is an empirical finding.** The MINLPLib
documentation says only that the three best bounds are set in bold. Write
"empirically equals the third-best per-solver bound (`inf` entries
counted)".

## Assessment of PT-1 to PT-13

| issue | assessment |
|---|---|
| PT-1 | correct and sufficient; add C11 (`p = d` case) and X6 |
| PT-2 | direction correct; add C8, C9 and X4 |
| PT-3 | correct; the suggested §9 wording needs C12 |
| PT-4 | correct; Lemma 1′ checked, and also covers the verifier's stronger catmix duals |
| PT-5 | correct (the "partly by sampling" passage is SYNTHESIS l.42, not l.41) |
| PT-6 | correct in substance; the cost estimate and scope are too small (C17) |
| PT-7 | (i) correct; (ii) must say 2N+1 (C1) |
| PT-8 to PT-12 | correct and sufficient |
| PT-13 | the narrower wording is right; the conditional strengthening needs C14, or replace it by X3 |
| §8.2 "nothing invalidates" | agreed |

## Commands run (targeted; from `checks/pattern-theory-critique/`, inputs copied to `/tmp/ptcrit`)

```
OMP_NUM_THREADS=1 python3 recount.py    > logs/recount.log
OMP_NUM_THREADS=1 python3 listing.py    > logs/listing.log
python3 fw.py lnts50.osil; python3 fw.py lnts50.osil 255   > logs/lnts_width.log
OMP_NUM_THREADS=1 python3 ext_checks.py > logs/ext_checks.log
```

I also ran read-only `grep`, `sed` and small inline Python on copies:
- census widths;
- the optcdeg2 variable bound types;
- the chain50 expression tree;
- campaign rows;
- BARON iteration counts;
- review quotations.

No solver, certificate or research script was run, and CI was not
inspected.
