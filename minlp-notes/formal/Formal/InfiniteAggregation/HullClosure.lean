import Formal.InfiniteAggregation.HullModel
import Formal.InfiniteAggregation.GramConcavity

/-! The closure of the explicit hull region, including its degenerate boundary. -/

open Set Filter
open scoped Topology

noncomputable section

namespace InfiniteAggregation

variable {r : ℕ}

theorem isClosed_closedRegion : IsClosed (closedRegion r) := by
  have hq : Continuous (qnorm : Vec r → ℝ) := by
    unfold qnorm dot dotProduct
    fun_prop
  have hd : Continuous (fun x : Var r => dot x.1 x.2) := by
    unfold dot dotProduct
    fun_prop
  exact (isClosed_le (hq.comp continuous_fst) continuous_const).inter
    ((isClosed_le (hq.comp continuous_snd) continuous_const).inter
      (isClosed_le continuous_const (hd.add
        (Real.continuous_sqrt.comp
          ((continuous_const.sub (hq.comp continuous_fst)).mul
            (continuous_const.sub (hq.comp continuous_snd)))))))

theorem smul_mem_hullRegion {x : Var r} (hx : x ∈ closedRegion r)
    {s : ℝ} (hs : 0 ≤ s) (hs1 : s < 1) : s • x ∈ hullRegion r := by
  rcases hx with ⟨hu, hv, hc⟩
  have hk : 0 ≤ s ^ 2 := sq_nonneg s
  have hk1 : s ^ 2 < 1 := by nlinarith
  have hpu : GramPSD (1 - qnorm x.1) (1 - qnorm x.2) 0 :=
    ⟨sub_nonneg.mpr hu, sub_nonneg.mpr hv, by
      simpa using mul_nonneg (sub_nonneg.mpr hu) (sub_nonneg.mpr hv)⟩
  have hp0 : GramPSD 1 1 0 := by norm_num [GramPSD]
  have hg := gram_det_concave hpu hp0 hk (sub_nonneg.mpr hk1.le)
  simp only [zero_pow (by omega : 2 ≠ 0), sub_zero, mul_zero, add_zero,
    mul_one, Real.sqrt_one] at hg
  have he : s ^ 2 * (1 - qnorm x.1) + (1 - s ^ 2) =
      1 - s ^ 2 * qnorm x.1 := by ring
  have hf : s ^ 2 * (1 - qnorm x.2) + (1 - s ^ 2) =
      1 - s ^ 2 * qnorm x.2 := by ring
  rw [he, hf] at hg
  change qnorm (s • x.1) < 1 ∧ qnorm (s • x.2) < 1 ∧
    1 / 2 < dot (s • x.1) (s • x.2) +
      Real.sqrt ((1 - qnorm (s • x.1)) * (1 - qnorm (s • x.2)))
  simp only [qnorm_smul, dot_smul_left, dot_smul_right]
  refine ⟨lt_of_le_of_lt (mul_le_mul_of_nonneg_left hu hk) (by simpa using hk1),
    lt_of_le_of_lt (mul_le_mul_of_nonneg_left hv hk) (by simpa using hk1), ?_⟩
  have hc' := mul_le_mul_of_nonneg_left hc hk
  nlinarith

theorem closure_hullRegion_eq_closedRegion : closure (hullRegion r) = closedRegion r := by
  apply Subset.antisymm
  · exact closure_minimal hullRegion_subset_closedRegion isClosed_closedRegion
  · intro x hx
    have ht : Tendsto (fun s : ℝ => s • x) (𝓝[<] 1) (𝓝 x) := by
      simpa using ((show Continuous (fun s : ℝ => s • x) by fun_prop).continuousWithinAt
        (s := Iio (1 : ℝ)) (x := 1)).tendsto
    apply mem_closure_of_tendsto ht
    filter_upwards [self_mem_nhdsWithin,
      (show ∀ᶠ s : ℝ in 𝓝[<] 1, 0 < s from
        (eventually_gt_nhds (by norm_num : (0 : ℝ) < 1)).filter_mono nhdsWithin_le_nhds)]
      with s hs hs0
    exact smul_mem_hullRegion hx hs0.le hs

theorem closedRegion_bounded : Bornology.IsBounded (closedRegion r) := by
  apply isBounded_iff_forall_norm_le.2
  refine ⟨1, fun x hx => ?_⟩
  rw [Prod.norm_def, max_le_iff]
  exact ⟨norm_le_one_of_qnorm_le_one hx.1, norm_le_one_of_qnorm_le_one hx.2.1⟩

theorem isCompact_closedRegion : IsCompact (closedRegion r) :=
  Metric.isCompact_of_isClosed_isBounded isClosed_closedRegion closedRegion_bounded

theorem isClosed_weakFeasible : IsClosed (weakFeasible r) := by
  simp only [weakFeasible, ofPred_forall]
  exact isClosed_iInter fun i => isClosed_le
    ((continuous_apply i).comp continuous_eval) continuous_const

theorem weakFeasible_bounded : Bornology.IsBounded (weakFeasible r) := by
  apply isBounded_iff_forall_norm_le.2
  refine ⟨1, fun x hx => ?_⟩
  have h := (mem_weakFeasible_iff x).1 hx
  rw [Prod.norm_def, max_le_iff]
  exact ⟨norm_le_one_of_qnorm_le_one h.1, norm_le_one_of_qnorm_le_one h.2.1⟩

theorem isCompact_weakFeasible : IsCompact (weakFeasible r) :=
  Metric.isCompact_of_isClosed_isBounded isClosed_weakFeasible weakFeasible_bounded

/-- All segments between two points of the weak system form a compact set. -/
def weakSegments (r : ℕ) : Set (Var r) :=
  (fun p : ℝ × (Var r × Var r) => p.1 • p.2.1 + (1 - p.1) • p.2.2) ''
    (Icc 0 1 ×ˢ (weakFeasible r ×ˢ weakFeasible r))

theorem isCompact_weakSegments : IsCompact (weakSegments r) := by
  apply (isCompact_Icc.prod (isCompact_weakFeasible.prod isCompact_weakFeasible)).image
  fun_prop

theorem weakSegments_subset_convexHull : weakSegments r ⊆ convexHull ℝ (weakFeasible r) := by
  rintro x ⟨⟨t, y, z⟩, ⟨ht, hy, hz⟩, rfl⟩
  exact convex_convexHull ℝ _ (subset_convexHull ℝ _ hy) (subset_convexHull ℝ _ hz)
    ht.1 (sub_nonneg.mpr ht.2) (by ring)

end InfiniteAggregation
