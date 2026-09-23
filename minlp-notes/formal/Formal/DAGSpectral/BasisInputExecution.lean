import Formal.DAGSpectral.NormalizationData
import Formal.DAGSpectral.RationalStorage
import Formal.DAGSpectral.FinRangeExecution

namespace DAGSpectral
open ReciprocalAnchor Matrix
open scoped BigOperators
namespace BasisInputExecution
open NormalizationTrials CoverBitCost

/-- A commutative full scan: first component counts matches, second counts
executed identifier comparisons. The quotient representation does not affect either. -/
def membershipRun {M : ℕ} (b : Finset (Fin M)) (a : Fin M) : Bool × ℕ :=
  let scanned : ℕ × ℕ := ∑ j ∈ b, (if j = a then 1 else 0, M+1)
  (decide (0 < scanned.1),scanned.2)

theorem membershipRun_spec {M : ℕ} (b : Finset (Fin M)) (a : Fin M) :
    membershipRun b a = (decide (a ∈ b),b.card*(M+1)) := by
  have hh : (∑ j ∈ b, (if j = a then 1 else 0, M+1)) =
      ((if a ∈ b then 1 else 0),b.card*(M+1)) := by
    induction b using Finset.induction_on with
    | empty => simp; rfl
    | @insert x b hx ih =>
      rw [Finset.sum_insert hx,ih,Finset.card_insert_of_notMem hx]
      by_cases hxa : x = a
      · subst a
        simp [hx,Prod.mk_add_mk,Nat.add_mul,Nat.add_comm]
      · simp [hxa,Ne.symm hxa,Prod.mk_add_mk,Nat.add_mul,Nat.add_comm]
  simp only [membershipRun,hh]
  by_cases ha : a ∈ b <;> simp [ha]


/-- Scan all identifiers in increasing order. Each membership test scans the
candidate once, and each retained identifier is copied to the output. -/
def labelsRun {M : ℕ} (b : Finset (Fin M)) : List (Fin M) → List (Fin M) × ℕ
  | [] => ([],0)
  | a::xs =>
    let checked := membershipRun b a
    let tail := labelsRun b xs
    if checked.1 then (a::tail.1,checked.2+tail.2+2*(M+1))
    else (tail.1,checked.2+tail.2+(M+1))

theorem labelsRun_value {M : ℕ} (b : Finset (Fin M)) (xs : List (Fin M)) :
    (labelsRun b xs).1 = xs.filter (fun a => decide (a ∈ b)) := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    by_cases ha : a ∈ b <;> simp [labelsRun,membershipRun_spec,ih,ha]

theorem labelsRun_cost {M : ℕ} (b : Finset (Fin M)) (xs : List (Fin M)) :
    (labelsRun b xs).2 ≤ xs.length*(b.card+2)*(M+1) := by
  induction xs with
  | nil => simp [labelsRun]
  | cons a xs ih =>
    simp only [labelsRun,membershipRun_spec]
    split_ifs <;> simp only [List.length_cons] <;> nlinarith

theorem labelsRun_sorted {M : ℕ} (b : Finset (Fin M)) :
    (labelsRun b (List.finRange M)).1 = b.sort (· ≤ ·) := by
  rw [labelsRun_value]
  apply ((List.sortedLT_finRange M).pairwise.filter _).sortedLT.eq_of_mem_iff b.sortedLT_sort
  intro a
  simp

def labelCache {M : ℕ} (b : Finset (Fin M)) : Vector (Fin M) b.card :=
  ⟨(labelsRun b (List.finRange M)).1.toArray,by simp [labelsRun_sorted]⟩

theorem labelCache_get {M : ℕ} (b : Finset (Fin M)) (i : Fin b.card) :
    (labelCache b).get i = label b i := by
  simp [labelCache,labelsRun_sorted,label,Finset.orderEmbOfFin_apply,Vector.get]
  rfl

/-- All owner comparisons are executed, including those after a match. -/
def ownerCheckRun {m : ℕ} (e : Fin m) : List (Option (Fin m)) → Bool × ℕ
  | [] => (false,0)
  | a::xs =>
    let tail := ownerCheckRun e xs
    (decide (a = some e) || tail.1,tail.2+(m+1))

