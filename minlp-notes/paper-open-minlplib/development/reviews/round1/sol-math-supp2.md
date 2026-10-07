# Mathematical review of supplement S1.6–S1.9, S2 and S5

**Verdict: major revision for the assurance of the KAN lower-bound implementation; otherwise mathematically sound under the stated computational trust bases, subject to the minor corrections below. No blocker and no refutation of a reported numerical bound. The three eg primal points are proved exactly feasible for the specified OSIL files with exact decimal data.**

The major issue is a missing arithmetic-domain justification in KAN path (I), not the exact KAN infeasibility result or the construction of points of R_P. A concrete test shows that its quadratic bounding routine is unsafe on some subnormal inputs allowed by IEEE binary64. I have not established that such an input occurs in a recorded KAN search. The previous review established exact halving in one complete n4 search, not all six searches. A guard with a complete targeted replay, or a proved domain bound, can settle the issue without changing the mathematical method.

Paths and line numbers below refer to the source files reviewed on 2026-10-04. Paths are relative to the repository unless prefixed by `/tmp`. I did not change the paper or commit anything.

1. **Major — close the arithmetic-domain gap in KAN path (I).**

   **Location:** `paper-open-minlplib/sections/B9-ann-kan.tex:262`, `:288`–`:291`, `:319`–`:324`; supporting code `paper-open-minlplib/development/dossiers/ann-kan-checks/kan_bnb_rigexp.py:375`–`:389`, especially `:378`.

   **Problem:** The second-order bound uses `minquad`, whose contract promises a lower bound on `g*s + m*s^2/2`. It computes `half_m = 0.5*m` as an exact operation. H0 does not make this exact when halving a subnormal loses a bit. The subsequent outward steps do not always repair the lost coefficient. The supplement presents path (I) as a rigorous alternative for every instance without establishing the extra contract for all of its calls. Path (II)'s unchecked absence of NaN bounds is disclosed at line 285, so agreement with that path does not by itself close this assurance gap.

   **Evidence:** I executed the function extracted from a `/tmp` copy of the reviewed file, SHA-256 `82ca1dbd5def9b4bb2b701650e6961b53833f0074383dce20e509d7a86b29b33`. Let `t = 2^-1074`, `gl = gh = 0`, `m = -t`, `sl = -3`, and `sh = 3`. These are finite binary64 values and satisfy the caller's signed-displacement condition `sl <= 0 <= sh`. The routine returns `-3*t`, whereas the exact minimum is `-9*t/2`. Its returned value is therefore too large to be a lower bound. The probe and exact comparison are in `eg-dyadic/math-probes.log` and `eg-dyadic/check_math.py` beside this report. This is a counterexample to the routine's general contract, **not** a counterexample to a reported instance bound. `development/reviews/sol-kan-rigexp.md:157`–`:163` and `:229`–`:236` already identify the missing precondition and document instrumentation only for n4.

   **Concrete fix:** Either prove from the decoded data and all possible search boxes that every invocation has exact halving, or add an exact representability guard and replay all six path-(I) searches with that guard enabled. Alternatively, use a downward enclosure of `m/2` in the endpoint lower bound and retain verified safe handling of the convex vertex. Also establish the finite-arithmetic and signed-displacement conditions used by the vertex test. Archive the checks and reproduced lower bounds. Until then, state the unresolved condition explicitly when invoking path (I); do not treat H0 and the exponential review as establishing it. A fully checked, NaN-safe path-(II) replay could instead supply the lower-bound proof.

2. **Minor — the claim about second-order exponential terms is false under the stated hypothesis.**

   **Location:** `paper-open-minlplib/sections/F-eg-rounding.tex:255`–`:259`, especially `:257`.

   **Problem:** `delta E < 10^-6` does not imply that the second-order terms are below `10^-27`. This is an incorrect intermediate statement in the proof of the weight padding.

   **Evidence:** For `delta E = 10^-7`, which satisfies that hypothesis, `exp(delta E) - 1 - delta E >= (delta E)^2/2 = 5*10^-15`. Importantly, the affine error bound used in the table can still be justified over the full stated interval. My exact rational check proves, with `u = 2^-53` and `eps = 10^-14`,

   `exp(d)/((1-u)^2*(1-eps)) - 1 <= 1.000001*d + eps + 2.01*u`

   for `0 <= d <= 10^-6`. The positive-series tail bound and the comparisons of the constant and linear coefficients are recorded in `eg-dyadic/math-probes.log`. Thus this error does not invalidate the existing padding or the eg dual bounds.

   **Concrete fix:** Delete the `10^-27` assertion. Derive the affine inequality directly, for example by bounding `(exp(d)-1)/d` on `[0,10^-6]` with a positive Taylor series and its tail, and bounding the reciprocal denominator separately. Retain the computation of the padding constants using their exact binary64 values.

