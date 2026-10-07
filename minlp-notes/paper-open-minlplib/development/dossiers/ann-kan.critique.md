# Critique of dossier `ann-kan.md` (ann_cumene_tanh and the six KAN models)

Independent critic, 2026-10-04. Paths without a prefix are relative to
`research-20260929/` (R/). Nothing under R/ or literature/ was edited. All
checks ran in a disposable copy (`/tmp/annkan_critic/`), one process at a
time. The new check scripts and logs are in
`paper-open-minlplib/development/dossiers/ann-kan-critique-checks/`.

## Verdict

**Corrections needed; nothing invalidating.** Every claimed number that I
rechecked is right: L\*, the ANN primal enclosure and gap, all six KAN gaps,
the displays, the Δ values, L ≤ LB_ideal − Δ, L ≤ L_ver, the rerun table, the
listed MINLPLib values, and the worked infeasibility example. The proofs of
Lemmas A.1, A.3, A.4, A.5 and K.3 hold. So do Proposition K.1, the
saturated-tanh argument (I12), and the soundness of the rounding in `annx.py`
and of the one-function change in `kan_bnb_rigexp.py`. The corrections below
concern:

- one wrong statement about prior work (the source paper's reduced-space
  problem is not "the same" as our R);
- one missing method antecedent in the local knowledge base (Ninin, Messine
  and Hansen 2015);
- a component that the two KAN bound paths now share (the authors' rigorous
  exp), which the "either code is correct" argument must name;
- one false factual remark about the rerun incumbents;
- two displays rounded the wrong way;
- several precision and wording points.

I also closed one trust gap that the dossier did not name. All decoders use
the same OSIL reader (`osilx`). An exact comparison with the primal
reviewer's independent reader `rosil` finds 0 differences in all eight files
involved.

## What I checked (targeted; no project-wide checks, no CI)

1. Read the dossier on disk (identical in content to the task text) and its
   check scripts and logs (`ann-kan-checks/`).
2. Exact recomputation (Fractions/Decimal), from `open-instances-wave3/logs/*.result.json`,
   the point JSONs, `gap-values.json`, `reviews/wave3-verification/logs/*.bnb_v2.json`
   and the rerun `ann-kan-checks/logs/*.bnb.json`:
   - L\* = −7447080719734483/2⁴¹ equals the double −3386.5402291369187.
   - The ANN gap is 6.5578350651471487992…. The relative gaps are
     1.9401980e-3 of |primal| and 1.9364409e-3 of |dual|.
   - The twin difference is 7.18e-8, and the p1 difference is 4.82e-8.
   - The wave-3 gap is 644.51258 (19.0685% of |primal|, 16.0147% of |dual|).
   - All six KAN values U − L equal `exact_upper` in `gap-values.json`.
   - L ≤ LB_ideal − Δ holds for all six, with margins from 5e-19 to 6.7e-14.
   - L_ver − L and U − L_ver match the dossier, for both the wave-3 run and
     the rerun.
   - All safe displays in Section 5 are correct, except the two noted in C5.
3. OSIL facts with `osilx` on copies:
   - ann rows e749, e750, e782–e790, the bounds of the ten extra variables
     and the 728 bounded variables; c₀ = 10619.965999999999.
   - kan_r5_h1_n3 rows e48, e49 and e77, and the big-M rows e29/e30
     (b6 interval [−0.5857759315175706, −0.0040155389917946]), giving
     ρ₁ = −2.8e-17. Scaling row e4, with a + sign, as in I17.
   - kan_r3_h1_n4: x1076 and its scaled copy x1077 (row e6), and copies
     x1083–x1085.
4. Rerun of the dossier's `kan_infeas_edge_class.py`:
   - kan_r5_h1_n3/x776: 6 of 6 pieces infeasible. b4: ρ₁ ≡ ρ₂ ≡ 0, ρ₃ has
     no root in the interval. b5: gcd constant. b6–b9: ρ₁ is a nonzero
     constant. This matches Section 3.2.1.
   - kan_r5_h1_n5/x1292 and kan_r5_h1_n8/x2066: 6 of 6 each, with
     Z₁ = [−1.7394724746200056, 1.7328417001798049] in both.
