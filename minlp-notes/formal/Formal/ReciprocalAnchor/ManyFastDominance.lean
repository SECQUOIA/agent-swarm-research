import Formal.ReciprocalAnchor.ManyFastConstruction
import Formal.ReciprocalAnchor.ManyFastSegments

/-! Pointwise domination by retained lines, without an artificial zero baseline. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

def Dominates (xs ys : List Line) (x : ℝ) : Prop :=
  ∀ l ∈ xs, ∃ k ∈ ys, l.evalReal x ≤ k.evalReal x

theorem Dominates.refl (ls : List Line) (x : ℝ) : Dominates ls ls x :=
  fun l hl => ⟨l, hl, le_rfl⟩

theorem Dominates.trans {as bs cs : List Line} {x : ℝ}
    (h : Dominates as bs x) (h' : Dominates bs cs x) : Dominates as cs x := by
  intro l hl
  obtain ⟨k, hk, hlk⟩ := h l hl
  obtain ⟨j, hj, hkj⟩ := h' k hk
  exact ⟨j, hj, hlk.trans hkj⟩

theorem Dominates.cons {as bs : List Line} {x : ℝ}
    (h : Dominates as bs x) (a : Line) : Dominates (a :: as) (a :: bs) x := by
  intro l hl
  rcases List.mem_cons.mp hl with he | hl
  · subst l
    exact ⟨a, List.mem_cons_self, le_rfl⟩
  · obtain ⟨k, hk, hle⟩ := h l hl
    exact ⟨k, List.mem_cons_of_mem _ hk, hle⟩

theorem dominates_drop_head {a b : Line} (bs : List Line) (x : ℝ)
    (h : a.evalReal x ≤ b.evalReal x) : Dominates (a :: b :: bs) (b :: bs) x := by
  intro l hl
  rcases List.mem_cons.mp hl with he | hl
  · subst l
    exact ⟨b, List.mem_cons_self, h⟩
  · exact ⟨l, hl, le_rfl⟩

theorem dominates_drop_second {a b : Line} (bs : List Line) (x : ℝ)
    (h : b.evalReal x ≤ a.evalReal x) : Dominates (a :: b :: bs) (a :: bs) x := by
  intro l hl
  rcases List.mem_cons.mp hl with he | hl
  · subst l
    exact ⟨a, List.mem_cons_self, le_rfl⟩
  · rcases List.mem_cons.mp hl with he | hl
    · subst l
      exact ⟨a, List.mem_cons_self, h⟩
    · exact ⟨l, List.mem_cons_of_mem _ hl, le_rfl⟩

theorem parallelDedup_dominates (ls : List Line) (x : ℝ) :
    Dominates ls (parallelDedup ls).1 x := by
  induction ls with
  | nil => exact Dominates.refl [] x
  | cons a as ih =>
    apply (ih.cons a).trans
    simp only [parallelDedup]
    split <;> rename_i he
    · rw [he]
      exact Dominates.refl _ _
    · rename_i b bs
      rw [he]
      have hreal {l k : Line} (hs : l.slope = k.slope)
          (hi : l.intercept ≤ k.intercept) : l.evalReal x ≤ k.evalReal x := by
        have hs' : (l.slope : ℝ) = k.slope := by exact_mod_cast hs
        have hi' : (l.intercept : ℝ) ≤ k.intercept := by exact_mod_cast hi
        dsimp [Line.evalReal]
        rw [hs']
        linarith
      split <;> rename_i hs
      · split <;> rename_i hi
        · exact dominates_drop_head bs x (hreal hs hi)
        · exact dominates_drop_second bs x (hreal hs.symm (le_of_not_ge hi))
      · exact Dominates.refl _ _

theorem push_dominates (c : Line) (stack : List Line) (x : ℝ) :
    Dominates (c :: stack) (push c stack).1 x := by
  induction stack using push.induct c with
  | case1 b a rest hr ih =>
    rw [push, if_pos hr]
    apply Dominates.trans (bs := c :: a :: rest) ?_ ih
    intro l hl
    rcases List.mem_cons.mp hl with he | hl
    · subst l
      exact ⟨c, by simp, le_rfl⟩
    · rcases List.mem_cons.mp hl with he | hl
      · subst l
        have hb := redundant_evalReal hr x
        by_cases hac : a.evalReal x ≤ c.evalReal x
        · exact ⟨c, by simp, by simpa [max_eq_right hac] using hb⟩
        · exact ⟨a, by simp, by simpa [max_eq_left (le_of_not_ge hac)] using hb⟩
      · exact ⟨l, List.mem_cons_of_mem _ hl, le_rfl⟩
  | case2 b a rest hr =>
    rw [push, if_neg hr]
    exact Dominates.refl _ _
  | case3 stack hr =>
    cases stack with
    | nil => simpa [push] using Dominates.refl [c] x
    | cons b rest =>
      cases rest with
      | nil => simpa [push] using Dominates.refl [c, b] x
      | cons a rest => exact False.elim (hr b a rest rfl)

theorem scan_dominates (input stack : List Line) (x : ℝ) :
    Dominates (input ++ stack) (scan input stack).1 x := by
  induction input generalizing stack with
  | nil => exact Dominates.refl _ _
  | cons c cs ih =>
    simp only [scan]
    apply Dominates.trans (bs := cs ++ (push c stack).1) ?_ (ih _)
    intro l hl
    have hp := push_dominates c stack x
    rcases List.mem_append.mp hl with hl | hl
    · rcases List.mem_cons.mp hl with he | hl
      · subst l
        obtain ⟨k, hk, he⟩ := hp c List.mem_cons_self
        exact ⟨k, List.mem_append_right _ hk, he⟩
      · exact ⟨l, List.mem_append_left _ hl, le_rfl⟩
    · obtain ⟨k, hk, he⟩ := hp l (List.mem_cons_of_mem _ hl)
      exact ⟨k, List.mem_append_right _ hk, he⟩

theorem buildStack_dominates (input : List Line) (x : ℝ) :
    Dominates input (buildStack input).1 x := by
  have hs : Dominates input (countedSort Line.slope input).1 x := by
    intro l hl
    exact ⟨l, (countedSort_spec Line.slope input).1.mem_iff.mpr hl, le_rfl⟩
  have hd := parallelDedup_dominates (countedSort Line.slope input).1 x
  have hc := scan_dominates (parallelDedup (countedSort Line.slope input).1).1 [] x
  simp only [List.append_nil] at hc
  exact (hs.trans hd).trans hc

theorem scan_members (input stack : List Line) {l : Line}
    (hl : l ∈ (scan input stack).1) : l ∈ input ∨ l ∈ stack := by
  induction input generalizing stack with
  | nil => exact Or.inr hl
  | cons c cs ih =>
    simp only [scan] at hl
    rcases ih _ hl with hc | hc
    · exact Or.inl (List.mem_cons_of_mem _ hc)
    · rcases push_mem c stack hc with he | hm
      · exact Or.inl (List.mem_cons.mpr (Or.inl he))
      · exact Or.inr hm

theorem buildStack_members (input : List Line) {l : Line}
    (hl : l ∈ (buildStack input).1) : l ∈ input := by
  have hm := scan_members (parallelDedup (countedSort Line.slope input).1).1 [] hl
  simp only [List.not_mem_nil, or_false] at hm
  have hd := (parallelDedup_members_cost (countedSort Line.slope input).1).1 l hm
  exact (countedSort_spec Line.slope input).1.mem_iff.mp hd

theorem buildStack_nonempty (input : List Line) (hi : input ≠ []) :
    (buildStack input).1 ≠ [] := by
  cases input with
  | nil => exact False.elim (hi rfl)
  | cons a as =>
    intro he
    obtain ⟨k, hk, _⟩ := buildStack_dominates (a :: as) 0 a List.mem_cons_self
    rw [he] at hk
    exact List.not_mem_nil hk

theorem built_segments_dominate_input (input : List Line) (lo hi : ℚ) (hlo : lo ≤ hi)
    {s : Segment} (hs : s ∈ segments (buildStack input).1 lo hi) (x : ℝ)
    (hx : (s.lo : ℝ) ≤ x ∧ x ≤ (s.hi : ℝ)) :
    ∀ l ∈ input, l.evalReal x ≤ s.active.evalReal x := by
  intro l hl
  obtain ⟨k, hk, hle⟩ := buildStack_dominates input x l hl
  exact hle.trans (segments_active _ _ _ (buildStack_good input) hlo hs x hx k hk)

theorem built_segments_nonneg (input : List Line) (lo hi : ℚ) (hlo : lo ≤ hi)
    (hz : (⟨0, 0⟩ : Line) ∈ input)
    {s : Segment} (hs : s ∈ segments (buildStack input).1 lo hi) (x : ℝ)
    (hx : (s.lo : ℝ) ≤ x ∧ x ≤ (s.hi : ℝ)) : 0 ≤ s.active.evalReal x := by
  simpa [Line.evalReal] using built_segments_dominate_input input lo hi hlo hs x hx _ hz

theorem valueReal_le {ls : List Line} {x v : ℝ} (hv : 0 ≤ v)
    (h : ∀ l ∈ ls, l.evalReal x ≤ v) : valueReal ls x ≤ v := by
  induction ls with
  | nil => exact hv
  | cons a as ih =>
    exact max_le (h a List.mem_cons_self)
      (ih (fun l hl => h l (List.mem_cons_of_mem _ hl)))

theorem evalReal_le_valueReal {ls : List Line} {l : Line} (hl : l ∈ ls) (x : ℝ) :
    l.evalReal x ≤ valueReal ls x := by
  induction ls with
  | nil => exact False.elim (List.not_mem_nil hl)
  | cons a as ih =>
    rcases List.mem_cons.mp hl with he | ht
    · subst l; exact le_max_left _ _
    · exact (ih ht).trans (le_max_right _ _)

theorem built_segments_valueReal (input : List Line) (lo hi : ℚ) (hlo : lo ≤ hi)
    (hz : (⟨0, 0⟩ : Line) ∈ input)
    {s : Segment} (hs : s ∈ segments (buildStack input).1 lo hi) (x : ℝ)
    (hx : (s.lo : ℝ) ≤ x ∧ x ≤ (s.hi : ℝ)) :
    valueReal input x = s.active.evalReal x := by
  apply le_antisymm
  · exact valueReal_le (built_segments_nonneg input lo hi hlo hz hs x hx)
      (built_segments_dominate_input input lo hi hlo hs x hx)
  · exact evalReal_le_valueReal
      (buildStack_members input (segments_bounds _ _ _ hlo hs).2.2.2) x

end ReciprocalAnchor.ManyLeaf.FastEnvelope
