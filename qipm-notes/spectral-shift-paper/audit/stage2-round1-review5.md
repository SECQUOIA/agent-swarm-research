# Stage 2, round 1 — independent review 5

**Result: 0 major findings, 1 minor finding.** The new joint bounds and parity results are supported by their proofs. The numerical artifacts reproduce, and their stated limitations are appropriate.

I reviewed the frozen `sections/05-joint-accuracy.tex`, the new material in `sections/04-fixed-accuracy.tex` starting at “Nonnegative even thresholds,” the relevant earlier definitions and constructions, `audit/stage2-author.md`, the diagnostic script and artifacts, and all three September 4 joint-accuracy source notes. I did not read peer reports or edit the manuscript. All scripts used the qipm interpreter.

## Finding

### R5-1 — Minor: the explicit maximum needs a nonempty-index condition

**Location:** `sections/05-joint-accuracy.tex:207–212`, equation `eq:FR-max`.

The all-index theorem correctly gives a bound for every admissible index. Its following maximum, however, is undefined if no positive integer satisfies the half-threshold condition. This occurs when

`K > sqrt(rho) R_0^(-2)/(4 e)`.

The section permits a shrinking `K`, but this displayed assertion does not itself impose that restriction or explicitly say that `K` is sufficiently small. The preceding theorem is valid even when its index condition is vacuous; passing to a maximum needs one additional qualifier. All subsequent small-accuracy conclusions use nonempty index sets, so no claimed asymptotic law changes.

**Repair:** Preface the display with `0<K<=sqrt(rho) R_0^(-2)/(4 e)`, or explicitly assign value zero when its index set is empty. Keep the separate `K=0` argument, where every finite index can be used and no finite maximum exists.

## Uniformity and proof checks

### Exterior lower bound

The affine angle coordinate maps the entire correctness interval exactly, and the comparison at the negative extrapolation point has the right sign. In particular, retaining the Taylor polynomial of the sine target avoids a false error floor when `K` is much smaller than `delta^2`.

The constants in the Bernstein remainder remain inside the growing power. The lower estimate obtained from maximality of the odd index controls `u_s/K` uniformly over all admissible indices at one sufficiently small, degree-independent gap. This supports the claim of no upper restriction on `log(1/K)`. The factorial root supplies the essential index factor. The asymptotic inversion for `n(K)` and the bounded factor `K^(1/(n+1))` are consistent.

### Integrated-sign upper and high-accuracy law

