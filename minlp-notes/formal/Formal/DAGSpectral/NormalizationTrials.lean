import Formal.DAGSpectral.NormalizationProducer
import Formal.DAGSpectral.DyadicScale
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Sort

/-! Actual finite rational normalization trials. Labels are distinct even when
factor vectors coincide. Within each trial columns follow increasing label order. -/
namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators

namespace NormalizationTrials
variable {p M m : ℕ}

/-- Exact bit bound computed from the numerator and denominator. -/
def weightBits (w : ℚ) : ℕ := max w.num.natAbs.size w.den.size

theorem weightBits_spec (w : ℚ) : ReciprocalAnchor.RationalBits w (weightBits w) := by
  rw [ReciprocalAnchor.rationalBits_iff_size]
  exact ⟨le_max_left _ _, le_max_right _ _⟩

def scale (w : ℚ) : ℚ := dyadicScale w (weightBits w)

theorem scale_spec {w : ℚ} (hw : 0 < w) :
    0 < scale w ∧ 1 ≤ (scale w)^2 * w ∧ (scale w)^2 * w < 4 :=
  dyadicScale_spec hw (weightBits_spec w)

/-- Every candidate is an unordered label subset, not an ordered tuple. -/
def candidates (M r : ℕ) : Finset (Finset (Fin M)) := Finset.univ.powersetCard r

@[simp] theorem mem_candidates (s : Finset (Fin M)) (r : ℕ) :
    s ∈ candidates M r ↔ s.card = r := by simp [candidates]

@[simp] theorem candidates_card (M r : ℕ) :
    (candidates M r).card = M.choose r := by simp [candidates]

/-- Canonical ordering of the labels in a candidate. -/
def label (s : Finset (Fin M)) : Fin s.card ↪o Fin M := s.orderEmbOfFin rfl

@[simp] theorem label_mem (s : Finset (Fin M)) (i : Fin s.card) : label s i ∈ s :=
  Finset.orderEmbOfFin_mem s rfl i

theorem label_image (s : Finset (Fin M)) : Finset.univ.image (label s) = s :=
  Finset.image_orderEmbOfFin_univ s rfl

def columns (u : Fin M → Fin p → ℚ) (s : Finset (Fin M)) :
    Matrix (Fin p) (Fin s.card) ℚ := fun i j => u (label s j) i

def independent (u : Fin M → Fin p → ℚ) (s : Finset (Fin M)) : Prop :=
  ((columns u s)ᵀ * columns u s).det ≠ 0

instance (u : Fin M → Fin p → ℚ) (s : Finset (Fin M)) :
    Decidable (independent u s) := inferInstanceAs (Decidable (_ ≠ (0 : ℚ)))

/-- The exact rational Gram determinant is the independence test. -/
theorem independent_iff (u : Fin M → Fin p → ℚ) (s : Finset (Fin M)) :
    independent u s ↔ Function.Injective (columns u s).mulVec := by
  constructor
  · intro h x y hxy
    apply (Matrix.mulVec_injective_iff_isUnit.mpr
      ((Matrix.isUnit_iff_isUnit_det _).mpr (isUnit_iff_ne_zero.mpr h)))
    simp only [← Matrix.mulVec_mulVec, hxy]
  · intro h
    exact isUnit_iff_ne_zero.mp ((Matrix.isUnit_iff_isUnit_det _).mp (gram_isUnit _ h))

def trials (u : Fin M → Fin p → ℚ) (r : ℕ) : Finset (Finset (Fin M)) :=
  (candidates M r).filter (independent u)

@[simp] theorem mem_trials (u : Fin M → Fin p → ℚ) (r : ℕ) (s : Finset (Fin M)) :
    s ∈ trials u r ↔ s.card = r ∧ independent u s := by simp [trials]

theorem trial_count (u : Fin M → Fin p → ℚ) (r : ℕ) :
    (trials u r).card ≤ M.choose r := by
  rw [← candidates_card]
  exact Finset.card_filter_le _ _

def scales (w : Fin M → ℚ) (s : Finset (Fin M)) : Fin s.card → ℚ :=
  fun i => scale (w (label s i))

