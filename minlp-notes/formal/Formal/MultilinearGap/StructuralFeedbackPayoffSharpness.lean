import Formal.MultilinearGap.StructuralFeedbackUniversal
import Formal.MultilinearGap.StructuralFeedbackOrder
import Mathlib.Combinatorics.SimpleGraph.Star

/-! Sharpness of universal nonnegative-payoff retention. Factors are indexed
cell indicators on the same scope. Their incidence graph retains the distinct
factor indices. These payoffs are not positive monomials. -/
namespace MultilinearGap.StructuralFeedbackPayoffSharpness
open CubicGap
noncomputable section
abbrev Coord (f : ℕ) := Option (Fin f)
abbrev State (f : ℕ) := Vertex (Coord f)
def feedback (f : ℕ) : Finset (Coord f) := Finset.univ.image some
def payoff {f : ℕ} (s v : State f) : ℝ := if v = s then 1 else 0
theorem payoff_nonneg {f : ℕ} (s v : State f) : 0 ≤ payoff s v := by
  unfold payoff
  split_ifs <;> norm_num

theorem payoff_dependsOn {f : ℕ} (s : State f) :
    DependsOn (payoff s) (Finset.univ : Finset (Coord f)) := by
  simpa using dependsOn_univ (payoff s)

def opposite {f : ℕ} (s : State f) : State f := fun i => !(s i)
def localLaw {f : ℕ} (s : State f) : Law (State f) :=
  (Law.point s).mix (Law.point (opposite s)) (1 / 2) (1 / 2)
    (by norm_num) (by norm_num) (by norm_num)
@[simp] theorem card_feedback (f : ℕ) : (feedback f).card = f := by
  simp [feedback, Finset.card_image_of_injective _ (Option.some_injective _)]
@[simp] theorem localLaw_means {f : ℕ} (s : State f) :
    HasMeans (localLaw s) (fun _ => 1 / 2) := by
  intro i
  simp only [localLaw, Law.expect, Law.mix, add_mul, Finset.sum_add_distrib,
    mul_assoc, ← Finset.mul_sum]
  change (1 / 2 : ℝ) * (Law.point s).expect _ + (1 / 2 : ℝ) * (Law.point (opposite s)).expect _ = _
  simp only [Law.expect_point, opposite, vertexPoint]
  by_cases hb : s i = true
  · simp [hb]
  · have hf : s i = false := Bool.eq_false_iff.mpr hb
    simp [hf]
@[simp] theorem localLaw_payoff {f : ℕ} (s : State f) :
    (localLaw s).expect (payoff s) = 1 / 2 := by
  have hne : opposite s ≠ s := by
    intro h
    have := congrFun h none
    simp only [opposite] at this
    cases s none <;> simp_all
  simp [localLaw, Law.expect, Law.mix, Law.point, payoff, Ne.symm hne]
/-- Every feasible law assigns a cell at most half its mass. -/
theorem payoff_upper {f : ℕ} (s : State f) (μ : Law (State f))
    (hm : HasMeans μ (fun _ => 1 / 2)) : μ.expect (payoff s) ≤ 1 / 2 := by
  have h := feedbackCellMass_le_literal μ (fun _ => 1 / 2) hm Finset.univ s
    (Finset.mem_univ none)
  have heq : feedbackCell Finset.univ s = payoff s := by
    funext v
    simp [feedbackCell_eq_indicator, payoff, funext_iff]
  rw [feedbackCellMass, heq] at h
  cases hb : s none <;> norm_num [feedbackLiteral, hb] at h ⊢ <;> exact h
/-- The local optimum is attained. -/
theorem local_optimum {f : ℕ} (s : State f) :
    IsGreatest {r : ℝ | ∃ μ : Law (State f), HasMeans μ (fun _ => 1 / 2) ∧
      μ.expect (payoff s) = r} (1 / 2) := by
  refine ⟨⟨localLaw s, localLaw_means s, localLaw_payoff s⟩, ?_⟩
  rintro r ⟨μ, hm, rfl⟩
  exact payoff_upper s μ hm
@[simp] theorem sum_payoffs {f : ℕ} (v : State f) : ∑ s : State f, payoff s v = 1 := by
  simp [payoff]
