import Formal.NetworkSimplex.ThresholdStateRecovery
import Formal.ReciprocalAnchor.ManyRationalSize

/-! Explicit rational graph decompositions with at most one point per simplex state. -/
namespace NetworkSimplex.Chain
open scoped BigOperators

variable {L N : ℕ}

/-- A cached normalized flow; the simplex vertex is stored by its index separately. -/
structure NormalizedState (L : ℕ) where
  a : Vector ℚ L
  b : Vector ℚ L
  h : ℚ
  work : ℕ

/-- One zero test, then one division per flow coordinate in the nonzero branch.
The zero branch is the feasible all-bypass flow. -/
def normalizeState (f : RationalStateFlows L N) (weights : Fin N → ℚ) (j : Fin N) :
    NormalizedState L :=
  if weights j = 0 then
    ⟨Vector.replicate L 0, Vector.replicate L 0, 1, 1⟩
  else
    ⟨Vector.ofFn (fun i => (f.a.get i).get j / weights j),
      Vector.ofFn (fun i => (f.b.get i).get j / weights j),
      f.h.get j / weights j, 2 * L + 2⟩

def normalizeStates (f : RationalStateFlows L N) (weights : Fin N → ℚ) :
    Vector (NormalizedState L) N := Vector.ofFn (normalizeState f weights)

def normalizationWork (f : RationalStateFlows L N) (weights : Fin N → ℚ) : ℕ :=
  ∑ j, ((normalizeStates f weights).get j).work

theorem normalizeState_charge (f : RationalStateFlows L N) (weights : Fin N → ℚ)
    (j : Fin N) : (normalizeState f weights j).work ≤ 2 * L + 2 := by
  unfold normalizeState
  split_ifs <;> simp

theorem normalizationWork_bound (f : RationalStateFlows L N) (weights : Fin N → ℚ) :
    normalizationWork f weights ≤ N * (2 * L + 2) := by
  calc
    _ ≤ ∑ _j : Fin N, (2 * L + 2) := by
      unfold normalizationWork
      apply Finset.sum_le_sum
      intro j _
      simpa [normalizeStates] using normalizeState_charge f weights j
    _ = _ := by simp


/-- Rational flow lookup; only the nonzero vertex index need be stored. -/
def NormalizedState.rationalFlow (g : NormalizedState L) : ChainArc L → ℚ
  | Sum.inl (i, false) => g.a.get i
  | Sum.inl (i, true) => g.b.get i
  | Sum.inr _ => g.h

def NormalizedState.rationalProduct (g : NormalizedState L) (j : Fin N)
    (o : ChainArc L × Fin N) : ℚ := if o.2 = j then g.rationalFlow o.1 else 0

noncomputable def NormalizedState.flow (g : NormalizedState L) : ChainArc L → ℝ :=
  pack (fun i => (g.a.get i : ℝ)) (fun i => (g.b.get i : ℝ)) (g.h : ℝ)

noncomputable def rawStateFlow (f : RationalStateFlows L N) (j : Fin N) : ChainArc L → ℝ :=
  pack (fun i => f.toReal.a i j) (fun i => f.toReal.b i j) (f.toReal.h j)

noncomputable def normalizedGraphPoint (f : RationalStateFlows L N) (weights : Fin N → ℚ)
    (c : Fin L → Fin N → StateClass) (observedH : Fin N → Prop) (j : Fin N) :
    Point (ChainArc L) (Fin N) (Observation c observedH) :=
  let x := ((normalizeStates f weights).get j).flow
  (x, (fun k => if k = j then 1 else 0,
    fun o => x o.val.1 * (if o.val.2 = j then 1 else 0)))


@[simp] theorem rationalFlow_cast (g : NormalizedState L) (e : ChainArc L) :
    (g.rationalFlow e : ℝ) = g.flow e := by
  rcases e with ⟨i, flag⟩ | bypassUnit
  · cases flag <;> rfl
  · rfl

/-- Every observed product is an executable rational lookup in the compressed output. -/
theorem normalizedGraphPoint_product_cast (f : RationalStateFlows L N)
    (weights : Fin N → ℚ) (c : Fin L → Fin N → StateClass) (observedH : Fin N → Prop)
    (j : Fin N) (o : Observation c observedH) :
    (((normalizeStates f weights).get j).rationalProduct j o.val : ℝ) =
      (normalizedGraphPoint f weights c observedH j).2.2 o := by
  simp only [NormalizedState.rationalProduct, normalizedGraphPoint]
  split_ifs <;> simp

private theorem normalized_flow_zero (f : RationalStateFlows L N) (weights : Fin N → ℚ)
    (j : Fin N) (hj : weights j = 0) :
    ((normalizeStates f weights).get j).flow = pack (fun _ => 0) (fun _ => 0) 1 := by
  funext e
  rcases e with ⟨i, flag⟩ | u
  · cases flag <;> simp [normalizeStates, normalizeState, hj, NormalizedState.flow, pack]
  · simp [normalizeStates, normalizeState, hj, NormalizedState.flow, pack]

