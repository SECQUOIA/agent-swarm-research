# Final outline: rigorous certificates for open MINLPLib instances and an audit of listed dual bounds

Target: Mathematical Programming Computation, long paper with appendices and an archived supplement.
Date: 2026-10-04. R = `research-20260929/`. D = `paper-open-minlplib/development/`.

---

## 0. Basis and evaluation of the three proposals

### 0.1 Sources

- The 13 dossiers and critiques in `D/dossiers/`; where they disagree, the critique governs.
- `D/dossier-results.json`.
- The three independent reviews dated 2026-10-04 (`D/reviews/`):
  - `sol-lnts-theorem3.md`: verified;
  - `sol-dtoc5-exact.md`: verified;
  - `sol-kan-rigexp.md`: verified within scope.
- The eg audit code in `D/eg-audit/`: its rerun is not finished.
- `R/open-instances-summary.md`, `R/publication/READINESS.md`, `R/publication/solver-runs/report.md` and `R/publication/integration/gap-values.json`.
- The literature syntheses L1–L3 in `literature/topics/`.
- Every KB slug cited below was checked to exist in `literature/papers/`.

### 0.2 Scores (1 = poor, 5 = strong)

| criterion | P1 referee | P2 rigor | P3 insight |
|---|---|---|---|
| clarity of contribution | 5 | 4 | 4 |
| correctness of claims and novelty boundaries | 4 | 3 | 3 |
| structure and readability for an expert | 4 | 3 | 4 |
| completeness | 5 | 5 | 4 |
| feasibility within the page budget | 4 | 3 | 4 |
| **total (of 25)** | **22** | **18** | **19** |

**P1 (referee).**

Strengths:
- the most precise contribution sentences, with qualifiers attached;
- a consistent category A/B language for disagreements;
- a complete credit list, the longest and most accurate "do not claim" list, and a referee-question map;
- a structure that groups certificates by mechanism, which keeps the common pattern visible.

Defects:
- It treats the lnts, dtoc5 and KAN reviews as pending; all three are now verified.
- Its "Krawczyk primal points agree to 3.5·10⁻⁵⁸" reads as equality. The lnts review proves the stored points strictly suboptimal (their middle control is nonzero).
- C5 omits that the refutations hold under the display hypothesis H.
- It lists 352.238025369202 as unsafe. It is a valid, superseded author bound.
- It names a GUROBI capability failure that the campaign does not record (GUROBI: 0 capability failures, 1 other failure).
- It quotes ex6_2_* box counts without tying them to the certificate whose bound is displayed.
- It misses the dual-side data-reading check, which the primal-points critique (CR-A4) rates major.

**P2 (rigor).**

Strengths:
- the pre-writing dependency on how each dual code reads decimals;
- the claim register;
- evidence levels that separate stored-object checks from search reruns;
- a uniform certificate box, a display record and referee replay tiers.

Defects:
- It states that Vigerske's 2014 paper is "not in the Haugland package". L1 records that the MAGO proceedings PDF is stored under `haugland2014-the-hardness-of-the-pooling`.
- C1 claims a unique dtoc5 minimizer, which the lead author has not adopted.
- C3 makes a "first" claim about R_P, a model we defined ourselves.
- It puts the ann wave-3 figure 16.02% in the KAN table.
- Twelve family-by-family sections repeat one template and hide the shared mechanism.
- Fifteen tables and twelve figures do not fit in 38 pages.

**P3 (insight).**

Strengths:
- a clear thesis with three lessons;
- the recommendations section;
- the headline figure with three markers per instance;
- the structure-to-certificate table;
- treatment of tolerance artifacts in both directions.

Defects:
- The abstract's two-criterion gap ("absolute ≤ 1.5·10⁻⁹ or relative ≤ 2.1·10⁻⁹") is confusing; one relative bound, 3.1·10⁻⁹, covers all 31.
- "Each closure was verified independently with separately written code" overclaims. The displayed catmix and lukvle10 duals are certified by one implementation; the second implementation certifies weaker bounds.
- It lists optcdeg2 among the mpmath-only primal claims, although an integer-interval proof exists and was reproduced by the dtoc5-optcdeg2 critique.
- It cites an internal, unpublished separation result (0.57·(5/3)ⁿ).
- It places the interpretation (§4) before the evidence.
- Its check value 6.22 for the waterno2 factor is rounded up; the safe lower value is 6.21.

### 0.3 What the final outline takes from each

- **From P1:**
  - the overall structure (definitions → results at a glance → certificates grouped by mechanism → points → audit → solvers → interpretation → reproducibility);
  - the contribution wording and qualifiers;
  - the category A/B rules, the credit list, the "do not claim" list and the referee-question map.
- **From P2:**
  - the data-reading check (§9, item 2);
  - evidence levels and the trust table;
  - the certificate box for every theorem;
  - the claim register (App. I), the display record (App. J) and the replay tiers.
- **From P3:**
  - the three lessons (§1 and §11);
  - the recommendations for libraries, solver developers and users (§11);
  - the three-marker headline figure (Fig. 1);
  - the structure-to-certificate table (Table 9);
  - tolerance artifacts that err upward as well as downward.

### 0.4 Facts that changed after the proposals were written, or that the proposals got wrong

1. **lnts Theorem 3 is verified** (`D/reviews/sol-lnts-theorem3.md`).
   - Two integer-only implementations exist: the dossier's, and the reviewer's (rational enclosure width below 1.11·10⁻⁹¹).
   - The attaining point is θ*_j = arctan(ν* r_j). The stored Krawczyk points are strictly suboptimal; their objective enclosures merely contain the optimum enclosure.
2. **The dtoc5 exact certificate is verified** (`D/reviews/sol-dtoc5-exact.md`).
   - The certificate gap is ≤ 7.21·10⁻⁴³; 7.2·10⁻⁴³ is false.
   - The displayed bracket has width 7.3·10⁻⁴³.
   - The computed quantity is a rigorous rational evaluation below the dual function. Do not call it "the exact dual value" or claim a "zero duality gap".
3. **The KAN rigorous-exp rerun is verified within scope** (`D/reviews/sol-kan-rigexp.md`).
   - The r3 searches were rerun; the r5 full searches were not.
   - Both bound paths share `kan_iv`/`ia` (exp and interval core), and this must be disclosed.
   - The review's evidence is only in `/tmp/sol-kan-review/` and must be archived (§9).
4. **The eg exp/pow audit is pending.**
   - `D/eg-audit/cert/auditor.py` is a fresh Cody–Waite auditor. It shares no code with `egfast.fexp`, `kan_iv`, `ia` or r1's `own_ia`, as the eg critique recommends.
   - The written Lemma A1 does not yet exist.
5. **MINLPLib documents no gap formula for the S mark** (chain-catmix critique). The formula |p − d|/min(|p|, |d|) is our scout rule only.
6. **Huang 2011 is a Diplom thesis** (FU Berlin catalog), and only its catalog record was read.
   - A 2022 paper on the adjacent waterno2_04 could not be retrieved (L1).
   - Ghaddar et al. 2015 was also not read.
7. **The displayed lukvle10 and catmix duals each rest on one certifying implementation.**
   - lukvle10: the verifier's 352.2380254050784. The author's own certificate gives 352.238025369202.
   - catmix: `v_catmix_dp`. The authors' code certifies weaker bounds end to end.
8. **Primal trust after reconciliation** (primal-points and dtoc5-optcdeg2 critiques):
   - The mpmath-iv-only primal claims are hvycrash, etamac, pricing050 and pindyck.
   - etamac and pricing050 have one implementation.
   - optcdeg2 now also has an integer-interval proof, which its critique reproduced.

---

## 1. Title

**Recommended: "Rigorous certificates for open MINLPLib instances and an audit of listed dual bounds".** The title states both contributions, contains no priority word, and remains true for the unclosed instances. "Rigorous" avoids suggesting formal verification.

Alternatives:
1. Closing open MINLPLib instances under exact feasibility.
2. Exactly feasible points and rigorous dual bounds for MINLPLib instances listed as open.
3. What benchmark bounds prove: certificates for 31 open MINLPLib instances and an audit of listed dual bounds.

Keep "first", "solved" and "global optima of 43 instances" out of the title.

---

## 2. Abstract draft (about 250 words)

> MINLPLib lists tolerance-feasible points and solver-reported dual bounds, and it marks an instance solved when three solvers claim global optimality. These records are not proofs. We study 43 nonconvex instances without the solved mark under exact semantics: the decimal data of the stored model are read as rational numbers, and a feasible point must satisfy every constraint without tolerance. For 31 instances we prove a dual bound and exhibit an exactly feasible point within a relative gap of 3.1·10⁻⁹; for nine of them we characterize the optimal value exactly. For five pump-scheduling instances we raise the best listed dual bounds by factors of 1.68 to 6.21, leaving gaps of 1.68–10.82%. For ann_cumene_tanh, which has no listed dual bound, we prove one within 0.195% of an exactly feasible point. Six KAN models have no exactly feasible point; for the model without its partition-of-unity rows we enclose the optimum to an absolute width of 2.42·10⁻⁸. The certificates use classical devices (Lagrangian and SDP duality, discrete calibrations, a discrete Sturm comparison, hidden convexity, Taylor-model branch and bound). They are evaluated in exact rational or outward-rounded arithmetic and rechecked by separately written code. Applying the same standard to the 11,086 per-solver dual bounds listed on MINLPLib's instance pages, we prove 19 bounds on 15 instances invalid. We also report a seed-dependent SCIP 10 error that yields wrong optimal values on waterno2 subproblems, and listed and published optimal values that no exactly feasible point attains. In one-hour runs, BARON, GUROBI and SCIP closed none of the 43 instances under exact feasibility. Code, certificates and points are archived for replay.

Checks behind the abstract:
- **3.1·10⁻⁹.** The largest relative gap is catmix800: 1.4844·10⁻¹⁰/0.048056 = 3.09·10⁻⁹. It is the same under every denominator of §4.3.
- **Factors.** 278.230573/165.19 = 1.684 and 4790.820715/770.74 = 6.2159. Both are rounded down.
- **0.195%.** This is δ under the conservative denominator of §4.3 (the dual denominator would give 0.194%).
- **2.42·10⁻⁸.** This is kan_r5_h1_n3; the other five KAN gaps are ≤ 1.08·10⁻¹⁰.
- **"Closed none."** There were 129 kept outcomes and 0 accepted closures. The only two raw optimality claims (BARON on camshape100/200) return values below the proved optima.

---

## 3. Contributions: exact wording and required qualifiers

The introduction states each contribution in this form. "Qualifier" marks text that must appear next to the claim.

**C1. Closures.** "For 31 MINLPLib instances that are not marked solved (instance pages fetched 2026-09-29/30, unchanged at a refresh on 2026-10-02), we prove a dual bound that is valid for every exactly feasible point of the stored OSIL model, and we exhibit an exactly feasible point. Every certified relative gap is at most 3.1·10⁻⁹. For nine of them (camshape100/200/400/800, hvycrash and lnts50/100/200/400) we characterize the optimal value exactly and prove that it is attained."

*Qualifier (search scope):* "To our knowledge, within the search described in Section 1.4 and Appendix D, no rigorous certificate had been published for any of these 31 stored models."

*Qualifier (prior floating-point and other results), in the same paragraph:*

| instance(s) | prior result | sources |
|---|---|---|
| lnts50 | Gurobi closure | Göß–Burlacu–Martin; Table 17 unchanged by the publisher correction |
| lnts100–400 | PARA gaps of 0.00–0.01% | Göß 2026 |
| camshape100 | floating-point solve of the MINLPLib model by Octeract | Bestuzheva et al. 2025 |
| camshape200 | Octeract listed for the rounded copy QPLIB_2480 (value and log unavailable). That copy's optimum exceeds camshape200's by ≥ 9.82·10⁻⁶ | |
| eg_int_s | SCIP 8.1 closure | Göß–Burlacu–Martin |
| dtoc5 | MINOTAUR closure on QPLIB_8585, with assumed default bounds | |
| optcdeg2 | MINOTAUR solve listing on QPLIB_8803 that cannot be checked | |
| powerflow0030p | ANTIGONE closure of the rectangular twin powerflow0030r | |
| powerflow0039p/r | floating-point global solution of the related MATPOWER case39 with transformer taps | Ghaddar et al. 2016 |
| ex6_2_5/7 | possible ε-global results in McDonald–Floudas 1997; unread and unconfirmed | |
| hvycrash | value −0.21850 recorded without proof in the CUTE SIF file | |

**C2. Exactly feasible points.** "Every primal value we report is the upper end of a rigorous enclosure of the objective at a point that satisfies every row, bound and integrality requirement exactly. For 13 closures (lnts50–400, dtoc5, lukvle10, chain50–400, powerflow0030p/0039p/0039r), the earlier closure evidence used points that violate rows by 2.4·10⁻²⁰ to 7.9·10⁻¹²."
- *Qualifier:* the existence tests are classical: Krawczyk, the fixed-coordinate square subsystem of Kearfott 1998, and exact algebraic and triangular definitions. What is new is the points and their independent re-proofs.

**C3. Improved bounds for six unclosed instances.**
- *waterno2:* "For waterno2_06/09/12/18/24 we prove dual bounds 1.68 to 6.21 times the best listed bounds, and we give exactly feasible points. The remaining relative gaps are at most 1.68%, 10.82%, 6.90%, 4.87% and 5.90%."
- *ann:* "For ann_cumene_tanh, for which MINLPLib lists no dual bound, we prove the bound −3386.5403 and exhibit an exactly feasible point within 0.195%."
- *Qualifier (waterno2):* "No closure of these stored models was found in the retrievable literature. Huang's 2011 Diplom thesis cited by MINLPLib, a 2022 paper on waterno2_04 and Ghaddar et al. 2015 could not be read. We claim no priority for period decomposition."
- *Qualifier (ann):* "The bound applies verbatim to the algebraically identical ann_cumene_exp, which SCIP and LINDO closed in floating point; our rigorous bound is weaker than their values."

**C4. KAN models.** "All six KAN models in MINLPLib are infeasible in exact arithmetic. With the decimal B-spline coefficients, the partition-of-unity rows of a single edge have no common solution on any admissible knot interval (exact certificates). For the model without these rows (R_P), we enclose the optimal value to an absolute width of at most 2.42·10⁻⁸ (kan_r5_h1_n3) and 1.08·10⁻¹⁰ (the other five). The lower ends also bound the network relaxation R." Add: "Published zero-gap SCIP optima for kan_r3_h1_n4/n5 lie at least 1.70·10⁻³ and 2.03·10⁻³ below the certified minimum of R; they are tolerance artifacts."

