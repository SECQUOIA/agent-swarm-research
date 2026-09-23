# Stage 3 round 1 — reviewer 04

Major findings: 0
Minor findings: 0

I found no concrete correction to request in this frozen stage. I read the entire 1,564-line `sections/03-scalar-nonlinear.tex` and reconstructed its proof chains, with additional depth on the signed monotone-curvature integration lemma. This verdict is bounded by the coverage and limits below; it is not a proof of external priority or a guarantee that every defect has been found.

## Findings

No MAJOR, MINOR, or QUESTION findings.

## Detailed review of the primary lens

The signed-coefficient proof in `lem:certified-curvature`, especially lines 275–319, withstands the following reconstruction.

1. **Taylor certificate and failed-panel count.** The exact sum of absolute nonconstant Taylor coefficients bounds the variation throughout the radius-length complex disk. Passing the test therefore puts the polynomial in the open right half-plane, supplying a holomorphic square root bounded by `2U`. The contrapositive of the root-product estimate is valid with multiplicities: a failed panel has a root within `8d` panel lengths. At a fixed depth, centers have uniform spacing, so each root accounts for at most `16d+2` failed panels. Bounding failures, rather than merely the maximum depth, is necessary to prove polynomial tree size; the manuscript does both.

2. **Rational height and separation.** Clearing denominators has polynomial bit cost for dense input. Gauss's lemma justifies the leading-coefficient divisibility for the primitive square-free part of `H_int x(x-1)`. Expanding its roots inside the Cauchy disk gives the stated loose coefficient height. In the discriminant product, the claimed separation exponent is more than sufficient after bounding the leading coefficient and all other root differences. Artificial endpoint roots control real roots beyond one and near zero; conjugate separation controls imaginary parts. Repeated roots cause no problem because separation is used only between distinct roots, while the earlier product uses multiplicity. This proves polynomial depth as well as polynomial work per exact Taylor test. Constant positive curvature and zero curvature are explicitly separated.

3. **Subintervals and Gaussian errors.** Intersecting a panel with a branch interval or query prefix preserves the required analytic disk. The radius-to-half-length ratio gives the Taylor tail `4U 4^{-q}`. Polynomial exactness and positive weight sum then give `8U length 4^{-q}` quadrature error. These bounds sum over total interval length, without an exponential accuracy loss from the number of panels.

4. **Weight and value precision.** The weight formula is correctly normalized for an interval of length one. The lower weight bound and the denominator lower bound follow from the derivative estimate and positive weights summing to one. Polynomial coefficient derivative bounds permit rational relative weight approximation with polynomial precision. Evaluation through monotone rational endpoint bounds and `sqrt(v)-sqrt(u) <= sqrt(v-u)` avoids an unjustified positive lower bound on the square root. The separate cutoff, branch-neighborhood, analytic-quadrature, and rational-evaluation budgets fit within the stated slack. No joint algebraic extension is needed.

5. **Inverse conditioning.** For nonzero monotone nonnegative polynomial `H`, its value at any positive rational point is strictly positive. Exact evaluation at `delta/4` has polynomial rational encoding even when coefficients cancel. The two branch bounds imply the density lower bound on the central interval, and every interval of length `delta` contains a central subinterval of length `delta/2`. The uncertain bisection case therefore certifies input error, while the strict comparison case preserves a quantile bracket. The precision requirement depends polynomially on rational input length, not inversely on a potentially small numerical curvature minimum. Fixed-depth padding and exact endpoint handling support the common-denominator compiler.

## Full-stage coverage

I also checked the following proof obligations throughout the stage:

