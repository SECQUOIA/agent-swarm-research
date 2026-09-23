import Formal.DAGSpectral.CoverExecution
import Formal.DAGSpectral.CoverCacheCost
import Formal.DAGSpectral.BasisInputExecution
import Formal.DAGSpectral.CacheStorageExecution
import Formal.DAGSpectral.ProfileDPCacheExecution

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators
namespace CoverBitCost
open NormalizationTrials CoverNormalizationExecution BasisInputExecution

/-- Execute the mesh arithmetic rather than treating the quotient as a free input. -/
def meshRun (η : ℚ) (r N : ℕ) : ℚ × List ArithmeticEvent :=
  (ArithmeticExpr.op .div (.atom η)
    (.op .mul (.atom r) (.atom N))).run

@[simp] theorem meshRun_value (η : ℚ) (r N : ℕ) :
    (meshRun η r N).1 = η / (r*N : ℚ) := by
  simp [meshRun,ArithmeticExpr.run_eq,ArithmeticExpr.eval,primitiveResult]

/-- One stored integer read includes the edge address, the two square-cache
indices, and the copied label's digit bound. -/
def trialLabelReadCost (m r F C : ℕ) : ℕ := (m+1)*(r+1)^2*(F+C+2)

/-- One trial uses eager matrix and label caches and the executed profile DP.
A rejected prior produces no paths. -/
def trialBitRun {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B K F C : ℕ) :
    List (List (Fin m)) × ℕ :=
  let basis := basisRun D b
  let scales := scalesRun basis.1.weights
  let mesh := meshRun η b.card (max 1 (v-1))
  let cache := trialRun basis.1.columns (fun i => (scales.get i).1) D.atom mesh.1
  let pre := traceBitWork (13*B+4) (List.ofFn fun i => (scales.get i).2).flatten +
    traceBitWork (3*B+1) mesh.2 + cacheWork cache K F C + basis.2 + cache.copies +
      RationalStorage.vectorCopy (fun i => (scales.get i).1) + b.card+1 +
      RationalStorage.scalarCopy mesh.1
  if cache.prior.accepted then
    let result := G.outputCachedBitCounted (fun e => (cache.atoms.get e).accepted) s
      basis.1.required (fun e => (cache.labels.get e).value)
      (trialLabelReadCost m b.card F C) t
    (result.1,pre+result.2+1)
  else ([],pre+1)

theorem trialBitRun_paths {v m p M : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (b : Finset (Fin M)) (B K F C : ℕ) :
    (trialBitRun G s t D η b B K F C).1.toFinset = trialPathSet G s t D η b := by
  have hs : (fun i => ((scalesRun (fun j => D.weight (label b j))).get i).1) =
      scales D.weight b := by
    funext i
    simp [NormalizationBits.actualScales,NormalizationBits.actualWeightBits,
      scales,scale,weightBits]
  have hatom : (fun e => (trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v-1) : ℚ))).atoms.get e |>.accepted) =
      trialAllowed D b := by
    funext e
    simp [trialRun,trialAllowed,atomRun_accepted_code]
  have hlab : (fun e => ((trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v-1) : ℚ))).labels.get e).value) =
      rationalUpperLabels (η / (b.card*max 1 (v-1) : ℚ))
        (fun e => trialAtom D b (some e)) := by
    rw [trialRun_labels]
    rfl
  simp only [trialBitRun,basisRun_columns,basisRun_weights,basisRun_required,meshRun_value,hs]
  simp only [trialRun] at hatom
  simp only [trialRun] at hlab
  simp only [trialRun,atomRun_accepted_code]
  split_ifs with h
  · simp only [ExplicitDAG.outputCachedBitCounted_paths]
    change _ = trialPathSet G s t D η b
    rw [trialPathSet,if_pos (of_decide_eq_true h)]
    congr 1
    rw [← hatom,← hlab]
  · simp only [List.toFinset_nil]
    rw [trialPathSet,if_neg (by simpa using h)]

end CoverBitCost
end DAGSpectral
