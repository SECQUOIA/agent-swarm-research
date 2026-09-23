import Formal.DAGSpectral.BitComplexity
import Formal.DAGSpectral.EigenCompareSeparation

/-! Fixed-degree root separation has a linear rational bit budget. -/
namespace DAGSpectral
open ReciprocalAnchor Polynomial
open scoped BigOperators

lemma rationalBits_abs {q : ℚ} {B : ℕ} (hq : RationalBits q B) : RationalBits |q| B := by
  rcases le_total 0 q with h | h
  · simpa only [abs_of_nonneg h] using hq
  · simpa only [abs_of_nonpos h] using rationalBits_neg hq

lemma rationalBits_den_cast {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    RationalBits (q.den : ℚ) B := by
  constructor
  · simpa using hq.2
  · simpa using (show 1 < 2 ^ B by
      exact (Nat.one_le_iff_ne_zero.mpr q.den_nz).trans_lt hq.2)

lemma rationalBits_list_prod {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits xs.prod (1 + xs.length * B) := by
  induction xs with
  | nil => simpa using rationalBits_one
  | cons q xs ih =>
    have hq := h q (by simp)
    have hx := ih (fun r hr => h r (by simp [hr]))
    have hp := rationalBits_mul hq hx
    convert hp using 1 <;> simp [List.prod_cons, Nat.add_mul]
    omega

lemma eigenCompare_rationalBits_finset_prod {ι : Type*} (s : Finset ι) (f : ι → ℚ) {B : ℕ}
    (h : ∀ i ∈ s, RationalBits (f i) B) :
    RationalBits (∏ i ∈ s, f i) (1 + s.card * B) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using rationalBits_one
  | @insert i s hi ih =>
    have hp := rationalBits_mul (h i (by simp)) (ih (fun j hj => h j (by simp [hj])))
    rw [Finset.prod_insert hi, Finset.card_insert_of_notMem hi]
    convert hp using 1
    ring

lemma ratPolynomialDen_bits {P : ℚ[X]} {B : ℕ}
    (h : ∀ i ∈ P.support, RationalBits (P.coeff i) B) :
    RationalBits (ratPolynomialDen P : ℚ) (1 + P.support.card * B) := by
  unfold ratPolynomialDen
  push_cast
  exact eigenCompare_rationalBits_finset_prod _ _ (fun i hi => rationalBits_den_cast (h i hi))

lemma ratPolynomialHeight_bits {P : ℚ[X]} {B : ℕ}
    (h : ∀ i ∈ P.support, RationalBits (P.coeff i) B) :
    RationalBits (ratPolynomialHeight P) (1 + P.support.card * (B + 1)) :=
  rationalBits_finset_sum _ _ (fun i hi => rationalBits_abs (h i hi))

lemma rationalBits_max_one {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    RationalBits (max 1 q) B := by
  rcases le_total 1 q with h | h
  · simpa [max_eq_right h] using hq
  · simpa [max_eq_left h] using rationalBits_mono rationalBits_one (rationalBits_pos hq)

/-- Explicit linear-in-input-bits budget for a degree-`d` polynomial gap. -/
def rootSeparationBitBound (d B : ℕ) : ℕ := 2 + (d + 1) * (2 * B + 1)

lemma ratRootSeparation_bits {P : ℚ[X]} {d B : ℕ} (hd : P.natDegree ≤ d)
    (h : ∀ i ∈ P.support, RationalBits (P.coeff i) B) :
    RationalBits (ratRootSeparation P) (rootSeparationBitBound d B) := by
  have hD := ratPolynomialDen_bits h
  have hH := rationalBits_max_one (ratPolynomialHeight_bits h)
  have hprod := rationalBits_inv (rationalBits_mul hD hH)
  have hc : P.support.card ≤ d + 1 := by
    exact (Finset.card_le_card P.supp_subset_range_natDegree_succ).trans
      (by simpa only [Finset.card_range] using Nat.add_le_add_right hd 1)
  apply rationalBits_mono (by simpa only [ratRootSeparation, one_div] using hprod)
  unfold rootSeparationBitBound
  have hh := Nat.mul_le_mul_right (2 * B + 1) hc
  nlinarith

lemma rootSeparationBitBound_linear (d B : ℕ) :
    rootSeparationBitBound d B ≤ (2 * d + 4) * (B + 1) := by
  unfold rootSeparationBitBound
  nlinarith

/-- The numerator digit count used as a bisection budget is linear in the
bit budgets of its two rational inputs. -/
lemma bisection_numerator_size {R δ : ℚ} {BR Bδ : ℕ}
    (hR : RationalBits R BR) (hδ : RationalBits δ Bδ) :
    (4 * R / δ).num.natAbs.size ≤ 3 + BR + Bδ := by
  have h4 : RationalBits 4 3 := by unfold RationalBits; decide
  exact ((rationalBits_iff_size _ _).mp
    (rationalBits_div (rationalBits_mul h4 hR) hδ)).1

lemma root_separation_bisection_size {P : ℚ[X]} {d B BR : ℕ} {R : ℚ}
    (hd : P.natDegree ≤ d) (h : ∀ i ∈ P.support, RationalBits (P.coeff i) B)
    (hR : RationalBits R BR) :
    (4 * R / ratRootSeparation P).num.natAbs.size ≤
      3 + BR + rootSeparationBitBound d B :=
  bisection_numerator_size hR (ratRootSeparation_bits hd h)


lemma separationFromCoefficients_bits {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits (separationFromCoefficients xs) (2 + xs.length * (2 * B + 1)) := by
  have hD : RationalBits ((xs.map Rat.den).prod : ℚ) (1 + xs.length * B) := by
    have hh : ∀ q ∈ xs.map (fun r => (r.den : ℚ)), RationalBits q B := by
      intro q hq
      obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hq
      exact rationalBits_den_cast (h r hr)
    have hp := rationalBits_list_prod hh
    have heq (ys : List ℚ) : ((ys.map Rat.den).prod : ℚ) =
        (ys.map (fun r => (r.den : ℚ))).prod := by
      induction ys with
      | nil => simp
      | cons r xs ih => simpa using congrArg (fun a : ℚ => (r.den : ℚ) * a) ih
    simpa only [List.length_map, heq xs] using hp
  have hH : RationalBits (xs.map abs).sum (1 + xs.length * (B + 1)) := by
    have hh : ∀ q ∈ xs.map abs, RationalBits q B := by
      intro q hq
      obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hq
      exact rationalBits_abs (h r hr)
    simpa only [List.length_map] using rationalBits_list_sum hh
  have hg := rationalBits_inv (rationalBits_mul hD (rationalBits_max_one hH))
  convert hg using 1
  · simp only [separationFromCoefficients, one_div]
  · ring

lemma separationFromCoefficients_bits_of_length {xs : List ℚ} {d B : ℕ}
    (hlen : xs.length ≤ d + 1) (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits (separationFromCoefficients xs) (rootSeparationBitBound d B) := by
  apply rationalBits_mono (separationFromCoefficients_bits h)
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hlen) 2

lemma coefficient_list_bisection_size {xs : List ℚ} {d B BR : ℕ} {R : ℚ}
    (hlen : xs.length ≤ d + 1) (h : ∀ q ∈ xs, RationalBits q B)
    (hR : RationalBits R BR) :
    (4 * R / separationFromCoefficients xs).num.natAbs.size ≤
      3 + BR + rootSeparationBitBound d B :=
  bisection_numerator_size hR (separationFromCoefficients_bits_of_length hlen h)

end DAGSpectral
