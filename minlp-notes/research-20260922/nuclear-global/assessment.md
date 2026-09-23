# Can problem-specific theory close the open nuclear* instances? A feasibility assessment


## Corrections after independent review

An [independent review](review-assessment.txt) (scripts in `code/review/`,
outputs in `runs/review/`) confirmed the reformulation, the counts, the validity
of all four bounds and the no-go verdict. Corrections:

- Reformulation: (R4) should include `lam_t > 0` in the feasible set, and `p_t` is
  the Perron vector of `diag(k) G` (not `G diag(k)`). The 24 tie rows in va–vf
  (nodes (1,7) and (11,14) carry the same fuel type) are confirmed.
- Certified root bounds (B3 with B2), recomputed and certified in exact rational
  arithmetic by the reviewer, rounded up: nuclearva 1.182044, vb 1.184036, vc
  1.194607, vd 1.193068, ve 1.189370, vf 1.178376, nuclear14 1.196839. These
  improve the earlier certified bounds by 0.22–1.25%. Four of the six-decimal
  entries below (va, vd, vf, 14) were up to 1.2e-6 below what can be certified;
  the va value 1.182043 came from a Gurobi tolerance artifact. The
  aggregate-burn bound (B4) is valid, but its values (for example nuclearva
  1.16071, nuclear14 1.1855) are floating-point Gurobi results, not certificates.
- "A fixed pattern leaves no continuous freedom" depends on the unproven
  uniqueness assumption U. As stated ("at most one peaking-feasible fixed point"),
  U does not support enumeration: for the 78% of patterns whose computed fixed
  point violates peaking, a second, feasible fixed point would not be excluded.
  U must be stated as uniqueness over the whole domain where reactivity stays
  positive. The sampled contraction bound "<= 0.53" is a sample maximum; the
  reviewer found 0.578.
- "No subtree can be pruned at any depth" is false: with only the fresh fuel
  placed, the interval propagation proves 4 of the 220 placements infeasible
  (about 1.8% of va patterns). No subtree is pruned by bound, so the conclusion
  that the search degenerates into enumeration stands.
- The stored primal points keep about 25 digits, so their row violations are
  about 1e-24, not 1e-57; all seven are feasible and their objectives confirmed
  (also re-checked by the coordinator with the separate evaluator,
  `code/check_primal_independent.py`).
- Enumeration cost: 2.8–3.6 ms per pattern, 62–79 core-hours per instance.
- Reviewer addendum: for the nuclear14 aggregate-burn (B4) root relaxation, the
  reviewer's independent model with auxiliary variables `s = Gp` ended at a Gurobi
  bound of 1.184370 (incumbent 1.182184), consistent with and tighter than the
  author's 1.185512; without `s = Gp` Gurobi stalled at 1.194700. These are
  floating-point values, not certificates.
Date: 2026-09-23. Author: research agent. Status: author results, not independently
reviewed. Code: `code/` (entry points listed in Section 7). Run outputs: `runs/`.
Context: [nuclear-bounds.md](../benchmark-observations/nuclear-bounds.md) and its
[review](../benchmark-observations/review-nuclear-bounds.txt).

## Summary

- **Verdict: no-go** for proving global optimality of any of the 18 instances with
  bound-driven branch and bound over reload patterns. The bounds developed here
  are valid. Even at a complete pattern, however, they are 11–13% above the
  pattern's true value (nuclearva) or 3.9–4.9% above it (nuclear14). Pattern values
  differ by only about 3%. No subtree can be pruned at any depth.
- **Conditional go** for the six va–vf instances by exhaustive enumeration. They
  have 12!/3! = 79,833,600 distinct patterns, and no symmetry reduces this.
  Measured cost is 2.8 ms per pattern, so a full enumeration takes about
  62 core-hours: a few hours wall-clock on this 36-thread machine when it is idle.
  Enumeration proves optimality only if each pattern has a **unique equilibrium cycle** (assumption U below).
  All numerical evidence supports U, but U is unproven. Without U, certifying one
  pattern is itself hard: Gurobi left a 0.75% gap on one fixed pattern after
  600 s on 4 threads.