def transform (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (s : Finset (Fin M)) :=
  normalizer (columns u s) (scales w s)

def restore (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (s : Finset (Fin M)) :=
  reconstructor (columns u s) (scales w s)

/-- Exact original-atom range and diagonal magnitude tests. -/
def acceptsAtom (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) (Q : Matrix (Fin p) (Fin p) ℚ) : Prop :=
  rangeProjector (columns u s) * Q = Q ∧
    ∀ i, (transform u w s * Q * (transform u w s)ᵀ) i i ≤ 4 * p

instance (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) (Q : Matrix (Fin p) (Fin p) ℚ) :
    Decidable (acceptsAtom u w s Q) := inferInstanceAs (Decidable (_ ∧ _))

/-- Prior-owned columns do not force an atom; repeated owners are counted once. -/
def forcedOwners (owner : Fin M → Option (Fin m)) (s : Finset (Fin M)) : Finset (Fin m) :=
  s.biUnion (fun j => (owner j).toFinset)

theorem forcedOwners_card (owner : Fin M → Option (Fin m)) (s : Finset (Fin M)) :
    (forcedOwners owner s).card ≤ s.card := by
  unfold forcedOwners
  apply Finset.card_biUnion_le.trans
  calc
    ∑ j ∈ s, (owner j).toFinset.card ≤ ∑ _j ∈ s, 1 := by
      apply Finset.sum_le_sum
      intro j _
      cases owner j <;> simp
    _ = s.card := by simp

@[simp] theorem mem_forcedOwners (owner : Fin M → Option (Fin m))
    (s : Finset (Fin M)) (a : Fin m) :
    a ∈ forcedOwners owner s ↔ ∃ j ∈ s, owner j = some a := by
  simp [forcedOwners]

/-- Acceptance of a selected set includes the prior and every selected atom,
plus the owners needed for the identity floor. -/
def acceptsSelection (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (owner : Fin M → Option (Fin m)) (s : Finset (Fin M))
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (S : Finset (Fin m)) : Prop :=
  forcedOwners owner s ⊆ S ∧ acceptsAtom u w s (A none) ∧
    ∀ a ∈ S, acceptsAtom u w s (A (some a))

theorem accepted_owner (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (owner : Fin M → Option (Fin m)) (s : Finset (Fin M))
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (S : Finset (Fin m))
    (h : acceptsSelection u w owner s A S) (j : Fin M) (hj : j ∈ s) :
    owner j = none ∨ ∃ a ∈ S, owner j = some a := by
  cases he : owner j with
  | none => exact Or.inl rfl
  | some a => exact Or.inr ⟨a,h.1 ((mem_forcedOwners owner s a).mpr ⟨j,hj,he⟩),rfl⟩

theorem reconstruct_accepted (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (hw : ∀ j, 0 < w j) (s : Finset (Fin M))
    (Q : Matrix (Fin p) (Fin p) ℚ) (hQ : Qᵀ = Q) (h : acceptsAtom u w s Q) :
    restore u w s * (transform u w s * Q * (transform u w s)ᵀ) *
      (restore u w s)ᵀ = Q :=
  reconstruct_retained _ _ (fun i => (scale_spec (hw (label s i))).1.ne') Q hQ h.1

/-- Executable trial coordinates; equality to the semantic inverse is proved below. -/
def transformCode (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (s : Finset (Fin M)) :=
  normalizerProducer (columns u s) (scales w s)

def restoreCode (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ) (s : Finset (Fin M)) :=
  reconstructorProducer (columns u s) (scales w s)

@[simp] theorem transformCode_eq (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) : transformCode u w s = transform u w s :=
  normalizerProducer_eq _ _

@[simp] theorem restoreCode_eq (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) : restoreCode u w s = restore u w s := rfl

def acceptsAtomCode (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) (Q : Matrix (Fin p) (Fin p) ℚ) : Prop :=
  rangeProjectorProducer (columns u s) * Q = Q ∧
    ∀ i, (transformCode u w s * Q * (transformCode u w s)ᵀ) i i ≤ 4 * p

instance (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) (Q : Matrix (Fin p) (Fin p) ℚ) :
    Decidable (acceptsAtomCode u w s Q) := inferInstanceAs (Decidable (_ ∧ _))

@[simp] theorem acceptsAtomCode_iff (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (s : Finset (Fin M)) (Q : Matrix (Fin p) (Fin p) ℚ) :
    acceptsAtomCode u w s Q ↔ acceptsAtom u w s Q := by
  simp only [acceptsAtomCode,acceptsAtom,rangeProjectorProducer_eq,transformCode_eq]

def acceptsSelectionCode (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (owner : Fin M → Option (Fin m)) (s : Finset (Fin M))
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (S : Finset (Fin m)) : Prop :=
  forcedOwners owner s ⊆ S ∧ acceptsAtomCode u w s (A none) ∧
    ∀ a ∈ S, acceptsAtomCode u w s (A (some a))

instance (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (owner : Fin M → Option (Fin m)) (s : Finset (Fin M))
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (S : Finset (Fin m)) :
    Decidable (acceptsSelectionCode u w owner s A S) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

@[simp] theorem acceptsSelectionCode_iff (u : Fin M → Fin p → ℚ) (w : Fin M → ℚ)
    (owner : Fin M → Option (Fin m)) (s : Finset (Fin M))
    (A : Option (Fin m) → Matrix (Fin p) (Fin p) ℚ) (S : Finset (Fin m)) :
    acceptsSelectionCode u w owner s A S ↔ acceptsSelection u w owner s A S := by
  simp only [acceptsSelectionCode,acceptsSelection,acceptsAtomCode_iff]

end NormalizationTrials
end
end DAGSpectral
