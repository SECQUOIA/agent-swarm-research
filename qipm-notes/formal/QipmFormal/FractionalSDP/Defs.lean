import Mathlib

/-! Definitions for the trace-normalized fractional SDP spectrum.

The parameter `t` is the ratio of the objective gap to the positive (1,2)
entry. It makes the center rational and tends to zero with the gap.
-/

namespace QipmFormal.FractionalSDP

noncomputable section

def denom (t : ℝ) : ℝ := t ^ 2 + 2 * t + 3
def b (t : ℝ) : ℝ := t / denom t
def g (t : ℝ) : ℝ := t ^ 2 / denom t
def a (t : ℝ) : ℝ := (t + 3) / denom t
def q (t : ℝ) : ℝ := a t * g t - b t ^ 2
def mu (t : ℝ) : ℝ := q t / (1 - b t - 2 * g t)

def point (b g t e : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![1 - g - b, b, t; b, g, e; t, e, b]

def centerMatrix (t : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  point (b t) (g t) 0 0

def tangent (u v w z : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![-v-u, u, w; u, v, z; w, z, u]

def k00 (t : ℝ) : ℝ := (b t)⁻¹ ^ 2 + (-g t - 2 * b t) ^ 2 / q t ^ 2 + 2 / q t
def k01 (t : ℝ) : ℝ := (-g t - 2 * b t) * (1 - b t - 2 * g t) / q t ^ 2 + 1 / q t
def k11 (t : ℝ) : ℝ := (1 - b t - 2 * g t) ^ 2 / q t ^ 2 + 2 / q t

def diagTrace (t : ℝ) : ℝ := (2 * k00 t - 2 * k01 t + 4 * k11 t) / 7
def diagDet (t : ℝ) : ℝ := (k00 t * k11 t - k01 t ^ 2) / 7
def diagHigh (t : ℝ) : ℝ :=
  (diagTrace t + Real.sqrt (diagTrace t ^ 2 - 4 * diagDet t)) / 2
def diagLow (t : ℝ) : ℝ := diagDet t / diagHigh t

def aHigh (t : ℝ) : ℝ :=
  (a t + g t + Real.sqrt ((a t - g t) ^ 2 + 4 * b t ^ 2)) / 2
def offLow (t : ℝ) : ℝ := 1 / (b t * aHigh t)
def offHigh (t : ℝ) : ℝ := aHigh t / (b t * q t)

end
end QipmFormal.FractionalSDP