theorem ownerCheckRun_spec {m : ℕ} (e : Fin m) (xs : List (Option (Fin m))) :
    ownerCheckRun e xs = (decide (some e ∈ xs),xs.length*(m+1)) := by
  induction xs with
  | nil => simp [ownerCheckRun]
  | cons a xs ih => simp [ownerCheckRun,ih,eq_comm,Nat.add_mul]

def ownersRun {m : ℕ} (owners : List (Option (Fin m))) :
    List (Fin m) → List (Fin m) × ℕ
  | [] => ([],0)
  | e::es =>
    let checked := ownerCheckRun e owners
    let tail := ownersRun owners es
    if checked.1 then (e::tail.1,checked.2+tail.2+2*(m+1))
    else (tail.1,checked.2+tail.2+(m+1))

theorem ownersRun_value {m : ℕ} (owners : List (Option (Fin m))) (es : List (Fin m)) :
    (ownersRun owners es).1 = es.filter (fun e => decide (some e ∈ owners)) := by
  induction es with
  | nil => rfl
  | cons e es ih =>
    by_cases he : some e ∈ owners <;> simp [ownersRun,ownerCheckRun_spec,ih,he]

theorem ownersRun_cost {m : ℕ} (owners : List (Option (Fin m))) (es : List (Fin m)) :
    (ownersRun owners es).2 ≤ es.length*(owners.length+2)*(m+1) := by
  induction es with
  | nil => simp [ownersRun]
  | cons e es ih =>
    simp only [ownersRun,ownerCheckRun_spec]
    split_ifs <;> simp only [List.length_cons] <;> nlinarith

/-- The output identifiers are already distinct, so no duplicate-removal
algorithm is needed to construct the owner finset. -/
def ownerCache {m r : ℕ} (owners : Vector (Option (Fin m)) r) : Finset (Fin m) :=
  ⟨(ownersRun owners.toList (List.finRange m)).1,by
    rw [ownersRun_value]
    exact (List.nodup_finRange m).filter _⟩

theorem mem_ownerCache {m r : ℕ} (owners : Vector (Option (Fin m)) r) (e : Fin m) :
    e ∈ ownerCache owners ↔ ∃ i, owners.get i = some e := by
  simp only [ownerCache, ownersRun_value, Vector.mem_toList_iff, Vector.mem_iff_getElem,
    Finset.mem_mk, Multiset.mem_coe, List.mem_filter, List.mem_finRange,
    decide_eq_true_eq, true_and]
  exact ⟨fun ⟨i,hi,h⟩ => ⟨⟨i,hi⟩,h⟩,fun ⟨i,h⟩ => ⟨i.val,i.isLt,h⟩⟩

/-- Construct the deduplicated owner set and return the charge from the same scan. -/
def ownerCacheRun {m r : ℕ} (owners : Vector (Option (Fin m)) r) : Finset (Fin m) × ℕ :=
  let ids := finRangeCounted m
  let checked := ownersRun owners.toList ids.1
  (⟨checked.1,by
    simp only [checked,ids,finRangeCounted_value,ownersRun_value]
    exact (List.nodup_finRange m).filter _⟩,ids.2+checked.2)

theorem ownerCacheRun_value {m r : ℕ} (owners : Vector (Option (Fin m)) r) :
    (ownerCacheRun owners).1 = ownerCache owners := by
  simp [ownerCacheRun,ownerCache]

theorem ownerCacheRun_work {m r : ℕ} (owners : Vector (Option (Fin m)) r) :
    (ownerCacheRun owners).2 ≤ (m+1)^2+m*(r+2)*(m+1) := by
  have hr := finRangeCounted_work m
  have ho := ownersRun_cost owners.toList (List.finRange m)
  simp only [Vector.length_toList,List.length_finRange] at ho
  simp only [ownerCacheRun,finRangeCounted_value]
  omega

/-- Copy scalar payloads to a list. Each access pays `readCost` before copying.
The factor two pays both the list cell and
its final array cell; each scalar contributes its actual numerator/denominator size. -/
def copyValuesRun {ι : Type*} (readCost : ℕ) (f : ι → ℚ) : List ι → List ℚ × ℕ
  | [] => ([],0)
  | i::is =>
    let q := f i
    let tail := copyValuesRun readCost f is
    (q::tail.1,tail.2+2*(RationalStorage.scalarCopy q+1)+readCost)

