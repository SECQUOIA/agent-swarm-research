# Multi-attribute single-pool single-output pooling hulls: feasibility, novelty, impact

## Corrections after independent verification

An [independent verification](verification.txt) (scripts `code/indep_bound.py`,
`code/gen_points.py`, `code/check_author.py`, `code/check_indep_points.py`; logs in
`code/out/verify/`) rebuilt the relaxation from the original files and found:

- The added constraints are valid. The "valid" bounds come from an LP outer
  approximation (piecewise McCormick on a 46-point grid, joined disjunctively),
  not from the second-order-cone extended formulation or the exact hull. 130
  (sppb0pq) and 150 (sppc0pq) feasible points, including MINLPLib's solutions,
  satisfy the LP up to 5.7e-10. The rebuilt model contains every original row.
- Safe bounds (Neumaier–Shcherbina correction): sppc0pq -93325.2208, sppb0pq
  -45046.1011; the values reported below (-93442.92, -45047.42) are weaker and
  also valid.
- The MINLPLib baselines quoted below were wrong: the best listed dual bounds
  are Gurobi's (updated August 2025), not BARON's. The instances exist only as
  pq, stp and tp variants.
- **sppb0: claim refuted.** Listed Gurobi bounds -44564.92 (tp), -44775.36 (stp),
  -44853.09 (pq) are all better than -45046.10.
- **sppc0: confirmed with a smaller margin.** The best listed bound is -95124.69
  (tp; -95824.43 on the pq page); the safe bound -93325.22 beats it by about
  1799, and the gap to the best known solution (-87925.00) falls from 8.19% to
  6.14%. The Alfaki–Haugland (2013) values quoted below were not rechecked.


Date: 2026-09-23. Status: scouting assessment with numerical experiments. No theorem
is claimed. Bounds are labeled by how they were computed (Section 4.1):

- **valid:** a lower bound on the relaxation, hence on the pooling optimum;
- **inner:** a restricted-hull estimate, which can only overstate the bound.

All computations use floating-point LPs (Gurobi 13); none uses exact arithmetic.

## 1. Bottom line

- **Literature.** From 2019 to 2026, no paper was found that gives a convex hull or a
  dedicated strong relaxation of a single-pool single-output pooling set with two or
  more attributes. The literature does not pose it as an open problem either. The
  stated open directions are:
  - Luedtke et al. (2020): disaggregated input variables, or several pools.
  - Gupte et al. (2017): valid inequalities for the single (output, attribute) set.
    Luedtke et al. later solved that case.
- **Math.**
  - The aggregated multi-attribute set `T^K` has a simple extreme-point structure. The
    curved part is `x = min_k phi_k(t_k)`, where each `phi_k` is Luedtke's hyperbola.
    The minimizing attribute is the binding one, and a ridge appears where two
    attributes bind together.
  - `conv(T^K)` is strictly smaller than the intersection of the per-attribute Luedtke
    hulls.
  - For `K = 2`, with box data and one bypass quality, the hull is numerically the
    convex hull of nine explicit pieces: points, polytopes, and hyperbolic arcs. This
    gives a compact second-order-cone (SOC) extended formulation for fixed `K`.
  - A Luedtke-style closed form in the original variables looks case-heavy. None was
    found.
- **Impact.** In practice, what matters is the attribute correlation: the pool's
  quality vector lies in the polytope spanned by its input quality vectors. With this
  single-pool single-output hull added to the pq relaxation, the root bound closes:

  | Instance | Root gap closed | Earlier dual bound (A&H 2013 / MINLPLib) | New root bound (valid) |
  |---|---|---|---|
  | `pooling_sppc0pq` | 51% | −96256.99 / −97328.57 | **−93442.92**; remaining gap to the best primal falls from 9.5% to 6.3% |
  | `pooling_sppb0pq` | 20% | −45179.93 / −45318.86 | **−45047.42**; remaining gap falls from 4.1% to 3.8% |
  | `pooling_sppa0pq` | 50% | – | does not beat the best known dual bound |

  A&H 2013 is Alfaki and Haugland (2013). Both earlier sppc0/sppb0 bounds come from
  branch and bound, not the root. Per-attribute Luedtke hulls close 0–0.6% on sppa0, sppa5 and sppb0
  (not run on sppc0). On sppa0, single-attribute sets close at most 13%, and the box
  (uncorrelated) multi-attribute set closes at most 4.3%. The gain is small on sppa5
  (1.9%) and on Luedtke's two-attribute random Haverly instances (mean 1 point).
