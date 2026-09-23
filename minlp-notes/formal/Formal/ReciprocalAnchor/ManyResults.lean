import Formal.ReciprocalAnchor.ManyLaws
import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyIntegrals
import Formal.ReciprocalAnchor.ManySelection
import Formal.ReciprocalAnchor.ManyEnvelopeBound

/-! The exact graph-hull theorem, with common finite laws and sharp support bounds. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {n : ℕ} {a b : ℝ}

def Law.Realizes (μ : Law a b) (q w : Fin n → ℝ) : Prop :=
  ∃ y : Fin μ.size → Fin n → ℝ, (∀ i j, 0 ≤ y i j ∧ y i j ≤ 1) ∧
    (∀ j, ∑ i, μ.mass i * y i j = q j) ∧
    (∀ j, ∑ i, μ.mass i * (μ.location i * y i j) = w j)

theorem Law.realizes_iff (μ : Law a b) (q w : Fin n → ℝ) :
    μ.Realizes q w ↔ (∀ j, 0 ≤ q j ∧ q j ≤ 1) ∧
      ∀ s, envelope μ.mean q w s ≤ μ.call s := by
  constructor
  · rintro ⟨y, hy, hq, hw⟩
    have hn (j : Fin n) := selection_necessary μ.mass μ.location (fun i => y i j)
      μ.nonneg μ.total (fun i => hy i j)
    have hm (j : Fin n) : selectionMass μ.mass (fun i => y i j) = q j := hq j
    have hv (j : Fin n) : selectionMoment μ.mass μ.location (fun i => y i j) = w j := by
      simpa only [selectionMoment, mul_assoc] using hw j
    refine ⟨fun j => ?_, fun s => envelope_le_iff.mpr ⟨μ.call_nonneg s, μ.mean_sub_le_call s,
      fun j => ?_⟩⟩
    · exact ⟨by simpa only [hm j] using (hn j).1,
        by simpa only [hm j] using (hn j).2.1⟩
    · simpa only [hm j, hv j, selectionMean, selectionCall, Law.mean, Law.call] using (hn j).2.2 s
  · rintro ⟨hq, hc⟩
    obtain ⟨y, hy⟩ := simultaneous_fractional_selection μ.mass μ.location μ.nonneg μ.total q w
      (fun j => ⟨(hq j).1, (hq j).2, fun s => (envelope_le_iff.mp (hc s)).2.2 j⟩)
    refine ⟨fun i j => y j i, fun i j => (hy j).1 i, fun j => (hy j).2.1, fun j => ?_⟩
    simpa only [selectionMoment, mul_assoc] using (hy j).2.2

theorem Law.realizes_mem_hull (μ : Law a b) {q w : Fin n → ℝ} (h : μ.Realizes q w) :
    point μ.mean μ.reciprocal q w ∈ hull n a b := by
  obtain ⟨y, hy, hq, hw⟩ := h
  exact finite_representation_mem_hull μ.mass μ.location y μ.nonneg μ.total μ.bounds
    hy rfl rfl hq hw

theorem mem_hull_iff_law {m t : ℝ} {q w : Fin n → ℝ} :
    point m t q w ∈ hull n a b ↔
      ∃ μ : Law a b, μ.mean = m ∧ μ.reciprocal = t ∧ μ.Realizes q w := by
  constructor
  · intro h
    obtain ⟨ι, _, p, x, y, hp, hp1, hx, hy, hm, ht, hq, hw⟩ :=
      mem_hull_has_finite_representation h
    refine ⟨Law.ofFinite p x hp hp1 hx, ?_, ?_, ?_⟩
    · exact (Law.ofFinite_mean p x hp hp1 hx).trans hm
    · exact (Law.ofFinite_reciprocal p x hp hp1 hx).trans ht
    · refine ⟨fun i => y ((Fintype.equivFin ι).symm i), fun i j => hy _ j, ?_, ?_⟩
      · intro j
        exact (Equiv.sum_comp (Fintype.equivFin ι).symm (fun i => p i * y i j)).trans (hq j)
      · intro j
        exact (Equiv.sum_comp (Fintype.equivFin ι).symm
          (fun i => p i * (x i * y i j))).trans (hw j)
  · rintro ⟨μ, hm, ht, hr⟩
    simpa only [hm, ht] using μ.realizes_mem_hull hr

theorem mem_hull_lowerMoment {m t : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : point m t q w ∈ hull n a b) :
    lowerMoment a b m q w ≤ t := by
  obtain ⟨μ, hm, ht, hr⟩ := mem_hull_iff_law.mp h
  have hc := (μ.realizes_iff q w).mp hr
  have hb := μ.reciprocal_lower_of_call_le ha hab.le
    (envelope_continuous μ.mean q w).continuousOn (fun s _ => hc.2 s)
  simpa only [hm, ht, lowerMoment] using hb

