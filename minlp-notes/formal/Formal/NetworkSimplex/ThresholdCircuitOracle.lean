import Formal.NetworkSimplex.ThresholdGrouping

/-! Executable rational circuit tests retaining the selected original row identifiers. -/
namespace NetworkSimplex.ThresholdOracle

/-- A sparse circuit contains normal keys and nonnegative integer weights. -/
abbrev Circuit (K : ℕ) := List (Fin K × ℕ)

/-- Missing directions disable the circuit. Zero weights do not require a present row. -/
def selectTerms {K : ℕ} {α : Type*} (table : Fin K → Option α) :
    Circuit K → Option (List (ℕ × α))
  | [] => some []
  | (key, weight) :: rest =>
      if weight = 0 then selectTerms table rest else
        match table key, selectTerms table rest with
        | some row, some tail => some ((weight, row) :: tail)
        | _, _ => none

def weightedValue {α : Type*} (rhs : α → ℚ) (rows : List (ℕ × α)) : ℚ :=
  (rows.map (fun t => (t.1 : ℚ) * rhs t.2)).sum

/-- The actual circuit scan: select the minimizing original rows and return the
first strictly negative weighted right-hand side. Its count charges the rational
multiplications, additions, and final comparison used by each present circuit. -/
def circuitOracle {K : ℕ} {α : Type*} (table : Fin K → Option α) (rhs : α → ℚ) :
    List (Circuit K) → Option (List (ℕ × α)) × ℕ
  | [] => (none, 0)
  | c :: cs =>
      match selectTerms table c with
      | none => circuitOracle table rhs cs
      | some rows =>
          if weightedValue rhs rows < 0 then (some rows, 2 * rows.length + 1)
          else let result := circuitOracle table rhs cs
               (result.1, result.2 + 2 * rows.length + 1)

