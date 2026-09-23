import Formal.NetworkSimplex.ThresholdObservedIndex

/-! Materialized observed-label compression. Every data field uses array lookup;
the merged residual is computed once by observed-label preprocessing. -/
namespace NetworkSimplex
open scoped BigOperators
open ThresholdGrouping

/-- Marking and scanning produces the same increasing order as the mathematical index. -/
theorem observedLabels_eq_sort {m : ℕ} (labels : List (Fin m)) :
    observedLabels labels = labels.toFinset.sort := by
  apply ((List.sortedLT_finRange m).pairwise.filter _).sortedLT.eq_of_mem_iff
    labels.toFinset.sortedLT_sort
  intro j
  change j ∈ observedLabels labels ↔ j ∈ labels.toFinset.sort
  simp only [mem_observedLabels, Finset.mem_sort, List.mem_toFinset]

/-- The sorted labels are converted to a packed array once. -/
def observedVector {m : ℕ} (labels : List (Fin m)) : Vector (Fin m) labels.toFinset.card :=
  ⟨(observedLabels labels).toArray, by simp [observedLabels_length]⟩

theorem observedVector_get {m : ℕ} (labels : List (Fin m)) (j : Fin labels.toFinset.card) :
    (observedVector labels).get j = (observedIndex labels.toFinset j).val := by
  change (observedLabels labels)[j.val]'_ = _
  simp only [observedLabels_eq_sort]
  rfl

/-- Sparse reverse-index rows are generated from the cached forward array. -/
@[inline] def observedRankRows {m a : ℕ} (active : Vector (Fin m) a) :
    List (IndexedRow m (Fin a)) :=
  (active.mapFinIdx fun i v hi => ⟨v, 0, ⟨i, hi⟩⟩).toList

theorem observedRankRows_eq {m a : ℕ} (active : Vector (Fin m) a) :
    observedRankRows active = List.ofFn fun j => ⟨active.get j, 0, j⟩ := by
  apply List.ext_getElem
  · simp [observedRankRows]
  · intro i hi hi'
    simp [observedRankRows, Vector.get, Vector.mapFinIdx]

/-- Map a cached label array and prepend its residual entry. The runtime loops
use array sizes, so no finite-set cardinality computation is performed. -/
def observedField {m a : ℕ} {α : Type*} (active : Vector (Fin m) a)
    (residual : α) (f : Fin m → α) : Vector α (a + 1) :=
  ⟨#[residual] ++ active.toArray.map f, by simp [Nat.add_comm]⟩

