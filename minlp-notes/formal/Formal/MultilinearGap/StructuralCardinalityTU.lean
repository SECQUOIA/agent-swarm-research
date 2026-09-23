import Formal.MultilinearGap.StructuralCardinality
import Formal.MultilinearGap.StructuralTreewidthTU

/-!
# Binary laws from totally unimodular slab systems

Integer inequalities with a totally unimodular matrix have integral extreme
points. When those inequalities bound the unit cube, every feasible point is
a convex combination of feasible binary points, and hence is the mean of a
law supported on those binary points.
-/

namespace MultilinearGap.TUSlab

open CubicGap Matrix Set
noncomputable section
variable {R I : Type*} [Fintype R] [Fintype I] [DecidableEq R] [DecidableEq I]

/-- The real feasible region of an integer inequality system. -/
def polyhedron (A : Matrix R I ℤ) (b : R → ℤ) : Set (I → ℝ) :=
  {x | ∀ r, (A.map (Int.castRingHom ℝ) *ᵥ x) r ≤ (b r : ℝ)}

/-- Rows tight at a point of the real feasible region. -/
def active (A : Matrix R I ℤ) (b : R → ℤ) (x : I → ℝ) : Finset R :=
  Finset.univ.filter fun r => (A.map (Int.castRingHom ℝ) *ᵥ x) r = (b r : ℝ)

omit [DecidableEq R] [DecidableEq I] in
/-- Vanishing on the tight rows permits perturbations in both directions. -/
theorem exists_symmetric_perturbation {A : Matrix R I ℤ} {b : R → ℤ}
    {x d : I → ℝ} (hx : x ∈ polyhedron A b)
    (hd : ∀ r ∈ active A b x, (A.map (Int.castRingHom ℝ) *ᵥ d) r = 0) :
    ∃ t : ℝ, 0 < t ∧ x + t • d ∈ polyhedron A b ∧
      x - t • d ∈ polyhedron A b := by
  let B := A.map (Int.castRingHom ℝ)
  change ∀ r, (B *ᵥ x) r ≤ (b r : ℝ) at hx
  have he : ∀ᶠ t : ℝ in nhds 0, x + t • d ∈ polyhedron A b := by
    change ∀ᶠ t : ℝ in nhds 0, ∀ r, (B *ᵥ (x + t • d)) r ≤ (b r : ℝ)
    rw [Filter.eventually_all]
    intro r
    by_cases hr : (B *ᵥ x) r = (b r : ℝ)
    · have hz : (B *ᵥ d) r = 0 := hd r (Finset.mem_filter.mpr ⟨Finset.mem_univ r, hr⟩)
      exact Filter.Eventually.of_forall (fun t => by
        simpa [Matrix.mulVec_add, Matrix.mulVec_smul, hz] using hx r)
    · have hlt : (B *ᵥ x) r < (b r : ℝ) := lt_of_le_of_ne (hx r) hr
      have hc : ContinuousAt (fun t : ℝ => (B *ᵥ x) r + t * (B *ᵥ d) r) 0 := by
        fun_prop
      filter_upwards [hc.eventually_lt_const (by simpa using hlt)] with t ht
      simpa [Matrix.mulVec_add, Matrix.mulVec_smul] using ht.le
  obtain ⟨δ, hδ, hh⟩ := Metric.eventually_nhds_iff.mp he
  refine ⟨δ / 2, by positivity, hh ?_, ?_⟩
  · simpa [Real.dist_eq, abs_of_pos hδ] using (show δ / 2 < δ by linarith)
  · have h := hh (y := -(δ / 2)) (by
      simpa [Real.dist_eq, abs_neg, abs_of_pos hδ] using (show δ / 2 < δ by linarith))
    simpa [sub_eq_add_neg, neg_smul] using h

omit [DecidableEq R] [DecidableEq I] in
/-- The active rows have trivial kernel at an extreme feasible point. -/
theorem extreme_kernel_eq_zero {A : Matrix R I ℤ} {b : R → ℤ}
    {x d : I → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ)
    (hd : ∀ r ∈ active A b x, (A.map (Int.castRingHom ℝ) *ᵥ d) r = 0) : d = 0 := by
  obtain ⟨t, ht, hp, hn⟩ := exists_symmetric_perturbation hx.1 hd
  have hseg : x ∈ openSegment ℝ (x + t • d) (x - t • d) := by
    refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
    ext i
    simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have he := hx.2 hp hn hseg
  have htd : t • d = 0 := add_left_cancel (he.trans (add_zero x).symm)
  exact (smul_eq_zero.mp htd).resolve_left (ne_of_gt ht)

