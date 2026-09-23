import QipmFormal.Coupling.Block

/-! # Positive normal blocks supply the invertible elimination factors

This finite-dimensional bridge discharges the invertibility premises of block
elimination from the positive quadratic form of the normal operator. It uses
orthogonal-sum inner products explicitly, avoiding the default product norm.
-/
namespace QipmFormal.Coupling
noncomputable section

variable {U K : Type*} [NormedAddCommGroup U] [InnerProductSpace ℝ U]
  [NormedAddCommGroup K] [InnerProductSpace ℝ K]

/-- A strictly positive quadratic form has no kernel. Symmetry is not needed
for this implication. -/
theorem positive_operator_injective (L : U →ₗ[ℝ] U)
    (hL : ∀ u, u ≠ 0 → 0 < inner ℝ u (L u)) : Function.Injective L := by
  apply L.ker_eq_bot.mp
  apply LinearMap.ker_eq_bot'.mpr
  intro u hu
  by_contra hne
  have hp := hL u hne
  simp [hu] at hp

/-- Finite dimension upgrades positivity to an actual linear equivalence. -/
def positiveOperatorEquiv [FiniteDimensional ℝ U] (L : U →ₗ[ℝ] U)
    (hL : ∀ u, u ≠ 0 → 0 < inner ℝ u (L u)) : U ≃ₗ[ℝ] U :=
  LinearEquiv.ofInjectiveEndo L (positive_operator_injective L hL)

/-- Quadratic form of the exact-center normal operator before either block
has been assumed invertible. -/
def blockQuadratic (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K →ₗ[ℝ] K) (u : U) (v : K) : ℝ :=
  inner ℝ u (μ⁻¹ • C u + μ • (D u + T v)) +
    inner ℝ v (μ • (F u + E v))

theorem positive_inactive (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K →ₗ[ℝ] K) (hμ : 0 < μ)
    (hH : ∀ u v, u ≠ 0 ∨ v ≠ 0 → 0 < blockQuadratic μ C D F T E u v) :
    ∀ v, v ≠ 0 → 0 < inner ℝ v (E v) := by
  intro v hv
  have hp := hH 0 v (Or.inr hv)
  simp only [blockQuadratic, map_zero, inner_zero_left, zero_add,
    inner_smul_right] at hp
  exact (mul_pos_iff_of_pos_left hμ).1 hp

/-- The scaled Schur map is defined before its invertibility is proved. -/
def schurOperator (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K) : U →ₗ[ℝ] U :=
  C + μ ^ 2 • (D - T.comp (E.symm.toLinearMap.comp F))

lemma blockQuadratic_schur (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K) (hμ : μ ≠ 0) (u : U) :
    inner ℝ u (schurOperator μ C D F T E u) =
      μ * blockQuadratic μ C D F T E.toLinearMap u (-E.symm (F u)) := by
  simp only [schurOperator, LinearMap.add_apply, LinearMap.smul_apply,
    LinearMap.sub_apply, LinearMap.comp_apply, LinearEquiv.coe_coe,
    blockQuadratic, map_neg, E.apply_symm_apply, add_neg_cancel, smul_zero,
    inner_zero_right, add_zero, inner_add_right, inner_sub_right,
    inner_smul_right, inner_neg_right]
  field_simp
  ring

/-- The Schur complement is positive by evaluation on (u,−E⁻¹Fu). -/
theorem positive_schur (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K)
    (T : K →ₗ[ℝ] U) (E : K ≃ₗ[ℝ] K) (hμ : 0 < μ)
    (hH : ∀ u v, u ≠ 0 ∨ v ≠ 0 →
      0 < blockQuadratic μ C D F T E.toLinearMap u v) :
    ∀ u, u ≠ 0 → 0 < inner ℝ u (schurOperator μ C D F T E u) := by
  intro u hu
  rw [blockQuadratic_schur μ C D F T E (ne_of_gt hμ)]
  exact mul_pos hμ (hH u (-E.symm (F u)) (Or.inl hu))

/-- Positivity of the original block system supplies both equivalences needed
by `blockEquiv` and the exact inverse identities. -/
theorem positive_blocks_have_factors [FiniteDimensional ℝ U] [FiniteDimensional ℝ K]
    (μ : ℝ) (C D : U →ₗ[ℝ] U) (F : U →ₗ[ℝ] K) (T : K →ₗ[ℝ] U)
    (E₀ : K →ₗ[ℝ] K) (hμ : 0 < μ)
    (hH : ∀ u v, u ≠ 0 ∨ v ≠ 0 → 0 < blockQuadratic μ C D F T E₀ u v) :
    ∃ (E : K ≃ₗ[ℝ] K) (S : U ≃ₗ[ℝ] U),
      E.toLinearMap = E₀ ∧ HasSchurFactor μ C D F T E S := by
  let E := positiveOperatorEquiv E₀ (positive_inactive μ C D F T E₀ hμ hH)
  have hE : E.toLinearMap = E₀ := rfl
  have hs := positive_schur μ C D F T E hμ (by simpa only [hE] using hH)
  let S := positiveOperatorEquiv (schurOperator μ C D F T E) hs
  refine ⟨E, S, hE, ?_⟩
  intro u
  rfl

end
end QipmFormal.Coupling
