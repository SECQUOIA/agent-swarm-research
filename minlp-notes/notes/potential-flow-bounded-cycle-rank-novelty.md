# Novelty audit: MPD with bounded cycle rank in each block

Date: 2026-09-05. This note audits [the block-cycle-rank investigation](potential-flow-block-cycle-rank-investigation.md). It concentrates on the extension beyond the cactus result; the [cactus novelty audit](potential-flow-cactus-approximation-novelty.md) supplies the broader MPD literature and attribution for the electrical derivative identity.

**Assessment:** no prior theorem was found giving precision-polynomial additive MPD optimization for bounded maximum cycle rank of a biconnected block. No matching use of a positive-source adjoint perturbation to obtain a bounded-dimensional nomination face was found. The candidate appears to extend the single-cycle and cactus results substantially, subject to its separate mathematical reviews. Cycle-space parameterization, path suppression, electrical differentiation, and fixed-dimensional algebraic solving are established ingredients. The distinct proposed contribution is a global nomination-structure argument that leaves only a number of free loads controlled by the cycle rank, even when a block has arbitrarily many subdividing vertices.

## What is stronger than a fixed number of cycles

The parameter is

\[
r_{\max}=\max_{H\text{ a biconnected block}}(|E(H)|-|V(H)|+1),
\]

with bridges treated separately. The candidate permits arbitrarily many blocks and arbitrarily many independent cycles overall. Rank one recovers cacti. Rank two permits subdivided theta blocks, and rank three permits subdivided \(K_4\) blocks. The latter are outside the series-parallel class. These are graph-theoretic consequences of the stated parameter, not separate literature claims.

The objective nodes and signed rational nomination intervals are arbitrary. The graph is passive, with positive rational quadratic resistances, and the MPD subproblem has no arc capacities or potential bounds. The output is a certified additive value interval and a rational feasible near-optimal nomination. The runtime is polynomial in input length and precision bits for each fixed rank bound; the exponent may depend on that bound. This is not an FPT claim and does not settle exact threshold equality.

The advance is not simply that a spanning-tree representation uses one circulation variable per independent cycle. That observation reduces physical-state dimension **after nominations are fixed**. An unrestricted nomination box still has a growing number of free coordinates. The perturbed-adjoint argument is what the candidate adds to make the combined state-and-nomination dimension bounded.

## Closest bounded-cycle algebraic predecessors

