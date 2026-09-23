import Formal.NetworkSimplex.ThresholdGrouping
import Formal.NetworkSimplex.ThresholdRows

/-! Executable rational generation of every original reduced profile row. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- Rational input data; its real interpretation is exactly `ReductionData`. -/
structure RationalData (m L : ℕ) where
  c : Fin L → Fin (m + 1) → StateClass
  u : Fin L → Fin (m + 1) → ℚ
  v : Fin L → Fin (m + 1) → ℚ
  weights : Fin (m + 1) → ℚ
  xa : Fin L → ℚ
  xh : ℚ
  observedH : Fin (m + 1) → Bool
  zh : Fin (m + 1) → ℚ

namespace RationalData
variable {m L : ℕ}

noncomputable def toReal (D : RationalData m L) : ReductionData m (Fin L) where
  c := D.c
  u i j := D.u i j
  v i j := D.v i j
  weights j := D.weights j
  xa i := D.xa i
  xh := D.xh
  observedH := D.observedH
  zh j := D.zh j

def total (D : RationalData m L) : ℚ := 1 - D.xh

def residual (D : RationalData m L) (i : Fin L) : ℚ :=
  D.xa i - ((List.ofFn fun j => if observesA (D.c i j) then D.u i j else 0).sum) +
    ((List.ofFn fun j => if D.c i j = .bOnly then D.v i j else 0).sum)

@[simp] theorem total_cast (D : RationalData m L) :
    (D.total : ℝ) = D.toReal.total := by simp [total, toReal, ReductionData.total]

@[simp] theorem residual_cast (D : RationalData m L) (i : Fin L) :
    (D.residual i : ℝ) = Chain.residual (D.toReal.c i) (D.toReal.u i) (D.toReal.v i)
      (D.toReal.xa i) := by
  change (D.residual i : ℝ) = Chain.residual (D.c i)
    (fun j => (D.u i j : ℝ)) (fun j => (D.v i j : ℝ)) (D.xa i)
  simp only [residual, Chain.residual, List.sum_ofFn,
    Rat.cast_add, Rat.cast_sub, Rat.cast_sum]
  congr 1
  · congr 1
    apply Finset.sum_congr rfl
    intro j _
    split_ifs <;> simp
  · apply Finset.sum_congr rfl
    intro j _
    split_ifs <;> simp

/-- All expensive gadget quantities are computed once and cached in an array. -/
structure GadgetCache (m : ℕ) where
  endpoint : ℚ
  subsetB : Finset (Fin m)
  subsetA : Finset (Fin m)

def gadgetCache (D : RationalData m L) (i : Fin L) : GadgetCache m where
  endpoint := D.residual i
  subsetB := Finset.univ.filter fun j => D.c i j.succ = .bOnly
  subsetA := Finset.univ.filter fun j => observesA (D.c i j.succ)

structure Cache (m L : ℕ) where
  total : ℚ
  gadgets : Array (GadgetCache m)
  size_eq : gadgets.size = L

def cache (D : RationalData m L) : Cache m L where
  total := D.total
  gadgets := Array.ofFn D.gadgetCache
  size_eq := Array.size_ofFn

def Cache.gadget (C : Cache m L) (i : Fin L) : GadgetCache m :=
  C.gadgets[i.val]'(by rw [C.size_eq]; exact i.isLt)

@[simp] theorem cache_gadget (D : RationalData m L) (i : Fin L) :
    D.cache.gadget i = D.gadgetCache i := by
  simp [Cache.gadget, cache]

