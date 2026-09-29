# Lean coverage for the quadratic penalty examples

Date: 2026-09-25. Source: [PenaltyEncoding.lean](PenaltyEncoding.lean).
The main mathematical note is
[parametric-exploration.md](../parametric-exploration.md).

The targeted Lean check succeeds for both the one-binary main construction
and its two-binary symmetric companion. It proves their augmented dual
values using literal real infima and suprema, including optimization over
every real multiplier. The proof starts from the quadratic-chain and native
constraints; it does not assume a residual separation parameter in place of
the construction.

## Mathematical correspondence

The Lean index `k : Nat` corresponds to the paper's `n = k + 1`.
`delta 0 = 1/4` and `delta (k+1) = (delta k)^2`.
`delta_closed` identifies this sequence with
`(1/2)^(2^(k+1))`, and `sequence_lower` proves its coordinatewise lower
bound for any nonnegative chain satisfying the source inequalities.

`OneFeasible` uses the precise main-model constraints: the chain bounds,
`q = 0` or `q = 1`, `-1 ≤ y ≤ 1`, and
`a k - 2 * (1 - q) ≤ y`. `Feasible` uses the symmetric model's extra
binary `b` and its two source linking inequalities. The real variables `q`
and `b` obey explicit binary disjunctions; no continuous relaxation replaces
them in the proofs.

There is one representational difference: Lean stores `a` as a sequence
`Nat → Real` and only uses its finite prefix `0, ..., k`. Restricting a Lean
point to that prefix gives a point of the paper's finite model. Extending
any finite vector arbitrarily after coordinate `k` gives a Lean point with
the same constraints and objective. Thus the two representations have the
same objective-value sets. This elementary restriction/extension statement
is a human correspondence check, not a separate Lean theorem. In
particular, the full sequence representation is not itself a compact set;
the formal dual proof does not rely on compactness.

## Results checked

| Source theorem or construction | Lean declaration(s) |
| --- | --- |
| Chain bound, attaining chain, and closed-form separation | `sequence_lower`, `delta_pos`, `delta_le_one`, `delta_closed` |
| Actual feasible zero and positive/negative witnesses | `zero_feasible`, `plus_feasible`, `minus_feasible`; `one_zero_feasible`, `one_plus_feasible`, `one_minus_feasible` |
| Every original feasible point has objective zero | `primal_objective`, `one_primal_objective`, together with the feasible zero witnesses |
| Symmetric residual lower bound | `residual_lower` |
| Symmetric dual value `min 0 (-1 + rho * delta k)` | `dual_eq` |
| Symmetric zero-gap threshold and its double-exponential value | `exact_threshold`, `reciprocal_delta` |
| One-binary residual lower bound | `one_residual_lower` |
| Two actual endpoints cancel any multiplier in their weighted objective sum | `one_weighted_identity`, `one_multiplier_witness` |
| An explicit multiplier attains the one-binary dual bound | `one_multiplier_lower`, `one_inner_at_multiplier` |
| One-binary dual value `min 0 ((2*rho*delta k - 1)/(1 + delta k))` | `one_dual_eq` |
| One-binary zero-gap threshold `1/(2*delta k)` and value `2^(2^(k+1))/2` | `one_exact_threshold`, `one_threshold_size` |

Both dual theorems require `rho ≥ 0`. Each inner objective-value set is
explicitly proved nonempty and bounded below. The set of inner dual values
is explicitly bounded above before `sSup` is used. Consequently the
infimum/supremum statements do not exploit the default values of real
conditional infima or suprema on empty or unbounded sets.

The one-binary lower proof uses
`oneMultiplier k rho = (1 + rho * (1 - delta k))/(1 + delta k)`
for every `rho ≥ 0`. This multiplier works above the threshold as well as
below it. The paper's piecewise choice of an optimal multiplier gives the
same value.

The threshold theorems establish equality of the augmented dual bound with
the original optimum. They do not assert that every penalized minimizer is
feasible at the threshold; that assertion would be false.

## Scope and limitations

Lean checks the stated analytic identities and inequalities from the
explicit native constraints. It does not check the literature comparison,
originality, application significance, polynomial model-encoding size,
binary-digit count, finite-dimensional convexity or compactness, Slater
claims, approximate-gap consequences, or solution-set exactness claims.
Those require the separate arguments and reviews in the research note.

The primal optimum is certified by a zero-valued feasible point and a
theorem saying that all original feasible points have objective zero; a
separate symbol for the primal infimum is unnecessary. The closed-form
one-binary threshold is expressed as `2^(2^(k+1))/2`; its rewriting as
`2^(2^(k+1)-1)` and the associated integer digit count remain ordinary
arithmetic in the paper.

The `#print axioms` commands for nine core theorems report only the
standard Lean/mathlib axioms `propext`, `Classical.choice`, and
`Quot.sound`. The source has no `sorry`, `admit`, custom axioms, or
unchecked native-computation proof steps. Successful compilation is
evidence for the formal statements, not a substitute for checking their
correspondence with the intended mathematical claim.

## Verification record

Only the following targeted command was run, from
`paper-certified-minlp/formal`, using that existing project's pinned
Lean/mathlib version `v4.33.1`:

```sh
lake env lean ../../research-20260925/formal/PenaltyEncoding.lean
```

The final run completed with exit code 0, no warnings, and the nine standard
axiom reports recorded in [penalty-encoding-lean.log](penalty-encoding-lean.log).
Earlier development runs exposed local rewrite and tactic mistakes, which
were corrected before the successful run. No project-wide build, tests,
or CI checks were run. The existing formal project's configuration and
library sources were not changed.

An independent source and statement review is recorded in
[penalty-lean-review.md](penalty-lean-review.md).
