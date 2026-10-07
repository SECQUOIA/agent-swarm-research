# Prior-art audit: mixed-shell certificates for a proposed box optimum

Date: 2026-10-02. This is a focused comparison of the candidate in
[`mixed-shell-certificate.md`](../new-direction/mixed-shell-certificate.md).
The candidate's separate [independent review](../new-direction/mixed-shell-independent-review.md)
and [grid/bit review](../new-direction/mixed-shell-grid-bit-review.md) are
complete. The literature comparisons below do not establish priority.

## Candidate result being compared

The candidate takes a rational point in a bounded product box whose
coordinates are continuous or restricted to rational lattices, a quadratic
objective, and a supplied tree decomposition of the quadratic interaction
graph. It first checks feasibility and the first-order signs on continuous
coordinates. For each physical dyadic shell away from the point, it builds a
finite feasible grid and minimizes a curvature-corrected quadratic over that
grid using one exact tree-decomposition DP. The proposed proof uses
independent mean-preserving endpoint rounding to convert that finite minimum
into a lower bound over every point in the shell. The continuous first-order
signs then extend the bottom-shell inequality along rays with lattice
coordinates fixed.

If all checks pass, the finite rational data certify that the point is the
unique global minimizer and give a rational global quadratic-growth margin.
The search over dyadic grid sizes terminates when the point has positive
global growth, without taking that growth constant as input. For curvature
scale `L`, growth `g`, and bag size `p`, the shell-DP work is
`f(p, L/g) poly(I)`, where `I` includes the rational instance, proposed
point, and decomposition. There are `O(I)` physical shells; this is an
encoded-range factor, not an extra `p`-power. The returned margin need not be
within a constant factor of `g` when `g` is much larger than `L`. These are
claims of the candidate draft, not independently re-proved here.

The reviewed draft also handles the endpoint case in which every diagonal
quadratic coefficient is nonpositive: coordinatewise concavity reduces
uniqueness checking to the two endpoints per coordinate, followed by an
ordinary tree DP and endpoint-rounding growth bound. This is the classical
endpoint-DP case, not the mixed-shell contribution. A companion theorem in
[`geometric-product-face-certificate.md`](../new-direction/geometric-product-face-certificate.md)
extends the physical-shell method to a supplied coordinate fiber as the
entire optimal set, with a growth bound in distance to that fiber. It checks
the objective identity on the proposed fiber and permits mixed continuous
and lattice coordinates on both active and free sides. That result verifies
a supplied product face; it does not identify an arbitrary union, a tilted
flat set, or a disconnected optimal set.

## Closest primary sources

