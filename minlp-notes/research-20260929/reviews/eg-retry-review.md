# Review: `open-instances-wave3/eg/retry.md` (eg_int_s, eg_disc_s, eg_disc2_s)

Date: 2026-10-01. Independent, adversarial verifier. I did not write the
retry or any of its code. Scope: the model decoding, the soundness of the
enclosures and affine models, the coverage and aggregation argument, the
integer handling, the primal values, and the literature and novelty
statements of
[`../open-instances-wave3/eg/retry.md`](../open-instances-wave3/eg/retry.md).
My scripts and logs are in
[`eg-retry-review-checks/`](eg-retry-review-checks/). Only targeted checks
were run. No project-wide verification was run and no CI results were
consulted. Every process ran single-threaded and under `timeout`.

Labels used below.

- **By hand**: I redid the derivation myself.
- **Exact**: checked in exact rational arithmetic (`fractions.Fraction`) or at
  50–80 digits with mpmath.
- **Independent rigorous**: my own bounding code, which shares no code with
  the retry (Section 5). Its floating-point bounds rest on a stated error
  analysis with large safety factors and on one assumption: numpy's `exp` has
  relative error at most 1e-14. A sample of 25,000 arguments gave at most
  1.3e-16 (`logs/check_libm_exp.log`). Its final certificates are checked in
  exact rational arithmetic.
- **Float / sampling**: evidence, not proof.
- **Reproduced**: I reran the author's code and got the logged output.

Nothing was checked in Lean. No finite lemma here would gain from it; the
risk lies in the floating-point bounds and the bookkeeping, and both were
checked by independent computation instead.

## 1. Verdict

All main results hold. I reproduced the search trees of the reported
certificate runs and checked that every tree covers its domain. I then
re-certified the leaves of those trees with independent code against the
claimed bounds:

| instance | claimed dual bound | trees checked for coverage | leaves re-certified independently | failures |
|---|---|---|---|---|
| eg_int_s | 6.4531031529331155 | run C (56,189 boxes) | all 33,385 | 0 |
| eg_disc_s | 5.760539610694994 | run E, both parts (62,779 + 55,973 boxes) | all 46,223 + 40,573 | 0 |
| eg_disc2_s | 5.642100574331458 | run G, all 8 parts (1,152,830 boxes) | part 1 (contains the optimum): all 135,317. Parts 0 and 2–7: 110,676 of 979,044 (in each part the 2,000 tightest closures plus a 10% random sample) | 0 |

The primal points are exactly feasible, and their values match the report
to all printed digits (checked at 60 digits against an independent reading
of the GAMS files). The decoding agrees exactly with that reading.

Problems found. None affects a bound, a primal value or a closure claim.

1. **Wrong CPU time for eg_int_s.** Section 5 and the author's summary give
   "7 min (run C)", but run C took 274 s (4.6 min), as its log and the run
   table say. 401 s (6.7 min) is run A.
2. **Wrong justification for the exp cap.** Section 6 justifies "ℓ below 100
   on every box" by |γ| ≤ 46.4, |t| ≤ 4 and r ≤ 1.5. Those numbers only give
   ℓ ≤ 7·2·46.4·4·1.5 ≈ 3,900. The conclusion is still true: a
   per-coordinate bound over the root box gives ℓ ≤ 17 for every row, term
   and box of all three instances, far below the cap of 700. This affects
   only the order-2 interval replay B.
3. **Missing guard in the code.** `egbb.BB.dual_value` divides by `S.lo`
   when the combined value is negative, without checking `S.lo > 0`. If HiGHS
   returned objective-row duals summing to about 1e-300 or less, the result
   could be a large positive and wrong bound. LP dual feasibility forces that
   sum to be 1, and every leaf I re-certified passed, so this never happened.
   A guard would still be cleaner.
4. **Table 17 of Göß et al.** In the local text of the paper, the headers of
   Table 17 read "primal value | dual value". The numbers fit only the reverse
   reading (for example 3.6 | 5.8 for eg_disc_s, whose optimum is 5.76). The
   report uses the consistent reading but does not say so. It also does not
   mention that this SCIP run on eg_disc_s is marked with an asterisk for
   numerical or memory errors and excluded from the paper's evaluation.
5. **Small points.**
   - The 15–20 times tightness gain holds at ρ = 0.1 and 0.03 (19× and 15×).
     It falls to 7× at ρ = 0.01 and to about 3× at ρ = 0.003 and 0.3. "At
     medium box sizes" is correct, but the small-box ratios are worth stating.
   - The `fexp` docstring bounds |r̃ − r| by 1e-18. When x − mL1 is not exact
     (only at the reduction boundary) the bound is about 1.2e-18. The
     difference is far inside the 4e-15 slack.

