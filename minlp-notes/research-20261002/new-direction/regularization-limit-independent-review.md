# Independent review: residual regularization and point precision

Date: 2026-10-02. Verdict: the scoped statements pass. This review covers
the actual [quartic obstruction](regularization-point-precision-obstruction.md)
and [regularization exploration](core-only-noise-regularization-limit.md).
It does not establish a general lower bound for exact point extraction.

The later [conditional rate note](canonical-convex-fiber-regularization.md)
also passes the separate mathematical check below. Its elementary
compact-domain lemma is not presented as a new literature result.

## Mathematical checks

The chain Hessian has diagonal at least 14 and off-diagonal absolute row
sum at most 4, so its stated uniform modulus 10 is valid. Lower-bound
stationarity excludes zero coordinates successively, starting from the
strictly negative first derivative; upper-bound derivatives are positive.
The same reasoning holds after regularization. With the auxiliary
constant `x_0=1/2`, the recurrence therefore gives
`x_i<=x_{i-1}^2/14` for both the original and every regularized minimizer.
Solving this scalar inequality yields `x_n<=14*28^(-2^n)`.

The division-free Hessian identity for the added term
`x_n^2(y-1)^2` is exact: expanding its square leaves the original added
diagonal `2(1-y)^2`, mixed entry `-4x_n(1-y)`, and `y` diagonal `2x_n^2`.
Its remaining chain block is at least `4I`. Thus joint convexity holds
even at `x_n=0`; there is no assumption of a positive residual modulus.
The unique original optimizer has `y=1`, while conditional stationarity
under `lambda*(||x||^2+y^2)` gives
`y_lambda=x_n,lambda^2/(x_n,lambda^2+lambda)`. The uniform chain bound
then forces at least `2^n` ordinary rational parameter bits for even
`y_lambda>=1/2`.

The coefficient-height consequence is also valid. The point `(x*,0)`
has distance one from the original optimizer and gap at most `U_n^2`.
Hence an error bound `dist<=C*gap^theta` requires
`log_2(C)/theta>=2*log_2(1/U_n)>=2^n`. A dimension-independent exponent
would not remove this obstruction: the constant, or the onset radius of
a local estimate, can conceal exponentially many precision bits.

The exploration's canonical projection estimate uses two distinct
facts correctly: Tikhonov optimality gives a norm no greater than that
of the minimum-norm optimal point, and projection onto the convex
optimal fiber gives the stated Pythagorean inequality. Compactness and
uniqueness of the optimal core suffice for qualitative convergence of
global regularized minimizers. They do not provide an effective rate.
The degree-three moving-core example separately verifies that canonical
fiber selection need not be continuous, despite projected quadratic
growth. Its three regularization schedules have the stated different
limits.

## Scope and solver significance

The obstruction applies to exact or accurately tracked isotropic
Tikhonov points. It does not apply to every point returned by an
objective-only approximate oracle. The original example is easy:
setting `y=1` reduces it to a uniformly strongly convex chain. Adding an
independent noisy core preserves this distinction on every draw; it does
not create a hardness result. The proof gives exponential growth in the
number of variables, and thus superpolynomial growth in the explicitly
stated `O(n log n)` input length.

The fixed-law qualification is necessary. A theorem whose finite noise
grid must satisfy `M>=2^J(lambda)` cannot be applied at all positive
regularizers using one finite `M` when its required cutoff diverges.
Resampling for each requested precision changes the objective. This
shows that the proposed composition is incomplete, rather than ruling
out a new fixed-law analysis.

The useful next target is a structural certificate that extracts an
optimal residual section or supports a coordinate oracle without this
vanishing-regularizer schedule. An exact value oracle, a core-point
oracle, and a full canonical-point oracle remain different outputs.

## Compact convex-polynomial growth and conditional rates

The rate note proves the existential bound
`f-f*>=c*dist(.,argmin f)^d` for one degree-`d` polynomial convex on a
compact polytope. I checked each reduction. Polynomial constancy on a
relative interior extends to the affine hull of the optimal set.
Convex combination with a relative interior optimal point cancels the
tangential displacement and gives a feasible transverse point. The
transverse problem has an isolated minimizer. Its polyhedral tangent
directions extend a uniform positive radius, while univariate Lagrange
interpolation bounds growth from below by a constant times radius to
power `d`. The outer part of each ray is handled by monotonicity and
compactness. Finally, the stated finite-cone proof of the polyhedral
error bound is sound: a feasible tangent direction that is normal to
the optimal affine section cannot lie nontrivially in that section.

The fixed-fiber rate uses the sharper pair of inequalities
`c*e^d<=2R*lambda*e` and `||y_lambda-a||^2<=2R*e`, with `a` the
minimum-norm optimum. Both follow from comparison of norms and convex
projection. The mixed-gradient sensitivity term `B/(2lambda)` and the
approximate-solve term `sqrt(eta/lambda)` have the correct normalization.
The global regularizer estimate also correctly compares with the
canonical optimizer before applying projected core growth; it does not
assume uniqueness of the regularized global optimum.

These results supply conditional rates, with the quantitative constant
charged explicitly. They do not overcome the verified exponential
constant example. Comparison with classical error-bound exponents is a
separate literature question, assigned to the literature researcher.

## Verification record

I read the three actual files and independently derived the inequalities
above. The source author's exact symbolic checks are recorded in the
obstruction; I did not duplicate them. A targeted Python check of these
three notes and this review verified local links, control characters,
trailing whitespace, and paired display delimiters. No project-wide
tests or CI checks were run. The only correction requested during this
review was an escaped LaTeX command, now repaired.
