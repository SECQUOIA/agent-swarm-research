# Stage 2 independent review 2

## Verdict

No supported major or minor finding. I read the entire frozen `sections/01-foundations.tex` (1,296 lines) and `sections/02-quadratic-finite.tex` (1,571 lines), including proofs, examples and unnumbered estimates, and compared their changes with the stage 1 frozen sources. I also read `stage2-author.md` and `stage2-literature.md`. I did not read other current reviewer reports or edit the manuscript.

The modified exposition accurately distinguishes established approximation/algebraic ingredients from the graph-containing, minimum-integer-dimension comparison. The new product Hessian factorization repairs the formerly restricted equal-coordinate explanation. No conclusion in these sections depends on an unresolved question identified in their discussion.

## Additional scrutiny: rational covariance construction

I reconstructed the algorithm in `thm:rational-finite` and its preceding numerical lemmas rather than relying on the author's audit.

- **Jacobi residual and encoding:** a maximal off-diagonal pivot contributes at least `s^2/[n(n-1)]`; exact annihilation removes twice this quantity. A rational exactly orthogonal rotation within `sigma/(8NM)` adds at most `sigma/(4N)` to the off-norm. The claimed contraction follows while `s>sigma`. Half-angle parameterization has bounded denominator on the chosen angle range. Each update adds rotation denominator lengths, and the polynomial number of rotations and norm bounds give polynomial total rational size. Repeated eigenvalues do not require choosing a stable exact eigenbasis.
- **Matrix functions:** the logarithm resolvent bound, the Sylvester integral for square roots, the inverse-square-root identity and Duhamel exponential bound control operator errors without an eigenvalue gap. On the algorithm's polynomial logarithmic spectral range, the needed absolute precision is inverse-exponential with polynomial exponent. Scalar range reduction thus suffices in the bit model.
- **Exact penalty:** homogeneous scaling by `exp(-h(P))` simultaneously repairs the cap and quadratic energies, and its negative log determinant is exactly the penalty objective. The half-log energy gradient is `M_j^2/tr(M_j^2)` in the stated isometric frame. It is PSD with trace one even for indefinite `H_j`. The Rayleigh gradient has the same property, giving the claimed global Lipschitz bounds.
- **Radius:** the dyadic feasible scalar covariance bounds the optimum determinant below; the cap then bounds every optimum eigenvalue below. This gives the stated polynomial metric radius without assuming a well-conditioned optimum in ordinary Euclidean coordinates.
- **Actual-iterate recurrence:** Zhang–Sra's comparison factor depends on the current-to-comparator distance, not a global condition number. The manuscript bounds that distance by `D`; projection fixes the feasible comparator and is nonexpansive. Allowing stored points in the slightly larger ball is harmless: the triangle comparison is global, and the subsequent projection inequality still applies. The local rounding loss in squared distance is bounded by `2D xi+xi^2`, so the distances telescope on the actual stored rational iterates.
- **Constants:** with the displayed step size, curvature contributes `1/32`; the initial-distance term is at most `1/32`; branch/gradient error is less than `1/32`; and the rounding term is below `1/64`. The objective-selection and multiplicative-repair errors leave sufficient margin for `log det(P_hat) >= log D_* - 1`. There is no exponential global-trajectory tracking assumption hidden in this argument.
- **Oracle conditioning:** every nonzero energy is bounded below by `lambda_min(P)^2 ||H_j||_F^2`. Rational input height therefore supplies polynomial precision depth for normalization. The rational Rayleigh vector supplies a near-active cap branch without eigenvector-gap dependence. Near-active branch value error and gradient approximation give the stated inexact subgradient inequality.
- **Exact feasibility and grid:** a certified rational upper bound on the homogeneous scaling factor gives exact feasibility, not merely a numerical test. Near-diagonalization and division by four give the displayed PSD sandwich. For indefinite `H`, PSD-order energy monotonicity is still valid because the derivative in direction `A>=0` is `2 tr(HPHA)>=0`. The determinant loss is `O(n)`, all new widths and depths are rationally constructible, and their total size is polynomial in the complete tolerance/coefficient input.

