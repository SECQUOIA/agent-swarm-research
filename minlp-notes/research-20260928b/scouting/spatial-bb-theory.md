# Scout report: spatial branch-and-bound theory beyond worst-case lower bounds

Area: `spatial-bb-theory`. Date: 2026-09-28. Status: scouting report with
first-pass proofs and small uncertified computations. Nothing here has been
independently reviewed. Scratch code and logs are in
[`spatial-bb-theory/`](spatial-bb-theory/).

## Summary

The repository already covers most of the named subareas: exponential node
lower bounds in the dimension at fixed tolerance, a cluster-free local count at
nondegenerate KKT points, iterated-OBBT contraction rates, FBBT hardness,
curvature-based convex covers, and two limit examples for singular equality
certification. The clearest missing piece is an **instance-dependent** theory
of node counts as a function of the tolerance `eps`. The cluster literature
gives only upper estimates. Du and Kearfott say explicitly that their count is
"an upper bound, and not a precise value". None of the sources checked gives a
lower bound on node counts for adaptive trees.

First-pass mathematics below proves a small, coherent package for relaxation
schemes whose pointwise gap is at least `alpha * sum_i (y_i-l_i)(u_i-y_i)` on
every box. This covers uniform alphaBB and secant relaxations of separable
concave quadratic parts. The package has four parts:

- **Integral lower bound (Theorem B).** Every box certificate has at least
  `(alpha n/pi^2)^(n/2) * integral (f-f*+eps)^(-n/2) dx` leaves. This holds
  for any split points, any node order and any valid incumbent. It also holds
  with OBBT or marginal reduction on the same relaxation.
- **Near-optimal sets (Theorem D).** A feasible set of dimension `p` on which
  `f <= f*+eta` forces `Omega(H^p(S) (alpha/(eps+eta))^(p/2))` leaves, with
  constraints allowed.
- **Bisection versus optimal (Theorem A).** Uniform bisection is within a
  factor `C_n log(1/eps)` of the optimal certificate. The log factor is
  attained at sharp minima.
- **Bisection matches the integral (Theorem C).** Under a quadratic-doubling
  regularity condition, bisection is within a constant factor of the integral,
  so for such instances all three quantities agree up to `e^{O(n)}` factors.

Together these recover the known rates: `log(1/eps)` at nondegenerate minima,
`eps^(-1/4)` in the quartic example of Kannan–Barton, and `eps^(-p/2)` for
`p`-dimensional optimal sets. They add, for the first time as far as the
bounded search found, **lower** bounds that hold for adaptive trees.

Numerical checks with a toy branch-and-bound agree with every predicted
exponent. They also show that the relaxation's gap-vanishing geometry matters.
For a McCormick relaxation whose gap vanishes on box faces, a 2-leaf
certificate exists, while widest-side bisection needs at least order
`eps^(-1/2)` nodes.

Recommended direction: Q1 below, the instance-dependent characterization,
extended to constrained problems and to an instance-optimal branching rule.
Score 6/10. The main risks are moderate originality, because the Lipschitz
analogue is known (Bachoc–Cesari–Gerchinovitz 2021), and moderate practical
impact.

## 1. Frontier map

### 1.1 Repository baseline (checked locally)

| Topic | Local result | Exact scope |
|---|---|---|
| Worst-case tree lower bounds | `results/spatial-bb-*-exponential-lower-bound.md` (7 notes) | `2^Omega(n)` leaves at a **fixed** gap for coordinate branching, for separable, SDP–RLT, higher SOS, product-domain, quadratic-cut, monomial-lift and relative-gap node oracles. Dense affine branching is outside the proof method (`notes/spatial-bb-affine-branching-barrier.md`). |
| Cluster problem | `results/cluster-free-branch-and-bound-constrained-minima.md` | Under KKT, LICQ, SC, SOSC and second-order pointwise convergence: `L(Z) >= f* + c1 dist(Z,z*)^2 - c2 w(Z)^2`. The number of unfathomed boxes **per fixed scale** is `O(1)`. This is a local count, not a total-tree bound, and not a lower bound. The core inequality is attributed to Anitescu (2005) and Bonnans–Shapiro. |
| OBBT | `research-20260922/iterated-obbt/theory.md` | Contraction theory of iterated OBBT: rates via a tangent map `r*`, stalls, and root gap `O(eps)`. There is no tree-size statement. |
| FBBT | `results/fbbt-monotone-system-hardness.md`, `results/fbbt-doubly-exponential-convergence.md` | PosSLP-hardness of approximating bilinear FBBT limits, and `2^(2^n-1)` primitive updates. |
| Convex covers | `research-20260928/solver/branching-curvature-atlas.md`, `branching-degeneracy-barrier.md` | **Uniform** epigraph cover count `Theta(eps^(-k/2))` with `k` negative eigenvalues and a positive spectral complement. Without the complement, count up to `~eps^(-n/2)`. The notes say explicitly that this is not a bound for branch-and-bound stopped after one objective bound. |
| Equality certification | `research-20260927/equality-frontier.md`, `notes/equality-frontier-literature-audit-2026-09-27.md` | Two limit examples: a non-robust even-multiplicity optimum with a fixed upper-bound gap, and a robust singular chain needing `delta <= eps^((2^k+1)/2)`. The broad theory is prior art (Franek–Ratschan–Zgliczynski; Kollár). A "checkable structural parameter" is listed as open. |
| Scouting | `research-20260922/scouting/scout_area23_bt_branch.md` | Ranked open items: iterated OBBT (since done), a spatial tree-size theory for branching rules, reduced-space propagation, **`eps`-dependent cluster lower bounds**, and affine branching. The latter two are not developed. |