/-- No residual sum or subset scan occurs in this per-row evaluator. -/
def cachedRhs (D : RationalData m L) (C : Cache m L) : ProfileRow m (Fin L) → ℚ
  | .lower _ => 0
  | .upper j => D.weights j.succ
  | .totalLower => D.weights 0 - C.total
  | .totalUpper => C.total
  | .bypassLower j => if D.observedH j.succ then D.zh j.succ - D.weights j.succ else 0
  | .bypassUpper j => if D.observedH j.succ then D.weights j.succ - D.zh j.succ else 0
  | .aLower i j => if D.c i j.succ = .aOnly then -D.u i j.succ else 0
  | .bLower i j => if D.c i j.succ = .bOnly then -D.v i j.succ else 0
  | .bothLower i j => if D.c i j.succ = .both then -(D.u i j.succ + D.v i j.succ) else 0
  | .bothUpper i j => if D.c i j.succ = .both then D.u i j.succ + D.v i j.succ else 0
  | .endpointB i => (C.gadget i).endpoint
  | .endpointA i => C.total - (C.gadget i).endpoint

def cachedNormal (D : RationalData m L) (C : Cache m L) :
    ProfileRow m (Fin L) → ProfileNormal m
  | .lower j => .negativeSingleton j
  | .upper j => .subset {j}
  | .totalLower => .negativeTotal
  | .totalUpper => .subset Finset.univ
  | .bypassLower j => if D.observedH j.succ then .negativeSingleton j else .subset ∅
  | .bypassUpper j => if D.observedH j.succ then .subset {j} else .subset ∅
  | .aLower i j => if D.c i j.succ = .aOnly then .negativeSingleton j else .subset ∅
  | .bLower i j => if D.c i j.succ = .bOnly then .negativeSingleton j else .subset ∅
  | .bothLower i j => if D.c i j.succ = .both then .negativeSingleton j else .subset ∅
  | .bothUpper i j => if D.c i j.succ = .both then .subset {j} else .subset ∅
  | .endpointB i => .subset (C.gadget i).subsetB
  | .endpointA i => .subset (C.gadget i).subsetA

@[simp] theorem cachedRhs_cast (D : RationalData m L) (r : ProfileRow m (Fin L)) :
    (D.cachedRhs D.cache r : ℝ) = D.toReal.rowRhs r := by
  cases r <;> simp only [cachedRhs, ReductionData.rowRhs, toReal] <;>
    (try split_ifs) <;> simp_all [cache, Cache.gadget, gadgetCache, total, ReductionData.total]
  all_goals rfl

@[simp] theorem cachedNormal_eq (D : RationalData m L) (r : ProfileRow m (Fin L)) :
    D.cachedNormal D.cache r = D.toReal.rowNormal r := by
  cases r <;> simp only [cachedNormal, ReductionData.rowNormal, toReal, cache_gadget, gadgetCache]
  all_goals congr 1

/-- Original global row tags, including the two total rows. -/
def globalTags (m L : ℕ) : List (ProfileRow m (Fin L)) :=
  [ProfileRow.totalLower, .totalUpper] ++
    (List.ofFn fun j : Fin m => [ProfileRow.lower j, .upper j,
      .bypassLower j, .bypassUpper j]).flatten

/-- Original rows for one gadget, with both endpoint rows. -/
def gadgetTags (m : ℕ) {L : ℕ} (i : Fin L) : List (ProfileRow m (Fin L)) :=
  [ProfileRow.endpointB i, .endpointA i] ++
    (List.ofFn fun j : Fin m => [ProfileRow.aLower i j, .bLower i j,
      .bothLower i j, .bothUpper i j]).flatten

def allTags (m L : ℕ) : List (ProfileRow m (Fin L)) :=
  globalTags m L ++ (List.ofFn (gadgetTags m (L := L))).flatten

theorem globalTags_length (m L : ℕ) : (globalTags m L).length = 4 * m + 2 := by
  simp [globalTags, List.length_flatten, List.map_ofFn, List.sum_ofFn]
  omega

theorem gadgetTags_length (m : ℕ) {L : ℕ} (i : Fin L) :
    (gadgetTags m i).length = 4 * m + 2 := by
  simp [gadgetTags, List.length_flatten, List.map_ofFn, List.sum_ofFn]
  omega

