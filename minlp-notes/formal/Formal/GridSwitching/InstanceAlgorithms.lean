import Formal.GridSwitching.ThreeMode

/-!
# SC33, SC34 and SC35: exact one-switch algorithms for a supplied input

This module discharges the tier-4 obligations SC33, SC34 and SC35 of
`topics/17-grid-switching/CLAIMS.md`, which are `thm:linear-one-switch`, the unimodality
paragraph following it, and `lem:final-residual` of
`paper-switching-control/sections/10-instance-algorithms.tex`.

## SC33: three candidate pairs per boundary (`thm:linear-one-switch`)

Fix a boundary time `t` on the horizon, a mode `h₁` of largest terminal mass, a mode `h₂` of
largest terminal mass among the modes other than `h₁`, and a mode `pt` maximizing `A_i(t)`
among the modes outside `{h₁, h₂}`. Then the three ordered pairs `(h₁, h₂)`, `(h₂, h₁)` and
`(pt, h₁)` dominate every ordered pair of distinct modes:

* `candidateError_le_switchError` is the pointwise dominance, and
  `inf'_distinctPairs_eq_inf'_candidatePairs` is the resulting equality of the minimum over
  *all* ordered pairs of distinct modes with the minimum over the candidate set.
* `min_switchError_le_switchError_two` is the case `n = 2`, where the first two pairs
  already suffice; `inf'_distinctPairs_eq_inf'_candidatePairs_two`,
  `isLeast_permittedErrorSet_two` and `gridOPT_one_eq_permittedCandidateValue_two` are its
  counterparts to the three general results below. They are needed as separate statements:
  the general results require a boundary leader `pt` with `pt ≠ h₁` and `pt ≠ h₂`, which is
  unsatisfiable when `n = 2`, so at `n = 2` the general statements are vacuous while the
  source's algorithmic sentence still applies. The two-candidate set is the general one with
  `pt := h₂`, since `candidateError A T t h₁ h₂ h₂` is the minimum of the first two
  candidates (`candidateError_self`).
* `exists_massLeaders` (needs `1 < n`) and `exists_boundaryLeader` (needs `3 ≤ n`) supply
  the leaders; the dominance theorems take them as hypotheses, so they apply to any
  consistent tie-breaking.

The **structural** content of the complexity claim is `candidatePairs_card_le`: the
candidate set has at most three elements, a bound independent of the mode count `n`, while
the set of competitors it replaces has `n(n-1)` elements. `CLAIMS.md` excludes machine-level
cost models, so **no arithmetic-operation count is claimed anywhere in this module**; in
particular the source's `O(nN)` and `O(n log(N+1))` counts are not formalized.

The algorithmic consequence is stated for an arbitrary `Finset` of permitted grid nodes,
the empty one included:

* `isLeast_permittedErrorSet`: the best constant schedule compared with the three candidates
  at every permitted boundary is the exact optimum of the permitted at-most-one-switch
  problem. `D_constSchedule` identifies the best constant schedule: its error is `T - m_r`,
  so a largest-mass mode is optimal among constant schedules.
* `gridOPT_one_eq_permittedCandidateValue`: with every grid node permitted this computed
  value *is* the grid one-switch instance optimum `gridOPT x A T 1`.
* `isLeast_prescribedErrorSet`: the variant with a prescribed initial mode `p`, where only
  the constant schedule of `p` and the single pair `p → q_p` at each permitted boundary are
  compared.

Degenerate boundaries are permitted, as everywhere in this package: `oneSwitch p q 0 T` and
`oneSwitch p q T T` have a zero-length block and are nominally still the word `(p, q)`. In
the prescribed-initial-mode variant this means the boundary `t = 0` contributes the constant
schedule of `q_p`, whose *nominal* word starts with `p` but whose initial block is empty.

## SC34: the unimodality refinement

For a **fixed** ordered pair `(p, q)` the two varying terms of `eq:one-switch-error` are
`L_p(t) = t - A_p(t)` (`initialDeficit`, nondecreasing by `initialDeficit_mono`, proved
upstream) and `R_q(t) = T - m_q - t` (`finalDeficit`).

* `sub_le_deficitGap_sub`: the increase of `L_p - R_q` between `u < v` is at least `v - u`,
  which is the source's own reason for strictness;
* `deficitGap_strictMonoOn`: hence `L_p - R_q` is strictly increasing on `[0, T]`, so it
  changes sign at most once;
* `maxDeficit_le_of_le_crossing` and `maxDeficit_le_of_crossing_le`: `max(L_p, R_q)` is
  nonincreasing before the crossing and nondecreasing after it;
* `adjacentBoundaries` selects the last permitted boundary at or before the crossing and the
  first one at or after it, `adjacentBoundaries_card_le` bounds that set by two elements,
  and `inf'_maxDeficit_adjacentBoundaries` and `inf'_switchError_adjacentBoundaries` are the
  reduction: minimizing over all permitted boundaries and minimizing over those at most two
  gives the same value. When the crossing lies outside the permitted range one of the two
  sides is empty and the definition returns the first, respectively last, permitted
  boundary, exactly as the source describes.

Permitted boundaries are here an arbitrary `Finset ℝ` contained in the horizon, which covers
an arbitrary set of grid nodes.

**Scope caveat, stated because it is easy to misread.** This reduction holds for a *fixed*
ordered pair `(p, q)`; that is the setting of the source's paragraph, which opens with "For
a fixed initial mode `p` and its final choice `q_p`". It does **not** apply to SC33's
three-candidate set as such, because the third candidate `(p_t, h₁)` has an initial mode
`p_t` that depends on the boundary `t`, so both its omitted-mass term and its initial
deficit vary with `t` in a way the two monotonicity lemmas above do not cover. Nothing in
this module claims otherwise.

**This casts no doubt on the source's procedure.** The `O(n log(N+1))` algorithm of the
source is the union over the `n` possible initial modes `p` of the per-pair reduction, each
with its own best final mode `q_p`; every ordered pair of distinct modes is dominated by
some `(p, q_p)` by `D_oneSwitch_le_of_max_mass`, so that union does solve the whole
at-most-one-switch problem, and each of its `n` per-pair searches is exactly the reduction
proved here. The caveat concerns only the *three-candidate* presentation, not the source's
algorithm.

## SC35: the best completion of a fixed prefix (`lem:final-residual`)

See the section comment below for the statement, for the treatment of negative residuals,
and for the source's own limitation, which is preserved: the lemma optimizes the last block
after a fixed prefix and supplies **no greedy rule for choosing that prefix**.

## Hypotheses added beyond the sources

* `IsCumulative A T` wherever the source writes "the input"; this is the package's standing
  hypothesis and is what makes `A_p` nondecreasing and `1`-Lipschitz.
* `1 < n`, `3 ≤ n` are stated explicitly where the source's `n ≥ 3` (or its implicit
  assumption that a second, respectively third, mode exists) is used. The dominance results
  themselves take the leaders as hypotheses and so need no cardinality assumption.
* In SC35 the prefix discrepancy `E₀` is the **exact** prefix error `D A W u`, that is the
  supremum of `|A_i - W_i|` over *all* of `[0, u]`. Neither weakening of this reading keeps
  `eq:final-residual` an equality, and they fail in opposite directions.

  An arbitrary **upper bound** `E₀ > D A W u` breaks the `≥` direction, simply because an
  over-estimate inflates the maximum: the completion's error is still bounded by the true
  maximum, so the right-hand side is strictly larger than the left. (The `≤` direction
  survives, and that is what `D_completion_le` proves for an arbitrary `c`.)

  Reading `E₀` as the discrepancy at the single **endpoint** `u` instead breaks the `≤`
  direction, because a larger discrepancy earlier in the prefix is then not counted. With
  two modes, `T = 4`, `u = 3`, input `A i t = t / 2`, and the prefix that runs mode `0` on
  `[0, 2]` and mode `1` on `[2, 3]`, the discrepancy at `u = 3` is `1 / 2` in both modes,
  whereas the prefix error is `1`, attained at `t = 2` where `W_0(2) = 2` and `A_0(2) = 1`.
  The residuals are `r_0 = 0` and `r_1 = 1`, so completing in mode `1` would get the value
  `max{1/2, 0, 0} = 1/2` under the endpoint reading, while its actual error is `1`. With
  `E₀ = D A W u = 1` the formula gives `max{1, 0, 0} = 1`, correctly. This witness is
  formalized: `endpointWitnessA`, `endpointWitnessW` and `endpointWitness_lt_D_completion`
  prove that the endpoint-reading right-hand side is strictly below the completion's error.
* The `1`-Lipschitz bound on `A_j` is load-bearing in SC35 and is used twice, in the
  `i = j` branch of `D_completion_le`: it is what absorbs a negative final term
  `T - u - r_j < 0`, which the source's "this argument is unaffected by negative residuals"
  passes over. Monotonicity of `A` alone does not suffice. This is **not** a missing
  hypothesis of the source: inside `IsCumulative` the `lipschitz` field is derivable from
  `mono` together with `conservation`, so the bound is already implicit in "the input is a
  cumulative allocation". A formal proof merely has to make that step explicit.
* `IsCumulative W u` for the prefix schedule: only monotonicity, the Lipschitz bound,
  `W_i(0) = 0` and the conservation identity `∑ i, W_i(u) = u` are used, so the prefix need
  not be a schedule with finitely many blocks. `u ≤ T` is assumed but `u < T` is not needed.
-/

namespace GridSwitching

open Set

variable {n N : ℕ}

