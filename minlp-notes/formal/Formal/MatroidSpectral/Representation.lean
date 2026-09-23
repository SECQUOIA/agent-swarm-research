import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Finset.Sort
import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise

/-! Rational column representations with the row count fixed during restrictions.

The determinant test uses the original number of rows. In particular, restricting
columns never silently replaces the original rank by a smaller rank.
-/
namespace MatroidSpectral
open Matrix
open scoped BigOperators

abbrev RationalRepresentation (q m : ℕ) := Matrix (Fin q) (Fin m) ℚ

/-- The canonically ordered maximal minor, zero for sets of the wrong size. -/
noncomputable def columnMinor {q m : ℕ} (A : RationalRepresentation q m)
    (B : Finset (Fin m)) : ℚ :=
  if h : B.card = q then (A.submatrix id (B.orderEmbOfFin h)).det else 0

def IsBase {q m : ℕ} (A : RationalRepresentation q m) (B : Finset (Fin m)) : Prop :=
  columnMinor A B ≠ 0

theorem IsBase.card {q m : ℕ} {A : RationalRepresentation q m} {B : Finset (Fin m)}
    (h : IsBase A B) : B.card = q := by
  by_contra hn
  exact h (by simp [columnMinor, hn])

theorem isBase_iff {q m : ℕ} {A : RationalRepresentation q m} {B : Finset (Fin m)}
    (h : B.card = q) :
    IsBase A B ↔ (A.submatrix id (B.orderEmbOfFin h)).det ≠ 0 := by
  simp [IsBase, columnMinor, h]

/-- This finite family specifies the bases; it is not a polynomial enumeration algorithm. -/
noncomputable def bases {q m : ℕ} (A : RationalRepresentation q m) :
    Finset (Finset (Fin m)) := by
  classical
  exact Finset.univ.filter (IsBase A)

@[simp] theorem mem_bases {q m : ℕ} {A : RationalRepresentation q m}
    {B : Finset (Fin m)} : B ∈ bases A ↔ IsBase A B := by
  classical
  simp [bases]

/-- Allowed columns and forced columns are filters on original bases. -/
noncomputable def feasibleBases {q m : ℕ} (A : RationalRepresentation q m)
    (allowed forced : Finset (Fin m)) : Finset (Finset (Fin m)) := by
  classical
  exact (bases A).filter (fun B => B ⊆ allowed ∧ forced ⊆ B)

@[simp] theorem mem_feasibleBases {q m : ℕ} {A : RationalRepresentation q m}
    {allowed forced B : Finset (Fin m)} :
    B ∈ feasibleBases A allowed forced ↔
      IsBase A B ∧ B ⊆ allowed ∧ forced ⊆ B := by
  classical
  simp [feasibleBases]

theorem feasibleBases_mono {q m : ℕ} (A : RationalRepresentation q m)
    {allowed larger forced : Finset (Fin m)} (h : allowed ⊆ larger) :
    feasibleBases A allowed forced ⊆ feasibleBases A larger forced := by
  intro B hB
  rw [mem_feasibleBases] at hB ⊢
  exact ⟨hB.1, hB.2.1.trans h, hB.2.2⟩

theorem feasibleBases_empty_of_card_lt {q m : ℕ} (A : RationalRepresentation q m)
    (allowed forced : Finset (Fin m)) (h : allowed.card < q) :
    feasibleBases A allowed forced = ∅ := by
  apply Finset.eq_empty_iff_forall_notMem.mpr
  intro B hB
  obtain ⟨hb, ha, _⟩ := mem_feasibleBases.mp hB
  have := Finset.card_le_card ha
  rw [hb.card] at this
  omega

theorem forced_card_le {q m : ℕ} {A : RationalRepresentation q m}
    {allowed forced : Finset (Fin m)} (h : (feasibleBases A allowed forced).Nonempty) :
    forced.card ≤ q := by
  obtain ⟨B, hB⟩ := h
  obtain ⟨hb, _, hf⟩ := mem_feasibleBases.mp hB
  simpa [hb.card] using Finset.card_le_card hf

theorem forced_subset_allowed {q m : ℕ} {A : RationalRepresentation q m}
    {allowed forced : Finset (Fin m)} (h : (feasibleBases A allowed forced).Nonempty) :
    forced ⊆ allowed := by
  obtain ⟨B, hB⟩ := h
  obtain ⟨_, ha, hf⟩ := mem_feasibleBases.mp hB
  exact hf.trans ha

/-- A full original base witnesses that restriction preserves the original rank. -/
def PreservesRank {q m : ℕ} (A : RationalRepresentation q m)
    (allowed : Finset (Fin m)) : Prop := ∃ B, IsBase A B ∧ B ⊆ allowed

theorem preservesRank_iff {q m : ℕ} (A : RationalRepresentation q m)
    (allowed : Finset (Fin m)) :
    PreservesRank A allowed ↔ (feasibleBases A allowed ∅).Nonempty := by
  simp [PreservesRank, Finset.Nonempty]

