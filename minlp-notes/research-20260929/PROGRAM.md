# Program: structure-exploiting spatial branch-and-bound

Date started: 2026-09-29. Status: closed on 2026-09-30 at the user's
request; results in [closing-research-results.md](closing-research-results.md).
This page is the original program definition, with corrections marked
inline.

## Question

Global MINLP solvers (SCIP, BARON, Gurobi, ANTIGONE, Couenne) run one
branch-and-bound (B&B) tree whose leaves are boxes in the full variable
space. Many important models are *sparse*: multi-period planning, networks,
discretized dynamics, trays of a column, chains of units. Their factor
(interaction) graphs have small treewidth `w` while the dimension `n` is
large.

Does single-tree spatial B&B pay a price exponential in `n` on such
problems, even when the global minimizer is unique and nondegenerate? Can a
decomposition-aware B&B (branching only on separator variables of a tree
decomposition, combining children through dynamic programming with
Lagrangian or affine child bounds) reduce the cost to `poly(n) * g(w, eps)`?
What is the right structural parameter, and what are matching lower bounds?

## Why it matters

If the separation is real and large, it identifies a missing solver
capability: decomposing the *search* (not only the relaxation) along a tree
decomposition of the factorable expression graph. Component branching in
MIP solvers (Gamrath et al.) handles only exactly decoupled components after
integer fixings; continuous separators are never fixed by spatial branching,
so components never appear.

## First evidence (2026-09-29, root)

`scratch/probe3.py`: minimize
`sum_i t_i + sum_i c_i x_i`, `x in [-1,1]^n`, with separate constraints
`t_i >= x_i^2 - 0.1 x_i^4 + 0.8 x_i x_{i+1}` (last term without the
product), `c_i ~ U(-0.3, 0.3)` (seeds 0, 1). Each constraint is nonconvex;
the sum is strictly convex near the origin (tridiagonal Hessian with
diagonal about 2 and off-diagonal 0.8) and nonconvex near the box corners,
which the root expected to give a unique interior nondegenerate global
minimizer. Interaction graph: a path (treewidth 1).

*Correction (computation study, `computation/scaling-study.md` §1.3):* the
uniqueness/interiority premise fails for some seeds from `n = 12` on and,
by the study's evidence, for all five seeds at `n = 1000` (eps-optimal
points with 2–27 coordinates at `±1`; the computation review proved
boundary optima for 9 instances). With the
linear coefficients scaled by 2/3, all 75 tested instances (`n` up to 1000)
have a certified unique, interior, nondegenerate minimizer while the
objective stays nonconvex on the box, and SCIP's growth on that family is
the same. SCIP 10 via PySCIPOpt 6.2.1, `absgap = 1e-4`,
`gap = 0`, 120 s limit, default settings otherwise:

| n | nodes (seed 0) | nodes (seed 1) |
|---|---|---|
| 2 | 1 | 11 |
| 4 | 217 | 351 |
| 6 | 1055 | 2941 |
| 8 | 4447 | 8991 |
| 10 | 28954 | 43762 |
| 12 | >92202 (time limit) | >201654 (time limit) |
| 16 | time limit, gap 0.24 | time limit, gap 0.24 |

The larger study (`computation/scaling-study.md`, 5 seeds, 300 CPU-s) gives
geometric-mean node counts 220–240, 1.5–1.8k, 7.1–7.8k and 29–37k at
`n = 4, 6, 8, 10` (about 5x per two variables) under every setting tried,
while a chain dynamic-programming B&B prototype with valid bounds solves
certified instances up to `n = 8192`.

