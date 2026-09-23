import Formal.MultilinearGap.StructuralFrequencyTheorem
import Formal.MultilinearGap.StructuralFrequencyMonomial
import Formal.MultilinearGap.StructuralFrequencySupport
import Formal.MultilinearGap.StructuralCommonAspect

/-! Original monomial and physical-box consequences of the proved
frequency-two cardinality theorem. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The sharp universal frequency-two bound for the original polynomial. -/
theorem frequencyTwo_monomial_three_halves (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap S a x ≤ (3 / 2 : ℝ) * hullGap (supportPolynomial S a) x := by
  apply weightedTermwiseGap_le_of_cardinality_bound S a ha x hx (3/2)
  intro φ hφ
  exact frequencyTwo_cardinality_three_halves (fun s : {s // s ∈ S} => s.val)
    (FrequencyTwo.subtype_card_le hS) φ hφ _
    (fun s => cardinalityFactor_separatelyAffine (φ s) s.val)
    (fun s v => cardinalityFactor_vertex (φ s) s.val v) x hx

/-- The odd-girth improvement applies to the original support polynomial. -/
theorem frequencyTwo_monomial_oddGirth (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (g : ℕ) (hg : 1 < g) (hgirth : FrequencyOddGirthAtLeast (fun s : {s // s ∈ S} => s.val) g)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap S a x ≤ ((g : ℝ) / ((g : ℝ) - 1)) *
      hullGap (supportPolynomial S a) x := by
  apply weightedTermwiseGap_le_of_cardinality_bound S a ha x hx
  intro φ hφ
  exact frequencyTwo_cardinality_oddGirth (fun s : {s // s ∈ S} => s.val)
    (FrequencyTwo.subtype_card_le hS) g hg hgirth φ hφ _
    (fun s => cardinalityFactor_separatelyAffine (φ s) s.val)
    (fun s v => cardinalityFactor_vertex (φ s) s.val v) x hx

/-- Bipartite dual graphs give equality of the actual original-factor gaps. -/
theorem frequencyTwo_monomial_bipartite (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (hbi : FrequencyBipartite (fun s : {s // s ∈ S} => s.val))
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s) (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap S a x = hullGap (supportPolynomial S a) x := by
  apply le_antisymm
  · have h : weightedTermwiseGap S a x ≤ 1 * hullGap (supportPolynomial S a) x := by
      apply weightedTermwiseGap_le_of_cardinality_bound S a ha x hx 1
      intro φ hφ
      simpa only [one_mul] using frequencyTwo_cardinality_bipartite_le
        (fun s : {s // s ∈ S} => s.val) (FrequencyTwo.subtype_card_le hS) hbi φ hφ _
        (fun s => cardinalityFactor_separatelyAffine (φ s) s.val)
        (fun s v => cardinalityFactor_vertex (φ s) s.val v) x hx
    simpa using h
  · exact hullGap_le_weightedTermwiseGap S a ha x hx

omit [Fintype I] in
/-- Scaling to zero-lower boxes preserves the original support frequency. -/
theorem frequencyTwo_zeroLower_three_halves [Finite I] (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (x : I → ℝ)
    (hx : x ∈ coordinateBox (fun _ => 0) u) :
    boxTermwiseGap S a (fun _ => 0) u x ≤
      (3 / 2 : ℝ) * boxHullGap (fun _ => 0) u (supportPolynomial S a) x := by
  let := Fintype.ofFinite I
  exact zeroLower_gap_bound_transfer S (3/2) (frequencyTwo_monomial_three_halves S hS)
    a ha u hu x hx

omit [Fintype I] in
/-- The exact same odd-girth bound holds on arbitrary zero-lower boxes. -/
theorem frequencyTwo_zeroLower_oddGirth [Finite I] (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (g : ℕ) (hg : 1 < g) (hgirth : FrequencyOddGirthAtLeast (fun s : {s // s ∈ S} => s.val) g)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (x : I → ℝ)
    (hx : x ∈ coordinateBox (fun _ => 0) u) :
    boxTermwiseGap S a (fun _ => 0) u x ≤
      ((g : ℝ) / ((g : ℝ) - 1)) *
        boxHullGap (fun _ => 0) u (supportPolynomial S a) x := by
  let := Fintype.ofFinite I
  exact zeroLower_gap_bound_transfer S _ (frequencyTwo_monomial_oddGirth S hS g hg hgirth)
    a ha u hu x hx

omit [Fintype I] in
/-- Zero-lower normalization preserves exact equality for a bipartite dual graph. -/
theorem frequencyTwo_zeroLower_bipartite [Finite I] (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (hbi : FrequencyBipartite (fun s : {s // s ∈ S} => s.val))
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (u : I → ℝ) (hu : ∀ i, 0 ≤ u i) (x : I → ℝ)
    (hx : x ∈ coordinateBox (fun _ => 0) u) :
    boxTermwiseGap S a (fun _ => 0) u x =
      boxHullGap (fun _ => 0) u (supportPolynomial S a) x := by
  let := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint (fun _ => 0) u hu x hx
  rw [boxTermwiseGap_zeroLower S a u hu p hp, boxHullGap_zeroLower S a u hu p hp]
  exact frequencyTwo_monomial_bipartite S hS hbi _
    (fun s hs => zeroLowerCoefficient_nonneg u hu a s (ha s hs)) p hp

variable {J : Type*} [Fintype J]

omit [Fintype I] in
/-- Common-aspect physical monomials retain the sharp universal bound after
fixed coordinates are removed. Each original monomial is still one factor. -/
theorem frequencyTwo_commonAspect_three_halves [Finite I]
    (S : J → Finset I)
    (hfreq : ∀ i, (Finset.univ.filter fun j => i ∈ S j).card ≤ 2)
    (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (rho : J → ℝ) (hrho : ∀ j, 0 ≤ rho j)
    (hr : ∀ j i, i ∈ varyingBoxSupport l u (S j) → u i = rho j * l i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j, a j * boxHullGap l u (monomial (S j)) x) ≤
      (3 / 2 : ℝ) * boxHullGap l u (factorSum fun j y => a j * monomial (S j) y) x := by
  let := Fintype.ofFinite I
  apply commonAspect_original_box_transfer S a ha l u hl hlu rho hrho hr (3/2) _ x hx
  intro f φ hf hφ hv p hp
  apply frequencyTwo_cardinality_three_halves _ _ φ hφ f hf hv p hp
  exact frequency_le_two_varyingBoxSupport hfreq l u

omit [Fintype I] in
/-- Odd-girth improvements also preserve original physical factors. -/
theorem frequencyTwo_commonAspect_oddGirth [Finite I]
    (S : J → Finset I)
    (hfreq : ∀ i, (Finset.univ.filter fun j => i ∈ S j).card ≤ 2)
    (g : ℕ) (hg : 1 < g) (hgirth : FrequencyOddGirthAtLeast S g)
    (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (rho : J → ℝ) (hrho : ∀ j, 0 ≤ rho j)
    (hr : ∀ j i, i ∈ varyingBoxSupport l u (S j) → u i = rho j * l i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j, a j * boxHullGap l u (monomial (S j)) x) ≤
      ((g : ℝ) / ((g : ℝ) - 1)) *
        boxHullGap l u (factorSum fun j y => a j * monomial (S j) y) x := by
  let := Fintype.ofFinite I
  apply commonAspect_original_box_transfer S a ha l u hl hlu rho hrho hr _ _ x hx
  intro f φ hf hφ hv p hp
  apply frequencyTwo_cardinality_oddGirth _ _ g hg _ φ hφ f hf hv p hp
  · exact frequency_le_two_varyingBoxSupport hfreq l u
  · exact hgirth.of_subset (fun _ => Finset.filter_subset _ _)

omit [Fintype I] in
/-- The original positive-box gaps are equal when the dual graph is bipartite
and each factor has a common aspect ratio on its varying coordinates. -/
theorem frequencyTwo_commonAspect_bipartite [Finite I]
    (S : J → Finset I)
    (hfreq : ∀ i, (Finset.univ.filter fun j => i ∈ S j).card ≤ 2)
    (hbi : FrequencyBipartite S)
    (a : J → ℝ) (ha : ∀ j, 0 ≤ a j)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (rho : J → ℝ) (hrho : ∀ j, 0 ≤ rho j)
    (hr : ∀ j i, i ∈ varyingBoxSupport l u (S j) → u i = rho j * l i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∑ j, a j * boxHullGap l u (monomial (S j)) x) =
      boxHullGap l u (factorSum fun j y => a j * monomial (S j) y) x := by
  let := Fintype.ofFinite I
  apply le_antisymm
  · have h := commonAspect_original_box_transfer S a ha l u hl hlu rho hrho hr 1
      (fun f φ hf hφ hv p hp => by
        simpa only [one_mul] using frequencyTwo_cardinality_bipartite_le _
          (frequency_le_two_varyingBoxSupport hfreq l u)
          (hbi.of_subset (fun _ => Finset.filter_subset _ _)) φ hφ f hf hv p hp) x hx
    simpa using h
  · exact boxHullGap_factorSum_monomial_le S a ha l u hlu x hx

end
end MultilinearGap