5. **New:** `cmp_readers.py`, an exact comparison of `osilx` with `rosil`
   (`publication/reviews/primal-water-ann-kan-r1/rosil.py`) on ann_cumene_tanh,
   ann_cumene_exp and the six KAN files. It compares variable names, types and
   bounds, the objective, row bounds and constants, and the linear, quadratic
   and nonlinear terms. Result: 0 differences in all eight files.
6. **New:** `silu_exact.py` checks in rational arithmetic that the actual
   constant `kan_iv.SILU_MIN_LO` = −0.27846454276107413 is ≤ the mean-value
   lower bound −0.2784645427610738 (margin 3.35e-16).
7. Code reading (no execution in the main tree):
   - `kan_iv.py` and `ia.py` in full;
   - `annx.py` in full (forward pass, tanh_lin, objective, bound,
     dual_value, prove) and `verify_boxes.py`;
   - in the authors' ANN code: `ann_bb.tanh_pt`, `ann_tm.tanh_lin`,
     `_g_range`, `_tm_affine`, the start of `SepModel`, and the affine,
     forward and objective code in `ann_fast.py` and `ann_bb.py`;
   - `kan_bnb.py`: evaluate, `_lb3`, `_half_ginv_g`, `minquad`, `bnb`, and
     the 17-line diff of `kan_bnb_rigexp.py`;
   - `bbcore.py`, the Net and main functions of `kan_bb.py`, and
     `kan_model.spline_error`.
8. Literature: Table 4 of the local arXiv text of
   `schweidtmann2019-deterministic-global-optimization-with-artificial`;
   Section 2.4.4 and Table 2.8 of the 2021 dissertation; the network report,
   Sections 4 and 6; the saved MINLPLib pages; and a search of the local
   knowledge base for affine-arithmetic sources.

## Corrections

**C1. Section 7, ann bullet 1 (dossier line ≈823): the source's reduced-space problem is not "the same" as our reduction.**

- *Problem.* The dossier says "Their reduced-space formulation has the same
  five variables and one inequality as our reduction." Our R (Section 1.1) has
  5 variables and 723 inequalities: the 722 bounds of determined variables
  plus x772 ≥ 0.999. One of these bounds, the training-domain bound
  x647 ≥ −1, is active at the best known point.
- *Evidence.*
  - arXiv v2, p. 21, and the dissertation, Section 2.4.4 (p. 29): "The RS
    formulation constitutes only 5 variables, 0 equality and 1 inequality
    constraints."
  - `reviews/ann-extension-review.md` Section 5: x647 is active, with
    multiplier 58.51.
- *Consequence.* Unless MAiNGO enforced the intermediate bounds implicitly
  (the source does not say), the source's reduced-space runs addressed a
  relaxation of the MINLPLib model whose optimum may lie below −3379.98.
- *Fix.* Write: "Their RS formulation uses the same five decision variables
  but is stated with one inequality. Our R keeps the 722 bounds of the
  determined variables, and x647 ≥ −1 is active at the best point. The source
  does not say whether its RS runs enforced these bounds, so those MAiNGO
  gaps may refer to a relaxation of the MINLPLib model. The BARON
  full-space runs used the 794-variable model."

**C2. Section 7 and I16: the closest method antecedent is missing.**

- *Problem.* The local knowledge base contains
  `ninin2015-a-reliable-affine-relaxation-method` (Ninin, Messine, Hansen).
  That paper builds affine-arithmetic linear relaxations of *constrained*
  problems inside an interval B&B. It obtains rigorous lower bounds and
  infeasibility certificates by rounded interval post-processing of
  approximate LP duals. This is exactly Lemma A.4 plus the per-box LP and
  the infeasibility test. The knowledge base also contains
  `messine2002-extensions-of-affine-arithmetic-application`.