3. **Minor — H0 alone does not establish the feasibility check's correctness.**

   **Location:** `paper-open-minlplib/sections/B7-eg.tex:349`.

   **Problem:** “Under H0 alone” omits the correctness of the interval implementation, decimal enclosure, model reading, and feasibility tests. The following claims about the binary64 search points are software-assisted proofs, not consequences of IEEE arithmetic alone. Elsewhere the supplement gives the appropriate additional code-correctness premise (`B7-eg.tex:261`, `:366`, and `F-eg-rounding.tex:402`).

   **Evidence:** The interval search must interpret the right rows and inequalities and implement the rigorous exponential correctly. H0 specifies arithmetic primitives; it does not imply these facts. The exact-decimal primal points have a separate proof, which I reran successfully.

   **Concrete fix:** Replace “Under H0 alone” by “Under H0 and the correctness of the interval-mode implementation and its reader.” The intended distinction from a library exp accuracy assumption remains valid.

4. **Minor — make the dyadic exponential self-test meaningful at its large test argument.**

   **Location:** `paper-open-minlplib/development/dossiers/primal-points-checks/eg_dyadic_check.py:248`–`:255`; the check is cited in `paper-open-minlplib/sections/C-points.tex:269` and `B7-eg.tex:345`.

   **Problem:** The reciprocity assertion ends with `or (t > 100)`, so the test at `1234/7` cannot fail. Successful execution of this built-in test supplies no evidence for that argument. This affects the test, not the alternating-series proof or the feasibility conclusions.

   **Evidence:** Source inspection shows the bypass. My new test checks negative point values against independent rational positive-series enclosures, signed interval values including both signs of `1234/7`, and exact reciprocity without this bypass wherever the reciprocal branch has a positive denominator enclosure. All checks pass. Logs and the test source are saved under `development/reviews/round1/eg-dyadic/`.

   **Concrete fix:** Remove the bypass for this finite argument and print or retain the self-test result. If testing an argument beyond the fixed-precision reciprocal branch's domain, mark that case explicitly as unsupported rather than passing it automatically. Keep the mathematical proof distinct from these tests.

## Proofs and trust bases checked

I read all six requested supplement source files, the relevant theorem statements in `sections/05-other.tex` and `sections/06-points.tex`, the arithmetic hypothesis in `sections/02-semantics.tex`, and the relevant dossiers, critiques, decision-register entries, and prior eg/KAN reviews. This was a proof-level review with targeted implementation checks, not a formal verification or a fresh execution of every long search.

