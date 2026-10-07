# Independent review of the residual-convex cubic point extension

Date: 2026-10-03. Verdict: the completed argument passes this independent
mathematical review, relative to its stated predecessor interfaces. No
blocking gap was found. This is an internal proof review, not a claim of
publication priority or an implementation of the general solver.

## Files and scope

The reviewer read the actual complete files:

- [Full theorem](../../cubic-recourse/theorem.md).
- [Lattice certificate](../../cubic-recourse/lattice-certificate.md).
- [Contact and finite-noise margin bounds](../../cubic-recourse/margin-tail.md).

The review also read the predecessor's
[residual-convex cubic structure and conditional error bound](../../../research-20261002/new-direction/residual-convex-cubic-boundary.md),
[selected-core interface](../../../research-20261002/new-direction/core-only-noise-core-oracle.md),
and [convexifiable cubic completion argument](../../../research-20261002/new-direction/cubic-core-full-point-oracle.md).
The all-scale value theorem was consulted for its fixed mesh and common
random work factor. This review does not repeat the entire inherited
quantifier-elimination, cell-counting, or convex value-oracle proofs.

The new result concerns an explicitly represented rational cubic on a
product box, convex in the residual variables for every core. One finite
core perturbation supports approximation of a fixed full optimizer at
every requested precision. The result removes the joint quadratic core
convexifier assumption in this setting. Arbitrary coupled domains, degree
four, exact algebraic output, and solving the unperturbed objective are
outside its conclusion.

## Sound certificates, including exceptional draws

The nearby-tilt face test is sound for every original global optimizer,
not merely the selected one. After projecting every other variable out,
the scalar value function is semiconcave with upper curvature `Lbar`.
Two interior minimizing contacts for slopes differing by `t` must be
separated by at least `t/Lbar`. Monotonicity orders their coordinates.
The strict test on the *certified interval endpoint* therefore forces
the original coordinate to its box endpoint. The two opposing tests
cannot conflict. No approximate equality is promoted to exact equality.

For a fixed choice of all other noise coefficients, failure to detect an
actual lower endpoint confines the remaining coefficient to the interval
`[theta,theta+t]`, where `theta` is the exact supporting-slope threshold
at zero. The reflected argument handles the upper endpoint. The stated
finite-grid mass bound is conservative and remains valid at ties and
threshold atoms.

The lattice certificate correctly separates sound acceptance from a
sufficient condition for acceptance. A tested polynomial of height at
most `B` and value at most `sB/T` produces a nonzero lattice vector of
length at most `sqrt(5)sB`. The LLL approximation guarantee and the
strict acceptance threshold rule out that vector. Consequently an
accepted certificate excludes exact zeros in this tested family.

For the success analysis, the proof enlarges the coefficient family to
height `R`. This is necessary: a short lattice vector can have
coefficients larger than `B`. The stated condition `T mu_0>(s+1)R`
forces every nonzero lattice vector to have length greater than `R`
and therefore makes the test accept. Neither proof enumerates the
polynomial family.

Uniform denominator and coefficient bounds cover the minors on every
original face. An identically zero minor is harmless. A minor that
vanishes only at the exact selected core makes its nonzero scaled
polynomial fail the certificate. Similarly, an endpoint missed by the
face tests makes a free coordinate polynomial vanish and prevents
acceptance. An exact vertex needs no lattice test. These cases justify
using the predecessor's conditional error bound on every accepted draw.

## Probability and the finite law

The contact-gradient argument in the margin note is complete. A
semiconcave value function with an affine lower support at an interior
point has a unique contact slope and a quadratic upper support with
the same linear part. For two nearby contact points, applying these
supports at a displacement in the direction of their slope difference
proves the local Lipschitz estimate. The displacement stays inside the
face on a sufficiently small interior ball. A countable cover and a
disjoint measurable partition then justify the image-volume bound.
This does not assume continuity of any residual optimizer selector.

The quadratic sublevel bound also checks. A nonzero square coefficient
allows coordinate slicing. When only mixed quadratic coefficients are
present, rotating the two relevant coordinates gives leading magnitude
at least `1/2`; the projected cube has volume `sqrt(2)`. Linear and
constant cases are treated separately. The resulting `8 sqrt(mu)`
bound is independent of dimension and of the coefficient upper bound.

