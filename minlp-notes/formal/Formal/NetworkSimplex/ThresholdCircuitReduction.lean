import Formal.NetworkSimplex.ThresholdPositive

/-! Every negative cancellation certificate contains a negative positive circuit. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
noncomputable section

variable {I : Type*} {A : I → (Fin m → ℝ)}

def PositiveCircuit.weights (C : PositiveCircuit A) (i : I) : ℝ := by
  classical
  exact ∑ k, if C.index k = i then C.mass k else 0

theorem PositiveCircuit.weights_nonneg (C : PositiveCircuit A) (i : I) :
    0 ≤ C.weights i := by
  classical
  apply Finset.sum_nonneg
  intro k _
  split_ifs
  · exact (C.positive k).le
  · exact le_rfl

theorem PositiveCircuit.weights_index (C : PositiveCircuit A) (k : Fin C.size) :
    C.weights (C.index k) = C.mass k := by
  classical
  simp [weights, C.index.injective.eq_iff]

theorem PositiveCircuit.weights_zero (C : PositiveCircuit A) {i : I}
    (hi : ∀ k, C.index k ≠ i) : C.weights i = 0 := by
  classical
  simp [weights, hi]

variable [Fintype I]

theorem PositiveCircuit.weights_sum (C : PositiveCircuit A) : ∑ i, C.weights i = 1 := by
  classical
  simp only [weights]
  rw [Finset.sum_comm]
  simp [C.total]

theorem PositiveCircuit.weights_cancel (C : PositiveCircuit A) :
    ∑ i, C.weights i • A i = 0 := by
  classical
  simp only [weights, Finset.sum_smul]
  rw [Finset.sum_comm]
  simpa using C.cancel

theorem PositiveCircuit.weights_objective (C : PositiveCircuit A) (b : I → ℝ) :
    ∑ i, C.weights i * b i = ∑ k, C.mass k * b (C.index k) := by
  classical
  simp only [weights, Finset.sum_mul]
  rw [Finset.sum_comm]
  simp

omit [Fintype I] in
/-- Subtracting the largest feasible multiple removes at least one positive entry. -/
theorem PositiveCircuit.subtract_step (C : PositiveCircuit A) (u : I → ℝ)
    (hu : ∀ i, 0 ≤ u i) (hsupport : ∀ k, 0 < u (C.index k)) :
    ∃ t : ℝ, 0 < t ∧ (∀ i, 0 ≤ u i - t * C.weights i) ∧
      ∃ i, 0 < u i ∧ u i - t * C.weights i = 0 := by
  classical
  have hne : (Finset.univ : Finset (Fin C.size)).Nonempty :=
    ⟨⟨0, C.size_pos⟩, Finset.mem_univ _⟩
  obtain ⟨k, _, hk⟩ := Finset.exists_min_image Finset.univ
    (fun j => u (C.index j) / C.mass j) hne
  let t := u (C.index k) / C.mass k
  have ht : 0 < t := div_pos (hsupport k) (C.positive k)
  refine ⟨t, ht, ?_, C.index k, hsupport k, ?_⟩
  · intro i
    by_cases hi : ∃ j, C.index j = i
    · obtain ⟨j, rfl⟩ := hi
      rw [C.weights_index]
      exact sub_nonneg.mpr ((le_div_iff₀ (C.positive j)).mp (hk j (Finset.mem_univ j)))
    · rw [C.weights_zero (by simpa using hi), mul_zero, sub_zero]
      exact hu i
  · rw [C.weights_index]
    dsimp [t]
    rw [div_mul_cancel₀ _ (ne_of_gt (C.positive k)), sub_self]

/-- The actual set of row indices participating in a circuit. -/
def PositiveCircuit.support (C : PositiveCircuit A) : Finset I :=
  Finset.univ.map C.index

omit [Fintype I] in
theorem PositiveCircuit.mem_support (C : PositiveCircuit A) (i : I) :
    i ∈ C.support ↔ ∃ k, C.index k = i := by
  classical
  simp [support]

omit [Fintype I] in
theorem PositiveCircuit.support_card (C : PositiveCircuit A) :
    C.support.card = C.size := by simp [support]

theorem PositiveCircuit.sum_index_of_supported (C : PositiveCircuit A)
    {M : Type*} [AddCommMonoid M] (f : I → M) (hf : ∀ i, i ∉ C.support → f i = 0) :
    (∑ k, f (C.index k)) = ∑ i, f i := by
  classical
  calc
    _ = ∑ i ∈ C.support, f i := by simp [support]
    _ = ∑ i, f i := Finset.sum_subset (Finset.subset_univ _) (fun i _ hi => hf i hi)