- **nuclear14, 14a and 14b have 24 nodes, not 14.** The name comes from
  the MacMINLP data file `c-reload-14a.dat`. They have 24!/6! ≈ 8.6e20 patterns (F1)
  or about 2.9e25 reload path covers (F2, F3), which rules out enumeration. The 25-,
  49- and 104-node families are larger still.
- **Gap closing is modest.** The new root bounds lower the certified bound by
  0.2–1.3% (interval equilibrium propagation, B3) or by 2.0–4.4% for va–vf and 1.2% for nuclear14
  (root aggregate-burn relaxation, B4, a floating-point Gurobi value). For example,
  nuclearva goes from 1.18463 to 1.16071 against a primal of 1.01430. The gap is
  structural: every relaxation that does not solve the coupled burnup–eigenvalue
  equilibrium loses about 13% on va–vf.
- **By-products:**
  - An exact power-variable reformulation. It was checked by regenerating every
    OSiL row of 9 instances exactly, plus a 60-digit round trip on 4 instances.
  - Improved primal points on nuclearva, nuclearvb, nuclearvd, nuclearve,
    nuclearvf and nuclear14 (Section 5), each checked against all OSiL rows at
    60 digits.

## 1. Power-variable reformulation

Notation from `nuclear-bounds.md`: nodes `i`, steps `t = 1..T`, `G >= 0`
irreducible, weights `V`, burn coefficient `a`, peaking limit `c`, and
fresh-fuel reactivity `KF`.

The reformulated model uses variables `p_{it} >= 0`, `k_{it}`, `lam_t`, and the
unchanged assignment and reload variables (binaries, `kappa`, continuous copies, `z`):

    (R1) k_{i,t+1} = k_{it} - a p_{it}                (linear burnup)
    (R2) sum_i V_i p_{it} = 1                         (linear normalization)
    (R3) p_{it} <= c_{it}                             (linear peaking)
    (R4) lam_t p_{it} = k_{it} (G p_t)_i,  lam_t > 0  (eigen rows)
    (R5) phi_lb lam_t <= (G p_t)_i                    (only F2/F3, where phi >= phi_lb > 0)
    reload and assignment rows unchanged (they involve only k_{.,1}, k_{.,T} and the pattern variables)
    objective: max lam_T

**Proposition 1 (exact equivalence).** The map `(phi, k, lam, w) -> (phi o k, k, lam, w)`
is a bijection from the OSiL feasible set onto the feasible set of (R1)–(R5) plus
the reload rows. It preserves the objective. Its inverse is `phi_t = G p_t / lam_t`.

*Proof.*

- **lam_t > 0 in the original model.** If `lam_t = 0`, the eigen rows give
  `sum_j G_ij phi_jt k_jt = 0` for all `i`. Every column of an irreducible `G`
  (with `N >= 2`) has a positive entry, and `phi, k >= 0`. Hence
  `phi_jt k_jt = 0` for every `j`, which contradicts the normalization row.
- **Forward direction.** Set `p = phi o k >= 0`. The eigen row gives
  `phi_t = G p_t / lam_t`. Multiplying row `i` by `k_it` gives (R4). The burnup,
  normalization and peaking rows become (R1)–(R3). The bound on `phi` becomes (R5).
- **Converse.** Given a reformulated point, define `phi = G p / lam >= 0`. Then
  (R4) gives `phi_i k_i = p_i`, so `lam phi_i = (G p)_i = sum_j G_ij phi_j k_j`, and
  every original row holds.
- **Uniqueness of the inverse.** The inverse is unique because
  `phi = G p / lam` is forced by the original eigen rows. □

The only upper bounds on `phi` in any file are `+INF`, so (R5) has no upper
counterpart.

**Verification** (targeted checks, run locally):

- `code/nucmodel.py` rebuilds all rows and variable bounds of an instance from
  the structured data (G, V, c, a, KF and the reload structure). It then compares
  them with the parsed file as multisets of exact rational rows, up to a sign
  per row. The files are parsed by the reviewer's independent exact parser.
- This check passed for nuclearva, vb, vc, vd, ve, vf, 14, 14a and 14b. It found one
  structural fact missing from the earlier note: in va–vf, 24 rows
  `y_{1,g} = y_{7,g}` and `y_{11,g} = y_{14,g}` (1-based nodes) tie the two
  pairs of diagonal half-nodes to the same fuel type.
