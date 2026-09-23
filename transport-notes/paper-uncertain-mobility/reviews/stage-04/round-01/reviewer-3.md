# Independent review: Stage 04, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Snapshot: `da3db325e0812991ad97d79560c4c8aeb99b83d7260ade75d6172d61d3b4aaa6`.

I reviewed all of `sections/04-generic-folds.tex`, its author handoff, and the accepted scalar variational, local Neumann, graded-design, and physical-transfer prerequisites. I did not read other reviewer reports or coordinator checks, edit manuscript sources, or delegate work.

## Uniform geometry and adversarial families

The compact-family hypotheses rule out all unlisted spatial multiple zeros, including ones at parameter endpoints. A finite cover of the zero set by product neighborhoods with a fixed sign of either the first or second spatial derivative gives a uniform root-count bound. The closed zero set outside the fold products has a positive minimum slope. Thus an accumulating number of ordinary roots or an ordinary-root separation tending to zero would contradict the stated assumptions, rather than being an unexamined case of the theorem.

The construction of fold coordinates is valid at the stated regularity. Solving `g_s(z(c),c)=0` gives the moving critical point; the Taylor integral coefficient remains nonzero in a smaller neighborhood. Its square root gives a coordinate with nonzero Jacobian. The signed parameter derivative is `-sigma_j g_c`, and the critical-point drift is O(parameter distance). Therefore root distances, separation, and slopes are uniformly comparable to the square root of the signed parameter on the two-root side. The zero-curve calculation gives `C_j''=-g_ss/g_c` because its first derivative vanishes at the fold.

Distinct fold sites and parameters allow the proof to shrink each local product so that its unfolding roots lie in its retained spatial neighborhood whenever that parameter neighborhood is active. Ordinary-root neighborhoods can then be chosen with fixed radius outside those products. At the boundary of an active parameter neighborhood, the already separated fold roots have a positive fixed separation, so switching to the ordinary-root treatment does not create a small uncontrolled scale. Outside the retained root neighborhoods, compactness supplies a uniform positive rate. This supports the bracketing partitions asserted at lines 116–128.

I checked an explicit allowed family with stationary additional roots: on a circle take `g(s,c)=cos(s)(c+cos(s))`, with `c` in `[0.8,1.2]` and a bounded positive density. It has one fold at `(pi,1)`, satisfying `g_ss=-1` and `g_c=-1`, and two additional stationary simple roots at `pi/2` and `3pi/2`, with slopes of magnitude c. These stationary roots remain within the ordinary-root contribution in the proof. They do not need a nonzero parameter velocity or a root-position probability density. This example does not defeat the theorem's upper bound because the design has a global lower floor proportional to a_R.

An ordinary root occupying another fold's spatial site at a different parameter value likewise does not defeat the bound: the grading exponent is nonnegative, so the fold site is a region of increased, rather than depleted, mobility. The proof does not invoke cosine reflection symmetry or equal slopes.

## Arbitrary-competitor lower bounds

On a one-sided root branch, `|C_j'(u)|` is comparable to r on a shell at distance r. The bounded density with an almost-everywhere lower bound near the fold therefore gives parameter probability comparable to `r du`. A null exceptional density set remains null on each such shell because its parameter map is a diffeomorphism with derivative bounded away from zero there.

The sliding-bump derivative integral has mean at most `Cm/(r ell)`, while its reaction energy is at most `Cr^2 ell^3`. With `ell` proportional to `(m/r^3)^(1/4)`, Jensen for the negative qth power gives `r^(2-5q/4)m^(-q/4)`. This uses local total mass, so oscillatory coefficients, spikes, and zero-mobility regions are included. If local mass is zero, shrinking the bump yields an infinite lower bound as asserted.

