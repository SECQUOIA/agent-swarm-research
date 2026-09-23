# Stage 3: coordinator checks

## Linear-capacity numerical check

Independently evaluated the exact physical power-law weight by 160-point Gauss–Hermite quadrature for two Gaussian energy components with means `-N/2,+N/2`, variances `2N,0.7N`, beta one, and capacity exponent `3N`. This is a deterministic Gaussian benchmark, not a microscopic Potts simulation or a rigorous quadrature enclosure.

The predicted information limit is `0.7324933148` nats. At N equal to 100, 10000, and 1000000 the computed values for balanced weights were `0.7314223988`, `0.7324952434`, and `0.7324933341`. At minus weight 0.7 the last two values agree to the displayed precision. The predicted marginal TV from the separate one-dimensional limiting integral is `0.0676953095` for balanced weights and `0.2001343263` for minus weight 0.7; the exact-bath quadrature at N=1000000 gives `0.06769531` and `0.20013433`. This checks the unequal-variance covariance and information formulas, including cancellation of the original phase weights from the information limit. Absolute-value quadratures are not accuracy certificates.

## Proof and scope checks

The author's additional linear-boundary joint-TV CDF formula was independently derived as the difference between tilted and reference probabilities on the set where the likelihood exceeds one. Separate scalar adaptive quadrature for `(alpha,V,p_O)` equal to `(1/3,2.7,0.5)`, `(0.1,2,0.42)`, and `(5,3,0.02)` gave errors below `1.1e-10` against the CDF formula. This is an analytic check plus a numerical consistency check, not a rigorous numerical enclosure.

- The centered bath likelihood is bounded by one globally, making the phase-selection theorem independent of interfacial tail estimates. This differs from the secant calibration used for isolated two-phase accuracy.
- Entropy convergence requires the separate bounded `x log x` argument and bounded marginal likelihood ratios. It cannot be deduced from TV convergence alone.
- At linear capacity, the limiting Gaussian densities evaluate integrals of actual microscopic likelihoods. A discrete microscopic law need not and cannot converge in TV to a continuous Gaussian merely because its standardized energy converges weakly.
- The positive-variance boundary formulas apply to the plain short-range model and kinetic mean-field model. The pure-spin mean-field disordered variance vanishes and must not be silently included in density formulas requiring positive variance.
- Temperature balancing specifies a new common canonical reference sequence before bath tuning. It does not establish accuracy relative to the unbalanced law at fixed coexistence temperature.

## Local primary-source inspection

Inspected the retained text of Ramírez-Hernández, Larralde, and Leyvraz (2008), especially the entropy maxima and Figure 3 discussion: opposite-phase assignment and switching are established prior phenomena. Inspected the ground-state degeneracy discussion in Cohen, Rittenberg, and Sadhu (2015), Section 4.3: degenerate phases contribute order-one information terms in their setting. The paper should credit these precedents and state its contribution as the particular physical-bath scaling and full microscopic error/information theorems.
