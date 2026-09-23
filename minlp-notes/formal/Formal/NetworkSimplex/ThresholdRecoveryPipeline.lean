import Formal.NetworkSimplex.ThresholdRationalRows
import Formal.NetworkSimplex.ThresholdDecomposition
import Formal.NetworkSimplex.ThresholdRecoverySize
import Formal.NetworkSimplex.ProfileHull

/-! Cached rational state and graph recovery from a reduced profile. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {m L : ℕ}

/-- The eliminated base-state coordinate is formed once and stored with the profile. -/
def rationalRestore (D : RationalData m L) (x : Fin m → ℚ) : Vector ℚ (m + 1) :=
  let base := D.total - (List.ofFn x).sum
  Vector.ofFn (Fin.cons base x)

theorem rationalRestore_cast (D : RationalData m L) (x : Fin m → ℚ) :
    (fun j => ((rationalRestore D x).get j : ℝ)) =
      restoreProfile D.toReal.total (fun j => (x j : ℝ)) := by
  funext j
  refine Fin.cases ?_ (fun k => ?_) j
  · simp [rationalRestore, restoreProfile, List.sum_ofFn]
  · simp [rationalRestore, restoreProfile]

/-- The stored atoms include the feasible all-bypass atom for zero weights. -/
structure ProfileRecovery (m L : ℕ) where
  profile : Vector ℚ (m + 1)
  flows : RationalStateFlows L (m + 1)
  atoms : Vector (NormalizedState L) (m + 1)
  work : ℕ

/-- All arrays are actual outputs of interval filling and normalization. -/
def recoverProfile (D : RationalData m L) (x : Fin m → ℚ) : ProfileRecovery m L :=
  let profile := rationalRestore D x
  let flows := recoverStateFlows D.c D.u D.v D.weights D.xa profile.get
  let atoms := normalizeStates flows D.weights
  ⟨profile, flows, atoms, m + 3 + flows.work + ∑ j, (atoms.get j).work⟩

theorem recoverProfile_work (D : RationalData m L) (x : Fin m → ℚ) :
    (recoverProfile D x).work ≤ m + 3 + L * (9 * (m + 1) + 1) +
      (m + 1) + (m + 1) * (2 * L + 2) := by
  have hn := normalizationWork_bound
    (recoverStateFlows D.c D.u D.v D.weights D.xa (rationalRestore D x).get) D.weights
  simp only [recoverProfile, recoverStateFlows_charge]
  change m + 3 + (L * (9 * (m + 1) + 1) + (m + 1)) + normalizationWork _ _ ≤ _
  omega

theorem recoverProfile_fullProfile (D : RationalData m L) (x : Fin m → ℚ)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hx : D.toReal.ReducedProfile (fun j => (x j : ℝ))) :
    D.toReal.FullProfile (fun j => ((recoverProfile D x).profile.get j : ℝ)) := by
  change D.toReal.FullProfile (fun j => ((rationalRestore D x).get j : ℝ))
  rw [rationalRestore_cast]
  exact (D.toReal.fullProfile_restore_iff _ hc hh).mpr hx

theorem recoverProfile_valid (D : RationalData m L) (x : Fin m → ℚ)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hd : D.toReal.OriginalDomain)
    (hx : D.toReal.ReducedProfile (fun j => (x j : ℝ))) :
    ValidStateFlows D.toReal.c D.toReal.u D.toReal.v D.toReal.weights
      D.toReal.xa D.toReal.xb D.toReal.xh (fun j => D.observedH j = true)
      D.toReal.zh (recoverProfile D x).flows.toReal := by
  have hw : ∑ j, D.weights j = 1 := by
    have h : (∑ j, (D.weights j : ℝ)) = 1 := hd.1.2
    exact_mod_cast h
  have hf := recoverStateFlows_spec D.c D.u D.v D.weights D.xa
    (fun i => 1 - D.xh - D.xa i) D.xh (fun j => D.observedH j = true) D.zh
    (rationalRestore D x).get hw (by intro i; ring) hd.2.2.1
    (recoverProfile_fullProfile D x hc hh hx)
  convert hf using 1 <;> simp only [RationalData.toReal, recoverProfile,
    Rat.cast_sub, Rat.cast_one]
  rfl

noncomputable def ProfileRecovery.graphPoint (R : ProfileRecovery m L)
    (D : RationalData m L) (j : Fin (m + 1)) :
    Point (ChainArc L) (Fin (m + 1)) (Observation D.c (fun k => D.observedH k = true)) :=
  let flow := (R.atoms.get j).flow
  (flow, (fun k => if k = j then 1 else 0,
    fun o => flow o.val.1 * (if o.val.2 = j then 1 else 0)))

theorem recoverProfile_graphPoint (D : RationalData m L) (x : Fin m → ℚ)
    (j : Fin (m + 1)) :
    (recoverProfile D x).graphPoint D j =
      normalizedGraphPoint (recoverProfile D x).flows D.weights D.c
        (fun k => D.observedH k = true) j := rfl

/-- At most `m+1` actual cached graph atoms, exact moments, and the input weights. -/
theorem recoverProfile_decomposition (D : RationalData m L) (x : Fin m → ℚ)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hd : D.toReal.OriginalDomain)
    (hx : D.toReal.ReducedProfile (fun j => (x j : ℝ))) :
    (∀ j, (recoverProfile D x).graphPoint D j ∈ D.toReal.graph) ∧
    Simplex (fun j => (D.weights j : ℝ)) ∧
    (∑ j, (D.weights j : ℝ) • (recoverProfile D x).graphPoint D j = D.toReal.graphPoint) ∧
    Fintype.card (Fin (m + 1)) = m + 1 := by
  have hw : ∑ j, D.weights j = 1 := by
    have h : (∑ j, (D.weights j : ℝ)) = 1 := hd.1.2
    exact_mod_cast h
  convert (rational_chain_decomposition D.toReal.c D.toReal.u D.toReal.v D.weights
      D.toReal.xa D.toReal.xb D.toReal.xh (fun j => D.observedH j = true) D.toReal.zh
      (recoverProfile D x).flows (recoverProfile_valid D x hc hh hd hx) hw) using 1 <;> rfl

/-- Products are executable rational lookups in the stored atoms. -/
theorem recoverProfile_product_cast (D : RationalData m L) (x : Fin m → ℚ)
    (j : Fin (m + 1)) (o : Observation D.c (fun k => D.observedH k = true)) :
    (((recoverProfile D x).atoms.get j).rationalProduct j o.val : ℝ) =
      ((recoverProfile D x).graphPoint D j).2.2 o :=
  normalizedGraphPoint_product_cast _ _ _ _ _ _

end NetworkSimplex.Chain.Threshold
