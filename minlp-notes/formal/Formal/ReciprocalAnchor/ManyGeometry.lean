import Formal.ReciprocalAnchor.ManyModel
import Formal.ReciprocalAnchor.ManyEnvelope

namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

theorem line_le_envelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ)
    (i : Fin (2 * n + 2)) (s : ℝ) : line m q w i s ≤ envelope m q w s := by
  classical
  unfold envelope
  exact Finset.le_max' (Finset.univ.image (fun j => line m q w j s)) _
    (Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩)

theorem envelope_le {n : ℕ} {m s c : ℝ} {q w : Fin n → ℝ}
    (h : ∀ i, line m q w i s ≤ c) : envelope m q w s ≤ c := by
  apply Finset.max'_le
  intro v hv
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hv
  exact h i

@[simp] theorem line_leaf {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (j : Fin n) (s : ℝ) :
    line m q w ⟨j.val, by omega⟩ s = w j - q j * s := by simp [line, j.isLt]

@[simp] theorem line_complement {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (j : Fin n) (s : ℝ) :
    line m q w ⟨n + j.val, by omega⟩ s = m - w j - (1 - q j) * s := by
  simp [line, show ¬n + j.val < n by omega, show n + j.val < 2 * n by omega]

@[simp] theorem line_zero {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) :
    line m q w ⟨2 * n, by omega⟩ s = 0 := by
  simp [line, show ¬2 * n < n by omega]

@[simp] theorem line_mean {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) :
    line m q w ⟨2 * n + 1, by omega⟩ s = m - s := by
  simp [line, show ¬2 * n + 1 < n by omega]

theorem envelope_nonneg {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) :
    0 ≤ envelope m q w s := by
  simpa using line_le_envelope m q w ⟨2 * n, by omega⟩ s

theorem mean_sub_le_envelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) :
    m - s ≤ envelope m q w s := by
  simpa using line_le_envelope m q w ⟨2 * n + 1, by omega⟩ s

theorem leaf_le_envelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) (j : Fin n) :
    w j - q j * s ≤ envelope m q w s := by
  simpa using line_le_envelope m q w ⟨j.val, by omega⟩ s

theorem complement_le_envelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) (j : Fin n) :
    m - w j - (1 - q j) * s ≤ envelope m q w s := by
  simpa using line_le_envelope m q w ⟨n + j.val, by omega⟩ s

theorem envelope_le_iff {n : ℕ} {m s c : ℝ} {q w : Fin n → ℝ} :
    envelope m q w s ≤ c ↔ 0 ≤ c ∧ m - s ≤ c ∧
      ∀ j, w j - q j * s ≤ c ∧ m - w j - (1 - q j) * s ≤ c := by
  constructor
  · intro h
    exact ⟨(envelope_nonneg _ _ _ _).trans h, (mean_sub_le_envelope _ _ _ _).trans h,
      fun j => ⟨(leaf_le_envelope _ _ _ _ j).trans h,
        (complement_le_envelope _ _ _ _ j).trans h⟩⟩
  · rintro ⟨h0, hm, hj⟩
    apply envelope_le
    intro i
    unfold line
    split_ifs with h h' h''
    · exact (hj ⟨i.val, h⟩).1
    · exact (hj ⟨i.val - n, by omega⟩).2
    · exact h0
    · exact hm

theorem envelope_left {n : ℕ} {a b m s : ℝ} {q w : Fin n → ℝ}
    (h : LinearBounds a b m q w) (hs : s ≤ a) : envelope m q w s = m - s := by
  apply le_antisymm _ (mean_sub_le_envelope _ _ _ _)
  apply envelope_le_iff.mpr
  refine ⟨by linarith [h.1], le_rfl, fun j => ?_⟩
  obtain ⟨hq, hq1, hw, _, hc, _⟩ := h.2.2 j
  constructor <;> nlinarith [mul_nonneg (sub_nonneg.mpr hs) hq,
    mul_nonneg (sub_nonneg.mpr hs) (sub_nonneg.mpr hq1)]

theorem envelope_right {n : ℕ} {a b m s : ℝ} {q w : Fin n → ℝ}
    (h : LinearBounds a b m q w) (hs : b ≤ s) : envelope m q w s = 0 := by
  apply le_antisymm _ (envelope_nonneg _ _ _ _)
  apply envelope_le_iff.mpr
  refine ⟨le_rfl, by linarith [h.2.1], fun j => ?_⟩
  obtain ⟨hq, hq1, _, hw, _, hc⟩ := h.2.2 j
  constructor <;> nlinarith [mul_nonneg (sub_nonneg.mpr hs) hq,
    mul_nonneg (sub_nonneg.mpr hs) (sub_nonneg.mpr hq1)]

theorem line_continuous {n : ℕ} (m : ℝ) (q w : Fin n → ℝ)
    (i : Fin (2 * n + 2)) : Continuous (line m q w i) := by
  unfold line
  split_ifs <;> fun_prop

