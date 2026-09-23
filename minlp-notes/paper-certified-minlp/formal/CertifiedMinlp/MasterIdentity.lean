import CertifiedMinlp.DiscreteRows

/-! Exact identity checks for rational masters up to variable renaming, positive
row scaling, and row permutation. File parsing is outside this algebraic result. -/
namespace CertifiedMinlp.MasterIdentity
open CertifiedMinlp.Discrete

variable {n m : ℕ}

def renamePoint (e : Fin n ≃ Fin m) (x : Fin n → ℝ) : Fin m → ℝ :=
  fun j => x (e.symm j)

def renameRow (e : Fin n ≃ Fin m) (r : Row n) : Row m :=
  ⟨fun j => r.coeff (e.symm j), r.rhs, r.kind⟩

theorem rename_value (e : Fin n ≃ Fin m) (r : Row n) (x : Fin n → ℝ) :
    value (renameRow e r) (renamePoint e x) = value r x := by
  unfold value renameRow renamePoint
  exact Equiv.sum_comp e.symm (fun i => (r.coeff i : ℝ) * x i)

theorem rename_holds (e : Fin n ≃ Fin m) (r : Row n) (x : Fin n → ℝ) :
    Holds (renameRow e r) (renamePoint e x) ↔ Holds r x := by
  change Discrete.Rel r.kind (value (renameRow e r) (renamePoint e x)) r.rhs ↔ _
  rw [rename_value]
  rfl

def scaleRow (q : ℚ) (r : Row n) : Row n :=
  ⟨fun i => q * r.coeff i, q * r.rhs, r.kind⟩

theorem scale_value (q : ℚ) (r : Row n) (x : Fin n → ℝ) :
    value (scaleRow q r) x = (q : ℝ) * value r x := by
  simp [value, scaleRow, Finset.mul_sum, mul_assoc]

theorem scale_holds (q : ℚ) (hq : 0 < q) (r : Row n) (x : Fin n → ℝ) :
    Holds (scaleRow q r) x ↔ Holds r x := by
  have hq' : (0 : ℝ) < q := by exact_mod_cast hq
  change Discrete.Rel r.kind (value (scaleRow q r) x) (q * r.rhs : ℚ) ↔ _
  rw [scale_value, Rat.cast_mul]
  cases hk : r.kind <;> simp [Holds, hk, Discrete.Rel, mul_le_mul_iff_right₀ hq',
    ne_of_gt hq]

theorem rename_integral (e : Fin n ≃ Fin m) (ints : Fin n → Bool)
    (x : Fin n → ℝ) :
    Integral (fun j => ints (e.symm j)) (renamePoint e x) ↔ Integral ints x := by
  constructor
  · intro h i hi
    simpa [renamePoint] using h (e i) (by simpa using hi)
  · intro h j hj
    exact h (e.symm j) hj

structure Master (n : ℕ) where
  rows : List (Row n)
  integers : Fin n → Bool
  objectiveCoeff : Fin n → ℚ
  objectiveConstant : ℚ

def Master.Feasible (M : Master n) (x : Fin n → ℝ) : Prop :=
  Integral M.integers x ∧ ∀ r ∈ M.rows, Holds r x

def Master.objective (M : Master n) (x : Fin n → ℝ) : ℝ :=
  ∑ i, (M.objectiveCoeff i : ℝ) * x i + M.objectiveConstant

/-- The witness associates each source row with a strictly positive rational
scale. Both permutations are checked, so no row can be silently omitted. -/
def checkMaster (e : Fin n ≃ Fin m) (source : Master n) (target : Master m)
    (witness : List (ℚ × Row n)) : Bool :=
  decide ((∀ t ∈ witness, 0 < t.1) ∧
    source.rows.Perm (witness.map Prod.snd) ∧
    target.rows.Perm (witness.map (fun t => renameRow e (scaleRow t.1 t.2))) ∧
    (∀ j, target.integers j = source.integers (e.symm j)) ∧
    (∀ j, target.objectiveCoeff j = source.objectiveCoeff (e.symm j)) ∧
    target.objectiveConstant = source.objectiveConstant)

theorem matches_feasible (e : Fin n ≃ Fin m) (source : Master n) (target : Master m)
    (witness : List (ℚ × Row n)) (h : checkMaster e source target witness = true)
    (x : Fin n → ℝ) : target.Feasible (renamePoint e x) ↔ source.Feasible x := by
  obtain ⟨hpos, hs, ht, hi, _, _⟩ := of_decide_eq_true h
  have hints : target.integers = fun j => source.integers (e.symm j) := funext hi
  constructor
  · rintro ⟨hint, hrows⟩
    refine ⟨(rename_integral e source.integers x).mp (by simpa [hints] using hint), ?_⟩
    intro r hr
    obtain ⟨t, htw, htr⟩ := List.mem_map.mp (hs.mem_iff.mp hr)
    have htarget : renameRow e (scaleRow t.1 t.2) ∈ target.rows :=
      ht.mem_iff.mpr (List.mem_map.mpr ⟨t, htw, rfl⟩)
    have hh := (rename_holds e (scaleRow t.1 t.2) x).mp (hrows _ htarget)
    have hh' := (scale_holds t.1 (hpos t htw) t.2 x).mp hh
    simpa only [htr] using hh'
  · rintro ⟨hint, hrows⟩
    refine ⟨by simpa [hints] using (rename_integral e source.integers x).mpr hint, ?_⟩
    intro r hr
    obtain ⟨t, htw, htr⟩ := List.mem_map.mp (ht.mem_iff.mp hr)
    have hsource : t.2 ∈ source.rows := hs.mem_iff.mpr (List.mem_map.mpr ⟨t, htw, rfl⟩)
    have hh := (scale_holds t.1 (hpos t htw) t.2 x).mpr (hrows _ hsource)
    have hh' := (rename_holds e (scaleRow t.1 t.2) x).mpr hh
    simpa only [htr] using hh'

theorem matches_objective (e : Fin n ≃ Fin m) (source : Master n) (target : Master m)
    (witness : List (ℚ × Row n)) (h : checkMaster e source target witness = true)
    (x : Fin n → ℝ) : target.objective (renamePoint e x) = source.objective x := by
  obtain ⟨_, _, _, _, hc, hb⟩ := of_decide_eq_true h
  simp only [Master.objective, hc, hb, renamePoint]
  congr 1
  exact Equiv.sum_comp e.symm (fun i => (source.objectiveCoeff i : ℝ) * x i)

/-- Checked matching gives a bijection of feasible points preserving objective values. -/
theorem matches_attainable_values (e : Fin n ≃ Fin m) (source : Master n)
    (target : Master m) (witness : List (ℚ × Row n))
    (h : checkMaster e source target witness = true) (v : ℝ) :
    (∃ y, target.Feasible y ∧ target.objective y = v) ↔
      ∃ x, source.Feasible x ∧ source.objective x = v := by
  constructor
  · rintro ⟨y, hy, hv⟩
    let x : Fin n → ℝ := fun i => y (e i)
    have he : renamePoint e x = y := by ext j; simp [renamePoint, x]
    refine ⟨x, (matches_feasible e source target witness h x).mp (by simpa [he] using hy), ?_⟩
    rw [← matches_objective e source target witness h x, he, hv]
  · rintro ⟨x, hx, hv⟩
    exact ⟨renamePoint e x, (matches_feasible e source target witness h x).mpr hx,
      (matches_objective e source target witness h x).trans hv⟩

end CertifiedMinlp.MasterIdentity
