# Stage 3c, round 1 — independent reviewer 2

Reviewed `sections/10-structured.tex`, the relevant access-model definitions and earlier polynomial/sampling interfaces, and `audit/stage3c-author.md`. I did not consult other review reports, edit the manuscript, or delegate this review.

## Findings

1. **Minor — make the sparse input interfaces explicit.** In the first subsection, the statement that the locations of each one-entry map `T_j` are queryable should explicitly grant row **and column** location/value access, or an equivalent forward/inverse partial-permutation interface. The rejection proof materializes columns as well as rows. A forward-only permutation oracle does not provide inverse locations at constant cost. Likewise, `cor:cone-sq` should explicitly supply row and column sparse access to A; sparsity by itself is a structural promise, not an oracle. **Fix:** add these two short access qualifications. The cone applications use diagonal maps and known embeddings, so their implementation already has the necessary bidirectional access.

2. **Minor — explicitly handle zero radial vectors in the cone access contract.** The Lorentz and generalized-power derivations correctly omit corrections at z=0, but `cor:cone-sq` requests SQ(z), while Definition `def:access` defines SQ(v) only for nonzero v. **Fix:** state that a zero radial block is identified by a returned zero norm and needs no sample request, or restrict the supplied sampling oracle to nonzero radial blocks and grant their norms in all cases. This is a boundary clarification; the zero-block algebra is correct.

3. **Minor — state full row rank in the profile subsection.** Proposition `prop:profile` asserts positive definiteness and uses inverses, but the subsection does not explicitly repeat the full-row-rank assumption on A. For example, A=0 makes N and P_theta zero. The preceding cone corollary assumes full row rank, but that theorem's hypothesis is not an unambiguous section-wide convention. **Fix:** begin the profile subsection with the assumption that A has full row rank (equivalently here S is positive definite).

4. **Minor — explicitly retain the A=I scope of the final profile rank-necessity sentence.** Following `eq:profile-rank-lower`, the statement that blocks with chi_j>theta force positive and negative update directions is valid in the stated A=I worst-case example. It is not a claim for arbitrary A: a row that selects only a middle Lorentz eigendirection has N=S regardless of the block's eccentricity. **Fix:** introduce the stronger Loewner-contract sentence with “In the same A=I family” or equivalent wording. The worst-case sharpness result and proof are correct.

No major findings. The mathematical algorithms, power-cone perturbation analysis, sampling law, and structured full-output comparisons check out under their intended interfaces.

## General sparse-base theorem and scalar estimator

- `C^T S^{-1} C` is an orthogonal projection, giving the stated bounds on K and h. The identity for `(I+LK)^{-1}` and its norm bound follow from N>=aS without assuming that L is invertible or positive semidefinite.
- The residual polynomial supplies the three operator bounds and the K/h biases. Sampling from the original source vectors yields entry second moments at most 4 and 4kappa. The entry tolerances, union bound, and total estimation count imply the advertised operator/vector error bounds.
- Re-derived the small-core inverse perturbation and the final vector error. The rho, nu, eta choices make the three error contributions each at most epsilon/(12 beta); the target norm is at least 1/beta. The coefficient guard does not reject a good setup.
- The raw rectangular rejection law remains valid for singular transforms. Choosing a component with weight c_j squared D_j and applying the final cancellation acceptance gives exactly `|y_tilde_i|^2/((r+1)Z)` per raw trial. Thus nearly zero individual transformed columns do not cause normalization costs. The lower acceptance bound, inverse Frobenius guard, coefficient guard, and finite cap give bounded costs even on bad setups. Conditional on successful output, truncation preserves the exact fixed-vector sampling law.
- The scalar corollary's smaller vector tolerance gives absolute bias at most epsilon/(4 beta). The independent coordinate estimator has the stated second-moment bound, so its sample count and union of setup/readout failures give relative error epsilon. No positivity of the approximate map is needed.

## Generalized-power algebra and perturbation

