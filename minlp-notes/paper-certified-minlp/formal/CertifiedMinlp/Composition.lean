import Mathlib.Analysis.Convex.SpecificFunctions.Pow
import Mathlib.Analysis.Convex.Mul
import Mathlib.Analysis.Normed.Module.Convex

/-! Scalar composition rules for the sufficient curvature checker. Domain hypotheses concern
all points of the certified convex set, including any admitted zero endpoint. -/
namespace CertifiedMinlp
namespace Composition

open Set

variable {E : Type*} [AddCommGroup E] [Module ℝ E]
variable {s : Set E} {t : Set ℝ} {v : E → ℝ} {u : ℝ → ℝ}

/-- Convex nondecreasing outer function and convex inner function. -/
theorem convex_mono (hv : ConvexOn ℝ s v) (hu : ConvexOn ℝ t u)
    (hm : MonotoneOn u t) (hr : MapsTo v s t) :
    ConvexOn ℝ s (fun x => u (v x)) := by
  refine ⟨hv.1, fun x hx y hy a b ha hb hab => ?_⟩
  exact (hm (hr (hv.1 hx hy ha hb hab)) (hu.1 (hr hx) (hr hy) ha hb hab)
    (hv.2 hx hy ha hb hab)).trans (hu.2 (hr hx) (hr hy) ha hb hab)

/-- Convex nonincreasing outer function and concave inner function. -/
theorem convex_anti (hv : ConcaveOn ℝ s v) (hu : ConvexOn ℝ t u)
    (hm : AntitoneOn u t) (hr : MapsTo v s t) :
    ConvexOn ℝ s (fun x => u (v x)) := by
  refine ⟨hv.1, fun x hx y hy a b ha hb hab => ?_⟩
  exact (hm (hu.1 (hr hx) (hr hy) ha hb hab) (hr (hv.1 hx hy ha hb hab))
    (hv.2 hx hy ha hb hab)).trans (hu.2 (hr hx) (hr hy) ha hb hab)

/-- Concave nondecreasing outer function and concave inner function. -/
theorem concave_mono (hv : ConcaveOn ℝ s v) (hu : ConcaveOn ℝ t u)
    (hm : MonotoneOn u t) (hr : MapsTo v s t) :
    ConcaveOn ℝ s (fun x => u (v x)) := by
  refine ⟨hv.1, fun x hx y hy a b ha hb hab => ?_⟩
  exact (hu.2 (hr hx) (hr hy) ha hb hab).trans
    (hm (hu.1 (hr hx) (hr hy) ha hb hab) (hr (hv.1 hx hy ha hb hab))
      (hv.2 hx hy ha hb hab))

/-- Concave nonincreasing outer function and convex inner function. -/
theorem concave_anti (hv : ConvexOn ℝ s v) (hu : ConcaveOn ℝ t u)
    (hm : AntitoneOn u t) (hr : MapsTo v s t) :
    ConcaveOn ℝ s (fun x => u (v x)) := by
  refine ⟨hv.1, fun x hx y hy a b ha hb hab => ?_⟩
  exact (hu.2 (hr hx) (hr hy) ha hb hab).trans
    (hm (hr (hv.1 hx hy ha hb hab)) (hu.1 (hr hx) (hr hy) ha hb hab)
      (hv.2 hx hy ha hb hab))

theorem convex_exp (hv : ConvexOn ℝ s v) :
    ConvexOn ℝ s (fun x => Real.exp (v x)) :=
  convex_mono hv convexOn_exp (Real.exp_monotone.monotoneOn _) (fun _ _ => mem_univ _)

theorem concave_log (hv : ConcaveOn ℝ s v) (hpos : ∀ x ∈ s, 0 < v x) :
    ConcaveOn ℝ s (fun x => Real.log (v x)) :=
  concave_mono hv strictConcaveOn_log_Ioi.concaveOn
    (fun _ hx _ _ hxy => Real.log_le_log hx hxy) hpos

