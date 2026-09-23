import Formal.UpperBounds

namespace ExactCounts

noncomputable section
open scoped BigOperators

/-- The union of the rational boxes with their retained code labels. -/
def LabeledBoxes {J : Type*} {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ) :
    Set (Visible n × Code p) :=
  {q | ∃ j, (∀ i k, (lo j i k : ℝ) ≤ q.1 i k ∧ q.1 i k ≤ (hi j i k : ℝ)) ∧
    q.2 = fun l => (label j l : ℝ)}

/-- The projection of the weighted box formulation is convex. -/
theorem convex_weightedBoxes {J : Type*} [Fintype J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ) :
    Convex ℝ {q : Visible n × Code p | ∃ w, WeightedBoxes n p lo hi label q.1 q.2 w} := by
  rintro x ⟨w, hw, hs, hb, hz⟩ y ⟨w', hw', hs', hb', hz'⟩ a b ha hbb hab
  refine ⟨fun j => a * w j + b * w' j, ?_, ?_, ?_, ?_⟩
  · intro j
    exact add_nonneg (mul_nonneg ha (hw j)) (mul_nonneg hbb (hw' j))
  · simp [Finset.sum_add_distrib, ← Finset.mul_sum, hs, hs', hab]
  · intro i k
    change (∑ j, (a * w j + b * w' j) * _) ≤ a * x.1 i k + b * y.1 i k ∧
      a * x.1 i k + b * y.1 i k ≤ ∑ j, (a * w j + b * w' j) * _
    simp only [add_mul, mul_assoc, Finset.sum_add_distrib, ← Finset.mul_sum]
    exact ⟨add_le_add (mul_le_mul_of_nonneg_left (hb i k).1 ha)
      (mul_le_mul_of_nonneg_left (hb' i k).1 hbb),
      add_le_add (mul_le_mul_of_nonneg_left (hb i k).2 ha)
      (mul_le_mul_of_nonneg_left (hb' i k).2 hbb)⟩
  · intro l
    change a * x.2 l + b * y.2 l = _
    simp [hz, hz', add_mul, mul_assoc, Finset.sum_add_distrib, ← Finset.mul_sum]

/-- A value between weighted endpoint sums can be allocated inside each interval.
The proof also covers zero total width and zero weights. -/
theorem weighted_interval_allocation {J : Type*} [Fintype J]
    (lo hi w : J → ℝ) (hbox : ∀ j, lo j ≤ hi j) (hw : ∀ j, 0 ≤ w j)
    (v : ℝ) (hv : (∑ j, w j * lo j) ≤ v ∧ v ≤ ∑ j, w j * hi j) :
    ∃ q : J → ℝ, (∀ j, lo j ≤ q j ∧ q j ≤ hi j) ∧ ∑ j, w j * q j = v := by
  let L := ∑ j, w j * lo j
  let H := ∑ j, w j * hi j
  have hLH : L ≤ H := Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hbox j) (hw j)
  change L ≤ v ∧ v ≤ H at hv
  by_cases hzero : H = L
  · refine ⟨lo, fun j => ⟨le_rfl, hbox j⟩, ?_⟩
    change L = v
    exact le_antisymm hv.1 (by simpa [hzero] using hv.2)
  · have hpos : 0 < H - L := sub_pos.mpr (lt_of_le_of_ne hLH (Ne.symm hzero))
    let t := (v - L) / (H - L)
    have ht0 : 0 ≤ t := div_nonneg (sub_nonneg.mpr hv.1) hpos.le
    have ht1 : t ≤ 1 := (div_le_one hpos).mpr (sub_le_sub_right hv.2 L)
    have heq : t * (H - L) = v - L := div_mul_cancel₀ _ (ne_of_gt hpos)
    refine ⟨fun j => lo j + t * (hi j - lo j), ?_, ?_⟩
    · intro j
      have hdiff := sub_nonneg.mpr (hbox j)
      have hl := mul_nonneg ht0 hdiff
      have hu := mul_le_mul_of_nonneg_right ht1 hdiff
      constructor <;> nlinarith
    · calc
        (∑ j, w j * (lo j + t * (hi j - lo j))) =
            L + t * (H - L) := by
          simp only [L, H, mul_add, Finset.sum_add_distrib, mul_sub]
          rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
          congr 1
          apply Finset.sum_congr rfl
          intro j _
          ring
        _ = v := by linarith

/-- The retained weighted inequalities describe exactly the actual convex hull
of the labeled boxes, including empty index sets and degenerate boxes. -/
theorem weightedBoxes_iff_mem_convexHull {J : Type*} [Fintype J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k) (v : Visible n) (z : Code p) :
    (∃ w, WeightedBoxes n p lo hi label v z w) ↔
      (v, z) ∈ convexHull ℝ (LabeledBoxes lo hi label) := by
  classical
  constructor
  · rintro ⟨w, hw, hs, hb, hz⟩
    have hall (i : Fin n) (k : Fin 3) := weighted_interval_allocation
      (fun j => (lo j i k : ℝ)) (fun j => (hi j i k : ℝ)) w
      (fun j => by exact_mod_cast hbox j i k) hw (v i k) (hb i k)
    choose q hq hsum using hall
    let point : J → Visible n × Code p :=
      fun j => (fun i k => q i k j, fun l => (label j l : ℝ))
    have hmem (j : J) : point j ∈ LabeledBoxes lo hi label :=
      ⟨j, fun i k => hq i k j, rfl⟩
    have h := (convex_convexHull ℝ (LabeledBoxes lo hi label)).sum_mem
      (fun j (_ : j ∈ Finset.univ) => hw j) hs
      (fun j (_ : j ∈ Finset.univ) => subset_convexHull ℝ _ (hmem j))
    have heq : ∑ j, w j • point j = (v, z) := by
      apply Prod.ext
      · funext i k
        simpa [point, Finset.sum_apply, Prod.fst_sum, Prod.snd_sum] using hsum i k
      · funext l
        simpa [point, Finset.sum_apply, Prod.fst_sum, Prod.snd_sum] using (hz l).symm
    exact heq ▸ h
  · apply convexHull_min _ (convex_weightedBoxes lo hi label)
    rintro q ⟨j, hb, hz⟩
    exact ⟨_, hz ▸ weightedBoxes_single j q.1 hb⟩

/-- Explicit rational endpoints: one Boolean selects each box coordinate. -/
def labeledBoxVertex {J : Type*} {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (s : J × (Fin n → Fin 3 → Bool)) : Visible n × Code p :=
  (fun i k => if s.2 i k then (hi s.1 i k : ℝ) else (lo s.1 i k : ℝ),
    fun l => (label s.1 l : ℝ))

theorem labeledBoxVertex_rational {J : Type*} {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (s : J × (Fin n → Fin 3 → Bool)) :
    (∀ i k, ∃ r : ℚ, (labeledBoxVertex lo hi label s).1 i k = r) ∧
      ∀ l, ∃ r : ℚ, (labeledBoxVertex lo hi label s).2 l = r := by
  constructor
  · intro i k
    exact ⟨if s.2 i k then hi s.1 i k else lo s.1 i k, by
      simp only [labeledBoxVertex]; split <;> simp_all⟩
  · intro l
    exact ⟨label s.1 l, rfl⟩

theorem labeledBoxVertex_mem {J : Type*} {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k)
    (s : J × (Fin n → Fin 3 → Bool)) :
    labeledBoxVertex lo hi label s ∈ LabeledBoxes lo hi label := by
  refine ⟨s.1, ?_, rfl⟩
  intro i k
  have h : (lo s.1 i k : ℝ) ≤ hi s.1 i k := by exact_mod_cast hbox s.1 i k
  change _ ≤ (if s.2 i k then _ else _) ∧ (if s.2 i k then _ else _) ≤ _
  split
  · exact ⟨h, le_rfl⟩
  · exact ⟨le_rfl, h⟩

/-- Each labeled box is the convex hull of its rational endpoint vertices. -/
theorem labeledBoxes_subset_convexHull_vertices {J : Type*} {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k) :
    LabeledBoxes lo hi label ⊆ convexHull ℝ (Set.range (labeledBoxVertex lo hi label)) := by
  classical
  rintro q ⟨j, hq, hz⟩
  let corners : Set (Visible n) := Set.pi Set.univ fun i =>
    Set.pi Set.univ fun k => {(lo j i k : ℝ), (hi j i k : ℝ)}
  have hc : q.1 ∈ convexHull ℝ corners := by
    apply mem_convexHull_pi
    intro i _
    apply mem_convexHull_pi
    intro k _
    rw [convexHull_pair, segment_eq_Icc (by exact_mod_cast hbox j i k)]
    exact hq i k
  have hpair : q ∈ convexHull ℝ (corners ×ˢ {fun l => (label j l : ℝ)}) := by
    rw [convexHull_prod, convexHull_singleton]
    exact ⟨hc, hz⟩
  apply convexHull_mono _ hpair
  rintro x ⟨hx, hxl⟩
  have hx' : ∀ i k, x.1 i k = (lo j i k : ℝ) ∨ x.1 i k = (hi j i k : ℝ) := by
    simpa [corners, Set.mem_pi] using hx
  let bits : Fin n → Fin 3 → Bool := fun i k => decide (x.1 i k = (hi j i k : ℝ))
  refine ⟨(j, bits), ?_⟩
  apply Prod.ext
  · funext i k
    change (if bits i k then (hi j i k : ℝ) else (lo j i k : ℝ)) = x.1 i k
    by_cases h : x.1 i k = (hi j i k : ℝ)
    · simp [bits, h]
    · simp only [bits, h, decide_false, Bool.false_eq_true, ↓reduceIte]
      exact ((hx' i k).resolve_right h).symm
  · exact hxl.symm

/-- An explicit finite rational vertex representation of the complete labeled hull. -/
theorem labeledBoxes_convexHull_vertices {J : Type*} [Finite J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k) :
    (Set.range (labeledBoxVertex lo hi label)).Finite ∧
      convexHull ℝ (LabeledBoxes lo hi label) =
        convexHull ℝ (Set.range (labeledBoxVertex lo hi label)) := by
  refine ⟨Set.finite_range _, le_antisymm ?_ ?_⟩
  · exact convexHull_min (labeledBoxes_subset_convexHull_vertices lo hi label hbox)
      (convex_convexHull ℝ _)
  · apply convexHull_mono
    rintro _ ⟨s, rfl⟩
    exact labeledBoxVertex_mem lo hi label hbox s

/-- Distinct binary labels admit exactly the selected box on every binary slice. -/
theorem weightedBoxes_binary_slice {J : Type*} [Fintype J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hinj : Function.Injective label) (hlabel : ∀ j l, label j l = 0 ∨ label j l = 1)
    (v : Visible n) (z : Code p) (hbin : z ∈ BinaryCodes p) :
    (∃ w, WeightedBoxes n p lo hi label v z w) ↔
      ∃ j, z = (fun l => (label j l : ℝ)) ∧
        ∀ i k, (lo j i k : ℝ) ≤ v i k ∧ v i k ≤ (hi j i k : ℝ) := by
  classical
  constructor
  · rintro ⟨w, hw, hs, hb, hz⟩
    have hex : ∃ j, 0 < w j := by
      by_contra! hn
      have : ∑ j, w j ≤ 0 := Finset.sum_nonpos fun j _ => hn j
      linarith
    obtain ⟨j, hj⟩ := hex
    have hjlabel := binary_weight_support label hlabel hw hs hz hbin hj
    have hzero (t : J) (ht : t ≠ j) : w t = 0 := by
      by_contra hne
      have htpos : 0 < w t := lt_of_le_of_ne (hw t) (Ne.symm hne)
      have htlabel := binary_weight_support label hlabel hw hs hz hbin htpos
      apply ht
      apply hinj
      funext l
      exact_mod_cast (htlabel l).trans (hjlabel l).symm
    have hwj : w j = 1 := by
      rw [Finset.sum_eq_single j (fun t _ ht => hzero t ht) (by simp)] at hs
      exact hs
    have hwform : w = fun t => if t = j then 1 else 0 := by
      funext t
      by_cases ht : t = j
      · simp [ht, hwj]
      · simp [ht, hzero t ht]
    refine ⟨j, funext fun l => (hjlabel l).symm, ?_⟩
    simpa [hwform] using hb
  · rintro ⟨j, rfl, hb⟩
    exact ⟨_, weightedBoxes_single j v hb⟩

/-- The labeled rational box hull is compact, hence in particular closed. -/
theorem isCompact_labeledBoxes_convexHull {J : Type*} [Finite J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k) :
    IsCompact (convexHull ℝ (LabeledBoxes lo hi label)) := by
  obtain ⟨hfinite, heq⟩ := labeledBoxes_convexHull_vertices lo hi label hbox
  rw [heq]
  exact hfinite.isCompact_convexHull ℝ

/-- The geometric hull itself has precisely the claimed binary slices. -/
theorem labeledBoxes_convexHull_binary_slice {J : Type*} [Finite J] {n p : ℕ}
    (lo hi : J → Fin n → Fin 3 → ℚ) (label : J → Fin p → ℚ)
    (hbox : ∀ j i k, lo j i k ≤ hi j i k)
    (hinj : Function.Injective label) (hlabel : ∀ j l, label j l = 0 ∨ label j l = 1)
    (v : Visible n) (z : Code p) (hbin : z ∈ BinaryCodes p) :
    (v, z) ∈ convexHull ℝ (LabeledBoxes lo hi label) ↔
      ∃ j, z = (fun l => (label j l : ℝ)) ∧
        ∀ i k, (lo j i k : ℝ) ≤ v i k ∧ v i k ≤ (hi j i k : ℝ) := by
  let := Fintype.ofFinite J
  rw [← weightedBoxes_iff_mem_convexHull lo hi label hbox]
  exact weightedBoxes_binary_slice lo hi label hinj hlabel v z hbin

/-- All endpoints in the concrete three-box construction are correctly ordered. -/
theorem boxLo_le_boxHi (j k : Fin 3) : boxLo j k ≤ boxHi j k := by
  fin_cases j <;> fin_cases k <;> norm_num [boxLo, boxHi, boxL, boxD]

/-- The one-coordinate formulation is precisely the labeled three-box hull. -/
theorem one_coordinate_weighted_hull (v : Visible 1) (z : Code 1) :
    (∃ w, WeightedBoxes 1 1 (fun j _ k => boxLo j k) (fun j _ k => boxHi j k)
      (fun j _ => (j.val : ℚ)) v z w) ↔
    (v, z) ∈ convexHull ℝ (LabeledBoxes (fun j _ k => boxLo j k)
      (fun j _ k => boxHi j k) (fun j _ => (j.val : ℚ))) :=
  weightedBoxes_iff_mem_convexHull _ _ _ (fun j _ k => boxLo_le_boxHi j k) v z

/-- The actual binary formulation projects exactly to the coded product-box hull. -/
theorem binarySystem_projection_iff_hull {n p : ℕ}
    (e : BoxLabels n ↪ BinaryLabels p) (v : Visible n) (z : Code p) :
    (∃ a, BinarySystem e (v, z, a)) ↔
      (v, z) ∈ convexHull ℝ (LabeledBoxes
        (fun j i k => boxLo (j i) k) (fun j i k => boxHi (j i) k)
        (fun j l => ((e j l).val : ℚ))) := by
  classical
  rw [← weightedBoxes_iff_mem_convexHull
    (fun j i k => boxLo (j i) k) (fun j i k => boxHi (j i) k)
    (fun j l => ((e j l).val : ℚ)) (fun j i k => boxLo_le_boxHi (j i) k)]
  constructor
  · rintro ⟨a, ha⟩
    exact ⟨_, ha⟩
  · rintro ⟨w, hw⟩
    refine ⟨fun a => w ((Fintype.equivFin (BoxLabels n)).symm a), ?_⟩
    simpa [BinarySystem] using hw

/-- Every feasible binary slice of the concrete construction is its selected
product box, and every point of that product box is feasible. -/
theorem binarySystem_exact_slice {n p : ℕ}
    (e : BoxLabels n ↪ BinaryLabels p) (v : Visible n) (z : Code p)
    (hz : z ∈ BinaryCodes p) :
    (∃ a, BinarySystem e (v, z, a)) ↔
      ∃ j, z = (fun l => ((e j l).val : ℝ)) ∧ ∀ i, InBox (j i) (v i) := by
  rw [binarySystem_projection_iff_hull]
  have hinj : Function.Injective (fun j l => ((e j l).val : ℚ)) := by
    intro j t h
    apply e.injective
    funext l
    apply Fin.ext
    have heq : ((e j l).val : ℚ) = ((e t l).val : ℚ) := congrFun h l
    exact_mod_cast heq
  have hlabel : ∀ j l, ((e j l).val : ℚ) = 0 ∨ ((e j l).val : ℚ) = 1 := by
    intro j l
    have h := (e j l).isLt
    have : (e j l).val = 0 ∨ (e j l).val = 1 := by omega
    rcases this with h | h <;> simp [h]
  simpa [InBox] using labeledBoxes_convexHull_binary_slice
    (fun j i k => boxLo (j i) k) (fun j i k => boxHi (j i) k)
    (fun j l => ((e j l).val : ℚ)) (fun j i k => boxLo_le_boxHi (j i) k)
    hinj hlabel v z hz

/-- With binary labels, integer code constraints already force binary values. -/
theorem weightedBoxes_integer_code_binary {J : Type*} [Fintype J] {n p : ℕ}
    {lo hi : J → Fin n → Fin 3 → ℚ} {label : J → Fin p → ℚ}
    (hlabel : ∀ j l, label j l = 0 ∨ label j l = 1)
    {v : Visible n} {z : Code p} {w : J → ℝ}
    (hw : WeightedBoxes n p lo hi label v z w) (hz : z ∈ IntegerCodes p) :
    z ∈ BinaryCodes p := by
  obtain ⟨k, rfl⟩ := hz
  intro l
  have hlo : (0 : ℝ) ≤ ∑ j, w j * (label j l : ℝ) := by
    apply Finset.sum_nonneg
    intro j _
    rcases hlabel j l with h | h <;> simp [h, hw.1]
  have hhi : (∑ j, w j * (label j l : ℝ)) ≤ 1 := by
    rw [← hw.2.1]
    apply Finset.sum_le_sum
    intro j _
    rcases hlabel j l with h | h <;> simp [h, hw.1]
  rw [← hw.2.2.2 l] at hlo hhi
  change (0 : ℝ) ≤ (k l : ℝ) at hlo
  change (k l : ℝ) ≤ 1 at hhi
  have hk0 : (0 : ℤ) ≤ k l := by exact_mod_cast hlo
  have hk1 : k l ≤ (1 : ℤ) := by exact_mod_cast hhi
  have hk : k l = 0 ∨ k l = 1 := by omega
  rcases hk with hk | hk <;> simp [hk]

/-- Imposing general integrality on the concrete binary formulation produces
exactly the same selected product boxes. -/
theorem binarySystem_exact_integer_slice {n p : ℕ}
    (e : BoxLabels n ↪ BinaryLabels p) (v : Visible n) (z : Code p)
    (hz : z ∈ IntegerCodes p) :
    (∃ a, BinarySystem e (v, z, a)) ↔
      ∃ j, z = (fun l => ((e j l).val : ℝ)) ∧ ∀ i, InBox (j i) (v i) := by
  have hlabel : ∀ j l, ((e j l).val : ℚ) = 0 ∨ ((e j l).val : ℚ) = 1 := by
    intro j l
    have h := (e j l).isLt
    have : (e j l).val = 0 ∨ (e j l).val = 1 := by omega
    rcases this with h | h <;> simp [h]
  constructor
  · rintro ⟨a, ha⟩
    have hb := weightedBoxes_integer_code_binary hlabel ha hz
    exact (binarySystem_exact_slice e v z hb).mp ⟨a, ha⟩
  · rintro ⟨j, rfl, hj⟩
    have hb : (fun l => ((e j l).val : ℝ)) ∈ BinaryCodes p := by
      intro l
      rcases hlabel j l with h | h
      · left
        change ((e j l).val : ℝ) = 0
        exact_mod_cast h
      · right
        change ((e j l).val : ℝ) = 1
        exact_mod_cast h
    exact (binarySystem_exact_slice e v _ hb).mpr ⟨j, rfl, hj⟩

end
end ExactCounts
