import Formal.MatroidSpectral.ExecutionRecovery
import Formal.DAGSpectral.ProfileDPBitExecution

namespace MatroidSpectral.Execution

def coordinateRun {m : ℕ} {κ : Type*} [DecidableEq κ] (q D : ℕ)
    (coords : List κ)
    (query : (κ → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) : List (Finset (Fin m)) × ℕ :=
  let profiles := coordinateGrid D coords
  let run := candidates q query retained profiles
  (run.1, run.2 + (coords.length + 1) * (D + 1) * profiles.length)

theorem coordinateRun_value {m : ℕ} {κ : Type*} [DecidableEq κ] (q D : ℕ)
    (coords : List κ)
    (query : (κ → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) :
    (coordinateRun q D coords query retained).1 =
      (coordinateProfileProducerRun q D coords (fun z S => (query z S).1) retained).1 :=
  candidates_value q query retained _

theorem coordinateRun_work {m W : ℕ} {κ : Type*} [DecidableEq κ] (q D : ℕ)
    (coords : List κ)
    (query : (κ → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (hquery : ∀ z S, (query z S).2 ≤ W) (retained : Finset (Fin m)) :
    (coordinateRun q D coords query retained).2 ≤ (D + 1) ^ coords.length *
      ((m + 1) * W + (m + 2) * columnWork m + (coords.length + 1) * (D + 1)) := by
  have hh := candidates_work q query hquery retained (coordinateGrid D coords)
  simp only [coordinateRun, coordinateGrid_length] at *
  nlinarith

theorem coordinateRun_length {m : ℕ} {κ : Type*} [DecidableEq κ] (q D : ℕ)
    (coords : List κ)
    (query : (κ → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) :
    (coordinateRun q D coords query retained).1.length ≤ (D + 1) ^ coords.length := by
  rw [coordinateRun_value]
  exact coordinateProfileProducerRun_length _ _ _ _ _

/-- The full-scan deduplicator executes operand-dependent key charges. Its
application must bound those charges for the actual bases it receives. -/
def deduplicate {α κ : Type*} [DecidableEq κ] (key : α → κ)
    (comparisonWork : α → α → ℕ) (copyWork : ℕ) (xs : List α) : List α × ℕ :=
  let result := DAGSpectral.representativesBitCounted key comparisonWork xs
  (result.1, result.2 + xs.length * (copyWork + 1))

theorem deduplicate_value {α κ : Type*} [DecidableEq κ] (key : α → κ)
    (comparisonWork : α → α → ℕ) (copyWork : ℕ) (xs : List α) :
    (deduplicate key comparisonWork copyWork xs).1 =
      DAGSpectral.representatives key xs := by
  simp only [deduplicate, DAGSpectral.representativesBitCounted_spec]

theorem comparison_sum_work {α : Type*} (cost : α → α → ℕ) {W : ℕ}
    (a : α) (xs : List α) (h : ∀ b ∈ xs, cost a b ≤ W) :
    (xs.map (cost a)).sum ≤ xs.length * W := by
  induction xs with
  | nil => simp
  | cons b bs ih =>
      have hb := h b List.mem_cons_self
      have ht := ih (fun c hc => h c (List.mem_cons_of_mem _ hc))
      simp only [List.map_cons, List.sum_cons, List.length_cons]
      nlinarith

theorem representatives_work {α κ : Type*} [DecidableEq κ] (key : α → κ)
    (cost : α → α → ℕ) {W : ℕ} (xs : List α)
    (h : ∀ a ∈ xs, ∀ b ∈ xs, cost a b ≤ W) :
    DAGSpectral.representativeBitWork key cost xs ≤ xs.length ^ 2 * W := by
  induction xs with
  | nil => simp [DAGSpectral.representativeBitWork]
  | cons a xs ih =>
      have ht := ih (fun b hb c hc => h b (List.mem_cons_of_mem _ hb)
        c (List.mem_cons_of_mem _ hc))
      have hs := comparison_sum_work cost a (DAGSpectral.representatives key xs)
        (fun b hb => h a List.mem_cons_self b (List.mem_cons_of_mem _
          (DAGSpectral.representatives_subset key xs hb)))
      have hl : (DAGSpectral.representatives key xs).length ≤ xs.length :=
        (List.pwFilter_sublist _).length_le
      have hs' := hs.trans (Nat.mul_le_mul_right W hl)
      simp only [DAGSpectral.representativeBitWork, List.length_cons]
      nlinarith

theorem deduplicate_work {α κ : Type*} [DecidableEq κ] (key : α → κ)
    (cost : α → α → ℕ) {W : ℕ} (copyWork : ℕ) (xs : List α)
    (h : ∀ a ∈ xs, ∀ b ∈ xs, cost a b ≤ W) :
    (deduplicate key cost copyWork xs).2 ≤
      xs.length ^ 2 * W + xs.length * (copyWork + 1) := by
  simp only [deduplicate, DAGSpectral.representativesBitCounted_spec]
  exact Nat.add_le_add_right (representatives_work key cost xs h) _

/-- Collect actual trial results, charging traversal and copying each returned
witness. Rejected trials are still executed and still pay their own charge. -/
def collect {α β : Type*} (run : α → List β × ℕ) (copyWork : ℕ) :
    List α → List β × ℕ
  | [] => ([], 0)
  | a :: as =>
      let here := run a
      let rest := collect run copyWork as
      (here.1 ++ rest.1, here.2 + rest.2 + here.1.length * (copyWork + 1) + 1)

theorem collect_value {α β : Type*} (run : α → List β × ℕ)
    (copyWork : ℕ) (xs : List α) :
    (collect run copyWork xs).1 = xs.flatMap (fun a => (run a).1) := by
  induction xs with
  | nil => rfl
  | cons a as ih => simp only [collect, List.flatMap_cons, ih]

theorem collect_work {α β : Type*} (run : α → List β × ℕ)
    (copyWork W R : ℕ) (xs : List α)
    (hw : ∀ a ∈ xs, (run a).2 ≤ W)
    (hr : ∀ a ∈ xs, (run a).1.length ≤ R) :
    (collect run copyWork xs).2 ≤ xs.length * (W + R * (copyWork + 1) + 1) := by
  induction xs with
  | nil => simp [collect]
  | cons a as ih =>
      have hh := hw a List.mem_cons_self
      have hl := hr a List.mem_cons_self
      have ht := ih (fun b hb => hw b (List.mem_cons_of_mem _ hb))
        (fun b hb => hr b (List.mem_cons_of_mem _ hb))
      simp only [collect, List.length_cons]
      nlinarith

theorem collect_length {α β : Type*} (run : α → List β × ℕ)
    (copyWork R : ℕ) (xs : List α) (hr : ∀ a ∈ xs, (run a).1.length ≤ R) :
    (collect run copyWork xs).1.length ≤ xs.length * R := by
  induction xs with
  | nil => simp [collect]
  | cons a as ih =>
      have hh := hr a List.mem_cons_self
      have ht := ih (fun b hb => hr b (List.mem_cons_of_mem _ hb))
      simp only [collect, List.length_append, List.length_cons]
      nlinarith

theorem collect_sum_work {α β : Type*} (run : α → List β × ℕ)
    (copyWork : ℕ) (W R : α → ℕ) (xs : List α)
    (hw : ∀ a ∈ xs, (run a).2 ≤ W a)
    (hr : ∀ a ∈ xs, (run a).1.length ≤ R a) :
    (collect run copyWork xs).2 ≤
      (xs.map (fun a => W a + R a * (copyWork + 1) + 1)).sum := by
  induction xs with
  | nil => simp [collect]
  | cons a as ih =>
      have hh := hw a List.mem_cons_self
      have hl := Nat.mul_le_mul_right (copyWork + 1) (hr a List.mem_cons_self)
      have ht := ih (fun b hb => hw b (List.mem_cons_of_mem _ hb))
        (fun b hb => hr b (List.mem_cons_of_mem _ hb))
      simp only [collect, List.map_cons, List.sum_cons]
      omega

end MatroidSpectral.Execution
