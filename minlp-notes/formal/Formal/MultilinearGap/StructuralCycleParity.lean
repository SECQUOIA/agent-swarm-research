import Formal.MultilinearGap.StructuralTreewidthGraph

/-! Simple-cycle factor parity extends to every closed trail by removing
simple subcycles. Repeated edges are excluded: a backtrack need not have even
factor parity, so the trail hypothesis is material. -/
namespace MultilinearGap.TreewidthGraph
open SimpleGraph
variable {V : Type*} {G : SimpleGraph V}

theorem cycleParity_remove_subcycle (factor : V → Bool) {u v : V}
    (a : G.Walk u v) (c : G.Walk v v) (b : G.Walk v u) :
    cycleParity factor ((a.append c).append b) =
      cycleParity factor (a.append b) + cycleParity factor c := by
  have hc := pathParity_eq_start_add_tail factor c
  change pathParity factor c = factorWeight factor v + cycleParity factor c at hc
  rw [cycleParity_append, cycleParity_append, pathParity_append, hc]
  ring

/-- Every closed trail decomposes into simple cycles for the purpose of
factor parity. This theorem applies to actual graph walks. -/
theorem cycleParity_eq_zero_of_isTrail (factor : V → Bool)
    (hcycle : ∀ (v : V) (c : G.Walk v v), c.IsCycle → cycleParity factor c = 0)
    {u : V} (p : G.Walk u u) (hp : p.IsTrail) : cycleParity factor p = 0 := by
  classical
  induction hn : p.length using Nat.strong_induction_on generalizing u with
  | h n ih =>
    by_cases hpath : p.IsPath
    · have he : p = .nil := by simpa using p.isPath_iff_nil.mp hpath
      subst p
      simp [cycleParity]
    · have hex : ∃ (v : V) (c : G.Walk v v), c.IsSubwalk p ∧ c.IsCycle := by
        have h := hp.isPath_iff_isSubwalk_imp_not_isCycle
        by_contra hn
        apply hpath
        exact h.mpr fun v c hsub hc => hn ⟨v, c, hsub, hc⟩
      obtain ⟨v, c, ⟨a, b, rfl⟩, hc⟩ := hex
      have hab : (a.append b).IsTrail := by
        rw [Walk.isTrail_def] at hp ⊢
        simp only [Walk.edges_append] at hp ⊢
        exact hp.sublist ((List.append_sublist_append_right b.edges).mpr
          (List.sublist_append_left a.edges c.edges))
      have hpos : 0 < c.length := by
        have hcne := hc.not_nil
        have : c.length ≠ 0 := by simpa [Walk.length_eq_zero_iff] using hcne
        omega
      have hlen : (a.append b).length < n := by
        simp only [Walk.length_append] at hn ⊢
        omega
      have hr := ih (a.append b).length hlen (a.append b) hab rfl
      rw [cycleParity_remove_subcycle, hr, hcycle v c hc, add_zero]

end MultilinearGap.TreewidthGraph
