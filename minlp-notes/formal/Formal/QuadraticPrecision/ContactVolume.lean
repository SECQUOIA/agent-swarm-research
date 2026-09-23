import Mathlib.Topology.Instances.Matrix
import Mathlib.Topology.Order.Compact
import Formal.QuadraticPrecision.ContactNondegenerate
import Formal.NetworkSimplex.ThresholdHadamard

/-! The determinant and volume argument for indefinite quadratic contact sets. -/

open scoped BigOperators Matrix
open MeasureTheory Set
noncomputable section
namespace QuadraticPrecision

/-- Half of the symmetric matrix quadratic form. -/
def contactQuadratic {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ) (x : Fin d → ℝ) : ℝ :=
  (x ⬝ᵥ M.mulVec x) / 2

/-- A uniform entry bound gives the dimension-sharp Hadamard estimate. -/
theorem contact_det_bound {d : ℕ} (G : Matrix (Fin d) (Fin d) ℝ)
    {c : ℝ} (hc : 0 ≤ c) (hG : ∀ i j, |G i j| ≤ c) :
    |G.det| ≤ (Real.sqrt d * c) ^ d := by
  apply (NetworkSimplex.Threshold.abs_det_le_prod_column_norm G).trans
  calc
    _ ≤ ∏ _i : Fin d, (Real.sqrt d * c) := by
      apply Finset.prod_le_prod (fun _ _ => norm_nonneg _)
      intro i _
      rw [EuclideanSpace.norm_eq]
      calc
        _ ≤ Real.sqrt (∑ _j : Fin d, c ^ 2) := by
          apply Real.sqrt_le_sqrt
          apply Finset.sum_le_sum
          intro j _
          simpa only [Real.norm_eq_abs] using pow_le_pow_left₀ (abs_nonneg _) (hG j i) 2
        _ = Real.sqrt d * c := by
          simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
          rw [Real.sqrt_mul (Nat.cast_nonneg d), Real.sqrt_sq hc]
    _ = _ := by simp

/-- The columns of the simplex difference matrix. -/
def contactMatrix {d : ℕ} (o : Fin d → ℝ) (s : Fin d → Fin d → ℝ) :
    Matrix (Fin d) (Fin d) ℝ := fun i j => s j i - o i

/-- Compactness supplies a determinant-maximizing simplex with a fixed vertex. -/
theorem exists_max_contactMatrix {d : ℕ} {S : Set (Fin d → ℝ)}
    (hS : IsCompact S) (hne : S.Nonempty) (o : Fin d → ℝ) :
    ∃ s : Fin d → Fin d → ℝ, (∀ i, s i ∈ S) ∧
      ∀ t : Fin d → Fin d → ℝ, (∀ i, t i ∈ S) →
        |(contactMatrix o t).det| ≤ |(contactMatrix o s).det| := by
  let T : Set (Fin d → Fin d → ℝ) := {s | ∀ i, s i ∈ S}
  have hT : IsCompact T := isCompact_pi_infinite (fun _ => hS)
  have hnT : T.Nonempty := by
    obtain ⟨x, hx⟩ := hne
    exact ⟨fun _ => x, fun _ => hx⟩
  have hc : Continuous (fun s : Fin d → Fin d → ℝ => |(contactMatrix o s).det|) := by
    apply Continuous.abs
    apply Continuous.matrix_det
    unfold contactMatrix
    fun_prop
  obtain ⟨s, hs, hm⟩ := hT.exists_isMaxOn hnT hc.continuousOn
  exact ⟨s, hs, fun t ht => hm ht⟩

