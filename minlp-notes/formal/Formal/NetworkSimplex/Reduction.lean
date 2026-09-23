import Formal.NetworkSimplex.Profile

/-! Residual profile elimination and exact grouping of repeated linear rows. -/

namespace NetworkSimplex

noncomputable section

/-- Restore the unobserved state from the explicit profile and its total. -/
def restoreProfile {m : ℕ} (t : ℝ) (x : Fin m → ℝ) : Fin (m + 1) → ℝ :=
  Fin.cons (t - ∑ j, x j) x

@[simp] theorem restoreProfile_zero {m : ℕ} (t : ℝ) (x : Fin m → ℝ) :
    restoreProfile t x 0 = t - ∑ j, x j := rfl

@[simp] theorem restoreProfile_succ {m : ℕ} (t : ℝ) (x : Fin m → ℝ) (j : Fin m) :
    restoreProfile t x j.succ = x j := rfl

@[simp] theorem sum_restoreProfile {m : ℕ} (t : ℝ) (x : Fin m → ℝ) :
    ∑ j, restoreProfile t x j = t := by
  simp [Fin.sum_univ_succ]

/-- Eliminating state zero is a bijection between full profiles of total `t`
and explicit profiles. -/
theorem restoreProfile_eq {m : ℕ} (t : ℝ) (w : Fin (m + 1) → ℝ)
    (h : ∑ j, w j = t) : restoreProfile t (fun j => w j.succ) = w := by
  funext j
  refine Fin.cases ?_ (fun j => ?_) j
  · have hs := h
    rw [Fin.sum_univ_succ] at hs
    simp only [restoreProfile_zero]
    linarith
  · rfl

/-- The residual box bounds become the positive and negative total rows. -/
theorem restoreProfile_bounds_iff {m : ℕ} (t : ℝ) (weights : Fin (m + 1) → ℝ)
    (x : Fin m → ℝ) :
    (∀ j, 0 ≤ restoreProfile t x j ∧ restoreProfile t x j ≤ weights j) ↔
      (∀ j, 0 ≤ x j ∧ x j ≤ weights j.succ) ∧
      (∑ j, x j ≤ t) ∧ -(∑ j, x j) ≤ weights 0 - t := by
  constructor
  · intro h
    refine ⟨fun j => h j.succ, ?_, ?_⟩
    · have := (h 0).1
      simp only [restoreProfile_zero] at this
      linarith
    · have := (h 0).2
      simp only [restoreProfile_zero] at this
      linarith
  · rintro ⟨h, hl, hu⟩ j
    refine Fin.cases ?_ (fun j => h j) j
    simp only [restoreProfile_zero]
    constructor <;> linarith

/-- A row not involving the residual state retains its explicit subset normal. -/
theorem sum_restoreProfile_selected {m : ℕ} (t : ℝ) (x : Fin m → ℝ)
    (p : Fin (m + 1) → Prop) [DecidablePred p] (h0 : ¬p 0) :
    (∑ j, if p j then restoreProfile t x j else 0) =
      ∑ j, if p j.succ then x j else 0 := by
  simp [Fin.sum_univ_succ, h0]

/-- An endpoint upper bound uses the complementary explicit-state subset. -/
theorem residual_endpoint_iff {m : ℕ} (t R : ℝ) (x : Fin m → ℝ)
    (p : Fin (m + 1) → Prop) [DecidablePred p] (h0 : p 0) :
    R ≤ (∑ j, if p j then restoreProfile t x j else 0) ↔
      (∑ j, if ¬p j.succ then x j else 0) ≤ t - R := by
  have hs : (∑ j : Fin m, if p j.succ then x j else 0) +
      (∑ j : Fin m, if ¬p j.succ then x j else 0) = ∑ j, x j := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    by_cases h : p j.succ <;> simp [h]
  simp only [Fin.sum_univ_succ, h0, if_true, restoreProfile_zero,
    restoreProfile_succ]
  constructor <;> intro h <;> linarith

/-- Distinct row normals are grouped by the least right-hand side in their
nonempty finite fibers. A zero normal is retained, so its scalar check is not lost. -/
def groupedBound {κ ν : Type*} [Fintype κ] [DecidableEq ν]
    (normal : κ → ν) (rhs : κ → ℝ) (present : Function.Surjective normal) (v : ν) : ℝ :=
  (Finset.univ.filter (fun k => normal k = v)).inf'
    (by obtain ⟨k, hk⟩ := present v; exact ⟨k, by simp [hk]⟩) rhs

