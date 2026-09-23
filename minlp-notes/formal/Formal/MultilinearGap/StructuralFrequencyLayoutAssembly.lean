import Formal.MultilinearGap.StructuralFrequencyLayout
import Formal.MultilinearGap.StructuralFrequencyRounding

/-! Assembly of component cycles into the global finite rounding layout. -/
namespace MultilinearGap.FrequencySlab
open Set StructuralFrequencyCycle
noncomputable section
variable {V E C : Type*} [Fintype V] [Fintype E] [DecidableEq E]

private theorem finCongr_sub_one {m n : ℕ} [NeZero m] [NeZero n]
    (h : m = n) (i : Fin m) : finCongr h (i - 1) = finCongr h i - 1 := by
  subst n
  rfl

/-- Disjoint indexed odd cycles covering the fractional coordinates provide the
complete layout consumed by the explicit product rounding law. -/
theorem frequencyCycleLayout_of_indexed_cycles {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    (A : C → Set V) (D : ∀ c, IndexedFractionalCycle S x (A c))
    (hodd : ∀ c, Odd (D c).n)
    (hrow : Function.Injective (fun t : (c : C) × Fin (D c).n => (D t.1).row t.2))
    (hcover : ∀ e ∈ fractional x, ∃ c i, (D c).edge i = e) :
    Nonempty (FrequencyCycleLayout S x C) := by
  classical
  let size : C → ℕ := fun c => ((D c).n - 3) / 2
  have hsize (c : C) : 2 * size c + 3 = (D c).n := by
    have hthree := (D c).three_le
    obtain ⟨k, hk⟩ := hodd c
    dsimp [size]
    omega
  let q (c : C) : Cycle (size c) ≃ Fin (D c).n := finCongr (hsize c)
  have hqsub (c : C) (i : Cycle (size c)) : q c (i-1) = q c i - 1 :=
    finCongr_sub_one (hsize c) i
  have hedge : Function.Injective (fun t : (c : C) × Fin (D c).n => (D t.1).edge t.2) := by
    rintro ⟨c,i⟩ ⟨d,j⟩ hij
    change (D c).edge i = (D d).edge j at hij
    have hc : (D c).edge i ∈ S ((D c).row i) :=
      ((D c).endpoints i _).mpr (Or.inl rfl)
    rw [hij] at hc
    have hcd : c = d := by
      rcases ((D d).endpoints j _).mp hc with hr | hr
      · exact congrArg Sigma.fst (hrow (a₁ := ⟨c,i⟩) (a₂ := ⟨d,j⟩) hr)
      · exact congrArg Sigma.fst (hrow (a₁ := ⟨c,i⟩) (a₂ := ⟨d,j+1⟩) hr)
    subst d
    have hh := (D c).edge_injective hij
    subst j
    rfl
  refine ⟨{
    size := size
    edge := fun c i => (D c).edge (q c i)
    edge_injective := ?_
    row := fun c i => (D c).row (q c i)
    row_injective := ?_
    half := ?_
    integral := ?_
    incident := ?_
    outside := ?_
  }⟩
  · rintro ⟨c,i⟩ ⟨d,j⟩ hij
    have hh := hedge (a₁ := ⟨c,q c i⟩) (a₂ := ⟨d,q d j⟩) hij
    have hc : c = d := congrArg Sigma.fst hh
    subst d
    have hi : q c i = q c j := by
      simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and, and_self] using hh
    have := (q c).injective hi
    subst j
    rfl
  · rintro ⟨c,i⟩ ⟨d,j⟩ hij
    have hh := hrow (a₁ := ⟨c,q c i⟩) (a₂ := ⟨d,q d j⟩) hij
    have hc : c = d := congrArg Sigma.fst hh
    subst d
    have hi : q c i = q c j := by
      simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and, and_self] using hh
    have := (q c).injective hi
    subst j
    rfl
  · intro c i
    exact extreme_fractional_eq_half hfreq hx ((D c).fractional_edge (q c i))
  · intro e he
    apply binary_of_not_fractional hx.1.1
    intro hf
    obtain ⟨c,i,hi⟩ := hcover e hf
    exact he ⟨c, (q c).symm i, by simpa using hi⟩
  · intro c i e
    rw [hqsub]
    have hf : x e = 1 / 2 ↔ e ∈ fractional x := by
      constructor
      · intro hh
        norm_num [fractional, hh]
      · exact extreme_fractional_eq_half hfreq hx
    rw [hf]
    exact (D c).incident hfreq hx (q c i) e
  · intro v hv e he
    apply binary_of_not_fractional hx.1.1
    intro hf
    obtain ⟨c,i,rfl⟩ := hcover e hf
    rcases ((D c).endpoints i v).mp he with hh | hh
    · exact hv ⟨c, (q c).symm i, by simpa using hh.symm⟩
    · exact hv ⟨c, (q c).symm (i+1), by simpa using hh.symm⟩

omit [Fintype E] in
/-- Every extreme frequency-two degree-slab point has a complete disjoint
odd-cycle layout, with all other coordinates integral. -/
theorem exists_frequencyCycleLayout [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    ∃ n : ℕ, Nonempty (FrequencyCycleLayout S x (Fin n)) := by
  classical
  let : Fintype E := Fintype.ofFinite E
  obtain ⟨n, A, D, hrow, hcover⟩ := exists_indexed_cycle_family hfreq hx
  exact ⟨n, frequencyCycleLayout_of_indexed_cycles hfreq hx A D
    (fun c => (D c).odd hx hfreq) hrow hcover⟩

end
end MultilinearGap.FrequencySlab
