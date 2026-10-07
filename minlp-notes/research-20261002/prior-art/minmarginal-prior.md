# Prior-art audit: min-marginal pruning with conditioned regridding

Date: 2026-10-02. This is a focused, read-only prior-art audit for the
proposed [pruned-coordinate-grid algorithm](../new-direction/pruned-coordinate-grid.md).
The current theorem draft reports mathematical and bit-complexity reviews
finding no substantive gap. A targeted exact-rational check reports 12 mixed
QP pruning stages and 766 conditional-bound samples passed. The algorithmic
bounds below should be read against that draft, not as an independent proof
review. This audit is not a priority determination and does not maintain the
literature knowledge base.

## Finding

The ingredients have clear precedents. Exact min-marginals are standard
conditional optimum values in discrete graphical models and can be computed
by forward/backward or junction-tree message passing. Removing a value or region that cannot
beat a known incumbent is standard cost-based domain filtering and
optimization-based reduction. Adaptive-resolution dynamic programming on
treewidth-structured interaction graphs also predates this work, as does using
min-marginal energies to guide local refinement of discretized continuous
labels.

The focused search did not locate a source combining these ingredients with
the proposed guarantee: exact min-marginals of a corrected geometric-grid
objective prune original coordinate intervals; a global quadratic-growth
promise bounds the retained coordinate hulls after each recentering step; and
the resulting grid size is independent of the requested accuracy stage. In
the current draft, this is used to replace an XP dependence on bag size by an
FPT bit/table bound for rational mixed-integer box QPs, without a variable
occurrence parameter. At a suitable trial value, the draft bounds the
coordinate grid size by `O(sqrt(kappa) log(n+2))`; the raw min-marginal table
count still depends on `n` and `p`. The potential contribution is this conditioned
complexity analysis and certificate chain, not min-marginal computation,
domain filtering, geometric grids, or finite-state tree-decomposition DP by
themselves. This is a qualified search result, not evidence of novelty.

The current proposed assumptions are a supplied tree decomposition with
maximum bag size `p`, a rational mixed-integer product box, a unique global
optimizer, global quadratic growth with constant `g` on that mixed domain,
and a known upper coordinate-curvature bound `L` (largest positive diagonal
Hessian entry). The conditioning parameter is `kappa=max(1,L/g)`. At a
refinement stage, the algorithm minimizes the corrected-grid objective by
exact min-sum DP, computes every coordinate min-marginal, deletes an original
coordinate interval when both endpoint min-marginals exceed the incumbent,
keeps the hull of the retained intervals, and builds the next geometric grid
around the corrected-grid minimizer. The draft claims the retained hull lies
within `O(sqrt(n*kappa) h)` of the optimizer at mesh scale `h`, so the next
grid has `O(sqrt(kappa) log(n+2))` points per coordinate, independent of
the number of accuracy refinements. It claims table work fixed-parameter in
`(p,kappa)` and polynomial in input length and accuracy bits, with exact
rational recovery for QPs. The current theorem and proof review should control
the final statement of these bounds.

## Closest prior methods

