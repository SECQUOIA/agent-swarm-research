import Formal.DAGSpectral.CoverBitCost
import Formal.DAGSpectral.CoverEnumerationCost
import Formal.DAGSpectral.CoverIndependenceExecution
import Formal.DAGSpectral.SubsetInputExecution
import Formal.DAGSpectral.BasisInputExecution

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators
namespace CoverBitCost
open NormalizationTrials CoverNormalizationExecution

/-- Execute the Gram gate before evaluating a candidate trial. -/
def candidateBitRun {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B K F C : ℕ) :
    List (List (Fin m)) × ℕ :=
  let basis := BasisInputExecution.basisRun D b
  let gate := independenceRun basis.1.columns
  let gateCost := basis.2 + traceBitWork (independenceBudget p b.card B) gate.events + gate.copies
  if gate.independent then
    let run := trialBitRun G s t D η b B K F C
    (run.1,gateCost+run.2+1)
  else ([],gateCost+1)

theorem candidateBitRun_paths {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B K F C : ℕ) :
    (candidateBitRun G s t D η b B K F C).1.toFinset =
      if independent D.vector b then trialPathSet G s t D η b else ∅ := by
  simp only [candidateBitRun,BasisInputExecution.basisRun_columns,independenceRun_code]
  split_ifs <;> simp_all [trialBitRun_paths]

