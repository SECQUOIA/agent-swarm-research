import Formal.GridSwitching.Model

/-!
# SC10 and SC11: the three-term one-switch error formula and final-mode dominance

This module treats the one-switch schedules `W^{p,q,τ}` of
`paper-switching-control/sections/02-uniform-one-switch.tex`: mode `p` is active on `[0, τ]`
and mode `q` on `[τ, T]`, with `0 ≤ τ ≤ T`. The endpoints `τ = 0` and `τ = T` are permitted,
so constant schedules are included.

* `oneSwitch`, `isSchedule_oneSwitch`: the schedule itself, as an `occupation` of the
  two-letter word `![p, q]` with the ordered times `![0, τ, T]`, and its membership in the
  two-block schedule class.
* `D_oneSwitch` (SC10): `lem:one-switch-error`, the three-term formula
  `eq:one-switch-error`.
* `initialDeficit_mono` (first half of SC34): `t - A p t` is nondecreasing on the horizon.
* `D_oneSwitch_mono_masses`, `D_oneSwitch_le_of_max_mass`, `oneSwitch_reduction` (SC11):
  final-mode dominance and the reduction to the pairs `p → h₁` (`p ≠ h₁`) and `h₁ → h₂`.

## Vocabulary

The three terms of `eq:one-switch-error` are named once here and used under these names by
the rest of the package.

* The **omitted mass** `omittedMass A T p q` is the largest terminal mass of a mode outside
  `{p, q}`, and is `0` when there is no such mode (the `n = 2` convention).
* The **initial deficit** `initialDeficit A p τ = τ - A p τ` is the positive discrepancy of
  the final mode at the switch time, bounded through `A p τ + A q τ ≤ τ`.
* The **final deficit** `finalDeficit A T q τ = T - masses A T q - τ` is the negative
  terminal discrepancy of the final mode, and also bounds the positive terminal discrepancy
  of the initial mode through `m p + m q ≤ T`.

## Representing the omitted maximum

`omittedMass` is `Finset.fold max 0` over `(Finset.univ.erase p).erase q`. Compared with
`Finset.sup'`, folding needs no nonemptiness side condition, so the `n = 2` case where the
index set is empty is handled by the definition itself rather than by a case split at every
use; compared with `Finset.sup`, it avoids `ℝ` lacking an `OrderBot` and avoids a detour
through `ℝ≥0`. The explicit neutral element `0` is exactly the convention demanded by SC10.
Downstream modules should use only the three-lemma interface `omittedMass_nonneg`,
`masses_le_omittedMass` and `omittedMass_le`, which characterizes `omittedMass` as the least
upper bound of `0` together with the omitted terminal masses.
-/

namespace GridSwitching

open Set

variable {n : ℕ}

/-- A mode index witnesses that there is at least one mode. -/
private theorem pos_of_mode (i : Fin n) : 0 < n :=
  Nat.lt_of_le_of_lt (Nat.zero_le i.val) i.isLt

/-- Two distinct coordinates of a cumulative allocation together never exceed the elapsed
time; this is the conservation identity together with nonnegativity of the other
coordinates. -/
theorem IsCumulative.pair_le {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) {p q : Fin n}
    (hpq : p ≠ q) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : A p t + A q t ≤ t :=
  calc A p t + A q t = ∑ i ∈ ({p, q} : Finset (Fin n)), A i t :=
        (Finset.sum_pair (f := fun i => A i t) hpq).symm
    _ ≤ ∑ i, A i t :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun i _ _ => hA.nonneg i ht
    _ = t := hA.conservation t ht

/-! ## The one-switch schedule -/

/-- The one-switch schedule `W^{p,q,τ}`: mode `p` is active on `[0, τ]` and mode `q` on
`[τ, T]`. It is the cumulative occupation of the two-letter word `![p, q]` with the ordered
times `![0, τ, T]`. Both `τ = 0` and `τ = T` are allowed, so constant schedules are
included. -/
noncomputable def oneSwitch (p q : Fin n) (τ T : ℝ) : Fin n → ℝ → ℝ :=
  occupation ![p, q] ![0, τ, T]

