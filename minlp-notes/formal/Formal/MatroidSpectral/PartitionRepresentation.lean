import Formal.MatroidSpectral.UniformRepresentation
import Formal.MatroidSpectral.RepresentationReduction
import Mathlib.LinearAlgebra.StdBasis
import Mathlib.LinearAlgebra.Dimension.Finite

/-! Direct sums of rational Vandermonde representations realize exact partition
quotas. The representation is explicit and its columns retain group identities. -/
namespace MatroidSpectral
open Matrix ReciprocalAnchor DAGSpectral
open scoped BigOperators
noncomputable section
variable {k : ℕ} (q m : Fin k → ℕ)

abbrev PartitionRows := (g : Fin k) → Fin (q g) → ℚ
abbrev PartitionElements := Σ g : Fin k, Fin (m g)

def partitionColumn (e : PartitionElements m) : PartitionRows q :=
  Pi.single e.1 (fun i => (((e.2.val+1 : ℕ) : ℚ)^i.val))

def flattenPartitionRows : PartitionRows q →ₗ[ℚ]
    (Fin (Fintype.card (Σ g : Fin k, Fin (q g))) → ℚ) where
  toFun f i := let r := (Fintype.equivFin (Σ g : Fin k, Fin (q g))).symm i; f r.1 r.2
  map_add' := by intros; rfl
  map_smul' := by intros; rfl

theorem flattenPartitionRows_injective : Function.Injective (flattenPartitionRows q) := by
  intro f h he
  funext g i
  have hh := congrFun he (Fintype.equivFin (Σ g : Fin k, Fin (q g)) ⟨g,i⟩)
  change f _ _ = h _ _ at hh
  rw [Equiv.symm_apply_apply] at hh
  exact hh

def partitionRepresentation : RationalRepresentation
    (Fintype.card (Σ g : Fin k, Fin (q g))) (Fintype.card (PartitionElements m)) :=
  fun i j => flattenPartitionRows q
    (partitionColumn q m ((Fintype.equivFin (PartitionElements m)).symm j)) i

def partitionSelection (S : (g : Fin k) → Finset (Fin (m g))) :
    Finset (Fin (Fintype.card (PartitionElements m))) :=
  (Finset.univ.sigma S).map (Fintype.equivFin (PartitionElements m)).toEmbedding

@[simp] theorem partitionSelection_card (S : (g : Fin k) → Finset (Fin (m g))) :
    (partitionSelection m S).card = ∑ g, (S g).card := by
  simp [partitionSelection]

def selectedPartitionEquiv (S : (g : Fin k) → Finset (Fin (m g))) :
    (Σ g : Fin k, S g) ≃ partitionSelection m S :=
  Equiv.ofBijective
    (fun e => ⟨Fintype.equivFin (PartitionElements m) ⟨e.1,e.2⟩,
      by simp [partitionSelection, e.2.property]⟩)
    (by
      constructor
      · intro e f h
        have hh := (Fintype.equivFin (PartitionElements m)).injective
          (congrArg Subtype.val h)
        cases e with | mk g e =>
          cases f with | mk h f =>
            simp only [Sigma.mk.inj_iff] at hh
            obtain ⟨rfl, hh⟩ := hh
            exact congrArg (Sigma.mk g) (Subtype.ext (eq_of_heq hh))
      · intro e
        have he := e.property
        simp only [partitionSelection, Finset.mem_map] at he
        obtain ⟨f,hf,he⟩ := he
        refine ⟨⟨f.1,⟨f.2, (Finset.mem_sigma.mp hf).2⟩⟩, ?_⟩
        exact Subtype.ext he)

theorem partition_independent_iff (S : (g : Fin k) → Finset (Fin (m g))) :
    ColumnIndependent (partitionRepresentation q m) (partitionSelection m S) ↔
      LinearIndependent ℚ (fun e : Σ g : Fin k, S g =>
        partitionColumn q m ⟨e.1,e.2⟩) := by
  rw [ColumnIndependent, ← linearIndependent_equiv (selectedPartitionEquiv m S)]
  have he : (fun e : partitionSelection m S =>
      (partitionRepresentation q m).col e) ∘ selectedPartitionEquiv m S =
      (flattenPartitionRows q) ∘ (fun e : Σ g : Fin k, S g =>
        partitionColumn q m ⟨e.1,e.2⟩) := by
    funext e i
    change flattenPartitionRows q (partitionColumn q m
      ((Fintype.equivFin (PartitionElements m)).symm
        ((Fintype.equivFin (PartitionElements m)) ⟨e.1,e.2⟩))) i = _
    rw [Equiv.symm_apply_apply]
    rfl
  rw [he]
  exact (flattenPartitionRows q).linearIndependent_iff
    (LinearMap.ker_eq_bot.mpr (flattenPartitionRows_injective q))

theorem partition_independent_card_le (S : (g : Fin k) → Finset (Fin (m g)))
    (h : ColumnIndependent (partitionRepresentation q m) (partitionSelection m S))
    (g : Fin k) : (S g).card ≤ q g := by
  have hh := (partition_independent_iff q m S).mp h
  have hg := hh.comp (fun e : S g => (⟨g,e⟩ : Σ g : Fin k, S g))
    (fun _ _ h => by cases h; rfl)
  have hu : LinearIndependent ℚ (fun e : S g =>
      fun i : Fin (q g) => (((e.val.val+1 : ℕ) : ℚ)^i.val)) :=
    hg.of_comp (LinearMap.single ℚ (fun g => Fin (q g) → ℚ) g)
  simpa using hu.fintype_card_le_finrank

