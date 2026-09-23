import Mathlib.LinearAlgebra.Determinant
import Mathlib.LinearAlgebra.Basis.VectorSpace
import Mathlib.Data.Finset.Max
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Algebra.Order.Star.Real

/-! Maximum-volume bases of an actual finite family. The maximizing labels
are constructed by finite maximization, not supplied as an extra hypothesis. -/
namespace DAGSpectral
open Module
open scoped Matrix

variable {J V : Type*} [Finite J] [AddCommGroup V] [Module ℝ V]
  [FiniteDimensional ℝ V]

omit [Finite J] in
/-- A finite spanning family contains a labeled basis, even in dimension zero. -/
theorem exists_labeled_basis (v : J → V)
    (hspan : Submodule.span ℝ (Set.range v) = ⊤) :
    ∃ (b : Fin (Module.finrank ℝ V) → J) (B : Basis (Fin (Module.finrank ℝ V)) ℝ V),
      ∀ i, B i = v (b i) := by
  classical
  have hs : ⊤ ≤ Submodule.span ℝ (Set.range v) := hspan.ge
  let I := (linearIndepOn_empty ℝ (id : V → V)).extend (Set.empty_subset (Set.range v))
  let B₀ : Basis I ℝ V := Basis.ofSpan hs
  let := Fintype.ofFinite I
  let e : I ≃ Fin (Module.finrank ℝ V) := Fintype.equivOfCardEq (by
    rw [Fintype.card_fin, Module.finrank_eq_card_basis B₀])
  let B := B₀.reindex e
  have hv (i) : B i ∈ Set.range v := by
    apply Basis.ofSpan_subset hs
    refine ⟨e.symm i, ?_⟩
    change B₀ (e.symm i) = B₀.reindex e i
    exact (Basis.reindex_apply B₀ e i).symm
  choose b hb using hv
  exact ⟨b, B, fun i => (hb i).symm⟩

/-- A maximum-volume basis of a finite spanning family has every coordinate
of every family member bounded by one in absolute value. -/
theorem max_volume_basis_of_span (v : J → V)
    (hspan : Submodule.span ℝ (Set.range v) = ⊤) :
    ∃ (b : Fin (Module.finrank ℝ V) → J) (B : Basis (Fin (Module.finrank ℝ V)) ℝ V),
      Function.Injective b ∧ (∀ i, B i = v (b i)) ∧
      ∀ j i, |B.repr (v j) i| ≤ 1 := by
  classical
  let := Fintype.ofFinite J
  obtain ⟨b₀, E, hE⟩ := exists_labeled_basis v hspan
  let D : (Fin (Module.finrank ℝ V) → J) → ℝ := fun b => E.det (fun i => v (b i))
  have hD₀ : D b₀ = 1 := by
    change E.det _ = 1
    have he : (fun i => v (b₀ i)) = E := by funext i; exact (hE i).symm
    rw [he, E.det_self]
  obtain ⟨b, _, hmax⟩ := Finset.exists_max_image Finset.univ (fun b => |D b|)
    ⟨b₀, Finset.mem_univ _⟩
  have hDb : 0 < |D b| := by
    have hm := hmax b₀ (Finset.mem_univ _)
    rw [hD₀, abs_one] at hm
    linarith
  have hunit : IsUnit (E.det (fun i => v (b i))) :=
    isUnit_iff_ne_zero.mpr (abs_pos.mp hDb)
  obtain ⟨hli, hsp⟩ := E.is_basis_iff_det.mpr hunit
  let B := Basis.mk hli hsp.ge
  refine ⟨b, B, ?_, ?_, ?_⟩
  · intro i k hik
    exact hli.injective (congrArg v hik)
  · intro i
    exact Basis.mk_apply hli hsp.ge i
  · intro j i
    have hdet := congrArg (fun L : V →ₗ[ℝ] ℝ => L (v j))
      (E.det_smul_mk_coord_eq_det_update hli hsp.ge i)
    have hup : Function.update (fun k => v (b k)) i (v j) =
        (fun k => v (Function.update b i j k)) := by
      funext k
      by_cases hk : k = i <;> simp [hk]
    change D b * B.repr (v j) i = E.det (Function.update (fun k => v (b k)) i (v j)) at hdet
    rw [hup] at hdet
    have hm := hmax (Function.update b i j) (Finset.mem_univ _)
    change |E.det (fun k => v (Function.update b i j k))| ≤ |D b| at hm
    rw [← hdet, abs_mul] at hm
    exact (mul_le_mul_iff_right₀ hDb).mp (by simpa [mul_comm] using hm)

