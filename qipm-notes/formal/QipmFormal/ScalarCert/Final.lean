import QipmFormal.ScalarCert.Comparison
import QipmFormal.ScalarCert.KBound
import QipmFormal.ScalarCert.LogBounds
import QipmFormal.ScalarCert.Certificate
import QipmFormal.ScalarCert.Witness

/-!
# The upper certificate `c⋆ < 69/50`

Assembles the appendix's upper certificate.  With `a = 69/50`:

* `Phi_pos` at `(v, W v)` gives `log (E v) > k log t + (t-1)(E v - k)` for the
  dilation ratio `t = ratio v`, because `P (W v) = E v * P v`;
* if `t ≥ a` this forces `h_k (E v) < 0`, where
  `h_k E = k log a + (a-1)(E-k) - log E`;
* `h₁ > 0` on `(0,2]` and `h_{107/200} > 0` everywhere, by the tangent-line
  bound `log x ≤ x - 1` together with the rational logarithm bounds of
  `LogBounds.lean`.

The case split is the appendix's: `k = 1` uses `K < 1`, valid everywhere;
`k = 107/200` uses `K < 107/200`, valid on `E > 2`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- `Phi_pos` on an interval `(a,1)` rather than `(0,1)`. -/
theorem Phi_pos' {k a v0 v : ℝ} (ha : 0 ≤ a) (hav : a < v0) (h : v0 < v) (hv1 : v < 1)
    (hg : StrictMonoOn (g k) (Ioo a 1)) : 0 < Phi k v0 v := by
  have hv00 : 0 < v0 := lt_of_le_of_lt ha hav
  have hv01 : v0 < 1 := h.trans hv1
  have hmono : StrictMonoOn (Phi k v0) (Ico v0 1) := by
    have hmem : ∀ x ∈ Ico v0 1, 0 < x ∧ x < 1 := fun x hx =>
      ⟨lt_of_lt_of_le hv00 hx.1, hx.2⟩
    refine strictMonoOn_of_deriv_pos (convex_Ico v0 1) ?_ ?_
    · intro x hx
      obtain ⟨hx0, hx1⟩ := hmem x hx
      exact (Phi_hasDerivAt (k := k) hv00 hv01 hx0 hx1).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ico] at hx
      obtain ⟨hx0, hx1⟩ := hmem x ⟨hx.1.le, hx.2⟩
      have habs : |x| < 1 := by rwa [abs_of_pos hx0]
      rw [(Phi_hasDerivAt (k := k) hv00 hv01 hx0 hx1).deriv]
      have hgx : g k v0 < g k x := hg ⟨hav, hv01⟩ ⟨hav.trans hx.1, hx1⟩ hx.1
      have hY := Y_deriv_pos habs
      have hpos : 0 < g k x - g k v0 := by linarith
      positivity
  have := hmono (left_mem_Ico.mpr hv01) ⟨h.le, hv1⟩ h
  rwa [Phi_self hv00 hv01] at this

