import Formal.NetworkSimplex.ThresholdRecovery

/-! Executable cached-basis recovery for finite rational inequality tables. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open Matrix

/-- All ordered selections of `m` rows, generated without any choice operator. -/
def basisChoices (N : ℕ) : (m : ℕ) → List (Fin m → Fin N)
  | 0 => [Fin.elim0]
  | m + 1 => (List.finRange N).flatMap fun i ↦ (basisChoices N m).map (Fin.cons i)

@[simp] theorem mem_basisChoices {N m : ℕ} (e : Fin m → Fin N) : e ∈ basisChoices N m := by
  induction m with
  | zero => simp [basisChoices, Subsingleton.elim e Fin.elim0]
  | succ m ih =>
    simp only [basisChoices, List.mem_flatMap, List.mem_finRange, true_and, List.mem_map]
    exact ⟨e 0, Fin.tail e, ih _, Fin.cons_self_tail e⟩

@[simp] theorem basisChoices_length (N m : ℕ) : (basisChoices N m).length = N ^ m := by
  induction m with
  | zero => simp [basisChoices]
  | succ m ih => simp [basisChoices, List.length_flatMap, ih, pow_succ, Nat.mul_comm]

/-- Rational adjugate formula, executable even though the generic matrix inverse
uses a noncomputable ring-unit inverse. All inverses are computed in preprocessing. -/
def inverseRat {m : ℕ} (M : Matrix (Fin m) (Fin m) ℚ) : Matrix (Fin m) (Fin m) ℚ :=
  M.det⁻¹ • M.adjugate

theorem inverseRat_eq_inv {m : ℕ} (M : Matrix (Fin m) (Fin m) ℚ) : inverseRat M = M⁻¹ := by
  simp [inverseRat, Matrix.inv_def, Ring.inverse_eq_inv]

structure CachedBasis (N m : ℕ) where
  rowData : Vector (Fin N) m
  inverseData : Vector (Vector ℚ m) m

def CachedBasis.rows {N m : ℕ} (B : CachedBasis N m) : Fin m → Fin N := B.rowData.get

def CachedBasis.inverse {N m : ℕ} (B : CachedBasis N m) : Matrix (Fin m) (Fin m) ℚ :=
  fun i j ↦ (B.inverseData.get i).get j

def cacheBasis {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ) (e : Fin m → Fin N) :
    CachedBasis N m :=
  ⟨Vector.ofFn e, Vector.ofFn (fun i ↦ Vector.ofFn (inverseRat (A.submatrix e id) i))⟩

/-- The entire cache depends only on the normal matrix, not on right-hand sides. -/
def basisLibrary {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ) : List (CachedBasis N m) :=
  (basisChoices N m).filterMap fun e ↦
    if (A.submatrix e id).det = 0 then none else some (cacheBasis A e)

theorem cacheBasis_mem_library {N m : ℕ} {A : Matrix (Fin N) (Fin m) ℚ}
    {e : Fin m → Fin N} (he : (A.submatrix e id).det ≠ 0) :
    cacheBasis A e ∈ basisLibrary A := by
  simp only [basisLibrary, List.mem_filterMap]
  exact ⟨e, mem_basisChoices e, by simp [he]⟩

