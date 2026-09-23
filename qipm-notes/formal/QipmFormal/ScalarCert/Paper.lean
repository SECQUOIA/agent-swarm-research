import QipmFormal.ScalarCert.Correspondence
import QipmFormal.ScalarCert.Surjectivity
import QipmFormal.ScalarCert.Attainment

/-!
# The scalar certificate in the manuscript's coordinates

On positive arguments, `rhoInv` is the inverse of the manuscript's arclength
`rho`, `p = deriv bb ∘ rhoInv`, and `pInv` is the inverse of `p`. The final
theorems identify the manuscript's supremum with the certified `cstar`.
Values of the inverse outside the positive domain play no role.
-/

namespace QipmFormal.ScalarCert.Paper

open Real Set

/-- The inverse of `Y` on positive arguments, extended by zero elsewhere. -/
noncomputable def Yinv (y : ℝ) : ℝ :=
  if hy : 0 < y then (Y_surjOn hy).choose else 0

theorem Yinv_mem {y : ℝ} (hy : 0 < y) : Yinv y ∈ Ioo (0 : ℝ) 1 := by
  simp only [Yinv, dif_pos hy]
  exact (Y_surjOn hy).choose_spec.1

theorem Y_Yinv {y : ℝ} (hy : 0 < y) : Y (Yinv y) = y := by
  simp only [Yinv, dif_pos hy]
  exact (Y_surjOn hy).choose_spec.2

