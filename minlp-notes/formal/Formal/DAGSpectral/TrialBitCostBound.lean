import Formal.DAGSpectral.CoverBitCost
import Formal.DAGSpectral.CoverCardinality

namespace DAGSpectral
open Matrix ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
namespace CoverBitCost
open NormalizationTrials CoverNormalizationExecution NormalizationBits BasisInputExecution

theorem meshRun_work {η : ℚ} {B r N : ℕ} (hη : RationalBits η B)
    (hsize : r + N + 2 ≤ B) :
    traceBitWork (3*B+1) (meshRun η r N).2 ≤ 2*(256*(3*B+2)^3) := by
  have hr := rationalBits_nat r
  have hn := rationalBits_nat N
  have hm := rationalBits_mul hr hn
  apply (traceBitWork_le (by
    intro e he
    have he : e = (.mul,(r:ℚ),(N:ℚ)) ∨ e = (.div,η,(r:ℚ)*N) := by
      simpa [meshRun,ArithmeticExpr.run,primitiveResult] using he
    rcases he with rfl | rfl
    · exact ⟨rationalBits_mono hr (by omega),rationalBits_mono hn (by omega)⟩
    · exact ⟨rationalBits_mono hη (by omega),rationalBits_mono hm (by omega)⟩)).trans
  simp [meshRun,ArithmeticExpr.run]

theorem selectedScales_eq {p m M} (D : FactorData p m M) (b : Finset (Fin M)) :
    actualScales (fun i => D.weight (label b i)) = scales D.weight b := by
  rfl

theorem trialAtom_bits {p m M B} (D : FactorData p m M) (b : Finset (Fin M))
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (o : Option (Fin m)) :
    MatrixBits (trialAtom D b o) (transformBudget p b.card B (6*B+1) B) := by
  exact transform_bits (fun i j => hV _ _) (actualScales_bits (fun i => hw _)) (hA o)

/-- The uniform cached-read charge covers actual signed label digits and all
three cache indices, using the proved widths of the computed entries and mesh. -/
theorem trialLabel_readWork {v m p M B : ℕ} (D : FactorData p m M)
    (b : Finset (Fin M)) {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hηB : RationalBits η B)
    (e : Fin m) (z : UpperCoord b.card) :
    (m+1)*(b.card*b.card+1)*
      ((rationalUpperLabels (η/(b.card*max 1 (v - 1):ℚ))
        (fun e => trialAtom D b (some e)) e z).natAbs.size+1) ≤
      trialLabelReadCost m b.card (transformBudget p b.card B (6*B+1) B)
        (B+b.card+max 1 (v - 1)+2) := by
  have hbits := integerBits_floor (rationalBits_div
    (trialAtom_bits D b hV hw hA (some e)
      (upperCoordEquiv b.card z).val.1 (upperCoordEquiv b.card z).val.2)
    (rationalMesh_bits hηB b.card (max 1 (v - 1))))
  have hs := Nat.size_le.mpr hbits
  change (rationalUpperLabels (η/(b.card*max 1 (v - 1):ℚ))
    (fun e => trialAtom D b (some e)) e z).natAbs.size ≤
    transformBudget p b.card B (6*B+1) B+(B+b.card+max 1 (v - 1)+2)+1 at hs
  unfold trialLabelReadCost
  apply Nat.mul_le_mul
  · exact Nat.mul_le_mul_left (m+1) (by nlinarith)
  · omega

noncomputable def trialCapacity (p r N : ℕ) (η : ℚ) : ℕ :=
  2^r*(8*p*r*N^2*⌈1/(η:ℝ)⌉₊+N+2)^(r*(r+1)/2)

noncomputable def trialWorkBound (v m p M r B : ℕ) (η : ℚ) : ℕ :=
  let N := max 1 (v - 1)
  let F := transformBudget p r B (6*B+1) B
  r*(9*B+1)*(256*(13*B+5)^3) + 2*(256*(3*B+2)^3) +
    ((m+1)*atomCostCoefficient p r*(B+1)^3 +
      m*r*r*(268*(F+(B+r+N+2)+1)^3)) +
    basisWorkBound p m M r B + trialStorageBudget p r m B (6*B+1) B (B+r+N+2) +
    r*(2*(6*B+1)+1)+r+1+(2*(B+r+N+2)+1) +
    ExplicitDAG.dpWorkPolynomial v m (r*(r+1)/2) r (F+(B+r+N+2)+1)
      (trialCapacity p r N η) +
    (v*(1+m*trialCapacity p r N η)^2)*(2*v*(r*(r+1)/2))*
      trialLabelReadCost m r F (B+r+N+2) + 1

