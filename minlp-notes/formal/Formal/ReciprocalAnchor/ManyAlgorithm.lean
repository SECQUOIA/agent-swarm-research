import Formal.ReciprocalAnchor.ManyIntegrals
import Formal.ReciprocalAnchor.ManyModel

/-! Exact rational data and independently checkable envelope certificates. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
open Set MeasureTheory

/-- A rational affine line, in the convention used in the integral formula. -/
structure RationalLine where
  intercept : ℚ
  negSlope : ℚ
  deriving DecidableEq, Repr

def RationalLine.eval (l : RationalLine) (s : ℚ) : ℚ :=
  l.intercept - l.negSlope * s

def RationalLine.evalReal (l : RationalLine) (s : ℝ) : ℝ :=
  (l.intercept : ℝ) - (l.negSlope : ℝ) * s

@[simp] theorem RationalLine.cast_eval (l : RationalLine) (s : ℚ) :
    ((l.eval s : ℚ) : ℝ) = l.evalReal s := by
  simp [eval, evalReal]

/-- Exact reciprocal-weighted integral of an affine line. -/
def rationalSegmentIntegral (l : RationalLine) (a b : ℚ) : ℚ :=
  l.intercept * ((a ^ 2)⁻¹ - (b ^ 2)⁻¹) -
    2 * l.negSlope * (a⁻¹ - b⁻¹)

@[simp] theorem cast_rationalSegmentIntegral (l : RationalLine) (a b : ℚ) :
    (rationalSegmentIntegral l a b : ℝ) =
      (l.intercept : ℝ) * (((a : ℝ) ^ 2)⁻¹ - ((b : ℝ) ^ 2)⁻¹) -
        2 * (l.negSlope : ℝ) * ((a : ℝ)⁻¹ - (b : ℝ)⁻¹) := by
  simp [rationalSegmentIntegral]

/-- Endpoints suffice to certify comparison of two affine functions throughout an interval. -/
theorem RationalLine.le_on_interval {l r : RationalLine} {a b : ℚ}
    (ha : l.eval a ≤ r.eval a) (hb : l.eval b ≤ r.eval b)
    {s : ℝ} (has : (a : ℝ) ≤ s) (hsb : s ≤ (b : ℝ)) :
    l.evalReal s ≤ r.evalReal s := by
  have ha' : l.evalReal a ≤ r.evalReal a := by
    rw [← cast_eval, ← cast_eval]
    exact_mod_cast ha
  have hb' : l.evalReal b ≤ r.evalReal b := by
    rw [← cast_eval, ← cast_eval]
    exact_mod_cast hb
  simp only [evalReal] at *
  by_cases h : (l.negSlope : ℝ) ≤ r.negSlope
  · nlinarith [mul_nonneg (sub_nonneg.mpr h) (sub_nonneg.mpr hsb)]
  · have h' : (r.negSlope : ℝ) ≤ l.negSlope := le_of_not_ge h
    nlinarith [mul_nonneg (sub_nonneg.mpr h') (sub_nonneg.mpr has)]

/-- A certificate specifies rational knots and an input line on each interval. -/
structure RationalEnvelopeCertificate (n k : ℕ) where
  knots : Fin (k + 1) → ℚ
  active : Fin k → Fin n

/-- All conditions are finite rational comparisons, so the predicate is executable. -/
def RationalEnvelopeCertificate.Valid {n k : ℕ}
    (c : RationalEnvelopeCertificate n k) (lines : Fin n → RationalLine) (a b : ℚ) : Prop :=
  c.knots 0 = a ∧ c.knots (Fin.last k) = b ∧
  ∀ i : Fin k, c.knots i.castSucc ≤ c.knots i.succ ∧
    ∀ j : Fin n,
      (lines j).eval (c.knots i.castSucc) ≤ (lines (c.active i)).eval (c.knots i.castSucc) ∧
      (lines j).eval (c.knots i.succ) ≤ (lines (c.active i)).eval (c.knots i.succ)

instance {n k : ℕ} (c : RationalEnvelopeCertificate n k)
    (lines : Fin n → RationalLine) (a b : ℚ) : Decidable (c.Valid lines a b) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ ∀ _i : Fin k, _ ∧ ∀ _j : Fin n, _ ∧ _))