theorem groupedBound_iff {κ ν : Type*} [Fintype κ] [DecidableEq ν]
    (normal : κ → ν) (rhs : κ → ℝ) (present : Function.Surjective normal)
    (value : ν → ℝ) :
    (∀ k, value (normal k) ≤ rhs k) ↔
      ∀ v, value v ≤ groupedBound normal rhs present v := by
  constructor
  · intro h v
    rw [groupedBound, Finset.le_inf'_iff]
    intro k hk
    have he : normal k = v := (Finset.mem_filter.mp hk).2
    simpa [he] using h k
  · intro h k
    exact (h (normal k)).trans
      (Finset.inf'_le _ (by simp : k ∈ Finset.univ.filter
        (fun j => normal j = normal k)))

namespace Chain

/-- All gadget rows after elimination of the unobserved state zero. -/
def ReducedGadget {m : ℕ} (c : Fin (m + 1) → StateClass)
    (u v : Fin (m + 1) → ℝ) (t xa : ℝ) (x : Fin m → ℝ) : Prop :=
  (∀ j, c j.succ = .aOnly → u j.succ ≤ x j) ∧
  (∀ j, c j.succ = .bOnly → v j.succ ≤ x j) ∧
  (∀ j, c j.succ = .both → x j = u j.succ + v j.succ) ∧
  (∑ j, if c j.succ = .bOnly then x j else 0) ≤ residual c u v xa ∧
  (∑ j, if observesA (c j.succ) then x j else 0) ≤ t - residual c u v xa

theorem gadget_residual_elimination {m : ℕ} (c : Fin (m + 1) → StateClass)
    (u v : Fin (m + 1) → ℝ) (t xa : ℝ) (x : Fin m → ℝ)
    (hc : c 0 = .neither) :
    GadgetProfile c u v (restoreProfile t x) xa ↔ ReducedGadget c u v t xa x := by
  have ha : (∀ j, c j = .aOnly → u j ≤ restoreProfile t x j) ↔
      ∀ j, c j.succ = .aOnly → u j.succ ≤ x j := by
    rw [Fin.forall_fin_succ]
    simp [hc]
  have hb : (∀ j, c j = .bOnly → v j ≤ restoreProfile t x j) ↔
      ∀ j, c j.succ = .bOnly → v j.succ ≤ x j := by
    rw [Fin.forall_fin_succ]
    simp [hc]
  have ht : (∀ j, c j = .both → restoreProfile t x j = u j + v j) ↔
      ∀ j, c j.succ = .both → x j = u j.succ + v j.succ := by
    rw [Fin.forall_fin_succ]
    simp [hc]
  have hbs : bSum c (restoreProfile t x) =
      ∑ j, if c j.succ = .bOnly then x j else 0 := by
    simp [bSum, Fin.sum_univ_succ, hc]
  have hbu : bSum c (restoreProfile t x) + ∑ j, freeA c (restoreProfile t x) j =
      ∑ j, if ¬observesA (c j) then restoreProfile t x j else 0 := by
    unfold bSum freeA
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    cases c j <;> simp [observesA]
  have hep := residual_endpoint_iff t (residual c u v xa) x
    (fun j => ¬observesA (c j)) (by simp [hc, observesA])
  simp only [not_not] at hep
  unfold GadgetProfile ReducedGadget
  rw [hbu]
  simp only [ha, hb, ht, hbs, hep]

/-- The finite universe of reduced profile row normals, including the zero row. -/
inductive ProfileNormal (m : ℕ) where
  | subset : Finset (Fin m) → ProfileNormal m
  | negativeSingleton : Fin m → ProfileNormal m
  | negativeTotal : ProfileNormal m
  deriving DecidableEq, Fintype

def ProfileNormal.value {m : ℕ} (x : Fin m → ℝ) : ProfileNormal m → ℝ
  | .subset s => ∑ j ∈ s, x j
  | .negativeSingleton j => -x j
  | .negativeTotal => -(∑ j, x j)

inductive ProfileRow (m : ℕ) (I : Type*) where
  | lower : Fin m → ProfileRow m I
  | upper : Fin m → ProfileRow m I
  | totalLower | totalUpper
  | bypassLower : Fin m → ProfileRow m I
  | bypassUpper : Fin m → ProfileRow m I
  | aLower : I → Fin m → ProfileRow m I
  | bLower : I → Fin m → ProfileRow m I
  | bothLower : I → Fin m → ProfileRow m I
  | bothUpper : I → Fin m → ProfileRow m I
  | endpointB : I → ProfileRow m I
  | endpointA : I → ProfileRow m I
  deriving DecidableEq, Fintype

