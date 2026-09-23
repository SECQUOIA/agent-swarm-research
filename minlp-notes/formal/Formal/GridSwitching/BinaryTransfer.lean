import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Rounding

/-!
# SC27: sharp binary transfer on an arbitrary grid

This module proves `prop:binary-transfer` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex`: with **two modes** and an
**arbitrary** (possibly nonuniform) grid, every finitely switching schedule has a grid schedule
with no more activation blocks whose discrepancy is at most half the mesh width, and the
constant one half cannot be improved.

The construction is the explicit invariant of the source. Write `e` for the mode-zero endpoint
discrepancy `V_0 - W_0` of the transferred schedule against the original one, and `Dm` for the
mesh width. On a cell of length `d ≤ Dm` carrying original mode-zero occupation `a`:

* if `a = d` the only supported choice is mode zero, and it leaves `e` unchanged;
* if `a = 0` the only supported choice is mode one, and it leaves `e` unchanged;
* otherwise both modes are supported, the two candidate discrepancies are `e - a` and
  `e + d - a`, the first is at most `Dm / 2`, the second at least `-Dm / 2`, and they differ by
  `d ≤ Dm`, so at least one lies in `[-Dm / 2, Dm / 2]`.

`binSel` below implements all three cases by the single rule "take mode one when it is
supported and keeps the discrepancy above `-Dm / 2`". The mode-one discrepancy is the negative
of the mode-zero one, so the same bound covers both components, and
`Endpoint.gridSchedule_D_le_iff` turns the grid-node bounds into a bound on the whole horizon.
The block budget is preserved by `Rounding.isGridSchedule_comp_blockMap`.

Sharpness is `binaryTransfer_sharp`: on a one-cell grid of length `L`, the schedule that
occupies each mode for half the cell is at distance at least `L / 2` from *every* grid
schedule, whatever its block budget.
-/

namespace GridSwitching

open Set

/-! ## The mesh width is nonnegative -/

/-- The mesh width of a grid is nonnegative; for the empty grid it is zero. -/
theorem meshWidth_nonneg {N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) :
    0 ≤ meshWidth x := by
  cases N with
  | zero => simp [meshWidth]
  | succ N =>
    exact le_trans (hx.cellLength_pos 0).le (cellLength_le_meshWidth x 0)

/-! ## The binary selection rule -/

/-- The running mode-zero endpoint discrepancy `e = V_0 - W_0` produced by the binary transfer
rule, for cell occupations `aa` of mode zero, cell lengths `dd`, and mesh width `Dm`. -/
noncomputable def binErr (aa dd : ℕ → ℝ) (Dm : ℝ) : ℕ → ℝ
  | 0 => 0
  | u + 1 =>
      if aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u then binErr aa dd Dm u - aa u
      else binErr aa dd Dm u + dd u - aa u

/-- The mode selected on cell `u` by the binary transfer rule: mode one whenever it is
supported and keeps the discrepancy at least `-Dm / 2`, and mode zero otherwise. -/
noncomputable def binSel (aa dd : ℕ → ℝ) (Dm : ℝ) (u : ℕ) : Fin 2 :=
  if aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u then 1 else 0

@[simp] theorem binErr_zero (aa dd : ℕ → ℝ) (Dm : ℝ) : binErr aa dd Dm 0 = 0 := rfl

/-- One step of the recursion, expressed through the selected mode: the discrepancy grows by
the cell length exactly when mode zero is selected, and always drops by the original mode-zero
occupation of the cell. -/
theorem binErr_succ (aa dd : ℕ → ℝ) (Dm : ℝ) (u : ℕ) :
    binErr aa dd Dm (u + 1)
      = binErr aa dd Dm u + (if binSel aa dd Dm u = 0 then dd u else 0) - aa u := by
  rw [binErr, binSel]
  by_cases h : aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u
  · rw [if_pos h, if_pos h, if_neg (by decide : ¬ (1 : Fin 2) = 0)]
    ring
  · rw [if_neg h, if_neg h, if_pos rfl]

/-- The invariant of `prop:binary-transfer`: the mode-zero discrepancy never leaves the
interval `[-Dm / 2, Dm / 2]`. -/
theorem abs_binErr_le {aa dd : ℕ → ℝ} {Dm : ℝ} (h0 : ∀ u, 0 ≤ aa u) (h1 : ∀ u, aa u ≤ dd u)
    (h2 : ∀ u, dd u ≤ Dm) (hD : 0 ≤ Dm) (u : ℕ) : |binErr aa dd Dm u| ≤ Dm / 2 := by
  induction u with
  | zero => simpa using by linarith
  | succ u ih =>
    rw [abs_le] at ih ⊢
    rw [binErr]
    by_cases h : aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u
    · rw [if_pos h]
      exact ⟨h.2, by linarith [h0 u, ih.2]⟩
    · rw [if_neg h]
      refine ⟨by linarith [h1 u, ih.1], ?_⟩
      rcases le_or_gt (dd u) (aa u) with hd | hd
      · have : aa u = dd u := le_antisymm (h1 u) hd
        rw [this]
        linarith [ih.2]
      · have hlt : binErr aa dd Dm u - aa u < -(Dm / 2) := by
          by_contra hcon
          exact h ⟨hd, by linarith⟩
        linarith [h2 u]

/-- Support of the selection: the selected mode has positive original occupation on the cell.
Mode zero is selected only when its occupation `aa u` is positive, and mode one only when its
occupation `dd u - aa u` is positive. -/
theorem binSel_support {aa dd : ℕ → ℝ} {Dm : ℝ} (h0 : ∀ u, 0 ≤ aa u) (h1 : ∀ u, aa u ≤ dd u)
    (h2 : ∀ u, dd u ≤ Dm) (hD : 0 ≤ Dm) {u : ℕ} (hpos : 0 < dd u) :
    (binSel aa dd Dm u = 0 → 0 < aa u) ∧ (binSel aa dd Dm u = 1 → 0 < dd u - aa u) := by
  have hinv := abs_le.mp (abs_binErr_le h0 h1 h2 hD u)
  constructor
  · intro hsel
    rw [binSel] at hsel
    by_cases h : aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u
    · rw [if_pos h] at hsel
      exact absurd hsel (by decide)
    · rcases le_or_gt (dd u) (aa u) with hd | hd
      · linarith [h1 u]
      · have hlt : binErr aa dd Dm u - aa u < -(Dm / 2) := by
          by_contra hcon
          exact h ⟨hd, by linarith⟩
        linarith [hinv.1]
  · intro hsel
    rw [binSel] at hsel
    by_cases h : aa u < dd u ∧ -(Dm / 2) ≤ binErr aa dd Dm u - aa u
    · linarith [h.1]
    · rw [if_neg h] at hsel
      exact absurd hsel.symm (by decide)

/-- Case distinction on the two modes. -/
private theorem fin_two_cases (i : Fin 2) : i = 0 ∨ i = 1 := by
  fin_cases i <;> simp

/-! ## SC27: the transfer theorem -/

/-- SC27, main statement (`prop:binary-transfer`): on an **arbitrary** grid, a two-mode
schedule with `k` activation blocks has a grid schedule with the same block budget, hence no
more switches, whose discrepancy is at most half the mesh width. The bound is not strict. -/
theorem exists_isGridSchedule_binary {N k : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {W : Fin 2 → ℝ → ℝ} (hW : IsSchedule k T W) :
    ∃ V : Fin 2 → ℝ → ℝ, IsGridSchedule x k V ∧ D W V T ≤ meshWidth x / 2 := by
  obtain ⟨p, τ, hτ, rfl⟩ := hW
  have hxm : Monotone x := hx.strictMono.monotone
  have hWcum : IsCumulative (occupation p τ) T := occupation_isCumulative p hτ
  set Dm : ℝ := meshWidth x with hDm
  have hD : 0 ≤ Dm := meshWidth_nonneg hx
  set nd : ℕ → ℝ := fun u => x (satNode N u) with hnddef
  have hndmono : Monotone nd := fun _ _ huv => hxm (satNode_mono huv)
  have hndmem : ∀ u, nd u ∈ Icc (0 : ℝ) T := fun u => hx.mem_Icc (satNode N u)
  set aa : ℕ → ℝ := fun u => occupation p τ 0 (nd (u + 1)) - occupation p τ 0 (nd u) with haadef
  set dd : ℕ → ℝ := fun u => nd (u + 1) - nd u with hdddef
  have hstep : ∀ u, nd u ≤ nd (u + 1) := fun u => hndmono (Nat.le_succ u)
  have h0 : ∀ u, 0 ≤ aa u := fun u => by
    have := occupation_mono (p := p) hτ.mono 0 (hstep u)
    simp only [haadef]
    linarith
  have h1 : ∀ u, aa u ≤ dd u := fun u =>
    occupation_lipschitz hτ 0 (hndmem u).1 (hstep u) (hndmem (u + 1)).2
  have h2 : ∀ u, dd u ≤ Dm := by
    intro u
    rcases lt_or_ge u N with hu | hu
    · have hc : dd u = cellLength x ⟨u, hu⟩ := by
        simp only [hdddef, hnddef, cellLength]
        rw [satNode_castSucc ⟨u, hu⟩, satNode_succ ⟨u, hu⟩]
      rw [hc]
      exact cellLength_le_meshWidth x _
    · have : nd (u + 1) = nd u := by
        simp only [hnddef]
        rw [satNode_of_le hu, satNode_of_le (le_trans hu (Nat.le_succ u))]
      simp only [hdddef, this]
      simpa using hD
  set y : Fin N → Fin 2 := fun j => binSel aa dd Dm (j : ℕ) with hydef
  have hcell : ∀ j : Fin N, nd (j : ℕ) = x j.castSucc ∧ nd ((j : ℕ) + 1) = x j.succ := by
    intro j
    exact ⟨by simp only [hnddef, satNode_castSucc], by simp only [hnddef, satNode_succ]⟩
  -- the transferred schedule tracks the original one at every grid node
  have hkey : ∀ u : ℕ,
      occupation y x 0 (nd u) - occupation p τ 0 (nd u) = binErr aa dd Dm u := by
    intro u
    induction u with
    | zero =>
      have h : nd 0 = 0 := by
        simp only [hnddef]
        rw [show satNode N 0 = 0 from Fin.ext (by simp [satNode])]
        exact hx.first
      rw [h, binErr_zero, occupation_zero hx.orderedTimes, occupation_zero hτ, sub_zero]
    | succ u ih =>
      have hocc : occupation y x 0 (nd (u + 1)) - occupation y x 0 (nd u)
          = if binSel aa dd Dm u = 0 then dd u else 0 := by
        rcases lt_or_ge u N with hu | hu
        · have hj := hcell ⟨u, hu⟩
          have hy : y ⟨u, hu⟩ = binSel aa dd Dm u := rfl
          by_cases hsel : binSel aa dd Dm u = 0
          · rw [if_pos hsel, hj.1, hj.2]
            have := occupation_selected_increment y hxm ⟨u, hu⟩ (le_refl (x (Fin.castSucc ⟨u, hu⟩)))
              (hxm (Fin.castSucc_le_succ _)) (le_refl (x (Fin.succ ⟨u, hu⟩)))
            rw [hy, hsel] at this
            rw [this]
            simp only [hdddef]
            rw [hj.1, hj.2]
          · have hne : (0 : Fin 2) ≠ y ⟨u, hu⟩ := by
              rw [hy]
              exact fun h => hsel h.symm
            rw [if_neg hsel, hj.1, hj.2]
            rw [occupation_other_const y hxm ⟨u, hu⟩ hne (le_refl (x (Fin.castSucc ⟨u, hu⟩)))
              (hxm (Fin.castSucc_le_succ _)) (le_refl (x (Fin.succ ⟨u, hu⟩)))]
            ring
        · have hsat : nd (u + 1) = nd u := by
            simp only [hnddef]
            rw [satNode_of_le hu, satNode_of_le (le_trans hu (Nat.le_succ u))]
          have hdz : dd u = 0 := by simp [hdddef, hsat]
          rw [hsat, sub_self, hdz]
          simp
      rw [binErr_succ, ← ih, ← hocc]
      simp only [haadef]
      ring
  -- support of the selection inside the original schedule
  have hsupp : ∀ j : Fin N,
      0 < occupation p τ (y j) (x j.succ) - occupation p τ (y j) (x j.castSucc) := by
    intro j
    have hpos : 0 < dd (j : ℕ) := by
      have hc : dd (j : ℕ) = cellLength x j := by
        simp only [hdddef]
        rw [(hcell j).1, (hcell j).2, cellLength]
      rw [hc]
      exact hx.cellLength_pos j
    have hs := binSel_support h0 h1 h2 hD hpos
    have hsum : occupation p τ 0 (x j.succ) - occupation p τ 0 (x j.castSucc)
        + (occupation p τ 1 (x j.succ) - occupation p τ 1 (x j.castSucc))
        = dd (j : ℕ) := by
      have e1 := occupation_sum p hτ (x j.succ)
      have e2 := occupation_sum p hτ (x j.castSucc)
      rw [Fin.sum_univ_two] at e1 e2
      rw [min_eq_left (hx.mem_Icc j.succ).2, min_eq_right (hx.mem_Icc j.succ).1] at e1
      rw [min_eq_left (hx.mem_Icc j.castSucc).2, min_eq_right (hx.mem_Icc j.castSucc).1] at e2
      simp only [hdddef]
      rw [(hcell j).1, (hcell j).2]
      linarith
    have haval : aa (j : ℕ) = occupation p τ 0 (x j.succ) - occupation p τ 0 (x j.castSucc) := by
      simp only [haadef]
      rw [(hcell j).1, (hcell j).2]
    have hy : y j = binSel aa dd Dm (j : ℕ) := rfl
    rcases fin_two_cases (y j) with hsel | hsel
    · rw [hsel]
      have hgt := hs.1 (hy ▸ hsel)
      rw [haval] at hgt
      linarith
    · rw [hsel]
      have hgt := hs.2 (hy ▸ hsel)
      linarith
  choose β hβ1 hβ2 hβ3 using fun j : Fin N =>
    exists_blockIndex hτ.mono (hxm (Fin.castSucc_le_succ j)) (hsupp j)
  have hβmono : Monotone β := blockMap_monotone hxm hτ.mono
    (fun j => hβ2 j) (fun j => hβ3 j)
  have hycomp : y = fun j => p (β j) := funext fun j => (hβ1 j).symm
  refine ⟨occupation y x, ?_, ?_⟩
  · rw [hycomp]
    exact isGridSchedule_comp_blockMap x p hβmono
  · rw [gridSchedule_D_le_iff hx (by rw [hycomp]; exact isGridSchedule_comp_blockMap x p hβmono)
      hWcum (by linarith)]
    intro q i
    have hq : x q = nd (q : ℕ) := by simp only [hnddef, satNode_coe]
    have h0q : occupation y x 0 (x q) - occupation p τ 0 (x q) = binErr aa dd Dm (q : ℕ) := by
      rw [hq]; exact hkey (q : ℕ)
    have hsum : occupation y x 0 (x q) + occupation y x 1 (x q) = x q := by
      have e := occupation_sum y hx.orderedTimes (x q)
      rw [Fin.sum_univ_two] at e
      rw [min_eq_left (hx.mem_Icc q).2, min_eq_right (hx.mem_Icc q).1, sub_zero] at e
      exact e
    have hsumW : occupation p τ 0 (x q) + occupation p τ 1 (x q) = x q := by
      have e := occupation_sum p hτ (x q)
      rw [Fin.sum_univ_two] at e
      rw [min_eq_left (hx.mem_Icc q).2, min_eq_right (hx.mem_Icc q).1, sub_zero] at e
      exact e
    have hbound := abs_le.mp (abs_binErr_le h0 h1 h2 hD (q : ℕ))
    rcases fin_two_cases i with hi | hi <;> subst hi <;> rw [abs_le] <;>
      constructor <;> linarith

/-! ## SC27: sharpness of the constant one half

On a single cell of length `L` the original schedule that occupies each mode for half the cell
is at distance at least `L / 2` from every grid schedule, whatever its block budget. Since the
mesh width of that grid is `L`, the constant `1 / 2` in `exists_isGridSchedule_binary` cannot
be replaced by any smaller one. -/

/-- The one-cell grid of length `L`. -/
theorem isGrid_oneCell {L : ℝ} (hL : 0 < L) : IsGrid ![(0 : ℝ), L] L := by
  refine ⟨rfl, rfl, ?_⟩
  refine Fin.strictMono_iff_lt_succ.mpr fun j => ?_
  fin_cases j
  simpa using hL

/-- The mesh width of the one-cell grid is its cell length. -/
theorem meshWidth_oneCell {L : ℝ} : meshWidth ![(0 : ℝ), L] = L := by
  simp [meshWidth, cellLength, ciSup_unique]

/-- The two-mode schedule that occupies each mode for half of a single cell of length `L`. -/
noncomputable def halfSchedule (L : ℝ) : Fin 2 → ℝ → ℝ :=
  occupation ![0, 1] ![0, L / 2, L]

/-- The half-and-half schedule uses two activation blocks, that is, one switch. -/
theorem isSchedule_halfSchedule {L : ℝ} (hL : 0 ≤ L) : IsSchedule 2 L (halfSchedule L) := by
  refine ⟨![0, 1], ![0, L / 2, L], ⟨rfl, by simp, ?_⟩, rfl⟩
  refine Fin.monotone_iff_le_succ.mpr fun j => ?_
  fin_cases j <;> simp <;> linarith

/-- At the end of the horizon the half-and-half schedule has occupied each mode for `L / 2`. -/
theorem halfSchedule_apply {L : ℝ} (hL : 0 ≤ L) (i : Fin 2) : halfSchedule L i L = L / 2 := by
  have h1 : min L (L / 2) = L / 2 := min_eq_right (by linarith)
  have h2 : min L (0 : ℝ) = 0 := min_eq_right hL
  have h3 : min L L = L := min_self L
  rcases fin_two_cases i with hi | hi <;> subst hi <;>
    simp only [halfSchedule, occupation, Fin.sum_univ_two] <;>
    norm_num [h1, h2, h3, Matrix.cons_val_two, Matrix.vecHead, Matrix.vecTail]
  all_goals ring

/-- On a one-cell grid every grid schedule is constant, so each mode is occupied either for
none or for all of the cell. -/
theorem gridSchedule_oneCell_eq {L : ℝ} (hL : 0 < L) {k : ℕ} {V : Fin 2 → ℝ → ℝ}
    (hV : IsGridSchedule ![(0 : ℝ), L] k V) : V 0 L = 0 ∨ V 0 L = L := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hV
  have hx := isGrid_oneCell hL
  have hu : OrderedTimes (![(0 : ℝ), L] ∘ g) L :=
    ⟨by simp [hg0], by simp [hgl], hx.strictMono.monotone.comp hg⟩
  set u : Fin (k + 1) → ℝ := ![(0 : ℝ), L] ∘ g with hudef
  have hval : ∀ m : Fin (k + 1), u m = 0 ∨ u m = L := by
    intro m
    rcases fin_two_cases (g m) with h | h <;> simp [hudef, h]
  have hblock : ∀ i : Fin 2, 0 < occupation p u i L →
      ∃ m : Fin k, p m = i ∧ u m.castSucc = 0 ∧ u m.succ = L := by
    intro i hpos
    have hpos' : 0 < occupation p u i L - occupation p u i 0 := by
      rw [occupation_zero hu]
      simpa using hpos
    obtain ⟨m, hpm, hlt1, hlt2⟩ := exists_blockIndex hu.mono hL.le hpos'
    refine ⟨m, hpm, ?_, ?_⟩
    · rcases hval m.castSucc with h | h
      · exact h
      · exact absurd hlt1 (by simp [h])
    · rcases hval m.succ with h | h
      · exact absurd hlt2 (by simp [h])
      · exact h
  by_contra hcon
  push Not at hcon
  obtain ⟨h0, hL0⟩ := hcon
  have hsum : occupation p u 0 L + occupation p u 1 L = L := by
    have e := occupation_sum p hu L
    rw [Fin.sum_univ_two, min_self, min_eq_right hL.le, sub_zero] at e
    exact e
  have hn0 : 0 ≤ occupation p u 0 L := occupation_nonneg hu.mono 0 L
  have hn1 : 0 ≤ occupation p u 1 L := occupation_nonneg hu.mono 1 L
  obtain ⟨m, hpm, hm1, hm2⟩ := hblock 0 (lt_of_le_of_ne hn0 (Ne.symm h0))
  obtain ⟨m', hpm', hm1', hm2'⟩ := hblock 1 (by
    rcases lt_or_eq_of_le hn1 with h | h
    · exact h
    · exact absurd (by linarith : occupation p u 0 L = L) hL0)
  have hne : m ≠ m' := by
    intro h
    rw [h, hpm'] at hpm
    exact absurd hpm (by decide)
  rcases lt_or_gt_of_ne hne with h | h
  · have : u m.succ ≤ u m'.castSucc :=
      hu.mono (Fin.le_def.mpr (by simpa using Fin.lt_def.mp h))
    rw [hm2, hm1'] at this
    linarith
  · have : u m'.succ ≤ u m.castSucc :=
      hu.mono (Fin.le_def.mpr (by simpa using Fin.lt_def.mp h))
    rw [hm2', hm1] at this
    linarith

/-- SC27, sharpness (`prop:binary-transfer`, last sentence): on a one-cell grid of length `L`
the half-and-half schedule is at distance at least `L / 2` from every grid schedule, so the
constant `1 / 2` of `exists_isGridSchedule_binary` is attained and cannot be lowered. -/
theorem binaryTransfer_sharp {L : ℝ} (hL : 0 < L) {k : ℕ} {V : Fin 2 → ℝ → ℝ}
    (hV : IsGridSchedule ![(0 : ℝ), L] k V) :
    meshWidth ![(0 : ℝ), L] / 2 ≤ D (halfSchedule L) V L := by
  have hx := isGrid_oneCell hL
  have hcum : IsCumulative (halfSchedule L) L :=
    (isSchedule_halfSchedule hL.le).isCumulative
  have hVcum : IsCumulative V L := (hV.isSchedule hx).isCumulative
  have hmem : (L : ℝ) ∈ Icc (0 : ℝ) L := ⟨hL.le, le_refl L⟩
  have hle := le_D hcum hVcum 0 hmem
  rw [halfSchedule_apply hL.le 0] at hle
  rw [meshWidth_oneCell]
  refine le_trans ?_ hle
  rcases gridSchedule_oneCell_eq hL hV with h | h <;> rw [h]
  · rw [sub_zero, abs_of_nonneg (by linarith)]
  · rw [abs_of_nonpos (by linarith)]
    linarith

end GridSwitching
