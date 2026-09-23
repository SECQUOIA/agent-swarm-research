# Stage 3, round 1 — reviewer 09

Major findings: 0
Minor findings: 1

The full stage supports its stated finite and constructive comparisons, subject to the minor tolerance-input clarification below. I found no mathematical defect in the dense dyadic-layer construction or its sparse binary-exponent extension. This is a bounded review, not a guarantee of correctness or publication priority.

## Finding

1. **MINOR — missing computational input qualifier.** In `sections/03-scalar-nonlinear.tex`, lines 394–403, `thm:compiled-curvature` specifies a rational polynomial and rational interval but only says “absolute error $\eta>0$.” Its polynomial-time claim needs a finite representation of the tolerance. The proof immediately invokes `lem:certified-curvature`, whose hypothesis at lines 237–238 explicitly requires rational $\eta$. The canonical `results/compiled-curvature-quantile-precision.md`, under “Assumptions and conclusion,” also explicitly requires rational epsilon. For an arbitrary real tolerance, the theorem has not specified an input representation or a bit-complexity model. This is a statement/input-model omission, not a counterexample to the intended rational-input theorem. **Repair:** write “For every positive rational tolerance $\eta$” in the theorem statement; its existing proof then applies without modification. The real-data finite theorem should retain its existing broader scope.

## Coverage and independent reconstruction

I read all 1,564 lines of `sections/03-scalar-nonlinear.tex`, the review task/protocol and process instructions, the coverage inventory, bibliography entries, and the relevant accepted-stage interfaces. I checked all seven snapshot hashes and checked them again before writing this report. Earlier full reviews of stages 1 and 2 supplied context; for this stage I rechecked the parity/volume and binary-product interfaces and the corrected scalar specialization of `lem:block-logdet-oracle` in accepted stage 2.

The full-stage review covered:

- Scalar chord refinement, parity spans and maximal packing; the truncated curvature remainder and telescoping potential; both the raw-curvature and coefficient-allocation degree-gap examples. The finite real-coefficient formulation scope is preserved.
- The indexed compiler, conditional Boolean integrality of continuous gate wires, signed fixed-denominator outputs, exact interpolation products, unused indices and the zero-index-bit case.
- Positive-sector and signed Taylor-certificate integration panels; branch root isolation, squarefree root-separation preprocessing, the failed-panel proximity argument, polynomial panel count and depth, Gaussian node/weight conditioning, and the inverse modulus. I reconstructed why the signed adaptive scheme does not enumerate an exponentially fine uniform grid.
- Mass-accurate quantiles, uncertain comparisons and targets above the estimated total mass. The neighboring-knot mass bound is $133/320$, giving a chord bound below $13\eta/16$; downward endpoint rounding and the final band give $15\eta/16$. Reversed and duplicate knots retain domain coverage through the continuous path from zero to one.
- The general dense convex-polynomial hybrid: rational fine-grid perturbation, exact greedy chord predicates, the $9D$ stopping threshold, root neighborhoods, local compiler counts and the final eleven-bit comparison.
- Jensen superadditivity for continuous convex summands, the positive feature-curve inequalities, product packing and the lattice-ball counting bound. Both scalar-sum and independent-output constants were checked, including the distinction between finite and compiled bounds.
- Positive-polynomial allocation, unconditional domination, the baseline exact prefix powers, supporting scalarization and the degree-independent transformed covariance lower bound. The transformation is a homeomorphism onto the cube; no unjustified volume-preservation claim is needed. Zero supporting coefficients and cap multipliers are treated correctly.
- The complete dense and sparse proofs of `thm:positive-loglog`, discussed below.
- Pure-power finite geometry, the scaled inequalities for exponents between one and two, Stieltjes inverse approximation, positive rationalization and normalization, the general signed rational endpoint gadget with its supplied positive denominator bound, and both dense reciprocal and binary rational-exponent constructions.
- Relative-error residue-class obstructions, the concave threshold and truncated-domain estimates; the rational MILP root-graph encoding lower bound with unrestricted integer witnesses; its four-bit upper bound; the conic-value gadget at zero weight; and the explicit repeated-squaring dual certificate. The encoding separation does not assert efficient exact optimization or numerical stability.

