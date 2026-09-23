# Stage 2, round 1 — independent review 08

**Verdict: PASS.** No major or minor finding. The frozen Stage 2 claims, proofs, finite certificates, and stated limiting quantifiers withstand this review.

## Coverage

I read the assignment, review protocol, Stage 2 author assignment and author ledger, and the Stage 2 scope rows. The mathematical review used the frozen files under `process/snapshots/stage02-round01/`:

- `sections/02-universal-positive.tex` in full;
- `sections/03-cubic-equal-means.tex` in full;
- `sections/appendix-positive-couplings.tex` in full;
- `sections/appendix-cubic-certificates.tex` in full;
- `sections/01-foundations.tex` in full, particularly vertex laws, common upper attainment, deficiencies, independence, and the original-versus-expanded box comparison;
- `main.tex`, `macros.tex`, and `references.bib`.

The previously accepted finite-signing appendix is not a new Stage 2 dependency and was not re-audited. The Stage 1 operator-theoretic references were not independently reopened; none is needed to establish the new positive multilinear bounds.

I read all ten canonical Stage 2 result notes: `positive-multilinear-gap`, `positive-multilinear-degree-upper-bound`, `positive-multilinear-sharp-degree-growth`, `positive-multilinear-second-order-upper`, `positive-multilinear-coefficient-removal`, `positive-cubic-gap`, `positive-cubic-analytic-family`, `positive-cubic-two-level-family`, `positive-cubic-rounding-upper-bound`, and `positive-multilinear-equal-marginals` under the repository's `results/`. I inspected the relevant earlier correction records, including the sparse/dense distinction, coefficient-removal quantifiers, tuned cutoff, Bernstein slack, second rational two-level family, and cubic mixture's restricted optimality. These records were used to locate obligations, not as proof substitutes. I did not read another current-round report.

After reading `literature/AGENTS.md`, I checked Luedtke–Namazifar–Linderoth's extracted p.22 and the same page extracted directly from the original PDF. Conjecture 1 concerns a universal constant for positive coefficients on nonnegative boxes, with no fixed-degree restriction that would invalidate the counterexample. I inspected Sherali's extracted text and original-PDF equations and proof on printed pp.252–255 (PDF pages 8–11). Equation (13) and Theorem 3 match the manuscript's whole-cube elementary-symmetric formula. I retrieved the open Hoeffding PDF to `/tmp` and visually read printed p.16, Theorem 2/equation (2.6); independent bounded summands and the exponent agree with the manuscript's two-tail specialization. No copyrighted original was copied into the paper directory. The source equation is available in the [open primary Hoeffding paper](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).

## Findings

None. In particular, I found no unsupported transition from a finite lower certificate to an attained optimum, or from a finite computational check to a universal theorem.

## Independent verification

### Dyadic hull and interpolation

The surrogate is an upper bound before geometry is restored. For a fixed law of the failure count, selecting the upper tail separately for each anchor is simultaneously feasible because the anchors have no other joint restrictions. Its marginal mass is exactly `2^-j`. The affine certificate caps the first `l-s` summands and retains `s` linear summands; its integrated intercept is `(L-s)2^-s`.

The two resource profiles have expectations `B_s` and `B_(s+1)`, which straddle one. Their mixture weights are nonnegative, sum to one, and force expected failure count one. Each profile lies in an equality segment of the same affine certificate. Prefix counts from bit reversal are exact for every level simultaneously, and XOR randomization gives each leaf conditional failure probability `R/2^L`. Thus all original singleton marginals, not just their aggregate count, hold. At cutoff ties the adjacent formulas agree. The finite check below also covered ties at `L=4,9,18,35,68`.

The arbitrary-partition proof never asserts this geometric attainment. Its Jensen measure is restricted to positive `r`, with zero contribution elsewhere; the integral of `1/t` is `(L-1)log 2`. The dense count LP has both a projection and a uniform-subset realization, so its exactness does not assert an exact sparse formula.

