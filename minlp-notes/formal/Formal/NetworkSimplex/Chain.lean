import Formal.NetworkSimplex.Disaggregation

namespace NetworkSimplex

noncomputable section

abbrev ChainArc (L : ℕ) := (Fin L × Bool) ⊕ Unit

namespace Chain

def a {L : ℕ} (i : Fin L) : ChainArc L := Sum.inl (i, false)
def b {L : ℕ} (i : Fin L) : ChainArc L := Sum.inl (i, true)
def bypass {L : ℕ} : ChainArc L := Sum.inr ()

def incoming (L : ℕ) : (Fin L → ℝ) →ₗ[ℝ] (Fin (L + 1) → ℝ) where
  toFun f := Fin.cases 0 f
  map_add' f g := by
    funext v
    refine Fin.cases ?_ (fun i => ?_) v <;> simp
  map_smul' c f := by
    funext v
    refine Fin.cases ?_ (fun i => ?_) v <;> simp

def outgoing (L : ℕ) : (Fin L → ℝ) →ₗ[ℝ] (Fin (L + 1) → ℝ) where
  toFun f := Fin.lastCases 0 f
  map_add' f g := by
    funext v
    refine Fin.lastCases ?_ (fun i => ?_) v <;> simp
  map_smul' c f := by
    funext v
    refine Fin.lastCases ?_ (fun i => ?_) v <;> simp

def boundary (L : ℕ) := incoming L - outgoing L

def cuts (L : ℕ) : (ChainArc L → ℝ) →ₗ[ℝ] (Fin L → ℝ) where
  toFun f i := f (a i) + f (b i) + f bypass
  map_add' f g := by ext i; simp; ring
  map_smul' c f := by ext i; simp; ring

/-- Incoming minus outgoing flow on the chain of parallel pairs with its bypass.
Each chain cut contains the two arcs of that gadget and the bypass. -/
def incidence (L : ℕ) := (boundary L).comp (cuts L)

def demand (L : ℕ) : Fin (L + 1) → ℝ := boundary L (fun _ => 1)

def tail {L : ℕ} : ChainArc L → Fin (L + 1)
  | Sum.inl (i, _) => i.castSucc
  | Sum.inr _ => 0

def head {L : ℕ} : ChainArc L → Fin (L + 1)
  | Sum.inl (i, _) => i.succ
  | Sum.inr _ => Fin.last L

theorem incoming_sum (L : ℕ) (f : Fin L → ℝ) (v : Fin (L + 1)) :
    incoming L f v = ∑ i, if i.succ = v then f i else 0 := by
  refine Fin.cases ?_ (fun i => ?_) v <;> simp [incoming]

theorem outgoing_sum (L : ℕ) (f : Fin L → ℝ) (v : Fin (L + 1)) :
    outgoing L f v = ∑ i, if i.castSucc = v then f i else 0 := by
  refine Fin.lastCases ?_ (fun i => ?_) v <;> simp [outgoing]

theorem incoming_const (L : ℕ) (f : Fin L → ℝ) (h : ℝ) (v : Fin (L + 1)) :
    incoming L (fun i => f i + h) v = incoming L f v + if v = 0 then 0 else h := by
  refine Fin.cases ?_ (fun i => ?_) v <;> simp [incoming]

theorem outgoing_const (L : ℕ) (f : Fin L → ℝ) (h : ℝ) (v : Fin (L + 1)) :
    outgoing L (fun i => f i + h) v =
      outgoing L f v + if v = Fin.last L then 0 else h := by
  refine Fin.lastCases ?_ (fun i => ?_) v <;> simp [outgoing]

theorem demand_eq (L : ℕ) (v : Fin (L + 1)) :
    demand L v = (if v = Fin.last L then 1 else 0) - (if v = 0 then 1 else 0) := by
  change incoming L (fun _ => 1) v - outgoing L (fun _ => 1) v = _
  rw [show (fun _ : Fin L => (1 : ℝ)) = (fun _ => 0 + 1) by ext; simp]
  rw [incoming_const, outgoing_const]
  change (incoming L 0 v + if v = 0 then 0 else 1) -
    (outgoing L 0 v + if v = Fin.last L then 0 else 1) = _
  simp only [map_zero, Pi.zero_apply, zero_add]
  split_ifs <;> norm_num

/-- The cut-difference definition equals the standard incoming-minus-outgoing
incidence sum for the stated tail and head of every arc. -/
theorem incidence_eq_sum (L : ℕ) (f : ChainArc L → ℝ) (v : Fin (L + 1)) :
    incidence L f v =
      (∑ e, if head e = v then f e else 0) -
      (∑ e, if tail e = v then f e else 0) := by
  change incoming L (fun i => f (a i) + f (b i) + f bypass) v -
    outgoing L (fun i => f (a i) + f (b i) + f bypass) v = _
  rw [incoming_const, outgoing_const, incoming_sum, outgoing_sum]
  simp only [Fintype.sum_sum_type, Fintype.sum_prod_type, Fintype.sum_bool,
    Fintype.sum_unique, head, tail, a, b, bypass]
  have hadd (p : Prop) [Decidable p] (x y : ℝ) :
      (if p then x + y else 0) = (if p then x else 0) + (if p then y else 0) := by
    split <;> simp
  simp only [hadd, Finset.sum_add_distrib,
    eq_comm (a := Fin.last L) (b := v), eq_comm (a := (0 : Fin (L + 1))) (b := v)]
  split_ifs <;> ring!

theorem boundary_injective (L : ℕ) : Function.Injective (boundary L) := by
  intro f g h
  cases L with
  | zero => exact Subsingleton.elim _ _
  | succ L =>
    funext i
    refine Fin.induction ?_ (fun j ih => ?_) i
    · have hz := congrFun h (0 : Fin (L + 1 + 1))
      have he : (0 : Fin (L + 1 + 1)) = (0 : Fin (L + 1)).castSucc := rfl
      simp only [boundary, LinearMap.sub_apply, Pi.sub_apply, incoming, outgoing,
        LinearMap.coe_mk, AddHom.coe_mk] at hz
      rw [Fin.cases_zero, Fin.cases_zero, he, Fin.lastCases_castSucc,
        Fin.lastCases_castSucc] at hz
      linarith
    · have hz := congrFun h j.succ.castSucc
      have he : j.succ.castSucc = j.castSucc.succ := rfl
      simp only [boundary, LinearMap.sub_apply, Pi.sub_apply, incoming, outgoing,
        LinearMap.coe_mk, AddHom.coe_mk] at hz
      rw [Fin.lastCases_castSucc, Fin.lastCases_castSucc, he,
        Fin.cases_succ, Fin.cases_succ] at hz
      linarith

theorem conservation_iff (L : ℕ) (f : ChainArc L → ℝ) (w : ℝ) :
    incidence L f = w • demand L ↔ ∀ i, f (a i) + f (b i) + f bypass = w := by
  change boundary L (cuts L f) = w • boundary L (fun _ => 1) ↔ _
  rw [← map_smul]
  constructor
  · intro h i
    have hi := congrFun (boundary_injective L h) i
    simpa [cuts] using hi
  · intro h
    congr 1
    funext i
    simpa [cuts] using h i

theorem flow_iff (L : ℕ) (f : ChainArc L → ℝ) (w : ℝ) :
    Flow (incidence L) (demand L) (fun _ => 1) w f ↔
      (∀ e, 0 ≤ f e ∧ f e ≤ w) ∧
      (∀ i, f (a i) + f (b i) + f bypass = w) := by
  simp only [Flow, conservation_iff, mul_one]
  exact and_comm

end Chain
end
end NetworkSimplex
