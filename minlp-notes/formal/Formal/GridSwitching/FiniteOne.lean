import Formal.GridSwitching.Coverage
import Formal.GridSwitching.Symmetrize
import Formal.GridSwitching.TwoLarge

/-!
# SC20: `thm:finite-one`, the arbitrary-grid one-switch minimax formula

This module assembles the headline theorem `thm:finite-one` of
`paper-switching-control/sections/08-finite-grid-one-switch.tex`, obligation SC20 of
`topics/17-grid-switching/CLAIMS.md`, from the parts proved in the other modules of
`Formal.GridSwitching`. Nothing new about the model is proved here: every step is one of
`gridH_le_gridF`, `le_gridF_of_admissible`, `exists_feasible_gridF`,
`TwoLargeFeasible.le_gridH_of_pos` and `exists_admissible_of_allInitialFeasible`.

## Admissibility: two conventions

`Formal.GridSwitching.Elimination` defines `Admissible nu T A B` to be **only** the first
inequality of `eq:grid-admissible`, namely `(nu-2)(T-A) ≤ (nu-1)B`. The source calls `(a,b)`
admissible when *both* inequalities of `eq:grid-admissible` hold, the second being
`L_ab ≤ U_ab`. The two conventions therefore differ, and the formula `eq:grid-minimax-formula`
needs the source's one: without `L_ab ≤ U_ab` the pair carries no feasible point and `U_ab`
may exceed the minimax value.

`AdmissiblePair` below is the source's notion, stated explicitly as the conjunction

* `(ja : ℕ) ≤ (jb : ℕ)`, the index range `1 ≤ a ≤ b ≤ N` of the source;
* `Admissible (n : ℝ) T A B`, the first inequality of `eq:grid-admissible`;
* `gridL ≤ gridU`, the second inequality of `eq:grid-admissible`.

## The formula, and the empty inner maximum

`eq:grid-minimax-formula` reads `F = max {H, max over admissible (a,b) of U_ab}` "where an
empty inner maximum is ignored". Rather than a `Finset.sup'`, which would need a nonemptiness
side condition and would silently make the convention an accident of the definition, the
formula is stated as

`IsGreatest (gridCandidateSet n x T) (gridF x n 1 T)`

for the candidate *set*

`gridCandidateSet n x T = {gridH ...} ∪ {gridU ja jb | (ja, jb) admissible}`.

`IsGreatest S a` is `a ∈ S ∧ ∀ b ∈ S, b ≤ a`, so this says simultaneously that the value is
attained by one of the candidates and dominates all of them. The convention "an empty inner
maximum is ignored" is then honest rather than accidental: `gridH ...` is unconditionally a
member of the candidate set (`gridH_mem_gridCandidateSet`), so when no pair is admissible the
set is the singleton `{gridH ...}` and the statement is `gridF = gridH ...`; no maximum over
an empty index set is ever formed.

## Contents

* `gridL`, `gridU`, `AdmissiblePair`, `gridCandidateSet`.
* `le_gridF_of_mem_gridCandidateSet` (the `≥` half of the formula) and
  `gridF_mem_gridCandidateSet` (the `≤` half, with attainment), packaged as
  **`isGreatest_gridCandidateSet`**, which is SC20's formula.
* `third_le_of_mem_gridCandidateSet` and `third_le_gridF_of_formula`: the floor `T/3` is
  consistent with the formula, every candidate being at least `T/3`.
* `gridCandidateFinset`, `card_gridCandidateFinset_le`,
  `gridCandidateSet_subset_gridCandidateFinset` and `gridF_mem_gridCandidateFinset`: the
  structural form of the complexity claim.
* `lpInput_phase_one`, `lpInput_phase_two`, `lpInput_phase_three`,
  `lpInput_congr_modeClass`, `TwoTypesOneLarge`, `TwoTypesTwoLarge` and
  **`exists_compressed_maximizer`**: the compressed maximizer, whose statement carries both
  halves of the source's sentence, the three phases and the two component types.
* `isGreatest_gridOPT_cumulative`: the SC05 sub-clause, that the value of the formula is the
  maximum of the grid one-switch instance optimum over *all* cumulative inputs, not only the
  grid-constant ones.
* `isGreatest_gridCandidateSet_one_cell`, `lpInput_eq_of_degenerate_phase_two`,
  `lpInput_eq_of_degenerate_phase_three`, `le_D_constSchedule_of_allInitialFeasible` and
  `le_D_constSchedule_of_twoLargeFeasible`: `N = 1`, zero-length phases and constant integer
  controls are permitted.

## Complexity: what is and is not claimed