theorem feasible_preservesRank {q m : ℕ} {A : RationalRepresentation q m}
    {allowed forced : Finset (Fin m)} (h : (feasibleBases A allowed forced).Nonempty) :
    PreservesRank A allowed := by
  obtain ⟨B, hB⟩ := h
  obtain ⟨hb, ha, _⟩ := mem_feasibleBases.mp hB
  exact ⟨B, hb, ha⟩

/-- One additional profile coordinate enforces inclusion of all forced owners. -/
def ownerCount {m : ℕ} (forced B : Finset (Fin m)) : ℕ :=
  ∑ e ∈ B, if e ∈ forced then 1 else 0

theorem ownerCount_eq_card_inter {m : ℕ} (forced B : Finset (Fin m)) :
    ownerCount forced B = (B ∩ forced).card := by
  classical
  simp [ownerCount]

theorem ownerCount_eq_iff {m : ℕ} (forced B : Finset (Fin m)) :
    ownerCount forced B = forced.card ↔ forced ⊆ B := by
  rw [ownerCount_eq_card_inter]
  constructor
  · intro h
    have heq : B ∩ forced = forced := Finset.eq_of_subset_of_card_le
      Finset.inter_subset_right (by omega)
    rw [← heq]
    exact Finset.inter_subset_left
  · intro h
    rw [Finset.inter_eq_right.mpr h]

@[simp] theorem isBase_zero_iff {m : ℕ} (A : RationalRepresentation 0 m)
    (B : Finset (Fin m)) : IsBase A B ↔ B = ∅ := by
  constructor
  · intro h
    exact Finset.card_eq_zero.mp h.card
  · rintro rfl
    simp [IsBase, columnMinor]

@[simp] theorem bases_zero {m : ℕ} (A : RationalRepresentation 0 m) :
    bases A = {∅} := by
  ext B
  simp

theorem orderedMinor_injective {q m : ℕ} (A : RationalRepresentation q m)
    (b : Fin q → Fin m) (h : (A.submatrix id b).det ≠ 0) : Function.Injective b := by
  intro i j hij
  by_contra hn
  apply h
  exact Matrix.det_zero_of_column_eq hn (fun k => by simp [Matrix.submatrix, hij])

theorem orderedMinor_eq_perm {q m : ℕ} (A : RationalRepresentation q m)
    (b : Fin q → Fin m) (hb : Function.Injective b) :
    ∃ e : Equiv.Perm (Fin q),
      (A.submatrix id b).det = Equiv.Perm.sign e * columnMinor A (Finset.univ.image b) := by
  classical
  let B := Finset.univ.image b
  have hcard : B.card = q := by
    simp [B, Finset.card_image_of_injective _ hb]
  let f : Fin q → B := fun i => ⟨b i, Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩⟩
  have hf : Function.Bijective f := by
    constructor
    · intro i j hij
      apply hb
      exact congrArg Subtype.val hij
    · intro x
      obtain ⟨i, _, hi⟩ := Finset.mem_image.mp x.property
      exact ⟨i, Subtype.ext hi⟩
  let e := (Equiv.ofBijective f hf).trans (B.orderIsoOfFin hcard).toEquiv.symm
  have he : ∀ i, B.orderEmbOfFin hcard (e i) = b i := by
    intro i
    change ↑((B.orderIsoOfFin hcard) ((B.orderIsoOfFin hcard).symm (f i))) = b i
    simp [f]
  refine ⟨e, ?_⟩
  have hmat : A.submatrix id b = (A.submatrix id (B.orderEmbOfFin hcard)).submatrix id e := by
    ext i j
    simp [Matrix.submatrix, he]
  rw [hmat, Matrix.det_permute']
  simp [columnMinor, hcard, B]

theorem orderedMinor_isBase {q m : ℕ} (A : RationalRepresentation q m)
    (b : Fin q → Fin m) :
    IsBase A (Finset.univ.image b) ↔ (A.submatrix id b).det ≠ 0 := by
  classical
  by_cases hb : Function.Injective b
  · obtain ⟨e, he⟩ := orderedMinor_eq_perm A b hb
    rw [he]
    simp [IsBase]
  · constructor
    · intro h
      have hcard := h.card
      have hh : Function.Injective b := by
        have hi : Set.InjOn b (↑(Finset.univ : Finset (Fin q))) :=
          Finset.card_image_iff.mp (by simpa using hcard)
        intro i j hij
        exact hi (Finset.mem_univ _) (Finset.mem_univ _) hij
      exact (hb hh).elim
    · intro h
      exact (hb (orderedMinor_injective A b h)).elim

theorem IsBase.exists_orderedMinor {q m : ℕ} {A : RationalRepresentation q m}
    {B : Finset (Fin m)} (h : IsBase A B) :
    ∃ b : Fin q → Fin m, Finset.univ.image b = B ∧ (A.submatrix id b).det ≠ 0 := by
  exact ⟨B.orderEmbOfFin h.card, B.image_orderEmbOfFin_univ h.card,
    (isBase_iff h.card).mp h⟩

end MatroidSpectral
