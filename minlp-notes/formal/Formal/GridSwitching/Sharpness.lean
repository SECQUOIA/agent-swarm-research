import Formal.GridSwitching.ThreeMode

/-!
# SC28: the coefficient one of the instance transfer estimate is not uniformly reducible

This module discharges the obligation SC28 of `topics/17-grid-switching/CLAIMS.md`:
`prop:transfer-sharpness` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex` together with the
repeated-cycle family of the paragraph that follows it. The fuller derivation is the section
"Sharp universal transfer constant and a half-grid obstruction" of
`notes/cia-reopened-grid-transfer.md`.

## The family

Fix `n ≥ 2` modes and `m ≥ 1` cycles, use the unit grid with `N = n m + 1` cells and horizon
`T = N`, and allow `s = n m - 1 = N - 2` switches.

* `sharpRate`, `sharpInput`: the relaxed input runs every mode at rate `1 / n` on the first
  cell `[0, 1]` and the distinguished mode `n` (`tailMode`) purely on `[1, N]`. It is grid
  constant (`isGridConstant_sharpInput`), and `sharp_budget` records `1 ≤ s ≤ N - 2`, so the
  example lives inside the restricted regime the cited conjecture assumes.
* `sharpWord`, `sharpTimes`, `sharpSchedule`: the continuous competitor repeats the cycle of
  modes `1, ..., n` exactly `m` times inside the first cell, using blocks of length
  `1 / (n m)`, and then stays in mode `n`. Its final within-cell block already selects mode
  `n`, so it merges with the pure tail and the schedule uses exactly `n m` activation blocks,
  that is `s = n m - 1` switches (`isSchedule_sharpSchedule`).

## The three parts of SC28

* Grid optimum (`gridOPT_sharpInput`): `OPT^T_s(A) = 1 - 1/n` on **every** unit grid with at
  least one cell and for **every** switch budget. The lower bound
  `le_gridOPT_sharpInput` uses `exists_first_cell_full`: a grid schedule can only switch at
  grid nodes, so one mode occupies the whole of `[0, 1]` and its discrepancy at time one is
  `1 - 1/n`. The upper bound `gridOPT_sharpInput_le` is the constant mode-`n` schedule.
* Continuous competitor (`D_sharpSchedule_le`, `OPT_sharpInput_le`): the competitor has
  maximum absolute error at most `(n - 1) / (n² m)`, and all its discrepancies vanish at time
  one (`sharpInput_sub_sharpSchedule_one`). The source states `(n - 1) / (n² m)` as an
  **upper bound** on the continuous optimum, and only the upper bound is proved here.
* Gap (`sharp_gap`): `OPT^T_s(A) - OPT_s(A) ≥ (1 - 1/n)(1 - 1/(n m))`. For `m = 1` this is
  `(1 - 1/n)²` (`sharp_gap_sq`), which tends to one (`tendsto_sharp_gap_bound`); hence no
  constant strictly below one works uniformly in the mode count
  (`exists_sharp_gap_gt`). The concrete instance of the manuscript, `n = 4`, `N = 5`,
  `s = 3`, gives a gap of at least `9/16` (`sharp_gap_four`), which exceeds one half
  (`half_lt_sharp_gap_four`).

The arithmetic of the source was checked and is correct:
`(1 - 1/n) - (n - 1)/n² = (n - 1)/n - (n - 1)/n² = (n - 1)²/n² = (1 - 1/n)²`, and for `n = 4`
`3/4 - 3/16 = 9/16 > 1/2`. The general identity
`(1 - 1/n) - (n - 1)/(n² m) = (1 - 1/n)(1 - 1/(n m))` is `hid` inside `sharp_gap`.

## SC29: the scope of this counterexample

Recorded here as scope, not as a mathematical claim, and deliberately not formalized.

The statement this family refutes is the instance-wise half-mesh **heuristic** that precedes
Conjecture 1 in Sager–Zeile (2021), p. 615, and the corresponding passage of Zeile's 2021
dissertation, p. 139: the inference that discretization costs at most half the maximum grid
width because each individual switch time can be moved by that much. Those passages motivate
a conjecture; they are not stated or proved as transfer theorems, so nothing here refutes an
established theorem.

The example is an **instance-wise** gap for one fixed relaxed input. It says nothing about
the difference of the two minimax values `F_{n,s}(T)` and `F^T_{n,s}`, and no such claim is
made anywhere in this module. The one-switch nearest-boundary half-mesh estimate is
unaffected.

## Hypotheses added beyond the source

* The definitions `tailMode`, `sharpRate`, `sharpInput`, `sharpWord` and `sharpSchedule` take
  a proof of `0 < n` as a parameter, because the distinguished mode `n - 1 : Fin n` and the
  residue word `j ↦ j mod n` do not exist for an empty mode type. Statements therefore carry
  `hn : 0 < n` (and `hm : 0 < m`) explicitly; the source leaves `n ≥ 2`, `m ≥ 1` implicit.
  Where `n ≥ 2` is genuinely needed it appears separately, as in `sharp_budget`.
* `gridOPT_sharpInput` is proved for every cell count `N ≥ 1` and every switch budget `s`,
  which is stronger than the source needs: the grid optimum of this input does not depend on
  the budget at all.
* `sharp_gap` takes the cell count `N` and the budget `s` as parameters constrained by
  `N = n m + 1` and `s = n m - 1`, so that the `m = 1` specialization can be stated with the
  literal `n + 1` and `n - 1` rather than with `n * 1 + 1` and `n * 1 - 1`; the grid appears
  as the type-level index of `unitGrid N`, which blocks rewriting `n * 1` to `n` after the
  fact.
-/

namespace GridSwitching

open Set

/-! ## The distinguished mode, the relaxed input, and the grid -/

/-- The distinguished mode `n` of the sharpness family: the last mode, which the relaxed
input runs purely after time one. -/
def tailMode {n : ℕ} (hn : 0 < n) : Fin n := ⟨n - 1, by omega⟩

@[simp] theorem tailMode_val {n : ℕ} (hn : 0 < n) : (tailMode hn : ℕ) = n - 1 := rfl

/-- The per-cell rate matrix of the sharpness family on `N` unit cells: every mode runs at
rate `1 / n` on the first cell `[0, 1]`, and the distinguished mode `n` runs purely on every
later cell. -/
noncomputable def sharpRate {n : ℕ} (hn : 0 < n) (N : ℕ) (j : Fin N) (i : Fin n) : ℝ :=
  if (j : ℕ) = 0 then (n : ℝ)⁻¹ else if i = tailMode hn then 1 else 0

/-- The rates of the sharpness family form a rate matrix. -/
theorem isRateMatrix_sharpRate {n : ℕ} (hn : 0 < n) (N : ℕ) :
    IsRateMatrix (sharpRate hn N) where
  nonneg j i := by
    simp only [sharpRate]
    split_ifs <;> norm_num
  conservation j := by
    simp only [sharpRate]
    by_cases hj : (j : ℕ) = 0
    · simp only [if_pos hj, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
        nsmul_eq_mul]
      exact mul_inv_cancel₀ (Nat.cast_ne_zero.mpr hn.ne')
    · simp only [if_neg hj]
      rw [Finset.sum_ite_eq' Finset.univ (tailMode hn) (fun _ => (1 : ℝ))]
      simp


/-! ### Grid-node values of the unit grid -/

/-- The left endpoint of the `j`-th unit cell. -/
private theorem unitGrid_castSucc {N : ℕ} (j : Fin N) :
    unitGrid N j.castSucc = ((j : ℕ) : ℝ) := rfl

/-- The right endpoint of the `j`-th unit cell. -/
private theorem unitGrid_succ {N : ℕ} (j : Fin N) :
    unitGrid N j.succ = ((j : ℕ) : ℝ) + 1 := by
  simp [unitGrid]

/-! ### The relaxed input -/

/-- The relaxed input of the sharpness family on the unit grid with `N` cells: every mode
runs at rate `1 / n` on the first cell `[0, 1]`, and the distinguished mode `n` runs purely
on `[1, N]`. -/
noncomputable def sharpInput {n : ℕ} (hn : 0 < n) (N : ℕ) : Fin n → ℝ → ℝ :=
  gridCumulative (unitGrid N) (sharpRate hn N)

/-- The input of the sharpness family is grid constant, so the example lives inside the
restricted regime the cited conjecture assumes. -/
theorem isGridConstant_sharpInput {n : ℕ} (hn : 0 < n) (N : ℕ) :
    IsGridConstant (unitGrid N) (sharpInput hn N) :=
  ⟨sharpRate hn N, isRateMatrix_sharpRate hn N, rfl⟩

/-- The input of the sharpness family is a cumulative allocation. -/
theorem isCumulative_sharpInput {n : ℕ} (hn : 0 < n) (N : ℕ) :
    IsCumulative (sharpInput hn N) ((N : ℕ) : ℝ) :=
  gridCumulative_isCumulative (isGrid_unitGrid N).orderedTimes (isRateMatrix_sharpRate hn N)

/-- On the first cell every mode has accumulated exactly `t / n`. -/
theorem sharpInput_apply_of_le_one {n N : ℕ} (hn : 0 < n) (hN : 0 < N) (i : Fin n) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : sharpInput hn N i t = t / (n : ℝ) := by
  simp only [sharpInput, gridCumulative]
  rw [Finset.sum_eq_single (⟨0, hN⟩ : Fin N)]
  · rw [sharpRate]
    have hc : unitGrid N (⟨0, hN⟩ : Fin N).castSucc = 0 := by
      rw [unitGrid_castSucc]; norm_num
    have hs : unitGrid N (⟨0, hN⟩ : Fin N).succ = 1 := by
      rw [unitGrid_succ]; norm_num
    rw [hc, hs, if_pos rfl, min_eq_left ht1, min_eq_right ht0, sub_zero]
    field_simp
  · intro j _ hj
    have hj1 : (1 : ℝ) ≤ ((j : ℕ) : ℝ) := by
      have h : 1 ≤ (j : ℕ) := Nat.one_le_iff_ne_zero.mpr fun h => hj (Fin.ext h)
      exact_mod_cast h
    rw [unitGrid_castSucc, unitGrid_succ, min_eq_left (ht1.trans hj1),
      min_eq_left (ht1.trans (by linarith)), sub_self, mul_zero]
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- At the horizon the distinguished mode carries all the mass accumulated after time one. -/
theorem sharpInput_apply_horizon {n N : ℕ} (hn : 0 < n) (hN : 0 < N) (i : Fin n) :
    sharpInput hn N i ((N : ℕ) : ℝ)
      = (n : ℝ)⁻¹ + (if i = tailMode hn then ((N : ℕ) : ℝ) - 1 else 0) := by
  obtain ⟨k, rfl⟩ : ∃ k, N = k + 1 := ⟨N - 1, by omega⟩
  have hcell : ∀ j : Fin (k + 1),
      min ((k + 1 : ℕ) : ℝ) (unitGrid (k + 1) j.succ) -
        min ((k + 1 : ℕ) : ℝ) (unitGrid (k + 1) j.castSucc) = 1 := by
    intro j
    have hj : ((j : ℕ) : ℝ) + 1 ≤ ((k + 1 : ℕ) : ℝ) := by
      have h : (j : ℕ) + 1 ≤ k + 1 := j.isLt
      exact_mod_cast h
    rw [unitGrid_castSucc, unitGrid_succ, min_eq_right hj, min_eq_right (by linarith)]
    ring
  simp only [sharpInput, gridCumulative]
  rw [Finset.sum_congr rfl fun j _ => by rw [hcell j, mul_one], Fin.sum_univ_succ]
  have h0 : sharpRate hn (k + 1) 0 i = (n : ℝ)⁻¹ := by rw [sharpRate]; simp
  have hsucc : ∀ j : Fin k, sharpRate hn (k + 1) j.succ i
      = if i = tailMode hn then 1 else 0 := fun j => by rw [sharpRate, if_neg (by simp)]
  rw [h0, Finset.sum_congr rfl fun j _ => hsucc j, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul]
  push_cast
  split_ifs <;> ring

/-! ## The grid optimum of the sharpness family -/

/-- A monotone `{0, 1}`-valued family on the block endpoints jumps by a total of one, so some
mode of the word collects the whole jump. -/
private theorem exists_word_jump {n : ℕ} :
    ∀ (k : ℕ) (p : Fin k → Fin n) (f : Fin (k + 1) → ℝ), Monotone f →
      (∀ q, f q = 0 ∨ f q = 1) → f 0 = 0 → f (Fin.last k) = 1 →
      ∃ i : Fin n, ∑ j : Fin k, (if p j = i then f j.succ - f j.castSucc else 0) = 1 := by
  intro k
  induction k with
  | zero =>
    intro p f _ _ h0 hl
    rw [show (Fin.last 0 : Fin 1) = 0 from rfl, h0] at hl
    exact absurd hl (by norm_num)
  | succ k ih =>
    intro p f hmono hval h0 hl
    have hcast0 : ((0 : Fin (k + 1)).castSucc : Fin (k + 2)) = 0 := rfl
    have hsucc0 : ((0 : Fin (k + 1)).succ : Fin (k + 2)) = 1 := rfl
    rcases hval 1 with h1 | h1
    · obtain ⟨i, hi⟩ := ih (fun j => p j.succ) (fun q => f q.succ)
        (fun a b hab => hmono (Fin.succ_le_succ_iff.mpr hab)) (fun q => hval q.succ)
        (by simpa using h1) (by rw [Fin.succ_last]; exact hl)
      refine ⟨i, ?_⟩
      rw [Fin.sum_univ_succ, hcast0, hsucc0, h1, h0, sub_zero, ite_self, zero_add, ← hi]
      exact Finset.sum_congr rfl fun j _ => by rw [Fin.succ_castSucc]
    · have hone : ∀ q : Fin (k + 2), 1 ≤ (q : ℕ) → f q = 1 := by
        intro q hq
        rcases hval q with h | h
        · have hle : f 1 ≤ f q := hmono (by rw [Fin.le_def]; simpa using hq)
          rw [h1, h] at hle
          linarith
        · exact h
      refine ⟨p 0, ?_⟩
      rw [Fin.sum_univ_succ, hcast0, hsucc0, h1, h0, if_pos rfl, sub_zero]
      have hzero : ∀ j : Fin k,
          (if p j.succ = p 0 then f j.succ.succ - f j.succ.castSucc else 0) = 0 := by
        intro j
        rw [hone j.succ.succ (by simp), hone j.succ.castSucc (by simp), sub_self, ite_self]
      rw [Finset.sum_congr rfl fun j _ => hzero j, Finset.sum_const, smul_zero, add_zero]

/-- Every grid schedule on the unit grid activates a single mode throughout the first cell,
so that mode has occupied the whole cell at time one. -/
theorem exists_first_cell_full {n N k : ℕ} (hN : 0 < N) {W : Fin n → ℝ → ℝ}
    (hW : IsGridSchedule (unitGrid N) k W) : ∃ i : Fin n, W i 1 = 1 := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  refine exists_word_jump k p (fun q => min (1 : ℝ) (unitGrid N (g q))) ?_ ?_ ?_ ?_
  · exact fun a b hab =>
      min_le_min le_rfl ((isGrid_unitGrid N).strictMono.monotone (hg hab))
  · intro q
    rcases Nat.eq_zero_or_pos (g q : ℕ) with h | h
    · left
      rw [unitGrid_apply, h]
      norm_num
    · right
      refine min_eq_left ?_
      rw [unitGrid_apply]
      exact_mod_cast h
  · rw [hg0]
    norm_num [unitGrid]
  · rw [hgl, unitGrid_apply, Fin.val_last]
    exact min_eq_left (by exact_mod_cast hN)

/-- Lower bound: every grid schedule of the sharpness family errs by at least `1 - 1/n` at
time one, in whichever mode it selected on the first cell. -/
theorem le_gridOPT_sharpInput {n N : ℕ} (hn : 0 < n) (hN : 0 < N) (s : ℕ) :
    1 - (n : ℝ)⁻¹ ≤ gridOPT (unitGrid N) (sharpInput hn N) ((N : ℕ) : ℝ) s := by
  have hn1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  refine le_gridOPT hn fun W hW => ?_
  obtain ⟨i, hi⟩ := exists_first_cell_full hN hW
  have hmem : (1 : ℝ) ∈ Icc (0 : ℝ) ((N : ℕ) : ℝ) := ⟨zero_le_one, by exact_mod_cast hN⟩
  have hle := le_D (isCumulative_sharpInput hn N)
    (hW.isSchedule (isGrid_unitGrid N)).isCumulative i hmem
  rw [sharpInput_apply_of_le_one hn hN i zero_le_one le_rfl, hi] at hle
  refine le_trans (le_of_eq ?_) hle
  rw [abs_of_nonpos (by rw [sub_nonpos, div_le_one (by linarith)]; linarith)]
  field_simp
  ring

/-- Upper bound: the constant schedule of the distinguished mode attains the error
`1 - 1/n`. -/
theorem gridOPT_sharpInput_le {n N : ℕ} (hn : 0 < n) (hN : 0 < N) (s : ℕ) :
    gridOPT (unitGrid N) (sharpInput hn N) ((N : ℕ) : ℝ) s ≤ 1 - (n : ℝ)⁻¹ := by
  have hx := isGrid_unitGrid N
  have hT : (0 : ℝ) ≤ ((N : ℕ) : ℝ) := Nat.cast_nonneg _
  have hA := isCumulative_sharpInput hn N
  have hW : IsGridSchedule (unitGrid N) (s + 1)
      (constSchedule (tailMode hn) ((N : ℕ) : ℝ)) :=
    IsGridSchedule.mono hn (Nat.succ_le_succ (Nat.zero_le s))
      (isGridSchedule_constSchedule hx (tailMode hn))
  refine (gridOPT_le_D hn hx hA hT hW).trans ?_
  refine (D_constSchedule_le hA hT (tailMode hn)).trans (le_of_eq ?_)
  rw [sharpInput_apply_horizon hn hN (tailMode hn), if_pos rfl]
  ring

/-- SC28, grid optimum: the grid optimum of the sharpness family is exactly `1 - 1/n`, for
every switch budget. -/
theorem gridOPT_sharpInput {n N : ℕ} (hn : 0 < n) (hN : 0 < N) (s : ℕ) :
    gridOPT (unitGrid N) (sharpInput hn N) ((N : ℕ) : ℝ) s = 1 - (n : ℝ)⁻¹ :=
  le_antisymm (gridOPT_sharpInput_le hn hN s) (le_gridOPT_sharpInput hn hN s)

/-! ## The continuous competitor

The competitor repeats the cycle of modes `1, ..., n` exactly `m` times inside the first
cell, using `n m` blocks of length `1 / (n m)`, and then stays in the distinguished mode `n`.
The final block of the cycle already selects mode `n`, so it merges with the pure tail and
the schedule uses exactly `n m` blocks, that is `s = n m - 1` switches. -/

/-- The word of the continuous competitor: block `j` selects mode `j mod n`. -/
def sharpWord {n : ℕ} (hn : 0 < n) (m : ℕ) (j : Fin (n * m)) : Fin n :=
  ⟨(j : ℕ) % n, Nat.mod_lt _ hn⟩

/-- The switch times of the continuous competitor: `n m` blocks of length `1 / (n m)` fill
the first cell, and the last of them is extended to the horizon. -/
noncomputable def sharpTimes (n m : ℕ) (l : Fin (n * m + 1)) : ℝ :=
  if (l : ℕ) < n * m then ((l : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) else ((n * m + 1 : ℕ) : ℝ)

/-- The continuous competitor of the sharpness family. -/
noncomputable def sharpSchedule {n : ℕ} (hn : 0 < n) (m : ℕ) : Fin n → ℝ → ℝ :=
  occupation (sharpWord hn m) (sharpTimes n m)

/-- The competitor is the cumulative occupation of its word and switch times. -/
theorem sharpSchedule_eq {n : ℕ} (hn : 0 < n) (m : ℕ) :
    sharpSchedule hn m = occupation (sharpWord hn m) (sharpTimes n m) := rfl

/-- The switch times of the competitor are ordered on the horizon. -/
theorem orderedTimes_sharpTimes {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) :
    OrderedTimes (sharpTimes n m) ((n * m + 1 : ℕ) : ℝ) where
  first := by
    rw [sharpTimes, if_pos (by simpa using Nat.mul_pos hn hm)]
    simp
  last := by
    rw [sharpTimes, if_neg (by simp)]
  mono := by
    have hnm : (0 : ℝ) < ((n * m : ℕ) : ℝ) := by exact_mod_cast Nat.mul_pos hn hm
    intro a b hab
    have hab' : (a : ℕ) ≤ (b : ℕ) := hab
    simp only [sharpTimes]
    split_ifs with h1 h2 h2
    · have : ((a : ℕ) : ℝ) ≤ ((b : ℕ) : ℝ) := by exact_mod_cast hab'
      gcongr
    · refine le_trans ?_
        (by exact_mod_cast Nat.le_add_left 1 (n * m) : (1 : ℝ) ≤ ((n * m + 1 : ℕ) : ℝ))
      rw [div_le_one hnm]
      exact_mod_cast h1.le
    · omega
    · exact le_rfl

/-- The left endpoint of the `j`-th block of the competitor. -/
private theorem sharpTimes_castSucc {n m : ℕ} (j : Fin (n * m)) :
    sharpTimes n m j.castSucc = ((j : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) := by
  rw [sharpTimes, if_pos (by simp)]
  simp

/-- The length of the `j`-th block of the competitor: `1 / (n m)`, except that the final
block absorbs the whole pure tail. -/
private theorem sharpTimes_block {n m : ℕ} (j : Fin (n * m)) :
    sharpTimes n m j.succ - sharpTimes n m j.castSucc
      = 1 / ((n * m : ℕ) : ℝ)
        + (if (j : ℕ) + 1 = n * m then ((n * m : ℕ) : ℝ) else 0) := by
  have hnm : (0 : ℝ) < ((n * m : ℕ) : ℝ) := by
    have : 0 < n * m := lt_of_le_of_lt (Nat.zero_le _) j.isLt
    exact_mod_cast this
  have hval : ((j.succ : Fin (n * m + 1)) : ℕ) = (j : ℕ) + 1 := rfl
  rw [sharpTimes_castSucc, sharpTimes, hval]
  rcases Nat.lt_or_ge ((j : ℕ) + 1) (n * m) with hlt | hge
  · rw [if_pos hlt, if_neg (by omega), add_zero, div_sub_div_same]
    congr 1
    push_cast
    ring
  · have heq : (j : ℕ) + 1 = n * m := le_antisymm j.isLt hge
    rw [if_neg (by omega), if_pos heq]
    have hj : ((j : ℕ) : ℝ) = ((n * m : ℕ) : ℝ) - 1 := by
      have : ((j : ℕ) : ℝ) + 1 = ((n * m : ℕ) : ℝ) := by exact_mod_cast heq
      linarith
    have hK : ((n * m + 1 : ℕ) : ℝ) = ((n * m : ℕ) : ℝ) + 1 := by push_cast; ring
    rw [hj, hK]
    field_simp
    ring

/-! ### Counting the blocks of a mode -/

/-- The number of blocks before index `l` that the competitor assigns to mode `i`. -/
private def cyc (n i l : ℕ) : ℕ := ((Finset.range l).filter fun j => j % n = i).card

/-- The closed form of the block count: a full quotient of cycles plus one extra block for
the modes already visited in the current cycle. -/
private theorem cyc_eq {n i : ℕ} (hi : i < n) (l : ℕ) :
    cyc n i l = l / n + (if i < l % n then 1 else 0) := by
  have hn : 0 < n := Nat.lt_of_le_of_lt (Nat.zero_le i) hi
  induction l with
  | zero => simp [cyc]
  | succ l ih =>
    have hstep : cyc n i (l + 1) = cyc n i l + (if l % n = i then 1 else 0) := by
      rw [cyc, cyc, Finset.range_add_one, Finset.filter_insert]
      split_ifs with h
      · rw [Finset.card_insert_of_notMem (by simp)]
      · simp
    have hdm : n * (l / n) + l % n = l := Nat.div_add_mod l n
    have hmod : l % n < n := Nat.mod_lt _ hn
    rw [hstep, ih]
    rcases Nat.lt_or_ge (l % n + 1) n with hlt | hge
    · have hrw : l + 1 = n * (l / n) + (l % n + 1) := by omega
      have h1 : (l + 1) % n = l % n + 1 := by
        rw [hrw, Nat.mul_add_mod, Nat.mod_eq_of_lt hlt]
      have h2 : (l + 1) / n = l / n := by
        rw [hrw, Nat.mul_add_div hn, Nat.div_eq_of_lt hlt, add_zero]
      rw [h1, h2]
      split_ifs <;> omega
    · have hfull : l % n + 1 = n := by omega
      have hrw : l + 1 = n * (l / n + 1) := by rw [Nat.mul_succ]; omega
      have h1 : (l + 1) % n = 0 := by rw [hrw, Nat.mul_mod_right]
      have h2 : (l + 1) / n = l / n + 1 := by rw [hrw, Nat.mul_div_cancel_left _ hn]
      rw [h1, h2]
      split_ifs <;> omega

/-- The block count deviates from its ideal value `l / n` by less than one block. -/
private theorem cyc_bounds {n i : ℕ} (hi : i < n) (l : ℕ) :
    n * cyc n i l + 1 ≤ l + n ∧ l + 1 ≤ n * cyc n i l + n := by
  have hn : 0 < n := Nat.lt_of_le_of_lt (Nat.zero_le i) hi
  have hdm : n * (l / n) + l % n = l := Nat.div_add_mod l n
  have hmod : l % n < n := Nat.mod_lt _ hn
  rw [cyc_eq hi, Nat.mul_add]
  split_ifs <;> omega

/-- Over a whole number of cycles every mode receives the same number of blocks. -/
private theorem cyc_mul {n i : ℕ} (hi : i < n) (m : ℕ) :
    cyc n i (n * m) = m := by
  have hn : 0 < n := Nat.lt_of_le_of_lt (Nat.zero_le i) hi
  rw [cyc_eq hi, Nat.mul_mod_right, Nat.mul_div_cancel_left _ hn, if_neg (by omega),
    add_zero]

/-! ### The occupation of the competitor at its switch times -/

/-- At a switch time only the blocks strictly before it contribute to the occupation. -/
private theorem occupation_apply_time {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) (i : Fin n) (l : Fin (k + 1)) :
    occupation p τ i (τ l)
      = ∑ j : Fin k,
          (if (j : ℕ) < (l : ℕ) ∧ p j = i then τ j.succ - τ j.castSucc else 0) := by
  refine Finset.sum_congr rfl fun j _ => ?_
  by_cases hjl : (j : ℕ) < (l : ℕ)
  · have h1 : τ j.succ ≤ τ l := hτ (by rw [Fin.le_def]; simpa using hjl)
    have h2 : τ j.castSucc ≤ τ l := hτ (by rw [Fin.le_def]; simp; omega)
    rw [min_eq_right h1, min_eq_right h2]
    by_cases hp : p j = i <;> simp [hp, hjl]
  · have h1 : τ l ≤ τ j.castSucc := hτ (by rw [Fin.le_def]; simp; omega)
    have h2 : τ l ≤ τ j.succ := h1.trans (hτ (Fin.castSucc_le_succ j))
    rw [min_eq_left h1, min_eq_left h2, sub_self]
    simp [hjl]

/-- Summing a constant over the blocks of one mode before a given index counts them. -/
private theorem sum_ite_sharpWord {n : ℕ} (hn : 0 < n) {m : ℕ} (i : Fin n) {l : ℕ}
    (hl : l ≤ n * m) (c : ℝ) :
    ∑ j : Fin (n * m), (if (j : ℕ) < l ∧ sharpWord hn m j = i then c else 0)
      = (cyc n (i : ℕ) l : ℝ) * c := by
  have hfil : (Finset.range (n * m)).filter (fun j => j < l ∧ j % n = (i : ℕ))
      = (Finset.range l).filter (fun j => j % n = (i : ℕ)) := by
    ext j
    simp only [Finset.mem_filter, Finset.mem_range]
    constructor
    · rintro ⟨-, hjl, hji⟩
      exact ⟨hjl, hji⟩
    · rintro ⟨hjl, hji⟩
      exact ⟨by omega, hjl, hji⟩
  have hstep : ∑ j : Fin (n * m), (if (j : ℕ) < l ∧ sharpWord hn m j = i then c else 0)
      = ∑ j ∈ Finset.range (n * m), (if j < l ∧ j % n = (i : ℕ) then c else 0) := by
    rw [← Fin.sum_univ_eq_sum_range]
    refine Finset.sum_congr rfl fun j _ => ?_
    refine if_congr (and_congr_right fun _ => ?_) rfl rfl
    rw [sharpWord, Fin.ext_iff]
  rw [hstep, ← Finset.sum_filter, hfil, Finset.sum_const, nsmul_eq_mul, cyc]

/-- The occupation of the competitor at a switch time inside the first cell. -/
private theorem sharpSchedule_apply_lt {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) (i : Fin n)
    (l : Fin (n * m + 1)) (hl : (l : ℕ) < n * m) :
    sharpSchedule hn m i (sharpTimes n m l)
      = (cyc n (i : ℕ) (l : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) := by
  rw [sharpSchedule_eq,
    occupation_apply_time _ (orderedTimes_sharpTimes hn hm).mono i l]
  have hterm : ∀ j : Fin (n * m),
      (if (j : ℕ) < (l : ℕ) ∧ sharpWord hn m j = i then
        sharpTimes n m j.succ - sharpTimes n m j.castSucc else 0)
      = (if (j : ℕ) < (l : ℕ) ∧ sharpWord hn m j = i then 1 / ((n * m : ℕ) : ℝ) else 0) := by
    intro j
    by_cases hj : (j : ℕ) < (l : ℕ) ∧ sharpWord hn m j = i
    · rw [if_pos hj, if_pos hj, sharpTimes_block j, if_neg (by omega), add_zero]
    · rw [if_neg hj, if_neg hj]
  rw [Finset.sum_congr rfl fun j _ => hterm j,
    sum_ite_sharpWord hn i (le_of_lt hl) (1 / ((n * m : ℕ) : ℝ))]
  ring

/-- The final block of the competitor selects the distinguished mode. -/
private theorem sharpWord_last {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m)
    (j : Fin (n * m)) (hj : (j : ℕ) + 1 = n * m) : sharpWord hn m j = tailMode hn := by
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  have hmul : n * (m' + 1) = n * m' + n := Nat.mul_succ n m'
  have hjv : (j : ℕ) = n * m' + (n - 1) := by omega
  refine Fin.ext ?_
  change (j : ℕ) % n = n - 1
  rw [hjv, Nat.mul_add_mod, Nat.mod_eq_of_lt (by omega)]

/-- The occupation of the competitor at the horizon: it matches the input exactly. -/
private theorem sharpSchedule_apply_horizon {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m)
    (i : Fin n) (l : Fin (n * m + 1)) (hl : (l : ℕ) = n * m) :
    sharpSchedule hn m i (sharpTimes n m l)
      = (n : ℝ)⁻¹ + (if i = tailMode hn then ((n * m : ℕ) : ℝ) else 0) := by
  have hnm0 : 0 < n * m := Nat.mul_pos hn hm
  have hnm : (0 : ℝ) < ((n * m : ℕ) : ℝ) := by exact_mod_cast hnm0
  rw [sharpSchedule_eq,
    occupation_apply_time _ (orderedTimes_sharpTimes hn hm).mono i l]
  have hsplit : ∀ j : Fin (n * m),
      (if (j : ℕ) < (l : ℕ) ∧ sharpWord hn m j = i then
        sharpTimes n m j.succ - sharpTimes n m j.castSucc else 0)
      = (if (j : ℕ) < (l : ℕ) ∧ sharpWord hn m j = i then 1 / ((n * m : ℕ) : ℝ) else 0)
        + (if (j : ℕ) + 1 = n * m ∧ i = tailMode hn then ((n * m : ℕ) : ℝ) else 0) := by
    intro j
    rw [sharpTimes_block j]
    by_cases hj : (j : ℕ) + 1 = n * m
    · rw [if_pos hj]
      have hlt : (j : ℕ) < (l : ℕ) := by omega
      rw [sharpWord_last hn hm j hj]
      by_cases hi : i = tailMode hn
      · rw [if_pos (And.intro hlt hi.symm), if_pos (And.intro hlt hi.symm),
          if_pos (And.intro hj hi)]
      · rw [if_neg (by rintro ⟨-, h⟩; exact hi h.symm),
          if_neg (by rintro ⟨-, h⟩; exact hi h.symm), if_neg (by rintro ⟨-, h⟩; exact hi h)]
        ring
    · rw [if_neg hj, add_zero, if_neg (fun h : _ ∧ _ => hj h.1), add_zero]
  rw [Finset.sum_congr rfl fun j _ => hsplit j, Finset.sum_add_distrib,
    sum_ite_sharpWord hn i (le_of_eq hl) (1 / ((n * m : ℕ) : ℝ)), hl, cyc_mul i.isLt m]
  have hsecond : ∑ _j : Fin (n * m),
      (if (_j : ℕ) + 1 = n * m ∧ i = tailMode hn then ((n * m : ℕ) : ℝ) else 0)
      = if i = tailMode hn then ((n * m : ℕ) : ℝ) else 0 := by
    rw [Finset.sum_eq_single (⟨n * m - 1, by omega⟩ : Fin (n * m))]
    · refine if_congr (and_iff_right ?_) rfl rfl
      change n * m - 1 + 1 = n * m
      omega
    · intro j _ hj
      refine if_neg ?_
      rintro ⟨h, -⟩
      exact hj (Fin.ext (show (j : ℕ) = n * m - 1 by omega))
    · intro h
      exact absurd (Finset.mem_univ _) h
  rw [hsecond]
  congr 1
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hm' : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hm.ne'
  rw [Nat.cast_mul]
  field_simp


/-! ### The competitor is a schedule with `n m - 1` switches -/

/-- The competitor uses exactly `n m` activation blocks, that is `s = n m - 1` switches. -/
theorem isSchedule_sharpSchedule {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) :
    IsSchedule (n * m) ((n * m + 1 : ℕ) : ℝ) (sharpSchedule hn m) :=
  ⟨sharpWord hn m, sharpTimes n m, orderedTimes_sharpTimes hn hm, rfl⟩

/-- The occupation of the competitor at time one: every mode has been active for exactly
`1 / n`, so all discrepancies vanish there. -/
theorem sharpSchedule_apply_one {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) (i : Fin n) :
    sharpSchedule hn m i 1 = (n : ℝ)⁻¹ := by
  have hnm0 : 0 < n * m := Nat.mul_pos hn hm
  have hnm : (0 : ℝ) < ((n * m : ℕ) : ℝ) := by exact_mod_cast hnm0
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hm' : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hm.ne'
  have hterm : ∀ j : Fin (n * m),
      min (1 : ℝ) (sharpTimes n m j.succ) - min (1 : ℝ) (sharpTimes n m j.castSucc)
        = 1 / ((n * m : ℕ) : ℝ) := by
    intro j
    have hc : sharpTimes n m j.castSucc = ((j : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) :=
      sharpTimes_castSucc j
    have hcle : sharpTimes n m j.castSucc ≤ 1 := by
      rw [hc, div_le_one hnm]
      exact_mod_cast j.isLt.le
    have hval : ((j.succ : Fin (n * m + 1)) : ℕ) = (j : ℕ) + 1 := rfl
    rcases Nat.lt_or_ge ((j : ℕ) + 1) (n * m) with hlt | hge
    · have hs : sharpTimes n m j.succ = (((j : ℕ) + 1 : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) := by
        rw [sharpTimes, hval, if_pos hlt]
      have hsle : sharpTimes n m j.succ ≤ 1 := by
        rw [hs, div_le_one hnm]
        exact_mod_cast hlt.le
      rw [min_eq_right hsle, min_eq_right hcle, hs, hc, div_sub_div_same]
      congr 1
      push_cast
      ring
    · have heq : (j : ℕ) + 1 = n * m := le_antisymm j.isLt hge
      have hs : sharpTimes n m j.succ = ((n * m + 1 : ℕ) : ℝ) := by
        rw [sharpTimes, hval, if_neg (by omega)]
      have hsge : (1 : ℝ) ≤ sharpTimes n m j.succ := by
        rw [hs]
        exact_mod_cast Nat.le_add_left 1 (n * m)
      have hj : ((j : ℕ) : ℝ) = ((n * m : ℕ) : ℝ) - 1 := by
        have h : ((j : ℕ) : ℝ) + 1 = ((n * m : ℕ) : ℝ) := by exact_mod_cast heq
        linarith
      rw [min_eq_left hsge, min_eq_right hcle, hc, hj]
      field_simp
      ring
  have hexp : sharpSchedule hn m i 1
      = ∑ j : Fin (n * m),
          (if sharpWord hn m j = i then
            min (1 : ℝ) (sharpTimes n m j.succ) - min (1 : ℝ) (sharpTimes n m j.castSucc)
            else 0) := rfl
  have hconv : ∀ j : Fin (n * m),
      (if sharpWord hn m j = i then 1 / ((n * m : ℕ) : ℝ) else 0)
        = (if (j : ℕ) < n * m ∧ sharpWord hn m j = i then 1 / ((n * m : ℕ) : ℝ) else 0) :=
    fun j => (if_congr (and_iff_right j.isLt) rfl rfl).symm
  rw [hexp, Finset.sum_congr rfl fun j _ => by rw [hterm j],
    Finset.sum_congr rfl fun j _ => hconv j,
    sum_ite_sharpWord hn i (le_refl (n * m)) (1 / ((n * m : ℕ) : ℝ)), cyc_mul i.isLt m]
  push_cast
  field_simp

/-- SC28, continuous competitor: all discrepancies of the competitor vanish at time one. -/
theorem sharpInput_sub_sharpSchedule_one {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m)
    (i : Fin n) : sharpInput hn (n * m + 1) i 1 - sharpSchedule hn m i 1 = 0 := by
  rw [sharpInput_apply_of_le_one hn (Nat.succ_pos _) i zero_le_one le_rfl,
    sharpSchedule_apply_one hn hm i, one_div, sub_self]

/-! ### The error of the competitor -/

/-- SC28, continuous competitor: the schedule that cycles through all `n` modes inside the
first cell, `m` times, and then stays in the distinguished mode has maximum absolute error
`(n - 1) / (n ^ 2 m)`. -/
theorem D_sharpSchedule_le {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) :
    D (sharpInput hn (n * m + 1)) (sharpSchedule hn m) ((n * m + 1 : ℕ) : ℝ)
      ≤ ((n : ℝ) - 1) / ((n : ℝ) ^ 2 * (m : ℝ)) := by
  have hnm0 : 0 < n * m := Nat.mul_pos hn hm
  have hnm : (0 : ℝ) < ((n * m : ℕ) : ℝ) := by exact_mod_cast hnm0
  have hn0 : (0 : ℝ) < (n : ℝ) := by exact_mod_cast hn
  have hm0 : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  have hn1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hd : (0 : ℝ) < (n : ℝ) ^ 2 * (m : ℝ) := by positivity
  have hc : (0 : ℝ) ≤ ((n : ℝ) - 1) / ((n : ℝ) ^ 2 * (m : ℝ)) :=
    div_nonneg (by linarith) hd.le
  have hNM : ((n * m : ℕ) : ℝ) = (n : ℝ) * (m : ℝ) := by push_cast; ring
  rw [sharpSchedule_eq, D_le_iff_switchTimes _ (orderedTimes_sharpTimes hn hm)
    (isCumulative_sharpInput hn (n * m + 1)) hc]
  intro l i
  rcases Nat.lt_or_ge (l : ℕ) (n * m) with hl | hl
  · have hτ : sharpTimes n m l = ((l : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) := by
      rw [sharpTimes, if_pos hl]
    have ht0 : (0 : ℝ) ≤ sharpTimes n m l := by
      rw [hτ]
      positivity
    have ht1 : sharpTimes n m l ≤ 1 := by
      rw [hτ, div_le_one hnm]
      exact_mod_cast hl.le
    rw [← sharpSchedule_eq, sharpSchedule_apply_lt hn hm i l hl,
      sharpInput_apply_of_le_one hn (Nat.succ_pos _) i ht0 ht1, hτ]
    obtain ⟨hb1, hb2⟩ := cyc_bounds i.isLt (l : ℕ)
    have hb1' : (n : ℝ) * (cyc n (i : ℕ) (l : ℕ) : ℝ) + 1 ≤ ((l : ℕ) : ℝ) + (n : ℝ) := by
      exact_mod_cast hb1
    have hb2' : ((l : ℕ) : ℝ) + 1 ≤ (n : ℝ) * (cyc n (i : ℕ) (l : ℕ) : ℝ) + (n : ℝ) := by
      exact_mod_cast hb2
    have key : ((l : ℕ) : ℝ) / ((n * m : ℕ) : ℝ) / (n : ℝ)
          - (cyc n (i : ℕ) (l : ℕ) : ℝ) / ((n * m : ℕ) : ℝ)
        = (((l : ℕ) : ℝ) - (n : ℝ) * (cyc n (i : ℕ) (l : ℕ) : ℝ))
            / ((n : ℝ) ^ 2 * (m : ℝ)) := by
      rw [hNM]
      field_simp
    rw [key, abs_div, abs_of_pos hd]
    have habs : |((l : ℕ) : ℝ) - (n : ℝ) * (cyc n (i : ℕ) (l : ℕ) : ℝ)| ≤ (n : ℝ) - 1 :=
      abs_le.mpr ⟨by linarith, by linarith⟩
    gcongr
  · have hleq : (l : ℕ) = n * m := le_antisymm (Nat.lt_succ_iff.mp l.isLt) hl
    have hst : sharpTimes n m l = ((n * m + 1 : ℕ) : ℝ) := by
      rw [sharpTimes, if_neg (by omega)]
    rw [← sharpSchedule_eq, sharpSchedule_apply_horizon hn hm i l hleq, hst,
      sharpInput_apply_horizon hn (Nat.succ_pos _) i,
      show ((n * m + 1 : ℕ) : ℝ) - 1 = ((n * m : ℕ) : ℝ) by push_cast; ring, sub_self,
      abs_zero]
    exact hc

/-- SC28, continuous optimum: with the budget `s = n m - 1` the continuous optimum of the
sharpness family is at most `(n - 1) / (n ^ 2 m)`. The source states this quantity as an
upper bound on the continuous optimum, and only the upper bound is used. -/
theorem OPT_sharpInput_le {n : ℕ} (hn : 0 < n) {m : ℕ} (hm : 0 < m) :
    OPT (sharpInput hn (n * m + 1)) ((n * m + 1 : ℕ) : ℝ) (n * m - 1)
      ≤ ((n : ℝ) - 1) / ((n : ℝ) ^ 2 * (m : ℝ)) := by
  have hnm0 : 0 < n * m := Nat.mul_pos hn hm
  have hW : IsSchedule (n * m - 1 + 1) ((n * m + 1 : ℕ) : ℝ) (sharpSchedule hn m) := by
    rw [show n * m - 1 + 1 = n * m by omega]
    exact isSchedule_sharpSchedule hn hm
  exact (OPT_le_D hn (isCumulative_sharpInput hn (n * m + 1)) (Nat.cast_nonneg _) hW).trans
    (D_sharpSchedule_le hn hm)

/-! ## The gap and its consequences -/

/-- The switch budget of the sharpness family satisfies `1 ≤ s ≤ N - 2`, the restricted
regime the cited conjecture assumes. -/
theorem sharp_budget {n m : ℕ} (hn : 2 ≤ n) (hm : 1 ≤ m) :
    1 ≤ n * m - 1 ∧ n * m - 1 ≤ n * m + 1 - 2 := by
  have h : 2 ≤ n * m := le_trans hn (Nat.le_mul_of_pos_right n hm)
  omega

/-- SC28, the gap: on the sharpness family with `N = n m + 1` cells and `s = n m - 1`
switches, the grid optimum exceeds the continuous optimum by at least
`(1 - 1/n) (1 - 1/(n m))`. -/
theorem sharp_gap {n m N s : ℕ} (hn : 0 < n) (hm : 0 < m) (hN : N = n * m + 1)
    (hs : s = n * m - 1) :
    (1 - (n : ℝ)⁻¹) * (1 - ((n : ℝ) * (m : ℝ))⁻¹)
      ≤ gridOPT (unitGrid N) (sharpInput hn N) ((N : ℕ) : ℝ) s
          - OPT (sharpInput hn N) ((N : ℕ) : ℝ) s := by
  subst hN
  subst hs
  have hn0 : (0 : ℝ) < (n : ℝ) := by exact_mod_cast hn
  have hm0 : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  have hid : (1 - (n : ℝ)⁻¹) * (1 - ((n : ℝ) * (m : ℝ))⁻¹)
      = 1 - (n : ℝ)⁻¹ - ((n : ℝ) - 1) / ((n : ℝ) ^ 2 * (m : ℝ)) := by
    field_simp
  rw [gridOPT_sharpInput hn (Nat.succ_pos _), hid]
  linarith [OPT_sharpInput_le hn hm]

/-- SC28, the one-cycle family `N = n + 1`, `s = n - 1`: the gap is at least
`(1 - 1/n)^2`. -/
theorem sharp_gap_sq {n : ℕ} (hn : 0 < n) :
    (1 - (n : ℝ)⁻¹) ^ 2
      ≤ gridOPT (unitGrid (n + 1)) (sharpInput hn (n + 1)) ((n + 1 : ℕ) : ℝ) (n - 1)
          - OPT (sharpInput hn (n + 1)) ((n + 1 : ℕ) : ℝ) (n - 1) := by
  have h := sharp_gap (m := 1) (N := n + 1) (s := n - 1) hn Nat.one_pos (by rw [mul_one])
    (by rw [mul_one])
  rw [Nat.cast_one, mul_one, ← sq] at h
  exact h

/-- SC28, the concrete instance of the manuscript: four modes, five unit cells and three
switches give a gap of at least `9/16`. The hypothesis `0 < 4` is the positivity proof the
family's definitions take as a parameter. -/
theorem sharp_gap_four (h4 : (0 : ℕ) < 4) :
    (9 : ℝ) / 16
      ≤ gridOPT (unitGrid 5) (sharpInput h4 5) ((5 : ℕ) : ℝ) 3
          - OPT (sharpInput h4 5) ((5 : ℕ) : ℝ) 3 := by
  have h := sharp_gap (n := 4) (m := 1) (N := 5) (s := 3) h4 Nat.one_pos (by norm_num)
    (by norm_num)
  norm_num at h
  exact h

/-- SC28: the concrete gap exceeds one half, refuting a universal half-mesh correction. -/
theorem half_lt_sharp_gap_four (h4 : (0 : ℕ) < 4) :
    (1 : ℝ) / 2
      < gridOPT (unitGrid 5) (sharpInput h4 5) ((5 : ℕ) : ℝ) 3
          - OPT (sharpInput h4 5) ((5 : ℕ) : ℝ) 3 := by
  have h := sharp_gap_four h4
  linarith

/-- The one-cycle gap bound tends to one as the mode count grows. -/
theorem tendsto_sharp_gap_bound :
    Filter.Tendsto (fun n : ℕ => (1 - (n : ℝ)⁻¹) ^ 2) Filter.atTop (nhds 1) := by
  have h : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_inv_atTop_nhds_zero_nat
  have h2 : Filter.Tendsto (fun n : ℕ => (1 : ℝ) - (n : ℝ)⁻¹) Filter.atTop (nhds (1 - 0)) :=
    tendsto_const_nhds.sub h
  have h3 := h2.pow 2
  norm_num at h3
  exact h3

/-- SC28, conclusion: no constant strictly below one bounds the instance transfer error
uniformly in the mode count. For every `c < 1` some member of the one-cycle family has a gap
larger than `c`. -/
theorem exists_sharp_gap_gt {c : ℝ} (hc : c < 1) :
    ∃ (n : ℕ) (hn : 0 < n), 2 ≤ n ∧
      c < gridOPT (unitGrid (n + 1)) (sharpInput hn (n + 1)) ((n + 1 : ℕ) : ℝ) (n - 1)
            - OPT (sharpInput hn (n + 1)) ((n + 1 : ℕ) : ℝ) (n - 1) := by
  obtain ⟨n, hgt, hn2⟩ :=
    ((tendsto_sharp_gap_bound.eventually (eventually_gt_nhds hc)).and
      (Filter.eventually_ge_atTop 2)).exists
  exact ⟨n, by omega, hn2, lt_of_lt_of_le hgt (sharp_gap_sq (by omega))⟩

end GridSwitching
