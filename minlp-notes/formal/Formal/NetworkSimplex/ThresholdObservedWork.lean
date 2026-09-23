import Formal.NetworkSimplex.ThresholdGrouping
import Formal.NetworkSimplex.ThresholdMergeRational

/-! Executable observed-label marking and original-simplex bookkeeping. The
word-operation ledger includes array initialization, input scans and output lists. -/
namespace NetworkSimplex
open ThresholdGrouping
open scoped BigOperators

def observedLabelRows {m : ℕ} (labels : List (Fin m)) : List (IndexedRow m Unit) :=
  labels.map fun j => ⟨j, 0, ()⟩

def observedLabels {m : ℕ} (labels : List (Fin m)) : List (Fin m) :=
  let marked := group (observedLabelRows labels)
  (List.finRange m).filter fun j => (marked.table.get j).isSome

theorem mem_observedLabels {m : ℕ} (labels : List (Fin m)) (j : Fin m) :
    j ∈ observedLabels labels ↔ j ∈ labels := by
  simp only [observedLabels, List.mem_filter, List.mem_finRange, true_and]
  constructor
  · intro h
    obtain ⟨r, hr⟩ := Option.isSome_iff_exists.mp h
    obtain ⟨hm, hk, _⟩ := group_minimum (observedLabelRows labels) j hr
    obtain ⟨k, hmem, rfl⟩ := List.mem_map.mp hm
    simpa only [← hk] using hmem
  · intro h
    cases he : (group (observedLabelRows labels)).table.get j with
    | none =>
      have hh := (group_none_iff _ j).mp he ⟨j, 0, ()⟩ (List.mem_map.mpr ⟨j,h,rfl⟩)
      exact (hh rfl).elim
    | some r => rfl

theorem observedLabels_nodup {m : ℕ} (labels : List (Fin m)) :
    (observedLabels labels).Nodup := (List.nodup_finRange m).filter _

theorem observedLabels_set {m : ℕ} (labels : List (Fin m)) :
    (observedLabels labels).toFinset = labels.toFinset := by
  ext j
  simp [mem_observedLabels]

theorem observedLabels_length {m : ℕ} (labels : List (Fin m)) :
    (observedLabels labels).length = labels.toFinset.card := by
  rw [← observedLabels_set, List.toFinset_card_of_nodup (observedLabels_nodup labels)]

theorem observedLabels_length_le {m : ℕ} (labels : List (Fin m)) :
    (observedLabels labels).length ≤ m := by
  exact (List.length_filter_le _ _).trans_eq List.length_finRange

/-- One addition, comparison and Boolean conjunction per stored weight. -/
def weightScan : List ℚ → ℚ × Bool × ℕ
  | [] => (0, true, 0)
  | q :: qs =>
      let tail := weightScan qs
      (q + tail.1, decide (0 ≤ q) && tail.2.1, 3 + tail.2.2)

theorem weightScan_sum (qs : List ℚ) : (weightScan qs).1 = qs.sum := by
  induction qs with
  | nil => rfl
  | cons q qs ih => simp [weightScan, ih]

theorem weightScan_nonneg (qs : List ℚ) :
    (weightScan qs).2.1 = true ↔ ∀ q ∈ qs, 0 ≤ q := by
  induction qs with
  | nil => simp [weightScan]
  | cons q qs ih => simp [weightScan, ih]

theorem weightScan_work (qs : List ℚ) : (weightScan qs).2.2 = 3 * qs.length := by
  induction qs with
  | nil => rfl
  | cons q qs ih => simp [weightScan, ih]; omega

structure ObservedPreprocess (m : ℕ) where
  active : List (Fin m)
  weights : List ℚ
  activeWeights : List ℚ
  originalResidual : ℚ
  mergedResidual : ℚ
  simplex : Bool
  work : ℕ

