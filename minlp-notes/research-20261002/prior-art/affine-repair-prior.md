# Prior-art audit: affine repair and certified control decomposition

Date: 2026-10-02. This is a focused, read-only audit of the constrained
regridded-certificate result in
[`affine-repair-exploration.md`](../new-direction/affine-repair-exploration.md)
and its stable scalar-dynamics specialization. It is not a literature-KB
maintenance run or a priority clearance.

## Main assessment

There is strong prior art for the ingredients: global solution of multistage
nonconvex MINLPs by nested decomposition, Lagrangian and generalized-conjugacy
cuts, costate/adjoint multipliers for linear dynamics, and iterative
trajectory-centered dynamic programming. The candidate should not claim any
of those ideas by themselves. The closest control-specific global method is
Füllner and Rebennack's nonconvex nested Benders decomposition (NC-NBD): it
proves finite epsilon-globality for broad multistage nonconvex MINLPs and
explicitly uses dynamically refined state encodings and Lagrangian cuts.
Zhang and Sun likewise give global SDDP-style algorithms for multistage
stochastic MINLPs with generalized-conjugacy cuts and iteration bounds.

The narrower distinction worth testing is the certificate and its rate. Given
a supplied affine retraction that maps the whole domain box into the affine
feasible set, the candidate modifies bag-gradient slopes by equality
multipliers so that copy disagreement has no first-order cost after repair.
It then applies aggregate quadratic-growth contraction to a globally valid,
full-domain graded decomposition certificate. For scalar stable dynamics,
the repair and multiplier recurrences have horizon-uniform conditioning when
the stability margin is fixed. At fixed width, smoothness/growth ratios, and
repair conditioning, the result reports certificate size
`O(T log(T/eps))` and exact local convex-oracle calls
`O(T log^3(T/eps))` (with constants depending on those fixed parameters).
The cited prior algorithms establish broader global convergence, but their
papers do not give this same polylogarithmic-accuracy certificate count with
bounded-width exact convex local oracles and QG required only on feasible
trajectories. This is a focused comparison, not evidence of priority.

## Closest global decomposition methods

