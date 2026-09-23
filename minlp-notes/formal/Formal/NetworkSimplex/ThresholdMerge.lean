import Formal.NetworkSimplex.SimplexEncoding

/-! Exact state merging and proportional refinement for sparse network–simplex hulls. -/
namespace NetworkSimplex
open scoped BigOperators

variable {K L E V O : Type*} [Fintype K] [Fintype L] [DecidableEq L]

/-- Sum one fiber of a finite state grouping. -/
def groupSum {M : Type*} [AddCommMonoid M] (g : K → L) (f : K → M) (l : L) : M :=
  ∑ k, if g k = l then f k else 0

theorem groupSum_total {M : Type*} [AddCommMonoid M] (g : K → L) (f : K → M) :
    ∑ l, groupSum g f l = ∑ k, f k := by
  unfold groupSum
  rw [Finset.sum_comm]
  simp

omit [Fintype L] in
theorem groupSum_nonneg (g : K → L) (w : K → ℝ) (hw : ∀ k, 0 ≤ w k) (l : L) :
    0 ≤ groupSum g w l :=
  Finset.sum_nonneg (fun k _ => by split_ifs <;> simp_all)

omit [Fintype L] in
theorem le_groupSum (g : K → L) (w : K → ℝ) (hw : ∀ k, 0 ≤ w k) (k : K) :
    w k ≤ groupSum g w (g k) := by
  classical
  have h := Finset.single_le_sum (s := Finset.univ)
    (f := fun j => if g j = g k then w j else 0)
    (fun j _ => by split_ifs <;> simp_all) (Finset.mem_univ k)
  simpa [groupSum] using h

omit [Fintype L] in
theorem groupSum_singleton {M : Type*} [AddCommMonoid M] (g : K → L) (f : K → M)
    (k : K) (hk : ∀ j, g j = g k → j = k) : groupSum g f (g k) = f k := by
  classical
  have he : ∀ j, g j = g k ↔ j = k := fun j => ⟨hk j, by rintro rfl; rfl⟩
  simp [groupSum, he]

theorem simplex_groupSum (g : K → L) {w : K → ℝ} (hw : Simplex w) :
    Simplex (groupSum g w) :=
  ⟨groupSum_nonneg g w hw.1, (groupSum_total g w).trans hw.2⟩

omit [Fintype K] in
theorem flow_finset_sum {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ} {u : E → ℝ}
    (S : Finset K) (w : K → ℝ) (f : K → E → ℝ)
    (hf : ∀ k ∈ S, Flow A b u (w k) (f k)) :
    Flow A b u (∑ k ∈ S, w k) (∑ k ∈ S, f k) := by
  classical
  induction S using Finset.induction_on with
  | empty => simp [Flow]
  | @insert k S hk ih =>
    simp only [Finset.sum_insert hk]
    exact flow_add (hf k (by simp)) (ih (fun j hj => hf j (by simp [hj])))

omit [Fintype L] in
theorem flow_groupSum (g : K → L) {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)}
    {b : V → ℝ} {u : E → ℝ} {w : K → ℝ} {f : K → E → ℝ}
    (hf : ∀ k, Flow A b u (w k) (f k)) (l : L) :
    Flow A b u (groupSum g w l) (groupSum g f l) := by
  apply flow_finset_sum
  intro k _
  split_ifs
  · exact hf k
  · exact (flow_zero_iff _ _ _ _).mpr rfl

/-- The same proportional formula applies at zero merged mass, where every
constituent weight and the merged flow vanish. -/
noncomputable def proportionalRefine (g : K → L) (w : K → ℝ) (f : L → E → ℝ)
    (k : K) : E → ℝ := (w k / groupSum g w (g k)) • f (g k)

omit [Fintype L] in
theorem proportionalRefine_flow (g : K → L) {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)}
    {b : V → ℝ} {u : E → ℝ} {w : K → ℝ} {f : L → E → ℝ}
    (hw : ∀ k, 0 ≤ w k) (hf : ∀ l, Flow A b u (groupSum g w l) (f l)) (k : K) :
    Flow A b u (w k) (proportionalRefine g w f k) := by
  by_cases hz : groupSum g w (g k) = 0
  · have hk : w k = 0 := le_antisymm (by simpa [hz] using le_groupSum g w hw k) (hw k)
    simp only [proportionalRefine, hz, div_zero, zero_smul, hk]
    exact (flow_zero_iff _ _ _ _).mpr rfl
  · have hs := flow_smul (hf (g k))
      (div_nonneg (hw k) (groupSum_nonneg g w hw (g k)))
    simpa only [div_mul_cancel₀ _ hz, proportionalRefine] using hs

