# Fixed-preconditioner minimax bound

This development verifies the fixed-preconditioner theorem in
[`paper/sections/12-preconditioning.tex`](../paper/sections/12-preconditioning.tex),
including its actual matrices, spectral condition numbers, arbitrary
invertible congruence factors, and the matching order achieved by the identity.

## Result and manuscript improvement

Let `B` be the grounded lower-bidiagonal path incidence matrix, with diagonal
entries one and subdiagonal entries minus one. Put `C = B Bᵀ` and
`R = diag(1, −1, 1, −1, …)`. For every positive dimension `m` and every
invertible real matrix `P`, the verified theorem is

```text
max{κ(Pᵀ C P), κ(Pᵀ R C R P)} ≥ (4m² − 1)/3 ≥ m².
```

The SPD-preconditioner statement uses the actual positive inverse square
root `P = M⁻¹ᐟ²`. No sparsity or diagonal restriction is imposed on `M` or `P`.
One common factor must serve both inputs; an input-dependent choice of
different factors is not covered by the lower bound.

The original manuscript's `m²/4` bound for `m ≥ 4` was valid. The exact ramp
calculation strengthens its constant and extends the result to every `m ≥ 1`:

```text
r = (m, m−1, …, 1)
rᵀ C r = m
rᵀ R C R r = m(4m²−1)/3.
```

The reciprocal witness is `Rr`. Pulling both witnesses back through `P⁻¹`
proves the result for arbitrary invertible congruences directly, without
needing a polar-decomposition theorem. The previous bound is retained as
a Lean corollary.

The identity upper bound follows from the finite quadratic inequalities

```text
‖x‖₂² ≤ m² xᵀ C x,       xᵀ C x ≤ 4 ‖x‖₂².
```

The upper bound holds for every assignment of edge signs, not just the two
lower-bound inputs. Explicit orthogonal switching proves equality of all
their condition numbers. These results establish the matching quadratic
order. The lower constant is a witness bound, not a claim to compute the
exact minimax value.

## Representation and proof obligations

- `spectralCondition` is the largest actual eigenvalue divided by the
  smallest actual eigenvalue of a real symmetric matrix. Matrix-vector
  energies are connected to those eigenvalues by Mathlib's spectral theorem.
- Vectors are finite real coordinate functions; `euclideanSq` is their sum
  of squares. No default supremum norm on function spaces is used as the
  Euclidean norm.
- `pathMatrix` is defined as the product of the actual incidence matrix and
  its transpose. Its positive definiteness is proved from the incidence
  determinant, rather than assumed from an abstract energy formula.
- The alternating conjugate is identified with the normal matrix of the
  all-negative edge signing. Thus both lower-bound inputs are legal path
  inputs.
- `inverseSqrt` is the inverse of `CFC.sqrt M`. Its symmetry, positivity,
  invertibility, square, and whitening identity are proved for the stated
  SPD input.
- The spectral statements require a nonempty coordinate space. The path
  theorem uses `NeZero m`, equivalent to positive dimension; zero-dimensional
  matrices are not assigned a meaningful SPD condition ratio.

## Claim map

| Module | Claims |
|---|---|
| `Preconditioner/Path.lean` | Actual path matrices, positive definiteness, exact ramp energies, alternating involution, legal negative signing. |
| `Preconditioner/PathBounds.lean` | Finite telescoping and Cauchy–Schwarz bounds for the grounded path. |
| `Preconditioner/Sign.lean` | Every legal edge signing is an orthogonal diagonal switching, via explicit cumulative sign products. |
| `Preconditioner/Spectral.lean` | Actual eigenvalue extrema, quadratic bounds, reciprocal-witness minimax theorem, arbitrary congruences, orthogonal invariance. |
| `Preconditioner/Congruence.lean` | The actual positive inverse square root and SPD-preconditioning identities. |
| `Preconditioner/Simultaneous.lean` | `simultaneous_preconditioning`, exactly the manuscript's general condition-number product inequality. |
| `Preconditioner/WitnessRatio.lean` | `generalized_condition_ge_sq`, the relative condition lower bound from reciprocal witnesses. |
| `Preconditioner/Paper.lean` | `path_congruence_minimax`, `path_spd_minimax`, `path_spd_original_bound`, `path_relative_condition_lower`, `path_condition_bounds`, `edgePath_condition_eq`, and `all_signed_paths_identity_bound`. |

In particular, `path_condition_bounds` proves
`(4m²−1)/3 ≤ κ(C) ≤ 4m²`; `rampRatio_ge_sq` gives the simpler lower
bound `m²`. `path_relative_condition_lower` verifies the intermediate
inequality `κ(C⁻¹ᐟ² R C R C⁻¹ᐟ²) ≥ ((4m²−1)/3)²`.

## Scope

This is a finite-dimensional conditioning theorem. It does not verify the
later claims about data-dependent factors, transformed right-hand-side
preparation, parity query complexity, amortization, or the full LP Newton
construction. Those results have separate access and output assumptions.

The related supporting note is
[`2026-09-02-parity-preconditioner-dichotomy.md`](../research-archive/2026-09-research-cycle/supporting-results/2026-09-02-parity-preconditioner-dichotomy.md).
Its fixed-preconditioner theorem is updated to the stronger bound. The other
three standalone manuscripts do not state this theorem and require no changes
for this result.

## Reproduction

From `formal/`:

```sh
env PATH="$HOME/.elan/bin:$PATH" lake build
./scripts/verify.sh
```

The [verification contract](README.md#verification-contract) permits only
`propext`, `Classical.choice`, and `Quot.sound`. The audit rejects project
axioms, `sorryAx`, and native evaluation dependencies. The optional
`./scripts/verify.sh --replay` also rechecks the full import closure in a
fresh Lean kernel environment.

## Validation

The integrated build and axiom audit passed on 2026-09-20 for all 2701
project declarations, including 152 declarations added by these eight modules.
All new modules build without warnings. Independent review checked the
mathematical statements, assumptions, signed-input realization, spectral
correspondence, and manuscript scope and found no outstanding issues.
The main paper was rebuilt with LaTeX; pages 135–136, containing Theorem 12.6,
its proof, and the verification scope, were rendered and visually checked.
The optional fresh-environment kernel replay was not run.