All eleven canonical stage-3 developments have corresponding statements and proofs in the manuscript. I compared their source statements and relevant derivations, with full specialist comparisons against `results/positive-polynomial-loglog-degree-precision.md` and `results/sparse-positive-polynomial-circuit-precision.md`. I also checked the distinct supporting-development inventory against the manuscript, including the signed rational $P/Q$ endpoint gadget and the relative-error obstruction. The generic compiled-knot note correctly points to the promoted rational-power result. Explicit stage-4 vector material remains outside this gate and was not marked missing.

## Additional depth: dyadic layers and sparse mixtures

The normalized monomial curvature estimate works on every layer. On a nonfinal layer, setting $v=(k-2)s$ bounds the relevant expression by $(v+1)^2e^{-v}\le4/e<2$; on the final layer, $D s\le1$ gives an even smaller bound. It is uniform over all listed powers and has no hidden dependence on the number of monomials.

Layer selectors are forced to the selected unit vector by the external layer bits and matching literals. Unused codes cannot satisfy the selector sum. The dense exact prefix-power recurrence therefore uses only the declared layer and local-prefix bits, including when the local prefix length is zero. Its continuous size depends polynomially on numerical degree, as the theorem states.

For sparse input, the exact endpoint precision $J_i+L_i+1$ is sufficient even on the final layer. Downward rounded exponentiation has an error recurrence indexed by the represented exponent, yielding at most $(k-1)2^{-P}$ error with an exact base. It needs only logarithmically many fixed-precision products. The chosen precision depends on exponent bit length and allocation precision, not numerical degree.

The same index and interpolation weight are shared by every monomial for a coordinate. Thus each interpolated monomial satisfies $-\xi_i\le z_{ik}-x_i^k\le h_i^2/4$. Nonnegative coefficients allow these inequalities to be summed into the stated output bands. Each band contains the exact graph and admits absolute error at most $(Cp)_j/2$; unconditionality then supplies the coupled-body conclusion. The support multipliers used in the lower bound need not be computed by the constructive algorithm.

## Executed checks and primary-source evidence

The following existing checks passed:

- `python code/quadratic_rank/check_positive_polynomial_loglog.py`: 276 convex-square-root identities, 1,021 layer-curvature checks, 1,021 exact prefix/Taylor checks and 30 scalarization KKT checks.
- `python code/quadratic_rank/check_sparse_positive_polynomial_circuits.py`: 56 exact rounded-power enclosures and 12 high-precision sparse endpoint/band cases, including exponent $2^{120}+11$.

An independent inline Python `Fraction` checker passed 1,470 exact sparse interpolation/band cases and 42 layer-code cases. It used degrees 2, 3, 5, 9, 17, 33 and 65; all layers; allocations 1, 1/3 and 1/64; first and last local cells; and interpolation weights 0, 3/8 and 1. It independently implemented fixed-point downward exponentiation and checked endpoint errors, chord enclosures, graph containment and both extreme band errors. These tests supplement the proofs and do not implement a full compiler or separation oracle.

After reading `literature/AGENTS.md`, I inspected cached primary evidence for consequential imports: Sagraloff–Mehlhorn's root-refinement theorem and squarefree hypothesis; Simchowitz et al.'s chord/midpoint lemma; Bonito–Pasciak's positive resolvent quadrature construction; and Avis et al.'s Boolean-circuit LP lemma and its credit to Valiant. The manuscript's own integration, rounding and normalization details were checked directly rather than inferred from those sources. Existing root/source audits were used only as corroboration after independent reconstruction.

## Limits

I did not compile the LaTeX or generate and solve the full MILPs. I did not independently implement certified integration, exact root isolation, the rational log-product oracle or the inverse-power circuit generator. Their bit bounds received a proof review, not an end-to-end implementation test. Source comparisons outside the specialist constructions were selective; I did not reread every historical audit among the 196 indexed supporting notes or independently verify every bibliographic metadata field. Accepted stages 1–2 were reviewed here as dependencies, not reopened wholesale. No external-priority claim is certified by this report.

## Verified snapshot SHA-256 hashes

All values match `reviews/stage3-round1/snapshot.json`.

```text
coverage.md
19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5
macros.tex
3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f
main.tex
e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599
references.bib
d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80
sections/01-foundations.tex
3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e
sections/02-quadratic-finite.tex
0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3
sections/03-scalar-nonlinear.tex
dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be
```
