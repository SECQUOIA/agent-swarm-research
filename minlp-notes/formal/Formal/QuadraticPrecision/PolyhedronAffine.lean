import Formal.QuadraticPrecision.Polyhedron
import Mathlib

namespace QuadraticPrecision
noncomputable section

/-- Finite-dimensional affine inequalities have closed scalar projections. -/
theorem isClosed_exists_affine
    {V ι : Type*} [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V] [Finite ι]
    (row : ι → V →ᵃ[ℝ] ℝ) (c : ι → ℝ → ℝ) (hc : ∀ i, Continuous (c i)) :
    IsClosed {t : ℝ | ∃ v : V, ∀ i, row i v ≤ c i t} := by
  classical
  let B := Module.finBasis ℝ V
  have hformula (i : ι) (v : V) :
      row i v = (∑ k, (row i).linear (B k) * B.equivFun v k) + row i 0 := by
    have h := (row i).map_vadd (0 : V) v
    simp only [vadd_eq_add, add_zero] at h
    rw [h]
    congr 1
    have hh := congrArg (row i).linear (B.sum_equivFun v)
    simp only [map_sum, map_smul, smul_eq_mul] at hh
    simpa only [mul_comm] using hh.symm
  have hh := isClosed_exists_linear (Module.finrank ℝ V)
    (fun i k => (row i).linear (B k)) (fun i t => c i t - row i 0)
    (fun i => (hc i).sub continuous_const)
  convert hh using 1
  ext t
  constructor
  · rintro ⟨v, hv⟩
    refine ⟨B.equivFun v, fun i => ?_⟩
    have h := hv i
    rw [hformula] at h
    linarith
  · rintro ⟨y, hy⟩
    refine ⟨B.equivFun.symm y, fun i => ?_⟩
    rw [hformula, LinearEquiv.apply_symm_apply]
    exact (le_sub_iff_add_le).mp (hy i)

/-- Linear programming attainment with arbitrary real coefficients, lineality,
and an unbounded feasible region. -/
theorem affine_minimum
    {V ι : Type*} [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V] [Finite ι]
    (row : ι → V →ᵃ[ℝ] ℝ) (T : V →ᵃ[ℝ] ℝ)
    (hfeas : ∃ v, ∀ i, row i v ≤ 0)
    (hlower : ∃ L : ℝ, ∀ v, (∀ i, row i v ≤ 0) → L ≤ T v) :
    ∃ v, (∀ i, row i v ≤ 0) ∧ ∀ w, (∀ i, row i w ≤ 0) → T v ≤ T w := by
  classical
  let rows : ι ⊕ Bool → V →ᵃ[ℝ] ℝ := Sum.elim row (fun b => if b then T else -T)
  let rhs : ι ⊕ Bool → ℝ → ℝ := Sum.elim (fun _ _ => 0)
    (fun b t => if b then t else -t)
  have hc : ∀ i, Continuous (rhs i) := by
    intro i
    rcases i with i | b
    · exact continuous_const
    · cases b
      · exact continuous_neg
      · exact continuous_id
  have he (v : V) (t : ℝ) : (∀ i, rows i v ≤ rhs i t) ↔
      (∀ i, row i v ≤ 0) ∧ T v = t := by
    simp only [Sum.forall, Bool.forall_bool, rows, rhs, Sum.elim_inl, Sum.elim_inr,
      Bool.false_eq_true, ↓reduceIte, AffineMap.coe_neg, Pi.neg_apply, neg_le_neg_iff]
    constructor
    · rintro ⟨h, h₁, h₂⟩
      exact ⟨h, le_antisymm h₂ h₁⟩
    · rintro ⟨h, rfl⟩
      exact ⟨h, le_rfl, le_rfl⟩
  let S : Set ℝ := {t | ∃ v, (∀ i, row i v ≤ 0) ∧ T v = t}
  have hclosed : IsClosed S := by
    simpa only [he] using isClosed_exists_affine rows rhs hc
  have hn : S.Nonempty := by
    obtain ⟨v, hv⟩ := hfeas
    exact ⟨T v, v, hv, rfl⟩
  have hl : BddBelow S := by
    obtain ⟨L, hL⟩ := hlower
    refine ⟨L, ?_⟩
    rintro t ⟨v, hv, rfl⟩
    exact hL v hv
  obtain ⟨v, hv, ht⟩ := hclosed.csInf_mem hn hl
  refine ⟨v, hv, fun w hw => ?_⟩
  rw [ht]
  exact csInf_le hl ⟨w, hw, rfl⟩

end
end QuadraticPrecision
