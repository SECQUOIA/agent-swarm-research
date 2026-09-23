import Formal.DAGSpectral.RationalStorage
import Formal.DAGSpectral.FactorBits
import Formal.DAGSpectral.NormalizationInput
import Formal.DAGSpectral.CoverNormalizationExecution
import Mathlib.Data.Fin.Tuple.Take

/-! Eager LDL execution and original-input factor caches. Rational coordinates
are materialized in vectors; later indexing does not repeat factorization. -/
namespace DAGSpectral
open Matrix ReciprocalAnchor
open scoped BigOperators
namespace FactorInputExecution
open CoverNormalizationExecution

abbrev StoredFactor (n : ℕ) := ℚ × Vector ℚ n

def factorView {n : ℕ} (f : StoredFactor n) : RationalFactor n := (f.1,f.2.get)

def extendStored {n : ℕ} (f : StoredFactor n) : StoredFactor (n + 1) :=
  (f.1,Vector.ofFn (Fin.cases 0 f.2.get))

@[simp] theorem extendStored_view {n : ℕ} (f : StoredFactor n) :
    factorView (extendStored f) = extendFactor (factorView f) := by
  apply Prod.ext
  · rfl
  · funext i
    simp [factorView,extendStored,extendFactor]

@[simp] private theorem vector_get_ofFn {n : ℕ} (f : Fin n → ℚ) :
    (Vector.ofFn f).get = f := by funext i; simp

/-- Exact signed numerator/denominator storage charge. -/
abbrev scalarCopy := RationalStorage.scalarCopy

abbrev vectorCopy := @RationalStorage.vectorCopy
abbrev matrixCopy {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) : ℕ := RationalStorage.matrixCopy A
def factorCopy {n : ℕ} (f : StoredFactor n) : ℕ := scalarCopy f.1+vectorCopy f.2.get+1

def extendStoredCounted {n : ℕ} : List (StoredFactor n) → List (StoredFactor (n + 1)) × ℕ
  | [] => ([],1)
  | f::fs =>
      let g := extendStored f
      let tail := extendStoredCounted fs
      (g::tail.1, factorCopy g+tail.2+1)

@[simp] theorem extendStoredCounted_value {n : ℕ} (fs : List (StoredFactor n)) :
    (extendStoredCounted fs).1 = fs.map extendStored := by
  induction fs with
  | nil => rfl
  | cons f fs ih => simp [extendStoredCounted,ih]

private def schurExpr {n : ℕ} (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ)
    (i j : Fin n) : ArithmeticExpr :=
  .op .sub (.atom (A i.succ j.succ))
    (.op .div (.op .mul (.atom (A i.succ 0)) (.atom (A 0 j.succ))) (.atom (A 0 0)))

@[simp] private theorem schurExpr_eval {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) (i j : Fin n) :
    (schurExpr A i j).eval = rationalSchur A i j := rfl

private theorem schurExpr_trace {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) (i j : Fin n) :
    (schurExpr A i j).trace = schurEntryTrace A i j := by
  simp [schurExpr,ArithmeticExpr.trace,ArithmeticExpr.eval,primitiveResult,schurEntryTrace]

@[simp] private theorem materializedMatrix_copies {l m : ℕ}
    (E : Fin l → Fin m → ArithmeticExpr) :
    (runMatrix E).copies = 2*RationalStorage.matrixCopy (runMatrix E).value+
      2*(l+1)*(m+1) := by
  simp [runMatrix,RationalStorage.matrixCopy,RationalStorage.vectorCopy,
    ArithmeticExpr.run_eq,MatrixRun.value]

@[simp] private theorem runSchur_value {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    (runMatrix (schurExpr A)).value = rationalSchur A := by ext i j; simp

@[simp] private theorem runTail_value {n : ℕ}
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℚ) :
    (runMatrix (fun i j : Fin n => ArithmeticExpr.atom (A i.succ j.succ))).value =
      A.submatrix Fin.succ Fin.succ := by ext i j; simp [ArithmeticExpr.eval]

@[simp] private theorem map_extend_views {n : ℕ} (fs : List (StoredFactor n)) :
    (fs.map extendStored).map factorView = (fs.map factorView).map extendFactor := by
  simp [List.map_map,Function.comp_def]