In addition, I replayed part 1 of eg_disc2_s (the part with the optimum)
with the retry's interval-arithmetic model. It followed the same tree and
certified the same value (Section 6).

Verdict: **verified**. Items 1, 2 and 4 are wording corrections, which I
recommend.

## 2. Decoding and structure

**Exact; independent reader.** I downloaded the GAMS files from
`https://www.minlplib.org/gms/<name>.gms` (2026-09-30, `data/`) and wrote a
separate reader, `gms_model.py`. It turns each equation into a Python
expression with exact decimal constants, and it also extracts the term data
with regular expressions. It shares no code with `osilx`, `eg_model` or
`egdata`. `check_decode.py` (`logs/check_decode.log`)
gives:

- **Term data.** For every row of the three instances, the multiset of terms
  {(a, μ vector, γ vector)} is identical as Fractions to `egdata.Data`. The
  same holds for the scales, the linear terms, c_k, the side-row bounds
  (glo/ghi, with the sign flip of `-(…) =G=/=L= rhs`), the variable bounds
  and the integrality flags: 0 mismatches.
- **Extraction.** The extracted data reproduce the evaluated expression text
  to about 1e-47 at 50 digits.
- **Float evaluator.** `egdata`'s float evaluator agrees with the GAMS text to
  4.4e-17·(Σ|a| + 1).

Caveat: the GAMS and OSIL files come from the same MINLPLib source. This
check confirms the decoder, not the source.

**Exact or float; `check_structure.py` (`logs/check_structure.log`).** The
structural claims of Section 2 hold:

- **Shared data.** All four instances (eg_all_s too) have identical data in
  y = s·x, with the linear coefficients scaled by s, and the same y box.
- **Rows e27 and e28** have identical terms, Σ|a| = 39,666.8 and
  max |a| = 1,711.4.
- **Side rows.** e25 and e26 carry −0.45 y3 and −0.45 y2. The side bounds are
  g ≤ −0.350268824, g ≤ −0.374014485, g ≥ −346.198237 and
  g ≤ 53.8017630000004.
- **Cancellation at the eg_int_s point.** For e12, Σ|w| = 61.4 and
  g = −7.115. For e26, Σ|w| = 78.4 and the Gaussian part is −0.0829.
- **Integer combinations.** 16, 1,764 and 3,751.
- **Flat landscape.** The exploration file gives 75 and 507 combinations
  below 6 and 7 for eg_disc2_s, and 10 below 6 for eg_disc_s.

## 3. Primal points and listed values

**Exact (60 digits), independent of `osilx`/`ev.py`; `check_primal.py`
(`logs/check_primal.log`).**

| point | objvar | F(x) at 60 digits | bound/integrality violation | row violations |
|---|---|---|---|---|
| eg_int_s retry | 6.4531031593842274088 | 6.4531031593842274087 | 0 | none |
| eg_int_s p1 | 6.453103159051920 | 6.4531031590519245666 | 0 | e12 4.57e-15, e26 2.89e-16 |
| eg_disc_s retry | 5.7605396164535106058 | 5.7605396164535106057 | 0 | none |
| eg_disc_s p1 | 5.760539616453500 | 5.7605396164535166131 | 0 | e12 1.66e-14 |
| eg_disc2_s retry | 5.6421005799711067563 | 5.6421005799711067562 | 0 | none |
| eg_disc2_s p1 | 5.642100579971110 | 5.642100579971104574 | 0 | none |

- **Gaps.** Between each retry objvar and the claimed dual bound: 6.451e-9,
  5.759e-9 and 5.640e-9, all with relative gap 9.997e-10 or less. "Closed to
  1e-9 relative" holds.
- **p1 points.** F(p1) − bound is 6.12e-9, 5.76e-9 and 5.64e-9, so the claim
  that the listed p1 values are optimal within a relative 1e-9 holds. The p1
  violations quoted in the report are confirmed.
- **Listed MINLPLib values.** I fetched the three MINLPLib pages myself on
  2026-09-30 (extract in `data/minlplib_pages_extract.txt`). Every listed
  primal and dual value in the report's table matches. All three new bounds
  exceed every listed dual bound.

## 4. Mathematics and floating-point analysis (by hand)

