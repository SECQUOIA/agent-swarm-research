import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.EigenCompareBits
import Formal.DAGSpectral.MatrixArithmeticTrace

/-! Actual rational events for the coefficient-list gap and spectral search
radius. Reading a canonical rational denominator is a representation projection;
its product, the absolute-value branches, sums, max and inverse are traced. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- The branch comparison and, when needed, sign change are both recorded. -/
def absoluteWithTrace (q : ℚ) : ℚ × List ArithmeticEvent :=
  if 0 ≤ q then (q, [(.compare, 0, q)])
  else (-q, [(.compare, 0, q), (.neg, q, 0)])

@[simp] theorem absoluteWithTrace_value (q : ℚ) : (absoluteWithTrace q).1 = |q| := by
  unfold absoluteWithTrace
  split_ifs with h
  · exact (abs_of_nonneg h).symm
  · exact (abs_of_neg (lt_of_not_ge h)).symm

theorem absoluteWithTrace_length (q : ℚ) : (absoluteWithTrace q).2.length ≤ 2 := by
  unfold absoluteWithTrace
  split_ifs <;> simp

theorem absoluteWithTrace_bits {q : ℚ} {B : ℕ} (hq : RationalBits q B) :
    ∀ e ∈ (absoluteWithTrace q).2, eventBits B e := by
  have hz := rationalBits_mono rationalBits_zero (rationalBits_pos hq)
  unfold absoluteWithTrace
  split_ifs <;> intro e he <;> simp only [List.mem_cons, List.not_mem_nil, or_false] at he
  · subst e; exact ⟨hz, hq⟩
  · rcases he with rfl | rfl
    · exact ⟨hz, hq⟩
    · exact ⟨hq, hz⟩

def absoluteSumWithTrace : List ℚ → ℚ × List ArithmeticEvent
  | [] => (0, [])
  | q :: qs =>
    let a := absoluteWithTrace q
    let tail := absoluteSumWithTrace qs
    (a.1 + tail.1, a.2 ++ tail.2 ++ [(.add, a.1, tail.1)])

@[simp] theorem absoluteSumWithTrace_value (xs : List ℚ) :
    (absoluteSumWithTrace xs).1 = (xs.map abs).sum := by
  induction xs with
  | nil => rfl
  | cons q qs ih => simp [absoluteSumWithTrace, ih]

theorem absoluteSumWithTrace_length (xs : List ℚ) :
    (absoluteSumWithTrace xs).2.length ≤ 3 * xs.length := by
  induction xs with
  | nil => simp [absoluteSumWithTrace]
  | cons q qs ih =>
    have ha := absoluteWithTrace_length q
    simp only [absoluteSumWithTrace, List.length_append, List.length_cons, List.length_nil]
    omega

lemma absoluteSum_bits {xs : List ℚ} {B : ℕ} (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits (xs.map abs).sum (1 + xs.length * (B + 1)) := by
  have ha : ∀ q ∈ xs.map abs, RationalBits q B := by
    intro q hq
    obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hq
    exact rationalBits_abs (h r hr)
  simpa only [List.length_map] using rationalBits_list_sum ha

theorem absoluteSumWithTrace_bits {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    ∀ e ∈ (absoluteSumWithTrace xs).2, eventBits (1 + xs.length * (B + 1)) e := by
  induction xs with
  | nil => simp [absoluteSumWithTrace]
  | cons q qs ih =>
    have hq := h q (by simp)
    have ht : ∀ r ∈ qs, RationalBits r B := fun r hr => h r (by simp [hr])
    have hs := absoluteSum_bits ht
    intro e he
    simp only [absoluteSumWithTrace, List.mem_append, List.mem_singleton] at he
    rcases he with (he | he) | rfl
    · exact eventBits_mono (absoluteWithTrace_bits hq e he) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega)
    · exact eventBits_mono (ih ht e he) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega)
    · simp only [eventBits, absoluteWithTrace_value, absoluteSumWithTrace_value]
      exact ⟨rationalBits_mono (rationalBits_abs hq) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega),
        rationalBits_mono hs (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega)⟩

