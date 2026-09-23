import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.OneSwitch

/-!
# SC12 and SC13: the two linear-program families and the floor `T / 3`

This module proves the two tier-2 obligations of `topics/17-grid-switching/CLAIMS.md` that
supply *lower bounds* for the arbitrary-grid one-switch minimax value: the sufficiency half of
the linear-program characterization `eq:grid-LP`, and the floor `T / 3`.

## SC12: the two families and sufficiency

Fix a grid `x` with `IsGrid x T`, a mode count `n ≥ 3`, and two cell indices `ja jb : Fin N`.
Using cell indices rather than node indices encodes `1 ≤ a ≤ b ≤ N` directly: the four
quantities of the source are `A = x ja.succ`, `P = x ja.castSucc`, `B = x jb.succ` and
`Q = x jb.castSucc`. The inequality `a ≤ b` is not assumed; it follows from the constraints
(`LPCommon.index_le`).

* `LPCommon` is the common constraint block of `eq:grid-LP` in the variables `u v m : Fin 3 → ℝ`
  and `E : ℝ`, with the weights `w = (1, 1, n - 2)` of `lpWeight`. Component `2` describes each
  of the `n - 2` bulk modes separately, not their sum.
* `AllInitialFeasible` adds `u 2 + E ≤ A`; `TwoLargeFeasible` instead adds `m 1 ≥ E`. As the
  source insists, the first family does **not** impose `m 1 ≤ E`; that restriction is used only
  in the coverage argument (SC14), which is not part of this module.
* `lpInput` is the relaxed control obtained from a feasible point by linear interpolation
  through the four times `0, A, B, T`. Since `A` and `B` are grid nodes it is grid constant
  (`isGridConstant_lpInput`) and cumulative (`isCumulative_lpInput`); the rates are nonnegative
  because the states are nondecreasing and sum to one on every cell because of the three
  weighted equalities (`isRateMatrix_lpRates`).
* `allInitial_le_gridOPT` and `twoLarge_le_gridOPT` are sufficiency: every grid one-switch
  schedule has error at least `E` against that input. Their packaged forms are
  `exists_gridConstant_of_allInitialFeasible`, `exists_gridConstant_of_twoLargeFeasible`, and
  the minimax forms `allInitial_le_gridF`, `twoLarge_le_gridF`.

The proof follows the source. Every grid schedule with two activation blocks is a one-switch
schedule whose switch time is a grid node (`exists_oneSwitch_of_isGridSchedule`), constant
schedules included as the degenerate `oneSwitch p p τ T` (`oneSwitch_self_eq`). A switch
strictly before the cutoff node lies at or before the previous node, so its final deficit is at
least `E`; a switch at or after the cutoff node has initial deficit at least `E`, because
`t - A p t` is nondecreasing (`initialDeficit_mono`). This is `E_le_D_oneSwitch`. In the
all-initial-modes family the dominance reduction `oneSwitch_reduction` leaves only `p → 0` with
`p ≠ 0` and `0 → 1`, and both are obstructed. In the two-large-modes family no reduction is
needed: a schedule omitting mode `0` or mode `1` already errs by at least `m 1 ≥ E`, and the two
remaining orders are obstructed by the common constraints.

Zero-length phases are covered rather than excluded: equal weighted sums together with
componentwise monotonicity force equal states (`eq_of_lpWeighted_eq`), so `a = b` and `b = N`
need no separate treatment.

## SC13: the floor

`third_le_gridF`: on every grid, `T / 3 ≤ gridF x n 1 T` for `n ≥ 3`, witnessed by the input
that runs the first three modes at rate `1/3` throughout (`thirdsInput`). A one-switch schedule
activates at most two modes, so it omits one of the three, and by `lem:one-switch-error` its
error is at least that omitted terminal mass.

## Hypotheses added beyond the sources

`3 ≤ n` is stated explicitly wherever it is used: it makes the bulk weight `n - 2` positive,
which is what forces equal states on empty phases, and it provides the two distinguished modes.
`IsGrid x T` replaces the source's implicit assumption that the grid data are the nodes of a
strictly increasing grid on `[0, T]`; `N = 0` is not excluded, and then `T = 0` and the
statements remain true. Nothing here assumes `T > 0`.

This module proves only sufficiency. Coverage (SC14), the boundary case (SC15) and the
elimination of the two-large-modes family (SC16--SC19) are separate obligations, so no claim is
made here that the programs are feasible or that their optimal values are attained.
-/

namespace GridSwitching

open Set

variable {n N : ℕ}

/-! ## Weights, mode classes and cell blocks -/

/-- The weight vector `w = (1, 1, n - 2)` of `eq:grid-LP`: component `2` stands for each of the
`n - 2` bulk modes, not for their sum. -/
noncomputable def lpWeight (n : ℕ) : Fin 3 → ℝ := ![1, 1, (n : ℝ) - 2]

/-- The weighted sum `∑ j, w j * f j` of `eq:grid-LP`. -/
noncomputable def lpWeighted (n : ℕ) (f : Fin 3 → ℝ) : ℝ := ∑ j, lpWeight n j * f j

/-- The weighted sum, written out. -/
theorem lpWeighted_eq (n : ℕ) (f : Fin 3 → ℝ) :
    lpWeighted n f = f 0 + f 1 + ((n : ℝ) - 2) * f 2 := by
  simp [lpWeighted, lpWeight, Fin.sum_univ_three]

/-- The class of a mode: the two distinguished modes `0` and `1` have classes `0` and `1`, and
every other mode has the bulk class `2`. -/
def modeClass {n : ℕ} (i : Fin n) : Fin 3 :=
  if (i : ℕ) = 0 then 0 else if (i : ℕ) = 1 then 1 else 2

@[simp] theorem modeClass_of_val_zero {i : Fin n} (h : (i : ℕ) = 0) : modeClass i = 0 := by
  simp [modeClass, h]

@[simp] theorem modeClass_of_val_one {i : Fin n} (h : (i : ℕ) = 1) : modeClass i = 1 := by
  simp [modeClass, h]

theorem modeClass_of_two_le {i : Fin n} (h : 2 ≤ (i : ℕ)) : modeClass i = 2 := by
  have h0 : (i : ℕ) ≠ 0 := by omega
  have h1 : (i : ℕ) ≠ 1 := by omega
  simp [modeClass, h0, h1]

