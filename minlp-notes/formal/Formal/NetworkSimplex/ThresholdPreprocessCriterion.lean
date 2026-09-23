import Formal.NetworkSimplex.ThresholdCircuitPreprocess
import Formal.NetworkSimplex.ThresholdBoundedCriterion

/-! Exact feasibility from the actual cofactor library, including absent row groups. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
open Chain.Threshold

/-- A stored circuit is tested only when all of its rows are present. -/
def CompiledPartialTests {m N : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (table : Fin N → Option ℝ) : Prop :=
  ∀ c ∈ preprocessCircuits A,
    (∀ i, table (c.candidate.support i) ≠ none) →
      0 ≤ ∑ i, (c.weight i : ℝ) * (table (c.candidate.support i)).getD 0

/-- Actual preprocessing is complete for every pattern of present row groups.
There is no supplied circuit list or full-dimensionality assumption. -/
theorem feasible_iff_compiledPartialTests {m N : ℕ}
    (A : Matrix (Fin N) (Fin m) ℤ) (hA : RowSignedZeroOne A)
    (table : Fin N → Option ℝ) :
    (∃ x : Fin m → ℝ, ∀ i, table i ≠ none →
      ∑ j, (A i j : ℝ) * x j ≤ (table i).getD 0) ↔
      CompiledPartialTests A table := by
  classical
  constructor
  · rintro ⟨x, hx⟩ c hc hp
    exact integer_cancel_valid (fun i => A (c.candidate.support i))
      (fun i => (table (c.candidate.support i)).getD 0) id c.weight
      (preprocessCircuits_sound A hA hc).2.2
      (fun i => hx _ (hp i))
  · intro ht
    let Present := {i : Fin N // table i ≠ none}
    have hex : ∃ x : Fin m → ℝ, ∀ i : Present,
        ∑ j, (A i.val j : ℝ) * x j ≤ (table i.val).getD 0 := by
      apply (feasible_iff_positiveCircuits
        (fun (i : Present) j => (A i.val j : ℝ))
        (fun i => (table i.val).getD 0)).mpr
      intro C
      let D : PositiveCircuit (fun i j => (A i j : ℝ)) :=
        { size := C.size
          index := C.index.trans ⟨Subtype.val, Subtype.val_injective⟩
          mass := C.mass
          positive := C.positive
          total := C.total
          cancel := C.cancel
          independent := C.independent }
      obtain ⟨c, hc, hrange, scale, hscale, heq⟩ :=
        preprocessCircuits_complete A hA D
      have hp : ∀ i, table (c.candidate.support i) ≠ none := by
        intro i
        have hm : c.candidate.support i ∈ Set.range D.index := by
          rw [← hrange]
          exact ⟨i, rfl⟩
        obtain ⟨k, hk⟩ := hm
        rw [← hk]
        exact (C.index k).property
      have htest := ht c hc hp
      rw [heq (fun i => (table i).getD 0)] at htest
      exact nonneg_of_mul_nonneg_right htest hscale
    obtain ⟨x, hx⟩ := hex
    exact ⟨x, fun i hi => hx ⟨i, hi⟩⟩

end NetworkSimplex.Threshold
