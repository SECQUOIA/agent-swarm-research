# Assessment: effective point output for convex and convexifiable cubics

Date: 2026-10-02. This assessment reads the actual
[convex box theorem](convex-cubic-point-oracle.md),
[polytope addendum](convex-cubic-polytope-point-oracle.md), and
[full-point core composition](cubic-core-full-point-oracle.md).
All three now have completed designated independent proof reviews;
the polytope and full-point review statuses were checked again after
the initial assessment.
This is a separate significance assessment, not a replacement for those
reviews or a publication-priority claim.

## 1. The effective error constant is the substantive deterministic step

Convex value optimization was already available locally. With a supplied
positive strong-convexity modulus of polynomial bit length, turning a
value gap into point distance was also routine. The cubic theorem removes
that modulus, uniqueness, and optimal-face premises. It returns distance
to the optimizer set and, separately, approximates its unique minimum-norm
point in polynomial bit time.

The important new local ingredient is a computable rational error
constant whose **logarithm** is polynomial in the input. An existential
Holder bound would not suffice: the reviewed quartic examples have
constants requiring exponentially many precision bits. For a convex
cubic, Hessian affinity and third-derivative symmetry control displacement
transverse to a rational common kernel. The optimizer set is an affine
slice with a known rational coefficient matrix, though its right-hand
side can be irrational. A height-controlled Hoffman bound completes
the conversion. The fourth-root exponent is adequate; sharpening it
would not change the polynomial-bit conclusion.

The polytope extension is chiefly an interface extension, but a useful
one. Relative affine-hull reduction, a rational interior ball, reflection,
and the general-polytope Hoffman bound replace the box identities. It
covers coupled linear constraints and lower-dimensional feasible sets
without assigning a numerical condition parameter to small slacks.
It does not cover nonlinear feasible sets or make convexity recognition
free. The source reviewer reports that the checked classical error-bound
sources did not already supply this effective box-cubic point oracle;
the [completed focused source audit](../prior-art/convex-cubic-point-oracle-prior.md)
remains the authority for prior comparison and leaves priority unresolved.

## 2. The full-point bridge adds something beyond core coordinates

The preceding coupled-core theorem approximates one selected optimal
core while its feasible residual coordinates need not converge. The
cubic bridge instead gives a Cauchy name for a fixed full optimizer:
the minimum-norm point in the fiber of the lexicographically first optimal
core. This is a meaningful additional solver contract, including when
that fiber has positive dimension.

Its completion argument is more than applying the rational cubic theorem
at an approximate core. The exact core can be irrational, and fixing a
nearby core can alter a residual optimizer set. The bridge instead adds
a squared distance penalty centered at the exact selected core and solves
on the original polytope. It describes the target fiber using rational
rows from the convexified cubic, together with core-coordinate rows.
This avoids an error constant depending on the irrational linear tilt.
A short rational core approximation then suffices for a strongly convex
regularized completion. The completion coefficient `alpha+1` affects
precision bits, while the search retains the supplied `alpha` parameter.

The full conclusion is expected fixed-parameter work for one sampled
objective, one finite law, and every accuracy query; every atom remains
correct through fallback. It is not a deterministic solver for the
unperturbed nonconvex cubic. Total degree at most three and a supplied
joint core convexifier are essential premises. Merely convex cubic
residual slices do not give the same rational common-kernel argument.
The convexifier may be numerically large even when residual convexity
and original core upper curvature are well controlled.

For a globally convex cubic, the deterministic theorem already gives
minimum-norm full-point output without noise. The nonconvex cubic
composition is therefore the substantive new smoothed regime. Its
`alpha=0` selected-core refinement should not be presented as the first
efficient point approximation for convex cubics. For quadratics, the
local exact rational reconstruction results already give stronger exact
output.

## 3. The arithmetic barriers distinguish contracts, not a contradiction

| Contract | Relevant local conclusion |
| --- | --- |
| Arbitrary certified objective precision | Available for much broader convex polynomial classes |
| Distance to a convex cubic optimizer set | Deterministically polynomial under the convexity promise |
| A fixed minimum-norm convex cubic optimizer | Also polynomial by effective regularization |
| Exact active-bound recognition for cubics | The reviewed strongly convex cubic construction contains Square Root Sum comparison |
| Constant-distance point output for general convex quartics | The reviewed construction implies a polynomial-time PosSLP algorithm |

The [cubic active-bound reduction](convex-active-set-radical-comparison.md)
already has a uniform strong-convexity modulus. Its positive coordinate
can be arbitrarily small. An accurate Cauchy name cannot in general
decide whether that coordinate is exactly zero, so the new cubic theorem
does not bypass the reduction.

The [quartic point reduction](posslp-convex-point-extraction.md) forces a
designated coordinate to zero or one according to a circuit comparison.
It concerns distance to **any** optimizer, not merely a difficult canonical
choice. The cubic theorem therefore establishes a useful degree-sensitive
boundary in the present methods. It does not prove that quartic point
approximation is impossible, NP-hard, or separated from the cubic case
by a known complexity-class separation. Likewise an always-correct
expected-polynomial extension to that class would have the corresponding
randomized expected-time comparison implication, not automatically a
deterministic polynomial-time one.

Neither cubic theorem promises a short expanded algebraic coordinate.
The local radical constructions can already produce cubic optimizers
with coordinates of exponential algebraic degree. Compact descriptions
with efficient numerical evaluation are the appropriate output here.

## 4. The bounded higher-degree extension

The already-authorized extension treats degree greater than three with
an explicit structured convexifier, rather than arbitrary convex
quartics. Its class is an affine function plus a PSD quadratic
and a sum of positive rational multiples of even powers of rational affine
forms. Scalar uniform convexity directly controls the affine-form
residuals; a rational Hoffman bound replaces the cubic Hessian
argument. The same selected-core completion supplies full-point output
for this nonlinear class; its
[separate saved proof review](../reviews/affine-power-core-point-review.md)
has passed. The variable-coefficient quartic amplifier is
not automatically in that representation.

This authorized extension is developed separately in
[the affine-power corollary](affine-power-core-point-oracle.md); it is not
a consequence silently attributed to the cubic theorem. Its value is a verifiable higher-degree
class with effective point evaluation; the scalar inequalities themselves
are classical. The broader
[globally convex polynomial theorem](globally-convex-polynomial-point-oracle.md)
was already underway when the user requested completion and a stop. It
has now passed two independent actual-file reviews and root's separate
check. Global convexity on all of Euclidean space gives an effective
degree-only error bound through interpolation and rational gradient
samples, and its core-completion result contains the affine-power class.
The cubic theorem remains distinct because it needs convexity only on
the feasible polytope. These extensions are complete; no further work
is initiated by this assessment.

## Verification record

I read the saved three main statements and proofs, the selected-core
interfaces, and the actual cubic active-bound and quartic PosSLP
constructions. I did not duplicate their mathematical diagnostics or
the designated fresh composition review. Literature questions were
routed to the source reviewer; no external search or ingestion was
performed here. A targeted check of this assessment's local links,
whitespace and control characters passed. No index or project-wide
verification was changed.