theorem concave_sqrt (hv : ConcaveOn ℝ s v) (hnonneg : ∀ x ∈ s, 0 ≤ v x) :
    ConcaveOn ℝ s (fun x => Real.sqrt (v x)) :=
  concave_mono hv Real.strictConcaveOn_sqrt.concaveOn
    (Real.sqrt_monotone.monotoneOn _) hnonneg

theorem convex_rpow (hv : ConvexOn ℝ s v) (hnonneg : ∀ x ∈ s, 0 ≤ v x)
    {p : ℝ} (hp : 1 ≤ p) : ConvexOn ℝ s (fun x => v x ^ p) :=
  convex_mono hv (convexOn_rpow hp)
    (fun _ hx _ _ hxy => Real.rpow_le_rpow hx hxy (by linarith)) hnonneg

theorem concave_rpow (hv : ConcaveOn ℝ s v) (hnonneg : ∀ x ∈ s, 0 ≤ v x)
    {p : ℝ} (hp : 0 ≤ p) (hp1 : p ≤ 1) : ConcaveOn ℝ s (fun x => v x ^ p) :=
  concave_mono hv (Real.concaveOn_rpow hp hp1)
    (fun _ hx _ _ hxy => Real.rpow_le_rpow hx hxy hp) hnonneg

/-- Scaling by a nonpositive coefficient reverses curvature. -/
theorem convex_scale_nonpos (hv : ConcaveOn ℝ s v) {c : ℝ} (hc : c ≤ 0) :
    ConvexOn ℝ s (fun x => c * v x) := by
  simpa only [Pi.neg_apply, smul_eq_mul, neg_mul_neg] using
    hv.neg.smul (neg_nonneg.mpr hc)

theorem concave_scale_nonpos (hv : ConvexOn ℝ s v) {c : ℝ} (hc : c ≤ 0) :
    ConcaveOn ℝ s (fun x => c * v x) := by
  simpa only [Pi.neg_apply, smul_eq_mul, neg_mul_neg] using
    hv.neg.smul (neg_nonneg.mpr hc)

/-- Negative real powers are convex on positive concave bases, by `exp (p * log v)`. -/
theorem convex_rpow_nonpos (hv : ConcaveOn ℝ s v) (hpos : ∀ x ∈ s, 0 < v x)
    {p : ℝ} (hp : p ≤ 0) : ConvexOn ℝ s (fun x => v x ^ p) := by
  apply (convex_exp (convex_scale_nonpos (concave_log hv hpos) hp)).congr
  intro x hx
  change Real.exp (p * Real.log (v x)) = v x ^ p
  rw [Real.rpow_def_of_pos (hpos x hx), mul_comm]

theorem convex_reciprocal (hv : ConcaveOn ℝ s v) (hpos : ∀ x ∈ s, 0 < v x)
    {c : ℝ} (hc : 0 ≤ c) : ConvexOn ℝ s (fun x => c / v x) := by
  simpa [Real.rpow_neg_one, div_eq_mul_inv] using
    (convex_rpow_nonpos hv hpos (show (-1 : ℝ) ≤ 0 by norm_num)).smul hc

theorem convex_nat_pow (hv : ConvexOn ℝ s v) (hnonneg : ∀ x ∈ s, 0 ≤ v x)
    (n : ℕ) : ConvexOn ℝ s (fun x => v x ^ n) :=
  convex_mono hv (convexOn_pow n)
    (fun _ hx _ _ hxy => pow_le_pow_left₀ hx hxy n) hnonneg

/-- The nonpositive concave branch for even integer powers. -/
theorem convex_even_pow_nonpos (hv : ConcaveOn ℝ s v)
    (hnonpos : ∀ x ∈ s, v x ≤ 0) {n : ℕ} (hn : Even n) :
    ConvexOn ℝ s (fun x => v x ^ n) := by
  simpa only [Pi.neg_apply, hn.neg_pow] using
    convex_nat_pow hv.neg (fun x hx => neg_nonneg.mpr (hnonpos x hx)) n

