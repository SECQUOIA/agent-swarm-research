import Formal.DAGSpectral.ProfileBitCost

/-! Schoolbook work of the implemented list-based DP. Key computations are
charged again at every comparison; no constant-time dictionary is assumed. -/
namespace DAGSpectral
open ReciprocalAnchor ReciprocalAnchor.ManyLeaf.BitCost
open scoped BigOperators

/-- Charge every representative comparison with its actual key-work expression. -/
def representativeBitWork {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) : List α → ℕ
  | [] => 0
  | x::xs => representativeBitWork key cost xs +
      ((representatives key xs).map (cost x)).sum

theorem representativeBitWork_le {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (cost : α → α → ℕ) (xs : List α) (K : ℕ)
    (hc : ∀ x ∈ xs, ∀ y ∈ xs, cost x y ≤ K) :
    representativeBitWork key cost xs ≤ representativeComparisonBudget key xs*K := by
  induction xs with
  | nil => simp [representativeBitWork,representativeComparisonBudget]
  | cons x xs ih =>
    have ht := ih (fun a ha b hb => hc a (by simp [ha]) b (by simp [hb]))
    have hs : ((representatives key xs).map (cost x)).sum ≤
        (representatives key xs).length*K := by
      have hh := List.sum_le_card_nsmul ((representatives key xs).map (cost x)) K
      apply (by simpa using hh)
      intro z hz
      exact hc x (by simp) z (by simp [representatives_subset key xs hz])
    simp only [representativeBitWork,representativeComparisonBudget]
    nlinarith

namespace ExplicitDAG
variable {v m : ℕ} {κ : Type*} [Fintype κ]

def profileBitWork (label : Fin m → κ → ℤ) (es : List (Fin m)) : ℕ :=
  ∑ i, integerSumBitWork (es.map (fun e => label e i))

theorem profileBitWork_le {label : Fin m → κ → ℤ} {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (es : List (Fin m)) :
    profileBitWork label es ≤ Fintype.card κ*es.length*(B+es.length+1) := by
  unfold profileBitWork
  calc
    _ ≤ ∑ _i : κ, es.length*(B+es.length+1) := by
      apply Finset.sum_le_sum
      intro i _
      simpa only [List.length_map] using integerSumBitWork_le
        (xs := es.map (fun e => label e i)) (by
          intro x hx; obtain ⟨e,_,rfl⟩ := List.mem_map.mp hx; exact hl e i)
    _ = _ := by simp; ring

/-- Owner-mask equality is decided by membership scans on the original paths.
This avoids treating a finite-set key as a unit-cost machine word. -/
theorem ownerMask_eq_iff_membership (required : Finset (Fin m))
    (es fs : List (Fin m)) :
    ownerMask required es = ownerMask required fs ↔
      ∀ e ∈ required, e ∈ es ↔ e ∈ fs := by
  constructor
  · intro h e he
    have hm := congrArg (fun s : Finset (Fin m) => e ∈ s) h
    simpa [ownerMask,he] using hm
  · intro h
    ext e
    by_cases he : e ∈ required
    · simpa [ownerMask,he] using h e he
    · simp [ownerMask,he]

/-- List membership and mask comparisons use bounded edge identifiers. The
quadratic list budget covers duplicate removal, intersection, and equality. -/
def maskBitBudget (m r a b : ℕ) : ℕ := (a+b+r+1)^2*(m+1)

def keyBitWork (required : Finset (Fin m)) (label : Fin m → κ → ℤ)
    (es fs : List (Fin m)) : ℕ :=
  profileBitWork label es + profileBitWork label fs +
    (∑ i, addCost (profile label es i).natAbs.size (profile label fs i).natAbs.size) +
    maskBitBudget m required.card es.length fs.length

def keyWorkBound (v m d r B : ℕ) : ℕ :=
  2*d*v*(B+v+1)+d*(B+v+1)+(2*v+r+1)^2*(m+1)

theorem keyBitWork_le {label : Fin m → κ → ℤ} {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (required : Finset (Fin m))
    (es fs : List (Fin m)) (he : es.length ≤ v) (hf : fs.length ≤ v) :
    keyBitWork required label es fs ≤ keyWorkBound v m (Fintype.card κ) required.card B := by
  have hew : profileBitWork label es ≤ Fintype.card κ*v*(B+v+1) :=
    (profileBitWork_le hl es).trans (by gcongr)
  have hfw : profileBitWork label fs ≤ Fintype.card κ*v*(B+v+1) :=
    (profileBitWork_le hl fs).trans (by gcongr)
  have hc : (∑ i, addCost (profile label es i).natAbs.size (profile label fs i).natAbs.size) ≤
      Fintype.card κ*(B+v+1) := by
    calc
      _ ≤ ∑ _i : κ, (B+v+1) := by
        apply Finset.sum_le_sum
        intro i _
        have h1 := Nat.size_le.mpr (integerBits_mono (profile_integerBits hl es i)
          (show B+es.length ≤ B+v by omega))
        have h2 := Nat.size_le.mpr (integerBits_mono (profile_integerBits hl fs i)
          (show B+fs.length ≤ B+v by omega))
        unfold addCost
        omega
      _ = _ := by simp
  have hm : maskBitBudget m required.card es.length fs.length ≤
      (2*v+required.card+1)^2*(m+1) := by
    unfold maskBitBudget
    gcongr
    omega
  unfold keyBitWork keyWorkBound
  nlinarith

/-- Actual candidate lists and actual representative comparisons are charged. -/
def comparisonBitWork (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ :=
  ∑ t : Fin v, representativeBitWork (stateKey required label) (keyBitWork required label)
    (candidates G allowed s t (run G allowed s required label t.val))

theorem comparisonBitWork_le (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) :
    comparisonBitWork G allowed s required label ≤
      comparisonBudget G allowed s required label *
        keyWorkBound v m (Fintype.card κ) required.card B := by
  unfold comparisonBitWork comparisonBudget
  rw [Finset.sum_mul]
  apply Finset.sum_le_sum
  intro t _
  apply representativeBitWork_le
  intro es hes fs hfs
  have hpath {zs} (hz : zs ∈ candidates G allowed s t (run G allowed s required label t.val)) :
      zs.length ≤ v := by
    have hh := candidates_sound G allowed s _ t
      (fun u zs hzs => run_sound G allowed s required label t.val u zs hzs) hz
    have hlen := hh.1.length_le_vertices
    omega
  exact keyBitWork_le hl required es fs (hpath hes) (hpath hfs)

theorem comparisonBitWork_window_bound (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (window : Finset ℤ)
    (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window) :
    comparisonBitWork G allowed s required label ≤
      (v*(1+m*(2^required.card*window.card^Fintype.card κ))^2) *
        keyWorkBound v m (Fintype.card κ) required.card B := by
  exact (comparisonBitWork_le G allowed s required label hl).trans
    (Nat.mul_le_mul_right _ (comparisonBudget_bound G allowed s required label window hw))

/-- A realizable eager DP charge: scan every incoming-edge candidate list,
update/copy the vertex table, copy extended paths, and scan terminal masks.
The key work is charged at every actual representative comparison. -/
def dpBitWork (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ :=
  comparisonBitWork G allowed s required label +
    (v*(m+1)+v*v)*(v+m+1)^2 +
    edgeExtensions G allowed s required label*(v+1)*(m+1) +
    storedStates G allowed s required label v*(required.card+1)*(v+1)*(m+1)

/-- The full list-DP schoolbook charge is an explicit polynomial in the state
bound, graph size, and rational-label input widths. -/
theorem dpBitWork_window_bound (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) {B : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (window : Finset ℤ)
    (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window) :
    dpBitWork G allowed s required label ≤
      (v*(1+m*(2^required.card*window.card^Fintype.card κ))^2) *
        keyWorkBound v m (Fintype.card κ) required.card B +
      (v*(m+1)+v*v)*(v+m+1)^2 +
      (m*(2^required.card*window.card^Fintype.card κ))*(v+1)*(m+1) +
      (v*(2^required.card*window.card^Fintype.card κ))*(required.card+1)*(v+1)*(m+1) := by
  have hc := comparisonBitWork_window_bound G allowed s required label hl window hw
  have he := edgeExtensions_bound G allowed s required label window hw
  have hs := storedStates_bound G allowed s required label window hw v
  unfold dpBitWork
  gcongr

/-- Every call of a coordinate-label function made while recomputing compared
profiles. This charge does not assume that label values have been cached. -/
def labelAccessCount (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ :=
  ∑ t : Fin v, representativeBitWork (stateKey required label)
    (fun es fs => (es.length+fs.length)*Fintype.card κ)
    (candidates G allowed s t (run G allowed s required label t.val))

theorem labelAccessCount_le (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) :
    labelAccessCount G allowed s required label ≤
      comparisonBudget G allowed s required label*(2*v*Fintype.card κ) := by
  unfold labelAccessCount comparisonBudget
  rw [Finset.sum_mul]
  apply Finset.sum_le_sum
  intro t _
  apply representativeBitWork_le
  intro es hes fs hfs
  have hpath {zs} (hz : zs ∈ candidates G allowed s t (run G allowed s required label t.val)) :
      zs.length ≤ v := by
    have hh := candidates_sound G allowed s _ t
      (fun u zs hzs => run_sound G allowed s required label t.val u zs hzs) hz
    have hlen := hh.1.length_le_vertices
    omega
  apply Nat.mul_le_mul_right
  have he := hpath hes
  have hf := hpath hfs
  omega

/-- Allows an explicit cost for every recomputed rational label. -/
def uncachedDPBitWork (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) (sourceLabelCost : ℕ) : ℕ :=
  dpBitWork G allowed s required label +
    labelAccessCount G allowed s required label*sourceLabelCost

def labelPreprocessingBitWork (x : Fin m → κ → ℚ) (h : ℚ) (B C : ℕ) : ℕ :=
  ∑ e, ∑ i, floorLabelBitWork (x e i) h B C

theorem labelPreprocessingBitWork_le {x : Fin m → κ → ℚ} {h : ℚ} {B C : ℕ}
    (hx : ∀ e i, RationalBits (x e i) B) (hh : RationalBits h C) :
    labelPreprocessingBitWork x h B C ≤ m*Fintype.card κ*(268*(B+C+1)^3) := by
  unfold labelPreprocessingBitWork
  calc
    _ ≤ ∑ _e : Fin m, ∑ _i : κ, (268*(B+C+1)^3) := by
      apply Finset.sum_le_sum
      intro e _
      apply Finset.sum_le_sum
      intro i _
      exact floorLabelBitWork_le (hx e i) hh
    _ = _ := by simp; ring

omit [Fintype κ] in
theorem rational_floor_labels_bits {x : Fin m → κ → ℚ} {h : ℚ} {B C : ℕ}
    (hx : ∀ e i, RationalBits (x e i) B) (hh : RationalBits h C) :
    ∀ e i, IntegerBits ⌊x e i/h⌋ (B+C+1) :=
  fun e i => integerBits_floor (rationalBits_div (hx e i) hh)

end ExplicitDAG

/-- The paper's profile interval size has a polynomial upper bound in the
inverse-accuracy parameter. This is the fixed-dimensional complexity regime. -/
theorem coordinateCount_le_polynomial (p r N : ℕ) (η : ℝ) :
    coordinateCount p r N η ≤ 8*p*r*N^2*⌈1/η⌉₊+N+2 := by
  unfold coordinateCount
  apply Nat.add_le_add_right _ 2
  apply Nat.ceil_le.mpr
  have h := Nat.le_ceil (1/η)
  have hp : (0:ℝ) ≤ 8*p*r*N^2 := by positivity
  have hh := mul_le_mul_of_nonneg_left h hp
  push_cast
  convert add_le_add_right hh (N:ℝ) using 1 <;> ring

end DAGSpectral
