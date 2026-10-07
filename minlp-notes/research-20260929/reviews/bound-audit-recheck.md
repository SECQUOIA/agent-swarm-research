# Recheck of the MINLPLib bound audit: open verification gaps and presentation revision

Date: 2026-09-30. Reviewed: `research-20260929/bound-audit/audit-report.md`
(revised version), with `results.csv` and `results.json`. Earlier review:
`reviews/bound-audit-verification/verification-report.md`. Code, data and logs
for this recheck are in `reviews/bound-audit-recheck/`. Nothing was committed.
No solver developer or MINLPLib maintainer was contacted.

## 1. Summary

**The five unchecked class (i) pairs are confirmed.** For each of them I
built an exactly feasible point in rational arithmetic whose objective is
beyond LINDO's listed dual by more than the display slack. The margins agree
with the audit's margins. With the 14 pairs confirmed earlier, all 19 class (i)
pairs have now been checked with code that is independent of the audit's.

| instance | point | LINDO listed dual d | exactly feasible objective f (exact rational, truncated) | audit enclosure (outward-rounded) | d − f | (d − f)/\|d\| | margin / slack |
|---|---|---|---|---|---|---|---|
| sssd22-08persp | p4 | 508748.972 | 508713.73101118680506… | [508713.7310104, 508713.7310120] | 35.241 | 6.9e-5 | 7.0e4 |
| sssd22-08persp | p3 | 508748.972 | 508719.49127347838546… | [508719.4912727, 508719.4912742] | 29.481 | 5.8e-5 | 5.9e4 |
| sssd25-04persp | p3 | 300186.8048 | 300176.56366586825118… | [300176.5636655, 300176.5636663] | 10.241 | 3.4e-5 | 2.0e5 |
| sssd25-08persp | p4 | 472098.947 | 472093.07796988413312… | [472093.0779691, 472093.0779707] | 5.869 | 1.2e-5 | 1.2e4 |
| sssd25-08persp | p3 | 472098.947 | 472094.42417922338578… | [472094.4241784, 472094.4241801] | 4.523 | 9.6e-6 | 9.0e3 |
| smallinvDAXr2b150-165 | p2 | 88.1049355 | 88.104934760000006 (listed point as is); 88.10493476 exactly with objvar := xᵀQx | [88.104934760000005, 88.104934760000007] | 7.4e-7 | 8.4e-9 | 14.8 |
| smallinvDAXr2b200-220 | p2 | 156.604269 | 156.604267884 exactly | [156.60426788384, 156.60426788416] | 1.116e-6 exactly | 7.1e-9 | 2.23 |

- Each of my values lies inside the audit's enclosure. For smallinvDAXr2b150-165,
  the audit's enclosure is the listed point as is; lowering its objvar to xᵀQx
  gives a second exactly feasible point, 6e-15 lower.
- The audit's labels are right: the three sssd pairs are gross (margin above
  1e-6 of |d|), and the two smallinvDAX pairs are tolerance-scale.
- For smallinvDAXr2b200-220 the margin is 1.116 units in the last shown digit
  of d. So the verdict survives even if the site truncates instead of rounding.
  This is the tightest class (i) case, as for smallinvDAXr1b200-220.

**The emfl exact-optimum claims are confirmed.** For each instance I proved an
upper bound (an exactly feasible point) and a lower bound (an exact
weak-duality certificate). Each of my intervals lies inside the audit's
enclosure, and my gaps are about 100 to 2200 times smaller.

| instance | exact optimum (this recheck, outward-rounded) | gap | audit's proven enclosure (from `logs/cert_socp_*.json`) |
|---|---|---|---|
| emfl050_5_5 | [18.9136329557291, 18.9136329557624] | 3.3e-11 | [18.913632952947, 18.913632956282] |
| emfl100_3_3 | [18.1326531242336, 18.1326531242359] | 2.2e-12 | [18.132653119485, 18.132653124323] |
| emfl100_5_5 | [32.6381903545115, 32.6381903545301] | 1.9e-11 | [32.638190351378, 32.638190354730] |
| emfl050_3_3 (control, confirmed earlier) | [10.4017521318429, 10.4017521318448] | 1.8e-12 | [10.401752131628, 10.401752131871] |

- Every listed dual of the four instances is at or below my lower bound, so
  every listed dual is valid, as the audit says.
- Every statement the audit makes about the emfl optimum values is true (Section 4).

