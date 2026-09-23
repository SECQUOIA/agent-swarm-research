# Stage 5 coordinator checks during authorship

## Fourier argument

I independently rederived the bounded-test characteristic equation and checked all constants against the accepted half-moment bound. With omega=kappa(b+sigma), the nonlinear term is bounded by |k| a0 exp(-omega t). Variation of constants has an absolutely convergent amplitude integral when delta=omega+Re psi>0. Its physical characteristic remainder is exp(-omega t), while its rescaled remainder is exp(-delta t). Uniform convergence on a compact interval proves continuous amplitude with value one at zero, without differentiability or logarithmic moments. The ratio division uses a denominator at least half that amplitude and gives the recorded exponential constant. No independence or probability interpretation of the limiting amplitude is needed.

For uniqueness, subtracting the difference of total jump masses at zero gives a finite signed measure supported on the closed negative half-line. Its transform is holomorphic in the lower half-plane: the sign gives exponential damping. Boundary continuity follows from finiteness. Zero boundary values on an interval permit Schwarz reflection, after which the identity theorem and Fourier uniqueness apply. Restriction back to the open negative half-line eliminates the artificial atom at zero. Strictly smaller daughters are essential. Selection zero leaves an unused daughter law unidentified; count growth plus known mass supplies the coagulation rate.

The elementary instability example uses two nearby positive complementary atom pairs, with four distinct atoms. Their exponents converge uniformly on bounded frequency intervals, although the full signed variation norm of the daughter-measure difference equals four. This is not the manuscript's supremum-set TV convention for probabilities and must be labeled as a variation norm.

## Sampling bounds

Real and imaginary components lie in [-1,1]. Four Hoeffding bounds at epsilon/sqrt(2) give 8 exp(-n epsilon^2/4). The observed-denominator certificate is an exact quotient identity and requires a strict denominator inequality. It bounds sampling error relative to the exact finite-time ratio, so deterministic nonlinear bias must be added separately. Using the already bounded true ratio prevents an unnecessary second attenuation factor in the noise term. The sufficient time log(1/epsilon)/omega balances powers because delta+attenuation=omega. This uses predetermined frequency/time and constants supplied by the model or class; it is neither an adaptive nor a minimax statement. The independent sample count is separate from the physical population parameter.

## Preparation algebra

I checked the finite-shell converse, including the skew-matrix correction. A quadratic polynomial vanishing on an interior feasible shell vanishes on its affine hull. Its kernel-to-kernel block is zero, so K=C^T A+A^T C. The remaining linear functional is C^T gamma with gamma orthogonal to h. The displayed skew B satisfies B^T h=gamma and leaves K unchanged under A -> A+BC. Thus s=A^T h can be imposed. The assumption h nonzero and full row rank are used; rank at most 2r is necessary, not sufficient.

The fixed-concentration gauge, unknown-source residual gauge at two concentrations, polarization reconstruction, and scalar measurement counts follow by direct substitution. Positivity may collapse an algebraic gauge at the boundary. For the continuous two-constraint sufficient construction, a count trajectory requires integrability of the scalar coefficient, not just formal cancellation; bounded nonnegative coefficient functions are a sufficient conditional setting. No continuum representation converse follows from the finite-grid theorem.

The noise constants 3/c^2 and 5/(2c) are sums of absolute linear coefficients. The finite-difference rate error is eta/t+B t/2 when initial count is exact; the optimal positive time requires eta,B>0 and the chosen validity interval. It does not justify arbitrarily concentrated preparations.

## Primary-source checks

Garnier's [primary preprint](https://arxiv.org/html/2405.10588v1), Section 2.2, uses two-time transform cancellation and a distinguished logarithm; the present nonlinear bias estimate must carry the contribution. The direct PMC pages for the mixture and Mirzaev articles challenged this browser; the author is independently pursuing available primary copies.

The [McCoy–Madras publisher introduction](https://www.sciencedirect.com/science/article/abs/pii/S0009250903001593) explicitly identifies earlier constant-number coagulation–fragmentation examples and then describes its variable-number extension. Its metadata are CES 58(13), 3049–3051 (2003), DOI 10.1016/S0009-2509(03)00159-3. The [Patil–Andrews publisher record](https://www.sciencedirect.com/science/article/abs/pii/S000925099700314X) verifies CES 53(3), 599–601 (1998), DOI 10.1016/S0009-2509(97)00314-X, and identifies Lage's correction, CES 57(19), 4253–4254 (2002), DOI 10.1016/S0009-2509(02)00369-X. These primary records support the narrow historical statement; the older proofs have not been reverified here.

## Actual-file checks after authorship

I read the complete authored Fourier section, preparation appendix, abstract, introduction, assumption roadmap, and discussion. Every added proof agrees with the independent derivations above. The explicit projection formula for the shell representation is correct because its symmetrization is PK+KP-PKP=K when QKQ=0. The new unknown-source error terms follow from the absolute reconstruction coefficients; the bound seven epsilon for source recovery is conservative and valid despite reused observations.

The discussion preserves the distinction between fully proved statements and separate unsolved research problems. The paper does not promise a sharp calendar-time exponent, propagation of chaos on growing horizons, or stable whole-law inversion. These are not missing steps in its theorems.

I also freshly read the accepted model, fractional-moment, well-posedness, auxiliary-process, log-limit, last-event, daughter-comparison, and exact-critical files. The comparison lemma keeps the direct loss before bounding the cross loss; the positive expansion identifies number marginals without assuming unbounded-generator uniqueness; the product martingale proves finite coagulations without expectations of its random envelope; and the last-event density projects future marks at actual coagulation stopping times before compensation. No new defect emerged. The Stage 4 moment, finite-population, and numerical checks are recorded separately.

After the Stage 5 author handoff I inspected the rendered first page and extracted the complete PDF text. The opening abstract and introduction are legible and within margins; no unresolved double-question-mark reference remains. The PDF has 55 pages. Its extracted word count includes mathematics and is not a prose-word count. No manuscript or frozen supplement mutation occurred during these checks.

## Correction after independent review — 2026-09-07

Added by the separate revision agent with coordinator authorization. The historical body above is preserved. Its statement that strictly smaller daughters form an essential identification boundary is too strong. The strict-support theorem is correct, but with both daughter constraints known, an atom at fraction one is recoverable despite contributing no term directly to the exponent. For a hypothetical daughter measure on (0,1], write ν_-=σ(log)_#(B restricted to (0,1)) and z=σB({1}). One-sided uniqueness identifies ν_-. Subtracting the mass constraint from the count constraint gives σ=∫(1−exp(y))ν_-(dy), a bounded integral; the count constraint then gives z=2σ−ν_-(R). For positive σ this recovers B, including its endpoint atom. No enlarged forward theorem is asserted.

The abstract now explicitly places the finite-population count and mass-distribution claims at critical balance σ=λm. Five independent Stage 5 reviews and all accepted minor corrections are complete. Coordinator verification and acceptance remain pending; see `stage5-revision.md`.
