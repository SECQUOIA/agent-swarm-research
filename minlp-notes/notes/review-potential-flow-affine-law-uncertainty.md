# Independent review of affine constitutive-law uncertainty

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/potential-flow-affine-law-uncertainty-investigation.md`,
including its later continuous-law smoothing addendum.

**Verdict: PASS for affine coefficient-box uncertainty, polynomial-time
uniform-monotonicity validation, and the C0 extension.** Only the maximum
block cycle rank needs to be fixed under the explicit dense polynomial
representation. The initial C1 version and the subsequent centered
smoothing argument are both sound. This review establishes correctness
within the stated uncertainty model, not novelty.

## Physical states and the nomination face family

For every fixed coefficient vector, the complete law is continuous,
strictly increasing, zero at zero, and finite-piece polynomial. Its
outer pieces cannot be constant, so it is unbounded in both directions.
The same coercive strictly convex energy argument gives a unique
physical flow. The sign condition again makes the physical flow
orientation acyclic, giving the common bound `|x_e|<=B`.

No positive scalar resistance multiplier is needed for this argument:
it is strict monotonicity of the **complete** law that supplies strict
convexity. Individual basis functions may have negative derivatives,
and coefficient intervals may include negative values, provided every
complete law is admissible as required.

Physical solutions depend continuously on nominations and coefficients.
For a sequence of inputs, flows have the uniform bound `B`, and
normalized potentials are bounded by sums of the uniformly bounded
complete laws over paths. Every convergent state subsequence satisfies
the limiting conservation equations and laws. Their uniqueness fixes
the limit. Compact uncertainty sets therefore give joint extrema.

At a joint optimizer, fix its coefficient vector and apply the reviewed
nomination-face theorem to its strictly monotone laws. The face family
is independent of their coefficients. This transfers an optimizer to
the same one-active-block family. Independent coefficient boxes then
allow separate optimization of block drops once the nomination face
has been fixed. A coefficient shared between different blocks would
not justify this separation; the displayed model has separate
`theta_ej` coordinates and does not permit that coupling.

## Fixed-core algebraic mapping

Take the common refinement of all basis breakpoints on each edge.
The total count is at most the explicitly listed input count; no
Cartesian product of piece choices is needed. After affine flow
parameterization, these breakpoints give hyperplanes in the fixed
nomination/circulation core. On a cell, all basis values are
polynomials in that core.

Every uncertain scalar coefficient is a compact rational interval
leaf. The cycle equations are linear in those leaves, with their
fixed-law terms moved to polynomial core right-hand sides. Potential
difference is a polynomial core term plus a leaf-linear sum. Edge
flow is an affine core-only objective. Thus all local problems fit
the reviewed fixed-core support representation.

The degree/piece strengthening was checked separately in
`notes/review-potential-flow-polynomial-laws.md`. For these scalar
boxes, support endpoint selection uses signs of polynomial support
scores and needs no core-dependent denominators. Fixed core and
support-direction dimension gives polynomial complexity in the dense
degree, polynomial count, and coefficient bits. Original piecewise
polynomials remain the objects used in the exact algorithm.

Exact edge-flow optimization takes place in one block. At fixed
coefficients, the target law is strictly increasing, so maximizing
its flow is equivalent to maximizing its endpoint potential
difference over nominations. Reversing the objective handles its
minimum without requiring odd laws. The fixed-core exact algebraic
algorithm and comparison over the enumerated faces therefore give
the stated exact extrema and robust rational capacity decisions.
There is no sum of independent block values for this objective.

## Sensitivity with affine coefficients

For the C1 version, smoothing the complete law by `rho x` gives
electrical resistance `g'_e(x_e,theta_e)+rho>0`. Its upper bound is
the stated `M_e+rho`. Differentiating the law at fixed nominations
gives

```
partial F_rho/partial theta_ej = j_h,e f_ej(x_e).
```

The unit-source/unit-sink electrical adjoint satisfies `|j_h,e|<=1`.
The nomination derivative is bounded by its effective resistance,
which is no larger than the derivative-resistance sum on a fixed
terminal path. Integrating these two bounds along admissible box
segments proves the displayed joint Lipschitz estimate. Every
intermediate coefficient vector remains admissible by the uniform
law hypothesis.

The coefficient-sum constants have polynomial binary length for
dense input degrees and explicit piece lists. Isolating algebraic
coordinates to rational boxes, recovering balanced nominations by
rational LP, and rounding coefficients inside their intervals
therefore gives the promised rational near-optimal pressure inputs.
The rounded inputs have their own unique physical solution; no
claim about rational physical flows or retaining the old circulation
coordinates is needed. Exact edge-flow values likewise require no
quantitative inverse-law modulus.

