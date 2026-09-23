import Formal.MatroidSpectral.Recovery
import Mathlib.Data.Fin.Tuple.Basic

namespace MatroidSpectral

/-- Enumerate only the bounded profile grid, never the family of bases. -/
def profileGrid (D : ℕ) : (d : ℕ) → List (Fin d → Fin (D + 1))
  | 0 => [Fin.elim0]
  | d + 1 => (List.finRange (D + 1)).flatMap fun x =>
      (profileGrid D d).map (Fin.cons x)

theorem mem_profileGrid (D d : ℕ) (z : Fin d → Fin (D + 1)) :
    z ∈ profileGrid D d := by
  induction d with
  | zero =>
      have hz : z = Fin.elim0 := by funext i; exact Fin.elim0 i
      simp [profileGrid, hz]
  | succ d ih =>
      apply List.mem_flatMap.mpr
      refine ⟨z 0, List.mem_finRange _, List.mem_map.mpr ?_⟩
      exact ⟨Fin.tail z, ih _, Fin.cons_self_tail z⟩

theorem profileGrid_length (D d : ℕ) : (profileGrid D d).length = (D + 1) ^ d := by
  induction d with
  | zero => simp [profileGrid]
  | succ d ih =>
      simp [profileGrid, List.length_flatMap, ih, pow_succ, Nat.mul_comm]

/-- A coordinate-list version avoids choosing a noncomputable numbering of a
finite coordinate type. Coordinates omitted from the list have value zero. -/
def coordinateGrid {κ : Type*} [DecidableEq κ] (D : ℕ) :
    List κ → List (κ → Fin (D + 1))
  | [] => [fun _ => 0]
  | i :: is => (List.finRange (D + 1)).flatMap fun x =>
      (coordinateGrid D is).map (fun z => Function.update z i x)

theorem coordinateGrid_length {κ : Type*} [DecidableEq κ] (D : ℕ)
    (coords : List κ) : (coordinateGrid D coords).length = (D + 1) ^ coords.length := by
  induction coords with
  | nil => simp [coordinateGrid]
  | cons i is ih =>
      simp [coordinateGrid, List.length_flatMap, ih, pow_succ, Nat.mul_comm]

theorem coordinateGrid_agrees {κ : Type*} [DecidableEq κ] (D : ℕ)
    (coords : List κ) (z : κ → Fin (D + 1)) :
    ∃ w ∈ coordinateGrid D coords, ∀ i ∈ coords, w i = z i := by
  induction coords with
  | nil => exact ⟨fun _ => 0, List.mem_cons_self, by simp⟩
  | cons i is ih =>
      obtain ⟨w, hw, hagree⟩ := ih
      refine ⟨Function.update w i (z i), ?_, ?_⟩
      · exact List.mem_flatMap.mpr ⟨z i, List.mem_finRange _,
          List.mem_map.mpr ⟨w, hw, rfl⟩⟩
      · intro j hj
        by_cases hji : j = i
        · subst j; simp
        · rw [Function.update_of_ne hji]
          exact hagree j ((List.mem_cons.mp hj).resolve_left hji)

theorem mem_coordinateGrid {κ : Type*} [DecidableEq κ] (D : ℕ)
    (coords : List κ) (hcoords : ∀ i, i ∈ coords) (z : κ → Fin (D + 1)) :
    z ∈ coordinateGrid D coords := by
  obtain ⟨w, hw, hagree⟩ := coordinateGrid_agrees D coords z
  have heq : w = z := funext (fun i => hagree i (hcoords i))
  exact heq ▸ hw

/-- Query support for each candidate profile and recover one actual base when
positive. The count includes the initial test and every deletion test. -/
def profileCandidatesRun {m : ℕ} {β : Type*} (q : ℕ)
    (oracle : β → Finset (Fin m) → Bool) (retained : Finset (Fin m)) :
    List β → List (Finset (Fin m)) × ℕ
  | [] => ([], 0)
  | z :: zs =>
      let rest := profileCandidatesRun q oracle retained zs
      if oracle z retained then
        let recovered := recoverBasisAtRank q (oracle z) retained
        (recovered.1 :: rest.1, 1 + recovered.2 + rest.2)
      else (rest.1, 1 + rest.2)

theorem profileCandidatesRun_length {m : ℕ} {β : Type*} (q : ℕ)
    (oracle : β → Finset (Fin m) → Bool) (retained : Finset (Fin m))
    (profiles : List β) :
    (profileCandidatesRun q oracle retained profiles).1.length ≤ profiles.length := by
  induction profiles with
  | nil => simp [profileCandidatesRun]
  | cons z zs ih =>
      simp only [profileCandidatesRun, List.length_cons]
      split <;> simp only [List.length_cons] <;> omega

theorem profileCandidatesRun_calls {m : ℕ} {β : Type*} (q : ℕ)
    (oracle : β → Finset (Fin m) → Bool) (retained : Finset (Fin m))
    (profiles : List β) :
    (profileCandidatesRun q oracle retained profiles).2 ≤ profiles.length * (m + 1) := by
  induction profiles with
  | nil => simp [profileCandidatesRun]
  | cons z zs ih =>
      have hr := recoverBasisAtRank_calls q (oracle z) retained
      simp only [profileCandidatesRun, List.length_cons]
      split <;> simp only [Nat.add_mul, Nat.one_mul] <;> omega