theorem Yinv_Y {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : Yinv (Y v) = v := by
  have hm := Yinv_mem (Y_pos hv0 hv1)
  exact Y_strictMonoOn.injOn ⟨hm.1.le, hm.2⟩ ⟨hv0.le, hv1⟩
    (Y_Yinv (Y_pos hv0 hv1))

theorem xOf_mem {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    xOf v ∈ Ioo (0 : ℝ) 1 := by
  have hv : |v| < 1 := by rwa [abs_of_pos hv0]
  have hd := two_sub_sq_pos' hv
  have hx0 : 0 < xOf v := div_pos hv0 (Real.sqrt_pos.mpr hd)
  have hx2 : (xOf v) ^ 2 < 1 := by
    rw [xOf_sq hv, div_lt_iff₀ hd]
    nlinarith
  exact ⟨hx0, by nlinarith⟩

theorem vOf_xOf {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : vOf (xOf v) = v := by
  have hx := xOf_mem hv0 hv1
  have hxabs : |xOf v| < 1 := by simpa only [abs_of_pos hx.1] using hx.2
  have hvabs := vOf_lt_one hxabs
  have hpos : 0 < vOf (xOf v) := by
    unfold vOf
    exact div_pos (mul_pos (by positivity) hx.1) (sqrt_one_add_sq_pos' _)
  exact xOf_strictMonoOn.injOn
    ⟨hpos.le, (abs_lt.mp hvabs).2⟩ ⟨hv0.le, hv1⟩ (xOf_vOf hxabs)

/-- The inverse of the manuscript's arclength on `(0,∞)`. -/
noncomputable def rhoInv (y : ℝ) : ℝ := xOf (Yinv y)

theorem rhoInv_mem {y : ℝ} (hy : 0 < y) : rhoInv y ∈ Ioo (0 : ℝ) 1 :=
  xOf_mem (Yinv_mem hy).1 (Yinv_mem hy).2

theorem rho_rhoInv {y : ℝ} (hy : 0 < y) : rho (rhoInv y) = y := by
  have hx := rhoInv_mem hy
  have hxabs : |rhoInv y| < 1 := by simpa only [abs_of_pos hx.1] using hx.2
  rw [← Y_vOf_eq_rho hxabs, rhoInv,
    vOf_xOf (Yinv_mem hy).1 (Yinv_mem hy).2, Y_Yinv hy]

theorem rhoInv_rho {x : ℝ} (hx0 : 0 < x) (hx1 : x < 1) : rhoInv (rho x) = x := by
  have hxabs : |x| < 1 := by rwa [abs_of_pos hx0]
  have hv0 : 0 < vOf x := by
    unfold vOf
    exact div_pos (mul_pos (by positivity) hx0) (sqrt_one_add_sq_pos' _)
  have hv1 : vOf x < 1 := (abs_lt.mp (vOf_lt_one hxabs)).2
  rw [rhoInv, ← Y_vOf_eq_rho hxabs, Yinv_Y hv0 hv1, xOf_vOf hxabs]

/-- Exactly the manuscript's definition `p = b' ∘ rho⁻¹`. -/
noncomputable def p (y : ℝ) : ℝ := deriv bb (rhoInv y)

theorem p_Y {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : p (Y v) = P v := by
  have hx := xOf_mem hv0 hv1
  have hxabs : |xOf v| < 1 := by simpa only [abs_of_pos hx.1] using hx.2
  rw [p, rhoInv, Yinv_Y hv0 hv1, ← P_vOf_eq_bb_deriv hxabs, vOf_xOf hv0 hv1]

theorem p_eq_P_Yinv {y : ℝ} (hy : 0 < y) : p y = P (Yinv y) := by
  have h := p_Y (Yinv_mem hy).1 (Yinv_mem hy).2
  rwa [Y_Yinv hy] at h

theorem Yinv_monotoneOn : MonotoneOn Yinv (Ioi (0 : ℝ)) := by
  intro a ha b hb hab
  have hma := Yinv_mem ha
  have hmb := Yinv_mem hb
  apply (Y_strictMonoOn.le_iff_le ⟨hma.1.le, hma.2⟩ ⟨hmb.1.le, hmb.2⟩).mp
  simpa only [Y_Yinv ha, Y_Yinv hb] using hab

theorem Yinv_continuousAt {y : ℝ} (hy : 0 < y) : ContinuousAt Yinv y := by
  apply continuousAt_of_monotoneOn_of_image_mem_nhds Yinv_monotoneOn (Ioi_mem_nhds hy)
  apply Filter.mem_of_superset (Ioo_mem_nhds (Yinv_mem hy).1 (Yinv_mem hy).2)
  intro v hv
  exact ⟨Y v, Y_pos hv.1 hv.2, Yinv_Y hv.1 hv.2⟩

theorem Yinv_hasDerivAt {y : ℝ} (hy : 0 < y) :
    HasDerivAt Yinv
      (2 / ((1 - (Yinv y) ^ 2) * (2 - (Yinv y) ^ 2)))⁻¹ y := by
  have hm := Yinv_mem hy
  have hv : |Yinv y| < 1 := by simpa only [abs_of_pos hm.1] using hm.2
  apply HasDerivAt.of_local_left_inverse (Yinv_continuousAt hy) (Y_deriv hv)
    (Y_deriv_pos hv).ne'
  filter_upwards [Ioi_mem_nhds hy] with z hz
  exact Y_Yinv hz

/-- The manuscript's derivative identity, proved through the inverse of `Y`. -/
theorem p_hasDerivAt {y : ℝ} (hy : 0 < y) : HasDerivAt p (A (Yinv y)) y := by
  have hm := Yinv_mem hy
  have hv : |Yinv y| < 1 := by simpa only [abs_of_pos hm.1] using hm.2
  have h1 := one_sub_sq_pos hv
  have h2 := two_sub_sq_pos hv
  have hs : 0 < √(2 - (Yinv y) ^ 2) := Real.sqrt_pos.mpr h2
  have h := (P_hasDerivAt hv).comp y (Yinv_hasDerivAt hy)
  have heq : (2 / ((1 - (Yinv y) ^ 2) ^ 2 * √(2 - (Yinv y) ^ 2))) *
      (2 / ((1 - (Yinv y) ^ 2) * (2 - (Yinv y) ^ 2)))⁻¹ = A (Yinv y) := by
    calc
      _ = (2 - (Yinv y) ^ 2) /
          ((1 - (Yinv y) ^ 2) * √(2 - (Yinv y) ^ 2)) := by
        field_simp [h1.ne', h2.ne', hs.ne']
      _ = A (Yinv y) := by
        unfold A
        apply (div_eq_div_iff (mul_pos h1 hs).ne' h1.ne').2
        calc
          _ = (√(2 - (Yinv y) ^ 2)) ^ 2 * (1 - (Yinv y) ^ 2) := by
            rw [Real.sq_sqrt h2.le]
          _ = _ := by ring
  apply (h.congr_deriv heq).congr_of_eventuallyEq
  filter_upwards [Ioi_mem_nhds hy] with z hz
  exact p_eq_P_Yinv hz

theorem deriv_p_Y {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : deriv p (Y v) = A v := by
  rw [(p_hasDerivAt (Y_pos hv0 hv1)).deriv, Yinv_Y hv0 hv1]

/-- The inverse of `p` on positive arguments. -/
noncomputable def pInv (z : ℝ) : ℝ := Y (Pinv z)

theorem p_pInv {z : ℝ} (hz : 0 < z) : p (pInv z) = z := by
  rw [pInv, p_Y (Pinv_pos hz) (Pinv_lt_one z), P_Pinv hz]

theorem pInv_p {y : ℝ} (hy : 0 < y) : pInv (p y) = y := by
  have hm := Yinv_mem hy
  have hp := P_pos hm.1 hm.2
  have hpinv : Pinv (P (Yinv y)) = Yinv y :=
    P_strictMonoOn.injOn (Pinv_mem hp) ⟨hm.1.le, hm.2⟩ (P_Pinv hp)
  rw [p_eq_P_Yinv hy, pInv, hpinv, Y_Yinv hy]

/-- The manuscript's dilation ratio at `y > 0`. -/
noncomputable def ratio (y : ℝ) : ℝ := pInv (y * deriv p y) / y

theorem ratio_Y {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    ratio (Y v) = ScalarCert.ratio v := by
  rw [ratio, deriv_p_Y hv0 hv1]
  rfl

theorem ratio_image : ratio '' Ioi (0 : ℝ) = ScalarCert.ratio '' Ioo 0 1 := by
  ext z
  constructor
  · rintro ⟨y, hy, rfl⟩
    obtain ⟨v, hv, rfl⟩ := Y_surjOn hy
    exact ⟨v, hv, (ratio_Y hv.1 hv.2).symm⟩
  · rintro ⟨v, hv, rfl⟩
    exact ⟨Y v, Y_pos hv.1 hv.2, ratio_Y hv.1 hv.2⟩

/-- The supremum in the manuscript's original `y` coordinate. -/
noncomputable def cstar : ℝ := sSup (ratio '' Ioi (0 : ℝ))

theorem cstar_eq : cstar = ScalarCert.cstar := by
  unfold cstar ScalarCert.cstar
  rw [ratio_image]

/-- The rational certificate for the manuscript's original definition. -/
theorem cstar_bounds : (68743 : ℝ) / 50000 < cstar ∧ cstar < 69 / 50 := by
  rw [cstar_eq]
  exact ScalarCert.cstar_bounds

/-- The manuscript's supremum is attained at a positive argument. -/
theorem cstar_attained : ∃ y ∈ Ioi (0 : ℝ), ratio y = cstar := by
  obtain ⟨v, hv, heq⟩ := ScalarCert.cstar_attained
  refine ⟨Y v, Y_pos hv.1 hv.2, ?_⟩
  rw [ratio_Y hv.1 hv.2, heq, cstar_eq]

/-- The variational definition is a maximum, as stated in the manuscript. -/
theorem cstar_isGreatest : IsGreatest (ratio '' Ioi (0 : ℝ)) cstar := by
  obtain ⟨y, hy, heq⟩ := cstar_attained
  refine ⟨⟨y, hy, heq⟩, ?_⟩
  intro z hz
  rw [cstar_eq]
  apply le_csSup ScalarCert.bddAbove_ratio
  rwa [← ratio_image]

end QipmFormal.ScalarCert.Paper