/-- Mark sparse observation labels in an indexed array, then scan the original
weights once. Both the original residual and merged residual are retained. -/
def preprocessObserved {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    ObservedPreprocess m :=
  let marked := group (observedLabelRows labels)
  let active := (List.finRange m).filter fun j => (marked.table.get j).isSome
  let weights := List.ofFn y
  let totals := weightScan weights
  let activeWeights := active.map y
  let activeTotals := weightScan activeWeights
  ⟨active, weights, activeWeights, 1 - totals.1, 1 - activeTotals.1,
    totals.2.1 && decide (totals.1 ≤ 1),
    2 * labels.length + marked.accesses + marked.comparisons + 3 * m +
      totals.2.2 + active.length + activeTotals.2.2 + 4⟩

theorem preprocessObserved_active {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    (preprocessObserved labels y).active = observedLabels labels := rfl

theorem preprocessObserved_simplex {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    (preprocessObserved labels y).simplex = true ↔ OriginalSimplex (fun j => (y j : ℝ)) := by
  simp only [preprocessObserved, Bool.and_eq_true, decide_eq_true_eq,
    weightScan_nonneg, weightScan_sum, List.sum_ofFn, List.mem_ofFn,
    forall_exists_index, forall_apply_eq_imp_iff]
  unfold OriginalSimplex
  dsimp only
  constructor
  · rintro ⟨hn, hs⟩
    constructor
    · intro j; exact_mod_cast hn j
    · exact_mod_cast hs
  · rintro ⟨hn, hs⟩
    constructor
    · intro j; exact_mod_cast hn j
    · exact_mod_cast hs

theorem preprocessObserved_residual {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    (preprocessObserved labels y).originalResidual = 1 - ∑ j, y j := by
  simp [preprocessObserved, weightScan_sum, List.sum_ofFn]

theorem preprocessObserved_mergedResidual {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    (preprocessObserved labels y).mergedResidual = 1 - ∑ j ∈ labels.toFinset, y j := by
  change 1 - (weightScan ((observedLabels labels).map y)).1 = _
  rw [weightScan_sum, ← List.sum_toFinset _ (observedLabels_nodup labels), observedLabels_set]

theorem preprocessObserved_work {m : ℕ} (labels : List (Fin m)) (y : Fin m → ℚ) :
    (preprocessObserved labels y).work ≤ 11 * m + 5 * labels.length + 4 := by
  have hg := group_cost (observedLabelRows labels)
  have ha := observedLabels_length_le labels
  have hlen : (observedLabelRows labels).length = labels.length := by
    simp [observedLabelRows]
  rw [hlen] at hg
  change 2 * labels.length + (group (observedLabelRows labels)).accesses +
    (group (observedLabelRows labels)).comparisons + 3 * m +
      (weightScan (List.ofFn y)).2.2 + (observedLabels labels).length +
      (weightScan ((observedLabels labels).map y)).2.2 + 4 ≤ _
  rw [weightScan_work, weightScan_work, List.length_ofFn, List.length_map, hg.2]
  omega

/-- The fixed-observed-label procedure receives the materialized preprocessing
result. Its own recorded charge is added to the scans actually performed here. -/
def withObservedPreprocess {m : ℕ} {α : Type*} (labels : List (Fin m))
    (y : Fin m → ℚ) (core : ObservedPreprocess m → α × ℕ) : α × ℕ :=
  let prepared := preprocessObserved labels y
  let result := core prepared
  (result.1, prepared.work + result.2)

theorem withObservedPreprocess_value {m : ℕ} {α : Type*} (labels : List (Fin m))
    (y : Fin m → ℚ) (core : ObservedPreprocess m → α × ℕ) :
    (withObservedPreprocess labels y core).1 = (core (preprocessObserved labels y)).1 := rfl

theorem withObservedPreprocess_work {m L C overhead : ℕ} {α : Type*}
    (labels : List (Fin m)) (y : Fin m → ℚ) (core : ObservedPreprocess m → α × ℕ)
    (hcore : (core (preprocessObserved labels y)).2 ≤
      C * (labels.toFinset.card + 1) * (L + 1) + overhead) :
    (withObservedPreprocess labels y core).2 ≤
      11 * m + 5 * labels.length + 4 +
        C * (labels.toFinset.card + 1) * (L + 1) + overhead := by
  have hp := preprocessObserved_work labels y
  change (preprocessObserved labels y).work + (core (preprocessObserved labels y)).2 ≤ _
  omega

/-- All original weights are stored once. The merged mass is cached before
normalizing the common flow, so it is not recomputed at each output coordinate. -/
structure CompactMergedOutput where
  weights : List ℚ
  commonFlow : List ℚ
  work : ℕ

def emitCompactMerged {states arcs : ℕ} (w : Fin states → ℚ) (W : ℚ)
    (f base : Fin arcs → ℚ) : CompactMergedOutput :=
  let weights := List.ofFn w
  let common := if W = 0 then List.ofFn base else List.ofFn fun e => f e / W
  ⟨weights, common, weights.length + common.length + (if W = 0 then 0 else common.length) + 1⟩

theorem emitCompactMerged_weights {states arcs : ℕ} (w : Fin states → ℚ) (W : ℚ)
    (f base : Fin arcs → ℚ) : (emitCompactMerged w W f base).weights = List.ofFn w := rfl

theorem emitCompactMerged_common {states arcs : ℕ} (w : Fin states → ℚ) (W : ℚ)
    (f base : Fin arcs → ℚ) :
    (emitCompactMerged w W f base).commonFlow =
      List.ofFn (fun e => if W = 0 then base e else f e / W) := by
  by_cases h : W = 0 <;> simp [emitCompactMerged, h]

theorem emitCompactMerged_size {states arcs : ℕ} (w : Fin states → ℚ) (W : ℚ)
    (f base : Fin arcs → ℚ) :
    (emitCompactMerged w W f base).weights.length +
      (emitCompactMerged w W f base).commonFlow.length = states + arcs := by
  rw [emitCompactMerged_weights, emitCompactMerged_common]
  simp

theorem emitCompactMerged_work {states arcs : ℕ} (w : Fin states → ℚ) (W : ℚ)
    (f base : Fin arcs → ℚ) :
    (emitCompactMerged w W f base).work ≤ states + 2 * arcs + 1 := by
  by_cases h : W = 0 <;> simp [emitCompactMerged, h] <;> omega

/-- The emitted common flow is exactly the rational proportional-refinement
flow, including the zero-weight case. Original weights are left intact. -/
theorem emitCompactMerged_exact {m arcs : ℕ} (J : Finset (Fin m))
    (w : Fin (m + 1) → ℚ) (f : Option {j // j ∈ J} → Fin arcs → ℚ)
    (base : Fin arcs → ℚ) :
    (emitCompactMerged w (groupSum (observedGroup J) w none) (f none) base).commonFlow =
      List.ofFn (commonMergedFlow (observedGroup J) w f base none) := by
  rw [emitCompactMerged_common]
  rfl

/-- Compact chain output keeps original weights, observed flows and one common
flow. Expanding every original state/arc pair is a distinct, larger output. -/
theorem compact_chain_output_size (m a L : ℕ) :
    (m + 1) + a * (2 * L + 1) + (2 * L + 1) =
      (m + 1) + (a + 1) * (2 * L + 1) := by ring

end NetworkSimplex