### 1.2 External frontier (strongest results, with assumptions)

**(a) Convergent and certified upper bounds.**

- Füllner, Kirst, Stein, Math. Program. 187 (2021) 617–651.
  - Assumptions: equality and box constraints, `C^1` data, feasible points
    strictly inside the box, LICQ at every global minimizer, exact
    arithmetic.
  - Result: a Miranda test on a Jacobian-transformed, extended box eventually
    succeeds along nested exhaustive boxes, so the upper bounds converge and
    the method terminates finitely (Theorem 4.11, Corollary 4.12).
  - No rate is given. On COCONUT, 26 of 35 problems terminate.
- Füllner, Kirst, Otto, Rebennack, IJOC 36(6) (2024).
  - Extends the framework to inequalities through approximate active index
    sets, under LICQ at minimizers.
  - On 70 COCONUT problems, 42 terminate.
- Kirst, Füllner, COAP 90 (2025).
  - Restricts right-hand sides to `g <= -delta` in alternating box
    selection.
  - Assumes a local Slater condition at every global minimizer. Upper bounds
    converge and the method terminates finitely.
- Kirst–Stein, TOP (2015), "Deterministic upper bounds for spatial
  branch-and-bound…". Only the metadata was seen.
- Franek, Ratschan, Zgliczynski (FRZ), J. Autom. Reason. 57 (2016), as
  audited in `notes/equality-frontier-literature-audit-2026-09-27.md`:
  robust zeros of square systems are characterized by nonzero local degree
  (Theorem 6). Padded interval oracles cannot certify non-robust zeros
  (Lemma 8).
- **Gap.** No result characterizes when certified upper bounds can converge
  if LICQ or Slater fails. No result gives node or rate bounds for the
  certification step.

**(b) Convergence order and the cluster problem.**

- Du–Kearfott (1994).
  - Setting: interval extensions of order `alpha`, with the minimizer at a
    box vertex or in the interior.
  - Result: an **upper bound** on the number of boxes left. Order below 2
    "may" cause a severe cluster.
  - Remark 1 says explicitly that the theorem is an upper bound only.
- Wechsung–Schaber–Barton (2014).
  - Result: covering estimates for boxes of fixed width `delta`. Their
    Lemma 1 is a necessary condition under the *assumption* that the
    convergence-order bound is sharp.
  - Finding: a prefactor threshold for second-order schemes.
  - Assumption: boxes can be placed with the minimizer at the centre. They
    say that vertex placement would put an exponential number of boxes
    around the minimizer.
- Kannan–Barton (2017, 2018).
  - Result: conservative worst-case estimates in the constrained setting,
    and orders of lower-bounding schemes.
  - Open questions (2018 conclusion): neighbourhood second order, which the
    repository has bypassed, and reduced-space propagation conditions.
- Bompadre–Mitsos (2012) and Najman–Mitsos (2016): second-order pointwise
  convergence of McCormick and alphaBB relaxations.
- **Closest analogue outside MINLP:** Bachoc, Cesari, Gerchinovitz,
  "Instance-dependent bounds for zeroth-order Lipschitz optimization with
  error certificates", NeurIPS 2021, arXiv:2102.01977.
  - Setting: Lipschitz, black box, any `d`.
  - Result: the optimal number of evaluations for a certified algorithm is
    within log factors of `integral dx/(max f - f(x) + eps)^d`. The upper
    bound uses a certified version of DOO; the lower bound (their Theorem 2)
    uses a local adversary and loses `1/(1+log(eps0/eps))`.
  - This solves a 1991 question of Hansen–Jaumard–Lu for `d >= 2`. Their
    listed open problems concern constants, adaptivity to smoothness and
    randomization. They do not treat convex relaxations, second-order
    schemes, constraints or branch-and-bound box certificates.
- Dym, arXiv:2005.13728, "Quasi branch and bound for smooth global
  optimization": second- and third-order *upper* guarantees. Only the
  abstract was read.
- **Gap.** No rigorous lower bound on total tree size in `eps` for adaptive
  spatial branch-and-bound. No instance-dependent characterization for
  convex-relaxation schemes.

**(c) Branching-rule theory.**

- Belotti et al. (2009): no rule dominates.
- Speakman–Lee (2018) and follow-ups: volume-optimal branching points for
  trilinear hulls.
- Dey–Han–Wang, arXiv:2510.20650, extreme strong branching: empirical, with
  no theorems.
- Hübner–Gupte–Rebennack (IJOC 2026): finite versus limit convergence for
  piecewise-linear separable problems.
- Al-Khayyal–Sherali (SIAM J. Optim. 10, 2000) and Shectman–Sahinidis (1998):
  finite termination when branching at relaxation solutions for concave or
  bilinear classes. Only the metadata was seen; these are qualitative
  results.
- Learning: Ghaddar et al. (2023), González-Rodríguez et al. (2025,
  "myopic"), Berthold–Geis (2026). Cheng–Basu (2026) is the MILP theory of
  misleading local scores.
- **Gap.** "No tree-size guarantee is known for any spatial branching rule"
  (repository scout, 2026-09-22). No quantitative theory of branching-point
  placement.

**(d) Bound tightening.**

- Belotti et al. (2012): the FBBT fixed point, which an LP computes for
  linear systems.
- Caprara–Locatelli (2010) and Caprara–Locatelli–Monaci (2016): OBBT limits
  "can hardly" be guaranteed.