/-! ## Mode leaders -/

/-- Two mass leaders exist as soon as there are two modes. -/
theorem exists_massLeaders (hn : 1 < n) (A : Fin n → ℝ → ℝ) (T : ℝ) :
    ∃ h₁ h₂ : Fin n, h₁ ≠ h₂ ∧ (∀ i, masses A T i ≤ masses A T h₁) ∧
      ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂ := by
  have hne : (Finset.univ : Finset (Fin n)).Nonempty := ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
  obtain ⟨h₁, -, hmax₁⟩ := Finset.exists_max_image Finset.univ (masses A T) hne
  have hne₂ : (Finset.univ.erase h₁).Nonempty := by
    rw [← Finset.card_pos, Finset.card_erase_of_mem (Finset.mem_univ h₁)]
    simp only [Finset.card_univ, Fintype.card_fin]
    omega
  obtain ⟨h₂, hh₂, hmax₂⟩ := Finset.exists_max_image _ (masses A T) hne₂
  exact ⟨h₁, h₂, Ne.symm (Finset.mem_erase.mp hh₂).1,
    fun i => hmax₁ i (Finset.mem_univ i),
    fun i hi => hmax₂ i (Finset.mem_erase.mpr ⟨hi, Finset.mem_univ i⟩)⟩

/-- A boundary leader exists as soon as there are three modes. -/
theorem exists_boundaryLeader (hn : 3 ≤ n) {h₁ h₂ : Fin n} (h₁₂ : h₁ ≠ h₂)
    (A : Fin n → ℝ → ℝ) (t : ℝ) :
    ∃ p : Fin n, p ≠ h₁ ∧ p ≠ h₂ ∧ ∀ i, i ≠ h₁ → i ≠ h₂ → A i t ≤ A p t := by
  have hne : ((Finset.univ.erase h₁).erase h₂).Nonempty := by
    rw [← Finset.card_pos, Finset.card_erase_of_mem
      (Finset.mem_erase.mpr ⟨Ne.symm h₁₂, Finset.mem_univ h₂⟩),
      Finset.card_erase_of_mem (Finset.mem_univ h₁)]
    simp only [Finset.card_univ, Fintype.card_fin]
    omega
  obtain ⟨p, hp, hmax⟩ := Finset.exists_max_image _ (fun i => A i t) hne
  rw [Finset.mem_erase, Finset.mem_erase] at hp
  exact ⟨p, hp.2.1, hp.1,
    fun i hi₁ hi₂ => hmax i (Finset.mem_erase.mpr ⟨hi₂, Finset.mem_erase.mpr ⟨hi₁,
      Finset.mem_univ i⟩⟩)⟩

/-! ## SC33: three candidate pairs per boundary -/

/-- The error of the one-switch schedule that runs `p` on `[0, t]` and `q` on `[t, T]`. -/
noncomputable def switchError (A : Fin n → ℝ → ℝ) (T t : ℝ) (p q : Fin n) : ℝ :=
  D A (oneSwitch p q t T) T

/-- The best of the three candidates of `thm:linear-one-switch` at the boundary `t`. -/
noncomputable def candidateError (A : Fin n → ℝ → ℝ) (T t : ℝ) (h₁ h₂ pt : Fin n) : ℝ :=
  min (switchError A T t h₁ h₂) (min (switchError A T t h₂ h₁) (switchError A T t pt h₁))

/-- For an initial mode outside `{h₁, h₂}` and the final mode `h₁`, the omitted maximum of
`eq:one-switch-error` is the second largest terminal mass `m_{h₂}`. -/
theorem omittedMass_eq_second {A : Fin n → ℝ → ℝ} {T : ℝ} {h₁ h₂ p : Fin n}
    (hA : IsCumulative A T) (hT : 0 ≤ T)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (hp₂ : p ≠ h₂) (h₁₂ : h₁ ≠ h₂) :
    omittedMass A T p h₁ = masses A T h₂ := by
  refine le_antisymm (omittedMass_le ?_ fun i _ hi₁ => hmax₂ i hi₁)
    (masses_le_omittedMass (Ne.symm hp₂) (Ne.symm h₁₂))
  exact hA.nonneg h₂ ⟨hT, le_rfl⟩

/-- Among the initial modes outside `{h₁, h₂}`, with final mode `h₁`, only the cumulative
value `A_p(t)` varies, so a maximizer of `A_p(t)` is an optimal initial mode. -/
theorem switchError_le_of_cumulative_le {A : Fin n → ℝ → ℝ} {T t : ℝ} {h₁ h₂ p p' : Fin n}
    (hA : IsCumulative A T) (ht : t ∈ Icc (0 : ℝ) T)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) (hp₁ : p ≠ h₁)
    (hp₂ : p ≠ h₂) (hp'₁ : p' ≠ h₁) (hp'₂ : p' ≠ h₂) (hle : A p t ≤ A p' t) :
    switchError A T t p' h₁ ≤ switchError A T t p h₁ := by
  have hT : (0 : ℝ) ≤ T := ht.1.trans ht.2
  simp only [switchError, D_oneSwitch hA hp'₁ ht.1 ht.2, D_oneSwitch hA hp₁ ht.1 ht.2,
    omittedMass_eq_second hA hT hmax₂ hp₂ h₁₂, omittedMass_eq_second hA hT hmax₂ hp'₂ h₁₂]
  refine max_le_max le_rfl (max_le_max ?_ le_rfl)
  simp only [initialDeficit]
  linarith

/-- SC33 for `n ≥ 3`: at a fixed boundary `t` the three candidate pairs `(h₁, h₂)`,
`(h₂, h₁)` and `(p_t, h₁)` dominate every ordered pair of distinct modes. -/
theorem candidateError_le_switchError {A : Fin n → ℝ → ℝ} {T t : ℝ} {h₁ h₂ pt p q : Fin n}
    (hA : IsCumulative A T) (ht : t ∈ Icc (0 : ℝ) T)
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) (hpt₁ : pt ≠ h₁)
    (hpt₂ : pt ≠ h₂) (hptmax : ∀ i, i ≠ h₁ → i ≠ h₂ → A i t ≤ A pt t) (hpq : p ≠ q) :
    candidateError A T t h₁ h₂ pt ≤ switchError A T t p q := by
  simp only [candidateError]
  rcases oneSwitch_reduction hA hmax₁ hmax₂ h₁₂ hpq ht.1 ht.2 with h | ⟨hp₁, h⟩
  · exact (min_le_left _ _).trans h
  · by_cases hp₂ : p = h₂
    · subst hp₂
      exact ((min_le_right _ _).trans (min_le_left _ _)).trans h
    · refine ((min_le_right _ _).trans (min_le_right _ _)).trans (le_trans ?_ h)
      exact switchError_le_of_cumulative_le hA ht hmax₂ h₁₂ hp₁ hp₂ hpt₁ hpt₂
        (hptmax p hp₁ hp₂)

/-- With two modes, a mode distinct from `h₁` is `h₂`. -/
private theorem eq_of_ne_two : ∀ p h₁ h₂ : Fin 2, p ≠ h₁ → h₂ ≠ h₁ → p = h₂ := by decide

/-- SC33 for `n = 2`: the two candidate pairs `(h₁, h₂)` and `(h₂, h₁)` already dominate
every ordered pair of distinct modes. -/
theorem min_switchError_le_switchError_two {A : Fin n → ℝ → ℝ} {T t : ℝ} {h₁ h₂ p q : Fin n}
    (hn : n = 2) (hA : IsCumulative A T) (ht : t ∈ Icc (0 : ℝ) T)
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) (hpq : p ≠ q) :
    min (switchError A T t h₁ h₂) (switchError A T t h₂ h₁) ≤ switchError A T t p q := by
  subst hn
  rcases oneSwitch_reduction hA hmax₁ hmax₂ h₁₂ hpq ht.1 ht.2 with h | ⟨hp₁, h⟩
  · exact (min_le_left _ _).trans h
  · rw [eq_of_ne_two p h₁ h₂ hp₁ (Ne.symm h₁₂)] at h ⊢
    exact (min_le_right _ _).trans h

/-- Taking the boundary leader to be `h₂` collapses the three-candidate minimum to the
two-candidate minimum of the case `n = 2`. -/
theorem candidateError_self (A : Fin n → ℝ → ℝ) (T t : ℝ) (h₁ h₂ : Fin n) :
    candidateError A T t h₁ h₂ h₂ =
      min (switchError A T t h₁ h₂) (switchError A T t h₂ h₁) := by
  rw [candidateError, min_self]

/-! ### The candidate set as a finite set of pairs

The structural content of `thm:linear-one-switch` is that the minimum over the *continuum*
of ordered pairs of distinct modes -- a set whose size grows like `n²` -- equals the minimum
over a candidate set of at most **three** pairs, a bound independent of `n`. No
arithmetic-operation count is claimed here; `CLAIMS.md` excludes machine-level cost models. -/

/-- All ordered pairs of distinct modes. -/
def distinctPairs (n : ℕ) : Finset (Fin n × Fin n) :=
  Finset.univ.filter fun z => z.1 ≠ z.2

@[simp] theorem mem_distinctPairs {z : Fin n × Fin n} : z ∈ distinctPairs n ↔ z.1 ≠ z.2 := by
  simp [distinctPairs]

