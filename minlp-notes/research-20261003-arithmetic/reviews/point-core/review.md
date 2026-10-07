# Independent audit of the point-output core

Date: 2026-10-03. The two positive point-output theorems pass this
independent proof audit under their stated input promises. The two
degree-four comparisons are reviewed separately in
[the hardness audit](hardness-audit.md), which also passes both reductions.
This is internal mathematical
review, not publication peer review or a novelty determination.

The audit read the complete current versions of
[the global-convex theorem](../../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md),
[the cubic polytope theorem](../../../research-20261002/new-direction/convex-cubic-polytope-point-oracle.md),
and their value, box-cubic, and completion dependencies. Prior review
verdicts were not used to justify the conclusions below.

## Theorem-specific verdicts

| Statement | Verdict | Qualifications that must survive integration |
| --- | --- | --- |
| Effective distance to the optimizer set for a globally convex polynomial | Accept | Explicit rational polynomial of fixed degree; convexity on all of the ambient space; bounded rational polytope with polynomial-bit bounds. |
| Fixed minimum-norm optimizer for the same problem | Accept | Minimum norm is in the original coordinates; requested accuracy is charged as a number of bits. |
| Distance to the optimizer set for a cubic convex on a bounded rational polytope | Accept | Affine-hull reduction precedes the Hessian argument; supplied convexity is a promise. |
| Fixed minimum-norm optimizer for the same cubic | Accept | Regularization uses the original norm after substitution, not the norm of the free-coordinate vector. |
| Square Root Sum constant-accuracy point comparison | Accept | Degree four, convexity on the feasible box, width two, bounded upper coordinate curvature; no uniform lower growth guarantee. |
| PosSLP constant-accuracy point comparison | Accept | Degree four, convexity on the feasible box, unique optimizer; unrestricted width and no uniform strong convexity on the whole box. |
| Global-convex core-completion transfer in Section 7 | Accept as a conditional composition | The underlying selected-core oracle and its probability/work bound remain inherited hypotheses; this audit checks the completion, not the full finite-noise search proof. |

No substantive correction to these historical theorem statements was
identified. The global-versus-domain convexity distinction and output
representations are essential assumptions, not optional explanatory text.

## Reconstruction of the globally convex argument

The central step is stronger than ordinary convex weak optimization.
For a feasible displacement `d=x-y` from an optimizer and gap `E`, the
globally nonnegative Bregman polynomial

```text
h_y(u)=f(y+u)-f(y)-grad f(y)'u
```

is at most `E` on the segment `u=sd`, `0<=s<=1`. Degree-bounded
interpolation controls it at `2td`. Global Jensen convexity then controls
`h_y(c-y+td)` for a rational sample `c`, even when these points lie
outside the feasible polytope. Taking an interval of length `E^(-1/D)`
in the elementary derivative bound gives

```text
|grad f(c)'d| <= (1+J_D W) E^(1/D).
```

I checked the coefficient majorants: both `y` and `2c-y` lie in the
box with radius `U+2D`; the linear Bregman term is bounded by
`2G(D+U)`. The constants therefore do not contain unknown optimizer
heights. The interpolation derivative denominator estimate also bounds
every derivative term at zero, including the node zero. No asymptotic
root-separation assumption enters this calculation.

The zero-gap case is valid without a limiting argument. The segment
Bregman polynomial vanishes identically, and Jensen bounds its shifted
version on the whole real line; that polynomial is constant. Thus two
optimizers differ by a direction annihilated by every sampled gradient.

The integer simplex samples are unisolvent for degree `D-1`: the
falling-factorial basis gives a triangular evaluation matrix with unit
diagonal. Consequently the sampled rational gradients determine exactly
the global translation-invariance space. This proves

```text
argmin_P f = {x in P : A x = A y}
```

for a rational, explicitly computable matrix `A`, although `A y` can be
irrational. Affine objectives require their constant-gradient row; the
construction includes it.

The integer-row Hoffman estimate is sound. Project a feasible `x` onto
the slice, retain independent equality rows, and conically eliminate
dependent active inequality normals modulo their span. In the resulting
independent integer row matrix `R`, the Gram determinant is at least
one and all singular values are at most `nC`. Its least singular value
is therefore at least `(nC)^(-(n-1))`. Active outward inequality normals
have nonpositive inner product with the displacement from the projection
to the already feasible `x`. Dropping their contribution leaves precisely
the equality residual, without multiplying by the possibly irrational
right-hand side. Redundant constraints and relative dimension cause no
exception.

All sample counts, evaluation lengths, denominator products, integer
heights, and exponents in the displayed constant are polynomial in the
input when `D` is fixed. This verifies the claimed computable precision
schedule. It does not by itself establish any bound polynomial jointly
in dimension and variable degree.

## Reconstruction of the cubic argument

The universally tight-row test uses maximum slack equal to zero. A row
that is tight somewhere is insufficient; the note uses the correct
test. Averaging strict witnesses for the other rows proves that the
universal rows describe the entire affine hull. Free-coordinate
parametrization has polynomial rational height and an identity
submatrix, and fixed-degree substitution remains explicit and polynomial
in size.