- `code/reform.py` solves the equilibrium in power variables at 60 digits. It maps
  the point back with `phi = G p / lam` and evaluates every OSiL row with the
  independent evaluator `osil_eval` at 60 digits.
- Maximum row violations: nuclearva 2.8e-57, nuclear14 8.6e-57, nuclear14a
  3.0e-56 and nuclear14b 3.0e-56. The power-model residuals are below 3e-61, and
  bound violations are 0 (`runs/reform_check.txt`).

## 2. Combinatorial structure (14-node va–vf; 24-node nuclear14, 14a, 14b)

| | va–vf | nuclear14 | nuclear14a (F2) / 14b (F3) |
|---|---|---|---|
| nodes N, steps T | 14, 6 | 24, 8 | 24, 8 |
| pattern | 12 fuel types (3 chains × ages 0–3) on 12 slots (10 nodes + 2 tied half-node pairs) | 24 types (6 chains × 4 ages) on 24 nodes | each node gets fresh fuel or the fuel of one node; 6 fresh; chains of any length |
| distinct patterns | 12!/3! = 7.98e7 | 24!/6! = 8.62e20 | Lah number L(24,6) = 2.90e25 (path covers) |
| exact automorphisms of (G, V, c, ties) | trivial | trivial | trivial |

- Chains are interchangeable, which gives the division by the number of chains
  factorial.
- The automorphism search (`code/symmetry.py`) compares exact rational entries.
- In F2, a closed reload cycle is infeasible because burnup is strictly positive
  (`phi >= phi_lb > 0`).
- F3 also lets the reload lower reactivity (`z_ij <= k_jT`), which leaves
  continuous freedom even after the pattern is fixed.

**A fixed F1 pattern has no continuous freedom.**

1. **Positive reactivity.** Each burn step removes at most `a c`, so a feasible
   point satisfies `k_{it} >= KF - a c (A(T-1) + t - 1) > 0` for fuel of age `A`.
   Over all ages and steps these lower bounds are at least 0.69 (va), 0.70 (vc), 0.77 (vf), 0.79 (vb,
   vd, ve) and 0.945 (nuclear14).
2. **Perron uniqueness at each step.** `G diag(k_t)` is irreducible and
   nonnegative. By Perron–Frobenius, the only nonnegative `p_t` with `V'p_t = 1`
   that satisfies (R4) is the normalized Perron vector, and `lam_t = rho(G diag(k_t))`.
3. **Reduction to a fixed point.** The reload is affine for a fixed pattern:
   `k_1 = KF f + R k_T`, where `R >= 0` is nilpotent, its rows are V-weighted
   means, and `R^4 = 0`. The feasible set of a pattern is therefore
   `{fixed points of Phi(k_1) = KF f + R(k_1 - a sum_{t<T} p_t(k_1))}` intersected
   with peaking. This is a square system of 183 equations in 183 unknowns for va.

**Assumption U (unique equilibrium cycle): Phi has at most one peaking-feasible fixed point.**
The numerical evidence is strong but is not a proof (`code/uniqueness.py`,
`runs/uniq_*.txt`).

- **Random starts.** Fixed-point iteration was run from 20 random starts
  (10 for nuclear14) in the a-priori box, on 30 random patterns each for va and vc
  and 10 for nuclear14. Every start converged to the same point (spread ≤ 1.5e-9).
- **Local contraction.** At the fixed points `rho(dPhi)` is 0.33–0.61.
- **Sampled contraction of Phi^4.** At random points of the box,
  `||d(Phi^4)||_inf` is at most 0.53 (va), 0.60 (vc) and 0.72 (nuclear14).
- **No proof yet.** The obvious proof routes fail:
  - The Birkhoff–Hopf contraction coefficient of `G^5` is `1 - 4e-5` (va) and 1 to
    machine precision (nuclear14).
  - The cores are loosely coupled: `|lambda_2|/lambda_1` is 0.941 (va) and 0.966
    (nuclear14).
  - The naive bound `||dPhi^4|| <= (1 + a||D||)^4 - 1`, where `D` is the Perron
    sensitivity, exceeds 1.

  The measured contraction comes from the negative feedback between burnup and
  power, not from a spectral gap.