/-- The number of modes with index below `k`. -/
private theorem card_filter_val_lt {k : ℕ} (hk : k ≤ n) :
    (Finset.univ.filter (fun i : Fin n => (i : ℕ) < k)).card = k := by
  classical
  have himg : (Finset.univ.filter (fun i : Fin n => (i : ℕ) < k)) =
      Finset.univ.image (Fin.castLE hk) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_image]
    constructor
    · intro hi
      exact ⟨⟨(i : ℕ), hi⟩, Fin.ext rfl⟩
    · rintro ⟨j, -, rfl⟩
      exact j.isLt
  rw [himg, Finset.card_image_of_injective _ (Fin.castLE_injective hk), Finset.card_univ,
    Fintype.card_fin]

/-- Summing a function of the mode class reproduces the weighted sum with weights
`w = (1, 1, n - 2)`. -/
theorem sum_modeClass (hn : 3 ≤ n) (f : Fin 3 → ℝ) :
    ∑ i : Fin n, f (modeClass i) = lpWeighted n f := by
  classical
  have h0 : (0 : ℕ) < n := by omega
  have h1 : (1 : ℕ) < n := by omega
  have hpair : (Finset.univ.filter (fun i : Fin n => (i : ℕ) < 2)) =
      ({⟨0, h0⟩, ⟨1, h1⟩} : Finset (Fin n)) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert,
      Finset.mem_singleton, Fin.ext_iff]
    omega
  have hne : (⟨0, h0⟩ : Fin n) ≠ ⟨1, h1⟩ := by
    simp [Fin.ext_iff]
  have hcard : (Finset.univ.filter (fun i : Fin n => ¬ (i : ℕ) < 2)).card = n - 2 := by
    have hsum := Finset.card_filter_add_card_filter_not
      (s := (Finset.univ : Finset (Fin n))) (p := fun i : Fin n => (i : ℕ) < 2)
    rw [card_filter_val_lt (by omega : 2 ≤ n), Finset.card_univ, Fintype.card_fin] at hsum
    omega
  rw [← Finset.sum_filter_add_sum_filter_not Finset.univ (fun i : Fin n => (i : ℕ) < 2),
    hpair, Finset.sum_pair hne]
  have hbulk : ∀ i ∈ (Finset.univ.filter (fun i : Fin n => ¬ (i : ℕ) < 2)),
      f (modeClass i) = f 2 := by
    intro i hi
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, not_lt] at hi
    rw [modeClass_of_two_le hi]
  rw [Finset.sum_congr rfl hbulk, Finset.sum_const, hcard, nsmul_eq_mul,
    Nat.cast_sub (by omega : 2 ≤ n), lpWeighted_eq]
  simp

/-- Summing a constant over the first three modes. -/
private theorem sum_ite_val_lt_three (hn : 3 ≤ n) (c : ℝ) :
    ∑ i : Fin n, (if (i : ℕ) < 3 then c else 0) = 3 * c := by
  classical
  rw [← Finset.sum_filter, Finset.sum_const, card_filter_val_lt hn, nsmul_eq_mul]
  norm_num

/-- Telescoping the cells of a block: the cells with index in `[k₁, k₂)` contribute the
increment of the clipped time between the grid nodes `k₁` and `k₂`. -/
private theorem sum_cell_block (x : Fin (N + 1) → ℝ) (t c : ℝ) {k₁ k₂ : ℕ}
    (h₁₂ : k₁ ≤ k₂) (h₂ : k₂ ≤ N) :
    (∑ j : Fin N, if k₁ ≤ (j : ℕ) ∧ (j : ℕ) < k₂ then
        c * (min t (x j.succ) - min t (x j.castSucc)) else 0) =
      c * (min t (x ⟨k₂, by omega⟩) - min t (x ⟨k₁, by omega⟩)) := by
  classical
  have hgcast : ∀ j : Fin N,
      min t (x ⟨min (j : ℕ) N, by omega⟩) = min t (x j.castSucc) := by
    intro j
    have h : (⟨min (j : ℕ) N, by omega⟩ : Fin (N + 1)) = j.castSucc :=
      Fin.ext (by simp)
    rw [h]
  have hgsucc : ∀ j : Fin N,
      min t (x ⟨min ((j : ℕ) + 1) N, by omega⟩) = min t (x j.succ) := by
    intro j
    have h : (⟨min ((j : ℕ) + 1) N, by omega⟩ : Fin (N + 1)) = j.succ :=
      Fin.ext (by simp [Nat.succ_le_of_lt j.isLt])
    rw [h]
  have key : ∀ j : Fin N,
      (if k₁ ≤ (j : ℕ) ∧ (j : ℕ) < k₂ then
          c * (min t (x j.succ) - min t (x j.castSucc)) else 0) =
        (if k₁ ≤ (j : ℕ) ∧ (j : ℕ) < k₂ then
          c * (min t (x ⟨min ((j : ℕ) + 1) N, by omega⟩) -
            min t (x ⟨min ((j : ℕ)) N, by omega⟩)) else 0) := by
    intro j
    rw [hgcast j, hgsucc j]
  rw [Finset.sum_congr rfl (fun j _ => key j),
    Fin.sum_univ_eq_sum_range (fun k : ℕ => if k₁ ≤ k ∧ k < k₂ then
      c * (min t (x ⟨min (k + 1) N, by omega⟩) - min t (x ⟨min k N, by omega⟩)) else 0) N,
    ← Finset.sum_filter]
  have hfil : ((Finset.range N).filter (fun k => k₁ ≤ k ∧ k < k₂)) = Finset.Ico k₁ k₂ := by
    ext k
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
    omega
  rw [hfil, ← Finset.mul_sum,
    Finset.sum_Ico_sub (fun k : ℕ => min t (x ⟨min k N, by omega⟩)) h₁₂]
  simp only [min_eq_left h₂, min_eq_left (h₁₂.trans h₂)]

/-- The same telescoping, with the block endpoints presented as grid indices. -/
private theorem sum_cell_phase (x : Fin (N + 1) → ℝ) (t c : ℝ) {k₁ k₂ : ℕ}
    (q₁ q₂ : Fin (N + 1)) (h : k₁ ≤ k₂) (h₁ : (q₁ : ℕ) = k₁) (h₂ : (q₂ : ℕ) = k₂) :
    (∑ j : Fin N, if k₁ ≤ (j : ℕ) ∧ (j : ℕ) < k₂ then
        c * (min t (x j.succ) - min t (x j.castSucc)) else 0) =
      c * (min t (x q₂) - min t (x q₁)) := by
  subst h₁
  subst h₂
  exact sum_cell_block x t c h (Nat.lt_succ_iff.mp q₂.isLt)

/-! ## SC12: the two linear-program families -/

