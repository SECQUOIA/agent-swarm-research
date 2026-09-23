import Formal.QuadraticPrecision.SquareConstruction
import Formal.QuadraticPrecision.Model
import Formal.QuadraticPrecision.LinearSystem

noncomputable section
namespace QuadraticPrecision

abbrev SquareAmbient (L : ℕ) := LiftPoint 1 L (2 + (L + L))

def squareInput (L : ℕ) : SquareAmbient L →ₗ[ℝ] ℝ :=
  (LinearMap.proj 0).comp (LinearMap.fst ℝ _ _)
def squareOutput (L : ℕ) : SquareAmbient L →ₗ[ℝ] ℝ :=
  (LinearMap.fst ℝ _ _).comp (LinearMap.snd ℝ _ _)
def squareAux (L : ℕ) (i : Fin (2 + (L + L))) : SquareAmbient L →ₗ[ℝ] ℝ :=
  (LinearMap.proj i).comp ((LinearMap.fst ℝ _ _).comp
    ((LinearMap.snd ℝ _ _).comp (LinearMap.snd ℝ _ _)))
def squareBit (L : ℕ) (i : Fin L) : SquareAmbient L →ₗ[ℝ] ℝ :=
  (LinearMap.proj i).comp ((LinearMap.snd ℝ _ _).comp
    ((LinearMap.snd ℝ _ _).comp (LinearMap.snd ℝ _ _)))
def squareR (L : ℕ) := squareAux L ((0 : Fin 2).castAdd (L + L))
def squareQ (L : ℕ) := squareAux L ((1 : Fin 2).castAdd (L + L))
def squareV (L : ℕ) (i : Fin L) := squareAux L ((i.castAdd L).natAdd 2)
def squareT (L : ℕ) (i : Fin L) := squareAux L ((i.natAdd L).natAdd 2)

def squareAffinePrefix {V : Type*} [AddCommGroup V] [Module ℝ V] :
    (L : ℕ) → (Fin L → V →ᵃ[ℝ] ℝ) → V →ᵃ[ℝ] ℝ
  | 0, _ => 0
  | L+1, b => (1/2:ℝ) • b 0 + (1/2:ℝ) • squareAffinePrefix L (fun i => b i.succ)

@[simp] theorem squareAffinePrefix_apply {V : Type*} [AddCommGroup V] [Module ℝ V]
    (L : ℕ) (b : Fin L → V →ᵃ[ℝ] ℝ) (x : V) :
    squareAffinePrefix L b x = squarePrefix L (fun i => b i x) := by
  induction L with
  | zero => rfl
  | succ L ih => simp [squareAffinePrefix, squarePrefix, ih, div_eq_mul_inv, mul_comm]

def squareBaseRows (L : ℕ) (hypo : Bool) : Fin 11 → SquareAmbient L →ᵃ[ℝ] ℝ :=
  let y := (squareInput L).toAffineMap
  let w := (squareOutput L).toAffineMap
  let r := (squareR L).toAffineMap
  let q := (squareQ L).toAffineMap
  let a := squareAffinePrefix L (fun i => (squareBit L i).toAffineMap)
  let v := squareAffinePrefix L (fun i => (squareV L i).toAffineMap)
  let t := squareAffinePrefix L (fun i => (squareT L i).toAffineMap)
  let c := fun z => AffineMap.const ℝ (SquareAmbient L) z
  ![-y, y-c 1, -r, r-c (squareWidth L), y-a-r, a+r-y,
    if hypo then 0 else -q,
    if hypo then 0 else (2*squareWidth L) • r-c ((squareWidth L)^2)-q,
    q-squareWidth L • r, w-v-t-q, v+t+q-w]

def squareDigitRows (L : ℕ) (i : Fin L) : Fin 10 → SquareAmbient L →ᵃ[ℝ] ℝ :=
  let y := (squareInput L).toAffineMap
  let r := (squareR L).toAffineMap
  let b := (squareBit L i).toAffineMap
  let v := (squareV L i).toAffineMap
  let t := (squareT L i).toAffineMap
  let c := fun z => AffineMap.const ℝ (SquareAmbient L) z
  ![-b,b-c 1,-v,v-b,v-y,y-c 1+b-v,
    -t,t-squareWidth L • b,t-r,r-c (squareWidth L)+squareWidth L • b-t]

