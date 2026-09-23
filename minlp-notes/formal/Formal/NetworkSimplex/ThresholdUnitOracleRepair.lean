import Formal.NetworkSimplex.ThresholdUnitDescription

/-! Executable balance repair, including the search for an actual gadget. -/
namespace NetworkSimplex.Chain.Threshold

def findFlowCoefficient {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L)))
    (target : ℤ) : List (Fin L) → Option (Fin L) × ℕ
  | [] => (none, 0)
  | i :: rest =>
      if e.coefficient (.aFlow i) = target then (some i, 1)
      else let tail := findFlowCoefficient e target rest
           (tail.1, tail.2 + 1)

theorem findFlowCoefficient_spec {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L)))
    (target : ℤ) (is : List (Fin L)) :
    (findFlowCoefficient e target is).2 ≤ is.length ∧
    (∀ i, (findFlowCoefficient e target is).1 = some i →
      i ∈ is ∧ e.coefficient (.aFlow i) = target) ∧
    ((findFlowCoefficient e target is).1 = none ↔
      ∀ i ∈ is, e.coefficient (.aFlow i) ≠ target) := by
  induction is with
  | nil => simp [findFlowCoefficient]
  | cons i is ih =>
    by_cases hi : e.coefficient (.aFlow i) = target
    · simp [findFlowCoefficient, hi]
    · simp only [findFlowCoefficient, hi, ↓reduceIte, List.length_cons]
      refine ⟨by omega, ?_, ?_⟩
      · intro j hj
        exact ⟨List.mem_cons_of_mem i (ih.2.1 j hj).1, (ih.2.1 j hj).2⟩
      · simpa [hi] using ih.2.2

def Repairable {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L))) : Prop :=
  (-2 ≤ e.coefficient .bypassFlow ∧ e.coefficient .bypassFlow ≤ 2) ∧
  (∀ i, -1 ≤ e.coefficient (.aFlow i) ∧ e.coefficient (.aFlow i) ≤ 1) ∧
  (∀ i, e.coefficient (.bFlow i) = 0) ∧
  (∀ z, NonFlow z → FlowOrProduct z → -1 ≤ e.coefficient z ∧ e.coefficient z ≤ 1) ∧
  (e.coefficient .bypassFlow = -2 → ∃ i, e.coefficient (.aFlow i) = -1) ∧
  (e.coefficient .bypassFlow = 2 → ∃ i, e.coefficient (.aFlow i) = 1)

/-- The ledger counts coefficient queries/comparisons, including the bypass tests. -/
def unitRepair {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L))) :
    Option (AffineExpression (Coordinate 3 (Fin L))) × ℕ :=
  if e.coefficient .bypassFlow = -2 then
    let found := findFlowCoefficient e (-1) (List.finRange L)
    (found.1.map (fun i => balanceRepair e i true), found.2 + 1)
  else if e.coefficient .bypassFlow = 2 then
    let found := findFlowCoefficient e 1 (List.finRange L)
    (found.1.map (fun i => balanceRepair e i false), found.2 + 2)
  else (some e, 2)

theorem unitRepair_cost {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L))) :
    (unitRepair e).2 ≤ L + 2 := by
  have hm := (findFlowCoefficient_spec e (-1) (List.finRange L)).1
  have hp := (findFlowCoefficient_spec e 1 (List.finRange L)).1
  simp only [List.length_finRange] at hm hp
  unfold unitRepair
  split_ifs <;> dsimp <;> omega

private theorem repair_nonflow_unit {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L)))
    (he : Repairable e) (i : Fin L) (s : Bool) (hf : UnitFlow (balanceRepair e i s)) :
    UnitFlowProducts (balanceRepair e i s) := by
  intro z hz
  cases z with
  | bypassFlow => exact hf.1
  | aFlow j => exact hf.2.1 j
  | bFlow j => exact hf.2.2 j
  | aProduct j k =>
    rw [balanceRepair_nonFlow e i s (.aProduct j k) trivial]
    exact he.2.2.2.1 _ trivial hz
  | bProduct j k =>
    rw [balanceRepair_nonFlow e i s (.bProduct j k) trivial]
    exact he.2.2.2.1 _ trivial hz
  | bypassProduct k =>
    rw [balanceRepair_nonFlow e i s (.bypassProduct k) trivial]
    exact he.2.2.2.1 _ trivial hz
  | weight k => exact False.elim hz

