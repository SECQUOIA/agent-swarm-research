import Formal.InfiniteAggregation.HullRepresentations

/-! Euclidean Hausdorff approximation by finite families of actual good aggregations. -/

open Set
open scoped ENNReal

noncomputable section

namespace InfiniteAggregation

/-- The Euclidean geometry of the original `2r` real coordinates. -/
abbrev EuclideanVar (r : ℕ) := EuclideanSpace ℝ (Fin r ⊕ Fin r)

def euclidean {r : ℕ} (x : Var r) : EuclideanVar r :=
  WithLp.toLp 2 (Sum.elim x.1 x.2)

def euclideanDist {r : ℕ} (x y : Var r) : ℝ := dist (euclidean x) (euclidean y)

@[simp] theorem euclidean_sub {r : ℕ} (x y : Var r) :
    euclidean (x - y) = euclidean x - euclidean y := by
  ext i
  cases i <;> rfl

@[simp] theorem euclidean_smul {r : ℕ} (s : ℝ) (x : Var r) :
    euclidean (s • x) = s • euclidean x := by
  ext i
  cases i <;> rfl

theorem euclidean_injective (r : ℕ) : Function.Injective (@euclidean r) := by
  intro x y h
  apply Prod.ext
  · funext i
    exact congrArg (fun z : EuclideanVar r => z (Sum.inl i)) h
  · funext i
    exact congrArg (fun z : EuclideanVar r => z (Sum.inr i)) h

theorem euclidean_surjective (r : ℕ) : Function.Surjective (@euclidean r) := by
  intro z
  refine ⟨((fun i => z (Sum.inl i)), (fun i => z (Sum.inr i))), ?_⟩
  ext i
  cases i <;> rfl

theorem euclidean_norm_sq {r : ℕ} (x : Var r) :
    ‖euclidean x‖ ^ 2 = qnorm x.1 + qnorm x.2 := by
  rw [EuclideanSpace.real_norm_sq_eq, Fintype.sum_sum_type]
  simp [euclidean, qnorm, dot, dotProduct, pow_two]

theorem euclideanDist_sq {r : ℕ} (x y : Var r) :
    euclideanDist x y ^ 2 = qnorm (x.1 - y.1) + qnorm (x.2 - y.2) := by
  rw [euclideanDist, dist_eq_norm, ← euclidean_sub, euclidean_norm_sq]
  rfl

theorem euclideanDist_comm {r : ℕ} (x y : Var r) :
    euclideanDist x y = euclideanDist y x := dist_comm _ _

theorem euclideanDist_triangle {r : ℕ} (x y z : Var r) :
    euclideanDist x z ≤ euclideanDist x y + euclideanDist y z := dist_triangle _ _ _

theorem euclidean_norm_le_sqrt_two {r : ℕ} {x : Var r}
    (hu : qnorm x.1 ≤ 1) (hv : qnorm x.2 ≤ 1) : ‖euclidean x‖ ≤ Real.sqrt 2 := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hn := euclidean_norm_sq x
  have hp := norm_nonneg (euclidean x)
  have hq := Real.sqrt_nonneg (2 : ℝ)
  nlinarith

theorem continuous_euclidean (r : ℕ) : Continuous (@euclidean r) := by
  apply (PiLp.continuous_toLp 2 (fun _ : Fin r ⊕ Fin r => ℝ)).comp
  apply continuous_pi
  intro i
  cases i with
  | inl i => exact (continuous_apply i).comp continuous_fst
  | inr i => exact (continuous_apply i).comp continuous_snd

