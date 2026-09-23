# Source audit: integer precision for common PSD coordinate blocks

Date: 2026-09-05. Focused independent source audit of
[the block PSD candidate](block-psd-quadratic-precision.md).
Mathematical correctness is assigned to separate reviewers.

## Assessment

No matching finite minimum-integer theorem was found in the checked primary
sources. The supported novelty claim is a polynomial rational construction
within `O(sum_b r_b log(r_b+1))` integers of the best arbitrary convex lifted
graph approximation, where `r_b` is the common nonlinear input rank within
each disjoint original coordinate block. The Hessians need not commute
inside a block. Bounded block ranks therefore give an additive `O(r)` bound.

The matrix allocation, determinant inequality, block decomposition idea,
and anisotropic grids are established. Relative to the repository's general
quadratic and input-rank results, this is a structural refinement: local
block dimensions replace the single global logarithmic dimension loss.
It should be presented as such, rather than as a new MAXDET algorithm or
a first use of block structure in MINLP approximation.

## Matrix allocation is an established MAXDET problem

Vandenberghe, Boyd and Wu,
[Determinant maximization with linear matrix inequality constraints](https://web.stanford.edu/~boyd/papers/pdf/maxdet.pdf),
provide the general determinant-maximization framework, its geometric and
statistical applications, and interior-point complexity analysis. The
checked author preprint is dated April 8, 1996; the
[author publication record](https://web.stanford.edu/~boyd/papers/maxdet.html)
identifies the final publication as SIAM Journal on Matrix Analysis and
Applications 19(2), 499--533 (1998). Section 1 defines the general problem;
Section 6 analyzes path-following methods. Section 2 includes ellipsoid,
covariance, and moment applications. None of these claims should be treated
as new here.

The candidate allocation is directly an instance: set
`P=diag(P_1,...,P_B)`, so its objective is `log det P`; encode each
`epsilon_j-sum_b tr(H_jb P_b)>=0` as a scalar linear matrix inequality
and include the block PSD caps. Noncommuting Hessians do not obstruct this
standard reduction. This observation identifies prior methodology; it does
not replace the candidate's explicitly reviewed rational bit-complexity
argument with an unqualified real-arithmetic solver assertion.

## The lower-bound matrix inequality is classical

Russell Merris's primary paper,
[An improvement of the Fischer inequality](https://nvlpubs.nist.gov/nistpubs/jres/75B/jresv75Bn1-2p77_A1b.pdf)
(1971), states in its introduction the classical inequality
`det H<=det H_11 det H_22` for a PSD Hermitian block matrix and credits
Fischer. Iterating gives precisely the candidate's block covariance
determinant bound. No priority for the inequality or its iteration is
claimed. The potentially new use is to retain separate block-size factors
in a parity-support volume bound for arbitrary convex formulations.

## Block structure in MINLP is already explicit

Muts, Nowak and Hendrix,
[The decomposition-based outer approximation algorithm for convex mixed-integer nonlinear programming](https://link.springer.com/article/10.1007/s10898-020-00888-x)
(2020), Section 2, discusses the effect of block size and explains that
copy variables can produce smaller blocks in sparse factorable MINLPs.
It also identifies connected components of the Hessian adjacency graph
as a natural block decomposition preserving convexity. Section 3 uses
low-dimensional block subproblems to construct outer approximations.
The checked paper targets optimization by decomposition and refinement,
not minimization of the integer dimension of uniform graph approximations.

This comparison also marks an essential scope boundary. Arbitrarily
introducing variable copies imposes coupling equations between the new
blocks. The candidate instead starts with disjoint original coordinate
blocks; after common-kernel quotients, its domain remains a product of
zonotopes. The full product volume is used in the lower bound. Therefore
the theorem does not follow for an arbitrary sparse model merely because
a conventional lifting gives small algebraic blocks.

## Interpolation and compact formulation precedents

Cao's
[An interpolation error estimate on anisotropic meshes and optimal metrics for mesh refinement](https://epubs.siam.org/doi/10.1137/060667992)
(2007) designs anisotropic metrics using derivative information and
ellipsoids. Frey and Alauzet's
[Anisotropic mesh adaptation for CFD computations](https://www.ljll.fr/~frey/publications/cmame05-3.pdf)
combines metrics associated with multiple fields. These are relevant
precedents for allocating directions and accommodating several errors.
They do not supply a lower bound against arbitrary convex lifts with
unrestricted integer variables.

The [weighted-quadratic source audit](quadratic-weighted-precision-algorithm-novelty.md)
and [diagonal PSD source audit](diagonal-psd-quadratic-precision-novelty.md)
record the already checked interpolation, rational spectral approximation,
and shared-binary formulation sources. Applying those constructions within
blocks does not establish separate priority for their encoding mechanisms.

## Precise novelty boundary and remaining limits

The distinctive comparison has two matching structural parts. Positivity
turns every output's expected Jensen gap into a trace constraint; Fischer's
inequality bounds support volume using block covariance determinants.
Conversely, a grid adapted to each block controls all its PSD outputs by
trace allocation, without simultaneous diagonalization. Independent
blockwise quotient normalization then charges each rank separately.

The universal comparison is to the minimum over all convex lifts, not
only block-respecting grids. This is stronger than saying that independent
small blocks are easier to approximate. It does not assert that a global
optimum decomposes into separate output problems: trace budgets still couple
the blocks. Nor does polynomial construction imply polynomial optimization
of the resulting MILP.

The focused search covered block PSD quadratic approximation, minimum
binary variables, convex representability, block-separable MINLP outer
approximation, anisotropic multiple-field metrics, and determinant
allocation with trace constraints. No exact match was found. This is a
qualified no-match assessment; the theorem still needs its mathematical
reviews and cannot be declared unknown throughout the literature on the
basis of this bounded search.
