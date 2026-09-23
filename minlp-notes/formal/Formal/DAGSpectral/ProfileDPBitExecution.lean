import Formal.DAGSpectral.SpectralAlgorithmCost

namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost

/-- Execute every comparison and accumulate its operand-dependent key charge. -/
def compareAllBitCounted {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) (a : α) : List α → Bool × ℕ
  | [] => (true,0)
  | b::xs =>
    let rest := compareAllBitCounted key cost a xs
    (decide (key a ≠ key b) && rest.1,rest.2+cost a b)

theorem compareAllBitCounted_spec {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) (a : α) (xs : List α) :
    compareAllBitCounted key cost a xs =
      (decide (∀ b ∈ xs, key a ≠ key b),(xs.map (cost a)).sum) := by
  induction xs with
  | nil => simp [compareAllBitCounted]
  | cons b xs ih => simp [compareAllBitCounted,ih,Nat.add_comm]

def representativesBitCounted {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) : List α → List α × ℕ
  | [] => ([],0)
  | a::xs =>
    let tail := representativesBitCounted key cost xs
    let checked := compareAllBitCounted key cost a tail.1
    (if checked.1 then a::tail.1 else tail.1,tail.2+checked.2)

theorem representativesBitCounted_spec {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) (xs : List α) :
    representativesBitCounted key cost xs =
      (representatives key xs,representativeBitWork key cost xs) := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp [representativesBitCounted,ih,compareAllBitCounted_spec,
      representatives,List.pwFilter,representativeBitWork]

namespace ExplicitDAG
open scoped BigOperators
variable {v m : ℕ} {κ : Type*} [Fintype κ]

/-- Copy every generated candidate's edge identifiers; the empty seed costs zero. -/
def candidateCopyWork (xs : List (List (Fin m))) : ℕ :=
  (xs.map fun es => es.length*(m+1)).sum

