import Formal.NetworkSimplex.ThresholdObstruction
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-! Quantitative inverse perturbations for balanced incidence sections. -/
namespace NetworkSimplex.Chain.Balanced
open scoped BigOperators
noncomputable section

variable {N : ℕ}

def incidenceMatrix (S : Fin N → Finset (Fin N)) : Matrix (Fin N) (Fin N) ℝ :=
  fun i j => if j ∈ S i then 1 else 0

/-- The infinity norm induced by the sup norm on coordinate vectors. -/
def inverseOperator (K : Matrix (Fin N) (Fin N) ℝ) : (Fin N → ℝ) →L[ℝ] (Fin N → ℝ) :=
  (Matrix.toLin' K⁻¹).toContinuousLinearMap

def inverseSize (K : Matrix (Fin N) (Fin N) ℝ) : ℝ := ‖inverseOperator K‖

def epsilon (a R C : ℝ) : ℝ := a / (16 * (1 + R) * (1 + C))

def delta (r s : Fin N) (u v : ℝ) (i : Fin N) : ℝ :=
  (if i = r then u else 0) + (if i = s then v else 0)

def tau (s : Fin N) (R u v : ℝ) (i : Fin N) : ℝ :=
  if i = s then R * u + v else 0

def perturbation (K : Matrix (Fin N) (Fin N) ℝ) (r s : Fin N) (R u v : ℝ) :=
  inverseOperator K (fun i => -delta r s u v i + tau s R u v i)

theorem inverseOperator_apply (K : Matrix (Fin N) (Fin N) ℝ) (z : Fin N → ℝ) :
    inverseOperator K z = K⁻¹.mulVec z := rfl

theorem perturbation_equation (K : Matrix (Fin N) (Fin N) ℝ) (hK : IsUnit K.det)
    (r s : Fin N) (R u v : ℝ) :
    K.mulVec (perturbation K r s R u v) = fun i => -delta r s u v i + tau s R u v i := by
  simp [perturbation, inverseOperator_apply, Matrix.mulVec_mulVec, K.mul_nonsing_inv hK]

theorem epsilon_pos {a R C : ℝ} (ha : 0 < a) (hR : 0 < R) (hC : 0 ≤ C) :
    0 < epsilon a R C := by unfold epsilon; positivity

/-- The displayed neighborhood controls both free perturbations after multiplication by 1+R. -/
theorem epsilon_control {a R C x : ℝ} (_ha : 0 < a) (hR : 0 < R) (hC : 0 ≤ C)
    (hx : |x| < epsilon a R C) : (1 + C) * (1 + R) * |x| < a / 16 := by
  have hd : 0 < 16 * (1 + R) * (1 + C) := by positivity
  have hh := (lt_div_iff₀ hd).mp hx
  nlinarith

theorem perturbation_rhs_bound {r s : Fin N} (hrs : r ≠ s) {R u v : ℝ} (hR : 0 < R) :
    ‖fun i => -delta r s u v i + tau s R u v i‖ ≤ (1 + R) * |u| := by
  apply (pi_norm_le_iff_of_nonneg (by positivity)).mpr
  intro i
  by_cases hir : i = r
  · subst i
    simp [delta, tau, hrs, Real.norm_eq_abs]
    nlinarith [abs_nonneg u]
  · by_cases his : i = s
    · subst i
      simp [delta, tau, hir, Real.norm_eq_abs, abs_of_pos hR]
      nlinarith [abs_nonneg u]
    · simpa [delta, tau, hir, his] using
        (show 0 ≤ (1 + R) * |u| by positivity)

theorem perturbation_bound {K : Matrix (Fin N) (Fin N) ℝ} {r s : Fin N}
    (hrs : r ≠ s) {a R u v : ℝ} (ha : 0 < a) (hR : 0 < R)
    (hu : |u| < epsilon a R (inverseSize K)) (j : Fin N) :
    |perturbation K r s R u v j| < a / 16 := by
  have hC : 0 ≤ inverseSize K := norm_nonneg _
  have hcontrol := epsilon_control ha hR hC hu
  have hnorm := (inverseOperator K).le_opNorm
    (fun i => -delta r s u v i + tau s R u v i)
  have hz := perturbation_rhs_bound (u := u) (v := v) hrs hR
  have hcoord := norm_le_pi_norm (perturbation K r s R u v) j
  change ‖perturbation K r s R u v‖ ≤ inverseSize K * _ at hnorm
  rw [Real.norm_eq_abs] at hcoord
  have hm := mul_le_mul_of_nonneg_left hz hC
  have hu0 := abs_nonneg u
  nlinarith

theorem tau_bound {a R C u v : ℝ} (ha : 0 < a) (hR : 0 < R) (hC : 0 ≤ C)
    (hu : |u| < epsilon a R C) (hv : |v| < epsilon a R C)
    (hh : 0 ≤ R * u + v) : 0 ≤ R * u + v ∧ R * u + v < a / 16 := by
  refine ⟨hh, ?_⟩
  have hd : 0 < 16 * (1 + R) * (1 + C) := by positivity
  have hu' := (lt_div_iff₀ hd).mp hu
  have hv' := (lt_div_iff₀ hd).mp hv
  have he := epsilon_pos ha hR hC
  have hule : u ≤ |u| := le_abs_self u
  have hvle : v ≤ |v| := le_abs_self v
  have hsum : R * u + v < (1 + R) * epsilon a R C := by nlinarith
  have heq : (1 + R) * epsilon a R C ≤ a / 16 := by
    unfold epsilon
    apply (le_div_iff₀ (by norm_num : (0 : ℝ) < 16)).mpr
    rw [← mul_div_assoc, div_mul_eq_mul_div]
    apply (div_le_iff₀ hd).mpr
    nlinarith [mul_nonneg (le_of_lt ha) hC]
  exact hsum.trans_le heq

/-- Positive balancing makes the recovered perturbation sum to zero. -/
theorem perturbation_sum_zero (K : Matrix (Fin N) (Fin N) ℝ) (hK : IsUnit K.det)
    (alpha : Fin N → ℝ) {beta : ℝ} (hbeta : 0 < beta)
    (hbal : ∀ j, ∑ i, alpha i * K i j = beta)
    {r s : Fin N} (_hrs : r ≠ s) (hs : alpha s ≠ 0) (u v : ℝ) :
    ∑ j, perturbation K r s (alpha r / alpha s) u v j = 0 := by
  have he := perturbation_equation K hK r s (alpha r / alpha s) u v
  have hh := congrArg (fun z : Fin N → ℝ => ∑ i, alpha i * z i) he
  have hleft : (∑ i, alpha i * K.mulVec (perturbation K r s (alpha r / alpha s) u v) i) =
      beta * ∑ j, perturbation K r s (alpha r / alpha s) u v j := by
    simp only [Matrix.mulVec, dotProduct, Finset.mul_sum]
    rw [Finset.sum_comm]
    simp only [← mul_assoc, ← Finset.sum_mul, hbal, ← Finset.mul_sum]
  rw [hleft] at hh
  have hright : (∑ i, alpha i * (-delta r s u v i + tau s (alpha r / alpha s) u v i)) = 0 := by
    simp [delta, tau, mul_add, mul_ite, mul_zero, Finset.sum_add_distrib,
      Finset.sum_neg_distrib, mul_neg]
    field_simp
    ring
  rw [hright] at hh
  exact (mul_eq_zero.mp hh).resolve_left (ne_of_gt hbeta)

end
end NetworkSimplex.Chain.Balanced