/-- The common constraint block of `eq:grid-LP`, for the grid `x` on the horizon `T`, the cell
indices `ja` and `jb` (so that `A = x ja.succ`, `P = x ja.castSucc`, `B = x jb.succ` and
`Q = x jb.castSucc`, which encodes `1 ≤ a ≤ b ≤ N`), the endpoint states `u`, `v`, `m` and the
objective value `E`. Component `2` describes each of the `n - 2` bulk modes separately, which
is why the equalities are weighted by `lpWeight n`. -/
structure LPCommon (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N)
    (u v m : Fin 3 → ℝ) (E : ℝ) : Prop where
  /-- The states at `A` are nonnegative. -/
  u_nonneg : ∀ j, 0 ≤ u j
  /-- The states are nondecreasing from `A` to `B`. -/
  u_le_v : ∀ j, u j ≤ v j
  /-- The states are nondecreasing from `B` to `T`. -/
  v_le_m : ∀ j, v j ≤ m j
  /-- The terminal masses are ordered: `m 0 ≥ m 1`. -/
  m_one_le_m_zero : m 1 ≤ m 0
  /-- The terminal masses are ordered: `m 1 ≥ m 2`. -/
  m_two_le_m_one : m 2 ≤ m 1
  /-- The objective is at least `T / 3`. -/
  horizon_third_le : T / 3 ≤ E
  /-- The weighted states at `A` sum to `A`. -/
  weighted_u : lpWeighted n u = x ja.succ
  /-- The weighted states at `B` sum to `B`. -/
  weighted_v : lpWeighted n v = x jb.succ
  /-- The weighted terminal masses sum to `T`. -/
  weighted_m : lpWeighted n m = T
  /-- Lower cutoff at `A`: `T - A ≤ E + m 0`. -/
  cutoff_a_lower : T - x ja.succ ≤ E + m 0
  /-- Upper cutoff at `A`: `E + m 0 ≤ T - P`. -/
  cutoff_a_upper : E + m 0 ≤ T - x ja.castSucc
  /-- Lower cutoff at `B`: `T - B ≤ E + m 1`. -/
  cutoff_b_lower : T - x jb.succ ≤ E + m 1
  /-- Upper cutoff at `B`: `E + m 1 ≤ T - Q`. -/
  cutoff_b_upper : E + m 1 ≤ T - x jb.castSucc
  /-- Initial-deficit constraint at `A` for the distinguished mode `1`. -/
  deficit_a : u 1 + E ≤ x ja.succ
  /-- Initial-deficit constraint at `B` for the distinguished mode `0`. -/
  deficit_b : v 0 + E ≤ x jb.succ

/-- The all-initial-modes family of `eq:grid-LP`: the common block together with the
initial-deficit constraint at `A` for the bulk modes. It deliberately does **not** impose
`m 1 ≤ E`. -/
structure AllInitialFeasible (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N)
    (u v m : Fin 3 → ℝ) (E : ℝ) : Prop where
  /-- The common constraint block. -/
  common : LPCommon n x T ja jb u v m E
  /-- Initial-deficit constraint at `A` for each of the `n - 2` bulk modes. -/
  deficit_a_bulk : u 2 + E ≤ x ja.succ

/-- The two-large-modes family of `eq:grid-LP`: the common block together with `m 1 ≥ E`. -/
structure TwoLargeFeasible (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N)
    (u v m : Fin 3 → ℝ) (E : ℝ) : Prop where
  /-- The common constraint block. -/
  common : LPCommon n x T ja jb u v m E
  /-- The second largest terminal mass is at least the objective. -/
  E_le_m_one : E ≤ m 1

/-! ### Elementary consequences of the weighted equalities -/

/-- The weighted sum is monotone in the state vector. -/
theorem lpWeighted_mono (hn : 3 ≤ n) {f g : Fin 3 → ℝ} (h : ∀ j, f j ≤ g j) :
    lpWeighted n f ≤ lpWeighted n g := by
  have hw : (0 : ℝ) ≤ (n : ℝ) - 2 := by
    have h3 : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  rw [lpWeighted_eq, lpWeighted_eq]
  have := mul_le_mul_of_nonneg_left (h 2) hw
  linarith [h 0, h 1]

/-- Equal times force equal states: if two ordered state vectors have the same weighted sum,
they are equal. This is what makes zero-length phases harmless. -/
theorem eq_of_lpWeighted_eq (hn : 3 ≤ n) {f g : Fin 3 → ℝ} (hle : ∀ j, f j ≤ g j)
    (heq : lpWeighted n f = lpWeighted n g) (j : Fin 3) : f j = g j := by
  have hw : (0 : ℝ) < (n : ℝ) - 2 := by
    have h3 : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  rw [lpWeighted_eq, lpWeighted_eq] at heq
  have h2 : 0 ≤ ((n : ℝ) - 2) * (g 2 - f 2) := mul_nonneg hw.le (sub_nonneg.mpr (hle 2))
  have hz2 : ((n : ℝ) - 2) * (g 2 - f 2) = 0 := by nlinarith [hle 0, hle 1]
  have hf2 : f 2 = g 2 := by
    rcases mul_eq_zero.mp hz2 with h | h
    · exact absurd h (ne_of_gt hw)
    · linarith
  rw [hf2] at heq
  fin_cases j
  · change f 0 = g 0
    linarith [hle 0, hle 1]
  · change f 1 = g 1
    linarith [hle 0, hle 1]
  · change f 2 = g 2
    exact hf2

variable {x : Fin (N + 1) → ℝ} {T : ℝ} {ja jb : Fin N} {u v m : Fin 3 → ℝ} {E : ℝ}

/-- The first phase of the interpolation has positive length: `A > 0`, because `a ≥ 1`. -/
theorem IsGrid.zero_lt_succ (hx : IsGrid x T) (j : Fin N) : 0 < x j.succ := by
  have hlt : (0 : Fin (N + 1)) < j.succ := by
    rw [Fin.lt_def, Fin.val_zero, Fin.val_succ]
    omega
  have h : x 0 < x j.succ := hx.strictMono hlt
  rwa [hx.first] at h

/-- A feasible point has `a ≤ b`: the weighted state at `A` is below the one at `B`. -/
theorem LPCommon.index_le (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) : (ja : ℕ) ≤ (jb : ℕ) := by
  have h : x ja.succ ≤ x jb.succ := by
    rw [← hc.weighted_u, ← hc.weighted_v]
    exact lpWeighted_mono hn hc.u_le_v
  have h2 : ja.succ ≤ jb.succ := hx.strictMono.le_iff_le.mp h
  have h3 : (ja : ℕ) + 1 ≤ (jb : ℕ) + 1 := h2
  omega