theorem mem_basisLibrary_iff {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (B : CachedBasis N m) : B ∈ basisLibrary A ↔
      ∃ e : Fin m → Fin N, (A.submatrix e id).det ≠ 0 ∧ B = cacheBasis A e := by
  constructor
  · intro h
    obtain ⟨e, _, he⟩ := List.mem_filterMap.mp h
    by_cases hd : (A.submatrix e id).det = 0
    · simp [hd] at he
    · refine ⟨e, hd, ?_⟩
      simpa [hd] using he.symm
  · rintro ⟨e, he, rfl⟩
    exact cacheBasis_mem_library he

theorem basisLibrary_length_le {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ) :
    (basisLibrary A).length ≤ N ^ m := by
  exact (List.length_filterMap_le _ _).trans_eq (basisChoices_length N m)

/-- Missing directions impose no constraint. -/
def PartialFeasible {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (x : Fin m → ℚ) : Prop :=
  ∀ i b, table i = some b → A i ⬝ᵥ x ≤ b

def validCandidate {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (x : Fin m → ℚ) : Bool :=
  (List.finRange N).all fun i ↦ match table i with
    | none => true
    | some b => decide (A i ⬝ᵥ x ≤ b)

@[simp] theorem validCandidate_eq_true {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (x : Fin m → ℚ) :
    validCandidate A table x = true ↔ PartialFeasible A table x := by
  simp only [validCandidate, List.all_eq_true, List.mem_finRange, forall_true_left]
  constructor
  · intro h i b hi
    simpa [hi] using h i
  · intro h i
    cases hi : table i with
    | none => rfl
    | some b => simpa using h i b hi

def CachedBasis.present {N m : ℕ} (B : CachedBasis N m) (table : Fin N → Option ℚ) : Bool :=
  (List.finRange m).all fun j ↦ (table (B.rows j)).isSome

def CachedBasis.candidate {N m : ℕ} (B : CachedBasis N m)
    (table : Fin N → Option ℚ) : Fin m → ℚ :=
  let rhs := Vector.ofFn (fun j ↦ (table (B.rows j)).getD 0)
  (Vector.ofFn (B.inverse *ᵥ rhs.get)).get

/-- One work unit is a table lookup, comparison, or rational multiply-accumulate.
This conservative ledger charges complete dense products and all validation rows,
even when Boolean short-circuiting stops earlier. -/
def basisTrialCharge (N m : ℕ) : ℕ := 2 * m + m * m + N * (m + 1) + 1

/-- Scan cached bases and return the first validated candidate, with its work ledger. -/
def scanBases {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ) (table : Fin N → Option ℚ) :
    List (CachedBasis N m) → Option (Fin m → ℚ) × ℕ
  | [] => (none, 0)
  | B :: rest =>
    if B.present table then
      let x := B.candidate table
      if validCandidate A table x then (some x, basisTrialCharge N m)
      else let r := scanBases A table rest; (r.1, basisTrialCharge N m + r.2)
    else let r := scanBases A table rest; (r.1, m + 1 + r.2)

theorem scanBases_charge_le {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (L : List (CachedBasis N m)) :
    (scanBases A table L).2 ≤ L.length * basisTrialCharge N m := by
  induction L with
  | nil => simp [scanBases]
  | cons B L ih =>
    simp only [scanBases]
    split_ifs <;> simp only [List.length_cons] <;>
      dsimp [basisTrialCharge] at * <;> nlinarith

theorem scanBases_sound {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (L : List (CachedBasis N m)) {x : Fin m → ℚ}
    (hx : (scanBases A table L).1 = some x) : PartialFeasible A table x := by
  induction L with
  | nil => simp [scanBases] at hx
  | cons B L ih =>
    simp only [scanBases] at hx
    split_ifs at hx with hp hv
    · simp only [Option.some.injEq] at hx
      subst x
      exact (validCandidate_eq_true _ _ _).mp hv
    · exact ih hx
    · exact ih hx

theorem scanBases_complete {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (L : List (CachedBasis N m))
    (hex : ∃ B ∈ L, B.present table = true ∧ PartialFeasible A table (B.candidate table)) :
    ∃ x, (scanBases A table L).1 = some x ∧ PartialFeasible A table x := by
  induction L with
  | nil => simp at hex
  | cons B L ih =>
    by_cases hp : B.present table = true
    · by_cases hv : validCandidate A table (B.candidate table) = true
      · exact ⟨B.candidate table, by simp [scanBases, hp, hv],
          (validCandidate_eq_true _ _ _).mp hv⟩
      · have hrest : ∃ C ∈ L, C.present table = true ∧
            PartialFeasible A table (C.candidate table) := by
          obtain ⟨C, hC, hCp, hCv⟩ := hex
          rcases List.mem_cons.mp hC with rfl | hC
          · exact False.elim (hv ((validCandidate_eq_true _ _ _).mpr hCv))
          · exact ⟨C, hC, hCp, hCv⟩
        obtain ⟨x, hx, hxf⟩ := ih hrest
        exact ⟨x, by simpa [scanBases, hp, hv] using hx, hxf⟩
    · have hrest : ∃ C ∈ L, C.present table = true ∧
          PartialFeasible A table (C.candidate table) := by
        obtain ⟨C, hC, hCp, hCv⟩ := hex
        rcases List.mem_cons.mp hC with rfl | hC
        · exact False.elim (hp hCp)
        · exact ⟨C, hC, hCp, hCv⟩
      obtain ⟨x, hx, hxf⟩ := ih hrest
      exact ⟨x, by simpa [scanBases, hp] using hx, hxf⟩

/-- Real semantics of the partial rational system. -/
def realPartialSet {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) : Set (Fin m → ℝ) :=
  {x | ∀ i b, table i = some b → (fun j ↦ (A i j : ℝ)) ⬝ᵥ x ≤ (b : ℝ)}

noncomputable def effectiveMatrix {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) : Matrix (Fin N) (Fin m) ℝ :=
  fun i j ↦ if (table i).isSome then (A i j : ℝ) else 0

noncomputable def effectiveRhs {N : ℕ} (table : Fin N → Option ℚ) : Fin N → ℝ :=
  fun i ↦ ((table i).getD 0 : ℝ)

theorem effective_polyhedron_eq {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) :
    NetworkSimplex.Threshold.polyhedron (effectiveMatrix A table) (effectiveRhs table) =
      realPartialSet A table := by
  ext x
  constructor
  · intro h i b hi
    simpa [effectiveMatrix, effectiveRhs, hi, dotProduct] using h i
  · intro h i
    cases hi : table i with
    | none => simp [effectiveMatrix, effectiveRhs, hi, dotProduct]
    | some b => simpa [effectiveMatrix, effectiveRhs, hi, dotProduct] using h i b hi

theorem inverseRat_cast {m : ℕ} (M : Matrix (Fin m) (Fin m) ℚ) :
    (inverseRat M).map (Rat.castHom ℝ) = (M.map (Rat.castHom ℝ))⁻¹ := by
  rw [Matrix.inv_def, Ring.inverse_eq_inv]
  have hd := (Rat.castHom ℝ).map_det M
  have ha := (Rat.castHom ℝ).map_adjugate M
  simp only [RingHom.mapMatrix_apply] at hd ha
  rw [← hd, ← ha]
  ext i j
  simp [inverseRat, Matrix.map_apply, smul_eq_mul]

theorem rational_feasible_iff_cast {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (x : Fin m → ℚ) :
    PartialFeasible A table x ↔ (fun j ↦ (x j : ℝ)) ∈ realPartialSet A table := by
  constructor <;> intro h i b hi
  · have hh := h i b hi
    simp only [dotProduct] at hh ⊢
    exact_mod_cast hh
  · have hh := h i b hi
    simp only [dotProduct] at hh ⊢
    exact_mod_cast hh

/-- Completeness of the actual precomputed library for every bounded nonempty
partial system; absent rows cannot occur in a nonsingular basis. -/
theorem basisLibrary_has_feasible_candidate {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (hne : (realPartialSet A table).Nonempty)
    (hb : Bornology.IsBounded (realPartialSet A table)) :
    ∃ B ∈ basisLibrary A, B.present table = true ∧
      PartialFeasible A table (B.candidate table) := by
  have hp := effective_polyhedron_eq A table
  obtain ⟨e, _, hd, hx⟩ := NetworkSimplex.Threshold.bounded_polyhedron_has_basis
    (effectiveMatrix A table) (effectiveRhs table) (hp.symm ▸ hne) (hp.symm ▸ hb)
  have hpres : ∀ j, (table (e j)).isSome = true := by
    intro j
    cases h : table (e j) with
    | some b => rfl
    | none =>
      exfalso
      apply hd
      apply Matrix.det_eq_zero_of_row_eq_zero j
      intro k
      simp [Matrix.submatrix_apply, effectiveMatrix, h]
  have hmat : (effectiveMatrix A table).submatrix e id =
      (A.submatrix e id).map (Rat.castHom ℝ) := by
    ext j k
    simp [Matrix.submatrix_apply, effectiveMatrix, hpres]
  have hdetq : (A.submatrix e id).det ≠ 0 := by
    intro hz
    apply hd
    rw [hmat]
    have hh := (Rat.castHom ℝ).map_det (A.submatrix e id)
    simpa [RingHom.mapMatrix_apply, hz] using hh.symm
  refine ⟨cacheBasis A e, cacheBasis_mem_library hdetq, ?_, ?_⟩
  · simpa [CachedBasis.present, CachedBasis.rows, cacheBasis] using hpres
  · apply (rational_feasible_iff_cast A table _).mpr
    rw [← hp]
    have hcast : (fun j ↦ ((cacheBasis A e).candidate table j : ℝ)) =
        ((effectiveMatrix A table).submatrix e id)⁻¹ *ᵥ (effectiveRhs table ∘ e) := by
      rw [hmat, ← inverseRat_cast]
      ext j
      simp [CachedBasis.candidate, CachedBasis.inverse, CachedBasis.rows, cacheBasis,
        effectiveRhs, Matrix.mulVec, dotProduct,
        Matrix.map_apply, Function.comp_apply]
    exact hcast ▸ hx

/-- Recover a feasible rational vector, using only the previously cached inverses. -/
def recoverFromCache {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (cache : List (CachedBasis N m)) : Option (Fin m → ℚ) :=
  (scanBases A table cache).1

theorem recoverFromCache_complete {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) (hne : (realPartialSet A table).Nonempty)
    (hb : Bornology.IsBounded (realPartialSet A table)) :
    ∃ x, recoverFromCache A table (basisLibrary A) = some x ∧ PartialFeasible A table x :=
  scanBases_complete A table (basisLibrary A) (basisLibrary_has_feasible_candidate A table hne hb)

theorem recoverFromCache_charge {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℚ)
    (table : Fin N → Option ℚ) :
    (scanBases A table (basisLibrary A)).2 ≤ N ^ m * basisTrialCharge N m :=
  (scanBases_charge_le A table (basisLibrary A)).trans
    (Nat.mul_le_mul_right _ (basisLibrary_length_le A))

end NetworkSimplex.Chain.Threshold