- Scalar chord refinement, compact parity spans, trimming finite interval covers, existence of finite maximal incompatible sets, and the distinction between finite real formulations and rational polynomial construction.
- Truncated curvature mass, the local Taylor-remainder inequality, the telescoping potential bound, and both positive-polynomial counterexamples to raw-curvature or coefficient-allocation benchmarks.
- Conditional integrality of continuous circuit wires, exact interpolation products, common output denominators, signed outputs, zero-bit cases, and exclusion of unused codes.
- Fixed-accuracy mass quantiles, targets beyond total mass, duplicate or reversed knots, graph containment and the `15/16` error band, and the `+7` count. For the arbitrary convex polynomial hybrid, I checked interval expansion and knot rounding, the exact greedy predicate, the `9D` stopping threshold, the implication that the optimal chord count exceeds degree, monotone-curvature pieces, and the global `+11` count.
- Jensen superadditivity, the positive feature-curve comparison, product packing with the integer lattice ball bound, and separate scalar-sum versus independent-output constants. I checked the continuous-convex, positive-polynomial, and arbitrary dense convex-polynomial scopes separately.
- Supporting scalarization for the allocation optimum, nonnegative multipliers, unused multiplier rows, cap constraints, the transformed covariance lower bound, exact dense prefix powers, endpoint layers, and rounded sparse binary-exponent evaluation. The manuscript retains the baseline construction while stating the stronger double-logarithmic degree bound with its proper sparse extension.
- Scaled power geometry for `1 < alpha < 2`, the finite pure-power formulation, Stieltjes tails and analytic panels, rational positive normalization, reciprocal bounds, and the general signed `P/Q` endpoint gadget with a supplied positive denominator certificate.
- Integer inverse-power uncertainty termination and rational-exponent log/exp computation. Their binary-exponent guarantees are distinguished from the Stieltjes construction's dependence on numerical degree.
- Relative-error obstruction near zero, arbitrary-modulus residue classes, the concave threshold, the truncated-domain order, and exact-error exclusions.
- The rational MILP root-encoding lower bound with unrestricted integer witnesses, the matching four-bit upper, the zero-weight conic-value gadget, and the explicit squaring-chain dual. Coefficients are distinguished from potentially huge witnesses, and total encoding from integer count and optimization complexity.

I compared the eleven canonical stage-3 result statements and their substantive constructions with the corresponding manuscript developments. I checked the current coverage inventory, including the supporting curvature, feature-curve, indexed-knot, Stieltjes, allocation-oracle, relative-error, rational-interpolation, and encoding developments. I read the signed-monotone integration supporting note in full and checked the relevant indexed-interpolation and feature-curve notes directly. Existing review/audit conclusions were treated as leads rather than evidence of correctness. I did not mark the explicitly pending stage-4 vector results as omissions.

The relevant accepted foundations are the formulation definitions, parity/contact geometry, bounded disjunction and binary-product constructions, and covariance-volume argument. I checked the scalar specialization of accepted `lem:block-logdet-oracle` and its central-ball repair in section 02; the stage-3 use satisfies those hypotheses. I read the bibliography and checked the consequential new classical imports against primary material: Sagraloff–Mehlhorn Theorem 36 gives the stated polynomial isolation/refinement bound for integer polynomials after square-free preprocessing; Simchowitz et al. Lemma 2.1 gives the stated chord/midpoint comparison; Bonito–Pasciak Section 3.3, equation (37), and Lemma 3.4 support the credited positive-resolvent quadrature predecessor. Gaussian positivity and the Gauss–Legendre setting agree with [DLMF Section 3.5(v)](https://dlmf.nist.gov/3.5#v). The stage supplies its own bit-conditioning and formulation proofs rather than importing those conclusions from the predecessor sources.

## Executed checks

All commands below completed successfully using the repository's existing scripts:

- `check_signed_curvature_panels.py`: four signed-coefficient examples, 198 exact certified panels, maximum observed depth 21; numerical integral comparisons passed.
- `check_compiled_curvature_mass_knots.py`: 109 exact indexed mass-cell certificates and 545 exact graph bands; implicit grids through 4,194,304 cells.
- `check_convex_polynomial_hybrid.py`: 70 exact expansion/rounding bounds, 14 greedy-versus-optimal grid comparisons using 2,040 exact chord decisions, and 11 global-index checks.
- `check_positive_rational_stieltjes.py`: 5,776 positive rational terms, 62 samples, and exact endpoints; worst observed error/tolerance approximately 0.000439.

I also ran an independent inline exact-rational check on 24 signed cubic polynomials
`H(x) = offset + (a^2 + epsilon)x - a x^2 + x^3/3`, whose derivative is `(x-a)^2 + epsilon > 0`. Parameters included `a=2^-30` and `epsilon=2^-80`, with zero and positive constant terms. Across 2,284 adaptive panel tests, the certificates, interval partition, and per-depth failure-count bound passed; maximum observed depth was 23. A further 648 rational checks verified both branch lower bounds used in the inverse modulus. This is a finite stress check, not a substitute for the universal separation and counting argument.

## Snapshot integrity

All seven hashes were recomputed and matched `reviews/stage3-round1/snapshot.json` at review time and again before writing this report. Paths below are relative to `paper-integer-dimension`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

## Limits

I did not execute a complete end-to-end certified quadrature implementation, a generated MILP solver run, or a conic numerical solve. The finite scripts mix exact certificates and numerical comparisons as described above. The signed quadrature's full polynomial-time guarantee was checked analytically, including root heights and rational conditioning. I did not redo every accepted stage-1/2 proof or conduct an exhaustive literature/priority search, and did not read every historical review note in the coverage index. No manuscript, bibliography, canonical result, supporting note, or other reviewer report was edited.
