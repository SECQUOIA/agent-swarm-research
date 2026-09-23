import Formal.DAGSpectral.Headline

open DAGSpectral Matrix
open scoped Matrix

def reviewParallel : ExplicitDAG 2 2 where
  src _ := 0
  dst _ := 1
  forward _ := by decide

def reviewSingle : ExplicitDAG 2 1 where
  src _ := 0
  dst _ := 1
  forward _ := by decide

def reviewNoEdges : ExplicitDAG 2 0 where
  src := Fin.elim0
  dst := Fin.elim0
  forward e := Fin.elim0 e

def reviewTriangle : ExplicitDAG 3 3 where
  src := ![0, 1, 0]
  dst := ![1, 2, 2]
  forward e := by fin_cases e <;> decide

def reviewDiag (a b : ℚ) : Matrix (Fin 2) (Fin 2) ℚ := diagonal ![a,b]

theorem reviewDiagPSD (a b : ℚ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    (ratMatrixReal (reviewDiag a b)).PosSemidef := by
  rw [reviewDiag, ratMatrixReal_diagonal]
  apply Matrix.posSemidef_diagonal_iff.mpr
  intro i
  fin_cases i
  · simpa using (show (0 : ℝ) ≤ (a : ℝ) by exact_mod_cast ha)
  · simpa using (show (0 : ℝ) ≤ (b : ℝ) by exact_mod_cast hb)

def reviewSingularAtoms (e : Fin 2) : Matrix (Fin 2) (Fin 2) ℚ :=
  reviewDiag (if e = 0 then 1 else 0) (if e = 0 then 0 else 1)

theorem reviewSingularPSD (e : Fin 2) : (ratMatrixReal (reviewSingularAtoms e)).PosSemidef := by
  apply reviewDiagPSD <;> split_ifs <;> norm_num

def reviewSingularCover := dagSpectralCover reviewParallel 0 1
  (reviewDiag 0 0) reviewSingularAtoms (reviewDiagPSD 0 0 (by norm_num) (by norm_num))
  reviewSingularPSD (1/2)

def reviewMixedAtoms (e : Fin 2) : Matrix (Fin 2) (Fin 2) ℚ :=
  reviewDiag (if e = 0 then 0 else 1) 0

theorem reviewMixedPSD (e : Fin 2) : (ratMatrixReal (reviewMixedAtoms e)).PosSemidef := by
  apply reviewDiagPSD
  · split_ifs <;> norm_num
  · norm_num

def reviewMixedCover := dagSpectralCover reviewParallel 0 1
  (reviewDiag 0 0) reviewMixedAtoms (reviewDiagPSD 0 0 (by norm_num) (by norm_num))
  reviewMixedPSD (1/2)

def reviewOneOwnerCover := dagSpectralCover reviewSingle 0 1
  (reviewDiag 0 0) (fun _ => reviewDiag 1 1)
  (reviewDiagPSD 0 0 (by norm_num) (by norm_num))
  (fun _ => reviewDiagPSD 1 1 (by norm_num) (by norm_num)) (1/2)

def reviewNoPathCover := dagSpectralCover reviewNoEdges 0 1
  (reviewDiag 1 1) (fun e => Fin.elim0 e)
  (reviewDiagPSD 1 1 (by norm_num) (by norm_num)) (fun e => Fin.elim0 e) (1/2)

def reviewSelfCover := dagSpectralCover reviewSingle 0 0
  (reviewDiag 1 1) (fun _ => reviewDiag 1 1)
  (reviewDiagPSD 1 1 (by norm_num) (by norm_num))
  (fun _ => reviewDiagPSD 1 1 (by norm_num) (by norm_num)) (1/2)

def reviewPriorOnlyCover := dagSpectralCover reviewTriangle 0 2
  (reviewDiag 1 1) (fun _ => reviewDiag 0 0)
  (reviewDiagPSD 1 1 (by norm_num) (by norm_num))
  (fun _ => reviewDiagPSD 0 0 (by norm_num) (by norm_num)) (1/2)

def reviewDimensionZeroCover := dagSpectralCover reviewParallel 0 1
  (0 : Matrix (Fin 0) (Fin 0) ℚ) (fun _ => 0)
  (by simp only [ratMatrixReal_zero]; exact Matrix.PosSemidef.zero)
  (fun _ => by simp only [ratMatrixReal_zero]; exact Matrix.PosSemidef.zero) (1/2)

-- Runtime assertions create no proof declarations or native-decision axioms.
#eval do
  unless decide (reviewSingularCover = {[0], [1]}) do
    throw (IO.userError "Different singular ranges were not both retained")
  unless decide (reviewMixedCover = {[0], [1]}) do
    throw (IO.userError "Mixed rank-zero/rank-one cover failed")
  unless decide (reviewOneOwnerCover = {[0]}) do
    throw (IO.userError "Repeated-owner factors failed")
  unless decide (reviewNoPathCover = ∅) do
    throw (IO.userError "Infeasible graph output was not empty")
  unless decide (reviewSelfCover = {[]}) do
    throw (IO.userError "Source-equals-target output failed")
  unless decide (reviewPriorOnlyCover.card = 1 ∧
      ∀ es ∈ reviewPriorOnlyCover, es = [2] ∨ es = [0,1]) do
    throw (IO.userError "Unequal-length paths with a common prior failed to merge")
  unless decide (reviewDimensionZeroCover.card = 1 ∧
      ∀ es ∈ reviewDimensionZeroCover, es = [0] ∨ es = [1]) do
    throw (IO.userError "Dimension-zero branch failed")
  IO.println "Seven raw-input cover boundary checks passed."

#print axioms dagSpectralCover_isRelativeCover
#print axioms dagSpectralCover_empty_iff
#print axioms dagSpectralCover_kernel
#print axioms dagSpectralCover_card