/-- Maximality bounds every coordinate in the selected simplex basis. -/
theorem contactMatrix_enclosure {d : ℕ} {S : Set (Fin d → ℝ)}
    (o : Fin d → ℝ) (s : Fin d → Fin d → ℝ) (hs : ∀ i, s i ∈ S)
    (hm : ∀ t : Fin d → Fin d → ℝ, (∀ i, t i ∈ S) →
      |(contactMatrix o t).det| ≤ |(contactMatrix o s).det|)
    (hd : (contactMatrix o s).det ≠ 0) :
    S ⊆ (fun z => o + (contactMatrix o s).mulVec z) ''
      Set.Icc (fun _ => -1) (fun _ => 1) := by
  classical
  intro x hx
  let A := contactMatrix o s
  let z := A⁻¹.mulVec (x - o)
  have hunit : IsUnit A.det := isUnit_iff_ne_zero.mpr hd
  have hAz : A.mulVec z = x - o := by
    dsimp [z]
    rw [Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv A hunit, Matrix.one_mulVec]
  have hz : ∀ j, |z j| ≤ 1 := by
    intro j
    have ht : ∀ i, Function.update s j x i ∈ S := by
      intro i
      by_cases h : i = j
      · subst i; simpa using hx
      · simpa [Function.update_of_ne h] using hs i
    have heq : contactMatrix o (Function.update s j x) = A.updateCol j (x - o) := by
      ext i k
      by_cases h : k = j <;> simp [contactMatrix, A, h]
    have hb := hm _ ht
    rw [heq, ← hAz] at hb
    have hdet : (A.updateCol j (A.mulVec z)).det = z j * A.det := by
      have hv : A.mulVec z = fun k => ∑ i, z i • A k i := by
        funext k
        simp only [Matrix.mulVec_apply, Matrix.row, dotProduct, smul_eq_mul, mul_comm]
      rw [hv, Matrix.det_updateCol_sum, smul_eq_mul]
    rw [hdet, abs_mul] at hb
    have hpos : 0 < |A.det| := abs_pos.mpr hd
    exact (mul_le_mul_iff_left₀ hpos).mp (by simpa [mul_comm] using hb)
  refine ⟨z, ⟨fun i => (abs_le.mp (hz i)).1, fun i => (abs_le.mp (hz i)).2⟩, ?_⟩
  change o + A.mulVec z = x
  rw [hAz]
  abel

