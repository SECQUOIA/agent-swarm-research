import Formal.MatroidSpectral.CriteriaContrastExecution
import Formal.DAGSpectral.BasisInputExecution

/-! Identifier work for criterion selection. Candidate sets are materialized by
an executed increasing identifier scan, with every membership comparison
charged. No uncharged finite-set sorting is used in this implementation. -/
namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials ReciprocalAnchor
open DAGSpectral.BasisInputExecution DAGSpectral.CoverBitCost

def materializeSetRun {m : ℕ} (S : Finset (Fin m)) : List (Fin m) × ℕ :=
  let ids := finRangeCounted m
  let selected := labelsRun S ids.1
  (selected.1,ids.2+selected.2)

@[simp] theorem materializeSetRun_value {m : ℕ} (S : Finset (Fin m)) :
    (materializeSetRun S).1 = S.sort (· ≤ ·) := by
  simp only [materializeSetRun,finRangeCounted_value,labelsRun_sorted]

def materializeSetWork (m : ℕ) : ℕ := (m+1)^2+m*(m+2)*(m+1)

theorem materializeSetRun_work {m : ℕ} (S : Finset (Fin m)) :
    (materializeSetRun S).2 ≤ materializeSetWork m := by
  have hc : S.card ≤ m := by simpa using S.card_le_univ
  have hi := finRangeCounted_work m
  have hl := labelsRun_cost S (List.finRange m)
  simp only [List.length_finRange] at hl
  simp only [materializeSetRun,finRangeCounted_value,materializeSetWork]
  exact Nat.add_le_add hi (hl.trans (by gcongr))

def setComparisonBitRun {p m M : ℕ} (D : FactorData p m M)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent) (K : ℕ) (S T : Finset (Fin m)) : Bool × ℕ :=
  let s := materializeSetRun S
  let t := materializeSetRun T
  let r := pathComparisonRun (D.atom none) (fun e => D.atom (some e)) compare s.1 t.1
  (r.1,s.2+t.2+traceBitWork K r.2+1)

@[simp] theorem setComparisonBitRun_value {p m M : ℕ} (D : FactorData p m M)
    (compare) (K : ℕ) (S T : Finset (Fin m)) :
    (setComparisonBitRun D compare K S T).1 =
      (compare (information D S) (information D T)).1 := by
  simp only [setComparisonBitRun,materializeSetRun_value,pathComparisonRun_value,
    ← information_eq_sortedInformation]

theorem setComparisonBitRun_work {p m M B q C K : ℕ} (D : FactorData p m M)
    (hD : ∀ o, MatrixBits (D.atom o) B) (compare)
    (hK : 1 + (q + 1) * (B + 1) ≤ K)
    (hcompare : ∀ A, MatrixBits A (1 + (q + 1) * (B + 1)) →
      ∀ T, MatrixBits T (1 + (q + 1) * (B + 1)) →
      (compare A T).2.length ≤ C ∧ ∀ e ∈ (compare A T).2, eventBits K e)
    (S T : Finset (Fin m)) (hS : S.card ≤ q) (hT : T.card ≤ q) :
    (setComparisonBitRun D compare K S T).2 ≤
      2*materializeSetWork m+(2*(p*p*(q+1))+C)*(256*(K+1)^3)+1 := by
  have hs := materializeSetRun_work S
  have ht := materializeSetRun_work T
  have hb := pathComparisonRun_bounds (hD none) (fun e => hD (some e)) compare hK hcompare
    (S.sort (· ≤ ·)) (T.sort (· ≤ ·)) (by simpa using hS) (by simpa using hT)
  have he := (traceBitWork_le hb.2).trans (Nat.mul_le_mul_right _ hb.1)
  simp only [setComparisonBitRun,materializeSetRun_value]
  omega

/-- The branch returns an existing immutable candidate; its control cost covers
list headers, addresses, and incumbent selection, without copying its matrix. -/
def scanFromBitRun {α : Type*} (compare : α → α → Bool × ℕ) (control : ℕ)
    (a : α) : List α → α × ℕ
  | [] => (a,1)
  | b::xs =>
    let c := compare a b
    let tail := scanFromBitRun compare control (if c.1 then b else a) xs
    (tail.1,c.2+tail.2+control)

def scanBestBitRun {α : Type*} (compare : α → α → Bool × ℕ) (control : ℕ) :
    List α → Option α × ℕ
  | [] => (none,1)
  | a::xs => let r := scanFromBitRun compare control a xs; (some r.1,r.2+1)