theorem copyValuesRun_value {ι : Type*} (readCost : ℕ) (f : ι → ℚ) (xs : List ι) :
    (copyValuesRun readCost f xs).1 = xs.map f := by
  induction xs with
  | nil => rfl
  | cons i xs ih => simp [copyValuesRun,ih]

theorem copyValuesRun_cost {ι : Type*} (readCost : ℕ) (f : ι → ℚ) (xs : List ι) {B : ℕ}
    (hf : ∀ i, RationalBits (f i) B) :
    (copyValuesRun readCost f xs).2 ≤ xs.length*(4*B+4+readCost) := by
  induction xs with
  | nil => simp [copyValuesRun]
  | cons i xs ih =>
    have hh := RationalStorage.scalarCopy_le (hf i)
    simp only [copyValuesRun,List.length_cons]
    nlinarith

/-- Each source coordinate access pays for traversing the original factor list
and for binary index control; no hoisting of a function-valued column is assumed. -/
def columnRun {p : ℕ} (M : ℕ) (f : Fin p → ℚ) : Vector ℚ p × ℕ :=
  let ids := finRangeCounted p
  let copied := copyValuesRun ((M+p+2)^2) f ids.1
  (⟨copied.1.toArray,by simp [copied,ids,copyValuesRun_value]⟩,ids.2+copied.2)

theorem columnRun_get {p : ℕ} (M : ℕ) (f : Fin p → ℚ) (i : Fin p) :
    (columnRun M f).1.get i = f i := by
  simp [columnRun,copyValuesRun_value,Vector.get]
  rfl

def cellsRun {p m M : ℕ} (D : FactorData p m M) :
    List (Fin M) → List (Vector ℚ p × ℚ × Option (Fin m)) × ℕ
  | [] => ([],0)
  | j::js =>
    let column := columnRun M (D.vector j)
    let weight := D.weight j
    let owner := D.owner j
    let tail := cellsRun D js
    ((column.1,weight,owner)::tail.1,
      tail.2+column.2+2*(RationalStorage.scalarCopy weight+1)+(m+2*(M+p+2)^2+5))

theorem cellsRun_value {p m M : ℕ} (D : FactorData p m M) (js : List (Fin M)) :
    (cellsRun D js).1 = js.map (fun j => ((columnRun M (D.vector j)).1,D.weight j,D.owner j)) := by
  induction js with
  | nil => rfl
  | cons j js ih => simp [cellsRun,ih]

theorem cellsRun_cost {p m M B : ℕ} (D : FactorData p m M) (js : List (Fin M))
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B) :
    (cellsRun D js).2 ≤ js.length*((p+1)^2+p*(4*B+4+(M+p+2)^2)+(4*B+4)+(m+2*(M+p+2)^2+5)) := by
  induction js with
  | nil => simp [cellsRun]
  | cons j js ih =>
    have hc := copyValuesRun_cost ((M+p+2)^2) (D.vector j) (List.finRange p) (hV j)
    have hr := finRangeCounted_work p
    have hh := RationalStorage.scalarCopy_le (hw j)
    simp only [List.length_finRange] at hc
    simp only [cellsRun,columnRun,List.length_cons,finRangeCounted_value]
    nlinarith

structure BasisCache (p m M r : ℕ) where
  labels : Vector (Fin M) r
  cells : Vector (Vector ℚ p × ℚ × Option (Fin m)) r
  required : Finset (Fin m)

def BasisCache.columns {p m M r : ℕ} (cache : BasisCache p m M r) :
    Matrix (Fin p) (Fin r) ℚ := fun i j => (cache.cells.get j).1.get i

def BasisCache.weights {p m M r : ℕ} (cache : BasisCache p m M r) :
    Fin r → ℚ := fun j => (cache.cells.get j).2.1

