import QipmFormal.Preconditioner.Path

open scoped BigOperators Matrix
open Matrix

namespace QipmFormal.Preconditioner

/-- Vertex signs switch the signs on incident path edges. -/
def signMatrix {m : ℕ} (s : Fin m → ℝ) : Matrix (Fin m) (Fin m) ℝ := diagonal s

/-- Signed incidence with arbitrary edge signs; the sign at index zero is unused. -/
def signedPathIncidence {m : ℕ} (e : Fin m → ℝ) : Matrix (Fin m) (Fin m) ℝ :=
  fun i j => (if i = j then 1 else 0) - (if i.val = j.val + 1 then e i else 0)

lemma signMatrix_transpose {m : ℕ} (s : Fin m → ℝ) : (signMatrix s)ᵀ = signMatrix s := by
  simp [signMatrix]

lemma signMatrix_mulVec {m : ℕ} (s x : Fin m → ℝ) :
    signMatrix s *ᵥ x = fun i => s i * x i := by
  ext i
  simp [signMatrix, mulVec_diagonal]

lemma signMatrix_sq {m : ℕ} {s : Fin m → ℝ} (hs : ∀ i, s i ^ 2 = 1) :
    signMatrix s * signMatrix s = 1 := by
  rw [signMatrix, diagonal_mul_diagonal]
  ext i j
  simp [← pow_two, hs]

lemma signMatrix_orthogonal {m : ℕ} {s : Fin m → ℝ} (hs : ∀ i, s i ^ 2 = 1) :
    (signMatrix s)ᵀ * signMatrix s = 1 := by
  rw [signMatrix_transpose, signMatrix_sq hs]

lemma signMatrix_norm_sq {m : ℕ} {s : Fin m → ℝ} (hs : ∀ i, s i ^ 2 = 1)
    (x : Fin m → ℝ) : (∑ i, (signMatrix s *ᵥ x) i ^ 2) = ∑ i, x i ^ 2 := by
  simp [signMatrix_mulVec, mul_pow, hs]

lemma signMatrix_pathIncidence {m : ℕ} {s e : Fin m → ℝ}
    (hs : ∀ i, s i ^ 2 = 1)
    (he : ∀ i j : Fin m, i.val = j.val + 1 → s i * s j = e i) :
    signMatrix s * pathIncidence m * signMatrix s = signedPathIncidence e := by
  ext i j
  simp only [signMatrix, mul_diagonal, diagonal_mul, pathIncidence, signedPathIncidence]
  by_cases hij : i = j
  · subst j
    simp [← pow_two, hs]
  · by_cases hnext : i.val = j.val + 1
    · simp [hij, hnext, ← he i j hnext]
    · simp [hij, hnext]

lemma signMatrix_pathMatrix {m : ℕ} {s e : Fin m → ℝ}
    (hs : ∀ i, s i ^ 2 = 1)
    (he : ∀ i j : Fin m, i.val = j.val + 1 → s i * s j = e i) :
    signMatrix s * pathMatrix m * signMatrix s =
      signedPathIncidence e * (signedPathIncidence e)ᵀ := by
  rw [← signMatrix_pathIncidence hs he, transpose_mul, transpose_mul, signMatrix_transpose]
  simp only [pathMatrix, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc (signMatrix s) (signMatrix s), signMatrix_sq hs, one_mul]

/-- Cumulative edge-sign products, with the root sign immaterial. -/
def pathVertexSigns {m : ℕ} (e : Fin m → ℝ) (i : Fin m) : ℝ :=
  ∏ k ∈ Finset.range (i.val + 1), if hk : k < m then e ⟨k, hk⟩ else 1

lemma pathVertexSigns_sq {m : ℕ} {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1)
    (i : Fin m) : pathVertexSigns e i ^ 2 = 1 := by
  unfold pathVertexSigns
  rw [← Finset.prod_pow]
  apply Finset.prod_eq_one
  intro k hk
  have hkm : k < m := by have := Finset.mem_range.mp hk; omega
  simp [hkm, he]

lemma pathVertexSigns_succ {m : ℕ} (e : Fin m → ℝ) (i j : Fin m)
    (hij : i.val = j.val + 1) : pathVertexSigns e i = pathVertexSigns e j * e i := by
  unfold pathVertexSigns
  rw [hij, Finset.prod_range_succ]
  congr 1
  simp only [← hij, dif_pos i.isLt]

lemma pathVertexSigns_edge {m : ℕ} {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1)
    (i j : Fin m) (hij : i.val = j.val + 1) :
    pathVertexSigns e i * pathVertexSigns e j = e i := by
  rw [pathVertexSigns_succ e i j hij]
  calc
    _ = (pathVertexSigns e j)^2 * e i := by ring
    _ = e i := by rw [pathVertexSigns_sq he, one_mul]

/-- Every legal signed path is an orthogonal diagonal switching of the unsigned path. -/
lemma signedPathIncidence_switching {m : ℕ} {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1) :
    signMatrix (pathVertexSigns e) * pathIncidence m * signMatrix (pathVertexSigns e) =
      signedPathIncidence e :=
  signMatrix_pathIncidence (pathVertexSigns_sq he) (pathVertexSigns_edge he)

lemma signedPathMatrix_switching {m : ℕ} {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1) :
    signMatrix (pathVertexSigns e) * pathMatrix m * signMatrix (pathVertexSigns e) =
      signedPathIncidence e * (signedPathIncidence e)ᵀ :=
  signMatrix_pathMatrix (pathVertexSigns_sq he) (pathVertexSigns_edge he)

end QipmFormal.Preconditioner