- Gleixner et al. (2017): OBBT alone gives no average speedup.
- Puranik–Sahinidis (2017): large node reductions from domain reduction
  across solvers, and a call for reduction that "avoids the cluster effect".
- The repository's iterated-OBBT theory gives rates.
- **Gap.** No theorem relates bound tightening to node counts. The first-pass
  corollary in Section 3.3 gives a partial answer.

### 1.3 Sources examined, and what was checked

Local files:

- The brief.
- `literature/topics/deterministic-global-minlp.md`: all.
- `literature/topics/open-theory-challenges.md`: Sections 2–4, the
  cross-cutting refinements, and all priority lists.
- `literature/topics/repository-claim-boundaries-2026-09-26.md`: the preview,
  including the cluster and OBBT paragraph.
- `results/cluster-free-branch-and-bound-constrained-minima.md`: all.
- The headers and scope of the seven `results/spatial-bb-*.md` and two
  `results/fbbt-*.md` notes.
- `notes/screen-cluster-problem-domain-reduction.md`: all.
- `research-20260922/scouting/scout_area23_bt_branch.md`: all.
- `research-20260922/iterated-obbt/theory.md`: the theorem list and
  Section 6.
- `research-20260922/iterated-obbt/experiment-report.md`: Sections 0–1.
- `research-20260928/solver/branching-curvature-atlas.md`: all.
- `research-20260928/solver/branching-degeneracy-barrier.md`: statement.
- `research-20260927/equality-frontier.md`: all.
- `notes/equality-frontier-literature-audit-2026-09-27.md`: all.
- `code/cluster_problem/README.md`.
- Grep of the local full texts of Du–Kearfott (1994), Wechsung et al.
  (2014), Kannan–Barton (2017) and Kannan's thesis (2018) for any lower-bound
  statement. None was found; the quotations above come from those files.
- Local summaries of Füllner et al. (2021, 2024) and Kirst–Füllner (2025).

Web sources:

- arXiv:2102.01977: abstract, and the full PDF text of Theorem 2 and the
  conclusions and open problems.
- arXiv:2005.13728: abstract only.
- Search-result metadata only for:
  - the Springer pages of Kannan–Barton 2017/2018;
  - Kirst–Stein TOP 2015;
  - Füllner et al. IJOC 2024;
  - Hübner et al. IJOC;
  - Al-Khayyal–Sherali 2000;
  - arXiv:2510.20650, 1706.08438, 2602.09996, 2406.03626, 2605.00855 and
    2308.00978.
- Two arXiv listing searches: "cluster problem branch and bound" (50 results)
  and "spatial branch and bound branching point" (39 results). Neither found
  a 2023–2026 paper on node-count lower bounds or instance-dependent
  spatial-branch-and-bound complexity.

Not examined:

- Schöbel–Scholz (J. Glob. Optim. 2010, a conservative worst-case iteration
  bound, known only through the Wechsung et al. citation).
- Neumaier (2004), Section 15, directly.
- Ratschek–Rokne and Csendes on interval branch-and-bound box counts.
- Hansen–Jaumard–Lu (1991), known only through Bachoc et al.

The web-search budget for this session ran out, and later arXiv queries
returned HTTP 429. **The novelty search is therefore incomplete. An
unsuccessful search does not establish novelty.** The interval-analysis
literature on box counts is the most likely place for close prior work.

## 2. Open questions

**Q1 (recommended). Instance-dependent node complexity of spatial
branch-and-bound.**

- Scheme: objective and constraint relaxations with pointwise gaps
  `alpha q_B <= gap_B <= alpha' q_B`, where
  `q_B(y) = sum_i (y_i-l_i)(u_i-y_i)`.
- Define `N_opt(eps)`: the minimum number of leaves of a box certificate,
  meaning a partition of the root box into boxes pruned at tolerance `eps`.

(a) Prove that, for constrained problems whose near-optimal feasible set has
a regular stratification into smooth strata `S` with transversal
nondegeneracy,

```
N_opt(eps)  ≍  sum over strata S of  integral_S (f - f* + eps)^(-dim S/2) dσ,
```

up to factors depending only on `n`, the scheme constants and the
conditioning of the strata.

where 0-dimensional strata contribute `O(1)`. Also prove that uniform
bisection attains this within `C_n log(1/eps)`.

(b) Find a *local* branching-point rule, meaning one computed from node
relaxation data such as safeguarded splitting at the relaxation minimizer,
whose tree size is at most `C_n N_opt(eps)` on every instance. This would
remove the log factor of Theorem A. Alternatively, prove that no local rule
can achieve this.

Evidence that Q1 is open:

- The cluster papers give only upper or worst-case estimates (quoted in 1.2).
- The repository's screen says "No lower bounds on node counts exist in this
  literature".
- Bachoc et al. treat Lipschitz black-box evaluation only.

The unconstrained and feasible-stratum parts are proved below (Theorems A–D).
The general constrained upper bound and part (b) are not.

**Q2. Gap-vanishing geometry and branching points for face-exact
relaxations.**

- Setting: McCormick, multilinear-envelope and secant relaxations in lifted
  coordinates are exact on box facets (or on vertices), so Theorem B does not
  apply.
- Question: characterize `N_opt(eps)` in terms of how the near-optimal set
  aligns with coordinate hyperplanes, and bound the loss of widest-side
  bisection and of practical rules. The practical rules to cover are SCIP's
  convex combination of the relaxation value and the midpoint, violation
  transfer, and splitting at the relaxation solution.

