import Formal.InfiniteAggregation.AccuracyUpperGeometry
import Formal.InfiniteAggregation.AccuracyAngular
import Formal.InfiniteAggregation.AccuracyMesh
import Formal.InfiniteAggregation.AccuracyModel
import Formal.InfiniteAggregation.AccuracyConstants

/-! Uniform finite angular cuts and their Euclidean Hausdorff error. -/
noncomputable section
open Set
namespace InfiniteAggregation

theorem mem_closedRegion_iff_angular {r : ℕ} (hr : 2 ≤ r) (x : Var r) :
    x ∈ closedRegion r ↔ ∀ t ∈ Icc 0 (Real.pi / 2), 0 ≤ pointAngularForm x t := by
  constructor
  · intro hx t ht
    rw [pointAngularForm_eq_neg_aggregate]
    have hg := good_closedHull_valid (angleWeight_good hr ht)
      (show x ∈ closure (convexHull ℝ (feasible r)) by
        rwa [closure_convexHull_feasible_eq_closedRegion hr])
    linarith
  · exact angular_tests_subset_closedRegion

theorem euclideanDist_radial_le {r : ℕ} {x : Var r} {s a : ℝ}
    (hu : qnorm x.1 ≤ 1) (hv : qnorm x.2 ≤ 1)
    (hs1 : s ≤ 1) (hsa : 1 - s ≤ a) :
    euclideanDist x (s • x) ≤ Real.sqrt 2 * a := by
  unfold euclideanDist
  rw [euclidean_smul, dist_eq_norm]
  have heq : euclidean x - s • euclidean x = (1 - s) • euclidean x := by
    rw [sub_smul, one_smul]
  rw [heq, norm_smul, Real.norm_eq_abs, abs_of_nonneg (by linarith)]
  calc
    (1 - s) * ‖euclidean x‖ ≤ (1 - s) * Real.sqrt 2 :=
      mul_le_mul_of_nonneg_left (euclidean_norm_le_sqrt_two hu hv) (by linarith)
    _ ≤ Real.sqrt 2 * a := by nlinarith [Real.sqrt_nonneg 2]

/-- Every point satisfying a covering family admits a nearby point of the exact hull. -/
theorem angle_samples_repair {r : ℕ} (T : Set ℝ) {ρ : ℝ}
    (hzero : 0 ∈ T) (hpi : Real.pi / 2 ∈ T)
    (hcover : ∀ t ∈ Icc 0 (Real.pi / 2), ∃ s ∈ T, |s - t| ≤ ρ)
    {x : Var r} (hx : ∀ t ∈ T, aggregate (angleWeight t) x ≤ 0) :
    ∃ y ∈ closedRegion r, euclideanDist x y ≤ 5 * Real.sqrt 2 * ρ ^ 2 := by
  have hnonneg : ∀ t ∈ T, 0 ≤ pointAngularForm x t := by
    intro t ht
    rw [pointAngularForm_eq_neg_aggregate]
    linarith [hx t ht]
  have hu : qnorm x.1 ≤ 1 := by
    have := hnonneg 0 hzero
    rw [pointAngularForm_zero] at this
    linarith
  have hv : qnorm x.2 ≤ 1 := by
    have := hnonneg (Real.pi / 2) hpi
    rw [pointAngularForm_pi_div_two] at this
    linarith
  have hb : -(3 / 2 : ℝ) ≤ dot x.1 x.2 - 1 / 2 := by
    have := qnorm_nonneg (x.1 + x.2)
    rw [qnorm_add] at this
    linarith
  have hlower : ∀ t ∈ Icc 0 (Real.pi / 2), -(5 * ρ ^ 2) ≤ pointAngularForm x t := by
    intro t ht
    simpa only [pointAngularForm, angularForm, neg_mul] using
      angular_sample_lower_bound (1 - qnorm x.1) (dot x.1 x.2 - 1 / 2)
      (1 - qnorm x.2) ρ T ⟨by linarith, by linarith [qnorm_nonneg x.1]⟩
      ⟨by linarith, by linarith [qnorm_nonneg x.2]⟩ hb hcover hnonneg t ht
  obtain ⟨s, _hs, hs1, hsa, hmem⟩ := radial_repair (by positivity : 0 ≤ 5 * ρ ^ 2) hlower
  refine ⟨s • x, hmem, ?_⟩
  have hd := euclideanDist_radial_le hu hv hs1 hsa
  nlinarith

/-- A reusable error bound for arbitrary finite angular meshes. -/
theorem hausdorffError_angle_samples_le {r : ℕ} (hr : 2 ≤ r) (T : Finset ℝ) {ρ : ℝ}
    (hT : (T : Set ℝ) ⊆ Icc 0 (Real.pi / 2))
    (hzero : 0 ∈ T) (hpi : Real.pi / 2 ∈ T)
    (hcover : ∀ t ∈ Icc 0 (Real.pi / 2), ∃ s ∈ T, |s - t| ≤ ρ) :
    hausdorffError r (T.image angleWeight) ≤ ENNReal.ofReal (5 * Real.sqrt 2 * ρ ^ 2) := by
  apply hausdorffError_le_of_repair hr
  · intro w hw
    obtain ⟨t, ht, rfl⟩ := Finset.mem_image.1 hw
    exact angleWeight_good hr (hT ht)
  · intro x hx
    apply angle_samples_repair (T : Set ℝ) hzero hpi hcover
    intro t ht
    exact hx _ (Finset.mem_image_of_mem _ ht)

/-- The explicit equally spaced family, with the endpoint ball cuts. -/
def angleCuts (N : ℕ) : Finset Weight := (angleMesh N).image angleWeight

theorem card_angleCuts_le (N : ℕ) : (angleCuts N).card ≤ N :=
  (Finset.card_image_le).trans (card_angleMesh_le N)

theorem angleCuts_admissible {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    admissibleFamily r (angleCuts N) := by
  intro w hw
  obtain ⟨t, ht, rfl⟩ := Finset.mem_image.1 hw
  exact angleWeight_good hr (angleMesh_subset_Icc hN ht)

/-- Exact uniform upper constant, for all ambient dimensions in the construction. -/
theorem hausdorffError_angleCuts_le {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    hausdorffError r (angleCuts N) ≤ ENNReal.ofReal (accuracyUpperBound N) := by
  have h := hausdorffError_angle_samples_le hr (angleMesh N)
    (angleMesh_subset_Icc hN) (zero_mem_angleMesh hN) (pi_div_two_mem_angleMesh hN)
    (ρ := Real.pi / (4 * (N - 1 : ℕ))) (by
      intro t ht
      obtain ⟨s, hs, hd⟩ := exists_mem_angleMesh_dist_le hN ht
      exact ⟨s, hs, by rwa [abs_sub_comm]⟩)
  have hid : 5 * Real.sqrt 2 * (Real.pi / (4 * (N - 1 : ℕ))) ^ 2 =
      accuracyUpperBound N := by
    rw [Nat.cast_sub (by omega : 1 ≤ N), Nat.cast_one]
    unfold accuracyUpperBound
    rw [div_pow]
    ring
  simpa only [angleCuts, hid] using h

end InfiniteAggregation
