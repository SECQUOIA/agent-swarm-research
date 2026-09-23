import Formal.ReciprocalAnchor.Representation

/-! Actual graph hull and finite common-factor laws for arbitrarily many leaves. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

abbrev Point (n : ℕ) := ℝ × ℝ × (Fin n → ℝ) × (Fin n → ℝ)

def point {n : ℕ} (m t : ℝ) (q w : Fin n → ℝ) : Point n := (m, t, q, w)

def graph (n : ℕ) (a b : ℝ) : Set (Point n) :=
  {z | ∃ x : ℝ, ∃ y : Fin n → ℝ, a ≤ x ∧ x ≤ b ∧
    (∀ j, 0 ≤ y j ∧ y j ≤ 1) ∧ z = point x (1 / x) y (fun j => x * y j)}

def hull (n : ℕ) (a b : ℝ) : Set (Point n) := convexHull ℝ (graph n a b)

/-- Finitely many atoms, including zero masses, represent a probability law. -/
structure Law (a b : ℝ) where
  size : ℕ
  mass : Fin size → ℝ
  location : Fin size → ℝ
  nonneg : ∀ i, 0 ≤ mass i
  total : ∑ i, mass i = 1
  bounds : ∀ i, a ≤ location i ∧ location i ≤ b

def Law.mean {a b : ℝ} (μ : Law a b) : ℝ := ∑ i, μ.mass i * μ.location i

noncomputable def Law.reciprocal {a b : ℝ} (μ : Law a b) : ℝ := ∑ i, μ.mass i / μ.location i

def Law.call {a b : ℝ} (μ : Law a b) (s : ℝ) : ℝ :=
  ∑ i, μ.mass i * max (μ.location i - s) 0

def LinearBounds {n : ℕ} (a b m : ℝ) (q w : Fin n → ℝ) : Prop :=
  a ≤ m ∧ m ≤ b ∧ ∀ j, 0 ≤ q j ∧ q j ≤ 1 ∧
    a * q j ≤ w j ∧ w j ≤ b * q j ∧
    a * (1 - q j) ≤ m - w j ∧ m - w j ≤ b * (1 - q j)

