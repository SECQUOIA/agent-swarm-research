import Mathlib

/-! Cumulative allocations at the endpoints of equal unit cells. -/
namespace SwitchingControl

abbrev Profile (n : ℕ) := Fin n → Fin 3 → ℝ

/-- Endpoint data of a simplex-valued relaxed input. Index `j` denotes time `j+1`.
The increment bounds also describe all intermediate endpoint pairs. -/
structure ValidProfile {n : ℕ} (A : Profile n) : Prop where
  nonneg : ∀ j i, 0 ≤ A j i
  first : ∀ j i, j.val = 0 → A j i ≤ 1
  increments : ∀ j k i, j ≤ k → A j i ≤ A k i ∧
    A k i - A j i ≤ (k.val : ℝ) - j.val
  conservation : ∀ j, ∑ i, A j i = (j.val : ℝ) + 1

/-- No endpoint coordinate is an integer. -/
def StrictProfile {n : ℕ} (A : Profile n) : Prop :=
  ∀ j i, ∀ z : ℤ, A j i ≠ z

noncomputable def floors {n : ℕ} (A : Profile n) (j : Fin n) (i : Fin 3) : ℕ :=
  ⌊A j i⌋₊

/-- A strict endpoint lies in the open interval between its floor and successor. -/
theorem strict_floor_bounds {n : ℕ} {A : Profile n} (hA : ValidProfile A)
    (hs : StrictProfile A) (j : Fin n) (i : Fin 3) :
    (floors A j i : ℝ) < A j i ∧ A j i < (floors A j i : ℝ) + 1 := by
  refine ⟨lt_of_le_of_ne (Nat.floor_le (hA.nonneg j i)) ?_, Nat.lt_floor_add_one _⟩
  simpa [floors] using (hs j i (⌊A j i⌋₊ : ℤ)).symm

/-- The initial floor vector is zero. -/
theorem initial_floors {n : ℕ} {A : Profile n} (hA : ValidProfile A)
    (hs : StrictProfile A) (j : Fin n) (hj : j.val = 0) (i : Fin 3) :
    floors A j i = 0 := by
  have hlt : A j i < 1 := lt_of_le_of_ne (hA.first j i hj) (by simpa using hs j i 1)
  have := (Nat.floor_lt (n := 1) (hA.nonneg j i)).2 (by simpa using hlt)
  change ⌊A j i⌋₊ = 0
  omega

/-- On adjacent cells each coordinate floor increases by zero or one. -/
theorem floor_increment {n : ℕ} {A : Profile n} (hA : ValidProfile A)
    (j k : Fin n) (hjk : k.val = j.val + 1) (i : Fin 3) :
    floors A j i ≤ floors A k i ∧ floors A k i ≤ floors A j i + 1 := by
  have h := hA.increments j k i (by omega)
  refine ⟨Nat.floor_mono h.1, ?_⟩
  have hle : A k i ≤ A j i + 1 := by
    have hc : (k.val : ℝ) = j.val + 1 := by exact_mod_cast hjk
    linarith [h.2]
  have hf := Nat.floor_mono hle
  rw [show A j i + 1 = A j i + (1 : ℕ) by norm_num,
    Nat.floor_add_natCast (hA.nonneg j i)] at hf
  exact hf

