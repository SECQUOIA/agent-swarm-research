import Formal.ReciprocalAnchor.ManyFastDominance

/-! Executable positive slope jumps of the computed global envelope stack. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

structure Atom where
  mass : ℚ
  location : ℚ
  deriving DecidableEq, Repr

/-- One strictly positive atom per pair of consecutive envelope lines. -/
def slopeAtoms : List Line → List Atom
  | [] => []
  | [_] => []
  | c :: d :: rest => ⟨c.slope - d.slope, cross d c⟩ :: slopeAtoms (d :: rest)

def atomCall (atoms : List Atom) (s : ℝ) : ℝ :=
  (atoms.map (fun a => (a.mass : ℝ) * max ((a.location : ℝ) - s) 0)).sum

/-- The actual maximum, without adjoining an artificial zero line. -/
def peak : List Line → ℝ → ℝ
  | [], _ => 0
  | [c], x => c.evalReal x
  | c :: d :: rest, x => max (c.evalReal x) (peak (d :: rest) x)

theorem slopeAtoms_length (stack : List Line) :
    (slopeAtoms stack).length = stack.length - 1 := by
  induction stack using slopeAtoms.induct with
  | case1 => rfl
  | case2 c => rfl
  | case3 c d rest ih =>
    simp only [slopeAtoms, List.length_cons] at *
    omega

theorem slopeAtoms_positive (stack : List Line) (hg : Good stack)
    {a : Atom} (ha : a ∈ slopeAtoms stack) : 0 < a.mass := by
  induction stack using slopeAtoms.induct with
  | case1 => simp [slopeAtoms] at ha
  | case2 c => simp [slopeAtoms] at ha
  | case3 c d rest ih =>
    simp only [slopeAtoms, List.mem_cons] at ha
    rcases ha with he | ha
    · subst a; exact sub_pos.mpr (good_pair_slope hg)
    · exact ih (good_tail c _ hg) ha

theorem peak_valueReal (stack : List Line) (hne : stack ≠ []) (x : ℝ) :
    valueReal stack x = max (peak stack x) 0 := by
  induction stack using slopeAtoms.induct with
  | case1 => contradiction
  | case2 c => rfl
  | case3 c d rest ih =>
    change max (c.evalReal x) (valueReal (d :: rest) x) =
      max (max (c.evalReal x) (peak (d :: rest) x)) 0
    rw [ih (by simp), max_assoc]

/-- Every remaining knot is below the immediately preceding knot. -/
theorem slopeAtoms_location_le {c d : Line} {rest : List Line}
    (hg : Good (c :: d :: rest)) {a : Atom} (ha : a ∈ slopeAtoms (d :: rest)) :
    a.location ≤ cross d c := by
  induction rest generalizing c d with
  | nil => simp [slopeAtoms] at ha
  | cons e rest ih =>
    simp only [slopeAtoms, List.mem_cons] at ha
    rcases ha with he | ha
    · subst a; exact (good_cross hg).le
    · exact (ih hg.2.2 ha).trans (good_cross hg).le

theorem atomCall_zero_of_right (stack : List Line) (s : ℝ)
    (hr : ∀ a ∈ slopeAtoms stack, (a.location : ℝ) ≤ s) : atomCall (slopeAtoms stack) s = 0 := by
  unfold atomCall
  apply List.sum_eq_zero
  intro z hz
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hz
  rw [max_eq_right (sub_nonpos.mpr (hr a ha)), mul_zero]

theorem cross_identity {c d : Line} (hdc : d.slope < c.slope) (x : ℝ) :
    ((c.slope - d.slope : ℚ) : ℝ) * ((cross d c : ℝ) - x) =
      d.evalReal x - c.evalReal x := by
  have hn : (c.slope : ℝ) - d.slope ≠ 0 := by
    exact_mod_cast sub_ne_zero.mpr (ne_of_gt hdc)
  simp only [cross, Rat.cast_sub, Rat.cast_div, Line.evalReal]
  field_simp
  ring

