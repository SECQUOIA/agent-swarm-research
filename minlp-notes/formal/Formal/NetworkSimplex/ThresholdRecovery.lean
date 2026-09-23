import Mathlib

/-! Exact active-basis recovery in bounded polyhedra, including lower-dimensional ones. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
open Matrix Set

/-- A finite system of non-strict linear inequalities. -/
def polyhedron {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℝ) (b : Fin N → ℝ) :
    Set (Fin m → ℝ) := {x | ∀ i, A i ⬝ᵥ x ≤ b i}

theorem polyhedron_closed {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℝ) (b : Fin N → ℝ) :
    IsClosed (polyhedron A b) := by
  rw [show polyhedron A b = ⋂ i, {x | A i ⬝ᵥ x ≤ b i} by ext; simp [polyhedron]]
  apply isClosed_iInter
  intro i
  apply isClosed_le _ continuous_const
  exact continuous_finsetSum _ fun j _ ↦ continuous_const.mul (continuous_apply j)

/-- A direction annihilating all active rows permits a small perturbation in
both directions. Strictly inactive inequalities remain feasible by continuity. -/
theorem exists_symmetric_perturbation {N m : ℕ} {A : Matrix (Fin N) (Fin m) ℝ}
    {b : Fin N → ℝ} {x z : Fin m → ℝ} (hx : x ∈ polyhedron A b)
    (hz : ∀ i, A i ⬝ᵥ x = b i → A i ⬝ᵥ z = 0) :
    ∃ t : ℝ, 0 < t ∧ x + t • z ∈ polyhedron A b ∧ x - t • z ∈ polyhedron A b := by
  have he : ∀ᶠ t : ℝ in nhds 0, ∀ i, A i ⬝ᵥ x + t * (A i ⬝ᵥ z) ≤ b i := by
    rw [Filter.eventually_all]
    intro i
    by_cases hi : A i ⬝ᵥ x = b i
    · simp only [hz i hi, mul_zero, add_zero, hi, le_refl, Filter.eventually_true]
    · have hlt : A i ⬝ᵥ x < b i := lt_of_le_of_ne (hx i) hi
      have hc : ContinuousAt (fun t : ℝ ↦ A i ⬝ᵥ x + t * (A i ⬝ᵥ z)) 0 := by
        fun_prop
      exact (hc.eventually_lt_const (by simpa using hlt)).mono fun _ h ↦ h.le
  obtain ⟨δ, hδ, hh⟩ := Metric.eventually_nhds_iff.mp he
  refine ⟨δ / 2, by positivity, ?_, ?_⟩
  · intro i
    simpa [dotProduct_add, dotProduct_smul, smul_eq_mul] using
      hh (by simpa [Real.dist_eq, abs_of_pos hδ] using
        (show δ / 2 < δ by linarith)) i
  · intro i
    have h := hh (y := -(δ / 2)) (by
      simpa [Real.dist_eq, abs_neg, abs_of_pos hδ] using
        (show δ / 2 < δ by linarith)) i
    simpa [dotProduct_sub, dotProduct_smul, smul_eq_mul, sub_eq_add_neg] using h

/-- At an extreme point the active rows have trivial common kernel. -/
theorem extreme_active_kernel_eq_zero {N m : ℕ} {A : Matrix (Fin N) (Fin m) ℝ}
    {b : Fin N → ℝ} {x : Fin m → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ)
    {z : Fin m → ℝ} (hz : ∀ i, A i ⬝ᵥ x = b i → A i ⬝ᵥ z = 0) : z = 0 := by
  obtain ⟨t, ht, hp, hn⟩ := exists_symmetric_perturbation hx.1 hz
  have hseg : x ∈ openSegment ℝ (x + t • z) (x - t • z) := by
    refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
    ext j
    simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have he := hx.2 hp hn hseg
  have htz : t • z = 0 := by exact add_left_cancel (he.trans (add_zero x).symm)
  exact (smul_eq_zero.mp htz).resolve_left (ne_of_gt ht)

