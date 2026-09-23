import Mathlib
import Formal.CubicGap.Expectation

/-!
# Half integrality of degree slabs

The incidence sets may contain parallel graph edges: edges have their own
index type, and the only incidence restriction is that each edge belongs to
at most two rows. Bounds are arbitrary integers, including coincident bounds.
-/

namespace MultilinearGap.FrequencySlab

open scoped BigOperators
open Set Matrix

noncomputable section

variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq E]

/-- The sum of edge coordinates incident to a row. -/
def degree (S : V → Finset E) (x : E → ℝ) (v : V) : ℝ := ∑ e ∈ S v, x e

/-- The cube intersected with integer degree bounds. -/
def slab (S : V → Finset E) (lo hi : V → ℤ) : Set (E → ℝ) :=
  {x | (∀ e, 0 ≤ x e ∧ x e ≤ 1) ∧
    ∀ v, (lo v : ℝ) ≤ degree S x v ∧ degree S x v ≤ (hi v : ℝ)}

/-- Fractional edge coordinates. -/
def fractional (x : E → ℝ) : Finset E :=
  Finset.univ.filter fun e => 0 < x e ∧ x e < 1

/-- Active rows that contain at least one fractional edge. A coincident pair
of lower and upper bounds still contributes just one row. -/
def active (S : V → Finset E) (lo hi : V → ℤ) (x : E → ℝ) : Finset V :=
  Finset.univ.filter fun v =>
    (degree S x v = (lo v : ℝ) ∨ degree S x v = (hi v : ℝ)) ∧
      (S v ∩ fractional x).Nonempty

