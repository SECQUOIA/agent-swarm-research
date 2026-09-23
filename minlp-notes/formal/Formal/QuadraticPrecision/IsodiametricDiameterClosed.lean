import Mathlib.Topology.Sets.VietorisTopology
import Mathlib.Topology.MetricSpace.Basic

/-! Diameter constraints form a closed family in the compact hyperspace. -/
open Set TopologicalSpace
namespace QuadraticPrecision.Isodiametric

lemma isClosed_diameter_le {E : Type*} [PseudoMetricSpace E] (D : ℝ) :
    IsClosed {K : Compacts E | ∀ x ∈ (K : Set E), ∀ y ∈ (K : Set E), dist x y ≤ D} := by
  have hf : Continuous (fun K : Compacts E => K ×ˢ K) :=
    Compacts.continuous_prod.comp (continuous_id.prodMk continuous_id)
  have hc : IsClosed {L : Compacts (E × E) |
      (L : Set (E × E)) ⊆ {p | dist p.1 p.2 ≤ D}} :=
    Compacts.isClosed_subsets_of_isClosed
      (isClosed_le (continuous_fst.dist continuous_snd) continuous_const)
  convert hc.preimage hf using 1
  ext K
  simp only [mem_preimage, mem_ofPred_eq, Compacts.coe_prod, Set.prod_subset_iff]

end QuadraticPrecision.Isodiametric
