import Mathlib

/-! Squarefree polynomial semantics and the elementary envelope inequalities. -/

namespace CubicGap

noncomputable section

def monomial {ι : Type*} (s : Finset ι) (x : ι → ℝ) : ℝ := ∏ i ∈ s, x i

def supportPolynomial {ι : Type*} (supports : Finset (Finset ι))
    (coefficient : Finset ι → ℝ) (x : ι → ℝ) : ℝ :=
  ∑ s ∈ supports, coefficient s * monomial s x

theorem monomial_coordinate_affine {ι : Type*} [DecidableEq ι]
    (s : Finset ι) (x : ι → ℝ) (i : ι) (t : ℝ) :
    monomial s (Function.update x i t) =
      (1-t) * monomial s (Function.update x i 0) +
      t * monomial s (Function.update x i 1) := by
  unfold monomial
  by_cases h : i ∈ s
  · simp only [Finset.prod_update_of_mem h]
    ring
  · simp only [Finset.prod_update_of_notMem h]
    ring

theorem supportPolynomial_coordinate_affine {ι : Type*} [DecidableEq ι]
    (supports : Finset (Finset ι)) (coefficient : Finset ι → ℝ)
    (x : ι → ℝ) (i : ι) (t : ℝ) :
    supportPolynomial supports coefficient (Function.update x i t) =
      (1-t) * supportPolynomial supports coefficient (Function.update x i 0) +
      t * supportPolynomial supports coefficient (Function.update x i 1) := by
  simp only [supportPolynomial, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  rw [monomial_coordinate_affine]
  ring

theorem monomial_nonneg {ι : Type*} (s : Finset ι) {x : ι → ℝ}
    (hx : ∀ i ∈ s, 0 ≤ x i) : 0 ≤ monomial s x :=
  Finset.prod_nonneg hx

theorem monomial_le_coordinate {ι : Type*}
    (s : Finset ι) {x : ι → ℝ} (hx : ∀ i ∈ s, 0 ≤ x i ∧ x i ≤ 1)
    {i : ι} (hi : i ∈ s) : monomial s x ≤ x i := by
  classical
  unfold monomial
  rw [← Finset.mul_prod_erase s x hi]
  apply mul_le_of_le_one_right (hx i hi).1
  exact Finset.prod_le_one (fun j hj => (hx j (Finset.mem_of_mem_erase hj)).1)
    (fun j hj => (hx j (Finset.mem_of_mem_erase hj)).2)

theorem monomial_lower {ι : Type*} (s : Finset ι) {x : ι → ℝ}
    (hx : ∀ i ∈ s, 0 ≤ x i ∧ x i ≤ 1) :
    (∑ i ∈ s, x i) - (s.card - 1 : ℝ) ≤ monomial s x := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [monomial]
  | @insert a s ha ih =>
    have ha' := hx a (Finset.mem_insert_self a s)
    have hs : ∀ i ∈ s, 0 ≤ x i ∧ x i ≤ 1 :=
      fun i hi => hx i (Finset.mem_insert_of_mem hi)
    have hp := Finset.prod_le_one (fun i hi => (hs i hi).1)
      (fun i hi => (hs i hi).2)
    have hn := mul_nonneg (sub_nonneg.mpr ha'.2) (sub_nonneg.mpr hp)
    have hb := ih hs
    simp only [monomial, Finset.sum_insert ha, Finset.card_insert_of_notMem ha,
      Nat.cast_add, Nat.cast_one, Finset.prod_insert ha] at *
    nlinarith

theorem supportPolynomial_nonneg {ι : Type*}
    (supports : Finset (Finset ι)) (coefficient : Finset ι → ℝ)
    (hc : ∀ s ∈ supports, 0 ≤ coefficient s) {x : ι → ℝ}
    (hx : ∀ i, 0 ≤ x i) : 0 ≤ supportPolynomial supports coefficient x := by
  exact Finset.sum_nonneg fun s hs => mul_nonneg (hc s hs)
    (monomial_nonneg s fun i _ => hx i)

end
end CubicGap
