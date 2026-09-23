import Formal.GridSwitching.LinearPrograms

/-!
# SC16 and SC17: the two-large-modes family contributes exactly `H`

This module proves the two tier-2 obligations of `topics/17-grid-switching/CLAIMS.md` that
dispose of the two-large-modes family of `eq:grid-LP`: the family is bounded by the quantity
`H` of `eq:grid-H`, and that bound is attained by the explicit witness `eq:grid-H-witness`.

## Naming

The source writes `H` for the quantity of `eq:grid-H`, but `H_n(T)` elsewhere in the package
denotes the *continuous* one-switch minimax value. To avoid confusion this module calls the
grid quantity `gridH`, and the cutoff index `c = min {j : T / 3 <= t_j}` is `gridCutoff`. The
grid index just below a given one is `gridPred` (with `gridPred 0 = 0`; that degenerate case
never arises in the statements below, where the relevant index is positive).

## SC16: the family is bounded by `gridH`

Fix a two-large-modes feasible point with cell indices `ja jb`, so `B = x jb.succ` and
`Q = x jb.castSucc`. Following the source:

* `TwoLargeFeasible.four_mul_le` : `4 * E ≤ T + B`. At `B` both distinguished modes have
  allocation at most `B - E`. For mode `0` this is the constraint `v 0 + E ≤ B`. For mode `1`
  it is monotonicity of its deficit after `A`: the weighted state sums at `A` and `B` give
  `v 1 - u 1 ≤ B - A`, and `u 1 + E ≤ A`. The bulk modes hold at most
  `(n - 2) * m 2 = T - m 0 - m 1 ≤ T - 2 * E`, because `m 0` and `m 1` are both at least `E`.
  Adding the three bounds to `B = v 0 + v 1 + (n - 2) * v 2` gives `B ≤ 2 * (B - E) + T - 2 * E`.
* `TwoLargeFeasible.two_mul_le` : `2 * E ≤ T - Q`, from the upper cutoff `E + m 1 ≤ T - Q`
  at `B` together with `E ≤ m 1`.
* `TwoLargeFeasible.le_third_of_node_le` and `TwoLargeFeasible.le_third_of_le_prev` : each of
  the two bounds degenerates to `E ≤ T / 3` when `B ≤ T / 3`, respectively `T / 3 ≤ Q`.
* `TwoLargeFeasible.le_gridH` : when `jb.succ` is the cutoff index, the two bounds are exactly
  `E ≤ gridH x T (gridCutoff x T)`.
* `TwoLargeFeasible.le_max_third_gridH` : in all cases `E ≤ max (T / 3) (gridH x T c)`, by
  trichotomy of `jb.succ` against the cutoff index `c`. This is the form the final assembly
  needs, since it holds for every horizon.
* `TwoLargeFeasible.le_gridH_of_pos` : for `0 < T` the maximum can be dropped, because
  `T / 3 ≤ gridH x T c` there (`third_le_gridH_gridCutoff`). This is the statement of the
  source, "the entire family is bounded by `H`".

**Correction to the manuscript.** The source states the degenerate case with strict
inequalities, "if `B < T / 3` or `Q > T / 3`". Strict hypotheses do not cover the whole
complement of `jb.succ = c`: if `x c = T / 3` exactly and `jb.succ` is the successor of `c`,
then `Q = T / 3` is *not* `> T / 3`. The non-strict statements proved here (`B ≤ T / 3`,
respectively `T / 3 ≤ Q`) are what the two bounds actually give, they do cover that case, and
they still yield `E ≤ T / 3`, so the conclusion of the paragraph is correct as stated.

## SC17: attainment

