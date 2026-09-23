import Formal.QuadraticPrecision.PrincipalMinor
import Formal.QuadraticPrecision.LowerNegativeSlice
import Formal.QuadraticPrecision.LowerDeterminant

open scoped BigOperators Matrix
open Matrix MeasureTheory
namespace QuadraticPrecision

/-- Coordinate inclusion matrix for a selected list of distinct coordinates. -/
noncomputable def coordinateMatrix {n d : ℕ} (f : Fin d → Fin n) : Matrix (Fin n) (Fin d) ℝ :=
  fun i j => if i = f j then 1 else 0

theorem coordinateMatrix_apply {n d : ℕ} (f : Fin d → Fin n) (hf : Function.Injective f)
    (x : Input d) (j : Fin d) : (coordinateMatrix f *ᵥ x) (f j) = x j := by
  classical
  simp [coordinateMatrix, mulVec, dotProduct, hf.eq_iff]

theorem coordinateMatrix_apply_outside {n d : ℕ} (f : Fin d → Fin n)
    (x : Input d) (i : Fin n) (hi : i ∉ Set.range f) :
    (coordinateMatrix f *ᵥ x) i = 0 := by
  classical
  have hn (j) : i ≠ f j := by intro h; exact hi ⟨j, h.symm⟩
  simp [coordinateMatrix, mulVec, dotProduct, hn]

theorem coordinateMatrix_hessian {n d : ℕ} (H : Matrix (Fin n) (Fin n) ℝ)
    (f : Fin d → Fin n) :
    (coordinateMatrix f)ᵀ * H * coordinateMatrix f = H.submatrix f f := by
  classical
  ext i j
  simp [coordinateMatrix, Matrix.mul_apply, Matrix.transpose_apply, Matrix.submatrix,
    mul_ite]

/-- Restricting selected coordinates preserves the integer dimension and
produces the actual corresponding principal Hessian. -/
theorem graph_principal_pullback {n d p : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (a l u : Input n) (b ε : ℝ)
    (hlu : ∀ i, l i ≤ u i) (f : Fin d → Fin n) (hf : Function.Injective f)
    (h : HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p) :
    ∃ a' : Input d, ∃ b' : ℝ,
      HasGraphLift (Set.Icc (0 : Input d) (fun j => u (f j)-l (f j)))
        (quadraticPolynomial (H.submatrix f f) a' b') ε p := by
  classical
  let T := coordinateMatrix f
  let A : Input d →ᵃ[ℝ] Input n :=
    (Matrix.mulVecLin T).toAffineMap + AffineMap.const ℝ _ l
  have hA (x) : A x = l + T *ᵥ x := by simp [A, add_comm]
  have hbox : ∀ x ∈ Set.Icc (0 : Input d) (fun j => u (f j)-l (f j)),
      A x ∈ Set.Icc l u := by
    intro x hx
    constructor <;> intro i
    · by_cases hi : i ∈ Set.range f
      · obtain ⟨j, rfl⟩ := hi
        simp only [hA, Pi.add_apply, T, coordinateMatrix_apply f hf]
        have hh := hx.1 j
        change 0 ≤ x j at hh
        linarith
      · simp [hA, T, coordinateMatrix_apply_outside f x i hi]
    · by_cases hi : i ∈ Set.range f
      · obtain ⟨j, rfl⟩ := hi
        simp only [hA, Pi.add_apply, T, coordinateMatrix_apply f hf]
        have hh := hx.2 j
        linarith
      · simpa [hA, T, coordinateMatrix_apply_outside f x i hi] using hlu i
  have hp := h.pullback A _ (convex_Icc _ _) hbox
  refine ⟨(1/2:ℝ) • ((l ᵥ* H + H *ᵥ l) ᵥ* T) + a ᵥ* T,
    quadraticPolynomial H a b l, ?_⟩
  convert hp using 1
  funext x
  simp only [Function.comp_apply, hA, quadraticPolynomial_affine,
    T, coordinateMatrix_hessian]

/-- A nonsingular rank-sized principal minor indexed by an actual finite
coordinate inclusion. -/
theorem exists_principal_coordinate_rank {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian) :
    ∃ f : Fin H.rank → Fin n, Function.Injective f ∧ (H.submatrix f f).det ≠ 0 := by
  classical
  obtain ⟨s, hs, hdet⟩ := exists_principal_minor_rank H hH
  let e : Fin H.rank ≃ s :=
    (Fintype.equivOfCardEq (by simp only [Fintype.card_fin, Fintype.card_coe]; exact hs.symm))
  refine ⟨fun j => (e j).val, Subtype.val_injective.comp e.injective, ?_⟩
  have he := Matrix.det_submatrix_equiv_self e
    (H.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n))
  exact (show (H.submatrix (fun j => (e j).val) (fun j => (e j).val)).det =
    (H.submatrix (Subtype.val : s → Fin n) (Subtype.val : s → Fin n)).det from he) ▸ hdet

