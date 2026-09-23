import Formal.QuadraticAggregation.Recession
import Mathlib.Analysis.LocallyConvex.Separation
import Mathlib.Analysis.Convex.Topology
import Mathlib.LinearAlgebra.Pi
import Mathlib.Algebra.BigOperators.Field

open Set Finset

namespace QuadraticAggregation

/-- Separation from the strict negative orthant gives normalized nonnegative weights. -/
theorem exists_simplex_separator {m : ℕ} {C : Set (Fin m → ℝ)}
    (hC : Convex ℝ C) (hzero : 0 ∈ C)
    (hmiss : ∀ y ∈ C, ¬ ∀ i, y i < 0) :
    ∃ w : Fin m → ℝ, (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
      ∀ y ∈ C, 0 ≤ ∑ i, w i * y i := by
  classical
  let N : Set (Fin m → ℝ) := {y | ∀ i, y i < 0}
  have hN : Convex ℝ N := by
    intro x hx y hy a b ha hb hab i
    exact (convex_Iio (0 : ℝ)) (hx i) (hy i) ha hb hab
  have hoN : IsOpen N := by
    simpa only [N, ← Set.ofPred_forall] using
      (isOpen_iInter_of_finite fun i : Fin m =>
        isOpen_lt (continuous_apply i) (continuous_const : Continuous fun _ : Fin m → ℝ => (0 : ℝ)))
  obtain ⟨f, u, hNf, hCf⟩ := geometric_hahn_banach_open hN hoN hC
    (Set.disjoint_left.mpr fun y hy hyC => hmiss y hyC hy)
  let w : Fin m → ℝ := fun i => f (Pi.single i 1)
  have hf (y : Fin m → ℝ) : f y = ∑ i, w i * y i := by
    conv_lhs => rw [← Finset.univ_sum_single y]
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro i hi
    have : Pi.single i (y i) = y i • Pi.single i (1 : ℝ) := by
      ext j
      by_cases h : j = i <;> simp [h]
    rw [this, map_smul]
    simp [w, mul_comm]
  have hu : u ≤ 0 := by simpa using hCf 0 hzero
  have hn : f (fun _ => -1) < 0 := lt_of_lt_of_le (hNf _ (fun _ => by norm_num)) hu
  have hw : ∀ i, 0 ≤ w i := by
    intro i
    by_contra hnwi
    have hwi : w i < 0 := lt_of_not_ge hnwi
    let t := (f (fun _ => -1) - 1) / w i
    have ht : 0 ≤ t := le_of_lt (div_pos_of_neg_of_neg (by linarith) hwi)
    have hneg : (fun _ => -1) - t • Pi.single i (1 : ℝ) ∈ N := by
      intro j
      by_cases h : j = i
      · simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, h, Pi.single_eq_same, mul_one]
        linarith
      · simp [h]
    have hv := lt_of_lt_of_le (hNf _ hneg) hu
    rw [map_sub, map_smul] at hv
    have he : t * w i = f (fun _ => -1) - 1 := by
      dsimp [t]
      exact div_mul_cancel₀ _ (ne_of_lt hwi)
    change f (fun _ => -1) - t * w i < 0 at hv
    linarith
  have hsum : 0 < ∑ i, w i := by
    rw [hf] at hn
    simpa using hn
  have hCy : ∀ y ∈ C, 0 ≤ ∑ i, w i * y i := by
    intro y hy
    by_contra hny
    have hfy : f y < 0 := by rw [hf]; exact lt_of_not_ge hny
    let z : Fin m → ℝ := fun _ => f y / (2 * ∑ i, w i)
    have hz : z ∈ N := fun i => div_neg_of_neg_of_pos hfy (by positivity)
    have hzf : f z = f y / 2 := by
      rw [hf]
      simp only [z, ← Finset.sum_mul]
      field_simp
    have hh := lt_of_lt_of_le (hNf z hz) (hCf y hy)
    rw [hzf] at hh
    linarith
  refine ⟨fun i => w i / ∑ j, w j, fun i => div_nonneg (hw i) hsum.le, ?_, ?_⟩
  · rw [← Finset.sum_div, div_self (ne_of_gt hsum)]
  · intro y hy
    simpa only [div_mul_eq_mul_div, ← Finset.sum_div] using
      div_nonneg (hCy y hy) hsum.le