`twoLargeFeasible_witness` verifies `eq:grid-H-witness` at `ja = jb = c` from the inequalities
the source lists, and nothing else: with `C = x jc.succ` and `E` arbitrary subject to
`T / 3 ≤ E`, `E ≤ C`, `4 * E ≤ T + C`, `T - C ≤ 2 * E ≤ T - x jc.castSucc`, `C ≤ T` and
`0 ≤ x jc.castSucc`, the point given by two identical modes of terminal mass `E` each, holding
`gridHSmall C T E = max 0 ((C - T + 2 * E) / 2)` at `C`, and `n - 2` bulk modes of terminal
mass `(T - 2 * E) / (n - 2)` each, holding `min C (T - 2 * E) / (n - 2)` at `C`, is
two-large-modes feasible. `twoLargeFeasible_gridH` instantiates this at the cutoff index, and
`gridH_le_gridF` concludes through `twoLarge_le_gridF` of `LinearPrograms`.

The four inequalities hold at the cutoff index by `third_le_gridH`, `gridH_le_node`,
`node_sub_le_two_mul_gridH` and the two defining bounds `gridH_le_quarter`, `gridH_le_half`.
The source's remark `E ≤ t_c ≤ 3 E` is `gridH_le_node` together with `node_le_three_mul_gridH`.
The condition `t_{c-1} ≤ E`, which the manuscript does not spell out, is `prev_node_le_gridH`:
minimality of `c` gives `x (c - 1) < T / 3 ≤ E`.

## Hypotheses added beyond the source

* `3 ≤ n`, as everywhere in this package: it makes the bulk weight `n - 2` positive.
* `IsGrid x T`, which replaces the source's implicit assumption on the grid data.
* `0 < T` in `exists_cell_succ_eq_gridCutoff` and `gridH_le_gridF`. The source never states it,
  but it is needed: for `T = 0` the cutoff index is `0`, no cell `jc` has `jc.succ = c`, and
  the witness of `eq:grid-H-witness` does not exist. Every SC16 bound holds without it.
-/

namespace GridSwitching

open Set

variable {n N : ℕ}

/-! ## The cutoff index and the quantity `gridH` -/

/-- The grid index just below `c`, with `0` its own predecessor. For a positive index this is
the node `t_{c-1}` of `eq:grid-H`. -/
def gridPred (c : Fin (N + 1)) : Fin (N + 1) :=
  ⟨(c : ℕ) - 1, lt_of_le_of_lt (Nat.sub_le _ _) c.isLt⟩

@[simp] theorem gridPred_val (c : Fin (N + 1)) : (gridPred c : ℕ) = (c : ℕ) - 1 := rfl

/-- The predecessor of the upper endpoint of a cell is its lower endpoint. -/
theorem gridPred_succ (j : Fin N) : gridPred j.succ = j.castSucc := Fin.ext (by simp)

/-- The quantity `H` of `eq:grid-H`, evaluated at a grid index `c`. It is called `gridH`
because `H_n(T)` denotes the *continuous* one-switch minimax value elsewhere in the package. -/
noncomputable def gridH (x : Fin (N + 1) → ℝ) (T : ℝ) (c : Fin (N + 1)) : ℝ :=
  min ((T + x c) / 4) ((T - x (gridPred c)) / 2)

/-- The first defining bound of `gridH`. -/
theorem gridH_le_quarter (x : Fin (N + 1) → ℝ) (T : ℝ) (c : Fin (N + 1)) :
    gridH x T c ≤ (T + x c) / 4 :=
  min_le_left _ _

/-- The second defining bound of `gridH`. -/
theorem gridH_le_half (x : Fin (N + 1) → ℝ) (T : ℝ) (c : Fin (N + 1)) :
    gridH x T c ≤ (T - x (gridPred c)) / 2 :=
  min_le_right _ _

variable {x : Fin (N + 1) → ℝ} {T : ℝ}

/-- The set of grid indices whose node is at or beyond `T / 3`, as a set of naturals. -/
private def cutoffSet (x : Fin (N + 1) → ℝ) (T : ℝ) : Set ℕ :=
  {k : ℕ | ∃ h : k < N + 1, T / 3 ≤ x ⟨k, h⟩}