/-- Coordinate identification as a linear homeomorphism, preserving hulls and closure. -/
def euclideanEquiv (r : ℕ) : Var r ≃L[ℝ] EuclideanVar r :=
  LinearEquiv.toContinuousLinearEquiv {
    toFun := euclidean
    invFun := fun z => ((fun i => z (Sum.inl i)), (fun i => z (Sum.inr i)))
    left_inv := fun x => by rfl
    right_inv := fun z => by ext i; cases i <;> rfl
    map_add' := fun x y => by ext i; cases i <;> rfl
    map_smul' := fun s x => euclidean_smul s x }

theorem euclidean_closedRegion_eq_closedHull {r : ℕ} (hr : 2 ≤ r) :
    euclidean '' closedRegion r = closure (convexHull ℝ (euclidean '' feasible r)) := by
  rw [← closure_convexHull_feasible_eq_closedRegion hr]
  change (euclideanEquiv r).toHomeomorph '' closure (convexHull ℝ (feasible r)) = _
  rw [(euclideanEquiv r).toHomeomorph.image_closure]
  change closure ((euclideanEquiv r).toLinearMap '' convexHull ℝ (feasible r)) = _
  rw [(euclideanEquiv r).toLinearMap.image_convexHull]
  rfl

/-- All original points satisfying every selected weak aggregation. -/
def relaxation {r : ℕ} (W : Finset Weight) : Set (Var r) :=
  {x | ∀ w ∈ W, aggregate w x ≤ 0}

/-- Goodness is the original spectral-and-validity property, not a surrogate. -/
def admissibleFamily (r : ℕ) (W : Finset Weight) : Prop := ∀ w ∈ W, Good r w

/-- Extended Euclidean Hausdorff error, including infinity for unbounded relaxations. -/
def hausdorffError (r : ℕ) (W : Finset Weight) : ℝ≥0∞ :=
  Metric.hausdorffEDist (euclidean '' closedRegion r) (euclidean '' relaxation W)

/-- Infimum over all families with at most `N` cuts; no attainment is asserted. -/
def optimalError (r N : ℕ) : ℝ≥0∞ :=
  ⨅ W : Finset Weight, ⨅ (_ : admissibleFamily r W ∧ W.card ≤ N), hausdorffError r W

theorem closedRegion_subset_relaxation {r : ℕ} (hr : 2 ≤ r) {W : Finset Weight}
    (hW : admissibleFamily r W) : closedRegion r ⊆ relaxation W := by
  intro x hx w hw
  apply good_closedHull_valid (hW w hw)
  rwa [closure_convexHull_feasible_eq_closedRegion hr]

theorem isCompact_euclidean_closedRegion (r : ℕ) :
    IsCompact (euclidean '' closedRegion r) :=
  isCompact_closedRegion.image (continuous_euclidean r)

theorem zero_mem_closedRegion (r : ℕ) : (0 : Var r) ∈ closedRegion r := by
  norm_num [closedRegion, qnorm, dot, dotProduct]

theorem euclidean_closedRegion_nonempty (r : ℕ) :
    (euclidean '' closedRegion r).Nonempty :=
  ⟨euclidean 0, mem_image_of_mem _ (zero_mem_closedRegion r)⟩

/-- A pointwise repair in the original coordinates yields a Hausdorff upper bound. -/
theorem hausdorffError_le_of_repair {r : ℕ} (hr : 2 ≤ r) {W : Finset Weight}
    (hW : admissibleFamily r W) {B : ℝ}
    (hrepair : ∀ x ∈ relaxation W, ∃ y ∈ closedRegion r, euclideanDist x y ≤ B) :
    hausdorffError r W ≤ ENNReal.ofReal B := by
  apply Metric.hausdorffEDist_le_of_mem_edist
  · rintro _ ⟨x, hx, rfl⟩
    exact ⟨euclidean x, mem_image_of_mem _ (closedRegion_subset_relaxation hr hW hx),
      by simp⟩
  · rintro _ ⟨x, hx, rfl⟩
    obtain ⟨y, hy, hxy⟩ := hrepair x hx
    refine ⟨euclidean y, mem_image_of_mem _ hy, ?_⟩
    rw [edist_dist]
    exact ENNReal.ofReal_le_ofReal hxy

/-- One admitted witness separated from every hull point yields a lower bound. -/
theorem le_hausdorffError_of_witness {r : ℕ} {W : Finset Weight} {x : Var r}
    (hx : x ∈ relaxation W) {B : ℝ}
    (hsep : ∀ y ∈ closedRegion r, B ≤ euclideanDist x y) :
    ENNReal.ofReal B ≤ hausdorffError r W := by
  have h := Metric.infEDist_le_hausdorffEDist_of_mem
    (t := euclidean '' closedRegion r) (mem_image_of_mem euclidean hx)
  rw [Metric.hausdorffEDist_comm] at h
  apply le_trans _ h
  rw [Metric.le_infEDist]
  rintro _ ⟨y, hy, rfl⟩
  rw [edist_dist]
  exact ENNReal.ofReal_le_ofReal (hsep y hy)

/-- An unbounded relaxation has genuinely infinite error under this definition. -/
theorem hausdorffError_eq_top_of_unbounded {r : ℕ} {W : Finset Weight}
    (hP : ¬ Bornology.IsBounded (euclidean '' (relaxation W : Set (Var r)))) :
    hausdorffError r W = ⊤ := by
  by_contra hfinite
  obtain ⟨n, hn⟩ := ENNReal.exists_nat_gt hfinite
  apply hP
  rw [isBounded_iff_forall_norm_le]
  refine ⟨(n : ℝ) + Real.sqrt 2, ?_⟩
  intro x hx
  have hd : Metric.hausdorffEDist (euclidean '' (relaxation W : Set (Var r)))
      (euclidean '' closedRegion r) < (n : ℝ≥0∞) := by
    rw [Metric.hausdorffEDist_comm]
    exact hn
  obtain ⟨y, hy, hxy⟩ := Metric.exists_edist_lt_of_hausdorffEDist_lt hx hd
  obtain ⟨z, hz, rfl⟩ := hy
  have hdist : dist x (euclidean z) < (n : ℝ) := by
    simpa only [edist_dist, ← ENNReal.ofReal_natCast,
      ENNReal.ofReal_lt_ofReal_iff_of_nonneg (dist_nonneg : 0 ≤ dist x (euclidean z))] using hxy
  have hz' := euclidean_norm_le_sqrt_two hz.1 hz.2.1
  have hnorm : ‖x‖ ≤ dist x (euclidean z) + ‖euclidean z‖ := by
    simpa only [dist_eq_norm] using norm_le_norm_sub_add x (euclidean z)
  linarith

theorem optimalError_le_family {r N : ℕ} {W : Finset Weight}
    (hW : admissibleFamily r W) (hcard : W.card ≤ N) :
    optimalError r N ≤ hausdorffError r W :=
  iInf_le_of_le W (iInf_le_of_le ⟨hW, hcard⟩ le_rfl)

theorem le_optimalError {r N : ℕ} {B : ℝ≥0∞}
    (h : ∀ W, admissibleFamily r W → W.card ≤ N → B ≤ hausdorffError r W) :
    B ≤ optimalError r N := by
  exact le_iInf fun W => le_iInf fun hW => h W hW.1 hW.2

end InfiniteAggregation
