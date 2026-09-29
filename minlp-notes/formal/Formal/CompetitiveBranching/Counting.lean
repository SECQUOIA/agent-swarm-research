import Formal.CompetitiveBranching.Lemmas

/-!
# Counting split points of a minimizer-rule tree

All statements concern a `MinRule` tree on a node interval `[l, u]` on which
`m > 0`. For a valid interval `[a, b]` with `a < b`, the number of internal
nodes whose split point lies in `(a, b)` is

* `0` if neither `a` nor `b` is interior to `[l, u]` (`count_zero_of_out`);
* at most `1` if `b` is not interior (`count_le_one_of_right_out`);
* at most `1` if `a` is not interior (`count_le_one_of_left_out`);
* at most `3` in general (`count_le_three`).

The two one-sided bounds use Lemma 2 through `count_left_zero` and
`count_right_zero`. Each point is a split point at most once
(`count_eq_le_one`, Lemma 1(ii)).
-/

open Set

noncomputable section

namespace CompetitiveBranching

variable {m : ℝ → ℝ} {α : ℝ}

namespace Tree

theorem count_node_of {p : ℝ → Prop} {y : ℝ} {tl tr : Tree} (h : p y) :
    (node y tl tr).count p = 1 + tl.count p + tr.count p := by
  simp [count, h]

theorem count_node_of_not {p : ℝ → Prop} {y : ℝ} {tl tr : Tree} (h : ¬ p y) :
    (node y tl tr).count p = tl.count p + tr.count p := by
  simp [count, h]

/-- A count for `p` is at most the sum of the counts for `q₁` and `q₂` when
`p` implies `q₁ ∨ q₂`. -/
theorem count_le_add {p q₁ q₂ : ℝ → Prop} (h : ∀ y, p y → q₁ y ∨ q₂ y) (t : Tree) :
    t.count p ≤ t.count q₁ + t.count q₂ := by
  classical
  induction t with
  | leaf => simp [count]
  | node y tl tr ihl ihr =>
    have hy : (node y leaf leaf).count p ≤
        (node y leaf leaf).count q₁ + (node y leaf leaf).count q₂ := by
      by_cases hp : p y
      · rcases h y hp with h1 | h1 <;> simp [count, hp, h1]
      · simp [count, hp]
    simp only [count] at hy ⊢
    omega

end Tree

theorem pos_left {l u y : ℝ} (hpos : ∀ z ∈ Icc l u, 0 < m z) (hyu : y ≤ u) :
    ∀ z ∈ Icc l y, 0 < m z :=
  fun z hz => hpos z ⟨hz.1, hz.2.trans hyu⟩

theorem pos_right {l u y : ℝ} (hpos : ∀ z ∈ Icc l u, 0 < m z) (hly : l ≤ y) :
    ∀ z ∈ Icc y u, 0 < m z :=
  fun z hz => hpos z ⟨hly.trans hz.1, hz.2⟩

/-- Split points of a minimizer-rule tree lie in the open node interval. -/
theorem count_eq_zero_of_forall {p : ℝ → Prop} :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      (∀ y ∈ Ioo l u, ¬ p y) → t.count p = 0 := by
  intro t
  induction t with
  | leaf => intros; rfl
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos hp
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    rw [Tree.count_node_of_not (hp y ⟨hly, hyu⟩),
      ihl l y htl (pos_left hpos hy.2) (fun z hz => hp z ⟨hz.1, hz.2.trans hyu⟩),
      ihr y u htr (pos_right hpos hy.1) (fun z hz => hp z ⟨hly.trans hz.1, hz.2⟩)]