/-- The last index is a cutoff candidate: `x (Fin.last N) = T` and `T / 3 ≤ T`. -/
private theorem last_mem_cutoffSet (hx : IsGrid x T) : N ∈ cutoffSet x T := by
  refine ⟨Nat.lt_succ_self N, ?_⟩
  have hlast : (⟨N, Nat.lt_succ_self N⟩ : Fin (N + 1)) = Fin.last N := rfl
  rw [hlast, hx.last]
  linarith [hx.horizon_nonneg]

/-- The cutoff index `c = min {j : T / 3 ≤ t_j}` of `eq:grid-H`. The truncation at `N` only
makes the definition total; on a grid it is inactive (`gridCutoff_val`). -/
noncomputable def gridCutoff (x : Fin (N + 1) → ℝ) (T : ℝ) : Fin (N + 1) :=
  ⟨min (sInf (cutoffSet x T)) N, Nat.lt_succ_of_le (min_le_right _ _)⟩

/-- On a grid the cutoff index is exactly the infimum of the cutoff set. -/
theorem gridCutoff_val (hx : IsGrid x T) :
    ((gridCutoff x T : Fin (N + 1)) : ℕ) = sInf (cutoffSet x T) :=
  min_eq_left (Nat.sInf_le (last_mem_cutoffSet hx))

/-- The cutoff index is well defined: its node is at or beyond `T / 3`. -/
theorem third_le_gridCutoff_node (hx : IsGrid x T) : T / 3 ≤ x (gridCutoff x T) := by
  obtain ⟨h, hle⟩ := Nat.sInf_mem (⟨N, last_mem_cutoffSet hx⟩ : (cutoffSet x T).Nonempty)
  have hc : gridCutoff x T = ⟨sInf (cutoffSet x T), h⟩ := Fin.ext (gridCutoff_val hx)
  rw [hc]
  exact hle

/-- Minimality of the cutoff index: every strictly earlier node is below `T / 3`. -/
theorem node_lt_third_of_lt_gridCutoff (hx : IsGrid x T) {j : Fin (N + 1)}
    (hj : (j : ℕ) < (gridCutoff x T : ℕ)) : x j < T / 3 := by
  by_contra hcon
  have hmem : (j : ℕ) ∈ cutoffSet x T := ⟨j.isLt, by rw [Fin.eta]; exact not_lt.mp hcon⟩
  exact Nat.notMem_of_lt_sInf (by rwa [gridCutoff_val hx] at hj) hmem

/-- On a positive horizon the cutoff index is positive, since `x 0 = 0 < T / 3`. -/
theorem gridCutoff_pos (hx : IsGrid x T) (hT : 0 < T) : 0 < (gridCutoff x T : ℕ) := by
  rcases Nat.eq_zero_or_pos (gridCutoff x T : ℕ) with h | h
  · exfalso
    have hz : gridCutoff x T = (0 : Fin (N + 1)) := Fin.ext (by simpa using h)
    have hspec := third_le_gridCutoff_node hx
    rw [hz, hx.first] at hspec
    linarith
  · exact h

/-- On a positive horizon the cutoff index is the upper endpoint of a grid cell. -/
theorem exists_cell_succ_eq_gridCutoff (hx : IsGrid x T) (hT : 0 < T) :
    ∃ jc : Fin N, jc.succ = gridCutoff x T := by
  have hpos := gridCutoff_pos hx hT
  have hlt := (gridCutoff x T).isLt
  refine ⟨⟨(gridCutoff x T : ℕ) - 1, by omega⟩, Fin.ext ?_⟩
  simp only [Fin.val_succ]
  omega

/-! ### The inequalities behind the witness

All of these hold at any index `c` whose node is at or beyond `T / 3` and whose predecessor
node is strictly below `T / 3`; the cutoff index is such an index. -/

