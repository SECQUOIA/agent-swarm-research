# Independent audit: joint nomination and resistance optimization

Date: 2026-09-05. Reviewer: independent `benders_review` agent.

The candidate in [the investigation note](potential-flow-joint-resistance-investigation.md) is mathematically correct for a finite connected passive quadratic network with independent finite rational nomination intervals, their balance equation, and independent strictly positive rational resistance boxes. The bound on each biconnected block's cycle rank is fixed. The conclusion is polynomial bit complexity for additive potential-difference optimization and feasible rational nomination/resistance output. It is not an exact pressure-threshold algorithm.

This audit uses the two independent reviews of the bounded-cycle-rank nomination theorem and my independent review of the fixed-core/polyhedral-block theorem. It checks the new composition, resistance sensitivity, and output encoding. It also approves the exact edge-flow consequence detailed below, subject to retaining its stated model scope. Literature novelty is separate.

## 1. The nomination faces transfer without a new perturbation argument

The family of nomination faces in the bounded-cycle-rank theorem depends on graph paths, topological core vertices, interval endpoints, and balance. Its enumeration does not depend on the numerical resistance vector. This independence is the essential fact.

Take a joint optimum `(b*,β*)`. At this fixed `β*`, the reviewed nomination theorem supplies a nomination optimum on an enumerated face. Its value equals the joint optimum: it cannot be worse than `b*` at the same resistance vector, and cannot exceed the global joint optimum. Thus the same resistance vector and a suitable face nomination form a joint optimum. The same argument applies to the local bounded-free-coordinate refinement inside the selected block.

This argument is simpler than repeating smoothing and objective perturbation while optimizing resistances jointly. It needs the established fixed-resistance structural result for every positive resistance vector and its resistance-independent face family. Both properties hold in the reviewed theorem. No resistance stationarity condition and no assumption that nomination intervals contain zero is used.

Joint attainment follows from continuity and compactness. For completeness, route nominations on a fixed spanning tree and express the remaining flow by circulations. Passive nonzero flows follow strictly decreasing potentials and therefore form an acyclic directed flow, so every edge carries at most total positive injection. For convergent nomination/resistance sequences, the physical flows have a convergent subsequence. Comparing their strictly convex energies against translated feasible competitors shows that the limit is the unique energy minimizer for the limiting data. Hence all physical flows converge; normalized potentials then converge by summing continuous edge drops on tree paths. This establishes joint continuity on the compact uncertainty domain.

The graph must be connected, or each component must separately satisfy balance and the objective endpoints must lie in the same component. The candidate should state the connected case explicitly; global balance alone would not suffice on a disconnected graph.

## 2. Inactive blocks really separate

After off-path aggregation, potential difference is the sum of drops along the objective's block path. A selected-block face fixes every outside nomination and fixes the total nomination of the selected block by global balance.

The effective nomination at a boundary vertex of any inactive block is the sum of original nominations in the corresponding attached component. Such a component contains either all varying nominations of the selected block or none of them. In the former case their sum is fixed. Therefore all effective nominations of each inactive block are fixed, including at shared articulations. Its unique flow and local potential drop depend only on those effective nominations and its own resistances.

Since resistance boxes are independent and different blocks have disjoint edge sets, their resistance optimizations separate exactly. Conversely, independently chosen local optimizers glue to a global physical solution: conservation holds at articulations by the effective-nomination construction, and local potentials can be shifted to agree along the block tree. Off-path blocks affect only their attachment's aggregate nomination and can use arbitrary rational resistances in their boxes.

Coupled uncertainty constraints across resistance blocks would invalidate this separation. No such constraints are present in the candidate.

## 3. Exact mapping to the fixed-core theorem

On an active nomination face with at least one free coordinate, eliminate one coordinate using the rational balance equation. There are at most `8r−3` independent nomination coordinates. Add at most `r` fundamental-cycle coordinates. For a non-bridge block this gives core dimension at most `9r−3`. A fixed-nomination block uses only its at most `r` circulation coordinates. Faces without free coordinates and bridges are handled separately, so the negative dimension formula at `r=0` is never used.

A tree routing is affine in the independent nominations and zero on chords. Normalize each fundamental-cycle coordinate to equal its chord flow. Every edge flow is then affine in the core, and every circulation coordinate is bounded by the same rational injection bound as physical flows. The core's nomination bounds, circulation box, and closed sign-cell inequalities form a compact rational semialgebraic set of polynomial description size.

On a flow-sign cell, `x_e|x_e|` equals the polynomial `σ_e x_e²`. Using the cell closure is harmless: at a zero-flow boundary both neighboring sign formulas equal zero. Retaining all cells or their closures covers lower-dimensional feasible cores as well.