**The presentation revision is consistent with `results.csv` and
`results.json`.** I recomputed, with my own scripts, the class counts,
margins, gross / tolerance-scale split, histogram, per-solver table and screen
counts quoted in the report (Section 5.1), and found no numerical mismatch. I found nine small text problems (Section 5.2). Only one
is a factual error about a proof: Section 5 says ghg_3veh p2 "is exactly
feasible", but only its repair is. None of the problems changes a class or a
verdict.

## 2. Data and independence

- **Data** (`fetch.py`, `logs/fetch.log`). Fetched from minlplib.org:
  - the instance pages, the OSIL files and 22 listed points for the eight
    instances above, plus sssd20-04persp p2 and p3 as a control;
  - requests were sequential, with a 2 s delay.

  Every fetched OSIL file is byte-identical to `~/.cache/minlplib`. Every
  fetched point that the audit also has is byte-identical to the audit's
  `sol/` copy.

  The emfl050_3_3 control used the cached OSIL file. It is byte-identical to
  the previous verifier's fetched copy.
- **Listed values.** `listed.py` extracts the listed points, infeasibilities,
  duals and objective sense from my fetched pages (`logs/listed.log`). They
  agree with the audit's `pages.json` and with the report.
- **Own code** (all in `reviews/bound-audit-recheck/`):
  - `qosil.py`: my own OSiL reader and exact evaluator, using Python
    Fractions.
    - It handles variables, one objective (constant included), row
      constants, `mult`/`incr` arrays, both storage orders of the linear
      coefficients, and quadratic terms.
    - It rejects any other OSiL element. None of the nine models has
      nonlinear expressions.
    - `violations(x)` checks every row, every bound and integrality exactly.
  - `sssd_exact.py`, `smallinv_exact.py`: exact certificates (Section 3).
  - `emfl_bounds.py`: two-sided emfl bounds (Section 4).
  - `sanity.py`: negative controls.
  - `crosseval.py`, `xparse.py`: cross-checks.
  - `consistency.py`, `screen_recount.py`: recomputation of the report's
    numbers (Section 5).
- **Not used:**
  - the audit's code;
  - `reviews/open-instances-verification/osilx.py`. The audit used this
    reader, so it is not independent of the audit.
- **Reused from the previous verifier, as a cross-check only:** its reader
  `reviews/bound-audit-verification/osil.py`, which is separate from the
  audit's.
  - `xparse.py` confirms that my reader and that reader produce identical
    exact data for all nine models (`logs/xparse.log`).
  - `crosseval.py` re-evaluates all eight constructed sssd and smallinvDAX
    points with the verifier's evaluator. It finds 0 violations and
    identical objectives (`logs/crosseval.log`).
- **No interval arithmetic or Krawczyk test was needed.** Every certificate
  here is checked in exact rational arithmetic.
- **Negative controls** (`sanity.py`, `logs/sanity.log`). The unperturbed
  points pass. Each perturbation below makes the exact checker report the
  expected row, bound or integrality violation:
  - lowering an sssd queue variable by 1e-30;
  - raising a utilization variable by 1e-30;
  - setting a binary to 1/2;
  - lowering the smallinvDAX objvar by 1e-30 below xᵀQx;
  - setting an emfl t just below ‖w‖;
  - setting an emfl base variable to −1e-30.

  The exact certificate check also rejects two perturbed emfl duals:
  - one cone scaled by 1 + 1e-12 (the norm condition fails);
  - one g component pushed to −1e-20 (the condition g ≥ 0 fails).

## 3. The five LINDO pairs

### 3.1 sssd22-08persp, sssd25-04persp, sssd25-08persp

**Structure.** `sssd_exact.py` asserts this structure from the OSIL file.
- Binaries b. Continuous utilization variables u, each in one link row
  u − b ≤ 0 and in one load equality Σ aᵢbᵢ − Σ c_l u_l = 0.
- Continuous queue variables q ≥ 0, which appear only in the objective (with
  positive cost) and in quadratic rows −b·q + b·u + q·u ≤ 0.
- All other rows involve binaries only.

**Construction.** The listed binaries are exactly 0/1 in every point used.
With them fixed:
- u = 0 whenever its link binary is 0;
- the load equality then fixes the one remaining u exactly, as a rational
  number. At most one level binary per server is 1.
