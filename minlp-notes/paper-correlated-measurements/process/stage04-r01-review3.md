# Stage 4, round 1, independent review 3

Decision: **No major issues. No minor issues.**

I reviewed the frozen Stage 4 sources independently, without reading another review report or the author's/root's check programs. My main scope was the latent-separator construction in `sections/04-certification.tex:399–578` and the complete cross-representation and bridge proofs in `appendices/certification.tex:236–393`. I also checked the section-wide prior assumptions, the support-certificate arithmetic contract, the virtual-noise definition, and consistency with the initial statistical model. Later computational and synthesis stages are intentionally outside this gate.

## Mathematical assessment

- The augmented matrix uses the correct Gaussian nuisance precision. Its Schur complement is the selected-covariance information, with no free anchor observations. The section-wide assumption `J_0` positive definite supplies every full-matrix definiteness assertion used here.
- The cross-representation proof retains the off-diagonal blocks of the anchor prior. The change from `V` to `V-LU` fixes the retained coordinates and is a bijection on the minimized coordinates. Thus its minimization really is the claimed Schur complement in the original retained coordinates. The conditional-mean and conditional-covariance identities hold after arbitrary row selection, including no rows. Markov structure is appropriately confined to economical pattern enumeration.
- The nested-hull direction is correct: Schur complementation is matrix concave, so averaging before eliminating the extra anchors gives the larger matrix. Applying the remaining monotone Schur map and log determinant gives `U_A <= U_B`. The two optimizations use the same distribution over complete feasible schedules. The text explicitly excludes expected-count replacements and numerical-witness or nonnested-partition monotonicity.
- The support certificate is valid for arbitrary nuisance witness `G` and positive definite `W`; stationarity is unnecessary. Completing the square precedes the ordinary logdet tangent, and the prior is charged once. The gradient has rank exactly `p` and trace pairing `p`. The count DP handles exactly `k` observations. Its stated bound accounts for pattern enumeration, while the text separately acknowledges score construction and nuisance-system costs.
- The singleton reduction is valid at zero selection weights and for a singular low-rank covariance factor. It recovers the actual conditional residual split, which differs from `r I` when the last state remains unanchored. The one-time case, no-anchor case, full-anchor case and actual indicator hull are treated correctly.
- The stationary bridge loading, covariance, transition and sparse prior formulas preserve the sign of the correlation. Their denominators are positive under the stated assumptions. An observed anchor contributes its independent-noise score and resets the latent filter; subsequent nonanchor times start with the appropriate conditional variance. This avoids division by a zero anchor variance. Both possible assignments of anchor observations to adjacent blocks are consistent.
- The two integrality examples serve different purposes and are accurate. In particular, the intermediate one-anchor value is explicitly an equal-mixture value, not an unsupported optimum claim.

## Independent exact checks

`verification/stage04-review3/check.py` is a new, self-contained SymPy checker; it imports no archived audit implementation. It passed:

- 216 cross-representation and selected-information identities over all nested anchor sets and observation subsets of a rational non-Markov positive definite covariance;
- 27 exact positive-semidefinite common-mixture order checks;
- 1,440 conditional bridge covariance entries, including negative, zero and positive correlations and all anchor sets of five times, with loading checks as well;
- 93 sparse anchor-prior trace identities;
- 15 singleton virtual-noise identities, including zero/one/fractional weights and one-time, empty-anchor and full-anchor cases;
- all three stated strict-hierarchy example values;
- 192 bridge-filter versus dense-inverse checks, including both anchor-assignment conventions, together with arbitrary-witness PSD differences and exact gradient rank/trace checks.

The counts and outcomes are in `verification/stage04-review3/results.json`. These finite exact checks supplement the proofs; they do not replace their general arguments.

## Prior-work assessment

After reading `literature/AGENTS.md`, I inspected the local primary originals directly through fresh text extraction:

- Sagnol and Harman, arXiv:1307.4953v3, the subsystem criterion on printed pp. 2–3 and Theorem 4.3 / Corollaries 4.4–4.5 on printed pp. 12–14. The manuscript correctly credits the general subsystem information and conic design framework. A fixed prior atom and block-pattern atoms fit that framework.
- Levine and How, *Sensor Selection in High-Dimensional Gaussian Trees with Nuisances*, Section 7 / Proposition 7, printed p. 8. Its auxiliary augmented-target mutual information bounds are real predecessors but are not the present changing-representation mixture-Schur comparison. The manuscript describes this distinction accurately.
- Alexanderian et al., the linear primary/secondary parameter model and marginalized posterior treatment in Sections 2–3. The citation supports the established nuisance-marginalization ingredient; the paper does not improperly claim that ingredient as new.
- Harman and Trnovská, the general PSD information hull and grouped-observation discussion on printed pp. 694–695. The manuscript appropriately credits general atoms and hulls.

The qualified novelty sentence concerns the particular nested Markov-anchor hierarchy in inspected predecessors, not Schur complementation, nuisance marginalization, generic conic optimization, or grouped designs. The formulation is appropriately narrow. No claim that an inaccessible source was inspected was needed for this review.

All frozen source hashes still matched at the end of review. Temporary full-text extracts were removed; third-party originals were not copied into the deliverable. No manuscript files were changed.
