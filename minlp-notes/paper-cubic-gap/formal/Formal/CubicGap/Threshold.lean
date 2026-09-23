import Formal.CubicGap.Families
import Formal.CubicGap.Laws

namespace CubicGap

noncomputable section

def twoThresholdVertex (m : ℕ) (t : Fin 4) : Vertex (Fin 2 × Fin m) :=
  fun i => if i.1 = 0 then decide (t.val < 2) else decide (t.val < 3)

def threeThresholdVertex (m : ℕ) (t : Fin 4) : Vertex (Fin 3 × Fin m) :=
  fun i => if i.1 = 0 then decide (t.val < 1)
    else if i.1 = 1 then decide (t.val < 2) else decide (t.val < 3)

def twoThreshold (m : ℕ) : Law (Vertex (Fin 2 × Fin m)) :=
  (Law.uniform (Fin 4)).map (twoThresholdVertex m)

def threeThreshold (m : ℕ) : Law (Vertex (Fin 3 × Fin m)) :=
  (Law.uniform (Fin 4)).map (threeThresholdVertex m)

def thresholdTwoMeans (m : ℕ) (i : Fin 2 × Fin m) : ℝ := if i.1 = 0 then 1/2 else 3/4

def thresholdThreeMeans (m : ℕ) (i : Fin 3 × Fin m) : ℝ :=
  if i.1 = 0 then 1/4 else if i.1 = 1 then 1/2 else 3/4

theorem twoThreshold_mean (m : ℕ) (i : Fin 2 × Fin m) :
    (twoThreshold m).expect (fun v => vertexPoint v i) = thresholdTwoMeans m i := by
  rcases i with ⟨g,i⟩
  fin_cases g <;> norm_num [twoThreshold, Law.expect_map, Law.expect_uniform,
    Function.comp_def, twoThresholdVertex, vertexPoint, thresholdTwoMeans, Fin.sum_univ_succ] <;>
    norm_num [show (Finset.univ.filter (fun x : Fin 4 => x.val ≤ 1)).card = 2 by decide,
      show (Finset.univ.filter (fun x : Fin 4 => x.val < 3)).card = 3 by decide]

theorem threeThreshold_mean (m : ℕ) (i : Fin 3 × Fin m) :
    (threeThreshold m).expect (fun v => vertexPoint v i) = thresholdThreeMeans m i := by
  rcases i with ⟨g,i⟩
  fin_cases g <;> norm_num [threeThreshold, Law.expect_map, Law.expect_uniform,
    Function.comp_def, threeThresholdVertex, vertexPoint, thresholdThreeMeans,
    Fin.sum_univ_succ] <;>
    norm_num [show (Finset.univ.filter (fun x : Fin 4 => x.val ≤ 1)).card = 2 by decide,
      show (Finset.univ.filter (fun x : Fin 4 => x.val < 3)).card = 3 by decide]

theorem twoThreshold_value (m : ℕ) :
    (twoThreshold m).expect (fun v => twoFamily m (vertexPoint v)) = (twoUpper m : ℝ) := by
  simp [twoThreshold, Law.expect_map, Law.expect_uniform, Function.comp_def,
    Fin.sum_univ_succ, twoFamily, twoThresholdVertex, vertexPoint, elementary_const, twoUpper]
  ring

theorem threeThreshold_value (m : ℕ) (coef : Fin 6 → ℚ) :
    (threeThreshold m).expect (fun v => threeFamily m coef (vertexPoint v)) =
      (orbitUpper m coef : ℝ) := by
  simp [threeThreshold, Law.expect_map, Law.expect_uniform, Function.comp_def,
    Fin.sum_univ_succ, threeFamily, threeThresholdVertex, vertexPoint, elementary_const, orbitUpper]
  ring

end
end CubicGap