/-- `gridH` is at least the floor `T / 3`. -/
theorem third_le_gridH {c : Fin (N + 1)} (hc : T / 3 ≤ x c) (hp : x (gridPred c) < T / 3) :
    T / 3 ≤ gridH x T c :=
  le_min (by linarith) (by linarith)

/-- `gridH` is at most the node `t_c`: the lower half of the source's remark
`E ≤ t_c ≤ 3 E`. -/
theorem gridH_le_node {c : Fin (N + 1)} (hc : T / 3 ≤ x c) : gridH x T c ≤ x c :=
  (gridH_le_quarter x T c).trans (by linarith)

/-- The node `t_c` is at most `3 * gridH`: the upper half of the source's remark
`E ≤ t_c ≤ 3 E`. -/
theorem node_le_three_mul_gridH (hx : IsGrid x T) {c : Fin (N + 1)}
    (hp : x (gridPred c) < T / 3) : x c ≤ 3 * gridH x T c := by
  have hCT := (hx.mem_Icc c).2
  have hT0 := hx.horizon_nonneg
  have h : x c / 3 ≤ gridH x T c := le_min (by linarith) (by linarith)
  linarith

/-- The predecessor node is at most `gridH`: the condition `t_{c-1} ≤ E` that the manuscript
leaves implicit. It follows from minimality of the cutoff index. -/
theorem prev_node_le_gridH {c : Fin (N + 1)} (hc : T / 3 ≤ x c) (hp : x (gridPred c) < T / 3) :
    x (gridPred c) ≤ gridH x T c :=
  hp.le.trans (third_le_gridH hc hp)

/-- The remaining inequality of the source's list, `T - t_c ≤ 2 E`. -/
theorem node_sub_le_two_mul_gridH {c : Fin (N + 1)} (hc : T / 3 ≤ x c)
    (hp : x (gridPred c) < T / 3) : T - x c ≤ 2 * gridH x T c := by
  have h := third_le_gridH hc hp
  linarith

/-- At the cutoff index of a positive horizon, `gridH` is at least the floor `T / 3`. The
predecessor node is then a genuine earlier node, so minimality of the cutoff index applies. -/
theorem third_le_gridH_gridCutoff (hx : IsGrid x T) (hT : 0 < T) :
    T / 3 ≤ gridH x T (gridCutoff x T) := by
  refine third_le_gridH (third_le_gridCutoff_node hx) (node_lt_third_of_lt_gridCutoff hx ?_)
  have hpos := gridCutoff_pos hx hT
  rw [gridPred_val]
  omega

/-! ## SC16: the two-large-modes family is bounded by `gridH` -/

variable {ja jb : Fin N} {u v m : Fin 3 → ℝ} {E : ℝ}

/-- SC16, first bound: `4 E ≤ T + B`. At `B` both distinguished modes have allocation at most
`B - E`, and the bulk modes hold at most `T - 2 E` in total. -/
theorem TwoLargeFeasible.four_mul_le (hn : 3 ≤ n)
    (hf : TwoLargeFeasible n x T ja jb u v m E) : 4 * E ≤ T + x jb.succ := by
  have hc := hf.common
  have hw : (0 : ℝ) ≤ (n : ℝ) - 2 := by
    have h3 : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  have hu := hc.weighted_u
  have hv := hc.weighted_v
  have hm := hc.weighted_m
  rw [lpWeighted_eq] at hu hv hm
  have huv2 : ((n : ℝ) - 2) * u 2 ≤ ((n : ℝ) - 2) * v 2 :=
    mul_le_mul_of_nonneg_left (hc.u_le_v 2) hw
  have hvm2 : ((n : ℝ) - 2) * v 2 ≤ ((n : ℝ) - 2) * m 2 :=
    mul_le_mul_of_nonneg_left (hc.v_le_m 2) hw
  have hE1 := hf.E_le_m_one
  have hE0 : E ≤ m 0 := hE1.trans hc.m_one_le_m_zero
  have h0 := hc.u_le_v 0
  have hda := hc.deficit_a
  have hdb := hc.deficit_b
  linarith