theorem allTags_length (m L : ℕ) : (allTags m L).length = (4 * m + 2) * (L + 1) := by
  simp only [allTags, List.length_append, globalTags_length, List.length_flatten]
  simp [List.map_ofFn, List.sum_ofFn, gadgetTags_length]
  ring

theorem mem_allTags {m L : ℕ} (r : ProfileRow m (Fin L)) : r ∈ allTags m L := by
  cases r <;> simp [allTags, globalTags, gadgetTags, List.mem_flatten, List.mem_ofFn]

/-- Indexed key tables. Their construction encodes each subset only once. -/
structure KeyCache (m L K : ℕ) where
  zero : Fin K
  positive : Vector (Fin K) m
  negative : Vector (Fin K) m
  totalLower : Fin K
  totalUpper : Fin K
  endpoints : Vector (Fin K × Fin K) L

def keyCache {K : ℕ} (C : Cache m L) (key : ProfileNormal m → Fin K) : KeyCache m L K where
  zero := key (.subset ∅)
  positive := Vector.ofFn fun j => key (.subset {j})
  negative := Vector.ofFn fun j => key (.negativeSingleton j)
  totalLower := key .negativeTotal
  totalUpper := key (.subset Finset.univ)
  endpoints := Vector.ofFn fun i =>
    (key (.subset (C.gadget i).subsetB), key (.subset (C.gadget i).subsetA))

/-- Per-row keys use cached masks and indexed vector lookup only. -/
def cachedKey {K : ℕ} (D : RationalData m L) (C : KeyCache m L K) :
    ProfileRow m (Fin L) → Fin K
  | .lower j => C.negative.get j
  | .upper j => C.positive.get j
  | .totalLower => C.totalLower
  | .totalUpper => C.totalUpper
  | .bypassLower j => if D.observedH j.succ then C.negative.get j else C.zero
  | .bypassUpper j => if D.observedH j.succ then C.positive.get j else C.zero
  | .aLower i j => if D.c i j.succ = .aOnly then C.negative.get j else C.zero
  | .bLower i j => if D.c i j.succ = .bOnly then C.negative.get j else C.zero
  | .bothLower i j => if D.c i j.succ = .both then C.negative.get j else C.zero
  | .bothUpper i j => if D.c i j.succ = .both then C.positive.get j else C.zero
  | .endpointB i => (C.endpoints.get i).1
  | .endpointA i => (C.endpoints.get i).2

@[simp] theorem cachedKey_eq {K : ℕ} (D : RationalData m L)
    (key : ProfileNormal m → Fin K) (r : ProfileRow m (Fin L)) :
    D.cachedKey (keyCache D.cache key) r = key (D.toReal.rowNormal r) := by
  rw [← cachedNormal_eq]
  cases r <;> simp only [cachedKey, keyCache, cachedNormal, Vector.get_ofFn] <;>
    split_ifs <;> rfl

/-- Original row identifiers are stored as payloads of the grouping input.
The rational and key caches are shared by all rows. -/
def indexedRows {K : ℕ} (D : RationalData m L) (key : ProfileNormal m → Fin K) :
    List (NetworkSimplex.ThresholdGrouping.IndexedRow K (ProfileRow m (Fin L))) :=
  let C := D.cache
  let keys := keyCache C key
  (allTags m L).map fun r => ⟨D.cachedKey keys r, D.cachedRhs C r, r⟩

theorem indexedRows_length {K : ℕ} (D : RationalData m L) (key : ProfileNormal m → Fin K) :
    (D.indexedRows key).length = (4 * m + 2) * (L + 1) := by
  simpa only [indexedRows, List.length_map] using allTags_length m L

