import Formal.ReciprocalAnchor.ManyFastEvaluation

/-! The actual outer lines of the constructed envelope stack. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

theorem affine_nonneg_right_slope {c d T : ℝ}
    (h : ∀ x : ℝ, T ≤ x → 0 ≤ c + d * x) : 0 ≤ d := by
  by_contra hd
  have hd' : 0 < -d := by linarith
  let x := max T ((c + 1) / (-d))
  have hh := h x (le_max_left _ _)
  have hx : (c + 1) / (-d) ≤ x := le_max_right _ _
  have hm := (div_le_iff₀ hd').mp hx
  nlinarith

theorem affine_nonneg_left_slope {c d T : ℝ}
    (h : ∀ x : ℝ, x ≤ T → 0 ≤ c + d * x) : d ≤ 0 := by
  have hh : 0 ≤ -d := affine_nonneg_right_slope (T := -T) (c := c) (d := -d) (by
    intro y hy
    have hz := h (-y) (by linarith)
    nlinarith)
  linarith

theorem good_head_eventually (c : Line) (cs : List Line) (hg : Good (c :: cs)) :
    ∃ T : ℝ, ∀ x : ℝ, T ≤ x → ∀ l ∈ c :: cs, l.evalReal x ≤ c.evalReal x := by
  cases cs with
  | nil =>
    refine ⟨0, ?_⟩
    intro x hx l hl
    simp only [List.mem_singleton] at hl
    subst l
    exact le_rfl
  | cons a rest =>
    refine ⟨cross a c, ?_⟩
    intro x hx l hl
    rcases List.mem_cons.mp hl with he | hl
    · subst l; exact le_rfl
    · exact head_dominates hg x hx l hl

theorem good_last_eventually (c : Line) (cs : List Line) (hg : Good (c :: cs)) :
    ∃ T : ℝ, ∀ x : ℝ, x ≤ T → ∀ l ∈ c :: cs,
      l.evalReal x ≤ ((c :: cs).getLast (by simp)).evalReal x := by
  induction cs generalizing c with
  | nil =>
    refine ⟨0, ?_⟩
    intro x hx l hl
    simp only [List.mem_singleton] at hl
    subst l
    exact le_rfl
  | cons a rest ih =>
    obtain ⟨T, ht⟩ := ih a (good_tail c _ hg)
    refine ⟨min T (cross a c), ?_⟩
    intro x hx l hl
    have hT := hx.trans (min_le_left _ _)
    have hcross := hx.trans (min_le_right _ _)
    simp only [List.getLast_cons_cons]
    rcases List.mem_cons.mp hl with he | hl
    · subst l
      exact ((reverse_eval_le_iff_real (good_pair_slope hg) x).2 hcross).trans
        (ht x hT a List.mem_cons_self)
    · exact ht x hT l hl

/-- Membership bounds plus actual domination of the zero line force the retained
rightmost line to be exactly zero, including its intercept. -/
theorem buildStack_head_zero (input : List Line) (b : ℚ)
    (hz : (⟨0, 0⟩ : Line) ∈ input)
    (hb : ∀ l ∈ input, l.slope ≤ 0 ∧ l.evalReal b ≤ 0)
    {c : Line} {cs : List Line} (hc : (buildStack input).1 = c :: cs) : c = ⟨0, 0⟩ := by
  have hm : c ∈ input := buildStack_members input (by rw [hc]; simp)
  have hg : Good (c :: cs) := hc ▸ buildStack_good input
  obtain ⟨T, ht⟩ := good_head_eventually c cs hg
  have hnonneg : ∀ x : ℝ, T ≤ x → 0 ≤ c.evalReal x := by
    intro x hx
    obtain ⟨l, hl, hle⟩ := buildStack_dominates input x _ hz
    rw [hc] at hl
    have he := hle.trans (ht x hx l hl)
    simpa [Line.evalReal] using he
  have hs : c.slope = 0 := by
    have hs0 : (0 : ℝ) ≤ c.slope := affine_nonneg_right_slope (by
      intro x hx; exact hnonneg x hx)
    have hs1 : (c.slope : ℝ) ≤ 0 := by exact_mod_cast (hb c hm).1
    exact_mod_cast le_antisymm hs1 hs0
  have hi : c.intercept = 0 := by
    have h0 := hnonneg T le_rfl
    have h1 := (hb c hm).2
    simp only [Line.evalReal, hs, Rat.cast_zero, zero_mul, add_zero] at h0 h1
    exact_mod_cast le_antisymm h1 h0
  cases c
  simp_all

/-- The retained leftmost line is the original mean-minus-argument baseline. -/
theorem buildStack_last_mean (input : List Line) (a m : ℚ)
    (hz : (⟨-1, m⟩ : Line) ∈ input)
    (hb : ∀ l ∈ input, -1 ≤ l.slope ∧ l.evalReal a ≤ (m : ℝ) - a)
    {c : Line} {cs : List Line} (hc : (buildStack input).1 = c :: cs) :
    (c :: cs).getLast (by simp) = ⟨-1, m⟩ := by
  let last := (c :: cs).getLast (by simp)
  have hm : last ∈ input := buildStack_members input (by rw [hc]; exact List.getLast_mem _)
  have hg : Good (c :: cs) := hc ▸ buildStack_good input
  obtain ⟨T, ht⟩ := good_last_eventually c cs hg
  have hnonneg : ∀ x : ℝ, x ≤ T → (m : ℝ) - x ≤ last.evalReal x := by
    intro x hx
    obtain ⟨l, hl, hle⟩ := buildStack_dominates input x _ hz
    rw [hc] at hl
    have he := hle.trans (ht x hx l hl)
    simpa [Line.evalReal, sub_eq_add_neg] using he
  have hs : last.slope = -1 := by
    have hs0 : (last.slope : ℝ) + 1 ≤ 0 := affine_nonneg_left_slope (c := last.intercept - m) (by
      intro x hx
      have he := hnonneg x hx
      dsimp [Line.evalReal] at he
      nlinarith)
    have hs1 : (-1 : ℝ) ≤ last.slope := by exact_mod_cast (hb last hm).1
    have hs2 : (last.slope : ℝ) = -1 := by linarith
    exact_mod_cast hs2
  have hi : last.intercept = m := by
    have h0 := hnonneg T le_rfl
    have h1 := (hb last hm).2
    simp only [Line.evalReal, hs, Rat.cast_neg, Rat.cast_one, neg_mul, one_mul] at h0 h1
    have he : (last.intercept : ℝ) = m := by linarith
    exact_mod_cast he
  change last = _
  cases he : last with
  | mk sl i =>
    rw [he] at hs hi
    simp only at hs hi
    simp [hs, hi]

theorem sourceLines_mean {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) :
    (⟨-1, m⟩ : Line) ∈ sourceLines m q w := by
  apply List.mem_ofFn.mpr
  refine ⟨⟨2 * n + 1, by omega⟩, ?_⟩
  simp [rationalLines, show ¬ 2 * n + 1 < n by omega,
    show ¬ 2 * n + 1 < 2 * n by omega]

theorem sourceLines_slope_bounds {n : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1) {l : Line} (hl : l ∈ sourceLines m q w) :
    -1 ≤ l.slope ∧ l.slope ≤ 0 := by
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hl
  have hq' : ∀ j, (0 : ℝ) ≤ q j ∧ (q j : ℝ) ≤ 1 := by
    intro j; exact_mod_cast hq j
  have hb := lineSlope_bounds (m := (m : ℝ)) (w := fun j => (w j : ℝ)) hq' i
  have he : lineSlope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) i =
      (-(rationalLines m q w i).negSlope : ℚ) := by
    rw [lineSlope, ← sourceLine_eval, ← sourceLine_eval]
    simp [Line.evalReal]
  rw [he] at hb
  exact_mod_cast hb

