import Formal.DAGSpectral.CriterionSelect
import Formal.DAGSpectral.Criteria
import Formal.DAGSpectral.CriteriaCost
import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.RationalMatrixArithmetic

namespace DAGSpectral
open Matrix
open scoped ENNReal

@[simp] theorem ratMatrixReal_det {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    (ratMatrixReal A).det = (A.det : ℝ) := ((Rat.castHom ℝ).map_det A).symm

@[simp] theorem ratMatrixReal_trace {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) :
    Matrix.trace (ratMatrixReal A) = ((Matrix.trace A : ℚ) : ℝ) := by
  simp [Matrix.trace,ratMatrixReal]

@[simp] theorem ratMatrixReal_rationalMatrixInverse {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) :
    ratMatrixReal (rationalMatrixInverse A) = (ratMatrixReal A)⁻¹ := by
  rw [rationalMatrixInverse, ratMatrixReal_smul, Matrix.inv_def]
  simp only [Rat.cast_inv, ratMatrixReal_det, Ring.inverse_eq_inv]
  congr 1
  exact (Rat.castHom ℝ).map_adjugate A

def determinantLE {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : Bool := decide (A.det ≤ B.det)

theorem determinantLE_correct {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    determinantLE A B = true ↔ (ratMatrixReal A).det ≤ (ratMatrixReal B).det := by
  simp only [determinantLE,decide_eq_true_eq,ratMatrixReal_det]
  exact_mod_cast Iff.rfl

/-- Exact rational A-cost comparison; zero determinants encode infinite cost. -/
def inverseTraceCostLE {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) : Bool :=
  if B.det = 0 then true else if A.det = 0 then false else
    decide (Matrix.trace (rationalMatrixInverse A) ≤ Matrix.trace (rationalMatrixInverse B))

theorem inverseTraceCostLE_correct {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (hB : (ratMatrixReal B).PosSemidef) :
    inverseTraceCostLE A B = true ↔ inverseTraceCost (ratMatrixReal A) ≤
      inverseTraceCost (ratMatrixReal B) := by
  have ha : (ratMatrixReal A).PosDef ↔ A.det ≠ 0 := by
    rw [hA.posDef_iff_det_ne_zero,ratMatrixReal_det]
    norm_cast
  have hb : (ratMatrixReal B).PosDef ↔ B.det ≠ 0 := by
    rw [hB.posDef_iff_det_ne_zero,ratMatrixReal_det]
    norm_cast
  by_cases hzB : B.det = 0
  · simp [inverseTraceCostLE,hzB,inverseTraceCost,hb]
  by_cases hzA : A.det = 0
  · simp [inverseTraceCostLE,hzB,hzA,inverseTraceCost,ha,hb]
  have hpA := ha.mpr hzA
  have hpB := hb.mpr hzB
  have htB : 0 ≤ Matrix.trace (ratMatrixReal B)⁻¹ := hpB.inv.posSemidef.trace_nonneg
  rw [inverseTraceCostLE,if_neg hzB,if_neg hzA,decide_eq_true_eq,
    inverseTraceCost,if_pos hpA,inverseTraceCost,if_pos hpB,
    ENNReal.ofReal_le_ofReal_iff htB]
  rw [← ratMatrixReal_rationalMatrixInverse, ← ratMatrixReal_rationalMatrixInverse,
    ratMatrixReal_trace,ratMatrixReal_trace]
  exact_mod_cast Iff.rfl

def selectDeterminant {α : Type*} {n : ℕ} (J : α → Matrix (Fin n) (Fin n) ℚ) :
    List α → Option α := bestBy (fun a b => determinantLE (J a) (J b))

def selectMinimumEigenvalue {α : Type*} {n : ℕ} (J : α → Matrix (Fin n) (Fin n) ℚ) :
    List α → Option α := bestBy (fun a b => minimumEigenvalueLE (J a) (J b))

def selectInverseTrace {α : Type*} {n : ℕ} (J : α → Matrix (Fin n) (Fin n) ℚ) :
    List α → Option α := bestBy (fun a b => inverseTraceCostLE (J b) (J a))

theorem selectDeterminant_spec {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α) {b : α}
    (hb : selectDeterminant J xs = some b) :
    b ∈ xs ∧ ∀ a ∈ xs, (ratMatrixReal (J a)).det ≤ (ratMatrixReal (J b)).det := by
  have hh := bestBy_spec (fun a b => determinantLE (J a) (J b))
    (fun a => (ratMatrixReal (J a)).det) (fun _ => True)
    (fun a _ b _ => determinantLE_correct _ _) xs (by simp) hb
  exact ⟨hh.1,hh.2.2⟩

theorem selectMinimumEigenvalue_spec {α : Type*} {n : ℕ} [Nonempty (Fin n)]
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, (ratMatrixReal (J a)).PosSemidef) {b : α}
    (hb : selectMinimumEigenvalue J xs = some b) :
    b ∈ xs ∧ ∀ a ∈ xs, minimumEigenvalue (ratMatrixReal (J a)) ≤
      minimumEigenvalue (ratMatrixReal (J b)) := by
  have hh := bestBy_spec (fun a b => minimumEigenvalueLE (J a) (J b))
    (fun a => minimumEigenvalue (ratMatrixReal (J a)))
    (fun a => (ratMatrixReal (J a)).PosSemidef)
    (fun a ha b hb => minimumEigenvalueLE_correct _ _ ha hb) xs hJ hb
  exact ⟨hh.1,hh.2.2⟩

theorem selectInverseTrace_spec {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, (ratMatrixReal (J a)).PosSemidef) {b : α}
    (hb : selectInverseTrace J xs = some b) :
    b ∈ xs ∧ ∀ a ∈ xs, inverseTraceCost (ratMatrixReal (J b)) ≤
      inverseTraceCost (ratMatrixReal (J a)) := by
  have hh := bestBy_spec (β := OrderDual ℝ≥0∞)
    (fun a b => inverseTraceCostLE (J b) (J a))
    (fun a => inverseTraceCost (ratMatrixReal (J a)))
    (fun a => (ratMatrixReal (J a)).PosSemidef)
    (fun a ha b hb => inverseTraceCostLE_correct _ _ hb ha) xs hJ hb
  exact ⟨hh.1,hh.2.2⟩

theorem IsRelativeCover.selectDeterminant_guarantee {α : Type*} [DecidableEq α]
    {n : ℕ} {ε : ℝ} {J : α → Matrix (Fin n) (Fin n) ℚ} {F : Finset α} {xs : List α}
    (h : IsRelativeCover (ε / n) (fun a => ratMatrixReal (J a)) F xs.toFinset)
    (hJ : ∀ a ∈ F, (ratMatrixReal (J a)).PosSemidef)
    (hn : 0 < n) (hε : 0 ≤ ε) (hε1 : ε ≤ 1) {b : α}
    (hb : selectDeterminant J xs = some b) :
    b ∈ F ∧ ∀ a ∈ F, (1-ε)*(ratMatrixReal (J a)).det ≤ (ratMatrixReal (J b)).det := by
  apply h.bestBy_guarantee (fun a b => determinantLE (J a) (J b))
    (fun a => (ratMatrixReal (J a)).det) (fun a => (1-ε)*(ratMatrixReal (J a)).det)
    (fun a _ b _ => determinantLE_correct _ _) _ hb
  intro a ha b hb hs
  exact hs.det_lower_eps (hJ a ha) (hJ b hb) hn hε hε1

theorem IsRelativeCover.selectMinimumEigenvalue_guarantee {α : Type*} [DecidableEq α]
    {n : ℕ} [NeZero n] {η : ℝ} {J : α → Matrix (Fin n) (Fin n) ℚ}
    {F : Finset α} {xs : List α}
    (h : IsRelativeCover η (fun a => ratMatrixReal (J a)) F xs.toFinset)
    (hJ : ∀ a ∈ F, (ratMatrixReal (J a)).PosSemidef) (hη : η ≤ 1) {b : α}
    (hb : selectMinimumEigenvalue J xs = some b) :
    b ∈ F ∧ ∀ a ∈ F, (1-η)*minimumEigenvalue (ratMatrixReal (J a)) ≤
      minimumEigenvalue (ratMatrixReal (J b)) := by
  apply h.bestBy_guarantee (fun a b => minimumEigenvalueLE (J a) (J b))
    (fun a => minimumEigenvalue (ratMatrixReal (J a)))
    (fun a => (1-η)*minimumEigenvalue (ratMatrixReal (J a)))
    (fun a ha b hb => minimumEigenvalueLE_correct _ _ (hJ a ha) (hJ b hb)) _ hb
  intro a ha b hb hs
  simpa using hs.criterion_lower (hJ a ha) (hJ b hb) hη minimumEigenvalue_criterion

theorem IsRelativeCover.selectInverseTrace_guarantee {α : Type*} [DecidableEq α]
    {n : ℕ} {η : ℝ} {J : α → Matrix (Fin n) (Fin n) ℚ} {F : Finset α} {xs : List α}
    (h : IsRelativeCover η (fun a => ratMatrixReal (J a)) F xs.toFinset)
    (hJ : ∀ a ∈ F, (ratMatrixReal (J a)).PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1) {b : α}
    (hb : selectInverseTrace J xs = some b) :
    b ∈ F ∧ ∀ a ∈ F, inverseTraceCost (ratMatrixReal (J b)) ≤
      ENNReal.ofReal ((1-η)⁻¹)*inverseTraceCost (ratMatrixReal (J a)) := by
  apply h.bestBy_guarantee (β := OrderDual ℝ≥0∞)
    (fun a b => inverseTraceCostLE (J b) (J a))
    (fun a => inverseTraceCost (ratMatrixReal (J a)))
    (fun a => ENNReal.ofReal ((1-η)⁻¹)*inverseTraceCost (ratMatrixReal (J a)))
    (fun a ha b hb => inverseTraceCostLE_correct _ _ (hJ b hb) (hJ a ha)) _ hb
  intro a _ b _ hs
  exact hs.inverseTraceCost_upper hη0 hη1

end DAGSpectral