structure LDLRun (n : ℕ) where
  factors : List (StoredFactor n)
  events : List ArithmeticEvent
  copies : ℕ

/-- Every recursive matrix and leading factor column is stored before use.
The pivot uses exact reduced-rational equality, whose digit scan is charged
in `copies`. The extra `.compare` event is a conservative arithmetic charge;
its less-than-or-equal result is not used to decide the equality branch. -/
def ldlRun : (n : ℕ) → Matrix (Fin n) (Fin n) ℚ → LDLRun n
  | 0, _ => ⟨[],[],1⟩
  | n+1, A =>
      if A 0 0 = 0 then
        let S := runMatrix (fun i j : Fin n => ArithmeticExpr.atom (A i.succ j.succ))
        let tail := ldlRun n S.value
        let extended := extendStoredCounted tail.factors
        ⟨extended.1, (.compare,A 0 0,0)::tail.events,
          matrixCopy A + S.copies + extended.2 + tail.copies+scalarCopy (A 0 0)+1⟩
      else
        let column := Vector.ofFn fun i : Fin (n + 1) =>
          (ArithmeticExpr.op .div (.atom (A i 0)) (.atom (A 0 0))).run
        let lead : StoredFactor (n + 1) := (A 0 0,column.map Prod.fst)
        let S := runMatrix (schurExpr A)
        let tail := ldlRun n S.value
        let extended := extendStoredCounted tail.factors
        ⟨lead::extended.1,
          (.compare,A 0 0,0)::((List.ofFn fun i => (column.get i).2).flatten ++
            S.events ++ tail.events),
          matrixCopy A + S.copies + 2*factorCopy lead + 2*(n+2) + extended.2 +
          tail.copies+scalarCopy (A 0 0)+1⟩