Growth is roughly a factor 5 per two added variables (2–3 per variable).
*(Corrected 2026-09-30: an earlier version said "a factor 2–3 per two added
variables", which contradicts the table above.)* A dynamic program
along the path should need `O(n log(1/eps))` local work. This is
floating-point evidence from one solver version, not a proof.

*Correction (2026-09-29, from the Theory B note).* An earlier version of
this page said that the variant without the quartic term (convex sum,
`probe2.py`) "was solved at the root". That holds only up to `n = 5` in the
root's own probe (31 and 21 nodes at `n = 6`); the Theory B runs found 21–30
nodes at `n = 8`, 1271–5619 at `n = 12`, and more than 60 s at `n = 16`. The
effect therefore appears even when the summed objective is convex but is
written as separate nonconvex terms.

## Model (shared definitions)

- `F(x) = sum_{c in C} f_c(x_c)` on `X0 = prod_i [L_i, U_i]`, factors `c`
  are subsets of `[n]` of size at most `r`, factor hypergraph `H`.
- Factorable node relaxation on a box `B`: `F_B = sum_c f_{c,B_c}` where
  `f_{c,B_c} <= f_c` on `B_c` is a convex underestimator depending only on
  the projection `B_c` of `B`. Examples: per-factor alphaBB
  (`f_c - alpha_c q_{B_c}`), McCormick for bilinear factors, per-factor
  convex envelopes (the strongest factorable relaxation for a given
  factorization; the face-exact and decomposition reviews show that the
  lower bounds depend on how the objective is split into factors).
- Single-tree certificate: a partition of `X0` into boxes `C` with
  `min_C F_C >= f* - eps` (repo model: research-20260928b/bb-complexity/
  spatial-constrained/instance-dependent-node-complexity.md, Section 1).
- Decomposition certificate (to be formalized): a rooted tree decomposition
  `(T, {V_t})` of `H`; for each tree node `t` with separator
  `S_t = V_t ∩ V_parent`, a partition of the separator box into cells and,
  for each cell, a valid lower bound (constant or affine/convex minorant)
  on the subtree value function
  `phi_t(x_{S_t}) = min { sum of factors assigned to subtree(t) }`,
  certified by a local box B&B over the bag `V_t` that uses the children's
  minorants. Size = total number of local leaves.

## Existing repository results used

- Theorem 3.1 (integral lower bound) of the constrained note: every
  `alpha`-valid box family has
  `|P| >= (alpha n/pi^2)^{n/2} ∫ (m+eps)^{-n/2}`. With per-factor alphaBB,
  the gap is `sum_c alpha_c q_{B_c} >= alpha q_B` if every variable lies in
  a nonconvex factor. This gives an `exp(Omega(n))` single-tree lower bound
  only when `alpha` exceeds about `0.29` times the geometric mean of the
  Hessian eigenvalues at the minimizer (convention `m ≈ y'Hy/2`).
  *Correction:* an earlier version said it "already gives" such a bound on
  chains; on the probe family it gives base 0.78 (exact per-factor `alpha`)
  or 1.03 (root-box `alpha`), i.e. no useful growth (Theory B note,
  Section 6). McCormick and other face-exact relaxations are not covered by
  Theorem 3.1; Theory B proves a separate bound for them.
- Theorem 6.3: bisection and `N_opt` within `C log(1/eps)` of a multi-scale
  covering profile.
- Face-exact note: McCormick gaps vanish on faces whose fixed coordinates
  form a vertex cover of the bilinear graph.

## Workstreams

1. Literature and novelty audit (AND/OR search, nonserial DP, reduced-space
   and decomposition B&B, component branching, nested Benders with
   partitions, Bienstock–Muñoz, sparse SOS).
2. Theory A: decomposition-certificate model; instance-dependent upper
   bounds; worst-case `poly(n) (C/eps)^{O(w)}`; lower bounds in `w`;
   separation theorem.
3. Theory B: single-tree lower bounds for face-exact factorable relaxations
   (McCormick, per-factor envelopes) at isolated nondegenerate minimizers.
4. Computation: prototype decomposition-aware B&B on chains/trees versus
   SCIP; robustness of SCIP's growth to settings; application-like families.
