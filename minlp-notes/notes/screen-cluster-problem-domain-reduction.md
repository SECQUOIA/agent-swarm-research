# Screen: cluster problem, convergence order, and domain reduction (2026-09-21)

Two read-only screening agents summarized the state of the convergence-order
theory of spatial branch-and-bound (Kannan–Barton, J. Global Optim. 69 (2017)
and 71 (2018), open-access full texts on VTechWorks) to decide whether a
theorem on bound tightening is within reach. Kept as a candidate direction;
nothing here is a result.

## What is proven

- Unconstrained cluster problem (Du–Kearfott 1994; Wechsung–Schaber–Barton
  2014): with relaxations of convergence order `beta` and a nondegenerate
  minimizer, the number of boxes of width `(eps/tau)^(1/beta)` needed to cover
  the `eps`-suboptimal set scales as `eps^(n(1/2 - 1/beta))`: first order clusters,
  second order does not.
- Constrained (KB 2017): if the objective grows linearly along feasible
  directions at `x*` (nontrivial only when some inequality is active and the
  critical cone is trivial), first order with a small enough prefactor already
  avoids clustering; at KKT points with only equalities active, second order is
  required (Proposition 2, Theorem 3). No lower bounds on node counts exist in
  this literature.
- Schemes (KB 2018): Definition 14 defines the convergence order of a lower
  bounding scheme for all boxes containing the point. Theorem 1: full-space
  convex relaxation schemes are first order. Theorem 2: second order at a
  feasible point if the relaxations are second-order pointwise convergent and
  the relaxed argmin is within `O(w(Z)^2)` of `F(Z)` (condition (3)). Corollary
  2/3: Slater points. Theorem 5 and Corollary 4: second order at an *interior
  KKT point* via the Lagrangian dual with fixed multipliers (pointwise; the
  proof uses `grad L = 0` at that point). Reduced-space (Epperly–Pistikopoulos,
  Dür–Horst) schemes: first order in general (Theorem 9), second order only for
  separable data or vanishing cross-Hessian (Theorem 10).
- Domain reduction enters KB 2018 only as a set `X(Z)` with
  `X ⊇ X(Z) ⊇ F_X(Z)`; no theorem has a quantitative hypothesis on it. Examples
  16–18 show by example that constraint propagation turns a first-order
  reduced-space scheme into a second-order one; after Example 6 the paper notes
  that FBBT does not raise the order of the full-space example `-xy`, `x + y <= 1`.

## Open questions stated by Kannan–Barton (2018, Conclusion)

1. Whether full-space schemes achieve second order on a *neighborhood* of KKT
   constrained minima (needed by KB 2017 Theorem 3 to exclude clustering).
2. Sufficient conditions on the constraint-propagation scheme for second-order
   convergence of reduced-space schemes at regular constrained minima.

Kannan's MIT thesis (2018) could not be read (access wall); its abstract only
restates the papers.

## Candidate theorems (not developed)

- **Equality-determined case.** If the active equalities determine `x*(y)` with
  nonsingular Jacobian and the reduction map returns a box within `O(w(Z))` of
  the interval hull of `F_X(Z)`, then Theorems 3 and 5 applied on the reduced
  box give second order. Interval Newton supplies such a map. Low novelty
  (relabelled Corollary 4 plus Wechsung 2014).
- **Anchoring case (candidate, apparently new).** Inequality constraints,
  interior KKT point with LICQ and strict complementarity, active set of size
  `n_x`, objective pushing a coordinate `x_k` to the face `x_k = max_{F(Z)} x_k`.
  If the reduction map is first-order tight in coordinate `k` (the tightened
  upper bound exceeds the true maximum by `O(w(Z))`), the McCormick gap of every
  product involving `x_k` at the relaxed minimizer is `O(w(Z)^2)` because the
  McCormick underestimator is exact on the face; with an error bound for the
  active system this gives second order. Examples 17–18 of KB 2018 are
  instances. FBBT provides first-order tightness when a constraint is monotone
  in `x_k`; OBBT provides it whenever the constraint relaxations are first-order
  pointwise convergent (second-order constraint relaxations are not needed).
- **Mixed-order cluster count (candidate).** The Theorem 5 proof gives, at a
  feasible point `z` near the KKT point `z*`, a gap bound
  `tau_1 w(Z)^2 + tau_2 |z - z*| w(Z)`. Unfathomed boxes in KB 2017's count
  satisfy `|z - z*| = O(sqrt eps)` and `w(Z) ~ sqrt eps`, so the mixed term is
  `O(eps)`, the same order as the tolerance. Working this through would answer
  the practical form of open question 1 without proving neighborhood second
  order.

## Outcome (2026-09-22)

Developed in
[results/cluster-free-branch-and-bound-constrained-minima.md](../results/cluster-free-branch-and-bound-constrained-minima.md):
Theorem 1 (fixed-multiplier neighborhood bound), Theorem 2 (`eps`-independent
count), Theorem 3 (reduced-space schemes with width-tight domain reduction,
e.g. interval Newton on equality-determined variables). The anchoring mechanism
and the mixed-order count above are subsumed or superseded: the mixed bound
`c_1 dist^2 - c_2 w^2` is exactly what Theorem 1 proves. Not covered: second
order via anchoring without width control (Kannan–Barton Examples 17–18).
