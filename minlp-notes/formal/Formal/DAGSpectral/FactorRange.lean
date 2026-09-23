import Formal.DAGSpectral.LabeledFactors
import Formal.DAGSpectral.PSDAlgebra
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Rank

/-! The range of a positive rank-one sum is exactly the span of its columns.
Square roots occur only in this geometric proof, not in the rational producer. -/
namespace DAGSpectral
open Matrix
open scoped BigOperators
noncomputable section

variable {n : ℕ} {K : Type*} [Fintype K]

def rankOneSum (w : K → ℝ) (v : K → Fin n → ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => ∑ k, w k * v k i * v k j

private def sqrtFactorMatrix (w : K → ℝ) (v : K → Fin n → ℝ) :
    Matrix (Fin n) K ℝ := fun i k => Real.sqrt (w k) * v k i

private theorem rankOneSum_eq_gram (w : K → ℝ) (v : K → Fin n → ℝ)
    (hw : ∀ k, 0 ≤ w k) :
    rankOneSum w v = sqrtFactorMatrix w v * (sqrtFactorMatrix w v)ᵀ := by
  ext i j
  apply Finset.sum_congr rfl
  intro k _
  dsimp [sqrtFactorMatrix,Matrix.transpose_apply]
  conv_lhs => rw [←Real.sq_sqrt (hw k)]
  ring

theorem rankOneSum_posSemidef (w : K → ℝ) (v : K → Fin n → ℝ)
    (hw : ∀ k, 0 ≤ w k) : (rankOneSum w v).PosSemidef := by
  rw [rankOneSum_eq_gram w v hw]
  simpa only [conjTranspose_eq_transpose_of_trivial] using
    Matrix.posSemidef_self_mul_conjTranspose (sqrtFactorMatrix w v)

theorem rankOneSum_kernel_iff (w : K → ℝ) (v : K → Fin n → ℝ)
    (hw : ∀ k, 0 < w k) (x : Fin n → ℝ) :
    rankOneSum w v *ᵥ x = 0 ↔ ∀ k, v k ⬝ᵥ x = 0 := by
  classical
  rw [rankOneSum_eq_gram w v (fun k => (hw k).le)]
  have hker := Matrix.ker_mulVecLin_transpose_mul_self (sqrtFactorMatrix w v)ᵀ
  rw [transpose_transpose] at hker
  have he (k : K) : ((sqrtFactorMatrix w v)ᵀ *ᵥ x) k =
      Real.sqrt (w k) * (v k ⬝ᵥ x) := by
    simp [sqrtFactorMatrix,mulVec,dotProduct,Finset.mul_sum,mul_assoc]
  have hz : (sqrtFactorMatrix w v * (sqrtFactorMatrix w v)ᵀ) *ᵥ x = 0 ↔
      (sqrtFactorMatrix w v)ᵀ *ᵥ x = 0 := by
    have hh := congrArg (fun S : Submodule ℝ (Fin n → ℝ) => x ∈ S) hker
    exact eq_iff_iff.mp hh
  rw [hz]
  constructor
  · intro h k
    have hh := congrFun h k
    rw [he] at hh
    exact (mul_eq_zero.mp hh).resolve_left (Real.sqrt_pos.mpr (hw k)).ne'
  · intro h
    funext k
    rw [he,h k,mul_zero]
    rfl

theorem rankOneSum_range (w : K → ℝ) (v : K → Fin n → ℝ)
    (hw : ∀ k, 0 < w k) :
    LinearMap.range (rankOneSum w v).mulVecLin = Submodule.span ℝ (Set.range v) := by
  classical
  let C := sqrtFactorMatrix w v
  have hgram : rankOneSum w v = C*Cᵀ := rankOneSum_eq_gram w v (fun k => (hw k).le)
  have hrange : LinearMap.range (C*Cᵀ).mulVecLin = LinearMap.range C.mulVecLin := by
    apply Submodule.eq_of_le_of_finrank_eq
    · rintro x ⟨y,rfl⟩
      exact ⟨Cᵀ *ᵥ y, by simp only [Matrix.mulVecLin_apply, Matrix.mulVec_mulVec]⟩
    · exact Matrix.rank_self_mul_transpose C
  rw [hgram,hrange,Matrix.range_mulVecLin]
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro x ⟨k,rfl⟩
    exact (Submodule.span ℝ (Set.range v)).smul_mem (Real.sqrt (w k))
      (Submodule.subset_span ⟨k,rfl⟩)
  · apply Submodule.span_le.mpr
    rintro x ⟨k,rfl⟩
    have hm := (Submodule.span ℝ (Set.range C.col)).smul_mem (Real.sqrt (w k))⁻¹
      (Submodule.subset_span (show C.col k ∈ Set.range C.col from ⟨k,rfl⟩))
    have he : (Real.sqrt (w k))⁻¹ • C.col k = v k := by
      funext i
      dsimp [C,sqrtFactorMatrix,Matrix.col]
      field_simp [(Real.sqrt_pos.mpr (hw k)).ne']
    rwa [he] at hm

theorem rankOneSum_rank (w : K → ℝ) (v : K → Fin n → ℝ) (hw : ∀ k, 0 < w k) :
    (rankOneSum w v).rank = Module.finrank ℝ (Submodule.span ℝ (Set.range v)) := by
  rw [Matrix.rank,rankOneSum_range w v hw]

/-- A PSD sum vanishes on a vector exactly when each summand does. -/
theorem psd_sum_kernel_iff (A : K → Matrix (Fin n) (Fin n) ℝ)
    (hA : ∀ k, (A k).PosSemidef) (x : Fin n → ℝ) :
    (∑ k, A k) *ᵥ x = 0 ↔ ∀ k, A k *ᵥ x = 0 := by
  constructor
  · intro hx
    have hq : ∑ k, x ⬝ᵥ (A k *ᵥ x) = 0 := by
      rw [←dotProduct_sum,←Matrix.sum_mulVec,hx,dotProduct_zero]
    have hn (k : K) : 0 ≤ x ⬝ᵥ (A k *ᵥ x) := by
      simpa only [star_trivial] using (hA k).dotProduct_mulVec_nonneg x
    have hz := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => hn k)).mp hq
    intro k
    apply ((hA k).dotProduct_mulVec_zero_iff x).mp
    simpa only [star_trivial] using hz k (Finset.mem_univ k)
  · intro h
    rw [Matrix.sum_mulVec]
    simp only [h,Finset.sum_const_zero]

