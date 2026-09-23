import Mathlib.Algebra.Order.Round
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-! Equally spaced meshes with their sharp half-step covering radius. -/

noncomputable section

namespace InfiniteAggregation

theorem exists_nearest_nat {n : ℕ} {x : ℝ} (hx : x ∈ Set.Icc (0 : ℝ) n) :
    ∃ k : ℕ, k ≤ n ∧ |x - k| ≤ 1 / 2 := by
  let z := round x
  have hz0 : 0 ≤ z := by
    dsimp [z]
    rw [round_eq]
    exact Int.floor_nonneg.mpr (by linarith [hx.1])
  have hzn : z ≤ (n : ℤ) := by
    have hzlt : z < (n : ℤ) + 1 := by
      dsimp [z]
      rw [round_eq, Int.floor_lt]
      push_cast
      linarith [hx.2]
    omega
  refine ⟨z.toNat, ?_, ?_⟩
  · have : (z.toNat : ℤ) ≤ n := by simpa only [Int.toNat_of_nonneg hz0] using hzn
    exact_mod_cast this
  · have : (z.toNat : ℝ) = z := by
      rw [← Int.cast_natCast, Int.toNat_of_nonneg hz0]
    rw [this]
    exact abs_sub_round x

/-- The mesh of `N` equally spaced points in a real interval. -/
def intervalMesh (a b : ℝ) (N : ℕ) : Finset ℝ :=
  (Finset.range N).image (fun k : ℕ => a + (b - a) * k / (N - 1 : ℕ))

theorem card_intervalMesh_le (a b : ℝ) (N : ℕ) :
    (intervalMesh a b N).card ≤ N := by
  exact (Finset.card_image_le).trans_eq (Finset.card_range N)

theorem left_mem_intervalMesh (a b : ℝ) {N : ℕ} (hN : 2 ≤ N) :
    a ∈ intervalMesh a b N := by
  exact Finset.mem_image.mpr ⟨0, Finset.mem_range.mpr (by omega), by simp⟩

theorem right_mem_intervalMesh (a b : ℝ) {N : ℕ} (hN : 2 ≤ N) :
    b ∈ intervalMesh a b N := by
  have hn : ((N - 1 : ℕ) : ℝ) ≠ 0 := by exact_mod_cast (show N - 1 ≠ 0 by omega)
  refine Finset.mem_image.mpr ⟨N - 1, Finset.mem_range.mpr (by omega), ?_⟩
  simp [mul_div_cancel_right₀ _ hn]

theorem intervalMesh_subset_Icc {a b : ℝ} (hab : a ≤ b) {N : ℕ} (hN : 2 ≤ N) :
    ↑(intervalMesh a b N) ⊆ Set.Icc a b := by
  intro y hy
  obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hy
  have hkn : (k : ℝ) ≤ (N - 1 : ℕ) := by
    exact_mod_cast (show k ≤ N - 1 from Nat.le_pred_of_lt (Finset.mem_range.mp hk))
  have hn : (0 : ℝ) < (N - 1 : ℕ) := by exact_mod_cast (show 0 < N - 1 by omega)
  constructor
  · exact le_add_of_nonneg_right
      (div_nonneg (mul_nonneg (sub_nonneg.mpr hab) (Nat.cast_nonneg k)) hn.le)
  · have := (div_le_iff₀ hn).mpr (mul_le_mul_of_nonneg_left hkn (sub_nonneg.mpr hab))
    linarith

theorem exists_mem_intervalMesh_dist_le {a b θ : ℝ} (hab : a ≤ b)
    {N : ℕ} (hN : 2 ≤ N) (hθ : θ ∈ Set.Icc a b) :
    ∃ φ ∈ intervalMesh a b N, |θ - φ| ≤ (b - a) / (2 * (N - 1 : ℕ)) := by
  rcases hab.eq_or_lt with rfl | hab
  · refine ⟨a, left_mem_intervalMesh a a hN, ?_⟩
    have : θ = a := le_antisymm hθ.2 hθ.1
    simp [this]
  have hn : (0 : ℝ) < (N - 1 : ℕ) := by exact_mod_cast (show 0 < N - 1 by omega)
  have hd : 0 < b - a := sub_pos.mpr hab
  let x := (θ - a) * (N - 1 : ℕ) / (b - a)
  have hx : x ∈ Set.Icc (0 : ℝ) (N - 1 : ℕ) := by
    constructor
    · exact div_nonneg (mul_nonneg (sub_nonneg.mpr hθ.1) hn.le) hd.le
    · apply (div_le_iff₀ hd).mpr
      nlinarith [hθ.2]
  obtain ⟨k, hk, hdist⟩ := exists_nearest_nat hx
  refine ⟨a + (b - a) * k / (N - 1 : ℕ),
    Finset.mem_image.mpr ⟨k, Finset.mem_range.mpr (by omega), rfl⟩, ?_⟩
  have heq : θ - (a + (b - a) * k / (N - 1 : ℕ)) =
      (b - a) / (N - 1 : ℕ) * (x - k) := by
    dsimp [x]
    field_simp [ne_of_gt hd, ne_of_gt hn]
    ring
  rw [heq, abs_mul, abs_of_pos (div_pos hd hn)]
  calc
    (b - a) / (N - 1 : ℕ) * |x - k| ≤ (b - a) / (N - 1 : ℕ) * (1 / 2) :=
      mul_le_mul_of_nonneg_left hdist (div_nonneg hd.le hn.le)
    _ = (b - a) / (2 * (N - 1 : ℕ)) := by ring

def angleMesh (N : ℕ) : Finset ℝ := intervalMesh 0 (Real.pi / 2) N

theorem card_angleMesh_le (N : ℕ) : (angleMesh N).card ≤ N :=
  card_intervalMesh_le _ _ _

theorem angleMesh_subset_Icc {N : ℕ} (hN : 2 ≤ N) :
    ↑(angleMesh N) ⊆ Set.Icc 0 (Real.pi / 2) :=
  intervalMesh_subset_Icc (by positivity) hN

theorem zero_mem_angleMesh {N : ℕ} (hN : 2 ≤ N) : 0 ∈ angleMesh N :=
  left_mem_intervalMesh _ _ hN

theorem pi_div_two_mem_angleMesh {N : ℕ} (hN : 2 ≤ N) : Real.pi / 2 ∈ angleMesh N :=
  right_mem_intervalMesh _ _ hN

theorem exists_mem_angleMesh_dist_le {θ : ℝ} {N : ℕ} (hN : 2 ≤ N)
    (hθ : θ ∈ Set.Icc 0 (Real.pi / 2)) :
    ∃ φ ∈ angleMesh N, |θ - φ| ≤ Real.pi / (4 * (N - 1 : ℕ)) := by
  obtain ⟨φ, hφ, hdist⟩ := exists_mem_intervalMesh_dist_le (by positivity) hN hθ
  refine ⟨φ, hφ, ?_⟩
  convert hdist using 1
  ring

end InfiniteAggregation