The finite-law event is defined by a face optimizer witness and a
universal competitor block. It includes every global optimizer on
that face, so using face minimization only enlarges the bad event.
The quantifier format has bounded degree and polynomially many
variables and atoms. Applying the inherited scalar-section bound and
replacing marginals one at a time handles arbitrary mixed continuous
and discrete conditioning measures. It includes exact-zero atoms.
The opposite perturbation signs in the theorem and margin note are
equivalent because the endpoint-inclusive law is symmetric.

Although the union ranges over exponentially many faces and
bounded-height polynomials, its cardinality has a polynomial-length
logarithm. It therefore changes the base precision and mesh bit length,
not the number of polynomials inspected by the algorithm. A large full
core Hessian bound enters only this precision budget. It does not
replace `L` by that larger numerical bound in the final expected-work
parameter.

## Selector, completion, and work bound

The declared selector is the lexicographically first optimal core,
followed by the minimum-norm optimizer of that exact residual fiber.
Residual convexity makes the second selection unique. The fallback's
fixed-block formula describes this same point. Thus ordinary output and
fallback output converge to the same point, including on tied draws.

On acceptance, the supplied minor and face margins give a computable
fourth-root fiber error bound with a polynomial-bit constant. The
regularization argument uses that bound at the exact selected core.
It solves a rational convex problem at a nearby core only after
controlling the objective perturbation uniformly in the residual
variable. The stated powers and constants imply both the norm-selector
error and the error from the final convex solve. Clipping and fixing
certified core endpoints preserve feasibility and cannot increase core
error. This avoids the invalid assumption that exact residual solutions
at arbitrary approximate cores converge to the minimum-norm selection.

The order of base choices avoids circularity: choose the original
fallback factor, face tilt, polynomial margin, and lattice scale first;
instantiate the finitely many shifted-baseline core evaluators next;
then choose a common sufficiently fine noise mesh. Every shifted
baseline has polynomial input length, and its core second derivatives
are unchanged. The inherited mesh requirements are lower bounds.

All certificate failure probabilities refer to a single base event.
The exponentially expensive full fallback is charged to that event,
whose probability is inversely proportional to its base cost factor.
The sum of the original and shifted core evaluators' common work
factors, plus this fallback charge, bounds all precision queries at
once. No independence between those factors and the failure event is
needed. No union over requested accuracies or resampling occurs.

## Corrections and verification boundary

The review requested replacing “original objective-gap certificate” by
“sampled objective-gap certificate.” The theorem now uses the latter.
This matters because the perturbation theorem does not certify the
unperturbed optimum at the same cost.

The reviewer also inspected
[the author's exact diagnostic](../../cubic-recourse/check_cubic_recourse.py).
It exercises LLL acceptance, bounded-height polynomial margins, exact
boundary relations, nearby-tilt face decisions, and minimum-norm
completion on a discontinuous residual-selector example. These are
small exact fixtures, not a general implementation or a proof of the
probability estimate. The reviewer did not rerun the author's already
passing diagnostic. The author added the requested clarification that
the `a=1/2` fixture uses a short relation outside the tested height
family, for which conservative rejection is permitted.

An inline `python3 - <<'PY'` validation command passed all eight local
Markdown links, trailing-whitespace checks, and code-fence balance for
this review. No project-wide checks or CI inspection were performed.
The review's confidence in the theorem comes from the derivations above,
with the predecessor interfaces explicitly inherited.

## Integrated section review

The reviewer also read the complete
[integrated cubic section](../../document/sections/06-recourse.tex).
Its assumptions, lattice constants, fixed selector, shared finite law,
fallback budget, and completion precision agree with the reviewed
companion proofs. It states the weaker but valid parameter dependence
with an unspecified computable `f(k)`.

The review caught an ambiguity in the condensed kernel statement.
The author corrected it to distinguish the common kernel inclusion
`ker H_A subseteq ker H(v,z)` from equality for `H(v,c_z)` when the
core lies in the relative interior of the face. Individual residual
boundary Hessians can have larger kernels. The fiber identity is now
explicitly conditional on that core interiority, which the subsequent
lattice acceptance certifies. The reviewer read the corrected paragraph.
With these clarifications, the integrated section passes the spot-check.
The author reports its separate scoped compilation; this reviewer did
not rerun that build.
