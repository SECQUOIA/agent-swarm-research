import Formal.QuadraticPrecision.SquarePrefix

noncomputable section
namespace QuadraticPrecision

/-- Square constraints with `L` bits, `2*L+2` continuous auxiliaries, and
`8*L+11` affine inequality rows (each equality counts twice). `SquareSystem`
adds two explicit code-bound rows per bit, for `10*L+11` rows in the lift. -/
def SquareRows (L : ℕ) (y w r q : ℝ) (b v t : Fin L → ℝ) : Prop :=
  y ∈ Set.Icc 0 1 ∧ r ∈ Set.Icc 0 (squareWidth L) ∧
  y = squarePrefix L b + r ∧
  (∀ i, BinaryProductRows 1 (b i) y (v i)) ∧
  (∀ i, BinaryProductRows (squareWidth L) (b i) r (t i)) ∧
  SquareTriangle (squareWidth L) r q ∧
  w = squarePrefix L v + squarePrefix L t + q

/-- Projection with exactly `L` binary coordinates. -/
def SquareRelaxation (L : ℕ) (y w : ℝ) : Prop :=
  ∃ b v t : Fin L → ℝ, ∃ r q : ℝ, BinaryDigits b ∧ SquareRows L y w r q b v t

theorem squareRows_identity {L : ℕ} {y w r q : ℝ} {b v t : Fin L → ℝ}
    (hb : BinaryDigits b) (h : SquareRows L y w r q b v t) : w-y^2=q-r^2 := by
  rcases h with ⟨hy,hr,he,hv,ht,hq,hw⟩
  have ev : v = fun i => b i*y := funext fun i => binaryProductRows_exact (hb i) (hv i)
  have et : t = fun i => b i*r := funext fun i => binaryProductRows_exact (hb i) (ht i)
  rw [ev, et, squarePrefix_mul, squarePrefix_mul] at hw
  rw [he] at *
  nlinarith

theorem squareRelaxation_contains_graph (L : ℕ) (y : ℝ) (hy : y ∈ Set.Icc (0 : ℝ) 1) :
    SquareRelaxation L y (y ^ 2) := by
  obtain ⟨b,r,hb,hr,he⟩ := exists_squarePrefix L y hy
  refine ⟨b, (fun i => b i*y), (fun i => b i*r), r, r^2, hb, hy, hr, he,
    (fun i => binaryProductRows_graph (hb i) hy),
    (fun i => binaryProductRows_graph (hb i) hr), squareTriangle_graph hr, ?_⟩
  rw [squarePrefix_mul, squarePrefix_mul]
  rw [he] at *
  nlinarith

theorem squareRelaxation_error {L : ℕ} {y w : ℝ} (h : SquareRelaxation L y w) :
    y ∈ Set.Icc (0 : ℝ) 1 ∧ |w-y^2| ≤ (squareWidth L)^2/4 := by
  obtain ⟨b,v,t,r,q,hb,h⟩ := h
  refine ⟨h.1, ?_⟩
  rw [squareRows_identity hb h]
  exact squareTriangle_error h.2.1 h.2.2.2.2.2.1

@[simp] theorem squarePrefix_all_zero (L : ℕ) : squarePrefix L (fun _ => 0) = 0 := by
  induction L with
  | zero => rfl
  | succ L ih => simp [squarePrefix, ih]

theorem squareRelaxation_attains (L : ℕ) :
    SquareRelaxation L (squareWidth L/2) ((squareWidth L)^2/2) ∧
    (squareWidth L)^2/2 - (squareWidth L/2)^2 = (squareWidth L)^2/4 := by
  have hp := squareWidth_pos L
  have hu := squareWidth_le_one L
  constructor
  · refine ⟨(fun _ => 0), (fun _ => 0), (fun _ => 0), squareWidth L/2,
      (squareWidth L)^2/2, (fun _ => Or.inl rfl), ?_⟩
    refine ⟨⟨by positivity, by linarith⟩, ⟨by positivity, by linarith⟩,
      by simp, ?_, ?_, ?_, by simp⟩
    · intro i
      simpa using binaryProductRows_graph (b := (0 : ℝ)) (U:=1) (u:=squareWidth L/2) (Or.inl rfl)
        ⟨by positivity, by linarith⟩
    · intro i
      simpa using binaryProductRows_graph (b := (0 : ℝ)) (U:=squareWidth L) (u:=squareWidth L/2)
        (Or.inl rfl) ⟨by positivity, by linarith⟩
    · unfold SquareTriangle
      constructor
      · positivity
      constructor <;> nlinarith [sq_nonneg (squareWidth L)]
  · ring

/-- Dropping the two lower triangle rows gives an unbounded hypograph relaxation. -/
def SquareHypographRows (L : ℕ) (y w r q : ℝ) (b v t : Fin L → ℝ) : Prop :=
  y ∈ Set.Icc 0 1 ∧ r ∈ Set.Icc 0 (squareWidth L) ∧
  y = squarePrefix L b + r ∧
  (∀ i, BinaryProductRows 1 (b i) y (v i)) ∧
  (∀ i, BinaryProductRows (squareWidth L) (b i) r (t i)) ∧
  q ≤ squareWidth L*r ∧ w = squarePrefix L v + squarePrefix L t + q

def SquareHypographRelaxation (L : ℕ) (y w : ℝ) : Prop :=
  ∃ b v t : Fin L → ℝ, ∃ r q : ℝ, BinaryDigits b ∧ SquareHypographRows L y w r q b v t

theorem squareHypograph_contains {L : ℕ} {y w : ℝ} (hy : y ∈ Set.Icc (0 : ℝ) 1)
    (hw : w ≤ y ^ 2) : SquareHypographRelaxation L y w := by
  obtain ⟨b,r,hb,hr,he⟩ := exists_squarePrefix L y hy
  refine ⟨b, (fun i => b i*y), (fun i => b i*r), r, w-y^2+r^2, hb,
    hy, hr, he, (fun i => binaryProductRows_graph (hb i) hy),
    (fun i => binaryProductRows_graph (hb i) hr), ?_, ?_⟩
  · have := (squareTriangle_graph hr).2.2; linarith
  · rw [squarePrefix_mul, squarePrefix_mul, he]; ring

theorem squareHypograph_error {L : ℕ} {y w : ℝ} (h : SquareHypographRelaxation L y w) :
    y ∈ Set.Icc (0 : ℝ) 1 ∧ w ≤ y^2 + (squareWidth L)^2/4 := by
  obtain ⟨b,v,t,r,q,hb,hy,hr,he,hv,ht,hq,hw⟩ := h
  have ev : v = fun i => b i*y := funext fun i => binaryProductRows_exact (hb i) (hv i)
  have et : t = fun i => b i*r := funext fun i => binaryProductRows_exact (hb i) (ht i)
  rw [ev,et,squarePrefix_mul,squarePrefix_mul] at hw
  refine ⟨hy, ?_⟩
  have hid : w-y^2=q-r^2 := by rw [he] at hw ⊢; nlinarith
  nlinarith [sq_nonneg (r-squareWidth L/2)]

end QuadraticPrecision
