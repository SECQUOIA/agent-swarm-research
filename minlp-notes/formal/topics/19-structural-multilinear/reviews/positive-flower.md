# Independent review of the positive-box flower

Reviewed 2026-09-20 against W04 in [CLAIMS.md](../CLAIMS.md) and the fixed
positive bound-ratio sharpness argument in
[the treewidth-two source note](../../../../results/positive-multilinear-treewidth-two-exact.md).
The reviewer did not author or modify the reviewed proof file.

**Result: no mathematical or statement defect found. The analytic W04
obligations are proved for actual original physical factors. The incidence
graph assertions live in separate graph modules on the same scopes; they
are not hypotheses hidden in the analytic calculation.**

## Declaration coverage

All declarations below are in `MultilinearGap.StructuralPositiveFlower`
unless a different namespace is specified. Write `α = 1 - ε` and
`c_n = (1 - ε^n)/n`.

| Obligation | Declarations and review result |
|---|---|
| Actual physical polynomial | `physical_supportPolynomial` identifies the original supports and coefficients with `(1/α) a Σ_i x_i + ∏_i x_i`. `physical_split` separates its normalized nonlinear part from an explicit affine remainder. |
| Actual graph-hull width | `remainder_meanExact` and `physical_hullGap` prove that removing the affine remainder preserves the physical graph-hull gap. This is an envelope identity, not substitution of an auxiliary optimization value for the physical gap. |
| Feasible means | `means_strict`, `physicalMeans_strict`, and `scaledMeans_strict` prove strict interiority for every `n ≥ 2` and the stated nondegenerate boxes. `threshold_means` and the imported `singleFailLaw_means` establish the means of the attaining laws. |
| Leaf-factor endpoints | `leaf_minimum` proves lower endpoint `ε`; `leaf_maximum` proves upper endpoint `1-c_n`; both include actual attaining laws. `leaf_gap` gives `α-c_n`. |
| Exact original-term gap | `physical_pair_gap` gives the unweighted physical bilinear width `α²/n`. `physical_termwiseGap` includes each original coefficient `1/α` and proves `T_n = 2α-c_n`. |
| Exact attained payoff representation | `physical_payoff_maximum` proves `IsGreatest (payoffValues n ε) (H_n+c_n)`, with `payoff = α A R + 1-ε^R` over actual laws with every prescribed singleton mean. Thus the maximum is attained, and the admissible laws have not been relaxed to two scalar-moment constraints. |
| Truncation upper bound | `payoff_bound` proves a pointwise inequality for every real `M>0`; `hullGap_upper` takes expectations to obtain `H_n ≤ α + αM/n + 1/M-c_n`, slightly stronger than the source's displayed estimate. |
| Matching asymptotic lower bound | `hullGap_lower` supplies a concrete feasible law and proves `H_n ≥ α + α/n-c_n`. |
| Limits | `correction_tendsto`, `reduced_hullGap_tendsto`, `physical_hullGap_tendsto`, and `physical_termwiseGap_tendsto` give `c_n→0`, `H_n→α`, and `T_n→2α`. `physical_ratio_tendsto` gives ratio limit two. |
| Denominator positivity | `physical_hullGap_eventually_pos` and `scaled_hullGap_eventually_pos` explicitly establish eventually positive widths before the sharp uniform-constant consequence. |
| Fixed `[1,ρ]` box | `scaledCoefficient_pos`, `scaledPhysical_eq`, `scaled_boxPoint`, `scaled_hullGap`, and `scaled_termwiseGap` transfer the actual polynomial and each original term by `x↦x/ρ`, with `ε=1/ρ`. |
| Sharpness as a supremum | `scaled_ratio_tendsto` proves limit two for every fixed `ρ>1`; `scaled_universal_constant_ge_two` proves any uniform upper constant on this family is at least two. It does not claim a finite flower attains ratio two. |

## Mathematical checks

The factor family remains `StructuralSharpness.supports n`: one scope for
all leaves and one scope `{anchor, leaf i}` per leaf. The large leaf scope
contains no anchor, so it is distinct from every pair scope, including at
`n=2`; pair scopes are also distinct. The algebra never treats normalized
expansion terms as new factors.

