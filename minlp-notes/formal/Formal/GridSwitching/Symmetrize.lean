import Formal.GridSwitching.Elimination
import Formal.GridSwitching.LinearPrograms

/-!
# SC18: symmetrization to one distinguished mode, and the bridge to SC19

This module discharges obligation SC18 of `topics/17-grid-switching/CLAIMS.md` and connects it
to SC19. It is the bridge between the two halves of `thm:finite-one` that are already proved
separately:

* `Formal.GridSwitching.LinearPrograms` provides the all-initial-modes family
  `AllInitialFeasible` of `eq:grid-LP` and its sufficiency `allInitial_le_gridF`;
* `Formal.GridSwitching.Elimination` provides the purely algebraic predicate `StateOK` and the
  two equivalences `exists_state_iff` and `elimination_iff`, with no reference to the linear
  programs at all.

## The correspondence

The symmetrized configuration of the source's paragraph "Write `M = m_1`, `x = A_1(A)`,
`y = A_1(B)`" is *exactly* `StateOK`. With one distinguished mode of terminal mass `M` holding
`X` at `A` and `Y` at `B`, and `n - 1` identical modes holding `(A - X)/(n - 1)`,
`(B - Y)/(n - 1)` and `(T - M)/(n - 1)`, every constraint of `eq:grid-LP` becomes a conjunct of
`StateOK`:

* the failure constraint `X ≥ (n-1)E - (n-2)A` is the averaged initial deficit
  `A - (A - X)/(n-1) ≥ E`, that is, the constraints `u 1 + E ≤ A` and `u 2 + E ≤ A`;
* `Y ≤ B - E` is the distinguished mode's initial deficit at `B`, that is, `v 0 + E ≤ B`;
* the four cutoffs `T - A ≤ E + M ≤ T - P` and `T - B ≤ E + (T-M)/(n-1) ≤ T - Q` are the
  cutoffs at `A` and at `B` for `m 0 = M` and `m 1 = (T - M)/(n - 1)`;
* `T/n ≤ M` is `m 1 ≤ m 0`, the statement that the distinguished mode carries the largest mass;
* the six monotonicity inequalities of `StateOK` are the componentwise monotonicity of the
  three symmetrized vectors, the bulk ones after clearing the positive factor `n - 1`.

The correspondence is exact in both directions, with a single addition: `StateOK` does not
record `T/3 ≤ E`, which `LPCommon.horizon_third_le` demands. That is the only hypothesis the
converse `allInitialFeasible_symmState` needs beyond `StateOK` and `3 ≤ n`; it is not a defect
of the source, which carries `E ≥ T/3` throughout.

## The cell index genuinely moves

The forward direction `exists_stateOK_of_allInitialFeasible` produces a possibly *new* cell
`jb'`, as the source says ("with a possibly new `b ≥ a`"), and the move is real, not an
artefact of the proof. The symmetrized common terminal mass is
`(T - m 0)/(n - 1) = (m 1 + (n-2) * m 2)/(n - 1)`, which is at most `m 1`, so the lower cutoff
`T - B ≤ E + m 1` at the old cell need not survive as `T - B ≤ E + (T - m 0)/(n - 1)`; the
first eligible final time moves weakly later.

`cellMove_feasible_and_not_stateOK` is a verified four-mode instance where it moves
strictly: on the grid `0 < 1/5 < 7/5 < 3/2 < 3` with `T = 3` and `E = T/3 = 1`, the point
`u = (1/2, 2/5, 1/4)`, `v = (1/2, 1/2, 1/4)`, `m = (9/5, 3/5, 3/10)` at the cells `(1/5, 7/5)`
and `(7/5, 3/2)` is all-initial-modes feasible, while its symmetrized common mass
`(T - m 0)/3 = 2/5` is strictly below `m 1 = 3/5` and makes `T - B ≤ E + 2/5`, that is
`3/2 ≤ 7/5`, fail. So `jb' = jb` is *not* always available and the statement proved below is
the correct one. The failure is a property of the symmetrized configuration, in which the
distinguished mass is pinned to `M = m 0`; in that same instance `StateOK` at the old pair is
nonempty for other values of `M`.

