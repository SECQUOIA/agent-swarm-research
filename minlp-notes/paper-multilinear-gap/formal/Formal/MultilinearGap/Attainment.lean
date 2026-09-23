import Formal.MultilinearGap.BoxTransfer

/-! General vertex representations and attained envelope endpoints on finite boxes. -/

noncomputable section

namespace CubicGap

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
/-- A separately affine graph hull is a compact polytope. -/
theorem cubeGraph_hull_isCompact [Finite I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    IsCompact (convexHull ℝ (cubeGraph f)) := by
  rw [cubeGraph_hull_eq_vertexGraph_hull f hf]
  exact (Set.finite_range _).isCompact_convexHull ℝ

omit [Fintype I] in
/-- Every vertical slice is compact, including slices outside the cube. -/
theorem envelopeValues_isCompact [Finite I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) : IsCompact (envelopeValues f x) := by
  have h : IsCompact (convexHull ℝ (cubeGraph f) ∩ {q | q.1 = x}) :=
    (cubeGraph_hull_isCompact f hf).inter_right
      (isClosed_eq continuous_fst continuous_const)
  have he : Prod.snd '' (convexHull ℝ (cubeGraph f) ∩ {q | q.1 = x}) =
      envelopeValues f x := by
    ext z
    constructor
    · rintro ⟨⟨y, w⟩, ⟨hq, hy⟩, rfl⟩
      change y = x at hy
      subst y
      exact hq
    · intro hz
      exact ⟨(x, z), ⟨hz, rfl⟩, rfl⟩
  rw [← he]
  exact h.image continuous_snd

omit [Fintype I] [DecidableEq I] in
/-- The original graph point belongs to its own vertical hull slice. -/
theorem envelopeValues_nonempty (f : (I → ℝ) → ℝ) (x : I → ℝ) (hx : x ∈ cube I) :
    (envelopeValues f x).Nonempty :=
  ⟨f x, subset_convexHull ℝ (cubeGraph f) ⟨hx, rfl⟩⟩

omit [Fintype I] in
/-- The infimum and supremum are actual endpoints, without certificate assumptions. -/
theorem envelopeValues_endpoints [Finite I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ cube I) :
    IsLeast (envelopeValues f x) (sInf (envelopeValues f x)) ∧
    IsGreatest (envelopeValues f x) (sSup (envelopeValues f x)) :=
  ⟨(envelopeValues_isCompact f hf x).isLeast_sInf (envelopeValues_nonempty f x hx),
   (envelopeValues_isCompact f hf x).isGreatest_sSup (envelopeValues_nonempty f x hx)⟩

/-- Both envelope endpoints are attained by finite vertex laws with the given means. -/
theorem envelope_endpoints_attained_by_laws (f : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f) (x : I → ℝ) (hx : x ∈ cube I) :
    (∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => f (vertexPoint v)) = sInf (envelopeValues f x)) ∧
    (∃ μ : Law (Vertex I), HasMeans μ x ∧
      μ.expect (fun v => f (vertexPoint v)) = sSup (envelopeValues f x)) := by
  have h := envelopeValues_endpoints f hf x hx
  exact ⟨(mem_cubeGraph_hull_iff f hf x _).mp h.1.1,
    (mem_cubeGraph_hull_iff f hf x _).mp h.2.1⟩

theorem hullGap_nonneg (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ cube I) : 0 ≤ hullGap f x := by
  have h := envelopeValues_endpoints f hf x hx
  exact sub_nonneg.mpr (h.1.2 h.2.1)

end CubicGap

namespace MultilinearGap

