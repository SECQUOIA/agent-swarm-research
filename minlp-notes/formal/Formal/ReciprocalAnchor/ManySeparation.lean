import Formal.ReciprocalAnchor.ManyAlgorithm
import Formal.ReciprocalAnchor.ManyGeometry

/-! The full family of rational cuts, including completeness at real candidates. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
open Set MeasureTheory

/-- A cut selects a source line independently on each rational interval. -/
structure RationalCut (n : ℕ) (a b : ℚ) where
  size : ℕ
  knots : Fin (size + 1) → ℚ
  active : Fin size → Fin (2 * n + 2)
  monotone : Monotone knots
  first : knots 0 = a
  last : knots (Fin.last size) = b

noncomputable def RationalCut.value {n : ℕ} {a b : ℚ} (c : RationalCut n a b)
    (m : ℝ) (q w : Fin n → ℝ) : ℝ :=
  1 / a - (m - a) / (a : ℝ) ^ 2 + ∑ i,
    ∫ s in (c.knots i.castSucc : ℝ)..(c.knots i.succ : ℝ),
      2 * line m q w (c.active i) s / s ^ 3

theorem RationalCut.knots_bounds {n : ℕ} {a b : ℚ} (c : RationalCut n a b)
    (i : Fin (c.size + 1)) : a ≤ c.knots i ∧ c.knots i ≤ b := by
  constructor
  · simpa only [c.first] using c.monotone (Fin.zero_le i)
  · simpa only [c.last] using c.monotone (Fin.le_last i)

theorem weighted_continuousOn {f : ℝ → ℝ} {a b : ℝ}
    (ha : 0 < a) (hf : Continuous f) :
    ContinuousOn (fun s => 2 * f s / s ^ 3) (Icc a b) := by
  fun_prop (disch := intro s hs; exact pow_ne_zero 3 (ne_of_gt (ha.trans_le hs.1)))

theorem RationalCut.segment_integrable {n : ℕ} {a b : ℚ} (c : RationalCut n a b)
    (ha : 0 < a) {f : ℝ → ℝ} (hf : Continuous f) (i : Fin c.size) :
    IntervalIntegrable (fun s => 2 * f s / s ^ 3) volume
      (c.knots i.castSucc : ℝ) (c.knots i.succ : ℝ) := by
  have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by
    exact_mod_cast c.monotone (Fin.castSucc_le_succ i)
  have hp : 0 < (c.knots i.castSucc : ℝ) := by
    exact_mod_cast ha.trans_le (c.knots_bounds i.castSucc).1
  apply ContinuousOn.intervalIntegrable
  simpa only [uIcc_of_le ho] using weighted_continuousOn hp hf

/-- Every selected-line cut is valid globally, even away from its construction point. -/
theorem RationalCut.value_le_lowerMoment {n : ℕ} {a b : ℚ} (c : RationalCut n a b)
    (ha : 0 < a) (m : ℝ) (q w : Fin n → ℝ) :
    c.value m q w ≤ lowerMoment a b m q w := by
  unfold value lowerMoment
  apply add_le_add_right
  have hs := sum_integral_fin_partition (fun i => (c.knots i : ℝ))
    (c.segment_integrable ha (envelope_continuous m q w))
  rw [c.first, c.last] at hs
  rw [← hs]
  apply Finset.sum_le_sum
  intro i _
  have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by
    exact_mod_cast c.monotone (Fin.castSucc_le_succ i)
  apply intervalIntegral.integral_mono_on ho
    (c.segment_integrable ha (line_continuous m q w (c.active i)) i)
    (c.segment_integrable ha (envelope_continuous m q w) i)
  intro s hs
  apply div_le_div_of_nonneg_right
    (mul_le_mul_of_nonneg_left (line_le_envelope m q w (c.active i) s) (by norm_num))
  exact pow_nonneg ((show (0 : ℝ) < a by exact_mod_cast ha).le.trans
    ((show (a : ℝ) ≤ c.knots i.castSucc by exact_mod_cast (c.knots_bounds i.castSucc).1).trans
      hs.1)) 3

/-- The finite maximum always has an active input line. -/
theorem exists_active_line {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) :
    ∃ i, line m q w i s = envelope m q w s := by
  have hm := Finset.max'_mem (Finset.univ.image (fun i => line m q w i s))
    (Finset.image_nonempty.mpr Finset.univ_nonempty)
  obtain ⟨i, _, hi⟩ := Finset.mem_image.mp hm
  exact ⟨i, hi⟩

