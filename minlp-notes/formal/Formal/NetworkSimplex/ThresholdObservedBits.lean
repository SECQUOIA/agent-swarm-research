import Formal.NetworkSimplex.ThresholdObservedCache
import Formal.NetworkSimplex.ThresholdOracleSize

/-! Rational encoding bounds for actual observed-label compression. -/
namespace NetworkSimplex.Chain.Threshold.RationalData
open ReciprocalAnchor
open scoped BigOperators

/-- Compression only copies input coordinates and forms one residual sum. -/
def observedInputBits (a B : ℕ) : ℕ := 3 + (a + 1) * (B + 1)

theorem compressObserved_inputBits {m L B : ℕ} {D : RationalData m L}
    (h : D.InputBits B) (J : Finset (Fin m)) :
    (D.compressObserved J).InputBits (observedInputBits J.card B) := by
  have hcopy : B ≤ observedInputBits J.card B := by
    unfold observedInputBits
    nlinarith
  have hz : RationalBits (0 : ℚ) (observedInputBits J.card B) :=
    rationalBits_mono rationalBits_zero (by unfold observedInputBits; omega)
  have hsum : RationalBits (∑ j : Fin J.card, D.weights (observedIndex J j).val.succ)
      (1 + J.card * (B + 1)) := by
    have hs := rationalBits_list_sum
      (xs := List.ofFn fun j : Fin J.card => D.weights (observedIndex J j).val.succ)
      (by intro q hq; obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hq; exact h.weights _)
    simpa only [List.length_ofFn, List.sum_ofFn] using hs
  have hr : RationalBits (1 - ∑ j : Fin J.card, D.weights (observedIndex J j).val.succ)
      (observedInputBits J.card B) :=
    rationalBits_mono (rationalBits_sub rationalBits_one hsum)
      (by unfold observedInputBits; nlinarith)
  constructor
  · intro i j
    refine Fin.cases ?_ (fun k => ?_) j
    · exact hz
    · exact rationalBits_mono (h.u i (observedIndex J k).val.succ) hcopy
  · intro i j
    refine Fin.cases ?_ (fun k => ?_) j
    · exact hz
    · exact rationalBits_mono (h.v i (observedIndex J k).val.succ) hcopy
  · intro j
    refine Fin.cases ?_ (fun k => ?_) j
    · exact hr
    · exact rationalBits_mono (h.weights (observedIndex J k).val.succ) hcopy
  · exact fun i => rationalBits_mono (h.xa i) hcopy
  · exact rationalBits_mono h.xh hcopy
  · intro j
    refine Fin.cases ?_ (fun k => ?_) j
    · exact hz
    · exact rationalBits_mono (h.zh (observedIndex J k).val.succ) hcopy

/-- The bound applies to the executable cached instance, including zero-weight
observed labels and an empty observed set. -/
theorem observedCache_inputBits {m L B : ℕ} {D : RationalData m L}
    (h : D.InputBits B) (labels : List (Fin m)) :
    (D.observedCache labels).data.InputBits (observedInputBits labels.toFinset.card B) := by
  rw [observedCache_data]
  exact compressObserved_inputBits h labels.toFinset

end NetworkSimplex.Chain.Threshold.RationalData