omit [Fintype V] [Fintype E] [DecidableEq E] in
theorem degree_add_smul (S : V → Finset E) (x d : E → ℝ) (t : ℝ) (v : V) :
    degree S (x + t • d) v = degree S x v + t * degree S d v := by
  simp [degree, Finset.sum_add_distrib, Finset.mul_sum]

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- A direction vanishing on integral coordinates and on tight degree rows
admits a symmetric feasible perturbation. -/
theorem exists_symmetric_perturbation [Finite V] [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    {x d : E → ℝ} (hx : x ∈ slab S lo hi)
    (hd : ∀ e, x e = 0 ∨ x e = 1 → d e = 0)
    (hrow : ∀ v, degree S x v = (lo v : ℝ) ∨ degree S x v = (hi v : ℝ) →
      degree S d v = 0) :
    ∃ t : ℝ, 0 < t ∧ x + t • d ∈ slab S lo hi ∧ x - t • d ∈ slab S lo hi := by
  let := Fintype.ofFinite V
  let := Fintype.ofFinite E
  have hbox : ∀ᶠ t : ℝ in nhds 0, ∀ e, 0 ≤ x e + t * d e ∧ x e + t * d e ≤ 1 := by
    rw [Filter.eventually_all]
    intro e
    by_cases he : x e = 0 ∨ x e = 1
    · exact Filter.Eventually.of_forall (fun _ : ℝ => by simpa [hd e he] using hx.1 e)
    · have h0 : 0 < x e := lt_of_le_of_ne (hx.1 e).1 (by aesop)
      have h1 : x e < 1 := lt_of_le_of_ne (hx.1 e).2 (by aesop)
      have hc : ContinuousAt (fun t : ℝ => x e + t * d e) 0 := by fun_prop
      filter_upwards [hc.eventually_const_lt (by simpa using h0),
        hc.eventually_lt_const (by simpa using h1)] with t ht0 ht1
      exact ⟨ht0.le, ht1.le⟩
  have hrows : ∀ᶠ t : ℝ in nhds 0, ∀ v,
      (lo v : ℝ) ≤ degree S x v + t * degree S d v ∧
      degree S x v + t * degree S d v ≤ (hi v : ℝ) := by
    rw [Filter.eventually_all]
    intro v
    by_cases hv : degree S x v = (lo v : ℝ) ∨ degree S x v = (hi v : ℝ)
    · exact Filter.Eventually.of_forall (fun _ : ℝ => by simpa [hrow v hv] using hx.2 v)
    · have h0 : (lo v : ℝ) < degree S x v :=
        lt_of_le_of_ne (hx.2 v).1 (by aesop)
      have h1 : degree S x v < (hi v : ℝ) :=
        lt_of_le_of_ne (hx.2 v).2 (by aesop)
      have hc : ContinuousAt (fun t : ℝ => degree S x v + t * degree S d v) 0 := by
        fun_prop
      filter_upwards [hc.eventually_const_lt (by simpa using h0),
        hc.eventually_lt_const (by simpa using h1)] with t ht0 ht1
      exact ⟨ht0.le, ht1.le⟩
  have he : ∀ᶠ t : ℝ in nhds 0, x + t • d ∈ slab S lo hi := by
    filter_upwards [hbox, hrows] with t htbox htrows
    exact ⟨htbox, fun v => by simpa [degree_add_smul] using htrows v⟩
  obtain ⟨δ, hδ, hh⟩ := Metric.eventually_nhds_iff.mp he
  refine ⟨δ / 2, by positivity, hh ?_, ?_⟩
  · simpa [Real.dist_eq, abs_of_pos hδ] using (show δ / 2 < δ by linarith)
  · have h := hh (y := -(δ / 2)) (by
      simpa [Real.dist_eq, abs_neg, abs_of_pos hδ] using (show δ / 2 < δ by linarith))
    simpa [sub_eq_add_neg, neg_smul] using h

/-- At an extreme point, the active degree rows are injective on the
fractional coordinates. -/
theorem extreme_kernel_eq_zero {S : V → Finset E} {lo hi : V → ℤ}
    {x d : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    (hd : ∀ e, e ∉ fractional x → d e = 0)
    (hrow : ∀ v ∈ active S lo hi x, degree S d v = 0) : d = 0 := by
  have hint : ∀ e, x e = 0 ∨ x e = 1 → d e = 0 := by
    intro e he
    apply hd
    simp only [fractional, Finset.mem_filter, Finset.mem_univ, true_and, not_and]
    rcases he with h | h <;> simp [h]
  have hrows : ∀ v, degree S x v = (lo v : ℝ) ∨ degree S x v = (hi v : ℝ) →
      degree S d v = 0 := by
    intro v hv
    by_cases hn : (S v ∩ fractional x).Nonempty
    · exact hrow v (by simp [active, hv, hn])
    · apply Finset.sum_eq_zero
      intro e he
      exact hd e (fun hf => hn ⟨e, Finset.mem_inter.mpr ⟨he, hf⟩⟩)
  obtain ⟨t, ht, hp, hn⟩ := exists_symmetric_perturbation hx.1 hint hrows
  have hseg : x ∈ openSegment ℝ (x + t • d) (x - t • d) := by
    refine ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, ?_⟩
    ext e
    simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have he := hx.2 hp hn hseg
  have htd : t • d = 0 := add_left_cancel (he.trans (add_zero x).symm)
  exact (smul_eq_zero.mp htd).resolve_left (ne_of_gt ht)

theorem fractional_card_le_active_card {S : V → Finset E} {lo hi : V → ℤ}
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    (fractional x).card ≤ (active S lo hi x).card := by
  classical
  let A : Matrix (active S lo hi x) (fractional x) ℝ :=
    fun v e => if e.val ∈ S v.val then 1 else 0
  have hinj : Function.Injective A.mulVec := by
    intro a b hab
    let d : E → ℝ := fun e => if he : e ∈ fractional x then a ⟨e, he⟩ - b ⟨e, he⟩ else 0
    have hd : d = 0 := by
      apply extreme_kernel_eq_zero hx
      · intro e he
        simp [d, he]
      · intro v hv
        have heq := congrFun hab (⟨v, hv⟩ : active S lo hi x)
        have hsum : degree S d v = ∑ e : fractional x, A ⟨v, hv⟩ e * (a e - b e) := by
          calc
            degree S d v = ∑ e ∈ S v ∩ fractional x, d e := by
              symm
              apply Finset.sum_subset Finset.inter_subset_left
              intro e he hn
              have hf : e ∉ fractional x := fun hf => hn (Finset.mem_inter.mpr ⟨he, hf⟩)
              simp [d, hf]
            _ = ∑ e ∈ fractional x, if e ∈ S v then d e else 0 := by
              rw [← Finset.sum_filter]
              congr 1
              ext e
              simp [and_comm]
            _ = ∑ e : fractional x, if e.val ∈ S v then d e.val else 0 :=
              Finset.sum_subtype _ (fun _ => Iff.rfl) _
            _ = _ := by
              apply Finset.sum_congr rfl
              intro e he
              simp [A, d, e.property, ite_mul]
        rw [hsum]
        change (∑ e, A ⟨v, hv⟩ e * (a e - b e)) = 0
        simp only [mul_sub, Finset.sum_sub_distrib]
        exact sub_eq_zero.mpr heq
    ext e
    have h := congrFun hd e.val
    exact sub_eq_zero.mp (by simpa [d, e.property] using h)
  have hcard := (Matrix.mulVec_injective_iff.mp hinj).fintype_card_le_finrank
  simpa using hcard

omit [DecidableEq E] in
/-- A nonfractional coordinate of a cube point is binary. -/
theorem binary_of_not_fractional {x : E → ℝ} (hx : ∀ e, 0 ≤ x e ∧ x e ≤ 1)
    {e : E} (he : e ∉ fractional x) : x e = 0 ∨ x e = 1 := by
  simp only [fractional, Finset.mem_filter, Finset.mem_univ, true_and, not_and] at he
  rcases (hx e).1.eq_or_lt with h | h
  · exact Or.inl h.symm
  · exact Or.inr (le_antisymm (hx e).2 (not_lt.mp (he h)))

/-- Removing the integral coordinates from an integer tight row leaves an
integer sum on its fractional coordinates. -/
theorem active_fractional_sum_integer {S : V → Finset E} {lo hi : V → ℤ}
    {x : E → ℝ} (hx : x ∈ slab S lo hi) {v : V} (hv : v ∈ active S lo hi x) :
    ∃ k : ℤ, ∑ e ∈ S v ∩ fractional x, x e = (k : ℝ) := by
  classical
  have hact := (Finset.mem_filter.mp hv).2.1
  obtain ⟨k, hk⟩ : ∃ k : ℤ, degree S x v = (k : ℝ) := by
    rcases hact with h | h
    · exact ⟨lo v, h⟩
    · exact ⟨hi v, h⟩
  let rest := S v \ (S v ∩ fractional x)
  have hint : ∃ n : ℤ, ∑ e ∈ rest, x e = (n : ℝ) := by
    refine ⟨∑ e ∈ rest, if x e = 1 then (1 : ℤ) else 0, ?_⟩
    push_cast
    apply Finset.sum_congr rfl
    intro e he
    have hf : e ∉ fractional x := by
      have hh := Finset.mem_sdiff.mp he
      exact fun hf => hh.2 (Finset.mem_inter.mpr ⟨hh.1, hf⟩)
    rcases binary_of_not_fractional hx.1 hf with h | h <;> simp [h]
  obtain ⟨n, hn⟩ := hint
  refine ⟨k - n, ?_⟩
  have hsum := Finset.sum_sdiff (f := x) (Finset.inter_subset_left : S v ∩ fractional x ⊆ S v)
  change (∑ e ∈ rest, x e) + (∑ e ∈ S v ∩ fractional x, x e) = degree S x v at hsum
  rw [hn, hk] at hsum
  push_cast
  linarith

/-- Each active row contains at least two fractional edges. -/
theorem two_le_active_fractional_card {S : V → Finset E} {lo hi : V → ℤ}
    {x : E → ℝ} (hx : x ∈ slab S lo hi) {v : V} (hv : v ∈ active S lo hi x) :
    2 ≤ (S v ∩ fractional x).card := by
  have hpos := Finset.card_pos.mpr (Finset.mem_filter.mp hv).2.2
  by_contra hn
  have hone : (S v ∩ fractional x).card = 1 := by omega
  obtain ⟨e, he⟩ := Finset.card_eq_one.mp hone
  obtain ⟨k, hk⟩ := active_fractional_sum_integer hx hv
  rw [he, Finset.sum_singleton] at hk
  have hf : e ∈ fractional x :=
    Finset.mem_of_mem_inter_right (he.symm ▸ Finset.mem_singleton_self e)
  have hbounds := (Finset.mem_filter.mp hf).2
  rw [hk] at hbounds
  have hk0 : 0 < k := by exact_mod_cast hbounds.1
  have hk1 : k < 1 := by exact_mod_cast hbounds.2
  omega

omit [Fintype V] [Fintype E] in
/-- Double counting fractional incidences at active rows. -/
theorem incidence_count (S : V → Finset E) (R : Finset V) (F : Finset E) :
    ∑ v ∈ R, (S v ∩ F).card = ∑ e ∈ F, (R.filter fun v => e ∈ S v).card := by
  classical
  calc
    _ = ∑ v ∈ R, ∑ e ∈ F, if e ∈ S v then 1 else 0 := by
      apply Finset.sum_congr rfl
      intro v hv
      rw [← Finset.card_filter]
      congr 1
      ext e
      simp [and_comm]
    _ = ∑ e ∈ F, ∑ v ∈ R, if e ∈ S v then 1 else 0 := Finset.sum_comm
    _ = _ := by simp only [Finset.card_filter]

/-- Full rank and the incidence bound force equality in both incidence
counts: exactly two fractional edges at every active row, and exactly two
active endpoints at every fractional edge. -/
theorem extreme_fractional_degree_two {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    (∀ v ∈ active S lo hi x, (S v ∩ fractional x).card = 2) ∧
    (∀ e ∈ fractional x, ((active S lo hi x).filter fun v => e ∈ S v).card = 2) := by
  classical
  let R := active S lo hi x
  let F := fractional x
  have hrow : ∀ v ∈ R, 2 ≤ (S v ∩ F).card := fun v hv =>
    two_le_active_fractional_card hx.1 hv
  have hedge : ∀ e ∈ F, (R.filter fun v => e ∈ S v).card ≤ 2 := by
    intro e he
    apply le_trans (Finset.card_le_card ?_) (hfreq e)
    intro v hv
    simpa only [Finset.mem_filter, Finset.mem_univ, true_and] using
      (Finset.mem_filter.mp hv).2
  have hlow : 2 * R.card ≤ ∑ v ∈ R, (S v ∩ F).card := by
    simpa [Nat.mul_comm] using Finset.sum_le_sum hrow
  have hupp : (∑ e ∈ F, (R.filter fun v => e ∈ S v).card) ≤ 2 * F.card := by
    simpa [Nat.mul_comm] using Finset.sum_le_sum hedge
  have hcard : F.card ≤ R.card := fractional_card_le_active_card hx
  have hcount := incidence_count S R F
  have heqR : (∑ v ∈ R, 2) = ∑ v ∈ R, (S v ∩ F).card := by
    simp only [Finset.sum_const, smul_eq_mul]
    omega
  have heqF : (∑ e ∈ F, (R.filter fun v => e ∈ S v).card) = ∑ e ∈ F, 2 := by
    simp only [Finset.sum_const, smul_eq_mul]
    omega
  exact ⟨fun v hv => ((Finset.sum_eq_sum_iff_of_le hrow).mp heqR v hv).symm,
    (Finset.sum_eq_sum_iff_of_le hedge).mp heqF⟩

/-- The two fractional coordinates of each active row sum to one. -/
theorem extreme_active_fractional_sum_one {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {v : V} (hv : v ∈ active S lo hi x) :
    ∑ e ∈ S v ∩ fractional x, x e = 1 := by
  have hcard := (extreme_fractional_degree_two hfreq hx).1 v hv
  have hn := (Finset.mem_filter.mp hv).2.2
  have hlo : 0 < ∑ e ∈ S v ∩ fractional x, x e := by
    simpa using Finset.sum_lt_sum_of_nonempty hn (fun e he =>
      (Finset.mem_filter.mp (Finset.mem_inter.mp he).2).2.1)
  have hhi : (∑ e ∈ S v ∩ fractional x, x e) < 2 := by
    have h := Finset.sum_lt_sum_of_nonempty hn (fun e he =>
      (Finset.mem_filter.mp (Finset.mem_inter.mp he).2).2.2)
    simpa [hcard] using h
  obtain ⟨k, hk⟩ := active_fractional_sum_integer hx.1 hv
  rw [hk] at hlo hhi ⊢
  have hk0 : 0 < k := by exact_mod_cast hlo
  have hk2 : k < 2 := by exact_mod_cast hhi
  have hk1 : k = 1 := by omega
  simp [hk1]

omit [Fintype E] in
/-- Every extreme point of an integer degree slab with edge frequency at
most two is half integral. No graph simplicity or bound nondegeneracy is
required. -/
theorem extreme_half_integral [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    ∀ e, x e = 0 ∨ x e = 1 / 2 ∨ x e = 1 := by
  let := Fintype.ofFinite E
  classical
  let d : E → ℝ := fun e => if e ∈ fractional x then x e - 1 / 2 else 0
  have hd : d = 0 := by
    apply extreme_kernel_eq_zero hx
    · intro e he
      simp [d, he]
    · intro v hv
      have hrestrict : degree S d v = ∑ e ∈ S v ∩ fractional x, (x e - 1 / 2) := by
        calc
          _ = ∑ e ∈ S v ∩ fractional x, d e := by
            symm
            apply Finset.sum_subset Finset.inter_subset_left
            intro e he hn
            have hf : e ∉ fractional x := fun hf => hn (Finset.mem_inter.mpr ⟨he, hf⟩)
            simp [d, hf]
          _ = _ := Finset.sum_congr rfl (fun e he => by simp [d, (Finset.mem_inter.mp he).2])
      rw [hrestrict, Finset.sum_sub_distrib, extreme_active_fractional_sum_one hfreq hx hv]
      simp [(extreme_fractional_degree_two hfreq hx).1 v hv]
  intro e
  by_cases he : e ∈ fractional x
  · right
    left
    have h := congrFun hd e
    simpa [d, he] using (sub_eq_zero.mp (by simpa [d, he] using h) : x e = 1 / 2)
  · rcases binary_of_not_fractional hx.1.1 he with h | h
    · exact Or.inl h
    · exact Or.inr (Or.inr h)

/-- Every fractional coordinate of an extreme slab point is one half. -/
theorem extreme_fractional_eq_half {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {e : E} (he : e ∈ fractional x) : x e = 1 / 2 := by
  have hb := (Finset.mem_filter.mp he).2
  rcases extreme_half_integral hfreq hx e with h | h | h
  · linarith
  · exact h
  · linarith

/-- Every endpoint of a fractional edge is active; slack degree rows never
meet the fractional subgraph. -/
theorem active_of_fractional_incident {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {e : E} (he : e ∈ fractional x) {v : V} (hv : e ∈ S v) :
    v ∈ active S lo hi x := by
  classical
  have hsub : ((active S lo hi x).filter fun v => e ∈ S v) ⊆
      (Finset.univ.filter fun v => e ∈ S v) := by
    intro w hw
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, (Finset.mem_filter.mp hw).2⟩
  have heq : ((active S lo hi x).filter fun v => e ∈ S v) =
      (Finset.univ.filter fun v => e ∈ S v) := by
    apply Finset.eq_of_subset_of_card_le hsub
    rw [(extreme_fractional_degree_two hfreq hx).2 e he]
    exact hfreq e
  have hm : v ∈ (active S lo hi x).filter fun v => e ∈ S v := by
    rw [heq]
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, hv⟩
  exact (Finset.mem_filter.mp hm).1

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- The degree slab is convex. -/
theorem slab_convex (S : V → Finset E) (lo hi : V → ℤ) : Convex ℝ (slab S lo hi) := by
  intro x hx y hy a b ha hb hab
  refine ⟨fun e => ?_, fun v => ?_⟩
  · exact (convex_Icc (𝕜 := ℝ) (0 : ℝ) 1) (hx.1 e) (hy.1 e) ha hb hab
  · have h := (convex_Icc (𝕜 := ℝ) (lo v : ℝ) (hi v : ℝ)) (hx.2 v) (hy.2 v) ha hb hab
    simpa [degree, Finset.sum_add_distrib, Finset.mul_sum] using h

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- The slab is compact, including the empty and lower-dimensional cases. -/
theorem slab_compact (S : V → Finset E) (lo hi : V → ℤ) : IsCompact (slab S lo hi) := by
  have hc : IsClosed (slab S lo hi) := by
    change IsClosed ({x : E → ℝ | ∀ e, 0 ≤ x e ∧ x e ≤ 1} ∩
      {x : E → ℝ | ∀ v, (lo v : ℝ) ≤ degree S x v ∧ degree S x v ≤ (hi v : ℝ)})
    apply IsClosed.inter
    · rw [Set.ofPred_forall]
      apply isClosed_iInter
      intro e
      exact (isClosed_le continuous_const (continuous_apply e)).inter
        (isClosed_le (continuous_apply e) continuous_const)
    · rw [Set.ofPred_forall]
      apply isClosed_iInter
      intro v
      have hdeg : Continuous (fun x : E → ℝ => degree S x v) := by
        unfold degree
        fun_prop
      exact (isClosed_le continuous_const hdeg).inter (isClosed_le hdeg continuous_const)
  apply (isCompact_pi_infinite (fun _ : E =>
    isCompact_Icc (a := (0 : ℝ)) (b := 1))).of_isClosed_subset hc
  exact fun _ hx => hx.1

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- The original vector belongs to the slab with floor/ceiling degree bounds. -/
theorem mem_floor_ceil_slab (S : V → Finset E) {x : E → ℝ}
    (hx : ∀ e, 0 ≤ x e ∧ x e ≤ 1) :
    x ∈ slab S (fun v => ⌊degree S x v⌋) (fun v => ⌈degree S x v⌉) :=
  ⟨hx, fun _ => ⟨Int.floor_le _, Int.le_ceil _⟩⟩

omit [Fintype E] in
/-- There are finitely many extreme points: half-integral points lie in a
finite product of three-element coordinate sets. -/
theorem extremePoints_finite [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2) :
    ((slab S lo hi).extremePoints ℝ).Finite := by
  let := Fintype.ofFinite E
  have hf : (Set.univ.pi (fun _ : E => ({0, 1 / 2, 1} : Set ℝ))).Finite :=
    Set.Finite.pi (fun _ => by simp)
  apply hf.subset
  intro x hx e he
  simpa only [Set.mem_insert_iff, Set.mem_singleton_iff] using extreme_half_integral hfreq hx e

omit [Fintype E] in
/-- Every point is a finite convex combination of extreme slab points.
Those points have the half-integral and incidence conclusions proved above. -/
theorem convexHull_extremePoints_eq [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2) :
    convexHull ℝ ((slab S lo hi).extremePoints ℝ) = slab S lo hi := by
  let := Fintype.ofFinite E
  have hclosed :=
    ((extremePoints_finite (lo := lo) (hi := hi) hfreq).isCompact_convexHull ℝ).isClosed
  rw [← hclosed.closure_eq]
  exact closure_convexHull_extremePoints (slab_compact S lo hi) (slab_convex S lo hi)

omit [Fintype E] in
/-- A finite probability law on actual extreme slab points, with the
prescribed barycenter. The finite state space is explicitly `Fin n`. -/
theorem exists_extreme_law [Finite E] {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {p : E → ℝ} (hp : p ∈ slab S lo hi) :
    ∃ (n : ℕ) (μ : CubicGap.Law (Fin n)) (z : Fin n → E → ℝ),
      (∀ a, z a ∈ (slab S lo hi).extremePoints ℝ) ∧ μ.barycenter z = p := by
  let := Fintype.ofFinite E
  classical
  let T := (slab S lo hi).extremePoints ℝ
  let : Fintype T := (extremePoints_finite hfreq).fintype
  let e := Fintype.equivFin T
  let z : Fin (Fintype.card T) → E → ℝ := fun a => (e.symm a).val
  have hz : Set.range z = T := by
    ext x
    constructor
    · rintro ⟨a, rfl⟩
      exact (e.symm a).property
    · intro hx
      exact ⟨e ⟨x, hx⟩, by simp [z]⟩
  have hmem : p ∈ convexHull ℝ (Set.range z) := by
    rw [hz, show T = (slab S lo hi).extremePoints ℝ from rfl,
      convexHull_extremePoints_eq hfreq]
    exact hp
  obtain ⟨μ, hμ⟩ := (CubicGap.Law.mem_convexHull_range_iff z p).mp hmem
  exact ⟨Fintype.card T, μ, z, fun a => (e.symm a).property, hμ⟩

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- Coverage is affine on every floor/ceiling slab: it is the degree below
one and is constantly one above that threshold. -/
theorem cap_eq_of_mem_floor_ceil_slab {S : V → Finset E} {p z : E → ℝ}
    (hz : z ∈ slab S (fun v => ⌊degree S p v⌋) (fun v => ⌈degree S p v⌉))
    (v : V) :
    min 1 (degree S z v) = if degree S p v < 1 then degree S z v else 1 := by
  split_ifs with hp
  · apply min_eq_right
    have hc : ⌈degree S p v⌉ ≤ (1 : ℤ) := Int.ceil_le.mpr (by simpa using hp.le)
    have hc' : (⌈degree S p v⌉ : ℝ) ≤ 1 := by exact_mod_cast hc
    exact (hz.2 v).2.trans hc'
  · apply min_eq_left
    have hf : (1 : ℤ) ≤ ⌊degree S p v⌋ := Int.le_floor.mpr (by simpa using not_lt.mp hp)
    have hf' : (1 : ℝ) ≤ (⌊degree S p v⌋ : ℝ) := by exact_mod_cast hf
    exact hf'.trans (hz.2 v).1

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- Taking degree sums commutes with taking the finite barycenter. -/
theorem expect_degree {A : Type*} [Fintype A] (μ : CubicGap.Law A)
    (S : V → Finset E) (z : A → E → ℝ) (v : V) :
    μ.expect (fun a => degree S (z a) v) = degree S (μ.barycenter z) v := by
  simp only [CubicGap.Law.expect, degree, CubicGap.Law.barycenter,
    Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  exact Finset.sum_comm

omit [Fintype V] [Fintype E] [DecidableEq E] in
/-- Coverage caps are preserved exactly when a finite law remains inside
the original vector's floor/ceiling degree slab. -/
theorem expect_cap {A : Type*} [Fintype A] (μ : CubicGap.Law A)
    {S : V → Finset E} {p : E → ℝ} {z : A → E → ℝ}
    (hz : ∀ a, z a ∈ slab S (fun v => ⌊degree S p v⌋) (fun v => ⌈degree S p v⌉))
    (hmean : μ.barycenter z = p) (v : V) :
    μ.expect (fun a => min 1 (degree S (z a) v)) = min 1 (degree S p v) := by
  simp_rw [cap_eq_of_mem_floor_ceil_slab (hz _) v]
  by_cases hp : degree S p v < 1
  · simp only [hp, if_true, min_eq_right hp.le]
    rw [expect_degree, hmean]
  · simp only [hp, if_false, min_eq_left (not_lt.mp hp), CubicGap.Law.expect_const]

end
end MultilinearGap.FrequencySlab
