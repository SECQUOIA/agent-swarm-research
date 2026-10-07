# Prior-art audit: selected-coordinate output under finite convex tilts

Date: 2026-10-02. This focused audit compares the reviewed
[joint convex core-point theorem](../new-direction/joint-convex-core-point-oracle.md)
with low-dimensional polynomial perturbation algorithms, weak convex
optimization, generic tilt results, and nearby project theorems. It is a
scoped comparison, not a priority claim.

## Candidate contract

The input is a bounded rational polytope `P`, a fixed-degree explicit
rational polynomial `F0` convex on `P`, and selected coordinates
`v in [0,1]^k`. The input includes a polynomial-time-verifiable convexity
certificate or the cost of verifying it. One finite endpoint-inclusive
rational product law is selected from the base input and adds independent
linear coefficients only to `v`:

```text
F_gamma(x) = F0(x) + gamma'v.
```

For every sampled `gamma` and every requested `q`, the algorithm returns a
feasible rational point and a certified interval of width at most `2^-q`
for the sampled global value. Its `v` coordinates are within `2^-q` of the
core of a fixed lexicographically selected optimizer of that same sampled
instance. Expected bit work and proof/output size are `poly_d(I+q)`, with
one fixed noise law and a single random work factor valid for every `q`.
There is no inverse-noise, inverse-curvature, or condition parameter in the
polynomial bound; the binary representation of the noise width is included
in `I`. Correctness is per draw, including atoms with ties. Coordinates not
in `v` need not approach any selected optimizer.

The theorem optimizes the perturbed instance. It does not recover an
optimizer of the unperturbed `F0` merely because its noise is small. It
also does not promise an expanded algebraic representation of the sampled
optimizer. If all variables are eligible unit-box coordinates and all are
selected, the same statement becomes a full selected-point Cauchy output
for the sampled objective.

## Value output is standard for this convex sampled problem

For each fixed rational `gamma`, the candidate's sampled objective is
convex on the rational polytope. Its feasible point with a certified
`2^-q` objective gap and its rational value interval can therefore be
obtained by ordinary rational weak convex optimization: tangent gradients
give separation, and the project's reviewed GLS interface supplies
feasibility and objective repair. This is polynomial in `I+q` for fixed
degree. Neither randomization nor growth is needed for value accuracy.

Weak convex optimization does not generally return a point near a selected
optimizer when the objective is flat or has very small growth. The
candidate's substantive output is the `2^-q` Cauchy bound on the selected
noisy coordinates, with no growth modulus supplied and no numerical
condition factor in expected work. Its buffered near-optimal sublevel
construction and `2k` coordinate extrema create a verifiable hull; a
quantitative random-tilt growth tail makes the same-draw exact fallback
rare. The random law is fixed for every future `q`.

## Broader low-dimensional perturbation antecedent: Kannan–Rademacher

Kannan and Rademacher's “Optimization of a Convex Program with a Polynomial
Perturbation” is a close and broader algorithmic antecedent. They minimize
an arbitrary convex function `f` plus a polynomial `p` supported on `k`
variables over a convex body. Theorem 4 in §3 returns a feasible point with
objective error at most `epsilon * range_K(p)`, using a grid in the selected
coordinates. The stated cost is

```text
O((k d^2 / sqrt(epsilon))^k) (T(f,K) + T_tilde(K)),
```

where `T(f,K)` is the cost of solving the unperturbed convex problem and
`T_tilde(K)` is the cost of putting the body in near-isotropic position.
The algorithm handles a broader perturbation class, including nonconvex
polynomials `p`, and already establishes that low-dimensional dependence
can make a convex program with a structured polynomial perturbation
approximable.