- *Evidence.* `literature/papers/ninin2015-a-reliable-affine-relaxation-method/fulltext.md`
  (abstract) and its `paper.md` notes ("Rounded interval postprocessing of
  approximate LP dual solutions supplies rigorous lower bounds or
  infeasibility certificates"). I16 lists only stolfi2003, figueiredo1997
  and berz2009.
- *Fix.*
  - Cite ninin2015 as the direct precedent of the per-box bound, and
    messine2002 for affine-arithmetic extensions.
  - Describe what differs: reduced space, one shared symbol per neuron for
    250 tanh neurons, explicit rounding analysis, a box partition replayed
    and re-certified by a second code.
  - Keep "not claimed as new in method".

**C3. Sections 3.2.4, 6 ("Remaining assumptions"), 9 and I1/I13: the two KAN paths now share the authors' exp.**

- *Problem.* The rerun `kan_bnb_rigexp.py` replaces the verifier's numpy exp
  with `kan_iv.iexp_pt_fast`, which is built on `ia.NI`. Both are the
  authors' code, and path (II) uses them too. After the rerun, "L is valid
  if either code is correct" holds only if these shared routines are also
  correct.
- *Evidence.* `kan_bnb_rigexp.diff` (`import kan_iv as _KIV`). `kan_bb.py`
  and `ann_bb.py` import `kan_iv`, which imports `ia`.
- *Fix.*
  - State: "Path (I) as rerun and path (II) share the rigorous exp
    `kan_iv.iexp_pt_fast` and the interval core `ia.NI`. These were read in
    full by the dossier author and by this critic, and their mpmath-derived
    constants were checked in rational arithmetic. The wave-3 run of (I),
    with numpy's exp widened by 2⁻⁵⁰, gives the same bounds (bit-identical
    for five instances; 3.2e-12 higher for kan_r5_h1_n3). It is an
    exp-independent but empirical cross-check."
  - No computation is needed.

**C4. Section 8.3, last paragraph: "the same incumbent point was found in all six runs" is false.**

- *Evidence.* `ub_u` differs between `reviews/wave3-verification/logs/<n>.bnb_v2.json`
  and `ann-kan-checks/logs/<n>.bnb.json` for two instances:
  - kan_r3_h1_n4: [0.8622569972242282, 0.7887338126096038, 0.8096463448382059]
    against [0.8622569044105722, 0.7887336048903788, 0.8096459380687246];
  - kan_r3_h1_n5: [0.8660529443494409, …] against [0.8660528182558672, …].

  The rigorous UB values are bit-identical. Changing the exp changed which
  local-search start came first among starts with equal outward-rounded UB.
  For r3_n9, r5_n3, r5_n5 and r5_n8 the points are identical.
- *Fix.* "In all six runs the incumbent's rigorous UB, and hence UB − tol, is
  bit-identical, except kan_r5_h1_n3 (same point, UB 3.2e-12 lower). For
  kan_r3_h1_n4 and n5 the local search returned a different nearby point
  with the same outward-rounded UB."

**C5. Section 5: two displays are rounded the wrong way.**

- *Problem.*
  - KAN table, relative column, kan_r5_h1_n5: the exact value is
    1.0177548e-10 / 0.27258325385485 = 3.73374e-10. Under the dossier's
    "gaps rounded up" rule this is **3.74e-10**, not 3.73e-10. The other
    five entries are correct upward roundings.
  - Section 5.1, wave-3 row: 16.0147% of |dual| rounds up to **16.02%**,
    not 16.01%. The value 16.1% in `gap-values.json` is a valid upward
    rounding at three significant digits, not a discrepancy.
- *Fix.* Replace the two values and drop the implied discrepancy.

**C6. Section 3.1, Lemma A.3: "(asserted in both codes)" is not literally true.**

- *Evidence.*
  - `annx.forward` asserts `Az[…, sym] == 0`.
  - The authors' `SepModel` has no such assertion. It asserts exactly two
    tanh levels (`assert len(th) == 2`). A neuron's own symbol is created
    only at its level, so the property holds by construction.
- *Fix.* "asserted in the reviewer's code; true by construction in the
  authors' code (two tanh levels, asserted)."

**C7. Section 3.2.1, proof of Proposition K.1: "equivalently, the gcd of the nonzero residuals is constant" is inaccurate.**

