import Mathlib

/-! Primitive interval hulls and their monotonicity, without a solver oracle. -/
namespace FBBT

structure Box (ι : Type*) where
  lower : ι → ℝ
  upper : ι → ℝ

namespace Box

def carrier {ι : Type*} (B : Box ι) : Set (ι → ℝ) :=
  {x | ∀ i, B.lower i ≤ x i ∧ x i ≤ B.upper i}

def unit (ι : Type*) : Box ι := ⟨fun _ => 0, fun _ => 1⟩

/-- The smallest coordinate interval box containing the constrained points. -/
def IsHull {ι : Type*} (S : Set (ι → ℝ)) (B : Box ι) : Prop :=
  S ⊆ B.carrier ∧ ∀ C : Box ι, S ⊆ C.carrier → B.carrier ⊆ C.carrier

noncomputable def hull {ι : Type*} (S : Set (ι → ℝ)) : Box ι :=
  ⟨fun i => sInf ((fun x => x i) '' S), fun i => sSup ((fun x => x i) '' S)⟩

theorem hull_isHull {ι : Type*} {S : Set (ι → ℝ)} (hS : S.Nonempty)
    (B : Box ι) (hB : S ⊆ B.carrier) : IsHull S (hull S) := by
  have hn (i : ι) : ((fun x => x i) '' S).Nonempty := hS.image _
  have hlo (i : ι) : BddBelow ((fun x => x i) '' S) := by
    refine ⟨B.lower i, ?_⟩
    rintro _ ⟨x, hx, rfl⟩
    exact (hB hx i).1
  have hhi (i : ι) : BddAbove ((fun x => x i) '' S) := by
    refine ⟨B.upper i, ?_⟩
    rintro _ ⟨x, hx, rfl⟩
    exact (hB hx i).2
  constructor
  · intro x hx i
    exact ⟨csInf_le (hlo i) ⟨x, hx, rfl⟩, le_csSup (hhi i) ⟨x, hx, rfl⟩⟩
  · intro C hC x hx i
    have hl : C.lower i ≤ sInf ((fun x => x i) '' S) := by
      apply le_csInf (hn i)
      rintro _ ⟨y, hy, rfl⟩
      exact (hC hy i).1
    have hu : sSup ((fun x => x i) '' S) ≤ C.upper i := by
      apply csSup_le (hn i)
      rintro _ ⟨y, hy, rfl⟩
      exact (hC hy i).2
    exact ⟨hl.trans (hx i).1, (hx i).2.trans hu⟩

theorem hull_mono {ι : Type*} {S T : Set (ι → ℝ)} {B C : Box ι}
    (hB : IsHull S B) (hC : IsHull T C) (hST : S ⊆ T) : B.carrier ⊆ C.carrier :=
  hB.2 C (hST.trans hC.1)

theorem lower_mem {ι : Type*} {B : Box ι} (hB : B.carrier.Nonempty) :
    B.lower ∈ B.carrier := by
  obtain ⟨x, hx⟩ := hB
  exact fun i => ⟨le_rfl, (hx i).1.trans (hx i).2⟩

theorem upper_mem {ι : Type*} {B : Box ι} (hB : B.carrier.Nonempty) :
    B.upper ∈ B.carrier := by
  obtain ⟨x, hx⟩ := hB
  exact fun i => ⟨(hx i).1.trans (hx i).2, le_rfl⟩

theorem lower_mono {ι : Type*} {B C : Box ι}
    (hBC : B.carrier ⊆ C.carrier) (hB : B.carrier.Nonempty) (i : ι) :
    C.lower i ≤ B.lower i := (hBC (lower_mem hB) i).1

/-- A primitive update is the actual hull of one equation intersected with the box. -/
def Step {ι κ : Type*} (E : κ → Set (ι → ℝ)) (a : κ) (B C : Box ι) : Prop :=
  IsHull (B.carrier ∩ E a) C

