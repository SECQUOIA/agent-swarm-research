import QipmFormal.ScalarCert.Upper

/-!
# The comparison inequality `E(ty) > k + t(E(y) - k)`

This file formalises the differential-inequality step of
`notes/central-path-cost/sections/appendix-scalar-certificate.tex`, in a
reformulation that needs no integration and no reparametrisation: only
monotonicity of an explicit auxiliary function.

Throughout, `Y' v = 2 / ((1 - v²)(2 - v²))` is the derivative of `Y`
(`Y_deriv`).  The two identities that drive everything are

* the **elasticity identity** `Y v * E' v = (E v - K v) * Y' v`
  (equivalently `dE / d(log Y) = E - K`), and
* the **log-derivative identity** `P' v / P v = E v * Y' v / Y v`
  (equivalently `d(log P) / d(log Y) = E`).

From the first, the function `g k v = (E v - k) / Y v` has derivative
`(k - K v) * Y' v / (Y v)²`, so `g k` is strictly increasing wherever
`K < k`; since `K < 1` on `(0,1)` this applies to `k = 1`.  Clearing the
positive denominators in `g k v < g k u` gives the appendix's comparison
inequality, and combining both identities gives the integrated form via the
potential `Φ`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-! ### Basic positivity facts -/

lemma two_sub_sq_pos {v : ℝ} (hv : |v| < 1) : (0 : ℝ) < 2 - v ^ 2 := by
  have := one_sub_sq_pos hv; linarith

/-- `Y' v = 2 / ((1 - v²)(2 - v²)) > 0` on `(-1,1)`. -/
lemma Y_deriv_pos {v : ℝ} (hv : |v| < 1) :
    (0 : ℝ) < 2 / ((1 - v ^ 2) * (2 - v ^ 2)) := by
  have h1 := one_sub_sq_pos hv
  have h2 := two_sub_sq_pos hv
  positivity

lemma P_pos {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) : 0 < P v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  exact mul_pos hv0 (A_pos habs)

/-! ### 1. The elasticity identity -/