theorem selectTerms_length {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (c : Circuit K) {rows : List (ℕ × α)} (h : selectTerms table c = some rows) :
    rows.length ≤ c.length := by
  induction c generalizing rows with
  | nil => simp [selectTerms] at h; subst rows; simp
  | cons term cs ih =>
    rcases term with ⟨key, weight⟩
    by_cases hw : weight = 0
    · simp only [selectTerms, hw, ↓reduceIte] at h
      exact (ih h).trans (by simp)
    · simp only [selectTerms, hw, ↓reduceIte] at h
      cases ht : table key <;> simp only [ht] at h
      · cases h
      · cases hs : selectTerms table cs <;> simp only [hs] at h
        · cases h
        · simp only [Option.some.injEq] at h
          subst rows
          simp only [List.length_cons]
          exact Nat.succ_le_succ (ih hs)

/-- The successful selection uses exactly the original-key rows supplied by the table. -/
theorem selectTerms_rows {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (c : Circuit K) {rows : List (ℕ × α)} (h : selectTerms table c = some rows)
    {weight : ℕ} {row : α} (hr : (weight, row) ∈ rows) :
    0 < weight ∧ ∃ key, (key, weight) ∈ c ∧ table key = some row := by
  induction c generalizing rows with
  | nil => simp [selectTerms] at h; subst rows; simp at hr
  | cons term cs ih =>
    rcases term with ⟨key, w⟩
    by_cases hw : w = 0
    · simp only [selectTerms, hw, ↓reduceIte] at h
      obtain ⟨hp, k, hk, he⟩ := ih h hr
      exact ⟨hp, k, List.mem_cons_of_mem _ hk, he⟩
    · simp only [selectTerms, hw, ↓reduceIte] at h
      cases ht : table key <;> simp only [ht] at h
      · cases h
      · cases hs : selectTerms table cs <;> simp only [hs] at h
        · cases h
        · simp only [Option.some.injEq] at h
          subst rows
          rcases List.mem_cons.mp hr with he | hr
          · cases he
            exact ⟨Nat.pos_of_ne_zero hw, key, List.mem_cons_self, ht⟩
          · obtain ⟨hp, k, hk, he⟩ := ih hs hr
            exact ⟨hp, k, List.mem_cons_of_mem _ hk, he⟩

/-- Selection preserves every weighted scalar expression attached to the normal keys. -/
theorem selectTerms_sum {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (f : α → ℝ) (g : Fin K → ℝ)
    (ht : ∀ key row, table key = some row → f row = g key)
    (c : Circuit K) {rows : List (ℕ × α)} (h : selectTerms table c = some rows) :
    (rows.map (fun t => (t.1 : ℝ) * f t.2)).sum =
      (c.map (fun t => (t.2 : ℝ) * g t.1)).sum := by
  induction c generalizing rows with
  | nil => simp [selectTerms] at h; subst rows; simp
  | cons term cs ih =>
    rcases term with ⟨key, weight⟩
    by_cases hw : weight = 0
    · simp only [selectTerms, hw, ↓reduceIte] at h
      simpa [hw] using ih h
    · simp only [selectTerms, hw, ↓reduceIte] at h
      cases hk : table key <;> simp only [hk] at h
      · cases h
      · cases hs : selectTerms table cs <;> simp only [hs] at h
        · cases h
        · simp only [Option.some.injEq] at h
          subst rows
          simp only [List.map_cons, List.sum_cons]
          rw [ih hs, ht _ _ hk]

/-- Every reported cut is a present library circuit and is strictly violated. -/
theorem circuitOracle_some {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (library : List (Circuit K)) {rows : List (ℕ × α)}
    (h : (circuitOracle table rhs library).1 = some rows) :
    weightedValue rhs rows < 0 ∧ ∃ c ∈ library, selectTerms table c = some rows := by
  induction library with
  | nil => simp [circuitOracle] at h
  | cons c cs ih =>
    unfold circuitOracle at h
    cases hs : selectTerms table c with
    | none =>
      rw [hs] at h
      obtain ⟨hv, d, hd, he⟩ := ih h
      exact ⟨hv, d, List.mem_cons_of_mem _ hd, he⟩
    | some selected =>
      simp only [hs] at h
      split_ifs at h with hv
      · simp only [Option.some.injEq] at h
        subst rows
        exact ⟨hv, c, List.mem_cons_self, hs⟩
      · obtain ⟨hv, d, hd, he⟩ := ih h
        exact ⟨hv, d, List.mem_cons_of_mem _ hd, he⟩

/-- Acceptance means every circuit whose required directions are present passes its exact test. -/
theorem circuitOracle_none_iff {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (library : List (Circuit K)) :
    (circuitOracle table rhs library).1 = none ↔
      ∀ c ∈ library, ∀ rows, selectTerms table c = some rows → 0 ≤ weightedValue rhs rows := by
  induction library with
  | nil => simp [circuitOracle]
  | cons c cs ih =>
    cases hs : selectTerms table c with
    | none => simp [circuitOracle, hs, ih]
    | some rows =>
      by_cases hv : weightedValue rhs rows < 0
      · simp [circuitOracle, hs, hv]
      · simp [circuitOracle, hs, hv, ih, le_of_not_gt hv]

/-- Testing a fixed preprocessed library has cost independent of the number of original rows. -/
theorem circuitOracle_cost {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (rhs : α → ℚ) (library : List (Circuit K)) :
    (circuitOracle table rhs library).2 ≤
      (library.map (fun c => 2 * c.length + 1)).sum := by
  induction library with
  | nil => simp [circuitOracle]
  | cons c cs ih =>
    cases hs : selectTerms table c with
    | none => simpa [circuitOracle, hs] using ih.trans (Nat.le_add_left _ _)
    | some rows =>
      have hl := selectTerms_length table c hs
      simp only [circuitOracle, hs, List.map_cons, List.sum_cons]
      split_ifs <;> dsimp only <;> omega

/-- The returned representation is an original-coordinate affine cut once each
stored row identifier is interpreted by its original affine right-hand side. -/
def realCut {α : Type*} (rhs : α → ℝ) (rows : List (ℕ × α)) : ℝ :=
  (rows.map (fun t => (t.1 : ℝ) * rhs t.2)).sum

@[simp] theorem cast_weightedValue {α : Type*} (rhs : α → ℚ) (rows : List (ℕ × α)) :
    (weightedValue rhs rows : ℝ) = realCut (fun r => (rhs r : ℝ)) rows := by
  simp [weightedValue, realCut, Rat.cast_list_sum, List.map_map, Function.comp_def]

/-- Any selected positive cancellation is valid at every point satisfying the
original rows, independently of which rows minimize their groups at that point. -/
theorem selected_cut_nonnegative {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (normalValue rhs : α → ℝ) (keyValue : Fin K → ℝ)
    (ht : ∀ key row, table key = some row → normalValue row = keyValue key)
    (hf : ∀ key row, table key = some row → normalValue row ≤ rhs row)
    (c : Circuit K) (hc : (c.map (fun t => (t.2 : ℝ) * keyValue t.1)).sum = 0)
    {rows : List (ℕ × α)} (hs : selectTerms table c = some rows) :
    0 ≤ realCut rhs rows := by
  have he := selectTerms_sum table normalValue keyValue ht c hs
  rw [hc] at he
  rw [← he]
  unfold realCut
  apply List.sum_le_sum
  intro term hterm
  obtain ⟨hp, key, _, hkey⟩ := selectTerms_rows table c hs hterm
  exact mul_le_mul_of_nonneg_left (hf key term.2 hkey) (by positivity)

/-- End-to-end certificate soundness: the computed cut is strictly violated at
the rational query and valid at any feasible original-coordinate comparison point. -/
theorem circuitOracle_separates {K : ℕ} {α : Type*} (table : Fin K → Option α)
    (query : α → ℚ) (library : List (Circuit K))
    (normalValue rhs : α → ℝ) (keyValue : Fin K → ℝ)
    (ht : ∀ key row, table key = some row → normalValue row = keyValue key)
    (hf : ∀ key row, table key = some row → normalValue row ≤ rhs row)
    (hc : ∀ c ∈ library, (c.map (fun t => (t.2 : ℝ) * keyValue t.1)).sum = 0)
    {rows : List (ℕ × α)} (hr : (circuitOracle table query library).1 = some rows) :
    realCut (fun row => (query row : ℝ)) rows < 0 ∧ 0 ≤ realCut rhs rows := by
  obtain ⟨hv, c, hmem, hs⟩ := circuitOracle_some table query library hr
  refine ⟨?_, selected_cut_nonnegative table normalValue rhs keyValue ht hf c (hc c hmem) hs⟩
  rw [← cast_weightedValue]
  exact_mod_cast hv

/-- The actual indexed minimum table is computed once, then the fixed circuit library is scanned. -/
def groupedCircuitOracle {K : ℕ} {α : Type*}
    (input : List (ThresholdGrouping.IndexedRow K α)) (library : List (Circuit K)) :
    Option (List (ℕ × ThresholdGrouping.IndexedRow K α)) × ℕ :=
  let grouped := ThresholdGrouping.group input
  let result := circuitOracle grouped.table.get (fun r => r.value) library
  (result.1, grouped.comparisons + result.2)

theorem groupedCircuitOracle_cost {K : ℕ} {α : Type*}
    (input : List (ThresholdGrouping.IndexedRow K α)) (library : List (Circuit K)) :
    (groupedCircuitOracle input library).2 ≤ input.length +
      (library.map (fun c => 2 * c.length + 1)).sum := by
  have hg := (ThresholdGrouping.group_cost input).1
  have hc := circuitOracle_cost (ThresholdGrouping.group input).table.get
    (fun r => r.value) library
  exact Nat.add_le_add hg hc

/-- Every row in an emitted cut is one of the actual input rows, never an inserted box row. -/
theorem groupedCircuitOracle_original_rows {K : ℕ} {α : Type*}
    (input : List (ThresholdGrouping.IndexedRow K α)) (library : List (Circuit K))
    {rows : List (ℕ × ThresholdGrouping.IndexedRow K α)}
    (ho : (groupedCircuitOracle input library).1 = some rows)
    {weight : ℕ} {row : ThresholdGrouping.IndexedRow K α} (hr : (weight, row) ∈ rows) :
    row ∈ input := by
  obtain ⟨_, c, _, hc⟩ := circuitOracle_some (ThresholdGrouping.group input).table.get
    (fun r => r.value) library ho
  obtain ⟨_, key, _, hk⟩ := selectTerms_rows _ _ hc hr
  exact (ThresholdGrouping.group_minimum input key hk).1

/-- Separation is valid on every original-row feasible point; selecting minima only
at the query does not impose a hidden restriction on the global cut. -/
theorem groupedCircuitOracle_separates {K : ℕ} {α : Type*}
    (input : List (ThresholdGrouping.IndexedRow K α)) (library : List (Circuit K))
    (valueAt : α → ℝ) (normalValue : Fin K → ℝ)
    (hf : ∀ r ∈ input, normalValue r.key ≤ valueAt r.payload)
    (hc : ∀ c ∈ library, (c.map (fun t => (t.2 : ℝ) * normalValue t.1)).sum = 0)
    {rows : List (ℕ × ThresholdGrouping.IndexedRow K α)}
    (ho : (groupedCircuitOracle input library).1 = some rows) :
    realCut (fun r => (r.value : ℝ)) rows < 0 ∧
      0 ≤ realCut (fun r => valueAt r.payload) rows := by
  apply circuitOracle_separates (ThresholdGrouping.group input).table.get
    (fun r => r.value) library (fun r => normalValue r.key) (fun r => valueAt r.payload)
    normalValue ?_ ?_ hc ho
  · intro key row hr
    rw [(ThresholdGrouping.group_minimum input key hr).2.1]
  · intro key row hr
    exact hf row (ThresholdGrouping.group_minimum input key hr).1

end NetworkSimplex.ThresholdOracle


