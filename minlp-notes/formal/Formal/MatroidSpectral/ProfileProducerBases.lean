import Formal.MatroidSpectral.ProfileProducerOracle
import Formal.DAGSpectral.Profiles

namespace MatroidSpectral

/-- Actual represented bases, obtained by interpolation and deletion. The final
filter keeps one base per ordinary profile, including at information rank zero. -/
def profileBases {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ) : List (Finset (Fin m)) :=
  DAGSpectral.representatives (naturalProfile w)
    (coordinateProfileProducerRun q (q * W) coords
      (markedProfileOracle A ground forced w W) ground).1

theorem profileBases_keys_nodup {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ) :
    ((profileBases A ground forced w W coords).map (naturalProfile w)).Nodup :=
  DAGSpectral.representatives_keys_nodup _ _

theorem profileBases_length {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ) :
    (profileBases A ground forced w W coords).length ≤ (q * W + 1) ^ coords.length := by
  apply (List.pwFilter_sublist _).length_le.trans
  exact coordinateProfileProducerRun_length q (q * W) coords _ ground

theorem profileBases_sound {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W)
    {B : Finset (Fin m)} (hB : B ∈ profileBases A ground forced w W coords) :
    IsBase A B ∧ B ⊆ ground ∧ forced ⊆ B := by
  have hraw := DAGSpectral.representatives_subset (naturalProfile w) _ hB
  obtain ⟨z, _, hb, hg, hf, _⟩ := profileCandidatesRun_sound q
    (fun z => MarkedTarget A ground forced w (fun i => (z i).val))
    (markedProfileOracle A ground forced w W)
    (markedProfileOracle_spec A ground forced w W hw)
    (fun _ _ ht => ht.1.card) ground (coordinateGrid (q * W) coords) hraw
  exact ⟨hb, hg, hf⟩

theorem profileBases_complete {q m : ℕ} {κ : Type*} [Fintype κ] [DecidableEq κ]
    (A : RationalRepresentation q m) (ground forced : Finset (Fin m))
    (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W) (hcoords : ∀ i, i ∈ coords)
    {B : Finset (Fin m)} (hbase : IsBase A B) (hground : B ⊆ ground)
    (hforced : forced ⊆ B) :
    ∃ C ∈ profileBases A ground forced w W coords,
      naturalProfile w C = naturalProfile w B := by
  let z : κ → Fin (q * W + 1) := fun i => ⟨naturalProfile w B i,
    Nat.lt_succ_of_le ((naturalProfile_le w B W
      (fun e he => hw e (hground he)) i).trans_eq (by rw [hbase.card]))⟩
  have hs : Supports (MarkedTarget A ground forced w (fun i => (z i).val)) ground :=
    ⟨B, ⟨hbase, hground, hforced, rfl⟩, hground⟩
  obtain ⟨C, hC, htarget⟩ := profileCandidatesRun_complete q
    (fun z => MarkedTarget A ground forced w (fun i => (z i).val))
    (markedProfileOracle A ground forced w W)
    (markedProfileOracle_spec A ground forced w W hw)
    (fun _ _ ht => ht.1.card) ground (coordinateGrid (q * W) coords)
    (mem_coordinateGrid (q * W) coords hcoords z) hs
  obtain ⟨C', hC', hkey⟩ := DAGSpectral.representatives_complete (naturalProfile w) hC
  exact ⟨C', hC', hkey.trans htarget.2.2.2⟩

theorem profileBases_empty_of_no_base {q m : ℕ} {κ : Type*}
    [Fintype κ] [DecidableEq κ] (A : RationalRepresentation q m)
    (ground forced : Finset (Fin m)) (w : Fin m → κ → ℕ) (W : ℕ) (coords : List κ)
    (hw : ∀ e ∈ ground, ∀ i, w e i ≤ W)
    (hn : ¬ ∃ B, IsBase A B ∧ B ⊆ ground ∧ forced ⊆ B) :
    profileBases A ground forced w W coords = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro B hB
  exact hn ⟨B, profileBases_sound A ground forced w W coords hw hB⟩

end MatroidSpectral