/-- Telescoping hinge functions reconstruct the complete global maximum. -/
theorem slopeAtoms_call {c : Line} {rest : List Line} (hg : Good (c :: rest)) (x : ℝ) :
    peak (c :: rest) x = c.evalReal x + atomCall (slopeAtoms (c :: rest)) x := by
  induction rest generalizing c with
  | nil => simp [peak, slopeAtoms, atomCall]
  | cons d rest ih =>
    have hdc := good_pair_slope hg
    have ht := ih (good_tail c _ hg)
    by_cases hx : x ≤ (cross d c : ℝ)
    · have he := (reverse_eval_le_iff_real hdc x).2 hx
      have hb : d.evalReal x ≤ peak (d :: rest) x := by
        cases rest with
        | nil => exact le_rfl
        | cons e tail => exact le_max_left _ _
      rw [peak, max_eq_right (he.trans hb), ht]
      simp only [slopeAtoms, atomCall, List.map_cons, List.sum_cons]
      rw [max_eq_left (sub_nonneg.mpr hx), cross_identity hdc x]
      ring
    · have hx' : (cross d c : ℝ) ≤ x := (lt_of_not_ge hx).le
      have hz : atomCall (slopeAtoms (d :: rest)) x = 0 := by
        apply atomCall_zero_of_right
        intro a ha
        exact (by exact_mod_cast slopeAtoms_location_le hg ha :
          (a.location : ℝ) ≤ cross d c).trans hx'
      have he := (eval_le_iff_real hdc x).2 hx'
      rw [peak, ht, hz, add_zero, max_eq_left he]
      simp only [slopeAtoms, atomCall, List.map_cons, List.sum_cons]
      rw [max_eq_right (sub_nonpos.mpr hx'), mul_zero]
      change c.evalReal x = c.evalReal x + (0 + atomCall (slopeAtoms (d :: rest)) x)
      rw [hz]
      ring

theorem slopeAtoms_mass_sum (c : Line) (rest : List Line) :
    ((slopeAtoms (c :: rest)).map Atom.mass).sum =
      c.slope - (rest.getLastD c).slope := by
  induction rest generalizing c with
  | nil => simp [slopeAtoms]
  | cons d rest ih =>
    simp only [slopeAtoms, List.map_cons, List.sum_cons, List.getLastD_cons]
    rw [ih]
    ring

theorem slopeAtoms_mean (c : Line) (rest : List Line) (hg : Good (c :: rest)) :
    ((slopeAtoms (c :: rest)).map (fun a => a.mass * a.location)).sum =
      (rest.getLastD c).intercept - c.intercept := by
  induction rest generalizing c with
  | nil => simp [slopeAtoms]
  | cons d rest ih =>
    simp only [slopeAtoms, List.map_cons, List.sum_cons, List.getLastD_cons]
    rw [ih d (good_tail c _ hg)]
    have hz : c.slope - d.slope ≠ 0 := sub_ne_zero.mpr (ne_of_gt (good_pair_slope hg))
    dsimp [cross]
    field_simp
    ring

theorem atomCall_nonneg (atoms : List Atom) (hp : ∀ a ∈ atoms, 0 ≤ a.mass) (x : ℝ) :
    0 ≤ atomCall atoms x := by
  unfold atomCall
  apply List.sum_nonneg
  intro v hv
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hv
  exact mul_nonneg (by exact_mod_cast hp a ha) (le_max_right _ _)

theorem atomCall_term_le (atoms : List Atom) (hp : ∀ a ∈ atoms, 0 ≤ a.mass)
    {a : Atom} (ha : a ∈ atoms) (x : ℝ) :
    (a.mass : ℝ) * max ((a.location : ℝ) - x) 0 ≤ atomCall atoms x := by
  apply List.single_le_sum
  · intro v hv
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hv
    exact mul_nonneg (by exact_mod_cast hp a ha) (le_max_right _ _)
  · exact List.mem_map.mpr ⟨a, ha, rfl⟩

def atomPut (atoms : List Atom) (s : ℝ) : ℝ :=
  (atoms.map (fun a => (a.mass : ℝ) * max (s - (a.location : ℝ)) 0)).sum

theorem atom_parity (atoms : List Atom) (x : ℝ) :
    atomCall atoms x - atomPut atoms x =
      (atoms.map (fun a => (a.mass : ℝ) * a.location)).sum -
        x * (atoms.map (fun a => (a.mass : ℝ))).sum := by
  induction atoms with
  | nil => simp [atomCall, atomPut]
  | cons a atoms ih =>
    simp only [atomCall, atomPut, List.map_cons, List.sum_cons] at *
    by_cases hx : (a.location : ℝ) ≤ x
    · rw [max_eq_right (sub_nonpos.mpr hx), max_eq_left (sub_nonneg.mpr hx)]
      nlinarith
    · have hx' := (lt_of_not_ge hx).le
      rw [max_eq_left (sub_nonneg.mpr hx'), max_eq_right (sub_nonpos.mpr hx')]
      nlinarith

theorem atomPut_term_le (atoms : List Atom) (hp : ∀ a ∈ atoms, 0 ≤ a.mass)
    {a : Atom} (ha : a ∈ atoms) (x : ℝ) :
    (a.mass : ℝ) * max (x - (a.location : ℝ)) 0 ≤ atomPut atoms x := by
  apply List.single_le_sum
  · intro v hv
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hv
    exact mul_nonneg (by exact_mod_cast hp a ha) (le_max_right _ _)
  · exact List.mem_map.mpr ⟨a, ha, rfl⟩

/-- Endpoint call values certify support of the actual positive atom list. -/
theorem atom_support (atoms : List Atom) {a b m : ℝ}
    (hp : ∀ z ∈ atoms, 0 < z.mass)
    (ht : (atoms.map (fun z => (z.mass : ℝ))).sum = 1)
    (hm : (atoms.map (fun z => (z.mass : ℝ) * z.location)).sum = m)
    (ha : atomCall atoms a = m - a) (hb : atomCall atoms b = 0)
    {z : Atom} (hz : z ∈ atoms) : a ≤ z.location ∧ (z.location : ℝ) ≤ b := by
  have hpp : (0 : ℝ) < z.mass := by exact_mod_cast hp z hz
  have hp' : ∀ z ∈ atoms, 0 ≤ z.mass := fun z hz => (hp z hz).le
  have hpar := atom_parity atoms a
  rw [ha, hm, ht] at hpar
  have hput : atomPut atoms a = 0 := by linarith
  have hl := atomPut_term_le atoms hp' hz a
  have hr := atomCall_term_le atoms hp' hz b
  rw [hput] at hl
  rw [hb] at hr
  have hl' : max (a - (z.location : ℝ)) 0 ≤ 0 := by nlinarith
  have hr' : max ((z.location : ℝ) - b) 0 ≤ 0 := by nlinarith
  exact ⟨sub_nonpos.mp ((le_max_left _ _).trans hl'),
    sub_nonpos.mp ((le_max_left _ _).trans hr')⟩

theorem slopeAtoms_provenance (stack : List Line) {a : Atom} (ha : a ∈ slopeAtoms stack) :
    ∃ c ∈ stack, ∃ d ∈ stack,
      a.mass = c.slope - d.slope ∧ a.location = cross d c := by
  induction stack using slopeAtoms.induct with
  | case1 => simp [slopeAtoms] at ha
  | case2 c => simp [slopeAtoms] at ha
  | case3 c d rest ih =>
    simp only [slopeAtoms, List.mem_cons] at ha
    rcases ha with he | ha
    · subst a; exact ⟨c, by simp, d, by simp, rfl, rfl⟩
    · obtain ⟨u, hu, v, hv, he⟩ := ih ha
      exact ⟨u, List.mem_cons_of_mem _ hu, v, List.mem_cons_of_mem _ hv, he⟩

/-- Compute a rational scalar law from the actual global envelope stack.
There are four rational operations per atom: a mass subtraction and an
intersection using two subtractions and one division. -/
def buildAtoms (input : List Line) : List Atom × ℕ :=
  let stack := buildStack input
  (slopeAtoms stack.1, stack.2 + 4 * (stack.1.length - 1))

theorem buildAtoms_length (input : List Line) :
    (buildAtoms input).1.length ≤ input.length - 1 := by
  exact (slopeAtoms_length _).trans_le (Nat.sub_le_sub_right (buildStack_length input) 1)

theorem buildAtoms_cost (input : List Line) :
    (buildAtoms input).2 ≤ input.length * (input.length.log2 + 31) := by
  have hs := buildStack_cost input
  have hl := buildStack_length input
  have hd : (buildStack input).1.length - 1 ≤ input.length := by omega
  dsimp [buildAtoms]
  nlinarith

end ReciprocalAnchor.ManyLeaf.FastEnvelope