/-- Denominator products are formed by actual rational multiplications. -/
def denominatorProductWithTrace : List ℚ → ℚ × List ArithmeticEvent
  | [] => (1, [])
  | q :: qs =>
    let tail := denominatorProductWithTrace qs
    ((q.den : ℚ) * tail.1, tail.2 ++ [(.mul, (q.den : ℚ), tail.1)])

@[simp] theorem denominatorProductWithTrace_value (xs : List ℚ) :
    (denominatorProductWithTrace xs).1 = ((xs.map Rat.den).prod : ℚ) := by
  induction xs with
  | nil => rfl
  | cons q qs ih => simp [denominatorProductWithTrace, ih]

@[simp] theorem denominatorProductWithTrace_length (xs : List ℚ) :
    (denominatorProductWithTrace xs).2.length = xs.length := by
  induction xs with
  | nil => rfl
  | cons q qs ih => simp [denominatorProductWithTrace, ih]

lemma denominatorProduct_bits {xs : List ℚ} {B : ℕ} (h : ∀ q ∈ xs, RationalBits q B) :
    RationalBits ((xs.map Rat.den).prod : ℚ) (1 + xs.length * B) := by
  induction xs with
  | nil => simpa using rationalBits_one
  | cons q qs ih =>
    have hm := rationalBits_mul (rationalBits_den_cast (h q (by simp)))
      (ih (fun r hr => h r (by simp [hr])))
    convert hm using 1 <;> simp [List.prod_cons, Nat.add_mul]
    omega

theorem denominatorProductWithTrace_bits {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    ∀ e ∈ (denominatorProductWithTrace xs).2, eventBits (1 + xs.length * B) e := by
  induction xs with
  | nil => simp [denominatorProductWithTrace]
  | cons q qs ih =>
    have ht : ∀ r ∈ qs, RationalBits r B := fun r hr => h r (by simp [hr])
    intro e he
    simp only [denominatorProductWithTrace, List.mem_append, List.mem_singleton] at he
    rcases he with he | rfl
    · exact eventBits_mono (ih ht e he) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega)
    · simp only [eventBits, denominatorProductWithTrace_value]
      exact ⟨rationalBits_mono (rationalBits_den_cast (h q (by simp))) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega),
        rationalBits_mono (denominatorProduct_bits ht) (by
          simp only [List.length_cons, Nat.add_mul, Nat.one_mul]
          omega)⟩

/-- Execute every operation used in the coefficient-list separation formula. -/
def separationFromCoefficientsWithTrace (xs : List ℚ) : ℚ × List ArithmeticEvent :=
  let d := denominatorProductWithTrace xs
  let a := absoluteSumWithTrace xs
  let cap := if 1 ≤ a.1 then a.1 else 1
  let product := d.1 * cap
  (product⁻¹, d.2 ++ a.2 ++ [(.compare, 1, a.1), (.mul, d.1, cap), (.inv, product, 0)])

@[simp] theorem separationFromCoefficientsWithTrace_value (xs : List ℚ) :
    (separationFromCoefficientsWithTrace xs).1 = separationFromCoefficients xs := by
  simp only [separationFromCoefficientsWithTrace, denominatorProductWithTrace_value,
    absoluteSumWithTrace_value, separationFromCoefficients, one_div]
  rw [max_def]

/-- An exact linear count in the coefficient-list length. -/
theorem separationFromCoefficientsWithTrace_length (xs : List ℚ) :
    (separationFromCoefficientsWithTrace xs).2.length ≤ 4 * xs.length + 3 := by
  have hs := absoluteSumWithTrace_length xs
  simp only [separationFromCoefficientsWithTrace, List.length_append,
    denominatorProductWithTrace_length, List.length_cons, List.length_nil]
  omega

def separationPreprocessingWidth (n B : ℕ) : ℕ := 3 + n * (2 * B + 2)