theorem step_contracts {ι κ : Type*} {E : κ → Set (ι → ℝ)} {a : κ} {B C : Box ι}
    (h : Step E a B C) : C.carrier ⊆ B.carrier := h.2 B Set.inter_subset_left

theorem step_preserves {ι κ : Type*} {E : κ → Set (ι → ℝ)} {a : κ} {B C : Box ι}
    (h : Step E a B C) {x : ι → ℝ} (hx : x ∈ B.carrier) (he : x ∈ E a) :
    x ∈ C.carrier := h.1 ⟨hx, he⟩

theorem step_mono {ι κ : Type*} {E : κ → Set (ι → ℝ)} {a : κ} {B C D F : Box ι}
    (hB : Step E a B C) (hD : Step E a D F) (hBD : B.carrier ⊆ D.carrier) :
    C.carrier ⊆ F.carrier := hull_mono hB hD (Set.inter_subset_inter_left _ hBD)

/-- Exact real arithmetic supplies a canonical primitive contractor. -/
noncomputable def contract {ι κ : Type*} (E : κ → Set (ι → ℝ)) (a : κ) (B : Box ι) : Box ι :=
  hull (B.carrier ∩ E a)

theorem contract_step {ι κ : Type*} (E : κ → Set (ι → ℝ)) (a : κ) (B : Box ι)
    (h : (B.carrier ∩ E a).Nonempty) : Step E a B (contract E a B) :=
  hull_isHull h B Set.inter_subset_left

/-- A run applies exactly one primitive hull at each schedule position. -/
structure Run {ι κ : Type*} (E : κ → Set (ι → ℝ)) (start : Box ι)
    (schedule : ℕ → κ) (states : ℕ → Box ι) : Prop where
  initial : states 0 = start
  step : ∀ t, Step E (schedule t) (states t) (states (t + 1))

theorem Run.preserves {ι κ : Type*} {E : κ → Set (ι → ℝ)} {start : Box ι}
    {schedule : ℕ → κ} {states : ℕ → Box ι} (h : Run E start schedule states)
    {x : ι → ℝ} (hx : x ∈ start.carrier) (he : ∀ a, x ∈ E a) :
    ∀ t, x ∈ (states t).carrier := by
  intro t
  induction t with
  | zero => simpa [h.initial] using hx
  | succ t ih => exact step_preserves (h.step t) ih (he _)

theorem Run.comparison {ι κ : Type*} {E : κ → Set (ι → ℝ)} {B C : Box ι}
    {schedule : ℕ → κ} {xs ys : ℕ → Box ι}
    (hx : Run E B schedule xs) (hy : Run E C schedule ys) (hBC : B.carrier ⊆ C.carrier) :
    ∀ t, (xs t).carrier ⊆ (ys t).carrier := by
  intro t
  induction t with
  | zero => simpa [hx.initial, hy.initial] using hBC
  | succ t ih => exact step_mono (hx.step t) (hy.step t) ih

/-- Canonical exact primitive updates exist for every schedule. -/
noncomputable def iterate {ι κ : Type*} (E : κ → Set (ι → ℝ)) (start : Box ι)
    (schedule : ℕ → κ) : ℕ → Box ι
  | 0 => start
  | t + 1 => contract E (schedule t) (iterate E start schedule t)

theorem iterate_preserves {ι κ : Type*} (E : κ → Set (ι → ℝ)) (start : Box ι)
    (schedule : ℕ → κ) {x : ι → ℝ} (hx : x ∈ start.carrier) (he : ∀ a, x ∈ E a) :
    ∀ t, x ∈ (iterate E start schedule t).carrier := by
  intro t
  induction t with
  | zero => exact hx
  | succ t ih =>
    exact (contract_step E (schedule t) _ ⟨x, ih, he _⟩).1 ⟨ih, he _⟩

