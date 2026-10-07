# Prior-art audit: conditioned exact algorithms for sparse nonconvex box QPs

Date: 2026-10-02. This is a focused read-only prior-art audit for the
[regridded rational box-QP theorem](../geometric-dp/regridded-qp-bit.md) and
its feedback-vertex-set follow-up. It does not establish priority, and it
does not maintain the literature knowledge base.

## Finding

The strongest direct exact comparator is Del Pia and Khajavirad's exact
dynamic program for continuous rational box QPs on forests. It is already a
Turing-model result with polynomial-length intermediates and a rational
optimizer output; its `O(n^2)` arithmetic/comparison bound is not merely a
real-RAM statement. It requires no uniqueness or growth promise, but applies
only at interaction-treewidth one. The same paper proves strong
NP-hardness at treewidth two for unrestricted box QPs with small integral
coefficients. That hardness does not address the present global-growth
promise.

The candidate theorem occupies a narrower, conditioned regime above that
forest boundary: rational continuous box QPs with a supplied bag
factorization and decomposition, a unique global minimizer, global quadratic
growth with constant `g`, and a supplied rational bound `M` on every bag
Hessian norm. It is FPT in bag size `p`, variable occurrence `k`, and
`κ = max(1, M/g)`, with an absolute exponent on input length and
accuracy bits; exact optimizer and value recovery are also claimed in this
parameterization, and the algorithm need not be given `g` or `κ`. Its affine
lower models reduce each table subproblem to
exact corner choices, so it needs no nonlinear optimization oracle. The
conditioned fixed-parameter guarantee and bit bound, rather than sparse-QP
dynamic programming by itself, are the plausible contribution.

The project’s [exact-box-QP note](../geometric-dp/exact-box-qp.md) proves
that uniqueness on a compact continuous box already implies some positive
global quadratic-growth constant for a quadratic objective. This is only a
qualitative fact: the constant may be exponentially small relative to the
input, so uniqueness alone does not give the theorem’s useful running-time
bound. The QG promise is a conditioning parameter, not convexity or an
automatic uniform polynomial-time guarantee.