For all-integer degree interpolation, maximal admissible `L` gives `d_L <= d < d_(L+1)`, with `d_(L+1)/d_L` tending to two. Therefore `log d_L = log d + O(1)` and the iterated logarithms have the same leading behavior. The dimension sequence has the same bounded successive ratio, and unused-coordinate padding preserves both envelopes: feasible laws project to the old vector, and every old law can be extended with the new means. These arguments establish limits for every integer parameter tending to infinity, not only for the chosen subsequence. The simultaneous Fréchet statement quantifies over unrestricted ambient dimension; summing its inequalities over the dyadic supports gives the matching obstruction to its guaranteed fraction.

### Harmonic laws and lower-order terms

All conditional probabilities lie in `[0,1]`. The integral of the harmonic kernel is exactly `p`, including saturation at `h_p=1`; `p=0` is separately fixed. In the hard-term interval, `p_j <= t <= t_e <= u`, so inactive mass is at most `(d-1)t/M = eta t`. The remaining lower exponent is nonnegative because `eta <= 1`. This checks both the integration limits and its dependence on the degree allowance. The endpoint case `d=2, M=1` has a valid kernel and fixed point; the Lambert certificate is explicitly conditional on `w >= 1`.

Writing `J'=-F` makes `J` strictly convex. Its root is unique because `J(z)-z` is strictly decreasing with opposite endpoint signs. The tangent mixture attains the scalar crossing guarantee. Evaluating both scalar curves at their crossing supplies only the asserted optimum for these lower-bound curves. The separate mixture with independence has inverse-guarantee weights and all discarded contributions are nonnegative.

I rederived

`integral_z^1 (1/v-eta)^2 dv = 1/z-1+2 eta log z+eta^2(1-z) <= 1/z`.

For `A=w-1/(2w)`, the residual in the finite Lambert argument is `log(1-1/(2w^2))+1/(4Aw^2) <= 0`; `A >= 1/2` ensures the needed sign and a positive denominator. For the tuned cutoff, `Lambda=N+log N` and `eta=1/N`. The identity `w+log w=log Lambda-eta` first gives `w/log N -> 1`, then `w=log N-log log N+o(1)`. Multiplying by `N/Lambda` changes the denominator by `O((log N)^2/N)=o(1)`, so no constant term is lost during the numerator change.

For the fixed `eta=1` cutoff, the integrated cubic Taylor remainder is at most `1/(12 alpha^2)`. The remaining endpoint and logarithmic terms are `O(log Lambda/Lambda)=o(alpha^-2)`. Consequently `alpha+log alpha=log Lambda-1-1/(2alpha)+O(alpha^-2)`, and comparison with `w+log w=log Lambda-1` gives the printed reciprocal correction. These are upper-certificate expansions; neither argument supplies a second-order lower bound for `R_d`. The distinct dyadic tail proof, original finite harmonic constant, and older leading-constant mixture also have valid scale sets, nonempty integration intervals, normalized weights, and stated positive parameters.

### Cloning and finite coefficient removal

Any clone law can be converted to an original binary law by conditional independent rounding of its group averages; multilinearity preserves its normalized expectation. Conversely, setting all clones within each group equal embeds every original law. This proves equality of both feasible expectation intervals. The termwise identity follows separately from repeated marginal lists and the `m^d` distinct clones of each homogeneous support.

Sampling uses one event for every one of the `2^(nm)` vertices plus one event for the termwise gap. Dependence among these events does not obstruct their union bound. With the original instance fixed, `K^2 > sn log(2)/2` dominates the exponential number of vertices, and normalized error tends to zero for every fixed `d >= 2`. Uniform vertex error bounds each envelope error at every point by `t`. Positive limiting hull gap justifies ratio convergence. Homogenization and interior perturbation preserve arbitrary strict target inequalities, which is exactly enough for equality of suprema.