`CLAIMS.md` excludes machine-level bit-complexity models, so **no arithmetic-operation count
and no bit-cost model is claimed here**. What is claimed is the structural content behind the
source's `O(N^2)`: the candidate set is contained in an explicit finite set of at most
`N^2 + 1` real numbers, indexed by `Fin N × Fin N` together with the single extra candidate
`gridH`, each an explicit expression in the grid nodes and `n`
(`gridCandidateSet_subset_gridCandidateFinset`, `card_gridCandidateFinset_le`), and the value
is one of them (`gridF_mem_gridCandidateFinset`).

## Hypotheses

`3 ≤ n` and `IsGrid x T`, as everywhere in this package, and `0 < T`. The horizon hypothesis
is not removable: `gridH_le_gridF` and `exists_feasible_gridF` both need it, since a grid on
`T = 0` has `N = 0` cells and no witness at all exists. No other hypothesis is added; in
particular `N = 1`, `ja = jb`, `jb.succ = Fin.last N` and `n = 3` are all permitted.
-/

namespace GridSwitching

variable {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} {ja jb : Fin N} {u v m : Fin 3 → ℝ} {E : ℝ}

/-! ## The candidates of `eq:grid-minimax-formula` -/

/-- The lower endpoint `L_ab` of `eq:grid-L` at a pair of grid cells. -/
noncomputable def gridL (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) : ℝ :=
  L (n : ℝ) T (x ja.succ) (x jb.succ)

/-- The upper endpoint `U_ab` of `eq:grid-U` at a pair of grid cells. -/
noncomputable def gridU (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) : ℝ :=
  U (n : ℝ) T (x ja.succ) (x jb.succ) (x ja.castSucc) (x jb.castSucc)

/-- Admissibility of a pair of cells in the sense of the source's `eq:grid-admissible`: the
index range `a ≤ b`, the inequality `(n-2)(T-A) ≤ (n-1)B` (which is `Admissible` of
`Formal.GridSwitching.Elimination`) **and** the comparison `L_ab ≤ U_ab`, which `Admissible`
does not include. Both inequalities are needed: the second is exactly what makes the pair
carry a feasible point of the all-initial-modes family. -/
def AdmissiblePair (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) : Prop :=
  (ja : ℕ) ≤ (jb : ℕ) ∧ Admissible (n : ℝ) T (x ja.succ) (x jb.succ) ∧
    gridL n x T ja jb ≤ gridU n x T ja jb

/-- The candidate set of `eq:grid-minimax-formula`: the quantity `gridH` at the cutoff index,
together with `U_ab` for every admissible pair of cells. The first candidate is present
unconditionally, which is how "an empty inner maximum is ignored" is realized. -/
def gridCandidateSet (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) : Set ℝ :=
  {w : ℝ | w = gridH x T (gridCutoff x T) ∨
    ∃ ja jb : Fin N, AdmissiblePair n x T ja jb ∧ w = gridU n x T ja jb}

/-- The quantity `gridH` is always a candidate; no admissible pair is needed. -/
theorem gridH_mem_gridCandidateSet (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) :
    gridH x T (gridCutoff x T) ∈ gridCandidateSet n x T :=
  Or.inl rfl

/-- The upper endpoint of an admissible pair is a candidate. -/
theorem gridU_mem_gridCandidateSet (h : AdmissiblePair n x T ja jb) :
    gridU n x T ja jb ∈ gridCandidateSet n x T :=
  Or.inr ⟨ja, jb, h, rfl⟩

/-- The candidate set is never empty. -/
theorem gridCandidateSet_nonempty (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) :
    (gridCandidateSet n x T).Nonempty :=
  ⟨_, gridH_mem_gridCandidateSet n x T⟩

/-! ## The `≥` half: every candidate is a lower bound for the minimax value -/

/-- The `≥` half of `eq:grid-minimax-formula`. The quantity `gridH` is a lower bound by the
witness `eq:grid-H-witness` (SC17), and `U_ab` is a lower bound for every admissible pair by
the symmetrized witness (SC18--SC19); the latter uses `L_ab ≤ U_ab`, that is, exactly the
second inequality of the source's `eq:grid-admissible`. -/
theorem le_gridF_of_mem_gridCandidateSet (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) {w : ℝ}
    (hw : w ∈ gridCandidateSet n x T) : w ≤ gridF x n 1 T := by
  rcases hw with rfl | ⟨ja, jb, ⟨hab, hadm, hLU⟩, rfl⟩
  · exact gridH_le_gridF hn hx hT
  · exact le_gridF_of_admissible hn hx hab hadm hLU le_rfl

/-! ## The `≤` half: the minimax value is itself a candidate -/

