import Formal.NetworkSimplex.ThresholdPositive
import Formal.NetworkSimplex.ThresholdCircuitWeights

/-! Primitive bounded integer representatives of positive real circuits. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- An actual positive circuit of row-signed zero-one integer normals has a
primitive positive integer representative. Its real normalization is exactly
the given circuit, so every right-hand-side evaluation has the same sign. -/
theorem PositiveCircuit.exists_primitive_integer_weights {I : Type*} {m : ℕ}
    (A : I → Fin m → ℤ)
    (C : PositiveCircuit (fun i j => (A i j : ℝ)))
    (hA : RowSignedZeroOne A) :
    ∃ p : Fin C.size → ℕ,
      (∀ i, 0 < p i ∧ p i ≤ delta01 m) ∧ Finset.univ.gcd p = 1 ∧
      (∀ j, ∑ i, (p i : ℤ) * A (C.index i) j = 0) ∧
      ∀ i, (p i : ℝ) = (∑ j, (p j : ℝ)) * C.mass i := by
  classical
  let s := C.size - 1
  have hs : s + 1 = C.size := by have := C.size_pos; dsimp [s]; omega
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
  obtain ⟨q, hq, hgq, hcq⟩ := exists_primitive_bounded_weights B hB D.mass
    D.positive D.cancel hli
  let p : Fin C.size → ℕ := fun i => q (e.symm i)
  have hp : ∀ i, 0 < p i ∧ p i ≤ delta01 m := fun i => hq (e.symm i)
  have hgp : Finset.univ.gcd p = 1 := by
    change Finset.univ.gcd (q ∘ e.symm) = 1
    rw [← Finset.gcd_image]
    simpa using hgq
  have hcp : ∀ j, ∑ i, (p i : ℤ) * A (C.index i) j = 0 := by
    intro j
    have he : (∑ i, (p i : ℤ) * A (C.index i) j) =
        ∑ i, (q i : ℤ) * B i j := by
      simpa [p, B, D] using
        (e.sum_comp (fun i => (p i : ℤ) * A (C.index i) j)).symm
    exact he.trans (hcq j)
  refine ⟨p, hp, hgp, hcp, C.kernel_unique (fun i => (p i : ℝ)) ?_⟩
  ext j
  have h := hcp j
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
  exact_mod_cast h

end NetworkSimplex.Chain.Threshold
