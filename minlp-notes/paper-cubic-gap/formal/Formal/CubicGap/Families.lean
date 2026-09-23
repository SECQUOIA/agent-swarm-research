import Formal.CubicGap.Polynomial
import Formal.CubicGap.Counts
import Formal.CubicGap.Finite

namespace CubicGap

noncomputable section

/-- The two-group polynomial in the manuscript, on its actual coordinates. -/
def twoFamily (m : ℕ) (x : Fin 2 × Fin m → ℝ) : ℝ :=
  (∑ i, x (0,i)) * elementary 2 (fun i => x (1,i)) +
    (5 * (m : ℝ) / 4) * elementary 2 (fun i => x (0,i))

/-- The six support orbits of the three-group examples. -/
def threeFamily (m : ℕ) (coef : Fin 6 → ℚ) (x : Fin 3 × Fin m → ℝ) : ℝ :=
  (coef 0 : ℝ) * elementary 3 (fun i => x (2,i)) +
    (coef 1 : ℝ) * (∑ i, x (1,i)) * elementary 2 (fun i => x (2,i)) +
    (coef 2 : ℝ) * elementary 2 (fun i => x (1,i)) +
    (coef 3 : ℝ) * (∑ i, x (0,i)) * (∑ i, x (2,i)) +
    (coef 4 : ℝ) * (∑ i, x (0,i)) * (∑ i, x (1,i)) +
    (coef 5 : ℝ) * elementary 2 (fun i => x (0,i))

theorem elementary_coordinate_affine {I : Type*} [Fintype I] [DecidableEq I]
    (d : ℕ) (x : I → ℝ) (i : I) (t : ℝ) :
    elementary d (Function.update x i t) =
      (1-t) * elementary d (Function.update x i 0) +
      t * elementary d (Function.update x i 1) := by
  simpa [supportPolynomial, elementary, monomial] using
    supportPolynomial_coordinate_affine (Finset.univ.powersetCard d) (fun _ => 1) x i t

theorem sum_coordinate_affine {I : Type*} [Fintype I] [DecidableEq I]
    (x : I → ℝ) (i : I) (t : ℝ) :
    (∑ j, Function.update x i t j) =
      (1-t) * (∑ j, Function.update x i 0 j) +
      t * (∑ j, Function.update x i 1 j) := by
  simp only [Finset.sum_update_of_mem (Finset.mem_univ i)]
  ring

theorem twoFamily_binary (m : ℕ) (v : Fin 2 × Fin m → Bool) :
    twoFamily m (fun i => if v i = true then 1 else 0) =
      (twoValue m (count fun i => v (0,i)) (count fun i => v (1,i)) : ℝ) := by
  simp only [twoFamily, elementary_binary, sum_binary, twoValue]
  push_cast
  rfl

theorem threeFamily_binary (m : ℕ) (coef : Fin 6 → ℚ) (v : Fin 3 × Fin m → Bool) :
    threeFamily m coef (fun i => if v i = true then 1 else 0) =
      (countPhi coef (count fun i => v (0,i)) (count fun i => v (1,i))
        (count fun i => v (2,i)) : ℝ) := by
  simp only [threeFamily, elementary_binary, sum_binary, countPhi]
  push_cast
  rfl

theorem group_update_same {k m : ℕ} (x : Fin k × Fin m → ℝ)
    (g : Fin k) (i : Fin m) (t : ℝ) :
    (fun j => Function.update x (g,i) t (g,j)) =
      Function.update (fun j => x (g,j)) i t := by
  funext j
  by_cases h : j = i <;> simp [h]

theorem group_update_other {k m : ℕ} (x : Fin k × Fin m → ℝ)
    (g h : Fin k) (hne : h ≠ g) (i : Fin m) (t : ℝ) :
    (fun j => Function.update x (g,i) t (h,j)) = (fun j => x (h,j)) := by
  funext j
  simp [hne]

theorem twoFamily_coordinate_affine (m : ℕ) (x : Fin 2 × Fin m → ℝ)
    (i : Fin 2 × Fin m) (t : ℝ) :
    twoFamily m (Function.update x i t) =
      (1-t) * twoFamily m (Function.update x i 0) +
      t * twoFamily m (Function.update x i 1) := by
  rcases i with ⟨g,i⟩
  fin_cases g <;> norm_num only [Fin.zero_eta, Fin.mk_one] at *
  · simp only [twoFamily]
    simp_rw [group_update_same, group_update_other x 0 1 (by decide)]
    rw [sum_coordinate_affine _ i t, elementary_coordinate_affine 2 _ i t]
    ring
  · simp only [twoFamily]
    simp_rw [group_update_same, group_update_other x 1 0 (by decide)]
    rw [elementary_coordinate_affine 2 _ i t]
    ring

theorem threeFamily_coordinate_affine (m : ℕ) (coef : Fin 6 → ℚ)
    (x : Fin 3 × Fin m → ℝ) (i : Fin 3 × Fin m) (t : ℝ) :
    threeFamily m coef (Function.update x i t) =
      (1-t) * threeFamily m coef (Function.update x i 0) +
      t * threeFamily m coef (Function.update x i 1) := by
  rcases i with ⟨g,i⟩
  fin_cases g <;> norm_num only [Fin.zero_eta, Fin.mk_one] at *
  · simp only [threeFamily]
    simp_rw [group_update_same,
      group_update_other x 0 1 (by decide), group_update_other x 0 2 (by decide)]
    rw [sum_coordinate_affine _ i t, elementary_coordinate_affine 2 _ i t]
    ring
  · simp only [threeFamily]
    simp_rw [group_update_same,
      group_update_other x 1 0 (by decide), group_update_other x 1 2 (by decide)]
    rw [sum_coordinate_affine _ i t, elementary_coordinate_affine 2 _ i t]
    ring
  · change threeFamily m coef (Function.update x (2,i) t) =
      (1-t) * threeFamily m coef (Function.update x (2,i) 0) +
      t * threeFamily m coef (Function.update x (2,i) 1)
    simp only [threeFamily]
    simp_rw [group_update_same,
      group_update_other x 2 0 (by decide), group_update_other x 2 1 (by decide)]
    rw [sum_coordinate_affine _ i t, elementary_coordinate_affine 2 _ i t,
      elementary_coordinate_affine 3 _ i t]
    ring

end
end CubicGap