The new cell is the first cell at or after `jb` whose right node reaches `T - E - (T-M)/(n-1)`;
it exists because the last node is the horizon. Its left node gives the upper cutoff either by
minimality (when the cell moved) or from `E + (T-M)/(n-1) ≤ E + M ≤ T - P` (when it did not).
Taking the first cell at or after `jb` rather than at or after `ja` matters: the cell that is
first at or after `ja` can be *earlier* than `jb`, and then the state `Y` built below would be
attached to a node smaller than `B`.

## Contents

* `symmState`, `lpWeighted_symmState`: the symmetrized vector and its weighted total.
* `exists_stateOK_of_allInitialFeasible` (**SC18**): every all-initial-modes feasible point
  yields, at the cell `ja` and a weakly later cell `jb'`, a `StateOK` instance, with the three
  preservation claims of the source proved as stated.
* `allInitialFeasible_symmState`: the converse bridge, a `StateOK` instance together with
  `T/3 ≤ E` is an all-initial-modes feasible point.
* `cellMoveGrid`, `cellMoveU`, `cellMoveV`, `cellMoveM`, `isGrid_cellMoveGrid` and
  `cellMove_feasible_and_not_stateOK`: the four-mode instance certifying that the final cell
  must be allowed to move.
* `exists_admissible_of_allInitialFeasible` and `exists_allInitialFeasible_of_admissible`, the
  two consequences the final assembly needs, and the packaged form `le_gridF_of_admissible`.

## Hypotheses

`3 ≤ n` and `IsGrid x T` are stated where used, as in the two imported modules. The forward
direction needs the grid only to know that the last node is the horizon, that the nodes are
ordered, and that `0 < x ja.succ` (so `0 < T`); the converse needs no property of the grid at
all beyond `3 ≤ n` and `T/3 ≤ E`.
-/

namespace GridSwitching

variable {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} {ja jb : Fin N} {u v m : Fin 3 → ℝ} {E : ℝ}

/-! ## The symmetrized state vector -/

/-- The symmetrized state vector: the distinguished mode carries `X` and each of the other
`n - 1` modes carries the average `(S - X) / (n - 1)`. The two endpoint states (`S = A` and
`S = B`) and the terminal masses (`S = T`) all have this shape, so one definition serves for
all three. Component `2` describes one bulk mode, as everywhere in `eq:grid-LP`. -/
noncomputable def symmState (n : ℕ) (S X : ℝ) : Fin 3 → ℝ := fun j =>
  if (j : ℕ) = 0 then X else (S - X) / ((n : ℝ) - 1)

@[simp] theorem symmState_zero (n : ℕ) (S X : ℝ) : symmState n S X 0 = X := rfl

@[simp] theorem symmState_one (n : ℕ) (S X : ℝ) :
    symmState n S X 1 = (S - X) / ((n : ℝ) - 1) := rfl

@[simp] theorem symmState_two (n : ℕ) (S X : ℝ) :
    symmState n S X 2 = (S - X) / ((n : ℝ) - 1) := rfl

/-- The weights `(1, 1, n - 2)` of `eq:grid-LP` recover the total: the distinguished mode and
the `n - 1` averaged modes together carry `S`. -/
theorem lpWeighted_symmState (hn : 3 ≤ n) (S X : ℝ) : lpWeighted n (symmState n S X) = S := by
  have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hne : ((n : ℝ) - 1) ≠ 0 := ne_of_gt (by linarith)
  have key : ((n : ℝ) - 1) * ((S - X) / ((n : ℝ) - 1)) = S - X := by field_simp
  rw [lpWeighted_eq, symmState_zero, symmState_one, symmState_two]
  linarith [key]

/-! ## The converse bridge: a symmetrized state is a feasible point -/

/-- **The converse bridge.** A `StateOK` instance at the cells `ja` and `jb`, together with the
objective bound `T/3 ≤ E` that `StateOK` does not record, is an all-initial-modes feasible
point of `eq:grid-LP`: the three symmetrized vectors `symmState` verify every field of
`LPCommon` and the extra field `deficit_a_bulk`.