/-- A feasible point has `A ≤ B`. -/
theorem LPCommon.node_le (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E) :
    x ja.succ ≤ x jb.succ := by
  rw [← hc.weighted_u, ← hc.weighted_v]
  exact lpWeighted_mono hn hc.u_le_v

/-- A feasible point has `B ≤ T`. -/
theorem LPCommon.node_le_horizon (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E) :
    x jb.succ ≤ T := by
  rw [← hc.weighted_v, ← hc.weighted_m]
  exact lpWeighted_mono hn hc.v_le_m

/-- The weighted sum is additive in the state vector. -/
theorem lpWeighted_sub (n : ℕ) (f g : Fin 3 → ℝ) :
    lpWeighted n (fun j => f j - g j) = lpWeighted n f - lpWeighted n g := by
  simp only [lpWeighted_eq]
  ring

/-! ### The interpolated input

The relaxed input attached to a feasible point interpolates linearly through the four times
`0, A, B, T`. Because `A` and `B` are grid nodes this is a grid-constant input: on each cell
the rate is the increment of the enclosing phase divided by its length. -/

/-- The per-cell rate matrix of the interpolation through `0, A, B, T`. Component `0` of the
state vectors describes mode `0`, component `1` describes mode `1`, and component `2`
describes each of the remaining `n - 2` modes. -/
noncomputable def lpRates (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N)
    (u v m : Fin 3 → ℝ) : Fin N → Fin n → ℝ := fun j i =>
  if (j : ℕ) < (ja : ℕ) + 1 then u (modeClass i) / x ja.succ
  else if (j : ℕ) < (jb : ℕ) + 1 then
    (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ)
  else (m (modeClass i) - v (modeClass i)) / (T - x jb.succ)

/-- The relaxed input attached to a feasible point of `eq:grid-LP`. -/
noncomputable def lpInput (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N)
    (u v m : Fin 3 → ℝ) : Fin n → ℝ → ℝ :=
  gridCumulative x (lpRates n x T ja jb u v m)

/-- Cells of the second phase have `A < B`. -/
private theorem node_lt_of_phase_two (hx : IsGrid x T) {j : Fin N}
    (h1 : ¬ (j : ℕ) < (ja : ℕ) + 1) (h2 : (j : ℕ) < (jb : ℕ) + 1) :
    x ja.succ < x jb.succ := by
  refine hx.strictMono ?_
  rw [Fin.lt_def, Fin.val_succ, Fin.val_succ]
  omega

/-- Cells of the third phase have `B < T`. -/
private theorem node_lt_of_phase_three (hx : IsGrid x T) {j : Fin N}
    (h2 : ¬ (j : ℕ) < (jb : ℕ) + 1) : x jb.succ < T := by
  have hj : (j : ℕ) < N := j.isLt
  have h : x jb.succ < x (Fin.last N) := by
    refine hx.strictMono ?_
    rw [Fin.lt_def, Fin.val_succ, Fin.val_last]
    omega
  rwa [hx.last] at h