After reduction the objective has a positive semidefinite affine Hessian
on a full-dimensional polytope. The rational inball is certified by
`a_i'c+rho ||a_i||_1 <= d_i`; positivity follows from full dimension.
Reflecting a feasible point into that ball gives

```text
0 <= H(u) <= (1+R/rho) H(c).
```

The common Hessian kernel is therefore rational and computable. Boundary
Hessians are allowed to have a larger kernel. Third-derivative symmetry
gives the stated center/endpoint identity; positivity of the endpoint
Hessians and exact cubic Taylor expansion then imply the fourth-root
transverse gap bound. The constants in the polytope version are
conservative but valid: its diameter bound `2R` and Hessian bound `2M`
are both sufficient for the box estimate it invokes.

The gradient equality in the optimizer slice is necessary. The Hessian
kernel alone permits nonconstant affine objective motion. The note
retains `g_c'(u-v)=0` and bounds its residual by the value gap plus
`MR` times the transverse displacement. Integer-minor eigenvalue and
Hoffman bounds then have polynomial binary length. The affine and
zero-dimensional branches are handled separately and do not divide by
a missing positive eigenvalue.

## Fixed-selector and feasible-output checks

For either error bound `dist(x,S)<=Gamma gap^(1/d)`, let `p` be the
minimum-original-norm point of `S` and let `x_tau` minimize
`f+tau ||x||^2`. If `s` is nearest to `x_tau` in `S`, and
`e=||x_tau-s||`, optimality and the projection characterization of `p`
give

```text
e^d/Gamma^d <= gap(x_tau) <= 2R tau e,
||x_tau-p||^2 <= 2R e.
```

The second inequality uses both `||x_tau||<=||p||` and
`p'(s-p)>=0`; proximity to the optimizer set alone would not prove a
fixed selector. Substituting the stated `tau` makes selection bias at
most half the requested accuracy. A regularized value gap at most
`tau epsilon^2/4` supplies the other half by strong convexity. Only
`log(1/tau)` and `log(1/eta)` are charged. The original-coordinate
penalty preserves the declared selector under nonorthogonal affine-hull
coordinates and on lower-dimensional polytopes.

I read the local primary GLS text at Definition 2.1.10 and Corollary
4.2.7. The cited theorem gives weak optimization against the eroded body
and permits approximate feasibility; it does not give exact feasible
epigraph output. Both present interfaces correctly account for this.
The capped epigraph contains the stated ball, and homothety from an
exact minimizer toward its center bounds the erosion penalty. The
general value interface repairs feasibility by a rational LP. The cubic
polytope interface instead uses its explicit homothety. For the latter,

```text
u_hat-bar_u = [rho(u-bar_u)+delta(c-bar_u)]/(rho+delta)
```

proves the claimed repair displacement. Both endpoints used for the
gradient loss lie in the polytope. A tangent LP gives an independently
checkable lower bound when that certificate, rather than an internally
certified weak-optimization interval, is requested.

For the global-convex core-completion corollary, the unknown exact core
appears only as a bounded linear tilt. Rational gradient rows for the
known polynomial plus core-extraction rows replace that unknown slope.
The core residual is bounded by `sqrt(2 Delta/beta)` and therefore by a
constant times `Delta^(1/D)`. Equality of the core removes the tilt
when identifying the target slice. The subsequent solve consumes a
short rational approximation to the core, whose uniform objective
perturbation fits the stated regularization budget. It does not require
reading an exponentially expanded fallback representation in ordinary
polynomial postprocessing time.

## Boundaries and further work

The four current development workstreams cover the major gaps exposed by
this audit: literature reconciliation, unbounded/variable-degree global
point approximation, cubic residual completion, and unrestricted exact
constrained comparison. I found no additional theorem whose absence
invalidates the existing positive core.

A sharper cubic error exponent than `1/4` would be a reasonable optional
extension. The scalar example `f(t)=t^3` on `[0,1]` excludes any uniform
exponent larger than `1/3`, but neither this observation nor the present
proof establishes that `1/3` is achievable in general with
polynomial-bit constants. Such an improvement changes the accuracy
schedule; it is not required for the polynomial-time point-output
result. Do not present it as proved or as a prerequisite to integration.

The final report should preserve the hardness audit's distinction
between a conditional reduction and a proved complexity-class
separation. It should likewise distinguish explicit rational coefficients
from succinct arithmetic circuits, bounded upper curvature from an
effective lower growth bound, and fixed-point approximation from exact
active labels or expanded algebraic output.

## Verification record

This audit used complete-file reads of the two positive notes and their
listed dependencies, targeted `rg -n`/`sed -n` reads of the local GLS
source, and independent analytic reconstruction as recorded above.
It did not rerun the historical diagnostic suites: those finite fixture
checks were already recorded by their original authors, and this
review's distinct contribution is proof and computation-model auditing.
No project-wide verification or CI inspection was performed. Document
checks were run with a targeted `python3 -B - <<'PY'` script over the
two Markdown files in this review directory. All six local links,
paired code fences, and whitespace checks passed. The hardness reviewer
separately records its actual arithmetic diagnostic commands and
outcomes in the linked audit; those checks were not rerun here.
