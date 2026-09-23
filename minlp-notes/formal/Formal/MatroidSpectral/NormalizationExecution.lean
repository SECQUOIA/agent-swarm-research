import Formal.MatroidSpectral.TrialLabels
import Formal.DAGSpectral.TrialBitCostBound
import Formal.DAGSpectral.CoverIndependenceExecution

/-! Coupled preparation of a represented-matroid normalization trial. Stored
factor columns are read once. The independence test and every atom filter are
executed and charged, including rejected candidates. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open DAGSpectral.CoverNormalizationExecution DAGSpectral.NormalizationBits
open DAGSpectral.CoverBitCost DAGSpectral.BasisInputExecution
open ReciprocalAnchor

structure PreparedTrial (p m r : ℕ) where
  independent : Bool
  required : Finset (Fin m)
  cache : TrialRun p r m

def prepareTrialRun {p m M : ℕ} (D : FactorData p m M) (η : ℚ) (q : ℕ)
    (b : Finset (Fin M)) (B : ℕ) : PreparedTrial p m b.card × ℕ :=
  let basis := basisRun D b
  let gate := independenceRun basis.1.columns
  let scales := scalesRun basis.1.weights
  let mesh := meshRun η b.card q
  let cache := trialRun basis.1.columns (fun i => (scales.get i).1) D.atom mesh.1
  let K := atomBudget p b.card B (6*B+1) B
  let F := transformBudget p b.card B (6*B+1) B
  let C := B+b.card+q+2
  (⟨gate.independent,basis.1.required,cache⟩,
    basis.2 + traceBitWork (independenceBudget p b.card B) gate.events + gate.copies +
    traceBitWork (13*B+4) (List.ofFn fun i => (scales.get i).2).flatten +
    traceBitWork (3*B+1) mesh.2 + cacheWork cache K F C + cache.copies +
    RationalStorage.vectorCopy (fun i => (scales.get i).1) + b.card+1 +
    RationalStorage.scalarCopy mesh.1)

@[simp] theorem prepareTrialRun_independent {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    (prepareTrialRun D η q b B).1.independent = decide (independent D.vector b) := by
  simp only [prepareTrialRun,basisRun_columns,independenceRun_code]

@[simp] theorem prepareTrialRun_required {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    (prepareTrialRun D η q b B).1.required = forcedOwners D.owner b := by
  simp only [prepareTrialRun,basisRun_required]

theorem prepareTrialRun_cache {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    (prepareTrialRun D η q b B).1.cache =
      trialRun (columns D.vector b) (scales D.weight b) D.atom
        (η / (b.card*q : ℚ)) := by
  simp only [prepareTrialRun,basisRun_columns,basisRun_weights,scalesRun_value,
    meshRun_value,selectedScales_eq]

@[simp] theorem prepareTrialRun_prior {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    (prepareTrialRun D η q b B).1.cache.prior.accepted =
      decide (acceptsAtomCode D.vector D.weight b (D.atom none)) := by
  rw [prepareTrialRun_cache]
  exact atomRun_accepted_code _ _ _ _

@[simp] theorem prepareTrialRun_allowed {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) (e : Fin m) :
    ((prepareTrialRun D η q b B).1.cache.atoms.get e).accepted = trialAllowed D b e := by
  rw [prepareTrialRun_cache]
  simpa only [trialRun,Vector.get_ofFn,trialAllowed] using atomRun_accepted_code
    D.vector D.weight b (D.atom (some e))

theorem prepareTrialRun_signed {p m M : ℕ} (D : FactorData p m M)
    (η : ℚ) (q : ℕ) (b : Finset (Fin M)) (B : ℕ) :
    (fun e => ((prepareTrialRun D η q b B).1.cache.labels.get e).value) =
      trialSigned D q η b := by
  rw [prepareTrialRun_cache,trialRun_labels]
  rfl

def normalizationWorkBound (p m M r q B : ℕ) : ℕ :=
  let F := transformBudget p r B (6*B+1) B
  basisWorkBound p m M r B +
    independenceCostCoefficient p r*(B+1)^3 + independenceStorageBudget p r 1*(B+1) +
    r*(9*B+1)*(256*(13*B+5)^3) + 2*(256*(3*B+2)^3) +
    ((m+1)*atomCostCoefficient p r*(B+1)^3 +
      m*r*r*(268*(F+(B+r+q+2)+1)^3)) +
    trialStorageBudget p r m B (6*B+1) B (B+r+q+2) +
    r*(2*(6*B+1)+1)+r+1+(2*(B+r+q+2)+1)

/-- No positivity or independence hypothesis is required for this work bound:
it includes all rejected factor subsets. -/
theorem prepareTrialRun_work {p m M B : ℕ} (D : FactorData p m M)
    (b : Finset (Fin M)) {η : ℚ} {q : ℕ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hη : RationalBits η B)
    (hsize : b.card + q + 2 ≤ B) :
    (prepareTrialRun D η q b B).2 ≤ normalizationWorkBound p m M b.card q B := by
  have hi := independenceRun_bitWork (V := columns D.vector b) (fun i j => hV (label b j) i)
  have hic := independenceRun_copies_polynomial (V := columns D.vector b)
    (fun i j => hV (label b j) i)
  have hs := (traceBitWork_le (scalesTrace_bits (fun i => hw (label b i)))).trans
    (Nat.mul_le_mul_right _ (scalesTrace_length (fun i => hw (label b i))))
  simp only [Nat.add_assoc,Nat.reduceAdd] at hs
  have hm := meshRun_work hη hsize
  have hc := cacheWork_bound (m := m) (fun i j => hV (label b j) i)
    (fun i => hw (label b i)) hA (rationalMesh_bits hη b.card q)
  have hb := basisRun_work D b hV hw
  have hcopy := trialRun_copies_le (m := m) (fun i j => hV (label b j) i)
    (actualScales_bits (fun i => hw (label b i))) hA (rationalMesh_bits hη b.card q)
  have hsc := RationalStorage.vectorCopy_le (actualScales_bits (fun i => hw (label b i)))
  have hmc := RationalStorage.scalarCopy_le (rationalMesh_bits hη b.card q)
  simp only [prepareTrialRun,basisRun_columns,basisRun_weights,basisRun_required,
    meshRun_value,scalesRun_value,scalesRun_events,normalizationWorkBound]
  change cacheWork (trialRun (columns D.vector b)
    (fun i => actualScales (fun j => D.weight (label b j)) i) D.atom
    (η / (b.card*q : ℚ))) _ _ _ ≤ _ at hc
  change (trialRun (columns D.vector b)
    (fun i => actualScales (fun j => D.weight (label b j)) i) D.atom
    (η / (b.card*q : ℚ))).copies ≤ _ at hcopy
  change RationalStorage.vectorCopy (fun i => actualScales (fun j => D.weight (label b j)) i)
    ≤ _ at hsc
  change RationalStorage.scalarCopy (η / (b.card*q : ℚ)) ≤ _ at hmc
  omega

end MatroidSpectral
