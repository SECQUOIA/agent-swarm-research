# Investigation of low-rank costs for rank-one flow blocks

Date: 2026-09-04. Candidate results are in `results/rank-one-low-rank-costs.md`; an independent
proof review has been requested. Novelty is not established.

## Outcome

Low ordinary rank and low rank after subtracting additive source/terminal costs give polynomial
exact optimization when the rank is fixed. Thus NP-hardness at rank one or two cannot hold for
this precise bounded-margin model unless P=NP. The resulting dependence on rank is XP, not FPT.

The constructive argument projects both margin boxes into low-dimensional zonotopes while
retaining total flow and objective coordinates. A fixed-total optimum can be chosen at vertices
of the two slices. Slice vertices occur on edges of the unsliced zonotopes, so polynomially many
vertex-pair segments capture all needed candidates. Pairing row and column segments reduces
the objective to `alpha*S+beta+gamma/S`, preserving exact quadratic-field output instead of
requiring general quantifier elimination.

For rank-one costs without an added additive term, four continuous-knapsack envelope products
suffice. All envelopes have linearly many breakpoints, yielding a near-linear arithmetic
algorithm when factors are supplied. The result includes arbitrary cost signs and zero lower
bounds. Additive costs plus one rank-one term are covered by the general theorem, but not by
the simpler four-extrema formula: the additive row cost can trade off against its scalar factor.

## Relation to the existing repository

`results/rank-one-row-column-hardness.md` gives strong hardness for arbitrary costs and FPT
tractability in the smaller matrix dimension. The new parameter permits both dimensions to
increase. Its proof reuses the elementary one-total quadratic-fractional minimization already
present there. `results/common-factor-fixed-linking-optimization.md` studies a different common
factor model with a fixed number of linking rows; its notes already identify Punnen's method.
The present theorem is not a new general low-rank bilinear optimization technique.

## Primary literature found

1. Punnen, Sripratak and Karapetyan, *The bipartite unconstrained 0–1 quadratic programming
   problem: polynomially solvable cases*, 2015, [open manuscript](https://repository.essex.ac.uk/22056/1/1212.3736v3.pdf),
   [arXiv](https://arxiv.org/abs/1212.3736). The continuous Cartesian-box version is equivalent
   to its binary counterpart. The paper proves fixed-rank polynomial tractability and an
   `O(n log n)` rank-one algorithm. This is close prior art for both theorem headlines; the
   common-total equality and variable denominator are the specific differences.
2. Hladík, Černý and Rada, *A new polynomially solvable class of quadratic optimization problems
   with box constraints*, Optimization Letters 15(6):2331–2341, 2021,
   [author page](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html).
   Fixed-rank indefinite quadratic objectives with arbitrary linear terms over a continuous
   box are polynomially solvable through low-dimensional zonotope face enumeration. This
   prevents claiming the projection or zonotope strategy as new. Their published scope does
   not directly state the present equal-total fractional model.
3. [Girard and Le Guernic, zonotope/hyperplane intersection](https://www.cecs.uci.edu/~papers/cpsweek08/papers/hscc08/session1/s1-2.pdf)
   treats zonotope slices in reachability analysis and explicitly connects the two-dimensional
   slice problem with continuous knapsack. This supports treating the slicing/greedy ingredients
   as standard geometry rather than a new algorithmic primitive.

Search terms included `fixed rank bilinear programming polynomial time`, `fixed rank bilinear
fractional`, `quadratic fractional fixed rank box`, `zonotope fractional optimization quadratic`,
`rank-one row sum cost polynomial`, and `Punnen zonotope bilinear`. No exact theorem for this
row-and-column rank-one flow set was located. The low-rank fractional optimization literature
is not exhaustively covered, so the safe status is a verified-if-reviewed structural extension
with provisional application-level novelty.

## Scope safeguards

- The cost parameter differs from `rank(W)`, which is always at most one.
- The canonical double-difference matrix computes the smallest residual rank after arbitrary
  additive costs; this is a linear-algebra fact, not an algorithm for approximate rank reduction.
- All bounds are finite and rational. Degenerate projected zonotopes and zero-only feasibility
  are included in the proof.
- The segment list may contain nonedges. This creates additional feasible candidates, never
  invalid ones, and avoids a generic-position or edge-enumeration assumption.
- Horizontal segments are omitted; original vertices handle their possible slice vertices.
- Near-linear complexity counts arithmetic operations with supplied cost factors. It is not a
  near-linear binary running-time claim and does not evade reading a dense input matrix.
- Approximate cost factorization gives a simple additive objective guarantee scaled by the
  maximum total flow. It does not imply an FPTAS for unrestricted cost matrices.

## Specific quality-constraint application

For additive operating costs, dualizing `K` terminal quality rows per terminal with supplied
rational multipliers produces a cost of the form `Q Lambdaᵀ` plus additive terms. Hence fixed
quality count gives an exact polynomial per-pool Lagrangian oracle, provided the remaining block
constraints are only row/column bounds and rank one. This algebraic corollary was independently
checked by `review_extension`. It makes the cost parameter relevant to standard quality data
without asserting zero duality gap or solvability of the full coupled pooling problem.
