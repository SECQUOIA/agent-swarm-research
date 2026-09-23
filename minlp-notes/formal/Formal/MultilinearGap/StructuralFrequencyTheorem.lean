import Formal.MultilinearGap.StructuralFrequencyLayoutAssembly
import Formal.MultilinearGap.StructuralFrequencyBound
import Formal.MultilinearGap.StructuralFrequencyBipartite

/-! Sharp scalar cardinality-gap bounds from actual frequency-two supports.
The extreme-point decomposition and fractional odd-cycle layouts are constructed
from the incidence hypothesis, rather than supplied as premises. -/
namespace MultilinearGap
open CubicGap FrequencySlab
noncomputable section
variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq E]

omit [Fintype E] in
/-- Every cube mean decomposes into slab points equipped with proved layouts. -/
theorem exists_frequency_slab_layouts [Finite E] (S : V → Finset E)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (x : E → ℝ) (hx : x ∈ cube E) :
    ∃ (n : ℕ) (μ : Law (Fin n)) (z : Fin n → E → ℝ) (m : Fin n → ℕ),
      (∀ a, z a ∈ cube E) ∧
      (∀ e, μ.expect (fun a => z a e) = x e) ∧
      (∀ a v, (countFloor (S v) x : ℝ) ≤ meanSum (S v) (z a) ∧
        meanSum (S v) (z a) ≤ (countFloor (S v) x : ℝ) + 1) ∧
      Nonempty (∀ a, FrequencyCycleLayout S (z a) (Fin (m a))) := by
  classical
  let := Fintype.ofFinite E
  let lo : V → ℤ := fun v => countFloor (S v) x
  let hi : V → ℤ := fun v => lo v + 1
  have hmem : x ∈ slab S lo hi := by
    refine ⟨hx, fun v => ?_⟩
    change ((countFloor (S v) x : ℕ) : ℝ) ≤ meanSum (S v) x ∧
      meanSum (S v) x ≤ (((countFloor (S v) x : ℕ) : ℤ) + 1 : ℤ)
    push_cast
    exact ⟨countFloor_le hx, (Nat.lt_floor_add_one _).le⟩
  obtain ⟨n, μ, z, hz, hmean⟩ := exists_extreme_law hfreq hmem
  choose m hm using fun a => exists_frequencyCycleLayout hfreq (hz a)
  refine ⟨n, μ, z, m, fun a => (hz a).1.1, ?_, ?_,
    ⟨fun a => Classical.choice (hm a)⟩⟩
  · intro e
    have h := congrFun hmean e
    simpa [Law.barycenter, Law.expect, Finset.sum_apply] using h
  · intro a v
    have h := (hz a).1.2 v
    simpa [lo, hi, degree, meanSum] using h

/-- The universal three-halves theorem for original convex cardinality factors. -/
theorem frequencyTwo_cardinality_three_halves
    (S : V → Finset E)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (φ : V → ℕ → ℝ) (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (x : E → ℝ) (hx : x ∈ cube E) :
    (∑ v, hullGap (f v) x) ≤ (3 / 2 : ℝ) * hullGap (factorSum f) x := by
  classical
  obtain ⟨n, μ, z, m, hz, hmean, hslab, ⟨D⟩⟩ := exists_frequency_slab_layouts S hfreq x hx
  exact cardinality_gap_three_halves_of_cycle_layouts S φ hφ f hf hv μ z hz x hx
    hmean hslab (fun a => Fin (m a)) D

/-- The sharp odd-girth factor, derived from actual odd cycles in the input. -/
theorem frequencyTwo_cardinality_oddGirth
    (S : V → Finset E)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (g : ℕ) (hg : 1 < g) (hgirth : FrequencyOddGirthAtLeast S g)
    (φ : V → ℕ → ℝ) (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (x : E → ℝ) (hx : x ∈ cube E) :
    (∑ v, hullGap (f v) x) ≤ ((g : ℝ) / ((g : ℝ) - 1)) * hullGap (factorSum f) x := by
  classical
  obtain ⟨n, μ, z, m, hz, hmean, hslab, ⟨D⟩⟩ := exists_frequency_slab_layouts S hfreq x hx
  exact cardinality_gap_girth_of_cycle_layouts S φ hφ f hf hv μ z hz x hx hmean hslab
    (fun a => Fin (m a)) D g (by exact_mod_cast hg) (fun a c => by
      exact_mod_cast (D a).length_le_of_oddGirth hgirth c)

/-- A bipartite dual graph makes every extreme slab layout integral, so all
cardinality-factor lower envelopes are attained simultaneously. -/
theorem frequencyTwo_cardinality_bipartite_le
    (S : V → Finset E)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (hbi : FrequencyBipartite S)
    (φ : V → ℕ → ℝ) (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (x : E → ℝ) (hx : x ∈ cube E) :
    (∑ v, hullGap (f v) x) ≤ hullGap (factorSum f) x := by
  classical
  obtain ⟨n, μ, z, m, hz, hmean, hslab, ⟨D⟩⟩ := exists_frequency_slab_layouts S hfreq x hx
  have h := cardinality_gap_of_cycle_layouts S φ hφ f hf hv μ z hz x hx hmean hslab
    (fun a => Fin (m a)) D 0 (by norm_num) (fun a c => by
      have := (D a).isEmpty_of_bipartite hbi
      exact isEmptyElim c)
  simpa using h

/-- Exact equality for a bipartite dual graph, including signed convex tables. -/
theorem frequencyTwo_cardinality_bipartite
    (S : V → Finset E)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (hbi : FrequencyBipartite S)
    (φ : V → ℕ → ℝ) (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (x : E → ℝ) (hx : x ∈ cube E) :
    (∑ v, hullGap (f v) x) = hullGap (factorSum f) x :=
  le_antisymm (frequencyTwo_cardinality_bipartite_le S hfreq hbi φ hφ f hf hv x hx)
    (hullGap_factorSum_le f hf x hx)

end
end MultilinearGap