/-- The coefficient for any chosen nonsingular principal coordinate minor. -/
noncomputable def principalErrorConstant {n d : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (l u : Input n) (f : Fin d → Fin n) : ℝ :=
  determinantErrorConstant d |(H.submatrix f f).det| (∏ j, (u (f j)-l (f j)))

theorem principalErrorConstant_pos {n d : ℕ} (hd : 0 < d)
    (H : Matrix (Fin n) (Fin n) ℝ) (l u : Input n) (hlu : ∀ i, l i < u i)
    (f : Fin d → Fin n) (hdet : (H.submatrix f f).det ≠ 0) :
    0 < principalErrorConstant H l u f :=
  determinantErrorConstant_pos hd (abs_pos.mpr hdet)
    (Finset.prod_pos fun j _ => sub_pos.mpr (hlu (f j)))

theorem graph_principal_log_lower {n d p : ℕ} (hd : 0 < d)
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b ε : ℝ) (hlu : ∀ i, l i < u i) (hε : 0 < ε)
    (f : Fin d → Fin n) (hf : Function.Injective f)
    (hdet : (H.submatrix f f).det ≠ 0)
    (h : HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p) :
    (d : ℝ) / 2 * Real.logb 2 (1 / ε) +
      (d : ℝ) / 2 * Real.logb 2 (principalErrorConstant H l u f) ≤ p := by
  obtain ⟨a', b', hpull⟩ := graph_principal_pullback H a l u b ε
    (fun i => (hlu i).le) f hf h
  let D : Set (Input d) := Set.Icc 0 (fun j => u (f j)-l (f j))
  have hvol : (volume D).toReal = ∏ j, (u (f j)-l (f j)) := by
    rw [Real.volume_Icc_pi_toReal (by intro j; exact (sub_pos.mpr (hlu (f j))).le)]
    simp
  have hv := graph_quadratic_volume_bound (D := D) isCompact_Icc
    (H.submatrix f f) (Matrix.isHermitian_iff_isSymm.mp (hH.submatrix f)) hdet
    a' b' ε hε.le hpull
  have hr : 0 ≤ (2:ℝ)^p * ((2:ℝ)^d *
      (12 * Real.sqrt d * ε)^((d:ℝ)/2) / Real.sqrt |(H.submatrix f f).det|) := by positivity
  have hv' := ENNReal.toReal_le_of_le_ofReal hr hv
  rw [hvol] at hv'
  exact determinant_volume_log_lower hd (abs_pos.mpr hdet)
    (Finset.prod_pos fun j _ => sub_pos.mpr (hlu (f j))) hε hv'

/-- A nonsingular principal slice rules out zero error on the original box. -/
theorem graph_principal_error_pos {n d p : ℕ} (hd : 0 < d)
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b ε : ℝ) (hlu : ∀ i, l i < u i) (hε : 0 ≤ ε)
    (f : Fin d → Fin n) (hf : Function.Injective f)
    (hdet : (H.submatrix f f).det ≠ 0)
    (h : HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p) : 0 < ε := by
  obtain ⟨a', b', hpull⟩ := graph_principal_pullback H a l u b ε
    (fun i => (hlu i).le) f hf h
  have hvol : volume (Set.Icc (0 : Input d) (fun j => u (f j)-l (f j))) ≠ 0 := by
    rw [Real.volume_Icc_pi]
    apply Finset.prod_ne_zero_iff.mpr
    intro j _
    simpa using (sub_pos.mpr (hlu (f j))).not_ge
  exact graph_quadratic_error_pos hd isCompact_Icc hvol (H.submatrix f f)
    (Matrix.isHermitian_iff_isSymm.mp (hH.submatrix f)) hdet a' b' ε hε hpull

/-- Every nonsingular principal coordinate minor gives the stated exact
exponential obstruction for the original full-domain lift. -/
theorem graph_principal_error_lower {n d p : ℕ} (hd : 0 < d)
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b ε : ℝ) (hlu : ∀ i, l i < u i) (hε : 0 ≤ ε)
    (f : Fin d → Fin n) (hf : Function.Injective f)
    (hdet : (H.submatrix f f).det ≠ 0)
    (h : HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p) :
    principalErrorConstant H l u f * (2:ℝ)^(-2*(p:ℝ)/(d:ℝ)) ≤ ε := by
  have he := graph_principal_error_pos hd H hH a l u b ε hlu hε f hf hdet h
  exact error_lower_of_log_lower hd (principalErrorConstant_pos hd H l u hlu f hdet) he
    (graph_principal_log_lower hd H hH a l u b ε hlu he f hf hdet h)

/-- The rank lower bound follows from an actual nonsingular principal minor,
with a constant independent of the tolerance and the lift. -/
theorem graph_rank_lower {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) (hr : 0 < H.rank) :
    ∃ c : ℝ, ∀ ε : ℝ, 0 < ε → ∀ p : ℕ,
      HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p →
      (H.rank : ℝ) / 2 * Real.logb 2 (1 / ε) + c ≤ p := by
  obtain ⟨f, hf, hdet⟩ := exists_principal_coordinate_rank H hH
  refine ⟨(H.rank : ℝ)/2 * Real.logb 2 (principalErrorConstant H l u f), ?_⟩
  intro ε hε p h
  exact graph_principal_log_lower hr H hH a l u b ε hlu hε f hf hdet h

/-- Positive rank precludes an exact finite convex integer graph lift. -/
theorem no_exact_graph_of_positive_rank {n p : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) (hr : 0 < H.rank) :
    ¬ HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) 0 p := by
  intro h
  obtain ⟨f, hf, hdet⟩ := exists_principal_coordinate_rank H hH
  have hh := graph_principal_error_pos hr H hH a l u b 0 hlu le_rfl f hf hdet h
  exact (lt_irrefl (0 : ℝ)) hh

end QuadraticPrecision
