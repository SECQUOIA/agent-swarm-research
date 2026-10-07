# Review: pindyck global dual bound (`open-instances-wave2/small/pindyck-extension.md`)

Date: 2026-09-30. I am an independent, adversarial reviewer; I did not write the extension,
`pindyck_global.py` or `tm1.py`.

Scope:

- recompute the new bound with my own code;
- check every step of the validity argument, both on paper and in the author's code;
- re-evaluate the primal point.

My scripts and logs are in [`pindyck-review-checks/`](pindyck-review-checks/). Following
`AGENTS.md`, I ran only targeted checks. I ran no project-wide verification and did not
look at CI status or logs. All runs were single-threaded (`OMP_NUM_THREADS=1`) and under
`timeout`. The longest run, my branch and bound, took 5 minutes.

## Verdict

**Verified.** The bound holds. I rebuilt the whole certificate with my own code: model
reader, LP range bounds, Hessian map, affine arithmetic, exact matrix test, branch and bound,
and interval evaluation at p*. I found a different partition of the parameter box, and every
leaf passed an exact rational test. The bound from my own pieces is

  every feasible point has objective ≥ −1170.4862854360886163931058729 (rounded down).

This is 9.4e-20 *above* (tighter than) the claimed −1170.4862854360886163932. So the claimed
bound follows from my computation. The primal claim also holds: the objective at the exactly
feasible point defined by p* is −1170.486285436088562087577425069…, which is
≤ −1170.486285436088562087577. The instance is closed.

I also reran the author's certificate data through my code. All 9 of the author's leaf boxes
pass my exact test, and my float estimates match the author's to 5 digits.

Issues (Section 8). None of them affects the bound. Two statements need a wording fix:

1. **"gap ≤ 5.43e-14" is rounded the wrong way.** The certified gap is 5.43055e-14, and
   the difference between the two printed numbers is 5.43056e-14. Write "gap ≤ 5.44e-14"
   or "gap ≈ 5.43e-14".
2. **Overclaim in the claims list:** "Entrywise interval Hessians over any price box cannot
   succeed". report.md Section 7 itself certified the box p* ± 10 with entrywise interval
   Hessians. The supporting number also depends on how the samples are drawn: with uniform
   samples over [0, pmax], the sampled hull *passes* the same test.
3. Minor documentation and presentation points: mpmath's float conversion truncates rather
   than rounding to nearest (harmless); the uniqueness argument needs one more sentence;
   running the script overwrites its stored log.

## 1. Model read independently (`own_osil.py`, `own_model.py`)

- I wrote my own OSIL reader with ElementTree. It expands the `mult`/`incr` arrays itself
  and keeps decimal strings exact. It shares no code with `osilx.py` or `ev.py`.
- Row by row, I asserted the same structure the report states:
  - demand: td_t = .87 td_{t−1} − .13 p_t + c_t;
  - supply: s_t = .75 s_{t−1} + 1.02^(−.142857142857143·cs_t)(1.1 + .1 p_t);
  - cs_t = cs_{t−1} + s_t, d_t = td_t − s_t, R_t = R_{t−1} − d_t;
  - x_{100+t} = (p_t − 250/R_t)·d_t;
  - objective: min −Σ δ_t x_{100+t}.
- Bounds: td_0 = 18, s_0 = 6.5, cs_0 = 0 (x51 has ub = 0) and R_0 = 500. x101..x116 are free
  and every other variable is ≥ 0. All variables are continuous.
- K = .142857142857143·ln 1.02 exactly (the decimal, not 1/7). δ_t are the 15-digit decimals
  from the OSIL, not 1.05^(−t+1). Both codes use the exact strings.
- Reduction (report Section 3.1): the supply equation is s − a − b·e^(−Ks) = 0 with
  b = (1.1 + .1p_t)e^(−K cs_{t−1}) > 0. Its left side has derivative 1 + Kb e^(−Ks) > 0, so it
  has exactly one root, and the root is positive. Given p, every variable is therefore
  determined, and the objective is −J(p). F = {p ≥ 0 : d(p) ≥ 0} drops the other sign
  constraints, so it contains the projection of the OSIL feasible set. That is the correct
  direction for a bound.

