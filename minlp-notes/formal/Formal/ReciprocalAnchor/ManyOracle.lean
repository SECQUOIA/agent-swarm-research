import Formal.ReciprocalAnchor.ManyLinearSeparation
import Formal.ReciprocalAnchor.ManyFastSeparation

/-! A total executable rational oracle returns either membership or a separating affine cut. -/
namespace ReciprocalAnchor.ManyLeaf

/-- Convert a lower bound on the reciprocal coordinate into the convention `eval ≤ 0`. -/
def lowerMomentCut {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : RationalAffineCut n :=
  let F := FastEnvelope.fastCut a b m q w
  ⟨F.1, F.2.1, -1, F.2.2.1, F.2.2.2⟩

theorem lowerMomentCut_evalReal {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ)
    (m' t' : ℝ) (q' w' : Fin n → ℝ) :
    (lowerMomentCut a b m q w).evalReal m' t' q' w' =
      (FastEnvelope.fastCut a b m q w).eval m' q' w' - t' := by
  simp only [lowerMomentCut, RationalAffineCut.evalReal, RationalAffineForm.eval,
    Rat.cast_neg, Rat.cast_one, neg_one_mul]
  ring

/-- The finite affine scan is followed by the exact rational lower-moment test. -/
def separationOracle {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    Option (RationalAffineCut n) :=
  match findLinearViolation a b m t q w with
  | some C => some C
  | none => if FastEnvelope.fastLowerMoment a b m q w ≤ t then none
      else some (lowerMomentCut a b m q w)

theorem separationOracle_none_iff {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b) :
    separationOracle a b m t q w = none ↔
      point (m : ℝ) t (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∈ hull n a b := by
  rw [← rationalMembership_correct ha hab]
  unfold rationalMembership
  simp only [decide_eq_true_eq]
  unfold separationOracle
  cases he : findLinearViolation a b m t q w with
  | none =>
    obtain ⟨hl, hu⟩ := (findLinearViolation_none ha hab m t q w).mp he
    simp [hl, hu]
  | some C =>
    have hn : ¬ (rationalLinearBounds a b m q w ∧ t ≤ (a + b - m) / (a * b)) := by
      intro h
      have := (findLinearViolation_none ha hab m t q w).mpr h
      rw [he] at this
      contradiction
    simp only [Option.some_ne_none, false_iff, not_and]
    intro hl ht hu
    exact hn ⟨hl, hu⟩

theorem separationOracle_some_sound {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b) {C : RationalAffineCut n}
    (h : separationOracle a b m t q w = some C) :
    0 < C.eval m t q w ∧ ∀ (m' t' : ℝ) (q' w' : Fin n → ℝ),
      point m' t' q' w' ∈ hull n a b → C.evalReal m' t' q' w' ≤ 0 := by
  unfold separationOracle at h
  cases he : findLinearViolation a b m t q w with
  | some D =>
    simp only [he] at h
    cases Option.some.inj h
    exact findLinearViolation_sound ha hab he
  | none =>
    simp only [he] at h
    by_cases ht : FastEnvelope.fastLowerMoment a b m q w ≤ t
    · simp [ht] at h
    · simp only [ht, if_false] at h
      cases Option.some.inj h
      constructor
      · have hex := FastEnvelope.fastCut_exact (m := m) (q := q) (w := w) ha hab.le
        have hr : (0 : ℝ) <
            (lowerMomentCut a b m q w).evalReal m t (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
          rw [lowerMomentCut_evalReal, hex]
          exact sub_pos.mpr (by exact_mod_cast lt_of_not_ge ht)
        rw [← RationalAffineCut.eval_cast] at hr
        exact_mod_cast hr
      · intro m' t' q' w' hm
        rw [lowerMomentCut_evalReal]
        have hv := FastEnvelope.fastCut_valid (m := m) (q := q) (w := w) ha hab.le m' q' w'
        have hh := (mem_hull_iff_bounds (by exact_mod_cast ha) (by exact_mod_cast hab)).mp hm
        linarith [hh.2.1]

/-- Every rejected input receives an actual cut from the executable producer. -/
theorem separationOracle_complete {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b)
    (h : point (m : ℝ) t (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∉ hull n a b) :
    ∃ C, separationOracle a b m t q w = some C ∧ 0 < C.eval m t q w ∧
      ∀ (m' t' : ℝ) (q' w' : Fin n → ℝ), point m' t' q' w' ∈ hull n a b →
        C.evalReal m' t' q' w' ≤ 0 := by
  cases he : separationOracle a b m t q w with
  | none => exact False.elim (h ((separationOracle_none_iff ha hab).mp he))
  | some C => exact ⟨C, rfl, separationOracle_some_sound ha hab he⟩

/-- Number of affine tests actually visited by the finite scan. -/
def linearScanVisits {n : ℕ} (m t : ℚ) (q w : Fin n → ℚ) :
    List (RationalAffineCut n) → ℕ
  | [] => 0
  | C :: rest => if 0 < C.eval m t q w then 1 else 1 + linearScanVisits m t q w rest

theorem linearScanVisits_le {n : ℕ} (m t : ℚ) (q w : Fin n → ℚ)
    (cuts : List (RationalAffineCut n)) : linearScanVisits m t q w cuts ≤ cuts.length := by
  induction cuts with
  | nil => simp [linearScanVisits]
  | cons C rest ih =>
    simp only [linearScanVisits, List.length_cons]
    split_ifs <;> omega

theorem linearCuts_length {n : ℕ} (a b : ℚ) :
    (linearCuts (n := n) a b).length = 6 * n + 3 := by
  simp [linearCuts, List.length_flatten, List.map_ofFn, Function.comp_def, leafCuts,
    List.ofFn_const, Nat.mul_comm, Nat.add_comm]
  omega

/-- A rational-operation charge for dense cut evaluation and comparison, including
materializing the affine input coefficients. Each tested cut uses two length-`n`
dot products and a constant number of scalar operations. -/
def linearScanArithmeticCharge {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) : ℕ :=
  (4 * n + 7) * linearScanVisits m t q w (linearCuts a b) + 10 * (n + 1)

theorem linearScanArithmeticCharge_le {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    linearScanArithmeticCharge a b m t q w ≤ (4 * n + 7) * (6 * n + 3) + 10 * (n + 1) := by
  have hv := linearScanVisits_le m t q w (linearCuts a b)
  rw [linearCuts_length] at hv
  exact Nat.add_le_add_right (Nat.mul_le_mul_left (4 * n + 7) hv) _

/-- Envelope construction plus segment integration, tangent evaluation, and
construction of the input lines, charged in exact rational operations. -/
def lowerEvaluationCharge {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) : ℕ :=
  (FastEnvelope.buildSegments (FastEnvelope.sourceLines m q w) a b).2 +
    40 * ((FastEnvelope.buildSegments (FastEnvelope.sourceLines m q w) a b).1.length + 1) +
      10 * (2 * n + 2)

theorem lowerEvaluationCharge_le {n : ℕ} (a b m : ℚ) (q w : Fin n → ℚ) :
    lowerEvaluationCharge a b m q w ≤
      (2 * n + 2) * ((2 * n + 2).log2 + 37) + 40 * (2 * n + 3) + 10 * (2 * n + 2) := by
  have hc := FastEnvelope.buildSegments_cost (FastEnvelope.sourceLines m q w) a b
  have hl := FastEnvelope.buildSegments_length (FastEnvelope.sourceLines m q w) a b
  simp only [FastEnvelope.sourceLines, List.length_ofFn] at hc hl
  unfold lowerEvaluationCharge FastEnvelope.sourceLines
  omega

/-- A charge that follows the actual dispatch, including the second envelope
construction when extracting a lower-moment cut. Bit costs are separate. -/
def separationOracleArithmeticCharge {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) : ℕ :=
  linearScanArithmeticCharge a b m t q w +
    match findLinearViolation a b m t q w with
    | some _ => 0
    | none => lowerEvaluationCharge a b m q w +
        if FastEnvelope.fastLowerMoment a b m q w ≤ t then 0
        else FastEnvelope.fastCutArithmeticCharge a b m q w

/-- The complete dispatch and coefficient producer have polynomial arithmetic charge. -/
theorem separationOracleArithmeticCharge_le {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    separationOracleArithmeticCharge a b m t q w ≤
      (4 * n + 7) * (6 * n + 3) + 10 * (n + 1) +
      ((2 * n + 2) * ((2 * n + 2).log2 + 37) + 40 * (2 * n + 3) + 10 * (2 * n + 2)) +
      ((2 * n + 2) * ((2 * n + 2).log2 + 37) + 8 * (2 * n + 2) ^ 2 +
        100 * (n + 1) * (2 * n + 3)) := by
  have hs := linearScanArithmeticCharge_le a b m t q w
  have he := lowerEvaluationCharge_le a b m q w
  have hc := FastEnvelope.fastCutArithmeticCharge_le a b m q w
  unfold separationOracleArithmeticCharge
  split
  · omega
  · split_ifs
    · simp only [Nat.add_zero]
      exact (Nat.add_le_add hs he).trans (Nat.le_add_right _ _)
    · simpa only [Nat.add_assoc] using Nat.add_le_add hs (Nat.add_le_add he hc)

end ReciprocalAnchor.ManyLeaf
