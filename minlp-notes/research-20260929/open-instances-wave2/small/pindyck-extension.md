# pindyck: a rigorous global dual bound (extension of report.md, Section 7)

Date: 2026-09-30. Status: computational result with a proof sketch in this
file; the proof is carried out by `pindyck_global.py`. Independently
verified ([`../../reviews/pindyck-review.md`](../../reviews/pindyck-review.md);
independent rebuild of the whole certificate). The review's wording fixes
were applied by the root on 2026-09-30 (Section 8). All runs were single-threaded (`OMP_NUM_THREADS=1`) and short (the
final script takes about 20 s).

## 1. Result

| quantity | value (min form) |
|---|---|
| listed primal (MINLPLib p1) | −1170.486285 |
| best listed dual (SCIP) | −1437.941134 |
| **our rigorous dual bound** | **−1170.4862854360886163932** |
| objective of the exactly feasible point defined by p* | ≤ −1170.486285436088562087577 |
| gap | ≤ 5.44e-14 (≈ 5.43e-14; relative 4.6e-17) |

The instance is closed. Every feasible point of the OSIL model has objective
≥ −1170.4862854360886163932. The point p* is the price vector from
`logs/pindyck_primal.txt` (17-digit decimals, computed by `pindyck.py`), with
all other variables given by the model's recursion.

A consequence of the certificate (Section 3.7): the maximizer of J over the
feasible set is unique and lies within Euclidean distance 6.4e-13 of p*.

The earlier result in report.md Section 7 was concavity only on the box
p* ± 10 and no global bound. This file supersedes that "no global dual
bound" statement.

## 2. Idea in one paragraph

Given the prices p, every other variable is fixed, so the problem is
max J(p) over the feasible price set F (report.md, Section 7). J looks
strongly concave: at 3,000 sampled feasible points the largest Hessian
eigenvalue lies in [−0.1195, −0.1111]. Earlier attempts enclosed the Hessian
entry by entry over a box and failed, because intervals lose the correlation
between entries. The key step here is to write the Hessian as an explicit
function Ψ(θ) of per-period quantities θ_t: the supply-decay factor
E_t = exp(−K cs_{t−1}), the product (1.1 + 0.1 p_t)·E_t, exp(−K s_t), d_t,
p_t − 250/R_t, 1/R_t² and 1/R_t³. In these coordinates Ψ is close to affine. A first-order Taylor model of Ψ over a box Θ of θ values then
keeps the correlations. A small branch and bound on Θ (9 boxes) proves
Ψ ⪯ −0.001·I. Θ is made to contain θ(p) for every p in a polytope G ⊇ F.
Hence J is concave on G, and the tangent plane at the interior stationary
point p* bounds J on F.

## 3. The certificate, step by step

Notation (checked against the OSIL by exact string comparison, as in
`pindyck.py`), t = 1..16:

- td_t = 0.87 td_{t−1} − 0.13 p_t + c_t, with td_0 = 18;
- s_t = 0.75 s_{t−1} + exp(−K cs_t)(1.1 + 0.1 p_t), with cs_t = cs_{t−1} + s_t,
  s_0 = 6.5, cs_0 = 0 and K = 0.142857142857143·ln 1.02;
- d_t = td_t − s_t ≥ 0;
- R_t = R_{t−1} − d_t, with R_0 = 500;
- J(p) = Σ δ_t d_t (p_t − 250/R_t); the objective is −J.

Let α_t = td_t(0).

### 3.1 Reduction

Every feasible x of the OSIL model has prices p = (x1..x16) ∈ F, where
F = {p ≥ 0 : d_t(p) ≥ 0 for all t}, and objective −J(p). The supply equation
has exactly one root s_t for p ≥ 0, because its left side is strictly
increasing in s_t. So it suffices to bound J from above on F.

### 3.2 Step 1: bounds on cumulative supply over F

On F the following hold:

- s_t ≤ td_t;
- s_t = 0.75 s_{t−1} + (1.1 + 0.1 p_t) e_t with e_t = exp(−K cs_t);
- e_t ∈ [exp(−K·CSH_t), exp(−K·CSL_t)] whenever CSL_t ≤ cs_t ≤ CSH_t.