- *Problem.* A nonzero pairwise resultant (the verifier's test) and a
  constant gcd of all nonzero residuals (the dossier's test) are different
  sufficient conditions. The second is weaker.
- *Fix.* "…or the residuals have no common complex root: the verifier shows
  a nonzero pairwise resultant, and this dossier shows that the gcd of the
  nonzero residuals is constant."

**C8. Section 0 table ("points of R_P attaining U") and Section 9 ("The upper ends are attained by points…").**

- *Problem.* U is the upper end of an outward enclosure of the point's
  objective. The objective lies within 3.2e-89 below U (review r1), but it
  is not equal to U.
- *Fix.* "points of R_P with objective ≤ U (enclosure width ≤ 3.2e-89)".

**C9. Section 4.1, Lemma P: the linearity condition is missing.**

- *Problem.* The lemma requires only "the only unknown with a nonzero
  coefficient". The construction and review r1 also require that the unknown
  does not occur inside a nonlinear term or a square, and that its total
  coefficient (linear coefficient plus bilinear partners) is provably
  nonzero.
- *Fix.* Add both conditions to the lemma.

**C10. Section 7, last ann bullet: "The remaining gap is a constrained cluster effect" is stated as a fact.**

- *Problem.* This is an interpretation.
- *Evidence.*
  - The 1800 s frontier is spread over the domain. The median normalized
    distance from u\* is 0.464 (review Section 5).
  - f is nearly flat along x772 = 0.999 over a large region (extension
    Section 5).
  - The sub-box test (gap 0.655 after 900 s) supports slow local closure
    but does not isolate the cause.
- *Fix.* "The remaining gap is consistent with a constrained cluster effect
  of first-order bounds along a large, nearly flat valley on x772 = 0.999
  (…eigenvalues…)."

**C11. Section 3.2.3: tolerance details.**

- *Problem.*
  - Path (II): `tol_abs = tol_rel·max(1, |fbest|)` is fixed from the
    local-search value, not from |UB|.
  - Path (I): tol is recomputed whenever UB improves. The chain
    "UB_then − tol ≥ UB_final − tol" then needs the fact that
    x − rtol·max(1, |x|) is nondecreasing in x.
- *Fix.* Say both. Validity is unchanged.

**C12. Archive hygiene in `ann-kan-checks/`.**

- *Problem.*
  - The docstring and usage line of `kan_infeas_edge_class.py` say "the
    argument's own variable bounds" and `kan_infeas_edge.py`. The script
    actually intersects with the input-class box.
  - `silu_min_check.py` tests the constants −0.27846454276108 and
    −0.278464542761075, not the actual `SILU_MIN_LO` = −0.27846454276107413.
  - Its log line "claimed bound … valid: False" comes from the crude bound
    and will confuse readers.
- *Evidence.* The scripts and the log. My `silu_exact.py` confirms the
  actual constant (margin 3.35e-16).
- *Fix.* Correct the docstring and the usage line, test the actual constant,
  and label the crude-bound line.

## Additional issues

**A1 (minor; resolved here). One OSIL reader is shared by all decoders.**

- *Problem.* `ann_model`, `annv`, `kan_model`, `kan_decode` and the
  dossier's infeasibility scripts all parse with
  `reviews/open-instances-verification/osilx.py`. The dossier presents
  decoder agreement (and "three readers") as independent model reading.
  Decoder agreement tests the decoding logic, not the parsing.
- *Resolution.* `cmp_readers.py` compares `osilx` with the independent
  `rosil` exactly for ann_cumene_tanh, ann_cumene_exp and the six KAN files:
  0 differences. Add this to the trust list ("model reading: osilx, checked
  exactly against an independent reader") and archive the script.

**A2 (minor). NaN in the authors' KAN branch and bound is not addressed.**

- *Problem.* In `bbcore.run`, a NaN lower bound is discarded silently:
  `keep = lb < UB − tol` is false, and `fath` excludes NaN. The verifier's
  code is NaN-safe: lb1 and lb2 map NaN to −inf, and lb3 is set only from
  finite estimates with an exact rational correction. The dossier raises
  NaN only for the ANN codes.
- *Fix.* Add "no NaN lower bound (unchecked)" to the assumptions of path
  (II). Since L ≤ L_ver, the conclusion is unaffected.

**A3 (minor). Review of the one-function change requested in I1: done.**

- *Finding.* The change is correct.
  - `iexp` returns [lower end of `iexp_pt_fast(x.lo)`, upper end of
    `iexp_pt_fast(x.hi)`]; this is valid because exp is increasing.
  - Shapes are preserved.
  - `iexp_pt_fast` asserts |x| ≤ 700 and |r| ≤ 0.0055, so NaN or
    out-of-range arguments crash instead of passing silently.
  - k ≥ −1010 keeps the results normal.
  - No other libm call remains in a rigorous path of `kan_bnb_rigexp.py`
    or `kan_decode.py`.
- *Remaining action.* Only archiving.

**A4 (minor). The cost and risk of I2 need two additions.**

- *Problem.*
  - Regenerating the region list depends on the replay reproducing the
    authors' tree bit for bit in the current numpy/scipy environment.
    Acceptance test: `leaves.py` frontier identity. If the environment has
    changed, the new tree must be re-verified in full.
  - Under the project's two-core limit, `verify_boxes.py` needs about
    9.3e3 CPU-s ≈ 2.6 CPU-h, that is about 1.3 h wall, not 35 min.
  - The final-open-box part can be re-verified directly from
    `ext_logs/open_run2.npz` without the replay: about 25 CPU-minutes.
- *Fix.* Add both points to I2.

**A5 (minor). The infeasibility of p1 is given in two different metrics.**

- *Problem.* Section 2 gives "infeas 2e-12" (the MINLPLib page). Section 4.1
  gives "row violation 8.2e-12" (the absolute maximum, row e790; review r1
  and the wave-3 verifier).
- *Fix.* Name the metric next to each value.

## Assessment of the dossier's own issues I1–I17

- **I1.** Correct. With C3 and A3 the resolution is sufficient. The cost is
  right: 3274 s ≈ 55 CPU-min.
- **I2.** Correct. Add A4.
- **I3.** Correct (review r1 used exact rational arithmetic only).
- **I4.** Correct. The statements L ≤ min R ≤ min R_P ≤ U are all proved.
- **I5 and I6.** Correct. I confirmed the wording in `SYNTHESIS.md:434–436`,
  `closing-research-results.md:214–215` and
  `publication/reproduction/README.md:330, 335`.
- **I7.** Correct. Use 16.02% if the dual percentage is kept (C5).
- **I8.** Correct.
- **I9.** Correct. The margin is 7.18e-8 against a slack of 5e-7; class
  (i-r) has 0 < d − hi ≤ slack. The bound audit has no cumene entry.
- **I10.** Acceptable, with the softened wording of C10.
- **I11.** Correct. "Minutes" is plausible.
- **I12.** Correct; I re-derived it. Every use of a saturated T = [1, 1]
  passes through an outward-rounded operation that widens the result by at
  least 2⁻⁵⁵·max(1, |w|):
  - T − α·s (including α = 0, where the step at 1 absorbs it);
  - 1 − T·T;
  - w·T in `NI` products;
  - midpoint-radius affine maps, where the term γ_{k+1}|w||x_m| covers it.

  This holds in `ann_tm.tanh_lin`/`_g_range`, the forward passes of
  `ann_fast` and `ann_bb`, and `annx.tanh_lin`.
- **I13.** Correct. Add C3 and A2.
- **I14.** Correct; I re-read `check_constants.py`, and its logic is sound.
- **I15.** Correct (1.62e-14, 2.93e-15 and 2.09e-13 in `kan_primal.log`).
- **I16.** Incomplete; see C2.
- **I17.** Correct (row e4).

## Conclusion

- **L\* = −3386.5403** (display) for ann_cumene_tanh and ann_cumene_exp:
  stands.
- **The exactly feasible ANN point** (−3379.98239407177…): stands.
- **KAN, exact infeasibility of the six OSIL models:** stands.
- **KAN, enclosures [L, U] of min R and min R_P**, with gaps ≤ 2.42e-8 for
  kan_r5_h1_n3 and ≤ 1.08e-10 for the others: stand.
- **What must change before writing the paper:**
  - the prior-work statements C1 and C2;
  - the shared-component disclosure C3;
  - the factual fix C4 and the displays C5;
  - the wording fixes C6–C11.
- **Model reading** can now be stated as cross-checked by an independent
  reader (A1).
