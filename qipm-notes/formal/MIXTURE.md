# Sparse convex mixtures and centrality

Source: the first two subsections of
[`paper/sections/10-gadget-frontiers.tex`](../paper/sections/10-gadget-frontiers.tex).
The development is in [`QipmFormal/Mixture/`](QipmFormal/Mixture/).

This report distinguishes the mathematical mixture topic from the other
results in the same section. The scope includes residual estimates,
decoder stability, centrality, soundness consequences, and explicit
counterexamples. It excludes the separate LP constructions establishing
sharpness of the resource orders, electrical frontiers, quantum query
lower bounds. The noncommutative SDP extension in Section 14 is now covered
by a separate [SDP verification report](SDP_MIXTURE.md) and development,
which reuse this topic's residual infrastructure.

## Representation and hypotheses

Vectors are functions on finite coordinate types. `sqNorm` is the sum of
coordinate squares and `euclideanNorm` is its square root; the proofs do
not use the function type's sup norm as a Euclidean norm. `mix` is the
actual coordinatewise finite weighted sum. `ProbWeights` requires
nonnegative weights summing to one.

Residual estimates start with base and neighboring matrices, exact
neighboring feasibility, coefficient bounds, witness height bounds, and
coefficient locality. They do not assume the residual bound being proved.
Decoder soundness is an explicit hypothesis about every candidate in the
named residual tube. It is not inferred from coefficient locality.

The relative tube is written without division as
`euclideanNorm (residual A z b) ≤ eta * euclideanNorm b`. It agrees with
the manuscript's ratio convention when `b` is nonzero. Nonnegative
thresholds are needed when passing between a norm and its square.
Divided resource frontiers require positive row sparsity. Positive
cardinality is explicit for uniform weights and point-centered means.

## Verified claim map

All names below are in `QipmFormal.Mixture`; counterexample names additionally
use `Counterexample`. These are theorem families, with supporting identities
in the same files. The development has 13 modules.