Specific conjectures:

- For a `p`-dimensional optimal stratum transversal to all coordinate
  hyperplanes, McCormick certificates also need `Omega(eps^(-p/2))` leaves.
- For axis-aligned strata, certificates of size `O(1)` exist, while
  widest-side bisection needs `Theta(eps^(-p/2))`. This is proved by the
  example in Section 3.7 for `p = 1`.
- No node-local rule is within `polylog(1/eps)` of optimal on all instances,
  by analogy with Cheng–Basu (2026) for MILP scores.

Evidence that Q2 is open: branching-point theory consists of volume criteria
(Speakman–Lee), qualitative finiteness results (Al-Khayyal–Sherali;
Shectman–Sahinidis) and empirical studies. Wechsung et al. and Kannan–Barton
treat vertex placement of minimizers as the *bad* case, because many boxes
then contain the minimizer. Theorem A's tightness example and Section 3.7
show that, for relaxations exact on faces or vertices, vertex placement can
be what makes a certificate small.

**Q3. Convergent certified upper bounds beyond LICQ.**

Conjecture: certified-incumbent spatial branch-and-bound can have convergent
upper bounds from an interval oracle **if and only if** `f*` equals the
infimum of `f` over *robust feasible points*. A robust feasible point is one
where, after fixing some `n-m` coordinates, the active equality system has an
isolated zero of nonzero local Brouwer degree, in the Franek–Ratschan–
Zgliczynski sense.

A proof would give:

- A degree-based verifier. Strict Poincaré–Miranda conditions on a box
  imply local degree `±1`, so Miranda-type tests, even after affine
  transformations, cannot certify an isolated zero of even degree. An
  example is the degree-2 zero of `h = (x^2-y^2, 2xy)`, which is robust.
- Convergence under this condition. The condition is weaker than LICQ and
  covers complementarity equalities `x y = 0`, whose non-robust corner is
  approached by robust points `(0, c)`.
- A bound on nodes until certification in terms of a robustness margin.
- The converse, by an interval-oracle adversary extending FRZ Lemma 8 and
  Proposition 1 of `research-20260927/equality-frontier.md`.

Evidence that Q3 is open: all convergence theorems assume LICQ or local
Slater (1.2(a)). The repository's equality notes give only obstructions and
state that a positive structural criterion is open. Caution: FRZ already
supplies the topological core, so the MINLP contribution would be the
integration, the handling of non-square systems and the quantitative
analysis.

Bound tightening (area d) needs no separate question. Corollary 3.3 shows
that tightening with the same relaxation cannot change the `eps`-exponent.
The remaining question, whether tightening that uses *different* information
(interval FBBT on the objective DAG, KKT-based OBDR) can change exponents, is
recorded under Q1 as a secondary item.

## 3. First-pass mathematics for Q1

All proofs below are first-pass derivations by this scout, without
independent review.

### 3.1 Model

- Root box `X0 = prod [L_i,U_i]` in `R^n`.
- Problem: `min f` over feasible `F subset X0`, with optimal value `f*`.
- For a box `B = prod [l_i,u_i] subset X0`, write
  `a_i(y) = (y_i-l_i)(u_i-y_i)` and `q_B(y) = sum_i a_i(y)`.
- A node relaxation uses an objective underestimator `f_B <= f` on `B` and
  any valid relaxation of `F`.
- **Gap hypothesis (G_alpha):** `f(y) - f_B(y) >= alpha q_B(y)` on `B`.
- Examples of (G_alpha):
  - Uniform alphaBB, `f_B = f - alpha q_B`.
  - A DC split `f = g - sum_i c_i y_i^2` with `g` convex and `c_i >= alpha`,
    relaxed by `g` plus the secants of `-c_i y_i^2`. The gap is
    `sum_i c_i a_i`.
  - Any weaker relaxation of either scheme.
- Counterexamples: interval-Hessian alphaBB with box-dependent `alpha_B` that
  tends to 0 on locally convex boxes, and McCormick (Section 3.7).

**alpha-valid family.** A finite family `P` of boxes with disjoint interiors
is alpha-valid at tolerance `eps` if it covers `X0` and, for every `C` in `P`
and every **feasible** `y` in `C`,

```
f(y) - f* + eps >= alpha q_C(y).                                   (V)
```

**Lemma 0.** Consider any spatial branch-and-bound run under (G_alpha) that
terminates at tolerance `eps`. It may use:

- arbitrary axis-parallel splits;
- any node order;
- any incumbent `UBD >= f*`;
- pruning by bound or by infeasibility;
- feasibility-based reduction that removes only infeasible points;
- OBBT or marginal reduction whose objective cutoff uses (G_alpha)
  underestimators.

Split each removed L-shaped region into at most `2n` boxes. Then the leaves
together with the removed pieces form an alpha-valid family. The number of
relaxations solved is at least `|P|/(2n+1)`.

*Proof.* Take a leaf `C` pruned by bound and a feasible `y` in `C`. Then `y`
is relaxed-feasible, so `f_C(y) >= UBD - eps >= f* - eps`, and (G_alpha)
gives (V). Take a piece `S` removed from a node `B` by objective-based
reduction and a feasible `y` in `S`. Then `f_B(y) > f* - eps`, so
`f(y) - f* + eps > alpha q_B(y) >= alpha q_S(y)`, because `S subset B`
implies `q_S <= q_B` on `S`. Pieces with no feasible point satisfy (V)
vacuously. Each processed node yields at most `2n` pieces plus itself or its
two children. □