/-- The sum of the three strict fractional parts is either one or two. -/
theorem floor_sum_cases {n : ℕ} {A : Profile n} (hA : ValidProfile A)
    (hs : StrictProfile A) (j : Fin n) :
    (∑ i, floors A j i) + 1 = j.val + 1 ∨
    (∑ i, floors A j i) + 2 = j.val + 1 := by
  have h0 := strict_floor_bounds hA hs j 0
  have h1 := strict_floor_bounds hA hs j 1
  have h2 := strict_floor_bounds hA hs j 2
  have hc := hA.conservation j
  simp only [Fin.sum_univ_succ] at hc ⊢
  have hlo : (floors A j 0 : ℝ) + floors A j 1 + floors A j 2 < j.val + 1 := by
    norm_num at hc
    linarith
  have hhi : (j.val : ℝ) + 1 < floors A j 0 + floors A j 1 + floors A j 2 + 3 := by
    norm_num at hc
    linarith
  have hlo' : floors A j 0 + floors A j 1 + floors A j 2 < j.val + 1 := by
    exact_mod_cast hlo
  have hhi' : j.val + 1 < floors A j 0 + floors A j 1 + floors A j 2 + 3 := by
    exact_mod_cast hhi
  norm_num
  omega

/-- Every coordinate is bounded by the total mass. -/
theorem profile_bounded {n : ℕ} {A : Profile n} (hA : ValidProfile A)
    (j : Fin n) (i : Fin 3) : 0 ≤ A j i ∧ A j i ≤ n := by
  refine ⟨hA.nonneg j i, ?_⟩
  have hi : A j i ≤ ∑ k, A j k := Finset.single_le_sum
    (fun k _ => hA.nonneg j k) (Finset.mem_univ i)
  rw [hA.conservation j] at hi
  have hj : (j.val : ℝ) + 1 ≤ n := by exact_mod_cast j.isLt
  linarith

/-- Convex interpolation preserves every allocation constraint. -/
theorem valid_interpolate {n : ℕ} {A B : Profile n}
    (hA : ValidProfile A) (hB : ValidProfile B) {ε : ℝ}
    (hε : 0 ≤ ε) (hε1 : ε ≤ 1) :
    ValidProfile (fun j i => (1 - ε) * A j i + ε * B j i) := by
  have he : 0 ≤ 1 - ε := sub_nonneg.mpr hε1
  constructor
  · intro j i
    positivity [hA.nonneg j i, hB.nonneg j i]
  · intro j i hj
    nlinarith [mul_nonneg he (sub_nonneg.mpr (hA.first j i hj)),
      mul_nonneg hε (sub_nonneg.mpr (hB.first j i hj))]
  · intro j k i hjk
    obtain ⟨ha, ha'⟩ := hA.increments j k i hjk
    obtain ⟨hb, hb'⟩ := hB.increments j k i hjk
    constructor
    · nlinarith [mul_nonneg he (sub_nonneg.mpr ha),
        mul_nonneg hε (sub_nonneg.mpr hb)]
    · nlinarith [mul_nonneg he (sub_nonneg.mpr ha'),
        mul_nonneg hε (sub_nonneg.mpr hb')]
  · intro j
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
      hA.conservation, hB.conservation]
    ring

/-- A single rational baseline works on all grids of at most seven cells. -/
noncomputable def baseline (n : ℕ) : Profile n :=
  fun j i => ((j.val : ℝ) + 1) * (![1, 2, 8] i / 11)

theorem baseline_valid (n : ℕ) : ValidProfile (baseline n) := by
  constructor
  · intro j i
    fin_cases i <;> dsimp [baseline] <;> positivity
  · intro j i hj
    fin_cases i <;> norm_num [baseline, hj]
  · intro j k i hjk
    have hh : (j.val : ℝ) ≤ k.val := by exact_mod_cast hjk
    fin_cases i <;> norm_num [baseline] <;> constructor <;> first | omega | linarith
  · intro j
    simp [baseline, Fin.sum_univ_succ]
    ring

theorem baseline_strict {n : ℕ} (hn : n ≤ 7) : StrictProfile (baseline n) := by
  intro j i z hz
  have hj : j.val ≤ 6 := by omega
  have hf : ⌊baseline n j i⌋ = z := by rw [hz, Int.floor_intCast]
  interval_cases hj' : j.val <;> fin_cases i <;>
    norm_num [baseline, hj'] at hf <;> subst z <;> norm_num [baseline, hj'] at hz

end SwitchingControl
