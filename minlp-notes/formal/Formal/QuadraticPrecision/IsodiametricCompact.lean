import Formal.QuadraticPrecision.IsodiametricDiameterClosed
import Mathlib.Topology.Sets.VietorisTopology
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.MeasureTheory.Measure.Regular

open Set TopologicalSpace MeasureTheory

namespace QuadraticPrecision

/-- Outer regularity makes compact-set measure upper semicontinuous in the
Vietoris topology. The measure need not be finite. -/
theorem upperSemicontinuous_compact_measure {E : Type*} [TopologicalSpace E]
    [MeasurableSpace E] [BorelSpace E] (μ : Measure E) [μ.OuterRegular] :
    UpperSemicontinuous (fun K : Compacts E => μ (K : Set E)) := by
  intro K r hr
  obtain ⟨U, hKU, hU, hμU⟩ := (K : Set E).exists_isOpen_lt_of_lt r hr
  filter_upwards [(Compacts.isOpen_subsets_of_isOpen hU).mem_nhds hKU] with L hL
  exact (measure_mono hL).trans_lt hμU

/-- A closed, nonempty family of compact subsets of a fixed compact set admits
a measure maximizer. This includes the empty compact set. -/
theorem exists_compact_measure_maximizer_of_closed
    {E : Type*} [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [μ.OuterRegular] (Q : Set E) (hQ : IsCompact Q)
    (P : Set (Compacts E)) (hP : IsClosed P)
    (hne : ∃ K : Compacts E, (K : Set E) ⊆ Q ∧ K ∈ P) :
    ∃ K : Compacts E, (K : Set E) ⊆ Q ∧ K ∈ P ∧
      ∀ L : Compacts E, (L : Set E) ⊆ Q → L ∈ P → μ (L : Set E) ≤ μ (K : Set E) := by
  have hc : IsCompact ({K : Compacts E | (K : Set E) ⊆ Q} ∩ P) :=
    (Compacts.isCompact_subsets_of_isCompact hQ).inter_right hP
  obtain ⟨K, hK, hm⟩ := UpperSemicontinuousOn.exists_isMaxOn hne hc
    ((upperSemicontinuous_compact_measure μ).upperSemicontinuousOn _)
  exact ⟨K, hK.1, hK.2, fun L hL hLP => hm ⟨hL, hLP⟩⟩

/-- A compact set of bounded diameter maximizing an outer regular measure
among compact subsets of a specified compact ambient set. -/
theorem exists_compact_measure_maximizer
    {E : Type*} [PseudoMetricSpace E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [μ.OuterRegular] (Q : Set E) (hQ : IsCompact Q) (D : ℝ) :
    ∃ K : Set E, IsCompact K ∧ K ⊆ Q ∧
      (∀ x ∈ K, ∀ y ∈ K, dist x y ≤ D) ∧
      ∀ L : Set E, IsCompact L → L ⊆ Q →
        (∀ x ∈ L, ∀ y ∈ L, dist x y ≤ D) → μ L ≤ μ K := by
  obtain ⟨K, hKQ, hKD, hmax⟩ := exists_compact_measure_maximizer_of_closed μ Q hQ
    {K : Compacts E | ∀ x ∈ (K : Set E), ∀ y ∈ (K : Set E), dist x y ≤ D}
    (Isodiametric.isClosed_diameter_le D) ⟨⟨∅, isCompact_empty⟩, Set.empty_subset Q,
      fun _ hx => False.elim hx⟩
  exact ⟨K, K.isCompact, hKQ, hKD, fun L hL hLQ hLD => hmax ⟨L, hL⟩ hLQ hLD⟩

end QuadraticPrecision