Cost of one pattern: 19 ms (va) and 89 ms (nuclear14) serially, or 2.8–3.6 ms (va,
vd) with the batched evaluator `code/enum_batch.py`. Fixed-point residuals are
below 7e-12.

## 3. Node bounds for a branch and bound over patterns

Let `kh_i` be any valid upper bound on `k_{i,T}` at a node of the search tree.

The following facts give node bounds; each is valid under the stated
assumptions:

- **(K+) Age bounds on reactivity.** For fuel of age `A` at step `t`,
  `KF - a c (A(T-1) + t - 1) <= k_{it} <= KF`.
  - The upper bound is (K) from the earlier note.
  - The lower bound follows by induction: each step burns at most `a c` because
    `p <= c`, and the reload takes V-weighted means.
- **B1 (Perron monotonicity).** `lam_T <= rho(G diag(kh))`.
  - `phi_T >= 0` and `phi_T != 0`, so `lam_T` is an eigenvalue of `G diag(k_T)`,
    hence `lam_T <= rho(G diag(k_T))`.
  - `0 <= G diag(k_T) <= G diag(kh)` entrywise, and the spectral radius is
    monotone in the entries of a nonnegative matrix.
- **B2 (Collatz–Wielandt with node-adaptive weights and peaking).**
  `lam_T <= max_{p in P} y'Gp / sum_i y_i p_i/kh_i` for every `y >= 0` with
  `sum_i y_i p_i/kh_i > 0` on `P = {V'p = 1, 0 <= p <= c}`.
  - Since `phi, k >= 0`, `p_i = phi_i k_i <= phi_i kh_i`.
  - Hence `lam_T sum_i y_i p_i/kh_i <= lam_T y'phi_T = y'G p_T`.
  - Choosing `y` as the left Perron vector of `G diag(kh)` makes the ratio equal
    `rho(G diag(kh))` for every `p`. So the optimized B2 is never worse than B1
    (it is better only through peaking).
  - `y` is found by LP bisection, and the inner maximum is a fractional knapsack.
    This generalizes the (P) bound of the earlier note, which used `kh = KF`.
- **B3 (burn-aware kh by interval equilibrium propagation, IEP; `code/iep.py`,
  `code/nodebounds.py`).** Keep boxes `K_t` for `k_t` and repeat the following
  until nothing changes:
  - Set `Lam_t = [rho(G diag kl_t), rho(G diag kh_t)]`. This is valid because
    `lam_t` is the Perron root when `k_t > 0` (by (K+)), and the Perron root is
    monotone.
  - Take `P_t` as the box hull of the Perron cone
    `Q_t = {p >= 0, V'p = 1, p <= c, Ll p_i <= kh_i (G p)_i, Lh p_i >= kl_i (G p)_i}`.
    Every feasible `p_t` lies in `Q_t`, because
    `Ll p_i <= lam p_i = k_i (G p)_i <= kh_i (G p)_i`, and similarly for the other side.
  - Update `K_{t+1} <- K_{t+1} ∩ (K_t - a P_t)` and `K_1 <- K_1 ∩ (KF f + R K_T)`
    wherever the node's fuel type and its predecessor are assigned.
  - Every feasible point of the subtree stays inside the boxes. An empty `Q_t`
    proves the subtree infeasible.
- **B4 (aggregate-burn relaxation).** Keep the eigen rows at `T` only. Replace the
  steps `t < T` by the cycle burn `b = sum_{t<T} p_t`, with
  `k_T = k_1 - a b`, `V'b = T - 1` and `0 <= b <= (T-1)c`. Keep the reload rows.
  - This is a relaxation because every feasible point maps to a feasible point
    with the same `lam_T`.
  - It is solved globally by Gurobi, both at a fixed pattern
    (`code/nodebounds.py`) and at the root over all patterns (`code/b4root.py`).

Certification status:

- B1, B2 and B3 are computed in floating point here. A certificate would need
  safe LP bounds (Neumaier–Shcherbina) and Collatz–Wielandt enclosures of the
  eigenvalues. This is routine and has not been done.