/-- Every affine map has both curvature classifications. -/
theorem affine_curvature (hs : Convex ℝ s) (v : E →ᵃ[ℝ] ℝ) :
    ConvexOn ℝ s v ∧ ConcaveOn ℝ s v := by
  constructor
  · exact ((convexOn_id (convex_univ : Convex ℝ (univ : Set ℝ))).comp_affineMap v).subset
      (fun _ _ => mem_univ _) hs
  · exact ((concaveOn_id (convex_univ : Convex ℝ (univ : Set ℝ))).comp_affineMap v).subset
      (fun _ _ => mem_univ _) hs

theorem convex_even_pow_affine (hs : Convex ℝ s) (v : E →ᵃ[ℝ] ℝ)
    {n : ℕ} (hn : Even n) : ConvexOn ℝ s (fun x => v x ^ n) :=
  (hn.convexOn_pow.comp_affineMap v).subset (fun _ _ => mem_univ _) hs

theorem convex_abs_affine (hs : Convex ℝ s) (v : E →ᵃ[ℝ] ℝ) :
    ConvexOn ℝ s (fun x => |v x|) := by
  change ConvexOn ℝ s (norm ∘ v)
  exact
    (convexOn_univ_norm.comp_affineMap v).subset (fun _ _ => mem_univ _) hs

theorem convex_const_rpow (hs : Convex ℝ s) (v : E →ᵃ[ℝ] ℝ)
    {c : ℝ} (hc : 0 < c) : ConvexOn ℝ s (fun x => c ^ v x) :=
  (convexOn_rpow_left hc).comp_affineMap v |>.subset (fun _ _ => mem_univ _) hs

theorem convex_const_rpow_of_convex (hv : ConvexOn ℝ s v) {c : ℝ} (hc : 1 ≤ c) :
    ConvexOn ℝ s (fun x => c ^ v x) := by
  have hpos : 0 < c := lt_of_lt_of_le zero_lt_one hc
  apply (convex_exp (hv.smul (Real.log_nonneg hc))).congr
  intro x _
  exact (Real.rpow_def_of_pos hpos (v x)).symm

theorem convex_const_rpow_of_concave (hv : ConcaveOn ℝ s v)
    {c : ℝ} (hc : 0 < c) (hc1 : c ≤ 1) : ConvexOn ℝ s (fun x => c ^ v x) := by
  apply (convex_exp (convex_scale_nonpos hv (Real.log_nonpos hc.le hc1))).congr
  intro x _
  exact (Real.rpow_def_of_pos hc (v x)).symm

/-- Powers zero and one are the constant and identity after separate domain checking. -/
theorem rpow_zero_one (x : ℝ) : x ^ (0 : ℝ) = 1 ∧ x ^ (1 : ℝ) = x := by simp

theorem convex_add {w : E → ℝ} (hv : ConvexOn ℝ s v) (hw : ConvexOn ℝ s w) :
    ConvexOn ℝ s (fun x => v x + w x) := hv.add hw

theorem concave_add {w : E → ℝ} (hv : ConcaveOn ℝ s v) (hw : ConcaveOn ℝ s w) :
    ConcaveOn ℝ s (fun x => v x + w x) := hv.add hw

theorem convex_scale_nonneg (hv : ConvexOn ℝ s v) {c : ℝ} (hc : 0 ≤ c) :
    ConvexOn ℝ s (fun x => c * v x) := hv.smul hc

theorem concave_scale_nonneg (hv : ConcaveOn ℝ s v) {c : ℝ} (hc : 0 ≤ c) :
    ConcaveOn ℝ s (fun x => c * v x) := hv.smul hc

end Composition
end CertifiedMinlp