- **Powerflow:** The polar-to-rectangular substitution preserves the exact coefficients and objective. Positivity of the polar voltage bounds supplies the sign needed by the tangent inequalities. The Lagrangian multiplier signs, independent scalar minimizations, and eigenvalue-shift penalty are correct. The rational LDL^T test handles a zero pivot correctly: a nonzero row then contradicts PSD, while a zero row can be deleted. The J-commutation and paired-eigenvalue argument are correct. The leaf identity uses rank-one voltage coordinates, not arbitrary PSD lifts; the supplement correctly explains that the Shor lift supplies only the corresponding inequality. The perspective convexity argument makes vertex majorants valid over entire boxes. Closed leaf coverage, exact vertex checks, and each leaf's own rational dual certificate are sufficient; inherited search bounds and optimizer convergence are unnecessary. The Shor upper/lower sandwich for 0030p is valid, and the unproved size of the 39-bus root SDP gap is appropriately described as numerical. I found no mathematical issue in these proofs.
- **eg:** The reduced minimax problem and side constraints are correct. Differentiating `exp(tau*a + tau^2*b)` gives the stated third and fourth derivatives; `b <= 0` is essential and follows from the negative length-scale coefficients. Both remainder bounds and the signed cubic-moment bound follow. The affine quadratic bounds are valid elementwise bounds, not PSD assumptions. The LP and Farkas tests use valid nonnegative combinations and exact rational final evaluations, so HiGHS is untrusted. Integer relaxation only enlarges each tested set. The tree-free coverage recursion proves coverage of continuous domains and integer assignments; volume or samples are not its proof. The revised power-auditor lemma excludes the interval where the tolerance product may underflow, and the actual power arguments are asserted to avoid it. I checked the exponential reduction, table certification, Horner/remainder bound, normal scaling, and acceptance implication, and ran its supplied targeted test suite. The complete retained audit is evidence about the recorded execution, not a guarantee about an arbitrary future execution.
- **waterno2:** The Lagrangian signs and the terminal-volume identity telescope correctly. A shared cell and shared slope at each interface are what cancel the price terms; no continuity of the slopes across cell faces is required. The slope-change correction is a coordinatewise endpoint minimum on a containing box. The level-range proof treats off/one-pump/two-pump cases correctly, including the exclusion of two different admissible quadratic roots at station D. The finite-list branch-and-bound invariant covers objective-cut tightening without assuming a feasible incumbent. The LP bound has the correct sign for `Az <= b`. The full-volume closed-cell argument is valid for the nondegenerate root boxes used here. V_fl's unproved propagation is disclosed; the paper does not establish its correctness merely by comparing samples. The period and record conclusions remain conditional on the respective complete implementations and valid-box construction. I did not rerun the 7.4-hour period checks or the roughly 60-CPU-hour record checks.
- **ANN:** The reduction substitutes products without division, so zero product coefficients in full-space points do not invalidate the relaxation. The tanh convex/concave range proof and shared-noise construction are sound. The product remainder and the sharper diagonal-centering bound are valid. Weak duality over the noise cube uses the correct upper enclosure of each feasible constraint. Slab coverage and the minimum over closed/open regions justify the incomplete search's lower bound. The saturated-tanh shortcut does not itself enclose tanh; its use is justified by the subsequent outward operations as explained in the remark. Exact tanh bounds are still required for the separate triangular primal certificate. I did not rerun the long covering replay or all region checks.
- **KAN:** Polynomial propagation over Q, nonzero constants, resultants/GCDs, and interval root exclusion suffice to prove infeasibility of the exact OSIL decimals. I reran the certifying edge of all six instances, with 12/12 admissible intervals excluded in each r3 model and 6/6 in each r5 model. The input-class bound is needed to exclude the exceptional r3 endpoint root. Projection from R_P to the network relaxation, finite-choice compactness, and the perturbation estimate are correct. The hidden-box enlargement is necessary to apply the output-edge derivative bound along the entire connecting segment. The common exponential, interval core and reader are correctly disclosed; two-path agreement cannot remove a shared failure. Issue 1 concerns the remaining arithmetic contract in path (I).
- **Exactly feasible points:** The fixed-coordinate Krawczyk proof is correct. Componentwise mean values belong to the interval matrix even though their evaluation points differ. Strict inclusion gives the weighted norm bound from widths, which makes C and every enclosed Jacobian nonsingular; Brouwer then supplies a zero and the mean-value argument gives uniqueness. The remaining rows and bounds must hold on the whole box, including domains and exact fixed integers. A small equality residual or an interval containing zero would not suffice. The triangular-definition proof establishes rows symbolically before enclosing bounds. The quadratic-field sign test, verified nonnegative square-root candidates, chain parametrization, and row-by-row use of separate quadratic fields are correct. For waterno2, costs are rational and no defining row mixes the station fields. For ANN and KAN primal points, divisors must exclude zero and every retained bound must be checked; these requirements are stated.

## Resolution of the eg primal open item

I read `eg_dyadic_check.py` in full. Its integer floor/ceiling operations enclose rational constants, products, and squares. After halving a nonnegative rational argument, the terms of the alternating exp(-y) series decrease. Odd-index partial sums are lower bounds and even-index sums upper bounds. The code evaluates the former at the upper argument endpoint and the latter at the lower endpoint, rounds each signed term in the required direction, clips the lower bound at zero, and squares nonnegative endpoints outward. The positive-argument branch uses a proved positive lower endpoint before taking reciprocals. Interval monotonicity then encloses exp over each argument interval. The `math.factorial` call uses exact integer arithmetic, not a libm transcendental.