- **Second-order model.** With u = L + Q, e^u = 1 + L + Q + L²/2 + (LQ + Q²/2)
  + u³e^{θu}/6. Since Q ≤ 0, u ≤ L ≤ ℓ, which gives the stated |R| bound.
- **Signed sums.** Because γ is common to a row, Q is the same for all 97
  terms. G, ∇ and H are then the signed sums stated, with
  H = Σ w v vᵀ + diag(2γs²)Σw.
- **Third-order alternative.** u³/6 = L³/6 + L²Q/2 + LQ²/2 + Q³/6, so the
  part beyond the quadratic is C₃ = L³/6 + LQ plus the stated fourth-order
  remainder. The bounds on |C₃| through T_ijk (multiplicities 6, 3 and 1)
  and through U_ij = γ_j s_j² Σ w v_i are correct, and so is their code
  (`egfast` and `egtm`).
- **Quadratic part.** The elementwise bound over the box and the folding of
  the gradient error into aL and aU are correct.
- **`fexp`.**
  - The Cody–Waite split is exact for |m| < 2^20 (here |m| ≤ 64,640).
  - The Horner error is at most γ₁₂e^{0.0055} ≈ 1.35e-15 relative; the
    truncation error is below 1e-19.
  - The final factors (1 ± 4e-15) dominate (1 ± u)(1 ± 2e-15) after one more
    rounding.
  - Scaling with `ldexp` is exact because x ≥ −700 keeps the result normal.
  - Only a negligible slip in the r̃ error was found (item 5 of Section 1).
- **Term data.** The error budgets for t̃ (3.1u per element), Ẽ ((d+5)u plus
  the t error), w̃ (de(1+4u) + (1.02dE + 4u)|w̃|) and the moment sums
  ((M+3)u or (M+4)u Σ|·|, valid for any order and with or without FMA) each
  cover the operations performed. The 1e-12 relative slack on all derived
  quantities covers the few-ulp errors of the midpoint constants k1 and kd.
- **Pipeline.** The weak-duality combination and the Farkas test in `egbb`
  are correct:
  - outer-rounded side bounds; c_lo for the objective rows;
  - θ only in the cut rows;
  - interval evaluation of const + coef·d;
  - division by the enclosure of Σy, except for the missing `S.lo > 0` guard
    (item 3).
- **Domain reduction.** The rounding directions and the integer rounding
  (ceil and floor of rigorous outer bounds) are correct.
- **Coverage logic of `BB.run`.**
  - A key is a valid bound for the children of a box, because the reduced box
    keeps every feasible point with F ≤ θ.
  - The cutoffs never increase, and `theta_min` is taken before any closure
    at level θ.
  - The final value is min(θ_min, UB − tol, open keys, forced keys).
  - The certified value does not depend on the incumbent being feasible; the
    gap claim does, and Section 3 checks it.
  - Splitting into parts (`array_split` of the integer range) covers all
    integer values. The part ranges in the logs are [7, 11] and [12, 15] for
    i4 (eg_disc_s), and [20, 23], [24, 27], …, [44, 47], [48, 50] for i7
    (eg_disc2_s).
  - Resume and checkpoint-splitting matter only for the superseded
    1e-6 run F of eg_disc2_s. `summary.py` handles them correctly.

**Exact; `check_fexp.py` (`logs/check_fexp.log`).** The table [TLO_j, THI_j]
encloses 2^{j/64} for all j at 80 digits. 49,049 arguments contained no
enclosure failure, with a maximum relative width of 9.0e-15. They include
both neighbours of the reduction boundary (m + ½)ln2/64 for about 5,600
values of m (every m near 0 and near −64,640, and 8% of the others),
arguments near −700 and 0, subnormal arguments and integers. The branch
x < −700 returns [0, 1e-300], which contains e^x.

## 5. Independent bounding code and the re-certification of all leaves

**Reproduced.** `record_run.py` is `egbb.BB.run` with recording lines added;
`difflib` shows only recording lines and the removed checkpoint saving. It
records every processed box (box, θ, key, bound, reduced box, kept flag,
split coordinate) and every pre-closed box. The replays reproduce the
original logs exactly:

| replay | processed boxes | statistics | certified value |
|---|---|---|---|
| eg_int_s, run C | 56,189 | `lp_close` 343, `farkas` 5, `fbbt_close` 57, `row_close` 27,690 | 6.4531031529331155 |
| eg_disc_s, run E part 0 | 62,779 | identical to `disc9_p0.log` | 5.7605396106949955 |
| eg_disc_s, run E part 1 | 55,973 | identical to `disc9_p1.log` | 5.760539610694994 |
| eg_disc2_s, run G parts 0–7 | 119,873; 134,607; 178,085; 223,449; 222,097; 155,279; 82,919; 36,521 | identical to `disc2_9_p*.log` | 5.642100574331458 each |