**C5. Audit of listed dual bounds.** "We screened all 11,086 per-solver dual bounds displayed on MINLPLib's 1,633 instance pages against the 2,816 listed points. For 19 bounds on 15 instances we prove, under a stated hypothesis on how pages display numbers, that no number displayed as the listed string is a valid dual bound. Each proof exhibits an exactly feasible point and was repeated by a second implementation. Eleven margins exceed 10⁻⁶·|d|, four of them 1%. The other eight lie below MINLPLib's gap tolerance and contradict no solved mark. For the four emfl instances every listed dual is valid, while their best listed primal values lie below the exact optimum."
- *Qualifier (novelty):* "MINLPLib 2 cross-checked dual bounds by agreement among solvers [Vigerske 2014], and wrong solver bounds have been reported for individual instances [Nowak–Vigerske 2008; Vigerske–Gleixner 2017]. To our knowledge, within the search of Appendix D, this is the first systematic screen of MINLPLib's listed per-solver bounds that decides each conflict by proving that an exactly feasible point exists." No cause and no solver bug is attributed.

**C6. Solver and published claims under exact semantics.**
- **SCIP defect.** "SCIP 10.0.2, 10.0.3, 10.1.0 and a tested development commit return wrong optimal values on subproblems of waterno2_06 for some random seeds."
  - Exactly feasible rational witnesses refute the claims, and SCIP's own feasibility check accepts the witnesses.
  - A 15-variable model reproduces the error.
  - In instrumented runs, reverse propagation removes the witness because of a binary64 residual in a cubic equality whose bounds agree in decimal: the tightest outward enclosure of fl(0.7)³ lies below fl(0.343).
  - *Qualifier:* "To our knowledge not previously reported (SCIP issue tracker searched 2026-10-02)." Add "reported upstream" only if it is true at submission.
- **CAMINO.** The best bounds recorded for Gurobi 13.0.0 on eg_* exceed objectives of exactly feasible points by at least 4.3%, 7.4% and 80%. The CSV has no status column, and the cause is unknown.
- **MINOTAUR.** Its optcdeg2 (QPLIB_8803) infeasibility report is false, assuming its `.nl` file encodes the MINLPLib model.
- **Category A catalogue.** Listed and published optimal values that are not attainable under exact feasibility (§8.1).

**C7. One-hour comparison.**
- Setup: BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3; one thread; 3600 s; requested gaps 10⁻⁹; all 43 instances.
- Results:
  - No accepted closure.
  - All 109 finite final dual bounds are weaker than the certificates.
  - BARON's two optimality claims (camshape100/200) come with valid dual bounds within 1.23·10⁻⁷ and 4.80·10⁻⁷ relative of the exact optima, which is a tolerance-level closure by one solver. Their returned values lie 5.26·10⁻⁷ and 2.05·10⁻⁶ below the optima.
- *Qualifier:* no performance ranking.

**C8. Structure and interpretation.** "Fifteen closures share one certificate pattern. The objective is split along the model's stage structure using Lagrange multipliers, a discrete calibration, or chord minorants of concave value functions. The resulting stage problems are small enough to be minimized rigorously, over derived enclosures of unbounded states. Two of the fifteen add an exactly minimized window. We state the validity results in the extended-value, constrained form that the certificates need."
- *Qualifier:* the mechanisms are classical (Krotov, Mangasarian, Lagrangian decomposition, relaxed dynamic programming). The interpretation of why the instances stayed open is labelled as such and was not tested by experiment.
- *Optional (decision D1):* the band identity and the constant-cell bound, which are explanatory only.

**C9. Reproducibility.** A public archive contains:
- the models with SHA-256 hashes;
- certificate data;
- exact point definitions;
- the checkers and the independent re-implementations;
- a claim register mapping every reported number to its artifact;
- replay commands in three tiers.

The archive separates replay of stored certificates from regeneration.

**What is classical (one paragraph in §1.4).** The following predate this work:
- Lagrangian, SDP and Krotov/Mangasarian sufficiency arguments;
- discrete Sturm comparison and the Gibbs tangent-plane test;
- hidden convexity;
- Taylor models, affine arithmetic and safe LP bounds;
- interval existence tests and rational PSD certificates.

What is new: the instance-specific constructions, their exact or outward-rounded evaluation, the two-sided verification on the stored models, and what these reveal about benchmark data and solver claims.

---

## 4. Notation and conventions (paper §2, plus a one-page boxed table)

### 4.1 Model semantics

- **The model M_I** is the MINLPLib OSIL file for instance I, identified by its SHA-256 hash.
  - Every numeric string (bounds, coefficients, `number` nodes, constants) is read as the rational number its decimal denotes.
  - OSiL defaults apply: variable bounds [0, ∞), continuous type, row bounds (−∞, ∞), coefficient 1, constant 0.
  - `sqrt` is the nonnegative root and `ln` the natural logarithm. `power(a, b)` with a > 0 is exp(b ln a); integer powers are exact.
  - **Domain rule:** every expression must be real-valued at the point (nonzero denominators, positive log and power bases, nonnegative sqrt arguments). The rule matters for hvycrash, ex6_2_* and lukvle10.
  - Integrality and fixings are exact.
- **Three readings:**
  - (a) the `.gms` text with exact decimals;
  - (b) the OSIL text with exact decimals;
  - (c) binary64 data, which solvers see and which the OSiL schema's `xs:double` typing suggests.
- **All claims concern reading (b).**
  - Reading (b) follows exact-MIP practice for rational input data (Cook et al. 2011; Eifler–Gleixner 2023; Hoen–Gleixner 2025).
  - (a) = (b) exactly for most instances. Exceptions:
    - catmix: the OSIL prints binary64 products such as 0.045000000000000005; Proposition M8 transports the lower bounds to c = 9a;
    - methanol50 (audit): 360 objective coefficients with relative change ≤ 2.4·10⁻¹⁶;
    - stockcycle: no exact comparison.
  - Under (c), the dtoc5, chain and powerflow points are known to be infeasible. Feasibility of the other points under (c) is not established. The camshape and hvycrash exact values, and every gap at or below the 10⁻¹⁶ relative scale, are statements about (b).
- **Sets and values.**
  - F(M) is the set of exactly feasible points.
  - v*(M) = inf over F(M) of f, with v* = +∞ if F(M) = ∅.
  - A point is ε-feasible if every row and bound is violated by at most ε in its written scaling. This is MINLPLib's documented measure (maximal absolute violation).
- **Sense.** All instances minimize except pricing050, which maximizes. The sign is s = +1 for minimization and s = −1 for maximization, and every direction below is reversed for maximization.

### 4.2 Bounds, enclosures, closure

- **Valid dual bound:** L ≤ v*(M).
- **Optimum enclosure [L, U]:** L is valid, and U is the upper end of a rigorous enclosure of f(x*) for a proved x* ∈ F(M).
- **Closure:** an optimum enclosure with δ ≤ 10⁻⁶ (δ as in 4.3). This is MINLPLib's gap tolerance applied under exact semantics; it does not earn an S mark.
- **Exact optimum:** v* is characterized and attained.
  - camshape and hvycrash: rational values.
  - lnts: N·h*, with h* defined by a scalar equation and enclosed by rationals of width below 10⁻⁶⁰.
  - "Gap 0" is printed only together with "attained exact optimum", and never as a difference of displays.

### 4.3 Gaps

- **Absolute gap:** Δ = s(U − L), computed from exact source values (`gap-values.json`, certificate rationals) and printed rounded up.
- **Relative gap (single convention):** δ = Δ / min(|L|, |U|).
  - This is the conservative choice: every printed δ also bounds Δ/|L| and Δ/|U|.
  - It matches the scout rule in 4.5.
  - It keeps the summary cells for waterno2 (dual denominator, since the values are positive) and ann (0.195%).
  - It changes no closed-table cell beyond its last digit. All relative cells are regenerated by script.
  - KAN gaps are absolute only, because the values lie near or across 0.
- **Percent cells** have two decimals and are rounded up.
- **Displays versus gap cells.** A gap cell may be smaller than the difference of the two printed displays. Either print enough digits that the displays reproduce the cell, or footnote that the cell uses the exact enclosure. The small critique found this mismatch for ex6_2_5 (2.59·10⁻¹⁵ against ≤ 2.1·10⁻¹⁵) and etamac.

### 4.4 Display directions

- Dual displays are truncated toward the infeasible side (down for minimization), so each display is itself a valid bound.
- Primal displays are rounded toward the feasible side (up for minimization).
- Gap cells and deficit upper bounds (D_n(ε)) are rounded up. "At least" margins are rounded down.
- Exact optima are shown with both a floor display and a ceiling display.
- Shortest-repr binary64 strings and float-printed log fields are never printed as bounds. The list of known unsafe strings is in Appendix J.

### 4.5 Listed data and "open"

- **Snapshot.**
  - The site was last updated 2026-09-14.
  - Instance pages were fetched 2026-09-29; audit pages 2026-09-30.
  - A refresh on 2026-10-02 found the relevant pages, marks, points, bounds and OSIL files unchanged. Claims concern this snapshot, not the later live state.
- **Best listed dual:** the best single-solver bound on the instance page.
- **Listing dual:** the value in the instance list.
  - It empirically equals the third-best per-solver bound, counting `inf` entries, in all 1,568 instances with at least three finite bounds. This is an observation, not a documented rule.
  - `.solu` `=bestdual=` empirically equals min(third-best including `inf`, lowest listed point) in 589 of 589 cases.
  - Pages bold the three best bounds.
  - Instances with fewer than three duals (e.g., catmix) have no listing dual.
- **Listed point:** a point together with its listed maximal absolute violation.
- **"Open", sense (a): no S mark.** MINLPLib defines the mark as: "at least 3 solvers claim global optimality (up to a relative optimal tolerance (gap) of 10⁻⁶)", or at least three claim infeasibility (documentation snapshot). No gap formula is documented. All 43 paper instances lack the mark. **"Listed as open" in the paper means sense (a).**
- **"Open", sense (b): the scout rule (our selection rule).** Take the best single-solver listed dual d and the best listed point p with listed violation ≤ 10⁻⁸. Define gap(p, d) as follows:
  - 0 if p = d;
  - otherwise ∞ if the signs differ or one value is 0;
  - otherwise |p − d|/min(|p|, |d|).

  The instance is open in sense (b) if gap(p, d) > 10⁻⁴; missing values count as open. camshape100 (gap 1.2·10⁻⁶) and lnts50 (3.9·10⁻⁵, rounded up) are open in sense (a) only.

### 4.6 Arithmetic, trust base and verification terms

- **Arithmetic tags** (one per dual and primal computation; Table 1):
  - [E] exact rational or algebraic arithmetic (Python integers, `Fraction`, `isqrt`, GMP);
  - [I] mpmath 1.3.0 interval arithmetic at a stated precision, with the primitives used named (+ − × ÷, sqrt, exp, log, sin, cos);
  - [F] own outward-rounded binary64 arithmetic: one `nextafter` step per operation, or a proved padding lemma;
  - [L] a named hypothesis on a library function. After the eg audit, none should remain. If one remains, it is stated as an assumption.
- **Trust base terms:**
  - **T-int:** integer and rational arithmetic.
  - **T-fp (H0):** IEEE binary64 round-to-nearest with gradual underflow; `nextafter` and power-of-two scaling exact.
  - **T-mp:** mpmath iv outward rounding for the named primitives.
  - **T-read:** OSIL reading under 4.1, with the number of separately written readers.
  - **T-code:** correctness of the named checking programs (reviewed, not formally verified).
  - **T-thm:** the classical theorems used (mean value, intermediate value, Brouwer, Sturm, Lindemann–Weierstrass, series remainders).
- **Evidence levels:**
  - **P:** pen-and-paper proof.
  - **C:** computer-assisted; a stored finite certificate is checked by exact or outward-rounded replay.
  - **S:** computer-assisted; checking needs a deterministic rerun of a search whose tree is not stored (waterno2, ann, eg, KAN, ex6_2_*, lukvle10, chain).
  - Numerical evidence never supports a claim.
- **Verification terms:**
  - **Separately written implementation:** code written without importing or reading the other party's code, except where stated. Table 1 records which implementation certifies the displayed value and what the other one certifies.
  - **Separate reader:** an independent OSIL parser.
  - **Replay:** same code and saved inputs. **Regeneration:** the multiplier or tree search is rerun; it may produce a different valid certificate (waterno2_18/24, the topopt p5 point).
  - **Negative control:** a perturbed input that must be rejected.
- **Disclosure (required, in §2.6 and the declarations).** The certificates, the independent implementations and the reviews were produced by separate AI-agent sessions without shared code. The main common-mode risk is a shared misreading of OSiL semantics. The human-responsibility wording is decision D7.

### 4.7 Language for disagreements

- **Category A (tolerance artifact):** a reported value is not attainable by any exactly feasible point (or a reported point is not exactly feasible), while the reported dual bound, if any, is valid.
  - Wording: "not attainable under exact feasibility", "feasible only within a tolerance".
  - Category A covers both directions. Values can lie below v* (camshape p2) or above a value that every feasible point attains (hvycrash p1/p2: −0.21413 against the constant −0.2185).
- **Category B (invalid claim):** a reported dual bound or infeasibility claim is contradicted by an exactly feasible point.
  - Wording: "invalid as listed" or "invalid as recorded; cause unknown".
  - "Wrong optimal value" and "defect" are used only for SCIP, the one case refuted under the solver's own tolerance semantics and with a traced mechanism.
- **Credit tolerance-level closures explicitly:**
  - BARON on camshape100/200 (our campaign);
  - Octeract on camshape100;
  - Gurobi on lnts50 and SCIP 8.1 on eg_int_s (Göß–Burlacu–Martin);
  - PARA on lnts100–400;
  - SCIP and LINDO on ann_cumene_exp;
  - ANTIGONE on powerflow0030r;
  - MINOTAUR on dtoc5 (default-bound caveat);
  - the hvycrash SIF value.

### 4.8 Object notation

- OSIL names are kept (x⟨k⟩, e⟨k⟩).
- For KAN, R is the network relaxation over the inputs and R_P is the OSIL model minus the partition-of-unity rows; min_R F ≤ min R_P.
- u(s) is the unit of the last displayed digit of a listing string s.
- fl is round-to-nearest binary64, and u = 2⁻⁵³.