In the candidate's specialization, `p` is a random linear tilt supported on
the selected coordinates. Kannan–Rademacher's bound is not the strongest
baseline for value output here: since the whole sampled objective remains
convex, the standard GLS oracle gives arbitrary absolute value precision in
polynomial bit time directly. If one instead invokes Kannan–Rademacher's
relative-to-`range_K(p)` guarantee for absolute precision `2^-q`, then
`epsilon <= 2^-q/(k sigma)` and the stated grid factor becomes exponential
in `k q`. More importantly, that guarantee does not locate a selected
optimizer when the objective is flat or weakly curved. Kannan–Rademacher
should therefore be credited as a broad low-dimensional polynomial-
perturbation precedent, especially for nonconvex `p`, while the direct
convex value oracle and selected-coordinate output are distinct comparisons.
The candidate's point-output difference is its finite-law, expected
ordinary-bit-polynomial Cauchy bound for selected noisy coordinates, with
same-draw fallback. This is a scoped comparison, not novelty by absence.

The primary text inspected was the author-hosted
[full PDF](https://www.math.ucdavis.edu/~lrademac/fplusp.pdf): Kannan and
Rademacher (2009), *Operations Research Letters* 37(6), 384–386, DOI
[10.1016/j.orl.2009.07.002](https://doi.org/10.1016/j.orl.2009.07.002),
§3 and Theorem 4 (author-PDF p. 4). The exact runtime multiplies
`T(f,K)+T_tilde(K)` by the grid factor; Theorem 3's randomized near-isotropic
rounding routine is on p. 3. The full author text is now read in the local
package
[`kannan2009-optimization-of-a-convex-program`](../../literature/papers/kannan2009-optimization-of-a-convex-program/paper.md).

## Weak convex optimization supplies values, not a selector

For each fixed rational tilt, the sampled objective remains convex. The
standard Grötschel–Lovász–Schrijver weak-optimization framework therefore
provides a rational feasible near-optimal point and certified value
approximation when the polynomial tangent separation oracle and rational
feasibility repair are supplied. This is a classical component used by the
candidate. In general, however, objective accuracy alone does not locate a
chosen optimizer: flat optimal faces or a small transverse growth constant
can leave far-away near-optimal points.

The candidate obtains a buffered convex near-optimal sublevel set and uses
`2k` weak optimizations to bound its selected-coordinate ranges. If their
diameter is small enough, that one feasible near-optimal point certifies
the requested core accuracy. A random-tilt projected-growth tail makes
failure rare; failure triggers an exact same-draw lexicographic fallback.
The sampling law is chosen once from the base input, so the same draw
supports every later value and coordinate-accuracy query. The GLS source
and exact oracle conventions are detailed in
[`convex-patch-evaluation.md`](../new-direction/convex-patch-evaluation.md).
The new step is not a replacement weak-optimization algorithm; it combines
standard weak optimization with a finite-law growth estimate and a
coordinate-hull certificate.

## Generic tilts and finite perturbations

Lee and Phạm's semialgebraic results give the closest qualitative
genericity baseline. For a fixed compact semialgebraic feasible set,
Theorem 6.1 of their 2016 paper gives an open dense semialgebraic set of
polynomial objective coefficients for which the optimizer is unique and
satisfies global quadratic growth with some positive constant. Their 2017
Theorem A treats generic linear tilts of a fixed regular semialgebraic set:
nearby tilts have unique minimizers, uniform local quadratic growth, and a
separate global sharp-minimum inequality. These establish qualitative
uniqueness and sensitivity under generic perturbation. They do not give a
quantitative probability tail for the growth constant, an ordinary
polynomial bit-work algorithm, or a guarantee for a prescribed
finite-support tilt law. The 2017 result also perturbs in the full ambient
linear-objective space, while the candidate may perturb only a selected
coordinate subspace. Source locators and exact assumptions are recorded in
the existing [core-only-noise audit](core-only-noise-boundary-recourse-prior.md).

For finite feasible sets, Beier and Vöcking's random-objective
perturbation result isolates the best and second-best objective values.
That is the discrete winner-gap analogue, not a continuous optimizer
growth estimate. On a continuum, there need not be a second-best point at
positive objective distance. The candidate instead controls how objective
gap forces closeness in the selected projection, and handles finite-grid
ties by fallback. The precise comparison is in the project's
[proximal-growth-tail audit](proximal-growth-tail-prior.md).

## Relation to nearby project results

The closest existing point-output result is the reviewed
[all-scale core-only Cauchy theorem](../new-direction/core-only-noise-core-oracle.md).
For arbitrary `k`, it gives selected-core Cauchy output under one fixed
finite law, with expected work
`f_d(k)(1+L/sigma)^k poly_d(I+q)`. It applies on a product box when fixing
the core leaves convex polynomial recourse and core diagonal curvature is
bounded; the full objective may be nonconvex in the core. The new theorem
trades that broader nonconvexity for joint convexity on an arbitrary
bounded rational polytope, and under that stronger convexity removes the
`f_d(k)(1+L/sigma)^k` factor. It keeps the selected-core Cauchy output,
without requiring a coordinate-curvature bound. The related
[all-scale value theorem](../new-direction/all-scale-core-value-oracle.md)
has the same nonconvex-core FPT setting but gives value accuracy only.

The following internal result handles a different tradeoff:

- The [strongly convex residual theorem](../new-direction/core-only-noise-boundary-recourse.md)
  gives exact implicit full-point output under core-only noise for arbitrary
  core size, but assumes a certified uniform residual strong-convexity
  modulus and its work depends on the curvature-to-noise ratio. The present
  theorem allows flat residual directions and makes no condition-number
  promise, while only selected coordinates are Cauchy-controlled.
- The [quartic SRS point-output comparison](convex-point-radical-prior.md)
  shows that point output for an unperturbed jointly convex quartic can
  encode Square Root Sum. It does not contradict a solver for a sampled,
  randomly tilted instance: the perturbation changes the objective, and
  converting its optimizer to an optimizer of the original problem would
  require a separately justified noise scale and gap bound. The candidate
  makes no such recovery claim.

The exact rational convex-QP source is another clean boundary. Kozlov,
Tarasov, and Khachiyan provide deterministic polynomial-bit exact values
and attaining points for convex QPs, including singular Hessians. The
candidate's smoothed selected-coordinate theorem matters for general
fixed-degree convex polynomials and partial coordinate output; it is not
needed to solve convex QP exactly. The primary source and its rational
denominator-clearing qualification are documented in
[`kozlov1980-the-polynomial-solvability-of-convex`](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md).

## Assessment

The checked antecedents already cover low-dimensional polynomial
perturbations with accuracy-dependent grid enumeration, ordinary weak
convex value optimization, qualitative generic growth under tilts,
discrete winner-gap isolation, and an internal all-k FPT selected-core
Cauchy theorem for nonconvex core objectives. Under joint convexity, value
accuracy itself is standard. The candidate's specific distinction is a
fixed finite rational law on selected continuous coordinates, expected
ordinary bit-polynomial work in `I+q` for selected-core Cauchy output, and
correctness for every draw through a same-draw exact fallback when the
selected core is not well separated. Residual coordinates may remain
nonunique, and the theorem does not enumerate critical regions.

This does not establish a novel algorithmic class or first publication.
Kannan–Rademacher is particularly close conceptually, so any eventual
novelty statement should name its broader low-dimensional perturbation
model and then state the candidate's stronger bit-precision/output target
carefully. The sampled-objective qualifier, convexity certificate cost,
and selected-coordinate-only selector are all material.

## Source access and scope

- Kannan–Rademacher's six-page author-hosted PDF is read in the local
  primary-text package linked above.
- The project's all-scale value and selected-core Cauchy antecedents are
  linked above; their scope and cost are taken from the reviewed local
  theorem notes, not external literature.
- Lee–Phạm, GLS, Beier–Vöcking, and KTK sources are available as read
  primary-text packages or in the linked prior audits.
- Ahmadi–Hall's box-convexity hardness result is a relevant boundary if
  polynomial-time recognition is proposed; the cubic-point audit records
  the primary text and source-access status.

No KB indexes, topic pages, or literature packages were edited by this
audit.