- B4 values are Gurobi's floating-point claims.

**Root bounds** (upper bounds on `lam_T`; the objective is `-lam_T`):

| instance | certified (earlier note) | B2 with root IEP (B3) | root B4 | best primal, 60-digit verified | listed primal |
|---|---|---|---|---|---|
| nuclearva | 1.184634 | 1.182043 | 1.160711 | 1.0143049 | 1.0142312 |
| nuclearvb | 1.195181 | 1.184036 | 1.151812 | 1.0323440 | 1.0313359 |
| nuclearvc | 1.204743 | 1.194607 | 1.151740 | 1.0048472 | 1.0048472 |
| nuclearvd | 1.205524 | 1.193067 | 1.166136 | 1.0420785 | 1.0416454 |
| nuclearve | 1.202431 | 1.189370 | 1.162638 | 1.0398217 | 1.0376405 |
| nuclearvf | 1.193331 | 1.178375 | 1.151199 | 1.0245314 | 1.0240875 |
| nuclear14 | 1.200010 | 1.196838 | 1.185512 (time limit 1800 s; Gurobi's dual bound) | 1.1297096 | 1.1296874 |

**Partial-pattern bounds** (B2 with IEP). The fuel is assigned in the order
"fresh fuel first, then by age" along one pattern:

| slots assigned | 0 | 3 | 6 | 9 | all (leaf) | leaf B4 | the pattern's value |
|---|---|---|---|---|---|---|---|
| nuclearva (best pattern) | 1.18204 | 1.17621 | 1.16627 | 1.15339 | 1.14430 | 1.13105 | 1.01430 |
| nuclear14 (a random feasible pattern) | 1.19684 | 1.19617 | 1.19486 | 1.19284 | 1.17901 | 1.16869 | 1.12442 |

The rows of the nuclear14 partial-pattern table are at 0, 3, 6, 9 and 24
assigned slots.

On one fixed nuclearva pattern (`code/grb_power.py`), Gurobi on the power model
reached a root bound of 1.1497 after cuts. After 600 s on 4 threads it stood at
1.02192, a 0.75% gap, against the value 1.01430.

**Required accuracy versus achieved accuracy.**

- A random sample of 124,000 nuclearva patterns (`runs/sample_nuclearva_*.npy`)
  shows how many patterns are feasible and within a given distance of the best
  value 1.01430:
  - within 1%: 14.6% of patterns;
  - within 0.5%: 2.5%;
  - within 0.2%: 0.086%.
  21.7% of patterns satisfy peaking at all.
- The same figures for nuclearvd (40,000 patterns) are 6.7%, 0.26% and 0.01%.
- To prune most of the tree, a bound at a partial pattern would need an accuracy
  of about 0.1–0.5%. The bounds above are 13% off at the leaves. The effective
  branching factor is therefore the full `12, 11, ..., 1`: branch and bound
  degenerates into enumeration.
- The loss is structural. Any relaxation that decouples the power shape at
  `t < T` from the reactivity lets the fresh fuel keep `k = KF` with little burn.
  The true equilibrium has high power in high-reactivity fuel. The IEP Perron
  cone cannot express this either, because over a-priori boxes (reactivity ratio
  about 1.4) and with `|lambda_2|/lambda_1 ≈ 0.94–0.97`, it barely constrains the
  power shape.

## 4. Go/no-go

- **nuclear14, 14a, 14b, 25, 25a, 25b, 49, 49a, 49b, 10a, 10b and 104: no-go.**
  - They have at least 8.6e20 patterns, and no bound prunes.
  - The best new root bound improves the certified gap only slightly. For
    nuclear14 it drops from 6.2% to 5.9% (B3) or to 4.9% (B4, floating point).
  - Closing these gaps "substantially" would need a relaxation that captures
    the burnup–eigenvalue equilibrium. None is known.
- **va–vf: no-go for branch and bound, and conditional go for enumeration.**
  - Pruning is impossible with the available bounds (Section 3), but the whole
    space is only 7.98e7 patterns.
  - A proof requires two steps:
    1. **Prove U.** One uniform theorem for all patterns suffices. Candidate
       routes:
       - a contraction of `Phi^4` in a weighted norm, proved with bounds on
         Perron sensitivity that exploit the burnup feedback;
       - the Gale–Nikaido univalence theorem (`I - dPhi` is a P-matrix on the
         domain);
       - a degree or index argument.

       None is in hand. The measured `||d(Phi^4)||_inf <= 0.72` suggests a
       contraction constant exists.
    2. **Enumerate with certified per-pattern enclosures.** Given U with a
       constant `L < 1` for `Phi^4`, the error bound
       `|k* - k~| <= |Phi^4(k~) - k~| / (1 - L)` and verified eigenvalue bounds
       settle each pattern's value and peaking with margin. Only patterns within
       a tolerance of the incumbent need extended precision.
  - Estimated cost: 62 core-hours per instance with the numpy code as measured.
    That is 2–3 hours on 30 free cores, and a compiled implementation would
    likely be several times faster. A full run was started and then stopped
    because other jobs were loading the machine (load average about 60).
  - Without U, each pattern needs a global continuous certificate. Generic
    spatial branch and bound does not deliver one in 600 s, and IEP from the
    a-priori box stalls at 1.146, so exhaustive certification is out of reach.

## 5. Improved primal points (60-digit check against all OSiL rows)

`code/verify_primal.py`; the points are stored in `runs/primal_verified.json`.
The patterns come from swap local search (`code/localsearch.py`).

| instance | objective found | listed primal | max row violation |
|---|---|---|---|
| nuclearva | -1.01430486 | -1.01423116 | 8.0e-57 |
| nuclearvb | -1.03234402 | -1.03133586 | 6.7e-59 |
| nuclearvc | -1.00484715 | -1.00484715 (same) | 2.7e-58 |
| nuclearvd | -1.04207854 | -1.04164538 | 6.0e-58 |
| nuclearve | -1.03982168 | -1.03764054 | 2.1e-58 |
| nuclearvf | -1.02453142 | -1.02408746 | 7.3e-57 |
| nuclear14 | -1.12970962 | -1.12968744 | 1.0e-56 |

Variable bound violations are 0 and all binaries are exactly 0 or 1. The values are
the 60-digit equilibrium of the stated pattern, rounded; the stored points are
decimal strings, not exact rationals.

## 6. Open questions worth a separate task

- **U itself.** Uniqueness of the equilibrium cycle for fixed reload patterns
  is widely assumed in the core-reload literature. A proof for these models
  would be a clean result on its own. Section 4 lists the candidate routes.
- **Stronger coupled relaxations.** Could a relaxation keep all `T` eigen
  equations together with pattern-dependent reactivity ordering and close the
  leaf gap from 13% to below 1%? Gurobi's fixed-pattern run suggests that
  spatial branching on the continuous state converges, but slowly.
- **The F3 variants (14b, 25b, 49b, 10b).** They let reload lower reactivity.
  Whether `z = k_T` is always optimal is unproven.

## 7. Files and commands (targeted local checks only; no CI results are involved)

The Python interpreter is `~/miniconda3/envs/exact-quadratic-hull/bin/python`.
Commands run from `code/`:

- `nucmodel.py nuclearva ... nuclear14b`: exact regeneration of the rows (9 instances).
- `reform.py nuclearva|nuclear14a|nuclear14b|nuclear14 1`: 60-digit round trip.
- `symmetry.py ...`: automorphisms and pattern counts (`runs/symmetry.txt`).
- `localsearch.py <va..vf> 6 {1,2,3}` and `localsearch.py nuclear14 2 1`:
  primal patterns.
- `uniqueness.py nuclearva 30 20 5`, `nuclearvc 30 20 6`, `nuclear14 10 10 7`.
- `grb_power.py nuclearva 600 <pattern> 4`
  (`runs/grb_power_va_fixed.log`).
- `iep.py`, `nodebounds.py nuclearva|nuclear14 best`, `rootiep.py ...`,
  `b4root.py <name> 1800 2`.
- `enum_batch.py nuclearva sample 20000 {11,21..26}` and
  `enum_batch.py nuclearvd sample 20000 {31,32}`.
- `verify_primal.py nuclearva ... nuclearvf nuclear14`.