Conservation is already enforced by the affine flow representation. The remaining fundamental-cycle equations are

\[
\sum_e Z_{ie}\beta_e\sigma_e x_e(z)^2=0.
\]

These equations are sufficient as well as necessary. A vector of edge drops annihilating the cycle space is a potential gradient. Together with conservation and the strictly increasing passive laws, it specifies exactly the unique physical flow for those nominations and resistances. There are no extraneous nonlinear feasible points introduced by the sign decomposition.

Each `β_e` is one scalar leaf with a fixed rational box. There are at most `r` aggregate equations, whose coefficients are quadratic polynomials of the fixed-dimensional core. A path drop is a sum of leaf-linear terms with the same quadratic coefficients. This is precisely the reviewed fixed-core model. Minimization versus maximization is handled by negating the objective. Zero-width resistance boxes are valid bounded leaves.

For bridges, conservation fixes the through-flow when nominations are fixed; maximizing `β x|x|` chooses an appropriate resistance endpoint according to the sign of `x`. An active bridge has one independent nomination parameter. The objective is increasing in its oriented flow for every positive resistance, so first take the largest feasible flow and then the appropriate resistance endpoint. These cases need no cycle equations.

The number of nomination faces and flow-sign cells is polynomial for fixed block rank. The fixed-core theorem supplies exact local algebraic values and local algebraic optimizers of polynomial encoding length. Its resistance leaves have constant vertex denominators; even the general theorem's polynomial denominator-degree growth is unnecessary here.

## 4. Sum intervals, not common algebraic fields

Each block's algebraic optimizer and value may use its own polynomial-degree field. The degree of a common field containing optimizers from an unbounded number of blocks can be exponential. No such common field is needed or should be constructed.

Approximate each local value by a rational enclosing interval of width `η/q`, where `q` bounds the number of objective-path blocks. Summing endpoints encloses a face optimum within width `η`. The maximum of lower endpoints and maximum of upper endpoints over the polynomially many faces again gives a width-`η` enclosure of the global optimum. Selecting a face with maximum lower endpoint loses at most `η` relative to the true global optimum.

Coordinates can likewise be isolated and rounded within each local field separately. Only the single active block has varying nomination coordinates; other nomination coordinates are fixed rational endpoints. None of these steps requires comparing an unbounded algebraic sum exactly. This distinction supports the additive conclusion while preserving the previously identified pressure-threshold barrier.

## 5. Resistance sensitivity and the joint Lipschitz constant

For smoothed laws, write `ψρ(x)=x|x|+ρx` and let `B_inc` be the oriented incidence matrix. With nominations fixed, differentiation gives

\[
B_{\rm inc}D^{-1}B_{\rm inc}^{\mathsf T}\,d\pi
=B_{\rm inc}D^{-1}\operatorname{diag}(\psi_\rho(x))\,d\beta,
\qquad
D=\operatorname{diag}(\beta_e(2|x_e|+\rho)).
\]

For the ordinary unit-source/unit-sink adjoint `h`, this yields the signed derivative

\[
\frac{\partial F_\rho}{\partial\beta_e}
=j_{h,e}\psi_\rho(x_e),\qquad
j_{h,e}=(B_{\rm inc}^{\mathsf T}h)_e/D_{ee}.
\]

The sign and normalization in the draft are correct. Orient every nonzero adjoint current in the direction of decreasing `h`. This flow is acyclic and has total source one, so every edge current has absolute value at most one. This bound is for the ordinary objective adjoint; the positive-internal-source perturbed adjoint used in the face proof has a different total source and should not be substituted here.

With physical flows bounded by `B`, the derivative magnitude is at most `B²+ρB`. Integrating along a resistance-box segment is valid because every resistance remains positive. The previously proved nomination estimate is uniform after replacing each path resistance by its upper bound. Integrating the two changes separately and taking the smoothing limit gives

\[
|F(b,\beta)-F(c,\gamma)|
\le C_b\|b-c\|_1+B^2\|\beta-\gamma\|_1,
\qquad C_b=2B\sum_{e\in P}\overline\beta_e.
\]

This estimate does not assert componentwise resistance monotonicity. Its rational constants have polynomial bit length, even when numerical magnitudes are large. If `B=0`, all core physical flows and the objective are zero; return a rational feasible nomination and resistance vector directly rather than dividing by a zero rounding constant.

## 6. Rational recovery preserves exactly the intended feasibility