/-- SC16, second bound: `2 E ≤ T - Q`, from the upper cutoff at `B` and `E ≤ m 1`. -/
theorem TwoLargeFeasible.two_mul_le (hf : TwoLargeFeasible n x T ja jb u v m E) :
    2 * E ≤ T - x jb.castSucc := by
  have h := hf.common.cutoff_b_upper
  have h1 := hf.E_le_m_one
  linarith

/-- SC16: a feasible point whose node `B` is at or below `T / 3` has value at most `T / 3`. -/
theorem TwoLargeFeasible.le_third_of_node_le (hn : 3 ≤ n)
    (hf : TwoLargeFeasible n x T ja jb u v m E) (hB : x jb.succ ≤ T / 3) : E ≤ T / 3 := by
  have h := hf.four_mul_le hn
  linarith

/-- SC16: a feasible point whose node `Q` is at or beyond `T / 3` has value at most
`T / 3`. -/
theorem TwoLargeFeasible.le_third_of_le_prev (hf : TwoLargeFeasible n x T ja jb u v m E)
    (hQ : T / 3 ≤ x jb.castSucc) : E ≤ T / 3 := by
  have h := hf.two_mul_le
  linarith

/-- SC16, the clean bound at the cutoff index: if `B` is the cutoff node then the two bounds
are exactly `E ≤ gridH`. -/
theorem TwoLargeFeasible.le_gridH (hn : 3 ≤ n) (hf : TwoLargeFeasible n x T ja jb u v m E)
    (hb : jb.succ = gridCutoff x T) : E ≤ gridH x T (gridCutoff x T) := by
  have h4 := hf.four_mul_le hn
  have h2 := hf.two_mul_le
  rw [gridH, ← hb, gridPred_succ]
  exact le_min (by linarith) (by linarith)

/-- SC16, in the form used by the final assembly: every two-large-modes feasible value is at
most `max (T / 3) (gridH x T c)` for the cutoff index `c`. -/
theorem TwoLargeFeasible.le_max_third_gridH (hn : 3 ≤ n) (hx : IsGrid x T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) :
    E ≤ max (T / 3) (gridH x T (gridCutoff x T)) := by
  rcases lt_trichotomy ((jb.succ : Fin (N + 1)) : ℕ) ((gridCutoff x T : Fin (N + 1)) : ℕ) with
    h | h | h
  · exact le_max_of_le_left
      (hf.le_third_of_node_le hn (node_lt_third_of_lt_gridCutoff hx h).le)
  · exact le_max_of_le_right (hf.le_gridH hn (Fin.ext h))
  · refine le_max_of_le_left (hf.le_third_of_le_prev ?_)
    refine (third_le_gridCutoff_node hx).trans (hx.strictMono.monotone ?_)
    simp only [Fin.val_succ] at h
    rw [Fin.le_def, Fin.val_castSucc]
    omega

/-- SC16 in the form the source states it: on a positive horizon the entire two-large-modes
family is bounded by `gridH`, because the floor `T / 3` is itself at most `gridH` at the cutoff
index. -/
theorem TwoLargeFeasible.le_gridH_of_pos (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T)
    (hf : TwoLargeFeasible n x T ja jb u v m E) : E ≤ gridH x T (gridCutoff x T) :=
  (hf.le_max_third_gridH hn hx).trans (max_le (third_le_gridH_gridCutoff hx hT) le_rfl)

/-! ## SC17: attainment of `gridH`

The witness of `eq:grid-H-witness`: two identical modes of terminal mass `E`, each holding
`gridHSmall C T E` at the node `C`, and `n - 2` identical bulk modes of terminal mass
`(T - 2 E) / (n - 2)`, each holding `min C (T - 2 E) / (n - 2)` at `C`. Component `2` of the
state vectors describes one bulk mode, as everywhere in `eq:grid-LP`. -/

