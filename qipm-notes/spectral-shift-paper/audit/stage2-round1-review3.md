# Stage 2, round 1: independent review 3

**Findings: 0 major, 0 minor.** No repair is requested for the reviewed
material. This is an independent mathematical and numerical review, not a
claim of machine-checked proof.

Reviewed all of `sections/05-joint-accuracy.tex`, the additions in
`sections/04-fixed-accuracy.tex` from “Nonnegative even thresholds” onward,
and `scripts/joint_accuracy_diagnostics.py`. Read `audit/stage2-author.md`,
the growing-index pinned source note, and the local primary-source statement
of Gilyen et al., Lemma 25. No peer report was read. No manuscript or script
was edited. Numerical work used the required qipm interpreter and wrote
outputs to `/tmp/spectral-shift-review3-stage2`.

## Even staircase and the concrete separation

- **Attainment, positivity, and decay of F_r:** Coefficient compactness
  preserves evenness and nonnegativity on the entire real line. Squared
  approximants to `v^(1/4)`, followed by `v=y^2`, give the required even
  approximants to `y` on the positive interval. The nested feasible sets
  permit plateaus, so strict monotonicity is correctly not claimed.
- **Lower staircase:** The rescaled Taylor limit is both globally
  nonnegative and even. Applying the order-`2r+1` expansion gives the
  exponent `1-1/(2r+2)` below `F_r`. At the first admissible index ell,
  minimality provides the strict inequality `K<F_(ell-1)` even when the
  sequence has plateaus.
- **Exact-threshold upper:** For an even minimizer, the positive-error
  contact set is nonempty because an upward constant perturbation would
  otherwise improve the maximum error while preserving admissibility.
  It is finite because an even polynomial minus `y` is nonconstant.
  The slack has contact multiplicity at most `2r`; consequently the
  existing pinned gate, whose leakage vanishes to order `2r+2`, applies
  without requiring the Chebyshev form of the unrestricted minimizer.
  The blend remains even and retains the global contractivity argument.
  This establishes threshold equality, including `K=E_1`.
- **F_1=F_2=E_1:** Nonnegativity of a quadratic `A(v)` for `v>=0` forces
  its quadratic coefficient to be nonnegative. Its convexity makes the
  endpoint chord bound valid. At the maximum chord gap of `sqrt(v)`,
  the two approximation inequalities imply `2E>=2E_1`. The affine
  minimizer is admissible, completing the plateau argument. This does
  justify the stronger `Omega(delta^(-5/6))` lower bound below `E_1`.
- **Degree-six witness:** The derivative of the cubic in z is strictly
  positive (its minimum is `5/12`), and its value at `z=-1` is `5/16`.
  Hence substitution `z=2y^2/5-1` produces a globally positive even
  degree-six polynomial. The displayed binomial-tail estimate equals
  `81*sqrt(5/2)/6400`; its square is exactly `6561/16384000`, which is
  less than `(1/32)^2`. Thus `F_3(2)<1/32`, while the plateau excludes
  indices one and two. The resulting `Theta(delta^(-5/6))` is justified.

## Odd parity

The Taylor/exterior argument supplies the additional logarithm. With
`n=floor(D/(2 log Rbar))`, the interval error multiplied by `Rbar^n`
vanishes, while the value at zero remains one. The resulting Taylor
remainder lower bound and factorial estimate imply `d*t_2>=c*n`, hence
`d=Omega(D/delta)`. The Chebyshev-factor bound is uniform in n because
the exterior coordinate converges to a fixed point strictly below the
one corresponding to the chosen `Rbar`.

The upper polynomial `(s(x)-x)/(1+tau)` has the claimed global range:
the transition interval uses the raw bound `s>=-1`, and its complement
uses `s>=1-epsilon`. Oddness covers the negative half interval. The
error on all of `[delta,1]` is at most `(epsilon+tau)/(1+tau)<=K delta`.
The cited sign-approximation lemma has the necessary boundedness,
oddness, and degree; I checked its local primary-source statement.
The constants need not depend on c. The comparison is correctly scoped
to one definite-parity transform, not arbitrary compositions.

## Joint bounds and uniform constants

