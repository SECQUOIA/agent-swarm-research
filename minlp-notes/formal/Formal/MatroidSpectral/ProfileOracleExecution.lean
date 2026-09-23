import Formal.MatroidSpectral.ProfileProducerOracle
import Formal.MatroidSpectral.InterpolationTraceBits

namespace MatroidSpectral
open scoped BigOperators
open ReciprocalAnchor DAGSpectral

structure CoefficientEvaluation where
  value : ℚ
  trace : List ArithmeticEvent
  evaluationWork : ℕ

section OrderedCoordinates
variable {κ : Type*} [Fintype κ] [LinearOrder κ]

/-- Every determinant evaluation is performed once per grid node and retained
together with its cost before the corresponding interpolation term is formed. -/
def coefficientEvaluationRun (D : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ) (z : κ → Fin (D + 1)) :
    CoefficientEvaluation :=
  let terms := (interpolationGridList κ D).map (fun t =>
    let value := evaluate t
    let term := interpolationTermTrace D value.1 t z
    (term, value.2))
  let total := (sumExpr (terms.map (fun t => .atom t.1.1))).run
  ⟨total.1, terms.flatMap (fun t => t.1.2) ++ total.2,
    (terms.map (fun t => t.2)).sum⟩

theorem coefficientEvaluationRun_value (D : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ) (z : κ → Fin (D + 1)) :
    (coefficientEvaluationRun D evaluate z).value =
      interpolateCoefficientRun D (fun t => (evaluate t).1) z := by
  rw [← interpolateCoefficientTrace_value]
  simp [coefficientEvaluationRun, interpolateCoefficientTrace, List.map_map,
    Function.comp_def]

theorem coefficientEvaluationRun_trace (D : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ) (z : κ → Fin (D + 1)) :
    (coefficientEvaluationRun D evaluate z).trace =
      (interpolateCoefficientTrace D (fun t => (evaluate t).1) z).2 := by
  simp [coefficientEvaluationRun, interpolateCoefficientTrace, List.map_map,
    Function.comp_def, List.flatMap_map]

theorem coefficientEvaluationRun_work (D E : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ)
    (he : ∀ t, (evaluate t).2 ≤ E) (z : κ → Fin (D + 1)) :
    (coefficientEvaluationRun D evaluate z).evaluationWork ≤
      (D + 1) ^ Fintype.card κ * E := by
  simp only [coefficientEvaluationRun, List.map_map, Function.comp_def]
  calc
    _ ≤ ((interpolationGridList κ D).map (fun _ => E)).sum :=
      List.sum_le_sum (fun t _ => he t)
    _ = _ := by simp [interpolationGridList_length, Nat.mul_comm]

/-- A polynomial scan/sort/copy charge for the explicit tensor grid and its
coordinate comparisons. Rational arithmetic is charged from recorded operands. -/
def coefficientLoopWork (d D B : ℕ) : ℕ :=
  32 * (d + 1) ^ 2 * (D + 2) ^ 4 * ((D + 1) ^ d + 1) ^ 2 *
    (interpolationTraceBits d D B + 1)

def coefficientQueryRun (D B : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ) (z : κ → Fin (D + 1)) : Bool × ℕ :=
  let run := coefficientEvaluationRun D evaluate z
  let comparison := decide (run.value ≤ 0)
  (!comparison, run.evaluationWork +
    traceBitWork (interpolationTraceBits (Fintype.card κ) D B)
      (run.trace ++ [(.compare, run.value, 0)]) +
    coefficientLoopWork (Fintype.card κ) D B)

theorem coefficientQueryRun_value (D B : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ) (z : κ → Fin (D + 1)) :
    (coefficientQueryRun D B evaluate z).1 =
      decide (0 < interpolateCoefficientRun D (fun t => (evaluate t).1) z) := by
  simp only [coefficientQueryRun, coefficientEvaluationRun_value]
  by_cases h : interpolateCoefficientRun D (fun t => (evaluate t).1) z ≤ 0
  · simp [h, not_lt.mpr h]
  · simp [h, lt_of_not_ge h]

def coefficientQueryWork (d D B E : ℕ) : ℕ :=
  (D + 1) ^ d * E +
    ((D + 1) ^ d * (d * ((2 * (D + 1) + 2) * D + 2) + 2) + 1) *
      (256 * (interpolationTraceBits d D B + 1) ^ 3) + coefficientLoopWork d D B

theorem coefficientQueryRun_work (D B E : ℕ)
    (evaluate : (κ → Fin (D + 1)) → ℚ × ℕ)
    (hb : ∀ t, RationalBits (evaluate t).1 B)
    (he : ∀ t, (evaluate t).2 ≤ E) (z : κ → Fin (D + 1)) :
    (coefficientQueryRun D B evaluate z).2 ≤
      coefficientQueryWork (Fintype.card κ) D B E := by
  let K := interpolationTraceBits (Fintype.card κ) D B
  have hvalue : RationalBits (coefficientEvaluationRun D evaluate z).value K := by
    rw [coefficientEvaluationRun_value]
    apply rationalBits_mono (interpolateCoefficientRun_bits D B _ hb z)
    dsimp [K, interpolationTraceBits, interpolationTermBits]
    apply Nat.add_le_add_left (Nat.mul_le_mul_left _ ?_) 1
    nlinarith
  have hzero : RationalBits 0 K := rationalBits_mono rationalBits_zero (by
    dsimp [K, interpolationTraceBits]
    omega)
  have htrace : ∀ e ∈ (coefficientEvaluationRun D evaluate z).trace ++
      [(.compare, (coefficientEvaluationRun D evaluate z).value, 0)], eventBits K e := by
    intro e he
    rcases List.mem_append.mp he with he | he
    · rw [coefficientEvaluationRun_trace] at he
      exact interpolateCoefficientTrace_bits D B _ hb z e he
    · simp only [List.mem_singleton] at he
      subst e
      exact ⟨hvalue, hzero⟩
  have ht := traceBitWork_le htrace
  rw [List.length_append, List.length_singleton, coefficientEvaluationRun_trace,
    interpolateCoefficientTrace_length] at ht
  have heval := coefficientEvaluationRun_work D E evaluate he z
  simpa only [coefficientQueryRun, coefficientQueryWork, coefficientEvaluationRun_trace] using
    Nat.add_le_add_right (Nat.add_le_add heval ht) (coefficientLoopWork (Fintype.card κ) D B)

end OrderedCoordinates
end MatroidSpectral