- **Recommendation: GO, with a changed target.** Do not aim for a closed-form hull of
  the box-data `T^2`; it has little practical value. Instead:
  1. Consolidate the computational result: a safe, verified dual bound for
     sppc0/sppb0 and a scalable separation routine.
  2. Develop the theory for the polytope-data (correlated) set: extreme points and a
     compact SOC extended formulation for fixed `K` or for 2-input pools.

  The repository already has the exact linear-optimization oracle (the common-factor
  theorem, Section 2). New work must supply the hull description and the
  computational result.

## 2. Literature, 2019–2026

Sources searched: the local KB (grep over `literature/papers/*/paper.md` and
`fulltext.md`); web, arXiv API, OpenAlex and Semantic Scholar searches for papers
citing Luedtke et al. (2020).

| Work | What it covers | Multi-attribute hull? |
|---|---|---|
| Luedtke, D'Ambrosio, Linderoth, Schweiger, SIOPT 30(2) 2020 | Hull of the 5-variable set `T` (one pool, one output, one attribute, aggregated inputs): 2 linear + 2 convex nonlinear inequalities, exact in three parameter cases | No; each attribute separately |
| Gupte, Ahmed, Dey, Cheon, JOGO 2017 | pq equals the intersection of single-pool hulls; Lagrangian bound LAG3 via an exponential LP (all pools' `q` at simplex vertices), small instances only | No hull; LAG3 captures some multi-attribute strength (Section 4.2) |
| Dey, Kocuk, Santana, JOGO 77 2020 | Rank-one sets with linear side constraints (polyhedral hull if `A^k = alpha_k beta^T`, `beta > 0`; SOC hull for two arbitrary side constraints); source/terminal pooling relaxations | Partial: quality rows with bypass flows do not fit Theorem 1; Theorem 2 allows only two side constraints |
| Jalilian, Kocuk, Optim. Eng. 27 2026 (arXiv 2306.10810) | SOC hull of nonnegative rank-one matrices with bounded row, column and total sums; OBBT | No quality constraints |
| Ceccon, Misener, Comput. Chem. Eng. 2022 (GALINI) | Luedtke cuts per (pool, output, quality) triplet at scale | No |
| Khademnia, Davarnia, Math. OR 2024 | Hull of `z_ij = x_i y_j` with `x` in a network polytope and `y` in a simplex; explicit facets for a single `y` | Related to 2-input pools; no quality side constraints |
| Chen, Maravelias, Zhang (2021, 2023) | Bounds on bilinear terms; tighter discretization MILPs | No |
| Oh, Wiecek, Yang, SIAM OP26 abstract | Box sets with bilinear inequalities sharing a common variable; claims extreme points, facets and separation | Possible overlap with the box, fixed-bypass `T^K` case (abstract only) |
| Boland, Kalinowski, Rigterink, JOGO 2017 | One pool with a fixed number of inputs: polynomial optimization by cell enumeration | Optimization, not a hull |
| Boland et al. 2016; Alfaki and Haugland 2013 | MCF and STP formulations; root and BARON bounds on sppA/B/C | Used as bound baselines (Section 4.4) |

- Searches for "Marandi", "Grimstad and Knudsen" and "multivariate pooling set" found
  no relevant hull results. The Marandi–Dahl–de Klerk pooling papers evaluate
  sum-of-squares hierarchies.
- The Khajavirad and Dey–Kazachkov–Lodi–Muñoz lines work on multilinear, cutting-plane
  and V-polyhedral topics. No pooling-specific multi-attribute sets were found there.

Stated open directions, summarized:

- Luedtke et al. (2020), Section 6: stronger pooling relaxations may require richer
  substructures. For a fixed attribute k, output j, and pool ℓ, they suggest retaining
  the individual variables x_ij, w_iℓj, and q_iℓ for i ∈ I instead of aggregating them
  into z_iℓ, t_kℓ and u_kℓj. They also suggest studying several pools together while
  keeping the summary variables.
- Gupte et al. (2017), Section 3.2: they leave open whether valid inequalities for
  the set associated with a fixed j ∈ J and k ∈ K can strengthen the PQ lower bound.
- Luedtke et al., Section 5.3: their instances omit lower concentration bounds, but
  they suggest sampling such bounds and separating them by an analogous procedure.
  They treat each lower bound as a separate attribute.

So the multi-attribute case is unstudied rather than explicitly posed.

**Repository overlap.**

- `results/pooling-*.md` are complexity results. The one-pool hardness results
  (`pooling-one-pool-bypass-*.md`) concern several outputs. Our substructure has a
  single output, so there is no conflict.
- `results/common-factor-fixed-linking-optimization.md` does apply. The single-pool
  single-output set is a common-factor set: the scalar `x` multiplies the leaves `q`,
  and the linking rows are the `K` quality rows plus capacity rows.
  - Its Theorem 1 and Corollary 1b give exact polynomial linear optimization over the
    set for fixed `K`. Hence separation over the hull is polynomial via the ellipsoid
    method.
  - The oracle is therefore not new. The pricing used below (a 1-D branch and bound on
    `x`) is a practical version of the same observation: for fixed `x`, the set is a
    polytope.

## 3. Target sets and the mathematics

With capacity `C = 1`: `x` is the pool→output flow, `z` the bypass flow, `t in R^K`
the pool excess qualities, `u = x t`, and `y` the bypass excess.

- `T^K(P, B) = {x, z >= 0, x + z <= 1, t in P, u = x t, y in z B, u + y <= 0}`.
  - **Abox:** `P` and `B` are boxes (the interval data of Luedtke's sets).
  - **Apoly:** `P = conv{gamma_i : i in I_l}` and `B = conv{gamma_b : bypass sources}`.
    This keeps attribute correlation.
- **D:** `{(x, q, w, v): q in simplex, w = x q, v >= 0, x + sum v <= C_j,
  Gamma w + Gamma_b v <= 0}`. This is Luedtke's suggested disaggregation, with all
  attributes.
- **L1** and **D1:** the single-attribute versions. L1 is Luedtke's set.

Inclusions:

- `D` maps into `Apoly`, `Apoly ⊆ Abox`, and `Abox ⊆` the intersection over `k` of
  `L1_k`.
- `D ⊆` the intersection over `k` of `D1_k`, and `D1` is at least as strong as `L1`.

All computed numbers respect these inclusions.

### 3.1 Extreme points (box data, one bypass quality `beta < 0`)

For fixed `t`, the fiber in `(x, z)` is a polygon with vertices `(0,0)`, `(0,1)`, and
`(x*(t), 1 - x*(t))`, where

`x*(t) = min(1, min_k phi_k(t_k))` and `phi_k(t) = -beta_k / (t - beta_k)`.

On the curved part, the point is affine in every non-binding `t_{k'}`. Hence the
extreme points of `conv(T^K)` lie on these pieces:

- the two `t`-boxes at `x = 0`;
- the face `x = 1`;
- for each binding `k`, the arc `x = phi_k(t_k)`, with every other `t_{k'}` at a bound
  or on a ridge;
- the ridges where several attributes bind. On a ridge, `t_k = -beta_k (1 - x)/x` and
  `u_k = -beta_k z`: a planar hyperbola.

**Numerical check for `K = 2`** (`code/pieces_k2.py`). The support function of the
sampled nine pieces was compared with Gurobi's exact `max c.p` over `T^2`, on 400
directions across 10 random instances. The maximum discrepancy is 4.0e-3 with 400
samples per arc and 1.5e-4 with 4000 samples. It shrinks with refinement, which is
consistent with equality.

**Consequences.**

- Each piece is SOC-representable, so disjunctive programming gives a compact SOC
  extended formulation.
- For general `K`, the number of pieces grows like `3^K`: each non-binding attribute
  sits at its lower bound, at its upper bound, or binds.
- Polytope data `P` adds pieces along the faces of `P`.
- For a 2-input pool, `t` moves on a segment, so the set has one bilinear term and all
  pieces are again hyperbolic arcs.

### 3.2 The hull is strictly smaller than the per-attribute intersection

Setup (`code/local.py`, `K = 2`, 60 random directions per case):

- Relaxation: McCormick/pq plus the per-attribute exact hulls. The hulls are
  grid-inner-approximated, so strict gaps are certified.
- Reference: exact `max c.p` over `T^2`, computed by Gurobi.

| Data family | Cases with a strict gap | Mean share of the McCormick-to-hull gap left by per-attribute hulls |
|---|---|---|
| Box `P`, box `B` (20 cases) | 16 | 29% |
| Random 3-input polytope `P` (20) | 12 | 17% |
| One quality, two-sided spec (`t2 = d - t1`; 20) | 3 | 0.2% |
| Box `P`, single bypass `beta` (`local_simple.py`; 16) | 15 | 20–61% per case |

A two-sided specification of a single quality nearly decomposes. Genuinely different
attributes do not.

### 3.3 Feasibility of a theory result

- **Likely provable in weeks:**
  - the extreme-point characterization for box and polytope data;
  - "hull = conv of an explicit finite union of SOC pieces", with a compact extended
    formulation for fixed `K`;
  - an explicit arc list for 2-input pools.
- **Uncertain:** a Luedtke-style closed form for `K = 2`. The single-attribute case
  already needed three parameter cases. The ridge adds an arc, and bypass boxes add
  `y`-endpoint patterns.
- **Novelty risks:**
  - The oracle is in the repository.
  - The disjunctive "union of pieces" argument is standard.
  - Oh–Wiecek–Yang (2026) may cover the box, fixed-bypass case.
  - New would be the pooling-specific piece structure (ridges, correlated data) and
    the computational result.

## 4. Practical impact

### 4.1 Method

Every relaxation is the pq McCormick LP with the pq reduction constraints, plus, for
every pool→output arc `(l, j)`, the hull of the chosen local set. The local
coordinates are exact linear maps of pq variables. Upper and lower specifications are
both attributes.

- **DW (valid, and an inner estimate).** Dantzig–Wolfe column generation with exact
  pricing. For fixed `x`, the block is an LP; a 1-D spatial branch and bound on `x`
  with McCormick LPs certifies each pricing minimum. The Lagrangian value
  `master + sum_b min(0, min reduced cost)` is valid. The final master value is an
  inner estimate. See `instance.py` and `certify.py`.
- **Outer LP (valid).** `gridrelax.py ... outer` splits `[0, XU]` into intervals and
  applies McCormick on each interval. Every block point lies in one piece, so the
  disjunctive LP is a relaxation. It converges as the grid refines.
- **Grid LP (inner).** The same construction, using slices at fixed `x` instead of
  intervals. The slices lie inside the hull, so the LP can only overstate the bound.
  This gives an upper bound on a relaxation's gap closure; it is how D1 and Abox are
  bounded on sppa0.
- **Agreement.** Where several methods ran, they agree:
  - sppa0 D: DW [−36787.51, −36784.30]; outer −36789.73; grid −36774.39.
  - sppa5 D: DW [−28255.17, −28250.63]; outer −28251.40.
- **Validation.**
  - The pq bounds equal Luedtke et al.'s published `zpq` on the random Haverly instances.
  - L1 reproduces their `pq+` on haverly3 and adhya2–4, and is at least as strong
    as their cut-loop `pq+` on all 15 random single-attribute instances.
  - The rebuilt MINLPLib `spp` models account for every OSiL row: all capacity rows,
    quality rows, simplex rows and bilinear rows. They put no objective coefficient
    on `q` or `y`.
  - For sppa0, sppb0 and sppc0, the MINLPLib reference solutions are feasible in the
    rebuilt models and give identical objectives (`verify_spp.py`).

### 4.2 Literature instances (DW bounds, % of root gap closed)

`K` counts qualities. `rt2` has two-sided specifications, so 8 attributes.

| Instance | K | Root gap % | L1 (Luedtke) | D1 | Abox | Apoly | D | Gupte LAG3 |
|---|---|---|---|---|---|---|---|---|
| adhya1 | 4 | 39.4 | 48.7 | 49.5 | 49.0 | 54.5 | 54.5 | 52.2 |
| adhya2 | 6 | 3.8 | 11.7 | 18.1 | 16.3 | 42.6 | 42.6 | 35.7 |
| adhya3 | 6 | 1.8 | 6.2 | 27.2 | 13.5 | 34.7 | 34.6 | 45.4 |
| adhya4 | 4 | 9.5 | 6.9 | 58.6 | 63.9 | 76.7 | 76.7 | 72.8 |
| rt2 | 4 (8) | 37.4 | 17.5 | 17.4 | not converged | 17.5 | 17.5 | – |
| haverly3 | 1 | 6.7 | 16.7 | 16.7 | 16.7 | 16.7 | 16.7 | – |

- haverly1, haverly2 and bental4 are closed by every set; bental5 and foulds2 have no
  pq gap.
- The multi-attribute gain (D over the best single-attribute set) is +5 to +25 points
  on the adhya instances.
- Gupte et al.'s whole-pool Lagrangian LAG3 (their Table 2) has similar strength, but
  it needs an LP of exponential size.

### 4.3 Luedtke et al.'s random Haverly instances (10 copies; DW bounds)

Mean % of root gap closed; global optima from Gurobi. The `attr_1` instances have two
attributes.

| Set | L1 | D1 | Abox | Apoly | D | D − D1 |
|---|---|---|---|---|---|---|
| 15 single-attribute | 54.9 | 63.7 | 54.9 | 54.9 | 63.7 | 0 |
| 15 two-attribute | 46.1 | 52.0 | 48.0 | 51.4 | 52.9 | mean 0.95, max 6.2 |

Here the gain over Luedtke comes from disaggregation (D1 over L1: up to +33 points),
not from multiple attributes.

### 4.4 Open MINLPLib instances (pq formulation rebuilt from the OSiL files)

Attribute rows per output: 24 (sppa), 34 (sppb) and 40 (sppc). Each "best dual" is
the best over the pq/stp/tp variants in MINLPLib and Alfaki and Haugland (2013,
Table 4, 1 h BARON or their code).

| Instance | Root pq | Best primal | Best known dual | L1 | D1 | Abox | Apoly | D |
|---|---|---|---|---|---|---|---|---|
| sppa0pq | −37772.75 | −35812.33 | −36102.10 | −37760.80 (0.6%) | ≤ 13.2% (inner −37514.67) | ≤ 4.3% (inner −37687.61) | DW [−36789.63, −36786.09] (50.1–50.3%) | valid −36789.73; inner −36784.30 (50.1–50.4%) |
| sppa5pq | −28257.75 | −27915.84 | −28251.33 (A&H) | 0% | – | – | – | valid −28251.40; inner −28250.63 (1.9–2.1%) |
| sppb0pq | −45466.54 | −43412.41 | −45179.93 (A&H) | 0% (DW) | – | – | – | **valid −45047.42**; inner −45038.59 (20.4–20.8%) |
| sppc0pq | −99129.09 | −87925.00 | −96256.99 (A&H); −97328.57 (MINLPLib) | not run | – | – | inner −93679.41 (≤ 48.6%) | **valid −93442.92**; inner −93317.03 (50.8–51.9%) |

Reading the table:

- **Multiple attributes cause the gain.** On sppa0, D1 closes at most 13.2% and D at
  least 50.1%. Luedtke's per-attribute hulls close ≤ 0.6% on sppa0, sppa5 and sppb0
  (not run on sppc0). This
  matches their Table 4 finding that `pq+` barely helps on randstd-type instances.
- **sppb0 and sppc0: new dual bounds.** The valid root D bounds are better than every
  dual bound we found:
  - sppc0: by 2814 over Alfaki–Haugland and 3886 over MINLPLib.
  - sppb0: by 132.5.
  - Floating-point tolerance is far smaller than these margins.
  - The bounds apply to the stp/tp variants too, since they encode the same instance.
- **sppa0 and sppa5: no new dual bound.** On sppa0, branch and bound in the literature
  reaches −36102.10, above our root −36789.73. On sppa5, our bound equals Alfaki–Haugland's
  up to 0.07.
- **Caveats.**
  - The literature search for sppB/C bounds was not exhaustive; papers after 2016
    that report sppC0 bounds may exist.
  - These are floating-point LP values. A publishable claim needs a safe dual bound
    (Neumaier–Shcherbina correction) or an exact-rational recheck.
- **Cost.** The outer LPs took 218 s (sppa0), 1669 s (sppa5), 3545 s (sppb0) and
  1149 s (sppc0, 46 grid points), with 4-thread barrier, plus Python model building.
  Memory reached 10–13 GB on sppb0 and sppc0. A separation-based implementation would
  be needed in a solver.

### 4.5 Where the gain comes from

- **Large when:** pools have few inputs relative to the number of binding
  specifications (adhya: 2–3 inputs, 4–6 qualities; spp: 3–13 inputs, 24–40
  specification rows). The pool quality vector is then confined to a low-dimensional
  polytope that per-attribute intervals cannot express.
- **Small when:**
  - only the box data is used (Abox);
  - attributes are independent random add-ons (random Haverly `attr_1`);
  - on sppa5.

## 5. Recommendation

**GO**, re-targeted:

1. **First (computational note).**
   - Verify the sppc0 and sppb0 bounds safely: a Neumaier–Shcherbina safe dual bound
     on the outer LP, and an independent rebuild of the models from the MINLPLib
     GAMS files.
   - Extend to sppC1–C3 and sppB1–B5, and check post-2016 literature bounds.
   - If the bounds hold, improving the best known dual bounds of open MINLPLib pooling
     instances is a publishable result on its own.
2. **Then (theory).**
   - Extreme-point characterization of the correlated single-pool single-output set
     (`Apoly` and `D`).
   - The "finite union of SOC pieces" hull theorem, with a compact extended
     formulation for fixed `K`.
   - An explicit arc list for 2-input pools.
   - A cheap separation routine.
   - Credit the common-factor theorem and Dey–Kocuk–Santana. Check the full
     Oh–Wiecek–Yang paper when it appears.
3. **No-go** on a closed-form hull of the box-data `T^2` as the main goal: little
   practical value (Abox ≤ 4.3% on sppa0) and heavy case analysis.

Risks:

- The gain is instance-dependent: large on adhya, sppa0, sppb0 and sppc0; small on
  sppa5 and random Haverly.
- The oracle part is not new.
- The sppb0/sppc0 bounds need independent, safe verification before any claim.

## 6. Reproduction (targeted commands run)

All commands run in `code/`, with `PY=~/miniconda3/envs/exact-quadratic-hull/bin/python`.

Instance data:

- literature JSON from `github.com/cog-imperial/pooling-network`;
- random Haverly from `github.com/poolinginstances/poolinginstances`, converted with
  `convert_rh.py` into `rh/`;
- the published reference table, parsed into `random_haverly_reference.json`;
- MINLPLib OSiL files in `spp_data/`.

Commands:

- `$PY local.py 7 60` writes `local_60.jsonl` (Section 3.2). Also run:
  `$PY local_simple.py 3 16` and `$PY pieces_k2.py 5 10 4000`.
- `$PY instance.py <json|osil> [modes]` gives DW bounds (logs in `out/*.log`);
  `$PY summarize.py` writes `summary.json`.
- `$PY solve_global.py rh/*attr_1*.json` writes `out/rh_global.jsonl`.
- `$PY gridrelax.py spp_data/<inst>.osil <modes> <G> [outer]` gives inner and outer LPs
  (`out/grid_*.log`, `out/outer_*.log`).
- `$PY certify.py spp_data/<inst>.osil <mode> 30 <sec>` gives grid-seeded DW
  (`out/cert_*.log`). `stab.py` is a smoothed variant; it did not converge within the
  time used.
- `$PY verify_spp.py spp_data/<inst>.osil <minlplib .p1.sol>` checks the rebuild.

No project-wide checks were run. CI results are separate.