- **Exterior lower bound:** The affine angle coordinate maps the entire
  low interval exactly. The negative extrapolation point has the required
  sign by convexity of arcsin. Retaining the sine Taylor polynomial avoids
  a spurious rescaled `O(delta^2)` floor. The factorial remainders and the
  maximality condition on n make `u_s/K<=1` uniform over arbitrarily large
  n. The threshold asymptotic gives both the stated inverse-index formula
  and `K^(1/(n+1))=Theta_rho(1)`.
- **Integrated sign and matched law:** Oddness of s gives integral one,
  and its boundedness gives a monotone primitive between zero and one.
  The signed integral error is correct. When `L>=beta D`, the exterior
  lower factor `exp(-C D/L)` is bounded below and the upper `D+L` reduces
  to order L. The substitution `K=eta/delta` correctly yields the
  full-complement statement with constants depending only on beta.
- **Fejer--Riesz route:** The factor is analytic on the stated disk; the
  maximum-principle bound and Cauchy remainder give the displayed
  exponential and geometric factors. Squaring its Taylor polynomial
  produces a real polynomial nonnegative on all real inputs, which is
  the required feasible class for `G_r`. The endpoint-magnitude argument
  and the separate large-`T delta` branch justify the finite-index radius
  choice. For unrestricted r, the fixed-radius contradiction rules out
  `T<r+1` simultaneously for every r at sufficiently small delta. The
  explicit half-threshold condition and the subsequent root extraction
  introduce only fixed rho-dependent losses.
- **Uniform pinned gate:** Recounted its degree as
  `4(r+1)^2(r+2)(k-1)`. The nearest contact in angular coordinates has
  distance `O(1/r)` in y and provides the quadratic slack. Dividing the
  local leakage by `delta` times the slack gives exactly the displayed
  `exp(-D/r)*(C R_0^2/r)^r` bound. Contacts themselves are harmless by
  continuity. The signed blend proves exactly `G_r delta` on the low
  interval.
- **Global and high-band bounds:** The tail's factor `2^(n+4)` is retained
  correctly. In the outer global region it produces a linear contribution
  `O(r^2 2^n/k)` and a polynomial contribution bounded by
  `C r [2B/(A R_0)]^n`; the stated fixed choice of A controls both.
  The other two regions also give `o(1)` under `r=o(D)`. On the high
  interval, direct exponent counting gives `delta^(n+2-4/n)` for the
  constant/linear contribution after division by `G_r delta`, and
  `delta^(3-4/n)` for the degree-n contribution. The powers of constants
  are explicit and cannot defeat these estimates. The `c=1` truncation
  choice has zero high-point series error.
- **Intermediate comparison:** Applying the finite-margin theorem at
  index `r-1` gives the same delta exponent as the growing upper. The
  margin factor cannot be discarded near the upper boundary; it is
  retained correctly. A fixed relative margin, including exact
  `K=G_r` for large r, gives an `O(r^2)` ratio. The manuscript correctly
  leaves the optimal uniform multiplicative law unresolved.

## Numerical script and reproducibility

Ran successfully:

```text
/workspace/local-home/miniconda3/envs/qipm/bin/python scripts/joint_accuracy_diagnostics.py --output /tmp/spectral-shift-review3-stage2
```

The CSVs and both image formats were produced; I inspected the PNG.
The signed-error computation avoids subtracting values near one, the
series coefficients implement the stated partial sums, and the gate uses
logarithms to track tiny leakage. Clipping a floating-point kernel to the
analytically established range is documented. The code and audit correctly
describe meshes as diagnostics rather than feasibility certificates.

The run reproduced maximum sampled normalized errors of one, zero pin
leakage to working precision, and leakage/slack ratios approximately
`6.85e-25`, `1.94e-46`, and `3.33e-74` for r=2,3,4. An additional qipm
check confirmed all 32 tabulated thresholds decrease, G_1 agrees with its
closed form to floating-point precision, and the r=32 asymptotic ratio is
approximately `1.00836`. A separate exact rational comparison verified the
degree-six witness's error-bound inequality; its sampled maximum error
on 10,001 points was approximately `0.0143006`.
