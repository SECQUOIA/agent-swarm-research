import Formal.NetworkSimplex.ThresholdMerge

/-! Only observed simplex labels remain separate; all unused labels and the residual merge. -/
namespace NetworkSimplex
open scoped BigOperators

variable {E V O : Type*} {m : ℕ}

/-- One merged residual state and one state for each observed original label. -/
def observedGroup (J : Finset (Fin m)) : Fin (m + 1) → Option {j // j ∈ J} :=
  Fin.cases none (fun j => if h : j ∈ J then some ⟨j, h⟩ else none)

theorem observedGroup_succ (J : Finset (Fin m)) (j : {j // j ∈ J}) :
    observedGroup J j.val.succ = some j := by simp [observedGroup, j.property]

theorem observedGroup_fiber (J : Finset (Fin m)) (j : {j // j ∈ J})
    (k : Fin (m + 1)) : observedGroup J k = some j ↔ k = j.val.succ := by
  refine Fin.cases ?_ (fun i => ?_) k
  · simp only [observedGroup, Fin.cases_zero, reduceCtorEq, false_iff]
    exact (Fin.succ_ne_zero _).symm
  · by_cases hi : i ∈ J
    · simp [observedGroup, hi, Subtype.ext_iff]
    · simp only [observedGroup, Fin.cases_succ, dif_neg hi, reduceCtorEq, false_iff,
        Fin.succ_inj]
      intro he
      exact hi (he.symm ▸ j.property)

theorem observed_weight {w : Fin (m + 1) → ℝ} (J : Finset (Fin m))
    (j : {j // j ∈ J}) : groupSum (observedGroup J) w (some j) = w j.val.succ := by
  classical
  simp only [groupSum, observedGroup_fiber]
  simp

theorem merged_residual_weight (J : Finset (Fin m)) (w : Fin (m + 1) → ℝ)
    (hw : Simplex w) :
    groupSum (observedGroup J) w none = 1 - ∑ j : {j // j ∈ J}, w j.val.succ := by
  have hs := (simplex_groupSum (observedGroup J) hw).2
  rw [Fintype.sum_option] at hs
  simp only [observed_weight] at hs
  linarith

theorem observed_state_count (J : Finset (Fin m)) :
    Fintype.card (Option {j // j ∈ J}) = J.card + 1 := by simp

theorem three_observed_states (J : Finset (Fin m)) (h : J.card ≤ 3) :
    Fintype.card (Option {j // j ∈ J}) ≤ 4 := by rw [observed_state_count]; omega

theorem two_observed_states (J : Finset (Fin m)) (h : J.card ≤ 2) :
    Fintype.card (Option {j // j ∈ J}) ≤ 3 := by rw [observed_state_count]; omega

/-- This is an exact original-coordinate hull reduction for arbitrarily many
unobserved labels. Original nonnegativity constraints are retained. -/
theorem original_hull_observed_merge_iff (J : Finset (Fin m))
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (hJ : ∀ o, label o ∈ J)
    (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      OriginalSimplex p.2.1 ∧
      mergedPoint (observedGroup J) (liftPoint p) ∈
        convexHull ℝ (Graph A b u arc (fun o => some ⟨label o, hJ o⟩)) := by
  rw [original_hull_iff_lift]
  have hobs : ∀ o k, observedGroup J k = observedGroup J (label o).succ → k = (label o).succ := by
    intro o k hk
    have hh := observedGroup_succ J ⟨label o, hJ o⟩
    rw [hh] at hk
    exact (observedGroup_fiber J ⟨label o, hJ o⟩ k).mp hk
  rw [hull_merge_iff (observedGroup J) hobs]
  have hs : (observedGroup J ∘ fun o => (label o).succ) =
      (fun o => some ⟨label o, hJ o⟩) := by
    funext o
    exact observedGroup_succ J ⟨label o, hJ o⟩
  rw [hs]
  exact and_congr_left' (residualWeights_simplex p.2.1)

/-- A reduced linear cut changes only its simplex coefficients under substitution. -/
theorem merged_cut_pullback {K L : Type*} [Fintype K] [Fintype L] [DecidableEq L]
    [Fintype E] [Fintype O] (g : K → L) (α : E → ℝ) (β : L → ℝ) (γ : O → ℝ)
    (p : Point E K O) :
    (∑ e, α e * (mergedPoint g p).1 e) +
      (∑ l, β l * (mergedPoint g p).2.1 l) +
      (∑ o, γ o * (mergedPoint g p).2.2 o) =
    (∑ e, α e * p.1 e) + (∑ k, β (g k) * p.2.1 k) + (∑ o, γ o * p.2.2 o) := by
  congr 2
  simp only [mergedPoint, groupSum, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro k _
  simp [mul_ite]

/-- Eliminating the merged residual substitutes only a constant and simplex terms. -/
theorem observed_cut_simplex_substitution (J : Finset (Fin m)) (y : Fin m → ℝ)
    (hy : OriginalSimplex y) (β : Option {j // j ∈ J} → ℝ) :
    (∑ l, β l * groupSum (observedGroup J) (residualWeights y) l) =
      β none + ∑ j : {j // j ∈ J}, (β (some j) - β none) * y j.val := by
  rw [Fintype.sum_option, merged_residual_weight J _ ((residualWeights_simplex y).mpr hy)]
  simp only [observed_weight, residualWeights, Fin.cons_succ, sub_mul,
    Finset.sum_sub_distrib, ← Finset.mul_sum]
  ring

/-- With no observed products the hull is exactly the independent flow/simplex product. -/
theorem original_hull_no_observations [IsEmpty O]
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      Flow A b u 1 p.1 ∧ OriginalSimplex p.2.1 := by
  constructor
  · intro hp
    obtain ⟨hy, f, hf, hs, _⟩ := (original_mem_hull_iff A b u arc label p).mp hp
    have hsum := flow_finset_sum Finset.univ (residualWeights p.2.1) f (fun k _ => hf k)
    rw [(residualWeights_simplex p.2.1).mpr hy |>.2, hs] at hsum
    exact ⟨hsum, hy⟩
  · rintro ⟨hx, hy⟩
    apply subset_convexHull
    exact ⟨hy, hx, fun o => isEmptyElim o⟩

theorem original_hull_zero_observed (J : Finset (Fin m)) (hcard : J.card = 0)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (label : O → Fin m) (hJ : ∀ o, label o ∈ J)
    (p : OriginalPoint E O m) :
    p ∈ convexHull ℝ (OriginalGraph A b u arc label) ↔
      Flow A b u 1 p.1 ∧ OriginalSimplex p.2.1 := by
  have hJ0 : J = ∅ := Finset.card_eq_zero.mp hcard
  let : IsEmpty O := ⟨fun o => by simpa only [hJ0, Finset.notMem_empty] using hJ o⟩
  exact original_hull_no_observations A b u arc label p

end NetworkSimplex