/-- The actual linear span of a family. -/
def familySpan (v : J → V) : Submodule ℝ V := Submodule.span ℝ (Set.range v)

/-- A family vector regarded as an element of its actual span. -/
def familyVector (v : J → V) (j : J) : familySpan v :=
  ⟨v j, Submodule.subset_span ⟨j, rfl⟩⟩

/-- Every finite vector family has a maximum-volume basis of its actual span. -/
theorem max_volume_basis (v : J → V) :
    ∃ (b : Fin (Module.finrank ℝ (familySpan v)) → J)
      (B : Basis (Fin (Module.finrank ℝ (familySpan v))) ℝ (familySpan v)),
      Function.Injective b ∧ (∀ i, B i = familyVector v (b i)) ∧
      ∀ j i, |B.repr (familyVector v j) i| ≤ 1 := by
  apply max_volume_basis_of_span
  exact (Submodule.span_range_subtype_eq_top_iff (familySpan v)
    (fun j => Submodule.subset_span ⟨j, rfl⟩)).mpr rfl

omit [Finite J] [FiniteDimensional ℝ V] in
/-- Rescaling each labeled vector by a nonzero scalar preserves the actual span. -/
theorem familySpan_smul (v : J → V) (w : J → ℝ) (hw : ∀ j, w j ≠ 0) :
    familySpan (fun j => w j • v j) = familySpan v := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨j, rfl⟩
    exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨j, rfl⟩)
  · apply Submodule.span_le.mpr
    rintro _ ⟨j, rfl⟩
    have hh := Submodule.smul_mem (familySpan (fun j => w j • v j)) (w j)⁻¹
      (Submodule.subset_span (show w j • v j ∈ Set.range (fun j => w j • v j) from ⟨j,rfl⟩))
    simpa [smul_smul, hw j] using hh

omit [Finite J] [FiniteDimensional ℝ V] in
/-- A selected basis in the span is linearly independent in the ambient space. -/
theorem basis_ambient_independent (v : J → V)
    (b : Fin (Module.finrank ℝ (familySpan v)) → J)
    (B : Basis (Fin (Module.finrank ℝ (familySpan v))) ℝ (familySpan v))
    (hB : ∀ i, B i = familyVector v (b i)) :
    LinearIndependent ℝ (fun i => v (b i)) := by
  have h := B.linearIndependent.map' (familySpan v).subtype (Submodule.ker_subtype _)
  have he : ((familySpan v).subtype ∘ B) = (fun i => v (b i)) := by
    funext i
    exact congrArg Subtype.val (hB i)
  rw [he] at h
  exact h

omit [Finite J] [FiniteDimensional ℝ V] in
/-- The selected labels span exactly the original family. -/
theorem basis_ambient_span (v : J → V)
    (b : Fin (Module.finrank ℝ (familySpan v)) → J)
    (B : Basis (Fin (Module.finrank ℝ (familySpan v))) ℝ (familySpan v))
    (hB : ∀ i, B i = familyVector v (b i)) :
    familySpan (fun i => v (b i)) = familySpan v := by
  apply (Submodule.span_range_subtype_eq_top_iff (familySpan v)
    (fun i => (familyVector v (b i)).property)).mp
  have he : (fun i => familyVector v (b i)) = B := by funext i; exact (hB i).symm
  change Submodule.span ℝ (Set.range (fun i => familyVector v (b i))) = ⊤
  rw [he, B.span_eq]