This use of QG sits beside a broader local stability literature. Bonnans and
Ioffe's [“Second-order Sufficiency and Quadratic Growth for Nonisolated
Minima”](https://doi.org/10.1287/moor.20.4.801) studies the relation between
weak second-order sufficient conditions and quadratic growth for nonlinear
programs, including isolated minima under a constraint qualification. That
is local optimality theory, not a global exact box-QP algorithm or a
complexity result. I checked the publisher abstract; the full text was not
available from the publisher route used here.

The parameters must remain explicit. This is not an FPT result in treewidth
and global Hessian conditioning alone: the current theorem has an occurrence
parameter and uses a per-bag absolute Hessian bound that depends on the
provided factorization. The forest algorithm already solves the `p=2`
interaction-graph case without these assumptions. The width-two hardness
result rules out removing structural or conditioning promises from a broader
claim; it does not show hardness under global quadratic growth.

Relative to the earlier shared-coordinate-grid result and the continuous
regridding certificate in the [geometric-grid audit](geometric-grid-prior.md),
this QP theorem improves the parameterized bit bound: the exponent of
`I+q+1` no longer grows with bag size. It also replaces the continuous
convex-optimization oracle with rational affine minimization over corners.
The tradeoff is a stronger full-bag Hessian bound and explicit dependence on
variable occurrence; it is not an automatic bit-complexity upgrade for the
broader factor/oracle model.

A separate development uses a supplied feedback vertex set `C` of size
`r`, with `G−C` a forest; it needs no supplied tree decomposition. For hub
values `h=x_C`, define the exact forest recourse value
`v(h)=min_y F(h,y)`, where `y` collects the non-hub coordinates. The proposed
core curvature parameter is `L=max(0,max_{i∈C} 2Q_ii)`. If `L=0`,
coordinatewise concavity reduces
the hub search to `2^r` endpoint assignments and no growth promise is
needed. If `L>0`, the proposed promise is that `v` has a unique minimizing
hub vector `h*` and global projected growth
`v(h)−f* ≥ g ||h−h*||^2`; the full optimizer need not be unique. A unique
full optimizer with global QG is a sufficient stronger promise. With
`κ=max(1,L/g)`, the proposed exact algorithm uses corrected dyadic
branch-and-bound, with `O((1+sqrt(rκ))^r)` active hub boxes per level,
followed by exact hub reconstruction and an exact forest-oracle call. The
stated bit bound is `f(r,κ) poly(I)` and the search need not know `g`. Its
candidate-specific ingredient is the bound on active boxes from projected
growth and semiconcavity. The targeted search found no prior global exact
box-QP result with this arbitrary-sign, projected-QG FPT-in-`(r, κ)`
guarantee. This is not a treewidth-only result:
chains of vertex-disjoint triangles joined by bridges have treewidth two and
feedback vertex set size linear in the number of triangles.

There is a relevant fixed-parameter caveat. Del Pia and Khajavirad's
Theorem 4 already yields polynomial time for each fixed `r` in the special
case where the positive-diagonal vertices themselves form the feedback
vertex set and all other diagonal entries are nonpositive. Their hypotheses
then hold with forest negative-diagonal graph, at most `r` hub neighbors per
component, and cross-rank at most `r`. The theorem uses additional sign and
component/rank structure and does not state a uniform FPT bound in `r`; its
proof bounds the arrangement cell count by `O(H^ρ)`, where `H` is the number
of hyperplanes and `ρ≤r`, so that argument is XP-shaped rather than an
explicit uniform FPT bound. The
proposed FVS result should therefore be framed as the arbitrary-sign,
projected-QG-conditioned FPT extension, not as first polynomial solvability
at fixed feedback-vertex-set size.

The same paper also reaches some width-two block graphs. Most directly,
Corollary 8 covers block-cactus interaction graphs (blocks are cliques or
cycles) with clique number `O(log n)`, provided the positive-diagonal
induced graph is a forest and the cut-vertex-containing positive components
have `O(log n)` interfaces into each remaining component and constant-rank
coupling to those interfaces. Thus a chain or tree of triangle blocks is
already covered when these additional sign/interface/rank conditions hold,
even if its feedback vertex set is large. This is not an algorithm for
arbitrary box QPs on such a graph: the block-cactus theorem depends on those
extra conditions. Theorem 3's width-two hardness remains the unrestricted
boundary. The forest DP's exact concave piecewise-quadratic messages also
show that message closure is established for forests; the cited paper does
not give a general message-piece bound for arbitrary bounded-size blocks
under QG.

## Closest exact and conditioned algorithms

| Work | Result and computational model | Relation and limit |
|---|---|---|
| Alberto Del Pia and Aida Khajavirad, [“Treewidth and the complexity of box-constrained quadratic programs”](https://arxiv.org/abs/2609.35595), arXiv:2609.35595v1 (2026) | Theorem 1 gives an exact leaf-to-root value-function DP for rational continuous box QPs whose interaction graph is a forest, using `O(n^2)` arithmetic operations and comparisons. The authors define strong polynomiality to include polynomial-bit intermediate values in the Turing model. Lemma 19 recovers an optimal rational vector of polynomial encoding length by backtracking. Theorem 3 proves strong NP-hardness at treewidth two even for integral `Q,c` with `||Q||max ≤ 5`, `||c||∞ ≤ 4`. Theorem 4 also gives polynomial-time classes of possibly unbounded full treewidth by making nonpositive-diagonal variables binary at an optimum and imposing graph-boundary, cross-rank, and positive-component solvability conditions. | This is the closest direct predecessor and a stronger result on forests: it needs no QG promise and already establishes exact rational optimizer output. Its Theorem 4 covers fixed-`r` polynomial time when positive-diagonal vertices form an `r`-vertex feedback set and the remaining variables have nonpositive diagonal, but it uses extra sign/component/rank structure and does not provide a uniform `f(r,κ) poly(I)` bound. The forest result does not cover general treewidth or the candidate's conditioned bit bound. The width-two hardness is unrestricted and cannot be read as hardness under the candidate's promise. I checked the primary [arXiv HTML](https://arxiv.org/html/2609.35595v1), especially §1, Theorem 1, §2.4 Lemma 19 and bit-length proof, Theorem 3, and §4.2 Theorem 4. |
| Aaresh Bhathena, Salar Fattahi, Andrés Gómez, and Simge Küçükyavuz, [“Solving Convex Quadratic Optimization with Indicators Over Structured Graphs”](https://arxiv.org/abs/2603.02103), arXiv:2603.02103 (2026) | Exact parametric DP for a positive-definite quadratic objective with binary support indicators. The efficient bound uses bounded treewidth, polynomial volume growth, and a `(k, eta)`-margin condition; Theorem 1 bounds time by `O(n ω^2 δ k_δ^2 4^(Δ_(m+1)))` and memory by `O(n ω^2 k_δ 2^(Δ_(m+1)))`, with linear dependence on `n` for fixed structural/numerical parameters. | This is the closest conditioning/margin-based exact treewidth DP. It concerns convex indicator QP, not arbitrary nonconvex continuous box QP; its pruning argument controls relevant binary support patterns in a bounded solution region. It does not supply the global-QG, recentered certificate or the candidate's exact rational Turing FPT theorem. I checked the read KB package and its extracted full text, with the theorem statements against the package's original PDF. |
| Daniel Bienstock and Gonzalo Muñoz, [“LP Formulations for Polynomial Optimization Problems”](https://arxiv.org/abs/1501.00288), SIAM J. Optim. 28(2), 2018 | Treewidth-based LP approximations for mixed-integer polynomial optimization. Their formulation size has a power dependence on `1/ε`, with an exponent depending on structural width/degree; the guarantee is scaled feasibility and optimality. | A broad sparse global-optimization approximation result, but not an exact Turing FPT algorithm with accuracy-bit exponent independent of bag size. I checked the local extracted full text, including Theorem 7 and the stated size bound. |
| Daniel Bienstock and Tongtong Chen, [“Solving convex QPs with structured sparsity under indicator conditions”](https://arxiv.org/abs/2411.11722), arXiv:2411.11722 (2024) | A width-dependent approximation algorithm for convex quadratic programs with block indicators and combinatorial constraints. Theorem 14 returns a superoptimal point satisfying combinatorial constraints, with mixed-integer constraint violation at most `max_r |B_r| ε`; the runtime has a power dependence on `1/ε` and includes blockwise convex QP solves. | Relevant structured convex-QP approximation, but a different block/indicator model and approximate-feasibility guarantee. It does not handle general nonconvex box QP under QG or exact rational recovery. I checked the local extracted full text, including Theorem 14. |
| Ciamac C. Moallemi and Benjamin Van Roy, [“Convergence of Min-Sum Message-Passing for Convex Optimization”](https://arxiv.org/abs/0705.4253), IEEE Trans. Inf. Theory 56(4), 2010 | Proves iterative min-sum convergence for unconstrained separable convex objectives under scaled diagonal dominance and appropriate initialization, including computation-tree and asynchronous analyses. | Establishes convergence, not a finite global certificate or a treewidth-based bit-complexity bound; it assumes convexity and does not treat the nonconvex box-QP class. See also the project’s [tree-sensitivity audit](tree-sensitivity-audit.md). |
| Hoai An Le Thi and Mohand Ouanes, [“Convex quadratic underestimation and Branch and Bound for univariate global optimization with one nonconvex constraint”](https://doi.org/10.1051/ro:2006024), RAIRO Oper. Res. 40(3), 2006 | Uses quadratic lower bounds and interval subdivision in a one-dimensional smooth global-optimization branch-and-bound method. | Confirms that curvature-based underestimation and branching are established methods. It does not analyze sparse-QP recourse, projected QG, or FPT Turing complexity in the hub dimension. The primary open article is available from [Numdam](https://www.numdam.org/articles/10.1051/ro:2006024/). |

Vavasis's [“Quadratic programming is in NP”](https://doi.org/10.1016/0020-0190(90)90100-C) and the rational-QP discussion in Del Pia, Dey, and Molinaro's [“Mixed-integer quadratic programming is in NP”](https://arxiv.org/abs/1407.4798) are relevant to the standard polynomial-height certificate. The project proves the needed box-QP denominator and reconstruction bounds directly in [exact-box-qp.md](../geometric-dp/exact-box-qp.md). Short rational optimizer/value representations and continued-fraction reconstruction are established ingredients; they do not supply the candidate DP or its runtime.

## Sparse SDP and SOS exactness boundary

Sparse semidefinite exactness results already cover useful box-QP subclasses,
but their guarantees use sign and graph restrictions rather than a global
quadratic-growth promise. Khajavirad's [“Tight semidefinite programming
relaxations for sparse box-constrained quadratic programs”](https://arxiv.org/abs/2601.18545v2)
studies the convex hull of the lifted feasible set. Theorem 5 gives a
constructive SDP representation when each connected component induced by
positive-diagonal (“plus-loop”) variables has at most two vertices, with a
potentially exponential-size lift. Theorem 6 gives a polynomial-size lift
when, in addition, the plus-loop condition holds, graph treewidth is
`O(log n)`, and each plus-loop vertex has degree `O(log n)`. These are
objective-independent convex-hull results for a restricted sparsity/sign
pattern; they do not imply a bounded-order sparse certificate for arbitrary
box QPs from QG alone.

Qiu and Yıldırım's [“On Exact and Inexact RLT and SDP-RLT Relaxations of
Quadratic Programs with Box Constraints”](https://doi.org/10.1007/s10898-024-01407-y)
characterizes exactness for particular global RLT and SDP-RLT relaxations.
Their Corollary 3.2(ii) shows the SDP-RLT underestimator touches the original
objective at any local or global box-QP minimizer, but the paper explicitly
notes this necessary contact condition is generally not sufficient for
relaxation exactness. It does not give a QG-plus-treewidth criterion for
exactness.

For SOS hierarchies, Nie's [“Optimality Conditions and Finite Convergence of
Lasserre's Hierarchy”](https://doi.org/10.1007/s10107-013-0680-x), Theorem
1.1, proves finite convergence under an Archimedean condition plus constraint
qualification, strict complementarity, and second-order sufficiency at every
global minimizer. The result is not a sparsity- or QG-based degree bound, and
the paper notes that a uniform hierarchy order for generic instances
typically does not exist. Thus finite SOS convergence under its stronger
local conditions is known; QG by itself has not been shown in these sources
to yield a bounded-order sparse SOS/PSD certificate at bounded treewidth.

These sources do not make the proposed sparse DP/certificate result
redundant. The candidate's novelty should still be limited to the proved
conditioned algorithm and its explicit parameter/bit bounds; exactness of
sparse convex relaxations or SOS hierarchies should not be claimed as a new
principle.

## Occurrence, degree, and modulator parameters

Variable occurrence is independent of treewidth. For example, in a star,
every bag of size `p` can cover at most `p-1` of the center's incident
edges, so any such decomposition places the center in at least
`ceil(deg(center)/(p-1))` bags. A treewidth-only claim cannot silently
discard `k`.

There is a useful structural tradeoff. David R. Wood,
[“Tree-Decompositions with Small Width, Spread, Order and Degree”](https://arxiv.org/abs/2509.01140), arXiv:2509.01140v3 (2026), Theorem 2, gives a decomposition of width at most \(14\operatorname{tw}(G)+13\) in which each vertex appears in at most \(\deg_G(v)+1\) bags. Theorem 7 also bounds the decomposition-tree maximum degree by six while preserving these width and spread bounds. Thus bounded maximum degree permits replacing occurrence by \(\Delta+1\), at the cost of a constant-factor width increase, if the algorithm is supplied a decomposition with this spread. The theorem does not remove dependence on degree for general graphs. Since the QP theorem's (M) is a bound on the Hessians of the chosen bag factors, any regrouping onto a new decomposition must also recheck that conditioning parameter. I read the theorem statements in the primary [arXiv HTML](https://arxiv.org/html/2509.01140).

Generic cycle-cutset conditioning normally assumes finite hub domains; that
principle alone does not give a bound for continuous hubs. The univariate
branch-and-bound source above supplies no FPT-in-`(r,κ)` bit bound,
projected-growth packing estimate, or exact forest recourse. No direct prior
with the stated nonconvex-QP, projected-QG, and exact bit-complexity
combination was located in the targeted searches. This is a qualified search
result, not evidence of novelty.

The two FPT formulations are complementary. Small occurrence may hold when
the graph has many cycles; a small feedback vertex set may hold when some
variables occur in many bags. Neither parameter is bounded by treewidth
alone. In particular, bounded-treewidth graphs can have linear feedback
vertex-set size, and high-degree stars force large occurrence at fixed
bag size.

## What supports a novelty claim

The components below are established or have close precedents: exact
finite-state tree-decomposition DP; exact value-function DP on forest QPs;
interval branch-and-bound; affine/Taylor underestimators for bounded
curvature; sparse rational QP height bounds; and graph decomposition by
small modulators. The candidate should not claim any of these alone as new.

The candidate-specific package is narrower:

- a global-QG-conditioned exact Turing algorithm for nonconvex rational
  continuous box QPs above interaction width one, parameterized by
  \((p,k,M/g)\), with input/accuracy-bit exponents independent of these
  parameters;
- a valid global objective interval at every refinement stage, with affine
  quadratic lower models minimized by exact corners and no nonlinear
  optimization oracle; and
- for the feedback-vertex-set formulation, a count of active master boxes
  per accuracy level under projected QG and semiconcavity, composed with
  exact forest recourse. This formulation permits nonunique full optimizers
  when the hub projection is unique.

For the first claim, keep the decomposition and factorization part of the
input, retain occurrence (k), and distinguish the per-bag norm (M) from
the global Hessian norm. The growth constant need not be known by the
algorithm, but the runtime depends on `M/g`; a unique optimizer alone does
not make this parameter small. For the second claim, present the
feedback-vertex-set result as a complementary FPT theorem, not as a general
treewidth-only result. Its growth promise is on the projected recourse
value, so full optimizer uniqueness is not required. The exact height
argument is a standard final reconstruction step, not its own novelty claim.

## Scope and sources checked

The review checked the primary Del Pia–Khajavirad forest, width-two
hardness, and sign-structured results; the read project-KB texts for
Bhathena et al., Bienstock–Muñoz, Bienstock–Chen, and Moallemi–Van Roy;
Wood's spread theorem; and the publisher abstracts for Le Thi–Ouanes and
Bonnans–Ioffe.
Targeted terminology searches covered nonconvex quadratic programming
combined with feedback vertex set, cycle cutset, treewidth, quadratic
growth/error bounds, and conditioned global optimization. They returned
graph-only FVS algorithms and generic box-QP material, but no closer
continuous global-optimization result. This search boundary is not a
completeness claim.

The existing [geometric-grid prior audit](geometric-grid-prior.md) remains
the right comparison for the earlier mixed-box shared-grid theorem, adaptive
continuous graphical-model discretization, and global lower-bound
certificates. This report focuses on the strengthened exact rational
continuous-QP FPT formulation and its forest/FVS parameterizations.