| Manuscript claim | File and declarations |
|---|---|
| Actual one-bit input update leaves other coefficients unchanged | [Augmentation.lean](QipmFormal/Mixture/Augmentation.lean): `oneBitMatrix_update_locality` |
| RHS augmentation, including height, support, incidence, and locality | `Augmentation.lean`: `rhs_residual`, `rhsWitness_height`, `rhsMatrix_sparsity`, `rhsDependent_incidence`, `rhsMatrix_locality`, `rhsWitness_mix` |
| Inequality/slack conversion with bounded slack coordinates | `Augmentation.lean`: `slack_conversion`, `slackWitness_height`, `slackMatrix_supportCount`, `slackMatrix_locality` |
| Weighted and uniform single-flip residuals | [Residual.lean](QipmFormal/Mixture/Residual.lean): `weighted_residual_bound`, `uniform_residual_bound`; `euclideanNorm_eq_norm_toLp` identifies the norm with actual Euclidean space |
| Sensitive subsets and zero-incidence bits | `Residual.lean`: `sensitive_residual_bound`, `zero_incidence_feasible` |
| Multibit bound and row-union specialization | [Multibit.lean](QipmFormal/Mixture/Multibit.lean): `multibit_residual_bound`, `multibit_row_union_bound` |
| Nonnegativity, height, objective, convex-domain preservation | [Decoder.lean](QipmFormal/Mixture/Decoder.lean): `mix_nonneg`, `mix_abs_le`, `mix_objective`, `mix_mem_convex` |
| Actual parity flips and affine wrong margins | `Decoder.lean`: `parity_flip`, `parity_is_sign`, `single_flip_affine_wrong`, `mix_signed_margin` |
| Disjoint pair decoder, normalization, and binary bias | `Decoder.lean`: `mixture_pair_decoder_bound`, `pair_expectation_normalized`, `pair_probability_fair_outside`, `pair_probability_valid`, `pair_probability_bias` |
| Half-base cancellation, objective, membership, and half residual | `Decoder.lean`: `half_base_mixture_map`, `half_base_objective`, `half_base_mem_convex`, `half_base_residual_norm` |
| Harmonic weights and their optimality | [Incidence.lean](QipmFormal/Mixture/Incidence.lean): `harmonicWeight_prob`, `harmonicWeight_cost`, `harmonicWeight_minimizes`, `harmonic_cost_le_uniform` |
| Harmonic residual and strict affine resource frontiers | [Frontier.lean](QipmFormal/Mixture/Frontier.lean): `harmonic_residual_bound`, `weighted_affine_soundness_frontier`, `uniform_affine_soundness_product`, `harmonic_affine_soundness_product` |
| Pair-decoder resource frontier | [PairFrontier.lean](QipmFormal/Mixture/PairFrontier.lean): `weighted_pair_soundness_frontier` |
| Literal nonnegative split KKT system, its sparsity and incidence factor three | [KKTStack.lean](QipmFormal/Mixture/KKTStack.lean): `kktWitness_nonnegative`, `kktWitness_height`, `kktMatrix_sparsity`, `kktDependent_incidence`, `kktMatrix_locality`, `kktMatrix_sqNorm`, `split_multiplier_mix_difference` |
| Actual weighted and uniform KKT residuals | [KKT.lean](QipmFormal/Mixture/KKT.lean): `weighted_kkt_bound`, `weighted_kkt_paper_bound`, `uniform_kkt_paper_bound` |
| Algebraic objective-gap preservation | `KKT.lean`: `mixture_objective_gap`, `central_objective_gap`, `central_mixture_objective_gap`; common primal and dual objective values are separately preserved by `mix_objective` |
| Weighted/uniform multiplicative variance and its equality case | [Centrality.lean](QipmFormal/Mixture/Centrality.lean): `weighted_multiplicative_variance`, `central_uniform_variance`, `multiplicativeDefect_nonneg`, `multiplicativeDefect_eq_zero_iff`, `uniform_multiplicativeDefect_eq_zero_iff` |
| Scalar Kantorovich and finite maximum/minimum ratios | `Centrality.lean`: `kantorovich_bound`, `kantorovich_extrema_ratio_bound`, `extrema_ratio_iff_pairwise`, `central_mixture_product_bounds`, `kantorovich_sub_one` |
| Exact point-centered width and its bound | `Centrality.lean`: `point_centered_defect_identity`, `point_centered_width_identity`, `point_centered_defect_bound` |
| Actual central triples, wrong outputs, and strict dichotomies | [Paper.lean](QipmFormal/Mixture/Paper.lean): `actual_mixture_variance`, `central_affine_soundness_dichotomy`, `central_pair_soundness_dichotomy`, `point_centered_affine_soundness_dichotomy`, `central_uniform_soundness_dichotomy` |
| Diagonal LP, exact means, residuals, and gaps | [Counterexample.lean](QipmFormal/Mixture/Counterexample.lean): `neighbor_central`, `uniform_primal`, `uniform_slack`, `actual_residualSquared_exact`, `algebraic_gap`, `inner_product` |
| Finite counterexample bounds and both neighborhood conventions | `Counterexample.lean`: `small_parameter_product_bounds`, `inverse_square_defect`, `inverse_square_residual`, `point_centered_width_zero`, `padded_quantitative_failure` |
| Counterexample coefficient, sparsity, locality, and incidence bounds | `Counterexample.lean`: `example_matrix_bounds`, `diagonal_row_support`, `diagonal_column_support`, `example_locality`, `padded_example_locality`, `example_incidence`, `padded_example_incidence`, `example_totalIncidence`, `padded_example_totalIncidence` |

`central_uniform_soundness_dichotomy` applies to either neighborhood contract
and any explicitly proved wrong-output predicate. The affine and pair
decoder theorems supply that predicate. The point-centered pair case also
follows from `point_centered_soundness_from_residual_bound` and
`mixture_pair_decoder_bound`; it does not require a separate quantum-state
construction. The statements about measurement concern finite real
normalized squared amplitudes and the displayed binary probabilities.