### 3.2 Theorem B (integral lower bound, unconstrained)

Let `F = X0`. Every alpha-valid family satisfies

```
|P|  >=  (alpha n / pi^2)^(n/2) * integral_{X0} (f(y) - f* + eps)^(-n/2) dy.
```

*Proof.*

1. On `C` in `P`, condition (V) gives
   `(f-f*+eps)^(-n/2) <= (alpha q_C)^(-n/2)`.
2. By AM–GM, `q_C >= n (prod_i a_i)^(1/n)`, so
   `q_C^(-n/2) <= n^(-n/2) prod_i a_i^(-1/2)`.
3. Each factor integrates to the arcsine integral
   `integral_l^u ((t-l)(u-t))^(-1/2) dt = pi`. This value does not depend on
   `u-l`.
4. Hence `integral_C (f-f*+eps)^(-n/2) <= (pi^2/(alpha n))^(n/2)` for
   **every** box, whatever its shape.
5. Sum over `C`. □

Remarks:

- **Anisotropic alpha.** With gap `sum_i alpha_i a_i`, the constant becomes
  `(n/pi^2)^(n/2) prod_i alpha_i^(1/2)`.
- **Low-rank nonconvexity.** Suppose the gap involves only a coordinate set
  `K` with `|K| = k`. Slicing the partition at fixed values `z` of the other
  coordinates gives
  `|P| >= (alpha k/pi^2)^(k/2) sup_z integral (f(y,z)-f*+eps)^(-k/2) dy`.
  If only `K` is branched, the problem reduces exactly to the value function
  `v(y) = min_z f(y,z)` in `k` dimensions.
- **Exact finite certificates.** A certificate at `eps = 0` requires
  `integral (f-f*)^(-n/2) < infinity`. The integral is finite at sharp
  minima and infinite at nondegenerate smooth minima.

### 3.3 Theorem D (near-optimal sets, constraints allowed)

Setting:

- `S subset F` is `p`-dimensional and `f <= f* + eta` on `S`.
- Regularity: `H^p(S ∩ Q) <= c_S l^p` for every cube `Q` of side `l <= l0`.

Then for `eps + eta <= alpha l0^2/4`, every alpha-valid family satisfies

```
|P|  >=  H^p(S) * (alpha / (4 (eps + eta)))^(p/2) / (2^n c_S).
```

*Proof.*

1. Take `y` in `S ∩ C`. Condition (V) gives `eps + eta >= alpha a_i(y)` for
   every `i`.
2. Also `a_i(y) >= d_i(y)^2`, where `d_i(y)` is the distance from `y_i` to
   the nearer endpoint `l_i` or `u_i`.
3. So `d_i(y) <= r := ((eps+eta)/alpha)^(1/2)` in **every** coordinate, and
   `y` lies within sup-norm distance `r` of one of the `2^n` vertices of
   `C`.
4. Hence `H^p(S ∩ C) <= 2^n c_S (2r)^p`.
5. Sum over `C`, using subadditivity. □

Corollary (bound tightening). By Lemma 0, the bound holds for any branching
rule and node order, with FBBT that removes infeasible points, and with OBBT
or marginal reduction built on the same (G_alpha) relaxation. The number of
relaxations solved is at least the bound divided by `2n+1`. In this model,
**bound tightening cannot change the `eps`-exponent.**

This fits the repository's experiment finding that iterated OBBT did not pay
off on MINLPLib QCQPs. It is not an explanation of that finding. Tightening
that uses different information, such as interval evaluation of `f` or KKT
exclusion, is outside the corollary.

The integral version for a stratum `S` of dimension `d`,
`|P| >= c integral_S (f-f*+eps)^(-d/2) dσ`, is proved in two cases:

- **Axis-aligned strata** (for example active variable bounds): AM–GM on the
  `d` free coordinates gives constant `(alpha d/pi^2)^(d/2)`.
- **Flat or bounded-curvature strata, cubes of bounded aspect ratio
  `rho`:** use `q_C >= (s_min/2) dist_1(y, vertices of C)`. The integral of
  `dist^(-d/2)` over `d` dimensions converges at the vertices.

The case of arbitrary boxes with non-aligned strata is **open**. The key
lemma would be that `integral_{S∩B} q_B^(-d/2) dσ <= C(n,d,S)` for every
box `B`.

### 3.4 Theorem A (bisection is within a log factor of optimal)

Setting:

- `X0` is a cube of side `s0`, and `F = X0`.
- Two-sided gaps: `alpha q_B <= f - f_B <= alpha' q_B`, with
  `kappa = alpha'/alpha`.
- `T_bis` is uniform dyadic refinement with incumbent `f*`, which makes the
  processed set independent of node order. The binary widest-side bisection
  used in the computations generates the same cubes at every `n`-th level.

Then for every alpha-valid family `P`,

```
|T_bis| <= 1 + 4^n (sqrt(kappa n) + 4)^n * J_eps * |P|,
J_eps = max(0, ceil(log2(s0 sqrt(alpha' n/(4 eps))))).
```

*Proof.*

1. At level `j`, cubes have side `s_j`. Let `Q_j = n s_j^2/4`.
2. A non-pruned cube `D` contains some `y` with
   `f(y) - f* + eps < alpha' q_D(y) <= alpha' Q_j`. This forces
   `s_j > 2(eps/(alpha' n))^(1/2)`, so at most `J_eps` levels occur.