open CubicGap

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [Fintype I] in
/-- Rescaling each coordinate preserves separate affinity, also at zero widths. -/
theorem separatelyAffine_boxPoint (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (l u : I → ℝ) : SeparatelyAffine (fun p => f (boxPoint l u p)) := by
  intro p i t
  have he (a : ℝ) : boxPoint l u (Function.update p i a) =
      Function.update (boxPoint l u p) i (l i + (u i - l i) * a) := by
    funext j
    by_cases hji : j = i
    · subst j; simp [boxPoint]
    · simp [boxPoint, Function.update_of_ne hji]
  simp only [he]
  rw [hf (boxPoint l u p) i (l i + (u i - l i) * t),
    hf (boxPoint l u p) i (l i + (u i - l i) * 0),
    hf (boxPoint l u p) i (l i + (u i - l i) * 1)]
  ring

/-- The graph vertices of a finite box; fixed coordinates may repeat vertices. -/
def boxVertexGraph (l u : I → ℝ) (f : (I → ℝ) → ℝ) : Set ((I → ℝ) × ℝ) :=
  Set.range fun v : Vertex I => (boxPoint l u (vertexPoint v),
    f (boxPoint l u (vertexPoint v)))

private def graphRescaling (l u : I → ℝ) :
    ((I → ℝ) × ℝ) →ᵃ[ℝ] ((I → ℝ) × ℝ) where
  toFun q := (boxPoint l u q.1, q.2)
  linear := {
    toFun q := (fun i => (u i - l i) * q.1 i, q.2)
    map_add' := by intros; ext <;> simp [mul_add]
    map_smul' := by intros; ext <;> simp [mul_left_comm] }
  map_vadd' := by intros; ext <;> simp [boxPoint]; ring

omit [Fintype I] in
/-- The continuous graph over any finite box has exactly its vertex graph hull. -/
theorem boxGraph_hull_eq_boxVertexGraph_hull [Finite I] (l u : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    convexHull ℝ (boxGraph l u f) = convexHull ℝ (boxVertexGraph l u f) := by
  have he : graphRescaling l u '' cubeGraph (fun p => f (boxPoint l u p)) =
      boxGraph l u f := by
    ext q
    constructor
    · rintro ⟨r, hr, rfl⟩
      exact ⟨boxPoint_mem l u r.1 hlu hr.1, hr.2⟩
    · intro hq
      obtain ⟨p, hp, he⟩ := exists_boxPoint l u hlu q.1 hq.1
      refine ⟨(p, q.2), ⟨hp, ?_⟩, ?_⟩
      · simpa [he] using hq.2
      · change (boxPoint l u p, q.2) = q
        simp [he]
  rw [← he, ← (graphRescaling l u).image_convexHull,
    cubeGraph_hull_eq_vertexGraph_hull _ (separatelyAffine_boxPoint f hf l u),
    (graphRescaling l u).image_convexHull]
  congr 1
  ext q
  constructor
  · rintro ⟨r, ⟨v, rfl⟩, rfl⟩
    exact ⟨v, rfl⟩
  · rintro ⟨v, rfl⟩
    exact ⟨(vertexPoint v, f (boxPoint l u (vertexPoint v))), ⟨v, rfl⟩, rfl⟩

/-- Every box graph hull point is a law on box vertices with its coordinate means. -/
theorem mem_boxGraph_hull_iff (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) (x : I → ℝ) (z : ℝ) :
    (x, z) ∈ convexHull ℝ (boxGraph l u f) ↔
      ∃ μ : Law (Vertex I),
        (∀ i, μ.expect (fun v => boxPoint l u (vertexPoint v) i) = x i) ∧
        μ.expect (fun v => f (boxPoint l u (vertexPoint v))) = z := by
  rw [boxGraph_hull_eq_boxVertexGraph_hull l u hlu f hf,
    boxVertexGraph, Law.mem_convexHull_range_iff]
  constructor
  · rintro ⟨μ, hμ⟩
    refine ⟨μ, ?_, ?_⟩
    · intro i
      simpa [Law.barycenter, Law.expect, Prod.fst_sum, Finset.sum_apply] using
        congrArg (fun q => q.1 i) hμ
    · simpa [Law.barycenter, Law.expect, Prod.snd_sum] using congrArg Prod.snd hμ
  · rintro ⟨μ, hm, ho⟩
    refine ⟨μ, ?_⟩
    apply Prod.ext
    · ext i
      simpa [Law.barycenter, Law.expect, Prod.fst_sum, Finset.sum_apply] using hm i
    · simpa [Law.barycenter, Law.expect, Prod.snd_sum] using ho

omit [Fintype I] in
/-- The graph hull on a finite box is compact, including degenerate boxes. -/
theorem boxGraph_hull_isCompact [Finite I] (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) :
    IsCompact (convexHull ℝ (boxGraph l u f)) := by
  rw [boxGraph_hull_eq_boxVertexGraph_hull l u hlu f hf]
  exact (Set.finite_range _).isCompact_convexHull ℝ

omit [Fintype I] in
/-- Every feasible box slice is compact, also at fixed coordinates. -/
theorem boxEnvelopeValues_isCompact [Finite I] (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    IsCompact (boxEnvelopeValues l u f x) := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxEnvelopeValues_eq_of_mem l u hlu f p hp]
  exact envelopeValues_isCompact _ (separatelyAffine_boxPoint f hf l u) p

omit [Fintype I] in
/-- The endpoint theorem on arbitrary finite boxes includes fixed coordinates. -/
theorem boxEnvelopeValues_endpoints [Finite I] (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    IsLeast (boxEnvelopeValues l u f x) (sInf (boxEnvelopeValues l u f x)) ∧
    IsGreatest (boxEnvelopeValues l u f x) (sSup (boxEnvelopeValues l u f x)) := by
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxEnvelopeValues_eq_of_mem l u hlu f p hp]
  exact envelopeValues_endpoints _ (separatelyAffine_boxPoint f hf l u) p hp

/-- Both box envelope endpoints have attaining vertex laws. -/
theorem boxEnvelope_endpoints_attained_by_laws (l u : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) :
    (∃ μ : Law (Vertex I),
      (∀ i, μ.expect (fun v => boxPoint l u (vertexPoint v) i) = x i) ∧
      μ.expect (fun v => f (boxPoint l u (vertexPoint v))) =
        sInf (boxEnvelopeValues l u f x)) ∧
    (∃ μ : Law (Vertex I),
      (∀ i, μ.expect (fun v => boxPoint l u (vertexPoint v) i) = x i) ∧
      μ.expect (fun v => f (boxPoint l u (vertexPoint v))) =
        sSup (boxEnvelopeValues l u f x)) := by
  have h := boxEnvelopeValues_endpoints l u hlu f hf x hx
  exact ⟨(mem_boxGraph_hull_iff l u hlu f hf x _).mp h.1.1,
    (mem_boxGraph_hull_iff l u hlu f hf x _).mp h.2.1⟩

omit [Fintype I] in
theorem boxHullGap_nonneg [Finite I] (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u) : 0 ≤ boxHullGap l u f x := by
  have h := boxEnvelopeValues_endpoints l u hlu f hf x hx
  exact sub_nonneg.mpr (h.1.2 h.2.1)

end MultilinearGap
