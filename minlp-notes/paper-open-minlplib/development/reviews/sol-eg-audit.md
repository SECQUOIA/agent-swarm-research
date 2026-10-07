# Independent review of the eg exp/power audit

Date: 2026-10-04. Reviewer: Codex review sub-agent. Repository paths below are relative to `/workspace/minlp-notes`. Review scripts, copies, rerun results and logs are under `/tmp/sol-eg-audit-review/`.

**Verdict: VERIFIED for the recorded dual bounds**, under binary64 round-to-nearest-even arithmetic with gradual underflow, correctness of the certificate-checking code and its runtime primitives, and faithful execution and retention of the recorded run. The verified decimal bounds are **6.4531031529331155**, **5.760539610694993**, and **5.642100574331458**. The audited eg_disc_s run actually checks the stronger exact decimal **5.760539610694994**.

There are **no blockers or major issues for these three bounds**. Four minor issues below need correction before publishing the lemma verbatim. My verdict uses the domain restrictions and the numerical clarifications supplied in this review; it does not endorse every intermediate claim in the present prose. I did not rely on the earlier checker's verdict.

## Numbered issues

1. **Minor — the general power-auditor proof omits underflow of its tolerance product.** In `development/eg-audit/cert/auditor.py:210` and Lemma P in `development/eg-lemma-A1.md`, the step `fl(CP*z) <= CP*z*(1+u)` needs a normal product. For `x = 2^-250`, `k = 4`, `z = 2^-1000`, but `CP*z` is approximately `9.02179694e-316`, which is subnormal. Normality of `z` alone is insufficient. The general proof on the entire advertised interval therefore has a gap; my tests did not demonstrate a false acceptance.

   This does **not** affect the certificates reviewed here. From the exact root bounds, scales, positive `dt`, nonzero-radius spacing and length scales, I obtained conservative lower bounds on nonzero `p` of `2.03e-33`, `1.72e-34`, and `2.03e-33`, respectively. `tau > 2.99e-16`, and `S` is 0.1 or 1. Thus every nonzero `CP*z` on their power paths is normal by a very large margin; zero is checked exactly. Repair the general statement by restricting the floating comparison to a range where its tolerance product is normal, or include its additive underflow error and adjust the acceptance test. A statement restricted to the actual eg arguments also suffices for this paper.

2. **Minor — some intermediate exp claims and tolerance displays are stronger than the proof supports.** The natural-enclosure table at lemma lines 171–172 labels `elo` and `ehi` themselves as directed exp endpoints. Under hypothesis (E) with exact epsilon `1e-14`, their factors `1 ± 1e-14` alone do not ensure this. For example, an (E)-compliant hypothetical result at `x = -4.608392048642763` gives `elo = 0.009967833219752614`, about `7.24e-17` relatively above the exact exponential. An (E)-compliant result at `x = -0.06427946257864381` gives `ehi = 0.9377428988601503`, about `2.74e-17` relatively below it. These are counterexamples to the intermediate properties, **not** to the final natural enclosure. The subsequent term padding makes the full chains sound. Describe the intermediate quantities as approximations whose errors are covered by the chained term bounds.

   Also, the quoted natural threshold `1.9548e-14` rounds upward from approximately `1.9547918011776054e-14`. The conservative exact `dw` intercept calculation gives approximately `1.0777955395074846e-14`, rather than an exact guarantee through `1.0778e-14`. Label these as approximate thresholds, or round downward. Neither discrepancy threatens the enforced exact epsilon `1e-14`. The `el` table's narrower claim of a deficit at most `u` should also use its stated conservative `3u` allowance; the remainder padding absorbs that allowance.

3. **Minor — historical bit identity is established for eg_disc2_s, not for all three original runs.** `compare_audit.py` correctly documents that only logs survive from the original eg_int_s and eg_disc_s independent certifications. Matching progress statistics, final counts and the smallest printed margin does not establish identity of every historical leaf, multiplier or margin. Consequently, the unrestricted final sentence of lemma Section 5, “the saved certificate is the audited certificate,” needs qualification.

   For eg_disc2_s, every saved per-leaf result field named by the comparison is byte-identical across all 38 chunks. For eg_int_s and eg_disc_s, say that a complete audited certificate was obtained and its historical logs reproduced apart from timings. Coverage and exact final tests establish those bounds directly, so historical bit identity is unnecessary. My own new eg_int_s rerun matches the retained **audited** results byte for byte, which does not recover the missing original results.