/-- The `≤` half of `eq:grid-minimax-formula`, in the sharp form "the value is attained by one
of the candidates". `exists_feasible_gridF` (SC14--SC15) produces a feasible point of one of
the two families at the objective `gridF` itself. In the two-large-modes case
`TwoLargeFeasible.le_gridH_of_pos` (SC16) bounds it by `gridH`, which is also a lower bound,
so the value *is* `gridH`. In the all-initial-modes case
`exists_admissible_of_allInitialFeasible` (SC18--SC19) produces an admissible pair with
`L_ab ≤ gridF ≤ U_ab`; since `U_ab` is also a lower bound, the value *is* `U_ab`. -/
theorem gridF_mem_gridCandidateSet (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    gridF x n 1 T ∈ gridCandidateSet n x T := by
  obtain ⟨ja, jb, u, v, m, -, hf⟩ := exists_feasible_gridF hn hx hT
  rcases hf with hf | hf
  · obtain ⟨jb', hab', hadm, hL, hU⟩ := exists_admissible_of_allInitialFeasible hn hx hf
    have hpair : AdmissiblePair n x T ja jb' := ⟨hab', hadm, hL.trans hU⟩
    exact Or.inr ⟨ja, jb', hpair,
      le_antisymm hU (le_gridF_of_admissible hn hx hab' hadm (hL.trans hU) le_rfl)⟩
  · exact Or.inl (le_antisymm (hf.le_gridH_of_pos hn hx hT) (gridH_le_gridF hn hx hT))

/-! ## SC20: the formula -/

/-- **SC20, `thm:finite-one`, `eq:grid-minimax-formula`.** For `n ≥ 3`, a positive horizon and
every grid, the one-switch grid minimax value is the greatest element of the candidate set
consisting of `gridH` at the cutoff index together with `U_ab` over the admissible pairs of
cells, admissibility being the source's `eq:grid-admissible` in full (see `AdmissiblePair`).

`IsGreatest` states both halves at once: the value belongs to the candidate set, so it is
*attained* by one of the candidates, and it dominates every candidate. The convention that an
empty inner maximum is ignored is built in: `gridH` is a candidate whether or not any pair is
admissible, so when none is, the statement reads `gridF x n 1 T = gridH x T (gridCutoff x T)`
(`isGreatest_gridCandidateSet_of_forall_not_admissible`). -/
theorem isGreatest_gridCandidateSet (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    IsGreatest (gridCandidateSet n x T) (gridF x n 1 T) :=
  ⟨gridF_mem_gridCandidateSet hn hx hT,
    fun _ hw => le_gridF_of_mem_gridCandidateSet hn hx hT hw⟩

/-- The degenerate case of the formula: if no pair of cells is admissible, the inner maximum
is empty and the value is `gridH` alone. -/
theorem gridF_eq_gridH_of_forall_not_admissible (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T)
    (h : ∀ ja jb : Fin N, ¬ AdmissiblePair n x T ja jb) :
    gridF x n 1 T = gridH x T (gridCutoff x T) := by
  rcases gridF_mem_gridCandidateSet hn hx hT with heq | ⟨ja, jb, hpair, -⟩
  · exact heq
  · exact absurd hpair (h ja jb)

/-- The degenerate case of the formula, in `IsGreatest` form: if no pair is admissible the
candidate set is the singleton `{gridH ...}`. -/
theorem isGreatest_gridCandidateSet_of_forall_not_admissible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hT : 0 < T) (h : ∀ ja jb : Fin N, ¬ AdmissiblePair n x T ja jb) :
    IsGreatest {gridH x T (gridCutoff x T)} (gridF x n 1 T) := by
  refine ⟨gridF_eq_gridH_of_forall_not_admissible hn hx hT h, ?_⟩
  rintro w rfl
  exact le_gridF_of_mem_gridCandidateSet hn hx hT (gridH_mem_gridCandidateSet n x T)

/-! ## The floor `T / 3` is consistent with the formula -/

/-- Every candidate is at least the floor `T / 3`: `gridH` by `third_le_gridH_gridCutoff`, and
`U_ab` because the admissible pair satisfies `T / 3 ≤ L_ab ≤ U_ab`, the first term of `L_ab`
of `eq:grid-L` being `T / 3`. -/
theorem third_le_of_mem_gridCandidateSet (hx : IsGrid x T) (hT : 0 < T) {w : ℝ}
    (hw : w ∈ gridCandidateSet n x T) : T / 3 ≤ w := by
  rcases hw with rfl | ⟨ja, jb, ⟨-, -, hLU⟩, rfl⟩
  · exact third_le_gridH_gridCutoff hx hT
  · exact le_trans (le_max_left _ _) hLU

/-- The floor `T / 3` of SC13 is consistent with the formula: it is inherited from the
candidates. This reproves `third_le_gridF` on a positive horizon through
`eq:grid-minimax-formula` rather than through the explicit thirds input. -/
theorem third_le_gridF_of_formula (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    T / 3 ≤ gridF x n 1 T :=
  third_le_of_mem_gridCandidateSet hx hT (gridF_mem_gridCandidateSet hn hx hT)

/-! ## The structural form of the complexity claim

No arithmetic-operation count and no bit-cost model is claimed; see the module docstring. The
content below is that the candidates form an explicit list of at most `N^2 + 1` numbers,
indexed by `Fin N × Fin N` plus the single candidate `gridH`. -/

/-- The explicit candidate list: `gridH` at the cutoff index together with `U_ab` for *all*
`N^2` pairs of cells, admissible or not. It is a superset of the candidate set, which is what
makes the cardinality bound a statement about the number of expressions to evaluate. -/
noncomputable def gridCandidateFinset (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) :
    Finset ℝ :=
  insert (gridH x T (gridCutoff x T))
    ((Finset.univ : Finset (Fin N × Fin N)).image fun p => gridU n x T p.1 p.2)

/-- The candidate list has at most `N^2 + 1` entries: one `gridH` and one `U_ab` per pair of
cells. This is the structural content of the source's `O(N^2)` candidate count. -/
theorem card_gridCandidateFinset_le (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) :
    (gridCandidateFinset n x T).card ≤ N ^ 2 + 1 := by
  refine (Finset.card_insert_le _ _).trans ?_
  have h := Finset.card_image_le (s := (Finset.univ : Finset (Fin N × Fin N)))
    (f := fun p => gridU n x T p.1 p.2)
  simp only [Finset.card_univ, Fintype.card_prod, Fintype.card_fin] at h
  rw [pow_two]
  omega

/-- Every candidate occurs in the explicit list. -/
theorem gridCandidateSet_subset_gridCandidateFinset (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) :
    gridCandidateSet n x T ⊆ ↑(gridCandidateFinset n x T) := by
  rintro w (rfl | ⟨ja, jb, -, rfl⟩)
  · exact Finset.mem_coe.2 (Finset.mem_insert_self _ _)
  · exact Finset.mem_coe.2
      (Finset.mem_insert_of_mem (Finset.mem_image.2 ⟨(ja, jb), Finset.mem_univ _, rfl⟩))

/-- The minimax value is one of the at most `N^2 + 1` listed numbers. -/
theorem gridF_mem_gridCandidateFinset (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    gridF x n 1 T ∈ gridCandidateFinset n x T :=
  gridCandidateSet_subset_gridCandidateFinset n x T (gridF_mem_gridCandidateSet hn hx hT)

/-! ## The three phases of the interpolated input

The relaxed inputs of `lpInput` are built from exactly the three phases `[0, A]`, `[A, B]`,
`[B, T]` of the source: on each of them the cumulative allocation of every mode is affine in
`t`, with a rate depending only on the phase and the mode class. None of the three statements
assumes that a phase is nondegenerate. -/

/-- The first phase `[0, A]`: the allocation grows at the constant rate `u / A`. -/
theorem lpInput_phase_one (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) {t : ℝ} (ht0 : 0 ≤ t) (htA : t ≤ x ja.succ) :
    lpInput n x T ja jb u v m i t = u (modeClass i) / x ja.succ * t := by
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  rw [lpInput_apply hn hx hc, min_eq_left htA, min_eq_right ht0,
    min_eq_left (htA.trans hAB), min_eq_left (htA.trans (hAB.trans hBT))]
  ring

/-- The second phase `[A, B]`: the allocation grows at the constant rate `(v - u) / (B - A)`
from the state `u`. On a zero-length phase (`A = B`) both sides are `u = v`. -/
theorem lpInput_phase_two (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) {t : ℝ} (htA : x ja.succ ≤ t) (htB : t ≤ x jb.succ) :
    lpInput n x T ja jb u v m i t =
      u (modeClass i) + (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ) *
        (t - x ja.succ) := by
  have hA0 : 0 < x ja.succ := hx.zero_lt_succ ja
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  have hcancel : u (modeClass i) / x ja.succ * x ja.succ = u (modeClass i) :=
    div_mul_cancel₀ _ hA0.ne'
  rw [lpInput_apply hn hx hc, min_eq_right htA, min_eq_right (hA0.le.trans htA),
    min_eq_left htB, min_eq_left (htB.trans hBT), sub_zero, hcancel]
  ring

/-- The third phase `[B, T]`: the allocation grows at the constant rate `(m - v) / (T - B)`
from the state `v`. On a zero-length phase (`B = T`) both sides are `v = m`. -/
theorem lpInput_phase_three (hn : 3 ≤ n) (hx : IsGrid x T) (hc : LPCommon n x T ja jb u v m E)
    (i : Fin n) {t : ℝ} (htB : x jb.succ ≤ t) (htT : t ≤ T) :
    lpInput n x T ja jb u v m i t =
      v (modeClass i) + (m (modeClass i) - v (modeClass i)) / (T - x jb.succ) *
        (t - x jb.succ) := by
  have hA0 : 0 < x ja.succ := hx.zero_lt_succ ja
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hcancel : u (modeClass i) / x ja.succ * x ja.succ = u (modeClass i) :=
    div_mul_cancel₀ _ hA0.ne'
  have hmid : (v (modeClass i) - u (modeClass i)) / (x jb.succ - x ja.succ) *
      (x jb.succ - x ja.succ) = v (modeClass i) - u (modeClass i) := by
    rcases eq_or_lt_of_le hAB with heq | hlt
    · have h : u (modeClass i) = v (modeClass i) :=
        eq_of_lpWeighted_eq hn hc.u_le_v (by rw [hc.weighted_u, hc.weighted_v, heq]) _
      rw [← heq, sub_self, mul_zero, h, sub_self]
    · exact div_mul_cancel₀ _ (sub_pos.mpr hlt).ne'
  rw [lpInput_apply hn hx hc, min_eq_right htB, min_eq_right (hAB.trans htB),
    min_eq_right (hA0.le.trans (hAB.trans htB)), min_eq_left htT, sub_zero, hcancel, hmid]
  ring

/-- Zero-length second phase: if `A = B` the two endpoint states coincide, so the phase can be
dropped. This is the source's "equal times force equal states". -/
theorem lpInput_eq_of_degenerate_phase_two (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E)
    (h : x ja.succ = x jb.succ) (j : Fin 3) : u j = v j :=
  eq_of_lpWeighted_eq hn hc.u_le_v (by rw [hc.weighted_u, hc.weighted_v, h]) j

/-- Zero-length third phase: if `B = T` the state at `B` is already the terminal mass. -/
theorem lpInput_eq_of_degenerate_phase_three (hn : 3 ≤ n) (hc : LPCommon n x T ja jb u v m E)
    (h : x jb.succ = T) (j : Fin 3) : v j = m j :=
  eq_of_lpWeighted_eq hn hc.v_le_m (by rw [hc.weighted_v, hc.weighted_m, h]) j

/-! ## At most three, and in fact two, component types -/

/-- The interpolated input has at most three distinct component functions: a mode's component
depends only on its class. -/
theorem lpInput_congr_modeClass (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) {i i' : Fin n} (h : modeClass i = modeClass i') :
    lpInput n x T ja jb u v m i = lpInput n x T ja jb u v m i' := by
  funext t
  rw [lpInput_apply hn hx hc, lpInput_apply hn hx hc, h]

/-- An input of the first compressed shape of `thm:finite-one`: one distinguished mode and
`n - 1` identical modes. -/
def TwoTypesOneLarge {n : ℕ} (A : Fin n → ℝ → ℝ) : Prop :=
  ∀ i i' : Fin n, (i : ℕ) ≠ 0 → (i' : ℕ) ≠ 0 → A i = A i'

/-- An input of the second compressed shape of `thm:finite-one`: two identical modes and
`n - 2` identical modes. -/
def TwoTypesTwoLarge {n : ℕ} (A : Fin n → ℝ → ℝ) : Prop :=
  (∀ i i' : Fin n, (i : ℕ) < 2 → (i' : ℕ) < 2 → A i = A i') ∧
    (∀ i i' : Fin n, 2 ≤ (i : ℕ) → 2 ≤ (i' : ℕ) → A i = A i')

/-- A state vector with equal bulk entries is constant on the modes other than `0`. -/
private theorem state_eq_one_of_ne_zero {f : Fin 3 → ℝ} (h : f 1 = f 2) {i : Fin n}
    (hi : (i : ℕ) ≠ 0) : f (modeClass i) = f 1 := by
  rcases eq_or_ne (i : ℕ) 1 with h1 | h1
  · rw [modeClass_of_val_one h1]
  · rw [modeClass_of_two_le (by omega)]
    exact h.symm

/-- A state vector with equal distinguished entries is constant on the modes `0` and `1`. -/
private theorem state_eq_zero_of_lt_two {f : Fin 3 → ℝ} (h : f 0 = f 1) {i : Fin n}
    (hi : (i : ℕ) < 2) : f (modeClass i) = f 0 := by
  rcases (by omega : (i : ℕ) = 0 ∨ (i : ℕ) = 1) with h0 | h1
  · rw [modeClass_of_val_zero h0]
  · rw [modeClass_of_val_one h1]
    exact h.symm

/-- Every state vector is constant on the bulk modes. -/
private theorem state_eq_two_of_two_le {f : Fin 3 → ℝ} {i : Fin n} (hi : 2 ≤ (i : ℕ)) :
    f (modeClass i) = f 2 := by
  rw [modeClass_of_two_le hi]

/-- If the bulk entries of the three state vectors agree with the entries of mode `1`, the
interpolated input has the first compressed shape. -/
theorem lpInput_twoTypesOneLarge (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) (hu : u 1 = u 2) (hv : v 1 = v 2) (hm : m 1 = m 2) :
    TwoTypesOneLarge (lpInput n x T ja jb u v m) := by
  intro i i' hi hi'
  funext t
  rw [lpInput_apply hn hx hc, lpInput_apply hn hx hc, state_eq_one_of_ne_zero hu hi,
    state_eq_one_of_ne_zero hv hi, state_eq_one_of_ne_zero hm hi,
    state_eq_one_of_ne_zero hu hi', state_eq_one_of_ne_zero hv hi',
    state_eq_one_of_ne_zero hm hi']

/-- If the two distinguished entries of the three state vectors agree, the interpolated input
has the second compressed shape. -/
theorem lpInput_twoTypesTwoLarge (hn : 3 ≤ n) (hx : IsGrid x T)
    (hc : LPCommon n x T ja jb u v m E) (hu : u 0 = u 1) (hv : v 0 = v 1) (hm : m 0 = m 1) :
    TwoTypesTwoLarge (lpInput n x T ja jb u v m) := by
  constructor
  · intro i i' hi hi'
    funext t
    rw [lpInput_apply hn hx hc, lpInput_apply hn hx hc, state_eq_zero_of_lt_two hu hi,
      state_eq_zero_of_lt_two hv hi, state_eq_zero_of_lt_two hm hi,
      state_eq_zero_of_lt_two hu hi', state_eq_zero_of_lt_two hv hi',
      state_eq_zero_of_lt_two hm hi']
  · intro i i' hi hi'
    funext t
    rw [lpInput_apply hn hx hc, lpInput_apply hn hx hc, state_eq_two_of_two_le (f := u) hi,
      state_eq_two_of_two_le (f := v) hi, state_eq_two_of_two_le (f := m) hi,
      state_eq_two_of_two_le (f := u) hi', state_eq_two_of_two_le (f := v) hi',
      state_eq_two_of_two_le (f := m) hi']

/-! ## The compressed maximizer -/

/-- The symmetrized feasible point of an admissible pair, with its shape exposed. This is
`exists_allInitialFeasible_of_admissible` of `Formal.GridSwitching.Symmetrize` with the
witness kept visible: the three state vectors are `symmState`, that is, one distinguished mode
and `n - 1` identical modes. -/
theorem exists_symmState_allInitialFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hab : (ja : ℕ) ≤ (jb : ℕ)) (hadm : Admissible (n : ℝ) T (x ja.succ) (x jb.succ))
    (hL : gridL n x T ja jb ≤ E) (hU : E ≤ gridU n x T ja jb) :
    ∃ X Y M : ℝ, AllInitialFeasible n x T ja jb (symmState n (x ja.succ) X)
      (symmState n (x jb.succ) Y) (symmState n T M) E := by
  have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hP0 : (0 : ℝ) ≤ x ja.castSucc := by
    have h := hx.strictMono.monotone (Fin.zero_le ja.castSucc)
    rwa [hx.first] at h
  have hPA : x ja.castSucc ≤ x ja.succ :=
    hx.strictMono.monotone (Fin.castSucc_lt_succ (i := ja)).le
  have hQB : x jb.castSucc ≤ x jb.succ :=
    hx.strictMono.monotone (Fin.castSucc_lt_succ (i := jb)).le
  have hAB : x ja.succ ≤ x jb.succ := by
    refine hx.strictMono.monotone ?_
    rw [Fin.le_def]
    simp only [Fin.val_succ]
    omega
  have hBT : x jb.succ ≤ T := by
    have h := hx.strictMono.monotone (Fin.le_last jb.succ)
    rwa [hx.last] at h
  obtain ⟨hMne, h3E, hEA, hE2⟩ := (elimination_iff h3n hPA hQB T E).2 ⟨hadm, hL, hU⟩
  obtain ⟨X, Y, M, hs⟩ :=
    (exists_state_iff h3n hP0 hPA hAB hBT (x jb.castSucc) E).2 ⟨hEA, hE2, hMne⟩
  exact ⟨X, Y, M, allInitialFeasible_symmState hn h3E hs⟩

/-- **SC20, the compressed maximizer.** On a positive horizon there are cells `ja`, `jb` and
state vectors `u`, `v`, `m` feasible in one of the two families of `eq:grid-LP` at the
objective `gridF x n 1 T` such that the interpolated input `lpInput n x T ja jb u v m` is a
grid-constant cumulative input attaining the grid one-switch minimax value, which is affine on
each of the three phases `[0, A]`, `[A, B]`, `[B, T]` and has two component types: either one
distinguished mode and `n - 1` identical modes (the symmetrized all-initial-modes case) or two
identical modes and `n - 2` identical modes (the two-large-modes case).

This is exactly the source's claim "the relaxed maximizer can be chosen with at most three
time phases and two types of component", and both conjuncts are in the statement: the three
displayed phase identities (the instances of `lpInput_phase_one`, `lpInput_phase_two` and
`lpInput_phase_three` at the produced data) say that on each phase every component grows at a
constant rate, so the underlying relaxed control is constant on three phases, and the final
disjunction gives the two component types. `lpInput_congr_modeClass` gives the a priori bound
of three component types for every `lpInput`; the disjunction improves it to two. Nothing
stronger is claimed: in particular the maximizer is not claimed to be unique, three phases are
not claimed to be necessary, and no claim is made about maximizers other than the one produced
here. -/
theorem exists_compressed_maximizer (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    ∃ (ja jb : Fin N) (u v m : Fin 3 → ℝ),
      IsGridConstant x (lpInput n x T ja jb u v m) ∧
      IsCumulative (lpInput n x T ja jb u v m) T ∧
      gridOPT x (lpInput n x T ja jb u v m) T 1 = gridF x n 1 T ∧
      (∀ (i : Fin n) (t : ℝ), 0 ≤ t → t ≤ x ja.succ →
          lpInput n x T ja jb u v m i t = u (modeClass i) / x ja.succ * t) ∧
      (∀ (i : Fin n) (t : ℝ), x ja.succ ≤ t → t ≤ x jb.succ →
          lpInput n x T ja jb u v m i t =
            u (modeClass i) + (v (modeClass i) - u (modeClass i)) /
              (x jb.succ - x ja.succ) * (t - x ja.succ)) ∧
      (∀ (i : Fin n) (t : ℝ), x jb.succ ≤ t → t ≤ T →
          lpInput n x T ja jb u v m i t =
            v (modeClass i) + (m (modeClass i) - v (modeClass i)) /
              (T - x jb.succ) * (t - x jb.succ)) ∧
      ((AllInitialFeasible n x T ja jb u v m (gridF x n 1 T) ∧
          TwoTypesOneLarge (lpInput n x T ja jb u v m)) ∨
        (TwoLargeFeasible n x T ja jb u v m (gridF x n 1 T) ∧
          TwoTypesTwoLarge (lpInput n x T ja jb u v m))) := by
  rcases gridF_mem_gridCandidateSet hn hx hT with heq | ⟨ja, jb, ⟨hab, hadm, hLU⟩, heq⟩
  · -- the two-large-modes case: the value is `gridH`, attained by `eq:grid-H-witness`
    obtain ⟨jc, hjc⟩ := exists_cell_succ_eq_gridCutoff hx hT
    have hf := twoLargeFeasible_gridH hn hx hjc
    rw [hjc, ← heq] at hf
    have hc := hf.common
    refine ⟨jc, jc, _, _, _, isGridConstant_lpInput hn hx hc, isCumulative_lpInput hn hx hc,
      le_antisymm (gridOPT_le_gridF (by omega) hx (isGridConstant_lpInput hn hx hc) 1)
        (twoLarge_le_gridOPT hn hx hf),
      fun i t h₀ h₁ => lpInput_phase_one hn hx hc i h₀ h₁,
      fun i t h₀ h₁ => lpInput_phase_two hn hx hc i h₀ h₁,
      fun i t h₀ h₁ => lpInput_phase_three hn hx hc i h₀ h₁, Or.inr ⟨hf, ?_⟩⟩
    exact lpInput_twoTypesTwoLarge hn hx hc rfl rfl rfl
  · -- the all-initial-modes case: the value is `U_ab`, attained by the symmetrized witness
    obtain ⟨X, Y, M, hf⟩ :=
      exists_symmState_allInitialFeasible hn hx hab hadm (heq ▸ hLU) (heq ▸ le_rfl)
    have hc := hf.common
    refine ⟨ja, jb, _, _, _, isGridConstant_lpInput hn hx hc, isCumulative_lpInput hn hx hc,
      le_antisymm (gridOPT_le_gridF (by omega) hx (isGridConstant_lpInput hn hx hc) 1)
        (allInitial_le_gridOPT hn hx hf),
      fun i t h₀ h₁ => lpInput_phase_one hn hx hc i h₀ h₁,
      fun i t h₀ h₁ => lpInput_phase_two hn hx hc i h₀ h₁,
      fun i t h₀ h₁ => lpInput_phase_three hn hx hc i h₀ h₁, Or.inl ⟨hf, ?_⟩⟩
    exact lpInput_twoTypesOneLarge hn hx hc rfl rfl rfl

/-! ## Arbitrary inputs are covered -/

/-- **SC20, the SC05 sub-clause.** The value computed by `eq:grid-minimax-formula` is the
maximum of the grid one-switch instance optimum over *all* cumulative inputs, not only over
the grid-constant ones that `gridF` maximizes over. So the formula covers arbitrary relaxed
inputs, which is the sense in which `thm:finite-one` applies "to arbitrary measurable relaxed
inputs through `lem:endpoint`": by SC05 the grid error of a grid schedule depends on the input
only through its grid endpoints, so by SC06 (`gridOPT_cellAverageInput`) replacing an input by
its cell average changes neither the grid instance optimum nor membership in the cumulative
class, and by SC07 (`exists_gridF_eq`) the value is attained.

`IsCumulative A T` is the package's input class `Acal_n(T)`: nonnegative, nondecreasing,
jointly 1-Lipschitz allocations starting at zero. It contains every cumulative allocation of a
measurable relaxed control, and the statement quantifies over all of it; no measurability or
grid-constancy hypothesis appears. -/
theorem isGreatest_gridOPT_cumulative (hn : 0 < n) (hx : IsGrid x T) :
    IsGreatest {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsCumulative A T ∧ v = gridOPT x A T 1}
      (gridF x n 1 T) := by
  have hbdd : BddAbove {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧
      v = gridOPT x A T 1} := by
    refine ⟨T, ?_⟩
    rintro v ⟨A, ⟨r, hr, rfl⟩, rfl⟩
    exact gridOPT_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) 1
  refine ⟨?_, ?_⟩
  · obtain ⟨A, ⟨r, hr, rfl⟩, heq⟩ := exists_gridF_eq hn hx 1
    exact ⟨_, gridCumulative_isCumulative hx.orderedTimes hr, heq⟩
  · rintro v ⟨A, hA, rfl⟩
    rw [gridOPT_cellAverageInput hn hx hA 1]
    exact le_csSup hbdd ⟨cellAverageInput x A, isGridConstant_cellAverageInput hx hA, rfl⟩

/-! ## `N = 1`, zero-length phases and constant integer controls are permitted

The formula has no hypothesis beyond `3 ≤ n`, `IsGrid x T` and `0 < T`, so a one-cell grid is
covered; `AdmissiblePair` allows `ja = jb` and `jb.succ = Fin.last N`, that is, zero-length
first, second and third phases, and the three phase formulas above hold without any
nondegeneracy hypothesis (`lpInput_eq_of_degenerate_phase_two` and
`lpInput_eq_of_degenerate_phase_three` record what happens then). Constant integer controls
are among the schedules the maximizer is tested against, as the two statements below make
explicit. -/

/-- `N = 1`: the formula on a one-cell grid, an instance of `isGreatest_gridCandidateSet`. -/
theorem isGreatest_gridCandidateSet_one_cell (hn : 3 ≤ n) {x : Fin 2 → ℝ} {T : ℝ}
    (hx : IsGrid x T) (hT : 0 < T) : IsGreatest (gridCandidateSet n x T) (gridF x n 1 T) :=
  isGreatest_gridCandidateSet hn hx hT

/-- Constant integer controls are permitted: an all-initial-modes feasible point also
obstructs every constant schedule, which is the degenerate one-switch schedule. -/
theorem le_D_constSchedule_of_allInitialFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) (p : Fin n) :
    E ≤ D (lpInput n x T ja jb u v m) (constSchedule p T) T := by
  have h0n : (0 : ℕ) < n := by omega
  have h1n : (1 : ℕ) < n := by omega
  obtain ⟨q, hq⟩ : ∃ q : Fin n, q ≠ p := by
    rcases eq_or_ne p ⟨0, h0n⟩ with h | h
    · exact ⟨⟨1, h1n⟩, by rw [h]; simp [Fin.ext_iff]⟩
    · exact ⟨⟨0, h0n⟩, fun hh => h hh.symm⟩
  have h := allInitial_le_D_oneSwitch hn hx hf hq (0 : Fin (N + 1))
  rwa [hx.first, oneSwitch_zero] at h

/-- Constant integer controls are permitted: the same for the two-large-modes family. -/
theorem le_D_constSchedule_of_twoLargeFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) (p : Fin n) :
    E ≤ D (lpInput n x T ja jb u v m) (constSchedule p T) T := by
  have h := twoLarge_le_D_oneSwitch hn hx hf p p (0 : Fin (N + 1))
  rwa [hx.first, oneSwitch_zero] at h

end GridSwitching