## Polynomial-time validation of the whole coefficient family

On a common original polynomial piece, minimization of the derivative
over the independent coefficient box is exactly

```
f'_e0(x)+sum_j min(theta_lower_ej f'_ej(x),
                  theta_upper_ej f'_ej(x)).
```

This is valid even for negative coefficients or nonmonotone basis
functions. Nonnegativity of this envelope for every `x` is equivalent
to nonnegativity of every complete-law derivative. Partitioning by
the roots of nonzero basis derivative polynomials fixes every endpoint
choice; the envelope is then one rational polynomial on each interval.

Identically zero derivative polynomials must be omitted from root
partitioning. The author added this clarification during review.
Roots can be isolated and ordered using the product of the remaining
rational polynomials, whose degree and coefficient length remain
polynomial in dense input. There is no need to form a field containing
all roots simultaneously. Exact univariate sign tests handle each
resulting interval, including outer unbounded intervals. Continuity
handles values at the partition boundaries.

Nonnegative derivatives alone would admit flat laws. The additional
LP test is exactly the needed strictness condition. A parameter vector
makes the derivative identically zero on a common original piece
if and only if its rational polynomial coefficients all vanish.
These are linear equations in the uncertain coefficients. Intersect
them with the coefficient box and test feasibility by LP.

If such a vector exists on any nonempty piece, that admissible law
is constant on an open interval and is not strictly increasing.
Conversely, a continuous nondecreasing function that fails strict
increase is constant on some nontrivial interval. With finitely many
pieces, part of that interval lies inside one nonempty original
polynomial piece, forcing its derivative polynomial to vanish
identically. Thus the collection of LP tests is necessary and
sufficient once derivative nonnegativity has passed.

For illustration, `g(x,theta)=x+theta|x|` on `theta in [-1,1]` passes
nondecreasingness but fails the LP test at the two endpoint parameters,
which flatten one half-line. The box `[-1/2,1/2]` passes strictness.
The family `(1-theta)x^3+theta x`, `theta in [0,1]`, passes strictness
despite a zero derivative at `x=0,theta=0`; the LP correctly excludes
flat intervals rather than isolated zero derivatives.

## Continuous laws: the centered smoothing addendum

The C0 extension also passes. A continuous finite-piece polynomial
is Lipschitz on each compact interval, with constant bounded by its
piecewise derivative magnitudes. A nonnegative smooth compactly
supported mollifier produces a smooth nondecreasing convolution of
every nondecreasing complete law. Subtracting its value at zero
preserves monotonicity and forces value zero at zero. Adding
`rho x` then gives derivative at least `rho`.

Centering is essential to the argument: it preserves the flow/drop
sign correspondence and hence the uniform acyclic-flow bound.
The centered convolution operator is linear, so the law remains
affine in its coefficients. Compactness of the coefficient box and
the basis-wise Lipschitz bounds give uniform convergence to the
original laws as `rho` tends to zero. The bounded-state and uniqueness
argument above gives uniform physical-flow and normalized-potential
convergence as well.

Therefore these smooth laws can be used in the existential
nomination-face proof and then removed by the finite-face limit.
They need no effective polynomial representation: the algorithm
enumerates the resulting graph-defined faces and solves the original
continuous piecewise-polynomial laws exactly on their cells.

For `0<rho<=1`, the enlarged interval `[-B-1,B+1]` contains all
arguments of the convolution on physical flows. If basis values
there are bounded by `N_ej`, the centered smoothed values are bounded
by `2N_ej`. The derivative of the convolution is bounded by the
original piecewise derivative bound, using its almost-everywhere
derivative. Consequently the stated enlarged-interval path constant
and the safe coefficient factor `2N_ej` prove the new Lipschitz
estimate. These constants retain polynomial bit length.

Uniform monotonicity validation needs only value matching at
breakpoints in the C0 case. Derivative nonnegativity on the open
pieces and the same no-flat-piece LP criterion characterize strict
increase. Derivative jumps themselves introduce no extra condition.

The result remains restricted to fixed rational breakpoints, dense
polynomial coefficients, independent coefficient boxes, and uniformly
strictly increasing complete laws. It neither admits uncertain
exponents/breakpoints by analogy nor removes the distinction between
additive pressure optimization and exact arc-flow comparison.