**Coverage, exact bookkeeping; `verify_tree.py`.** For every recorded tree:

- **Root and parts.** The root box contains the exact domain (continuous ends
  rounded outward, integer ends exact) or the stated part of the integer
  range.
- **Reduced boxes and children.** Every reduced box lies in its box and has
  integral integer ends. Every split is valid: integer coordinates split
  into [a, m] and [m+1, b] with a ≤ m < b; continuous coordinates bisected
  with a shared face. I recomputed the children from the reduced boxes.
- **Every box accounted for.** The multiset of generated boxes (the root plus
  all children) equals the multiset of popped boxes. No box was lost or
  duplicated, none was left open, none was forced closed as tiny, and no box
  was pre-closed.
- **Leaves.** It follows that the leaves cover the domain: the closed boxes
  (taken whole, not only their reduced part) and the slabs removed by domain
  reduction. The slabs are decomposed disjointly, and integer slabs start at
  the next integer.

**Independent rigorous certification; `indep_cert.py`.** It shares no code
with `egfast`, `egtm`, `egbb`, `kan_iv` or `ia`, and it reads the model data
from the GAMS files.

- **Natural enclosure** with generous error bounds:
  - t ranges widened by 1e-15(|μ| + |sx| + |t|), where about 2u is needed;
  - exponent sums widened by 1e-14 Σ|γ|t², where about 9u is needed;
  - libm exp taken to be within 1e-14 relative;
  - 97-term sums widened by 1e-13 Σ|·|, where 96u is needed.
- **Taylor model** at the box centre with signed moment sums, and a remainder
  that I derived differently from the retry. For φ(τ) = exp(τa + τ²b), with
  a = L(d), |a| ≤ ℓ and b = Q(d) ∈ [−q, 0]:
  - φ''' = φp(p² + 6b) and φ'''' = φ(p⁴ + 12bp² + 12b²), where p = a + 2bτ
    and |p| ≤ ℓ + 2q;
  - order 2: |R₂| ≤ e^ℓ[(ℓ+2q)³/6 + q(ℓ+2q)];
  - order 3: the signed cubic a³/6 + ab plus
    |R₄| ≤ e^ℓ[(ℓ+2q)⁴ + 12q(ℓ+2q)² + 12q²]/24.
  - My bounds are slightly weaker than the retry's.
- **Certificates.** Each is checked in exact rational arithmetic from the
  float data: row bound, side-row infeasibility, LP weak duality with scipy's
  HiGHS multipliers, and a Farkas test with the objective cuts at θ*. A box
  without a certificate is bisected (integers at integers) up to depth 24.
- **Target.** Every leaf is checked against the final claimed bound θ*. That
  is stronger than needed, because the cutoff in force when a leaf was closed
  was never below θ*.
- **Controls; `negative_control.py` (`logs/negative_control.log`).**
  - Negative control: the certifier must refuse any box around the primal
    point x* with θ = F(x*) + 1e-6 or F(x*) + 1e-9. It refused all 24
    (3 instances × 2 targets × 4 box sizes).
  - Positive control: with θ = claimed bound − 1e-6 it certified the boxes
    of relative size 1e-4 to 1e-8. The box of size 1e-2 exceeded the depth
    limit of 12 used in the control.