/-- `E = Y / id` is differentiable on `(0,1)`, with the quotient-rule derivative. -/
theorem E_hasDerivAt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    HasDerivAt E ((2 / ((1 - v ^ 2) * (2 - v ^ 2)) * v - Y v) / v ^ 2) v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h := (Y_deriv habs).div (hasDerivAt_id' (x := v)) hv0.ne'
  change HasDerivAt (fun y => Y y / y) _ v
  exact h.congr_deriv (by ring)

/-- `K v * Y' v = (Y v / v)²`: the coefficient `K` is exactly `Y² / (v² Y')`. -/
lemma K_mul_Y_deriv {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    K v * (2 / ((1 - v ^ 2) * (2 - v ^ 2))) = Y v ^ 2 / v ^ 2 := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := (one_sub_sq_pos habs).ne'
  have h2 := (two_sub_sq_pos habs).ne'
  simp only [K]
  field_simp

/-- **The elasticity identity.**  `Y v * E' v = (E v - K v) * Y' v`, i.e.
`dE / d(log Y) = E - K`. -/
theorem Y_mul_deriv_E {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    Y v * deriv E v = (E v - K v) * (2 / ((1 - v ^ 2) * (2 - v ^ 2))) := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := (one_sub_sq_pos habs).ne'
  have h2 := (two_sub_sq_pos habs).ne'
  rw [(E_hasDerivAt hv0 hv1).deriv]
  simp only [E, K]
  field_simp

/-! ### 2. The key monotonicity -/

/-- `g k v = (E v - k) / Y v`.  Along the flow it satisfies
`g' = (k - K) Y' / Y²`, so it increases wherever `K < k`. -/
noncomputable def g (k v : ℝ) : ℝ := (E v - k) / Y v

/-- `g k` is differentiable on `(0,1)` with derivative `(k - K v) Y' v / (Y v)²`. -/
theorem g_hasDerivAt {k v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    HasDerivAt (g k)
      ((k - K v) * (2 / ((1 - v ^ 2) * (2 - v ^ 2))) / Y v ^ 2) v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := (one_sub_sq_pos habs).ne'
  have h2 := (two_sub_sq_pos habs).ne'
  have hY := (Y_pos hv0 hv1).ne'
  have h := ((E_hasDerivAt hv0 hv1).sub_const k).div (Y_deriv habs) hY
  change HasDerivAt (fun y => (E y - k) / Y y) _ v
  refine h.congr_deriv ?_
  simp only [E, K]
  field_simp
  ring

/-- `g k` is strictly increasing on any `(a,b) ⊆ (0,1]` on which `K < k`. -/
theorem g_strictMonoOn_of_K_lt {k : ℝ} {a b : ℝ} (ha : 0 ≤ a) (hb : b ≤ 1)
    (hK : ∀ v, a < v → v < b → K v < k) : StrictMonoOn (g k) (Ioo a b) := by
  have hmem : ∀ x ∈ Ioo a b, 0 < x ∧ x < 1 := fun x hx =>
    ⟨lt_of_le_of_lt ha hx.1, lt_of_lt_of_le hx.2 hb⟩
  refine strictMonoOn_of_deriv_pos (convex_Ioo a b) ?_ ?_
  · intro x hx
    obtain ⟨hx0, hx1⟩ := hmem x hx
    exact (g_hasDerivAt (k := k) hx0 hx1).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioo] at hx
    obtain ⟨hx0, hx1⟩ := hmem x hx
    have habs : |x| < 1 := by rwa [abs_of_pos hx0]
    rw [(g_hasDerivAt (k := k) hx0 hx1).deriv]
    have hk := hK x hx.1 hx.2
    have hY := Y_pos hx0 hx1
    have := Y_deriv_pos habs
    positivity

/-- **Specialisation to `k = 1`.**  Since `K < 1` on `(0,1)`, `g 1` is strictly
increasing there. -/
theorem g_one_strictMonoOn : StrictMonoOn (g 1) (Ioo 0 1) :=
  g_strictMonoOn_of_K_lt le_rfl le_rfl (fun _ hv0 hv1 => (K_pos_lt_one hv0 hv1).2)

/-! ### 3. The comparison inequality -/

/-- **The comparison inequality.**  With `t = Y u / Y v > 1`, this is the
appendix's `E(ty) > k + t (E(y) - k)`.

Note the hypothesis asks for monotonicity of `g k` on all of `(0,1)`, which
by `g_one_strictMonoOn` holds at `k = 1` but NOT at `k = 107/200`: `K v → 1`
as `v → 0`, so `g (107/200)` decreases near `0`.  The certificate therefore
uses the interval-restricted variant `Phi_pos'` in `Final.lean`, and this
lemma is not on the critical path. -/
theorem E_comparison {k v u : ℝ} (hv0 : 0 < v) (hvu : v < u) (hu1 : u < 1)
    (hg : StrictMonoOn (g k) (Ioo 0 1)) :
    (E v - k) * (Y u / Y v) < E u - k := by
  have hu0 : 0 < u := hv0.trans hvu
  have hv1 : v < 1 := hvu.trans hu1
  have hYv : 0 < Y v := Y_pos hv0 hv1
  have hYu : 0 < Y u := Y_pos hu0 hu1
  have h : (E v - k) / Y v < (E u - k) / Y u := hg ⟨hv0, hv1⟩ ⟨hu0, hu1⟩ hvu
  have h' := mul_lt_mul_of_pos_right h hYu
  rw [div_mul_cancel₀ _ hYu.ne'] at h'
  calc (E v - k) * (Y u / Y v) = (E v - k) / Y v * Y u := by ring
    _ < E u - k := h'

/-! ### 4. The log-derivative identity `d(log P) / d(log Y) = E` -/

/-- `A' v = v (3 - v²) / (√(2 - v²) (1 - v²)²)`. -/
theorem A_hasDerivAt {v : ℝ} (hv : |v| < 1) :
    HasDerivAt A (v * (3 - v ^ 2) / (√(2 - v ^ 2) * (1 - v ^ 2) ^ 2)) v := by
  have h1 := one_sub_sq_pos hv
  have h2 := two_sub_sq_pos hv
  have hs : (0 : ℝ) < √(2 - v ^ 2) := Real.sqrt_pos.mpr h2
  have hs2 : √(2 - v ^ 2) * √(2 - v ^ 2) = 2 - v ^ 2 := Real.mul_self_sqrt h2.le
  have hin : HasDerivAt (fun x : ℝ => 2 - x ^ 2) (-(2 * v)) v := by
    simpa using (hasDerivAt_pow 2 v).const_sub (2 : ℝ)
  have hnum : HasDerivAt (fun x : ℝ => √(2 - x ^ 2))
      (-(2 * v) / (2 * √(2 - v ^ 2))) v := by
    have h := (Real.hasDerivAt_sqrt h2.ne').comp v hin
    rw [Function.comp_def] at h
    exact h.congr_deriv (by ring)
  have hden : HasDerivAt (fun x : ℝ => 1 - x ^ 2) (-(2 * v)) v := by
    simpa using (hasDerivAt_pow 2 v).const_sub (1 : ℝ)
  have h := hnum.div hden h1.ne'
  change HasDerivAt (fun x => √(2 - x ^ 2) / (1 - x ^ 2)) _ v
  refine h.congr_deriv ?_
  rw [div_eq_div_iff (by positivity) (by positivity)]
  field_simp
  rw [Real.sq_sqrt h2.le]
  ring

/-- `P' v = 2 / ((1 - v²)² √(2 - v²))`. -/
theorem P_hasDerivAt {v : ℝ} (hv : |v| < 1) :
    HasDerivAt P (2 / ((1 - v ^ 2) ^ 2 * √(2 - v ^ 2))) v := by
  have h1 := one_sub_sq_pos hv
  have h2 := two_sub_sq_pos hv
  have hs : (0 : ℝ) < √(2 - v ^ 2) := Real.sqrt_pos.mpr h2
  have hs2 : √(2 - v ^ 2) * √(2 - v ^ 2) = 2 - v ^ 2 := Real.mul_self_sqrt h2.le
  have h := (hasDerivAt_id' (x := v)).mul (A_hasDerivAt hv)
  change HasDerivAt (fun x => x * A x) _ v
  refine h.congr_deriv ?_
  simp only [A]
  field_simp
  rw [Real.sq_sqrt h2.le]
  ring

/-- **The log-derivative identity.**  `P' v / P v = E v * Y' v / Y v`, which
simplifies to `Y' v / v = 2 / (v (1 - v²)(2 - v²))`. -/
theorem logP_hasDerivAt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    HasDerivAt (fun x => Real.log (P x))
      (2 / (v * ((1 - v ^ 2) * (2 - v ^ 2)))) v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := one_sub_sq_pos habs
  have h2 := two_sub_sq_pos habs
  have hs : (0 : ℝ) < √(2 - v ^ 2) := Real.sqrt_pos.mpr h2
  have hs2 : √(2 - v ^ 2) * √(2 - v ^ 2) = 2 - v ^ 2 := Real.mul_self_sqrt h2.le
  have hP := P_pos hv0 hv1
  have hfac : 2 / ((1 - v ^ 2) ^ 2 * √(2 - v ^ 2))
      = P v * (2 / (v * ((1 - v ^ 2) * (2 - v ^ 2)))) := by
    simp only [P, A]
    field_simp
    rw [Real.sq_sqrt h2.le]
  have h := (P_hasDerivAt habs).log hP.ne'
  refine h.congr_deriv ?_
  rw [hfac]
  exact mul_div_cancel_left₀ _ hP.ne'

/-- The statement `d(log P)/d(log Y) = E` in the form used by the appendix. -/
theorem logP_deriv_eq {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    deriv (fun x => Real.log (P x)) v
      = E v * (2 / ((1 - v ^ 2) * (2 - v ^ 2))) / Y v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := (one_sub_sq_pos habs).ne'
  have h2 := (two_sub_sq_pos habs).ne'
  have hY := (Y_pos hv0 hv1).ne'
  rw [(logP_hasDerivAt hv0 hv1).deriv]
  simp only [E]
  field_simp

/-! ### The potential `Φ` -/

/-- The potential `Φ`: the integrated form of the comparison inequality.
`Φ k v₀ v = log P v - log P v₀ - (k (log Y v - log Y v₀) + (Y v / Y v₀ - 1)(E v₀ - k))`. -/
noncomputable def Phi (k v0 v : ℝ) : ℝ :=
  Real.log (P v) - Real.log (P v0)
    - (k * (Real.log (Y v) - Real.log (Y v0)) + (Y v / Y v0 - 1) * (E v0 - k))

theorem Phi_self {k v0 : ℝ} (hv0 : 0 < v0) (hv1 : v0 < 1) : Phi k v0 v0 = 0 := by
  have hY := (Y_pos hv0 hv1).ne'
  simp [Phi, div_self hY]

/-- `Φ' v = Y' v * (g k v - g k v₀)`. -/
theorem Phi_hasDerivAt {k v0 v : ℝ} (hv00 : 0 < v0) (hv01 : v0 < 1)
    (hv0 : 0 < v) (hv1 : v < 1) :
    HasDerivAt (Phi k v0)
      (2 / ((1 - v ^ 2) * (2 - v ^ 2)) * (g k v - g k v0)) v := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h1 := (one_sub_sq_pos habs).ne'
  have h2 := (two_sub_sq_pos habs).ne'
  have hY := (Y_pos hv0 hv1).ne'
  have hY0 := (Y_pos hv00 hv01).ne'
  have hlogP := logP_hasDerivAt hv0 hv1
  have hlogY := (Y_deriv habs).log hY
  have h2' := ((hlogY.sub_const (Real.log (Y v0))).const_mul k).add
      ((((Y_deriv habs).div_const (Y v0)).sub_const 1).mul_const (E v0 - k))
  have h := (hlogP.sub_const (Real.log (P v0))).sub h2'
  change HasDerivAt (fun x => Real.log (P x) - Real.log (P v0)
      - (k * (Real.log (Y x) - Real.log (Y v0))
        + (Y x / Y v0 - 1) * (E v0 - k))) _ v
  refine h.congr_deriv ?_
  simp only [g, E]
  field_simp
  ring

/-- `Φ k v₀` is strictly increasing on `[v₀, 1)`. -/
theorem Phi_strictMonoOn {k v0 : ℝ} (hv00 : 0 < v0) (hv01 : v0 < 1)
    (hg : StrictMonoOn (g k) (Ioo 0 1)) :
    StrictMonoOn (Phi k v0) (Ico v0 1) := by
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
    have hgx : g k v0 < g k x := hg ⟨hv00, hv01⟩ ⟨hx0, hx1⟩ hx.1
    have := Y_deriv_pos habs
    have : 0 < g k x - g k v0 := by linarith
    positivity

/-- **The integrated comparison inequality.**  `Φ k v₀ v > 0` for `v₀ < v < 1`.

As with `E_comparison`, the `(0,1)`-wide hypothesis is satisfiable only at
`k = 1`; `Final.lean`'s `Phi_pos'` is the version actually used. -/
theorem Phi_pos {k v0 v : ℝ} (hv0 : 0 < v0) (h : v0 < v) (hv1 : v < 1)
    (hg : StrictMonoOn (g k) (Ioo 0 1)) : 0 < Phi k v0 v := by
  have hv01 : v0 < 1 := h.trans hv1
  have hmono := Phi_strictMonoOn (k := k) hv0 hv01 hg
  have := hmono (left_mem_Ico.mpr hv01) ⟨h.le, hv1⟩ h
  rwa [Phi_self hv0 hv01] at this

end QipmFormal.ScalarCert
