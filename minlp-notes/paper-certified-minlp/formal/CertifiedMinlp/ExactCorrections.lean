import CertifiedMinlp.SafeCuts

/-! Exact coordinate suprema. Unbounded corrections are represented by failure
of `BddAbove`, never by a real-valued infinity. -/
namespace CertifiedMinlp

def shiftValues (B : Coordinate) (z d : ℝ) : Set ℝ :=
  (fun x => d * (z - x)) '' {x | B.contains x}

def Coordinate.finiteShift (B : Coordinate) (d : ℝ) : Prop :=
  match B with
  | .bounded _ _ => True
  | .lowerBounded _ => 0 ≤ d
  | .upperBounded _ => d ≤ 0
  | .free => d = 0

def Coordinate.exactShift (B : Coordinate) (z d : ℝ) : ℝ :=
  match B with
  | .bounded L U => max (d * (z - L)) (d * (z - U))
  | .lowerBounded L => d * (z - L)
  | .upperBounded U => d * (z - U)
  | .free => 0

theorem exactShift_isGreatest (B : Coordinate) (z d : ℝ)
    (hz : B.contains z) (hf : B.finiteShift d) :
    IsGreatest (shiftValues B z d) (B.exactShift z d) := by
  constructor
  · cases B with
    | bounded L U =>
      change (L : ℝ) ≤ z ∧ z ≤ (U : ℝ) at hz
      rcases le_total (d * (z - (L : ℝ))) (d * (z - (U : ℝ))) with h | h
      · exact ⟨U, ⟨le_trans hz.1 hz.2, le_rfl⟩, (max_eq_right h).symm⟩
      · exact ⟨L, ⟨le_rfl, le_trans hz.1 hz.2⟩, (max_eq_left h).symm⟩
    | lowerBounded L => exact ⟨(L : ℝ), by change (L : ℝ) ≤ L; rfl, rfl⟩
    | upperBounded U => exact ⟨(U : ℝ), by change (U : ℝ) ≤ U; rfl, rfl⟩
    | free => exact ⟨z, trivial, by simp [Coordinate.exactShift]⟩
  · rintro _ ⟨x, hx, rfl⟩
    cases B with
    | bounded L U =>
      exact bounded_shift_le L U z x d d d hx.1 hx.2 hz.1 hz.2 le_rfl le_rfl
    | lowerBounded L => exact lower_shift_le L z x d d d hx hz hf le_rfl le_rfl
    | upperBounded U => exact upper_shift_le U z x d d d hx hz hf le_rfl le_rfl
    | free => simp only [Coordinate.finiteShift] at hf; simp [hf, Coordinate.exactShift]

theorem exactShift_nonneg (B : Coordinate) (z d : ℝ)
    (hz : B.contains z) (hf : B.finiteShift d) : 0 ≤ B.exactShift z d := by
  apply (exactShift_isGreatest B z d hz hf).2
  exact ⟨z, hz, by ring⟩

theorem lower_shift_unbounded (L z d M : ℝ) (hz : L ≤ z) (hd : d < 0) :
    ∃ x, L ≤ x ∧ M < d * (z - x) := by
  refine ⟨z + (|M| + 1) / (-d), ?_, ?_⟩
  · have hp : 0 ≤ (|M| + 1) / (-d) := div_nonneg (by positivity) (by linarith)
    linarith
  · have hid : d * (z - (z + (|M| + 1) / (-d))) = |M| + 1 := by
      field_simp [ne_of_lt hd]
      ring
    rw [hid]
    linarith [le_abs_self M]

theorem upper_shift_unbounded (U z d M : ℝ) (hz : z ≤ U) (hd : 0 < d) :
    ∃ x, x ≤ U ∧ M < d * (z - x) := by
  refine ⟨z - (|M| + 1) / d, ?_, ?_⟩
  · have hp : 0 ≤ (|M| + 1) / d := div_nonneg (by positivity) hd.le
    linarith
  · have hid : d * (z - (z - (|M| + 1) / d)) = |M| + 1 := by
      field_simp [ne_of_gt hd]
      ring
    rw [hid]
    linarith [le_abs_self M]

