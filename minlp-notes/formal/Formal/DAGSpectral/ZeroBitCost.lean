import Formal.DAGSpectral.CoverWholeExecution

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators
namespace CoverBitCost
open CoverNormalizationExecution NormalizationTrials

theorem matrixZeroRun_events_length {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    (matrixZeroRun A).2.length = 2*p*p := by
  simp [matrixZeroRun,List.length_flatten,List.map_flatten,Function.comp_def,compareRun_events]
  ring

theorem matrixZeroRun_events_bits {p B : ℕ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hA : MatrixBits A B) : ∀ e ∈ (matrixZeroRun A).2, eventBits B e := by
  intro e he
  have hh : ∃ i j, e = (.compare,A i j,0) ∨ e = (.compare,0,A i j) := by
    simpa [matrixZeroRun,List.mem_flatten,List.mem_map,List.mem_ofFn,compareRun_events,
      eq_comm,or_and_right,exists_or] using he
  obtain ⟨i,j,hi|hi⟩ := hh
  · subst e
    exact ⟨hA i j,rationalBits_mono rationalBits_zero (rationalBits_pos (hA i j))⟩
  · subst e
    exact ⟨rationalBits_mono rationalBits_zero (rationalBits_pos (hA i j)),hA i j⟩

theorem matrixZeroRun_bitWork {p B : ℕ} {A : Matrix (Fin p) (Fin p) ℚ}
    (hA : MatrixBits A B) :
    traceBitWork B (matrixZeroRun A).2 ≤ (2*p*p)*(256*(B+1)^3) := by
  simpa only [matrixZeroRun_events_length] using traceBitWork_le (matrixZeroRun_events_bits hA)

/-- The zero-rank producer executes only rational zero tests and a singleton-state
DP. No externally supplied profile-window or label-size premise is required. -/
theorem zeroBitRun_work {v m p M B : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (hA : ∀ o, MatrixBits (D.atom o) B) :
    (zeroBitRun G s t D B).2 ≤
      (m+1)*((2*p*p)*(256*(B+1)^3)+4*p*p+1) +
        ExplicitDAG.dpWorkPolynomial v m 0 0 B 1 + 1 := by
  have hz (allowed : Fin m → Bool) :
      (G.outputBitCounted allowed s ∅ (fun _ (_ : Fin 0) => (0:ℤ)) t).2 ≤
        ExplicitDAG.dpWorkPolynomial v m 0 0 B 1 := by
    apply (ExplicitDAG.outputBitCounted_work G allowed s ∅ _ t).trans
    apply ExplicitDAG.dpBitWork_capacity_bound G allowed s ∅ _
      (fun _ i => Fin.elim0 i) ({0} : Finset ℤ)
      (fun _ _ _ i => Fin.elim0 i) (by simp) (by simp)
  have hp := matrixZeroRun_bitWork (hA none)
  have hs : (∑ e : Fin m, traceBitWork B (matrixZeroRun (D.atom (some e))).2) ≤
      m*((2*p*p)*(256*(B+1)^3)) := by
    calc
      _ ≤ ∑ _e : Fin m, ((2*p*p)*(256*(B+1)^3)) :=
        Finset.sum_le_sum (fun e _ => matrixZeroRun_bitWork (hA (some e)))
      _ = _ := by simp
  simp only [zeroBitRun,Vector.get_ofFn,matrixZeroCacheRun_value,
    matrixZeroCacheRun_events,matrixZeroCacheRun_control,Vector.size_toArray,
    Finset.sum_add_distrib,Finset.sum_const,Finset.card_univ,Fintype.card_fin,
    smul_eq_mul]
  split_ifs
  · have hd := hz (fun e => (matrixZeroRun (D.atom (some e))).1)
    nlinarith
  · have hn : 0 ≤ ExplicitDAG.dpWorkPolynomial v m 0 0 B 1 := Nat.zero_le _
    nlinarith

end CoverBitCost
end DAGSpectral
