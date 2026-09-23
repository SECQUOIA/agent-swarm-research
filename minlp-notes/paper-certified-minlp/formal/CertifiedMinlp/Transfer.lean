import CertifiedMinlp.SafeCuts

/-! Objective-preserving relaxation, epigraph construction, incumbent cutoffs,
and primal completion. These are semantic results, not parser verification. -/
namespace CertifiedMinlp

/-- A lower bound is deliberately pointwise, including empty feasible sets. -/
def LowerBoundOn {X : Type*} (F : Set X) (f : X → ℝ) (β : ℝ) : Prop :=
  ∀ x ∈ F, β ≤ f x

theorem objective_preserving_transfer {X Y : Type*} (F : Set X) (M : Set Y)
    (f : X → ℝ) (objective : Y → ℝ) (E : X → Y) (β : ℝ)
    (hembed : ∀ x ∈ F, E x ∈ M)
    (hobjective : ∀ x ∈ F, objective (E x) = f x)
    (hbound : LowerBoundOn M objective β) : LowerBoundOn F f β := by
  intro x hx
  rw [← hobjective x hx]
  exact hbound (E x) (hembed x hx)

theorem infeasible_master_transfer {X Y : Type*} (F : Set X) (M : Set Y)
    (E : X → Y) (hembed : ∀ x ∈ F, E x ∈ M) (hempty : M = ∅) : F = ∅ := by
  apply Set.eq_empty_iff_forall_notMem.mpr
  intro x hx
  have h := hembed x hx
  rw [hempty] at h
  exact h

/-- The master retains the base feasible superset and all supplied valid cuts.
The graph point (x,h(x)) proves the epigraph extension constructively. -/
def epigraphMaster {X K : Type*} (base : Set X) (cuts : K → X × ℝ → ℝ) :
    Set (X × ℝ) := {y | y.1 ∈ base ∧ ∀ k, cuts k y ≤ 0}

theorem epigraph_graph_feasible {X K : Type*} (F base : Set X) (h : X → ℝ)
    (cuts : K → X × ℝ → ℝ) (hbase : F ⊆ base)
    (hcuts : ∀ k x t, x ∈ F → h x ≤ t → cuts k (x, t) ≤ 0) :
    ∀ x ∈ F, (x, h x) ∈ epigraphMaster base cuts := by
  intro x hx
  exact ⟨hbase hx, fun k => hcuts k x (h x) hx le_rfl⟩

theorem epigraph_bound_transfer {X K : Type*} (F base : Set X) (h : X → ℝ)
    (cuts : K → X × ℝ → ℝ) (β : ℝ) (hbase : F ⊆ base)
    (hcuts : ∀ k x t, x ∈ F → h x ≤ t → cuts k (x, t) ≤ 0)
    (hbound : LowerBoundOn (epigraphMaster base cuts) Prod.snd β) :
    LowerBoundOn F h β := by
  exact objective_preserving_transfer F (epigraphMaster base cuts) h Prod.snd
    (fun x => (x, h x)) β (epigraph_graph_feasible F base h cuts hbase hcuts)
    (fun _ _ => rfl) hbound

/-- An underestimator of an epigraph row is a valid epigraph-master cut. -/
theorem epigraph_cut_of_underestimator {X : Type*} (F : Set X) (h : X → ℝ)
    (cut : X × ℝ → ℝ)
    (hunder : ∀ x ∈ F, ∀ t, cut (x, t) ≤ h x - t) :
    ∀ x t, x ∈ F → h x ≤ t → cut (x, t) ≤ 0 := by
  intro x t hx ht
  exact le_trans (hunder x hx t) (sub_nonpos.mpr ht)

theorem signed_min_bound {X : Type*} (F : Set X) (f : X → ℝ) (β : ℝ)
    (h : LowerBoundOn F (fun x => (1 : ℝ) * f x) β) : LowerBoundOn F f β := by
  simpa only [one_mul] using h

theorem signed_max_bound {X : Type*} (F : Set X) (f : X → ℝ) (β : ℝ)
    (h : LowerBoundOn F (fun x => (-1 : ℝ) * f x) β) :
    ∀ x ∈ F, f x ≤ -β := by
  intro x hx
  have hb := h x hx
  linarith

/-- A checked feasible incumbent belongs to its own weak cutoff. A bound on
that restricted set therefore lifts to every feasible point without attainment. -/
theorem incumbent_cutoff_lifting {Y : Type*} (M : Set Y) (objective : Y → ℝ)
    (incumbent : Y) (β : ℝ) (hinc : incumbent ∈ M)
    (hrestricted : ∀ y ∈ M, objective y ≤ objective incumbent → β ≤ objective y) :
    LowerBoundOn M objective β := by
  have hb : β ≤ objective incumbent := hrestricted incumbent hinc le_rfl
  intro y hy
  by_cases h : objective y ≤ objective incumbent
  · exact hrestricted y hy h
  · exact le_trans hb (le_of_lt (lt_of_not_ge h))

/-- Pointwise gap and matching-witness results do not require infima. -/
theorem primal_gap {X : Type*} (F : Set X) (f : X → ℝ) (β U : ℝ)
    (witness : X) (hlower : LowerBoundOn F f β) (hw : witness ∈ F)
    (hupper : f witness ≤ U) :
    β ≤ f witness ∧ ∀ x ∈ F, f witness - f x ≤ U - β := by
  exact ⟨hlower witness hw, fun x hx => sub_le_sub hupper (hlower x hx)⟩

theorem matching_primal_attains {X : Type*} (F : Set X) (f : X → ℝ) (β : ℝ)
    (witness : X) (hlower : LowerBoundOn F f β) (hw : witness ∈ F)
    (hupper : f witness ≤ β) :
    f witness = β ∧ ∀ x ∈ F, f witness ≤ f x := by
  have heq := le_antisymm hupper (hlower witness hw)
  exact ⟨heq, fun x hx => heq ▸ hlower x hx⟩

/-- With an actual feasible witness, the real infimum is well-defined because
of the certified finite lower bound. -/
theorem primal_infimum_bounds {X : Type*} (F : Set X) (f : X → ℝ) (β U : ℝ)
    (witness : X) (hlower : LowerBoundOn F f β) (hw : witness ∈ F)
    (hupper : f witness ≤ U) :
    β ≤ sInf (f '' F) ∧ sInf (f '' F) ≤ f witness ∧
      0 ≤ f witness - sInf (f '' F) ∧ f witness - sInf (f '' F) ≤ U - β := by
  have hne : (f '' F).Nonempty := ⟨f witness, ⟨witness, hw, rfl⟩⟩
  have hl : ∀ y ∈ f '' F, β ≤ y := by
    rintro y ⟨x, hx, rfl⟩
    exact hlower x hx
  have hbdd : BddBelow (f '' F) := ⟨β, hl⟩
  have hβ : β ≤ sInf (f '' F) := le_csInf hne hl
  have hw' : sInf (f '' F) ≤ f witness := csInf_le hbdd ⟨witness, hw, rfl⟩
  exact ⟨hβ, hw', sub_nonneg.mpr hw', sub_le_sub hupper hβ⟩

end CertifiedMinlp