/-- With at least two modes there is an ordered pair of distinct modes. -/
theorem distinctPairs_nonempty (hn : 1 < n) : (distinctPairs n).Nonempty := by
  have hcard : 1 < Fintype.card (Fin n) := by simpa using hn
  obtain ⟨b, hb⟩ := Fintype.exists_ne_of_one_lt_card hcard ⟨0, by omega⟩
  exact ⟨(b, ⟨0, by omega⟩), mem_distinctPairs.mpr hb⟩

/-- The three candidate pairs of `thm:linear-one-switch` at a fixed boundary. -/
def candidatePairs (h₁ h₂ pt : Fin n) : Finset (Fin n × Fin n) :=
  {(h₁, h₂), (h₂, h₁), (pt, h₁)}

/-- The candidate set is never empty. -/
theorem candidatePairs_nonempty (h₁ h₂ pt : Fin n) : (candidatePairs h₁ h₂ pt).Nonempty :=
  ⟨(h₁, h₂), by simp [candidatePairs]⟩

/-- **The structural content of SC33**: the candidate set has at most three elements,
independently of the mode count `n`. -/
theorem candidatePairs_card_le (h₁ h₂ pt : Fin n) : (candidatePairs h₁ h₂ pt).card ≤ 3 := by
  refine (Finset.card_insert_le _ _).trans ?_
  have h : ({(h₂, h₁), (pt, h₁)} : Finset (Fin n × Fin n)).card ≤ 2 :=
    (Finset.card_insert_le _ _).trans (by simp)
  omega

/-- Each candidate pair consists of two distinct modes. -/
theorem candidatePairs_subset {h₁ h₂ pt : Fin n} (h₁₂ : h₁ ≠ h₂) (hpt₁ : pt ≠ h₁) :
    candidatePairs h₁ h₂ pt ⊆ distinctPairs n := by
  intro z hz
  simp only [candidatePairs, Finset.mem_insert, Finset.mem_singleton] at hz
  rcases hz with rfl | rfl | rfl
  · exact mem_distinctPairs.mpr h₁₂
  · exact mem_distinctPairs.mpr (Ne.symm h₁₂)
  · exact mem_distinctPairs.mpr hpt₁

/-- The minimum over the candidate set is the three-way minimum `candidateError`. -/
theorem inf'_candidatePairs {A : Fin n → ℝ → ℝ} {T t : ℝ} (h₁ h₂ pt : Fin n) :
    (candidatePairs h₁ h₂ pt).inf' (candidatePairs_nonempty h₁ h₂ pt)
        (fun z => switchError A T t z.1 z.2) = candidateError A T t h₁ h₂ pt := by
  simp [candidatePairs, candidateError, Finset.inf'_insert, Finset.inf'_singleton]

