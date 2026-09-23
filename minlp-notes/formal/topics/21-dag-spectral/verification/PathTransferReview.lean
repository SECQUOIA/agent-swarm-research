import Formal.DAGSpectral.TrialApproximation
import Formal.DAGSpectral.Transfer
open DAGSpectral Matrix

-- Rational labels use mathematical floor at a negative off-diagonal entry.
example : rationalUpperLabels (1/2 : ℚ)
    (fun _ : Fin 1 => !![1, -(1/4 : ℚ); -(1/4 : ℚ), 1]) 0
    ((upperCoordEquiv 2).symm ⟨(0,1), by decide⟩) = -1 := by norm_num [rationalUpperLabels, upperCoordEquiv]

-- A common prior cancels even for unequal-length edge lists.
example {E : Type*} {r : ℕ} (A0 : RealMatrix r) (A : E → RealMatrix r)
    (es fs : List E) (i j : Fin r) :
    (pathMatrix A0 A fs - pathMatrix A0 A es) i j =
      (fs.map (fun e => A e i j)).sum - (es.map (fun e => A e i j)).sum := by
  simp only [Matrix.sub_apply, pathMatrix_entry, add_sub_add_left_eq_sub]

-- No lower spectral floor on the representative is an input hypothesis.
example {E : Type*} {r N : ℕ} {A0 : RealMatrix r} {A : E → RealMatrix r}
    (h0 : A0.IsHermitian) (hA : ∀ e, (A e).IsHermitian)
    {η : ℝ} (hη : 0 < η) (hr : 0 < r) (hN : 0 < N)
    (es fs : List E) (he : es.length ≤ N) (hf : fs.length ≤ N)
    (hfloor : Loewner 1 (pathMatrix A0 A es))
    (hl : ∀ i j : Fin r, i ≤ j →
      pathLabel (spectralMesh η r N) (es.map (fun e => A e i j)) =
      pathLabel (spectralMesh η r N) (fs.map (fun e => A e i j))) :
    Loewner ((1-η) • pathMatrix A0 A es) (pathMatrix A0 A fs) ∧
      Loewner (pathMatrix A0 A fs) ((1+η) • pathMatrix A0 A es) :=
  pathMatrix_relativeSandwich h0 hA hη hr hN es fs he hf hfloor hl

-- The transfer handles rank-zero matrices without invertibility assumptions.
example (n : ℕ) {ε δ : ℝ} (he0 : 0 < ε) (he1 : ε < 1)
    (hd0 : 0 ≤ δ) (hd : δ ≤ ε/8) :
    RelativeSandwich ε (0 : RealMatrix n) 0 := by
  have h0 (a : ℝ) : RelativeSandwich a (0 : RealMatrix n) 0 := by
    simp [RelativeSandwich, Loewner, Matrix.PosSemidef.zero]
  exact relative_cover_transfer_accuracy Matrix.PosSemidef.zero he0 he1 hd0 hd
    (h0 δ) (h0 δ) (h0 (ε/4))

-- The maximal admitted graph error is included, rather than assumed strict.
example :
    1 - ((1-(1/2:ℝ)/4)*(1-(1/2:ℝ)/8)/(1+(1/2:ℝ)/8)) ≤ (1/2:ℝ)/2 ∧
    ((1+(1/2:ℝ)/4)*(1+(1/2:ℝ)/8)/(1-(1/2:ℝ)/8))-1 ≤ 17*(1/2:ℝ)/28 := by
  exact transfer_factors_accuracy (by norm_num) (by norm_num) (by norm_num) le_rfl

#print axioms pathMatrix_entry_close
#print axioms pathMatrix_relativeSandwich
#print axioms rationalUpperLabels_profile
#print axioms trial_output_relative
#print axioms relative_cover_transfer
#print axioms transfer_factors_accuracy
#print axioms relative_cover_transfer_accuracy
