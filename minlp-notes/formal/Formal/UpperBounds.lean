import Formal.Scalar
import Formal.UpperCore
import Formal.RationalPolyhedron
import Formal.IntegerPolyhedron

namespace ExactCounts
noncomputable section
open scoped BigOperators

theorem integerSystem_admissible (n : ℕ) :
    Admissible {y | IntegerSystem y} (IntegerCodes n) := by
  classical
  constructor
  · intro x hx
    choose j hj using fun i => graph_in_box (hx i).1 (hx i).2
    refine ⟨fun i => ((j i).val : ℝ), ?_,
      fun a => if (finProdFinEquiv.symm a).2 = j (finProdFinEquiv.symm a).1 then 1 else 0, ?_⟩
    · exact ⟨fun i => ((j i).val : ℤ), by simp⟩
    · intro i
      convert weightedBoxes_single (lo := fun j _ k => boxLo j k)
        (hi := fun j _ k => boxHi j k)
        (label := fun j _ => (j.val : ℚ)) (j i) (fun _ => graphPoint (x i))
        (fun _ k => hj i k) using 1 <;> simp [graph]
  · intro v z a hz hy i
    obtain ⟨k, rfl⟩ := hz
    obtain ⟨hw, hs, hv, he⟩ := hy i
    apply integer_mixture_valid (fun j => a (finProdFinEquiv (i, j))) (v i) (k i) hw hs
    · exact hv 0
    · simpa using he 0

theorem rational_integer_upper (n : ℕ) : HasRationalIntegerLift n n := by
  apply hasRationalIntegerLift_of_rows integerRows
  have h := integerSystem_admissible n
  simpa only [Admissible, integerRows_iff, Set.mem_ofPred_eq] using h

/-- The integer construction uses three continuous weights and thirteen inequalities
per input coordinate, with rational coefficients. -/
theorem integer_upper_linear_size (n : ℕ) :
    ∃ rows : Fin (13 * n) → RationalAffine n n (n * 3),
      Admissible (rationalPolyhedron rows) (IntegerCodes n) := by
  let I := IntegerInequalityIndex n ⊕ (IntegerEqualityIndex n × Fin 2)
  have hc : Fintype.card I = 13 * n := integer_row_count n
  let e : I ≃ Fin (13 * n) := (Fintype.equivFin I).trans (finCongr hc)
  refine ⟨integerRows ∘ e.symm, ?_⟩
  have hset : rationalPolyhedron (integerRows ∘ e.symm) =
      {y | IntegerSystem y} := by
    ext y
    change (∀ r, (integerRows (e.symm r)).eval y ≤ 0) ↔ IntegerSystem y
    constructor
    · intro h
      apply (integerRows_iff y).mp
      intro r
      simpa only [Equiv.symm_apply_apply] using h (e r)
    · intro h r
      exact (integerRows_iff y).mpr h (e.symm r)
  rw [hset]
  exact integerSystem_admissible n

theorem integer_upper (n : ℕ) : HasIntegerLift n n :=
  (rational_integer_upper n).toHasIntegerLift

abbrev BoxLabels (n : ℕ) := Fin n → Fin 3
abbrev BinaryLabels (p : ℕ) := Fin p → Fin 2

def BinarySystem {n p : ℕ} (e : BoxLabels n ↪ BinaryLabels p)
    (y : Ambient n p (Fintype.card (BoxLabels n))) : Prop :=
  WeightedBoxes n p (fun j i k => boxLo (j i) k) (fun j i k => boxHi (j i) k)
    (fun j l => ((e j l).val : ℚ)) y.1 y.2.1
    (fun j => y.2.2 (Fintype.equivFin (BoxLabels n) j))