theorem trialDP_work {v m p M B} (G : ExplicitDAG v m) (s : Fin v)
    (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hηB : RationalBits η B)
    (hb : 0 < b.card) (hη : 0 < η) :
    ExplicitDAG.dpBitWork G (trialAllowed D b) s (forcedOwners D.owner b)
      (rationalUpperLabels (η/(b.card*max 1 (v - 1):ℚ))
        (fun e => trialAtom D b (some e))) ≤
    ExplicitDAG.dpWorkPolynomial v m (b.card*(b.card+1)/2) b.card
      (transformBudget p b.card B (6*B+1) B+(B+b.card+max 1 (v - 1)+2)+1)
      (trialCapacity p b.card (max 1 (v - 1)) η) := by
  have h := G.spectral_rational_dpBitWork (trialAllowed D b) s (forcedOwners D.owner b)
    (fun e (z : UpperCoord b.card) => trialAtom D b (some e)
      (upperCoordEquiv b.card z).val.1 (upperCoordEquiv b.card z).val.2)
    p b.card (max 1 (v - 1)) (transformBudget p b.card B (6*B+1) B) B η
    (fun e z => trialAtom_bits D b hV hw hA (some e) _ _) hηB hb (by omega) hη
    (by omega) (forcedOwners_card D.owner b)
    (fun e he z => trialAtom_entry_bound D b e he _ _)
  unfold DAGSpectral.rationalUpperLabels
  simpa only [rationalMesh,card_upperCoord,trialCapacity] using h

theorem trialDP_labelAccessCount {v m p M} (G : ExplicitDAG v m) (s : Fin v)
    (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ}
    (hb : 0 < b.card) (hη : 0 < η) :
    ExplicitDAG.labelAccessCount G (trialAllowed D b) s (forcedOwners D.owner b)
      (rationalUpperLabels (η/(b.card*max 1 (v - 1):ℚ))
        (fun e => trialAtom D b (some e))) ≤
      (v*(1+m*trialCapacity p b.card (max 1 (v - 1)) η)^2)*
        (2*v*(b.card*(b.card+1)/2)) := by
  rw [rationalUpperLabels_eq_spectral]
  let a := fun e (z : UpperCoord b.card) => ratMatrixReal (trialAtom D b (some e))
    (upperCoordEquiv b.card z).val.1 (upperCoordEquiv b.card z).val.2
  let window := coordinateRange p (max 1 (v - 1))
    (spectralMesh (η:ℝ) b.card (max 1 (v - 1)))
  have hηR : (0:ℝ) < η := by exact_mod_cast hη
  have hw : ∀ t es, G.AllowedPath (trialAllowed D b) s t es → ∀ i,
      ExplicitDAG.profile (ExplicitDAG.spectralLabels a (η:ℝ) b.card (max 1 (v - 1)))
        es i ∈ window := by
    intro t es he i
    exact G.allowed_profile_window (trialAllowed D b) s t a p b.card (max 1 (v - 1))
      (η:ℝ) hb (by omega) hηR (by omega)
      (fun e he z => trialAtom_entry_bound D b e he _ _) he i
  have hcap := ExplicitDAG.spectral_state_capacity (κ := UpperCoord b.card)
    (forcedOwners D.owner b) p b.card (max 1 (v - 1)) (η:ℝ) hb (by omega) hηR
    (forcedOwners_card D.owner b)
  have hpoly := coordinateCount_le_polynomial p b.card (max 1 (v - 1)) (η:ℝ)
  have hsize : 2^(forcedOwners D.owner b).card * window.card^Fintype.card (UpperCoord b.card) ≤
      trialCapacity p b.card (max 1 (v - 1)) η := by
    apply hcap.trans
    simpa only [trialCapacity,card_upperCoord] using
      Nat.mul_le_mul_left (2^b.card) (Nat.pow_le_pow_left hpoly (Fintype.card (UpperCoord b.card)))
  have hc := G.comparisonBudget_bound (trialAllowed D b) s (forcedOwners D.owner b)
    (ExplicitDAG.spectralLabels a (η:ℝ) b.card (max 1 (v - 1))) window hw
  have hh := G.labelAccessCount_le (trialAllowed D b) s (forcedOwners D.owner b)
    (ExplicitDAG.spectralLabels a (η:ℝ) b.card (max 1 (v - 1)))
  apply hh.trans
  simp only [card_upperCoord]
  gcongr
  exact hc.trans (by gcongr)

theorem trialBitRun_length {v m p M} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ} (B K F C : ℕ)
    (hb : 0 < b.card) (hη : 0 < η) :
    (trialBitRun G s t D η b B K F C).1.length ≤
      trialCapacity p b.card (max 1 (v - 1)) η := by
  have hs : (fun i => ((scalesRun (fun j => D.weight (label b j))).get i).1) =
      scales D.weight b := by funext i; simp only [scalesRun_value]; rfl
  have hatom : (fun e => (trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v - 1) : ℚ))).atoms.get e |>.accepted) =
      trialAllowed D b := by
    funext e
    simp [trialRun,trialAllowed,atomRun_accepted_code]
  have hlab : (fun e => ((trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v - 1) : ℚ))).labels.get e).value) =
      rationalUpperLabels (η / (b.card*max 1 (v - 1) : ℚ))
        (fun e => trialAtom D b (some e)) := by
    rw [trialRun_labels]; rfl
  simp only [trialBitRun,basisRun_columns,basisRun_weights,basisRun_required,meshRun_value,hs]
  split_ifs
  · simp only [hatom,hlab,ExplicitDAG.outputCachedBitCounted_paths]
    rw [rationalUpperLabels_eq_spectral]
    have hh := G.spectral_dp_bounds (trialAllowed D b) s t (forcedOwners D.owner b)
      (fun e z => ratMatrixReal (trialAtom D b (some e))
        (upperCoordEquiv b.card z).val.1 (upperCoordEquiv b.card z).val.2)
      p b.card (max 1 (v - 1)) (η : ℝ) hb (by omega) (by exact_mod_cast hη)
      (by omega) (forcedOwners_card D.owner b)
      (fun e he z => trialAtom_entry_bound D b e he _ _)
    have hc := coordinateCount_le_polynomial p b.card (max 1 (v - 1)) (η:ℝ)
    apply (hh.2.2).trans
    simpa only [card_upperCoord,trialCapacity] using
      (Nat.mul_le_mul_left (2^b.card) (Nat.pow_le_pow_left hc (Fintype.card (UpperCoord b.card))))
  · exact Nat.zero_le _

