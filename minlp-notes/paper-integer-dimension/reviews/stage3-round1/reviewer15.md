# Reviewer 15: stage 3, round 1

Major findings: 0

Minor findings: 1

The stage has a coherent proof chain from scalar chord geometry to compact rational formulations and the encoding separation. I found no major mathematical defect. The single finding concerns the explicit input model of one algorithmic theorem. This verdict is bounded by the coverage and source checks below; it is not a claim of publication priority or a guarantee that no further error exists.

## Finding

1. **MINOR — missing rational-tolerance hypothesis in the compiled-curvature statement.** Location: `sections/03-scalar-nonlinear.tex:394–403`, Theorem `thm:compiled-curvature`. The theorem specifies rational polynomial coefficients and a rational interval, but states a polynomial-time, polynomial-size rational construction for absolute error merely “\(\eta>0\).” The proof invokes `lem:certified-curvature`, whose tolerance is explicitly rational, and forms the rational coefficient bound \(B=1+\sum_k k(k-1)|c_k|/\eta\). An arbitrary real tolerance has no specified finite input representation, so the algorithmic statement needs the same input hypothesis as its proof. This does not undermine the proved construction for rational inputs. **Repair:** write “For rational \(\eta>0\) and a densely encoded rational polynomial …,” as the subsequent dense convex-polynomial theorem already does. A section-wide explicit encoding convention would also suffice, but the local amendment is smaller.

## Coverage and reconstruction

I read the entire 1,564-line stage-3 section, the review task, protocol and lens instructions, the stage-3 canonical and substantive-supporting coverage entries, the bibliography, and the frozen snapshot. I used the previously reviewed foundations and finite-quadratic stage for parity, disjunctive formulations, covariance, product constructions and rational allocation. I revisited the accepted block-logdet oracle and its rational feasibility repair where stage 3 specializes them. The accepted stage-1 hash is unchanged from my previous review; the accepted stage-2 hash includes the intervening corrections.

I checked the mathematical content of all eleven canonical stage-3 developments and the distinct supporting developments mapped into the section. In particular:

- **Scalar finite geometry.** I reconstructed the three-piece chord refinement, interval trimming, finite maximal incompatible packing, parity-span bound and the resulting two-bit finite linear comparison. Uniform continuity gives finiteness of the relevant packings, and convexity gives the required interval compatibility. The argument applies to continuous convex functions without silently assuming differentiability.
- **Truncated curvature.** I checked the split of the Taylor remainder giving \(E\le m^2+3m/2\), the reverse bound on admissible intervals, and the potential estimate giving the global mass/count constants. The two tolerances in the high-degree positive-polynomial example serve different purposes; the raw-curvature and coefficient-allocation obstructions are both retained.
- **Indexed linear compilation.** The gate inequalities force Boolean wire values conditional on the external binary index. A common interpolation weight and products with those wires give exact endpoint interpolation without making the wires additional integer variables. Invalid indices, fixed denominators, signed outputs and padded computation lengths have explicit treatments.
- **Certified integration and inversion.** I followed the endpoint cutoff, polynomial branch isolation, positive-coefficient panels and signed-coefficient adaptive Taylor panels. The failed-panel/root-proximity argument bounds the number of panels at each depth, while squarefree root separation bounds the depth. On accepted panels, the complex disk and positive Gaussian weights give the stated approximation control. The Legendre weight formula and denominator bound support rational evaluation. The lower bound on mass in any interval of a specified input length gives the claimed polynomial-bit inverse modulus, including uncertain-comparison termination.
- **Mass knots and the dense hybrid.** I checked the target-mass overshoot case, mass error from uncertain bisection, reversed or repeated knots, downward endpoint rounding and both sides of the output band. The continuous knot path still covers the input interval. For the hybrid, I checked interval perturbation, rounding a partition to the fine grid, the exact chord predicate, the greedy stopping certificate, isolated inflection neighborhoods and the sum of cells before applying one global index. The constants support the seven- and eleven-bit comparisons.
- **Separable sums and independent outputs.** The hinge representation proves Jensen superadditivity for continuous convex summands. Product packing and the discrete code estimate give the lower bounds needed to compare the sum of local counts with the true integer minimum. I checked the distinction between a single total error budget and independent output tolerances, including the stated finite and compiled overhead constants.
- **Positive-polynomial allocation.** The power-coordinate map is used to transport a cover of the cube; the proof does not claim that this nonlinear map preserves volume. The nonnegative supporting multiplier reduces the optimal allocation to a scalar objective, and the transformed square-root polynomial is convex because it is a norm of nonnegative convex powers. The unconditional-body argument uses the accepted rational allocation oracle with its required inner/outer bounds and feasibility repair. The feature-curve identity remains explicitly proved even though the later geometric argument is stronger.
- **Dense and sparse endpoint constructions.** I checked the dyadic-layer curvature bound, the implied layer selectors, exact prefix powers and the use of the same index bits for their products. The sparse repeated-squaring enclosure depends polynomially on exponent bit length and requested precision; the band accounts for its rounded endpoint evaluations.
- **Pure powers and rational inverse maps.** The scaled Jensen and chord estimates distinguish exponents below two from those at least two. I checked Stieltjes tail truncation, dyadic analytic panels, positive rationalization and exact normalization. The reciprocal construction reuses the external bits, and the signed rational-function extension explicitly needs a positive denominator bound. The direct inverse-power compiler has a separate uncertain-comparison argument and rational log/exp evaluation. The Stieltjes construction is polynomial in numerical degree, whereas the direct rational-exponent compiler has the stronger binary-exponent complexity claimed for it.
- **Relative error.** The residue-class argument works with any modulus, rather than being limited to parity. It gives the convex obstruction near zero, the concave threshold, and the truncated-domain double-logarithmic law with the appropriate dependence on the fixed exponent and tolerance.
- **Encoding separation.** Fixing an unrestricted integer witness leaves rational LP coefficients whose denominator bound depends on their encoding, not the witness magnitude. I checked the positive attained LP optimum used in the denominator argument and the matching four-bit construction. In the conic-value gadget, the zero-weight case follows by comparison with an original feasible primal-dual pair. The explicit dual of the repeated-squaring chain telescopes to the required value identity. Large primal/dual witness coordinates are not counted as coefficient encoding. The final separation concerns exact feasibility and formulation encoding, and does not claim numerical stability or polynomial solution time.

