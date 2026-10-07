# Critique of the `small` dossier (hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck)

Reviewer: independent critic, 2026-10-04. Target: `dossiers/small.md` (file of
2026-10-04 04:07). `R/` = `research-20260929/`. Nothing under `R/` or
`literature/` was edited. Checks ran on copies in `/tmp/critic-small/`. The
script and logs are in `dossiers/small-critique-checks/`.

## Verdict

**Corrections needed; nothing invalidating.** I tried to refute every theorem,
proof step and claimed bound, and I failed to break any of them. All six
dual bounds, all primal points and every summary gap cell are valid as stated.
The corrections below fix presentation problems, an incomplete list of unsafe
strings, an inaccurate trust-base statement, outdated literature metadata and
some small numeric slips.

## What I checked

**Proofs re-derived by hand.**
- **hvycrash.** Theorem 1(a) and (b): κ, A(0.08), D(0.08), the downward
  induction, and the cos 2.6 bracket. The partial sums were recomputed in
  exact rationals: the sum through x¹⁴ gives −0.856888957 and the sum through
  x¹² gives −0.856881557. The terms decrease from the second on.
- **Gibbs.** Lemma G1, Lemma G2 and Theorem G, including:
  - t ≤ T follows from the rows and the lower bounds;
  - the min(0, T·m_p) step;
  - the t ln t⟨r, y⟩ ≥ −max r/e step.

  For ex6_2_7, D(y_p) = −(1 + ln t_p)·5e-14·y_{3p} at the three phases
  (t = 0.317, 0.485, 0.198). This reproduces the C1 minima 7.21e-15,
  −4.19e-15 and 7.10e-15, and confirms the figure-3 mapping.
- **etamac.** Lemma E2 (the power-mean form, the exponent identities and the
  majorant inequality) and Theorem E.
- **pricing050.** Theorem P and μ·r: −11339002580124213683593/2.5e18. The
  upper bound recomputed from Σ min F_j equals the logged value exactly.
- **pindyck.**
  - Lemma P2.
  - Lemma P4: the full implicit second derivative of s = a + bφ(s) and the
    ∇²b, ∇q and ∇²q terms.
  - Lemma P5.
  - Theorem 6, including the completed square. ‖g‖²/(2μ) ≤ 1.69945e-29 was
    recomputed from `primal_enclosure.txt`.
  - The display −…069306 is valid, the primal display −…069288 is safe, and
    the radius is 3.687e-13.

**Code read for soundness.**
- `small-checks/r2/gibbs_cert.py` (C1), covering:
  - domain cover and the 200-bit discard test;
  - the window construction;
  - the monotonicity of λ_min of a 2×2 matrix;
  - the use of the mean-value hull;
  - the assembly.

  mpmath 1.3.0 keeps a 50-digit mpf exact when it converts it into a 30-digit
  `iv` interval, so the window sub-boxes do cover W.
- The verifier's `gibbs_bb.py` (natural, mean-value and second-order forms,
  including the off-diagonal endpoint argument) and `gibbs_bound.py`, which
  checks the vapour form symbolically.
- `small-checks/r2/pricing_check.py` (window and exclusion, F′ and F″
  formulas, structure asserts).
- The review's `own_psi.py`, where I checked the arithmetic model only.

**Reruns on copies.** All runs used one thread. Results are in
`small-critique-checks/rerun.log`.
- `hvy_check`, `etamac_point`, `pindyck_sc` and `gibbs_check`: identical
  logs.
- `pricing_check` and `gibbs_cert.py ex6_2_7`: identical except for timings.
- Negative control: I ran `gibbs_cert.py ex6_2_7` with an empty window list.
  It fails with "cannot fathom" at (0.692795, 0.003993), the −4.19e-15
  minimiser. So the exclusion step is not vacuous.
- The ex6_2_5 run of C1 (198 s) was not repeated. C1 has therefore now had
  one independent code reading and a partial rerun. It has not had a full
  second implementation review.

