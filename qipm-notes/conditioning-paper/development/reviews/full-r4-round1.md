# Full-manuscript independent review — reviewer 4, round 1

**Verdict: no valid major or minor issues identified.**

This is a fresh integrated assessment of `main.tex`, the macros, and all twelve sections, including the proofs and the numerical conclusions. I did not read the other current full-manuscript review reports or edit manuscript sources. The numerical executions cited below were performed in an isolated copy, not in the submitted reproduction directory.

## Mathematical audit

### Setup, geometric comparison, and widths

The compactness, relative-interior, nonconstant-objective, finite-barrier-parameter, and fixed-metric assumptions are stated before use. The elementary Dikin inclusion and semibounded-gradient arguments supply the needed boundary facts. The central-path gap is strictly increasing, and the stated comparison between gap and central-path parameter follows with the correct integration direction. Equal-gap notation avoids silently comparing different objective sublevels.

I checked the one-sided local-distance proof and its explicit constant, including the early-endpoint case and the residual-dependent extension. The difference-body sandwich has the correct factor two. Its use in the different-center Loewner comparison, the inradius estimate, and the matching diameter/gap law is consistent. The homothetic interior-ball argument supplies the missing transverse width uniformly in the gap; the objective support bound supplies the converse. The positive-sublevel localization states only the pointwise conclusions it establishes and does not assume existence of a global analytic center in an unbounded set.

The final width bounds use the two Courant–Fischer formulas in the correct order: the lower eigenvalue bound has the reciprocal square of the max–min width, and the upper bound has the reciprocal square of the min–max width. The width comparison follows as stated. The directed-width version needs pointwise ray bounds, not continuity of the chosen direction on the objective equator; the proof does not assume that continuity. Endpoint widths recover the diameter and inradius quantities used earlier.

### Classifications and LP limits

The distinction between an error-bound upper estimate and an attained diameter exponent is preserved throughout. The finite-vertex argument proves bounded conditioning at a unique compact LP optimum without a nondegeneracy hypothesis. The near-degenerate simplex estimate is uniform in the displayed objective parameter; its limiting generalized eigenvalues and the iterated plateau constant agree with the claimed formulas.

In the LP limit, uniqueness implies injectivity of the positive-support column restriction, which in turn makes the limiting reduced slack matrix positive definite. The dual analytic-center characterization and the conditioning bounds retain their required endpoint and rank assumptions. The compact degenerate witness is strictly feasible, has the stated unique optimum, and uses the correct nonorthogonal Gram matrix. The unbounded witness is explicitly covered through compact positive objective sublevels, not by an unstated compact-feasible-set assumption.

### Fractional SDP, facial reduction, and exact constants

I independently followed the minor bounds, the attained two-point construction, the paired section, and both facial-reduction steps. The impossibility of a one-step reduction follows from the zero diagonal of a PSD exposing matrix forcing its corresponding row to vanish. This rules out the off-diagonal multiplier terms in the stated order. The two degree-two assertions refer expressly to the displayed optimality systems in the ambient PSD cone. The strict-complementarity failure and strict feasibility statements are consistent with those systems. The paired example therefore supports the precise conclusion that the degree alone does not determine the attained conditioning exponent.

At the logarithmic center, the sign symmetry eliminates the two third-row off-diagonal coordinates. The scalar quadratic for the remaining off-diagonal entry, the relation between gap and central-path parameter, and the determinant quantities have the correct signs and factors. The off-block Frobenius metric contributes a factor two to both the Hessian representation and the coordinate Gram matrix, leaving the stated quotient eigenvalues. For the remaining block, the Gram matrix is `[[4,1],[1,2]]`; the leading generalized eigenvalue is `(4/7) μ^-2`, and its generalized determinant gives the other eigenvalue `μ^-1`. Combining the blocks yields the ordered constants `sqrt(2), 1, sqrt(2), 4/7` and the two reported gap-scaled condition-number constants. No canonical-barrier leading constant is transferred to arbitrary barriers: only the orders are transferred.

### LP eigenspaces and the oscillatory example

The canonical Hessian splits into a bounded positive-support part and a part of order inverse-square gap with kernel equal to the optimal-face tangent. This proves the cluster multiplicities, including the zero-dimensional weak-space case. The general-barrier Loewner bound gives the projector error of order gap; the canonical eigenvector equation gives the stronger inverse-square-block argument and order gap squared. The forcing calculation uses objective orthogonality to the face tangent and distinguishes the norm of the weak component from its squared weight.

