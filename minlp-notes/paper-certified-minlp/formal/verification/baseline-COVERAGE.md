# Claim-to-theorem map

Every name below is in namespace `CertifiedMinlp`. Modules are imported by
`CertifiedMinlp.lean`; `Verify.lean` audits all owned declarations, rather than
only the selected public theorems below.

| Manuscript assertion | Declaration | Premises and exact scope |
|---|---|---|
| Table 2 finite interval enclosure | `bounded_shift_le` | Real endpoints and true residual; both points in interval; enclosing residual bounds. Proves the two-endpoint maximum upper bound. |
| Table 2 lower half-line enclosure | `lower_shift_le` | Both points above lower endpoint; nonnegative enclosing lower residual; residual enclosed. |
| Table 2 upper half-line enclosure | `upper_shift_le` | Both points below upper endpoint; nonpositive enclosing upper residual; residual enclosed. |
| Table 2 including free coordinates | `coordinate_correction_sound` | Rational endpoints/data, real residual and tested point; membership and `accepts`. Free enclosure `[0,0]` forces zero real residual. |
| Fixed-coordinate correction | `fixed_correction` | Exact equal rational endpoints and support coordinate. |
| Nonnegative correction | `correction_nonneg` | Support membership, accepted enclosing interval, actual enclosed residual. |
| Safe affine correction, finite sums | `safe_affine_of_shift_bounds` | General real support inequality, individual residual shift bounds, intercept bound. The conclusion is the resulting affine underestimator. |
| Corollary 3.3 rational enclosure test | `rational_enclosure_cut` | Arbitrary finite coordinate type, rational row/cut/enclosure data, real function/support slopes; valid support on box, enclosed residual, lower value enclosure and rational intercept test. Derives coordinate shift bounds using the table theorem, then sums. |
| Row-cut validity | `cut_valid_of_underestimator` | Underestimation and original row nonpositivity imply cut nonpositivity. |
| Objective-preserving transfer | `objective_preserving_transfer` | Feasible embedding, exact objective preservation, pointwise master lower bound. All three are explicit assumptions. |
| Master infeasibility implication | `infeasible_master_transfer` | Feasible embedding and empty master. Mathematical implication only; not a public-API infeasibility checker. |
| Epigraph graph inclusion | `epigraph_graph_feasible` | Original feasible set included in base constraints, cuts valid on the original epigraph. Constructs `(x,h(x))` and proves membership in the explicitly defined `epigraphMaster`. |
| Epigraph cut underestimation | `epigraph_cut_of_underestimator` | Underestimation of `h(x)-t` implies validity on its epigraph. |
| Epigraph lower bound | `epigraph_bound_transfer` | Base inclusion, epigraph-cut validity and master lower bound; uses the proved graph inclusion. |
| Objective signs | `signed_min_bound`, `signed_max_bound` | Lower bound on respectively `1*f` and `(-1)*f`; gives original lower and upper bounds. |
| Theorem 3.6 weak incumbent-cutoff lifting | `incumbent_cutoff_lifting` | Actual feasible incumbent and bound on every feasible point no worse than it. Derives bound at incumbent, then extends outside cutoff. Does not assume master optimum attainment or prove the VIPR invariant. |
| Pointwise primal gap | `primal_gap` | Actual feasible witness, globally valid lower bound, witness objective upper enclosure. |
| Matching witness optimality | `matching_primal_attains` | Feasible witness with objective at most the global lower bound. Proves equality and pointwise optimality. |
| Corollary 3.8 infimum and gap | `primal_infimum_bounds` | Feasible witness and finite lower/upper bounds establish nonempty, bounded-below objective image before using the real infimum. |

The theorem-number labels refer to the stage-3 manuscript and may change with
later editing; names and descriptive assertions are stable identifiers.

## Explicit exclusions

- The supremum equality and necessity of finite-correction sign conditions in
  Table 1. The formalized table inequalities suffice for accepted-cut safety.
- Deducing supporting inequalities from convexity or subgradients; expression
  domains; symbolic differentiation; curvature recognition; actual interval
  enclosure computation and rational endpoint conversion.
- Bound propagation, including integer rounding; exact parser/loader semantics;
  sparse variables; objective-constant serialization; LP/VIPR master matching.
- VIPR inference semantics, including assumption tracking, combination, rounding,
  unsplitting, and the inference invariant. Only the semantic cutoff-lifting
  argument after that invariant is formalized.
- Python or external executable correctness; any certificate bundle, benchmark
  count, primal-witness arithmetic, performance measurement or novelty claim.
- Extended-real infima of empty sets. Lower bounds are pointwise for all sets;
  real infima occur only with a feasible witness and a finite lower bound.

A proof of these implications does not establish that a particular executable
computed inputs satisfying their premises. Matching declarations to the paper
and trusting the stated Lean/mathlib dependency base remain explicit duties.
