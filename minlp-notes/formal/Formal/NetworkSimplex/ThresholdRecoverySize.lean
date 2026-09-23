import Formal.NetworkSimplex.ThresholdStateRecovery

/-! Reduced-rational size bounds for the actual cached state-flow recovery outputs. -/

namespace NetworkSimplex.Chain
open scoped BigOperators
open ReciprocalAnchor

variable {L N B : ℕ}

theorem rationalFixedA_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) (j : Fin N) :
    RationalBits (rationalFixedA c u v w j) (2 * B + 1) := by
  cases hc : c j <;> simp only [rationalFixedA, hc]
  · exact rationalBits_mono (hu j) (by omega)
  · convert rationalBits_sub (hw j) (hv j) using 1; omega
  · exact rationalBits_mono (hu j) (by omega)
  · exact rationalBits_mono rationalBits_zero (by omega)

theorem rationalFreeA_bits (c : Fin N → StateClass) (w : Fin N → ℚ)
    (hw : ∀ j, RationalBits (w j) B) (j : Fin N) :
    RationalBits (rationalFreeA c w j) (B + 1) := by
  unfold rationalFreeA
  split_ifs
  · exact rationalBits_mono (hw j) (by omega)
  · exact rationalBits_mono rationalBits_zero (by omega)

/-- All partial sums used in the fixed allocation have a polynomial size bound. -/
theorem fixedAPartialSum_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) (S : Finset (Fin N)) :
    RationalBits (∑ j ∈ S, rationalFixedA c u v w j) (1 + N * (2 * B + 2)) := by
  have hs := rationalBits_finset_sum S (rationalFixedA c u v w)
    (fun j _ => rationalFixedA_bits c u v w hu hv hw j)
  apply rationalBits_mono hs
  have hcard : S.card ≤ N := by simpa using Finset.card_le_card (Finset.subset_univ S)
  have hm := Nat.mul_le_mul_right (2 * B + 2) hcard
  convert Nat.add_le_add_left hm 1 using 1

theorem fixedASum_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) :
    RationalBits (∑ j, rationalFixedA c u v w j) (1 + N * (2 * B + 2)) :=
  fixedAPartialSum_bits c u v w hu hv hw Finset.univ

theorem recoveryResidual_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) (hxa : RationalBits xa B) :
    RationalBits (xa - ∑ j, rationalFixedA c u v w j) (B + N * (2 * B + 2) + 2) := by
  convert rationalBits_sub hxa (fixedASum_bits c u v w hu hv hw) using 1; omega

/-- Every intermediate greedy residual in gadget reconstruction is polynomially bounded. -/
theorem recoveryGreedyResiduals_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) (hxa : RationalBits xa B) (i : Fin (N + 1)) :
    RationalBits (greedyResiduals (rationalFreeA c w)
      (xa - ∑ j, rationalFixedA c u v w j) i) (B + N * (3 * B + 4) + 2) := by
  have hi := greedyResiduals_bits (rationalFreeA c w)
    (xa - ∑ j, rationalFixedA c u v w j) (rationalFreeA_bits c w hw)
    (recoveryResidual_bits c u v w xa hu hv hw hxa) i
  apply rationalBits_mono hi
  have hival : i.val ≤ N := by omega
  have hm := Nat.mul_le_mul_right (B + 2) hival
  nlinarith

def gadgetBits (N B : ℕ) : ℕ := 3 * B + N * (3 * B + 4) + 4

theorem recoverGadget_bits (c : Fin N → StateClass) (u v w : Fin N → ℚ) (xa : ℚ)
    (hu : ∀ j, RationalBits (u j) B) (hv : ∀ j, RationalBits (v j) B)
    (hw : ∀ j, RationalBits (w j) B) (hxa : RationalBits xa B) (j : Fin N) :
    RationalBits ((recoverGadget c u v w xa).1.get j) (gadgetBits N B) := by
  rw [recoverGadget_value]
  have hf := greedyFill_bits (rationalFreeA c w)
    (xa - ∑ j, rationalFixedA c u v w j) (rationalFreeA_bits c w hw)
    (recoveryResidual_bits c u v w xa hu hv hw hxa) j
  convert rationalBits_add (rationalFixedA_bits c u v w hu hv hw j) hf using 1
  unfold gadgetBits
  ring

def recoveryBits (N B : ℕ) : ℕ := 4 * B + N * (3 * B + 4) + 5

/-- Every materialized coordinate of the state-flow arrays has polynomial bit size.
The bound requires only rational input sizes, not feasibility of the candidate. -/
theorem recoverStateFlows_bits (c : Fin L → Fin N → StateClass)
    (u v : Fin L → Fin N → ℚ) (weights : Fin N → ℚ) (xa : Fin L → ℚ) (w : Fin N → ℚ)
    (hu : ∀ i j, RationalBits (u i j) B) (hv : ∀ i j, RationalBits (v i j) B)
    (hweights : ∀ j, RationalBits (weights j) B) (hxa : ∀ i, RationalBits (xa i) B)
    (hw : ∀ j, RationalBits (w j) B) :
    (∀ i j, RationalBits (((recoverStateFlows c u v weights xa w).a.get i).get j)
      (recoveryBits N B)) ∧
    (∀ i j, RationalBits (((recoverStateFlows c u v weights xa w).b.get i).get j)
      (recoveryBits N B)) ∧
    (∀ j, RationalBits ((recoverStateFlows c u v weights xa w).h.get j) (recoveryBits N B)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j
    rw [recoverStateFlows_a]
    apply rationalBits_mono (recoverGadget_bits (c i) (u i) (v i) w (xa i)
      (hu i) (hv i) hw (hxa i) j)
    unfold gadgetBits recoveryBits
    omega
  · intro i j
    rw [recoverStateFlows_b]
    convert rationalBits_sub (hw j) (recoverGadget_bits (c i) (u i) (v i) w (xa i)
      (hu i) (hv i) hw (hxa i) j) using 1
    unfold gadgetBits recoveryBits
    ring
  · intro j
    rw [recoverStateFlows_h]
    apply rationalBits_mono (rationalBits_sub (hweights j) (hw j))
    unfold recoveryBits
    omega

end NetworkSimplex.Chain
