import Formal.NetworkSimplex.ThresholdDomainOracleCost
import Formal.NetworkSimplex.ThresholdUnitOracle
import Formal.NetworkSimplex.ThresholdResults

/-! Full original-coordinate separation, including failed original-domain checks. -/
namespace NetworkSimplex.Chain.Threshold

/-- The domain scan precedes the sixteen profile tests and actual unit repair. -/
def separateThree {L : ℕ} (D : RationalData 3 L) :
    Option (AffineExpression (Coordinate 3 (Fin L))) × ℕ :=
  let domain := D.domainSeparator
  match domain.1 with
  | some e => (some e, domain.2)
  | none => let profile := threeUnitOracle D
      (profile.1, domain.2 + profile.2)

theorem separateThree_none_iff {L : ℕ} (D : RationalData 3 L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (separateThree D).1 = none ↔ D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  rw [D.toReal.mem_hull_iff, D.toReal.exists_fullProfile_iff_rows hc hh]
  have he : (∃ x, ∀ r, (D.toReal.rowNormal r).value x ≤ D.toReal.rowRhs r) ↔
      ∃ x, D.toReal.ReducedProfile x := exists_congr fun x => D.toReal.rows_iff_reducedProfile x
  rw [he, ← threeUnitOracle_none_iff, ← D.domainSeparator_none_iff hc hh]
  cases hd : D.domainSeparator.1 <;> simp [separateThree, hd]

theorem separateThree_sound {L : ℕ} (D : RationalData 3 L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    {e : AffineExpression (Coordinate 3 (Fin L))} (ho : (separateThree D).1 = some e) :
    UnitFlowProducts e ∧ e.eval (coordinates D.toReal D.toReal.xb) < 0 ∧
      ∀ E : ReductionData 3 (Fin L), D.c = E.c → D.observedH = E.observedH →
        E.graphPoint ∈ convexHull ℝ E.graph → 0 ≤ e.eval (coordinates E E.xb) := by
  cases hd : D.domainSeparator.1 with
  | none =>
    have hp : (threeUnitOracle D).1 = some e := by simpa [separateThree, hd] using ho
    exact threeUnitOracle_separates D hc hh hp
  | some out =>
    have he : out = e := by simpa [separateThree, hd] using ho
    subst out
    obtain ⟨hn, hv⟩ := D.domainSeparator_some hc hh hd
    have hn' : ((e.evalRat D.coordinatesRat : ℚ) : ℝ) < 0 := by exact_mod_cast hn
    rw [D.evalRat_coordinates_cast] at hn'
    exact ⟨fun z _ => D.domainSeparator_some_unit hd z, hn',
      fun E hp ho hm => hv E hp ho (E.mem_hull_iff.mp hm).1⟩

theorem separateThree_work {L : ℕ} (D : RationalData 3 L) :
    (separateThree D).2 ≤ D.domainSeparator.2 + 983 * L + 3170 := by
  have h := threeUnitOracle_cost D
  cases hd : D.domainSeparator.1 <;> simp only [separateThree, hd] <;> omega

/-- In arbitrary dimension, a domain cut is an affine expression and a profile
cut is the compact integer-weighted list of original source row identifiers. -/
abbrev FullCut (m L : ℕ) := AffineExpression (Coordinate m (Fin L)) ⊕ EncodedCut m L

def FullCut.valueAt {m L : ℕ} (cut : FullCut m L) (E : ReductionData m (Fin L)) : ℝ :=
  match cut with
  | .inl e => e.eval (coordinates E E.xb)
  | .inr rows => rows.eval E.rowRhs

def separateGeneral {m L : ℕ} (D : RationalData m L)
    (library : List (NetworkSimplex.ThresholdOracle.Circuit (normalKeyCount m))) :
    Option (FullCut m L) × ℕ :=
  let domain := D.domainSeparator
  match domain.1 with
  | some e => (some (.inl e), domain.2)
  | none => let profile := generalOracle D library
      (profile.1.map Sum.inr, domain.2 + profile.2)

theorem separateGeneral_none_iff {m L : ℕ} (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (separateGeneral D (generalLibrary m)).1 = none ↔
      D.toReal.graphPoint ∈ convexHull ℝ D.toReal.graph := by
  rw [D.toReal.mem_hull_iff, D.toReal.exists_fullProfile_iff_rows hc hh]
  have he : (∃ x, ∀ r, (D.toReal.rowNormal r).value x ≤ D.toReal.rowRhs r) ↔
      ∃ x, D.toReal.ReducedProfile x := exists_congr fun x => D.toReal.rows_iff_reducedProfile x
  rw [he, ← generalOracle_none_iff, ← D.domainSeparator_none_iff hc hh]
  cases hd : D.domainSeparator.1 <;> simp [separateGeneral, hd]

theorem separateGeneral_sound {m L : ℕ} (D : RationalData m L)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    {cut : FullCut m L} (ho : (separateGeneral D (generalLibrary m)).1 = some cut) :
    cut.valueAt D.toReal < 0 ∧
      ∀ E : ReductionData m (Fin L), D.c = E.c → D.observedH = E.observedH →
        E.graphPoint ∈ convexHull ℝ E.graph → 0 ≤ cut.valueAt E := by
  cases hd : D.domainSeparator.1 with
  | some e =>
    have he : Sum.inl e = cut := by simpa [separateGeneral, hd] using ho
    subst cut
    obtain ⟨hn, hv⟩ := D.domainSeparator_some hc hh hd
    have hn' : ((e.evalRat D.coordinatesRat : ℚ) : ℝ) < 0 := by exact_mod_cast hn
    rw [D.evalRat_coordinates_cast] at hn'
    exact ⟨hn', fun E hp ho hm => hv E hp ho (E.mem_hull_iff.mp hm).1⟩
  | none =>
    have hp : ((generalOracle D (generalLibrary m)).1.map Sum.inr) = some cut := by
      simpa [separateGeneral, hd] using ho
    obtain ⟨rows, hr, rfl⟩ := Option.map_eq_some_iff.mp hp
    have hnegative := NetworkSimplex.ThresholdOracle.circuitOracle_some
      (packedGroup D).table.get (fun r => r.value) (generalLibrary m) hr
    have hn : (NetworkSimplex.ThresholdOracle.weightedValue
        (fun r : PackedRow m L => r.value) rows : ℝ) < 0 := by exact_mod_cast hnegative.1
    rw [NetworkSimplex.ThresholdOracle.cast_weightedValue] at hn
    have hval : NetworkSimplex.ThresholdOracle.realCut
        (fun r : PackedRow m L => (r.value : ℝ)) rows = rows.eval D.toReal.rowRhs := by
      unfold NetworkSimplex.ThresholdOracle.realCut EncodedCut.eval
      apply congrArg List.sum
      apply List.map_congr_left
      intro t ht
      dsimp only
      rw [(D.indexedRows_spec packNormal (packed_row_source D (generalLibrary m) hr ht)).2]
    rw [hval] at hn
    refine ⟨hn, ?_⟩
    intro E hclasses hbypass hmem
    have hec : ∀ i, E.c i 0 = .neither := by rw [← hclasses]; exact hc
    have heh : E.observedH 0 = false := by rw [← hbypass]; exact hh
    obtain ⟨x, hx⟩ := (E.exists_fullProfile_iff_rows hec heh).mp (E.mem_hull_iff.mp hmem).2
    apply (packedOracle_separates_real D (generalLibrary m) (generalLibrary_cancel m)
      hr E x ?_ ((E.rows_iff_reducedProfile x).mp hx)).2
    intro r
    cases r <;> simp [ReductionData.rowNormal, RationalData.toReal, hclasses, hbypass]

/-- Full three-label separation, including domain rejection, has linear work. -/
theorem separateThree_linear {L : ℕ} (D : RationalData 3 L) :
    (separateThree D).2 ≤ 1033 * L + 3228 := by
  have h := separateThree_work D
  have hd := D.domainSeparator_charge_le
  omega

/-- The cached parameter-dependent library is not rebuilt during a query. -/
theorem separateGeneral_work {m L : ℕ} (D : RationalData m L) (hm : 1 ≤ m) :
    (separateGeneral D (generalLibrary m)).2 ≤
      (10 * m * L + 20 * L + 12 * m + 22) +
      26 * m * (L + 1) + 2 ^ (4 * (m + 1) ^ 2) * (2 * m + 3) := by
  have hd := D.domainSeparator_charge_le
  have hp := generalOracle_charge D hm
  cases h : D.domainSeparator.1 <;> simp only [separateGeneral, h] <;> omega

end NetworkSimplex.Chain.Threshold