| Source | Established result and relevance | Boundary relative to the candidate |
|---|---|---|
| Burer and Vandenbussche, [“A finite branch-and-bound algorithm for nonconvex quadratic programming via semidefinite relaxations”](https://doi.org/10.1007/s10107-006-0080-6), *Mathematical Programming* 113 (2008), Theorem 3.3, pp. 10–12 | Proves correctness and finite termination of a KKT-branching algorithm using SDP relaxations for bounded nonconvex QP. The paper gives both an exact-arithmetic argument and a bit-model discussion; box-QP experiments are reported on pp. 17–19. | This is the strongest general finite-search comparison found. Its proof is a branch-and-bound computation, with no polynomial bound in treewidth and curvature divided by growth. It establishes algorithmic finite certification, not a compact width-parameterized certificate of the proposed form. |
| Dvijotham et al., [“Graphical Models for Optimal Power Flow”](https://doi.org/10.1007/s10601-016-9253-y), *Constraints* 22 (2017), Theorem 2, §4.3 | Uses interval-valued messages and adaptive refinement in a tree DP for a mixed-integer nonconvex OPF model. Under bounded-data assumptions and maximum degree three, its guarantee bounds constraint violation by `ζ ε`, returns a superoptimal cost, and uses at most `n ζ′ ε⁻⁵` calls to its bound-propagation routine. | This is the closest interval-grid lower-bound DP for a mixed nonconvex model. The guarantee is OPF-specific and approximate; it permits constraint violation and has a polynomial `1/ε` dependence. It does not certify a feasible candidate's exact global optimality or use physical shells and a global growth margin. |
| Bhathena, Fattahi, Gómez, and Küçükyavuz, [“A Parametric Approach for Solving Convex Quadratic Optimization with Indicators Over Trees”](https://doi.org/10.1007/s10107-025-02222-3), *Mathematical Programming* (2025), Theorem 2 | Gives an exact `O(n²)` time-and-memory DP for positive-definite QPs with one binary support indicator per continuous variable when the Hessian support graph is a tree. | Strong exact mixed optimization on trees, but the model is convex with indicator constraints and the graph is a tree. It does not treat arbitrary mixed product lattices, indefinite quadratic objectives, bounded bag size beyond trees, or a separately checkable lower certificate based on the candidate's growth ratio. |
| Bhathena et al., [“Solving Convex Quadratic Optimization with Indicators Over Structured Graphs”](https://arxiv.org/abs/2603.02103), arXiv:2603.02103 (2026), Theorem 1 and Corollary 1 | Extends exact parametric DP to positive-definite indicator QPs on bounded-treewidth graphs. The efficient bound also depends on polynomial volume growth, conditioning, and a `(k, η)`-margin controlling near-tied indicator assignments. | This is the closest conditioning/margin-dependent exact treewidth-MIQP solver. Its margin is a discrete near-tie condition for local support patterns, not global quadratic growth of the full mixed-domain objective. It does not use a proposed-point certificate or a geometric shell correction. |
| Eiben, Ganian, Knop, and Ordyniak, [“Solving Integer Quadratic Programming via Explicit and Structural Restrictions”](https://doi.org/10.1609/aaai.v33i01.33011477), AAAI 2019, Corollary 11 and Theorem 13 | Gives exact structural algorithms for IQP under bounded-domain/treewidth conditions, and under hybrid domain/coefficient restrictions with a suitable graph parameter. The paper also proves that treewidth or a bounded domain alone is insufficient in its broader IQP setting. | This supplies the standard finite-domain tree-decomposition baseline. A finite grid of `K` states per coordinate gives the usual exponential-in-`p` DP state count, but the candidate's grid is only useful for the original continuum because its rounding correction proves a valid lower bound between grid points. The candidate's state count depends on `L/g` rather than the full integer-domain cardinality. |
| Del Pia and Khajavirad, [“Treewidth and the complexity of box-constrained quadratic programs”](https://arxiv.org/abs/2609.35595v1), arXiv:2609.35595v1 (2026), Theorems 1 and 3 | Gives an exact strongly polynomial `O(n²)` DP for continuous box-QP on forests and proves strong NP-hardness already at interaction treewidth two for unrestricted box-QP, even with bounded integral coefficients. The authors state that their results extend to mixed-binary boxes. | This is the sharpest structural boundary for nonconvex quadratic objectives. The candidate's positive growth-to-curvature condition is a substantive additional promise that may permit an FPT bound beyond forests; the hardness theorem cautions against implying that treewidth alone suffices. It does not establish the mixed-lattice shell certificate. |
| Del Pia, Dey, and Molinaro, [“Mixed-integer quadratic programming is in NP”](https://doi.org/10.1007/s10107-016-1036-0), *Mathematical Programming* 162 (2016), Theorem 1 and Corollary 2 | Proves polynomial-bit rational feasible witnesses for the single-quadratic-inequality decision MIQP formulation. | This supports short primal witnesses, but not a short proof that no better feasible point exists. The candidate instead supplies a verifiable lower-bound argument over the full domain. |
| Bienstock and Muñoz, [“LP Formulations for Polynomial Optimization Problems”](https://doi.org/10.1137/15M1054079), *SIAM Journal on Optimization* 28 (2018), Theorem 4/15 | Gives certified treewidth-based LP approximations for bounded mixed-integer polynomial optimization, with formulation size having a power dependence on `1/ε` and scaled feasibility/optimality tolerances. The paper also gives limits on replacing that dependence by polylogarithmic accuracy for its broad model. | Relevant general certificate/approximation precedent. Its model and guarantee differ; the candidate relies on a strict global growth certificate and does not claim a generic approximation scheme for all mixed-integer polynomial optimization. See also the project's [box-quadratic certificate audit](box-quadratic-jet-certificate-prior.md). |

All sources in the table have read packages in the local literature KB. No
additional source was routed for ingestion in this audit.

## What is standard and what remains distinctive

Once a finite shared grid is specified, exact min-sum DP on a supplied
tree decomposition is standard, with a table factor exponential in bag size.
Finite-domain IQP DPs and exact structured convex-indicator DPs already
demonstrate this solver capability. Generic global branch-and-bound also
provides a finite proof path for nonconvex QP under its stated assumptions.

The candidate's specific certificate is the bridge between those tools and
the original mixed continuum/lattice domain: feasible grids are laid over
physical displacement shells, diagonal variance alone bounds the error
under independent endpoint rounding, and a continuous first-order ray
argument fills the region below the smallest lattice-scale shell. The
shell-by-shell decomposition avoids raising the encoded shell count to the
bag-size power. The paper comparisons above establish close ingredients,
but this focused scan found no source proving that same combination of
physical mixed-lattice shells, a finite exact DP certificate for the full
domain, and a growth/curvature-controlled state count.

That last sentence records the scope of the search, not a priority claim.
The result should be described as a candidate direct optimality and growth
certificate for a supplied point, not as a new general MIQP solver. The
source set already contains exact global solvers in important special
classes, finite branch-and-bound for general nonconvex quadratic problems,
and broad treewidth approximation results. Any stronger originality claim
would require a wider search and review of the candidate proof, especially
its rational bit bounds and the bottom-shell argument.
