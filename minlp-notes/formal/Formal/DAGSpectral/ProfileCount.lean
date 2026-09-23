import Formal.DAGSpectral.Rounding
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Finset.Pi

/-! Finite coordinate intervals for signed accumulated labels. -/
namespace DAGSpectral
noncomputable section
open scoped BigOperators

/-- The signed range allows residuals of up to N whole mesh units. -/
def coordinateRange (p N : ℕ) (h : ℝ) : Finset ℤ :=
  Finset.Icc ⌊-(4 * (p : ℝ) * N / h) - N⌋ ⌊4 * (p : ℝ) * N / h⌋

/-- The explicit number of values per coordinate in a rank-r trial. -/
def coordinateCount (p r N : ℕ) (η : ℝ) : ℕ :=
  ⌈8 * (p : ℝ) * r * N ^ 2 / η + N⌉₊ + 2

theorem sum_abs_le_length (xs : List ℝ) {B : ℝ}
    (hb : ∀ x ∈ xs, |x| ≤ B) : |xs.sum| ≤ xs.length * B := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := hb x (by simp)
    have ht := ih (fun y hy => hb y (by simp [hy]))
    simp only [List.sum_cons, List.length_cons, Nat.cast_add, Nat.cast_one]
    have ha := abs_add_le x xs.sum
    linarith

theorem pathLabel_mem_coordinateRange {p N : ℕ} (hN : 0 < N) {h : ℝ}
    (hh : 0 < h) (xs : List ℝ) (hlen : xs.length ≤ N)
    (hb : ∀ x ∈ xs, |x| ≤ 4 * p) : pathLabel h xs ∈ coordinateRange p N h := by
  have hs : |xs.sum| ≤ (N : ℝ) * (4 * p) := (sum_abs_le_length xs hb).trans
    (mul_le_mul_of_nonneg_right (by exact_mod_cast hlen) (by positivity))
  obtain ⟨hl, hu⟩ := abs_le.mp hs
  obtain ⟨hrl, hru⟩ := path_residual_bounds hh hN xs hlen
  simp only [coordinateRange, Finset.mem_Icc]
  constructor
  · have hlower : -(4 * (p : ℝ) * N / h) - N ≤ (pathLabel h xs : ℝ) := by
      nlinarith [mul_div_cancel₀ (4 * (p : ℝ) * N) (ne_of_gt hh)]
    exact_mod_cast (Int.floor_le (-(4 * (p : ℝ) * N / h) - N)).trans hlower
  · apply Int.le_floor.mpr
    apply (le_div_iff₀ hh).mpr
    nlinarith

theorem floor_interval_card_le (a b : ℝ) :
    (Finset.Icc ⌊a⌋ ⌊b⌋).card ≤ ⌈b - a⌉₊ + 2 := by
  rw [Int.card_Icc, Int.toNat_le]
  have ha := Int.lt_floor_add_one a
  have hb := Int.floor_le b
  have hc := Nat.le_ceil (b - a)
  have hz : ((⌊b⌋ + 1 - ⌊a⌋ : ℤ) : ℝ) ≤ ((⌈b - a⌉₊ + 2 : ℕ) : ℝ) := by
    push_cast
    linarith
  exact_mod_cast hz

theorem coordinateRange_card_le {p r N : ℕ} {η : ℝ}
    (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) :
    (coordinateRange p N (spectralMesh η r N)).card ≤ coordinateCount p r N η := by
  have hrd : (r : ℝ) ≠ 0 := by positivity
  have hNd : (N : ℝ) ≠ 0 := by positivity
  have he : 4 * (p : ℝ) * N / spectralMesh η r N -
      (-(4 * (p : ℝ) * N / spectralMesh η r N) - N) =
      8 * (p : ℝ) * r * N ^ 2 / η + N := by
    unfold spectralMesh
    field_simp
    ring
  unfold coordinateRange coordinateCount
  simpa only [he] using floor_interval_card_le
    (-(4 * (p : ℝ) * N / spectralMesh η r N) - N)
    (4 * (p : ℝ) * N / spectralMesh η r N)

/-- A profile is a genuine bounded integer vector. -/
def BoundedProfile (d : ℕ) (s : Finset ℤ) := Fin d → {z : ℤ // z ∈ s}

instance (d : ℕ) (s : Finset ℤ) : Fintype (BoundedProfile d s) :=
  inferInstanceAs (Fintype (Fin d → {z : ℤ // z ∈ s}))

theorem card_boundedProfile (d : ℕ) (s : Finset ℤ) :
    Fintype.card (BoundedProfile d s) = s.card ^ d := by
  change Fintype.card (Fin d → {z : ℤ // z ∈ s}) = _
  convert @Fintype.card_fun (Fin d) {z : ℤ // z ∈ s} _ _ _ using 1
  simp

theorem card_spectral_profiles_le (d p r N : ℕ) {η : ℝ}
    (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) :
    Fintype.card (BoundedProfile d (coordinateRange p N (spectralMesh η r N))) ≤
      coordinateCount p r N η ^ d := by
  rw [card_boundedProfile]
  exact Nat.pow_le_pow_left (coordinateRange_card_le hr hN hη) d

end
end DAGSpectral