/-- Enumerate all subsets of one rank, including the rejected dependent subsets. -/
def rankBitRun {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (r B K F C : ℕ) :
    List (List (Fin m)) × ℕ :=
  let identifiers := finRangeCounted M
  let enumeration := sublistsCounted r identifiers.1
  let subsets := subsetsCounted enumeration.1
  let result := collectRuns (fun b => candidateBitRun G s t D η b B K F C) subsets.1
  (result.1,identifiers.2+enumeration.2*(M+1)+subsets.2+result.2)

theorem rankBitRun_paths {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (r B K F C : ℕ) :
    (rankBitRun G s t D η r B K F C).1.toFinset =
      (trials D.vector r).biUnion (trialPathSet G s t D η) := by
  ext es
  simp only [rankBitRun,finRangeCounted_value,subsetsCounted_value,
    collectRuns_value,List.mem_toFinset,List.mem_flatMap,
    Finset.mem_biUnion]
  change (∃ b ∈ candidateBasisList r M,
    es ∈ (candidateBitRun G s t D η b B K F C).1) ↔ _
  simp only [← List.mem_toFinset, candidateBitRun_paths,candidateBasisList_toFinset,
    Finset.mem_powersetCard,Finset.subset_univ,true_and,mem_trials]
  constructor
  · rintro ⟨b,hcard,h⟩
    split_ifs at h with hind
    · exact ⟨b,⟨hcard,hind⟩,h⟩
    · simp at h
  · rintro ⟨b,⟨hcard,hind⟩,h⟩
    exact ⟨b,hcard,by simp [hind,h]⟩

/-- Exact zero tests execute both rational comparisons for every entry. -/
def matrixZeroRun {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    Bool × List ArithmeticEvent :=
  let cells := (List.ofFn fun i => (List.ofFn fun j =>
    [compareRun (A i j) 0,compareRun 0 (A i j)]).flatten).flatten
  (cells.all Prod.fst,(cells.map Prod.snd).flatten)

@[simp] theorem matrixZeroRun_value {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    (matrixZeroRun A).1 = decide (A=0) := by
  apply Bool.eq_iff_iff.mpr
  simp only [matrixZeroRun,List.all_flatten,all_ofFn,List.all_cons,List.all_nil,
    Bool.and_true,Bool.and_eq_true,compareRun_value,decide_eq_true_eq]
  constructor
  · intro h
    ext i j
    exact le_antisymm (h i j).1 (h i j).2
  · intro h
    subst A
    simp

/-- Cache every compared Boolean and charge the full Boolean scan. The control
count is taken from the actual cell list built by this execution. -/
def matrixZeroCacheRun {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    Bool × (List ArithmeticEvent × ℕ) :=
  let cells := (List.ofFn fun i => (List.ofFn fun j =>
    [compareRun (A i j) 0,compareRun 0 (A i j)]).flatten).flatten
  (cells.all Prod.fst,((cells.map Prod.snd).flatten,2*cells.length))

@[simp] theorem matrixZeroCacheRun_value {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    (matrixZeroCacheRun A).1 = (matrixZeroRun A).1 := rfl

@[simp] theorem matrixZeroCacheRun_events {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    (matrixZeroCacheRun A).2.1 = (matrixZeroRun A).2 := rfl

@[simp] theorem matrixZeroCacheRun_control {p : ℕ} (A : Matrix (Fin p) (Fin p) ℚ) :
    (matrixZeroCacheRun A).2.2 = 4*p*p := by
  simp [matrixZeroCacheRun,List.length_flatten,List.map_ofFn,
    Function.comp_def]
  ring

/-- The rank-zero branch caches every atom-zero test and retains at most one path. -/
def zeroBitRun {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (B : ℕ) : List (List (Fin m)) × ℕ :=
  let prior := matrixZeroCacheRun (D.atom none)
  let atoms := Vector.ofFn fun e => matrixZeroCacheRun (D.atom (some e))
  let pre := traceBitWork B prior.2.1 + prior.2.2 +
    (∑ e : Fin m, (traceBitWork B (atoms.get e).2.1 + (atoms.get e).2.2)) +
    atoms.toArray.size + 1
  if prior.1 then
    let result := G.outputBitCounted (fun e => (atoms.get e).1) s ∅
      (fun _ (_ : Fin 0) => (0 : ℤ)) t
    (result.1.take 1,pre+result.2+1)
  else ([],pre+1)

theorem zeroBitRun_paths {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (B : ℕ) :
    (zeroBitRun G s t D B).1.toFinset = zeroPathSet G s t D := by
  simp only [zeroBitRun,matrixZeroCacheRun_value,matrixZeroRun_value,Vector.get_ofFn]
  split_ifs with h
  · simp only [ExplicitDAG.outputBitCounted_paths]
    rw [zeroPathSet,if_pos (of_decide_eq_true h)]
  · simp only [List.toFinset_nil]
    rw [zeroPathSet,if_neg (by simpa using h)]

/-- Execute all ranks and form one duplicate-free output list. -/
def coverBitRun {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (B : ℕ) (K F C : ℕ → ℕ) :
    List (List (Fin m)) × ℕ :=
  if s=t then ([[]],v+1) else
    let ranks := finRangeCounted p
    let zero := zeroBitRun G s t D B
    let positive := collectRuns (fun r : Fin p =>
      rankBitRun G s t D η (r.val+1) B (K (r.val+1)) (F (r.val+1)) (C (r.val+1)))
      ranks.1
    let merged := appendPathsCounted zero.1 positive.1
    let unique := dedupCounted merged.1
    (unique.1,ranks.2+zero.2+positive.2+merged.2+unique.2+v+1)

theorem coverBitRun_paths {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (B : ℕ) (K F C : ℕ → ℕ) :
    (coverBitRun G s t D η B K F C).1.toFinset = spectralPathSet G s t D η := by
  unfold coverBitRun spectralPathSet
  split_ifs with h
  · simp
  · simp only [finRangeCounted_value,dedupCounted_finset,
      appendPathsCounted_value,List.toFinset_append,
      zeroBitRun_paths,collectRuns_value]
    congr 1
    ext es
    simp only [List.mem_toFinset,List.mem_flatMap,List.mem_finRange,true_and,
      Finset.mem_biUnion,Finset.mem_univ]
    constructor
    · rintro ⟨r,hr⟩
      have hh := List.mem_toFinset.mpr hr
      rw [rankBitRun_paths] at hh
      obtain ⟨b,hb,he⟩ := Finset.mem_biUnion.mp hh
      exact ⟨r,b,hb,he⟩
    · rintro ⟨r,b,hb,he⟩
      refine ⟨r,List.mem_toFinset.mp ?_⟩
      rw [rankBitRun_paths]
      exact Finset.mem_biUnion.mpr ⟨b,hb,he⟩

end CoverBitCost
end DAGSpectral