/-- The minimizing law is constructed from the upper envelope; all leaves are
then selected on this same law. No representing measure is an input premise. -/
theorem exists_minimizing_law {m : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : LinearBounds a b m q w) :
    ∃ μ : Law a b, μ.size ≤ 2 * n + 1 ∧ μ.mean = m ∧
      μ.reciprocal = lowerMoment a b m q w ∧ μ.Realizes q w := by
  obtain ⟨μ, hsize, hm, hc⟩ := envelope_exists_small_law hab h
  refine ⟨μ, hsize, hm, ?_, (μ.realizes_iff q w).mpr ⟨fun j => ⟨(h.2.2 j).1, (h.2.2 j).2.1⟩,
    fun s => ?_⟩⟩
  · rw [μ.reciprocal_eq_call_integral ha hab.le, hm, hc]
    rfl
  · rw [hm, hc]

theorem endpoint_law_realizes {m : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : LinearBounds a b m q w) :
    (Law.endpoints a b m hab ⟨h.1, h.2.1⟩).Realizes q w := by
  obtain ⟨μ, _, hm, _, hr⟩ := exists_minimizing_law ha hab h
  apply (Law.realizes_iff _ q w).mpr
  refine ⟨fun j => ⟨(h.2.2 j).1, (h.2.2 j).2.1⟩, fun s => ?_⟩
  have hc := ((μ.realizes_iff q w).mp hr).2 s
  have he := μ.call_le_endpoints hab s
  rw [hm] at hc
  rw [Law.endpoints_call, hm] at he
  rw [Law.endpoints_mean, Law.endpoints_call]
  exact hc.trans he

theorem exists_hull_law {m t : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) (h : LinearBounds a b m q w)
    (ht : lowerMoment a b m q w ≤ t ∧ t ≤ (a + b - m) / (a * b)) :
    ∃ μ : Law a b, μ.size ≤ 2 * n + 3 ∧ μ.mean = m ∧ μ.reciprocal = t ∧ μ.Realizes q w := by
  obtain ⟨μ, hsize, hm, hrec, hr⟩ := exists_minimizing_law ha hab h
  let ν := Law.endpoints a b m hab ⟨h.1, h.2.1⟩
  have hn : ν.mean = m := Law.endpoints_mean m hab ⟨h.1, h.2.1⟩
  have htν : ν.reciprocal = (a + b - m) / (a * b) :=
    Law.endpoints_reciprocal m ha hab ⟨h.1, h.2.1⟩
  have hL : μ.reciprocal ≤ t := by simpa only [hrec] using ht.1
  have hU : t ≤ ν.reciprocal := by simpa only [htν] using ht.2
  by_cases heq : μ.reciprocal = ν.reciprocal
  · refine ⟨μ, by omega, hm, le_antisymm hL (by simpa [heq] using hU), hr⟩
  · have hd : 0 < ν.reciprocal - μ.reciprocal :=
      sub_pos.mpr (lt_of_le_of_ne (hL.trans hU) heq)
    let r := (t - μ.reciprocal) / (ν.reciprocal - μ.reciprocal)
    have hrange : 0 ≤ r ∧ r ≤ 1 :=
      ⟨div_nonneg (sub_nonneg.mpr hL) hd.le, (div_le_one hd).mpr (by linarith)⟩
    let ξ := μ.mix ν r hrange
    have hmean : ξ.mean = m := by dsimp [ξ]; rw [Law.mix_mean, hm, hn]; ring
    refine ⟨ξ, ?_, hmean, ?_, (ξ.realizes_iff q w).mpr
      ⟨fun j => ⟨(h.2.2 j).1, (h.2.2 j).2.1⟩, fun s => ?_⟩⟩
    · dsimp [ξ]
      rw [Law.mix_size]
      have hnsize : ν.size = 2 := rfl
      omega
    · dsimp [ξ]
      rw [Law.mix_reciprocal]
      dsimp [r]
      field_simp
      ring
    · rw [hmean]
      have hcμ := ((μ.realizes_iff q w).mp hr).2 s
      have hcν := ((ν.realizes_iff q w).mp (endpoint_law_realizes ha hab h)).2 s
      rw [hm] at hcμ
      rw [hn] at hcν
      change envelope m q w s ≤ (μ.mix ν r hrange).call s
      rw [Law.mix_call]
      calc
        envelope m q w s = (1-r) * envelope m q w s + r * envelope m q w s := by ring
        _ ≤ _ := add_le_add (mul_le_mul_of_nonneg_left hcμ (sub_nonneg.mpr hrange.2))
          (mul_le_mul_of_nonneg_left hcν hrange.1)

theorem mem_hull_iff_bounds {m t : ℝ} {q w : Fin n → ℝ}
    (ha : 0 < a) (hab : a < b) :
    point m t q w ∈ hull n a b ↔ LinearBounds a b m q w ∧
      lowerMoment a b m q w ≤ t ∧ t ≤ (a + b - m) / (a * b) := by
  constructor
  · intro h
    exact ⟨mem_hull_linearBounds ha hab h, mem_hull_lowerMoment ha hab h,
      mem_hull_reciprocal_upper ha hab h⟩
  · rintro ⟨hl, ht⟩
    obtain ⟨μ, _, hm, hrec, hr⟩ := exists_hull_law ha hab hl ht
    exact mem_hull_iff_law.mpr ⟨μ, hm, hrec, hr⟩

end ReciprocalAnchor.ManyLeaf
