import Formal.QuadraticPrecision.UpperAssembly

namespace QuadraticPrecision
noncomputable section
open scoped BigOperators
namespace UpperAssembly
variable {n : ℕ} {J : Type*} [Fintype J]

/-- Two original-box inequalities per coordinate, including fixed coordinates. -/
def boxSystem (l u : Input n) : LinearSystem (Input n) where
  rowCount := n+n
  row := Fin.addCases (fun i => AffineMap.const ℝ _ (l i) - (LinearMap.proj i).toAffineMap)
    (fun i => (LinearMap.proj i).toAffineMap - AffineMap.const ℝ _ (u i))
@[simp] theorem boxSystem_feasible (l u x : Input n) :
    x ∈ (boxSystem l u).feasible ↔ ∀ i, x i ∈ Set.Icc (l i) (u i) := by
  change (∀ i, (boxSystem l u).row i x ≤ 0) ↔ _
  simp only [boxSystem, Fin.forall_fin_add, Fin.addCases_left, Fin.addCases_right]
  simp [Set.mem_Icc, forall_and]

theorem graph (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (δ : ℝ)
    (hy : ∀ x ∈ D.feasible, ∀ j, y j x ∈ Set.Icc (0 : ℝ) 1)
    (hS : ∀ j, IsGraphRelaxation {x : Input 1 | x 0 ∈ Set.Icc (0 : ℝ) 1}
      (fun x => (x 0) ^ 2) δ (S j).relaxation) :
    IsGraphRelaxation D.feasible (fun x => a x + ∑ j, c j * (y j x) ^ 2)
      ((∑ j, |c j|) * δ) (lift D p q S y a c false).relaxation := by
  constructor
  · intro x hx
    rw [relaxation]
    exact ⟨hx, fun j => (y j x) ^ 2, fun j => (hS j).1 _ (hy x hx j), le_rfl,
      fun _ => le_rfl⟩
  · rintro ⟨x,w⟩ hw
    obtain ⟨hx,t,ht,hw,hw'⟩ := (relaxation D p q S y a c false x w).mp hw
    have he : w = a x + ∑ j, c j * t j := le_antisymm (hw' rfl) hw
    refine ⟨hx, ?_⟩
    rw [he]
    have hid : a x + ∑ j, c j * t j - (a x + ∑ j, c j * (y j x) ^ 2) =
        ∑ j, c j * (t j - (y j x) ^ 2) := by
      simp only [mul_sub,Finset.sum_sub_distrib]; ring
    rw [hid]
    calc
      |∑ j, c j * (t j - (y j x) ^ 2)| ≤ ∑ j, |c j * (t j - (y j x) ^ 2)| :=
        Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ j, |c j| * δ := by
        apply Finset.sum_le_sum
        intro j _
        rw [abs_mul]
        exact mul_le_mul_of_nonneg_left ((hS j).2 _ (ht j)).2 (abs_nonneg _)
      _ = (∑ j, |c j|) * δ := (Finset.sum_mul _ _ _).symm

/-- Each signed component is allowed an unbounded favourable output direction. -/
theorem epigraph (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (δ : ℝ)
    (hy : ∀ x ∈ D.feasible, ∀ j, y j x ∈ Set.Icc (0 : ℝ) 1)
    (hc : ∀ j, ∀ z ∈ Set.Icc (0 : ℝ) 1,
      ((fun _ => z), z ^ 2) ∈ (S j).relaxation)
    (hs : ∀ j, ∀ z w, ((fun _ => z), w) ∈ (S j).relaxation →
      c j * (z ^ 2 - w) ≤ |c j| * δ) :
    IsEpigraphRelaxation D.feasible (fun x => a x + ∑ j, c j * (y j x) ^ 2)
      ((∑ j, |c j|) * δ) (lift D p q S y a c true).relaxation := by
  constructor
  · intro x hx w hw
    rw [relaxation]
    exact ⟨hx, fun j => (y j x) ^ 2, fun j => hc j _ (hy x hx j), hw,
      by simp⟩
  · rintro ⟨x,w⟩ hw
    obtain ⟨hx,t,ht,hw,_⟩ := (relaxation D p q S y a c true x w).mp hw
    refine ⟨hx, ?_⟩
    have hsum := Finset.sum_le_sum (s := Finset.univ) (fun j _ => hs j _ _ (ht j))
    simp only [mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul] at hsum
    linarith

end UpperAssembly
end
end QuadraticPrecision
