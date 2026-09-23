import Formal.QuadraticPrecision.BinaryModel

/-! Minimum counts retain the possibility that no finite lift exists. Positive
accuracy existence is proved by the explicit constructions, not built into
the definition of a minimum. -/
namespace QuadraticPrecision
noncomputable section

/-- A count is attained and no smaller count is feasible. -/
def IsMinimumCount (feasible : ℕ → Prop) (p : ℕ) : Prop :=
  feasible p ∧ ∀ k, feasible k → p ≤ k

theorem exists_minimumCount {feasible : ℕ → Prop} (h : ∃ p, feasible p) :
    ∃ p, IsMinimumCount feasible p := by
  classical
  exact ⟨Nat.find h, Nat.find_spec h, fun k hk => Nat.find_min' h hk⟩

theorem IsMinimumCount.unique {feasible : ℕ → Prop} {p q : ℕ}
    (hp : IsMinimumCount feasible p) (hq : IsMinimumCount feasible q) : p = q :=
  Nat.le_antisymm (hp.2 q hq.1) (hq.2 p hp.1)

theorem minimumCount_of_threshold {feasible : ℕ → Prop} {p : ℕ}
    (hupper : feasible p) (hlower : ∀ k, feasible k → p ≤ k) :
    IsMinimumCount feasible p := ⟨hupper, hlower⟩

variable {n : ℕ} {D : Set (Input n)} {f : Input n → ℝ} {ε δ : ℝ} {p : ℕ}

theorem IsGraphRelaxation.mono_error {R : Set (Input n × ℝ)}
    (h : IsGraphRelaxation D f ε R) (hεδ : ε ≤ δ) : IsGraphRelaxation D f δ R :=
  ⟨h.1, fun v hv => ⟨(h.2 v hv).1, (h.2 v hv).2.trans hεδ⟩⟩

theorem IsEpigraphRelaxation.mono_error {R : Set (Input n × ℝ)}
    (h : IsEpigraphRelaxation D f ε R) (hεδ : ε ≤ δ) : IsEpigraphRelaxation D f δ R := by
  refine ⟨h.1, fun v hv => ⟨(h.2 v hv).1, ?_⟩⟩
  exact (sub_le_sub_left hεδ _).trans (h.2 v hv).2

theorem IsHypographRelaxation.mono_error {R : Set (Input n × ℝ)}
    (h : IsHypographRelaxation D f ε R) (hεδ : ε ≤ δ) : IsHypographRelaxation D f δ R :=
  ⟨h.1, fun v hv => ⟨(h.2 v hv).1, (h.2 v hv).2.trans (add_le_add_right hεδ _)⟩⟩

theorem HasGraphLift.mono_error (h : HasGraphLift D f ε p) (hεδ : ε ≤ δ) :
    HasGraphLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

theorem HasBinaryGraphLift.mono_error (h : HasBinaryGraphLift D f ε p) (hεδ : ε ≤ δ) :
    HasBinaryGraphLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

theorem HasEpigraphLift.mono_error (h : HasEpigraphLift D f ε p) (hεδ : ε ≤ δ) :
    HasEpigraphLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

theorem HasBinaryEpigraphLift.mono_error (h : HasBinaryEpigraphLift D f ε p) (hεδ : ε ≤ δ) :
    HasBinaryEpigraphLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

theorem HasHypographLift.mono_error (h : HasHypographLift D f ε p) (hεδ : ε ≤ δ) :
    HasHypographLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

theorem HasBinaryHypographLift.mono_error (h : HasBinaryHypographLift D f ε p) (hεδ : ε ≤ δ) :
    HasBinaryHypographLift D f δ p := by
  obtain ⟨q, L, h⟩ := h
  exact ⟨q, L, h.mono_error hεδ⟩

end
end QuadraticPrecision
