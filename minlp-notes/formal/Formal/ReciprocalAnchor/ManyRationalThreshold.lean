import Formal.ReciprocalAnchor.ManyRationalWitness

/-! A finite rational threshold search, with an explicit arithmetic-work bound. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

/-- Each test performs two length-`K` tail sums and their two final comparisons. -/
def rationalThresholdTest {K : ℕ} (p x : Fin K → ℚ) (q s : ℚ) : Bool :=
  decide ((∑ i, if s < x i then p i else 0) ≤ q ∧
    q ≤ ∑ i, if s ≤ x i then p i else 0)

/-- The second component counts a conservative budget of rational comparisons and
additions: two comparisons and two additions per atom, plus two comparisons. -/
def rationalThresholdSearch {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) :
    List ℚ → Option ℚ × ℕ
  | [] => (none, 0)
  | s :: ss => if rationalThresholdTest p x q s then (some s, 4 * K + 2)
      else let r := rationalThresholdSearch p x q ss; (r.1, r.2 + (4 * K + 2))

theorem rationalThresholdSearch_value {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) (ss : List ℚ) :
    (rationalThresholdSearch p x q ss).1 = ss.find? (rationalThresholdTest p x q) := by
  induction ss with
  | nil => rfl
  | cons s ss ih =>
    simp only [rationalThresholdSearch, List.find?_cons]
    split_ifs <;> simp_all

theorem rationalThresholdSearch_cost {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) (ss : List ℚ) :
    (rationalThresholdSearch p x q ss).2 ≤ ss.length * (4 * K + 2) := by
  induction ss with
  | nil => simp [rationalThresholdSearch]
  | cons s ss ih =>
    simp only [rationalThresholdSearch, List.length_cons]
    split_ifs
    · change 4 * K + 2 ≤ (ss.length + 1) * (4 * K + 2)
      nlinarith
    · change (rationalThresholdSearch p x q ss).2 + (4 * K + 2) ≤ _
      nlinarith

def rationalThreshold {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) : Option ℚ × ℕ :=
  rationalThresholdSearch p x q (0 :: List.ofFn x)

/-- The search always succeeds, including zero mass, repeated locations, and zero weights. -/
theorem rationalThreshold_spec {K : ℕ} (p x : Fin K → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q : ℚ) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ s, (rationalThreshold p x q).1 = some s ∧
      (∑ i, if s < x i then p i else 0) ≤ q ∧
      q ≤ ∑ i, if s ≤ x i then p i else 0 := by
  obtain ⟨s, hlo, hhi, hs⟩ := exists_weighted_threshold_finset_supported p x Finset.univ
    (fun i _ => hp i) q hq (by simpa [hsum] using hq1)
  have hmem : s ∈ (0 :: List.ofFn x) := by
    rcases hs with rfl | ⟨i, _, rfl⟩
    · simp
    · simp
  have ht : rationalThresholdTest p x q s = true := by
    simpa only [rationalThresholdTest, decide_eq_true_eq] using And.intro hlo hhi
  have hex : ((0 :: List.ofFn x).find? (rationalThresholdTest p x q)).isSome :=
    List.find?_isSome.mpr ⟨s, hmem, ht⟩
  cases he : (0 :: List.ofFn x).find? (rationalThresholdTest p x q) with
  | none => simp [he] at hex
  | some t =>
    refine ⟨t, ?_, ?_⟩
    · exact (rationalThresholdSearch_value p x q _).trans he
    · have ht := List.find?_some he
      simpa only [rationalThresholdTest, decide_eq_true_eq] using ht

theorem rationalThreshold_polynomial_cost {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) :
    (rationalThreshold p x q).2 ≤ (K + 1) * (4 * K + 2) := by
  simpa [rationalThreshold] using rationalThresholdSearch_cost p x q (0 :: List.ofFn x)

/-- A rational upper selector is obtained directly from the successful finite search. -/
theorem rationalThreshold_selector {K : ℕ} (p x : Fin K → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q : ℚ) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ s, (rationalThreshold p x q).1 = some s ∧
      (∀ i, thresholdSelection p x q s i ∈ Set.Icc (0 : ℚ) 1) ∧
      selectionMass p (thresholdSelection p x q s) = q ∧
      selectionMoment p x (thresholdSelection p x q s) = q * s + selectionCall p x s := by
  obtain ⟨s, he, hlo, hhi⟩ := rationalThreshold_spec p x hp hsum q hq hq1
  exact ⟨s, he, thresholdSelection_spec p x hp q s hlo hhi⟩

/-- Every candidate compared by the search is zero or an original support location. -/
theorem rationalThreshold_candidate_supported {K : ℕ} (x : Fin K → ℚ) {s : ℚ}
    (hs : s ∈ 0 :: List.ofFn x) : s = 0 ∨ ∃ i, s = x i := by
  rcases List.mem_cons.mp hs with h | h
  · exact Or.inl h
  · obtain ⟨i, hi⟩ := List.mem_ofFn.mp h
    exact Or.inr ⟨i, hi.symm⟩

/-- Success cannot introduce a threshold outside the original finite candidate list. -/
theorem rationalThreshold_supported {K : ℕ} (p x : Fin K → ℚ) (q : ℚ) {s : ℚ}
    (hs : (rationalThreshold p x q).1 = some s) : s = 0 ∨ ∃ i, s = x i := by
  apply rationalThreshold_candidate_supported x
  apply List.mem_of_find?_eq_some
  exact (rationalThresholdSearch_value p x q _).symm.trans hs

/-- All thresholds visited by the search have the input coordinate bit bound. -/
theorem rationalThreshold_candidate_bits {K B : ℕ} (x : Fin K → ℚ)
    (hx : ∀ i, RationalBits (x i) B) (hB : 0 < B) {s : ℚ}
    (hs : s ∈ 0 :: List.ofFn x) : RationalBits s B := by
  rcases rationalThreshold_candidate_supported x hs with rfl | ⟨i, rfl⟩
  · exact rationalBits_mono rationalBits_zero hB
  · exact hx i

/-- In particular, every returned threshold has the input coordinate bit bound. -/
theorem rationalThreshold_bits {K B : ℕ} (p x : Fin K → ℚ) (q : ℚ)
    (hx : ∀ i, RationalBits (x i) B) (hB : 0 < B) {s : ℚ}
    (hs : (rationalThreshold p x q).1 = some s) : RationalBits s B := by
  rcases rationalThreshold_supported p x q hs with rfl | ⟨i, rfl⟩
  · exact rationalBits_mono rationalBits_zero hB
  · exact hx i

end ReciprocalAnchor.ManyLeaf