private theorem normalized_flow_nonzero (f : RationalStateFlows L N) (weights : Fin N → ℚ)
    (j : Fin N) (hj : weights j ≠ 0) :
    ((normalizeStates f weights).get j).flow = (weights j : ℝ)⁻¹ • rawStateFlow f j := by
  funext e
  rcases e with ⟨i, flag⟩ | u
  · cases flag <;>
      simp [normalizeStates, normalizeState, hj, NormalizedState.flow, rawStateFlow,
        RationalStateFlows.toReal, pack, div_eq_mul_inv, mul_comm]
  · simp [normalizeStates, normalizeState, hj, NormalizedState.flow, rawStateFlow,
      RationalStateFlows.toReal, pack, div_eq_mul_inv, mul_comm]

variable (c : Fin L → Fin N → StateClass) (u v : Fin L → Fin N → ℝ)
    (weights : Fin N → ℚ) (xa xb : Fin L → ℝ) (xh : ℝ)
    (observedH : Fin N → Prop) (zh : Fin N → ℝ) (f : RationalStateFlows L N)

private theorem rawStateFlow_valid
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal)
    (j : Fin N) : Flow (incidence L) (demand L) (fun _ => 1) (weights j) (rawStateFlow f j) := by
  obtain ⟨ha, hb, hh, hbalance, _⟩ := hf
  apply (flow_iff L _ _).mpr
  constructor
  · intro e
    rcases e with ⟨i, flag⟩ | bypassUnit
    · cases flag
      · exact ha i j
      · exact hb i j
    · exact hh j
  · exact fun i => hbalance i j

private theorem normalized_flow_valid
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal)
    (j : Fin N) :
    Flow (incidence L) (demand L) (fun _ => 1) 1
      ((normalizeStates f weights).get j).flow := by
  by_cases hj : weights j = 0
  · rw [normalized_flow_zero f weights j hj]
    apply (flow_iff L _ _).mpr
    constructor
    · intro e
      rcases e with ⟨i, flag⟩ | bypassUnit
      · cases flag <;> norm_num [pack]
      · norm_num [pack]
    · simp
  · rw [normalized_flow_nonzero f weights j hj]
    have hnonneg : 0 ≤ (weights j : ℝ) := (hf.2.2.1 j).1.trans (hf.2.2.1 j).2
    have hne : (weights j : ℝ) ≠ 0 := by exact_mod_cast hj
    simpa [hne] using flow_smul (rawStateFlow_valid c u v weights xa xb xh observedH zh f hf j)
      (inv_nonneg.mpr hnonneg)

private theorem weighted_normalized_flow
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal)
    (j : Fin N) :
    (weights j : ℝ) • ((normalizeStates f weights).get j).flow = rawStateFlow f j := by
  by_cases hj : weights j = 0
  · have hfzero : rawStateFlow f j = 0 :=
      (flow_zero_iff (incidence L) (demand L) (fun _ => 1) _).mp
        (by simpa [hj] using rawStateFlow_valid c u v weights xa xb xh observedH zh f hf j)
    simp [hj, hfzero]
  · rw [normalized_flow_nonzero f weights j hj]
    have hne : (weights j : ℝ) ≠ 0 := by exact_mod_cast hj
    simp [smul_smul, hne]

/-- Every returned point belongs to the original sparse bilinear graph, also at zero weight. -/
theorem normalizedGraphPoint_mem
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal)
    (j : Fin N) : normalizedGraphPoint f weights c observedH j ∈ chainGraph c observedH := by
  refine ⟨⟨?_, ?_⟩, normalized_flow_valid c u v weights xa xb xh observedH zh f hf j, ?_⟩
  · intro k
    simp only [normalizedGraphPoint]
    split_ifs <;> norm_num
  · simp [normalizedGraphPoint]
  · intro o
    rfl