theorem separationFromCoefficientsWithTrace_bits {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    ∀ e ∈ (separationFromCoefficientsWithTrace xs).2,
      eventBits (separationPreprocessingWidth xs.length B) e := by
  have hd := denominatorProduct_bits h
  have ha := absoluteSum_bits h
  have hm := rationalBits_max_one ha
  have hp := rationalBits_mul hd hm
  have hds : 1 + xs.length * B ≤ separationPreprocessingWidth xs.length B := by
    unfold separationPreprocessingWidth; nlinarith
  have has : 1 + xs.length * (B + 1) ≤ separationPreprocessingWidth xs.length B := by
    unfold separationPreprocessingWidth; nlinarith
  have hps : (1 + xs.length * B) + (1 + xs.length * (B + 1)) ≤
      separationPreprocessingWidth xs.length B := by unfold separationPreprocessingWidth; nlinarith
  have h1 : 1 ≤ separationPreprocessingWidth xs.length B := by
    unfold separationPreprocessingWidth; omega
  intro e he
  simp only [separationFromCoefficientsWithTrace, denominatorProductWithTrace_value,
    absoluteSumWithTrace_value, ← max_def, List.mem_append, List.mem_cons,
    List.not_mem_nil, or_false] at he
  rcases he with (he | he) | (rfl | rfl | rfl)
  · exact eventBits_mono (denominatorProductWithTrace_bits h e he) hds
  · exact eventBits_mono (absoluteSumWithTrace_bits h e he) has
  · exact ⟨rationalBits_mono rationalBits_one h1, rationalBits_mono ha has⟩
  · exact ⟨rationalBits_mono hd hds, rationalBits_mono hm has⟩
  · exact ⟨rationalBits_mono hp hps, rationalBits_mono rationalBits_zero h1⟩

theorem separationFromCoefficientsWithTrace_bitWork {xs : List ℚ} {B : ℕ}
    (h : ∀ q ∈ xs, RationalBits q B) :
    traceBitWork (separationPreprocessingWidth xs.length B)
      (separationFromCoefficientsWithTrace xs).2 ≤
      (4 * xs.length + 3) * (256 * (separationPreprocessingWidth xs.length B + 1) ^ 3) := by
  exact (traceBitWork_le (separationFromCoefficientsWithTrace_bits h)).trans
    (Nat.mul_le_mul_right _ (separationFromCoefficientsWithTrace_length xs))

/-- Execute the absolute diagonal sums and the two additions defining the radius. -/
def eigenSearchRadiusWithTrace {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℚ) :
    ℚ × List ArithmeticEvent :=
  let a := absoluteSumWithTrace (List.ofFn (fun i => A i i))
  let b := absoluteSumWithTrace (List.ofFn (fun i => B i i))
  let first := 1 + a.1
  (first + b.1, a.2 ++ b.2 ++ [(.add, 1, a.1), (.add, first, b.1)])

@[simp] theorem eigenSearchRadiusWithTrace_value {n : ℕ}
    (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenSearchRadiusWithTrace A B).1 = eigenSearchRadius A B := by
  simp only [eigenSearchRadiusWithTrace, absoluteSumWithTrace_value,
    List.map_ofFn, List.sum_ofFn, Function.comp_def, eigenSearchRadius]

theorem eigenSearchRadiusWithTrace_length {n : ℕ}
    (A B : Matrix (Fin n) (Fin n) ℚ) :
    (eigenSearchRadiusWithTrace A B).2.length ≤ 6 * n + 2 := by
  have ha := absoluteSumWithTrace_length (List.ofFn (fun i => A i i))
  have hb := absoluteSumWithTrace_length (List.ofFn (fun i => B i i))
  simp only [List.length_ofFn] at ha hb
  simp only [eigenSearchRadiusWithTrace, List.length_append, List.length_cons, List.length_nil]
  omega

def radiusPreprocessingWidth (n bits : ℕ) : ℕ := 3 + 2 * n * (bits + 1)

theorem eigenSearchRadiusWithTrace_bits {n K : ℕ}
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A K) (hB : MatrixBits B K) :
    ∀ e ∈ (eigenSearchRadiusWithTrace A B).2, eventBits (radiusPreprocessingWidth n K) e := by
  have ha : ∀ q ∈ List.ofFn (fun i => A i i), RationalBits q K := by
    intro q hq
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hq
    exact hA i i
  have hb : ∀ q ∈ List.ofFn (fun i => B i i), RationalBits q K := by
    intro q hq
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hq
    exact hB i i
  have hab := absoluteSum_bits ha
  have hbb := absoluteSum_bits hb
  simp only [List.length_ofFn] at hab hbb
  have hf := rationalBits_add rationalBits_one hab
  have hsum : 1 + n * (K + 1) ≤ radiusPreprocessingWidth n K := by
    unfold radiusPreprocessingWidth; nlinarith
  have hfirst : 1 + (1 + n * (K + 1)) + 1 ≤ radiusPreprocessingWidth n K := by
    unfold radiusPreprocessingWidth; nlinarith
  have hone : 1 ≤ radiusPreprocessingWidth n K := by unfold radiusPreprocessingWidth; nlinarith
  intro e he
  simp only [eigenSearchRadiusWithTrace, List.mem_append, List.mem_cons,
    List.not_mem_nil, or_false, absoluteSumWithTrace_value] at he
  rcases he with (he | he) | (rfl | rfl)
  · have hh := absoluteSumWithTrace_bits ha e he
    simp only [List.length_ofFn] at hh
    exact eventBits_mono hh hsum
  · have hh := absoluteSumWithTrace_bits hb e he
    simp only [List.length_ofFn] at hh
    exact eventBits_mono hh hsum
  · exact ⟨rationalBits_mono rationalBits_one hone, rationalBits_mono hab hsum⟩
  · exact ⟨rationalBits_mono hf hfirst, rationalBits_mono hbb hsum⟩

