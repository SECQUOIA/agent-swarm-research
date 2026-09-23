import Mathlib.LinearAlgebra.Matrix.Determinant.TotallyUnimodular
import Mathlib.Algebra.Group.Submonoid.BigOperators
import Mathlib.LinearAlgebra.Matrix.Adjugate
import Mathlib.LinearAlgebra.Matrix.Rank

/-!
# Total-unimodularity operations for structural multilinear gaps

The gap argument uses signed copies of scope rows and coordinate bounds.
This file proves that these operations preserve total unimodularity.
It also proves that a solution of a full-column-rank integer TU system over
the reals is integer: extract independent rows, use the adjugate to solve
the resulting square system over the integers, and identify the solutions.
It does not prove the separate graph-to-TU (Camion) criterion.
-/

namespace MultilinearGap

open Matrix

variable {m n R : Type*} [CommRing R]

set_option backward.isDefEq.respectTransparency false in
/-- Multiplying arbitrary rows by `-1`, `0`, or `1` preserves total unimodularity. -/
theorem totallyUnimodular_sign_rows {A : Matrix m n R}
    (hA : A.IsTotallyUnimodular) (s : m → SignType) :
    (Matrix.of fun i j => (s i : R) * A i j).IsTotallyUnimodular := by
  rw [Matrix.isTotallyUnimodular_iff] at hA ⊢
  intro k f g
  change Matrix.det (Matrix.of fun i j => (s (f i) : R) * (A.submatrix f g) i j) ∈ _
  rw [Matrix.det_mul_column (fun i => (s (f i) : R)) (A.submatrix f g)]
  change _ ∈ MonoidHom.mrange SignType.castHom.toMonoidHom
  apply mul_mem
  · apply prod_mem
    intro i _
    exact Set.mem_range_self (s (f i))
  · exact hA k f g

/-- Selecting and repeating rows, then changing their signs, preserves TU. -/
theorem totallyUnimodular_signed_row_selection {p : Type*} {A : Matrix m n R}
    (hA : A.IsTotallyUnimodular) (f : p → m) (s : p → SignType) :
    (Matrix.of fun i j => (s i : R) * A (f i) j).IsTotallyUnimodular :=
  totallyUnimodular_sign_rows (hA.submatrix f id) s

/-- Both signs of every row can be imposed simultaneously. -/
theorem totallyUnimodular_two_sided {A : Matrix m n R}
    (hA : A.IsTotallyUnimodular) :
    (Matrix.fromRows A (-A)).IsTotallyUnimodular := by
  have h := totallyUnimodular_signed_row_selection hA
    (Sum.elim id id) (Sum.elim (fun _ => (1 : SignType)) (fun _ => -1))
  have heq : Matrix.fromRows A (-A) = Matrix.of (fun i j =>
      ((Sum.elim (fun _ => (1 : SignType)) (fun _ => -1)) i : R) *
        A (Sum.elim id id i) j) := by
    ext i j
    cases i <;> simp
  rw [heq]
  exact h

/-- The matrix for two-sided scope inequalities and unit-cube constraints. -/
def scopeBoxMatrix [DecidableEq n] (A : Matrix m n R) :
    Matrix ((m ⊕ n) ⊕ (m ⊕ n)) n R :=
  Matrix.fromRows (Matrix.fromRows A 1) (-(Matrix.fromRows A 1))

/-- Adding both signs of coordinate and scope rows preserves TU. -/
theorem totallyUnimodular_scopeBoxMatrix [DecidableEq n] {A : Matrix m n R}
    (hA : A.IsTotallyUnimodular) : (scopeBoxMatrix A).IsTotallyUnimodular :=
  totallyUnimodular_two_sided hA.fromRows_one

/-- A nonsingular square TU matrix has determinant square equal to one. -/
theorem totallyUnimodular_det_mul_self [Fintype n] [DecidableEq n]
    {A : Matrix n n R} (hA : A.IsTotallyUnimodular) (hd : A.det ≠ 0) :
    A.det * A.det = 1 := by
  have hdet := (Matrix.isTotallyUnimodular_iff_fintype A).mp hA n id id
  simp only [Matrix.submatrix_id_id] at hdet
  obtain ⟨s, hs⟩ := hdet
  rw [← hs] at hd ⊢
  clear hs
  cases s <;> simp_all

/-- The unique solution of a nonsingular square TU system is obtained over
the original ring. In particular, integer right-hand sides have integer
solutions; no rational or real relaxation is needed for this step. -/
theorem totallyUnimodular_nonsingular_system [Fintype n] [DecidableEq n]
    {A : Matrix n n R} (hA : A.IsTotallyUnimodular) (hd : A.det ≠ 0)
    (b : n → R) : ∃! x : n → R, A *ᵥ x = b := by
  have hsq := totallyUnimodular_det_mul_self hA hd
  refine ⟨A.det • (A.adjugate *ᵥ b), ?_, ?_⟩
  · change A *ᵥ (A.det • (A.adjugate *ᵥ b)) = b
    rw [Matrix.mulVec_smul, Matrix.mulVec_mulVec, Matrix.mul_adjugate,
      Matrix.smul_mulVec, Matrix.one_mulVec, smul_smul, hsq, one_smul]
  · intro x hx
    have heq : A.det • x = A.adjugate *ᵥ b := by
      rw [← hx, Matrix.mulVec_mulVec, Matrix.adjugate_mul,
        Matrix.smul_mulVec, Matrix.one_mulVec]
    rw [← heq, smul_smul, hsq, one_smul]