/-- The baseline lines are always present, even with no leaves. -/
def line {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (i : Fin (2 * n + 2)) (s : ℝ) : ℝ :=
  if h : i.val < n then w ⟨i.val, h⟩ - q ⟨i.val, h⟩ * s
  else if h' : i.val < 2 * n then
    m - w ⟨i.val - n, by omega⟩ - (1 - q ⟨i.val - n, by omega⟩) * s
  else if i.val = 2 * n then 0 else m - s

noncomputable def envelope {n : ℕ} (m : ℝ) (q w : Fin n → ℝ) (s : ℝ) : ℝ :=
  (Finset.univ.image (fun i => line m q w i s)).max'
    (Finset.image_nonempty.mpr Finset.univ_nonempty)

noncomputable def lowerMoment {n : ℕ} (a b m : ℝ) (q w : Fin n → ℝ) : ℝ :=
  1 / a - (m - a) / a ^ 2 + ∫ s in a..b, 2 * envelope m q w s / s ^ 3

theorem finite_representation_mem_hull {ι : Type*} [Fintype ι] {n : ℕ}
    {a b m t : ℝ} {q w : Fin n → ℝ} (p x : ι → ℝ) (y : ι → Fin n → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hy : ∀ i j, 0 ≤ y i j ∧ y i j ≤ 1)
    (hm : ∑ i, p i * x i = m) (ht : ∑ i, p i / x i = t)
    (hq : ∀ j, ∑ i, p i * y i j = q j)
    (hw : ∀ j, ∑ i, p i * (x i * y i j) = w j) :
    point m t q w ∈ hull n a b := by
  apply mem_convexHull_of_exists_fintype p
    (fun i => point (x i) (1 / x i) (y i) (fun j => x i * y i j)) hp hp1
  · intro i
    exact ⟨x i, y i, (hx i).1, (hx i).2, hy i, rfl⟩
  · apply Prod.ext
    · simpa [point, Prod.fst_sum, smul_eq_mul] using hm
    · apply Prod.ext
      · simpa [point, Prod.snd_sum, Prod.fst_sum, smul_eq_mul, div_eq_mul_inv] using ht
      · apply Prod.ext <;> funext j
        · simpa [point, Prod.snd_sum, Prod.fst_sum, Finset.sum_apply, smul_eq_mul] using hq j
        · simpa [point, Prod.snd_sum, Finset.sum_apply, smul_eq_mul] using hw j

theorem mem_hull_has_finite_representation {n : ℕ} {a b m t : ℝ} {q w : Fin n → ℝ}
    (h : point m t q w ∈ hull n a b) :
    ∃ (ι : Type) (_ : Fintype ι) (p x : ι → ℝ) (y : ι → Fin n → ℝ),
      (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1) ∧
      (∀ i, a ≤ x i ∧ x i ≤ b) ∧ (∀ i j, 0 ≤ y i j ∧ y i j ≤ 1) ∧
      (∑ i, p i * x i = m) ∧ (∑ i, p i / x i = t) ∧
      (∀ j, ∑ i, p i * y i j = q j) ∧
      (∀ j, ∑ i, p i * (x i * y i j) = w j) := by
  classical
  obtain ⟨ι, hι, p, z, hp, hp1, hz, hsum⟩ := mem_convexHull_iff_exists_fintype.mp h
  have hi : ∀ i, ∃ x : ℝ, ∃ y : Fin n → ℝ, a ≤ x ∧ x ≤ b ∧
      (∀ j, 0 ≤ y j ∧ y j ≤ 1) ∧ z i = point x (1 / x) y (fun j => x * y j) := hz
  choose x y hx hx' hy heq using hi
  refine ⟨ι, hι, p, x, y, hp, hp1, fun i => ⟨hx i, hx' i⟩, hy, ?_, ?_, ?_, ?_⟩
  · have he := congrArg Prod.fst hsum
    simpa [heq, point, Prod.fst_sum, smul_eq_mul] using he
  · have he := congrArg (fun z : Point n => z.2.1) hsum
    simpa [heq, point, Prod.fst_sum, Prod.snd_sum, smul_eq_mul, div_eq_mul_inv] using he
  · intro j
    have he := congrArg (fun z : Point n => z.2.2.1 j) hsum
    simpa [heq, point, Prod.fst_sum, Prod.snd_sum, Finset.sum_apply, smul_eq_mul] using he
  · intro j
    have he := congrArg (fun z : Point n => z.2.2.2 j) hsum
    simpa [heq, point, Prod.snd_sum, Finset.sum_apply, smul_eq_mul] using he

/-- A generic finite probability law can be indexed by a finite initial segment. -/
noncomputable def Law.ofFinite {ι : Type*} [Fintype ι] {a b : ℝ} (p x : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) : Law a b where
  size := Fintype.card ι
  mass := fun i => p ((Fintype.equivFin ι).symm i)
  location := fun i => x ((Fintype.equivFin ι).symm i)
  nonneg := fun _i => hp _
  total := (Equiv.sum_comp (Fintype.equivFin ι).symm p).trans hp1
  bounds := fun _i => hx _

theorem Law.ofFinite_mean {ι : Type*} [Fintype ι] {a b : ℝ} (p x : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) :
    (Law.ofFinite p x hp hp1 hx).mean = ∑ i, p i * x i :=
  Equiv.sum_comp (Fintype.equivFin ι).symm (fun i => p i * x i)

theorem Law.ofFinite_reciprocal {ι : Type*} [Fintype ι] {a b : ℝ} (p x : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) :
    (Law.ofFinite p x hp hp1 hx).reciprocal = ∑ i, p i / x i :=
  Equiv.sum_comp (Fintype.equivFin ι).symm (fun i => p i / x i)

theorem Law.ofFinite_call {ι : Type*} [Fintype ι] {a b : ℝ} (p x : ι → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (s : ℝ) :
    (Law.ofFinite p x hp hp1 hx).call s = ∑ i, p i * max (x i - s) 0 :=
  Equiv.sum_comp (Fintype.equivFin ι).symm (fun i => p i * max (x i - s) 0)

theorem leaf_bounds_imply_mean_bounds {n : ℕ} {a b m : ℝ} {q w : Fin n → ℝ}
    (j : Fin n) (h₁ : a * q j ≤ w j) (h₂ : w j ≤ b * q j)
    (h₃ : a * (1 - q j) ≤ m - w j) (h₄ : m - w j ≤ b * (1 - q j)) :
    a ≤ m ∧ m ≤ b := by constructor <;> nlinarith

end ReciprocalAnchor.ManyLeaf
