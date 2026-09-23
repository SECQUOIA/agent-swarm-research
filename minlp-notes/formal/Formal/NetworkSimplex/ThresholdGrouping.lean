import Mathlib

/-! One-pass indexed minimum grouping of actual input rows. No rows are added. -/
namespace NetworkSimplex.ThresholdGrouping

structure IndexedRow (K : ℕ) (α : Type*) where
  key : Fin K
  value : ℚ
  payload : α

structure Table (K : ℕ) (α : Type*) where
  data : Array (Option (IndexedRow K α))
  size_eq : data.size = K

def Table.get {K : ℕ} {α : Type*} (t : Table K α) (k : Fin K) :
    Option (IndexedRow K α) := t.data[k.val]'(by rw [t.size_eq]; exact k.isLt)

def Table.set {K : ℕ} {α : Type*} (t : Table K α) (k : Fin K)
    (r : Option (IndexedRow K α)) : Table K α where
  data := t.data.set k.val r (by rw [t.size_eq]; exact k.isLt)
  size_eq := (Array.size_set _).trans t.size_eq

theorem Table.get_set {K : ℕ} {α : Type*} (t : Table K α) (i j : Fin K)
    (r : Option (IndexedRow K α)) :
    (t.set i r).get j = if i = j then r else t.get j := by
  simp only [get, set, Array.getElem_set]
  congr 1
  exact propext Fin.val_inj

def empty (K : ℕ) (α : Type*) : Table K α where
  data := Array.replicate K none
  size_eq := Array.size_replicate

@[simp] theorem empty_get (K : ℕ) (α : Type*) (k : Fin K) : (empty K α).get k = none := by
  simp [Table.get, empty]

/-- The comparison count is zero for an absent key and one for a present key.
Both branches retain an actual row, including its original identifier. -/
def choose {K : ℕ} {α : Type*} (r : IndexedRow K α) :
    Option (IndexedRow K α) → Option (IndexedRow K α) × ℕ
  | none => (some r, 0)
  | some old => (if r.value < old.value then some r else some old, 1)

structure Run (K : ℕ) (α : Type*) where
  table : Table K α
  comparisons : ℕ
  accesses : ℕ

/-- One indexed array read followed by one indexed array write. -/
def insert {K : ℕ} {α : Type*} (t : Table K α) (r : IndexedRow K α) : Run K α :=
  let c := choose r (t.get r.key)
  ⟨t.set r.key c.1, c.2, 2⟩

/-- Left-to-right streaming traversal. -/
def scan {K : ℕ} {α : Type*} : List (IndexedRow K α) → Table K α → Run K α
  | [], t => ⟨t, 0, 0⟩
  | r :: rows, t =>
      let step := insert t r
      let rest := scan rows step.table
      ⟨rest.table, step.comparisons + rest.comparisons, step.accesses + rest.accesses⟩

/-- Initialization writes one absent entry per key. -/
def group {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) : Run K α :=
  let result := scan rows (empty K α)
  ⟨result.table, result.comparisons, K + result.accesses⟩

def EntrySpec {K : ℕ} {α : Type*} (seen : IndexedRow K α → Prop) (k : Fin K) :
    Option (IndexedRow K α) → Prop
  | none => ∀ r, seen r → r.key ≠ k
  | some r => seen r ∧ r.key = k ∧ ∀ s, seen s → s.key = k → r.value ≤ s.value

def TableSpec {K : ℕ} {α : Type*} (seen : IndexedRow K α → Prop) (t : Table K α) : Prop :=
  ∀ k, EntrySpec seen k (t.get k)

theorem entrySpec_congr {K : ℕ} {α : Type*} {p q : IndexedRow K α → Prop}
    (h : ∀ r, p r ↔ q r) (k : Fin K) (e : Option (IndexedRow K α)) :
    EntrySpec p k e ↔ EntrySpec q k e := by
  cases e <;> simp only [EntrySpec] <;> simp_rw [h]

theorem choose_spec {K : ℕ} {α : Type*} (seen : IndexedRow K α → Prop)
    (r : IndexedRow K α) (old : Option (IndexedRow K α)) (h : EntrySpec seen r.key old) :
    EntrySpec (fun s => s = r ∨ seen s) r.key (choose r old).1 := by
  cases old with
  | none =>
    refine ⟨Or.inl rfl, rfl, ?_⟩
    intro s hs hkey
    rcases hs with he | hs
    · subst s; exact le_rfl
    · exact False.elim (h s hs hkey)
  | some old =>
    obtain ⟨hmem, hkey, hmin⟩ := h
    by_cases hv : r.value < old.value
    · simp only [choose, hv, ↓reduceIte, EntrySpec]
      refine ⟨Or.inl trivial, trivial, ?_⟩
      intro s hs hsk
      rcases hs with he | hs
      · subst s; exact le_rfl
      · exact hv.le.trans (hmin s hs hsk)
    · simp only [choose, hv, ↓reduceIte, EntrySpec]
      refine ⟨Or.inr hmem, hkey, ?_⟩
      intro s hs hsk
      rcases hs with he | hs
      · subst s; exact le_of_not_gt hv
      · exact hmin s hs hsk