**Sources checked.**
- Section 2 (listed values) against `fetched.csv`, the saved pages and
  `tables.md`.
- Section 10 item 8 against `solver-runs/results_table.md`.
- The runtimes against `reproduction/commands.json`.
- All literature slugs cited in Section 7 exist.
- OSIL spot checks:
  - pricing050 has 46 positive c_j and r = (−500, −651, −615, −788, −984);
  - the etamac weights and bounds;
  - pindyck has 116 = 7·16 + 4 variables;
  - all six GAMS files agree with the OSIL files numerically.

## Corrections

1. **Section 5, etamac row (line 745).** "exact 2.5760e-15" is a typo.
   - The exact gap against the certified value −15.2946756433680921685 is
     2.57652e-15 (`etamac_point.log`; my `critique_checks.log`). Against
     the l(x̂) end it is 2.57650e-15. E2 and Appendix A already say 2.5765e-15.
   - **Fix:** write "exact 2.5765e-15". The cell "≤ 2.6e-15" is unchanged.

2. **Section 5 table and Section 9 (a paper table built from them).** For two
   rows the displayed numbers do not reproduce the gap cell.
   - ex6_2_5: −70.752077833447705 − (−70.75207783344770759) = **2.59e-15**,
     but the cell says ≤ 2.1e-15.
   - etamac: with the proposed primal display, −15.29467564336808959 −
     (−15.294675643368093) = **3.41e-15**, but the cell says ≤ 2.6e-15.
   - The cells are correct, because they use unrounded certificate and
     enclosure ends (summary footnote). A reader who subtracts the displayed
     numbers will still see a contradiction. The dossier's "Display checks"
     test only the rounding direction.
   - **Fix:** use displays that are consistent with the cells. All of these
     were checked exactly as safe:
     - ex6_2_5 primal: −70.75207783344770558 (rounded up from
       −…558036712). The display difference is then 2.01e-15.
     - etamac dual: −15.29467564336809217 (rounded down; it is
       ≤ −15.2946756433680921685), with primal −15.29467564336808959. The
       display difference is then 2.58e-15.

     Alternatively, footnote that the gaps are computed from certificate
     ends, not from the displayed numbers.

3. **Section 5 "Disagreements" item 1 and E6 (lines 764–775, 1063–1064).**
   The list of unsafe secondary strings is incomplete. Each string below lies
   *above* its certified lower bound, so it is not a valid dual display:
   - ex6_2_7 "−0.16084761546364904" lies 3.44e-18 above. It appears in
     `verification-report.md` §1 and §3 and in wave-2 `report.md` §11.
   - etamac "−15.294675643368092" lies 1.68e-16 above, in the same places
     (§1, §4, §11).
   - etamac `etamac.json` "dual_bound": "−15.294675643368092168" lies
     4.9e-19 above.

   **Fix:** add these strings to the E6 "do not copy" list next to the two
   ex6_2_5 strings.

4. **Section 3.5 "Trusted" (lines 709–713) and Section 6 "Remaining
   assumptions" (lines 802–804).** Both statements are inaccurate.
   - "Review: only mpmath `iv` (exp, log) and `Fraction`" is not right. The
     review's affine arithmetic (`own_psi.py`) uses numpy binary64 operations
     with one `np.nextafter` step. It therefore assumes that each IEEE result
     lies within half an ulp of the exact result (its line 17).
   - "Authors' (non-displayed) … pindyck bounds" is wrong. The summary's
     displayed pindyck dual −1170.4862854360886163932 *is* the author's value.
     It is also implied by the review's tighter −…3931058729.
   - Section 0 (line 47) says that no certificate uses A1/A2. That holds for
     the review's code only. The author's pindyck code relies on an A1-type
     hand-checked γ_n padding analysis.
   - **Fix:** state the trust bases as follows.
     - Author: IEEE round-to-nearest plus the γ_n padding analysis.
     - Review: IEEE binary64 elementwise rounding with nextafter, mpmath `iv`
       and `Fraction`.
     - Attribute the displayed pindyck value to both codes, the review's
       being the one with the weaker assumption.

