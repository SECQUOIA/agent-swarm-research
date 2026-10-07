# Prior-art audit: quadratic growth and adaptive grids around an optimum set

Date: 2026-10-02. This is a focused, read-only audit of (i) the qualitative
quadratic-growth fact used by the exact rational box-QP corollary and (ii) a
set-valued extension of the corrected-grid dynamic program. It is a scoped
comparison, not a novelty or priority clearance.

## Candidate scope

The current set-valued candidate has product domains for continuous or
large-integer variables `x`, optionally with finite-state variables `z` that
are fully enumerated in the tree DP. There are no coupled constraints
involving `x`. The objective has uniform upper coordinate curvature `L` in
`x` and satisfies projected quadratic growth

`F(x,z) - f* >= g dist(x,S)^2`,

where `S={x : some feasible z has F(x,z)=f*}` is the compact set of
`x`-coordinates occurring in global optima. The distance is Euclidean in the
gridded `x` coordinates and the growth inequality must hold for every
feasible `(x,z)`. Finite-state values have no metric; a closest point in `S`
need not share the current `z`. The proposal does not require derivatives.
It forms each coordinate grid as a union of geometric grids centered at
previously discovered coordinate anchors. The corrected grid objective
subtracts the unary interpolation penalty `L ell_i^2/8` (with unit integer
intervals omitted), so its grid minimum remains a lower bound on `f*` over
the full product domain. If the certified gap is still too large, the next
solve adds the new minimizer's coordinates as anchors.

For the finite-projection case, each failed solve is charged to a
coordinate-value pair `(i,s_i)` with `s_i in pi_i(S)`. With
`h = sqrt(eps)/(2 sqrt(L n))`,
`theta <= min(1/2, sqrt(g/L)/2)`, and
`tau = sqrt(eps)/(theta sqrt(2 L n))`, the current bound is

`T_fin <= sum_i |pi_i(S)| max(0, ceil(log_{sqrt(2)}(s_i/tau)))`.

Thus a set with exponentially many joint optima can still have a small
charge when its coordinate projections are small. For example, `2^n`
combinations of binary coordinatewise double wells have only `2n` projected
coordinate values. For general compact `S`, the note replaces projection
cardinality by finite-resolution covering numbers of the coordinate
projections; its bound uses nets of radius `tau/16` and a logarithmic factor
`ceil_+(log_(6/5)(s_i/(15 tau/16)))`. A polylogarithmic accuracy bound
follows when the projection counts or relevant covering numbers stay
bounded, but not for every positive-dimensional optimum set. The note's
diagonal-optimum example forces coordinate grids of size
`Omega(eps^(-1/2))` and width-one tables of size `Omega(eps^(-1))` for this
specific corrected-grid certificate. This is a certificate limitation, not
an optimization-hardness result.

With `T` failed solves, no finite-state exact-oracle table work is
`O((N + number_of_factors) q0^p (T+1)^(p+1))`, where `p` is the largest
gridded bag size and each per-anchor grid has
`q0 = O(1 + theta^-1 log(1 + theta s/h))` nodes. The full note gives a
bag-specific sum when finite-state products vary by bag. Its rational
extension gives polynomial bit work for rational polynomials of numerically
bounded degree at fixed width and polynomially bounded conditioning and
optimal-projection complexity; it does not cover exact-real function oracles,
unbounded binary-encoded degree, or finite-precision evaluation without a
separate error budget. Budgeted dovetailing removes the need to know `g`,
with logarithmic overhead over a successful admissible run. Even without
quadratic growth, fixed-ratio refinement has a crude finite-termination
packing bound, but the fast complexity charge uses growth. For purely
integer gridded variables, exact tables can stop with an exact value
certificate despite multiple optima. The full-domain correction and
finite-width DP are essential: this is not merely local refinement around a
list of candidate minimizers.

## Uniqueness and quadratic growth for compact quadratic programs

For the exact-box-QP corollary, the qualitative lemma is correct under its
stated assumptions: a quadratic objective on a compact mixed box with a
unique global optimizer has some positive global quadratic-growth constant.
The proof already in [exact-box-qp.md](../geometric-dp/exact-box-qp.md) is a
direct argument from exact quadratic expansion, compactness, and the feasible
tangent cone. It handles integer coordinates by noting that any sequence
converging to the optimizer must eventually have the same integer
assignment. This proof is a good citation boundary: the result is elementary
for this class, but it does not give a useful numerical lower bound on the
growth constant.

The same tangent-ray argument extends from a box to a compact polyhedron for
a continuous quadratic program: a violating sequence has a limiting
feasible tangent direction with zero first-order change and nonpositive
quadratic change; exact quadratic expansion then makes a short feasible ray
optimal, contradicting uniqueness. Compactness matters for the global
statement. Without it, uniqueness need not give global quadratic growth; on
`[0,infinity)`, for example, `f(x)=x` has a unique minimizer at zero but
`f(x)/x^2` tends to zero. For a general smooth objective, uniqueness is also
insufficient: `f(x)=x^4` on a compact interval is a counterexample.