/-- Lemma 1(ii): every point is the split point of at most one internal node. -/
theorem count_eq_le_one (c : ℝ) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      t.count (· = c) ≤ 1 := by
  intro t
  induction t with
  | leaf => intros; simp [Tree.count]
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    rcases lt_trichotomy c y with h | rfl | h
    · rw [Tree.count_node_of_not (p := (· = c)) h.ne',
        count_eq_zero_of_forall tr y u htr (pos_right hpos hy.1)
          (fun z hz hzc => (h.trans hz.1).ne' hzc)]
      simpa using ihl l y htl (pos_left hpos hy.2)
    · rw [Tree.count_node_of (p := (· = c)) rfl,
        count_eq_zero_of_forall tl l c htl (pos_left hpos hy.2)
          (fun z hz hzc => hz.2.ne hzc),
        count_eq_zero_of_forall tr c u htr (pos_right hpos hy.1)
          (fun z hz hzc => hz.1.ne' hzc)]
    · rw [Tree.count_node_of_not (p := (· = c)) h.ne,
        count_eq_zero_of_forall tl l y htl (pos_left hpos hy.2)
          (fun z hz hzc => (hz.2.trans h).ne hzc)]
      simpa using ihr y u htr (pos_right hpos hy.1)

variable {a b : ℝ}

/-- Lemma 1(iii): if neither `a` nor `b` is interior to the node interval,
no split point lies in `(a, b)`. A node inside `[a, b]` would be valid. -/
theorem count_zero_of_out (hα : 0 < α) (hJ : Valid m α a b) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      a ∉ Ioo l u → b ∉ Ioo l u → t.count (· ∈ Ioo a b) = 0 := by
  intro t
  induction t with
  | leaf => intros; rfl
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos ha hb
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    have hyab : y ∉ Ioo a b := by
      rintro ⟨hay, hyb⟩
      apply hnv
      refine hJ.mono hα.le ?_ ?_
      · exact not_lt.mp fun h => ha ⟨h, hay.trans hyu⟩
      · exact not_lt.mp fun h => hb ⟨hly.trans hyb, h⟩
    rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab,
      ihl l y htl (pos_left hpos hy.2) (fun h => ha (Ioo_subset_Ioo_right hy.2 h))
        (fun h => hb (Ioo_subset_Ioo_right hy.2 h)),
      ihr y u htr (pos_right hpos hy.1) (fun h => ha (Ioo_subset_Ioo_left hy.1 h))
        (fun h => hb (Ioo_subset_Ioo_left hy.1 h))]

/-- Lemma 2 applied along a subtree: if an internal node on `[l₁, u₁]` with
`u₁ ≤ b` splits at `y₁ < b`, then no node of its left subtree splits in
`(a, b)`. -/
theorem count_left_zero (hα : 0 < α) (hJ : Valid m α a b) {l₁ y₁ u₁ : ℝ}
    (hmin₁ : IsMinOn (phi m α l₁ u₁) (Icc l₁ u₁) y₁) (hy₁u : y₁ ≤ u₁)
    (hy₁b : y₁ < b) (hub : u₁ ≤ b) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      l₁ ≤ l → u ≤ y₁ → t.count (· ∈ Ioo a b) = 0 := by
  intro t
  induction t with
  | leaf => intros; rfl
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos hl hu
    obtain ⟨hneg, hly, hyu⟩ := node_facts hpos hnv hy hmin
    have hyab : y ∉ Ioo a b := fun hyab =>
      not_lt.mpr hub
        (key_left hα hmin₁ hy₁u hl hy.1 hy.2 hu hneg hJ hyab.1 (hyu.trans_le hu) hy₁b)
    rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab,
      ihl l y htl (pos_left hpos hy.2) hl (hy.2.trans hu),
      ihr y u htr (pos_right hpos hy.1) (hl.trans hy.1) hu]

/-- Mirror of `count_left_zero`: if an internal node on `[l₁, u₁]` with
`a ≤ l₁` splits at `y₁ > a`, then no node of its right subtree splits in
`(a, b)`. -/
theorem count_right_zero (hα : 0 < α) (hJ : Valid m α a b) {l₁ y₁ u₁ : ℝ}
    (hmin₁ : IsMinOn (phi m α l₁ u₁) (Icc l₁ u₁) y₁) (hly₁ : l₁ ≤ y₁)
    (hay₁ : a < y₁) (hal : a ≤ l₁) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      y₁ ≤ l → u ≤ u₁ → t.count (· ∈ Ioo a b) = 0 := by
  intro t
  induction t with
  | leaf => intros; rfl
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos hl hu
    obtain ⟨hneg, hly, hyu⟩ := node_facts hpos hnv hy hmin
    have hyab : y ∉ Ioo a b := fun hyab =>
      not_lt.mpr hal
        (key_right hα hmin₁ hly₁ hl hy.1 hy.2 hu hneg hJ hay₁ (hl.trans_lt hly) hyab.2)
    rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab,
      ihl l y htl (pos_left hpos hy.2) hl (hy.2.trans hu),
      ihr y u htr (pos_right hpos hy.1) (hl.trans hy.1) hu]

/-- If `b` is not interior to the node interval, at most one split point lies
in `(a, b)` (the class `Y^L` of the note has at most one element). -/
theorem count_le_one_of_right_out (hα : 0 < α) (hab : a < b) (hJ : Valid m α a b) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      b ∉ Ioo l u → t.count (· ∈ Ioo a b) ≤ 1 := by
  intro t
  induction t with
  | leaf => intros; simp [Tree.count]
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos hb
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    by_cases hyab : y ∈ Ioo a b
    · have hub : u ≤ b := not_lt.mp fun h => hb ⟨hly.trans hyab.2, h⟩
      rw [Tree.count_node_of (p := (· ∈ Ioo a b)) hyab,
        count_left_zero hα hJ hmin hy.2 hyab.2 hub tl l y htl (pos_left hpos hy.2)
          le_rfl le_rfl,
        count_zero_of_out hα hJ tr y u htr (pos_right hpos hy.1)
          (fun h => lt_asymm h.1 hyab.1) (fun h => not_lt.mpr hub h.2)]
    · rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab]
      rcases not_and_or.mp hyab with hya | hyb
      · replace hya := not_lt.mp hya
        rw [count_zero_of_out hα hJ tl l y htl (pos_left hpos hy.2)
          (fun h => not_lt.mpr hya h.2) (fun h => not_lt.mpr (hya.trans hab.le) h.2)]
        simpa using ihr y u htr (pos_right hpos hy.1)
          (fun h => hb (Ioo_subset_Ioo_left hy.1 h))
      · replace hyb := not_lt.mp hyb
        have hbl : b ≤ l := not_lt.mp fun h => hb ⟨h, hyb.trans_lt hyu⟩
        rw [count_zero_of_out hα hJ tl l y htl (pos_left hpos hy.2)
          (fun h => not_lt.mpr (hab.le.trans hbl) h.1) (fun h => not_lt.mpr hbl h.1)]
        simpa using ihr y u htr (pos_right hpos hy.1) (fun h => not_lt.mpr hyb h.1)

