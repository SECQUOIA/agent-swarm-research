import Formal.FBBT.Boxes
import Formal.FBBT.Contractors
import Formal.FBBT.Circuit
import Formal.FBBT.Dynamics

namespace FBBT

noncomputable section

/-- One defining equality of the constant-coefficient input circuit. -/
def equations (n : ℕ) (a : CircuitVar n) : Set (CircuitVar n → ℝ) :=
  {x | x a = (circuitRhs n a).eval x}

/-- Fix all acyclic variables exactly, and supply the two feedback coordinates. -/
def embed (n : ℕ) (p : ℝ × ℝ) : CircuitVar n → ℝ
  | .z => p.1
  | .w => p.2
  | a => circuitPoint n a

def strongBox (n : ℕ) (Q : FeedbackBox) : Box (CircuitVar n) :=
  ⟨embed n (Q.lz, Q.lw), embed n (Q.uz, Q.uw)⟩

theorem embed_mem_strongBox_iff (n : ℕ) (p : ℝ × ℝ) (Q : FeedbackBox) :
    embed n p ∈ (strongBox n Q).carrier ↔ Q.Mem p := by
  constructor
  · intro h
    exact ⟨(h .z).1, (h .z).2, (h .w).1, (h .w).2⟩
  · intro h a
    cases a <;> simp_all [strongBox, embed, FeedbackBox.Mem]

theorem mem_strongBox (n : ℕ) (Q : FeedbackBox) (x : CircuitVar n → ℝ)
    (hx : x ∈ (strongBox n Q).carrier) :
    Q.Mem (x .z, x .w) ∧ x = embed n (x .z, x .w) := by
  constructor
  · exact ⟨(hx .z).1, (hx .z).2, (hx .w).1, (hx .w).2⟩
  · funext a
    cases a with
    | z => rfl
    | w => rfl
    | b i => exact le_antisymm (hx (.b i)).2 (hx (.b i)).1
    | c i => exact le_antisymm (hx (.c i)).2 (hx (.c i)).1
    | h i => exact le_antisymm (hx (.h i)).2 (hx (.h i)).1
    | v i => exact le_antisymm (hx (.v i)).2 (hx (.v i)).1

/-- Exact two-coordinate hulls remain exact when all other coordinates are fixed. -/
theorem strongBox_hull {n : ℕ} {S : Set (ℝ × ℝ)} {Q : FeedbackBox}
    (hne : S.Nonempty) (hQ : IsFeedbackHull S Q) :
    Box.IsHull (embed n '' S) (strongBox n Q) := by
  constructor
  · rintro _ ⟨p, hp, rfl⟩
    exact (embed_mem_strongBox_iff n p Q).2 (hQ.1 p hp)
  · intro D hD x hx
    obtain ⟨hp, heq⟩ := mem_strongBox n Q x hx
    rw [heq]
    let R : FeedbackBox := ⟨D.lower .z, D.lower .w, D.upper .z, D.upper .w⟩
    have hR : ∀ p ∈ S, R.Mem p := by
      intro p hp
      have hd := hD ⟨p,hp,rfl⟩
      exact ⟨(hd .z).1, (hd .z).2, (hd .w).1, (hd .w).2⟩
    have hr := hQ.2 R hR _ hp
    obtain ⟨p₀,hp₀⟩ := hne
    have hd := hD ⟨p₀,hp₀,rfl⟩
    intro a
    cases a with
    | z => exact ⟨hr.1,hr.2.1⟩
    | w => exact ⟨hr.2.2.1,hr.2.2.2⟩
    | b i => exact hd (.b i)
    | c i => exact hd (.c i)
    | h i => exact hd (.h i)
    | v i => exact hd (.v i)

theorem product_intersection (n : ℕ) (Q : FeedbackBox) :
    (strongBox n Q).carrier ∩ equations n .w =
      embed n '' {p | Q.Mem p ∧ p.2 = cValue n * p.1} := by
  ext x
  constructor
  · rintro ⟨hx,he⟩
    obtain ⟨hp,hxp⟩ := mem_strongBox n Q x hx
    refine ⟨(x .z,x .w), ⟨hp, ?_⟩, hxp.symm⟩
    rw [hxp] at he
    simpa [equations, circuitRhs, PrimitiveRhs.eval, embed, circuitPoint] using he
  · rintro ⟨p, ⟨hp,he⟩, rfl⟩
    exact ⟨(embed_mem_strongBox_iff n p Q).2 hp,
      by simpa [equations, circuitRhs, PrimitiveRhs.eval, embed, circuitPoint] using he⟩

theorem affine_intersection (n : ℕ) (Q : FeedbackBox) :
    (strongBox n Q).carrier ∩ equations n .z =
      embed n '' {p | Q.Mem p ∧ p.1 = bValue n + p.2} := by
  ext x
  constructor
  · rintro ⟨hx,he⟩
    obtain ⟨hp,hxp⟩ := mem_strongBox n Q x hx
    refine ⟨(x .z,x .w), ⟨hp, ?_⟩, hxp.symm⟩
    rw [hxp] at he
    simpa [equations, circuitRhs, PrimitiveRhs.eval, embed, circuitPoint] using he
  · rintro ⟨p, ⟨hp,he⟩, rfl⟩
    exact ⟨(embed_mem_strongBox_iff n p Q).2 hp,
      by simpa [equations, circuitRhs, PrimitiveRhs.eval, embed, circuitPoint] using he⟩

