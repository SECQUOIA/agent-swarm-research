import Formal.NetworkSimplex.ThresholdObservedCache

/-! Run compressed algorithms at the stored array dimension. Equality transports
are proof-only; no finite-set deduplication is executed to recover the dimension. -/
namespace NetworkSimplex.Chain.Threshold
variable {m a L : ℕ}

@[inline] def runSized {P R : ℕ → Type} (n : ℕ) (h : a = n)
    (run : ∀ n, RationalData n L → P n → R n × ℕ)
    (D : RationalData a L) (parameters : P a) : R a × ℕ :=
  let result := run n (h ▸ D) (h ▸ parameters)
  (h.symm ▸ result.1, result.2)

theorem runSized_eq {P R : ℕ → Type} (n : ℕ) (h : a = n)
    (run : ∀ n, RationalData n L → P n → R n × ℕ)
    (D : RationalData a L) (parameters : P a) :
    runSized n h run D parameters = run a D parameters := by cases h; rfl

@[inline] def runCachedSize {P R : ℕ → Type} (C : RationalData.ObservedCache m a L)
    (run : ∀ n, RationalData n L → P n → R n × ℕ) (parameters : P a) : R a × ℕ :=
  runSized C.labels.toArray.size C.labels.size_toArray.symm run C.data parameters

@[simp] theorem runCachedSize_eq {P R : ℕ → Type} (C : RationalData.ObservedCache m a L)
    (run : ∀ n, RationalData n L → P n → R n × ℕ) (parameters : P a) :
    runCachedSize C run parameters = run a C.data parameters :=
  runSized_eq _ _ _ _ _

end NetworkSimplex.Chain.Threshold
