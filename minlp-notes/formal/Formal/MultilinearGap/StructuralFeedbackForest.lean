import Formal.CubicGap.Laws
import Mathlib.Logic.Function.DependsOn

/-! Exact gluing of finite laws along a common separator. This is the probability
step used when attaching one factor in an incidence forest. -/

namespace MultilinearGap
namespace SeparatorGluing

open CubicGap

variable {A B S : Type*} [Fintype A] [Fintype B] [Fintype S]

/-- The mass of a separator state. -/
noncomputable def marginal (μ : Law A) (f : A → S) (s : S) : ℝ :=
  (μ.map f).weight s

theorem weight_le_marginal (μ : Law A) (f : A → S) (a : A) :
    μ.weight a ≤ marginal μ f (f a) := by
  classical
  unfold marginal Law.map
  exact le_trans (by simp) (Finset.single_le_sum
    (fun i _ => by split_ifs <;> simp_all [μ.nonneg]) (Finset.mem_univ a))

theorem weight_zero_of_marginal_zero (μ : Law A) (f : A → S) (a : A)
    (h : marginal μ f (f a) = 0) : μ.weight a = 0 := by
  exact le_antisymm (h ▸ weight_le_marginal μ f a) (μ.nonneg a)

/-- Conditional product weights. Zero separator masses contribute zero. -/
noncomputable def weight (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (p : A × B) : ℝ := by
  classical
  exact if f p.1 = g p.2 then μ.weight p.1 * ν.weight p.2 /
    marginal μ f (f p.1) else 0

theorem weight_nonneg (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (p : A × B) : 0 ≤ weight μ ν f g p := by
  classical
  unfold weight
  split_ifs
  · exact div_nonneg (mul_nonneg (μ.nonneg _) (ν.nonneg _)) ((μ.map f).nonneg _)
  · exact le_rfl

theorem sum_right (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (a : A) :
    ∑ b, weight μ ν f g (a, b) = μ.weight a := by
  classical
  by_cases hz : marginal μ f (f a) = 0
  · have ha := weight_zero_of_marginal_zero μ f a hz
    simp [weight, ha]
  · calc
      ∑ b, weight μ ν f g (a, b) =
          μ.weight a * marginal ν g (f a) / marginal μ f (f a) := by
        simp only [weight, marginal, Law.map]
        rw [Finset.mul_sum, Finset.sum_div]
        apply Finset.sum_congr rfl
        intro b _
        by_cases he : f a = g b
        · simp [he]
        · simp [he, Ne.symm he]
      _ = μ.weight a := by rw [← h]; exact mul_div_cancel_right₀ _ hz

theorem weight_swap (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (a : A) (b : B) :
    weight μ ν f g (a, b) = weight ν μ g f (b, a) := by
  classical
  by_cases he : f a = g b
  · unfold weight
    rw [if_pos he, if_pos he.symm, ← he, ← h]
    ring
  · simp [weight, he, Ne.symm he]

theorem sum_left (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (b : B) :
    ∑ a, weight μ ν f g (a, b) = ν.weight b := by
  simp_rw [weight_swap μ ν f g h]
  exact sum_right ν μ g f (fun s => (h s).symm) b

/-- An explicit gluing, preserving both input laws. -/
noncomputable def glue (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) : Law (A × B) where
  weight := weight μ ν f g
  nonneg := weight_nonneg μ ν f g
  mass_one := by
    rw [Fintype.sum_prod_type]
    simp_rw [sum_right μ ν f g h]
    exact μ.mass_one

theorem glue_expect_left (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (φ : A → ℝ) :
    (glue μ ν f g h).expect (fun p => φ p.1) = μ.expect φ := by
  simp only [Law.expect, glue, Fintype.sum_prod_type, ← Finset.sum_mul,
    sum_right μ ν f g h]

theorem glue_expect_right (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (φ : B → ℝ) :
    (glue μ ν f g h).expect (fun p => φ p.2) = ν.expect φ := by
  simp only [Law.expect, glue, Fintype.sum_prod_type]
  rw [Finset.sum_comm]
  simp only [← Finset.sum_mul, sum_left μ ν f g h]

theorem glue_supported (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (p : A × B)
    (hne : f p.1 ≠ g p.2) : (glue μ ν f g h).weight p = 0 := by
  classical
  simp [glue, weight, hne]

/-- Assemble consistent pairs into a new state space. Every observable inherited
from the left state retains its expectation. -/
theorem glue_map_expect_left {C : Type*} [Fintype C]
    (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (assemble : A × B → C)
    (φ : C → ℝ) (ψ : A → ℝ)
    (hφ : ∀ a b, f a = g b → φ (assemble (a, b)) = ψ a) :
    ((glue μ ν f g h).map assemble).expect φ = μ.expect ψ := by
  rw [Law.expect_map, ← glue_expect_left μ ν f g h ψ]
  apply Finset.sum_congr rfl
  rintro ⟨a, b⟩ _
  by_cases he : f a = g b
  · simp [hφ a b he]
  · simp [glue_supported μ ν f g h (a, b) he]

/-- The corresponding preservation result for the right state. -/
theorem glue_map_expect_right {C : Type*} [Fintype C]
    (μ : Law A) (ν : Law B) (f : A → S) (g : B → S)
    (h : ∀ s, marginal μ f s = marginal ν g s) (assemble : A × B → C)
    (φ : C → ℝ) (ψ : B → ℝ)
    (hφ : ∀ a b, f a = g b → φ (assemble (a, b)) = ψ b) :
    ((glue μ ν f g h).map assemble).expect φ = ν.expect ψ := by
  rw [Law.expect_map, ← glue_expect_right μ ν f g h ψ]
  apply Finset.sum_congr rfl
  rintro ⟨a, b⟩ _
  by_cases he : f a = g b
  · simp [hφ a b he]
  · simp [glue_supported μ ν f g h (a, b) he]

end SeparatorGluing

namespace ScopeGluing

open CubicGap SeparatorGluing

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Two laws have the same distribution on a scope. -/
def AgreesOn (μ ν : Law (Vertex I)) (s : Finset I) : Prop :=
  ∀ φ : Vertex I → ℝ, DependsOn φ (s : Set I) → μ.expect φ = ν.expect φ

theorem agreesOn_empty (μ ν : Law (Vertex I)) : AgreesOn μ ν ∅ := by
  intro φ hφ
  have hc (v : Vertex I) : φ v = φ (fun _ => false) := hφ (by simp)
  simp [Law.expect, hc, ← Finset.sum_mul, μ.mass_one, ν.mass_one]

theorem agreesOn_subsingleton (μ ν : Law (Vertex I)) (s : Finset I)
    (hs : (s : Set I).Subsingleton) (h : ∀ i, AgreesOn μ ν {i}) : AgreesOn μ ν s := by
  by_cases hn : s.Nonempty
  · obtain ⟨i, hi⟩ := hn
    intro φ hφ
    apply h i φ
    apply hφ.mono
    intro j hj
    simp only [Finset.coe_singleton, Set.mem_singleton_iff]
    exact hs hj hi
  · simpa [Finset.not_nonempty_iff_eq_empty.mp hn] using agreesOn_empty μ ν

/-- Restrict an assignment to its factor scope. -/
def restrict (s : Finset I) (v : Vertex I) : Vertex s := fun i => v i

theorem marginal_eq_of_agreesOn (μ ν : Law (Vertex I)) (s : Finset I)
    (h : AgreesOn μ ν s) (z : Vertex s) :
    marginal μ (restrict s) z = marginal ν (restrict s) z := by
  classical
  have he := h (fun v => if restrict s v = z then 1 else 0) (by
    intro a b hab
    have hr : restrict s a = restrict s b := funext fun i => hab i i.property
    change (if restrict s a = z then (1 : ℝ) else 0) =
      (if restrict s b = z then 1 else 0)
    rw [hr])
  simp only [marginal, Law.map, Law.expect, mul_ite, mul_one, mul_zero] at he ⊢
  convert he using 1 <;> apply Finset.sum_congr rfl <;> intro v _ <;>
    split_ifs <;> rfl

/-- Combine two assignments, taking the old scope from the first. -/
def assemble (s : Finset I) (p : Vertex I × Vertex I) : Vertex I :=
  fun i => if i ∈ s then p.1 i else p.2 i

/-- Glue two laws whose marginals agree on the scope intersection. -/
noncomputable def glue (μ ν : Law (Vertex I)) (s t : Finset I)
    (h : ∀ z, marginal μ (restrict (s ∩ t)) z =
      marginal ν (restrict (s ∩ t)) z) : Law (Vertex I) :=
  (SeparatorGluing.glue μ ν (restrict (s ∩ t)) (restrict (s ∩ t)) h).map
    (assemble s)

theorem expect_left (μ ν : Law (Vertex I)) (s t : Finset I)
    (h : ∀ z, marginal μ (restrict (s ∩ t)) z =
      marginal ν (restrict (s ∩ t)) z)
    (φ : Vertex I → ℝ) (hφ : DependsOn φ (s : Set I)) :
    (glue μ ν s t h).expect φ = μ.expect φ := by
  apply glue_map_expect_left μ ν (restrict (s ∩ t)) (restrict (s ∩ t)) h
  intro a b _
  apply hφ
  intro i hi
  change i ∈ s at hi
  simp [assemble, hi]

theorem expect_right (μ ν : Law (Vertex I)) (s t : Finset I)
    (h : ∀ z, marginal μ (restrict (s ∩ t)) z =
      marginal ν (restrict (s ∩ t)) z)
    (φ : Vertex I → ℝ) (hφ : DependsOn φ (t : Set I)) :
    (glue μ ν s t h).expect φ = ν.expect φ := by
  apply glue_map_expect_right μ ν (restrict (s ∩ t)) (restrict (s ∩ t)) h
  intro a b hab
  apply hφ
  intro i hi
  by_cases his : i ∈ s
  · have he := congrFun hab ⟨i, Finset.mem_inter.mpr ⟨his, hi⟩⟩
    simpa [assemble, restrict, his] using he
  · simp [assemble, his]

theorem glue_singletons (μ ν ρ : Law (Vertex I)) (s t : Finset I)
    (h : ∀ z, marginal μ (restrict (s ∩ t)) z =
      marginal ν (restrict (s ∩ t)) z)
    (hμ : ∀ i, AgreesOn μ ρ {i}) (hν : ∀ i, AgreesOn ν ρ {i}) :
    ∀ i, AgreesOn (glue μ ν s t h) ρ {i} := by
  intro i φ hφ
  by_cases hi : i ∈ s
  · rw [expect_left μ ν s t h φ (hφ.mono (by simpa using hi))]
    exact hμ i φ hφ
  · trans ν.expect φ
    · apply glue_map_expect_right μ ν (restrict (s ∩ t)) (restrict (s ∩ t)) h
      intro a b _
      apply hφ
      intro j hj
      have hji : j = i := by simpa using hj
      subst j
      simp [assemble, hi]
    · exact hν i φ hφ

theorem agreesOn_union_subsingleton (μ ν : Law (Vertex I)) (F s : Finset I)
    (hs : (s : Set I).Subsingleton) (hF : AgreesOn μ ν F)
    (h : ∀ i, AgreesOn μ ν (insert i F)) : AgreesOn μ ν (F ∪ s) := by
  by_cases hn : s.Nonempty
  · obtain ⟨i, hi⟩ := hn
    intro φ hφ
    apply h i φ
    apply hφ.mono
    intro j hj
    rcases Finset.mem_union.mp hj with hj | hj
    · exact Finset.mem_insert_of_mem hj
    · exact Finset.mem_insert.mpr (Or.inl (hs hj hi))
  · simpa [Finset.not_nonempty_iff_eq_empty.mp hn] using hF

/-- A shared feedback block can be carried through every gluing step. -/
theorem glue_feedback_pairs (μ ν ρ : Law (Vertex I)) (F s t : Finset I)
    (hFs : F ⊆ s) (hFt : F ⊆ t)
    (h : ∀ z, marginal μ (restrict (s ∩ t)) z =
      marginal ν (restrict (s ∩ t)) z)
    (hμ : ∀ i, AgreesOn μ ρ (insert i F))
    (hν : ∀ i, AgreesOn ν ρ (insert i F)) :
    ∀ i, AgreesOn (glue μ ν s t h) ρ (insert i F) := by
  intro i φ hφ
  by_cases hi : i ∈ s
  · rw [expect_left μ ν s t h φ (hφ.mono (by
      intro j hj
      rcases Finset.mem_insert.mp hj with rfl | hj
      · exact hi
      · exact hFs hj))]
    exact hμ i φ hφ
  · trans ν.expect φ
    · apply glue_map_expect_right μ ν (restrict (s ∩ t)) (restrict (s ∩ t)) h
      intro a b hab
      apply hφ
      intro j hj
      rcases Finset.mem_insert.mp hj with rfl | hj
      · simp [assemble, hi]
      · have hjs := hFs hj
        have he := congrFun hab ⟨j, Finset.mem_inter.mpr ⟨hjs, hFt hj⟩⟩
        simpa [assemble, restrict, hjs] using he
    · exact hν i φ hφ

end ScopeGluing

namespace ForestGluing

open CubicGap ScopeGluing

variable {I E : Type*} [Fintype I] [DecidableEq I]

/-- Variables covered by a finite list of factors. -/
def covered (scope : E → Finset I) : List E → Finset I
  | [] => ∅
  | e :: es => scope e ∪ covered scope es

omit [Fintype I] in
theorem scope_subset_covered (scope : E → Finset I) {es : List E} {e : E}
    (he : e ∈ es) : scope e ⊆ covered scope es := by
  induction es with
  | nil => simp at he
  | cons a es ih =>
    rcases List.mem_cons.mp he with rfl | he
    · exact Finset.subset_union_left
    · exact (ih he).trans Finset.subset_union_right

/-- A constructive incidence-forest elimination order: each factor meets the
later factors in at most one variable. Empty intersections are allowed. -/
inductive EliminationOrder (scope : E → Finset I) : List E → Prop
  | nil : EliminationOrder scope []
  | cons (e : E) (es : List E) (tail : EliminationOrder scope es)
      (separator : ((covered scope es ∩ scope e : Finset I) : Set I).Subsingleton) :
      EliminationOrder scope (e :: es)

/-- Sequential gluing constructs a genuine global finite law. It preserves all
factor distributions and all singleton distributions without multiplying losses.
The hypothesis is a combinatorial elimination order, not an assumed gluing law. -/
theorem exists_global (scope : E → Finset I) (localLaw : E → Law (Vertex I))
    (reference : Law (Vertex I))
    (consistent : ∀ e i, AgreesOn (localLaw e) reference {i})
    (es : List E) (order : EliminationOrder scope es) :
    ∃ μ : Law (Vertex I), (∀ i, AgreesOn μ reference {i}) ∧
      ∀ e ∈ es, AgreesOn μ (localLaw e) (scope e) := by
  induction order with
  | nil => exact ⟨reference, fun _ _ _ => rfl, by simp⟩
  | cons e es _ hsep ih =>
    obtain ⟨μ, hμ, hlocal⟩ := ih
    have hsingle (i : I) : AgreesOn μ (localLaw e) {i} := by
      intro φ hφ
      exact (hμ i φ hφ).trans (consistent e i φ hφ).symm
    have hmatch := marginal_eq_of_agreesOn μ (localLaw e)
      (covered scope es ∩ scope e)
      (agreesOn_subsingleton μ (localLaw e) _ hsep hsingle)
    refine ⟨glue μ (localLaw e) (covered scope es) (scope e) hmatch,
      glue_singletons μ (localLaw e) reference _ _ hmatch hμ (consistent e), ?_⟩
    intro a ha φ hφ
    rcases List.mem_cons.mp ha with rfl | ha
    · exact expect_right μ (localLaw a) _ _ hmatch φ hφ
    · rw [expect_left μ (localLaw e) _ _ hmatch φ
        (hφ.mono (scope_subset_covered scope ha))]
      exact hlocal a ha φ hφ

/-- Gluing with a fixed feedback block. The local laws need agree only on that
block together with each individual outside variable. -/
theorem exists_global_feedback (scope : E → Finset I) (localLaw : E → Law (Vertex I))
    (reference : Law (Vertex I)) (F : Finset I)
    (consistentF : ∀ e, AgreesOn (localLaw e) reference F)
    (consistent : ∀ e i, AgreesOn (localLaw e) reference (insert i F))
    (es : List E) (order : EliminationOrder scope es) :
    ∃ μ : Law (Vertex I), AgreesOn μ reference F ∧
      (∀ i, AgreesOn μ reference (insert i F)) ∧
      ∀ e ∈ es, AgreesOn μ (localLaw e) (F ∪ scope e) := by
  induction order with
  | nil => exact ⟨reference, fun _ _ => rfl, fun _ _ _ => rfl, by simp⟩
  | cons e es _ hsep ih =>
    obtain ⟨μ, hμF, hμ, hlocal⟩ := ih
    have hsingle (i : I) : AgreesOn μ (localLaw e) (insert i F) := by
      intro φ hφ
      exact (hμ i φ hφ).trans (consistent e i φ hφ).symm
    have hbase : AgreesOn μ (localLaw e) F := by
      intro φ hφ
      exact (hμF φ hφ).trans (consistentF e φ hφ).symm
    have hsepEq : (F ∪ covered scope es) ∩ (F ∪ scope e) =
        F ∪ (covered scope es ∩ scope e) := by
      ext i
      simp only [Finset.mem_inter, Finset.mem_union]
      tauto
    have hagree : AgreesOn μ (localLaw e)
        ((F ∪ covered scope es) ∩ (F ∪ scope e)) := by
      rw [hsepEq]
      exact agreesOn_union_subsingleton μ (localLaw e) F _ hsep hbase hsingle
    have hmatch := marginal_eq_of_agreesOn μ (localLaw e) _ hagree
    refine ⟨glue μ (localLaw e) (F ∪ covered scope es) (F ∪ scope e) hmatch,
      ?_, glue_feedback_pairs μ (localLaw e) reference F _ _
        Finset.subset_union_left Finset.subset_union_left hmatch hμ (consistent e), ?_⟩
    · intro φ hφ
      rw [expect_left μ (localLaw e) _ _ hmatch φ
        (hφ.mono Finset.subset_union_left)]
      exact hμF φ hφ
    · intro a ha φ hφ
      rcases List.mem_cons.mp ha with rfl | ha
      · exact expect_right μ (localLaw a) _ _ hmatch φ hφ
      · rw [expect_left μ (localLaw e) _ _ hmatch φ
          (hφ.mono (by
            intro i hi
            rcases Finset.mem_union.mp hi with hi | hi
            · exact Finset.mem_union_left _ hi
            · exact Finset.mem_union_right _ (scope_subset_covered scope ha hi)))]
        exact hlocal a ha φ hφ

end ForestGluing
end MultilinearGap