/-- No cancellation is possible among positive-semidefinite summands. -/
theorem psd_sum_eq_zero_iff (A : K → Matrix (Fin n) (Fin n) ℝ)
    (hA : ∀ k, (A k).PosSemidef) :
    (∑ k, A k) = 0 ↔ ∀ k, A k = 0 := by
  constructor
  · intro h
    have ht : ∑ k, (A k).trace = 0 := by rw [←Matrix.trace_sum,h,Matrix.trace_zero]
    have hz := (Finset.sum_eq_zero_iff_of_nonneg
      (fun k _ => (hA k).trace_nonneg)).mp ht
    exact fun k => (hA k).trace_eq_zero_iff.mp (hz k (Finset.mem_univ k))
  · intro h
    simp only [h,Finset.sum_const_zero]

abbrev SelectedFactorLabel {n : ℕ} {O : Type*}
    (A : O → Matrix (Fin n) (Fin n) ℚ) (s : Finset O) :=
  {k : FactorLabel A // factorOwner k ∈ s}

theorem selected_factor_sum {O : Type*} [Fintype O] [DecidableEq O]
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) :
    (∑ o ∈ s, ratMatrixReal (A o)) =
      rankOneSum (fun k : SelectedFactorLabel A s => (factorWeight A k.val : ℝ))
        (fun k i => (factorVector A k.val i : ℝ)) := by
  classical
  ext i j
  have hr : (∑ o ∈ s, A o i j) = ∑ k : SelectedFactorLabel A s,
      factorWeight A k.val * factorVector A k.val i * factorVector A k.val j := by
    rw [factorLabel_selected_reconstruct A hA s i j]
    rw [←Finset.sum_filter]
    apply Finset.sum_subtype
    intro k
    simp
  have he := congrArg (fun t : ℚ => (t : ℝ)) hr
  push_cast at he
  simpa only [Matrix.sum_apply,Finset.sum_apply,ratMatrixReal_apply,rankOneSum] using he

/-- The actual sum of selected original matrices has exactly the factor span as its range. -/
theorem selected_factor_range {O : Type*} [Finite O]
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) :
    LinearMap.range (∑ o ∈ s, ratMatrixReal (A o)).mulVecLin =
      Submodule.span ℝ (Set.range
        (fun k : SelectedFactorLabel A s => fun i => (factorVector A k.val i : ℝ))) := by
  classical
  let := Fintype.ofFinite O
  rw [selected_factor_sum A hA s]
  apply rankOneSum_range
  intro k
  exact_mod_cast (factorLabel_positive A hA k.val).1

theorem selected_factor_rank {O : Type*} [Finite O]
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) :
    (∑ o ∈ s, ratMatrixReal (A o)).rank = Module.finrank ℝ
      (Submodule.span ℝ (Set.range
        (fun k : SelectedFactorLabel A s => fun i => (factorVector A k.val i : ℝ)))) := by
  rw [Matrix.rank,selected_factor_range A hA s]

/-- The zero-rank branch can retain exactly paths whose selected matrices are all zero. -/
theorem selected_psd_sum_eq_zero_iff {O : Type*}
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) :
    (∑ o ∈ s, ratMatrixReal (A o)) = 0 ↔ ∀ o ∈ s, A o = 0 := by
  classical
  have he : (∑ o ∈ s, ratMatrixReal (A o)) = ∑ o : s, ratMatrixReal (A o.val) := by
    exact Finset.sum_subtype s (fun _ => Iff.rfl) _
  rw [he,psd_sum_eq_zero_iff _ (fun o : s => hA o.val)]
  constructor
  · intro h o ho
    apply ratMatrixReal_injective
    simpa only [ratMatrixReal_zero] using h ⟨o,ho⟩
  · intro h o
    rw [h o.val o.property,ratMatrixReal_zero]

theorem realMatrix_rank_zero_iff (A : Matrix (Fin n) (Fin n) ℝ) : A.rank = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hr : LinearMap.range A.mulVecLin = ⊥ := Submodule.finrank_eq_zero.mp h
    have hm : A.mulVecLin = 0 := LinearMap.range_eq_bot.mp hr
    ext i j
    have he := congrFun (LinearMap.congr_fun hm (Pi.single j 1)) i
    simpa [Matrix.mulVec,dotProduct,Pi.single_apply] using he
  · rintro rfl
    exact Matrix.rank_zero

theorem selected_psd_rank_zero_iff {O : Type*}
    (A : O → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset O) :
    (∑ o ∈ s, ratMatrixReal (A o)).rank = 0 ↔ ∀ o ∈ s, A o = 0 := by
  rw [realMatrix_rank_zero_iff,selected_psd_sum_eq_zero_iff A hA s]

end
end DAGSpectral
