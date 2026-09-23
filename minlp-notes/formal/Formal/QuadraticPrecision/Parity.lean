import Formal.QuadraticPrecision.Model
import Mathlib.Topology.Constructions.SumProd
import Mathlib.Topology.Instances.ENNReal.Lemmas

/-! Parity contacts from unrestricted integer lifts. Raw contacts are arbitrary
sets. Closure is taken only after establishing a closed midpoint relation. -/
namespace QuadraticPrecision
open Set

abbrev ParityCode (p : ℕ) := Fin p → Fin 2

def parityCode {p : ℕ} (z : Fin p → ℤ) : ParityCode p :=
  fun i => ⟨(z i % 2).toNat, by
    have := Int.emod_nonneg (z i) (by norm_num : (2 : ℤ) ≠ 0)
    have := Int.emod_lt_of_pos (z i) (by norm_num : (0 : ℤ) < 2)
    omega⟩

theorem card_parityCode (p : ℕ) : Fintype.card (ParityCode p) = 2 ^ p := by
  simp [ParityCode]

namespace ConvexIntegerLift
variable {n p q : ℕ}

def rawContact (L : ConvexIntegerLift n p q) (D : Set (Input n))
    (f : Input n → ℝ) (α : ParityCode p) : Set (Input n) :=
  {x | x ∈ D ∧ ∃ z : Fin p → ℤ,
    parityCode z = α ∧ (x, f x) ∈ L.sectionAt (fun i => (z i : ℝ))}

theorem rawContact_cover (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ}
    (hgraph : ∀ x ∈ D, (x, f x) ∈ L.relaxation) :
    D ⊆ ⋃ α, L.rawContact D f α := by
  intro x hx
  obtain ⟨z, hz⟩ := hgraph x hx
  exact mem_iUnion.mpr ⟨parityCode z, hx, z, rfl, hz⟩