A single fixed shell lies in a positively sampled fold neighborhood and supplies the subcritical lower order even if the density vanishes on most other parameter intervals. At criticality, sufficiently separated shell radii give disjoint spatial enlargements and disjoint parameter images, since the parameter displacement is comparable to the square of root displacement. The mass sum is at most M, and convexity gives `N^(7/5)M^(-2/5)` with `N` comparable to `log(1/M)`. Above criticality, the fixed fold-centered bump has source squared of order R squared and energy at most `M/R^2+R^5`; with `R=M^(1/7)`, the response is bounded below by `R^(-3)` on a parameter window of probability proportional to R squared. Additional roots cannot invalidate these lower tests.

## One design and parameter-uniform upper bounds

The distance-to-fold design is positive and bounded for each fixed M. Since the fold sites are finitely many and distinct, its normalization has the three stated forms, with `a_R` comparable to `R^(6+alpha)`. For moment orders at most 2/3 the chosen exponent is zero, protecting all ordinary roots while preserving the required order.

At an active fold, other fold sites are a fixed positive distance away, so the distance function in its small spatial neighborhood equals distance to the active site. The moving critical-point shift is smaller than the root distance. Thus on a root interval of radius proportional to r, the mobility is comparable to `a_R r^(-alpha)` and the kinetic curvature to r squared. The scaled harmonic length divided by r is `(R/r)^((6+alpha)/4)`. Neumann estimates apply with a uniform lower bound on the rescaled interval length. The reciprocal-potential complement, of order `r^(-3)`, is bounded by the same root contribution with the stated ratio.

In the central interval the scaled mobility stays uniformly bounded below, even though its exact shape depends on the distance function. The potential converges uniformly to a quadratic-square potential with nonzero quadratic coefficient, on a fixed interval and compact scaled-parameter set. A hypothetical unit-L2 sequence of vanishing energy must approach a constant because of the derivative lower bound, and the nonzero limiting potential forces that constant to vanish. This proves the required uniform Neumann coercivity. Choosing the interval sufficiently large retains every local root with a margin, and its remaining reciprocal contribution is O(R^(-3)).

On the rootless fold side, bounded coordinate Jacobians give the direct integral of `(|t|+x^2)^(-2)`, hence `|t|^(-3/2)`. Other roots have uniformly nonzero slopes and the global mobility floor `c a_R`, so their contributions are at most `C a_R^(-1/4)` independently of their motion in parameter. The number of intervals is uniformly bounded, and the positive-potential complement costs a constant. These observations establish the full response bounds rather than bounds only for the active fold contribution.

## Moment integration and full-bulk consequence

A finite sum raised to any fixed positive q is controlled by a constant times the sum of qth powers, using subadditivity below one and the finite-sum convex bound above one. Bounded density and the fold-parameter Jacobian give radial exponent

`e=2-3q/2+alpha q/4`.

For q above 2/3 this simplifies to `(8-5q)/(q+4)`; for smaller q, alpha is zero and e stays positive. The root integral is therefore bounded, logarithmic, or lower-endpoint dominated in the stated three regimes. The central term divided by `a_R^(-q/4)` is exactly of order `R^e`. The rootless integral is bounded below q=2/3, logarithmic at that order, and of order `R^(2-3q)` above it. This checks both intermediate thresholds, including their lower-order terms. At q=8/5 the central and rootless terms contain one fewer logarithm than the main term. Above 8/5 the ordinary-root contribution is lower order because e is negative.

The rate anchor follows from continuity on the compact family: an integral minimum of zero would force an identically zero spatial profile, violating the finite multiple-zero set. The accepted full-bulk comparison is therefore applicable with family-uniform rate constants. Each scalar lower order dominates the required logarithmic growth scale. Consequently the exact physical/scalar ratio follows even though only two-sided orders, and no sharp scalar coefficients, have been proved for this generic family.

## Findings and verdict

No major or minor issue identified. The assumptions cover the geometry and sampling actually used, the proof protects extra stationary roots, and its parameter-dependent partitions and moment bounds are uniform. The exclusions of simultaneous folds, vanishing fold density, higher degeneracy, and uncertain fold sites accurately delimit the result. I recommend accepting Stage 04 subject to the coordinator's assessment of all five independent reports. This review establishes no generic sharp coefficient or new literature-priority claim.