/-- `v < W v`: the target point of the dilation lies strictly to the right. -/
theorem lt_W {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : v < W v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have hA : 0 < A v := A_pos habs
  have hPv : P v < Y v * A v := by
    rw [P]
    exact mul_lt_mul_of_pos_right (lt_Y hv0 hv1) hA
  have hPW : P (W v) = Y v * A v := P_W hv0 hv1
  have hlt : P v < P (W v) := by rw [hPW]; exact hPv
  rcases lt_trichotomy v (W v) with h | h | h
  · exact h
  · rw [← h] at hlt; exact absurd hlt (lt_irrefl _)
  · exact absurd (P_strictMonoOn (W_mem hv0 hv1) ⟨hv0.le, hv1⟩ h) (not_lt.mpr hlt.le)

/-- `P (W v) = E v * P v`. -/
theorem P_W_eq {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : P (W v) = E v * P v := by
  rw [P_W hv0 hv1, E, P]
  field_simp

/-- `log P (W v) - log P v = log (E v)`. -/
theorem logP_W {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    Real.log (P (W v)) - Real.log (P v) = Real.log (E v) := by
  have hPv : 0 < P v := P_pos hv0 hv1
  have hE : 0 < E v := by
    rw [E]; exact div_pos (Y_pos hv0 hv1) hv0
  rw [P_W_eq hv0 hv1, Real.log_mul hE.ne' hPv.ne']
  ring

/-- The key inequality: `log (E v) > k log t + (t-1)(E v - k)` for the
dilation ratio `t = ratio v`.  This is `Phi_pos` at `(v, W v)`. -/
theorem key_ineq {k v a : ℝ} (hv0 : 0 < v) (hv1 : v < 1) (ha : 0 ≤ a) (hav : a < v)
    (hg : StrictMonoOn (g k) (Ioo a 1)) :
    k * Real.log (ratio v) + (ratio v - 1) * (E v - k) < Real.log (E v) := by
  have hW := lt_W hv0 hv1
  have hWmem := W_mem hv0 hv1
  have hW1 : W v < 1 := hWmem.2
  have hW0 : 0 < W v := hv0.trans hW
  have hpos := Phi_pos' (k := k) ha hav hW hW1 hg
  have hYv : 0 < Y v := Y_pos hv0 hv1
  have hYW : 0 < Y (W v) := Y_pos hW0 hW1
  have hlogY : Real.log (Y (W v)) - Real.log (Y v) = Real.log (ratio v) := by
    rw [ratio, Real.log_div hYW.ne' hYv.ne']
  have hratio : Y (W v) / Y v = ratio v := rfl
  rw [Phi, logP_W hv0 hv1, hratio] at hpos
  rw [hlogY] at hpos
  linarith

/-! ### The functions `h₁` and `h_k` of the appendix -/

/-- `h_{a,k} E = k log a + (a-1)(E-k) - log E`.  The appendix uses `a = 69/50`. -/
noncomputable def hgen (a k E : ℝ) : ℝ :=
  k * Real.log a + (a - 1) * (E - k) - Real.log E

/-- Generic upper bound: if `h_{a,1} > 0` on `(0,2]` and `h_{a,107/200} > 0`
everywhere, then every dilation ratio is below `a`.  This is the appendix's
case split: `k = 1` uses `K < 1`, valid everywhere; `k = 107/200` uses
`K < 107/200`, valid on `E > 2`. -/
theorem ratio_lt_of_hgen {a : ℝ} (ha : 1 < a)
    (h1 : ∀ E : ℝ, 0 < E → E ≤ 2 → 0 < hgen a 1 E)
    (hk : ∀ E : ℝ, 0 < E → 0 < hgen a (107 / 200) E)
    {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : ratio v < a := by
  by_contra hcon
  rw [not_lt] at hcon
  have hE1 : 1 < E v := one_lt_E hv0 hv1
  have hE0 : (0:ℝ) < E v := lt_trans one_pos hE1
  have hrpos : (0:ℝ) < ratio v := lt_of_lt_of_le (by linarith) hcon
  have hlog : Real.log a ≤ Real.log (ratio v) :=
    Real.log_le_log (by linarith) hcon
  rcases le_or_gt (E v) 2 with hE | hE
  · have hkey := key_ineq (k := 1) (a := 0) hv0 hv1 le_rfl hv0 g_one_strictMonoOn
    have hEk : (0:ℝ) < E v - 1 := by linarith
    have hmul : (a - 1) * (E v - 1) ≤ (ratio v - 1) * (E v - 1) := by nlinarith
    have hpos := h1 (E v) hE0 hE
    rw [hgen] at hpos
    linarith
  · have hv2 := lt_of_two_lt_E hv0 hv1 hE
    have hgK : StrictMonoOn (g (107 / 200)) (Ioo v2 1) := by
      refine g_strictMonoOn_of_K_lt v2_pos.le le_rfl ?_
      intro w hw1 hw2
      exact lt_trans (K_strictAntiOn (left_mem_Ico.mpr v2_lt_one) ⟨hw1.le, hw2⟩ hw1) K_v2_lt
    have hkey := key_ineq (k := 107 / 200) (a := v2) hv0 hv1 v2_pos.le hv2 hgK
    have hEk : (0:ℝ) < E v - 107 / 200 := by linarith
    have hmul : (a - 1) * (E v - 107 / 200) ≤ (ratio v - 1) * (E v - 107 / 200) := by nlinarith
    have hpos := hk (E v) hE0
    rw [hgen] at hpos
    linarith

/-- Tangent-line bound `log E ≤ log c + E/c - 1` for `c > 0`. -/
lemma log_le_tangent {E c : ℝ} (hE : 0 < E) (hc : 0 < c) :
    Real.log E ≤ Real.log c + E / c - 1 := by
  have h := Real.log_le_sub_one_of_pos (show (0:ℝ) < E / c by positivity)
  rw [Real.log_div hE.ne' hc.ne'] at h
  linarith

/-! ### Instantiation at `a = 3449/2500`, which is `< 69/50` -/

lemma hgen_one_pos_strict {E : ℝ} (hE0 : 0 < E) (hE2 : E ≤ 2) :
    0 < hgen (3449 / 2500) 1 E := by
  have htan := log_le_tangent hE0 (show (0:ℝ) < 2 by norm_num)
  have h1 := log_3449_2500_ge
  have h2 := log_two_le
  rw [hgen]
  nlinarith [htan, h1, h2, hE2]

lemma hgen_k_pos_strict {E : ℝ} (hE0 : 0 < E) :
    0 < hgen (3449 / 2500) (107 / 200) E := by
  have htan := log_le_tangent hE0 (show (0:ℝ) < 2500 / 949 by norm_num)
  have h1 := log_3449_2500_ge
  have h2 := log_2500_949_le
  rw [hgen]
  nlinarith [htan, h1, h2]

/-! ### The upper certificate -/

/-- **Upper certificate.**  Every dilation ratio is below `3449/2500 < 69/50`. -/
theorem ratio_lt_strict {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : ratio v < 3449 / 2500 :=
  ratio_lt_of_hgen (by norm_num)
    (fun _ h h2 => hgen_one_pos_strict h h2) (fun _ h => hgen_k_pos_strict h) hv0 hv1

/-- Every dilation ratio is below `69/50`. -/
theorem ratio_lt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : ratio v < 69 / 50 :=
  lt_trans (ratio_lt_strict hv0 hv1) (by norm_num)

/-- The dilation ratios are bounded above. -/
theorem bddAbove_ratio : BddAbove (ratio '' Ioo 0 1) := by
  refine ⟨3449 / 2500, ?_⟩
  rintro y ⟨v, hv, rfl⟩
  exact (ratio_lt_strict hv.1 hv.2).le

/-- `c⋆ < 69/50`, the appendix's strict upper bound. -/
theorem cstar_lt : cstar < 69 / 50 := by
  have hle : cstar ≤ 3449 / 2500 := by
    rw [cstar]
    refine csSup_le ⟨ratio (1/2), ⟨1/2, by norm_num, rfl⟩⟩ ?_
    rintro y ⟨v, hv, rfl⟩
    exact (ratio_lt_strict hv.1 hv.2).le
  linarith

/-- **The two-sided certificate of `eq:cstar`, unconditionally.** -/
theorem cstar_bounds : (68743 : ℝ) / 50000 < cstar ∧ cstar < 69 / 50 :=
  ⟨a0_lt_cstar bddAbove_ratio, cstar_lt⟩

end QipmFormal.ScalarCert
