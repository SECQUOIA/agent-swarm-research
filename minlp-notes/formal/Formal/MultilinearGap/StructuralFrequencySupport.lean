import Formal.MultilinearGap.StructuralFrequencyBipartite
import Formal.MultilinearGap.StructuralFrequencyDual
import Formal.MultilinearGap.StructuralCommonAspect

/-! Frequency and incidence graph hypotheses pass to restrictions of each
original factor support. Factor labels remain fixed, so equal restricted
supports remain distinct factors. -/
namespace MultilinearGap
noncomputable section

/-- Removing coordinates from individual rows cannot increase their frequency. -/
theorem frequency_le_two_of_subset {V E : Type*} [Fintype V] [DecidableEq E]
    {S T : V → Finset E} (hsub : ∀ v, T v ⊆ S v)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2) :
    ∀ e, (Finset.univ.filter fun v => e ∈ T v).card ≤ 2 := by
  intro e
  apply le_trans (Finset.card_le_card ?_) (hfreq e)
  intro v hv
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, hsub v (Finset.mem_filter.mp hv).2⟩

/-- A coloring of the original factor graph also colors every support restriction. -/
theorem FrequencyBipartite.of_subset {V E : Type*}
    {S T : V → Finset E} (hbi : FrequencyBipartite S) (hsub : ∀ v, T v ⊆ S v) :
    FrequencyBipartite T := by
  obtain ⟨color,hcolor⟩ := hbi
  exact ⟨color, fun v w e hne hv hw => hcolor v w e hne (hsub v hv) (hsub w hw)⟩

/-- A support restriction cannot create a new odd cycle. -/
theorem FrequencyOddGirthAtLeast.of_subset {V E : Type*}
    {S T : V → Finset E} {g : ℕ} (hg : FrequencyOddGirthAtLeast S g)
    (hsub : ∀ v, T v ⊆ S v) : FrequencyOddGirthAtLeast T g := by
  intro k row edge hrow hedge hinc
  exact hg k row edge hrow hedge (fun i =>
    ⟨hsub (row i) (hinc i).1, hsub (row (i+1)) (hinc i).2⟩)

/-- The indexed original-factor frequency is exactly the support-family frequency. -/
theorem FrequencyTwo.iff_subtype {E : Type*} [DecidableEq E] (S : Finset (Finset E)) :
    FrequencyTwo S ↔
      ∀ e, (Finset.univ.filter fun s : {s // s ∈ S} => e ∈ s.val).card ≤ 2 := by
  simp only [FrequencyTwo, ← FrequencyTwo.card_factorsAt, FrequencyTwo.factorsAt]

theorem FrequencyTwo.subtype_card_le {E : Type*} [DecidableEq E]
    {S : Finset (Finset E)} (hS : FrequencyTwo S) :
    ∀ e, (Finset.univ.filter fun s : {s // s ∈ S} => e ∈ s.val).card ≤ 2 :=
  (FrequencyTwo.iff_subtype S).mp hS

/-- Removing fixed coordinates only restricts each original support. -/
theorem varyingBoxSupport_subset {E : Type*} (l u : E → ℝ) (s : Finset E) :
    varyingBoxSupport l u s ⊆ s := Finset.filter_subset _ _

theorem frequency_le_two_varyingBoxSupport {V E : Type*} [Fintype V] [DecidableEq E]
    {S : V → Finset E}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2) (l u : E → ℝ) :
    ∀ e, (Finset.univ.filter fun v => e ∈ varyingBoxSupport l u (S v)).card ≤ 2 :=
  frequency_le_two_of_subset (fun v => varyingBoxSupport_subset l u (S v)) hfreq

theorem FrequencyBipartite.varyingBoxSupport {V E : Type*}
    {S : V → Finset E} (hbi : FrequencyBipartite S) (l u : E → ℝ) :
    FrequencyBipartite (fun v => varyingBoxSupport l u (S v)) :=
  hbi.of_subset (fun v => varyingBoxSupport_subset l u (S v))

theorem FrequencyOddGirthAtLeast.varyingBoxSupport {V E : Type*}
    {S : V → Finset E} {g : ℕ} (hg : FrequencyOddGirthAtLeast S g) (l u : E → ℝ) :
    FrequencyOddGirthAtLeast (fun v => varyingBoxSupport l u (S v)) g :=
  hg.of_subset (fun v => varyingBoxSupport_subset l u (S v))

end
end MultilinearGap