4. **Minor — state the domain restriction used by Lemma A1.** Its statement currently admits an arbitrary float box with `lo <= hi`, but the proof uses these instances' root-domain bounds: endpoints at least 0.25, positive `Sc`, bounded half-widths, length scales and term values. The exp cap and the underflow/radius arguments also use those bounds. State that the lemma applies to boxes contained in the outward-enlarged roots used for these instances, including recursively split pieces, with the stated assertions satisfied. Coverage and splitting establish this restriction for the recorded run. This is a scope correction, not an additional empirical accuracy assumption. Section 6's “full run has not been launched yet” is also stale and should refer to the completed retained run.

## Code changes and call coverage

I read the original and audited sources and ran direct unified diffs, rather than relying only on `# AUDIT` markers. The changes in `indep_cert_audit.py` add the audit object, wrappers, begin/end calls and flags. Each wrapper computes the original `np.exp(x)` or `x ** k` expression, checks its result without modifying its input or result, and returns that same array. Mechanically undoing the wrappers recovers all 382 nonblank lines of the original certifier. The unchanged model reader, GAMS files, original certifier copy and recording dependencies are byte-identical to their research-tree sources.

The margin-certifier diff changes imports and carries violation flags through the original recursion. It does not change `_one`, the exact tests or splitting decisions. Parent flags are preserved and ORed with every child's flags. The shared `S ** 2` checks use `perbox=False`, correctly flagging the whole affected batch. The recheck-driver changes add optional batch selection, completed-leaf bookkeeping, audit output and atomic saving. The recorded complete jobs have `batches == "all"`, so the selection feature removes no leaf.

I used text searches and an AST call inventory over the certification modules. There are four exp sites (`nat_Elo`, `nat_Ehi`, `tay_E0`, `tay_ell`) and six power-site labels (`tau2`, `tau3`, `s2`, `p2`, `p3`, `p4`). Every occurrence feeding an enclosure is wrapped, including repeated powers and powers of `S`. There is no `np.log`, scalar log, sqrt or other unaudited transcendental in this enclosure path. `K1`, `KD`, squares written as products, reductions and divisions use basic arithmetic.

Both einsums use the installed NumPy 2.5.1 default `optimize=False`; I inspected its dispatcher, which sends this path directly to `c_einsum`. Their sums of two- and three-factor products are covered by the arithmetic error bounds. They do not request log, sqrt, exp or power transformations. Correct implementation of these arithmetic reductions remains part of code/runtime correctness.

Some library calls occur outside the trusted enclosure path. `gms_model.lhs`, `eval_terms` and `check_libm_exp` contain mpmath/NumPy exp calls, but the driver never invokes them. HiGHS proposes multipliers; the certificate is checked independently with Fractions. The recording/search code also uses unaudited numerical functions, but its leaves are only proposed boxes, whose coverage and bounds are rechecked independently.

The auditor itself has scalar float powers. Its `2.0 ** (j/64)` values are **initial table guesses**: exact integer comparisons certify the final entries, regardless of seed accuracy. I independently checked the loaded `YTINY`, `PLO` and `PHI` constants against the exact dyadics `2^-1020`, `2^-250` and `2^250`. These constant uses introduce no remaining accuracy assumption for this recorded host/run. Encoding or asserting those dyadics explicitly would make this point clearer.

## Independent numerical derivation

The exp enclosure is sound on its stated range. The tail of `sum 1/(k*2^k)` after term 400 is bounded by `1/(400*2^400)`. I independently constructed a tighter rational bracket using `ln(2) = 2*atanh(1/3)` and proved that bracket lies inside the auditor's bracket. This also checked the reduction-constant error. The table checks were repeated as integer numerator/denominator power comparisons.

The small integer `m` and the 36-bit dyadic `L1` make `m*L1` exact. The three reduction errors give the stated `DR` after bounding `s` by the computed `r` and `p2`. The Horner error uses 14 rounding operations, exact coefficient errors and the degree-7 Taylor tail. Its additive underflow allowance is sufficient for this short polynomial. The computed constants are:

| quantity | value, approximately |
|---|---:|
| `DL` | `1.5746795524851787e-30` |
| `DR` | `1.2212462822687658e-18` |
| `EH` | `1.562884526319768e-15` |
| `RHO_H` | `1.5715279299344097e-15` |

The exact `CLO` and `CHI` inequalities absorb polynomial/reduction errors and both product roundings. Exact series bounds establish normal scaling at -708 and absence of overflow at 709. The power-of-two scaling is therefore exact. The final `FUP`/`FDN` inequalities prove the acceptance implication, rather than merely testing whether the vendor result lies inside an approximate enclosure. For arguments below -708, the check proves the **absolute** condition `0 <= y <= 2^-1020`; it does not claim a relative exp error bound there. That condition suffices for the discarded Taylor/lower-exp values and the absolute natural upper padding.