/-- The parallelepiped enclosing a maximal simplex has its expected volume. -/
theorem contact_parallelepiped_volume {d : ℕ} (A : Matrix (Fin d) (Fin d) ℝ)
    (o : Fin d → ℝ) :
    volume ((fun z => o + A.mulVec z) '' Set.Icc (fun _ => -1) (fun _ => 1)) =
      ENNReal.ofReal ((2 : ℝ)^d * |A.det|) := by
  have hi : (fun z => o + A.mulVec z) '' Set.Icc (fun _ => -1) (fun _ => 1) =
      (fun z => o + z) '' (A.toLin' '' Set.Icc (fun _ => -1) (fun _ => 1)) := by
    rw [← Set.image_comp]
    rfl
  rw [hi, Set.image_add_left, measure_preimage_add, Measure.addHaar_image_linearMap,
    LinearMap.det_toLin', Real.volume_Icc_pi]
  simp only [sub_neg_eq_add, one_add_one_eq_two, Finset.prod_const, Finset.card_univ,
    Fintype.card_fin]
  rw [← ENNReal.ofReal_pow (by norm_num : (0 : ℝ) ≤ 2),
    ← ENNReal.ofReal_mul (abs_nonneg _), mul_comm]

/-- Polarization of a symmetric quadratic matrix. -/
theorem contact_polarization {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsSymm) (x y : Fin d → ℝ) :
    x ⬝ᵥ M.mulVec y = contactQuadratic M x + contactQuadratic M y -
      contactQuadratic M (x - y) := by
  have hxy : y ⬝ᵥ M.mulVec x = x ⬝ᵥ M.mulVec y := by
    simpa only [hM.eq] using (Matrix.dotProduct_transpose_mulVec M x y).symm
  simp only [contactQuadratic, Matrix.mulVec_sub, sub_dotProduct, dotProduct_sub]
  rw [hxy]
  ring

/-- Pairwise quadratic contact bounds all entries of the simplex Gram matrix. -/
theorem contact_gram_entry_bound {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsSymm) {S : Set (Fin d → ℝ)} {δ : ℝ}
    (hcontact : ∀ x ∈ S, ∀ y ∈ S, |contactQuadratic M (x - y)| ≤ δ)
    (o : Fin d → ℝ) (ho : o ∈ S) (s : Fin d → Fin d → ℝ)
    (hs : ∀ i, s i ∈ S) (i j : Fin d) :
    |((contactMatrix o s)ᵀ * M * contactMatrix o s) i j| ≤ 3 * δ := by
  have he : ((contactMatrix o s)ᵀ * M * contactMatrix o s) i j =
      (s i - o) ⬝ᵥ M.mulVec (s j - o) := by
    simp only [Matrix.mul_apply, Matrix.transpose_apply, contactMatrix,
      Matrix.mulVec, dotProduct, Pi.sub_apply, Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro k _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro l _
    ring
  rw [he, contact_polarization M hM]
  have hsub : s i - o - (s j - o) = s i - s j := by abel
  rw [hsub]
  calc
    _ ≤ |contactQuadratic M (s i - o)| + |contactQuadratic M (s j - o)| +
        |contactQuadratic M (s i - s j)| := (abs_sub _ _).trans
          (add_le_add (abs_add_le _ _) le_rfl)
    _ ≤ δ + δ + δ := add_le_add (add_le_add (hcontact _ (hs i) _ ho)
      (hcontact _ (hs j) _ ho)) (hcontact _ (hs i) _ (hs j))
    _ = 3 * δ := by ring

/-- The Gram determinant controls the volume of the selected simplex. -/
theorem contact_simplex_det_bound {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsSymm) (hdet : M.det ≠ 0) {S : Set (Fin d → ℝ)} {δ : ℝ}
    (hδ : 0 ≤ δ)
    (hcontact : ∀ x ∈ S, ∀ y ∈ S, |contactQuadratic M (x - y)| ≤ δ)
    (o : Fin d → ℝ) (ho : o ∈ S) (s : Fin d → Fin d → ℝ)
    (hs : ∀ i, s i ∈ S) :
    |(contactMatrix o s).det| ≤
      (3 * Real.sqrt d * δ) ^ ((d : ℝ) / 2) / Real.sqrt |M.det| := by
  let A := contactMatrix o s
  have hg := contact_det_bound (Aᵀ * M * A) (mul_nonneg (by norm_num) hδ)
    (contact_gram_entry_bound M hM hcontact o ho s hs)
  have he : |(Aᵀ * M * A).det| = |A.det| ^ 2 * |M.det| := by
    rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose, abs_mul, abs_mul]
    ring
  rw [he] at hg
  have hh := Real.sqrt_le_sqrt hg
  rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (abs_nonneg _)] at hh
  have hr : Real.sqrt ((Real.sqrt d * (3 * δ)) ^ d) =
      (3 * Real.sqrt d * δ) ^ ((d : ℝ) / 2) := by
    have hn : 0 ≤ Real.sqrt d * (3 * δ) := by positivity
    rw [Real.sqrt_eq_rpow, ← Real.rpow_natCast, ← Real.rpow_mul hn]
    congr 1 <;> ring
  rw [hr] at hh
  exact (le_div_iff₀ (Real.sqrt_pos.mpr (abs_pos.mpr hdet))).mpr hh

/-- Exact indefinite-contact volume estimate, including empty sets, zero tolerance,
and dimension zero. Compactness is used to obtain the maximizing simplex. -/
theorem contact_volume_bound {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsSymm) (hdet : M.det ≠ 0) {S : Set (Fin d → ℝ)}
    (hS : IsCompact S) {δ : ℝ} (hδ : 0 ≤ δ)
    (hcontact : ∀ x ∈ S, ∀ y ∈ S, |contactQuadratic M (x - y)| ≤ δ) :
    volume S ≤ ENNReal.ofReal
      ((2 : ℝ)^d * (3 * Real.sqrt d * δ) ^ ((d : ℝ) / 2) / Real.sqrt |M.det|) := by
  classical
  by_cases hz : volume S = 0
  · rw [hz]
    exact zero_le
  have hne : S.Nonempty := by
    by_contra h
    exact hz (by simp [Set.not_nonempty_iff_eq_empty.mp h])
  obtain ⟨o, ho⟩ := hne
  obtain ⟨s, hs, hm⟩ := exists_max_contactMatrix hS ⟨o, ho⟩ o
  obtain ⟨t, ht⟩ := exists_nondegenerate_contacts hz o
  have hd : (contactMatrix o s).det ≠ 0 := by
    have hp := abs_pos.mpr ht
    have hle := hm (fun i => (t i).val) (fun i => (t i).property)
    exact abs_pos.mp (hp.trans_le hle)
  calc
    volume S ≤ volume ((fun z => o + (contactMatrix o s).mulVec z) ''
        Set.Icc (fun _ => -1) (fun _ => 1)) :=
      measure_mono (contactMatrix_enclosure o s hs hm hd)
    _ = ENNReal.ofReal ((2 : ℝ)^d * |(contactMatrix o s).det|) :=
      contact_parallelepiped_volume _ _
    _ ≤ ENNReal.ofReal
        ((2 : ℝ)^d * ((3 * Real.sqrt d * δ) ^ ((d : ℝ) / 2) / Real.sqrt |M.det|)) :=
      ENNReal.ofReal_le_ofReal (mul_le_mul_of_nonneg_left
        (contact_simplex_det_bound M hM hdet hδ hcontact o ho s hs) (by positivity))
    _ = _ := by rw [mul_div_assoc]

end QuadraticPrecision
