import Formal.NetworkSimplex.ThresholdRecoveryPipeline
import Formal.NetworkSimplex.ThresholdOracleSize
import Formal.NetworkSimplex.ThresholdBasisOracleSize
import Formal.NetworkSimplex.ThresholdWitness

/-! Polynomial sizes for the actual restored profiles, cached flows, and graph atoms. -/

namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open ReciprocalAnchor

variable {m L B : ℕ}

def restoreBits (m B : ℕ) : ℕ := B + m * (B + 1) + 4

def pipelineFlowBits (m B : ℕ) : ℕ := recoveryBits (m + 1) (restoreBits m B)

def pipelineAtomBits (m B : ℕ) : ℕ := 2 * pipelineFlowBits m B + 1

theorem restoreBits_ge_input (m B : ℕ) : B ≤ restoreBits m B := by
  unfold restoreBits
  omega

/-- Every partial sum of the supplied reduced profile has polynomial size. -/
theorem restorePartialSum_bits (x : Fin m → ℚ) (hx : ∀ j, RationalBits (x j) B)
    (xs : List ℚ) (hxs : xs.Sublist (List.ofFn x)) :
    RationalBits xs.sum (1 + m * (B + 1)) := by
  have he : ∀ r ∈ xs, RationalBits r B := by
    intro r hr
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp (hxs.subset hr)
    exact hx j
  apply rationalBits_mono (rationalBits_list_sum he)
  have hn : xs.length ≤ m := by simpa using hxs.length_le
  exact Nat.add_le_add_left (Nat.mul_le_mul_right (B + 1) hn) 1

theorem rationalRestore_base_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) :
    RationalBits (D.total - (List.ofFn x).sum) (restoreBits m B) := by
  have hs := restorePartialSum_bits x hx (List.ofFn x) (List.Sublist.refl _)
  convert rationalBits_sub (RationalData.total_bits hd) hs using 1
  unfold restoreBits
  omega

theorem rationalRestore_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) :
    ∀ j, RationalBits ((rationalRestore D x).get j) (restoreBits m B) := by
  intro j
  refine Fin.cases ?_ (fun k => ?_) j
  · simpa [rationalRestore] using rationalRestore_base_bits D x hd hx
  · simpa [rationalRestore] using rationalBits_mono (hx k) (restoreBits_ge_input m B)

theorem recoverProfile_profile_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) :
    ∀ j, RationalBits ((recoverProfile D x).profile.get j) (restoreBits m B) :=
  rationalRestore_bits D x hd hx

/-- All three stored, unnormalized state-flow arrays have polynomial size. -/
theorem recoverProfile_flows_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) :
    (∀ i j, RationalBits ((((recoverProfile D x).flows.a).get i).get j)
      (pipelineFlowBits m B)) ∧
    (∀ i j, RationalBits ((((recoverProfile D x).flows.b).get i).get j)
      (pipelineFlowBits m B)) ∧
    (∀ j, RationalBits ((recoverProfile D x).flows.h.get j) (pipelineFlowBits m B)) := by
  exact recoverStateFlows_bits D.c D.u D.v D.weights D.xa (rationalRestore D x).get
    (fun i j => rationalBits_mono (hd.u i j) (restoreBits_ge_input m B))
    (fun i j => rationalBits_mono (hd.v i j) (restoreBits_ge_input m B))
    (fun j => rationalBits_mono (hd.weights j) (restoreBits_ge_input m B))
    (fun i => rationalBits_mono (hd.xa i) (restoreBits_ge_input m B))
    (rationalRestore_bits D x hd hx)

private theorem input_le_pipelineFlowBits (m B : ℕ) : B ≤ pipelineFlowBits m B := by
  have h := restoreBits_ge_input m B
  unfold pipelineFlowBits recoveryBits
  omega