theorem strongBox_product_step {n : ℕ} {Q : FeedbackBox}
    (h : Good (bValue n) (cValue n) Q) :
    Box.Step (equations n) .w (strongBox n Q)
      (strongBox n (productUpdate (cValue n) Q)) := by
  unfold Box.Step
  rw [product_intersection]
  exact strongBox_hull ⟨(1,cValue n),h.feasible,by simp⟩ h.product_hull

theorem strongBox_affine_step {n : ℕ} {Q : FeedbackBox}
    (h : Good (bValue n) (cValue n) Q) :
    Box.Step (equations n) .z (strongBox n Q)
      (strongBox n (affineUpdate (bValue n) (cValue n) Q)) := by
  unfold Box.Step
  rw [affine_intersection]
  exact strongBox_hull ⟨(1,cValue n),h.feasible,(bValue_add_cValue n).symm⟩ h.affine_hull

theorem embed_upstream_equation (n : ℕ) (p : ℝ × ℝ) (a : CircuitVar n)
    (hz : a ≠ .z) (hw : a ≠ .w) : embed n p ∈ equations n a := by
  have hs := circuitPoint_solution n a
  cases a with
  | b i =>
    obtain ⟨i,hi⟩ := i
    cases i <;> simpa [equations, circuitRhs, PrimitiveRhs.eval, embed] using hs
  | c i =>
    obtain ⟨i,hi⟩ := i
    cases i <;> simpa [equations, circuitRhs, PrimitiveRhs.eval, embed] using hs
  | h i => simpa [equations, circuitRhs, PrimitiveRhs.eval, embed] using hs
  | v i => simpa [equations, circuitRhs, PrimitiveRhs.eval, embed] using hs
  | z => exact (hz rfl).elim
  | w => exact (hw rfl).elim

theorem strongBox_upstream_step (n : ℕ) (Q : FeedbackBox) (a : CircuitVar n)
    (hz : a ≠ .z) (hw : a ≠ .w) :
    Box.Step (equations n) a (strongBox n Q) (strongBox n Q) := by
  have he : (strongBox n Q).carrier ⊆ equations n a := by
    intro x hx
    obtain ⟨_,heq⟩ := mem_strongBox n Q x hx
    rw [heq]
    exact embed_upstream_equation n _ a hz hw
  constructor
  · exact Set.inter_subset_left
  · intro D hD x hx
    exact hD ⟨hx,he hx⟩

theorem strongBox_initial_subset_unit (n : ℕ) :
    (strongBox n initialBox).carrier ⊆ (Box.unit (CircuitVar n)).carrier := by
  intro x hx
  obtain ⟨hp,heq⟩ := mem_strongBox n initialBox x hx
  rw [heq]
  intro a
  cases a with
  | z => exact ⟨hp.1,hp.2.1⟩
  | w => exact ⟨hp.2.2.1,hp.2.2.2⟩
  | b i => exact circuitPoint_mem_unit n (.b i)
  | c i => exact circuitPoint_mem_unit n (.c i)
  | h i => exact circuitPoint_mem_unit n (.h i)
  | v i => exact circuitPoint_mem_unit n (.v i)

def feedbackAction {n : ℕ} : CircuitVar n → FeedbackAction
  | .z => .affine
  | .w => .product
  | _ => .idle

def strongRun (n : ℕ) (schedule : ℕ → CircuitVar n) (t : ℕ) : Box (CircuitVar n) :=
  strongBox n (feedbackRun (bValue n) (cValue n) (fun t => feedbackAction (schedule t)) t)

/-- The explicit stronger trajectory is a genuine primitive hull run of the full input. -/
theorem strongRun_isRun (n : ℕ) (schedule : ℕ → CircuitVar n) :
    Box.Run (equations n) (strongBox n initialBox) schedule (strongRun n schedule) := by
  constructor
  · rfl
  · intro t
    have hg := feedbackRun_good (bValue n) (cValue n) (bValue_pos n)
      (cValue_pos n) (bValue_add_cValue n) (fun t => feedbackAction (schedule t)) t
    cases ha : schedule t with
    | z => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_affine_step hg
    | w => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_product_step hg
    | b i => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_upstream_step n _ (.b i) (by simp) (by simp)
    | c i => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_upstream_step n _ (.c i) (by simp) (by simp)
    | h i => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_upstream_step n _ (.h i) (by simp) (by simp)
    | v i => simpa [strongRun, feedbackRun, ha, feedbackAction, feedbackStep]
        using strongBox_upstream_step n _ (.v i) (by simp) (by simp)

end
end FBBT