/-- SC12, first half: the interpolation is a genuine grid-constant relaxed control. The rates
are nonnegative because the states are nondecreasing, and they sum to one on every cell
because of the three weighted sum equalities. -/
theorem isRateMatrix_lpRates (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) : IsRateMatrix (lpRates n x T ja jb u v m) where
  nonneg j i := by
    simp only [lpRates]
    split_ifs with h1 h2
    · exact div_nonneg (hc.u_nonneg _) (hx.zero_lt_succ ja).le
    · exact div_nonneg (sub_nonneg.mpr (hc.u_le_v _))
        (sub_nonneg.mpr (node_lt_of_phase_two hx h1 h2).le)
    · exact div_nonneg (sub_nonneg.mpr (hc.v_le_m _))
        (sub_nonneg.mpr (node_lt_of_phase_three hx h2).le)
  conservation j := by
    simp only [lpRates]
    split_ifs with h1 h2
    · rw [← Finset.sum_div, sum_modeClass hn u, hc.weighted_u]
      exact div_self (hx.zero_lt_succ ja).ne'
    · rw [← Finset.sum_div, sum_modeClass hn (fun c => v c - u c), lpWeighted_sub,
        hc.weighted_v, hc.weighted_u]
      exact div_self (sub_ne_zero.mpr (node_lt_of_phase_two hx h1 h2).ne')
    · rw [← Finset.sum_div, sum_modeClass hn (fun c => m c - v c), lpWeighted_sub,
        hc.weighted_m, hc.weighted_v]
      exact div_self (sub_ne_zero.mpr (node_lt_of_phase_three hx h2).ne')

/-- The interpolated input is grid constant. -/
theorem isGridConstant_lpInput (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) :
    IsGridConstant x (lpInput n x T ja jb u v m) :=
  ⟨_, isRateMatrix_lpRates hn hx hc, rfl⟩

/-- The interpolated input lies in the cumulative class. -/
theorem isCumulative_lpInput (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) : IsCumulative (lpInput n x T ja jb u v m) T :=
  gridCumulative_isCumulative hx.orderedTimes (isRateMatrix_lpRates hn hx hc)

/-- The interpolated input, written out as its three linear phases. -/
theorem lpInput_apply (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) (t : ℝ) :
    lpInput n x T ja jb u v m i t =
      u (modeClass i) / x ja.succ * (min t (x ja.succ) - min t 0) +
        (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ) *
          (min t (x jb.succ) - min t (x ja.succ)) +
        (m (modeClass i) - v (modeClass i)) / (T - x jb.succ) *
          (min t T - min t (x jb.succ)) := by
  have hab : (ja : ℕ) ≤ (jb : ℕ) := hc.index_le hn hx
  have hjb : (jb : ℕ) < N := jb.isLt
  have key : ∀ j : Fin N,
      lpRates n x T ja jb u v m j i * (min t (x j.succ) - min t (x j.castSucc)) =
        (if 0 ≤ (j : ℕ) ∧ (j : ℕ) < (ja : ℕ) + 1 then
            u (modeClass i) / x ja.succ * (min t (x j.succ) - min t (x j.castSucc))
          else 0) +
        (if (ja : ℕ) + 1 ≤ (j : ℕ) ∧ (j : ℕ) < (jb : ℕ) + 1 then
            (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ) *
              (min t (x j.succ) - min t (x j.castSucc))
          else 0) +
        (if (jb : ℕ) + 1 ≤ (j : ℕ) ∧ (j : ℕ) < N then
            (m (modeClass i) - v (modeClass i)) / (T - x jb.succ) *
              (min t (x j.succ) - min t (x j.castSucc))
          else 0) := by
    intro j
    have hjN : (j : ℕ) < N := j.isLt
    simp only [lpRates]
    split_ifs <;> first | omega | ring
  simp only [lpInput, gridCumulative]
  rw [Finset.sum_congr rfl fun j _ => key j, Finset.sum_add_distrib, Finset.sum_add_distrib,
    sum_cell_phase (k₁ := 0) (k₂ := (ja : ℕ) + 1) x t _ 0 ja.succ (Nat.zero_le _) (by simp) rfl,
    sum_cell_phase (k₁ := (ja : ℕ) + 1) (k₂ := (jb : ℕ) + 1) x t _ ja.succ jb.succ (by omega)
      rfl rfl,
    sum_cell_phase (k₁ := (jb : ℕ) + 1) (k₂ := N) x t _ jb.succ (Fin.last N) (by omega) rfl
      (by simp),
    hx.first, hx.last]

/-- The first phase carries the state `u`. -/
private theorem phase_one_mul (hx : IsGrid x T) (c : ℝ) :
    c / x ja.succ * x ja.succ = c :=
  div_mul_cancel₀ _ (hx.zero_lt_succ ja).ne'

/-- The second phase carries the increment from `u` to `v`, also when it is empty. -/
private theorem phase_two_mul (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E) (i : Fin n) :
    (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ) *
        (x jb.succ - x ja.succ) = v (modeClass i) - u (modeClass i) := by
  rcases eq_or_lt_of_le (hc.node_le hn) with heq | hlt
  · have h : u (modeClass i) = v (modeClass i) :=
      eq_of_lpWeighted_eq hn hc.u_le_v (by rw [hc.weighted_u, hc.weighted_v, heq]) _
    rw [← heq, sub_self, mul_zero, h, sub_self]
  · exact div_mul_cancel₀ _ (sub_pos.mpr hlt).ne'

/-- The third phase carries the increment from `v` to `m`, also when it is empty. -/
private theorem phase_three_mul (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E) (i : Fin n) :
    (m (modeClass i) - v (modeClass i)) / (T - x jb.succ) * (T - x jb.succ) =
      m (modeClass i) - v (modeClass i) := by
  rcases eq_or_lt_of_le (hc.node_le_horizon hn) with heq | hlt
  · have h : v (modeClass i) = m (modeClass i) :=
      eq_of_lpWeighted_eq hn hc.v_le_m (by rw [hc.weighted_v, hc.weighted_m, heq]) _
    rw [← heq, sub_self, mul_zero, h, sub_self]
  · exact div_mul_cancel₀ _ (sub_pos.mpr hlt).ne'

/-- At the node `A` the interpolated input has the state `u`. -/
theorem lpInput_at_a (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) : lpInput n x T ja jb u v m i (x ja.succ) = u (modeClass i) := by
  have hA : 0 < x ja.succ := hx.zero_lt_succ ja
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  rw [lpInput_apply hn hx hc, min_self, min_eq_right hA.le, min_eq_left hAB,
    min_eq_left (hAB.trans hBT), sub_zero, phase_one_mul hx]
  ring

/-- At the node `B` the interpolated input has the state `v`. -/
theorem lpInput_at_b (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) : lpInput n x T ja jb u v m i (x jb.succ) = v (modeClass i) := by
  have hA : 0 < x ja.succ := hx.zero_lt_succ ja
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  rw [lpInput_apply hn hx hc, min_self, min_eq_right hAB, min_eq_right (hA.le.trans hAB),
    min_eq_left hBT, sub_zero, phase_one_mul hx, phase_two_mul hn hc]
  ring

/-- The terminal masses of the interpolated input are the state `m`. -/
theorem lpInput_mass (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) : lpInput n x T ja jb u v m i T = m (modeClass i) := by
  have hA : 0 < x ja.succ := hx.zero_lt_succ ja
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  rw [lpInput_apply hn hx hc, min_self, min_eq_right hBT, min_eq_right (hAB.trans hBT),
    min_eq_right (hA.le.trans (hAB.trans hBT)), sub_zero, phase_one_mul hx,
    phase_two_mul hn hc, phase_three_mul hn hc]
  ring

/-! ### Grid one-switch schedules

Every grid schedule with two activation blocks is a one-switch schedule whose switch time is
a grid node, including the constant schedules, which appear as `oneSwitch p p τ T`. -/

/-- A degenerate one-switch schedule, whose two modes agree, is the one-switch schedule that
switches at time zero from an arbitrary mode. -/
theorem oneSwitch_self_eq {n : ℕ} (p q : Fin n) (τ T : ℝ) :
    oneSwitch p p τ T = oneSwitch q p 0 T := by
  have h : oneSwitch p p τ T = oneSwitch p p 0 T := by
    funext i t
    rw [oneSwitch_apply, oneSwitch_apply]
    split_ifs <;> ring
  rw [h, oneSwitch_zero, oneSwitch_zero]

/-- A grid schedule with two activation blocks is a one-switch schedule that switches at a
grid node. -/
theorem exists_oneSwitch_of_isGridSchedule (hx : IsGrid x T) {W : Fin n → ℝ → ℝ}
    (hW : IsGridSchedule x 2 W) :
    ∃ (p q : Fin n) (c : Fin (N + 1)), W = oneSwitch p q (x c) T := by
  obtain ⟨p, g, -, hg0, hgl, rfl⟩ := hW
  refine ⟨p 0, p 1, g 1, ?_⟩
  unfold oneSwitch
  congr 1
  · funext i
    fin_cases i <;> rfl
  · funext i
    fin_cases i
    · change x (g 0) = 0
      rw [hg0, hx.first]
    · rfl
    · change x (g 2) = T
      rw [show (2 : Fin 3) = Fin.last 2 from rfl, hgl, hx.last]

/-! ### SC12: sufficiency

The two obstructions of the source. A grid switch strictly before the cutoff node has final
deficit at least `E`, because the switch time is then at most the previous node; a grid switch
at or after the cutoff node has initial deficit at least `E`, because `t - A p t` is
nondecreasing. -/

/-- The obstruction estimate: if the final mode `f` satisfies the upper cutoff inequality at
the cell `jc` and the initial mode `p` satisfies the initial-deficit inequality at the node
`x jc.succ`, then the switch `p → f` has error at least `E` at every grid node. -/
theorem E_le_D_oneSwitch (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T)
    (jc : Fin N) {p f : Fin n} (hpf : p ≠ f)
    (hfin : E + masses A T f ≤ T - x jc.castSucc)
    (hinit : A p (x jc.succ) + E ≤ x jc.succ) (c : Fin (N + 1)) :
    E ≤ D A (oneSwitch p f (x c) T) T := by
  have hmem : x c ∈ Icc (0 : ℝ) T := hx.mem_Icc c
  rw [D_oneSwitch hA hpf hmem.1 hmem.2]
  rcases lt_or_ge (x c) (x jc.succ) with h | h
  · refine le_trans ?_ ((le_max_right _ _).trans (le_max_right _ _))
    have hlt : c < jc.succ := hx.strictMono.lt_iff_lt.mp h
    have hcle : x c ≤ x jc.castSucc := by
      refine hx.strictMono.monotone ?_
      rw [Fin.lt_def, Fin.val_succ] at hlt
      rw [Fin.le_def, Fin.val_castSucc]
      omega
    simp only [finalDeficit]
    linarith
  · refine le_trans ?_ ((le_max_left _ _).trans (le_max_right _ _))
    have hmono := initialDeficit_mono hA p (hx.zero_lt_succ jc).le h hmem.2
    simp only [initialDeficit] at hmono ⊢
    linarith

/-- Every terminal mass is at most `m 0`. -/
private theorem m_modeClass_le_zero (hc : LPCommon n x T ja jb u v m E) (i : Fin n) :
    m (modeClass i) ≤ m 0 := by
  unfold modeClass
  split_ifs
  · exact le_rfl
  · exact hc.m_one_le_m_zero
  · exact hc.m_two_le_m_one.trans hc.m_one_le_m_zero

/-- Every terminal mass other than that of mode `0` is at most `m 1`. -/
private theorem m_modeClass_le_one (hc : LPCommon n x T ja jb u v m E) {i : Fin n}
    (hi : (i : ℕ) ≠ 0) : m (modeClass i) ≤ m 1 := by
  unfold modeClass
  rw [if_neg hi]
  split_ifs
  · exact le_rfl
  · exact hc.m_two_le_m_one

/-- A schedule that omits a mode of terminal mass at least `E` has error at least `E`. -/
private theorem E_le_D_of_omitted (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) {i p q : Fin n} (hip : i ≠ p) (hiq : i ≠ q)
    (hE : E ≤ m (modeClass i)) {τ : ℝ} (hτ : τ ∈ Icc (0 : ℝ) T) :
    E ≤ D (lpInput n x T ja jb u v m) (oneSwitch p q τ T) T := by
  have hA := isCumulative_lpInput hn hx hc
  have hW := isCumulative_oneSwitch hτ.1 hτ.2 p q
  have hT : T ∈ Icc (0 : ℝ) T := ⟨hx.horizon_nonneg, le_rfl⟩
  have h := le_D hA hW i hT
  rw [oneSwitch_of_ne hip hiq, sub_zero, abs_of_nonneg (hA.nonneg i hT),
    lpInput_mass hn hx hc] at h
  exact hE.trans h

/-- SC12, sufficiency for the all-initial-modes family at a fixed ordered pair of distinct
modes and a fixed grid switch time. By dominance only `p → 0` with `p ≠ 0` and `0 → 1` have to
be obstructed, and the all-initial-modes constraint covers every initial mode `p ≠ 0`. -/
theorem allInitial_le_D_oneSwitch (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) {p q : Fin n} (hpq : p ≠ q)
    (c : Fin (N + 1)) :
    E ≤ D (lpInput n x T ja jb u v m) (oneSwitch p q (x c) T) T := by
  have hc := hf.common
  have hA := isCumulative_lpInput hn hx hc
  have h0n : (0 : ℕ) < n := by omega
  have h1n : (1 : ℕ) < n := by omega
  have hclass0 : modeClass (⟨0, h0n⟩ : Fin n) = 0 := modeClass_of_val_zero rfl
  have hclass1 : modeClass (⟨1, h1n⟩ : Fin n) = 1 := modeClass_of_val_one rfl
  have h01 : (⟨0, h0n⟩ : Fin n) ≠ ⟨1, h1n⟩ := by simp [Fin.ext_iff]
  have hmem := hx.mem_Icc c
  have hmax₁ : ∀ i, masses (lpInput n x T ja jb u v m) T i ≤
      masses (lpInput n x T ja jb u v m) T ⟨0, h0n⟩ := by
    intro i
    simp only [masses, lpInput_mass hn hx hc, hclass0]
    exact m_modeClass_le_zero hc i
  have hmax₂ : ∀ i, i ≠ (⟨0, h0n⟩ : Fin n) →
      masses (lpInput n x T ja jb u v m) T i ≤
        masses (lpInput n x T ja jb u v m) T ⟨1, h1n⟩ := by
    intro i hi
    simp only [masses, lpInput_mass hn hx hc, hclass1]
    exact m_modeClass_le_one hc fun hval => hi (Fin.ext hval)
  rcases oneSwitch_reduction hA hmax₁ hmax₂ h01 hpq hmem.1 hmem.2 with h | ⟨hp0, h⟩
  · refine le_trans ?_ h
    refine E_le_D_oneSwitch hx hA jb h01 ?_ ?_ c
    · rw [masses, lpInput_mass hn hx hc, hclass1]
      exact hc.cutoff_b_upper
    · rw [lpInput_at_b hn hx hc, hclass0]
      exact hc.deficit_b
  · refine le_trans ?_ h
    refine E_le_D_oneSwitch hx hA ja hp0 ?_ ?_ c
    · rw [masses, lpInput_mass hn hx hc, hclass0]
      exact hc.cutoff_a_upper
    · rw [lpInput_at_a hn hx hc]
      have hval : (p : ℕ) ≠ 0 := fun hh => hp0 (Fin.ext hh)
      unfold modeClass
      rw [if_neg hval]
      split_ifs
      · exact hc.deficit_a
      · exact hf.deficit_a_bulk

/-- SC12, sufficiency for the two-large-modes family at a fixed ordered pair of modes and a
fixed grid switch time. No distinctness of the two modes is needed: a schedule omitting mode
`0` or mode `1` already errs by at least `m 1 ≥ E`, and the two remaining orders are
obstructed by the common constraints. -/
theorem twoLarge_le_D_oneSwitch (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) (p q : Fin n) (c : Fin (N + 1)) :
    E ≤ D (lpInput n x T ja jb u v m) (oneSwitch p q (x c) T) T := by
  have hc := hf.common
  have hA := isCumulative_lpInput hn hx hc
  have h0n : (0 : ℕ) < n := by omega
  have h1n : (1 : ℕ) < n := by omega
  have hclass0 : modeClass (⟨0, h0n⟩ : Fin n) = 0 := modeClass_of_val_zero rfl
  have hclass1 : modeClass (⟨1, h1n⟩ : Fin n) = 1 := modeClass_of_val_one rfl
  have h01 : (⟨0, h0n⟩ : Fin n) ≠ ⟨1, h1n⟩ := by simp [Fin.ext_iff]
  have hmem := hx.mem_Icc c
  have hE0 : E ≤ m (modeClass (⟨0, h0n⟩ : Fin n)) := by
    rw [hclass0]
    exact hf.E_le_m_one.trans hc.m_one_le_m_zero
  have hE1 : E ≤ m (modeClass (⟨1, h1n⟩ : Fin n)) := by
    rw [hclass1]
    exact hf.E_le_m_one
  by_cases hp0 : p = (⟨0, h0n⟩ : Fin n)
  · by_cases hq1 : q = (⟨1, h1n⟩ : Fin n)
    · subst hp0
      subst hq1
      refine E_le_D_oneSwitch hx hA jb h01 ?_ ?_ c
      · rw [masses, lpInput_mass hn hx hc, hclass1]
        exact hc.cutoff_b_upper
      · rw [lpInput_at_b hn hx hc, hclass0]
        exact hc.deficit_b
    · refine E_le_D_of_omitted hn hx hc (i := ⟨1, h1n⟩) ?_ (Ne.symm hq1) hE1 hmem
      rw [hp0]
      exact h01.symm
  · by_cases hp1 : p = (⟨1, h1n⟩ : Fin n)
    · by_cases hq0 : q = (⟨0, h0n⟩ : Fin n)
      · subst hp1
        subst hq0
        refine E_le_D_oneSwitch hx hA ja h01.symm ?_ ?_ c
        · rw [masses, lpInput_mass hn hx hc, hclass0]
          exact hc.cutoff_a_upper
        · rw [lpInput_at_a hn hx hc, hclass1]
          exact hc.deficit_a
      · exact E_le_D_of_omitted hn hx hc (i := ⟨0, h0n⟩) (Ne.symm hp0) (Ne.symm hq0) hE0 hmem
    · by_cases hq0 : q = (⟨0, h0n⟩ : Fin n)
      · refine E_le_D_of_omitted hn hx hc (i := ⟨1, h1n⟩) (Ne.symm hp1) ?_ hE1 hmem
        rw [hq0]
        exact h01.symm
      · exact E_le_D_of_omitted hn hx hc (i := ⟨0, h0n⟩) (Ne.symm hp0) (Ne.symm hq0) hE0 hmem

/-! ### SC12: the grid one-switch optimum of the interpolated input -/

/-- Reduction of the grid one-switch optimum to the one-switch schedules at grid nodes. -/
private theorem le_gridOPT_of_forall (hn : 3 ≤ n) (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ}
    (h : ∀ (p q : Fin n) (c : Fin (N + 1)), E ≤ D A (oneSwitch p q (x c) T) T) :
    E ≤ gridOPT x A T 1 := by
  have h0n : 0 < n := by omega
  obtain ⟨W₀, hW₀⟩ := exists_isGridSchedule h0n x (k := 1 + 1) (by omega)
  rw [gridOPT]
  refine le_csInf ⟨D A W₀ T, W₀, hW₀, rfl⟩ ?_
  rintro e ⟨W, hW, rfl⟩
  obtain ⟨p, q, c, rfl⟩ := exists_oneSwitch_of_isGridSchedule hx hW
  exact h p q c

/-- SC12, sufficiency for the all-initial-modes family: every grid one-switch schedule has
error at least `E` against the interpolated input. Constant schedules are covered, since they
are the one-switch schedules with equal modes. -/
theorem allInitial_le_gridOPT (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) :
    E ≤ gridOPT x (lpInput n x T ja jb u v m) T 1 := by
  refine le_gridOPT_of_forall hn hx fun p q c => ?_
  by_cases hpq : p = q
  · subst hpq
    have h0n : (0 : ℕ) < n := by omega
    have h1n : (1 : ℕ) < n := by omega
    obtain ⟨r, hr⟩ : ∃ r : Fin n, r ≠ p := by
      rcases eq_or_ne p ⟨0, h0n⟩ with h | h
      · exact ⟨⟨1, h1n⟩, by rw [h]; simp [Fin.ext_iff]⟩
      · exact ⟨⟨0, h0n⟩, fun hh => h hh.symm⟩
    have hmain := allInitial_le_D_oneSwitch hn hx hf hr (0 : Fin (N + 1))
    rw [hx.first] at hmain
    rw [oneSwitch_self_eq p r (x c) T]
    exact hmain
  · exact allInitial_le_D_oneSwitch hn hx hf hpq c

/-- SC12, sufficiency for the two-large-modes family. -/
theorem twoLarge_le_gridOPT (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) :
    E ≤ gridOPT x (lpInput n x T ja jb u v m) T 1 :=
  le_gridOPT_of_forall hn hx fun p q c => twoLarge_le_D_oneSwitch hn hx hf p q c

/-- Every grid-constant input contributes to the grid minimax value. -/
theorem gridOPT_le_gridF (hn : 0 < n) (hx : IsGrid x T) {A : Fin n → ℝ → ℝ}
    (hA : IsGridConstant x A) (s : ℕ) : gridOPT x A T s ≤ gridF x n s T := by
  have hbdd : BddAbove {w : ℝ | ∃ B : Fin n → ℝ → ℝ, IsGridConstant x B ∧
      w = gridOPT x B T s} := by
    refine ⟨T, ?_⟩
    rintro w ⟨B, ⟨r, hr, rfl⟩, rfl⟩
    exact gridOPT_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) s
  exact le_csSup hbdd ⟨A, hA, rfl⟩

/-- SC12 for the all-initial-modes family, in the form used downstream: a feasible point is a
lower-bound witness for the grid one-switch minimax value. -/
theorem allInitial_le_gridF (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) : E ≤ gridF x n 1 T :=
  (allInitial_le_gridOPT hn hx hf).trans
    (gridOPT_le_gridF (by omega) hx (isGridConstant_lpInput hn hx hf.common) 1)

/-- SC12 for the two-large-modes family, in the form used downstream. -/
theorem twoLarge_le_gridF (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) : E ≤ gridF x n 1 T :=
  (twoLarge_le_gridOPT hn hx hf).trans
    (gridOPT_le_gridF (by omega) hx (isGridConstant_lpInput hn hx hf.common) 1)

/-- SC12, packaged for the all-initial-modes family: a feasible point yields a grid-constant
relaxed control whose grid one-switch optimum is at least `E`. -/
theorem exists_gridConstant_of_allInitialFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) :
    ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ IsCumulative A T ∧ E ≤ gridOPT x A T 1 :=
  ⟨lpInput n x T ja jb u v m, isGridConstant_lpInput hn hx hf.common,
    isCumulative_lpInput hn hx hf.common, allInitial_le_gridOPT hn hx hf⟩

