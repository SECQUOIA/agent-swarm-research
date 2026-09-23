import Formal.Scalar
import Formal.UpperCore
import Formal.RationalPolyhedron

namespace ExactCounts
noncomputable section
variable {n : ℕ}

def IntegerSystem (y : Ambient n n (n * 3)) : Prop :=
  ∀ i, WeightedBoxes 1 1 (fun j _ k => boxLo j k) (fun j _ k => boxHi j k)
    (fun j _ => (j.val : ℚ)) (fun _ => y.1 i) (fun _ => y.2.1 i)
    (fun j => y.2.2 (finProdFinEquiv (i, j)))

abbrev IntegerInequalityIndex (n : ℕ) :=
  (Fin n × Fin 3) ⊕ (Fin n × Fin 3 × Fin 2)
abbrev IntegerEqualityIndex (n : ℕ) := Fin n × Fin 2

def integerWeightExpr (i : Fin n) (j : Fin 3) : RationalAffine n n (n * 3) :=
  .aux (finProdFinEquiv (i, j))

def integerInequalities : IntegerInequalityIndex n → RationalAffine n n (n * 3)
  | .inl (i, j) => .scale (-1) (integerWeightExpr i j)
  | .inr (i, k, s) => if s = 0 then
      .sub (.sum (fun j => .scale (boxLo j k) (integerWeightExpr i j))) (.visible i k)
    else
      .sub (.visible i k) (.sum (fun j => .scale (boxHi j k) (integerWeightExpr i j)))

def integerEqualities : IntegerEqualityIndex n → RationalAffine n n (n * 3)
  | (i, s) => if s = 0 then
      .sub (.sum (fun j => integerWeightExpr i j)) (.const 1)
    else
      .sub (.code i) (.sum (fun j => .scale (j.val : ℚ) (integerWeightExpr i j)))

def integerRows := @systemRows n n (n * 3) (IntegerInequalityIndex n)
  (IntegerEqualityIndex n) integerInequalities integerEqualities

theorem integerRows_iff (y : Ambient n n (n * 3)) :
    y ∈ rationalPolyhedron integerRows ↔ IntegerSystem y := by
  rw [integerRows, mem_systemRows]
  constructor
  · rintro ⟨hi, he⟩ i
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro j
      have h := hi (.inl (i, j))
      simpa [integerInequalities, integerWeightExpr] using h
    · have h := he (i, 0)
      simpa [integerEqualities, integerWeightExpr, sub_eq_zero] using h
    · intro a k
      have hl := hi (.inr (i, k, 0))
      have hu := hi (.inr (i, k, 1))
      constructor
      · simpa [integerInequalities, integerWeightExpr, mul_comm] using hl
      · simpa [integerInequalities, integerWeightExpr, mul_comm] using hu
    · intro a
      have h := he (i, 1)
      simpa [integerEqualities, integerWeightExpr, mul_comm, sub_eq_zero] using h
  · intro h
    constructor
    · intro r
      rcases r with ⟨i, j⟩ | ⟨i, k, s⟩
      · simpa [integerInequalities, integerWeightExpr] using (h i).1 j
      · fin_cases s
        · simpa [integerInequalities, integerWeightExpr, mul_comm] using (h i).2.2.1 0 k |>.1
        · simpa [integerInequalities, integerWeightExpr, mul_comm] using (h i).2.2.1 0 k |>.2
    · rintro ⟨i, s⟩
      fin_cases s
      · simpa [integerEqualities, integerWeightExpr, sub_eq_zero] using (h i).2.1
      · simpa [integerEqualities, integerWeightExpr, mul_comm, sub_eq_zero] using (h i).2.2.2 0

theorem integer_row_count (n : ℕ) :
    Fintype.card (IntegerInequalityIndex n ⊕ (IntegerEqualityIndex n × Fin 2)) = 13 * n := by
  simp [IntegerInequalityIndex, IntegerEqualityIndex]
  omega

end
end ExactCounts