No property of the grid is used: the statement is a pure computation with the four numbers
`x ja.succ`, `x jb.succ`, `x ja.castSucc`, `x jb.castSucc`. -/
theorem allInitialFeasible_symmState (hn : 3 ≤ n) (h3E : T / 3 ≤ E) {X Y M : ℝ}
    (hs : StateOK (n : ℝ) T (x ja.succ) (x jb.succ) (x ja.castSucc) (x jb.castSucc) E X Y M) :
    AllInitialFeasible n x T ja jb (symmState n (x ja.succ) X) (symmState n (x jb.succ) Y)
      (symmState n T M) E := by
  obtain ⟨hX0, hXY, hYM, hAX, hAXBY, hBYTM, hfail, hdefb, hca, hcb, hcc, hcd, hmass⟩ := hs
  have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hnu1 : (0 : ℝ) < (n : ℝ) - 1 := by linarith
  have hnu0 : (0 : ℝ) < (n : ℝ) := by linarith
  -- dividing by the positive factor `n - 1` is monotone
  have hdiv : ∀ a b : ℝ, a ≤ b → a / ((n : ℝ) - 1) ≤ b / ((n : ℝ) - 1) := by
    intro a b hab
    have h := div_nonneg (sub_nonneg.mpr hab) hnu1.le
    rw [sub_div] at h
    linarith
  -- the averaged initial deficit at `A`
  have hdefa : (x ja.succ - X) / ((n : ℝ) - 1) + E ≤ x ja.succ := by
    have h : (x ja.succ - X) / ((n : ℝ) - 1) ≤ x ja.succ - E := by
      rw [div_le_iff₀ hnu1]
      linarith
    linarith
  -- the symmetrized masses are ordered
  have hmassle : (T - M) / ((n : ℝ) - 1) ≤ M := by
    rw [div_le_iff₀ hnu1]
    rw [div_le_iff₀ hnu0] at hmass
    linarith
  refine ⟨{ u_nonneg := ?_, u_le_v := ?_, v_le_m := ?_, m_one_le_m_zero := ?_,
            m_two_le_m_one := le_rfl, horizon_third_le := h3E,
            weighted_u := lpWeighted_symmState hn _ _,
            weighted_v := lpWeighted_symmState hn _ _,
            weighted_m := lpWeighted_symmState hn _ _,
            cutoff_a_lower := ?_, cutoff_a_upper := ?_, cutoff_b_lower := ?_,
            cutoff_b_upper := ?_, deficit_a := ?_, deficit_b := ?_ }, ?_⟩
  · intro j
    simp only [symmState]
    split_ifs
    · exact hX0
    · exact div_nonneg (by linarith) hnu1.le
  · intro j
    simp only [symmState]
    split_ifs
    · exact hXY
    · exact hdiv _ _ (by linarith)
  · intro j
    simp only [symmState]
    split_ifs
    · exact hYM
    · exact hdiv _ _ (by linarith)
  · rw [symmState_zero, symmState_one]
    exact hmassle
  · rw [symmState_zero]
    exact hca
  · rw [symmState_zero]
    exact hcb
  · rw [symmState_one]
    exact hcc
  · rw [symmState_one]
    exact hcd
  · rw [symmState_one]
    exact hdefa
  · rw [symmState_zero]
    linarith
  · rw [symmState_two]
    exact hdefa

/-! ## SC18: symmetrization -/

