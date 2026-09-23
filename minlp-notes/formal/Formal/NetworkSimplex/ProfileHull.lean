import Formal.NetworkSimplex.Chain
import Formal.NetworkSimplex.Profile
import Formal.NetworkSimplex.Reduction

/-! The common-profile inequalities describe the actual chain bilinear convex hull. -/
namespace NetworkSimplex
namespace Chain

noncomputable section

variable {L : ℕ} {J : Type*} [Fintype J]

/-- Assemble the two gadget arcs and the bypass into a network flow vector. -/
def pack (xa xb : Fin L → ℝ) (xh : ℝ) : ChainArc L → ℝ
  | Sum.inl (i, false) => xa i
  | Sum.inl (i, true) => xb i
  | Sum.inr _ => xh

@[simp] theorem pack_a (xa xb : Fin L → ℝ) (xh : ℝ) (i : Fin L) :
    pack xa xb xh (a i) = xa i := rfl
@[simp] theorem pack_b (xa xb : Fin L → ℝ) (xh : ℝ) (i : Fin L) :
    pack xa xb xh (b i) = xb i := rfl
@[simp] theorem pack_bypass (xa xb : Fin L → ℝ) (xh : ℝ) :
    pack xa xb xh bypass = xh := rfl

/-- Arbitrary observed arc-state pairs, without imposing a positive state weight. -/
def Selected (c : Fin L → J → StateClass) (observedH : J → Prop) :
    ChainArc L × J → Prop
  | (Sum.inl (i, false), j) => observesA (c i j)
  | (Sum.inl (i, true), j) => observesB (c i j)
  | (Sum.inr _, j) => observedH j