The upper attaining law has three atoms: all bits zero; anchor zero and
all leaves one; all bits one. Their masses are `1/n`, `1-2/n`, and `1/n`.
All are nonnegative for `n≥2`, including the zero middle mass at `n=2`.
It attains the leaf upper endpoint and every pair upper endpoint
simultaneously. The lower leaf law has exactly one uniformly selected
failed leaf, hence `R=1` almost surely and expectation `ε`.

The leaf lower bound follows from the proved support line for `ε^r` and
`E R=1`; its upper bound follows from the proved chord on integer
`0≤r≤n`. The exact payoff identity uses the individual prescribed means
to show `E R=1` and `E A=1/n`, while retaining the full law in the
optimization domain. Compact graph-envelope attainment proves existence
of the maximizing payoff law.

The truncation proof splits pointwise at `R≤M`. On that event it bounds
`α A R` by `α A M` and `1-ε^R` by `α R`. On `R>M` it bounds the first
term by `α R` and the second by `1≤R/M`. Taking expectations gives the
needed uniform bound using only those two first moments. Setting
`M=√n` is valid eventually because `n≥2`; the proof checks positivity
and the square-root identity explicitly. Correction bounds
`0≤c_n≤1/n` complete the squeeze.

The lower-law implementation correlates the anchor with the identity of
the failed leaf, whereas the source describes an independent anchor.
This is valid: the constructed anchor has mean `1/n`, all leaf means are
correct, and `R=1` identically makes `E[AR]=E[A]` regardless of that
correlation. Both constructions give the same bound.

For fixed `ρ>1`, the scaled coefficient of support `s` is the original
positive coefficient divided by `ρ^s.card`. `scaledCoefficient_pos`
proves strict positivity, so every original scope remains active. The
monomial gap identity includes precisely the reciprocal scaling factor;
`scaled_termwiseGap` verifies the original termwise sum, separately from
the total graph-hull identity. No common scaling of differently sized
monomials is incorrectly assumed.

The formulas admit `ε=0` where stated, with the usual polynomial
convention `0^0=1`. Ratio limits require `ε<1`; for the fixed positive
box, `ε=1/ρ` lies strictly between zero and one. Values of the sequences
at `n=0,1` do not enter the limit or uniform-constant argument: all
finite formulas are applied on the eventual set `n≥2`.

## Graph membership and completion boundary

The analytic module does not import graph membership. It uses exactly the
same scopes as the following separate declarations:

- `StructuralTreewidth.flowerSupportGraph` is the incidence graph on
  the actual support subtype, with incidence `i ∈ s.val`.
- `StructuralTreewidth.flower_supports_treewidth_le_two` transfers an
  explicit width-two decomposition to those actual scopes.
- `StructuralSharpness.flower_supports_treewidth_exactly_two`, in
  `StructuralFeedbackFlowerGraph`, also rules out width one for `n≥2`.
- `StructuralSharpness.flower_feedback_acyclic` proves that deleting the
  anchor's incidence edges leaves an acyclic graph.

These graph statements are external to this analytic module, but are
present in the repository. Their scope definitions were inspected for
agreement; their full proofs and axiom closure were not independently
re-audited in this bounded review. Strictly positive scaled coefficients
show that scaling introduces no change to the active incidence graph.
No additional graph theorem specific to `[1,ρ]` is mathematically needed.

The matching upper bound two for all incidence-treewidth-two instances
belongs to W01–W03 and is outside this review. The positive-flower module
proves the required lower sharpness witness, not that universal upper
bound by itself. The unit-box flower portion of W04 is supplied separately
by the F06 declarations in `StructuralSharpness` and its graph module.

## Targeted verification

The following commands passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralPositiveFlower
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake --wfail build Formal.MultilinearGap.StructuralPositiveFlower
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-positive-flower-review.lean
```

Both builds reported success (8729 dependency jobs). The temporary audit
printed axioms for 16 declarations covering the physical polynomial,
physical gaps, attained payoff maximum, pointwise truncation, both
truncation bounds, limits, coefficient positivity, both scaling identities,
scaled ratio and eventual positivity, uniform-constant sharpness, and
strict scaled means. Every declaration listed only `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`.

An initial attempt placed `--wfail` on `lake env lean`; Lean rejected that
option before checking the file. The corrected `lake --wfail build`
command above passed. No project-wide verification or CI inspection was
performed, and no proof module was changed.

Reviewed SHA-256:

```text
189a5d61e9778fe9dda8a284a8675596e87382ff850587fbd4c886e512c23b6c  StructuralPositiveFlower.lean
```
