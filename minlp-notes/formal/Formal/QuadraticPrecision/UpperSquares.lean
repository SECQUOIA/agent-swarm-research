import Formal.QuadraticPrecision.UpperBounds
import Formal.QuadraticPrecision.SquareLift
import Formal.QuadraticPrecision.FoldingLift
namespace QuadraticPrecision
noncomputable section
open scoped BigOperators
variable {n : ℕ} {J : Type*} [Fintype J]

/-- Actual graph lift obtained by sharing the original affine coordinates. -/
def signedSquaresGraphLift (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ) :=
  UpperAssembly.lift D (fun _ : J => L) (fun _ => 2+(L+L))
    (fun _ => squareBinaryLift L false) y a c false

theorem signedSquares_graph (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ)
    (hy : ∀ x ∈ D.feasible, ∀ j, y j x ∈ Set.Icc (0 : ℝ) 1) :
    HasBinaryGraphLift D.feasible (fun x => a x + ∑ j, c j * (y j x) ^ 2)
      ((∑ j, |c j|) * (squareWidth L) ^ 2 / 4) (Fintype.card J * L) := by
  have h := UpperAssembly.graph D (fun _ : J => L) (fun _ => 2+(L+L))
    (fun _ => squareBinaryLift L false) y a c ((squareWidth L) ^ 2/4) hy
    (fun _ => squareBinaryLift_graph L)
  have hcount : Fintype.card (UpperAssembly.CodeIndex (fun _ : J => L)) =
      Fintype.card J * L := by simp
  rw [← mul_div_assoc] at h
  rw [← hcount]
  exact ⟨_, signedSquaresGraphLift D y a c L, h⟩

theorem signedSquaresGraphLift_rowCount (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ) :
    (signedSquaresGraphLift D y a c L).system.rowCount =
      D.rowCount + Fintype.card J * (11+L*10) + 2 := by
  simp [signedSquaresGraphLift]

theorem folding_square_error (L : ℕ) : foldError L = (squareWidth L) ^ 2/4 := by
  unfold foldError squareWidth
  rw [← pow_mul, Nat.mul_comm L 2, pow_mul]
  norm_num

namespace SignedEpigraph

private def componentData (c : J → ℝ) (L : ℕ) (j : J) :
    Σ p, Σ q, BinaryLinearLift 1 p q :=
  if c j < 0 then ⟨L, 2 + (L + L), squareBinaryLift L true⟩
  else ⟨0, L, foldingBinaryLift L⟩

def bits (c : J → ℝ) (L : ℕ) (j : J) : ℕ := (componentData c L j).1
def auxiliaries (c : J → ℝ) (L : ℕ) (j : J) : ℕ := (componentData c L j).2.1
def component (c : J → ℝ) (L : ℕ) (j : J) :
    BinaryLinearLift 1 (bits c L j) (auxiliaries c L j) := (componentData c L j).2.2

omit [Fintype J] in
@[simp] theorem bits_eq (c : J → ℝ) (L : ℕ) (j : J) :
    bits c L j = if c j < 0 then L else 0 := by
  unfold bits componentData
  split_ifs <;> rfl
omit [Fintype J] in
@[simp] theorem auxiliaries_eq (c : J → ℝ) (L : ℕ) (j : J) :
    auxiliaries c L j = if c j < 0 then 2 + (L + L) else L := by
  unfold auxiliaries
  split_ifs with h
  · rw [show componentData c L j = ⟨L, 2 + (L + L), squareBinaryLift L true⟩ by
      simp [componentData,h]]
  · rw [show componentData c L j = ⟨0, L, foldingBinaryLift L⟩ by
      simp [componentData,h]]

omit [Fintype J] in
@[simp] theorem component_relaxation (c : J → ℝ) (L : ℕ) (j : J) :
    (component c L j).relaxation =
      if c j < 0 then (squareBinaryLift L true).relaxation
      else (foldingBinaryLift L).relaxation := by
  unfold component bits auxiliaries
  split_ifs with h
  · rw [show componentData c L j = ⟨L, 2 + (L + L), squareBinaryLift L true⟩ by
      simp [componentData,h]]
  · rw [show componentData c L j = ⟨0, L, foldingBinaryLift L⟩ by
      simp [componentData,h]]

omit [Fintype J] in
theorem contains (c : J → ℝ) (L : ℕ) (j : J) (z : ℝ) (hz : z ∈ Set.Icc (0 : ℝ) 1) :
    ((fun _ => z),z ^ 2) ∈ (component c L j).relaxation := by
  classical
  by_cases h : c j < 0
  · simpa [component_relaxation,h] using
       (squareBinaryLift_hypograph L).1 (fun _ => z) hz (z ^ 2) le_rfl
  · simpa [component_relaxation,h] using
       (foldingBinaryLift_isEpigraph L).1 (fun _ => z) hz (z ^ 2) le_rfl

