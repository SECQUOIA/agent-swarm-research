import Mathlib

/-!
# Exact simplex-vertex disaggregation

Formalizes Proposition `prop:disaggregation` in
`paper-network-simplex/sections/01-foundations.tex`.

`K` includes the residual simplex vertex (take `K = Fin (m + 1)`).
An observation type `O` and its two coordinate maps encode arbitrary sparse
observations. The map `A` may be any real linear map, so incidence matrices,
parallel arcs, and loops are included. Real capacities are finite; their sign
need not be assumed separately for this equivalence.
-/

namespace NetworkSimplex

noncomputable section


variable {E V K O : Type*} [Fintype K]

abbrev Point (E K O : Type*) := (E → ℝ) × ((K → ℝ) × (O → ℝ))

/-- All simplex weights, including the residual weight. -/
def Simplex (w : K → ℝ) : Prop := (∀ k, 0 ≤ w k) ∧ ∑ k, w k = 1

/-- The scaled system is defined by equations and bounds, also at weight zero. -/
def Flow (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (w : ℝ) (f : E → ℝ) : Prop :=
  A f = w • b ∧ ∀ e, 0 ≤ f e ∧ f e ≤ w * u e

/-- Observed bilinear graph with all simplex weights explicitly represented. -/
def Graph (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → K) : Set (Point E K O) :=
  {p | Simplex p.2.1 ∧ Flow A b u 1 p.1 ∧
    ∀ o, p.2.2 o = p.1 (arc o) * p.2.1 (state o)}

/-- State flows, conservation of their sum, and observed state coordinates. -/
def Disaggregated (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u : E → ℝ)
    (arc : O → E) (state : O → K) (p : Point E K O) : Prop :=
  Simplex p.2.1 ∧ ∃ f : K → E → ℝ,
    (∀ k, Flow A b u (p.2.1 k) (f k)) ∧
    (∑ k, f k) = p.1 ∧ ∀ o, f (state o) (arc o) = p.2.2 o

theorem flow_zero_iff (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ) (u f : E → ℝ) :
    Flow A b u 0 f ↔ f = 0 := by
  constructor
  · intro h
    funext e
    exact le_antisymm (by simpa using (h.2 e).2) (h.2 e).1
  · rintro rfl
    simp [Flow]

theorem flow_smul {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ} {u f : E → ℝ}
    {w a : ℝ} (h : Flow A b u w f) (ha : 0 ≤ a) :
    Flow A b u (a * w) (a • f) := by
  constructor
  · simp [map_smul, h.1, smul_smul]
  · intro e
    exact ⟨mul_nonneg ha (h.2 e).1, by
      simpa [mul_assoc] using mul_le_mul_of_nonneg_left (h.2 e).2 ha⟩

theorem flow_add {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ} {u f g : E → ℝ}
    {a c : ℝ} (hf : Flow A b u a f) (hg : Flow A b u c g) :
    Flow A b u (a + c) (f + g) := by
  constructor
  · simp [hf.1, hg.1, add_smul]
  · intro e
    exact ⟨add_nonneg (hf.2 e).1 (hg.2 e).1, by
      simpa [add_mul] using add_le_add (hf.2 e).2 (hg.2 e).2⟩

theorem graph_disaggregated {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ}
    {u : E → ℝ} {arc : O → E} {state : O → K} {p : Point E K O}
    (h : p ∈ Graph A b u arc state) : Disaggregated A b u arc state p := by
  refine ⟨h.1, fun k => p.2.1 k • p.1, ?_, ?_, ?_⟩
  · intro k
    simpa using flow_smul h.2.1 (h.1.1 k)
  · rw [← Finset.sum_smul, h.1.2, one_smul]
  · intro o
    simpa [mul_comm] using (h.2.2 o).symm

theorem convex_disaggregated (A : (E → ℝ) →ₗ[ℝ] (V → ℝ)) (b : V → ℝ)
    (u : E → ℝ) (arc : O → E) (state : O → K) :
    Convex ℝ {p | Disaggregated A b u arc state p} := by
  rintro p ⟨hp, f, hf, hfs, hfo⟩ q ⟨hq, g, hg, hgs, hgo⟩ a c ha hc hac
  refine ⟨⟨?_, ?_⟩, fun k => a • f k + c • g k, ?_, ?_, ?_⟩
  · intro k
    exact add_nonneg (mul_nonneg ha (hp.1 k)) (mul_nonneg hc (hq.1 k))
  · change ∑ k, (a * p.2.1 k + c * q.2.1 k) = 1
    simp [Finset.sum_add_distrib, ← Finset.mul_sum, hp.2, hq.2, hac]
  · intro k
    exact flow_add (flow_smul (hf k) ha) (flow_smul (hg k) hc)
  · simp only [Finset.sum_add_distrib, ← Finset.smul_sum, hfs, hgs]
    rfl
  · intro o
    change a * f (state o) (arc o) + c * g (state o) (arc o) = _
    rw [hfo, hgo]
    rfl

open Classical in
/-- A lift supplies at most `Fintype.card K` graph points. Zero weights use a
feasible positive-weight state's normalized flow, so no flow-existence assumption
is needed and the proof also detects the empty-flow case. -/
theorem disaggregation_decomposition {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ}
    {u : E → ℝ} {arc : O → E} {state : O → K} {p : Point E K O}
    (h : Disaggregated A b u arc state p) :
    ∃ q : K → Point E K O, (∀ k, q k ∈ Graph A b u arc state) ∧
      (∀ k j, (q k).2.1 j = if j = k then 1 else 0) ∧
      ∑ k, p.2.1 k • q k = p := by
  classical
  obtain ⟨hw, f, hf, hfs, hfo⟩ := h
  have hex : ∃ k, 0 < p.2.1 k := by
    by_contra! hn
    have : ∑ k, p.2.1 k ≤ 0 := Finset.sum_nonpos fun k _ => hn k
    linarith [hw.2]
  obtain ⟨k₀, hk₀⟩ := hex
  let base := (p.2.1 k₀)⁻¹ • f k₀
  have hbase : Flow A b u 1 base := by
    simpa [base, ne_of_gt hk₀] using flow_smul (hf k₀) (inv_nonneg.mpr hk₀.le)
  let x : K → E → ℝ := fun k => if p.2.1 k = 0 then base else (p.2.1 k)⁻¹ • f k
  have hx : ∀ k, Flow A b u 1 (x k) := by
    intro k
    by_cases hk : p.2.1 k = 0
    · simpa [x, hk] using hbase
    · simpa [x, hk] using flow_smul (hf k) (inv_nonneg.mpr (hw.1 k))
  have hxf : ∀ k, p.2.1 k • x k = f k := by
    intro k
    by_cases hk : p.2.1 k = 0
    · have hf0 : f k = 0 := (flow_zero_iff A b u (f k)).mp (by simpa [hk] using hf k)
      simp [hk, hf0]
    · simp [x, hk, smul_smul]
  let q : K → Point E K O := fun k =>
    (x k, (fun j => if j = k then 1 else 0,
      fun o => x k (arc o) * (if state o = k then 1 else 0)))
  refine ⟨q, ?_, ?_, ?_⟩
  · intro k
    refine ⟨⟨?_, ?_⟩, hx k, ?_⟩
    · intro j
      simp only [q]
      split_ifs <;> norm_num
    · simp [q]
    · intro o
      rfl
  · intro k j
    rfl
  · apply Prod.ext
    · simpa only [Prod.fst_sum, Prod.smul_fst, q, hxf] using hfs
    · apply Prod.ext
      · funext j
        simp only [Prod.snd_sum, Prod.fst_sum, Prod.smul_snd, Prod.smul_fst,
          Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
        simp [q, mul_ite]
      · funext o
        simp only [Prod.snd_sum, Prod.smul_snd, Finset.sum_apply, Pi.smul_apply,
          smul_eq_mul, q, mul_ite, mul_one, mul_zero]
        have he := congrFun (hxf (state o)) (arc o)
        simpa using he.trans (hfo o)

/-- Exact hull equality, including empty base flow systems and a single state. -/
theorem mem_convexHull_graph_iff {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ}
    {u : E → ℝ} {arc : O → E} {state : O → K} {p : Point E K O} :
    p ∈ convexHull ℝ (Graph A b u arc state) ↔ Disaggregated A b u arc state p := by
  constructor
  · intro hp
    exact convexHull_min (fun _ h => graph_disaggregated h)
      (convex_disaggregated A b u arc state) hp
  · intro h
    obtain ⟨q, hq, _, heq⟩ := disaggregation_decomposition h
    exact mem_convexHull_of_exists_fintype p.2.1 q h.1.1 h.1.2 hq heq

theorem flow_nonempty_of_disaggregated {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)} {b : V → ℝ}
    {u : E → ℝ} {arc : O → E} {state : O → K} {p : Point E K O}
    (h : Disaggregated A b u arc state p) : ∃ x, Flow A b u 1 x := by
  obtain ⟨q, hq, _, _⟩ := disaggregation_decomposition h
  have hex : Nonempty K := by
    by_contra hn
    have : IsEmpty K := not_nonempty_iff.mp hn
    have := h.1.2
    simp at this
  obtain ⟨k⟩ := hex
  exact ⟨(q k).1, (hq k).2.1⟩

theorem disaggregated_empty_of_flow_empty {A : (E → ℝ) →ₗ[ℝ] (V → ℝ)}
    {b : V → ℝ} {u : E → ℝ} (arc : O → E) (state : O → K)
    (h : ¬ ∃ x, Flow A b u 1 x) :
    {p | Disaggregated A b u arc state p} = ∅ := by
  apply Set.eq_empty_iff_forall_notMem.mpr
  intro p hp
  exact h (flow_nonempty_of_disaggregated hp)

end
end NetworkSimplex