/-- If `a` is not interior to the node interval, at most one split point lies
in `(a, b)` (the class `Y^R` of the note has at most one element). -/
theorem count_le_one_of_left_out (hα : 0 < α) (hab : a < b) (hJ : Valid m α a b) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      a ∉ Ioo l u → t.count (· ∈ Ioo a b) ≤ 1 := by
  intro t
  induction t with
  | leaf => intros; simp [Tree.count]
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos ha
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    by_cases hyab : y ∈ Ioo a b
    · have hal : a ≤ l := not_lt.mp fun h => ha ⟨h, hyab.1.trans hyu⟩
      rw [Tree.count_node_of (p := (· ∈ Ioo a b)) hyab,
        count_right_zero hα hJ hmin hy.1 hyab.1 hal tr y u htr (pos_right hpos hy.1)
          le_rfl le_rfl,
        count_zero_of_out hα hJ tl l y htl (pos_left hpos hy.2)
          (fun h => not_lt.mpr hal h.1) (fun h => lt_asymm h.2 hyab.2)]
    · rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab]
      rcases not_and_or.mp hyab with hya | hyb
      · replace hya := not_lt.mp hya
        have hua : u ≤ a := not_lt.mp fun h => ha ⟨hly.trans_le hya, h⟩
        rw [count_zero_of_out hα hJ tr y u htr (pos_right hpos hy.1)
          (fun h => not_lt.mpr hua h.2) (fun h => not_lt.mpr (hua.trans hab.le) h.2)]
        simpa using ihl l y htl (pos_left hpos hy.2)
          (fun h => ha (Ioo_subset_Ioo_right hy.2 h))
      · replace hyb := not_lt.mp hyb
        rw [count_zero_of_out hα hJ tr y u htr (pos_right hpos hy.1)
          (fun h => not_lt.mpr (hab.le.trans hyb) h.1) (fun h => not_lt.mpr hyb h.1)]
        simpa using ihl l y htl (pos_left hpos hy.2)
          (fun h => ha (Ioo_subset_Ioo_right hy.2 h))

/-- At most three split points lie in `(a, b)`: one node containing both
endpoints in its interior (`Y^LR`), and one from each one-sided class. -/
theorem count_le_three (hα : 0 < α) (hab : a < b) (hJ : Valid m α a b) :
    ∀ (t : Tree) (l u : ℝ), MinRule m α l u t → (∀ z ∈ Icc l u, 0 < m z) →
      t.count (· ∈ Ioo a b) ≤ 3 := by
  intro t
  induction t with
  | leaf => intros; simp [Tree.count]
  | node y tl tr ihl ihr =>
    rintro l u ⟨hnv, hy, hmin, htl, htr⟩ hpos
    obtain ⟨-, hly, hyu⟩ := node_facts hpos hnv hy hmin
    by_cases hyab : y ∈ Ioo a b
    · rw [Tree.count_node_of (p := (· ∈ Ioo a b)) hyab]
      have h1 := count_le_one_of_right_out hα hab hJ tl l y htl (pos_left hpos hy.2)
        (fun h => lt_asymm h.2 hyab.2)
      have h2 := count_le_one_of_left_out hα hab hJ tr y u htr (pos_right hpos hy.1)
        (fun h => lt_asymm h.1 hyab.1)
      omega
    · rw [Tree.count_node_of_not (p := (· ∈ Ioo a b)) hyab]
      rcases not_and_or.mp hyab with hya | hyb
      · replace hya := not_lt.mp hya
        rw [count_zero_of_out hα hJ tl l y htl (pos_left hpos hy.2)
          (fun h => not_lt.mpr hya h.2) (fun h => not_lt.mpr (hya.trans hab.le) h.2)]
        simpa using ihr y u htr (pos_right hpos hy.1)
      · replace hyb := not_lt.mp hyb
        rw [count_zero_of_out hα hJ tr y u htr (pos_right hpos hy.1)
          (fun h => not_lt.mpr (hab.le.trans hyb) h.1) (fun h => not_lt.mpr hyb h.1)]
        simpa using ihl l y htl (pos_left hpos hy.2)

end CompetitiveBranching