/-- SC12, packaged for the two-large-modes family. -/
theorem exists_gridConstant_of_twoLargeFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) :
    ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧ IsCumulative A T ∧ E ≤ gridOPT x A T 1 :=
  ⟨lpInput n x T ja jb u v m, isGridConstant_lpInput hn hx hf.common,
    isCumulative_lpInput hn hx hf.common, twoLarge_le_gridOPT hn hx hf⟩

/-! ## SC13: the floor `T / 3`

Three modes of terminal mass `T / 3` each, the remaining modes of mass zero. Any one-switch
schedule uses at most two modes, hence omits one of the three, and its error is at least the
omitted terminal mass `T / 3`. -/

/-- The rate matrix of SC13: the first three modes run at rate `1/3` on every cell. -/
noncomputable def thirdsRates (n : ℕ) {N : ℕ} : Fin N → Fin n → ℝ :=
  fun _ i => if (i : ℕ) < 3 then 1 / 3 else 0

/-- The input of SC13. -/
noncomputable def thirdsInput (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) : Fin n → ℝ → ℝ :=
  gridCumulative x (thirdsRates n)

/-- The rates of SC13 form a rate matrix. -/
theorem isRateMatrix_thirdsRates (hn : 3 ≤ n) : IsRateMatrix (thirdsRates n (N := N)) where
  nonneg j i := by
    simp only [thirdsRates]
    split_ifs <;> norm_num
  conservation j := by
    simp only [thirdsRates]
    rw [sum_ite_val_lt_three hn]
    norm_num