/-- Picking an active line at the left endpoint loses at most the interval length. -/
theorem active_line_error {n : ℕ} {m l r s : ℝ} {q w : Fin n → ℝ}
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) {i : Fin (2 * n + 2)}
    (hi : line m q w i l = envelope m q w l) (hl : l ≤ s) (hr : s ≤ r) :
    0 ≤ envelope m q w s - line m q w i s ∧
      envelope m q w s - line m q w i s ≤ r - l := by
  have hline := line_secant (m := m) (w := w) hq hl i
  have henv := envelope_secant (m := m) (w := w) hq hl
  constructor
  · exact sub_nonneg.mpr (line_le_envelope m q w i s)
  · linarith

/-- The sum of interval lengths is exactly the length of the full domain. -/
theorem RationalCut.sum_lengths {n : ℕ} {a b : ℚ} (c : RationalCut n a b) :
    (∑ i : Fin c.size, ((c.knots i.succ : ℝ) - c.knots i.castSucc)) = (b : ℝ) - a := by
  have hs := sum_integral_fin_partition (f := fun _ => (1 : ℝ))
    (fun i => (c.knots i : ℝ)) (fun _ => intervalIntegrable_const)
  simpa only [intervalIntegral.integral_const, smul_eq_mul, mul_one, c.first, c.last] using hs

/-- A mesh bound controls how much a cut can underestimate the envelope integral. -/
theorem RationalCut.lowerMoment_le_value_add {n : ℕ} {a b : ℚ}
    (c : RationalCut n a b) (ha : 0 < a) (m : ℝ) (q w : Fin n → ℝ)
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) {δ : ℝ} (hδ : 0 ≤ δ)
    (hmesh : ∀ i : Fin c.size, (c.knots i.succ : ℝ) - c.knots i.castSucc ≤ δ)
    (hactive : ∀ i, line m q w (c.active i) (c.knots i.castSucc) =
      envelope m q w (c.knots i.castSucc)) :
    lowerMoment a b m q w ≤ c.value m q w + 2 * δ / (a : ℝ) ^ 3 * ((b : ℝ) - a) := by
  have haR : (0 : ℝ) < a := by exact_mod_cast ha
  let K : ℝ := 2 * δ / (a : ℝ) ^ 3
  have hK : 0 ≤ K := div_nonneg (mul_nonneg (by norm_num) hδ) (pow_nonneg haR.le 3)
  have hi (i : Fin c.size) :
      (∫ s in (c.knots i.castSucc : ℝ)..(c.knots i.succ : ℝ),
        2 * envelope m q w s / s ^ 3) ≤
      (∫ s in (c.knots i.castSucc : ℝ)..(c.knots i.succ : ℝ),
        2 * line m q w (c.active i) s / s ^ 3) +
        K * ((c.knots i.succ : ℝ) - c.knots i.castSucc) := by
    have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by
      exact_mod_cast c.monotone (Fin.castSucc_le_succ i)
    have hl := c.segment_integrable ha (line_continuous m q w (c.active i)) i
    have he := c.segment_integrable ha (envelope_continuous m q w) i
    have hpoint : ∀ s ∈ Icc (c.knots i.castSucc : ℝ) (c.knots i.succ : ℝ),
        2 * envelope m q w s / s ^ 3 ≤ 2 * line m q w (c.active i) s / s ^ 3 + K := by
      intro s hs
      have has : (a : ℝ) ≤ s :=
        (show (a : ℝ) ≤ c.knots i.castSucc by
          exact_mod_cast (c.knots_bounds i.castSucc).1).trans hs.1
      have hspos : 0 < s := haR.trans_le has
      have herr := active_line_error hq (hactive i) hs.1 hs.2
      have hgap : envelope m q w s - line m q w (c.active i) s ≤ δ :=
        herr.2.trans (hmesh i)
      have hden : (a : ℝ) ^ 3 ≤ s ^ 3 := by gcongr
      have hmul : 2 * (envelope m q w s - line m q w (c.active i) s) ≤ K * s ^ 3 := by
        have heq : K * (a : ℝ) ^ 3 = 2 * δ := by dsimp [K]; field_simp
        nlinarith [mul_le_mul_of_nonneg_left hden hK]
      have hdiv := (div_le_iff₀ (pow_pos hspos 3)).mpr hmul
      calc
        _ = 2 * line m q w (c.active i) s / s ^ 3 +
            2 * (envelope m q w s - line m q w (c.active i) s) / s ^ 3 := by ring
        _ ≤ _ := add_le_add_right hdiv _
    have hbound := intervalIntegral.integral_mono_on ho he (hl.add intervalIntegrable_const) hpoint
    rw [intervalIntegral.integral_add hl intervalIntegrable_const,
      intervalIntegral.integral_const] at hbound
    simpa only [smul_eq_mul, mul_comm K] using hbound
  have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hi i)
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, c.sum_lengths] at hsum
  have ht := sum_integral_fin_partition (fun i => (c.knots i : ℝ))
    (c.segment_integrable ha (envelope_continuous m q w))
  rw [c.first, c.last] at ht
  rw [ht] at hsum
  unfold lowerMoment value
  dsimp [K] at hsum
  linarith

