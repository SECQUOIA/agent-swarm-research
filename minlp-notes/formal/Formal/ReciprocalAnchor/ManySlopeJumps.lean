import Formal.ReciprocalAnchor.ManyModel

/-! Exact finite call distributions obtained from ordered affine pieces. -/

namespace ReciprocalAnchor.ManyLeaf

/-- A continuous finite chain of affine pieces, with the exterior pieces
`m - s` and `0`. The `N` knot positions separate `N + 1` pieces. -/
structure SlopeJumpData (N : ℕ) (m : ℝ) where
  knot : ℕ → ℝ
  intercept : ℕ → ℝ
  slope : ℕ → ℝ
  slope_first : slope 0 = -1
  slope_last : slope N = 0
  intercept_first : intercept 0 = m
  intercept_last : intercept N = 0
  slope_mono : ∀ i < N, slope i ≤ slope (i + 1)
  continuous_at : ∀ i < N,
    intercept (i + 1) + slope (i + 1) * knot i = intercept i + slope i * knot i

namespace SlopeJumpData

variable {N : ℕ} {m : ℝ} (D : SlopeJumpData N m)

/-- The atom at a knot has mass equal to the upward jump in slope. -/
def mass (i : ℕ) : ℝ := D.slope (i + 1) - D.slope i

/-- The finite call function of the slope-jump distribution. -/
def call (s : ℝ) : ℝ := ∑ i ∈ Finset.range N, D.mass i * max (D.knot i - s) 0

theorem mass_nonneg {i : ℕ} (hi : i < N) : 0 ≤ D.mass i :=
  sub_nonneg.mpr (D.slope_mono i hi)

theorem mass_sum : ∑ i ∈ Finset.range N, D.mass i = 1 := by
  simp only [mass, Finset.sum_range_sub, D.slope_last, D.slope_first]
  norm_num

theorem mass_mul_knot {i : ℕ} (hi : i < N) :
    D.mass i * D.knot i = D.intercept i - D.intercept (i + 1) := by
  have h := D.continuous_at i hi
  dsimp [mass]
  nlinarith

theorem mean : ∑ i ∈ Finset.range N, D.mass i * D.knot i = m := by
  calc
    _ = ∑ i ∈ Finset.range N, (D.intercept i - D.intercept (i + 1)) :=
      Finset.sum_congr rfl fun i hi ↦ D.mass_mul_knot (Finset.mem_range.mp hi)
    _ = m := by rw [Finset.sum_range_sub', D.intercept_first, D.intercept_last, sub_zero]

/-- On the interval belonging to piece `k`, the call sum is exactly that
piece. The endpoint cases `k = 0` and `k = N` give both exterior pieces. -/
theorem call_eq_piece (s : ℝ) (k : ℕ) (hk : k ≤ N)
    (hleft : ∀ i < k, D.knot i ≤ s)
    (hright : ∀ i, k ≤ i → i < N → s ≤ D.knot i) :
    D.call s = D.intercept k + D.slope k * s := by
  have hzero : ∑ i ∈ Finset.range k, D.mass i * max (D.knot i - s) 0 = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    rw [max_eq_right (sub_nonpos.mpr (hleft i (Finset.mem_range.mp hi))), mul_zero]
  have htail : ∑ i ∈ Finset.Ico k N, D.mass i * max (D.knot i - s) 0 =
      ∑ i ∈ Finset.Ico k N,
        ((D.intercept i + D.slope i * s) -
          (D.intercept (i + 1) + D.slope (i + 1) * s)) := by
    apply Finset.sum_congr rfl
    intro i hi
    obtain ⟨hki, hiN⟩ := Finset.mem_Ico.mp hi
    rw [max_eq_left (sub_nonneg.mpr (hright i hki hiN)), mul_sub,
      D.mass_mul_knot hiN]
    dsimp [mass]
    ring
  have htel := Finset.sum_Ico_sub (fun i ↦ D.intercept i + D.slope i * s) hk
  rw [Finset.sum_Ico_eq_sub _ hk, hzero, sub_zero] at htail
  dsimp [call]
  rw [htail]
  calc
    _ = -(∑ i ∈ Finset.Ico k N,
        ((D.intercept (i + 1) + D.slope (i + 1) * s) -
          (D.intercept i + D.slope i * s))) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = D.intercept k + D.slope k * s := by
      rw [htel, D.intercept_last, D.slope_last]
      ring

/-- Affine interpolation data determine the entire finite call function.
The hypothesis identifies the piece containing each threshold; it does not
assume a distributional representation. -/
theorem call_eq_of_pieces (f : ℝ → ℝ)
    (hpieces : ∀ s, ∃ k ≤ N,
      (∀ i < k, D.knot i ≤ s) ∧
      (∀ i, k ≤ i → i < N → s ≤ D.knot i) ∧
      f s = D.intercept k + D.slope k * s) : D.call = f := by
  funext s
  obtain ⟨k, hk, hleft, hright, hf⟩ := hpieces s
  exact (D.call_eq_piece s k hk hleft hright).trans hf.symm

/-- The actual bounded probability law reconstructed from slope jumps. -/
noncomputable def toLaw {a b : ℝ}
    (hb : ∀ i < N, a ≤ D.knot i ∧ D.knot i ≤ b) : Law a b where
  size := N
  mass i := D.mass i
  location i := D.knot i
  nonneg i := D.mass_nonneg i.isLt
  total := by simpa [Fin.sum_univ_eq_sum_range] using D.mass_sum
  bounds i := hb i i.isLt

theorem toLaw_mean {a b : ℝ} (hb : ∀ i < N, a ≤ D.knot i ∧ D.knot i ≤ b) :
    (D.toLaw hb).mean = m := by
  change (∑ i : Fin N, (fun j ↦ D.mass j * D.knot j) i) = m
  exact (Fin.sum_univ_eq_sum_range (fun j ↦ D.mass j * D.knot j) N).trans D.mean

theorem toLaw_call {a b : ℝ} (hb : ∀ i < N, a ≤ D.knot i ∧ D.knot i ≤ b)
    (s : ℝ) : (D.toLaw hb).call s = D.call s := by
  change (∑ i : Fin N, (fun j ↦ D.mass j * max (D.knot j - s) 0) i) = D.call s
  exact Fin.sum_univ_eq_sum_range (fun j ↦ D.mass j * max (D.knot j - s) 0) N

end SlopeJumpData
end ReciprocalAnchor.ManyLeaf
