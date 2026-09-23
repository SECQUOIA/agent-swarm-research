import Formal.MatroidSpectral.ExecutionCandidate
import Formal.DAGSpectral.FactorInputData

namespace MatroidSpectral.Execution
open DAGSpectral DAGSpectral.NormalizationTrials ReciprocalAnchor
open scoped BigOperators

def rankRun {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (r B : ℕ) : List (Finset (Fin m)) × ℕ :=
  let enumeration := candidateSubsetsRun r M
  let result := collect (fun b => candidateRun A D η b B) (columnWork m) enumeration.1
  (result.1, enumeration.2 + result.2)

theorem rankRun_value {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (r B : ℕ) :
    (rankRun A D η r B).1.toFinset =
      (trials D.vector r).biUnion (trialBasisSet A D η) := by
  ext E
  simp only [rankRun, collect_value, candidateSubsetsRun_value, List.mem_toFinset,
    List.mem_flatMap, Finset.mem_biUnion]
  simp only [← List.mem_toFinset, candidateRun_value, CoverBitCost.candidateBasisList_toFinset,
    Finset.mem_powersetCard, Finset.subset_univ, true_and, mem_trials]
  constructor
  · rintro ⟨b,hcard,h⟩
    split_ifs at h with hi
    · exact ⟨b,⟨hcard,hi⟩,h⟩
    · simp at h
  · rintro ⟨b,⟨hcard,hi⟩,h⟩
    exact ⟨b,hcard,by simp [hi,h]⟩

theorem rankRun_length {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (r B : ℕ) :
    (rankRun A D η r B).1.length ≤ M.choose r * candidateCapacity q p r η := by
  have hh := collect_length (fun b => candidateRun A D η b B) (columnWork m)
    (candidateCapacity q p r η) (candidateSubsetsRun r M).1 (by
      intro b hb
      simpa only [mem_candidateSubsetsRun.mp hb] using candidateRun_length A D η b B)
  simpa only [rankRun, candidateSubsetsRun_length] using hh

def rankWorkBound (q p m M r B : ℕ) (η : ℚ) : ℕ :=
  candidateSubsetsWorkBound r M + M.choose r *
    (candidateWorkBound q p m M r B η + candidateCapacity q p r η * (columnWork m + 1) + 1)

theorem rankRun_work {q p m M B r : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η) (hq : 0 < q) (hr : 0 < r)
    (hA : MatrixBits A B) (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B) (hD : ∀ o, MatrixBits (D.atom o) B)
    (hηB : RationalBits η B) (hsize : r + q + 2 ≤ B) :
    (rankRun A D η r B).2 ≤ rankWorkBound q p m M r B η := by
  have he := candidateSubsetsRun_work r M
  have hc := collect_work (fun b => candidateRun A D η b B) (columnWork m)
    (candidateWorkBound q p m M r B η) (candidateCapacity q p r η)
    (candidateSubsetsRun r M).1 (by
      intro b hb
      have heq := mem_candidateSubsetsRun.mp hb
      simpa only [heq] using candidateRun_work A D hη hq b (by omega)
        hA hV hw hD hηB (by omega)) (by
      intro b hb
      simpa only [mem_candidateSubsetsRun.mp hb] using candidateRun_length A D η b B)
  simpa only [rankRun, rankWorkBound, candidateSubsetsRun_length] using Nat.add_le_add he hc

def coverRun {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (B : ℕ) : List (Finset (Fin m)) × ℕ :=
  if q = 0 then ([∅], 1) else
    let zero := zeroRun A D B
    let positive := collect (fun r : Fin p => rankRun A D η (r.val + 1) B)
      (columnWork m) (List.finRange p)
    (zero.1 ++ positive.1,
      zero.2 + positive.2 + (p + 1) ^ 2 + zero.1.length * columnWork m + 1)

theorem coverRun_value {q p m M : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (η : ℚ) (B : ℕ) :
    (coverRun A D η B).1.toFinset = spectralBasisSet A D η := by
  by_cases hq : q = 0
  · simp [coverRun, spectralBasisSet, hq]
  · simp only [coverRun, spectralBasisSet, if_neg hq, List.toFinset_append, zeroRun_value]
    congr 1
    ext E
    simp only [collect_value, List.mem_toFinset, List.mem_flatMap, List.mem_finRange,
      true_and, Finset.mem_biUnion, Finset.mem_univ]
    simp only [← List.mem_toFinset, rankRun_value, Finset.mem_biUnion]

theorem coverRun_cast {q p m M N : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) (h : M = N) (η : ℚ) (B : ℕ) :
    coverRun A (castFactorData h D) η B = coverRun A D η B := by
  subst N
  rfl

def coverWorkBound (q p m M B : ℕ) (η : ℚ) : ℕ :=
  zeroWorkBound q p m B +
    (∑ r : Fin p, (rankWorkBound q p m M (r.val + 1) B η +
      M.choose (r.val + 1) * candidateCapacity q p (r.val + 1) η * (columnWork m + 1) + 1)) +
    (p + 1) ^ 2 + columnWork m + 1

theorem coverRun_work {q p m M B : ℕ} (A : RationalRepresentation q m)
    (D : FactorData p m M) {η : ℚ} (hη : 0 < η)
    (hA : MatrixBits A B) (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B) (hD : ∀ o, MatrixBits (D.atom o) B)
    (hηB : RationalBits η B) (hsize : p + q + 2 ≤ B) :
    (coverRun A D η B).2 ≤ coverWorkBound q p m M B η := by
  by_cases hq : q = 0
  · simp only [coverRun, if_pos hq, coverWorkBound]
    omega
  · have hz := zeroRun_work A D hA hD
    have hzl := Nat.mul_le_mul_right (columnWork m) (zeroRun_length A D B)
    have hr := collect_sum_work (fun r : Fin p => rankRun A D η (r.val + 1) B)
      (columnWork m) (fun r => rankWorkBound q p m M (r.val + 1) B η)
      (fun r => M.choose (r.val + 1) * candidateCapacity q p (r.val + 1) η)
      (List.finRange p) (by
        intro r _
        exact rankRun_work A D hη (Nat.pos_of_ne_zero hq) (by omega)
          hA hV hw hD hηB (by omega))
      (fun r _ => rankRun_length A D η (r.val + 1) B)
    simp only [← List.ofFn_eq_map, List.sum_ofFn] at hr
    simp only [coverRun, if_neg hq, coverWorkBound]
    omega

end MatroidSpectral.Execution