/-- The common allocation `x = max {0, (C - T + 2E)/2}` of `eq:grid-H-witness` that each of
the two large modes holds at the node `C`. -/
noncomputable def gridHSmall (C T E : ℝ) : ℝ := max 0 ((C - T + 2 * E) / 2)

/-- The endpoint state vector of `eq:grid-H-witness` at the node `C`. -/
noncomputable def gridHState (n : ℕ) (C T E : ℝ) : Fin 3 → ℝ := fun j =>
  if (j : ℕ) < 2 then gridHSmall C T E else min C (T - 2 * E) / ((n : ℝ) - 2)

/-- The terminal mass vector of `eq:grid-H-witness`. -/
noncomputable def gridHMass (n : ℕ) (T E : ℝ) : Fin 3 → ℝ := fun j =>
  if (j : ℕ) < 2 then E else (T - 2 * E) / ((n : ℝ) - 2)

@[simp] theorem gridHState_zero (n : ℕ) (C T E : ℝ) :
    gridHState n C T E 0 = gridHSmall C T E := rfl

@[simp] theorem gridHState_one (n : ℕ) (C T E : ℝ) :
    gridHState n C T E 1 = gridHSmall C T E := rfl

@[simp] theorem gridHState_two (n : ℕ) (C T E : ℝ) :
    gridHState n C T E 2 = min C (T - 2 * E) / ((n : ℝ) - 2) := rfl

@[simp] theorem gridHMass_zero (n : ℕ) (T E : ℝ) : gridHMass n T E 0 = E := rfl

@[simp] theorem gridHMass_one (n : ℕ) (T E : ℝ) : gridHMass n T E 1 = E := rfl

@[simp] theorem gridHMass_two (n : ℕ) (T E : ℝ) :
    gridHMass n T E 2 = (T - 2 * E) / ((n : ℝ) - 2) := rfl

/-- SC17, the feasibility computation: the witness of `eq:grid-H-witness` at `a = b` is
two-large-modes feasible as soon as the inequalities the source lists hold. No property of the
grid beyond `0 ≤ Q` and `C ≤ T` is used. -/
theorem twoLargeFeasible_witness (hn : 3 ≤ n) {jc : Fin N} {C : ℝ}
    (hC : x jc.succ = C) (h3E : T / 3 ≤ E) (hEC : E ≤ C) (h4 : 4 * E ≤ T + C)
    (hTC : T - C ≤ 2 * E) (h2P : 2 * E ≤ T - x jc.castSucc) (hP0 : 0 ≤ x jc.castSucc)
    (hCT : C ≤ T) :
    TwoLargeFeasible n x T jc jc (gridHState n C T E) (gridHState n C T E)
      (gridHMass n T E) E := by
  have hk : (0 : ℝ) < (n : ℝ) - 2 := by
    have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  have hkne : ((n : ℝ) - 2) ≠ 0 := ne_of_gt hk
  have hdiv : ∀ a : ℝ, ((n : ℝ) - 2) * (a / ((n : ℝ) - 2)) = a := by
    intro a
    field_simp
  have hE0 : 0 ≤ E := by linarith
  have hC0 : 0 ≤ C := by linarith
  have hT2E : 0 ≤ T - 2 * E := by linarith
  have hnE : T ≤ (n : ℝ) * E := by
    have h3n : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    nlinarith
  have hsmall : gridHSmall C T E ≤ C - E := max_le (by linarith) (by linarith)
  have hsmallE : gridHSmall C T E ≤ E := max_le hE0 (by linarith)
  have hsmall0 : 0 ≤ gridHSmall C T E := le_max_left _ _
  have hstate : lpWeighted n (gridHState n C T E) = C := by
    rw [lpWeighted_eq, gridHState_zero, gridHState_one, gridHState_two]
    rcases le_total C (T - 2 * E) with h | h
    · have hz : gridHSmall C T E = 0 := max_eq_left (by linarith)
      rw [min_eq_left h, hdiv, hz]
      ring
    · have hz : gridHSmall C T E = (C - T + 2 * E) / 2 :=
        max_eq_right (by linarith)
      rw [min_eq_right h, hdiv, hz]
      ring
  have hmassw : lpWeighted n (gridHMass n T E) = T := by
    rw [lpWeighted_eq, gridHMass_zero, gridHMass_one, gridHMass_two, hdiv]
    ring
  refine ⟨{ u_nonneg := ?_, u_le_v := fun _ => le_rfl, v_le_m := ?_,
            m_one_le_m_zero := le_rfl, m_two_le_m_one := ?_, horizon_third_le := h3E,
            weighted_u := ?_, weighted_v := ?_, weighted_m := hmassw,
            cutoff_a_lower := ?_, cutoff_a_upper := ?_, cutoff_b_lower := ?_,
            cutoff_b_upper := ?_, deficit_a := ?_, deficit_b := ?_ }, le_rfl⟩
  · intro j
    simp only [gridHState]
    split_ifs
    · exact hsmall0
    · exact div_nonneg (le_min hC0 hT2E) hk.le
  · intro j
    simp only [gridHState, gridHMass]
    split_ifs
    · exact hsmallE
    · gcongr
      exact min_le_right _ _
  · rw [gridHMass_one, gridHMass_two, div_le_iff₀ hk]
    linarith
  · rw [hC]
    exact hstate
  · rw [hC]
    exact hstate
  · rw [hC, gridHMass_zero]
    exact hTC.trans (by linarith)
  · rw [gridHMass_zero]
    linarith
  · rw [hC, gridHMass_one]
    exact hTC.trans (by linarith)
  · rw [gridHMass_one]
    linarith
  · rw [hC, gridHState_one]
    linarith
  · rw [hC, gridHState_zero]
    linarith

