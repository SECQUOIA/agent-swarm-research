import CertifiedMinlp.Coordinates

/-! Finite-dimensional support correction, with rational certificate data. -/
namespace CertifiedMinlp
open scoped BigOperators

variable {ι : Type*} [Fintype ι]

def dot (a x : ι → ℝ) : ℝ := ∑ j, a j * x j

def affine (a : ι → ℝ) (b : ℝ) (x : ι → ℝ) : ℝ := dot a x + b

def boxContains (B : ι → Coordinate) (x : ι → ℝ) : Prop :=
  ∀ j, (B j).contains (x j)

/-- Algebraic composition: the premises are a support inequality, an intercept
bound, and coordinate shift bounds, rather than the desired underestimator. -/
theorem safe_affine_of_shift_bounds
    (g : (ι → ℝ) → ℝ) (q a p z x W : ι → ℝ) (c b : ℝ)
    (hsupport : g z + dot p (fun j => x j - z j) ≤ g x)
    (hshift : ∀ j, (p j + q j - a j) * (z j - x j) ≤ W j)
    (hb : b ≤ g z + dot q z + c - dot a z - ∑ j, W j) :
    affine a b x ≤ g x + dot q x + c := by
  have hsum := Finset.sum_le_sum (s := Finset.univ) (fun j _ => hshift j)
  have hid :
      (∑ j, (p j + q j - a j) * (z j - x j)) =
        dot p z - dot p x + dot q z - dot q x - dot a z + dot a x := by
    simp only [dot, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    ring
  have hp : dot p (fun j => x j - z j) = dot p x - dot p z := by
    simp only [dot, mul_sub, Finset.sum_sub_distrib]
  rw [hid] at hsum
  rw [hp] at hsupport
  unfold affine
  linarith

/-- The rational test in the manuscript's enclosure table, summed over any
finite set of coordinates. Values and true support slopes remain real. -/
theorem rational_enclosure_cut
    (B : ι → Coordinate) (g : (ι → ℝ) → ℝ)
    (q a z lo hi : ι → ℚ) (p : ι → ℝ) (c b v : ℚ)
    (hz : boxContains B (fun j => (z j : ℝ)))
    (hsupport : ∀ x, boxContains B x →
      g (fun j => (z j : ℝ)) + dot p (fun j => x j - (z j : ℝ)) ≤ g x)
    (ha : ∀ j, (B j).accepts (lo j) (hi j))
    (hlo : ∀ j, (lo j : ℝ) ≤ p j + (q j : ℝ) - (a j : ℝ))
    (hhi : ∀ j, p j + (q j : ℝ) - (a j : ℝ) ≤ (hi j : ℝ))
    (hv : (v : ℝ) ≤ g (fun j => (z j : ℝ)) +
      dot (fun j => (q j : ℝ)) (fun j => (z j : ℝ)) + (c : ℝ) -
      dot (fun j => (a j : ℝ)) (fun j => (z j : ℝ)))
    (hb : b ≤ v - ∑ j, (B j).correction (z j) (lo j) (hi j)) :
    ∀ x, boxContains B x →
      affine (fun j => (a j : ℝ)) b x ≤ g x + dot (fun j => (q j : ℝ)) x + c := by
  intro x hx
  apply safe_affine_of_shift_bounds g (fun j => (q j : ℝ))
    (fun j => (a j : ℝ)) p (fun j => (z j : ℝ)) x
    (fun j => ((B j).correction (z j) (lo j) (hi j) : ℝ)) c b (hsupport x hx)
  · intro j
    exact coordinate_correction_sound (B j) (z j) (lo j) (hi j) (x j)
      (p j + (q j : ℝ) - (a j : ℝ)) (hz j) (hx j) (ha j) (hlo j) (hhi j)
  · have hb' : (b : ℝ) ≤ (v : ℝ) -
        ∑ j, ((B j).correction (z j) (lo j) (hi j) : ℝ) := by
      exact_mod_cast hb
    linarith

omit [Fintype ι] in
theorem cut_valid_of_underestimator (r cut : (ι → ℝ) → ℝ)
    (B : Set (ι → ℝ)) (hcut : ∀ x ∈ B, cut x ≤ r x) :
    ∀ x ∈ B, r x ≤ 0 → cut x ≤ 0 := by
  intro x hx hr
  exact le_trans (hcut x hx) hr

end CertifiedMinlp
