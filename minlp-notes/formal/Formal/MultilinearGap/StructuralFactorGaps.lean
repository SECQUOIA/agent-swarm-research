import Formal.MultilinearGap.StructuralInterpolation
import Formal.MultilinearGap.StructuralCardinalityUpper
import Formal.MultilinearGap.EnvelopeFunctions

/-!
# From simultaneous factor laws to scalar graph-hull bounds

These are integration lemmas. Their law hypotheses are explicit; a graph
theorem must construct those laws before any structural gap bound follows.
-/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J]

def factorSum (f : J → (I → ℝ) → ℝ) (x : I → ℝ) : ℝ := ∑ j, f j x

omit [Fintype I] in
theorem factorSum_separatelyAffine (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j, SeparatelyAffine (f j)) : SeparatelyAffine (factorSum f) := by
  intro x i t
  simp only [factorSum, Finset.mul_sum, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun j _ => hf j x i t

theorem expect_factorSum (μ : Law (Vertex I)) (f : J → (I → ℝ) → ℝ) :
    μ.expect (fun v => factorSum f (vertexPoint v)) =
      ∑ j, μ.expect (fun v => f j (vertexPoint v)) := by
  simp only [factorSum, Law.expect, Finset.mul_sum]
  exact Finset.sum_comm

/-- One law maximizing every factor also maximizes their sum. -/
theorem factorSum_maximum (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j, SeparatelyAffine (f j)) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x)
    (hmax : ∀ j, IsGreatest (envelopeValues (f j) x)
      (μ.expect (fun v => f j (vertexPoint v)))) :
    IsGreatest (envelopeValues (factorSum f) x)
      (∑ j, sSup (envelopeValues (f j) x)) := by
  apply maximum_from_laws _ (factorSum_separatelyAffine f hf)
  · intro ν hn
    rw [expect_factorSum]
    apply Finset.sum_le_sum
    intro j _
    rw [(hmax j).csSup_eq]
    apply (hmax j).2
    exact (mem_cubeGraph_hull_iff _ (hf j) x _).mpr ⟨ν, hn, rfl⟩
  · refine ⟨μ, hm, ?_⟩
    rw [expect_factorSum]
    exact Finset.sum_congr rfl fun j _ => (hmax j).csSup_eq.symm

/-- Any feasible lower-law bound gives a gap bound once the upper values have
been attained simultaneously. The hypothesis is on actual expectations. -/
theorem factorSum_gap_of_law (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j, SeparatelyAffine (f j)) (x : I → ℝ)
    (hmax : IsGreatest (envelopeValues (factorSum f) x)
      (∑ j, sSup (envelopeValues (f j) x)))
    (μ : Law (Vertex I)) (hm : HasMeans μ x) (c : ℝ)
    (hdef : c * (∑ j, hullGap (f j) x) ≤
      (∑ j, sSup (envelopeValues (f j) x)) -
        μ.expect (fun v => factorSum f (vertexPoint v))) :
    c * (∑ j, hullGap (f j) x) ≤ hullGap (factorSum f) x := by
  have hx : x ∈ cube I := by
    intro i
    rw [← hm i]
    constructor
    · exact μ.expect_nonneg fun v => by simp only [vertexPoint]; split <;> norm_num
    · calc μ.expect (fun v => vertexPoint v i) ≤ μ.expect (fun _ => 1) :=
            μ.expect_mono fun v => by simp only [vertexPoint]; split <;> norm_num
           _ = 1 := μ.expect_const 1
  have hl := (envelopeValues_endpoints (factorSum f)
    (factorSum_separatelyAffine f hf) x hx).1.2
    ((mem_cubeGraph_hull_iff _ (factorSum_separatelyAffine f hf) x _).mpr ⟨μ, hm, rfl⟩)
  rw [hullGap, hmax.csSup_eq]
  linarith

/-- If two feasible laws between them minimize each factor, their equal
mixture captures at least half the sum of the factor gaps. -/
theorem factorSum_two_law_bound (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j, SeparatelyAffine (f j)) (x : I → ℝ) (hx : x ∈ cube I)
    (hmax : IsGreatest (envelopeValues (factorSum f) x)
      (∑ j, sSup (envelopeValues (f j) x)))
    (μ ν : Law (Vertex I)) (hm : HasMeans μ x) (hn : HasMeans ν x)
    (hmin : ∀ j,
      μ.expect (fun v => f j (vertexPoint v)) = sInf (envelopeValues (f j) x) ∨
      ν.expect (fun v => f j (vertexPoint v)) = sInf (envelopeValues (f j) x)) :
    (∑ j, hullGap (f j) x) ≤ 2 * hullGap (factorSum f) x := by
  let ξ := Law.mix μ ν (1/2) (1/2) (by norm_num) (by norm_num) (by norm_num)
  have he (g : Vertex I → ℝ) : ξ.expect g = (1/2) * μ.expect g + (1/2) * ν.expect g := by
    simp [ξ, Law.expect, Law.mix, add_mul, mul_assoc, Finset.sum_add_distrib,
      ← Finset.mul_sum]
  have hξ : HasMeans ξ x := by intro i; rw [he, hm i, hn i]; ring
  have h := factorSum_gap_of_law f hf x hmax ξ hξ (1/2) ?_
  · linarith
  rw [expect_factorSum, Finset.mul_sum, ← Finset.sum_sub_distrib]
  apply Finset.sum_le_sum
  intro j _
  have hμ := (envelopeValues_endpoints (f j) (hf j) x hx).2.2
    ((mem_cubeGraph_hull_iff _ (hf j) x _).mpr ⟨μ, hm, rfl⟩)
  have hν := (envelopeValues_endpoints (f j) (hf j) x hx).2.2
    ((mem_cubeGraph_hull_iff _ (hf j) x _).mpr ⟨ν, hn, rfl⟩)
  rw [he, hullGap]
  rcases hmin j with hj | hj <;> rw [hj] <;> linarith


/-- The scalar gap of a sum never exceeds the sum of the individual gaps.
No simultaneous maximizing or minimizing law is required. -/
theorem hullGap_factorSum_le (f : J → (I → ℝ) → ℝ)
    (hf : ∀ j, SeparatelyAffine (f j)) (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (factorSum f) x ≤ ∑ j, hullGap (f j) x := by
  obtain ⟨μ, hm, hlo⟩ := (envelope_endpoints_attained_by_laws (factorSum f)
    (factorSum_separatelyAffine f hf) x hx).1
  obtain ⟨ν, hn, hhi⟩ := (envelope_endpoints_attained_by_laws (factorSum f)
    (factorSum_separatelyAffine f hf) x hx).2
  rw [hullGap, ← hhi, ← hlo, expect_factorSum, expect_factorSum,
    ← Finset.sum_sub_distrib]
  apply Finset.sum_le_sum
  intro j _
  have hu := (envelopeValues_endpoints (f j) (hf j) x hx).2.2
    ((mem_cubeGraph_hull_iff _ (hf j) x _).mpr ⟨ν, hn, rfl⟩)
  have hl := (envelopeValues_endpoints (f j) (hf j) x hx).1.2
    ((mem_cubeGraph_hull_iff _ (hf j) x _).mpr ⟨μ, hm, rfl⟩)
  exact sub_le_sub hu hl

end
end MultilinearGap