Refine isolating intervals for the active block's finitely many algebraic nomination coordinates. Intersect the resulting rational boxes with the original rational nomination intervals and the exact balance hyperplane. The algebraic optimum witnesses nonemptiness. Rational LP produces a rational nomination with the prescribed total `l1` error and exact feasibility. Off-path nomination groups can then be disaggregated within their rational original intervals.

For each edge, intersect a sufficiently narrow rational isolating interval for its algebraic resistance with its original rational resistance box, and choose any rational point in the intersection. This also handles optima at box endpoints. There may be many interior resistance coordinates, but allocating error inversely to their count costs only logarithmically many additional precision bits.

The circulation coordinates need not remain feasible after this rounding. They are not the claimed output. Every rounded feasible nomination/resistance pair has its own unique physical solution, and the global Lipschitz estimate controls its potential difference. This is why rational recovery does not require rational physical flows or potentials and does not need to preserve the original sign cell or cycle equations under rounding.

For example, use face-value enclosures of width `ε/4`, allocate `C_b||Δb||_1≤ε/4` and `B²||Δβ||_1≤ε/4`, and use exact local optimizers. The selected rational pair then loses at most `3ε/4`. A separately computed global value interval can have width at most `ε`. Standard small adjustments handle zero constants. All requested bit precisions remain polynomial in input size and `log(1/ε)`.

## 7. Exact edge-flow extrema and capacity validation

The author's additional consequence is also valid. Fix an oriented edge `e=(u,v)` and maximize its physical flow jointly over nominations and resistance boxes. At a joint optimizer, fix its resistance vector. Since

\[
\pi_u-\pi_v=\beta_e x_e|x_e|
\]

is strictly increasing in `x_e` at fixed positive `β_e`, a nomination maximizing the endpoint potential difference also maximizes `x_e`. The resistance-independent nomination-face theorem can therefore replace the optimizer's nomination by one on the same bounded-dimensional family without losing the joint flow optimum.

The edge endpoints belong to a single block. All other components can be aggregated into that block's vertices. Thus its objective has no sum of independently algebraic block drops. On each face/sign cell, `x_e` is an affine core function, so it fits the fixed-core theorem through its core objective term. Exactly comparing the polynomially many resulting algebraic values is polynomial time: pairwise comparisons of polynomial-degree algebraic numbers suffice, and the winning value is one of the local values. No unbounded common-field construction is needed. Minimize by reversing the edge orientation and the objective terminals. Bridges reduce directly to linear nomination optimization.

Consequently, testing whether every uncertainty realization's passive physical flow satisfies specified rational lower and upper bounds on every edge reduces to at most two exact extrema per edge. This is exact polynomial-time robust capacity validation for fixed maximum block cycle rank. The bounds being validated are not imposed as extra constraints when defining the underlying passive state; that different constrained-uncertainty optimization is not justified by this argument. Exact extrema and optimizing uncertainty can be algebraic rather than rational.

The separate [exact arc-capacity draft](potential-flow-exact-arc-capacity-investigation.md) was read in full and passes this review. I flagged its optional rational near-optimal flow-output claim for clarification: a joint pressure maximizer need not maximize edge flow when the edge resistance also varies. The author corrected the claim to round an exact **edge-flow** optimizer. The needed explicit estimate is valid:

\[
|x_e-y_e|^2\le\frac{2}{\underline\beta_e}
\left(|F_e-G_e|+B^2|\beta_e-\gamma_e|\right)
\le\frac{2}{\underline\beta_e}
\left(C_b\|b-c\|_1+2B^2\|\beta-\gamma\|_1\right),
\]

where `F_e,G_e` are the endpoint potential differences and `C_b=2B β_upper,e` uses the single-edge path. The scalar inequality behind this is `|x−y|²≤2|φ(x)−φ(y)|` for `φ(x)=x|x|`, including opposite-sign flows. Hence an `O(ε²)` parameter-error allowance yields additive `ε` flow accuracy with only polynomially many precision bits. This quantitative rounding argument, rather than qualitative continuity alone, supports the optional output statement.

## 8. Independent numerical checks

[The independent checker](../code/potential_flow_mpd/joint_resistance_review_checks.py) uses the ordinary unit-source adjoint on twelve subdivided theta and K4 networks with shifted balanced nominations. It passed 60 resistance finite-difference checks and twelve simultaneous nomination/resistance sensitivity-bound checks. The maximum derivative error was `1.1e-9`, the largest absolute adjoint edge current was about `0.868`, and the maximum physical residual was `1.99e-12`.

These checks support the sensitivity formulas and distinguish the ordinary adjoint from the perturbed one. The structural and polynomial-complexity claims rest on the exact arguments above and their independently reviewed dependencies, not on numerical testing. Novelty and publication significance require the separate literature investigation.
