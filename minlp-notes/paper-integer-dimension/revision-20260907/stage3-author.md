# Stage 3 author report

The author pass covers the complete `sections/03-scalar-nonlinear.tex`, its dependencies and cited sources. All proofs were read and reconstructed; historical review acceptance was not used as evidence. This report completes the author pass and does not replace the required five independent reviews.

## Changes

- Added short explanations of the two-bit existence comparison, the index/interpolation/band construction, and why the seven-bit algorithm needs accuracy in cumulative mass rather than input distance. These make the connection between the geometric count and the rational compiler explicit before the detailed proofs.
- Replaced the scalar section's 2021 LinA citation with precise locators in the published 2025 article. The comparison now credits its greedy optimality, continuity for convex corridors, logarithmic oracle cost per maximal segment, and additive splitting bound. It distinguishes splitting at convexity changes from this manuscript's monotone-curvature split, and identifies the lower-bound test plus certified random access as the additional development.
- Removed the now-uncited duplicate LinA technical-report entry. Updated Adams–Henry and Sagraloff–Mehlhorn to verified published metadata, retaining explicit references to the inspected author/preprint versions for technical locators. The current bibliography has 44 entries.

No theorem statement, hypothesis, count, proof dependency or mathematical scope was changed. No unqualified novelty claim was introduced.

## Mathematical audit

The reconstruction covered chord refinement and parity-span covers; maximal incompatible sets and Jensen superadditivity; both truncated-mass estimates and their endpoint potential; the high-degree obstruction; indexed Boolean compilation with continuous gate wires; the signed-coefficient analytic-panel tree and root-separation termination; Gaussian conditioning and certified quantile bisection; the seven-bit and hybrid eleven-bit counts; separable product packings; supporting-normal scalarization and transformed covariance; exact and sparse positive-polynomial layers; Stieltjes tails, rational conditioning and normalization; exact rational endpoint products; binary integer and rational inverse powers; relative-error residue obstructions; and both rational encoding bounds.

Particular checks included the following boundaries.

1. The hybrid grid comparison uses the last original knot with the same rounded value. This keeps every resulting cell inside one original interval enlarged by at most the grid width, even when several knots coalesce.
2. Signed polynomial coefficients do not enter the positive-sector argument. Their separate Taylor-certificate tree has polynomially many failed panels per depth, and root separation gives polynomial depth. Zero curvature is handled separately.
3. The seven-bit routine allows targets above the true total mass by a controlled additive amount. Unordered computed knots remain valid because each local chord has a mass certificate and the input path joins zero to one.
4. Dense algorithms may use numerical degree. The sparse positive-polynomial and rational-exponent algorithms use rounded powers or short rational series and keep complexity polynomial in exponent bit lengths. The reciprocal construction explicitly retains its numerical-degree dependence.
5. The root-graph lower bound freezes only the integer witness. Its possibly huge coordinates change the integral right-hand side, not the continuous-column determinant controlling a positive optimum's denominator. Standard-form splitting handles polyhedra without vertices in their original free-variable description.
6. The conic value gadget handles zero interpolation weight directly. The repeated-square dual certificate cancels all intermediate coefficients and has value equal to the primal optimum; its long witness coordinates do not appear as formulation data.

I found no unresolved mathematical dependency requiring additional development or a narrower theorem. The constants remain conservative bounds, not claims of sharp additive optimality. The manuscript does not promise practical efficiency of the theoretical compiler or tolerance-stable exact conic value enforcement.

## Validation and evidence

`stage3-literature.md` records the primary passages inspected and the source-version distinctions. The independent manuscript check passes: 258 labels, 44 references, no duplicate or unresolved labels/citations. `stage3-build.log` records the successful 87-page build; the final `main.log` and `main.blg` have no warnings or overfull/underfull boxes. The first build pass reported the removed LinA key from stale auxiliary data; subsequent passes resolved it.

No mathematical algorithm or numerical constant was modified, so the already successful 45-script baseline was not rerun and no implementation-mirroring tests were added. The verification here is a complete proof reading and primary-source check, not formal proof verification. No other paper directory or generated literature metadata was modified.
