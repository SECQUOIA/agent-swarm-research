import Formal.QuadraticPrecision.LowerEuclidean
import Formal.QuadraticPrecision.Isodiametric
import Formal.QuadraticPrecision.LowerNegativeSlice

open MeasureTheory
open scoped BigOperators Matrix
namespace QuadraticPrecision
noncomputable section

/-- The sharp Euclidean contact-volume bound, expressed in the original
coordinate Lebesgue measure. -/
theorem negative_contact_volume_sharp {d : ℕ} (hd : 0 < d)
    (M : Matrix (Fin d) (Fin d) ℝ) {μ ε : ℝ} (hμ : 0 < μ) (_hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    {S : Set (Input d)} (hS : IsCompact S)
    (hcontact : ∀ x ∈ S, ∀ y ∈ S, -contactQuadratic M (x-y) ≤ 4*ε) :
    volume S ≤ ENNReal.ofReal (unitBallVolume d * (Real.sqrt (8*ε/μ)/2)^d) := by
  have hi := Isodiametric.volume_le_unitBall_mul_half_diameter_pow hd
    (euclidean_image_compact hS) (Real.sqrt_nonneg (8*ε/μ))
    (by
      rintro _ ⟨x,hx,rfl⟩ _ ⟨y,hy,rfl⟩
      exact negative_contact_euclidean_distance M hμ hcurv (hcontact x hx y hy))
  rw [euclidean_image_volume hS] at hi
  convert hi using 1
  rw [ENNReal.ofReal_mul (by unfold unitBallVolume; positivity),
    ENNReal.ofReal_pow (by positivity)]
  congr 1
  exact ENNReal.ofReal_toReal (isCompact_closedBall
    (0 : EuclideanSpace ℝ (Fin d)) 1).measure_lt_top.ne

/-- The same-parity cover has the sharp unit-ball volume constant. -/
theorem epigraph_negative_volume_sharp {d p : ℕ} (hd : 0 < d)
    {D : Set (Input d)} (hD : IsCompact D)
    (M : Matrix (Fin d) (Fin d) ℝ) (a : Input d) (b ε μ : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) :
    volume D ≤ ENNReal.ofReal ((2:ℝ)^p * unitBallVolume d *
      (Real.sqrt (8*ε/μ)/2)^d) := by
  obtain ⟨S,hc,_,hcover,he⟩ := epigraph_quadratic_parity_cover hD M a b ε h
  calc
    volume D ≤ volume (⋃ α, S α) := measure_mono hcover
    _ ≤ ∑ α, volume (S α) := measure_iUnion_fintype_le volume S
    _ ≤ ∑ _α : ParityCode p, ENNReal.ofReal
        (unitBallVolume d * (Real.sqrt (8*ε/μ)/2)^d) := by
      apply Finset.sum_le_sum
      intro α _
      exact negative_contact_volume_sharp hd M hμ hε hcurv (hc α) (he α)
    _ = _ := by
      rw [Finset.sum_const, Finset.card_univ, card_parityCode, nsmul_eq_mul]
      rw [← ENNReal.ofReal_natCast, ← ENNReal.ofReal_mul (by positivity)]
      simp [mul_assoc]

/-- Positive-volume strongly concave graphs have no exact finite-integer
epigraph lift, even when the convex carrier is not closed. -/
theorem epigraph_negative_error_pos {d p : ℕ} (hd : 0 < d)
    {D : Set (Input d)} (hD : IsCompact D) (hvol : volume D ≠ 0)
    (M : Matrix (Fin d) (Fin d) ℝ) (a : Input d) (b ε μ : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) : 0 < ε := by
  have hv := epigraph_negative_volume_sharp hd hD M a b ε μ hμ hε hcurv h
  by_contra hn
  have hz : ε = 0 := by linarith
  simp only [hz, mul_zero, zero_div, Real.sqrt_zero, zero_pow (Nat.ne_of_gt hd),
    ENNReal.ofReal_zero] at hv
  exact hvol (le_antisymm hv zero_le)

/-- The source's explicit strong-curvature bound with coefficient μ/2 and
Euclidean unit-ball volume. The premise is an actual epigraph lift. -/
theorem epigraph_strong_curvature_error_lower {d p : ℕ} (hd : 0 < d)
    {D : Set (Input d)} (hD : IsCompact D) (hvol : volume D ≠ 0)
    (M : Matrix (Fin d) (Fin d) ℝ) (a : Input d) (b ε μ : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hcurv : ∀ v : Input d, μ * ∑ i, (v i)^2 ≤ -(v ⬝ᵥ M.mulVec v))
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) :
    (μ/2) * ((volume D).toReal/unitBallVolume d)^((2:ℝ)/d) *
      (2:ℝ)^(-2*(p:ℝ)/(d:ℝ)) ≤ ε := by
  have he := epigraph_negative_error_pos hd hD hvol M a b ε μ hμ hε hcurv h
  have hv := epigraph_negative_volume_sharp hd hD M a b ε μ hμ hε hcurv h
  have hV : 0 < (volume D).toReal := ENNReal.toReal_pos hvol hD.measure_lt_top.ne
  have ho := unitBallVolume_pos d
  have hv' := ENNReal.toReal_le_of_le_ofReal (by positivity) hv
  exact error_lower_of_log_lower hd (curvatureErrorConstant_pos hμ hV) he
    (curvature_volume_log_lower hd hμ hV he hv')

/-- An explicit sharp bound on the negative slice constructed from the actual
Hessian and original box. Its parameter volume is `(2ρ)^k`. -/
theorem epigraph_negative_inertia_sharp_lower {n : ℕ}
    (H : Matrix (Fin n) (Fin n) ℝ) (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i)
    (hk : 0 < negativeInertia hH) :
    ∃ ρ μ : ℝ, 0 < ρ ∧ 0 < μ ∧ ∀ ε : ℝ, 0 ≤ ε → ∀ p : ℕ,
      HasEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε p →
      (μ/2) * ((2*ρ)^(negativeInertia hH)/unitBallVolume (negativeInertia hH))^
        ((2:ℝ)/negativeInertia hH) *
        (2:ℝ)^(-2*(p:ℝ)/(negativeInertia hH:ℝ)) ≤ ε := by
  obtain ⟨ρ, μ, A, M, a', b', hρ, hμ, _, hbox, hpoly, hcurv⟩ :=
    exists_negative_quadratic_slice H hH a l u b hlu
  let D : Set (Input (negativeInertia hH)) := Set.Icc (fun _ => -ρ) (fun _ => ρ)
  have hvolume : (volume D).toReal = (2*ρ)^(negativeInertia hH) := by
    rw [Real.volume_Icc_pi_toReal (by intro i; linarith :
      (fun _ : Fin (negativeInertia hH) => -ρ) ≤ fun _ => ρ)]
    simp only [sub_neg_eq_add, ← two_mul, Finset.prod_const, Finset.card_univ,
      Fintype.card_fin]
  have hvol : volume D ≠ 0 := by
    intro hz
    have hp : 0 < (volume D).toReal := by rw [hvolume]; positivity
    simp [hz] at hp
  refine ⟨ρ, μ, hρ, hμ, ?_⟩
  intro ε hε p h
  have hpull := h.pullback A D (convex_Icc _ _) hbox
  rw [hpoly] at hpull
  simpa only [hvolume] using epigraph_strong_curvature_error_lower (D := D) hk isCompact_Icc
    hvol M a' b' ε μ hμ hε hcurv hpull

end
end QuadraticPrecision