/-- Every proper open quadratic hull has a strict supporting halfspace. -/
theorem System.exists_strict_support {n m : ℕ} (D : System n m)
    (hne : D.feasible.Nonempty) (hproper : convexHull ℝ D.feasible ≠ Set.univ) :
    ∃ α : Vec n, α ≠ 0 ∧ ∃ β : ℝ, ∀ x ∈ D.feasible, dotProduct α x < β := by
  classical
  obtain ⟨y, hy⟩ := (Set.ne_univ_iff_exists_notMem _).mp hproper
  obtain ⟨f, hf⟩ := geometric_hahn_banach_open_point (convex_convexHull ℝ D.feasible)
    D.isOpen_feasible.convexHull hy
  let α : Vec n := fun i => f (Pi.single i 1)
  have heval (x : Vec n) : f x = dotProduct α x := by
    conv_lhs => rw [← Finset.univ_sum_single x]
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro i hi
    have he : Pi.single i (x i) = x i • Pi.single i (1 : ℝ) := by
      ext j
      by_cases h : j = i <;> simp [h]
    rw [he, map_smul]
    simp [α, mul_comm]
  have hα : α ≠ 0 := by
    intro h
    obtain ⟨x, hx⟩ := hne
    have hh := hf x (subset_convexHull ℝ D.feasible hx)
    simp [heval, h] at hh
  exact ⟨α, hα, f y, fun x hx => by
    rw [← heval]
    exact hf x (subset_convexHull ℝ D.feasible hx)⟩

/-- A convex homogeneous image missing the strict negative orthant has a simplex certificate. -/
theorem System.hyperplane_certificate {n m : ℕ} (D : System n m)
    {α : Vec n} {s : ℝ} (hs : s ≠ 0)
    (hconv : Convex ℝ (D.homEval '' hyperplane α s))
    (hmiss : Disjoint (hyperplane α s) D.homFeasible) :
    ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
      ∀ x : Vec n, 0 ≤ q (D.aggA w) x +
        2 * (dotProduct α x / s) * dotProduct (D.aggB w) x +
        D.aggC w * (dotProduct α x / s) ^ 2 := by
  obtain ⟨w, hw, hsum, hsep⟩ := exists_simplex_separator hconv
    (by exact ⟨(0, 0), by simp [hyperplane], D.homEval_origin⟩)
    (by rintro y ⟨z, hz, rfl⟩ hneg
        exact Set.disjoint_left.mp hmiss hz hneg)
  refine ⟨w, hw, hsum, fun x => ?_⟩
  have hz : (x, dotProduct α x / s) ∈ hyperplane α s := by
    change dotProduct α x = s * (dotProduct α x / s)
    field_simp
  have h := hsep _ (Set.mem_image_of_mem D.homEval hz)
  rwa [D.agg_homEval] at h

/-- Supporting halfspaces exclude the sweeping hyperplanes from strict homogeneous feasibility. -/
theorem System.sweep_disjoint {n m : ℕ} (D : System n m)
    {α : Vec n} {β s : ℝ}
    (hsupport : ∀ x ∈ D.feasible, dotProduct α x < β)
    (hrec : ∀ v : Vec n, ¬ ∀ i, q (D.A i) v < 0)
    (hs : β ≤ s) : Disjoint (hyperplane α s) D.homFeasible := by
  apply Set.disjoint_left.mpr
  rintro ⟨x, t⟩ hplane hfeas
  by_cases ht : t = 0
  · subst t
    exact hrec x (fun i => by simpa using hfeas i)
  · have hf := hsupport (t⁻¹ • x) (D.dehomogenize_mem ht hfeas)
    rw [dot_dehomogenize ht hplane] at hf
    exact (not_lt_of_ge hs) hf

/-- Proper feasible hulls provide certificates on arbitrarily distant sweeping hyperplanes. -/
theorem System.exists_unbounded_certificates {n m : ℕ} (D : System n m)
    (hne : D.feasible.Nonempty) (hproper : convexHull ℝ D.feasible ≠ Set.univ)
    (hHC : D.AsymptoticHC) :
    ∃ α : Vec n, α ≠ 0 ∧ ∀ R : ℝ, ∃ s : ℝ, R < s ∧ 0 < s ∧
      ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        ∀ x : Vec n, 0 ≤ q (D.aggA w) x +
          2 * (dotProduct α x / s) * dotProduct (D.aggB w) x +
          D.aggC w * (dotProduct α x / s) ^ 2 := by
  obtain ⟨α, hα, β, hsupp⟩ := D.exists_strict_support hne hproper
  refine ⟨α, hα, fun R => ?_⟩
  obtain ⟨s, hs, hc⟩ := hHC α hα (max R (max β 0))
  have hRs : R < s := lt_of_le_of_lt (le_max_left _ _) hs
  have hβs : β ≤ s := (le_trans (le_max_left β 0) (le_max_right R (max β 0))).trans hs.le
  have hspos : 0 < s := lt_of_le_of_lt
    (le_trans (le_max_right β 0) (le_max_right R (max β 0))) hs
  refine ⟨s, hRs, hspos, ?_⟩
  exact D.hyperplane_certificate (ne_of_gt hspos) hc
    (D.sweep_disjoint hsupp (D.no_negative_recession hproper) hβs)

end QuadraticAggregation