/-- Data needed by the reduced rows; the observations are arbitrary. -/
structure ReductionData (m : ℕ) (I : Type*) where
  c : I → Fin (m + 1) → StateClass
  u : I → Fin (m + 1) → ℝ
  v : I → Fin (m + 1) → ℝ
  weights : Fin (m + 1) → ℝ
  xa : I → ℝ
  xh : ℝ
  observedH : Fin (m + 1) → Bool
  zh : Fin (m + 1) → ℝ

namespace ReductionData

variable {m : ℕ} {I : Type*}

def total (D : ReductionData m I) : ℝ := 1 - D.xh

def rowNormal (D : ReductionData m I) : ProfileRow m I → ProfileNormal m
  | .lower j => .negativeSingleton j
  | .upper j => .subset {j}
  | .totalLower => .negativeTotal
  | .totalUpper => .subset Finset.univ
  | .bypassLower j => if D.observedH j.succ then .negativeSingleton j else .subset ∅
  | .bypassUpper j => if D.observedH j.succ then .subset {j} else .subset ∅
  | .aLower i j => if D.c i j.succ = .aOnly then .negativeSingleton j else .subset ∅
  | .bLower i j => if D.c i j.succ = .bOnly then .negativeSingleton j else .subset ∅
  | .bothLower i j => if D.c i j.succ = .both then .negativeSingleton j else .subset ∅
  | .bothUpper i j => if D.c i j.succ = .both then .subset {j} else .subset ∅
  | .endpointB i => .subset (Finset.univ.filter fun j => D.c i j.succ = .bOnly)
  | .endpointA i => .subset (Finset.univ.filter fun j => observesA (D.c i j.succ))

def rowRhs (D : ReductionData m I) : ProfileRow m I → ℝ
  | .lower _ => 0
  | .upper j => D.weights j.succ
  | .totalLower => D.weights 0 - D.total
  | .totalUpper => D.total
  | .bypassLower j => if D.observedH j.succ then D.zh j.succ - D.weights j.succ else 0
  | .bypassUpper j => if D.observedH j.succ then D.weights j.succ - D.zh j.succ else 0
  | .aLower i j => if D.c i j.succ = .aOnly then -D.u i j.succ else 0
  | .bLower i j => if D.c i j.succ = .bOnly then -D.v i j.succ else 0
  | .bothLower i j => if D.c i j.succ = .both then -(D.u i j.succ + D.v i j.succ) else 0
  | .bothUpper i j => if D.c i j.succ = .both then D.u i j.succ + D.v i j.succ else 0
  | .endpointB i => residual (D.c i) (D.u i) (D.v i) (D.xa i)
  | .endpointA i => D.total - residual (D.c i) (D.u i) (D.v i) (D.xa i)

def ReducedProfile (D : ReductionData m I) (x : Fin m → ℝ) : Prop :=
  (∀ j, 0 ≤ x j ∧ x j ≤ D.weights j.succ) ∧
  (∑ j, x j) ≤ D.total ∧ -(∑ j, x j) ≤ D.weights 0 - D.total ∧
  (∀ j, D.observedH j.succ = true → x j = D.weights j.succ - D.zh j.succ) ∧
  ∀ i, ReducedGadget (D.c i) (D.u i) (D.v i) D.total (D.xa i) x