theorem binarySystem_admissible {n p : ℕ} (e : BoxLabels n ↪ BinaryLabels p) :
    Admissible {y | BinarySystem e y} (BinaryCodes p) := by
  classical
  constructor
  · intro x hx
    choose j hj using fun i => graph_in_box (hx i).1 (hx i).2
    refine ⟨fun l => ((e j l).val : ℝ), ?_,
      fun a => if (Fintype.equivFin (BoxLabels n)).symm a = j then 1 else 0, ?_⟩
    · intro l
      have h := (e j l).isLt
      have : (e j l).val = 0 ∨ (e j l).val = 1 := by omega
      rcases this with h | h <;> simp [h]
    · change WeightedBoxes n p _ _ _ _ _ _
      convert weightedBoxes_single (lo := fun j i k => boxLo (j i) k)
        (hi := fun j i k => boxHi (j i) k)
        (label := fun j l => ((e j l).val : ℚ)) j (graph x) (fun i k => hj i k) using 1 <;>
        simp
  · intro v z a hz hy
    rcases hy with ⟨hw, hs, hv, he⟩
    let w : BoxLabels n → ℝ := fun j => a (Fintype.equivFin (BoxLabels n) j)
    have hpositive : ∃ j, 0 < w j := by
      by_contra h
      push Not at h
      have hsum : ∑ j, w j ≤ 0 := Finset.sum_nonpos (fun j _ => h j)
      change (∑ j, w j) = 1 at hs
      linarith
    obtain ⟨j, hj⟩ := hpositive
    have hlabel : ∀ t l, ((e t l).val : ℚ) = 0 ∨ ((e t l).val : ℚ) = 1 := by
      intro t l
      have h := (e t l).isLt
      have : (e t l).val = 0 ∨ (e t l).val = 1 := by omega
      rcases this with h | h <;> simp [h]
    have support (t : BoxLabels n) (ht : 0 < w t) :
        ∀ l, (((e t l).val : ℚ) : ℝ) = z l :=
      binary_weight_support (fun t l => ((e t l).val : ℚ)) hlabel hw hs he hz ht
    have hjcode := support j hj
    have hzero (t : BoxLabels n) (hne : t ≠ j) : w t = 0 := by
      by_contra h
      have ht : 0 < w t := lt_of_le_of_ne (hw t) (Ne.symm h)
      have htcode := support t ht
      apply hne
      apply e.injective
      funext l
      apply Fin.ext
      have heq := (htcode l).trans (hjcode l).symm
      exact_mod_cast heq
    have weighted (c : BoxLabels n → ℝ) : (∑ t, w t * c t) = c j := by
      have hwj : w j = 1 := by
        calc w j = ∑ t, w t := by
               symm
               exact Finset.sum_eq_single j (fun t _ h => hzero t h) (by simp)
             _ = 1 := hs
      rw [Finset.sum_eq_single j]
      · simp [hwj]
      · intro t _ h; simp [hzero t h]
      · simp
    intro i
    apply inBox_valid (j := j i)
    intro k
    have h := hv i k
    change (∑ t, w t * (boxLo (t i) k : ℝ)) ≤ v i k ∧
      v i k ≤ ∑ t, w t * (boxHi (t i) k : ℝ) at h
    simpa only [weighted] using h

abbrev BinaryIneq (n : ℕ) := BoxLabels n ⊕ (Fin n × Fin 3 × Fin 2)
abbrev BinaryEq (p : ℕ) := Unit ⊕ Fin p

def binaryWeight (n p : ℕ) (j : BoxLabels n) :
    RationalAffine n p (Fintype.card (BoxLabels n)) :=
  .aux (Fintype.equivFin (BoxLabels n) j)

def binaryIneq (n p : ℕ) : BinaryIneq n →
    RationalAffine n p (Fintype.card (BoxLabels n))
  | .inl j => .scale (-1) (binaryWeight n p j)
  | .inr (i, k, s) => if s = 0 then
      .sub (.sum (fun j => .scale (boxLo (j i) k) (binaryWeight n p j))) (.visible i k)
    else .sub (.visible i k)
      (.sum (fun j => .scale (boxHi (j i) k) (binaryWeight n p j)))

def binaryEq {n p : ℕ} (e : BoxLabels n ↪ BinaryLabels p) : BinaryEq p →
    RationalAffine n p (Fintype.card (BoxLabels n))
  | .inl _ => .sub (.sum (binaryWeight n p)) (.const 1)
  | .inr l => .sub (.code l)
      (.sum (fun j => .scale ((e j l).val : ℚ) (binaryWeight n p j)))

