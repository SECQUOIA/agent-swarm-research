import QipmFormal.Coupling.LP

/-!
# LP support and Gram positivity

The active matrix is the actual restriction to active columns. Orthogonality is
expressed by the real dot product; full row rank is expressed by injectivity of
the transpose action. These are finite-dimensional Euclidean statements, without
central-path convergence or analytic-extension assumptions.
-/

namespace QipmFormal.Coupling
noncomputable section
open scoped BigOperators
open Matrix

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq n]

/-- Restriction of the constraint matrix to the active columns. -/
def activeColumns (A : Matrix m n ℝ) (B : Finset n) : Matrix m B ℝ :=
  A.submatrix id Subtype.val

omit [Fintype m] [DecidableEq n] in
/-- A feasible vector supported on the active set places its RHS in the active range. -/
theorem supported_rhs_mem_active_range (A : Matrix m n ℝ) (B : Finset n)
    (x : n → ℝ) (b : m → ℝ) (hx : ∀ i, i ∉ B → x i = 0)
    (hb : A *ᵥ x = b) : b ∈ LinearMap.range (activeColumns A B).mulVecLin := by
  refine ⟨fun i => x i, ?_⟩
  change activeColumns A B *ᵥ (fun i => x i) = b
  rw [← hb]
  ext j
  change (∑ i : B, A j i * x i) = ∑ i, A j i * x i
  rw [← Finset.sum_subtype B (fun i => Iff.rfl) (fun i => A j i * x i)]
  apply Finset.sum_subset (Finset.subset_univ B)
  intro i _ hi
  simp [hx i hi]

omit [DecidableEq n] in
/-- Positive slack paired with a nonzero nonnegative primal vector is positive. -/
theorem strict_slack_dot_pos (s x : n → ℝ) (hs : ∀ i, 0 < s i)
    (hx : ∀ i, 0 ≤ x i) (hne : x ≠ 0) : 0 < s ⬝ᵥ x := by
  obtain ⟨i, hi⟩ : ∃ i, x i ≠ 0 := by
    by_contra h
    apply hne
    ext i
    simpa using not_exists.mp h i
  apply Finset.sum_pos'
  · intro j _
    exact mul_nonneg (hs j).le (hx j)
  · exact ⟨i, Finset.mem_univ i, mul_pos (hs i) (lt_of_le_of_ne (hx i) (Ne.symm hi))⟩

omit [DecidableEq n] in
/-- An optimal nonzero primal point and a strictly feasible dual force `b ≠ 0`.
The optimal value is supplied as a zero primal-dual gap with some multiplier `yStar`.
-/
theorem rhs_ne_zero_of_strict_dual (A : Matrix m n ℝ) (x c s : n → ℝ)
    (b y yStar : m → ℝ) (hx : ∀ i, 0 ≤ x i) (hne : x ≠ 0)
    (hs : ∀ i, 0 < s i) (hprimal : A *ᵥ x = b)
    (hdual : A.transpose *ᵥ y + s = c) (hgap : c ⬝ᵥ x = yStar ⬝ᵥ b) :
    b ≠ 0 := by
  intro hb
  have hcx : c ⬝ᵥ x = 0 := by simpa [hb] using hgap
  have hax : (A.transpose *ᵥ y) ⬝ᵥ x = 0 := by
    rw [mulVec_transpose, ← dotProduct_mulVec, hprimal, hb, dotProduct_zero]
  have hpos := strict_slack_dot_pos s x hs hx hne
  rw [← hdual, add_dotProduct, hax, zero_add] at hcx
  linarith

/-- The weighted Gram quadratic form is a sum of weighted coordinate squares. -/
theorem weightedGram_dot (A : Matrix m n ℝ) (w : n → ℝ) (z : m → ℝ) :
    z ⬝ᵥ (weightedGram A w *ᵥ z) = ∑ i, w i * (A.transpose *ᵥ z) i ^ 2 := by
  unfold weightedGram
  rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_mulVec,
    ← mulVec_transpose]
  unfold dotProduct
  apply Finset.sum_congr rfl
  intro i _
  simp only [mulVec_diagonal]
  ring

/-- Positive weights give positivity wherever the transpose sees the vector. -/
theorem weightedGram_pos_of_transpose_ne_zero (A : Matrix m n ℝ) (w : n → ℝ)
    (hw : ∀ i, 0 < w i) (z : m → ℝ) (hz : A.transpose *ᵥ z ≠ 0) :
    0 < z ⬝ᵥ (weightedGram A w *ᵥ z) := by
  rw [weightedGram_dot]
  apply Finset.sum_pos'
  · intro i _
    exact mul_nonneg (hw i).le (sq_nonneg _)
  · obtain ⟨i, hi⟩ : ∃ i, (A.transpose *ᵥ z) i ≠ 0 := by
      by_contra h
      apply hz
      ext i
      simpa using not_exists.mp h i
    exact ⟨i, Finset.mem_univ i, mul_pos (hw i) (sq_pos_of_ne_zero hi)⟩

