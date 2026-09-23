import Formal.ReciprocalAnchor.ManyFastEnvelope

/-! Linear removal of dominated parallel lines before the envelope stack. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- Each counter increment records a rational comparison: slope equality, then
intercept order only when slopes agree. The winner is an input line. -/
def parallelDedup : List Line → List Line × ℕ
  | [] => ([], 0)
  | a :: as =>
      let r := parallelDedup as
      match r.1 with
      | [] => ([a], r.2)
      | b :: bs =>
          if a.slope = b.slope then
            if a.intercept ≤ b.intercept then (b :: bs, r.2 + 2)
            else (a :: bs, r.2 + 2)
          else (a :: b :: bs, r.2 + 1)

theorem parallelDedup_members_cost (ls : List Line) :
    (∀ a ∈ (parallelDedup ls).1, a ∈ ls) ∧
    (parallelDedup ls).1.length ≤ ls.length ∧
    (parallelDedup ls).2 ≤ 2 * ls.length := by
  induction ls with
  | nil => simp [parallelDedup]
  | cons a as ih =>
    rcases ih with ⟨hm, hl, hc⟩
    simp only [parallelDedup]
    split <;> rename_i he
    · simp only [List.length_cons, List.length_nil, List.mem_singleton]
      exact ⟨by intro x hx; subst x; simp, by omega, by omega⟩
    · rename_i b bs
      rw [he] at hm hl
      split <;> rename_i hs
      · split <;> rename_i hi
        · refine ⟨?_, ?_, ?_⟩
          · intro x hx; exact List.mem_cons_of_mem a (hm x hx)
          · simp only [List.length_cons] at *; omega
          · simp only [List.length_cons]; omega
        · refine ⟨?_, ?_, ?_⟩
          · intro x hx
            rcases List.mem_cons.mp hx with rfl | hx
            · exact List.mem_cons_self
            · exact List.mem_cons_of_mem a (hm x (List.mem_cons_of_mem b hx))
          · simp only [List.length_cons] at *; omega
          · simp only [List.length_cons]; omega
      · refine ⟨?_, ?_, ?_⟩
        · intro x hx
          rcases List.mem_cons.mp hx with rfl | hx
          · exact List.mem_cons_self
          · exact List.mem_cons_of_mem a (hm x hx)
        · simp only [List.length_cons] at *; omega
        · simp only [List.length_cons]; omega

theorem parallelDedup_valueReal (ls : List Line) (x : ℝ) :
    valueReal (parallelDedup ls).1 x = valueReal ls x := by
  induction ls with
  | nil => simp [parallelDedup]
  | cons a as ih =>
    simp only [parallelDedup]
    split <;> rename_i he
    · rw [he] at ih
      simp only [valueReal] at ih ⊢
      rw [← ih]
    · rename_i b bs
      rw [he] at ih
      simp only [valueReal] at ih
      have hbase : valueReal (a :: as) x = max (a.evalReal x)
          (max (b.evalReal x) (valueReal bs x)) := by simp only [valueReal, ← ih]
      rw [hbase]
      split <;> rename_i hs
      · have hsr : (a.slope : ℝ) = b.slope := by exact_mod_cast hs
        split <;> rename_i hi
        · have hir : (a.intercept : ℝ) ≤ b.intercept := by exact_mod_cast hi
          have hv : a.evalReal x ≤ b.evalReal x := by dsimp [Line.evalReal]; rw [hsr]; linarith
          simp only [valueReal]
          rw [max_eq_right (le_trans hv (le_max_left _ _))]
        · have hir : (b.intercept : ℝ) ≤ a.intercept := by exact_mod_cast (le_of_not_ge hi)
          have hv : b.evalReal x ≤ a.evalReal x := by dsimp [Line.evalReal]; rw [hsr]; linarith
          simp only [valueReal]
          rw [← max_assoc, max_eq_left hv]
      · rfl

theorem parallelDedup_strict (ls : List Line)
    (hs : ls.Pairwise (fun a b => a.slope ≤ b.slope)) :
    (parallelDedup ls).1.Pairwise (fun a b => a.slope < b.slope) := by
  induction ls with
  | nil => simp [parallelDedup]
  | cons a as ih =>
    have htail := ih hs.tail
    have hmem := (parallelDedup_members_cost as).1
    simp only [parallelDedup]
    split <;> rename_i he
    · simp
    · rename_i b bs
      rw [he] at htail hmem
      have hab : a.slope ≤ b.slope := List.rel_of_pairwise_cons hs (hmem b List.mem_cons_self)
      split <;> rename_i heq
      · split
        · exact htail
        · apply List.Pairwise.cons
          · intro c hc
            have hbc := List.rel_of_pairwise_cons htail hc
            simpa [heq] using hbc
          · exact htail.tail
      · apply List.Pairwise.cons
        · intro c hc
          rcases List.mem_cons.mp hc with rfl | hc
          · exact lt_of_le_of_ne hab heq
          · exact lt_of_le_of_lt hab (List.rel_of_pairwise_cons htail hc)
        · exact htail

end ReciprocalAnchor.ManyLeaf.FastEnvelope
