# Stage 3, round 1 — reviewer 05

Major findings: 0

Minor findings: 0

## Assessment

I found no concrete mathematical defect or material omission in this frozen stage. The principal lens was mass-accurate quantiles and the dense convex-polynomial hybrid compiler. I independently reconstructed their error, integer-count, and bit-complexity arguments, including the cases in which approximate knots are reversed or duplicated. This is a bounded review, not a correctness guarantee or a claim about publication priority.

There are no numbered findings requiring adjudication or repair.

## Coverage

I read all 1,564 lines of `sections/03-scalar-nonlinear.tex`, the task, lens and review protocol, the coverage inventory, bibliography, and the relevant accepted stage 1 and 2 dependencies. Those dependencies include parity and convex-section arguments, binary linear disjunctions and prefix products, covariance bounds, unconditional allocation, and the rational logdet oracle and its feasibility repair. I checked that the eleven canonical stage 3 developments and the distinct supporting developments listed in the coverage table have corresponding mathematical content in this stage. I did not treat the explicitly deferred stage 4 vector results as omissions.

The strongest direct comparison against the original research texts was for `compiled-curvature-quantile-precision.md`, `convex-polynomial-compiled-integer-precision.md`, and the signed monotone-curvature certification note. I also checked the inventory's supporting obligations against the proofs actually supplied in the manuscript. I did not reread every historical audit or every note in the 196-file dependency index; those audit labels were not used as proof.

### Mass quantiles and the hybrid compiler

1. **Scalar and curvature prerequisites, lines 11–145.** I reconstructed the three-piece chord refinement, the interval compatibility argument, and the passage from maximal midpoint-incompatible sets to `N_eta <= 6 P`. For the truncated density I checked both the local remainder bound `E <= m^2 + 3m/2` and the telescoping potential estimate. Together they give the constants needed later: `M_eta <= 48 * 2^p` and the chord-count comparison. The proof uses monotonicity of curvature where needed; reflection covers the decreasing case.

2. **Certified integration, lines 223–390.** The cutoff leaves a polynomially controlled omitted mass. The branch polynomial is nonzero; isolated switch neighborhoods have controlled total width. The signed-coefficient Taylor test gives a root-free complex disk, and failure forces the panel center close to a root. The root-separation estimate yields polynomial depth even when coefficients have large cancellations. Intersecting a certified panel with a branch interval preserves its disk certificate. I checked the Gauss weight conditioning, positive-weight error accounting, and the inverse modulus used to turn uncertain mass comparisons into input accuracy. This proof does not assume that a lower bound on curvature is polynomially large in value; it needs a lower bound with polynomial binary encoding.

3. **Random-access mass knots, lines 394–458.** With `zeta = 1/512`, the chosen rational upper mass bound satisfies `M <= U <= M + 2 zeta`. The `N = 2^L` targets have step at most `2/5`. Targets slightly above the true total mass are covered by the same endpoint/bracket argument; a true inverse at those targets is unnecessary. I checked the `4 zeta` mass certificate for forced endpoints and uncertain bisection outputs. The unoriented mass between adjacent approximate knots is at most `2/5 + 8 zeta = 133/320`. Consequently the local remainder is at most `81529/102400` times the tolerance, strictly below `13/16` times the tolerance. Downward endpoint rounding by at most `1/8` of the tolerance makes the stated band contain the exact graph and keeps all admitted points within `15/16` of the tolerance. Reversed and duplicate knots do not invalidate chord bounds, and the continuous path from 0 to 1 covers the input interval. Finally, `2.5 U < 128 * 2^p` proves the seven-bit overhead, including the one-cell case.

4. **Dense hybrid, lines 470–548.** I checked the interval-expansion bound, downward rounding and deletion of duplicate grid knots, and the restriction argument establishing greedy optimality on the fixed grid. The exact chord predicate can handle equality by polynomial sign determination; binary search is justified by monotonicity under interval inclusion. If the capped greedy search does not finish, its count gives `N_eta > D`. Rational brackets around roots of the third derivative produce at most `3D` pieces; narrow brackets themselves need only one cell, and the remaining pieces have monotone curvature after normalization or reflection. Cutting an optimal partition adds at most one cell per internal piece boundary. This yields `K <= 120 N_eta + 122 b < 486 N_eta`, then `K < 2048 * 2^p`, establishing the eleven-bit overhead. The global index uses prefix sums of local counts, rather than a product of local index ranges. Piece selection, local evaluation, common denominators, and invalid-code exclusion have polynomial description size without enumerating exponentially many cells.

