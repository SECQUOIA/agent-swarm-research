import Formal.DAGSpectral.FactorInputExecution

namespace DAGSpectral
open Matrix NormalizationTrials FactorInputExecution

theorem FactorData.ext_fields {p m M : ℕ} {D E : FactorData p m M}
    (ha : D.atom = E.atom) (ho : D.owner = E.owner)
    (hw : D.weight = E.weight) (hv : D.vector = E.vector) : D = E := by
  cases D
  cases E
  simp_all

/-- Relabel only the dependent length of a factor cache. This transport is
proof-only and does not construct or read any factors. -/
def castFactorData {p m M N : ℕ} (h : M = N) (D : FactorData p m M) :
    FactorData p m N := h ▸ D

@[simp] theorem castFactorData_atom {p m M N : ℕ} (h : M = N) (D : FactorData p m M) :
    (castFactorData h D).atom = D.atom := by subst N; rfl

@[simp] theorem castFactorData_owner {p m M N : ℕ} (h : M = N) (D : FactorData p m M)
    (k : Fin N) : (castFactorData h D).owner k = D.owner (k.cast h.symm) := by
  subst N; rfl

@[simp] theorem castFactorData_weight {p m M N : ℕ} (h : M = N) (D : FactorData p m M)
    (k : Fin N) : (castFactorData h D).weight k = D.weight (k.cast h.symm) := by
  subst N; rfl

@[simp] theorem castFactorData_vector {p m M N : ℕ} (h : M = N) (D : FactorData p m M)
    (k : Fin N) : (castFactorData h D).vector k = D.vector (k.cast h.symm) := by
  subst N; rfl

namespace FactorInputExecution

/-- A factor read follows the stored list and records each visited cell. -/
def InputRun.factorAtRun {p m : ℕ} (cache : InputRun p m)
    (k : Fin cache.factors.length) : (Fin m × StoredFactor p) × ℕ :=
  let r := cachedLookup cache.factors k.val
  have hr : r.1.isSome := by
    simp only [r,cachedLookup_value,List.getElem?_eq_getElem k.isLt,Option.isSome_some]
  (r.1.get hr,r.2)

@[simp] theorem InputRun.factorAtRun_value {p m : ℕ} (cache : InputRun p m)
    (k : Fin cache.factors.length) : (cache.factorAtRun k).1 = cache.factorAt k := by
  simp [InputRun.factorAtRun,cachedLookup_value,InputRun.factorAt]

theorem InputRun.factorAtRun_steps {p m : ℕ} (cache : InputRun p m)
    (k : Fin cache.factors.length) : (cache.factorAtRun k).2 ≤ cache.factors.length+1 :=
  cachedLookup_steps cache.factors k.val

theorem factorAt_inputRun {p m : ℕ} (A : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (k : Fin (inputRun A).factors.length) :
    let f := (inputRun A).factorAt k
    (f.1, factorView f.2) =
      (indexedFactorOwner A (k.cast (inputRun_count A)),
        (indexedFactorWeight A (k.cast (inputRun_count A)),
          indexedFactorVector A (k.cast (inputRun_count A)))) := by
  exact inputRunAt_value A (k.cast (inputRun_count A))

/-- A runtime view of the stored labels. Its length is read from the cache;
the semantic LDL label count is used only in the proof fields. -/
def cachedFactorData {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (cache : InputRun p (m + 1)) (hc : cache = inputRun (priorAtomMatrices Q0 Q)) :
    FactorData p m cache.factors.length := by
  let A := priorAtomMatrices Q0 Q
  have hn : cache.factors.length = indexedFactorCount A := by rw [hc, inputRun_count]
  let D := castFactorData hn.symm (producedData Q0 Q hQ0 hQ)
  let owner : Fin cache.factors.length → Option (Fin m) :=
    fun k => Fin.cases none some (cache.factorAtRun k).1.1
  let weight := fun k : Fin cache.factors.length => (cache.factorAtRun k).1.2.1
  let vector := fun k : Fin cache.factors.length => (cache.factorAtRun k).1.2.2.get
  have hf (k : Fin cache.factors.length) :
      ((cache.factorAt k).1, factorView (cache.factorAt k).2) =
        (indexedFactorOwner A (k.cast hn),
          (indexedFactorWeight A (k.cast hn), indexedFactorVector A (k.cast hn))) := by
    subst cache
    exact factorAt_inputRun A k
  have ho : owner = D.owner := by
    funext k
    have h := congrArg Prod.fst (hf k)
    simpa [owner,D,producedData,indexedPriorAtomOwner] using congrArg (Fin.cases none some) h
  have hw : weight = D.weight := by
    funext k
    simpa [weight,D,producedData,factorView] using congrArg (fun f => f.2.1) (hf k)
  have hv : vector = D.vector := by
    funext k
    simpa [vector,D,producedData,factorView] using congrArg (fun f => f.2.2) (hf k)
  exact {
    atom := fun o => o.elim Q0 Q
    owner := owner
    weight := weight
    vector := vector
    weight_pos := by rw [hw]; exact D.weight_pos
    atom_eq := by
      rw [ho,hw,hv]
      simpa only [D,castFactorData_atom,producedData] using D.atom_eq
    owner_card := by rw [ho]; exact D.owner_card }

theorem cachedFactorData_eq {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (cache : InputRun p (m + 1)) (hc : cache = inputRun (priorAtomMatrices Q0 Q)) :
    cachedFactorData Q0 Q hQ0 hQ cache hc =
      castFactorData (by rw [hc,inputRun_count]) (producedData Q0 Q hQ0 hQ) := by
  apply FactorData.ext_fields
  · simp [cachedFactorData,producedData]
  · funext k
    subst cache
    have h := congrArg Prod.fst (factorAt_inputRun (priorAtomMatrices Q0 Q) k)
    simpa [cachedFactorData,producedData,indexedPriorAtomOwner] using
      congrArg (Fin.cases none some) h
  · funext k
    subst cache
    simpa [cachedFactorData,producedData,factorView] using
      congrArg (fun f => f.2.1) (factorAt_inputRun (priorAtomMatrices Q0 Q) k)
  · funext k
    subst cache
    simpa [cachedFactorData,producedData,factorView] using
      congrArg (fun f => f.2.2) (factorAt_inputRun (priorAtomMatrices Q0 Q) k)

theorem cachedFactorData_bits {p m B : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (cache : InputRun p (m + 1)) (hc : cache = inputRun (priorAtomMatrices Q0 Q))
    (h0 : MatrixBits Q0 B) (he : ∀ e, MatrixBits (Q e) B)
    (k : Fin cache.factors.length) :
    ReciprocalAnchor.RationalBits ((cachedFactorData Q0 Q hQ0 hQ cache hc).weight k)
      (factorBits p B) ∧ ∀ i,
    ReciprocalAnchor.RationalBits ((cachedFactorData Q0 Q hQ0 hQ cache hc).vector k i)
      (factorBits p B) := by
  change StoredFactorBits (cache.factorAtRun k).1.2 (factorBits p B)
  rw [InputRun.factorAtRun_value]
  subst cache
  apply inputRun_factorBits (priorAtomMatrices Q0 Q)
    (Fin.cases h0 he) _
  exact List.get_mem _ _

end FactorInputExecution
end DAGSpectral