/-- The eager producer charges inspected incoming edges, vertex-table access and
update, copied candidate paths, and the actual full-scan key computations. -/
def runBitCounted (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ → PathTable v m × ℕ
  | 0 => (fun _ => [],0)
  | n+1 =>
    let old := runBitCounted G allowed s required label n
    if hn : n < v then
      let t : Fin v := ⟨n,hn⟩
      let generated := candidates G allowed s t old.1
      let merged := representativesBitCounted (stateKey required label)
        (keyBitWork required label) generated
      (Function.update old.1 t merged.1,
        old.2+merged.2+(m+1+v)*(v+m+1)^2+candidateCopyWork generated)
    else old

variable (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
  (required : Finset (Fin m)) (label : Fin m → κ → ℤ)

theorem runBitCounted_table (n : ℕ) :
    (runBitCounted G allowed s required label n).1 = run G allowed s required label n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    by_cases hn : n < v <;>
      simp [runBitCounted,run,hn,ih,representativesBitCounted_spec]

def vertexBitCost (k : ℕ) : ℕ :=
  if hk : k < v then
    let generated := candidates G allowed s ⟨k,hk⟩ (run G allowed s required label k)
    representativeBitWork (stateKey required label) (keyBitWork required label) generated +
      (m+1+v)*(v+m+1)^2+candidateCopyWork generated
  else 0

theorem runBitCounted_cost (n : ℕ) :
    (runBitCounted G allowed s required label n).2 =
      ∑ k ∈ Finset.range n, vertexBitCost G allowed s required label k := by
  induction n with
  | zero => simp [runBitCounted]
  | succ n ih =>
    rw [Finset.sum_range_succ]
    by_cases hn : n < v <;>
      simp [runBitCounted,hn,ih,runBitCounted_table,representativesBitCounted_spec,
        vertexBitCost,Nat.add_assoc]

theorem candidateCopyWork_bound (t : Fin v) :
    candidateCopyWork (candidates G allowed s t (run G allowed s required label t.val)) ≤
      (transitionCandidates G allowed t (run G allowed s required label t.val)).length *
        (v+1)*(m+1) := by
  have he : candidateCopyWork
      (candidates G allowed s t (run G allowed s required label t.val)) =
      candidateCopyWork
        (transitionCandidates G allowed t (run G allowed s required label t.val)) := by
    rw [candidates_decomposition]
    simp only [candidateCopyWork,List.map_append,List.sum_append]
    split_ifs <;> simp
  rw [he]
  unfold candidateCopyWork
  have hh := List.sum_le_card_nsmul
    ((transitionCandidates G allowed t (run G allowed s required label t.val)).map
      fun es => es.length*(m+1)) ((v+1)*(m+1)) (by
      intro z hz
      obtain ⟨es,hes,rfl⟩ := List.mem_map.mp hz
      have hc : es ∈ candidates G allowed s t (run G allowed s required label t.val) := by
        rw [candidates_decomposition]
        exact List.mem_append_right _ hes
      have hp := candidates_sound G allowed s _ t
        (fun u zs hzs => run_sound G allowed s required label t.val u zs hzs) hc
      have hlen := hp.1.length_le_vertices
      exact Nat.mul_le_mul_right (m+1) (by omega : es.length ≤ v+1))
  simpa [Nat.mul_assoc] using hh

theorem runBitCounted_final_bound :
    (runBitCounted G allowed s required label v).2 ≤
      comparisonBitWork G allowed s required label +
        (v*(m+1)+v*v)*(v+m+1)^2 +
        edgeExtensions G allowed s required label*(v+1)*(m+1) := by
  rw [runBitCounted_cost,← Fin.sum_univ_eq_sum_range]
  have hv : (∑ t : Fin v, vertexBitCost G allowed s required label t.val) =
      comparisonBitWork G allowed s required label + v*((m+1+v)*(v+m+1)^2) +
      ∑ t : Fin v, candidateCopyWork
        (candidates G allowed s t (run G allowed s required label t.val)) := by
    simp [vertexBitCost,comparisonBitWork,Finset.sum_add_distrib]
  rw [hv]
  have hc := Finset.sum_le_sum (fun t (_ : t ∈ Finset.univ) =>
    candidateCopyWork_bound G allowed s required label t)
  rw [← Finset.sum_mul,← Finset.sum_mul,← edgeExtensions_eq_generated] at hc
  nlinarith

/-- Terminal mask filtering is performed on each stored terminal path. -/
def terminalMaskWork (xs : List (List (Fin m))) : ℕ :=
  (xs.map fun es => (required.card+1)*(es.length+1)*(m+1)).sum

/-- Scan each required owner directly in the path. No path-to-finset
construction or duplicate elimination is performed by this predicate. -/
def terminalOwnerCheck (required : Finset (Fin m)) (es : List (Fin m)) : Bool :=
  decide (∀ e ∈ required, e ∈ es)

theorem terminalOwnerCheck_eq (required : Finset (Fin m)) (es : List (Fin m)) :
    terminalOwnerCheck required es = decide (ownerMask required es = required) := by
  simp [terminalOwnerCheck,ownerMask,Finset.inter_eq_left,Finset.subset_iff]

def outputBitCounted (t : Fin v) : List (List (Fin m)) × ℕ :=
  let result := runBitCounted G allowed s required label v
  let terminal := result.1 t
  (terminal.filter (terminalOwnerCheck required),
    result.2+terminalMaskWork required terminal)

theorem outputBitCounted_paths (t : Fin v) :
    (outputBitCounted G allowed s required label t).1 = output G allowed s t required label := by
  simp only [outputBitCounted,output,runBitCounted_table]
  congr 1
  funext es
  exact terminalOwnerCheck_eq required es

theorem terminalMaskWork_bound (t : Fin v) :
    terminalMaskWork required (run G allowed s required label v t) ≤
      storedStates G allowed s required label v*(required.card+1)*(v+1)*(m+1) := by
  have hh := List.sum_le_card_nsmul
    ((run G allowed s required label v t).map fun es =>
      (required.card+1)*(es.length+1)*(m+1)) ((required.card+1)*(v+1)*(m+1)) (by
      intro z hz
      obtain ⟨es,hes,rfl⟩ := List.mem_map.mp hz
      have hp := (run_sound G allowed s required label v t es hes).1.length_le_vertices
      gcongr
      omega)
  have hs : (run G allowed s required label v t).length ≤
      storedStates G allowed s required label v := by
    unfold storedStates
    exact Finset.single_le_sum (f := fun u : Fin v =>
      (run G allowed s required label v u).length)
      (fun _ _ => Nat.zero_le _) (Finset.mem_univ t)
  unfold terminalMaskWork
  have ht : ((run G allowed s required label v t).map fun es =>
      (required.card+1)*(es.length+1)*(m+1)).sum ≤
      (run G allowed s required label v t).length*((required.card+1)*(v+1)*(m+1)) := by
    simpa using hh
  exact ht.trans (by simpa [Nat.mul_assoc] using
    Nat.mul_le_mul_right ((required.card+1)*(v+1)*(m+1)) hs)

/-- The measured charge belongs to a producer returning the actual output.
The bound is proved from the operations it accumulated, not returned as a cost. -/
theorem outputBitCounted_work (t : Fin v) :
    (outputBitCounted G allowed s required label t).2 ≤ dpBitWork G allowed s required label := by
  have hr := runBitCounted_final_bound G allowed s required label
  have ht := terminalMaskWork_bound G allowed s required label t
  simp only [outputBitCounted,runBitCounted_table]
  unfold dpBitWork
  omega

end ExplicitDAG
end DAGSpectral