theorem profileCandidatesRun_sound {m : ℕ} {β : Type*} (q : ℕ)
    (target : β → Finset (Fin m) → Prop)
    (oracle : β → Finset (Fin m) → Bool)
    (hOracle : ∀ z S, oracle z S = true ↔ Supports (target z) S)
    (hRank : ∀ z B, target z B → B.card = q)
    (retained : Finset (Fin m)) (profiles : List β)
    {B : Finset (Fin m)} (hB : B ∈ (profileCandidatesRun q oracle retained profiles).1) :
    ∃ z ∈ profiles, target z B := by
  induction profiles with
  | nil => simp [profileCandidatesRun] at hB
  | cons z zs ih =>
      simp only [profileCandidatesRun] at hB
      split at hB
      · rename_i hz
        rcases List.mem_cons.mp hB with rfl | hB
        · exact ⟨z, List.mem_cons_self,
            recoverBasisAtRank_target (target z) (oracle z) (hOracle z) (hRank z)
              retained ((hOracle z retained).mp hz)⟩
        · obtain ⟨w, hw, ht⟩ := ih hB
          exact ⟨w, List.mem_cons_of_mem _ hw, ht⟩
      · obtain ⟨w, hw, ht⟩ := ih hB
        exact ⟨w, List.mem_cons_of_mem _ hw, ht⟩

theorem profileCandidatesRun_complete {m : ℕ} {β : Type*} (q : ℕ)
    (target : β → Finset (Fin m) → Prop)
    (oracle : β → Finset (Fin m) → Bool)
    (hOracle : ∀ z S, oracle z S = true ↔ Supports (target z) S)
    (hRank : ∀ z B, target z B → B.card = q)
    (retained : Finset (Fin m)) (profiles : List β)
    {z : β} (hz : z ∈ profiles) (hs : Supports (target z) retained) :
    ∃ B ∈ (profileCandidatesRun q oracle retained profiles).1, target z B := by
  induction profiles with
  | nil => simp at hz
  | cons w ws ih =>
      rcases List.mem_cons.mp hz with rfl | hz
      · have ht := (hOracle z retained).mpr hs
        simp only [profileCandidatesRun, ht, ↓reduceIte]
        exact ⟨_, List.mem_cons_self,
          recoverBasisAtRank_target (target z) (oracle z) (hOracle z) (hRank z) retained hs⟩
      · obtain ⟨B, hB, hb⟩ := ih hz
        refine ⟨B, ?_, hb⟩
        simp only [profileCandidatesRun]
        split
        · exact List.mem_cons_of_mem _ hB
        · exact hB

/-- The fixed-marker producer scans the ordinary `d` profile coordinates. A
forced-owner marker can be incorporated in the supplied support oracle. -/
def profileProducerRun {m d : ℕ} (q D : ℕ)
    (oracle : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : List (Finset (Fin m)) × ℕ :=
  profileCandidatesRun q oracle retained (profileGrid D d)

theorem profileProducerRun_length {m d : ℕ} (q D : ℕ)
    (oracle : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) :
    (profileProducerRun q D oracle retained).1.length ≤ (D + 1) ^ d := by
  simpa only [profileProducerRun, profileGrid_length] using
    profileCandidatesRun_length q oracle retained (profileGrid D d)

theorem profileProducerRun_calls {m d : ℕ} (q D : ℕ)
    (oracle : (Fin d → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) :
    (profileProducerRun q D oracle retained).2 ≤ (D + 1) ^ d * (m + 1) := by
  simpa only [profileProducerRun, profileGrid_length] using
    profileCandidatesRun_calls q oracle retained (profileGrid D d)

def coordinateProfileProducerRun {m : ℕ} {κ : Type*} [DecidableEq κ]
    (q D : ℕ) (coords : List κ)
    (oracle : (κ → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : List (Finset (Fin m)) × ℕ :=
  profileCandidatesRun q oracle retained (coordinateGrid D coords)

theorem coordinateProfileProducerRun_length {m : ℕ} {κ : Type*} [DecidableEq κ]
    (q D : ℕ) (coords : List κ)
    (oracle : (κ → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) :
    (coordinateProfileProducerRun q D coords oracle retained).1.length ≤
      (D + 1) ^ coords.length := by
  simpa only [coordinateProfileProducerRun, coordinateGrid_length] using
    profileCandidatesRun_length q oracle retained (coordinateGrid D coords)

theorem coordinateProfileProducerRun_calls {m : ℕ} {κ : Type*} [DecidableEq κ]
    (q D : ℕ) (coords : List κ)
    (oracle : (κ → Fin (D + 1)) → Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) :
    (coordinateProfileProducerRun q D coords oracle retained).2 ≤
      (D + 1) ^ coords.length * (m + 1) := by
  simpa only [coordinateProfileProducerRun, coordinateGrid_length] using
    profileCandidatesRun_calls q oracle retained (coordinateGrid D coords)

end MatroidSpectral