- **Sampling check of my models and the retry's; `test_models_indep.py`.**
  Reference values in long double (error about 1e-17·Σ|w|). Test points: the
  centre, the corners, random points, and local extremes of
  g − β·(x − c) found by L-BFGS-B for 6 rows × 2 signs per box. Boxes: 16
  families per instance (relative size 0.3 to 1e-7, near the optimum and
  uniform, integers fixed or relaxed), 5–6 boxes each.
  - All margins were positive for both models on all three instances.
  - The smallest normalised margins were 1.2e-13 (mine) and 2.4e-14 (the
    retry's), at boxes of size 1e-7.
  - Retry minus my aL had a median of about 1e-12 on small boxes, so the two
    models agree closely where it matters.

Results against θ* (`logs/verify_*.log`):

| tree | leaves (closed boxes + slabs) | certified | failures | smallest LP-certificate margin over θ* |
|---|---|---|---|---|
| eg_int_s run C | 28,095 + 5,290 | all 33,385 | 0 | 7.7e-11 |
| eg_disc_s run E part 0 | 31,390 + 14,833 | all 46,223 | 0 | 6.6e-5 |
| eg_disc_s run E part 1 | 27,987 + 12,586 | all 40,573 | 0 | 2.0e-9 |
| eg_disc2_s run G part 1 (i7 ∈ [24, 27]) | 67,304 + 68,013 | all 135,317 | 0 | 1.0e-9 |
| eg_disc2_s run G part 0 (i7 ∈ [20, 23]) | 59,937 + 57,240 | sample of 13,699 | 0 | 2.4e-4 |
| eg_disc2_s run G part 2 (i7 ∈ [28, 31]) | 89,043 + 89,664 | sample of 19,696 | 0 | 6.6e-4 |
| eg_disc2_s run G part 3 (i7 ∈ [32, 35]) | 111,725 + 109,393 | sample of 23,916 | 0 | 3.5e-4 |
| eg_disc2_s run G part 4 (i7 ∈ [36, 39]) | 111,049 + 99,316 | sample of 22,925 | 0 | 6.7e-4 |
| eg_disc2_s run G part 5 (i7 ∈ [40, 43]) | 77,640 + 67,583 | sample of 16,281 | 0 | 9.9e-4 |
| eg_disc2_s run G part 6 (i7 ∈ [44, 47]) | 41,460 + 35,901 | sample of 9,509 | 0 | 1.1e-3 |
| eg_disc2_s run G part 7 (i7 ∈ [48, 50]) | 18,261 + 10,832 | sample of 4,650 | 0 | 1.0e-2 |

For eg_int_s and eg_disc_s, therefore, every leaf of the reported trees has
been certified twice: by the retry's code and by mine. Together with the
coverage check, this gives an independent certificate of both bounds; its
only shared inputs are the tree shapes and the model data. (The LP
multipliers are not shared: my code takes its own from scipy's HiGHS.) For
eg_disc2_s, the same holds for part 1, which contains the optimum.

In parts 0 and 2–7 of eg_disc2_s, the coverage is checked completely but the
leaves only by sample. The unsampled leaves rest on the retry's fast model
alone. The risk there is small, for two reasons:

- In each part I certified the 2,000 closed boxes with the smallest retry
  bound. The smallest margin of any of my LP certificates in those parts was
  2.4e-4 or more, so the closures there are not close to the cutoff. The
  unsampled closed boxes have retry bounds at least as large. This argument
  does not rank the domain-reduction slabs; they are covered only by the
  random sample.
- My independent code never disagreed with a closure of the retry, over all
  366,174 leaves I certified.

## 6. Interval-arithmetic replay of eg_disc2_s

**Reproduced with the retry's interval model.** The report did not replay
eg_disc2_s with the interval model (`EGMODEL=ni`). I ran part 1 of run G
(i7 ∈ [24, 27], the part with the optimum) that way:
`EGMODEL=ni python3 egbb.py eg_disc2_s 1e-9 17000 … - 1 8`
(`logs/disc2_9_ni_p1.log`). Result:

- the same tree as the fast run: 134,607 boxes, with identical statistics
  (`lp_close` 918, `farkas` 49, `fbbt_close` 2,459, `row_close` 63,878);
- the same certified value, 5.642100574331458;
- 5,755 s, against 1,515 s for the fast run.

The report's statement that eg_disc2_s has no interval replay is therefore
now out of date for the part that contains the optimum. The other seven
parts were not replayed in interval arithmetic.

The retry's own interval replays B, H and I are consistent with their logs:

- run B: 66,423 boxes, as run A;
- run H: 56,189 boxes, as run C, with identical statistics;
- run I: 62,779 and 55,971 boxes, against 62,779 and 55,973 for run E.

All three end with the claimed bounds.

## 7. Other claims

- **Ablations.**
  - The four ablation logs match the table in Section 6 of the report: full
    run 55,903 boxes in 591 s; without domain reduction 57,499 boxes in
    583 s; order 2 only 66,141 boxes in 615 s; without the LP stopped at
    125,375 boxes in 900 s with bound 6.452656 and 30,720 boxes open.
  - The LP multiplier of e26 relative to e12 on a box of half-width 1e-4
    around the eg_int_s optimum is 22.27 (my run of `BB.lp_bound`), as
    stated.
- **Tightness table.** The table in Section 3.1 of the report matches
  `cmp_bounds.log`; see item 5 of Section 1.
- **Sampling-check logs.** `test_fexp.log`, `test_decode.log`,
  `test_models.log` and `test_bound_final.log` contain what the report says:
  5,595 qualifying points and 1,680 comparisons.
- **Compute.**
  - eg_disc_s: 726 + 650 s = 23 min.
  - eg_disc2_s run G: the eight part times sum to 12,378 s (3.4 h), and the
    longest part takes 2,258 s (38 min).
  - Run F: 4,408 + 12,661 s = 4.7 h.
  - eg_int_s: see item 1 of Section 1.
- **Literature.**
  - Göß, Burlacu and Martín, J. Glob. Optim. 94 (2026) 951–996, local copy:
    SCIP 8.1 and Gurobi 11, 8 threads, 4 h. Table 17 for the original
    models: eg_int_s solved by SCIP in 9,085.1 s (6.5 / 6.5); eg_disc_s
    3.6 / 5.8; eg_disc2_s −1.1 / 6.3 (see item 4 of Section 1).
  - arXiv 2603.16505 ("Clash of MINLP Relaxations: Piecewise Linear vs.
    Global Parabolic") exists. Its HTML text has no eg_* instance.
  - The local Cristofari et al. copy lists only primal values (6.4531,
    5.7605, 5.6421, 7.6578).
  - My own web search ("eg_disc2_s" OR "eg_disc_s" MINLP dual bound global
    optimum) found only MINLPLib pages, old GAMSlinks BONMIN logs (local
    solver, no valid global bound) and the papers above. No closure of
    eg_disc_s or eg_disc2_s was found.
  - The report's novelty statement is suitably qualified. An unsuccessful
    search does not establish novelty.

## 8. Commands run

All targeted, and run from `reviews/eg-retry-review-checks/` unless noted,
with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1` and `timeout`.

- `curl` of `https://www.minlplib.org/gms/<name>.gms` (kept in `data/`) and
  `https://www.minlplib.org/<name>.html` for the three instances (kept only
  as the extract `data/minlplib_pages_extract.txt`).
- `python3 check_decode.py` (`logs/check_decode.log`): 0 exact mismatches per
  instance; extraction versus text at most 1.1e-47; float evaluator at most
  4.4e-17·(Σ|a| + 1).
- `python3 check_structure.py`, `python3 check_primal.py`,
  `python3 check_fexp.py`: results in Sections 2–4 (`logs/check_*.log`).
- `python3 test_models_indep.py <name> 6|5 <seed>` for the three instances
  (`logs/test_models_indep_*.log`).
- `python3 negative_control.py` (`logs/negative_control.log`, Section 5).
- `python3 -c "import indep_cert; …check_libm_exp()"`
  (`logs/check_libm_exp.log`).
- `python3 record_run.py eg_int_s 1e-9 3600 logs/rec_int.npz`;
  `python3 record_run.py eg_disc_s 1e-9 5400 logs/rec_disc_p$k.npz $k 2` for
  k = 0, 1; `python3 record_run.py eg_disc2_s 1e-9 7000
  logs/rec_disc2_p$k.npz $k 8` for k = 0..7 (`logs/rec_*.log`).
- `python3 verify_tree.py <rec.npz> <name> <theta*> 1.0` for eg_int_s, both
  eg_disc_s parts and eg_disc2_s part 1; `… 0.1 <k>` for the other eg_disc2_s
  parts (`run_disc2_parts.sh`; `logs/verify_*.log`).
- From `open-instances-wave3/eg/retry/`: `EGMODEL=ni python3 egbb.py
  eg_disc2_s 1e-9 17000 <review>/logs/disc2_9_ni_p1.npz - 1 8`
  (`logs/disc2_9_ni_p1.log`), and a one-off call of `BB.bound` and
  `BB.lp_bound` for the e26 multiplier.
- Web: arXiv abstract pages 2603.16505 and 2407.06143, the HTML text of
  2603.16505, and one web search (Section 7).

Compute used by this review: about 2.4 CPU-hours for the eleven tree
recordings, 1.3 CPU-hours for the leaf certifications, 1.6 CPU-hours for the
interval replay, and under 0.5 CPU-hours for everything else. At most about
8 processes ran at once, for about 2 hours of wall time.

The tree recordings (`logs/rec_*.npz`, 53 MB in total) were deleted after
the checks. `record_run.py` regenerates them deterministically: the replays
reproduce the original logs exactly. The logs keep every number quoted
here.