def basisRun {p m M : ℕ} (D : FactorData p m M) (b : Finset (Fin M)) :
    BasisCache p m M b.card × ℕ :=
  let ids := finRangeCounted M
  let ls := labelsRun b ids.1
  let labels : Vector (Fin M) b.card := ⟨ls.1.toArray,by simp [ls,ids,labelsRun_sorted]⟩
  let cs := cellsRun D ls.1
  let cells : Vector (Vector ℚ p × ℚ × Option (Fin m)) b.card :=
    ⟨cs.1.toArray,by simp [cs,cellsRun_value,ls,ids,labelsRun_sorted]⟩
  let owners := cells.map (fun c => c.2.2)
  let required := ownerCacheRun owners
  (⟨labels,cells,required.1⟩,
    ids.2+ls.2+cs.2+required.2+b.card*(m+M+2))

theorem basisRun_cell {p m M : ℕ} (D : FactorData p m M) (b : Finset (Fin M))
    (j : Fin b.card) :
    ((basisRun D b).1.cells.get j) =
      ((columnRun M (D.vector (label b j))).1,D.weight (label b j),D.owner (label b j)) := by
  simp only [Vector.get, basisRun, finRangeCounted_value, labelsRun_sorted, cellsRun_value,
    Vector.map_mk, List.map_toArray, List.map_map, List.getElem_toArray, List.getElem_map,
    label, Finset.orderEmbOfFin_apply, Fin.getElem_fin, Prod.mk.injEq]
  exact ⟨rfl,rfl,rfl⟩

theorem basisRun_columns {p m M : ℕ} (D : FactorData p m M) (b : Finset (Fin M)) :
    (basisRun D b).1.columns = columns D.vector b := by
  funext i j
  simp [BasisCache.columns,basisRun_cell,columnRun_get,columns]

theorem basisRun_weights {p m M : ℕ} (D : FactorData p m M) (b : Finset (Fin M)) :
    (basisRun D b).1.weights = fun j => D.weight (label b j) := by
  funext j
  simp [BasisCache.weights,basisRun_cell]

theorem basisRun_required {p m M : ℕ} (D : FactorData p m M) (b : Finset (Fin M)) :
    (basisRun D b).1.required = forcedOwners D.owner b := by
  ext e
  simp only [basisRun,ownerCacheRun_value,mem_ownerCache,Vector.get_map]
  change (∃ i, ((basisRun D b).1.cells.get i).2.2 = some e) ↔ _
  simp only [basisRun_cell,mem_forcedOwners]
  constructor
  · rintro ⟨i,hi⟩
    exact ⟨label b i,label_mem b i,hi⟩
  · rintro ⟨j,hj,he⟩
    have him := label_image b
    have hj' : j ∈ Finset.univ.image (label b) := by simpa only [him] using hj
    obtain ⟨i,_,hi⟩ := Finset.mem_image.mp hj'
    exact ⟨i,hi ▸ he⟩

def basisWorkBound (p m M r B : ℕ) : ℕ :=
  (M+1)^2+M*(r+2)*(M+1)+r*((p+1)^2+p*(4*B+4+(M+p+2)^2)+(4*B+4)+(m+2*(M+p+2)^2+5))+
    ((m+1)^2+m*(r+2)*(m+1))+r*(m+M+2)

theorem basisRun_work {p m M B : ℕ} (D : FactorData p m M) (b : Finset (Fin M))
    (hV : ∀ j i, RationalBits (D.vector j i) B)
    (hw : ∀ j, RationalBits (D.weight j) B) :
    (basisRun D b).2 ≤ basisWorkBound p m M b.card B := by
  have hr := finRangeCounted_work M
  have hl := labelsRun_cost b (List.finRange M)
  have hc := cellsRun_cost D (labelsRun b (List.finRange M)).1 hV hw
  have ho := ownerCacheRun_work ((basisRun D b).1.cells.map (fun c => c.2.2))
  simp only [List.length_finRange,labelsRun_sorted,Finset.length_sort] at hl hc
  change (finRangeCounted M).2+(labelsRun b (finRangeCounted M).1).2 +
      (cellsRun D (labelsRun b (finRangeCounted M).1).1).2 +
      (ownerCacheRun ((basisRun D b).1.cells.map (fun c => c.2.2))).2+
      b.card*(m+M+2) ≤ _
  rw [finRangeCounted_value,labelsRun_sorted]
  unfold basisWorkBound
  omega

end BasisInputExecution
end DAGSpectral
