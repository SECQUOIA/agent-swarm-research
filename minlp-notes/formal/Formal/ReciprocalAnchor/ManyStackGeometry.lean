import Formal.ReciprocalAnchor.ManyFastEnvelope

namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- Stack order is decreasing slope, with increasing intersections in the reverse order. -/
def Good : List Line → Prop
  | [] => True
  | [_] => True
  | [b, a] => a.slope < b.slope
  | c :: b :: a :: rest =>
      b.slope < c.slope ∧ ¬ Redundant a b c ∧ Good (b :: a :: rest)

theorem good_tail (b : Line) (rest : List Line) (h : Good (b :: rest)) : Good rest := by
  cases rest with
  | nil => trivial
  | cons a tail =>
    cases tail with
    | nil => trivial
    | cons d tail => exact h.2.2

theorem push_mem (c : Line) (stack : List Line) {l : Line} (h : l ∈ (push c stack).1) :
    l = c ∨ l ∈ stack := by
  induction stack using push.induct c with
  | case1 b a rest hr ih =>
    rw [push, if_pos hr] at h
    rcases ih h with hc | ht
    · exact Or.inl hc
    · exact Or.inr (List.mem_cons_of_mem _ ht)
  | case2 b a rest hr => simpa [push, hr] using h
  | case3 stack hr =>
    cases stack with
    | nil => simpa [push] using h
    | cons b rest =>
      cases rest with
      | nil => simpa [push] using h
      | cons a rest => exact False.elim (hr b a rest rfl)

theorem push_good (c : Line) (stack : List Line) (hg : Good stack)
    (hc : ∀ l ∈ stack, l.slope < c.slope) : Good (push c stack).1 := by
  induction stack using push.induct c with
  | case1 b a rest hr ih =>
    rw [push, if_pos hr]
    exact ih (good_tail b _ hg) (fun l hl => hc l (List.mem_cons_of_mem _ hl))
  | case2 b a rest hr =>
    rw [push, if_neg hr]
    exact ⟨hc b (by simp), hr, hg⟩
  | case3 stack hr =>
    cases stack with
    | nil => simp [push, Good]
    | cons b rest =>
      cases rest with
      | nil => simpa [push, Good] using hc b (by simp)
      | cons a rest => exact False.elim (hr b a rest rfl)

theorem scan_good (input stack : List Line)
    (hi : input.Pairwise (fun a b => a.slope < b.slope)) (hg : Good stack)
    (hb : ∀ a ∈ stack, ∀ b ∈ input, a.slope < b.slope) :
    Good (scan input stack).1 := by
  induction input generalizing stack with
  | nil => exact hg
  | cons c cs ih =>
    simp only [scan]
    obtain ⟨hc, hcs⟩ := List.pairwise_cons.mp hi
    apply ih _ hcs (push_good c stack hg (fun a ha => hb a ha c (by simp)))
    intro a ha b hbm
    rcases push_mem c stack ha with he | hm
    · subst a; exact hc b hbm
    · exact hb a hm b (List.mem_cons_of_mem _ hbm)

def cross (a b : Line) : ℚ := (a.intercept - b.intercept) / (b.slope - a.slope)

theorem cross_order {a b c : Line} (hab : a.slope < b.slope)
    (hbc : b.slope < c.slope) :
    Redundant a b c ↔ cross b c ≤ cross a b := by
  have hab' : 0 < b.slope - a.slope := sub_pos.mpr hab
  have hbc' : 0 < c.slope - b.slope := sub_pos.mpr hbc
  rw [cross, cross, div_le_div_iff₀ hbc' hab']
  constructor
  · intro h; rcases h with ⟨_, _, _, h⟩; nlinarith
  · intro h; refine ⟨hab.le, hbc.le, hab.trans hbc, ?_⟩; nlinarith

theorem good_pair_slope {b a : Line} {rest : List Line} (h : Good (b :: a :: rest)) :
    a.slope < b.slope := by
  cases rest with
  | nil => exact h
  | cons d tail => exact h.1

theorem good_cross {c b a : Line} {rest : List Line} (h : Good (c :: b :: a :: rest)) :
    cross a b < cross b c := by
  exact lt_of_not_ge ((cross_order (good_pair_slope h.2.2) h.1).not.mp h.2.1)

theorem eval_le_iff {a b : Line} (hab : a.slope < b.slope) (x : ℚ) :
    a.eval x ≤ b.eval x ↔ cross a b ≤ x := by
  rw [cross, div_le_iff₀ (sub_pos.mpr hab)]
  dsimp [Line.eval]
  constructor <;> intro h <;> nlinarith

theorem eval_le_iff_real {a b : Line} (hab : a.slope < b.slope) (x : ℝ) :
    a.evalReal x ≤ b.evalReal x ↔ (cross a b : ℝ) ≤ x := by
  have hd : 0 < (b.slope : ℝ) - a.slope := by exact_mod_cast sub_pos.mpr hab
  simp only [cross, Rat.cast_div, Rat.cast_sub]
  rw [div_le_iff₀ hd]
  dsimp [Line.evalReal]
  constructor <;> intro h <;> nlinarith

/-- To the right of its last intersection the head dominates every retained line. -/
theorem head_dominates {b a : Line} {rest : List Line} (h : Good (b :: a :: rest))
    (x : ℝ) (hx : (cross a b : ℝ) ≤ x) :
    ∀ l ∈ a :: rest, l.evalReal x ≤ b.evalReal x := by
  induction rest generalizing b a with
  | nil =>
    intro l hl
    simp only [List.mem_singleton] at hl
    subst l
    exact (eval_le_iff_real h x).2 hx
  | cons d tail ih =>
    have hab := (eval_le_iff_real h.1 x).2 hx
    have hda : (cross d a : ℝ) ≤ x := by
      have ho : (cross d a : ℝ) < cross a b := by exact_mod_cast good_cross h
      exact ho.le.trans hx
    intro l hl
    rcases List.mem_cons.mp hl with hl | hl
    · subst l; exact hab
    · exact (ih h.2.2 hda l hl).trans hab

end ReciprocalAnchor.ManyLeaf.FastEnvelope