theorem iterate_run {ι κ : Type*} (E : κ → Set (ι → ℝ)) (start : Box ι)
    (schedule : ℕ → κ) {x : ι → ℝ} (hx : x ∈ start.carrier) (he : ∀ a, x ∈ E a) :
    Run E start schedule (iterate E start schedule) := by
  refine ⟨rfl, fun t => ?_⟩
  exact contract_step E _ _ ⟨x, iterate_preserves E start schedule hx he t, he _⟩

theorem Run.lower_monotone {ι κ : Type*} {E : κ → Set (ι → ℝ)} {start : Box ι}
    {schedule : ℕ → κ} {states : ℕ → Box ι} (h : Run E start schedule states)
    {x : ι → ℝ} (hx : x ∈ start.carrier) (he : ∀ a, x ∈ E a) (i : ι) :
    Monotone (fun t => (states t).lower i) := by
  apply monotone_nat_of_le_succ
  intro t
  exact lower_mono (step_contracts (h.step t)) ⟨x, h.preserves hx he (t + 1)⟩ i

/-- Any forward bound valid on a single constraint's intersection is retained
by its exact interval hull. -/
theorem forward_lower {ι κ : Type*}
    {E : κ → Set (ι → ℝ)} {a : κ} {B C : Box ι} (h : Step E a B C)
    (hC : C.carrier.Nonempty) (i : ι) (v : ℝ)
    (hv : ∀ x ∈ B.carrier ∩ E a, v ≤ x i) : v ≤ C.lower i := by
  classical
  let D : Box ι := ⟨Function.update B.lower i (max (B.lower i) v), B.upper⟩
  have hD : B.carrier ∩ E a ⊆ D.carrier := by
    intro x hx j
    by_cases hji : j = i
    · subst j
      constructor
      · simpa [D] using (max_le (hx.1 i).1 (hv x hx))
      · exact (hx.1 i).2
    · simpa [D, Function.update_of_ne hji] using hx.1 j
  have hh := h.2 D hD (lower_mem hC) i
  have hi : max (B.lower i) v ≤ C.lower i := by
    simpa [D] using hh.1
  exact (le_max_right _ _).trans hi

theorem upper_mono {ι : Type*} {B C : Box ι}
    (hBC : B.carrier ⊆ C.carrier) (hB : B.carrier.Nonempty) (i : ι) :
    B.upper i ≤ C.upper i := (hBC (upper_mem hB) i).2

theorem Run.upper_antitone {ι κ : Type*} {E : κ → Set (ι → ℝ)} {start : Box ι}
    {schedule : ℕ → κ} {states : ℕ → Box ι} (h : Run E start schedule states)
    {x : ι → ℝ} (hx : x ∈ start.carrier) (he : ∀ a, x ∈ E a) (i : ι) :
    Antitone (fun t => (states t).upper i) := by
  apply antitone_nat_of_succ_le
  intro t
  exact upper_mono (step_contracts (h.step t)) ⟨x, h.preserves hx he (t + 1)⟩ i

/-- Forward upper bounds are also enforced by the exact simultaneous hull. -/
theorem forward_upper {ι κ : Type*}
    {E : κ → Set (ι → ℝ)} {a : κ} {B C : Box ι} (h : Step E a B C)
    (hC : C.carrier.Nonempty) (i : ι) (v : ℝ)
    (hv : ∀ x ∈ B.carrier ∩ E a, x i ≤ v) : C.upper i ≤ v := by
  classical
  let D : Box ι := ⟨B.lower, Function.update B.upper i (min (B.upper i) v)⟩
  have hD : B.carrier ∩ E a ⊆ D.carrier := by
    intro x hx j
    by_cases hji : j = i
    · subst j
      constructor
      · exact (hx.1 i).1
      · simpa [D] using (le_min (hx.1 i).2 (hv x hx))
    · simpa [D, Function.update_of_ne hji] using hx.1 j
  have hh := h.2 D hD (upper_mem hC) i
  have hi : C.upper i ≤ min (B.upper i) v := by
    simpa [D] using hh.2
  exact hi.trans (min_le_right _ _)

end Box
end FBBT
