import Formal.DAGSpectral.NormalizationData
import Formal.DAGSpectral.TrialApproximation

namespace DAGSpectral
open Matrix
namespace NormalizationTrials
variable {v m p M : ℕ}

/-- The trial's exact atom filter on the original edge identities. -/
def trialAllowed (D : FactorData p m M) (b : Finset (Fin M)) : Fin m → Bool :=
  fun e => decide (acceptsAtomCode D.vector D.weight b (D.atom (some e)))

def trialAtom (D : FactorData p m M) (b : Finset (Fin M))
    (o : Option (Fin m)) : Matrix (Fin b.card) (Fin b.card) ℚ :=
  let T := transformCode D.vector D.weight b
  T * D.atom o * Tᵀ

/-- An actual DP run; only the common prior is tested outside the graph. -/
def trialPathSet (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M)
    (η : ℚ) (b : Finset (Fin M)) : Finset (List (Fin m)) :=
  if acceptsAtomCode D.vector D.weight b (D.atom none) then
    (G.output (trialAllowed D b) s t (forcedOwners D.owner b)
      (rationalUpperLabels (η / (b.card * max 1 (v-1) : ℚ))
        (fun e => trialAtom D b (some e)))).toFinset
  else ∅

/-- At most one actual path through zero atoms is needed for rank zero. -/
def zeroPathSet (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M) :
    Finset (List (Fin m)) :=
  if D.atom none = 0 then
    ((G.output (fun e => decide (D.atom (some e) = 0)) s t ∅
      (fun _ (_ : Fin 0) => (0 : ℤ))).take 1).toFinset
  else ∅

/-- The finite cover is produced before a scalar criterion is chosen. -/
def spectralPathSet (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M)
    (η : ℚ) : Finset (List (Fin m)) :=
  if s = t then {[]} else
    zeroPathSet G s t D ∪
      Finset.univ.biUnion (fun r : Fin p =>
        (trials D.vector (r.val+1)).biUnion (trialPathSet G s t D η))

theorem trialPathSet_sound (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M)
    (η : ℚ) (b : Finset (Fin M)) {es : List (Fin m)}
    (he : es ∈ trialPathSet G s t D η b) :
    G.Path s t es ∧ acceptsSelection D.vector D.weight D.owner b D.atom es.toFinset := by
  unfold trialPathSet at he
  split_ifs at he with h0
  · have hh := G.output_sound (trialAllowed D b) s (forcedOwners D.owner b)
      (rationalUpperLabels (η / (b.card * max 1 (v-1) : ℚ))
        (fun e => trialAtom D b (some e))) t (List.mem_toFinset.mp he)
    refine ⟨hh.1.1, hh.2, (acceptsAtomCode_iff _ _ _ _).mp h0, ?_⟩
    intro e he
    have hp := hh.1.2 e (List.mem_toFinset.mp he)
    exact (acceptsAtomCode_iff _ _ _ _).mp (of_decide_eq_true hp)
  · simp at he

theorem zeroPathSet_sound (G : ExplicitDAG v m) (s t : Fin v) (D : FactorData p m M)
    {es : List (Fin m)} (he : es ∈ zeroPathSet G s t D) :
    G.Path s t es ∧ D.atom none = 0 ∧ ∀ e ∈ es, D.atom (some e) = 0 := by
  unfold zeroPathSet at he
  split_ifs at he with h0
  · have hh := G.output_sound (fun e => decide (D.atom (some e) = 0)) s ∅
      (fun _ (_ : Fin 0) => (0 : ℤ)) t
      (List.mem_of_mem_take (List.mem_toFinset.mp he))
    exact ⟨hh.1.1,h0,fun e he => of_decide_eq_true (hh.1.2 e he)⟩
  · simp at he

theorem spectralPathSet_sound (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) {es : List (Fin m)}
    (he : es ∈ spectralPathSet G s t D η) : G.Path s t es := by
  unfold spectralPathSet at he
  split_ifs at he with hst
  · have : es = [] := Finset.mem_singleton.mp he
    subst es
    subst t
    exact .nil
  · rcases Finset.mem_union.mp he with hz | hp
    · exact (zeroPathSet_sound G s t D hz).1
    · obtain ⟨r,_,hrep⟩ := Finset.mem_biUnion.mp hp
      obtain ⟨b,_,he⟩ := Finset.mem_biUnion.mp hrep
      exact (trialPathSet_sound G s t D η b he).1

end NormalizationTrials
end DAGSpectral