Starting from the valid bounds CSL = 0 and CSH_t = Σ_{j≤t} α_j (true because
s_j ≤ td_j ≤ α_j), the script repeatedly solves a linear program in (p, s):

- maximize and minimize Σ_{j≤t} s_j;
- subject to s_t ≤ td_t(p) and the two supply inequalities with e_t replaced
  by its lower or upper bound.

Every true point (p, s(p)) with p ∈ F is feasible for this LP, so each LP
value bounds cs_t on F. Six rounds give CSH_16 = 169.27.

### 3.3 Step 2: a polytope G ⊇ F

Set e_lo,t = exp(−K·CSH_t), rounded down. By induction, on F the supply
satisfies s_t ≥ ℓ_t(p) = 0.75^t·6.5 + Σ_{j≤t} 0.75^{t−j}(1.1 + 0.1 p_j) e_lo,j.
Combined with s_t ≤ td_t(p), this gives 16 linear inequalities W p ≤ γ, where:

- W is lower triangular and positive, with
  W_tj = 0.13·0.87^{t−j} + 0.1·0.75^{t−j} e_lo,j;
- W is rounded down and γ is rounded up.

Define G = {p ≥ 0 : W p ≤ γ}. Then F ⊆ G, G is convex, and
p_t ≤ γ_t/W_tt on G. These price bounds range from 57.4 (t = 1) to 126.2
(t = 16). The point p* lies in the interior of G: its smallest slack is 6.44,
checked in exact rationals.

### 3.4 Step 3: state ranges over G

This step uses only G, not d ≥ 0, so the bounds hold at every p ∈ G, feasible
or not. The LP variables are p, s, e_t = exp(−K cs_t) and z_t = p_t e_t. The
constraints are:

- W p ≤ γ;
- the supply equation s_t = 0.75 s_{t−1} + 1.1 e_t + 0.1 z_t (exact);
- five tangent lines below the convex function exp(−K cs_t) and one secant
  above it, on the current range of cs_t;
- the four McCormick inequalities for z_t = p_t e_t;
- finite bounds on every variable.

The line coefficients are floats whose validity on the range is proved in
interval arithmetic. If needed, a line's constant is shifted by the proved
deficit.

Seven rounds give cs_16 ∈ [71.1, 158.8] on G. Then 96 further LP bounds give
the ranges of s_t, d_t and R_t. For example, R_16 ∈ [192.5, 500.9] and
d_16 ∈ [−3.16, 23.48].

LP certificates: HiGHS only proposes dual multipliers. Each bound is
recomputed by weak duality in exact rational arithmetic (Python `Fraction`),
with finite bounds on all variables. For the s_t upper bounds, the certified
values exceed the LP values by at most 6e-15.

### 3.5 Step 4: the Hessian as an explicit function Ψ(θ)

Implicit differentiation of s = a + b·exp(−K s) and forward second-order
differentiation give ∇²J(p) = Ψ(θ(p)). Here θ collects seven quantities per
period (112 in total; E_1 ≡ 1):

- β_t = (1.1 + 0.1 p_t)·E_t, with E_t = exp(−K cs_{t−1});
- E_t itself;
- φ_t = exp(−K s_t);
- d_t;
- u_t = p_t − 250/R_t;
- 1/R_t² and 1/R_t³.

Ψ is explicit. It uses no s, cs, td or R values, only θ, and it needs no
implicit solve. Write e_t for the t-th unit vector, ι_t = 1/(1 + Kβ_tφ_t),
κ_t = φ_t ι_t, and G_t = ∇cs_{t−1}. The recursion is:

```
∇b   = 0.1 E_t e_t − K β_t G_t
∇²b  = β_t (K² G_t G_tᵀ − K ∇²cs_{t−1}) + 0.1 (e_t ∇Eᵀ + ∇E e_tᵀ),   ∇E = −K E_t G_t
∇s_t = 0.75 ι_t ∇s_{t−1} + κ_t ∇b
∇²s_t = 0.75 ι_t ∇²s_{t−1} + κ_t ∇²b − K κ_t (∇b ∇s_tᵀ + ∇s_t ∇bᵀ) + K² β_t κ_t ∇s_t ∇s_tᵀ
∇d_t = ∇td_t − ∇s_t,  ∇²d_t = −∇²s_t,  ∇R_t = ∇R_{t−1} − ∇d_t,  ∇²R_t = ∇²R_{t−1} − ∇²d_t
∇q_t = e_t + 250 R_t⁻² ∇R_t,   ∇²q_t = 250 (R_t⁻² ∇²R_t − 2 R_t⁻³ ∇R_t ∇R_tᵀ)
∇²J  = Σ_t δ_t (u_t ∇²d_t + d_t ∇²q_t + ∇d_t ∇q_tᵀ + ∇q_t ∇d_tᵀ)
```

Here ∇td_t = −0.13 Σ_{k≤t} 0.87^{t−k} e_k is exact. The box Θ is built from
the step 3 ranges by interval arithmetic:

- β_t ∈ [1.1·E_lo, (1.1 + 0.1·pmax_t)·E_hi];
- u_t ∈ [−250/R_lo, pmax_t − 250/R_hi];
- the other quantities similarly.

So θ(p) ∈ Θ for every p ∈ G. The quantities are treated as independent in Θ.
This is a relaxation, but a mild one: 200 random points of Θ (half of them
vertices), followed by two sweeps of coordinate ascent over vertices, found no
θ with λ_max(Ψ(θ)) above −0.1096.

### 3.6 Step 5: Ψ ⪯ −0.001·I on Θ

**Taylor models.** `tm1.py` implements first-order Taylor models
(c, a, r). Each one means: value ∈ c + a·ε ± r for ε ∈ [−1, 1]^112, with
c + a·ε evaluated exactly.

- All rounding errors of the double-precision operations are added to r.
- Products use the affine-arithmetic rule with the ε_k² refinement.
- The reciprocal in ι_t is replaced by a line plus an error δ. δ is proved
  from convexity with mpmath interval evaluations.
- Decimal constants are enclosed by the correctly rounded double ± 1 relative
  ulp.

**Test for one box.** The Taylor model gives
∇²J ∈ C + Σ_k ε_k A_k ± r entrywise. After exact symmetrization:

1. For each k, the script builds an interval enclosure of
   X_k = V|Λ|Vᵀ + e_k I. Here A_k ≈ VΛVᵀ is a floating eigendecomposition and
   e_k ≥ ‖A_k − VΛVᵀ‖_∞, computed in interval arithmetic. Then
   X_k ∓ A_k = V(|Λ| ∓ Λ)Vᵀ + (e_k I ∓ (A_k − VΛVᵀ)) ⪰ 0 exactly, for any real
   V. Hence Σ ε_k A_k ⪯ Σ X_k for |ε_k| ≤ 1.
2. ρ(r) is bounded above by the Collatz–Wielandt formula with upward
   rounding.
3. An interval LDLᵀ factorization without pivoting (outward-rounded `ia.NI`)
   of −C − ΣX_k − (ρ̄ + 0.001)I must have all pivots positive. This proves
   that the exact symmetric matrix is positive definite.

**Branch and bound.** At the root box the float estimate of the bound is
+0.0126, so the test fails. The linear part costs about 0.012 and the Taylor
remainder about 0.117. The script bisects the parameter with the largest
(root sensitivity × relative width). Eight bisections, on u_16, u_15 (twice),
β_13 (three times) and β_12 (twice), give 9 leaf boxes. All 9 pass the
rigorous test. The largest float estimate among them is −0.0049. This step
takes 15 s.

**Consequence.** ∇²J(p) ⪯ −0.001·I for every p ∈ G.

### 3.7 Step 6: the bound

At the decimal point p*, J(p*) and ∇J(p*) are enclosed with mpmath
intervals (40 digits). The implicit s_t comes from a verified interval
fixed-point inclusion, and the gradient is computed in forward mode. The
results are:

- J(p*) = 1170.486285436088562087577 to all printed digits (enclosure width
  4.9e-30);
- |∂J/∂p_t(p*)| ≤ 8.01e-17;
- min_t d_t(p*) = 5.437 and min_t R_t(p*) = 350.3, so the point is exactly
  feasible.

Take any p ∈ F. Then p ∈ G, and the segment [p*, p] lies in G. Taylor's
formula with integral remainder and ∇²J ⪯ −μI (μ = 0.001) give

  J(p) ≤ J(p*) + ∇J(p*)·(p − p*) − (μ/2)‖p − p*‖²
       ≤ J(p*) + Σ_t |∂_tJ(p*)|·max(p*_t, pmax_t − p*_t).

This is evaluated with outward rounding and gives the bound in Section 1. The
same inequality shows that J(p) ≥ J(p*) forces
‖p − p*‖ ≤ 2‖∇J(p*)‖/μ ≤ 6.4e-13. This gives the uniqueness statement. (The
review adds that this ball lies in F because p* is interior, and that its
own enclosure ‖∇J(p*)‖₂ ≤ 1.85e-16 gives radius ≤ 3.7e-13.)

## 4. Checks that are not part of the proof

These are floating-point checks, run to catch modelling or coding errors.

- **θ-ranges.** At 300 hit-and-run points of G, every θ(p) lies inside Θ.
  The largest Hessian eigenvalue among them is −0.112.
- **Ψ against a separate Hessian.** Ψ evaluated at θ(p*) agrees to 1.1e-16
  with an independent float forward-mode Hessian of J at p*. That float
  Hessian agrees to 3e-16 with 30-digit finite differences of a value-only
  simulation, at 3 random points of G. This last check was a one-off script
  in `/tmp`, not kept.
- **Taylor-model soundness.** At 300 random θ in Θ (half of them vertices),
  the root-box Taylor model contained the point value of Ψ. The largest
  |point − affine part| used 92% of the remainder, which suggests the
  remainder bound is not grossly pessimistic. One-off, not kept.
- **Interval LDLᵀ test.** It accepted 200/200 random positive definite
  16×16 matrices and rejected 200/200 matrices with λ_min = −1e-6. One-off,
  not kept.

## 5. What did not work

These were exploratory runs in `/tmp`, not kept. The numbers show why the
final design was needed.

- **Entrywise interval Hessian over the full price box.** Over the full
  price box [0, pmax], the λ_max(mid) + ρ(rad) test fails on the entrywise
  hull of sampled Hessians when corners are sampled (not part of the proof;
  the sampling script was not kept, and the review could not reproduce the
  figure −0.109 + 0.119 first given here: corner samples fail, uniform
  samples pass). report.md Section 7 certified the smaller box p* ± 10 with
  entrywise interval Hessians. Over the feasible set the sampled hull would
  pass (−0.114 + 0.053), but F is not known to be convex, so it cannot serve
  as the concavity region. The natural interval forward second-order
  computation, even with optimistic sampled state ranges, gives
  ρ(radius) = 0.19 against a margin of 0.11.
- **Taylor model in price space.** Over the box, the remainder has
  ρ = 0.37 against a margin of about 0.095. Restricting the Taylor-model
  ranges to G, with exact LP-dual range bounds, gives 0.23. The value-level
  remainders grow along the recursion (s_16 ± 6.7, cs_16 ± 38), because
  (1.1 + 0.1p)·exp(−K cs) is far from affine over G. Halving one price
  coordinate barely helps, since the remainder comes from all 16 coordinates
  together. Halving all of them would need 2^16 boxes.
- **θ-space model with 1/(1 + Kw_t) as its own parameter.** The root fails
  by +0.014. Tying it to β_t and φ_t improved this only slightly (+0.0126).
  The 9-box branch and bound was needed.
- **Not tried.**
  - Dynamic programming over the 4-D state (td, s, cs, R). A rigorous grid
    scheme accumulates about a Lipschitz constant times the cell width per
    stage over 16 stages. I did not expect it to get near 1e-6.
  - A Lagrangian over copied states. The report's argument applies: each
    block keeps a bilinear td_{t−1}·p_t term, so the block maxima sit at box
    corners.

  Both were unnecessary once the concavity certificate closed.