/-- A checked certificate proves dominance over every input line at every real point. -/
theorem RationalEnvelopeCertificate.active_dominates {n k : ℕ}
    {c : RationalEnvelopeCertificate n k} {lines : Fin n → RationalLine} {a b : ℚ}
    (hc : c.Valid lines a b) (i : Fin k) (j : Fin n) {s : ℝ}
    (hl : (c.knots i.castSucc : ℝ) ≤ s) (hr : s ≤ (c.knots i.succ : ℝ)) :
    (lines j).evalReal s ≤ (lines (c.active i)).evalReal s :=
  RationalLine.le_on_interval ((hc.2.2 i).2 j).1 ((hc.2.2 i).2 j).2 hl hr

/-- The original finite family, evaluated with rational arithmetic. -/
def rationalLines {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) (i : Fin (2 * n + 2)) :
    RationalLine :=
  if h : i.val < n then ⟨w ⟨i.val, h⟩, q ⟨i.val, h⟩⟩
  else if h' : i.val < 2 * n then
    ⟨m - w ⟨i.val - n, by omega⟩, 1 - q ⟨i.val - n, by omega⟩⟩
  else if i.val = 2 * n then ⟨0, 0⟩ else ⟨m, 1⟩

@[simp] theorem rationalLines_evalReal {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    (i : Fin (2 * n + 2)) (s : ℝ) :
    (rationalLines m q w i).evalReal s =
      line (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) i s := by
  unfold rationalLines line
  split_ifs <;> simp [RationalLine.evalReal]

/-- The certified active line equals the real upper envelope, including breakpoints. -/
theorem RationalEnvelopeCertificate.active_eq_envelope {n k : ℕ}
    {c : RationalEnvelopeCertificate (2 * n + 2) k} {m a b : ℚ} {q w : Fin n → ℚ}
    (hc : c.Valid (rationalLines m q w) a b) (i : Fin k) {s : ℝ}
    (hl : (c.knots i.castSucc : ℝ) ≤ s) (hr : s ≤ (c.knots i.succ : ℝ)) :
    (rationalLines m q w (c.active i)).evalReal s =
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) s := by
  symm
  apply (Finset.max'_eq_iff _ _ _).mpr
  constructor
  · exact Finset.mem_image.mpr ⟨c.active i, Finset.mem_univ _, (rationalLines_evalReal ..).symm⟩
  · intro v hv
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hv
    rw [← rationalLines_evalReal]
    exact RationalEnvelopeCertificate.active_dominates hc i j hl hr

/-- A certificate produces the claimed lower reciprocal moment using only rational operations. -/
def RationalEnvelopeCertificate.value {n k : ℕ}
    (c : RationalEnvelopeCertificate (2 * n + 2) k) (m a : ℚ) (q w : Fin n → ℚ) : ℚ :=
  1 / a - (m - a) / a ^ 2 + ∑ i,
    rationalSegmentIntegral (rationalLines m q w (c.active i))
      (c.knots i.castSucc) (c.knots i.succ)

/-- Exact certified integration on a single interval. -/
theorem RationalEnvelopeCertificate.segment_integral {n k : ℕ}
    {c : RationalEnvelopeCertificate (2 * n + 2) k} {m a b : ℚ} {q w : Fin n → ℚ}
    (hc : c.Valid (rationalLines m q w) a b) (i : Fin k)
    (hi : 0 < c.knots i.castSucc) :
    (∫ s in (c.knots i.castSucc : ℝ)..(c.knots i.succ : ℝ),
      2 * envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) s / s ^ 3) =
      (rationalSegmentIntegral (rationalLines m q w (c.active i))
        (c.knots i.castSucc) (c.knots i.succ) : ℝ) := by
  rw [cast_rationalSegmentIntegral]
  have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by exact_mod_cast (hc.2.2 i).1
  rw [← affine_call_integral (by exact_mod_cast hi) ho]
  apply intervalIntegral.integral_congr
  intro s hs
  rw [uIcc_of_le ho] at hs
  dsimp only
  rw [← RationalEnvelopeCertificate.active_eq_envelope hc i hs.1 hs.2]
  rfl