/-- The input of SC13 is grid constant. -/
theorem isGridConstant_thirdsInput (hn : 3 ≤ n) (x : Fin (N + 1) → ℝ) :
    IsGridConstant x (thirdsInput n x) :=
  ⟨_, isRateMatrix_thirdsRates hn, rfl⟩

/-- Each of the first three modes of the input of SC13 has terminal mass `T / 3`. -/
theorem thirdsInput_mass (hx : IsGrid x T) {i : Fin n} (hi : (i : ℕ) < 3) :
    thirdsInput n x i T = T / 3 := by
  have key : ∀ j : Fin N, thirdsRates n j i * (min T (x j.succ) - min T (x j.castSucc)) =
      if 0 ≤ (j : ℕ) ∧ (j : ℕ) < N then
        (1 / 3 : ℝ) * (min T (x j.succ) - min T (x j.castSucc)) else 0 := by
    intro j
    rw [if_pos ⟨Nat.zero_le _, j.isLt⟩]
    simp only [thirdsRates]
    rw [if_pos hi]
  simp only [thirdsInput, gridCumulative]
  rw [Finset.sum_congr rfl fun j _ => key j,
    sum_cell_phase (k₁ := 0) (k₂ := N) x T _ 0 (Fin.last N) (Nat.zero_le _) (by simp) (by simp),
    hx.first, hx.last, min_self, min_eq_right hx.horizon_nonneg]
  ring

