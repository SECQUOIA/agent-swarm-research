import Formal.NetworkSimplex.ThreeState

/-! The sixteen positive dependencies giving the three-state feasibility tests. -/

namespace NetworkSimplex
namespace ThreeStateCircuits

/-- Positive singleton, pair, and full normals; then negative singleton and full normals. -/
def normal : Fin 11 → Fin 3 → ℤ :=
  ![![1, 0, 0], ![0, 1, 0], ![0, 0, 1], ![1, 1, 0], ![1, 0, 1],
    ![0, 1, 1], ![1, 1, 1], ![-1, 0, 0], ![0, -1, 0], ![0, 0, -1], ![-1, -1, -1]]

/-- Seven subset dependencies, five partitions, three overlaps, and one half-cover. -/
def weight : Fin 16 → Fin 11 → ℤ :=
  ![![1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ![0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    ![0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    ![0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    ![0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    ![0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    ![0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    ![1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    ![0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    ![0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    ![1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    ![0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1],
    ![0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    ![0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    ![0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2]]

theorem weight_nonnegative : ∀ c i, 0 ≤ weight c i := by decide +kernel

theorem weight_nonzero : ∀ c, ∃ i, weight c i ≠ 0 := by decide +kernel

theorem normal_cancellation : ∀ c j, ∑ i, weight c i * normal i j = 0 := by
  decide +kernel

/-- No row is duplicated in the library. -/
theorem weight_injective : Function.Injective weight := by decide +kernel

private def pivot : Fin 16 → Fin 11 :=
  ![0, 1, 2, 3, 4, 5, 6, 6, 0, 1, 2, 0, 3, 3, 4, 3]

set_option maxHeartbeats 2000000 in
-- Expanding the sixteen supports requires 176 scalar coordinate checks.
/-- Every dependence on a listed support is a scalar multiple of the listed row. -/
theorem dependence_on_support (c : Fin 16) (a : Fin 11 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0) :
    a = fun i => a (pivot c) * (weight c i : ℝ) := by
  fin_cases c <;>
    (simp only [Fin.forall_fin_succ] at hs hc
     simp [weight, normal, Fin.sum_univ_succ] at hs hc
     ext i
     fin_cases i <;> simp [weight, pivot] <;> simp_all <;> linarith)

/-- Each nonzero dependence supported on a library entry uses its entire support.
Together with positivity and cancellation, this is support minimality. -/
theorem minimal_support (c : Fin 16) (a : Fin 11 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0)
    (ha : ∃ i, a i ≠ 0) : ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
  have heq := dependence_on_support c a hs hc
  have hp : a (pivot c) ≠ 0 := by
    intro hp
    obtain ⟨i, hi⟩ := ha
    have hi' := congrFun heq i
    rw [hp, zero_mul] at hi'
    exact hi hi'
  intro i
  have hi := congrFun heq i
  rw [hi, mul_ne_zero_iff]
  simp [hp]

def rhs (b : ThreeStateBounds) : Fin 11 → ℝ :=
  ![b.u1, b.u2, b.u3, b.u12, b.u13, b.u23, b.us, -b.l1, -b.l2, -b.l3, -b.ls]

def CircuitTests (b : ThreeStateBounds) : Prop :=
  ∀ c, 0 ≤ ∑ i, (weight c i : ℝ) * rhs b i

theorem circuit_tests_iff_sixteen_tests (b : ThreeStateBounds) :
    CircuitTests b ↔ b.SixteenTests := by
  constructor
  · intro h
    simp only [CircuitTests, weight, Matrix.cons_val', Matrix.cons_val_fin_one, rhs,
      Fin.sum_univ_succ, Fin.isValue, Matrix.cons_val_zero, Matrix.cons_val_succ, mul_neg,
      Finset.univ_unique, Fin.default_eq_zero, Finset.sum_neg_distrib, Finset.sum_const,
      Finset.card_singleton, one_smul, Fin.forall_fin_succ, Int.cast_one, one_mul,
      Int.cast_zero, zero_mul, neg_zero, add_zero, zero_add, le_add_neg_iff_add_le,
      Int.cast_ofNat, forall_const] at h
    rcases h with
      ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16⟩
    unfold ThreeStateBounds.SixteenTests
    and_intros <;> linarith
  · intro h
    rcases h with
      ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16⟩
    intro c
    fin_cases c <;> simp [weight, rhs, Fin.sum_univ_succ] <;> linarith

/-- Completeness holds for every real right-hand side, with no unlisted feasibility tests. -/
theorem circuit_tests_iff_feasible (b : ThreeStateBounds) :
    CircuitTests b ↔ ∃ x y z, b.Feasible x y z :=
  (circuit_tests_iff_sixteen_tests b).trans (b.sixteen_tests_iff_feasible)

end ThreeStateCircuits
end NetworkSimplex