/-- Normalizing the cached flows keeps every actual stored atom polynomial in size,
including the all-bypass atom selected when a state has zero weight. -/
theorem recoverProfile_atoms_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) (j : Fin (m + 1)) :
    (∀ i, RationalBits (((recoverProfile D x).atoms.get j).a.get i) (pipelineAtomBits m B)) ∧
    (∀ i, RationalBits (((recoverProfile D x).atoms.get j).b.get i) (pipelineAtomBits m B)) ∧
    RationalBits ((recoverProfile D x).atoms.get j).h (pipelineAtomBits m B) := by
  obtain ⟨ha, hb, hh⟩ := recoverProfile_flows_bits D x hd hx
  simpa only [recoverProfile, normalizeStates, Vector.get_ofFn, pipelineAtomBits] using
    normalizeState_bits ha hb hh
      (fun k => rationalBits_mono (hd.weights k) (input_le_pipelineFlowBits m B)) j

/-- Product coordinates are rational lookups in the stored atoms, with the same size bound. -/
theorem recoverProfile_products_bits (D : RationalData m L) (x : Fin m → ℚ)
    (hd : D.InputBits B) (hx : ∀ j, RationalBits (x j) B) (j : Fin (m + 1))
    (o : ChainArc L × Fin (m + 1)) :
    RationalBits (((recoverProfile D x).atoms.get j).rationalProduct j o)
      (pipelineAtomBits m B) := by
  obtain ⟨ha, hb, hh⟩ := recoverProfile_flows_bits D x hd hx
  exact normalized_products_bits ha hb hh
    (fun k => rationalBits_mono (hd.weights k) (input_le_pipelineFlowBits m B)) j o

/-- The atom bound is an explicit polynomial in the reduced dimension and input bit size. -/
theorem pipelineAtomBits_formula (m B : ℕ) :
    pipelineAtomBits m B =
      2 * (4 * (B + m * (B + 1) + 4) +
        (m + 1) * (3 * (B + m * (B + 1) + 4) + 4) + 5) + 1 := rfl

/-- Grouping selects an actual original row and therefore preserves its bit bound. -/
theorem packedRationalTable_bits (D : RationalData m L) (hd : D.InputBits B)
    (k : Fin (normalKeyCount m)) (q : ℚ)
    (hq : (packedRationalTable D).get k = some q) :
    RationalBits q (RationalData.rowBits m B) := by
  rw [packedRationalTable_get] at hq
  obtain ⟨r, hr, rfl⟩ := Option.map_eq_some_iff.mp hq
  exact RationalData.indexedRows_bits hd packNormal
    (NetworkSimplex.ThresholdGrouping.group_minimum (D.indexedRows packNormal) k hr).1

theorem keyNormal_natAbs (k : Fin (normalKeyCount m)) (j : Fin m) :
    (keyNormal k j).natAbs ≤ 1 := by
  unfold keyNormal
  split_ifs <;> norm_num

/-- A successful basis scan has bounded output directly from original input widths. -/
theorem recoverPackedProfile_bits (D : RationalData m L) (hd : D.InputBits B)
    {x : Fin m → ℚ} (hx : (recoverPackedProfile D (packedBasisLibrary m)).1 = some x)
    (j : Fin m) :
    RationalBits (x j) (basisCandidateBits m (RationalData.rowBits m B)) := by
  apply recoverFromCache_bits (fun k j => keyNormal k j) keyNormal_natAbs
    (packedRationalTable D).get (by unfold RationalData.rowBits; positivity)
    (packedRationalTable_bits D hd) hx j

/-- One width covers both original inputs and the computed reduced profile. -/
def recoveredInputBits (m B : ℕ) : ℕ :=
  B + basisCandidateBits m (RationalData.rowBits m B)

theorem RationalData.InputBits.mono {D : RationalData m L} {C : ℕ}
    (h : D.InputBits B) (hBC : B ≤ C) : D.InputBits C :=
  ⟨fun i j => rationalBits_mono (h.u i j) hBC,
   fun i j => rationalBits_mono (h.v i j) hBC,
   fun j => rationalBits_mono (h.weights j) hBC,
   fun i => rationalBits_mono (h.xa i) hBC,
   rationalBits_mono h.xh hBC, fun j => rationalBits_mono (h.zh j) hBC⟩