| Work | What it establishes | Relation and limit |
|---|---|---|
| Pushmeet Kohli and Philip H. S. Torr, [“Measuring Uncertainty in Graph Cut Solutions: Efficiently Computing Min-marginal Energies Using Dynamic Graph Cuts”](https://www.robots.ox.ac.uk/~phst/Papers/ECCV2006/MinMarginals.pdf), ECCV 2006, DOI [10.1007/11744023_45](https://doi.org/10.1007/11744023_45) | Defines min-marginal energies by fixing a variable label and minimizing the energy over all remaining variables. For graph-cut-solvable binary MRFs it computes these conditional minima for all node labels using dynamic graph cuts; the paper notes exact tree min-marginals from belief propagation. | A primary source for the exact conditional-energy meaning of min-marginals and their efficient computation in special discrete models. It does not shrink a continuous search domain, regrid a box, or establish a complexity guarantee from quadratic growth. Full PDF text was inspected. |
| Andrew Leaver-Fay, Brian Kuhlman, and Jack Snoeyink, [“An Adaptive Dynamic Programming Algorithm for the Side Chain Placement Problem”](https://psb.stanford.edu/psb-online/proceedings/psb05/leaver-fay.pdf), Pacific Symposium on Biocomputing 10:16–27 (2005) | Gives treewidth-based DP for pairwise state-assignment energies, then an adaptive two-resolution version that examines fine states for “stiff” interactions and coarse states otherwise. Theorem 2.2 bounds returned energy error by `2 epsilon |E_2|`. | A direct adaptive-DP precedent. Its refinement is driven by local interaction variation in a discrete protein-design model; the theorem controls approximation error linearly in the number of pairwise interactions. It does not use exact per-coordinate min-marginals to contract an original continuous box, nor a global QG promise for an FPT/log-accuracy rate. Full primary PDF inspected. |
| Sarah Parisot, William Wells III, Stéphane Chemouny, Hugues Duffau, and Nikos Paragios, [“Concurrent Tumor Segmentation and Registration with Uncertainty-based Sparse Non-uniform Graphs”](https://doi.org/10.1016/j.media.2014.02.006), Medical Image Analysis 18(4):647–659 (2014) | In a discrete MRF for joint image segmentation and registration, defines min-marginals by fixing a control-point label and minimizing over all other labels (Eq. 21). It uses min-marginal energy variation to estimate displacement uncertainty, resample the displacement set, and refine a sparse spatial grid in a coarse-to-fine scheme (§§3.1–3.2, author PDF pp. 5–7). | The closest direct precedent for min-marginal-guided adaptive label and grid resolution. It is an application-specific, empirically evaluated heuristic: uncertainty selects local resolutions, without a certified interval lower bound, global QG contraction, or width/bit-complexity theorem. The author-hosted full PDF was inspected. |
| Pietro Belotti et al., [“Branching and bounds tightening techniques for non-convex MINLP”](https://doi.org/10.1080/10556780903087124), Optimization Methods & Software 24 (2009), existing KB package `belotti2009-branching-and-bounds-tightening-techniques` | Reviews and evaluates feasibility-, optimality-, and aggressive bounds-tightening inside spatial branch-and-bound for nonconvex MINLP. OBBT solves auxiliary optimization problems to tighten variable bounds, while incumbent-based pruning removes regions that cannot improve the incumbent. | Establishes optimization-based bound tightening as standard global-optimization practice. The work uses relaxation-based variable extrema and solver branching, not exact grid min-marginals or a QG-driven, stage-uniform grid-count bound. Its full text is already read in the project KB. |
| Alberto Del Pia and Aida Khajavirad, [“Treewidth and the complexity of box-constrained quadratic programs”](https://arxiv.org/abs/2609.35595v1), arXiv:2609.35595v1 (2026), existing KB package `pia2026-treewidth-and-the-complexity-of` | Gives an exact strongly polynomial value-function DP for rational continuous box QPs on forests and strong NP-hardness at interaction treewidth two for unrestricted instances. | Important boundary evidence: treewidth alone does not make general nonconvex box QP tractable. A separate check found that their width-two reduction admits unique-optimum instances with exponentially large `L/g`; this family therefore does not refute an algorithm parameterized by that ratio. See [the hardness compatibility check](../reviews/pruned-grid-hardness-sanity.md). |

## Ingredient and claim boundaries

Exact finite-state min-sum DP and its forward/backward or junction-tree
extension are established; Leaver-Fay et al. give a primary treewidth-DP
example, and Kohli–Torr explicitly discuss exact tree min-marginals. Given a finite grid, computing one minimum value
for every grid point of a selected coordinate is just exact conditional MAP
inference. The standard safe filter is also simple: if the best objective
value subject to a value/region restriction exceeds a feasible incumbent,
that restriction cannot contain a global optimizer. OBBT, cost-based filtering,
and dead-end elimination are established versions of this basic idea under
different representations and relaxations.

Adaptive state resolution in treewidth DP is established by Leaver-Fay et al.;
min-marginal-guided adaptation of discrete label sets and spatial grid
resolution for continuous imaging is established by Parisot et al. Neither
source proves that endpoint
min-marginals of a corrected sampled objective lower-bound every point in the
corresponding original interval. Neither gives a QG-based bound on the entire
coordinate hull retained after pruning, and neither gives an accuracy-stage
grid count independent of `log(1/epsilon)`.

The candidate should therefore make its possible contribution conditional
on the current proof passing review: the coupling of (i) a valid interval
certificate from endpoint conditional minima of the corrected grid, (ii)
global QG contraction of all intervals that survive that certificate, and
(iii) recentering/regridding whose bag table size depends on `(p,kappa)` but
not on the accuracy stage. The per-stage min-marginal pass remains a
classical DP operation. The FPT conversion also needs to be stated exactly:
the proposed bag table factor has a `(log(n+2))^p` term, absorbed into a
parameter-only factor times a fixed
polynomial in `n`; it does not mean the raw table count is independent of
`n` or of `p`.

This result must remain distinct from the preceding
[shared-grid certificate audit](geometric-grid-prior.md), which compares
recentered global lower bounds and polylogarithmic accuracy dependence but
retains a variable-occurrence parameter and uses a different certificate.
The current draft removes occurrence by using global coordinate min-marginals
and interval hulls, so its key additional question is whether that exact
filtering and packing argument is valid for every bag factorization and all
mixed integer/continuous boundary cases.

## Focused search and limits

Queries examined “min-marginal” with domain filtering, pruning, adaptive
discretization, graph cuts, and treewidth; “quadratic growth” or “error
bound” with treewidth DP and global optimization; and optimization-based
bounds tightening with min-marginals. They found the separate precedents
above, but no directly equivalent QG-conditioned min-marginal regridding
algorithm. Searches are terminology-dependent and do not establish priority.
The cited width-two hardness compatibility check found no contradiction
under the candidate's conditioning promise. It does not validate the
algorithm or rule out another hardness construction that preserves bounded
`L/g`; no novelty conclusion should be drawn from this search.

The [adaptive-treewidth-QP audit](regridded-qp-prior.md) remains the stronger
comparison for rational QP bit complexity and treewidth-two hardness. The
[geometric-grid audit](geometric-grid-prior.md) remains the broad comparison
for continuous factor-graph discretization, interval DP, and certified
polylogarithmic accuracy. This note covers only the new min-marginal pruning
and contraction mechanism.

## Source retrieval handoff

The following missing primary sources were routed to the sole literature
ingest agent because they anchor the adaptive/min-marginal comparison:

1. Leaver-Fay, Kuhlman, and Snoeyink (2005), “An Adaptive Dynamic Programming
   Algorithm for the Side Chain Placement Problem,”
   https://psb.stanford.edu/psb-online/proceedings/psb05/leaver-fay.pdf —
   public primary PDF inspected here; ingest for a durable project citation
   to adaptive treewidth DP and its explicit approximation theorem.
2. Kohli and Torr (2006), “Measuring Uncertainty in Graph Cut Solutions,”
   https://www.robots.ox.ac.uk/~phst/Papers/ECCV2006/MinMarginals.pdf — public
   primary PDF inspected here; ingest for exact conditional-energy
   min-marginals and efficient computation in graph-cut models.
3. Parisot, Wells, Chemouny, Duffau, and Paragios (2014), “Concurrent Tumor
   Segmentation and Registration with Uncertainty-based Sparse Non-uniform
   Graphs,” DOI 10.1016/j.media.2014.02.006,
   https://parisots.github.io/PDFs/ParisotMedia14.pdf — public author-hosted
   primary PDF inspected; ingest for a durable source note on min-marginal
   uncertainty driving adaptive displacement labels and grid refinement.

The Del Pia–Khajavirad package's full PDF was read directly for the cited
hardness boundary. The separate compatibility check reads its reduction and
derives the stated `L/g` bound; that calculation is not a prior-art or
novelty result.

The Del Pia–Khajavirad source is already present and read in the KB at
`literature/papers/pia2026-treewidth-and-the-complexity-of/`; no new ingest is
needed. Belotti et al. (2009) is also already present and read. I did not
perform KB edits, broad project checks, or external changes.
