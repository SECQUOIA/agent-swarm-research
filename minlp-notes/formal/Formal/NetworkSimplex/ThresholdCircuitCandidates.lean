import Formal.NetworkSimplex.ThresholdPositive
import Formal.NetworkSimplex.ThresholdCircuitWeights

/-! Every positive circuit occurs among the explicitly enumerated cofactor candidates. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- Enumerating row and column assignments suffices to find every positive circuit.
The returned weights are exactly normalized absolute cofactors, not an existential
integer representative with no link to the finite preprocessing procedure. -/
theorem PositiveCircuit.exists_cofactor_candidate {I : Type*} {m : ℕ}
    (A : Matrix I (Fin m) ℤ) (C : PositiveCircuit (fun i j => (A i j : ℝ)))
    (hA : RowSignedZeroOne A) :
    ∃ s : ℕ, s ≤ m ∧ ∃ rows : Fin (s + 1) ↪ I, ∃ cols : Fin s ↪ Fin m,
      let p := primitiveWeights (fun i => (cofactorVector (A.submatrix rows cols) i).natAbs)
      (∀ i, 0 < p i ∧ p i ≤ delta01 m) ∧ Finset.univ.gcd p = 1 ∧
      (∀ j, ∑ i, (p i : ℤ) * A (rows i) j = 0) ∧
      Set.range rows = Set.range C.index ∧
      ∃ scale : ℝ, 0 < scale ∧ ∀ b : I → ℝ,
        (∑ i, (p i : ℝ) * b (rows i)) = scale * ∑ i, C.mass i * b (C.index i) := by
  classical
  let s := C.size - 1
  have hs : s + 1 = C.size := by have := C.size_pos; dsimp [s]; omega
  have hsm : s ≤ m := by have := C.size_le; omega
  let e : Fin (s + 1) ≃ Fin C.size := finCongr hs
  let D : PositiveCircuit (fun i j => (A i j : ℝ)) := {
    size := s + 1
    index := e.toEmbedding.trans C.index
    mass := fun i => C.mass (e i)
    positive := fun i => C.positive (e i)
    total := (e.sum_comp C.mass).trans C.total
    cancel := (e.sum_comp (fun i => C.mass i • (fun j => (A (C.index i) j : ℝ)))).trans C.cancel
    independent := C.independent.comp_embedding e.toEmbedding
  }
  let B : Matrix (Fin (s + 1)) (Fin m) ℤ := fun i => A (D.index i)
  have hB : RowSignedZeroOne B := fun i => hA (D.index i)
  have hli : LinearIndependent ℝ (fun i : Fin s => fun j => (B i.succ j : ℝ)) :=
    tail_independent_of_kernel_unique (fun i j => (B i j : ℝ)) D.mass (D.positive 0)
      (fun v hv => D.kernel_unique v hv)
  obtain ⟨cols, p, hpdef, hp, hgp, hcp⟩ := exists_primitive_bounded_cofactor_weights
    B hB D.mass D.positive D.cancel hli
  have hkernel : (∑ i, (p i : ℝ) • (fun j => (A (D.index i) j : ℝ))) = 0 := by
    ext j
    have h := hcp j
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
    exact_mod_cast h
  have hprop := D.kernel_unique (fun i => (p i : ℝ)) hkernel
  have hscale : (0 : ℝ) < ∑ i, (p i : ℝ) := by
    apply Finset.sum_pos'
    · intro i _
      exact_mod_cast (hp i).1.le
    · exact ⟨0, Finset.mem_univ _, by exact_mod_cast (hp 0).1⟩
  refine ⟨s, hsm, D.index, cols, ?_⟩
  have heq : primitiveWeights
      (fun i => (cofactorVector (A.submatrix D.index cols) i).natAbs) = p := hpdef.symm
  rw [heq]
  refine ⟨hp, hgp, hcp, ?_, ∑ i, (p i : ℝ), hscale, ?_⟩
  · ext i
    constructor
    · rintro ⟨j, rfl⟩
      exact ⟨e j, rfl⟩
    · rintro ⟨j, rfl⟩
      refine ⟨e.symm j, ?_⟩
      change C.index (e (e.symm j)) = C.index j
      rw [e.apply_symm_apply]
  · intro b
    calc
      _ = (∑ j, (p j : ℝ)) * ∑ i, D.mass i * b (D.index i) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        rw [hprop i]
        ring
      _ = _ := congrArg ((∑ j, (p j : ℝ)) * ·)
        (e.sum_comp (fun i => C.mass i * b (C.index i)))

end NetworkSimplex.Chain.Threshold
