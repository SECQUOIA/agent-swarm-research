import Formal.MatroidSpectral.SpectralCover
import Formal.DAGSpectral.Criteria
import Formal.DAGSpectral.CriteriaCost
import Formal.DAGSpectral.PseudoinverseOrder

/-! Criterion consequences for a verified cover of actual selected sets.
`F` and `C` are semantic families; these results do not enumerate `F`.
Singular costs use extended nonnegative reals. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped ENNReal NNReal

variable {p m M : ℕ} (D : FactorData p m M)
  {F C : Finset (Finset (Fin m))} {η ε : ℝ}

theorem cover_homogeneous_maximum
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hη : η ≤ 1) {a : ℝ} {Φ : RealMatrix p → ℝ}
    (hΦ : HomogeneousCriterion a Φ) :
    ∃ B ∈ C, (∀ S ∈ C, Φ (ratMatrixReal (information D S)) ≤
      Φ (ratMatrixReal (information D B))) ∧
      ∀ S ∈ F, (1-η)^a * Φ (ratMatrixReal (information D S)) ≤
        Φ (ratMatrixReal (information D B)) :=
  h.homogeneous_maximum hF (fun S _ => information_real_psd D S) hη hΦ

theorem cover_determinant_maximum
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hη : η ≤ 1) :
    ∃ B ∈ C, (∀ S ∈ C, (ratMatrixReal (information D S)).det ≤
      (ratMatrixReal (information D B)).det) ∧
      ∀ S ∈ F, (1-η)^p * (ratMatrixReal (information D S)).det ≤
        (ratMatrixReal (information D B)).det := by
  apply h.maximize hF (fun S => (ratMatrixReal (information D S)).det)
    (fun S => (1-η)^p * (ratMatrixReal (information D S)).det)
  intro S _ B _ hSB
  exact hSB.det_lower (information_real_psd D S) (information_real_psd D B) hη

theorem cover_D_optimality
    (h : IsRelativeCover (ε / p) (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hp : 0 < p) (hε : 0 ≤ ε) (hε1 : ε ≤ 1) :
    ∃ B ∈ C, (∀ S ∈ C, (ratMatrixReal (information D S)).det ≤
      (ratMatrixReal (information D B)).det) ∧
      ∀ S ∈ F, (1-ε) * (ratMatrixReal (information D S)).det ≤
        (ratMatrixReal (information D B)).det :=
  h.determinant_maximum hF (fun S _ => information_real_psd D S) hp hε hε1

theorem cover_determinantRoot_maximum
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hη : η ≤ 1) (hp : 0 < p) :
    ∃ B ∈ C, (∀ S ∈ C, determinantRoot (ratMatrixReal (information D S)) ≤
      determinantRoot (ratMatrixReal (information D B))) ∧
      ∀ S ∈ F, (1-η) * determinantRoot (ratMatrixReal (information D S)) ≤
        determinantRoot (ratMatrixReal (information D B)) :=
  h.determinantRoot_maximum hF (fun S _ => information_real_psd D S) hη hp

theorem cover_E_optimality [NeZero p]
    (h : IsRelativeCover ε (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hε1 : ε ≤ 1) :
    ∃ B ∈ C, (∀ S ∈ C, minimumEigenvalue (ratMatrixReal (information D S)) ≤
      minimumEigenvalue (ratMatrixReal (information D B))) ∧
      ∀ S ∈ F, (1-ε) * minimumEigenvalue (ratMatrixReal (information D S)) ≤
        minimumEigenvalue (ratMatrixReal (information D B)) :=
  h.eigenvalue_maximum hF (fun S _ => information_real_psd D S) hε1

theorem cover_E_all_singular [NeZero p]
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hsing : ∀ S ∈ F, (ratMatrixReal (information D S)).det = 0) :
    ∀ B ∈ C, minimumEigenvalue (ratMatrixReal (information D B)) = 0 :=
  h.eigenvalue_all_singular (fun S _ => information_real_psd D S) hsing

theorem cover_inverseTrace_minimum
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    ∃ B ∈ C, (∀ S ∈ C, inverseTraceCost (ratMatrixReal (information D B)) ≤
      inverseTraceCost (ratMatrixReal (information D S))) ∧
      ∀ S ∈ F, inverseTraceCost (ratMatrixReal (information D B)) ≤
        ENNReal.ofReal ((1-η)⁻¹) * inverseTraceCost (ratMatrixReal (information D S)) :=
  h.inverseTrace_minimum hF hη0 hη1