/-- A scaled factor remains in the raw factor span. -/
def scaledFamilyVector (v : J → V) (w : J → ℝ) (j : J) : familySpan v :=
  w j • familyVector v j

/-- Maximum volume after positive weighting, with raw labeled columns still
independent and spanning the original range. No maximizing tuple is assumed. -/
theorem max_volume_scaled_basis (v : J → V) (w : J → ℝ) (hw : ∀ j, w j ≠ 0) :
    ∃ (b : Fin (Module.finrank ℝ (familySpan v)) → J)
      (B : Basis (Fin (Module.finrank ℝ (familySpan v))) ℝ (familySpan v)),
      Function.Injective b ∧
      (∀ i, B i = scaledFamilyVector v w (b i)) ∧
      LinearIndependent ℝ (fun i => v (b i)) ∧
      familySpan (fun i => v (b i)) = familySpan v ∧
      ∀ j i, |B.repr (scaledFamilyVector v w j) i| ≤ 1 := by
  classical
  have hs : Submodule.span ℝ (Set.range (scaledFamilyVector v w)) = ⊤ := by
    apply (Submodule.span_range_subtype_eq_top_iff (familySpan v)
      (fun j => (scaledFamilyVector v w j).property)).mpr
    exact familySpan_smul v w hw
  obtain ⟨b, B, hb, hB, hcoord⟩ := max_volume_basis_of_span (scaledFamilyVector v w) hs
  have hli : LinearIndependent ℝ (fun i => w (b i) • v (b i)) := by
    have h := B.linearIndependent.map' (familySpan v).subtype (Submodule.ker_subtype _)
    have he : (familySpan v).subtype ∘ B = (fun i => w (b i) • v (b i)) := by
      funext i
      exact congrArg Subtype.val (hB i)
    rw [he] at h
    exact h
  have hraw : LinearIndependent ℝ (fun i => v (b i)) := by
    apply (LinearIndependent.units_smul_iff (fun i => v (b i))
      (fun i => Units.mk0 (w (b i)) (hw (b i)))).mp
    exact hli
  have hspan : familySpan (fun i => v (b i)) = familySpan v := by
    rw [← familySpan_smul (fun i => v (b i)) (fun i => w (b i)) (fun i => hw (b i))]
    apply (Submodule.span_range_subtype_eq_top_iff (familySpan v)
      (fun i => (scaledFamilyVector v w (b i)).property)).mp
    have he : (fun i => scaledFamilyVector v w (b i)) = B := by
      funext i; exact (hB i).symm
    change Submodule.span ℝ (Set.range (fun i => scaledFamilyVector v w (b i))) = ⊤
    rw [he, B.span_eq]
  exact ⟨b, B, hb, hB, hraw, hspan, hcoord⟩

/-- The dyadic weight window gives the strict transformed coordinate bound
used by the magnitude filter. -/
theorem transformed_coordinate_lt_two {w τ x : ℝ} (hw : 0 < w)
    (hτ : τ ^ 2 * w < 4) (hx : |x| ≤ 1) :
    |τ * Real.sqrt w * x| < 2 := by
  have hs : (Real.sqrt w)^2 = w := Real.sq_sqrt hw.le
  have hbase : |τ * Real.sqrt w| < 2 := by
    apply abs_lt.mpr
    have hh : (τ * Real.sqrt w)^2 < 4 := by nlinarith
    constructor <;> nlinarith [sq_nonneg (τ * Real.sqrt w - 2),
      sq_nonneg (τ * Real.sqrt w + 2)]
  rw [abs_mul]
  exact (mul_le_of_le_one_right (abs_nonneg _) hx).trans_lt hbase

