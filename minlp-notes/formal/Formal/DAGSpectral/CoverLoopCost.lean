import Formal.DAGSpectral.CoverWholeExecution
import Formal.DAGSpectral.CoverCardinality
import Formal.DAGSpectral.CoverSizePolynomial

namespace DAGSpectral.CoverBitCost
open NormalizationTrials

/-- Every path in an executed candidate is an actual source-to-target path. -/
theorem candidateBitRun_path_length {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B K F C : ℕ)
    {es : List (Fin m)} (he : es ∈ (candidateBitRun G s t D η b B K F C).1) :
    es.length ≤ max 1 (v-1) := by
  have hh := List.mem_toFinset.mpr he
  rw [candidateBitRun_paths] at hh
  split_ifs at hh with hi
  · exact (trialPathSet_sound G s t D η b hh).1.length_le_vertices.trans
      (Nat.le_max_right _ _)
  · simp at hh

/-- A rank loop includes the actual enumeration work, every candidate gate and
trial, subset conversion, and copies of the returned paths. -/
theorem rankBitRun_work {v m p M r B K F C W S : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) (η : ℚ)
    (hw : ∀ b : Finset (Fin M), b.card=r →
      (candidateBitRun G s t D η b B K F C).2 ≤ W)
    (hc : ∀ b : Finset (Fin M), b.card=r →
      (candidateBitRun G s t D η b B K F C).1.length ≤ S) :
    (rankBitRun G s t D η r B K F C).2 ≤
      (M+1)^2 + enumerationCoefficient r*(M+1)^(r+2)*(M+1) +
        (1+M.choose r*((r+1)^2*(2*M+3)+1)) + (1+M.choose r*(W+S*(max 1 (v-1)*(m+1)+2)+2)) := by
  have he := sublistsCounted_bound r (List.finRange M)
  have hh := collectRuns_bound
    (fun b => candidateBitRun G s t D η b B K F C) (candidateBasisList r M)
    (fun b hb => hw b (mem_candidateBasisList.mp hb))
    (fun b hb => hc b (mem_candidateBasisList.mp hb))
    (fun b _ es hes => candidateBitRun_path_length G s t D η b B K F C hes)
  simp only [List.length_finRange] at he
  rw [candidateBasisList_length] at hh
  have hs := subsetsCounted_work (r := r) (sublistsCounted r (List.finRange M)).1 (by
    intro xs hx
    rw [sublistsCounted_value] at hx
    exact (List.length_of_sublistsLen hx).le)
  rw [sublistsCounted_length,List.length_finRange] at hs
  simp only [rankBitRun,finRangeCounted_value,subsetsCounted_value]
  exact Nat.add_le_add (Nat.add_le_add
    (Nat.add_le_add (finRangeCounted_work M) (Nat.mul_le_mul_right (M+1) he)) hs) hh

theorem rankBitRun_length {v m p M r B K F C S : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) (η : ℚ)
    (hc : ∀ b : Finset (Fin M), b.card=r →
      (candidateBitRun G s t D η b B K F C).1.length ≤ S) :
    (rankBitRun G s t D η r B K F C).1.length ≤ M.choose r*S := by
  have hh := collectRuns_length
    (fun b => candidateBitRun G s t D η b B K F C) (candidateBasisList r M)
    (fun b hb => hc b (mem_candidateBasisList.mp hb))
  rw [candidateBasisList_length] at hh
  simpa only [rankBitRun,finRangeCounted_value,subsetsCounted_value,candidateBasisList] using hh

