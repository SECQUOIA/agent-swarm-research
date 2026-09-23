**Independent review of certified MINLP expression semantics and safe cuts.**

Reviewed 2026-09-13. No blocking soundness defect was found in the reviewed code. This is a bounded independent code review, supported by regressions and exploratory falsification; it is not a formal verification of the implementation or a certification of the benchmark results.

The review covered `code/minlp_solver_lab/certify/exact_model.py`, `convexity.py`, and `safecut.py`; the model extraction and cut replay paths in `driver.py`, especially `prepare_model` and `_verify_given_cut`; and the mathematical hypotheses and formulas in [the soundness note](certified-minlp-soundness.md). The discrete proof checker and benchmark replay have separate reviews.

The substantive checks were:

- Expression decomposition and differentiation use exact rational interpretations of stored numeric leaves. Constant arithmetic, fixed variables, and Pyomo bound intersections preserve that interpretation. Python arithmetic completed before expression construction remains outside the reconstruction guarantee.
- Domain validation inspects the original expression before cancellation. Zero multiplication, zero powers, and canceled quotients must not hide undefined functions. The domain rules are conservative over declared variable bounds; rejection of an expression that is defined on a smaller feasible set is a limitation of recognition, not evidence of invalidity.
- Exact quadratic PSD checks, monomial sign/exponent conditions, linear-fractional denominator signs, and supported composition rules were inspected for overclaims of curvature. The repaired rules did not reproduce the previous floating-point cancellation and perspective-domain failures.
- The final product-range change preserves domain information independently of curvature. Its four sign cases for half-lines bound the product in the correct direction; finite boxes use all endpoint products, and unsupported unbounded sign combinations return no bounds. This permits the existing concave geometric-mean rule on nonnegative coordinates without calling a bilinear product convex or concave. Six independent regressions cover these cases.
- The rational intercept calculation agrees with the supporting inequality in the soundness note for bounded, half-line, free, and fixed coordinates. An omitted slope contributes zero to the proposed cut while its nonlinear and linear residual terms still participate in the bound. Free coordinates require a certified zero residual; half-lines require the correct residual sign.
- Symbolic differentiation is not a general subgradient oracle. `abs(x)`, `sqrt(x*x)`, and `sqrt(x*x+y*y)` at their origins abstain rather than invent derivative values. The norm example has valid finite subgradients, but the implemented route does not justify one. Singular or nonfinite derivative enclosures also abstain. The theorem explicitly needs a justified finite supporting vector.

A nonblocking evaluator inconsistency was reported and repaired during review: high-precision SymPy Float exponents were converted through a Python float. The reviewed final conversion uses the exact rational value of the SymPy Float. The model translation already emitted rational leaves, so the old branch was not reachable from the current model-to-certificate path.

Ten independent regressions were added in `certify/tests/test_independent_semantics.py`. Three check the exact analytic minimum for a quadratic row whose omitted linear slope lies on a lower half-line, an upper half-line, or a free coordinate. A fourth checks abstention at a convex norm origin despite the existence of finite subgradients. Six cover the final product-range change described above. Together with the existing exact-semantics, curvature, and safe-cut tests, the following command passed **63 tests**:

```bash
cd code/minlp_solver_lab
.venv/bin/python -m pytest certify/tests/test_independent_semantics.py certify/tests/test_exact_semantics.py certify/tests/test_review_convexity.py certify/tests/test_review_safecut.py -q
```

An exploratory deterministic experiment also tested 546 certified expressions across positive, negative, and mixed-sign boxes, using ten random midpoint pairs per expression. No numerical curvature violation was found. This experiment was a falsification aid only: finite sampling with numerical tolerances cannot prove convexity or soundness. The durable regressions above supply repeatable checks of specific contracts.

The audited source snapshot had these SHA-256 hashes. They identify the reviewed bytes, not a promise that later edits have been reviewed:

| File under `code/minlp_solver_lab/certify/` | SHA-256 |
| --- | --- |
| `exact_model.py` | `8bf158cb2647b607aef6a19a8073603596258238b464e236f05c39b56a024261` |
| `convexity.py` | `3db003517164228d39007ffa79167af161d3b457a05974ada1c4f5ed7e4ee129` |
| `safecut.py` | `52600abb82d41f00dafc106559ca539710df44a1a237cf90ca707ba3c64e7efa` |
| `driver.py` | `cefb9d8278e2b7e942830964b7fac78994c647edb05cdf98f7c3d3f258911afb` |

From the repository root, compare the current files with that snapshot using:

```bash
sha256sum code/minlp_solver_lab/certify/exact_model.py code/minlp_solver_lab/certify/convexity.py code/minlp_solver_lab/certify/safecut.py code/minlp_solver_lab/certify/driver.py
```

The model loader, exact reconstruction, symbolic differentiation, interval library, rational propagation, master identity checks, and discrete proof replay remain software proof obligations. This review supports the stated conditional mathematical argument; it does not remove those components from the trusted implementation or establish completeness for convex MINLP.