/-- The two blocks of the one-switch schedule, written out. -/
theorem oneSwitch_apply (p q : Fin n) (τ T : ℝ) (i : Fin n) (t : ℝ) :
    oneSwitch p q τ T i t =
      (if p = i then min t τ - min t 0 else 0) + (if q = i then min t T - min t τ else 0) := by
  rw [oneSwitch, occupation, Fin.sum_univ_two]
  rfl

/-- A mode outside `{p, q}` is never activated by the one-switch schedule. -/
theorem oneSwitch_of_ne {p q i : Fin n} (hip : i ≠ p) (hiq : i ≠ q) (τ T t : ℝ) :
    oneSwitch p q τ T i t = 0 := by
  rw [oneSwitch_apply, if_neg (fun h => hip h.symm), if_neg (fun h => hiq h.symm), add_zero]

/-- The initial mode of the one-switch schedule is active exactly up to the switch time. -/
theorem oneSwitch_left {p q : Fin n} (hpq : p ≠ q) (τ T : ℝ) {t : ℝ} (ht : 0 ≤ t) :
    oneSwitch p q τ T p t = min t τ := by
  rw [oneSwitch_apply, if_pos rfl, if_neg (Ne.symm hpq), add_zero, min_eq_right ht, sub_zero]

/-- The final mode of the one-switch schedule is active exactly after the switch time. -/
theorem oneSwitch_right {p q : Fin n} (hpq : p ≠ q) (τ : ℝ) {T t : ℝ} (ht : t ≤ T) :
    oneSwitch p q τ T q t = t - min t τ := by
  rw [oneSwitch_apply, if_neg hpq, if_pos rfl, zero_add, min_eq_left ht]

/-- Switching at time zero leaves only the final mode: the one-switch schedule degenerates to
the constant schedule of `q`. -/
theorem oneSwitch_zero (p q : Fin n) (T : ℝ) : oneSwitch p q 0 T = constSchedule q T := by
  funext i t
  rw [oneSwitch_apply]
  change _ = ∑ j : Fin 1, if q = i then min t (![0, T] j.succ) - min t (![0, T] j.castSucc) else 0
  rw [Fin.sum_univ_one]
  simp

/-- Switching at the horizon leaves only the initial mode: the one-switch schedule degenerates
to the constant schedule of `p`. -/
theorem oneSwitch_horizon (p q : Fin n) (T : ℝ) : oneSwitch p q T T = constSchedule p T := by
  funext i t
  rw [oneSwitch_apply]
  change _ = ∑ j : Fin 1, if p = i then min t (![0, T] j.succ) - min t (![0, T] j.castSucc) else 0
  rw [Fin.sum_univ_one]
  simp

/-- SC10, first half: the one-switch schedule uses two activation blocks, that is, at most
one switch. The degenerate switch times `τ = 0` and `τ = T` are included. -/
theorem isSchedule_oneSwitch {τ T : ℝ} (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) (p q : Fin n) :
    IsSchedule 2 T (oneSwitch p q τ T) := by
  refine ⟨![p, q], ![0, τ, T], ⟨rfl, rfl, ?_⟩, rfl⟩
  refine Fin.monotone_iff_le_succ.mpr fun j => ?_
  fin_cases j
  · simpa using hτ0
  · simpa using hτT

/-- The one-switch schedule is a cumulative allocation. -/
theorem isCumulative_oneSwitch {τ T : ℝ} (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) (p q : Fin n) :
    IsCumulative (oneSwitch p q τ T) T :=
  (isSchedule_oneSwitch hτ0 hτT p q).isCumulative

/-! ## The three terms of the formula -/

/-- The **omitted mass**: the largest terminal mass of a mode outside `{p, q}`, and `0` when
there is no such mode. The fold with neutral element `0` implements the `n = 2` convention of
`lem:one-switch-error` without a case split. -/
noncomputable def omittedMass (A : Fin n → ℝ → ℝ) (T : ℝ) (p q : Fin n) : ℝ :=
  ((Finset.univ.erase p).erase q).fold max 0 (masses A T)

/-- The omitted mass is nonnegative, by the `n = 2` convention even when no mode is
omitted. -/
theorem omittedMass_nonneg {A : Fin n → ℝ → ℝ} {T : ℝ} (p q : Fin n) :
    0 ≤ omittedMass A T p q :=
  (Finset.le_fold_max _).mpr (Or.inl le_rfl)

