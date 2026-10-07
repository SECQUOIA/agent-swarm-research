# Stage 3b, round 1 — independent reviewer 2

Reviewed `sections/08-temporal.tex`, `sections/09-reuse.tex`, their use of the Section 7 cyclic/tilt construction, and `audit/stage3b-author.md`. I did not consult other review reports or change the manuscript.

## Findings

1. **Minor — distinguish the unscaled and scaled solutions in the elementary hard-ray proof.** In the proof of `lem:tree-hard-ray`, immediately after setting `M=A/sqrt(8)`, the text says that the exact solution is one on the first tree, the parity H on the second, and prefix parities on the path. Those are the entries of `A^{-1}e`; the target `M^{-1}e` has every entry multiplied by `sqrt(8)`. **Fix:** explicitly describe `A^{-1}e` first and then state `M^{-1}e=sqrt(8)A^{-1}e`. The normalized state, leaf probability, condition number, query costs, and subsequent KKT identities are unchanged.

No major findings. In particular, I found no error in the predictor-decrement formula, its leakage constants, the two distinct coherent joint-output guarantees, or the dynamic-interface accounting.

## SOCP predictors and access boundaries

- At the old exact center, the new multiplier leaves radial residual magnitude `2 sigma eta theta_i ||v_i||`. The radial inverse-Hessian calculation gives exactly `2 sigma^2 r_i^2/(1+r_i^2)`, which equals `sigma^2 f(eta theta_i ||v_i||)` with the stated f. Thus the predictor identity and the global `Lambda_j^2<=sigma_0^2` bound are correct.
- Re-derived the derivative of `psi_z`. For the active scale its range lies between `2 xi/6^(3/2)` and `xi/4`. The high-scale and low-scale geometric tails sum to the displayed leakage; the simplification to `0.4 xi/(Gamma-1)` is valid for Gamma>=256.
- The conservative low/high gap exceeds `0.075 xi` for Gamma>=256. At Gamma=2^20 it exceeds `0.079 xi`, so error `0.036 xi` remains decodable.
- At the tighter accuracy, estimating only the active amplitude to error 0.02 contributes at most `0.005 xi`; adding the full tail remains below `0.01 xi`. Failure amplification to `1/(3B)` gives the stated joint success and O(B log B) source-query cost.
- The O(B) guarantee is genuinely weaker numerical output. The high-case midpoint error is at most `0.4 xi/5^(3/2)<0.035778 xi`; the tail still fits under `0.036 xi`. The low-case midpoint bound is also valid. Thus joint recovery of Boolean promise bits suffices at this accuracy without falsely supplying joint high-precision amplitudes.
- The dynamic norm is `rho(sqrt(1+xi Phi_j))`. In the stated range its radius is below 2/3, giving derivative at least `25 xi/(117 sqrt(5))` with respect to the amplitude. The norm promise gap exceeds `0.056 xi`, which is larger than twice the requested `xi/50` error.
- The dynamic-interface corollary correctly charges setup plus all responses, rather than silently making preprocessing free. The section explicitly grants formulation SQ, not exact access to the later central iterate. Supplying its conditional block norms would reveal the active source bits and invalidate the original formulation-only lower bound; this boundary is correctly stated.
- All objective/equality SQ metadata remain public: the tilted objective pieces occupy separate u/x registers, and hidden signs appear only in old matrix values. The exact center's Hessian is not assumed to be a free formulation oracle.

## Direct sums, increment outputs, and endpoint compilation

