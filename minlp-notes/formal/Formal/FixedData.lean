import Formal.IntegerPolyhedron

namespace ExactCounts

noncomputable section

namespace RationalAffine

variable {n p q : ℕ}

/-- All rational literals in an affine expression, including multiplication coefficients. -/
def data : RationalAffine n p q → Finset ℚ
  | .const r => {r}
  | .visible _ _ => ∅
  | .code _ => ∅
  | .aux _ => ∅
  | .add e f => e.data ∪ f.data
  | .scale r e => insert r e.data

theorem data_sub_subset {e f : RationalAffine n p q} {S : Finset ℚ}
    (hneg : -1 ∈ S) (he : e.data ⊆ S) (hf : f.data ⊆ S) : (e.sub f).data ⊆ S := by
  exact Finset.union_subset he (Finset.insert_subset_iff.mpr ⟨hneg, hf⟩)

theorem data_listSum_subset {es : List (RationalAffine n p q)} {S : Finset ℚ}
    (hzero : 0 ∈ S) (hes : ∀ e ∈ es, e.data ⊆ S) : (listSum es).data ⊆ S := by
  induction es with
  | nil => simpa [listSum, data] using hzero
  | cons e es ih =>
    have he := hes e (by simp)
    have ht := ih (fun f hf => hes f (by simp [hf]))
    exact Finset.union_subset he ht

theorem data_sum_subset {ι : Type} [Fintype ι] {f : ι → RationalAffine n p q}
    {S : Finset ℚ} (hzero : 0 ∈ S) (hf : ∀ i, (f i).data ⊆ S) : (sum f).data ⊆ S := by
  apply data_listSum_subset hzero
  intro e he
  obtain ⟨i, _, rfl⟩ := List.mem_map.mp he
  exact hf i

end RationalAffine

/-- A fixed finite alphabet for every dimension of the integer formulation. -/
def integerDataAlphabet : Finset ℚ :=
  {-1, 0, 1, 2} ∪
    Finset.univ.image (fun jk : Fin 3 × Fin 3 => boxLo jk.1 jk.2) ∪
    Finset.univ.image (fun jk : Fin 3 × Fin 3 => boxHi jk.1 jk.2)

theorem integerDataAlphabet_neg_one : -1 ∈ integerDataAlphabet := by
  simp [integerDataAlphabet]

theorem integerDataAlphabet_zero : 0 ∈ integerDataAlphabet := by
  simp [integerDataAlphabet]

theorem integerDataAlphabet_one : 1 ∈ integerDataAlphabet := by
  simp [integerDataAlphabet]

theorem integerDataAlphabet_label (j : Fin 3) : (j.val : ℚ) ∈ integerDataAlphabet := by
  fin_cases j <;> simp [integerDataAlphabet]

theorem integerDataAlphabet_lo (j k : Fin 3) : boxLo j k ∈ integerDataAlphabet := by
  apply Finset.mem_union_left
  apply Finset.mem_union_right
  exact Finset.mem_image.mpr ⟨(j, k), Finset.mem_univ _, rfl⟩

theorem integerDataAlphabet_hi (j k : Fin 3) : boxHi j k ∈ integerDataAlphabet := by
  apply Finset.mem_union_right
  exact Finset.mem_image.mpr ⟨(j, k), Finset.mem_univ _, rfl⟩

theorem integerInequalities_data_subset (n : ℕ) (r : IntegerInequalityIndex n) :
    (integerInequalities r).data ⊆ integerDataAlphabet := by
  rcases r with ⟨i, j⟩ | ⟨i, k, s⟩
  · simpa [integerInequalities, integerWeightExpr, RationalAffine.data] using
      integerDataAlphabet_neg_one
  · dsimp only [integerInequalities]
    split
    · apply RationalAffine.data_sub_subset integerDataAlphabet_neg_one
      · apply RationalAffine.data_sum_subset integerDataAlphabet_zero
        intro j
        simpa [integerWeightExpr, RationalAffine.data] using integerDataAlphabet_lo j k
      · simp [RationalAffine.data]
    · apply RationalAffine.data_sub_subset integerDataAlphabet_neg_one
      · simp [RationalAffine.data]
      · apply RationalAffine.data_sum_subset integerDataAlphabet_zero
        intro j
        simpa [integerWeightExpr, RationalAffine.data] using integerDataAlphabet_hi j k

theorem integerEqualities_data_subset (n : ℕ) (r : IntegerEqualityIndex n) :
    (integerEqualities r).data ⊆ integerDataAlphabet := by
  rcases r with ⟨i, s⟩
  dsimp only [integerEqualities]
  split
  · apply RationalAffine.data_sub_subset integerDataAlphabet_neg_one
    · apply RationalAffine.data_sum_subset integerDataAlphabet_zero
      intro j
      simp [integerWeightExpr, RationalAffine.data]
    · simpa [RationalAffine.data] using integerDataAlphabet_one
  · apply RationalAffine.data_sub_subset integerDataAlphabet_neg_one
    · simp [RationalAffine.data]
    · apply RationalAffine.data_sum_subset integerDataAlphabet_zero
      intro j
      simpa [integerWeightExpr, RationalAffine.data] using integerDataAlphabet_label j

/-- No new rational numerical data appear when the dimension increases. -/
theorem integerRows_data_subset (n : ℕ)
    (r : IntegerInequalityIndex n ⊕ (IntegerEqualityIndex n × Fin 2)) :
    (integerRows r).data ⊆ integerDataAlphabet := by
  rcases r with r | ⟨r, s⟩
  · exact integerInequalities_data_subset n r
  · change (if s = 0 then integerEqualities r else
      RationalAffine.scale (-1) (integerEqualities r)).data ⊆ integerDataAlphabet
    split
    · exact integerEqualities_data_subset n r
    · simpa [RationalAffine.data, Finset.insert_subset_iff] using
        ⟨integerDataAlphabet_neg_one, integerEqualities_data_subset n r⟩

end

end ExactCounts