omit [Finite J] in
/-- The actual factor rank cannot exceed the ambient dimension. -/
theorem family_rank_le_dimension {p : ℕ} (v : J → (Fin p → ℝ)) :
    Module.finrank ℝ (familySpan v) ≤ p := by
  simpa using (familySpan v).finrank_le

/-- Independent rectangular columns have strictly positive Gram determinant. -/
theorem gram_det_pos {p r : ℕ} (v : Fin r → (Fin p → ℝ))
    (hv : LinearIndependent ℝ v) :
    0 < Matrix.det ((Matrix.of (fun i j => v j i))ᵀ * Matrix.of (fun i j => v j i)) := by
  have hi : Function.Injective (Matrix.mulVec (fun i j => v j i)) := by
    exact Matrix.mulVec_injective_iff.mpr hv
  have hd := Matrix.PosDef.conjTranspose_mul_self (Matrix.of (fun i j => v j i)) hi
  have hp := (RCLike.pos_iff.mp hd.det_pos).1
  simpa only [RCLike.re_to_real, Matrix.conjTranspose_eq_transpose_of_trivial] using hp

omit [Finite J] [FiniteDimensional ℝ V] in
/-- A linear normalizer taking the selected raw columns to scaled coordinate
vectors acts on every weighted factor through its maximum-volume coordinates. -/
theorem normalized_factor_coordinate {r : ℕ} (v : J → V) (w : J → ℝ)
    (b : Fin r → J)
    (B : Basis (Fin r) ℝ (familySpan v))
    (hB : ∀ i, B i = scaledFamilyVector v w (b i))
    (T : V →ₗ[ℝ] (Fin r → ℝ))
    (τ : Fin r → ℝ)
    (hT : ∀ i k, T (v (b i)) k = if k = i then τ i else 0)
    (j : J) (k : Fin r) :
    T (w j • v j) k = τ k * w (b k) * B.repr (scaledFamilyVector v w j) k := by
  classical
  have hs := congrArg (fun y : familySpan v => T y.val k)
    (B.sum_repr (scaledFamilyVector v w j))
  simp only [Submodule.coe_sum, Submodule.coe_smul, map_sum, map_smul,
    Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at hs
  have hb (i) : (B i).val = w (b i) • v (b i) := congrArg Subtype.val (hB i)
  simp only [hb, map_smul, Pi.smul_apply, smul_eq_mul, hT] at hs
  simp only [mul_ite, mul_zero] at hs
  simp only [Finset.sum_ite_eq, Finset.mem_univ, ite_true] at hs
  change _ = T (w j • v j) k at hs
  rw [← hs]
  ring

omit [Finite J] [FiniteDimensional ℝ V] in
/-- A labeled basis and its coordinate bound survive any enumeration of the
same distinct labels, including the sorted enumeration used by the algorithm. -/
theorem reindex_labeled_basis {r : ℕ} (v : J → V) (b c : Fin r → J)
    (hc : Function.Injective c) (hrange : Set.range c = Set.range b)
    (B : Basis (Fin r) ℝ V) (hB : ∀ i, B i = v (b i))
    (hcoord : ∀ j i, |B.repr (v j) i| ≤ 1) :
    ∃ C : Basis (Fin r) ℝ V, (∀ i, C i = v (c i)) ∧
      ∀ j i, |C.repr (v j) i| ≤ 1 := by
  classical
  have hh (i : Fin r) : ∃ k, b k = c i := by
    have hi : c i ∈ Set.range b := hrange ▸ Set.mem_range_self i
    exact hi
  choose f hf using hh
  have hfi : Function.Injective f := by
    intro i j hij
    apply hc
    rw [← hf i, ← hf j, hij]
  let e : Fin r ≃ Fin r := Equiv.ofBijective f (Finite.injective_iff_bijective.mp hfi)
  refine ⟨B.reindex e.symm, ?_, ?_⟩
  · intro i
    rw [Basis.reindex_apply, Equiv.symm_symm, hB]
    exact congrArg v (hf i)
  · intro j i
    simpa using hcoord j (e i)

end DAGSpectral