/-- The rational flows and implicit simplex vertices reproduce every input coordinate. -/
theorem normalizedGraphPoint_sum
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal) :
    ∑ j, (weights j : ℝ) • normalizedGraphPoint f weights c observedH j =
      chainPoint c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh := by
  have hw := weighted_normalized_flow c u v weights xa xb xh observedH zh f hf
  obtain ⟨_, _, _, _, hsuma, hsumb, hsumh, hobsA, hobsB, hobsH⟩ := hf
  apply Prod.ext
  · simp only [Prod.fst_sum, Prod.smul_fst, normalizedGraphPoint, hw]
    funext e
    rcases e with ⟨i, flag⟩ | bypassUnit
    · cases flag
      · simpa [rawStateFlow, chainPoint, pack] using hsuma i
      · simpa [rawStateFlow, chainPoint, pack] using hsumb i
    · simpa [rawStateFlow, chainPoint, pack] using hsumh
  · apply Prod.ext
    · funext j
      simp only [Prod.snd_sum, Prod.fst_sum, Prod.smul_snd, Prod.smul_fst,
        Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
      simp [normalizedGraphPoint, chainPoint, mul_ite]
    · funext o
      simp only [Prod.snd_sum, Prod.smul_snd, Finset.sum_apply, Pi.smul_apply,
        smul_eq_mul, normalizedGraphPoint, mul_ite, mul_one, mul_zero]
      have he := congrFun (hw o.val.2) o.val.1
      have hobs : rawStateFlow f o.val.2 o.val.1 =
          (chainPoint c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh).2.2 o := by
        rcases o with ⟨⟨e, j⟩, hselected⟩
        rcases e with ⟨i, flag⟩ | bypassUnit
        · cases flag
          · exact hobsA i j hselected
          · exact hobsB i j hselected
        · exact hobsH j hselected
      simpa using he.trans hobs

/-- At most `N` graph points, with explicit rational cached flow coordinates. -/
theorem rational_chain_decomposition
    (hf : ValidStateFlows c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh f.toReal)
    (hweights : (∑ j, weights j) = 1) :
    (∀ j, normalizedGraphPoint f weights c observedH j ∈ chainGraph c observedH) ∧
    Simplex (fun j => (weights j : ℝ)) ∧
    (∑ j, (weights j : ℝ) • normalizedGraphPoint f weights c observedH j =
      chainPoint c u v (fun j => (weights j : ℝ)) xa xb xh observedH zh) ∧
    Fintype.card (Fin N) = N := by
  refine ⟨normalizedGraphPoint_mem c u v weights xa xb xh observedH zh f hf, ⟨?_, ?_⟩,
    normalizedGraphPoint_sum c u v weights xa xb xh observedH zh f hf, Fintype.card_fin N⟩
  · intro j
    exact (hf.2.2.1 j).1.trans (hf.2.2.1 j).2
  · change (∑ j, (weights j : ℝ)) = 1
    exact_mod_cast hweights

open ReciprocalAnchor

/-- Reduced numerators and denominators of the actual normalized flow coordinates. -/
theorem normalizeState_bits {f : RationalStateFlows L N} {weights : Fin N → ℚ} {B : ℕ}
    (ha : ∀ i j, RationalBits ((f.a.get i).get j) B)
    (hb : ∀ i j, RationalBits ((f.b.get i).get j) B)
    (hh : ∀ j, RationalBits (f.h.get j) B)
    (hw : ∀ j, RationalBits (weights j) B) (j : Fin N) :
    (∀ i, RationalBits ((normalizeState f weights j).a.get i) (2 * B + 1)) ∧
    (∀ i, RationalBits ((normalizeState f weights j).b.get i) (2 * B + 1)) ∧
    RationalBits (normalizeState f weights j).h (2 * B + 1) := by
  unfold normalizeState
  split_ifs
  · simp only [Vector.get_replicate]
    exact ⟨fun _ => rationalBits_mono rationalBits_zero (by omega),
      fun _ => rationalBits_mono rationalBits_zero (by omega),
      rationalBits_mono rationalBits_one (by omega)⟩
  · simp only [Vector.get_ofFn]
    exact ⟨fun i => rationalBits_mono (rationalBits_div (ha i j) (hw j)) (by omega),
      fun i => rationalBits_mono (rationalBits_div (hb i j) (hw j)) (by omega),
      rationalBits_mono (rationalBits_div (hh j) (hw j)) (by omega)⟩


/-- The product coordinates require no larger fractions than the cached flow coordinates. -/
theorem normalized_products_bits {f : RationalStateFlows L N} {weights : Fin N → ℚ} {B : ℕ}
    (ha : ∀ i j, RationalBits ((f.a.get i).get j) B)
    (hb : ∀ i j, RationalBits ((f.b.get i).get j) B)
    (hh : ∀ j, RationalBits (f.h.get j) B)
    (hw : ∀ j, RationalBits (weights j) B) (j : Fin N) (o : ChainArc L × Fin N) :
    RationalBits (((normalizeStates f weights).get j).rationalProduct j o) (2 * B + 1) := by
  have hg := normalizeState_bits ha hb hh hw j
  simp only [NormalizedState.rationalProduct, normalizeStates, Vector.get_ofFn]
  split_ifs
  · rcases o.1 with ⟨i, flag⟩ | bypassUnit
    · cases flag
      · exact hg.1 i
      · exact hg.2.1 i
    · exact hg.2.2
  · exact rationalBits_mono rationalBits_zero (by omega)

end NetworkSimplex.Chain
