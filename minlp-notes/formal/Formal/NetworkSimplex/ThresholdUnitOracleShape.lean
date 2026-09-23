import Formal.NetworkSimplex.ThresholdThreePacked

/-! The executed three-state oracle returns an actual zero row or an actual
source-row circuit branch. The identity holds for every scalar evaluation of
those row identifiers, not only at the candidate that selected them. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdGrouping NetworkSimplex.ThresholdOracle
open scoped BigOperators

local instance unitOracleKeyCountNeZero : NeZero (normalKeyCount 3) := ⟨by decide⟩

/-- Deterministic source identifiers selected by the cached minimizing table.
The fallback is ignored wherever its circuit weight is zero. -/
def selectedThreeBranch {L : ℕ} (D : RationalData 3 L) (k : Fin 11) :
    ProfileRow 3 (Fin L) :=
  (((packedGroup D).table.get (threeKey k)).map (fun r => r.payload)).getD .totalLower

theorem selectedThreeBranch_valid {L : ℕ} (D : RationalData 3 L) (c : Fin 16)
    {rows : EncodedCut 3 L}
    (hs : selectTerms (packedGroup D).table.get (threeCircuit c) = some rows) :
    ThreeBranch D.toReal c (selectedThreeBranch D) := by
  have hp := (dense_selectTerms_exists_iff (packedGroup D).table.get threeKey
    (fun k => (ThreeStateCircuits.weight c k).toNat)).mp ⟨rows, hs⟩
  intro k hk
  cases ht : (packedGroup D).table.get (threeKey k) with
  | none =>
    have hz := hp k ht
    have hn := ThreeStateCircuits.weight_nonnegative c k
    have : ThreeStateCircuits.weight c k = 0 := by omega
    exact (hk this).elim
  | some r =>
    have hm := group_minimum (D.indexedRows packNormal) (threeKey k) ht
    have hspec := D.indexedRows_spec packNormal hm.1
    have hn : normalVector (D.toReal.rowNormal r.payload) = ThreeStateCircuits.normal k := by
      rw [← keyNormal_packNormal, ← hspec.1, hm.2.1, threeKey_normal]
    simpa [selectedThreeBranch, ht] using hn

theorem selectedThreeBranch_eval {L : ℕ} (D : RationalData 3 L) (c : Fin 16)
    {rows : EncodedCut 3 L}
    (hs : selectTerms (packedGroup D).table.get (threeCircuit c) = some rows)
    (f : ProfileRow 3 (Fin L) → ℝ) :
    rows.eval f = ∑ k, (ThreeStateCircuits.weight c k : ℝ) * f (selectedThreeBranch D k) := by
  let g (key : Fin (normalKeyCount 3)) :=
    f ((((packedGroup D).table.get key).map (fun r => r.payload)).getD .totalLower)
  have hh := selectTerms_sum (packedGroup D).table.get (fun r => f r.payload) g
    (fun key row hk => by simp [g, hk]) (threeCircuit c) hs
  simpa only [EncodedCut.eval, realCut, threeCircuit, List.map_ofFn, List.sum_ofFn,
    Function.comp_def, g, selectedThreeBranch, threeWeight_cast] using hh

/-- A reported cut has either one actual zero-normal row, or one of the sixteen
actual source branches. The latter's deterministic row identifiers retain every
scalar evaluation and therefore also all affine coefficients. -/
theorem threeOracle_output_shape {L : ℕ} (D : RationalData 3 L)
    {rows : EncodedCut 3 L} (ho : (threeOracle D).1 = some rows) :
    (∃ r : ProfileRow 3 (Fin L), normalVector (D.toReal.rowNormal r) = 0 ∧
      ∀ f : ProfileRow 3 (Fin L) → ℝ, rows.eval f = f r) ∨
    (∃ c : Fin 16, ThreeBranch D.toReal c (selectedThreeBranch D) ∧
      ∀ f : ProfileRow 3 (Fin L) → ℝ,
        rows.eval f = ∑ k, (ThreeStateCircuits.weight c k : ℝ) *
          f (selectedThreeBranch D k)) := by
  obtain ⟨_, circuit, hc, hs⟩ := circuitOracle_some (packedGroup D).table.get
    (fun r => r.value) threeLibrary ho
  rcases List.mem_cons.mp hc with rfl | hc
  · left
    cases ht : (packedGroup D).table.get 0 with
    | none => simp [selectTerms, ht] at hs
    | some r =>
      simp only [selectTerms, one_ne_zero, ↓reduceIte, ht, Option.some.injEq] at hs
      subst rows
      have hm := group_minimum (D.indexedRows packNormal) 0 ht
      have hspec := D.indexedRows_spec packNormal hm.1
      refine ⟨r.payload, ?_, ?_⟩
      · rw [← keyNormal_packNormal, ← hspec.1, hm.2.1, three_zero]
      · intro f
        simp [EncodedCut.eval, realCut]
  · right
    obtain ⟨c, rfl⟩ := List.mem_ofFn.mp hc
    exact ⟨c, selectedThreeBranch_valid D c hs, selectedThreeBranch_eval D c hs⟩

end NetworkSimplex.Chain.Threshold