For the finite cubic instance, the concentration exponent is `m^3/23200`, and the strict normalized excess after all errors is `3131/2275-1/2 = 3987/4550 > 0`. The sample is therefore nonempty, and interior positivity gives positive hull gap. This establishes the claimed finite existence result without generating a sample.

### Cubic certificates, mixtures, and equal means

The scalar cubic proof has positive-definite Hessian with determinant 248. On the first interval its first-order boundary condition has the correct sign; outside that interval unrestricted quadratic minimization gives a valid lower bound. I independently expanded both eliminated quartics and all five Bernstein rows read from the frozen manuscript. Their minimum coefficient is exactly `901/120000`. The scaled finite hull upper bound consequently has denominator `223/12-delta_*+135/(4m)+9/m^2`, and the limiting certified lower ratio reduces to `1610000/743033`. The text correctly avoids claiming convergence of the actual ratios to this endpoint.

The finite count certificates cover all original vertices because the objective depends only on group counts. The primal count laws lift to every individual marginal by uniform subsets. I ran the executable block extracted directly from the frozen appendix: all `7^3+9^3+65^3` inequalities, all probability/mean conditions, primal–dual equalities, ratios, and all `17^2` two-level residuals passed exactly. The 25-variable envelope loss `46/25` and the 52-variable loss `12/5` are valid for arbitrary dependence on padding coordinates. The 4,320 supports in the latter construction are distinct.

Both two-level scalar identities were independently expanded. Their equality-atom laws give the correct means and expected scalar values. Conditional Bernoulli sampling produces the factor `(1-1/m)` in every term because each monomial uses distinct variables. This supplies both sides of the finite interval and proves convergence of actual ratios, unlike the analytic three-group minorant alone. The older `33/16` family and its `m=50` certificate also check.

For endpoint orientation, conditional exclusion intervals are nested, and the expected maximum is the stated geometrically weighted sorted sum. The cubic three-law proof handles both sides of the `1/2` classification boundary and every quadratic class. The four one-low cases exhaust all ordered failure pairs. For all-high terms the subtraction of the anchor failure from the full failure union gives `a/2+b/4`. The three optimality tests are exact or explicitly limiting; their convex combination cancels both free mixture-weight coefficients. The result establishes optimum fixed-mixture termwise guarantee, not the exact value of `R_3`.

For equal means, the adjacent-count distribution is a single common law for every degree. Convexity of the interpolated binomial count function supplies both a lower bound and attainment for each `E_d`. Comparing with independence gives `q_(n,d) <= u^d < u`, so all ratio denominators are positive. The infinite-dimensional argument first establishes a finite maximizing degree via monotonicity on either side of `u/(1-u)` and then takes that fixed degree to increasing dimension. Thus it does not interchange an uncontrolled growing-degree maximum and a limit. Bernoulli's inequality proves the uniform two, and the even complete-graph sequence proves sharpness.

### Reproducible checks

Files are under `verification/reviewer08/stage02-round01/`:

- `frozen_finite.py`: the frozen appendix's verbatim checker, extracted and replayed unchanged; all finite cubic certificates passed.
- `independent.py`: independently written exact checks of the scalar eliminations, five manuscript Bernstein rows, both two-level identities, dyadic resource profiles for `L=2,...,80` including adjacent ties, rational equal-mean/Sherali comparisons for `2 <= n <= 24` and denominators `2,...,15`, and the finite sampling margin; all passed.

The finite dyadic and equal-mean ranges are supplementary checks. The universal conclusions rest on the arguments above. No numerical optimization, approximate certificate, or existing passing log was used as proof.

## Remaining limits

This review does not establish publication priority or the absence of related results elsewhere. The exact finite-degree supremum, a matching second-order lower theorem, exact finite analytic-family hulls, and global optimality of the cubic coupling remain unresolved as the manuscript states. I did not rerun the LaTeX build or visually inspect the compiled manuscript layout; the review addresses the frozen source mathematics and its certificates. No new Stage 2 mathematical dependency was left inaccessible.