Classical second-order-growth and error-bound theory is the right background,
but the sources examined do not replace the short exact-QP proof above.
Bonnans and Ioffe study quadratic growth and stability for convex `C^2`
programs with a possibly non-singleton solution set. Chen's thesis surveys
global quadratic growth and its relation to second-order sufficient
conditions, including constraint-qualification qualifications. Fadili,
Nghia, and Tran state the standard convex piecewise-linear-quadratic result
that uniqueness and strong minimization are equivalent, citing
Rockafellar--Wets; a convex QP plus a polyhedral indicator is in this PLQ
class. These are useful for terminology and the convex boundary, not a blanket
claim that uniqueness of an arbitrary smooth or nonconvex constrained
minimizer implies quadratic growth.

Sources examined:

- J. F. Bonnans and A. D. Ioffe, [“Quadratic Growth and Stability in Convex
  Programming Problems with Multiple Solutions”](https://doi.org/10.68381/jca02003),
  *Journal of Convex Analysis* 2 (1995), 41–57. The publisher's open abstract
  states the setting as convex programs with `C^2` functions and a convex
  solution set; it supplies a second-order condition characterizing quadratic
  growth and stability.
- Zhangyou Chen, [*On the Equivalence of Global Quadratic Growth Condition
  and Second-Order Sufficient Condition*](https://theses.lib.polyu.edu.hk/handle/200/5540),
  M.Phil. thesis, Hong Kong Polytechnic University (2009). The introduction
  discusses growth relative to a solution set and its relation to standard
  second-order sufficient conditions under constraint qualifications. Its
  quadratic examples are narrower than a general nonconvex QP theorem.
- M. Fadili, T. T. A. Nghia, and T. T. Tran, [“Sharp, Strong and Unique
  Minimizers for Low Complexity Robust Recovery”](https://doi.org/10.1093/imaiai/iaad005),
  *Information and Inference* 12(3) (2023), 1461–1513. Its PLQ discussion
  cites the convex piecewise-linear-quadratic uniqueness/strong-minimizer
  equivalence; this applies to convex QP with polyhedral domain, not an
  indefinite QP.

## Adaptive optimization with multiple minima

The closest focused comparator found is Matthias Horn,
[“Optimal Algorithms for Global Optimization in Case of Unknown Lipschitz
Constant”](https://d-nb.info/987595660/34), Dagstuhl Seminar Proceedings
04401 (2005). Horn treats real-valued functions on `[0,1]^d` with a known
Lipschitz bound for one algorithm (and an unknown-Lipschitz variant) plus a
global near-optimal-sublevel-volume condition
`lambda^d({x : f(x) <= f* + delta}) <= D delta^(d/2)` for small `delta`.
The paper explicitly allows many global minimizers and uses adaptive
geometric mesh refinement from retained near-best points. Its optimal
worst-case error rate is equivalent to a query cost with a polynomial
`eps^(-d/2)` dependence, up to parameters and dimension-dependent constants.
For finitely many nondegenerate minima, the paper notes that its volume
condition follows locally from Taylor expansion.

Horn therefore rules out any broad claim that adaptive geometric refinement
around several minimizers, using only objective values, is itself new. The
comparison differs in the analyzed parameter and algorithmic structure:
Horn's count depends on ambient dimension and the near-optimal-volume
constant; it does not exploit factor-graph width or the sum of coordinate
projection cardinalities. The candidate retains a full product-domain grid,
uses a summed curvature correction as a certified global lower bound, and
charges failed solves to projected optimum values under quadratic growth.
That is the specific combination this audit did not find in Horn.

The targeted checks also covered the terms “interval dynamic programming,”
“adaptive discretization quadratic growth global optimization,” “discrete
differential dynamic programming global convergence,” and “sparse global
optimization log accuracy.” The first surfaced tree-structured interval DP
comparators already discussed in
[geometric-grid-prior.md](geometric-grid-prior.md). The DDDP source uses
trajectory-centered corridors and warns that corridor choices can converge
to a local extremum; it does not provide the candidate's full-domain
corrected lower bound or QG-conditioned projected-value charge. The other
targeted searches did not identify a direct formulation of the same
projection-cardinality bound. This negative result is limited to these
queries and sources; it is not evidence of novelty by itself. A parallel
audit covers near-optimality-dimension and bandit partitioning results.

## Comparison boundary

The supportable distinction is narrower than “adaptive multi-center
optimization is new.” Prior work already supplies QG/error-bound theory,
multiple-minimum Lipschitz optimization, geometric refinement, and tree
dynamic programming as separate ingredients. The candidate's possible
contribution is the combination of (a) coordinatewise unions of geometric
meshes around discovered anchors, (b) a nodewise correction that is a valid
lower bound over the entire mixed product domain, (c) a set-valued QG
contraction argument, and (d) a failed-solve bound controlled by
`sum_i |pi_i(S)|` rather than the number of joint optima, with exact
finite-width DP table work. No source examined here establishes that complete
combination. This remains a qualified prior-art finding, not a novelty
claim.

## Ingest handoff

These works are not additional literature claims in the project's note yet.
They were routed to the sole literature-ingest agent for its decision on KB
coverage and full-text packaging. No literature KB files were changed during
this audit.