theorem sourceStack_head_zero {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    {c : Line} {cs : List Line} (hc : (buildStack (sourceLines m q w)).1 = c :: cs) :
    c = ⟨0, 0⟩ := by
  apply buildStack_head_zero (sourceLines m q w) b (sourceLines_zero m q w) ?_ hc
  intro l hl
  have hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1 := by
    intro j
    exact_mod_cast (show (0 : ℝ) ≤ q j ∧ (q j : ℝ) ≤ 1 from
      ⟨(h.2.2 j).1, (h.2.2 j).2.1⟩)
  refine ⟨(sourceLines_slope_bounds hq hl).2, ?_⟩
  have he := evalReal_le_valueReal hl (b : ℝ)
  rw [sourceLines_valueReal, envelope_right h le_rfl] at he
  exact he

theorem sourceStack_last_mean {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    {c : Line} {cs : List Line} (hc : (buildStack (sourceLines m q w)).1 = c :: cs) :
    (c :: cs).getLast (by simp) = ⟨-1, m⟩ := by
  apply buildStack_last_mean (sourceLines m q w) a m (sourceLines_mean m q w) ?_ hc
  intro l hl
  have hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1 := by
    intro j
    exact_mod_cast (show (0 : ℝ) ≤ q j ∧ (q j : ℝ) ≤ 1 from
      ⟨(h.2.2 j).1, (h.2.2 j).2.1⟩)
  refine ⟨(sourceLines_slope_bounds hq hl).1, ?_⟩
  have he := evalReal_le_valueReal hl (a : ℝ)
  rw [sourceLines_valueReal, envelope_left h le_rfl] at he
  exact he

end ReciprocalAnchor.ManyLeaf.FastEnvelope
