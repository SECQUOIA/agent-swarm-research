import Formal.DAGSpectral.Perturbation
import Formal.DAGSpectral.Rounding

namespace DAGSpectral
open scoped BigOperators
open Matrix

variable {E : Type*} {r : ℕ}

def pathMatrix (A0 : RealMatrix r) (A : E → RealMatrix r) (es : List E) : RealMatrix r :=
  A0 + (es.map A).sum

theorem pathMatrix_entry (A0 : RealMatrix r) (A : E → RealMatrix r) (es : List E)
    (i j : Fin r) : pathMatrix A0 A es i j = A0 i j + (es.map (fun e => A e i j)).sum := by
  induction es with
  | nil => simp [pathMatrix]
  | cons e es ih => simp only [pathMatrix, List.map_cons, List.sum_cons,
      Matrix.add_apply] at ih ⊢; linarith

theorem pathMatrix_hermitian {A0 : RealMatrix r} {A : E → RealMatrix r}
    (h0 : A0.IsHermitian) (hA : ∀ e, (A e).IsHermitian) (es : List E) :
    (pathMatrix A0 A es).IsHermitian := by
  apply h0.add
  induction es with
  | nil => simp
  | cons e es ih => simpa only [List.map_cons, List.sum_cons] using (hA e).add ih

theorem pathMatrix_psd {A0 : RealMatrix r} {A : E → RealMatrix r}
    (h0 : A0.PosSemidef) (hA : ∀ e, (A e).PosSemidef) (es : List E) :
    (pathMatrix A0 A es).PosSemidef := by
  apply h0.add
  induction es with
  | nil => simpa using (Matrix.PosSemidef.zero : (0 : RealMatrix r).PosSemidef)
  | cons e es ih => simpa only [List.map_cons, List.sum_cons] using (hA e).add ih

theorem pathMatrix_entry_close {A0 : RealMatrix r} {A : E → RealMatrix r}
    (h0 : A0.IsHermitian) (hA : ∀ e, (A e).IsHermitian)
    {h : ℝ} (hh : 0 < h) {N : ℕ} (hN : 0 < N) (es fs : List E)
    (he : es.length ≤ N) (hf : fs.length ≤ N)
    (hlabels : ∀ i j : Fin r, i ≤ j →
      pathLabel h (es.map (fun e => A e i j)) = pathLabel h (fs.map (fun e => A e i j))) :
    ∀ i j, |(pathMatrix A0 A fs - pathMatrix A0 A es) i j| < N * h := by
  have hc (i j : Fin r) (hij : i ≤ j) :
      |(pathMatrix A0 A fs - pathMatrix A0 A es) i j| < N * h := by
    have hx := equal_label_sum_close hh hN (fs.map (fun e => A e i j))
      (es.map (fun e => A e i j)) (by simpa using hf) (by simpa using he)
      (hlabels i j hij).symm
    simpa only [Matrix.sub_apply, pathMatrix_entry, add_sub_add_left_eq_sub] using hx
  intro i j
  rcases le_total i j with hij | hji
  · exact hc i j hij
  · have hs := (pathMatrix_hermitian h0 hA fs).sub (pathMatrix_hermitian h0 hA es)
    have heq := congrFun (congrFun hs.eq j) i
    simp only [Matrix.conjTranspose_apply, star_trivial] at heq
    rw [heq]
    exact hc j i hji

theorem pathMatrix_relativeSandwich {A0 : RealMatrix r} {A : E → RealMatrix r}
    (h0 : A0.IsHermitian) (hA : ∀ e, (A e).IsHermitian)
    {η : ℝ} (hη : 0 < η) (hr : 0 < r) {N : ℕ} (hN : 0 < N)
    (es fs : List E) (he : es.length ≤ N) (hf : fs.length ≤ N)
    (hfloor : Loewner 1 (pathMatrix A0 A es))
    (hlabels : ∀ i j : Fin r, i ≤ j →
      pathLabel (spectralMesh η r N) (es.map (fun e => A e i j)) =
      pathLabel (spectralMesh η r N) (fs.map (fun e => A e i j))) :
    RelativeSandwich η (pathMatrix A0 A es) (pathMatrix A0 A fs) := by
  have hh := spectralMesh_pos hη hr hN
  apply relativeSandwich_of_entrywise (pathMatrix_hermitian h0 hA es)
    (pathMatrix_hermitian h0 hA fs) hfloor (mul_nonneg (Nat.cast_nonneg N) hh.le)
  · exact le_of_eq (by simpa only [mul_assoc] using rank_mul_mesh (η := η) hr hN)
  · exact fun i j => (pathMatrix_entry_close h0 hA hh hN es fs he hf hlabels i j).le

end DAGSpectral
