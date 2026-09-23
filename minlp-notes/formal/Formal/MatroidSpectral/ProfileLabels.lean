import Formal.DAGSpectral.TrialApproximation
import Mathlib.Data.Finset.Card

/-! Signed profile shifts and a forced-owner coordinate. All tests use the
original base cardinality; the extra coordinate avoids contraction. -/
namespace MatroidSpectral
open scoped BigOperators

def signedProfile {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (B : Finset (Fin m)) : κ → ℤ := fun i => ∑ e ∈ B, z e i

def shiftedWeight {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (L : ℕ) : Fin m → κ → ℕ := fun e i => (z e i + L).toNat

def naturalProfile {m : ℕ} {κ : Type*} (w : Fin m → κ → ℕ)
    (B : Finset (Fin m)) : κ → ℕ := fun i => ∑ e ∈ B, w e i

theorem shiftedWeight_cast {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (L : ℕ) (e : Fin m) (i : κ) (h : -(L : ℤ) ≤ z e i) :
    (shiftedWeight z L e i : ℤ) = z e i + L := by
  exact Int.toNat_of_nonneg (by omega)

theorem shiftedWeight_le {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (L : ℕ) (e : Fin m) (i : κ) (h : z e i ≤ L) :
    shiftedWeight z L e i ≤ 2 * L := by
  unfold shiftedWeight
  omega

theorem shiftedProfile_cast {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (L : ℕ) (B : Finset (Fin m)) (h : ∀ e ∈ B, ∀ i, -(L : ℤ) ≤ z e i)
    (i : κ) :
    (naturalProfile (shiftedWeight z L) B i : ℤ) =
      signedProfile z B i + B.card * L := by
  simp only [naturalProfile, Nat.cast_sum]
  simp_rw [shiftedWeight]
  rw [Finset.sum_congr rfl (fun e he => Int.toNat_of_nonneg (by have := h e he i; omega))]
  simp [signedProfile, Finset.sum_add_distrib]

theorem shiftedProfile_eq_iff {m : ℕ} {κ : Type*} (z : Fin m → κ → ℤ)
    (L : ℕ) (B C : Finset (Fin m)) (hc : B.card = C.card)
    (hB : ∀ e ∈ B, ∀ i, -(L : ℤ) ≤ z e i)
    (hC : ∀ e ∈ C, ∀ i, -(L : ℤ) ≤ z e i) :
    naturalProfile (shiftedWeight z L) B = naturalProfile (shiftedWeight z L) C ↔
      signedProfile z B = signedProfile z C := by
  constructor
  · intro h
    funext i
    have hi := congrArg (fun f => (f i : ℤ)) h
    rw [shiftedProfile_cast z L B hB, shiftedProfile_cast z L C hC, hc] at hi
    exact add_right_cancel hi
  · intro h
    funext i
    apply Int.natCast_inj.mp
    rw [shiftedProfile_cast z L B hB, shiftedProfile_cast z L C hC, hc, h]

def ownerWeight {m : ℕ} (F : Finset (Fin m)) (e : Fin m) : ℕ :=
  if e ∈ F then 1 else 0

theorem ownerProfile_eq_card {m : ℕ} (F B : Finset (Fin m)) :
    (∑ e ∈ B, ownerWeight F e) = (B ∩ F).card := by
  simp [ownerWeight]

theorem ownerProfile_full_iff {m : ℕ} (F B : Finset (Fin m)) :
    (∑ e ∈ B, ownerWeight F e) = F.card ↔ F ⊆ B := by
  rw [ownerProfile_eq_card]
  constructor
  · intro h
    have he := Finset.eq_of_subset_of_card_le (Finset.inter_subset_right : B ∩ F ⊆ F) h.ge
    rw [← he]
    exact Finset.inter_subset_left
  · intro h
    rw [Finset.inter_eq_right.mpr h]

/-- The marker is a single extra coordinate, independent of the number of
forced owners. Requiring its full value forces every selected owner. -/
def markedWeight {m : ℕ} {κ : Type*} (F : Finset (Fin m))
    (w : Fin m → κ → ℕ) : Fin m → Option κ → ℕ :=
  fun e i => i.elim (ownerWeight F e) (w e)

@[simp] theorem markedProfile_none {m : ℕ} {κ : Type*} (F B : Finset (Fin m))
    (w : Fin m → κ → ℕ) :
    naturalProfile (markedWeight F w) B none = (B ∩ F).card :=
  ownerProfile_eq_card F B

@[simp] theorem markedProfile_some {m : ℕ} {κ : Type*} (F B : Finset (Fin m))
    (w : Fin m → κ → ℕ) (i : κ) :
    naturalProfile (markedWeight F w) B (some i) = naturalProfile w B i := rfl

theorem floorLabel_bounds {x h : ℚ} (hh : 0 < h) (p : ℕ)
    (hx : |x| ≤ 4 * p) :
    -(⌈4 * (p : ℚ) / h⌉₊ : ℤ) ≤ ⌊x / h⌋ ∧
      ⌊x / h⌋ ≤ (⌈4 * (p : ℚ) / h⌉₊ : ℤ) := by
  have hc := Nat.le_ceil (4 * (p : ℚ) / h)
  obtain ⟨hl, hu⟩ := abs_le.mp hx
  constructor
  · apply Int.le_floor.mpr
    push_cast
    have hx' : -(4 * (p : ℚ) / h) ≤ x / h := by
      rw [← neg_div]
      exact div_le_div_of_nonneg_right hl hh.le
    linarith
  · have hx' := div_le_div_of_nonneg_right hu hh.le
    have hf := Int.floor_le (x / h)
    exact_mod_cast hf.trans (hx'.trans hc)

theorem naturalProfile_le {m : ℕ} {κ : Type*} (w : Fin m → κ → ℕ)
    (B : Finset (Fin m)) (W : ℕ) (h : ∀ e ∈ B, ∀ i, w e i ≤ W) (i : κ) :
    naturalProfile w B i ≤ B.card * W := by
  exact (Finset.sum_le_sum (fun e he => h e he i)).trans_eq (by simp)

end MatroidSpectral
