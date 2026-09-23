import Formal.DAGSpectral.CacheStorageExecution

/-! The trial independence test computes and caches the rational Gram matrix
and its determinant. Its arithmetic trace includes the two order comparisons
used to test whether the determinant is zero. -/
namespace DAGSpectral
namespace CoverNormalizationExecution
open Matrix ReciprocalAnchor NormalizationBits

structure IndependenceRun where
  determinant : ℚ
  independent : Bool
  events : List ArithmeticEvent
  copies : ℕ

def independenceRun {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) : IndependenceRun :=
  let G := mulRun Vᵀ V
  let d := (determinantExpr G.value).run
  let lower := compareRun d.1 0
  let upper := compareRun 0 d.1
  { determinant := d.1
    independent := !(lower.1 && upper.1)
    events := G.events ++ d.2 ++ lower.2 ++ upper.2
    copies := G.copies + RationalStorage.scalarCopy d.1 + 3 }

@[simp] theorem independenceRun_determinant {p r : ℕ}
    (V : Matrix (Fin p) (Fin r) ℚ) : (independenceRun V).determinant = (Vᵀ*V).det := by
  simp [independenceRun, ArithmeticExpr.run_eq, determinantExpr_eval]

@[simp] theorem independenceRun_value {p r : ℕ}
    (V : Matrix (Fin p) (Fin r) ℚ) :
    (independenceRun V).independent = decide ((Vᵀ*V).det ≠ 0) := by
  apply Bool.eq_iff_iff.mpr
  simp only [independenceRun, mulRun_value, ArithmeticExpr.run_eq, determinantExpr_eval,
    compareRun_value, Bool.not_eq_true', Bool.and_eq_false_iff, decide_eq_false_iff_not,
    decide_eq_true_eq]
  exact ⟨fun h he => h.elim (fun h => h (he.le)) (fun h => h (he.ge)),
    fun h => by by_cases hd : (Vᵀ*V).det ≤ 0
                · exact Or.inr (fun hh => h (le_antisymm hd hh))
                · exact Or.inl hd⟩

theorem independenceRun_code {p M : ℕ} (u : Fin M → Fin p → ℚ)
    (b : Finset (Fin M)) :
    (independenceRun (NormalizationTrials.columns u b)).independent =
      decide (NormalizationTrials.independent u b) := independenceRun_value _

@[simp] theorem independenceRun_events {p r : ℕ}
    (V : Matrix (Fin p) (Fin r) ℚ) :
    (independenceRun V).events = matrixMulTrace Vᵀ V ++ (determinantExpr (Vᵀ*V)).trace ++
      [(ManyLeaf.BitCost.RationalPrimitive.compare,(Vᵀ*V).det,0),
       (ManyLeaf.BitCost.RationalPrimitive.compare,0,(Vᵀ*V).det)] := by
  simp [independenceRun, ArithmeticExpr.run_eq, determinantExpr_eval, compareRun_events,
    List.append_assoc]

def independenceOperations (p r : ℕ) : ℕ := r*r*(2*p)+determinantOperations r+2

def independenceBudget (p r B : ℕ) : ℕ :=
  arithmeticWidth (2*p) (B+1) + arithmeticWidth (determinantOperations r) (gramBudget p B)+1

@[simp] theorem independenceRun_length {p r : ℕ}
    (V : Matrix (Fin p) (Fin r) ℚ) :
    (independenceRun V).events.length = independenceOperations p r := by
  simp [independenceOperations, Nat.add_assoc]

theorem independenceRun_bits {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) :
    ∀ e ∈ (independenceRun V).events, eventBits (independenceBudget p r B) e := by
  have hg := gram_bits hV
  have hgb : 0 < gramBudget p B := by unfold gramBudget mulBudget; omega
  obtain ⟨hd, ht⟩ := (determinantExpr (Vᵀ*V)).eval_trace_bits (determinantExpr_leaves hgb hg)
  simp only [determinantExpr_operations, determinantExpr_eval] at hd ht
  have hd' := rationalBits_mono hd (show arithmeticWidth (determinantOperations r)
      (gramBudget p B) ≤ independenceBudget p r B by unfold independenceBudget; omega)
  have hz := rationalBits_mono rationalBits_zero
    (show 1 ≤ independenceBudget p r B by unfold independenceBudget; omega)
  intro e he
  rw [independenceRun_events] at he
  simp only [List.mem_append, List.mem_cons, List.not_mem_nil, or_false] at he
  rcases he with (he | he) | (rfl | rfl)
  · exact eventBits_mono (matrixMulTrace_bits (B := B+1) (by omega)
      (matrixBits_mono (matrixBits_transpose hV) (by omega))
      (matrixBits_mono hV (by omega)) e he) (by unfold independenceBudget; omega)
  · exact eventBits_mono (ht e he) (by unfold independenceBudget; omega)
  · exact ⟨hd', hz⟩
  · exact ⟨hz, hd'⟩