/-- Finite-partition telescoping, with no assumption that intervals have positive length. -/
theorem sum_integral_fin_partition {k : ℕ} {f : ℝ → ℝ} (x : Fin (k + 1) → ℝ)
    (hi : ∀ i : Fin k, IntervalIntegrable f volume (x i.castSucc) (x i.succ)) :
    (∑ i : Fin k, ∫ s in x i.castSucc..x i.succ, f s) =
      ∫ s in x 0..x (Fin.last k), f s := by
  let a : ℕ → ℝ := fun j => x ⟨min j k, by omega⟩
  have ha (i : Fin (k + 1)) : a i.val = x i := by
    dsimp [a]
    congr 1
    ext
    exact Nat.min_eq_left (by omega)
  have hsum := intervalIntegral.sum_integral_adjacent_intervals
    (a := a) (n := k) (f := f) (μ := volume)
    (fun j hj => by
      have h := hi ⟨j, hj⟩
      rw [← ha (Fin.castSucc ⟨j, hj⟩), ← ha (Fin.succ ⟨j, hj⟩)] at h
      exact h)
  rw [← Fin.sum_univ_eq_sum_range] at hsum
  simpa only [← ha, Fin.val_castSucc, Fin.val_succ, Fin.val_zero, Fin.val_last] using hsum

theorem RationalEnvelopeCertificate.monotone {n k : ℕ}
    {c : RationalEnvelopeCertificate n k} {lines : Fin n → RationalLine} {a b : ℚ}
    (hc : c.Valid lines a b) : Monotone c.knots :=
  Fin.monotone_iff_le_succ.mpr (fun i => (hc.2.2 i).1)

theorem RationalEnvelopeCertificate.positive_knots {n k : ℕ}
    {c : RationalEnvelopeCertificate n k} {lines : Fin n → RationalLine} {a b : ℚ}
    (hc : c.Valid lines a b) (ha : 0 < a) (i : Fin (k + 1)) : 0 < c.knots i := by
  have h := RationalEnvelopeCertificate.monotone hc (Fin.zero_le i)
  rw [hc.1] at h
  exact ha.trans_le h

theorem RationalEnvelopeCertificate.segment_integrable {n k : ℕ}
    {c : RationalEnvelopeCertificate (2 * n + 2) k} {m a b : ℚ} {q w : Fin n → ℚ}
    (hc : c.Valid (rationalLines m q w) a b) (ha : 0 < a) (i : Fin k) :
    IntervalIntegrable
      (fun s : ℝ => 2 * envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) s / s ^ 3)
      volume (c.knots i.castSucc) (c.knots i.succ) := by
  have ho : (c.knots i.castSucc : ℝ) ≤ c.knots i.succ := by exact_mod_cast (hc.2.2 i).1
  have hp : 0 < (c.knots i.castSucc : ℝ) := by
    exact_mod_cast RationalEnvelopeCertificate.positive_knots hc ha i.castSucc
  have hcont : ContinuousOn (fun s : ℝ =>
      2 * (rationalLines m q w (c.active i)).evalReal s / s ^ 3)
      (Icc (c.knots i.castSucc : ℝ) (c.knots i.succ : ℝ)) := by
    unfold RationalLine.evalReal
    fun_prop (disch := intro s hs; exact pow_ne_zero 3 (ne_of_gt (hp.trans_le hs.1)))
  have hcont' : ContinuousOn
      (fun s : ℝ => 2 * envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) s / s ^ 3)
      (Icc (c.knots i.castSucc : ℝ) (c.knots i.succ : ℝ)) := by
    apply hcont.congr
    intro s hs
    dsimp only
    rw [RationalEnvelopeCertificate.active_eq_envelope hc i hs.1 hs.2]
  apply ContinuousOn.intervalIntegrable
  simpa only [uIcc_of_le ho] using hcont'

/-- Verified rational evaluation agrees with the continuous-support formula exactly. -/
theorem RationalEnvelopeCertificate.value_eq_lowerMoment {n k : ℕ}
    {c : RationalEnvelopeCertificate (2 * n + 2) k} {m a b : ℚ} {q w : Fin n → ℚ}
    (hc : c.Valid (rationalLines m q w) a b) (ha : 0 < a) :
    (c.value m a q w : ℝ) =
      lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
  unfold value lowerMoment
  push_cast
  congr 1
  have hsum := sum_integral_fin_partition (fun i => (c.knots i : ℝ))
    (RationalEnvelopeCertificate.segment_integrable hc ha)
  rw [hc.1, hc.2.1] at hsum
  rw [← hsum]
  apply Finset.sum_congr rfl
  intro i _
  exact (RationalEnvelopeCertificate.segment_integral hc i
    (RationalEnvelopeCertificate.positive_knots hc ha i.castSucc)).symm

end ReciprocalAnchor.ManyLeaf



