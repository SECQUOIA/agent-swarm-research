import Formal.FBBT.Lift
import Formal.FBBT.Limits

/-! Actual primitive FBBT from the original unit box, with arbitrary update order. -/
namespace FBBT

abbrev PrimitiveRun (n : ℕ) (schedule : ℕ → CircuitVar n)
    (states : ℕ → Box (CircuitVar n)) :=
  Box.Run (equations n) (Box.unit (CircuitVar n)) schedule states

noncomputable def originalRun (n : ℕ) (schedule : ℕ → CircuitVar n) :
    ℕ → Box (CircuitVar n) := Box.iterate (equations n) (Box.unit _) schedule

theorem point_mem_unit (n : ℕ) : circuitPoint n ∈ (Box.unit (CircuitVar n)).carrier :=
  circuitPoint_mem_unit n

theorem point_mem_equations (n : ℕ) (a : CircuitVar n) : circuitPoint n ∈ equations n a :=
  circuitPoint_solution n a

/-- The quantification over primitive runs is nonvacuous for every schedule. -/
theorem originalRun_isRun (n : ℕ) (schedule : ℕ → CircuitVar n) :
    PrimitiveRun n schedule (originalRun n schedule) :=
  Box.iterate_run (equations n) (Box.unit _) schedule (point_mem_unit n) (point_mem_equations n)

theorem PrimitiveRun.point_mem {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    circuitPoint n ∈ (states t).carrier :=
  h.preserves (point_mem_unit n) (point_mem_equations n) t

theorem PrimitiveRun.lower_monotone {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (a : CircuitVar n) :
    Monotone fun t => (states t).lower a :=
  Box.Run.lower_monotone h (point_mem_unit n) (point_mem_equations n) a

theorem PrimitiveRun.lower_nonnegative {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ)
    (a : CircuitVar n) : 0 ≤ (states t).lower a := by
  have hh := h.lower_monotone a (Nat.zero_le t)
  simpa [h.initial, Box.unit] using hh

/-- Nonnegative primitive right sides are monotone on the nonnegative orthant. -/
theorem PrimitiveRhs.eval_mono {ι : Type*} (r : PrimitiveRhs ι)
    {x y : ι → ℝ} (hx : ∀ i, 0 ≤ x i) (hxy : ∀ i, x i ≤ y i) :
    r.eval x ≤ r.eval y := by
  cases r with
  | half => exact le_rfl
  | copy a => exact hxy a
  | add a b => exact add_le_add (hxy a) (hxy b)
  | mul a b => exact mul_le_mul (hxy a) (hxy b) (hx b) ((hx a).trans (hxy a))

/-- The exact bidirectional hull enforces the ordinary forward lower bound. -/
theorem PrimitiveRun.forward {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (circuitRhs n (schedule t)).eval (states t).lower ≤ (states (t + 1)).lower (schedule t) := by
  apply Box.forward_lower (h.step t) ⟨circuitPoint n, h.point_mem (t + 1)⟩
  intro x hx
  have he : x (schedule t) = (circuitRhs n (schedule t)).eval x := hx.2
  rw [he]
  exact PrimitiveRhs.eval_mono _ (h.lower_nonnegative t) (fun i => (hx.1 i).1)

/-- Every fair primitive run from the original unit box converges in its lower
endpoints to the unique feasible point, without bounded-delay assumptions. -/
theorem PrimitiveRun.lower_tendsto {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states)
    (hf : FairSchedule schedule) :
    Filter.Tendsto (fun t => (states t).lower) Filter.atTop (nhds (circuitPoint n)) :=
  fair_circuit_lower_tendsto h.lower_monotone h.lower_nonnegative
    (fun t a => (h.point_mem t a).1) hf h.forward

/-- The designated lower endpoint tends to one for every fair primitive schedule. -/
theorem PrimitiveRun.z_tendsto_one {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states)
    (hf : FairSchedule schedule) :
    Filter.Tendsto (fun t => (states t).lower .z) Filter.atTop (nhds 1) := by
  simpa [circuitPoint] using (h.lower_tendsto hf).apply_nhds CircuitVar.z

theorem PrimitiveRun.upper_antitone {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (a : CircuitVar n) :
    Antitone fun t => (states t).upper a :=
  Box.Run.upper_antitone h (point_mem_unit n) (point_mem_equations n) a

theorem PrimitiveRun.forward_upper {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (states (t + 1)).upper (schedule t) ≤ (circuitRhs n (schedule t)).eval (states t).upper := by
  apply Box.forward_upper (h.step t) ⟨circuitPoint n, h.point_mem (t + 1)⟩
  intro x hx
  have he : x (schedule t) = (circuitRhs n (schedule t)).eval x := hx.2
  rw [he]
  exact PrimitiveRhs.eval_mono _
    (fun i => (h.lower_nonnegative t i).trans (hx.1 i).1) (fun i => (hx.1 i).2)

theorem PrimitiveRun.upper_tendsto {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states)
    (hf : FairSchedule schedule) :
    Filter.Tendsto (fun t => (states t).upper) Filter.atTop (nhds (circuitPoint n)) := by
  apply fair_circuit_upper_tendsto h.upper_antitone
    (fun t a => (h.point_mem t a).2) _ hf h.forward_upper
  simp [h.initial, Box.unit]

/-- Both endpoint vectors converge to the unique feasible point; the limiting
box is a singleton, even from the original uninformative unit box. -/
theorem PrimitiveRun.singleton_limit {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states)
    (hf : FairSchedule schedule) :
    Filter.Tendsto (fun t => (states t).lower) Filter.atTop (nhds (circuitPoint n)) ∧
    Filter.Tendsto (fun t => (states t).upper) Filter.atTop (nhds (circuitPoint n)) :=
  ⟨h.lower_tendsto hf, h.upper_tendsto hf⟩

end FBBT