| Work | Verified result | Relation to the candidate |
|---|---|---|
| Füllner and Rebennack, [“Non-convex nested Benders decomposition”](https://doi.org/10.1007/s10107-021-01740-0), *Mathematical Programming* 196 (2022), 987–1024 | NC-NBD handles general multistage nonconvex MINLPs, continuous and integer states, nonlinear stage objectives and constraints. It combines MILP outer approximations, regularization, temporary dynamically refined binary state approximations, projected Lagrangian cuts, and nested Benders. Theorem 4.8(c) proves finite termination with an `eps`-optimal solution for `eps` above its approximation threshold, assuming each outer MILP can be solved globally in finite time. The paper's unit-commitment study includes nonconvex stage costs. [[fullner2022-non-convex-nested-benders-decomposition]] p.1-5, [[fullner2022-non-convex-nested-benders-decomposition]] p.22-26 | Strongest control-like global predecessor. It already establishes global finite-epsilon algorithms for nonconvex sequential models and already uses Lagrangian cuts and refinement. Its theorem is qualitative finite termination rather than a polynomial bound in horizon and `log(1/eps)`; the outer global MILP cost is not controlled. The authors also note that high binary precision can make subproblems very large. It does not use feasible-set QG plus a box-preserving affine retraction to prove a second-order copy-error bound. |
| Zhang and Sun, [“Stochastic dual dynamic programming for multistage stochastic mixed-integer nonlinear optimization”](https://doi.org/10.1007/s10107-022-01875-8), *Mathematical Programming* 196 (2022), 935–985 | Their nested, deterministic-sampling, and stochastic-sampling methods use exact-penalty value-function regularization and generalized-conjugacy cuts, with global lower/upper bounds and iteration complexity. Under bounded state dimension and Lipschitz/diameter parameters, Corollary 1 gives `T(1+2LDT/eps)^d`; finite-state and `T eps`-gap variants have linear-in-`T` bounds. Theorem 4 supplies a matching state-visit lower-bound mechanism for the deterministic method. [[zhang2022-stochastic-dual-dynamic-programming-for]] p.6-19, [[zhang2022-stochastic-dual-dynamic-programming-for]] p.20-24 | Establishes that global decomposition and complexity analysis for nonconvex multistage models are mature. The continuous-state accuracy dependence is polynomial in `1/eps` to a state-dimension power, and it assumes exact subproblem/dual oracles. The method does not give the candidate's feasible-QG contraction or a fixed-width polylogarithmic certificate count. |
| Robertson, Cheng, and Scott, [“On the convergence order of value function relaxations used in decomposition-based global optimization of nonconvex stochastic programs”](https://doi.org/10.1007/s10898-024-01458-1), *Journal of Global Optimization* 91(4) (2025), 701–742 | Their Li–Grossmann value-function relaxation uses Lagrangian cuts obtained by dualizing nonanticipativity constraints. In Pengfei Cheng's open dissertation, which contains the full theorem development corresponding to the paper, Theorem 6 gives order `beta<1` generally, order `1` under locally Lipschitz scenario value functions, and order `2` when the functions are real-valued and smooth on the full first-stage box; Corollary 6 gives a local smooth-region version. | Directly establishes that multiplier-corrected value-function cuts and second-order convergence orders are prior art. The second-order guarantee assumes smooth projected value functions, whereas the candidate's cancellation is derived directly from a supplied affine retraction and does not require scenario/subtree value functions to be smooth. The method is spatial branch-and-bound and does not supply the candidate's low-treewidth oracle-count bound. |

The open theorem source for Robertson–Cheng–Scott is Pengfei Cheng,
[*Advanced Optimization in Nonconvex Stochastic Programming and Integrated
Carbon Capture Systems*](https://hdl.handle.net/1853/75710), Georgia Tech
dissertation (2024), Chapter 2, especially Theorem 6 and Corollary 6. The
published paper is the preferred citation; the dissertation gives the
accessible primary text needed to verify the theorem. The article is not in
the local KB and should be routed to its sole writer, along with the
dissertation as its full-text source.

## Control and constraint terminology

For the scalar dynamics `s_(t+1)=a s_t+b u_t`, the transpose of the linear
part of forward simulation maps an ambient objective gradient to its
feasible-direction component. Solving for the equality multipliers that
produce this projected gradient is the standard discrete-adjoint/costate
calculation. The backward recurrence in the project note is therefore a
computational realization of familiar adjoint algebra; the candidate's
claim should concern how those multipliers enter a decomposition certificate
and cancel copy drift, not their derivation.

Heidari et al.'s original DDDP method
([1971 paper](https://doi.org/10.1029/WR007i002p00273)) is an early
trajectory-centered control algorithm. It applies Bellman recursion only in
a neighborhood of a trial trajectory and recenters on the locally improved
trajectory. Luus's systematic grid-reduction method
([1990 paper](https://doi.org/10.1080/00207179008934113)) is also a coarse-to-
fine DP predecessor. Both are relevant to iterative grid refinement, but the
reviewed source does not provide the candidate's globally valid lower
certificate or QG-conditioned polylogarithmic complexity; DDDP is explicitly
local. Munos and Moore's variable-resolution DP is another adaptive-grid
precedent, aimed at value/policy approximation rather than this static
treewidth certificate. These control comparisons are discussed with source
details in the [tree-sensitivity audit](tree-sensitivity-audit.md).

The project obstruction in
[`constraint-obstruction.md`](../new-direction/constraint-obstruction.md)
also narrows the claim. A Hoffman error bound or a Lipschitz feasible-repair
map controls distance but does not cancel the normal component of the
objective gradient: the two-bag example has fixed curvature, QG, and repair
constant while objective-only slopes leave a first-order gap. Lagrangian
normal corrections are established prior art; the sufficient condition used
here is more specific—a single known affine retraction valid throughout the
box, with local equality factors that cancel against its repaired point.
Kannan and Barton's constrained cluster analysis already relates the order of
lower bounds to growth on the feasible set, including second-order behavior
under quadratic growth. That result is about global branch-and-bound cluster
rates, not a constructive tree-decomposition DP with the present certificate
and operation counts. See [their 2017 article](https://doi.org/10.1007/s10898-017-0531-z),
especially [[kannan2017-the-cluster-problem-in-constrained]] p.21-22, and the
existing package `literature/papers/kannan2017-the-cluster-problem-in-constrained/`.

## Scope of the candidate rate

The stable-dynamics specialization uses path bags `{s_t,u_t,s_(t+1)}`,
treewidth two, and variable occurrence at most two. Its affine repair leaves
`s_0` and the controls fixed and simulates the states forward. The project
note proves
`||K|| <= 1/(1-|a|)` and a corresponding horizon-independent multiplier
bound when `1-|a|` is bounded below. The box is preserved under
`|a|+|b|<=1`. Thus fixed stability margin, `M/g`, relaxation error relative
to growth, and other displayed conditioning parameters make the grading ratio
constant; with `J=O(log(T/eps))`, the displayed certificate and oracle counts
are polynomial in `T` and logarithmic in accuracy. A concrete nonconvex
quartic stage objective satisfies the required global QG assumption in the
project note, so this is not limited to convex control costs.

Keeping each dynamics equation in its path bag also preserves the small local
scopes. Eliminating states can substitute long affine combinations of earlier
controls into later factors and make the reduced objective dense; the
certificate instead solves local convex problems with the dynamics equality
still present.

These are exact-oracle counts, not bit-complexity or wall-clock bounds. Each
local oracle is an equality-constrained convex problem after the supplied
factor relaxation; global retraction and gradients are also required. The
uniform complexity depends on a fixed stability margin and uniform
conditioning, and the theorem does not cover a general polyhedral feasible
set, inequality constraints, arbitrary nonlinear dynamics, or a retraction
that changes affine pieces across the box. The finite-control extension
replicates local leaves by the alphabet size and needs a uniform QG bound over
mixed feasible points. Those qualifications should accompany any comparison
with broader multistage MINLP results.

## Source routing and search limit

Send these two missing records to the sole literature-KB writer:

1. Robertson, Dillard; Cheng, Pengfei; Scott, Joseph K. (2025), DOI
   `10.1007/s10898-024-01458-1`, official [Springer landing
   page](https://link.springer.com/article/10.1007/s10898-024-01458-1). It is the
   closest published prior on Lagrangian value-function cuts and their
   convergence order; the article full text is paywalled.
2. Cheng, Pengfei (2024), Georgia Tech dissertation, handle `1853/75710`,
   [official repository record](https://repository.gatech.edu/entities/publication/93078490-2bc0-4fd5-a5d3-0ae1938c02ff),
   [official open PDF bitstream](https://repository.gatech.edu/server/api/core/bitstreams/cffb2fae-7cba-4f0e-8bd9-473948eba737/content).
   Chapter 2 contains the full primary theorem statements corresponding to
   the joint article and is the lawful full-text source for verification.

The scan also checked the project packages for NC-NBD, Zhang–Sun, constrained
cluster analysis, DDDP, Luus, and variable-resolution DP. It was focused on
global decomposition, Lagrangian/costate correction, stable finite-horizon
control, and certified accuracy dependence; it was not an exhaustive search
of optimal-control or mathematical-programming literature. No inference of
novelty should be made from sources not found in this scope.