3. Let `C` in `P` contain `y`. Condition (V) gives `a_i^C(y) <= q_C(y) <
   kappa Q_j`. Since `a_i >= d_i^2`, `y` is within sup-norm distance
   `(kappa Q_j)^(1/2)` of a vertex of `C`.
4. Therefore `D` lies in a cube of radius `s_j((kappa n)^(1/2)/2 + 1)` around
   that vertex. At most `(sqrt(kappa n)+4)^n` level-`j` cubes meet such a
   cube, since an interval of length `2R` meets at most `2R/s_j + 2` grid
   cells.
5. Charge each non-pruned `D` to the pair (`C`, vertex). Each processed node
   has at most `2^n` children. □

**The log factor is attained.**

- Instance: `f(y) = 2|y-a| - (y-a)^2` on `[0,1]`, `a = 1/3`, exact alphaBB
  with `alpha = 1`.
- Optimal certificate: `{[0,a], [a,1]}`. On `[a,1]` the relaxation equals
  `(y-a)(1+a) >= 0`, and on `[0,a]` it equals `(a-y)(2-a) >= 0`. So
  `N_opt = 2` for every `eps >= 0`, including `eps = 0`.
- Bisection: `a` sits at relative position 1/3 or 2/3 in every dyadic
  interval, so the lower bound is at most `-(2/9)s_j^2`. Bisection needs
  `Theta(log(1/eps))` nodes.
- Splitting at the relaxation minimizer, which is exactly `a`, gives 3 nodes.

This refines the Wechsung–Schaber–Barton and Kannan–Barton view. For
relaxations that are exact at vertices, putting the minimizer on a vertex is
optimal at sharp minima.

### 3.5 Theorem C (bisection matches the integral under quadratic doubling)

Assume the same setting as Theorem A. Write `m = f - f*`. Assume

```
(QD)  m(x) <= K (m(y) + |x-y|_inf^2)   for x, y in X0.
```

Condition (QD) holds with `K = max(2, M)` when `m >= 0` has an
`M`-Lipschitz gradient on a neighbourhood where `m >= 0` persists. The reason
is that `|grad m(y)|^2 <= 2 M m(y)`. It holds for polynomial growth with
exponents at least 2, and fails at sharp minima. Then

```
|T_bis| <= 1 + 2^(n+1) Lambda^(n/2) integral_{X0} (m + eps)^(-n/2),
Lambda = K(alpha' n/4 + 1) + alpha' n/4.
```

*Proof.*

1. A non-pruned level-`j` cube lies inside `{m + eps <= Lambda s_j^2}`. This
   follows from (QD) and `eps < alpha' Q_j`.
2. So the level-`j` count is at most `V(Lambda s_j^2)/s_j^n`, where `V(t)`
   is the volume of `{m + eps <= t}`.
3. Sum over dyadic shells of `m + eps` and exchange the order of summation
   against the geometric series `sum_{j<=k} s_j^(-n) <= 2 s_k^(-n)`. □

With Theorem B, for (QD) instances:
`N_opt ≍ |T_bis| ≍ integral (f-f*+eps)^(-n/2)`. Both hidden constants are
`e^{O(n)}` and independent of `eps`.

### 3.6 Consequences (rates), unconstrained and (QD) unless stated

The consequences follow by evaluating `I(eps) = integral (f-f*+eps)^(-n/2)`
near the near-optimal set.

| Near-optimal structure | `N_opt` and bisection | Source of the lower bound |
|---|---|---|
| `r` isolated nondegenerate minimizers, curvature `gamma` | `Theta(log(1/eps))`. The lower bound grows like `r (c alpha/gamma)^(n/2) log(1/eps)`, so it is exponential in `n` when `alpha/gamma` exceeds a constant. | Theorem B |
| `p`-dimensional manifold of minimizers, Morse–Bott | `Theta(eps^(-p/2))`. The lower bound also holds with constraints (Theorem D). | Theorems B, D |
| Growth `sum_i |t_i|^(q_i)`, `q_i >= 2` | `Theta(eps^(-(n/2 - sum_i 1/q_i)))`, or `Theta(log(1/eps))` when the exponent is 0. This gives `eps^(-1/4)` for one quartic direction, matching the Kannan–Barton-type example B in the repository. | Theorem B |
| Sharp minimum, `m >= c|t|_1` on the root box, exact alphaBB | `N_opt <= (s0 alpha max(1, n/4)/c + 2)^n`, independent of `eps`. Use a grid of side `s = min(c/alpha, 4c/(alpha n))` with the minimizer at a grid vertex. Cells with that vertex have `q <= s|t|_1`; the other cells have `m >= c s >= alpha n s^2/4 >= alpha q`. Bisection needs `Theta(log(1/eps))` when the minimizer avoids dyadic points. | Theorem A (tight) |
| Low-rank nonconvexity, `k` branched coordinates | The `k`-dimensional integral of the value function `v` | slice remark |

The per-scale `O(1)` count of the cluster-free theorem is consistent with the
`log(1/eps)` total in the first row. The Wechsung–Schaber–Barton prefactor
threshold becomes the factor `(alpha/gamma)^(n/2)` in front of the log. The
dependence on `alpha/gamma` is not claimed to be tight.

### 3.7 Boundary: face-exact (McCormick) relaxations

- Instance: `f(x,y) = 2|x-a| - (x-a)(y-b)` on `[0,1]^2`, with `a = 1/3` and
  `b = sqrt 2 - 1`.
- Minimizers: `f >= (2-|y-b|)|x-a| >= 0`, so the segment `x = a` is optimal
  (`p = 1`).
