import Mathlib

/-! Small positive dependencies obtained from actual cancellation vectors. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- A normalized positive dependence with affinely independent supporting normals. -/
structure PositiveCircuit {I : Type*} (A : I → (Fin m → ℝ)) where
  size : ℕ
  index : Fin size ↪ I
  mass : Fin size → ℝ
  positive : ∀ i, 0 < mass i
  total : ∑ i, mass i = 1
  cancel : ∑ i, mass i • A (index i) = 0
  independent : AffineIndependent ℝ (fun i => A (index i))

theorem PositiveCircuit.size_pos {I : Type*} {A : I → (Fin m → ℝ)}
    (C : PositiveCircuit A) : 0 < C.size := by
  by_contra h
  have he : C.size = 0 := by omega
  have : IsEmpty (Fin C.size) := ⟨fun i => by have := i.isLt; omega⟩
  have ht := C.total
  simp at ht

theorem PositiveCircuit.size_le {I : Type*} {A : I → (Fin m → ℝ)}
    (C : PositiveCircuit A) : C.size ≤ m + 1 := by
  have h := C.independent.card_le_finrank_succ
  have hb := Submodule.finrank_le (vectorSpan ℝ (Set.range (fun i => A (C.index i))))
  simpa only [Fintype.card_fin, Module.finrank_pi, Module.finrank_self, Finset.sum_const,
    Finset.card_univ, smul_eq_mul, mul_one] using h.trans (Nat.add_le_add_right hb 1)

/-- Affine independence and a positive barycenter make the linear relation unique. -/
theorem PositiveCircuit.kernel_unique {I : Type*} {A : I → (Fin m → ℝ)}
    (C : PositiveCircuit A) (v : Fin C.size → ℝ)
    (hv : ∑ i, v i • A (C.index i) = 0) :
    ∀ i, v i = (∑ j, v j) * C.mass i := by
  have hs : ∑ i, (v i - (∑ j, v j) * C.mass i) = 0 := by
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum, C.total]
    ring
  have hc : ∑ i, (v i - (∑ j, v j) * C.mass i) • A (C.index i) = 0 := by
    simp only [sub_smul, mul_smul, Finset.sum_sub_distrib, ← Finset.smul_sum,
      hv, C.cancel, smul_zero, sub_zero]
  intro i
  exact sub_eq_zero.mp (C.independent.eq_zero_of_sum_eq_zero hs hc i (Finset.mem_univ i))

/-- Removing any support position destroys every nonzero linear dependence. -/
theorem PositiveCircuit.kernel_eq_zero_of_zero_coordinate {I : Type*}
    {A : I → (Fin m → ℝ)} (C : PositiveCircuit A) (v : Fin C.size → ℝ)
    (hv : ∑ i, v i • A (C.index i) = 0) (k : Fin C.size) (hk : v k = 0) :
    v = 0 := by
  have hu := C.kernel_unique v hv
  have hs : (∑ j, v j) = 0 := by
    have he := hu k
    rw [hk] at he
    exact (mul_eq_zero.mp he.symm).resolve_right (ne_of_gt (C.positive k))
  funext i
  simpa only [hs, zero_mul, Pi.zero_apply] using hu i

/-- A nonzero nonnegative cancellation vector contains a small positive circuit.
Its support is selected from the strictly positive original entries. -/
theorem exists_positiveCircuit {I : Type*} [Fintype I] (A : I → (Fin m → ℝ))
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (hne : ∃ i, 0 < u i)
    (hcancel : ∑ i, u i • A i = 0) :
    ∃ C : PositiveCircuit A, ∀ i, 0 < u (C.index i) := by
  classical
  let S : Set (Fin m → ℝ) := A '' {i | 0 < u i}
  have hsum : 0 < ∑ i, u i := by
    obtain ⟨i, hi⟩ := hne
    exact Finset.sum_pos' (fun j _ => hu j) ⟨i, Finset.mem_univ i, hi⟩
  let J := {i : I // 0 < u i}
  have htotal : ∑ i : J, u i = ∑ i, u i := by
    have he := Fintype.sum_subtype_add_sum_subtype (fun i => 0 < u i) u
    rw [Finset.sum_eq_zero (f := fun i : {i : I // ¬0 < u i} => u i) (by
      intro i _
      exact le_antisymm (not_lt.mp i.property) (hu i)), add_zero] at he
    exact he
  have hvec : ∑ i : J, u i • A i = 0 := by
    have he := Fintype.sum_subtype_add_sum_subtype (fun i => 0 < u i) (fun i => u i • A i)
    have hz : ∑ i : {i : I // ¬0 < u i}, u i • A i = 0 := by
      apply Finset.sum_eq_zero
      intro i _
      rw [show u i = 0 from le_antisymm (not_lt.mp i.property) (hu i), zero_smul]
    rw [hz, add_zero, hcancel] at he
    exact he
  have hconv : (0 : Fin m → ℝ) ∈ convexHull ℝ S := by
    apply mem_convexHull_of_exists_fintype (fun i : J => u i / (∑ j, u j))
      (fun i : J => A i)
    · intro i
      exact div_nonneg (hu i) hsum.le
    · rw [← Finset.sum_div, htotal, div_self (ne_of_gt hsum)]
    · intro i
      exact ⟨i, i.property, rfl⟩
    · simp only [div_eq_mul_inv, mul_comm (u _) _, mul_smul, ← Finset.smul_sum, hvec,
        smul_zero]
  obtain ⟨K, hK, z, w, hzS, haff, hw, hw1, hzw⟩ :=
    eq_pos_convex_span_of_mem_convexHull hconv
  have hz : ∀ k, ∃ i, 0 < u i ∧ A i = z k := by
    intro k
    exact hzS ⟨k, rfl⟩
  choose f hf hzf using hz
  have hf_inj : Function.Injective f := by
    intro i j hij
    apply haff.injective
    rw [← hzf i, ← hzf j, hij]
  let e := (Fintype.equivFin K).symm
  let C : PositiveCircuit A := {
    size := Fintype.card K
    index := ⟨fun i => f (e i), hf_inj.comp e.injective⟩
    mass := fun i => w (e i)
    positive := fun i => hw (e i)
    total := (e.sum_comp w).trans hw1
    cancel := by
      change (∑ i, w (e i) • A (f (e i))) = 0
      simp only [hzf]
      exact (e.sum_comp (fun k => w k • z k)).trans hzw
    independent := by
      change AffineIndependent ℝ (fun i => A (f (e i)))
      simp only [hzf]
      exact haff.comp_embedding e.toEmbedding
  }
  exact ⟨C, fun i => hf (e i)⟩

end NetworkSimplex.Chain.Threshold