## 2. Primal point (`primal_check.py`, `logs/primal_check.txt`)

- I built the full 116-vector from the 17-digit prices in `logs/pindyck_primal.txt` by the
  exact recursion at 60 digits. My own tree evaluator gives:
  - max row residual 1.2e-60 and no bound violation;
  - objective −1170.486285436088562087577425069288…;
  - min d_t = 5.4373, min R_t = 350.32 and min td_t = 13.99.
- The stored 30-digit state vector has row residual 8.3e-28, as report.md says.
- Rigorous enclosure (mpmath.iv, 50 digits, own forward mode). Each s_t is enclosed by an
  interval Newton step N(X) ⊂ int X, which proves a unique root in X.
  - J(p*) is enclosed with width 1.4e-46.
  - max_t |∂J/∂p_t(p*)| ≤ 8.008e-17 (report: 8.01e-17) and ‖∇J(p*)‖₂ ≤ 1.844e-16.
  - The lower ends of d_t and R_t are positive, so the point is exactly feasible.

## 3. Hessian identity ∇²J(p) = Ψ(θ(p)) (`own_psi.py`, `hess_check.py`)

**Derivation.** I derived the second-order recursion myself; it matches report Section 3.5.
Differentiating (1 + Kbφ)∇s = ∇a + φ∇b once more gives

  ∇²s = ι∇²a + κ∇²b − Kκ(∇b∇sᵀ + ∇s∇bᵀ) + K²bκ ∇s∇sᵀ,

where φ = e^(−Ks), ι = 1/(1 + Kbφ) and κ = φι. The other steps are:

- ∇b = .1E e_t − Kβ∇cs_{t−1} and ∇²b = β(K²∇cs∇csᵀ − K∇²cs) − .1KE(e_t∇csᵀ + ∇cs e_tᵀ);
- ∇q = e_t + 250R⁻²∇R and ∇²q = 250(R⁻²∇²R − 2R⁻³∇R∇Rᵀ);
- ∇²J = Σδ_t(u_t∇²d_t + d_t∇²q_t + ∇d∇qᵀ + ∇q∇dᵀ).

This uses only θ_t = (β_t, E_t, φ_t, d_t, u_t, R_t⁻², R_t⁻³), as claimed.

**Numerical check (not part of the proof).** I used 12 points of G:

- p*;
- 6 LP vertices of G in random directions, where d_t reaches −1.19;
- 4 hit-and-run points;
- the maximizer of p15 + p16 over G, where d_t reaches −2.70.

At each point I compared a 50-digit finite-difference Hessian of my own value-only simulation
with two maps:

| compared with the finite-difference Hessian | largest difference |
|---|---|
| my Ψ | 1.7e-16 |
| the author's `psi_tm` (centre at a degenerate box) | 2.2e-16 |

λ_max ranged from −0.1189 to −0.1132. At all 12 points, θ(p) lay inside my Θ′ and inside the
author's Θ.

## 4. G ⊇ F and the parameter box (`own_ranges.py`, `logs/own_ranges*.log`)

My own code, same ideas, independent implementation. HiGHS only proposes duals. Every bound
is recomputed by weak duality in exact `Fraction` arithmetic, with finite variable bounds that
are themselves valid. For step 3 I used globally valid tangent lines of e^(−Kx): I checked the
closed-form minimum (−b/K)(1 − ln(−b/K)) − a ≥ 0 in interval arithmetic. The secants are
checked at their end points.

- **Step 1′ (F).** CSH_16 = 169.2729, the same as the author's 169.273 (relative difference
  ≤ 5.5e-10; the author's floats are rounded up). pmax runs from 57.413 to 126.155, and the
  slack of p* is 6.4376. Both match the log.
- **The author's G contains F.** The author's W is entrywise ≤ my exact W′, and the author's
  γ is ≥ my exact γ′. Since p ≥ 0, W p ≤ W′p ≤ γ′ ≤ γ on F.
