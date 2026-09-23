# Reviewer03: stage3-round1

Major findings: 0
Minor findings: 0

No concrete major or minor defect was identified in the frozen stage. This is a bounded review, not a correctness guarantee or a publication-priority determination. No manuscript change is requested by this report.

## Scope and method

I read the entire `sections/03-scalar-nonlinear.tex`, lines 1–1564, and independently reconstructed its proof arguments. My primary lens was positive-coefficient curvature integration, with particular attention to branch isolation, analytic sectors, Gaussian exactness and positivity, rational evaluation, inverse conditioning, and their use in the compiled formulation.

I also read the task, lenses, process and review protocol, checked the snapshot, bibliography and coverage inventory, and checked the relevant accepted foundations and quadratic dependencies: parity-support closure and covariance volume bounds, finite disjunctions, binary product formulations, unconditional coordinate domination, and the scalar specialization of `lem:block-logdet-oracle` with its exact central-ball repair. The accepted first two stages had also received my earlier complete stage reviews; this review did not simply assume their use in stage3 was valid.

I compared the statements and substantive development of all eleven canonical stage3 results against the manuscript: accuracy-dependent curvature; compiled curvature quantiles; the arbitrary dense convex-polynomial hybrid; positive-polynomial loglog-degree bounds; pure-power reciprocal interpolation; the baseline positive separable-polynomial theorem; unconditional error bodies; rational powers; separable convex sums and independent outputs; the MILP/MISOCP encoding separation; and sparse positive-polynomial circuits. The stronger manuscript statements have their additional arguments, including continuous-convex finite separable comparisons and signed monotone-curvature integration. I checked the stage3 supporting-development inventory against the actual proof text, including the raw-curvature and allocation counterexamples, feature geometry, relative-error boundaries, and signed rational endpoint gadget. I did not treat the inventory's “drafted” labels as evidence of correctness.

For additional source depth I read the positive-curvature integration supporting note in full, the signed integration note's root-separation argument, and the compiled-quantile source's certificates and count proof. Other canonical sources were used principally to compare hypotheses, stated bounds, distinctions, and section coverage; I did not re-audit every historical source proof or every supporting audit file. I consulted the root source-audit document after reconstructing the manuscript arguments and treated it as a source index, not an independent proof.

## Detailed checks

1. **Scalar geometry and curvature mass, lines 11–184.** I checked chord refinement by three, the two-bit finite comparison, maximal midpoint-incompatible packings and interval trimming. I reconstructed the local remainder estimate `E <= m^2 + 3m/2`, the reverse mass estimate through the telescoping potential, and the constants 24 and 49. Zero curvature and affine cases are handled. The raw curvature and coefficient-allocation examples establish distinct limitations; their accuracy choices and degree dependence agree with the displayed claims.

2. **Indexed compiler, lines 192–221.** Boolean gate inequalities force all internal wires to Boolean values conditional on the external index bits. Products with the common continuous interpolation variable are then exact without extra integer declarations. Fixed output precision, signed offsets, unused codes, and polynomial uniform circuit generation suffice for the stated linear-lift construction. This argument does not incorrectly infer ideality or efficient MILP solution.

3. **Certified positive-curvature integration, lines 235–390.** Nonzero monotone nonnegative polynomial `H` is positive on `(0,1]`. The branch polynomial is nonzero because its value at 1 is −1. Rational neighborhoods of all distinct crossings may be omitted within the stated mass budget, including tangencies. On the positive-coefficient dyadic panels, `ell/c <= 1/(16d0)` bounds every monomial's argument by 1/8 and modulus by 2 on the radius-`ell` disk. Their nonnegative sum lies in a right-half-plane sector; hence the selected square root is holomorphic and bounded by `2U`. Intersections with branch and prefix intervals preserve the disk certificate.

   I independently derived the Taylor-tail estimate `4U 4^(-q)` on the half-radius real interval. Gaussian exactness through degree `2q−1`, positive weights, and their length sum give the stated `8U ell 4^(-q)` error. The prescribed order makes the total analytic error at most `zeta/16`. The Legendre formula uses weights for an interval of length one; its missing factor 2 relative to weights on `[-1,1]` is therefore correct. The bound `(q Hq)^(-2) <= wi <= 1` gives polynomial logarithmic conditioning. Polynomial derivative bounds and root refinement allow positive rational relative weight approximations without requiring a joint algebraic field. Monotone polynomial endpoint evaluation followed by the square-root Hölder estimate controls node/function errors even when curvature is very small.

   The cutoff, crossing neighborhoods, analytic quadrature, and rational evaluation budgets fit strictly inside the requested tolerance. Rational summation across polynomially many panels preserves polynomial encoding. For inverse quantiles, both density branches exceed `kappa` on the central interval; any interval of input length `delta` contains a central subinterval of length `delta/2`. Consequently the ambiguous bisection residual `4mu` really implies input error below `delta`, including quantiles near either endpoint. Exact endpoint outputs and common dyadic padding are compatible with compilation.

