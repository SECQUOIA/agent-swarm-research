import Formal.MatroidSpectral.Representation
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.LinearIndependent.Lemmas

/-! Determinant-tested row selection for an arbitrary rational representation. -/
namespace MatroidSpectral
open Matrix
open scoped BigOperators

def rowRestriction {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    Matrix S (Fin m) ℚ := fun i j => A i j

def rowGram {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    Matrix S S ℚ := rowRestriction A S * (rowRestriction A S).transpose

theorem rowGram_det_ne_zero_iff {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) :
    (rowGram A S).det ≠ 0 ↔ LinearIndepOn ℚ A.row (S : Set (Fin a)) := by
  classical
  rw [← isUnit_iff_ne_zero, ← Matrix.isUnit_iff_isUnit_det,
    ← Matrix.linearIndependent_rows_iff_isUnit,
    linearIndependent_iff_card_eq_finrank_span, Set.finrank,
    ← Matrix.rank_eq_finrank_span_row, rowGram, Matrix.rank_self_mul_transpose,
    Matrix.rank_eq_finrank_span_row]
  change Fintype.card S = Set.finrank ℚ (Set.range (rowRestriction A S).row) ↔ _
  rw [← linearIndependent_iff_card_eq_finrank_span]
  rfl

def rowSpan {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    Submodule ℚ (Fin m → ℚ) := Submodule.span ℚ (A.row '' (S : Set (Fin a)))

theorem rowSpan_insert {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i : Fin a) :
    rowSpan A (insert i S) = Submodule.span ℚ (insert (A i) (A.row '' (S : Set (Fin a)))) := by
  change Submodule.span ℚ (A.row '' (↑(insert i S) : Set (Fin a))) =
    Submodule.span ℚ (insert (A.row i) (A.row '' (S : Set (Fin a))))
  rw [Finset.coe_insert, Set.image_insert_eq]

theorem rejected_row_mem_span {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i : Fin a)
    (hS : LinearIndepOn ℚ A.row (S : Set (Fin a)))
    (h : (rowGram A (insert i S)).det = 0) : A i ∈ rowSpan A S := by
  classical
  by_cases hi : i ∈ S
  · exact Submodule.subset_span (Set.mem_image_of_mem A.row hi)
  · by_contra hmem
    have hind : LinearIndepOn ℚ A.row ((insert i S : Finset (Fin a)) : Set (Fin a)) := by
      rw [Finset.coe_insert, linearIndepOn_insert hi]
      exact ⟨hS, hmem⟩
    exact (rowGram_det_ne_zero_iff A (insert i S)).mpr hind h

/-- A single reverse scan; every decision is a rational Gram determinant test. -/
noncomputable def selectRows {a m : ℕ} (A : RationalRepresentation a m) :
    List (Fin a) → Finset (Fin a)
  | [] => ∅
  | i :: is =>
      let S := selectRows A is
      if (rowGram A (insert i S)).det ≠ 0 then insert i S else S

theorem selectRows_independent {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) :
    LinearIndepOn ℚ A.row (selectRows A rows : Set (Fin a)) := by
  classical
  induction rows with
  | nil => simp [selectRows, LinearIndepOn]
  | cons i is ih =>
      simp only [selectRows]
      split_ifs with h
      · exact (rowGram_det_ne_zero_iff A _).mp h
      · exact ih

theorem selectRows_subset {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : selectRows A rows ⊆ rows.toFinset := by
  classical
  induction rows with
  | nil => simp [selectRows]
  | cons i is ih =>
      simp only [selectRows, List.toFinset_cons]
      split_ifs
      · exact Finset.insert_subset_insert i ih
      · exact ih.trans (Finset.subset_insert _ _)

theorem selectRows_span {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : rowSpan A (selectRows A rows) = rowSpan A rows.toFinset := by
  classical
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp only [selectRows, List.toFinset_cons]
      by_cases h : (rowGram A (insert i (selectRows A is))).det ≠ 0
      · rw [if_pos h, rowSpan_insert, rowSpan_insert,
          Submodule.span_insert, Submodule.span_insert]
        exact congrArg (fun P => Submodule.span ℚ {A i} ⊔ P) ih
      · rw [if_neg h]
        have hm := rejected_row_mem_span A (selectRows A is) i
          (selectRows_independent A is) (not_ne_iff.mp h)
        have he : rowSpan A (insert i (selectRows A is)) = rowSpan A (selectRows A is) := by
          rw [rowSpan_insert, Submodule.span_insert_eq_span hm]
          rfl
        calc
          rowSpan A (selectRows A is) = rowSpan A (insert i (selectRows A is)) := he.symm
          _ = rowSpan A (insert i is.toFinset) := by
            rw [rowSpan_insert, rowSpan_insert, Submodule.span_insert, Submodule.span_insert]
            exact congrArg (fun P => Submodule.span ℚ {A i} ⊔ P) ih

noncomputable def independentRows {a m : ℕ} (A : RationalRepresentation a m) :
    Finset (Fin a) := selectRows A (List.finRange a)

theorem independentRows_independent {a m : ℕ} (A : RationalRepresentation a m) :
    LinearIndepOn ℚ A.row (independentRows A : Set (Fin a)) := selectRows_independent A _

theorem independentRows_span {a m : ℕ} (A : RationalRepresentation a m) :
    rowSpan A (independentRows A) = Submodule.span ℚ (Set.range A.row) := by
  rw [independentRows, selectRows_span]
  simp [rowSpan, Set.image_univ]

noncomputable def reducedRepresentation {a m : ℕ} (A : RationalRepresentation a m) :
    RationalRepresentation (independentRows A).card m :=
  A.submatrix ((independentRows A).orderEmbOfFin rfl) id

theorem reducedRepresentation_independent {a m : ℕ} (A : RationalRepresentation a m) :
    LinearIndependent ℚ (reducedRepresentation A).row := by
  have h := (independentRows_independent A).comp
    ((independentRows A).orderIsoOfFin rfl) ((independentRows A).orderIsoOfFin rfl).injective
  exact h

theorem independentRows_card {a m : ℕ} (A : RationalRepresentation a m) :
    (independentRows A).card = A.rank := by
  have h := linearIndependent_iff_card_eq_finrank_span.mp (independentRows_independent A)
  have hr : Set.range (fun i : independentRows A => A.row i) =
      A.row '' (independentRows A : Set (Fin a)) := by
    ext x
    simp
  change Fintype.card (independentRows A) =
    Module.finrank ℚ (Submodule.span ℚ (Set.range (fun i : independentRows A => A.row i))) at h
  rw [hr] at h
  change Fintype.card (independentRows A) = Module.finrank ℚ (rowSpan A (independentRows A)) at h
  rw [independentRows_span, ← Matrix.rank_eq_finrank_span_row] at h
  simpa using h

/-- Every linear dependence among any selected columns is preserved by row reduction. -/
theorem reducedRepresentation_mulVec_eq_zero_iff {a m k : ℕ}
    (A : RationalRepresentation a m) (b : Fin k → Fin m) (x : Fin k → ℚ) :
    ((reducedRepresentation A).submatrix id b) *ᵥ x = 0 ↔
      (A.submatrix id b) *ᵥ x = 0 := by
  classical
  constructor
  · intro hx
    let L : (Fin m → ℚ) →ₗ[ℚ] ℚ :=
      { toFun := fun v => ∑ j, v (b j) * x j
        map_add' := by intro v w; simp [add_mul, Finset.sum_add_distrib]
        map_smul' := by intro c v; simp [Finset.mul_sum, mul_assoc] }
    have hs : rowSpan A (independentRows A) ≤ LinearMap.ker L := by
      apply Submodule.span_le.mpr
      rintro _ ⟨i, hi, rfl⟩
      let j := (independentRows A).orderIsoOfFin rfl |>.symm ⟨i, hi⟩
      have he : (independentRows A).orderEmbOfFin rfl j = i := by
        change ↑((independentRows A).orderIsoOfFin rfl
          (((independentRows A).orderIsoOfFin rfl).symm ⟨i, hi⟩)) = i
        simp
      have hh := congrFun hx j
      simpa [LinearMap.mem_ker, L, Matrix.mulVec, dotProduct,
        reducedRepresentation, Matrix.submatrix, he, Matrix.row] using hh
    funext i
    have hi : A.row i ∈ rowSpan A (independentRows A) := by
      rw [independentRows_span]
      exact Submodule.subset_span (Set.mem_range_self i)
    have hz := hs hi
    simpa [LinearMap.mem_ker, L, Matrix.mulVec, dotProduct, Matrix.submatrix, Matrix.row] using hz
  · intro hx
    funext i
    have h := congrFun hx ((independentRows A).orderEmbOfFin rfl i)
    simpa [reducedRepresentation, Matrix.mulVec, dotProduct, Matrix.submatrix] using h

theorem reducedRepresentation_columnIndependent_iff {a m k : ℕ}
    (A : RationalRepresentation a m) (b : Fin k → Fin m) :
    LinearIndependent ℚ ((reducedRepresentation A).submatrix id b).col ↔
      LinearIndependent ℚ (A.submatrix id b).col := by
  have hker : LinearMap.ker ((reducedRepresentation A).submatrix id b).mulVecLin =
      LinearMap.ker (A.submatrix id b).mulVecLin := by
    ext x
    simp only [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact reducedRepresentation_mulVec_eq_zero_iff A b x
  rw [← Matrix.mulVec_injective_iff, ← Matrix.mulVec_injective_iff]
  change Function.Injective ((reducedRepresentation A).submatrix id b).mulVecLin ↔
    Function.Injective (A.submatrix id b).mulVecLin
  rw [← LinearMap.ker_eq_bot, ← LinearMap.ker_eq_bot, hker]

def ColumnIndependent {a m : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) : Prop := LinearIndependent ℚ (fun j : B => A.col j)

/-- Bases of a rectangular rational representation use its actual matrix rank. -/
def IsColumnBase {a m : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) : Prop := B.card = A.rank ∧ ColumnIndependent A B

theorem isColumnBase_of_span_eq {a m : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) (hi : ColumnIndependent A B)
    (hs : Submodule.span ℚ (Set.range (fun j : B => A.col j)) =
      Submodule.span ℚ (Set.range A.col)) : IsColumnBase A B := by
  refine ⟨?_, hi⟩
  have hc := linearIndependent_iff_card_eq_finrank_span.mp hi
  change Fintype.card B = Module.finrank ℚ
    (Submodule.span ℚ (Set.range (fun j : B => A.col j))) at hc
  rw [hs, ← Matrix.rank_eq_finrank_span_cols] at hc
  simpa using hc

theorem isColumnBase_iff_span {a m : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) : IsColumnBase A B ↔
      ColumnIndependent A B ∧
      Submodule.span ℚ (Set.range (fun j : B => A.col j)) =
        Submodule.span ℚ (Set.range A.col) := by
  constructor
  · rintro ⟨hc, hi⟩
    refine ⟨hi, Submodule.eq_of_le_of_finrank_eq ?_ ?_⟩
    · apply Submodule.span_mono
      rintro _ ⟨j, rfl⟩
      exact Set.mem_range_self (j : Fin m)
    · have hh := linearIndependent_iff_card_eq_finrank_span.mp hi
      change Fintype.card B = Module.finrank ℚ
        (Submodule.span ℚ (Set.range (fun j : B => A.col j))) at hh
      rw [← hh, ← Matrix.rank_eq_finrank_span_cols]
      simpa using hc
  · rintro ⟨hi, hs⟩
    exact isColumnBase_of_span_eq A B hi hs

theorem columnIndependent_iff_ordered {a m k : ℕ} (A : RationalRepresentation a m)
    (B : Finset (Fin m)) (hB : B.card = k) :
    ColumnIndependent A B ↔ LinearIndependent ℚ (A.submatrix id (B.orderEmbOfFin hB)).col := by
  exact (linearIndependent_equiv (B.orderIsoOfFin hB).toEquiv).symm

theorem reducedRepresentation_independent_iff {a m : ℕ}
    (A : RationalRepresentation a m) (B : Finset (Fin m)) :
    ColumnIndependent (reducedRepresentation A) B ↔ ColumnIndependent A B := by
  rw [columnIndependent_iff_ordered _ _ rfl, columnIndependent_iff_ordered _ _ rfl]
  exact reducedRepresentation_columnIndependent_iff A _

/-- The determinant bases after preprocessing are precisely the original column bases. -/
theorem reducedRepresentation_isBase_iff {a m : ℕ}
    (A : RationalRepresentation a m) (B : Finset (Fin m)) :
    IsBase (reducedRepresentation A) B ↔ IsColumnBase A B := by
  constructor
  · intro h
    refine ⟨h.card.trans (independentRows_card A), ?_⟩
    rw [← reducedRepresentation_independent_iff, columnIndependent_iff_ordered _ _ h.card]
    exact Matrix.linearIndependent_cols_of_det_ne_zero ((isBase_iff h.card).mp h)
  · rintro ⟨hc, hi⟩
    have hc' : B.card = (independentRows A).card := hc.trans (independentRows_card A).symm
    rw [isBase_iff hc']
    rw [← reducedRepresentation_independent_iff, columnIndependent_iff_ordered _ _ hc'] at hi
    exact isUnit_iff_ne_zero.mp ((Matrix.isUnit_iff_isUnit_det _).mp
      (Matrix.linearIndependent_cols_iff_isUnit.mp hi))

/-- Scanning the transposed representation constructs an original column base. -/
theorem independentRows_transpose_isColumnBase {a m : ℕ} (A : RationalRepresentation a m) :
    IsColumnBase A (independentRows A.transpose) := by
  refine ⟨?_, ?_⟩
  · rw [independentRows_card, Matrix.rank_transpose]
  · exact independentRows_independent A.transpose

theorem reducedRepresentation_bases_nonempty {a m : ℕ} (A : RationalRepresentation a m) :
    (bases (reducedRepresentation A)).Nonempty := by
  refine ⟨independentRows A.transpose, mem_bases.mpr ?_⟩
  exact (reducedRepresentation_isBase_iff A _).mpr (independentRows_transpose_isColumnBase A)

/-- The exact sequence of row-set determinant queries made by the scan. -/
noncomputable def rowQueries {a m : ℕ} (A : RationalRepresentation a m) :
    List (Fin a) → List (Finset (Fin a))
  | [] => []
  | i :: is => rowQueries A is ++ [insert i (selectRows A is)]

@[simp] theorem rowQueries_length {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : (rowQueries A rows).length = rows.length := by
  induction rows with
  | nil => rfl
  | cons i is ih => simp [rowQueries, ih]

theorem rowQueries_card_le {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) (S : Finset (Fin a)) (_h : S ∈ rowQueries A rows) :
    S.card ≤ a := by
  simpa using Finset.card_le_univ S

@[simp] theorem independentRows_queries {a m : ℕ} (A : RationalRepresentation a m) :
    (rowQueries A (List.finRange a)).length = a := by simp

end MatroidSpectral