Gotzes, Nitsche, and Schultz, *Probability of Feasible Loads in Passive Gas Networks with up to Three Cycles* (2017), is a directly relevant precursor on small cycle systems. Its title and report details are confirmed by [the author's publication page](https://www.uni-due.de/mathematik/agschultz/claudia_publikationen_engl.php). The OPUS report link returned an access error in this audit, so no claim here relies on having inspected that report's full proof.

The accessible primary continuation is Sabrina Nitsche's 2018 dissertation, *Analytical and Algebraic Approaches to Gas Transportation with Uncertain Loads*. It develops cycle equations and Gröbner/comprehensive Gröbner methods. Chapter 6, Algorithm 6.2, computes feasible radial load intervals for spherical-radial probability integration: the nominations on each such ray depend on one scalar. Later computational discussion reports treatment of up to three interacting fundamental cycles and numerical difficulties for larger systems. This is important prior for low-cycle algebraic physical-state analysis. It does not establish optimization of MPD over all coordinates of a balanced nomination box or the proposed free-load bound. [Primary thesis](https://duepublico2.uni-due.de/servlets/MCRFileNodeServlet/duepublico_derivate_00046525/DissSabrinaNitsche.pdf).

Denis Aßmann's 2019 dissertation, *Exact Methods for Two-Stage Robust Optimization with Applications in Gas Networks*, Section 2.3, explicitly derives spanning-tree/circulation parameterization and credits Gotzes et al. (2016) and earlier hydraulic formulations. Section 4.4.3 discusses polynomial reformulations of absolute values and a single-cycle uncertainty partition; Chapter 5 derives a different decomposition of two-stage robust gas problems. It supplies no matching bounded-block-cycle-rank MPD approximation theorem. [Primary thesis](https://d-nb.info/1196351791/34).

Ralf Lenz and Kai Helge Becker, *Optimization of Capacity Expansion in Potential-driven Networks including Multiple Looping – A comparison of modelling approaches*, ZIB Report 18-44 (2018), explicitly varies cycle rank in its computational tests. Its problem is capacity expansion and its contribution compares optimization formulations. It is not an MPD complexity theorem. The term “cycle rank” in gas-network optimization therefore is not new. [Primary report](https://edocs.tib.eu/files/e01fn18/1029867585.pdf).

## The perturbed adjoint: precise novelty boundary

The candidate perturbs the **local potential objective**, adding a positive coefficient for every degree-two path-interior potential. It first smooths the quadratic edge law so the linearized electrical resistances are positive. On every such path, the perturbed adjoint current has strictly positive increments. The resulting potential sequence rises then falls, with at most a two-vertex plateau. A common box/balance multiplier consequently leaves at most two free internal nominations per path. Compactness passes an optimizer back to one of these finitely many closed faces as both perturbations vanish.

The electrical current identity is elementary Kirchhoff conservation, and the relation between an objective's potential coefficients and adjoint forcing is standard. The candidate-specific idea is choosing the objective perturbation so that all long paths have the same sign of internal adjoint forcing, then using the resulting threshold pattern to control the number of free nominations. Generic perturbation alone would not prove the necessary path ordering or polynomial face count. No directly matching argument was found in the inspected MPD or gas-network sources.

The known inverse grounded-Laplacian derivative formula should retain credit to Misra, Vuffray, and Chertkov (2015), Lemma 1, equations (19) and (21), as detailed in the cactus audit. A further search found Sonja Hossbach's *Finite-difference-based simulation and adjoint optimization of gas networks* (2022), which derives transient adjoints for numerical local optimization and explicitly disclaims guaranteed global optimization. This does not supply the proposed structural theorem. [Primary stationary-flow derivative source](https://arxiv.org/abs/1504.02370), [open transient-adjoint paper](https://doi.org/10.1002/mma.8030).

Path suppression here is **topological bookkeeping**. It is not a replacement of a path containing independent uncertain nominations by a physically equivalent single pipe. Consequently it does not contradict the nonlinear network-reduction limitations discussed in Raber's 2022 dissertation and subsequent reduction work.

## A sharp limitation already follows from the known hardness reduction

The bounded cycle-rank assumption cannot be replaced by bounded treewidth or bounded feedback-vertex number while retaining the same precision-polynomial guarantee, unless \(P=NP\). This is a consequence of an existing primary reduction, rather than a new independent hardness proof.

Thürauf's *Deciding the feasibility of a booking in the European gas market is coNP-hard* (2022), Section 4, Figure 2, constructs vertices \(s,t,z_i^+,z_i^-\) and edges

\[
\{s,z_i^+\},\quad\{z_i^+,t\},\quad\{z_i^+,z_i^-\}
\qquad(i=1,\ldots,n).
\]

Lemma 4.3 gives MPD at least one for a feasible Partition instance. Lemma 4.17 gives MPD below \(T(K)<1\) for an infeasible instance. Equation (3) defines a rational, polynomial-encoding-length \(T(K)\). [Primary published paper](https://d-nb.info/1265956588/34), [author manuscript](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf).

The following deductions are our analysis of that construction:

1. Its nontrivial block is \(K_{2,n}\), so its block cycle rank is \(n-1\). Pendant exits do not change this.
2. It has treewidth two: bags \(\{s,t,z_i^+\}\) arranged in a path, with each pendant bag \(\{z_i^+,z_i^-\}\) attached to its corresponding bag, give a width-two decomposition. It is series-parallel as an undirected graph.
3. Its undirected feedback-vertex number is one: deleting \(s\) leaves the tree with branches \(t-z_i^+-z_i^-\).
4. Let \(g=1-T(K)>0\). A certified value interval of width at most \(g/4\) distinguishes MPD below \(T(K)\) from MPD at least one, by comparison with \((1+T(K))/2\). Because \(T(K)\) has polynomial rational encoding length, \(\log(1/g)\) is polynomially bounded in the Partition input length. Thus a polynomial-in-input-and-precision algorithm on either of these broader fixed-parameter graph classes would solve Partition in polynomial time.

This distinguishes **feedback edges**, measured by cycle rank, from **feedback vertices**. One vertex can participate in arbitrarily many independent cycles. It also explains why the candidate is compatible with the known general MPD hardness even though both concern sparse networks. The candidate's allowance of arbitrarily many low-rank blocks remains meaningful: the hardness construction puts an unbounded rank inside one block.

## Priority and remaining uncertainty

Relative to the cactus theorem, the broader result deserves priority as the main structural theorem if its independent reviews pass. It handles interacting cycles and non-series-parallel fixed-rank blocks, while leaving arbitrarily many nominations and blocks. The cactus case is then a transparent special case and the earlier exact SRS result explains why approximation, rather than equality-sensitive exact optimization, is the appropriate guarantee across many blocks.

The 2026 overview and single-cycle paper already establish the motivation for extending tractability beyond a cycle; their details are in the cactus audit and are not repeated here. Searches specifically combined MPD, potential-based/dissipative flow, cycle rank, cyclomatic number, bounded cycles, feedback edges, feedback vertices, biconnected blocks, treewidth, adjoint perturbation, unimodality, and uncertainty. No matching theorem was found. The small-cycle probability literature is the closest additional source family identified. The inaccessible 2017 OPUS report and possible unindexed work remain limits of the search. Novelty should be stated as not found in the inspected open literature, not as conclusively established absence of all antecedents.