/-- Rational uniform knots remain rational even when the candidate coordinates are real. -/
def uniformKnot (a b : ℚ) (N : ℕ) (i : Fin (N + 1)) : ℚ :=
  a + (b - a) * (i.val : ℚ) / N

theorem uniformKnot_monotone {a b : ℚ} (hab : a ≤ b) (N : ℕ) :
    Monotone (uniformKnot a b N) := by
  intro i j hij
  unfold uniformKnot
  gcongr
  exact_mod_cast hij

@[simp] theorem uniformKnot_zero (a b : ℚ) (N : ℕ) : uniformKnot a b N 0 = a := by
  simp [uniformKnot]

@[simp] theorem uniformKnot_last (a b : ℚ) {N : ℕ} (hN : 0 < N) :
    uniformKnot a b N (Fin.last N) = b := by
  have hn : (N : ℚ) ≠ 0 := by exact_mod_cast ne_of_gt hN
  simp [uniformKnot, hn]

/-- Select a maximizing line separately at every left grid endpoint. -/
noncomputable def uniformCut {n : ℕ} {a b : ℚ} (hab : a ≤ b) (N : ℕ) (hN : 0 < N)
    (m : ℝ) (q w : Fin n → ℝ) : RationalCut n a b where
  size := N
  knots := uniformKnot a b N
  active := fun i => (exists_active_line m q w (uniformKnot a b N i.castSucc)).choose
  monotone := uniformKnot_monotone hab N
  first := uniformKnot_zero a b N
  last := uniformKnot_last a b hN

theorem uniformCut_active {n : ℕ} {a b : ℚ} (hab : a ≤ b) (N : ℕ) (hN : 0 < N)
    (m : ℝ) (q w : Fin n → ℝ) (i : Fin N) :
    line m q w ((uniformCut hab N hN m q w).active i)
      ((uniformCut hab N hN m q w).knots i.castSucc) =
    envelope m q w ((uniformCut hab N hN m q w).knots i.castSucc) :=
  (exists_active_line m q w (uniformKnot a b N i.castSucc)).choose_spec

theorem uniformKnot_mesh {a b : ℚ} {N : ℕ} (i : Fin N) :
    (uniformKnot a b N i.succ : ℝ) - uniformKnot a b N i.castSucc =
      ((b : ℝ) - a) / N := by
  simp only [uniformKnot, Fin.val_succ, Fin.val_castSucc]
  push_cast
  ring