theorem envelope_continuous {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    Continuous (envelope m q w) := by
  classical
  change Continuous (fun s => envelope m q w s)
  simp only [envelope, Finset.max'_eq_sup', Finset.sup'_image, Function.comp_def, id_eq]
  exact Continuous.finset_sup'_apply Finset.univ_nonempty (fun i _ => line_continuous m q w i)

theorem line_affine {n : ℕ} (m : ℝ) (q w : Fin n → ℝ)
    (i : Fin (2 * n + 2)) (s t u v : ℝ) (huv : u + v = 1) :
    line m q w i (u * s + v * t) = u * line m q w i s + v * line m q w i t := by
  unfold line
  have hv : v = 1 - u := by linarith
  subst v
  split_ifs <;> ring

theorem envelope_convex {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    ConvexOn ℝ Set.univ (envelope m q w) := by
  refine ⟨convex_univ, ?_⟩
  intro s _ t _ u v hu hv huv
  change envelope m q w (u * s + v * t) ≤ u * envelope m q w s + v * envelope m q w t
  apply envelope_le
  intro i
  rw [line_affine m q w i s t u v huv]
  exact add_le_add (mul_le_mul_of_nonneg_left (line_le_envelope _ _ _ _ _) hu)
    (mul_le_mul_of_nonneg_left (line_le_envelope _ _ _ _ _) hv)

theorem line_secant {n : ℕ} {m s t : ℝ} {q w : Fin n → ℝ}
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) (hst : s ≤ t) (i : Fin (2 * n + 2)) :
    -(t - s) ≤ line m q w i t - line m q w i s ∧
    line m q w i t - line m q w i s ≤ 0 := by
  unfold line
  split_ifs with h h' h''
  · have hj := hq ⟨i.val, h⟩
    constructor <;> nlinarith [mul_nonneg (sub_nonneg.mpr hst) hj.1,
      mul_nonneg (sub_nonneg.mpr hst) (sub_nonneg.mpr hj.2)]
  · have hj := hq ⟨i.val - n, by omega⟩
    constructor <;> nlinarith [mul_nonneg (sub_nonneg.mpr hst) hj.1,
      mul_nonneg (sub_nonneg.mpr hst) (sub_nonneg.mpr hj.2)]
  · constructor <;> linarith
  · constructor <;> linarith

theorem envelope_secant {n : ℕ} {m s t : ℝ} {q w : Fin n → ℝ}
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) (hst : s ≤ t) :
    -(t - s) ≤ envelope m q w t - envelope m q w s ∧
    envelope m q w t - envelope m q w s ≤ 0 := by
  have ht : envelope m q w t ≤ envelope m q w s := by
    apply envelope_le
    intro i
    have hi := line_secant (m := m) (w := w) hq hst i
    have hj := line_le_envelope m q w i s
    linarith
  have hs : envelope m q w s ≤ envelope m q w t + (t - s) := by
    apply envelope_le
    intro i
    have hi := line_secant (m := m) (w := w) hq hst i
    have hj := line_le_envelope m q w i t
    linarith
  constructor <;> linarith

theorem line_coordinates_affine {n : ℕ} (m₁ m₂ : ℝ) (q₁ q₂ w₁ w₂ : Fin n → ℝ)
    (i : Fin (2 * n + 2)) (s u v : ℝ) (huv : u + v = 1) :
    line (u * m₁ + v * m₂) (fun j => u * q₁ j + v * q₂ j)
      (fun j => u * w₁ j + v * w₂ j) i s =
      u * line m₁ q₁ w₁ i s + v * line m₂ q₂ w₂ i s := by
  have hv : v = 1 - u := by linarith
  subst v
  unfold line
  split_ifs <;> ring

theorem envelope_coordinates_convex {n : ℕ} (m₁ m₂ : ℝ) (q₁ q₂ w₁ w₂ : Fin n → ℝ)
    (s u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) (huv : u + v = 1) :
    envelope (u * m₁ + v * m₂) (fun j => u * q₁ j + v * q₂ j)
      (fun j => u * w₁ j + v * w₂ j) s ≤
      u * envelope m₁ q₁ w₁ s + v * envelope m₂ q₂ w₂ s := by
  apply envelope_le
  intro i
  rw [line_coordinates_affine m₁ m₂ q₁ q₂ w₁ w₂ i s u v huv]
  exact add_le_add (mul_le_mul_of_nonneg_left (line_le_envelope _ _ _ _ _) hu)
    (mul_le_mul_of_nonneg_left (line_le_envelope _ _ _ _ _) hv)

theorem envelope_coordinates_continuous {X : Type*} [TopologicalSpace X] {n : ℕ}
    (m : X → ℝ) (q w : X → Fin n → ℝ) (s : X → ℝ)
    (hm : Continuous m) (hq : ∀ j, Continuous (fun x => q x j))
    (hw : ∀ j, Continuous (fun x => w x j)) (hs : Continuous s) :
    Continuous (fun x => envelope (m x) (q x) (w x) (s x)) := by
  classical
  simp only [envelope, Finset.max'_eq_sup', Finset.sup'_image, Function.comp_def, id_eq]
  apply Continuous.finset_sup'_apply Finset.univ_nonempty
  intro i _
  unfold line
  split_ifs <;> fun_prop

theorem envelope_integrand_continuousOn {n : ℕ} {a b : ℝ} (ha : 0 < a)
    (m : ℝ) (q w : Fin n → ℝ) :
    ContinuousOn (fun s => 2 * envelope m q w s / s ^ 3) (Set.Icc a b) := by
  have hC := (envelope_continuous m q w).continuousOn (s := Set.Icc a b)
  have hn : ∀ s ∈ Set.Icc a b, s ^ 3 ≠ 0 := fun s hs =>
    pow_ne_zero 3 (ne_of_gt (ha.trans_le hs.1))
  fun_prop (disch := aesop)

theorem envelope_integrand_integrable {n : ℕ} {a b : ℝ} (ha : 0 < a) (hab : a ≤ b)
    (m : ℝ) (q w : Fin n → ℝ) :
    IntervalIntegrable (fun s => 2 * envelope m q w s / s ^ 3) MeasureTheory.volume a b := by
  apply ContinuousOn.intervalIntegrable
  simpa only [Set.uIcc_of_le hab] using envelope_integrand_continuousOn ha m q w

theorem lowerMoment_coordinates_convex {n : ℕ} {a b : ℝ} (ha : 0 < a) (hab : a ≤ b)
    (m₁ m₂ : ℝ) (q₁ q₂ w₁ w₂ : Fin n → ℝ)
    (u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) (huv : u + v = 1) :
    lowerMoment a b (u * m₁ + v * m₂) (fun j => u * q₁ j + v * q₂ j)
      (fun j => u * w₁ j + v * w₂ j) ≤
      u * lowerMoment a b m₁ q₁ w₁ + v * lowerMoment a b m₂ q₂ w₂ := by
  have h₁ := envelope_integrand_integrable ha hab m₁ q₁ w₁
  have h₂ := envelope_integrand_integrable ha hab m₂ q₂ w₂
  have hmix := envelope_integrand_integrable ha hab (u * m₁ + v * m₂)
    (fun j => u * q₁ j + v * q₂ j) (fun j => u * w₁ j + v * w₂ j)
  have hi := intervalIntegral.integral_mono_on hab hmix ((h₁.const_mul u).add (h₂.const_mul v))
    (fun s (hs : s ∈ Set.Icc a b) => show
      2 * envelope (u * m₁ + v * m₂) (fun j => u * q₁ j + v * q₂ j)
        (fun j => u * w₁ j + v * w₂ j) s / s ^ 3 ≤
        u * (2 * envelope m₁ q₁ w₁ s / s ^ 3) + v * (2 * envelope m₂ q₂ w₂ s / s ^ 3) from by
      have he := div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_left (envelope_coordinates_convex m₁ m₂ q₁ q₂ w₁ w₂ s u v hu hv huv)
          (by norm_num : (0 : ℝ) ≤ 2)) (pow_nonneg (ha.trans_le hs.1).le 3)
      calc
        _ ≤ 2 * (u * envelope m₁ q₁ w₁ s + v * envelope m₂ q₂ w₂ s) / s ^ 3 := he
        _ = _ := by ring)
  rw [intervalIntegral.integral_add (h₁.const_mul u) (h₂.const_mul v),
    intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul] at hi
  unfold lowerMoment
  have hv' : v = 1 - u := by linarith
  subst v
  have hi' := add_le_add_left hi (1 / a - (u * m₁ + (1 - u) * m₂ - a) / a ^ 2)
  convert hi' using 1 <;> ring

def lineIntercept {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (i : Fin (2 * n + 2)) : ℝ :=
  line m q w i 0

def lineSlope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (i : Fin (2 * n + 2)) : ℝ :=
  line m q w i 1 - line m q w i 0

theorem line_eq_intercept_slope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ)
    (i : Fin (2 * n + 2)) (s : ℝ) :
    line m q w i s = lineIntercept m q w i + lineSlope m q w i * s := by
  unfold lineIntercept lineSlope line
  split_ifs <;> ring

theorem envelope_eq_affineEnvelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    envelope m q w = affineEnvelope (lineIntercept m q w) (lineSlope m q w) := by
  classical
  funext s
  simp only [envelope, Finset.max'_eq_sup', Finset.sup'_image, Function.comp_def, id_eq,
    affineEnvelope, line_eq_intercept_slope]

theorem lineSlope_bounds {n : ℕ} {m : ℝ} {q w : Fin n → ℝ}
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) (i : Fin (2 * n + 2)) :
    -1 ≤ lineSlope m q w i ∧ lineSlope m q w i ≤ 0 := by
  simpa [lineSlope] using line_secant (m := m) (w := w) hq (show (0 : ℝ) ≤ 1 by norm_num) i

theorem lineSlope_neg_one {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    lineSlope m q w ⟨2 * n + 1, by omega⟩ = -1 := by simp [lineSlope]

theorem lineSlope_zero {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    lineSlope m q w ⟨2 * n, by omega⟩ = 0 := by simp [lineSlope]

end ReciprocalAnchor.ManyLeaf