def squareSystem (L : ℕ) (hypo : Bool) : LinearSystem (SquareAmbient L) where
  rowCount := 11+L*10
  row := Fin.addCases (squareBaseRows L hypo)
    (fun k => squareDigitRows L (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2)

theorem squareSystem_feasible (L : ℕ) (hypo : Bool) (x : SquareAmbient L) :
    x ∈ (squareSystem L hypo).feasible ↔
    (∀ i, 0 ≤ squareBit L i x ∧ squareBit L i x ≤ 1) ∧
    (if hypo then SquareHypographRows L (squareInput L x) (squareOutput L x)
      (squareR L x) (squareQ L x) (fun i => squareBit L i x)
      (fun i => squareV L i x) (fun i => squareT L i x)
    else SquareRows L (squareInput L x) (squareOutput L x)
      (squareR L x) (squareQ L x) (fun i => squareBit L i x)
      (fun i => squareV L i x) (fun i => squareT L i x)) := by
  have hall : (∀ k : Fin (L*10),
      squareDigitRows L (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2 x ≤ 0) ↔
      ∀ i : Fin L, ∀ j : Fin 10, squareDigitRows L i j x ≤ 0 := by
    constructor
    · intro h i j; simpa using h (finProdFinEquiv (i,j))
    · intro h k; exact h _ _
  change (∀ k, (squareSystem L hypo).row k x ≤ 0) ↔ _
  simp only [squareSystem, Fin.forall_fin_add, Fin.addCases_left, Fin.addCases_right]
  rw [hall]
  cases hypo <;>
    simp only [squareBaseRows, Bool.false_eq_true, reduceIte, Fin.forall_fin_succ, Fin.isValue,
      Matrix.cons_val_zero, AffineMap.coe_neg, LinearMap.coe_toAffineMap, Pi.neg_apply,
      Left.neg_nonpos_iff, Matrix.cons_val_succ, AffineMap.coe_sub, AffineMap.coe_const,
      Function.const_one, Pi.sub_apply, Pi.one_apply, tsub_le_iff_right, zero_add,
      Function.const_apply, squareAffinePrefix_apply, AffineMap.coe_add, Pi.add_apply,
      AffineMap.coe_smul, Pi.smul_apply, smul_eq_mul, Matrix.cons_val_fin_one, forall_const,
      squareDigitRows, SquareRows, Set.mem_Icc, BinaryProductRows, one_mul, SquareTriangle,
      AffineMap.coe_zero, Pi.zero_apply, le_refl, true_and, SquareHypographRows] <;>
    constructor
  · rintro ⟨⟨hy0,hy1,hr0,hr1,he0,he1,hq0,hq1,hq2,hw0,hw1⟩,hd⟩
    refine ⟨fun i => ⟨(hd i).1,(hd i).2.1⟩, ⟨hy0,hy1⟩, ⟨hr0,hr1⟩,
      by linarith, ?_, ?_, ⟨hq0,hq1,hq2⟩, by linarith⟩
    · intro i
      rcases hd i with ⟨_,_,hv0,hv1,hv2,hv3,_⟩
      exact ⟨hv0,hv1,hv2,by linarith⟩
    · intro i
      rcases hd i with ⟨_,_,_,_,_,_,ht0,ht1,ht2,ht3⟩
      exact ⟨ht0,ht1,ht2,by nlinarith⟩
  · rintro ⟨hb,⟨hy0,hy1⟩,⟨hr0,hr1⟩,he,hv,ht,⟨hq0,hq1,hq2⟩,hw⟩
    refine ⟨⟨hy0,hy1,hr0,hr1,by linarith,by linarith,hq0,hq1,hq2,
      by linarith,by linarith⟩, ?_⟩
    intro i
    rcases hv i with ⟨hv0,hv1,hv2,hv3⟩
    rcases ht i with ⟨ht0,ht1,ht2,ht3⟩
    exact ⟨(hb i).1,(hb i).2,hv0,hv1,hv2,by linarith,ht0,ht1,ht2,by nlinarith⟩
  · rintro ⟨⟨hy0,hy1,hr0,hr1,he0,he1,hq2,hw0,hw1⟩,hd⟩
    refine ⟨fun i => ⟨(hd i).1,(hd i).2.1⟩, ⟨hy0,hy1⟩, ⟨hr0,hr1⟩,
      by linarith, ?_, ?_, hq2, by linarith⟩
    · intro i
      rcases hd i with ⟨_,_,hv0,hv1,hv2,hv3,_⟩
      exact ⟨hv0,hv1,hv2,by linarith⟩
    · intro i
      rcases hd i with ⟨_,_,_,_,_,_,ht0,ht1,ht2,ht3⟩
      exact ⟨ht0,ht1,ht2,by nlinarith⟩
  · rintro ⟨hb,⟨hy0,hy1⟩,⟨hr0,hr1⟩,he,hv,ht,hq2,hw⟩
    refine ⟨⟨hy0,hy1,hr0,hr1,by linarith,by linarith,hq2,
      by linarith,by linarith⟩, ?_⟩
    intro i
    rcases hv i with ⟨hv0,hv1,hv2,hv3⟩
    rcases ht i with ⟨ht0,ht1,ht2,ht3⟩
    exact ⟨(hb i).1,(hb i).2,hv0,hv1,hv2,by linarith,ht0,ht1,ht2,by nlinarith⟩

end QuadraticPrecision