theorem indexedRows_mem {K : ℕ} (D : RationalData m L) (key : ProfileNormal m → Fin K)
    (r : ProfileRow m (Fin L)) :
    (⟨D.cachedKey (keyCache D.cache key) r, D.cachedRhs D.cache r, r⟩ :
      NetworkSimplex.ThresholdGrouping.IndexedRow K (ProfileRow m (Fin L))) ∈
        D.indexedRows key :=
  List.mem_map.mpr ⟨r, mem_allTags r, rfl⟩

theorem indexedRows_spec {K : ℕ} (D : RationalData m L) (key : ProfileNormal m → Fin K)
    {r : NetworkSimplex.ThresholdGrouping.IndexedRow K (ProfileRow m (Fin L))}
    (hr : r ∈ D.indexedRows key) :
    r.key = key (D.toReal.rowNormal r.payload) ∧ (r.value : ℝ) = D.toReal.rowRhs r.payload := by
  obtain ⟨tag, _, rfl⟩ := List.mem_map.mp hr
  exact ⟨cachedKey_eq D key tag, cachedRhs_cast D tag⟩

/-- The grouping input gives exactly the original reduced profile system. -/
theorem indexedRows_constraints {K : ℕ} (D : RationalData m L)
    (key : ProfileNormal m → Fin K) (value : Fin K → (Fin m → ℝ) → ℝ)
    (hkey : ∀ p x, value (key p) x = p.value x) (x : Fin m → ℝ) :
    (∀ r ∈ D.indexedRows key, value r.key x ≤ (r.value : ℝ)) ↔ D.toReal.ReducedProfile x := by
  rw [← ReductionData.rows_iff_reducedProfile]
  constructor
  · intro h r
    have hr := h _ (indexedRows_mem D key r)
    simpa only [cachedKey_eq, cachedRhs_cast, hkey] using hr
  · intro h r hr
    obtain ⟨hk, hv⟩ := indexedRows_spec D key hr
    rw [hk, hv, hkey]
    exact h r.payload

/-- A single cached RHS evaluation uses at most two rational operations. -/
def rhsCharge (D : RationalData m L) : ProfileRow m (Fin L) → ℕ
  | .lower _ | .upper _ | .totalUpper | .endpointB _ => 0
  | .totalLower | .endpointA _ => 1
  | .bypassLower j | .bypassUpper j => if D.observedH j.succ then 1 else 0
  | .aLower i j => if D.c i j.succ = .aOnly then 1 else 0
  | .bLower i j => if D.c i j.succ = .bOnly then 1 else 0
  | .bothLower i j => if D.c i j.succ = .both then 2 else 0
  | .bothUpper i j => if D.c i j.succ = .both then 1 else 0

theorem rhsCharge_le (D : RationalData m L) (r : ProfileRow m (Fin L)) :
    D.rhsCharge r ≤ 2 := by
  cases r <;> simp only [rhsCharge] <;> (try split_ifs) <;> omega

/-- The two residual sums each add `m+1` entries, followed by one subtraction
and one addition. Key encoding and array accesses are separate charges. -/
def arithmeticCharge (D : RationalData m L) : ℕ :=
  1 + L * (2 * (m + 1) + 2) + ((allTags m L).map D.rhsCharge).sum

theorem arithmeticCharge_le (D : RationalData m L) :
    D.arithmeticCharge ≤ 1 + L * (2 * m + 4) + 2 * ((4 * m + 2) * (L + 1)) := by
  have hs : ((allTags m L).map D.rhsCharge).sum ≤ 2 * (allTags m L).length := by
    induction allTags m L with
    | nil => simp
    | cons r rows ih =>
      simp only [List.map_cons, List.sum_cons, List.length_cons]
      have h := D.rhsCharge_le r
      omega
  rw [allTags_length] at hs
  dsimp [arithmeticCharge]
  nlinarith

theorem arithmeticCharge_linear (D : RationalData m L) (hm : 1 ≤ m) :
    D.arithmeticCharge ≤ 20 * m * (L + 1) := by
  have h := arithmeticCharge_le D
  nlinarith

end RationalData
end NetworkSimplex.Chain.Threshold
