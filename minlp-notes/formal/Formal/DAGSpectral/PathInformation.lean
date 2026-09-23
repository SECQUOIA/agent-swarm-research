import Formal.DAGSpectral.PathMatrix
import Formal.DAGSpectral.NormalizationData

namespace DAGSpectral
open Matrix
open scoped BigOperators

variable {E : Type*} {p r : ℕ}

theorem pathMatrix_congruence (K : Matrix (Fin r) (Fin p) ℝ)
    (Q0 : RealMatrix p) (Q : E → RealMatrix p) (es : List E) :
    pathMatrix (K * Q0 * Kᵀ) (fun e => K * Q e * Kᵀ) es =
      K * pathMatrix Q0 Q es * Kᵀ := by
  have hh : (es.map (fun e => K * Q e * Kᵀ)).sum = K * (es.map Q).sum * Kᵀ := by
    induction es with
    | nil => simp
    | cons e es ih => simp only [List.map_cons, List.sum_cons, Matrix.mul_add,
        Matrix.add_mul, ih]
  simp only [pathMatrix, Matrix.mul_add, Matrix.add_mul, hh]

theorem ratMatrixReal_list_sum {E : Type*} {p : ℕ}
    (Q : E → Matrix (Fin p) (Fin p) ℚ) (es : List E) :
    ratMatrixReal (es.map Q).sum = (es.map (fun e => ratMatrixReal (Q e))).sum := by
  induction es with
  | nil => simp
  | cons e es ih => simp only [List.map_cons, List.sum_cons, ratMatrixReal_add, ih]

namespace NormalizationTrials
variable {m M : ℕ}

theorem pathMatrix_eq_information (D : FactorData p m M) (es : List (Fin m))
    (hn : es.Nodup) :
    pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es =
      ratMatrixReal (information D es.toFinset) := by
  have hs := List.sum_toFinset (fun e => D.atom (some e)) hn
  simp only [information, ratMatrixReal_add, hs, ratMatrixReal_list_sum, pathMatrix]

theorem transformed_pathMatrix_eq (D : FactorData p m M) (s : Finset (Fin M))
    (es : List (Fin m)) (hn : es.Nodup) :
    pathMatrix
      (ratMatrixReal (transform D.vector D.weight s * D.atom none *
        (transform D.vector D.weight s)ᵀ))
      (fun e => ratMatrixReal (transform D.vector D.weight s * D.atom (some e) *
        (transform D.vector D.weight s)ᵀ)) es =
    ratMatrixReal (transform D.vector D.weight s * information D es.toFinset *
      (transform D.vector D.weight s)ᵀ) := by
  simp only [ratMatrixReal_mul, ratMatrixReal_transpose]
  rw [pathMatrix_congruence, pathMatrix_eq_information D es hn]

end NormalizationTrials
end DAGSpectral