omit [DecidableEq R] [DecidableEq I] in
/-- The real matrix of active integer rows is injective at an extreme point. -/
theorem extreme_active_injective {A : Matrix R I ℤ} {b : R → ℤ}
    {x : I → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ) :
    Function.Injective
      ((A.submatrix (fun r : active A b x => r.val) id).map (Int.castRingHom ℝ)).mulVec := by
  intro u v huv
  have hd : u - v = 0 := by
    apply extreme_kernel_eq_zero hx
    intro r hr
    have h := congrFun huv (⟨r, hr⟩ : active A b x)
    change (A.map (Int.castRingHom ℝ) *ᵥ u) r =
      (A.map (Int.castRingHom ℝ) *ᵥ v) r at h
    simpa [Matrix.mulVec_sub] using sub_eq_zero.mpr h
  exact sub_eq_zero.mp hd

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- Finite integer halfspaces form a convex set. -/
theorem polyhedron_convex (A : Matrix R I ℤ) (b : R → ℤ) :
    Convex ℝ (polyhedron A b) := by
  intro x hx y hy p q hp hq hpq r
  simp only [Matrix.mulVec_add, Matrix.mulVec_smul, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  have h := add_le_add (mul_le_mul_of_nonneg_left (hx r) hp)
    (mul_le_mul_of_nonneg_left (hy r) hq)
  simpa [← add_mul, hpq] using h

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- Finite integer halfspaces form a closed set. -/
theorem polyhedron_closed (A : Matrix R I ℤ) (b : R → ℤ) :
    IsClosed (polyhedron A b) := by
  unfold polyhedron
  simp only [Set.ofPred_forall]
  apply isClosed_iInter
  intro r
  apply isClosed_le _ continuous_const
  simp only [Matrix.mulVec, dotProduct]
  fun_prop

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- A feasible region contained in the cube is compact. -/
theorem polyhedron_compact (A : Matrix R I ℤ) (b : R → ℤ)
    (hbox : polyhedron A b ⊆ cube I) : IsCompact (polyhedron A b) := by
  apply (isCompact_pi_infinite (fun _ : I =>
    isCompact_Icc (a := (0 : ℝ)) (b := 1))).of_isClosed_subset (polyhedron_closed A b)
  exact hbox

/-- Binary feasible points of the inequality system. -/
def binaryPoints (A : Matrix R I ℤ) (b : R → ℤ) : Set (I → ℝ) :=
  {x | x ∈ polyhedron A b ∧ ∃ v : Vertex I, x = vertexPoint v}

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- There are only finitely many binary feasible points. -/
theorem binaryPoints_finite (A : Matrix R I ℤ) (b : R → ℤ) :
    (binaryPoints A b).Finite := by
  apply (Set.finite_range (vertexPoint (I := I))).subset
  rintro x ⟨_, v, rfl⟩
  exact Set.mem_range_self v

omit [Fintype R] [DecidableEq R] in
/-- A convex combination of feasible binary points is a law supported on
feasible vertices with the prescribed means. -/
theorem exists_binaryLaw_of_mem_hull {A : Matrix R I ℤ} {b : R → ℤ} {x : I → ℝ}
    (hx : x ∈ convexHull ℝ (binaryPoints A b)) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      ∀ v : Vertex I, μ.weight v ≠ 0 → vertexPoint v ∈ polyhedron A b := by
  classical
  have hrange : Set.range (fun w : {v : Vertex I // vertexPoint v ∈ polyhedron A b} =>
      vertexPoint w.val) = binaryPoints A b := by
    ext z
    constructor
    · rintro ⟨w, rfl⟩
      exact ⟨w.2, w.val, rfl⟩
    · rintro ⟨hz, v, rfl⟩
      exact ⟨⟨v, hz⟩, rfl⟩
  rw [← hrange] at hx
  obtain ⟨μ, hμ⟩ := (Law.mem_convexHull_range_iff _ x).mp hx
  refine ⟨μ.map Subtype.val, fun i => ?_, fun v hv => ?_⟩
  · have h := congrFun hμ i
    simp only [Law.barycenter, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] at h
    rw [Law.expect_map]
    simpa [Law.expect, Function.comp] using h
  · by_contra hns
    refine hv ?_
    simp only [Law.map]
    refine Finset.sum_eq_zero fun w _ => if_neg ?_
    rintro rfl
    exact hns w.2

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- Every extreme point of a TU system with integer bounds is integral. -/
theorem extreme_integral [Finite R] {A : Matrix R I ℤ} {b : R → ℤ}
    (hA : A.IsTotallyUnimodular) {x : I → ℝ}
    (hx : x ∈ (polyhedron A b).extremePoints ℝ) :
    ∃ z : I → ℤ, (fun i => (z i : ℝ)) = x := by
  let := Fintype.ofFinite R
  apply totallyUnimodular_injective_system_descends (Int.castRingHom ℝ)
    Int.cast_injective (hA.submatrix (fun r : active A b x => r.val) id)
    (extreme_active_injective hx) (fun r : active A b x => b r.val)
  ext r
  exact (Finset.mem_filter.mp r.property).2

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- Integral extreme points inside the unit cube are binary feasible points. -/
theorem extreme_mem_binaryPoints [Finite R] {A : Matrix R I ℤ} {b : R → ℤ}
    (hA : A.IsTotallyUnimodular) (hbox : polyhedron A b ⊆ cube I)
    {x : I → ℝ} (hx : x ∈ (polyhedron A b).extremePoints ℝ) :
    x ∈ binaryPoints A b := by
  obtain ⟨z, hz⟩ := extreme_integral hA hx
  have hc := hbox hx.1
  have hb (i : I) : x i = 0 ∨ x i = 1 := by
    have hzi : (z i : ℝ) = x i := congrFun hz i
    have hlo : 0 ≤ z i := by exact_mod_cast (hzi ▸ (hc i).1)
    have hhi : z i ≤ 1 := by exact_mod_cast (hzi ▸ (hc i).2)
    have h : z i = 0 ∨ z i = 1 := by omega
    rcases h with h | h <;> simp_all
  refine ⟨hx.1, ⟨fun i => if x i = 1 then true else false, funext fun i => ?_⟩⟩
  rcases hb i with h | h <;> simp [vertexPoint, h]

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- Every point of a cube-bounded TU polyhedron is a finite convex
combination of feasible binary points. -/
theorem polyhedron_subset_convexHull_binaryPoints [Finite R]
    {A : Matrix R I ℤ} {b : R → ℤ}
    (hA : A.IsTotallyUnimodular) (hbox : polyhedron A b ⊆ cube I) :
    polyhedron A b ⊆ convexHull ℝ (binaryPoints A b) := by
  have he : (polyhedron A b).extremePoints ℝ ⊆ binaryPoints A b :=
    fun _ hx => extreme_mem_binaryPoints hA hbox hx
  have hc := (binaryPoints_finite A b).isCompact_convexHull ℝ
  rw [← closure_convexHull_extremePoints (polyhedron_compact A b hbox) (polyhedron_convex A b)]
  exact closure_minimal (convexHull_mono he) hc.isClosed

omit [Fintype R] [DecidableEq R] [DecidableEq I] in
/-- A cube-bounded TU polyhedron equals the hull of its feasible binary points. -/
theorem convexHull_binaryPoints_eq [Finite R] {A : Matrix R I ℤ} {b : R → ℤ}
    (hA : A.IsTotallyUnimodular) (hbox : polyhedron A b ⊆ cube I) :
    convexHull ℝ (binaryPoints A b) = polyhedron A b :=
  Set.Subset.antisymm (convexHull_min (fun _ hx => hx.1) (polyhedron_convex A b))
    (polyhedron_subset_convexHull_binaryPoints hA hbox)

omit [Fintype R] [DecidableEq R] in
/-- TU and integer bounds supply an actual feasible binary law; integrality
is proved above rather than assumed. -/
theorem exists_binaryLaw [Finite R] {A : Matrix R I ℤ} {b : R → ℤ}
    (hA : A.IsTotallyUnimodular) (hbox : polyhedron A b ⊆ cube I)
    {x : I → ℝ} (hx : x ∈ polyhedron A b) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      ∀ v : Vertex I, μ.weight v ≠ 0 → vertexPoint v ∈ polyhedron A b :=
  exists_binaryLaw_of_mem_hull (polyhedron_subset_convexHull_binaryPoints hA hbox hx)

/-- Bounds corresponding to the rows `[A; I; -A; -I]`. -/
def boxBounds (lo hi : R → ℤ) : ((R ⊕ I) ⊕ (R ⊕ I)) → ℤ
  | .inl (.inl r) => hi r
  | .inl (.inr _) => 1
  | .inr (.inl r) => -lo r
  | .inr (.inr _) => 0

omit [Fintype R] [DecidableEq R] in
/-- The augmented inequality system is exactly the unit cube with the
specified two-sided integer row bounds. -/
theorem mem_scopeBox_iff (A : Matrix R I ℤ) (lo hi : R → ℤ) (x : I → ℝ) :
    x ∈ polyhedron (scopeBoxMatrix A) (boxBounds lo hi) ↔
      x ∈ cube I ∧ ∀ r, (lo r : ℝ) ≤ (A.map (Int.castRingHom ℝ) *ᵥ x) r ∧
        (A.map (Int.castRingHom ℝ) *ᵥ x) r ≤ (hi r : ℝ) := by
  simp only [polyhedron, Set.mem_ofPred_eq, Sum.forall, scopeBoxMatrix, boxBounds,
    Matrix.mulVec, dotProduct, Matrix.map_apply, Matrix.fromRows, Matrix.of_apply, Sum.elim,
    Matrix.neg_apply, Int.coe_castRingHom, Int.cast_neg, neg_mul,
    Finset.sum_neg_distrib]
  simp only [Matrix.one_apply, Int.cast_ite, Int.cast_one, Int.cast_zero,
    ite_mul, one_mul, zero_mul, Finset.sum_ite_eq, Finset.mem_univ, if_true]
  constructor
  · rintro ⟨⟨hu, h1⟩, hl, h0⟩
    exact ⟨fun i => ⟨by linarith [h0 i], h1 i⟩, fun r => ⟨by linarith [hl r], hu r⟩⟩
  · rintro ⟨hc, hr⟩
    exact ⟨⟨fun r => (hr r).2, fun i => (hc i).2⟩,
      (fun r => by linarith [(hr r).1]), fun i => by linarith [(hc i).1]⟩

omit [Fintype R] [DecidableEq R] in
/-- Integer slabs of a TU matrix admit binary rounding that preserves all
means and all slab bounds simultaneously. -/
theorem exists_scopeBoxLaw [Finite R] (A : Matrix R I ℤ) (hA : A.IsTotallyUnimodular)
    (lo hi : R → ℤ) (x : I → ℝ) (hx : x ∈ cube I)
    (hrows : ∀ r, (lo r : ℝ) ≤ (A.map (Int.castRingHom ℝ) *ᵥ x) r ∧
      (A.map (Int.castRingHom ℝ) *ᵥ x) r ≤ (hi r : ℝ)) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ v : Vertex I, μ.weight v ≠ 0 →
      ∀ r, (lo r : ℝ) ≤ (A.map (Int.castRingHom ℝ) *ᵥ vertexPoint v) r ∧
        (A.map (Int.castRingHom ℝ) *ᵥ vertexPoint v) r ≤ (hi r : ℝ) := by
  obtain ⟨μ, hm, hs⟩ := exists_binaryLaw (totallyUnimodular_scopeBoxMatrix hA)
    (fun y hy => ((mem_scopeBox_iff A lo hi y).mp hy).1)
    ((mem_scopeBox_iff A lo hi x).mpr ⟨hx, hrows⟩)
  exact ⟨μ, hm, fun v hv => ((mem_scopeBox_iff A lo hi (vertexPoint v)).mp (hs v hv)).2⟩

/-- The integer incidence matrix of an indexed family of scopes. -/
def scopeMatrix (scope : R → Finset I) : Matrix R I ℤ :=
  fun r i => if i ∈ scope r then 1 else 0

omit [Fintype R] [DecidableEq R] in
/-- Incidence rows compute the corresponding support sums. -/
theorem scopeMatrix_mulVec (scope : R → Finset I) (x : I → ℝ) (r : R) :
    ((scopeMatrix scope).map (Int.castRingHom ℝ) *ᵥ x) r = meanSum (scope r) x := by
  simp [scopeMatrix, Matrix.mulVec, dotProduct, meanSum]

omit [Fintype R] [DecidableEq R] in
/-- TU incidence allows every support count to lie in its two adjacent
integers under one law with the prescribed means. -/
theorem exists_adjacent_scopeLaw [Finite R] (scope : R → Finset I)
    (hTU : (scopeMatrix scope).IsTotallyUnimodular)
    (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ v : Vertex I, μ.weight v ≠ 0 →
      ∀ r, countOn (scope r) v = countFloor (scope r) x ∨
        countOn (scope r) v = countFloor (scope r) x + 1 := by
  obtain ⟨μ, hm, hs⟩ := exists_scopeBoxLaw (scopeMatrix scope) hTU
    (fun r => (countFloor (scope r) x : ℤ))
    (fun r => (countFloor (scope r) x : ℤ) + 1) x hx (by
      intro r
      rw [scopeMatrix_mulVec]
      constructor
      · exact_mod_cast countFloor_le (s := scope r) hx
      · have h := countFrac_lt_one (scope r) x
        unfold countFrac at h
        push_cast
        linarith)
  refine ⟨μ, hm, fun v hv r => ?_⟩
  have hr := hs v hv r
  rw [scopeMatrix_mulVec] at hr
  have hcount : meanSum (scope r) (vertexPoint v) = (countOn (scope r) v : ℝ) :=
    (countOn_eq_sum (scope r) v).symm
  rw [hcount] at hr
  have hlo : countFloor (scope r) x ≤ countOn (scope r) v := by exact_mod_cast hr.1
  have hhi : countOn (scope r) v ≤ countFloor (scope r) x + 1 := by exact_mod_cast hr.2
  omega

omit [Fintype R] [DecidableEq R] in
/-- An adjacent-count support condition and the means determine every
count-table expectation, including tables whose entries have either sign. -/
theorem expect_cardinality_of_adjacent (s : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hs : ∀ v : Vertex I, μ.weight v ≠ 0 →
      countOn s v = countFloor s x ∨ countOn s v = countFloor s x + 1)
    (φ : ℕ → ℝ) :
    μ.expect (fun v => φ (countOn s v)) = cardinalityLower φ s x := by
  have he : μ.expect (fun v => φ (countOn s v)) =
      μ.expect (fun v => φ (countFloor s x) +
        ((countOn s v : ℝ) - countFloor s x) *
          (φ (countFloor s x + 1) - φ (countFloor s x))) := by
    unfold Law.expect
    apply Finset.sum_congr rfl
    intro v _
    dsimp only
    by_cases hv : μ.weight v = 0
    · simp [hv]
    · rcases hs v hv with hc | hc <;> rw [hc] <;> push_cast <;> ring
  rw [he, Law.expect_add, Law.expect_const, Law.expect_mul_const,
    Law.expect_sub, expect_countOn s x μ hm, Law.expect_const]
  unfold cardinalityLower countFrac
  ring

omit [Fintype R] [DecidableEq R] in
/-- One law simultaneously attains the interpolated count table on every
scope of a TU incidence family. Convexity is needed only when identifying
these values as lower envelope endpoints. -/
theorem exists_cardinality_scopeLaw [Finite R] (scope : R → Finset I)
    (hTU : (scopeMatrix scope).IsTotallyUnimodular)
    (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ r (φ : ℕ → ℝ),
      μ.expect (fun v => φ (countOn (scope r) v)) = cardinalityLower φ (scope r) x := by
  obtain ⟨μ, hm, hs⟩ := exists_adjacent_scopeLaw scope hTU x hx
  exact ⟨μ, hm, fun r φ => expect_cardinality_of_adjacent (scope r) x μ hm
    (fun v hv => hs v hv r) φ⟩

end
end MultilinearGap.TUSlab
