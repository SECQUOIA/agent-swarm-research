import Formal.DAGSpectral.ProfileDPBitExecution
import Formal.DAGSpectral.CoverProducer
import Mathlib.Data.List.Sublists

/-! Executed subset enumeration and output deduplication. Counters use the
schoolbook operation model of the profile DP, not Lean evaluator timings. -/
namespace DAGSpectral.CoverBitCost

def pathEqualCounted {m : ℕ} : List (Fin m) → List (Fin m) → Bool × ℕ
  | [], [] => (true,1)
  | [], _::_ => (false,1)
  | _::_, [] => (false,1)
  | a::as, b::bs =>
    let tail := pathEqualCounted as bs
    (decide (a=b) && tail.1,tail.2+(m+1))

@[simp] theorem pathEqualCounted_value {m : ℕ} (a b : List (Fin m)) :
    (pathEqualCounted a b).1 = decide (a=b) := by
  induction a generalizing b with
  | nil => cases b <;> simp [pathEqualCounted]
  | cons x xs ih => cases b <;> simp [pathEqualCounted,ih]

theorem pathEqualCounted_bound {m : ℕ} (a b : List (Fin m)) :
    (pathEqualCounted a b).2 ≤ (a.length+b.length+1)*(m+1) := by
  induction a generalizing b with
  | nil => cases b <;> simp only [pathEqualCounted,List.length_nil,List.length_cons] <;> nlinarith
  | cons x xs ih =>
    cases b with
    | nil => simp only [pathEqualCounted,List.length_nil,List.length_cons]; dsimp; nlinarith
    | cons y ys =>
      have h := ih ys
      simp only [pathEqualCounted,List.length_cons]
      nlinarith

/-- Full scan of the previously stored paths. -/
def absentCounted {m : ℕ} (a : List (Fin m)) : List (List (Fin m)) → Bool × ℕ
  | [] => (true,1)
  | b::xs =>
    let comparison := pathEqualCounted a b
    let rest := absentCounted a xs
    (!comparison.1 && rest.1,comparison.2+rest.2+1)

@[simp] theorem absentCounted_value {m : ℕ} (a : List (Fin m))
    (xs : List (List (Fin m))) : (absentCounted a xs).1 = decide (a ∉ xs) := by
  induction xs with
  | nil => simp [absentCounted]
  | cons b xs ih => simp [absentCounted,ih]

theorem absentCounted_bound {m N : ℕ} (a : List (Fin m))
    (xs : List (List (Fin m))) (ha : a.length ≤ N)
    (hx : ∀ b ∈ xs, b.length ≤ N) :
    (absentCounted a xs).2 ≤ 1+xs.length*((2*N+1)*(m+1)+1) := by
  induction xs with
  | nil => simp [absentCounted]
  | cons b xs ih =>
    have hb := pathEqualCounted_bound a b
    have hbn := hx b (by simp)
    have ht := ih (fun c hc => hx c (by simp [hc]))
    simp only [absentCounted,List.length_cons]
    nlinarith

/-- Construct the output list while executing equality tests and charging copies. -/
def dedupCounted {m : ℕ} : List (List (Fin m)) → List (List (Fin m)) × ℕ
  | [] => ([],1)
  | a::xs =>
    let rest := dedupCounted xs
    let absent := absentCounted a rest.1
    if absent.1 then
      (a::rest.1,rest.2+absent.2+a.length*(m+1)+1)
    else (rest.1,rest.2+absent.2+1)

@[simp] theorem dedupCounted_value {m : ℕ} (xs : List (List (Fin m))) :
    (dedupCounted xs).1 = xs.dedup := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp [dedupCounted,ih,List.dedup_cons]
    split_ifs <;> rfl

@[simp] theorem dedupCounted_finset {m : ℕ} (xs : List (List (Fin m))) :
    (dedupCounted xs).1.toFinset = xs.toFinset := by
  ext a
  simp