/-- Ring homomorphisms preserve total unimodularity. -/
theorem totallyUnimodular_map {S : Type*} [CommRing S]
    (φ : R →+* S) {A : Matrix m n R} (hA : A.IsTotallyUnimodular) :
    (A.map φ).IsTotallyUnimodular := by
  rw [Matrix.isTotallyUnimodular_iff] at hA ⊢
  intro k f g
  obtain ⟨s, hs⟩ := hA k f g
  refine ⟨s, ?_⟩
  change (s : S) = (φ.mapMatrix (A.submatrix f g)).det
  rw [← φ.map_det, ← hs]
  cases s <;> simp

/-- A solution of a nonsingular TU system after an injective ring extension
comes from a solution over the original ring. Specializing `R` to integers
and `S` to reals is the integer-basis step in polyhedral integrality. -/
theorem totallyUnimodular_solution_descends {S : Type*} [CommRing S]
    [Fintype n] [DecidableEq n] (φ : R →+* S) (hφ : Function.Injective φ)
    {A : Matrix n n R} (hA : A.IsTotallyUnimodular) (hd : A.det ≠ 0)
    (b : n → R) {x : n → S} (hx : A.map φ *ᵥ x = φ ∘ b) :
    ∃ z : n → R, A *ᵥ z = b ∧ φ ∘ z = x := by
  obtain ⟨z, hz, _⟩ := totallyUnimodular_nonsingular_system hA hd b
  refine ⟨z, hz, ?_⟩
  have hd' : (A.map φ).det ≠ 0 := by
    change (φ.mapMatrix A).det ≠ 0
    rw [← φ.map_det]
    exact fun heq => hd (hφ (heq.trans φ.map_zero.symm))
  obtain ⟨w, _, hw⟩ := totallyUnimodular_nonsingular_system
    (totallyUnimodular_map φ hA) hd' (φ ∘ b)
  have hz' : A.map φ *ᵥ (φ ∘ z) = φ ∘ b := by
    ext i
    rw [← φ.map_mulVec, hz]
    rfl
  exact (hw _ hz').trans (hw _ hx).symm

/-- A matrix with injective action on column vectors contains a nonsingular
square submatrix obtained by selecting rows. -/
theorem exists_nonsingular_row_selection {K : Type*} [Field K]
    [Finite m] [Fintype n] [DecidableEq n] (A : Matrix m n K)
    (hA : Function.Injective A.mulVec) :
    ∃ f : n → m, Function.Injective f ∧ (A.submatrix f id).det ≠ 0 := by
  classical
  obtain ⟨κ, a, ha, hspan, hlin⟩ := exists_linearIndependent' K A.row
  let : Finite κ := Finite.of_injective a ha
  let : Fintype κ := Fintype.ofFinite κ
  have hcard : Fintype.card κ = Fintype.card n := by
    calc
      Fintype.card κ = Module.finrank K (Submodule.span K (Set.range (A.row ∘ a))) :=
        linearIndependent_iff_card_eq_finrank_span.mp hlin
      _ = Module.finrank K (Submodule.span K (Set.range A.row)) := by rw [hspan]
      _ = A.rank := A.rank_eq_finrank_span_row.symm
      _ = Fintype.card n := by
        rw [Matrix.rank, LinearMap.finrank_range_of_inj hA,
          Module.finrank_fintype_fun_eq_card]
  let e : n ≃ κ := Fintype.equivOfCardEq hcard.symm
  refine ⟨a ∘ e, ha.comp e.injective, ?_⟩
  apply IsUnit.ne_zero
  apply (Matrix.isUnit_iff_isUnit_det _).mp
  apply Matrix.linearIndependent_rows_iff_isUnit.mp
  exact hlin.comp e e.injective

/-- Full column rank suffices for descent of a rectangular TU system.
This extracts an independent square system from the rows, proves its solution
belongs to the original ring, and identifies it with the prescribed solution.
For integer matrices embedded into the reals, this is the active-constraint
basis argument for integral vertices. -/
theorem totallyUnimodular_injective_system_descends {K : Type*} [Field K]
    [Finite m] [Fintype n]
    (φ : R →+* K) (hφ : Function.Injective φ) {A : Matrix m n R}
    (hA : A.IsTotallyUnimodular) (hinj : Function.Injective (A.map φ).mulVec)
    (b : m → R) {x : n → K} (hx : A.map φ *ᵥ x = φ ∘ b) :
    ∃ z : n → R, φ ∘ z = x := by
  classical
  obtain ⟨f, _, hd⟩ := exists_nonsingular_row_selection (A.map φ) hinj
  have hd' : (A.submatrix f id).det ≠ 0 := by
    intro hz
    apply hd
    change (φ.mapMatrix (A.submatrix f id)).det = 0
    rw [← φ.map_det, hz, map_zero]
  have hx' : (A.submatrix f id).map φ *ᵥ x = φ ∘ (b ∘ f) := by
    ext i
    exact congrFun hx (f i)
  obtain ⟨z, _, hz⟩ := totallyUnimodular_solution_descends φ hφ
    (hA.submatrix f id) hd' (b ∘ f) hx'
  exact ⟨z, hz⟩

end MultilinearGap