theorem rows_iff_reducedProfile (D : ReductionData m I) (x : Fin m → ℝ) :
    (∀ r, (D.rowNormal r).value x ≤ D.rowRhs r) ↔ D.ReducedProfile x := by
  constructor
  · intro h
    have hlo (j) := h (.lower j)
    have hup (j) := h (.upper j)
    have htl := h .totalLower
    have htu := h .totalUpper
    simp only [rowNormal, rowRhs, ProfileNormal.value, Finset.sum_singleton,
      neg_nonpos] at hlo hup htl htu
    refine ⟨fun j => ⟨hlo j, hup j⟩, htu, htl, ?_, ?_⟩
    · intro j hj
      have hl := h (.bypassLower j)
      have hu := h (.bypassUpper j)
      simp [rowNormal, rowRhs, ProfileNormal.value, hj] at hl hu
      linarith
    · intro i
      refine ⟨?_, ?_, ?_, ?_, ?_⟩
      · intro j hj
        have hh := h (.aLower i j)
        simpa [rowNormal, rowRhs, ProfileNormal.value, hj] using hh
      · intro j hj
        have hh := h (.bLower i j)
        simpa [rowNormal, rowRhs, ProfileNormal.value, hj] using hh
      · intro j hj
        have hl := h (.bothLower i j)
        have hu := h (.bothUpper i j)
        simp [rowNormal, rowRhs, ProfileNormal.value, hj] at hl hu
        linarith
      · simpa [rowNormal, rowRhs, ProfileNormal.value, Finset.sum_filter] using h (.endpointB i)
      · simpa [rowNormal, rowRhs, ProfileNormal.value, Finset.sum_filter] using h (.endpointA i)
  · rintro ⟨hb, htu, htl, hh, hg⟩ r
    cases r with
    | lower j => simpa [rowNormal, rowRhs, ProfileNormal.value] using (hb j).1
    | upper j => simpa [rowNormal, rowRhs, ProfileNormal.value] using (hb j).2
    | totalLower => exact htl
    | totalUpper => exact htu
    | bypassLower j =>
        by_cases hj : D.observedH j.succ = true
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj, hh j hj]
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | bypassUpper j =>
        by_cases hj : D.observedH j.succ = true
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj, hh j hj]
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | aLower i j =>
        by_cases hj : D.c i j.succ = .aOnly
        · simpa [rowNormal, rowRhs, ProfileNormal.value, hj] using (hg i).1 j hj
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | bLower i j =>
        by_cases hj : D.c i j.succ = .bOnly
        · simpa [rowNormal, rowRhs, ProfileNormal.value, hj] using (hg i).2.1 j hj
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | bothLower i j =>
        by_cases hj : D.c i j.succ = .both
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj, (hg i).2.2.1 j hj]
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | bothUpper i j =>
        by_cases hj : D.c i j.succ = .both
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj, (hg i).2.2.1 j hj]
        · simp [rowNormal, rowRhs, ProfileNormal.value, hj]
    | endpointB i =>
        simpa [rowNormal, rowRhs, ProfileNormal.value, Finset.sum_filter] using (hg i).2.2.2.1
    | endpointA i =>
        simpa [rowNormal, rowRhs, ProfileNormal.value, Finset.sum_filter] using (hg i).2.2.2.2

/-- The complete profile system from the paper, specialized to a residual state zero. -/
def FullProfile (D : ReductionData m I) (w : Fin (m + 1) → ℝ) : Prop :=
  Profile D.c D.u D.v D.weights D.xa D.xh (fun j => D.observedH j = true) D.zh w

/-- Elimination preserves every local observation, endpoint row, and box bound. -/
theorem fullProfile_restore_iff (D : ReductionData m I) (x : Fin m → ℝ)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.FullProfile (restoreProfile D.total x) ↔ D.ReducedProfile x := by
  have hH : (∀ j, D.observedH j = true →
      restoreProfile D.total x j = D.weights j - D.zh j) ↔
      ∀ j, D.observedH j.succ = true → x j = D.weights j.succ - D.zh j.succ := by
    rw [Fin.forall_fin_succ]
    simp [hh]
  have hG : (∀ i, GadgetProfile (D.c i) (D.u i) (D.v i)
      (restoreProfile D.total x) (D.xa i)) ↔
      ∀ i, ReducedGadget (D.c i) (D.u i) (D.v i) D.total (D.xa i) x := by
    exact forall_congr' fun i => gadget_residual_elimination
      (D.c i) (D.u i) (D.v i) D.total (D.xa i) x (hc i)
  unfold FullProfile Profile ReducedProfile
  rw [restoreProfile_bounds_iff, sum_restoreProfile, hH, hG]
  have ht : D.total = 1 - D.xh := rfl
  simp only [ht, true_and, eq_self]
  tauto

/-- The original profile feasibility is exactly feasibility of the finite reduced rows. -/
theorem exists_fullProfile_iff_rows (D : ReductionData m I)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (∃ w, D.FullProfile w) ↔
      ∃ x, ∀ r, (D.rowNormal r).value x ≤ D.rowRhs r := by
  constructor
  · rintro ⟨w, hw⟩
    have hsum : ∑ j, w j = D.total := hw.2.1
    refine ⟨fun j => w j.succ, (rows_iff_reducedProfile D _).mpr ?_⟩
    apply (fullProfile_restore_iff D _ hc hh).mp
    simpa only [restoreProfile_eq D.total w hsum] using hw
  · rintro ⟨x, hx⟩
    exact ⟨restoreProfile D.total x, (fullProfile_restore_iff D x hc hh).mpr
      ((rows_iff_reducedProfile D x).mp hx)⟩

end ReductionData

end Chain

end

end NetworkSimplex
