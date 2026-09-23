# Stage 2 independent review 1

Reviewed 2026-09-13. Scope: `03-soundness.tex`, `04-implementation.tex`, the integrated Sections 1–4, current author report, analytic validation script and JSON, and corresponding checker source. No manuscript or checker source was edited.

## Verdict

**No major issue found.** The proofs establish their stated conditional soundness results, including solution-conditioned inference and unconditional bound transfer. The implementation description distinguishes sufficient recognition from general convexity, complete artifact checking from proof-system completeness, and mathematical premises from unmechanized software trust. Two minor precision corrections are needed.

## Findings

### R1-1 — Minor: explicitly restrict the even-power index to integers

Location: `sections/04-implementation.tex:40`, Table `tab:composition`.

The row currently says `v^{2k}, k >= 1` without declaring `k` integral. The condition must be `k` a positive integer when the base can be negative. For example, `k=3/2` gives the odd power `v^3`, which is not convex for an arbitrary affine base across zero. Merely using the letter `k` is not an explicit hypothesis, particularly next to rows allowing rational exponents.

Evidence: `_pow_cert` in `certify/convexity.py` checks `p.denominator == 1`, even numerator, and `p >= 2` for this rule.

Correction: write `k in Z, k >= 1` or declare immediately in the table caption that `k` is a positive integer. This is a missing qualifier in the presentation; the implementation already has the right test.

### R1-2 — Minor: make the domain of the quadratic equivalence explicit

Location: `sections/04-implementation.tex:49`, “convexity is equivalent to Q positive semidefinite”.

That equivalence concerns global convexity on the ambient real space (or a full-dimensional box). The paper otherwise permits fixed coordinates and convexity restricted to a box, where necessity can fail: `q(x,y)=-x^2+y^2` is convex on `{0} x [-1,1]` although its ambient matrix is indefinite.

Correction: write “global convexity on R^n is equivalent to ...; hence this gives a sufficient test on the certified box.” The existing exact fixed-variable elimination can be mentioned if useful, but no algorithm change is needed. The PSD lemma and its proof are correct.

## Proof and implementation assessment

1. **Propagation.** The coefficient signs, use of lower rest bounds for upper rows and upper rest bounds for lower rows, and directed integer rounding are correct. The finite-sequence induction proves preservation without assuming a fixed point. The 20-sweep implementation is accurately described. Empty-box detection is distinguished from a public infeasibility certificate.

2. **Support correction.** I checked every coordinate case. Because `z` lies in the box, the two displacement signs give the stated rational enclosure maximum. On an upper half-line only a nonnegative residual is admissible; on a lower half-line only a nonpositive residual is admissible; a free coordinate requires exactly zero residual. The interval implementation in `_verify_given_cut` encloses this calculation with the same signs. It includes linear-only variables and omitted cut slopes. The finite support-vector premise is explicit and sufficient.

3. **Boundary derivatives.** The segment-derivative argument in Section 4 is correct for finite convex functions on the segment. Its warning about coordinate derivatives is mathematically material: the axis derivatives of `-sqrt(x*y)` at the origin do not give a supporting vector. I inspected `SafeCutter`, its finite-endpoint checks, and `iv_eval`; quotient singularities and unsupported sign derivatives are refused in the stated examples. The manuscript appropriately treats correct symbolic differentiation/relative-domain semantics as part of the trusted implementation, rather than claiming that interval finiteness by itself proves support. No accepted nonsupporting derivative counterexample was found in this review; this is not a formal theorem for SymPy or the expression implementation.

4. **Discrete invariant.** I independently matched all five admitted rules against `_derive` and `_integral_form` in `vipr.py`. The incumbent-conditioned set is the correct domain for `sol`. All supplied points are checked against master rows and integrality; nonzero inference terms retain dependencies; multiplication signs and dominance are checked. The unsplit dependency union correctly retains cross-branch assumptions. No requirement that a conclusion actually use its matching branch assumption is needed for soundness.

5. **Unconditional bound.** The proof uses the best supplied witness, which belongs to the cutoff set. This first proves `beta <= b_M`; all points outside that set have still larger objective. Thus the proof is valid without assuming an optimizer exists. With no supplied solutions the set is the entire master. The explicit empty-solution requirement for infeasibility and rejection of the stronger integer-objective cutoff agree with code.

6. **Transfer and primal completion.** The extension preserves original coordinates and assigns exact objective/constant auxiliaries. It proves the correct feasible-set inclusion and objective identity. Sign normalization, affine constants, lack of attainment assumptions, and the independent original-model primal witness are handled correctly.

7. **Curvature recognition.** Completing the square/Schur elimination proves the PSD test, including zero pivots. The homogeneous PSD matrix yields a real norm factorization, with no unwarranted rational factorization claim. The monomial Hessian identity, weighted Cauchy–Schwarz concavity test, and one-positive-exponent Schur complement are correct. Continuous boundary extension is properly restricted. The linear-fractional second derivative and sign classification are correct. The two findings above concern presentation of hypotheses, not incorrect implemented rules.

8. **Checking boundary.** The manuscript matches optional historical semantics/hash fields, mandatory complete replay, byte-identical regenerated LP, stricter-than-general-equivalence master matching, all-suffix proof checking, inferred assumption sets, lifetime verification, and two-pass memory accounting. It explicitly assumes stable files; ordinary before/after hashing is not represented as protection against adversarial replacement races. Search budgets and proof completion time are separated.

## Independent execution

- Reran `process/stage02-analytic-validation.py` in the solver-lab environment. All exact identity checks passed, and the emitted seven source hashes matched the recorded JSON. The bundled complete certificate again gave lower bound `1/4`, 11 nonlinear cuts, 39 derivations, and the same proof statistics.
- Ran the existing targeted `test_vipr.py`, `test_independent_semantics.py`, and `test_review_convexity.py` suites: **87 tests passed**. These exercise discrete proof contracts, unbounded/semantic boundaries, and recognizers; they are not a substitute for the mathematical proof.
- Independently rederived the rounded-tangent exclusion and correction, monomial Hessian argument, and linear-fractional derivative rather than relying solely on the script.
- Did not repeat large-proof benchmark replay, run new solver performance experiments, or claim complete formal verification.

## Later-stage obligations

Keep subsequent formalization claims limited to actually mechanized theorems and their assumptions. The final experiments and artifact package must substantiate reliability/reproducibility and distinguish historical replay from new generation. Those sections are deliberately not yet part of this review. The integrated abstract can be updated from its present prospective wording during final manuscript integration.

After the two minor hypothesis clarifications, this review finds no reason to repeat a major-issue Stage 2 cycle.