theorem zeroBitRun_length {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (B : ℕ) : (zeroBitRun G s t D B).1.length ≤ 1 := by
  simp only [zeroBitRun]
  split_ifs <;> simp [List.length_take]

theorem rankBitRun_path_length {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (r B K F C : ℕ) {es : List (Fin m)}
    (he : es ∈ (rankBitRun G s t D η r B K F C).1) :
    es.length ≤ max 1 (v-1) := by
  have hh := List.mem_toFinset.mpr he
  rw [rankBitRun_paths] at hh
  obtain ⟨b,_,hb⟩ := Finset.mem_biUnion.mp hh
  exact (trialPathSet_sound G s t D η b hb).1.length_le_vertices.trans
    (Nat.le_max_right _ _)

def coverLoopBound (v m p Z R L : ℕ) : ℕ :=
  let N := max 1 (v-1)
  (p+1)^2 + Z + (1+p*(R+L*(N*(m+1)+2)+2)) + (1+(N*(m+1)+2)) +
    (1+p*L+1)^2*((2*N+1)*(m+1)+N*(m+1)+3) + v+1

/-- Compose the measured outer loop with bounds for the executed rank and zero
branches. This is a counting lemma; the branch bounds are supplied separately. -/
theorem coverBitRun_work {v m p M B Z R L : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) (η : ℚ)
    (K F C : ℕ → ℕ)
    (hz : (zeroBitRun G s t D B).2 ≤ Z)
    (hr : ∀ r : Fin p,
      (rankBitRun G s t D η (r.val+1) B (K (r.val+1)) (F (r.val+1)) (C (r.val+1))).2 ≤ R)
    (hl : ∀ r : Fin p,
      (rankBitRun G s t D η (r.val+1) B (K (r.val+1)) (F (r.val+1)) (C (r.val+1))).1.length ≤ L) :
    (coverBitRun G s t D η B K F C).2 ≤ coverLoopBound v m p Z R L := by
  let run := fun r : Fin p =>
    rankBitRun G s t D η (r.val+1) B (K (r.val+1)) (F (r.val+1)) (C (r.val+1))
  let positive := collectRuns run (List.finRange p)
  let zero := zeroBitRun G s t D B
  let merged := appendPathsCounted zero.1 positive.1
  have hp := collectRuns_bound run (List.finRange p) (fun r _ => hr r) (fun r _ => hl r)
    (fun r _ es hes => rankBitRun_path_length G s t D η _ _ _ _ _ hes)
  have hpl := collectRuns_length run (List.finRange p) (fun r _ => hl r)
  simp only [List.length_finRange] at hp hpl
  have hzl := zeroBitRun_length G s t D B
  have hzp : ∀ es ∈ zero.1, es.length ≤ max 1 (v-1) := by
    intro es hes
    have hh := List.mem_toFinset.mpr hes
    change es ∈ (zeroBitRun G s t D B).1.toFinset at hh
    rw [zeroBitRun_paths] at hh
    exact (zeroPathSet_sound G s t D hh).1.length_le_vertices.trans
      (Nat.le_max_right _ _)
  change zero.1.length ≤ 1 at hzl
  change positive.1.length ≤ p*L at hpl
  have happ := appendPathsCounted_bound zero.1 positive.1 hzp
  have happ' : merged.2 ≤ 1+(max 1 (v-1)*(m+1)+2) := by
    exact happ.trans (by simpa only [one_mul] using
      (Nat.add_le_add_left (Nat.mul_le_mul_right (max 1 (v-1)*(m+1)+2) hzl) 1))
  have hlen : merged.1.length ≤ 1+p*L := by
    simp only [merged,appendPathsCounted_value,List.length_append]
    omega
  have hpath : ∀ es ∈ merged.1, es.length ≤ max 1 (v-1) := by
    intro es hes
    simp only [merged,appendPathsCounted_value,List.mem_append] at hes
    rcases hes with hz' | hp'
    · exact hzp es hz'
    · simp only [positive,collectRuns_value,List.mem_flatMap] at hp'
      obtain ⟨r,_,he⟩ := hp'
      exact rankBitRun_path_length G s t D η _ _ _ _ _ he
  have hd := dedupCounted_bound merged.1 hpath
  have hd' := hd.trans (Nat.mul_le_mul_right _
    (Nat.pow_le_pow_left (Nat.add_le_add_right hlen 1) 2))
  have hinit := finRangeCounted_work p
  simp only [coverBitRun,finRangeCounted_value]
  split_ifs
  · dsimp
    dsimp only [coverLoopBound]
    omega
  · change (finRangeCounted p).2+zero.2+positive.2+merged.2+(dedupCounted merged.1).2+v+1 ≤ _
    dsimp only [coverLoopBound]
    change positive.2 ≤ _ at hp
    change zero.2 ≤ Z at hz
    omega

def rankLoopBound (v m p M W S : ℕ) : ℕ :=
  (M+1)^2 + (p+2)^2*(M+1)^(p+2)*(M+1) +
    (1+(M+1)^p*((p+1)^2*(2*M+3)+1)) +
    (1+(M+1)^p*(W+S*(max 1 (v-1)*(m+1)+2)+2))

/-- Uniform per-candidate bounds propagate through every executed branch. -/
theorem coverBitRun_work_of_candidates {v m p M B Z W S : ℕ}
    (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) (η : ℚ)
    (K F C : ℕ → ℕ)
    (hz : (zeroBitRun G s t D B).2 ≤ Z)
    (hw : ∀ b : Finset (Fin M), 0 < b.card → b.card ≤ p →
      (candidateBitRun G s t D η b B (K b.card) (F b.card) (C b.card)).2 ≤ W)
    (hc : ∀ b : Finset (Fin M), 0 < b.card → b.card ≤ p →
      (candidateBitRun G s t D η b B (K b.card) (F b.card) (C b.card)).1.length ≤ S) :
    (coverBitRun G s t D η B K F C).2 ≤
      coverLoopBound v m p Z (rankLoopBound v m p M W S) ((M+1)^p*S) := by
  apply coverBitRun_work G s t D η K F C hz
  · intro r
    have hwork := rankBitRun_work G s t D η
      (r := r.val+1) (B := B) (K := K (r.val+1)) (F := F (r.val+1)) (C := C (r.val+1))
      (fun b hb => by simpa only [← hb] using hw b (by omega) (by omega))
      (fun b hb => by simpa only [← hb] using hc b (by omega) (by omega))
    apply hwork.trans
    have hchoose := CoverSizePolynomial.choose_bound (M := M) (show r.val+1 ≤ p by omega)
    have hexp : (M+1)^(r.val+1+2) ≤ (M+1)^(p+2) :=
      Nat.pow_le_pow_right (by omega) (by omega)
    unfold enumerationCoefficient rankLoopBound
    gcongr <;> omega
  · intro r
    have hlen := rankBitRun_length G s t D η
      (r := r.val+1) (B := B) (K := K (r.val+1)) (F := F (r.val+1)) (C := C (r.val+1))
      (fun b hb => by simpa only [← hb] using hc b (by omega) (by omega))
    exact hlen.trans (Nat.mul_le_mul_right S
      (CoverSizePolynomial.choose_bound (show r.val+1 ≤ p by omega)))

end DAGSpectral.CoverBitCost
