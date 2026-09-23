import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Compactness
import Formal.GridSwitching.UniformTransfer
import Formal.GridSwitching.BinaryTransfer
import Formal.GridSwitching.Transfer
import Formal.GridSwitching.Refinement

/-!
# SC30 and SC32: the certified coarsening bracket and input perturbation

This module proves `thm:certified-coarsening` and `cor:coarse-perturbation` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex`, together with the three
remark paragraphs that follow the theorem.

## SC30: the coarsening certificate

Write `U_h = gridOPT x A T s` for the exact optimum over schedules that switch only at the
nodes of a uniform coarse grid of width `h`, and `V_h` for a coarse schedule attaining it
(`exists_gridOPT_eq`, SC07). Then `eq:coarsening-certificate` is

`U_h - h < OPT A T s ≤ U_h = D A V_h T`   (`coarsening_certificate`).

Each of the three relations comes from a different place. The right equality is attainment.
The middle inequality `OPT ≤ U_h` is pure restriction of the schedule class
(`OPT_le_gridOPT`). The strict left inequality is SC25 (`gridOPT_lt_OPT_add`), whose strictness
rests on the continuous optimum being *attained*, not merely approached. The point of the
certificate is that all three quantities are computable from the coarse node values alone:
`gridSchedule_D_le_iff` evaluates `D A V_h T` exactly from `A i (x q)`, with no constancy
assumption on the rates inside coarse cells.

The consequences proved here are the ones listed in `topics/17-grid-switching/CLAIMS.md`.

* The `M = ⌈1/eps⌉` statement: `coarsening_suboptimality` for any width with `h ≤ eps * T`,
  and `exists_coarsening_ceil` on the concrete grid `uniformGrid ⌈1/eps⌉₊ (T / ⌈1/eps⌉₊)`.
  The source's `eps ≤ 1` is carried as a hypothesis but is not needed: `⌈1/eps⌉₊ ≥ 1` already
  follows from `eps > 0`.
* The two sharper special cases, with `h/2` in place of `h` and a **non-strict** lower
  endpoint. For `n = 2` and any `s` this is SC27 (`exists_isGridSchedule_binary`) applied to
  an attained continuous optimum: `coarsening_certificate_binary` on an arbitrary grid, with
  `meshWidth x` in place of `h`, and `coarsening_certificate_binary_uniform` on a uniform
  grid of `M ≥ 1` cells. For `s = 1` and any `n` it is a separate argument, carried out in
  `gridOPT_le_OPT_add_half_one_switch`, and it too holds on an **arbitrary** grid, with
  `meshWidth x` in place of `h`: the attained continuous optimum has a single switch time, and
  moving it to a nearest node (`exists_node_abs_sub_le_meshWidth`, which locates the cell
  containing the time by `exists_cell_mem_Icc` and then takes the nearer of its two endpoints)
  changes every cumulative occupation by at most `meshWidth x / 2`, because
  `abs_occupation_sub_occupation_le` bounds the change by the sum of the displacements of the
  switch times, and the first and last times do not move. The source states this case only for
  a uniform grid; that form is `gridOPT_le_OPT_add_half_one_switch_uniform` and
  `coarsening_certificate_one_switch_uniform`, obtained through `meshWidth_eq_of_uniform`.
* The clipping remark: `coarsening_certificate_clipped` replaces the lower endpoint by
  `max (U_h - h) 0`, `coarsening_zero_lt_OPT` retains strictness when `U_h - h = 0`, and
  `coarsening_clipped_eq` exhibits an instance where the clipped endpoint is attained with
  equality, so the clipped form genuinely cannot be made strict.
* The nested-grid chain: `coarsening_certificate_nested`.

## How the hypotheses are stated

"Uniform coarse grid of `M` cells of width `h`" is the hypothesis triple `IsGrid x T`,
`0 < h`, `∀ j : Fin M, cellLength x j = h`, exactly as in SC24 and SC25, so that the results
apply to any grid that happens to be uniform. The relation `T = M * h` follows from
`horizon_eq_of_uniform`; when `M > 0`, it also gives `h = T / M` and `T > 0`. At `M = 0`,
uniformity is vacuous and `T = 0`, so the certificate remains valid as `-h < 0`. The theorem
`exists_coarsening_ceil` records that the hypotheses are met by its concrete `uniformGrid`
on an explicitly positive horizon.

"The coarse grid's nodes are a subset of a finer switching grid" is stated as
`Set.range x ⊆ Set.range y` for two grids on the same horizon. Nothing else is assumed: the
monotone index embedding `e` with `y ∘ e = x` is *derived* by choice, its monotonicity follows
from both grids being strictly increasing, and `e 0 = 0`, `e (Fin.last M) = Fin.last Nf`
follow from the shared endpoints (`isGridSchedule_of_range_subset`).

## SC32: input perturbation

With `‖A - Ã‖_∞ ≤ delta` stated pointwise as `∀ i, ∀ t ∈ Icc 0 T, |A i t - Ã i t| ≤ delta`,
and `U_h`, `V_h` the exact coarse optimum and an attaining coarse schedule **for `Ã`**,
`perturbed_certificate` proves `eq:perturbed-certificate`

`U_h - h - delta < OPT A T s ≤ D A V_h T ≤ U_h + delta`,

hence `perturbed_suboptimality`: the returned schedule is strictly within `h + 2 * delta` of
the true optimum. The left inequality uses the `1`-Lipschitz dependence of `OPT` on the input
(`abs_OPT_sub_OPT_le`, SC07) together with the strict lower certificate for `Ã`; the right one
is the triangle inequality `D_le_D_add_input`. A pointwise rate bound `rho` integrates to
`delta = rho * T`: this *is* formalized here, as `abs_cumulative_sub_le_of_rate_le`, and fed
back into the certificate by `exists_perturbed_certificate_rate`.

## The coarse-data construction for nonaligned grids

The certificate is only useful if the coarse data `A i (x q)` can actually be formed from the
given description of `A`. The source's recipe — traverse the sorted input and coarse endpoints
together and add, over each segment of their common refinement, its length times the known
input rate — is formalized in `Formal.GridSwitching.Refinement`, which this module imports:

* correctness of the traversal, with **no alignment** between the input and coarse grids:
  `gridCumulative_coarseNode_eq_refinementSum`, resting on the refinement invariance
  `gridCumulative_refine` and the node evaluation `gridCumulative_node_eq_prefixSum`;
* well-definedness of "the known input rate": `exists_fineCell`, `exists_refinementRates`;
* the size recursion: the common refinement of an `M`-cell and an `N`-cell grid has at most
  `M + N - 1` cells (`card_refinementNodes_le`, `exists_commonRefinement`);
* the source's caveat that "merely grouping whole fine cells would be incorrect for nonaligned
  grids", justified by an explicit instance: `wholeCellSum_ne_gridCumulative`.

## What is deliberately not claimed

`topics/17-grid-switching/CLAIMS.md` excludes machine-level cost models. What remains excluded
is therefore only the *counted cost*: the operation count `O(n(N+M))` for the coarse-data
construction, the arithmetic bound `eq:coarsening-complexity`
`O(n(N+M) + C(M-1, k-1) n (k 2^k + 3^k))`, and the polynomial bit-complexity assertion. The
correctness and size-recursion content of that same paragraph is *not* excluded and is proved
in `Formal.GridSwitching.Refinement` as listed above; what is proved here is the *validity of
the certificate*: the bracket `eq:coarsening-certificate`, its perturbed form
`eq:perturbed-certificate`, and the stated consequences. The "additive, not relative" remark
is not formalized as such; the instance with `OPT = 0` used in `coarsening_clipped_eq` is
precisely the situation it describes.
-/

namespace GridSwitching

open Set

variable {n M : ℕ}

/-! ## Uniform grids: node values, mesh width, nearest node -/

/-- On a grid all of whose cells have length `h`, the `q`-th node is `q * h`. -/
theorem node_eq_of_uniform {x : Fin (M + 1) → ℝ} {T h : ℝ} (hx : IsGrid x T)
    (hunif : ∀ j : Fin M, cellLength x j = h) (q : Fin (M + 1)) : x q = (q : ℕ) * h := by
  induction q using Fin.induction with
  | zero => simpa using hx.first
  | succ j ih =>
    have hj : x j.succ = x j.castSucc + h := by
      have := hunif j
      rw [cellLength] at this
      linarith
    rw [hj, ih, Fin.val_castSucc, Fin.val_succ]
    push_cast
    ring

/-- The horizon of a uniform grid of `M` cells of width `h` is `M * h`. -/
theorem horizon_eq_of_uniform {x : Fin (M + 1) → ℝ} {T h : ℝ} (hx : IsGrid x T)
    (hunif : ∀ j : Fin M, cellLength x j = h) : T = (M : ℝ) * h := by
  have := node_eq_of_uniform hx hunif (Fin.last M)
  rw [hx.last] at this
  simpa using this

/-- The mesh width of a uniform grid with at least one cell is the common cell length. -/
theorem meshWidth_eq_of_uniform {x : Fin (M + 1) → ℝ} {h : ℝ} (hM : 0 < M)
    (hunif : ∀ j : Fin M, cellLength x j = h) : meshWidth x = h := by
  have : Nonempty (Fin M) := ⟨⟨0, hM⟩⟩
  simp only [meshWidth, hunif]
  exact ciSup_const

/-- Every time of the horizon has a node of a uniform grid within half the cell width. -/
theorem exists_node_abs_sub_le {x : Fin (M + 1) → ℝ} {T h : ℝ} (hx : IsGrid x T) (hh : 0 < h)
    (hunif : ∀ j : Fin M, cellLength x j = h) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    ∃ q : Fin (M + 1), |t - x q| ≤ h / 2 := by
  have hT : T = (M : ℝ) * h := horizon_eq_of_uniform hx hunif
  have hr0 : 0 ≤ t / h := div_nonneg ht.1 hh.le
  have hrM : t / h ≤ (M : ℝ) := by
    rw [div_le_iff₀ hh]
    exact hT ▸ ht.2
  have hnn : (0 : ℝ) ≤ t / h + 1 / 2 := by linarith
  set u : ℕ := ⌊t / h + 1 / 2⌋₊ with hu
  have huM : u < M + 1 := by
    rw [hu, Nat.floor_lt hnn]
    push_cast
    linarith
  refine ⟨⟨u, huM⟩, ?_⟩
  have hnode : x ⟨u, huM⟩ = (u : ℝ) * h := node_eq_of_uniform hx hunif ⟨u, huM⟩
  have hle : (u : ℝ) ≤ t / h + 1 / 2 := Nat.floor_le hnn
  have hlt : t / h + 1 / 2 < (u : ℝ) + 1 := Nat.lt_floor_add_one _
  have hfe : (t / h + 1 / 2) * h = t + h / 2 := by field_simp
  have h1 : (u : ℝ) * h ≤ t + h / 2 := by
    have := mul_le_mul_of_nonneg_right hle hh.le
    rwa [hfe] at this
  have h2 : t - h / 2 < (u : ℝ) * h := by
    have hlt' : t / h - 1 / 2 < (u : ℝ) := by linarith
    have := mul_lt_mul_of_pos_right hlt' hh
    have hfe' : (t / h - 1 / 2) * h = t - h / 2 := by field_simp
    rwa [hfe'] at this
  rw [hnode, abs_le]
  constructor <;> linarith

/-! ## Arbitrary grids: cell location and nearest node -/

/-- Every time of the horizon lies in some cell of the grid. The cell is the first one whose
right node reaches `t`; minimality puts its left node at or below `t`, except for the first
cell, whose left node is the origin. -/
theorem exists_cell_mem_Icc {x : Fin (M + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (hM : 0 < M)
    {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : ∃ j : Fin M, x j.castSucc ≤ t ∧ t ≤ x j.succ := by
  classical
  have hex : ∃ k : ℕ, ∃ h : k < M, t ≤ x (⟨k, h⟩ : Fin M).succ := by
    refine ⟨M - 1, by omega, ?_⟩
    have hsucc : (⟨M - 1, by omega⟩ : Fin M).succ = Fin.last M := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_last]
      omega
    rw [hsucc, hx.last]
    exact ht.2
  obtain ⟨hlt, hle⟩ := Nat.find_spec hex
  refine ⟨⟨Nat.find hex, hlt⟩, ?_, hle⟩
  rcases Nat.eq_zero_or_pos (Nat.find hex) with h0 | hpos
  · have hzero : (⟨Nat.find hex, hlt⟩ : Fin M).castSucc = 0 := by
      apply Fin.ext
      simpa using h0
    rw [hzero, hx.first]
    exact ht.1
  · have hpred : Nat.find hex - 1 < M := by omega
    have hmin := Nat.find_min hex (m := Nat.find hex - 1) (by omega)
    have hno : ¬ t ≤ x (⟨Nat.find hex - 1, hpred⟩ : Fin M).succ := fun hcon => hmin ⟨hpred, hcon⟩
    have hcell : (⟨Nat.find hex - 1, hpred⟩ : Fin M).succ
        = (⟨Nat.find hex, hlt⟩ : Fin M).castSucc := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    rw [hcell] at hno
    exact (not_le.mp hno).le

/-- Every time of the horizon has a node of the grid within half the **mesh width**, on an
**arbitrary** grid: no uniformity is assumed. The two distances from `t` to the endpoints of
its cell sum to that cell's length, so the smaller of them is at most half the cell length,
hence at most half the mesh width.

At `M = 0` the grid is the single node `0` on the degenerate horizon `T = 0`, where both sides
are `0`; note that `meshWidth x` is then a supremum over an empty index and equals `0`. -/
theorem exists_node_abs_sub_le_meshWidth {x : Fin (M + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : ∃ q : Fin (M + 1), |t - x q| ≤ meshWidth x / 2 := by
  rcases Nat.eq_zero_or_pos M with rfl | hM
  · have hT : (0 : ℝ) = T := by rw [← hx.first]; simpa using hx.last
    have ht0 : t = 0 := le_antisymm (by linarith [ht.2]) ht.1
    have hmesh : meshWidth x = 0 := Real.iSup_of_isEmpty _
    exact ⟨0, by rw [ht0, hx.first, hmesh]; norm_num⟩
  · obtain ⟨j, hl, hr⟩ := exists_cell_mem_Icc hx hM ht
    have hcl : cellLength x j ≤ meshWidth x := cellLength_le_meshWidth x j
    rw [cellLength] at hcl
    rcases le_total (t - x j.castSucc) (x j.succ - t) with hc | hc
    · refine ⟨j.castSucc, ?_⟩
      rw [abs_of_nonneg (by linarith)]
      linarith
    · refine ⟨j.succ, ?_⟩
      rw [abs_sub_comm, abs_of_nonneg (by linarith)]
      linarith

/-! ## SC30: the coarsening certificate -/

/-- SC30, `eq:coarsening-certificate`: on a uniform coarse grid of width `h`, the exact coarse
optimum `U_h = gridOPT x A T s` and any attaining coarse schedule `V_h` satisfy
`U_h - h < OPT A T s ≤ U_h = D A V_h T`. -/
theorem coarsening_certificate (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) {V : Fin n → ℝ → ℝ}
    (hVopt : gridOPT x A T s = D A V T) :
    gridOPT x A T s - h < OPT A T s ∧ OPT A T s ≤ gridOPT x A T s ∧
      gridOPT x A T s = D A V T := by
  refine ⟨?_, OPT_le_gridOPT_uniform hn hx hh hunif hA s, hVopt⟩
  have := gridOPT_lt_OPT_add hn hx hh hunif hA s
  linarith

/-- SC30, `eq:coarsening-certificate` with the attaining coarse schedule produced. -/
theorem exists_coarsening_certificate (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) V ∧
      gridOPT x A T s - h < OPT A T s ∧ OPT A T s ≤ gridOPT x A T s ∧
        gridOPT x A T s = D A V T := by
  obtain ⟨V, hV, hVopt⟩ := exists_gridOPT_eq hn x A T s
  exact ⟨V, hV, coarsening_certificate hn hx hh hunif hA s hVopt⟩

/-- SC30, suboptimality of the returned schedule: whenever the coarse width satisfies
`h ≤ eps * T`, the coarse optimizer is strictly within `eps * T` of the continuous optimum. -/
theorem coarsening_suboptimality (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h eps : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) (heps : h ≤ eps * T) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) V ∧ gridOPT x A T s = D A V T ∧
      D A V T - OPT A T s < eps * T := by
  obtain ⟨V, hV, hlow, _, hVopt⟩ := exists_coarsening_certificate hn hx hh hunif hA s
  exact ⟨V, hV, hVopt, by rw [← hVopt]; linarith⟩

/-- SC30, the `M = ⌈1/eps⌉` consequence: on the uniform grid of `⌈1/eps⌉` cells of width
`T / ⌈1/eps⌉` the exact coarse optimizer has suboptimality strictly below `eps * T`.

The hypothesis `eps ≤ 1` of the source is recorded but not needed: `⌈1/eps⌉ ≥ 1` already
follows from `eps > 0`. -/
theorem exists_coarsening_ceil (hn : 0 < n) {T eps : ℝ} (hT : 0 < T) (heps : 0 < eps)
    (_heps1 : eps ≤ 1) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    ∃ V : Fin n → ℝ → ℝ,
      IsGridSchedule (uniformGrid ⌈1 / eps⌉₊ (T / (⌈1 / eps⌉₊ : ℝ))) (s + 1) V ∧
        gridOPT (uniformGrid ⌈1 / eps⌉₊ (T / (⌈1 / eps⌉₊ : ℝ))) A T s = D A V T ∧
          D A V T - OPT A T s < eps * T := by
  have hMc1 : 1 ≤ ⌈1 / eps⌉₊ := by
    rw [Nat.one_le_ceil_iff]
    positivity
  have hge : 1 / eps ≤ ((⌈1 / eps⌉₊ : ℕ) : ℝ) := Nat.le_ceil _
  obtain ⟨M', hM'⟩ : ∃ M', ⌈1 / eps⌉₊ = M' + 1 := ⟨⌈1 / eps⌉₊ - 1, by omega⟩
  rw [hM'] at hge ⊢
  have hMcR : (0 : ℝ) < ((M' + 1 : ℕ) : ℝ) := by positivity
  have hh : 0 < T / ((M' + 1 : ℕ) : ℝ) := div_pos hT hMcR
  have hTeq : ((M' + 1 : ℕ) : ℝ) * (T / ((M' + 1 : ℕ) : ℝ)) = T := by field_simp
  have hx : IsGrid (uniformGrid (M' + 1) (T / ((M' + 1 : ℕ) : ℝ))) T := by
    have hg := isGrid_uniformGrid (N := M' + 1) hh
    rwa [hTeq] at hg
  have hle : T / ((M' + 1 : ℕ) : ℝ) ≤ eps * T := by
    rw [div_le_iff₀ hMcR]
    calc T = (1 / eps) * (eps * T) := by field_simp
      _ ≤ ((M' + 1 : ℕ) : ℝ) * (eps * T) :=
        mul_le_mul_of_nonneg_right hge (by positivity)
      _ = eps * T * ((M' + 1 : ℕ) : ℝ) := by ring
  exact coarsening_suboptimality hn hx hh (fun j => cellLength_uniformGrid j) hA s hle

/-! ### SC30: the sharper special cases -/

/-- With two modes, on an **arbitrary** grid, the grid optimum exceeds the continuous optimum
by at most half the mesh width. This is SC27 (`exists_isGridSchedule_binary`) applied to an
attained continuous optimum; unlike SC25 the bound is non-strict. -/
theorem gridOPT_le_OPT_add_half_meshWidth {x : Fin (M + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin 2 → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s ≤ OPT A T s + meshWidth x / 2 := by
  have hn : 0 < 2 := by norm_num
  obtain ⟨W, hW, hWopt⟩ := exists_OPT_eq hn hA hx.horizon_nonneg s
  obtain ⟨V, hV, hWV⟩ := exists_isGridSchedule_binary hx hW
  have hWc : IsCumulative W T := hW.isCumulative
  have hVc : IsCumulative V T := (hV.isSchedule hx).isCumulative
  have hstep : D A V T ≤ D A W T + D W V T :=
    D_le_D_add_schedule hn hA hWc hx.horizon_nonneg fun i t ht => by
      rw [abs_sub_comm]
      exact le_D hWc hVc i ht
  have hgrid : gridOPT x A T s ≤ D A V T := gridOPT_le_D hn hx hA hx.horizon_nonneg hV
  rw [hWopt]
  linarith

/-- SC30, the `n = 2` refinement on an arbitrary grid:
`U - meshWidth/2 ≤ OPT A T s ≤ U`, both inequalities non-strict. -/
theorem coarsening_certificate_binary {x : Fin (M + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin 2 → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s - meshWidth x / 2 ≤ OPT A T s ∧ OPT A T s ≤ gridOPT x A T s := by
  refine ⟨by linarith [gridOPT_le_OPT_add_half_meshWidth hx hA s],
    OPT_le_gridOPT (by norm_num) hx hA s⟩

/-- SC30, the `n = 2` refinement on a uniform coarse grid of width `h` with `M ≥ 1` cells:
`U_h - h/2 ≤ OPT A T s ≤ U_h`. -/
theorem coarsening_certificate_binary_uniform {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hM : 0 < M) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin 2 → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s - h / 2 ≤ OPT A T s ∧ OPT A T s ≤ gridOPT x A T s := by
  rw [← meshWidth_eq_of_uniform hM hunif]
  exact coarsening_certificate_binary hx hA s

/-- SC30, the `s = 1` refinement for any number of modes, on an **arbitrary** grid: moving the
single switch of an attained continuous optimum to a nearest grid node changes the cumulative
occupation by at most half the mesh width. The source states this for a uniform grid; no
uniformity is needed, and the uniform form is `gridOPT_le_OPT_add_half_one_switch_uniform`. -/
theorem gridOPT_le_OPT_add_half_one_switch (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    gridOPT x A T 1 ≤ OPT A T 1 + meshWidth x / 2 := by
  obtain ⟨W, hW, hWopt⟩ := exists_OPT_eq hn hA hx.horizon_nonneg 1
  obtain ⟨p, τ, hτ, rfl⟩ := hW
  obtain ⟨q, hq⟩ := exists_node_abs_sub_le_meshWidth hx (hτ.mem_Icc 1)
  set g : Fin 3 → Fin (M + 1) := ![0, q, Fin.last M] with hg
  have hgmono : Monotone g := by
    refine Fin.monotone_iff_le_succ.mpr fun i => ?_
    fin_cases i <;> simp [hg, Fin.le_last]
  have hV : IsGridSchedule x 2 (occupation p (x ∘ g)) := ⟨p, g, hgmono, rfl, rfl, rfl⟩
  have hsum : ∀ (i : Fin n) (t : ℝ),
      |occupation p τ i t - occupation p (x ∘ g) i t| ≤ meshWidth x / 2 := by
    intro i t
    refine (abs_occupation_sub_occupation_le p τ (x ∘ g) i t).trans ?_
    rw [Fin.sum_univ_three]
    have h0 : τ 0 - (x ∘ g) 0 = 0 := by simp [hg, hτ.first, hx.first]
    have hτ2 : τ 2 = T := hτ.last
    have h2 : τ 2 - (x ∘ g) 2 = 0 := by simp [hg, hτ2, hx.last]
    rw [h0, h2]
    simpa [hg] using hq
  have hWc : IsCumulative (occupation p τ) T := occupation_isCumulative p hτ
  have hstep : D A (occupation p (x ∘ g)) T ≤ D A (occupation p τ) T + meshWidth x / 2 :=
    D_le_D_add_schedule hn hA hWc hx.horizon_nonneg fun i t _ => by
      rw [abs_sub_comm]
      exact hsum i t
  have hgrid : gridOPT x A T 1 ≤ D A (occupation p (x ∘ g)) T :=
    gridOPT_le_D hn hx hA hx.horizon_nonneg hV
  rw [hWopt]
  linarith

/-- SC30, the `s = 1` refinement on an **arbitrary** grid:
`U - meshWidth/2 ≤ OPT A T 1 ≤ U`, for any number of modes, both inequalities non-strict. -/
theorem coarsening_certificate_one_switch (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    gridOPT x A T 1 - meshWidth x / 2 ≤ OPT A T 1 ∧ OPT A T 1 ≤ gridOPT x A T 1 :=
  ⟨by linarith [gridOPT_le_OPT_add_half_one_switch hn hx hA], OPT_le_gridOPT hn hx hA 1⟩

/-- SC30, the `s = 1` refinement in the source's uniform setting: on a uniform coarse grid of
width `h` with `M ≥ 1` cells, `gridOPT x A T 1 ≤ OPT A T 1 + h / 2`. -/
theorem gridOPT_le_OPT_add_half_one_switch_uniform (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hM : 0 < M) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    gridOPT x A T 1 ≤ OPT A T 1 + h / 2 := by
  rw [← meshWidth_eq_of_uniform hM hunif]
  exact gridOPT_le_OPT_add_half_one_switch hn hx hA

/-- SC30, the `s = 1` refinement in the source's uniform setting: `U_h - h/2 ≤ OPT A T 1 ≤ U_h`
on a uniform coarse grid of width `h` with `M ≥ 1` cells, for any number of modes. -/
theorem coarsening_certificate_one_switch_uniform (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hM : 0 < M) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    gridOPT x A T 1 - h / 2 ≤ OPT A T 1 ∧ OPT A T 1 ≤ gridOPT x A T 1 := by
  rw [← meshWidth_eq_of_uniform hM hunif]
  exact coarsening_certificate_one_switch hn hx hA

/-! ### SC30: the clipping remark -/

/-- SC30, clipping: the lower endpoint of `eq:coarsening-certificate` may be replaced by zero,
at the cost of making that endpoint non-strict. -/
theorem coarsening_certificate_clipped (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    max (gridOPT x A T s - h) 0 ≤ OPT A T s := by
  have hlt : gridOPT x A T s - h < OPT A T s := by
    have := gridOPT_lt_OPT_add hn hx hh hunif hA s
    linarith
  exact max_le hlt.le (OPT_nonneg hn hA hx.horizon_nonneg s)

/-- SC30, clipping: when the clipping level is exactly zero, strictness is retained. -/
theorem coarsening_zero_lt_OPT (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ)
    (h0 : gridOPT x A T s - h = 0) : 0 < OPT A T s := by
  have := gridOPT_lt_OPT_add hn hx hh hunif hA s
  linarith

/-- SC30, clipping: the clipped endpoint really is non-strict. For the input that is itself
the cumulative occupation of a constant schedule, both optima vanish, the clipping level
`U_h - h = -h` is negative, and the clipped endpoint is attained with equality. -/
theorem coarsening_clipped_eq (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h : ℝ} (hx : IsGrid x T)
    (hh : 0 < h) (q : Fin n) (s : ℕ) :
    gridOPT x (constSchedule q T) T s - h < 0 ∧
      max (gridOPT x (constSchedule q T) T s - h) 0 = OPT (constSchedule q T) T s := by
  have hT : (0 : ℝ) ≤ T := hx.horizon_nonneg
  have hAc : IsCumulative (constSchedule q T) T :=
    (isSchedule_constSchedule hT q).isCumulative
  have hD : D (constSchedule q T) (constSchedule q T) T = 0 :=
    le_antisymm (D_le le_rfl fun i t _ => by simp) (D_nonneg hn hAc hAc hT)
  have hgs : IsGridSchedule x (s + 1) (constSchedule q T) :=
    IsGridSchedule.mono hn (Nat.succ_le_succ (Nat.zero_le s))
      (isGridSchedule_constSchedule hx q)
  have hgrid : gridOPT x (constSchedule q T) T s ≤ 0 := by
    have := gridOPT_le_D hn hx hAc hT hgs
    rwa [hD] at this
  have hopt : OPT (constSchedule q T) T s ≤ gridOPT x (constSchedule q T) T s :=
    OPT_le_gridOPT hn hx hAc s
  have hoptnn : 0 ≤ OPT (constSchedule q T) T s := OPT_nonneg hn hAc hT s
  have hopt0 : OPT (constSchedule q T) T s = 0 := le_antisymm (hopt.trans hgrid) hoptnn
  have hgrid0 : gridOPT x (constSchedule q T) T s = 0 :=
    le_antisymm hgrid (by linarith)
  refine ⟨by rw [hgrid0]; linarith, ?_⟩
  rw [hgrid0, hopt0, max_eq_right (by linarith)]

/-! ### SC30: the nested-grid chain

"The coarse grid's nodes are a subset of the fine switching grid" is formalized as
`Set.range x ⊆ Set.range y`. Nothing more is assumed: a monotone index embedding is *derived*
from the two grids being strictly increasing, and the two endpoint conditions `e 0 = 0` and
`e (Fin.last M) = Fin.last Nf` are derived from the shared horizon. -/

/-- If the nodes of the grid `x` are among the nodes of the grid `y`, then every `x`-grid
schedule is a `y`-grid schedule with the same block budget. -/
theorem isGridSchedule_of_range_subset {Nf : ℕ} {x : Fin (M + 1) → ℝ} {y : Fin (Nf + 1) → ℝ}
    {T : ℝ} (hx : IsGrid x T) (hy : IsGrid y T) (hsub : Set.range x ⊆ Set.range y) {k : ℕ}
    {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x k W) : IsGridSchedule y k W := by
  obtain ⟨e, hemono, he0, hel, he⟩ := exists_gridEmbedding hx hy hsub
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  refine ⟨p, e ∘ g, hemono.comp hg, ?_, ?_, ?_⟩
  · simp only [Function.comp_apply, hg0, he0]
  · simp only [Function.comp_apply, hgl, hel]
  · funext i t
    congr 1
    funext m
    simp only [Function.comp_apply, he]

/-- If the nodes of the coarse grid `x` are among the nodes of the fine grid `y`, then the
fine grid optimum is no larger than the coarse one. -/
theorem gridOPT_le_gridOPT_of_range_subset (hn : 0 < n) {Nf : ℕ} {x : Fin (M + 1) → ℝ}
    {y : Fin (Nf + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (hy : IsGrid y T)
    (hsub : Set.range x ⊆ Set.range y) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT y A T s ≤ gridOPT x A T s := by
  refine csInf_le_csInf (gridScheduleErrorSet_bddBelow hn hy hA hx.horizon_nonneg _)
    (gridScheduleErrorSet_nonempty hn A T (Nat.succ_pos s)) ?_
  rintro e ⟨V, hV, rfl⟩
  exact ⟨V, isGridSchedule_of_range_subset hx hy hsub hV, rfl⟩

/-- SC30, the nested-grid chain: if the coarse grid's nodes are a subset of the fine switching
grid's nodes, the coarse certificate also brackets the fine optimum,
`U_h - h < OPT A T s ≤ gridOPT y A T s ≤ U_h`. -/
theorem coarsening_certificate_nested (hn : 0 < n) {Nf : ℕ} {x : Fin (M + 1) → ℝ}
    {y : Fin (Nf + 1) → ℝ} {T h : ℝ} (hx : IsGrid x T) (hy : IsGrid y T) (hh : 0 < h)
    (hunif : ∀ j : Fin M, cellLength x j = h) (hsub : Set.range x ⊆ Set.range y)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s - h < OPT A T s ∧ OPT A T s ≤ gridOPT y A T s ∧
      gridOPT y A T s ≤ gridOPT x A T s := by
  refine ⟨?_, OPT_le_gridOPT hn hy hA s,
    gridOPT_le_gridOPT_of_range_subset hn hx hy hsub hA s⟩
  have := gridOPT_lt_OPT_add hn hx hh hunif hA s
  linarith

/-! ## SC32: input perturbation (`cor:coarse-perturbation`) -/

/-- SC32, `eq:perturbed-certificate`: if the available data describe `B` with
`‖A - B‖_∞ ≤ delta`, and `U_h = gridOPT x B T s`, `V` are the exact coarse optimum and an
attaining coarse schedule **for `B`**, then
`U_h - h - delta < OPT A T s ≤ D A V T ≤ U_h + delta`.

The left inequality combines the strict lower certificate for `B` with the `1`-Lipschitz
dependence of `OPT` on the input (`abs_OPT_sub_OPT_le`); the right one is the triangle
inequality `D_le_D_add_input`. -/
theorem perturbed_certificate (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h delta : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A B : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hB : IsCumulative B T)
    (hAB : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ delta) (s : ℕ)
    {V : Fin n → ℝ → ℝ} (hV : IsGridSchedule x (s + 1) V)
    (hVopt : gridOPT x B T s = D B V T) :
    gridOPT x B T s - h - delta < OPT A T s ∧ OPT A T s ≤ D A V T ∧
      D A V T ≤ gridOPT x B T s + delta := by
  have hT : (0 : ℝ) ≤ T := hx.horizon_nonneg
  have hlip := abs_le.mp (abs_OPT_sub_OPT_le hn hA hB hT s hAB)
  have hstrict : gridOPT x B T s - h < OPT B T s := by
    have := gridOPT_lt_OPT_add hn hx hh hunif hB s
    linarith
  refine ⟨by linarith [hlip.1], OPT_le_D hn hA hT (hV.isSchedule hx), ?_⟩
  have htri : D A V T ≤ D B V T + delta :=
    D_le_D_add_input hn hB (hV.isSchedule hx).isCumulative hT hAB
  rw [hVopt]
  linarith

/-- SC32 with the attaining coarse schedule for the perturbed data produced. -/
theorem exists_perturbed_certificate (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h delta : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A B : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hB : IsCumulative B T)
    (hAB : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ delta) (s : ℕ) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) V ∧ gridOPT x B T s = D B V T ∧
      gridOPT x B T s - h - delta < OPT A T s ∧ OPT A T s ≤ D A V T ∧
        D A V T ≤ gridOPT x B T s + delta := by
  obtain ⟨V, hV, hVopt⟩ := exists_gridOPT_eq hn x B T s
  exact ⟨V, hV, hVopt, perturbed_certificate hn hx hh hunif hA hB hAB s hV hVopt⟩

/-- SC32, the suboptimality consequence: the schedule returned by exact coarse optimization of
the perturbed data is strictly within `h + 2 * delta` of the true continuous optimum. -/
theorem perturbed_suboptimality (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h delta : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {A B : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hB : IsCumulative B T)
    (hAB : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |A i t - B i t| ≤ delta) (s : ℕ)
    {V : Fin n → ℝ → ℝ} (hV : IsGridSchedule x (s + 1) V)
    (hVopt : gridOPT x B T s = D B V T) :
    D A V T - OPT A T s < h + 2 * delta := by
  obtain ⟨hlow, _, hhigh⟩ := perturbed_certificate hn hx hh hunif hA hB hAB s hV hVopt
  linarith

/-! ### SC32: a pointwise rate bound integrates to `delta = rho * T` -/

/-- A pointwise bound `rho` on the difference of two relaxed controls integrates to the
cumulative bound `delta = rho * T`, which is exactly the hypothesis `hAB` of
`perturbed_certificate`. -/
theorem abs_cumulative_sub_le_of_rate_le {α β : Fin n → ℝ → ℝ} {T rho : ℝ}
    (hα : SimplexRates α T) (hβ : SimplexRates β T) (hT : 0 ≤ T)
    (hrate : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |α i t - β i t| ≤ rho) (i : Fin n) {t : ℝ}
    (ht : t ∈ Icc (0 : ℝ) T) : |cumulative α i t - cumulative β i t| ≤ rho * T := by
  have hrho : 0 ≤ rho := le_trans (abs_nonneg _) (hrate i 0 ⟨le_rfl, hT⟩)
  have hint : cumulative α i t - cumulative β i t = ∫ u in (0 : ℝ)..t, (α i u - β i u) := by
    rw [cumulative, cumulative, intervalIntegral.integral_sub
      (hα.intervalIntegrable le_rfl ht.1 ht.2 i) (hβ.intervalIntegrable le_rfl ht.1 ht.2 i)]
  have hbound : ∀ u ∈ Set.uIoc (0 : ℝ) t, ‖α i u - β i u‖ ≤ rho := by
    intro u hu
    rw [Set.uIoc_of_le ht.1] at hu
    rw [Real.norm_eq_abs]
    exact hrate i u ⟨hu.1.le, hu.2.trans ht.2⟩
  have hnorm := intervalIntegral.norm_integral_le_of_norm_le_const hbound
  rw [Real.norm_eq_abs, sub_zero, abs_of_nonneg ht.1] at hnorm
  rw [hint]
  exact hnorm.trans (mul_le_mul_of_nonneg_left ht.2 hrho)

/-- SC32 with the perturbation bound supplied by a pointwise rate bound `rho`, so that
`delta = rho * T`. -/
theorem exists_perturbed_certificate_rate (hn : 0 < n) {x : Fin (M + 1) → ℝ} {T h rho : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin M, cellLength x j = h)
    {α β : Fin n → ℝ → ℝ} (hα : SimplexRates α T) (hβ : SimplexRates β T)
    (hrate : ∀ i : Fin n, ∀ t ∈ Icc (0 : ℝ) T, |α i t - β i t| ≤ rho) (s : ℕ) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule x (s + 1) V ∧
      gridOPT x (cumulative β) T s = D (cumulative β) V T ∧
      gridOPT x (cumulative β) T s - h - rho * T < OPT (cumulative α) T s ∧
        OPT (cumulative α) T s ≤ D (cumulative α) V T ∧
          D (cumulative α) V T ≤ gridOPT x (cumulative β) T s + rho * T :=
  exists_perturbed_certificate hn hx hh hunif hα.isCumulative hβ.isCumulative
    (fun i _t ht =>
      abs_cumulative_sub_le_of_rate_le hα hβ hx.horizon_nonneg hrate i ht) s

end GridSwitching
