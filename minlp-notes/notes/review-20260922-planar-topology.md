# Independent review of the planar smoothed-region theorem

Date: 2026-09-22. Reviewed source:
[higher-dimensional smoothing](research-20260922-higher-dimensional-smoothing.md).
This review concentrates on the two-coordinate area estimate, multiplicity,
genericity, planar topology, and the interpretation of the result. It also
checks the curvature argument for consistency, but is not a replacement for
a separate review of that analytic step.

**Verdict:** I found no substantive gap in the stated planar theorem. The
conditioning and topology arguments establish the stated constant, provided
the level-set curvature lemma is used with its stated regular-level convention.
One terminology correction is advisable: use “regular affine zero set of a
polynomial of degree at most two” in place of “nonsingular conic.” The result
is a representation theorem, not yet an expected polynomial-time algorithm.
The novelty claim should remain provisional.

## Two-coordinate conditioning

Three distinct binary vectors cannot be collinear: a line through two binary
vectors contains no further binary vector. Thus two coordinates give a
rank-two projection, and the projected vectors occupy three different corners
of the binary square. Each corner triple has one elbow joined to the other
two by coordinate edges.

After fixing all other noise, the four class minima are independent of the
two unrevealed coordinates. Taking equality with the elbow therefore gives
each noise coordinate as a signed difference of two class minima. There is
no larger inverse-matrix factor: the two pattern differences are signed unit
coordinate vectors. Each class minimum is L-Lipschitz, so each row of the
Jacobian of H has norm at most 2L. Hadamard's determinant bound gives 4L².

The area formula applies to this Lipschitz map even where the active support
within a class changes. Its multiplicity integral includes all preimages,
including any unwanted class equalities. Multiplying by the conditional
joint density bound gives 4 phi² L² A. Union over four corner triples and
coordinate pairs gives the stated 16 binom(m,2) factor. The pair witnessing
a junction may depend on the noise; the union is over a fixed finite set of
possible pairs, so this causes no conditioning error.

The same map restricted to an edge has a two-dimensional null image. This
excludes boundary triple ties. A finite multiplicity integral also excludes
an infinite interior triple locus almost surely. Neither step assumes
independence between the exponentially many support costs.

## Multiplicity and regularity

An affine plane has an injective projection onto two appropriately selected
coordinates. Its intersection with the binary cube consequently has at most
four elements. Five distinct binary vectors therefore contain an affinely
independent quadruple. Select three noise coordinates on which the three
difference vectors have a nonsingular minor. Conditional on the remaining
noise, a quadruple equality forces these coordinates onto a polynomial image
of a two-dimensional domain in three-dimensional space. That image has
zero volume. The finite union over possible quadruples proves that no
affine-rank-three co-minimizer set occurs almost surely. In particular, at
most four supports can be active at any point.

Four active supports really can persist under independent continuous noise.
For z in {0,1}², consider

```
q_z(x,y)=z_1 x+z_2 y.
```

For every noise realization with (-xi_1,-xi_2) in the square's interior,
all four supports minimize at that point. The lower envelope is
`min(0,x+xi_1)+min(0,y+xi_2)`, with four surrounding regions. It would be
incorrect to replace the source's argument by an assertion that all
junctions generically involve exactly three supports.

For any distinct support pair, the random offset has a density: condition
on all but one differing coordinate. A fixed quadratic has at most one
critical value when its critical set is nonempty. Avoiding that value makes
its affine zero set regular. This is precisely what the proof needs.
The phrase “nonsingular conic” can be misleading: linear differences give
lines, and a difference such as x² with a noncritical offset can give two
parallel lines, a projectively degenerate conic. Both have the required
local two-half-arc property. No substantive estimate changes.

The edge version is also correct. A quadratic restriction has finitely many
critical values unless constant; the constant case has no zero almost surely.
Fixed corners have no tie almost surely.

## Planar graph accounting

At a point with exactly two minimizing supports, the other finitely many
supports have a strictly positive local gap. The global tie set locally
equals the regular equality curve of this pair. At a point with three or
four minimizers, all locally relevant tie arcs belong to at most six regular
pair curves, giving at most twelve incident half-arcs. Tangencies between
different pair curves do not invalidate this upper bound.

After cutting at interior junctions and boundary crossings, each nonclosed
arc has two ends. A loop returning to the same vertex contributes two ends
there, as required by the handshake count. Boundary crossings have degree
one within the square. Thus the number of arcs is at most 6J+B/2. Isolated
junctions contribute no complementary regions. Semialgebraicity supplies
finitely many graph pieces; no accumulation of arcs has been overlooked.