For powers on the actual eg arguments, the repeated-product reference has relative error at most `(1+u)^3 - 1`. A passing comparison forces the candidate and reference within a factor of two. Their subtraction is then exact by Sterbenz, and the exactly checked `CP` inequality implies relative error at most `1e-14`. Issue 1 concerns extending that proof to much smaller arguments, not its application here.

I re-derived the second- and third-order remainder formulas and followed the data, exponent, moment, gradient, Hessian, quadratic and remainder errors through the final affine endpoints. The sums-of-products counts `gamma_97`, `gamma_98`, `gamma_99` and the cubic accumulation allowance are conservative. The power deficits in `e2/e3`, `q/U2` and `R2/R4` are covered by the existing slack. In particular, the final remainder factors cover the small possible deficits in `AW`, `el` and `U2`; those intermediate quantities need not individually be exact upper bounds.

I checked the near-tight natural chains with exact binary64 constants. Their minimum epsilon limit is approximately `1.9547918011776054e-14`. For `dw`, a rigorous upper error bound for nonzero `w` is

`|w| * [exp(dE)/((1-u)^2*(1-eps)) - 1]`.

An exact Taylor-series upper bound at `dE = 1e-6` bounds this by an affine function of `dE`. Even after four conservative padding-rounding factors, the code's intercept exceeds the necessary intercept by a factor `1.07610565`, and its slope exceeds the necessary slope by `1.01999949`. This avoids relying on the prose's abbreviated first-order expression. The enforced epsilon is exactly `Fraction(1, 10**14)` for both exp and powers.

The root-wide bounds were checked independently from the GAMS data and retained outward root endpoints. All three instances have conservative `ell < 16.964`, `q < 5.136`, `|t| < 3.000000000001`, `|A| < 1712`, and `|gamma| < 46.4`. No positive-exp cap binds. For the underflow bookkeeping, one can use a looser amplification bound of `1e14`, rather than the note's terse `1e8`: inspect the separate moment/cubic and remainder paths, with inflated `r < 16`, `|K1| < 93`, `p < 28`, and `exp(ell) < exp(17)`. There are fewer than `1e6` contributing operations per row output. The resulting total additive underflow allowance is below `3e-304`, still below the `1e-300` absolute padding. This covers basic-operation underflows separately from the explicit exp cutoff cases and the audited powers.

## Run comparison, coverage and reruns

I reran the copied `compare_audit.py`, including all coverage proofs. It independently reproduced:

`RESULT: PASS (complete run; 1234542 leaves compared or checked; 63017129222 exp/power results audited, 0 violations)`.

The totals are 33,385 eg_int_s leaves, 86,796 eg_disc_s leaves, and 1,114,361 eg_disc2_s leaves. They comprise 1,933,502 certified pieces. I additionally checked all 41 result files against their logs for the intended exact-decimal target and successful completion. Exp counts equal pieces times 28 times 97 at every site. Power counts also agree: `tau2` occurs three times, `tau3` twice, and each `p` power once per term per piece; the shared `s2` count is positive and even. Every saved success flag is true, every audit flag is false, and every violation/example collection is empty.

The guillotine proof is an exact coverage proof, not a volume or random-point argument. At each cut, the two child node domains cover the parent domain, with a shared continuous face or consecutive integer endpoints. A terminal leaf must contain its assigned node domain. Induction therefore proves coverage even if a proposed cut leaves a gap: such a gap prevents a terminal containment check from succeeding. Removing an actual eg_int_s leaf made this proof fail in my negative control.

Each part's chunk indices are exactly `0 .. n_leaves-1`, without repetitions or omissions. Continuous roots contain the exact GAMS intervals. The integer part check is sufficient for these instances because only one integer coordinate changes between roots: i4 for eg_disc_s and i7 for eg_disc2_s. All other integer coordinates retain their full ranges. Thus the parts cover the Cartesian domain; the script's marginal tiling test should not be generalized to arbitrary partitions on several changing coordinates.

My independent reruns produced:

| rerun | result |
|---|---|
| eg_int_s recording | 56,189 processed boxes; every saved recording field byte-identical to the retained audited recording; about 144 s |
| eg_int_s full independent certification | 33,385/33,385 leaves, 38,173 pieces, 1,244,140,388 audited results, zero violations; about 174 s |
| eg_disc2_s part 7, its complete single chunk | 29,093/29,093 leaves, 48,287 pieces, 1,573,780,848 audited results, zero violations; about 283 s |