/-- The radius value itself has a linear rational bit budget. -/
theorem eigenSearchRadius_bits {n K : ℕ}
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A K) (hB : MatrixBits B K) :
    RationalBits (eigenSearchRadius A B) (5 + 2 * n * (K + 1)) := by
  have ha : RationalBits (∑ i, |A i i|) (1 + n * (K + 1)) := by
    simpa only [Finset.card_univ, Fintype.card_fin] using
      rationalBits_finset_sum Finset.univ (fun i => |A i i|)
        (fun i _ => rationalBits_abs (hA i i))
  have hb : RationalBits (∑ i, |B i i|) (1 + n * (K + 1)) := by
    simpa only [Finset.card_univ, Fintype.card_fin] using
      rationalBits_finset_sum Finset.univ (fun i => |B i i|)
        (fun i _ => rationalBits_abs (hB i i))
  have hv := rationalBits_add (rationalBits_add rationalBits_one ha) hb
  convert hv using 1
  · rfl
  · ring

theorem eigenSearchRadiusWithTrace_bitWork {n K : ℕ}
    {A B : Matrix (Fin n) (Fin n) ℚ} (hA : MatrixBits A K) (hB : MatrixBits B K) :
    traceBitWork (radiusPreprocessingWidth n K) (eigenSearchRadiusWithTrace A B).2 ≤
      (6 * n + 2) * (256 * (radiusPreprocessingWidth n K + 1) ^ 3) := by
  exact (traceBitWork_le (eigenSearchRadiusWithTrace_bits hA hB)).trans
    (Nat.mul_le_mul_right _ (eigenSearchRadiusWithTrace_length A B))

theorem separationPreprocessingWidth_linear (n B : ℕ) :
    separationPreprocessingWidth n B ≤ (2 * n + 3) * (B + 1) := by
  unfold separationPreprocessingWidth
  nlinarith

theorem radiusPreprocessingWidth_linear (n B : ℕ) :
    radiusPreprocessingWidth n B ≤ (2 * n + 3) * (B + 1) := by
  unfold radiusPreprocessingWidth
  nlinarith

end DAGSpectral
