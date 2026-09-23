import Formal.DAGSpectral.CriterionSelectMatrixTrace
import Formal.DAGSpectral.PathInformationBits

namespace DAGSpectral
open ReciprocalAnchor Matrix

/-- Evaluate and store each rational matrix entry once before returning the
matrix and its concatenated addition trace. -/
def rationalPathRun {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) :
    Matrix (Fin p) (Fin p) ℚ × List ArithmeticEvent :=
  let rows := List.ofFn fun i => List.ofFn fun j => rationalPathEntryRun Q0 Q es i j
  ((fun i j => ((rows[i]'(by simp [rows]))[j]'(by simp [rows])).1),
    rows.flatMap fun row => row.flatMap Prod.snd)

@[simp] theorem rationalPathRun_value {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) :
    (rationalPathRun Q0 Q es).1 = rationalPathInformation Q0 Q es := by
  ext i j
  simp [rationalPathRun,rationalPathEntryRun_value]

@[simp] theorem rationalPathRun_length {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) :
    (rationalPathRun Q0 Q es).2.length = p*p*(es.length+1) := by
  simp [rationalPathRun,List.length_flatMap,rationalPathEntryRun,rationalSumRun_length,
    Function.comp_def]
  ring

theorem rationalPathRun_bits {p m B N : ℕ} {Q0 : Matrix (Fin p) (Fin p) ℚ}
    {Q : Fin m → Matrix (Fin p) (Fin p) ℚ} (h0 : MatrixBits Q0 B)
    (hQ : ∀ e, MatrixBits (Q e) B) (es : List (Fin m)) (he : es.length ≤ N) :
    ∀ e ∈ (rationalPathRun Q0 Q es).2, eventBits (1 + (N + 1) * (B + 1)) e := by
  intro e he'
  change e ∈ (List.ofFn fun i => List.ofFn fun j => rationalPathEntryRun Q0 Q es i j).flatMap
    (fun row => row.flatMap Prod.snd) at he'
  obtain ⟨row,hr,he'⟩ := List.mem_flatMap.mp he'
  obtain ⟨i,rfl⟩ := List.mem_ofFn.mp hr
  obtain ⟨entry,hentry,he'⟩ := List.mem_flatMap.mp he'
  obtain ⟨j,rfl⟩ := List.mem_ofFn.mp hentry
  have hh := rationalSumRun_bits (qs := Q0 i j :: es.map (fun e => Q e i j))
    (B := B) (by
      intro q hq
      rcases List.mem_cons.mp hq with rfl | hq
      · exact h0 i j
      · obtain ⟨a,_,rfl⟩ := List.mem_map.mp hq
        exact hQ a i j)
  exact eventBits_mono (hh e he') (by
    simp only [List.length_cons,List.length_map]
    gcongr)

/-- A path comparator computes the two path matrices, then invokes the exact
criterion comparator. Only retained candidates are evaluated. -/
def pathComparisonRun {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent) (a b : List (Fin m)) : Bool × List ArithmeticEvent :=
  let x := rationalPathRun Q0 Q a
  let y := rationalPathRun Q0 Q b
  let c := compare x.1 y.1
  (c.1,x.2++y.2++c.2)

@[simp] theorem pathComparisonRun_value {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (compare) (a b : List (Fin m)) :
    (pathComparisonRun Q0 Q compare a b).1 =
      (compare (rationalPathInformation Q0 Q a) (rationalPathInformation Q0 Q b)).1 := by
  simp [pathComparisonRun]

theorem pathComparisonRun_bounds {p m B N C K : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent)
    (hK : 1 + (N + 1) * (B + 1) ≤ K)
    (hcompare : ∀ A, MatrixBits A (1 + (N + 1) * (B + 1)) →
      ∀ D, MatrixBits D (1 + (N + 1) * (B + 1)) →
      (compare A D).2.length ≤ C ∧ ∀ e ∈ (compare A D).2, eventBits K e)
    (a b : List (Fin m)) (ha : a.length ≤ N) (hb : b.length ≤ N) :
    (pathComparisonRun Q0 Q compare a b).2.length ≤ 2*(p*p*(N+1))+C ∧
    ∀ e ∈ (pathComparisonRun Q0 Q compare a b).2, eventBits K e := by
  have hc := hcompare _ (rationalPathInformation_bits h0 hQ a ha)
    _ (rationalPathInformation_bits h0 hQ b hb)
  simp only [pathComparisonRun,rationalPathRun_value,List.length_append]
  constructor
  · rw [rationalPathRun_length,rationalPathRun_length]
    have h1 := Nat.mul_le_mul_left (p*p) (Nat.add_le_add_right ha 1)
    have h2 := Nat.mul_le_mul_left (p*p) (Nat.add_le_add_right hb 1)
    omega
  · intro e he
    rcases List.mem_append.mp he with he | he
    · rcases List.mem_append.mp he with he | he
      · exact eventBits_mono (rationalPathRun_bits h0 hQ a ha e he) hK
      · exact eventBits_mono (rationalPathRun_bits h0 hQ b hb e he) hK
    · exact hc.2 e he

def selectPathsRun {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (compare : Matrix (Fin p) (Fin p) ℚ → Matrix (Fin p) (Fin p) ℚ →
      Bool × List ArithmeticEvent)
    (xs : List (List (Fin m))) : Option (List (Fin m)) × List ArithmeticEvent :=
  bestByRun (pathComparisonRun Q0 Q compare) xs

theorem selectPathsRun_result {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (compare) (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q compare xs).1 = bestBy
      (fun a b => (compare (rationalPathInformation Q0 Q a)
        (rationalPathInformation Q0 Q b)).1) xs := by
  simp only [selectPathsRun,bestByRun_result,pathComparisonRun_value]

theorem selectPathsRun_bitWork {p m B N C K : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B) (compare)
    (hK : 1 + (N + 1) * (B + 1) ≤ K)
    (hcompare : ∀ A, MatrixBits A (1 + (N + 1) * (B + 1)) →
      ∀ D, MatrixBits D (1 + (N + 1) * (B + 1)) →
      (compare A D).2.length ≤ C ∧ ∀ e ∈ (compare A D).2, eventBits K e)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    traceBitWork K (selectPathsRun Q0 Q compare xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+C)*(256*(K+1)^3) :=
  bestByRun_bitWork _ (fun a => a.length ≤ N)
    (fun a ha b hb => pathComparisonRun_bounds h0 hQ compare hK hcompare a b ha hb) xs hxs

@[simp] theorem selectPathsRun_determinant {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q determinantLERun xs).1 =
      selectDeterminant (rationalPathInformation Q0 Q) xs := by
  simp only [selectPathsRun_result,determinantLERun_result,selectDeterminant]

@[simp] theorem selectPathsRun_inverseTrace {p m : ℕ}
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (xs : List (List (Fin m))) :
    (selectPathsRun Q0 Q (fun a b => inverseTraceCostLERun b a) xs).1 =
      selectInverseTrace (rationalPathInformation Q0 Q) xs := by
  simp only [selectPathsRun_result,inverseTraceCostLERun_result,selectInverseTrace]

theorem selectPathsRun_determinant_bitWork {p m B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    let K := arithmeticWidth (2*determinantOperations p+1) (1 + (N + 1) * (B + 1))
    traceBitWork K (selectPathsRun Q0 Q determinantLERun xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+(2*determinantOperations p+1))*(256*(K+1)^3) := by
  apply selectPathsRun_bitWork h0 hQ determinantLERun
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA D hD
    exact determinantLERun_bounds (by omega) hA hD
  · exact hxs

theorem selectPathsRun_inverseTrace_bitWork {p m B N : ℕ}
    {Q0 : Matrix (Fin p) (Fin p) ℚ} {Q : Fin m → Matrix (Fin p) (Fin p) ℚ}
    (h0 : MatrixBits Q0 B) (hQ : ∀ e, MatrixBits (Q e) B)
    (xs : List (List (Fin m))) (hxs : ∀ a ∈ xs, a.length ≤ N) :
    let K := arithmeticWidth (inverseTraceCompareOperations p) (1 + (N + 1) * (B + 1))
    traceBitWork K (selectPathsRun Q0 Q (fun a b => inverseTraceCostLERun b a) xs).2 ≤
      (xs.length-1)*(2*(p*p*(N+1))+inverseTraceCompareOperations p)*(256*(K+1)^3) := by
  apply selectPathsRun_bitWork h0 hQ (fun a b => inverseTraceCostLERun b a)
  · exact (arithmeticWidth_zero _).symm.le.trans (arithmeticWidth_mono (Nat.zero_le _))
  · intro A hA D hD
    exact inverseTraceCostLERun_bounds (by omega) hD hA
  · exact hxs

end DAGSpectral
