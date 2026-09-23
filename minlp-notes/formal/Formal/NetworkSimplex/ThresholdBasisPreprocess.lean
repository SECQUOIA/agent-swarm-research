import Formal.NetworkSimplex.ThresholdBasisOracle
import Formal.NetworkSimplex.ThresholdDetTrace
import Formal.NetworkSimplex.ThresholdCircuitPreprocess

/-! Counted executable preprocessing of cached inverse bases for integer normals. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- The rational normal matrix used by the exact basis oracle. -/
def integerMatrixRat {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) : Matrix (Fin N) (Fin m) ℚ :=
  A.map (Int.castRingHom ℚ)

private theorem inverseRat_int_entry {m : ℕ} (M : Matrix (Fin m) (Fin m) ℤ) (i j : Fin m) :
    inverseRat (integerMatrixRat M) i j = (M.det : ℚ)⁻¹ * (M.adjugate i j : ℚ) := by
  have hd := (Int.castRingHom ℚ).map_det M
  have ha := (Int.castRingHom ℚ).map_adjugate M
  simp only [RingHom.mapMatrix_apply] at hd ha
  simp only [inverseRat, integerMatrixRat]
  rw [← hd, ← ha]
  rfl

/-- Both the determinant and every adjugate entry are evaluated by the counted
Laplace recursion. The inverse determinant and all entries are materialized once. -/
def basisCacheTrace {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) (e : Fin m → Fin N) :
    Option (CachedBasis N m) × ℕ :=
  let M := A.submatrix e id
  let dt := determinantTrace m M
  if dt.1 = 0 then (none, dt.2 + 1) else
    let cof := Vector.ofFn fun i : Fin m ↦ Vector.ofFn fun j : Fin m ↦
      determinantTrace m (M.updateRow j (Pi.single i 1))
    let reciprocal : ℚ := (dt.1 : ℚ)⁻¹
    let entries := cof.map fun row ↦ row.map fun p ↦ reciprocal * (p.1 : ℚ)
    (some ⟨Vector.ofFn e, entries⟩,
      dt.2 + 2 + ∑ i : Fin m, ∑ j : Fin m, (((cof.get i).get j).2 + 1))