Both certification outputs match **every saved field except elapsed time** in the retained audited outputs, including decisions, boxes, margins, statistics and audit counts. The part-7 retained output also matches the original unaudited certificate through the full comparison. The minimum LP margins reproduced as `7.687113138246043e-11` and `0.0021692888261855003`, respectively.

The supplied auditor test suite passed, including its 32,010 high-precision enclosure checks. The supplied boundary suite passed on 141,706 hard arguments. My separately written check used 512-bit references on 84,640 arguments formed from high-precision reduction half-points, binary exponent boundaries and their float neighbors; all enclosures held, with maximum relative width approximately `4.3933e-15`. Exact power tests covered 16,005 bases for each exponent and rejected the first float outside each side of the allowed band, including bases near `2^-250`. These numerical tests corroborate the analytical proof; mpmath is not a premise of it.

The end-to-end negative tests also passed. They detected injected errors at every exp/power site tested, retained a child's error on its owning original leaf, and flagged all 64 boxes for a shared `S ** 2` violation. Small in-band perturbations were accepted.

## Trust-base statement for the paper

Suggested wording:

> For the stored models with decimal literals interpreted as exact rationals, the dual bounds are certified by a complete independent leaf check with exact rational final tests and an exact coverage proof. The proof assumes IEEE-754 binary64 arithmetic with round-to-nearest-even and gradual underflow, correct implementation of the model reader, numerical bounds, auditor, exact arithmetic and coverage checker, and faithful execution and retention of the reported run. Every exp and integer-power result used in the enclosures was checked against a mathematically proved enclosure or error test. No accuracy guarantee for NumPy, libm or Intel SVML exp/pow is assumed. The LP solver supplies proposed multipliers whose validity is checked exactly.

“Correct implementation” includes Python integer/Fraction arithmetic and float conversion, NumPy's basic arithmetic/reductions, comparisons, array indexing, adjacent-float operations and the integer/bit operations used for scaling. These programs and their proofs have been reviewed, not formally verified. The recorded-run premise includes that the retained inputs, outputs and zero-violation counts came from the reviewed code with the stated targets. The author search code, solver optimality claims, sampled vendor accuracy and high-precision reference tests are not premises of the dual theorem. Primal feasibility and reported gaps require their separate certificates and are outside this review.

## Targeted commands and retained review evidence

All repository Python code was copied before execution. No script was imported or run in place. All generated files stayed under `/tmp/sol-eg-audit-review/`, except this requested review. At most four single-threaded processes ran concurrently; `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1` and `PYTHONDONTWRITEBYTECODE=1` were set for numerical runs. No commits, project-wide verification or CI inspection were performed.

The commands actually run were the direct source diffs and searches described above, and, with `A=/tmp/sol-eg-audit-review/audit` and `EG_AUDIT_R=/workspace/minlp-notes/research-20260929` where needed:

- `python3 $A/tests/check_copies.py` — passed; `check_copies.log`.
- `python3 $A/compare_audit.py` — complete coverage/comparison passed; `compare.log`.
- `python3 $A/tests/test_auditor.py 200000` — passed; `test_auditor.log`.
- `python3 $A/tests/boundary_check.py` — passed; `boundary_check.log`.
- `python3 $A/tests/test_negative.py $EG_AUDIT_R/publication/eg-recheck/rec/rec_disc2_p1.npz /tmp/sol-eg-audit-review/negative` — passed; `test_negative.log`.
- `python3 $A/cert/recheck_audit.py $A/out/rec/rec_int.npz eg_int_s 6.4531031529331155 0 1 /tmp/sol-eg-audit-review/rerun/int.npz` — passed; `rerun/int.log`.
- `python3 $A/cert/recheck_audit.py $EG_AUDIT_R/publication/eg-recheck/rec/rec_disc2_p7.npz eg_disc2_s 5.642100574331458 0 1 /tmp/sol-eg-audit-review/rerun/disc2_p7_c0.npz` — passed; `rerun/disc2_p7_c0.log`.
- `python3 $A/record/research-20260929/reviews/eg-retry-review-checks/record_run.py eg_int_s 1e-9 20000 /tmp/sol-eg-audit-review/rerun/rec_int.npz` — passed; `rerun/record_int.log`.
- Reviewer scripts `independent_numeric.py`, `source_and_range.py`, `verify_artifacts.py` — final runs passed; corresponding `.log` files. `prose_counterexamples.py` records issue 2. An initial deliberately conservative global lower bound in the reviewer's range script failed its own assertion; replacing it with the appropriate per-coordinate bound yielded the reported proved bounds.

`input-sha256.txt` identifies the copied certification sources, GAMS files and retained result/recording inputs. The full audit itself was inspected and compared, not rerun in full during this review. The independently repeated computations are exactly those listed above.
