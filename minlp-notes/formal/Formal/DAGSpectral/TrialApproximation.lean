import Formal.DAGSpectral.PathMatrix
import Formal.DAGSpectral.ProfileDP
import Formal.DAGSpectral.UpperTriangle
import Formal.DAGSpectral.RatMatrix

namespace DAGSpectral
open Matrix

/-- Actual rational labels on the upper triangle; no real floor is executed. -/
def rationalUpperLabels {m r : ℕ} (h : ℚ)
    (A : Fin m → Matrix (Fin r) (Fin r) ℚ) : Fin m → UpperCoord r → ℤ :=
  fun e z => ⌊A e (upperCoordEquiv r z).val.1 (upperCoordEquiv r z).val.2 / h⌋

theorem rationalUpperLabels_profile {m r : ℕ} (h : ℚ)
    (A : Fin m → Matrix (Fin r) (Fin r) ℚ) (es : List (Fin m))
    (i j : Fin r) (hij : i ≤ j) :
    ExplicitDAG.profile (rationalUpperLabels h A) es
      ((upperCoordEquiv r).symm ⟨(i,j),hij⟩) =
    pathLabel (h : ℝ) (es.map (fun e => ratMatrixReal (A e) i j)) := by
  rw [ExplicitDAG.profile_apply]
  have hc := pathLabel_ratCast h (es.map (fun e => A e i j))
  simpa only [List.map_map, Function.comp_def, rationalUpperLabels,
    Equiv.apply_symm_apply, ratMatrixReal_apply] using hc.symm

/-- A terminal state produces a single actual feasible representative satisfying
both PSD inequalities. The hypotheses here are exactly the normalization
properties later supplied by the trial construction. -/
theorem trial_output_relative {v m r : ℕ} (G : ExplicitDAG v m)
    (allowed : Fin m → Bool) (s t : Fin v) (required : Finset (Fin m))
    (A0 : Matrix (Fin r) (Fin r) ℚ) (A : Fin m → Matrix (Fin r) (Fin r) ℚ)
    (h0 : (ratMatrixReal A0).IsHermitian) (hA : ∀ e, (ratMatrixReal (A e)).IsHermitian)
    (η : ℚ) (hη : 0 < η) (hr : 0 < r)
    (es : List (Fin m)) (he : G.AllowedPath allowed s t es) (hf : required ⊆ es.toFinset)
    (hfloor : Loewner 1 (pathMatrix (ratMatrixReal A0) (fun e => ratMatrixReal (A e)) es)) :
    let N := max 1 (v - 1)
    let h := η / (r * N : ℚ)
    ∃ fs ∈ G.output allowed s t required (rationalUpperLabels h A),
      G.AllowedPath allowed s t fs ∧ required ⊆ fs.toFinset ∧
      RelativeSandwich (η : ℝ)
        (pathMatrix (ratMatrixReal A0) (fun e => ratMatrixReal (A e)) es)
        (pathMatrix (ratMatrixReal A0) (fun e => ratMatrixReal (A e)) fs) := by
  dsimp only
  let N := max 1 (v - 1)
  let h : ℚ := η / (r * N)
  obtain ⟨fs,hfs,hkey⟩ := G.output_complete allowed s required (rationalUpperLabels h A)
    t es he hf
  obtain ⟨hpath,howner⟩ := G.output_sound allowed s required (rationalUpperLabels h A) t hfs
  refine ⟨fs,hfs,hpath,howner,?_⟩
  have hN : 0 < N := lt_of_lt_of_le Nat.zero_lt_one (le_max_left _ _)
  have hmesh : (h : ℝ) = spectralMesh (η : ℝ) r N := by
    simp [h, spectralMesh]
  apply pathMatrix_relativeSandwich h0 hA (by exact_mod_cast hη) hr hN es fs
    (he.1.length_le_vertices.trans (le_max_right _ _))
    (hpath.1.length_le_vertices.trans (le_max_right _ _)) hfloor
  intro i j hij
  have hp := congrArg Prod.snd hkey
  have hv := congrFun hp ((upperCoordEquiv r).symm ⟨(i,j),hij⟩)
  change ExplicitDAG.profile (rationalUpperLabels h A) fs _ =
    ExplicitDAG.profile (rationalUpperLabels h A) es _ at hv
  rw [rationalUpperLabels_profile, rationalUpperLabels_profile, hmesh] at hv
  exact hv.symm

end DAGSpectral
