# Prior-art audit: smoothed sparse optimization on products of simplexes

Date: 2026-10-02. This focused audit compares the candidate in
[`simplex-block-smoothed-extension.md`](../new-direction/simplex-block-smoothed-extension.md)
with established genericity, rounding, and smoothed-count results. The
candidate's mathematical interfaces and equality-simplex corollary have
passed independent review. This note records prior-art boundaries, not a
publication-priority claim.

## Candidate and remaining distinction

The candidate replaces independent box coordinates by disjoint unit-simplex
blocks, while retaining fixed-degree sparse polynomial factors, a supplied
tree decomposition containing whole blocks, and independent ambient linear
noise. Its cell at mesh `h` is a simplex intersected with a dyadic cube. Since
the rescaled budget has an integer right-hand side, each such cell is the
convex hull of its feasible cube corners. A convex combination of those
corners gives mean-preserving rounding. A block Hessian upper bound controls
the rounding error.

The closest algorithmic comparison is the project's
[semiconcave grid-cell result](smoothed-semiconcave-cells-prior.md) and the
[sparse polynomial box audit](sparse-smoothed-polynomial-prior.md). Those
already contain conditional semiconcavity, independent linear perturbations,
near-optimal bag-state counting, sparse tree-decomposition DP, finite-law
handling, and exact closure. The simplex candidate adapts that machinery to
feasible faces: for each relative face of dimension `r`, it counts at most
`h^{-r}` grid nodes and imposes `r` independent tangent comparisons on the
noise. On a saturated face, conditioning on one anchor coefficient leaves
independent differences for the other tangent coordinates. The probability
factor cancels the face's mesh-dependent node count. This is a precise
geometric extension of the box count, not a new tree-DP or semiconcavity
principle.

The simplexes also change exact closure. The proposed derivative and
derivative-difference tests identify zero coordinates and a tight budget;
strict-complementarity margins then make those tests succeed on a sufficiently
fine retained hull. These are standard KKT face-identification ideas. The
potentially distinctive algorithmic claim is their composition with the
face-stratified expected bag-cell count and the candidate's same-draw exact
output contract. The candidate's completed review covers its closure and
relative-polytope evaluation interfaces; these are part of the checked
algorithm, not new KKT or convex-oracle principles.

## Qualitative genericity already covers simplex blocks

Lee and Phạm's 2017 Theorem A applies to a fixed polynomial objective plus a
linear tilt on a regular closed semialgebraic set. It gives generic
uniqueness, strong second-order sufficiency, local quadratic growth, and a
global sharp-minimum inequality. On a compact set, bounded objective gap
turns that sharp-minimum inequality into some global quadratic-growth
constant. Their theorem also gives strict complementarity and a locally
constant active manifold. It is direct qualitative prior art for the
continuous part of this candidate; it does not give a quantitative tail,
finite-grid guarantee, or an expected sparse algorithm.
[[lee2017-generic-properties-for-semialgebraic-programs]] Theorem A, pp. 3–4;
Definition 3.1, p. 9

The product of unit simplexes meets their regularity condition. In one block,
the active coordinate normals are distinct coordinate vectors. If the budget
is tight, at least one coordinate is positive, so the all-ones budget normal
is independent of the active zero-coordinate normals. Blocks use disjoint
coordinates, so their active gradients remain independent in the product.
Bounded integer labels can be encoded by one equality per integer coordinate,
`prod_{k=l}^{u}(z-k)=0`; its derivative is nonzero at each allowed label.
This produces a compact regular semialgebraic set for the qualitative
theorem. That encoding has degree proportional to the integer-domain size,
so it is not a complexity reduction and supplies no bound for the candidate's
finite noise grid.

The project's [quantitative linear-tilt growth tail](../new-direction/proximal-growth-tail.md)
is stronger on the modulus question: its compact-domain result applies to
arbitrary continuous objectives and gives an explicit probability bound.
The project's [finite-grid tail note](../new-direction/polynomial-finite-noise-tails.md)
proves the rational finite-law transfer for mixed boxes. The candidate proves
the simplex-face version; it should not be described as already covered by
the box statement. Neither route makes qualitative growth the contribution.
The simplex extension's algorithmic comparison should focus on feasible
sparse rounding, the facewise count, and exact face closure.

## Nearby rounding and smoothed-count results

The clipped-cell rounding claim needs no specialized dependent-rounding
theorem: every point of the cell is a convex combination of its feasible
vertices, so those vertices define a mean-preserving distribution. The
candidate does not need to sample this distribution; it uses it to prove a
lower-bound error and to preserve a specified cell. The optional phrase
“pairwise dependent rounding” should therefore not be read as an algorithmic
ingredient or a claim that a particular rounding procedure applies.

Röglin and Rösner's Theorem 2 bounds expected Pareto-optimal solutions on a
finite set of real-valued points under independent noisy linear coefficients
and a coordinate-separation condition. This is a close probabilistic
comparison, but it counts exact Pareto solutions on a fixed finite set, not
near-optimal grid nodes on a continuum. Its separation parameter also
deteriorates under mesh refinement. The candidate instead obtains a
mesh-uniform bound by matching tangent dimension to the original simplex
face dimension.
[[roglin2017-the-smoothed-number-of-pareto]] Theorem 2

Kelner and Nikolova's Theorem 2.9 gives expected polynomial-time smoothed
minimization for a fixed constant-rank quasi-concave objective over an
integral polytope, after randomly rotating the objective's low-rank
subspace. Their bound counts vertices in projected shadows. This is strong
prior art for smoothed global optimization over polytopes, but the
perturbation and geometric count differ from independent ambient linear
noise, semiconcave bag min-marginals, and facewise near-optimal grid cells.
[[kelner2007-on-the-hardness-and-smoothed]] Theorem 2.9

Lee–Phạm's genericity result and these finite-set/polytope smoothed counts
do not subsume the proposed cell-count theorem as stated. Conversely, the
focused comparisons here do not establish that no equivalent result exists
under other terminology or in a specialized optimization literature.

## Assessment boundary

The elementary ingredients—polytope convex combinations, simplex KKT
conditions, strict complementarity, and dynamic programming on a supplied
tree decomposition—are established. The existing box result already
contains the general sparse expected-cell method. The reviewed candidate
extends that method to products of simplex blocks by a face-stratified count
and exact face closure. It should be described as a constrained extension
of the box method, not as a general method for arbitrary sparse linear
constraints or as a new rounding principle.

Sources checked were the local full texts of Lee–Phạm (2017),
Röglin–Rösner (2017), and Kelner–Nikolova (2007). A narrow discovery query
did not add a source to this comparison; no new package was needed or ingested.
No project-wide check or CI inspection was performed.