/-- The sum equals one for every global law. -/
theorem sum_expectations {f : ℕ} (μ : Law (State f)) :
    ∑ s : State f, μ.expect (payoff s) = 1 := by
  rw [← Law.expect_sum]
  simp
theorem sum_local_optima (f : ℕ) : (∑ _ : State f, (1 / 2 : ℝ)) = 2^f := by
  simp [State, Coord, pow_succ]
/-- The actual indexed incidence graph after feedback deletion is a star,
with the removed variables isolated. -/
theorem residual_incidence_acyclic (f : ℕ) :
    (StructuralTreewidth.incidenceGraph (fun (i : Coord f) (_s : State f) =>
      i ∈ (Finset.univ : Finset (Coord f)) \ feedback f)).IsAcyclic := by
  apply (SimpleGraph.isAcyclic_starGraph (Sum.inl (none : Coord f))).anti
  intro v w h
  cases v with
  | inl i =>
    cases w with
    | inl j => exact False.elim h
    | inr s =>
      have hi : i = none := by
        cases i with
        | none => rfl
        | some i => simp [StructuralTreewidth.incidenceGraph, feedback] at h
      subst i
      simp [SimpleGraph.starGraph]
  | inr s =>
    cases w with
    | inl i =>
      have hi : i = none := by
        cases i with
        | none => rfl
        | some i => simp [StructuralTreewidth.incidenceGraph, feedback] at h
      subst i
      simp [SimpleGraph.starGraph]
    | inr t => exact False.elim h
/-- Any retention fraction valid simultaneously for these locally optimal
laws is at most `2^(-f)`, including when `f=0`. -/
theorem retention_le (f : ℕ) (c : ℝ) (μ : Law (State f))
    (h : ∀ s : State f, c * (localLaw s).expect (payoff s) ≤ μ.expect (payoff s)) :
    c ≤ (1 / 2 : ℝ)^f := by
  have hs := Finset.sum_le_sum (s := Finset.univ) (fun s _ => h s)
  simp only [localLaw_payoff, ← Finset.mul_sum, sum_local_optima,
    sum_expectations] at hs
  have hp : (0 : ℝ) < 2^f := by positivity
  have hpow : (1 / 2 : ℝ)^f * 2^f = 1 := by rw [← mul_pow]; norm_num
  nlinarith
/-! Distinct genuine scopes: one private mean-one variable for each cell. -/
abbrev PrivateCoord (f : ℕ) := Coord f ⊕ State f

def privateFeedback (f : ℕ) : Finset (PrivateCoord f) :=
  (feedback f).image Sum.inl

def privateScope {f : ℕ} (s : State f) : Finset (PrivateCoord f) :=
  Finset.univ.image Sum.inl ∪ {Sum.inr s}

def privateMeans (f : ℕ) : PrivateCoord f → ℝ := Sum.elim (fun _ => 1 / 2) (fun _ => 1)

def privatePayoff {f : ℕ} (s : State f) (v : Vertex (PrivateCoord f)) : ℝ :=
  payoff s (v ∘ Sum.inl) * vertexPoint v (.inr s)

def extendState {f : ℕ} (v : State f) : Vertex (PrivateCoord f) :=
  Sum.elim v (fun _ => true)

def privateLocalLaw {f : ℕ} (s : State f) : Law (Vertex (PrivateCoord f)) :=
  (localLaw s).map extendState

@[simp] theorem card_privateFeedback (f : ℕ) : (privateFeedback f).card = f := by
  simp [privateFeedback, Finset.card_image_of_injective _ Sum.inl_injective]

theorem privateScope_injective (f : ℕ) : Function.Injective (@privateScope f) := by
  intro s t h
  have hm : Sum.inr s ∈ privateScope t := h ▸ (by simp [privateScope])
  simpa [privateScope] using hm

theorem privatePayoff_nonneg {f : ℕ} (s : State f) (v : Vertex (PrivateCoord f)) :
    0 ≤ privatePayoff s v := by
  exact mul_nonneg (payoff_nonneg _ _) (by simp [vertexPoint]; split_ifs <;> norm_num)

theorem privatePayoff_dependsOn {f : ℕ} (s : State f) :
    DependsOn (privatePayoff s) (privateScope s) := by
  intro v w h
  have hb : v ∘ Sum.inl = w ∘ Sum.inl := by
    funext i
    exact h _ (by simp [privateScope])
  have hp : v (.inr s) = w (.inr s) := h _ (by simp [privateScope])
  simp only [privatePayoff, hb, vertexPoint, hp]

@[simp] theorem privateLocalLaw_means {f : ℕ} (s : State f) :
    HasMeans (privateLocalLaw s) (privateMeans f) := by
  intro i
  cases i with
  | inl i =>
      rw [privateLocalLaw, Law.expect_map]
      exact localLaw_means s i
  | inr t => simp [privateLocalLaw, Law.expect_map, Function.comp_def,
      extendState, vertexPoint, privateMeans]

@[simp] theorem privateLocalLaw_payoff {f : ℕ} (s : State f) :
    (privateLocalLaw s).expect (privatePayoff s) = 1 / 2 := by
  have he : (privatePayoff s) ∘ extendState = payoff s := by
    funext v
    simp [privatePayoff, extendState, Function.comp_def, vertexPoint]
  rw [privateLocalLaw, Law.expect_map, he, localLaw_payoff]

/-- At mean one, each private multiplier preserves the cell expectation. -/
theorem privatePayoff_expect {f : ℕ} (s : State f) (μ : Law (Vertex (PrivateCoord f)))
    (hm : HasMeans μ (privateMeans f)) :
    μ.expect (privatePayoff s) = μ.expect (fun v => payoff s (v ∘ Sum.inl)) := by
  have hlo : ∀ v : Vertex (PrivateCoord f),
      privatePayoff s v ≤ payoff s (v ∘ Sum.inl) := by
    intro v
    unfold privatePayoff payoff vertexPoint
    split_ifs <;> norm_num
  have hhi : ∀ v : Vertex (PrivateCoord f),
      payoff s (v ∘ Sum.inl) ≤ privatePayoff s v + (1 - vertexPoint v (.inr s)) := by
    intro v
    unfold privatePayoff payoff vertexPoint
    split_ifs <;> norm_num
  apply le_antisymm (μ.expect_mono hlo)
  have h := μ.expect_mono hhi
  simpa only [Law.expect_add, Law.expect_sub, Law.expect_const,
    hm (.inr s), privateMeans, Sum.elim_inr, sub_self, add_zero] using h

theorem private_local_optimum {f : ℕ} (s : State f) :
    IsGreatest {r : ℝ | ∃ μ : Law (Vertex (PrivateCoord f)),
      HasMeans μ (privateMeans f) ∧ μ.expect (privatePayoff s) = r} (1 / 2) := by
  refine ⟨⟨privateLocalLaw s, privateLocalLaw_means s, privateLocalLaw_payoff s⟩, ?_⟩
  rintro r ⟨μ, hm, rfl⟩
  rw [privatePayoff_expect s μ hm]
  let ν := μ.map (fun v => v ∘ Sum.inl)
  have hn : HasMeans ν (fun _ => 1 / 2) := by
    intro i
    simpa [ν, Law.expect_map, Function.comp_def, vertexPoint, privateMeans]
      using hm (.inl i)
  simpa only [ν, Law.expect_map, Function.comp_def] using payoff_upper s ν hn

theorem private_sum_expectations {f : ℕ} (μ : Law (Vertex (PrivateCoord f)))
    (hm : HasMeans μ (privateMeans f)) :
    ∑ s : State f, μ.expect (privatePayoff s) = 1 := by
  simp_rw [privatePayoff_expect _ μ hm]
  rw [← Law.expect_sum]
  simp

theorem private_retention_le (f : ℕ) (c : ℝ) (μ : Law (Vertex (PrivateCoord f)))
    (hm : HasMeans μ (privateMeans f))
    (h : ∀ s : State f, c * (privateLocalLaw s).expect (privatePayoff s) ≤
      μ.expect (privatePayoff s)) : c ≤ (1 / 2 : ℝ)^f := by
  have hs := Finset.sum_le_sum (s := Finset.univ) (fun s _ => h s)
  simp only [privateLocalLaw_payoff, ← Finset.mul_sum, sum_local_optima,
    private_sum_expectations μ hm] at hs
  have hp : (0 : ℝ) < 2^f := by positivity
  have hpow : (1 / 2 : ℝ)^f * 2^f = 1 := by rw [← mul_pow]; norm_num
  nlinarith

def privateResidualGraph (f : ℕ) : SimpleGraph (PrivateCoord f ⊕ State f) :=
  StructuralTreewidth.incidenceGraph (fun i s => i ∈ privateScope s \ privateFeedback f)

private theorem private_factor_neighbor {f : ℕ} (s : State f) (v : PrivateCoord f ⊕ State f)
    (h : (privateResidualGraph f).Adj (.inr s) v) :
    v = .inl (.inl none) ∨ v = .inl (.inr s) := by
  cases v with
  | inr t => exact False.elim h
  | inl i =>
    cases i with
    | inl i =>
      cases i with
      | none => exact Or.inl rfl
      | some i => simp [privateResidualGraph, StructuralTreewidth.incidenceGraph,
          privateScope, privateFeedback, feedback] at h
    | inr t =>
      right
      simpa [privateResidualGraph, StructuralTreewidth.incidenceGraph,
        privateScope, privateFeedback] using h

private theorem private_variable_neighbor {f : ℕ} (s : State f)
    (v : PrivateCoord f ⊕ State f)
    (h : (privateResidualGraph f).Adj (.inl (.inr s)) v) : v = .inr s := by
  cases v with
  | inl i => exact False.elim h
  | inr t =>
    simpa [privateResidualGraph, StructuralTreewidth.incidenceGraph,
      privateScope, privateFeedback, eq_comm] using h

private theorem private_no_leaf_cycle {f : ℕ} (s : State f)
    (p : (privateResidualGraph f).Walk (.inl (.inr s)) (.inl (.inr s))) : ¬ p.IsCycle := by
  intro hp
  exact hp.snd_ne_penultimate
    ((private_variable_neighbor s _ (p.adj_snd hp.not_nil)).trans
      (private_variable_neighbor s _ (p.adj_penultimate hp.not_nil).symm).symm)

private theorem private_no_factor_cycle {f : ℕ} (s : State f)
    (p : (privateResidualGraph f).Walk (.inr s) (.inr s)) : ¬ p.IsCycle := by
  intro hp
  have hs : p.snd = .inl (.inl none) := by
    rcases private_factor_neighbor s _ (p.adj_snd hp.not_nil) with h | h
    · exact h
    · have hc : ∃ q : (privateResidualGraph f).Walk p.snd p.snd, q.IsCycle :=
        ⟨_, hp.rotate (p.getVert_mem_support 1)⟩
      rw [h] at hc
      obtain ⟨q, hq⟩ := hc
      exact False.elim (private_no_leaf_cycle s q hq)
  have ht : p.penultimate = .inl (.inl none) := by
    rcases private_factor_neighbor s _ (p.adj_penultimate hp.not_nil).symm with h | h
    · exact h
    · have hc : ∃ q : (privateResidualGraph f).Walk p.penultimate p.penultimate, q.IsCycle :=
        ⟨_, hp.rotate (p.getVert_mem_support (p.length - 1))⟩
      rw [h] at hc
      obtain ⟨q, hq⟩ := hc
      exact False.elim (private_no_leaf_cycle s q hq)
  exact hp.snd_ne_penultimate (hs.trans ht.symm)

/-- Distinct genuine scopes retain the required forest after feedback deletion. -/
theorem private_residual_incidence_acyclic (f : ℕ) : (privateResidualGraph f).IsAcyclic := by
  intro v p hp
  cases v with
  | inr s => exact private_no_factor_cycle s p hp
  | inl i =>
    have ha := p.adj_snd hp.not_nil
    have hc : ∃ q : (privateResidualGraph f).Walk p.snd p.snd, q.IsCycle :=
      ⟨_, hp.rotate (p.getVert_mem_support 1)⟩
    cases he : p.snd with
    | inl j => rw [he] at ha; exact False.elim ha
    | inr s =>
      rw [he] at hc
      obtain ⟨q, hq⟩ := hc
      exact private_no_factor_cycle s q hq

end
end MultilinearGap.StructuralFeedbackPayoffSharpness
