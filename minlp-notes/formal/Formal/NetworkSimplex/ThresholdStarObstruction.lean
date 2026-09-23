import Formal.NetworkSimplex.ThresholdBalancedRatio
import Formal.NetworkSimplex.ThresholdBalancedCounts
import Formal.NetworkSimplex.ThresholdStarFamily
import Formal.NetworkSimplex.ThresholdCycleRank

/-! An unbounded family of unavoidable original-coordinate coefficient ratios. -/
namespace NetworkSimplex.Chain.ThresholdStarFamily
open scoped BigOperators
noncomputable section

/-- Instantiate every hypothesis of the actual balanced-incidence hull theorem. -/
def sectionData (k : ℕ) (hk : 3 ≤ k) : Balanced.SectionData (k + 1) where
  S := S k
  alpha := balancingWeight k
  beta := k
  a := 1 / (2 * (k + 1 : ℕ))
  invertible := by
    have he : Balanced.incidenceMatrix (S k) = incidenceMatrix k := by
      ext i j
      simp [Balanced.incidenceMatrix, incidenceMatrix]
    rw [he]
    exact det_isUnit (by omega : 0 < k)
  nonempty := S_nonempty (by omega)
  proper := S_proper (by omega)
  positive := weight_positive (by omega)
  beta_pos := by exact_mod_cast (show 0 < k by omega)
  a_pos := (Balanced.normalization (by omega : 0 < k + 1)).1
  scale := (Balanced.normalization (by omega : 0 < k + 1)).2
  balance := by
    intro j
    simpa [Balanced.incidenceMatrix, incidenceMatrix] using balanced k j
  r := 0
  s := ⟨1, by omega⟩
  jr := 0
  js := ⟨2, by omega⟩
  distinct := by simp [Fin.ext_iff]
  r_forbidden := by simp [allowed]
  s_forbidden := by simp [allowed, Fin.ext_iff]

theorem sectionData_ratio (k : ℕ) (hk : 3 ≤ k) :
    (sectionData k hk).alpha (sectionData k hk).r /
      (sectionData k hk).alpha (sectionData k hk).s = (k : ℝ) - 1 := by
  simp [sectionData, balancingWeight, Fin.ext_iff]

/-- The ratio is forced in every finite description of the actual original-coordinate hull. -/
theorem every_description_ratio (k : ℕ) (hk : 3 ≤ k) {ι κ : Type*} [Finite ι]
    (rows : ι → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k)))
    (eqs : κ → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k)))
    (hd : ∀ q, q ∈ convexHull ℝ (Balanced.originalGraph (S k)) ↔
      (∀ i, 0 ≤ (rows i).eval q) ∧ (∀ j, (eqs j).eval q = 0)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧
      (rows i).product (sectionData k hk).oU = ((k : ℝ) - 1) * t ∧
      (rows i).product (sectionData k hk).oV = t := by
  obtain ⟨i, t, ht, _, hU, hV⟩ := (sectionData k hk).finite_description_ratio rows eqs hd
  exact ⟨i, t, ht, by simpa [sectionData, balancingWeight, Fin.ext_iff, mul_comm] using hU,
    by simpa [sectionData, balancingWeight, Fin.ext_iff] using hV⟩

/-- The denominator coefficient is positive, so the ratio is an actual quotient. -/
theorem every_description_quotient (k : ℕ) (hk : 3 ≤ k) {ι κ : Type*} [Finite ι]
    (rows : ι → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k)))
    (eqs : κ → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k)))
    (hd : ∀ q, q ∈ convexHull ℝ (Balanced.originalGraph (S k)) ↔
      (∀ i, 0 ≤ (rows i).eval q) ∧ (∀ j, (eqs j).eval q = 0)) :
    ∃ i, 0 < (rows i).product (sectionData k hk).oV ∧
      (rows i).product (sectionData k hk).oU /
        (rows i).product (sectionData k hk).oV = (k : ℝ) - 1 := by
  obtain ⟨i, t, ht, hU, hV⟩ := every_description_ratio k hk rows eqs hd
  refine ⟨i, by rwa [hV], ?_⟩
  rw [hU, hV, mul_div_cancel_right₀ _ (ne_of_gt ht)]

/-- These are the observations of the actual graph, not a separate matrix count. -/
theorem actual_observation_count (k : ℕ) :
    Fintype.card (Balanced.Obs (S k)) = 1 + k * (k - 1) := by
  rw [← Fintype.card_congr (Balanced.forbiddenObservationEquiv (S k))]
  exact observations_card k

/-- All stated sparse-instance dimensions, including the genuine cycle-space dimension. -/
theorem actual_counts (k : ℕ) :
    Fintype.card (Fin (k + 2)) = k + 2 ∧
    Fintype.card (ChainArc (k + 1)) = 2 * k + 3 ∧
    Fintype.card (Fin (k + 1)) = k + 1 ∧
    Fintype.card (Balanced.Obs (S k)) = 1 + k * (k - 1) ∧
    Module.finrank ℝ (LinearMap.ker (incidence (k + 1))) = k + 2 := by
  have h := graph_counts k
  exact ⟨h.1, h.2.1, h.2.2, actual_observation_count k, cycle_rank (k + 1)⟩

/-- No bound independent of the state count can bound the forced section ratios. -/
theorem unbounded_forced_section_ratio (B : ℝ) :
    ∃ N, ∃ D : Balanced.SectionData N, B < D.alpha D.r / D.alpha D.s := by
  obtain ⟨k, hk⟩ := exists_nat_gt (max (B + 1) 3)
  have hk3 : 3 ≤ k := by
    have hh : (3 : ℝ) < k := (le_max_right _ _).trans_lt hk
    exact_mod_cast hh.le
  refine ⟨k + 1, sectionData k hk3, ?_⟩
  rw [sectionData_ratio]
  have hb := (le_max_left _ _).trans_lt hk
  linarith

/-- The absence of a state-independent bound concerns every finite hull description. -/
theorem unbounded_every_description (B : ℝ) {ι κ : Type*} [Finite ι] :
    ∃ k : ℕ, ∃ hk : 3 ≤ k,
      ∀ (rows : ι → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k)))
        (eqs : κ → AffineRow (ChainArc (k + 1)) (Fin (k + 1)) (Balanced.Obs (S k))),
      (∀ q, q ∈ convexHull ℝ (Balanced.originalGraph (S k)) ↔
        (∀ i, 0 ≤ (rows i).eval q) ∧ (∀ j, (eqs j).eval q = 0)) →
      ∃ i, 0 < (rows i).product (sectionData k hk).oV ∧
        B < (rows i).product (sectionData k hk).oU /
          (rows i).product (sectionData k hk).oV := by
  obtain ⟨k, hk⟩ := exists_nat_gt (max (B + 1) 3)
  have hk3 : 3 ≤ k := by
    have hh : (3 : ℝ) < k := (le_max_right _ _).trans_lt hk
    exact_mod_cast hh.le
  refine ⟨k, hk3, ?_⟩
  intro rows eqs hd
  obtain ⟨i, hi, hq⟩ := every_description_quotient k hk3 rows eqs hd
  refine ⟨i, hi, ?_⟩
  rw [hq]
  have hb := (le_max_left _ _).trans_lt hk
  linarith

end
end NetworkSimplex.Chain.ThresholdStarFamily