/-- SC17: the witness of `eq:grid-H-witness` at the cutoff index is two-large-modes feasible
with value `gridH`. -/
theorem twoLargeFeasible_gridH (hn : 3 ≤ n) (hx : IsGrid x T) {jc : Fin N}
    (hjc : jc.succ = gridCutoff x T) :
    TwoLargeFeasible n x T jc jc
      (gridHState n (x jc.succ) T (gridH x T jc.succ))
      (gridHState n (x jc.succ) T (gridH x T jc.succ))
      (gridHMass n T (gridH x T jc.succ)) (gridH x T jc.succ) := by
  have hcnode : T / 3 ≤ x jc.succ := by
    rw [hjc]
    exact third_le_gridCutoff_node hx
  have hprev : x (gridPred jc.succ) < T / 3 := by
    rw [gridPred_succ]
    refine node_lt_third_of_lt_gridCutoff hx ?_
    rw [← hjc, Fin.val_castSucc, Fin.val_succ]
    omega
  have hquarter := gridH_le_quarter x T jc.succ
  have hhalf := gridH_le_half x T jc.succ
  rw [gridPred_succ] at hhalf
  refine twoLargeFeasible_witness hn rfl (third_le_gridH hcnode hprev)
    (gridH_le_node hcnode) (by linarith) (node_sub_le_two_mul_gridH hcnode hprev)
    (by linarith) (hx.mem_Icc _).1 (hx.mem_Icc _).2

/-- SC17: on a grid with positive horizon, `gridH` is a lower bound for the one-switch grid
minimax value. Together with SC16 this says the two-large-modes family contributes exactly
`gridH`. -/
theorem gridH_le_gridF (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    gridH x T (gridCutoff x T) ≤ gridF x n 1 T := by
  obtain ⟨jc, hjc⟩ := exists_cell_succ_eq_gridCutoff hx hT
  have h := twoLarge_le_gridF hn hx (twoLargeFeasible_gridH hn hx hjc)
  rwa [hjc] at h

end GridSwitching