- Differentiating p gives p_i=2p alpha_i/x_i and p_ij=4p a_i a_j-2p diag(alpha_i/x_i squared). Substituting into the Hessian of the displayed barrier reproduces D0 and all three signed low-rank terms in `eq:power-normalized`, including the cross-term coefficient.
- Verified the exact barrier and parameter against [Roy–Xiao, Theorem 1](https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf). The manuscript's generalized-power barrier is precisely the cited (m_x+1)-self-concordant barrier.
- The true t lies in the clipping interval because k_i is between one and 2lambda and k_i>=2lambda alpha_i. For every clipped t, the two-dimensional core has positive leading entry, trace at most 4lambda, and determinant at least one. This proves the stated uniform spectral bounds.
- Writing the inverse correction through the Gram matrix proves symmetry and the `10 Lambda^2` coefficient bound. Direct differentiation gives `L'=L E_11 L`, hence the `100 Lambda^4` Lipschitz bound. The interval is convex, so the derivative bound integrates over all admissible estimates. The t estimator is an average of bounded values under the supplied alpha-squared distribution and needs no norm of X1.
- Estimated L is treated as a genuinely perturbed operator, rather than silently substituted into an exact identity. Its whitened error is at most v; v<=a/2 preserves a known positive comparison. With S normalized above by I, the resolvent bound is `2 kappa_S v/a` relative to the original solution. The coefficient tolerance and subsequent epsilon/4 solve leave sufficient total error margin. Repeating this vector construction at the smaller scalar tolerance correctly transfers the guarantee to the original inverse form.
- Clipping bounds the coefficient norm even on statistically inaccurate estimates. The generic setup guards/caps therefore remain applicable on bad initial estimates, while the good-event probability is obtained by splitting the setup failure budget.

## Scalar acquisition and other cone identities

- The Lorentz inverse eigenvalues and signed rank-two correction are correct; normalizing by the scalar base gives coefficient norm at most chi_max-1 and spectral comparison [1/chi_max,chi_max].
- The equal-norm pair construction gives the exact geometric-mean formula and constant-query simulation of the original vector SQ interface. Exact p determines the weight and hence parity. In the large logarithmic-range example, consecutive values have ratio greater than three, so relative error less than one half still identifies the weight. This lower bound correctly concerns acquiring p from the original input, rather than a model that already supplies p.
- The bounded-log-range discussion correctly distinguishes alpha-weight sampling from SQ(alpha)'s alpha-squared sampling law.
- The aggregated logarithm-cone Hessian has the displayed positive diagonal and rank-at-most-three correction. Its inverse has the same departure rank, but no uniform spectral/sampling theorem is inferred from that algebra alone.

## Profile and latent-width comparisons

- Subject to full row rank as in finding 3, the profile Loewner sandwich, condition at most theta squared, preconditioned-CG iteration bound, and energy residual certificate are correct. The primal and multiplier energy errors are exactly equal under the stated reconstruction formula.
- The row-intersection width bounds column support, base assembly, Cholesky fill, transformed-update solves, Gram formation, and the small signed core. The setup/apply counts conservatively include these operations. The core is nonsingular by the determinant identity even for indefinite corrections.
- The inertia and kernel-intersection proof of the worst-case rank lower bound is valid. The positive/negative update construction also gives the claimed sharp Loewner rank requirement in that same family.
- The profile quasidefinite augmentation has a positive first principal group because S-VV^T is positive definite, and a negative last group. Its graph width and exact factorization counts are consistent. The manuscript appropriately separates exact factorability from floating-point stability.
- The one-hub KKT expansion eliminates to the exact original Hessian. Full row rank and positive definiteness imply nonsingularity. Doubling graph vertices into row and column copies gives width at most 2tau_L+1 with the required compact decomposition. The use of [Fürer–Hoppen–Trevisan's primary theorem](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.116) is valid for a one-right-hand-side exact field-operation solve.
- The two-hub positive-diagonal decomposition, strict downdate condition, regularized quasidefinite grouping, and Neumann perturbation bound are correct. The generic one-hub obstruction and the coarse-forest width construction also check out.
- The final CGLS residual bound follows from the normal-equation energy bound for a consistent full-column-rank system. The full-output comparisons require the stated uniform trajectory and residual contracts; they do not apply to scalar, sampling, or state outputs.

## Diagnostics and attribution

The qipm diagnostic `checks/check_structured_identities.py` passed all 152 checks. Its numerical Hessians, core endpoints/derivatives, rectangular proposals, indefinite corrections, and Schur identities support the independent derivations above; they are not used in place of proofs.

The section credits the existing cone barriers, inverse-Hessian formulas, SQ matrix arithmetic, Woodbury/factorization methods, and low-treewidth elimination. I found no unsupported first-result or broader novelty assertion in this stage.