- A quadratic row with b = 1 reads q(u − 1) + u ≤ 0, that is,
  q ≥ u/(1 − u). With b = 0 it reads q·u ≤ 0, which holds because u = 0.
- I set q to the least allowed value.

The result is the minimum over the continuous variables for the listed
binaries.

**Proof.** The construction only produces a candidate. The proof is the exact
check of every row, bound and integrality condition of the OSIL model, plus
the exact objective value (`logs/sssd_exact.log`). The constructed points
differ from the listed points by at most 7e-12.

**Controls.**
- sssd20-04persp p3 gives 347691.41048398308…. This lies inside both the
  audit's enclosure and the previous verifier's Krawczyk enclosure
  [347691.4104839489, 347691.4104840173].
- The listed p2 points (the points whose values equal LINDO's bounds) repair
  in the same way to objectives within the display slack of LINDO's listed
  numbers (`logs/sssd_p2.log`):
  - sssd22-08persp: 508748.97204582…;
  - sssd25-04persp: 300186.80480598…;
  - sssd25-08persp: 472098.94698466….

  So the current OSIL files reproduce LINDO's numbers at p2. This supports,
  but does not prove, that the model has not changed since 2014.

### 3.2 smallinvDAXr2b150-165 and smallinvDAXr2b200-220

**Structure** (asserted by `smallinv_exact.py`):
- min objvar;
- e1: xᵀQx − objvar ≤ 0;
- three linear rows in the 30 integer variables;
- objvar free.

**Checks** (`logs/smallinv_exact.log`).
- The listed integer values are exact integers.
- **150-165 p2.** The listed point is exactly feasible as listed. Its objvar
  is 88.104934760000006, and xᵀQx = 88.10493476 = 2202623369/25000000.
- **200-220 p2.** As listed, the point violates e1 by exactly 5e-15:
  objvar = 156.604267883999995 < xᵀQx. With objvar := xᵀQx =
  156.604267884 = 39151066971/250000000, the point is exactly feasible.
- These agree with the audit's route A (150-165) and route B (200-220)
  results.

## 4. emfl050_5_5, emfl100_3_3, emfl100_5_5

**Structure** (asserted by `emfl_bounds.py`):
- min Σ c_k t_k with c_k ≥ 0 and no constant;
- cone rows t_k² − Σ_{w∈W_k} w² ≥ 0, with t_k ≥ 0;
- every w is free and appears in exactly one equality row. The other
  variables of that row are base variables z, so w = a_w·z + e_w exactly;
- base variables z ≥ 0, with no upper bound.

**Upper bound.**
- Take z from a numerical Clarabel solve, as exact rationals, clipped at 0.
- Compute w exactly.
- Set t_k to a rational upper bound of ‖w_k‖ (integer square root at 2⁻²⁰⁰).
- The whole OSIL model is then checked exactly: all 9375 rows and 9425
  bounds for emfl100_5_5. The objective is evaluated exactly.

**Lower bound (weak duality).** Take y_k with ‖y_k‖ ≤ c_k and
g = Σ_k A_kᵀy_k ≥ 0. Every feasible point satisfies

Σ c_k t_k ≥ Σ c_k‖w_k‖ ≥ Σ y_k·w_k = g·z + Σ y_k·e_k ≥ Σ y_k·e_k.

- I tried two float candidates for y:
  - the dual SOCP solved directly;
  - the cone multipliers of the primal solve.
- Each was converted to rationals and repaired exactly:
  1. scale each cone into radius c_k(1 − η), for η from 1e-11 to 1e-14;
  2. set each negative g_j to 0 by changing one component of a cone whose
     row of A_k has its only nonzero in column j;
  3. apply a final global scale s ≤ 1 if needed.
- Both conditions are then checked exactly, and Σ y·e is evaluated exactly.
- The best certificate came from the primal multipliers with η = 1e-14. It
  needed at most 24 exact g-corrections of size ≤ 4e-13, and s ≥ 1 − 1e-12.
- The repair differs from both the audit's (`cert_socp.py`) and the previous
  verifier's (a least-norm correction).
- Clarabel reported "optimal_inaccurate". This does not matter, because only
  the exact checks are relied on.

**Results** (`logs/emfl*.log`). The bounds are in the Section 1 table. Every
listed value, compared with my bounds:

| instance | listed duals | listed points (section, listed infeas): exact optimum − value |
|---|---|---|
| emfl050_5_5 | BARON, LINDO, SCIP 18.91340776; ANTIGONE 0.117; COUENNE 0.117: all ≤ LB | p1 (primal, 1e-10) 1.98e-4; p2 (primal, 8e-10) 2.25e-4; p3 (primal, 4e-11) 1.22e-4; p6 (primal, 1e-8) 1.98e-3; p4 (other) 4.44e-3; p5 (other) 8.12e-3 |
| emfl100_3_3 | BARON, LINDO, SCIP 18.13262446; ANTIGONE 0.117; COUENNE 0.118: all ≤ LB | p1 (primal, 1e-10) 2.87e-5; p2 (primal, 2e-10) 2.13e-6; p4 (primal, 1e-8) 2.92e-4; p3 (other) 6.71e-4 |
| emfl100_5_5 | BARON, LINDO 32.63818348; SCIP 32.63818206; ANTIGONE 0.100; COUENNE 0: all ≤ LB | p1 (primal, 1e-10) 6.88e-6; p2 (other) 3.54e-4 |

**Consequences for the audit's emfl statements.** Each of the following is
true:
- "exact optimum ≥ 18.9136329529" (emfl050_5_5) and "≥ 18.1326531194"
  (emfl100_3_3);
- the Section 4 table entries "opt >= 18.91363295295", "18.13265311949" and
  "32.63819035138";
- "emfl100_5_5 … exact optimum in [32.6381903514, 32.6381903547]";
- "the listed optimal value 32.63818348 is below the exact optimum by
  6.9e-6";
- "gaps of at most 5e-9". The audit's largest gap is 4.84e-9 (emfl100_3_3).

The (ii)-proven classification of all 12 emfl pairs holds. The audit's
repaired points (for example 18.914568775 for emfl050_5_5 p6) all lie above
my upper bounds, as feasible points must.

**Stronger than the report says.** In emfl050_5_5, emfl100_3_3 and
emfl100_5_5, every listed point lies below the exact optimum. This includes
primal-section points with listed infeasibility 4e-11 to 2e-10: for example,
emfl050_5_5 p3 (infeas 4e-11) lies 1.2e-4 below. In emfl050_3_3, p1 and p2 lie
below, and only p3 lies above. So, apart from emfl050_3_3 p3, no listed point
value of these four instances is the objective value of any exactly feasible
point. The listed duals are valid. The listed primal bounds (the best listed
values) are all below the exact optimum, so they are not valid primal bounds.

## 5. Presentation revision

### 5.1 What agrees with `results.csv` and `results.json`

I recomputed the following with my own scripts (`consistency.py`,
`screen_recount.py`, `logs/consistency.log`, `logs/screen_recount.log`). All
of them agree with the report:

- **Class counts per (instance, solver) pair**, using the strongest class:
  - (i) gross: 11 pairs, 9 instances;
  - (i) tolerance-scale: 8 pairs, 6 instances;
  - (i-r): 12 pairs, 4 instances;
  - (ii) proven: 12 pairs, 4 instances;
  - (ii) repair: 63 pairs, 11 instances;
  - (iii): 25 pairs, 12 instances;
  - 131 pairs in total. No pair has mixed classes over its points.
- **The split rules.** In every (i) and (i-r) row of `results.json`:
  - "(i) iff d − hi > slack" holds;
  - "gross iff d − hi > 1e-6·|d|" holds;
  - `margin_proved` and `rel_margin` equal d − hi and (d − hi)/|d|.
- **Every margin** in both class (i) tables of Section 1, the Section 4 table
  and the Section 5 margin column.
- **The histogram** of (d − f)/|d|: 6, 2, 7, 1, 3.
- **The per-solver table.** LINDO has 8 gross and 5 tolerance-scale pairs;
  the other solvers match too.
- **"At least 7.9 times the slack in all cases but one".** The smallest ratio
  is 7.95 (watercontamination0303, BONMIN); smallinvDAX*200-220 is 2.23. All
  19 class (i) margins exceed a full unit in the last shown digit.
- **The closing and solved flags:**
  - nd_netgen, watercontamination0303 and the four smallinvDAX instances
    have closing class (i) bounds;
  - the four sssd*persp instances are solved, but LINDO's bound is not
    closing.
- **The screen counts, recomputed from the audit's `pages.json`:**
  - 1633 pages, 2816 points, 11086 duals (11031 finite);
  - 158 flagged pairs over 46 instances and 56 points, 110 of them from the
    "other points" section;
  - 3851 display ties over 1133 instances;
  - no pair skipped for infeas > 1e-5;
  - the flagged set equals the pairs in `results.json`.

  The parsing of the pages was not rechecked, except for the nine pages I
  fetched.
- **Page facts:**
  - the dates behind the Section 5 statements;
  - LINDO's duals equal to p2 (sssd), p3 (methanol50) and p1 (glider100);
  - GUROBI's nd_netgen bound equal to p1;
  - the topopt primal ratio 46.343/10.335 = 4.5.
- **Section 8** agrees with the previous verification report.
- **Inference labels.** Every statement that a solver reported a local
  solution or a point's value as a bound is now marked as an inference: in
  Section 1 (glider100) and Section 5 (LINDO; ANTIGONE and BARON; COUENNE by
  reference).
- **glider100.** I read the listed p2 point myself. My identification of the
  variable blocks is an inference from their values: I did not use the GAMS
  source.
  - tf = x1 = 62163.18 s, so h = 621.63 s.
  - The altitude block (x103–x203, endpoints 1000 and 900) has a maximum of
    64580 m.
  - A block with |value| from 7.77 to 9.77 changes sign at all 100 steps.

  This agrees with the report and the verifier. One detail is missing: the
  altitude first drops to exactly 0 at node 1 (y₁ = 0, a variable fixed at
  its bound in the verifier's proof), and only then rises.

### 5.2 Problems found (text only; no class or verdict changes)

1. **Section 5, ANTIGONE and BARON:** "Point p2, added in 2015, is exactly
   feasible with objective 7.7540060500." This is not correct as written.
   - p2 fails the exact check as listed. The audit's own route A failed on
     row e1 by 5e-14 (`logs/verify/ghg_3veh.p2.json`).
   - The proof is route B: Krawczyk proves that an exactly feasible point
     exists near p2.
   - Suggested text: "Point p2, added in 2015, repairs to an exactly feasible
     point with objective in [7.754006050049, 7.754006050064]."
2. **Section 5, "Tolerance effects (class ii) involve every solver, and they
   are not errors".**
   - AOA and BONMIN have no class (ii) pair.
   - For the 63 (ii)-repair pairs, the validity of d is not proven. The
     report itself calls that class "evidence, not a proof".
   - Suggested text: "involve eight of the ten solvers … the flagged
     conflicts are not evidence of solver errors; validity is proven only for
     emfl*."
3. **Section 5, LINDO:** "the objective of an earlier listed point … methanol50
   (p3)". But methanol50 p3 and LINDO's dual are both dated 15 Feb 2022, so
   the point is not earlier. Suggested wording: "a listed point".
4. **Section 7:** "The glider100 and ghg_3veh bounds date from 2013–2015, and
   their points from 2014–2022."
   - The listed points date from 2011 (ghg_3veh p1) to 2022 (glider100 p2).
   - The two decisive points date from 2015 (ghg_3veh p2) and 2022
     (glider100 p2).
   - So "2014" fits neither reading.
5. **Displayed enclosures are rounded to nearest, not outward.**
   - Section 6 gives emfl100_5_5 as "[32.6381903514, 32.6381903547]". The
     audit's own proven interval is [32.63819035137867, 32.63819035472937],
     so both displayed ends are rounded inward, by 2–3e-11.
   - The "opt >=" entries of the Section 4 table use %.13g, which rounds to
     nearest. For example, "18.91363295295" is 2.8e-12 above the audit's
     proven 18.913632952947.
   - The class (i) and (i-r) enclosures in the tables are also rounded to
     nearest. In the Section 4 table (13 significant digits), some upper ends
     are rounded down, by up to 9.1e-7 (nd_netgen). The upper end is the one
     that sets the margin.
   - My tighter bounds make every displayed emfl statement true. Class (i)
     margins are computed from exact endpoints and exceed these roundings by
     at least six orders of magnitude.
   - Still, a rigorous enclosure should be displayed rounded outward.
6. **The "gross" label and the ghg_3veh caveat.** Section 5 notes that
   ghg_3veh (4.1e-5 of |d|) is "below common relative gap tolerances of 1e-4".
   The same holds for 7 of the 11 gross pairs (sssd ×4, nuclear14 and
   ghg_3veh ×2), whose values lie between 1.2e-5 and 7.3e-5.
   - The report already says that "gross" is a size label only.
   - Stating the caveat for all seven, not only ghg_3veh, would avoid
     implying that the sssd and nuclear14 cases are of a different kind.
7. **Section 1, tolerance-scale pairs:** "far below MINLPLib's 1e-6 relative
   gap convention".
   - For nd_netgen GUROBI, 3.3e-7 is a factor 3 below 1e-6, not "far" below.
   - The claim that the pairs are "below the feasibility and optimality
     tolerances with which solvers compute bounds" is a general judgment.
     The solver settings of these runs are not known.
   - Suggested wording: "below MINLPLib's 1e-6 convention and of the size of
     typical solver tolerances".
8. **Section 1 (glider100):** "the altitude rises from 1000 m". It first
   drops to 0 m at node 1 (Section 5.1).
9. **Header, Section 1 (Rigor) and Section 8 are now out of date.**
   - All 19 class (i) pairs have been checked independently (14 in the
     earlier review, 5 here).
   - The (ii)-proven claims have been checked for all four emfl instances.
   - The earlier review's "Not checked" list shrinks to:
     - the (i-r), (ii)-repair and (iii) rows;
     - the parsing of the 1633 pages. The counts derived from `pages.json`
       have now been recomputed.
     - instance change histories.

## 6. Assumptions and limits

- **Model identity.** The certificates are for the current OSIL files, as
  distributed and cached (byte-identical). Whether each bound was computed on
  the same model version is not known. For the sssd instances, the listed p2
  points still reproduce LINDO's numbers on the current files. This is
  evidence, not proof, that the model has not changed.
- **Display.** A listed number is taken to be within half a unit of its last
  shown digit of the solver's number. The smallinvDAXr2b200-220 margin also
  survives truncation (1.116 units).
- **Arithmetic.** The results rely on Python `Fraction` and integer arithmetic
  (including `isqrt`) being exact. Clarabel and the float steps are
  heuristics only, and every conclusion rests on an exact check.
- **Not checked here:**
  - the (i-r), (ii)-repair and (iii) rows;
  - the parsing of the 1633 pages. I only recounted from the audit's
    `pages.json`, and compared the nine pages I fetched;
  - rocket100/200/400;
  - the audit's Krawczyk-based results for pairs that the previous review
    already confirmed.

## 7. Commands run

These were targeted checks only: no project-wide verification, and no CI. All
runs finished in seconds, single-threaded, with OMP_NUM_THREADS=1,
OPENBLAS_NUM_THREADS=1 and RAYON_NUM_THREADS=1.

```
python3 fetch.py sssd22-08persp:p2,p3,p4 sssd25-04persp:p2,p3 sssd25-08persp:p2,p3,p4 \
  smallinvDAXr2b150-165:p2 smallinvDAXr2b200-220:p2                    # sequential, 2 s delay
python3 fetch.py emfl050_5_5:p1,p2,p3,p4,p5,p6 emfl100_3_3:p1,p2,p3,p4 emfl100_5_5:p1,p2 sssd20-04persp:p2,p3
cmp data/*.osil ~/.cache/minlplib/minlplib/osil/ ; cmp data/*.sol ../../bound-audit/sol/   # all identical
python3 listed.py <9 instances>                                  # logs/listed.log
python3 xparse.py <9 instances>                                  # logs/xparse.log
python3 sssd_exact.py sssd20-04persp.p3=347716.8909 sssd22-08persp.p4=508748.972 sssd22-08persp.p3=508748.972 \
  sssd25-04persp.p3=300186.8048 sssd25-08persp.p4=472098.947 sssd25-08persp.p3=472098.947   # logs/sssd_exact.log
python3 sssd_exact.py sssd20-04persp.p2=... sssd22-08persp.p2=... sssd25-04persp.p2=... sssd25-08persp.p2=...  # logs/sssd_p2.log
python3 smallinv_exact.py smallinvDAXr2b150-165.p2=88.1049355 smallinvDAXr2b200-220.p2=156.604269  # logs/smallinv_exact.log
python3 emfl_bounds.py emfl050_3_3 | emfl050_5_5 | emfl100_3_3 | emfl100_5_5 <label=value ...>   # logs/emfl*.log
python3 crosseval.py                                             # logs/crosseval.log
python3 sanity.py                                                # logs/sanity.log
python3 consistency.py ; python3 screen_recount.py               # logs/consistency.log, logs/screen_recount.log
```

The results in the logs match the numbers reported here.
