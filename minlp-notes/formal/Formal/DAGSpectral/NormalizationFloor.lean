import Formal.DAGSpectral.RangeNormalization
import Formal.DAGSpectral.PSDAlgebra

/-! Forced selected basis factors give an actual identity lower floor. -/
namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators MatrixOrder

/-- A selected positive rank-one sum dominates any subset of its labels. -/
theorem rankOne_sum_mono {p M : ℕ} (v : Fin M → Fin p → ℝ) (w : Fin M → ℝ)
    (s t : Finset (Fin M)) (hst : s ⊆ t) (hw : ∀ k ∈ t, 0 ≤ w k) :
    Loewner (∑ k ∈ s, w k • vecMulVec (v k) (v k))
      (∑ k ∈ t, w k • vecMulVec (v k) (v k)) := by
  change (∑ k ∈ s, w k • vecMulVec (v k) (v k)) ≤
    (∑ k ∈ t, w k • vecMulVec (v k) (v k))
  apply Finset.sum_le_sum_of_subset_of_nonneg hst
  intro k hk _
  have hp : (vecMulVec (v k) (v k)).PosSemidef := by
    simpa using posSemidef_vecMulVec_self_star (v k)
  exact (hp.smul (hw k hk)).nonneg

/-- A weighted coordinate basis with diagonal masses at least one dominates I. -/
theorem coordinate_basis_floor {r : ℕ} (τ w : Fin r → ℝ)
    (hf : ∀ i, 1 ≤ τ i ^ 2 * w i) :
    Loewner 1 (∑ k, w k • vecMulVec
      (fun i => if i = k then τ k else 0) (fun i => if i = k then τ k else 0)) := by
  have he : (∑ k, w k • vecMulVec
      (fun i => if i = k then τ k else 0) (fun i => if i = k then τ k else 0)) =
      diagonal (fun i => τ i ^ 2 * w i) := by
    ext i j
    simp only [Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul, vecMulVec_apply, diagonal_apply]
    by_cases hij : i = j
    · subst j
      simp only [ite_mul, zero_mul, mul_ite, mul_zero, if_true]
      rw [Finset.sum_eq_single i]
      · simp; ring
      · intro k _ hk; simp [Ne.symm hk]
      · simp
    · apply Eq.trans ?_ (if_neg hij).symm
      apply Finset.sum_eq_zero
      intro k _
      by_cases hi : i = k <;> by_cases hj : j = k <;> simp_all
  rw [he]
  unfold Loewner
  rw [← diagonal_one, diagonal_sub]
  exact Matrix.posSemidef_diagonal_iff.mpr (fun i => sub_nonneg.mpr (hf i))

/-- An actual normalizer maps every selected column to its scaled coordinate vector. -/
theorem normalizer_column {p M r : ℕ} (u : Fin M → Fin p → ℚ)
    (b : Fin r → Fin M) (τ : Fin r → ℚ)
    (hV : Function.Injective (Matrix.mulVec (Matrix.of fun i j => u (b j) i)))
    (j : Fin r) :
    normalizer (Matrix.of fun i j => u (b j) i) τ *ᵥ u (b j) =
      fun i => if i = j then τ j else 0 := by
  have he := normalizer_mul_columns (Matrix.of fun i j => u (b j) i) hV τ
  funext i
  have hij := congrFun (congrFun he i) j
  simp only [Matrix.mul_apply, Matrix.of_apply, diagonal_apply] at hij
  change (∑ k, normalizer (Matrix.of fun i j => u (b j) i) τ i k * u (b j) k) = _
  rw [hij]
  split_ifs with h
  · subst j; rfl
  · rfl