- **Step 3′ (ranges over G).** I ran this on my G′ and again on the author's G:
  - cs_16 ∈ [71.137, 158.791];
  - R_16 ∈ [192.52, 500.90];
  - d_16 ∈ [−3.156, 23.48].

  These match the log.
- **Θ.** My rigorous ranges over the author's G lie inside the author's Θ except in two
  entries, where mine are looser by ≤ 5.4e-16: the upper end of E_12 and the lower end of
  d_2. This comes from the different LP relaxations and dual roundings, not from an error.
  To avoid depending on it, my concavity proof uses the *hull* of the author's Θ, my Θ′ over
  G′, and my Θ″ over the author's G.

## 5. Concavity certificate, recomputed (`own_psi.py`, `own_concavity.py`, `verify_own_leaves.py`)

**Affine arithmetic.** My implementation differs from `tm1.py`:

- every coefficient is an *interval*;
- every float operation is rounded outward with `nextafter`;
- sums use pairwise outward-rounded additions.

So no rounding-error analysis (γ_n, `upb`) is needed. The product uses the standard rule with
the ε_k² refinement. I checked the remainder bound Sx·Sy − ½Σ mx_k my_k by a monotonicity
argument that also holds for interval coefficients.

1/(1 + w) is replaced by αw + [h_min, h_max], where:

- h = 1/(1 + w) − αw;
- h_max is the larger of the interval values at the two end points (h is convex);
- h_min = 2√(−α) + α is the global minimum over w > −1, by AM–GM.

**Matrix test, all in exact rationals.** Let C, A_k and R be the mid-points and the enclosing
remainder. The upper triangle is mirrored, because the true Ψ is symmetric.

- X_k = V|Λ|Vᵀ + e_k I, with the float eigendecomposition turned exact through scaled
  integers and e_k = ‖A_k − VΛVᵀ‖_∞ computed exactly.
- ρ̄ comes from the Collatz–Wielandt quotient, computed exactly.
- The certificate is an exact Gaussian elimination showing that
  −C − ΣX_k − (ρ̄ + 1/1000)I is positive definite.

**Monte Carlo soundness check (not part of the proof).** I drew 300 θ per box, half of them
vertices, on the hull box and on a small box. There were 0 enclosure violations, and the
largest used fraction of the remainder was 0.925 (the author reported 92%). The largest
sampled λ_max(Ψ) on the hull was −0.110.

**Results:**

| run | root estimate | leaves | splits | largest leaf estimate | all exact tests |
|---|---|---|---|---|---|
| own B&B on the hull box | +0.01259 (linear part 0.0116, remainder ρ 0.1166) | 6 | β_13 ×1, β_12 ×2, β_11 ×2 | −0.00160 | pass |
| author's 9 leaves (covering the author's Θ), my code | +0.0126 (author) | 9 | u_16, u_15 ×2, β_13 ×3, β_12 ×2 | −0.00493 | pass |

Coverage of both partitions was checked exactly: all leaves lie in the root box, their
interiors are pairwise disjoint, and their exact volume sum equals the root volume. My float
estimates on the author's leaves equal the author's to 5 digits.

**Conclusion.** Ψ(θ) ⪯ −(1/1000)I on a box that contains θ(G′) and θ(G). Hence J is
1/1000-strongly concave on the convex sets G′ and G. J is C² near G, because R_t ≥ 192 on G.

## 6. The bound (`final_bound.py`, `logs/final_bound.log`)

For p ∈ F ⊆ G′, the segment [p*, p] lies in G′. Taylor's formula with integral remainder then
gives

  J(p) ≤ J(p*) + ∇J(p*)·(p − p*) − (μ/2)‖p − p*‖² ≤ J(p*) + Σ_t |∂_tJ(p*)| max(p*_t, pmax_t − p*_t).

This is evaluated in exact rationals from the interval end points in Section 2:

| G used | bound (min form, rounded down) | gap to J(p*) |
|---|---|---|
| own G′ | −1170.4862854360886163931058729 | 5.430553e-14 |
| author's G | −1170.4862854360886163931058747 | 5.430553e-14 |
| claimed | −1170.4862854360886163932 | — |

The claimed value is 9.4e-20 below mine, so it is valid.

**Uniqueness claim.** J(p) ≥ J(p*) forces ‖p − p*‖ ≤ 2‖∇J(p*)‖₂/μ ≤ 3.7e-13. This is
inside the stated 6.4e-13; the report's figure comes from 4 × 8.01e-17 and equals 6.408e-13.
F is not known to be convex, so uniqueness needs one more step. p* is interior to F
(min d_t = 5.44 and p* > 0), so the tiny ball around p* lies in F, and J is strictly concave
there. The conclusion holds.

## 7. Review of the author's code (`pindyck_global.py`, `tm1.py`)

I read both files line by line. I found no validity error.

- **LP rows.**
  - Step 1: s ≤ td; the two supply inequalities with e ∈ [e(CSH), e(CSL)]; bounds
    p ≤ α_t/.13 and s ≤ α_t, both valid on F.
  - Step 3: the four McCormick rows for z = pe; the supply equality; the tangent and secant
    rows; bounds s ≤ sub_t, e ∈ [e_lo, e_hi] and z ≤ pmax·e_hi, all valid on G.
  - The initial GCSH has a 1e-12 relative slack.

  All signs are right.
- **Weak-duality code (`LP.bound`).** The ≤-row multipliers are clipped to ≤ 0, the
  equality multipliers are free, and each reduced-cost term is minimized over the box. All
  of this is in exact `Fraction` arithmetic. Correct.
- **W, γ, pmax and Θ.** W is rounded down, γ rounded up, and the Θ end points are rounded
  outward. The indexing E_t ↔ cs_{t−1} is right.
- **`tm1.TM`.**
  - Addition and multiplication allowances: U = 2u, with the ε² rule and remainder
    propagation r_y(|c_x| + S_x) + r_x(|c_y| + S_y) + r_x r_y.
  - `upb`/`lowb` cover sums of ≤ 2^10 terms.
  - `range`, `dec` and `from_iv` are all sound.
- **`linearize`.** Max at the end points plus a tangent lower bound, all in mpmath.iv.
  - One nit: max(t0 − lo, hi − t0) is computed in round-to-nearest.
  - The possible deficit is |h′(t0)|·½ulp ≈ 1e-33. The 2^-40 relative slack on δ ≈ 1e-4
    covers it by a wide margin here.
- **`check_box`.** The symmetrization is exact: fl(a + b) = fl(b + a). The rounding of the
  averages is added to r_s. X_k ⪰ ±A_k holds for any real V. The Collatz–Wielandt bound has a
  128u BLAS allowance, which exceeds γ_16. The interval Gaussian elimination is inclusion
  isotone, so positive pivots prove that the exact symmetric member is positive definite.
- **Branch and bound.** Bisection keeps coverage; mid is between lo and hi.
- **Step 6.**
  - The fixed-point inclusion TX ⊆ X gives a root in X by Brouwer. The root is unique, and it
    lies in TX.
  - The gradient recursion is right.
  - `dec_down` rounds toward −∞.
- **Reproduction.** The author's full run (`logs/author_rerun.out`) reproduces the stored log
  line for line; only the timings differ (15.7 s against 19.1 s).

## 8. Issues

1. **Gap rounding (text fix).**
   - The report and claim 2 say "gap ≤ 5.43e-14". The certified gap is UB − J(p*) =
     5.430553e-14.
   - The two printed numbers differ by 5.430562e-14. Both exceed 5.43e-14 by about 6e-19.
   - The script prints `mp.nstr(..., 3)`, which rounds to nearest.
   - Suggested wording: "gap ≤ 5.44e-14 (≈ 5.43e-14)".