theorem unitRepair_correct {L : ℕ} (e : AffineExpression (Coordinate 3 (Fin L)))
    (he : Repairable e) :
    ∃ out, (unitRepair e).1 = some out ∧ UnitFlowProducts out ∧
      ∀ x, (∀ i, (balanceExpression i).eval x = 0) → out.eval x = e.eval x := by
  by_cases hn : e.coefficient .bypassFlow = -2
  · obtain ⟨i, hi⟩ := he.2.2.2.2.1 hn
    have hs := findFlowCoefficient_spec e (-1) (List.finRange L)
    cases ht : (findFlowCoefficient e (-1) (List.finRange L)).1 with
    | none => exact False.elim (((hs.2.2.mp ht) i (by simp)) hi)
    | some j =>
      have hj := (hs.2.1 j ht).2
      obtain ⟨hh, ha, hb⟩ := balanceRepair_add_unit e j hn hj he.2.1 he.2.2.1
      refine ⟨balanceRepair e j true, ?_, ?_, ?_⟩
      · simp [unitRepair, hn, ht]
      · exact repair_nonflow_unit e he j true ⟨by simp [hh], ha, hb⟩
      · exact fun x hx => balanceRepair_eval e j true x (hx j)
  · by_cases hp : e.coefficient .bypassFlow = 2
    · obtain ⟨i, hi⟩ := he.2.2.2.2.2 hp
      have hs := findFlowCoefficient_spec e 1 (List.finRange L)
      cases ht : (findFlowCoefficient e 1 (List.finRange L)).1 with
      | none => exact False.elim (((hs.2.2.mp ht) i (by simp)) hi)
      | some j =>
        have hj := (hs.2.1 j ht).2
        obtain ⟨hh, ha, hb⟩ := balanceRepair_sub_unit e j hp hj he.2.1 he.2.2.1
        refine ⟨balanceRepair e j false, ?_, ?_, ?_⟩
        · simp [unitRepair, hp, ht]
        · exact repair_nonflow_unit e he j false ⟨by simp [hh], ha, hb⟩
        · exact fun x hx => balanceRepair_eval e j false x (hx j)
    · refine ⟨e, by simp [unitRepair, hn, hp], ?_, fun _ _ => rfl⟩
      intro z hz
      cases z with
      | bypassFlow => have h := he.1; omega
      | aFlow i => exact he.2.1 i
      | bFlow i => simp [he.2.2.1 i]
      | aProduct i j => exact he.2.2.2.1 _ trivial hz
      | bProduct i j => exact he.2.2.2.1 _ trivial hz
      | bypassProduct j => exact he.2.2.2.1 _ trivial hz
      | weight j => exact False.elim hz

theorem circuitExpression_repairable {L : ℕ} (D : ReductionData 3 (Fin L))
    {c : Fin 16} {r : Fin 11 → ProfileRow 3 (Fin L)} (hr : ThreeBranch D c r) :
    Repairable (circuitExpression D c r) := by
  have hc := circuitExpression_coefficient D c r
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [hc, circuit_bypass_eq D hr]
    rcases bypass_cases r c with hu | ⟨_, hn, _⟩ | ⟨_, hp, _⟩ <;> omega
  · intro i
    rw [hc]
    exact circuit_aFlow_unit D hr i
  · intro i
    rw [hc, circuit_bFlow]
  · intro z hn hz
    rw [hc]
    cases z with
    | bypassFlow => exact False.elim hn
    | aFlow i => exact False.elim hn
    | bFlow i => exact False.elim hn
    | aProduct i j => exact threeBranch_aProduct_unit D c r hr i j
    | bProduct i j => exact threeBranch_bProduct_unit D c r hr i j
    | bypassProduct j => exact threeBranch_bypassProduct_unit D c r hr j
    | weight j => exact False.elim hz
  · intro h
    rw [hc] at h
    obtain ⟨i, _, hi⟩ := negative_bypass_witness D hr h
    exact ⟨i, (hc _).trans hi⟩
  · intro h
    rw [hc] at h
    obtain ⟨i, _, hi⟩ := positive_bypass_witness D hr h
    exact ⟨i, (hc _).trans hi⟩

/-- Repairability depends only on the represented affine coefficients. -/
theorem Repairable.congr {L : ℕ} {e f : AffineExpression (Coordinate 3 (Fin L))}
    (h : ∀ z, e.coefficient z = f.coefficient z) (hf : Repairable f) : Repairable e := by
  simpa only [Repairable, h] using hf

/-- Every single source row needs no balance repair. -/
theorem rowExpression_repairable {L : ℕ} (D : ReductionData 3 (Fin L))
    (r : ProfileRow 3 (Fin L)) : Repairable (rowExpression D r) := by
  have hu := row_flow_product_unit D r
  have hh := hu .bypassFlow trivial
  change -1 ≤ (rowExpression D r).coefficient .bypassFlow ∧
    (rowExpression D r).coefficient .bypassFlow ≤ 1 at hh
  refine ⟨by omega, fun i => hu (.aFlow i) trivial, ?_, ?_, ?_, ?_⟩
  · intro i
    exact row_bFlow_coefficient D r i
  · intro z _ hz
    exact hu z hz
  · intro h
    omega
  · intro h
    omega

end NetworkSimplex.Chain.Threshold
