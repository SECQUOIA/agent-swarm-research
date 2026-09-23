import Formal.NetworkSimplex.ThresholdCircuitReduction
import Formal.NetworkSimplex.ThresholdFarkas

/-! The exact positive-circuit criterion, with no prior polyhedral assumptions. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- Every normalized positive circuit is a necessary and sufficient family of tests. -/
theorem feasible_iff_positiveCircuits {I : Type*} [Finite I]
    (A : I → (Fin m → ℝ)) (b : I → ℝ) :
    (∃ x : Fin m → ℝ, ∀ i, ∑ j, A i j * x j ≤ b i) ↔
      ∀ C : PositiveCircuit A, 0 ≤ ∑ k, C.mass k * b (C.index k) := by
  let : Fintype I := Fintype.ofFinite I
  rw [NetworkSimplex.Threshold.farkas_inequalities]
  constructor
  · intro h C
    have hc : ∀ j, ∑ i, C.weights i * A i j = 0 := by
      intro j
      have he := congrFun C.weights_cancel j
      simpa only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] using he
    simpa only [C.weights_objective] using h C.weights C.weights_nonneg hc
  · intro h u hu hc
    by_contra hn
    have hvec : ∑ i, u i • A i = 0 := by
      ext j
      simpa only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] using hc j
    obtain ⟨C, hneg⟩ := exists_negative_positiveCircuit A b u hu hvec (lt_of_not_ge hn)
    exact (not_lt_of_ge (h C)) hneg

end NetworkSimplex.Chain.Threshold