/-- The first cell at or after `jb` whose right node reaches the level `c`. Such a cell exists
because the last node is the horizon. Minimality of the cell bounds its left node strictly
below `c`, except in the case where the cell is `jb` itself. -/
private theorem exists_cell_ge (hx : IsGrid x T) (jb : Fin N) {c : ℝ} (hc : c ≤ T) :
    ∃ jb' : Fin N, (jb : ℕ) ≤ (jb' : ℕ) ∧ c ≤ x jb'.succ ∧
      ((jb' : ℕ) = (jb : ℕ) ∨ x jb'.castSucc < c) := by
  classical
  have hjbN : (jb : ℕ) < N := jb.isLt
  have hex : ∃ k : ℕ, ∃ h : k < N, (jb : ℕ) ≤ k ∧ c ≤ x (⟨k, h⟩ : Fin N).succ := by
    refine ⟨N - 1, by omega, by omega, ?_⟩
    have hsucc : (⟨N - 1, by omega⟩ : Fin N).succ = Fin.last N := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_last]
      omega
    rw [hsucc, hx.last]
    exact hc
  obtain ⟨hlt, hge, hle⟩ := Nat.find_spec hex
  refine ⟨⟨Nat.find hex, hlt⟩, hge, hle, ?_⟩
  rcases Nat.eq_or_lt_of_le hge with heq | hgt
  · exact Or.inl heq.symm
  · refine Or.inr ?_
    have hmin := Nat.find_min hex (m := Nat.find hex - 1) (by omega)
    have hpred : Nat.find hex - 1 < N := by omega
    have hno : ¬ c ≤ x (⟨Nat.find hex - 1, hpred⟩ : Fin N).succ := fun hcon =>
      hmin ⟨hpred, by omega, hcon⟩
    have hcell : (⟨Nat.find hex - 1, hpred⟩ : Fin N).succ
        = (⟨Nat.find hex, hlt⟩ : Fin N).castSucc := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    rw [hcell] at hno
    exact not_le.mp hno

/-- **SC18, symmetrization to one distinguished mode.** Every all-initial-modes feasible point
of `eq:grid-LP` symmetrizes to a state of the form described by `StateOK`, at the same initial
cell `ja` and at a weakly later final cell `jb'`.

The distinguished mode is the one of largest terminal mass, so `M = m 0`, `X = u 0` and the
state at the new node is `Y = max (v 0) (B' - T + M)`. The three preservation claims of the
source are the three nontrivial verifications:

* the averaged initial deficit at `t_a` still exceeds `E`, because
  `A - u 0 = u 1 + (n-2) * u 2` is an average of `n - 1` quantities each at most `A - E`, by
  `deficit_a` and `deficit_a_bulk`;
* the common terminal mass `(T - m 0)/(n - 1)` is at most the old `m 1`, so the first eligible
  final time moves weakly later, which is why `jb'` may differ from `jb`;
* the distinguished mode's initial deficit is nondecreasing, so `Y ≤ B' - E` still holds at the
  later node; this is what the `max` records, its second branch being forced by the terminal
  monotonicity `B' - Y ≤ T - M`. -/