theorem insert_spec {K : ℕ} {α : Type*} (seen : IndexedRow K α → Prop)
    (t : Table K α) (r : IndexedRow K α) (h : TableSpec seen t) :
    TableSpec (fun s => s = r ∨ seen s) (insert t r).table := by
  intro k
  simp only [insert, Table.get_set]
  by_cases hk : r.key = k
  · subst k
    simp only [↓reduceIte]
    exact choose_spec seen r _ (h r.key)
  · simp only [hk, ↓reduceIte]
    have ho := h k
    cases he : t.get k with
    | none =>
      rw [he] at ho
      intro s hs
      rcases hs with hs | hs
      · subst s; exact hk
      · exact ho s hs
    | some old =>
      rw [he] at ho
      obtain ⟨hm, hkey, hmin⟩ := ho
      refine ⟨Or.inr hm, hkey, ?_⟩
      intro s hs hsk
      rcases hs with hs | hs
      · subst s; exact False.elim (hk hsk)
      · exact hmin s hs hsk

theorem scan_spec {K : ℕ} {α : Type*} (rows : List (IndexedRow K α))
    (seen : IndexedRow K α → Prop) (t : Table K α) (h : TableSpec seen t) :
    TableSpec (fun s => s ∈ rows ∨ seen s) (scan rows t).table := by
  induction rows generalizing seen t with
  | nil => simpa only [scan, List.not_mem_nil, false_or] using h
  | cons r rows ih =>
    have hs := ih (fun s => s = r ∨ seen s) (insert t r).table (insert_spec seen t r h)
    intro k
    exact (entrySpec_congr (fun s => by simp only [List.mem_cons]; tauto) k _).mp (hs k)

theorem group_spec {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) :
    TableSpec (fun s => s ∈ rows) (group rows).table := by
  have he : TableSpec (fun _ : IndexedRow K α => False) (empty K α) := by
    intro k
    rw [empty_get]
    intro r hr
    contradiction
  have h := scan_spec rows (fun _ => False) (empty K α) he
  simpa only [group, or_false] using h

theorem group_none_iff {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) (k : Fin K) :
    (group rows).table.get k = none ↔ ∀ r ∈ rows, r.key ≠ k := by
  have h := group_spec rows k
  cases he : (group rows).table.get k with
  | none => simpa [he, EntrySpec] using h
  | some r =>
    simp only [he, EntrySpec] at h
    simp only [reduceCtorEq, false_iff]
    exact fun hn => hn r h.1 h.2.1

theorem group_minimum {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) (k : Fin K)
    {r : IndexedRow K α} (hr : (group rows).table.get k = some r) :
    r ∈ rows ∧ r.key = k ∧ ∀ s ∈ rows, s.key = k → r.value ≤ s.value := by
  simpa only [hr, EntrySpec] using group_spec rows k

/-- Present minima give exactly the original real inequalities. Absent keys
impose no inequality, and a zero-direction key is handled by the same rule. -/
theorem group_real_constraints_iff {K : ℕ} {α : Type*}
    (rows : List (IndexedRow K α)) (lhs : Fin K → ℝ) :
    (∀ k r, (group rows).table.get k = some r → lhs k ≤ (r.value : ℝ)) ↔
      ∀ r ∈ rows, lhs r.key ≤ (r.value : ℝ) := by
  constructor
  · intro h r hr
    cases he : (group rows).table.get r.key with
    | none => exact False.elim ((group_none_iff rows r.key).mp he r hr rfl)
    | some s =>
      have hm := group_minimum rows r.key he
      exact (h r.key s he).trans (by exact_mod_cast hm.2.2 r hr rfl)
  · intro h k r hr
    have hm := group_minimum rows k hr
    rw [← hm.2.1]
    exact h r hm.1

theorem scan_cost {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) (t : Table K α) :
    (scan rows t).comparisons ≤ rows.length ∧ (scan rows t).accesses = 2 * rows.length := by
  induction rows generalizing t with
  | nil => simp [scan]
  | cons r rows ih =>
    have hi := ih (insert t r).table
    have hc : (insert t r).comparisons ≤ 1 := by
      simp only [insert]
      cases t.get r.key <;> simp [choose]
    simp only [scan, insert, List.length_cons] at *
    constructor <;> omega

theorem group_cost {K : ℕ} {α : Type*} (rows : List (IndexedRow K α)) :
    (group rows).comparisons ≤ rows.length ∧
      (group rows).accesses = K + 2 * rows.length := by
  have h := scan_cost rows (empty K α)
  exact ⟨h.1, congrArg (K + ·) h.2⟩

end NetworkSimplex.ThresholdGrouping