- The direct-sum minimax argument uses a hard distribution for average success 9/16. Uniform target placement is independent of the assembled input, so expected charged target queries are O(Q/B), even with nonuniform public global-sampling weights. Truncation loses at most 1/12 and leaves 7/12 success. This is a valid argument and does not amplify distributional average success incorrectly.
- The box-path increment kernel is nonnegative and telescopes to mass one. The central mass and leakage bounds are correct. Error 0.21h separates the promise cases, and Boolean representatives meet that accuracy. The h/100 numerical output correctly uses O(B log B) quantum queries instead. The stronger absolute-checkpoint output is not conflated with increments.
- The approximate-centering bound follows from 2-strong convexity in the u variables and the norm of the combined readout, giving `sqrt(B K tau_ctr)`. The fixed-k parameter choices preserve a positive gap.
- Independently checked [Buhrman et al., Corollary 3 and its coherent-subroutine model](https://homepages.cwi.nl/~rdewolf/publ/qc/robust_journal.pdf). It supports joint Boolean recovery with linear cost. Its use in the increment, decrement, and XOR upper bounds is valid; it is not being used as a joint real-number estimator.
- Re-derived the threshold LP optimum and the unit objective-gap inequality in both promise cases. The linear inverse-history constraints correctly encode `q_i=z_i Phi_i` without multiplying optimization variables. The XOR hull preserves the projection onto the t variables, forces a unique Boolean extension at the optimum, and gives the stated accumulated-error inequality for every feasible point.
- The threshold compiler has eight inequalities per block and four per additional XOR gate. The proposed strictly feasible point satisfies all inequalities, so the certified logarithmic-barrier count is valid. Public readout rounding preserves the effective promise and remains compatible with the r bound and objective dominance.
- Checked [Brody et al., Theorem 1.1](https://theoryofcomputing.org/articles/v019a011/v019a011.pdf). It applies to partial inner functions and worst-input expected randomized query cost. The manuscript correctly converts the constant-error expected lower bound into a worst-case query lower bound. Restriction to two fixed source inputs gives the coherent parity lower bound.
- The signed parity carrier, final scalar, objective-gap transfer, final unnormalized sum, and normalization-by-B accuracy distinction are correct. The manuscript does not turn separated central-path transitions into fresh oracle inputs.

## Reuse and residual certification

- The augmented KKT equations and common normalized solution ray are correct. Extracting the x register succeeds with constant probability because `||M^{-1}e||>=1`. The scalar reuse identity is separate from the state-output comparison.
- The signed-tree matrix has the stated dimension, sparsity, condition scale, leaf-state parity readout, and width-three KKT decomposition, subject only to the harmless scaling clarification in finding 1.
- The ball barrier's gradient norm bound gives the claimed metric-length lower bound. Along a chord, the two logarithmic factors yield the speed bound `h/(1-th)`, hence the bounded-Dikin movement count. Its algorithmic scope is properly limited.
- Exact span reuse adds an independent ray on every rejection. In the robust version, the minimization/test error budgets imply rejection only when the true minimum residual exceeds eta/2. The normalized checkpoint columns then have QR separation greater than Delta. The determinant lower bound and singular-value upper bound prove the `2r-1` refresh result with the stated width threshold.
- The stable-coefficient refinement correctly refers to exact versions of previously selected checkpoints, which is the condition required for the adaptive argument. No testing, tomography, or dense-output cost is hidden in the refresh count.
- The holomorphic Chebyshev-width bound is correct. The strictly complementary QP supplies independent predictor coordinate functions, and the normalized two-coordinate example has the stated pole approaching the real parameter interval.
- The low-rank certification counterexample has residual zero or `1/sqrt(2)` and uses coordinate access explicitly; a free norm oracle would indeed destroy the lower bound. The dense sign-vector lower bound correctly uses the canonical bit/value oracle, the degree-Q common-state span, and Hamming-ball counting. It does not assume exact recovery or treat a global phase as an observable.

## Validation and attribution

`/workspace/local-home/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/checks/check_temporal_identities.py` passed. The diagnostic covers the numerical kernel constants, threshold/XOR identities, scaled KKT solutions, and rank-volume inequalities. The proof checks above, rather than the finite tests, establish the conclusions.

The sections appropriately credit direct-sum/XOR theory, robust quantum input recovery, parity lower bounds, and recycling/reduced-basis methods. Their limited original-contribution language concerns explicit sparse optimization realizations, quantitative kernels, and output/access contracts; I found no unsupported priority claim here.