theorem partition_independent_of_quotas (S : (g : Fin k) → Finset (Fin (m g)))
    (hS : ∀ g, (S g).card = q g) :
    ColumnIndependent (partitionRepresentation q m) (partitionSelection m S) := by
  apply (partition_independent_iff q m S).mpr
  let v := fun g : Fin k => fun e : S g =>
    fun i : Fin (q g) => (((e.val.val+1 : ℕ) : ℚ)^i.val)
  have hv : ∀ g, LinearIndependent ℚ (v g) := by
    intro g
    have hb := (uniform_isBase_iff (S g)).mpr (hS g)
    have hi := Matrix.linearIndependent_cols_of_det_ne_zero ((isBase_iff (hS g)).mp hb)
    exact (columnIndependent_iff_ordered (uniformRepresentation (q g) (m g))
      (S g) (hS g)).mpr hi
  simpa only [partitionColumn] using Pi.linearIndependent_single v hv

theorem isBase_iff_card_columnIndependent {a n : ℕ} (A : RationalRepresentation a n)
    (B : Finset (Fin n)) : IsBase A B ↔ B.card = a ∧ ColumnIndependent A B := by
  constructor
  · intro h
    refine ⟨h.card, ?_⟩
    rw [columnIndependent_iff_ordered _ _ h.card]
    exact Matrix.linearIndependent_cols_of_det_ne_zero ((isBase_iff h.card).mp h)
  · rintro ⟨hc, hi⟩
    rw [isBase_iff hc]
    rw [columnIndependent_iff_ordered _ _ hc] at hi
    exact isUnit_iff_ne_zero.mp ((Matrix.isUnit_iff_isUnit_det _).mp
      (Matrix.linearIndependent_cols_iff_isUnit.mp hi))

/-- Exact base feasibility is exactly the quota in every group. -/
theorem partition_isBase_iff (S : (g : Fin k) → Finset (Fin (m g))) :
    IsBase (partitionRepresentation q m) (partitionSelection m S) ↔
      ∀ g, (S g).card = q g := by
  rw [isBase_iff_card_columnIndependent, partitionSelection_card]
  simp only [Fintype.card_sigma, Fintype.card_fin]
  constructor
  · rintro ⟨hc, hi⟩ g
    have hl := partition_independent_card_le q m S hi
    exact (Finset.sum_eq_sum_iff_of_le (fun g _ => hl g)).mp hc g (Finset.mem_univ _)
  · intro hS
    exact ⟨Finset.sum_congr rfl (fun g _ => hS g), partition_independent_of_quotas q m S hS⟩

def partitionGroups (B : Finset (Fin (Fintype.card (PartitionElements m))))
    (g : Fin k) : Finset (Fin (m g)) :=
  Finset.univ.filter (fun e => Fintype.equivFin (PartitionElements m) ⟨g,e⟩ ∈ B)

/-- Every finite column selection has the grouped form used by the quota theorem. -/
theorem partitionSelection_groups
    (B : Finset (Fin (Fintype.card (PartitionElements m)))) :
    partitionSelection m (partitionGroups m B) = B := by
  ext e
  simp only [partitionSelection, Finset.mem_map]
  constructor
  · rintro ⟨x,hx,rfl⟩
    exact (Finset.mem_filter.mp (Finset.mem_sigma.mp hx).2).2
  · intro he
    refine ⟨(Fintype.equivFin (PartitionElements m)).symm e, ?_, by simp⟩
    simp [partitionGroups, he]

theorem partition_arbitrary_isBase_iff
    (B : Finset (Fin (Fintype.card (PartitionElements m)))) :
    IsBase (partitionRepresentation q m) B ↔
      ∀ g, (partitionGroups m B g).card = q g := by
  conv_lhs => rw [← partitionSelection_groups m B]
  exact partition_isBase_iff q m _

theorem partition_has_base (hq : ∀ g, q g ≤ m g) :
    ∃ B, IsBase (partitionRepresentation q m) B := by
  let S := fun g => Finset.univ.image (Fin.castLE (hq g))
  refine ⟨partitionSelection m S, (partition_isBase_iff q m S).mpr ?_⟩
  intro g
  simp [S, Finset.card_image_of_injective _ (Fin.castLE_injective (hq g))]

theorem partitionColumn_bits (Q M : ℕ) (hq : ∀ g, q g ≤ Q) (hm : ∀ g, m g ≤ M)
    (e : PartitionElements m) (r : Σ g : Fin k, Fin (q g)) :
    RationalBits (partitionColumn q m e r.1 r.2) ((M+1)*(Q+1)+1) := by
  rcases e with ⟨g,e⟩
  rcases r with ⟨h,i⟩
  by_cases hh : h = g
  · subst h
    simp only [partitionColumn, Pi.single_eq_same]
    exact rationalBits_mono (uniformRepresentation_bits (q g) (m g) i e)
      (by nlinarith [hq g, hm g])
  · simp only [partitionColumn, Pi.single_eq_of_ne hh, Pi.zero_apply]
    exact rationalBits_mono rationalBits_zero (by omega)

/-- Padding with zero blocks adds no large coefficients. -/
theorem partitionRepresentation_bits (Q M : ℕ)
    (hq : ∀ g, q g ≤ Q) (hm : ∀ g, m g ≤ M) :
    MatrixBits (partitionRepresentation q m) ((M+1)*(Q+1)+1) := by
  intro i j
  exact partitionColumn_bits q m Q M hq hm
    ((Fintype.equivFin (PartitionElements m)).symm j)
    ((Fintype.equivFin (Σ g : Fin k, Fin (q g))).symm i)

end
end MatroidSpectral
