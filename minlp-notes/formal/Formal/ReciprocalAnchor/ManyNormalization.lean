import Formal.ReciprocalAnchor.ManyModel

/-! Affine normalization of arbitrary leaf boxes, positive anchors, and fixed anchors. -/
namespace ReciprocalAnchor.ManyLeaf

/-- The graph with the actual, possibly fixed, leaf intervals. -/
def boxGraph {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ) : Set (Point n) :=
  {z | ∃ x : ℝ, ∃ y : Fin n → ℝ, a ≤ x ∧ x ≤ b ∧
    (∀ j, l j ≤ y j ∧ y j ≤ u j) ∧ z = point x (1 / x) y (fun j => x * y j)}

/-- Restoring a leaf box is affine in all graph and product coordinates. -/
def restore {n : ℕ} (l u : Fin n → ℝ) : Point n →ᵃ[ℝ] Point n where
  toFun z := point z.1 z.2.1 (fun j => l j + (u j - l j) * z.2.2.1 j)
    (fun j => l j * z.1 + (u j - l j) * z.2.2.2 j)
  linear :=
    { toFun := fun z => point z.1 z.2.1 (fun j => (u j - l j) * z.2.2.1 j)
        (fun j => l j * z.1 + (u j - l j) * z.2.2.2 j)
      map_add' := by intros; ext <;> simp [point] <;> ring
      map_smul' := by intros; ext <;> simp [point] <;> ring }
  map_vadd' := by intros; ext <;> simp [point] <;> ring

theorem restore_graph {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) : restore l u '' graph n a b = boxGraph a b l u := by
  ext z
  constructor
  · rintro ⟨_, ⟨x, y, hx, hx', hy, rfl⟩, rfl⟩
    refine ⟨x, fun j => l j + (u j - l j) * y j, hx, hx', ?_, ?_⟩
    · intro j
      constructor
      · nlinarith [mul_nonneg (sub_nonneg.mpr (hlu j)) (hy j).1]
      · nlinarith [mul_le_mul_of_nonneg_left (hy j).2 (sub_nonneg.mpr (hlu j))]
    · ext <;> simp [restore, point]
      ring
  · rintro ⟨x, y, hx, hx', hy, rfl⟩
    let q := fun j => (y j - l j) / (u j - l j)
    have hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1 := by
      intro j
      by_cases h : u j = l j
      · simp [q, h]
      · have hd : 0 < u j - l j := sub_pos.mpr (lt_of_le_of_ne (hlu j) (Ne.symm h))
        exact ⟨div_nonneg (sub_nonneg.mpr (hy j).1) hd.le,
          (div_le_one hd).mpr (sub_le_sub_right (hy j).2 _)⟩
    have he : ∀ j, l j + (u j - l j) * q j = y j := by
      intro j
      by_cases h : u j = l j
      · have : y j = l j := le_antisymm (h ▸ (hy j).2) (hy j).1
        simp [h, this]
      · dsimp [q]
        rw [mul_div_cancel₀ _ (sub_ne_zero.mpr h)]
        ring
    refine ⟨point x (1 / x) q (fun j => x * q j), ⟨x, q, hx, hx', hq, rfl⟩, ?_⟩
    change point x (1 / x) _ _ = point x (1 / x) _ _
    refine Prod.ext rfl (Prod.ext rfl (Prod.ext (funext he) ?_))
    funext j
    change l j * x + (u j - l j) * (x * q j) = x * y j
    rw [← he j]
    ring

/-- Normalization preserves the actual convex hull, including fixed leaves. -/
theorem restore_hull {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) :
    restore l u '' hull n a b = convexHull ℝ (boxGraph a b l u) := by
  rw [hull, AffineMap.image_convexHull, restore_graph a b l u hlu]

/-- The inverse normalization on nonfixed leaves, with the required product correction. -/
noncomputable def normalize {n : ℕ} (l u : Fin n → ℝ) (z : Point n) : Point n :=
  point z.1 z.2.1 (fun j => (z.2.2.1 j - l j) / (u j - l j))
    (fun j => (z.2.2.2 j - l j * z.1) / (u j - l j))

theorem restore_normalize {n : ℕ} (l u : Fin n → ℝ)
    (hlu : ∀ j, l j < u j) (z : Point n) : restore l u (normalize l u z) = z := by
  ext <;> simp [restore, normalize, point]
  all_goals field_simp [ne_of_gt (sub_pos.mpr (hlu _))]
  all_goals ring

theorem normalize_restore {n : ℕ} (l u : Fin n → ℝ)
    (hlu : ∀ j, l j < u j) (z : Point n) : normalize l u (restore l u z) = z := by
  ext <;> simp [restore, normalize, point]
  all_goals field_simp [ne_of_gt (sub_pos.mpr (hlu _))]

theorem mem_box_hull_iff {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j < u j) (z : Point n) :
    z ∈ convexHull ℝ (boxGraph a b l u) ↔ normalize l u z ∈ hull n a b := by
  rw [← restore_hull a b l u (fun j => (hlu j).le)]
  constructor
  · rintro ⟨v, hv, rfl⟩
    rwa [normalize_restore l u hlu]
  · intro h
    exact ⟨normalize l u z, h, restore_normalize l u hlu z⟩

/-- Fixed leaves impose only their two linear coordinate equations. -/
theorem fixed_leaf_equations {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) {z : Point n}
    (hz : z ∈ convexHull ℝ (boxGraph a b l u)) (j : Fin n) (hj : u j = l j) :
    z.2.2.1 j = l j ∧ z.2.2.2 j = l j * z.1 := by
  rw [← restore_hull a b l u hlu] at hz
  rcases hz with ⟨v, hv, rfl⟩
  simp [restore, point, hj]

/-- Removing inactive normalized leaves means setting their two coordinates to zero. -/
noncomputable def eraseFixed {n : ℕ} (l u : Fin n → ℝ) : Point n →ₗ[ℝ] Point n where
  toFun z := point z.1 z.2.1 (fun j => if u j = l j then 0 else z.2.2.1 j)
    (fun j => if u j = l j then 0 else z.2.2.2 j)
  map_add' := by
    intros z v
    ext j <;> simp [point]
    all_goals split_ifs <;> simp
  map_smul' := by
    intros r z
    ext j <;> simp [point]

theorem eraseFixed_graph {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ) :
    eraseFixed l u '' graph n a b ⊆ graph n a b := by
  rintro _ ⟨_, ⟨x, y, hx, hx', hy, rfl⟩, rfl⟩
  refine ⟨x, fun j => if u j = l j then 0 else y j, hx, hx', ?_, ?_⟩
  · intro j
    dsimp only
    split_ifs
    · exact ⟨le_rfl, zero_le_one⟩
    · exact hy j
  · ext j <;> simp [eraseFixed, point]

theorem eraseFixed_mem_hull {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    {z : Point n} (hz : z ∈ hull n a b) : eraseFixed l u z ∈ hull n a b := by
  have hi := Set.mem_image_of_mem (eraseFixed l u) hz
  rw [hull, LinearMap.image_convexHull] at hi
  exact convexHull_mono (eraseFixed_graph a b l u) hi

theorem restore_eraseFixed {n : ℕ} (l u : Fin n → ℝ) (z : Point n) :
    restore l u (eraseFixed l u z) = restore l u z := by
  ext j <;> simp only [restore, point, eraseFixed, LinearMap.coe_mk, AddHom.coe_mk,
    AffineMap.coe_mk, mul_ite, mul_zero, add_right_inj, ite_eq_right_iff, zero_eq_mul]
  all_goals intro h; simp [h]

/-- Every boxed hull point has a normalized witness with fixed leaves deleted;
restoring them changes neither the point nor any active coordinate. -/
theorem mem_box_hull_iff_fixed_deleted {n : ℕ} (a b : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) (z : Point n) :
    z ∈ convexHull ℝ (boxGraph a b l u) ↔
      ∃ v ∈ hull n a b, (∀ j, u j = l j → v.2.2.1 j = 0 ∧ v.2.2.2 j = 0) ∧
        restore l u v = z := by
  rw [← restore_hull a b l u hlu]
  constructor
  · rintro ⟨v, hv, rfl⟩
    refine ⟨eraseFixed l u v, eraseFixed_mem_hull a b l u hv, ?_, restore_eraseFixed l u v⟩
    intro j hj
    simp [eraseFixed, point, hj]
  · rintro ⟨v, hv, _, he⟩
    exact ⟨v, hv, he⟩

/-- A fixed anchor graph is convex for every number of leaves. -/
theorem graph_degenerate_convex (n : ℕ) (a : ℝ) : Convex ℝ (graph n a a) := by
  rintro _ ⟨x, y, hx0, hx1, hy, rfl⟩ _ ⟨x', y', hx0', hx1', hy', rfl⟩ r s hr hs hrs
  have hx : x = a := le_antisymm hx1 hx0
  have hx' : x' = a := le_antisymm hx1' hx0'
  subst x
  subst x'
  refine ⟨a, fun j => r * y j + s * y' j, le_rfl, le_rfl, ?_, ?_⟩
  · intro j
    constructor
    · exact add_nonneg (mul_nonneg hr (hy j).1) (mul_nonneg hs (hy' j).1)
    · nlinarith [mul_le_mul_of_nonneg_left (hy j).2 hr,
        mul_le_mul_of_nonneg_left (hy' j).2 hs]
  · ext <;> simp only [point, one_div, Prod.fst_add, Prod.snd_add, Prod.smul_fst,
      Prod.smul_snd, smul_eq_mul, Pi.add_apply, Pi.smul_apply]
    · rw [← add_mul, hrs, one_mul]
    · rw [← add_mul, hrs, one_mul]
    · ring

theorem hull_degenerate (n : ℕ) (a : ℝ) : hull n a a = graph n a a :=
  (graph_degenerate_convex n a).convexHull_eq

theorem mem_hull_degenerate_iff {n : ℕ} (a m t : ℝ) (q w : Fin n → ℝ) :
    point m t q w ∈ hull n a a ↔
      m = a ∧ t = 1 / a ∧ (∀ j, 0 ≤ q j ∧ q j ≤ 1) ∧ w = fun j => a * q j := by
  rw [hull_degenerate]
  constructor
  · rintro ⟨x, y, hx0, hx1, hy, he⟩
    have hx : x = a := le_antisymm hx1 hx0
    subst x
    have hm := congrArg Prod.fst he
    have ht := congrArg (fun z : Point n => z.2.1) he
    have hq := congrArg (fun z : Point n => z.2.2.1) he
    have hw := congrArg (fun z : Point n => z.2.2.2) he
    simp only [point] at hm ht hq hw
    exact ⟨hm, ht, hq.symm ▸ hy, hw.trans (congrArg (fun y j => a * y j) hq.symm)⟩
  · rintro ⟨rfl, rfl, hq, rfl⟩
    exact ⟨_, q, le_rfl, le_rfl, hq, rfl⟩

/-- The fixed-anchor hull stays linear in the original leaf boxes. -/
theorem box_hull_degenerate {n : ℕ} (a : ℝ) (l u : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) :
    convexHull ℝ (boxGraph a a l u) = boxGraph a a l u := by
  rw [← restore_hull a a l u hlu, hull_degenerate, restore_graph a a l u hlu]

theorem mem_box_hull_degenerate_iff {n : ℕ} (a m t : ℝ) (l u q w : Fin n → ℝ)
    (hlu : ∀ j, l j ≤ u j) :
    point m t q w ∈ convexHull ℝ (boxGraph a a l u) ↔
      m = a ∧ t = 1 / a ∧ (∀ j, l j ≤ q j ∧ q j ≤ u j) ∧ w = fun j => a * q j := by
  rw [box_hull_degenerate a l u hlu]
  constructor
  · rintro ⟨x, y, hx0, hx1, hy, he⟩
    have hx : x = a := le_antisymm hx1 hx0
    subst x
    have hm := congrArg Prod.fst he
    have ht := congrArg (fun z : Point n => z.2.1) he
    have hq := congrArg (fun z : Point n => z.2.2.1) he
    have hw := congrArg (fun z : Point n => z.2.2.2) he
    simp only [point] at hm ht hq hw
    exact ⟨hm, ht, hq.symm ▸ hy, hw.trans (congrArg (fun y j => a * y j) hq.symm)⟩
  · rintro ⟨rfl, rfl, hq, rfl⟩
    exact ⟨_, q, le_rfl, le_rfl, hq, rfl⟩

/-- Original positive-anchor graph: the second coordinate satisfies `x * y₀ = p`. -/
def anchoredGraph (n : ℕ) (a b p : ℝ) : Set (Point n) :=
  {z | ∃ x y₀ : ℝ, ∃ y : Fin n → ℝ, a ≤ x ∧ x ≤ b ∧ x * y₀ = p ∧
    (∀ j, 0 ≤ y j ∧ y j ≤ 1) ∧ z = point x y₀ y (fun j => x * y j)}

def scaleAnchor {n : ℕ} (p : ℝ) : Point n →ₗ[ℝ] Point n where
  toFun z := point z.1 (p * z.2.1) z.2.2.1 z.2.2.2
  map_add' := by intros; ext <;> simp [point]; ring
  map_smul' := by intros; ext <;> simp [point]; ring

theorem scaleAnchor_graph (n : ℕ) {a b : ℝ} (ha : 0 < a) (p : ℝ) :
    scaleAnchor p '' graph n a b = anchoredGraph n a b p := by
  ext z
  constructor
  · rintro ⟨_, ⟨x, y, hx, hx', hy, rfl⟩, rfl⟩
    refine ⟨x, p * (1 / x), y, hx, hx', ?_, hy, rfl⟩
    field_simp [ne_of_gt (lt_of_lt_of_le ha hx)]
  · rintro ⟨x, y₀, y, hx, hx', hprod, hy, rfl⟩
    refine ⟨point x (1 / x) y (fun j => x * y j), ⟨x, y, hx, hx', hy, rfl⟩, ?_⟩
    have he : p * (1 / x) = y₀ := by
      rw [← hprod]
      field_simp [ne_of_gt (lt_of_lt_of_le ha hx)]
    simpa [scaleAnchor, point] using he

theorem scaleAnchor_hull (n : ℕ) {a b : ℝ} (ha : 0 < a) (p : ℝ) :
    scaleAnchor p '' hull n a b = convexHull ℝ (anchoredGraph n a b p) := by
  rw [hull, LinearMap.image_convexHull, scaleAnchor_graph n ha p]

theorem mem_anchored_hull_iff {n : ℕ} {a b p : ℝ} (ha : 0 < a) (hp : 0 < p)
    (m y₀ : ℝ) (q w : Fin n → ℝ) :
    point m y₀ q w ∈ convexHull ℝ (anchoredGraph n a b p) ↔
      point m (y₀ / p) q w ∈ hull n a b := by
  rw [← scaleAnchor_hull n ha p]
  constructor
  · rintro ⟨v, hv, he⟩
    have hm := congrArg Prod.fst he
    have ht := congrArg (fun z : Point n => z.2.1) he
    have hq := congrArg (fun z : Point n => z.2.2.1) he
    have hw := congrArg (fun z : Point n => z.2.2.2) he
    simp only [scaleAnchor, LinearMap.coe_mk, AddHom.coe_mk, point] at hm ht hq hw
    have hv' : point m (y₀ / p) q w = v := by
      ext <;> simp [point, ← hm, ← ht, ← hq, ← hw, ne_of_gt hp]
    rwa [hv']
  · intro hz
    refine ⟨point m (y₀ / p) q w, hz, ?_⟩
    simp only [scaleAnchor, LinearMap.coe_mk, AddHom.coe_mk, point, Prod.mk.injEq]
    field_simp [ne_of_gt hp]
    simp

end ReciprocalAnchor.ManyLeaf