5. **Compilation, lines 192–221 and the constructions above.** Boolean gate constraints force the internal wires once the external index bits are fixed. Thus counting only external index bits is valid for binary linear lifts. The bounded products with the interpolation parameter are linearizable. The proof distinguishes polynomial index length, polynomial circuit size, and potentially exponential cell count.

### Remaining stage

- **Separable comparisons, lines 557–644:** I checked Jensen-gap superadditivity, the product deletion/packing argument, scalar-sum tolerance allocation, and the constants giving the finite, monotone-curvature, and hybrid overheads. Independent outputs use separate componentwise tolerances; no arbitrary coupled output extension is silently inferred.
- **Positive polynomial allocation, lines 646–939:** I checked the transformed-domain covariance argument, prefix-power construction, nonnegative supporting normal and active-coordinate cases, scalarized allocation, dyadic endpoint layers, and rounded binary exponent evaluation. The feature-coordinate Jacobian is accounted for through the transformed domain. The sparse construction depends polynomially on exponent encoding, while dense degree-dependent arguments are identified as such. The allocation and raw-arclength counterexamples retain their distinct conclusions.
- **Pure powers, lines 941–1329:** I checked the scaled Jensen and chord estimates on both sides of exponent 2, including the first cell near zero; positive Stieltjes tails and rational quadrature normalization; the positive denominator certificate in the generic rational endpoint gadget; the zero-bit and zero interpolation-weight cases; and the inverse-power evaluator using logarithms/exponentials or guarded integer bisection. Approximate input paths are clipped or covered as stated, and endpoint errors are included in the output bands.
- **Relative error and encoding, lines 1331–1564:** I checked the residue-class obstruction near zero, the concave threshold, and the truncated-domain logarithmic comparison. For the rational MILP barrier, fixing an integer witness changes the right-hand side but not the coefficient determinant bound; the use of total row encoding supports the claimed linear-in-`D` lower bound. The four-bit upper construction and the primal-dual conic-value gadget preserve graph containment, including interpolation weight zero. The conic upper uses an exact cone primitive and is not presented as a rational MILP encoding result.

## Primary-source checks

I inspected the cached primary text of Sagraloff–Mehlhorn, especially Theorem 36 and its integer-coefficient specialization, against the polynomial root-isolation and refinement import. The manuscript explicitly performs square-free preprocessing and clears rational denominators; polynomial dependence on degree, coefficient height and requested precision is the consequence it needs. I also inspected Simchowitz et al., Lemma 2.1, for the midpoint/chord relation, and the Codsi–Ngueveu–Gendron discussion of greedy extension, dichotomy and piece splitting. The manuscript supplies its own fixed-chord-grid greedy proof, so it does not import an unrestricted continuous piecewise-linear optimality assertion from the latter source. The accepted stage 2 oracle interface was checked at its use here; its objective-variation and feasible-repair argument supplies the scalar allocation specialization.

The primary texts were available locally in `build/source-cache`; no new web search was required. This was a hypothesis and attribution check, not a new comprehensive literature or novelty search.

## Executed checks and limits

I executed these existing checks successfully:

- `python code/quadratic_rank/check_compiled_curvature_mass_knots.py`: 109 exact indexed mass-cell certificates and 545 exact graph-band checks; grids through 4,194,304 cells without enumeration.
- `python code/quadratic_rank/check_convex_polynomial_hybrid.py`: 70 exact expansion/rounding bounds, 14 greedy-versus-optimal comparisons using 2,040 exact chord decisions, and 11 global-index checks.
- `python code/quadratic_rank/check_signed_curvature_panels.py`: four signed-coefficient examples with 198 certified panels.

The first two are finite exact checks, not universal proofs. The signed-panel script combines exact panel certification with numerical integral comparisons. These scripts do not implement or certify the complete quadrature-to-Boolean-circuit-to-MILP pipeline. I relied on the manuscript's independently reconstructed arguments for that pipeline, and did not compile the LaTeX or claim end-to-end implementation verification. I made no manuscript or research edits.

## Snapshot verification

I computed SHA-256 hashes and compared all seven frozen files with `reviews/stage3-round1/snapshot.json`; every value matched, including a final recheck before writing this report. Paths below are relative to `paper-integer-dimension`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |
