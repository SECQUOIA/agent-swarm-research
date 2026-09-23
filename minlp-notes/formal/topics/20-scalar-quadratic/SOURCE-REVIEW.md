# Independent source inventory: scalar quadratic precision

Review date: 2026-09-20. This inventory identifies the mathematical scope
before proof implementation. It is not a claim that the obligations below
have already been formalized or checked by Lean.

## Sources and boundary with topic 26

The topic-20 entry in [the recommended-topic plan](../../RECOMMENDED-TOPICS-PLAN.md)
requires rank and inertia laws, unrestricted-integer lower bounds, and
matching explicit approximation constructions. The primary result notes are
[the rank law](../../../results/quadratic-rank-integer-complexity.md) and
[the inertia law](../../../results/quadratic-inertia-one-sided-integer-complexity.md).
Their manuscript counterpart is the section `sec:scalar-quadratic` in
[01-foundations.tex](../../../paper-integer-dimension/sections/01-foundations.tex),
including its epigraph/hypograph subsection. The scalar square law and
representation/parity definitions earlier in that file are necessary
dependencies. The [square and product note](../../../results/mip-relaxation-binary-lower-bounds.md)
also supplies those dependencies.

The section `sec:ncrank`, following the scalar section in the same file,
begins the broader simultaneous quadratic-system theory. It belongs to
topic 26, as does most of
[02-quadratic-finite.tex](../../../paper-integer-dimension/sections/02-quadratic-finite.tex).
That file is not the primary source for topic 20. Topic 20 does not include
the general vector covariance, noncommutative-rank, allocation, rational
algorithm, or later nonlinear precision claims merely because they occur
in the same manuscript.

The general strong-curvature and shared-product-graph theorems preceding
the scalar section are likewise not new topic-20 headlines. Their special
cases needed for scalar quadratic lower bounds and the exact square law
must nevertheless be proved. No headline scalar result may be reduced to
a conditional theorem assuming the geometric or formulation conclusion
that its source establishes.

## Representation conventions that must survive formalization

The input box is bounded and full-dimensional: every side satisfies
`l_i < u_i`. Its dimension may be zero; then the function is affine.
The Hessian is real and symmetric, and all formulation coefficients may
be real. Affine coefficients do not affect the error or integer counts.

A convex integer lift uses a finite number of continuous auxiliaries and
`p` unrestricted integer coordinates. Its common lifted set is convex;
it need not be closed, polyhedral, or bounded. A binary linear lift uses
an actual finite system of affine inequalities/equalities. Merely
exhibiting a finite union, a piecewise formula, or an unspecified convex
set does not establish the advertised binary linear upper bound or its
row and variable counts.

Graph containment means every exact graph point has a lift. Accuracy
means every admitted point over the domain has the stated vertical error.
Epigraph containment includes every `w >= f(x)`, with no upper output
bound. Hypograph containment includes every `w <= f(x)`, with no lower
output bound. Binary lifts are admissible convex integer lifts after
imposing the usual bounds on their integer coordinates.

The minimum-count statements require actual minima or an equivalent
proved least-count characterization. Their finiteness for positive
accuracy follows from the explicit constructions. The `O(1)` laws mean
a uniformly bounded additive difference for all sufficiently small
positive tolerances, with fixed Hessian and box. A result only along a
dyadic sequence, or only a ratio limit, does not by itself establish this
bounded-error assertion.

## Complete scalar obligation inventory

The identifiers here label source obligations, not final Lean declaration
names. The frozen claims and final coverage map should preserve their
substance even if the proof decomposition changes.

| ID | Source statement and required conclusion |
|---|---|
| M1 | Arbitrary convex integer lifts produce at most `2^p` parity contact classes. Same parity makes the midpoint integer, including negative and unbounded integer coordinates. |
| M2 | Closing each contact inside the compact box preserves the midpoint error, supplies compact measurable sets, and preserves coverage. No measurability of the original contact or closedness of the lift is assumed. |
| M3 | Affine output changes and affine input restrictions preserve the represented-set and error assertions without adding integer coordinates. The binary-linear specializations retain finite affine descriptions. |
| S1 | For the square on `[0,1]`, every convex lift with `p` arbitrary integers has error at least `2^(-2p-2)`. The conclusion concerns every full-domain lift. An exact parity pigeonhole argument on a `2^p+1` grid is an equivalent proof; fixed numerical examples alone are insufficient. |
| S2 | An explicit binary linear square graph formulation has exactly `p` binary coordinates, `O(p+1)` continuous variables and rows, contains the graph, and admits only error at most `2^(-2p-2)`. The upper error is attained. Empty depth and the endpoint `x=1` are included. |
| S3 | For every `eps > 0`, both square count minima equal `max(0, ceil((log2(1/eps)-2)/2))`. This includes coarse accuracies and the exact threshold cases. |
| R1 | For symmetric nonsingular `M` of order `d > 0`, `delta >= 0`, and compact `S` with `abs((s-t)^T M (s-t)/2) <= delta`, its volume is at most `2^d (3 sqrt(d) delta)^(d/2) / sqrt(abs(det M))`. The empty, lower-dimensional, and `delta=0` cases are covered. |
| R2 | A symmetric rank-`r` matrix has a nonsingular principal submatrix of order `r`. Fixing complementary coordinates in the original box creates an actual rank-dimensional slice with this Hessian and unchanged integer dimension. |
| R3 | For every nonsingular principal submatrix `H[I,I]` of order `r > 0`, every admissible convex `p`-integer graph lift satisfies `eps >= abs(det H[I,I])^(1/r) (product_i_in_I (u_i-l_i))^(2/r) / (48 sqrt(r)) * 2^(-2p/r)`. The displayed constant is part of the source claim. |
| R4 | Every real symmetric rank-`r` quadratic on the box admits a normalized representation `affine + sum_j c_j y_j^2`, with exactly `r` nonzero terms and affine `y_j` in `[0,1]`. The coordinate widths are positive. The decomposition must be obtained from the Hessian, not supplied as a new headline premise. |
| R5 | For `A=sum_j abs(c_j) > 0` and `L=max(0,ceil(log2(A/(4 eps))/2))`, an actual binary linear graph lift has error at most `eps`, uses `r L` binaries, and `O(n+r(L+1))` rows/variables. Dependent affine square coordinates do not obstruct graph containment. |
| R6 | Both graph minima equal `(r/2) log2(1/eps)+O_(H,B)(1)` as `eps` decreases to zero. Rank zero gives an exact affine graph with zero integers and binaries. Positive rank precludes finite exact graph lifts by R3. |
| I1 | The negative eigenspace of a Hessian with negative inertia `k > 0` contains an actual `k`-dimensional affine box inside the original domain. The restricted quadratic is strongly concave with some positive modulus. Neither the slice nor the curvature bound may be assumed at the original headline. |
| I2 | The same unrestricted-integer parity argument for epigraphs controls the downward chord-midpoint error on that negative slice. It gives the rate `(k/2) log2(1/eps)-O(1)` without any upper output bound. The note also states the explicit strong-curvature bound `eps >= (mu/2)(volume(D)/omega_k)^(2/k) 2^(-2p/k)`. |
| I3 | The dyadic folding interpolant `F_L(t)=t-sum_(j=1..L)4^(-j)G^[j](t)` satisfies `0 <= F_L(t)-t^2 <= 4^(-L)/4`. The relaxed continuous folding inequalities actually project to the stated lower epigraph boundary; this requires the optimization/dominance argument, not only feasibility of the exact folds. |
| I4 | An actual continuous linear square epigraph construction has error `2^(-2L-4)` and linear size in `L+1`, with zero binaries. The manuscript obtains this via depth `L+1` in I3. The note's enhanced depth-`L` construction is a different valid implementation with the same required bound. |
| I5 | The upper half of an explicit depth-`L` binary square construction contains the entire square hypograph and has overerror at most `2^(-2L-2)`. In particular, its output must not retain a lower bound that truncates the hypograph. |
| I6 | Combining positive I4 blocks and negative I5 blocks gives a real binary linear epigraph lift with `k_- L` binaries, error at most `A 2^(-2L-2)`, and `O(n+(k_++k_-)(L+1))` rows/variables. Every exact epigraph point lifts and arbitrarily large outputs remain feasible. |
| I7 | Both epigraph minima are `(k_-/2) log2(1/eps)+O_(H,B)(1)` for `k_->0`. If `k_-=0`, both minima vanish for every positive tolerance, and the exact convex-lift minimum vanishes too. This does not assert an exact finite LP description of a curved convex epigraph. |
| I8 | Apply the proved sign/output transformation to obtain every hypograph conclusion with `k_+`. This includes output direction, the zero-inertia cases, and the compact linear upper formulations. |
| P1 | For `xy` on `[0,1]^2`, the exact best epigraph and hypograph errors with `p` arbitrary integers and convex constraints are both `2^(-2p-2)`. The lower bound follows on the actual slice `y=1-x`, not on an independently assumed univariate problem. |
| P2 | The matching product lift uses `u=(x+y)/2`, `v=(x-y+1)/2`, the identity `xy=u^2-v^2+v-1/4`, an exact convex positive-square epigraph and the binary square hypograph. It contains the full epigraph and attains the stated error at valid original inputs. The affine hypograph transformation preserves accuracy and integer dimension. |
| P3 | The exact product one-sided convex minima equal `max(0,ceil((log2(1/eps)-2)/2))` for `eps>0`. Purely linear lifts approach the same fixed-`p` error with arbitrarily small positive extra slack and no additional binaries. Exact finite-LP attainment at every threshold is not claimed. |
| Z1 | Every finite continuous linear extended formulation of the square epigraph with error `eps>0` and `M` inequalities satisfies `M >= (1/2)log2(1/eps)-1`. The source uses a projected polyhedral lower boundary and at most `2^M` exposed faces. An equivalent proof via attained minimum lifts and their active row patterns is allowed. Equalities and lineality must be allowed. I4 gives matching logarithmic order. |

## Checks of the source arguments

The subsequent contact-volume review identified one required source
qualification: the geometric lemma must state `delta >= 0`. For empty
`S` the pairwise condition is vacuous, and `d=2`, `M=I`, `delta=-1`
would give a negative real volume bound. Nonempty contacts imply
nonnegativity by choosing identical points, and all precision applications
use `delta=4 eps >= 0`. The rank note, manuscript, and frozen claims now
state this qualification. No change to the rank or inertia conclusions
was needed. The existing independent reviews of the
[rank argument](../../../notes/review-quadratic-rank-integer-complexity.md)
and [inertia argument](../../../notes/review-quadratic-inertia-one-sided.md)
agree with the main algebra and scope. Those historical reviews are not
substitutes for reviewing the new Lean statements and proofs.

The determinant constant is consistent. The midpoint error is
`(x-y)^T H (x-y)/8`; hence the contact lemma uses `delta=4 eps`.
The contact cover gives
`V sqrt(abs(det H)) <= 2^p 2^r (12 sqrt(r) eps)^(r/2)`.
Raising to `2/r` contributes the further factor four, producing the
denominator `48 sqrt(r)`. A weaker unspecified constant would establish
the exponent but would leave R3 unverified.

The maximal-simplex enclosure may maximize over all `d+1` contact
vertices, as in the source, or fix any base vertex in the contact and
maximize over the other `d` vertices. In the latter route, nonzero volume
must first supply a nondegenerate simplex for that same base vertex.
Replacing one other vertex then yields the coordinate bound through the
determinant. A proof assuming an enclosing parallelepiped with a
sufficiently small determinant would omit the main geometric obligation.

The principal-minor assertion uses symmetry. Rank alone for a general
nonsymmetric matrix is insufficient. The signed-square normalization
also needs the box interior to ensure positive width for each nonzero
linear coordinate. A choice of normalized square coordinates must be
linked to both actual rank and actual eigenvalue signs.

The original parity contacts can overlap and need not be convex. Neither
disjointness nor convexity should be added as an assumption. Closure
inside the compact domain is the route used in the source to justify
volume and diameter arguments.

The continuous folding proof must show that the relaxed folds cannot
improve the weighted objective beyond the exact folds. A proof of just
the interpolation error does not show the stated LP is accurate. The
manuscript's future-weight estimate is consistent:
`sum_(j>k) 4^(-j) 2^(j-k) < 4^(-k)` for a finite tail. This proves the
required dominance by backward induction.

There is a harmless implementation distinction in the sources: the
note and numerical script use the enhanced depth-`L` positive-square
epigraph with error `2^(-2L-4)`, whereas the manuscript gives a simple
shifted interpolant at depth `L+1` with that same error and linear size.
Both support the inertia theorem. Documentation should identify which
one the formal construction verifies rather than identifying their
projected sets without proof.

The finite-LP row lower bound counts inequalities in the extension, not
facets in the projection. The source uses exposed faces to relate these
counts. An equivalent argument may instead use attained minimum lifts,
their at most `2^M` active row patterns, and an exact finite grid.
Counting only the displayed output facets without relating them to
extension size does not verify Z1. The result does not assert a binary
lower bound for convex square epigraphs.

## Existing Lean material and proof decomposition

The existing `Formal.Model`, `Formal.LowerBounds`, and
`Formal.RationalPolyhedron` files concern the completed exact-count
polynomial example. They provide useful patterns for finite continuous
lifts, integer/binary codes, convexity of explicit affine systems, and
modular integer averaging. Their graph, validity predicate, and concrete
polyhedra are specialized to that example; they do not already prove the
general scalar quadratic claims. In particular, the existing modular
lower bound is modulo three and has finitely many chosen contacts,
rather than the modulo-two compact contact cover needed here.

Mathlib supplies real symmetric spectral decompositions in
`Analysis/Matrix/Spectrum`, including eigenvalues and an orthonormal
eigenvector basis, and real quadratic-form diagonalization in
`LinearAlgebra/QuadraticForm/Real`. Its Lebesgue/Haar measure and
finite-dimensional compactness libraries support the geometric route.
An exact ready-made principal-minor or isodiametric theorem was not
identified during this bounded inventory; that is a search result, not
a claim of nonexistence.

The independently implementable proof blocks are: representation and
parity contacts; maximal-simplex contact volume; spectral decomposition
and box slices; explicit square binary systems; continuous folding LPs;
inertia and product assembly; and finite-LP projection/face counts.
Final assembly must connect these blocks to arbitrary original Hessians,
count minima, and the stated quantitative formulas. Intermediate
conditional interfaces are useful but are not final substitutes for
those connections.

## Verification evidence and exclusions

This review read the listed source statements, their historical reviews,
the scalar numerical checker, and the relevant existing Lean definitions.
No Lean build, numerical execution, project-wide check, or CI inspection
was run as part of this source inventory. The scripts
`code/quadratic_rank/check_simplex.py` and
`code/quadratic_rank/check_one_sided.py` are appropriate targeted
computational corroboration if rerun and recorded by the implementation
work. Their finite examples do not verify the universal theorems.

The optional covariance proof and improved constant in the rank review
are explicitly optional corroboration, not part of the stated scalar
result. Novelty, bibliographic priority, rational spectral algorithms,
optimization runtime, and lower bounds for an arbitrary constrained
optimization instance are not asserted by this package. Non-full-dimensional
domains require a separately justified restriction and cannot use ambient
rank or inertia automatically. These exclusions preserve the source
scope; they do not excuse omitting any scalar obligation in the table.