The reader checks the actual file structure, exact variable bounds and integrality, linear coefficients and nonlinear expression trees, and the objective coefficient. For these files it evaluates the original product-of-seven-exponentials expression trees directly. It does not assume that an approximately feasible decision vector can be repaired by increasing the objective if a side row fails.

The unmodified copy reproduced these strict objective-row slacks:

| OSIL instance | Exact objective variable | Smallest objective-row slack, approximately |
|---|---|---|
| eg_int_s | 6.4531031593842274088 | 5.5744e-20, e12 |
| eg_disc_s | 5.7605396164535106058 | 7.8003e-20, e12 |
| eg_disc2_s | 5.6421005799711067563 | 7.4919e-20, e10 |

All 28 rows passed for each point; all variable bounds and integrality checks passed exactly. The e26 side-row slack of eg_int_s is at least approximately 1.4922e-11. The smallest side-row slacks of the other two points are approximately 0.14017 and 0.12306. The logged row widths are around 10^-74. These are the exact-decimal points of the paper, not the distinct binary64 search points or MINLPLib's listed p1 vectors.

**Conclusion on this open item:** the three stated eg primal points are exactly feasible under decimal OSIL semantics, conditional only on the reader and exact Python integer/Fraction operations being correctly implemented. No mpmath, NumPy exp, or libm accuracy assumption enters this proof.

## Targeted commands and retained evidence

All executable repository sources were copied to `/tmp/sol-math-supp2/` before execution or import. OSIL and solution inputs for the dyadic check and KAN edge checks were copied too. The audit comparison reads retained repository data and logs; its executable reader and comparison sources are `/tmp` copies. Numerical-library thread limits were set to one. At most two single-threaded checks ran concurrently, below the four-core limit. No project-wide verification or CI inspection was performed.

Commands actually run, with working directories inside the copied trees:

```text
python3 -u eg_dyadic_check.py eg_int_s eg_disc_s eg_disc2_s
python3 -u exp_test.py
python3 /tmp/sol-math-supp2/check_math.py
python3 -u tests/test_auditor.py 6000
python3 -u checks/kan_infeas_edge_class.py kan_r3_h1_n4 x1076
python3 -u checks/kan_infeas_edge_class.py kan_r3_h1_n5 x1344
python3 -u checks/kan_infeas_edge_class.py kan_r3_h1_n9 x2416
python3 -u checks/kan_infeas_edge_class.py kan_r5_h1_n3 x776
python3 -u checks/kan_infeas_edge_class.py kan_r5_h1_n5 x1292
python3 -u checks/kan_infeas_edge_class.py kan_r5_h1_n8 x2066
python3 -u compare_audit.py --out <repository>/paper-open-minlplib/development/eg-audit/out
```

The exponential test uses an independent positive Taylor polynomial of degree 128 with a geometric tail bound, reciprocation, and 512-bit directed integer squaring. It passed 227 negative-point enclosure comparisons, 453 signed interval comparisons, and 452 exact reciprocity checks, including both signs of 1234/7. Inputs include zero, tiny rationals, argument-halving boundaries and their rational neighbors, 180 seeded random arguments in [0,15], and a negative-exponential check at 708. A first version of my reference harness attempted a positive reciprocal at 708 with an insufficient 512-bit lower endpoint; that reference-domain failure was corrected by explicitly excluding that positive case. It was not a failure of an eg point check. These tests support the analytic proof; they do not replace it.

The supplied exp/pow auditor suite passed, including its 32,010 enclosure comparisons and injected-error tests. The copied audit-comparison program also passed with its full tree-free coverage and domain checks: 1,234,542 leaves compared or checked, 63,017,129,222 retained exp/power results audited, and zero violations. This is a new verification of the retained complete run, not a fresh execution of those 63 billion calls. The exact KAN checks passed for all six models. The math probes prove the valid affine weight estimate and demonstrate the two defective intermediate/general claims described in issues 1 and 2.

Retained sources, hashes and logs are in `paper-open-minlplib/development/reviews/round1/eg-dyadic/`. They include the unmodified checker, `exp_test.py`, `exp-test.log`, `primal-rerun.log`, `check_math.py`, `math-probes.log`, `test-auditor.log`, the six KAN edge logs, and the audit comparison log. The source checker SHA-256 is `233b669847408d767fcda577a9180831348d6aa988d26aa90da6ceee83882b72`; the OSIL and solution hashes agree with the existing dossier log.