/-- **SC33, the exact reduction**: at a fixed boundary the minimum of the one-switch error
over *all* ordered pairs of distinct modes equals the minimum over the three candidate
pairs. -/
theorem inf'_distinctPairs_eq_inf'_candidatePairs {A : Fin n → ℝ → ℝ} {T t : ℝ}
    {h₁ h₂ pt : Fin n} (hn : 1 < n) (hA : IsCumulative A T) (ht : t ∈ Icc (0 : ℝ) T)
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) (hpt₁ : pt ≠ h₁)
    (hpt₂ : pt ≠ h₂) (hptmax : ∀ i, i ≠ h₁ → i ≠ h₂ → A i t ≤ A pt t) :
    (distinctPairs n).inf' (distinctPairs_nonempty hn) (fun z => switchError A T t z.1 z.2) =
      (candidatePairs h₁ h₂ pt).inf' (candidatePairs_nonempty h₁ h₂ pt)
        (fun z => switchError A T t z.1 z.2) := by
  refine le_antisymm (Finset.le_inf' _ _ fun z hz => Finset.inf'_le _
    (candidatePairs_subset h₁₂ hpt₁ hz)) (Finset.le_inf' _ _ fun z hz => ?_)
  rw [inf'_candidatePairs]
  exact candidateError_le_switchError hA ht hmax₁ hmax₂ h₁₂ hpt₁ hpt₂ hptmax
    (mem_distinctPairs.mp hz)

/-- With the boundary leader taken to be `h₂`, the candidate set is the two-element set of
the case `n = 2`. -/
theorem candidatePairs_self (h₁ h₂ : Fin n) :
    candidatePairs h₁ h₂ h₂ = {(h₁, h₂), (h₂, h₁)} := by
  simp [candidatePairs]

/-- **The structural content of SC33 for `n = 2`**: two candidate pairs suffice. -/
theorem candidatePairs_self_card_le (h₁ h₂ : Fin n) :
    (candidatePairs h₁ h₂ h₂).card ≤ 2 := by
  rw [candidatePairs_self]
  exact (Finset.card_insert_le _ _).trans (by simp)

/-- **SC33 for `n = 2`, the exact reduction**: the minimum of the one-switch error over all
ordered pairs of distinct modes equals the minimum over the two candidate pairs. -/
theorem inf'_distinctPairs_eq_inf'_candidatePairs_two {A : Fin n → ℝ → ℝ} {T t : ℝ}
    {h₁ h₂ : Fin n} (hn : n = 2) (hA : IsCumulative A T) (ht : t ∈ Icc (0 : ℝ) T)
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) :
    (distinctPairs n).inf' (distinctPairs_nonempty (by omega))
        (fun z => switchError A T t z.1 z.2) =
      (candidatePairs h₁ h₂ h₂).inf' (candidatePairs_nonempty h₁ h₂ h₂)
        (fun z => switchError A T t z.1 z.2) := by
  refine le_antisymm (Finset.le_inf' _ _ fun z hz => Finset.inf'_le _
    (candidatePairs_subset h₁₂ (Ne.symm h₁₂) hz)) (Finset.le_inf' _ _ fun z hz => ?_)
  rw [inf'_candidatePairs, candidateError_self]
  exact min_switchError_le_switchError_two hn hA ht hmax₁ hmax₂ h₁₂ (mem_distinctPairs.mp hz)

/-! ### The best constant schedule -/

/-- The constant schedule of mode `r`, written out on the horizon. -/
theorem constSchedule_apply (r i : Fin n) {T t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    constSchedule r T i t = if r = i then t else 0 := by
  rw [← oneSwitch_const r 0 T, oneSwitch_apply, min_eq_right ht.1, min_eq_left ht.2]
  split_ifs <;> ring

/-- The error of the constant schedule of mode `r` is `T - m_r`, so a largest-mass mode is
the best constant choice, as `thm:linear-one-switch` records. -/
theorem D_constSchedule {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    (r : Fin n) : D A (constSchedule r T) T = T - masses A T r := by
  have hTmem : T ∈ Icc (0 : ℝ) T := ⟨hT, le_rfl⟩
  have hmr : masses A T r ≤ T := hA.le_self r hTmem
  have hW : IsCumulative (constSchedule r T) T := (isSchedule_constSchedule hT r).isCumulative
  refine le_antisymm (D_le (by simp only [masses] at hmr ⊢; linarith) fun i t ht => ?_) ?_
  · rw [constSchedule_apply r i ht]
    rcases eq_or_ne r i with rfl | hri
    · rw [if_pos rfl, abs_of_nonpos (sub_nonpos.mpr (hA.le_self r ht))]
      have h := initialDeficit_mono hA r ht.1 ht.2 le_rfl
      simp only [initialDeficit, masses] at h ⊢
      linarith
    · rw [if_neg hri, sub_zero, abs_of_nonneg (hA.nonneg i ht)]
      have h1 : A i t ≤ A i T := hA.mono i t T ht.1 ht.2 le_rfl
      have h2 : A i T + A r T ≤ T := hA.pair_le (Ne.symm hri) hTmem
      simp only [masses]
      linarith
  · have h := le_D hA hW r hTmem
    rw [constSchedule_apply r r hTmem, if_pos rfl,
      abs_of_nonpos (sub_nonpos.mpr (hA.le_self r hTmem))] at h
    simp only [masses]
    linarith

/-! ### The at-most-one-switch problem on an arbitrary set of permitted boundaries

A set of permitted boundaries is an arbitrary `Finset` of grid nodes; the source allows any
subset, and the empty subset (only constant schedules remain) is included. -/

/-- The errors of the schedules permitted by the boundary set `S`: all constant schedules,
and the one-switch schedules between distinct modes whose switch time is a permitted
node. -/
def permittedErrorSet (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (S : Finset (Fin (N + 1))) : Set ℝ :=
  {e | (∃ r : Fin n, e = D A (constSchedule r T) T) ∨
    ∃ p q : Fin n, ∃ m ∈ S, p ≠ q ∧ e = switchError A T (x m) p q}

/-- The value computed by `thm:linear-one-switch`: the best constant schedule compared with
the three candidates at every permitted boundary. -/
noncomputable def permittedCandidateValue (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (S : Finset (Fin (N + 1))) (h₁ h₂ : Fin n) (pt : Fin (N + 1) → Fin n) : ℝ :=
  (insert (T - masses A T h₁)
    (S.image fun m => candidateError A T (x m) h₁ h₂ (pt m))).min'
      (Finset.insert_nonempty _ _)

/-- The candidate value is attained by one of the permitted schedules. -/
theorem permittedCandidateValue_mem {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) {h₁ h₂ : Fin n} (h₁₂ : h₁ ≠ h₂)
    {pt : Fin (N + 1) → Fin n} (hpt₁ : ∀ m, pt m ≠ h₁) (S : Finset (Fin (N + 1))) :
    permittedCandidateValue x A T S h₁ h₂ pt ∈ permittedErrorSet x A T S := by
  have hmem := Finset.min'_mem (insert (T - masses A T h₁)
    (S.image fun m => candidateError A T (x m) h₁ h₂ (pt m))) (Finset.insert_nonempty _ _)
  rw [Finset.mem_insert] at hmem
  rcases hmem with h | h
  · exact Or.inl ⟨h₁, by rw [permittedCandidateValue, h, D_constSchedule hA hT]⟩
  · obtain ⟨m, hm, hval⟩ := Finset.mem_image.mp h
    refine Or.inr ?_
    have hv : permittedCandidateValue x A T S h₁ h₂ pt =
        candidateError A T (x m) h₁ h₂ (pt m) := by rw [permittedCandidateValue, hval]
    rcases min_choice (switchError A T (x m) h₁ h₂)
      (min (switchError A T (x m) h₂ h₁) (switchError A T (x m) (pt m) h₁)) with h' | h'
    · exact ⟨h₁, h₂, m, hm, h₁₂, by rw [hv, candidateError, h']⟩
    · rcases min_choice (switchError A T (x m) h₂ h₁)
        (switchError A T (x m) (pt m) h₁) with h'' | h''
      · exact ⟨h₂, h₁, m, hm, Ne.symm h₁₂, by rw [hv, candidateError, h', h'']⟩
      · exact ⟨pt m, h₁, m, hm, hpt₁ m, by rw [hv, candidateError, h', h'']⟩

/-- **SC33, the algorithmic consequence**: comparing the three candidates at every permitted
boundary with the best constant schedule solves the at-most-one-switch problem exactly. The
permitted boundaries are an arbitrary `Finset` of grid nodes. -/
theorem isLeast_permittedErrorSet {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hx : IsGrid x T) (hA : IsCumulative A T) {h₁ h₂ : Fin n}
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂)
    {pt : Fin (N + 1) → Fin n} (hpt₁ : ∀ m, pt m ≠ h₁) (hpt₂ : ∀ m, pt m ≠ h₂)
    (hptmax : ∀ m i, i ≠ h₁ → i ≠ h₂ → A i (x m) ≤ A (pt m) (x m))
    (S : Finset (Fin (N + 1))) :
    IsLeast (permittedErrorSet x A T S) (permittedCandidateValue x A T S h₁ h₂ pt) := by
  have hT : (0 : ℝ) ≤ T := (node_mem_Icc hx 0).1.trans (node_mem_Icc hx 0).2
  refine ⟨permittedCandidateValue_mem hA hT h₁₂ hpt₁ S, ?_⟩
  set C : Finset ℝ := insert (T - masses A T h₁)
    (S.image fun m => candidateError A T (x m) h₁ h₂ (pt m)) with hC
  have hval : permittedCandidateValue x A T S h₁ h₂ pt = C.min' (Finset.insert_nonempty _ _) :=
    rfl
  rintro e (⟨r, rfl⟩ | ⟨p, q, m, hm, hpq, rfl⟩)
  · rw [D_constSchedule hA hT, hval]
    have h : C.min' (Finset.insert_nonempty _ _) ≤ T - masses A T h₁ :=
      Finset.min'_le C _ (by rw [hC]; exact Finset.mem_insert_self _ _)
    have := hmax₁ r
    linarith
  · obtain ⟨h0, hTx⟩ := node_mem_Icc hx m
    refine le_trans ?_ (candidateError_le_switchError hA ⟨h0, hTx⟩ hmax₁ hmax₂ h₁₂ (hpt₁ m)
      (hpt₂ m) (hptmax m) hpq)
    rw [hval]
    exact Finset.min'_le C _ (by
      rw [hC]
      exact Finset.mem_insert_of_mem (Finset.mem_image_of_mem _ hm))

/-- With every grid node permitted, the permitted schedules are exactly the grid schedules
with two activation blocks. -/
theorem permittedErrorSet_univ {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ} (hn : 1 < n)
    (hx : IsGrid x T) :
    permittedErrorSet x A T Finset.univ = gridScheduleErrorSet x A T 2 := by
  ext e
  constructor
  · rintro (⟨r, rfl⟩ | ⟨p, q, m, -, -, rfl⟩)
    · refine ⟨constSchedule r T, ?_, rfl⟩
      have h := isGridSchedule_oneSwitch hx r r (0 : Fin (N + 1))
      rwa [hx.first, oneSwitch_zero] at h
    · exact ⟨oneSwitch p q (x m) T, isGridSchedule_oneSwitch hx p q m, rfl⟩
  · rintro ⟨W, hW, rfl⟩
    obtain ⟨p, q, m, hpq, rfl⟩ := exists_oneSwitch_ne_of_isGridSchedule hn hx hW
    exact Or.inr ⟨p, q, m, Finset.mem_univ m, hpq, rfl⟩

/-- **SC33 for the grid optimum**: with every grid node permitted, the three-candidate
comparison computes the grid one-switch instance optimum `gridOPT x A T 1` exactly. -/
theorem gridOPT_one_eq_permittedCandidateValue {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ}
    {T : ℝ} (hn : 1 < n) (hx : IsGrid x T) (hA : IsCumulative A T) {h₁ h₂ : Fin n}
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂)
    {pt : Fin (N + 1) → Fin n} (hpt₁ : ∀ m, pt m ≠ h₁) (hpt₂ : ∀ m, pt m ≠ h₂)
    (hptmax : ∀ m i, i ≠ h₁ → i ≠ h₂ → A i (x m) ≤ A (pt m) (x m)) :
    gridOPT x A T 1 = permittedCandidateValue x A T Finset.univ h₁ h₂ pt := by
  have h := isLeast_permittedErrorSet hx hA hmax₁ hmax₂ h₁₂ hpt₁ hpt₂ hptmax Finset.univ
  rw [permittedErrorSet_univ hn hx] at h
  exact h.csInf_eq

/-- **SC33's algorithmic consequence for `n = 2`**: with two modes the two candidates
`(h₁, h₂)` and `(h₂, h₁)` at every permitted boundary, compared with the best constant
schedule, solve the at-most-one-switch problem exactly. The candidate value is the general
one with the boundary leader taken to be `h₂`; by `candidateError_self` its per-boundary
entry is `min (switchError A T (x m) h₁ h₂) (switchError A T (x m) h₂ h₁)`. -/
theorem isLeast_permittedErrorSet_two {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hn : n = 2) (hx : IsGrid x T) (hA : IsCumulative A T) {h₁ h₂ : Fin n}
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂)
    (S : Finset (Fin (N + 1))) :
    IsLeast (permittedErrorSet x A T S)
      (permittedCandidateValue x A T S h₁ h₂ fun _ => h₂) := by
  have hT : (0 : ℝ) ≤ T := (node_mem_Icc hx 0).1.trans (node_mem_Icc hx 0).2
  refine ⟨permittedCandidateValue_mem hA hT h₁₂ (fun _ => Ne.symm h₁₂) S, ?_⟩
  set C : Finset ℝ := insert (T - masses A T h₁)
    (S.image fun m => candidateError A T (x m) h₁ h₂ h₂) with hC
  have hval : (permittedCandidateValue x A T S h₁ h₂ fun _ => h₂) =
      C.min' (Finset.insert_nonempty _ _) := rfl
  rintro e (⟨r, rfl⟩ | ⟨p, q, m, hm, hpq, rfl⟩)
  · rw [D_constSchedule hA hT, hval]
    have h : C.min' (Finset.insert_nonempty _ _) ≤ T - masses A T h₁ :=
      Finset.min'_le C _ (by rw [hC]; exact Finset.mem_insert_self _ _)
    have := hmax₁ r
    linarith
  · obtain ⟨h0, hTx⟩ := node_mem_Icc hx m
    have hdom : candidateError A T (x m) h₁ h₂ h₂ ≤ switchError A T (x m) p q := by
      rw [candidateError_self]
      exact min_switchError_le_switchError_two hn hA ⟨h0, hTx⟩ hmax₁ hmax₂ h₁₂ hpq
    refine le_trans ?_ hdom
    rw [hval]
    exact Finset.min'_le C _ (by
      rw [hC]
      exact Finset.mem_insert_of_mem (Finset.mem_image_of_mem _ hm))

/-- **SC33 for `n = 2` and the grid optimum**: with every grid node permitted, the
two-candidate comparison computes `gridOPT x A T 1` exactly. -/
theorem gridOPT_one_eq_permittedCandidateValue_two {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ}
    {T : ℝ} (hn : n = 2) (hx : IsGrid x T) (hA : IsCumulative A T) {h₁ h₂ : Fin n}
    (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) :
    gridOPT x A T 1 = permittedCandidateValue x A T Finset.univ h₁ h₂ fun _ => h₂ := by
  have h := isLeast_permittedErrorSet_two hn hx hA hmax₁ hmax₂ h₁₂ Finset.univ
  rw [permittedErrorSet_univ (by omega) hx] at h
  exact h.csInf_eq

/-! ### A prescribed initial mode

With the initial mode fixed to `p`, `thm:linear-one-switch` compares only the constant
schedule of `p` with `p → q_p`, where `q_p` carries a largest terminal mass among the modes
other than `p`. -/

/-- The errors of the schedules with prescribed initial mode `p` permitted by `S`. -/
def prescribedErrorSet (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (S : Finset (Fin (N + 1))) (p : Fin n) : Set ℝ :=
  {e | e = D A (constSchedule p T) T ∨
    ∃ q : Fin n, q ≠ p ∧ ∃ m ∈ S, e = switchError A T (x m) p q}

/-- The value computed with a prescribed initial mode `p` and its optimal final mode `qp`. -/
noncomputable def prescribedCandidateValue (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) (T : ℝ)
    (S : Finset (Fin (N + 1))) (p qp : Fin n) : ℝ :=
  (insert (T - masses A T p) (S.image fun m => switchError A T (x m) p qp)).min'
    (Finset.insert_nonempty _ _)

/-- The prescribed-mode candidate value is attained by one of the permitted schedules. -/
theorem prescribedCandidateValue_mem {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) {p qp : Fin n} (hpq : p ≠ qp)
    (S : Finset (Fin (N + 1))) :
    prescribedCandidateValue x A T S p qp ∈ prescribedErrorSet x A T S p := by
  have hmem := Finset.min'_mem (insert (T - masses A T p)
    (S.image fun m => switchError A T (x m) p qp)) (Finset.insert_nonempty _ _)
  rw [Finset.mem_insert] at hmem
  rcases hmem with h | h
  · exact Or.inl (by rw [prescribedCandidateValue, h, D_constSchedule hA hT])
  · obtain ⟨m, hm, hv⟩ := Finset.mem_image.mp h
    exact Or.inr ⟨qp, Ne.symm hpq, m, hm, by rw [prescribedCandidateValue, hv]⟩

/-- **SC33 with a prescribed initial mode**: comparing the constant schedule of `p` with the
single pair `p → q_p` at every permitted boundary solves the at-most-one-switch problem with
initial mode `p`. -/
theorem isLeast_prescribedErrorSet {x : Fin (N + 1) → ℝ} {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hx : IsGrid x T) (hA : IsCumulative A T) {p qp : Fin n} (hpq : p ≠ qp)
    (hmax : ∀ i, i ≠ p → masses A T i ≤ masses A T qp) (S : Finset (Fin (N + 1))) :
    IsLeast (prescribedErrorSet x A T S p) (prescribedCandidateValue x A T S p qp) := by
  have hT : (0 : ℝ) ≤ T := (node_mem_Icc hx 0).1.trans (node_mem_Icc hx 0).2
  set C : Finset ℝ := insert (T - masses A T p) (S.image fun m => switchError A T (x m) p qp)
    with hC
  have hval : prescribedCandidateValue x A T S p qp = C.min' (Finset.insert_nonempty _ _) :=
    rfl
  refine ⟨prescribedCandidateValue_mem hA hT hpq S, ?_⟩
  · rintro e (rfl | ⟨q, hq, m, hm, rfl⟩)
    · rw [D_constSchedule hA hT, hval]
      exact Finset.min'_le C _ (by rw [hC]; exact Finset.mem_insert_self _ _)
    · obtain ⟨h0, hTx⟩ := node_mem_Icc hx m
      refine le_trans ?_ (D_oneSwitch_le_of_max_mass hA (Ne.symm hq) hpq hmax h0 hTx)
      rw [hval]
      exact Finset.min'_le C _ (by
        rw [hC]
        exact Finset.mem_insert_of_mem (Finset.mem_image_of_mem _ hm))

/-! ## SC34: the unimodality refinement

For a fixed initial mode `p` and final mode `q` the two varying terms of
`eq:one-switch-error` are `L_p(t) = t - A_p(t)` (`initialDeficit`) and
`R_p(t) = T - t - m_q` (`finalDeficit`). The first is nondecreasing, which is
`initialDeficit_mono`; their difference is *strictly* increasing, which is
`deficitGap_strictMonoOn` below. Hence `max(L_p, R_p)` is nonincreasing before the crossing
of the difference and nondecreasing after it, and the omitted-mass term does not depend on
`t` at all. -/

/-- The difference `L_p(t) - R_p(t)` of the two varying terms of `eq:one-switch-error`. -/
def deficitGap (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) (t : ℝ) : ℝ :=
  initialDeficit A p t - finalDeficit A T q t

/-- The difference of the two deficits is `2t - A_p(t) - T + m_q`, as in the source. -/
theorem deficitGap_eq (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) (t : ℝ) :
    deficitGap A T p q t = 2 * t - A p t - T + masses A T q := by
  simp only [deficitGap, initialDeficit, finalDeficit]
  ring

/-- **SC34, the quantitative half**: between `u < v` the difference of the two deficits
increases by at least `v - u`. This is exactly the source's reason for strictness. -/
theorem sub_le_deficitGap_sub {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (p q : Fin n)
    {u v : ℝ} (hu : 0 ≤ u) (huv : u ≤ v) (hv : v ≤ T) :
    v - u ≤ deficitGap A T p q v - deficitGap A T p q u := by
  have h := hA.lipschitz p u v hu huv hv
  simp only [deficitGap, initialDeficit, finalDeficit]
  linarith

/-- **SC34, the strict monotonicity**: the difference of the two deficits is strictly
increasing on the horizon, so it has at most one sign change. -/
theorem deficitGap_strictMonoOn {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (p q : Fin n) : StrictMonoOn (deficitGap A T p q) (Icc (0 : ℝ) T) := by
  intro u hu v hv huv
  have h := sub_le_deficitGap_sub hA p q hu.1 huv.le hv.2
  linarith

/-- The `t`-dependent part of the one-switch error: the larger of the two deficits. -/
noncomputable def maxDeficit (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) (t : ℝ) : ℝ :=
  max (initialDeficit A p t) (finalDeficit A T q t)

/-- The one-switch error is the omitted mass, which does not depend on the boundary, and the
larger of the two deficits. -/
theorem switchError_eq_max {A : Fin n → ℝ → ℝ} {T t : ℝ} {p q : Fin n} (hA : IsCumulative A T)
    (hpq : p ≠ q) (ht : t ∈ Icc (0 : ℝ) T) :
    switchError A T t p q = max (omittedMass A T p q) (maxDeficit A T p q t) :=
  D_oneSwitch hA hpq ht.1 ht.2

/-- Before the crossing the larger deficit is nonincreasing: if the gap is still nonpositive
at `v`, then `v` is at least as good as every earlier boundary. -/
theorem maxDeficit_le_of_le_crossing {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {u v : ℝ}
    (hv : initialDeficit A p v ≤ finalDeficit A T q v) (huv : u ≤ v) :
    maxDeficit A T p q v ≤ maxDeficit A T p q u := by
  simp only [maxDeficit, max_eq_right hv]
  refine le_trans ?_ (le_max_right (initialDeficit A p u) (finalDeficit A T q u))
  simp only [finalDeficit]
  linarith

/-- After the crossing the larger deficit is nondecreasing: if the gap is already nonnegative
at `u`, then `u` is at least as good as every later boundary. -/
theorem maxDeficit_le_of_crossing_le {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {u v : ℝ}
    (hA : IsCumulative A T) (hu : finalDeficit A T q u ≤ initialDeficit A p u) (hu0 : 0 ≤ u)
    (huv : u ≤ v) (hv : v ≤ T) : maxDeficit A T p q u ≤ maxDeficit A T p q v := by
  simp only [maxDeficit, max_eq_left hu]
  exact (initialDeficit_mono hA p hu0 huv hv).trans
    (le_max_left (initialDeficit A p v) (finalDeficit A T q v))

/-! ### Narrowing the candidate boundaries to the two adjacent to the crossing -/

/-- The permitted boundaries at or before the crossing of the two deficits. -/
noncomputable def lowerBoundaries (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) (S : Finset ℝ) :
    Finset ℝ :=
  S.filter fun t => initialDeficit A p t ≤ finalDeficit A T q t

/-- The permitted boundaries at or after the crossing of the two deficits. -/
noncomputable def upperBoundaries (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) (S : Finset ℝ) :
    Finset ℝ :=
  S.filter fun t => finalDeficit A T q t ≤ initialDeficit A p t

/-- The two permitted boundaries adjacent to the crossing: the last one at or before it and
the first one at or after it. When the crossing lies outside the permitted range one of the
two sides is empty and only the first, respectively last, permitted boundary remains. -/
noncomputable def adjacentBoundaries (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n)
    (S : Finset ℝ) : Finset ℝ :=
  (lowerBoundaries A T p q S).filter (fun t => ∀ s ∈ lowerBoundaries A T p q S, s ≤ t) ∪
    (upperBoundaries A T p q S).filter (fun t => ∀ s ∈ upperBoundaries A T p q S, t ≤ s)

/-- The adjacent boundaries are permitted boundaries. -/
theorem adjacentBoundaries_subset {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {S : Finset ℝ} :
    adjacentBoundaries A T p q S ⊆ S := by
  intro t ht
  rw [adjacentBoundaries, Finset.mem_union] at ht
  rcases ht with ht | ht <;>
    [exact (Finset.mem_filter.mp (Finset.mem_filter.mp ht).1).1;
     exact (Finset.mem_filter.mp (Finset.mem_filter.mp ht).1).1]

/-- A set of boundaries that are all maximal in a fixed finite set has at most one
element. -/
private theorem card_filter_le_one {C : Finset ℝ} :
    (C.filter fun t => ∀ s ∈ C, s ≤ t).card ≤ 1 := by
  refine Finset.card_le_one.mpr fun a ha b hb => ?_
  rw [Finset.mem_filter] at ha hb
  exact le_antisymm (hb.2 a ha.1) (ha.2 b hb.1)

/-- A set of boundaries that are all minimal in a fixed finite set has at most one
element. -/
private theorem card_filter_le_one' {C : Finset ℝ} :
    (C.filter fun t => ∀ s ∈ C, t ≤ s).card ≤ 1 := by
  refine Finset.card_le_one.mpr fun a ha b hb => ?_
  rw [Finset.mem_filter] at ha hb
  exact le_antisymm (ha.2 b hb.1) (hb.2 a ha.1)

/-- **SC34, the structural content**: at most two permitted boundaries survive, whatever the
number of permitted boundaries and of modes. -/
theorem adjacentBoundaries_card_le {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {S : Finset ℝ} :
    (adjacentBoundaries A T p q S).card ≤ 2 := by
  refine (Finset.card_union_le _ _).trans ?_
  have h₁ := card_filter_le_one (C := lowerBoundaries A T p q S)
  have h₂ := card_filter_le_one' (C := upperBoundaries A T p q S)
  omega

/-- Every permitted boundary is dominated by one of the two adjacent boundaries. -/
theorem exists_adjacentBoundaries_le {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {S : Finset ℝ}
    (hA : IsCumulative A T) (hS : ∀ t ∈ S, t ∈ Icc (0 : ℝ) T) {t : ℝ} (ht : t ∈ S) :
    ∃ t' ∈ adjacentBoundaries A T p q S, maxDeficit A T p q t' ≤ maxDeficit A T p q t := by
  rcases le_total (initialDeficit A p t) (finalDeficit A T q t) with h | h
  · have htL : t ∈ lowerBoundaries A T p q S := Finset.mem_filter.mpr ⟨ht, h⟩
    have hne : (lowerBoundaries A T p q S).Nonempty := ⟨t, htL⟩
    refine ⟨(lowerBoundaries A T p q S).max' hne, ?_, ?_⟩
    · rw [adjacentBoundaries, Finset.mem_union]
      exact Or.inl (Finset.mem_filter.mpr ⟨Finset.max'_mem _ hne,
        fun s hs => Finset.le_max' _ s hs⟩)
    · exact maxDeficit_le_of_le_crossing
        (Finset.mem_filter.mp (Finset.max'_mem _ hne)).2 (Finset.le_max' _ t htL)
  · have htU : t ∈ upperBoundaries A T p q S := Finset.mem_filter.mpr ⟨ht, h⟩
    have hne : (upperBoundaries A T p q S).Nonempty := ⟨t, htU⟩
    refine ⟨(upperBoundaries A T p q S).min' hne, ?_, ?_⟩
    · rw [adjacentBoundaries, Finset.mem_union]
      exact Or.inr (Finset.mem_filter.mpr ⟨Finset.min'_mem _ hne,
        fun s hs => Finset.min'_le _ s hs⟩)
    · have hmem : (upperBoundaries A T p q S).min' hne ∈ S :=
        (Finset.mem_filter.mp (Finset.min'_mem _ hne)).1
      exact maxDeficit_le_of_crossing_le hA
        (Finset.mem_filter.mp (Finset.min'_mem _ hne)).2 (hS _ hmem).1
        (Finset.min'_le _ t htU) (hS t ht).2

/-- The adjacent boundaries are not all missing. -/
theorem adjacentBoundaries_nonempty {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n} {S : Finset ℝ}
    (hA : IsCumulative A T) (hS : ∀ t ∈ S, t ∈ Icc (0 : ℝ) T) (hne : S.Nonempty) :
    (adjacentBoundaries A T p q S).Nonempty := by
  obtain ⟨t, ht⟩ := hne
  obtain ⟨t', ht', -⟩ := exists_adjacentBoundaries_le (p := p) (q := q) hA hS ht
  exact ⟨t', ht'⟩

/-- **SC34, the reduction**: minimizing the larger deficit over all permitted boundaries is
the same as minimizing it over the two boundaries adjacent to the crossing. -/
theorem inf'_maxDeficit_adjacentBoundaries {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n}
    {S : Finset ℝ} (hA : IsCumulative A T) (hS : ∀ t ∈ S, t ∈ Icc (0 : ℝ) T)
    (hne : S.Nonempty) :
    (adjacentBoundaries A T p q S).inf' (adjacentBoundaries_nonempty hA hS hne)
        (maxDeficit A T p q) = S.inf' hne (maxDeficit A T p q) := by
  refine le_antisymm (Finset.le_inf' _ _ fun t ht => ?_)
    (Finset.le_inf' _ _ fun t ht => Finset.inf'_le _ (adjacentBoundaries_subset ht))
  obtain ⟨t', ht', hle⟩ := exists_adjacentBoundaries_le (p := p) (q := q) hA hS ht
  exact (Finset.inf'_le _ ht').trans hle

/-- **SC34 for the one-switch error**: since the omitted-mass term does not depend on the
boundary, the same two adjacent boundaries suffice for the full one-switch error. -/
theorem inf'_switchError_adjacentBoundaries {A : Fin n → ℝ → ℝ} {T : ℝ} {p q : Fin n}
    {S : Finset ℝ} (hA : IsCumulative A T) (hpq : p ≠ q) (hS : ∀ t ∈ S, t ∈ Icc (0 : ℝ) T)
    (hne : S.Nonempty) :
    (adjacentBoundaries A T p q S).inf' (adjacentBoundaries_nonempty hA hS hne)
        (fun t => switchError A T t p q) = S.inf' hne (fun t => switchError A T t p q) := by
  refine le_antisymm (Finset.le_inf' _ _ fun t ht => ?_)
    (Finset.le_inf' _ _ fun t ht => Finset.inf'_le _ (adjacentBoundaries_subset ht))
  obtain ⟨t', ht', hle⟩ := exists_adjacentBoundaries_le (p := p) (q := q) hA hS ht
  refine (Finset.inf'_le _ ht').trans ?_
  rw [switchError_eq_max hA hpq (hS t' (adjacentBoundaries_subset ht')),
    switchError_eq_max hA hpq (hS t ht)]
  exact max_le_max le_rfl hle

/-! ## SC35: the best completion of a fixed prefix

`lem:final-residual`. A schedule `W` is fixed on the prefix `[0, u]`; its discrepancy there
is `E₀ = D A W u`, its service is `c_i = W_i(u)`, and the residuals are `r_i = m_i - c_i`.
Completing the schedule by running mode `j` on `[u, T]` has *exact* error
`max{E₀, max_{i ≠ j} r_i, T - u - r_j}`.

**Residuals may be negative** and nothing below assumes otherwise: a mode that has already
been served more than its terminal mass has `r_i < 0`. Such a term is absorbed by `E₀`,
because `-r_i ≤ W_i(u) - A_i(u) ≤ E₀`, which is why the formula uses `r_i` and not `|r_i|`.
Symmetrically `T - u - r_j` can be negative, and it is then absorbed by `E₀` as well,
because `r_j - (T - u) ≤ A_j(u) - W_j(u) ≤ E₀` by the Lipschitz bound on `A_j`.

**Limitation of the source, preserved here.** This lemma optimizes the *last block after a
fixed prefix*. It supplies **no greedy rule for choosing that prefix**: nothing below
compares different prefixes, and no claim is made that extending a locally optimal prefix
stays optimal. The eligible set of final modes is held fixed during the comparison
`D_completion_le_of_max_residual`. -/

/-- The completion of the prefix schedule `W` on `[0, u]` by the mode `j`, which is then run
for the whole remaining horizon. -/
noncomputable def completion (W : Fin n → ℝ → ℝ) (u : ℝ) (j : Fin n) : Fin n → ℝ → ℝ :=
  fun i t => W i (min t u) + (if i = j then t - min t u else 0)

/-- On the prefix the completion is the prefix schedule itself. -/
theorem completion_of_le (W : Fin n → ℝ → ℝ) (u : ℝ) (j i : Fin n) {t : ℝ} (ht : t ≤ u) :
    completion W u j i t = W i t := by
  simp [completion, min_eq_left ht]

/-- After the prefix the completion serves only the mode `j`. -/
theorem completion_of_ge (W : Fin n → ℝ → ℝ) (u : ℝ) (j i : Fin n) {t : ℝ} (ht : u ≤ t) :
    completion W u j i t = W i u + (if i = j then t - u else 0) := by
  simp [completion, min_eq_right ht]

/-- The residual `r_i = m_i - c_i` of mode `i` after the prefix. It may be negative. -/
def residual (A W : Fin n → ℝ → ℝ) (T u : ℝ) (i : Fin n) : ℝ := masses A T i - W i u

/-- The residuals sum to the remaining time, `∑ i, r_i = T - u`. -/
theorem sum_residual {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) :
    ∑ i, residual A W T u i = T - u := by
  simp only [residual, masses, Finset.sum_sub_distrib]
  rw [hA.conservation T ⟨hu0.trans huT, le_rfl⟩, hW.conservation u ⟨hu0, le_rfl⟩]

/-- Shrinking the horizon of a cumulative allocation. -/
theorem IsCumulative.mono_horizon {A : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (huT : u ≤ T) : IsCumulative A u where
  initial := hA.initial
  mono i s t hs hst ht := hA.mono i s t hs hst (ht.trans huT)
  lipschitz i s t hs hst ht := hA.lipschitz i s t hs hst (ht.trans huT)
  conservation t ht := hA.conservation t ⟨ht.1, ht.2.trans huT⟩

/-- The time spent beyond the prefix is nondecreasing. -/
private theorem sub_min_le_sub_min {u s t : ℝ} (hst : s ≤ t) : s - min s u ≤ t - min t u := by
  rcases le_total s u with hs | hs
  · rw [min_eq_left hs]
    rcases le_total t u with ht | ht
    · rw [min_eq_left ht]
      linarith
    · rw [min_eq_right ht]
      linarith
  · rw [min_eq_right hs, min_eq_right (hs.trans hst)]
    linarith

/-- The completion of a prefix schedule is a cumulative allocation on the full horizon. -/
theorem isCumulative_completion {W : Fin n → ℝ → ℝ} {u T : ℝ} (hW : IsCumulative W u)
    (hu0 : 0 ≤ u) (j : Fin n) : IsCumulative (completion W u j) T where
  initial i := by
    rw [completion_of_le W u j i hu0, hW.initial i]
  mono i s t hs hst _ := by
    have hmin : min s u ≤ min t u := min_le_min hst le_rfl
    have h1 : W i (min s u) ≤ W i (min t u) :=
      hW.mono i _ _ (le_min hs hu0) hmin (min_le_right t u)
    have h2 : s - min s u ≤ t - min t u := sub_min_le_sub_min hst
    simp only [completion]
    split_ifs <;> linarith
  lipschitz i s t hs hst _ := by
    have hmin : min s u ≤ min t u := min_le_min hst le_rfl
    have h1 : W i (min t u) - W i (min s u) ≤ min t u - min s u :=
      hW.lipschitz i _ _ (le_min hs hu0) hmin (min_le_right t u)
    have h2 : s - min s u ≤ t - min t u := sub_min_le_sub_min hst
    simp only [completion]
    split_ifs <;> linarith
  conservation t ht := by
    simp only [completion, Finset.sum_add_distrib]
    rw [hW.conservation (min t u) ⟨le_min ht.1 hu0, min_le_right t u⟩]
    simp

/-- Every error of the completion on the prefix is already an error of the prefix
schedule. -/
theorem D_le_D_completion {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) (j : Fin n) :
    D A W u ≤ D A (completion W u j) T := by
  have hn : 0 < n := Nat.lt_of_le_of_lt (Nat.zero_le j.val) j.isLt
  refine csSup_le_csSup (errorSet_bddAbove hA (isCumulative_completion hW hu0 j))
    (errorSet_nonempty hn hu0) ?_
  rintro e ⟨i, t, ht, rfl⟩
  exact ⟨i, t, ⟨ht.1, ht.2.trans huT⟩, (completion_of_le W u j i ht.2).symm ▸ rfl⟩

/-- Every residual of an inactive mode is an error of the completion, at the horizon. -/
theorem residual_le_D_completion {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) {i j : Fin n} (hij : i ≠ j) :
    residual A W T u i ≤ D A (completion W u j) T := by
  have h := le_D hA (isCumulative_completion hW hu0 j) i ⟨hu0.trans huT, le_rfl⟩
  rw [completion_of_ge W u j i huT, if_neg hij, add_zero] at h
  exact (le_abs_self _).trans h

/-- The final term of `eq:final-residual` is an error of the completion, at the horizon. -/
theorem sub_residual_le_D_completion {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) (j : Fin n) :
    T - u - residual A W T u j ≤ D A (completion W u j) T := by
  have h := le_D hA (isCumulative_completion hW hu0 j) j ⟨hu0.trans huT, le_rfl⟩
  rw [completion_of_ge W u j j huT, if_pos rfl] at h
  refine le_trans ?_ ((neg_le_abs _).trans h)
  simp only [residual, masses]
  linarith

/-- The three terms of `eq:final-residual` bound the error of the completion. -/
theorem D_completion_le {A W : Fin n → ℝ → ℝ} {T u c : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) {j : Fin n} (hE : D A W u ≤ c)
    (hM : ∀ i, i ≠ j → residual A W T u i ≤ c) (hF : T - u - residual A W T u j ≤ c) :
    D A (completion W u j) T ≤ c := by
  have hn : 0 < n := Nat.lt_of_le_of_lt (Nat.zero_le j.val) j.isLt
  have hAu : IsCumulative A u := hA.mono_horizon huT
  have hE0 : 0 ≤ D A W u := D_nonneg hn hAu hW hu0
  refine D_le (hE0.trans hE) fun i t ht => ?_
  rcases le_total t u with htu | hut
  · rw [completion_of_le W u j i htu]
    exact (le_D hAu hW i ⟨ht.1, htu⟩).trans hE
  · rw [completion_of_ge W u j i hut]
    have h3 := abs_le.mp (le_D hAu hW i ⟨hu0, le_rfl⟩)
    rcases eq_or_ne i j with rfl | hij
    · rw [if_pos rfl]
      have h1 : A i t - A i u ≤ t - u := hA.lipschitz i u t hu0 hut ht.2
      have h2 : A i T - A i t ≤ T - t := hA.lipschitz i t T ht.1 ht.2 le_rfl
      have hFi : T - u - (A i T - W i u) ≤ c := hF
      rw [abs_le]
      constructor <;> linarith [h3.1, h3.2]
    · rw [if_neg hij, add_zero]
      have h1 : A i u ≤ A i t := hA.mono i u t hu0 hut ht.2
      have h2 : A i t ≤ A i T := hA.mono i t T ht.1 ht.2 le_rfl
      have hMi : A i T - W i u ≤ c := hM i hij
      rw [abs_le]
      constructor <;> linarith [h3.1, h3.2]

/-- **SC35, `eq:final-residual`**: the exact error of completing the fixed prefix `W` on
`[0, u]` in mode `j` is `max{E₀, max_{i ≠ j} r_i, T - u - r_j}`, where `E₀ = D A W u` is the
prefix discrepancy and `r_i = m_i - W_i(u)` are the residuals. Residuals are not assumed
nonnegative. -/
theorem D_completion_eq {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T) (j : Fin n)
    (hne : (Finset.univ.erase j).Nonempty) :
    D A (completion W u j) T =
      max (D A W u) (max ((Finset.univ.erase j).sup' hne (residual A W T u))
        (T - u - residual A W T u j)) := by
  refine le_antisymm (D_completion_le hA hW hu0 huT (le_max_left _ _) (fun i hij => ?_)
    ((le_max_right _ _).trans' (le_max_right _ _))) (max_le ?_ (max_le ?_ ?_))
  · exact le_trans (Finset.le_sup' (residual A W T u)
      (Finset.mem_erase.mpr ⟨hij, Finset.mem_univ i⟩)) ((le_max_left _ _).trans
        (le_max_right _ _))
  · exact D_le_D_completion hA hW hu0 huT j
  · exact Finset.sup'_le _ _ fun i hi =>
      residual_le_D_completion hA hW hu0 huT (Finset.mem_erase.mp hi).1
  · exact sub_residual_le_D_completion hA hW hu0 huT j

/-- With at least two modes every mode has a competitor, so the maximum over the other modes
in `eq:final-residual` is over a nonempty set. -/
theorem erase_univ_nonempty (hn : 1 < n) (j : Fin n) : (Finset.univ.erase j).Nonempty := by
  rw [← Finset.card_pos, Finset.card_erase_of_mem (Finset.mem_univ j)]
  simp only [Finset.card_univ, Fintype.card_fin]
  omega

/-- **SC35, optimality of a largest residual**: replacing the final mode by one of no smaller
residual cannot increase the error of the completion. Residuals are not assumed
nonnegative. -/
theorem D_completion_le_of_residual_le {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hn : 1 < n)
    (hA : IsCumulative A T) (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T)
    {j j' : Fin n} (hrj : residual A W T u j ≤ residual A W T u j') :
    D A (completion W u j') T ≤ D A (completion W u j) T := by
  rcases eq_or_ne j' j with rfl | hjj
  · exact le_rfl
  · have hne := erase_univ_nonempty hn j
    have hrj' : residual A W T u j' ≤ (Finset.univ.erase j).sup' hne (residual A W T u) :=
      Finset.le_sup' _ (Finset.mem_erase.mpr ⟨hjj, Finset.mem_univ j'⟩)
    rw [D_completion_eq hA hW hu0 huT j' (erase_univ_nonempty hn j'),
      D_completion_eq hA hW hu0 huT j hne]
    refine max_le_max le_rfl (max_le_max (Finset.sup'_le _ _ fun i hi => ?_) (by linarith))
    rcases eq_or_ne i j with rfl | hij
    · exact hrj.trans hrj'
    · exact Finset.le_sup' _ (Finset.mem_erase.mpr ⟨hij, Finset.mem_univ i⟩)

/-- **SC35, the eligible-set form**: among any fixed nonempty set `J` of eligible final
modes, a mode `j'` of largest residual is an optimal completion. The eligible set is held
fixed during the comparison, and no comparison between different prefixes is made. -/
theorem isLeast_eligibleCompletionErrors {A W : Fin n → ℝ → ℝ} {T u : ℝ} (hn : 1 < n)
    (hA : IsCumulative A T) (hW : IsCumulative W u) (hu0 : 0 ≤ u) (huT : u ≤ T)
    {J : Finset (Fin n)} {j' : Fin n} (hj' : j' ∈ J)
    (hmax : ∀ i ∈ J, residual A W T u i ≤ residual A W T u j') :
    IsLeast {e | ∃ j ∈ J, e = D A (completion W u j) T} (D A (completion W u j') T) :=
  ⟨⟨j', hj', rfl⟩, by
    rintro e ⟨j, hj, rfl⟩
    exact D_completion_le_of_residual_le hn hA hW hu0 huT (hmax j hj)⟩

/-! ### SC35: the endpoint reading of `E₀` is false, with a witness

Reading `E₀` as the discrepancy at the single time `u` instead of the error over the whole
prefix `[0, u]` breaks the `≤` direction of `eq:final-residual`, because a larger discrepancy
earlier in the prefix is then not counted. The witness below has two modes, `T = 4`, `u = 3`,
the input `A i t = t / 2`, and the prefix schedule that runs mode `0` on `[0, 2]` and mode `1`
on `[2, 3]`. The endpoint discrepancy is `1/2` in both modes, the residuals are `r₀ = 0` and
`r₁ = 1`, so completing in mode `1` would be given the value `max{1/2, 0, 0} = 1/2` by the
endpoint reading, while the completion's actual error is `1`, attained at `t = 2`. With the
exact reading `E₀ = D A W u = 1` the formula gives `max{1, 0, 0} = 1`, correctly. -/

/-- The input of the endpoint-reading witness: two modes, each served at rate `1/2`. -/
noncomputable def endpointWitnessA : Fin 2 → ℝ → ℝ := fun _ t => t / 2

/-- The prefix schedule of the endpoint-reading witness: mode `0` on `[0, 2]`, then mode `1`
on `[2, 3]`. -/
noncomputable def endpointWitnessW : Fin 2 → ℝ → ℝ := occupation ![0, 1] ![0, 2, 3]

theorem endpointWitnessA_apply (i : Fin 2) (t : ℝ) : endpointWitnessA i t = t / 2 := rfl

theorem endpointWitnessW_zero (t : ℝ) : endpointWitnessW 0 t = min t 2 - min t 0 := by
  simp [endpointWitnessW, occupation, Fin.sum_univ_two]

theorem endpointWitnessW_one (t : ℝ) : endpointWitnessW 1 t = min t 3 - min t 2 := by
  simp [endpointWitnessW, occupation, Fin.sum_univ_two]

theorem endpointWitnessA_isCumulative : IsCumulative endpointWitnessA 4 where
  initial i := by simp [endpointWitnessA]
  mono i s t _ hst _ := by simp only [endpointWitnessA]; linarith
  lipschitz i s t _ hst _ := by simp only [endpointWitnessA]; linarith
  conservation t _ := by simp only [endpointWitnessA, Fin.sum_univ_two]; ring

/-- The prefix of the witness is a genuine two-block schedule on `[0, 3]`. -/
theorem endpointWitnessW_isSchedule : IsSchedule 2 3 endpointWitnessW := by
  refine ⟨![0, 1], ![0, 2, 3], ⟨rfl, rfl, ?_⟩, rfl⟩
  refine Fin.monotone_iff_le_succ.mpr ?_
  rw [Fin.forall_fin_two]
  refine ⟨by norm_num, ?_⟩
  change (2 : ℝ) ≤ 3
  norm_num

theorem endpointWitnessW_isCumulative : IsCumulative endpointWitnessW 3 :=
  endpointWitnessW_isSchedule.isCumulative

/-- Every discrepancy of the witness on the prefix `[0, 3]` is at most `1`. -/
theorem endpointWitness_abs_le_one {t : ℝ} (ht0 : 0 ≤ t) (ht3 : t ≤ 3) (i : Fin 2) :
    |endpointWitnessA i t - endpointWitnessW i t| ≤ 1 := by
  have h0 : min t 0 = 0 := min_eq_right ht0
  have h3 : min t 3 = t := min_eq_left ht3
  revert i
  rw [Fin.forall_fin_two]
  rcases le_total t 2 with h2 | h2
  · have hm : min t 2 = t := min_eq_left h2
    refine ⟨?_, ?_⟩
    · rw [endpointWitnessA_apply, endpointWitnessW_zero, h0, hm, abs_le]
      constructor <;> linarith
    · rw [endpointWitnessA_apply, endpointWitnessW_one, h3, hm, abs_le]
      constructor <;> linarith
  · have hm : min t 2 = 2 := min_eq_right h2
    refine ⟨?_, ?_⟩
    · rw [endpointWitnessA_apply, endpointWitnessW_zero, h0, hm, abs_le]
      constructor <;> linarith
    · rw [endpointWitnessA_apply, endpointWitnessW_one, h3, hm, abs_le]
      constructor <;> linarith

/-- The discrepancy of the witness at the interior time `t = 2` is `1`: mode `0` has been
served `2` while the input has allocated it only `1`. -/
theorem endpointWitness_abs_sub_two :
    |endpointWitnessA (0 : Fin 2) 2 - endpointWitnessW 0 2| = 1 := by
  rw [endpointWitnessA_apply, endpointWitnessW_zero]
  norm_num [min_def]

/-- The endpoint discrepancy of the witness is `1/2` in both modes. -/
theorem endpointWitness_abs_sub_endpoint (i : Fin 2) :
    |endpointWitnessA i 3 - endpointWitnessW i 3| = 1 / 2 := by
  revert i
  rw [Fin.forall_fin_two]
  refine ⟨?_, ?_⟩
  · rw [endpointWitnessA_apply, endpointWitnessW_zero]
    norm_num [min_def]
  · rw [endpointWitnessA_apply, endpointWitnessW_one]
    norm_num [min_def]

/-- The residual of the inactive mode `0` is zero. -/
theorem endpointWitness_residual_zero :
    residual endpointWitnessA endpointWitnessW 4 3 0 = 0 := by
  simp only [residual, masses, endpointWitnessA_apply, endpointWitnessW_zero]
  norm_num [min_def]

/-- The residual of the final mode `1` is `1`, exactly the remaining time `T - u`. -/
theorem endpointWitness_residual_one :
    residual endpointWitnessA endpointWitnessW 4 3 1 = 1 := by
  simp only [residual, masses, endpointWitnessA_apply, endpointWitnessW_one]
  norm_num [min_def]

/-- The exact prefix error of the witness is `1`, attained at `t = 2`, twice the endpoint
discrepancy. -/
theorem endpointWitness_D_prefix : D endpointWitnessA endpointWitnessW 3 = 1 := by
  refine le_antisymm (D_le zero_le_one fun i t ht =>
    endpointWitness_abs_le_one ht.1 ht.2 i) ?_
  have hAu : IsCumulative endpointWitnessA 3 :=
    endpointWitnessA_isCumulative.mono_horizon (by norm_num)
  have h := le_D hAu endpointWitnessW_isCumulative 0 (t := 2) ⟨by norm_num, by norm_num⟩
  rwa [endpointWitness_abs_sub_two] at h

/-- The exact error of completing the witness prefix in mode `1` is `1`, not the `1/2` that
the endpoint reading of `eq:final-residual` predicts. -/
theorem endpointWitness_D_completion :
    D endpointWitnessA (completion endpointWitnessW 3 1) 4 = 1 := by
  have hcomp : IsCumulative (completion endpointWitnessW 3 1) 4 :=
    isCumulative_completion endpointWitnessW_isCumulative (by norm_num) 1
  refine le_antisymm (D_le zero_le_one fun i t ht => ?_) ?_
  · obtain ⟨ht0, ht4⟩ := ht
    rcases le_total t 3 with h3 | h3
    · rw [completion_of_le _ _ _ _ h3]
      exact endpointWitness_abs_le_one ht0 h3 i
    · rw [completion_of_ge _ _ _ _ h3]
      revert i
      rw [Fin.forall_fin_two]
      refine ⟨?_, ?_⟩
      · rw [endpointWitnessA_apply, endpointWitnessW_zero,
          show min (3 : ℝ) 2 - min (3 : ℝ) 0 = 2 by norm_num [min_def],
          if_neg (by decide : ¬((0 : Fin 2) = 1)), add_zero, abs_le]
        constructor <;> linarith
      · rw [endpointWitnessA_apply, endpointWitnessW_one,
          show min (3 : ℝ) 3 - min (3 : ℝ) 2 = 1 by norm_num [min_def],
          if_pos rfl, abs_le]
        constructor <;> linarith
  · have h := le_D endpointWitnessA_isCumulative hcomp 0 (t := 2) ⟨by norm_num, by norm_num⟩
    rw [completion_of_le _ _ _ _ (by norm_num : (2 : ℝ) ≤ 3),
      endpointWitness_abs_sub_two] at h
    exact h

/-- **SC35, the endpoint reading of `E₀` is false.** For the two-mode witness with `T = 4`,
`u = 3`, input `A i t = t / 2` and the prefix schedule running mode `0` on `[0, 2]` and mode
`1` on `[2, 3]`, the right-hand side of `eq:final-residual` with `E₀` read as the discrepancy
at the single endpoint `u` is `max{1/2, 0, 0} = 1/2`, strictly below the actual error `1` of
the completion in mode `1`. With two modes and `j = 1` the middle term `max_{i ≠ j} r_i` is
`r₀`. So the `≤` direction of `eq:final-residual` fails under the endpoint reading, whereas
`D_completion_eq` holds with the exact prefix error `E₀ = D A W u = 1`. -/
theorem endpointWitness_lt_D_completion :
    max (max |endpointWitnessA 0 3 - endpointWitnessW 0 3|
          |endpointWitnessA 1 3 - endpointWitnessW 1 3|)
        (max (residual endpointWitnessA endpointWitnessW 4 3 0)
          (4 - 3 - residual endpointWitnessA endpointWitnessW 4 3 1))
      < D endpointWitnessA (completion endpointWitnessW 3 1) 4 := by
  rw [endpointWitness_abs_sub_endpoint 0, endpointWitness_abs_sub_endpoint 1,
    endpointWitness_residual_zero, endpointWitness_residual_one, endpointWitness_D_completion]
  norm_num

end GridSwitching
