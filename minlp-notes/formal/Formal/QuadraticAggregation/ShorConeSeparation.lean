import Formal.QuadraticAggregation.Recession
import Mathlib.Analysis.LocallyConvex.Separation
import Mathlib.Analysis.Convex.Topology
import Mathlib.LinearAlgebra.Pi
import Mathlib.Algebra.BigOperators.Field

open Set Finset

namespace QuadraticAggregation

/-- Separation from the strict negative orthant needs neither closedness nor an origin. -/
theorem exists_nonnegative_separator {m : ℕ} {C : Set (Fin m → ℝ)}
    (hC : Convex ℝ C) (hne : C.Nonempty)
    (hmiss : ∀ y ∈ C, ¬ ∀ i, y i < 0) :
    ∃ w : Fin m → ℝ, (∀ i, 0 ≤ w i) ∧ w ≠ 0 ∧
      ∀ y ∈ C, 0 ≤ ∑ i, w i * y i := by
  classical
  let N : Set (Fin m → ℝ) := {y | ∀ i, y i < 0}
  have hN : Convex ℝ N := by
    intro x hx y hy a b ha hb hab i
    exact (convex_Iio (0 : ℝ)) (hx i) (hy i) ha hb hab
  have hoN : IsOpen N := by
    simpa only [N, ← Set.ofPred_forall] using
      (isOpen_iInter_of_finite fun i : Fin m =>
        isOpen_lt (continuous_apply i) (continuous_const : Continuous fun _ : Fin m → ℝ => (0 : ℝ)))
  obtain ⟨f, u, hNf, hCf⟩ := geometric_hahn_banach_open hN hoN hC
    (Set.disjoint_left.mpr fun y hy hyC => hmiss y hyC hy)
  let w : Fin m → ℝ := fun i => f (Pi.single i 1)
  have hf (y : Fin m → ℝ) : f y = ∑ i, w i * y i := by
    conv_lhs => rw [← Finset.univ_sum_single y]
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro i hi
    have : Pi.single i (y i) = y i • Pi.single i (1 : ℝ) := by
      ext j
      by_cases h : j = i <;> simp [h]
    rw [this, map_smul]
    simp [w, mul_comm]
  have hn : f (fun _ => -1) < u := hNf _ (fun _ => by norm_num)
  have hw : ∀ i, 0 ≤ w i := by
    intro i
    by_contra hnwi
    have hwi : w i < 0 := lt_of_not_ge hnwi
    let t := (f (fun _ => -1) - u - 1) / w i
    have ht : 0 ≤ t := le_of_lt (div_pos_of_neg_of_neg (by linarith) hwi)
    have hneg : (fun _ => -1) - t • Pi.single i (1 : ℝ) ∈ N := by
      intro j
      by_cases h : j = i
      · simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, h, Pi.single_eq_same, mul_one]
        linarith
      · simp [h]
    have hv := hNf _ hneg
    rw [map_sub, map_smul] at hv
    have he : t * w i = f (fun _ => -1) - u - 1 := by
      dsimp [t]
      exact div_mul_cancel₀ _ (ne_of_lt hwi)
    change f (fun _ => -1) - t * w i < u at hv
    linarith
  have hw0 : w ≠ 0 := by
    intro he
    obtain ⟨y, hy⟩ := hne
    have hc := hCf y hy
    rw [hf, he] at hn hc
    simp at hn hc
    linarith
  have hsum : 0 < ∑ i, w i := by
    have hp : ∃ i, 0 < w i := by
      by_contra! h
      apply hw0
      ext i
      exact le_antisymm (h i) (hw i)
    obtain ⟨i, hi⟩ := hp
    exact Finset.sum_pos' (fun j _ => hw j) ⟨i, mem_univ _, hi⟩
  have hCy : ∀ y ∈ C, 0 ≤ ∑ i, w i * y i := by
    intro y hy
    by_contra hny
    have hfy : f y < 0 := by rw [hf]; exact lt_of_not_ge hny
    let z : Fin m → ℝ := fun _ => f y / (2 * ∑ i, w i)
    have hz : z ∈ N := fun i => div_neg_of_neg_of_pos hfy (by positivity)
    have hzf : f z = f y / 2 := by
      rw [hf]
      simp only [z, ← Finset.sum_mul]
      field_simp
    have hh := lt_of_lt_of_le (hNf z hz) (hCf y hy)
    rw [hzf] at hh
    linarith
  exact ⟨w, hw, hw0, hCy⟩

end QuadraticAggregation