abbrev Observation (c : Fin L → J → StateClass) (observedH : J → Prop) :=
  {o : ChainArc L × J // Selected c observedH o}

def chainPoint (c : Fin L → J → StateClass) (u v : Fin L → J → ℝ)
    (weights : J → ℝ) (xa xb : Fin L → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ) :
    Point (ChainArc L) J (Observation c observedH) :=
  (pack xa xb xh, weights, fun o =>
    pack (fun i => u i o.val.2) (fun i => v i o.val.2) (zh o.val.2) o.val.1)

def chainGraph (c : Fin L → J → StateClass) (observedH : J → Prop) :
    Set (Point (ChainArc L) J (Observation c observedH)) :=
  Graph (incidence L) (demand L) (fun _ => 1) (fun o => o.val.1) (fun o => o.val.2)

/-- Packing and unpacking state flows preserves every equation and observation. -/
theorem disaggregated_iff_stateFlows (c : Fin L → J → StateClass)
    (u v : Fin L → J → ℝ) (weights : J → ℝ) (xa xb : Fin L → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ) (hweights : Simplex weights) :
    Disaggregated (incidence L) (demand L) (fun _ => 1)
      (fun o : Observation c observedH => o.val.1) (fun o => o.val.2)
      (chainPoint c u v weights xa xb xh observedH zh) ↔
    ∃ f, ValidStateFlows c u v weights xa xb xh observedH zh f := by
  classical
  constructor
  · rintro ⟨_, g, hg, hsum, hobs⟩
    have hg' := fun j => (flow_iff L (g j) (weights j)).mp (hg j)
    let f : StateFlows (Fin L) J :=
      ⟨fun i j => g j (a i), fun i j => g j (b i), fun j => g j bypass⟩
    refine ⟨f, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact fun i j => (hg' j).1 (a i)
    · exact fun i j => (hg' j).1 (b i)
    · exact fun j => (hg' j).1 bypass
    · exact fun i j => (hg' j).2 i
    · intro i
      have h := congrFun hsum (a i)
      simpa [f, chainPoint] using h
    · intro i
      have h := congrFun hsum (b i)
      simpa [f, chainPoint] using h
    · have h := congrFun hsum bypass
      simpa [f, chainPoint] using h
    · intro i j hj
      exact hobs ⟨(a i, j), hj⟩
    · intro i j hj
      exact hobs ⟨(b i, j), hj⟩
    · intro j hj
      exact hobs ⟨(bypass, j), hj⟩
  · rintro ⟨f, ha, hb, hh, hbalance, hsuma, hsumb, hsumh, hobsA, hobsB, hobsH⟩
    let g : J → ChainArc L → ℝ := fun j =>
      pack (fun i => f.a i j) (fun i => f.b i j) (f.h j)
    refine ⟨hweights, g, ?_, ?_, ?_⟩
    · intro j
      apply (flow_iff L (g j) (weights j)).mpr
      refine ⟨?_, ?_⟩
      · intro e
        rcases e with ⟨i, flag⟩ | bypassUnit
        · cases flag
          · exact ha i j
          · exact hb i j
        · exact hh j
      · exact fun i => hbalance i j
    · funext e
      rcases e with ⟨i, flag⟩ | bypassUnit
      · cases flag
        · simpa [g, pack, chainPoint] using hsuma i
        · simpa [g, pack, chainPoint] using hsumb i
      · simpa [g, pack, chainPoint] using hsumh
    · rintro ⟨⟨e, j⟩, he⟩
      rcases e with ⟨i, flag⟩ | bypassUnit
      · cases flag
        · exact hobsA i j he
        · exact hobsB i j he
      · exact hobsH j he

/-- Proposition `chain-profile`: exact membership in the convex hull of the
observed products on the actual capacitated chain network. All simplex states
are explicit, so zero weights and the unobserved residual state are covered. -/
theorem mem_chainHull_iff_profile (c : Fin L → J → StateClass)
    (u v : Fin L → J → ℝ) (weights : J → ℝ) (xa xb : Fin L → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ) (hweights : Simplex weights)
    (haggregate : ∀ i, xa i + xb i = 1 - xh)
    (hn : ∀ i, ObservedNonnegative (c i) (u i) (v i)) :
    chainPoint c u v weights xa xb xh observedH zh ∈ convexHull ℝ (chainGraph c observedH) ↔
      ∃ w, Profile c u v weights xa xh observedH zh w := by
  rw [chainGraph, mem_convexHull_graph_iff]
  rw [disaggregated_iff_stateFlows c u v weights xa xb xh observedH zh hweights]
  exact (profile_iff_stateFlows c u v weights xa xb xh observedH zh
    hweights.2 haggregate hn).symm


namespace ReductionData

variable {m : ℕ}

/-- The other gadget arc is fixed by its original flow balance. -/
def xb (D : ReductionData m (Fin L)) (i : Fin L) : ℝ := 1 - D.xh - D.xa i

def graphPoint (D : ReductionData m (Fin L)) :
    Point (ChainArc L) (Fin (m + 1)) (Observation D.c (fun j => D.observedH j = true)) :=
  chainPoint D.c D.u D.v D.weights D.xa D.xb D.xh (fun j => D.observedH j = true) D.zh

def graph (D : ReductionData m (Fin L)) :
    Set (Point (ChainArc L) (Fin (m + 1)) (Observation D.c (fun j => D.observedH j = true))) :=
  chainGraph D.c (fun j => D.observedH j = true)

/-- The original-domain checks in the paper, with the b-arc balance substituted. -/
def OriginalDomain (D : ReductionData m (Fin L)) : Prop :=
  Simplex D.weights ∧ Flow (incidence L) (demand L) (fun _ => 1) 1
    (pack D.xa D.xb D.xh) ∧
  (∀ i, ObservedNonnegative (D.c i) (D.u i) (D.v i)) ∧
  ∀ j, D.observedH j = true → 0 ≤ D.zh j

/-- The full chain hull is exactly the original-domain checks and the common
profile system. This is the direct interface to residual elimination and the
finite two-state and three-state separation tests. -/
theorem mem_hull_iff (D : ReductionData m (Fin L)) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧ ∃ w, D.FullProfile w := by
  constructor
  · intro h
    have hd := (mem_convexHull_graph_iff).mp h
    have hweights : Simplex D.weights := hd.1
    have hf := (disaggregated_iff_stateFlows D.c D.u D.v D.weights D.xa D.xb D.xh
      (fun j => D.observedH j = true) D.zh hweights).mp hd
    obtain ⟨f, ha, hb, hh, hbalance, hsuma, hsumb, hsumh, hobsA, hobsB, hobsH⟩ := hf
    have hcap (g : Fin (m + 1) → ℝ) (hg : ∀ j, 0 ≤ g j ∧ g j ≤ D.weights j) :
        0 ≤ ∑ j, g j ∧ (∑ j, g j) ≤ 1 := by
      constructor
      · exact Finset.sum_nonneg fun j _ => (hg j).1
      · rw [← hweights.2]
        exact Finset.sum_le_sum fun j _ => (hg j).2
    have hn : ∀ i, ObservedNonnegative (D.c i) (D.u i) (D.v i) := by
      intro i
      constructor
      · intro j hj
        rw [← hobsA i j hj]
        exact (ha i j).1
      · intro j hj
        rw [← hobsB i j hj]
        exact (hb i j).1
    refine ⟨⟨hweights, ?_, hn, ?_⟩, ?_⟩
    · apply (flow_iff L (pack D.xa D.xb D.xh) 1).mpr
      constructor
      · intro e
        rcases e with ⟨i, flag⟩ | bypassUnit
        · cases flag
          · simpa [pack, hsuma i] using hcap (f.a i) (ha i)
          · simpa [pack, hsumb i] using hcap (f.b i) (hb i)
        · simpa [pack, hsumh] using hcap f.h hh
      · intro i
        simp only [pack_a, pack_b, pack_bypass, xb]
        ring
    · intro j hj
      rw [← hobsH j hj]
      exact (hh j).1
    · exact (mem_chainHull_iff_profile D.c D.u D.v D.weights D.xa D.xb D.xh
        (fun j => D.observedH j = true) D.zh hweights
        (fun i => by dsimp [xb]; ring) hn).mp h
  · rintro ⟨hd, hp⟩
    exact (mem_chainHull_iff_profile D.c D.u D.v D.weights D.xa D.xb D.xh
      (fun j => D.observedH j = true) D.zh hd.1
      (fun i => by dsimp [xb]; ring) hd.2.2.1).mpr hp

end ReductionData

end
end Chain
end NetworkSimplex
