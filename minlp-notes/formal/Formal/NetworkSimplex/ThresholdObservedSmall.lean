import Formal.NetworkSimplex.ThresholdObservedReal
import Formal.NetworkSimplex.Results
import Formal.NetworkSimplex.ThresholdSmallDescription

/-! Explicit observed-label zero-, one-, and five-test corollaries. -/
namespace NetworkSimplex.Chain.ReductionData
open scoped BigOperators
noncomputable section
variable {m L : ℕ}

def castDimension {a b : ℕ} (h : a = b) (D : ReductionData a (Fin L)) :
    ReductionData b (Fin L) := h ▸ D

theorem castDimension_hull {a b : ℕ} (h : a = b) (D : ReductionData a (Fin L)) :
    (D.castDimension h).graphPoint ∈ convexHull ℝ (D.castDimension h).graph ↔
      D.graphPoint ∈ convexHull ℝ D.graph := by cases h; rfl

theorem castDimension_residual {a b : ℕ} (h : a = b) (D : ReductionData a (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    (∀ i, (D.castDimension h).c i 0 = .neither) ∧
      (D.castDimension h).observedH 0 = false := by cases h; exact ⟨hc,hh⟩

/-- The compressed instance with exactly two observed labels is decided by the
five displayed tests, alongside original-simplex, domain and zero-row checks. -/
theorem observed_two_hull_iff_five_tests (D : ReductionData m (Fin L))
    (J : Finset (Fin m)) (hJ : D.CoversObservations J) (ha : J.card = 2) :
    let C := (D.compressObserved J).castDimension ha
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      Simplex D.weights ∧ C.OriginalDomain ∧ 0 ≤ C.grouped (.subset ∅) ∧ C.twoTests := by
  dsimp only
  have hc := castDimension_residual ha (D.compressObserved J)
    (fun _ => rfl) rfl
  rw [D.compressObserved_hull_iff J hJ,
    ← castDimension_hull ha (D.compressObserved J),
    mem_hull_iff_five_tests _ hc.1 hc.2]

/-- One scalar interval comparison is sufficient in dimension one. -/
def oneTest (D : ReductionData 1 (Fin L)) : Prop :=
  max (-D.grouped (.negativeSingleton 0)) (-D.grouped .negativeTotal) ≤
    D.grouped (.subset {0})

theorem one_test_iff_profile (D : ReductionData 1 (Fin L)) :
    (0 ≤ D.grouped (.subset ∅) ∧ D.oneTest) ↔ ∃ x, D.ReducedProfile x := by
  constructor
  · rintro ⟨hz,ht⟩
    refine ⟨fun _ => max (-D.grouped (.negativeSingleton 0))
      (-D.grouped .negativeTotal), (D.grouped_iff_reducedProfile _).mp ?_⟩
    intro n
    cases n with
    | negativeSingleton j =>
      have hj : j = 0 := Subsingleton.elim _ _
      subst j
      change -max _ _ ≤ _
      have h := le_max_left (-D.grouped (.negativeSingleton 0)) (-D.grouped .negativeTotal)
      linarith
    | negativeTotal =>
      simp only [ProfileNormal.value, Fin.sum_univ_one]
      have h := le_max_right (-D.grouped (.negativeSingleton 0)) (-D.grouped .negativeTotal)
      linarith
    | subset s =>
      have hs : s = ∅ ∨ s = {0} := by revert s; decide
      rcases hs with rfl | rfl
      · simpa [ProfileNormal.value] using hz
      · simpa only [ProfileNormal.value, Finset.sum_singleton, oneTest] using ht
  · rintro ⟨x,hx⟩
    have hg := (D.grouped_iff_reducedProfile x).mpr hx
    have hzero := hg (.subset ∅)
    have hu := hg (.subset {0})
    have hl := hg (.negativeSingleton 0)
    have ht := hg .negativeTotal
    simp only [ProfileNormal.value, Finset.sum_empty, Finset.sum_singleton,
      Fin.sum_univ_one] at hzero hu hl ht
    refine ⟨hzero, max_le ?_ ?_⟩ <;> linarith

theorem observed_one_hull_iff_one_test (D : ReductionData m (Fin L))
    (J : Finset (Fin m)) (hJ : D.CoversObservations J) (ha : J.card = 1) :
    let C := (D.compressObserved J).castDimension ha
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      Simplex D.weights ∧ C.OriginalDomain ∧ 0 ≤ C.grouped (.subset ∅) ∧ C.oneTest := by
  dsimp only
  have hc := castDimension_residual ha (D.compressObserved J)
    (fun _ => rfl) rfl
  rw [D.compressObserved_hull_iff J hJ,
    ← castDimension_hull ha (D.compressObserved J), mem_hull_iff,
    exists_fullProfile_iff_rows _ hc.1 hc.2]
  have hr := one_test_iff_profile ((D.compressObserved J).castDimension ha)
  have he : (∃ x, ∀ r, (((D.compressObserved J).castDimension ha).rowNormal r).value x ≤
      ((D.compressObserved J).castDimension ha).rowRhs r) ↔
      ∃ x, ((D.compressObserved J).castDimension ha).ReducedProfile x :=
    exists_congr fun x => rows_iff_reducedProfile _ x
  rw [he, ← hr]

/-- With no observed labels, domain and zero-normal rows suffice; there are no
positive circuit comparisons in a nonzero profile dimension. -/
theorem observed_zero_hull_iff_no_tests (D : ReductionData m (Fin L))
    (J : Finset (Fin m)) (hJ : D.CoversObservations J) (ha : J.card = 0) :
    let C := (D.compressObserved J).castDimension ha
    D.graphPoint ∈ convexHull ℝ D.graph ↔
      Simplex D.weights ∧ C.OriginalDomain ∧
        ∀ r, 0 ≤ C.rowRhs r := by
  dsimp only
  have hc := castDimension_residual ha (D.compressObserved J)
    (fun _ => rfl) rfl
  rw [D.compressObserved_hull_iff J hJ,
    ← castDimension_hull ha (D.compressObserved J)]
  apply and_congr_right
  intro _
  have hz (r : ProfileRow 0 (Fin L)) :
      Threshold.normalVector (((D.compressObserved J).castDimension ha).rowNormal r) = 0 :=
    funext fun j => Fin.elim0 j
  simpa only [hz, true_implies] using
    Threshold.zero_mem_hull_iff_source_tests _ hc.1 hc.2

/-- With no structural observations the original chain hull is literally the
flow/simplex product; the zero-label implementation needs no profile elimination. -/
theorem observed_zero_hull_iff_flow_simplex (D : ReductionData m (Fin L))
    (J : Finset (Fin m)) (hJ : D.CoversObservations J) (ha : J.card = 0) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ Simplex D.weights ∧
      Flow (incidence L) (demand L) (fun _ => 1) 1 (pack D.xa D.xb D.xh) := by
  constructor
  · intro h
    have hd := (D.mem_hull_iff.mp h).1
    exact ⟨hd.1, hd.2.1⟩
  · rintro ⟨hw,hf⟩
    apply subset_convexHull
    refine ⟨hw,hf,?_⟩
    intro o
    have hz : J = ∅ := Finset.card_eq_zero.mp ha
    have hc : ∀ i k, D.c i k = .neither := by
      intro i k
      refine Fin.cases (hJ.1 i) (fun j => (hJ.2.2 j (by simp [hz])).1 i) k
    have hh : ∀ k, D.observedH k = false := by
      intro k
      refine Fin.cases hJ.2.1 (fun j => (hJ.2.2 j (by simp [hz])).2) k
    rcases o with ⟨⟨arc,k⟩,hs⟩
    rcases arc with ⟨i,flag⟩ | h
    · cases flag <;> simp [Selected, hc, observesA, observesB] at hs
    · simp [Selected, hh] at hs

/-- The preceding three actual hull criteria cover every `a ≤ 2` instance. -/
theorem observed_at_most_two_cases (J : Finset (Fin m)) (ha : J.card ≤ 2) :
    J.card = 0 ∨ J.card = 1 ∨ J.card = 2 := by omega

end
end NetworkSimplex.Chain.ReductionData
