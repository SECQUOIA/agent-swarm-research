import Formal.DAGSpectral.ProfileDPBitExecution

namespace DAGSpectral

private theorem representativeBitWork_weighted {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost reads : α → α → ℕ) (R : ℕ) (xs : List α) :
    representativeBitWork key (fun a b => cost a b+reads a b*R) xs =
      representativeBitWork key cost xs+representativeBitWork key reads xs*R := by
  have hs (a : α) (ys : List α) :
      (ys.map (fun b => cost a b+reads a b*R)).sum =
        (ys.map (cost a)).sum+(ys.map (reads a)).sum*R := by
    induction ys with
    | nil => simp
    | cons b ys ih => simp only [List.map_cons,List.sum_cons,ih]; ring
  induction xs with
  | nil => simp [representativeBitWork]
  | cons a xs ih => simp only [representativeBitWork,ih,hs]; ring

namespace ExplicitDAG
open scoped BigOperators
variable {v m : ℕ} {κ : Type*} [Fintype κ]

/-- A cached label lookup is charged for every profile coordinate read by every
actual comparison. The caller supplies its proved per-read storage cost. -/
def runCachedBitCounted (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) (R : ℕ) :
    ℕ → PathTable v m × ℕ
  | 0 => (fun _ => [],0)
  | n+1 =>
    let old := runCachedBitCounted G allowed s required label R n
    if hn : n < v then
      let t : Fin v := ⟨n,hn⟩
      let generated := candidates G allowed s t old.1
      let merged := representativesBitCounted (stateKey required label)
        (fun es fs => keyBitWork required label es fs+
          ((es.length+fs.length)*Fintype.card κ)*R) generated
      (Function.update old.1 t merged.1,
        old.2+merged.2+(m+1+v)*(v+m+1)^2+candidateCopyWork generated)
    else old

variable (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
  (required : Finset (Fin m)) (label : Fin m → κ → ℤ) (R : ℕ)

theorem runCachedBitCounted_table (n : ℕ) :
    (runCachedBitCounted G allowed s required label R n).1 =
      run G allowed s required label n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    by_cases hn : n < v <;>
      simp [runCachedBitCounted,run,hn,ih,representativesBitCounted_spec]

def vertexLabelAccessCost (k : ℕ) : ℕ :=
  if hk : k < v then representativeBitWork (stateKey required label)
    (fun es fs => (es.length+fs.length)*Fintype.card κ)
    (candidates G allowed s ⟨k,hk⟩ (run G allowed s required label k)) else 0

theorem runCachedBitCounted_cost (n : ℕ) :
    (runCachedBitCounted G allowed s required label R n).2 =
      (runBitCounted G allowed s required label n).2 +
        (∑ k ∈ Finset.range n,vertexLabelAccessCost G allowed s required label k)*R := by
  induction n with
  | zero => simp [runCachedBitCounted,runBitCounted]
  | succ n ih =>
    rw [Finset.sum_range_succ]
    by_cases hn : n < v <;>
      simp [runCachedBitCounted,runBitCounted,hn,ih,runCachedBitCounted_table,
        runBitCounted_table,representativesBitCounted_spec,representativeBitWork_weighted,
        vertexLabelAccessCost]; ring

theorem runCachedBitCounted_final_cost :
    (runCachedBitCounted G allowed s required label R v).2 =
      (runBitCounted G allowed s required label v).2 +
        labelAccessCount G allowed s required label*R := by
  rw [runCachedBitCounted_cost,← Fin.sum_univ_eq_sum_range]
  congr 2
  unfold labelAccessCount
  apply Finset.sum_congr rfl
  intro t _
  simp [vertexLabelAccessCost]

/-- Same actual terminal paths as the original DP, with cached-label reads
charged in the comparisons that perform those reads. -/
def outputCachedBitCounted (t : Fin v) : List (List (Fin m)) × ℕ :=
  let result := runCachedBitCounted G allowed s required label R v
  let terminal := result.1 t
  (terminal.filter (terminalOwnerCheck required),result.2+terminalMaskWork required terminal)

theorem outputCachedBitCounted_paths (t : Fin v) :
    (outputCachedBitCounted G allowed s required label R t).1 =
      output G allowed s t required label := by
  simp only [outputCachedBitCounted,runCachedBitCounted_table,output]
  congr 1
  funext es
  exact terminalOwnerCheck_eq required es

theorem outputCachedBitCounted_cost (t : Fin v) :
    (outputCachedBitCounted G allowed s required label R t).2 =
      (outputBitCounted G allowed s required label t).2+
        labelAccessCount G allowed s required label*R := by
  simp only [outputCachedBitCounted,outputBitCounted,runCachedBitCounted_table,
    runBitCounted_table,runCachedBitCounted_final_cost]
  omega

theorem outputCachedBitCounted_work (t : Fin v) :
    (outputCachedBitCounted G allowed s required label R t).2 ≤
      uncachedDPBitWork G allowed s required label R := by
  rw [outputCachedBitCounted_cost]
  exact Nat.add_le_add_right (outputBitCounted_work G allowed s required label t) _

end ExplicitDAG
end DAGSpectral