theorem cover_A_optimality
    (h : IsRelativeCover (ε / (1 + ε)) (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hε : 0 ≤ ε) :
    ∃ B ∈ C, (∀ S ∈ C, inverseTraceCost (ratMatrixReal (information D B)) ≤
      inverseTraceCost (ratMatrixReal (information D S))) ∧
      ∀ S ∈ F, inverseTraceCost (ratMatrixReal (information D B)) ≤
        ENNReal.ofReal (1 + ε) * inverseTraceCost (ratMatrixReal (information D S)) :=
  h.inverseTrace_minimum_eps hF hε

theorem cover_positiveDefinite_exists_iff
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hη1 : η < 1) :
    (∃ S ∈ F, (ratMatrixReal (information D S)).PosDef) ↔
      ∃ B ∈ C, (ratMatrixReal (information D B)).PosDef :=
  h.positiveDefinite_exists_iff hη1

theorem information_pseudoInverse_sandwich (S T : Finset (Fin m))
    (h : RelativeSandwich η (ratMatrixReal (information D S))
      (ratMatrixReal (information D T))) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    Loewner ((1+η)⁻¹ • DAGSpectral.pseudoInverse (ratMatrixReal (information D S))
      (information_real_psd D S).isHermitian)
      (DAGSpectral.pseudoInverse (ratMatrixReal (information D T))
        (information_real_psd D T).isHermitian) ∧
    Loewner (DAGSpectral.pseudoInverse (ratMatrixReal (information D T))
      (information_real_psd D T).isHermitian)
      ((1-η)⁻¹ • DAGSpectral.pseudoInverse (ratMatrixReal (information D S))
        (information_real_psd D S).isHermitian) :=
  h.pseudoInverse (information_real_psd D S) (information_real_psd D T) hη0 hη1

theorem cover_estimable_exists_iff
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hη1 : η < 1) (c : Fin p → ℝ) :
    (∃ S ∈ F, Estimable (ratMatrixReal (information D S)) c) ↔
      ∃ B ∈ C, Estimable (ratMatrixReal (information D B)) c :=
  h.estimable_exists_iff (fun S _ => information_real_psd D S) hη1 c

theorem cover_contrast_minimum
    (h : IsRelativeCover (ε / (1 + ε)) (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hε : 0 ≤ ε) (c : Fin p → ℝ) :
    ∃ B ∈ C, (∀ S ∈ C, contrastCost (ratMatrixReal (information D B)) c ≤
      contrastCost (ratMatrixReal (information D S)) c) ∧
      ∀ S ∈ F, contrastCost (ratMatrixReal (information D B)) c ≤
        ENNReal.ofReal (1 + ε) * contrastCost (ratMatrixReal (information D S)) c :=
  h.contrast_minimum_eps hF (fun S _ => information_real_psd D S) hε c

theorem cover_weightedContrast_minimum {κ : Type*} [Fintype κ]
    (h : IsRelativeCover (ε / (1 + ε)) (fun S => ratMatrixReal (information D S)) F C)
    (hF : F.Nonempty) (hε : 0 ≤ ε) (w : κ → ℝ≥0) (c : κ → Fin p → ℝ) :
    ∃ B ∈ C, (∀ S ∈ C, weightedContrastCost w c (ratMatrixReal (information D B)) ≤
      weightedContrastCost w c (ratMatrixReal (information D S))) ∧
      ∀ S ∈ F, weightedContrastCost w c (ratMatrixReal (information D B)) ≤
        ENNReal.ofReal (1 + ε) * weightedContrastCost w c (ratMatrixReal (information D S)) :=
  h.weightedContrast_minimum_eps hF (fun S _ => information_real_psd D S) hε w c

theorem cover_add_prior
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (hη : 0 ≤ η) (H : RealMatrix p) (hH : H.PosSemidef) :
    IsRelativeCover η (fun S => ratMatrixReal (information D S) + H) F C :=
  h.add_prior hη hH

theorem cover_congruence {k : ℕ}
    (h : IsRelativeCover η (fun S => ratMatrixReal (information D S)) F C)
    (K : Matrix (Fin k) (Fin p) ℝ) :
    IsRelativeCover η (fun S => K * ratMatrixReal (information D S) * Kᵀ) F C :=
  h.congruence K

end MatroidSpectral
