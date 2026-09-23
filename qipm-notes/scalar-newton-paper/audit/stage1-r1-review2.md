# Stage 1, round 1 — independent reviewer 2

Reviewed `sections/02-models.tex`, `sections/03-classical.tex`, manuscript build files, bibliography, author and coverage ledgers, the principal scalar-upper source note, and the available local Gharibian–Le Gall summary. No other reviewer reports were consulted. Later manuscript sections are deliberately outside this stage.

## Findings

1. **Minor — define the estimator when an approximate sample lands outside the support of the sampling vector.** In Proposition `prop:precision`, a distribution within total variation `delta` of `p_b` may assign positive probability to an index with `b_i=0`. The formula defining the exact estimator then contains a division by zero, and the subsequent sufficient coordinate-error condition does not define a computation there. For example, `b=(1,0)` and approximate law `(1-delta,delta)` satisfy the sampling promise but can request the undefined second coordinate. The coupling proof already accounts for this event, so there is no change to the mathematical bound. **Fix:** extend the exact and computed estimator by an arbitrary finite value (for example zero) at zero coordinates, or specify that such a sample reports failure. State that arithmetic-error assumptions apply to the common-support event used by the coupling. This makes the finite-error implementation contract complete.

No major findings. The item above is an implementation-boundary clarification, not a counterexample to the main scalar, bilinear, overlap, or solution-sampling theorems.

## Independent derivations and checks

- The residual polynomial follows from `T_m(c)=(theta^{-m}+theta^m)/2`; its relative Loewner error and degree have the stated parameter dependence. The `K=1` cases are correctly separated.
- For complex vectors, `|b_i|^2/b_i=conjugate(b_i)` gives unbiasedness. The second moment sums only over the support of `b`; the manuscript correctly uses an inequality instead of an equality with the full output norm. Optimizing the scalar quadratic bound proves the stated sharp Kantorovich constant.
- With `eta=epsilon/4`, scalar bias plus group-mean error is at most `17 epsilon q/32`. The group size and union/Chernoff amplification suffice, and leave enough margin for the finite-error perturbation.
- The bilinear proof uses the correct energy-weighted error and second moment. Its sample count does not require knowing the unknown energy norms. Separate real and imaginary estimators leave more than enough error margin.
- Re-deriving the complete raw rejection law gives `Pr(output i in one trial)=|(Pv)_i|^2/(R b_P^2 ||v||^2)`. Both acceptance probabilities lie in `[0,1]`; invertibility gives the stated finite expected trial count. Materializing a sparse column followed by a row is charged correctly.
- For a nonnormal matrix, `P=q(A* A)A*` satisfies `P A=I-r(A* A)`. Thus `Pb-x=-r(A* A)x` is valid without any illicit normality assumption. Its singular values are `(1-r(sigma^2))/sigma`; the claimed upper and lower bounds follow. Local walk length and the resulting sampling cost are consistent.
- The norm-sensitive overlap theorem correctly retains `R_e` in both the statistical count and approximation accuracy. Euclidean additive accuracy is not incorrectly presented as relative overlap accuracy.
- The finite-error proof correctly uses successive conditional couplings and the sup-norm Lipschitz property of the median. The rational-input implementability paragraph does not overclaim a bit-complexity bound.
- The necessary conditioning scales follow from the explicit upper bounds at fixed sparsity and accuracy; they are correctly stated only as necessary conditions for a matching-contract dimension-power lower bound.

## Diagnostics

The repository script `scripts/verify_classical.py` passed with the required qipm interpreter. I additionally checked the normal-equation residual identity and singular-value bounds on complex nonnormal matrices of dimensions 2, 5, and 10 and condition promises 1.1, 3, and 30. Those diagnostics passed. These finite examples supplement, rather than replace, the derivations above.

## Attribution assessment

The section attributes the sparse-polynomial/importance-sampling primitive to prior work and does not claim novelty for Chebyshev approximation or the Kantorovich inequality. No unsupported first-result claim occurs in this stage. The overall novelty comparison and completeness of later results remain responsibilities of the later literature and full-manuscript stages.