/-- Every lower moment is approached from below by rational selected-line cuts. -/
theorem exists_rationalCut_approx {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    (m : ℝ) (q w : Fin n → ℝ) (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ c : RationalCut n a b, lowerMoment a b m q w < c.value m q w + ε := by
  have haR : (0 : ℝ) < a := by exact_mod_cast ha
  have habR : (a : ℝ) < b := by exact_mod_cast hab
  let B : ℝ := 2 * ((b : ℝ) - a) ^ 2 / (a : ℝ) ^ 3
  have hB : 0 < B := div_pos (mul_pos (by norm_num) (sq_pos_of_pos (sub_pos.mpr habR)))
    (pow_pos haR 3)
  obtain ⟨N, hN⟩ := exists_nat_gt (B / ε)
  have hNposR : (0 : ℝ) < N := (div_pos hB hε).trans hN
  have hNpos : 0 < N := by exact_mod_cast hNposR
  let c := uniformCut hab.le N hNpos m q w
  refine ⟨c, ?_⟩
  have hmesh : ∀ i : Fin c.size, (c.knots i.succ : ℝ) - c.knots i.castSucc ≤
      ((b : ℝ) - a) / N := fun i => (uniformKnot_mesh i).le
  have hbound := c.lowerMoment_le_value_add ha m q w hq
    (div_nonneg (sub_nonneg.mpr habR.le) hNposR.le) hmesh
    (uniformCut_active hab.le N hNpos m q w)
  have heq : 2 * (((b : ℝ) - a) / N) / (a : ℝ) ^ 3 * ((b : ℝ) - a) = B / N := by
    dsimp [B]
    ring
  rw [heq] at hbound
  have herr : B / N < ε := (div_lt_iff₀ hNposR).mpr (by
    simpa only [mul_comm] using (div_lt_iff₀ hε).mp hN)
  linarith

/-- All rational selected-line cuts characterize the lower moment, including at real inputs. -/
theorem all_rationalCuts_iff_lowerMoment {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    (m t : ℝ) (q w : Fin n → ℝ) (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) :
    (∀ c : RationalCut n a b, c.value m q w ≤ t) ↔ lowerMoment a b m q w ≤ t := by
  constructor
  · intro h
    by_contra ht
    have hgap : 0 < lowerMoment a b m q w - t := sub_pos.mpr (lt_of_not_ge ht)
    obtain ⟨c, hc⟩ := exists_rationalCut_approx ha hab m q w hq hgap
    linarith [h c]
  · intro h c
    exact (c.value_le_lowerMoment ha m q w).trans h

/-- Explicit rational coefficients for the constant, mean, leaf masses, and leaf moments. -/
abbrev RationalAffineForm (n : ℕ) := ℚ × ℚ × (Fin n → ℚ) × (Fin n → ℚ)

def RationalAffineForm.eval {n : ℕ} (F : RationalAffineForm n)
    (m : ℝ) (q w : Fin n → ℝ) : ℝ :=
  F.1 + (F.2.1 : ℝ) * m + ∑ j, (F.2.2.1 j : ℝ) * q j +
    ∑ j, (F.2.2.2 j : ℝ) * w j

@[simp] theorem RationalAffineForm.eval_zero {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) :
    RationalAffineForm.eval (0 : RationalAffineForm n) m q w = 0 := by simp [eval]

theorem RationalAffineForm.eval_add {n : ℕ} (F G : RationalAffineForm n)
    (m : ℝ) (q w : Fin n → ℝ) : (F + G).eval m q w = F.eval m q w + G.eval m q w := by
  simp only [eval, Prod.fst_add, Prod.snd_add, Pi.add_apply, Rat.cast_add, add_mul,
    Finset.sum_add_distrib]
  ring

theorem RationalAffineForm.eval_sum {ι : Type*} {n : ℕ} (S : Finset ι)
    (F : ι → RationalAffineForm n) (m : ℝ) (q w : Fin n → ℝ) :
    (∑ i ∈ S, F i).eval m q w = ∑ i ∈ S, (F i).eval m q w := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert i S hi ih => simp [hi, eval_add, ih]

/-- Integrating one source line yields this rational affine form. -/
def segmentForm {n : ℕ} (i : Fin (2 * n + 2)) (α β : ℚ) : RationalAffineForm n :=
  let A := (α ^ 2)⁻¹ - (β ^ 2)⁻¹
  let B := 2 * (α⁻¹ - β⁻¹)
  if h : i.val < n then
    (0, 0, (fun j => if j = ⟨i.val, h⟩ then -B else 0),
      (fun j => if j = ⟨i.val, h⟩ then A else 0))
  else if h' : i.val < 2 * n then
    (-B, A, (fun j => if j = ⟨i.val - n, by omega⟩ then B else 0),
      (fun j => if j = ⟨i.val - n, by omega⟩ then -A else 0))
  else if i.val = 2 * n then 0 else (-B, A, 0, 0)

theorem segmentForm_eval {n : ℕ} (i : Fin (2 * n + 2)) (α β : ℚ)
    (m : ℝ) (q w : Fin n → ℝ) :
    (segmentForm i α β).eval m q w =
      line m q w i 0 * (((α : ℝ) ^ 2)⁻¹ - ((β : ℝ) ^ 2)⁻¹) -
      2 * (line m q w i 0 - line m q w i 1) * ((α : ℝ)⁻¹ - (β : ℝ)⁻¹) := by
  unfold segmentForm line
  split_ifs <;> simp [RationalAffineForm.eval, apply_ite, ite_mul] <;> ring

theorem line_intercept_slope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ)
    (i : Fin (2 * n + 2)) (s : ℝ) :
    line m q w i s = line m q w i 0 - (line m q w i 0 - line m q w i 1) * s := by
  unfold line
  split_ifs <;> ring

theorem segmentForm_eval_eq_integral {n : ℕ} (i : Fin (2 * n + 2)) {α β : ℚ}
    (hα : 0 < α) (hαβ : α ≤ β) (m : ℝ) (q w : Fin n → ℝ) :
    (segmentForm i α β).eval m q w =
      ∫ s in (α : ℝ)..(β : ℝ), 2 * line m q w i s / s ^ 3 := by
  rw [segmentForm_eval, ← affine_call_integral (by exact_mod_cast hα)
    (by exact_mod_cast hαβ)]
  apply intervalIntegral.integral_congr
  intro s _
  simp only [← line_intercept_slope]

/-- The cut coefficients are rational and independent of the tested real coordinates. -/
def RationalCut.coefficients {n : ℕ} {a b : ℚ} (c : RationalCut n a b) :
    RationalAffineForm n :=
  (1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) +
    ∑ i, segmentForm (c.active i) (c.knots i.castSucc) (c.knots i.succ)

/-- The integral cut is exactly an affine expression with explicit rational coefficients. -/
theorem RationalCut.coefficients_eval {n : ℕ} {a b : ℚ} (c : RationalCut n a b)
    (ha : 0 < a) (m : ℝ) (q w : Fin n → ℝ) :
    c.coefficients.eval m q w = c.value m q w := by
  unfold coefficients value
  rw [RationalAffineForm.eval_add, RationalAffineForm.eval_sum]
  have hsum : (∑ i, (segmentForm (c.active i) (c.knots i.castSucc)
      (c.knots i.succ)).eval m q w) = ∑ i,
      ∫ s in (c.knots i.castSucc : ℝ)..(c.knots i.succ : ℝ),
        2 * line m q w (c.active i) s / s ^ 3 := by
    apply Finset.sum_congr rfl
    intro i _
    exact segmentForm_eval_eq_integral (c.active i)
      (ha.trans_le (c.knots_bounds i.castSucc).1)
      (c.monotone (Fin.castSucc_le_succ i)) m q w
  rw [hsum]
  congr 1
  simp [RationalAffineForm.eval]
  ring

/-- A violated lower bound has a strictly separating rational affine cut. -/
theorem exists_rational_separating_cut {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    (m t : ℝ) (q w : Fin n → ℝ) (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1)
    (ht : t < lowerMoment a b m q w) :
    ∃ c : RationalCut n a b, t < c.coefficients.eval m q w ∧
      ∀ m' q' w', c.coefficients.eval m' q' w' ≤ lowerMoment a b m' q' w' := by
  obtain ⟨c, hc⟩ := exists_rationalCut_approx ha hab m q w hq (sub_pos.mpr ht)
  refine ⟨c, ?_, fun m' q' w' => ?_⟩
  · rw [c.coefficients_eval ha]
    linarith
  · rw [c.coefficients_eval ha]
    exact c.value_le_lowerMoment ha m' q' w'

/-- A partition following the active envelope gives equality at its construction point. -/
theorem RationalCut.value_eq_lowerMoment_of_active {n : ℕ} {a b : ℚ}
    (c : RationalCut n a b) (ha : 0 < a) (m : ℝ) (q w : Fin n → ℝ)
    (hactive : ∀ i : Fin c.size, ∀ s ∈ Icc (c.knots i.castSucc : ℝ) (c.knots i.succ : ℝ),
      line m q w (c.active i) s = envelope m q w s) :
    c.value m q w = lowerMoment a b m q w := by
  unfold value lowerMoment
  congr 1
  have hs := sum_integral_fin_partition (fun i => (c.knots i : ℝ))
    (c.segment_integrable ha (envelope_continuous m q w))
  rw [c.first, c.last] at hs
  rw [← hs]
  apply Finset.sum_congr rfl
  intro i _
  apply intervalIntegral.integral_congr
  intro s hsi
  have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by
    exact_mod_cast c.monotone (Fin.castSucc_le_succ i)
  rw [uIcc_of_le ho] at hsi
  simp only [hactive i s hsi]

/-- A certified rational envelope is also a member of the global cut family. -/
def RationalEnvelopeCertificate.toCut {n k : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (c : RationalEnvelopeCertificate (2 * n + 2) k) (hc : c.Valid (rationalLines m q w) a b) :
    RationalCut n a b where
  size := k
  knots := c.knots
  active := c.active
  monotone := c.monotone hc
  first := hc.1
  last := hc.2.1

/-- Keeping a rational candidate's active intervals yields an exact supporting cut. -/
theorem RationalEnvelopeCertificate.toCut_exact {n k : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (c : RationalEnvelopeCertificate (2 * n + 2) k) (hc : c.Valid (rationalLines m q w) a b)
    (ha : 0 < a) :
    (c.toCut hc).coefficients.eval m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) =
      lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
  rw [RationalCut.coefficients_eval _ ha]
  apply RationalCut.value_eq_lowerMoment_of_active _ ha
  intro i s hs
  exact (rationalLines_evalReal m q w (c.active i) s).symm.trans
    (c.active_eq_envelope hc i hs.1 hs.2)

end ReciprocalAnchor.ManyLeaf
