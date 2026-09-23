import Formal.DAGSpectral.CriterionSelectMatrix
import Formal.DAGSpectral.RationalPseudoinverse

namespace DAGSpectral
open Matrix
open scoped ENNReal

/-- `none` represents an infinite cost; finite rational costs are clipped at
zero, matching `ENNReal.ofReal` even outside the PSD input contract. -/
def rationalCostLE : Option ℚ → Option ℚ → Bool
  | _, none => true
  | none, some _ => false
  | some a, some b => decide (max a 0 ≤ max b 0)

noncomputable def rationalCostValue : Option ℚ → ℝ≥0∞
  | none => ⊤
  | some a => ENNReal.ofReal (a : ℝ)

theorem rationalCostLE_correct (a b : Option ℚ) :
    rationalCostLE a b = true ↔ rationalCostValue a ≤ rationalCostValue b := by
  cases a with
  | none => cases b <;> simp [rationalCostLE,rationalCostValue]
  | some a =>
    cases b with
    | none => simp [rationalCostLE,rationalCostValue]
    | some b =>
      simp only [rationalCostLE,rationalCostValue,decide_eq_true_eq]
      have ha : ENNReal.ofReal (max (a : ℝ) 0) = ENNReal.ofReal (a : ℝ) := by simp
      have hb : ENNReal.ofReal (max (b : ℝ) 0) = ENNReal.ofReal (b : ℝ) := by simp
      rw [← ha, ← hb, ENNReal.ofReal_le_ofReal_iff (le_max_right _ _)]
      exact_mod_cast Iff.rfl

def rationalContrastCost {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) : Option ℚ :=
  if rationalEstimable A c then some (rationalContrastVariance A c) else none

theorem rationalContrastCost_value {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (c : Fin n → ℚ) :
    rationalCostValue (rationalContrastCost A c) =
      contrastCost (ratMatrixReal A) (fun i => (c i : ℝ)) := by
  rw [rationalContrastCost,contrastCost, dif_pos hA]
  by_cases hc : rationalEstimable A c = true
  · rw [if_pos hc,if_pos ((rationalEstimable_iff A hA.isHermitian c).mp hc)]
    simp only [rationalCostValue,rationalContrastVariance_eq A hA.isHermitian c]
  · rw [if_neg hc,if_neg (fun h => hc ((rationalEstimable_iff A hA.isHermitian c).mpr h))]
    rfl

def contrastCostLE {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) : Bool :=
  rationalCostLE (rationalContrastCost A c) (rationalContrastCost B c)

theorem contrastCostLE_correct {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef) (c : Fin n → ℚ) :
    contrastCostLE A B c = true ↔
      contrastCost (ratMatrixReal A) (fun i => (c i : ℝ)) ≤
      contrastCost (ratMatrixReal B) (fun i => (c i : ℝ)) := by
  rw [contrastCostLE,rationalCostLE_correct,rationalContrastCost_value A hA,
    rationalContrastCost_value B hB]

def selectContrast {α : Type*} {n : ℕ} (J : α → Matrix (Fin n) (Fin n) ℚ)
    (c : Fin n → ℚ) : List α → Option α :=
  bestBy (fun a b => contrastCostLE (J b) (J a) c)

theorem selectContrast_spec {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, (ratMatrixReal (J a)).PosSemidef) {b : α}
    (hb : selectContrast J c xs = some b) :
    b ∈ xs ∧ ∀ a ∈ xs, contrastCost (ratMatrixReal (J b)) (fun i => (c i : ℝ)) ≤
      contrastCost (ratMatrixReal (J a)) (fun i => (c i : ℝ)) := by
  have hh := bestBy_spec (β := OrderDual ℝ≥0∞)
    (fun a b => contrastCostLE (J b) (J a) c)
    (fun a => contrastCost (ratMatrixReal (J a)) (fun i => (c i : ℝ)))
    (fun a => (ratMatrixReal (J a)).PosSemidef)
    (fun a ha b hb => contrastCostLE_correct _ _ hb ha c) xs hJ hb
  exact ⟨hh.1,hh.2.2⟩

theorem IsRelativeCover.selectContrast_guarantee {α : Type*} [DecidableEq α] {n : ℕ}
    {η : ℝ} {J : α → Matrix (Fin n) (Fin n) ℚ} {F : Finset α} {xs : List α}
    (h : IsRelativeCover η (fun a => ratMatrixReal (J a)) F xs.toFinset)
    (hJ : ∀ a ∈ F, (ratMatrixReal (J a)).PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1)
    (c : Fin n → ℚ) {b : α} (hb : selectContrast J c xs = some b) :
    b ∈ F ∧ ∀ a ∈ F, contrastCost (ratMatrixReal (J b)) (fun i => (c i : ℝ)) ≤
      ENNReal.ofReal ((1-η)⁻¹) * contrastCost (ratMatrixReal (J a)) (fun i => (c i : ℝ)) := by
  apply h.bestBy_guarantee (β := OrderDual ℝ≥0∞)
    (fun a b => contrastCostLE (J b) (J a) c)
    (fun a => contrastCost (ratMatrixReal (J a)) (fun i => (c i : ℝ)))
    (fun a => ENNReal.ofReal ((1-η)⁻¹) *
      contrastCost (ratMatrixReal (J a)) (fun i => (c i : ℝ)))
    (fun a ha b hb => contrastCostLE_correct _ _ (hJ b hb) (hJ a ha) c) ?_ hb
  intro a ha b hb hs
  exact hs.contrastCost_upper (hJ a ha) (hJ b hb) hη0 hη1 _

end DAGSpectral
