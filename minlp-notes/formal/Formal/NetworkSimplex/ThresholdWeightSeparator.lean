import Formal.NetworkSimplex.ThresholdDomainOracle

/-! A linear-cost separator for all original simplex weights, including residual. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open RationalData

abbrev WeightCut (m : ℕ) := Fin (m + 1) ⊕ Bool

def WeightCut.value {m : ℕ} (cut : WeightCut m) (w : Fin (m + 1) → ℝ) : ℝ :=
  match cut with
  | .inl j => w j
  | .inr b => if b then (∑ j, w j) - 1 else 1 - ∑ j, w j

def weightCutValues {m : ℕ} (w : Fin (m + 1) → ℚ) : List (WeightCut m × ℚ) :=
  let ws := List.ofFn w
  let total := ws.sum
  (List.ofFn fun j => (Sum.inl j, w j)) ++
    [(Sum.inr true, total - 1), (Sum.inr false, 1 - total)]

def weightSeparator {m : ℕ} (w : Fin (m + 1) → ℚ) : Option (WeightCut m) × ℕ :=
  let scan := negativeCutRun (weightCutValues w)
  (scan.1, scan.2 + (m + 1) + 2)

theorem weightSeparator_none {m : ℕ} (w : Fin (m + 1) → ℚ) :
    (weightSeparator w).1 = none ↔ Simplex (fun j => (w j : ℝ)) := by
  rw [weightSeparator, negativeCutRun_none]
  simp only [weightCutValues, List.forall_mem_append, List.mem_ofFn,
    forall_exists_index, forall_apply_eq_imp_iff, List.forall_mem_cons, List.sum_ofFn,
    List.not_mem_nil, false_implies, implies_true, and_true]
  unfold Simplex
  dsimp only
  constructor
  · rintro ⟨hn,hlo,hhi⟩
    have he : ∑ j, w j = 1 := by linarith
    exact ⟨fun j => by exact_mod_cast hn j, by exact_mod_cast he⟩
  · rintro ⟨hn,hs⟩
    have he : ∑ j, w j = 1 := by exact_mod_cast hs
    exact ⟨fun j => by exact_mod_cast hn j, by simp [he], by simp [he]⟩

theorem weightSeparator_some {m : ℕ} (w : Fin (m + 1) → ℚ) {cut : WeightCut m}
    (h : (weightSeparator w).1 = some cut) :
    cut.value (fun j => (w j : ℝ)) < 0 ∧
      ∀ v : Fin (m + 1) → ℝ, Simplex v → 0 ≤ cut.value v := by
  obtain ⟨q,hq,hn⟩ := negativeCutRun_some (weightCutValues w) h
  have hv : (q : ℝ) = cut.value (fun j => (w j : ℝ)) := by
    simp only [weightCutValues, List.mem_append, List.mem_ofFn, List.sum_ofFn,
      List.mem_cons, List.not_mem_nil, or_false] at hq
    rcases hq with ⟨j,hj⟩ | ht | hf
    · cases hj
      rfl
    · cases ht
      simp [WeightCut.value]
    · cases hf
      simp [WeightCut.value]
  constructor
  · rw [← hv]; exact_mod_cast hn
  · intro v hs
    cases cut with
    | inl j => exact hs.1 j
    | inr b => cases b <;> simp [WeightCut.value, hs.2]

theorem weightSeparator_work {m : ℕ} (w : Fin (m + 1) → ℚ) :
    (weightSeparator w).2 = 2 * m + 6 := by
  simp [weightSeparator, negativeCutRun_charge, weightCutValues]
  omega

/-- A weight certificate is literally affine and has no flow or product terms. -/
def WeightCut.expression {m L : ℕ} : WeightCut m → AffineExpression (Coordinate m (Fin L))
  | .inl j => .variable (.weight j)
  | .inr b => if b then simplexExpression else .neg simplexExpression

theorem WeightCut.expression_eval {m L : ℕ} (cut : WeightCut m)
    (D : ReductionData m (Fin L)) :
    cut.expression.eval (coordinates D D.xb) = cut.value D.weights := by
  cases cut with
  | inl j => rfl
  | inr b => cases b <;> simp [WeightCut.expression, WeightCut.value,
      simplexExpression, AffineExpression.eval, AffineExpression.eval_sum, coordinates] <;> ring

end NetworkSimplex.Chain.Threshold
