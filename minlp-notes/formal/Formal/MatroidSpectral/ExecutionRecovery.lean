import Formal.MatroidSpectral.ProfileProducer

/-! Counted outer loops. Every query executes the supplied counted procedure;
its Boolean and cost are retained together. The non-arithmetic charge covers
linear finite-set scans and copies of encoded column identifiers. -/
namespace MatroidSpectral
namespace Execution

/-- A conservative scan/copy charge for sets of column identifiers. -/
def columnWork (m : ℕ) : ℕ := 4 * (m + 1) * (Nat.size m + 1)

def recovery {m : ℕ} (query : Finset (Fin m) → Bool × ℕ) :
    List (Fin m) → Finset (Fin m) → Finset (Fin m) × ℕ
  | [], retained => (retained, 0)
  | e :: es, retained =>
      let candidate := retained.erase e
      let test := query candidate
      let next := if test.1 then candidate else retained
      let rest := recovery query es next
      (rest.1, test.2 + columnWork m + rest.2)

theorem recovery_value {m : ℕ} (query : Finset (Fin m) → Bool × ℕ)
    (order : List (Fin m)) (retained : Finset (Fin m)) :
    (recovery query order retained).1 =
      (recoveryRun (fun S => (query S).1) order retained).1 := by
  induction order generalizing retained with
  | nil => rfl
  | cons e es ih => simp only [recovery, recoveryRun, ih]

theorem recovery_work {m W : ℕ} (query : Finset (Fin m) → Bool × ℕ)
    (hquery : ∀ S, (query S).2 ≤ W)
    (order : List (Fin m)) (retained : Finset (Fin m)) :
    (recovery query order retained).2 ≤ order.length * (W + columnWork m) := by
  induction order generalizing retained with
  | nil => simp [recovery]
  | cons e es ih =>
      simp only [recovery, List.length_cons, Nat.add_mul, Nat.one_mul]
      exact (Nat.add_le_add_right (Nat.add_le_add_right (hquery _) _) _).trans
        (by have hh := ih (if (query (retained.erase e)).1 then retained.erase e else retained)
            omega)

def recoverAtRank {m : ℕ} (q : ℕ) (query : Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) : Finset (Fin m) × ℕ :=
  if q = 0 then (∅, 1) else
    let run := recovery query (List.finRange m) retained
    (run.1, run.2 + columnWork m)

theorem recoverAtRank_value {m : ℕ} (q : ℕ)
    (query : Finset (Fin m) → Bool × ℕ) (retained : Finset (Fin m)) :
    (recoverAtRank q query retained).1 =
      (recoverBasisAtRank q (fun S => (query S).1) retained).1 := by
  simp only [recoverAtRank, recoverBasisAtRank, recoverBasis]
  split <;> simp [recovery_value]

theorem recoverAtRank_subset {m : ℕ} (q : ℕ)
    (query : Finset (Fin m) → Bool × ℕ) (retained : Finset (Fin m)) :
    (recoverAtRank q query retained).1 ⊆ retained := by
  simp only [recoverAtRank]
  split
  · exact Finset.empty_subset _
  · rw [recovery_value]
    exact recoveryRun_subset _ _ _

theorem recoverAtRank_work {m W : ℕ} (q : ℕ)
    (query : Finset (Fin m) → Bool × ℕ) (hquery : ∀ S, (query S).2 ≤ W)
    (retained : Finset (Fin m)) :
    (recoverAtRank q query retained).2 ≤ m * (W + columnWork m) + columnWork m := by
  have hc : 1 ≤ columnWork m := by unfold columnWork; nlinarith
  simp only [recoverAtRank]
  split
  · omega
  · have hh := recovery_work query hquery (List.finRange m) retained
    simpa only [List.length_finRange] using Nat.add_le_add_right hh (columnWork m)

/-- Support tests, deletion tests, and witness copies all belong to this run. -/
def candidates {m : ℕ} {β : Type*} (q : ℕ)
    (query : β → Finset (Fin m) → Bool × ℕ) (retained : Finset (Fin m)) :
    List β → List (Finset (Fin m)) × ℕ
  | [] => ([], 0)
  | z :: zs =>
      let test := query z retained
      let rest := candidates q query retained zs
      if test.1 then
        let recovered := recoverAtRank q (query z) retained
        (recovered.1 :: rest.1, test.2 + recovered.2 + columnWork m + rest.2)
      else (rest.1, test.2 + 1 + rest.2)

theorem candidates_value {m : ℕ} {β : Type*} (q : ℕ)
    (query : β → Finset (Fin m) → Bool × ℕ) (retained : Finset (Fin m))
    (profiles : List β) :
    (candidates q query retained profiles).1 =
      (profileCandidatesRun q (fun z S => (query z S).1) retained profiles).1 := by
  induction profiles with
  | nil => rfl
  | cons z zs ih =>
      simp only [candidates, profileCandidatesRun, ih, recoverAtRank_value]
      split <;> rfl

theorem candidates_subset {m : ℕ} {β : Type*} (q : ℕ)
    (query : β → Finset (Fin m) → Bool × ℕ) (retained : Finset (Fin m))
    (profiles : List β) {B : Finset (Fin m)}
    (hB : B ∈ (candidates q query retained profiles).1) : B ⊆ retained := by
  induction profiles with
  | nil => simp [candidates] at hB
  | cons z zs ih =>
      simp only [candidates] at hB
      split at hB
      · rcases List.mem_cons.mp hB with rfl | hB
        · exact recoverAtRank_subset q (query z) retained
        · exact ih hB
      · exact ih hB

theorem candidates_work {m W : ℕ} {β : Type*} (q : ℕ)
    (query : β → Finset (Fin m) → Bool × ℕ)
    (hquery : ∀ z S, (query z S).2 ≤ W) (retained : Finset (Fin m))
    (profiles : List β) :
    (candidates q query retained profiles).2 ≤
      profiles.length * ((m + 1) * W + (m + 2) * columnWork m) := by
  induction profiles with
  | nil => simp [candidates]
  | cons z zs ih =>
      have hr := recoverAtRank_work q (query z) (hquery z) retained
      have ht := hquery z retained
      have hc : 1 ≤ columnWork m := by unfold columnWork; nlinarith
      simp only [candidates, List.length_cons]
      split <;> simp only [Nat.add_mul, Nat.one_mul] <;> nlinarith

def profileRun {m d : ℕ} (q D : ℕ)
    (query : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) : List (Finset (Fin m)) × ℕ :=
  let profiles := profileGrid D d
  let run := candidates q query retained profiles
  (run.1, run.2 + (d + 1) * (D + 1) * profiles.length)

theorem profileRun_value {m d : ℕ} (q D : ℕ)
    (query : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (retained : Finset (Fin m)) :
    (profileRun q D query retained).1 =
      (profileProducerRun q D (fun z S => (query z S).1) retained).1 :=
  candidates_value q query retained _

theorem profileRun_work {m d W : ℕ} (q D : ℕ)
    (query : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool × ℕ)
    (hquery : ∀ z S, (query z S).2 ≤ W) (retained : Finset (Fin m)) :
    (profileRun q D query retained).2 ≤ (D + 1) ^ d *
      ((m + 1) * W + (m + 2) * columnWork m + (d + 1) * (D + 1)) := by
  have hh := candidates_work q query hquery retained (profileGrid D d)
  simp only [profileRun, profileGrid_length] at *
  nlinarith

end Execution
end MatroidSpectral
