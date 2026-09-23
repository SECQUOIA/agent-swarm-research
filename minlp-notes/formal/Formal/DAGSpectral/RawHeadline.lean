import Formal.DAGSpectral.Headline
import Formal.DAGSpectral.TopologicalPath

namespace DAGSpectral
open Matrix NormalizationTrials

/-- Feasible paths in an arbitrarily numbered input DAG. This finite semantic
domain is used in the statement, not enumerated by the cover algorithm. -/
noncomputable def rawFeasiblePaths {v m : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v) : Finset (List (Fin m)) :=
  feasiblePaths (topologicallyOrderedGraph src dst ha)
    (topologicalOrder src dst ha s) (topologicalOrder src dst ha t)

theorem mem_rawFeasiblePaths {v m : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v) (es : List (Fin m)) :
    es ∈ rawFeasiblePaths src dst ha s t ↔ RawPath src dst s t es := by
  rw [rawFeasiblePaths, mem_feasiblePaths, ← rawPath_iff_ordered ha]

/-- The original-input algorithm also computes its own topological ordering.
Both the returned edge identifiers and the rational matrix data are unchanged. -/
def rawDagSpectralCover {v m p : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) : Finset (List (Fin m)) :=
  dagSpectralCover (topologicallyOrderedGraph src dst ha)
    (topologicalOrder src dst ha s) (topologicalOrder src dst ha t) Q0 Q hQ0 hQ η

theorem rawDagSpectralCover_isRelativeCover {v m p : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    IsRelativeCover (η : ℝ) (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)))
      (rawFeasiblePaths src dst ha s t) (rawDagSpectralCover src dst ha s t Q0 Q hQ0 hQ η) :=
  dagSpectralCover_isRelativeCover _ _ _ Q0 Q hQ0 hQ η hη

theorem rawDagSpectralCover_empty_iff {v m p : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    rawDagSpectralCover src dst ha s t Q0 Q hQ0 hQ η = ∅ ↔
      ¬ ∃ es, RawPath src dst s t es := by
  simp only [rawDagSpectralCover, dagSpectralCover_empty_iff _ _ _ _ _ _ _ η hη,
    ← rawPath_iff_ordered ha]

theorem rawDagSpectralCover_kernel {v m p : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη0 : 0 < η) (hη1 : η < 1) (es : List (Fin m))
    (he : RawPath src dst s t es) :
    ∃ fs ∈ rawDagSpectralCover src dst ha s t Q0 Q hQ0 hQ η,
      RawPath src dst s t fs ∧
      RelativeSandwich (η : ℝ)
        (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) es)
        (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) fs) ∧
      ∀ x, pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) es *ᵥ x = 0 ↔
        pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) fs *ᵥ x = 0 := by
  obtain ⟨fs, hf, hp, hr, hk⟩ := dagSpectralCover_kernel _ _ _ Q0 Q hQ0 hQ η hη0 hη1
    es (he.toOrdered ha)
  exact ⟨fs, hf, (rawPath_iff_ordered ha).mpr hp, hr, hk⟩

theorem rawDagSpectralCover_card {v m p : ℕ} (src dst : Fin m → Fin v)
    (ha : RawAcyclic src dst) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    (rawDagSpectralCover src dst ha s t Q0 Q hQ0 hQ η).card ≤
      coverCardinalityBound p (indexedFactorCount (priorAtomMatrices Q0 Q))
        (max 1 (v-1)) (η : ℝ) :=
  dagSpectralCover_card _ _ _ Q0 Q hQ0 hQ η hη

end DAGSpectral