/-- The counted producer returns exactly the original cached-basis representation. -/
theorem basisCacheTrace_value {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (e : Fin m → Fin N) :
    (basisCacheTrace A e).1 =
      if (A.submatrix e id).det = 0 then none else some (cacheBasis (integerMatrixRat A) e) := by
  simp only [basisCacheTrace, determinantTrace_value]
  split_ifs
  · rfl
  · dsimp only
    congr 1
    unfold cacheBasis
    congr 1
    apply Vector.ext
    intro i hi
    apply Vector.ext
    intro j hj
    simp only [Vector.getElem_map, Vector.getElem_ofFn,
      determinantTrace_value]
    have he := inverseRat_int_entry (A.submatrix e id) ⟨i, hi⟩ ⟨j, hj⟩
    have hm : (integerMatrixRat A).submatrix e id =
        integerMatrixRat (A.submatrix e id) := by ext r c; rfl
    rw [hm]
    simpa only [Matrix.adjugate_apply] using he.symm

/-- Per-choice arithmetic bound, including singularity testing and reciprocal formation. -/
def basisCacheWork (m : ℕ) : ℕ := (m * m + 1) * determinantWork m + m * m + 2

theorem basisCacheTrace_work {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (e : Fin m → Fin N) : (basisCacheTrace A e).2 ≤ basisCacheWork m := by
  have hd := determinantTrace_work m (A.submatrix e id)
  simp only [basisCacheTrace]
  split_ifs
  · dsimp only
    unfold basisCacheWork
    nlinarith
  · dsimp only
    have hc : (∑ i : Fin m, ∑ j : Fin m,
        ((determinantTrace m ((A.submatrix e id).updateRow j (Pi.single i 1))).2 + 1)) ≤
        m * (m * (determinantWork m + 1)) := by
      calc
        _ ≤ ∑ _i : Fin m, ∑ _j : Fin m, (determinantWork m + 1) := by
          apply Finset.sum_le_sum
          intro i _
          apply Finset.sum_le_sum
          intro j _
          exact Nat.add_le_add_right (determinantTrace_work _ _) 1
        _ = _ := by simp
    simp only [Vector.get_ofFn]
    unfold basisCacheWork
    nlinarith

/-- Preprocess every ordered row choice and retain exactly nonsingular caches. -/
def basisListTrace {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    List (Fin m → Fin N) → List (CachedBasis N m) × ℕ
  | [] => ([], 0)
  | e :: es =>
      let head := basisCacheTrace A e
      let tail := basisListTrace A es
      (match head.1 with | none => tail.1 | some B => B :: tail.1,
        head.2 + tail.2 + 1)

/-- Actual executable basis preprocessing, with a complete arithmetic ledger. -/
def preprocessBases {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    List (CachedBasis N m) × ℕ := basisListTrace A (basisChoices N m)

private theorem integer_basis_det_zero_iff {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (e : Fin m → Fin N) :
    ((integerMatrixRat A).submatrix e id).det = 0 ↔ (A.submatrix e id).det = 0 := by
  have hd := (Int.castRingHom ℚ).map_det (A.submatrix e id)
  simp only [RingHom.mapMatrix_apply] at hd
  change ((A.submatrix e id).map (Int.castRingHom ℚ)).det = 0 ↔ _
  rw [← hd]
  exact Int.cast_eq_zero

theorem basisListTrace_value {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (L : List (Fin m → Fin N)) :
    (basisListTrace A L).1 = L.filterMap (fun e ↦
      if ((integerMatrixRat A).submatrix e id).det = 0 then none
      else some (cacheBasis (integerMatrixRat A) e)) := by
  induction L with
  | nil => rfl
  | cons e L ih =>
    simp only [basisListTrace, basisCacheTrace_value, List.filterMap_cons,
      integer_basis_det_zero_iff]
    split_ifs <;> simp [ih, integer_basis_det_zero_iff]

@[simp] theorem preprocessBases_value {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    (preprocessBases A).1 = basisLibrary (integerMatrixRat A) := basisListTrace_value _ _

theorem basisListTrace_work {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ)
    (L : List (Fin m → Fin N)) :
    (basisListTrace A L).2 ≤ L.length * (basisCacheWork m + 1) := by
  induction L with
  | nil => simp [basisListTrace]
  | cons e L ih =>
    have hh := basisCacheTrace_work A e
    simp only [basisListTrace, List.length_cons]
    nlinarith

theorem preprocessBases_work {N m : ℕ} (A : Matrix (Fin N) (Fin m) ℤ) :
    (preprocessBases A).2 ≤ N ^ m * (basisCacheWork m + 1) := by
  simpa [preprocessBases] using basisListTrace_work A (basisChoices N m)

/-- The materialized inverse preprocessing has a quadratic-exponential parameter
bound, including every determinant recursion and adjugate entry multiplication. -/
theorem basisCacheWork_exp (m : ℕ) : basisCacheWork m + 1 ≤ 2 ^ (4 * (m + 2) ^ 2) := by
  have hd := determinantWork_factorial m
  have hf : 1 ≤ (m + 2).factorial := Nat.factorial_pos _
  have hm : m + 2 ≤ 2 ^ (m + 2) := Nat.lt_two_pow_self.le
  have hp : basisCacheWork m + 1 ≤ 2 * (m + 2) ^ 2 * (m + 2).factorial := by
    have hh := Nat.mul_le_mul_left (m * m + 1) hd
    have hq := Nat.mul_le_mul_left (m * m + 3) hf
    unfold basisCacheWork
    nlinarith
  calc
    _ ≤ 2 * (m + 2) ^ 2 * (m + 2).factorial := hp
    _ ≤ 2 * (2 ^ (m + 2)) ^ 2 * (2 ^ (m + 2)) ^ (m + 2) :=
      Nat.mul_le_mul (Nat.mul_le_mul_left 2 (Nat.pow_le_pow_left hm _))
        ((Nat.factorial_le_pow _).trans (Nat.pow_le_pow_left hm _))
    _ = 2 ^ (1 + (m + 2) * 2 + (m + 2) * (m + 2)) := by
      norm_num [pow_add, pow_mul]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

theorem preprocessBases_work_exp {m : ℕ}
    (A : Matrix (Fin (2 ^ m + m + 1)) (Fin m) ℤ) :
    (preprocessBases A).2 ≤ 2 ^ (5 * (m + 2) ^ 2) := by
  calc
    _ ≤ (2 ^ m + m + 1) ^ m * (basisCacheWork m + 1) := preprocessBases_work A
    _ ≤ (2 ^ (m + 2)) ^ m * 2 ^ (4 * (m + 2) ^ 2) :=
      Nat.mul_le_mul (Nat.pow_le_pow_left (normal_universe_bound m) _)
        (basisCacheWork_exp m)
    _ = 2 ^ ((m + 2) * m + 4 * (m + 2) ^ 2) := by rw [← pow_mul, ← pow_add]
    _ ≤ _ := Nat.pow_le_pow_right (by decide) (by nlinarith)

end NetworkSimplex.Chain.Threshold
