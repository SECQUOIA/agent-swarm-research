import Mathlib.Data.Rat.Defs
import Mathlib.Data.List.Sort
import Mathlib.Tactic

/-! Rational line-envelope stack: exact envelope preservation and amortized cost. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

structure Line where
  slope : ℚ
  intercept : ℚ
  deriving DecidableEq, Repr

def Line.eval (l : Line) (x : ℚ) : ℚ := l.intercept + l.slope * x

/-- The middle coefficient point lies below the chord of the outer points. -/
def Redundant (a b c : Line) : Prop :=
  a.slope ≤ b.slope ∧ b.slope ≤ c.slope ∧ a.slope < c.slope ∧
  b.intercept * (c.slope - a.slope) ≤
    a.intercept * (c.slope - b.slope) + c.intercept * (b.slope - a.slope)

instance (a b c : Line) : Decidable (Redundant a b c) := by
  unfold Redundant
  infer_instance

theorem redundant_eval {a b c : Line} (h : Redundant a b c) (x : ℚ) :
    b.eval x ≤ max (a.eval x) (c.eval x) := by
  rcases h with ⟨hab, hbc, hac, h⟩
  have chord : b.eval x * (c.slope - a.slope) ≤
      a.eval x * (c.slope - b.slope) + c.eval x * (b.slope - a.slope) := by
    dsimp [Line.eval]
    nlinarith [h]
  have ha := le_max_left (a.eval x) (c.eval x)
  have hc := le_max_right (a.eval x) (c.eval x)
  have h1 := mul_le_mul_of_nonneg_right ha (sub_nonneg.mpr hbc)
  have h2 := mul_le_mul_of_nonneg_right hc (sub_nonneg.mpr hab)
  nlinarith

/-- Include the zero baseline, as in the reciprocal-anchor envelope. -/
def value : List Line → ℚ → ℚ
  | [], _ => 0
  | l :: ls, x => max (l.eval x) (value ls x)

/-- Push a slope-ordered line; each recursive call deletes one stack line.
The count is the number of tested stack positions, including the final position. -/
def push (c : Line) : List Line → List Line × ℕ
  | b :: a :: rest =>
      if Redundant a b c then
        let r := push c (a :: rest)
        (r.1, r.2 + 1)
      else (c :: b :: a :: rest, 1)
  | stack => (c :: stack, 1)
termination_by stack => stack.length

theorem push_value (c : Line) (stack : List Line) (x : ℚ) :
    value (push c stack).1 x = max (c.eval x) (value stack x) := by
  induction stack using push.induct c with
  | case1 b a rest h ih =>
      rw [push, if_pos h]
      simp only
      rw [ih]
      simp only [value]
      have hb := redundant_eval h x
      apply le_antisymm
      · exact max_le (le_max_left _ _) (max_le
          (le_trans (le_max_left _ _) (le_trans (le_max_right _ _) (le_max_right _ _)))
          (le_trans (le_max_right _ _) (le_trans (le_max_right _ _) (le_max_right _ _))))
      · apply max_le (le_max_left _ _)
        apply max_le
        · exact le_trans hb (max_le (le_trans (le_max_left _ _) (le_max_right _ _))
            (le_max_left _ _))
        · exact le_max_right _ _
  | case2 b a rest h => simp [push, h, value]
  | case3 stack h =>
      cases stack with
      | nil => simp [push, value]
      | cons b rest =>
          cases rest with
          | nil => simp [push, value]
          | cons a rest => exact False.elim (h b a rest rfl)

/-- Potential accounting: every extra test consumes one previously stored line. -/
theorem push_cost (c : Line) (stack : List Line) :
    (push c stack).2 + (push c stack).1.length = stack.length + 2 := by
  induction stack using push.induct c with
  | case1 b a rest h ih => simp only [push, if_pos h]; simp only [List.length_cons] at *; omega
  | case2 b a rest h => simp [push, h]; omega
  | case3 stack h =>
      cases stack with
      | nil => simp [push]
      | cons b rest =>
          cases rest with
          | nil => simp [push]
          | cons a rest => exact False.elim (h b a rest rfl)

def scan : List Line → List Line → List Line × ℕ
  | [], stack => (stack, 0)
  | c :: cs, stack =>
      let p := push c stack
      let r := scan cs p.1
      (r.1, p.2 + r.2)

theorem scan_cost (input stack : List Line) :
    (scan input stack).2 + (scan input stack).1.length =
      2 * input.length + stack.length := by
  induction input generalizing stack with
  | nil => simp [scan]
  | cons c cs ih =>
      simp only [scan, List.length_cons]
      have h := push_cost c stack
      have hi := ih (push c stack).1
      omega

theorem scan_cost_le (input : List Line) : (scan input []).2 ≤ 2 * input.length := by
  have h := scan_cost input []
  simp only [List.length_nil, Nat.add_zero] at h
  omega

