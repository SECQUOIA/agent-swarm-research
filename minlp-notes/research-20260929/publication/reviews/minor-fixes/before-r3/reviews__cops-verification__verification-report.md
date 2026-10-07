# Verification of the COPS chain and catmix dual bounds (wave 2)

Date: 2026-09-30. Reviewer: independent verifier (did not produce the results).

**Claims under review:**
`research-20260929/open-instances-wave2/cops/report.md`, with its code and logs.

**What I used:**
- my own code in this directory;
- the reviewer OSIL reader `osilx.py`, copied unchanged from
  `reviews/open-instances-verification/`. The authors' `osilx.py` is
  byte-identical to it.

I did not import or run any of the authors' scripts. I read their logs,
primal vectors, and control files only as data to check.

## Verdict summary

| item | verdict |
|---|---|
| 1a chain polyline reformulation | verified |
| 1b summation-by-parts identity | verified |
| 1c discrete catenary calibration lemma | verified (proof correct line by line; equality holds exactly when D = τ) |
| 1d theorem f ≥ B; V, H' depending on (z_1, z_N) | verified |
| 1e end-window domain and chord condition | verified (one negligible non-rigorous comparison in the authors' code, see 1e) |
| 1f chain dual bounds (all four N) and primal values | verified: my own 2-D branch and bound certifies every claimed bound |
| 2a catmix transformation, M ≥ 0 with exact decimals | verified (checked exactly in rational arithmetic) |
| 2b concavity, homogeneity, chord lower bounds | verified |
| 2c authors' per-ray 1-D interval branch and bound | verified by reading, with caveats (see 2c) |
| 2d catmix100 dual bound (my own implementation) and primal values | verified; my bound is tighter than the claimed one |
| 3 listed bounds; prior certificates; novelty of the lemma | listed bounds confirmed; no prior global certificate or equivalent lemma found in a brief search |

**Headline numbers from my code:**
- **chain dual bounds:** each claimed bound certified (0 unresolved boxes):
  - chain50: 5.072261493982863
  - chain100: 5.0697846107387505
  - chain200: 5.068917341793162
  - chain400: 5.068621694604009
- **catmix100 dual bound:** −0.04806943203114456 (finest grid, config B).
  - This is 7.7e-12 above (better than) the claimed −0.048069432038882705.
  - It is 1.65e-13 below the best primal I found, −0.048069432030979596
    (exact value of double controls), and 1.85e-13 below the authors'
    primal.
- **catmix200 dual bound:** −0.04805914559907277.
  - This is 1.6e-12 above the claimed −0.04805914560067171.
  - It is 1.9e-11 below the authors' primal.

## 1. chain

### 1a. Polyline reformulation: verified

**Structure (my own assertions, all four instances):**
- variables `x_0..x_N` (idx 0..N) and `u_0..u_N` (idx N+1..2N+1), all
  continuous and free except `x_0 = 1` and `x_N = 3`;
- N linear rows `x_{i+1} − x_i − eta u_i − eta u_{i+1} = 0`, with the
  decimal eta equal to exactly 1/(2N);
- length row `eta Σ_{i<N}(s_i + s_{i+1}) = 4`;
- objective `eta Σ_{i<N}(x_i s_i + x_{i+1} s_{i+1})`, constant 0.

**Derivation.** With `z_i = x_i − eta u_i` (i ≤ N) and
`z_{N+1} = x_N + eta u_N`, each linear row reads `z_{i+1} = x_i + eta u_i`.
So `x_i = (z_i + z_{i+1})/2` and `u_i = (z_{i+1} − z_i)/(2 eta)`. This is a
bijection between the solutions of the linear rows and `z ∈ R^{N+2}`.

The two fixed values give `z_0 = 2 − z_1` and `z_{N+1} = 6 − z_N`. Then
`eta s_i = l_i/2` with `l_i = √(h² + (z_{i+1} − z_i)²)`. This gives:
- `λ_0 = l_0/2 = √(eta² + (z_1 − 1)²)`, weighted by `x_0 = 1`;
- `λ_N = √(eta² + (3 − z_N)²)`, weighted by `x_N = 3`;
- interior pieces `λ_k = l_k` (k = 1..N−1), weighted by the midpoint height
  `(z_k + z_{k+1})/2`.

**Checks:**
- Random rational z: the linear rows evaluate to exactly 0 in Fractions.
- The OSIL objective and length row agree with the piece form to below
  1e-50 (60 digits), for N = 50, 100, 200, 400.

### 1b. Summation-by-parts identity: verified

Proof: `v_{k+1} z_{k+1} − v_k z_k = V_k Δz_k + λ_k (z_k + z_{k+1})/2`, with
`V_k = (v_k + v_{k+1})/2`. Summing over k = 1..N−1 gives the identity, with
`v_1 = V` and `v_N = V + L`.

It also holds exactly in rational arithmetic (3 random trials per N, for
arbitrary rational λ, z and V).

### 1c. Calibration lemma: verified

I checked the proof line by line.

- **Scaling to H' = 1.** All terms are homogeneous of degree 2 in
  (a, b, h, H').
- **Step 2.** With `a = sinh φ_a` and `b = sinh φ_b`:
  - `G(b) − G(a) = D + (1 + 2u²) sinh D cosh D`;
  - `c = τ + sinh τ cosh τ`;
  - `(a + b)/2 = sinh S cosh D`;
  - `((b − a)² − h²)/4 = (1 + u²) sinh² D − sinh² τ`.

  sympy reduces all four identities to 0.
- **Step 3 (AM–GM with weight tanh D).** The difference between the step-2
  expression and `f(D)` equals
  `(√(tanh D)·u cosh D − √(Y coth D))²`, with
  `Y = (1 + u²) sinh² D − sinh² τ ≥ 0`. This needs b − a ≥ h (so Y ≥ 0),
  u ≥ 0 and D > 0.
  - sympy leaves a factor `√x·√(1/x)·(e^{2D} + 1) − (e^{2D} + 1)`, which is 0
    for D > 0.
  - Numerically the residual is at double-precision level.
- **Step 4.** sympy confirms `f(τ) = 0` and
  `f'(D) = 1 − sinh²τ / sinh²D`. The derivative is negative below τ and
  positive above it, so f ≥ 0 on D > 0.
- **Equality.** It holds exactly when D = τ, i.e.
  `asinh(b/H') − asinh(a/H') = 2τ`. At D = τ the AM–GM square also
  vanishes, because `√Y = u sinh τ`. The report says "with equality when";
  it is in fact "if and only if".

**Independent tests:**
- **Random test, 200,000 cases at 50 digits.** H' ∈ [1e-4, 1e3],
  h ∈ [1e-5, 10]. The cases cover generic points, the exact equality
  manifold, perturbations of it by factors 1e-9 to 1e-1, and b − a = h or
  much larger.
  - Minimum of `G(b) − G(a) − c − |(a+b)/2|·√((b−a)² − h²)`: +1.7e-31.
  - Largest relative residual on the equality manifold: 8e-51.
- **Adversarial test.** Nelder–Mead over (a, b) at 30 digits, for 40 random
  (h, H') pairs. The minimum found is −2.5e-29, which is rounding on the
  equality manifold.

### 1d. Theorem f ≥ B, and (V, H') depending on (z_1, z_N): verified

**Proof.**
1. Apply 1b.
2. Use `−V_k Δz_k ≥ −|V_k|·|Δz_k|`, with `|Δz_k| = √(λ_k² − h²)`.
3. Apply the lemma to each pair `(v_k, v_{k+1})`, whose difference is
   `λ_k ≥ h`.
4. Telescope, and substitute `L = 4 − λ_0 − λ_N` from the length row.

The bound B depends on the point only through (z_1, z_N). V and H' > 0 are
arbitrary, so choosing them as functions of (z_1, z_N) is legitimate. No
bounds on the interior heights are used.

**Numerical tests:**
- **Random feasible chains** (N = 5, 20, 50; length row enforced to 1e-25;
  5 random multiplier pairs each). The minimum of f − B was 0.044, 0.065
  and 0.13.
- **Near-optimal chains.** I perturbed the optimal chain by amplitudes 1e-9
  to 1e-1, restored the length row exactly, and used both the optimal
  multipliers and perturbed ones (N = 50, 100). The minimum of f − B was
  +6.5e-17 and +1.7e-16. Both are nonnegative and second order, as
  expected.

**Tightness.** At the primal end values, with the multipliers maximizing B:
- chain50: B = 5.07226149398287231644543817697…, matching the authors'
  60-digit KKT value 5.072261493982872316445438;
- chain100, chain200 and chain400 match their KKT values in the same way.

I derived the maximizing multipliers myself from `∂B/∂V = 0` and
`∂B/∂H' = 0`, using `∂G/∂H' = H' asinh(v/H')`:
- `tanh φ_m = (z_N − z_1)/L`;
- `H' sinh((N−1) asinh(eta/H')) = √(L² − (z_N − z_1)²)/2`.

This is the same 1-D equation the authors use.

### 1e. Domain and chord condition: verified

**Domain.** From `λ_0 + λ_N + L = 4`, `L ≥ (N−1)h` and `λ_N ≥ eta`, we get
`λ_0 ≤ 3 + eta`, so `|z_1 − 1| < 3 + eta`. By the same argument,
`|z_N − 3| < 3 + eta`. The authors' box
`[−2−h, 4+h] × [−h, 6+h]` contains this region.

**Chord condition.** The interior polyline runs from `Q_1 = (h/2, z_1)` to
`Q_N = (1 − h/2, z_N)`, a horizontal span of `1 − h`. So
`L ≥ √((1−h)² + (z_N − z_1)²)` is a valid necessary condition.

**Caveat (negligible).** The authors' pruning test computes
`(L.b)**2 < chord2.a`, where `L.b` is squared in plain mpf arithmetic at
50 digits, not in interval arithmetic. It could only mis-prune a box that
touches the feasibility boundary within about 1e-50. My own
branch and bound does this test rigorously and reaches the same bounds.

### 1f. Recomputed dual bounds (own 2-D branch and bound) and primal checks: verified

**Method (`v_chain_bnb.py`):**
- mpmath `iv` at 30 digits;
- G enclosed through its monotonicity (`G' = √(H'² + v²) > 0`);
- asinh built from `iv.log` and `iv.sqrt`;
- per box, the larger of the natural extension and a first-order mean-value
  form, with my own gradient (matches finite differences to 1e-19);
- multipliers from my own brentq solve at the box centre, falling back to
  corners, then to the parent box's multipliers;
- rigorous chord pruning;
- target = (the authors' double-vector objective, as I evaluated it) − 1e-14.

| N | target certified | min leaf LB | boxes (infeasible) | unresolved | time |
|---|---|---|---|---|---|
| 50 | 5.072261493982863 | 5.07226149398286276 | 36,689 (36) | 0 | 50 s |
| 100 | 5.0697846107387505 | 5.06978461073875056 | 52,955 (39) | 0 | 79 s |
| 200 | 5.068917341793162 | 5.06891734179316167 | 75,385 (33) | 0 | 122 s |
| 400 | 5.068621694604009 | 5.06862169460400925 | 104,945 (36) | 0 | 154 s |

All four claimed dual bounds are reproduced exactly.

**Primal vectors (`logs/chainN_primal.txt`).** I evaluated them with my own
code: linear rows exactly (Fractions), the rest at 50 digits.

| N | objective | linear row violation | length row violation |
|---|---|---|---|
| 50 | 5.0722614939828723783 | 2.3e-16 | 2.7e-17 |
| 100 | 5.0697846107387604344 | 2.0e-16 | 1.1e-17 |
| 200 | 5.0689173417931710057 | 3.1e-16 | 2.4e-17 |
| 400 | 5.0686216946040190477 | 3.6e-16 | 1.2e-18 |

These match the report's primal values and violations. The resulting gaps
are 9.4e-15, 9.9e-15, 9.0e-15 and 1.0e-14, as claimed.

## 2. catmix

### 2a. Transformation and nonnegativity with exact decimals: verified

**Structure (own assertions, all four N):**
- `u ∈ [0,1]`, `x1_0 = 1`, `x2_0 = 0`, other states free;
- objective `x1_N + x2_N` with OSIL `constant="-1"`. The reader's
  `obj["constant"]` returns `"-1"`, and I added it everywhere.

**Constants.** They are read as exact rationals:
- `a = 1/(2N)`, `b = 10a`, `ep = 1 + a`, `em = 1 − a`;
- `ep + em = 2` exactly, so `Q = 2I − P` and `M = 2P^{-1} − I`;
- c is used exactly as written. Its offsets from 9a are:

  | N | c − 9a |
  |---|---|
  | 100 | 5e-18 (c = 4.5000000000000005e-2) |
  | 200 | 3e-18 |
  | 400 | 1e-18 |
  | 800 | 1e-18 |

**Stage polynomials.** sympy with exact rationals gives
`Nm = Q adj(P)`, `D = det P` and `T = (1,1) adj(P)`, and confirms
`P·adj(P) = det(P)·I`. Exact minimum over [0, 1] for N = 100:

| polynomial | minimum over [0,1] |
|---|---|
| Nm11 | 1.005 |
| Nm12, Nm21 | 0 (at u = 0) |
| Nm22 | 0.955 |
| T1 | 1.005 |
| T2 | 1 |
| D | 1.005 |
| Q entries | ≥ 0 |

Other N are analogous. So M ≥ 0 and P^{-1} ≥ 0 entrywise on [0, 1], the
states stay nonnegative, and J ≥ −1.

**Reduction.** Setting `y_i = Q(u_i) x_i` gives `x_i = P(u_i)^{-1} y_{i−1}`
and `y_i = M(u_i) y_{i−1}`. Composing my interval stage maps along the
authors' controls encloses the exact objective:
[−0.04806943203105763, −0.04806943203086033] contains
−0.0480694320309595635.

### 2b. Concavity, homogeneity, chord lower bounds: verified

- Each `V_i` is a pointwise minimum, over control sequences, of linear
  functions of y. So it is concave and positively homogeneous on the
  quadrant, hence superadditive.
- Then `V(s r_k + t r_{k+1}) ≥ s V(r_k) + t V(r_{k+1}) ≥ s w_k + t w_{k+1}`
  for s, t ≥ 0, which validates the chord interpolation.
- In θ form, `W(y) = w_k ρ(y) + σ_k g_k(y)` on cone k, where
  `g_k(y) = (1−θ_k) y_2 − θ_k y_1`. This matches the authors'
  `α = w_k − σ_k θ_k` and `β = w_k + σ_k(1−θ_k)`.
- Clipping at 0 is valid because V ≥ 0.
- Dyadic θ makes `1 − θ` and the θ differences exact.

### 2c. Authors' per-ray 1-D interval branch and bound (read critically): verified with caveats

I found no validity error in `catmix_bound.py` / `ivx.py`.

**What I checked:**
- **ivx rounding.** Round-to-nearest plus one `nextafter` step outward is
  valid.
- **Cone filter (`candidates`, `few_lb`).** The θ-range of the (z_1, z_2)
  box is rounded outward and padded by one cone. The cross-product filter
  can only drop cones the box cannot meet. `few_lb` is used only when there
  are at most KMAX = 8 candidate cones, so every candidate is examined.
- **`mv_lb`.** The formula for f'' is correct. The one-sided second-order
  Taylor bounds are correct for h > 0, h ≤ 0 and "stationary point beyond r".
  The monotone cases evaluate the correct endpoint.
- **Many-cone Lipschitz bound.** Uses
  `f' ∈ S'·[min w, max w] + S·[min σ, max σ]·Θ'` a.e. This is valid for the
  piecewise-C¹ Lipschitz f.
- **Leaves.** Leaves are either done (LB ≥ incumbent − 1e-14) or forced
  (width < 1e-14); their LB is always included. Exceeding `max_rounds`
  raises an error. Incumbents affect only termination.
- **Final value.** `dn(w0 − 1)` is correct.

**Caveats:**
1. The design relies on float incumbents and a 1e-14 per-stage tolerance.
   This makes it slightly lossy (see 2d); it is not invalid.
2. **Weaker than claimed:** their catmix100 bound is 7.7e-12 below the bound
   my implementation certifies. So the report's remark that "the remaining
   7.9e-12 is probably slack in our primal, not in the bound" is wrong:
   - their primal has at most 1.85e-13 of slack (a local Newton polish
     recovers 2.0e-14 of it);
   - at least 7.7e-12 of their gap is slack in their bound.
   
   Their 1e-5-plus-band run and their uniform 3e-6 run give bit-identical
   bounds, which also points to a grid-independent loss in their stage
   minimization. I did not diagnose it further.
3. The report calls the listed primal "improved by about 3.4e-8". That is
   relative to the authors' own local-solve value −0.04806939757. The
   MINLPLib page prints only 8 digits (−0.04806939).

### 2d. Own dual bound and primal checks: verified

**My method (`v_catmix_dp.py`).** It uses the same DP principle as the
authors, implemented independently, with a different per-ray minimization.

For each output ray r_j:
1. **Cut u ∈ [0, 1] into intervals.** The cuts are at float preimages p of
   the cone boundaries (roots of the quadratics `g_k(Nm(u) r_j)`), plus tiny
   intervals `[p − 1e-9, p + 1e-9]`.
2. **Verify cone ranges rigorously.** Each interval gets a cone range
   [klo, khi]. I verify it with rigorous bounds on the quadratics
   `g_klo(n(u)) ≥ 0` and `g_{khi+1}(n(u)) ≤ 0` over the interval, widening
   the range until verified. On each (interval, cone) pair, f equals the
   rational function `p_k(u)/D(u)`, with p_k and D quadratics.
3. **Bound each pair.** Each pair gets either:
   - a crude bound `(s/D)_min · min(w_k, w_{k+1})`, or
   - an exact Dinkelbach step: take the float minimum t, bound
     `min_u (p_k − tD)` rigorously (exact case analysis for quadratics,
     using lower coefficients since u ≥ 0), and set
     `LB = t + m/D_min` if m < 0, or `t + m/D_max` otherwise.

   The crude bound is used only when it is at least the float incumbent.
4. **Arithmetic.** My own numpy interval arithmetic (nextafter outward).
   Constants are exact Fractions rounded outward.

**Self-test.** 40 stages × 17 off-grid rays, for N = 100 and N = 200:
- the rigorous LB never exceeds a dense float minimum (20,001 samples plus a 20,001-point
  local refinement); the maximum of LB − dense is −6.7e-16;
- it stays within 2.1e-15 of that minimum.

**catmix100 results.** Gaps are measured to the authors' primal
−0.0480694320309596. The base grid is dyadic on [0, 13/128], plus 2^-7
spacing on [13/128, 1].

| grid | rays per stage | dual bound | gap | time |
|---|---|---|---|---|
| uniform 2^-9 | 168 | −0.048389042188658256 | 3.2e-4 | 0.4 s |
| uniform 2^-11 | 324 | −0.048090331072869426 | 2.1e-5 | 1 s |
| uniform 2^-13 | 948 | −0.04807071360756377 | 1.28e-6 | 9 s |
| uniform 2^-15 | 3,444 | −0.048069511665857274 | 8.0e-8 | 134 s |
| config A (below) | 4,917 (mean) | **−0.048069432031981114** | **1.02e-12** | 704 s |
| config B (below) | 9,131 (mean) | **−0.04806943203114456** | **1.85e-13** | 2,358 s |

- **Config A:** base 2^-15, band [0.0695, 0.0717] at 2^-19, and a window of
  401 rays at 2^-24 centred on the primal trajectory θ_i at every stage.
  6.6e8 (interval, cone) pairs; maximum stage loss against the float
  incumbent 2.2e-15.
- **Config B:** base 2^-16, band [0.0697, 0.0715] at 2^-20, and a window of
  601 rays at 2^-25 around θ_i. 2.0e9 pairs; maximum stage loss 2.1e-15.
- The uniform runs converge at second order (gap ×1/16 per halving of the
  spacing), as chord interpolation of a concave function should.
- The listed dual −0.0666 is beaten already at 2^-9.

**Primal.**
- **Authors' controls, simulated exactly in rational arithmetic:**
  - N=100: −0.0480694320309595635
  - N=200: −0.0480591455801143916
- **60-digit interval simulation:**
  - N=400: −0.048056547756611554855
  - N=800 (`_snap`): −0.048055901330847466886
  - N=800 (non-snap): −0.0480559013293737
- All values match the report.
- **Double vectors, evaluated exactly:** row violations of 1.0e-16,
  1.01e-16, 1.04e-16 and 1.05e-16 (N=800 non-snap: 1.06e-16). Bounds are
  satisfied, and the vectors' controls equal the `.npy` files.
- **My active-set Newton polish (40 digits) from the authors' N=100 point.**
  - It converges to a KKT point: 33 free controls, reduced Hessian
    eigenvalues in [9.2e-8, 1.8e-3], gradient ≥ 7.9e-9 at the lower bound
    and ≤ −2.77e-6 at the upper bound.
  - Value: J = −0.04806943203097959910654. Double-rounded controls give an
    exact J of −0.048069432030979596104, which is 2.0e-14 better than the
    authors' point (`logs/catmix100_u_newton.npy`).
  - So for catmix100, the global optimum lies in
    [−0.04806943203114456, −0.048069432030979596]. The width of this
    interval is 1.65e-13.

**catmix200 (config A grid, same flags):** dual bound −0.04805914559907277
(1,170 s, 8.6e8 pairs, maximum stage loss 2.1e-15).
- It is 1.9e-11 below the authors' exact primal −0.0480591455801143916.
- It is 1.6e-12 above the claimed −0.04805914560067171, so it confirms the
  claim.

**Not recomputed:** catmix400 and catmix800 dual bounds (primal values only).

## 3. Listed bounds and prior work

**MINLPLib instance pages (fetched 2026-09-30).** They agree with the
report's table.

| instance | primal | dual (source) | other duals |
|---|---|---|---|
| chain50 | 5.07226149 | 0.17451499 (ANTIGONE) | BARON −45.23, Couenne −49.77, Gurobi −37.10, LINDO −32.77, SCIP −38.84 |
| chain100 | 5.06978461 | 0.09367008 (ANTIGONE) | |
| chain200 | 5.06891734 | 0.08256615 (ANTIGONE) | |
| chain400 | 5.0686217 | 0.09563835 (ANTIGONE) | |
| catmix100 | −0.04806939 | −0.06655801 (LINDO) | |
| catmix200 | −0.04805912 | −0.07254639 (LINDO) | |
| catmix400 | −0.04805652 | −0.65810523 (LINDO) | |
| catmix800 | −0.04805584 | −1.48896963 (LINDO) | |

No instance is marked solved. LINDO's catmix800 dual is below the trivial
bound −1, as the report says.

**Prior certificates (brief search).** I found no prior global certificate
for the COPS chain or catmix instances.
- The COPS 3.0 report (Dolan, Moré and Munson, 2004) benchmarks local NLP
  solvers.
- Global optimal-control methods such as branch-and-lift (Houska and
  Chachuat, JOTA 2014) address continuous-time problems. I did not find
  them applied to these discretized instances.

**Lemma novelty (brief search).** I did not find the discrete catenary
calibration lemma, or a discrete Weierstrass-field argument for the
horizontally discretized COPS chain.
- The closest work is Gabrys and Sremac, arXiv:2510.20917 (Oct 2025),
  "A Convex Optimization Approach to the Discrete Hanging Chain Problem".
  It treats the fixed-link-length model with free 2-D joints, which is
  convex. It does not cover the COPS model (fixed horizontal mesh, variable
  piece lengths, total length), and it uses no calibration.
- General discrete variational theory exists (discrete Hamiltonian systems;
  discrete Jacobi and Legendre conditions, e.g. Ahlbrandt and Peterson).
  I did not check it in depth.
- "Not found" is therefore a weak statement, not a novelty proof.

## 4. What remains unchecked

- catmix400 and catmix800 dual bounds (not recomputed; the method was
  verified on N = 100 and N = 200).
- The authors' exploratory claims in "What failed" (grid estimates only).
- Whether the catmix KKT point I polished is the global optimum. The bound
  leaves a window of 1.65e-13.
- The literature search was brief (web search only; no full-text reading of
  the COPS report or the discrete-variational literature).

## 5. Commands run

All runs were targeted and single-threaded (`OMP_NUM_THREADS=1`), from this
directory. No CI or project-wide checks were run.

**chain:**
- `python3 v_chain_checks.py struct`: structure, parametrization, identity
  and primal vectors (`logs/chain_struct.log`).
- `python3 v_chain_checks.py lemma 200000` (`logs/chain_lemma.log`) and
  `python3 v_chain_checks.py lemma 0 adv` (`logs/chain_lemma_adv.log`).
  The traceback at the end of `chain_lemma.log` comes from the first version
  of the adversarial test, which formed b in double precision. The fixed
  test is the one in `chain_lemma_adv.log`.
- `python3 v_chain_checks.py theorem` (`logs/chain_theorem.log`).
- `python3 v_chain_bnb.py 1e-14 50` (`logs/chain50_bnb.log`),
  `python3 v_chain_bnb.py 1e-14 400` (`logs/chain400_bnb.log`) and
  `python3 v_chain_bnb.py 1e-14 100 200` (`logs/chain100_200_bnb.log`).

**catmix:**
- `python3 v_catmix_model.py 100 200 400 800`: structure, exact
  nonnegativity and primal checks (`logs/catmix_model.log`).
- `python3 v_catmix_selftest.py 100` and `python3 v_catmix_selftest.py 200`
  (`logs/catmix_selftest*.log`).
- `python3 v_catmix_dp.py 100 {9, 11}`, `python3 v_catmix_dp.py 100 13 15`
  (older CLI; `logs/catmix100_uniform_13_15.log`), and
  `python3 v_catmix_dp.py 100 13 0.0685 0.0725 13 200 24`
  (`logs/catmix100_win_test.log`).
- `python3 v_catmix_dp.py 100 15 0.0695 0.0717 19 200 24`
  (`logs/catmix100_cfgA.log`) and
  `python3 v_catmix_dp.py 200 15 0.0695 0.0717 19 200 24`
  (`logs/catmix200_cfgA.log`).
- `python3 v_catmix_dp.py 100 16 0.0697 0.0715 20 300 25`
  (`logs/catmix100_cfgB.log`).
- `python3 v_catmix_primal.py 100` (compose check;
  `logs/catmix100_primal_reviewer.log`) and
  `python3 v_catmix_newton.py 100` (`logs/catmix100_newton.log`).

**Web:** the MINLPLib pages of all eight instances, plus the searches cited
above.

## Files

All files are in `research-20260929/reviews/cops-verification/`:
- scripts: `v_chain_checks.py`, `v_chain_bnb.py`, `v_catmix_model.py`,
  `v_catmix_dp.py`, `v_catmix_selftest.py`, `v_catmix_primal.py`,
  `v_catmix_newton.py`;
- the OSIL reader `osilx.py` (copy);
- `logs/`.