def independenceBitCoefficient (p r : ℕ) : ℕ :=
  3*2^(2*p)+2^(determinantOperations r)*(gramBudget p 1+2)+1

theorem independenceBudget_linear (p r B : ℕ) :
    independenceBudget p r B ≤ independenceBitCoefficient p r*(B+1) := by
  have hg := gramBudget_scale (p := p) (show B ≤ 1*(B+1) by omega)
    (show 1 ≤ B+1 by omega)
  have h₁ : arithmeticWidth (2*p) (B+1) ≤ 3*2^(2*p)*(B+1) := by
    unfold arithmeticWidth
    calc
      _ ≤ 2^(2*p)*(B+1+2) := Nat.sub_le _ _
      _ ≤ 2^(2*p)*(3*(B+1)) := Nat.mul_le_mul_left _ (by omega)
      _ = _ := by ring
  have h₂ : arithmeticWidth (determinantOperations r) (gramBudget p B) ≤
      (2^(determinantOperations r)*(gramBudget p 1+2))*(B+1) := by
    unfold arithmeticWidth
    calc
      _ ≤ 2^(determinantOperations r)*(gramBudget p B+2) := Nat.sub_le _ _
      _ ≤ 2^(determinantOperations r)*((gramBudget p 1+2)*(B+1)) :=
        Nat.mul_le_mul_left _ (by nlinarith)
      _ = _ := by ring
  unfold independenceBudget independenceBitCoefficient
  nlinarith

def independenceCostCoefficient (p r : ℕ) : ℕ :=
  independenceOperations p r*256*(independenceBitCoefficient p r+1)^3

theorem independenceRun_bitWork {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) :
    traceBitWork (independenceBudget p r B) (independenceRun V).events ≤
      independenceCostCoefficient p r*(B+1)^3 := by
  have ht := traceBitWork_le (independenceRun_bits hV)
  rw [independenceRun_length] at ht
  have hb : independenceBudget p r B+1 ≤ (independenceBitCoefficient p r+1)*(B+1) := by
    have := independenceBudget_linear p r B
    nlinarith
  apply ht.trans
  calc
    _ ≤ independenceOperations p r*(256*((independenceBitCoefficient p r+1)*(B+1))^3) :=
      Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hb 3))
    _ = _ := by unfold independenceCostCoefficient; ring

/-- Store the cached Gram matrix, determinant, and comparison/control flags.
This cost is incurred before branching, including when the basis is rejected. -/
def independenceStorageBudget (p r B : ℕ) : ℕ :=
  matrixStorageBudget r r (gramBudget p B) + 2*determinantBits r (gramBudget p B)+4

@[simp] theorem independenceRun_copies {p r : ℕ} (V : Matrix (Fin p) (Fin r) ℚ) :
    (independenceRun V).copies = (mulRun Vᵀ V).copies +
      RationalStorage.scalarCopy (Vᵀ*V).det + 3 := by
  simp [independenceRun, ArithmeticExpr.run_eq, determinantExpr_eval]

theorem independenceRun_copies_le {p r B : ℕ} {V : Matrix (Fin p) (Fin r) ℚ}
    (hV : MatrixBits V B) :
    (independenceRun V).copies ≤ independenceStorageBudget p r B := by
  have hg := mulRun_copies_le (gram_bits hV)
  have hd := RationalStorage.scalarCopy_le (matrixBits_det (gram_bits hV))
  rw [independenceRun_copies]
  unfold independenceStorageBudget
  omega

theorem independenceStorageBudget_linear (p r B : ℕ) :
    independenceStorageBudget p r B ≤ independenceStorageBudget p r 1 * (B+1) := by
  have hg := gramBudget_scale (p := p) (show B ≤ 1*(B+1) by omega)
    (show 1 ≤ B+1 by omega)
  have hd := determinantBits_scale (n := r) hg (show 1 ≤ B+1 by omega)
  have hgm := Nat.mul_le_mul_left (2*(r*r)) hg
  have hdm := Nat.mul_le_mul_left 2 hd
  unfold independenceStorageBudget matrixStorageBudget
  nlinarith

theorem independenceRun_copies_polynomial {p r B : ℕ}
    {V : Matrix (Fin p) (Fin r) ℚ} (hV : MatrixBits V B) :
    (independenceRun V).copies ≤ independenceStorageBudget p r 1 * (B+1) :=
  (independenceRun_copies_le hV).trans (independenceStorageBudget_linear p r B)

end CoverNormalizationExecution
end DAGSpectral