omit [Fintype J] in
theorem error (c : J → ℝ) (L : ℕ) (j : J) (z w : ℝ)
    (hzw : ((fun _ => z), w) ∈ (component c L j).relaxation) :
    c j * (z ^ 2 - w) ≤ |c j| * ((squareWidth L) ^ 2/4) := by
  classical
  by_cases h : c j < 0
  · have hzw' : ((fun _ => z), w) ∈ (squareBinaryLift L true).relaxation := by
      simpa [component_relaxation,h] using hzw
    have hs := ((squareBinaryLift_hypograph L).2 _ hzw').2
    change w ≤ z ^ 2+(squareWidth L) ^ 2/4 at hs
    rw [abs_of_neg h]
    have hm := mul_le_mul_of_nonpos_left hs (le_of_lt h)
    nlinarith
  · have hzw' : ((fun _ => z), w) ∈ (foldingBinaryLift L).relaxation := by
      simpa [component_relaxation,h] using hzw
    have hs := ((foldingBinaryLift_isEpigraph L).2 _ hzw').2
    change z ^ 2-foldError L ≤ w at hs
    rw [folding_square_error] at hs
    rw [abs_of_nonneg (le_of_not_gt h)]
    exact mul_le_mul_of_nonneg_left (by linarith) (le_of_not_gt h)

theorem bits_count (c : J → ℝ) (L : ℕ) :
    Fintype.card (UpperAssembly.CodeIndex (bits c L)) =
      Fintype.card {j // c j < 0} * L := by
  classical
  rw [UpperAssembly.code_count]
  simp only [bits_eq]
  rw [← Finset.sum_filter]
  simp [Fintype.card_subtype]

end SignedEpigraph

def signedSquaresEpigraphLift (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ) :=
  UpperAssembly.lift D (SignedEpigraph.bits c L) (SignedEpigraph.auxiliaries c L)
    (SignedEpigraph.component c L) y a c true

theorem signedSquares_epigraph (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ)
    (hy : ∀ x ∈ D.feasible, ∀ j, y j x ∈ Set.Icc (0 : ℝ) 1) :
    HasBinaryEpigraphLift D.feasible (fun x => a x + ∑ j, c j * (y j x) ^ 2)
      ((∑ j, |c j|) * (squareWidth L) ^ 2 / 4) (Fintype.card {j // c j < 0} * L) := by
  have h := UpperAssembly.epigraph D (SignedEpigraph.bits c L) (SignedEpigraph.auxiliaries c L)
    (SignedEpigraph.component c L) y a c ((squareWidth L) ^ 2/4) hy
    (SignedEpigraph.contains c L) (SignedEpigraph.error c L)
  rw [← mul_div_assoc] at h
  rw [← SignedEpigraph.bits_count c L]
  exact ⟨_, signedSquaresEpigraphLift D y a c L, h⟩

/-- Exact number of real auxiliary coordinates in the graph construction. -/
theorem signedSquaresGraphLift_auxCount (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (fun _ : J => 2 + (L + L))) =
      Fintype.card J * (3 + 2 * L) := by
  simp only [UpperAssembly.aux_count, Finset.sum_const, Finset.card_univ, smul_eq_mul]
  congr 1
  omega

namespace SignedEpigraph

omit [Fintype J] in
theorem component_rowCount (c : J → ℝ) (L : ℕ) (j : J) :
    (component c L j).system.rowCount =
      if c j < 0 then 11 + L * 10 else 3 * L + 3 := by
  classical
  by_cases h : c j < 0
  · unfold component bits auxiliaries
    rw [show componentData c L j = ⟨L, 2 + (L + L), squareBinaryLift L true⟩ by
      simp [componentData,h]]
    simp [h]
  · unfold component bits auxiliaries
    rw [show componentData c L j = ⟨0, L, foldingBinaryLift L⟩ by
      simp [componentData,h]]
    simpa [h,foldingBinaryLift] using foldingSystem_rowCount L

theorem auxiliaries_count_le (c : J → ℝ) (L : ℕ) :
    Fintype.card (UpperAssembly.AuxIndex (auxiliaries c L)) ≤
      Fintype.card J * (3 + 2 * L) := by
  rw [UpperAssembly.aux_count]
  calc
    ∑ j, (auxiliaries c L j + 1) ≤ ∑ _j : J, (3 + 2 * L) := by
      apply Finset.sum_le_sum
      intro j _
      rw [auxiliaries_eq]
      split_ifs <;> omega
    _ = _ := by simp
end SignedEpigraph

theorem signedSquaresEpigraphLift_rowCount (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ) :
    (signedSquaresEpigraphLift D y a c L).system.rowCount =
      D.rowCount + (∑ j, if c j < 0 then 11 + L * 10 else 3 * L + 3) + 2 := by
  simp [signedSquaresEpigraphLift, SignedEpigraph.component_rowCount]

theorem signedSquaresEpigraphLift_rowCount_le (D : LinearSystem (Input n))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) (L : ℕ) :
    (signedSquaresEpigraphLift D y a c L).system.rowCount ≤
      D.rowCount + Fintype.card J * (11 + L * 10) + 2 := by
  rw [signedSquaresEpigraphLift_rowCount]
  apply Nat.add_le_add_right
  apply Nat.add_le_add_left
  calc
    ∑ j, (if c j < 0 then 11 + L * 10 else 3 * L + 3) ≤
        ∑ _j : J, (11 + L * 10) := by
      apply Finset.sum_le_sum
      intro j _
      split_ifs <;> omega
    _ = _ := by simp

end
end QuadraticPrecision