/-- The actual end-to-end witness has polynomial-size graph atoms. No externally
supplied profile-width premise remains. -/
theorem recoverWitness_atoms_bits (D : RationalData m L) (hd : D.InputBits B)
    {out : ProfileRecovery m L}
    (ho : (recoverWitness D (packedBasisLibrary m)).1 = some out) (j : Fin (m + 1)) :
    (∀ i, RationalBits ((out.atoms.get j).a.get i)
      (pipelineAtomBits m (recoveredInputBits m B))) ∧
    (∀ i, RationalBits ((out.atoms.get j).b.get i)
      (pipelineAtomBits m (recoveredInputBits m B))) ∧
    RationalBits (out.atoms.get j).h (pipelineAtomBits m (recoveredInputBits m B)) := by
  obtain ⟨x, hx, rfl⟩ := recoverWitness_source D _ ho
  apply recoverProfile_atoms_bits D x
    (hd.mono (by unfold recoveredInputBits; omega))
  intro k
  exact rationalBits_mono (recoverPackedProfile_bits D hd hx k)
    (by unfold recoveredInputBits; omega)

/-- The same direct input bound covers all stored flows before normalization. -/
theorem recoverWitness_flows_bits (D : RationalData m L) (hd : D.InputBits B)
    {out : ProfileRecovery m L}
    (ho : (recoverWitness D (packedBasisLibrary m)).1 = some out) :
    (∀ i j, RationalBits ((out.flows.a.get i).get j)
      (pipelineFlowBits m (recoveredInputBits m B))) ∧
    (∀ i j, RationalBits ((out.flows.b.get i).get j)
      (pipelineFlowBits m (recoveredInputBits m B))) ∧
    (∀ j, RationalBits (out.flows.h.get j) (pipelineFlowBits m (recoveredInputBits m B))) := by
  obtain ⟨x, hx, rfl⟩ := recoverWitness_source D _ ho
  apply recoverProfile_flows_bits D x
    (hd.mono (by unfold recoveredInputBits; omega))
  intro k
  exact rationalBits_mono (recoverPackedProfile_bits D hd hx k)
    (by unfold recoveredInputBits; omega)

/-- The combined input/profile budget is bounded by an explicit polynomial. -/
theorem recoveredInputBits_polynomial (m B : ℕ) :
    recoveredInputBits m B ≤ B + 1 + m *
      (m ^ 2 + 1 + (2 * m + 6) * (B + 2) + 1) := by
  have hb := basisEntryBits_polynomial m
  unfold recoveredInputBits basisCandidateBits RationalData.rowBits
  nlinarith [Nat.mul_le_mul_left m hb]

/-- Product coordinates are actual rational atom lookups and satisfy the same
original-input bound, including zero-weight fallback atoms. -/
theorem recoverWitness_products_bits (D : RationalData m L) (hd : D.InputBits B)
    {out : ProfileRecovery m L}
    (ho : (recoverWitness D (packedBasisLibrary m)).1 = some out)
    (j : Fin (m + 1)) (o : ChainArc L × Fin (m + 1)) :
    RationalBits ((out.atoms.get j).rationalProduct j o)
      (pipelineAtomBits m (recoveredInputBits m B)) := by
  obtain ⟨x, hx, rfl⟩ := recoverWitness_source D _ ho
  apply recoverProfile_products_bits D x
    (hd.mono (by unfold recoveredInputBits; omega))
  intro k
  exact rationalBits_mono (recoverPackedProfile_bits D hd hx k)
    (by unfold recoveredInputBits; omega)

/-- Converting each ledger unit to at most two primitive operations also covers
the basis scanner's fused multiply-accumulates. This uniform conservative bound
includes row generation, grouping, basis trials, greedy filling, and atom output. -/
theorem recoverWitness_primitive_work (D : RationalData m L) (hm : 1 ≤ m) :
    2 * (recoverWitness D (packedBasisLibrary m)).2 ≤
      2 * (26 * m * (L + 1) + normalKeyCount m +
      (normalKeyCount m) ^ m * basisTrialCharge (normalKeyCount m) m +
      (m + 3 + L * (9 * (m + 1) + 1) + (m + 1) + (m + 1) * (2 * L + 2))) :=
  Nat.mul_le_mul_left 2 (recoverWitness_work D hm)

end NetworkSimplex.Chain.Threshold