@[simp] theorem ldlRun_factors (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    ((ldlRun n A).factors.map factorView) = rationalLDL n A := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [ldlRun,rationalLDL]
    split
    · simp only [extendStoredCounted_value,map_extend_views,runTail_value,ih]
    · simp only [List.map_cons,extendStoredCounted_value,map_extend_views,runSchur_value,ih]
      congr 1
      simp [factorView,ArithmeticExpr.run_eq,ArithmeticExpr.eval,primitiveResult,Function.comp_def]

@[simp] theorem ldlRun_events (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    (ldlRun n A).events = rationalLDLTrace n A := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [ldlRun,rationalLDLTrace]
    split
    · simp only [runTail_value,ih]
    · simp only [runSchur_value,ih]
      simp [ArithmeticExpr.run_eq,ArithmeticExpr.trace,ArithmeticExpr.eval,primitiveResult,
        factorDivisionTrace,runMatrix_events,matrixExprTrace,schurTrace,schurExpr_trace,
        flatten_ofFn_singletons]

/-- Executed values and events agree simultaneously with the earlier instrumented LDL. -/
theorem ldlRun_eq_instrumented (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    ((ldlRun n A).factors.map factorView,(ldlRun n A).events) = rationalLDLWithTrace n A := by
  simp [rationalLDLWithTrace_eq]

private theorem flatten_get_offset {α : Type*} (rows : List (List α))
    (i : Fin rows.length) (j : Fin (rows.get i).length) :
    rows.flatten[((rows.map List.length).take i).sum+j]? = some ((rows.get i).get j) := by
  induction rows with
  | nil => exact Fin.elim0 i
  | cons xs rows ih =>
    revert j
    refine Fin.cases ?_ (fun k => ?_) i
    · intro j
      change Fin xs.length at j
      simp only [Fin.val_zero,List.take_zero,List.sum_nil,zero_add,List.flatten_cons]
      change (xs++rows.flatten)[j.val]? = some (xs.get j)
      rw [List.getElem?_append_left j.isLt]
      simp
    · intro j
      change Fin (rows.get k).length at j
      change (xs++rows.flatten)[xs.length+((rows.map List.length).take k).sum+j.val]? =
        some ((rows.get k).get j)
      rw [List.getElem?_append_right (by omega)]
      convert ih k j using 1; congr 1; omega

private theorem prefix_ofFn_sum {m : ℕ} (f : Fin m → ℕ) (k : Fin m) :
    ((List.ofFn f).take k).sum = ∑ i : Fin k, f (Fin.castLE k.isLt.le i) := by
  rw [← Fin.ofFn_take_eq_take_ofFn k.isLt.le, List.sum_ofFn]
  rfl

/-- Exact owner/local offset in a flattened list, using the same public label index. -/
theorem flattened_get_index {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) :
    let rows := List.ofFn fun o => (rationalLDL n (A o)).map (fun f => (o,f))
    rows.flatten[(indexedFactorEquiv A k).val]? =
      some (k.1,(rationalLDL n (A k.1)).get k.2) := by
  let rows := List.ofFn fun o => (rationalLDL n (A o)).map (fun f => (o,f))
  let i : Fin rows.length := ⟨k.1.val,by simp [rows]⟩
  have hj : (rows.get i).length = (rationalLDL n (A k.1)).length := by simp [rows,i]
  let j : Fin (rows.get i).length := k.2.cast hj.symm
  have h := flatten_get_offset rows i j
  have hp : ((rows.map List.length).take i).sum =
      ∑ z : Fin k.1, (rationalLDL n (A (Fin.castLE k.1.isLt.le z))).length := by
    simpa [rows,i,List.map_ofFn,Function.comp_def] using
      prefix_ofFn_sum (fun o => (rationalLDL n (A o)).length) k.1
  rw [hp] at h
  simpa [rows,i,j,indexedFactorEquiv_apply] using h

structure InputRun (n m : ℕ) where
  factors : List (Fin m × StoredFactor n)
  events : List ArithmeticEvent
  copies : ℕ

def tagFactorsCounted {n m : ℕ} (o : Fin m) :
    List (StoredFactor n) → List (Fin m × StoredFactor n) × ℕ
  | [] => ([],1)
  | f::fs =>
      let tail := tagFactorsCounted o fs
      ((o,f)::tail.1,factorCopy f+o.val.size+2+tail.2)

@[simp] theorem tagFactorsCounted_value {n m : ℕ} (o : Fin m) (fs : List (StoredFactor n)) :
    (tagFactorsCounted o fs).1 = fs.map (fun f => (o,f)) := by
  induction fs with
  | nil => rfl
  | cons f fs ih => simp [tagFactorsCounted,ih]

/-- Execute LDL once per owner and store its factors before constructing labels.
All input owners, including a zero or singular prior, use the same finite loop. -/
def inputRun {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) : InputRun n m :=
  let results := Vector.ofFn fun o => ldlRun n (A o)
  let labeled := Vector.ofFn fun o => tagFactorsCounted o (results.get o).factors
  { factors := (List.ofFn fun o => (labeled.get o).1).flatten
    events := (List.ofFn fun o => (results.get o).events).flatten
    copies := (∑ o : Fin m, ((results.get o).copies+(labeled.get o).2))+m+1 }

theorem inputRun_views {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    (inputRun A).factors.map (fun f => (f.1,factorView f.2)) =
      (List.ofFn fun o => (rationalLDL n (A o)).map (fun f => (o,f))).flatten := by
  simp only [inputRun,Vector.get_ofFn,tagFactorsCounted_value,List.map_flatten,List.map_ofFn]
  congr 2
  funext o
  dsimp only [Function.comp_def]
  rw [List.map_map]
  rw [← ldlRun_factors]
  simp only [List.map_map,Function.comp_def]

@[simp] theorem inputRun_events {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    (inputRun A).events = (List.ofFn fun o => rationalLDLTrace n (A o)).flatten := by
  simp [inputRun]

theorem inputRun_count {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    (inputRun A).factors.length = indexedFactorCount A := by
  have h := congrArg List.length (inputRun_views A)
  simpa [List.length_flatten,List.map_ofFn,Function.comp_def,List.sum_ofFn,
    indexedFactorCount] using h

/-- Cached access uses the same integer labels as the original-input construction. -/
theorem inputRun_indexed {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) :
    ((inputRun A).factors[k.val]?).map (fun f => (f.1,factorView f.2)) =
      some (indexedFactorOwner A k,(indexedFactorWeight A k,indexedFactorVector A k)) := by
  have h := flattened_get_index A ((indexedFactorEquiv A).symm k)
  dsimp only at h
  rw [← inputRun_views A] at h
  simpa only [List.getElem?_map,Equiv.apply_symm_apply,indexedFactorOwner,
    indexedFactorWeight,indexedFactorVector,factorOwner,factorWeight,factorVector] using h

def inputRunAt {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) : Fin m × StoredFactor n :=
  (inputRun A).factors.get ⟨k.val,by rw [inputRun_count]; exact k.isLt⟩

theorem inputRunAt_value {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) :
    ((inputRunAt A k).1,factorView (inputRunAt A k).2) =
      (indexedFactorOwner A k,(indexedFactorWeight A k,indexedFactorVector A k)) := by
  have h := inputRun_indexed A k
  have hk : k.val < (inputRun A).factors.length := by rw [inputRun_count]; exact k.isLt
  rw [List.getElem?_eq_getElem hk] at h
  exact Option.some.inj h

def StoredFactorBits {n : ℕ} (f : StoredFactor n) (B : ℕ) : Prop :=
  RationalBits f.1 B ∧ ∀ i, RationalBits (f.2.get i) B

theorem scalarCopy_le {q : ℚ} {B : ℕ} (h : RationalBits q B) : scalarCopy q ≤ 2*B+1 := by
  have hh := (rationalBits_iff_size q B).mp h
  unfold scalarCopy RationalStorage.scalarCopy
  omega

theorem vectorCopy_le {n B : ℕ} {x : Fin n → ℚ} (h : ∀ i, RationalBits (x i) B) :
    vectorCopy x ≤ n*(2*B+1) := by
  exact (Finset.sum_le_sum (fun i _ => scalarCopy_le (h i))).trans (by simp)

theorem matrixCopy_le {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (h : MatrixBits A B) : matrixCopy A ≤ n*n*(2*B+1) := by
  have hh := Finset.sum_le_sum (s := Finset.univ) (fun i _ => vectorCopy_le (h i))
  simpa only [matrixCopy,RationalStorage.matrixCopy,Finset.sum_const,
    Finset.card_univ,Fintype.card_fin,
    nsmul_eq_mul,Nat.cast_id,Nat.mul_assoc] using hh

theorem factorCopy_le {n B : ℕ} {f : StoredFactor n} (h : StoredFactorBits f B) :
    factorCopy f ≤ (n+1)*(2*B+1)+1 := by
  have hw := scalarCopy_le h.1
  have hv := vectorCopy_le h.2
  unfold factorCopy
  nlinarith

theorem ldlRun_bits {n B : ℕ} {A : Matrix (Fin n) (Fin n) ℚ} (h : MatrixBits A B) :
    ∀ f ∈ (ldlRun n A).factors, StoredFactorBits f (factorBits n B) := by
  intro f hf
  have hm : factorView f ∈ rationalLDL n A := by
    rw [← ldlRun_factors]
    exact List.mem_map.mpr ⟨f,hf,rfl⟩
  exact rationalLDL_bits n B A h _ hm

theorem ldlRun_length (n : ℕ) (A : Matrix (Fin n) (Fin n) ℚ) :
    (ldlRun n A).factors.length ≤ n := by
  have hh := congrArg List.length (ldlRun_factors n A)
  simp only [List.length_map] at hh
  rw [hh]
  exact rationalLDL_length_le n A

private theorem stored_bits_mono {n B C : ℕ} {f : StoredFactor n}
    (h : StoredFactorBits f B) (hBC : B ≤ C) : StoredFactorBits f C :=
  ⟨rationalBits_mono h.1 hBC,fun i => rationalBits_mono (h.2 i) hBC⟩

private theorem extendStored_bits {n B : ℕ} {f : StoredFactor n}
    (h : StoredFactorBits f B) (hB : 1 ≤ B) : StoredFactorBits (extendStored f) B := by
  refine ⟨h.1,fun i => ?_⟩
  refine Fin.cases ?_ (fun j => ?_) i
  · simpa [extendStored] using rationalBits_mono rationalBits_zero hB
  · simpa [extendStored] using h.2 j

theorem extendStoredCounted_copies {n B : ℕ} (fs : List (StoredFactor n))
    (hf : ∀ f ∈ fs, StoredFactorBits f B) (hB : 1 ≤ B) :
    (extendStoredCounted fs).2 ≤ 1+fs.length*((n+2)*(2*B+1)+2) := by
  induction fs with
  | nil => simp [extendStoredCounted]
  | cons f fs ih =>
    have h1 := factorCopy_le (extendStored_bits (hf f (by simp)) hB)
    have ht := ih (fun g hg => hf g (by simp [hg]))
    simp only [extendStoredCounted,List.length_cons]
    nlinarith

/-- Dimension-only coefficient for matrix scans, factor extension and control. -/
def copySteps : ℕ → ℕ
  | 0 => 1
  | n+1 => copySteps n + 20*(n+2)^3

theorem ldlRun_copies {n B : ℕ} (A : Matrix (Fin n) (Fin n) ℚ) (hA : MatrixBits A B) :
    (ldlRun n A).copies ≤ copySteps n*(2*factorBits n B+3) := by
  induction n generalizing B with
  | zero => simp [ldlRun,copySteps,factorBits]
  | succ n ih =>
    let K := factorBits (n+1) B
    have hK : 1 ≤ K := factorBits_pos _ _
    have hAK : MatrixBits A K := fun i j => rationalBits_mono (hA i j) (factorBits_input _ _)
    have hAc := matrixCopy_le hAK
    have hpc := scalarCopy_le (hAK 0 0)
    have assemble (S : Matrix (Fin n) (Fin n) ℚ) (C : ℕ)
        (hS : MatrixBits S C) (hCK : factorBits n C ≤ K) :
        (2*matrixCopy S+2*(n+1)*(n+1)) +
          (extendStoredCounted (ldlRun n S).factors).2+(ldlRun n S).copies ≤
          (2*(n*n*(2*K+1))+2*(n+1)*(n+1)) +
            (1+n*((n+2)*(2*K+1)+2))+copySteps n*(2*K+3) := by
      have hSK : MatrixBits S K := fun i j =>
        rationalBits_mono (hS i j) ((factorBits_input n C).trans hCK)
      have hs := matrixCopy_le hSK
      have ht := (ih S hS).trans (Nat.mul_le_mul_left _ (by omega : 2*factorBits n C+3 ≤ 2*K+3))
      have he := extendStoredCounted_copies (ldlRun n S).factors
        (fun f hf => stored_bits_mono (ldlRun_bits hS f hf) hCK) hK
      have hn := ldlRun_length n S
      have he' := he.trans (Nat.add_le_add_left (Nat.mul_le_mul_right _ hn) 1)
      omega
    by_cases hz : A 0 0 = 0
    · have hs := assemble (A.submatrix Fin.succ Fin.succ) B
        (fun i j => hA i.succ j.succ) (factorBits_mono_dim n B)
      simp only [ldlRun,if_pos hz,materializedMatrix_copies,runTail_value]
      change _ ≤ (copySteps n+20*(n+2)^3)*(2*K+3)
      nlinarith
    · have hs := assemble (rationalSchur A) (4*B+1) (rationalSchur_bits hA) (factorBits_step n B)
      have hlead : factorCopy (A 0 0,Vector.ofFn (fun i => A i 0/A 0 0)) ≤
          (n+2)*(2*K+1)+1 := by
        apply factorCopy_le
        refine ⟨hAK 0 0,fun i => ?_⟩
        simp only [Vector.get_ofFn]
        apply rationalBits_mono (rationalBits_div (hA i 0) (hA 0 0))
        have hb := factorBits_input n (4*B+1)
        have hs := factorBits_step n B
        change B+B ≤ K
        omega
      simp only [ldlRun,if_neg hz,materializedMatrix_copies,runSchur_value]
      simp only [ArithmeticExpr.run_eq,ArithmeticExpr.eval,primitiveResult,
        Vector.map_ofFn,Function.comp_def]
      change _ ≤ (copySteps n+20*(n+2)^3)*(2*K+3)
      nlinarith

theorem inputRun_factorBits {n m B : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, MatrixBits (A o) B) :
    ∀ f ∈ (inputRun A).factors, StoredFactorBits f.2 (factorBits n B) := by
  intro f hf
  have hm : (f.1,factorView f.2) ∈ (inputRun A).factors.map
      (fun g => (g.1,factorView g.2)) := List.mem_map.mpr ⟨f,hf,rfl⟩
  rw [inputRun_views,List.mem_flatten] at hm
  obtain ⟨fs,hfs,hm⟩ := hm
  obtain ⟨o,rfl⟩ := List.mem_ofFn.mp hfs
  obtain ⟨g,hg,he⟩ := List.mem_map.mp hm
  have he' : g = factorView f.2 := congrArg Prod.snd he
  rw [he'] at hg
  exact rationalLDL_bits n B (A o) (hA o) _ hg

/-- Access an already materialized cache; this function performs no LDL work. -/
def InputRun.factorAt {n m : ℕ} (cache : InputRun n m)
    (k : Fin cache.factors.length) : Fin m × StoredFactor n := cache.factors.get k

def cachedLookup {α : Type*} : List α → ℕ → Option α × ℕ
  | [], _ => (none,1)
  | a::_, 0 => (some a,1)
  | _::as, k+1 => let t := cachedLookup as k; (t.1,t.2+1)

theorem cachedLookup_value {α : Type*} (xs : List α) (k : ℕ) :
    (cachedLookup xs k).1 = xs[k]? := by
  induction xs generalizing k with
  | nil => simp [cachedLookup]
  | cons a xs ih => cases k <;> simp [cachedLookup,ih]

theorem cachedLookup_steps {α : Type*} (xs : List α) (k : ℕ) :
    (cachedLookup xs k).2 ≤ xs.length+1 := by
  induction xs generalizing k with
  | nil => simp [cachedLookup]
  | cons a xs ih =>
    cases k with
    | zero => simp [cachedLookup]
    | succ k =>
      simp only [cachedLookup,List.length_cons]
      exact Nat.add_le_add_right (ih k) 1

theorem inputRun_eventBits {n m B : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, MatrixBits (A o) B) :
    ∀ e ∈ (inputRun A).events, eventBits (factorBits n B) e := by
  intro e he
  rw [inputRun_events,List.mem_flatten] at he
  obtain ⟨es,hes,he⟩ := he
  obtain ⟨o,rfl⟩ := List.mem_ofFn.mp hes
  exact rationalLDLTrace_bits n B (A o) (hA o) e he

theorem inputRun_eventLength {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    (inputRun A).events.length ≤ m*factorOperations n := by
  rw [inputRun_events,List.length_flatten,List.map_ofFn,List.sum_ofFn]
  exact (Finset.sum_le_sum (fun o _ => rationalLDLTrace_length_le n (A o))).trans (by simp)

theorem tagFactorsCounted_copies {n m B : ℕ} (o : Fin m) (fs : List (StoredFactor n))
    (hf : ∀ f ∈ fs, StoredFactorBits f B) :
    (tagFactorsCounted o fs).2 ≤ 1+fs.length*((n+1)*(2*B+1)+m+3) := by
  have ho : o.val.size ≤ m := Nat.size_le.mpr (o.isLt.trans_le (Nat.le_of_lt m.lt_two_pow_self))
  induction fs with
  | nil => simp [tagFactorsCounted]
  | cons f fs ih =>
    have h1 := factorCopy_le (hf f (by simp))
    have ht := ih (fun g hg => hf g (by simp [hg]))
    simp only [tagFactorsCounted,List.length_cons]
    nlinarith

def inputCopyBound (n m B : ℕ) : ℕ :=
  m*(copySteps n*(2*factorBits n B+3)+1+n*((n+1)*(2*factorBits n B+1)+m+3))+m+1

theorem inputRun_copies {n m B : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, MatrixBits (A o) B) : (inputRun A).copies ≤ inputCopyBound n m B := by
  have each (o : Fin m) : (ldlRun n (A o)).copies+
      (tagFactorsCounted o (ldlRun n (A o)).factors).2 ≤
        copySteps n*(2*factorBits n B+3)+1+n*((n+1)*(2*factorBits n B+1)+m+3) := by
    have hl := ldlRun_copies (A o) (hA o)
    have ht := tagFactorsCounted_copies o (ldlRun n (A o)).factors (ldlRun_bits (hA o))
    have hn := ldlRun_length n (A o)
    have ht' := ht.trans (Nat.add_le_add_left (Nat.mul_le_mul_right _ hn) 1)
    omega
  have hs := Finset.sum_le_sum (s := Finset.univ) (fun o _ => each o)
  simp only [Finset.sum_const,Finset.card_univ,Fintype.card_fin,nsmul_eq_mul,Nat.cast_id] at hs
  simp only [inputRun,Vector.get_ofFn,inputCopyBound]
  omega

/-- Work charged to a materialized cache, without executing factorization again. -/
def InputRun.bitWork {n m : ℕ} (cache : InputRun n m) (B : ℕ) : ℕ :=
  traceBitWork (factorBits n B) cache.events+cache.copies

def inputBitWork {n m : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ) (B : ℕ) : ℕ :=
  let cache := inputRun A
  cache.bitWork B

theorem inputBitWork_le {n m B : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, MatrixBits (A o) B) :
    inputBitWork A B ≤ m*factorOperations n*(256*(factorBits n B+1)^3)+inputCopyBound n m B := by
  have ht := (traceBitWork_le (inputRun_eventBits A hA)).trans
    (Nat.mul_le_mul_right _ (inputRun_eventLength A))
  exact Nat.add_le_add ht (inputRun_copies A hA)

def inputCopyCoefficient (n : ℕ) : ℕ :=
  copySteps n*(2*4^n+3)+1+n*((n+1)*(2*4^n+1)+4)+2

def inputCoefficient (n : ℕ) : ℕ :=
  factorOperations n*256*(4^n+1)^3+inputCopyCoefficient n

theorem inputCopyBound_polynomial (n m B : ℕ) :
    inputCopyBound n m B ≤ inputCopyCoefficient n*(m+1)^2*(B+1) := by
  let t := (m+1)*(B+1)
  have ht : 1 ≤ t := by dsimp [t]; nlinarith
  have hm : m ≤ t := by dsimp [t]; nlinarith
  have hb : B+1 ≤ t := by dsimp [t]; nlinarith
  have h1 : 2*factorBits n B+3 ≤ (2*4^n+3)*t := by
    unfold factorBits
    nlinarith [Nat.mul_le_mul_left (2*4^n) hb]
  have h2 : 2*factorBits n B+1 ≤ (2*4^n+1)*t := by
    unfold factorBits
    nlinarith [Nat.mul_le_mul_left (2*4^n) hb]
  have hi : copySteps n*(2*factorBits n B+3)+1+
      n*((n+1)*(2*factorBits n B+1)+m+3) ≤ (inputCopyCoefficient n-2)*t := by
    have h1' := Nat.mul_le_mul_left (copySteps n) h1
    have h2' := Nat.mul_le_mul_left (n*(n+1)) h2
    have hm' := Nat.mul_le_mul_left n hm
    unfold inputCopyCoefficient
    simp only [Nat.add_sub_cancel]
    nlinarith
  have houter := Nat.mul_le_mul_left m hi
  unfold inputCopyBound
  have hc : 2 ≤ inputCopyCoefficient n := by unfold inputCopyCoefficient; omega
  have hc' : inputCopyCoefficient n-2+2 = inputCopyCoefficient n := Nat.sub_add_cancel hc
  have ho := houter.trans (Nat.mul_le_mul_right ((inputCopyCoefficient n-2)*t) (Nat.le_succ m))
  have hsmall : m+1 ≤ 2*(m+1)*t := by nlinarith
  calc
    _ ≤ (m+1)*((inputCopyCoefficient n-2)*t)+2*(m+1)*t := Nat.add_le_add ho hsmall
    _ = inputCopyCoefficient n*(m+1)^2*(B+1) := by
      conv_rhs => rw [← hc']
      dsimp [t]
      ring

theorem inputBitWork_polynomial {n m B : ℕ} (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, MatrixBits (A o) B) :
    inputBitWork A B ≤ inputCoefficient n*(m+1)^2*(B+1)^3 := by
  have h := inputBitWork_le A hA
  have hc := inputCopyBound_polynomial n m B
  have hb : factorBits n B+1 ≤ (4^n+1)*(B+1) := by unfold factorBits; nlinarith
  have hp := Nat.pow_le_pow_left hb 3
  have hm : m ≤ (m+1)^2 := by nlinarith
  have hh := Nat.mul_le_mul (Nat.mul_le_mul_right (factorOperations n*256) hm) hp
  have hb3 : B+1 ≤ (B+1)^3 := by nlinarith [sq_nonneg (B:ℤ)]
  have hc' := hc.trans (Nat.mul_le_mul_left (inputCopyCoefficient n*(m+1)^2) hb3)
  unfold inputCoefficient
  nlinarith [hh]

end FactorInputExecution
end DAGSpectral