5. **Section 7, ex6_2_* (line 863).** "no slug — the slug
   cuesta2025-global-optimization-of-mixed-integer is a different paper" is now
   wrong.
   - The slug was re-ingested on 2026-10-04 at 04:14, after this dossier was
     written. Its `paper.md` is arXiv:2510.14122v3, "On Leveraging
     Constrained Smooth Additive Regression Models for Global Optimization".
   - Its `fulltext.md` contains Table 5 with the ex6_2_7 gaps 2400.913%,
     1359.993% and 10913.441%.
   - **Fix:** cite the slug.

   Similarly, the Smith (2011) value −1.905155235 is held in the excerpt slug
   `smith2011-smith-thesis-coconut-table-a` (status read). The cited
   `smith2011-improved-placement-of-local-solver` is metadata-only and
   unread. Cite the excerpt slug for the number.

6. **Section 3.2 "No duality gap" (lines 455–458).** "(For ex6_2_7, λ·b
   itself is not a valid bound…)" suggests that λ·b is valid for ex6_2_5.
   - It is not: the exactly feasible rational point lies 1.32e-20 below λ·b.
     The dossier itself says the point lies 1.3e-20 below λ·b.
   - For ex6_2_5 the reason is that λ is rounded (the D minima are −1.24e-22
     and −1.38e-21), not inhomogeneity.
   - **Fix:** "For neither instance is λ·b itself a valid bound (ex6_2_7:
     inhomogeneity, −R·n terms summing to −2.5e-14; ex6_2_5: rounded λ)."

7. **Section 2 (lines 288–289).** "the `.solu` values are weaker for all six"
   is not right: hvycrash has no `.solu` `=bestdual=`, as the table above it
   shows.
   - **Fix:** "for the five instances that have one".

8. **Section 8.2 C1 (line 972).** The example "0.2407 + 11.24 + 2.248 −
   12.7287 combine to 1 − 2.1e-14" does not work: the printed numbers sum
   to exactly 1.
   - The stored coefficients are 0.240734108219679 and −12.7287341082197,
     which sum with 11.24 and 2.248 to 1 − 2.1e-14 (checked with sympy).
   - **Fix:** print the stored digits.

9. **Section 8.2 C1 (line 1001).** "so no λ certifies much below it" is
   imprecise.
   - The floor −4.188e-15 belongs to *this* λ. What the evidence shows is
     that, with this λ, no τ below about 4.19e-15 can be certified. The
     verifier's τ = 1e-17 run failed.
   - Most of the remaining ex6_2_7 gap is the crude −Σ max r/e term
     (5.52e-14), not this floor.
   - **Fix:** reword accordingly.

10. **Section 10 item 4 (line 1185) and Section 1.5 (line 252).** The
    eigenvalue range has two problems.
    - The quoted range "−0.1195 to −0.1111" comes from the extension's text
      about "3,000 sampled **feasible** points", that is, points of F, not G.
      No saved log contains these samples.
    - The saved data are:
      - `pindyck_global.log`: 300 hit-and-run points of G, giving only the
        largest eigenvalue −0.1123;
      - `hess_check.log`: 12 points of G, from −0.11886 to −0.11315.
    - **Fix:** correct the caption (F versus G), and plot only saved data or
      regenerate the samples first. A float sampling run takes seconds.

11. **Section 1.4 (line 212).** "the binary64 values of 0.1, 0.1², 0.1³
    printed in full" is not accurate.
    - The strings are the shortest round-trip decimals of fl(0.1·0.1) and
      fl(0.1³), plus ".1".
    - The model uses these decimals exactly, not the binary values.
    - **Fix:** reword.

## Additional issues (minor)