theorem rawContact_midpoint (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ} {α : ParityCode p}
    {x y : Input n} (hx : x ∈ L.rawContact D f α)
    (hy : y ∈ L.rawContact D f α) :
    ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y, (f x + f y) / 2) ∈ L.relaxation := by
  obtain ⟨_, z, hz, hx⟩ := hx
  obtain ⟨_, z', hz', hy⟩ := hy
  have hmod (i : Fin p) : z i % 2 = z' i % 2 := by
    have h := congrArg (fun c : ParityCode p => (c i).val) (hz.trans hz'.symm)
    dsimp [parityCode] at h
    have := Int.emod_nonneg (z i) (by norm_num : (2 : ℤ) ≠ 0)
    have := Int.emod_nonneg (z' i) (by norm_num : (2 : ℤ) ≠ 0)
    omega
  refine ⟨fun i => (z i + z' i) / 2, ?_⟩
  have hindex : (fun i => (((z i + z' i) / 2 : ℤ) : ℝ)) =
      (1 / 2 : ℝ) • (fun i => (z i : ℝ)) + (1 / 2 : ℝ) • (fun i => (z' i : ℝ)) := by
    funext i
    have hi : 2 * ((z i + z' i) / 2) = z i + z' i := by
      have := hmod i
      omega
    have hi' : (2 : ℝ) * (((z i + z' i) / 2 : ℤ) : ℝ) = (z i : ℝ) + (z' i : ℝ) := by
      exact_mod_cast hi
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    linarith
  rw [hindex]
  convert L.section_mix hx hy (by norm_num : (0 : ℝ) ≤ 1 / 2)
      (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (1 / 2 : ℝ) + 1 / 2 = 1) using 1
  simp [Prod.smul_mk, smul_eq_mul]
  ring

/-- A closed pair relation survives passage to compact parity contacts.
No measurability, boundedness of integer indices, or closure of the lift is assumed. -/
theorem compact_parity_cover (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ} (hD : IsCompact D)
    (hgraph : ∀ x ∈ D, (x, f x) ∈ L.relaxation)
    {E : Set (Input n × Input n)} (hE : IsClosed E)
    (herr : ∀ x y, ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y, (f x + f y) / 2) ∈
      L.relaxation → (x, y) ∈ E) :
    ∃ S : ParityCode p → Set (Input n),
      (∀ α, IsCompact (S α)) ∧ (∀ α, S α ⊆ D) ∧
      (D ⊆ ⋃ α, S α) ∧ ∀ α, ∀ x ∈ S α, ∀ y ∈ S α, (x, y) ∈ E := by
  refine ⟨fun α => closure (L.rawContact D f α), ?_, ?_, ?_, ?_⟩
  · intro α
    exact hD.of_isClosed_subset isClosed_closure (closure_minimal (fun _ h => h.1) hD.isClosed)
  · intro α
    exact closure_minimal (fun _ h => h.1) hD.isClosed
  · exact (L.rawContact_cover hgraph).trans (iUnion_mono fun _ => subset_closure)
  · intro α x hx y hy
    have hsub : L.rawContact D f α ×ˢ L.rawContact D f α ⊆ E := by
      intro v hv
      exact herr v.1 v.2 (L.rawContact_midpoint hv.1 hv.2)
    apply closure_minimal hsub hE
    rw [closure_prod_eq]
    exact ⟨hx, hy⟩

/-- Scalar graph contacts, obtained from an actual convex integer lift. -/
theorem graph_compact_parity_cover (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ}
    (hD : IsCompact D) (hf : Continuous f)
    (hR : IsGraphRelaxation D f ε L.relaxation) :
    ∃ S : ParityCode p → Set (Input n),
      (∀ α, IsCompact (S α)) ∧ (∀ α, S α ⊆ D) ∧
      (D ⊆ ⋃ α, S α) ∧ ∀ α, ∀ x ∈ S α, ∀ y ∈ S α,
        |(f x + f y) / 2 - f ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y)| ≤ ε := by
  apply L.compact_parity_cover hD hR.1 (E := {v |
    |(f v.1 + f v.2) / 2 - f ((1 / 2 : ℝ) • v.1 + (1 / 2 : ℝ) • v.2)| ≤ ε})
  · exact isClosed_le (by fun_prop) continuous_const
  · intro x y h
    exact (hR.2 _ h).2

/-- The epigraph obstruction has the opposite sign from the hypograph one. -/
theorem epigraph_compact_parity_cover (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ}
    (hD : IsCompact D) (hf : Continuous f)
    (hR : IsEpigraphRelaxation D f ε L.relaxation) :
    ∃ S : ParityCode p → Set (Input n),
      (∀ α, IsCompact (S α)) ∧ (∀ α, S α ⊆ D) ∧
      (D ⊆ ⋃ α, S α) ∧ ∀ α, ∀ x ∈ S α, ∀ y ∈ S α,
        f ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y) - (f x + f y) / 2 ≤ ε := by
  apply L.compact_parity_cover hD (fun x hx => hR.1 x hx (f x) le_rfl) (E := {v |
    f ((1 / 2 : ℝ) • v.1 + (1 / 2 : ℝ) • v.2) - (f v.1 + f v.2) / 2 ≤ ε})
  · exact isClosed_le (by fun_prop) continuous_const
  · intro x y h
    have := (hR.2 _ h).2
    dsimp at this ⊢
    linarith

theorem hypograph_compact_parity_cover (L : ConvexIntegerLift n p q)
    {D : Set (Input n)} {f : Input n → ℝ} {ε : ℝ}
    (hD : IsCompact D) (hf : Continuous f)
    (hR : IsHypographRelaxation D f ε L.relaxation) :
    ∃ S : ParityCode p → Set (Input n),
      (∀ α, IsCompact (S α)) ∧ (∀ α, S α ⊆ D) ∧
      (D ⊆ ⋃ α, S α) ∧ ∀ α, ∀ x ∈ S α, ∀ y ∈ S α,
        (f x + f y) / 2 - f ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y) ≤ ε := by
  apply L.compact_parity_cover hD (fun x hx => hR.1 x hx (f x) le_rfl) (E := {v |
    (f v.1 + f v.2) / 2 - f ((1 / 2 : ℝ) • v.1 + (1 / 2 : ℝ) • v.2) ≤ ε})
  · exact isClosed_le (by fun_prop) continuous_const
  · intro x y h
    have := (hR.2 _ h).2
    dsimp at this ⊢
    linarith

end ConvexIntegerLift
end QuadraticPrecision