A component with no junction and no boundary crossing must be a closed loop.
Its active pair is constant along the loop: a change in either support
would produce a triple tie by continuity. Choosing any coordinate where
this pair differs charges the loop to an entire compact component of the
corresponding class-difference level set. That level set is itself part of
the global tie set, so an unnoticed attached branch would also be a global
triple junction. This justifies charging whole loops, not merely subarcs,
to the curvature estimate.

The loop term cannot be omitted. With m=1, branches 0 and -(x²+y²), and a
positive noise value smaller than M², the tie set is an interior circle.
It gives two regions while J=B=0.

Each graph edge or separate loop increases the number of components of the
complement by at most one. Consequently

```
R <= 1+6J+B/2+W.
```

Substituting the source bounds gives exactly the displayed coefficient
96 binom(m,2) phi² L² A and the linear term
`(1+1/pi)m phi L P`. Every connected component of the complement has one
fixed unique minimizer, since changing that minimizer requires a tie.

## Analytic and application checks

The minimum of concave L-Lipschitz functions remains concave and
L-Lipschitz. The gradient jump across a smooth interface is normal to the
interface because the two formulas agree tangentially. Thus the singular
Hessian mass used in the source is the absolute normal gradient jump. The
corner-angle inequality follows from integrating the derivative of
`atan(b/a)` for fixed nonzero a. This addresses the main potential missing
term in a smooth-only curvature argument.

For a finite piecewise-quadratic function, semialgebraic stratification and
the critical-value exclusion make the regular level components embedded
piecewise-smooth curves. A compact connected component then has total
absolute curvature at least 2 pi. I found no conflict between this usage
and the topology argument above. A fully polished presentation should cite
the precise area/coarea theorem and justify the inner-square flux limit,
as the source already sketches.

The indicator-QP Schur complement has the claimed concavity after the
common boundary quadratic is removed. Its gradient is the original cross
term evaluated at the conditional minimizer; the derivative of that
minimizer cancels by stationarity. The diagonal-dominance box bound gives
the stated Euclidean gradient bound with its sqrt(2) factor.

The result bounds regions and therefore the number of support formulas
needed for an exact envelope. It does not explain how to discover those
formulas without enumerating supports. It also supplies only a first
moment, so an algorithm with a quadratic cost in message size cannot use
this estimate alone. The source states these limitations correctly.

## Literature check and significance

I inspected the primary full text of [Brunsch and Röglin, *Improved Smoothed
Analysis of Multiobjective Optimization*](https://arxiv.org/pdf/1111.1546),
including Theorems 3 and 4 and the model discussion. It already gives
polynomial expected Pareto counts and higher-moment bounds for several
perturbed linear objectives and one arbitrary deterministic objective.
Its zero-preserving results broaden that model further. The present
quadratic parameter family has several unperturbed coefficient functions
of a support and only one perturbed penalty vector. I found no reduction
that makes the existing theorems imply the present planar-region estimate.
Conversely, the present result does not replace their higher-moment or
general multiobjective conclusions.

I also inspected [Moitra and O'Donnell, *Pareto Optimal Solutions for
Smoothed Analysts*](https://www.cs.cmu.edu/~odonnell/papers/pareto-optima.pdf),
especially its model in Section 2.1 and its conditional-witness discussion.
It permits one arbitrary objective but independently perturbs the entries
of the other objective rows. The deferred-decision strategy is an important
antecedent of the coordinate-conditioning step here. Polynomial smoothed
representation size and conditional isolation are therefore not themselves
new concepts; the proposed addition is their combination with planar
curvature and support-dependent quadratic parameter functions.

Additional searches used “smoothed analysis parametric optimization two
parameters,” “smoothed parametric lower envelope,” and “smoothed
multiobjective one perturbed objective two arbitrary objectives.” They did
not establish an equivalent theorem or establish its absence. The existing
source correctly treats unsuccessful searching as insufficient evidence
of novelty.

The theorem is a meaningful step toward exact methods with two-coordinate
separators: it removes exponential *expected representation size* as one
obstruction while leaving discovery and arithmetic complexity unresolved.
Calling it a general bounded-treewidth smoothed solver would exceed the
proof. A potentially reusable extension is to finite C² semialgebraic
branches with a common concave Lipschitz normalization: most uses of
quadraticity are finite stratification and critical-value arguments. That
extension has not been established by this review and should remain a
separate question.

## Verification scope

This was an independent mathematical review, including the exact
four-junction and isolated-loop examples above and direct checking of the
constants. No numerical experiment or Lean proof was used. The only local
read was the topic note; the new review file is the only repository change.
No project-wide test or CI check was run.
