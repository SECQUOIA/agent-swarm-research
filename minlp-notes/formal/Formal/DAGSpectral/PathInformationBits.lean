import Formal.DAGSpectral.PathInformation
import Formal.DAGSpectral.RationalMatrixArithmetic

namespace DAGSpectral
open ReciprocalAnchor
open scoped BigOperators

/-- Actual sequential rational summation and its executed addition events. -/
def rationalSumRun : List ℚ → ℚ × List ArithmeticEvent
  | [] => (0, [])
  | q :: qs =>
    let tail := rationalSumRun qs
    (q + tail.1, tail.2 ++ [(.add,q,tail.1)])

theorem rationalSumRun_value (qs : List ℚ) : (rationalSumRun qs).1 = qs.sum := by
  induction qs with
  | nil => rfl
  | cons q qs ih => simp only [rationalSumRun,List.sum_cons,ih]

theorem rationalSumRun_length (qs : List ℚ) : (rationalSumRun qs).2.length = qs.length := by
  induction qs with
  | nil => rfl
  | cons q qs ih => simp [rationalSumRun,ih]

theorem rationalSumRun_bits {qs : List ℚ} {B : ℕ}
    (hq : ∀ q ∈ qs, RationalBits q B) :
    ∀ e ∈ (rationalSumRun qs).2, eventBits (1+qs.length*(B+1)) e := by
  induction qs with
  | nil => simp [rationalSumRun]
  | cons q qs ih =>
    have ht : ∀ q ∈ qs, RationalBits q B := fun q h => hq q (by simp [h])
    intro e he
    simp only [rationalSumRun,List.mem_append,List.mem_singleton] at he
    rcases he with he | rfl
    · obtain ⟨h1,h2⟩ := ih ht e he
      exact ⟨rationalBits_mono h1 (by simp only [List.length_cons]; nlinarith),
        rationalBits_mono h2 (by simp only [List.length_cons]; nlinarith)⟩
    · constructor
      · exact rationalBits_mono (hq q (by simp)) (by simp only [List.length_cons]; nlinarith)
      · rw [rationalSumRun_value]
        exact rationalBits_mono (rationalBits_list_sum ht)
          (by simp only [List.length_cons]; nlinarith)

def rationalPathInformation {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) :
    Matrix (Fin p) (Fin p) ℚ := Q0 + (es.map Q).sum

theorem rationalPathInformation_cast {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) :
    ratMatrixReal (rationalPathInformation Q0 Q es) =
      pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) es := by
  simp only [rationalPathInformation,ratMatrixReal_add,ratMatrixReal_list_sum,pathMatrix]

/-- Finite matrix evaluation runs one addition chain per entry. -/
def rationalPathEntryRun {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) (i j : Fin p) :=
  rationalSumRun (Q0 i j :: es.map (fun e => Q e i j))

theorem rationalPathEntryRun_value {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) (i j : Fin p) :
    (rationalPathEntryRun Q0 Q es i j).1 = rationalPathInformation Q0 Q es i j := by
  rw [rationalPathEntryRun,rationalSumRun_value]
  have hh : (es.map Q).sum i j = (es.map (fun e => Q e i j)).sum := by
    induction es with
    | nil => rfl
    | cons e es ih => simp only [List.map_cons,List.sum_cons,Matrix.add_apply,ih]
  simp only [List.sum_cons,rationalPathInformation,Matrix.add_apply,hh]

theorem rationalPathInformation_bits {p m B N : ℕ} {Q0 : Matrix (Fin p) (Fin p) ℚ}
    {Q : Fin m → Matrix (Fin p) (Fin p) ℚ} (h0 : MatrixBits Q0 B)
    (hQ : ∀ e, MatrixBits (Q e) B) (es : List (Fin m)) (he : es.length ≤ N) :
    MatrixBits (rationalPathInformation Q0 Q es) (1+(N+1)*(B+1)) := by
  intro i j
  rw [← rationalPathEntryRun_value, rationalPathEntryRun,rationalSumRun_value]
  have hs := rationalBits_list_sum (B := B)
    (xs := Q0 i j :: es.map (fun e => Q e i j)) (by
      intro q hq
      rcases List.mem_cons.mp hq with rfl | hq
      · exact h0 i j
      · obtain ⟨e,_,rfl⟩ := List.mem_map.mp hq
        exact hQ e i j)
  apply rationalBits_mono hs
  simp only [List.length_cons,List.length_map]
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ (Nat.add_le_add_right he 1)) 1

def rationalPathBitWork {p m : ℕ} (Q0 : Matrix (Fin p) (Fin p) ℚ)
    (Q : Fin m → Matrix (Fin p) (Fin p) ℚ) (es : List (Fin m)) (K : ℕ) : ℕ :=
  ∑ i, ∑ j, traceBitWork K (rationalPathEntryRun Q0 Q es i j).2

theorem rationalPathBitWork_le {p m B N : ℕ} {Q0 : Matrix (Fin p) (Fin p) ℚ}
    {Q : Fin m → Matrix (Fin p) (Fin p) ℚ} (h0 : MatrixBits Q0 B)
    (hQ : ∀ e, MatrixBits (Q e) B) (es : List (Fin m)) (he : es.length ≤ N) :
    rationalPathBitWork Q0 Q es (1+(N+1)*(B+1)) ≤
      p*p*(N+1)*(256*(2+(N+1)*(B+1))^3) := by
  have hb (i j : Fin p) : ∀ e ∈ (rationalPathEntryRun Q0 Q es i j).2,
      eventBits (1+(N+1)*(B+1)) e := by
    have hh := rationalSumRun_bits (qs := Q0 i j :: es.map (fun e => Q e i j))
      (B := B) (by
        intro q hq
        rcases List.mem_cons.mp hq with rfl | hq
        · exact h0 i j
        · obtain ⟨e,_,rfl⟩ := List.mem_map.mp hq
          exact hQ e i j)
    intro e he'
    obtain ⟨h1,h2⟩ := hh e he'
    have hh' : 1+(Q0 i j :: es.map (fun e => Q e i j)).length*(B+1) ≤
        1+(N+1)*(B+1) := by
      simp only [List.length_cons,List.length_map]
      gcongr
    exact ⟨rationalBits_mono h1 hh',rationalBits_mono h2 hh'⟩
  have hw (i j : Fin p) : traceBitWork (1+(N+1)*(B+1))
      (rationalPathEntryRun Q0 Q es i j).2 ≤ (N+1)*(256*(2+(N+1)*(B+1))^3) := by
    have h := traceBitWork_le (hb i j)
    simp only [rationalPathEntryRun,rationalSumRun_length,List.length_cons,List.length_map] at h
    have hlen : es.length+1 ≤ N+1 := by omega
    simpa only [rationalPathEntryRun,
      show 1+(N+1)*(B+1)+1 = 2+(N+1)*(B+1) by omega] using
      h.trans (Nat.mul_le_mul_right _ hlen)
  calc
    _ ≤ ∑ _i : Fin p, ∑ _j : Fin p, (N+1)*(256*(2+(N+1)*(B+1))^3) :=
      Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => hw i j
    _ = _ := by simp; ring

end DAGSpectral
