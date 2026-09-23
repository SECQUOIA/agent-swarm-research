import Formal.Model

namespace ExactCounts

noncomputable section
variable {n p q : ℕ}

/-- The three exact scalar contacts used in the counting obstruction. -/
def contactInput (j : Fin 3) : ℝ := (j.val : ℝ) / 2

def contactInputs (s : Fin n → Fin 3) : Fin n → ℝ := fun i => contactInput (s i)

lemma contactInputs_domain (s : Fin n → Fin 3) : InDomain (contactInputs s) := by
  intro i
  have h := (s i).isLt
  dsimp [contactInputs, contactInput]
  constructor
  · positivity
  · have : ((s i).val : ℝ) ≤ 2 := by exact_mod_cast (show (s i).val ≤ 2 by omega)
    linarith

/-- Distinct scalar contacts cannot have both oriented third-points valid. -/
lemma contact_eq_of_thirds (j k : Fin 3)
    (h₁ : ValidPoint ((1 / 3 : ℝ) • graphPoint (contactInput j) +
      (2 / 3 : ℝ) • graphPoint (contactInput k)))
    (h₂ : ValidPoint ((2 / 3 : ℝ) • graphPoint (contactInput j) +
      (1 / 3 : ℝ) • graphPoint (contactInput k))) : j = k := by
  fin_cases j <;> fin_cases k <;> first
  | rfl
  | solve | norm_num [ValidPoint, graphPoint, contactInput, leftValue, rightValue,
      Pi.add_apply, Pi.smul_apply, smul_eq_mul, Matrix.cons_val_two] at h₁
  | solve | norm_num [ValidPoint, graphPoint, contactInput, leftValue, rightValue,
      Pi.add_apply, Pi.smul_apply, smul_eq_mul, Matrix.cons_val_two] at h₂

lemma contacts_eq_of_thirds (s t : Fin n → Fin 3)
    (h₁ : Valid ((1 / 3 : ℝ) • graph (contactInputs s) +
      (2 / 3 : ℝ) • graph (contactInputs t)))
    (h₂ : Valid ((2 / 3 : ℝ) • graph (contactInputs s) +
      (1 / 3 : ℝ) • graph (contactInputs t))) : s = t := by
  funext i
  exact contact_eq_of_thirds (s i) (t i) (h₁ i) (h₂ i)

lemma integer_third_codes (k l : Fin p → ℤ)
    (h : ∀ i, (k i : ZMod 3) = (l i : ZMod 3)) :
    (1 / 3 : ℝ) • (fun i => (k i : ℝ)) +
      (2 / 3 : ℝ) • (fun i => (l i : ℝ)) ∈ IntegerCodes p := by
  have hm (i) : k i % 3 = l i % 3 := (ZMod.intCast_eq_intCast_iff' _ _ 3).mp (h i)
  refine ⟨fun i => (k i + 2 * l i) / 3, ?_⟩
  funext i
  have hd : 3 ∣ k i + 2 * l i := by
    apply Int.dvd_of_emod_eq_zero
    have := hm i
    omega
  have he : (k i + 2 * l i) / 3 * 3 = k i + 2 * l i := Int.ediv_mul_cancel hd
  have hr := congrArg (fun z : ℤ => (z : ℝ)) he
  push_cast at hr
  dsimp
  linarith

/-- Every admissible convex integer lift needs at least one integer per input. -/
theorem integer_lower_bound (h : HasIntegerLift n p) : n ≤ p := by
  classical
  obtain ⟨q, C, hC, hcover, hvalid⟩ := h
  have hc (s : Fin n → Fin 3) := hcover (contactInputs s) (contactInputs_domain s)
  choose z hz a ha using hc
  choose k hk using hz
  have hinj : Function.Injective (fun s i => (k s i : ZMod 3)) := by
    intro s t he
    have hm : ∀ i, (k s i : ZMod 3) = (k t i : ZMod 3) := congrFun he
    have hc₁ := hC (ha s) (ha t) (by norm_num : (0 : ℝ) ≤ 1 / 3)
      (by norm_num : (0 : ℝ) ≤ 2 / 3) (by norm_num : (1 / 3 : ℝ) + 2 / 3 = 1)
    have hc₂ := hC (ha t) (ha s) (by norm_num : (0 : ℝ) ≤ 1 / 3)
      (by norm_num : (0 : ℝ) ≤ 2 / 3) (by norm_num : (1 / 3 : ℝ) + 2 / 3 = 1)
    have hv₁ := hvalid _ _ _ (by simpa [hk] using integer_third_codes (k s) (k t) hm) hc₁
    have hv₂ := hvalid _ _ _ (by
      simpa [hk] using integer_third_codes (k t) (k s) (fun i => (hm i).symm)) hc₂
    apply contacts_eq_of_thirds s t hv₁
    simpa [add_comm] using hv₂
  have hcard := Fintype.card_le_of_injective _ hinj
  have hp : 3 ^ n ≤ 3 ^ p := by simpa [Fintype.card_fun, ZMod.card] using hcard
  exact (Nat.pow_le_pow_iff_right (by decide : 1 < 3)).mp hp

/-- Every admissible convex binary lift needs enough codes for all ternary contacts. -/
theorem binary_lower_bound (h : HasBinaryLift n p) : 3 ^ n ≤ 2 ^ p := by
  classical
  obtain ⟨q, C, hC, hcover, hvalid⟩ := h
  have hc (s : Fin n → Fin 3) := hcover (contactInputs s) (contactInputs_domain s)
  choose z hz a ha using hc
  let code (s : Fin n → Fin 3) (i : Fin p) : Fin 2 := if z s i = 0 then 0 else 1
  have code_eq (s t : Fin n → Fin 3) (he : code s = code t) : z s = z t := by
    funext i
    have hi := congrFun he i
    have hs := hz s i
    have ht := hz t i
    rcases hs with hs | hs <;> rcases ht with ht | ht <;>
      simp_all [code]
  have hinj : Function.Injective code := by
    intro s t he
    have hez := code_eq s t he
    have hc₁ := hC (ha s) (ha t) (by norm_num : (0 : ℝ) ≤ 1 / 3)
      (by norm_num : (0 : ℝ) ≤ 2 / 3) (by norm_num : (1 / 3 : ℝ) + 2 / 3 = 1)
    have hc₂ := hC (ha t) (ha s) (by norm_num : (0 : ℝ) ≤ 1 / 3)
      (by norm_num : (0 : ℝ) ≤ 2 / 3) (by norm_num : (1 / 3 : ℝ) + 2 / 3 = 1)
    have hz₁ : (1 / 3 : ℝ) • z s + (2 / 3 : ℝ) • z t ∈ BinaryCodes p := by
      rw [hez, ← add_smul]
      norm_num
      exact hz t
    have hz₂ : (1 / 3 : ℝ) • z t + (2 / 3 : ℝ) • z s ∈ BinaryCodes p := by
      rw [hez, ← add_smul]
      norm_num
      exact hz t
    have hv₁ := hvalid _ _ _ hz₁ hc₁
    have hv₂ := hvalid _ _ _ hz₂ hc₂
    apply contacts_eq_of_thirds s t hv₁
    simpa [add_comm] using hv₂
  simpa [Fintype.card_fun] using Fintype.card_le_of_injective _ hinj

end
end ExactCounts