Sensitive-subset resource consequences follow by using the subtype of
selected bits. Exact finite inequalities, rather than separate declarations
in asymptotic notation, justify the resource-order and counterexample
asymptotic prose. In particular, a fixed relative-tube asymptotic lower
bound needs a positive radius and nonzero RHS. The finite inequalities
also cover a zero threshold.

## Stronger results obtained during formalization

The multibit estimate holds with
`d_coeff = max_(r,j) |I_rj|`, rather than the potentially larger maximum
number of distinct bits in a row. The proof applies Cauchy--Schwarz first
over coefficient positions, then over the bits for each position. The
manuscript now gives the stronger bound and its original row-union
consequence. For one bit per coefficient it recovers the one-bit constant.

Keeping dual multipliers signed gives the squared KKT residual bound

\[
4(s_r+s_c)B^2H^2\sum_i M_iw_i^2.
\]

This implies the manuscript's original `12 s_KKT B_KKT²` bound. The
literal nonnegative split construction and its incidence factor three are
also verified. Both common-parameter and point-centered soundness theorems
accept the sharper residual estimate through their general composition
theorems. The paper records this improvement.

## Corrections identified during formalization

The original uniform diagonal counterexample has identical complementarity
products in all coordinates. Its point-centered width is zero. It shows
instability around the neighbors' common parameter, which the manuscript
now states explicitly. At the infeasible average, its algebraic objective
gap and its complementarity sum differ.

Appending an unchanged public block gives a separate counterexample for
the point-centered convention. For `N ≥ 8` and `mu = 1/N²`, its actual
combined squared residual is at most `2/N`, while every coordinate has
point-centered relative deviation at least `1/3`. Thus it excludes any
fixed width below `1/3`; no stronger limiting-width claim is needed or
advertised. Both examples have one-bit coefficient locality, row and
column sparsity at most one, and exactly `N` dependent positions.

The exact claim that a binary decoder's bias is half the signed observable
expectation uses a fair random sign outside the selected coordinate pairs.
The manuscript now specifies that decoder.

The manuscript also makes the nonempty pair family, positive sparsity
for divided inequalities, and positive radius for fixed-tube asymptotic
conclusions explicit. These qualifications agree with the formal proofs.

## Scope boundary and review

The verified topic is the finite residual/decoder/centrality argument in
the current manuscript. It is not the whole Gadget-Class Frontiers section
or the whole QIPM paper. Historical arbitrary-weight counterexample
formulas and the multibit KKT extension retained in the archived supplement
are not imported as additional claims. The three other standalone
manuscripts do not state this topic's results and needed no changes.

Independent reviews checked the claim inventory, mathematical hypotheses,
norms, incidence counts, decoder composition, both neighborhood conventions,
counterexamples, and manuscript correspondence. They prompted the explicit
qualifications and completed composition theorems recorded above. No
unresolved mathematical issue remained in the reviewed scope.

## Reproduction

From `formal/`, in the repository's environment:

```sh
conda run -n qipm --no-capture-output bash scripts/verify.sh
```

The audit must cover all imported project declarations and admit only
`propext`, `Classical.choice`, and `Quot.sound`. No project axioms,
`sorry`, or `native_decide` dependencies are permitted.

## Validation on 2026-09-20

- The integrated build and axiom audit passed for **1089 project declarations**,
  including all 13 mixture modules and both existing formalization topics.
- The final Lean build emitted no warnings. The audit found only the three
  allowed standard axioms.
- Independent mathematical and correspondence reviews completed with no
  unresolved findings in this topic's scope.
- The main paper rebuilt to 196 pages; the final LaTeX log has no warnings,
  unresolved references or citations, or overfull/underfull boxes.
  The revised multibit and counterexample pages were rendered and visually checked.
- The optional fresh-environment replay of the entire Mathlib import closure
  was not run. The completed checks are the project build and declaration-level
  axiom audit, as specified in the repository's verification contract.