/-- SC13: every grid one-switch schedule errs by at least `T / 3` against the input of SC13. -/
theorem third_le_gridOPT (hn : 3 ≤ n) (hx : IsGrid x T) :
    T / 3 ≤ gridOPT x (thirdsInput n x) T 1 := by
  have h0n : 0 < n := by omega
  obtain ⟨W₀, hW₀⟩ := exists_isGridSchedule h0n x (k := 1 + 1) (by omega)
  have hA : IsCumulative (thirdsInput n x) T :=
    gridCumulative_isCumulative hx.orderedTimes (isRateMatrix_thirdsRates hn)
  rw [gridOPT]
  refine le_csInf ⟨D (thirdsInput n x) W₀ T, W₀, hW₀, rfl⟩ ?_
  rintro e ⟨W, hW, rfl⟩
  obtain ⟨p, q, c, rfl⟩ := exists_oneSwitch_of_isGridSchedule hx hW
  obtain ⟨i, hi3, hip, hiq⟩ : ∃ i : Fin n, (i : ℕ) < 3 ∧ i ≠ p ∧ i ≠ q := by
    have h0 : (0 : ℕ) < n := by omega
    have h1 : (1 : ℕ) < n := by omega
    have h2 : (2 : ℕ) < n := by omega
    by_cases e0 : (p : ℕ) = 0 ∨ (q : ℕ) = 0
    · by_cases e1 : (p : ℕ) = 1 ∨ (q : ℕ) = 1
      · exact ⟨⟨2, h2⟩, by norm_num, by simp only [ne_eq, Fin.ext_iff]; omega,
          by simp only [ne_eq, Fin.ext_iff]; omega⟩
      · exact ⟨⟨1, h1⟩, by norm_num, by simp only [ne_eq, Fin.ext_iff]; omega,
          by simp only [ne_eq, Fin.ext_iff]; omega⟩
    · exact ⟨⟨0, h0⟩, by norm_num, by simp only [ne_eq, Fin.ext_iff]; omega,
        by simp only [ne_eq, Fin.ext_iff]; omega⟩
  have hmem := hx.mem_Icc c
  have hW' := isCumulative_oneSwitch hmem.1 hmem.2 p q
  have hT : T ∈ Icc (0 : ℝ) T := ⟨hx.horizon_nonneg, le_rfl⟩
  have h := le_D hA hW' i hT
  rwa [oneSwitch_of_ne hip hiq, sub_zero, abs_of_nonneg (hA.nonneg i hT),
    thirdsInput_mass hx hi3] at h

/-- SC13: on every grid the one-switch grid minimax value is at least `T / 3`. -/
theorem third_le_gridF (hn : 3 ≤ n) (hx : IsGrid x T) : T / 3 ≤ gridF x n 1 T :=
  (third_le_gridOPT hn hx).trans
    (gridOPT_le_gridF (by omega) hx (isGridConstant_thirdsInput hn x) 1)

end GridSwitching