/-- Congruence transforms a weighted rank-one sum factor by factor. -/
theorem rankOne_sum_congruence {p r M : ℕ} (T : Matrix (Fin r) (Fin p) ℝ)
    (u : Fin M → Fin p → ℝ) (w : Fin M → ℝ) (s : Finset (Fin M)) :
    T * (∑ k ∈ s, w k • vecMulVec (u k) (u k)) * Tᵀ =
      ∑ k ∈ s, w k • vecMulVec (T *ᵥ u k) (T *ᵥ u k) := by
  simp only [Matrix.mul_sum, Matrix.sum_mul, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_vecMulVec, Matrix.vecMulVec_mul, Matrix.vecMul_transpose]

theorem ratMatrixReal_rankOne_sum {p M : ℕ} (u : Fin M → Fin p → ℚ)
    (w : Fin M → ℚ) (s : Finset (Fin M)) :
    ratMatrixReal (∑ k ∈ s, w k • vecMulVec (u k) (u k)) =
      ∑ k ∈ s, (w k : ℝ) • vecMulVec (fun i => (u k i : ℝ))
        (fun i => (u k i : ℝ)) := by
  ext i j
  simp only [ratMatrixReal_apply, Matrix.sum_apply, Matrix.smul_apply,
    smul_eq_mul, vecMulVec_apply]
  push_cast
  rfl

/-- Every selected collection containing the basis labels has normalized sum at least I.
The matrix T is the actual rational Gram-inverse normalizer. -/
theorem normalization_forced_floor {p M r : ℕ} (u : Fin M → Fin p → ℚ)
    (w : Fin M → ℚ) (s : Finset (Fin M)) (b : Fin r → Fin M)
    (hb : Function.Injective b) (hbs : ∀ i, b i ∈ s)
    (hV : Function.Injective (Matrix.mulVec (Matrix.of fun i j => u (b j) i)))
    (τ : Fin r → ℚ) (hf : ∀ i, 1 ≤ τ i ^ 2 * w (b i))
    (hw : ∀ k ∈ s, 0 ≤ w k) :
    Loewner 1 (ratMatrixReal
      (normalizer (Matrix.of fun i j => u (b j) i) τ *
        (∑ k ∈ s, w k • vecMulVec (u k) (u k)) *
          (normalizer (Matrix.of fun i j => u (b j) i) τ)ᵀ)) := by
  let T := ratMatrixReal (normalizer (Matrix.of fun i j => u (b j) i) τ)
  let v : Fin M → Fin p → ℝ := fun k i => (u k i : ℝ)
  let a : Fin M → ℝ := fun k => (w k : ℝ)
  have hsub : Finset.univ.image b ⊆ s := by
    intro k hk
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hk
    exact hbs j
  have hmono := (rankOne_sum_mono v a _ s hsub
    (fun k hk => by dsimp [a]; exact_mod_cast hw k hk)).congruence T
  have hbas : T * (∑ k ∈ Finset.univ.image b, a k • vecMulVec (v k) (v k)) * Tᵀ =
      ∑ j, (w (b j) : ℝ) • vecMulVec
        (fun i => if i = j then (τ j : ℝ) else 0)
        (fun i => if i = j then (τ j : ℝ) else 0) := by
    rw [rankOne_sum_congruence, Finset.sum_image (by intro i _ j _ h; exact hb h)]
    apply Finset.sum_congr rfl
    intro j _
    have he : T *ᵥ v (b j) = fun i => if i = j then (τ j : ℝ) else 0 := by
      dsimp [T, v]
      rw [ratMatrixReal_mulVec, normalizer_column u b τ hV j]
      funext i
      split_ifs with hij <;> simp [hij]
    rw [he]
  rw [hbas] at hmono
  have hfloor := coordinate_basis_floor (fun i => (τ i : ℝ))
    (fun i => (w (b i) : ℝ)) (fun i => by exact_mod_cast hf i)
  have ht := hfloor.trans hmono
  simpa only [ratMatrixReal_mul, ratMatrixReal_transpose,
    ratMatrixReal_rankOne_sum] using ht

end
end DAGSpectral