theorem exists_stateOK_of_allInitialFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) :
    ∃ jb' : Fin N, (ja : ℕ) ≤ (jb' : ℕ) ∧ (jb : ℕ) ≤ (jb' : ℕ) ∧
      StateOK (n : ℝ) T (x ja.succ) (x jb'.succ) (x ja.castSucc) (x jb'.castSucc) E
        (u 0) (max (v 0) (x jb'.succ - T + m 0)) (m 0) := by
  have hc := hf.common
  have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hnu0 : (0 : ℝ) < (n : ℝ) := by linarith
  have hnu1 : (0 : ℝ) < (n : ℝ) - 1 := by linarith
  have hnu2 : (0 : ℝ) ≤ (n : ℝ) - 2 := by linarith
  -- the three weighted identities, written out
  have hsu : u 0 + u 1 + ((n : ℝ) - 2) * u 2 = x ja.succ := by
    rw [← lpWeighted_eq]; exact hc.weighted_u
  have hsv : v 0 + v 1 + ((n : ℝ) - 2) * v 2 = x jb.succ := by
    rw [← lpWeighted_eq]; exact hc.weighted_v
  have hsm : m 0 + m 1 + ((n : ℝ) - 2) * m 2 = T := by
    rw [← lpWeighted_eq]; exact hc.weighted_m
  have hu1 := hc.u_nonneg 1
  have hu2 := hc.u_nonneg 2
  have huv1 := hc.u_le_v 1
  have huv2 := hc.u_le_v 2
  have hvm0 := hc.v_le_m 0
  have hvm1 := hc.v_le_m 1
  have hvm2 := hc.v_le_m 2
  have hm2 : (0 : ℝ) ≤ m 2 := ((hc.u_nonneg 2).trans huv2).trans hvm2
  have hm10 := hc.m_one_le_m_zero
  have hm21 := hc.m_two_le_m_one
  -- the distinguished mode carries the largest mass
  have hbulk : ((n : ℝ) - 2) * m 2 ≤ ((n : ℝ) - 2) * m 0 :=
    mul_le_mul_of_nonneg_left (hm21.trans hm10) hnu2
  have hexp : ((n : ℝ) - 2) * m 0 = (n : ℝ) * m 0 - 2 * m 0 := by ring
  have hTle : T ≤ (n : ℝ) * m 0 := by linarith
  have hmassM : T / (n : ℝ) ≤ m 0 := by
    rw [div_le_iff₀ hnu0]
    linarith [mul_comm ((n : ℝ)) (m 0)]
  -- the symmetrized common terminal mass
  have hTM : T - m 0 = m 1 + ((n : ℝ) - 2) * m 2 := by linarith
  have hbulk1 : ((n : ℝ) - 2) * m 2 ≤ ((n : ℝ) - 2) * m 1 :=
    mul_le_mul_of_nonneg_left hm21 hnu2
  have hexp1 : ((n : ℝ) - 2) * m 1 = (n : ℝ) * m 1 - 2 * m 1 := by ring
  have havg_le_m1 : (T - m 0) / ((n : ℝ) - 1) ≤ m 1 := by
    rw [div_le_iff₀ hnu1]
    have : m 1 * ((n : ℝ) - 1) = (n : ℝ) * m 1 - m 1 := by ring
    linarith
  have havg_le_M : (T - m 0) / ((n : ℝ) - 1) ≤ m 0 := by
    rw [div_le_iff₀ hnu1]
    have : m 0 * ((n : ℝ) - 1) = (n : ℝ) * m 0 - m 0 := by ring
    linarith
  have havg_nonneg : (0 : ℝ) ≤ (T - m 0) / ((n : ℝ) - 1) := by
    refine div_nonneg ?_ hnu1.le
    have := mul_nonneg hnu2 hm2
    have hm1 : (0 : ℝ) ≤ m 1 := ((hc.u_nonneg 1).trans huv1).trans hvm1
    linarith
  -- the horizon is positive, hence so is the objective
  have hApos : 0 < x ja.succ := hx.zero_lt_succ ja
  have hAB : x ja.succ ≤ x jb.succ := hc.node_le hn
  have hBT : x jb.succ ≤ T := hc.node_le_horizon hn
  have hTpos : 0 < T := lt_of_lt_of_le hApos (hAB.trans hBT)
  have hE3 := hc.horizon_third_le
  have hEpos : 0 < E := lt_of_lt_of_le (by linarith) hE3
  -- the new final cell
  obtain ⟨jb', hjbb', hlevel, hcase⟩ :=
    exists_cell_ge hx jb (c := T - E - (T - m 0) / ((n : ℝ) - 1)) (by linarith)
  have hjab' : (ja : ℕ) ≤ (jb' : ℕ) := le_trans (hc.index_le hn hx) hjbb'
  have hBB' : x jb.succ ≤ x jb'.succ := by
    refine hx.strictMono.monotone ?_
    rw [Fin.le_def]
    simp only [Fin.val_succ]
    omega
  have hB'T : x jb'.succ ≤ T := by
    have h := hx.strictMono.monotone (Fin.le_last jb'.succ)
    rwa [hx.last] at h
  have hP0 : (0 : ℝ) ≤ x ja.castSucc := by
    have h := hx.strictMono.monotone (Fin.zero_le ja.castSucc)
    rwa [hx.first] at h
  -- the three preservation claims
  have hAu : x ja.succ - u 0 = u 1 + ((n : ℝ) - 2) * u 2 := by linarith
  have hdefa := hc.deficit_a
  have hdefbulk := hf.deficit_a_bulk
  have hfail : ((n : ℝ) - 1) * E - ((n : ℝ) - 2) * x ja.succ ≤ u 0 := by
    have hb : ((n : ℝ) - 2) * u 2 ≤ ((n : ℝ) - 2) * (x ja.succ - E) :=
      mul_le_mul_of_nonneg_left (by linarith) hnu2
    have hring : ((n : ℝ) - 2) * (x ja.succ - E)
        = (n : ℝ) * x ja.succ - 2 * x ja.succ - (n : ℝ) * E + 2 * E := by ring
    have hring2 : ((n : ℝ) - 1) * E - ((n : ℝ) - 2) * x ja.succ
        = (n : ℝ) * E - E - (n : ℝ) * x ja.succ + 2 * x ja.succ := by ring
    linarith
  have hATM : x ja.succ - u 0 ≤ T - m 0 := by
    have hb : ((n : ℝ) - 2) * u 2 ≤ ((n : ℝ) - 2) * m 2 :=
      mul_le_mul_of_nonneg_left (huv2.trans hvm2) hnu2
    linarith [huv1.trans hvm1]
  have hAB' : x ja.succ - u 0 ≤ x jb.succ - v 0 := by
    have hb : ((n : ℝ) - 2) * u 2 ≤ ((n : ℝ) - 2) * v 2 :=
      mul_le_mul_of_nonneg_left huv2 hnu2
    linarith
  have hEM : E + m 0 ≤ T := le_trans hc.cutoff_a_upper (by linarith)
  refine ⟨jb', hjab', hjbb', hc.u_nonneg 0, ?_, ?_, ?_, ?_, ?_, hfail, ?_,
    hc.cutoff_a_lower, hc.cutoff_a_upper, by linarith, ?_, hmassM⟩
  · exact le_trans (hc.u_le_v 0) (le_max_left _ _)
  · exact max_le hvm0 (by linarith)
  · linarith [mul_nonneg hnu2 hu2]
  · have h : max (v 0) (x jb'.succ - T + m 0) ≤ x jb'.succ - (x ja.succ - u 0) :=
      max_le (by linarith) (by linarith)
    linarith
  · linarith [le_max_right (v 0) (x jb'.succ - T + m 0)]
  · exact max_le (by linarith [hc.deficit_b]) (by linarith)
  · rcases hcase with heq | hstrict
    · have hcell : jb' = jb := Fin.ext heq
      subst hcell
      linarith [hc.cutoff_b_upper]
    · linarith

/-! ## The new cell is genuinely new

The statement above cannot be simplified by taking `jb' = jb`. The witness is a four-mode
example on the grid `0 < 1/5 < 7/5 < 3/2 < 3` of horizon `T = 3`, with `E = T/3 = 1`, the
initial cell `(1/5, 7/5)` and the final cell `(7/5, 3/2)`. -/

/-- The grid `0 < 1/5 < 7/5 < 3/2 < 3` of the counterexample. -/
noncomputable def cellMoveGrid : Fin 5 → ℝ := ![0, 1/5, 7/5, 3/2, 3]

/-- The counterexample grid is a grid on the horizon `3`. -/
theorem isGrid_cellMoveGrid : IsGrid cellMoveGrid 3 where
  first := rfl
  last := rfl
  strictMono := by
    rw [Fin.strictMono_iff_lt_succ]
    intro i
    fin_cases i
    · change (0 : ℝ) < 1/5
      norm_num
    · change (1/5 : ℝ) < 7/5
      norm_num
    · change (7/5 : ℝ) < 3/2
      norm_num
    · change (3/2 : ℝ) < 3
      norm_num

/-- The state at the initial node of the counterexample. -/
noncomputable def cellMoveU : Fin 3 → ℝ := ![1/2, 2/5, 1/4]

/-- The state at the final node of the counterexample. -/
noncomputable def cellMoveV : Fin 3 → ℝ := ![1/2, 1/2, 1/4]

/-- The terminal masses of the counterexample. -/
noncomputable def cellMoveM : Fin 3 → ℝ := ![9/5, 3/5, 3/10]

/-- **The final cell genuinely moves.** The four-mode point above is all-initial-modes
feasible, yet its symmetrization admits *no* state at the original pair of cells: the
symmetrized common terminal mass is `(T - m 0)/(n - 1) = 2/5`, strictly below `m 1 = 3/5`, so
the lower cutoff `T - B ≤ E + (T - m 0)/(n - 1)` reads `3/2 ≤ 7/5` and fails, whatever the two
endpoint states are.

So `exists_stateOK_of_allInitialFeasible` must be allowed to move the final cell, exactly as
the source's "with a possibly new `b ≥ a`" says; here `jb' = 3`, with `B' = 3` and
`Q' = 3/2`, and the upper cutoff `E + 2/5 = 7/5 ≤ 3 - 3/2` holds there. The failure is a
property of the *symmetrized* configuration, in which the distinguished mass is fixed to
`M = m 0`: `StateOK` at the original pair is not empty for other values of `M`. -/
theorem cellMove_feasible_and_not_stateOK :
    AllInitialFeasible 4 cellMoveGrid 3 (1 : Fin 4) (2 : Fin 4) cellMoveU cellMoveV cellMoveM 1 ∧
      ∀ X Y : ℝ, ¬ StateOK ((4 : ℕ) : ℝ) 3
        (cellMoveGrid (1 : Fin 4).succ) (cellMoveGrid (2 : Fin 4).succ)
        (cellMoveGrid (1 : Fin 4).castSucc) (cellMoveGrid (2 : Fin 4).castSucc)
        1 X Y (cellMoveM 0) := by
  constructor
  · refine ⟨{ u_nonneg := ?_, u_le_v := ?_, v_le_m := ?_, m_one_le_m_zero := ?_,
              m_two_le_m_one := ?_, horizon_third_le := ?_, weighted_u := ?_, weighted_v := ?_,
              weighted_m := ?_, cutoff_a_lower := ?_, cutoff_a_upper := ?_,
              cutoff_b_lower := ?_, cutoff_b_upper := ?_, deficit_a := ?_,
              deficit_b := ?_ }, ?_⟩
    · intro j
      fin_cases j <;> norm_num [cellMoveU]
    · intro j
      fin_cases j <;> norm_num [cellMoveU, cellMoveV]
    · intro j
      fin_cases j <;> norm_num [cellMoveV, cellMoveM]
    · change (3/5 : ℝ) ≤ 9/5
      norm_num
    · change (3/10 : ℝ) ≤ 3/5
      norm_num
    · norm_num
    · rw [lpWeighted_eq]
      change (1/2 : ℝ) + 2/5 + ((4 : ℕ) - 2) * (1/4) = 7/5
      norm_num
    · rw [lpWeighted_eq]
      change (1/2 : ℝ) + 1/2 + ((4 : ℕ) - 2) * (1/4) = 3/2
      norm_num
    · rw [lpWeighted_eq]
      change (9/5 : ℝ) + 3/5 + ((4 : ℕ) - 2) * (3/10) = 3
      norm_num
    · change (3 : ℝ) - 7/5 ≤ 1 + 9/5
      norm_num
    · change (1 : ℝ) + 9/5 ≤ 3 - 1/5
      norm_num
    · change (3 : ℝ) - 3/2 ≤ 1 + 3/5
      norm_num
    · change (1 : ℝ) + 3/5 ≤ 3 - 7/5
      norm_num
    · change (2/5 : ℝ) + 1 ≤ 7/5
      norm_num
    · change (1/2 : ℝ) + 1 ≤ 3/2
      norm_num
    · change (1/4 : ℝ) + 1 ≤ 7/5
      norm_num
  · rintro X Y ⟨-, -, -, -, -, -, -, -, -, -, hcut, -, -⟩
    have h : (3 : ℝ) - 3/2 ≤ 1 + (3 - 9/5) / (((4 : ℕ) : ℝ) - 1) := hcut
    norm_num at h

/-! ## The two consequences of the final assembly -/

/-- **The first consequence.** An all-initial-modes feasible point at the cells `ja`, `jb`
yields a weakly later cell `jb'` at which the pair `(ja, jb')` is admissible in the sense of
`eq:grid-admissible` and the objective lies between the two endpoints `L_ab` and `U_ab` of
`eq:grid-L` and `eq:grid-U`.

The bound `T/3 ≤ E` is not an extra hypothesis: it is the field `LPCommon.horizon_third_le`. -/
theorem exists_admissible_of_allInitialFeasible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : AllInitialFeasible n x T ja jb u v m E) :
    ∃ jb' : Fin N, (ja : ℕ) ≤ (jb' : ℕ) ∧
      Admissible (n : ℝ) T (x ja.succ) (x jb'.succ) ∧
      L (n : ℝ) T (x ja.succ) (x jb'.succ) ≤ E ∧
      E ≤ U (n : ℝ) T (x ja.succ) (x jb'.succ) (x ja.castSucc) (x jb'.castSucc) := by
  obtain ⟨jb', hjab', -, hs⟩ := exists_stateOK_of_allInitialFeasible hn hx hf
  have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hP0 : (0 : ℝ) ≤ x ja.castSucc := by
    have h := hx.strictMono.monotone (Fin.zero_le ja.castSucc)
    rwa [hx.first] at h
  have hPA : x ja.castSucc ≤ x ja.succ :=
    hx.strictMono.monotone (Fin.castSucc_lt_succ (i := ja)).le
  have hQB : x jb'.castSucc ≤ x jb'.succ :=
    hx.strictMono.monotone (Fin.castSucc_lt_succ (i := jb')).le
  have hAB' : x ja.succ ≤ x jb'.succ := by
    refine hx.strictMono.monotone ?_
    rw [Fin.le_def]
    simp only [Fin.val_succ]
    omega
  have hB'T : x jb'.succ ≤ T := by
    have h := hx.strictMono.monotone (Fin.le_last jb'.succ)
    rwa [hx.last] at h
  obtain ⟨hEA, hE2, hMne⟩ :=
    (exists_state_iff h3n hP0 hPA hAB' hB'T (x jb'.castSucc) E).1 ⟨_, _, _, hs⟩
  obtain ⟨hadm, hL, hU⟩ :=
    (elimination_iff h3n hPA hQB T E).1 ⟨hMne, hf.common.horizon_third_le, hEA, hE2⟩
  exact ⟨jb', hjab', hadm, hL, hU⟩

/-- **The second consequence.** Conversely, an admissible pair of cells whose endpoints bracket
the objective carries an all-initial-modes feasible point, namely the symmetrized one. -/
theorem exists_allInitialFeasible_of_admissible (hn : 3 ≤ n) (hx : IsGrid x T)
    (hab : (ja : ℕ) ≤ (jb : ℕ)) (hadm : Admissible (n : ℝ) T (x ja.succ) (x jb.succ))
    (hL : L (n : ℝ) T (x ja.succ) (x jb.succ) ≤ E)
    (hU : E ≤ U (n : ℝ) T (x ja.succ) (x jb.succ) (x ja.castSucc) (x jb.castSucc)) :
    ∃ uS vS mS : Fin 3 → ℝ, AllInitialFeasible n x T ja jb uS vS mS E := by
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
  exact ⟨_, _, _, allInitialFeasible_symmState hn h3E hs⟩

/-- **The second consequence, packaged.** An admissible pair of cells whose endpoints bracket
the objective certifies that value as a lower bound for the grid one-switch minimax value.

This is the composition of `exists_allInitialFeasible_of_admissible` with the sufficiency half
`allInitial_le_gridF` of SC12. -/
theorem le_gridF_of_admissible (hn : 3 ≤ n) (hx : IsGrid x T) (hab : (ja : ℕ) ≤ (jb : ℕ))
    (hadm : Admissible (n : ℝ) T (x ja.succ) (x jb.succ))
    (hL : L (n : ℝ) T (x ja.succ) (x jb.succ) ≤ E)
    (hU : E ≤ U (n : ℝ) T (x ja.succ) (x jb.succ) (x ja.castSucc) (x jb.castSucc)) :
    E ≤ gridF x n 1 T := by
  obtain ⟨uS, vS, mS, hfeas⟩ :=
    exists_allInitialFeasible_of_admissible hn hx hab hadm hL hU
  exact allInitial_le_gridF hn hx hfeas

end GridSwitching