theorem scanFromBitRun_value {α : Type*} (compare : α → α → Bool × ℕ)
    (control : ℕ) (a : α) (xs : List α) :
    (scanFromBitRun compare control a xs).1 = bestFrom (fun a b => (compare a b).1) a xs := by
  induction xs generalizing a with
  | nil => rfl
  | cons b xs ih => simpa only [scanFromBitRun,bestFrom,List.foldl_cons] using ih _

theorem scanBestBitRun_value {α : Type*} (compare : α → α → Bool × ℕ)
    (control : ℕ) (xs : List α) :
    (scanBestBitRun compare control xs).1 = bestBy (fun a b => (compare a b).1) xs := by
  cases xs <;> simp [scanBestBitRun,bestBy,scanFromBitRun_value]

theorem scanFromBitRun_work {α : Type*} (compare : α → α → Bool × ℕ)
    (control W : ℕ) (P : α → Prop)
    (hcompare : ∀ a, P a → ∀ b, P b → (compare a b).2 ≤ W)
    (a : α) (ha : P a) (xs : List α) (hxs : ∀ b ∈ xs, P b) :
    (scanFromBitRun compare control a xs).2 ≤ 1+xs.length*(W+control) := by
  induction xs generalizing a with
  | nil => simp [scanFromBitRun]
  | cons b xs ih =>
    have hb := hxs b (by simp)
    have hc := hcompare a ha b hb
    have hn : P (if (compare a b).1 then b else a) := by split_ifs <;> assumption
    have ht := ih _ hn (fun c hc => hxs c (by simp [hc]))
    simp only [scanFromBitRun,List.length_cons]
    nlinarith

theorem scanBestBitRun_work {α : Type*} (compare : α → α → Bool × ℕ)
    (control W : ℕ) (P : α → Prop)
    (hcompare : ∀ a, P a → ∀ b, P b → (compare a b).2 ≤ W)
    (xs : List α) (hxs : ∀ a ∈ xs, P a) :
    (scanBestBitRun compare control xs).2 ≤ 2+xs.length*(W+control) := by
  cases xs with
  | nil => simp [scanBestBitRun]
  | cons a xs =>
    have ht := scanFromBitRun_work compare control W P hcompare a (hxs a (by simp))
      xs (fun b hb => hxs b (by simp [hb]))
    simp only [scanBestBitRun,List.length_cons]
    nlinarith

def selectSetsBitRun {p m M : ℕ} (D : FactorData p m M)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent) (K : ℕ)
    (xs : List (Finset (Fin m))) : Option (Finset (Fin m)) × ℕ :=
  scanBestBitRun (setComparisonBitRun D compare K) ((m+xs.length+2)^2) xs

theorem selectSetsBitRun_value {p m M : ℕ} (D : FactorData p m M) (compare) (K : ℕ)
    (xs : List (Finset (Fin m))) :
    (selectSetsBitRun D compare K xs).1 = (selectSetsRun D compare xs).1 := by
  simp only [selectSetsBitRun,scanBestBitRun_value,setComparisonBitRun_value,selectSetsRun_result]

/-- Both identifier materialization and every rational operation are counted.
The remaining comparison bounds are instantiated for each exact criterion. -/
theorem selectSetsBitRun_work {p m M B q C K : ℕ} (D : FactorData p m M)
    (hD : ∀ o, MatrixBits (D.atom o) B) (compare)
    (hK : 1 + (q + 1) * (B + 1) ≤ K)
    (hcompare : ∀ A, MatrixBits A (1 + (q + 1) * (B + 1)) →
      ∀ T, MatrixBits T (1 + (q + 1) * (B + 1)) →
      (compare A T).2.length ≤ C ∧ ∀ e ∈ (compare A T).2, eventBits K e)
    (xs : List (Finset (Fin m))) (hxs : ∀ S ∈ xs, S.card ≤ q) :
    (selectSetsBitRun D compare K xs).2 ≤
      2+xs.length*(2*materializeSetWork m+(2*(p*p*(q+1))+C)*(256*(K+1)^3)+1+
        (m+xs.length+2)^2) :=
  scanBestBitRun_work _ _ _ (fun S => S.card ≤ q)
    (fun S hS T hT => setComparisonBitRun_work D hD compare hK hcompare S T hS hT) xs hxs

end MatroidSpectral