---

## 5. Section-by-section plan (main text ≈ 39 pp)

Every theorem gets a **certificate box** with these fields:
- inputs (hash prefixes);
- the computation and its arithmetic tag;
- data reading of the code (exact / outward enclosure / to confirm);
- the implementation that certifies the displayed value, and what the second implementation certifies;
- evidence level;
- replay time.

Theorem numbers below are the paper's.

### §1 Introduction (4.5 pp)

**1.1 Benchmark records are not proofs (1.25 pp).**
- **What MINLPLib records:**
  - points, with their maximal absolute violation;
  - per-solver dual bounds, which the FAQ calls "just the best value as computed in some run with some option settings on some machine at some time in the past" (`vigerske2026-minlplib-a-library-of-mixed`);
  - the S mark (4.5).
- **Why it matters.** Listed values serve as ground truth in solver testing, in learning-based studies (GoML's "GOpt" labels within 0.1% of reference values) and in published claims (CAMINO, the KAN study).
- **Example box (camshape800).**
  - The exact optimum −4.27427414195420… is rational, with a half-page proof.
  - The best listed dual is −5.12584096.
  - The listed point p2 violates rows by up to 3.0·10⁻¹⁰ (hundreds of rows by about 10⁻¹⁰) and lies about 3.3·10⁻⁵ below the optimum. Table 7 prints the logged value, rounded down.
- **One sentence on lnts50.** Its listed point p1 (row violation 9.1·10⁻¹⁰) lies at least 4.24·10⁻¹¹ below the optimum.

**1.2 Approach and three lessons (0.75 pp).**
- **Approach:**
  - exact semantics (b);
  - two-sided certificates;
  - structure-specific bounds;
  - rigorous evaluation;
  - separately written re-implementations;
  - the same standard applied to listed bounds and solver claims.
- **Three lessons** (from P3; repeated in §11):
  1. In every closure the decisive step was a bounding argument fitted to the model's structure. Afterwards, branching was absent or confined to a few dimensions in 27 of 31 closures (an interpretation, §9).
  2. Fifteen closures share one pattern: a split along stage structure with rigorously minimized stages.
  3. Exact feasibility changes the verdict on benchmark data and solver output. Some listed dual bounds are invalid. Some listed and published optimal values hold only within tolerances, and long chains amplify such tolerance effects. SCIP has a defect caused by a binary64 residual.

**1.3 Contributions (1.25 pp).** C1–C9 with their qualifiers (§3 of this outline). State that the certificates are built per instance and that no general solver capability is claimed.

**1.4 Prior work and what is classical (1 pp).** As planned in §7 of this outline, closing with the novelty limits:
- Halbig et al. (17 convex MINLPLib certificates);
- Vigerske 2014 (cross-solver bound check);
- the classical mechanisms;
- the floating-point closures in C1.

**1.5 Organization (0.25 pp).**

- **Box 1 ("Results at a glance"):**
  - 31 closed, 9 with exact optima;
  - 5 waterno2 instances improved, and ann bounded within 0.195%;
  - 6 KAN models exactly infeasible, with R_P enclosed;
  - 19 invalid listed bounds on 15 instances, plus 3 LINDO rocket bounds outside the screen;
  - one SCIP defect;
  - 0 exact closures in 129 solver runs.

### §2 Exact semantics, certificates and verification (4 pp)

**2.1 Model semantics.**
- Definitions 2.1–2.2 (4.1).
- Remark on the three readings and what transfers between them, with three sensitivity facts:
  - camshape: perturbing c, ū, α and c₀ by 10⁻¹⁴ moves the optimum by at most 5.9·10⁻¹¹ (n = 100) to 3.6·10⁻⁹ (n = 800);
  - KAN: the readings differ qualitatively (feasible within tolerance, infeasible exactly);
  - audit: margins of at least 1.9·10⁻⁹ relative against data rounding of about 10⁻¹⁶. This makes transfer to (c) plausible, not proved.

**2.2 Certificates.** Definition 2.3 (4.2) and the statements below.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Lemma 2.4 | (a) If L is valid, x* ∈ F(M) and f(x*) ≤ U, then L ≤ v* ≤ U, and U − L bounds both v* − L and f(x*) − v*. (b) If f(x̂) < L for a valid L, then x̂ ∉ F(M). | §2.2 (3 lines) | P |
| Lemma 2.5 | If L = inf_{x∈X} [f + λᵀh + μᵀg] with μ ≥ 0, every x̃ ∈ X with ‖h(x̃)‖_∞ ≤ τ and g(x̃) ≤ τ satisfies f(x̃) ≥ L − τ(‖λ‖₁ + ‖μ‖₁). Large multiplier mass along chains amplifies tolerance artifacts. | §2.2 (3 lines) | P |
| Prop. 2.6 | A refutation by an exactly feasible point holds for every feasibility tolerance (every tolerance-relaxed feasible set contains F(M)). A tolerance-feasible point below a valid bound refutes nothing (emfl050_3_3; BARON camshape). Data rounding (reading (c)) is not covered. | §2.2 | P |

**2.3 Categories A and B** (4.7).

**2.4 Display rules** (4.4), with a pointer to the display record (App. J).

**2.5 Arithmetic and trust base.**
- **Table 1 (trust base and verification by family).** One row per certificate family. Columns:
  - dual arithmetic tag and the library primitives trusted;
  - data reading of the dual code (confirmed / to confirm; §9 item 2);
  - the implementation certifying the displayed dual, and the value the second one certifies;
  - number of OSIL readers;
  - evidence level;
  - primal construction and its arithmetic;
  - whether an mpmath-free primal re-proof exists.
- **Known entries:**

| family | dual: arithmetic and library primitives | implementations certifying the displayed dual | primal |
|---|---|---|---|
| lnts | [E] for Theorem 4.6 (two integer-only implementations) | two | [E] |
| dtoc5 | [E] (author + review) | two | [E] |
| optcdeg2 | [E] dual; an IEEE-interval second implementation gives 293.8760750958728 | one exact, one interval | integer-interval proof, reproduced by the critique |
| camshape | [E] | three implementations agree to 30 digits | [E] |
| powerflow | [E] dual and PSD proof; the angle-free 0039p variant was replayed by an independent reader | two | [I]/[E] Krawczyk |
| lukvle10 | [I] exp/log, shared by both certificates | displayed value from the verifier only (author: 352.238025369202) | mpmath-free |
| chain | [I] sqrt/log | two | [E] in Q(√R_N) |
| catmix | [F] + − × ÷ only | displayed value from `v_catmix_dp` only; the authors' code certifies weaker bounds | exact rational states |
| ex6_2_*, etamac, pricing050 | [I], via the verifier's sympy-to-iv compiler (the third Gibbs code is separate) | verifier | etamac and pricing050: [I], one implementation |
| pindyck | displayed value is the author's (A1-type padding analysis); the review's code is [F] (nextafter) + [I] | author's | [I] |
| hvycrash | P (identity) | — | [I] backward definitions; two implementations, both mpmath |
| eg | route R with exact final tests and exact coverage, Lemma A1 proved, exp/pow audited **[pending]**; route S-I is a second certificate for eg_int_s, eg_disc_s and eg_disc2_s part 1 (guard caveat) | route R | [E] dyadic checks |
| waterno2 | rbb [F] with decimals enclosed outward; vbb/vbb2 with exact rational node bounds | either code alone yields every value | [E] algebraic |
| ann | [F], two codes, no library transcendental | two | [F] forward construction |
| KAN | [F]; both paths share `kan_iv`/`ia` exp after the rerun | reported L is the weaker of two codes | [E] rational intervals |

**2.6 Verification protocol and its limits (0.75 pp).**
- **Protocol:**
  - an author implementation and a separately written implementation;
  - separate OSIL readers where stated (the shared `osilx` reader was closed by an exact comparison with `rosil` for ANN and KAN);
  - negative controls;
  - replay distinguished from regeneration.
- **Mitigations for the common-mode risk:**
  - exact comparison of GAMS and OSIL forms;
  - SCIP accepting our points at tight tolerances (evidence only);
  - small residuals of MINLPLib's listed points under our readers;
  - the public archive.
- Nothing is formally verified.
- AI-agent disclosure (4.6).

### §3 Instances and results at a glance (3 pp)

**3.1 Snapshot and selection.**
- **Funnel**, as one sentence plus a small inline table (figure version in App. D):
  1,633 pages → 1,257 nonconvex → 596 without S mark → 360 meeting the width rule → 294 with listing gap > 10⁻⁴ (283 scout + 11 first wave) → 155 open by the scout rule → 29 closed here, plus 12 other paper instances. camshape100 and lnts50 are the two closures outside the 155.
- **Caveats (must appear):**
  - The funnel is a post hoc reconstruction.
  - The first wave came from a partial census.
  - Later targets were ranked by judged tractability and payoff, so 29/155 is not a solve rate.
  - Widths are heuristic min-degree upper bounds (chain's census width is 2N+1).
  - The scout and census code was not independently reviewed, but all counts reproduce with three implementations.
  - `fct` (footnote) does not change the 155.

**3.2 Table 2: the 31 closures.** Columns:
- instance; sense; variables (integer) / rows;
- best listed dual (solver);
- certified L (safe display);
- U (safe display) or "exact";
- Δ and δ (regenerated from `gap-values.json` and the certificates);
- certificate class (A staged, A′ comparison, B few dense rows, C global duality/convexity, D identity, E cancellation-preserving enclosures);
- arithmetic tag;
- prior-status code: F (floating-point solve of the same model), f (floating-point near-closure), Lst (listing that cannot be checked), T (twin or related model solved), K (value known without proof), U (possible result in an unread source), N (none found).

Current numbers:
- **lnts:** 16-decimal floor and ceiling displays from the lnts review, e.g. 0.5546687649386788 ≤ v* ≤ 0.5546687649386789 for lnts50; U column "exact".
- **dtoc5:** L = 5.38967211918114046742396649913627186883131268…, certificate gap ≤ 7.21·10⁻⁴³.
- **optcdeg2:** L = 293.87607509587509237 (truncated), U ≤ 293.87607509587509328, Δ ≤ 9·10⁻¹⁶.
- **lukvle10:** 352.2380254050784 / 352.2380254064957, Δ ≤ 1.42·10⁻⁹.
- **eg_disc_s:** L = 5.760539610694993 (safe under every route).
- **ex6_2_5 and etamac:** longer safe displays (4.3).

**3.3 Table 3: the other 12 instances.**
- **waterno2_06–24.** Columns: listed dual; L; exact primal U; δ; factor L/(listed dual), rounded down. For waterno2_06 add the progression: wave 2, separator branching, then cell slopes (263.735099 → 272.584700 → 278.230573).
- **ann_cumene_tanh.** L* = −7447080719734483·2⁻⁴¹ (display −3386.5403); U = −3379.9823940; δ ≤ 0.195%.
- **KAN.** Columns: listed dual and primal; [L, U] for R_P; Δ; published SCIP optima marked if below L.

**Figure 1 (headline).** One row per instance, on a log scale. It shows the relative distance to the certified primal of:
1. the best listed dual;
2. the best one-hour solver dual with a globality guarantee;
3. the certified dual.

Separate markers flag "no finite bound", "only BARON values that BARON disclaims", "SCIP on a tightened model" and "R only (KAN)". Data come from the summary, `results_table.csv` and `gap-values.json`.

**3.4 Prior status (0.5 pp).** One paragraph of credits (C1 qualifier). Name the cases where the improvement is in rigor, not size:
- camshape100: listed duals already within 1.3·10⁻⁶ relative;
- lnts50: listed duals already within 3.9·10⁻⁵ relative.

Full detail is in App. D.

### §4 Split certificates along stage structure (7 pp)

**4.1 Path model and validity (1.75 pp).** Model (P):
- bags z_t ∈ K_t;
- separators s_t = π^R_t z_t = π^L_{t+1} z_{t+1};
- costs F_t defined on all of ℝ^{d_t}, extended-valued.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Lemma 4.1 | Split bound. For any split φ and enclosures K′_t ⊇ proj_t F(P), Σ_t inf_{z∈K′_t} [F_t(z) + φ_t(π^R_t z) − φ_{t−1}(π^L_t z)] ≤ v*. (b) If one stage infimum is +∞, then F(P) = ∅. (c) The bound holds for the minimum over a finite cover (case split). (d) Row form: the bound holds after adding valid aggregated identities; affine splits are the case of copy rows. | App. G.1 | P |
| Lemma 4.2 | Value-function minorants. If W_i ≤ V_i at every stage (by induction), then inf W_0 ≤ v*. For cone-valued linear dynamics with concave, positively homogeneous value functions, chord interpolation over ordered rays preserves minorance. (catmix; not an instance of Lemma 4.1.) | App. G.2 | P |
| Prop. 4.3 | Affine splits. (a) An affine split is the Lagrangian dual of the copy formulation. (b) It is exact if one feasible point minimizes every stage problem; the converse needs v* attained. (c) At an interior, differentiable optimum, exact slopes equal the copy multipliers (discrete costates). This explains why multipliers come from one local KKT solve. | App. G.3 | P |
| Prop. 4.4 | Windows. Merging stages a..b into one exactly minimized window gives B(φ) ≤ B_[a,b](φ) ≤ v*. | App. G.3 | P |
| Prop. 4.5 | Cellwise slopes. One slope vector per separator cell, shared by both adjacent bags, gives v* ≥ the shortest path over the cell-pair bounds. With exact pair bounds and a partition, this equals the best cellwise-affine split (proof with finite potentials, assuming b_t > −∞). | App. G.4 | P |

- **Remark (derived enclosures).** Several certificates derive enclosures K′_t for unbounded states: optcdeg2's V_t, lukvle10's pair boxes, chain's end values. Valid enclosures are part of the pattern.
- **Classical-basis paragraph:**
  - Krotov 1967 and Mangasarian 1966;
  - Lagrangian decomposition: Geoffrion; Karuppiah–Grossmann; Khajavirad–Michalek; Cao–Zavala;
  - relaxed dynamic programming: Lincoln–Rantzer;
  - LP formulations for bounded-treewidth polynomial optimization: Bienstock–Muñoz.
- **Table 4 (the 15 staged certificates, plus a waterno2_06 row).** Columns:
  - stages and separator dimension;
  - free variables;
  - split class (affine, quadratic, field-type, chord minorant, cellwise affine);
  - validity result;
  - window or case split;
  - stage-check method and branching dimension;
  - arithmetic.

  Windows occur only in lukvle10 and chain. Box counts must belong to the certificate whose value is displayed.

**4.2 Exact affine splits: lnts and dtoc5 (1.5 pp).**

**Theorem 4.6 (lnts exact optimum).**
- *Notation.* For N ∈ {50, 100, 200, 400}:
  - w_0 = w_N = 1/2 and w_j = 1 otherwise;
  - c_0 = (2N−1)/4, c_j = N − j for 1 ≤ j < N, and c_N = 1/4;
  - r_j = c_j/w_j − N/2;
  - C(ν) = Σ_j w_j (1+ν²r_j²)^{−1/2} and D(ν) = ν Σ_j w_j r_j² (1+ν²r_j²)^{−1/2}.
- *Statement.* Let ν* be the unique positive root of g(ν) = D(ν) − (20/81) C(ν)². Then v*(lntsN) = N h* with h* = 9/(20 C(ν*)). The optimum is attained by θ*_j = arctan(ν* r_j), h = h* and the forward recursion.
- *Proof (main text, 0.8 pp):*
  - Lemma (exact elimination to three terminal equations; an equivalence for the OSIL model).
  - Proposition (Cauchy–Schwarz support bound S(μ, ν) with ν ≥ 0 and strict decrease in h).
  - Attainment at μ* = −ν*N/2 via the reflection identity r_{N−j} = −r_j.
  - The angle bound |arctan t| < π/2 < B, with 3·10⁻¹⁵ < B − π/2 < 4·10⁻¹⁵.
  - The enclosure via the intermediate value theorem and monotonicity of C.
- *Level:* P plus C, [E]. Two integer-only implementations, with rational enclosures of width below 10⁻⁶⁰.
- *Remarks:*
  - The stored Krawczyk points are strictly suboptimal (nonzero middle control); their enclosures only contain the optimum enclosure.
  - The listed Gurobi bound for lnts50 was already within 3.9·10⁻⁵ relative.
  - The zero-gap mechanism is classical (Mangasarian/Arrow-type sufficiency).

**Proposition 4.7 (dtoc5 dual identity).** Use the convention c_t = −(OSIL row t), λ_{T−1} = 0, λ_t < 1/4 and A_t = h(1−4λ_t). Then every exactly feasible point satisfies f = d(λ) + h Σ(u_t + λ_t/2)² + Σ A_t (y_t − ȳ_t)², with d(λ) in closed form. No state enclosure is needed. (Proof in the main text, 0.3 pp.)

**Theorem 4.8 (dtoc5 bracket).**
- *Statement.* With λ̂_t = −2û_t from the committed exact point and λ̂_{T−1} := 0, v* lies in [5.38967211918114046742396649913627186883131268, 5.38967211918114046742396649913627186883131341]. The certificate gap is ≤ 7.21·10⁻⁴³.
- *Corollary.* v* is attained, and every minimizer lies within 1.9·10⁻¹⁹ of the explicit values −λ̂_t/2 and ȳ_t(λ̂) in every u_t and in y_t for t ≤ T − 1.
- *Optional (D3):* uniqueness, by the critic's reduced-Hessian paragraph.
- *Level:* P plus C, [E]; [Fraction] arithmetic with GMP sums; 17 s. Two implementations: the dossier's (rounding the state-minimum terms up to 2⁻²⁵⁶) and the review's (full rational d).
- *Model notes.* The certificate concerns the MINLPLib dynamics y_{t+1} = y_t + 4h y_t² − h u_t (8·10⁻⁵ = 4h with h = 1/50000), not CUTEst's coefficient h. y_0 = 1 is fixed; all other variables are free.

**4.3 Richer split classes (2 pp).**

**optcdeg2.**
- *Why an affine split fails.* On the two u = −1/5 arcs the costate-affine stage residual is concave in v. The floating-point loss with refined costates is 0.6258; the certified affine bound is 293.2500703 with first-wave multipliers.
- *Quadratic calibration.* S_t = p^y_t y + p^v_t v + (q_t/2)(v − v̄_t)², with q_t = 0 on the middle arc and at both switches.
- *Lemmas (App. B.2):* B.2.1 (Krotov-type bound); B.2.2 (state enclosure); B.2.3 (exact stage minimization: y-elimination, then Sturm isolation of the quartic pieces; m_t ≥ min, with equality for the exact set).
- **Theorem 4.9.** v* ≥ B, where B is the rigorous rational evaluation 293.87607509587509237940… (display 293.87607509587509237); Δ ≤ 9·10⁻¹⁶. Computed in [E] in 16–18 s.
- *Certificate progression (in text):* affine 293.2500703 → affine plus monotone head block 293.8699938542 → IEEE intervals 293.8760750958728 → exact.
- *Facts to carry:*
  - Stage losses: 8.98·10⁻¹⁶ at stage 3091, 4.08·10⁻²⁰ at stage 47290, and ≤ 7.2·10⁻²⁵ elsewhere.
  - The diagnostic trajectory is a 2⁻³⁰⁰-rounded, near-feasible version, not exactly feasible.
  - GUROBI's listed dual 292.41713458 is valid; it equals the value of the tolerance-feasible p2 (violation 10⁻⁶).
- **Figure 2:** p^v_t, q_t and u_t against time, from the saved npz.

**chain (Theorem 4.10).**
- *Statement.* For N ∈ {50, 100, 200, 400}, v* ≥ L_N (displayed).
- *Proof idea.*
  - A discrete catenary calibration S_k(z, v) = G(v) − v z − k c in the lifted state (height, cumulative length weight) reduces the problem exactly to its two end values.
  - A 2-D interval B&B with per-box field parameters bounds the end values ([I] sqrt/log; 11,121–27,843 boxes).
  - A fixed-multiplier length Lagrangian fails, because the length row is effectively reverse-convex.
- *Lemmas (App. B.4):* polyline form, summation by parts, calibration inequality, end window.
- *Primal.* Exactly feasible points in Q(√R_N), characterized by Σω_i t_i = 12N and Σω_i/t_i = 4N; Δ ≤ 1.01·10⁻¹⁴.
- *Remark.* Proposition C6 (discrete Weierstrass), only for the strict chord condition and only as an explanation of tightness.

**catmix (Theorem 4.11).**
- *Statement.* v* ≥ L_N, with Δ ≤ 1.85·10⁻¹³ / 1.90·10⁻¹¹ / 6.81·10⁻¹¹ / 1.49·10⁻¹⁰.
- *Proof idea.*
  - Homogeneity reduces the 2-D state to a 1-D ray.
  - The true value functions are concave, positively homogeneous and superadditive, so chord minorants on about 14,080 rays per stage are valid (Lemma 4.2).
  - Lemmas M1–M6 are in App. B.4. Proposition M8 transports the bounds to c = 9a.
- *Arithmetic.* [F] (+ − × ÷ only).
- *Required wording.* "The strongest bounds come from one code. The authors' code certifies slightly weaker bounds end to end, and on identical inputs it agrees per stage within 9.44·10⁻¹⁵."
- *Remark.* The gap scales with the square of the grid spacing (data in App. B.4; no figure).

**4.4 Affine split plus window: lukvle10 (0.5 pp).**

**Theorem 4.12 (lukvle10).**
- *Statement.* 352.2380254050784 ≤ v* ≤ 352.2380254064957, so Δ ≤ 1.42·10⁻⁹.
- *Proof idea.*
  - 994 rows are dualized, giving 497 pair problems plus a 3-pair tail window parameterized by its 2-D entry pair.
  - Lemma B.1.x (coercive reduction to a box) needs q_k > −1; here q_k ∈ [−0.8156, 0], with q_0 = q_995 = 0. Stage values are infima ("inf ψ").
- *Arithmetic.* [I] exp/log; mpmath iv is part of the trust base (lead decision; no refinement).
- *Wording.* The dual value is known only to within 1.42·10⁻⁹. Global optimality of the KKT point is not proved.
- *Note.* The CUTEst SOLTN value 352.237 lies 1.0·10⁻³ below the certified bound. It is a tolerance artifact or belongs to another model version; its origin is inferred, not documented.

**4.5 Large bags: waterno2 (1.25 pp).**
- *Results (App. B.8):*
  - Fact (exact period structure: T periods, 3(T−1) tank-level copies, one horizon row).
  - Proposition (period Lagrangian).
  - Lemma (the horizon row is equivalent to a terminal-volume row; c_T = Σ d_t, checked exactly).
  - Proposition 4.5 applied (cells with 113–162 per link; 49,315 pair-box bounds; leaf-pair bounds by an exact linear correction, 556 also rebounded directly).
  - Lemma (reuse of a bound after a slope change).
  - Lemma B.8.5 (level ranges; complete row list in the appendix).
  - Lemma B.8.6 (B&B soundness).
- **Theorem 4.13.** v* ≥ 278.230573 / 824.834692 / 2089.754565 / 4790.820715 / 6576.151388 for _06/_09/_12/_18/_24. Exactly feasible points (exact algebraic arithmetic) give δ ≤ 1.68 / 10.82 / 6.90 / 4.87 / 5.90%.
- *Implementations.* rbb ([F], decimals enclosed outward) and vbb/vbb2 (exact rational node bounds); either alone yields every value. The polynomial rows of both builders equal an independent exact parse of the GAMS text.
- *Regeneration (lead decision; no rerun).* Rerunning `certify.py` regenerates SCIP-derived period targets. For _18 and _24 it certifies 4790.820086219 and 6576.150434342, which are slightly lower and also valid. The targets differ in periods 18 p1, 18 p7 and 24 p14. The reported values were certified at the stored targets by the original rbb run and by the vbb2 recheck. B&B trees are not stored (evidence level S).
- *Not claimed.*
  - The waterno2_06 primal is MINLPLib's p4 made exactly feasible, not our point.
  - Why the instances stay open is stated only as an interpretation: bags of 166 variables.

### §5 Other certificate classes (6 pp)

**5.1 Comparison along a chain: camshape (1.5 pp).**

**Theorem 5.1 (camshape exact optimum).**
- *Statement.* For n ∈ {100, 200, 400, 800}, the rational number v_n given by O(n) exact recurrences is the optimal value. It is attained only at the envelope point E, which is the componentwise greatest feasible radius vector.
- *Hypotheses.*
  - Part (a): C1, c₀ > 0, ū > 0, ℓ > 0.
  - Part (b): C2–C5 and an H-row coefficient ≤ 2; α ≥ 0 is implied.
- *Proof.* Sketch in the main text (0.75 pp); full proof in App. B.3.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Lemma 5.2 | Discrete Sturm comparison: the Green's function of the second-difference operator in u = 1/r is nonnegative because U_m(c/2) ≥ 0 (disconjugacy). | App. B.3 | P |
| Lemma 5.3 | Min-plus envelope for the slope rows; the envelope is feasible. | App. B.3 | P |

- *Computation.* Exact rational checks C1–C5, with no floating point. Three implementations agree to 30 digits.
- **Figure 3:** cam profiles for n = 100 and 800, with the comparison line R_j = 1/S_j, the cap 2 and the three phases (contact, maximal slope, r = 2).

**Proposition 5.4 (tolerance deficit bound).** Every point violating rows and bounds by at most ε has f ≥ v_n − D_n(ε), with D_n(ε) ≈ 0.6 n² ε for small ε.
- D_n is a proved upper bound, not the worst case. Explicit ε-feasible points reach 0.873 of it (BARON's camshape points reach 87%).
- Proof in App. B.3; a third implementation reproduces D_n.

**5.2 Lagrangians over a few dense rows (0.75 pp).** Instances of Lemma 4.1(d).

**Theorem 5.5 (ex6_2_5, ex6_2_7).**
- *Statement.* Dualizing the three mass balances leaves tangent-plane minimizations over the composition simplex. These are bounded by a 2-D interval B&B, giving Δ ≤ 2.1·10⁻¹⁵ and ≤ 4.9·10⁻¹⁴.
- *Lemmas.* Scaling identity, with r_p = 5·10⁻¹⁴ from the stored decimals; ideal phase via Gibbs' inequality.
- *Boxes.* Verifier: 131,111 (ex6_2_5 liquid; the vapour term is 0 by Lemma G2) and 42,111 (ex6_2_7).
- *Note.* λ·b is not itself a valid bound for either instance.
- *Optional (D3).* The tighter third-code values.

**Theorem 5.6 (pricing050, maximization).**
- *Statement.* A Lagrangian over 5 rows reduces to 50 certified 1-D minimizations. v* ≤ −1813.8290784519730577, with an exactly feasible point of objective ≥ −1813.8290784519731, so Δ ≤ 4.23·10⁻¹⁴ (conservative).
- *Note.* The Davarnia–van Hoeve value 1813.3 is a model/data discrepancy; instance identity is not proved.

**5.3 Global duality and convexity (1.5 pp).**

**powerflow (App. B.6).**

| No. | Statement | Level |
|---|---|---|
| Prop. 5.7 | Weak duality for the rectangular quadratic relaxation R with an eigenvalue shift ε, evaluated in exact rationals. The PSD proof is an exact LDLᵀ factorization (Bareiss). | P + C [E] |
| Theorem 5.8 | powerflow0030p: v* ≥ 576.8934122988004 at ε = 0; δ ≤ 2.1·10⁻⁹. | C [E] |
| Lemma 5.9 | Leaf identity at bus 30 (Lagrange's identity): W_NN = F(Pg, Qg, W_LL). | P |
| Lemma 5.10 | Vertex planes over a convex F; each plane passes through at least four box vertices. | P |
| Theorem 5.11 | powerflow0039p/r: branching on (Pg, Qg, W_LL) over 6 and 9 leaves gives 41869.05148485014 and 41869.05148327243; δ ≤ 6.4·10⁻¹⁰ and 6.7·10⁻¹⁰. | C [E] |

- With the angle-free 0039p variant, no trigonometric bound enters any dual proof.
- The 0039r balance rows are x64 − x263 and x156 − x273.
- Eigenvalues of A(w) stay exactly double (App. B.6).
- *Primal.* Krawczyk on an active-set square system.

**Theorem 5.12 (etamac).**
- *Facts.* The box comes from the model's own rows. With the stored exponents the CES aggregate has degree 1 + 4.14·10⁻¹⁶ and is not exactly concave.
- *Proof.* A concave majorant restores a convex relaxation; a KKT tangent plane then gives Δ ≤ 2.6·10⁻¹⁵ (exact value 2.5765·10⁻¹⁵).
- *Remark.* "The remaining gap is the price of κ" is an interpretation.

**Theorem 5.13 (pindyck).**
- *Statement.* ∇²J ⪯ −10⁻³ I on a polytope G ⊇ F, proved with 9 boxes in a 112-dimensional parameter box. Hence v* ≥ −1170.4862854360886163932 and Δ ≤ 5.44·10⁻¹⁴.
- *Corollary.* The optimizer is unique and lies within ‖·‖₂ distance 3.7·10⁻¹³ of p*.
- *Trust.* The displayed dual is the author's, relying on an A1-type padding analysis. The review's code relies on [F] (nextafter) and [I].
- *Note.* COCONUT's −1612.18 belongs to a mistranscribed model.

**5.4 An identity: hvycrash (0.3 pp).**

**Proposition 5.14 (hvycrash).** The rows force f ≡ −0.2185 on F(M), and F(M) ≠ ∅: an explicit backward construction r_k = √(−cos θ_k/D_k) with θ_k ∈ [2.6, 3] gives a feasible point. Hence v* = −0.2185.
- *Proof.* Main text (pen and paper, plus an [I] enclosure for the witness).
- *Credit.* The value −0.21850 is in the SIF file.
- *Note.* The listed solver dual −2.185·10⁸ never moves.

**5.5 Reduced-space branch and bound with strong enclosures (1.95 pp).**

**Theorem 5.15 (eg_int_s, eg_disc_s, eg_disc2_s).**
- *Statement.* L_I ≤ v* ≤ U_I with δ ≤ 1.0·10⁻⁹, and L_{eg_disc_s} = 5.760539610694993.
- *Algorithm:*
  - Lemma (minimax form);
  - Lemma (second-order Taylor model keeping the signed moments of the 97 kernel terms per row);
  - Lemma (per-box LP over the 24 minimax rows, checked by weak duality; the LP solver is untrusted);
  - domain reduction;
  - exact integer splits.
- *Independent leaf re-certifier (route R).* Exact rational final tests and an exact, tree-free coverage check. Leaves: 33,385 / 86,796 / 1,114,361.
- *Trust statement [pending].*
  - (H0), plus Lemma A1 written as a proof (App. F), including the `tau**3`, `p**3` and `p**4` paths.
  - Every exp and integer-power value used by route R is audited against rigorous enclosures by the separately written Cody–Waite auditor.
  - Route S-I is a second certificate for eg_int_s, eg_disc_s and eg_disc2_s part 1. Disclose that the S-I replay of part 1 ran before the dual-value guard existed.
  - *Fallback if the audit is incomplete:* state A2′ (exp relative error ≤ 9.9·10⁻¹⁴) and a pow hypothesis (≤ 10⁻¹²) as named assumptions.
- *Ablation.* Summing term ranges was 15–19 times looser at medium box sizes, and the wave-3 attempt failed. The per-box LP was essential near the optimum.
- **Figure 4:** (a) enclosure width against box size for the summed-range and Taylor-model enclosures; (b) cancellation bars for e12/e26 at the eg_int_s optimum.

**Theorem 5.16 (ann_cumene_tanh).**
- *Statement.* On the reduced space R over the 5 inputs (723 inequalities, including x772 ≥ 0.999), f ≥ L* = −7447080719734483·2⁻⁴¹.
- *Method.* Affine arithmetic with one noise symbol per tanh neuron, a rigorous per-box LP dual, and two bounding codes on one partition (Lemmas A.1–A.5 in App. B.9).
- *Primal.* An exactly feasible point gives δ ≤ 0.195%.
- *Scope.* The result applies verbatim to ann_cumene_exp.
- *Antecedents.* Schweidtmann–Mitsos 2019 (their reduced-space problem has 1 inequality) and Ninin–Messine–Hansen 2015.
- *Interpretation (labelled).* The remaining gap is consistent with a large, nearly flat valley on x772 = 0.999.

**KAN (App. B.9).**

**Proposition 5.17 (exact infeasibility).** For each model, on every admissible knot interval of one edge, the partition-of-unity rows have no common real solution. The certificates use Sturm counts and either nonzero pairwise resultants or a constant gcd of the residuals.
- *Worked-example box:* kan_r5_h1_n3, edge x776, interval b6, residual ρ₁ ≡ −2.8·10⁻¹⁷.

**Theorem 5.18 (KAN enclosure).** L ≤ min_R F ≤ min_{R_P} obj ≤ U, with U − L ≤ 2.42·10⁻⁸ (kan_r5_h1_n3) and ≤ 1.08·10⁻¹⁰ for the other five.
- U is the upper end of an enclosure (width ≤ 3.2·10⁻⁸⁹) of the objective at a point of R_P.
- *Trust.* The reported L is valid if either bound implementation is correct, given correct shared parsing, arithmetic and exp components (`kan_iv`/`ia`, whose constants were checked exactly).
- *Disclosure.* The r5 full searches were not rerun in the review. The rerun incumbents for r3_n4/n5 are different points with identical UB.

### §6 Exactly feasible points (2 pp)

**Constructions:**
- (A) explicit rational or quadratic-field points: dtoc5, chain, waterno2, camshape;
- (B) triangular definitions, forward or backward, generalized to non-affine identities on a proved domain: lukvle10, ann, KAN-R_P, catmix, hvycrash, etamac;
- (C) interval existence on a reduced or active-set square system, or a 1-D intermediate-value bracket: lnts, powerflow, optcdeg2, pindyck;
- (D) strictly interior points: pricing050, eg.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Theorem 6.1 | Krawczyk existence and uniqueness on a square subsystem with fixed coordinates. The remaining rows are checked on the proof box; nonsingularity follows from a width argument. | App. C (self-contained) | P |
| Prop. 6.2 | Points in Q or Q(√D) decide feasibility exactly; sqrt nodes are accepted by squaring the candidate root. | App. C | P |
| Prop. 6.3 | Triangular definitions. x_k := φ_k(x_{<k}) where r_k(x_{<k}, φ_k) = 0 is an identity on a domain the enclosures prove is entered. Each unknown appears only linearly (possibly multiplied by defined variables) with a provably nonzero total coefficient, or through a closed-form inverse. | App. C | P |
| Prop. 6.4 | No exactly feasible lnts point has all θ_j and h algebraic (Lindemann–Weierstrass), so an existence proof is needed. | App. C | P |

- Theorem 6.1 cites Krawczyk 1969 as the origin, Rump 2010 for the statement, and Kearfott 1998 for Hansen's fixed-coordinate square subsystem (the direct antecedent).
- **Remark (lukvle10).** Seed errors grow by about 2.73⁹⁹⁹. Seeds with 440 decimals suffice; the stored point uses 640. The point is rational but cannot usefully be printed.
- **Table 5 (the 13 formerly tolerance-only closures).** Columns: earlier violation; method; arithmetic; independent mpmath-free re-proof; enclosure width.
- **Trust paragraph:**
  - mpmath is not needed for the primal claims of these 13, waterno2, ANN, KAN, eg or ex6_2_*.
  - The mpmath-iv-only primal claims are hvycrash, etamac, pricing050 and pindyck; etamac and pricing050 have one implementation.
  - optcdeg2 has an integer-interval proof in addition to the mpmath one.
  - Four reviews verified the 13 points; a fifth verified the water, ANN and KAN points.

### §7 An audit of MINLPLib's listed dual bounds (3.5 pp)

**7.1 Population and screen.**
- 1,633 pages; 2,816 points; 11,086 per-solver bounds (11,031 finite) under 19 solver labels.
- The screen found 158 (bound, point) pairs on 46 instances (56 points), and 3,851 display ties on 1,133 instances that the screen cannot decide.
- The OSIL files of the 69 relevant instances are byte-identical to the live files.

**7.2 Refutation under explicit display hypotheses.**

| No. | Statement | Proof | Level |
|---|---|---|---|
| Hyp. H | The displayed string s and the solver's number b satisfy |b − d(s)| < u(s). | — | — |
| Lemma 7.1 | H holds if the page derives s from b by one rounding or truncation, or by page rounding to 10 significant digits and then 8 decimals, provided d(s) has at most 10 significant digits (true for |d| < 2²⁶). The fac1 string 160912612.40000001 shows why this restriction is needed. | App. E | P |
| Prop. 7.2 | If an exactly feasible point has objective f ≤ d(s) − u(s) (minimization), then no number displayed as s is a valid bound (class (i)). Class (i-r) refutes only the displayed number taken literally. | App. E | P |
| Cor. 7.3 | Refutations hold for every feasibility tolerance and for the GAMS form where the forms are exactly identical. Binary64 data rounding is not covered. | App. E | P |

**7.3 Existence certificates.**
- Route A: the listed point is exactly feasible.
- Route B: Krawczyk on a square subsystem (Theorem 6.1).
- Route C: shift and repair.
- Dedicated exact certificates.
- Every class (i) pair was re-proved by a second implementation.

**7.4 Results.**
- **Table 6 (the 19 class (i) pairs, compact; full version in App. E).** Columns:
  - instance; solver; date;
  - displayed d;
  - proven objective f (upper end);
  - d − f (at least) and relative margin;
  - margin in display units (every margin exceeds 1.11 units);
  - route;
  - second implementation.
- **Size labels:**
  - Four margins exceed 1% of |d|: glider100 (COUENNE, LINDO), topopt-cantilever_60x40_50 (LINDO) and methanol50 (LINDO).
  - Seven lie between 1.2·10⁻⁵ and 7.3·10⁻⁵ of |d|, below common 10⁻⁴ gap tolerances.
  - Eight are tolerance-scale (1.9·10⁻⁹ to 3.3·10⁻⁷ of |d|) on six instances: nd_netgen-2000-3-4-b-a-ns_7, watercontamination0303 and four smallinvDAX instances. All instances whose solved mark rests on an invalid bound are in this group, and the mark is not contradicted under MINLPLib's 10⁻⁶ rule.
- **Figure 5 (margin scatter).** x: margin in display units (log); y: (d − f)/|d| (log); reference lines at 1 unit and at 10⁻⁶ and 10⁻⁴; colour by solver.
- **glider100 remark.** The proven objective is about 784 times the listed bound. The exactly feasible point is a spurious period-2 solution of the discretized model, which is valid for the model as stored.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Prop. 7.4 | spring: the global optimum is 0.846245665643154281…, proved by enumeration; the five displayed bounds 0.84624567 are its 8-decimal rounding. | App. E | C [E] |
| Prop. 7.5 | emfl050_3_3/050_5_5/100_3_3/100_5_5: SOCP weak duality and Krawczyk give two-sided enclosures within 3.4·10⁻¹¹. Every listed dual is valid, while the best listed primal values lie below the optimum (S-marked emfl050_3_3: by at least 1.41·10⁻⁵ absolute, 1.36·10⁻⁶ relative). | App. E | C |

- **Class (i-r):** 12 pairs on 4 instances. Page rounding explains the five spring conflicts (proved). Earlier rounding to six significant digits could explain eniplac, lop97icx and stockcycle (evidence, not proof).
- **rocket100/200/400 (outside the screen).** LINDO bounds invalid by at least 1.06·10⁻⁷, 4.7·10⁻⁸ and 1.89·10⁻⁷; two implementations.
- **Model history.** Models are unchanged except three rounded ghg_3veh constants; the refutation also holds on the old text. No archived copy covers March–December 2014 for nine instances.

**7.5 What the audit does not show.**
- Display ties and classes (ii)/(iii) are undecided.
- No cause or solver bug is attributed.
- The aggregate (listing) dual is not invalidated beyond display rounding on the class (i) instances, but for eniplac and stockcycle it exceeds proven objectives by 0.083 and 0.31. Only unproved six-digit pre-storage rounding explains this.
- No S mark is contradicted.

### §8 Solver and published claims under exact feasibility (3 pp)

**8.1 Tolerance artifacts (category A).**

| No. | Statement | Proof | Level |
|---|---|---|---|
| Prop. 8.1 | BARON 26.5.27 on camshape100/200: the duals are valid and within 1.23·10⁻⁷ and 4.80·10⁻⁷ relative of the optima (reached in 0.45 s and 23 s). The returned values lie 5.26·10⁻⁷ and 2.05·10⁻⁶ below the optima, and the returned points violate rows by about 10⁻¹⁰. | App. H | C |
| Prop. 8.2 | QPLIB copies. No exactly feasible point of QPLIB_3177 attains MINOTAUR's −4.2774, and none of QPLIB_2738 attains ANTIGONE's −4.284302, nor any value within one unit of the last displayed digit (margins ≥ 3.11·10⁻³ and ≥ 1.54·10⁻⁴; round 1, G4-03). Reaching these values needs violations above 8·10⁻⁹ and 2.5·10⁻⁸; explicit points reach them with 9.7·10⁻⁹ and 2.9·10⁻⁸. MINOTAUR's implied dual is consistent with the optimum. QPLIB's own QPLIB_2738 point lies 5.8·10⁻¹⁴ below the bound. Assumes .nl = .gms (MINOTAUR). | App. B.3, H | C [E] |
| Prop. 8.3 | Published SCIP 9.0.1 optima for kan_r3_h1_n4/n5 lie at least 1.70·10⁻³ and 2.03·10⁻³ below min R. As duals of the exactly infeasible OSIL model, SCIP's values are trivially valid. | App. B.9 | C |

- **Table 7 (contradicted claims).** Columns: source; model; value; distance to the certified bound or exact value; violation; category; proof type; qualifier. Rows, by source:
  - **MINLPLib listed points:**
    - lnts50 p1 (≥ 4.24·10⁻¹¹ below the optimum; violation 9.1·10⁻¹⁰);
    - camshape400/800 p2 (about 8.2·10⁻⁶ and 3.3·10⁻⁵ below, printed rounded down from the logs; violation 3.0·10⁻¹⁰, hundreds of rows at about 10⁻¹⁰);
    - camshape200/400 p1;
    - hvycrash p1/p2 (−0.21413, above the constant −0.2185);
    - etamac p1 and pricing050 p1;
    - the emfl best listed primals.
  - **Our campaign:** BARON camshape100/200; SCIP camshape100 (1.5·10⁻⁷ below; violation 7.7·10⁻¹⁰); the further campaign points by a stated rule (all solver optimality claims and incumbents beyond printing scale, from `inconsistencies.md`).
  - **Published claims:**
    - optcdeg2: GUROBI's listed dual equals the value of p2 (violation 10⁻⁶), 1.459 below the optimum; the bound is valid;
    - the lukvle10 SOLTN value;
    - the KAN SCIP 9.0.1 optima and the kan_r5_h1_n5 ConvexHull primal (0.2725188);
    - Kosolap's ex6_2_5 value (−70.9586);
    - LANCELOT's COPS values for camshape and chain400;
    - CAMINO's S-B-MIQP value for eg_disc2_s;
    - the old GAMS World eg point;
    - MINOTAUR (QPLIB_3177) and ANTIGONE (QPLIB_2738).
  - **Upward direction:** the optcdeg2 floating-point author point lies 6·10⁻¹² above the rigorous upper bound.
- **Figure 6.** Objective deficit against maximal violation for camshape points (campaign, MINLPLib p2, QPLIB references), with the proved curves D_n(ε) for n = 100…800 and Lemma 2.5 reference lines.

**8.2 Invalid recorded claims (category B).**

**Box: the SCIP defect.**

| No. | Statement | Proof | Level |
|---|---|---|---|
| Prop. 8.4 | Eight exactly feasible rational witnesses (waterno2_06 periods 0, 4 and 5; one cell-pair subproblem; four derived small models) refute SCIP's "optimal" values: by up to 3.8 on the periods and 9.4 on the pair. SCIP's own `checkSol` accepts every witness, whose binary64 residuals are ≤ 2.9·10⁻¹⁵. Six to eight independent exact checkers confirm each witness. | App. H | C [E] |
| Prop. 8.5 | Exact optima of the reproducers: fm336 = 187/270 and tiny2 = −1.337 (by hand). fm336's SCIP claims are wrong under every data reading, including binary64 data with zero tolerance. | App. H | P |
| Lemma 8.6 | The tightest outward enclosure of fl(0.7)³ lies entirely below fl(0.343). SCIP's traced activity matches at the upper end; its lower end is one ulp looser. Only the upper end matters. | App. H | C [E] |
| Obs. 8.7 | In the instrumented runs, reverse propagation in the default nonlinear handler intersects the activity with the bounds using `SCIPintervalIntersect`, not the ε-version; the empty intersection declares the node infeasible. The syntactic trigger appears only in waterno2 models, and only the 0.7-station cube row (one per period) can fire. `varboundrelax = b` removed the wrong runs (0 of 122, against 78 of 122). | App. H | evidence |

- *Wording.* The error is seed- and version-dependent (version × seed table in App. H). The higher cell-pair claims are refuted; the low claims near 55.6898 are not. The untraced seed-11 run (0.85 station) is not linked to the mechanism. No listed MINLPLib SCIP bound is claimed wrong.

| No. | Statement | Proof | Level |
|---|---|---|---|
| Prop. 8.8 | CAMINO's best recorded Gurobi 13.0.0 bounds exceed the objectives of exactly feasible points by at least 4.3% (eg_disc2_s), 7.4% (eg_disc_s) and 80% (eg_int_s). The CSV has no status column; the pipeline kept only runs that AMPL labelled "solved" or "limit". The cause is unknown. | App. B.7 | C |
| Prop. 8.9 | MINOTAUR 0.4.1's infeasibility report on QPLIB_8803 is false, assuming its .nl file encodes the MINLPLib optcdeg2 model. The report occurs in the first presolve, before default bounds are added. | App. B.2 | C |

**8.3 One-hour comparison.**
- **Setup:**
  - GAMS 54.3.1, one thread, 3600 s, requested absolute and relative gaps 10⁻⁹, 8192 MiB memory;
  - BARON's limit is CPU time; GUROBI and SCIP use wall time;
  - unmodified GAMS files.
- **Table 8 (per solver).** Columns: passing measurements; finite final duals (BARON 35, 6 without a globality guarantee; GUROBI 36; SCIP 38); returned primals; raw optimality claims (2/0/0); accepted closures (0/0/0); capability failures (8/0/1); other failures (0/1/0); memory stops (0/0/3).
- **Caveats:**
  - ten runs in an overloaded first batch (dtoc5, optcdeg2 and waterno2_24 for each solver, plus kan_r3_h1_n9 with BARON);
  - three SCIP memory stops (ex6_2_5, ex6_2_7, pindyck);
  - six BARON values without a globality guarantee (catmix ×4, dtoc5, optcdeg2);
  - six SCIP values on log/pow argument bounds tightened to 10⁻⁹;
  - 18 KAN comparisons against R.
  - Only five final duals improve the best listed dual (BARON camshape100/200/400, GUROBI lnts200, SCIP waterno2_18).
  - No ranking and no speed claim.

### §9 Why these instances stayed open: an interpretation (2.5 pp)

State at the start that this section is an interpretation and was not tested by experiment.

**Table 9 (structure → certificate).** Columns:
- structural feature;
- instances;
- what a termwise relaxation sees;
- what the certificate used;
- branching dimension;
- arithmetic.

Rows:

| class | feature | instances | certificate |
|---|---|---|---|
| A, 15 | long chains of nonconvex equalities with free states | lnts, dtoc5, optcdeg2, lukvle10, chain, catmix | staged split |
| A′, 4 | chain with a monotone comparison after u = 1/r | camshape | comparison |
| B, 3 | a few dense coupling rows | ex6_2_5, ex6_2_7, pricing050 | Lagrangian over those rows |
| C, 5 | hidden convexity or concavity; tight quadratic/SDP structure | etamac, pindyck, powerflow ×3 | convex relaxation, tangent plane or SDP dual |
| D, 1 | an identity | hvycrash | short proof and witness |
| E, 3 | cancellation among many terms | eg_* | Taylor models plus per-box LP |

Branching profile:
- none: 12 (lnts ×4, dtoc5, camshape ×4, hvycrash, powerflow0030p, etamac);
- 1-D: 6 (optcdeg2, catmix ×4, pricing050);
- 2-D: 7 (lukvle10, chain ×4, ex6_2_5, ex6_2_7);
- 3-D: 2 (powerflow0039p/r);
- pindyck: 9 boxes in a 112-dimensional parameter box;
- eg: the full 7-variable space, up to 1.1·10⁶ leaves.

**Evidence.**
- For 14 of the 15 staged closures, no one-hour solver dual with a globality guarantee reached the listed dual. The exception is lnts200, at +2.8% of the listed gap.
- chain: solver duals from −36 to −1673, against a certified 5.07.
- catmix: no finite dual with a globality guarantee.
- hvycrash: the SCIP dual stays at −2.185·10⁸ over 504,455 nodes.
- powerflow0030p: the SCIP dual is 0 after 23,036 nodes.

**Counter-evidence (state explicitly).**
- On camshape100, SCIP's dual improves steadily over 1,179,749 nodes but stops 5.7% short.
- BARON's camshape iteration counts are not clean evidence of relaxation strength, because BARON pruned against incumbents below the exact optimum.
- eg and ex6_2_5 needed many boxes.
- ex6_2_*, pricing050 and eg have no free variables.
- On powerflow0039, SCIP and GUROBI rank the polar and rectangular formulations in opposite orders. The two optima are not proved equal.

**Fixed wording.** "In every closed case the decisive ingredient was a bounding argument fitted to the model's structure. Afterwards, branching was absent in 12 closures, at most three-dimensional in 15 more, and confined to the original variables in the rest. In our reading, termwise relaxations were held back by free variables, long chains of nonconvex equalities, hidden convexity or monotonicity, and cancellation among many terms."

**9.x Optional theory (decision D1; 1 pp if adopted).** Default layout, as recommended by the pattern critique:

| No. | Statement | Proof | Level |
|---|---|---|---|
| Theorem 9.1 | Band identity: when both sides of separator τ are minimized exactly, the least loss over a split class Φ at τ equals 2·dist(Φ, Band_τ). | App. G.5 | P |
| Prop. 9.2 | Constant cells: for a 1-D separator with exact stage minima, slope λ and band curvature M near a pinch point, a gap ≤ ε needs at least |λ|/√(2Mε) cells. Hence the working staged certificates used slopes. | App. G.5 | P |

- **Figure 7 (band schematic):** a 1-D separator with V_τ above, v* − Γ_τ below, the pinch at s*, an affine element tangent at s*, and a constant-cell staircase.
- **App. G.6:** path sandwich theorem; counterexample to per-separator diagnostics; pinch regularity with Γ_τ and V_τ semiconcave.
- **Limits.** The theory predicts no closure and gives no certificate size for these instances.
- **Requirements.** The extended-value proofs need the 2–4 reviewer-hour confirmation, and four antecedents must be added to the KB and read first (§7).
- **If D1 is "no":** drop 9.x and Figure 7; keep Lemma 4.1–Proposition 4.5, which validity needs. The unpublished note cannot be cited, so the results are omitted.

### §10 Reproducibility and computational effort (1.5 pp)

- **Archive content:**
  - models with hashes;
  - certificate data (multipliers, calibration arrays, leaf boxes, coverage records, PSD factors);
  - exact point definitions;
  - author checkers and independent re-implementations;
  - logs;
  - the claim register `claims.json` (App. I), keyed to `result-map.json` and `gap-values.json`.

  Copyrighted sources are not redistributed; their hashes are.
- **Replay tiers.** Wall times are recorded on a shared machine and support no speed claims.
  - **Tier 1 (minutes; under one CPU-hour in total).** lnts, dtoc5, camshape, optcdeg2, hvycrash, pricing050, etamac, pindyck, chain, powerflow0030p, the KAN infeasibility certificates, all exact primal checks, and the audit's class (i) existence proofs.
  - **Tier 2 (under one hour each).** ex6_2_*, lukvle10, powerflow0039p/r, KAN r3 and r5 bounds, the eg parts, and waterno2_06 cell slopes from the stored pair bounds.
  - **Tier 3 (hours to tens of CPU-hours).** catmix (≈ 2.9 h total), waterno2 period certificates, the ann extension, and eg all-leaf route R **[timing pending]**.
- **Replay versus regeneration:**
  - waterno2_18/24 (4.5);
  - document a fixed-target replay at the stored targets (vbb2), as the waterno2 critique requires (packaging only);
  - the topopt p5 regeneration selects a different valid point;
  - the waterno2 trees are not stored (evidence level S).
- **Disposable-copy rule.** Several scripts write logs or certificates when imported or run.
- **Environment.**
  - Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0 (HiGHS), mpmath 1.3.0, SymPy 1.14.0;
  - solver versions;
  - original per-run CPU times and BLAS/libm dispatch are only partly recoverable.

### §11 Implications, limitations and conclusion (2 pp)

**11.1 Recommendations** (from P3; each tied to its evidence; proposals, not novelty claims).
- **For benchmark libraries:**
  - state the data semantics (decimal or binary64) and the feasibility measure (evidence: KAN, camshape p2, lnts50 p1);
  - mark listed points as exactly verified or tolerance-only, and store exactly feasible reference points where known;
  - record provenance with each per-solver bound (version, options, tolerances, termination status), with directed rounding and enough digits (evidence: (i-r) on eniplac and stockcycle);
  - keep the three-solver aggregate. It protected the aggregates in this audit, except where six-digit storage is suspected. Flag per-solver entries that a listed point contradicts, and run the screen at each update;
  - accept certificate-backed bounds with a checker as a status separate from S;
  - flag ill-conditioned instances (Lemma 2.5, D_n(ε)) and exactly infeasible models (KAN);
  - check the identity of model copies and sources (QPLIB rounded copies; CUTEst coefficient factors of 4; MATPOWER shunts and taps).

  Precedents: MIPLIB checkers, VIPR, PAVER.
- **For solver developers:**
  - make propagation on equality rows robust to binary64 residuals in decimal bounds (SCIP; varboundrelax evidence);
  - report the maximal violation of returned points, and distinguish "optimal within tolerance" from certified;
  - exploit stage structure (multipliers from a local solve, stage-wise exactness tests by Prop. 4.3(b), derived enclosures for free states);
  - use enclosures that keep cancellation for sums of many similar terms.
- **For benchmark users:**
  - report versions, settings, termination status and violations;
  - do not count an "optimal" status as a closure without exact verification;
  - treat a single listed dual as unverified.

**11.2 Limitations.**
- **Trust base:** code correctness, mpmath iv where used, IEEE binary64, OSIL reading, and the common-mode risk of AI-generated code and reviews.
- **Readings:** reading (b) versus (c).
- **Per-instance work:** the certificates were built by hand per instance; no general solver capability was implemented.
- **Selection:** selection followed tractability.
- **Unread sources:** McDonald–Floudas 1997 (GLOPEQ), Floudas handbook 1999, Huang 2011, the 2022 waterno2_04 paper, Ghaddar et al. 2015, Arrow–Kurz, Murtagh–Saunders Example 5.11.
- **Snapshot:** all claims refer to one snapshot.
- **Verification:** nothing is formally verified.

**11.3 Open problems and conclusion.**
- Open problems:
  - closing waterno2 and ann_cumene_tanh;
  - KAN models with consistent partition rows;
  - the ex6_2_* priority question;
  - proof-assistant checks of short certificates (camshape, dtoc5, hvycrash);
  - the 126 instances open by the scout rule that are not closed here.
- Restate the three lessons; give the archive DOI.

**Statements and declarations:**
- data and code availability (DOI; licence, decision D8; third-party notices for MINLPLib/QPLIB CC BY 4.0, CUTEst/SIF BSD or MIT, MATPOWER case-data terms; MATPOWER and QPLIB citation requests);
- AI-use disclosure and responsibility statement (D7);
- competing interests.

**Page total:** 4.5 + 4 + 3 + 7 + 6 + 2 + 3.5 + 3 + 2.5 + 1.5 + 2 = **39 pp** plus references. If over 40, trim §5.3 and §9 first.

**Main-text figures:**
1. headline gaps (§3);
2. optcdeg2 calibration (§4);
3. camshape profiles (§5);
4. eg enclosures (§5);
5. audit margins (§7);
6. tolerance deficits (§8);
7. band schematic (only if D1).

**Main-text tables:**
1. trust base;
2. 31 closures;
3. other 12 instances;
4. staged certificates;
5. 13 formerly tolerance-only points;
6. audit pairs;
7. contradicted claims;
8. campaign summary;
9. structure → certificate.

Every numeric cell is generated from `gap-values.json`, `result-map.json` or the campaign CSV, never typed by hand.

---

## 6. Appendix plan and supplement (≈ 64 pp)

- **A. Model semantics and OSIL reading (2 pp).**
  - Defaults and the domain rule; the three readings.
  - GAMS/OSIL identity evidence per family; per-instance SHA-256 values.
  - Provenance facts:
    - dtoc5/optcdeg2 differ from CUTEst by a factor of 4 in one coefficient;
    - dtoc5 equals QPLIB_8585 apart from comments and the solve statement;
    - powerflow0030p drops two case30 shunts; 0039p/r drop the transformer taps;
    - catmix's OSIL c differs from GAMS c;
    - pindyck has 116 variables, 4 of them fixed initial states;
    - hvycrash is CUTE N = 50.
- **B. Certificates by family (≈ 30 pp).** Model, listed status, theorem with full proof, computation, numbers, and verification matrix (implementations, readers, verdicts, review dates).
  - B.1 lnts and lukvle10.
  - B.2 dtoc5 and optcdeg2 (state enclosure, exact stage minimization, certificate progression, MINOTAUR presolve note).
  - B.3 camshape (Theorem 5.1 proof, D_n(ε), QPLIB copy bounds by a separate route).
  - B.4 chain and catmix (M1–M6, M8; grid designs; Proposition C6 with the strict-chord restriction).
  - B.5 the six small instances.
  - B.6 powerflow (relaxation R, double eigenvalue, leaf data and partitions, angle-free variant).
  - B.7 eg (minimax form, Taylor-model and LP lemmas, routes and coverage matrix, run statistics, margins, CAMINO evaluation).
  - B.8 waterno2 (Lemmas B.8.5–B.8.6 with complete row lists, verification counts, regeneration note).
  - B.9 ann and KAN (Lemmas A.1–A.5, K.3, edge table, rerun table, R and R_P definitions).
- **C. Exactly feasible points (5 pp).** Theorem 6.1 with full proof; Propositions 6.2–6.4; per-instance construction, enclosure, trust and second implementation; a 43-row primal table.
- **D. Prior literature by instance (4 pp).**
  - 43 rows condensed from L2 and corrected by the critiques: model relation, evidence status, novelty wording (e.g., camshape200 credit; MINOTAUR's camshape800 value "not attainable").
  - Search scope and date.
  - The unread-source list.
  - The funnel figure.
- **E. Audit details (6 pp).**
  - The full 19-pair table with both implementations; the (i-r), emfl, spring and rocket tables.
  - Lemma 7.1 and Propositions 7.2–7.5 with proofs; Krawczyk floating-point error terms.
  - Model-history evidence; screen and class counts; pipeline figure; aggregation rule.
- **F. eg rounding-error analysis (3 pp).** Lemma A1 written as a proof (including the padding roundings and the pow paths); the auditor's design and results **[pending]**; Lemma S only if route S-F is mentioned.
- **G. Proofs for §4 (3 pp; +2 pp if D1).** Extended-value proofs of Lemma 4.1, Lemma 4.2, Propositions 4.3–4.5 (Remark with finite potentials); if D1, Theorem 9.1, Proposition 9.2, path sandwich, counterexample, pinch regularity (Γ_τ semiconcave).
- **H. Solver campaign and SCIP defect (5 pp).** The 129-row table (condensed); measurement rule; failure classes; the SCIP version × seed table; fm336 under three readings; the three binary64 propagation steps of tiny2; the varboundrelax experiment; trigger scan (`pattern_scan.py`).
- **I. Reproduction guide and claim register (3 pp).** Commands by tier; expected outputs; environment; replay versus regeneration. Claim register: claim → theorem → artifact paths and SHA-256 → checker command → expected output → wall time → verification label → trust tags (machine-readable copy in the archive).
- **J. Display record (1 p).** Safe displays used in the paper, and known unsafe strings (§8, item 11).
- **Supplement (archive with DOI).** Code, certificate data, points, logs, hashes, manifest, review reports and their evidence (including `/tmp/sol-kan-review/` once archived), `claims.json`.

---

## 7. Bibliography plan (KB slugs; all checked to exist)

**§1.1 and §1.4 (libraries, checks, positioning)**
- **MINLPLib:**
  - `bussieck2003-minlpliba-collection-of-test-models`;
  - Vigerske 2014, "MINLPLib 2", MAGO proceedings, printed pp. 137–140. The PDF is stored under `haugland2014-the-hardness-of-the-pooling`; cite Vigerske's own pages, not the Haugland package;
  - `vigerske2014-towards-minlplib-2-0` (quote verbatim, with [sic] for "a solvers dual bound claim");
  - `vigerske2026-minlplib-documentation-database-snapshot-2026` (S mark, violation measure);
  - `vigerske2026-minlplib-a-library-of-mixed` (FAQ sentence).
- **Other libraries and checks:**
  - `koch2011-miplib-2010-mixed-integer-programming`, `gleixner2021-miplib-2017-data-driven-compilation`, `bussieck2014-paver-2-0-an-open`;
  - `dolan2001-benchmarking-optimization-software-with-cops`, `dolan2004-benchmarking-optimization-software-with-cops-2`;
  - `bongartz1995-cute-constrained-and-unconstrained-testing`, `gould2003-cuter-and-sifdec-a-constrained`, `gould2015-cutest-a-constrained-and-unconstrained`;
  - `furini2018-qplib-a-library-of-quadratic`, `furini2026-qplib-official-solution-point-records`;
  - `shcherbina2003-benchmarking-global-optimization-and-constraint`.
- **Closest precedent:** `halbig2024-computing-optimality-certificates-for-convex`.
- **Rigorous global optimization:**
  - `neumaier2004-complete-search-in-continuous-global`;
  - `kearfott2003-globsol-history-composition-and-advice`, `kearfott2011-interval-computations-rigour-and-non`;
  - `domes2009-gloptlab-a-configurable-framework-for`;
  - `vanaret2014-certified-global-minima-for-a`;
  - `kuznetsov2024-convexification-and-global-optimization-of`.
- **Prior closures:**
  - `go2026-parabolic-approximation-relaxation-for-minlp` with `go2026-publisher-correction-parabolic-approximation-relaxation` (Table 17 rows unchanged);
  - `go2026-clash-of-minlp-relaxations-piecewise` (PARA, p. 32);
  - `bestuzheva2025-global-optimization-of-mixed-integer` (Octeract camshape100);
  - `ghezzi2026-camino-benchmark-results-for-nonconvex`, `cristofari2026-an-augmented-lagrangian-based-method`.
- **Solver reliability:**
  - `neumaier2005-a-comparison-of-complete-global`;
  - `nowak2008-lago-a-heuristic-branch-and` (wrong BARON root bound on bayes2_10);
  - `vigerske2017-scip-global-optimization-of-mixed`;
  - `montanher2018-a-computational-study-of-global`;
  - `bonami2018-designing-and-implementing-algorithms-for`;
  - `bertsimas2025-towards-a-practical-global-optimization` (GOpt labels are not certificates).

**§2 (semantics and exact arithmetic)**
- `cook2011-an-exact-rational-mixed-integer`, `eifler2023-a-computational-status-update-for`, `hoen2025-analyzing-the-numerical-correctness-of` (rational input data);
- `applegate2007-exact-solutions-to-linear-programming`, `cook2013-a-hybrid-branch-and-bound`, `cheung2017-verifying-integer-programming-results`;
- `neumaier2004-safe-bounds-in-linear-and`, `jansson2007-rigorous-error-bounds-for-the`.

**§4 (split certificates)**
- `krotov1967-sufficient-conditions-for-the-optimality`, `mangasarian1966-sufficient-conditions-for-the-optimal`;
- `geoffrion1972-generalized-benders-decomposition`, `karuppiah2008-a-lagrangean-based-branch-and`;
- `khajavirad2009-a-deterministic-lagrangian-based-global` (a model for framing "known pieces, new bounds");
- `cao2019-a-scalable-global-optimization-algorithm`;
- `lincoln2006-relaxing-dynamic-programming` (Lincoln–Rantzer; not the Rantzer solo slugs);
- `bienstock2018-lp-formulations-for-polynomial-optimization`;
- `zhang2022-stochastic-dual-dynamic-programming-for`, `fullner2022-non-convex-nested-benders-decomposition`, `yang2025-globally-converging-algorithm-for-multistage` (decomposition precedents).
- **Control sources:**
  - `waki2006-sums-of-squares-and-semidefinite` (preprint B-411 pages; caveats: floating-point SeDuMi, objective perturbation, h-variant);
  - `luksan2026-cutest-source-forms-for-dtoc5`, `coleman1993-the-global-convergence-of-a`, `luksan1999-test-problems-for-unconstrained-optimization`.
- **chain:** `denzler1999-catenaria-verathe-true-catenary`, `griva2005-case-studies-in-optimization-catenary`, `gabrys2025-a-convex-optimization-approach-to`, `library2026-cops-and-gams-source-models`.
- **waterno2:**
  - `tasseff2022-polyhedral-relaxations-for-optimal-pump`, `huang2019-optimal-operation-of-water-supply`;
  - `huang2011-operative-planning-of-water-supply` (catalog record only; Diplom thesis);
  - `gleixner2012-towards-globally-optimal-operation-of`, `ambrosio2015-mathematical-programming-techniques-in-water`;
  - `ghaddar2015-a-lagrangian-decomposition-approach-for` (metadata only; named as unread; no priority statement);
  - `matpower2026-minlplib-power-flow-and-water`.

**§5**
- **camshape:** `bohner1996-linear-hamiltonian-difference-systems-disconjugacy` (`hartman1978-difference-equations-disconjugacy-principal-solutions` is unread: title only), `cache2026-qplib-pages-and-rounded-camshape`, `mittelmann2026-continuous-non-convex-qplib-benchmark`, `mattick2023-reinforcement-learning-for-node-selection`, `smith2011-smith-thesis-coconut-table-a`.
- **ex6_2_*:** `tessier2000-reliable-phase-stability-analysis-for`, `mcdonald1995-global-optimization-for-the-phase-2` (NRTL), `mcdonald1997-glopeq-a-new-computational-tool` (metadata only; "unconfirmed"), `ninin2010-optimisation-globale-basee-sur-l`, `trombettoni2011-inner-regions-and-interval-linearizations`, `najman2021-linearization-of-mccormick-relaxations-and`, `kosolap2019-global-optimization-of-the-general`, `cuesta2025-global-optimization-of-mixed-integer` (arXiv v3).
- **pricing050, etamac, pindyck:** `davarnia2021-strong-relaxations-for-continuous-nonlinear` (likely source; identity not proved), `xia2020-a-survey-of-hidden-convex`, `coconut2026-globallib-gams-coconut-and-minlplib`, `tawarmalani2005-a-polyhedral-branch-and-cut`, `gleixner2017-three-enhancements-for-optimization-based`.
- **powerflow:**
  - `lavaei2012-zero-duality-gap-in-optimal`, `molzahn2019-a-survey-of-relaxations-and`, `josz2015-certified-moment-relaxation-for-ac`, `ghaddar2016-optimal-power-flow-as-a`;
  - `jansson2006-vsdp-verified-semidefinite-programming`, `peyrl2008-computing-sum-of-squares-decompositions`, `oustry2022-certified-and-accurate-sdp-bounds`;
  - `chen2016-a-spatial-branch-and-cut` (bounds on W_ii, W_jj and the phase ratio, not box bounds; no "affine image" sentence);
  - `coffrin2014-nesta-network-enabled-scalable-tools`, `bingane2019-tight-and-cheap-conic-relaxations`, `gopalakrishnan2012-global-optimization-of-optimal-power`.
- **hvycrash:** `toint2013-cute-hvycrash-source-sif-files`.
- **eg, ANN, KAN:**
  - `neumaier2003-taylor-formsuse-and-limits`, `berz2009-rigorous-global-search-using-taylor`, `figueiredo1997-fast-interval-branch-and-bound`;
  - `ninin2015-a-reliable-affine-relaxation-method` (direct antecedent of the per-box LP with safe duals);
  - `stolfi2003-an-introduction-to-affine-arithmetic`, `messine2002-extensions-of-affine-arithmetic-application`;
  - `schweidtmann2019-deterministic-global-optimization-with-artificial`, `schweidtmann2021-global-optimization-of-processes-through`, `anderson2018-strong-mixed-integer-programming-formulations`, `gonzalez2026-nonconvex-robust-optimization-for-process`;
  - `liu2024-kan-kolmogorov-arnold-networks`, `karia2025-deterministic-global-optimization-over-trained`, `karia2025-karia-et-al-zenodo-default`.

**§6:** `krawczyk1969-newton-algorithmen-zur-bestimmung-von` (metadata only; cite as origin), `rump2010-verification-methods-rigorous-results-using` (statement), `kearfott1998-on-proving-existence-of-feasible` (fixed-coordinate square subsystem), `fullner2021-convergent-upper-bounds-in-global`, `fullner2024-feasibility-verification-and-upper-bound`.

**§7–§8:**
- Vigerske 2014 (both sources); `nowak2008-lago-a-heuristic-branch-and`; `vigerske2017-scip-global-optimization-of-mixed`; `gleixner2021-miplib-2017-data-driven-compilation`;
- `bestuzheva2021-the-scip-optimization-suite-8`, `hojny2025-the-scip-optimization-suite-10`, `domes2010-constraint-propagation-on-quadratic-constraints`, `tawarmalani2005-a-polyhedral-branch-and-cut`;
- `optimization2026-nonlinear-constraints-gurobi-optimizer-13`, `mittelmann2026-mixed-integer-nonlinear-programming-benchmark`.

**§9:** `wechsung2014-the-cluster-problem-revisited`, `kannan2017-the-cluster-problem-in-constrained`, `basu2023-complexity-of-branch-and-bound`, `dey2022-lower-bound-on-size-of`, `belotti2009-branching-and-bounds-tightening-techniques`, `belotti2012-on-feasibility-based-bounds-tightening`, `chachuat2005-global-mixed-integer-dynamic-optimization`, `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization`.

**App. D:** all per-instance slugs from L2, including:
- `cache2026-minlplib-pages-for-43-target`, `shafique2017-heuristic-global-optimization`;
- `gomes2007-a-sequential-quadratic-programming-algorithm`, `buchanan2008-techniques-for-solving-nonlinear-programming`, `omheni2014-methodes-primales-duales-regularisees-pour`;
- `davarnia2026-a-graphical-framework-for-global`.

**Add to the KB and read before citing (only if D1 is adopted):**
- de Farias–Van Roy 2003;
- Grimm–Netzer–Schweighofer 2007;
- Korda–Magron–Ríos-Zertuche 2025;
- Han–Jiao–Weissman 2018;
- Junge–Osinga 2004;
- the cost-shifting papers (Wainwright et al. 2005; Werner 2007; Sontag et al. 2011; Wald–Globerson 2014).

`robertson2025-on-the-convergence-order-of` is metadata only: read it before citing. Higham (2002), cited by the eg auditor, must be added if App. F cites it.

**Citation rules.**
- Never cite unread sources for their content. Name them only as unavailable to us: Arrow–Kurz, GLOPEQ 1997, the Floudas handbook, Huang 2011, Ghaddar et al. 2015, the 2022 waterno2_04 paper, Murtagh–Saunders Example 5.11.
- Do not cite internal project notes under R/; theory that is used is proved in the paper.
- Cite unpublished companion manuscripts only if they are public.

---

## 8. Claims that must NOT be made

**1. Priority and novelty**
- "First certified (verified) MINLPLib instances" (Halbig et al.).
- "First audit or cross-check of MINLPLib bounds", "first benchmark verification", "first report of wrong dual bounds", or "first solver-reliability study" (Vigerske 2014; MIPLIB; Neumaier et al. 2005; Nowak–Vigerske 2008; Vigerske–Gleixner 2017; Bestuzheva et al. 2025).
- Any unconditional "first" or "previously unsolved globally".
- "First global solution" of lnts50, camshape100/200, eg_int_s, dtoc5 or optcdeg2.
- "First solution" of ex6_2_5/7, or any statement that McDonald–Floudas did or did not solve them.
- "First finite dual" for ann_cumene_tanh.
- Discovery of hvycrash's value.
- Any "first" about R_P, which is a model we defined.
- Novelty of any mechanism:
  - Lagrangian, SDP or period decomposition;
  - calibrations, Krotov/Mangasarian/Arrow sufficiency;
  - Sturm comparison, tangent-plane tests, hidden convexity;
  - Taylor models, affine arithmetic, safe LP bounds, FBBT;
  - Krawczyk existence proofs, rational PSD certificates;
  - envelope or rank-one cuts, cellwise slopes, DP over separators.
- That a general solver capability was implemented or tested.

**2. Scope**
- Any claim for reading (c), or for source models or copies:
  - CUTEst DTOC5/OPTCDEG2, COPS 3.0 catmix, the continuous control problems;
  - MATPOWER case30/39, powerflow0030r (its wave-3 bound is unverified and must not be used);
  - QPLIB copies, except by their separate bounds;
  - the Davarnia–van Hoeve data, Manne's etamac, and the glider or rocket physics.
- That dtoc5 is "textually identical" to QPLIB_8585.
- That any instance is "now solved on MINLPLib" or that its S mark will change.
- That our dual bounds bound tolerance-feasible points.
- That every dual code reads decimals exactly, until §9 item 2 is done.
- That points other than dtoc5, chain and powerflow are infeasible under binary64.
- That the camshape or hvycrash exact values hold under binary64.

**3. Exactness**
- Exact optima other than camshape, hvycrash and lnts.
- lnts in "closed form".
- That the stored lnts Krawczyk points are optimal or "agree" with the optimum. They are strictly suboptimal; only their enclosures overlap.
- For dtoc5:
  - "zero duality gap";
  - "the exact dual value" (say "rigorous rational evaluation below the dual function");
  - the gap "7.2·10⁻⁴³";
  - uniqueness, unless D3 adopts the critic's proof;
  - "no variable has finite bounds";
  - the dynamics "ẏ = y² − u".
- For lukvle10: global optimality of x*, a zero duality gap, "agrees to 10⁻¹⁹", or a dual independent of mpmath.
- That catmix chatters, or that its DP bound is exact.
- That the optcdeg2 optimizer is bang-bang (only the certified trajectory is), unless the critic's near-bang-bang proof is added.
- That the optcdeg2 diagnostic trajectory is exactly feasible.
- "Gap 0" without "attained exact optimum".

**4. Unclosed instances**
- KAN:
  - closed, solved, an OSIL optimum, or OSIL-feasible points;
  - R or R_P as "the trained network";
  - a blanket "10⁻¹⁰" gap;
  - a SCIP bug on KAN;
  - "the same incumbent in all six reruns";
  - that the review reran the r5 searches;
  - "SCIP's duals are valid for R".
- ann: closed; the "first finite dual"; that the source's reduced-space problem equals our R; the cluster effect stated as fact.
- waterno2:
  - closed; "1.67%"; factor "6.22" or "6.2" as a lower bound;
  - bounds checkable from stored files; three independent codes verified the pair bounds; bit-identical regeneration of 18/24;
  - the 06 primal as ours;
  - comparisons with Huang's numbers; "MSc thesis";
  - that listed waterno2 duals are invalid; that cell slopes beat further splitting.

**5. eg**
- An exact optimum.
- "Solved for the first time".
- "Assumption-free", "libm-free" or "interval-verified on every leaf", unless the audited rerun completes and is reviewed.
- 5.760539610694994: use …993.
- "Box-for-box identical" replays.
- A diagnosis of Gurobi, or "terminated optimally".
- Physical or GP provenance.
- That the listed p1 points are feasible.
- Values below L as solution values.

**6. Solvers**
- Bugs in BARON, Gurobi, MINOTAUR, ANTIGONE, LINDO, COUENNE or CPLEX.
- "BARON failed" on camshape100/200, or that it is wrong within its tolerances.
- "Zero closures" without crediting BARON's tolerance-level closures.
- That MINOTAUR's camshape800 (QPLIB_3177) claim is "false" or "refuted".
- That the SCIP mechanism explains every wrong run, or that any listed SCIP bound is wrong.
- "SCIP cuts off feasible points" without the sense of "feasible".
- "Independent of any data semantics".
- The 12-row trigger count.
- That SCIP's traced activity equals the tightest enclosure at both ends.
- "Reported upstream" or "confirmed by developers", unless true.
- That the latest patch releases were tested.
- Any speed ranking, isolated-core timing or CPU-time comparison.
- That instances "remain open for solvers" beyond these runs.
- Treating 50-digit residuals as proofs.

**7. Audit**
- Any cause; "reported a local optimum as a bound" (an inference).
- That aggregates, S marks or `.solu` values are invalid (eniplac and stockcycle keep only the (i-r) status of their displayed listing duals).
- That tolerance-scale cases contradict solved marks.
- That the (i-r) solver bounds are invalid (only the displayed numbers are).
- That six-digit rounding is proved.
- That all invalid MINLPLib bounds were found.
- That display ties or classes (ii)/(iii) are valid or invalid.
- "Three independent topopt points" (there are two).
- That all 1,632 OSIL files were checked byte-identical (69 were).

**8. Pattern and interpretation**
- That "most" closures share the pattern (it is 15 of 31).
- That all staged certificates are instances of Lemma 4.1 (catmix uses Lemma 4.2).
- That all pattern certificates use windows.
- That branching was always low-dimensional (pindyck, eg).
- That treewidth caused openness.
- That single-tree B&B is provably exponential on these instances.
- That the band theorems predict closures.
- That 146 or 155 is MINLPLib's open set, or that 29/155 is a solve rate.
- "Relaxation, not branching" as a tested fact.
- That the formulation decided powerflow0039, or that the 0039p and 0039r optima are equal.
- That no affine split can be exact on optcdeg2 (without hypotheses).
- That "the plain-SDP 0039 gap of about 1.27 is proved".
- "7 of 17 families" (it is 6 of the 14 closed families).

**9. Primal points**
- That a decimal vector (.sol, box centres, .approx40) is exactly feasible.
- mpmath-free proofs for hvycrash, etamac, pricing050 or pindyck.
- mpmath dependence for the 13, water, ANN, KAN, eg or ex6_2_* primal claims.
- The existence or non-existence of a rational chain point, or a genus claim.
- A listed page display below our dual, by itself, as evidence of infeasibility.

**10. Verification and process**
- "Each closure was verified by two independent codes" (false for the displayed catmix and lukvle10 duals).
- "Formally verified".
- "Independently reviewed by humans", unless true.
- "Independent" without the definition and the AI-agent disclosure.
- Describing internal verification as peer review.
- That the chain or catmix bounds need no trusted component.

**11. Unsafe or superseded displays (never print as bounds):**
Since round 2 (G7-04), these strings appear only in `artifact/HISTORY.md`
(the former S8 table and the superseded certificates); neither PDF prints any
of them, except 352.238025369202 as the weaker bound that the other `lukvle10`
implementation certifies (status *weaker second*; Section 4, S1.1 and
`tab:trust-full`), never as the paper's dual.
- 352.2380254050785 (lukvle10; above the certified end);
- 352.238025369202 (valid but superseded; never as the paper's dual);
- the 10⁻¹⁰-margin lnts values and the verifier's 16-digit lnts100/200 displays;
- 41869.05148327244 (0039r);
- 293.87607509587509238 (rounded up) and the "± 5·10⁻⁶⁴" optcdeg2 display;
- 5.072261493982863 (chain50) and 5.068917341793162 (chain200);
- −0.16084761546364904 (ex6_2_7);
- −15.294675643368092 and −15.294675643368092168 (etamac);
- −0.0480694320309595635 (catmix100) and the float-printed catmix200 primal digits;
- −0.048056547756611555 and −0.048055901330847467 (catmix recheck primal displays);
- 10.335474275747004 (topopt, a float of a rational);
- the superseded wave-3 powerflow0039 values;
- "within 3.8·10⁻⁵" (use 3.9·10⁻⁵);
- "1.67%";
- "7.2·10⁻⁴³";
- "600-fold";
- "3.73·10⁻¹⁰" and "16.01%" (use 3.74·10⁻¹⁰ and 16.02%);
- "≥ 3.162849·10⁻³" and "≥ 1.552322·10⁻⁴" (the paper prints 3.11·10⁻³ and 1.54·10⁻⁴, the margins to any value within one unit of the last displayed digit; round 1, G4-03; 3.162·10⁻³ and 1.552·10⁻⁴ are superseded);
- "by 4.3%, 7.5% and 81%" as "at least" margins (use 4.3/7.4/80%).

---

## 9. Pending work and author decisions before drafting

**Computations and checks**
1. **eg audited rerun** (in preparation; `D/eg-audit/`).
   - Rerun route R on every leaf of all three instances, with every exp and integer-power value audited by `auditor.py`.
   - Write Lemma A1 as a proof covering the pow paths.
   - Record timings.
   - Have the diff and results reviewed independently.
   - Until then, use the fallback wording of §5.5.
2. **Dual-side data reading** (primal-points critique CR-A4; about 10–20 minutes of code reading per family). Record in Table 1 whether each dual code reads decimals exactly, encloses them outward, or uses binary64. Rerun or add a perturbation margin for any binary64 reader. This matters for the zero gaps and every gap at or below the 10⁻¹⁶ relative scale.
   - Confirmed in the dossiers, reviews or critiques: lnts, dtoc5, optcdeg2, chain, the wave-2 small verifier, KAN, waterno2 and powerflow.
   - To confirm: camshape, catmix, pindyck (author's code), ANN, eg and lukvle10.
3. **Regenerate every relative cell** under δ = Δ/min(|L|, |U|) by script, and check the display-versus-cell rule (4.3).
4. **Reconcile the primal trust table** (§6). optcdeg2 has the integer-interval proof; the mpmath-only primal claims are hvycrash, etamac, pricing050 and pindyck.
5. **If D1 is adopted:** a 2–4 reviewer-hour confirmation of the extended-value proofs (Γ semiconcave; finite potentials; hypotheses of Theorem 9.1 and Proposition 9.2), and reading the antecedents listed in §7.
6. **Optional (seconds):** compare lnts100–400 p1 with the optimum before generalizing the lnts50 artifact remark.

**Packaging**

7. Archive the KAN review evidence from `/tmp/sol-kan-review/`: `audit.py`, `evidence/`, the exact table checks and the rerun logs. The lnts and dtoc5 review code is already in `D/reviews/code/`.
8. Document the waterno2 fixed-target replay (vbb2 at stored targets); no new computation is required by the paper.
9. Build `claims.json` and the display record (App. I, J); rerun `build_result_maps.py`, `rebuild_manifest.py` and `check_package.py` after edits.

**Author decisions**

- **D1:** whether this paper is the venue for the band theory. Default: main-text validity results (Lemma 4.1–Proposition 4.5); Theorem 9.1 and Proposition 9.2 as a short explanatory subsection; the rest in App. G.
- **D2:** the gap convention. Recommended: δ = Δ/min(|L|, |U|).
- **D3:** optional strengthenings, each only after review:
  - dtoc5 uniqueness (critic's paragraph);
  - optcdeg2 near-bang-bang control on the middle arc;
  - tighter ex6_2_5/7 values from the third Gibbs code;
  - the pindyck strong-concavity gap (≤ 6·10⁻²⁹, both enclosures);
  - lukvle10 ≤ 1.42·10⁻⁹ display (adopted here);
  - pricing050 ≤ 1.92·10⁻¹⁴ (needs the exact point objective stored).
- **D4:** SCIP upstream filing; optional notices to the MINLPLib and BARON maintainers. The text must match the facts at submission.
- **D5:** optional solver reruns (the overloaded batch and the memory stops). Not needed for any stated claim.
- **D6:** the KAN theorem object. Recommended: state it for R_P and note that L also bounds R.
- **D7:** AI-use disclosure wording and the human-responsibility statement.
- **D8:** release licence and archive DOI.

---

## 10. Anticipated referee questions and where the paper answers them

| question | answered in |
|---|---|
| Is anything new beyond hand-tuned instance work? | §1.3–1.4; §4.1 framework; §7 (systematic audit); §9 taxonomy; §11.1 |
| Why certify decimal semantics when solvers see binary64? | §2.1 (readings, sensitivity, KAN); 4.1 (exact-MIP precedent) |
| How independent is "independent", and which displayed values rest on one code? | §2.6; Table 1 |
| Which results rest on library functions or IEEE assumptions? | Table 1; §5.5 (eg, KAN); App. F |
| Is the instance selection biased? | §3.1 caveats |
| Are the solver runs fair? | §8.3 setup and caveats; App. H |
| Can a technical editor replay the claims in reasonable time? | §10 tiers; App. I |
| How large is the improvement where MINLPLib was nearly closed (lnts50, camshape100)? | Table 2; §3.4 (stated openly) |
| Why does regeneration of waterno2_18/24 give different numbers? | §4.5; §10 |
| Does a tolerance-feasible point below your bound mean your bound is wrong? | Lemma 2.4(b), Prop. 2.6, Lemma 2.5, Prop. 5.4 |