omit [Fintype L] in
theorem groupSum_proportionalRefine (g : K → L) {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)}
    {b : V → ℝ} {u : E → ℝ} {w : K → ℝ} {f : L → E → ℝ}
    (hf : ∀ l, Flow A b u (groupSum g w l) (f l)) (l : L) :
    groupSum g (proportionalRefine g w f) l = f l := by
  have he : ∀ k, (if g k = l then proportionalRefine g w f k else 0) =
      ((if g k = l then w k else 0) / groupSum g w l) • f l := by
    intro k
    split_ifs with h
    · simp [proportionalRefine, h]
    · simp
  simp only [groupSum, he, ← Finset.sum_smul, ← Finset.sum_div]
  change (groupSum g w l / groupSum g w l) • f l = f l
  by_cases hz : groupSum g w l = 0
  · have hf0 : f l = 0 := (flow_zero_iff _ _ _ _).mp (by simpa [hz] using hf l)
    simp [hz, hf0]
  · simp [hz]

theorem proportionalRefine_total (g : K → L) {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)}
    {b : V → ℝ} {u : E → ℝ} {w : K → ℝ} {f : L → E → ℝ}
    (hf : ∀ l, Flow A b u (groupSum g w l) (f l)) :
    ∑ k, proportionalRefine g w f k = ∑ l, f l := by
  rw [← groupSum_total g (proportionalRefine g w f)]
  simp only [groupSum_proportionalRefine g hf]

def mergedPoint (g : K → L) (p : Point E K O) : Point E L O :=
  (p.1, groupSum g p.2.1, p.2.2)

/-- Original simplex constraints remain necessary: a merged weight alone does not
certify nonnegativity of the unobserved constituent coordinates. -/
theorem disaggregated_merge_iff (g : K → L)
    {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ} {u : E → ℝ}
    {arc : O → E} {state : O → K} {p : Point E K O}
    (hobs : ∀ o k, g k = g (state o) → k = state o) :
    Disaggregated A b u arc state p ↔
      Simplex p.2.1 ∧ Disaggregated A b u arc (g ∘ state) (mergedPoint g p) := by
  constructor
  · rintro ⟨hw, f, hf, hsum, ho⟩
    refine ⟨hw, simplex_groupSum g hw, groupSum g f, flow_groupSum g hf, ?_, ?_⟩
    · exact (groupSum_total g f).trans hsum
    · intro o
      change groupSum g f (g (state o)) (arc o) = _
      rw [groupSum_singleton g f (state o) (hobs o)]
      exact ho o
  · rintro ⟨hw, _, f, hf, hsum, ho⟩
    refine ⟨hw, proportionalRefine g p.2.1 f, proportionalRefine_flow g hw.1 hf, ?_, ?_⟩
    · exact (proportionalRefine_total g hf).trans hsum
    · intro o
      have he := groupSum_proportionalRefine g hf (g (state o))
      rw [groupSum_singleton g _ (state o) (hobs o)] at he
      change proportionalRefine g p.2.1 f (state o) (arc o) = _
      rw [he]
      exact ho o

/-- Exact equivalence of the original graph hull and the projected, merged graph hull. -/
theorem hull_merge_iff (g : K → L)
    {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ} {u : E → ℝ}
    {arc : O → E} {state : O → K} {p : Point E K O}
    (hobs : ∀ o k, g k = g (state o) → k = state o) :
    p ∈ convexHull ℝ (Graph A b u arc state) ↔ Simplex p.2.1 ∧
      mergedPoint g p ∈ convexHull ℝ (Graph A b u arc (g ∘ state)) := by
  rw [mem_convexHull_graph_iff, mem_convexHull_graph_iff]
  exact disaggregated_merge_iff g hobs

end NetworkSimplex