/-- Every cancellation supported on a positive circuit lies on its one-dimensional line. -/
theorem PositiveCircuit.kernel_unique_global (C : PositiveCircuit A) (v : I → ℝ)
    (hv : ∑ i, v i • A i = 0) (hs : ∀ i, i ∉ C.support → v i = 0) :
    ∀ i, v i = (∑ j, v j) * C.weights i := by
  classical
  have htotal := C.sum_index_of_supported v hs
  have hvec := C.sum_index_of_supported (fun i => v i • A i)
    (fun i hi => by rw [hs i hi, zero_smul])
  rw [hv] at hvec
  have hk := C.kernel_unique (fun k => v (C.index k)) hvec
  intro i
  by_cases hi : i ∈ C.support
  · obtain ⟨k, rfl⟩ := (C.mem_support i).mp hi
    simpa only [htotal, C.weights_index] using hk k
  · rw [hs i hi, C.weights_zero (by simpa only [C.mem_support, not_exists] using hi), mul_zero]

omit [Fintype I] in
/-- The normalized circuit weights depend only on the support, not its enumeration. -/
theorem PositiveCircuit.weights_eq_of_support_eq [Finite I] (C D : PositiveCircuit A)
    (h : C.support = D.support) : C.weights = D.weights := by
  let : Fintype I := Fintype.ofFinite I
  funext i
  have hs : ∀ j, j ∉ C.support → D.weights j = 0 := by
    intro j hj
    rw [h] at hj
    exact D.weights_zero (by simpa only [D.mem_support, not_exists] using hj)
  have he := C.kernel_unique_global D.weights D.weights_cancel hs i
  simpa only [D.weights_sum, one_mul] using he.symm

/-- A violated nonnegative cancellation test has a violated positive circuit.
The proof successively removes a maximal positive circuit multiple. -/
theorem exists_negative_positiveCircuit (A : I → (Fin m → ℝ)) (b : I → ℝ)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i)
    (hcancel : ∑ i, u i • A i = 0) (hneg : ∑ i, u i * b i < 0) :
    ∃ C : PositiveCircuit A, ∑ k, C.mass k * b (C.index k) < 0 := by
  classical
  suffices hall : ∀ N : ℕ, ∀ v : I → ℝ,
      (Finset.univ.filter fun i => 0 < v i).card = N →
      (∀ i, 0 ≤ v i) → (∑ i, v i • A i = 0) → (∑ i, v i * b i < 0) →
      ∃ C : PositiveCircuit A, ∑ k, C.mass k * b (C.index k) < 0 from
    hall _ u rfl hu hcancel hneg
  intro N
  induction N using Nat.strong_induction_on with
  | h N ih =>
    intro v hN hv hvc hvneg
    have hpos : ∃ i, 0 < v i := by
      by_contra hn
      have hzero : ∀ i, v i = 0 := by
        intro i
        exact le_antisymm (not_lt.mp (not_exists.mp hn i)) (hv i)
      simp [hzero] at hvneg
    obtain ⟨C, hsupport⟩ := exists_positiveCircuit A v hv hpos hvc
    by_cases hbad : (∑ k, C.mass k * b (C.index k)) < 0
    · exact ⟨C, hbad⟩
    have hgood : 0 ≤ ∑ k, C.mass k * b (C.index k) := le_of_not_gt hbad
    obtain ⟨t, ht, hw, j, hj, hjzero⟩ := C.subtract_step v hv hsupport
    let w : I → ℝ := fun i => v i - t * C.weights i
    have hwc : ∑ i, w i • A i = 0 := by
      simp only [w, sub_smul, mul_smul, Finset.sum_sub_distrib, ← Finset.smul_sum,
        hvc, C.weights_cancel, smul_zero, sub_zero]
    have hwobj : ∑ i, w i * b i =
        (∑ i, v i * b i) - t * ∑ k, C.mass k * b (C.index k) := by
      simp only [w, sub_mul, mul_assoc, Finset.sum_sub_distrib, ← Finset.mul_sum,
        C.weights_objective]
    have hwneg : ∑ i, w i * b i < 0 := by
      rw [hwobj]
      have := mul_nonneg ht.le hgood
      linarith
    have hwcard : (Finset.univ.filter fun i => 0 < w i).card < N := by
      rw [← hN]
      apply Finset.card_lt_card
      apply Finset.ssubset_iff_subset_ne.mpr
      refine ⟨?_, ?_⟩
      · intro i hi
        have hwi := (Finset.mem_filter.mp hi).2
        have hn := mul_nonneg ht.le (C.weights_nonneg i)
        exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, by dsimp [w] at hwi; linarith⟩
      · intro he
        have hjmem : j ∈ Finset.univ.filter (fun i => 0 < v i) :=
          Finset.mem_filter.mpr ⟨Finset.mem_univ _, hj⟩
        rw [← he] at hjmem
        have h := (Finset.mem_filter.mp hjmem).2
        change 0 < v j - t * C.weights j at h
        rw [hjzero] at h
        exact lt_irrefl _ h
    exact ih _ hwcard w rfl hw hwc hwneg

end
end NetworkSimplex.Chain.Threshold