theorem dedupCounted_bound {m N : ℕ} (xs : List (List (Fin m)))
    (hx : ∀ a ∈ xs, a.length ≤ N) :
    (dedupCounted xs).2 ≤
      (xs.length+1)^2*((2*N+1)*(m+1)+N*(m+1)+3) := by
  induction xs with
  | nil => simp [dedupCounted]
  | cons a xs ih =>
    have ha := hx a (by simp)
    have ht := ih (fun b hb => hx b (by simp [hb]))
    have hab := absentCounted_bound a (dedupCounted xs).1 ha (by
      intro b hb
      simp only [dedupCounted_value,List.mem_dedup] at hb
      exact hx b (by simp [hb]))
    have hl : (dedupCounted xs).1.length ≤ xs.length := by
      simpa using (List.dedup_sublist xs).length_le
    have hab' := hab.trans (Nat.add_le_add_left
      (Nat.mul_le_mul_right ((2*N+1)*(m+1)+1) hl) 1)
    have hcopy := Nat.mul_le_mul_right (m+1) ha
    let K := (2*N+1)*(m+1)+N*(m+1)+3
    change (dedupCounted xs).2 ≤ (xs.length+1)^2*K at ht
    have hK : 1 ≤ K := by dsimp [K]; omega
    have hA : (2*N+1)*(m+1)+1 ≤ K := by dsimp [K]; omega
    have hC : N*(m+1)+1 ≤ K := by dsimp [K]; omega
    have habK : (absentCounted a (dedupCounted xs).1).2 ≤ (xs.length+1)*K := by
      calc
        _ ≤ 1+xs.length*((2*N+1)*(m+1)+1) := hab'
        _ ≤ K+xs.length*K := Nat.add_le_add hK (Nat.mul_le_mul_left _ hA)
        _ = _ := by ring
    have htotal : (xs.length+1)^2*K+(xs.length+1)*K+K ≤
        (xs.length+1+1)^2*K := by
      calc
        _ = ((xs.length+1)^2+(xs.length+1)+1)*K := by ring
        _ ≤ _ := Nat.mul_le_mul_right K (by nlinarith)
    change (dedupCounted (a::xs)).2 ≤ (xs.length+1+1)^2*K
    simp only [dedupCounted]
    split_ifs <;> dsimp
    · exact (by omega : _ ≤ (xs.length+1)^2*K+(xs.length+1)*K+K).trans htotal
    · exact (by omega : _ ≤ (xs.length+1)^2*K+(xs.length+1)*K+K).trans htotal

/-- Actual include/exclude recursion; the counter charges list-cell copies. -/
def sublistsCounted {α : Type*} : ℕ → List α → List (List α) × ℕ
  | 0, _ => ([[]],1)
  | _+1, [] => ([],1)
  | r+1, a::xs =>
    let excluded := sublistsCounted (r+1) xs
    let included := sublistsCounted r xs
    (excluded.1 ++ included.1.map (a::·),
      excluded.2+included.2+excluded.1.length+included.1.length*(r+2)+1)

@[simp] theorem sublistsCounted_value {α : Type*} (r : ℕ) (xs : List α) :
    (sublistsCounted r xs).1 = xs.sublistsLen r := by
  induction xs generalizing r with
  | nil => cases r <;> rfl
  | cons a xs ih =>
    cases r with
    | zero => simp [sublistsCounted]
    | succ r => simp [sublistsCounted,ih,List.sublistsLen_succ_cons]

@[simp] theorem sublistsCounted_length {α : Type*} (r : ℕ) (xs : List α) :
    (sublistsCounted r xs).1.length = xs.length.choose r := by
  simp [List.length_sublistsLen]

/-- Copy a path's edge identifiers into a fresh list. -/
def copyPathCounted {m : ℕ} : List (Fin m) → List (Fin m) × ℕ
  | [] => ([],1)
  | e::es => let tail := copyPathCounted es
            (e::tail.1,tail.2+(m+1))

@[simp] theorem copyPathCounted_value {m : ℕ} (es : List (Fin m)) :
    (copyPathCounted es).1 = es := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [copyPathCounted,ih]