4. **Signed integration and compiled/hybrid counts, lines 281–548.** I also checked the signed Taylor certificate, failed-panel root proximity, root separation after adjoining endpoint factors, and the polynomial number of adaptive tree nodes. The compiled mass knots need not be ordered: the continuous polygonal path still covers the interval, while consecutive mass differences control every traversed chord. I checked the constants 133/320, 13/16, the downward endpoint rounding band, and the seven-bit count. For the hybrid, rounding an optimal finer partition to the dyadic grid preserves the claimed gap; the stopped greedy count justifies the large-grid branch. Local cell counts are summed under a global index, yielding the stated eleven-bit comparison.

5. **Separable and positive-polynomial results, lines 550–949.** I checked Jensen-gap superadditivity, the product packing deletion bound, scalar-sum versus independent-output tolerances, and the finite/compiled dimension constants. The transformed-support covariance arguments take volume in the transformed cube and make no false volume-preservation inference. Supporting scalarization has the required normal-cone qualification and allows nonnegative multipliers, including zero rows and active caps. The original-axis Taylor and dyadic-layer constructions share one residual per coordinate across outputs. Their unconditional error rectangles contain every exact graph point. Dense prefix recurrences and sparse rounded exponentiation have the claimed distinct degree dependence; zero local bits and unused layer codes are covered.

6. **Powers and rational interpolation, lines 951–1334.** I reconstructed the scaled estimates for exponents in `(1,2)` as well as the stronger estimates for exponents at least2. In the Stieltjes construction I checked both tails, the complex-panel bound, positive Gaussian approximation, rational rounding, and exact normalization at 1. This route has polynomial numerical-degree complexity, as stated. The signed `P/Q` endpoint gadget uses a supplied positive denominator bound to give valid bounds on all continuous recurrences; it also works with zero index bits and clipped nonmonotone paths. The reciprocal interpolation equations determine their continuous variables uniquely and use the existing bits. The separate integer and rational inverse-power computations use polynomial precision in binary exponent length; their rounded log/exp comparisons and inverse modulus justify the circuit count.

7. **Relative error and encoding, lines 1337–1564.** The relative-error obstruction uses a freely chosen modulus, so its strict threshold argument does not rely on an insufficient midpoint bound. I checked the concave threshold and the truncated-domain loglog estimate. The rational MILP encoding lower bound freezes an arbitrary integer witness and bounds basis denominators by the formulation's row coefficients; it does not assume a bound on the witness itself. The four-bit construction and its total encoding are consistent. In the conic-value gadget, fixed feasible original primal and dual points force value zero when the scaling variable is zero. The displayed squaring-chain dual telescopes to the desired value, so dual attainment is explicitly supported. The short conic coefficients are properly distinguished from potentially long solution values and ordinary sparse encoding.

## Primary evidence and executed checks

I inspected Sagraloff–Mehlhorn, *Computing Real Roots of Real Polynomials*, Theorem 36, in `build/source-cache/sagraloff2015.txt` under the paper directory. The integer-polynomial bound is polynomial in degree, coefficient length and refinement bits. The paper explicitly performs square-free preprocessing, so the root-isolation import is used with its necessary hypothesis.

I checked the official [DLMF §3.5(v)](https://dlmf.nist.gov/3.5#v), including equations 3.5.18–3.5.20_1: its Gaussian weights are positive and its rule is exact through degree `2n−1`. These are the classical facts used by the manuscript; the sector and rational-conditioning arguments are supplied in the manuscript itself.

Executed `python code/quadratic_rank/check_curvature_integral_quadrature.py`: passed 12 cumulative-integral comparisons over 1905 panels; worst error/tolerance was 0.015625. I read the checker before running it. It uses exact rational branch isolation and high-precision Gaussian/function evaluations, so it is numerical support for the error calculations, not an implementation-level certification of every rational bit-complexity claim. I separately checked the constants and complexity arguments mathematically. I also executed SHA-256 comparisons of all seven frozen files twice; every comparison matched. No manuscript, bibliography, original-research or other-review file was edited.

The review did not run a full typesetting check, implement the complete compiler, prove every assertion formally, exhaustively search the literature, or review the unwritten stage4. The source comparisons and numerical checks support only the scope described above.

## Concrete findings

None. There are no numbered MAJOR, MINOR, or QUESTION findings in this report.

## Verified snapshot hashes

Paths below are relative to `paper-integer-dimension/` and match `reviews/stage3-round1/snapshot.json`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |
