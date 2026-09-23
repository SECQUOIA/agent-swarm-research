import Formal.NetworkSimplex.ThresholdMergeObserved

/-! Rational proportional refinement and compact recovery for unobserved states. -/
namespace NetworkSimplex
open scoped BigOperators

variable {K L E V : Type*} [Fintype K] [Fintype L] [DecidableEq L]

/-- Rational refinement is an explicit formula, including zero merged weights. -/
def rationalRefine (g : K → L) (w : K → ℚ) (f : L → E → ℚ) (k : K) (e : E) : ℚ :=
  (w k / groupSum g w (g k)) * f (g k) e

omit [Fintype L] in
theorem cast_groupSum (g : K → L) (w : K → ℚ) (l : L) :
    ((groupSum g w l : ℚ) : ℝ) = groupSum g (fun k => (w k : ℝ)) l := by
  unfold groupSum
  push_cast
  apply Finset.sum_congr rfl
  intro k _
  split_ifs <;> simp

omit [Fintype L] in
theorem cast_rationalRefine (g : K → L) (w : K → ℚ) (f : L → E → ℚ) (k : K) :
    (fun e => (rationalRefine g w f k e : ℝ)) =
      proportionalRefine g (fun k => (w k : ℝ)) (fun l e => (f l e : ℝ)) k := by
  funext e
  simp [rationalRefine, proportionalRefine, cast_groupSum]

omit [Fintype L] in
theorem rationalRefine_zero (g : K → L) (w : K → ℚ) (f : L → E → ℚ) (k : K)
    (h : groupSum g w (g k) = 0) : rationalRefine g w f k = 0 := by
  funext e
  simp [rationalRefine, h]

omit [Fintype L] in
theorem rationalRefine_flow (g : K → L) (w : K → ℚ) (f : L → E → ℚ)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (hw : ∀ k, 0 ≤ w k)
    (hf : ∀ l, Flow A b u ((groupSum g w l : ℚ) : ℝ) (fun e => (f l e : ℝ))) (k : K) :
    Flow A b u (w k : ℝ) (fun e => (rationalRefine g w f k e : ℝ)) := by
  rw [cast_rationalRefine]
  apply proportionalRefine_flow
  · intro k; exact_mod_cast hw k
  · intro l; simpa only [cast_groupSum] using hf l

/-- A single normalized flow suffices for every state in one fiber. At zero
merged weight any previously available feasible flow can serve as the default. -/
def commonMergedFlow (g : K → L) (w : K → ℚ) (f : L → E → ℚ) (base : E → ℚ)
    (l : L) (e : E) : ℚ :=
  if groupSum g w l = 0 then base e else f l e / groupSum g w l

omit [Fintype L] in
theorem commonMergedFlow_flow (g : K → L) (w : K → ℚ) (f : L → E → ℚ) (base : E → ℚ)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (hw : ∀ k, 0 ≤ w k)
    (hf : ∀ l, Flow A b u ((groupSum g w l : ℚ) : ℝ) (fun e => (f l e : ℝ)))
    (hbase : Flow A b u 1 (fun e => (base e : ℝ))) (l : L) :
    Flow A b u 1 (fun e => (commonMergedFlow g w f base l e : ℝ)) := by
  by_cases hz : groupSum g w l = 0
  · simpa [commonMergedFlow, hz] using hbase
  · have hn : (0 : ℝ) ≤ (groupSum g w l : ℚ) := by
      rw [cast_groupSum]
      exact groupSum_nonneg g _ (fun k => by exact_mod_cast hw k) l
    have hnz : ((groupSum g w l : ℚ) : ℝ) ≠ 0 := by exact_mod_cast hz
    have hs := flow_smul (hf l) (inv_nonneg.mpr hn)
    have he : (fun e => (commonMergedFlow g w f base l e : ℝ)) =
        (((groupSum g w l : ℚ) : ℝ))⁻¹ • (fun e => (f l e : ℝ)) := by
      funext e
      simp [commonMergedFlow, hz, div_eq_mul_inv, mul_comm]
    rw [he]
    simpa only [inv_mul_cancel₀ hnz] using hs

omit [Fintype L] in
theorem rationalRefine_common_flow (g : K → L) (w : K → ℚ) (f : L → E → ℚ)
    (base : E → ℚ) (hw : ∀ k, 0 ≤ w k) (k : K) (e : E) :
    rationalRefine g w f k e = w k * commonMergedFlow g w f base (g k) e := by
  by_cases hz : groupSum g w (g k) = 0
  · have hk : w k = 0 := by
      have hn := le_groupSum g (fun k => (w k : ℝ)) (fun k => by exact_mod_cast hw k) k
      rw [← cast_groupSum, hz, Rat.cast_zero] at hn
      have hn' : w k ≤ 0 := by exact_mod_cast hn
      exact le_antisymm hn' (hw k)
    simp [rationalRefine, commonMergedFlow, hz, hk]
  · simp only [rationalRefine, commonMergedFlow, if_neg hz]
    ring

/-- The original global weight vector is restored exactly, not an independent
simplex vector for each block. -/
theorem rationalRefine_total (g : K → L) (w : K → ℚ) (f : L → E → ℚ)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (hf : ∀ l, Flow A b u ((groupSum g w l : ℚ) : ℝ) (fun e => (f l e : ℝ))) (e : E) :
    ∑ k, rationalRefine g w f k e = ∑ l, f l e := by
  have hh := proportionalRefine_total g (fun l => by simpa only [cast_groupSum] using hf l)
  have he := congrFun hh e
  simp only [Finset.sum_apply, ← cast_rationalRefine] at he
  exact_mod_cast he

/-- Every unused label and the residual state read the same stored flow. -/
theorem unobserved_same_common_flow {m : ℕ} (J : Finset (Fin m))
    (w : Fin (m + 1) → ℚ) (f : Option {j // j ∈ J} → E → ℚ) (base : E → ℚ)
    (hw : ∀ k, 0 ≤ w k) (k : Fin (m + 1)) (hk : observedGroup J k = none) (e : E) :
    rationalRefine (observedGroup J) w f k e =
      w k * commonMergedFlow (observedGroup J) w f base none e := by
  rw [rationalRefine_common_flow _ _ _ base hw, hk]

omit [Fintype L] in
/-- A feasible rational reduced disaggregation supplies a rational default flow;
no extra feasibility oracle or arbitrary real-valued choice is required. -/
theorem exists_rational_default_flow [Finite L] (g : K → L) (w : K → ℚ) (f : L → E → ℚ)
    (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (hw : Simplex (fun k => (w k : ℝ)))
    (hf : ∀ l, Flow A b u ((groupSum g w l : ℚ) : ℝ) (fun e => (f l e : ℝ))) :
    ∃ base : E → ℚ, Flow A b u 1 (fun e => (base e : ℝ)) := by
  let := Fintype.ofFinite L
  have hs := simplex_groupSum g hw
  have hex : ∃ l, 0 < groupSum g (fun k => (w k : ℝ)) l := by
    by_contra! hn
    have hh := Finset.sum_nonpos (fun l (_ : l ∈ Finset.univ) => hn l)
    linarith [hs.2]
  obtain ⟨l, hl⟩ := hex
  rw [← cast_groupSum] at hl
  refine ⟨fun e => f l e / groupSum g w l, ?_⟩
  have hh := flow_smul (hf l) (inv_nonneg.mpr hl.le)
  have he : (fun e => ((f l e / groupSum g w l : ℚ) : ℝ)) =
      (((groupSum g w l : ℚ) : ℝ))⁻¹ • (fun e => (f l e : ℝ)) := by
    funext e
    simp [div_eq_mul_inv, mul_comm]
  rw [he]
  simpa only [inv_mul_cancel₀ (ne_of_gt hl)] using hh

/-- The actual compact data consist of one flow and a vector of weights. -/
structure CompactRefinement (I E : Type*) where
  weights : I → ℚ
  commonFlow : E → ℚ

def CompactRefinement.expand {I E : Type*} (c : CompactRefinement I E) (i : I) (e : E) : ℚ :=
  c.weights i * c.commonFlow e

def compactUnobserved {m : ℕ} (J : Finset (Fin m)) (w : Fin (m + 1) → ℚ)
    (f : Option {j // j ∈ J} → E → ℚ) (base : E → ℚ) :
    CompactRefinement {k // observedGroup J k = none} E where
  weights k := w k.val
  commonFlow := commonMergedFlow (observedGroup J) w f base none

theorem compactUnobserved_expand {m : ℕ} (J : Finset (Fin m)) (w : Fin (m + 1) → ℚ)
    (f : Option {j // j ∈ J} → E → ℚ) (base : E → ℚ) (hw : ∀ k, 0 ≤ w k)
    (k : {k // observedGroup J k = none}) (e : E) :
    (compactUnobserved J w f base).expand k e = rationalRefine (observedGroup J) w f k.val e :=
  (unobserved_same_common_flow J w f base hw k.val k.property e).symm

/-- Dense recovery emits one entry per state/arc pair. The compact representation
stores the common flow once, alongside the constituent weights. -/
def compactRecoverySize (states arcs : ℕ) : ℕ := states + arcs

def denseRecoverySize (states arcs : ℕ) : ℕ := states * arcs

theorem compact_recovery_cardinality [Fintype E] :
    Fintype.card (K ⊕ E) = compactRecoverySize (Fintype.card K) (Fintype.card E) := by
  simp [compactRecoverySize]

theorem dense_recovery_cardinality [Fintype E] :
    Fintype.card (K × E) = denseRecoverySize (Fintype.card K) (Fintype.card E) := by
  simp [denseRecoverySize]

end NetworkSimplex