@[simp] theorem copyPathCounted_work {m : ℕ} (es : List (Fin m)) :
    (copyPathCounted es).2 = 1+es.length*(m+1) := by
  induction es with
  | nil => simp [copyPathCounted]
  | cons e es ih => simp [copyPathCounted,ih]; ring

/-- Concatenation copies the first list and its path contents. -/
def appendPathsCounted {m : ℕ} :
    List (List (Fin m)) → List (List (Fin m)) → List (List (Fin m)) × ℕ
  | [], ys => (ys,1)
  | a::xs, ys =>
    let path := copyPathCounted a
    let tail := appendPathsCounted xs ys
    (path.1::tail.1,path.2+tail.2+1)

@[simp] theorem appendPathsCounted_value {m : ℕ}
    (xs ys : List (List (Fin m))) : (appendPathsCounted xs ys).1 = xs++ys := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp [appendPathsCounted,ih]

theorem appendPathsCounted_bound {m N : ℕ} (xs ys : List (List (Fin m)))
    (h : ∀ a ∈ xs, a.length ≤ N) :
    (appendPathsCounted xs ys).2 ≤ 1+xs.length*(N*(m+1)+2) := by
  induction xs with
  | nil => simp [appendPathsCounted]
  | cons a xs ih =>
    have ha := Nat.mul_le_mul_right (m+1) (h a (by simp))
    have ht := ih (fun b hb => h b (by simp [hb]))
    simp only [appendPathsCounted,copyPathCounted_work,List.length_cons]
    nlinarith

/-- Execute every trial and explicitly copy its returned paths into the union list. -/
def collectRuns {α : Type*} {m : ℕ} (run : α → List (List (Fin m)) × ℕ) :
    List α → List (List (Fin m)) × ℕ
  | [] => ([],1)
  | a::xs =>
    let head := run a
    let tail := collectRuns run xs
    let combined := appendPathsCounted head.1 tail.1
    (combined.1,head.2+tail.2+combined.2+1)

@[simp] theorem collectRuns_value {α : Type*} {m : ℕ}
    (run : α → List (List (Fin m)) × ℕ) (xs : List α) :
    (collectRuns run xs).1 = xs.flatMap (fun a => (run a).1) := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp [collectRuns,ih]

theorem collectRuns_bound {α : Type*} {m N S K : ℕ}
    (run : α → List (List (Fin m)) × ℕ) (xs : List α)
    (hwork : ∀ a ∈ xs, (run a).2 ≤ K)
    (hcount : ∀ a ∈ xs, (run a).1.length ≤ S)
    (hpath : ∀ a ∈ xs, ∀ es ∈ (run a).1, es.length ≤ N) :
    (collectRuns run xs).2 ≤ 1+xs.length*(K+S*(N*(m+1)+2)+2) := by
  induction xs with
  | nil => simp [collectRuns]
  | cons a xs ih =>
    have hw := hwork a (by simp)
    have hc := hcount a (by simp)
    have hap := appendPathsCounted_bound (run a).1 (collectRuns run xs).1
      (hpath a (by simp))
    have hap' := hap.trans (Nat.add_le_add_left
      (Nat.mul_le_mul_right (N*(m+1)+2) hc) 1)
    have ht := ih (fun b hb => hwork b (by simp [hb]))
      (fun b hb => hcount b (by simp [hb])) (fun b hb => hpath b (by simp [hb]))
    simp only [collectRuns,List.length_cons]
    nlinarith

theorem collectRuns_length {α : Type*} {m S : ℕ}
    (run : α → List (List (Fin m)) × ℕ) (xs : List α)
    (hcount : ∀ a ∈ xs, (run a).1.length ≤ S) :
    (collectRuns run xs).1.length ≤ xs.length*S := by
  induction xs with
  | nil => simp [collectRuns]
  | cons a xs ih =>
    have ha := hcount a (by simp)
    have ht := ih (fun b hb => hcount b (by simp [hb]))
    simp only [collectRuns,appendPathsCounted_value,List.length_append,List.length_cons]
    nlinarith

end DAGSpectral.CoverBitCost
