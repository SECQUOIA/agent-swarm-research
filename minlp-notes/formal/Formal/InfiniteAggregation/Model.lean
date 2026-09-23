import Mathlib

/-!
# The three-inequality infinite-aggregation example

The variables are two vectors in `ℝ^r`. Squared Euclidean lengths are
explicit dot products, independent of the norm instance on function spaces.
-/

open scoped BigOperators Matrix
open Set

noncomputable section

namespace InfiniteAggregation

abbrev Vec (r : ℕ) := Fin r → ℝ
abbrev Var (r : ℕ) := Vec r × Vec r
abbrev HomVar (r : ℕ) := Var r × ℝ
abbrev Weight := Fin 3 → ℝ

def dot {r : ℕ} (u v : Vec r) : ℝ := u ⬝ᵥ v
def qnorm {r : ℕ} (u : Vec r) : ℝ := dot u u

def eval {r : ℕ} (x : Var r) : Weight :=
  ![qnorm x.1 - 1, qnorm x.2 - 1, 1 / 2 - dot x.1 x.2]

def homEval {r : ℕ} (z : HomVar r) : Weight :=
  ![qnorm z.1.1 - z.2 ^ 2, qnorm z.1.2 - z.2 ^ 2,
    z.2 ^ 2 / 2 - dot z.1.1 z.1.2]

def feasible (r : ℕ) : Set (Var r) := {x | ∀ i, eval x i < 0}
def NonnegWeight (w : Weight) : Prop := (∀ i, 0 ≤ w i) ∧ w ≠ 0

def GoodCone (w : Weight) : Prop :=
  (∀ i, 0 ≤ w i) ∧ (w 2) ^ 2 ≤ 4 * w 0 * w 1

def aggregate {r : ℕ} (w : Weight) (x : Var r) : ℝ := ∑ i, w i * eval x i
def homAggregate {r : ℕ} (w : Weight) (z : HomVar r) : ℝ :=
  ∑ i, w i * homEval z i

def HHC (r : ℕ) : Prop :=
  ∀ l : HomVar r →ₗ[ℝ] ℝ, l ≠ 0 →
    Convex ℝ (homEval '' (LinearMap.ker l : Set (HomVar r)))

variable {r : ℕ}

theorem dot_comm (u v : Vec r) : dot u v = dot v u := dotProduct_comm _ _
@[simp] theorem dot_zero_left (u : Vec r) : dot 0 u = 0 := by simp [dot]
@[simp] theorem dot_zero_right (u : Vec r) : dot u 0 = 0 := by simp [dot]
@[simp] theorem qnorm_zero : qnorm (0 : Vec r) = 0 := by simp [qnorm]

theorem qnorm_nonneg (u : Vec r) : 0 ≤ qnorm u := by
  unfold qnorm dot dotProduct
  exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (u i)) (s := Finset.univ)

theorem dot_add_left (u v z : Vec r) : dot (u + v) z = dot u z + dot v z :=
  add_dotProduct _ _ _
theorem dot_add_right (u v z : Vec r) : dot u (v + z) = dot u v + dot u z :=
  dotProduct_add _ _ _
theorem dot_smul_left (a : ℝ) (u v : Vec r) : dot (a • u) v = a * dot u v := by
  simp [dot, smul_dotProduct]
theorem dot_smul_right (a : ℝ) (u v : Vec r) : dot u (a • v) = a * dot u v := by
  simp [dot, dotProduct_smul]
theorem qnorm_smul (a : ℝ) (u : Vec r) : qnorm (a • u) = a ^ 2 * qnorm u := by
  simp only [qnorm, dot_smul_left, dot_smul_right]
  ring
theorem qnorm_add (u v : Vec r) : qnorm (u + v) = qnorm u + 2 * dot u v + qnorm v := by
  simp only [qnorm, dot_add_left, dot_add_right]
  rw [dot_comm v u]
  ring

@[simp] theorem homEval_one (x : Var r) : homEval (x, 1) = eval x := by
  simp [homEval, eval]

theorem aggregate_formula (w : Weight) (x : Var r) :
    aggregate w x = w 0 * qnorm x.1 + w 1 * qnorm x.2 -
      w 2 * dot x.1 x.2 + (w 2 / 2 - w 0 - w 1) := by
  simp [aggregate, eval, Fin.sum_univ_succ]
  ring

theorem homAggregate_formula (w : Weight) (z : HomVar r) :
    homAggregate w z = w 0 * qnorm z.1.1 + w 1 * qnorm z.1.2 -
      w 2 * dot z.1.1 z.1.2 + (w 2 / 2 - w 0 - w 1) * z.2 ^ 2 := by
  simp [homAggregate, homEval, Fin.sum_univ_succ]
  ring

theorem mem_feasible_iff (x : Var r) : x ∈ feasible r ↔
    qnorm x.1 < 1 ∧ qnorm x.2 < 1 ∧ 1 / 2 < dot x.1 x.2 := by
  simp [feasible, eval, Fin.forall_fin_succ]

theorem aggregate_neg {w : Weight} (hw : NonnegWeight w) {x : Var r}
    (hx : x ∈ feasible r) : aggregate w x < 0 := by
  obtain ⟨hn, hne⟩ := hw
  have hp : ∃ i, 0 < w i := by
    by_contra! h
    apply hne
    ext i
    exact le_antisymm (h i) (hn i)
  obtain ⟨i, hi⟩ := hp
  exact Finset.sum_neg' (fun j _ => mul_nonpos_of_nonneg_of_nonpos (hn j) (hx j).le)
    ⟨i, Finset.mem_univ _, mul_neg_of_pos_of_neg hi (hx i)⟩