The grouped, total-absolute-error and block variants preserve these contracts. In particular, the grouped gradient is computed as a rational double sum in the correct tangent frame, and the proof-only real factorization is not silently required of the algorithm.

## Full-stage coverage

Read both frozen files completely, including all examples and unnumbered estimates. The review covered the representation/contact model; square, product, scalar-rank and one-sided constructions; principal compression and real shrinking; covariance/capacity arguments and matching nc-rank allocation; the oscillatory smooth-volume proof and polynomial compiler; constant-rank tubes and perspectives; finite covariance geometry and certificates; all rational algorithms; grouped and oracle output budgets; input quotient/domain volume; positive block/diagonal/feature/forest bounds; and the Max-Cut hardness proofs.

Critical quantifiers remained intact: arbitrary convex lifts may be nonclosed and use unbounded integers; binary upper models retain the entire graph; rational algorithms use the full input length and explicit oracle hypotheses; output and common-input rank reductions preserve the actual domain; and construction is separate from solving the resulting MILP. The new product Hessian factorization is valid at every positive point, including boxes avoiding the equal-coordinate line.

## Independently inspected primary evidence

- **IQS:** local primary manuscript, Theorem 1.5 (p.7) and Lemma 5.3 (p.16), supply a base-field shrunk subspace with polynomial rational size and field-extension invariance. Version confirmed at https://arxiv.org/abs/1512.03531v6.
- **GGOW:** local full text and cached published extraction, Theorem 2.18: integral rank-nondecreasing Kraus operators have capacity at least `n^(-2n)`. The determinant-ratio scaling `D_H^(-2r)` is correct.
- **Zhang–Sra:** cached primary PDF/text, pp.7–9, comparison inequality, Lemma 7 and Corollary 8/proof. Checked sign, distance-dependent curvature factor and projection. Primary record: https://proceedings.mlr.press/v49/zhang16b.html.
- **Criscitiello–Boumal:** cached original Appendix I, pp.70–71, stated affine-invariant metric and Proposition I.1 support the weaker `-1` curvature bound.
- **Del Pia:** cached original Theorem 2/proof, PDF p.15, supports polynomial rational orthogonal near-diagonalization; primary record independently opened at https://arxiv.org/abs/2607.29386. The manuscript also supplies its own proof.
- **GLS:** cached original, printed pp.172 and 177, weak optimization/separation definitions, ball assumptions and Theorem (3.1). Its output has the actual-body distance/objective guarantee used by the repairs.
- **DPV:** cached original Theorem B.5, printed p.38 / PDF p.39, supplies rational ellipsoid matrix, potentially real center, small-volume alternative and factor `(d+1)sqrt(d)`. Symmetry validly removes the center.
- The square/interpolant passages of **Beach et al.** were independently read in stage 1; the new band correctly supplies full graph containment.

Source caches are under `build/source-cache/`; IQS and GGOW also have local literature packages. These are passage-specific primary inspections, not assertions of complete verification of cited papers. `literature/AGENTS.md` remains applicable; no literature package/index was edited.

## Supplemental checks

As arithmetic checks in addition to the symbolic reasoning, I checked the recurrence's round/oracle constants using exact rational arithmetic for `n=1..30`, integer `R=1..99`; all satisfied the stated margins. I also checked the indefinite-H PSD-order energy identity and trace-one gradient on 800 deterministic random SPD instances in dimensions 1–8. These are limited checks of formulas, not evidence replacing their general proofs. No executable manuscript implementation was changed, and no additional test suite was necessary for this read-only review.

## Optional preferences

None requiring action. A future shorter presentation could move numerical implementation details to an appendix, but their present placement makes the polynomial-bit claim independently assessable and is not a defect.
