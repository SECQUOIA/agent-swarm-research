import Formal.NetworkSimplex.ThresholdDomainCheck

/-! Explicit finite traversal and arithmetic accounting for the domain precheck. -/
namespace NetworkSimplex.Chain.Threshold
namespace RationalData
variable {m L : ℕ}

/-- Every generated margin is checked, including zero placeholders for absent observations. -/
def domainMargins (D : RationalData m L) : List ℚ :=
  List.ofFn D.weights ++ [D.xh, 1 - D.xh] ++
    (List.ofFn fun i => let xb := D.oppositeFlow i
      [D.xa i, 1 - D.xa i, xb, 1 - xb]).flatten ++
    (List.ofFn fun i => List.ofFn fun j => if observesA (D.c i j) then D.u i j else 0).flatten ++
    (List.ofFn fun i => List.ofFn fun j => if observesB (D.c i j) then D.v i j else 0).flatten ++
    List.ofFn (fun j => if D.observedH j then D.zh j else 0)

theorem domainMargins_nonneg (D : RationalData m L) :
    (∀ q ∈ D.domainMargins, 0 ≤ q) ↔
      (∀ j, 0 ≤ D.weights j) ∧ (0 ≤ D.xh ∧ D.xh ≤ 1) ∧
      (∀ i, (0 ≤ D.xa i ∧ D.xa i ≤ 1) ∧
        (0 ≤ D.oppositeFlow i ∧ D.oppositeFlow i ≤ 1)) ∧
      (∀ i j, observesA (D.c i j) → 0 ≤ D.u i j) ∧
      (∀ i j, observesB (D.c i j) → 0 ≤ D.v i j) ∧
      (∀ j, D.observedH j = true → 0 ≤ D.zh j) := by
  have flatten_all (ls : List (List ℚ)) :
      (∀ q ∈ ls.flatten, 0 ≤ q) ↔ ∀ l ∈ ls, ∀ q ∈ l, 0 ≤ q := by
    simp only [List.mem_flatten, forall_exists_index, and_imp]
    constructor
    · intro h l hl q hq; exact h q l hl hq
    · intro h q l hl hq; exact h l hl q hq
  simp only [domainMargins, List.forall_mem_append, flatten_all,
    List.forall_mem_ofFn_iff, List.forall_mem_cons, sub_nonneg]
  have if_nonneg (p : Prop) [Decidable p] (q : ℚ) :
      (0 ≤ if p then q else 0) ↔ (p → 0 ≤ q) := by
    split_ifs <;> simp_all
  simp only [if_nonneg, List.not_mem_nil, false_implies, implies_true, and_true]
  simp only [and_assoc]

/-- Pair recursion forces one check for every generated margin. -/
def checkMargins : List ℚ → Bool × ℕ
  | [] => (true, 0)
  | q :: qs => let rest := checkMargins qs
      (decide (0 ≤ q) && rest.1, 1 + rest.2)

theorem checkMargins_spec (qs : List ℚ) :
    ((checkMargins qs).1 = true ↔ ∀ q ∈ qs, 0 ≤ q) ∧
      (checkMargins qs).2 = qs.length := by
  induction qs with
  | nil => simp [checkMargins]
  | cons q qs ih => simp [checkMargins, ih.1, ih.2, Nat.add_comm]

def weightSum : List ℚ → ℚ × ℕ
  | [] => (0, 0)
  | q :: qs => let rest := weightSum qs
      (q + rest.1, 1 + rest.2)

theorem weightSum_spec (qs : List ℚ) :
    (weightSum qs).1 = qs.sum ∧ (weightSum qs).2 = qs.length := by
  induction qs with
  | nil => simp [weightSum]
  | cons q qs ih => simp [weightSum, ih.1, ih.2, Nat.add_comm]

/-- The remaining charge is four subtractions per gadget, the bypass margin,
and the final simplex equality comparison. Observation gates and indexing are separate. -/
def domainRun (D : RationalData m L) : Bool × ℕ :=
  let margins := checkMargins D.domainMargins
  let weights := weightSum (List.ofFn D.weights)
  (margins.1 && decide (weights.1 = 1), margins.2 + weights.2 + 4 * L + 2)

theorem domainRun_correct (D : RationalData m L) :
    (D.domainRun).1 = true ↔ D.toReal.OriginalDomain := by
  rw [← D.domainChecks_iff]
  simp only [domainRun, Bool.and_eq_true, decide_eq_true_eq,
    (checkMargins_spec _).1, (weightSum_spec _).1, domainMargins_nonneg, DomainChecks]
  tauto

theorem domainMargins_length (D : RationalData m L) :
    D.domainMargins.length = 2 * (m + 1) * L + 4 * L + 2 * (m + 1) + 2 := by
  simp [domainMargins, List.length_flatten, List.map_ofFn, List.sum_ofFn,
    Finset.sum_const, mul_comm]
  ring

theorem domainRun_charge (D : RationalData m L) :
    D.domainRun.2 = 2 * (m + 1) * L + 8 * L + 3 * (m + 1) + 4 := by
  simp only [domainRun, (checkMargins_spec _).2, (weightSum_spec _).2,
    domainMargins_length, List.length_ofFn]
  ring

end RationalData
end NetworkSimplex.Chain.Threshold