theorem shiftValues_bddAbove_iff (B : Coordinate) (z d : ℝ)
    (hz : B.contains z) : BddAbove (shiftValues B z d) ↔ B.finiteShift d := by
  constructor
  · rintro ⟨M, hM⟩
    cases B with
    | bounded L U => trivial
    | lowerBounded L =>
      by_contra h
      have hd : d < 0 := lt_of_not_ge h
      obtain ⟨x, hx, hlt⟩ := lower_shift_unbounded L z d M hz hd
      exact (not_lt_of_ge (hM ⟨x, hx, rfl⟩)) hlt
    | upperBounded U =>
      by_contra h
      have hd : 0 < d := lt_of_not_ge h
      obtain ⟨x, hx, hlt⟩ := upper_shift_unbounded U z d M hz hd
      exact (not_lt_of_ge (hM ⟨x, hx, rfl⟩)) hlt
    | free =>
      change d = 0
      rcases lt_trichotomy d 0 with hd | hd | hd
      · obtain ⟨x, _, hlt⟩ := lower_shift_unbounded z z d M le_rfl hd
        exact False.elim ((not_lt_of_ge (hM ⟨x, trivial, rfl⟩)) hlt)
      · exact hd
      · obtain ⟨x, _, hlt⟩ := upper_shift_unbounded z z d M le_rfl hd
        exact False.elim ((not_lt_of_ge (hM ⟨x, trivial, rfl⟩)) hlt)
  · intro hf
    exact ⟨B.exactShift z d, (exactShift_isGreatest B z d hz hf).2⟩

theorem coordinate_supremum_eq (B : Coordinate) (z d : ℝ)
    (hz : B.contains z) (hf : B.finiteShift d) :
    sSup (shiftValues B z d) = B.exactShift z d :=
  (exactShift_isGreatest B z d hz hf).csSup_eq

theorem safe_affine_of_coordinate_suprema {ι : Type*} [Fintype ι]
    (B : ι → Coordinate) (g : (ι → ℝ) → ℝ) (q a p z : ι → ℝ) (c b : ℝ)
    (hz : boxContains B z)
    (hf : ∀ j, (B j).finiteShift (p j + q j - a j))
    (hsupport : ∀ x, boxContains B x → g z + dot p (fun j => x j - z j) ≤ g x)
    (hb : b ≤ g z + dot q z + c - dot a z -
      ∑ j, sSup (shiftValues (B j) (z j) (p j + q j - a j))) :
    ∀ x, boxContains B x → affine a b x ≤ g x + dot q x + c := by
  intro x hx
  apply safe_affine_of_shift_bounds g q a p z x
    (fun j => sSup (shiftValues (B j) (z j) (p j + q j - a j))) c b
    (hsupport x hx) _ hb
  intro j
  rw [coordinate_supremum_eq (B j) (z j) _ (hz j) (hf j)]
  exact (exactShift_isGreatest (B j) (z j) _ (hz j) (hf j)).2 ⟨x j, hx j, rfl⟩

/-- A directed lower enclosure of the full intercept expression can be used
without assuming that its interval evaluation is exact. -/
theorem safe_affine_of_intercept_enclosure {ι : Type*} [Fintype ι]
    (B : ι → Coordinate) (g : (ι → ℝ) → ℝ) (q a p z : ι → ℝ) (c b v : ℝ)
    (hz : boxContains B z)
    (hf : ∀ j, (B j).finiteShift (p j + q j - a j))
    (hsupport : ∀ x, boxContains B x → g z + dot p (fun j => x j - z j) ≤ g x)
    (hv : v ≤ g z + dot q z + c - dot a z -
      ∑ j, sSup (shiftValues (B j) (z j) (p j + q j - a j)))
    (hb : b ≤ v) :
    ∀ x, boxContains B x → affine a b x ≤ g x + dot q x + c :=
  safe_affine_of_coordinate_suprema B g q a p z c b hz hf hsupport (hb.trans hv)

theorem lower_directed_slope (L : ℚ) (p q a lo : ℝ)
    (hlo : lo ≤ p + q) (ha : a ≤ lo) :
    (Coordinate.lowerBounded L).finiteShift (p + q - a) := by
  change 0 ≤ p + q - a
  linarith

theorem upper_directed_slope (U : ℚ) (p q a hi : ℝ)
    (hhi : p + q ≤ hi) (ha : hi ≤ a) :
    (Coordinate.upperBounded U).finiteShift (p + q - a) := by
  change p + q - a ≤ 0
  linarith

theorem free_matched_slope (p q : ℝ) :
    Coordinate.free.finiteShift (p + q - (p + q)) := by
  simp [Coordinate.finiteShift]

end CertifiedMinlp