@[simp] theorem observedField_get {m a : ℕ} {α : Type*} (active : Vector (Fin m) a)
    (residual : α) (f : Fin m → α) (j : Fin (a + 1)) :
    (observedField active residual f).get j =
      Fin.cases residual (fun k => f (active.get k)) j := by
  refine Fin.cases ?_ (fun k => ?_) j
  · change (#[residual] ++ active.toArray.map f)[0] = residual
    simp
  · change (#[residual] ++ active.toArray.map f)[k.val + 1] = f active.toArray[k.val]
    simp

/-- Constant-time reverse lookup after a single indexed grouping pass. -/
@[inline] def observedRanks {m a : ℕ} (active : Vector (Fin m) a) : Run m (Fin a) :=
  group (observedRankRows active)

theorem observedRanks_get {m : ℕ} (labels : List (Fin m))
    (j : Fin labels.toFinset.card) :
    ((observedRanks (observedVector labels)).table.get
      (observedVector labels |>.get j)).map IndexedRow.payload = some j := by
  let rows := observedRankRows (observedVector labels)
  have hm : (⟨(observedVector labels).get j, 0, j⟩ : IndexedRow m _) ∈ rows := by
    simp [rows, observedRankRows_eq, List.mem_ofFn]
  cases he : (group rows).table.get ((observedVector labels).get j) with
  | none =>
    exact False.elim ((group_none_iff rows _).mp he _ hm rfl)
  | some r =>
    obtain ⟨hr, hk, _⟩ := group_minimum rows _ he
    obtain ⟨k, hkr⟩ := List.mem_ofFn.mp (by simpa only [rows, observedRankRows_eq] using hr)
    have hkey : (observedVector labels).get k = (observedVector labels).get j := by
      rw [← hk, ← hkr]
    have heq : k = j := (observedIndex labels.toFinset).injective
      (Subtype.ext (by simpa only [observedVector_get] using hkey))
    subst k
    change ((group rows).table.get ((observedVector labels).get j)).map _ = _
    rw [he]
    rw [← hkr]
    rfl

theorem observedRanks_none {m : ℕ} (labels : List (Fin m)) (j : Fin m) :
    (observedRanks (observedVector labels)).table.get j = none ↔ j ∉ labels := by
  rw [observedRanks, group_none_iff]
  constructor
  · intro h hj
    let k := (observedIndex labels.toFinset).symm ⟨j, List.mem_toFinset.mpr hj⟩
    have he : (observedVector labels).get k = j := by
      rw [observedVector_get]
      exact congrArg Subtype.val ((observedIndex labels.toFinset).apply_symm_apply _)
    exact h ⟨(observedVector labels).get k, 0, k⟩
      (by simp [observedRankRows_eq, List.mem_ofFn]) he
  · intro hj r hr hk
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp (by simpa only [observedRankRows_eq] using hr)
    apply hj
    rw [← hk, observedVector_get]
    exact List.mem_toFinset.mp (observedIndex labels.toFinset k).property

namespace Chain.Threshold.RationalData

/-- A packed compressed instance. The label vector is retained to lift outputs
back to the original labels without sorting or searching again. -/
structure ObservedCache (m a L : ℕ) where
  labels : Vector (Fin m) a
  ranks : Table m (Fin a)
  classes : Vector (Vector StateClass (a + 1)) L
  aProducts : Vector (Vector ℚ (a + 1)) L
  bProducts : Vector (Vector ℚ (a + 1)) L
  weights : Vector ℚ (a + 1)
  aFlows : Vector ℚ L
  bypassFlow : ℚ
  bypassObserved : Vector Bool (a + 1)
  bypassProducts : Vector ℚ (a + 1)
  originalSimplex : Bool
  originalResidual : ℚ
  work : ℕ

/-- Once materialized, every numerical or pattern lookup uses a constant number
of indexed array reads. No sorting, summation or list indexing occurs here. -/
def ObservedCache.data {m a L : ℕ} (C : ObservedCache m a L) : RationalData a L where
  c i j := (C.classes.get i).get j
  u i j := (C.aProducts.get i).get j
  v i j := (C.bProducts.get i).get j
  weights := C.weights.get
  xa := C.aFlows.get
  xh := C.bypassFlow
  observedH := C.bypassObserved.get
  zh := C.bypassProducts.get

/-- Map an original state to its cached compressed atom with one indexed read.
Residual and unobserved states use atom zero. -/
def ObservedCache.atomIndex {m a L : ℕ} (C : ObservedCache m a L) :
    Fin (m + 1) → Fin (a + 1) :=
  Fin.cases 0 (fun j => ((C.ranks.get j).map IndexedRow.payload).elim 0 Fin.succ)

/-- Materialize all compressed fields using the sorted active-label array and
one cached residual. The word ledger counts indexing, field reads, writes and
loop steps; input rational values are copied without arithmetic. -/
def observedCache {m L : ℕ} (D : RationalData m L) (labels : List (Fin m)) :
    ObservedCache m labels.toFinset.card L :=
  let prepared := preprocessObserved labels (fun j => D.weights j.succ)
  let active : Vector (Fin m) labels.toFinset.card :=
    ⟨prepared.active.toArray, by simp [prepared, preprocessObserved_active, observedLabels_length]⟩
  let ranks := observedRanks active
  { labels := active
    ranks := ranks.table
    classes := Vector.ofFn fun i => observedField active .neither (fun j => D.c i j.succ)
    aProducts := Vector.ofFn fun i => observedField active 0 (fun j => D.u i j.succ)
    bProducts := Vector.ofFn fun i => observedField active 0 (fun j => D.v i j.succ)
    weights := observedField active prepared.mergedResidual (fun j => D.weights j.succ)
    aFlows := Vector.ofFn D.xa
    bypassFlow := D.xh
    bypassObserved := observedField active false (fun j => D.observedH j.succ)
    bypassProducts := observedField active 0 (fun j => D.zh j.succ)
    originalSimplex := prepared.simplex
    originalResidual := prepared.originalResidual
    work := prepared.work + ranks.accesses + ranks.comparisons + 5 * active.toArray.size +
      18 * L * (active.toArray.size + 1) + 18 * (active.toArray.size + 1) + 4 * L + 6 }

/-- Cached residual agrees with the mathematical compression, without assuming
simplex feasibility or positive mass. -/
theorem observedCache_residual {m L : ℕ} (D : RationalData m L) (labels : List (Fin m)) :
    (preprocessObserved labels (fun j => D.weights j.succ)).mergedResidual =
      (D.compressObserved labels.toFinset).weights 0 := by
  rw [preprocessObserved_mergedResidual]
  change 1 - ∑ j ∈ labels.toFinset, D.weights j.succ =
    1 - ∑ j : Fin labels.toFinset.card, D.weights (observedIndex labels.toFinset j).val.succ
  congr 1
  rw [← Finset.sum_coe_sort]
  exact ((observedIndex labels.toFinset).sum_comp
    (fun j => D.weights j.val.succ)).symm

/-- The executable array-backed data is extensionally the mathematical compression. -/
theorem observedCache_data {m L : ℕ} (D : RationalData m L) (labels : List (Fin m)) :
    (observedCache D labels).data = D.compressObserved labels.toFinset := by
  have hi (j : Fin labels.toFinset.card) := observedVector_get labels j
  have hr := observedCache_residual D labels
  cases D
  simp_all [ObservedCache.data, observedCache, compressObserved, observedVector,
    preprocessObserved_active, Vector.get_ofFn, funext_iff]

/-- Cached forward labels are the exact canonical labels used by compression. -/
theorem observedCache_label {m L : ℕ} (D : RationalData m L) (labels : List (Fin m))
    (j : Fin labels.toFinset.card) :
    (observedCache D labels).labels.get j = (observedIndex labels.toFinset j).val :=
  observedVector_get labels j

/-- The cached reverse table returns the canonical compressed index. -/
theorem observedCache_rank {m L : ℕ} (D : RationalData m L) (labels : List (Fin m))
    (j : Fin labels.toFinset.card) :
    ((observedCache D labels).ranks.get (observedIndex labels.toFinset j).val).map
      IndexedRow.payload = some j := by
  have h := observedRanks_get labels j
  rw [observedVector_get] at h
  simpa only [observedCache, observedVector, preprocessObserved_active] using h

/-- Cached atom lookup agrees with the exact merged-state reindexing. -/
theorem observedCache_atomIndex {m L : ℕ} (D : RationalData m L) (labels : List (Fin m))
    (k : Fin (m + 1)) :
    (observedCache D labels).atomIndex k =
      observedStateIndex labels.toFinset (observedGroup labels.toFinset k) := by
  refine Fin.cases ?_ (fun j => ?_) k
  · simp [ObservedCache.atomIndex, observedGroup]
  · by_cases hj : j ∈ labels.toFinset
    · let t := (observedIndex labels.toFinset).symm ⟨j, hj⟩
      have ht : (observedIndex labels.toFinset t).val = j :=
        congrArg Subtype.val ((observedIndex labels.toFinset).apply_symm_apply ⟨j, hj⟩)
      have hr := observedCache_rank D labels t
      rw [ht] at hr
      simp only [ObservedCache.atomIndex, Fin.cases_succ, hr, Option.elim_some,
        observedGroup, dif_pos hj, observedStateIndex_some]
      rfl
    · have hn := (observedRanks_none labels j).mpr (by simpa using hj)
      have hr : (observedCache D labels).ranks.get j = none := by
        simpa only [observedCache, observedVector, preprocessObserved_active] using hn
      simp only [ObservedCache.atomIndex, Fin.cases_succ, hr, Option.map_none,
        Option.elim_none, observedGroup, dif_neg hj, observedStateIndex_none]

/-- This flag checks the original explicit-coordinate simplex. A separately
supplied full-state residual still requires its consistency check. -/
theorem observedCache_simplex {m L : ℕ} (D : RationalData m L) (labels : List (Fin m)) :
    (observedCache D labels).originalSimplex = true ↔
      OriginalSimplex (fun j : Fin m => (D.weights j.succ : ℝ)) :=
  preprocessObserved_simplex labels (fun j => D.weights j.succ)

/-- Materialization has linear cost in the original weights and observation list,
plus the size of the compressed instance. -/
theorem observedCache_work {m L : ℕ} (D : RationalData m L) (labels : List (Fin m)) :
    (observedCache D labels).work ≤ 12 * m + 5 * labels.length +
      30 * (labels.toFinset.card + 1) * (L + 1) + 10 := by
  have hp := preprocessObserved_work labels (fun j => D.weights j.succ)
  have hg := group_cost (observedRankRows (observedVector labels))
  have hn : (observedRankRows (observedVector labels)).length = labels.toFinset.card := by
    simp [observedRankRows_eq]
  rw [hn] at hg
  change (preprocessObserved labels (fun j => D.weights j.succ)).work +
    (observedRanks (observedVector labels)).accesses +
    (observedRanks (observedVector labels)).comparisons +
    5 * (observedVector labels).toArray.size +
    18 * L * ((observedVector labels).toArray.size + 1) +
    18 * ((observedVector labels).toArray.size + 1) +
    4 * L + 6 ≤ _
  simp only [Vector.size_toArray, observedRanks]
  nlinarith

end Chain.Threshold.RationalData
end NetworkSimplex
