import Formal.DAGSpectral.CriterionSelect
import Formal.DAGSpectral.BitComplexity

namespace DAGSpectral

/-- A candidate scan that executes each comparator once and records its actual
primitive trace before continuing with the selected incumbent. -/
def bestFromRun {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (a : α) : List α → α × List ArithmeticEvent
  | [] => (a,[])
  | b::xs =>
    let c := compare a b
    let r := bestFromRun compare (if c.1 then b else a) xs
    (r.1,c.2 ++ r.2)

def bestByRun {α : Type*} (compare : α → α → Bool × List ArithmeticEvent) :
    List α → Option α × List ArithmeticEvent
  | [] => (none,[])
  | a::xs => let r := bestFromRun compare a xs; (some r.1,r.2)

theorem bestFromRun_result {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (a : α) (xs : List α) :
    (bestFromRun compare a xs).1 = bestFrom (fun a b => (compare a b).1) a xs := by
  induction xs generalizing a with
  | nil => rfl
  | cons b xs ih => simpa only [bestFromRun,bestFrom,List.foldl_cons] using ih _

theorem bestByRun_result {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (xs : List α) :
    (bestByRun compare xs).1 = bestBy (fun a b => (compare a b).1) xs := by
  cases xs <;> simp [bestByRun,bestBy,bestFromRun_result]

theorem bestFromRun_bounds {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (P : α → Prop) {C K : ℕ}
    (hcompare : ∀ a, P a → ∀ b, P b →
      (compare a b).2.length ≤ C ∧ ∀ e ∈ (compare a b).2, eventBits K e)
    (a : α) (ha : P a) (xs : List α) (hxs : ∀ b ∈ xs, P b) :
    P (bestFromRun compare a xs).1 ∧ (bestFromRun compare a xs).2.length ≤ xs.length*C ∧
      ∀ e ∈ (bestFromRun compare a xs).2, eventBits K e := by
  induction xs generalizing a with
  | nil => simp [bestFromRun,ha]
  | cons b xs ih =>
    have hb := hxs b (by simp)
    have hc := hcompare a ha b hb
    have hn : P (if (compare a b).1 then b else a) := by split_ifs <;> assumption
    have hs := ih _ hn (fun c hc => hxs c (by simp [hc]))
    simp only [bestFromRun,List.length_append,List.length_cons]
    refine ⟨hs.1,?_,?_⟩
    · nlinarith [hc.1,hs.2.1]
    · intro e he
      rcases List.mem_append.mp he with he | he
      · exact hc.2 e he
      · exact hs.2.2 e he

theorem bestByRun_bounds {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (P : α → Prop) {C K : ℕ}
    (hcompare : ∀ a, P a → ∀ b, P b →
      (compare a b).2.length ≤ C ∧ ∀ e ∈ (compare a b).2, eventBits K e)
    (xs : List α) (hxs : ∀ b ∈ xs, P b) :
    (bestByRun compare xs).2.length ≤ (xs.length-1)*C ∧
      ∀ e ∈ (bestByRun compare xs).2, eventBits K e := by
  cases xs with
  | nil => simp [bestByRun]
  | cons a xs =>
    have hs := bestFromRun_bounds compare P hcompare a (hxs a (by simp)) xs
      (fun b hb => hxs b (by simp [hb]))
    simpa only [bestByRun,List.length_cons,Nat.add_sub_cancel] using hs.2

theorem bestByRun_bitWork {α : Type*} (compare : α → α → Bool × List ArithmeticEvent)
    (P : α → Prop) {C K : ℕ}
    (hcompare : ∀ a, P a → ∀ b, P b →
      (compare a b).2.length ≤ C ∧ ∀ e ∈ (compare a b).2, eventBits K e)
    (xs : List α) (hxs : ∀ b ∈ xs, P b) :
    traceBitWork K (bestByRun compare xs).2 ≤
      (xs.length-1)*C*(256*(K+1)^3) := by
  have hs := bestByRun_bounds compare P hcompare xs hxs
  exact (traceBitWork_le hs.2).trans (Nat.mul_le_mul_right _ hs.1)

end DAGSpectral