/-- Every omitted terminal mass is dominated by the omitted mass. -/
theorem masses_le_omittedMass {A : Fin n → ℝ → ℝ} {T : ℝ} {p q i : Fin n} (hip : i ≠ p)
    (hiq : i ≠ q) : masses A T i ≤ omittedMass A T p q :=
  (Finset.le_fold_max _).mpr
    (Or.inr ⟨i, Finset.mem_erase.mpr ⟨hiq, Finset.mem_erase.mpr ⟨hip, Finset.mem_univ i⟩⟩,
      le_rfl⟩)

/-- The omitted mass is the least of the nonnegative upper bounds of the omitted terminal
masses. -/
theorem omittedMass_le {A : Fin n → ℝ → ℝ} {T c : ℝ} {p q : Fin n} (hc : 0 ≤ c)
    (h : ∀ i, i ≠ p → i ≠ q → masses A T i ≤ c) : omittedMass A T p q ≤ c := by
  refine (Finset.fold_max_le _).mpr ⟨hc, fun i hi => ?_⟩
  rw [Finset.mem_erase] at hi
  obtain ⟨hiq, hi⟩ := hi
  exact h i (Finset.mem_erase.mp hi).1 hiq

/-- The **initial deficit** `t - A p t` of mode `p` at time `t`: the positive discrepancy
that mode `q` has accumulated when it is activated at time `t`. -/
def initialDeficit (A : Fin n → ℝ → ℝ) (p : Fin n) (t : ℝ) : ℝ := t - A p t

/-- The **final deficit** `T - m q - τ` of mode `q` for the switch time `τ`: the negative
terminal discrepancy of the final mode. -/
def finalDeficit (A : Fin n → ℝ → ℝ) (T : ℝ) (q : Fin n) (τ : ℝ) : ℝ :=
  T - masses A T q - τ