- **Cost estimates.**
  - E2 says "two script runs on copies, < 1 min". Neither `v_etamac.py` nor
    `v_pricing050.py` writes the decision decimals: the JSON logs contain
    objectives only. Copies must be patched to dump them, which is about
    15 minutes of work.
  - C3 has a cheaper and more independent route. Round the dossier's own
    `pricing_check.py` 50-digit Lagrangian minimisers (same 20-digit μ) to
    25 digits, check rows e5 and e6 in `iv`, and save the point. This takes
    seconds plus a few lines, and it should reproduce the verifier's
    1.1e-18-slack point. Nudge one coordinate if needed, as the authors did
    with x11.
  - E1(b) quotes about 2 h for an independent etamac rebuild. That omits an
    independent box (Lemma E1, about 97 bound steps) and the KKT solve of R.
    3–5 h is more realistic.
- **C2 support.** The 1.7e-29 figure uses the review's gradient enclosure.
  The author's own enclosure (max |∂J/∂p_t| ≤ 8.01e-17, J width 4.9e-30)
  gives ≤ 5.6e-29 independently. Mention this so that the sharper pindyck
  statement rests on both codes.
- **gibbs_cert.py hygiene.** Validity is not affected, for the reasons given
  in each item.
  - `assert all(r >= 0 for r in Rmax)` checks only max_i R_p,i ≥ 0. Theorem G
    needs R_p ≥ 0 componentwise, which holds here (logged R_p).
  - The vapour constant .156969560191053 is hard-coded rather than read from
    the OSIL. Its form is confirmed indirectly by the atom-tree agreement and
    directly by the verifier's sympy check.
  - Add explicit asserts for both before the paper cites C1 as fully
    independent.
- **etamac "Tightness" (line 542).** "the price of κ" is an interpretation.
  - The certified facts are two: the bound equals R's KKT objective (gradient
    4.9e-31), and the etamac point lies 2.58e-15 above it.
  - Whether the gap comes from κ, from the 4e-16 degree excess, or from
    suboptimality of the point is not shown.
  - **Fix:** label it as an interpretation.
- **Section 10 item 7.** The SIF SOLTN(100/500/1000) values belong to the
  N = 100/500/1000 instances, not the MINLPLib model. They are unattainable by
  the every-N identity, which is the literature track's hand derivation, not
  a computed check. Label them as such.
- **Section 1.5.** State that 4 of the 116 variables are fixed initial states
  (td_0 = 18, s_0 = 6.5, cs_0 = 0, R_0 = 500), so 116 = 7·16 + 4.
- **Section 8.4.** The bound |r_k| < 7.86 uses D ≥ 0.0162079. With
  c ≥ 0.08 the sharper value is 7.19. Both are valid.

## Assessment of the dossier's own issue list

- `small-pricing050-gap-v1-wrong`: confirmed. The v1 log prints 1.915e-14,
  and v1 had 2.0e-17 and 1.1e-20.
- `small-pindyck-gap-strong-concavity`: the mathematics is confirmed. Add
  correction 4 (trust base) and the C2 support note above.
- `small-gibbs-single-implementation`: C1 is now partly reviewed. I read the
  code, reran ex6_2_7 and ran the negative control. Adopting C1 still needs
  the two asserts above.
- `small-unsaved-verifier-points`: the cost estimate is understated; see
  above.
- `small-unsafe-secondary-displays`: incomplete; see correction 3.
- `small-etamac-primal-display-missing`: the proposed display is safe. Pair
  it with a longer dual display (correction 2).
- The other items are acceptable as written.

## Commands run (targeted; copies only)

```
python3 critique_checks.py            # in /tmp/critic-small (copy of primal_enclosure.txt)
python3 {hvy_check,etamac_point,pricing_check,pindyck_sc,gibbs_check}.py   # copies in /tmp/critic-small/rerun
python3 gibbs_cert.py ex6_2_7         # copy, 54 s
python3 gibbs_cert_nowin.py ex6_2_7   # sed copy with exclusion(F, ymin, []): fails as expected
```

No project-wide checks were run, and no CI was inspected.