## 6. Assumptions and caveats

- **What rigor rests on:**
  - numpy elementwise + − × ÷ follow IEEE double round-to-nearest, and numpy
    sums obey the standard error bound γ_n for any summation order;
  - Python `float(str)` rounds to nearest; mpmath's `to_float` truncates
    toward zero (mpmath 1.3.0, per the review), and every conversion on a
    rigorous path is followed by a one-ulp outward step or has ample slack;
  - mpmath.iv (exp, log, arithmetic) is correct;
  - Python `Fraction` is exact.

  Two library routines are used only to make proposals: LAPACK
  eigendecompositions (eigenvectors V, Perron vector x) and HiGHS (dual
  multipliers). Everything they return is then checked as described above.
  The one BLAS product, N·x in the Collatz–Wielandt bound, uses an error
  allowance (128u relative) that holds for any summation order, with or
  without FMA. No libm exp or log result enters the proof.
- **Scope of the concavity statement.** It is proved on the polytope G,
  which contains F; it is not claimed on the whole box [0, pmax]. The
  0.001 margin is small next to the true eigenvalues (about −0.11), because
  the proof uses a relaxation (independent θ components) and first-order
  Taylor models.
- **Primal point.** The bound compares with the exact recursion at the
  decimal p*. The 30-digit point in `logs/pindyck_primal.txt` rounds the
  states and has row violation 8.3e-28 (report.md). The exact point with the
  same prices is feasible, which the step 6 interval run confirms.
- **Not checked.**
  - Literature and novelty: I did not search for prior global certificates
    of pindyck.
  - Whether the certificate survives other choices of the split heuristic
    or of μ. These affect only speed or success, not validity.

## 7. Files and commands

New files in `research-20260929/open-instances-wave2/small/`:

- `tm1.py`: first-order Taylor models with rigorous rounding, and the convex
  linearization used for reciprocals;
- `pindyck_global.py`: steps 1–6 and the float checks of Section 4 (the
  first two items);
- `logs/pindyck_global.log`: the output of the final run.

Command, from that directory (targeted only, single-threaded, about 20 s):

```
OMP_NUM_THREADS=1 python3 pindyck_global.py
```

Also run, not part of the proof: `python3 -m pyflakes pindyck_global.py tm1.py`
(clean), and the exploratory and check scripts in `/tmp/pind` described in
Sections 4–5, which were not kept. `pindyck.py` and report.md were not
modified. No project-wide checks were run and no CI was inspected.

## 8. Revision after review (root, 2026-09-30)

The review ([`../../reviews/pindyck-review.md`](../../reviews/pindyck-review.md),
verdict "verified") rebuilt the certificate with its own code and found a
bound 9.4e-20 tighter than the one claimed here. It raised five issues, none
affecting the bound. Each was checked against the review's logs before the
text was changed.

1. **Gap rounding.** The certified gap is 5.430553e-14, so "≤ 5.43e-14" was
   rounded the wrong way; Section 1 now says "≤ 5.44e-14 (≈ 5.43e-14)".
2. **Entrywise interval Hessians.** Section 5 no longer says that no
   entrywise-interval method over the price box can succeed. It states the
   narrower observation for corner sampling, says that the supporting
   figure could not be reproduced, and points to report.md Section 7, which
   certified the box p* ± 10 by this method.
3. **mpmath rounding.** Section 6 now says that mpmath's `to_float`
   truncates toward zero and why validity is unaffected.
4. **Uniqueness radius.** Section 3.7 adds the review's remark that the ball
   lies in F and its tighter radius (≤ 3.7e-13, from
   `reviews/pindyck-review-checks/logs/primal_check.txt`).
5. **Not applied: script side effect.** `pindyck_global.py` still overwrites
   `logs/pindyck_global.log` when rerun; changing the script was outside
   this root pass. The review restored the original log after its rerun.

The header now records the review, and the Section 6 item "Independent
review. The root's verifier has not rerun this." is removed.