The boundary between this scalar/separable stage and the unwritten vector stage is clear enough to reconstruct the present arguments. I did not count stage-4 material as missing.

## Supporting-source and citation checks

I compared selected substantive passages of the canonical files for accuracy-dependent curvature, compiled curvature quantiles, the convex-polynomial hybrid, positive loglog-degree allocation, pure powers, rational powers and the encoding separation. I also inspected the full supporting notes on signed monotone-curvature quantiles, feature-curve geometry, shared-prefix rational interpolation and the small-exponent rational-formulation barrier. These comparisons checked proof content and model translation, rather than treating the research notes as authority.

I inspected the cached primary texts for Sagraloff–Mehlhorn Theorem 36, Simchowitz et al. Lemma 2.1, and Bonito–Pasciak's resolvent quadrature and associated uniform approximation estimate. The root-isolation import matches the squarefree preprocessing and requested interval precision used here. The chord/midpoint comparison and the positive-resolvent predecessor are consistent with the manuscript's attributions. The manuscript supplies its own arithmetic, positivity and bit-complexity arguments where they go beyond those imports.

I used the root's source audit as a guide only. I did not independently re-audit every historical citation or every archived review in the coverage index, and did not perform an exhaustive external priority search. I did not rerun the full LaTeX build. The report therefore does not certify all bibliography metadata or final rendered presentation.

## Executed checks

All four commands exited successfully:

1. `python code/quadratic_rank/check_convex_polynomial_hybrid.py`: 70 exact expansion/rounding bounds, 14 greedy-versus-optimal grid comparisons using 2,040 exact chord decisions, and 11 global-index checks.
2. `python code/quadratic_rank/check_signed_curvature_panels.py`: four signed-coefficient cases, 198 accepted panels in total, with maximum depth 21. The panel certificates are exact; the reported quadrature comparisons are numerical corroboration.
3. `python code/quadratic_rank/check_sparse_positive_polynomial_circuits.py`: 56 exact rounded-power enclosures and 12 high-precision sparse endpoint/band cases, including exponents through \(2^{120}+11\).
4. `python code/quadratic_rank/check_compiled_power_knots.py`: 1,479 exact rounded-power bounds, 60 integer inverse cases, 48 rational-exponent inverse cases, and 1,158 scaled Jensen/chord checks.

These are supplementary checks. The proof assessment above does not rely on their passing as a substitute for the arguments.

## Frozen-file verification

I recomputed all seven snapshot hashes and confirmed exact matches, including a final verification before writing this report. Paths below are relative to `paper-integer-dimension`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

No manuscript, bibliography, research-source or other-reviewer file was changed.