The oscillatory barrier certificate is global. The perturbation's first three directional derivatives obey the stated bounds in the base barrier metric, the Hessian lower comparison remains positive at the chosen perturbation amplitude, scaling by four gives the standard third-derivative bound, and the finite gradient parameter is less than twenty. The bounded perturbation preserves boundary divergence. On the exact subsequence, the mixed Hessian term gives weak eigenvector slope asymptotic to minus the perturbation amplitude times the gap. Keeping the factor four in the inverse Hessian gives the stated direction components: the discarded weak component dominates the retained component even though its residual fraction tends to zero. Thus the claimed sharp projector rate and the limiting relative direction error follow. The standard-form embedding changes the metric by a scalar and preserves the relevant angles and exponents.

### CG and formulation scope

The polynomial used for the clustered-CG consequence is normalized at zero. Its upper-cluster Chebyshev factor is bounded by one below that cluster, while its lower-cluster factor has controlled growth on the upper interval. The chosen repeated-factor exponent absorbs that growth and gives the stated degree bound. Singleton clusters are handled separately. Exact-arithmetic dimension termination is not used as a finite-precision iteration guarantee.

The quantum discussion correctly separates a polynomial small on the spectrum from the globally bounded polynomial required by QSVT. It also distinguishes block-encoding normalization, the ordinary condition number, right-hand-side preparation, and output requirements; it does not turn the geometric theorem into an unsupported quantum lower bound or a speedup claim.

The fixed-congruence condition bounds and the exact cancellation in the ambient Schur complement are correct. The Lorentz example is labeled as an ambient, unbounded-cone illustration. The path-derivative example permits growing data derivatives and is not presented as a contradiction of the fixed-objective sensitivity identity. The final finite-parameter counterexample remains self-concordant but fails the gradient-parameter bound in the claimed manner.

## Sources, novelty, and integration

The introduction and the adjacent discussions give proper scope to the contribution. They distinguish classical same-point chord/Hessian comparison from comparison at different centers of equal gap; they credit prior conditioning geometry, LP endpoint limits, the fractional SDP construction, and oscillatory self-concordant examples. The remaining qualified novelty claims identify precise statements rather than the broad research area.

For this full review I independently read the cached original Duistermaat manuscript, including Remark 2.3 on printed page 4. It explicitly gives a small sine perturbation of a barrier with oscillatory rescaled derivatives. The paper's attribution of this antecedent is supported. Its narrower claim for the mixed perturbation, global certificate, projector sharpness, and direction-error calculation is consistent with that source. This resolves the source-access limitation recorded in my earlier Stage 5 review, where the live URL returned 403.

The manuscript consistently distinguishes equality-reduced and ambient Hessians, Euclidean and coordinate Gram matrices, barrier parameter and central-path parameter, equal-gap and equal-parameter comparisons, upper error-bound exponents and attained exponents, residual error and direction error, and prescribed and rounded numerical spectra. Later sections rely on results actually established earlier. The abstract now allows at most two LP scales and is consistent with the unique-optimum case. The section order develops the main geometric result before its classifications, sharper examples, solver implications, and numerical evidence; I found no missing logical dependency or material readability problem.

## Numerical and reproduction assessment

The analytic examples agree with the mathematical formulas reviewed above. My isolated full reproduction during the independent Stage 5 assessment regenerated all 23 tracked artifact hashes identically and verified the supplied exact rational representation certificates. The final whole-paper conclusions retain the precision and representation limitations used in those checks.

For an independent solver reference, I used a 110-digit Decimal Cholesky calculation for the exact binary-rational rounded CG systems, rather than the package's 80-digit Gaussian elimination. The resulting final residuals and energy errors agree with the exported values. In particular, the deepest run's recursive residual is about `2.95e-9`, whereas its actual residual is about `2.52e-8`; the manuscript reports that distinction correctly. Its intermediate prescribed-spectrum energy diagnostic is explicitly identified as such and is not substituted for the final rounded-system reference.

The fractional SDP formulas avoid cancellation in the small roots and reproduce all four leading constants. The simplex and compact degenerate LP values agree with their limiting formulas. The oscillatory table's rounded ones are not claimed to be exact finite-gap direction errors. All benchmark attempts, including rejected points, are retained. The singular-value resolution screen is explicitly a numerical indicator, not a rigorous spectral certificate, and the accepted finite curves are not used to infer an asymptotic exponent. These qualifications are sufficient for the uses made of the experiments in the manuscript.

## Required corrections

None identified in this independent full-manuscript review. There is no major issue requiring another review cycle on the basis of this report, and no remaining minor correction requested by this reviewer.