2. **Overclaim about entrywise interval Hessians (text fix).**
   - Claim 5 says entrywise interval Hessians "over any price box cannot succeed". This is
     contradicted by report.md Section 7, which certified the box p* ± 10 by exactly that
     method.
   - The report body is narrower ("over that box … without heavy subdivision"). It still
     generalizes from one sufficient test, λ_max(mid) + ρ(rad).
   - The supporting number depends on the sampler. I used 4,000 samples over [0, pmax]
     (`hull_claim.py`):
     - uniform samples give a hull that passes: −0.105 + 0.090 = −0.015;
     - corner samples give a hull that fails: −0.108 + 0.156 > 0.
   - The report's −0.109 + 0.119 could not be reproduced; its script was not kept.
   - Suggested wording: "Over the full price box [0, pmax], the λ_max(mid) + ρ(rad) test
     fails on the entrywise hull of sampled Hessians when corners are sampled."
     This is not part of the proof.
3. **Documentation of rigor assumptions (minor).** Section 6 says mpmath's float conversions
   round to nearest. In mpmath 1.3.0, `to_float` truncates toward zero (`rnd='d'`). Every
   conversion on a rigorous path is followed by a one-ulp outward `nextafter`, or has ample
   slack (the `tdg` radius), so truncation is also covered. Validity is not affected.
4. **Uniqueness argument (minor).** Add that the ball of radius 2‖∇J‖/μ around p* lies in F,
   because p* is interior. The radius can be stated as ≤ 3.7e-13 using ‖∇J(p*)‖₂ ≤ 1.85e-16.
5. **Script side effect (minor).** `pindyck_global.py` opens `logs/pindyck_global.log` for
   writing, so every rerun replaces the stored log. After my rerun I restored the original
   (md5 8cbf35f0…); `author_data.py` and `author_exec.py` redirect it to `/dev/null`.
6. **Not checked by me.**
   - Literature and novelty.
   - The author's one-off checks in `/tmp/pind`, which were not kept: the 200/200 LDLᵀ
     test, the 30-digit finite differences and the price-space Taylor-model remainders. My own
     checks replace the first two.

## 9. Files and commands

All in `research-20260929/reviews/pindyck-review-checks/`, run from that directory with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout …`:

| command | purpose | result / log |
|---|---|---|
| `python3 <author dir>/pindyck_global.py` (run in the author's directory) | reproduce the author's run | `logs/author_rerun.out`; identical apart from timings |
| `python3 primal_check.py` | primal re-evaluation, J and ∇J enclosure | `logs/primal_check.txt`, `logs/primal_enclosure.txt` |
| `python3 author_data.py` | extract the author's G, Θ and leaves (log to /dev/null) | `author_data.pkl` |
| `python3 own_ranges.py`, `USE_AUTHOR_G=1 python3 own_ranges.py` | own steps 1–4; comparison with the author's G and Θ | `logs/own_ranges.log`, `logs/own_ranges_authorG.log` |
| `python3 hess_check.py` | Hessian identity at 12 points (3.5 min) | `logs/hess_check.log` |
| `python3 af_soundness.py` | Monte Carlo check of own affine forms | `logs/af_soundness.log` |
| `python3 own_concavity.py` | own branch and bound (5 min) | `logs/own_concavity.log`, `leaves.pkl` |
| `python3 verify_own_leaves.py` | re-verify own leaves with the final code, and coverage | `logs/verify_own_leaves.log` |
| `python3 author_leaves_check.py` | author's 9 leaves with own code, and coverage | `logs/author_leaves_check.log` |
| `python3 final_bound.py` | final bound in exact rationals, and statement checks | `logs/final_bound.log` |
| `python3 hull_claim.py` | the report's Section 5 statement (uniform, corner and mixed sampling) | `logs/hull_claim.log` |
| `python3 -m pyflakes *.py` | lint of the review scripts | clean |

- I did not edit any file in `open-instances-wave2/small/`. After rerunning the author's
  script I restored its log from my copy (`logs/author_pindyck_global.log.orig`); the md5
  matches the original.
- No root-maintained file was touched. Nothing was committed.