theorem value_nonneg (ls : List Line) (x : ℚ) : 0 ≤ value ls x := by
  induction ls with
  | nil => rfl
  | cons a as ih => exact le_trans ih (le_max_right _ _)

theorem scan_value (input stack : List Line) (x : ℚ) :
    value (scan input stack).1 x = max (value input x) (value stack x) := by
  induction input generalizing stack with
  | nil =>
      simp only [scan, value]
      exact (max_eq_right (value_nonneg stack x)).symm
  | cons c cs ih =>
      simp only [scan]
      rw [ih, push_value]
      simp only [value]
      simp only [max_assoc, max_left_comm]

/-- The real interpretation used in the continuous integral formula. -/
def Line.evalReal (l : Line) (x : ℝ) : ℝ := l.intercept + (l.slope : ℝ) * x

theorem redundant_evalReal {a b c : Line} (h : Redundant a b c) (x : ℝ) :
    b.evalReal x ≤ max (a.evalReal x) (c.evalReal x) := by
  rcases h with ⟨hab, hbc, hac, h⟩
  have hab' : (a.slope : ℝ) ≤ b.slope := by exact_mod_cast hab
  have hbc' : (b.slope : ℝ) ≤ c.slope := by exact_mod_cast hbc
  have hac' : (a.slope : ℝ) < c.slope := by exact_mod_cast hac
  have h' : (b.intercept : ℝ) * (c.slope - a.slope) ≤
      (a.intercept : ℝ) * (c.slope - b.slope) +
        (c.intercept : ℝ) * (b.slope - a.slope) := by exact_mod_cast h
  have chord : b.evalReal x * (c.slope - a.slope) ≤
      a.evalReal x * (c.slope - b.slope) +
        c.evalReal x * (b.slope - a.slope) := by
    dsimp [Line.evalReal]
    nlinarith [h']
  have ha := le_max_left (a.evalReal x) (c.evalReal x)
  have hc := le_max_right (a.evalReal x) (c.evalReal x)
  have h1 := mul_le_mul_of_nonneg_right ha (sub_nonneg.mpr hbc')
  have h2 := mul_le_mul_of_nonneg_right hc (sub_nonneg.mpr hab')
  nlinarith

def valueReal : List Line → ℝ → ℝ
  | [], _ => 0
  | l :: ls, x => max (l.evalReal x) (valueReal ls x)

theorem push_valueReal (c : Line) (stack : List Line) (x : ℝ) :
    valueReal (push c stack).1 x = max (c.evalReal x) (valueReal stack x) := by
  induction stack using push.induct c with
  | case1 b a rest h ih =>
      rw [push, if_pos h]
      simp only
      rw [ih]
      simp only [valueReal]
      have hb := redundant_evalReal h x
      apply le_antisymm
      · exact max_le (le_max_left _ _) (max_le
          (le_trans (le_max_left _ _) (le_trans (le_max_right _ _) (le_max_right _ _)))
          (le_trans (le_max_right _ _) (le_trans (le_max_right _ _) (le_max_right _ _))))
      · apply max_le (le_max_left _ _)
        apply max_le
        · exact le_trans hb (max_le (le_trans (le_max_left _ _) (le_max_right _ _))
            (le_max_left _ _))
        · exact le_max_right _ _
  | case2 b a rest h => simp [push, h, valueReal]
  | case3 stack h =>
      cases stack with
      | nil => simp [push, valueReal]
      | cons b rest =>
          cases rest with
          | nil => simp [push, valueReal]
          | cons a rest => exact False.elim (h b a rest rfl)

theorem valueReal_nonneg (ls : List Line) (x : ℝ) : 0 ≤ valueReal ls x := by
  induction ls with
  | nil => rfl
  | cons a as ih => exact le_trans ih (le_max_right _ _)

theorem scan_valueReal (input stack : List Line) (x : ℝ) :
    valueReal (scan input stack).1 x = max (valueReal input x) (valueReal stack x) := by
  induction input generalizing stack with
  | nil =>
      simp only [scan, valueReal]
      exact (max_eq_right (valueReal_nonneg stack x)).symm
  | cons c cs ih =>
      simp only [scan]
      rw [ih, push_valueReal]
      simp only [valueReal, max_assoc, max_left_comm]

theorem valueReal_perm {ls ks : List Line} (h : ls.Perm ks) (x : ℝ) :
    valueReal ls x = valueReal ks x := by
  induction h with
  | nil => rfl
  | cons a h ih => simp only [valueReal, ih]
  | swap a b tail => simp only [valueReal, max_left_comm]
  | trans h1 h2 ih1 ih2 => exact ih1.trans ih2

end ReciprocalAnchor.ManyLeaf.FastEnvelope