/-- The active row normals at an extreme point span the entire ambient space.
This conclusion does not require the feasible set to have interior. -/
theorem extreme_active_span {N m : ℕ} {A : Matrix (Fin N) (Fin m) ℝ}
    {b : Fin N → ℝ} {x : Fin m → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ) :
    Submodule.span ℝ (Set.range (fun i : {i : Fin N // A i ⬝ᵥ x = b i} ↦ A i)) = ⊤ := by
  classical
  let B : Matrix {i : Fin N // A i ⬝ᵥ x = b i} (Fin m) ℝ := fun i ↦ A i
  have hinj : Function.Injective B.mulVec := by
    intro u v huv
    apply sub_eq_zero.mp
    apply extreme_active_kernel_eq_zero hx
    intro i hi
    have h := congrFun huv (⟨i, hi⟩ : {i : Fin N // A i ⬝ᵥ x = b i})
    change A i ⬝ᵥ u = A i ⬝ᵥ v at h
    simp only [dotProduct_sub, h, sub_self]
  have hli := Matrix.mulVec_injective_iff.mp hinj
  exact span_flip_eq_top_iff_linearIndependent.mpr hli

/-- Every extreme point is the unique solution of an invertible square system
formed from active input rows. -/
theorem extreme_has_active_basis {N m : ℕ} {A : Matrix (Fin N) (Fin m) ℝ}
    {b : Fin N → ℝ} {x : Fin m → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ) :
    ∃ e : Fin m → Fin N, Function.Injective e ∧
      (∀ j, A (e j) ⬝ᵥ x = b (e j)) ∧
      (A.submatrix e id).det ≠ 0 ∧
      (A.submatrix e id)⁻¹ *ᵥ (b ∘ e) = x := by
  classical
  let I := {i : Fin N // A i ⬝ᵥ x = b i}
  obtain ⟨κ, f, hf, hspan, hli⟩ := exists_linearIndependent' ℝ (fun i : I ↦ A i)
  have htop : Submodule.span ℝ (Set.range ((fun i : I ↦ A i) ∘ f)) = ⊤ :=
    hspan.trans (extreme_active_span hx)
  let B := Module.Basis.mk hli htop.ge
  let : Finite κ := hli.finite
  let : Fintype κ := Fintype.ofFinite κ
  have hcard : Fintype.card κ = m := by
    rw [← Module.finrank_eq_card_basis B]
    simp
  let g : κ ≃ Fin m := Fintype.equivOfCardEq (by simpa using hcard)
  let e : Fin m → Fin N := fun j ↦ (f (g.symm j)).val
  have he : Function.Injective e := Subtype.val_injective.comp (hf.comp g.symm.injective)
  have hact : ∀ j, A (e j) ⬝ᵥ x = b (e j) := fun j ↦ (f (g.symm j)).property
  have hrow : LinearIndependent ℝ (A.submatrix e id).row :=
    hli.comp g.symm g.symm.injective
  have hu : IsUnit (A.submatrix e id) := Matrix.linearIndependent_rows_iff_isUnit.mp hrow
  have hdet : IsUnit (A.submatrix e id).det := (Matrix.isUnit_iff_isUnit_det _).mp hu
  refine ⟨e, he, hact, isUnit_iff_ne_zero.mp hdet, ?_⟩
  have heq : (A.submatrix e id) *ᵥ x = b ∘ e := funext hact
  rw [← heq, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hdet, Matrix.one_mulVec]

/-- A nonempty bounded polyhedron always has an active-basis candidate. -/
theorem bounded_polyhedron_has_basis {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℝ)
    (b : Fin N → ℝ) (hne : (polyhedron A b).Nonempty)
    (hbounded : Bornology.IsBounded (polyhedron A b)) :
    ∃ e : Fin m → Fin N, Function.Injective e ∧ (A.submatrix e id).det ≠ 0 ∧
      (A.submatrix e id)⁻¹ *ᵥ (b ∘ e) ∈ polyhedron A b := by
  have hcompact : IsCompact (polyhedron A b) :=
    Metric.isCompact_iff_isClosed_bounded.mpr ⟨polyhedron_closed A b, hbounded⟩
  obtain ⟨x, hx⟩ := hcompact.extremePoints_nonempty hne
  obtain ⟨e, he, _, hd, hxinv⟩ := extreme_has_active_basis hx
  exact ⟨e, he, hd, hxinv ▸ hx.1⟩

/-- Enumerating ordered selections of rows considers at most `N^m` systems. -/
theorem basis_selection_card (N m : ℕ) : Fintype.card (Fin m → Fin N) = N ^ m := by
  simp

end NetworkSimplex.Threshold
