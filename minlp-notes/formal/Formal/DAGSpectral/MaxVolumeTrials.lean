import Formal.DAGSpectral.MaxVolume
import Formal.DAGSpectral.RangeNormalization

namespace DAGSpectral
open Module Matrix
open scoped Matrix

variable {J : Type*} [Finite J] {p : ℕ}

def realFactorFamily (v : J → Fin p → ℚ) (j : J) : Fin p → ℝ := fun i => (v j i : ℝ)

def selectedColumns {r : ℕ} (v : J → Fin p → ℚ) (b : Fin r → J) : Matrix (Fin p) (Fin r) ℚ :=
  Matrix.of fun i j => v (b j) i

omit [Finite J] in
/-- A rational normalizer is determined on the actual selected raw columns. -/
theorem normalizer_selected_coordinate {r : ℕ} (v : J → Fin p → ℚ)
    (b : Fin r → J) (hb : Function.Injective (selectedColumns v b).mulVec)
    (τ : Fin r → ℚ) (i k : Fin r) :
    (ratMatrixReal (normalizer (selectedColumns v b) τ) *ᵥ realFactorFamily v (b i)) k =
      if k = i then (τ i : ℝ) else 0 := by
  have hm := congrArg ratMatrixReal (normalizer_mul_columns (selectedColumns v b) hb τ)
  rw [ratMatrixReal_mul] at hm
  have he := congrFun (congrFun hm k) i
  by_cases hk : k = i <;> simpa [Matrix.mul_apply, Matrix.mulVec, dotProduct, selectedColumns,
    realFactorFamily, ratMatrixReal, Matrix.diagonal_apply, hk] using he

omit [Finite J] in
/-- Any enumeration of the weighted basis gives a valid rational-column
normalizer, with the same bounded-coordinate guarantee. -/
theorem rational_trial_of_basis {r : ℕ} (v : J → Fin p → ℚ) (w : J → ℚ)
    (hw : ∀ j, 0 < w j) (b : Fin r → J)
    (B : Basis (Fin r) ℝ (familySpan (realFactorFamily v)))
    (hB : ∀ i, B i = scaledFamilyVector (realFactorFamily v)
      (fun j => Real.sqrt (w j : ℝ)) (b i))
    (hcoord : ∀ j i, |B.repr (scaledFamilyVector (realFactorFamily v)
      (fun j => Real.sqrt (w j : ℝ)) j) i| ≤ 1) :
    Function.Injective (selectedColumns v b).mulVec ∧
      familySpan (fun i => realFactorFamily v (b i)) = familySpan (realFactorFamily v) ∧
      ∀ τ : Fin r → ℚ, (∀ i, τ i ^ 2 * w (b i) < 4) → ∀ j k,
        |(ratMatrixReal (normalizer (selectedColumns v b) τ) *ᵥ
          (Real.sqrt (w j : ℝ) • realFactorFamily v j)) k| < 2 := by
  classical
  let vR := realFactorFamily v
  let s : J → ℝ := fun j => Real.sqrt (w j : ℝ)
  have hs : ∀ j, s j ≠ 0 := by
    intro j
    exact (Real.sqrt_pos.mpr (by exact_mod_cast hw j)).ne'
  have hli : LinearIndependent ℝ (fun i => s (b i) • vR (b i)) := by
    have h := B.linearIndependent.map' (familySpan vR).subtype (Submodule.ker_subtype _)
    have he : (familySpan vR).subtype ∘ B = (fun i => s (b i) • vR (b i)) := by
      funext i
      exact congrArg Subtype.val (hB i)
    rw [he] at h
    exact h
  have hraw : LinearIndependent ℝ (fun i => vR (b i)) := by
    apply (LinearIndependent.units_smul_iff (fun i => vR (b i))
      (fun i => Units.mk0 (s (b i)) (hs (b i)))).mp
    exact hli
  have hVr : Function.Injective (ratMatrixReal (selectedColumns v b)).mulVec :=
    Matrix.mulVec_injective_iff.mpr hraw
  have hV := (ratMatrixReal_mulVec_injective_iff (selectedColumns v b)).mp hVr
  have hspan : familySpan (fun i => vR (b i)) = familySpan vR := by
    rw [← familySpan_smul (fun i => vR (b i)) (fun i => s (b i)) (fun i => hs (b i))]
    apply (Submodule.span_range_subtype_eq_top_iff (familySpan vR)
      (fun i => (scaledFamilyVector vR s (b i)).property)).mp
    have he : (fun i => scaledFamilyVector vR s (b i)) = B := by
      funext i; exact (hB i).symm
    change Submodule.span ℝ (Set.range (fun i => scaledFamilyVector vR s (b i))) = ⊤
    rw [he, B.span_eq]
  refine ⟨hV, hspan, ?_⟩
  intro τ hτ j k
  let T := Matrix.mulVecLin (ratMatrixReal (normalizer (selectedColumns v b) τ))
  have hc := normalized_factor_coordinate vR s b B hB T (fun i => (τ i : ℝ))
    (normalizer_selected_coordinate v b hV τ) j k
  change (ratMatrixReal (normalizer (selectedColumns v b) τ) *ᵥ
    (s j • vR j)) k = _ at hc
  rw [hc]
  exact transformed_coordinate_lt_two (by exact_mod_cast hw (b k))
    (by exact_mod_cast hτ k) (hcoord j k)

/-- The geometric maximum-volume choice is one of the actual rational-column
trials. Every weighted factor passes the strict coordinate magnitude bound. -/
theorem exists_max_volume_rational_trial (v : J → Fin p → ℚ) (w : J → ℚ)
    (hw : ∀ j, 0 < w j) :
    ∃ b : Fin (Module.finrank ℝ (familySpan (realFactorFamily v))) → J,
      Function.Injective b ∧ Function.Injective (selectedColumns v b).mulVec ∧
      familySpan (fun i => realFactorFamily v (b i)) = familySpan (realFactorFamily v) ∧
      ∀ τ : Fin (Module.finrank ℝ (familySpan (realFactorFamily v))) → ℚ,
        (∀ i, τ i ^ 2 * w (b i) < 4) → ∀ j k,
        |(ratMatrixReal (normalizer (selectedColumns v b) τ) *ᵥ
          (Real.sqrt (w j : ℝ) • realFactorFamily v j)) k| < 2 := by
  classical
  let vR := realFactorFamily v
  let s : J → ℝ := fun j => Real.sqrt (w j : ℝ)
  have hs : ∀ j, s j ≠ 0 := by
    intro j
    exact (Real.sqrt_pos.mpr (by exact_mod_cast hw j)).ne'
  obtain ⟨b, B, hb, hB, _, _, hcoord⟩ := max_volume_scaled_basis vR s hs
  exact ⟨b, hb, rational_trial_of_basis v w hw b B hB hcoord⟩

end DAGSpectral
