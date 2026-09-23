import Formal.DAGSpectral.CriterionSelectCostTrace
import Formal.DAGSpectral.RationalContrastTrace

namespace DAGSpectral
open Matrix ReciprocalAnchor

/-- Convert the executed estimability/variance result into the finite-or-infinite cost. -/
def rationalContrastCostRun {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    Option ℚ × List ArithmeticEvent :=
  let r := rationalContrastWithTrace A c
  (if r.1.1 then some r.1.2 else none,r.2)

@[simp] theorem rationalContrastCostRun_value {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    (rationalContrastCostRun A c).1 = rationalContrastCost A c := by
  simp only [rationalContrastCostRun, rationalContrastWithTrace_value, rationalContrastCost]

theorem rationalContrastCostRun_bounds {n B : ℕ} (hB : 0 < B)
    {A : Matrix (Fin n) (Fin n) ℚ} {c : Fin n → ℚ}
    (hA : MatrixBits A B) (hc : ∀ i, RationalBits (c i) B) :
    (rationalContrastCostRun A c).2.length ≤ contrastOperations n ∧
      optionalRationalBits (rationalContrastCostRun A c).1 (contrastTraceBits n B) ∧
      ∀ e ∈ (rationalContrastCostRun A c).2, eventBits (contrastTraceBits n B) e := by
  have h := rationalContrastWithTrace_bits hB hA hc
  refine ⟨rationalContrastWithTrace_length A c, ?_, h.2⟩
  rw [rationalContrastCostRun_value]
  intro q hq
  unfold rationalContrastCost at hq
  split_ifs at hq
  · have hq' : q = rationalContrastVariance A c := by simpa [eq_comm] using hq
    simpa only [hq'] using h.1
  · simp at hq

def contrastCostLERun {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) :
    Bool × List ArithmeticEvent :=
  let a := rationalContrastCostRun A c
  let b := rationalContrastCostRun B c
  let t := rationalCostLERun a.1 b.1
  (t.1, a.2 ++ b.2 ++ t.2)

@[simp] theorem contrastCostLERun_value {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ)
    (c : Fin n → ℚ) : (contrastCostLERun A B c).1 = contrastCostLE A B c := by
  simp only [contrastCostLERun, rationalCostLERun_value, rationalContrastCostRun_value,
    contrastCostLE]

theorem contrastTraceBits_pos (n B : ℕ) : 0 < contrastTraceBits n B := by
  have h1 := arithmeticWidth_ge (2*n) (arithmeticWidth (pseudoInverseTraceDepth n) B+B+1)
  have h2 := arithmeticWidth_ge (2*n)
    (arithmeticWidth (2*n) (arithmeticWidth (pseudoInverseTraceDepth n) B+B+1))
  unfold contrastTraceBits
  omega

def contrastComparisonOperations (n : ℕ) : ℕ := 2*contrastOperations n+3

theorem contrastCostLERun_bounds {n K : ℕ} (hK : 0 < K)
    {A B : Matrix (Fin n) (Fin n) ℚ} {c : Fin n → ℚ}
    (hA : MatrixBits A K) (hB : MatrixBits B K) (hc : ∀ i, RationalBits (c i) K) :
    (contrastCostLERun A B c).2.length ≤ contrastComparisonOperations n ∧
      ∀ e ∈ (contrastCostLERun A B c).2, eventBits (contrastTraceBits n K) e := by
  have ha := rationalContrastCostRun_bounds hK hA hc
  have hb := rationalContrastCostRun_bounds hK hB hc
  have ht := rationalCostLERun_bounds (contrastTraceBits_pos n K) ha.2.1 hb.2.1
  constructor
  · simp only [contrastCostLERun, List.length_append]
    unfold contrastComparisonOperations
    omega
  · intro e he
    simp only [contrastCostLERun, List.mem_append] at he
    rcases he with (he|he)|he
    · exact ha.2.2 e he
    · exact hb.2.2 e he
    · exact ht.2 e he

/-- The actual finite candidate scan using the traced contrast comparator. -/
def selectContrastRun {α : Type*} {n : ℕ} (J : α → Matrix (Fin n) (Fin n) ℚ)
    (c : Fin n → ℚ) (xs : List α) : Option α × List ArithmeticEvent :=
  bestByRun (fun a b => contrastCostLERun (J b) (J a) c) xs

@[simp] theorem selectContrastRun_value {α : Type*} {n : ℕ}
    (J : α → Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) (xs : List α) :
    (selectContrastRun J c xs).1 = selectContrast J c xs := by
  simp only [selectContrastRun, bestByRun_result, contrastCostLERun_value, selectContrast]

theorem selectContrastRun_bounds {α : Type*} {n K : ℕ} (hK : 0 < K)
    (J : α → Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, MatrixBits (J a) K) (hc : ∀ i, RationalBits (c i) K) :
    (selectContrastRun J c xs).2.length ≤ (xs.length-1)*contrastComparisonOperations n ∧
      ∀ e ∈ (selectContrastRun J c xs).2, eventBits (contrastTraceBits n K) e :=
  bestByRun_bounds _ (fun a => MatrixBits (J a) K)
    (fun _a ha _b hb => contrastCostLERun_bounds hK hb ha hc) xs hJ

theorem selectContrastRun_bitWork {α : Type*} {n K : ℕ} (hK : 0 < K)
    (J : α → Matrix (Fin n) (Fin n) ℚ) (c : Fin n → ℚ) (xs : List α)
    (hJ : ∀ a ∈ xs, MatrixBits (J a) K) (hc : ∀ i, RationalBits (c i) K) :
    traceBitWork (contrastTraceBits n K) (selectContrastRun J c xs).2 ≤
      ((xs.length-1)*contrastComparisonOperations n)*(256*(contrastTraceBits n K+1)^3) :=
  (traceBitWork_le (selectContrastRun_bounds hK J c xs hJ hc).2).trans
    (Nat.mul_le_mul_right _ (selectContrastRun_bounds hK J c xs hJ hc).1)

end DAGSpectral
