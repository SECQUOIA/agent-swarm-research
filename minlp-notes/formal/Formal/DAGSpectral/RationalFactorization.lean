import Formal.DAGSpectral.RationalSchur

/-! A rational LDL producer that skips zero PSD pivots. It uses only rational
arithmetic and branches on exact rational equality. -/
namespace DAGSpectral
open Matrix

abbrev RationalFactor (n : ℕ) := ℚ × (Fin n → ℚ)

def extendFactor {n : ℕ} (f : RationalFactor n) : RationalFactor (n + 1) :=
  (f.1, Fin.cases 0 f.2)

def factorValue {n : ℕ} (fs : List (RationalFactor n)) (i j : Fin n) : ℚ :=
  (fs.map fun f => f.1 * f.2 i * f.2 j).sum

def rationalLDL : (n : ℕ) → Matrix (Fin n) (Fin n) ℚ → List (RationalFactor n)
  | 0, _ => []
  | n + 1, A =>
    if A 0 0 = 0 then
      (rationalLDL n (A.submatrix Fin.succ Fin.succ)).map extendFactor
    else
      (A 0 0, fun i => A i 0 / A 0 0) ::
        (rationalLDL n (rationalSchur A)).map extendFactor

@[simp] theorem factorValue_nil {n : ℕ} (i j : Fin n) : factorValue [] i j = 0 := rfl
@[simp] theorem factorValue_cons {n : ℕ} (f : RationalFactor n)
    (fs : List (RationalFactor n)) (i j : Fin n) :
    factorValue (f::fs) i j = f.1*f.2 i*f.2 j + factorValue fs i j := by
  simp [factorValue]

@[simp] theorem factorValue_extend_zero_left {n : ℕ} (fs : List (RationalFactor n))
    (j : Fin (n + 1)) : factorValue (fs.map extendFactor) 0 j = 0 := by
  simp [factorValue,extendFactor,List.map_map,Function.comp_def]

@[simp] theorem factorValue_extend_zero_right {n : ℕ} (fs : List (RationalFactor n))
    (i : Fin (n + 1)) : factorValue (fs.map extendFactor) i 0 = 0 := by
  simp [factorValue,extendFactor,List.map_map,Function.comp_def]

@[simp] theorem factorValue_extend_succ {n : ℕ} (fs : List (RationalFactor n))
    (i j : Fin n) : factorValue (fs.map extendFactor) i.succ j.succ = factorValue fs i j := by
  simp [factorValue,extendFactor,List.map_map,Function.comp_def]

/-- The producer performs at most one nonzero pivot per original coordinate. -/
theorem rationalLDL_length_le (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    (rationalLDL n A).length ≤ n := by
  induction n with
  | zero => simp [rationalLDL]
  | succ n ih =>
    simp only [rationalLDL]
    split
    · simpa only [List.length_map] using (ih (A.submatrix Fin.succ Fin.succ)).trans (Nat.le_succ n)
    · simpa only [List.length_cons,List.length_map] using Nat.succ_le_succ (ih (rationalSchur A))

/-- Every produced factor has positive weight and a nonzero rational column. -/
theorem rationalLDL_factors {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : A.PosSemidef) :
    ∀ f ∈ rationalLDL n A, 0 < f.1 ∧ f.2 ≠ 0 := by
  induction n with
  | zero => simp [rationalLDL]
  | succ n ih =>
    intro f hf
    by_cases hz : A 0 0 = 0
    · rw [rationalLDL,if_pos hz] at hf
      obtain ⟨g,hg,rfl⟩ := List.mem_map.mp hf
      have hg' := ih (A.submatrix Fin.succ Fin.succ) (hA.submatrix Fin.succ) g hg
      refine ⟨hg'.1, ?_⟩
      intro he
      apply hg'.2
      funext i
      exact congrFun he i.succ
    · have hp : 0 < A 0 0 := lt_of_le_of_ne (rationalPSD_diag_nonneg hA 0) (Ne.symm hz)
      rw [rationalLDL,if_neg hz,List.mem_cons] at hf
      rcases hf with rfl | hf
      · refine ⟨hp, ?_⟩
        intro he
        have hh := congrFun he 0
        simp [hz] at hh
      · obtain ⟨g,hg,rfl⟩ := List.mem_map.mp hf
        have hg' := ih (rationalSchur A) (rationalSchur_posSemidef hA hp) g hg
        refine ⟨hg'.1, ?_⟩
        intro he
        apply hg'.2
        funext i
        exact congrFun he i.succ

/-- Exact reconstruction, including zero and singular PSD matrices. -/
theorem rationalLDL_reconstruct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : A.PosSemidef) (i j : Fin n) : A i j = factorValue (rationalLDL n A) i j := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    have hsym (i j) : A i j = A j i := by
      simpa [Matrix.IsHermitian, Matrix.conjTranspose] using congrFun (congrFun hA.isHermitian j) i
    by_cases hz : A 0 0 = 0
    · rw [rationalLDL,if_pos hz]
      refine Fin.cases ?_ (fun i => ?_) i
      · rw [factorValue_extend_zero_left]
        exact rationalPSD_zero_row hA hz j
      · refine Fin.cases ?_ (fun j => ?_) j
        · rw [factorValue_extend_zero_right,hsym]
          exact rationalPSD_zero_row hA hz i.succ
        · rw [factorValue_extend_succ]
          exact ih (A.submatrix Fin.succ Fin.succ) (hA.submatrix Fin.succ) i j
    · have hp : 0 < A 0 0 := lt_of_le_of_ne (rationalPSD_diag_nonneg hA 0) (Ne.symm hz)
      rw [rationalLDL,if_neg hz]
      refine Fin.cases ?_ (fun i => ?_) i
      · rw [factorValue_cons,factorValue_extend_zero_left]
        simp only [div_self hz, mul_one,add_zero]
        rw [mul_div_cancel₀ _ hz,hsym]
      · refine Fin.cases ?_ (fun j => ?_) j
        · rw [factorValue_cons,factorValue_extend_zero_right]
          simp only [div_self hz,mul_one,add_zero]
          field_simp
        · rw [factorValue_cons,factorValue_extend_succ]
          have he := ih (rationalSchur A) (rationalSchur_posSemidef hA hp) i j
          dsimp [rationalSchur] at he
          rw [←he,hsym 0 j.succ]
          field_simp
          ring

/-- The all-zero input produces the empty list, rather than zero-weight factors. -/
@[simp] theorem rationalLDL_zero (n : ℕ) :
    rationalLDL n (0 : Matrix (Fin n) (Fin n) ℚ) = [] := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change (rationalLDL n 0).map extendFactor = []
    rw [ih]
    rfl

end DAGSpectral