- Relaxation: the McCormick envelope of `-(x-a)(y-b)`.
- Certificate: the partition `{x <= a}, {x >= a}` is a 2-leaf certificate
  for every `eps >= 0`, because the envelope is exact on the face `x = a`.
  The script checks that both relaxation values are 0.
- Widest-side bisection: every dyadic square of side `s` that straddles
  `x = a` has relaxation value at most `-s^2/6`. To see this, evaluate the
  envelope at `X = 0` and the `y`-midpoint; `a` sits at relative position
  1/3 or 2/3 of every dyadic `x`-interval. About `1/s` such squares exist per
  level, so bisection needs at least order `eps^(-1/2)` nodes. The numerics
  are consistent with `Theta(eps^(-1/2))`.
- Branching only on `x` gives `Theta(log(1/eps))`. Splitting at the LP
  solution on the most central coordinate gives 3 nodes.

Theorems B and D therefore rely on (G_alpha). Without it, the exponent
depends on how the near-optimal set aligns with coordinate hyperplanes. That
is Q2.

### 3.8 Computations

The toy branch-and-bound uses:

- the scheme and bounds of 3.1–3.4;
- incumbent fixed at `f*`;
- node lower bounds from exact 1D convex bisection or separable solves, or
  L-BFGS-B followed by a Frank–Wolfe dual bound;
- in 1D, the exact optimal certificate by a greedy cover, which is optimal
  because validity passes to subintervals;
- the Theorem B bound by quadrature.

These are floating-point illustrations, not certified counts. The table
reports **nodes** for the rules. Binary trees have `leaves = (nodes+1)/2`.
The columns `opt` and `LB` report **leaves**. Rules: `bis` = widest-side
bisection; `omega` = split at the relaxation minimizer on the coordinate with
the largest gap term, safeguarded 2% from the bounds; `mix` = `0.8 * minimizer
+ 0.2 * midpoint`, SCIP-like.

| Instance (`alpha`) | eps | bis | omega | mix | opt (1D) | Theorem B LB |
|---|---|---|---|---|---|---|
| 1D `t^2-2t^4` (4.33) | 1e-2 / 1e-5 / 1e-8 | 13 / 37 / 57 | 13 / 35 / 57 | 13 / 33 / 57 | 6 / 13 / 21 | 3.3 / 7.9 / 12.4 |
| 1D `t^4(1-t^2)` (0.30) | 1e-2 / 1e-5 / 1e-8 | 5 / 55 / 303 | 5 / 49 / 297 | 5 / 53 / 301 | 3 / 18 / 101 | 1.3 / 10.7 / 63.6 |
| 1D sharp `2|t|-t^2` (1) | 1e-2 / 1e-5 / 1e-8 | 7 / 17 / 27 | 3 / 3 / 3 | 5 / 9 / 13 | 2 / 2 / 2 | 0.60 / 0.66 / 0.66 |
| 2D sharp `2|t|_1-|t|^2` (1) | 1e-2 / 1e-5 / 1e-8 | 13 / 31 / 53 | 7 / 7 / 7 | 9 / 21 / 31 | – | 0.30 / 0.31 / 0.31 |
| 2D `|t|^2-|t|^4/2` (1.36) | 1e-2 / 1e-5 / 1e-8 | 39 / 105 / 197 | 29 / 101 / 173 | 33 / 101 / 175 | – | 3.0 / 9.0 / 15.0 |
| 2D `t1^2+t2^4-2.5t2^6` (2.36) | 1e-2 / 1e-5 / 1e-8 | 93 / 911 / 5401 | 95 / 833 / 4795 | 97 / 799 / 4743 | – | 10.3 / 92.8 / 550 |
| 2D ring `(|t|^2-0.04)^2` (0.08) | 1e-2 / 1e-5 / 1e-8 | 7 / 601 / 20129 | 7 / 597 / 19825 | 7 / 603 / 19189 | – | 0.76 / 49.0 / 1598 |

Observed exponents over the last three decades:

- Quartic and mixed instances: node ratio per decade of about 1.6–1.9,
  matching `eps^(-1/4)`, whose factor is 1.78.
- Ring: about 2.9–3.1 per decade, matching `eps^(-1/2)`, whose factor is
  3.16.
- Nondegenerate instances: additive growth, which is logarithmic.

Every certificate respects the Theorem B bound. The 1D optimal certificate is
within a factor 1.6–3.3 of the bound. The ratio of bisection leaves to the
bound is stable, about 2.3 in 1D and 5–7 in 2D, on the (QD) instances. For
the sharp instances the ratio grows like `log(1/eps)`.

McCormick face example (`run_mccormick.log`), widest bisection / x-only
bisection / omega: 21 / 11 / 3 nodes at `1e-2`, and 8189 / 45 / 3 at `1e-7`.

1D OBBT check (`run_obbt_1d.log`), relaxations with OBBT versus plain
bisection:

- Smooth instances: 74 versus 57 for `t^2-2t^4` at `1e-8`, and 506 versus
  303 for the quartic. OBBT adds relaxations. The certificate leaves, which
  include removed pieces, stay above the Theorem B bound, as Corollary 3.3
  requires.
- Sharp instance: 4 versus 27. Here OBBT collapses boxes onto the minimizer,
  in line with Proposition 2 of the repository's iterated-OBBT theory.

Targeted commands run, from `research-20260928b/scouting/spatial-bb-theory/`,
with the final code:

- `python3 sbb_toy.py nondeg1 quartic1 sharp1 sharp2 mixed2`, logged in
  `run_sep.log`. This run used an earlier `mixed2` that turned out to be
  convex (`alpha = 0`), so its lines were removed from the log.
- `python3 sbb_toy.py nondeg2 ring2`, logged in `run_2d.log`.
- `python3 sbb_toy.py mixed2` with the corrected nonconvex `mixed2`, logged
  in `run_mixed2.log`.
- `python3 mccormick_face.py`, logged in `run_mccormick.log`.
- `python3 obbt_1d.py`, logged in `run_obbt_1d.log`.

Earlier exploratory runs used superseded node solvers and are not reported.
No project-wide checks were run and CI was not inspected.

### 3.9 Attack plan, difficulty and risk

1. **Consolidate A–D.** This is easy.
   - Obtain an independent adversarial review of the four proofs and of
     Lemma 0's treatment of OBBT pieces.
   - Tighten constants.
   - State the one-sided versus two-sided gap hypotheses exactly.
   - Add the first-order analogue. With gap at least `alpha * w * (distance
     to the faces)`, the exponent becomes `n` instead of `n/2`, which ties
     the result to Bachoc et al.
2. **Constrained stratified characterization (Q1a).** This is moderate.
   - Prove the key lemma
     `integral_{S∩B} q_B^(-d/2) dσ <= C(n,d,S)` for all boxes.
   - Combine it with the repository's cluster-free inequality
     `L(Z) >= f* + c1 dist^2 - c2 w^2` across scales for the matching
     bisection upper bound.
   - Risk: the constants may depend on LICQ and curvature in a way that
     needs care at stratum boundaries.
3. **Instance-optimal branching (Q1b).** This is moderate to hard.
   - Analyse safeguarded omega-subdivision. Show that it charges to vertices
     of an optimal certificate at sharp minima and does no worse than
     bisection under (QD), or construct a counterexample. Numerics show
     `mix` still grows logarithmically at sharp minima.
   - A negative result in the style of Cheng–Basu is a plausible
     alternative outcome.
4. **Validation.** Estimate `dim` of the near-optimal set on a few symmetric
   or degenerate MINLPLib-type instances. Check whether solver node counts
   against `eps` follow `eps^(-p/2)`, and whether symmetry-breaking
   constraints reduce the exponent as predicted.

Main risks:

- **Originality.** The integral idea is the smooth, white-box analogue of
  Hansen–Jaumard–Lu and Bachoc–Cesari–Gerchinovitz. The partition proofs are
  short, and the interval-analysis literature was not checked.
- **Scope.** Real solvers use McCormick-type face-exact relaxations and
  box-dependent `alpha`, so Theorems B and D apply only to (G_alpha)
  schemes. Q2 is needed for mainstream relaxations.
- **Constants.** Constants that are exponential in `n` limit quantitative
  predictions.

## 4. Significance

**Proved here (first pass, unreviewed):**

- The first lower bounds, as far as the bounded search found, on the total
  tree size in `eps` for adaptive spatial branch-and-bound. They hold for
  (G_alpha) relaxations under every branching rule and node order, and with
  same-relaxation OBBT.
- Tight `eps`-rates for nondegenerate, degenerate and non-isolated minima.
- An `eps^(-p/2)` lower bound for any `p`-dimensional feasible set of
  `eta`-optimal points, which applies to constrained problems.
- Uniform bisection is instance-optimal up to `e^{O(n)}` under (QD), and up
  to a tight `log(1/eps)` factor in general.
- An explicit example where a face-exact relaxation makes branching-point
  placement worth a polynomial factor in `1/eps`.

**Plausible solver consequences:**

- A quantitative case for **symmetry breaking and degeneracy removal** in
  continuous global optimization. Each continuous dimension of the optimal
  set costs a factor `eps^(-1/2)`, and within (G_alpha) schemes no branching
  rule or same-relaxation tightening can avoid it.
- A diagnostic: the slope of `log(nodes)` against `log(1/eps)` estimates the
  effective dimension of the near-optimal set.
- Guidance that splitting at relaxation solutions is worth its cost mainly at
  sharp or vertex minima and at axis-aligned degenerate structure, not at
  smooth nondegenerate minima.

**Speculative:**

- Adaptive choice of tolerance, relaxation order or branching point from
  on-line estimates of the certificate integral.
- A normalized benchmark for learned branching that divides node counts by
  the instance's certificate integral.

**Needed for practical value:** the Q2 extension to McCormick and multilinear
relaxations, a constrained theory (Q1a), and evidence on real instances. None
of these is established here.

## 5. Recommendation

Pursue **Q1**, the instance-dependent node complexity of spatial
branch-and-bound.

- Start by getting Theorems A–D reviewed, since their proofs are short and
  checkable.
- Then extend to constrained stratified integrals and to the question of
  whether a local branching rule removes bisection's `log(1/eps)` loss.
- Keep **Q2** (face-exact relaxations) as the bridge to mainstream McCormick
  solvers.
- Keep **Q3** (robust-point certified upper bounds) as a secondary,
  well-posed direction adjacent to the repository's equality work.

The package unifies the cluster literature and supplies its missing lower
bounds. It also complements the repository's exponential-in-`n` lower bounds
with exact `eps`-dependence.

Its weaknesses:

- The core idea parallels known Lipschitz results.
- The cleanest theorems require an alphaBB-type gap.
- Practical speedups remain speculative.

**Score: 6/10.** Significance is moderate, feasibility high and originality
moderate and not yet verified.