omit [DecidableEq n] in
/-- A nonzero vector in a column range cannot be killed by the transpose. -/
theorem transpose_ne_zero_on_range (A : Matrix m n ℝ) (z : m → ℝ)
    (hz : z ∈ LinearMap.range A.mulVecLin) (hne : z ≠ 0) :
    A.transpose *ᵥ z ≠ 0 := by
  obtain ⟨x, hx⟩ := hz
  change A *ᵥ x = z at hx
  intro h
  apply hne
  apply dotProduct_self_eq_zero.mp
  calc
    z ⬝ᵥ z = z ⬝ᵥ (A *ᵥ x) := by rw [hx]
    _ = (A.transpose *ᵥ z) ⬝ᵥ x := by rw [dotProduct_mulVec, mulVec_transpose]
    _ = 0 := by rw [h, zero_dotProduct]

/-- The active positive-weight Gram is positive on every nonzero active-range vector. -/
theorem weightedGram_pos_on_range (A : Matrix m n ℝ) (w : n → ℝ)
    (hw : ∀ i, 0 < w i) (z : m → ℝ)
    (hz : z ∈ LinearMap.range A.mulVecLin) (hne : z ≠ 0) :
    0 < z ⬝ᵥ (weightedGram A w *ᵥ z) :=
  weightedGram_pos_of_transpose_ne_zero A w hw z (transpose_ne_zero_on_range A z hz hne)

omit [Fintype m] in
/-- Every nonnegative weighted Gram is positive semidefinite. -/
theorem weightedGram_posSemidef [Finite m] (A : Matrix m n ℝ) (w : n → ℝ)
    (hw : ∀ i, 0 ≤ w i) : (weightedGram A w).PosSemidef := by
  simpa [weightedGram, conjTranspose_eq_transpose_of_trivial] using
    (Matrix.posSemidef_diagonal_iff.mpr hw).mul_mul_conjTranspose_same A

omit [DecidableEq n] in
/-- Orthogonality to a column range forces vanishing transpose action. -/
theorem transpose_zero_of_orthogonal_range (A : Matrix m n ℝ) (z : m → ℝ)
    (hz : ∀ u ∈ LinearMap.range A.mulVecLin, z ⬝ᵥ u = 0) :
    A.transpose *ᵥ z = 0 := by
  apply dotProduct_self_eq_zero.mp
  have h := hz (A *ᵥ (A.transpose *ᵥ z)) ⟨A.transpose *ᵥ z, rfl⟩
  simpa only [dotProduct_mulVec, ← mulVec_transpose] using h

/-- Full row rank prevents a nonzero active-orthogonal vector from being killed
by the inactive transpose. The inactive columns are exactly the complement of `B`.
-/
theorem inactive_transpose_ne_zero (A : Matrix m n ℝ) (B : Finset n)
    (hfull : Function.Injective A.transpose.mulVec) (z : m → ℝ) (hne : z ≠ 0)
    (horth : ∀ u ∈ LinearMap.range (activeColumns A B).mulVecLin, z ⬝ᵥ u = 0) :
    (activeColumns A Bᶜ).transpose *ᵥ z ≠ 0 := by
  intro hinactive
  have hactive := transpose_zero_of_orthogonal_range (activeColumns A B) z horth
  apply hne
  apply hfull
  rw [mulVec_zero]
  ext i
  by_cases hi : i ∈ B
  · exact congrFun hactive ⟨i, hi⟩
  · exact congrFun hinactive ⟨i, Finset.mem_compl.mpr hi⟩

/-- The inactive positive-weight Gram is positive on the active orthogonal complement. -/
theorem inactive_weightedGram_pos (A : Matrix m n ℝ) (B : Finset n)
    (w : ↥(Bᶜ) → ℝ) (hw : ∀ i, 0 < w i)
    (hfull : Function.Injective A.transpose.mulVec) (z : m → ℝ) (hne : z ≠ 0)
    (horth : ∀ u ∈ LinearMap.range (activeColumns A B).mulVecLin, z ⬝ᵥ u = 0) :
    0 < z ⬝ᵥ (weightedGram (activeColumns A Bᶜ) w *ᵥ z) :=
  weightedGram_pos_of_transpose_ne_zero (activeColumns A Bᶜ) w hw z
    (inactive_transpose_ne_zero A B hfull z hne horth)

omit [Fintype n] [DecidableEq n] in
/-- Independent constraint rows give the transpose injectivity used above. -/
theorem transpose_injective_of_independent_rows (A : Matrix m n ℝ)
    (hrows : LinearIndependent ℝ A.row) : Function.Injective A.transpose.mulVec := by
  exact Matrix.mulVec_injective_iff.mpr hrows

omit [Fintype m] in
/-- Restricting the Gram matrix to active columns equals zeroing inactive weights.
This identifies the restricted-column formulation with the split in `LP.lean`.
-/
theorem active_weightedGram_eq_mask (A : Matrix m n ℝ) (B : Finset n) (w : n → ℝ) :
    weightedGram (activeColumns A B) (fun i => w i) =
      weightedGram A (fun i => if i ∈ B then w i else 0) := by
  ext j k
  simp only [weightedGram, Matrix.mul_apply, Matrix.diagonal_apply, Matrix.transpose_apply,
    activeColumns, Matrix.submatrix_apply, id_eq, mul_ite, mul_zero, Finset.sum_ite_eq',
    Finset.mem_univ, if_true]
  rw [← Finset.sum_subtype B (fun i => Iff.rfl) (fun i => A j i * w i * A k i)]
  simp only [ite_mul, zero_mul]
  rw [← Finset.sum_filter]
  simp

end
end QipmFormal.Coupling