/-- The initial deficit is nonnegative on the horizon. -/
theorem initialDeficit_nonneg {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (p : Fin n)
    {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) : 0 ≤ initialDeficit A p t :=
  sub_nonneg.mpr (hA.le_self p ht)

/-- First half of SC34: the initial deficit `t - A p t` is nondecreasing in `t` on the
horizon, because `A p` is `1`-Lipschitz. -/
theorem initialDeficit_mono {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (p : Fin n)
    {s t : ℝ} (hs : 0 ≤ s) (hst : s ≤ t) (ht : t ≤ T) :
    initialDeficit A p s ≤ initialDeficit A p t := by
  have := hA.lipschitz p s t hs hst ht
  simp only [initialDeficit]
  linarith

/-! ## SC10: the three-term one-switch error formula -/

/-- SC10, `eq:one-switch-error`: for a cumulative input `A`, distinct modes `p ≠ q` and a
switch time `0 ≤ τ ≤ T`, the error of the one-switch schedule is the maximum of the omitted
mass, the initial deficit `τ - A p τ` and the final deficit `T - m q - τ`.

The degenerate switch times `τ = 0` and `τ = T` are included, as is the case `n = 2`, where
the omitted mass is `0` by convention. -/
theorem D_oneSwitch {A : Fin n → ℝ → ℝ} {T τ : ℝ} {p q : Fin n} (hA : IsCumulative A T)
    (hpq : p ≠ q) (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) :
    D A (oneSwitch p q τ T) T =
      max (omittedMass A T p q) (max (initialDeficit A p τ) (finalDeficit A T q τ)) := by
  have hn : 0 < n := pos_of_mode p
  have hT : (0 : ℝ) ≤ T := hτ0.trans hτT
  have hτmem : τ ∈ Icc (0 : ℝ) T := ⟨hτ0, hτT⟩
  have hTmem : T ∈ Icc (0 : ℝ) T := ⟨hT, le_rfl⟩
  have hW : IsCumulative (oneSwitch p q τ T) T := isCumulative_oneSwitch hτ0 hτT p q
  have hmass : A p T + A q T ≤ T := hA.pair_le hpq hTmem
  have hswitch : A p τ + A q τ ≤ τ := hA.pair_le hpq hτmem
  have hM0 : 0 ≤ max (omittedMass A T p q) (max (initialDeficit A p τ) (finalDeficit A T q τ)) :=
    (omittedMass_nonneg p q).trans (le_max_left _ _)
  have hid : initialDeficit A p τ ≤
      max (omittedMass A T p q) (max (initialDeficit A p τ) (finalDeficit A T q τ)) :=
    (le_max_left _ _).trans (le_max_right _ _)
  have hfd : finalDeficit A T q τ ≤
      max (omittedMass A T p q) (max (initialDeficit A p τ) (finalDeficit A T q τ)) :=
    (le_max_right _ _).trans (le_max_right _ _)
  simp only [initialDeficit, finalDeficit, masses] at hid hfd ⊢
  refine le_antisymm (D_le hM0 fun i t ht => ?_) (max_le ?_ (max_le ?_ ?_))
  · -- Every pointwise discrepancy is bounded by the right-hand side.
    have hAt : 0 ≤ A i t := hA.nonneg i ht
    rcases eq_or_ne i p with rfl | hip
    · -- The initial mode.
      rw [oneSwitch_left hpq τ T ht.1, abs_le]
      rcases le_total t τ with h | h
      · rw [min_eq_left h]
        have h1 : t - A i t ≤ τ - A i τ :=
          initialDeficit_mono (A := A) hA i ht.1 h hτT
        exact ⟨by linarith, by linarith [hA.le_self i ht]⟩
      · rw [min_eq_right h]
        have h1 : A i τ ≤ A i t := hA.mono i τ t hτ0 h ht.2
        have h2 : A i t ≤ A i T := hA.mono i t T ht.1 ht.2 le_rfl
        exact ⟨by linarith, by linarith⟩
    · rcases eq_or_ne i q with rfl | hiq
      · -- The final mode.
        rw [oneSwitch_right (Ne.symm hip) τ ht.2, abs_le]
        rcases le_total t τ with h | h
        · rw [min_eq_left h, sub_self]
          have h1 : A i t ≤ A i τ := hA.mono i t τ ht.1 h hτT
          exact ⟨by linarith, by linarith⟩
        · rw [min_eq_right h]
          have h1 : A p τ ≤ A p t := hA.mono p τ t hτ0 h ht.2
          have h2 : A p t + A i t ≤ t := hA.pair_le (Ne.symm hip) ht
          have h3 : A i T - A i t ≤ T - t := hA.lipschitz i t T ht.1 ht.2 le_rfl
          exact ⟨by linarith, by linarith⟩
      · -- An omitted mode.
        rw [oneSwitch_of_ne hip hiq, sub_zero, abs_of_nonneg hAt]
        have h1 : A i t ≤ A i T := hA.mono i t T ht.1 ht.2 le_rfl
        have h2 : masses A T i ≤ omittedMass A T p q := masses_le_omittedMass hip hiq
        simp only [masses] at h2
        exact h1.trans (h2.trans (le_max_left _ _))
  · -- The omitted mass is an actual error, attained at the horizon.
    refine omittedMass_le (D_nonneg hn hA hW hT) fun i hip hiq => ?_
    have h1 : |A i T - oneSwitch p q τ T i T| ≤ D A (oneSwitch p q τ T) T :=
      le_D hA hW i hTmem
    rwa [oneSwitch_of_ne hip hiq, sub_zero, abs_of_nonneg (hA.nonneg i hTmem)] at h1
  · -- The initial deficit is an actual error, attained at the switch time.
    have h1 : |A p τ - oneSwitch p q τ T p τ| ≤ D A (oneSwitch p q τ T) T :=
      le_D hA hW p hτmem
    rwa [oneSwitch_left hpq τ T hτ0, min_self,
      abs_of_nonpos (sub_nonpos.mpr (hA.le_self p hτmem)), neg_sub] at h1
  · -- The final deficit is dominated by the terminal discrepancy of the final mode.
    have h1 : |A q T - oneSwitch p q τ T q T| ≤ D A (oneSwitch p q τ T) T :=
      le_D hA hW q hTmem
    rw [oneSwitch_right hpq τ (le_refl T), min_eq_right hτT] at h1
    have h2 : -(A q T - (T - τ)) ≤ |A q T - (T - τ)| := neg_le_abs _
    linarith

/-! ## SC11: final-mode dominance and the reduction to two families -/

/-- SC11: replacing the final mode by one of no smaller terminal mass cannot increase the
one-switch error. The initial deficit is unchanged, the final deficit decreases, and the
omitted mass cannot increase, because the newly omitted mode `q` has no larger mass than the
mode `q'` removed from the omitted set. -/
theorem D_oneSwitch_mono_masses {A : Fin n → ℝ → ℝ} {T τ : ℝ} {p q q' : Fin n}
    (hA : IsCumulative A T) (hpq : p ≠ q) (hpq' : p ≠ q')
    (hm : masses A T q ≤ masses A T q') (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) :
    D A (oneSwitch p q' τ T) T ≤ D A (oneSwitch p q τ T) T := by
  rw [D_oneSwitch hA hpq' hτ0 hτT, D_oneSwitch hA hpq hτ0 hτT]
  refine max_le_max ?_ (max_le_max le_rfl ?_)
  · refine omittedMass_le (omittedMass_nonneg p q) fun i hip hiq' => ?_
    rcases eq_or_ne i q with rfl | hiq
    · exact hm.trans (masses_le_omittedMass (Ne.symm hpq') (Ne.symm hiq'))
    · exact masses_le_omittedMass hip hiq
  · simp only [finalDeficit]
    linarith

/-- SC11, the form used downstream: a mode of largest terminal mass among the modes other
than the initial mode `p` is an optimal final mode. -/
theorem D_oneSwitch_le_of_max_mass {A : Fin n → ℝ → ℝ} {T τ : ℝ} {p q q' : Fin n}
    (hA : IsCumulative A T) (hpq : p ≠ q) (hpq' : p ≠ q')
    (hmax : ∀ i, i ≠ p → masses A T i ≤ masses A T q') (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) :
    D A (oneSwitch p q' τ T) T ≤ D A (oneSwitch p q τ T) T :=
  D_oneSwitch_mono_masses hA hpq hpq' (hmax q (Ne.symm hpq)) hτ0 hτT

/-- SC11, the reduction of `thm:linear-one-switch` and of the proof of `thm:finite-one`: if
`h₁` carries a largest terminal mass and `h₂` a largest mass among the modes other than `h₁`,
then at every switch time every one-switch schedule is dominated either by `h₁ → h₂` or by
`p → h₁` with the same initial mode `p ≠ h₁`. -/
theorem oneSwitch_reduction {A : Fin n → ℝ → ℝ} {T τ : ℝ} {h₁ h₂ p q : Fin n}
    (hA : IsCumulative A T) (hmax₁ : ∀ i, masses A T i ≤ masses A T h₁)
    (hmax₂ : ∀ i, i ≠ h₁ → masses A T i ≤ masses A T h₂) (h₁₂ : h₁ ≠ h₂) (hpq : p ≠ q)
    (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) :
    D A (oneSwitch h₁ h₂ τ T) T ≤ D A (oneSwitch p q τ T) T ∨
      (p ≠ h₁ ∧ D A (oneSwitch p h₁ τ T) T ≤ D A (oneSwitch p q τ T) T) := by
  by_cases hph : p = h₁
  · subst hph
    exact Or.inl (D_oneSwitch_le_of_max_mass hA hpq h₁₂ hmax₂ hτ0 hτT)
  · exact Or.inr ⟨hph,
      D_oneSwitch_le_of_max_mass hA hpq hph (fun i _ => hmax₁ i) hτ0 hτT⟩

/-- Every one-switch schedule competes in the one-switch instance optimum, so `OPT A T 1` is
below the error of each of the candidates produced by `oneSwitch_reduction`. -/
theorem OPT_le_D_oneSwitch {A : Fin n → ℝ → ℝ} {T τ : ℝ} (hA : IsCumulative A T) (p q : Fin n)
    (hτ0 : 0 ≤ τ) (hτT : τ ≤ T) : OPT A T 1 ≤ D A (oneSwitch p q τ T) T := by
  have hn : 0 < n := pos_of_mode p
  refine csInf_le ⟨0, ?_⟩ ⟨oneSwitch p q τ T, isSchedule_oneSwitch hτ0 hτT p q, rfl⟩
  rintro e ⟨W, hW, rfl⟩
  exact D_nonneg hn hA hW.isCumulative (hτ0.trans hτT)

end GridSwitching