Oddness of the sign approximant gives the exact integral normalization, and the nonnegative integrand makes the primitive range stay in `[0,1]` over the full interval. The displayed signed error identity is correct. I checked the bounded odd sign approximant against [Gilyén et al., Lemma 25](https://arxiv.org/pdf/1806.01838); its conditions support both this construction and the new odd-parity upper bound.

The comparison `L>=beta D` converts both the exterior lower and integrated-sign upper to `Theta(delta^(-1)L)` with uniform constants. For full complement conversion, setting `K=eta/delta` gives `L>=beta log(1/eta)/(1+beta)`, as needed. Neither argument depends on the high-band width, dimension, or sparsity. The access-contract qualifications prevent an inappropriate transfer to known finite spectra or supplied complement access.

### Fejér–Riesz lower bounds

The factor has degree at most the query count. Its maximum-modulus bound, the analytic arcsine estimate, and Cauchy's geometric tail yield the stated remainder for every allowed radius. Squaring the finite Taylor polynomial really produces a polynomial nonnegative on the entire real line, including when its coefficients are complex.

For the finite-margin theorem, the endpoint magnitude separation is uniformly positive because `K<G_1<G_0`. With a small enough constant in the index restriction, it ensures `r+1<=T`. The large `T delta` case and the adaptive-radius case together cover all query counts. Solving the quadratic error obstruction gives the stated margin factor, and taking its root does not introduce growing constants.

For the all-index theorem, evaluation of the exact threshold formula gives its explicit lower estimate. The fixed-radius branch rules out `T<r+1` simultaneously for every index, so the removal of the original index restriction is justified. Its large-index limit at zero error is consistent with exact interval impossibility. This route is independent of the exterior-Taylor argument.

### Growing pinned construction and intermediate regime

I checked the degree count, angular contact spacing, quadratic slack, nearest-contact leakage, and the powers of `r`, `delta`, and `R_0` in the leakage/slack ratio. The sign-sensitive error estimate includes the contacts themselves and gives exact threshold error.

The corrected tail retains the exponential factor `2^(2r+4)`. In the three global regions, the bounds control both the linear and high-degree parts of the approximant. A single sufficiently large leading constant suffices, while `r=o(D)` makes all remaining exponential-in-index factors harmless. The high-band estimate includes the isolated gate term as well as its product with the approximant. The series truncation has the claimed order, including the high-point case `c=1`.

Applying the finite-margin lower at index `r-1` matches the upper's gap exponent. Away from the upper tier boundary, the root of the margin has a positive uniform lower bound, and the threshold ratio limit supplies that margin at `K=G_r`. The residual `O(r^2)` comparison and the statement that no uniform multiplicative optimum is proved near a tier boundary accurately describe what follows.

## New parity results

- **Even staircase:** Attainment, positivity, monotonicity, and convergence of `F_r` are established. The even Taylor limit preserves global nonnegativity. The minimizer has a nonempty finite positive-error contact set, so the earlier pinning argument applies and preserves parity. Plateaus cause no difficulty because the first admissible index has a strict gap to its predecessor.
- **Plateau `F_1=F_2=E_1`:** An admissible quadratic in `v=y^2` must have a nonnegative leading coefficient and is convex. Its endpoint chord bound gives the stated minimax obstruction. This supports the improved `delta^(-5/6)` lower bound below `E_1`.
- **Explicit even comparison:** The cubic in `v` is positive on `v>=0`. Its geometric Taylor-tail bound is approximately `0.0200112883`, strictly below `1/32`. Thus the first even admissible index is exactly three in the example. This proves the matched even order, rather than only an improved lower bound.
- **Odd order:** The exterior argument applied to `1-A_n` retains the logarithmic factor. The Chebyshev growth estimate is uniform in its growing order. The upper construction's separate transition-region and outer-region bounds establish global contractivity, and its error allocation fits within `K delta`. The result holds for any fixed positive `K`, including coarse relative tolerances.

## Source coverage

| Source note | Review conclusion |
|---|---|
| `2026-09-04-joint-accuracy-normalized-shift.md` | Exterior thresholds, growing-order lower bound, exact sine target, integrated-sign upper, high-accuracy matching, and the full-complement corollary are retained. Fixed-order relations are represented without conflating odd exterior thresholds with the globally nonnegative thresholds. |
| `2026-09-04-joint-accuracy-normalized-shift-lower.md` | Factorization, finite-margin estimate, explicit threshold lower estimate, all-index fixed-radius branch, quantitative joint consequence, exact-error implication, and access-contract caveats are retained. |
| `2026-09-04-joint-accuracy-pinned-gate.md` | The complete growing-index construction is retained. The manuscript repairs the source's hidden exponential factors and separately controls the gate-only high-band contribution. The new margin comparison strengthens the source's description of the unresolved multiplicative gap. |

I found no omitted substantive theorem or proof development in these three sources. The broader novelty and literature discussion belongs to the planned presentation stage and is not a Stage 2 completeness defect.

## Numerical reproduction and artifact checks

Ran from the manuscript directory:

```sh
/workspace/local-home/miniconda3/envs/qipm/bin/python scripts/joint_accuracy_diagnostics.py --output /tmp/stage2-review5-diagnostics
```

The reproduced `thresholds.csv`, `pinned_kernels.csv`, and `joint_diagnostics.png` are byte-for-byte identical to the stored artifacts. The script also produced the PDF successfully. I visually inspected the PNG: labels, curves, and stated asymptotic trend agree with the data.

An independent bounded scalar maximization of the hyperbolic threshold ratio for every `r=1,...,32` agreed with the script's stationary-root computation to within `2.96e-14` relative error. The first threshold differed from its closed quadratic formula by `4.51e-17`; at `r=32` the ratio to the leading asymptotic is `1.008362186190595`.

The reproduced pinned rows have maximum sampled normalized absolute error `1.0`; leakage/slack ratios are respectively `6.854487931452993e-25`, `1.937732525431207e-46`, and `3.3320852703885618e-74`; sampled pin leakage is zero. These match the author audit. I also checked the positive-series coefficient recurrence and its evaluation, and the signed-error identity used to avoid catastrophic subtraction.

These are floating-point diagnostics of the chosen examples, not certificates of global feasibility or the growing-index regime. The script and author audit already state this distinction. No additional numerical claim needs to be weakened. Inspection of the frozen build log found no undefined references/citations, warnings, or overfull/underfull boxes; I did not rebuild or alter the frozen manuscript.