def binaryRows {n p : ℕ} (e : BoxLabels n ↪ BinaryLabels p) :=
  systemRows (binaryIneq n p) (binaryEq e)

theorem mem_binaryRows {n p : ℕ} (e : BoxLabels n ↪ BinaryLabels p)
    (y : Ambient n p (Fintype.card (BoxLabels n))) :
    y ∈ rationalPolyhedron (binaryRows e) ↔ BinarySystem e y := by
  rw [binaryRows, mem_systemRows]
  simp only [BinarySystem, WeightedBoxes]
  constructor
  · rintro ⟨hi, he⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro j
      have h := hi (.inl j)
      simpa [binaryIneq, binaryWeight] using h
    · have h := he (.inl ())
      simpa [binaryEq, binaryWeight, sub_eq_zero] using h
    · intro i k
      have h₀ := hi (.inr (i, k, 0))
      have h₁ := hi (.inr (i, k, 1))
      constructor
      · simpa [binaryIneq, binaryWeight, mul_comm, sub_nonpos] using h₀
      · simpa [binaryIneq, binaryWeight, mul_comm, sub_nonpos] using h₁
    · intro l
      have h := he (.inr l)
      simpa [binaryEq, binaryWeight, mul_comm, sub_eq_zero] using h
  · rintro ⟨hw, hs, hv, hz⟩
    constructor
    · rintro (j | ⟨i, k, s⟩)
      · simpa [binaryIneq, binaryWeight] using hw j
      · fin_cases s
        · simpa [binaryIneq, binaryWeight, mul_comm, sub_nonpos] using (hv i k).1
        · simpa [binaryIneq, binaryWeight, mul_comm, sub_nonpos] using (hv i k).2
    · rintro (u | l)
      · simpa [binaryEq, binaryWeight, sub_eq_zero] using hs
      · simpa [binaryEq, binaryWeight, mul_comm, sub_eq_zero] using hz l

theorem binary_row_count (n p : ℕ) :
    Fintype.card (BinaryIneq n ⊕ (BinaryEq p × Fin 2)) =
      3 ^ n + 6 * n + 2 * p + 2 := by
  simp [BinaryIneq, BinaryEq, BoxLabels]
  omega

theorem rationalBinaryLift_of_embedding {n p : ℕ}
    (e : BoxLabels n ↪ BinaryLabels p) : HasRationalBinaryLift n p := by
  apply hasRationalBinaryLift_of_rows (binaryRows e)
  have h := binarySystem_admissible e
  simpa only [Admissible, mem_binaryRows, Set.mem_ofPred_eq] using h

/-- There are sufficiently many binary words exactly when the cardinality bound holds. -/
theorem boxLabel_embedding {n p : ℕ} (h : 3 ^ n ≤ 2 ^ p) :
    Nonempty (BoxLabels n ↪ BinaryLabels p) := by
  classical
  have hc : Fintype.card (BoxLabels n) ≤ Fintype.card (BinaryLabels p) := by
    simpa [BoxLabels, BinaryLabels, Fintype.card_fun] using h
  refine ⟨⟨fun j => (Fintype.equivFin (BinaryLabels p)).symm
    (Fin.castLE hc (Fintype.equivFin (BoxLabels n) j)), ?_⟩⟩
  intro j k heq
  apply (Fintype.equivFin (BoxLabels n)).injective
  have hf := congrArg (Fintype.equivFin (BinaryLabels p)) heq
  simp only [Equiv.apply_symm_apply] at hf
  apply Fin.ext
  exact congrArg (fun f : Fin (Fintype.card (BinaryLabels p)) => f.val) hf

theorem rational_binary_upper {n p : ℕ} (h : 3 ^ n ≤ 2 ^ p) :
    HasRationalBinaryLift n p := by
  obtain ⟨e⟩ := boxLabel_embedding h
  exact rationalBinaryLift_of_embedding e

theorem binary_upper {n p : ℕ} (h : 3 ^ n ≤ 2 ^ p) : HasBinaryLift n p :=
  (rational_binary_upper h).toHasBinaryLift

end
end ExactCounts
