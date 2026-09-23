import Formal.MatroidSpectral.ProfileLabels
import Mathlib.Data.Finset.Pi

namespace MatroidSpectral
open DAGSpectral
open scoped BigOperators

instance upperCoordDecidableEq (r : ℕ) : DecidableEq (UpperCoord r) :=
  inferInstanceAs (DecidableEq (Σ j : Fin r, Fin (j.val + 1)))

/-- Executable upper-triangle enumeration; no choice of a finite equivalence. -/
def upperCoords (r : ℕ) : List (UpperCoord r) :=
  (List.ofFn fun j : Fin r => List.ofFn fun i : Fin (j.val + 1) =>
    (⟨j,i⟩ : UpperCoord r)).flatten

theorem mem_upperCoords {r : ℕ} (i : UpperCoord r) : i ∈ upperCoords r := by
  obtain ⟨j,i⟩ := i
  exact List.mem_flatten.mpr ⟨_, List.mem_ofFn.mpr ⟨j,rfl⟩,
    List.mem_ofFn.mpr ⟨i,rfl⟩⟩

theorem upperCoords_length (r : ℕ) : (upperCoords r).length = r * (r + 1) / 2 := by
  have he : (upperCoords r).length = ∑ j : Fin r, (j.val + 1) := by
    unfold upperCoords UpperCoord
    rw [List.length_flatten]
    simp only [List.map_ofFn, Function.comp_def, List.length_ofFn, List.sum_ofFn]
  have ht : 2 * (∑ j : Fin r, (j.val + 1)) = r * (r + 1) := by
    clear he
    induction r with
    | zero => simp
    | succ r ih =>
      rw [Fin.sum_univ_castSucc]
      simp only [Fin.val_castSucc, Fin.val_last]
      nlinarith
  rw [he, ← ht, Nat.mul_div_cancel_left _ (by decide : 0 < 2)]

theorem naturalProfile_union {m : ℕ} {κ : Type*} (w : Fin m → κ → ℕ)
    (B F : Finset (Fin m)) (hF : F ⊆ B) :
    naturalProfile w B = naturalProfile w F + naturalProfile w (B \ F) := by
  funext i
  simpa only [naturalProfile, Pi.add_apply, add_comm] using
    (Finset.sum_sdiff hF (f := fun e => w e i)).symm

theorem optionalProfile_injective {m : ℕ} {κ : Type*} (w : Fin m → κ → ℕ)
    (C : Finset (Finset (Fin m))) (F : Finset (Fin m))
    (hF : ∀ B ∈ C, F ⊆ B)
    (hinj : Set.InjOn (naturalProfile w) (C : Set (Finset (Fin m)))) :
    Set.InjOn (fun B => naturalProfile w (B \ F)) (C : Set (Finset (Fin m))) := by
  intro B hB B' hB' he
  dsimp only at he
  apply hinj hB hB'
  rw [naturalProfile_union w B F (hF B hB), naturalProfile_union w B' F (hF B' hB'), he]

/-- Distinct full profiles translate to distinct optional profiles. The forced
coordinate therefore adds no factor to the output cardinality. -/
theorem profileFamily_card_le {m : ℕ} {κ : Type*} [Fintype κ]
    (w : Fin m → κ → ℕ) (C : Finset (Finset (Fin m))) (F : Finset (Fin m))
    (q W : ℕ) (hcard : ∀ B ∈ C, B.card = q) (hF : ∀ B ∈ C, F ⊆ B)
    (hW : ∀ B ∈ C, ∀ e ∈ B \ F, ∀ i, w e i ≤ W)
    (hinj : Set.InjOn (naturalProfile w) (C : Set (Finset (Fin m)))) :
    C.card ≤ ((q - F.card) * W + 1) ^ Fintype.card κ := by
  classical
  let code : C → (κ → Fin ((q - F.card) * W + 1)) := fun B i =>
    ⟨naturalProfile w (B.val \ F) i, by
      have h := naturalProfile_le w (B.val \ F) W (hW B.val B.property) i
      rw [Finset.card_sdiff_of_subset (hF B.val B.property), hcard B.val B.property] at h
      omega⟩
  have hi : Function.Injective code := by
    intro B B' he
    apply Subtype.ext
    apply optionalProfile_injective w C F hF hinj B.property B'.property
    funext i
    exact congrArg Fin.val (congrFun he i)
  have hc := Fintype.card_le_of_injective code hi
  simpa using hc

end MatroidSpectral