theorem continuous_eval : Continuous (eval : Var r → Weight) := by
  unfold eval qnorm dot dotProduct
  fun_prop

theorem continuous_aggregate (w : Weight) : Continuous (aggregate w : Var r → ℝ) := by
  unfold aggregate
  exact continuous_finsetSum _ fun i _ => continuous_const.mul
    ((continuous_apply i).comp continuous_eval)

/-- Realize a positive first diagonal and a nonnegative two by two Gram determinant. -/
theorem gram_realization (hr : 2 ≤ r) {p q c : ℝ} (hp : 0 < p)
    (hdet : c ^ 2 ≤ p * q) :
    ∃ u v : Vec r, qnorm u = p ∧ qnorm v = q ∧ dot u v = c := by
  let i : Fin r := ⟨0, by omega⟩
  let j : Fin r := ⟨1, by omega⟩
  have hij : i ≠ j := by simp [i, j]
  let e : Vec r := Pi.single i 1
  let f : Vec r := Pi.single j 1
  have he : qnorm e = 1 := by simp [qnorm, dot, e, dotProduct_single]
  have hf : qnorm f = 1 := by simp [qnorm, dot, f, dotProduct_single]
  have hef : dot e f = 0 := by simp [dot, e, f, dotProduct_single, hij]
  have hs : Real.sqrt p ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hp)
  have hs2 : Real.sqrt p ^ 2 = p := Real.sq_sqrt hp.le
  have ht : 0 ≤ q - c ^ 2 / p := by
    have hdiv : c ^ 2 / p ≤ q := (div_le_iff₀ hp).2 (by nlinarith [hdet])
    linarith
  refine ⟨Real.sqrt p • e,
    (c / Real.sqrt p) • e + Real.sqrt (q - c ^ 2 / p) • f, ?_, ?_, ?_⟩
  · rw [qnorm_smul, he, mul_one, hs2]
  · rw [qnorm_add, qnorm_smul, qnorm_smul, he, hf,
      dot_smul_left, dot_smul_right, hef]
    rw [Real.sq_sqrt ht]
    have hd : (c / Real.sqrt p) ^ 2 = c ^ 2 / p := by
      rw [div_pow, hs2]
    rw [hd]
    ring
  · rw [dot_add_right, dot_smul_left, dot_smul_right, dot_smul_left,
      dot_smul_right, hef]
    change Real.sqrt p * (c / Real.sqrt p * qnorm e) +
      Real.sqrt p * (Real.sqrt (q - c ^ 2 / p) * 0) = c
    rw [he]
    field_simp
    ring

theorem feasible_nonempty (hr : 1 ≤ r) : (feasible r).Nonempty := by
  let i : Fin r := ⟨0, by omega⟩
  let u : Vec r := Pi.single i (3 / 4)
  have hu : qnorm u = 9 / 16 := by norm_num [qnorm, dot, u, dotProduct_single]
  refine ⟨(u, u), (mem_feasible_iff _).2 ?_⟩
  change qnorm u < 1 ∧ qnorm u < 1 ∧ 1 / 2 < qnorm u
  rw [hu]
  norm_num

theorem coordinate_sq_le_qnorm (u : Vec r) (i : Fin r) : (u i) ^ 2 ≤ qnorm u := by
  unfold qnorm dot dotProduct
  simpa only [sq] using Finset.single_le_sum
    (fun j (_ : j ∈ Finset.univ) => mul_self_nonneg (u j)) (Finset.mem_univ i)

theorem norm_le_one_of_qnorm_le_one {u : Vec r} (hu : qnorm u ≤ 1) : ‖u‖ ≤ 1 := by
  apply (pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1)).2
  intro i
  rw [Real.norm_eq_abs, abs_le]
  have h := coordinate_sq_le_qnorm u i
  constructor <;> nlinarith

theorem feasible_bounded : Bornology.IsBounded (feasible r) := by
  apply isBounded_iff_forall_norm_le.2
  refine ⟨1, fun x hx => ?_⟩
  have h := (mem_feasible_iff x).1 hx
  rw [Prod.norm_def, max_le_iff]
  exact ⟨norm_le_one_of_qnorm_le_one h.1.le, norm_le_one_of_qnorm_le_one h.2.1.le⟩

theorem convexHull_bounded : Bornology.IsBounded (convexHull ℝ (feasible r)) :=
  isBounded_convexHull.2 feasible_bounded

/-- The ordinary hull is proper as well as nonempty in every allowed dimension. -/
theorem convexHull_proper (hr : 1 ≤ r) : convexHull ℝ (feasible r) ≠ Set.univ := by
  let : NeZero r := ⟨by omega⟩
  intro h
  have hb : Bornology.IsBounded (Set.univ : Set (Var r)) := h ▸ convexHull_bounded
  exact NormedSpace.unbounded_univ ℝ (Var r) hb

theorem convexHull_nonempty (hr : 1 ≤ r) : (convexHull ℝ (feasible r)).Nonempty :=
  (feasible_nonempty hr).mono (subset_convexHull ℝ _)

end InfiniteAggregation