theorem trialBitRun_work {v m p M B} (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (b : Finset (Fin M)) {η : ℚ}
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B)
    (hA : ∀ o, MatrixBits (D.atom o) B) (hηB : RationalBits η B)
    (hb : 0 < b.card) (hη : 0 < η) (hsize : b.card + max 1 (v - 1) + 2 ≤ B) :
    (trialBitRun G s t D η b B (atomBudget p b.card B (6*B+1) B)
      (transformBudget p b.card B (6*B+1) B) (B+b.card+max 1 (v - 1)+2)).2 ≤
      trialWorkBound v m p M b.card B η := by
  have hs : (fun i => ((scalesRun (fun j => D.weight (label b j))).get i).1) =
      scales D.weight b := by funext i; simp only [scalesRun_value]; rfl
  have hscale := (traceBitWork_le (scalesTrace_bits (fun i => hw (label b i)))).trans
    (Nat.mul_le_mul_right _ (scalesTrace_length (fun i => hw (label b i))))
  simp only [Nat.add_assoc, Nat.reduceAdd] at hscale
  have hmesh := meshRun_work hηB hsize
  have hc := cacheWork_bound (m := m) (fun i j => hV (label b j) i)
    (fun i => hw (label b i)) hA (rationalMesh_bits hηB b.card (max 1 (v - 1)))
  have hbas := basisRun_work D b hV hw
  have hcop := trialRun_copies_le (m := m) (fun i j => hV (label b j) i)
    (actualScales_bits (fun i => hw (label b i))) hA
    (rationalMesh_bits hηB b.card (max 1 (v - 1)))
  have hscop := RationalStorage.vectorCopy_le (actualScales_bits (fun i => hw (label b i)))
  have hmcop := RationalStorage.scalarCopy_le (rationalMesh_bits hηB b.card (max 1 (v - 1)))
  have hd := trialDP_work G s D b hV hw hA hηB hb hη
  have hatom : (fun e => (trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v - 1) : ℚ))).atoms.get e |>.accepted) =
      trialAllowed D b := by
    funext e
    simp [trialRun,trialAllowed,atomRun_accepted_code]
  have hlab : (fun e => ((trialRun (columns D.vector b) (scales D.weight b)
      D.atom (η / (b.card*max 1 (v - 1) : ℚ))).labels.get e).value) =
      rationalUpperLabels (η / (b.card*max 1 (v - 1) : ℚ))
        (fun e => trialAtom D b (some e)) := by
    rw [trialRun_labels]; rfl
  have hread := Nat.mul_le_mul_right
    (trialLabelReadCost m b.card (transformBudget p b.card B (6*B+1) B)
      (B+b.card+max 1 (v - 1)+2)) (trialDP_labelAccessCount G s D b hb hη)
  have hout := G.outputCachedBitCounted_work (trialAllowed D b) s (forcedOwners D.owner b)
    (rationalUpperLabels (η / (b.card*max 1 (v - 1) : ℚ))
      (fun e => trialAtom D b (some e)))
    (trialLabelReadCost m b.card (transformBudget p b.card B (6*B+1) B)
      (B+b.card+max 1 (v - 1)+2)) t
  unfold ExplicitDAG.uncachedDPBitWork at hout
  simp only [trialBitRun,basisRun_columns,basisRun_weights,basisRun_required,
    meshRun_value,hs,scalesRun_events]
  change cacheWork (trialRun (columns D.vector b) (scales D.weight b) D.atom
    (η/(b.card*max 1 (v - 1):ℚ))) _ _ _ ≤ _ at hc
  change (trialRun (columns D.vector b) (scales D.weight b) D.atom
    (η/(b.card*max 1 (v - 1):ℚ))).copies ≤ _ at hcop
  change RationalStorage.vectorCopy (scales D.weight b) ≤ _ at hscop
  change RationalStorage.scalarCopy (η/(b.card*max 1 (v - 1):ℚ)) ≤ _ at hmcop
  dsimp only [trialWorkBound]
  split_ifs
  · simp only [hatom,hlab]
    omega
  · omega

end CoverBitCost
end DAGSpectral
